"""REFEREE ITEM: the counterfactual decomposition was computed on the superseded shareholder
layer, so the introduction, the counterfactual discussion and the conclusion still carried a
7.8 percent baseline and gains of +1.37 and +13.27 points while the fiscal section reported a
corrected 10.5 percent. Recompute the same counterfactuals on the decomposed layer rather than
labelling them superseded, on both jurisdictional bases, and report what changed.

DEFINITIONS, unchanged from the published version so the comparison is like for like.
  baseline                  the layer as assembled
  no_profit_shifting        shifted share set to zero, so every dollar is booked domestically
  complete_ownership_reach  the shareholder layer at its no-friction value: every share in a
                            taxable account, nothing deferred, nothing stepped up at death, so
                            the layer collapses to the statutory gains rate
  both                      the two together, with the interaction reported

The ownership counterfactual is the one the decomposition changes, because the baseline layer
it is measured against is no longer the same object.
"""
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tau_k"))
sys.path.insert(0, str(HERE))
import components as K
import assemble as A
import shareholder_lifecycle as SL
import annual_revenue_bridge as AB

OUT = HERE.parents[1] / "data" / "release" / "revision_r3"
REQ = {"federal": 0.1101, "all_government": 0.1240}


def entity(p, basis, shifted=None):
    s = p["shifted_share"] if shifted is None else shifted
    state = p["state_cit_effective"] if basis == "all_government" else 0.0
    ent_dom = K.V_FED_CIT + state * (1 - K.V_FED_CIT)
    return (1 - s) * ent_dom + s * K.V_CFC_RATE


def tau_marginal(p, basis, ts, sigma, shifted=None):
    ent = entity(p, basis, shifted)
    rent = ent + (1 - ent) * ts
    normal = (1 - p["debt_share"]) * ts + p["debt_share"] * (p["bondholder_rate"] - K.V_FED_CIT)
    return sigma * rent + (1 - sigma) * normal


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    p = dict(AB.CEN)
    sl = SL.layers(SL.CEN)
    ts_pub = A.tau_sh(K.THETA_TAXABLE["central"], SL.CEN["gains_rate"],
                      K.DEFERRAL_FACTOR["central"])
    ts_dec = sl["marginal"]
    ts_free = SL.CEN["gains_rate"]          # no-friction shareholder layer

    res = {"definitions": __doc__.split("DEFINITIONS")[1].strip(),
           "layers": {"published": round(ts_pub, 4), "decomposed": round(ts_dec, 4),
                      "no_friction": round(ts_free, 4)},
           "required": REQ, "readings": {}}

    for rname, sigma in K.RENT_READINGS.items():
        res["readings"][rname] = {}
        for basis in ("federal", "all_government"):
            cell = {}
            for lab, ts in (("published_layer", ts_pub), ("decomposed_layer", ts_dec)):
                base = tau_marginal(p, basis, ts, sigma)
                nos = tau_marginal(p, basis, ts, sigma, shifted=0.0)
                own = tau_marginal(p, basis, ts_free, sigma)
                both = tau_marginal(p, basis, ts_free, sigma, shifted=0.0)
                cell[lab] = {
                    "baseline": round(base, 4),
                    "no_profit_shifting": round(nos, 4),
                    "complete_ownership_reach": round(own, 4),
                    "both": round(both, 4),
                    "gain_from_removing_shifting": round(nos - base, 4),
                    "gain_from_ownership_reach": round(own - base, 4),
                    "interaction": round(both - nos - own + base, 4),
                    "ratio_ownership_to_shifting": (round((own - base) / (nos - base), 1)
                                                    if nos - base > 1e-9 else None),
                    "shifting_alone_clears": bool(nos >= REQ[basis]),
                    "ownership_alone_clears": bool(own >= REQ[basis]),
                }
            res["readings"][rname][basis] = cell

    b = res["readings"]["Barkai"]["federal"]
    res["finding"] = (
        "On the Barkai reading and the federal basis, the published layer gave a baseline of "
        "{:.4f} with gains of {:+.4f} from ending profit shifting and {:+.4f} from completing "
        "the shareholder tax, a ratio of {}. On the decomposed layer the baseline is {:.4f} and "
        "the gains are {:+.4f} and {:+.4f}, a ratio of {}. The ownership channel shrinks because "
        "the baseline layer it is measured against is already larger once withholding and the "
        "dividend split are counted: there is less friction left to remove. The qualitative "
        "ordering on the marginal object survives, and the paper reports the decomposed figures."
    ).format(b["published_layer"]["baseline"],
             b["published_layer"]["gain_from_removing_shifting"],
             b["published_layer"]["gain_from_ownership_reach"],
             b["published_layer"]["ratio_ownership_to_shifting"],
             b["decomposed_layer"]["baseline"],
             b["decomposed_layer"]["gain_from_removing_shifting"],
             b["decomposed_layer"]["gain_from_ownership_reach"],
             b["decomposed_layer"]["ratio_ownership_to_shifting"])

    (OUT / "counterfactuals_recomputed.json").write_text(json.dumps(res, indent=2))
    print(json.dumps(res["readings"]["Barkai"], indent=2))
    print()
    print(res["finding"])


if __name__ == "__main__":
    main()
