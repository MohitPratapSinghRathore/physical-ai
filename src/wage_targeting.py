"""Amendment (a): reorganise the dose-response table by the WAGE DISTRIBUTION rather than by
exposure index.

WHY. A87 showed that neither exposure-type contrast survives controlling for pay: between 1
and 11 percent of each raw gap remains once the two groups are put on a common wage
distribution, and one specification reverses sign. If exposure type is mostly a pay proxy,
then the primitive the paper should organise around is WHERE IN THE WAGE DISTRIBUTION
DISPLACEMENT FALLS, and the exposure indices become named scenarios for that, not separate
mechanisms.

WHAT THIS MODULE DOES.

  1. Displacement targeted by wage quintile. Bottom (Q1), middle (Q3) and top (Q5) of the
     individual wage distribution, each displacing the SAME share of the TOTAL wage bill, so
     the three are comparable by construction. Where a quintile cannot deliver the dose out
     of its own wage bill the row is SATURATED and flagged, exactly as in the exposure
     version.

  2. For each: the fiscal loss split into PAYROLL TAX and INCOME TAX, OASDI and HI
     separately, and the household exposures (mortgage, rent, auto, card, student), buffers
     and runway.

  3. Where each exposure index actually falls in the distribution, so the indices can be
     read as named scenarios.

  4. Whether the opposite-places geography result (A36) is also a pay result: the
     correlation of each exposure share with PUMA median home value, before and after
     controlling for PUMA mean wage.

SOURCES AND RATES.

  Payroll   Statutory rates, employee plus employer: OASDI 12.4 percent on wages up to the
            2026 contribution and benefit base of 184,500 dollars (26 USC 3101(a), 3111(a));
            HI 2.9 percent uncapped (26 USC 3101(b), 3111(b)). The 0.9 percent additional
            Medicare tax above 200,000 is NOT modelled and its omission understates the top
            quintile's payroll loss slightly.

  Income    A MARGINAL effective federal income tax rate schedule, differenced across
            adjusted gross income classes in IRS SOI Table 1.4 for 2023
            (data/raw/irs/23in14ar.xls): the change in income tax before credits divided by
            the change in AGI between adjacent classes. FLAGGED: "before credits" overstates
            tax actually paid, most at the bottom where refundable credits are largest, so
            the bottom-quintile income tax loss here is an upper bound. Household AGI is
            proxied by ACS household income.

  Balances  SIPP 2025, scaled by the CORRECTED full-universe under-reporting factors (A86).

WHAT THIS IS NOT. Targeting by wage quintile is a scenario device, not a prediction. Nothing
in the exposure data says displacement will fall on the bottom or the top. The point is that
once the dose and the place in the wage distribution are fixed, the exposure index adds
almost nothing, which is the same result as A87 seen from the other side.
"""
import io, json, pathlib, sys, zipfile
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).parents[1]
RAW, OUT = ROOT / "data" / "raw", ROOT / "data" / "processed"
sys.path.insert(0, str(ROOT))

OASDI_RATE, OASDI_CAP = 0.124, 184_500.0
HI_RATE = 0.029
WB_LEVELS = [0.05, 0.10, 0.25, 0.50, 0.75]
# All five quintiles, so the wage-organised dose-response table has a fiscal column
# for every row. The first version ran only Q1, Q3 and Q5, which left Q2 and Q4 with
# a credit loss and no fiscal loss and made their "who bears it" shares incomparable.
QUINTILE_TARGETS = {"bottom_Q1": 0, "Q2": 1, "middle_Q3": 2, "Q4": 3, "top_Q5": 4}

PCOLS = ["SERIALNO", "OCCP", "WAGP", "ADJINC", "PWGTP", "ESR"]
HCOLS = ["SERIALNO", "WGTP", "TEN", "MRGP", "GRNTP", "ADJHSG", "ADJINC", "HINCP", "NP",
         "PUMA", "STATE", "VALP"]


