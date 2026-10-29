"""
Core calculations for The Cost of Utilities project.

Used by the notebook (for the charts and narrative) and to build the data file
the interactive dashboard reads:

    python analysis.py      # writes dashboard/data.js

The key idea: a city's utility bill in USD can rise for three different reasons,
and they add up exactly in log terms:

    ln(USD change) = ln(local inflation) + ln(real utilities change) - ln(FX change)

    * local inflation        - general price growth in that country (CPI)
    * real utilities change  - utilities rising faster/slower than CPI
                               (the "is it in line with inflation?" question)
    * FX change              - the local currency weakening against the USD
                               lowers the USD bill even if local prices rise
"""

import json
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).parent
DATA_DIR = ROOT / "data"
REGIONS = ["Europe", "Middle East", "Asia", "North America",
           "South America", "Oceania", "Africa"]


def load(data_dir=DATA_DIR):
    """Merge utilities, city metadata and macro data into one city-year table."""
    data_dir = Path(data_dir)
    cities = pd.read_csv(data_dir / "cities.csv")
    util = pd.read_csv(data_dir / "utilities_monthly_usd.csv")
    macro = pd.read_csv(data_dir / "macro.csv")
    if util.empty:
        return pd.DataFrame()

    df = (util.merge(cities, on="city", how="left")
              .merge(macro.drop(columns="source", errors="ignore"), on=["iso3", "year"], how="left")
              .sort_values(["city", "year"])
              .reset_index(drop=True))

    unknown = df[df.region.isna()].city.unique()
    if len(unknown):
        raise ValueError(f"Cities missing from cities.csv: {list(unknown)}")

    df["utilities_lcu"] = df.utilities_usd * df.fx_lcu_per_usd
    df["cpi_level"] = cpi_level(df)

    us = df[df.iso3 == "USA"][["year", "cpi_level"]].rename(columns={"cpi_level": "us_cpi_level"})
    if us.empty:  # US CPI is needed to deflate USD figures
        us = macro[macro.iso3 == "USA"].assign(cpi_level=lambda m: cpi_level(m))
        us = us[["year", "cpi_level"]].rename(columns={"cpi_level": "us_cpi_level"})
    df = df.merge(us.drop_duplicates("year"), on="year", how="left")

    g = df.groupby("city")
    first = lambda col: g[col].transform("first")
    df["usd_index"] = 100 * df.utilities_usd / first("utilities_usd")
    df["lcu_index"] = 100 * df.utilities_lcu / first("utilities_lcu")
    df["cpi_index"] = 100 * df.cpi_level / first("cpi_level")
    df["fx_index"] = 100 * df.fx_lcu_per_usd / first("fx_lcu_per_usd")
    df["real_usd"] = df.utilities_usd * first("us_cpi_level") / df.us_cpi_level
    df["usd_yoy_pct"] = 100 * g.utilities_usd.pct_change()
    df["lcu_yoy_pct"] = 100 * g.utilities_lcu.pct_change()
    return df


def cpi_level(frame):
    """CPI level per row: the World Bank index where present, otherwise a level
    chained from IMF annual inflation (index 100 in each country's first year)."""
    out = pd.Series(np.nan, index=frame.index)
    for _, idx in frame.groupby("iso3").groups.items():
        sub = frame.loc[idx].sort_values("year")
        if sub.cpi_index.notna().all():
            out.loc[sub.index] = sub.cpi_index.values
        else:
            growth = (1 + sub.cpi_inflation_pct / 100).fillna(1.0).to_numpy(copy=True)
            growth[0] = 1.0
            out.loc[sub.index] = 100 * np.cumprod(growth)
    return out


