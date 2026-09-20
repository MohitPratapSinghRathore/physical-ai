"""Items 1 and 2: trust fund arithmetic done properly, and survey balances benchmarked.

ITEM 1. THE TRUST FUND BOUND VIOLATION.

A77 reported the fiscal loss as 107.4 and 214.8 percent of OASDI payroll income and 307 and
614 percent of HI revenue. **A loss on a payroll tax cannot exceed that tax.** The audit in
src/verify/plausibility_audit.py confirms the violation.

The error was dividing a GENERAL revenue loss, computed with an economy-wide labour tax rate
tau_l of about 0.30, by a PAYROLL-ONLY denominator. That is two different taxes.

Correct construction, stated explicitly:

    numerator   = payroll tax rate x displaced TAXABLE wages x (1 - R)
    denominator = that fund's payroll income

OASDI taxable wages are capped at the contribution and benefit base; HI wages are not capped.
Because both numerator and denominator carry the same rate, the rate cancels and the ratio is

    (taxable wages displaced / total taxable wages) x (1 - R) x payroll share of fund income

which is bounded by the payroll share of fund income and therefore cannot exceed 1.

SOURCED PARAMETERS

    OASDI contribution and benefit base, 2026: 184,500 USD (2025: 176,100). Verified through
    The Tax Adviser, AICPA, 24 October 2025, reporting the SSA announcement. **SSA.gov itself
    returns HTTP 403 to this environment on every route tried, including the COLA fact sheet
    and the contribution base page**, which is why a secondary source is used and named.
    OASDI rate 6.2 percent each side, HI 1.45 percent each side with no cap, plus an
    additional 0.9 percent above 200,000 which is NOT modelled here.
    Payroll is 91.26 percent of OASDI trust fund income and 87.20 percent of HI trust fund
    income, both read from the 2026 Trustees summary tables (Table 5). The earlier version
    of this module applied the OASDI share to HI as well, which overstated every HI ratio
    by a factor of 1.047.

ITEM 2. SURVEY BALANCES BENCHMARKED TO AGGREGATES.

The audit found implied bank shares above 1 for cards (2.97) and auto (1.06), which is
impossible and is a symptom of SIPP under-reporting. Household balances by loan type are
scaled to official aggregates and the scaling factors are reported. The caps are removed.
"""
import io, json, pathlib, zipfile
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).parents[1]
RAW, OUT = ROOT / "data" / "raw", ROOT / "data" / "processed"

OASDI_CAP_2026 = 184_500.0
# Payroll share of each fund's TOTAL income, read from the 2026 Trustees summary tables the
# owner placed in data/raw/owner/ (Table 5), not assumed. The two funds differ and using the
# OASDI share for HI overstated every HI ratio by a factor of 1.047.
_OWN = json.loads((pathlib.Path(__file__).parents[1] / "data" / "processed"
                   / "owner_sources.json").read_text())["trustees_2026"]
PAYROLL_SHARE_OASDI = _OWN["payroll_share_of_oasdi_income"]
PAYROLL_SHARE_HI = round(_OWN["hi_payroll_income_bn"] / _OWN["hi_total_income_bn"], 4)
# official aggregates, USD billions
AGG = {
    "mortgage": {"value": 13_100.0, "source": "NY Fed HHDC 2026Q2, mortgage balances"},
    "student": {"value": 1_650.0, "source": "NY Fed HHDC 2026Q2, outstanding student debt"},
}


def fred_last(series):
    p = RAW / "fred" / f"{series}.csv"
    if not p.exists():
        import requests
        r = requests.get(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series}",
                         timeout=90)
        if r.status_code != 200 or not r.text.lstrip().lower().startswith(
                ("observation_date", "date")):
            return None, None
        p.write_bytes(r.content)
    d = pd.read_csv(p)
    d.columns = ["date", "v"]
    d["v"] = pd.to_numeric(d["v"], errors="coerce")
    d = d.dropna()
    return float(d["v"].iloc[-1]), str(d["date"].iloc[-1])


