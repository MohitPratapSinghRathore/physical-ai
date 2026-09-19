"""Displacement scenarios: worker-level probability as a function of exposure and incidence.

METHOD NOTE, and it is the reason this module exists.

A39 established that share-based attribution (give a group a slice of the debt equal to its
slice of the wage bill) is an aggregation artifact. It is valid only if displacement is
drawn wage-neutrally from inside an exposure group, and household obligation per wage dollar
varies six to eleven fold across wage deciles, so that assumption is never innocuous. This
module replaces the assumption with an explicit, variable incidence rule, and the engines
that consume it work household by household rather than on group shares.

THE PROBABILITY FUNCTION

For an exposure construct T (an occupation-level score), let r be the employment-weighted
percentile rank of an occupation's score within T, so r is in [0, 1] and high r means high
exposure. Worker displacement probability over the scenario horizon is

    p(r) = min(1, a * r ** gamma)

with gamma fixed at 3.0 and a solved by bisection so that the employment-weighted mean of p
equals the scenario target share of total employment. gamma = 3 concentrates displacement in
the upper tail of exposure; gamma = 1 spreads it linearly in rank. Both are reported.

This is a REDUCED FORM. It is not estimated from observed displacement, because no dataset
measures AI displacement by occupation. It encodes one assumption only: that displacement is
monotone in the exposure score. The scenario target carries the magnitude, and the paper
must report results across targets rather than choosing one.

INCIDENCE VARIANTS, which are the point of the exercise

Within a scenario, who inside an exposed occupation loses the job is unknown. Three variants,
all holding the expected number displaced fixed:

    uniform             p does not depend on the worker's wage
    lowest_wage_first   p tilted toward low earners within the occupation
    highest_wage_first  p tilted toward high earners within the occupation

The tilt is a multiplicative factor m(q) in the worker's within-occupation wage percentile q,
m(q) proportional to (1 - q) ** delta or q ** delta with delta = 2, rescaled by bisection so
the employment-weighted expected count is unchanged, then clipped to [0, 1] and rescaled
again until the count matches to 1e-6. The spread between the three variants is the
quantitative answer to the understatement A39 flagged.

CAVEAT carried into every cognitive result: Felten AIOE and Eloundou GPT exposure measure
TASK OVERLAP, not displacement and not timing, and top-quintile occupations include
likely-augmented work. The probability function above converts a task-overlap rank into a
displacement probability by assumption, and that assumption is the weakest link in any
cognitive number this engine produces. It must be stated wherever such a number appears.
"""
import pathlib
import numpy as np
import pandas as pd
import importlib.util

ROOT = pathlib.Path(__file__).parents[2]
OUT = ROOT / "data" / "processed"

GAMMA_DEFAULT = 3.0
DELTA_TILT = 2.0
TARGETS = {"mild_5pct": 0.05, "central_10pct": 0.10, "severe_20pct": 0.20}
INCIDENCE = ("uniform", "lowest_wage_first", "highest_wage_first")

# Reemployment. omega from Jacobson, LaLonde and Sullivan as used throughout this
# repository (central 0.75, range 0.65 to 0.82). rho is NOT yet sourced: the BLS Displaced
# Worker Survey is blocked from this environment, so it is gridded and never asserted.
OMEGA = {"low": 0.65, "central": 0.75, "high": 0.82}
RHO_GRID = (0.50, 0.65, 0.80)


def _h3():
    s = importlib.util.spec_from_file_location("h3", ROOT / "src" / "h3_geography.py")
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
    return m


def occupation_scores():
    """One row per OCCP with every exposure score the project uses, plus employment.

    Returns columns: occp, employment, and a score column per construct in CONSTRUCTS.
    Pathways are categorical and become 0/1 score columns, ranked by embodiment P inside
    the pathway so that the probability function still has something monotone to work with.
    """
    h3 = _h3()
    B, _ = h3.build_groups()
    B = B[["occp", "title", "employment", "embodiment_P", "aioe", "gpt", "pct_robot"]].copy()
    pa = pd.read_csv(OUT / "pathway_assignment.csv")[["occp", "pathway"]]
    B = B.merge(pa, on="occp", how="left")
    return B


CONSTRUCTS = {
    "cognitive_AIOE": "aioe",
    "cognitive_GPT": "gpt",
    "embodied": "embodiment_P",
    "robot_reachable": "pct_robot",
}
PATHWAYS = ("driving", "gated", "manipulation")


