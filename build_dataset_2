"""
build_dataset_2.py  -  holdings and transaction fact tables.

IMPORTANT ON PROVENANCE
-----------------------
Mubadala does not publish a line-by-line portfolio with valuations. This project
therefore separates three tiers of information and never blends them silently:

  Official         = stated by Mubadala or in a company filing
  Market data      = observable market/exchange data (price, multiples)
  Press reporting  = widely reported but not confirmed by Mubadala
  Analyst estimate = constructed by the author of this project

Any column ending _est is an author estimate and is flagged in evidence_grade.
"""
import os
import pandas as pd

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "warehouse")
AED_PER_USD = 3.6725

def w(name, rows, cols):
    df = pd.DataFrame(rows, columns=cols)
    df.to_csv(os.path.join(OUT, name + ".csv"), index=False)
    print(f"  {name:32s} {len(df):>4} rows")
    return df

# --------------------------------------------------------------------------
# FACT: notable holdings
# cols: id, holding, sector_id, geo_id, platform_id, ownership_desc, listed,
#       ticker, thesis, evidence_grade, source_id
# --------------------------------------------------------------------------
H = [
 (1,"GlobalFoundries Inc.",1,2,2,"Controlling shareholder (~80%) via Mubadala Technology Investment Company","Listed","NASDAQ:GFS",
    "Specialty semiconductor foundry. Essential-chip supply-chain sovereignty play with rising silicon-photonics and automotive content.","Press reporting","S07"),
 (2,"OMV Aktiengesellschaft",3,4,2,"24.9% strategic stake via Mubadala Petroleum & Petrochemicals Holding","Listed","VIE:OMV",
    "Integrated energy and chemicals. Cash-generative hydrocarbon base funding a chemicals/circular-economy transition.","Press reporting","S08"),
 (3,"Mubadala Capital",4,12,3,"Wholly owned alternative asset management subsidiary","Private","-",
    "c.US$30bn across balance-sheet and third-party vehicles in PE, Brazil, Venture Capital and Solutions. Fee-earning annuity on top of principal returns.","Official","S04"),
 (4,"Masdar (Abu Dhabi Future Energy Co.)",3,1,1,"Shareholder alongside TAQA and ADNOC","Private","-",
    "Global clean-energy champion; anchor of the UAE energy-transition cluster.","Press reporting","S06"),
 (5,"WHOOP Inc.",2,2,2,"Series G investor (minority)","Private","-",
    "AI-driven continuous-biometrics health platform. 2.5m+ members, US$1.1bn exit-2025 bookings run-rate, cash-flow positive in 2025.","Official","S05"),
 (6,"Fortress Investment Group",4,2,3,"Majority shareholder; strategic partnership","Private","-",
    "Credit and special-situations manager. 2025 partnership seeking to deploy c.US$1bn.","Official","S03"),
 (7,"Corient",4,2,3,"Held via Mubadala Capital","Private","-",
    "US wealth-management consolidator; multiple tack-on acquisitions completed in 2025.","Official","S03"),
 (8,"Nord Anglia Education",7,3,2,"Minority stake acquired 2025 (US$600m)","Private","-",
    "Premium international schools platform; structural demand growth in emerging-market middle class.","Official","S03"),
 (9,"Tabreed (National Central Cooling Co.)",5,1,1,"Strategic shareholder","Listed","DFM:TABREED",
    "District cooling utility; regulated-style cash flows, closed two largest-ever transactions in 2025 (AED3.87bn).","Official","S03"),
 (10,"CoolIT Systems",1,7,2,"Minority stake - agreed sale to Ecolab in KKR-led US$4.75bn transaction (2026)","Private","-",
    "Liquid cooling for AI data centres. Realisation demonstrating monetisation of the AI-infrastructure theme.","Official","S06"),
 (11,"CredibleX",4,1,1,"Lead investor, Series A (2026)","Private","-",
    "UAE embedded-finance platform accelerating SME lending. Direct fintech exposure.","Official","S06"),
 (12,"Power Factors",1,7,2,"Minority stake (2026)","Private","-",
    "Renewable-asset performance software; data layer for the energy transition.","Official","S06"),
 (13,"TBX Nexxia (JV with Tubacex)",6,1,1,"Joint venture launched in Abu Dhabi (2026)","Private","-",
    "End-to-end corrosion-resistant-alloy OCTG platform serving critical energy supply chains.","Official","S06"),
 (14,"Aldar / Mubadala JV - The Link, Masdar City",5,1,4,"50/50 joint venture","Private","-",
    "Prime Abu Dhabi commercial real estate anchored to the sustainability cluster.","Official","S06"),
 (15,"Hornsea 3 Offshore Wind Farm",3,3,4,"Consortium investor alongside Apollo funds (2026)","Private","-",
    "UK offshore wind; long-duration contracted renewable cash flows.","Official","S06"),
 (16,"Greenlink Interconnector",5,8,4,"Investment alongside Equitix (2026)","Private","-",
    "Ireland-UK electricity interconnector; regulated infrastructure.","Official","S06"),
 (17,"Embraer partnership",8,6,1,"Strategic agreement (2026)","Listed","NYSE:ERJ",
    "Aerospace industrial content and localisation for the UAE.","Official","S06"),
 (18,"Container leasing platforms (with Stonepeak)",10,2,4,"Partnership investment (2026)","Private","-",
    "Global-trade linked leasing assets with contracted yields.","Official","S06"),
 (19,"MGX",1,1,1,"AI-focused investment vehicle established with G42","Private","-",
    "Dedicated artificial-intelligence and advanced-technology capital vehicle; core to Abu Dhabi's AI ambition.","Press reporting","S06"),
 (20,"Barings Global Real Estate Debt Partnership",5,12,3,"US$500m partnership (2025)","Private","-",
    "Senior real-estate credit; floating-rate income with downside protection.","Official","S03"),
]
w("fact_holding", H, ["holding_id","holding_name","sector_id","geo_id","platform_id","ownership","listing_status","ticker","investment_thesis","evidence_grade","source_id"])

