"""
The household condition engine. Executes SPECIFICATION.md exactly.

A structural identity worth stating up front. Required payments are FIXED in
nominal terms (section 2), so for household i

    PTI_after > PTI_before   <=>   income_after < income_before

The "whose payment-to-income ratio rises" test is therefore an INCOME INCIDENCE
test. Payments still matter for the threshold crossings of section 5.3, which
depend on levels, but the rising test does not depend on them at all. This is a
property of the specification, not a shortcut, and it is reported.

Accrual basis, reading recorded (DEVIATIONS D3). Section 4.2 says the whole
capital gain is counted as income "at a stated annuity rate applied to the
wealth increment". The shift of section 2 moves an income FLOW. Capitalising a
flow at rate a and then annuitising the resulting wealth at the same rate a
returns the flow. The accrual basis therefore counts the whole household-reaching
gain as income, and the annuity rate cancels; it bites only where a STOCK of
equity is converted into an income stream, which is the universal fund (7.2) and
broadened retirement ownership (7.3).
"""
from pathlib import Path
import io
import zipfile
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "household_condition"
OUT = ROOT / "framework" / "household_condition"

# ---- grids, fixed by SPECIFICATION section 2 ------------------------------
S_GRID = np.array([0.01, 0.02, 0.05, 0.10, 0.15, 0.20, 0.25])
G_GRID = np.round(np.arange(0, 0.20001, 0.0025), 6)

R_RETAINED = 0.568316                     # measurement paper
R_SENS = [0.568316, 0.70, 0.85]           # section 8.2
ANNUITY = {"central": 0.04, "low": 0.02, "high": 0.06}
KAPPA = {"cash_flow": 0.27, "accrual": 0.52, "counterfactual": 1.00}
ALLOCATIONS = ["proportional", "concentrated", "quintile"]
OWNERSHIP = {
    "direct": ["stocks", "nmmf"],
    "direct_business": ["stocks", "nmmf", "bus"],
    "all_routes": ["stocks", "nmmf", "bus", "retqliq", "annuit"],
}
BASES = ["cash_flow", "accrual"]
THRESHOLDS = {"pir40": 0.40, "dti36": 0.36, "qm43": 0.43, "du50": 0.50}
PRIMARY = dict(allocation="concentrated", ownership="all_routes",
               basis="cash_flow", kappa="cash_flow", threshold="pir40")

QUINTILE_WAGE_SHARE = np.array([0.0324, 0.0895, 0.1426, 0.2233, 0.5122])

DEBT_CLASSES = ["mortgage", "credit_card", "vehicle", "education",
                "other_install", "other"]
# SCF-to-official under-reporting factors, FEASIBILITY section 4
UR_FACTOR = {"mortgage": 1.113, "credit_card": 3.734, "vehicle": 1.768,
             "education": 1.232, "other_install": 1.659, "other": 1.659}

EXPOSURE_CASES = ["cognitive_AIOE", "cognitive_GPT", "embodied"]


def wpct(x, w):
    o = np.argsort(np.asarray(x), kind="stable")
    cw = np.cumsum(np.asarray(w)[o]) / np.asarray(w).sum()
    p = np.empty(len(x))
    p[o] = cw
    return p


def load(year=2022):
    z = zipfile.ZipFile(RAW / f"scfp{year}s.zip")
    return pd.read_stata(io.BytesIO(z.read(z.namelist()[0])))


