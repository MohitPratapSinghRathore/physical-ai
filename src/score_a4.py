"""A4 step 2: inter-rater agreement, and correlation of a text-built S against S_original.

S_text is built from the four rated dimensions. The rubric is written so that HIGH on every
dimension means MORE structured, which is the same orientation as S_original, so S_text is
the simple mean of the four normalised dimensions.

Two things are reported and they answer different questions:
  RELIABILITY   do two independent raters agree? (Krippendorff alpha, ICC, Pearson)
  VALIDITY      does the text-built S agree with the descriptor-built S_original?

The decision rule from the owner: if the correlation between S_original and S_text is below
about 0.5, treat S_original as unreliable and switch to whichever version is better
validated by the A3 adoption test.
"""
import json, pathlib
import numpy as np
import pandas as pd
from scipy import stats

ROOT = pathlib.Path(__file__).parents[1]
OUT = ROOT / "data" / "processed"
A4 = OUT / "a4"
DIMS = ["predictability", "object_variability", "workspace_access", "improvisation"]


def krippendorff_alpha_interval(m):
    """Krippendorff's alpha for interval data, 2 raters x n items, no missing."""
    n_items = m.shape[1]
    pairs = []
    for j in range(n_items):
        col = m[:, j]
        col = col[np.isfinite(col)]
        for a in range(len(col)):
            for b in range(len(col)):
                if a != b:
                    pairs.append((col[a], col[b]))
    pairs = np.array(pairs, float)
    Do = np.mean((pairs[:, 0] - pairs[:, 1]) ** 2)
    vals = m[np.isfinite(m)].ravel()
    De = np.mean([(x - y) ** 2 for x in vals for y in vals]) if len(vals) < 400 else \
        2 * np.var(vals)
    return 1.0 - Do / De if De else np.nan


def icc21(x, y):
    """ICC(2,1) two-way random, single measure, absolute agreement, k=2."""
    M = np.vstack([x, y]).T
    n, k = M.shape
    gm = M.mean()
    ms_r = k * ((M.mean(axis=1) - gm) ** 2).sum() / (n - 1)
    ms_c = n * ((M.mean(axis=0) - gm) ** 2).sum() / (k - 1)
    ms_e = ((M - M.mean(axis=1, keepdims=True) - M.mean(axis=0, keepdims=True) + gm) ** 2
            ).sum() / ((n - 1) * (k - 1))
    return float((ms_r - ms_e) / (ms_r + (k - 1) * ms_e + k * (ms_c - ms_e) / n))


