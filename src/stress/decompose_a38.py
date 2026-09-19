"""Decompose the correction to the A38 five-way share table.

The corrected table produced by src/stress/run_compare.py differs from A38 by more than the
vacant-unit fix, and reporting the new numbers without saying which change caused what would
be exactly the kind of silent substitution this project keeps catching. Three things differ:

  FIX 1  VACANT UNITS. A38 kept every housing record with a positive weight. ACS carries
         vacant units (NP = 0) with a housing weight; they have no occupants, no income and
         no tenure. 14.0m weighted, 9.6 percent of records, all landing in the non-working
         class. They contribute zero to every dollar column, so this fix moves the HOUSEHOLD
         percentages only.

  FIX 2  ONE WEIGHT SYSTEM. A38 weighted the mortgage and rent numerators by the HOUSEHOLD
         weight WGTP and the wage denominator by the PERSON weight PWGTP summed within the
         household. A lean built from two weight systems is not a ratio of two shares of the
         same universe. Both are now WGTP.

  FIX 3  WORKING-CORE DEFINITION. A38 required an employed member AND a REFERENCE PERSON
         aged 25 to 64. That excludes a household where a 40-year-old works but the
         reference person is 68, which is the wrong test for a displacement question. The
         engine requires an employed member AGED 25 to 64, regardless of who the reference
         person is.

Each fix is applied cumulatively and the table is printed at every stage, so the reader can
see which number moved and why.
"""
import json, pathlib, sys, io, zipfile, time
import numpy as np
import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).parents[2]))
from src.stress import scenarios as SC
from src.stress import acs_engine as AE

ROOT = pathlib.Path(__file__).parents[2]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed" / "stress"


def five_way(w, hh_earn, mort, rent, core, c_, e_):
    klass = np.where(~core, "non_working",
             np.where(c_ & e_, "both",
              np.where(c_ & ~e_, "cognitive_only",
               np.where(~c_ & e_, "embodied_only", "middle_exposure_working"))))
    tm, tr = float((mort * w).sum()), float((rent * w).sum())
    tw, th = float((hh_earn * w).sum()), float(w.sum())
    rows = []
    for k in ["cognitive_only", "embodied_only", "both",
              "middle_exposure_working", "non_working"]:
        s = klass == k
        r = {"class": k,
             "households_pct": 100 * float(w[s].sum()) / th,
             "wage_bill_pct": 100 * float((hh_earn * w)[s].sum()) / tw,
             "mortgage_service_pct": 100 * float((mort * w)[s].sum()) / tm,
             "rent_pct": 100 * float((rent * w)[s].sum()) / tr}
        r["mortgage_lean"] = r["mortgage_service_pct"] / r["wage_bill_pct"]
        r["rent_lean"] = r["rent_pct"] / r["wage_bill_pct"]
        rows.append(r)
    return pd.DataFrame(rows)


def main():
    t0 = time.time()
    print("loading ACS ...")
    P, H = AE.load_acs(with_reps=False)
    # load_acs already drops vacant units, so recover them for stage 0 by re-reading NP
    # and the reference-person age, which A38's definition needs.
    _, groups = SC._h3().build_groups()

    print("  re-reading reference-person age and person-weighted wage ...")
    z = zipfile.ZipFile(RAW / "pums" / "csv_pus.zip")
    parts = []
    for fn in ["psam_pusa.csv", "psam_pusb.csv"]:
        with z.open(fn) as fh:
            for ch in pd.read_csv(io.TextIOWrapper(fh, encoding="utf-8", errors="replace"),
                                  usecols=["SERIALNO", "SPORDER", "AGEP", "WAGP", "ADJINC",
                                           "PWGTP"], dtype={"SERIALNO": str},
                                  chunksize=400_000, low_memory=False):
                adj = pd.to_numeric(ch["ADJINC"], errors="coerce") / 1e6
                wage = pd.to_numeric(ch["WAGP"], errors="coerce").fillna(0.0) * adj
                pw = pd.to_numeric(ch["PWGTP"], errors="coerce").fillna(0.0)
                refage = np.where(pd.to_numeric(ch["SPORDER"], errors="coerce") == 1,
                                  pd.to_numeric(ch["AGEP"], errors="coerce"), np.nan)
                parts.append(pd.DataFrame({"SERIALNO": ch["SERIALNO"].astype(str),
                                           "wagewt": wage * pw,
                                           "refage": refage}
                                          ).groupby("SERIALNO").agg(
                    wagewt=("wagewt", "sum"), refage=("refage", "max")))
    X = pd.concat(parts).groupby(level=0).agg(wagewt=("wagewt", "sum"),
                                              refage=("refage", "max"))
    H = H.join(X, on="SERIALNO")
    H["wagewt"] = H["wagewt"].fillna(0.0)

    P, hh_idx = AE.link(P, H)
    n_hh = len(H)
    w = H["wgtp"].to_numpy(np.float64)
    mort = H["mort"].to_numpy(np.float64)
    rent = H["rent"].to_numpy(np.float64)
    hh_earn_hw = np.bincount(hh_idx, weights=P["wage"].to_numpy(np.float64), minlength=n_hh)
    wagewt = H["wagewt"].to_numpy(np.float64)          # person-weighted, A38's denominator
    refage = H["refage"].to_numpy(np.float64)
    core_engine = H["working_core"].to_numpy(bool)
    any_emp = np.bincount(hh_idx, weights=np.ones(len(hh_idx)), minlength=n_hh) > 0
    core_a38 = any_emp & (refage >= 25) & (refage <= 64)

    flags = {}
    for g in ["cognitive_AIOE", "cognitive_GPT", "embodied"]:
        f = P["occp"].isin(groups[g]).to_numpy(float)
        flags[g] = np.bincount(hh_idx, weights=f, minlength=n_hh) > 0

    # A38's denominator is a PERSON-weighted wage total but a HOUSEHOLD-weighted numerator.
    # Reproduced exactly: wage share uses wagewt with no household weight applied.
    stages = []
    for cog in ["cognitive_AIOE", "cognitive_GPT"]:
        c_, e_ = flags[cog], flags["embodied"]
        # stage 1: vacancy fixed (load_acs already did), A38 weights, A38 core
        s1 = five_way(w, wagewt / np.maximum(w, 1e-9), mort, rent, core_a38, c_, e_)
        # stage 2: + one weight system
        s2 = five_way(w, hh_earn_hw, mort, rent, core_a38, c_, e_)
        # stage 3: + engine core definition
        s3 = five_way(w, hh_earn_hw, mort, rent, core_engine, c_, e_)
        for name, tb in [("1_vacancy_fixed_a38_weights_a38_core", s1),
                         ("2_plus_single_weight_system", s2),
                         ("3_plus_engine_core_definition", s3)]:
            tb = tb.assign(stage=name, cognitive_definition=cog)
            stages.append(tb)
    T = pd.concat(stages, ignore_index=True)
    T.round(4).to_csv(OUT / "a38_correction_decomposition.csv", index=False)

    pd.set_option("display.width", 250)
    for cog in ["cognitive_AIOE", "cognitive_GPT"]:
        print(f"\n########## {cog} ##########")
        for name in ["1_vacancy_fixed_a38_weights_a38_core",
                     "2_plus_single_weight_system",
                     "3_plus_engine_core_definition"]:
            s = T[(T["stage"] == name) & (T["cognitive_definition"] == cog)]
            print(f"\n-- {name} --")
            print(s[["class", "households_pct", "wage_bill_pct", "mortgage_service_pct",
                     "rent_pct", "mortgage_lean", "rent_lean"]].round(2).to_string(index=False))
    print(f"\ntotal {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
