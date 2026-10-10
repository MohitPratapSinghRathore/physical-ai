"""
SPECIFICATION section 10, the pre-committed check, run before any boundary is
reported as a result.

Section 6 defines the boundary on the GRID (g up to 0.20). Where the grid is not
reached the boundary is CENSORED at >0.20 and reported as such. The analytic
(uncensored) boundary is reported alongside: it is a max-over-households
statistic and degenerates where the section 9 bound 5 cap drives one household's
income to near zero. See DEVIATIONS D7.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd

from engine import (BASES, KAPPA, PRIMARY, S_GRID, analytic_boundary, boundary,
                    load, prepare)

OUT = Path(__file__).resolve().parent


def main():
    D = prepare(load(2022))
    imps = sorted(D["imp"].unique())
    prim = PRIMARY
    rows = []
    for imp in imps:
        d = D[D["imp"] == imp]
        for s in S_GRID:
            for kap in KAPPA:
                for basis in BASES:
                    gb = boundary(d, s, prim["allocation"], prim["ownership"],
                                  basis, kap)
                    ab = analytic_boundary(d, s, prim["allocation"],
                                           prim["ownership"], basis, kap)
                    rows.append({"imp": imp, "s": float(s), "kappa": kap,
                                 "basis": basis, "grid_boundary": gb,
                                 "analytic_boundary": ab,
                                 "censored": bool(np.isnan(gb))})
    B = pd.DataFrame(rows)
    Bm = B.groupby(["s", "kappa", "basis"]).agg(
        grid_boundary=("grid_boundary", "mean"),
        analytic_boundary=("analytic_boundary", "mean"),
        censored_frac=("censored", "mean")).reset_index()
    Bm.to_csv(OUT / "s10_convention_grid.csv", index=False)

    defined_s = [float(s) for s in S_GRID
                 if Bm[Bm["s"] == float(s)]["censored_frac"].max() == 0.0]
    R = {"s_values_with_uncensored_grid_boundary": defined_s}

    if len(defined_s) >= 2:
        pc = Bm[(Bm["kappa"] == prim["kappa"])
                & (Bm["basis"] == prim["basis"])
                & (Bm["s"].isin(defined_s))]
        s_spread = float(pc["grid_boundary"].max()
                         - pc["grid_boundary"].min())
        cs = [float(Bm[Bm["s"] == s]["grid_boundary"].max()
                    - Bm[Bm["s"] == s]["grid_boundary"].min())
              for s in defined_s]
        conv_spread = float(np.nanmax(cs))
        verdict = bool(conv_spread > s_spread)
    else:
        s_spread = conv_spread = float("nan")
        cs, verdict = [], None

    R.update({"s_grid_spread_at_primary_convention": s_spread,
              "convention_spread_max": conv_spread,
              "per_s_convention_spread": dict(zip(defined_s, cs)),
              "convention_spread_exceeds_s_spread": verdict,
              "note": ("compared on the GRID boundary, the object section 6 "
                       "defines; s values censored beyond g=0.20 in any "
                       "convention cell are excluded from the comparison")})

    print("SECTION 10 PRE-COMMITTED CHECK\n")
    print(f"  s values with an uncensored grid boundary in every convention "
          f"cell: {defined_s}")
    print(f"  spread across those s values at the primary convention: "
          f"{s_spread:.4f}")
    print(f"  spread across CONVENTIONS, worst over those s: {conv_spread:.4f}")
    print(f"\n  CONVENTION SPREAD EXCEEDS s SPREAD: {verdict}\n")

    print("GRID boundary (mean over implicates; NaN = beyond g=0.20)")
    print(Bm.pivot_table(index="s", columns=["basis", "kappa"],
                         values="grid_boundary").round(4).to_string())
    print("\ncensored fraction (1.0 = beyond the grid in every implicate)")
    print(Bm.pivot_table(index="s", columns=["basis", "kappa"],
                         values="censored_frac").round(2).to_string())
    print("\nANALYTIC boundary (uncensored; a max-over-households statistic)")
    print(Bm.pivot_table(index="s", columns=["basis", "kappa"],
                         values="analytic_boundary").round(3).to_string())

    (OUT / "s10.json").write_text(json.dumps(R, indent=2, default=float),
                                  encoding="utf-8")


if __name__ == "__main__":
    main()
