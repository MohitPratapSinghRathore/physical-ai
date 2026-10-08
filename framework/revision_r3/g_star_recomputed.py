"""REFEREE ITEM: the pass-through boundary was computed on the superseded marginal rate.

The condition is tau_k * g >= tau_l * (1 - R), so the coefficient at which it closes is

    g* = required / tau_k.

With the published layer and a federal marginal rate near 7.8 percent, g* ran 1.40 to 1.75,
which is what the introduction and conclusion still reported. On the corrected layer the
marginal rate is about 10.5 percent and g* falls to roughly 1.05 to 1.31. On the annual rate it
falls below one, which is the substantive point: the annual result does NOT hold only at g = 1.
It holds for any g above the value reported here, and that value is well inside the admissible
range for output-preserving displacement.

This also fixes an overstatement. Saying the annual condition "closes everywhere" meant
everywhere in the rate-parameter box, at g = 1. The honest statement is that it closes
everywhere in that box for g at or above g*_annual, and g* must be quoted with it.
"""
import json
import pathlib

OUT = pathlib.Path(__file__).resolve().parents[2] / "data" / "release" / "revision_r3"
REQ = {"federal": {"easier": 0.1101, "harder": 0.1373},
       "all_government": {"easier": 0.1240, "harder": 0.1510}}


def main():
    tb = json.loads((OUT / "two_objects_both_bases.json").read_text())
    res = {"formula": "g_star = required / tau_k, from tau_k * g >= tau_l * (1 - R)",
           "required": REQ, "by_basis": {}}
    for basis in ("federal", "all_government"):
        r = tb["rates"][basis]
        cell = {}
        for obj in ("marginal_barkai", "annual"):
            d = r[obj]
            for lab, key in (("published_layer", "published_layer"),
                             ("decomposed_layer", "decomposed_layer")):
                tk = d[key]
                cell[f"{obj}__{lab}"] = {
                    "tau_k": round(tk, 4),
                    "g_star_easier": round(REQ[basis]["easier"] / tk, 3),
                    "g_star_harder": round(REQ[basis]["harder"] / tk, 3),
                    "g_star_harder_below_one": bool(REQ[basis]["harder"] / tk < 1.0),
                }
            lo, hi = d["range_over_shareholder_box"]
            cell[f"{obj}__g_star_harder_over_box"] = [
                round(REQ[basis]["harder"] / hi, 3), round(REQ[basis]["harder"] / lo, 3)]
        res["by_basis"][basis] = cell

    f = res["by_basis"]["federal"]
    res["finding"] = (
        "Federal basis. On the marginal rate the corrected layer gives tau_k = {:.4f} and a "
        "boundary of g* = {:.3f} to {:.3f}, against {:.3f} to {:.3f} on the superseded layer; "
        "both still exceed the output-preserved ceiling of one, so the marginal reading needs "
        "output to rise. On the annual rate tau_k = {:.4f} and g* = {:.3f} to {:.3f}, both below "
        "one, so the annual condition closes without any increase in output and holds for any "
        "pass-through at or above {:.3f} on the harder reading. Over the shareholder box the "
        "harder-reading boundary runs {:.3f} to {:.3f}."
    ).format(f["marginal_barkai__decomposed_layer"]["tau_k"],
             f["marginal_barkai__decomposed_layer"]["g_star_easier"],
             f["marginal_barkai__decomposed_layer"]["g_star_harder"],
             f["marginal_barkai__published_layer"]["g_star_easier"],
             f["marginal_barkai__published_layer"]["g_star_harder"],
             f["annual__decomposed_layer"]["tau_k"],
             f["annual__decomposed_layer"]["g_star_easier"],
             f["annual__decomposed_layer"]["g_star_harder"],
             f["annual__decomposed_layer"]["g_star_harder"],
             f["annual__g_star_harder_over_box"][0],
             f["annual__g_star_harder_over_box"][1])

    (OUT / "g_star_recomputed.json").write_text(json.dumps(res, indent=2))
    print(json.dumps(res["by_basis"]["federal"], indent=2))
    print()
    print(res["finding"])


if __name__ == "__main__":
    main()
