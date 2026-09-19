"""A1: reconcile PAEI coverage, and test whether what is lost is systematically different.

Two separate losses, which have to be diagnosed separately because only one of them is
testable on P and S.

  LOSS 1  PUMS employment whose OCCP code does not reach a PAEI occupation.
          P and S are unknown for these by construction, so they cannot be compared on
          P or S. They are characterised by SOC major group and employment instead.

  LOSS 2  PAEI occupations that carry no PUMS employment.
          P and S ARE known for these, so the systematic-difference test is run here.

Separately, PUMS covered wage bill is reconciled against NIPA wages and salaries (WASCUR),
which is a different and larger gap driven by survey undercount and top-coding, not by the
crosswalk.
"""
import io, json, pathlib, zipfile
import numpy as np
import pandas as pd
from scipy import stats

ROOT = pathlib.Path(__file__).parents[1]
RAW, OUT = ROOT / "data" / "raw", ROOT / "data" / "processed"

MAJOR = {
    "11": "Management", "13": "Business and Financial", "15": "Computer and Math",
    "17": "Architecture and Engineering", "19": "Life, Physical, Social Science",
    "21": "Community and Social Service", "23": "Legal", "25": "Education",
    "27": "Arts, Design, Entertainment, Media", "29": "Healthcare Practitioners",
    "31": "Healthcare Support", "33": "Protective Service", "35": "Food Preparation",
    "37": "Building and Grounds Cleaning", "39": "Personal Care", "41": "Sales",
    "43": "Office and Administrative", "45": "Farming, Fishing, Forestry",
    "47": "Construction and Extraction", "49": "Installation, Maintenance, Repair",
    "51": "Production", "53": "Transportation and Material Moving",
    "55": "Military",
}


def load_pums():
    frames = []
    z = zipfile.ZipFile(RAW / "pums" / "csv_pus.zip")
    for fn in ["psam_pusa.csv", "psam_pusb.csv"]:
        with z.open(fn) as fh:
            for ch in pd.read_csv(io.TextIOWrapper(fh, encoding="utf-8", errors="replace"),
                                  usecols=["OCCP", "PWGTP", "WAGP", "ADJINC"],
                                  chunksize=500_000, low_memory=False):
                frames.append(ch)
    P = pd.concat(frames, ignore_index=True)
    P["OCCP"] = pd.to_numeric(P["OCCP"], errors="coerce")
    P["PWGTP"] = pd.to_numeric(P["PWGTP"], errors="coerce").fillna(0.0)
    P["wage"] = (pd.to_numeric(P["WAGP"], errors="coerce").fillna(0.0)
                 * pd.to_numeric(P["ADJINC"], errors="coerce") / 1e6)
    return P.dropna(subset=["OCCP"])


def wmean(x, w):
    x = np.asarray(x, float); w = np.asarray(w, float)
    m = np.isfinite(x) & np.isfinite(w)
    return float(np.average(x[m], weights=w[m])) if m.sum() else np.nan


