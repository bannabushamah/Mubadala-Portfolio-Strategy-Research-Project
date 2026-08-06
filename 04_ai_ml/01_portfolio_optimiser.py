"""
01_portfolio_optimiser.py
Mean-variance optimisation of Mubadala's disclosed 2025 asset-class mix.

QUESTION: Mubadala reports Private 42 / Public 20 / Real Estate & Infrastructure 17
/ Alternatives 16 / Credit 5. Is that mix efficient, and what is it implicitly
optimising for?

METHOD: build an efficient frontier by numerically minimising portfolio
variance for a grid of target returns, subject to long-only weights summing
to one, then locate the actual policy portfolio relative to that frontier.

HEALTH WARNING: Mubadala does not publish asset-class returns, volatilities or
correlations. The capital-market assumptions below are the author's, chosen to
sit inside the ranges published by large institutional investors for long-
horizon planning. Conclusions are about STRUCTURE, not about precise numbers.
"""
import json, os
import numpy as np
from scipy.optimize import minimize

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs")
os.makedirs(OUT, exist_ok=True)

ASSETS = ["Private","Public","Real Estate & Infra","Alternatives","Credit"]
ACTUAL = np.array([0.42, 0.20, 0.17, 0.16, 0.05])          # OFFICIAL (Mubadala 2025)

# ---- capital-market assumptions (AUTHOR'S, clearly labelled) --------------
EXP_RET = np.array([0.115, 0.080, 0.075, 0.090, 0.060])
VOL     = np.array([0.170, 0.165, 0.120, 0.130, 0.070])
CORR = np.array([
 [1.00, 0.70, 0.45, 0.65, 0.35],
 [0.70, 1.00, 0.40, 0.60, 0.30],
 [0.45, 0.40, 1.00, 0.35, 0.30],
 [0.65, 0.60, 0.35, 1.00, 0.40],
 [0.35, 0.30, 0.30, 0.40, 1.00]])
COV = np.outer(VOL, VOL) * CORR
RF  = 0.0425

def port_ret(w): return float(w @ EXP_RET)
def port_vol(w): return float(np.sqrt(w @ COV @ w))
def sharpe(w):   return (port_ret(w) - RF) / port_vol(w)

cons_sum = {"type":"eq","fun":lambda w: np.sum(w) - 1}
bounds   = [(0.0, 1.0)] * len(ASSETS)
x0       = np.ones(len(ASSETS)) / len(ASSETS)

# ---- efficient frontier ---------------------------------------------------
targets = np.linspace(EXP_RET.min(), EXP_RET.max(), 40)
frontier = []
for t in targets:
    cons = [cons_sum, {"type":"eq","fun":(lambda w, t=t: port_ret(w) - t)}]
    res = minimize(lambda w: port_vol(w), x0, bounds=bounds, constraints=cons,
                   method="SLSQP", options={"maxiter":500,"ftol":1e-10})
    if res.success:
        frontier.append({"target_return":float(t), "volatility":port_vol(res.x),
                         "weights":[float(x) for x in res.x]})

# ---- maximum-Sharpe and minimum-variance portfolios -----------------------
res_ms = minimize(lambda w: -sharpe(w), x0, bounds=bounds, constraints=[cons_sum],
                  method="SLSQP", options={"maxiter":500,"ftol":1e-10})
res_mv = minimize(lambda w: port_vol(w), x0, bounds=bounds, constraints=[cons_sum],
                  method="SLSQP", options={"maxiter":500,"ftol":1e-10})
max_sharpe_w, min_var_w = res_ms.x, res_mv.x

# ---- where does the actual policy portfolio sit? -------------------------
act_r, act_v, act_s = port_ret(ACTUAL), port_vol(ACTUAL), sharpe(ACTUAL)
# the efficient portfolio with the SAME return - how much volatility is
# being carried unnecessarily?
cons = [cons_sum, {"type":"eq","fun":lambda w: port_ret(w) - act_r}]
res_eq = minimize(lambda w: port_vol(w), x0, bounds=bounds, constraints=cons,
                  method="SLSQP", options={"maxiter":500,"ftol":1e-10})
