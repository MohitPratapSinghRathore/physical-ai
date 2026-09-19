"""Item 2, second half: does the proportionality result hold for vehicle debt?

The project has repeatedly found that mortgage obligations track the wage bill roughly
one for one. Vehicle debt is the case where proportionality is EXPECTED TO FAIL, because
A30/A31 found vehicle debt concentrated in the driving pathway and NEGATIVE for the
manipulation pathway.

Same two tests as src/shares_and_proportionality.py, so the results are comparable:
  (a) lean = group share of the debt divided by group share of household EARNINGS
  (b) k through the origin, and its stability across earnings deciles

IMPORTANT NON-COMPARABILITY: SIPP carries debt BALANCES, ACS carries monthly SERVICE.
Levels of k are therefore not comparable across the two sources. Leans and decile
stability are.

CAVEAT on every cognitive figure: AIOE and Eloundou measure TASK OVERLAP, not displacement
and not timing; top-quintile occupations include likely-augmented work.
"""
import json, pathlib
import numpy as np
import pandas as pd
import importlib.util

ROOT = pathlib.Path(__file__).parents[1]
OUT = ROOT / "data" / "processed"


def _mod(name, fn):
    s = importlib.util.spec_from_file_location(name, ROOT / "src" / fn)
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
    return m


sb2 = _mod("sb2", "sipp_buffers_v2.py")
cc = _mod("cc", "cognitive_contrast.py")


def prop_stats(d, ycol, xcol, wcol, label):
    dd = d[(d[ycol] > 0) & (d[xcol] > 0)]
    if len(dd) < 50:
        return None
    y, x, w = (dd[ycol].to_numpy(float), dd[xcol].to_numpy(float),
               dd[wcol].to_numpy(float))
    k = float((y * w).sum() / (x * w).sum())
    q = pd.qcut(dd[xcol], 10, labels=False, duplicates="drop").to_numpy()
    ks = []
    for i in range(int(q.max()) + 1):
        s = q == i
        den = float((x[s] * w[s]).sum())
        if den > 0:
            ks.append(float((y[s] * w[s]).sum()) / den)
    ks = np.array(ks)
    sw = np.sqrt(w)
    Xm = np.column_stack([np.ones(len(x)), x])
    b, *_ = np.linalg.lstsq(Xm * sw[:, None], y * sw, rcond=None)
    return {**label, "n": int(len(dd)), "k_through_origin": k,
            "k_decile_min": float(ks.min()), "k_decile_max": float(ks.max()),
            "k_decile_cv": float(ks.std() / ks.mean()),
            "k_decile_ratio_max_min": float(ks.max() / ks.min()),
            "intercept_share_of_mean_y": float(b[0] / y.mean())}


def main():
    B, groups, _cuts = cc.build_groups()
    D, _ = sb2.load()
    hh = sb2.build_hh(D)
    D["hh"] = D["SSUID"].astype(str) + "_" + D["ERESIDENCEID"].astype(str)

    # household EARNINGS, the denominator the proportionality rule is stated against
    earn = (pd.to_numeric(D["TPEARN"], errors="coerce").fillna(0.0)
            .groupby(D["hh"]).sum() * 12.0)
    hh["hh_earn_a"] = earn.reindex(hh.index).fillna(0.0)

    for g, s in groups.items():
        hh[g] = D[D["occ"].isin(s)].groupby("hh").size().reindex(hh.index).fillna(0) > 0

    R = hh[hh["any_employed"] & hh["ref_age"].between(25, 64)].copy()
    R["unsecured_plus_veh"] = (R["unsecured_total"].fillna(0) + R["vehicle"].fillna(0))
    print(f"SIPP working-core households: {len(R):,} unweighted, "
          f"{R['wgt'].sum()/1e6:,.2f}m weighted")

    cogn_keys = [g for g in groups if g.startswith("cognitive")]
    emb_key = "embodied" if "embodied" in groups else [g for g in groups if "embod" in g][0]

    # ---- leans against the EARNINGS share ----
    te = float((R["hh_earn_a"] * R["wgt"]).sum())
    lean_rows = []
    for g in list(groups):
        d = R[R[g]]
        we = float((d["hh_earn_a"] * d["wgt"]).sum())
        row = {"group": g, "n": int(len(d)),
               "earnings_share_pct": 100 * we / te}
        for lab in ["vehicle", "mortgage", "unsecured_total", "credit_card",
                    "unsecured_plus_veh"]:
            tot = float((R[lab].fillna(0) * R["wgt"]).sum())
            sh = 100 * float((d[lab].fillna(0) * d["wgt"]).sum()) / tot if tot else np.nan
            row[f"{lab}_share_pct"] = sh
            row[f"{lab}_lean"] = sh / row["earnings_share_pct"] if row["earnings_share_pct"] else np.nan
        lean_rows.append(row)
    L = pd.DataFrame(lean_rows)
    L.round(3).to_csv(OUT / "vehicle_leans.csv", index=False)

    # ---- proportionality of k ----
    rows = []
    for g in list(groups):
        d = R[R[g]]
        for lab in ["vehicle", "mortgage", "unsecured_total"]:
            r = prop_stats(d.assign(**{lab: d[lab].fillna(0.0)}), lab, "hh_earn_a",
                           "wgt", {"group": g, "outcome": lab})
            if r:
                rows.append(r)
    P = pd.DataFrame(rows)
    P.round(5).to_csv(OUT / "vehicle_proportionality.csv", index=False)
    (OUT / "vehicle_proportionality.json").write_text(json.dumps(
        {"leans": L.round(3).to_dict("records"),
         "proportionality": P.round(5).to_dict("records")}, indent=2))

    pd.set_option("display.width", 240)
    print("\n=== LEANS against the earnings share, SIPP balances, working core ===")
    print(L[["group", "n", "earnings_share_pct", "vehicle_share_pct", "vehicle_lean",
             "mortgage_share_pct", "mortgage_lean", "unsecured_total_lean"]]
          .round(3).to_string(index=False))
    print("\n=== PROPORTIONALITY of k = balance per dollar of annual earnings ===")
    print(P[["group", "outcome", "n", "k_through_origin", "k_decile_min", "k_decile_max",
             "k_decile_ratio_max_min", "k_decile_cv", "intercept_share_of_mean_y"]]
          .round(4).to_string(index=False))


if __name__ == "__main__":
    main()
