"""make_charts.py - every figure used in the report and the dashboard."""
import os, json
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np, pandas as pd

HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(HERE)
WH=os.path.join(ROOT,"01_data","warehouse"); AI=os.path.join(ROOT,"04_ai_ml","outputs")
VAL=os.path.join(ROOT,"03_valuation_models","outputs"); QR=os.path.join(ROOT,"02_sql","query_results")

NAVY="#0B2545"; GOLD="#C9A227"; TEAL="#1B7F79"; SLATE="#5A6B7B"; RUST="#A6432F"; SAND="#E4D8B4"
PAL=[NAVY,GOLD,TEAL,SLATE,RUST,SAND,"#7A5C9E","#3E7CB1"]
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":9,"axes.edgecolor":"#C9CFD6",
  "axes.labelcolor":NAVY,"text.color":NAVY,"xtick.color":SLATE,"ytick.color":SLATE,
  "axes.spines.top":False,"axes.spines.right":False,"figure.dpi":150,"savefig.dpi":150,
  "savefig.bbox":"tight","axes.grid":True,"grid.color":"#EDF0F3","grid.linewidth":0.8})

def save(fig,name):
    fig.savefig(os.path.join(HERE,name+".png"), facecolor="white"); plt.close(fig)
    print("  ",name+".png")

J=lambda p: json.load(open(p))

# 1 ---- asset allocation donut
al=pd.read_csv(os.path.join(WH,"fact_asset_allocation.csv"))
fig,ax=plt.subplots(figsize=(6,4.4))
wed,_,at=ax.pie(al.weight_pct, labels=None, autopct="%1.0f%%", startangle=90,
  colors=PAL[:5], pctdistance=0.78, wedgeprops=dict(width=0.42,edgecolor="white",linewidth=2),
  textprops=dict(color="white",fontweight="bold",fontsize=10))
ax.legend(wed,[f"{a}  ({b:.0f}%)" for a,b in zip(al.asset_class,al.weight_pct)],
  loc="center left",bbox_to_anchor=(1.0,0.5),frameon=False,fontsize=9)
ax.text(0,0.08,"US$385bn",ha="center",fontsize=15,fontweight="bold",color=NAVY)
ax.text(0,-0.14,"AUM, FY2025",ha="center",fontsize=9,color=SLATE)
ax.set_title("Portfolio by asset class, FY2025",fontsize=11,fontweight="bold",loc="left",pad=14)
save(fig,"01_asset_allocation")

# 2 ---- capital flows
cf=pd.read_csv(os.path.join(WH,"fact_capital_flow.csv"))
fig,ax=plt.subplots(figsize=(6.6,3.6)); x=np.arange(len(cf)); w=0.36
ax.bar(x-w/2,cf.deployments_usd_bn,w,label="Capital deployed",color=NAVY)
ax.bar(x+w/2,cf.proceeds_usd_bn,w,label="Proceeds",color=GOLD)
for i,(d,p) in enumerate(zip(cf.deployments_usd_bn,cf.proceeds_usd_bn)):
    ax.text(i-w/2,d+0.6,f"${d:.0f}bn",ha="center",fontsize=8,fontweight="bold")
    ax.text(i+w/2,p+0.6,f"${p:.0f}bn",ha="center",fontsize=8,fontweight="bold")
ax.set_xticks(x); ax.set_xticklabels(cf.year); ax.set_ylabel("US$ billion"); ax.set_ylim(0,46)
ax.legend(frameon=False,ncol=2,loc="upper left")
ax.set_title("Capital deployed vs proceeds: a self-funding balance sheet",fontsize=11,fontweight="bold",loc="left",pad=12)
save(fig,"02_capital_flows")

# 3 ---- sector composition
q4=pd.read_csv(os.path.join(QR,"Q4.csv")).sort_values("n_holdings")
fig,ax=plt.subplots(figsize=(6.6,4.0))
cols=[GOLD if e=="High" else (TEAL if e=="Medium" else SLATE) for e in q4.ai_exposure]
ax.barh(q4.sector_name,q4.n_holdings,color=cols)
for i,(v,p) in enumerate(zip(q4.n_holdings,q4.pct_of_holdings)):
    ax.text(v+0.08,i,f"{v}  ({p:.0f}%)",va="center",fontsize=8)
