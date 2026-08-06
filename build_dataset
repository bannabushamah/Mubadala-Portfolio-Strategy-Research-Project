"""
build_dataset.py
Mubadala Portfolio Strategy Analyst - Data Layer

Builds a star-schema analytical dataset from public disclosures.
Every row carries a source_type + source_ref so the provenance of each
number can be audited. Nothing here is scraped live: the figures were
collected on 4 August 2026 and are frozen for reproducibility.

Author: bann | Aug 2026
"""
import os, csv, json
import pandas as pd

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "warehouse")
os.makedirs(OUT, exist_ok=True)
AED_PER_USD = 3.6725          # UAE dirham is pegged to the US dollar

def w(name, rows, cols):
    df = pd.DataFrame(rows, columns=cols)
    df.to_csv(os.path.join(OUT, name + ".csv"), index=False)
    print(f"  {name:32s} {len(df):>4} rows x {len(cols)} cols")
    return df

# --------------------------------------------------------------------------
# DIMENSION: source register  (audit trail for every fact table)
# --------------------------------------------------------------------------
sources = [
 ("S01","Mubadala press release - 2025 annual results","https://www.mubadala.com/en/news/strong-performance-by-uae-portfolio-drives-mubadalas-growth-in-2025","2026-04-09","Official"),
 ("S02","Mubadala 2025 Annual Review - Performance Overview","https://annual2025.mubadala.com/en/performance-overview","2026-04-09","Official"),
 ("S03","Mubadala 2025 Annual Review - Key Investment Highlights","https://annual2025.mubadala.com/en/key-investment-highlights","2026-04-09","Official"),
 ("S04","Mubadala corporate site - Our Structure (platforms)","https://www.mubadala.com/en/who-we-are/our-structure","2026-08-04","Official"),
 ("S05","Mubadala press release - WHOOP Series G","https://www.mubadala.com/en/news/whoop-raises-dollar-575-million-at-dollar-10-billion-valuation-to-advance-global-health-platform","2026-03-31","Official"),
 ("S06","Mubadala newsroom - 2026 transaction announcements","https://www.mubadala.com/en/media","2026-08-04","Official"),
 ("S07","StockAnalysis / S&P Global Market Intelligence - GlobalFoundries (GFS)","https://stockanalysis.com/stocks/gfs/statistics/","2026-08-03","Market data"),
 ("S08","StockAnalysis / S&P Global Market Intelligence - OMV AG (VIE:OMV)","https://stockanalysis.com/quote/vie/OMV/statistics/","2026-06-30","Market data"),
 ("S09","StockAnalysis - listed peer comparison tables","https://stockanalysis.com/stocks/compare/","2026-08-04","Market data"),
 ("S10","Analyst estimate constructed for this project","n/a","2026-08-04","Analyst estimate"),
]
w("dim_source", sources, ["source_id","source_name","source_url","as_of_date","source_class"])

# --------------------------------------------------------------------------
# DIMENSION: investment platforms  (source S04)
# --------------------------------------------------------------------------
platforms = [
 (1,"UAE Investments","Dr. Bakheet Al Katheeri","National investment vehicle building homegrown champions and industrial clusters across energy, metals, aerospace, technology, healthcare, real estate and infrastructure.","Domestic","S04"),
 (2,"Private Equity","Camilla Languille & Luca Molinari","Global direct buyout and late-stage growth equity across technology, healthcare, consumer, financial services, energy & sustainability, industrials & business services. Primary focus North America and Europe with increasing Asia exposure.","Global","S04"),
 (3,"Credit and Special Situations","Hani Ahmad Barhoush","Private debt, GP stakes, secondaries and opportunistic capital-structure solutions. Home to Mubadala Capital (c.US$30bn across balance sheet and third-party vehicles).","Global","S04"),
 (4,"Real Assets","Khaled Al Shamlan Al Marri","Real estate and infrastructure delivering steady, visible cash flows across business cycles.","Global","S04"),
]
w("dim_platform", platforms, ["platform_id","platform_name","platform_ceo","mandate","reach","source_id"])

# --------------------------------------------------------------------------
# DIMENSION: sectors
# --------------------------------------------------------------------------
sectors = [
 (1,"Technology","Growth / Disruption","High"),
 (2,"Healthcare & Life Sciences","Growth / Defensive","High"),
 (3,"Energy & Sustainability","Transition / Cyclical","Medium"),
 (4,"Financial Services","Compounding / Fee-based","High"),
 (5,"Real Estate & Infrastructure","Yield / Inflation-linked","Low"),
 (6,"Industrials & Business Services","Cyclical","Medium"),
 (7,"Consumer & Education","Defensive","Low"),
 (8,"Aerospace & Defence","Strategic / Sovereign","Medium"),
 (9,"Metals & Mining","Cyclical / Strategic","Low"),
 (10,"Mobility & Logistics","Cyclical","Low"),
 (11,"Telecom & Space","Strategic / Sovereign","Medium"),
 (12,"Multi-sector","Diversified","n/a"),
]
w("dim_sector", sectors, ["sector_id","sector_name","strategic_theme","ai_exposure"])

