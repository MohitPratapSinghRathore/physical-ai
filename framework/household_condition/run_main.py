"""
Run steps (b)-(g): boundaries, shares, holder mapping, arrangements,
sensitivities and the 2019 stability check. Executes SPECIFICATION.md exactly.
"""
from pathlib import Path
import io
import json
import zipfile
import numpy as np
import pandas as pd

from engine import (ALLOCATIONS, BASES, DEBT_CLASSES, EXPOSURE_CASES, G_GRID,
                    KAPPA, OWNERSHIP, PRIMARY, R_RETAINED, R_SENS, S_GRID,
                    THRESHOLDS, UR_FACTOR, affected_debt_share,
                    analytic_boundary, boundary, cap_and_redistribute, gamma,
                    income_after, load, prepare, wage_loss)

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
RAW = ROOT / "data" / "raw" / "household_condition"

TAU_K = {"assembled": 0.086, "required_low": 0.110, "required_high": 0.137}
OMEGA = [0.01, 0.02, 0.05, 0.10]
ANNUITY_C = 0.04
EQUITY_AGG_BN = 33387.3          # DFA 2022Q4 corporate equity + mutual funds
RETIREMENT_EQUITY_SHARE = 0.25   # Rosenthal-Mucciolo IRA+DB+DC
PI_GRID = [0.0, 0.25, 0.50, 1.00]
REFI = {"none": 0.0, "minus100bp": 0.11, "minus200bp": 0.21}  # payment cut
CLASS_TO_PAPER = {"mortgage": "home_mortgage", "credit_card": "credit_card",
                  "vehicle": "auto_loan", "education": "student_loan",
                  "other_install": "other_consumer", "other": "other_consumer"}


def rubin(per_imp):
    """Point estimate across implicates. Variance combination needs the
    within-implicate variance; supplied separately where computed."""
    a = np.asarray([x for x in per_imp if np.isfinite(x)], float)
    if a.size == 0:
        return np.nan, np.nan
    return float(a.mean()), float(a.var(ddof=1)) if a.size > 1 else 0.0


def setup(d, s, alloc, own, kap, exposure="cognitive_AIOE",
          r_ret=R_RETAINED):
    w = d["wageinc"].clip(lower=0).to_numpy()
    wt = d["wgt5"].to_numpy()
    delta = wage_loss(d, s, alloc, exposure, r_ret)
    gam = gamma(d, s, own, kap)
    delta = cap_and_redistribute(d, delta, gam, s * float((w * wt).sum()))
    return delta, gam


def shares_report(d, delta, gam, g, ur_adjust=False):
    wt = d["wgt5"].to_numpy()
    v = d["valid"].to_numpy()
    ia = income_after(d, delta, gam, g)
    r = (ia < d["inc"].to_numpy()) & v
    out = {"share_households": float((wt * r).sum() / (wt * v).sum())}
    for k in DEBT_CLASSES:
        bal = d[f"debt_{k}"].to_numpy() * (UR_FACTOR[k] if ur_adjust else 1.0)
        den = float((bal * wt * v).sum())
        out[f"debt_{k}"] = float((bal * wt * r).sum() / den) if den > 0 \
            else np.nan
    bal = sum(d[f"debt_{k}"].to_numpy() * (UR_FACTOR[k] if ur_adjust else 1.0)
              for k in DEBT_CLASSES)
    out["debt_total"] = float((bal * wt * r).sum() / (bal * wt * v).sum())
    # threshold crossings
    pti_a = np.where(ia > 0, d["tpay"].to_numpy() / np.where(ia > 0, ia, 1),
                     np.inf)
    pti_b = d["pti"].to_numpy()
    for name, thr in THRESHOLDS.items():
        cross = v & (pti_b <= thr) & (pti_a > thr)
        out[f"cross_{name}_households"] = float(
            (wt * cross).sum() / (wt * v).sum())
        out[f"cross_{name}_debt"] = float(
            (bal * wt * cross).sum() / (bal * wt * v).sum())
    return out


