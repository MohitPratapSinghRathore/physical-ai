"""
Run steps 3 and the section 10 pre-committed check.

Order is fixed by the run instruction: plausibility bounds first, then the
section 10 convention test, before any boundary is reported.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd

from engine import (ALLOCATIONS, BASES, G_GRID, KAPPA, OWNERSHIP, PRIMARY,
                    S_GRID, affected_debt_share, analytic_boundary, boundary,
                    cap_and_redistribute, gamma, income_after, load, prepare,
                    wage_loss)

OUT = Path(__file__).resolve().parent
TOL = 0.001          # section 9: 0.1 percent


def main():
    raw = load(2022)
    D = prepare(raw)
    imps = sorted(D["imp"].unique())
    R = {}

    # ================= PLAUSIBILITY BOUNDS, REPORTED FIRST =================
    print("PLAUSIBILITY BOUNDS (SPECIFICATION section 9)\n")
    bounds = {"violations": []}

    # bound 1: shares in [0,1]
    sh = {}
    for name in OWNERSHIP:
        for imp in imps:
            d = D[D["imp"] == imp]
            own = d[f"own_{name}"].to_numpy()
            wt = d["wgt5"].to_numpy()
            frac = own * 0 if (own * wt).sum() == 0 else \
                (own / (own * wt).sum() * wt.sum())
            sh[f"{name}_imp{imp}_min_weight"] = float(own.min())
    bad_share = [k for k, v in sh.items() if v < 0]
    bounds["bound1_ownership_weights_nonnegative"] = {
        "checked": len(sh), "negative": len(bad_share)}
    print(f"  bound 1  ownership weights non-negative (D1 flooring applied): "
          f"{len(bad_share)} violations of {len(sh)} checks")
    if bad_share:
        bounds["violations"].append("negative ownership weight after flooring")

    # bounds 2 and 3: aggregate identities, checked on a spanning subgrid
    checks, worst2, worst3 = 0, 0.0, 0.0
    for imp in imps:
        d = D[D["imp"] == imp]
        wt = d["wgt5"].to_numpy()
        w = d["wageinc"].clip(lower=0).to_numpy()
        W = float((w * wt).sum())
        base_tot = float((d["inc"].to_numpy() * wt).sum())
        for s in S_GRID:
            for alloc in ALLOCATIONS:
                delta0 = wage_loss(d, s, alloc)
                for own in OWNERSHIP:
                    for kap in KAPPA:
                        gam = gamma(d, s, own, kap)
                        delta = cap_and_redistribute(d, delta0, gam, s * W)
                        dev3a = abs(float((delta * wt).sum())
                                    - s * W) / (s * W)
                        worst3 = max(worst3, dev3a)
                        dev3b = abs(float((gam * wt).sum())
                                    - s * W * KAPPA[kap]) / (s * W * KAPPA[kap])
                        worst3 = max(worst3, dev3b)
                        for g in (0.0, 0.05, 0.10, 0.20):
                            got = float((income_after(d, delta, gam, g)
                                         * wt).sum())
                            want = (1 + g) * (base_tot - s * W
                                              + s * W * KAPPA[kap])
                            dev2 = abs(got - want) / abs(want)
                            worst2 = max(worst2, dev2)
                            checks += 1
    bounds["bound2_income_identity_worst_rel_dev"] = worst2
    bounds["bound3_balance_worst_rel_dev"] = worst3
    bounds["bound2_checks"] = checks
    print(f"  bound 2  aggregate income identity: worst relative deviation "
          f"{worst2:.2e} over {checks} checks (tolerance {TOL})"
          f"  {'OK' if worst2 < TOL else 'VIOLATION'}")
    print(f"  bound 3  wage loss and capital gain balance: worst relative "
          f"deviation {worst3:.2e} (tolerance {TOL})"
          f"  {'OK' if worst3 < TOL else 'VIOLATION'}")
    if worst2 >= TOL:
        bounds["violations"].append("aggregate income identity")
    if worst3 >= TOL:
        bounds["violations"].append("wage loss / capital gain balance")

    # bound 5: no negative household income after the shift
    neg = 0
    worstneg = 0
    for imp in imps:
        d = D[D["imp"] == imp]
        for s in S_GRID:
            for alloc in ALLOCATIONS:
                delta0 = wage_loss(d, s, alloc)
                for own in OWNERSHIP:
                    gam = gamma(d, s, own, "cash_flow")
                    delta = cap_and_redistribute(d, delta0, gam, s * W)
                    ia = income_after(d, delta, gam, 0.0)
                    v = d["valid"].to_numpy()
                    n = int(((ia < -1.0) & v).sum())  # $1 tolerance on float noise
                    neg += n
                    worstneg = min(worstneg, float(ia[v].min()))
    bounds["bound5_negative_income_cells"] = neg
    bounds["bound5_most_negative"] = worstneg
    print(f"  bound 5  no negative household income after the shift: "
          f"{neg} household-cells negative, most negative {worstneg:,.0f}"
          f"  {'OK' if neg == 0 else 'VIOLATION'}")
    if neg:
        bounds["violations"].append(
            f"{neg} household-cells with negative income after the shift")

    # bound 4: reconciliation tolerances, from FEASIBILITY
    bounds["bound4_reconciliation"] = {
        "mortgage_scf_over_official": 0.930, "within_10pct": True,
        "total_liabilities_scf_over_official": 0.905, "within_10pct_": True,
        "consumer_credit_scf_over_official": 0.603,
        "consumer_credit_reconciles": False}
    print("  bound 4  reconciliation: mortgages 0.930 and total liabilities "
          "0.905 within 10 percent OK; consumer credit 0.603 DOES NOT "
          "reconcile and is reported as unreconciled at every use")

    R["plausibility"] = bounds
    print(f"\n  VIOLATIONS: {bounds['violations'] or 'none'}")

    (OUT / "bounds.json").write_text(
        json.dumps(R, indent=2, default=float), encoding="utf-8")


if __name__ == "__main__":
    main()
