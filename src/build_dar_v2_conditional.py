"""Is the PAEI housing-burden gradient a PAEI effect or an income effect?

build_dar_v2.py finds housing obligation to wage income rising monotonically across PAEI
quintiles (combined: 15.7 percent at q1 to 27.9 percent at q5). That gradient cannot be
reported as a Physical AI result until it is separated from a much more ordinary fact:
housing costs are less than proportional to income, so housing burden falls with income
for reasons that have nothing to do with automation. PAEI correlates negatively with
wages, so an income effect alone would produce exactly this gradient.

Test: stratify households into income deciles, then compute the housing burden by PAEI
quintile WITHIN each decile. If the gradient survives within income bands it is a PAEI
effect. If it collapses or reverses, the raw gradient is an income-composition artifact.

Direct standardisation holds the income composition fixed at the overall distribution and
reports the residual PAEI gradient.

Two denominators are run. Wage income is the thesis-relevant one (it is the income
Physical AI threatens) but is a poor denominator at the bottom, where transfers and
self-employment dominate and burden ratios exceed 100 percent. Total household income is
the robustness check.
"""
import io, json, pathlib, zipfile
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).parents[1]
RAW, OUT = ROOT / "data" / "raw", ROOT / "data" / "processed"

PPART = [("csv_pus.zip", "psam_pusa.csv"), ("csv_pus.zip", "psam_pusb.csv")]
HPART = [("csv_hus.zip", "psam_husa.csv"), ("csv_hus.zip", "psam_husb.csv")]
PCOLS = ["SERIALNO", "OCCP", "WAGP", "ADJINC"]
HCOLS = ["SERIALNO", "WGTP", "TEN", "MRGP", "MRGT", "MRGI", "GRNTP", "ADJHSG", "HINCP"]


def read_part(zf, fn, cols):
    z = zipfile.ZipFile(RAW / "pums" / zf)
    with z.open(fn) as fh:
        return pd.concat(list(pd.read_csv(
            io.TextIOWrapper(fh, encoding="utf-8", errors="replace"),
            usecols=cols, dtype={"SERIALNO": str}, chunksize=400_000, low_memory=False)),
            ignore_index=True)


def wq(v, w, qs):
    o = np.argsort(v)
    v, w = np.asarray(v)[o], np.asarray(w)[o]
    return np.interp(qs, np.cumsum(w) / w.sum(), v)


def run(D, denom, label, out_csv):
    """Stratify on `denom` deciles, report housing burden by PAEI quintile within each."""
    D = D[D[denom] > 0].copy()
    pc = wq(D["paei_ew"].to_numpy(), D["WGTP"].to_numpy(), [.2, .4, .6, .8])
    D["pq"] = np.digitize(D["paei_ew"].to_numpy(), pc) + 1
    ic = wq(D[denom].to_numpy(), D["WGTP"].to_numpy(), np.arange(.1, 1.0, .1))
    D["idec"] = np.digitize(D[denom].to_numpy(), ic) + 1

    def burden(d):
        den = float((d[denom] * d["WGTP"]).sum())
        return 100 * float((d["housing"] * d["WGTP"]).sum()) / den if den else np.nan

    uncond = {f"q{q}": burden(D[D["pq"] == q]) for q in range(1, 6)}

    rows = []
    for dec in range(1, 11):
        s = D[D["idec"] == dec]
        r = {"income_decile": dec, "median_income_usd": float(np.median(s[denom])),
             "households_weighted": float(s["WGTP"].sum())}
        for q in range(1, 6):
            sq = s[s["pq"] == q]
            r[f"q{q}"] = burden(sq) if len(sq) else np.nan
        r["q5_minus_q1"] = r["q5"] - r["q1"]
        rows.append(r)
    W = pd.DataFrame(rows)

    wts = W["households_weighted"] / W["households_weighted"].sum()
    std = {f"q{q}": float(np.nansum(W[f"q{q}"] * wts)) for q in range(1, 6)}
    W.round(3).to_csv(out_csv, index=False)

    res = {"denominator": label,
           "unconditional_pct": uncond,
           "unconditional_gap_pp": uncond["q5"] - uncond["q1"],
           "standardised_pct": std,
           "standardised_gap_pp": std["q5"] - std["q1"],
           "deciles_with_positive_gap": int((W["q5_minus_q1"] > 0).sum())}

    print(f"\n########## denominator: {label} ##########")
    print("unconditional: " + "  ".join(f"{k}={v:.2f}%" for k, v in uncond.items()))
    print(f"  raw gap q5-q1: {res['unconditional_gap_pp']:+.2f} pp")
    print(W[["income_decile", "median_income_usd", "q1", "q3", "q5",
             "q5_minus_q1"]].round(2).to_string(index=False))
    print("income-standardised: " + "  ".join(f"{k}={v:.2f}%" for k, v in std.items()))
    print(f"  standardised gap q5-q1: {res['standardised_gap_pp']:+.2f} pp")
    print(f"  deciles with a positive gap: {res['deciles_with_positive_gap']} of 10")
    return res


