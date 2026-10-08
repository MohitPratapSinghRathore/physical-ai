"""REFEREE ITEM: the levers paragraph said the three-mechanism decomposition had not been
recomputed and then asserted that its ordering survives, and it supported that ordering with
parameter sensitivity ranges even though the counterfactual section explains that sensitivity
does not establish importance. Both objections are correct. This recomputes the decomposition
on the decomposed shareholder layer, by counterfactual, on BOTH tax objects, so the ordering is
claimed from an importance calculation or not at all.

THE THREE MECHANISMS, defined on the decomposed layer.

  base        the taxable shareholder base is complete: every share sits in a taxable account,
              so the holder groups collapse to the taxable-account treatment and no holding is
              outside the owner-level base.
  defer       deferral and step-up at death are eliminated: accrued gains bear the full
              statutory rate rather than the rate reduced by the share never taxed at death.
  shift       profit shifting is eliminated: every dollar of rent is booked domestically.

VALUE FUNCTION. v(S) is the assembled rate with the mechanisms in S set to their no-friction
values and the others at their measured values, so v({}) is the baseline and v({all}) is the
frictionless rate. Each mechanism's Shapley value averages its marginal contribution over all
six orderings of removal, and the three sum exactly to v({all}) - v({}).

WHY BOTH OBJECTS. The paragraph being corrected claimed an ordering on the marginal wedge and
a reversal on the annual rate, citing sensitivity swings for both. Computing the counterfactual
on each object settles it on the right basis.
"""
import itertools
import json
import math
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tau_k"))
sys.path.insert(0, str(HERE))
import components as K
import shareholder_lifecycle as SL
import annual_revenue_bridge as AB

OUT = HERE.parents[1] / "data" / "release" / "revision_r3"
MECHS = ("base", "defer", "shift")


def layer(p, S):
    """The decomposed shareholder layer with the mechanisms in S removed."""
    h = dict(SL.HOLDERS)
    step_up = 0.0 if "defer" in S else SL.GAINS_STEP_UP
    gains = p["gains_rate"]
    gains_eff = gains * (1 - step_up)
    if "base" in S:
        # every share in a taxable account: one group, taxable treatment
        return p["payout"] * gains + (1 - p["payout"]) * gains_eff
    trad = (h["ira"] * (1 - SL.ROTH_SHARE_OF_IRA) + h["defined_benefit"]
            + h["defined_contribution"] * (1 - p["roth_share_of_dc"]))
    taxable = h["taxable_accounts"] * (p["payout"] * gains + (1 - p["payout"]) * gains_eff)
    foreign = h["foreign"] * p["payout"] * p["withholding_eff"]
    trad_annual = trad * p["ordinary_rate_retirement"]
    return taxable + foreign, trad_annual


def tau(p, S, obj, sigma=None):
    """Assembled rate with the mechanisms in S removed, on the named object."""
    shifted = 0.0 if "shift" in S else p["shifted_share"]
    ent_dom = K.V_FED_CIT          # federal-only basis throughout, as the table states
    ent = (1 - shifted) * ent_dom + shifted * K.V_CFC_RATE
    L = layer(p, S)
    if isinstance(L, tuple):
        ts_marg, trad_annual = L
        ts_ann = ts_marg + trad_annual
    else:
        ts_marg = ts_ann = L       # base complete: no retirement group remains
    d, b = p["debt_share"], p["bondholder_rate"]
    if obj == "annual":
        return (1 - d) * (ent + (1 - ent) * ts_ann) + d * b
    rent = ent + (1 - ent) * ts_marg
    normal = (1 - d) * ts_marg + d * (b - K.V_FED_CIT)
    return sigma * rent + (1 - sigma) * normal


def shapley(p, obj, sigma=None):
    n = len(MECHS)
    vals = {m: 0.0 for m in MECHS}
    for order in itertools.permutations(MECHS):
        S = set()
        prev = tau(p, S, obj, sigma)
        for m in order:
            S.add(m)
            cur = tau(p, S, obj, sigma)
            vals[m] += cur - prev
            prev = cur
    k = math.factorial(n)
    return {m: v / k for m, v in vals.items()}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    p = {**SL.CEN, **{k: v for k, v in AB.CEN.items() if k not in SL.CEN}}
    res = {"definitions": __doc__.split("THE THREE MECHANISMS")[1].split("WHY BOTH")[0].strip(),
           "basis": "federal only", "readings": {}}
    for obj, sig, label in (("marginal", K.RENT_READINGS["Barkai"], "marginal_barkai"),
                            ("annual", None, "annual")):
        sh = shapley(p, obj, sig)
        base = tau(p, set(), obj, sig)
        full = tau(p, set(MECHS), obj, sig)
        order = sorted(sh, key=lambda m: -sh[m])
        res["readings"][label] = {
            "baseline": round(base, 4), "frictionless": round(full, 4),
            "joint": round(full - base, 4),
            "shapley": {m: round(sh[m], 4) for m in MECHS},
            "sums_to_joint": round(sum(sh.values()), 4),
            "order_largest_first": order,
            "ownership_over_shifting": (
                round((sh["base"] + sh["defer"]) / sh["shift"], 1) if sh["shift"] > 1e-9 else None),
            "base_over_shifting": (
                round(sh["base"] / sh["shift"], 1) if sh["shift"] > 1e-9 else None),
        }
    m, a = res["readings"]["marginal_barkai"], res["readings"]["annual"]
    res["finding"] = (
        "Recomputed by counterfactual on the decomposed layer, federal basis. On the marginal "
        "wedge the Shapley values are base {:.4f}, deferral {:.4f}, shifting {:.4f}, summing to "
        "the joint effect of {:.4f}, so the order largest first is {}. On the annual rate they "
        "are base {:.4f}, deferral {:.4f}, shifting {:.4f}, order {}. The ordering is now claimed "
        "from an importance calculation rather than from sensitivity swings, which is what the "
        "counterfactual section says is required."
    ).format(m["shapley"]["base"], m["shapley"]["defer"], m["shapley"]["shift"], m["joint"],
             ", ".join(m["order_largest_first"]),
             a["shapley"]["base"], a["shapley"]["defer"], a["shapley"]["shift"],
             ", ".join(a["order_largest_first"]))
    (OUT / "shapley_recomputed.json").write_text(json.dumps(res, indent=2))
    print(json.dumps(res["readings"], indent=2))
    print()
    print(res["finding"])


if __name__ == "__main__":
    main()
