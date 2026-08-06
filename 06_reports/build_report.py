# -*- coding: utf-8 -*-
"""Builds Equity_Research_Report.pdf - the main 10-15 page research document."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pdf_style import *
import pandas as pd

HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(HERE)
CH=os.path.join(ROOT,"07_charts"); VAL=os.path.join(ROOT,"03_valuation_models","outputs")
AI=os.path.join(ROOT,"04_ai_ml","outputs"); QR=os.path.join(ROOT,"02_sql","query_results")
J=lambda p: json.load(open(p)); C=lambda n: os.path.join(CH,n+".png")

g=J(os.path.join(VAL,"case_01_globalfoundries.json"))
o=J(os.path.join(VAL,"case_02_omv.json"))
wh=J(os.path.join(VAL,"case_03_whoop.json"))
mc=J(os.path.join(VAL,"case_04_mubadala_capital.json"))
po=J(os.path.join(AI,"portfolio_optimisation.json"))
sim=J(os.path.join(AI,"monte_carlo.json"))
clf=J(os.path.join(AI,"deal_classifier.json"))
pc=J(os.path.join(AI,"peer_clustering.json"))

doc=DocTemplate(os.path.join(HERE,"Equity_Research_Report.pdf"),
    "Mubadala Portfolio Strategy - Equity Research Report","Equity Research Report")
F=[]

# ============================================================ COVER
F+= cover("Mubadala Investment Company",
    "Portfolio strategy, sector allocation and valuation case studies across "
    "technology, healthcare, energy and financial services",
    [("Author","bann"),
     ("Document","Equity research report"),
     ("Date","August 2026"),
     ("Subject","Mubadala Investment Company (Abu Dhabi sovereign investor)"),
     ("Data as at","FY2025 results; market data 3-4 August 2026"),
     ("Case studies","GlobalFoundries | WHOOP | OMV AG | Mubadala Capital"),
     ("Methods","FCFF DCF, reverse DCF, trading comparables, mean-variance"),
     ("","optimisation, Monte Carlo simulation, machine-learning classification"),
     ("Deliverables","SQL warehouse, live Excel models, interactive dashboard")],
    kicker="EQUITY RESEARCH  |  SOVEREIGN WEALTH")

# ============================================================ 1 EXEC SUMMARY
F.append(Paragraph("1.  Executive summary", H1))
F.append(Paragraph(
 "Mubadala Investment Company ended 2025 with assets under management of AED1.414 trillion "
 "(US$385 billion), up 17% on the year, having compounded at 10.7% a year over five years and "
 "10.3% over ten. It deployed US$39 billion and realised US$38 billion. Those four numbers "
 "describe a balance sheet that grew without needing new shareholder capital.", LEAD))
F.append(kpi_strip([
 ("Assets under management","US$385bn","+17% year on year"),
 ("5-year annualised IRR","10.7%","10-year: 10.3%"),
 ("Capital deployed 2025","US$39bn","+20% year on year"),
 ("Proceeds 2025","US$38bn","+27% year on year")]))
F.append(Paragraph("This report asks five questions and answers each with evidence built from scratch.", H2))
F+= numbered([
 "<b>Is the portfolio concentrated?</b> Yes, and deliberately. The Herfindahl-Hirschman index of "
 "the disclosed asset-class mix is 2,734, which is formally 'concentrated'. The effective number of "
 "independent buckets is 3.7, not the five that the reported breakdown implies. Fifty-eight per cent "
 "of assets sit in private and alternative strategies, which is the illiquidity premium a sovereign "
 "investor with no redemption risk is uniquely able to harvest.",
 "<b>Is growth self-funded?</b> Yes. Proceeds covered 97 cents of every dollar deployed in 2025 and "
 "have averaged a recycling ratio of 1.01 over three years. Growth in the book came from performance "
 "and from realisations, not from a capital call on the shareholder.",
 "<b>Is the asset mix efficient?</b> Not in a narrow mean-variance sense, and that is informative "
 f"rather than damning. The published mix carries roughly {po['efficiency_test']['excess_volatility_carried_pp']}"
 " percentage points more volatility than an efficient portfolio at the same expected return. Almost all of "
 "the gap is the 20% public-equity sleeve, which a pure return optimiser would not hold at all. That sleeve "
 "is the price of liquidity, and quantifying that price is the useful output.",
 "<b>What is technology worth to the strategy?</b> Semiconductors, AI infrastructure and AI-enabled "
 "healthcare recur across every one of the four investment platforms, not just inside a technology bucket. "
 f"GlobalFoundries alone represents an enterprise value of US${g['market']['enterprise_value_usd_m']/1000:.1f} billion; "
 "the CoolIT realisation into a US$4.75 billion transaction shows the AI-infrastructure theme being monetised, "
 "not just accumulated.",
 "<b>Are the individual assets fairly valued?</b> Mixed, and the differences are instructive. Our base-case "
 f"discounted-cash-flow valuation of GlobalFoundries is ${g['dcf_value_per_share']:.2f} a share against a market price of "
 f"${g['market']['price']:.2f}; inverting the model shows the market requires a steady-state operating margin of "
 f"{g['reverse_dcf']['implied_terminal_ebit_margin']*100:.1f}% against {g['reverse_dcf']['ttm_ebit_margin']*100:.1f}% today. "
 f"OMV screens close to fair value at EUR{o['dcf_value_per_share']:.2f} against EUR{o['market']['price_eur']:.2f}, but "
 "free-cash-flow cover of its dividend has collapsed from 6.0 times to 1.3 times in four years. WHOOP's "
 f"US$10.1 billion Series G requires revenue to compound at {wh['reverse_dcf']['implied_revenue_cagr']*100:.1f}% a year for a decade.",
])
F.append(callout("The single most useful finding.",
 "Across three of the four case studies the interesting question was not <i>what is it worth</i> but "
 "<i>what does the price already assume</i>. Inverting a valuation model turns an argument about opinions "
 "into a statement that can be tested against evidence. That is the analytical habit this project is built around.",
 "find"))

F.append(PageBreak())
# ============================================================ 2 THE INSTITUTION
F.append(Paragraph("2.  The institution and its mandate", H1))
F.append(Paragraph(
 "Mubadala is Abu Dhabi's sovereign investor. Its mandate, in the company's own words, is to deliver "
 "sustainable, risk-adjusted returns for its shareholder - the Government of Abu Dhabi - while supporting "
 "the diversification of the domestic economy away from hydrocarbons. Those two objectives are not always "
 "aligned, and much of what looks unusual about the portfolio is the visible seam between them.", BODY))
F.append(Paragraph("2.1  Four platforms, one balance sheet", H2))
F.append(Paragraph(
 "The business is organised around four global investment platforms. Understanding them matters because "
 "the same sector appears in more than one, with a different objective each time.", BODY))
F.append(table([
 ["Platform","Chief executive","What it is actually for"],
 ["UAE Investments","Dr Bakheet Al Katheeri",
  "The national mandate. Builds homegrown champions and industrial clusters in energy, metals, aerospace, "
  "technology, healthcare, real estate and infrastructure. Success here is measured partly in GDP contribution, "
  "not only in IRR."],
 ["Private Equity","Camilla Languille and Luca Molinari",
  "Global direct buyouts and late-stage growth equity, principally North America and Europe with growing Asia "
  "exposure. This is where the return-seeking capital lives."],
 ["Credit and Special Situations","Hani Ahmad Barhoush",
  "Private debt, GP stakes, secondaries and opportunistic capital-structure solutions. Also home to Mubadala "
  "Capital, the asset-management subsidiary running about US$30bn across balance-sheet and third-party vehicles."],
 ["Real Assets","Khaled Al Shamlan Al Marri",
  "Real estate and infrastructure chosen for steady, visible cash flow across cycles. The ballast."],
],[30*mm,32*mm,None]))
F.append(Paragraph("2.2  What the credit rating tells you", H2))
F.append(Paragraph(
 "Mubadala's issuing entity carries long-term ratings of Aa2 from Moody's and AA from both S&amp;P Global and "
 "Fitch, all with stable outlooks. Those ratings explicitly reflect the support of the sole shareholder rather "
 "than the standalone credit of the portfolio. The practical consequence is a cost of debt far below what an "
 "equivalently levered private fund would pay, which is a structural competitive advantage when bidding for "
 "long-duration assets. It is also why the balance sheet can afford to be illiquid.", BODY))
F.append(callout("Why this section exists.",
 "A valuation is only as good as the understanding of the business behind it. Half the analytical mistakes "
 "in this project's first draft came from treating Mubadala as if it were a return-maximising fund. It is not. "
 "It is a return-maximising fund with a second mandate bolted on, and the second mandate explains most of the "
 "apparent inefficiencies.", "note"))

F.append(PageBreak())
# ============================================================ 3 PORTFOLIO
F.append(Paragraph("3.  Portfolio composition and sector allocation", H1))
F.append(Paragraph("3.1  Asset-class mix", H2))
F.append(Paragraph(
 "Mubadala disclosed the following split for FY2025: private assets 42%, public markets 20%, real estate and "
 "infrastructure 17%, alternatives 16% and credit 5%. Applied to US$385 billion of AUM, that implies roughly "
 "US$162 billion in private assets and US$77 billion in listed equities.", BODY))
F.append(figure(C("01_asset_allocation"),
 "Figure 1: Portfolio by asset class, FY2025. Source: Mubadala 2025 Annual Review.", 128))
F.append(Paragraph(
 "The headline observation is illiquidity. Private assets plus alternatives account for 58% of the book. For "
 "a pension fund with monthly redemptions that would be reckless; for a sovereign investor with a permanent "
 "capital base and no liabilities to match, it is the whole point. Illiquidity is the one risk premium that "
 "cannot be arbitraged away by anyone who might need their money back.", BODY))
F.append(Paragraph("3.2  How concentrated is it, really?", H2))
F.append(Paragraph(
 "A five-way split looks diversified. Measuring it says otherwise. The Herfindahl-Hirschman index - the sum of "
 "squared percentage weights, the same statistic competition regulators use to assess market concentration - "
 "comes out at 2,734. Anything above 2,500 is classified as concentrated. Inverting the index gives an "
 "'effective number' of 3.7 independent buckets rather than five.", BODY))
F.append(callout("How to read the HHI.",
 "If capital were spread perfectly evenly across five buckets, each would be 20%, the index would be "
 "5 x 20 squared = 2,000, and the effective number would be exactly 5. The higher the index climbs above "
 "that, the more the portfolio behaves like a smaller number of larger bets. At 2,734 Mubadala is running "
 "roughly three and a half real positions, dominated by the private book.", "note"))
F.append(Paragraph("3.3  Sector footprint", H2))
F.append(Paragraph(
 "Mubadala does not publish a position-level portfolio. To analyse sector allocation we assembled a dataset of "
 "twenty named holdings from the company's own disclosures, four of them listed, and tagged each to a sector, "
 "a country and a platform. Every row carries an evidence grade so that a reader can see which facts are "
 "company-stated and which are drawn from press reporting. Sixteen of the twenty are officially confirmed.", BODY))
F.append(figure(C("03_sector_composition"),
 "Figure 2: Tracked holdings by sector, shaded by AI exposure. Source: author's dataset built from Mubadala disclosures.", 150))
F.append(Paragraph(
 "Technology, financial services, and real estate and infrastructure each account for four of the twenty tracked "
 "positions. But counting positions understates technology's importance. Semiconductors sit inside the UAE "
 "Investments mandate through GlobalFoundries' Western fab footprint; AI infrastructure runs through MGX and the "
 "CoolIT realisation; AI-enabled healthcare arrives through WHOOP; and renewable-asset software arrives through "
 "Power Factors, which we have classified as technology but could equally be called energy. The theme is a "
 "spine running through the portfolio rather than a slice of it.", BODY))
F.append(Paragraph("3.4  Geographic allocation", H2))
F.append(figure(C("04_geography"),
 "Figure 3: Geographic footprint of tracked holdings. Source: author's dataset.", 140))
F.append(Paragraph(
 "Seventy per cent of tracked holdings sit outside the home market, with North America the largest single "
 "region at 35%. This is the two-mandate structure made visible: domestic capital is deployed to build "
 "national capability, international capital is deployed to earn a return, and the international book is "
 "the larger of the two. Mubadala describes itself as active in more than fifty countries.", BODY))

F.append(PageBreak())
# ============================================================ 4 CAPITAL
F.append(Paragraph("4.  Capital deployment and investment trends", H1))
F.append(figure(C("02_capital_flows"),
 "Figure 4: Capital deployed versus proceeds, 2023-2025. Source: Mubadala 2025 Annual Review.", 150))
F.append(Paragraph(
 "Deployment rose from US$24 billion in 2023 to US$39 billion in 2025, a 63% increase in two years. Proceeds "
 "rose from US$27 billion to US$38 billion over the same period. Dividing one by the other gives a recycling "
 "ratio: 1.13 in 2023, 0.94 in 2024 and 0.97 in 2025.", BODY))
F.append(table([
 ["Year","Deployed (US$bn)","Proceeds (US$bn)","Net (US$bn)","Recycling ratio"],
 ["2023","24.0","27.0","(3.0)","1.13x"],
 ["2024","32.0","30.0","2.0","0.94x"],
 ["2025","39.0","38.0","1.0","0.97x"],
],[22*mm,34*mm,34*mm,30*mm,None],align={1:"RIGHT",2:"RIGHT",3:"RIGHT",4:"RIGHT"}))
F.append(Paragraph(
 "A ratio near 1.0 sustained across three years is the signature of a mature investment platform rather than "
 "a growing one. Mubadala is not scaling by adding capital; it is scaling by turning the portfolio over faster "
 "at a higher level of activity. That matters for the risk assessment: an institution that must sell to buy is "
 "exposed to exit markets closing, which is precisely what a 20% liquid sleeve and a fee-earning subsidiary "
 "are there to insulate against.", BODY))
F.append(Paragraph("4.1  What the deal log actually shows", H2))
F.append(Paragraph(
 "We logged nineteen announced transactions across 2025 and 2026 from Mubadala's own newsroom and annual "
 "review. Nine carry a disclosed value totalling US$44.4 billion. Ten disclose no value at all.", BODY))
F.append(callout("A discipline worth naming.",
 "Because more than half the transactions have no published value, any 'total deal value' figure built from "
 "public sources is a floor, never a total. This project reports the floor and labels it as such. Databases "
 "that quietly estimate the missing values produce a bigger, more impressive and less true number.", "warn"))
F.append(table([
 ["Announced","Transaction","Sector","Value (US$m)"],
 ["2026","CoolIT minority stake sold to Ecolab, KKR-led","Technology","4,750 (transaction value)"],
 ["2025","ADIC indirect deployments","Multi-sector","19,061"],
 ["2025","Al Maryah Island transformation","Real estate","16,338"],
 ["2025","Tabreed - two largest ever transactions","Infrastructure","1,054"],
 ["2025","Fortress strategic partnership","Financial services","1,000 (to be deployed)"],
 ["2026","WHOOP Series G participation","Healthcare","575 (round size)"],
 ["2025","Nord Anglia Education stake","Education","600"],
 ["2025","Mubadala Capital Co-Investment Fund I close","Financial services","550"],
 ["2025","Barings global real-estate debt partnership","Real estate credit","500"],
],[20*mm,66*mm,32*mm,None],align={3:"RIGHT"}))
F.append(Paragraph(
 "The pattern in the undisclosed half is as informative as the disclosed half. Hornsea 3 offshore wind, the "
 "Greenlink interconnector, the Stonepeak container-leasing platform, the Aldar joint venture at Masdar City, "
 "the Tubacex energy-supply-chain venture and the Embraer aerospace agreement are all long-duration real assets "
 "or industrial partnerships. Mubadala is buying cash flows that are contracted, regulated or strategically "
 "protected, and it is doing so alongside partners - Apollo, KKR, Stonepeak, Equitix, Barings, Fortress - rather "
 "than alone. Co-investment is the operating model.", BODY))

F.append(PageBreak())
# ============================================================ 5 CASE 1
F.append(Paragraph("5.  Case study 1 - Technology: GlobalFoundries", H1))
F.append(Paragraph(
 "GlobalFoundries is a specialty semiconductor foundry listed on Nasdaq, in which Mubadala is the controlling "
 "shareholder with a stake widely reported at around 80% held through Mubadala Technology Investment Company. "
 "It is the largest single technology position in the group and the cleanest test of valuation discipline, "
 "because unlike most of the portfolio it has a daily market price to argue with.", BODY))
F.append(kpi_strip([
 ("Share price","$50.01","3 Aug 2026"),
 ("Enterprise value","$25.4bn","market"),
 ("Revenue TTM","$6.84bn","EBITDA $2.10bn"),
 ("EV / EBITDA","12.1x","peer UMC 14.5x")]))
F.append(Paragraph("5.1  Method and cost of capital", H2))
F.append(Paragraph(
 f"We built a five-year free-cash-flow-to-firm model. Cost of equity uses the capital asset pricing model with "
 f"a 4.25% risk-free rate, a 5.0% equity risk premium and the observed five-year beta of 1.76, giving "
 f"{g['wacc']['cost_of_equity']*100:.2f}%. With gross debt of US$1.72 billion against a US$27.4 billion market "
 f"capitalisation, the weighted average cost of capital is {g['wacc']['wacc']*100:.2f}%. As a sense check, the "
 f"published vendor estimate is 13.25% - close enough that the difference does not change the conclusion.", BODY))
F.append(Paragraph(
 "The revenue forecast starts from consensus, which puts three-year revenue growth at about 10% a year. We "
 "assume a cyclical recovery front-loaded into years two and three, fading to 5%. On margins we do not assume "
 "management delivers its stated plan in full: gross margin was 26.1% on a trailing basis against a public "
 "target of 40% by 2028 and 45% by 2030, and we model operating margin reaching 20% rather than the high-twenties "
 "that full delivery would imply.", BODY))
F.append(figure(C("07_gfs_football_field"),
 "Figure 5: GlobalFoundries valuation football field. Source: author's models.", 150))
F.append(Paragraph("5.2  Result, and the more interesting question", H2))
F.append(Paragraph(
 f"The base case values the equity at ${g['dcf_value_per_share']:.2f} a share, {abs(g['dcf_upside_pct']):.0f}% below "
 f"the traded price. Comparable-company analysis at 11.0 to 17.0 times EV/EBITDA gives "
 f"${g['comparables']['implied_value_per_share']['low']:.0f} to ${g['comparables']['implied_value_per_share']['high']:.0f}, "
 "a range that comfortably contains the market. Sell-side consensus sits at $80.24.", BODY))
F.append(Paragraph(
 "Rather than declare the market wrong, we inverted the model and solved for the assumption that would justify "
 f"the traded price. The answer is a steady-state operating margin of "
 f"{g['reverse_dcf']['implied_terminal_ebit_margin']*100:.1f}%, against "
 f"{g['reverse_dcf']['ttm_ebit_margin']*100:.1f}% today.", BODY))
F.append(callout("What that number means.",
 f"A {g['reverse_dcf']['implied_terminal_ebit_margin']*100:.0f}% operating margin is roughly what full delivery of "
 "management's 45% gross-margin target for 2030 would produce. The market is not pricing today's foundry; it is "
 "pricing the successful execution of a six-year margin plan, plus the silicon-photonics, quantum and automotive "
 "content that sits behind it. Buying the shares at $50 is an underwriting of execution, not a valuation call. "
 "Stating it that way makes the risk legible.", "warn"))
F.append(Paragraph("5.3  Evidence that the mix is already shifting", H2))
F.append(figure(C("08_gfs_mix_shift"),
 "Figure 6: Change in GlobalFoundries revenue mix, 2023-2025. Source: company reported segment data.", 150))
F.append(Paragraph(
 "Automotive silicon grew 34.8% between 2023 and 2025 and rose 6.6 percentage points as a share of revenue, "
 "while home and industrial internet-of-things fell 25.9% and lost 4.2 points. Smart mobile devices remain the "
 "largest end-market at 39% but are shrinking. This is a company actively rotating toward higher-content, "
 "longer-cycle silicon, which is consistent with the margin story - but the datacenter and communications "
 "line, the one most exposed to the AI narrative, is still only 11% of revenue and fell over the period. "
 "The optionality the market is paying for has not yet appeared in the reported numbers.", BODY))
F.append(callout("Peer selection - one exclusion, stated openly.",
 "Tower Semiconductor trades on 90.8 times EV/EBITDA after a 425% twelve-month re-rating. Including it in the "
 "peer median would not tell us what a foundry is worth; it would tell us what a momentum stock is worth. It is "
 "reported in the peer table and excluded from the applied range, and the exclusion is disclosed rather than "
 "buried. An unstated outlier exclusion is the most common way comparable-company analysis is quietly rigged.", "note"))

F.append(PageBreak())
# ============================================================ 6 CASE 2
F.append(Paragraph("6.  Case study 2 - Energy: OMV AG", H1))
F.append(Paragraph(
 "Mubadala holds 24.9% of OMV, the Vienna-listed integrated oil, gas and chemicals group, through Mubadala "
 "Petroleum and Petrochemicals Holding. It is a mature, cash-generative, cyclical asset with an 8.1% dividend "
 "yield - and it required three judgement calls that a mechanical model would have got wrong.", BODY))
F.append(Paragraph("6.1  Three adjustments, each disclosed", H2))
F+= numbered([
 "<b>The beta is not credible.</b> OMV's observed five-year beta is 0.21, which would imply an integrated "
 "energy producer carries almost no systematic risk. The cause is mechanical: a free float of 141 million "
 "shares out of 326 million and a domestic index listing suppress measured covariance. We substituted a "
 "European integrated-energy sector beta of 0.90 and disclosed the swap. The effect is to raise the cost of "
 f"equity to {o['wacc']['cost_of_equity']*100:.2f}% and the weighted average cost of capital to {o['wacc']['wacc']*100:.2f}%.",
 "<b>Enterprise value contains large minorities.</b> Market capitalisation is EUR17.6 billion and enterprise "
 "value EUR24.2 billion, but net debt is only EUR2.8 billion. The residual - roughly EUR3.75 billion - is "
 "minority interest, because OMV fully consolidates Borealis and Borouge while owning less than all of them. "
 "Failing to deduct it in the equity bridge would have overstated value per share by about 25%.",
 "<b>Reported earnings are not capitalisable.</b> Trailing twelve-month earnings per share of EUR7.20 include "
 "EUR1,303 million from <i>discontinued</i> operations. Applying a price/earnings multiple to that would value "
 "a business OMV no longer owns. FY2025 earnings of EUR3.11 are equally unusable in the other direction, having "
 "absorbed EUR497 million of write-downs. We used a three-year average of EUR3.96 as a mid-cycle proxy.",
])
F.append(Paragraph("6.2  Result", H2))
F.append(Paragraph(
 f"The discounted cash flow values the equity at EUR{o['dcf_value_per_share']:.2f} a share against a market price "
 f"of EUR{o['market']['price_eur']:.2f} - within 4%, which for a commodity business is as close to 'fairly valued' "
 f"as a model gets. Normalised price/earnings comparables against Shell, TotalEnergies, Eni and BP give a range "
 f"of EUR{o['comparables']['implied_value_per_share']['low']:.0f} to EUR{o['comparables']['implied_value_per_share']['high']:.0f} "
 f"with a median of EUR{o['comparables']['implied_value_per_share']['median']:.0f}. Consensus sits at EUR61.", BODY))
F.append(figure(C("14_omv_football_field"),
 "Figure 7: OMV valuation football field. Source: author's models.", 150))
F.append(Paragraph("6.3  The dividend is the real story", H2))
F.append(Paragraph(
 "OMV yields 8.1%. The relevant question is not whether the shares are cheap but whether the distribution is "
 "funded by cash the business actually earns. We tested free-cash-flow cover across five years.", BODY))
F.append(figure(C("09_omv_dividend_cover"),
 "Figure 8: OMV free cash flow versus the cost of the dividend, 2021-2025. Source: company reported data.", 150))
F.append(table([
 ["Year","Free cash flow (EURm)","Dividend per share","Dividend cost (EURm)","FCF cover"],
 ["2021","4,520","EUR2.30","750","6.03x"],
 ["2022","4,815","EUR2.80","913","5.27x"],
 ["2023","2,222","EUR2.95","962","2.31x"],
 ["2024","1,943","EUR3.05","994","1.95x"],
 ["2025","1,366","EUR3.15","1,027","1.33x"],
],[18*mm,40*mm,32*mm,36*mm,None],align={1:"RIGHT",3:"RIGHT",4:"RIGHT"}))
F.append(callout("The finding.",
 "Cover has fallen from 6.0 times to 1.3 times in four years while the dividend per share has been raised "
 "every single year. The payout is still covered - just. But the margin of safety has effectively gone, and "
 "one further leg down in refining or chemicals margins forces the distribution to be funded from the balance "
 "sheet or cut. For a shareholder like Mubadala, whose interest in this asset is substantially the cash it "
 "returns, that trajectory matters more than the two per cent of upside in the valuation.", "warn"))

F.append(PageBreak())
# ============================================================ 7 CASE 3
F.append(Paragraph("7.  Case study 3 - Healthcare: WHOOP", H1))
F.append(Paragraph(
 "In March 2026 WHOOP, the AI-driven human-performance and health platform, raised US$575 million in Series G "
 "funding at a US$10.1 billion post-money valuation. Mubadala participated alongside the Qatar Investment "
 "Authority, Abbott, Mayo Clinic and Collaborative Fund, which led. Mubadala separately announced a UAE "
 "preventative-health and research partnership with the company.", BODY))
F.append(kpi_strip([
 ("Post-money valuation","$10.1bn","31 Mar 2026"),
 ("Bookings run-rate","$1.1bn","exiting 2025"),
 ("2025 bookings growth","+103%","cash-flow positive"),
 ("Members","2.5m+","$440 revenue each")]))
F.append(Paragraph("7.1  Why a normal DCF would have been dishonest", H2))
F.append(Paragraph(
 "WHOOP is private. It publishes no accounts. Building a ten-year forecast from nothing and presenting the "
 "output as a valuation would be an exercise in laundering assumptions through arithmetic. So we ran the model "
 "backwards. The price a syndicate of sophisticated investors actually paid is a hard fact; what that price "
 "implies about the future is the thing worth calculating.", BODY))
F.append(Paragraph(
 f"At a US$10.1 billion post-money valuation on a US$1.1 billion run-rate, WHOOP was priced at "
 f"{wh['implied_entry_multiples']['ev_revenue_post_money']:.1f} times revenue, or "
 f"{wh['implied_entry_multiples']['ev_revenue_pre_money']:.1f} times excluding the cash just raised. The median "
 f"listed healthcare platform in our reference set trades at {wh['listed_reference_multiples']['median_price_to_sales']:.1f} "
 f"times sales, so the entry price is a {wh['listed_reference_multiples']['premium_to_listed_median_x']:.1f}-times premium "
 "to public comparables.", BODY))
F.append(Paragraph("7.2  Solving for what the price assumes", H2))
F.append(Paragraph(
 "Holding a required return of 18%, terminal growth of 3.5%, a ten-year horizon and free-cash-flow margins "
 "ramping from 4% to 20%, we solved for the revenue growth rate that reproduces the price paid.", BODY))
F.append(callout("The answer.",
 f"Revenue must compound at <b>{wh['reverse_dcf']['implied_revenue_cagr']*100:.1f}% a year for ten years</b>, taking "
 f"WHOOP from a US$1.1 billion run-rate to roughly <b>US${wh['reverse_dcf']['implied_revenue_year10_usd_bn']:.0f} billion "
 "by 2035</b>, while free-cash-flow margins reach 20%. That is demanding. It is not absurd against 2025 bookings "
 "growth of 103% and a business that was already cash-generative. The investment question is therefore about the "
 "<i>durability</i> of growth, not its direction - and durability in consumer subscriptions is a churn question, "
 "which is the one metric not disclosed.", "find"))
F.append(figure(C("10_whoop_scenarios"),
 "Figure 9: WHOOP scenario values against the price paid. Source: author's reverse-DCF model.", 150))
F.append(Paragraph(
 "The scenario spread is wide and asymmetric in an instructive way. If growth fades to 12% and margins cap at "
 "12%, the equity is worth about US$1.0 billion - an 89% loss from the entry price. If platform economics take "
 "hold at 42% growth and 25% margins, it is worth about US$24.6 billion. This is the shape of a venture position: "
 "a small probability of a very large outcome, funded by accepting a meaningful probability of near-total loss. "
 "Mubadala's participation is sized accordingly, as a minority in a syndicated round, which is the correct "
 "response to that payoff distribution.", BODY))
F.append(Paragraph("7.3  Why this asset fits the strategy", H2))
F+= bullets([
 "It is an <b>AI-data business wearing healthcare clothing</b>. Twenty-four billion hours of physiological data "
 "is the asset; the wrist strap is the collection mechanism. That is the same thesis as the group's semiconductor "
 "and AI-infrastructure positions, expressed in a different sector.",
 "The <b>UAE partnership converts a financial holding into a national-mandate asset</b>, bringing preventative-health "
 "capability onshore. One cheque serves both of Mubadala's objectives.",
 "Abbott and Mayo Clinic joining as strategic investors materially <b>de-risks the regulatory pathway</b> from "
 "consumer wellness toward clinical-grade prediction, which is where the durable margin would come from.",
])

F.append(PageBreak())
# ============================================================ 8 CASE 4
F.append(Paragraph("8.  Case study 4 - Financial services: Mubadala Capital", H1))
F.append(Paragraph(
 "Mubadala Capital is the group's wholly owned alternative asset manager. Mubadala's own website states that it "
 "manages approximately US$30 billion in aggregate across balance-sheet investments and third-party capital "
 "vehicles, through four businesses: Private Equity, Brazil, Venture Capital and Solutions. That single figure "
 "is the only hard input available - everything else in this case study is a labelled assumption, and the output "
 "is a framework rather than a valuation opinion.", BODY))
F.append(Paragraph("8.1  The question worth asking", H2))
F.append(Paragraph(
 "Not 'what is Mubadala Capital worth' - nobody outside the group can answer that. The useful question is "
 "structural: <i>if it were listed, what would the market pay for the fee stream, and therefore how much value "
 "does the asset-management franchise add on top of the investment returns Mubadala earns anyway?</i>", BODY))
F.append(table([
 ["Input","Value","Grade"],
 ["Aggregate AUM","US$30bn","Official - mubadala.com"],
 ["Third-party share of AUM","60%","Author assumption"],
 ["Blended management fee rate","1.20%","Author assumption"],
 ["Implied management fee revenue","US$216m","Derived"],
 ["Fee-related-earnings margin","35%","Author assumption"],
 ["Implied fee-related earnings","US$76m","Derived"],
 ["Private-company / control discount","25%","Author assumption"],
],[62*mm,32*mm,None]))
F.append(figure(C("11_mubadala_capital"),
 "Figure 10: Implied value of the Mubadala Capital fee franchise. Source: author's model.", 150))
F.append(Paragraph(
 f"Benchmarked against Blackstone, Ares, Blue Owl and TPG on price-to-fee-revenue, and cross-checked on "
 f"Blackstone's price/earnings multiple applied to fee-related earnings, the central estimate is "
 f"US${mc['central_before_discount_usd_bn']:.2f} billion before discount and "
 f"US${mc['central_after_discount_usd_bn']:.2f} billion after a 25% private-company discount - roughly "
 f"{mc['as_pct_of_group_aum']:.1f}% of group AUM.", BODY))
F.append(callout("Apollo excluded, and why.",
 "Apollo's reported revenue consolidates Athene's insurance premiums, which puts it on 2.1 times sales against "
 "a cohort clustered between 5 and 11 times. That is not a valuation signal, it is an accounting artefact. It is "
 "shown in the peer table and excluded from the applied range.", "note"))
F.append(Paragraph("8.2  Why the structure matters more than the number", H2))
F.append(Paragraph(
 "The number is soft. The structural point is not. Mubadala Capital converts third-party capital into a fee "
 "annuity that is valued on a multiple of earnings, sitting on top of the investment return earned on Mubadala's "
 "own balance sheet. Three consequences follow.", BODY))
F+= bullets([
 "<b>It extends reach beyond the balance sheet.</b> Third-party capital lets Mubadala underwrite transactions "
 "larger than its own equity cheque would allow, and take fees for the privilege.",
 "<b>It is counter-cyclical to realisations.</b> Management fees keep arriving when exit markets close. Given "
 "a recycling ratio near 1.0, that insulation has real value.",
 "<b>It is the only part of the group creating value independently of asset prices.</b> Everything else in the "
 "portfolio is a claim on the direction of markets. A fee stream is a claim on assets under management, which "
 "is a different and steadier thing.",
])

F.append(PageBreak())
# ============================================================ 9 QUANT
F.append(Paragraph("9.  Quantitative and AI analysis", H1))
F.append(Paragraph("9.1  Is the disclosed asset mix efficient?", H2))
F.append(Paragraph(
 "We built an efficient frontier over the five disclosed asset classes using long-horizon capital-market "
 "assumptions. Mubadala publishes weights but not returns, volatilities or correlations, so those inputs are the "
 "author's and are stated explicitly in the model file. The conclusions below concern structure, not precision.", BODY))
F.append(figure(C("05_efficient_frontier"),
 "Figure 11: The disclosed mix against the efficient frontier. Source: author's optimisation.", 140))
F.append(Paragraph(
 f"On these assumptions the published mix has an expected return of {po['actual_portfolio']['expected_return']*100:.2f}% "
 f"with volatility of {po['actual_portfolio']['volatility']*100:.2f}%, a Sharpe ratio of "
 f"{po['actual_portfolio']['sharpe']:.3f}. An efficient portfolio delivering the same return would carry "
 f"{po['efficiency_test']['efficient_volatility_at_same_return']*100:.2f}% volatility - so the actual allocation "
 f"is carrying about {po['efficiency_test']['excess_volatility_carried_pp']} percentage points of avoidable risk.", BODY))
F.append(Paragraph(
 "Almost all of that gap is the public-equity sleeve. The maximum-Sharpe portfolio holds <b>no</b> listed equity "
 "at all, replacing it with credit at 26% against an actual 5%. On a pure risk-return basis the 20% public "
 "allocation is not earning its place.", BODY))
F.append(callout("But that is not a criticism.",
 "A sovereign investor holds liquid assets so that a drawdown can be funded without selling private positions "
 "into a bad market. The optimiser cannot see that constraint because it has no concept of liquidity. What the "
 "exercise does is put a price on the insurance: roughly one percentage point of volatility, or about 0.5 "
 "percentage points of expected return. That is a number a board can debate. 'Is 20% public equity right?' is not.", "find"))
F.append(Paragraph(
 "Running the optimisation in reverse is more revealing still. If we assume the published weights <i>are</i> "
 "optimal and solve for the returns that would make them so, the implied expectations are: private 11.0%, "
 "public 10.0%, alternatives 8.4%, real estate and infrastructure 7.2%, credit 5.5%. Those are the beliefs an "
 "allocator must hold to justify this portfolio, and unlike the allocation itself they can be argued with directly.", BODY))
F.append(Paragraph("9.2  Ten-year outlook under uncertainty", H2))
F.append(Paragraph(
 "We simulated 50,000 ten-year paths for AUM using the disclosed 10.7% five-year return, an assumed 12.5% "
 "volatility, the observed US$1 billion of annual net deployment, and Student-t shocks with five degrees of "
 "freedom so that the tails are fat in the way real markets are.", BODY))
F.append(figure(C("06_monte_carlo"),
 "Figure 12: Ten-year AUM simulation, 50,000 paths. Source: author's Monte Carlo model.", 150))
F.append(table([
 ["Percentile","2035 AUM (US$bn)","Implied CAGR"],
 ["5th","559","3.8%"],
 ["25th","819","7.9%"],
 ["Median","1,058","10.6%"],
 ["75th","1,360","13.4%"],
 ["95th","2,004","17.9%"],
],[34*mm,44*mm,None],align={1:"RIGHT",2:"RIGHT"}))
F.append(Paragraph(
 f"The median path crosses US$1 trillion, and the probability of reaching that level by 2035 is "
 f"{sim['probabilities']['P(AUM > $1,000bn by 2035)']*100:.0f}%. Equally important is the downside: the median "
 f"worst peak-to-trough drawdown along a path is {abs(sim['drawdown']['median_max_drawdown'])*100:.1f}%, and there "
 f"is a {sim['drawdown']['P(peak-to-trough drawdown worse than 20%)']*100:.0f}% probability of a drawdown worse "
 "than 20% at some point in the decade. Planning for the median while ignoring the path is how institutions get "
 "caught needing liquidity at the worst moment - which brings the argument back to why that 20% public sleeve exists.", BODY))
F.append(Paragraph("9.3  Machine learning: tagging deal flow automatically", H2))
F.append(Paragraph(
 "Sovereign investors publish hundreds of free-text announcements a year. Tagging each to a sector by hand is "
 "slow and inconsistent between analysts. We trained a text classifier - TF-IDF word and character n-grams "
 "feeding a multinomial logistic regression - to read a headline and predict the sector.", BODY))
F.append(figure(C("13_classifier_confusion"),
 "Figure 13: Classifier confusion matrix. Source: author's model.", 108))
F.append(Paragraph(
 f"The honest measure of the model is the hold-out test: twelve real Mubadala announcements that appear nowhere "
 f"in training. The classifier got {clf['holdout_real_headlines']['accuracy']*100:.0f}% of them right.", BODY))
F.append(callout("The single failure is the most useful result.",
 "The model tagged 'Mubadala agrees to sell minority stake in CoolIT data centre liquid cooling to Ecolab' as "
 "Industrials rather than Technology. It is not obviously wrong. CoolIT makes physical cooling hardware for AI "
 "data centres - it is genuinely both. The lesson is not that the classifier needs more training data; it is that "
 "a single-label data model is the wrong shape for a portfolio where the most interesting assets sit between "
 "sectors. The fix is multi-label tagging, and that is a data-design decision, not a modelling one.", "warn"))
F.append(Paragraph("9.4  Do the chosen comparables match how the market groups companies?", H2))
F.append(Paragraph(
 "Analysts pick comparables by industry label. Markets price business characteristics. We clustered the "
 "nineteen-company peer universe on size and valuation features, choosing the number of clusters by silhouette "
 "score rather than by eye. GlobalFoundries' nearest neighbours in that space turn out to be ON Semiconductor "
 "and Agilent Technologies - not TSMC or UMC. The market treats it as a mid-cap specialty manufacturer, which "
 "is a useful corrective to a peer set assembled purely from the word 'foundry'.", BODY))

F.append(PageBreak())
# ============================================================ 10 CONCLUSIONS
F.append(Paragraph("10.  Conclusions, risks and limitations", H1))
F.append(Paragraph("10.1  What the analysis supports", H2))
F+= numbered([
 "<b>Mubadala is running a concentrated, illiquid, self-funding book, and that is a coherent strategy for a "
 "permanent-capital sovereign investor.</b> The HHI of 2,734 and the 58% private-plus-alternatives weighting are "
 "features, not bugs. The recycling ratio near 1.0 shows the model works without new shareholder capital.",
 "<b>Technology is the organising theme, expressed through four platforms rather than one bucket.</b> "
 "Semiconductors, AI infrastructure, AI-enabled healthcare and energy-transition software all recur, and the "
 "CoolIT exit demonstrates the theme being realised rather than merely accumulated.",
 "<b>The liquid sleeve is insurance, and the insurance costs about one point of volatility.</b> Naming the price "
 "converts a governance argument into a quantified trade-off.",
 "<b>Valuation discipline differs sharply by asset, and the differences are the useful output.</b> "
 "GlobalFoundries is priced for execution; OMV is fairly valued with a deteriorating dividend cushion; WHOOP is "
 "priced for a decade of 35% growth; Mubadala Capital's fee annuity is the only holding whose value does not "
 "depend on the direction of markets.",
])
F.append(Paragraph("10.2  Risks to the strategy", H2))
F.append(table([
 ["Risk","Why it matters here","Where it shows up in this report"],
 ["Exit-market closure","A recycling ratio near 1.0 means deployment depends on realisations. If exit markets "
  "freeze, deployment must fall or the balance sheet must lever.","Section 4"],
 ["Concentration in private assets","58% of the book is marked infrequently. Reported volatility understates "
  "true economic volatility.","Sections 3.2 and 9.1"],
 ["Execution risk in semiconductors","The GlobalFoundries share price requires a margin expansion of more than "
  "20 percentage points. Any slippage is repriced directly.","Section 5.2"],
 ["Commodity and dividend risk","OMV's dividend cover has fallen to 1.3x. A cut would hit both the income and "
  "the equity value of a 24.9% stake.","Section 6.3"],
 ["Venture-stage mispricing","WHOOP's entry multiple leaves no room for a growth disappointment; the bear case "
  "is an 89% loss.","Section 7.2"],
 ["Geopolitical and regulatory","Semiconductor, AI and energy assets are precisely the sectors most exposed to "
  "export controls, screening regimes and subsidy politics.","Sections 3.3 and 5"],
],[38*mm,None,28*mm]))
F.append(Paragraph("10.3  Limitations - what this report cannot tell you", H2))
F+= bullets([
 "<b>There is no position-level portfolio.</b> Mubadala does not publish one. The twenty tracked holdings are a "
 "curated, source-tagged sample, not the whole book, and the sector percentages describe that sample rather than "
 "the group's true economic exposure.",
 "<b>Deal totals are floors.</b> Ten of nineteen logged transactions disclose no value. The US$44.4 billion "
 "figure is what is public, not what was spent.",
 "<b>Capital-market assumptions are the author's.</b> Expected returns, volatilities and correlations behind the "
 "optimiser and the simulation are not Mubadala's. Change them and the conclusions about efficiency change with them.",
 "<b>All forward assumptions are estimates.</b> Growth rates, margins, discount rates and terminal values in "
 "every DCF are judgements. The sensitivity tables in the workbook exist so a reader can substitute their own.",
 "<b>Two case studies value private companies.</b> WHOOP and Mubadala Capital are frameworks built on stated "
 "assumptions. They are designed to expose their own inputs, not to produce a defensible price.",
 "<b>Nothing here is investment advice</b>, and the author holds no position in any security mentioned.",
])
F.append(Paragraph("10.4  What I would do next with more time", H2))
F+= bullets([
 "Replace the manual holdings dataset with an automated pipeline that ingests Mubadala's newsroom RSS feed, "
 "runs the classifier, and refreshes the warehouse nightly.",
 "Move from single-label to multi-label sector tagging, which the CoolIT failure showed is the real constraint.",
 "Extend the peer clustering to a full sector universe and use it to select comparables systematically rather "
 "than by hand.",
 "Add a currency layer: OMV is a euro asset, GlobalFoundries a dollar asset, and the reporting currency is the "
 "dirham. The FX translation effect on reported AUM is not modelled here and is not trivial.",
])
F.append(Spacer(1,6))
F.append(Paragraph("Sources", H2))
F.append(table([
 ["ID","Source","As of","Class"],
 ["S01","Mubadala press release - 2025 annual results (mubadala.com)","9 Apr 2026","Official"],
 ["S02","Mubadala 2025 Annual Review - Performance Overview","9 Apr 2026","Official"],
 ["S03","Mubadala 2025 Annual Review - Key Investment Highlights","9 Apr 2026","Official"],
 ["S04","Mubadala corporate site - Our Structure","4 Aug 2026","Official"],
 ["S05","Mubadala press release - WHOOP Series G","31 Mar 2026","Official"],
 ["S06","Mubadala newsroom - 2026 transaction announcements","4 Aug 2026","Official"],
 ["S07","StockAnalysis / S&amp;P Global Market Intelligence - GlobalFoundries","3 Aug 2026","Market data"],
 ["S08","StockAnalysis / S&amp;P Global Market Intelligence - OMV AG","30 Jun 2026","Market data"],
 ["S09","StockAnalysis - listed peer comparison tables","4 Aug 2026","Market data"],
 ["S10","Analyst estimates constructed for this project","4 Aug 2026","Analyst estimate"],
],[14*mm,None,24*mm,26*mm]))
F.append(Spacer(1,8))
F.append(Paragraph(
 "<i>This document was produced as an independent research project. It is not investment advice, not a "
 "recommendation to buy or sell any security, and not affiliated with or endorsed by Mubadala Investment "
 "Company. All forward-looking statements are the author's estimates.</i>", SMALL))

doc.build(F)
print("Built Equity_Research_Report.pdf")