def main():
    occ = pd.read_csv(OUT / "occp_to_paei.csv")
    P = pd.concat([read_part(z, f, PCOLS) for z, f in PPART], ignore_index=True)
    P["OCCP"] = pd.to_numeric(P["OCCP"], errors="coerce")
    P["adjinc"] = pd.to_numeric(P["ADJINC"], errors="coerce") / 1e6
    P["wage"] = pd.to_numeric(P["WAGP"], errors="coerce").fillna(0.0) * P["adjinc"]
    P = P.merge(occ[["occp", "PAEI"]], left_on="OCCP", right_on="occp", how="left")

    e = P[(P["wage"] > 0) & P["PAEI"].notna()].copy()
    e["num"] = e["PAEI"] * e["wage"]
    g = e.groupby("SERIALNO").agg(num=("num", "sum"), den=("wage", "sum"))
    hh = pd.DataFrame({"paei_ew": g["num"] / g["den"], "hh_wage": g["den"]})
    adj_by_hh = P.groupby("SERIALNO")["adjinc"].first()

    H = pd.concat([read_part(z, f, HCOLS) for z, f in HPART], ignore_index=True)
    for c in ["WGTP", "TEN", "MRGP", "GRNTP", "ADJHSG", "MRGT", "MRGI", "HINCP"]:
        H[c] = pd.to_numeric(H[c], errors="coerce")
    H = H.merge(hh, left_on="SERIALNO", right_index=True, how="left")
    a = H["ADJHSG"] / 1e6
    H["mortgage"] = np.where(H["TEN"] == 1, H["MRGP"] * 12 * a, np.nan)
    H["rent"] = np.where(H["TEN"] == 3, H["GRNTP"] * 12 * a, np.nan)
    H["housing"] = H[["mortgage", "rent"]].sum(axis=1, min_count=1)
    H["hh_inc"] = H["HINCP"] * H["SERIALNO"].map(adj_by_hh)

    D = H[H["paei_ew"].notna() & (H["hh_wage"] > 0)
          & H["housing"].notna() & (H["housing"] > 0)].copy()

    r_wage = run(D, "hh_wage", "household wage income", OUT / "dar_v2_conditional.csv")
    r_inc = run(D, "hh_inc", "total household income",
                OUT / "dar_v2_conditional_hhinc.csv")
    (OUT / "dar_v2_conditional_summary.json").write_text(
        json.dumps({"wage_denominator": r_wage, "total_income_denominator": r_inc},
                   indent=2))

    print("\n=== VERDICT ===")
    for r in (r_wage, r_inc):
        surv = 100 * r["standardised_gap_pp"] / r["unconditional_gap_pp"]
        print(f"  {r['denominator']:24s}: raw {r['unconditional_gap_pp']:+.2f} pp -> "
              f"standardised {r['standardised_gap_pp']:+.2f} pp "
              f"({surv:.0f}% of raw survives)")


if __name__ == "__main__":
    main()
