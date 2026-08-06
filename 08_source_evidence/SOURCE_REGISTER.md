# Source Register

Every figure in this project traces to one of the ten sources below. Data was collected and
**frozen on 4 August 2026** so that the project is reproducible: re-running the scripts today
gives the same answers as re-running them next year.

## Evidence grades used throughout

| Grade | Definition | Example in this project |
|---|---|---|
| **Official** | Stated by Mubadala or in a company filing | AUM of US$385bn |
| **Market data** | Observable exchange or vendor data | GlobalFoundries enterprise value of US$25.4bn |
| **Press reporting** | Widely reported but not confirmed by Mubadala | The c.80% GlobalFoundries stake |
| **Analyst estimate** | Constructed by the author, with stated reasoning | Every forward growth and margin assumption |

## The sources

| ID | Source | URL | As of | Class |
|---|---|---|---|---|
| S01 | Mubadala press release — *Strong performance by UAE Portfolio Drives Mubadala's Growth in 2025* | https://www.mubadala.com/en/news/strong-performance-by-uae-portfolio-drives-mubadalas-growth-in-2025 | 9 Apr 2026 | Official |
| S02 | Mubadala 2025 Annual Review — Performance Overview | https://annual2025.mubadala.com/en/performance-overview | 9 Apr 2026 | Official |
| S03 | Mubadala 2025 Annual Review — Key Investment Highlights | https://annual2025.mubadala.com/en/key-investment-highlights | 9 Apr 2026 | Official |
| S04 | Mubadala corporate site — Our Structure | https://www.mubadala.com/en/who-we-are/our-structure | 4 Aug 2026 | Official |
| S05 | Mubadala press release — *WHOOP Raises $575 Million at $10.1 Billion Valuation* | https://www.mubadala.com/en/news/whoop-raises-dollar-575-million-at-dollar-10-billion-valuation-to-advance-global-health-platform | 31 Mar 2026 | Official |
| S06 | Mubadala newsroom — 2026 transaction announcements | https://www.mubadala.com/en/media | 4 Aug 2026 | Official |
| S07 | StockAnalysis / S&P Global Market Intelligence — GlobalFoundries (GFS) | https://stockanalysis.com/stocks/gfs/statistics/ | 3 Aug 2026 | Market data |
| S08 | StockAnalysis / S&P Global Market Intelligence — OMV AG (VIE:OMV) | https://stockanalysis.com/quote/vie/OMV/statistics/ | 30 Jun 2026 | Market data |
| S09 | StockAnalysis — listed peer comparison tables | https://stockanalysis.com/stocks/compare/ | 4 Aug 2026 | Market data |
| S10 | Analyst estimates constructed for this project | n/a | 4 Aug 2026 | Analyst estimate |

## What each source contributed

**S01 — 2025 annual results.** AUM of AED1.414 trillion (US$385bn, +17% YoY); five-year IRR 10.7%
and ten-year IRR 10.3%; capital deployed AED143bn (US$39bn, +20%); proceeds AED138bn (US$38bn, +27%).
Also the disclosure that Mubadala has not published annual revenue or net income since 2021, which is
why this project uses IRR and flow metrics rather than earnings.

**S02 — Performance Overview.** The asset-class split (Private 42%, Public 20%, Real Estate &
Infrastructure 17%, Alternatives 16%, Credit 5%); the three-year deployment and proceeds history;
credit ratings for Mamoura Diversified Global Holding PJSC (Aa2 / AA / AA long-term, P-1 / A-1+ / F1+
short-term, all stable outlook). *Note: the geography chart on this page is rendered client-side and
returned zeros — see the Project Notes, entry 1.3.*

**S03 — Key Investment Highlights.** Eight 2025 transactions with disclosed values: Corient tack-ons,
ADIC deployments (AED70bn), Al Maryah Island (AED60bn+), Tabreed (AED3.87bn), the Fortress strategic
partnership (US$1bn to deploy), Nord Anglia Education (US$600m), Mubadala Capital Co-Investment
Fund I (US$550m+) and the Barings real-estate debt partnership (US$500m).

**S04 — Our Structure.** The four investment platforms, their chief executives and their mandates;
the statement that Mubadala Capital manages approximately US$30bn — the single hard input behind
case study 4; and that Mubadala is active in more than fifty countries.

**S05 — WHOOP Series G.** US$575m raised at a US$10.1bn post-money valuation; over 2.5 million
members; 2025 bookings growth of 103% exiting at a US$1.1bn run-rate; operating cash-flow positive
in 2025; 24 billion hours of physiological data; over 600 roles being hired in 2026. Every input to
case study 3.

**S06 — 2026 announcements.** Eleven transactions: Hornsea 3 offshore wind, the Greenlink
interconnector, the WHOOP UAE partnership, CredibleX Series A, Power Factors, the Stonepeak container
leasing platform, TBX Nexxia with Tubacex, the Aldar JV at Masdar City, the CoolIT sale to Ecolab in
a KKR-led US$4.75bn transaction, and the Embraer aerospace agreement.

**S07 / S08 / S09 — market data.** Share prices, market capitalisations, enterprise values, revenue,
EBITDA, cash flow, balance-sheet items, betas and trading multiples for GlobalFoundries, OMV and
seventeen peer companies across semiconductors, energy, alternative asset management and healthcare.

**S10 — analyst estimates.** All forward revenue growth and margin assumptions; the risk-free rates
and equity risk premiums; the sector beta substituted for OMV's raw beta; the capital-market
assumptions behind the optimiser and the Monte Carlo simulation; every input to the Mubadala Capital
model except AUM; and the applied comparable-multiple ranges.

## A note on what is deliberately absent

There is **no position-level portfolio valuation** anywhere in this project, because Mubadala does not
publish one and a number built by guessing would be worse than no number. Where a value is unknown,
the dataset stores `NULL`, the dashboard shows `n/d`, and the report says so.
