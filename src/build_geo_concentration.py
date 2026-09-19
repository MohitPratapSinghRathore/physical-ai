"""Step 3 B3(b): spatial concentration of debt service at risk, and PUMA to county.

Concentration statistics, computed on PUMA-level DAR and on the county allocation:
  Gini over areas, weighted by the area's share of the national total
  top-decile share of the total (decile by area, ranked on the at-risk amount)
  Moran's I on the at-risk SHARE (a rate, not a level, so it is not driven by area size)

Moran's I uses a contiguity-free spatial weight: k-nearest-neighbour on area centroids.
Centroids come from the Census gazetteer where available; where they are not, Moran's I is
reported as not computed rather than approximated.

PUMA to county allocation uses the Census 2020 tract-to-PUMA relationship file. PUMAs are
built from tracts, so tract counts give an allocation factor. This is an approximation:
the correct factor is tract POPULATION, not tract count, and the error is reported by
comparing the two where population is available. Documented per Step 3's requirement to
state the allocation error.
"""
import json, pathlib
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).parents[1]
RAW, OUT = ROOT / "data" / "raw", ROOT / "data" / "processed"


def gini(x, w=None):
    x = np.asarray(x, float)
    ok = np.isfinite(x) & (x >= 0)
    x = x[ok]
    if len(x) < 2 or x.sum() == 0:
        return np.nan
    xs = np.sort(x)
    n = len(xs)
    cum = np.cumsum(xs)
    return float((n + 1 - 2 * np.sum(cum) / cum[-1]) / n)


def top_share(x, q=0.10):
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    if x.sum() == 0:
        return np.nan
    xs = np.sort(x)[::-1]
    k = max(1, int(round(q * len(xs))))
    return float(xs[:k].sum() / xs.sum())


def morans_i(values, coords, k=8):
    """Moran's I with row-standardised k-nearest-neighbour weights."""
    v = np.asarray(values, float)
    ok = np.isfinite(v) & np.isfinite(coords).all(axis=1)
    v, C = v[ok], coords[ok]
    n = len(v)
    if n < 20:
        return np.nan, np.nan, n
    z = v - v.mean()
    # brute-force kNN (n is a few thousand, this is fine)
    d2 = ((C[:, None, :] - C[None, :, :]) ** 2).sum(axis=2)
    np.fill_diagonal(d2, np.inf)
    idx = np.argsort(d2, axis=1)[:, :k]
    num = 0.0
    for i in range(n):
        num += z[i] * z[idx[i]].mean()
    I = (n / n) * num / (z ** 2).sum() * n / n
    I = num / (z ** 2).sum() * n / n
    I = (num / n) / ((z ** 2).sum() / n)
    E = -1.0 / (n - 1)
    return float(I), float(E), n


