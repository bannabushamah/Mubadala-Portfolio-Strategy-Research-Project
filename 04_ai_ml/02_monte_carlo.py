"""
02_monte_carlo.py
Ten-year Monte Carlo projection of Mubadala's assets under management.

QUESTION: Mubadala grew AUM 17% to US$385bn in 2025 and has compounded at
10.7% over five years. If the next decade looks like a random draw from a
plausible return distribution, what range of outcomes should the board plan
for - and what is the probability of hitting a US$1 trillion balance sheet?

METHOD: geometric Brownian motion on total AUM with an annual net capital
flow, 50,000 paths, Student-t innovations to give the fat tails that normal
distributions famously miss in real markets.
"""
import json, os
import numpy as np

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs")
os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(20260804)

# ---- inputs ---------------------------------------------------------------
AUM_0        = 385.0     # OFFICIAL: US$bn at end-2025
MU           = 0.107     # OFFICIAL: disclosed 5-year annualised IRR
SIGMA        = 0.125     # ASSUMPTION: consistent with the modelled asset mix
NET_FLOW     = 1.0       # OFFICIAL: 2025 deployments 39 less proceeds 38
YEARS        = 10
PATHS        = 50_000
DF           = 5         # Student-t degrees of freedom -> fat tails

# ---- simulation -----------------------------------------------------------
t_draws = rng.standard_t(DF, size=(PATHS, YEARS))
t_draws /= np.sqrt(DF/(DF-2))                      # rescale to unit variance
shocks  = MU - 0.5*SIGMA**2 + SIGMA*t_draws        # log-return per year

paths = np.zeros((PATHS, YEARS+1)); paths[:,0] = AUM_0
for y in range(1, YEARS+1):
    paths[:,y] = paths[:,y-1]*np.exp(shocks[:,y-1]) + NET_FLOW

final = paths[:,-1]
pct = lambda p: float(np.percentile(final, p))

# ---- drawdown analysis ----------------------------------------------------
running_max = np.maximum.accumulate(paths, axis=1)
drawdowns   = (paths - running_max) / running_max
max_dd      = drawdowns.min(axis=1)

result = {
 "question": "What range of AUM outcomes should Mubadala plan for over 2026-2035?",
 "inputs": {"starting_aum_usd_bn": AUM_0, "expected_return": MU,
            "volatility_ASSUMPTION": SIGMA, "annual_net_flow_usd_bn": NET_FLOW,
            "years": YEARS, "paths": PATHS,
            "distribution": f"Student-t with {DF} degrees of freedom, variance-rescaled",
            "note": "Return is the officially disclosed 5-year IRR. Volatility is an author assumption."},
 "outcome_distribution_usd_bn": {
    "p5": round(pct(5),1), "p10": round(pct(10),1), "p25": round(pct(25),1),
    "median": round(pct(50),1), "mean": round(float(final.mean()),1),
    "p75": round(pct(75),1), "p90": round(pct(90),1), "p95": round(pct(95),1)},
 "probabilities": {
    "P(AUM > $500bn by 2035)": round(float((final>500).mean()),4),
    "P(AUM > $750bn by 2035)": round(float((final>750).mean()),4),
    "P(AUM > $1,000bn by 2035)": round(float((final>1000).mean()),4),
    "P(AUM below today's $385bn in 2035)": round(float((final<AUM_0).mean()),4)},
 "implied_cagr": {
    "p5":  round(float((pct(5)/AUM_0)**(1/YEARS)-1),4),
    "median": round(float((pct(50)/AUM_0)**(1/YEARS)-1),4),
    "p95": round(float((pct(95)/AUM_0)**(1/YEARS)-1),4)},
 "drawdown": {
    "median_max_drawdown": round(float(np.median(max_dd)),4),
    "p5_max_drawdown": round(float(np.percentile(max_dd,5)),4),
    "P(peak-to-trough drawdown worse than 20%)": round(float((max_dd<-0.20).mean()),4)},
 "median_path_usd_bn": [round(float(np.percentile(paths[:,y],50)),1) for y in range(YEARS+1)],
 "p10_path_usd_bn":    [round(float(np.percentile(paths[:,y],10)),1) for y in range(YEARS+1)],
 "p90_path_usd_bn":    [round(float(np.percentile(paths[:,y],90)),1) for y in range(YEARS+1)],
}
with open(os.path.join(OUT,"monte_carlo.json"),"w") as f: json.dump(result,f,indent=2)
np.save(os.path.join(OUT,"mc_paths_sample.npy"), paths[:500])

d=result["outcome_distribution_usd_bn"]
print(f"Starting AUM US${AUM_0:.0f}bn, {MU*100:.1f}% expected return, {SIGMA*100:.1f}% vol, {PATHS:,} paths\n")
print(f"2035 AUM   p5 ${d['p5']:,.0f}bn | p25 ${d['p25']:,.0f}bn | MEDIAN ${d['median']:,.0f}bn | p75 ${d['p75']:,.0f}bn | p95 ${d['p95']:,.0f}bn")
for k,v in result["probabilities"].items(): print(f"  {k:44s} {v*100:5.1f}%")
print(f"\nMedian worst peak-to-trough drawdown along the path: {result['drawdown']['median_max_drawdown']*100:.1f}%")
print(f"Probability of a drawdown worse than 20%:            {result['drawdown']['P(peak-to-trough drawdown worse than 20%)']*100:.1f}%")
