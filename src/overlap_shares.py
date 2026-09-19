"""Items 2 and 3: raw dollar shares by exposure combination, summing to 100 percent.

Four mutually exclusive household groups: cognitive only, embodied only, BOTH exposed,
neither. Shares of national mortgage debt service, rent, and wage bill. Reported for both
cognitive definitions (Felten AIOE and Eloundou GPT) side by side.

HEADLINE RULE (item 3): raw dollar shares are the headline for every stability claim.
Regression-adjusted coefficients answer a different question (does exposure predict debt
holding for otherwise-similar households) and are secondary.

CAVEAT on every cognitive figure: AIOE and Eloundou measure TASK OVERLAP, not displacement
and not timing; top-quintile occupations include likely-augmented work.
"""
import io, json, pathlib, zipfile
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).parents[1]
RAW, OUT = ROOT / "data" / "raw", ROOT / "data" / "processed"
PPART = [("csv_pus.zip", "psam_pusa.csv"), ("csv_pus.zip", "psam_pusb.csv")]
HPART = [("csv_hus.zip", "psam_husa.csv"), ("csv_hus.zip", "psam_husb.csv")]
import importlib.util
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
    results = {}

    for cogname in ("cognitive_AIOE", "cognitive_GPT"):
        cog = groups[cogname]
        print(f"\n########## {cogname} ##########")
        # person pass: which households contain which exposure, and wage by class
        parts = []
        for zf, fn in PPART:
            for ch in chunks(zf, fn, ["SERIALNO", "OCCP", "WAGP", "ADJINC", "PWGTP"]):
                occ = pd.to_numeric(ch["OCCP"], errors="coerce")
                wage = (pd.to_numeric(ch["WAGP"], errors="coerce").fillna(0.0)
                        * pd.to_numeric(ch["ADJINC"], errors="coerce") / 1e6)
                pw = pd.to_numeric(ch["PWGTP"], errors="coerce").fillna(0.0)
                d = pd.DataFrame({"SERIALNO": ch["SERIALNO"],
                                  "wagewt": wage * pw,
                                  "c": occ.isin(cog).astype(int),
                                  "e": occ.isin(emb).astype(int)})
                d = d[(d["wagewt"] > 0) | (d["c"] + d["e"] > 0)]
                parts.append(d.groupby("SERIALNO").agg(
                    wagewt=("wagewt", "sum"), c=("c", "max"), e=("e", "max")))
        H = pd.concat(parts).groupby(level=0).agg(
            wagewt=("wagewt", "sum"), c=("c", "max"), e=("e", "max"))
        H["klass"] = np.select(
            [(H["c"] == 1) & (H["e"] == 1), (H["c"] == 1) & (H["e"] == 0),
             (H["c"] == 0) & (H["e"] == 1)],
            ["both", "cognitive_only", "embodied_only"], default="neither")

        # housing pass
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
        HH["klass"] = HH["klass"].fillna("neither")
        HH["WGTP"] = HH["WGTP"].fillna(0.0)
        HH["wagewt"] = HH["wagewt"].fillna(0.0)

        tm = float((HH["mort"] * HH["WGTP"]).sum())
        tr = float((HH["rent"] * HH["WGTP"]).sum())
        tw = float(HH["wagewt"].sum())
        th = float(HH["WGTP"].sum())
        rows = []
        for k in ["cognitive_only", "embodied_only", "both", "neither"]:
            d = HH[HH["klass"] == k]
            rows.append({
                "cognitive_definition": cogname, "class": k,
                "households_pct": 100 * float(d["WGTP"].sum()) / th,
                "wage_bill_pct": 100 * float(d["wagewt"].sum()) / tw,
                "mortgage_service_pct": 100 * float((d["mort"] * d["WGTP"]).sum()) / tm,
                "rent_pct": 100 * float((d["rent"] * d["WGTP"]).sum()) / tr})
        T = pd.DataFrame(rows)
        T["mortgage_lean_vs_wage"] = T["mortgage_service_pct"] / T["wage_bill_pct"]
        T["rent_lean_vs_wage"] = T["rent_pct"] / T["wage_bill_pct"]
        results[cogname] = T.round(3).to_dict("records")
        pd.set_option("display.width", 220)
        print(T.round(2).to_string(index=False))
        print(f"  sums: households {T['households_pct'].sum():.1f}, "
              f"wage {T['wage_bill_pct'].sum():.1f}, "
              f"mortgage {T['mortgage_service_pct'].sum():.1f}, "
              f"rent {T['rent_pct'].sum():.1f}")

    pd.DataFrame([r for v in results.values() for r in v]).to_csv(
        OUT / "overlap_shares.csv", index=False)
    (OUT / "overlap_shares.json").write_text(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
