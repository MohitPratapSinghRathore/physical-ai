"""
Amendment 1, second half: the bank-level DEBTOR-SPECIFIC labour backing measure,
and the test of whether it has content the rival construct lacks.

    LB_debtor = sum_c  w_c * beta_c * wageshare_debtor(c, bank counties)

where the debtor-specific local wage share is matched to the class:
    residential (1-4 family, multifamily)  -> mortgage-holder wage share
    consumer (card, auto, other)           -> all-household wage share
    business classes                       -> zero by rule, unchanged

against the rival, which uses the population-wide county wage share everywhere:

    LB_rival = [ sum_c w_c * beta_c ] * wageshare_population(bank counties)

If the rival explains more than about 90 percent of the debtor-specific measure,
the refinement has no distinctive content either and the pilot proceeds as a test
of local labour exposure only. That verdict is reported first.

No outcome variable is read here.
"""
from pathlib import Path
import numpy as np
import numpy.linalg as la
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "validation"
OUT = ROOT / "framework" / "validation"

RULES = ROOT / "framework" / "labor_backing" / "claim_class_rules.csv"

# class -> (call report items, which debtor group's wage share applies)
CLASS_ITEMS = {
    "home_mortgage":        (["LNRERES"], "mortgage"),
    "multifamily_mortgage": (["LNREMULT"], "renter"),
    "credit_card":          (["LNCRCD"], "all"),
    "auto_loan":            (["LNAUTO"], "all"),
    "other_consumer":       (["LNCONOTH"], "all"),
    "state_local_debt":     (["SCMUNI"], "all"),
    "treasury":             (["SCOTHER"], "all"),
}
ZERO_ITEMS = ["LNRENRES", "LNRECONS", "LNREAG", "LNAG", "LNCI"]


def r2(y, X):
    X = np.column_stack([np.ones(len(X)), X])
    bh, *_ = la.lstsq(X, y, rcond=None)
    return 1 - ((y - X @ bh) ** 2).sum() / ((y - y.mean()) ** 2).sum()


