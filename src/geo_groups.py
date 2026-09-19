"""Item 2: the S-free geography result. Supersedes the c-path concentration finding.

Why this replaces A25. The earlier result (concentration of the at-risk rate falls as c
rises) is partly mechanical, because the c-threshold runs on S_rank and A23/the SMT test
showed S largely proxies manufacturing. A c-path built on a manufacturing proxy will
mechanically start in manufacturing geography and diffuse out of it. This version defines
the two groups EXTERNALLY, with no S anywhere:

  (a) ROBOT-REACHABLE  occupations in the top quintile of Webb (2020) pct_robot.
                       Robustness: top decile and top tercile.
  (b) EMBODIED         occupations at or above the median embodiment P.

REGISTERED HYPOTHESIS (owner, before running): (a) is geographically concentrated at roughly
Acemoglu and Restrepo magnitudes; (b) is near-uniform.

Reported per group: Gini, p90/p10 and p99/p1 of the AT-RISK RATE across PUMAs and counties,
and the tradable share of the wage bill at risk. Acemoglu and Restrepo (2020) JPE 128(6)
report their commuting-zone robot exposure spanning about 9 robots per thousand workers from
p1 to p99, roughly a ninefold spread.
"""
import io, json, pathlib, zipfile
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).parents[1]
RAW, OUT = ROOT / "data" / "raw", ROOT / "data" / "processed"
PPART = [("csv_pus.zip", "psam_pusa.csv"), ("csv_pus.zip", "psam_pusb.csv")]
HPART = [("csv_hus.zip", "psam_husa.csv"), ("csv_hus.zip", "psam_husb.csv")]
TRADABLE = {"11", "21", "31", "32", "33"}
NONTRADABLE = {"44", "45", "61", "62", "71", "72", "81"}


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
    xs = np.sort(x)
    n = len(xs)
    return float((n + 1 - 2 * np.sum(np.cumsum(xs)) / np.cumsum(xs)[-1]) / n)


def spread(x, lo, hi):
    x = np.asarray(x, float)
    x = x[np.isfinite(x) & (x > 0)]
    if len(x) < 50:
        return np.nan
    a, b = np.percentile(x, lo), np.percentile(x, hi)
    return float(b / a) if a > 0 else np.nan


