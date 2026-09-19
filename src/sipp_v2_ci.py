"""Item 4 fix 3: 95 percent confidence intervals from the SIPP replicate weights.

SIPP 2018+ uses Fay's balanced repeated replication with rho = 0.5 and 240 replicates. The
variance of an estimate theta is

    V(theta) = (1 / (240 * (1 - rho)^2)) * sum_r (theta_r - theta)^2
             = (1 / 60) * sum_r (theta_r - theta)^2   for rho = 0.5

Computed on the restricted sample (household with an employed member, reference person aged
25 to 64), for every pathway-level figure that the write-up quotes.
"""
import io, json, pathlib, zipfile
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).parents[1]
RAW, OUT = ROOT / "data" / "raw", ROOT / "data" / "processed"
SIPP = RAW / "sipp"
RHO, NREP = 0.5, 240
import importlib.util
spec = importlib.util.spec_from_file_location("sb2", ROOT / "src" / "sipp_buffers_v2.py")
sb2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(sb2)


def load_rep():
    z = zipfile.ZipFile(SIPP / "rw2025_csv.zip")
    fn = z.namelist()[0]
    cols = ["ssuid", "pnum", "monthcode"] + [f"repwgt{i}" for i in range(1, NREP + 1)]
    parts = []
    with z.open(fn) as fh:
        for ch in pd.read_csv(io.TextIOWrapper(fh, encoding="utf-8", errors="replace"),
                              sep="|", usecols=cols, chunksize=200_000, low_memory=False):
            parts.append(ch[ch["monthcode"] == 12])
    R = pd.concat(parts, ignore_index=True)
    R["key"] = R["ssuid"].astype(str) + "|" + R["pnum"].astype(str)
    return R.set_index("key")[[f"repwgt{i}" for i in range(1, NREP + 1)]]


def main():
    D, _ = sb2.load()
    hh = sb2.build_hh(D)
    ref = D[pd.to_numeric(D["ERELRPE"], errors="coerce").isin([1, 2])]
    ref = ref.sort_values("WPFINWGT").groupby("hh").tail(1)
    hh["key"] = ref.set_index("hh").reindex(hh.index).apply(
        lambda r: f"{r['SSUID']}|{r['PNUM']}", axis=1)

    R = load_rep()
    print(f"replicate weight rows (Dec): {len(R):,}")
    RW = R.reindex(hh["key"]).to_numpy(float)
    ok = np.isfinite(RW).all(axis=1)
    print(f"households matched to replicate weights: {ok.sum():,} of {len(hh):,} "
          f"({100*ok.mean():.1f}%)")

    S = hh[(hh["any_employed"]) & hh["ref_age"].between(25, 64)].copy()
    idx = np.array([hh.index.get_loc(i) for i in S.index])
    RWs = RW[idx]
    w0 = S["wgt"].to_numpy(float)
    keep = np.isfinite(RWs).all(axis=1)
    S, RWs, w0 = S[keep], RWs[keep], w0[keep]
    print(f"restricted sample with replicate weights: {len(S):,}")

    groups = {"driving": S["driving"], "gated": S["gated"],
              "manipulation": S["manipulation"], "all_embodied": S["any_embodied"],
              "no_embodied_worker": ~S["any_embodied"]}

    def dti(d, w, col):
        ti = float((d["hh_inc_a"] * w).sum())
        return 100 * float((d[col].fillna(0) * w).sum()) / ti if ti else np.nan

    def share(d, w, mask):
        return 100 * float(w[mask].sum()) / float(w.sum()) if w.sum() else np.nan

    METRICS = {
        "dti_vehicle": lambda d, w: dti(d, w, "vehicle"),
        "dti_credit_card": lambda d, w: dti(d, w, "credit_card"),
        "dti_medical": lambda d, w: dti(d, w, "medical"),
        "dti_unsecured_total": lambda d, w: dti(d, w, "unsecured_total"),
        "dti_mortgage": lambda d, w: dti(d, w, "mortgage"),
        "dti_all_debt": lambda d, w: dti(d, w, "all_debt"),
        "buffer_under_1mo_income": lambda d, w: share(
            d, w, (d["liquid_bank"].fillna(0)
                   < d["hh_inc_m"].replace(0, np.nan)).fillna(True).to_numpy()),
    }

    rows = []
    for g, m in groups.items():
        mm = m.to_numpy(bool)
        d = S[mm]
        for name, fn in METRICS.items():
            pt = fn(d, w0[mm])
            reps = np.array([fn(d, RWs[mm][:, r]) for r in range(NREP)])
            v = float(np.nansum((reps - pt) ** 2) / (NREP * (1 - RHO) ** 2))
            se = np.sqrt(v)
            rows.append({"group": g, "metric": name, "n_unweighted": int(mm.sum()),
                         "estimate": pt, "se": se,
                         "ci_low": pt - 1.96 * se, "ci_high": pt + 1.96 * se,
                         "thin_cell": bool(mm.sum() < 100)})
    T = pd.DataFrame(rows)
    T.round(3).to_csv(OUT / "sipp_v2_ci.csv", index=False)

    # gaps vs the no-embodied base, with CIs on the difference
    base = (~S["any_embodied"]).to_numpy(bool)
    grows = []
    for g in ["driving", "gated", "manipulation", "all_embodied"]:
        mm = groups[g].to_numpy(bool)
        for name, fn in METRICS.items():
            pt = fn(S[mm], w0[mm]) - fn(S[base], w0[base])
            reps = np.array([fn(S[mm], RWs[mm][:, r]) - fn(S[base], RWs[base][:, r])
                             for r in range(NREP)])
            v = float(np.nansum((reps - pt) ** 2) / (NREP * (1 - RHO) ** 2))
            se = np.sqrt(v)
            grows.append({"group": g, "metric": name, "gap": pt, "se": se,
                          "ci_low": pt - 1.96 * se, "ci_high": pt + 1.96 * se,
                          "significant": bool(abs(pt) > 1.96 * se)})
    G = pd.DataFrame(grows)
    G.round(3).to_csv(OUT / "sipp_v2_ci_gaps.csv", index=False)
    (OUT / "sipp_v2_ci_summary.json").write_text(json.dumps(
        {"levels": T.round(4).to_dict("records"),
         "gaps_vs_no_embodied": G.round(4).to_dict("records")}, indent=2))

    pd.set_option("display.width", 220)
    print("\n=== GAPS vs households with no embodied worker, 95% CI (replicate weights) ===")
    print(G.round(2).to_string(index=False))


if __name__ == "__main__":
    main()
