"""
build_dashboard.py
Generates Mubadala_Portfolio_Dashboard.html - a single self-contained file with
no external dependencies (no CDN, no internet needed). All charts are drawn as
inline SVG by vanilla JavaScript so the file works from a USB stick, an email
attachment, or a recruiter's laptop with the wifi off.

This is the Mac-friendly twin of the Power BI report described in
PowerBI_Build_Guide.md - identical data model, identical measures.
"""
import os, json, pandas as pd

HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(HERE)
WH=os.path.join(ROOT,"01_data","warehouse")
VAL=os.path.join(ROOT,"03_valuation_models","outputs")
AI=os.path.join(ROOT,"04_ai_ml","outputs")

R=lambda t: pd.read_csv(os.path.join(WH,t+".csv"))
J=lambda p: json.load(open(p))

hold=R("fact_holding"); txn=R("fact_transaction"); sec=R("dim_sector")
geo=R("dim_geography"); plat=R("dim_platform"); alloc=R("fact_asset_allocation")
flow=R("fact_capital_flow"); perf=R("fact_performance"); mkt=R("fact_market_data")

hold=hold.merge(sec[["sector_id","sector_name","ai_exposure"]],on="sector_id")\
         .merge(geo[["geo_id","country","region"]],on="geo_id")\
         .merge(plat[["platform_id","platform_name"]],on="platform_id")
txn=txn.merge(sec[["sector_id","sector_name"]],on="sector_id")\
       .merge(geo[["geo_id","country","region"]],on="geo_id")\
       .merge(plat[["platform_id","platform_name"]],on="platform_id")
txn["year"]=txn["announce_date"].str[:4]

DATA={
 "holdings":hold[["holding_name","sector_name","ai_exposure","country","region",
                  "platform_name","ownership","listing_status","ticker",
                  "investment_thesis","evidence_grade"]].to_dict("records"),
 "transactions":txn[["announce_date","year","target","deal_type","sector_name","country",
                     "region","platform_name","value_usd_m","disclosure_note"]]
                 .fillna("").to_dict("records"),
 "allocation":alloc[["asset_class","weight_pct","implied_usd_bn"]].to_dict("records"),
 "flows":flow[["year","deployments_usd_bn","proceeds_usd_bn"]].to_dict("records"),
 "kpi":{r["metric"]:r["value"] for _,r in perf[perf.year==2025].iterrows()},
 "market":mkt[["ticker","company","sector_id","mkt_cap_bn","pe_ttm","revenue_ttm_bn"]]
            .fillna(0).to_dict("records"),
 "cases":{
   "gfs":J(os.path.join(VAL,"case_01_globalfoundries.json")),
   "omv":J(os.path.join(VAL,"case_02_omv.json")),
   "whoop":J(os.path.join(VAL,"case_03_whoop.json")),
   "mcap":J(os.path.join(VAL,"case_04_mubadala_capital.json"))},
 "optimiser":J(os.path.join(AI,"portfolio_optimisation.json")),
 "montecarlo":J(os.path.join(AI,"monte_carlo.json")),
 "classifier":J(os.path.join(AI,"deal_classifier.json")),
}

