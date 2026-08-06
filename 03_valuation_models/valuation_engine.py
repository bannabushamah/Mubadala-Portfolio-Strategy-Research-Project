"""
valuation_engine.py
Reusable valuation primitives: WACC build-up, FCFF projection, discounting,
Gordon terminal value, sensitivity grids and football-field summarisation.

Everything is plain Python + numpy so a reader can follow the arithmetic line
by line. No black boxes.
"""
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional
import numpy as np


# ----------------------------------------------------------------- COST OF CAPITAL
@dataclass
class WACCInputs:
    risk_free: float            # e.g. 0.0425
    equity_risk_premium: float  # e.g. 0.050
    beta: float                 # levered equity beta actually used
    extra_equity_premium: float = 0.0   # country / size / illiquidity add-on
    cost_of_debt_pretax: float = 0.055
    tax_rate: float = 0.15
    equity_value: float = 1.0   # market cap, any consistent unit
    debt_value: float = 0.0     # gross debt, same unit

    @property
    def cost_of_equity(self) -> float:
        # CAPM: Ke = Rf + beta * ERP (+ judgemental add-on)
        return self.risk_free + self.beta * self.equity_risk_premium + self.extra_equity_premium

    @property
    def cost_of_debt_after_tax(self) -> float:
        return self.cost_of_debt_pretax * (1 - self.tax_rate)

    @property
    def weight_equity(self) -> float:
        return self.equity_value / (self.equity_value + self.debt_value)

    @property
    def weight_debt(self) -> float:
        return 1 - self.weight_equity

    @property
    def wacc(self) -> float:
        return (self.weight_equity * self.cost_of_equity
                + self.weight_debt * self.cost_of_debt_after_tax)

    def explain(self) -> Dict[str, float]:
        return {
            "risk_free": self.risk_free,
            "beta_used": self.beta,
            "equity_risk_premium": self.equity_risk_premium,
            "extra_equity_premium": self.extra_equity_premium,
            "cost_of_equity": self.cost_of_equity,
            "cost_of_debt_pretax": self.cost_of_debt_pretax,
            "tax_rate": self.tax_rate,
            "cost_of_debt_after_tax": self.cost_of_debt_after_tax,
            "weight_equity": self.weight_equity,
            "weight_debt": self.weight_debt,
            "wacc": self.wacc,
        }


# ----------------------------------------------------------------- FCFF PROJECTION
@dataclass
class DCFAssumptions:
    base_revenue: float
    revenue_growth: List[float]     # one entry per explicit forecast year
    ebit_margin: List[float]
    da_pct_revenue: List[float]
    capex_pct_revenue: List[float]
    nwc_pct_delta_revenue: float    # working capital investment per $1 of new revenue
    tax_rate: float
    terminal_growth: float


def project_fcff(a: DCFAssumptions) -> List[Dict[str, float]]:
    """Build the free-cash-flow-to-firm schedule.

    FCFF = EBIT x (1 - tax) + D&A - capex - change in net working capital
    We use FCFF (not FCFE) because it values the whole enterprise independent
    of the capital structure, which is the right lens when the shareholder is
    a sovereign investor that could refinance the business at will.
    """
    rows, rev_prev = [], a.base_revenue
    for i, g in enumerate(a.revenue_growth):
        rev   = rev_prev * (1 + g)
        ebit  = rev * a.ebit_margin[i]
        nopat = ebit * (1 - a.tax_rate)
        da    = rev * a.da_pct_revenue[i]
        capex = rev * a.capex_pct_revenue[i]
        dnwc  = (rev - rev_prev) * a.nwc_pct_delta_revenue
        fcff  = nopat + da - capex - dnwc
        rows.append(dict(year=i + 1, revenue=rev, growth=g, ebit=ebit,
                         ebit_margin=a.ebit_margin[i], nopat=nopat, da=da,
                         capex=capex, delta_nwc=dnwc, fcff=fcff))
        rev_prev = rev
    return rows