def main():
    grid = pd.read_csv(OUT / "paei_c.csv")
    base = grid[grid["c"] == 0.0][["occp", "title", "embodiment_P", "employment",
                                   "wage_bill"]].dropna(subset=["employment"])
    base = base[base["employment"] > 0]
    webb = pd.read_csv(OUT / "paei_webb_matched.csv")[["occp", "pct_robot"]]
    B = base.merge(webb, on="occp", how="left")

    w = B.dropna(subset=["pct_robot"])
    cuts = {q: float(np.percentile(w["pct_robot"], 100 - q)) for q in (10, 20, 33)}
    P_MED = float(B["embodiment_P"].median())

    groups = {
        "robot_reachable_top20": B["pct_robot"] >= cuts[20],
        "robot_reachable_top10": B["pct_robot"] >= cuts[10],
        "robot_reachable_top33": B["pct_robot"] >= cuts[33],
        "embodied_highP": B["embodiment_P"] >= P_MED,
    }
    memb = {g: set(B.loc[m.fillna(False), "occp"]) for g, m in groups.items()}
    for g, s in memb.items():
        sub = B[B["occp"].isin(s)]
        print(f"{g:24s} {len(s):4d} occupations, {sub['employment'].sum():>12,.0f} workers")

    # ---- PUMA-level accumulation ----
    print("\nperson pass ...")
    acc = {g: {} for g in memb}
    tot_wage, hh_share = {}, {}
    hs = {g: [] for g in memb}
    for zf, fn in PPART:
        for ch in chunks(zf, fn, ["SERIALNO", "STATE", "PUMA", "OCCP", "WAGP",
                                  "ADJINC", "PWGTP"]):
            occ = pd.to_numeric(ch["OCCP"], errors="coerce")
            wage = (pd.to_numeric(ch["WAGP"], errors="coerce").fillna(0.0)
                    * pd.to_numeric(ch["ADJINC"], errors="coerce") / 1e6)
            pw = pd.to_numeric(ch["PWGTP"], errors="coerce").fillna(0.0)
            key = (ch["STATE"].astype(int).astype(str).str.zfill(2)
                   + ch["PUMA"].astype(int).astype(str).str.zfill(5))
            wt = (wage * pw).groupby(key).sum()
            for k, v in wt.items():
                tot_wage[k] = tot_wage.get(k, 0.0) + v
            d = pd.DataFrame({"SERIALNO": ch["SERIALNO"], "wage": wage})
            d = d[d["wage"] > 0]
            tt = d.groupby("SERIALNO")["wage"].sum()
            for sid, v in tt.items():
                hh_share[sid] = hh_share.get(sid, 0.0) + v
            for g, s in memb.items():
                m = occ.isin(s)
                if m.any():
                    a = (wage * pw * m).groupby(key).sum()
                    for k, v in a.items():
                        acc[g][k] = acc[g].get(k, 0.0) + v
                    hs[g].append(d[m[d.index]].groupby("SERIALNO")["wage"].sum())
    HHS = {g: (pd.concat(v).groupby(level=0).sum() if v else pd.Series(dtype=float))
           for g, v in hs.items()}
    TOT = pd.Series(hh_share)

    print("household pass ...")
    hm, hr, hmt, hrt = {g: {} for g in memb}, {g: {} for g in memb}, {}, {}
    for zf, fn in HPART:
        for ch in chunks(zf, fn, ["SERIALNO", "STATE", "PUMA", "WGTP", "TEN",
                                  "MRGP", "GRNTP", "ADJHSG"]):
            for c in ["WGTP", "TEN", "MRGP", "GRNTP", "ADJHSG"]:
                ch[c] = pd.to_numeric(ch[c], errors="coerce")
            a = ch["ADJHSG"] / 1e6
            mort = np.nan_to_num(np.where(ch["TEN"] == 1, ch["MRGP"] * 12 * a, 0.0))
            rent = np.nan_to_num(np.where(ch["TEN"] == 3, ch["GRNTP"] * 12 * a, 0.0))
            key = (ch["STATE"].astype(int).astype(str).str.zfill(2)
                   + ch["PUMA"].astype(int).astype(str).str.zfill(5))
            W = ch["WGTP"].fillna(0.0).to_numpy()
            for k, v in pd.Series(mort * W).groupby(key).sum().items():
                hmt[k] = hmt.get(k, 0.0) + v
            for k, v in pd.Series(rent * W).groupby(key).sum().items():
                hrt[k] = hrt.get(k, 0.0) + v
            tot = ch["SERIALNO"].map(TOT)
            for g in memb:
                sh = (ch["SERIALNO"].map(HHS[g]) / tot).fillna(0.0).to_numpy()
                for k, v in pd.Series(mort * sh * W).groupby(key).sum().items():
                    hm[g][k] = hm[g].get(k, 0.0) + v
                for k, v in pd.Series(rent * sh * W).groupby(key).sum().items():
                    hr[g][k] = hr[g].get(k, 0.0) + v

    # ---- assemble and measure concentration ----
    cnt = pd.read_csv(OUT / "puma_to_county_afact.csv", dtype={"puma_id": str,
                                                               "county_fips": str})
    rows = []
    for g in memb:
        D = pd.DataFrame({"puma_id": list(tot_wage.keys())})
        D["wage_tot"] = D["puma_id"].map(tot_wage)
        D["wage_risk"] = D["puma_id"].map(acc[g]).fillna(0.0)
        D["mort_tot"] = D["puma_id"].map(hmt).fillna(0.0)
        D["mort_risk"] = D["puma_id"].map(hm[g]).fillna(0.0)
        D["rent_tot"] = D["puma_id"].map(hrt).fillna(0.0)
        D["rent_risk"] = D["puma_id"].map(hr[g]).fillna(0.0)
        C = D.merge(cnt[["puma_id", "county_fips", "afact"]], on="puma_id", how="inner")
        for c in ["wage_tot", "wage_risk", "mort_tot", "mort_risk", "rent_tot", "rent_risk"]:
            C[c] = C[c] * C["afact"]
        C = C.groupby("county_fips")[["wage_tot", "wage_risk", "mort_tot", "mort_risk",
                                      "rent_tot", "rent_risk"]].sum().reset_index()
        for lvl, df in [("PUMA", D), ("county", C)]:
            for metric, num, den in [("wage", "wage_risk", "wage_tot"),
                                     ("mortgage", "mort_risk", "mort_tot"),
                                     ("rent", "rent_risk", "rent_tot")]:
                r = (df[num] / df[den].replace(0, np.nan)).replace(
                    [np.inf, -np.inf], np.nan).dropna()
                rows.append({"group": g, "level": lvl, "metric": metric,
                             "n_areas": int(len(r)),
                             "national_rate": float(df[num].sum() / df[den].sum()),
                             "gini_of_rate": gini(r),
                             "p90_p10": spread(r, 10, 90),
                             "p99_p1": spread(r, 1, 99)})
    T = pd.DataFrame(rows)
    T.round(4).to_csv(OUT / "geo_groups_concentration.csv", index=False)

    # ---- tradable share of wage bill at risk ----
    pan = pd.read_csv(OUT / "within_industry_s_panel.csv")
    ncols = [c for c in pan.columns if c.isdigit() and len(c) == 2]
    pan["trad"] = pan[[c for c in ncols if c in TRADABLE]].sum(axis=1)
    pan["nontrad"] = pan[[c for c in ncols if c in NONTRADABLE]].sum(axis=1)
    tr = []
    for g, s in memb.items():
        d = pan[pan["occp"].isin(s)].merge(base[["occp", "wage_bill"]], on="occp",
                                           how="inner", suffixes=("", "_b"))
        wb = d["wage_bill"] if "wage_bill" in d else d["wage_bill_b"]
        tot = float(wb.sum())
        tr.append({"group": g, "wage_bill_usd_bn": tot / 1e9,
                   "tradable_pct": 100 * float((wb * d["trad"]).sum()) / tot,
                   "nontradable_pct": 100 * float((wb * d["nontrad"]).sum()) / tot})
    TR = pd.DataFrame(tr)
    TR.round(2).to_csv(OUT / "geo_groups_tradable.csv", index=False)

    (OUT / "geo_groups_summary.json").write_text(json.dumps(
        {"webb_pct_robot_cuts": cuts, "P_median": P_MED,
         "group_sizes": {g: int(len(s)) for g, s in memb.items()},
         "concentration": T.round(4).to_dict("records"),
         "tradable": TR.round(3).to_dict("records"),
         "ar_benchmark_p1_p99": 9.0}, indent=2))

    pd.set_option("display.width", 220)
    print("\n=== Concentration of the AT-RISK RATE, by externally defined group ===")
    print(T[T["metric"].isin(["wage", "mortgage"])]
          .sort_values(["metric", "level", "group"])
          .round(4).to_string(index=False))
    print("\n=== Tradable share of the wage bill ===")
    print(TR.round(1).to_string(index=False))


if __name__ == "__main__":
    main()
