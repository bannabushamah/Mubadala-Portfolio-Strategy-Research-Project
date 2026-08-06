# My Power BI Build Guide
### Mubadala Portfolio Strategy report

I built the data model and wrote the DAX; I shipped a
browser dashboard since I work on a Mac, and here is my exact build guide so it can be
done in Power BI.

---

## 1. Load the data

`Home → Get Data → Text/CSV`. Load all seventeen files from `01_data/powerbi_exports/`.

In **Power Query Editor**, for every table:

1. `Transform → Use First Row as Headers` (usually automatic)
2. Check each column's data type in the header icon. Fix these specifically:
   - `announce_date` → **Date**
   - `value_usd_m`, `weight_pct`, `pe_ttm`, all `_bn` and `_m` columns → **Decimal Number**
   - all `_id` columns → **Whole Number**
3. `Home → Close & Apply`

**Why fix types manually?** Power BI guesses from the first 200 rows. `value_usd_m` has
blanks in the first rows (undisclosed deals), so it often guesses *Text*, and every
measure that sums it then silently returns blank. This is the single most common reason
a beginner's Power BI report shows empty cards.

---

## 2. Build the star schema

`Model view` → drag to create relationships. Set each one to **Many-to-one, single direction**.

| From (many) | To (one) | Cardinality |
|---|---|---|
| `fact_holding[sector_id]` | `dim_sector[sector_id]` | Many-to-one |
| `fact_holding[geo_id]` | `dim_geography[geo_id]` | Many-to-one |
| `fact_holding[platform_id]` | `dim_platform[platform_id]` | Many-to-one |
| `fact_transaction[sector_id]` | `dim_sector[sector_id]` | Many-to-one |
| `fact_transaction[geo_id]` | `dim_geography[geo_id]` | Many-to-one |
| `fact_transaction[platform_id]` | `dim_platform[platform_id]` | Many-to-one |
| `fact_transaction[announce_date]` | `dim_date[date]` | Many-to-one |
| `fact_market_data[sector_id]` | `dim_sector[sector_id]` | Many-to-one |
| `fact_asset_allocation[asset_class_id]` | `dim_asset_class[asset_class_id]` | Many-to-one |
| every fact `[source_id]` | `dim_source[source_id]` | Many-to-one |

Then mark the date table: select `dim_date` → `Table tools → Mark as date table` → column `date`.

**Why a star and not one big table?** Power BI's storage engine compresses columns, and
its filter engine propagates *from* dimensions *into* facts. A flat table duplicates every
text field on every row, inflates the model, and makes slicers ambiguous when two facts
share a concept (a sector slicer would have to filter holdings and deals separately).
One dimension, filtering many facts, is the whole point.

---

## 3. DAX measures

Create a blank table called `_Measures` (`Home → Enter Data`, name it `_Measures`, delete
the column) and put every measure in it. Keeping measures out of fact tables makes them
easy to find.