HTML = r"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Mubadala Portfolio Strategy Dashboard</title>
<style>
:root{--navy:#0B2545;--navy2:#13315C;--gold:#C9A227;--teal:#1B7F79;--slate:#5A6B7B;
--rust:#A6432F;--bg:#F4F6F9;--card:#FFFFFF;--line:#E2E7ED;--ink:#122B45;}
*{box-sizing:border-box;margin:0;padding:0}
body{font:14px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
background:var(--bg);color:var(--ink);-webkit-font-smoothing:antialiased}
header{background:linear-gradient(135deg,var(--navy),var(--navy2));color:#fff;padding:26px 30px 22px}
header h1{font-size:22px;font-weight:700;letter-spacing:-.3px}
header p{opacity:.78;font-size:13px;margin-top:5px}
.badge{display:inline-block;background:rgba(201,162,39,.2);color:var(--gold);border:1px solid rgba(201,162,39,.4);
padding:3px 9px;border-radius:20px;font-size:11px;font-weight:600;margin-top:10px;margin-right:6px}
nav{background:var(--card);border-bottom:1px solid var(--line);padding:0 30px;display:flex;gap:2px;
overflow-x:auto;position:sticky;top:0;z-index:20}
nav button{background:none;border:none;padding:14px 16px;font-size:13px;font-weight:600;color:var(--slate);
cursor:pointer;border-bottom:3px solid transparent;white-space:nowrap;font-family:inherit}
nav button:hover{color:var(--navy)}
nav button.active{color:var(--navy);border-bottom-color:var(--gold)}
main{padding:24px 30px 60px;max-width:1500px;margin:0 auto}
.tab{display:none}.tab.active{display:block}
.grid{display:grid;gap:16px}
.k4{grid-template-columns:repeat(auto-fit,minmax(200px,1fr))}
.c2{grid-template-columns:repeat(auto-fit,minmax(420px,1fr))}
.c3{grid-template-columns:repeat(auto-fit,minmax(300px,1fr))}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:18px 20px;
box-shadow:0 1px 2px rgba(11,37,69,.04)}
.card h3{font-size:13px;font-weight:700;color:var(--navy);margin-bottom:3px}
.card .sub{font-size:11.5px;color:var(--slate);margin-bottom:14px}
.kpi .label{font-size:11px;text-transform:uppercase;letter-spacing:.7px;color:var(--slate);font-weight:600}
.kpi .value{font-size:28px;font-weight:700;color:var(--navy);margin:6px 0 2px;letter-spacing:-.5px}
.kpi .note{font-size:11.5px;color:var(--teal);font-weight:600}
.filters{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-bottom:16px;
background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 16px}
.filters label{font-size:11px;font-weight:700;color:var(--slate);text-transform:uppercase;letter-spacing:.5px}
select{font:13px inherit;padding:6px 10px;border:1px solid var(--line);border-radius:6px;
background:#fff;color:var(--ink);font-family:inherit}
table{width:100%;border-collapse:collapse;font-size:12.5px}
th{text-align:left;background:var(--navy);color:#fff;padding:9px 10px;font-weight:600;font-size:11px;
text-transform:uppercase;letter-spacing:.4px;cursor:pointer;user-select:none;white-space:nowrap}
th:hover{background:var(--navy2)}
td{padding:8px 10px;border-bottom:1px solid var(--line);vertical-align:top}
tbody tr:hover{background:#F8FAFC}
.num{text-align:right;font-variant-numeric:tabular-nums}
.pill{display:inline-block;padding:2px 8px;border-radius:12px;font-size:10.5px;font-weight:700}
.pill.hi{background:#FDF3D8;color:#8A6F10}.pill.md{background:#DFF0EE;color:#0F5A56}
.pill.lo{background:#EDF0F3;color:#5A6B7B}
.pill.off{background:#DFF0EE;color:#0F5A56}.pill.press{background:#FDF3D8;color:#8A6F10}
.scroll{max-height:520px;overflow:auto;border-radius:8px;border:1px solid var(--line)}
.scroll thead th{position:sticky;top:0;z-index:2}
.note{background:#FFF9E8;border-left:3px solid var(--gold);padding:11px 14px;border-radius:0 6px 6px 0;
font-size:12.5px;color:#5B4A10;margin-top:14px}
.finding{background:#EEF6F5;border-left:3px solid var(--teal);padding:11px 14px;border-radius:0 6px 6px 0;
font-size:12.5px;margin-top:14px}
.warn{background:#FBEFEC;border-left:3px solid var(--rust);padding:11px 14px;border-radius:0 6px 6px 0;
font-size:12.5px;margin-top:14px}
svg{display:block;width:100%;height:auto;overflow:visible}
.lgd{display:flex;gap:14px;flex-wrap:wrap;margin-top:10px;font-size:11.5px;color:var(--slate)}
.lgd i{width:11px;height:11px;border-radius:3px;display:inline-block;margin-right:5px;vertical-align:-1px}
footer{padding:20px 30px;font-size:11.5px;color:var(--slate);border-top:1px solid var(--line);background:var(--card)}
.tag{font-size:10.5px;color:var(--slate);font-weight:600}
</style></head><body>
<header>
 <h1>Mubadala Investment Company &mdash; Portfolio Strategy Dashboard</h1>
 <p>Sector allocation, global investment trends and valuation case studies across technology, healthcare, energy and financial services</p>
 <span class="badge">FY2025 results</span><span class="badge">Data frozen 4 Aug 2026</span><span class="badge">Every figure source-tagged</span>
</header>
<nav id="nav"></nav>
<main>
 <section class="tab active" id="t-overview"></section>
 <section class="tab" id="t-portfolio"></section>
 <section class="tab" id="t-deals"></section>
 <section class="tab" id="t-valuation"></section>
 <section class="tab" id="t-quant"></section>
 <section class="tab" id="t-method"></section>
</main>
<footer>
 Built by bann, August 2026. Sources: Mubadala 2025 Annual Review and press releases; StockAnalysis / S&amp;P Global Market Intelligence.
 Forward-looking assumptions are the author's own and are not investment advice.
</footer>
<script>
const DATA = __DATA__;
const C={navy:"#0B2545",gold:"#C9A227",teal:"#1B7F79",slate:"#5A6B7B",rust:"#A6432F",
         sand:"#E4D8B4",plum:"#7A5C9E",sky:"#3E7CB1"};
const PAL=[C.navy,C.gold,C.teal,C.slate,C.rust,C.sand,C.plum,C.sky];
const $=s=>document.querySelector(s);
const fmt=(n,d=0)=>n==null||isNaN(n)?"&ndash;":Number(n).toLocaleString("en-US",
   {minimumFractionDigits:d,maximumFractionDigits:d});
const esc=s=>String(s??"").replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));

/* ---------------- tiny SVG chart helpers (no libraries) ---------------- */
function svg(w,h,inner){return `<svg viewBox="0 0 ${w} ${h}" preserveAspectRatio="xMidYMid meet">${inner}</svg>`;}
function donut(rows,valKey,labKey,cx,cy,r,ir){
  const tot=rows.reduce((a,b)=>a+b[valKey],0); let a0=-Math.PI/2,out="";
  rows.forEach((row,i)=>{const frac=row[valKey]/tot,a1=a0+frac*2*Math.PI;
    const big=frac>0.5?1:0;
    const p=[`M ${cx+r*Math.cos(a0)} ${cy+r*Math.sin(a0)}`,
             `A ${r} ${r} 0 ${big} 1 ${cx+r*Math.cos(a1)} ${cy+r*Math.sin(a1)}`,
             `L ${cx+ir*Math.cos(a1)} ${cy+ir*Math.sin(a1)}`,
             `A ${ir} ${ir} 0 ${big} 0 ${cx+ir*Math.cos(a0)} ${cy+ir*Math.sin(a0)} Z`].join(" ");
    out+=`<path d="${p}" fill="${PAL[i%PAL.length]}" stroke="#fff" stroke-width="2"><title>${esc(row[labKey])}: ${row[valKey]}%</title></path>`;
    const am=(a0+a1)/2,rm=(r+ir)/2;
    out+=`<text x="${cx+rm*Math.cos(am)}" y="${cy+rm*Math.sin(am)+4}" text-anchor="middle" fill="#fff" font-size="12" font-weight="700">${row[valKey]}%</text>`;
    a0=a1;});
  return out;
}
function hbars(rows,labKey,valKey,w,rowH,opt={}){
  const max=Math.max(...rows.map(r=>r[valKey]))||1, lw=opt.labelWidth||190, pad=14;
  const bw=w-lw-90; let out="";
  rows.forEach((r,i)=>{const y=pad+i*rowH, len=Math.max(2,bw*r[valKey]/max);
    const col=opt.color?opt.color(r,i):PAL[i%PAL.length];
    out+=`<text x="${lw-8}" y="${y+rowH/2+4}" text-anchor="end" font-size="11.5" fill="${C.slate}">${esc(r[labKey])}</text>`;
    out+=`<rect x="${lw}" y="${y+3}" width="${len}" height="${rowH-10}" rx="3" fill="${col}"><title>${esc(r[labKey])}: ${r[valKey]}</title></rect>`;
    out+=`<text x="${lw+len+7}" y="${y+rowH/2+4}" font-size="11.5" font-weight="700" fill="${C.navy}">${opt.fmt?opt.fmt(r):fmt(r[valKey])}</text>`;});
  return svg(w,pad*2+rows.length*rowH,out);
}
function groupedBars(rows,catKey,series,w,h){
  const pad={l:52,r:14,t:14,b:34}, iw=w-pad.l-pad.r, ih=h-pad.t-pad.b;
  const max=Math.max(...rows.flatMap(r=>series.map(s=>r[s.key])))*1.18||1;
  const gw=iw/rows.length, bw=Math.min(34,(gw-16)/series.length);
  let out=`<line x1="${pad.l}" y1="${pad.t+ih}" x2="${pad.l+iw}" y2="${pad.t+ih}" stroke="${C.line||'#E2E7ED'}" stroke-width="1"/>`;
  for(let g=0;g<=4;g++){const v=max*g/4,y=pad.t+ih-ih*g/4;
    out+=`<line x1="${pad.l}" y1="${y}" x2="${pad.l+iw}" y2="${y}" stroke="#EDF0F3"/>`;
    out+=`<text x="${pad.l-8}" y="${y+4}" text-anchor="end" font-size="10.5" fill="${C.slate}">${fmt(v)}</text>`;}
  rows.forEach((r,i)=>{const x0=pad.l+i*gw+gw/2-(series.length*bw)/2;
    series.forEach((s,j)=>{const bh=ih*r[s.key]/max, x=x0+j*bw;
      out+=`<rect x="${x}" y="${pad.t+ih-bh}" width="${bw-3}" height="${bh}" rx="2.5" fill="${s.color}"><title>${esc(r[catKey])} ${s.name}: ${r[s.key]}</title></rect>`;
      out+=`<text x="${x+(bw-3)/2}" y="${pad.t+ih-bh-5}" text-anchor="middle" font-size="10" font-weight="700" fill="${C.navy}">${r[s.key]}</text>`;});
    out+=`<text x="${pad.l+i*gw+gw/2}" y="${h-11}" text-anchor="middle" font-size="11.5" fill="${C.slate}">${esc(r[catKey])}</text>`;});
  return svg(w,h,out);
}
function fanChart(years,med,lo,hi,w,h,threshold){
  const pad={l:56,r:16,t:16,b:30}, iw=w-pad.l-pad.r, ih=h-pad.t-pad.b;
  const ymax=Math.max(...hi)*1.05, ymin=0;
  const X=i=>pad.l+iw*i/(years.length-1), Y=v=>pad.t+ih-ih*(v-ymin)/(ymax-ymin);
  let out="";
  for(let g=0;g<=4;g++){const v=ymax*g/4,y=Y(v);
    out+=`<line x1="${pad.l}" y1="${y}" x2="${pad.l+iw}" y2="${y}" stroke="#EDF0F3"/>`;
    out+=`<text x="${pad.l-8}" y="${y+4}" text-anchor="end" font-size="10.5" fill="${C.slate}">${fmt(v)}</text>`;}
  const band=hi.map((v,i)=>`${X(i)},${Y(v)}`).join(" ")+" "+
             lo.map((v,i)=>`${X(lo.length-1-i)},${Y(lo[lo.length-1-i])}`).join(" ");
  out+=`<polygon points="${band}" fill="${C.gold}" opacity="0.22"/>`;
  out+=`<polyline points="${med.map((v,i)=>`${X(i)},${Y(v)}`).join(" ")}" fill="none" stroke="${C.navy}" stroke-width="2.6"/>`;
  if(threshold){out+=`<line x1="${pad.l}" y1="${Y(threshold)}" x2="${pad.l+iw}" y2="${Y(threshold)}" stroke="${C.rust}" stroke-dasharray="5 4"/>`;
    out+=`<text x="${pad.l+6}" y="${Y(threshold)-6}" font-size="10.5" font-weight="700" fill="${C.rust}">US$1 trillion</text>`;}
  years.forEach((y,i)=>{if(i%2===0)out+=`<text x="${X(i)}" y="${h-9}" text-anchor="middle" font-size="10.5" fill="${C.slate}">${y}</text>`;});
  return svg(w,h,out);
}
function footballField(bands,marks,w,h,cur){
  const pad={l:14,r:14,t:26,b:34}, iw=w-pad.l-pad.r;
  const all=[...bands.flatMap(b=>[b.lo,b.hi]),...marks.map(m=>m.v)];
  const min=Math.min(...all)*0.9, max=Math.max(...all)*1.06;
  const X=v=>pad.l+iw*(v-min)/(max-min);
  const rowH=(h-pad.t-pad.b)/bands.length;
  let out="";
  bands.forEach((b,i)=>{const y=pad.t+i*rowH;
    out+=`<rect x="${X(b.lo)}" y="${y+7}" width="${Math.max(3,X(b.hi)-X(b.lo))}" height="${rowH-20}" rx="4" fill="${b.color}" opacity="0.9"/>`;
    out+=`<text x="${X(b.lo)+8}" y="${y+rowH/2+2}" font-size="11" font-weight="700" fill="#fff">${cur}${fmt(b.lo)}</text>`;
    out+=`<text x="${X(b.hi)-8}" y="${y+rowH/2+2}" text-anchor="end" font-size="11" font-weight="700" fill="#fff">${cur}${fmt(b.hi)}</text>`;
    out+=`<text x="${pad.l}" y="${y+rowH-4}" font-size="10.5" fill="${C.slate}">${esc(b.name)}</text>`;
    if(b.mid!=null)out+=`<circle cx="${X(b.mid)}" cy="${y+rowH/2-3}" r="5" fill="#fff" stroke="${b.color}" stroke-width="2"/>`;});
  marks.forEach(m=>{out+=`<line x1="${X(m.v)}" y1="${pad.t-6}" x2="${X(m.v)}" y2="${h-pad.b+6}" stroke="${m.color}" stroke-width="2" stroke-dasharray="${m.dash||""}"/>`;
    out+=`<text x="${X(m.v)}" y="${pad.t-11}" text-anchor="middle" font-size="10.5" font-weight="700" fill="${m.color}">${esc(m.name)} ${cur}${fmt(m.v,2)}</text>`;});
  return svg(w,h,out);
}
function scatterFrontier(fr,pts,w,h){
  const pad={l:52,r:16,t:16,b:38}, iw=w-pad.l-pad.r, ih=h-pad.t-pad.b;
  const xs=fr.map(f=>f.volatility*100).concat(pts.map(p=>p.x));
  const ys=fr.map(f=>f.target_return*100).concat(pts.map(p=>p.y));
  const x0=Math.min(...xs)*0.9,x1=Math.max(...xs)*1.06,y0=Math.min(...ys)*0.94,y1=Math.max(...ys)*1.04;
  const X=v=>pad.l+iw*(v-x0)/(x1-x0), Y=v=>pad.t+ih-ih*(v-y0)/(y1-y0);
  let out="";
  for(let g=0;g<=4;g++){const y=pad.t+ih*g/4,v=y1-(y1-y0)*g/4;
    out+=`<line x1="${pad.l}" y1="${y}" x2="${pad.l+iw}" y2="${y}" stroke="#EDF0F3"/>`;
    out+=`<text x="${pad.l-8}" y="${y+4}" text-anchor="end" font-size="10.5" fill="${C.slate}">${v.toFixed(1)}%</text>`;}
  out+=`<polyline points="${fr.map(f=>`${X(f.volatility*100)},${Y(f.target_return*100)}`).join(" ")}" fill="none" stroke="${C.navy}" stroke-width="2.4"/>`;
  pts.forEach(p=>{out+=`<circle cx="${X(p.x)}" cy="${Y(p.y)}" r="8" fill="${p.color}" stroke="#fff" stroke-width="2"><title>${esc(p.name)}</title></circle>`;
    out+=`<text x="${X(p.x)+12}" y="${Y(p.y)+4}" font-size="11" font-weight="600" fill="${C.navy}">${esc(p.name)}</text>`;});
  out+=`<text x="${pad.l+iw/2}" y="${h-8}" text-anchor="middle" font-size="11" fill="${C.slate}">Volatility (% p.a.)</text>`;
  return svg(w,h,out);
}

/* ---------------- tabs ---------------- */
const TABS=[["overview","Overview"],["portfolio","Portfolio composition"],["deals","Investment trends"],
            ["valuation","Valuation case studies"],["quant","Quant &amp; AI"],["method","Method &amp; sources"]];
$("#nav").innerHTML=TABS.map(([id,l],i)=>`<button data-t="${id}" class="${i===0?'active':''}">${l}</button>`).join("");
$("#nav").addEventListener("click",e=>{const b=e.target.closest("button"); if(!b)return;
  document.querySelectorAll("nav button").forEach(x=>x.classList.remove("active"));
  document.querySelectorAll(".tab").forEach(x=>x.classList.remove("active"));
  b.classList.add("active"); $("#t-"+b.dataset.t).classList.add("active");});

/* ---------------- OVERVIEW ---------------- */
const k=DATA.kpi;
$("#t-overview").innerHTML=`
<div class="grid k4">
 ${[["Assets under management","US$"+fmt(k["AUM (USD bn)"])+"bn","+"+fmt(k["AUM growth YoY (%)"],0)+"% year on year"],
    ["5-year annualised IRR",fmt(k["5-year annualised IRR (%)"],1)+"%","10-year: "+fmt(k["10-year annualised IRR (%)"],1)+"%"],
    ["Capital deployed 2025","US$"+fmt(k["Capital deployed (USD bn)"])+"bn","+"+fmt(k["Deployment growth YoY (%)"],0)+"% year on year"],
    ["Proceeds 2025","US$"+fmt(k["Proceeds (USD bn)"])+"bn","+"+fmt(k["Proceeds growth YoY (%)"],0)+"% year on year"]]
  .map(([l,v,n])=>`<div class="card kpi"><div class="label">${l}</div><div class="value">${v}</div><div class="note">${n}</div></div>`).join("")}
</div>
<div class="grid c2" style="margin-top:16px">
 <div class="card"><h3>Portfolio by asset class</h3><div class="sub">FY2025 &mdash; officially disclosed weights</div>
   ${svg(420,250,donut(DATA.allocation,"weight_pct","asset_class",150,125,110,66)+
     `<text x="150" y="122" text-anchor="middle" font-size="19" font-weight="700" fill="${C.navy}">US$385bn</text>
      <text x="150" y="140" text-anchor="middle" font-size="11" fill="${C.slate}">total AUM</text>`+
     DATA.allocation.map((a,i)=>`<rect x="284" y="${52+i*26}" width="11" height="11" rx="3" fill="${PAL[i]}"/>
      <text x="302" y="${62+i*26}" font-size="11.5" fill="${C.slate}">${esc(a.asset_class)}</text>`).join(""))}
   <div class="finding"><b>Concentration:</b> the Herfindahl index of this mix is 2,734 &mdash; formally &ldquo;concentrated&rdquo;.
   The effective number of independent buckets is 3.7, not 5.</div>
 </div>
 <div class="card"><h3>Capital deployed versus proceeds</h3><div class="sub">US$ billion &mdash; is the balance sheet self-funding?</div>
   ${groupedBars(DATA.flows,"year",[{key:"deployments_usd_bn",name:"Deployed",color:C.navy},
      {key:"proceeds_usd_bn",name:"Proceeds",color:C.gold}],440,255)}
   <div class="lgd"><span><i style="background:${C.navy}"></i>Capital deployed</span><span><i style="background:${C.gold}"></i>Proceeds</span></div>
   <div class="finding"><b>Recycling ratio 0.97x in 2025.</b> Realisations funded 97 cents of every dollar deployed,
   so growth in the book came from performance rather than from new shareholder capital.</div>
 </div>
</div>
<div class="card" style="margin-top:16px"><h3>What this dashboard argues</h3><div class="sub">Five findings, each traceable to a query or a model in this project</div>
<ol style="margin-left:18px;font-size:13px;line-height:1.85">
<li><b>The book is concentrated, deliberately.</b> 42% private plus 16% alternatives means 58% of assets are illiquid by design &mdash; the return premium a sovereign with no redemption risk is uniquely able to harvest.</li>
<li><b>Growth is self-funded.</b> Proceeds of US$38bn against US$39bn deployed. The portfolio pays for its own expansion.</li>
<li><b>Technology is the strategic spine.</b> Semiconductors, AI infrastructure and AI-enabled healthcare recur across every platform, not just the technology bucket.</li>
<li><b>The public-equity sleeve is a liquidity choice, not a return choice.</b> Mean-variance optimisation would hold none of it; it exists to fund drawdowns without forced private-asset sales.</li>
<li><b>Valuation discipline varies by asset.</b> GlobalFoundries trades above our base-case DCF; OMV sits close to fair value with a thinning dividend cushion; WHOOP is priced for a decade of 35% growth.</li>
</ol></div>`;

/* ---------------- PORTFOLIO ---------------- */
function agg(rows,key){const m={};rows.forEach(r=>{m[r[key]]=(m[r[key]]||0)+1});
  return Object.entries(m).map(([k,v])=>({name:k,n:v})).sort((a,b)=>b.n-a.n);}
function renderPortfolio(){
  const fS=$("#fSector").value,fR=$("#fRegion").value,fP=$("#fPlatform").value;
  let rows=DATA.holdings.filter(h=>(fS==="All"||h.sector_name===fS)&&(fR==="All"||h.region===fR)&&(fP==="All"||h.platform_name===fP));
  $("#pCount").textContent=rows.length;
  const bySec=agg(rows,"sector_name"), byReg=agg(rows,"region"), byPlat=agg(rows,"platform_name");
  const aiCol=r=>{const h=rows.find(x=>x.sector_name===r.name); return h&&h.ai_exposure==="High"?C.gold:(h&&h.ai_exposure==="Medium"?C.teal:C.slate);};
  $("#chSector").innerHTML=hbars(bySec,"name","n",470,32,{labelWidth:200,color:aiCol});
  $("#chRegion").innerHTML=hbars(byReg,"name","n",470,32,{labelWidth:150,color:()=>C.navy});
  $("#chPlatform").innerHTML=hbars(byPlat,"name","n",470,32,{labelWidth:210,color:()=>C.teal});
  $("#tblHold").innerHTML=rows.map(h=>`<tr>
    <td><b>${esc(h.holding_name)}</b>${h.ticker&&h.ticker!=="-"?` <span class="tag">${esc(h.ticker)}</span>`:""}<div style="color:#5A6B7B;font-size:11.5px;margin-top:3px">${esc(h.investment_thesis)}</div></td>
    <td>${esc(h.sector_name)}<br><span class="pill ${h.ai_exposure==='High'?'hi':h.ai_exposure==='Medium'?'md':'lo'}">AI ${esc(h.ai_exposure)}</span></td>
    <td>${esc(h.country)}</td><td>${esc(h.platform_name)}</td>
    <td>${esc(h.ownership)}</td>
    <td><span class="pill ${h.evidence_grade==='Official'?'off':'press'}">${esc(h.evidence_grade)}</span></td></tr>`).join("");
}
$("#t-portfolio").innerHTML=`
<div class="filters">
 <label>Sector</label><select id="fSector"></select>
 <label>Region</label><select id="fRegion"></select>
 <label>Platform</label><select id="fPlatform"></select>
 <span style="margin-left:auto;font-size:12px;color:${C.slate}"><b id="pCount"></b> holdings shown</span>
</div>
<div class="grid c3">
 <div class="card"><h3>By sector</h3><div class="sub">Shaded by AI exposure</div><div id="chSector"></div>
   <div class="lgd"><span><i style="background:${C.gold}"></i>High</span><span><i style="background:${C.teal}"></i>Medium</span><span><i style="background:${C.slate}"></i>Low</span></div></div>
 <div class="card"><h3>By region</h3><div class="sub">Where the capital sits</div><div id="chRegion"></div></div>
 <div class="card"><h3>By platform</h3><div class="sub">Which team owns the relationship</div><div id="chPlatform"></div></div>
</div>
<div class="card" style="margin-top:16px"><h3>Tracked holdings</h3>
 <div class="sub">Twenty named positions assembled from Mubadala disclosures. Evidence grade shown for every row.</div>
 <div class="scroll"><table><thead><tr><th>Holding &amp; thesis</th><th>Sector</th><th>Country</th><th>Platform</th><th>Ownership</th><th>Evidence</th></tr></thead><tbody id="tblHold"></tbody></table></div>
 <div class="note"><b>Read this honestly:</b> Mubadala does not publish a line-by-line portfolio with valuations.
 This table is a curated set of named, publicly disclosed positions &mdash; it is a representative sample, not the whole book.</div></div>`;
["Sector","Region","Platform"].forEach(f=>{
  const key={Sector:"sector_name",Region:"region",Platform:"platform_name"}[f];
  const vals=["All",...[...new Set(DATA.holdings.map(h=>h[key]))].sort()];
  $("#f"+f).innerHTML=vals.map(v=>`<option>${esc(v)}</option>`).join("");
  $("#f"+f).addEventListener("change",renderPortfolio);});
renderPortfolio();

/* ---------------- DEALS ---------------- */
let sortKey="announce_date",sortDir=-1;
function renderDeals(){
  const fy=$("#dYear").value, fs=$("#dSector").value;
  let rows=DATA.transactions.filter(t=>(fy==="All"||t.year===fy)&&(fs==="All"||t.sector_name===fs));
  rows=[...rows].sort((a,b)=>{const A=a[sortKey],B=b[sortKey];
    const na=A===""||A==null, nb=B===""||B==null; if(na&&nb)return 0; if(na)return 1; if(nb)return -1;
    return (typeof A==="number"?A-B:String(A).localeCompare(String(B)))*sortDir;});
  const disclosed=rows.filter(r=>r.value_usd_m!=="").reduce((a,b)=>a+Number(b.value_usd_m||0),0);
  $("#dCount").textContent=rows.length;
  $("#dValue").textContent="US$"+fmt(disclosed/1000,1)+"bn";
  const bySec=agg(rows,"sector_name"), byReg=agg(rows,"region");
  $("#chDealSector").innerHTML=hbars(bySec,"name","n",470,30,{labelWidth:200,color:()=>C.navy});
  $("#chDealRegion").innerHTML=hbars(byReg,"name","n",470,30,{labelWidth:150,color:()=>C.gold});
  $("#tblDeals").innerHTML=rows.map(t=>`<tr>
    <td>${esc(t.announce_date)}</td><td><b>${esc(t.target)}</b></td><td>${esc(t.deal_type)}</td>
    <td>${esc(t.sector_name)}</td><td>${esc(t.country)}</td><td>${esc(t.platform_name)}</td>
    <td class="num">${t.value_usd_m===""?'<span class="tag">n/d</span>':fmt(t.value_usd_m)}</td></tr>`).join("");
}
$("#t-deals").innerHTML=`
<div class="filters"><label>Year</label><select id="dYear"></select>
 <label>Sector</label><select id="dSector"></select>
 <span style="margin-left:auto;font-size:12px;color:${C.slate}"><b id="dCount"></b> transactions &middot; <b id="dValue"></b> disclosed value</span></div>
<div class="grid c2">
 <div class="card"><h3>Transactions by sector</h3><div class="sub">2025&ndash;2026 announcements</div><div id="chDealSector"></div></div>
 <div class="card"><h3>Transactions by region</h3><div class="sub">Where new money is going</div><div id="chDealRegion"></div></div>
</div>
<div class="card" style="margin-top:16px"><h3>Transaction log</h3>
 <div class="sub">Click any column header to sort. &ldquo;n/d&rdquo; means the value was not disclosed &mdash; we do not estimate it.</div>
 <div class="scroll"><table><thead><tr>
  ${[["announce_date","Date"],["target","Target"],["deal_type","Type"],["sector_name","Sector"],
     ["country","Country"],["platform_name","Platform"],["value_usd_m","Value (US$m)"]]
    .map(([k,l])=>`<th data-k="${k}">${l}</th>`).join("")}
 </tr></thead><tbody id="tblDeals"></tbody></table></div>
 <div class="finding"><b>What the log shows:</b> of nineteen tracked announcements, ten carry no disclosed value.
 Any &ldquo;total deal value&rdquo; headline built from public sources is therefore a floor, never a total. The dashboard
 reports the floor and says so.</div></div>`;
$("#dYear").innerHTML=["All",...[...new Set(DATA.transactions.map(t=>t.year))].sort().reverse()].map(v=>`<option>${v}</option>`).join("");
$("#dSector").innerHTML=["All",...[...new Set(DATA.transactions.map(t=>t.sector_name))].sort()].map(v=>`<option>${esc(v)}</option>`).join("");
$("#dYear").addEventListener("change",renderDeals); $("#dSector").addEventListener("change",renderDeals);
$("#t-deals").addEventListener("click",e=>{const th=e.target.closest("th[data-k]"); if(!th)return;
  if(sortKey===th.dataset.k)sortDir*=-1; else{sortKey=th.dataset.k;sortDir=1;} renderDeals();});
renderDeals();

/* ---------------- VALUATION ---------------- */
const g=DATA.cases.gfs,o=DATA.cases.omv,wh=DATA.cases.whoop,mc=DATA.cases.mcap;
const gf=g.football_field,of_=o.football_field;
$("#t-valuation").innerHTML=`
<div class="grid c2">
 <div class="card"><h3>1. Technology &mdash; GlobalFoundries (NASDAQ: GFS)</h3>
  <div class="sub">Mubadala controls c.80%. Five-year FCFF DCF, WACC ${(g.wacc.wacc*100).toFixed(2)}%, terminal growth 2.5%.</div>
  ${footballField([{name:"DCF range",lo:gf["DCF low (WACC +1.5%, g -1.0%)"],hi:gf["DCF high (WACC -1.5%, g +1.0%)"],mid:gf["DCF base"],color:C.navy},
                   {name:"Comparables 11.0x&ndash;17.0x EV/EBITDA",lo:gf["Comparables low (11.0x EV/EBITDA)"],hi:gf["Comparables high (17.0x EV/EBITDA)"],mid:gf["Comparables mid (14.5x EV/EBITDA)"],color:C.gold}],
                  [{name:"market",v:gf["Current market price"],color:C.rust},{name:"consensus",v:gf["Sell-side consensus target"],color:C.teal,dash:"5 4"}],460,190,"$")}
  <div class="warn"><b>The reverse DCF is the interesting bit.</b> At $50.01 the market requires a steady-state EBIT margin of
  <b>${(g.reverse_dcf.implied_terminal_ebit_margin*100).toFixed(1)}%</b> against ${(g.reverse_dcf.ttm_ebit_margin*100).toFixed(1)}% today.
  That is essentially full delivery of management's 2030 gross-margin plan. Buying the shares here is underwriting execution, not valuation.</div></div>

 <div class="card"><h3>2. Energy &mdash; OMV AG (VIE: OMV)</h3>
  <div class="sub">Mubadala holds 24.9%. WACC ${(o.wacc.wacc*100).toFixed(2)}% using a sector beta of 0.90 in place of the raw 0.21.</div>
  ${footballField([{name:"DCF range",lo:of_["DCF low (WACC +1.5%, g -1.0%)"],hi:of_["DCF high (WACC -1.5%, g +1.0%)"],mid:of_["DCF base"],color:C.navy},
                   {name:"Comparables 9.8x&ndash;15.6x normalised P/E",lo:of_["Comparables low (9.8x normalised P/E)"],hi:of_["Comparables high (15.6x normalised P/E)"],mid:of_["Comparables median (12.4x normalised P/E)"],color:C.gold}],
                  [{name:"market",v:of_["Current market price"],color:C.rust},{name:"consensus",v:of_["Sell-side consensus target"],color:C.teal,dash:"5 4"}],460,190,"&euro;")}
  <div class="warn"><b>The dividend is the risk, not the valuation.</b> Free-cash-flow cover of the payout has fallen
  6.0x &rarr; 5.3x &rarr; 2.3x &rarr; 1.9x &rarr; 1.3x while the dividend per share was raised every year.
  The 8.1% yield is real but the cushion behind it has almost gone.</div></div>
</div>
<div class="grid c2" style="margin-top:16px">
 <div class="card"><h3>3. Healthcare &mdash; WHOOP Inc. (private)</h3>
  <div class="sub">Series G: US$575m raised at a US$10.1bn post-money, March 2026. Valued by reverse DCF.</div>
  ${hbars(Object.entries(wh.scenarios).map(([k,v])=>({name:k.split(" - ")[0],v:v.value_usd_m/1000,cagr:v.revenue_cagr})),
    "name","v",460,44,{labelWidth:60,color:(r,i)=>[C.rust,C.navy,C.teal][i],
    fmt:r=>`US$${r.v.toFixed(1)}bn &middot; ${(r.cagr*100).toFixed(0)}% CAGR`})}
  <div class="finding"><b>What the price assumes:</b> revenue compounding at
  <b>${(wh.reverse_dcf.implied_revenue_cagr*100).toFixed(1)}% a year for a decade</b>, from a US$1.1bn run-rate to about
  US$${wh.reverse_dcf.implied_revenue_year10_usd_bn}bn by 2035, with free-cash-flow margins reaching 20%.
  Entry multiple ${wh.implied_entry_multiples.ev_revenue_pre_money}x revenue &mdash; a ${wh.listed_reference_multiples.premium_to_listed_median_x}x premium to listed healthcare platforms.</div></div>

 <div class="card"><h3>4. Financial services &mdash; Mubadala Capital</h3>
  <div class="sub">c.US$30bn AUM (official). What would the fee franchise be worth if it were listed?</div>
  ${hbars(Object.entries(mc.valuation_range_usd_bn).map(([k,v])=>({name:k.split(" - ")[0].trim(),v})),
    "name","v",460,38,{labelWidth:150,color:(r,i)=>[C.slate,C.navy,C.gold,C.teal][i],fmt:r=>`US$${r.v.toFixed(2)}bn`})}
  <div class="finding"><b>Central estimate US$${mc.central_after_discount_usd_bn.toFixed(2)}bn</b> after a 25% private-company discount.
  The point is structural: Mubadala Capital converts third-party capital into a fee annuity valued on a multiple of earnings,
  on top of the return earned on Mubadala's own balance sheet. It is the one part of the group that creates value
  independently of the direction of asset prices.</div></div>
</div>
<div class="card" style="margin-top:16px"><h3>Why these four</h3>
<div class="sub">Four sectors, four deliberately different valuation problems &mdash; because one method does not fit every asset</div>
<table><thead><tr><th>Case</th><th>Sector</th><th>Why it is hard</th><th>Method chosen</th></tr></thead><tbody>
<tr><td><b>GlobalFoundries</b></td><td>Technology</td><td>Cyclical margins, heavy capex, AI optionality not in reported numbers</td><td>FCFF DCF, comparables, reverse DCF to price the optionality</td></tr>
<tr><td><b>OMV</b></td><td>Energy</td><td>Commodity cycle, non-credible raw beta, large consolidated minorities, distorted reported EPS</td><td>FCFF DCF with sector beta and a full EV bridge; normalised-EPS comparables; dividend-cover test</td></tr>
<tr><td><b>WHOOP</b></td><td>Healthcare</td><td>Private: no accounts, only a disclosed transaction price</td><td>Reverse DCF &mdash; solve for what the price assumes rather than invent a forecast</td></tr>
<tr><td><b>Mubadala Capital</b></td><td>Financial services</td><td>Private, and the asset is a fee stream rather than a balance sheet</td><td>Fee-franchise sum-of-the-parts against the listed alternative-manager cohort</td></tr>
</tbody></table></div>`;

/* ---------------- QUANT ---------------- */
const po=DATA.optimiser,m=DATA.montecarlo,cl=DATA.classifier;
const yrs=Array.from({length:m.median_path_usd_bn.length},(_,i)=>2025+i);
$("#t-quant").innerHTML=`
<div class="grid c2">
 <div class="card"><h3>Is the disclosed asset mix efficient?</h3>
  <div class="sub">Mean-variance optimisation. Capital-market assumptions are the author's; the weights are Mubadala's.</div>
  ${scatterFrontier(po.efficient_frontier,[
    {x:po.actual_portfolio.volatility*100,y:po.actual_portfolio.expected_return*100,name:"Actual mix",color:C.gold},
    {x:po.max_sharpe_portfolio.volatility*100,y:po.max_sharpe_portfolio.expected_return*100,name:"Max Sharpe",color:C.teal},
    {x:po.min_variance_portfolio.volatility*100,y:po.min_variance_portfolio.expected_return*100,name:"Min variance",color:C.rust}],460,270)}
  <div class="finding">The published mix sits <b>${po.efficiency_test.excess_volatility_carried_pp}pp</b> of volatility to the right of the frontier
  at the same expected return. The gap is almost entirely the 20% public-equity sleeve, which a pure return optimiser would not hold at all.
  That is not a mistake &mdash; it is the price of liquidity, and naming that price is the useful output.</div></div>

 <div class="card"><h3>Ten-year AUM simulation</h3>
  <div class="sub">50,000 paths, Student-t shocks for fat tails, 10.7% expected return (the disclosed 5-year IRR)</div>
  ${fanChart(yrs,m.median_path_usd_bn,m.p10_path_usd_bn,m.p90_path_usd_bn,460,270,1000)}
  <div class="finding">Median 2035 AUM <b>US$${fmt(m.outcome_distribution_usd_bn.median)}bn</b>, with a
  <b>${(m.probabilities["P(AUM > $1,000bn by 2035)"]*100).toFixed(0)}%</b> probability of crossing US$1 trillion and a
  ${(m.drawdown["P(peak-to-trough drawdown worse than 20%)"]*100).toFixed(0)}% chance of a peak-to-trough drawdown worse than 20% along the way.</div></div>
</div>
<div class="grid c2" style="margin-top:16px">
 <div class="card"><h3>Reverse optimisation &mdash; what returns does the mix imply?</h3>
  <div class="sub">If the published weights are optimal, these are the returns the allocator must believe in</div>
  ${hbars(Object.entries(po.reverse_optimisation.implied_expected_returns).map(([k,v])=>({name:k,v:+(v*100).toFixed(1)})),
    "name","v",460,34,{labelWidth:170,color:()=>C.navy,fmt:r=>r.v.toFixed(1)+"%"})}
  <div class="note">This is a cleaner way to interrogate an allocation than arguing about whether it is &ldquo;right&rdquo;.
  It converts a policy into a set of testable beliefs.</div></div>
 <div class="card"><h3>Machine-learning sector classifier</h3>
  <div class="sub">TF-IDF word + character n-grams &rarr; multinomial logistic regression</div>
  <div class="grid k4" style="margin-bottom:12px">
   <div><div class="label" style="font-size:10.5px;color:${C.slate};font-weight:700">HOLD-OUT ACCURACY</div>
     <div style="font-size:26px;font-weight:700;color:${C.navy}">${(cl.holdout_real_headlines.accuracy*100).toFixed(0)}%</div>
     <div style="font-size:11px;color:${C.teal};font-weight:600">on ${cl.holdout_real_headlines.n} real headlines</div></div>
   <div><div class="label" style="font-size:10.5px;color:${C.slate};font-weight:700">TRAINING EXAMPLES</div>
     <div style="font-size:26px;font-weight:700;color:${C.navy}">${fmt(cl.training_corpus.n_examples)}</div>
     <div style="font-size:11px;color:${C.slate};font-weight:600">synthetic, disclosed</div></div>
  </div>
  <div class="scroll" style="max-height:250px"><table><thead><tr><th>Headline</th><th>Predicted</th><th class="num">Conf.</th></tr></thead><tbody>
  ${cl.holdout_real_headlines.rows.map(r=>`<tr><td style="font-size:11.5px">${esc(r.headline.slice(0,72))}&hellip;</td>
    <td>${r.correct?"":"<b style='color:"+C.rust+"'>&times;</b> "}${esc(r.predicted)}</td>
    <td class="num">${r.confidence.toFixed(2)}</td></tr>`).join("")}</tbody></table></div>
  <div class="warn"><b>The one miss is the instructive one.</b> &ldquo;CoolIT data centre liquid cooling&rdquo; was tagged Industrials,
  not Technology. A single-label model cannot represent a deal that is genuinely both. The fix is a multi-label data model,
  not a bigger classifier.</div></div>
</div>`;

/* ---------------- METHOD ---------------- */
$("#t-method").innerHTML=`
<div class="grid c2">
 <div class="card"><h3>How this was built</h3><div class="sub">Seven stages, each reproducible from the repository</div>
 <ol style="margin-left:18px;line-height:2;font-size:13px">
  <li><b>Source collection</b> &mdash; Mubadala's 2025 Annual Review, press releases and corporate site; market data from StockAnalysis / S&amp;P Global.</li>
  <li><b>Star-schema warehouse</b> &mdash; five dimension and eleven fact tables in SQLite, every row carrying a source ID.</li>
  <li><b>SQL analysis</b> &mdash; twelve queries using CTEs, window functions, conditional aggregation and a Herfindahl concentration calculation.</li>
  <li><b>Valuation models</b> &mdash; a shared Python engine plus four case studies, mirrored in a live Excel workbook.</li>
  <li><b>Quantitative layer</b> &mdash; mean-variance optimisation, reverse optimisation, Monte Carlo, k-means clustering.</li>
  <li><b>Machine learning</b> &mdash; a text classifier that tags announcements to sectors, tested on unseen real headlines.</li>
  <li><b>Reporting</b> &mdash; this dashboard, a Power BI build guide, and three written documents.</li>
 </ol></div>
 <div class="card"><h3>Evidence grading</h3><div class="sub">Every number in this project carries one of four grades</div>
 <table><tbody>
  <tr><td><span class="pill off">Official</span></td><td>Stated by Mubadala or in a company filing. Example: AUM of US$385bn.</td></tr>
  <tr><td><span class="pill md">Market data</span></td><td>Observable exchange or vendor data. Example: GFS enterprise value of US$25.4bn.</td></tr>
  <tr><td><span class="pill press">Press reporting</span></td><td>Widely reported, not confirmed by Mubadala. Example: the c.80% GlobalFoundries stake.</td></tr>
  <tr><td><span class="pill lo">Analyst estimate</span></td><td>Constructed by the author. Example: every forward growth and margin assumption.</td></tr>
 </tbody></table>
 <div class="warn"><b>What this project deliberately does not do:</b> invent a valuation for Mubadala's whole portfolio.
 The group does not disclose position-level values, and a number built by guessing would be worse than no number.
 Where a value is unknown, this dashboard shows &ldquo;n/d&rdquo;.</div></div>
</div>
<div class="card" style="margin-top:16px"><h3>Sources</h3>
<table><thead><tr><th>ID</th><th>Source</th><th>As of</th><th>Class</th></tr></thead><tbody>
${[["S01","Mubadala press release &mdash; 2025 annual results","2026-04-09","Official"],
   ["S02","Mubadala 2025 Annual Review &mdash; Performance Overview","2026-04-09","Official"],
   ["S03","Mubadala 2025 Annual Review &mdash; Key Investment Highlights","2026-04-09","Official"],
   ["S04","Mubadala corporate site &mdash; Our Structure","2026-08-04","Official"],
   ["S05","Mubadala press release &mdash; WHOOP Series G","2026-03-31","Official"],
   ["S06","Mubadala newsroom &mdash; 2026 transaction announcements","2026-08-04","Official"],
   ["S07","StockAnalysis / S&amp;P Global &mdash; GlobalFoundries","2026-08-03","Market data"],
   ["S08","StockAnalysis / S&amp;P Global &mdash; OMV AG","2026-06-30","Market data"],
   ["S09","StockAnalysis &mdash; listed peer comparison tables","2026-08-04","Market data"],
   ["S10","Analyst estimate constructed for this project","2026-08-04","Analyst estimate"]]
  .map(r=>`<tr><td><b>${r[0]}</b></td><td>${r[1]}</td><td>${r[2]}</td><td>${r[3]}</td></tr>`).join("")}
</tbody></table></div>`;
</script></body></html>"""

html = HTML.replace("__DATA__", json.dumps(DATA, separators=(",",":"), default=str))
out = os.path.join(HERE, "Mubadala_Portfolio_Dashboard.html")
with open(out,"w") as f: f.write(html)
print(f"Written: {out}  ({len(html)/1024:.0f} KB, fully self-contained)")
