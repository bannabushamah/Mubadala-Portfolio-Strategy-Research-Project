"""
CASE STUDY 4 - FINANCIAL SERVICES
Mubadala Capital  -  the wholly-owned alternative asset management subsidiary

Mubadala's own website states that Mubadala Capital "manages c. $30 billion in
aggregate between its own balance sheet investments and in third-party capital
vehicles ... across four businesses: Private Equity, Brazil, Venture Capital,
and Solutions."

That single disclosed number is the only hard input. Everything else is an
explicit, labelled assumption. The question we answer is a real one that a
sovereign investor's strategy team would ask:

   "If Mubadala Capital were a listed alternative asset manager, what would
    the market pay for it - and therefore how much value does the fee-earning
    franchise add on top of the investment returns it generates?"

Method: sum-of-the-parts on Fee-Related Earnings (FRE), benchmarked to the
listed alternative-manager cohort on price/sales and price/earnings.
"""
import json, os, numpy as np

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs")
os.makedirs(OUT, exist_ok=True)

# ------------------------------------------------------------------ THE ONE HARD FACT
TOTAL_AUM_BN = 30.0     # OFFICIAL - mubadala.com, "Our Structure"

# ------------------------------------------------------------------ ASSUMPTIONS (all labelled)
A = {
 "third_party_share_of_aum": 0.60,   # split between balance sheet and LP capital
 "management_fee_rate":      0.0120, # 1.20% blended on third-party fee-paying AUM
 "balance_sheet_fee_rate":   0.0000, # no fee charged on own capital
 "fre_margin":               0.35,   # fee-related earnings margin
 "tax_rate":                 0.00,   # UAE sovereign vehicle; shown for transparency
}

third_party_aum = TOTAL_AUM_BN * A["third_party_share_of_aum"]
balance_sheet_aum = TOTAL_AUM_BN - third_party_aum
mgmt_fee_revenue_m = third_party_aum * 1000 * A["management_fee_rate"]
fre_m = mgmt_fee_revenue_m * A["fre_margin"]

# ------------------------------------------------------------------ LISTED COHORT
peers = {
 "Blackstone (BX)":      {"mkt_cap_bn":169.49, "revenue_bn":15.48, "pe":30.51},
 "Apollo (APO)":         {"mkt_cap_bn": 75.06, "revenue_bn":35.60, "pe":81.92},
 "Ares (ARES)":          {"mkt_cap_bn": 46.56, "revenue_bn": 5.99, "pe":62.43},
 "Blue Owl (OWL)":       {"mkt_cap_bn": 17.80, "revenue_bn": 2.99, "pe":95.88},
 "TPG (TPG)":            {"mkt_cap_bn": 18.74, "revenue_bn": 3.73, "pe":139.03},
}
for k, v in peers.items():
    v["price_to_sales"] = round(v["mkt_cap_bn"] / v["revenue_bn"], 2)

ps = np.array([v["price_to_sales"] for v in peers.values()])
pe = np.array([v["pe"] for v in peers.values()])

ps_stats = {"min":float(ps.min()), "q1":float(np.percentile(ps,25)),
            "median":float(np.median(ps)), "mean":float(ps.mean()),
            "q3":float(np.percentile(ps,75)), "max":float(ps.max())}
pe_stats = {"min":float(pe.min()), "q1":float(np.percentile(pe,25)),
            "median":float(np.median(pe)), "mean":float(pe.mean()),
            "q3":float(np.percentile(pe,75)), "max":float(pe.max())}

# ------------------------------------------------------------------ APPLIED MULTIPLES
# Apollo's revenue line consolidates Athene's insurance premiums, so its 2.1x
# price/sales is not comparable to a pure fee stream. We disclose it and use
# the median of the remaining four for the applied range.
ps_applied = np.array([v["price_to_sales"] for k, v in peers.items() if "Apollo" not in k])

# A private, single-shareholder manager should trade below a listed compounder:
# no liquid currency for acquisitions, no public track record, concentrated
# client base. We apply a 25% private-company / control discount.
PRIVATE_DISCOUNT = 0.25

def value_from_ps(mult):  return mgmt_fee_revenue_m * mult / 1000      # USD bn
def value_from_pe(mult):  return fre_m * mult / 1000                   # USD bn

val = {
 "PS low  (5.0x fee revenue)":   value_from_ps(5.0),
 "PS median (peer ex-Apollo)":   value_from_ps(float(np.median(ps_applied))),
 "PS high (10.9x, Blackstone)":  value_from_ps(10.90),
 "PE cross-check (30.5x FRE, BX)": value_from_pe(30.51),
}
# The cohort MEDIAN P/E of 81.9x is reported for completeness but is NOT used
# to set the central value: it reflects listed managers whose earnings are
# temporarily depressed by performance-fee timing, which inflates the ratio.
val_reported_only = {"PE at cohort median (81.9x FRE) - reported, not applied":
                     value_from_pe(pe_stats["median"])}
