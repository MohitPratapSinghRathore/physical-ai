"""Item 3: concentration against group breadth, by exposure type and geographic scale.

Four breadths (top 10, 20, 30, 50 percent of employment) x two exposure types x three
scales (PUMA, county, metro/CBSA). Gini, p90/p10, p99/p1, Moran's I (county centroids from
the Census 2024 Gazetteer), and a Theil decomposition into within-metro and between-metro.

The point of the exercise: the "near-uniformity" claim depends on how broadly the group is
defined, and the project has used two different definitions without saying so (A37).
"""
import io, json, pathlib, zipfile
import numpy as np
import pandas as pd
from scipy import stats
import importlib.util

ROOT = pathlib.Path(__file__).parents[1]
RAW, OUT = ROOT / "data" / "raw", ROOT / "data" / "processed"
spec = importlib.util.spec_from_file_location("h3", ROOT / "src" / "h3_geography.py")
h3 = importlib.util.module_from_spec(spec); spec.loader.exec_module(h3)
BREADTHS = [0.10, 0.20, 0.30, 0.50]


def gini(x):
    return h3.gini(x)


def theil(x, w, grp):
    """Theil T of rate x with weights w, decomposed by group."""
    x = np.asarray(x, float); w = np.asarray(w, float)
    m = np.isfinite(x) & (x > 0) & (w > 0)
    x, w, grp = x[m], w[m], np.asarray(grp)[m]
    mu = np.average(x, weights=w)
    tot = float(np.average((x / mu) * np.log(x / mu), weights=w))
    within = 0.0
    for g in np.unique(grp):
        s = grp == g
        if s.sum() < 2:
            continue
        mg = np.average(x[s], weights=w[s])
        if mg <= 0:
            continue
        tg = float(np.average((x[s] / mg) * np.log(x[s] / mg), weights=w[s]))
        within += (w[s].sum() / w.sum()) * (mg / mu) * tg
    return tot, within, tot - within


def morans_i(v, lat, lon, w_area, k=8):
    v = np.asarray(v, float)
    ok = np.isfinite(v) & np.isfinite(lat) & np.isfinite(lon)
    v = v[ok]; C = np.column_stack([lat[ok], lon[ok]])
    n = len(v)
    if n < 30:
        return np.nan, np.nan
    z = v - v.mean()
    d2 = ((C[:, None, :] - C[None, :, :]) ** 2).sum(axis=2)
    np.fill_diagonal(d2, np.inf)
    idx = np.argpartition(d2, k, axis=1)[:, :k]
    num = sum(z[i] * z[idx[i]].mean() for i in range(n))
    I = (num / n) / ((z ** 2).sum() / n)
    return float(I), float(-1.0 / (n - 1))


def build_breadth_groups(B):
    g = {}
    for col, name in [("aioe", "cognitive"), ("embodiment_P", "embodied")]:
        d = B.dropna(subset=[col]).sort_values(col)
        c = np.cumsum(d["employment"].to_numpy()) / d["employment"].sum()
        for br in BREADTHS:
            cut = np.interp(1 - br, c, d[col].to_numpy())
            g[f"{name}_top{int(br*100)}"] = set(B.loc[B[col] >= cut, "occp"])
    return g