def soi_marginal_rates():
    """Marginal effective federal income tax rate by AGI, differenced across SOI AGI
    classes. Returns (upper edges array, marginal rate array)."""
    d = pd.read_excel(RAW / "irs" / "23in14ar.xls", "TBL14", header=None)
    lab = d.iloc[:, 0].astype(str)
    start = lab[lab.str.startswith("All returns, total")].index[0]
    rows = []
    for i in range(start + 1, start + 40):
        s = lab.iloc[i]
        if not s.startswith(("$", "No adjusted")):
            break
        agi = pd.to_numeric(d.iloc[i, 2], errors="coerce")       # AGI less deficit, thousands
        tax = pd.to_numeric(d.iloc[i, 148], errors="coerce")     # income tax before credits
        m = s.replace("$", "").replace(",", "")
        if "or more" in m:
            hi = np.inf
        elif "under" in m:
            hi = float(m.split("under")[1].strip())
        else:
            hi = 0.0
        rows.append((hi, agi, tax))
    R = pd.DataFrame(rows, columns=["upper", "agi", "tax"]).dropna()
    R = R.sort_values("upper").reset_index(drop=True)
    R["cum_agi"] = R["agi"].cumsum()
    R["cum_tax"] = R["tax"].cumsum()
    R["marg"] = (R["cum_tax"].diff() / R["cum_agi"].diff()).fillna(
        R["tax"] / R["agi"].replace(0, np.nan))
    R["marg"] = R["marg"].clip(0, 0.45)
    return R


def load(with_geo=True):
    from src.stress import acs_engine as AE
    pp = []
    for fn in AE.PPART:
        for ch in AE._chunks("csv_pus.zip", fn, PCOLS):
            adj = pd.to_numeric(ch["ADJINC"], errors="coerce") / 1e6
            pp.append(pd.DataFrame({
                "SERIALNO": ch["SERIALNO"].astype(str),
                "occp": pd.to_numeric(ch["OCCP"], errors="coerce"),
                "wage": (pd.to_numeric(ch["WAGP"], errors="coerce").fillna(0.0)
                         * adj).astype(np.float32),
                "pwgtp": pd.to_numeric(ch["PWGTP"], errors="coerce").fillna(0.0
                                                                            ).astype(np.float32),
                "employed": pd.to_numeric(ch["ESR"], errors="coerce").isin(
                    [1, 2, 4, 5]).to_numpy()}))
    P = pd.concat(pp, ignore_index=True)
    hh = []
    for fn in AE.HPART:
        for ch in AE._chunks("csv_hus.zip", fn, HCOLS):
            adjh = pd.to_numeric(ch["ADJHSG"], errors="coerce") / 1e6
            adji = pd.to_numeric(ch["ADJINC"], errors="coerce") / 1e6
            ten = pd.to_numeric(ch["TEN"], errors="coerce")
            hh.append(pd.DataFrame({
                "SERIALNO": ch["SERIALNO"].astype(str),
                "wgtp": pd.to_numeric(ch["WGTP"], errors="coerce").fillna(0.0
                                                                          ).astype(np.float32),
                "mort": np.nan_to_num(np.where(ten == 1, pd.to_numeric(
                    ch["MRGP"], errors="coerce") * 12 * adjh, 0.0)).astype(np.float32),
                "rent": np.nan_to_num(np.where(ten == 3, pd.to_numeric(
                    ch["GRNTP"], errors="coerce") * 12 * adjh, 0.0)).astype(np.float32),
                "hincp": (pd.to_numeric(ch["HINCP"], errors="coerce").fillna(0.0)
                          * adji).astype(np.float32),
                "valp": (pd.to_numeric(ch["VALP"], errors="coerce") * adjh).astype(np.float32),
                "np_persons": pd.to_numeric(ch["NP"], errors="coerce").fillna(0).astype(np.int16),
                "puma_id": (ch["STATE"].astype(str).str.zfill(2)
                            + ch["PUMA"].astype(str).str.zfill(5))}))
    H = pd.concat(hh, ignore_index=True)
    H = H[(H["wgtp"] > 0) & (H["np_persons"] > 0)].reset_index(drop=True)
    P = P[(P["wage"] > 0) & P["occp"].notna() & P["employed"]].reset_index(drop=True)
    P["occp"] = P["occp"].astype(np.int32)
    return P, H