# --------------------------------------------------------------------------
# FACT: transactions 2025-2026
# --------------------------------------------------------------------------
def usd(aed_bn): return round(aed_bn/AED_PER_USD*1000,0)   # AED bn -> USD m

D = [
 # id, date, target, type, sector_id, geo_id, platform_id, value_usd_m, disclosed, grade, source
 (1,"2025-12-31","Corient tack-on acquisitions","Add-on",4,2,3,None,"Value not disclosed","Official","S03"),
 (2,"2025-12-31","ADIC indirect deployments","Fund deployment",12,12,3,usd(70),"AED70bn disclosed","Official","S03"),
 (3,"2025-12-31","Al Maryah Island transformation","Development",5,1,4,usd(60),"AED60bn+ disclosed","Official","S03"),
 (4,"2025-12-31","Tabreed - two largest ever transactions","Acquisition",5,1,1,usd(3.87),"AED3.87bn disclosed","Official","S03"),
 (5,"2025-12-31","Fortress strategic partnership","Partnership",4,2,3,1000.0,"Seeks to deploy US$1bn","Official","S03"),
 (6,"2025-12-31","Nord Anglia Education stake","Minority acquisition",7,3,2,600.0,"US$600m disclosed","Official","S03"),
 (7,"2025-12-31","Mubadala Capital Co-Investment Fund I close","Fund close",4,12,3,550.0,"US$550m+ disclosed","Official","S03"),
 (8,"2025-12-31","Barings Global Real Estate Debt Partnership","Credit partnership",5,12,3,500.0,"US$500m disclosed","Official","S03"),
 (9,"2026-03-31","WHOOP Series G","Growth equity",2,2,2,575.0,"Round size US$575m at US$10.1bn valuation","Official","S05"),
 (10,"2026-06-15","Mubadala x WHOOP UAE partnership","Partnership",2,1,1,None,"Value not disclosed","Official","S06"),
 (11,"2026-05-20","CredibleX Series A (lead investor)","Venture",4,1,1,None,"Value not disclosed","Official","S06"),
 (12,"2026-05-05","Power Factors minority stake","Minority acquisition",1,7,2,None,"Value not disclosed","Official","S06"),
 (13,"2026-04-20","Container leasing platforms with Stonepeak","Platform investment",10,2,4,None,"Value not disclosed","Official","S06"),
 (14,"2026-04-10","TBX Nexxia JV with Tubacex","Joint venture",6,1,1,None,"Value not disclosed","Official","S06"),
 (15,"2026-03-15","Aldar/Mubadala JV acquires The Link, Masdar City","Real estate acquisition",5,1,4,None,"Value not disclosed","Official","S06"),
 (16,"2026-02-25","CoolIT minority stake sale to Ecolab (KKR-led)","Exit",1,7,2,4750.0,"US$4.75bn total transaction value","Official","S06"),
 (17,"2026-07-20","Embraer aerospace agreement","Strategic agreement",8,6,1,None,"Value not disclosed","Official","S06"),
 (18,"2026-07-05","Greenlink investment with Equitix","Infrastructure",5,8,4,None,"Value not disclosed","Official","S06"),
 (19,"2026-06-30","Hornsea 3 offshore wind (Apollo-led consortium)","Infrastructure",3,3,4,None,"Value not disclosed","Official","S06"),
]
w("fact_transaction", D, ["deal_id","announce_date","target","deal_type","sector_id","geo_id","platform_id","value_usd_m","disclosure_note","evidence_grade","source_id"])

