"""Step 1: PAEI validation against published occupational exposure indices.

Question: does PAEI measure something real, and something NEW?

Discriminant validity is the test that matters most here. PAEI claims to score exposure to
EMBODIED automation. The established indices score COGNITIVE automation. If PAEI turns out
to be highly correlated with them, it is a relabelling and the novelty claim fails.

Indices used:
  Felten, Raj and Seamans AIOE  (SOC 6-digit)      cognitive AI exposure
  Eloundou et al. GPT exposure  (O*NET-SOC 8-digit) LLM exposure, alpha/beta/zeta variants

Not available, and the gate depends on one of them:
  Webb (2020) robot / software / AI scores. Webb distributes occupation-level scores only
  via his own site and neither michaelwebb.co nor the Stanford page currently serves a
  retrievable data file. The Step 1 acceptance gate is stated in terms of Webb's ROBOT
  score, so the gate CANNOT be fully resolved here. See notes/paei_validation.md.
  Frey and Osborne probabilities: not retrieved in a verified machine-readable form.

Correlations are reported unweighted and employment-weighted. Employment weights come from
ACS PUMS 2023 person weights aggregated to SOC through the Census OCCP crosswalk, because
BLS OES is not reachable from this environment.
"""
import io, json, pathlib, zipfile
import numpy as np
import pandas as pd
from scipy import stats

ROOT = pathlib.Path(__file__).parents[1]
RAW, OUT = ROOT / "data" / "raw", ROOT / "data" / "processed"
IDX = RAW / "indices"


def employment_by_soc():
    """Weighted employment by 6-digit SOC, from PUMS via the OCCP crosswalk."""
    occ = pd.read_csv(OUT / "occp_to_paei.csv")[["occp", "soc"]]
    frames = []
    for fn in ["psam_pusa.csv", "psam_pusb.csv"]:
        z = zipfile.ZipFile(RAW / "pums" / "csv_pus.zip")
        with z.open(fn) as fh:
            for ch in pd.read_csv(io.TextIOWrapper(fh, encoding="utf-8", errors="replace"),
                                  usecols=["OCCP", "PWGTP", "WAGP", "ADJINC"],
                                  chunksize=500_000, low_memory=False):
                frames.append(ch)
    P = pd.concat(frames, ignore_index=True)
    P["OCCP"] = pd.to_numeric(P["OCCP"], errors="coerce")
    P["PWGTP"] = pd.to_numeric(P["PWGTP"], errors="coerce")
    P["wage"] = (pd.to_numeric(P["WAGP"], errors="coerce").fillna(0)
                 * pd.to_numeric(P["ADJINC"], errors="coerce") / 1e6)
    P = P.merge(occ, left_on="OCCP", right_on="occp", how="inner")
    g = P.groupby("soc").apply(
        lambda d: pd.Series({"employment": d["PWGTP"].sum(),
                             "wage_bill": (d["wage"] * d["PWGTP"]).sum()}),
        include_groups=False)
    return g.reset_index()


def corr_block(df, a, b, w=None):
    d = df[[a, b] + ([w] if w else [])].dropna()
    if len(d) < 10:
        return {"n": len(d)}
    out = {"n": int(len(d)),
           "pearson": float(stats.pearsonr(d[a], d[b])[0]),
           "spearman": float(stats.spearmanr(d[a], d[b])[0])}
    if w:
        ww = d[w].to_numpy(float)
        x, y = d[a].to_numpy(float), d[b].to_numpy(float)
        mx, my = np.average(x, weights=ww), np.average(y, weights=ww)
        cov = np.average((x - mx) * (y - my), weights=ww)
        out["pearson_empweighted"] = float(
            cov / np.sqrt(np.average((x - mx) ** 2, weights=ww)
                          * np.average((y - my) ** 2, weights=ww)))
        rx = pd.Series(x).rank().to_numpy()
        ry = pd.Series(y).rank().to_numpy()
        mrx, mry = np.average(rx, weights=ww), np.average(ry, weights=ww)
        covr = np.average((rx - mrx) * (ry - mry), weights=ww)
        out["spearman_empweighted"] = float(
            covr / np.sqrt(np.average((rx - mrx) ** 2, weights=ww)
                           * np.average((ry - mry) ** 2, weights=ww)))
    return out


