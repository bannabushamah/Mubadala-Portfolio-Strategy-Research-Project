"""
CASE STUDY 3 - HEALTHCARE
WHOOP Inc.  -  Series G, US$575m raised at a US$10.1bn post-money valuation
               (31 March 2026; Mubadala a participating investor)

Private companies do not publish accounts, so a conventional forward DCF would
be an exercise in inventing numbers. Instead we run the model BACKWARDS:
we take the price the market of sophisticated investors actually paid and ask
what future it embeds. This is the "expectations investing" / reverse-DCF
approach, and it is honest about what is known versus assumed.

KNOWN (Mubadala press release, 31 Mar 2026):
  - post-money valuation US$10.1bn
  - round size US$575m
  - 2.5m+ members
  - 2025 bookings growth +103% YoY, exiting 2025 at a US$1.1bn run-rate
  - operating cash-flow positive in 2025
ASSUMED (flagged throughout): discount rate, margin path, terminal multiple.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs")
os.makedirs(OUT, exist_ok=True)

# ------------------------------------------------------------------ KNOWN FACTS
POST_MONEY   = 10_100.0      # USD m
ROUND_SIZE   = 575.0
PRE_MONEY    = POST_MONEY - ROUND_SIZE
RUN_RATE_REV = 1_100.0       # exit-2025 bookings run-rate
MEMBERS_M    = 2.5
GROWTH_2025  = 1.03

# Implied entry multiple. Post-money includes the cash just raised, so the
# operating business is being valued at the pre-money figure.
ev_rev_post = POST_MONEY / RUN_RATE_REV
ev_rev_pre  = PRE_MONEY  / RUN_RATE_REV
rev_per_member = RUN_RATE_REV / MEMBERS_M          # USD m per m members = USD per member per year

# ------------------------------------------------------------------ REVERSE DCF
DISCOUNT_RATE   = 0.18       # ASSUMPTION: late-stage private required return
TERMINAL_GROWTH = 0.035      # ASSUMPTION
HORIZON         = 10         # years
TERMINAL_FCF_MARGIN = 0.20   # ASSUMPTION: mature subscription-hardware margin

def value_at_cagr(cagr, fcf_margin=TERMINAL_FCF_MARGIN, r=DISCOUNT_RATE,
                  g=TERMINAL_GROWTH, horizon=HORIZON):
    """Value the business if revenue compounds at `cagr` for `horizon` years
    with the FCF margin ramping linearly from ~4% today to `fcf_margin`."""
    rev, pv = RUN_RATE_REV, 0.0
    for t in range(1, horizon + 1):
        rev *= (1 + cagr)
        margin = 0.04 + (fcf_margin - 0.04) * (t / horizon)
        fcf = rev * margin
        pv += fcf / (1 + r) ** t
    terminal_fcf = rev * fcf_margin * (1 + g)
    tv = terminal_fcf / (r - g)
    pv += tv / (1 + r) ** horizon
    return pv

# Solve for the revenue CAGR that reproduces the actual price paid.
lo, hi = 0.0, 1.5
for _ in range(80):
    mid = (lo + hi) / 2
    if value_at_cagr(mid) < PRE_MONEY: lo = mid
    else: hi = mid
implied_cagr = (lo + hi) / 2
implied_rev_yr10 = RUN_RATE_REV * (1 + implied_cagr) ** HORIZON

# ------------------------------------------------------------------ SCENARIOS
scenarios = {}
for name, (cagr, margin, r) in {
    "Bear - growth fades to 12%, margin caps at 12%": (0.12, 0.12, 0.20),
    "Base - reverse-DCF solution":               (implied_cagr, 0.20, 0.18),
    "Bull - platform economics, 25% margin":     (0.42, 0.25, 0.16),
}.items():
    v = value_at_cagr(cagr, margin, r)
    scenarios[name] = {
        "revenue_cagr": round(cagr, 4),
        "terminal_fcf_margin": margin,
        "discount_rate": r,
        "revenue_year10_usd_m": round(RUN_RATE_REV*(1+cagr)**HORIZON, 0),
        "value_usd_m": round(v, 0),
        "vs_pre_money_pct": round(100*(v/PRE_MONEY - 1), 1),
    }

# ------------------------------------------------------------------ MULTIPLE CHECK
# What do quality listed healthcare/life-science platforms trade on?
listed = {"Thermo Fisher": {"mkt_cap_bn":209.27,"rev_bn":46.34},
          "West Pharmaceutical": {"mkt_cap_bn":24.33,"rev_bn":3.33},
          "Agilent": {"mkt_cap_bn":39.20,"rev_bn":7.23},
          "ICON plc": {"mkt_cap_bn":12.08,"rev_bn":8.29},
          "Charles River": {"mkt_cap_bn":11.32,"rev_bn":4.03}}
for k,v in listed.items():
    v["price_to_sales"] = round(v["mkt_cap_bn"]/v["rev_bn"], 2)
ps_values = sorted(v["price_to_sales"] for v in listed.values())
ps_median = float(np.median(ps_values))

# ------------------------------------------------------------------ SENSITIVITY
cagr_axis   = [0.10,0.15,0.20,0.25,0.30,0.35]
margin_axis = [0.12,0.16,0.20,0.24,0.28]
grid = [[round(value_at_cagr(c, m)/1000, 2) for c in cagr_axis] for m in margin_axis]

result = {
 "case": "WHOOP Inc. (private)",
 "sector": "Healthcare & Life Sciences - AI-enabled continuous biometrics",
 "mubadala_link": "Participating investor in the March 2026 Series G; separate UAE preventative-health partnership announced 2026",
 "valuation_date": "2026-03-31",
 "known_facts": {"post_money_usd_m": POST_MONEY, "round_size_usd_m": ROUND_SIZE,
                 "pre_money_usd_m": PRE_MONEY, "run_rate_revenue_usd_m": RUN_RATE_REV,
                 "members_m": MEMBERS_M, "bookings_growth_2025_pct": 103.0,
                 "cash_flow_positive_2025": True,
                 "source": "Mubadala press release, 31 March 2026"},
 "implied_entry_multiples": {"ev_revenue_post_money": round(ev_rev_post,2),
                             "ev_revenue_pre_money": round(ev_rev_pre,2),
                             "revenue_per_member_usd": round(rev_per_member,0)},
 "reverse_dcf": {
     "method": "Solve for the revenue CAGR that makes a 10-year DCF equal the price actually paid",
     "assumptions": {"discount_rate": DISCOUNT_RATE, "terminal_growth": TERMINAL_GROWTH,
                     "horizon_years": HORIZON, "terminal_fcf_margin": TERMINAL_FCF_MARGIN,
                     "starting_fcf_margin": 0.04},
     "implied_revenue_cagr": round(implied_cagr, 4),
     "implied_revenue_year10_usd_m": round(implied_rev_yr10, 0),
     "implied_revenue_year10_usd_bn": round(implied_rev_yr10/1000, 2),
     "interpretation": (f"The Series G price requires revenue to compound at "
        f"{implied_cagr*100:.1f}% a year for a decade, reaching about "
        f"US${implied_rev_yr10/1000:.1f}bn by 2035, with free-cash-flow margins "
        f"reaching {TERMINAL_FCF_MARGIN*100:.0f}%. That is demanding but not absurd "
        f"against 2025 bookings growth of 103%; the question is durability, not direction.")},
 "scenarios": scenarios,
 "listed_reference_multiples": {"peers": listed, "median_price_to_sales": round(ps_median,2),
     "whoop_price_to_sales_pre_money": round(ev_rev_pre,2),
     "premium_to_listed_median_x": round(ev_rev_pre/ps_median,2),
     "note": "WHOOP is priced at a large premium to listed healthcare platforms. That premium is the market paying for growth rate and data-asset optionality, not for current profitability."},
 "sensitivity_value_usd_bn": {"revenue_cagr_axis": cagr_axis,
                              "terminal_fcf_margin_axis": margin_axis,
                              "grid": grid},
 "key_risks": [
   "Consumer subscription churn is the single biggest swing factor and is not disclosed.",
   "Hardware refresh cycles create lumpy working capital that a revenue-multiple lens hides.",
   "Competitive encroachment from Apple, Samsung and Oura on the same wrist.",
   "Regulatory reclassification of predictive health features as medical devices.",
   "A 9.2x revenue entry multiple leaves no margin for a growth disappointment."],
}
with open(os.path.join(OUT,"case_03_whoop.json"),"w") as f:
    json.dump(result, f, indent=2, default=float)

print(f"Post-money US${POST_MONEY/1000:.1f}bn on US${RUN_RATE_REV/1000:.1f}bn run-rate = {ev_rev_post:.1f}x revenue ({ev_rev_pre:.1f}x pre-money)")
print(f"Revenue per member US${rev_per_member:,.0f}/yr")
print(f"Reverse DCF: price implies {implied_cagr*100:.1f}% revenue CAGR for 10 years -> US${implied_rev_yr10/1000:.1f}bn revenue by 2035")
for k,v in scenarios.items():
    print(f"  {k:44s} US${v['value_usd_m']/1000:5.1f}bn  ({v['vs_pre_money_pct']:+.0f}% vs price paid)")
print(f"Listed healthcare platform median P/S {ps_median:.1f}x -> WHOOP at {ev_rev_pre:.1f}x is a {ev_rev_pre/ps_median:.1f}x premium")