def main():
    key = pd.read_csv(A4 / "a4_key.csv")
    r1 = pd.DataFrame(json.loads((A4 / "a4_ratings_rater1.json").read_text()))
    r2 = pd.DataFrame(json.loads((A4 / "a4_ratings_rater2.json").read_text()))
    print(f"rater1 {len(r1)} items, rater2 {len(r2)} items, key {len(key)} items")

    m = key.merge(r1, on="item_id", suffixes=("", "_r1")).merge(
        r2, on="item_id", suffixes=("_r1", "_r2"))
    print(f"merged: {len(m)} items")

    # ---- reliability per dimension ----
    rel = {}
    for d in DIMS:
        a, b = m[f"{d}_r1"].to_numpy(float), m[f"{d}_r2"].to_numpy(float)
        rel[d] = {
            "pearson": float(stats.pearsonr(a, b)[0]),
            "spearman": float(stats.spearmanr(a, b)[0]),
            "icc21": icc21(a, b),
            "krippendorff_alpha": float(krippendorff_alpha_interval(np.vstack([a, b]))),
            "exact_agreement_pct": float(100 * np.mean(a == b)),
            "within_one_pct": float(100 * np.mean(np.abs(a - b) <= 1)),
            "mean_r1": float(a.mean()), "mean_r2": float(b.mean()),
            "sd_r1": float(a.std()), "sd_r2": float(b.std()),
        }

    # ---- S_text: mean of the four dimensions, normalised to [0,1] ----
    for r in ["r1", "r2"]:
        m[f"S_text_{r}"] = m[[f"{d}_{r}" for d in DIMS]].mean(axis=1).sub(1).div(4)
    m["S_text"] = m[["S_text_r1", "S_text_r2"]].mean(axis=1)

    scale_rel = {
        "pearson_r1_r2": float(stats.pearsonr(m["S_text_r1"], m["S_text_r2"])[0]),
        "spearman_r1_r2": float(stats.spearmanr(m["S_text_r1"], m["S_text_r2"])[0]),
        "icc21": icc21(m["S_text_r1"].to_numpy(float), m["S_text_r2"].to_numpy(float)),
        "krippendorff_alpha": float(krippendorff_alpha_interval(
            np.vstack([m["S_text_r1"].to_numpy(float), m["S_text_r2"].to_numpy(float)]))),
    }

    # ---- validity: S_text vs S_original ----
    val = {}
    for lab, col in [("S_text_mean_of_raters", "S_text"),
                     ("S_text_rater1", "S_text_r1"), ("S_text_rater2", "S_text_r2")]:
        val[lab] = {
            "pearson_vs_S_original": float(stats.pearsonr(m[col], m["structure_S"])[0]),
            "spearman_vs_S_original": float(stats.spearmanr(m[col], m["structure_S"])[0]),
            "pearson_vs_S_rank": float(stats.pearsonr(m[col], m["structure_S_rank"])[0]),
            "spearman_vs_S_rank": float(stats.spearmanr(m[col], m["structure_S_rank"])[0]),
        }

    # occupation-level (collapse duplicate occupations if any)
    occ = m.groupby("occp").agg(S_text=("S_text", "mean"),
                                S_original=("structure_S", "first"),
                                S_rank=("structure_S_rank", "first"),
                                P=("embodiment_P", "first"),
                                employment=("employment", "first")).reset_index()
    occ_val = {
        "n_occupations": int(len(occ)),
        "pearson": float(stats.pearsonr(occ["S_text"], occ["S_original"])[0]),
        "spearman": float(stats.spearmanr(occ["S_text"], occ["S_original"])[0]),
    }

    headline = val["S_text_mean_of_raters"]["pearson_vs_S_original"]
    verdict = ("S_original RETAINED" if abs(headline) >= 0.5 else
               "BELOW 0.5 THRESHOLD: S_original reliability in question, "
               "arbitrate with the A3 adoption test")

    res = {"n_items": int(len(m)), "reliability_by_dimension": rel,
           "reliability_of_S_text_scale": scale_rel,
           "validity_vs_S_original": val,
           "occupation_level": occ_val,
           "owner_threshold": 0.5, "verdict": verdict}
    (A4 / "a4_results.json").write_text(json.dumps(res, indent=2))
    occ.round(4).to_csv(A4 / "a4_occupation_S_text.csv", index=False)
    m.round(4).to_csv(A4 / "a4_merged_ratings.csv", index=False)

    pd.set_option("display.width", 200)
    print("\n=== Inter-rater reliability by dimension ===")
    R = pd.DataFrame(rel).T[["pearson", "icc21", "krippendorff_alpha",
                             "exact_agreement_pct", "within_one_pct", "mean_r1", "mean_r2"]]
    print(R.round(3).to_string())
    print("\n=== Reliability of the S_text scale (mean of 4 dims) ===")
    for k, v in scale_rel.items():
        print(f"  {k:24s} {v:+.3f}")
    print("\n=== Validity: S_text vs S_original (item level) ===")
    for k, v in val.items():
        print(f"  {k:24s} pearson {v['pearson_vs_S_original']:+.3f}, "
              f"spearman {v['spearman_vs_S_original']:+.3f}, "
              f"vs S_rank pearson {v['pearson_vs_S_rank']:+.3f}")
    print(f"\n=== Occupation level (n={occ_val['n_occupations']}) ===")
    print(f"  pearson {occ_val['pearson']:+.3f}, spearman {occ_val['spearman']:+.3f}")
    print(f"\n=== VERDICT: {verdict} ===")


if __name__ == "__main__":
    main()