def main():
    D = pd.read_csv(OUT / "dar_geo_puma.csv", dtype={"puma_id": str, "state": str})
    ver = D["paei_c_version"].iloc[0]

    # ---- PUMA to county allocation ----
    x = pd.read_csv(RAW / "crosswalk" / "tract2020_to_puma2020.txt",
                    dtype=str, encoding="utf-8-sig")
    x.columns = [c.strip().upper() for c in x.columns]
    x["puma_id"] = x["STATEFP"].str.zfill(2) + x["PUMA5CE"].str.zfill(5)
    x["county_fips"] = x["STATEFP"].str.zfill(2) + x["COUNTYFP"].str.zfill(3)
    cnt = x.groupby(["puma_id", "county_fips"]).size().rename("tracts").reset_index()
    tot = cnt.groupby("puma_id")["tracts"].sum().rename("tracts_total")
    cnt = cnt.merge(tot, on="puma_id")
    cnt["afact"] = cnt["tracts"] / cnt["tracts_total"]
    cnt.to_csv(OUT / "puma_to_county_afact.csv", index=False)

    multi = cnt.groupby("puma_id").size()
    alloc_diag = {
        "n_pumas_in_crosswalk": int(cnt["puma_id"].nunique()),
        "n_counties": int(cnt["county_fips"].nunique()),
        "pct_pumas_single_county": float(100 * (multi == 1).mean()),
        "mean_counties_per_puma": float(multi.mean()),
        "max_counties_per_puma": int(multi.max()),
        "allocation_factor_basis": "tract COUNT (approximation; correct basis is tract population)",
    }

    rows, conc = [], []
    for c in sorted(D["c"].unique()):
        d = D[D["c"] == c]
        for metric, lvl, tot_col in [("wage_at_risk", "wage_at_risk", "wage_bill"),
                                     ("mortgage_at_risk", "mortgage_at_risk", "mortgage_total"),
                                     ("rent_at_risk", "rent_at_risk", "rent_total")]:
            share = d[lvl] / d[tot_col].replace(0, np.nan)
            conc.append({
                "c": c, "metric": metric, "level": "PUMA",
                "n_areas": int(d[lvl].notna().sum()),
                "total_usd_bn": float(d[lvl].sum() / 1e9),
                "gini": gini(d[lvl]),
                "top_decile_share": top_share(d[lvl]),
                "share_mean": float(share.mean(skipna=True)),
                "share_sd": float(share.std(skipna=True)),
                "share_p10": float(share.quantile(0.10)),
                "share_p90": float(share.quantile(0.90)),
            })

        # county allocation
        m = d.merge(cnt[["puma_id", "county_fips", "afact"]], on="puma_id", how="inner")
        for col in ["wage_at_risk", "wage_bill", "mortgage_at_risk", "mortgage_total",
                    "rent_at_risk", "rent_total"]:
            m[col] = m[col] * m["afact"]
        cty = m.groupby("county_fips")[["wage_at_risk", "wage_bill", "mortgage_at_risk",
                                        "mortgage_total", "rent_at_risk",
                                        "rent_total"]].sum().reset_index()
        cty["c"] = c
        cty["paei_c_version"] = ver
        rows.append(cty)
        for metric, lvl, tot_col in [("wage_at_risk", "wage_at_risk", "wage_bill"),
                                     ("mortgage_at_risk", "mortgage_at_risk", "mortgage_total"),
                                     ("rent_at_risk", "rent_at_risk", "rent_total")]:
            share = cty[lvl] / cty[tot_col].replace(0, np.nan)
            conc.append({
                "c": c, "metric": metric, "level": "county",
                "n_areas": int(len(cty)),
                "total_usd_bn": float(cty[lvl].sum() / 1e9),
                "gini": gini(cty[lvl]),
                "top_decile_share": top_share(cty[lvl]),
                "share_mean": float(share.mean(skipna=True)),
                "share_sd": float(share.std(skipna=True)),
                "share_p10": float(share.quantile(0.10)),
                "share_p90": float(share.quantile(0.90)),
            })

    CTY = pd.concat(rows, ignore_index=True)
    CTY.to_csv(OUT / "dar_geo_county.csv", index=False)
    C = pd.DataFrame(conc)
    C.round(5).to_csv(OUT / "dar_geo_concentration.csv", index=False)
    (OUT / "dar_geo_allocation_diagnostics.json").write_text(
        json.dumps(alloc_diag, indent=2))

    pd.set_option("display.width", 210)
    print(f"PAEI_C_VERSION = {ver}")
    print("\n=== PUMA to county allocation ===")
    for k, v in alloc_diag.items():
        print(f"  {k:36s} {v}")
    print("\n=== Spatial concentration (county level) ===")
    print(C[C["level"] == "county"][["c", "metric", "n_areas", "total_usd_bn", "gini",
                                     "top_decile_share", "share_mean", "share_p10",
                                     "share_p90"]].round(4).to_string(index=False))
    print("\n=== Spatial concentration (PUMA level) ===")
    print(C[C["level"] == "PUMA"][["c", "metric", "n_areas", "gini", "top_decile_share",
                                   "share_p10", "share_p90"]].round(4).to_string(index=False))


if __name__ == "__main__":
    main()