def discount(rows: List[Dict[str, float]], wacc: float, terminal_growth: float,
             mid_year: bool = True) -> Dict[str, float]:
    """Discount the explicit FCFF and a Gordon-growth terminal value.

    mid_year convention assumes cash arrives evenly through the year rather
    than all on 31 December. It lifts the value by roughly (1+WACC)^0.5 and is
    standard in banking models.
    """
    pv_explicit, disc_factors = 0.0, []
    for r in rows:
        t = r["year"] - (0.5 if mid_year else 0.0)
        df = 1 / (1 + wacc) ** t
        disc_factors.append(df)
        r["discount_factor"] = df
        r["pv_fcff"] = r["fcff"] * df
        pv_explicit += r["pv_fcff"]

    fcff_n = rows[-1]["fcff"]
    tv = fcff_n * (1 + terminal_growth) / (wacc - terminal_growth)
    t_last = rows[-1]["year"] - (0.5 if mid_year else 0.0)
    pv_tv = tv / (1 + wacc) ** t_last
    ev = pv_explicit + pv_tv
    return {"pv_explicit": pv_explicit, "terminal_value": tv, "pv_terminal": pv_tv,
            "enterprise_value": ev, "terminal_pct_of_ev": pv_tv / ev}


def equity_bridge(ev: float, net_debt: float, minorities: float = 0.0,
                  associates: float = 0.0, shares: float = 1.0) -> Dict[str, float]:
    """EV -> equity value per share.
    Equity = EV - net debt - minority interests + value of associates
    """
    eq = ev - net_debt - minorities + associates
    return {"enterprise_value": ev, "less_net_debt": -net_debt,
            "less_minorities": -minorities, "plus_associates": associates,
            "equity_value": eq, "shares": shares, "value_per_share": eq / shares}


def sensitivity_grid(a: DCFAssumptions, base_wacc: float, net_debt: float,
                     shares: float, minorities: float = 0.0,
                     wacc_range=(-0.015, 0.015), g_range=(-0.010, 0.010),
                     steps: int = 5) -> Dict:
    """Classic two-way WACC x terminal-growth sensitivity table."""
    waccs = np.linspace(base_wacc + wacc_range[0], base_wacc + wacc_range[1], steps)
    gs    = np.linspace(a.terminal_growth + g_range[0],
                        a.terminal_growth + g_range[1], steps)
    grid = []
    for g in gs:
        row = []
        for wc in waccs:
            if wc <= g + 0.005:          # guard against a meaningless denominator
                row.append(float("nan")); continue
            rows = project_fcff(a)
            d = discount(rows, wc, g)
            row.append(equity_bridge(d["enterprise_value"], net_debt,
                                     minorities, shares=shares)["value_per_share"])
        grid.append(row)
    return {"wacc_axis": [round(float(x), 4) for x in waccs],
            "growth_axis": [round(float(x), 4) for x in gs],
            "values": [[None if np.isnan(v) else round(float(v), 2) for v in r] for r in grid]}


# ----------------------------------------------------------------- COMPARABLES
def comps_stats(multiples: Dict[str, float], exclude_outliers: bool = True,
                z_threshold: float = 1.75) -> Dict:
    """Median / mean of a peer multiple set, with optional outlier screening.

    Why median first? Multiples are bounded below at zero but unbounded above,
    so a single re-rating name (a Tower Semiconductor on 90x EV/EBITDA) drags
    the mean far away from where the typical peer trades.
    """
    names = list(multiples.keys())
    vals = np.array([multiples[n] for n in names], dtype=float)
    kept, dropped = names, []
    if exclude_outliers and len(vals) > 3:
        med = np.median(vals)
        mad = np.median(np.abs(vals - med)) or 1e-9
        z = 0.6745 * (vals - med) / mad          # robust modified z-score
        keep_mask = np.abs(z) < z_threshold * 3
        dropped = [n for n, k in zip(names, keep_mask) if not k]
        kept    = [n for n, k in zip(names, keep_mask) if k]
        vals    = vals[keep_mask]
    return {"n": len(vals), "min": float(vals.min()), "q1": float(np.percentile(vals, 25)),
            "median": float(np.median(vals)), "mean": float(vals.mean()),
            "q3": float(np.percentile(vals, 75)), "max": float(vals.max()),
            "kept": kept, "dropped_as_outliers": dropped}