def city_summary(df):
    """One row per city: change from first to latest year and its decomposition."""
    rows = []
    for city, s in df.groupby("city"):
        a, b = s.iloc[0], s.iloc[-1]
        usd = b.utilities_usd / a.utilities_usd
        lcu = b.utilities_lcu / a.utilities_lcu
        cpi = b.cpi_level / a.cpi_level
        fx = b.fx_lcu_per_usd / a.fx_lcu_per_usd
        us_cpi = b.us_cpi_level / a.us_cpi_level
        rows.append({
            "city": city, "country": a.country, "region": a.region, "currency": a.currency,
            "start_year": int(a.year), "end_year": int(b.year),
            "start_usd": a.utilities_usd, "end_usd": b.utilities_usd,
            "usd_change_pct": 100 * (usd - 1),
            "lcu_change_pct": 100 * (lcu - 1),
            "local_inflation_pct": 100 * (cpi - 1),
            "real_change_pct": 100 * (lcu / cpi - 1),       # vs local inflation
            "real_usd_change_pct": 100 * (usd / us_cpi - 1),  # in constant US dollars
            "fx_change_pct": 100 * (fx - 1),                 # + = currency weakened
            # log-point decomposition of the USD change (sums exactly)
            "lp_inflation": 100 * np.log(cpi),
            "lp_real": 100 * np.log(lcu / cpi),
            "lp_fx": -100 * np.log(fx),
            "lp_total": 100 * np.log(usd),
            "peak_year": int(s.loc[s.utilities_usd.idxmax(), "year"]),
            "peak_usd": s.utilities_usd.max(),
        })
    out = pd.DataFrame(rows)
    out["beat_inflation"] = out.real_change_pct > 0
    return out.sort_values("end_usd", ascending=False).reset_index(drop=True)


def region_series(df):
    """Median of each city's 2020=100 index per region and year."""
    return (df.groupby(["region", "year"])
              .agg(usd_index=("usd_index", "median"), lcu_index=("lcu_index", "median"),
                   cpi_index=("cpi_index", "median"), real_usd=("real_usd", "median"),
                   utilities_usd=("utilities_usd", "median"), cities=("city", "nunique"))
              .reset_index())


def findings(df, summary):
    """Headline facts computed from the data (no hard-coded conclusions)."""
    if summary.empty:
        return {}
    end_year = int(df.year.max())
    latest = df[df.year == end_year]
    us = df.drop_duplicates("year").set_index("year").us_cpi_level.dropna()
    return {
        "start_year": int(df.year.min()),
        "end_year": end_year,
        "n_cities": int(summary.city.nunique()),
        "median_bill_end": float(latest.utilities_usd.median()),
        "median_usd_change_pct": float(summary.usd_change_pct.median()),
        "median_real_change_pct": float(summary.real_change_pct.median()),
        "us_cpi_change_pct": float(100 * (us.iloc[-1] / us.iloc[0] - 1)) if len(us) > 1 else None,
        "n_beat_inflation": int(summary.beat_inflation.sum()),
        "most_expensive": summary.iloc[0][["city", "end_usd"]].to_dict(),
        "cheapest": summary.iloc[-1][["city", "end_usd"]].to_dict(),
        "biggest_riser": summary.loc[summary.usd_change_pct.idxmax(), ["city", "usd_change_pct"]].to_dict(),
        "biggest_faller": summary.loc[summary.usd_change_pct.idxmin(), ["city", "usd_change_pct"]].to_dict(),
        "spread_ratio": float(summary.end_usd.max() / summary.end_usd.min()),
        "peak_year_mode": int(summary.peak_year.mode().iloc[0]),
        "fx_dominant_cities": summary.loc[summary.lp_fx.abs() > (summary.lp_inflation + summary.lp_real).abs(),
                                          "city"].tolist(),
    }


def export_dashboard(df, out=ROOT / "dashboard" / "data.js"):
    """Write the dashboard's data as a JS file so index.html also works from file://."""
    summary = city_summary(df) if not df.empty else pd.DataFrame()
    cols = ["city", "region", "year", "utilities_usd", "utilities_lcu", "usd_index",
            "lcu_index", "cpi_index", "fx_index", "real_usd", "usd_yoy_pct", "lcu_yoy_pct"]
    payload = {
        "generated": date.today().isoformat(),
        "regions": REGIONS,
        "rows": clean(df[cols]) if not df.empty else [],
        "cities": clean(summary),
        "regionSeries": clean(region_series(df)) if not df.empty else [],
        "findings": findings(df, summary) if not df.empty else {},
    }
    out.write_text("window.UTILITIES_DATA = " + json.dumps(payload, indent=1, default=float) + ";\n")
    return out


def clean(frame):
    """DataFrame -> records with NaN as null and floats rounded."""
    return json.loads(frame.round(3).to_json(orient="records"))


if __name__ == "__main__":
    import sys
    data = load(sys.argv[1] if len(sys.argv) > 1 else DATA_DIR)
    path = export_dashboard(data, *map(Path, sys.argv[2:3]))
    print(f"{len(data)} city-years -> {path}")