def main():
    beta = dict(zip(*pd.read_csv(RULES)[["claim_class",
                                         "labour_backing_share"]].values.T))
    beta = {k: float(v) for k, v in beta.items()}

    fin = pd.read_csv(RAW / "fdic_financials_20140630.csv")
    num = [c for c in fin.columns
           if c not in ("NAMEFULL", "STNAME", "ID", "REPDTE")]
    fin[num] = fin[num].apply(pd.to_numeric, errors="coerce")
    fin["SCOTHER"] = (fin["SC"].fillna(0) - fin["SCMUNI"].fillna(0)).clip(lower=0)
    fin["book"] = fin["LNLSGR"].fillna(0) + fin["SC"].fillna(0)
    fin = fin[(fin["book"] > 0) & (fin["ASSET"] > 0)].copy()

    # ---- county wage shares: debtor-specific and population-wide ---------
    cw = pd.read_csv(OUT / "county_debtor_wage_shares_2013.csv",
                     dtype={"county_fips": str})
    debtor = {g: d.set_index("county_fips")["wage_share"]
              for g, d in cw.groupby("group")}
    # Payment-weighted variant exists only for the tenure groups that have a
    # payment (mortgage service, gross rent). For the all-household group it is
    # undefined and the aggregation writes 0.0; treat non-positive as missing so
    # those classes fall back to the household-weighted share rather than zero.
    debtor_pw = {}
    for g, d in cw.groupby("group"):
        s = d.set_index("county_fips")["wage_share_payment_wtd"]
        debtor_pw[g] = s.where(s > 0)

    pop = pd.read_csv(RAW / "bea_cainc4_all_areas.csv", dtype=str)
    pop["GeoFIPS"] = pop["GeoFIPS"].str.strip().str.replace('"', "", regex=False)
    k = pop[pop["LineCode"].isin(["10", "50"])].copy()
    k["2013"] = pd.to_numeric(k["2013"], errors="coerce")
    w = k.pivot_table(index="GeoFIPS", columns="LineCode", values="2013",
                      aggfunc="first")
    w = w[w["10"] > 0]
    pop_share = (w["50"] / w["10"])
    pop_share = pop_share[~pop_share.index.str.endswith("000")]

    # ---- deposit weights --------------------------------------------------
    sod = pd.read_csv(RAW / "fdic_sod_2014.csv").dropna(subset=["STCNTYBR"])
    sod["fips"] = (sod["STCNTYBR"].astype(float).astype(int)
                   .astype(str).str.zfill(5))
    sod["DEPSUMBR"] = pd.to_numeric(sod["DEPSUMBR"], errors="coerce").fillna(0)

    def dep_wtd(series, name):
        s = sod.copy()
        s["v"] = s["fips"].map(series)
        s = s.dropna(subset=["v"])
        g = s.groupby("CERT").apply(
            lambda d: np.average(d["v"], weights=d["DEPSUMBR"])
            if d["DEPSUMBR"].sum() > 0 else np.nan, include_groups=False)
        return g.rename(name)

    gw_pop = dep_wtd(pop_share, "ws_pop")
    gw = {g: dep_wtd(debtor[g], f"ws_{g}") for g in debtor}
    gw_pw = {g: dep_wtd(debtor_pw[g].dropna(), f"wspw_{g}")
             for g in debtor_pw if debtor_pw[g].notna().any()}

    for s in [gw_pop] + list(gw.values()) + list(gw_pw.values()):
        fin[s.name] = fin["CERT"].map(s)

    # ---- the two constructs ----------------------------------------------
    b = fin["book"]
    comp_leg = np.zeros(len(fin))
    lb_debtor = np.zeros(len(fin))
    lb_debtor_pw = np.zeros(len(fin))
    for cls, (items, grp) in CLASS_ITEMS.items():
        share = sum(fin[i].fillna(0) for i in items) / b
        comp_leg += share * beta[cls]
        lb_debtor += share * beta[cls] * fin[f"ws_{grp}"]
        pw_col = f"wspw_{grp}"
        pw = fin[pw_col] if pw_col in fin.columns else fin[f"ws_{grp}"]
        lb_debtor_pw += share * beta[cls] * pw.fillna(fin[f"ws_{grp}"])
    # business classes contribute zero by rule
    for i in ZERO_ITEMS:
        comp_leg += (fin[i].fillna(0) / b) * 0.0

    fin["lb_composition"] = comp_leg
    fin["lb_debtor"] = lb_debtor
    fin["lb_debtor_paywtd"] = lb_debtor_pw
    fin["lb_rival"] = comp_leg * fin["ws_pop"]

    # conventional composition shares, for the joint test
    fin["sh_resre"] = fin["LNRERES"].fillna(0) / b
    fin["sh_cre"] = (fin["LNRENRES"].fillna(0) + fin["LNREMULT"].fillna(0)) / b
    fin["sh_constr"] = fin["LNRECONS"].fillna(0) / b
    fin["sh_ci"] = fin["LNCI"].fillna(0) / b
    fin["sh_consumer"] = (fin["LNCRCD"].fillna(0) + fin["LNAUTO"].fillna(0)
                          + fin["LNCONOTH"].fillna(0)) / b
    fin["sh_ag"] = (fin["LNAG"].fillna(0) + fin["LNREAG"].fillna(0)) / b
    fin["sh_sec"] = fin["SC"].fillna(0) / b

    p = fin.dropna(subset=["lb_debtor", "lb_rival", "ws_pop"]).copy()
    y = p["lb_debtor"].to_numpy()

    comp_basis = ["sh_resre", "sh_consumer", "sh_cre", "sh_constr", "sh_ci",
                  "sh_ag", "sh_sec"]
    C = p[comp_basis].fillna(0).to_numpy()

    y_pw = p["lb_debtor_paywtd"].to_numpy()
    models = {
        "rival alone (loan shares x population wage share)":
            p[["lb_rival"]].to_numpy(),
        "loan composition shares alone": C,
        "population wage share alone": p[["ws_pop"]].to_numpy(),
        "rival + loan composition shares":
            np.hstack([p[["lb_rival"]].to_numpy(), C]),
        "composition + population wage share + interactions":
            np.hstack([C, p[["ws_pop"]].to_numpy(),
                       C * p[["ws_pop"]].to_numpy()]),
    }
    rows = [{"model": k, "R2_explaining_lb_debtor": r2(y, X),
             "R2_explaining_lb_debtor_paywtd": r2(y_pw, X)}
            for k, X in models.items()]
    dec = pd.DataFrame(rows)
    dec.to_csv(OUT / "debtor_construct_decomposition.csv", index=False)

    verdict = {
        "n_banks": int(len(p)),
        "lb_debtor_mean": float(p["lb_debtor"].mean()),
        "lb_debtor_sd": float(p["lb_debtor"].std()),
        "lb_rival_mean": float(p["lb_rival"].mean()),
        "lb_rival_sd": float(p["lb_rival"].std()),
        "corr_debtor_rival": float(p["lb_debtor"].corr(p["lb_rival"])),
        "corr_debtor_paywtd_rival": float(
            p["lb_debtor_paywtd"].corr(p["lb_rival"])),
        "R2_rival_explaining_debtor": float(r2(y, p[["lb_rival"]].to_numpy())),
        "corr_ws_mortgage_ws_pop": float(p["ws_mortgage"].corr(p["ws_pop"])),
        "corr_ws_all_ws_pop": float(p["ws_all"].corr(p["ws_pop"])),
        "corr_ws_mortgage_ws_all": float(p["ws_mortgage"].corr(p["ws_all"])),
        "mean_ws_mortgage": float(p["ws_mortgage"].mean()),
        "mean_ws_all": float(p["ws_all"].mean()),
        "mean_ws_pop": float(p["ws_pop"].mean()),
    }
    pd.Series(verdict).to_json(OUT / "debtor_construct_verdict.json", indent=2)

    keep = (["CERT", "NAMEFULL", "STNAME", "lb_debtor", "lb_debtor_paywtd",
             "lb_rival", "lb_composition", "ws_pop"]
            + [c for c in p.columns if c.startswith(("ws_", "wspw_"))]
            + comp_basis)
    p[list(dict.fromkeys(keep))].to_csv(
        RAW / "preshock_debtor_panel_2014.csv", index=False)

    print("AMENDMENT 1 CONSTRUCT TEST\n")
    print(dec.to_string(index=False))
    print()
    for k, v in verdict.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
