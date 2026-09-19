"""Items 1 and 2: corrected four-way share table, and the proportionality result tested.

ITEM 1. Restrict to households with at least one employed member and a reference person
aged 25 to 64. Split the former "neither" class into:
    middle_exposure_working  working households with no TOP-QUINTILE exposed worker
    non_working              households failing the employment or age restriction
Recompute wage bill, mortgage service and rent shares and leans. Both cognitive definitions.

ITEM 2. State and test the proportionality result. Regress household mortgage debt service
on wage income across exposure deciles, report the slope and its stability, and give the
implied rule mortgage_service_at_risk = k x displaced_wage_bill with k and its interval.
Repeat for rent (expected to differ by type) and for vehicle debt (expected to fail).

CAVEAT on every cognitive figure: AIOE and Eloundou measure TASK OVERLAP, not displacement
and not timing; top-quintile occupations include likely-augmented work.
"""
import io, json, pathlib, zipfile
import numpy as np
import pandas as pd
from scipy import stats
import importlib.util

ROOT = pathlib.Path(__file__).parents[1]
RAW, OUT = ROOT / "data" / "raw", ROOT / "data" / "processed"
PPART = [("csv_pus.zip", "psam_pusa.csv"), ("csv_pus.zip", "psam_pusb.csv")]
HPART = [("csv_hus.zip", "psam_husa.csv"), ("csv_hus.zip", "psam_husb.csv")]
spec = importlib.util.spec_from_file_location("h3", ROOT / "src" / "h3_geography.py")
h3 = importlib.util.module_from_spec(spec); spec.loader.exec_module(h3)


def chunks(zf, fn, cols, size=300_000):
    z = zipfile.ZipFile(RAW / "pums" / zf)
    with z.open(fn) as fh:
        for ch in pd.read_csv(io.TextIOWrapper(fh, encoding="utf-8", errors="replace"),
                              usecols=cols, dtype={"SERIALNO": str},
                              chunksize=size, low_memory=False):
            yield ch