central_bn = float(np.median(list(val.values())))
central_after_discount = central_bn * (1 - PRIVATE_DISCOUNT)

# ------------------------------------------------------------------ SENSITIVITY
fee_axis    = [0.0090, 0.0105, 0.0120, 0.0135, 0.0150]
ps_axis     = [4.0, 5.0, 6.0, 8.0, 10.0]
grid = [[round(third_party_aum*1000*f*m/1000*(1-PRIVATE_DISCOUNT), 2) for m in ps_axis]
        for f in fee_axis]

result = {
 "case": "Mubadala Capital",
 "sector": "Financial Services - alternative asset management",
 "mubadala_link": "Wholly-owned subsidiary within the Credit and Special Situations platform",
 "valuation_date": "2026-08-04",
 "hard_facts": {"aggregate_aum_usd_bn": TOTAL_AUM_BN,
                "businesses": ["Private Equity","Brazil","Venture Capital","Solutions"],
                "source": "mubadala.com - Our Structure (Official)"},
 "assumptions": A,
 "assumption_warning": "Every input except AUM is an author assumption. Mubadala Capital does not publish fee rates, FRE or margins. Treat the output as a framework, not a valuation opinion.",
 "derived": {"third_party_aum_usd_bn": round(third_party_aum,1),
             "balance_sheet_aum_usd_bn": round(balance_sheet_aum,1),
             "management_fee_revenue_usd_m": round(mgmt_fee_revenue_m,1),
             "fee_related_earnings_usd_m": round(fre_m,1)},
 "listed_cohort": peers,
 "cohort_stats": {"price_to_sales": ps_stats, "pe": pe_stats},
 "apollo_exclusion_note": "Apollo's reported revenue consolidates Athene's insurance premiums; its 2.1x price/sales is not comparable to a pure fee stream and is excluded from the applied range.",
 "valuation_range_usd_bn": {k: round(v,2) for k,v in val.items()},
 "reported_not_applied_usd_bn": {k: round(v,2) for k,v in val_reported_only.items()},
 "central_before_discount_usd_bn": round(central_bn,2),
 "private_company_discount": PRIVATE_DISCOUNT,
 "central_after_discount_usd_bn": round(central_after_discount,2),
 "as_pct_of_group_aum": round(100*central_after_discount/385.0, 2),
 "sensitivity_usd_bn": {"fee_rate_axis": fee_axis, "price_to_sales_axis": ps_axis, "grid": grid},
 "strategic_conclusion": (
    "On these assumptions the fee-earning franchise is worth roughly "
    f"US${central_after_discount:.1f}bn - about {100*central_after_discount/385.0:.1f}% of group AUM. "
    "The strategic point is not the number but the structure: Mubadala Capital converts "
    "third-party capital into a fee annuity that is valued on a multiple of earnings, "
    "on top of the investment return earned on Mubadala's own balance sheet. "
    "It is the only part of the group that creates value which is independent of "
    "the direction of asset prices."),
 "why_this_matters_to_the_strategy": [
   "Third-party capital lets Mubadala underwrite deals larger than its own balance sheet would allow.",
   "Fee income is counter-cyclical relative to realisations: it keeps paying when exit markets close.",
   "A visible franchise valuation gives the board a benchmark for whether to keep scaling it.",
 ],
}
with open(os.path.join(OUT,"case_04_mubadala_capital.json"),"w") as f:
    json.dump(result, f, indent=2, default=float)

print(f"AUM (official)           US${TOTAL_AUM_BN:.0f}bn  ->  third-party US${third_party_aum:.0f}bn")
print(f"Assumed fee revenue      US${mgmt_fee_revenue_m:.0f}m at {A['management_fee_rate']*100:.2f}%")
print(f"Assumed FRE              US${fre_m:.0f}m at {A['fre_margin']*100:.0f}% margin")
print("Peer price/sales:        " + ", ".join(f"{k.split()[0]} {v['price_to_sales']}x" for k,v in peers.items()))
for k,v in val.items(): print(f"  {k:36s} US${v:5.2f}bn")
for k,v in val_reported_only.items(): print(f"  {k:36s} US${v:5.2f}bn  [reported only]")
print(f"Central (median)         US${central_bn:.2f}bn  ->  US${central_after_discount:.2f}bn after {PRIVATE_DISCOUNT*100:.0f}% private-company discount")