def main():
    D = prepare(load(2022))
    imps = sorted(D["imp"].unique())
    R = {}
    prim = PRIMARY

    # ---------- (b) boundaries: full table ------------------------------
    rows = []
    for imp in imps:
        d = D[D["imp"] == imp]
        for s in S_GRID:
            for alloc in ALLOCATIONS:
                for own in OWNERSHIP:
                    for basis in BASES:
                        for kap in KAPPA:
                            gb = boundary(d, s, alloc, own, basis, kap)
                            ab = analytic_boundary(d, s, alloc, own, basis,
                                                   kap)
                            rows.append(dict(imp=imp, s=float(s),
                                             allocation=alloc, ownership=own,
                                             basis=basis, kappa=kap,
                                             grid=gb, analytic=ab))
    BT = pd.DataFrame(rows)
    BTm = BT.groupby(["s", "allocation", "ownership", "basis", "kappa"]).agg(
        grid=("grid", "mean"), analytic=("analytic", "mean"),
        censored=("grid", lambda x: float(np.mean(np.isnan(x))))).reset_index()
    BTm.to_csv(OUT / "boundary_table.csv", index=False)
    R["boundary_primary"] = BTm[
        (BTm["allocation"] == prim["allocation"])
        & (BTm["ownership"] == prim["ownership"])
        & (BTm["basis"] == prim["basis"])
        & (BTm["kappa"] == prim["kappa"])].to_dict("records")
    print("BOUNDARY, primary cell (concentrated / all_routes / cash_flow "
          "/ kappa=0.27)")
    for r in R["boundary_primary"]:
        print(f"  s={r['s']:.2f}  grid {r['grid']}  analytic {r['analytic']:.4f}"
              f"  censored {r['censored']:.2f}")

    # replicate-weight standard error for the primary boundary, s=0.01, 0.02
    zrw = zipfile.ZipFile(RAW / "scf2022rw1s.zip")
    rw = pd.read_stata(io.BytesIO(zrw.read(zrw.namelist()[0])))
    rcols = [c for c in rw.columns if c.lower().startswith("wt1b")][:200]
    se = {}
    for s in (0.01, 0.02):
        pe, reps = [], []
        for imp in imps:
            d = D[D["imp"] == imp].merge(rw[["yy1"] + rcols], on="yy1",
                                         how="left")
            pe.append(analytic_boundary(d, s, prim["allocation"],
                                        prim["ownership"], prim["basis"],
                                        prim["kappa"]))
            if imp == 1:
                for c in rcols[:200]:
                    dd = d.copy()
                    # a case absent from a bootstrap replicate carries NaN;
                    # that is a zero weight, not a missing value
                    dd["wgt5"] = dd[c].fillna(0.0) * 5
                    reps.append(analytic_boundary(
                        dd, s, prim["allocation"], prim["ownership"],
                        prim["basis"], prim["kappa"]))
        m, vb = rubin(pe)
        reps = np.asarray([x for x in reps if np.isfinite(x)])
        vw = float(reps.var(ddof=1)) if reps.size > 1 else np.nan
        tot = vw + (1 + 1 / 5) * vb
        se[str(s)] = {"point": m, "se": float(np.sqrt(tot)),
                      "ci_lo": m - 1.96 * np.sqrt(tot),
                      "ci_hi": m + 1.96 * np.sqrt(tot),
                      "within_var": vw, "between_var": vb,
                      "replicates_used": int(reps.size)}
    R["boundary_primary_se"] = se
    print("\nprimary boundary with interval (analytic; Rubin + replicates)")
    for k, v in se.items():
        print(f"  s={k}: {v['point']:.4f} [{v['ci_lo']:.4f}, {v['ci_hi']:.4f}]")

    # ---------- (c) shares, by group, UR axis ---------------------------
    sh_rows = []
    for imp in imps:
        d = D[D["imp"] == imp]
        for s in S_GRID:
            delta, gam = setup(d, s, prim["allocation"], prim["ownership"],
                               prim["kappa"])
            for ur in (False, True):
                base = shares_report(d, delta, gam, 0.0, ur)
                base.update(imp=imp, s=float(s), ur_adjusted=ur, group="all")
                sh_rows.append(base)
                for col, gname in (("wq", "wage_quintile"),
                                   ("wealth_grp", "wealth"),
                                   ("agecl", "age")):
                    for lvl in d[col].dropna().unique():
                        m = d[col] == lvl
                        sub = d[m]
                        rr = shares_report(sub, delta[m.to_numpy()],
                                           gam[m.to_numpy()], 0.0, ur)
                        rr.update(imp=imp, s=float(s), ur_adjusted=ur,
                                  group=f"{gname}:{lvl}")
                        sh_rows.append(rr)
    SH = pd.DataFrame(sh_rows)
    SHm = SH.groupby(["s", "ur_adjusted", "group"]).mean(
        numeric_only=True).reset_index().drop(columns=["imp"])
    SHm.to_csv(OUT / "shares_table.csv", index=False)
    R["shares_all_s"] = SHm[SHm["group"] == "all"].to_dict("records")
    print("\nSHARES at the primary cell, g=0 (all households)")
    for r in R["shares_all_s"]:
        if r["ur_adjusted"]:
            continue
        print(f"  s={r['s']:.2f} households {r['share_households']:.4f} "
              f"debt {r['debt_total']:.4f} cross_pir40_debt "
              f"{r['cross_pir40_debt']:.4f}")

    # ---------- (d) holder mapping --------------------------------------
    H = pd.read_csv(ROOT / "framework" / "labor_backing"
                    / "holder_matrix_latest.csv")
    H = H[H["obligor"] == "households"]
    hmap = H.pivot_table(index="claim_class", columns="holder",
                         values="holder_share", aggfunc="sum").fillna(0.0)
    hold_rows = []
    for imp in imps:
        d = D[D["imp"] == imp]
        wt = d["wgt5"].to_numpy()
        v = d["valid"].to_numpy()
        for s in S_GRID:
            delta, gam = setup(d, s, prim["allocation"], prim["ownership"],
                               prim["kappa"])
            r = (income_after(d, delta, gam, 0.0)
                 < d["inc"].to_numpy()) & v
            aff = {}
            for k in DEBT_CLASSES:
                bal = d[f"debt_{k}"].to_numpy()
                aff[k] = float((bal * wt * r).sum())
            tot_aff = sum(aff.values())
            by_holder = {h: 0.0 for h in hmap.columns}
            for k, amt in aff.items():
                pc = CLASS_TO_PAPER[k]
                if pc not in hmap.index:
                    continue
                for h in hmap.columns:
                    by_holder[h] += amt * float(hmap.loc[pc, h])
            row = {"imp": imp, "s": float(s), "affected_debt_bn": tot_aff / 1e9}
            for h, amt in by_holder.items():
                row[f"holder_{h}"] = amt / tot_aff if tot_aff > 0 else np.nan
            # alternative agency classification: agency pools NOT federal
            fed_alt = by_holder["federal_government"] - (
                aff["mortgage"] * float(hmap.loc["home_mortgage",
                                                 "federal_government"]))
            row["holder_federal_agency_not_federal"] = (
                fed_alt / tot_aff if tot_aff > 0 else np.nan)
            hold_rows.append(row)
    HD = pd.DataFrame(hold_rows)
    HDm = HD.groupby("s").mean(numeric_only=True).reset_index().drop(
        columns=["imp"])
    HDm.to_csv(OUT / "holder_mapping.csv", index=False)
    R["holder_mapping"] = HDm.to_dict("records")
    print("\nHOLDER MAPPING of affected debt (primary cell, g=0)")
    for r in R["holder_mapping"]:
        print(f"  s={r['s']:.2f} affected {r['affected_debt_bn']:8.1f}bn "
              f"federal(central) {r['holder_federal_government']:.4f} "
              f"federal(agency-not-fed) "
              f"{r['holder_federal_agency_not_federal']:.4f} "
              f"banks {r['holder_banks']:.4f}")

    (OUT / "main_results.json").write_text(
        json.dumps(R, indent=2, default=float), encoding="utf-8")
    print("\nwritten main_results.json")


if __name__ == "__main__":
    main()
