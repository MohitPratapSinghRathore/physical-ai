"""ITEM 2(g). The labour-income component of AI capital spending.

Compensation paid to workers at the producers and integrators of AI capital: chip
fabrication, server assembly, data centre construction, systems integration, and the
software engineering that goes with them. The task asks for it at the labour rate, with a
sourced labour share and an import share.

THE RESULT IS THAT IT CONTRIBUTES ZERO TO tau_k, AND THE REASON IS THE NO-DOUBLE-COUNTING
RULE OF item 1. This is not a convenience. It is forced by how the fiscal condition is built
in this repository, and it took reading `src/consistency.py` and `src/fiscal_extended_axis.py`
to see it.

  The condition is   fiscal loss per displaced dollar = tau_l x (1 - R) - tau_k
  with R = rho x omega the RETAINED WAGE SHARE, and the wage bill it is scaled against is
  COMPENSATION OF EMPLOYEES, ECONOMY WIDE (16,224.3bn, FRED COE, used in
  `src/fiscal_extended_axis.py`).

  Compensation at AI producers and integrators is US compensation of employees. It is
  therefore ALREADY INSIDE that wage bill, and the labour tax on it is already inside the
  tau_l term. Worse, a displaced worker who is reemployed building data centres is
  reemployment, which is precisely what rho measures. So that compensation is already inside
  **R** as well.

  Adding tau_l x (labour share of AI capex) to tau_k would count the same dollar of wage tax
  twice: once in tau_l x (1 - R) and once again in tau_k. That is the exact error item 1
  exists to prevent, and it is the error that would have made the fiscal condition look
  closable.

SO THE HONEST DECOMPOSITION OF AI CAPITAL SPENDING IS:

  domestic labour component  -> already counted, inside R and inside the tau_l term. ZERO
                                new contribution to tau_k.
  imported component         -> a LEAKAGE. It compensates foreign workers, so the US
                                collects no labour tax on it at all. It is the one part of
                                this item that moves the answer, and it moves it the WRONG
                                way for the thesis: it means the share of AI capital
                                spending that recirculates as US wage income is smaller than
                                the domestic labour share alone would suggest.
  domestic non-labour        -> surplus at the producers, which is where tau_k already
                                applies, and it is the object the rest of this folder prices.

WHAT IS AND IS NOT SOURCED. Neither the labour share of AI capital spending nor the import
share could be verified from a primary source in this session. BEA's industry tables require
an interactive query, the Census foreign-trade exhibit returned HTTP 404, and the FRED CSV
endpoint timed out. Both are therefore SWEPT over structurally bounded ranges, listed in
`lit/unverified.md`, and NO POINT VALUE IS ASSERTED. Because the component contributes zero
to tau_k by the argument above, nothing in the assembled rate depends on either of them.
They are reported here only to size the leakage.
"""
import json
import pathlib

import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).parent

# NOT VERIFIED. Swept. Bounds are structural, and the bound is named.
LABOUR_SHARE_OF_AI_CAPEX = {
    "range": [0.20, 0.55],
    "bound": "a share of value added, so [0,1]. The lower end is below the labour share of "
             "semiconductor manufacturing, which is capital intensive; the upper end is "
             "below the labour share of construction and software, which are labour "
             "intensive. The true figure is a weighted mix of the two and must lie between.",
    "sought": "BEA GDP-by-industry compensation share for computer and electronic product "
              "manufacturing, software publishing and nonresidential construction. BEA "
              "iTable requires an interactive query; FRED CSV endpoint timed out.",
}
IMPORT_SHARE_OF_AI_CAPEX = {
    "range": [0.25, 0.70],
    "bound": "a share, [0,1]. Bounded below by the fact that advanced logic and memory are "
             "predominantly fabricated outside the United States, and above by the fact "
             "that data centre construction, power interconnection and integration labour "
             "are necessarily domestic and are a large part of total outlay.",
    "sought": "Census foreign-trade exhibit 8 (advanced technology products) returned HTTP "
              "404; no primary substitute obtained.",
}

# The labour tax readings already in this repository. Not averaged; carried as readings.
TAU_L = {"AMR_0.255": 0.255, "bottom_up_0.301": 0.301, "bottom_up_0.318": 0.318}

RNG = np.random.default_rng(20260920)
N = 100_000