```dax
-- ============ PORTFOLIO SCALE ============
Total AUM (USD bn) =
CALCULATE ( SUM ( fact_performance[value] ),
    fact_performance[metric] = "AUM (USD bn)", fact_performance[year] = 2025 )

AUM Growth % =
CALCULATE ( SUM ( fact_performance[value] ),
    fact_performance[metric] = "AUM growth YoY (%)" ) / 100

Five Year IRR =
CALCULATE ( SUM ( fact_performance[value] ),
    fact_performance[metric] = "5-year annualised IRR (%)" ) / 100

-- ============ CAPITAL FLOW ============
Capital Deployed = SUM ( fact_capital_flow[deployments_usd_bn] )
Proceeds         = SUM ( fact_capital_flow[proceeds_usd_bn] )

Recycling Ratio =
DIVIDE ( [Proceeds], [Capital Deployed] )

Net Deployment =
[Capital Deployed] - [Proceeds]

Deployment YoY % =
VAR Prior =
    CALCULATE ( [Capital Deployed],
        FILTER ( ALL ( fact_capital_flow ),
                 fact_capital_flow[year] = MAX ( fact_capital_flow[year] ) - 1 ) )
RETURN DIVIDE ( [Capital Deployed] - Prior, Prior )

-- ============ PORTFOLIO COMPOSITION ============
Holdings Count = COUNTROWS ( fact_holding )

Holdings % of Total =
DIVIDE ( [Holdings Count], CALCULATE ( [Holdings Count], ALL ( fact_holding ) ) )

AI-Exposed Holdings =
CALCULATE ( [Holdings Count], dim_sector[ai_exposure] = "High" )

AI Exposure % =
DIVIDE ( [AI-Exposed Holdings], [Holdings Count] )

International Share % =
DIVIDE (
    CALCULATE ( [Holdings Count], dim_geography[region] <> "Middle East" ),
    [Holdings Count] )

-- ============ CONCENTRATION ============
-- Herfindahl-Hirschman Index of the asset-class mix.
-- Below 1500 unconcentrated | 1500-2500 moderate | above 2500 concentrated.
HHI Asset Class =
SUMX ( fact_asset_allocation,
       fact_asset_allocation[weight_pct] * fact_asset_allocation[weight_pct] )

Effective Number of Buckets =
DIVIDE ( 1, DIVIDE ( [HHI Asset Class], 10000 ) )

Concentration Verdict =
SWITCH ( TRUE (),
    [HHI Asset Class] < 1500, "Unconcentrated",
    [HHI Asset Class] < 2500, "Moderately concentrated",
    "Concentrated" )

-- ============ DEAL FLOW ============
Deal Count = COUNTROWS ( fact_transaction )

Disclosed Deal Value (USD bn) =
DIVIDE ( SUM ( fact_transaction[value_usd_m] ), 1000 )

Deals With Disclosed Value =
CALCULATE ( [Deal Count], NOT ISBLANK ( fact_transaction[value_usd_m] ) )

Disclosure Rate % =
DIVIDE ( [Deals With Disclosed Value], [Deal Count] )

-- Honest label: never present a partial sum as a total.
Deal Value Label =
"US$" & FORMAT ( [Disclosed Deal Value (USD bn)], "0.0" ) & "bn disclosed across "
      & [Deals With Disclosed Value] & " of " & [Deal Count] & " deals"

-- ============ EVIDENCE QUALITY ============
Official Share % =
DIVIDE ( CALCULATE ( [Holdings Count], fact_holding[evidence_grade] = "Official" ),
         [Holdings Count] )

-- ============ VALUATION ============
Median Peer PE =
MEDIANX ( FILTER ( fact_market_data, NOT ISBLANK ( fact_market_data[pe_ttm] ) ),
          fact_market_data[pe_ttm] )

Median Peer EV/EBITDA =
MEDIANX ( FILTER ( fact_market_data, NOT ISBLANK ( fact_market_data[ev_ebitda] ) ),
          fact_market_data[ev_ebitda] )

Peer PE Premium =
VAR SelectedPE = SELECTEDVALUE ( fact_market_data[pe_ttm] )
RETURN SelectedPE - [Median Peer PE]

-- ============ GLOBALFOUNDRIES DRILL-DOWN ============
GFS Revenue = SUM ( fact_gfs_financials[revenue_usd_m] )
GFS FCF     = SUM ( fact_gfs_financials[free_cash_flow_usd_m] )

GFS FCF Margin % = DIVIDE ( [GFS FCF], [GFS Revenue] )

GFS Segment Mix % =
DIVIDE ( SUM ( fact_gfs_segment[revenue_usd_m] ),
         CALCULATE ( SUM ( fact_gfs_segment[revenue_usd_m] ),
                     ALL ( fact_gfs_segment[end_market] ) ) )

-- ============ OMV DIVIDEND SAFETY ============
OMV FCF = SUM ( fact_omv_financials[free_cash_flow_eur_m] )

OMV Dividend Cost =
SUMX ( fact_omv_financials, fact_omv_financials[dps_eur] * 326 )

OMV Dividend Cover = DIVIDE ( [OMV FCF], [OMV Dividend Cost] )

OMV Cover Status =
SWITCH ( TRUE (),
    [OMV Dividend Cover] < 1,   "NOT COVERED",
    [OMV Dividend Cover] < 1.5, "THIN",
    "COMFORTABLE" )
```

---

## 4. Build the four report pages

### Page 1 — Overview
| Visual | Type | Fields |
|---|---|---|
| Four KPI cards | Card | `Total AUM (USD bn)`, `Five Year IRR`, `Capital Deployed`, `Proceeds` |
| Asset-class mix | Donut | Legend `dim_asset_class[asset_class]`, Values `weight_pct` |
| Deployed vs proceeds | Clustered column | Axis `fact_capital_flow[year]`, Values `Capital Deployed`, `Proceeds` |
| Concentration | Card | `Concentration Verdict` with `HHI Asset Class` as a subtitle |

