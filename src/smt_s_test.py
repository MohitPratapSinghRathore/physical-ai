"""Item 1: the last S test. Survey of Manufacturing Technology, detailed manufacturing.

Why this is the decisive version. A23 showed the ACES-based test carries no within-industry
information: the adoption measure had an R-squared of 0.996 on the industry mix, and
manufacturing is a single sector there. SMT gives robot use at 4-digit SIC across 161
industries inside SIC 34 to 38, so it has genuine variation WITHIN manufacturing. If S
cannot predict robot use across detailed manufacturing industries, the S question closes.

Technology variables. The SMT collected 17 technologies in 5 documented categories (design
and engineering; fabrication, machining and assembly; automated materials handling;
automated sensor-based inspection or testing; communications and control). The 37 columns
here are `sic`, `freq`, `totemp`, and 17 technology stems each with an `01` and an `02`
suffix. The 17 stems partition exactly into the 5 documented categories with the documented
counts:

    design/engineering (3)   cad1, cad2, cad3
    fabrication (5)          fmc, cnc, mwl (materials working lasers), ppr, otr
    materials handling (2)   agv, asr
    sensors (2)              as1, as2
    comms/control (5)        cc1..cc5

ROBOT VARIABLES USED: `ppr` (pick and place robots) and `otr` (other robots). `agv`
(automated guided vehicles) is reported separately as materials handling, not as a robot.

Verification status, stated honestly: the 5-category / 17-technology structure and the
category memberships above are confirmed against Census descriptions of the SMT. A
variable-level data dictionary mapping these exact column stems to technology names was NOT
located, so the stem-to-technology mapping is inferred from the transparent naming plus the
exact partition into the documented categories. It is high confidence but not documented,
and is recorded as such.

Suffixes: `01` is the establishment count using the technology, `02` is employment in
establishments using it. Robot use is measured as employment share,
(ppr02 + otr02) / totemp, with the establishment share as a robustness check.

Crosswalk: SIC87 (4-digit) -> 1997 NAICS (Census concordance) -> PUMS INDP via the Census
2017 industry code list. Only 25 PUMS industries exist in the SIC 34-38 range, which is the
binding constraint on this test and is exactly at the owner's stated threshold.
"""
import io, json, pathlib, re, zipfile
import numpy as np
import pandas as pd
from scipy import stats

ROOT = pathlib.Path(__file__).parents[1]
RAW, OUT = ROOT / "data" / "raw", ROOT / "data" / "processed"
PKG = RAW / "manual" / "114030"
CW = RAW / "crosswalk"


def sic_to_naics():
    d = pd.read_excel(CW / "sic87_naics97.xls", header=None, skiprows=1)
    d = d[[0, 3]].copy()
    d.columns = ["sic", "naics"]
    d = d.dropna()
    # openpyxl/xlrd read numeric-looking codes as floats, so 11114 arrives as "11114.0"
    clean = lambda s: s.astype(str).str.strip().str.replace(r"\.0$", "", regex=True)
    d["sic"] = clean(d["sic"])
    d = d[d["sic"].str.fullmatch(r"\d{4}")]
    d["naics"] = clean(d["naics"])
    d = d[d["naics"].str.fullmatch(r"\d{4,6}")]
    d["sic"] = d["sic"].astype(int)
    return d.drop_duplicates()


def indp_naics():
    d = pd.read_excel(CW / "census2017_ind_naics.xlsx",
                      "2017 Census Industry Code List", header=None)
    rows = []
    for _, r in d.iterrows():
        code, naics = r[3], r[4]
        if pd.isna(code) or pd.isna(naics):
            continue
        code = str(code).strip()
        if not re.fullmatch(r"\d{3,4}", code):
            continue
        for part in str(naics).split(","):
            part = part.strip()
            part = re.sub(r"\.0$", "", part)
            m = re.match(r"^(\d{3,6})", part)
            if m:
                rows.append({"indp": int(code), "naics_pref": m.group(1),
                             "title": str(r[1]).strip()})
    return pd.DataFrame(rows).drop_duplicates()


