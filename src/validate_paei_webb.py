"""Step 1 GATE: PAEI against Webb (2020) robot, software and AI exposure.

This is the test the Step 1 gate is defined on. Webb's ROBOT score is the only published
index built against the same technology PAEI targets, so it is the test of whether PAEI at
c = 0 is that score under a new name.

    Gate criterion (MASTER_PROMPT_PHASE2.md Step 1): if PAEI correlates above roughly 0.8
    with Webb's robot score, PAEI at c = 0 is not novel.

Crosswalk chain, each hop reported with its match rate:

    Webb occ1990dd
      -> occ2010 (Autor and Dorn occ2010_occ1990dd.dta)
      -> 2018 Census occupation code (Census 2010-to-2018 crosswalk)
      -> PUMS OCCP, which is the spine PAEI is built on

Webb's scores are percentiles (0 to 100) of exposure within his occupation set, so Spearman
is the primary statistic and Pearson is reported alongside. Employment weights are ACS PUMS
2023 person weights; Webb's own labor supply weights (lswt2010) are reported as a
robustness check because they are the weights his percentiles were constructed under.

Nothing in this module is tuned. The prediction registered in notes/paei_validation.md
before the data arrived was: P correlates above 0.8 with Webb robot, PAEI as a whole lower.
"""
import io, json, pathlib, zipfile
import numpy as np
import pandas as pd
from scipy import stats

ROOT = pathlib.Path(__file__).parents[1]
RAW, OUT = ROOT / "data" / "raw", ROOT / "data" / "processed"
CW = RAW / "crosswalk"


def load_webb():
    d = pd.read_csv(RAW / "manual" / "exposure_by_occ1990dd_lswt2010.xls")
    d.columns = [c.strip() for c in d.columns]
    for c in ["pct_software", "pct_robot", "pct_ai"]:
        d[c] = pd.to_numeric(d[c], errors="coerce")
    d["occ1990dd"] = pd.to_numeric(d["occ1990dd"], errors="coerce")
    d = d.dropna(subset=["occ1990dd"])
    d["occ1990dd"] = d["occ1990dd"].astype(int)
    return d


def load_occ2010_to_1990dd():
    d = pd.read_stata(CW / "occ2010_occ1990dd" / "occ2010_occ1990dd.dta")
    d.columns = [c.lower() for c in d.columns]
    # the file ships the 2010 Census occupation code in a column named "occ"
    d = d.rename(columns={"occ": "occ2010"})[["occ2010", "occ1990dd"]].dropna()
    d["occ2010"] = pd.to_numeric(d["occ2010"].astype(str).str.strip(), errors="coerce")
    d["occ1990dd"] = pd.to_numeric(d["occ1990dd"], errors="coerce")
    d = d.dropna()
    d["occ2010"] = d["occ2010"].astype(int)
    d["occ1990dd"] = d["occ1990dd"].astype(int)
    return d[d["occ1990dd"] != 999].drop_duplicates()


def load_2010_to_2018():
    d = pd.read_excel(CW / "census2018_occ_soc.xlsx", "2010 to 2018 Crosswalk ",
                      header=None)
    hdr = d.index[d[1].astype(str).str.strip().str.startswith("2010 Census Code")]
    body = d.loc[hdr[0] + 1:, [1, 4]].copy()
    body.columns = ["occ2010", "occp2018"]
    body = body.dropna()
    body["occ2010"] = pd.to_numeric(body["occ2010"].astype(str).str.strip(),
                                    errors="coerce")
    body["occp2018"] = pd.to_numeric(body["occp2018"].astype(str).str.strip(),
                                     errors="coerce")
    return body.dropna().astype(int).drop_duplicates()


def wcorr(x, y, w):
    x, y, w = map(lambda a: np.asarray(a, float), (x, y, w))
    m = np.isfinite(x) & np.isfinite(y) & np.isfinite(w) & (w > 0)
    x, y, w = x[m], y[m], w[m]
    mx, my = np.average(x, weights=w), np.average(y, weights=w)
    cov = np.average((x - mx) * (y - my), weights=w)
    return float(cov / np.sqrt(np.average((x - mx) ** 2, weights=w)
                               * np.average((y - my) ** 2, weights=w)))


def wspearman(x, y, w):
    rx = pd.Series(x).rank().to_numpy()
    ry = pd.Series(y).rank().to_numpy()
    return wcorr(rx, ry, w)