def sipp_by_quintile():
    """SIPP balances, buffers and runway by individual wage quintile, on the corrected
    under-reporting factors."""
    ur = pd.read_csv(OUT / "under_reporting_factors.csv").set_index("loan")
    cols = ["SSUID", "ERESIDENCEID", "MONTHCODE", "WPFINWGT", "ERELRPE", "RMESR", "TPEARN",
            "THDEBT_HOME", "THDEBT_CC", "THDEBT_VEH", "THDEBT_ED", "THVAL_BANK", "TPTOTINC"]
    z = zipfile.ZipFile(RAW / "sipp" / "pu2025_csv.zip")
    rows = []
    with z.open("pu2025.csv") as fh:
        txt = io.TextIOWrapper(fh, encoding="utf-8", errors="replace")
        header = txt.readline().rstrip("\n").split("|")
        idx = {c: header.index(c) for c in cols if c in header}
        mc = idx["MONTHCODE"]
        for line in txt:
            f = line.rstrip("\n").split("|")
            if len(f) <= mc or f[mc] != "12":
                continue
            rows.append([f[idx[c]] if c in idx else "" for c in cols])
    D = pd.DataFrame(rows, columns=cols)
    for c in cols:
        if c not in ("SSUID", "ERESIDENCEID"):
            D[c] = pd.to_numeric(D[c], errors="coerce")
    D["hh"] = D["SSUID"].astype(str) + "_" + D["ERESIDENCEID"].astype(str)
    W = D[D["RMESR"].isin([1, 2, 3, 4, 5]) & (D["TPEARN"] > 0)].copy()
    W["annual_wage"] = W["TPEARN"] * 12.0
    # quintiles on individual annual wage, person weighted
    o = np.argsort(W["annual_wage"].to_numpy())
    w, wt = W["annual_wage"].to_numpy()[o], W["WPFINWGT"].to_numpy()[o]
    cum = np.cumsum(wt) / wt.sum()
    edges = np.interp([0.2, 0.4, 0.6, 0.8], cum, w)
    W["q"] = np.digitize(W["annual_wage"].to_numpy(), edges)
    ref = D[D["ERELRPE"].isin([1, 2])].sort_values("WPFINWGT").groupby("hh").tail(1
                                                                                   ).set_index("hh")
    bal = {}
    for lab, col in [("mortgage", "THDEBT_HOME"), ("card", "THDEBT_CC"),
                     ("auto", "THDEBT_VEH"), ("student", "THDEBT_ED")]:
        bal[lab] = D.groupby("hh")[col].max()
    liq = D.groupby("hh")["THVAL_BANK"].max()
    inc = D.groupby("hh")["TPTOTINC"].sum()
    out = []
    for q in range(5):
        sel = W[W["q"] == q]
        hhs = sel["hh"].unique()
        wtq = ref.reindex(hhs)["WPFINWGT"].fillna(0.0)
        row = {"q": q, "workers_m": sel["WPFINWGT"].sum() / 1e6,
               "mean_wage": np.average(sel["annual_wage"], weights=sel["WPFINWGT"])}
        for lab in bal:
            b = bal[lab].reindex(hhs).fillna(0.0)
            row[f"{lab}_balance_bn"] = float((b * wtq).sum()) / 1e9 * float(
                ur.loc[lab, "UNDER_REPORTING_factor"])
        L = liq.reindex(hhs).fillna(0.0)
        I = inc.reindex(hhs).fillna(0.0).replace(0, np.nan)
        row["median_liquid"] = float(np.nanmedian(L))
        runway = (L / I).replace([np.inf, -np.inf], np.nan)
        row["median_runway_months"] = float(np.nanmedian(runway))
        row["pct_under_1_month"] = float(((runway < 1).astype(float) * wtq).sum()
                                         / max(wtq.sum(), 1) * 100)
        out.append(row)
    return pd.DataFrame(out)


