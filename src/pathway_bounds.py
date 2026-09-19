"""Item 3 and correction A: reconcile the mortgage at-risk figures and bound them.

THE DISCREPANCY. Block 4 item 2 reported an "all embodied work" mortgage at-risk rate of
20.68 percent. The Block 3 pathway table sums to about 11.5 percent (driving 0.98, gated
7.83, manipulation 2.74). Both are correct arithmetic on DIFFERENT estimands:

    geo_groups.py used the household's share of wage income earned in the group, unweighted.
    build_pathways.py multiplied that share by the occupation's embodiment P.

P averages roughly 0.55 across high-P occupations, and 11.55 / 20.68 = 0.558. The whole gap
is the embodiment weighting. Nothing is wrong; two different questions were being answered
without saying so.

THREE DEFINITIONS, reported as upper, central and lower bounds:

    UPPER    full annual debt service of every household with ANY earner in the pathway.
             Answers "how much debt service sits in households touched by this pathway".
             Overstates, because a household with one exposed earner among three is counted
             whole.

    CENTRAL  debt service weighted by the pathway's share of household WAGE INCOME.
             Answers "how much debt service is serviced out of wages earned in this
             pathway". This is the paper's HEADLINE definition.

    LOWER    the central figure additionally weighted by embodiment P.
             Answers "how much debt service is serviced out of the physically embodied
             portion of wages earned in this pathway". Appropriate only when P is being
             used as an intensity, not as a scope filter, and it double-counts the fact that
             pathway membership already required high P.

The headline is CENTRAL. P is used to SELECT occupations into scope, so using it again as a
weight applies the same filter twice.
"""
import io, json, pathlib, zipfile
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).parents[1]
RAW, OUT = ROOT / "data" / "raw", ROOT / "data" / "processed"
PPART = [("csv_pus.zip", "psam_pusa.csv"), ("csv_pus.zip", "psam_pusb.csv")]
HPART = [("csv_hus.zip", "psam_husa.csv"), ("csv_hus.zip", "psam_husb.csv")]
GROUPS = ["driving", "gated", "manipulation", "all_embodied"]


def chunks(zf, fn, cols, size=300_000):
    z = zipfile.ZipFile(RAW / "pums" / zf)
    with z.open(fn) as fh:
        for ch in pd.read_csv(io.TextIOWrapper(fh, encoding="utf-8", errors="replace"),
                              usecols=cols, dtype={"SERIALNO": str},
                              chunksize=size, low_memory=False):
            yield ch


