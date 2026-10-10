"""
Build the pre-shock constructs and test whether bank labour backing carries
variation that loan composition alone does not.

NO OUTCOME VARIABLE IS READ HERE. Every input is dated 2014-06-30 or earlier,
before the oil-price collapse (2014Q4) that is the candidate primary episode.

Bank labour backing:
    LB_bank = [ sum_c  w_c * beta_c ] * wageshare(bank counties)
where w_c is the share of class c in the bank's gross loan-plus-securities book,
beta_c is the class-level direct labour backing coefficient from the labour
backing accounts (framework/labor_backing/claim_class_rules.csv, READ ONLY), and
wageshare is the deposit-weighted wage share of personal income across the
counties in which the bank holds branch deposits (FDIC SOD x BEA CAINC4).

The first bracket is called the composition leg; the second the geography leg.
"""
from pathlib import Path
import numpy as np
import numpy.linalg as la
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "validation"
OUT = ROOT / "framework" / "validation"
PRE_YEAR = "2013"          # pre-shock year for the geography leg

# Class coefficients, read from the labour backing accounts. Read only.
RULES = ROOT / "framework" / "labor_backing" / "claim_class_rules.csv"

# FDIC call-report item -> claim class in the labour backing accounts
CLASS_MAP = {
    "LNRERES":  "home_mortgage",              # 1-4 family, incl. HELOC
    "LNREMULT": "multifamily_mortgage",
    "LNCRCD":   "credit_card",
    "LNAUTO":   "auto_loan",
    "LNCONOTH": "other_consumer",
    "LNRENRES": "commercial_mortgage",        # zero by rule
    "LNRECONS": "commercial_mortgage",        # construction, business revenue
    "LNREAG":   "noncorporate_business_debt", # zero by rule
    "LNAG":     "noncorporate_business_debt",
    "LNCI":     "corporate_loans",            # zero by rule
    "SCMUNI":   "state_local_debt",
    "SCOTHER":  "treasury",                   # securities less munis
}

CONTROLS = ["sh_household", "sh_resre", "sh_consumer", "sh_cre", "sh_constr",
            "sh_ci", "sh_ag", "sh_sec", "tier1_lev", "cre_conc", "log_assets",
            "dep_assets", "brokered", "loans_assets", "geo_wage_share"]

COMPOSITION_BASIS = ["sh_resre", "sh_consumer", "sh_cre", "sh_constr", "sh_ci",
                     "sh_ag", "sh_sec"]


def county_wage_share(year=PRE_YEAR):
    """Wage and salary disbursements over personal income, by county, one year."""
    bea = pd.read_csv(RAW / "bea_cainc4_all_areas.csv", dtype=str)
    bea["GeoFIPS"] = bea["GeoFIPS"].str.strip().str.replace('"', "", regex=False)
    keep = bea[bea["LineCode"].isin(["10", "50", "70", "46", "47"])].copy()
    keep[year] = pd.to_numeric(keep[year], errors="coerce")
    wide = keep.pivot_table(index="GeoFIPS", columns="LineCode",
                            values=year, aggfunc="first")
    wide = wide.rename(columns={"10": "pi", "50": "wages", "70": "prop",
                                "46": "dir", "47": "transfers"})
    wide = wide[wide["pi"] > 0]
    wide["wage_share"] = wide["wages"] / wide["pi"]
    # counties only: drop state (xx000) and national aggregates
    wide = wide[~wide.index.str.endswith("000")]
    return wide