def main():
    from src.stress import scenarios as SC
    _, groups = SC._h3().build_groups()
    R = soi_marginal_rates()
    print("=== MARGINAL EFFECTIVE FEDERAL INCOME TAX RATE, SOI 2023 Table 1.4 ===")
    print("    income tax BEFORE CREDITS differenced across AGI classes; FLAGGED as an "
          "upper bound,\n    most at the bottom where refundable credits are largest")
    for _, r in R.iterrows():
        u = "and over" if np.isinf(r.upper) else f"under {r.upper:,.0f}"
        print(f"    AGI {u:>22s}   marginal rate {r.marg:6.2%}")

    P, H = load()
    hidx = pd.Series(np.arange(len(H), dtype=np.int32), index=H["SERIALNO"].to_numpy())
    hidx = hidx[~hidx.index.duplicated()]
    j = P["SERIALNO"].map(hidx)
    keep = j.notna().to_numpy()
    P, j = P[keep].reset_index(drop=True), j[keep].to_numpy(np.int32)

    wage = P["wage"].to_numpy(np.float64)
    wt = P["pwgtp"].to_numpy(np.float64)
    hinc = H["hincp"].to_numpy(np.float64)[j]
    mort = H["mort"].to_numpy(np.float64)[j]
    rent = H["rent"].to_numpy(np.float64)[j]
    hwt = H["wgtp"].to_numpy(np.float64)[j]

    # Marginal income tax rate at each worker's household AGI. The SOI class edges are in
    # DOLLARS of AGI, and ACS household income is in dollars, so no rescaling is applied.
    # The first run divided household income by a thousand, which put every household in
    # the lowest AGI class and made the income tax loss look flat at 0.28 percent across
    # the whole distribution. That was the error the flat column exposed.
    edges_agi = R["upper"].to_numpy()
    marg = R["marg"].to_numpy()
    pos = np.searchsorted(edges_agi, hinc, side="left").clip(0, len(marg) - 1)
    mrate = marg[pos]

    # wage quintiles, person weighted
    o = np.argsort(wage)
    cum = np.cumsum(wt[o]) / wt.sum()
    qedges = np.interp([0.2, 0.4, 0.6, 0.8], cum, wage[o])
    q = np.digitize(wage, qedges)
    total_wb = float((wage * wt).sum())
    print(f"\n=== WAGE QUINTILES, ACS, person weighted. total wage bill "
          f"{total_wb / 1e9:,.0f}bn ===")
    for k in range(5):
        m = q == k
        print(f"    Q{k+1}: wage {wage[m].min():>9,.0f} to {wage[m].max():>10,.0f}   "
              f"mean {np.average(wage[m], weights=wt[m]):>9,.0f}   "
              f"share of the wage bill {(wage[m] * wt[m]).sum() / total_wb:6.2%}")

    rows = []
    for name, qi in QUINTILE_TARGETS.items():
        m = q == qi
        wb_q = float((wage[m] * wt[m]).sum())
        for d in WB_LEVELS:
            f = d * total_wb / wb_q
            sat = f > 1.0
            f = min(f, 1.0)
            w_lost = f * wb_q
            taxable = np.minimum(wage[m], OASDI_CAP)
            oasdi = f * float((taxable * wt[m]).sum()) * OASDI_RATE
            hi = w_lost * HI_RATE
            inc_tax = f * float((wage[m] * mrate[m] * wt[m]).sum())
            rows.append({
                "target": name, "dose_share_of_total_wage_bill": d,
                "saturated": sat,
                "delivered_share": w_lost / total_wb,
                "wage_lost_bn": w_lost / 1e9,
                "payroll_tax_loss_bn": (oasdi + hi) / 1e9,
                "OASDI_loss_bn": oasdi / 1e9, "HI_loss_bn": hi / 1e9,
                "income_tax_loss_bn": inc_tax / 1e9,
                "total_fiscal_loss_bn": (oasdi + hi + inc_tax) / 1e9,
                "payroll_share_of_fiscal": (oasdi + hi) / (oasdi + hi + inc_tax),
                "mortgage_payment_exposed_bn": f * float((mort[m] * hwt[m]).sum()) / 1e9,
                "rent_payment_exposed_bn": f * float((rent[m] * hwt[m]).sum()) / 1e9,
                "effective_payroll_rate": (oasdi + hi) / w_lost,
                "effective_income_tax_rate": inc_tax / w_lost,
            })
    T = pd.DataFrame(rows)
    T.round(5).to_csv(OUT / "wage_targeted_dose_response.csv", index=False)

    pd.set_option("display.width", 250)
    print("\n=== FISCAL LOSS BY WHERE IN THE WAGE DISTRIBUTION DISPLACEMENT FALLS ===")
    print("    same dose, same total wage bill displaced, billions of dollars")
    v = T[~T.saturated]
    print(v.pivot_table(index="dose_share_of_total_wage_bill", columns="target",
                        values=["OASDI_loss_bn", "HI_loss_bn", "income_tax_loss_bn",
                                "total_fiscal_loss_bn"]).round(1).to_string())
    print("\n=== EFFECTIVE RATES ON THE DISPLACED WAGE DOLLAR ===")
    e = T.drop_duplicates("target")
    for _, r in e.iterrows():
        print(f"    {r.target:10s} payroll {r.effective_payroll_rate:6.2%}   "
              f"income tax {r.effective_income_tax_rate:6.2%}   "
              f"payroll is {r.payroll_share_of_fiscal:5.1%} of the fiscal loss")
    print("\n=== HOUSEHOLD PAYMENT EXPOSURE, billions per year ===")
    print(v.pivot_table(index="dose_share_of_total_wage_bill", columns="target",
                        values=["mortgage_payment_exposed_bn", "rent_payment_exposed_bn"]
                        ).round(1).to_string())
    print("\n=== SATURATION: a quintile cannot deliver more than its own wage bill ===")
    for _, r in T[T.saturated].iterrows():
        print(f"    {r.target:10s} target {r.dose_share_of_total_wage_bill:>4.0%}: "
              f"delivers {r.delivered_share:.1%} at most")

    # ---- where the exposure indices fall in the distribution
    print("\n=== WHERE EACH EXPOSURE INDEX FALLS IN THE WAGE DISTRIBUTION ===")
    print("    share of that index's top-quintile wage bill sitting in each wage quintile")
    gq = []
    for g in ["embodied", "cognitive_AIOE", "cognitive_GPT"]:
        sel = P["occp"].isin(groups[g]).to_numpy()
        tot = (wage[sel] * wt[sel]).sum()
        row = {"exposure": g}
        for k in range(5):
            mm = sel & (q == k)
            row[f"Q{k+1}"] = (wage[mm] * wt[mm]).sum() / tot
        gq.append(row)
    G = pd.DataFrame(gq).set_index("exposure")
    print((G * 100).round(1).to_string())
    G.round(5).to_csv(OUT / "exposure_by_wage_quintile.csv")

    # ---- geography: is the opposite-places result a pay result?
    print("\n=== IS THE OPPOSITE-PLACES GEOGRAPHY RESULT A PAY RESULT? ===")
    Pg = pd.DataFrame({"puma_id": H["puma_id"].to_numpy()[j], "wage": wage, "wt": wt})
    for g in ["embodied", "cognitive_AIOE", "cognitive_GPT"]:
        Pg[g] = (P["occp"].isin(groups[g]).to_numpy() * wage * wt)
    Pg["wwt"] = wage * wt
    A = Pg.groupby("puma_id").agg(
        wage_bill=("wwt", "sum"), wt=("wt", "sum"),
        **{g: (g, "sum") for g in ["embodied", "cognitive_AIOE", "cognitive_GPT"]})
    A["mean_wage"] = A["wage_bill"] / A["wt"]
    Hv = H[H["valp"] > 0]
    hv = Hv.groupby("puma_id").apply(
        lambda d: np.average(d["valp"], weights=d["wgtp"]), include_groups=False)
    A["mean_home_value"] = hv
    A = A.dropna()
    for g in ["embodied", "cognitive_AIOE", "cognitive_GPT"]:
        A[f"{g}_share"] = A[g] / A["wage_bill"]
    res = []
    for g in ["embodied", "cognitive_AIOE", "cognitive_GPT"]:
        x, y, z_ = (A[f"{g}_share"].to_numpy(), np.log(A["mean_home_value"].to_numpy()),
                    np.log(A["mean_wage"].to_numpy()))
        raw = np.corrcoef(x, y)[0, 1]
        # partial correlation of exposure share with log home value, controlling log wage
        def resid(a, b):
            b1 = np.polyfit(b, a, 1)
            return a - np.polyval(b1, b)
        part = np.corrcoef(resid(x, z_), resid(y, z_))[0, 1]
        wagecorr = np.corrcoef(x, z_)[0, 1]
        res.append({"exposure": g, "corr_with_PUMA_mean_wage": wagecorr,
                    "corr_with_home_value": raw,
                    "partial_corr_home_value_given_wage": part,
                    "share_of_correlation_surviving": part / raw if raw else np.nan})
        print(f"    {g:15s} corr with PUMA mean wage {wagecorr:+.3f}   "
              f"with home value {raw:+.3f}   "
              f"PARTIAL given wage {part:+.3f}   "
              f"survives {part / raw:6.1%}" if raw else "")
    Gg = pd.DataFrame(res)
    Gg.round(4).to_csv(OUT / "geography_pay_control.csv", index=False)
    print(f"\n    {len(A):,} PUMAs.")

    (OUT / "wage_targeting_summary.json").write_text(json.dumps({
        "total_wage_bill_bn": total_wb / 1e9,
        "quintile_edges": [float(x) for x in qedges],
        "marginal_income_tax_schedule": R[["upper", "marg"]].replace(
            {np.inf: None}).round(4).to_dict("records"),
        "geography": Gg.round(4).to_dict("records"),
        "exposure_by_wage_quintile": G.round(4).to_dict("index"),
    }, indent=2, default=str))

    S = sipp_by_quintile()
    S.round(3).to_csv(OUT / "sipp_by_wage_quintile.csv", index=False)
    print("\n=== SIPP: BALANCES, BUFFERS AND RUNWAY BY WAGE QUINTILE ===")
    print("    balances scaled by the corrected full-universe under-reporting factors")
    print(S.round(2).to_string(index=False))


if __name__ == "__main__":
    main()