### Page 2 — Portfolio composition
| Visual | Type | Fields |
|---|---|---|
| Slicers | Slicer ×3 | `dim_sector[sector_name]`, `dim_geography[region]`, `dim_platform[platform_name]` |
| By sector | Bar | Axis `dim_sector[sector_name]`, Values `Holdings Count`, colour by `ai_exposure` |
| By region | Map (filled) | Location `dim_geography[country]`, Colour saturation `Holdings Count` |
| Holdings table | Table | holding name, sector, country, platform, ownership, evidence grade |

**Conditional formatting for the evidence column:** select the table → Format → Cell
elements → `evidence_grade` → Background colour → Rules → `Official` green, everything
else amber. This makes provenance visible at a glance, which is the point of the column.

### Page 3 — Investment trends
| Visual | Type | Fields |
|---|---|---|
| Deals over time | Line + column | Axis `dim_date[year_quarter]`, Column `Deal Count`, Line `Disclosed Deal Value (USD bn)` |
| Sector × platform | Matrix | Rows `platform_name`, Columns `sector_name`, Values `Deal Count` |
| Honesty banner | Card | `Deal Value Label` |
| Deal log | Table | date, target, type, sector, country, value |

### Page 4 — Valuation case studies
| Visual | Type | Fields |
|---|---|---|
| Peer multiples | Scatter | X `revenue_ttm_bn`, Y `pe_ttm`, Size `mkt_cap_bn`, Legend `sector_name`, Details `ticker` |
| GFS revenue mix | 100% stacked column | Axis `fact_gfs_segment[year]`, Legend `end_market`, Values `GFS Segment Mix %` |
| OMV dividend cover | Line + column | Axis `year`, Column `OMV FCF` and `OMV Dividend Cost`, Line `OMV Dividend Cover` |
| Football fields | Static images | Import from `07_charts/07_...png` and `14_...png` |

---

## 5. Finishing touches that make it look professional

1. **Theme.** `View → Themes → Customise`. Set: `#0B2545` navy, `#C9A227` gold,
   `#1B7F79` teal, `#5A6B7B` slate, `#A6432F` rust. Consistent colour across pages is
   the single cheapest thing that makes a report look considered.
2. **Turn off the visual borders and shadows** on every chart, then add a single subtle
   card background. Less chrome, more data.
3. **Sync the slicers.** `View → Sync slicers` so a sector filter on page 2 carries to page 3.
4. **Add tooltips.** Create a hidden page sized *Tooltip*, put the investment thesis text
   on it, and set the holdings table's tooltip page to it.
5. **Add a "Sources" page** listing `dim_source`. Any report that cites its own sources
   inside the report itself is immediately more credible than one that does not.
6. **Publish** to the Power BI Service and share a read-only link on your CV.

---

## 6. Common problems and fixes

| Symptom | Cause | Fix |
|---|---|---|
| Cards show *(Blank)* | `value_usd_m` loaded as Text | Change the column type to Decimal Number in Power Query |
| Slicer filters one chart but not another | Missing relationship, or a bidirectional one creating ambiguity | Model view: every fact must have a single-direction path to the dimension |
| Totals do not match the sum of rows | You used an implicit `Sum of column` instead of a measure | Always write a measure; never drag a raw column into Values |
| Date hierarchy missing | `dim_date` not marked as a date table | Table tools → Mark as date table |
| Map shows nothing | Country names not recognised | Set `dim_geography[country]` Data category to *Country/Region* |
| Percentages sum to more than 100% | Filter context ignored in the denominator | Use `ALL()` or `ALLSELECTED()` deliberately, and know which one you meant |

---

## 7. What to say about this in an interview

- *"I modelled it as a star schema so one sector slicer filters holdings, deals and market
  data through a single dimension, rather than duplicating text across a flat table."*
- *"I wrote a disclosure-rate measure because thirteen of nineteen deals have no published
  value. Reporting a 'total deal value' from public sources would have been misleading, so
  the report shows the disclosed floor and labels it as such."*
- *"The concentration measure is a Herfindahl index in DAX — it comes out at 2,734, which
  is formally concentrated, and the effective number of independent buckets is 3.7 rather
  than 5."*
- *"I built the browser version because I'm on a Mac. The data model and the DAX are in the
  repository and rebuild in Power BI in under an hour."*
