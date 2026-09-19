"""Step 2: PAEI(c), the scenario-conditional Physical AI Exposure Index.

Why this exists. PAEI as built in Phase 1 penalises unstructured environments. But coping
with unstructured environments is precisely what Physical AI is supposed to achieve. So
PAEI at c = 0 is an index of exposure to CURRENT industrial robotics, not to Physical AI.
Making the index conditional on realised capability is what turns it into a measure of the
thing the paper is about.

Definitions:
    P in [0,1]  embodiment intensity: does the job require a physical body
    S in [0,1]  environmental structure: 1 is fully structured, 0 is fully unstructured
    c in [0,1]  realised Physical AI capability. c = 0 is current industrial robotics,
                which works only in structured settings. c = 1 is robust operation in
                unstructured settings, where structure no longer gates deployment.

Two functional forms, both reported:

    SMOOTH     PAEI_smooth(c) = P * S^(1 - c)
               At c = 0 this is P * S, the Phase 1 index. At c = 1 it is P: exposure equals
               embodiment, because structure no longer matters.

    THRESHOLD  exposed(c) = 1 if deficit <= c, with exposure magnitude P

Two corrections to the naive threshold implementation, both forced by the data:

1. SCALE. Raw S is compressed (sd 0.071, range 0.29 to 0.70) because it is a difference of
   two bounded means recentred on 0.5. A threshold on the raw deficit (1 - S) gives a step
   function: nothing exposed below c = 0.30, everything exposed by c = 0.70. That reflects
   the scale, not the economics. The reported threshold uses S_rank, the
   employment-weighted percentile rank of S, which gives c an interpretable meaning:
   capability c handles occupations up to the c-th percentile of unstructuredness. The raw
   version is still reported so the degeneracy is visible.

2. EMBODIMENT GATE. The threshold rule keys only on structure, so without a gate the
   switcher list is led by Lawyers (P = 0.095) and Chief Executives (P = 0.132). An
   occupation that needs no body cannot be displaced by a robot at any c. Switchers are
   therefore gated at the median P, and the headline exposure measure is weighted by P.

MODELLING ASSUMPTION, stated plainly. The mapping from scenario labels to c values is
stipulated, not estimated. No published robotics capability benchmark was located that maps
onto a normalised structure-tolerance scale, so anchoring c to benchmarks is outstanding.
Every result is reported across the whole c grid and the named scenarios are read off that
grid rather than driving it.
"""
import io, json, pathlib, zipfile
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).parents[1]
RAW, OUT = ROOT / "data" / "raw", ROOT / "data" / "processed"

C_GRID = np.round(np.arange(0.0, 1.0001, 0.05), 3)
SCENARIOS = {"low": 0.20, "medium": 0.50, "high": 0.80}   # stipulated, see docstring


def pums_occupation_stats():
    """Employment, wage bill and median hourly wage by 6-digit SOC, from ACS PUMS 2023."""
    occ = pd.read_csv(OUT / "occp_to_paei.csv")[["occp", "soc"]]
    frames = []
    z = zipfile.ZipFile(RAW / "pums" / "csv_pus.zip")
    for fn in ["psam_pusa.csv", "psam_pusb.csv"]:
        with z.open(fn) as fh:
            for ch in pd.read_csv(io.TextIOWrapper(fh, encoding="utf-8", errors="replace"),
                                  usecols=["OCCP", "PWGTP", "WAGP", "ADJINC", "WKHP"],
                                  chunksize=500_000, low_memory=False):
                frames.append(ch)
    P = pd.concat(frames, ignore_index=True)
    P["OCCP"] = pd.to_numeric(P["OCCP"], errors="coerce")
    P["PWGTP"] = pd.to_numeric(P["PWGTP"], errors="coerce")
    P["wage"] = (pd.to_numeric(P["WAGP"], errors="coerce").fillna(0)
                 * pd.to_numeric(P["ADJINC"], errors="coerce") / 1e6)
    P["WKHP"] = pd.to_numeric(P["WKHP"], errors="coerce")
    P = P.merge(occ, left_on="OCCP", right_on="occp", how="inner")
    P = P[P["PWGTP"].notna()]
    hrs = P["WKHP"] * 52.0
    P["hourly"] = np.where((hrs > 0) & (P["wage"] > 0), P["wage"] / hrs, np.nan)

    def agg(d):
        w = d["PWGTP"].to_numpy(float)
        hourly = d["hourly"].to_numpy(float)
        ok = np.isfinite(hourly)
        med = np.nan
        if ok.sum() > 0:
            o = np.argsort(hourly[ok])
            hv, hw = hourly[ok][o], w[ok][o]
            med = float(np.interp(0.5, np.cumsum(hw) / hw.sum(), hv))
        return pd.Series({"employment": float(w.sum()),
                          "wage_bill": float((d["wage"] * d["PWGTP"]).sum()),
                          "median_hourly_wage": med})

    return P.groupby("soc").apply(agg, include_groups=False).reset_index()