def main():
    B, groups = h3.build_groups()
    emb = groups["embodied"]
    out = {}

    # ---- person pass, once: household exposure flags, wage, employment, ref age ----
    print("person pass ...")
    parts = []
    for zf, fn in PPART:
        for ch in chunks(zf, fn, ["SERIALNO", "SPORDER", "OCCP", "WAGP", "ADJINC",
                                  "PWGTP", "AGEP", "ESR"]):
            occ = pd.to_numeric(ch["OCCP"], errors="coerce")
            wage = (pd.to_numeric(ch["WAGP"], errors="coerce").fillna(0.0)
                    * pd.to_numeric(ch["ADJINC"], errors="coerce") / 1e6)
            pw = pd.to_numeric(ch["PWGTP"], errors="coerce").fillna(0.0)
            esr = pd.to_numeric(ch["ESR"], errors="coerce")
            d = pd.DataFrame({
                "SERIALNO": ch["SERIALNO"], "wagewt": wage * pw, "wage": wage,
                "employed": esr.isin([1, 2, 4, 5]).astype(int),
                "refage": np.where(pd.to_numeric(ch["SPORDER"], errors="coerce") == 1,
                                   pd.to_numeric(ch["AGEP"], errors="coerce"), np.nan),
                "cA": occ.isin(groups["cognitive_AIOE"]).astype(int),
                "cG": occ.isin(groups["cognitive_GPT"]).astype(int),
                "e": occ.isin(emb).astype(int)})
            parts.append(d.groupby("SERIALNO").agg(
                wagewt=("wagewt", "sum"), wage=("wage", "sum"),
                employed=("employed", "max"), refage=("refage", "max"),
                cA=("cA", "max"), cG=("cG", "max"), e=("e", "max")))
    H = pd.concat(parts).groupby(level=0).agg(
        wagewt=("wagewt", "sum"), wage=("wage", "sum"), employed=("employed", "max"),
        refage=("refage", "max"), cA=("cA", "max"), cG=("cG", "max"), e=("e", "max"))

    # ---- housing pass ----
    print("housing pass ...")
    hp = []
    for zf, fn in HPART:
        for ch in chunks(zf, fn, ["SERIALNO", "WGTP", "TEN", "MRGP", "GRNTP", "ADJHSG"]):
            for c in ["WGTP", "TEN", "MRGP", "GRNTP", "ADJHSG"]:
                ch[c] = pd.to_numeric(ch[c], errors="coerce")
            a = ch["ADJHSG"] / 1e6
            ch["mort"] = np.nan_to_num(np.where(ch["TEN"] == 1, ch["MRGP"] * 12 * a, 0.0))
            ch["rent"] = np.nan_to_num(np.where(ch["TEN"] == 3, ch["GRNTP"] * 12 * a, 0.0))
            hp.append(ch[["SERIALNO", "WGTP", "mort", "rent"]])
    HH = pd.concat(hp, ignore_index=True).join(H, on="SERIALNO")
    for c in ["wagewt", "wage", "employed", "cA", "cG", "e"]:
        HH[c] = HH[c].fillna(0.0)
    HH["WGTP"] = HH["WGTP"].fillna(0.0)
    HH = HH[HH["WGTP"] > 0]
    HH["working_core"] = (HH["employed"] == 1) & HH["refage"].between(25, 64)

    # ---- ITEM 1: five-way table ----
    rows = []
    for cogn, ccol in [("cognitive_AIOE", "cA"), ("cognitive_GPT", "cG")]:
        HH["klass"] = np.select(
            [~HH["working_core"],
             (HH[ccol] == 1) & (HH["e"] == 1),
             (HH[ccol] == 1) & (HH["e"] == 0),
             (HH[ccol] == 0) & (HH["e"] == 1)],
            ["non_working", "both", "cognitive_only", "embodied_only"],
            default="middle_exposure_working")
        tm = float((HH["mort"] * HH["WGTP"]).sum())
        tr = float((HH["rent"] * HH["WGTP"]).sum())
        tw = float(HH["wagewt"].sum()); th = float(HH["WGTP"].sum())
        for k in ["cognitive_only", "embodied_only", "both",
                  "middle_exposure_working", "non_working"]:
            d = HH[HH["klass"] == k]
            w = float(d["wagewt"].sum())
            r = {"cognitive_definition": cogn, "class": k,
                 "households_pct": 100 * float(d["WGTP"].sum()) / th,
                 "wage_bill_pct": 100 * w / tw,
                 "mortgage_service_pct": 100 * float((d["mort"] * d["WGTP"]).sum()) / tm,
                 "rent_pct": 100 * float((d["rent"] * d["WGTP"]).sum()) / tr}
            r["mortgage_lean"] = r["mortgage_service_pct"] / r["wage_bill_pct"] if r["wage_bill_pct"] else np.nan
            r["rent_lean"] = r["rent_pct"] / r["wage_bill_pct"] if r["wage_bill_pct"] else np.nan
            rows.append(r)
    T = pd.DataFrame(rows)
    T.round(3).to_csv(OUT / "shares_fiveway.csv", index=False)

    # ---- ITEM 2: proportionality ----
    W = HH[HH["working_core"] & (HH["wage"] > 0)].copy()
    prop_rows, slope_rows = [], []
    for cogn, ccol in [("cognitive_AIOE", "cA"), ("cognitive_GPT", "cG")]:
        for tname, col in [("cognitive", ccol), ("embodied", "e")]:
            d = W[W[col] == 1]
            for out_lab, ycol in [("mortgage", "mort"), ("rent", "rent")]:
                dd = d[d[ycol] > 0]
                if len(dd) < 50:
                    continue
                # weighted slope through the origin: k = sum(w*y)/sum(w*x)
                k = float((dd[ycol] * dd["WGTP"]).sum()) / float((dd["wage"] * dd["WGTP"]).sum())
                # deciles of wage, slope stability
                q = pd.qcut(dd["wage"], 10, labels=False, duplicates="drop")
                ks = []
                for dq in range(int(q.max()) + 1):
                    s = dd[q == dq]
                    den = float((s["wage"] * s["WGTP"]).sum())
                    if den > 0:
                        ks.append(float((s[ycol] * s["WGTP"]).sum()) / den)
                ks = np.array(ks)
                # OLS slope with intercept, weighted, for the linearity check
                x = dd["wage"].to_numpy(float); y = dd[ycol].to_numpy(float)
                ww = dd["WGTP"].to_numpy(float)
                Xm = np.column_stack([np.ones(len(x)), x]); sw = np.sqrt(ww)
                b, *_ = np.linalg.lstsq(Xm * sw[:, None], y * sw, rcond=None)
                prop_rows.append({
                    "cognitive_definition": cogn, "exposure_type": tname,
                    "outcome": out_lab, "n": int(len(dd)),
                    "k_through_origin": k,
                    "k_decile_min": float(ks.min()), "k_decile_max": float(ks.max()),
                    "k_decile_cv": float(ks.std() / ks.mean()),
                    "ols_intercept": float(b[0]), "ols_slope": float(b[1]),
                    "intercept_share_of_mean_y": float(b[0] / y.mean())})
                for i, kk in enumerate(ks):
                    slope_rows.append({"cognitive_definition": cogn,
                                       "exposure_type": tname, "outcome": out_lab,
                                       "wage_decile": i + 1, "k": kk})
    P = pd.DataFrame(prop_rows)
    P.round(5).to_csv(OUT / "proportionality.csv", index=False)
    pd.DataFrame(slope_rows).round(5).to_csv(OUT / "proportionality_deciles.csv", index=False)

    out["fiveway"] = T.round(4).to_dict("records")
    out["proportionality"] = P.round(5).to_dict("records")
    (OUT / "shares_proportionality_summary.json").write_text(json.dumps(out, indent=2))

    pd.set_option("display.width", 230)
    print("\n=== ITEM 1: five-way shares, restricted to working core where applicable ===")
    for cogn in ["cognitive_AIOE", "cognitive_GPT"]:
        s = T[T["cognitive_definition"] == cogn]
        print(f"\n-- {cogn} --")
        print(s[["class", "households_pct", "wage_bill_pct", "mortgage_service_pct",
                 "rent_pct", "mortgage_lean", "rent_lean"]].round(2).to_string(index=False))
        print(f"   sums: hh {s['households_pct'].sum():.1f}  wage {s['wage_bill_pct'].sum():.1f}"
              f"  mort {s['mortgage_service_pct'].sum():.1f}  rent {s['rent_pct'].sum():.1f}")

    print("\n=== ITEM 2: proportionality, k = debt service per dollar of wage income ===")
    print(P[["cognitive_definition", "exposure_type", "outcome", "n", "k_through_origin",
             "k_decile_min", "k_decile_max", "k_decile_cv",
             "intercept_share_of_mean_y"]].round(4).to_string(index=False))


if __name__ == "__main__":
    main()