def main():
    B, _ = h3.build_groups()
    groups = build_breadth_groups(B)
    for k, s in groups.items():
        print(f"{k:22s} {len(s):4d} occs, "
              f"{100*B[B.occp.isin(s)]['employment'].sum()/B['employment'].sum():5.1f}% of employment")

    print("\nperson pass ...")
    tot, acc = {}, {k: {} for k in groups}
    z = zipfile.ZipFile(RAW / "pums" / "csv_pus.zip")
    for fn in ["psam_pusa.csv", "psam_pusb.csv"]:
        with z.open(fn) as fh:
            for ch in pd.read_csv(io.TextIOWrapper(fh, encoding="utf-8", errors="replace"),
                                  usecols=["STATE", "PUMA", "OCCP", "WAGP", "ADJINC",
                                           "PWGTP"], chunksize=300_000, low_memory=False):
                occ = pd.to_numeric(ch["OCCP"], errors="coerce")
                wage = (pd.to_numeric(ch["WAGP"], errors="coerce").fillna(0.0)
                        * pd.to_numeric(ch["ADJINC"], errors="coerce") / 1e6)
                pw = pd.to_numeric(ch["PWGTP"], errors="coerce").fillna(0.0)
                key = (ch["STATE"].astype(int).astype(str).str.zfill(2)
                       + ch["PUMA"].astype(int).astype(str).str.zfill(5))
                for k2, v in (wage * pw).groupby(key).sum().items():
                    tot[k2] = tot.get(k2, 0.0) + v
                for g, s in groups.items():
                    sel = occ.isin(s)
                    if sel.any():
                        for k2, v in (wage * pw * sel).groupby(key).sum().items():
                            acc[g][k2] = acc[g].get(k2, 0.0) + v

    D = pd.DataFrame({"puma_id": sorted(tot)})
    D["wt"] = D["puma_id"].map(tot)
    for g in groups:
        D[f"n_{g}"] = D["puma_id"].map(acc[g]).fillna(0.0)

    cnt = pd.read_csv(OUT / "puma_to_county_afact.csv",
                      dtype={"puma_id": str, "county_fips": str})
    M = D.merge(cnt[["puma_id", "county_fips", "afact"]], on="puma_id", how="inner")
    for c in ["wt"] + [f"n_{g}" for g in groups]:
        M[c] = M[c] * M["afact"]
    Cty = M.groupby("county_fips").sum(numeric_only=True).reset_index()

    # centroids and CBSA
    zg = zipfile.ZipFile(RAW / "gazetteer" / "2024_Gaz_counties.zip")
    gz = pd.read_csv(io.TextIOWrapper(zg.open(zg.namelist()[0]), encoding="latin-1"), sep="\t")
    gz.columns = [c.strip() for c in gz.columns]
    gz["county_fips"] = gz["GEOID"].astype(int).astype(str).str.zfill(5)
    Cty = Cty.merge(gz[["county_fips", "INTPTLAT", "INTPTLONG"]], on="county_fips", how="left")
    fh = pd.read_excel(RAW / "fhfa" / "conforming_limits_2025.xlsx", header=1)
    fh.columns = [str(c).strip().replace("\n", " ") for c in fh.columns]
    fh["county_fips"] = (fh["FIPS State Code"].astype(str).str.zfill(2)
                         + fh["FIPS County Code"].astype(str).str.zfill(3))
    Cty = Cty.merge(fh[["county_fips", "CBSA Number"]].drop_duplicates("county_fips"),
                    on="county_fips", how="left")
    # REPAIR. The first run pooled every non-metro county into ONE pseudo-group, which put
    # all rural variation into the "within" term and biased the decomposition. Non-metro
    # counties now form one group PER STATE (state non-metro remainders), the standard BEA
    # and BLS treatment, which keeps every group geographically coherent.
    Cty["state_fips"] = Cty["county_fips"].str[:2]
    Cty["region_group"] = np.where(
        Cty["CBSA Number"].notna(),
        "CBSA_" + Cty["CBSA Number"].astype("Int64").astype(str),
        "NONMETRO_" + Cty["state_fips"])

    rows = []
    for g in groups:
        for lvl, df in [("PUMA", D), ("county", Cty)]:
            r = (df[f"n_{g}"] / df["wt"].replace(0, np.nan)).replace([np.inf, -np.inf], np.nan).dropna()
            rec = {"group": g, "level": lvl, "n_areas": int(len(r)),
                   "national_rate": float(df[f"n_{g}"].sum() / df["wt"].sum()),
                   "gini": gini(r), "p90_p10": h3.spread(r, 10, 90),
                   "p99_p1": h3.spread(r, 1, 99)}
            if lvl == "county":
                rate = (Cty[f"n_{g}"] / Cty["wt"].replace(0, np.nan))
                I, E = morans_i(rate.to_numpy(), Cty["INTPTLAT"].to_numpy(),
                                Cty["INTPTLONG"].to_numpy(), Cty["wt"].to_numpy())
                rec["morans_I"] = I; rec["morans_E"] = E
                t, wi, be = theil(rate, Cty["wt"], Cty["region_group"])
                rec["theil_total"] = t
                rec["theil_within_abs"] = wi
                rec["theil_between_abs"] = be
                rec["theil_within_pct"] = 100 * wi / t if t else np.nan
                rec["theil_between_pct"] = 100 * be / t if t else np.nan
                rec["n_region_groups"] = int(Cty["region_group"].nunique())
            rows.append(rec)
    # metro level
    Met = Cty[Cty["CBSA Number"].notna()].groupby("CBSA Number").sum(numeric_only=True).reset_index()
    for g in groups:
        r = (Met[f"n_{g}"] / Met["wt"].replace(0, np.nan)).replace([np.inf, -np.inf], np.nan).dropna()
        rows.append({"group": g, "level": "metro_CBSA", "n_areas": int(len(r)),
                     "national_rate": float(Met[f"n_{g}"].sum() / Met["wt"].sum()),
                     "gini": gini(r), "p90_p10": h3.spread(r, 10, 90),
                     "p99_p1": h3.spread(r, 1, 99)})
    T = pd.DataFrame(rows)
    T.round(4).to_csv(OUT / "geo_breadth_scale.csv", index=False)
    (OUT / "geo_breadth_scale.json").write_text(json.dumps(T.round(4).to_dict("records"), indent=2))

    pd.set_option("display.width", 240)
    print("\n=== Concentration by BREADTH and SCALE ===")
    print(T[["group", "level", "n_areas", "national_rate", "gini", "p90_p10", "p99_p1"]]
          .round(3).to_string(index=False))
    print("\n=== Moran's I and Theil, county level ===")
    print(T[T["level"] == "county"][["group", "morans_I", "morans_E", "n_region_groups",
                                     "theil_total", "theil_within_abs", "theil_between_abs",
                                     "theil_within_pct",
                                     "theil_between_pct"]].round(4).to_string(index=False))
    make_figure(T)


