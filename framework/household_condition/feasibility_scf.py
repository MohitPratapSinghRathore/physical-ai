"""
Feasibility only. Documents the SCF structure, variable availability, sample
sizes and the replicate-weight design for the household condition exercise.

THIS COMPUTES NO RESULT OF THE EXERCISE. It reports counts and coverage so the
specification can be written against known data, and stops there. No shift is
applied, no boundary is computed.
"""
from pathlib import Path
import io
import json
import zipfile
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "household_condition"
OUT = ROOT / "framework" / "household_condition"

INCOME = ["income", "wageinc", "bussefarminc", "intdivinc", "kginc",
          "ssretinc", "transfothinc", "norminc", "equitinc"]
DEBT = ["debt", "mrthel", "nh_mort", "homeeq", "othloc", "resdbt", "ccbal",
        "veh_inst", "edn_inst", "install", "odebt"]
PAYMENT = ["tpay", "mortpay", "conspay", "revpay", "pirtotal", "pirmort",
           "pircons", "pirrev", "pir40", "debt2inc"]
EQUITY = ["equity", "stocks", "nmmf", "irakh", "thrift", "retqliq", "annuit",
          "savbnd", "deq", "bus", "actbus", "nonactbus", "farmbus", "kgbus"]
LIQUID = ["liq", "checking", "saving", "mmda", "call", "cds"]
DISTRESS = ["late", "late60", "bnkruplast5", "hpstppay", "forecloselast5"]


def load(year, kind="p"):
    f = RAW / (f"scf{kind}{year}s.zip")
    z = zipfile.ZipFile(f)
    name = z.namelist()[0]
    return pd.read_stata(io.BytesIO(z.read(name)))


def main():
    rep = {}
    for yr in (2022, 2019):
        df = load(yr)
        cols = set(df.columns)
        rep[str(yr)] = {
            "rows": int(len(df)),
            "households": int(df["yy1"].nunique()),
            "implicates": int(len(df) / df["yy1"].nunique()),
            "variables_total": int(df.shape[1]),
            "present": {g: [c for c in lst if c in cols] for g, lst in
                        [("income", INCOME), ("debt", DEBT),
                         ("payment", PAYMENT), ("equity", EQUITY),
                         ("liquid", LIQUID), ("distress", DISTRESS)]},
            "absent": {g: [c for c in lst if c not in cols] for g, lst in
                       [("income", INCOME), ("debt", DEBT),
                        ("payment", PAYMENT), ("equity", EQUITY),
                        ("liquid", LIQUID), ("distress", DISTRESS)]},
        }
        rep[str(yr)]["weighted_households_m"] = round(
            float(df["wgt"].sum() / 1e6), 2)
        print(f"SCF {yr}: {len(df)} rows = {df['yy1'].nunique()} households "
              f"x {len(df)//df['yy1'].nunique()} implicates, "
              f"{df.shape[1]} variables")

    df = load(2022)
    # SCF summary-extract WGT is scaled so that the sum over ALL FIVE implicates
    # equals the household count (131.31m in 2022). Aggregates therefore use all
    # rows with WGT as-is; a single implicate carries one fifth of the weight.
    i1 = df[df["y1"] % 10 == 1].copy()      # first implicate, unweighted counts
    i1["wgt5"] = i1["wgt"] * 5              # rescaled to household units

    # sample sizes for INDEBTED households, by wage and wealth group.
    # Groups are WEIGHTED percentiles: the SCF oversamples the wealthy, so
    # unweighted ranks would put almost no households in the top groups.
    i1["has_debt"] = i1["debt"] > 0

    def wq(x, w, cuts):
        o = np.argsort(x.to_numpy())
        cw = np.cumsum(w.to_numpy()[o]) / w.sum()
        pct = pd.Series(np.empty(len(x)), index=x.index)
        pct.iloc[o] = cw
        return pd.cut(pct, cuts["edges"], labels=cuts["labels"],
                      include_lowest=True)

    i1["wage_q"] = wq(i1["wageinc"], i1["wgt5"],
                      {"edges": [0, .2, .4, .6, .8, 1.0],
                       "labels": [1, 2, 3, 4, 5]})
    i1["wealth_grp"] = wq(i1["networth"], i1["wgt5"],
                          {"edges": [0, .25, .50, .75, .90, .99, 1.0],
                           "labels": ["p0-25", "p25-50", "p50-75", "p75-90",
                                      "p90-99", "top1"]})

    counts = {}
    t = i1.groupby("wage_q", observed=True).agg(
        n=("has_debt", "size"), n_indebted=("has_debt", "sum"))
    t["wtd_households_m"] = (i1[i1["has_debt"]].groupby("wage_q",
                             observed=True)["wgt5"].sum() / 1e6).round(2)
    counts["by_wage_quintile"] = t.to_dict("index")
    t2 = i1.groupby("wealth_grp", observed=True).agg(
        n=("has_debt", "size"), n_indebted=("has_debt", "sum"))
    t2["wtd_households_m"] = (i1[i1["has_debt"]].groupby("wealth_grp",
                              observed=True)["wgt5"].sum() / 1e6).round(2)
    counts["by_wealth_group"] = t2.to_dict("index")

    # unweighted counts holding each debt class
    cls = {}
    for c in ["mrthel", "homeeq", "veh_inst", "edn_inst", "ccbal", "odebt",
              "install", "othloc"]:
        if c in i1.columns:
            cls[c] = {"n_holding": int((i1[c] > 0).sum()),
                      "wtd_households_m": round(
                          float(i1.loc[i1[c] > 0, "wgt5"].sum() / 1e6), 2)}
    counts["by_debt_class"] = cls

    # aggregate totals for the reconciliation step (levels only, no exercise)
    agg = {}
    for c in ["debt", "mrthel", "ccbal", "veh_inst", "edn_inst", "equity",
              "stocks", "retqliq", "bus", "income", "wageinc"]:
        if c in df.columns:
            # x5 because a single implicate holds one fifth of the weight
            per_imp = [float((df.loc[df["y1"] % 10 == k, c]
                              * df.loc[df["y1"] % 10 == k, "wgt"]).sum()
                             * 5 / 1e9) for k in range(1, 6)]
            agg[c] = {"mean_bn": round(float(np.mean(per_imp)), 1),
                      "implicate_range_bn": [round(min(per_imp), 1),
                                             round(max(per_imp), 1)]}
    rep["aggregates_2022_bn"] = agg
    rep["sample_sizes_2022"] = counts

    # replicate weights
    zrw = zipfile.ZipFile(RAW / "scf2022rw1s.zip")
    rw = pd.read_stata(io.BytesIO(zrw.read(zrw.namelist()[0])))
    rwcols = [c for c in rw.columns if c.lower().startswith("wt1b")]
    rep["replicate_weights"] = {
        "file": zrw.namelist()[0],
        "rows": int(len(rw)),
        "columns": int(rw.shape[1]),
        "replicate_columns": len(rwcols),
        "first_five": rwcols[:5],
        "id_columns": [c for c in rw.columns if c.lower() in ("yy1", "y1")],
    }
    print(f"\nreplicate weights: {len(rw)} rows, {len(rwcols)} replicates")
    print(f"indebted households (first implicate): "
          f"{int(i1['has_debt'].sum())} of {len(i1)}")

    (OUT / "feasibility_scf.json").write_text(
        json.dumps(rep, indent=2, default=str), encoding="utf-8")
    print("\nwritten: feasibility_scf.json")


if __name__ == "__main__":
    main()