def main():
    rules = pd.read_csv(RULES)
    beta = dict(zip(rules["claim_class"], rules["labour_backing_share"]))

    fin = pd.read_csv(RAW / "fdic_financials_20140630.csv")
    num = [c for c in fin.columns
           if c not in ("NAMEFULL", "STNAME", "ID", "REPDTE")]
    fin[num] = fin[num].apply(pd.to_numeric, errors="coerce")
    fin["SCOTHER"] = (fin["SC"].fillna(0) - fin["SCMUNI"].fillna(0)).clip(lower=0)

    fin["book"] = fin["LNLSGR"].fillna(0) + fin["SC"].fillna(0)
    fin = fin[(fin["book"] > 0) & (fin["ASSET"] > 0)].copy()

    comp = np.zeros(len(fin))
    for item, cls in CLASS_MAP.items():
        comp += fin[item].fillna(0).to_numpy() / fin["book"].to_numpy() * beta[cls]
    fin["lb_composition"] = comp

    # geography leg: deposit-weighted county wage share
    sod = pd.read_csv(RAW / "fdic_sod_2014.csv")
    sod = sod.dropna(subset=["STCNTYBR"])
    sod["fips"] = (sod["STCNTYBR"].astype(float).astype(int)
                   .astype(str).str.zfill(5))
    sod["DEPSUMBR"] = pd.to_numeric(sod["DEPSUMBR"], errors="coerce").fillna(0)
    ws = county_wage_share()
    sod = sod.merge(ws[["wage_share"]], left_on="fips",
                    right_index=True, how="left")
    sod = sod.dropna(subset=["wage_share"])

    def wavg(d):
        w = d["DEPSUMBR"].to_numpy()
        return np.average(d["wage_share"].to_numpy(), weights=w) if w.sum() > 0 \
            else np.nan

    g = sod.groupby("CERT")[["wage_share", "DEPSUMBR"]].apply(wavg)
    fin["geo_wage_share"] = fin["CERT"].map(g)
    fin["n_counties"] = fin["CERT"].map(sod.groupby("CERT")["fips"].nunique())
    fin["lb_bank"] = fin["lb_composition"] * fin["geo_wage_share"]

    # conventional benchmarks
    b = fin["book"]
    fin["sh_resre"] = fin["LNRERES"].fillna(0) / b
    fin["sh_cre"] = (fin["LNRENRES"].fillna(0) + fin["LNREMULT"].fillna(0)) / b
    fin["sh_constr"] = fin["LNRECONS"].fillna(0) / b
    fin["sh_ci"] = fin["LNCI"].fillna(0) / b
    fin["sh_consumer"] = (fin["LNCRCD"].fillna(0) + fin["LNAUTO"].fillna(0)
                          + fin["LNCONOTH"].fillna(0)) / b
    fin["sh_ag"] = (fin["LNAG"].fillna(0) + fin["LNREAG"].fillna(0)) / b
    fin["sh_sec"] = fin["SC"].fillna(0) / b
    # the pure composition rival: household-serviced share of the book
    fin["sh_household"] = fin["sh_resre"] + fin["sh_consumer"]
    fin["tier1_lev"] = fin["RBC1AAJ"]
    fin["cre_conc"] = ((fin["LNRECONS"].fillna(0) + fin["LNRENRES"].fillna(0)
                        + fin["LNREMULT"].fillna(0))
                       / fin["RBCT1J"]).replace([np.inf, -np.inf], np.nan) * 100
    fin["log_assets"] = np.log(fin["ASSET"])
    fin["dep_assets"] = fin["DEP"] / fin["ASSET"]
    fin["brokered"] = fin["BRO"].fillna(0) / fin["DEP"].replace(0, np.nan)
    fin["loans_assets"] = fin["LNLSGR"] / fin["ASSET"]

    panel = fin.dropna(subset=["lb_bank", "tier1_lev"]).copy()

    rows = []
    for c in CONTROLS:
        s = panel[["lb_bank", "lb_composition", c]].dropna()
        rows.append({
            "control": c,
            "n": len(s),
            "corr_with_lb_bank": s["lb_bank"].corr(s[c]),
            "corr_with_composition_leg": s["lb_composition"].corr(s[c]),
        })
    corr = pd.DataFrame(rows).sort_values(
        "corr_with_lb_bank", key=abs, ascending=False)
    corr.to_csv(OUT / "preshock_correlations.csv", index=False)

    # the collinearity verdict: regress labour backing on loan composition alone
    X = panel[COMPOSITION_BASIS].fillna(0).to_numpy()
    X = np.column_stack([np.ones(len(X)), X])
    y = panel["lb_bank"].to_numpy()
    bh, *_ = la.lstsq(X, y, rcond=None)
    r2_full = 1 - ((y - X @ bh) ** 2).sum() / ((y - y.mean()) ** 2).sum()

    yc = panel["lb_composition"].to_numpy()
    bc, *_ = la.lstsq(X, yc, rcond=None)
    r2_leg = 1 - ((yc - X @ bc) ** 2).sum() / ((yc - yc.mean()) ** 2).sum()

    verdict = {
        "n_banks": int(len(panel)),
        "lb_bank_mean": float(panel["lb_bank"].mean()),
        "lb_bank_sd": float(panel["lb_bank"].std()),
        "lb_composition_mean": float(panel["lb_composition"].mean()),
        "lb_composition_sd": float(panel["lb_composition"].std()),
        "geo_wage_share_mean": float(panel["geo_wage_share"].mean()),
        "geo_wage_share_sd": float(panel["geo_wage_share"].std()),
        "R2_lb_bank_on_loan_composition": float(r2_full),
        "R2_composition_leg_on_loan_composition": float(r2_leg),
        "corr_lb_bank_household_share": float(
            panel["lb_bank"].corr(panel["sh_household"])),
        "corr_composition_leg_household_share": float(
            panel["lb_composition"].corr(panel["sh_household"])),
        "residual_sd_after_composition": float(np.std(y - X @ bh)),
        "residual_sd_as_share_of_total_sd": float(
            np.std(y - X @ bh) / panel["lb_bank"].std()),
    }
    pd.Series(verdict).to_json(OUT / "preshock_collinearity.json", indent=2)
    panel[["CERT", "NAMEFULL", "STNAME", "lb_bank", "lb_composition",
           "geo_wage_share", "n_counties"] + CONTROLS].to_csv(
        RAW / "preshock_panel_2014.csv", index=False)

    print(corr.to_string(index=False))
    print()
    for k, v in verdict.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
