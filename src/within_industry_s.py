"""Item 2: does S predict robot adoption with industry composition held fixed?

The concern: S may be a proxy for "works in manufacturing". A3 found adoption rises in
S_rank among high-P occupations (Spearman +0.419), but the adoption measure is built from
sector-level capex, so the test may carry no within-industry information at all.

STRUCTURAL PROBLEM, stated before any result. The occupation-level adoption measure is

    robot_exposure(occ) = sum_i share_i(occ) * intensity_i

where intensity_i varies only across 2-digit NAICS sectors. It is therefore a deterministic
linear function of the occupation's industry mix. Regressing it on the full NAICS2 share
vector must return R-squared = 1 and leave exactly zero residual variation for S to explain.
The test specified in item 2(a) is, for this dependent variable, vacuous by construction.

That is itself the finding: the ACES-based measure has no within-industry variation, so
A3 can only ever establish that high-S occupations are concentrated in robot-intensive
sectors. It cannot distinguish that from S being a sector proxy.

What CAN be run, and is:
  T1  control for manufacturing employment share alone (one covariate, leaves variation)
  T2  the mechanical check: R-squared of robot_exposure on the full NAICS2 share vector
  T3  within-manufacturing and within-non-manufacturing subsamples
  T4  the dominant-sector test: within occupations sharing the same dominant sector, does
      S still order adoption?
"""
import io, json, pathlib, zipfile
import numpy as np
import pandas as pd
from scipy import stats

ROOT = pathlib.Path(__file__).parents[1]
RAW, OUT = ROOT / "data" / "raw", ROOT / "data" / "processed"


def partial_spearman(x, y, z):
    """Spearman partial correlation of x and y controlling for columns z (2D)."""
    rx = stats.rankdata(x); ry = stats.rankdata(y)
    Z = np.column_stack([np.ones(len(rx))] + [stats.rankdata(c) for c in z.T])
    bx = np.linalg.lstsq(Z, rx, rcond=None)[0]
    by = np.linalg.lstsq(Z, ry, rcond=None)[0]
    ex = rx - Z @ bx
    ey = ry - Z @ by
    n, k = len(rx), Z.shape[1]
    r = float(np.corrcoef(ex, ey)[0, 1])
    if abs(r) >= 1 or n - k - 1 <= 0:
        return r, np.nan
    t = r * np.sqrt((n - k - 1) / (1 - r ** 2))
    return r, float(2 * (1 - stats.t.cdf(abs(t), n - k - 1)))