def main():
    paei = pd.read_csv(OUT / "paei_onet.csv")
    paei["soc"] = paei["onet_soc"].astype(str).str[:7]
    soc = (paei.groupby("soc")
           .agg(title=("title", "first"), P=("embodiment_P", "mean"),
                S=("structure_S", "mean")).reset_index())
    cw = pd.read_csv(OUT / "occp_to_paei.csv")

    P = load_pums()
    steps = []
    tot_emp = P["PWGTP"].sum()
    tot_wage = (P["wage"] * P["PWGTP"]).sum()
    steps.append({"step": "0. PUMS persons with an OCCP code",
                  "occupations": int(P["OCCP"].nunique()),
                  "employment": tot_emp, "wage_bill_usd_bn": tot_wage / 1e9})

    # employed = positive person weight; PUMS OCCP is populated for the employed and
    # recently employed, so restrict to positive wage for the wage-bill reconciliation
    Pm = P.merge(cw[["occp", "soc", "matched"]], left_on="OCCP", right_on="occp", how="left")

    in_cw = Pm["soc"].notna()
    steps.append({"step": "1. OCCP present in the Census 2018 OCCP-to-SOC crosswalk",
                  "occupations": int(Pm.loc[in_cw, "OCCP"].nunique()),
                  "employment": Pm.loc[in_cw, "PWGTP"].sum(),
                  "wage_bill_usd_bn": (Pm.loc[in_cw, "wage"] * Pm.loc[in_cw, "PWGTP"]).sum() / 1e9})

    has_paei = in_cw & Pm["soc"].isin(soc["soc"])
    steps.append({"step": "2. SOC also present in PAEI (O*NET 31.0)",
                  "occupations": int(Pm.loc[has_paei, "soc"].nunique()),
                  "employment": Pm.loc[has_paei, "PWGTP"].sum(),
                  "wage_bill_usd_bn": (Pm.loc[has_paei, "wage"] * Pm.loc[has_paei, "PWGTP"]).sum() / 1e9})

    pos = has_paei & (Pm["wage"] > 0)
    steps.append({"step": "3. and positive wage income (the Step 2 analysis frame)",
                  "occupations": int(Pm.loc[pos, "soc"].nunique()),
                  "employment": Pm.loc[pos, "PWGTP"].sum(),
                  "wage_bill_usd_bn": (Pm.loc[pos, "wage"] * Pm.loc[pos, "PWGTP"]).sum() / 1e9})

    T = pd.DataFrame(steps)
    T["employment_pct_of_start"] = 100 * T["employment"] / tot_emp
    T["wage_pct_of_start"] = 100 * T["wage_bill_usd_bn"] / (tot_wage / 1e9)
    T["employment_lost"] = -T["employment"].diff()
    T["wage_lost_usd_bn"] = -T["wage_bill_usd_bn"].diff()
    T.round(2).to_csv(OUT / "coverage_reconciliation.csv", index=False)

    # ---- LOSS 1: unmatched employment, characterised by SOC major group ----
    unm = Pm[~has_paei].copy()
    unm["major"] = np.where(unm["soc"].notna(), unm["soc"].astype(str).str[:2], "unmapped")
    l1 = (unm.groupby("major")
          .apply(lambda d: pd.Series({"employment": d["PWGTP"].sum(),
                                      "wage_bill_usd_bn": (d["wage"] * d["PWGTP"]).sum() / 1e9}),
                 include_groups=False)
          .sort_values("employment", ascending=False).reset_index())
    l1["group"] = l1["major"].map(MAJOR).fillna(l1["major"])
    l1["pct_of_unmatched_employment"] = 100 * l1["employment"] / l1["employment"].sum()
    l1.round(3).to_csv(OUT / "coverage_loss1_unmatched_by_major.csv", index=False)

    # ---- LOSS 2: PAEI occupations with no PUMS employment. P/S testable ----
    emp_by_soc = (Pm[pos].groupby("soc")["PWGTP"].sum().rename("employment"))
    sc = soc.merge(emp_by_soc, on="soc", how="left")
    sc["covered"] = sc["employment"].notna() & (sc["employment"] > 0)
    cov, unc = sc[sc["covered"]], sc[~sc["covered"]]

    tests = {}
    for col in ["P", "S"]:
        t = stats.ttest_ind(cov[col], unc[col], equal_var=False)
        u = stats.mannwhitneyu(cov[col], unc[col], alternative="two-sided")
        tests[col] = {
            "mean_covered": float(cov[col].mean()),
            "mean_uncovered": float(unc[col].mean()),
            "difference": float(cov[col].mean() - unc[col].mean()),
            "employment_weighted_mean_covered": wmean(cov[col], cov["employment"]),
            "welch_t": float(t.statistic), "welch_p": float(t.pvalue),
            "mannwhitney_p": float(u.pvalue),
            "cohens_d": float((cov[col].mean() - unc[col].mean())
                              / np.sqrt((cov[col].var() + unc[col].var()) / 2)),
        }

    # ---- bound the bias: reweight uncovered occupations to the covered employment
    # distribution is impossible (no employment). Instead bound: assume uncovered
    # occupations carry employment proportional to the covered mean, and recompute the
    # employment-weighted mean P and S.
    mean_emp = cov["employment"].mean()
    allsoc = sc.copy()
    allsoc["emp_bound"] = allsoc["employment"].fillna(mean_emp)
    bound = {
        "empwt_mean_P_covered_only": wmean(cov["P"], cov["employment"]),
        "empwt_mean_P_bounded": wmean(allsoc["P"], allsoc["emp_bound"]),
        "empwt_mean_S_covered_only": wmean(cov["S"], cov["employment"]),
        "empwt_mean_S_bounded": wmean(allsoc["S"], allsoc["emp_bound"]),
    }

    # ---- NIPA reconciliation ----
    man = json.loads((RAW / "fred" / "_manifest.json").read_text())
    w = json.loads((OUT / "legW_us_derived.json").read_text())
    nipa = w["wage_bill_usd_bn"]
    covered_wage = float(T.loc[T.index[-1], "wage_bill_usd_bn"])
    nipa_rec = {
        "nipa_wages_and_salaries_usd_bn": nipa,
        "nipa_series": "WASCUR",
        "nipa_note": man["WASCUR"]["title"],
        "pums_total_wage_bill_usd_bn": float(tot_wage / 1e9),
        "pums_covered_wage_bill_usd_bn": covered_wage,
        "pums_total_as_pct_of_nipa": 100 * float(tot_wage / 1e9) / nipa,
        "covered_as_pct_of_nipa": 100 * covered_wage / nipa,
        "gap_from_crosswalk_usd_bn": float(tot_wage / 1e9) - covered_wage,
        "gap_from_pums_vs_nipa_usd_bn": nipa - float(tot_wage / 1e9),
    }

    res = {"steps": T.round(3).to_dict("records"),
           "loss2_systematic_difference_tests": tests,
           "loss2_bias_bound": bound,
           "nipa_reconciliation": nipa_rec,
           "n_paei_soc": int(len(sc)), "n_covered": int(cov.shape[0]),
           "n_uncovered": int(unc.shape[0])}
    (OUT / "coverage_reconciliation.json").write_text(json.dumps(res, indent=2))

    pd.set_option("display.width", 200)
    print("\n=== A1 coverage waterfall ===")
    print(T[["step", "occupations", "employment", "wage_bill_usd_bn",
             "employment_pct_of_start", "wage_pct_of_start"]]
          .round(2).to_string(index=False, max_colwidth=52))

    print("\n=== LOSS 1: unmatched employment by SOC major group (top 10) ===")
    print(l1.head(10)[["group", "employment", "wage_bill_usd_bn",
                       "pct_of_unmatched_employment"]].round(2).to_string(index=False))

    print(f"\n=== LOSS 2: {len(unc)} PAEI occupations with no PUMS employment ===")
    for col, t in tests.items():
        print(f"  {col}: covered mean {t['mean_covered']:.4f}, "
              f"uncovered mean {t['mean_uncovered']:.4f}, "
              f"diff {t['difference']:+.4f}, d = {t['cohens_d']:+.3f}, "
              f"Welch p = {t['welch_p']:.2e}, MW p = {t['mannwhitney_p']:.2e}")
    print("\n  bias bound (assign uncovered occupations the mean covered employment):")
    for k, v in bound.items():
        print(f"    {k:38s} {v:.4f}")

    print("\n=== NIPA reconciliation ===")
    for k, v in nipa_rec.items():
        print(f"  {k:38s} {v if isinstance(v, str) else round(v, 2)}")


if __name__ == "__main__":
    main()