def main():
    lab = RNG.uniform(*LABOUR_SHARE_OF_AI_CAPEX["range"], N)
    imp = RNG.uniform(*IMPORT_SHARE_OF_AI_CAPEX["range"], N)

    # per dollar of AI capital spending
    domestic = 1 - imp
    dom_labour = domestic * lab            # already counted, inside R and tau_l
    leak = imp                             # no US labour tax at all
    dom_surplus = domestic * (1 - lab)     # the object tau_k prices

    rows = []
    for name, tl in TAU_L.items():
        # the labour tax that would be DOUBLE COUNTED if this item were added to tau_k
        double = tl * dom_labour
        rows.append({
            "tau_l_reading": name, "tau_l": tl,
            "contribution_to_tau_k": 0.0,
            "would_be_double_counted_per_dollar_of_capex_p05":
                round(float(np.percentile(double, 5)), 4),
            "would_be_double_counted_per_dollar_of_capex_median":
                round(float(np.median(double)), 4),
            "would_be_double_counted_per_dollar_of_capex_p95":
                round(float(np.percentile(double, 95)), 4),
        })
    T = pd.DataFrame(rows)
    T.to_csv(HERE / "labor_component.csv", index=False)

    # plausibility: the three parts of a dollar of capex must sum to one
    tot = dom_labour + dom_surplus + leak
    viol = []
    if not np.allclose(tot, 1.0, atol=1e-9):
        viol.append("the decomposition of a capex dollar does not sum to one")
    for nm, arr in [("domestic labour", dom_labour), ("leakage", leak),
                    ("domestic surplus", dom_surplus)]:
        if arr.min() < 0 or arr.max() > 1:
            viol.append(f"{nm} outside [0,1]")

    out = {
        "status": "STRUCTURAL RESULT, with two SWEPT unsourced parameters. The structural "
                  "result does not depend on either of them.",
        "contribution_to_tau_k": 0.0,
        "why_zero": "Compensation at AI producers and integrators is US compensation of "
                    "employees, so it is already inside the wage bill the fiscal condition "
                    "is scaled against (FRED COE, 16,224.3bn) and already inside the "
                    "retained wage share R, because reemployment at those producers is what "
                    "rho measures. Adding it to tau_k would count the same wage tax twice, "
                    "once in tau_l x (1 - R) and once in tau_k. Item 1 forbids exactly this.",
        "decomposition_of_one_dollar_of_ai_capex": {
            "domestic_labour_ALREADY_COUNTED": [
                round(float(np.percentile(dom_labour, 5)), 4),
                round(float(np.median(dom_labour)), 4),
                round(float(np.percentile(dom_labour, 95)), 4)],
            "imported_LEAKAGE_no_us_labour_tax": [
                round(float(np.percentile(leak, 5)), 4),
                round(float(np.median(leak)), 4),
                round(float(np.percentile(leak, 95)), 4)],
            "domestic_surplus_PRICED_BY_tau_k": [
                round(float(np.percentile(dom_surplus, 5)), 4),
                round(float(np.median(dom_surplus)), 4),
                round(float(np.percentile(dom_surplus, 95)), 4)],
        },
        "double_count_avoided": rows,
        "unverified_swept": {"labour_share_of_ai_capex": LABOUR_SHARE_OF_AI_CAPEX,
                             "import_share_of_ai_capex": IMPORT_SHARE_OF_AI_CAPEX},
        "plausibility_violations": viol,
        "thesis_direction": "This item WEAKENS the thesis-friendly reading in one direction "
                            "and the thesis-hostile reading in another. It removes a "
                            "recovery channel that a careless construction would have "
                            "credited to tau_k, which makes the condition harder to close. "
                            "It also shows that a median 47 percent of a dollar of AI "
                            "capital spending leaks abroad as imports and generates no US "
                            "labour tax at all, which is a larger leak than profit shifting "
                            "and has had none of the attention.",
    }
    (HERE / "labor_component.json").write_text(json.dumps(out, indent=2))

    pd.set_option("display.width", 200)
    print("ITEM 2(g), THE LABOUR COMPONENT OF AI CAPITAL SPENDING")
    print("PLAUSIBILITY:", "NO VIOLATIONS" if not viol else viol)
    print("\nCONTRIBUTION TO tau_k: 0.0, and it is forced, not chosen.")
    print("  " + out["why_zero"][:300])
    print("\nDECOMPOSITION OF ONE DOLLAR OF AI CAPEX, p5 / median / p95")
    for k, v in out["decomposition_of_one_dollar_of_ai_capex"].items():
        print(f"  {k:36s} {v[0]:.4f}  {v[1]:.4f}  {v[2]:.4f}")
    print("\nWAGE TAX THAT WOULD HAVE BEEN DOUBLE COUNTED, per dollar of capex")
    print(T.to_string(index=False))


if __name__ == "__main__":
    main()