def nyfed_auto_balance_bn():
    """AUTO AGGREGATE, replaced in the replication-repair session (item 5).

    FRED MVLOAS, motor vehicle loans owned and securitized, was DISCONTINUED after 2024Q4
    while every other input in this project is 2026, and Fed G.19 no longer publishes a
    live motor vehicle loan balance. The replacement is the NY Fed Household Debt and
    Credit report, which is ALREADY the source of the mortgage and student aggregates and
    is on the same 2026Q2 vintage. Read from the report's own data workbook rather than
    from the PDF, because the PDF gives auto only as a quarterly percentage change.

    CARDS stay on FRED REVOLSL. Revolving consumer credit and the NY Fed credit card
    balance are different objects (1,357.2bn against 1,263bn) and the brief names REVOLSL.
    The choice is stated rather than left implicit.
    """
    import openpyxl
    p = RAW / "manual" / "NYFed_HHDC_2026Q2_data.xlsx"
    wb = openpyxl.load_workbook(p, read_only=True, data_only=True)
    ws = wb["Page 3 Data"]
    rows = list(ws.iter_rows(min_row=1, values_only=True))
    header = next(list(r) for r in rows if r and "Auto Loan" in r)
    data = [r for r in rows if r and r[0] and isinstance(r[1], (int, float))]
    col = header.index("Auto Loan")
    last = data[-1]
    return float(last[col]) * 1000.0, (
        f"NY Fed Household Debt and Credit report data workbook, Page 3 Data, "
        f"auto loan balance at {last[0]}, trillions converted to billions. REPLACES FRED "
        f"MVLOAS (1,568.6bn at 2024Q4), which was discontinued after 2024Q4.")


def acs_wages():
    """Wage distribution by exposure group, for the OASDI cap. ACS PUMS person file."""
    import sys
    sys.path.insert(0, str(ROOT))
    from src.stress import scenarios as SC
    _, groups = SC._h3().build_groups()
    z = zipfile.ZipFile(RAW / "pums" / "csv_pus.zip")
    acc = {}
    for fn in ["psam_pusa.csv", "psam_pusb.csv"]:
        with z.open(fn) as fh:
            for ch in pd.read_csv(io.TextIOWrapper(fh, encoding="utf-8", errors="replace"),
                                  usecols=["OCCP", "WAGP", "ADJINC", "PWGTP", "ESR"],
                                  chunksize=400_000, low_memory=False):
                adj = pd.to_numeric(ch["ADJINC"], errors="coerce") / 1e6
                wage = pd.to_numeric(ch["WAGP"], errors="coerce").fillna(0.0) * adj
                pw = pd.to_numeric(ch["PWGTP"], errors="coerce").fillna(0.0)
                occ = pd.to_numeric(ch["OCCP"], errors="coerce")
                emp = pd.to_numeric(ch["ESR"], errors="coerce").isin([1, 2, 4, 5])
                m = emp & (wage > 0)
                w, p, o = wage[m].to_numpy(), pw[m].to_numpy(), occ[m]
                cap = np.minimum(w, OASDI_CAP_2026)
                for gname in ["cognitive_AIOE", "cognitive_GPT", "embodied", "ALL"]:
                    sel = np.ones(len(w), bool) if gname == "ALL" else o.isin(
                        groups[gname]).to_numpy()
                    a = acc.setdefault(gname, {"wage": 0.0, "taxable": 0.0})
                    a["wage"] += float((w[sel] * p[sel]).sum())
                    a["taxable"] += float((cap[sel] * p[sel]).sum())
    return acc


