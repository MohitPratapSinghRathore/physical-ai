"""H3: is cognitive exposure geographically concentrated, and is embodied near-uniformity
just employment density?

Registered in notes/prereg_cognitive_contrast.md Amendment 1 BEFORE running.

Groups, all defined externally and employment-weighted to a top quintile:
    cognitive_AIOE      Felten, Raj and Seamans AIOE
    cognitive_GPT       Eloundou et al. GPT exposure (dv_rating_beta)
    embodied            embodiment P
    robot_reachable     Webb (2020) pct_robot

CAVEAT carried on every cognitive result: AIOE and Eloundou measure TASK OVERLAP, not
displacement and not timing, and top-quintile occupations include likely-augmented work.

CONTROL FOR DENSITY. The headline statistic is the at-risk RATE (group wage bill over total
local wage bill), which is a share and therefore already normalises out area size. Two extra
controls are reported anyway:
  (a) the Gini of total employment LEVELS across areas, as the density benchmark;
  (b) a PLACEBO group: occupations drawn at random to match 20 percent of employment,
      seeded, giving the concentration a mechanically-unconcentrated group would show.
If a real group's rate-Gini is not materially above the placebo's, its "concentration" is
sampling noise rather than geography.

Correlations reported for each group's local rate against local median home value (PUMS
VALP) and local median wage.
"""
import io, json, pathlib, zipfile
import numpy as np
import pandas as pd
from scipy import stats

ROOT = pathlib.Path(__file__).parents[1]
RAW, OUT = ROOT / "data" / "raw", ROOT / "data" / "processed"
PPART = [("csv_pus.zip", "psam_pusa.csv"), ("csv_pus.zip", "psam_pusb.csv")]
HPART = [("csv_hus.zip", "psam_husa.csv"), ("csv_hus.zip", "psam_husb.csv")]
SEED = 20260919


def chunks(zf, fn, cols, size=300_000):
    z = zipfile.ZipFile(RAW / "pums" / zf)
    with z.open(fn) as fh:
        for ch in pd.read_csv(io.TextIOWrapper(fh, encoding="utf-8", errors="replace"),
                              usecols=cols, dtype={"SERIALNO": str},
                              chunksize=size, low_memory=False):
            yield ch


def gini(x):
    x = np.asarray(x, float)
    x = x[np.isfinite(x) & (x >= 0)]
    if len(x) < 2 or x.sum() == 0:
        return np.nan
    xs = np.sort(x); n = len(xs)
    return float((n + 1 - 2 * np.sum(np.cumsum(xs)) / np.cumsum(xs)[-1]) / n)


def spread(x, lo, hi):
    x = np.asarray(x, float); x = x[np.isfinite(x) & (x > 0)]
    if len(x) < 50:
        return np.nan
    a, b = np.percentile(x, lo), np.percentile(x, hi)
    return float(b / a) if a > 0 else np.nan


def build_groups():
    grid = pd.read_csv(OUT / "paei_c.csv")
    base = grid[grid["c"] == 0.0][["occp", "title", "embodiment_P", "employment"]]
    base = base[base["employment"].notna() & (base["employment"] > 0)].copy()
    val = pd.read_csv(OUT / "paei_validation.csv")
    val["soc"] = val["onet_soc"].astype(str).str[:7]
    cw = pd.read_csv(OUT / "occp_to_paei.csv")[["occp", "soc"]]
    agg = val.groupby("soc").agg(aioe=("aioe", "mean"),
                                 gpt=("dv_rating_beta", "mean")).reset_index()
    B = base.merge(cw.merge(agg, on="soc", how="left")[["occp", "aioe", "gpt"]],
                   on="occp", how="left")
    webb = pd.read_csv(OUT / "paei_webb_matched.csv")[["occp", "pct_robot"]]
    B = B.merge(webb, on="occp", how="left")

    def topq(col):
        d = B.dropna(subset=[col]).sort_values(col)
        c = np.cumsum(d["employment"].to_numpy()) / d["employment"].sum()
        cut = np.interp(0.80, c, d[col].to_numpy())
        return set(B.loc[B[col] >= cut, "occp"])

    g = {"cognitive_AIOE": topq("aioe"), "cognitive_GPT": topq("gpt"),
         "embodied": topq("embodiment_P"), "robot_reachable": topq("pct_robot")}
    # placebo: random occupations totalling ~20 percent of employment
    rng = np.random.default_rng(SEED)
    d = B.sample(frac=1.0, random_state=SEED)
    cum = np.cumsum(d["employment"].to_numpy()) / B["employment"].sum()
    g["placebo_random20"] = set(d.loc[cum <= 0.20, "occp"])
    return B, g