def main():
    webb = load_webb()
    c1 = load_occ2010_to_1990dd()
    c2 = load_2010_to_2018()
    print(f"Webb occupations: {len(webb)}")
    print(f"occ2010 -> occ1990dd rows: {len(c1)}; occ2010 -> occp2018 rows: {len(c2)}")

    # chain: occ1990dd -> occ2010 -> occp2018
    ch = c1.merge(c2, on="occ2010", how="inner")
    w = webb.merge(ch, on="occ1990dd", how="left")
    hop1 = 100 * w["occ2010"].notna().mean()
    print(f"Webb rows reaching occ2010: {hop1:.1f}%")

    # collapse to OCCP: several occ1990dd can map to one OCCP; average Webb scores
    wo = (w.dropna(subset=["occp2018"])
            .groupby("occp2018")
            .agg(pct_robot=("pct_robot", "mean"),
                 pct_software=("pct_software", "mean"),
                 pct_ai=("pct_ai", "mean"),
                 lswt2010=("lswt2010", "sum"),
                 n_src=("occ1990dd", "nunique")).reset_index()
            .rename(columns={"occp2018": "occp"}))
    print(f"distinct OCCP codes carrying a Webb score: {len(wo)}")

    grid = pd.read_csv(OUT / "paei_c.csv")
    base = grid[grid["c"] == 0.0][["occp", "title", "embodiment_P", "structure_S",
                                   "structure_S_rank", "employment", "wage_bill"]].copy()
    ver = json.loads((OUT / "paei_c_summary.json").read_text())["paei_c_version"]
    base["PAEI"] = base["embodiment_P"] * base["structure_S"]

    M = base.merge(wo, on="occp", how="inner")
    M = M[M["employment"].notna() & (M["employment"] > 0)]
    cov_emp = 100 * M["employment"].sum() / base["employment"].sum()
    print(f"matched occupations: {len(M)} of {len(base)}; "
          f"employment covered: {cov_emp:.1f}%")
    M.round(4).to_csv(OUT / "paei_webb_matched.csv", index=False)

    targets = [("pct_robot", "Webb ROBOT (the gate)"),
               ("pct_software", "Webb software"),
               ("pct_ai", "Webb AI")]
    ours = [("PAEI", "PAEI (P x S)"), ("embodiment_P", "embodiment P"),
            ("structure_S", "structure S"), ("structure_S_rank", "structure S_rank")]

    rows, res = [], {}
    for tc, tl in targets:
        for oc, ol in ours:
            d = M[[oc, tc, "employment", "lswt2010"]].dropna()
            r = {"our_measure": ol, "webb_index": tl, "n": int(len(d)),
                 "pearson": float(stats.pearsonr(d[oc], d[tc])[0]),
                 "spearman": float(stats.spearmanr(d[oc], d[tc])[0]),
                 "pearson_empwt": wcorr(d[oc], d[tc], d["employment"]),
                 "spearman_empwt": wspearman(d[oc], d[tc], d["employment"]),
                 "spearman_webbwt": wspearman(d[oc], d[tc], d["lswt2010"])}
            rows.append(r)
            res[f"{oc}__{tc}"] = r
    T = pd.DataFrame(rows)
    T.round(4).to_csv(OUT / "paei_webb_correlations.csv", index=False)

    g_paei = res["PAEI__pct_robot"]
    g_P = res["embodiment_P__pct_robot"]
    g_S = res["structure_S__pct_robot"]
    worst = max(abs(g_paei["spearman"]), abs(g_paei["pearson"]),
                abs(g_paei["spearman_empwt"]))
    gate = ("NOT NOVEL at c=0: PAEI duplicates Webb robot" if worst >= 0.8 else
            "NOVEL at c=0: PAEI is distinct from Webb robot")

    summary = {
        "paei_c_version": ver,
        "gate_criterion": "PAEI vs Webb robot correlation >= ~0.8 means not novel",
        "n_matched_occupations": int(len(M)),
        "employment_coverage_pct": cov_emp,
        "webb_rows_reaching_occ2010_pct": hop1,
        "PAEI_vs_webb_robot": g_paei,
        "P_vs_webb_robot": g_P,
        "S_vs_webb_robot": g_S,
        "max_abs_PAEI_vs_robot": worst,
        "GATE_VERDICT": gate,
        "registered_prediction": ("P correlates above 0.8 with Webb robot; PAEI as a "
                                  "whole lower. Recorded in notes/paei_validation.md "
                                  "before the data was available."),
    }
    (OUT / "paei_webb_summary.json").write_text(json.dumps(summary, indent=2))

    pd.set_option("display.width", 210)
    print("\n=== PAEI and its factors vs Webb (2020) ===")
    print(T[["our_measure", "webb_index", "n", "pearson", "spearman",
             "pearson_empwt", "spearman_empwt"]].round(3).to_string(index=False))
    print(f"\n=== GATE ===")
    print(f"  PAEI vs Webb ROBOT: pearson {g_paei['pearson']:+.3f}, "
          f"spearman {g_paei['spearman']:+.3f}, emp-wt spearman {g_paei['spearman_empwt']:+.3f}")
    print(f"  P    vs Webb ROBOT: pearson {g_P['pearson']:+.3f}, "
          f"spearman {g_P['spearman']:+.3f}")
    print(f"  S    vs Webb ROBOT: pearson {g_S['pearson']:+.3f}, "
          f"spearman {g_S['spearman']:+.3f}")
    print(f"\n  max |correlation| PAEI vs robot = {worst:.3f}")
    print(f"  VERDICT: {gate}")


if __name__ == "__main__":
    main()