def main():
    print("=== ITEM 1: trust fund arithmetic, rebuilt ===")
    acc = acs_wages()
    tot_taxable = acc["ALL"]["taxable"]
    tot_wage = acc["ALL"]["wage"]
    print(f"  total wage bill (ACS, employed with wages) {tot_wage/1e9:,.1f}bn")
    print(f"  OASDI-taxable portion at the {OASDI_CAP_2026:,.0f} cap "
          f"{tot_taxable/1e9:,.1f}bn ({100*tot_taxable/tot_wage:.1f}%)")
    for g in ["cognitive_AIOE", "cognitive_GPT", "embodied"]:
        a = acc[g]
        print(f"  {g:16s} wage {a['wage']/1e9:>9,.1f}bn  taxable {a['taxable']/1e9:>9,.1f}bn "
              f"({100*a['taxable']/a['wage']:.1f}% under the cap)")

    fx = pd.read_csv(OUT / "fiscal_extended_axis.csv")
    fx = fx[(fx.rho_mode == "fitted") & (fx.horizon == 10)
            & (fx.outlays == "no_outlays")].drop_duplicates(
        subset=["group", "level_of_exposed"])
    rows = []
    for _, r in fx.iterrows():
        d_wb = r["share_of_total_wage_bill"]
        R = r["R"]
        base = g_for = None
        for g in ["cognitive_AIOE", "cognitive_GPT", "embodied"]:
            if r["group"].startswith(g):
                g_for = g
        if g_for is None:
            g_for = "ALL"
        # taxable share of the displaced group's wages
        tx_share = acc[g_for]["taxable"] / acc[g_for]["wage"]
        # displaced taxable wages as a share of all taxable wages
        oasdi_ratio = (d_wb * tot_wage * tx_share / tot_taxable) * (1 - R) * PAYROLL_SHARE_OASDI
        hi_ratio = d_wb * (1 - R) * PAYROLL_SHARE_HI
        rows.append({"group": r["group"], "level_of_exposed": r["level_of_exposed"],
                     "share_of_total_wage_bill": d_wb, "R": R,
                     "taxable_share_of_group_wages": tx_share,
                     "OASDI_loss_pct_of_fund_payroll_income": 100 * oasdi_ratio,
                     "HI_loss_pct_of_fund_payroll_income": 100 * hi_ratio,
                     "outside_data": r["outside_data"]})
    T = pd.DataFrame(rows)
    T.round(4).to_csv(OUT / "trust_fund_corrected.csv", index=False)
    pd.set_option("display.width", 240)
    T["wb_pct"] = (T.share_of_total_wage_bill * 100).round(0)
    print("\n=== CORRECTED trust fund loss, percent of that fund's payroll income ===")
    for target in (10, 25, 50, 75):
        s = T[np.isclose(T.wb_pct, target, atol=4)]
        if not len(s):
            continue
        print(f"  {target:>3}% of the wage bill: OASDI "
              f"{s.OASDI_loss_pct_of_fund_payroll_income.mean():6.2f}%, HI "
              f"{s.HI_loss_pct_of_fund_payroll_income.mean():6.2f}%   "
              f"[{int(s.outside_data.sum())}/{len(s)} outside data]")
    mx = max(T.OASDI_loss_pct_of_fund_payroll_income.max(),
             T.HI_loss_pct_of_fund_payroll_income.max())
    print(f"\n  BOUND CHECK: maximum {mx:.2f} percent, "
          f"{'OK, within 0 to 100' if mx <= 100 else 'STILL VIOLATING'}")
    print(f"  A77 reported 107.4 and 214.8 percent for OASDI. Those are WITHDRAWN.")

    print("\n=== ITEM 2: survey balances benchmarked to aggregates ===")
    # UNITS READ FROM THE PROVIDER, per decision D1. Both series are in MILLIONS of dollars,
    # not billions. The first run of this module divided by the wrong scale and produced
    # scaling factors in the thousands, which is how the error was caught.
    card, cdate = fred_last("REVOLSL")
    AGG["card"] = {"value": card / 1000.0 if card else None,
                   "source": f"FRED REVOLSL revolving consumer credit, millions ({cdate})"}
    auto_bn, auto_date = nyfed_auto_balance_bn()
    AGG["auto"] = {"value": auto_bn, "source": auto_date}
    hc = pd.read_csv(OUT / "verify" / "hand_check_credit.csv")
    base = hc.drop_duplicates(subset=["loan"])[["loan", "total_balance_bn"]]
    scal = []
    for _, b in base.iterrows():
        agg = AGG.get(b["loan"], {}).get("value")
        if agg is None:
            continue
        scal.append({"loan": b["loan"], "sipp_working_core_bn": b["total_balance_bn"],
                     "official_aggregate_bn": agg,
                     "scaling_factor": agg / b["total_balance_bn"],
                     "source": AGG[b["loan"]]["source"]})
    S = pd.DataFrame(scal)
    S.round(3).to_csv(OUT / "balance_benchmark.csv", index=False)
    print(S.round(3).to_string(index=False))
    print("\n  NOTE: the SIPP figure is WORKING-CORE households only, so part of each gap is "
          "coverage\n  rather than under-reporting. The scaling factor is an upper bound on "
          "under-reporting.")

    # ---- rerun the credit rows on BENCHMARKED balances, caps removed ----
    FED_LOSSES = {"mortgage": 22.5, "card": 203.0, "auto": 54.1, "student": 54.1}
    FED_BAL = {"mortgage": 1500.0, "card": 1187.1, "auto": 741.1, "student": 741.1}
    LGD = {"mortgage": (0.25, 0.40), "card": (0.80, 1.00),
           "auto": (0.45, 0.65), "student": (0.75, 1.00)}
    # CORRECTED, item 2 of the final session. A80's scaling factor divided the official
    # aggregate by the WORKING-CORE balance, which conflates survey under-reporting with
    # sample coverage. The survey correction is the official aggregate over the FULL SIPP
    # household universe; the working-core share is a coverage fact and is not a scaling.
    urp = OUT / "under_reporting_factors.csv"
    if urp.exists():
        ur = pd.read_csv(urp)
        sf = {r["loan"]: r["UNDER_REPORTING_factor"] for _, r in ur.iterrows()}
        print("\n  USING CORRECTED FULL-UNIVERSE UNDER-REPORTING FACTORS: "
              + ", ".join(f"{k} {v:.3f}" for k, v in sf.items()))
    else:
        sf = {r["loan"]: r["scaling_factor"] for _, r in S.iterrows()}
    rows2 = []
    for _, h in hc.iterrows():
        ln = h["loan"]
        if ln not in sf:
            continue
        ead = h["exposure_at_default_bn"] * sf[ln]
        lo, hi = LGD[ln]
        agg = AGG[ln]["value"]
        bank_share = min(FED_BAL[ln] / agg, 1.0)
        rows2.append({"share_of_wage_bill": h["share_of_wage_bill"], "loan": ln,
                      "scaling_factor": sf[ln],
                      "benchmarked_ead_bn": ead,
                      "bank_share": bank_share,
                      "bank_loss_lo_bn": ead * lo * bank_share,
                      "bank_loss_hi_bn": ead * hi * bank_share,
                      "pct_of_fed_lo": 100 * ead * lo * bank_share / FED_LOSSES[ln],
                      "pct_of_fed_hi": 100 * ead * hi * bank_share / FED_LOSSES[ln]})
    B2 = pd.DataFrame(rows2)
    B2.round(3).to_csv(OUT / "credit_benchmarked.csv", index=False)
    print("\n=== CREDIT ROWS ON BENCHMARKED BALANCES, caps removed, bank-held basis ===")
    print(B2[["share_of_wage_bill", "loan", "scaling_factor", "bank_share",
              "bank_loss_lo_bn", "bank_loss_hi_bn", "pct_of_fed_lo",
              "pct_of_fed_hi"]].round(2).to_string(index=False))
    print("\n=== CROSSING THE 25 PERCENT THRESHOLD after benchmarking ===")
    for ln in ["mortgage", "student", "auto", "card"]:
        s2 = B2[B2.loan == ln].sort_values("share_of_wage_bill")
        cr = s2[s2.pct_of_fed_hi >= 25]
        if len(cr):
            f0 = cr.iloc[0]
            print(f"  {ln:9s} crosses at {f0.share_of_wage_bill:.0%} "
                  f"({f0.pct_of_fed_lo:.0f} to {f0.pct_of_fed_hi:.0f} percent of the Fed loss)")
        else:
            print(f"  {ln:9s} NEVER crosses (max {s2.pct_of_fed_hi.max():.1f} percent)")

    (OUT / "trust_fund_benchmark_summary.json").write_text(json.dumps({
        "oasdi_cap_2026": OASDI_CAP_2026,
        "cap_source": "The Tax Adviser, AICPA, 24 October 2025, reporting the SSA "
                      "announcement. SSA.gov returns HTTP 403 to this environment.",
        "payroll_share_of_oasdi_income": PAYROLL_SHARE_OASDI,
        "taxable_shares": {g: acc[g]["taxable"] / acc[g]["wage"] for g in acc},
        "max_trust_fund_pct": float(mx),
        "bound_respected": bool(mx <= 100),
        "aggregates": AGG,
        "scaling": S.round(4).to_dict("records") if len(S) else [],
    }, indent=2))


if __name__ == "__main__":
    main()
