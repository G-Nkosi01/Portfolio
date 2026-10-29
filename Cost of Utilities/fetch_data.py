"""
Fetch the raw data for The Cost of Utilities project.

Two sources:
  1. Numbeo city history  -> data/utilities_monthly_usd.csv
     "Basic (Electricity, Heating, Cooling, Water, Garbage) for 85m2 Apartment",
     the figure Deutsche Bank's *Mapping the World's Prices* reports quote.
  2. IMF World Economic Outlook (inflation) + World Bank (CPI index, FX)
     -> data/macro.csv

Usage:
    python fetch_data.py             # fetch both
    python fetch_data.py --macro     # macro only
    python fetch_data.py --utilities # Numbeo only

Numbeo's page layout isn't guaranteed to stay stable, so the scraper looks for
the utilities row in any table on the page and reports cities it couldn't
parse. Fill any gaps by hand in data/utilities_monthly_usd.csv, citing the
source in the `source` column.
"""

import argparse
import sys
import time
from io import StringIO
from pathlib import Path

import pandas as pd
import requests

DATA_DIR = Path(__file__).parent / "data"
YEARS = list(range(2020, 2026))
HEADERS = {"User-Agent": "Mozilla/5.0 (portfolio research; cost-of-utilities project)"}
UTILITIES_LABEL = "Basic (Electricity, Heating, Cooling, Water, Garbage)"

cities = pd.read_csv(DATA_DIR / "cities.csv")


# --------------------------------------------------------------------------
# Numbeo utilities history
# --------------------------------------------------------------------------

def get(url, **params):
    """GET with retries and a polite pause between requests."""
    for attempt in range(4):
        try:
            r = requests.get(url, params=params, headers=HEADERS, timeout=30)
            r.raise_for_status()
            time.sleep(1.5)
            return r
        except requests.RequestException as exc:
            if attempt == 3:
                raise
            print(f"  retry {attempt + 1} for {url}: {exc}")
            time.sleep(2 ** (attempt + 1))


def parse_numbeo_history(html):
    """Return {year: usd_value} for the basic-utilities row, or {} if not found."""
    try:
        tables = pd.read_html(StringIO(html))
    except ValueError:
        return {}

    for t in tables:
        t = t.copy()
        t.columns = [str(c).strip() for c in t.columns]
        first_col = t.columns[0]

        # Layout A: items as rows, years as columns
        year_cols = [c for c in t.columns if c[:4].isdigit() and int(c[:4]) in YEARS]
        if year_cols:
            row = t[t[first_col].astype(str).str.contains("Basic (Electricity", regex=False)]
            if not row.empty:
                return {int(c[:4]): to_number(row.iloc[0][c]) for c in year_cols}

        # Layout B: years as rows, items as columns
        util_cols = [c for c in t.columns if "Basic (Electricity" in c]
        if util_cols:
            out = {}
            for _, r in t.iterrows():
                y = str(r[first_col])[:4]
                if y.isdigit() and int(y) in YEARS:
                    out[int(y)] = to_number(r[util_cols[0]])
            if out:
                return out
    return {}


def to_number(x):
    s = str(x).replace("$", "").replace(",", "").replace("\xa0", "").strip()
    try:
        return float(s.split()[0])
    except (ValueError, IndexError):
        return None


def fetch_utilities():
    rows, missing = [], []
    for _, c in cities.iterrows():
        url = f"https://www.numbeo.com/cost-of-living/city-history/in/{c.numbeo_slug}"
        print(f"Numbeo: {c.city} ({url})")
        try:
            values = parse_numbeo_history(get(url, displayCurrency="USD").text)
        except requests.RequestException as exc:
            print(f"  failed: {exc}")
            values = {}
        found = {y: v for y, v in values.items() if v is not None}
        if len(found) < len(YEARS):
            missing.append((c.city, sorted(set(YEARS) - set(found))))
        for y, v in sorted(found.items()):
            rows.append({"city": c.city, "year": y, "utilities_usd": round(v, 2),
                         "source": "Numbeo city history", "notes": ""})

    out = pd.DataFrame(rows, columns=["city", "year", "utilities_usd", "source", "notes"])
    out.to_csv(DATA_DIR / "utilities_monthly_usd.csv", index=False)
    print(f"\nWrote {len(out)} rows to data/utilities_monthly_usd.csv")
    if missing:
        print("Gaps to fill by hand:")
        for city, yrs in missing:
            print(f"  {city}: {yrs}")


# --------------------------------------------------------------------------
# Inflation and exchange rates
# --------------------------------------------------------------------------

def world_bank(indicator):
    """World Bank indicator for all project countries -> {(iso3, year): value}."""
    iso = ";".join(cities.iso3.unique())
    url = f"https://api.worldbank.org/v2/country/{iso}/indicator/{indicator}"
    data = get(url, date=f"{YEARS[0] - 1}:{YEARS[-1]}", format="json", per_page=2000).json()
    if len(data) < 2 or data[1] is None:
        return {}
    return {(d["countryiso3code"], int(d["date"])): d["value"]
            for d in data[1] if d["value"] is not None}


def imf_inflation():
    """IMF WEO average CPI inflation (PCPIPCH) -> {(iso3, year): pct}.
    Preferred over World Bank because it already covers 2025."""
    iso = "/".join(cities.iso3.unique())
    url = f"https://www.imf.org/external/datamapper/api/v1/PCPIPCH/{iso}"
    data = get(url, periods=",".join(map(str, YEARS))).json()
    series = data.get("values", {}).get("PCPIPCH", {})
    return {(i, int(y)): v for i, yrs in series.items() for y, v in yrs.items()}


def fetch_macro():
    print("IMF: CPI inflation")
    infl = imf_inflation()
    print("World Bank: CPI index (2010=100)")
    cpi = world_bank("FP.CPI.TOTL")
    print("World Bank: official exchange rate (LCU per USD)")
    fx = world_bank("PA.NUS.FCRF")

    rows = []
    for iso3 in cities.iso3.unique():
        for y in YEARS:
            rows.append({
                "iso3": iso3, "year": y,
                "cpi_index": cpi.get((iso3, y)),
                "cpi_inflation_pct": infl.get((iso3, y)),
                "fx_lcu_per_usd": 1.0 if iso3 == "USA" else fx.get((iso3, y)),
                "source": "IMF WEO (inflation); World Bank WDI (CPI index, FX)",
            })
    out = pd.DataFrame(rows)
    out.to_csv(DATA_DIR / "macro.csv", index=False)
    print(f"\nWrote {len(out)} rows to data/macro.csv")

    gaps = out[out[["cpi_inflation_pct", "fx_lcu_per_usd"]].isna().any(axis=1)]
    if not gaps.empty:
        print("Gaps to fill by hand (e.g. 2025 FX from the central bank's annual average):")
        print(gaps[["iso3", "year", "cpi_inflation_pct", "fx_lcu_per_usd"]].to_string(index=False))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--macro", action="store_true")
    ap.add_argument("--utilities", action="store_true")
    args = ap.parse_args()
    both = not (args.macro or args.utilities)
    try:
        if args.utilities or both:
            fetch_utilities()
        if args.macro or both:
            fetch_macro()
    except requests.RequestException as exc:
        sys.exit(f"Network error: {exc}\nIs the host allowed in this environment's network settings?")