eff_same_ret_vol = port_vol(res_eq.x)
vol_drag = act_v - eff_same_ret_vol

# ---- reverse optimisation: what returns does the actual mix imply? -------
# Black-Litterman style: if ACTUAL is optimal, implied excess returns are
# proportional to COV @ w. Solve for the risk-aversion that reproduces the
# observed portfolio return.
lam = (act_r - RF) / (ACTUAL @ COV @ ACTUAL)
implied_ret = RF + lam * (COV @ ACTUAL)

result = {
 "question": "Is Mubadala's disclosed 2025 asset-class mix efficient, and what does it imply?",
 "assets": ASSETS,
 "actual_weights_official": [float(x) for x in ACTUAL],
 "capital_market_assumptions": {
   "WARNING": "Author's assumptions. Mubadala publishes weights, not returns/vols/correlations.",
   "expected_return": [float(x) for x in EXP_RET],
   "volatility": [float(x) for x in VOL],
   "correlation_matrix": CORR.tolist(),
   "risk_free": RF},
 "actual_portfolio": {"expected_return": act_r, "volatility": act_v, "sharpe": act_s},
 "max_sharpe_portfolio": {"weights": dict(zip(ASSETS, [round(float(x),4) for x in max_sharpe_w])),
                          "expected_return": port_ret(max_sharpe_w),
                          "volatility": port_vol(max_sharpe_w),
                          "sharpe": sharpe(max_sharpe_w)},
 "min_variance_portfolio": {"weights": dict(zip(ASSETS, [round(float(x),4) for x in min_var_w])),
                            "expected_return": port_ret(min_var_w),
                            "volatility": port_vol(min_var_w),
                            "sharpe": sharpe(min_var_w)},
 "efficiency_test": {
   "efficient_volatility_at_same_return": eff_same_ret_vol,
   "actual_volatility": act_v,
   "excess_volatility_carried_pp": round(100*vol_drag, 2),
   "efficient_weights_at_same_return": dict(zip(ASSETS,[round(float(x),4) for x in res_eq.x]))},
 "reverse_optimisation": {
   "implied_risk_aversion": float(lam),
   "implied_expected_returns": dict(zip(ASSETS,[round(float(x),4) for x in implied_ret])),
   "reading": ("Treating the published mix as an optimal solution and inverting the "
               "optimisation tells us what return assumptions the allocator must hold. "
               "This is a cleaner way to interrogate an allocation than arguing about "
               "whether it is 'right'.")},
 "efficient_frontier": frontier,
}
with open(os.path.join(OUT,"portfolio_optimisation.json"),"w") as f:
    json.dump(result, f, indent=2)

print(f"Actual mix       return {act_r*100:5.2f}%   vol {act_v*100:5.2f}%   Sharpe {act_s:.3f}")
print(f"Max-Sharpe mix   return {port_ret(max_sharpe_w)*100:5.2f}%   vol {port_vol(max_sharpe_w)*100:5.2f}%   Sharpe {sharpe(max_sharpe_w):.3f}")
print(f"Min-var mix      return {port_ret(min_var_w)*100:5.2f}%   vol {port_vol(min_var_w)*100:5.2f}%   Sharpe {sharpe(min_var_w):.3f}")
print(f"\nEfficiency test: an efficient portfolio with the SAME {act_r*100:.2f}% return would carry")
print(f"  {eff_same_ret_vol*100:.2f}% volatility vs the actual {act_v*100:.2f}%  ->  {vol_drag*100:.2f}pp of avoidable risk")
print("\nMax-Sharpe weights:", {k: f"{v*100:.0f}%" for k,v in zip(ASSETS, max_sharpe_w)})
print("Implied returns from reverse optimisation:", {k: f"{v*100:.1f}%" for k,v in zip(ASSETS, implied_ret)})