ax.set_xlabel("Number of tracked holdings"); ax.set_xlim(0,5.6)
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=GOLD,label="High AI exposure"),Patch(color=TEAL,label="Medium"),
                   Patch(color=SLATE,label="Low")],frameon=False,loc="lower right",fontsize=8)
ax.set_title("Tracked portfolio by sector, shaded by AI exposure",fontsize=11,fontweight="bold",loc="left",pad=12)
save(fig,"03_sector_composition")

# 4 ---- geography
q5=pd.read_csv(os.path.join(QR,"Q5.csv"))
fig,ax=plt.subplots(figsize=(6.0,3.4))
cols=[GOLD if r=="Middle East" else NAVY for r in q5.region]
ax.bar(q5.region,q5.pct,color=cols)
for i,v in enumerate(q5.pct): ax.text(i,v+0.7,f"{v:.0f}%",ha="center",fontsize=9,fontweight="bold")
ax.set_ylabel("% of tracked holdings"); ax.set_ylim(0,42)
plt.setp(ax.get_xticklabels(),rotation=18,ha="right")
ax.set_title("Geographic footprint: 70% of tracked holdings sit outside the home market",
             fontsize=10.5,fontweight="bold",loc="left",pad=12)
save(fig,"04_geography")

# 5 ---- efficient frontier
po=J(os.path.join(AI,"portfolio_optimisation.json"))
fr=po["efficient_frontier"]
fig,ax=plt.subplots(figsize=(6.4,4.2))
ax.plot([f["volatility"]*100 for f in fr],[f["target_return"]*100 for f in fr],
        color=NAVY,lw=2,label="Efficient frontier")
a=po["actual_portfolio"]; ms=po["max_sharpe_portfolio"]; mv=po["min_variance_portfolio"]
ax.scatter(a["volatility"]*100,a["expected_return"]*100,s=150,color=GOLD,zorder=5,
           edgecolor="white",linewidth=1.6,label="Mubadala actual mix (2025)")
ax.scatter(ms["volatility"]*100,ms["expected_return"]*100,s=110,color=TEAL,zorder=5,
           edgecolor="white",linewidth=1.4,label="Maximum-Sharpe portfolio")
ax.scatter(mv["volatility"]*100,mv["expected_return"]*100,s=110,color=RUST,zorder=5,
           edgecolor="white",linewidth=1.4,label="Minimum-variance portfolio")
et=po["efficiency_test"]
ax.annotate("", xy=(et["efficient_volatility_at_same_return"]*100,a["expected_return"]*100),
            xytext=(a["volatility"]*100,a["expected_return"]*100),
            arrowprops=dict(arrowstyle="->",color=RUST,lw=1.6))
ax.text((a["volatility"]+et["efficient_volatility_at_same_return"])/2*100,
        a["expected_return"]*100+0.28,f"{et['excess_volatility_carried_pp']:.1f}pp",
        ha="center",fontsize=8,color=RUST,fontweight="bold")
ax.set_xlabel("Volatility (% p.a.)"); ax.set_ylabel("Expected return (% p.a.)")
ax.legend(frameon=False,fontsize=8,loc="lower right")
ax.set_title("Is the disclosed asset mix efficient?",fontsize=11,fontweight="bold",loc="left",pad=12)
save(fig,"05_efficient_frontier")

# 6 ---- Monte Carlo
mc=J(os.path.join(AI,"monte_carlo.json"))
yrs=list(range(2025,2036))
fig,ax=plt.subplots(figsize=(6.6,4.0))
try:
    paths=np.load(os.path.join(AI,"mc_paths_sample.npy"))
    for p in paths[:180]: ax.plot(yrs,p,color=SLATE,alpha=0.055,lw=0.7)