def make_figure(T):
    """One figure: concentration against group breadth, by exposure type and geographic scale."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 3, figsize=(12.5, 4.0), sharey=True)
    breadths = [int(b * 100) for b in BREADTHS]
    styles = {"cognitive": ("#1f4e79", "o", "Cognitive (Felten AIOE)"),
              "embodied": ("#a6320a", "s", "Embodied (P)")}
    for ax, lvl, ttl in zip(axes, ["PUMA", "county", "metro_CBSA"],
                            ["PUMA (n = 2,462)", "County (n = 3,143)",
                             "Metro CBSA (n = 927)"]):
        for name, (col, mk, lab) in styles.items():
            y = [float(T[(T["group"] == name + "_top" + str(b))
                         & (T["level"] == lvl)]["gini"].iloc[0]) for b in breadths]
            ax.plot(breadths, y, marker=mk, color=col, lw=1.8, ms=6, label=lab)
        ax.set_title(ttl, fontsize=10)
        ax.set_xlabel("Group breadth, percent of employment")
        ax.grid(alpha=0.25, lw=0.6)
        ax.set_xticks(breadths)
    axes[0].set_ylabel("Gini of the local at-risk rate")
    axes[0].legend(frameon=False, fontsize=9)
    fig.suptitle("Measured concentration falls with group breadth, and the ordering of the "
                 "two exposure types reverses between PUMA and county", fontsize=10.5, y=1.03)
    fig.tight_layout()
    out = ROOT / "paper" / "figures"
    out.mkdir(parents=True, exist_ok=True)
    fig.savefig(out / "fig_concentration_breadth_scale.png", dpi=200, bbox_inches="tight")
    fig.savefig(out / "fig_concentration_breadth_scale.pdf", bbox_inches="tight")
    print("figure written to " + str(out / "fig_concentration_breadth_scale.png"))


if __name__ == "__main__":
    main()
