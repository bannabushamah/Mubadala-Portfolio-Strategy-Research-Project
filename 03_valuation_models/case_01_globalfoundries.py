"""
CASE STUDY 1 - TECHNOLOGY
GlobalFoundries Inc. (NASDAQ: GFS)  -  Mubadala's controlling technology asset

Method: 5-year FCFF DCF with Gordon terminal value, cross-checked against a
trading-comparables set of pure-play and specialty foundries.

All market inputs are as at 3-4 August 2026 (source: StockAnalysis /
S&P Global Market Intelligence). Forecast assumptions are the author's.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from valuation_engine import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs")
os.makedirs(OUT, exist_ok=True)

# ------------------------------------------------------------------ MARKET FACTS
PRICE      = 50.01      # USD, close 3 Aug 2026
SHARES     = 548.70     # millions
MKT_CAP    = 27_440.0   # USD m
EV_MARKET  = 25_400.0   # USD m  (published enterprise value)
NET_CASH   = MKT_CAP - EV_MARKET     # 2,040 -> the market's own bridge
GROSS_DEBT = 1_724.0
REV_TTM    = 6_840.0
EBIT_TTM   = 826.0
EBITDA_TTM = 2_100.0
BETA       = 1.76

# ------------------------------------------------------------------ COST OF CAPITAL
# Risk-free and ERP are stated assumptions, not observed data.
wacc_in = WACCInputs(
    risk_free=0.0425,            # assumption: 10y US Treasury
    equity_risk_premium=0.050,   # assumption: mature-market ERP
    beta=BETA,                   # observed 5y beta
    extra_equity_premium=0.000,
    cost_of_debt_pretax=0.055,   # assumption, consistent with IG credit
    tax_rate=0.15,               # normalised; TTM effective rate was 13.3%
    equity_value=MKT_CAP,
    debt_value=GROSS_DEBT,
)
WACC = round(wacc_in.wacc, 4)

# ------------------------------------------------------------------ FORECAST
# Revenue: consensus 3-year revenue CAGR is 10.1%. We front-load a cyclical
# recovery then fade toward GDP-plus.
# Margins: management has publicly targeted 40% gross margin by 2028 and 45%
# by 2030 (Q2-26 conference commentary). Gross margin was 26.1% TTM, so we
# model steady operating leverage without assuming the full target is met.
assump = DCFAssumptions(
    base_revenue=REV_TTM,
    revenue_growth   =[0.08, 0.10, 0.10, 0.07, 0.05],
    ebit_margin      =[0.130, 0.150, 0.170, 0.190, 0.200],
    da_pct_revenue   =[0.170, 0.165, 0.160, 0.155, 0.150],
    capex_pct_revenue=[0.130, 0.135, 0.135, 0.130, 0.125],
    nwc_pct_delta_revenue=0.02,
    tax_rate=0.15,
    terminal_growth=0.025,
)

rows = project_fcff(assump)
disc = discount(rows, WACC, assump.terminal_growth, mid_year=True)
bridge = equity_bridge(disc["enterprise_value"], net_debt=-NET_CASH,
                       shares=SHARES)          # negative net debt = net cash
sens = sensitivity_grid(assump, WACC, net_debt=-NET_CASH, shares=SHARES)

# ------------------------------------------------------------------ COMPARABLES
# Peer set = listed foundries and specialty analog/mixed-signal manufacturers.
# Tower Semiconductor trades on 90.8x EV/EBITDA and 92.7x earnings after a
# +425% twelve-month re-rating. Including it would not tell us what a foundry
# is worth; it would tell us what a momentum stock is worth. It is therefore
# reported but formally EXCLUDED from the applied range, and the exclusion is
# stated rather than hidden.
ev_ebitda_peers   = {"UMC": 14.53, "TSEM": 90.77}
ev_ebitda_applied = {"UMC": 14.53}          # closest pure-play mature-node comp
pe_peers          = {"UMC": 17.40, "TSM": 26.56, "ON": 51.93, "TSEM": 92.65}
pe_applied        = {"UMC": 17.40, "TSM": 26.56, "ON": 51.93}

ev_stats = comps_stats(ev_ebitda_peers, exclude_outliers=False)
pe_stats = comps_stats(pe_applied, exclude_outliers=False)

# Applied EV/EBITDA range: anchor on UMC, band +/- 2.5 turns for the fact that
# GFS has lower margins but stronger Western-fab strategic scarcity value.
ev_low, ev_mid, ev_high = 11.0, 14.5, 17.0
def ps_from_multiple(m):
    return (m * EBITDA_TTM + NET_CASH) / SHARES
comp_low, comp_mid, comp_high = ps_from_multiple(ev_low), ps_from_multiple(ev_mid), ps_from_multiple(ev_high)

# ------------------------------------------------------------------ REVERSE DCF
# The base-case DCF lands well below the traded price. Rather than declare the
# market wrong, we invert the model: what steady-state EBIT margin would the
# business have to reach to justify the current share price on our other
# assumptions? This turns a disagreement into a testable statement.
def value_for_terminal_margin(term_margin):
    a2 = DCFAssumptions(
        base_revenue=REV_TTM,
        revenue_growth=assump.revenue_growth,
        ebit_margin=[0.130, 0.150,
                     0.150 + (term_margin-0.150)*0.34,
                     0.150 + (term_margin-0.150)*0.67,
                     term_margin],
        da_pct_revenue=assump.da_pct_revenue,
        capex_pct_revenue=assump.capex_pct_revenue,
        nwc_pct_delta_revenue=assump.nwc_pct_delta_revenue,
        tax_rate=assump.tax_rate,
        terminal_growth=assump.terminal_growth)
    d2 = discount(project_fcff(a2), WACC, a2.terminal_growth)
    return equity_bridge(d2["enterprise_value"], -NET_CASH, shares=SHARES)["value_per_share"]

lo, hi = 0.10, 0.60
for _ in range(60):
    mid = (lo + hi) / 2
    if value_for_terminal_margin(mid) < PRICE: lo = mid
    else: hi = mid
implied_terminal_margin = (lo + hi) / 2

result = {
 "case": "GlobalFoundries Inc. (NASDAQ: GFS)",
 "sector": "Technology - specialty semiconductor foundry",
 "mubadala_link": "Controlling shareholder (~80%) via Mubadala Technology Investment Company",
 "valuation_date": "2026-08-04",
 "market": {"price": PRICE, "shares_m": SHARES, "market_cap_usd_m": MKT_CAP,
            "enterprise_value_usd_m": EV_MARKET, "net_cash_usd_m": NET_CASH,
            "revenue_ttm_usd_m": REV_TTM, "ebitda_ttm_usd_m": EBITDA_TTM,
            "ev_ebitda_market": round(EV_MARKET/EBITDA_TTM,2)},
 "wacc": wacc_in.explain(),
 "assumptions": asdict(assump),
 "fcff_schedule": rows,
 "dcf": disc,
 "equity_bridge": bridge,
 "dcf_value_per_share": round(bridge["value_per_share"], 2),
 "dcf_upside_pct": round(100*(bridge["value_per_share"]/PRICE - 1), 1),
 "sensitivity": sens,
 "comparables": {"ev_ebitda_set": ev_ebitda_peers, "ev_ebitda_stats": ev_stats,
                 "pe_set": pe_peers, "pe_stats": pe_stats,
                 "excluded_from_applied_range": ["TSEM"],
                 "exclusion_rationale": "Tower Semiconductor trades on 90.8x EV/EBITDA after a +425% 12-month re-rating; including it would distort the central tendency of the peer group.",
                 "applied_ev_ebitda_range": {"low": ev_low, "mid": ev_mid, "high": ev_high},
                 "implied_value_per_share": {"low": round(comp_low,2), "mid": round(comp_mid,2), "high": round(comp_high,2)},
                 "implied_upside_pct_mid": round(100*(comp_mid/PRICE-1),1)},
 "reverse_dcf": {
     "question": "What steady-state EBIT margin does the current $50.01 share price require?",
     "implied_terminal_ebit_margin": round(implied_terminal_margin,4),
     "base_case_terminal_ebit_margin": assump.ebit_margin[-1],
     "ttm_ebit_margin": round(EBIT_TTM/REV_TTM,4),
     "interpretation": "The market is underwriting a structurally higher through-cycle margin than our base case, consistent with capitalising silicon-photonics, quantum and automotive content that is not yet in the reported numbers."},
 "football_field": {
     "DCF base": round(bridge["value_per_share"],2),
     "DCF low (WACC +1.5%, g -1.0%)": sens["values"][0][-1],
     "DCF high (WACC -1.5%, g +1.0%)": sens["values"][-1][0],
     "Comparables low (11.0x EV/EBITDA)": round(comp_low,2),
     "Comparables mid (14.5x EV/EBITDA)": round(comp_mid,2),
     "Comparables high (17.0x EV/EBITDA)": round(comp_high,2),
     "Current market price": PRICE,
     "Sell-side consensus target": 80.24,
 },
}

with open(os.path.join(OUT, "case_01_globalfoundries.json"), "w") as f:
    json.dump(result, f, indent=2, default=float)

print(f"WACC                 {WACC*100:.2f}%")
print(f"Enterprise value     ${disc['enterprise_value']:,.0f}m  (terminal = {disc['terminal_pct_of_ev']*100:.0f}% of EV)")
print(f"Equity value         ${bridge['equity_value']:,.0f}m")
print(f"DCF value/share      ${bridge['value_per_share']:.2f}   vs market ${PRICE:.2f}  ({result['dcf_upside_pct']:+.1f}%)")
print(f"Comps value/share    ${comp_low:.2f} - ${comp_mid:.2f} - ${comp_high:.2f}  (11.0x / 14.5x / 17.0x EV/EBITDA)")
print(f"Reverse DCF          market price implies a {implied_terminal_margin*100:.1f}% steady-state EBIT margin (base case {assump.ebit_margin[-1]*100:.0f}%, TTM {EBIT_TTM/REV_TTM*100:.1f}%)")
