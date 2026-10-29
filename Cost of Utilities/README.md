# The Cost of Utilities, 2020–2025

How much does it cost to keep the lights on, the heating or cooling running, the water flowing and the bins emptied in capital cities around the world? Has it risen faster than inflation, and what is really driving the change?

**Data:** Numbeo's *Basic utilities (electricity, heating, cooling, water, garbage) for an 85 m² apartment*, the series used in Deutsche Bank Research's annual *Mapping the World's Prices* reports (and charted by Visual Capitalist). Inflation from the IMF World Economic Outlook; CPI index and exchange rates from the World Bank.

**Cities:** 25 capitals across Europe, the Middle East, Asia, North America, South America, Oceania and Africa (`data/cities.csv`).

## Questions

1. How have utility bills moved since 2020, by region?
2. Which capitals pay the most and the least?
3. Is the increase in line with inflation? (local-currency bill vs local CPI)
4. What drives the change in the dollar bill: local prices or exchange rates?
5. When did the increases hit (the 2022 energy shock)?
6. Do high-inflation countries hold utilities down (regulated tariffs, subsidies)?

## Method

A city's USD bill can change for three reasons, and in log points they add up exactly:

```
ln(USD change) = ln(local inflation) + ln(utilities vs inflation) − ln(currency vs USD)
```

So a falling dollar bill can hide soaring local prices (a collapsing currency), and a rising one can simply reflect general inflation. Separating the three answers "is it in line with inflation?" properly.

## Files

| File | What it does |
|---|---|
| `fetch_data.py` | Downloads Numbeo utilities history and IMF/World Bank inflation and FX into `data/` |
| `analysis.py` | Merges the data, computes indices, real changes and the decomposition; writes `dashboard/data.js` |
| `The Cost of Utilities.ipynb` | Step-by-step analysis with Seaborn/Matplotlib charts and findings |
| `dashboard/index.html` | Interactive dashboard: region filter, nominal/constant/local-currency views, five question panels, findings and a sortable data table |

## Run it

```bash
pip install pandas numpy matplotlib seaborn requests lxml
python fetch_data.py     # fill any gaps it reports by hand in data/*.csv
python analysis.py       # builds dashboard/data.js
open dashboard/index.html
```

Or run the notebook top to bottom. Its last cell also rebuilds the dashboard data.

**Status:** pipeline and dashboard built; waiting on the source data download.

**Tools:** Python, Pandas, NumPy, Seaborn/Matplotlib, HTML/SVG/JavaScript
