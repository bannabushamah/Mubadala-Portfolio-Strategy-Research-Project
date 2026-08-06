"""
CASE STUDY 2 - ENERGY
OMV Aktiengesellschaft (VIE: OMV)  -  Mubadala's 24.9% integrated energy stake

Method: 5-year FCFF DCF plus a dividend-sustainability test, cross-checked
against European integrated peers on P/E.

Two deliberate judgement calls are documented in the code below:
  (1) the raw 5-year beta of 0.21 is rejected in favour of a sector beta;
  (2) enterprise value is bridged for the large minority interests that arise
      because OMV fully consolidates Borealis/Borouge.
Market inputs as at 30 June 2026 (source: StockAnalysis / S&P Global).
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from valuation_engine import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs")
os.makedirs(OUT, exist_ok=True)

# ------------------------------------------------------------------ MARKET FACTS (EUR m unless noted)
PRICE      = 54.60
SHARES     = 326.0
MKT_CAP    = 17_620.0
EV_MARKET  = 24_160.0
GROSS_DEBT = 8_010.0
CASH       = 5_220.0
NET_DEBT   = GROSS_DEBT - CASH            # 2,790
# EV - market cap - net debt leaves the consolidated minority interest.
MINORITIES = EV_MARKET - MKT_CAP - NET_DEBT   # ~3,750
REV_TTM    = 23_378.0
EBITDA_TTM = 5_402.0
EBIT_TTM   = 3_509.0
DPS        = 4.40
RAW_BETA   = 0.21

# ------------------------------------------------------------------ COST OF CAPITAL
# JUDGEMENT: the observed 5-year beta of 0.21 implies OMV carries almost no
# systematic risk, which is not credible for an integrated oil and chemicals
# company. Thin free float (140.9m of 326m shares) and a domestic-index
# listing depress the measured covariance. We therefore substitute an
# industry beta of 0.90 for European integrated energy and disclose the swap.
SECTOR_BETA = 0.90
wacc_in = WACCInputs(
    risk_free=0.0275,            # assumption: 10y German Bund
    equity_risk_premium=0.055,   # assumption: eurozone ERP
    beta=SECTOR_BETA,
    extra_equity_premium=0.010,  # CEE / commodity-regime risk add-on
    cost_of_debt_pretax=0.045,
    tax_rate=0.30,               # normalised marginal rate; TTM effective 47.2%
    equity_value=MKT_CAP,
    debt_value=GROSS_DEBT,
)
WACC = round(wacc_in.wacc, 4)

# ------------------------------------------------------------------ FORECAST
# Volumes and refining margins normalise downward; chemicals recovers slowly.
# Capex steps down from the current elevated level as the Borouge 4 and
# ReOil investment cycle completes.
assump = DCFAssumptions(
    base_revenue=REV_TTM,
    revenue_growth   =[-0.03,  0.01,  0.02,  0.02,  0.02],
    ebit_margin      =[0.140, 0.145, 0.150, 0.150, 0.150],
    da_pct_revenue   =[0.080, 0.079, 0.078, 0.077, 0.076],
    capex_pct_revenue=[0.150, 0.135, 0.125, 0.118, 0.115],
    nwc_pct_delta_revenue=0.03,
    tax_rate=0.30,
    terminal_growth=0.010,     # below inflation: hydrocarbons are a declining pool
)

rows   = project_fcff(assump)
disc   = discount(rows, WACC, assump.terminal_growth, mid_year=True)
bridge = equity_bridge(disc["enterprise_value"], net_debt=NET_DEBT,
                       minorities=MINORITIES, shares=SHARES)
sens   = sensitivity_grid(assump, WACC, net_debt=NET_DEBT, shares=SHARES,
                          minorities=MINORITIES)

# ------------------------------------------------------------------ DIVIDEND TEST
# A 8.1% yield is only attractive if it is paid out of cash the business
# actually earns. We test cover across the last five reported years.
hist = [(2021,4520,2.30),(2022,4815,2.80),(2023,2222,2.95),(2024,1943,3.05),(2025,1366,3.15)]
div_test = [{"year":y, "fcf_eur_m":f, "dps_eur":d, "dividend_cost_eur_m":round(d*SHARES,0),
             "fcf_cover_x": round(f/(d*SHARES),2)} for y,f,d in hist]

# ------------------------------------------------------------------ COMPARABLES
pe_peers = {"Shell": 9.79, "TotalEnergies": 10.96, "Eni": 13.82, "BP": 20.86}
pe_stats = comps_stats(pe_peers, exclude_outliers=False)

# EARNINGS NORMALISATION - the single most important adjustment here.
# Reported TTM EPS of EUR 7.20 includes EUR 1,303m of earnings from
# DISCONTINUED operations. Capitalising that on a P/E multiple would value a
# business OMV no longer owns. FY2025 EPS of EUR 3.11 is equally unusable in
# the other direction because it absorbed EUR 497m of asset write-downs.
# We therefore use a three-year average of reported diluted EPS as a
# mid-cycle proxy.
EPS_TTM_REPORTED = 7.20
EPS_HISTORY      = {2023: 4.52, 2024: 4.24, 2025: 3.11}
EPS_NORMALISED   = round(sum(EPS_HISTORY.values())/len(EPS_HISTORY), 2)
comp_ps_median = pe_stats["median"] * EPS_NORMALISED
comp_ps_low    = pe_stats["min"]    * EPS_NORMALISED
comp_ps_high   = pe_stats["q3"]     * EPS_NORMALISED

result = {
 "case": "OMV Aktiengesellschaft (VIE: OMV)",
 "sector": "Energy & Sustainability - integrated oil, gas and chemicals",
 "mubadala_link": "24.9% strategic stake via Mubadala Petroleum & Petrochemicals Holding",
 "valuation_date": "2026-06-30",
 "market": {"price_eur": PRICE, "shares_m": SHARES, "market_cap_eur_m": MKT_CAP,
            "enterprise_value_eur_m": EV_MARKET, "net_debt_eur_m": NET_DEBT,
            "implied_minorities_eur_m": MINORITIES,
            "ev_ebitda_market": round(EV_MARKET/EBITDA_TTM,2),
            "dividend_per_share_eur": DPS,
            "dividend_yield_pct": round(100*DPS/PRICE,2)},
 "beta_judgement": {"raw_5y_beta": RAW_BETA, "beta_used": SECTOR_BETA,
    "rationale": "Raw beta of 0.21 is not economically credible for an integrated energy producer; thin free float and a domestic index listing suppress measured covariance. A European integrated-energy sector beta of 0.90 is substituted and disclosed."},
 "wacc": wacc_in.explain(),
 "assumptions": asdict(assump),
 "fcff_schedule": rows,
 "dcf": disc,
 "equity_bridge": bridge,
 "dcf_value_per_share": round(bridge["value_per_share"],2),
 "dcf_upside_pct": round(100*(bridge["value_per_share"]/PRICE-1),1),
 "sensitivity": sens,
 "dividend_sustainability": div_test,
 "dividend_conclusion": ("Free-cash-flow cover of the ordinary dividend has fallen from 6.0x in 2021 "
                         "to 1.3x in 2025 while the dividend per share has been raised every year. "
                         "The payout is still covered, but the margin of safety has largely gone; "
                         "a further leg down in refining or chemicals margins would force the "
                         "distribution to be funded from the balance sheet."),
 "comparables": {"pe_set": pe_peers, "pe_stats": pe_stats, "eps_ttm_reported_eur": EPS_TTM_REPORTED,
                 "eps_history": EPS_HISTORY,
                 "eps_normalised_eur": EPS_NORMALISED,
                 "normalisation_note": "TTM EPS of 7.20 includes EUR 1,303m from discontinued operations and is not a capitalisable earnings stream; FY2025 EPS of 3.11 absorbed EUR 497m of write-downs. A three-year average is used instead.",
                 "implied_value_per_share": {"low": round(comp_ps_low,2),
                                             "median": round(comp_ps_median,2),
                                             "high": round(comp_ps_high,2)},
                 "implied_upside_pct_median": round(100*(comp_ps_median/PRICE-1),1)},
 "football_field": {
     "DCF base": round(bridge["value_per_share"],2),
     "DCF low (WACC +1.5%, g -1.0%)": sens["values"][0][-1],
     "DCF high (WACC -1.5%, g +1.0%)": sens["values"][-1][0],
     "Comparables low (9.8x normalised P/E)": round(comp_ps_low,2),
     "Comparables median (12.4x normalised P/E)": round(comp_ps_median,2),
     "Comparables high (15.6x normalised P/E)": round(comp_ps_high,2),
     "Current market price": PRICE,
     "Sell-side consensus target": 61.00,
 },
}
with open(os.path.join(OUT,"case_02_omv.json"),"w") as f:
    json.dump(result, f, indent=2, default=float)

print(f"WACC                 {WACC*100:.2f}%   (Ke {wacc_in.cost_of_equity*100:.2f}%, beta {SECTOR_BETA} substituted for raw {RAW_BETA})")
print(f"Enterprise value     EUR {disc['enterprise_value']:,.0f}m  (terminal = {disc['terminal_pct_of_ev']*100:.0f}% of EV)")
print(f"less net debt        EUR {NET_DEBT:,.0f}m ; less minorities EUR {MINORITIES:,.0f}m")
print(f"DCF value/share      EUR {bridge['value_per_share']:.2f}  vs market EUR {PRICE:.2f}  ({result['dcf_upside_pct']:+.1f}%)")
print(f"Normalised EPS       EUR {EPS_NORMALISED:.2f}  (reported TTM {EPS_TTM_REPORTED:.2f} rejected: includes discontinued ops)")
print(f"Comps value/share    EUR {comp_ps_low:.2f} - {comp_ps_median:.2f} - {comp_ps_high:.2f}  (P/E {pe_stats['min']:.1f}x / {pe_stats['median']:.1f}x / {pe_stats['q3']:.1f}x)")
print("Dividend cover  " + " -> ".join(f"{d['year']}:{d['fcf_cover_x']}x" for d in div_test))