except Exception: pass
ax.fill_between(yrs,mc["p10_path_usd_bn"],mc["p90_path_usd_bn"],color=GOLD,alpha=0.22,label="10th-90th percentile")
ax.plot(yrs,mc["median_path_usd_bn"],color=NAVY,lw=2.4,label="Median path")
ax.axhline(1000,color=RUST,ls="--",lw=1.2)
ax.text(2025.15,1035,"US$1 trillion",color=RUST,fontsize=8,fontweight="bold")
ax.set_ylabel("AUM (US$ billion)"); ax.set_xlim(2025,2035); ax.set_ylim(200,2200)
ax.legend(frameon=False,fontsize=8,loc="upper left")
p1000=mc["probabilities"]["P(AUM > $1,000bn by 2035)"]
ax.set_title(f"Ten-year AUM simulation: {p1000*100:.0f}% probability of crossing US$1 trillion",
             fontsize=10.5,fontweight="bold",loc="left",pad=12)
save(fig,"06_monte_carlo")

# 7 ---- GFS football field
g=J(os.path.join(VAL,"case_01_globalfoundries.json"))
ff=g["football_field"]
bands=[("DCF range",ff["DCF low (WACC +1.5%, g -1.0%)"],ff["DCF high (WACC -1.5%, g +1.0%)"],NAVY),
       ("Comparables (11.0x-17.0x EV/EBITDA)",ff["Comparables low (11.0x EV/EBITDA)"],ff["Comparables high (17.0x EV/EBITDA)"],GOLD)]
fig,ax=plt.subplots(figsize=(6.8,3.0))
for i,(lab,lo,hi,c) in enumerate(bands):
    ax.barh(i,hi-lo,left=lo,height=0.42,color=c,alpha=0.85)
    ax.text(lo+0.7,i,f"${lo:.0f}",va="center",ha="left",fontsize=8,color="white",fontweight="bold")
    ax.text(hi-0.7,i,f"${hi:.0f}",va="center",ha="right",fontsize=8,color="white",fontweight="bold")
ax.axvline(ff["Current market price"],color=RUST,lw=2)
ax.text(ff["Current market price"],1.75,f"  market ${ff['Current market price']:.2f}",color=RUST,fontsize=8,fontweight="bold")
ax.axvline(ff["Sell-side consensus target"],color=TEAL,lw=1.6,ls="--")
ax.text(ff["Sell-side consensus target"],1.75,f"  consensus ${ff['Sell-side consensus target']:.0f}",color=TEAL,fontsize=8)
ax.scatter([ff["DCF base"]],[0],color="white",edgecolor=NAVY,zorder=5,s=45)
ax.scatter([ff["Comparables mid (14.5x EV/EBITDA)"]],[1],color="white",edgecolor=GOLD,zorder=5,s=45)
ax.set_yticks(range(len(bands))); ax.set_yticklabels([b[0] for b in bands],fontsize=8.5)
ax.set_xlim(20,90); ax.set_xlabel("Value per share (USD)"); ax.set_ylim(-0.6,2.1); ax.grid(axis="y",visible=False)
ax.set_title("GlobalFoundries: valuation football field",fontsize=11,fontweight="bold",loc="left",pad=16)
save(fig,"07_gfs_football_field")

# 8 ---- GFS revenue mix shift
q10=pd.read_csv(os.path.join(QR,"Q10.csv")).sort_values("mix_shift_pp")
fig,ax=plt.subplots(figsize=(6.6,3.4))
cols=[TEAL if v>0 else RUST for v in q10.mix_shift_pp]
ax.barh(q10.end_market,q10.mix_shift_pp,color=cols)
for i,v in enumerate(q10.mix_shift_pp):
    ax.text(v+(0.14 if v>0 else -0.14),i,f"{v:+.1f}pp",va="center",
            ha="left" if v>0 else "right",fontsize=8,fontweight="bold")
ax.axvline(0,color=SLATE,lw=1); ax.set_xlabel("Change in share of revenue, 2023 to 2025 (pp)")
ax.set_xlim(-6,8.5); ax.grid(axis="y",visible=False)
ax.set_title("GlobalFoundries is rotating toward automotive silicon",fontsize=11,fontweight="bold",loc="left",pad=12)
save(fig,"08_gfs_mix_shift")

