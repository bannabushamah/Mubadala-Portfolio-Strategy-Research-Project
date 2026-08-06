# -*- coding: utf-8 -*-
"""Beginner guide booklet - part 2 (steps 4-9 plus closing material)."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pdf_style import *
from build_guide_p1 import step_header, prosecons

ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH=os.path.join(ROOT,"07_charts"); C=lambda n: os.path.join(CH,n+".png")
VAL=os.path.join(ROOT,"03_valuation_models","outputs"); AI=os.path.join(ROOT,"04_ai_ml","outputs")
J=lambda p: json.load(open(p))
g=J(os.path.join(VAL,"case_01_globalfoundries.json")); o=J(os.path.join(VAL,"case_02_omv.json"))
wh=J(os.path.join(VAL,"case_03_whoop.json")); mc=J(os.path.join(VAL,"case_04_mubadala_capital.json"))
po=J(os.path.join(AI,"portfolio_optimisation.json")); sim=J(os.path.join(AI,"monte_carlo.json"))
clf=J(os.path.join(AI,"deal_classifier.json"))

def build():
    F=[]
    # ---------------- STEP 4 ----------------
    F.append(PageBreak())
    F.append(step_header("4","Working out what a company is worth",
                         "The four valuation case studies, explained from zero"))
    F.append(Paragraph("The idea behind all valuation, in one paragraph", H2))
    F.append(Paragraph(
     "A business is worth the cash it will hand you in the future, adjusted for the fact that cash later is worth "
     "less than cash now. That is it. Everything else - every model, every multiple, every spreadsheet - is a "
     "different way of estimating those two things. If you understand that sentence you understand valuation; the "
     "rest is bookkeeping.", LEAD))
    F.append(callout("Jargon box: discounting, and why later money is worth less.",
     "If someone offers you 100 pounds today or 100 pounds in a year, you take it today - you could invest it, and "
     "you avoid the risk they never pay. So future money must be shrunk before you compare it. If your required "
     "return is 10%, then 110 pounds next year is worth 100 today: you divide by 1.10. Money in two years gets "
     "divided by 1.10 twice. That shrinking is called <b>discounting</b>, and the rate you shrink by is the "
     "<b>discount rate</b>.", "note"))
    F.append(Paragraph("Method A - the discounted cash flow (DCF)", H2))
    F.append(Paragraph("Five steps, and I did exactly these five for GlobalFoundries and OMV:", BODY))
    F+= numbered([
     "<b>Forecast the cash</b> the business generates each year for five years.",
     "<b>Work out the discount rate</b> - how much return an investor needs to bother owning it.",
     "<b>Shrink each year's cash</b> back to today's money using that rate.",
     "<b>Add a terminal value</b> for everything after year five, because businesses do not stop in year six.",
     "<b>Add it all up</b>, then subtract debt and add cash to get to what the shares are worth.",
    ])
    F.append(callout("Jargon box: free cash flow to the firm (FCFF), and WACC.",
     "<b>FCFF</b> is the cash left over for everyone who funded the business - shareholders and lenders together - "
     "after paying costs, tax and the cost of maintaining the assets. The formula I used is: operating profit, "
     "minus tax, plus depreciation (which is an accounting charge, not real cash leaving), minus what the company "
     "spends on new equipment, minus any extra cash tied up in inventory and unpaid bills.<br/><br/>"
     "<b>WACC</b> (weighted average cost of capital) is the blended return that shareholders and lenders together "
     "demand. Shareholders want more because they get paid last; lenders want less because they get paid first and "
     "the interest is tax-deductible. You blend the two in proportion to how much of each the company uses.", "note"))
    F.append(Paragraph("Here is the GlobalFoundries WACC, built up number by number:", BODY))
    F.append(table([
     ["Ingredient","Value","In plain English"],
     ["Risk-free rate","4.25%","What you would earn lending to the US government. My assumption."],
     ["Equity risk premium","5.00%","The extra return shares must offer over government bonds. My assumption."],
     ["Beta","1.76","How violently this share moves versus the market. 1.0 = moves with it; 1.76 = moves 76% harder. Observed."],
     ["Cost of equity","13.05%","4.25% + (1.76 x 5.00%). This is the CAPM formula."],
     ["Cost of debt after tax","4.68%","5.5% interest, reduced because interest is tax-deductible."],
     ["Weight of equity / debt","94% / 6%","GlobalFoundries barely uses debt, so equity dominates the blend."],
     ["<b>WACC</b>","<b>12.55%</b>","The final discount rate. A published vendor estimate is 13.25% - close enough."],
    ],[40*mm,24*mm,None]))
    F.append(Paragraph("Method B - comparable companies ('comps')", H2))
    F.append(Paragraph(
     "The house-price method. If the identical house next door sold for 400,000, yours is probably worth about "
     "400,000. In finance you find similar companies, see what multiple of their profits the market pays, and "
     "apply that multiple to your company.", BODY))
    F.append(callout("Jargon box: EV/EBITDA and P/E.",
     "<b>P/E</b> is share price divided by earnings per share - how many years of profit you are paying for. "
     "<b>EV/EBITDA</b> is a bit fairer for comparing companies with different debt levels. EV (enterprise value) "
     "is the market value of the shares plus the debt minus the cash - what it would cost to buy the whole business "
     "outright. EBITDA is profit before interest, tax, depreciation and amortisation. Using EV with EBITDA compares "
     "like with like, because both ignore how the business is financed.", "note"))
    F.append(Paragraph(
     "The hard part of comps is not the arithmetic, it is choosing the peers. Tower Semiconductor trades at 90.8 "
     "times EV/EBITDA after its share price rose 425% in a year. Including it would have pushed the peer median to "
     "about 52x and produced a valuation of over $200 a share for a stock trading at $50 - obvious nonsense. So I "
     "excluded it, <b>and wrote down that I had excluded it and why</b>.", BODY))
    F.append(callout("This is where comps analysis is usually quietly rigged.",
     "It is very easy to pick the peers that give you the answer you already wanted, and nobody can tell from the "
     "output. The defence is to state your peer set, state your exclusions, and state your reason for each. If your "
     "reasoning is sound, the exclusion is analysis. If it is unstated, it is manipulation - even when you did not "
     "mean it to be.", "warn"))
    F.append(Paragraph("Method C - the reverse DCF, which is the best trick in this project", H2))
    F.append(Paragraph(
     "My GlobalFoundries DCF said $35.07. The market said $50.01. The beginner's instinct is to declare the market "
     "wrong. The better move is to run the model backwards: hold everything else constant and solve for the one "
     "assumption that would make the model agree with the price.", BODY))
    F.append(callout("The answer, and why it is so much more useful than a price target.",
     f"To justify $50.01, GlobalFoundries needs a long-run operating margin of "
     f"<b>{g['reverse_dcf']['implied_terminal_ebit_margin']*100:.1f}%</b>. It earns "
     f"{g['reverse_dcf']['ttm_ebit_margin']*100:.1f}% today. That is roughly what full delivery of management's "
     "published 2030 margin plan would produce.<br/><br/>"
     "So the sentence changes from 'I think it's overvalued' - which is just an opinion - to 'at this price you are "
     "underwriting complete execution of a six-year margin plan'. The second sentence is checkable, and it tells "
     "you exactly what to monitor each quarter.", "find"))
    F.append(figure(C("07_gfs_football_field"),
     "The 'football field' chart. Each bar is one valuation method's range; the red line is the actual share price. "
     "Analysts use this because no single method deserves to be trusted alone.", 145))
    F.append(Paragraph("Method D - valuing a company with no accounts", H2))
    F.append(Paragraph(
     "WHOOP is private. It publishes nothing. Building a ten-year forecast out of thin air and calling the output "
     "a valuation would be dressing up a guess in arithmetic. But one thing <i>is</i> known and hard: in March 2026 "
     "a syndicate including Mubadala, the Qatar Investment Authority, Abbott and the Mayo Clinic paid a price that "
     "valued the company at US$10.1 billion. So I ran the reverse DCF on that price.", BODY))
    F.append(callout("What US$10.1 billion assumes.",
     f"Revenue compounding at <b>{wh['reverse_dcf']['implied_revenue_cagr']*100:.1f}% every year for ten years</b>, "
     f"growing from a US$1.1 billion run-rate to about US${wh['reverse_dcf']['implied_revenue_year10_usd_bn']:.0f} "
     "billion by 2035, with cash margins reaching 20%. Given that bookings grew 103% in 2025 and the company was "
     "already cash-generative, that is demanding rather than impossible. The real risk is not whether it grows - "
     "it is whether it <i>keeps</i> growing, which depends on subscription churn, the one number nobody publishes.", "find"))
    F.append(prosecons(
     ["DCF","Comparable companies","Reverse DCF"],
     ["Forces you to state every assumption. Values the business, not the mood of the market.",
      "Fast. Reflects what buyers are actually paying today. Hard to argue with market prices.",
      "Turns disagreement into a testable claim. Works on private companies where a forward DCF cannot."],
     ["Enormously sensitive - shift the terminal growth rate by 1% and the value swings 20%+. Garbage in, garbage out.",
      "If the whole sector is mispriced, comps inherit the mistake. Peer choice can be quietly rigged.",
      "You still need every other assumption. It tells you what is priced in, not whether it will happen."],
     "All three, on purpose, and shown side by side on a football field. Any single method presented alone should "
     "make a reader suspicious."))

    # ---------------- STEP 5 ----------------
    F.append(PageBreak())
    F.append(step_header("5","Building the Excel model",
                         "A workbook with live formulas, not pasted numbers"))
    F.append(Paragraph("What I did", H2))
    F.append(Paragraph(
     "Everything I calculated in Python I rebuilt in Excel with <b>real formulas</b>. Change the WACC cell on the "
     "GlobalFoundries sheet and the value per share moves. Seven sheets: a cover, the two DCFs, the OMV dividend "
     "test, the WHOOP reverse DCF, the Mubadala Capital model, and a source register.", BODY))
    F.append(Paragraph(
     "I used the colour convention every banking desk uses, and it is worth adopting because it makes a model "
     "readable in seconds:", BODY))
    F.append(table([
     ["Colour","Meaning","Why it matters"],
     ["<font color='#0000CC'><b>Blue</b></font>","A hard-coded input you may change",
      "Tells a reviewer exactly which cells are assumptions - the only ones that can be argued with."],
     ["<b>Black</b>","A formula calculated on this sheet",
      "Never type over a black cell. If a number should be black and is blue, someone has broken the model."],
     ["<font color='#008000'><b>Green</b></font>","A link to another sheet",
      "Shows where a number arrives from without having to trace it."],
    ],[24*mm,58*mm,None]))
    F.append(Paragraph("Why bother, when Python already gave me the answer?", H2))
    F.append(Paragraph(
     "Because of who reads it. Most people who assess this project will open the Excel file before they open the "
     "Python. A workbook of pasted values is dead - nobody can interrogate it. A workbook with live formulas invites "
     "the reader to change an assumption and see what happens, which is exactly what an interviewer will do. "
     "Building it twice also caught two real errors, described below.", BODY))
    F.append(callout("The cross-check that found genuine mistakes.",
     "I forced the Excel workbook to recalculate and compared every output to Python. GlobalFoundries: $35.05 in "
     "Excel against $35.07 in Python - a rounding difference in WACC, fine. WHOOP reverse DCF: within 0.2%, fine. "
     "But Mubadala Capital came out at $1.42bn in Excel and $1.73bn in Python. That was not rounding - it was a "
     "real methodology difference. Python was including a peer P/E of 81.9x that was inflated by fee-timing "
     "distortions; Excel was not. Excel was right. I changed the Python to match and documented why.<br/><br/>"
     "<b>Building the same thing twice in two tools is the cheapest error-detector in analytics.</b> If I had only "
     "built it once, that inconsistency would have shipped.", "warn"))
    F.append(prosecons(
     ["Excel only","Python only","Both, cross-checked"],
     ["Universal. Everyone can open and audit it. Live and interactive.",
      "Repeatable. Version-controllable. Handles simulation and machine learning that Excel cannot.",
      "You get auditability and repeatability, and any disagreement between them is a bug you would otherwise ship."],
     ["Fragile. No version control. Cannot do Monte Carlo or ML. Errors hide inside cells.",
      "Most finance reviewers will not run it. Feels like a black box to a non-coder.",
      "Twice the work, and you must keep them in sync."],
     "Both. It cost extra time and it found a real error, which is the whole argument."))

    # ---------------- STEP 6 ----------------
    F.append(PageBreak())
    F.append(step_header("6","The quantitative and AI layer",
                         "Four techniques, each answering a question I could not answer otherwise"))
    F.append(Paragraph("6a. Portfolio optimisation - is the asset mix sensible?", H2))
    F.append(callout("Jargon box: the efficient frontier.",
     "For any set of investments there is a curve showing the best possible return for each level of risk. Anything "
     "on the curve is 'efficient'; anything below and to the right is carrying risk it is not being paid for. The "
     "maths is Harry Markowitz's, from 1952, and it won a Nobel Prize. The core insight is that risk is not about "
     "individual assets, it is about how they move <i>together</i>.", "note"))
    F.append(figure(C("05_efficient_frontier"),
     "The gold dot is Mubadala's actual mix. The navy curve is the best you could theoretically do. The gap is "
     "the risk being carried for no extra return.", 132))
    F.append(Paragraph(
     f"The result: Mubadala's disclosed mix carries about "
     f"{po['efficiency_test']['excess_volatility_carried_pp']} percentage points more volatility than an efficient "
     "portfolio at the same expected return. Almost all of the gap is the 20% held in public shares - the "
     "return-maximising portfolio would hold none at all.", BODY))
    F.append(callout("But do not stop at 'therefore they are wrong'.",
     "The optimiser has no concept of liquidity. A sovereign fund holds listed shares so it can raise cash in a "
     "crisis without dumping private stakes at a discount. So the honest conclusion is not 'the mix is inefficient' "
     "- it is <b>'the liquidity insurance costs about one percentage point of volatility'</b>. That version is a "
     "number a board can debate. It is also a much better interview answer, because it shows you know what your "
     "model cannot see.", "find"))
    F.append(Paragraph("6b. Reverse optimisation - what must they believe?", H2))
    F.append(Paragraph(
     "Instead of asking whether the mix is right, assume it <i>is</i> right and solve backwards for the returns "
     "that would justify it. The answer: private 11.0%, public 10.0%, alternatives 8.4%, real estate and "
     "infrastructure 7.2%, credit 5.5%. Those are now beliefs you can argue with individually, which is far more "
     "productive than arguing about a percentage weight.", BODY))
    F.append(Paragraph("6c. Monte Carlo simulation - what could the next decade look like?", H2))
    F.append(callout("Jargon box: Monte Carlo.",
     "Named after the casino. Instead of forecasting one future, you simulate tens of thousands of random futures "
     "and look at the distribution of outcomes. I ran 50,000 ten-year paths for Mubadala's AUM using its disclosed "
     "10.7% return, an assumed 12.5% volatility, and 'fat-tailed' random shocks - meaning extreme years are more "
     "common than a normal bell curve would suggest, which is how real markets actually behave.", "note"))
    F.append(figure(C("06_monte_carlo"),
     "50,000 simulated futures. The navy line is the median; the gold band covers the middle 80% of outcomes.", 145))
    F.append(Paragraph(
     f"Median 2035 AUM: US${sim['outcome_distribution_usd_bn']['median']:,.0f}bn. Probability of crossing US$1 "
     f"trillion: {sim['probabilities']['P(AUM > $1,000bn by 2035)']*100:.0f}%. But also: a "
     f"{sim['drawdown']['P(peak-to-trough drawdown worse than 20%)']*100:.0f}% chance of a peak-to-trough fall worse "
     "than 20% somewhere along the way. That second number is the one that matters for planning, and it is the "
     "number a single-point forecast can never give you.", BODY))
    F.append(Paragraph("6d. Machine learning - tagging deal announcements automatically", H2))
    F.append(Paragraph(
     "Mubadala publishes hundreds of free-text announcements. Tagging each to a sector by hand is slow and "
     "inconsistent. I trained a model to read a headline and predict the sector.", BODY))
    F.append(callout("Jargon box: TF-IDF and logistic regression.",
     "<b>TF-IDF</b> turns text into numbers by counting words, then down-weighting words that appear everywhere. "
     "'The' appears in every headline so it carries no information; 'offshore wind' appears rarely so it carries a "
     "lot. <b>Logistic regression</b> then learns a weight for each word per sector, and picks whichever sector "
     "scores highest. It is one of the simplest classifiers there is - which is exactly why it is a good choice "
     "when you want to be able to explain what the model learned.", "note"))
    F.append(Paragraph("What went wrong, and this failure is the best thing in the project", H2))
    F.append(Paragraph(
     "My first attempt used about fifty hand-written example sentences. Cross-validated accuracy came out at "
     "<b>6%</b> - far worse than random guessing across six classes. It would have been easy to quietly delete "
     "that and try something else. Instead I diagnosed it: every one of my examples used almost entirely different "
     "words, so a word-counting model had no shared vocabulary to generalise from. It had memorised fifty sentences "
     "and learned nothing.", BODY))
    F.append(Paragraph(
     "The fix was to generate 1,080 training examples by sampling from sector vocabulary pools built out of real "
     "Mubadala announcement language. Accuracy on that synthetic data went to 100% - which is meaningless on its "
     f"own, so the real test is twelve genuine Mubadala headlines the model had never seen. It got "
     f"{clf['holdout_real_headlines']['accuracy']*100:.0f}% right.", BODY))
    F.append(callout("The one it got wrong is the most interesting result of all.",
     "It tagged 'Mubadala agrees to sell minority stake in CoolIT data centre liquid cooling to Ecolab' as "
     "<i>Industrials</i> rather than <i>Technology</i>. And honestly - it has a point. CoolIT makes physical cooling "
     "hardware for AI data centres. It is genuinely both.<br/><br/>"
     "The lesson is not 'the model needs more data'. It is that <b>a single-label data model is the wrong shape</b> "
     "for a portfolio whose most interesting assets sit between sectors. The fix is multi-label tagging, which is a "
     "data-design decision rather than a modelling one. Being able to say that is worth far more than a higher "
     "accuracy score.", "warn"))
    F.append(prosecons(
     ["Tag every deal by hand","Keyword rules (if it says 'wind' then Energy)","Train a classifier"],
     ["Perfectly accurate if you are careful. Zero setup.",
      "Transparent and instantly debuggable. No training data needed.",
      "Scales to thousands of items. Learns combinations you would not think to write down. Gives a confidence score."],
     ["Does not scale. Two analysts will disagree. Nobody re-does it when the taxonomy changes.",
      "Brittle - breaks on wording you did not anticipate. The rule list grows unmanageable.",
      "Needs training data. Can fail confidently. Must be tested on genuinely unseen examples or you fool yourself."],
     "A classifier, but reported honestly: the number I quote is the hold-out score on real unseen headlines, not "
     "the flattering 100% on synthetic training data."))

    # ---------------- STEP 7 ----------------
    F.append(PageBreak())
    F.append(step_header("7","Building the dashboard",
                         "And what to do when the industry-standard tool will not run on your laptop"))
    F.append(Paragraph("The problem", H2))
    F.append(Paragraph(
     "The brief asked for Power BI dashboards. Power BI Desktop is Windows-only - there is no Mac version and "
     "Microsoft has said there will not be one. I am on a Mac. There were four honest options.", BODY))
    F.append(prosecons(
     ["Run Windows in a VM","Use Power BI in the browser","Build in a different tool","Build the model + a browser dashboard"],
     ["The genuine article. Full feature set. Can say 'I built it in Power BI' without qualification.",
      "Free with a Fabric trial. No VM needed. Real Power BI files.",
      "Tableau Public is free and Mac-native and equally respected.",
      "Works everywhere with no software at all. The recruiter opens it by double-clicking. Full control of design."],
     ["Needs a Windows licence and 8GB+ of RAM. Slow. Genuinely painful on Apple Silicon.",
      "Missing key modelling features. Needs a work or student email; personal Gmail is often rejected.",
      "Does not literally satisfy a brief that says 'Power BI'.",
      "Not Power BI, so you must be able to explain the substitution convincingly."],
     "The fourth, plus a full Power BI build guide. I built the star schema, wrote every DAX measure, and shipped "
     "a self-contained HTML dashboard as the Mac-native twin. The 290-line guide in the repository rebuilds the "
     "identical report in Power BI in under an hour on any Windows machine."))
    F.append(callout("How to answer 'so did you actually build it in Power BI?'",
     "Do not be defensive, and do not fudge it. Say: <i>\"I built the data model and wrote the DAX measures. I "
     "shipped a browser dashboard because I work on a Mac and Power BI Desktop is Windows-only. The build guide in "
     "the repo rebuilds the identical report in Power BI in under an hour - here's the DAX for the concentration "
     "measure.\"</i> That answer demonstrates the skill, explains the constraint, and shows you solved a problem "
     "instead of being stopped by it. That is a better answer than a plain yes.", "find"))
    F.append(Paragraph("What is in the dashboard", H2))
    F+= bullets([
     "<b>Six tabs</b>: overview, portfolio composition, investment trends, valuation case studies, quant and AI, and method and sources.",
     "<b>Live filters</b> on sector, region and platform that update every chart at once.",
     "<b>A sortable deal table</b> - click any column header.",
     "<b>Every chart drawn as inline SVG by hand-written JavaScript</b>, with no external libraries. The file works "
     "with the wifi turned off, which matters if someone opens it on a train.",
     "<b>Evidence grades shown next to every holding</b>, so a reader can see which facts are company-stated.",
    ])
    F.append(Paragraph("What I wrote for Power BI even though I could not run it", H2))
    F.append(Paragraph(
     "Twenty-five DAX measures, the full relationship map, page-by-page visual specifications, a theme colour list, "
     "and a troubleshooting table of the six mistakes beginners actually make - starting with the most common one, "
     "which is a numeric column silently importing as text and every card going blank.", BODY))

    # ---------------- STEP 8 ----------------
    F.append(PageBreak())
    F.append(step_header("8","Writing it up",
                         "The part most people rush, and the only part most people read"))
    F.append(Paragraph(
     "Three documents, because three different readers exist and they want completely different things.", BODY))
    F.append(table([
     ["Document","Who it is for","What it has to do"],
     ["Equity Research Report\n(20 pages)","A finance professional, a recruiter, an interviewer",
      "Lead with findings. Show the evidence. State the limitations before anyone else spots them. Look like something a real desk produced."],
     ["This booklet","You, in six months when you have forgotten how it works. Also anyone learning.",
      "Explain everything from zero. Justify every choice with alternatives. Be honest about the failures."],
     ["Project Notes","An assessor checking the work is genuinely yours",
      "Prove progress step by step. Log every file made, every problem hit, every fix."],
    ],[36*mm,44*mm,None]))
    F.append(Paragraph("Three writing rules I stuck to", H2))
    F+= numbered([
     "<b>Lead with the finding, not the method.</b> 'OMV's dividend cover has fallen from 6.0x to 1.3x' comes "
     "first; how I calculated it comes second. Readers decide whether to keep reading in the first sentence.",
     "<b>Put the limitations in, prominently.</b> A whole section says what the report cannot tell you. This feels "
     "like weakening your own work. It does the opposite - anyone experienced already knows the limitations exist, "
     "and listing them yourself proves you know too. Omitting them is what looks naive.",
     "<b>Never write a number without being able to say where it came from.</b> Every figure in the report traces "
     "to one of ten sources listed at the back with URLs and dates.",
    ])
    F.append(callout("The section that will get you the most credit.",
     "Section 10.3 of the research report, headed 'Limitations - what this report cannot tell you'. It says the "
     "holdings dataset is a sample not the whole portfolio, that deal totals are floors not totals, that the "
     "capital-market assumptions are mine, and that two of the four case studies value private companies and are "
     "frameworks rather than valuations. Every experienced reader will look for exactly these caveats. Finding them "
     "already written is the strongest possible signal that the rest of the work is trustworthy.", "find"))

    # ---------------- STEP 9 ----------------
    F.append(PageBreak())
    F.append(step_header("9","Checking the work",
                         "How I tried to catch my own mistakes"))
    F.append(table([
     ["Check","What it caught"],
     ["Rebuilt every model in Excel and recalculated it, then compared to Python",
      "A real methodology difference in the Mubadala Capital valuation - $1.42bn vs $1.73bn. Excel was right."],
     ["Ran PRAGMA foreign_key_check on the database",
      "Nothing, which is the point - it proved every sector, geography and platform ID in the fact tables actually exists."],
     ["Tested the classifier on unseen real headlines rather than its own training data",
      "That the flattering 100% training accuracy was meaningless. Real score is 92%."],
     ["Re-counted the deals with disclosed values by hand against the database",
      "The dashboard said 'thirteen of nineteen have no value'. The true figure was ten. Fixed."],
     ["Checked WACC against an independent published estimate",
      "My 12.55% for GFS against a vendor's 13.25% - close enough to trust, far enough apart to mention."],
     ["Sense-checked derived numbers against reality",
      "WHOOP revenue per member came out at $440/year, which is plausible for a subscription plus hardware. An earlier version said $440,000 - a units error, caught and fixed."],
     ["Rendered every chart and PDF page and looked at it",
      "Overlapping text labels on the football-field charts and a gold divider line cutting through the cover metadata."],
    ],[62*mm,None]))
    F.append(callout("Why the boring checks matter most.",
     "Every one of those errors was invisible in the output. The valuation of $1.73bn looked exactly as convincing "
     "as the correct $1.42bn. $440,000 per member looked like a number until you thought about it for two seconds. "
     "Nothing about a wrong answer announces itself - which is why the checking has to be systematic rather than "
     "instinctive.", "warn"))

    # ---------------- CLOSING ----------------
    F.append(PageBreak())
    F.append(Paragraph("If you had to redo this in one weekend", H1))
    F.append(Paragraph(
     "The full project took a long time. If you wanted 80% of the value in about sixteen hours, this is the order "
     "I would do it in - and notice that the writing gets a whole day, because that is the part that gets read.", BODY))
    F.append(table([
     ["Hours","Do this","Skip this"],
     ["0-2","Pick a fund. Read its latest annual report. Write down five questions.","Reading twenty articles about it"],
     ["2-5","Build the star schema in CSVs. Load into SQLite. Write six SQL queries.","Sixteen tables - eight is plenty"],
     ["5-9","One full DCF on one listed holding, in Excel with live formulas.","Four case studies - one done properly beats four rushed"],
     ["9-11","Add a reverse DCF. It is twenty lines and it is the best thing you will show.","A second full DCF"],
     ["11-13","One chart per question. Five or six charts total.","Fourteen charts"],
     ["13-16","Write the report. Findings first, limitations section included.","A dashboard, if time is short"],
    ],[18*mm,None,52*mm]))
    F.append(Paragraph("The five things worth remembering", H1))
    F+= numbered([
     "<b>Start with questions, not a topic.</b> It tells you what to build and when to stop.",
     "<b>Go to the primary source and cite it with a date.</b> A number a stranger can verify is worth ten they cannot.",
     "<b>Run your models backwards.</b> 'What does this price assume?' beats 'what is this worth?' almost every time, "
     "and it works on private companies where a forward model cannot.",
     "<b>Build important things twice in two tools.</b> The disagreements are your bugs. It found a real one here.",
     "<b>Write down what went wrong.</b> The 6% classifier and the CoolIT misclassification are more interesting to "
     "an interviewer than any number in the report, because they show how you think when something breaks.",
    ])
    F.append(callout("One last thing.",
     "You do not need to have built all of this to talk about all of this. What you need is to genuinely understand "
     "the reasoning in this booklet - why a star schema, why exclude Tower Semiconductor, why the raw beta was "
     "rejected, why the classifier's mistake was informative. Someone who can explain the <i>choices</i> will always "
     "interview better than someone who can only describe the <i>output</i>. Learn the reasons, and the project "
     "becomes genuinely yours.", "find"))
    F.append(Spacer(1,10))
    F.append(Paragraph(
     "<i>Companion documents: Equity_Research_Report.pdf (the findings) and "
     "Project_Notes_Evidence_Log.pdf (the step-by-step record of what was built and when).</i>", SMALL))
    return F