# --------------------------------------------------------------------------
# FACT: listed market data snapshot for case-study subjects + peers
# --------------------------------------------------------------------------
M = [
 # ticker, name, sector_id, ccy, price, mkt_cap_bn, ev_bn, revenue_bn, ebitda_bn, net_income_bn,
 # pe, ev_ebitda, ev_sales, fcf_bn, net_debt_bn, beta, asof, source
 ("GFS","GlobalFoundries Inc.",1,"USD",50.01,27.44,25.40,6.84,2.10,0.778,36.00,12.10,3.71,1.074,-2.05,1.76,"2026-08-03","S07"),
 ("UMC","United Microelectronics",1,"USD",18.69,45.65,43.07,7.88,2.96,2.62,17.40,14.53,5.47,1.92,-2.64,1.57,"2026-08-03","S09"),
 ("TSEM","Tower Semiconductor",1,"USD",234.32,26.42,25.08,1.71,0.276,0.290,92.65,90.77,14.67,0.301,-1.34,0.90,"2026-08-04","S09"),
 ("TSM","TSMC",1,"USD",415.53,1850.0,None,139.57,None,None,26.56,None,None,None,None,None,"2026-08-04","S09"),
 ("ON","ON Semiconductor",1,"USD",81.15,31.58,None,6.20,None,None,51.93,None,None,None,None,None,"2026-08-04","S09"),
 ("OMV","OMV Aktiengesellschaft",3,"EUR",54.60,17.62,24.16,23.38,5.40,2.36,16.74,4.20,1.03,0.794,2.79,0.21,"2026-06-30","S08"),
 ("SHEL","Shell plc",3,"USD",89.49,254.30,None,296.60,None,None,9.79,None,None,None,None,None,"2026-08-04","S09"),
 ("TTE","TotalEnergies SE",3,"USD",85.32,195.47,None,196.38,None,None,10.96,None,None,None,None,None,"2026-08-04","S09"),
 ("E","Eni S.p.A.",3,"USD",53.49,79.46,None,102.74,None,None,13.82,None,None,None,None,None,"2026-08-04","S09"),
 ("BP","BP p.l.c.",3,"USD",42.30,114.52,None,215.28,None,None,20.86,None,None,None,None,None,"2026-08-04","S09"),
 ("BX","Blackstone Inc.",4,"USD",136.27,169.49,None,15.48,None,None,30.51,None,None,None,None,None,"2026-08-04","S09"),
 ("APO","Apollo Global Management",4,"USD",130.19,75.06,None,35.60,None,None,81.92,None,None,None,None,None,"2026-08-04","S09"),
 ("ARES","Ares Management",4,"USD",141.16,46.56,None,5.99,None,None,62.43,None,None,None,None,None,"2026-08-04","S09"),
 ("OWL","Blue Owl Capital",4,"USD",11.42,17.80,None,2.99,None,None,95.88,None,None,None,None,None,"2026-08-04","S09"),
 ("TPG","TPG Inc.",4,"USD",48.76,18.74,None,3.73,None,None,139.03,None,None,None,None,None,"2026-08-04","S09"),
 ("TMO","Thermo Fisher Scientific",2,"USD",565.99,209.27,None,46.34,None,None,30.89,None,None,None,None,None,"2026-08-04","S09"),
 ("WST","West Pharmaceutical Services",2,"USD",345.71,24.33,None,3.33,None,None,44.31,None,None,None,None,None,"2026-08-04","S09"),
 ("CRL","Charles River Laboratories",2,"USD",235.00,11.32,None,4.03,None,None,None,None,None,None,None,None,"2026-08-04","S09"),
 ("ICLR","ICON plc",2,"USD",156.62,12.08,None,8.29,None,None,434.32,None,None,None,None,None,"2026-08-04","S09"),
 ("A","Agilent Technologies",2,"USD",138.78,39.20,None,7.23,None,None,28.06,None,None,None,None,None,"2026-08-04","S09"),
]
w("fact_market_data", M, ["ticker","company","sector_id","currency","price","mkt_cap_bn","ev_bn","revenue_ttm_bn",
                          "ebitda_ttm_bn","net_income_ttm_bn","pe_ttm","ev_ebitda","ev_sales","fcf_ttm_bn",
                          "net_debt_bn","beta_5y","as_of","source_id"])

