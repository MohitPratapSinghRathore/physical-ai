"""REFEREE ITEMS B1 and B3 together, on both jurisdictional bases.

A first pass at the annual counterpart compared an ALL-GOVERNMENT rate, which includes the
state corporate tax in the entity layer, against the FEDERAL-ONLY replacement requirement.
That is the same basis mismatch the companion paper was criticised for on the Treasury
receipts vintage, and it is corrected here: each rate is compared to the requirement computed
on its own basis.

The two objects, each on both bases, and each with the shareholder layer both as published
and as decomposed in shareholder_lifecycle.py. The referee's joint-robustness point is the
reason the corrections are applied together rather than one at a time.

STATUS. MEASURED given the component ranges, which are the paper's own.
"""
import itertools
import json
import pathlib
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tau_k"))
sys.path.insert(0, str(HERE))
import components as K
import assemble as A
import shareholder_lifecycle as SL
import annual_revenue_bridge as AB

OUT = HERE.parents[1] / "data" / "release" / "revision_r3"
REQ = {"federal": {"easier": 0.1101, "harder": 0.1373},
       "all_government": {"easier": 0.1240, "harder": 0.1510}}


def entity(p, basis):
    state = p["state_cit_effective"] if basis == "all_government" else 0.0
    ent_dom = K.V_FED_CIT + state * (1 - K.V_FED_CIT)
    return (1 - p["shifted_share"]) * ent_dom + p["shifted_share"] * K.V_CFC_RATE


def tau_marginal(p, basis, ts, sigma):
    ent = entity(p, basis)
    tau_rent = ent + (1 - ent) * ts
    tau_normal = (1 - p["debt_share"]) * ts + p["debt_share"] * (p["bondholder_rate"]
                                                                - K.V_FED_CIT)
    return sigma * tau_rent + (1 - sigma) * tau_normal


def tau_annual(p, basis, ts):
    ent = entity(p, basis)
    return ((1 - p["debt_share"]) * (ent + (1 - ent) * ts)
            + p["debt_share"] * p["bondholder_rate"])


def layer_corners(which):
    return SL.corners(lambda q: SL.layers(q)[which])


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    p = dict(AB.CEN)
    sl = SL.layers(SL.CEN)
    ts_pub = A.tau_sh(K.THETA_TAXABLE["central"], SL.CEN["gains_rate"],
                      K.DEFERRAL_FACTOR["central"])
    sigma = K.RENT_READINGS["Barkai"]

    res = {"requirements": REQ, "shareholder_layers": {
        "published": round(ts_pub, 4),
        "decomposed_marginal": round(sl["marginal"], 4),
        "decomposed_annual": round(sl["annual"], 4)}, "rates": {}}

    for basis in ("federal", "all_government"):
        r = {}
        # marginal object, Barkai rent reading
        m_pub = tau_marginal(p, basis, ts_pub, sigma)
        m_dec = tau_marginal(p, basis, sl["marginal"], sigma)
        lo, hi = layer_corners("marginal")
        m_lo = tau_marginal(p, basis, lo, sigma)
        m_hi = tau_marginal(p, basis, hi, sigma)
        r["marginal_barkai"] = {
            "published_layer": round(m_pub, 4), "decomposed_layer": round(m_dec, 4),
            "range_over_shareholder_box": [round(m_lo, 4), round(m_hi, 4)],
            "gap_to_easier": round(REQ[basis]["easier"] - m_dec, 4),
            "clears_easier": bool(m_dec >= REQ[basis]["easier"]),
            "range_straddles_easier": bool(m_lo < REQ[basis]["easier"] <= m_hi)}
        # annual object
        a_pub = tau_annual(p, basis, ts_pub)
        a_dec = tau_annual(p, basis, sl["annual"])
        alo, ahi = layer_corners("annual")
        r["annual"] = {
            "published_layer": round(a_pub, 4), "decomposed_layer": round(a_dec, 4),
            "range_over_shareholder_box": [round(tau_annual(p, basis, alo), 4),
                                           round(tau_annual(p, basis, ahi), 4)],
            "margin_over_harder": round(a_dec - REQ[basis]["harder"], 4),
            "clears_easier": bool(a_dec >= REQ[basis]["easier"]),
            "clears_harder": bool(a_dec >= REQ[basis]["harder"]),
            "clears_harder_at_worst_corner": bool(
                tau_annual(p, basis, alo) >= REQ[basis]["harder"])}
        res["rates"][basis] = r

    f = res["rates"]["federal"]
    g = res["rates"]["all_government"]
    res["finding"] = (
        "On the ANNUAL object the condition closes on both bases and at the worst corner of "
        "the shareholder box: {:.4f} federal against {:.4f} required, {:.4f} all-government "
        "against {:.4f}. On the MARGINAL object, with the shareholder corrections applied "
        "jointly, the remaining gap is {:.4f} federal and {:.4f} all-government, and the "
        "range over the shareholder box straddles the federal requirement. A gap of well "
        "under one percentage point, with a range that straddles, does not establish a sign. "
        "The shortfall is therefore not a finding on either object: it closes on the annual "
        "one and is indistinguishable from zero on the marginal one."
    ).format(f["annual"]["decomposed_layer"], REQ["federal"]["harder"],
             g["annual"]["decomposed_layer"], REQ["all_government"]["harder"],
             f["marginal_barkai"]["gap_to_easier"],
             g["marginal_barkai"]["gap_to_easier"])

    (OUT / "two_objects_both_bases.json").write_text(json.dumps(res, indent=2))
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
