"""A4 step 3: arbitrate S_original against S_text using the A3 adoption test.

A4 found the two raters agree almost perfectly with each other (scale alpha 0.967) but
agree with S_original only at r = 0.306. The disagreement is therefore a construct
difference, not rater noise, and the owner's rule is to let the A3 external test decide
which version is measuring the thing that predicts observed robot adoption.

Test, restricted to the 200 sampled occupations so both versions are scored on identical
data: among high-P occupations, does robot adoption rise more strongly in S_original or in
S_text?

Range-restriction caveat, stated because it matters for reading the result: the A4 sample
was stratified on S_original's rank, which guarantees S_original full spread across the
sample. S_text has whatever spread it has. That design favours S_original, so if S_text
nonetheless wins, the result is conservative in S_text's favour.
"""
import io, json, pathlib, zipfile
import numpy as np
import pandas as pd
from scipy import stats

ROOT = pathlib.Path(__file__).parents[1]
RAW, OUT = ROOT / "data" / "raw", ROOT / "data" / "processed"
A4 = OUT / "a4"


def main():
    occ = pd.read_csv(A4 / "a4_occupation_S_text.csv")
    anchor_src = json.loads((OUT / "anchor_c_summary.json").read_text())

    # rebuild occupation robot exposure exactly as anchor_c.py does
    import importlib.util
    spec = importlib.util.spec_from_file_location("anchor_c", ROOT / "src" / "anchor_c.py")
    ac = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ac)

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
    oi2 = oi[oi["intensity"].notna()]
    rob = (oi2.groupby("occp")
           .apply(lambda d: pd.Series({"robot_exposure": float(
               np.average(d["intensity"], weights=d["emp"]))}), include_groups=False)
           .reset_index())

    M = occ.merge(rob, on="occp", how="inner")
    M = M[M["employment"].notna() & (M["employment"] > 0)]

    # percentile ranks within this sample, employment weighted, for both versions
    def rank(col):
        w = M["employment"].to_numpy(float)
        o = np.argsort(M[col].to_numpy(float))
        cwt = np.cumsum(w[o]) / w.sum()
        r = np.empty(len(M)); r[o] = cwt
        return r

    M = M.copy()
    M["S_orig_rank"] = rank("S_original")
    M["S_text_rank"] = rank("S_text")

    P_MED = float(M["P"].median())
    hi = M[M["P"] >= P_MED]

    def t(d, col, label):
        sp = stats.spearmanr(d[col], d["robot_exposure"])
        pe = stats.pearsonr(d[col], d["robot_exposure"])
        w = d["employment"].to_numpy(float)
        x, y = d[col].to_numpy(float), d["robot_exposure"].to_numpy(float)
        mx, my = np.average(x, weights=w), np.average(y, weights=w)
        cov = np.average((x - mx) * (y - my), weights=w)
        pw = cov / np.sqrt(np.average((x - mx) ** 2, weights=w)
                           * np.average((y - my) ** 2, weights=w))
        return {"label": label, "n": int(len(d)), "spearman": float(sp[0]),
                "spearman_p": float(sp[1]), "pearson": float(pe[0]),
                "pearson_empwt": float(pw)}

    res = {
        "n_sample": int(len(M)), "n_high_P": int(len(hi)), "P_median": P_MED,
        "spread": {"S_original_sd": float(M["S_original"].std()),
                   "S_text_sd": float(M["S_text"].std()),
                   "S_original_range": [float(M["S_original"].min()), float(M["S_original"].max())],
                   "S_text_range": [float(M["S_text"].min()), float(M["S_text"].max())]},
        "high_P": {"S_original": t(hi, "S_orig_rank", "S_original (rank)"),
                   "S_text": t(hi, "S_text_rank", "S_text (rank)")},
        "all": {"S_original": t(M, "S_orig_rank", "S_original (rank)"),
                "S_text": t(M, "S_text_rank", "S_text (rank)")},
        "corr_between_versions": float(stats.pearsonr(M["S_original"], M["S_text"])[0]),
    }

    a = res["high_P"]["S_original"]["spearman"]
    b = res["high_P"]["S_text"]["spearman"]
    if max(a, b) <= 0:
        verdict = "NEITHER version predicts adoption in this subsample; inconclusive"
    elif abs(a - b) < 0.05:
        verdict = ("TIE within 0.05 Spearman: retain S_original (incumbent) and report "
                   "S_text as a robustness check")
    elif a > b:
        verdict = "S_original WINS the adoption test: retain S_original"
    else:
        verdict = "S_text WINS the adoption test: switch to S_text"
    res["verdict"] = verdict
    (A4 / "a4_arbitration.json").write_text(json.dumps(res, indent=2))

    print(f"sample {len(M)} occupations, high-P {len(hi)} (P >= {P_MED:.3f})")
    print(f"corr(S_original, S_text) = {res['corr_between_versions']:+.3f}")
    print(f"spread: S_original sd {res['spread']['S_original_sd']:.4f}, "
          f"S_text sd {res['spread']['S_text_sd']:.4f}")
    print("\n=== A3 adoption test, HIGH-P occupations (the arbitration) ===")
    for k in ["S_original", "S_text"]:
        v = res["high_P"][k]
        print(f"  {v['label']:22s} spearman {v['spearman']:+.3f} (p={v['spearman_p']:.2e}), "
              f"pearson {v['pearson']:+.3f}, emp-wt {v['pearson_empwt']:+.3f}")
    print("\n=== all occupations in sample ===")
    for k in ["S_original", "S_text"]:
        v = res["all"][k]
        print(f"  {v['label']:22s} spearman {v['spearman']:+.3f} (p={v['spearman_p']:.2e})")
    print(f"\n=== VERDICT: {verdict} ===")


if __name__ == "__main__":
    main()
