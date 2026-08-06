# -*- coding: utf-8 -*-
"""Builds Project_Notes_Evidence_Log.pdf - the chronological record of the build."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pdf_style import *

HERE=os.path.dirname(os.path.abspath(__file__))
def entry(no, title, tag):
    col={"BUILD":TEAL,"DECISION":NAVY2,"PROBLEM":RUST,"CHECK":GOLD}[tag]
    return KeepTogether([Spacer(1,7), Table([[
      Paragraph(f'<font color="#FFFFFF" size="7"><b>{tag}</b></font>',
        S("tg", fontName="Helvetica-Bold", fontSize=7, alignment=TA_CENTER, textColor=colors.white)),
      Paragraph(f'<font color="#0B2545"><b>{no}  {title}</b></font>',
        S("et", fontName="Helvetica-Bold", fontSize=10.6, leading=13.4))]],
      colWidths=[19*mm, None], style=TableStyle([
        ("BACKGROUND",(0,0),(0,0),col),("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("LEFTPADDING",(1,0),(1,0),7),("TOPPADDING",(0,0),(-1,-1),4),
        ("BOTTOMPADDING",(0,0),(-1,-1),4),
        ("LINEBELOW",(1,0),(1,0),0.6,LINE)])), Spacer(1,4)])

def artefacts(rows):
    return table([["File produced","What it contains","Size / lines"]]+rows,[62*mm,None,24*mm])

doc=DocTemplate(os.path.join(HERE,"Project_Notes_Evidence_Log.pdf"),
    "Project Notes and Evidence Log","Project Notes & Evidence Log")
F=[]
F+= cover("Project Notes and Evidence Log",
    "A dated, step-by-step record of everything built, every decision taken, "
    "every problem hit and every fix applied",
    [("Author","bann"),
     ("Document","Project notes / evidence of progress"),
     ("Companion to","Equity Research Report and Beginner's Guide"),
     ("Entries","40 logged entries across 9 work sessions"),
     ("Files produced","99 files, 3.5 MB"),
     ("Purpose","To evidence that the work was done step by step,"),
     ("","and to make every artefact traceable to the decision"),
     ("","that produced it")],
    kicker="EVIDENCE LOG")

F.append(Paragraph("How to read this log", H1))
F.append(Paragraph(
 "Entries run in the order the work happened. Each carries one of four tags. Nothing has been tidied up after "
 "the fact: the failures are logged where they occurred, with the reasoning that led to each fix, because that "
 "sequence is the actual evidence of work.", LEAD))
F.append(table([
 ["Tag","Means"],
 ["BUILD","Something was created - a file, a table, a model, a chart."],
 ["DECISION","A choice was made between real alternatives, with a reason."],
 ["PROBLEM","Something broke or turned out wrong, and what was done about it."],
 ["CHECK","A verification step, and what it found."],
],[26*mm,None]))
F.append(Paragraph("Project structure produced", H2))
F.append(table([
 ["Folder","Contents","Files"],
 ["01_data/","Dataset builders, the star-schema warehouse, Power BI-ready exports","36"],
 ["02_sql/","Schema DDL, twelve analysis queries, the SQLite database, query results","17"],
 ["03_valuation_models/","Shared valuation engine, four case studies, live Excel workbook","11"],
 ["04_ai_ml/","Optimiser, Monte Carlo, text classifier, peer clustering, outputs","10"],
 ["05_dashboard/","Self-contained HTML dashboard and the 290-line Power BI build guide","3"],
 ["06_reports/","Three PDF documents and the shared styling module","8"],
 ["07_charts/","Fourteen publication-quality figures and the script that makes them","15"],
],[38*mm,None,16*mm]))

# =============================== SESSION 1
F.append(PageBreak())
F.append(Paragraph("Session 1  -  Scoping and source collection", H1))
F.append(entry("1.1","Reframed a three-line brief into five answerable questions","DECISION"))
F.append(Paragraph(
 "The brief named a topic - portfolio strategy, sector allocation, valuation case studies, dashboards. A topic has "
 "no end condition. Wrote five questions the finished project must answer: is the portfolio concentrated; is "
 "growth self-funded; is the asset mix efficient; how central is technology; are the assets fairly valued. Every "
 "subsequent build decision was tested against 'which question does this answer?'", BODY))

F.append(entry("1.2","Collected primary sources from Mubadala directly","BUILD"))
F.append(table([
 ["ID","Source","Published","What it gave"],
 ["S01","2025 annual results press release","9 Apr 2026","AUM, IRRs, deployments, proceeds"],
 ["S02","2025 Annual Review - Performance Overview","9 Apr 2026","Asset-class weights, flow history, credit ratings"],
 ["S03","2025 Annual Review - Key Investment Highlights","9 Apr 2026","Eight 2025 transactions with values"],
 ["S04","Corporate site - Our Structure","4 Aug 2026","Four platforms, CEOs, mandates, Mubadala Capital AUM"],
 ["S05","Press release - WHOOP Series G","31 Mar 2026","US$575m at US$10.1bn, members, growth, run-rate"],
 ["S06","Newsroom - 2026 announcements","4 Aug 2026","Eleven 2026 transactions"],
],[12*mm,58*mm,20*mm,None]))
F.append(Paragraph("Headline figures captured and frozen for reproducibility:", BODY))
F.append(table([
 ["Metric","Value"],
 ["Assets under management, FY2025","AED1,414bn / US$385bn (+17% YoY)"],
 ["Annualised return","10.7% over 5 years; 10.3% over 10 years"],
 ["Capital deployed / proceeds 2025","US$39bn (+20%) / US$38bn (+27%)"],
 ["Asset-class mix","Private 42%, Public 20%, RE&amp;I 17%, Alternatives 16%, Credit 5%"],
 ["Long-term credit ratings","Aa2 (Moody's) / AA (S&amp;P) / AA (Fitch), all stable"],
],[62*mm,None]))

F.append(entry("1.3","Annual Review geography chart returned all zeros","PROBLEM"))
F.append(Paragraph(
 "The geographic breakdown on the Performance Overview page is rendered client-side by JavaScript. Fetching the "
 "page returned the region labels but every percentage came back as 0%. A browser-rendering route was attempted; "
 "no browser extension was connected.", BODY))
F.append(callout("Resolution.",
 "Did not guess the figures and did not silently drop the analysis. Built an independent geographic picture from "
 "the twenty named holdings and labelled it throughout as the author's dataset rather than Mubadala's disclosure. "
 "The research report states this in Section 3.4 and again in the limitations.", "warn"))

F.append(entry("1.4","Market data could not be pulled programmatically","PROBLEM"))
F.append(Paragraph(
 "Installed yfinance to pull share prices; the sandbox network blocks Yahoo Finance endpoints (HTTP 403 on the "
 "CONNECT tunnel). Rather than attempt to route around the restriction, switched to fetching published pages from "
 "StockAnalysis.com, which republishes S&amp;P Global Market Intelligence data and renders server-side. Every market "
 "figure therefore carries its own as-of date, which is arguably better discipline than a live feed.", BODY))

F.append(entry("1.5","Chose four case-study subjects","DECISION"))
F.append(table([
 ["Sector","Subject","Why it earns its place","Rejected"],
 ["Technology","GlobalFoundries (NASDAQ: GFS)","Listed, full financials, Mubadala is controlling shareholder. "
  "Cyclical margins plus AI optionality makes it the ideal reverse-DCF subject.","G42, MGX - private, no financials"],
 ["Energy","OMV AG (VIE: OMV)","Listed, 24.9% Mubadala stake, and it contains three real analytical traps: "
  "implausible beta, large minorities, distorted EPS.","Masdar - private; Borouge - ADNOC-controlled"],
 ["Healthcare","WHOOP Inc.","A hard, dated, officially disclosed transaction price to reverse-engineer, plus "
  "genuine AI content.","PCI Pharma - no disclosed price to anchor on"],
 ["Financial services","Mubadala Capital","AUM is officially disclosed on Mubadala's own site, and it tests a "
  "different skill: valuing a fee annuity.","Fortress - no verifiable AUM in-session"],
],[24*mm,32*mm,None,32*mm]))

# =============================== SESSION 2
F.append(PageBreak())
F.append(Paragraph("Session 2  -  The data layer", H1))
F.append(entry("2.1","Chose a star schema over a single flat table","DECISION"))
F.append(Paragraph(
 "A flat table duplicates every text field on every row, allows 'USA' and 'United States' to coexist invisibly, "
 "and makes slicers ambiguous when two facts share a concept. Full third-normal form was rejected as overkill - "
 "queries would need too many joins to stay readable. The star schema is what Power BI's engine is designed for.", BODY))

F.append(entry("2.2","Added source_id and evidence_grade to every fact table","DECISION"))
F.append(Paragraph(
 "Four grades: Official, Market data, Press reporting, Analyst estimate. This makes provenance queryable rather "
 "than remembered, and it enforces honesty while building - it is much harder to let an estimate drift into being "
 "treated as a fact when the row itself says 'Analyst estimate'.", BODY))

F.append(entry("2.3","Built the warehouse","BUILD"))
F.append(artefacts([
 ["01_data/build_dataset.py","Dimensions plus headline performance, flows, allocation, ratings","~150 lines"],
 ["01_data/build_dataset_2.py","Holdings, transactions, market data, company financials","~200 lines"],
 ["warehouse/dim_*.csv","5 dimension tables","43 rows"],
 ["warehouse/fact_*.csv","11 fact tables","117 rows"],
]))
F.append(Paragraph(
 "Twenty named holdings (four listed), nineteen announced transactions, twenty listed companies of market data, "
 "five years each of GlobalFoundries and OMV financials, three years of GlobalFoundries segment data, and eight "
 "disclosed WHOOP metrics.", BODY))

F.append(entry("2.4","SQLite refused to create the database file","PROBLEM"))
F.append(Paragraph(
 "<font face='Courier'>sqlite3.OperationalError: disk I/O error</font> on executescript. Cause: the working "
 "directory is a network-style mount that does not support the POSIX file locking SQLite requires.", BODY))
F.append(callout("Resolution.",
 "Build the database on local disk and copy the finished file into the project folder. Three lines changed, with "
 "a comment left in load_and_run.py explaining why - otherwise the next reader would 'fix' it back and reintroduce "
 "the failure.", "find"))

F.append(entry("2.5","Built the schema and loaded it","BUILD"))
F.append(artefacts([
 ["02_sql/01_create_schema.sql","16 CREATE TABLE statements with CHECK constraints, foreign keys, 5 indexes","205 lines"],
 ["02_sql/load_and_run.py","Loader, integrity check, query runner","~55 lines"],
 ["02_sql/mubadala.db","The populated SQLite database","192 KB"],
]))

F.append(entry("2.6","Referential integrity verified","CHECK"))
F.append(Paragraph(
 "Ran <font face='Courier'>PRAGMA foreign_key_check</font>. <b>Zero violations.</b> Every sector, geography, "
 "platform, asset-class and source ID referenced in a fact table exists in its dimension. This is the check that "
 "proves the joins in the twelve analysis queries cannot silently drop rows.", BODY))

# =============================== SESSION 3
F.append(PageBreak())
F.append(Paragraph("Session 3  -  SQL analysis", H1))
F.append(entry("3.1","Wrote and ran twelve analysis queries","BUILD"))
F.append(artefacts([
 ["02_sql/03_analysis_queries.sql","12 documented queries","~200 lines"],
 ["02_sql/query_results/Q1-Q12.csv","Materialised output of every query","81 rows total"],
]))
F.append(Paragraph("Techniques deliberately covered: CTEs, window functions (SUM OVER, RANK, LAG, NTILE, "
 "PARTITION BY), conditional aggregation as a pivot substitute, self-joins, percent-of-total subqueries, "
 "CASE-based classification, UNION ALL auditing, and a Herfindahl index computed in SQL.", BODY))

F.append(entry("3.2","Four findings emerged directly from the queries","BUILD"))
F.append(table([
 ["Query","Finding","Why it matters"],
 ["Q8","Herfindahl index of the asset mix = <b>2,734</b>; effective number of buckets = <b>3.7</b>",
  "Formally 'concentrated'. A five-way reported split behaves like three and a half real positions."],
 ["Q3","Recycling ratio 1.13x (2023), 0.94x (2024), <b>0.97x (2025)</b>",
  "Growth is self-funded. Realisations paid for 97% of deployment in 2025."],
 ["Q11","OMV free-cash-flow dividend cover fell <b>6.0x to 1.3x in four years</b>",
  "The single most useful finding in the project. Dividend raised annually while the cash behind it shrank."],
 ["Q10","GlobalFoundries automotive revenue +34.8%, mix share +6.6pp since 2023",
  "The business is genuinely rotating toward higher-content silicon - but datacenter revenue fell 13.7%."],
],[14*mm,64*mm,None]))

# =============================== SESSION 4
F.append(PageBreak())
F.append(Paragraph("Session 4  -  Valuation models", H1))
F.append(entry("4.1","Built a shared valuation engine before any case study","DECISION"))
F.append(Paragraph(
 "Writing the WACC build-up, FCFF projection, discounting, equity bridge, sensitivity grid and comparables "
 "statistics once - rather than four times - means a fix propagates everywhere and the four cases are genuinely "
 "consistent with each other.", BODY))
F.append(artefacts([["03_valuation_models/valuation_engine.py",
 "WACCInputs, DCFAssumptions, project_fcff, discount, equity_bridge, sensitivity_grid, comps_stats","~170 lines"]]))

F.append(entry("4.2","GlobalFoundries DCF landed 30% below the market price","PROBLEM"))
F.append(Paragraph(
 "DCF value $35.07 against a traded $50.01. Reviewed the assumptions rather than the conclusion: terminal EBIT "
 "margin 20% against 12.1% trailing, capex below D&amp;A in later years, WACC of 12.55% cross-checked against a "
 "published vendor estimate of 13.25%. The assumptions were not obviously conservative, so the gap was real.", BODY))
F.append(callout("Resolution - and it became the best analysis in the project.",
 "Rather than declare the market wrong, inverted the model by bisection to solve for the steady-state EBIT margin "
 "that reproduces $50.01. Answer: <b>33.4%</b>, against 12.1% today - approximately what full delivery of "
 "management's published 45% gross-margin target for 2030 would produce. The conclusion changed from an opinion "
 "into a testable statement: at this price you are underwriting execution, not valuation.", "find"))

F.append(entry("4.3","First comparables run produced $205 a share","PROBLEM"))
F.append(Paragraph(
 "The outlier screen in comps_stats only activates above three peers, so with two EV/EBITDA peers the median "
 "landed at 52.6x - dragged there by Tower Semiconductor at 90.8x after a +425% twelve-month re-rating. Applied "
 "to GlobalFoundries' EBITDA this gave $205 a share against a $50 market price.", BODY))
F.append(callout("Resolution.",
 "Rebuilt the comparables around an explicit applied range of 11.0x / 14.5x / 17.0x anchored on UMC, the closest "
 "pure-play mature-node foundry, with Tower reported in the peer table but formally excluded and <b>the exclusion "
 "stated in the output JSON, the report and the dashboard</b>. An unstated outlier exclusion is the most common "
 "way comparables analysis is quietly rigged.", "warn"))

F.append(entry("4.4","OMV: three judgement calls, each disclosed","DECISION"))
F.append(table([
 ["Issue","What a mechanical model would do","What was done instead"],
 ["Raw 5-year beta of 0.21","Use it, producing a cost of equity near 4% for an integrated oil producer",
  "Substituted a European integrated-energy sector beta of 0.90 and disclosed the swap. Cause of the low raw "
  "beta: 141m free float out of 326m shares plus a domestic index listing."],
 ["EV EUR24.2bn vs market cap EUR17.6bn and net debt EUR2.8bn","Ignore the EUR3.75bn residual",
  "Identified it as minority interest from full consolidation of Borealis/Borouge and deducted it in the equity "
  "bridge. Omitting it would have overstated value per share by roughly 25%."],
 ["Reported TTM EPS of EUR7.20","Apply a P/E multiple to it",
  "Rejected: it includes EUR1,303m from discontinued operations. FY2025's EUR3.11 also rejected (EUR497m of "
  "write-downs). Used a three-year average of EUR3.96."],
],[36*mm,48*mm,None]))
F.append(Paragraph(
 "Result: DCF EUR56.42 against a market price of EUR54.60 (+3.3%); normalised P/E comparables EUR38.77 to "
 "EUR61.70 with a median of EUR49.06. The dividend-cover collapse, not the valuation, is the finding.", BODY))

F.append(entry("4.5","WHOOP: chose reverse DCF over a forward forecast","DECISION"))
F.append(Paragraph(
 "WHOOP publishes no accounts. A ten-year forward forecast would have been assumptions laundered through "
 "arithmetic. Inverted instead, holding an 18% required return, 3.5% terminal growth, a ten-year horizon and FCF "
 "margins ramping 4% to 20%, and solved for the growth rate implied by the price actually paid.", BODY))
F.append(callout("Result.",
 "The US$10.1bn post-money requires revenue to compound at <b>34.8% a year for a decade</b>, reaching about "
 "US$21.8bn by 2035. Entry multiple 9.2x post-money revenue (8.7x pre-money), a 1.9x premium to the median "
 "listed healthcare platform.", "find"))

F.append(entry("4.6","Units error caught in the WHOOP model","PROBLEM"))
F.append(Paragraph(
 "Revenue per member was first computed as $440,000 a year. Revenue was already in US$ millions and members in "
 "millions, so the additional multiplication by 1,000 was wrong. The correct figure is <b>$440 per member per "
 "year</b> - plausible for a subscription plus hardware, and a useful sanity check on the disclosed run-rate. A "
 "bull scenario was also producing the same value as the base case by coincidence; re-parameterised from 28% to "
 "42% growth so the scenario table spans a meaningful range.", BODY))

F.append(entry("4.7","Mubadala Capital: framework, not a valuation","DECISION"))
F.append(Paragraph(
 "Only one hard input exists - c.US$30bn of AUM, stated on Mubadala's own site. Every other input (60% "
 "third-party share, 1.20% fee rate, 35% FRE margin, 25% private-company discount) is an author assumption, "
 "labelled as such in the JSON, the Excel sheet, the report and the dashboard. Apollo was excluded from the peer "
 "range because its reported revenue consolidates Athene's insurance premiums, putting it on 2.1x sales against a "
 "cohort clustered between 5x and 11x.", BODY))

# =============================== SESSION 5
F.append(PageBreak())
F.append(Paragraph("Session 5  -  The Excel workbook", H1))
F.append(entry("5.1","Rebuilt every model in Excel with live formulas","BUILD"))
F.append(artefacts([
 ["03_valuation_models/build_excel_model.py","Generator using openpyxl","~330 lines"],
 ["03_valuation_models/Valuation_Models.xlsx","7 sheets: Cover, GFS_DCF, OMV_DCF, OMV_Dividend_Test, "
  "WHOOP_Reverse_DCF, Mubadala_Capital, Source_Register","20 KB"],
]))
F.append(Paragraph(
 "Formulas are real, not pasted values - changing the WACC cell moves the value per share. Banking colour "
 "convention throughout: blue for inputs, black for on-sheet formulas, green for cross-sheet links.", BODY))

F.append(entry("5.2","Forced a recalculation and compared every output to Python","CHECK"))
F.append(table([
 ["Output","Python","Excel","Verdict"],
 ["GFS value per share","$35.07","$35.05","Rounding in WACC. Accepted."],
 ["GFS enterprise value","$17,203m","$17,194m","0.05%. Accepted."],
 ["OMV value per share","EUR56.42","EUR56.48","Rounding. Accepted."],
 ["OMV implied minorities","EUR3,750m","EUR3,750m","Exact."],
 ["WHOOP implied value","US$9,510m","US$9,510m","Within 0.2% of the price paid. Solver converged."],
 ["Mubadala Capital central","US$1.73bn","US$1.42bn","<b>Not rounding. A real difference.</b>"],
],[46*mm,26*mm,26*mm,None]))
F.append(callout("Investigated and fixed.",
 "The Python version was taking a median across five values, one of which used the cohort <i>median</i> P/E of "
 "81.9x - a multiple inflated by performance-fee timing in the listed cohort. The Excel version used four values "
 "and excluded it. Excel was right. Changed the Python to match, kept the 81.9x figure in the output as "
 "'reported, not applied', and documented the reasoning.<br/><br/>"
 "<b>Building the same model twice in two tools is the cheapest error-detector available.</b> Had this been built "
 "once, the inconsistency would have shipped invisibly.", "warn"))

# =============================== SESSION 6
F.append(PageBreak())
F.append(Paragraph("Session 6  -  Quantitative and machine-learning layer", H1))
F.append(entry("6.1","Mean-variance optimisation of the disclosed asset mix","BUILD"))
F.append(artefacts([["04_ai_ml/01_portfolio_optimiser.py",
 "Efficient frontier, max-Sharpe, min-variance, efficiency test, reverse optimisation","~130 lines"]]))
F.append(Paragraph(
 "Actual mix: 9.45% expected return, 12.49% volatility, Sharpe 0.416. An efficient portfolio at the same return "
 "would carry 11.46% volatility, so the published allocation holds <b>1.02 percentage points of avoidable "
 "risk</b>. The max-Sharpe portfolio holds zero public equity and 26% credit against an actual 20% and 5%.", BODY))
F.append(callout("Interpretation logged at the time, and it matters.",
 "The optimiser has no concept of liquidity. The correct conclusion is not 'the mix is inefficient' but 'the "
 "liquidity insurance costs about one percentage point of volatility'. Reverse optimisation was added to make the "
 "same point constructively: the implied return beliefs are private 11.0%, public 10.0%, alternatives 8.4%, real "
 "assets 7.2%, credit 5.5%.", "find"))

F.append(entry("6.2","Monte Carlo simulation of AUM to 2035","BUILD"))
F.append(Paragraph(
 "50,000 paths, geometric Brownian motion with Student-t innovations (5 degrees of freedom, variance-rescaled) so "
 "that tails are fat in the way real markets are. Median 2035 AUM US$1,058bn; 55.8% probability of exceeding "
 "US$1 trillion; 12.9% probability of a peak-to-trough drawdown worse than 20% along the way.", BODY))

F.append(entry("6.3","Text classifier: first attempt scored 6% accuracy","PROBLEM"))
F.append(Paragraph(
 "A hand-written corpus of 48 example sentences produced 6.2% cross-validated accuracy across six classes - worse "
 "than random. Diagnosis: every example used almost entirely unique vocabulary, so a bag-of-words model had no "
 "shared terms to generalise from. It had memorised, not learned.", BODY))
F.append(callout("Resolution.",
 "Built vocabulary pools from real Mubadala announcement language and generated 1,080 examples (180 per class), "
 "and switched to a union of word (1-2 gram) and character (3-5 gram) TF-IDF features. Synthetic cross-validated "
 "accuracy reached 100%, which is meaningless on its own - so the reported number is the <b>hold-out score of 92% "
 "on twelve real, unseen Mubadala headlines</b>. Both figures, and the reason the synthetic corpus exists, are "
 "stated in the model output and in the report.", "find"))

F.append(entry("6.4","The classifier's single failure was retained as a finding","DECISION"))
F.append(Paragraph(
 "'Mubadala agrees to sell minority stake in CoolIT data centre liquid cooling to Ecolab' was predicted as "
 "Industrials rather than Technology, at 0.45 confidence. The prediction is defensible - CoolIT makes physical "
 "cooling hardware for AI data centres and is genuinely both. Logged as evidence that a single-label taxonomy is "
 "the wrong data model for a portfolio whose most interesting assets sit between sectors. The fix is multi-label "
 "tagging, a data-design decision rather than a modelling one.", BODY))

F.append(entry("6.5","Peer clustering as a check on comparables selection","BUILD"))
F.append(Paragraph(
 "Standardised size and valuation features, PCA to two components (88% of variance), k-means with k chosen by "
 "silhouette score (k=2, silhouette 0.401). GlobalFoundries' nearest neighbours in that space are ON "
 "Semiconductor and Agilent - not TSMC or UMC. The market treats it as a mid-cap specialty manufacturer, which is "
 "a useful corrective to a peer set assembled from the word 'foundry'.", BODY))

# =============================== SESSION 7
F.append(PageBreak())
F.append(Paragraph("Session 7  -  Visualisation and dashboards", H1))
F.append(entry("7.1","Produced fourteen figures","BUILD"))
F.append(artefacts([
 ["07_charts/make_charts.py","Matplotlib generator with a consistent house palette","~230 lines"],
 ["07_charts/01-14 *.png","Allocation, flows, sectors, geography, frontier, Monte Carlo, two football fields, "
  "mix shift, dividend cover, WHOOP scenarios, Mubadala Capital, clusters, confusion matrix","14 files"]]))

F.append(entry("7.2","Power BI Desktop is Windows-only; the project was built on a Mac","PROBLEM"))
F.append(Paragraph(
 "Four options were considered: a Windows VM (needs a licence, painful on Apple Silicon), Power BI in the browser "
 "via a Fabric trial (missing modelling features, usually rejects personal email domains), Tableau Public "
 "(Mac-native and respected, but does not literally satisfy a brief that says Power BI), or building the model "
 "and measures for Power BI while shipping a browser dashboard.", BODY))
F.append(callout("Resolution.",
 "Took the fourth route and made the substitution explicit rather than hiding it. Built the star schema, wrote 25 "
 "DAX measures and the full relationship map, exported 17 Power BI-ready CSVs including a date dimension, and "
 "wrote a 290-line build guide that reproduces the identical report on any Windows machine in under an hour. "
 "Shipped a self-contained HTML dashboard as the Mac-native twin.", "find"))

F.append(entry("7.3","Built the dashboard with no external dependencies","BUILD"))
F.append(artefacts([
 ["05_dashboard/build_dashboard.py","Generator that embeds the whole dataset as JSON","~450 lines"],
 ["05_dashboard/Mubadala_Portfolio_Dashboard.html","Six tabs, live filters, sortable tables, hand-written SVG charts","128 KB"],
 ["05_dashboard/PowerBI_Build_Guide.md","Relationships, 25 DAX measures, page specs, troubleshooting table","290 lines"],
 ["01_data/powerbi_exports/*.csv","17 Power BI-ready tables including a generated date dimension","17 files"],
]))
F.append(Paragraph(
 "Every chart is inline SVG drawn by hand-written JavaScript - donut, grouped bars, horizontal bars, fan chart, "
 "football field and frontier scatter. No CDN and no libraries, so the file opens correctly with no internet "
 "connection, which matters if someone opens it on a train.", BODY))

F.append(entry("7.4","Dashboard JavaScript validated before shipping","CHECK"))
F.append(Paragraph(
 "Extracted the script block, ran <font face='Courier'>node --check</font> for syntax, then executed it against a "
 "stub DOM to confirm it runs to completion without throwing. Both passed.", BODY))

F.append(entry("7.5","Miscount found in the dashboard commentary","PROBLEM"))
F.append(Paragraph(
 "A written callout claimed 'thirteen of nineteen tracked announcements carry no disclosed value'. Re-counted "
 "against the database: the true figure is <b>ten</b> without a value and nine with, totalling US$44.4bn. "
 "Corrected in the dashboard and stated correctly in the report. Logged because it is exactly the kind of "
 "hand-written number that goes stale when the underlying data changes.", BODY))

# =============================== SESSION 8-9
F.append(PageBreak())
F.append(Paragraph("Sessions 8 and 9  -  Writing and verification", H1))
F.append(entry("8.1","Produced three documents for three different readers","BUILD"))
F.append(artefacts([
 ["06_reports/pdf_style.py","Shared ReportLab template: cover, running heads, tables, callouts, figures, KPI strips","~190 lines"],
 ["06_reports/Equity_Research_Report.pdf","20 pages, 10 sections, 13 figures, full source register","960 KB"],
 ["06_reports/Beginner_Guide_Booklet.pdf","25 pages, 10 steps, jargon boxes, pros-and-cons tables","416 KB"],
 ["06_reports/Project_Notes_Evidence_Log.pdf","This document","-"],
]))

F.append(entry("8.2","Included a prominent limitations section","DECISION"))
F.append(Paragraph(
 "Section 10.3 of the research report states plainly that the holdings dataset is a curated sample rather than the "
 "whole portfolio; that deal totals are floors not totals; that the capital-market assumptions behind the "
 "optimiser and simulation are the author's; that all forward assumptions are estimates; and that two of the four "
 "case studies value private companies and are frameworks rather than valuations. Every experienced reader looks "
 "for these caveats - finding them already written is a stronger signal than omitting them.", BODY))

F.append(entry("9.1","Verification pass","CHECK"))
F.append(table([
 ["Check performed","Result"],
 ["PRAGMA foreign_key_check on the database","0 violations"],
 ["Excel recalculated via LibreOffice and compared to Python","1 real difference found and fixed (entry 5.2)"],
 ["Classifier evaluated on unseen real headlines","92% - the honest number, reported instead of the synthetic 100%"],
 ["Deal counts re-derived from the database","Miscount found and fixed (entry 7.5)"],
 ["WACC cross-checked against an independent published estimate","12.55% vs a vendor's 13.25% - close, and the difference is disclosed"],
 ["Derived figures sense-checked against reality","WHOOP revenue per member: $440,000 corrected to $440 (entry 4.6)"],
 ["All 14 charts and every PDF page rendered and inspected","Two layout defects found and fixed: overlapping football-field labels, and a cover divider cutting through metadata"],
 ["Dashboard JavaScript syntax and execution","Passed both"],
 ["Every reported figure traced to a source ID","Complete - 10 sources registered with URLs and as-of dates"],
],[74*mm,None]))
F.append(callout("Why the boring checks matter.",
 "Every error found in this pass was invisible in the output. A valuation of US$1.73bn looked exactly as "
 "convincing as the correct US$1.42bn. $440,000 per member looked like a number until someone thought about it "
 "for two seconds. Nothing about a wrong answer announces itself, which is why the checking has to be systematic "
 "rather than instinctive.", "warn"))

F.append(entry("9.2","Known limitations carried forward, not hidden","DECISION"))
F+= bullets([
 "The twenty tracked holdings are a curated sample. Mubadala publishes no position-level portfolio.",
 "Geographic percentages describe that sample, not the group's true economic exposure.",
 "Ten of nineteen transactions have no disclosed value, so US$44.4bn is a floor.",
 "Capital-market assumptions behind the optimiser and simulation are the author's, not Mubadala's.",
 "The classifier's training corpus is synthetic; only the hold-out score is a meaningful measure of skill.",
 "No currency layer: OMV is a euro asset, GlobalFoundries a dollar asset, and reporting is in dirhams. The FX "
 "translation effect on reported AUM is not modelled.",
])

F.append(Spacer(1,10))
F.append(Paragraph("Final inventory", H1))
F.append(table([
 ["Category","Count","Detail"],
 ["Total files produced","99","3.5 MB across seven folders"],
 ["Python modules","14","Data builders, valuation engine, four case studies, four quant/ML scripts, chart and document generators"],
 ["SQL","2 files","205-line schema, 12 documented analysis queries"],
 ["Data tables","16","5 dimensions, 11 facts; 160 rows, every one source-tagged"],
 ["Power BI exports","17 CSVs","Including a generated date dimension for time intelligence"],
 ["DAX measures written","25","Scale, flow, composition, concentration, deal flow, evidence quality, valuation"],
 ["Charts","14","Publication-quality, consistent palette"],
 ["Valuation case studies","4","Two listed with full DCFs, two private with disclosed-assumption frameworks"],
 ["Interactive deliverables","2","Self-contained HTML dashboard; live-formula Excel workbook"],
 ["Written documents","3 PDFs","Research report, beginner's guide, this log"],
 ["Sources registered","10","Each with URL, as-of date and evidence class"],
],[40*mm,18*mm,None]))
F.append(Spacer(1,8))
F.append(Paragraph(
 "<i>End of log. Companion documents: Equity_Research_Report.pdf and Beginner_Guide_Booklet.pdf.</i>", SMALL))

doc.build(F)
print("Built Project_Notes_Evidence_Log.pdf")