def main():
    import importlib.util
    spec = importlib.util.spec_from_file_location("anchor_c", ROOT / "src" / "anchor_c.py")
    ac = importlib.util.module_from_spec(spec); spec.loader.exec_module(ac)

    aces = ac.aces_sectors()
    cw = ac.indp_to_naics2()
    oi = ac.pums_occ_ind().merge(cw, on="indp", how="left")
    sec_emp = (oi[oi["naics2"].notna()].groupby("naics2")["emp"].sum()
               .rename("sector_emp").reset_index())
    n2i = {}
    for _, r in aces.iterrows():
        s = ac.naics2_set(r["naics"])
        e = sec_emp[sec_emp["naics2"].isin(s)]["sector_emp"].sum()
        if e > 0:
            v = r["capex_musd"] * 1e6 / e
            for n in s:
                n2i[n] = max(n2i.get(n, 0.0), v)
    oi["intensity"] = oi["naics2"].map(n2i)

    # occupation x sector employment shares
    d = oi[oi["naics2"].notna()].copy()
    tot = d.groupby("occp")["emp"].sum().rename("tot")
    d = d.merge(tot, on="occp")
    d["share"] = d["emp"] / d["tot"]
    shares = d.pivot_table(index="occp", columns="naics2", values="share",
                           aggfunc="sum").fillna(0.0)

    dd = d[d["intensity"].notna()]
    rob = (dd.groupby("occp")
           .apply(lambda g: pd.Series({"robot_exposure": float(
               np.average(g["intensity"], weights=g["emp"]))}), include_groups=False))

    grid = pd.read_csv(OUT / "paei_c.csv")
    base = grid[grid["c"] == 0.0][["occp", "title", "embodiment_P", "structure_S",
                                   "structure_S_rank", "employment"]]
    M = (base.merge(rob, on="occp", how="inner")
              .merge(shares, on="occp", how="left"))
    M = M[M["employment"].notna() & (M["employment"] > 0)].copy()
    naics_cols = [c for c in shares.columns]
    M[naics_cols] = M[naics_cols].fillna(0.0)

    MFG = [c for c in naics_cols if c in ("31", "32", "33")]
    M["mfg_share"] = M[MFG].sum(axis=1) if MFG else 0.0
    M["dominant"] = M[naics_cols].idxmax(axis=1)

    P_MED = float(M["embodiment_P"].median())
    hi = M[M["embodiment_P"] >= P_MED].copy()
    print(f"occupations: {len(M)}; high-P (P >= {P_MED:.3f}): {len(hi)}")
    print(f"sectors with an ACES intensity: {len(set(n2i))} NAICS2 codes\n")

    res = {}

    # ---- T2 first: the mechanical check ----
    X = np.column_stack([np.ones(len(M))] + [M[c].to_numpy() for c in naics_cols])
    y = M["robot_exposure"].to_numpy()
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    r2_full = 1 - ((y - X @ beta) ** 2).sum() / ((y - y.mean()) ** 2).sum()
    Xm = np.column_stack([np.ones(len(M)), M["mfg_share"].to_numpy()])
    bm, *_ = np.linalg.lstsq(Xm, y, rcond=None)
    r2_mfg = 1 - ((y - Xm @ bm) ** 2).sum() / ((y - y.mean()) ** 2).sum()
    res["T2_mechanical"] = {"r2_robot_exposure_on_full_naics2_mix": float(r2_full),
                            "r2_robot_exposure_on_mfg_share_only": float(r2_mfg)}
    print("=== T2 mechanical check ===")
    print(f"  R2 of robot_exposure on FULL NAICS2 share vector : {r2_full:.6f}")
    print(f"  R2 of robot_exposure on manufacturing share only : {r2_mfg:.4f}")
    print("  (an R2 at or near 1.0 means item 2(a)'s full-mix control is vacuous "
          "by construction)\n")

    # ---- T1 partial correlation controlling for manufacturing share ----
    print("=== T1 partial Spearman(S_rank, robot_exposure | mfg share) ===")
    for lab, dfx in [("all", M), ("high-P", hi)]:
        raw = stats.spearmanr(dfx["structure_S_rank"], dfx["robot_exposure"])
        pr, pp = partial_spearman(dfx["structure_S_rank"].to_numpy(),
                                  dfx["robot_exposure"].to_numpy(),
                                  dfx[["mfg_share"]].to_numpy())
        res[f"T1_{lab}"] = {"n": int(len(dfx)), "raw_spearman": float(raw[0]),
                            "raw_p": float(raw[1]), "partial_spearman": pr,
                            "partial_p": pp}
        print(f"  {lab:7s} n={len(dfx):4d}  raw {raw[0]:+.3f} (p={raw[1]:.2e})  "
              f"-> partial {pr:+.3f} (p={pp:.3f})")

    # ---- T3 within manufacturing / non-manufacturing ----
    print("\n=== T3 subsamples by dominant sector ===")
    hi = hi.copy()
    hi["is_mfg"] = hi["dominant"].isin(["31", "32", "33"])
    for lab, dfx in [("high-P, dominant sector = manufacturing", hi[hi["is_mfg"]]),
                     ("high-P, dominant sector = non-manufacturing", hi[~hi["is_mfg"]])]:
        if len(dfx) < 12:
            print(f"  {lab}: n={len(dfx)}, too few to test")
            res[f"T3_{lab[:24]}"] = {"n": int(len(dfx)), "note": "too few"}
            continue
        r = stats.spearmanr(dfx["structure_S_rank"], dfx["robot_exposure"])
        res[f"T3_{lab[:24]}"] = {"n": int(len(dfx)), "spearman": float(r[0]),
                                 "p": float(r[1])}
        print(f"  {lab}: n={len(dfx)}, Spearman {r[0]:+.3f} (p={r[1]:.3f})")

    # ---- T4 within dominant sector, demeaned ----
    print("\n=== T4 within dominant sector (both variables demeaned by sector) ===")
    for lab, dfx in [("all", M), ("high-P", hi)]:
        g = dfx.groupby("dominant")
        sx = dfx["structure_S_rank"] - g["structure_S_rank"].transform("mean")
        sy = dfx["robot_exposure"] - g["robot_exposure"].transform("mean")
        keep = g["occp"].transform("size") >= 5
        sx, sy = sx[keep], sy[keep]
        if len(sx) < 12 or sy.std() == 0:
            print(f"  {lab}: no usable within-sector variation "
                  f"(n={len(sx)}, sd(y)={sy.std():.3g})")
            res[f"T4_{lab}"] = {"n": int(len(sx)), "sd_y": float(sy.std()),
                                "note": "no within-sector variation in the DV"}
            continue
        r = stats.spearmanr(sx, sy)
        res[f"T4_{lab}"] = {"n": int(len(sx)), "spearman": float(r[0]), "p": float(r[1]),
                            "sd_y": float(sy.std())}
        print(f"  {lab}: n={len(sx)}, within-sector Spearman {r[0]:+.3f} "
              f"(p={r[1]:.3f}), sd(demeaned y)={sy.std():.4g}")

    (OUT / "within_industry_s.json").write_text(json.dumps(res, indent=2))
    M.round(5).to_csv(OUT / "within_industry_s_panel.csv", index=False)
    print("\nwrote data/processed/within_industry_s.json")


if __name__ == "__main__":
    main()