# 9 ---- OMV dividend cover
om=pd.read_csv(os.path.join(QR,"Q11.csv"))
fig,ax1=plt.subplots(figsize=(6.6,3.5))
ax1.bar(om.year,om.free_cash_flow_eur_m,color=NAVY,label="Free cash flow (EURm)")
ax1.bar(om.year,om.dps_eur*326,color=GOLD,width=0.45,label="Dividend cost (EURm)")
ax1.set_ylabel("EUR million"); ax1.legend(frameon=False,fontsize=8,loc="upper right")
ax2=ax1.twinx(); ax2.plot(om.year,om.fcf_dividend_cover_x,color=RUST,marker="o",lw=2)
for x,v in zip(om.year,om.fcf_dividend_cover_x):
    ax2.text(x,v+0.22,f"{v:.1f}x",ha="center",fontsize=8,color=RUST,fontweight="bold")
ax2.set_ylabel("FCF cover (x)",color=RUST); ax2.set_ylim(0,7.6); ax2.grid(False)
ax2.axhline(1.0,color=RUST,ls=":",lw=1)
ax1.set_title("OMV: the dividend is still covered, but the cushion has gone",fontsize=11,fontweight="bold",loc="left",pad=12)
save(fig,"09_omv_dividend_cover")

# 10 ---- WHOOP scenarios
wh=J(os.path.join(VAL,"case_03_whoop.json"))
sc=wh["scenarios"]; names=list(sc.keys()); vals=[sc[n]["value_usd_m"]/1000 for n in names]
fig,ax=plt.subplots(figsize=(6.8,3.2))
ax.barh(range(len(names)),vals,color=[RUST,NAVY,TEAL])
for i,(n,v) in enumerate(zip(names,vals)):
    ax.text(v+0.4,i,f"${v:.1f}bn  ({sc[n]['revenue_cagr']*100:.0f}% CAGR)",va="center",fontsize=8)
ax.axvline(wh["known_facts"]["pre_money_usd_m"]/1000,color=GOLD,lw=2.2)
ax.text(wh["known_facts"]["pre_money_usd_m"]/1000,len(names)-0.35,"  price paid (pre-money $9.5bn)",
        color="#8a6f10",fontsize=8,fontweight="bold")
ax.set_yticks(range(len(names))); ax.set_yticklabels([n.split(" - ")[0] for n in names],fontsize=9)
ax.set_xlabel("Implied equity value (US$ billion)"); ax.set_xlim(0,28); ax.grid(axis="y",visible=False)
ax.set_title("WHOOP: what the Series G price requires",fontsize=11,fontweight="bold",loc="left",pad=14)
save(fig,"10_whoop_scenarios")

# 11 ---- Mubadala Capital range
mcap=J(os.path.join(VAL,"case_04_mubadala_capital.json"))
vr=mcap["valuation_range_usd_bn"]
fig,ax=plt.subplots(figsize=(6.8,3.0))
ks=list(vr.keys()); vs=[vr[k] for k in ks]
ax.barh(range(len(ks)),vs,color=[SLATE,NAVY,GOLD,TEAL])
for i,v in enumerate(vs): ax.text(v+0.04,i,f"${v:.2f}bn",va="center",fontsize=8,fontweight="bold")
ax.axvline(mcap["central_after_discount_usd_bn"],color=RUST,lw=2)
ax.text(mcap["central_after_discount_usd_bn"],len(ks)-0.3,
        f"  central ${mcap['central_after_discount_usd_bn']:.2f}bn",color=RUST,fontsize=8,fontweight="bold")
ax.set_yticks(range(len(ks))); ax.set_yticklabels([k.split(" - ")[0] for k in ks],fontsize=8.5)
ax.set_xlabel("Implied value of the fee franchise (US$ billion)"); ax.grid(axis="y",visible=False)
ax.set_title("Mubadala Capital: valuing the fee annuity",fontsize=11,fontweight="bold",loc="left",pad=14)
save(fig,"11_mubadala_capital")

# 12 ---- peer clustering scatter
pc=J(os.path.join(AI,"peer_clustering.json"))
fig,ax=plt.subplots(figsize=(6.6,4.2))
for c in sorted({a["cluster"] for a in pc["assignments"]}):
    pts=[a for a in pc["assignments"] if a["cluster"]==c]
    ax.scatter([p["pc1"] for p in pts],[p["pc2"] for p in pts],s=70,color=PAL[c],
               label=f"Cluster {c} (n={len(pts)})",edgecolor="white",linewidth=1.1,zorder=3)