# --------------------------------------------------------------------------
# DIMENSION: geography
# --------------------------------------------------------------------------
geos = [
 (1,"United Arab Emirates","Middle East","AED","Home market"),
 (2,"United States","North America","USD","Developed"),
 (3,"United Kingdom","Europe","GBP","Developed"),
 (4,"Austria","Europe","EUR","Developed"),
 (5,"Germany","Europe","EUR","Developed"),
 (6,"Brazil","Latin America","BRL","Emerging"),
 (7,"Canada","North America","CAD","Developed"),
 (8,"Ireland","Europe","EUR","Developed"),
 (9,"Spain","Europe","EUR","Developed"),
 (10,"India","Asia-Pacific","INR","Emerging"),
 (11,"China","Asia-Pacific","CNY","Emerging"),
 (12,"Multi-geography","Global","USD","Blended"),
]
w("dim_geography", geos, ["geo_id","country","region","currency","market_class"])

# --------------------------------------------------------------------------
# DIMENSION: asset class + official 2025 weights  (source S02)
# --------------------------------------------------------------------------
asset_classes = [
 (1,"Private",42.0,"Direct private equity and private co-investments","S02"),
 (2,"Public",20.0,"Listed equities and public market mandates","S02"),
 (3,"Real Estate & Infrastructure",17.0,"Physical real assets","S02"),
 (4,"Alternatives",16.0,"Funds, GP stakes, secondaries, hedge strategies","S02"),
 (5,"Credit",5.0,"Private and structured credit","S02"),
]
w("dim_asset_class", asset_classes, ["asset_class_id","asset_class","weight_2025_pct","description","source_id"])

# --------------------------------------------------------------------------
# FACT: headline performance  (sources S01, S02)
# --------------------------------------------------------------------------
perf = [
 (2025,"AUM (AED bn)",1414.0,"Official","S01"),
 (2025,"AUM (USD bn)",385.0,"Official","S01"),
 (2024,"AUM (USD bn)",329.1,"Derived from +17% YoY disclosure","S01"),
 (2025,"AUM growth YoY (%)",17.0,"Official","S01"),
 (2025,"5-year annualised IRR (%)",10.7,"Official","S01"),
 (2025,"10-year annualised IRR (%)",10.3,"Official","S01"),
 (2025,"Capital deployed (USD bn)",39.0,"Official","S01"),
 (2025,"Capital deployed (AED bn)",143.0,"Official","S01"),
 (2025,"Proceeds (USD bn)",38.0,"Official","S01"),
 (2025,"Proceeds (AED bn)",138.0,"Official","S01"),
 (2025,"Deployment growth YoY (%)",20.0,"Official","S01"),
 (2025,"Proceeds growth YoY (%)",27.0,"Official","S01"),
]
w("fact_performance", perf, ["year","metric","value","basis","source_id"])

# --------------------------------------------------------------------------
# FACT: capital flow history  (source S02)
# --------------------------------------------------------------------------
flows = [
 (2023,24.0,27.0),
 (2024,32.0,30.0),
 (2025,39.0,38.0),
]
flows = [(y,d,p,round(d-p,1),"Official","S02") for y,d,p in flows]
w("fact_capital_flow", flows, ["year","deployments_usd_bn","proceeds_usd_bn","net_deployment_usd_bn","basis","source_id"])

# --------------------------------------------------------------------------
# FACT: asset class allocation  (source S02)
# --------------------------------------------------------------------------
alloc = [(2025, ac[0], ac[1], ac[2], round(385.0*ac[2]/100,1), "S02") for ac in asset_classes]
w("fact_asset_allocation", alloc, ["year","asset_class_id","asset_class","weight_pct","implied_usd_bn","source_id"])

# --------------------------------------------------------------------------
# FACT: credit ratings  (source S02)
# --------------------------------------------------------------------------
ratings = [
 ("Moody's","Long-term","Aa2","Stable","S02"),
 ("S&P Global","Long-term","AA","Stable","S02"),
 ("Fitch","Long-term","AA","Stable","S02"),
 ("Moody's","Short-term","P-1","Stable","S02"),
 ("S&P Global","Short-term","A-1+","Stable","S02"),
 ("Fitch","Short-term","F1+","Stable","S02"),
]
w("fact_credit_rating", ratings, ["agency","tenor","rating","outlook","source_id"])

print("\nData layer part 1 complete.")