def main():
    fl = pd.read_csv(OUT / "pathway_assignment.csv")
    fl = fl[fl["employment"].notna() & (fl["employment"] > 0)]
    pmap = dict(zip(fl["occp"], fl["pathway"]))
    Pmap = dict(zip(fl["occp"], fl["embodiment_P"]))
    in_scope = set(fl.loc[fl["pathway"] != "out_of_scope", "occp"])

    print("person pass ...")
    parts = []
    for zf, fn in PPART:
        for ch in chunks(zf, fn, ["SERIALNO", "OCCP", "WAGP", "ADJINC"]):
            occ = pd.to_numeric(ch["OCCP"], errors="coerce")
            wage = (pd.to_numeric(ch["WAGP"], errors="coerce").fillna(0.0)
                    * pd.to_numeric(ch["ADJINC"], errors="coerce") / 1e6)
            d = pd.DataFrame({"SERIALNO": ch["SERIALNO"], "wage": wage,
                              "occp": occ,
                              "path": occ.map(pmap),
                              "P": occ.map(Pmap).fillna(0.0)})
            parts.append(d[d["wage"] > 0])
    P = pd.concat(parts, ignore_index=True)
    P["emb"] = np.where(P["occp"].isin(in_scope), "all_embodied", None)

    tot = P.groupby("SERIALNO")["wage"].sum().rename("hh_wage")
    # primary earner's pathway
    prim = (P.sort_values("wage").groupby("SERIALNO")
              .agg(prim_path=("path", "last")))
    H = pd.DataFrame(tot).join(prim)

    for g in GROUPS:
        sel = P[P["path"] == g] if g != "all_embodied" else P[P["occp"].isin(in_scope)]
        inc = sel.groupby("SERIALNO")["wage"].sum().rename(f"inc_{g}")
        pw = (sel.assign(v=sel["wage"] * sel["P"]).groupby("SERIALNO")["v"]
                 .sum().rename(f"pw_{g}"))
        H = H.join(inc).join(pw)
        H[f"inc_{g}"] = H[f"inc_{g}"].fillna(0.0)
        H[f"pw_{g}"] = H[f"pw_{g}"].fillna(0.0)
        H[f"any_{g}"] = (H[f"inc_{g}"] > 0).astype(float)
        H[f"sh_{g}"] = np.where(H["hh_wage"] > 0, H[f"inc_{g}"] / H["hh_wage"], 0.0)
        H[f"shP_{g}"] = np.where(H["hh_wage"] > 0, H[f"pw_{g}"] / H["hh_wage"], 0.0)
        H[f"prim_{g}"] = (H["prim_path"] == g).astype(float) if g != "all_embodied" else \
            H["prim_path"].isin(["driving", "gated", "manipulation"]).astype(float)

    print("household pass ...")
    hp = []
    for zf, fn in HPART:
        for ch in chunks(zf, fn, ["SERIALNO", "WGTP", "TEN", "MRGP", "GRNTP",
                                  "ADJHSG", "HINCP", "ADJINC"]):
            for c in ["WGTP", "TEN", "MRGP", "GRNTP", "ADJHSG", "HINCP", "ADJINC"]:
                ch[c] = pd.to_numeric(ch[c], errors="coerce")
            a = ch["ADJHSG"] / 1e6
            ch["mort"] = np.nan_to_num(np.where(ch["TEN"] == 1, ch["MRGP"] * 12 * a, 0.0))
            ch["rent"] = np.nan_to_num(np.where(ch["TEN"] == 3, ch["GRNTP"] * 12 * a, 0.0))
            ch["hh_inc"] = ch["HINCP"] * ch["ADJINC"] / 1e6
            hp.append(ch[["SERIALNO", "WGTP", "TEN", "mort", "rent", "hh_inc"]])
    HH = pd.concat(hp, ignore_index=True).join(H, on="SERIALNO")
    HH["WGTP"] = HH["WGTP"].fillna(0.0)

    tot_m = float((HH["mort"] * HH["WGTP"]).sum())
    tot_r = float((HH["rent"] * HH["WGTP"]).sum())
    tot_hh = float(HH["WGTP"].sum())

    def wmed(v, w):
        m = np.isfinite(v) & (w > 0)
        v, w = np.asarray(v)[m], np.asarray(w)[m]
        if not len(v):
            return np.nan
        o = np.argsort(v)
        return float(np.interp(0.5, np.cumsum(w[o]) / w[o].sum(), v[o]))

    rows = []
    for g in GROUPS:
        sub = HH[HH[f"any_{g}"] == 1]
        w = sub["WGTP"]
        rows.append({
            "group": g,
            "households_weighted": float(w.sum()),
            "household_share_pct": 100 * float(w.sum()) / tot_hh,
            "median_household_income_usd": wmed(sub["hh_inc"], w),
            "homeownership_rate_pct": 100 * float(
                w[sub["TEN"].isin([1, 2])].sum()) / float(w.sum()),
            "mortgaged_ownership_pct": 100 * float(
                w[sub["TEN"] == 1].sum()) / float(w.sum()),
            "primary_earner_in_group_pct": 100 * float(
                (sub[f"prim_{g}"] * w).sum()) / float(w.sum()),
            "mortgage_UPPER_pct": 100 * float((HH["mort"] * HH[f"any_{g}"]
                                               * HH["WGTP"]).sum()) / tot_m,
            "mortgage_CENTRAL_pct": 100 * float((HH["mort"] * HH[f"sh_{g}"]
                                                 * HH["WGTP"]).sum()) / tot_m,
            "mortgage_LOWER_pct": 100 * float((HH["mort"] * HH[f"shP_{g}"]
                                               * HH["WGTP"]).sum()) / tot_m,
            "rent_UPPER_pct": 100 * float((HH["rent"] * HH[f"any_{g}"]
                                           * HH["WGTP"]).sum()) / tot_r,
            "rent_CENTRAL_pct": 100 * float((HH["rent"] * HH[f"sh_{g}"]
                                             * HH["WGTP"]).sum()) / tot_r,
            "rent_LOWER_pct": 100 * float((HH["rent"] * HH[f"shP_{g}"]
                                           * HH["WGTP"]).sum()) / tot_r,
        })
    T = pd.DataFrame(rows)
    T.round(3).to_csv(OUT / "pathway_bounds.csv", index=False)

    s = T[T["group"] != "all_embodied"]
    bridge = {
        "pathway_sum_CENTRAL_mortgage_pct": float(s["mortgage_CENTRAL_pct"].sum()),
        "pathway_sum_LOWER_mortgage_pct": float(s["mortgage_LOWER_pct"].sum()),
        "all_embodied_CENTRAL_mortgage_pct": float(
            T.loc[T["group"] == "all_embodied", "mortgage_CENTRAL_pct"].iloc[0]),
        "all_embodied_LOWER_mortgage_pct": float(
            T.loc[T["group"] == "all_embodied", "mortgage_LOWER_pct"].iloc[0]),
        "block4_geo_groups_reported": 20.68,
        "block3_pathway_table_reported": 11.55,
        "explanation": ("Block 4 used the CENTRAL (wage-share) definition; Block 3 used the "
                        "LOWER (P-weighted) definition. The ratio is the mean embodiment P "
                        "of in-scope occupations."),
        "implied_mean_P": float(T.loc[T["group"] == "all_embodied", "mortgage_LOWER_pct"].iloc[0]
                                / T.loc[T["group"] == "all_embodied", "mortgage_CENTRAL_pct"].iloc[0]),
        "headline_definition": "CENTRAL: weighted by the pathway share of household wage income",
    }
    (OUT / "pathway_bounds_summary.json").write_text(json.dumps(bridge, indent=2))

    pd.set_option("display.width", 240)
    print("\n=== PATHWAY BOUNDS: mortgage and rent debt service at risk (% of national) ===")
    print(T[["group", "mortgage_UPPER_pct", "mortgage_CENTRAL_pct", "mortgage_LOWER_pct",
             "rent_UPPER_pct", "rent_CENTRAL_pct", "rent_LOWER_pct"]]
          .round(2).to_string(index=False))
    print("\n=== HOUSEHOLD CHARACTERISTICS ===")
    print(T[["group", "households_weighted", "household_share_pct",
             "median_household_income_usd", "homeownership_rate_pct",
             "mortgaged_ownership_pct", "primary_earner_in_group_pct"]]
          .round(1).to_string(index=False))
    print("\n=== BRIDGE (correction A) ===")
    for k, v in bridge.items():
        print(f"  {k:42s} {v if isinstance(v, str) else round(v, 3)}")


if __name__ == "__main__":
    main()