def rank_within(B, score_col, restrict=None):
    """Employment-weighted percentile rank of the score, NaN outside the construct.

    restrict: optional boolean mask. Occupations outside it get rank NaN and probability 0,
    which is how the pathway constructs are expressed.
    """
    d = B.copy()
    ok = d[score_col].notna() & d["employment"].notna() & (d["employment"] > 0)
    if restrict is not None:
        ok &= restrict
    r = pd.Series(np.nan, index=d.index)
    sub = d[ok].sort_values(score_col)
    e = sub["employment"].to_numpy(float)
    # midpoint of the employment interval each occupation occupies
    cum = np.cumsum(e) - 0.5 * e
    r.loc[sub.index] = cum / e.sum()
    return r


def _solve_scale(rank, emp, gamma, target_count):
    """Bisect a so that sum(emp * min(1, a*rank**gamma)) == target_count."""
    base = np.where(np.isfinite(rank), np.clip(rank, 0, 1) ** gamma, 0.0)
    lo, hi = 0.0, 1.0
    while (np.minimum(1.0, hi * base) * emp).sum() < target_count and hi < 1e9:
        hi *= 2.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if (np.minimum(1.0, mid * base) * emp).sum() < target_count:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi), np.minimum(1.0, 0.5 * (lo + hi) * base)


def occupation_probabilities(B, construct, target_share, gamma=GAMMA_DEFAULT):
    """Occupation-level displacement probability for one construct and scenario target.

    target_share is a share of TOTAL employment, not of the construct, so scenarios are
    comparable across constructs.
    """
    if construct in CONSTRUCTS:
        rank = rank_within(B, CONSTRUCTS[construct])
    elif construct in PATHWAYS:
        rank = rank_within(B, "embodiment_P", restrict=(B["pathway"] == construct))
    else:
        raise KeyError(construct)
    emp = B["employment"].fillna(0.0).to_numpy(float)
    target_count = target_share * emp.sum()
    in_scope = float(emp[np.isfinite(rank.to_numpy())].sum())
    if in_scope < target_count:
        # the construct is too small to absorb the scenario; cap at full displacement
        a, p = np.inf, np.where(np.isfinite(rank.to_numpy()), 1.0, 0.0)
    else:
        a, p = _solve_scale(rank.to_numpy(), emp, gamma, target_count)
    return pd.DataFrame({
        "occp": B["occp"], "employment": emp, "rank": rank.to_numpy(), "p_occ": p,
        "construct": construct, "target_share": target_share, "gamma": gamma,
        "scale_a": a, "in_scope_employment": in_scope,
        "capped": bool(in_scope < target_count)})


def apply_incidence(p_occ, wage_pctile_in_occ, emp_weight, mode, delta=DELTA_TILT):
    """Tilt worker probabilities by within-occupation wage rank, holding the count fixed.

    p_occ               occupation probability broadcast to workers
    wage_pctile_in_occ  worker's wage percentile inside their own occupation, in [0, 1]
    emp_weight          person weight, so the preserved quantity is the expected headcount
    """
    p_occ = np.asarray(p_occ, float)
    w = np.asarray(emp_weight, float)
    if mode == "uniform":
        return np.clip(p_occ, 0.0, 1.0)
    q = np.clip(np.asarray(wage_pctile_in_occ, float), 0.0, 1.0)
    m = (1.0 - q) ** delta if mode == "lowest_wage_first" else q ** delta
    target = float((p_occ * w).sum())
    if target <= 0:
        return np.zeros_like(p_occ)
    lo, hi = 0.0, 1.0
    f = lambda s: float((np.clip(s * m * p_occ, 0.0, 1.0) * w).sum())
    while f(hi) < target and hi < 1e9:
        hi *= 2.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if f(mid) < target:
            lo = mid
        else:
            hi = mid
    return np.clip(0.5 * (lo + hi) * m * p_occ, 0.0, 1.0)


def describe():
    """Human-readable record of the scenario grid, written into every output bundle."""
    return {
        "gamma_default": GAMMA_DEFAULT, "delta_tilt": DELTA_TILT,
        "targets_share_of_total_employment": TARGETS,
        "incidence_variants": list(INCIDENCE),
        "omega_wage_ratio_on_reemployment": OMEGA,
        "omega_source": "Jacobson, LaLonde and Sullivan, as used elsewhere in this repo",
        "rho_grid": list(RHO_GRID),
        "rho_status": "NOT SOURCED. BLS Displaced Worker Survey blocked from this "
                      "environment. rho is gridded and must never be asserted as observed.",
        "probability_form": "p(r) = min(1, a * r**gamma), r = employment-weighted "
                            "percentile rank of the exposure score, a solved so the "
                            "employment-weighted mean p equals the scenario target",
        "cognitive_caveat": "AIOE and Eloundou GPT measure TASK OVERLAP, not displacement "
                            "and not timing; top-quintile occupations include "
                            "likely-augmented work. Converting that rank to a displacement "
                            "probability is an assumption, and it is the weakest link in "
                            "any cognitive number produced by this engine.",
    }