def main():
    paei = pd.read_csv(OUT / "paei_onet.csv")
    paei["soc"] = paei["onet_soc"].astype(str).str[:7]
    soc = (paei.groupby("soc")
           .agg(title=("title", "first"), P=("embodiment_P", "mean"),
                S=("structure_S", "mean"), PAEI_c0=("PAEI", "mean"))
           .reset_index())

    stats = pums_occupation_stats()
    df = soc.merge(stats, on="soc", how="left")

    w = df["employment"].fillna(0.0).to_numpy(float)
    o = np.argsort(df["S"].to_numpy())
    cw = np.cumsum(w[o]) / max(w.sum(), 1.0)
    rank = np.empty(len(df)); rank[o] = cw
    df["S_rank"] = rank
    df["deficit_raw"] = 1.0 - df["S"]
    df["deficit_rank"] = 1.0 - df["S_rank"]

    covered = df["employment"].notna() & (df["employment"] > 0)
    print(f"SOC occupations: {len(df)}; with PUMS employment: {int(covered.sum())} "
          f"({100*covered.mean():.1f}%)")
    E = df[covered].copy()
    emp_tot, wb_tot = E["employment"].sum(), E["wage_bill"].sum()
    print(f"employment covered: {emp_tot:,.0f}; wage bill covered: ${wb_tot/1e9:,.1f} bn")

    recs = []
    for _, r in df.iterrows():
        for c in C_GRID:
            recs.append({
                "soc": r["soc"], "title": r["title"], "c": c,
                "embodiment_P": r["P"], "structure_S": r["S"],
                "structure_S_rank": r["S_rank"],
                "paei_smooth": r["P"] * (r["S"] ** (1.0 - c)),
                "structure_deficit_raw": r["deficit_raw"],
                "structure_deficit_rank": r["deficit_rank"],
                "exposed_threshold_raw": int(r["deficit_raw"] <= c),
                "exposed_threshold_rank": int(r["deficit_rank"] <= c),
                "exposure_magnitude_rank": r["P"] * float(r["deficit_rank"] <= c),
                "employment": r["employment"], "wage_bill": r["wage_bill"],
                "median_hourly_wage": r["median_hourly_wage"],
            })
    G = pd.DataFrame(recs)
    G.round(6).to_csv(OUT / "paei_c.csv", index=False)

    front = []
    for c in C_GRID:
        g = G[(G["c"] == c) & G["soc"].isin(E["soc"])]
        ex = g["exposed_threshold_rank"] == 1
        embodied_tot = float((g["employment"] * g["embodiment_P"]).sum())
        front.append({
            "c": c,
            "mean_paei_smooth_empwt": float(np.average(g["paei_smooth"],
                                                       weights=g["employment"])),
            "mean_paei_smooth_wagewt": float(np.average(g["paei_smooth"],
                                                        weights=g["wage_bill"])),
            "share_employment_exposed_rawS_pct":
                100 * float(g.loc[g["exposed_threshold_raw"] == 1, "employment"].sum()
                            / emp_tot),
            "share_employment_exposed_pct":
                100 * float(g.loc[ex, "employment"].sum() / emp_tot),
            "share_wagebill_exposed_pct":
                100 * float(g.loc[ex, "wage_bill"].sum() / wb_tot),
            "share_embodied_work_exposed_pct":
                (100 * float((g.loc[ex, "employment"] * g.loc[ex, "embodiment_P"]).sum()
                             / embodied_tot) if embodied_tot else 0.0),
            "wagebill_at_risk_usd_bn":
                float((g.loc[ex, "wage_bill"] * g.loc[ex, "embodiment_P"]).sum() / 1e9),
            "n_occupations_exposed": int(ex.sum()),
        })
    F = pd.DataFrame(front)
    F.round(4).to_csv(OUT / "paei_c_frontier.csv", index=False)

    cm, ch = SCENARIOS["medium"], SCENARIOS["high"]
    P_GATE = float(df["P"].median())
    sw = E.copy()
    sw["deficit"] = sw["deficit_rank"]
    switch = sw[(sw["deficit"] > cm) & (sw["deficit"] <= ch)].copy()
    switch = switch[switch["P"] >= P_GATE].copy()
    switch["employment_x_P"] = switch["employment"] * switch["P"]
    switch = switch.sort_values("employment_x_P", ascending=False)
    switch["employment_share_pct"] = 100 * switch["employment"] / emp_tot
    switch[["soc", "title", "P", "S", "S_rank", "deficit", "employment",
            "employment_share_pct", "wage_bill", "median_hourly_wage"]] \
        .round(4).to_csv(OUT / "paei_c_switchers_medium_to_high.csv", index=False)

    summary = {
        "c_grid": [float(x) for x in C_GRID],
        "scenario_c_values": SCENARIOS,
        "scenario_c_values_are": "STIPULATED MODELLING ASSUMPTION, not estimated",
        "structure_scale_note": ("threshold uses S_rank (employment-weighted percentile "
                                 "rank of S); raw-S threshold reported but degenerate"),
        "n_soc_occupations": int(len(df)),
        "n_with_employment": int(covered.sum()),
        "employment_covered": float(emp_tot),
        "wage_bill_covered_usd_bn": float(wb_tot / 1e9),
        "frontier": {
            f"c={c}": {
                "share_employment_exposed_pct": float(
                    F.loc[F["c"] == c, "share_employment_exposed_pct"].iloc[0]),
                "share_embodied_work_exposed_pct": float(
                    F.loc[F["c"] == c, "share_embodied_work_exposed_pct"].iloc[0]),
                "wagebill_at_risk_usd_bn": float(
                    F.loc[F["c"] == c, "wagebill_at_risk_usd_bn"].iloc[0]),
                "mean_paei_smooth_empwt": float(
                    F.loc[F["c"] == c, "mean_paei_smooth_empwt"].iloc[0]),
            } for c in [0.0, 0.2, 0.5, 0.8, 1.0]},
        "switchers_medium_to_high": {
            "embodiment_gate_P_median": P_GATE,
            "n_occupations": int(len(switch)),
            "employment": float(switch["employment"].sum()),
            "employment_share_pct": float(100 * switch["employment"].sum() / emp_tot),
            "wage_bill_usd_bn": float(switch["wage_bill"].sum() / 1e9),
        },
    }
    (OUT / "paei_c_summary.json").write_text(json.dumps(summary, indent=2))

    pd.set_option("display.width", 210)
    print("\n=== Exposure frontier ===")
    print("(rawS column shows the degenerate scale the rank version replaces)")
    print(F[["c", "share_employment_exposed_rawS_pct", "share_employment_exposed_pct",
             "share_embodied_work_exposed_pct", "wagebill_at_risk_usd_bn",
             "mean_paei_smooth_empwt"]].round(2).to_string(index=False))

    print(f"\n=== Occupations switching between c={cm} and c={ch} (embodiment-gated) ===")
    print(f"  embodiment gate: P >= {P_GATE:.3f} (median)")
    print(f"  {len(switch)} occupations, {switch['employment'].sum():,.0f} workers "
          f"({100*switch['employment'].sum()/emp_tot:.1f}% of covered employment), "
          f"${switch['wage_bill'].sum()/1e9:,.1f} bn wage bill")
    print(switch.head(20)[["title", "P", "S_rank", "deficit", "employment",
                           "median_hourly_wage"]].round(3).to_string(index=False,
                                                                     max_colwidth=46))


if __name__ == "__main__":
    main()
