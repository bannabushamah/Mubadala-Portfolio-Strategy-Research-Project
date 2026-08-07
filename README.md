# Equity Research — Mubadala Portfolio Strategy Analyst

**Author:** Bann · **Status:** ongoing

An independent equity-research project analysing the portfolio strategy, sector allocation and
global investments of **Mubadala Investment Company**, Abu Dhabi's sovereign investor
(US$385bn AUM, FY2025), with four valuation case studies, a SQL data warehouse, an interactive
dashboard, and a quantitative/AI layer.

---

## Headline findings

| Finding | Number | Where |
|---|---|---|
| The asset mix is formally **concentrated** — 5 reported buckets behave like 3.7 | HHI **2,734** | SQL Q8, Report §3.2 |
| Growth is **self-funded**: realisations paid for 97c of every dollar deployed | Recycling ratio **0.97x** | SQL Q3, Report §4 |
| The 20% public-equity sleeve is **liquidity insurance**, priced at ~1pp of volatility | **1.02pp** avoidable risk | Optimiser, Report §9.1 |
| GlobalFoundries at $50 requires a steady-state EBIT margin of 33.4% vs 12.1% today | Reverse DCF | Report §5.2 |
| OMV's dividend cover has collapsed while the dividend was raised every year | **6.0x → 1.3x** | SQL Q11, Report §6.3 |
| WHOOP's $10.1bn Series G assumes a decade of 35% compound growth | → **$21.8bn revenue by 2035** | Report §7.2 |
| 55.8% probability Mubadala crosses **US$1 trillion** AUM by 2035 | 50,000-path Monte Carlo | Report §9.2 |

---

## Four valuation case studies — 4 different problems

| Sector | Subject | The hard part | Method | Result |
|---|---|---|---|---|
| Technology | **GlobalFoundries** (NASDAQ: GFS) | AI optionality isn't in the reported numbers | FCFF DCF + comps + **reverse DCF** | DCF $35.07 vs market $50.01; price implies a 33.4% margin |
| Energy | **OMV AG** (VIE: OMV) | Implausible beta, consolidated minorities, distorted EPS | FCFF DCF with three disclosed adjustments + dividend-cover test | €56.42 vs €54.60 (+3.3%); cover down to 1.3x |
| Healthcare | **WHOOP** (private) | No accounts exist — only a transaction price | **Reverse DCF** on the disclosed Series G | Requires 34.8% CAGR for 10 years |
| Financial services | **Mubadala Capital** | Private, and the asset is a fee stream | Fee-franchise SOTP vs listed alt managers | ~US$1.42bn after a 25% private discount |

---

## Repository map

```
01_data/          Star-schema warehouse (5 dims, 11 facts, 160 source-tagged rows)
                  + 17 Power BI-ready CSV exports including a date dimension
02_sql/           205-line schema · 12 documented analysis queries · SQLite database
03_valuation_models/  Shared valuation engine · 4 case studies · live-formula Excel workbook
04_ai_ml/         Mean-variance optimiser · Monte Carlo · text classifier · peer clustering
05_dashboard/     Self-contained HTML dashboard · 290-line Power BI build statement (25 DAX measures)
06_reports/       Equity research report (20pp)
07_charts/        14 publication-quality figures
verify.py         72 independent checks re-deriving every headline figure
```

---

## Skills demonstrated

**Finance** — FCFF DCF, WACC build-up, CAPM, terminal value, equity bridges with minority interests,
sensitivity grids, trading comparables with disclosed outlier treatment, earnings normalisation,
reverse DCF / expectations investing, dividend-sustainability analysis, fee-franchise valuation,
scenario analysis.

**Data** — Kimball star-schema design, SQL DDL with constraints and indexes, CTEs, window functions
(`SUM OVER`, `LAG`, `RANK`, `NTILE`, `PARTITION BY`), conditional aggregation, self-joins, Herfindahl
concentration in SQL, referential-integrity testing.

**Quant / AI** — Markowitz mean-variance optimisation and efficient frontier, reverse (Black-Litterman
style) optimisation, Monte Carlo simulation with fat-tailed Student-t shocks, drawdown analysis,
TF-IDF + logistic-regression text classification with honest hold-out evaluation, PCA and k-means
clustering with silhouette-based model selection.

**BI / engineering** — Power BI data modelling and 25 DAX measures, dependency-free SVG dashboard,
openpyxl live-formula model generation, ReportLab document engineering, reproducible pipelines,
automated verification.

---

## Reproducing everything

```bash
pip install pandas numpy scipy scikit-learn matplotlib openpyxl reportlab pypdf pillow

python 01_data/build_dataset.py            # build the dimension and core fact tables
python 01_data/build_dataset_2.py          # holdings, transactions, market data
python 02_sql/load_and_run.py              # create the database, run 12 queries
python 03_valuation_models/case_01_globalfoundries.py
python 03_valuation_models/case_02_omv.py
python 03_valuation_models/case_03_whoop.py
python 03_valuation_models/case_04_mubadala_capital.py
python 03_valuation_models/build_excel_model.py
python 04_ai_ml/01_portfolio_optimiser.py
python 04_ai_ml/02_monte_carlo.py
python 04_ai_ml/03_deal_classifier.py
python 04_ai_ml/04_peer_clustering.py
python 07_charts/make_charts.py
python 05_dashboard/build_dashboard.py
python 06_reports/build_report.py
python 06_reports/build_guide.py
python 06_reports/build_notes.py
python verify.py                           # 72 checks — all must pass
```

---

Mubadala does not publish a position-level portfolio. The twenty tracked holdings are a **curated,
source-graded sample**, not the whole book. Ten of nineteen logged transactions disclose no value, so
US$44.4bn is a **floor, not a total**. Capital-market assumptions behind the optimiser and the
simulation are the author's. Two of the four case studies value private companies and are
**frameworks with disclosed assumptions, not valuation opinions**. Every figure carries one of four
evidence grades — Official, Market data, Press reporting, Analyst estimate — and the grade is visible
in the dataset, the dashboard and the report.

*Not affiliated with or endorsed by Mubadala Investment Company.
No position held in any security mentioned.*

**Sources:** Mubadala 2025 Annual Review and press releases (mubadala.com, annual2025.mubadala.com);
StockAnalysis.com / S&P Global Market Intelligence. Latest data from 4 August 2026.