def main():
    res = {}
    smt = {y: pd.read_stata(PKG / f"smt{y}.dta") for y in (88, 93)}
    for y, d in smt.items():
        d["robot_emp_share"] = (d["ppr02"] + d["otr02"]) / d["totemp"]
        d["robot_est_share"] = (d["ppr01"] + d["otr01"]) / d["freq"]
        d["agv_emp_share"] = d["agv02"] / d["totemp"]
        print(f"smt{y}: {len(d)} SIC industries, robot employment share "
              f"mean {d['robot_emp_share'].mean():.3f}, "
              f"median {d['robot_emp_share'].median():.3f}")

    s2n = sic_to_naics()
    i2n = indp_naics()
    print(f"SIC87->NAICS97 rows: {len(s2n)}; INDP naics prefixes: {len(i2n)}")

    # SIC -> INDP by longest NAICS prefix match
    def map_sic_to_indp(sic_df):
        out = []
        for _, r in sic_df.iterrows():
            cand = s2n[s2n["sic"] == r["sic"]]
            hits = set()
            for n in cand["naics"]:
                for L in (6, 5, 4, 3):
                    m = i2n[i2n["naics_pref"] == n[:L]]
                    if len(m):
                        hits.update(m["indp"].tolist())
                        break
            for h in hits:
                out.append({"sic": r["sic"], "indp": h,
                            "robot_emp_share": r["robot_emp_share"],
                            "robot_est_share": r["robot_est_share"],
                            "agv_emp_share": r["agv_emp_share"],
                            "totemp": r["totemp"]})
        if not out:
            return pd.DataFrame(columns=["sic", "indp", "robot_emp_share",
                                         "robot_est_share", "agv_emp_share", "totemp"])
        return pd.DataFrame(out)

    panels = {}
    for y, d in smt.items():
        m = map_sic_to_indp(d)
        # employment-weighted average across SICs mapping to the same INDP
        g = (m.groupby("indp")
               .apply(lambda x: pd.Series({
                   "robot_emp_share": float(np.average(x["robot_emp_share"],
                                                       weights=x["totemp"])),
                   "robot_est_share": float(np.average(x["robot_est_share"],
                                                       weights=x["totemp"])),
                   "agv_emp_share": float(np.average(x["agv_emp_share"],
                                                     weights=x["totemp"])),
                   "smt_emp": float(x["totemp"].sum()),
                   "n_sic": int(x["sic"].nunique())}), include_groups=False)
               .reset_index())
        panels[y] = g
        print(f"smt{y}: mapped to {len(g)} distinct PUMS INDP industries")

    P = panels[93].merge(panels[88], on="indp", suffixes=("_93", "_88"), how="outer")
    P["robot_emp_share"] = P[["robot_emp_share_93", "robot_emp_share_88"]].mean(axis=1)
    P["robot_est_share"] = P[["robot_est_share_93", "robot_est_share_88"]].mean(axis=1)
    n_ind = int(P["robot_emp_share"].notna().sum())
    res["n_distinct_industries"] = n_ind
    print(f"\nDISTINCT USABLE INDUSTRIES: {n_ind} (owner threshold: about 25)")

    # occupation x industry employment, restricted to these industries
    import importlib.util
    spec = importlib.util.spec_from_file_location("anchor_c", ROOT / "src" / "anchor_c.py")
    ac = importlib.util.module_from_spec(spec); spec.loader.exec_module(ac)
    oi = ac.pums_occ_ind()
    oi = oi.merge(P[["indp", "robot_emp_share", "robot_est_share"]], on="indp", how="inner")
    print(f"occupation x industry cells inside SMT industries: {len(oi):,}")

    occ = (oi.groupby("occp")
             .apply(lambda d: pd.Series({
                 "smt_robot": float(np.average(d["robot_emp_share"], weights=d["emp"])),
                 "smt_robot_est": float(np.average(d["robot_est_share"], weights=d["emp"])),
                 "emp_in_smt": float(d["emp"].sum()),
                 "n_ind": int(d["indp"].nunique())}), include_groups=False)
             .reset_index())

    grid = pd.read_csv(OUT / "paei_c.csv")
    base = grid[grid["c"] == 0.0][["occp", "title", "embodiment_P", "structure_S",
                                   "structure_S_rank", "employment"]]
    M = base.merge(occ, on="occp", how="inner")
    # require meaningful presence in SMT industries
    M = M[(M["emp_in_smt"] >= 1000) & (M["employment"] > 0)].copy()
    P_MED = float(M["embodiment_P"].median())
    hi = M[M["embodiment_P"] >= P_MED]
    print(f"occupations with SMT exposure: {len(M)}; high-P: {len(hi)}")
    M.round(5).to_csv(OUT / "smt_s_panel.csv", index=False)

    def t(d, lab, col="smt_robot"):
        if len(d) < 12:
            return {"n": int(len(d)), "note": "too few"}
        sp = stats.spearmanr(d["structure_S_rank"], d[col])
        pe = stats.pearsonr(d["structure_S"], d[col])
        w = d["employment"].to_numpy(float)
        x = stats.rankdata(d["structure_S_rank"]); y = stats.rankdata(d[col])
        mx, my = np.average(x, weights=w), np.average(y, weights=w)
        cov = np.average((x - mx) * (y - my), weights=w)
        sw = cov / np.sqrt(np.average((x - mx) ** 2, weights=w)
                           * np.average((y - my) ** 2, weights=w))
        r = {"n": int(len(d)), "spearman": float(sp[0]), "p": float(sp[1]),
             "pearson": float(pe[0]), "spearman_empwt": float(sw)}
        print(f"  {lab:34s} n={r['n']:4d}  Spearman {r['spearman']:+.3f} "
              f"(p={r['p']:.3f})  emp-wt {r['spearman_empwt']:+.3f}")
        return r

    print("\n=== S vs SMT robot use (employment share), across detailed mfg industries ===")
    res["all"] = t(M, "all occupations")
    res["high_P"] = t(hi, "HIGH-P occupations (the test)")
    print("\n  robustness: establishment-share measure")
    res["high_P_est"] = t(hi, "HIGH-P, establishment share", col="smt_robot_est")

    gate_r = res["high_P"].get("spearman", 0.0)
    gate_p = res["high_P"].get("p", 1.0)
    ok = (n_ind >= 25) and (gate_p < 0.05) and (gate_r > 0)
    res["verdict"] = ("S SURVIVES the detailed-manufacturing test" if ok else
                      "S FAILS: close the S question permanently")
    res["n_industries_threshold_met"] = bool(n_ind >= 25)
    (OUT / "smt_s_test.json").write_text(json.dumps(res, indent=2))
    print(f"\n=== VERDICT: {res['verdict']} ===")


if __name__ == "__main__":
    main()
