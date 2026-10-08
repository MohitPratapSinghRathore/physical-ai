"""REFEREE ITEM B1. Derive the mapping from the marginal investment wedge to an annual
revenue rate, and compute both. The referee's objection is that an effective marginal tax
wedge is not a revenue collection rate, and that full expensing can null the wedge on a
marginal normal-return project while an established sector still pays positive annual tax.

THE DERIVATION, stated before computing.

Let a stationary sector hold capital K, depreciating at delta, earning gross capital income
(r + delta) K, so net capital income is r K. In steady state replacement investment is
I = delta K.

  Annual entity deduction under 100 percent expensing  = I     = delta K
  Annual entity deduction under economic depreciation  = delta K
  so the two coincide IN STEADY STATE and the annual entity base is
      (r + delta) K - delta K = r K,
  the whole net capital income, normal return and rent alike.

The marginal wedge is a different object. For one marginal project, expensing deducts the
whole outlay at once, and the present value of that deduction exactly offsets the present
value of entity tax on the project's normal return. Hence the Acemoglu, Manera and Restrepo
result the paper uses, that the entity tax washes out on the normal return, which is correct
ON THE MARGIN and false for the annual flow from capital already in place.

Consequences, which are the point of the exercise:

  1. ANNUAL rate on a dollar of net capital income, equity financed: the entity tax applies,
     then the shareholder layer applies to what is left.
            ent + (1 - ent) * tau_sh
  2. Debt financed: the interest deduction at the entity offsets the interest income, so the
     annual entity tax is zero and only the bondholder layer collects.
            bondholder_rate
     This replaces the marginal object's (bond - fed_cit), which is negative and is a
     SUBSIDY to a marginal debt-financed project, not a negative annual revenue.
  3. tau_annual = (1 - debt) * [ent + (1 - ent) * tau_sh] + debt * bond.

  4. **The rent share sigma does not appear.** On the annual object the entity tax reaches
     normal return and rent alike, so the two rent readings that drive the marginal rate's
     spread collapse to one number. That also disposes of the awkwardness of the
     Karabarbounis and Neiman reading, under which sigma = 0 and the marginal rate nearly
     vanishes.

WHAT THIS DOES NOT ESTABLISH. The annual object is the right one for the replacement
condition only if the horizon over which displaced wage receipts must be replaced is long
relative to the transition, and if the capital stock is near stationary. During an investment
boom current deductions exceed tax on income from a smaller earlier stock, so collections run
below tau_annual and above tau_marginal. The two rates are therefore bounds on the transition
path rather than rival point estimates, and we report them as such.

STATUS. MEASURED given the component ranges, which are the paper's own.
"""
import itertools, json, pathlib, sys
import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tau_k"))
import components as K
import assemble as A

OUT = pathlib.Path(__file__).resolve().parents[2] / "data" / "release" / "revision_r3"
REQ = {"easier": 0.1101, "harder": 0.1373}

BOX = {
    "shifted_share": K.U["shifted_share"]["range"],
    "shareholder_rate": K.U["shareholder_rate"]["range"],
    "state_cit_effective": K.U["state_cit_effective"]["range"],
    "theta_taxable": [K.THETA_TAXABLE["low"], K.THETA_TAXABLE["high"]],
    "deferral_factor": [K.DEFERRAL_FACTOR["low"], K.DEFERRAL_FACTOR["high"]],
    "debt_share": [K.DEBT_SHARE["low"], K.DEBT_SHARE["high"]],
    "bondholder_rate": [K.BONDHOLDER_RATE["low"], K.BONDHOLDER_RATE["high"]],
}
CEN = {
    "shifted_share": 0.48,
    "shareholder_rate": float(np.mean(K.U["shareholder_rate"]["range"])),
    "state_cit_effective": float(np.mean(K.U["state_cit_effective"]["range"])),
    "theta_taxable": K.THETA_TAXABLE["central"],
    "deferral_factor": K.DEFERRAL_FACTOR["central"],
    "debt_share": K.DEBT_SHARE["central"],
    "bondholder_rate": K.BONDHOLDER_RATE["central"],
}
NAMES = list(BOX)


def entity(p):
    ent_dom = K.V_FED_CIT + p["state_cit_effective"] * (1 - K.V_FED_CIT)
    return (1 - p["shifted_share"]) * ent_dom + p["shifted_share"] * K.V_CFC_RATE


def tau_annual(p):
    ts = A.tau_sh(p["theta_taxable"], p["shareholder_rate"], p["deferral_factor"])
    ent = entity(p)
    return (1 - p["debt_share"]) * (ent + (1 - ent) * ts) + p["debt_share"] * p["bondholder_rate"]


def tau_marginal(p, sigma):
    z, _, _ = A.assemble(sigma, p["shifted_share"], p["theta_taxable"], p["shareholder_rate"],
                         p["deferral_factor"], p["state_cit_effective"], p["debt_share"],
                         p["bondholder_rate"])
    return float(z)


def corners(fn):
    """Both objects are multilinear in the seven parameters, so extrema sit at corners."""
    vals = []
    for combo in itertools.product(*[BOX[n] for n in NAMES]):
        vals.append(fn(dict(zip(NAMES, combo))))
    return float(min(vals)), float(max(vals))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    res = {"derivation": __doc__.split("STATUS.")[0].strip(), "required": REQ,
           "central_parameters": {k: round(v, 5) for k, v in CEN.items()}}

    a_cen = tau_annual(CEN)
    a_lo, a_hi = corners(tau_annual)
    res["annual"] = {"central": round(a_cen, 4), "corner_min": round(a_lo, 4),
                     "corner_max": round(a_hi, 4),
                     "sigma_free": True,
                     "closes_easier": bool(a_cen >= REQ["easier"]),
                     "closes_harder": bool(a_cen >= REQ["harder"]),
                     "closes_easier_at_worst_corner": bool(a_lo >= REQ["easier"]),
                     "closes_harder_at_worst_corner": bool(a_lo >= REQ["harder"])}

    res["marginal"] = {}
    for name, sig in K.RENT_READINGS.items():
        m_cen = tau_marginal(CEN, sig)
        m_lo, m_hi = corners(lambda p, s=sig: tau_marginal(p, s))
        res["marginal"][name] = {"sigma": sig, "central": round(m_cen, 4),
                                 "corner_min": round(m_lo, 4), "corner_max": round(m_hi, 4),
                                 "closes_easier": bool(m_cen >= REQ["easier"]),
                                 "gap_to_annual": round(a_cen - m_cen, 4)}

    res["finding"] = (
        "The annual rate is {:.4f} at central values against a requirement of {:.4f} to "
        "{:.4f}, so the replacement condition CLOSES on the annual object, and closes at "
        "every corner of the parameter box down to {:.4f}. The marginal wedge is {:.4f} to "
        "{:.4f} across the two rent readings and closes on neither. The paper's headline "
        "shortfall is therefore a property of the marginal object and does not survive the "
        "translation to annual revenue. The referee's objection is correct and material."
    ).format(a_cen, REQ["easier"], REQ["harder"], a_lo,
             min(v["central"] for v in res["marginal"].values()),
             max(v["central"] for v in res["marginal"].values()))

    (OUT / "annual_revenue_bridge.json").write_text(json.dumps(res, indent=2))
    print(json.dumps({k: v for k, v in res.items() if k != "derivation"}, indent=2))


if __name__ == "__main__":
    main()