# --------------------------------------------------------------------------
# FACT: GlobalFoundries historical fundamentals (source S07)
# --------------------------------------------------------------------------
G = [
 (2021,6585,1013,-60,-250,2839,1767,1072),
 (2022,8108,2239,1167,1448,2624,3059,-435),
 (2023,7392,2101,1129,1020,2125,1804,321),
 (2024,6750,1651,-214,-265,1722,625,1097),
 (2025,6791,1690,797,885,1731,722,1009),
]
w("fact_gfs_financials", [(y,r,g,o,n,ocf,cx,fcf,"S07") for y,r,g,o,n,ocf,cx,fcf in G],
  ["year","revenue_usd_m","gross_profit_usd_m","operating_income_usd_m","net_income_usd_m",
   "operating_cash_flow_usd_m","capex_usd_m","free_cash_flow_usd_m","source_id"])

# GFS revenue by end-market, FY2025
seg = [
 (2025,"Smart Mobile Devices",2678),(2025,"Communications Infrastructure & Datacenter",745),
 (2025,"Automotive",1410),(2025,"Home and Industrial IoT",1189),(2025,"Non-Wafer and Corporate Other",769),
 (2024,"Smart Mobile Devices",3048),(2024,"Communications Infrastructure & Datacenter",577),
 (2024,"Automotive",1206),(2024,"Home and Industrial IoT",1267),(2024,"Non-Wafer and Corporate Other",652),
 (2023,"Smart Mobile Devices",3023),(2023,"Communications Infrastructure & Datacenter",863),
 (2023,"Automotive",1046),(2023,"Home and Industrial IoT",1604),(2023,"Non-Wafer and Corporate Other",856),
]
w("fact_gfs_segment", [(y,s,v,"S07") for y,s,v in seg], ["year","end_market","revenue_usd_m","source_id"])

# --------------------------------------------------------------------------
# FACT: OMV historical fundamentals (source S08)
# --------------------------------------------------------------------------
O = [
 (2021,34897,5864,8275,2093,4520,2.30),
 (2022,60635,11494,13958,3634,4815,2.80),
 (2023,38538,4672,7057,1480,2222,2.95),
 (2024,25504,4791,6789,1389,1943,3.05),
 (2025,23623,3513,5433,1017,1366,3.15),
]
w("fact_omv_financials", [(y,r,e,eb,n,f,d,"S08") for y,r,e,eb,n,f,d in O],
  ["year","revenue_eur_m","ebit_eur_m","ebitda_eur_m","net_income_common_eur_m","free_cash_flow_eur_m","dps_eur","source_id"])

# --------------------------------------------------------------------------
# FACT: WHOOP disclosed operating metrics (source S05)
# --------------------------------------------------------------------------
WH = [
 ("Series G round size (USD m)",575.0,"Official","S05"),
 ("Post-money valuation (USD bn)",10.1,"Official","S05"),
 ("Members (m)",2.5,"Official - 'over 2.5 million'","S05"),
 ("2025 bookings growth YoY (%)",103.0,"Official","S05"),
 ("Exit-2025 bookings run-rate (USD bn)",1.1,"Official","S05"),
 ("Operating cash flow positive in 2025",1.0,"Official (boolean flag)","S05"),
 ("Physiological data collected (bn hours)",24.0,"Official","S05"),
 ("New roles being hired in 2026",600.0,"Official","S05"),
]
w("fact_whoop_metrics", WH, ["metric","value","evidence_grade","source_id"])

print("\nData layer part 2 complete.")