for a in pc["assignments"]:
    hl = a["ticker"] in ("GFS","OMV")
    ax.annotate(a["ticker"],(a["pc1"],a["pc2"]),fontsize=8.5 if hl else 7,
                fontweight="bold" if hl else "normal",
                color=RUST if hl else SLATE,xytext=(5,4),textcoords="offset points")
ax.set_xlabel("Principal component 1 (size)"); ax.set_ylabel("Principal component 2 (valuation)")
ax.legend(frameon=False,fontsize=8)
ax.set_title("How the market really groups the peer universe",fontsize=11,fontweight="bold",loc="left",pad=12)
save(fig,"12_peer_clusters")

# 13 ---- classifier confusion matrix
dc=J(os.path.join(AI,"deal_classifier.json"))
cm=np.array(dc["confusion_matrix"]["matrix"]); labs=dc["confusion_matrix"]["labels"]
fig,ax=plt.subplots(figsize=(5.8,4.8))
im=ax.imshow(cm,cmap="Blues")
ax.set_xticks(range(len(labs))); ax.set_yticks(range(len(labs)))
ax.set_xticklabels([l.replace(" & ","\n& ") for l in labs],rotation=42,ha="right",fontsize=7.5)
ax.set_yticklabels([l.replace(" & ","\n& ") for l in labs],fontsize=7.5)
for i in range(len(labs)):
    for j in range(len(labs)):
        ax.text(j,i,cm[i,j],ha="center",va="center",fontsize=8,
                color="white" if cm[i,j]>cm.max()/2 else NAVY)
ax.set_xlabel("Predicted"); ax.set_ylabel("Actual"); ax.grid(False)
ax.set_title(f"Sector classifier: {dc['holdout_real_headlines']['accuracy']*100:.0f}% correct on real headlines",
             fontsize=10.5,fontweight="bold",loc="left",pad=12)
save(fig,"13_classifier_confusion")

# 14 ---- OMV football field
o=J(os.path.join(VAL,"case_02_omv.json")); off=o["football_field"]
fig,ax=plt.subplots(figsize=(6.8,3.0))
bands=[("DCF range",off["DCF low (WACC +1.5%, g -1.0%)"],off["DCF high (WACC -1.5%, g +1.0%)"],NAVY),
       ("Comparables (9.8x-15.6x normalised P/E)",off["Comparables low (9.8x normalised P/E)"],off["Comparables high (15.6x normalised P/E)"],GOLD)]
for i,(lab,lo,hi,c) in enumerate(bands):
    ax.barh(i,hi-lo,left=lo,height=0.42,color=c,alpha=0.85)
    ax.text(lo+0.6,i,f"EUR {lo:.0f}",va="center",ha="left",fontsize=8,color="white",fontweight="bold")
    ax.text(hi-0.6,i,f"EUR {hi:.0f}",va="center",ha="right",fontsize=8,color="white",fontweight="bold")
ax.axvline(off["Current market price"],color=RUST,lw=2)
ax.text(off["Current market price"],1.75,f"  market EUR {off['Current market price']:.2f}",color=RUST,fontsize=8,fontweight="bold")
ax.axvline(off["Sell-side consensus target"],color=TEAL,lw=1.6,ls="--")
ax.text(off["Sell-side consensus target"],1.75,f"  consensus EUR {off['Sell-side consensus target']:.0f}",color=TEAL,fontsize=8)
ax.scatter([off["DCF base"]],[0],color="white",edgecolor=NAVY,zorder=5,s=45)
ax.scatter([off["Comparables median (12.4x normalised P/E)"]],[1],color="white",edgecolor=GOLD,zorder=5,s=45)
ax.set_yticks(range(len(bands))); ax.set_yticklabels([b[0] for b in bands],fontsize=8.5)
ax.set_xlabel("Value per share (EUR)"); ax.set_ylim(-0.6,2.1); ax.grid(axis="y",visible=False)
ax.set_title("OMV: valuation football field",fontsize=11,fontweight="bold",loc="left",pad=16)
save(fig,"14_omv_football_field")

print("\nAll charts written to 07_charts/")