def main():
    paei = pd.read_csv(OUT / "paei_onet.csv")
    paei["soc"] = paei["onet_soc"].astype(str).str[:7]

    # ---- Eloundou et al: joins on O*NET-SOC directly ----
    el = pd.read_csv(IDX / "gpt_occ_level.csv")
    el = el.rename(columns={"O*NET-SOC Code": "onet_soc"})
    el["onet_soc"] = el["onet_soc"].astype(str)
    gpt_cols = ["dv_rating_alpha", "dv_rating_beta", "dv_rating_gamma",
                "human_rating_alpha", "human_rating_beta", "human_rating_gamma"]
    m = paei.merge(el[["onet_soc"] + gpt_cols], on="onet_soc", how="left")
    el_match = float(m["dv_rating_alpha"].notna().mean() * 100)

    # ---- Felten AIOE: joins on 6-digit SOC ----
    ai = pd.read_excel(IDX / "AIOE_DataAppendix.xlsx", "Appendix A")
    ai.columns = [str(c).strip() for c in ai.columns]
    ai = ai.rename(columns={"SOC Code": "soc", "AIOE": "aioe"})
    ai["soc"] = ai["soc"].astype(str).str.strip()
    m = m.merge(ai[["soc", "aioe"]], on="soc", how="left")
    ai_match = float(m["aioe"].notna().mean() * 100)

    # ---- employment weights ----
    emp = employment_by_soc()
    m = m.merge(emp, on="soc", how="left")
    m["employment"] = m["employment"].fillna(0.0)
    emp_cov = float((m["employment"] > 0).mean() * 100)

    m.to_csv(OUT / "paei_validation.csv", index=False)

    targets = [("aioe", "Felten AIOE (cognitive AI)"),
               ("dv_rating_beta", "Eloundou GPT beta (LLM)"),
               ("dv_rating_alpha", "Eloundou GPT alpha (LLM, strict)"),
               ("dv_rating_gamma", "Eloundou GPT zeta (LLM, broad)"),
               ("human_rating_beta", "Eloundou human-rated beta")]

    res = {"match_rates_pct": {"eloundou_onet_soc": el_match, "felten_soc6": ai_match,
                               "employment_weight_coverage": emp_cov},
           "correlations": {}}
    rows = []
    for col, label in targets:
        for ours in ["PAEI", "embodiment_P", "structure_S"]:
            c = corr_block(m, ours, col, "employment")
            res["correlations"][f"{ours}__{col}"] = c
            if "pearson" in c:
                rows.append({"our_measure": ours, "index": label, "n": c["n"],
                             "pearson": c["pearson"], "spearman": c["spearman"],
                             "pearson_empwt": c.get("pearson_empweighted"),
                             "spearman_empwt": c.get("spearman_empweighted")})
    T = pd.DataFrame(rows)
    T.round(4).to_csv(OUT / "paei_validation_correlations.csv", index=False)
    (OUT / "paei_validation_summary.json").write_text(json.dumps(res, indent=2))

    pd.set_option("display.width", 200)
    print(f"\nmatch rates: Eloundou {el_match:.1f}%  Felten {ai_match:.1f}%  "
          f"employment coverage {emp_cov:.1f}%")
    print("\n=== PAEI vs published exposure indices ===")
    print(T.round(3).to_string(index=False, max_colwidth=34))

    print("\n=== Discriminant validity read ===")
    for col, label in targets[:2]:
        c = res["correlations"].get(f"PAEI__{col}", {})
        if "pearson" in c:
            print(f"  PAEI vs {label}: r = {c['pearson']:+.3f}, "
                  f"rho = {c['spearman']:+.3f}, "
                  f"r(emp-wt) = {c.get('pearson_empweighted', float('nan')):+.3f}")


if __name__ == "__main__":
    main()