def prepare(df):
    """Baseline frame. No shift applied."""
    d = df.copy()
    d["wgt5"] = d["wgt"] * 5
    d["imp"] = d["y1"] % 10
    d["other_inc"] = d["ssretinc"] + d["transfothinc"]
    d["inc"] = d["income"]
    d["oth_install"] = (d["install"] - d["veh_inst"]
                        - d["edn_inst"]).clip(lower=0)
    d["debt_mortgage"] = d["mrthel"]
    d["debt_credit_card"] = d["ccbal"]
    d["debt_vehicle"] = d["veh_inst"]
    d["debt_education"] = d["edn_inst"]
    d["debt_other_install"] = d["oth_install"]
    d["debt_other"] = d["odebt"] + d["othloc"] + d["resdbt"]
    d["debt_total"] = d[[f"debt_{k}" for k in DEBT_CLASSES]].sum(axis=1)
    d["valid"] = d["inc"] > 0
    d["pti"] = np.where(d["valid"], d["tpay"] / d["inc"].replace(0, np.nan),
                        np.nan)
    for name, cols in OWNERSHIP.items():
        d[f"own_{name}"] = sum(d[c].clip(lower=0) for c in cols)   # D1
    d["wq"] = pd.cut(wpct(d["wageinc"], d["wgt5"]), [0, .2, .4, .6, .8, 1.0],
                     labels=[1, 2, 3, 4, 5], include_lowest=True)
    d["wealth_grp"] = pd.cut(
        wpct(d["networth"], d["wgt5"]), [0, .25, .50, .75, .90, .99, 1.0],
        labels=["p0-25", "p25-50", "p50-75", "p75-90", "p90-99", "top1"],
        include_lowest=True)
    return d


def wage_loss(d, s, allocation, exposure_case="cognitive_AIOE",
              r_retained=R_RETAINED):
    """Delta_i. Sums to s*W over the implicate."""
    w = d["wageinc"].clip(lower=0).to_numpy()
    wt = d["wgt5"].to_numpy()
    W = float((w * wt).sum())
    target = s * W

    if allocation == "proportional":
        return s * w

    if allocation == "quintile":
        # The SCF's bottom wage quintile has NO wage income at all (the bottom
        # fifth of households by wage income are non-earners), so the paper's
        # Q1 share of 0.0324 cannot be placed. Section 9 bound 3 requires the
        # loss to sum to s*W, so the shares are renormalised over quintiles
        # with a positive wage bill. DEVIATIONS D5; affected results marked.
        delta = np.zeros(len(d))
        q = d["wq"].to_numpy()
        qw = np.array([float((w[q == k + 1] * wt[q == k + 1]).sum())
                       for k in range(5)])
        live = qw > 0
        shares = np.where(live, QUINTILE_WAGE_SHARE, 0.0)
        shares = shares / shares.sum()
        for k in range(5):
            if live[k]:
                delta[q == k + 1] = (target * shares[k] / qw[k]) * w[q == k + 1]
        return delta

    if allocation == "concentrated":
        occ = d["occat2"].to_numpy()
        if exposure_case.startswith("cognitive"):
            order = [(occ == 1), (occ == 2), (occ == 3)]
        else:
            order = [(occ == 3), (occ == 2), (occ == 1)]
        loss_rate = 1.0 - r_retained
        delta = np.zeros(len(d))
        placed = 0.0
        for grp in order:
            grp = grp & (w > 0)
            if not grp.any():
                continue
            cap = float((loss_rate * w[grp] * wt[grp]).sum())
            remaining = target - placed
            if remaining <= 0:
                break
            if cap >= remaining:
                frac = remaining / cap
                delta[grp] = loss_rate * w[grp] * frac
                placed += remaining
                break
            delta[grp] = loss_rate * w[grp]
            placed += cap
        return delta

    raise ValueError(allocation)


def cap_and_redistribute(d, delta, gam, target):
    """Section 9 bounds 3 and 5 conflict for the 121 valid households whose
    wage income exceeds their total income (negative business income): the
    loss can drive income below zero. Bound 5 is enforced by capping the loss
    at the household's income-plus-gain, and bound 3 is preserved by
    redistributing the capped excess pro rata across households that still
    have headroom. The excess is 0.0033 percent of the target at s = 0.25.
    DEVIATIONS D6; affected results marked."""
    inc = d["inc"].to_numpy()
    wt = d["wgt5"].to_numpy()
    headroom = np.maximum(inc + gam, 0.0)
    for _ in range(20):
        over = delta > headroom
        if not over.any():
            break
        excess = float(((delta - headroom)[over] * wt[over]).sum())
        delta = np.where(over, headroom, delta)
        room = np.maximum(headroom - delta, 0.0)
        room_tot = float((room * wt).sum())
        if room_tot <= 0 or excess <= 0:
            break
        delta = delta + (excess / room_tot) * room
    return delta


