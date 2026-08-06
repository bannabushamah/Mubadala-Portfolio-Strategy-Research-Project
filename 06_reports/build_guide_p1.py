# -*- coding: utf-8 -*-
"""Beginner guide booklet - part 1 of the flowable list (steps 0-4)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pdf_style import *

ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH=os.path.join(ROOT,"07_charts"); C=lambda n: os.path.join(CH,n+".png")

def step_header(n, title, oneline):
    return KeepTogether([
     Spacer(1,6),
     Table([[Paragraph(f'<font color="#FFFFFF" size="15"><b>{n}</b></font>',
              S("sn", fontName="Helvetica-Bold", fontSize=15, alignment=TA_CENTER, textColor=colors.white)),
             Paragraph(f'<font color="#0B2545" size="14"><b>{title}</b></font><br/>'
                       f'<font color="#5A6B7B" size="9">{oneline}</font>',
              S("sh", fontName="Helvetica", fontSize=13, leading=17))]],
           colWidths=[13*mm, None],
           style=TableStyle([("BACKGROUND",(0,0),(0,0),GOLD),
             ("BACKGROUND",(1,0),(1,0),colors.HexColor("#F4F6F9")),
             ("VALIGN",(0,0),(-1,-1),"MIDDLE"),("LEFTPADDING",(1,0),(1,0),9),
             ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7)])),
     Spacer(1,7)])

def prosecons(title, pros, cons, chosen):
    rows=[[Paragraph("<b>Option</b>",CELLH),Paragraph("<b>Good things about it</b>",CELLH),
           Paragraph("<b>Bad things about it</b>",CELLH)]]
    for name,p,c in zip(title,pros,cons):
        rows.append([Paragraph(f"<b>{name}</b>",CELLB),Paragraph(p,CELL),Paragraph(c,CELL)])
    t=table(rows,[34*mm,None,58*mm])
    return KeepTogether([t, callout("What I picked and why.", chosen, "find")])

def build():
    F=[]
    F+= cover("How I Built This Project",
        "Every single step explained in plain English - what I did, why I did it, "
        "and what else I could have done instead",
        [("Author","bann"),
         ("Document","Beginner's guide booklet"),
         ("Companion to","Equity Research Report and Project Notes"),
         ("Written for","Someone who has never built a financial model,"),
         ("","written a line of SQL, or opened Power BI"),
         ("Promise","No step is skipped and no jargon is used without"),
         ("","being explained the first time it appears")],
        kicker="PLAIN-ENGLISH GUIDE")

    # ---------------- HOW TO USE ----------------
    F.append(Paragraph("How to use this booklet", H1))
    F.append(Paragraph(
     "This is the instruction manual for the whole project. If you wanted to rebuild everything from scratch, "
     "you could do it by following this document from top to bottom. Nothing is assumed. Every technical word "
     "gets explained the first time it turns up, in a shaded box like this one.", LEAD))
    F.append(callout("Jargon box: what is a 'sovereign wealth fund'?",
     "A country's savings account, run like an investment firm. Instead of one family investing its money, it is "
     "an entire government. Mubadala is Abu Dhabi's. It takes money the country earned (historically from oil) and "
     "buys businesses, buildings and shares all over the world, so that future generations still have income when "
     "the oil runs out. That single sentence explains almost everything unusual about how it invests.", "note"))
    F.append(Paragraph("Each of the nine steps below follows the same shape:", BODY))
    F+= bullets([
     "<b>What I did</b> - the actual actions, in order.",
     "<b>Why I did it that way</b> - the reasoning.",
     "<b>What else I could have done</b> - a table of the realistic alternatives, with honest pros and cons.",
     "<b>What went wrong</b> - because something did, in almost every step, and the fixes are the part worth reading.",
     "<b>What to say in an interview</b> - the one or two sentences that turn the work into something a recruiter can grade.",
    ])
    F.append(callout("The most important idea in this whole booklet.",
     "A finance project is not impressive because the numbers are big. It is impressive because a stranger can "
     "check every number you wrote down. Almost every choice in this project was made in favour of being checkable "
     "rather than being impressive. Recruiters can tell the difference immediately, and it is the difference between "
     "a project that gets you an interview and one that gets you caught out in it.", "warn"))

    # ---------------- STEP 0 ----------------
    F.append(PageBreak())
    F.append(step_header("0","Deciding what the project actually is",
                         "Before touching data, decide what question you are answering"))
    F.append(Paragraph("What I did", H2))
    F.append(Paragraph(
     "The project brief was three lines long: research Mubadala's portfolio strategy and sector allocation, build "
     "valuation case studies in four sectors, and build dashboards and datasets. That is a topic, not a question. "
     "So the first thing I did was write down five questions the finished project would answer:", BODY))
    F+= numbered([
     "Is Mubadala's portfolio concentrated or spread out, and does it matter?",
     "Is the fund growing because it is being given money, or because it is making money?",
     "Is the mix of assets it holds actually a sensible mix?",
     "How important is technology to the overall strategy, really?",
     "Are the individual companies it owns cheap, expensive, or about right?",
    ])
    F.append(Paragraph("Why I did it that way", H2))
    F.append(Paragraph(
     "A project organised around questions has a natural ending: you stop when the questions are answered. A "
     "project organised around a topic never ends, because there is always one more chart you could make. It also "
     "changes what you build. If question three is 'is the mix sensible', you now <i>need</i> a portfolio "
     "optimiser, and you know exactly what it is for. Without the question, the optimiser is just a thing you "
     "added because it looked clever - and an interviewer will find that out in about thirty seconds by asking "
     "'why did you do that?'", BODY))
    F.append(prosecons(
     ["Start with a topic","Start with questions","Start with the tools"],
     ["Easy to begin. You can start reading immediately without deciding anything.",
      "Every piece of work has an obvious purpose. The project has a clear end point. Findings write themselves.",
      "You get to practise the software straight away, which feels productive."],
     ["No natural end. Easy to produce a lot of material that proves nothing. Very hard to write a conclusion.",
      "Slower to start. You may have to change the questions once you see what data actually exists.",
      "You end up with a dashboard that shows things nobody asked about. Classic beginner trap - lots of charts, no argument."],
     "Questions. It cost me about an hour up front and saved days later, because every time I was unsure "
     "whether to build something, I asked 'which of my five questions does this answer?' If the answer was "
     "'none', I did not build it."))
    F.append(callout("Interview line.",
     "\"I framed it as five questions rather than a topic, so every component in the repository exists to answer "
     "one of them. That is also why there is no chart in the project that I can't explain the purpose of.\"", "find"))

    # ---------------- STEP 1 ----------------
    F.append(PageBreak())
    F.append(step_header("1","Finding real information",
                         "Going to the source instead of trusting a summary"))
    F.append(Paragraph("What I did", H2))
    F.append(Paragraph(
     "I went to Mubadala's own website and read the primary documents rather than news articles about them:", BODY))
    F+= bullets([
     "The <b>2025 annual results press release</b>, published 9 April 2026 - this is where the headline numbers live.",
     "The <b>2025 Annual Review</b> microsite, especially the Performance Overview page, which has the asset-class breakdown.",
     "The <b>Our Structure</b> page, which describes the four investment platforms and names the people who run them.",
     "The <b>newsroom</b>, which lists every deal announcement - this became the transaction dataset.",
     "For the listed companies, <b>StockAnalysis.com</b>, which republishes S&amp;P Global Market Intelligence data.",
    ])
    F.append(Paragraph("Here are the numbers that came out of that, and they are the spine of everything else:", BODY))
    F.append(table([
     ["Number","Value","Where it came from"],
     ["Assets under management","AED1.414 trillion (US$385bn)","Mubadala press release, 9 Apr 2026"],
     ["Growth in the year","+17%","Same"],
     ["5-year annualised return","10.7%","Same"],
     ["10-year annualised return","10.3%","Same"],
     ["Money invested in 2025","US$39bn (AED143bn)","Same"],
     ["Money received back in 2025","US$38bn (AED138bn)","Same"],
     ["Asset mix","Private 42%, Public 20%, Real estate &amp; infra 17%, Alternatives 16%, Credit 5%","2025 Annual Review"],
    ],[38*mm,52*mm,None]))
    F.append(callout("Jargon box: AED and the peg.",
     "AED is the UAE dirham. It is <i>pegged</i> to the US dollar at a fixed rate of 3.6725 dirhams per dollar, and "
     "has been since 1997. A peg means the exchange rate does not float around - the central bank commits to holding "
     "it. That is why you can convert every dirham figure in this project to dollars with a single constant and not "
     "worry about which day you did it.", "note"))
    F.append(Paragraph("Why I did it that way", H2))
    F.append(Paragraph(
     "Two reasons. First, accuracy: every time a number passes through a journalist it can be rounded, mistranslated "
     "or given without context. Second, and more useful for you: <b>a recruiter can click your source</b>. If your "
     "footnote says 'Mubadala press release, 9 April 2026' they can verify it in ten seconds. If it says 'various "
     "media reports' they cannot, and they will assume the worst.", BODY))
    F.append(prosecons(
     ["Company primary sources","News articles","A paid database (Bloomberg, PitchBook)"],
     ["Free. Authoritative. Precisely dated. The company is legally careful about what it publishes.",
      "Fast. Often adds useful context and quotes that the company itself would not give.",
      "Complete, structured, includes private-company estimates. What the industry actually uses."],
     ["Selective - a company publishes what flatters it. No position-level portfolio is ever disclosed.",
      "Errors propagate. Numbers get rounded and lose their as-of date. Often no link back to the original.",
      "Extremely expensive. Licences forbid republishing, so you often cannot show your workings anyway."],
     "Primary sources for anything about Mubadala, and StockAnalysis (which republishes S&amp;P Global data) for "
     "share prices and multiples. This combination is free, citable and reproducible, which matters more for a "
     "portfolio project than completeness does."))
    F.append(Paragraph("What went wrong", H2))
    F.append(Paragraph(
     "The Annual Review's geography breakdown is drawn by JavaScript in the browser. When I fetched the page I got "
     "the labels - North America, Europe, UAE, Asia-Pacific - but every percentage came back as '0%'. Rather than "
     "guess the numbers or quietly drop the analysis, I built my own geographic picture from the twenty named "
     "holdings and <b>labelled it as my dataset, not Mubadala's disclosure</b>. The report says so explicitly.", BODY))
    F.append(callout("This is the single most transferable lesson in the booklet.",
     "When you cannot get a number, you have three options: guess it, hide the gap, or say so and work around it. "
     "The first two are how people get found out. The third is how you build a reputation. Every analyst hits "
     "missing data constantly - the job is not to have perfect data, it is to be honest about which data you have.", "warn"))

    # ---------------- STEP 2 ----------------
    F.append(PageBreak())
    F.append(step_header("2","Organising the information into a database",
                         "Turning scattered facts into something a computer can slice"))
    F.append(Paragraph("What I did", H2))
    F.append(Paragraph(
     "I built sixteen tables and loaded them into a SQLite database. The tables come in two types, and this "
     "split is called a <b>star schema</b>.", BODY))
    F.append(callout("Jargon box: star schema, dimension, fact.",
     "Imagine a school. A <b>dimension</b> table is a list of things that barely change: the pupils, the subjects, "
     "the teachers. A <b>fact</b> table is a list of things that happen: 'pupil 14 scored 78% in subject 3 on "
     "12 March'. The fact table only stores ID numbers, and you look up the names in the dimension tables. Drawn "
     "out, the facts sit in the middle and the dimensions radiate outward like the points of a star - hence the "
     "name. It is the standard way to build data for reporting tools.", "note"))
    F.append(table([
     ["Dimension tables (the 'nouns')","Fact tables (the 'events and measurements')"],
     ["dim_sector - the 12 sectors\n"
      "dim_geography - 12 countries and their regions\n"
      "dim_platform - Mubadala's 4 investment platforms\n"
      "dim_asset_class - the 5 asset classes\n"
      "dim_source - every source I used, with its URL and date",
      "fact_performance - AUM, returns, deployments\n"
      "fact_capital_flow - money in and out by year\n"
      "fact_holding - 20 named holdings\n"
      "fact_transaction - 19 announced deals\n"
      "fact_market_data - 20 listed companies' prices and multiples\n"
      "fact_gfs_financials / fact_omv_financials - company accounts\n"
      "fact_whoop_metrics - WHOOP's disclosed numbers"],
    ],[None,None]))
    F.append(Paragraph("Why I did it that way", H2))
    F.append(Paragraph(
     "The obvious alternative is one big spreadsheet with every column in it. That works until you want to ask a "
     "question. Suppose you type 'United States' in one row and 'USA' in another - now a filter on country misses "
     "half your data, silently. In a star schema the country lives in exactly one place and every other table "
     "points at it by ID, so that mistake becomes impossible.", BODY))
    F.append(Paragraph(
     "There is also a practical reason specific to this project: Power BI, Tableau and every other reporting tool "
     "are <i>built</i> for star schemas. One sector filter can control the holdings chart, the deals chart and the "
     "market-data chart at the same time, because all three point at the same dimension table. With one flat table "
     "you would need three separate filters and they would drift out of step.", BODY))
    F.append(prosecons(
     ["One big spreadsheet","Star schema","Fully normalised (3NF)"],
     ["Anyone can open it. Zero learning curve. Fine for under a few hundred rows.",
      "Filters behave predictably. Reporting tools are designed for it. No duplicated text.",
      "Mathematically the tidiest. Zero redundancy anywhere. What transactional databases use."],
     ["Typos create invisible errors. Text repeats on every row. Slicers become ambiguous. Does not scale.",
      "You have to learn about joins and keys. Slightly more set-up work at the start.",
      "Queries need many joins and become hard to read. Reporting tools run slower on it. Overkill here."],
     "Star schema. It is the industry standard for analytics precisely because it sits between the two extremes: "
     "tidy enough to prevent errors, simple enough that a query stays readable."))
    F.append(Paragraph("The one extra column that makes this project different", H2))
    F.append(Paragraph(
     "Every fact table has a <b>source_id</b> column and most have an <b>evidence_grade</b>. Grades are: "
     "<i>Official</i> (Mubadala said it), <i>Market data</i> (an exchange or data vendor said it), "
     "<i>Press reporting</i> (widely reported but not confirmed), and <i>Analyst estimate</i> (I made it up, "
     "with stated reasoning). Sixteen of the twenty holdings are Official and four are Press reporting, and the "
     "dashboard shows the grade next to every row.", BODY))
    F.append(callout("Why this is worth doing even though nobody asked for it.",
     "It means that when someone challenges a number, you do not have to remember where it came from - you can "
     "run one query and show them. It also forces honesty on yourself while you work, because writing "
     "'Analyst estimate' next to a figure makes it much harder to quietly treat a guess as a fact later on.", "find"))
    F.append(Paragraph("What went wrong", H2))
    F.append(Paragraph(
     "SQLite refused to create the database file, returning 'disk I/O error'. The cause was that the folder I was "
     "working in is a network-style mount that does not support the file locking SQLite needs. The fix was three "
     "lines: build the database on local disk, then copy the finished file into the project folder. The code still "
     "carries a comment explaining why, because otherwise the next person to read it would 'fix' it back.", BODY))

    # ---------------- STEP 3 ----------------
    F.append(PageBreak())
    F.append(step_header("3","Asking the database questions with SQL",
                         "Twelve queries that turn stored data into findings"))
    F.append(callout("Jargon box: SQL.",
     "SQL (say it 'sequel' or 'ess-cue-ell', both are accepted) stands for Structured Query Language. It is how "
     "you ask a database for things. It reads almost like English: SELECT the columns you want, FROM the table, "
     "WHERE some condition is true. That is 80% of it.", "note"))
    F.append(Paragraph("What I did", H2))
    F.append(Paragraph(
     "I wrote twelve queries, each deliberately using a different technique so the file demonstrates range as well "
     "as answering the questions.", BODY))
    F.append(table([
     ["Query","What it answers","Technique it shows off"],
     ["Q2","How concentrated is the asset mix?","Window function with a running total"],
     ["Q3","Is growth self-funded?","LAG() to compare a row to the previous year"],
     ["Q4","Which sectors dominate?","GROUP BY with a percent-of-total subquery"],
     ["Q6","Which platform invests in what?","Conditional aggregation (a pivot without PIVOT)"],
     ["Q7","How has deal flow moved?","CTE plus date extraction and honest NULL handling"],
     ["Q8","Herfindahl concentration index","Mathematical aggregate with CASE interpretation"],
     ["Q9","How do peers compare on multiples?","PARTITION BY and NTILE for quartiles"],
     ["Q10","How is GlobalFoundries' mix shifting?","Self-join of a CTE to compare two years"],
     ["Q11","Is OMV's dividend safe?","Derived ratio with a CASE-based verdict"],
     ["Q12","How much of my own data is officially sourced?","UNION ALL audit across tables"],
    ],[16*mm,None,60*mm]))
    F.append(Paragraph("Two findings that came straight out of these queries", H2))
    F.append(Paragraph(
     "<b>Q8 - the concentration index.</b> The Herfindahl-Hirschman index adds up the squares of the percentage "
     "weights. Five equal buckets of 20% would give 5 x 400 = 2,000. Mubadala's actual mix gives 2,734. Anything "
     "above 2,500 is officially 'concentrated'. Flip the number over and you get an 'effective number of buckets' "
     "of 3.7 - so despite reporting five asset classes, the portfolio behaves like about three and a half.", BODY))
    F.append(Paragraph(
     "<b>Q11 - the dividend cover.</b> Dividing OMV's free cash flow by the cost of its dividend gives 6.0x in "
     "2021, then 5.3x, 2.3x, 2.0x and 1.3x in 2025. That is a company raising its dividend every year while the "
     "cash behind it shrinks. This was the single most useful finding in the whole project and it came from four "
     "lines of arithmetic in a SQL query.", BODY))
    F.append(callout("Interview line.",
     "\"The most valuable thing in my SQL file is four lines long. I divided OMV's free cash flow by its dividend "
     "cost across five years and the cover ratio had fallen from six times to one point three, while the dividend "
     "per share went up every single year. Nothing clever - just asking the obvious question of the data.\"", "find"))
    F.append(prosecons(
     ["Do it all in Excel","Do it in SQL","Do it in Python pandas"],
     ["Visual, instant feedback, everyone can open the file.",
      "The logic is written down and re-runnable. Handles joins naturally. Universally expected in finance data roles.",
      "Most flexible. Same language as the models and the machine learning."],
     ["Formulas hide in cells. Impossible to review. One dragged formula corrupts everything silently.",
      "You must learn it, and debugging a long query is genuinely annoying at first.",
      "Reviewers cannot check it without running it. Fewer finance interviewers read Python than read SQL."],
     "SQL for anything that is a question about the dataset, Python for anything that is a calculation. That "
     "split also happens to be how most real analytics teams work."))
    return F