def main():
    B, groups = build_groups()
    for k, s in groups.items():
        sub = B[B["occp"].isin(s)]
        print(f"{k:18s} {len(s):4d} occs, {sub['employment'].sum():>12,.0f} workers "
              f"({100*sub['employment'].sum()/B['employment'].sum():.1f}% of employment)")

    # ---- person pass: wage bill by PUMA, total and by group ----
    print("\nperson pass ...")
    tot, acc = {}, {k: {} for k in groups}
    wagesum, wagecnt = {}, {}
    for zf, fn in PPART:
        for ch in chunks(zf, fn, ["STATE", "PUMA", "OCCP", "WAGP", "ADJINC", "PWGTP"]):
            occ = pd.to_numeric(ch["OCCP"], errors="coerce")
            wage = (pd.to_numeric(ch["WAGP"], errors="coerce").fillna(0.0)
                    * pd.to_numeric(ch["ADJINC"], errors="coerce") / 1e6)
            pw = pd.to_numeric(ch["PWGTP"], errors="coerce").fillna(0.0)
            key = (ch["STATE"].astype(int).astype(str).str.zfill(2)
                   + ch["PUMA"].astype(int).astype(str).str.zfill(5))
            for k, v in (wage * pw).groupby(key).sum().items():
                tot[k] = tot.get(k, 0.0) + v
            m = wage > 0
            for k, v in (wage * pw)[m].groupby(key[m]).sum().items():
                wagesum[k] = wagesum.get(k, 0.0) + v
            for k, v in pw[m].groupby(key[m]).sum().items():
                wagecnt[k] = wagecnt.get(k, 0.0) + v
            for g, s in groups.items():
                sel = occ.isin(s)
                if sel.any():
                    for k, v in (wage * pw * sel).groupby(key).sum().items():
                        acc[g][k] = acc[g].get(k, 0.0) + v

    # ---- housing pass: median home value by PUMA ----
    print("housing pass ...")
    hv = {}
    for zf, fn in HPART:
        for ch in chunks(zf, fn, ["STATE", "PUMA", "WGTP", "VALP", "TEN"]):
            v = pd.to_numeric(ch["VALP"], errors="coerce")
            wg = pd.to_numeric(ch["WGTP"], errors="coerce").fillna(0.0)
            ok = v.notna() & (v > 0) & pd.to_numeric(ch["TEN"], errors="coerce").isin([1, 2])
            key = (ch["STATE"].astype(int).astype(str).str.zfill(2)
                   + ch["PUMA"].astype(int).astype(str).str.zfill(5))
            for k, sub in pd.DataFrame({"k": key[ok], "v": v[ok], "w": wg[ok]}).groupby("k"):
                hv.setdefault(k, []).append(sub)
    home = {}
    for k, parts in hv.items():
        d = pd.concat(parts)
        o = np.argsort(d["v"].to_numpy())
        vv, ww = d["v"].to_numpy()[o], d["w"].to_numpy()[o]
        if ww.sum() > 0:
            home[k] = float(np.interp(0.5, np.cumsum(ww) / ww.sum(), vv))

    # ---- assemble PUMA frame ----
    D = pd.DataFrame({"puma_id": sorted(tot)})
    D["wage_total"] = D["puma_id"].map(tot)
    D["median_home_value"] = D["puma_id"].map(home)
    D["mean_wage"] = D["puma_id"].map(
        {k: wagesum[k] / wagecnt[k] for k in wagesum if wagecnt.get(k, 0) > 0})
    for g in groups:
        D[f"rate_{g}"] = D["puma_id"].map(acc[g]).fillna(0.0) / D["wage_total"].replace(0, np.nan)
    D.to_csv(OUT / "h3_puma.csv", index=False)

    # ---- county ----
    cnt = pd.read_csv(OUT / "puma_to_county_afact.csv",
                      dtype={"puma_id": str, "county_fips": str})
    M = D.merge(cnt[["puma_id", "county_fips", "afact"]], on="puma_id", how="inner")
    M["wt"] = M["wage_total"] * M["afact"]
    for g in groups:
        M[f"num_{g}"] = M[f"rate_{g}"] * M["wt"]
    Cty = M.groupby("county_fips").agg(
        wage_total=("wt", "sum"),
        median_home_value=("median_home_value", "mean"),
        mean_wage=("mean_wage", "mean"),
        **{f"num_{g}": (f"num_{g}", "sum") for g in groups}).reset_index()
    for g in groups:
        Cty[f"rate_{g}"] = Cty[f"num_{g}"] / Cty["wage_total"].replace(0, np.nan)
    Cty.to_csv(OUT / "h3_county.csv", index=False)

    # ---- statistics ----
    rows = []
    for lvl, df in [("PUMA", D), ("county", Cty)]:
        for g in groups:
            r = df[f"rate_{g}"].replace([np.inf, -np.inf], np.nan).dropna()
            sub = df[[f"rate_{g}", "median_home_value", "mean_wage"]].dropna()
            rows.append({
                "level": lvl, "group": g, "n_areas": int(len(r)),
                "national_rate": float(df[f"num_{g}"].sum() / df["wage_total"].sum())
                if lvl == "county" else float(
                    sum(acc[g].values()) / sum(tot.values())),
                "gini_of_rate": gini(r), "p90_p10": spread(r, 10, 90),
                "p99_p1": spread(r, 1, 99),
                "corr_home_value": float(stats.spearmanr(sub[f"rate_{g}"],
                                                         sub["median_home_value"])[0]),
                "corr_mean_wage": float(stats.spearmanr(sub[f"rate_{g}"],
                                                        sub["mean_wage"])[0])})
    T = pd.DataFrame(rows)
    # density benchmark
    dens = {"PUMA": gini(D["wage_total"]), "county": gini(Cty["wage_total"])}
    T["gini_of_wage_LEVELS_benchmark"] = T["level"].map(dens)
    T.round(4).to_csv(OUT / "h3_concentration.csv", index=False)
    (OUT / "h3_summary.json").write_text(json.dumps(
        {"density_benchmark_gini_of_levels": dens,
         "stats": T.round(4).to_dict("records")}, indent=2))

    pd.set_option("display.width", 240)
    print("\n=== H3: concentration of the AT-RISK RATE, and correlations ===")
    print(T[["level", "group", "n_areas", "national_rate", "gini_of_rate", "p90_p10",
             "p99_p1", "corr_home_value", "corr_mean_wage"]].round(3).to_string(index=False))
    print(f"\n  DENSITY BENCHMARK, Gini of total wage LEVELS: "
          f"PUMA {dens['PUMA']:.3f}, county {dens['county']:.3f}")
    print("  (the rate is a share, so density is already normalised out; the placebo row "
          "shows what an unconcentrated group looks like)")


if __name__ == "__main__":
    main()