def gamma(d, s, ownership, kappa_key):
    """Gamma_i, the per-household capital gain reaching households."""
    w = d["wageinc"].clip(lower=0).to_numpy()
    wt = d["wgt5"].to_numpy()
    pot = s * float((w * wt).sum()) * KAPPA[kappa_key]
    own = d[f"own_{ownership}"].to_numpy()
    tot = float((own * wt).sum())
    if tot <= 0:
        return np.zeros(len(d))
    # gamma_i is a PER-HOUSEHOLD level. tot already carries the weights, so
    # sum_i gamma_i * wt_i = pot exactly. Dividing by wt here would be wrong
    # and was: it made the capital gain ~1000x too small (DEVIATIONS D4).
    return pot * (own / tot)


def income_after(d, delta, gam, g):
    """Income after the shift and growth. See the module docstring on accrual."""
    return (1.0 + g) * (d["inc"].to_numpy() - delta + gam)


def rises(d, delta, gam, g):
    """PTI rises iff income falls (payments fixed)."""
    return income_after(d, delta, gam, g) < d["inc"].to_numpy()


def affected_debt_share(d, delta, gam, g, debt_col="debt_total",
                        ur_adjust=False):
    wt = d["wgt5"].to_numpy()
    v = d["valid"].to_numpy()
    if ur_adjust and debt_col == "debt_total":
        bal = sum(d[f"debt_{k}"].to_numpy() * UR_FACTOR[k]
                  for k in DEBT_CLASSES)
    elif ur_adjust:
        k = debt_col.replace("debt_", "")
        bal = d[debt_col].to_numpy() * UR_FACTOR[k]
    else:
        bal = d[debt_col].to_numpy()
    r = rises(d, delta, gam, g) & v
    den = float((bal * wt * v).sum())
    if den <= 0:
        return np.nan
    return float((bal * wt * r).sum() / den)


def boundary(d, s, allocation, ownership, basis, kappa_key,
             exposure_case="cognitive_AIOE", r_retained=R_RETAINED,
             debt_col="debt_total", g_grid=G_GRID, ur_adjust=False):
    """Smallest g on the grid at which the affected-debt share returns to its
    baseline value (D at s=0, which is 0). Returns np.nan if not reached."""
    w = d["wageinc"].clip(lower=0).to_numpy()
    wt = d["wgt5"].to_numpy()
    delta = wage_loss(d, s, allocation, exposure_case, r_retained)
    gam = gamma(d, s, ownership, kappa_key)
    delta = cap_and_redistribute(d, delta, gam, s * float((w * wt).sum()))
    for g in g_grid:
        if affected_debt_share(d, delta, gam, g, debt_col,
                               ur_adjust) <= 1e-12:
            return float(g)
    return np.nan


def analytic_boundary(d, s, allocation, ownership, basis, kappa_key,
                      exposure_case="cognitive_AIOE",
                      r_retained=R_RETAINED):
    """The exact boundary, not grid-limited: the growth that makes the
    worst-affected indebted household whole. Reported alongside the grid value
    so 'beyond grid' can be quantified."""
    w = d["wageinc"].clip(lower=0).to_numpy()
    wt = d["wgt5"].to_numpy()
    delta = wage_loss(d, s, allocation, exposure_case, r_retained)
    gam = gamma(d, s, ownership, kappa_key)
    delta = cap_and_redistribute(d, delta, gam, s * float((w * wt).sum()))
    inc = d["inc"].to_numpy()
    net = inc - delta + gam
    m = d["valid"].to_numpy() & (d["debt_total"].to_numpy() > 0) & (net > 0)
    if not m.any():
        return np.nan
    need = inc[m] / net[m] - 1.0
    return float(np.nanmax(need))
