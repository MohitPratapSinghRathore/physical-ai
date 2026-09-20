"""B11 (the two-sided bet, by holder) and B12 (the payoff table across AI outcomes).

PROVISIONAL throughout. The AI EQUITY SCALE is a SCENARIO parameter and is labelled as
one everywhere: no filing discloses an AI-attributable market value, so the AI share of
US nonfinancial corporate equity is swept over a stated grid rather than asserted. Every
dollar figure on the AI DEBT side is sourced.

B11 asks whether the federal government is the least hedged holder in the economy: it
holds or owes the majority of the wage leg, and its only claim on the AI leg is tax at
the operative effective rate.

B12 asks what each holder gains or loses in three states of the world, and uses two
MEASURED historical anchors rather than cited ones: the 2000 to 2002 equity-financed
bust and the 2008 debt-financed crisis, both rebuilt here from Z.1 and NIPA series
already in the repository.

PLAUSIBILITY BOUNDS: holder shares sum to 1 within each leg; every share in [0, 1]; the
hedge ratio at the break-even capital tax rate is 1 by construction for case A, which is
an internal check on the whole calculation and is asserted as such.
"""
import io, json, pathlib, sys, zipfile
import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
ROOT = HERE.parents[1]
PROC = ROOT / "data" / "processed"
FRED = ROOT / "data" / "raw" / "fred"

import config as C
from z1_loader import load_all, annual, catalog

# --------------------------------------------------------------------------- sourced
# Chicago Fed, verified in A45 against the publisher page: Cohen, Killen and Lau, "Tail
# Risk for Banks Posed by Investments in Generative Artificial Intelligence", Chicago Fed
# Insights, February 2026. A SECONDARY source reporting supervisory data.
CHICAGO_FED = dict(
    large_bank_ci_commitments_ai_bn=450.0,
    large_bank_ci_commitments_ai_share_of_total=0.13,
    commitments_2015_bn=250.0, commitments_2015_share=0.09,
    outstanding_share_of_bank_total_assets=0.008,
    outstanding_share_of_tier1=0.09,
    committed_share_of_tier1=0.25,
    software_commitments_bn=191.0,
    energy_and_semis_commitments_bn=275.0,
    software_rated_b_and_below_bn=50.0,
    energy_semis_rated_b_and_below_bn=15.0,
    source="Chicago Fed Insights, February 2026, verified A45")

# SCENARIO grid for the AI share of US nonfinancial corporate equity market value.
# NOT a measurement. No filing discloses an AI-attributable market value.
AI_EQUITY_SHARE_GRID = [0.10, 0.20, 0.30]
AI_EQUITY_SHARE_CENTRAL = 0.20

TAU_K_OPERATIVE = 0.0708          # claim 53, standing, independently confirmed
TAU_K_SOURCED_MAX = 0.20351       # top of the sourced effective range
PV_HORIZON, PV_RATE = 10, 0.03    # the project's present value convention


def ann(path, sid):
    d = pd.read_csv(path / f"{sid}.csv")
    d.columns = [c.strip() for c in d.columns]
    dc, vc = d.columns[0], d.columns[1]
    d[dc] = pd.to_datetime(d[dc])
    d[vc] = pd.to_numeric(d[vc], errors="coerce")
    return d.dropna(subset=[vc]).groupby(d[dc].dt.year)[vc].mean()


def dfa():
    z = zipfile.ZipFile(HERE / "_dfa_cache.zip")
    d = pd.read_csv(io.BytesIO(z.read("dfa-networth-levels.csv")))
    d["year"] = d["Date"].str[:4].astype(int)
    d["q"] = d["Date"].str[-1].astype(int)
    return d


def annuity(r, n):
    return (1 - (1 + r) ** -n) / r


def main():
    A = load_all()
    cat = catalog()
    H = pd.read_csv(HERE / "holder_matrix_latest.csv")
    summ = json.loads((HERE / "direct_ratio_latest.json").read_text())
    legA = pd.read_csv(PROC / "legA_tier2.csv")
    cases = pd.read_csv(PROC / "cases_A_and_B.csv")
    sov = pd.read_csv(PROC / "sovereign_consolidation.csv")
    D = dfa()

    # =================================================== B11: the two legs by holder
    # --- wage leg: labour-backed claims, by ultimate holder, PLUS the obligor leg
    wage_holder = H.groupby("holder")["labour_backed_bn"].sum()
    wage_total = float(wage_holder.sum())
    sov_ex = summ["sovereign_exposure"]

    # --- AI leg
    # equity: held in the same proportions as US nonfinancial corporate equity.
    # FLAGGED: AI-capital firms are mega-cap index constituents, so the household,
    # mutual fund and rest-of-world shares are probably HIGHER than the aggregate.
    sys.path.insert(0, str(HERE))
    from build_direct import holder_shares
    eq_shares, _ = holder_shares(A, cat, "3064105", summ["latest_year"])
    bond_shares, _ = holder_shares(A, cat, "3063005", summ["latest_year"])
    nfc_equity_bn = float(
        annual(A[[k for k in A if k.startswith("LM103164105")][0]])[summ["latest_year"]]) / 1000.0

    ai_debt_onbs_bn = float(legA["lt_debt"].sum() + legA["fin_lease"].sum())
    ai_bank_commit_bn = CHICAGO_FED["large_bank_ci_commitments_ai_bn"]

    rows = []
    for share in AI_EQUITY_SHARE_GRID:
        ai_equity_bn = nfc_equity_bn * share
        legs = {}
        for h in C.HOLDER_CLASSES:
            eq = ai_equity_bn * (0.0 if np.isnan(eq_shares[h]) else eq_shares[h])
            bd = ai_debt_onbs_bn * (0.0 if np.isnan(bond_shares[h]) else bond_shares[h])
            bk = ai_bank_commit_bn if h == "banks" else 0.0
            legs[h] = eq + bd + bk
        tot = sum(legs.values())
        for h in C.HOLDER_CLASSES:
            rows.append(dict(ai_equity_share_scenario=share, holder=h,
                             ai_leg_bn=round(legs[h], 1),
                             ai_leg_share=round(legs[h] / tot, 6),
                             wage_leg_bn=round(float(wage_holder.get(h, 0.0)), 1),
                             wage_leg_share=round(float(wage_holder.get(h, 0.0)) / wage_total, 6)))
    B11 = pd.DataFrame(rows)
    B11["overlap_min_share"] = B11[["ai_leg_share", "wage_leg_share"]].min(axis=1).round(6)
    B11.to_csv(HERE / "two_sided_bet_by_holder.csv", index=False)

    # --- the government's implicit claim on the AI leg
    gov = []
    for _, c in cases.iterrows():
        et, dose = c["exposure_type"], float(c["dose"])
        s = sov[(sov.exposure_type == et) & (sov.dose == dose)]
        if s.empty:
            continue
        fed_loss = float(s.iloc[0]["federal_first_round_bn"])
        # The PUBLISHED fiscal loss is already NET of capital tax at the OPERATIVE
        # rate (claim 179: the loss nets out tau_k). Measuring how much a capital tax
        # hedges against that net figure double counts the tax. The GROSS loss, before
        # any capital tax, is the right denominator, and on it the break-even rate
        # recovers exactly 100 percent by construction, which is the internal check.
        fiscal_loss = {"A": float(c["case_A_fiscal_loss_bn"]),
                       "B": float(c["case_B_fiscal_loss_bn"])}
        gross_fiscal = {k: fiscal_loss[k] + TAU_K_OPERATIVE * float(c[col])
                        for k, col in [("A", "case_A_surplus_bn"),
                                       ("B", "case_B_surplus_bn")]}
        gross_federal = fed_loss + TAU_K_OPERATIVE * float(c["case_A_surplus_bn"])
        for case, surplus_col, be_col in [("A", "case_A_surplus_bn", "case_A_break_even_tau_k"),
                                          ("B", "case_B_surplus_bn", "case_B_break_even_tau_k")]:
            S = float(c[surplus_col])
            be = float(c[be_col])
            for label, tau in [("operative_0.0708", TAU_K_OPERATIVE),
                               ("sourced_max_0.20351", TAU_K_SOURCED_MAX),
                               ("break_even", be)]:
                claim_flow = tau * S
                gov.append(dict(
                    exposure_type=et, dose=dose, case=case, tau_k_label=label,
                    tau_k=round(tau, 6), surplus_bn=round(S, 1),
                    gov_capital_tax_claim_annual_bn=round(claim_flow, 1),
                    gov_capital_tax_claim_pv_bn=round(
                        claim_flow * annuity(PV_RATE, PV_HORIZON), 1),
                    federal_first_round_loss_bn=round(fed_loss, 1),
                    federal_loss_pv_bn=round(fed_loss * annuity(PV_RATE, PV_HORIZON), 1),
                    fiscal_loss_net_of_operative_tax_bn=round(fiscal_loss[case], 1),
                    gross_fiscal_loss_bn=round(gross_fiscal[case], 1),
                    gross_federal_first_round_loss_bn=round(gross_federal, 1),
                    share_of_gross_fiscal_loss_hedged=round(
                        claim_flow / gross_fiscal[case], 6) if gross_fiscal[case] > 0 else np.nan,
                    share_of_wage_leg_loss_hedged=round(claim_flow / gross_federal, 6)
                    if gross_federal > 0 else np.nan,
                    inside_observed_data_range=bool(c["inside_observed_data_range"])))
    G = pd.DataFrame(gov)
    G.to_csv(HERE / "government_claim_on_ai_leg.csv", index=False)

    # =================================================== B12: the payoff table
    # --- measured historical anchors
    eq_ser = annual(A[[k for k in A if k.startswith("LM103164105")][0]]) / 1000.0
    receipts, ctax = ann(FRED, "FGRECPT"), ann(FRED, "FCTAX")
    gdp = ann(FRED, "GDP")
    anchors = []
    for name, pk, tr in [("2000_to_2002_equity_financed", 2000, 2002),
                         ("2007_to_2009_debt_financed", 2007, 2009)]:
        d = dict(anchor=name, peak_year=pk, trough_year=tr)
        d["nfc_equity_peak_bn"] = round(float(eq_ser[pk]), 1)
        d["nfc_equity_trough_bn"] = round(float(eq_ser[tr]), 1)
        d["nfc_equity_fall_pct"] = round(100 * (eq_ser[tr] / eq_ser[pk] - 1), 2)
        # explicit boolean masks: integer-index slicing is ambiguous and silently
        # returned an empty window here
        def window(s):
            return s[(s.index >= pk) & (s.index <= tr)]
        rp = window(receipts)
        d["federal_receipts_peak_bn"] = round(float(receipts.loc[pk]), 1)
        d["federal_receipts_trough_bn"] = round(float(rp.min()), 1)
        d["federal_receipts_fall_pct"] = round(100 * (rp.min() / receipts.loc[pk] - 1), 2)
        cp = window(ctax)
        d["corporate_tax_peak_bn"] = round(float(ctax.loc[pk]), 1)
        d["corporate_tax_trough_bn"] = round(float(cp.min()), 1)
        d["corporate_tax_fall_pct"] = round(100 * (cp.min() / ctax.loc[pk] - 1), 2)
        d["gdp_peak_bn"] = round(float(gdp[pk]), 1)
        d["equity_fall_pct_of_gdp"] = round(
            100 * (eq_ser[tr] - eq_ser[pk]) / gdp[pk], 1)
        dd = D[(D["year"].isin([pk, tr])) & (D["q"] == 4)]
        if len(dd):
            # the DFA is in MILLIONS of dollars, so one division by 1e6 gives trillions
            hw = dd.groupby("year")["Corporate equities and mutual fund shares"].sum() / 1e6
            if pk in hw.index and tr in hw.index:
                d["household_equity_peak_tn"] = round(float(hw[pk]), 2)
                d["household_equity_trough_tn"] = round(float(hw[tr]), 2)
                d["household_equity_fall_pct"] = round(100 * (hw[tr] / hw[pk] - 1), 2)
        anchors.append(d)
    AN = pd.DataFrame(anchors)
    AN.to_csv(HERE / "historical_anchors.csv", index=False)

    # --- financing structure of AI capex, from the filings in the repository
    lg = legA.dropna(subset=["capex"]).copy()
    lg["debt_financed_capex_bn"] = (lg["capex"] - lg["ocf"]).clip(lower=0)
    fin = dict(
        n_companies=int(len(lg)),
        total_capex_bn=round(float(lg["capex"].sum()), 1),
        total_ocf_bn=round(float(lg["ocf"].sum()), 1),
        aggregate_self_funding_ratio=round(float(lg["ocf"].sum() / lg["capex"].sum()), 4),
        capex_in_excess_of_ocf_bn=round(float(lg["debt_financed_capex_bn"].sum()), 1),
        debt_financed_share_of_capex=round(
            float(lg["debt_financed_capex_bn"].sum() / lg["capex"].sum()), 6),
        companies_with_capex_above_ocf=sorted(
            lg[lg["self_funding_ratio"] < 1]["ticker"].tolist()),
        by_company={r.ticker: dict(self_funding_ratio=float(r.self_funding_ratio),
                                   capex_bn=float(r.capex), ocf_bn=float(r.ocf))
                    for r in lg.itertuples()},
        reading="In AGGREGATE the named AI capital spenders fund capex out of operating "
                "cash flow, which is the 2000 structure and not the 2008 structure. The "
                "marginal dollar is not: Oracle, CoreWeave and the two data centre REITs "
                "all spend above operating cash flow, and the Chicago Fed commitments and "
                "the off-balance-sheet vehicles sit outside these filings entirely.")
    fin["off_balance_sheet"] = ("NOT SOURCED. BIS Quarterly Review March 2026 documents "
                                "SPV and lease structures as the dominant data centre "
                                "financing form; no dollar total is carried here because "
                                "none was verified. Any failure-state figure below is a "
                                "LOWER BOUND for that reason.")

    # --- household split by wealth percentile, latest
    last = D[D["Date"] == D["Date"].max()]
    hh = {}
    for _, r in last.iterrows():
        tot_eq = float(last["Corporate equities and mutual fund shares"].sum())
        tot_mt = float(last["Home mortgages"].sum() + last["Consumer credit"].sum())
        hh[r["Category"]] = dict(
            equity_share=round(float(r["Corporate equities and mutual fund shares"]) / tot_eq, 6),
            household_debt_share=round(
                float(r["Home mortgages"] + r["Consumer credit"]) / tot_mt, 6),
            equity_bn=round(float(r["Corporate equities and mutual fund shares"]) / 1e3, 1),
            household_debt_bn=round(float(r["Home mortgages"] + r["Consumer credit"]) / 1e3, 1))
    ratio = {k: round(v["equity_share"] / v["household_debt_share"], 3) for k, v in hh.items()}

    # --- the payoff table
    central = B11[B11.ai_equity_share_scenario == AI_EQUITY_SHARE_CENTRAL].set_index("holder")
    gsel = G[(G.tau_k_label == "operative_0.0708") & (G.case == "A") & (G.dose == 0.10)]
    hedge_operative = float(gsel["share_of_wage_leg_loss_hedged"].mean())
    gsel_be = G[(G.tau_k_label == "break_even") & (G.case == "A") & (G.dose == 0.10)]
    hedge_be = float(gsel_be["share_of_wage_leg_loss_hedged"].mean())

    pay = []
    for h in C.HOLDER_CLASSES:
        if h == "residual_unallocated":
            continue
        w = float(central.loc[h, "wage_leg_share"])
        a = float(central.loc[h, "ai_leg_share"])
        pay.append(dict(
            holder=h, wage_leg_share=round(w, 4), ai_leg_share=round(a, 4),
            state_failure="loss on the AI leg, sized by ai_leg_share; wage leg broadly "
                          "unharmed because no displacement occurs",
            state_partial="loss on the WAGE leg with little offsetting AI surplus; the "
                          "worst state for any holder whose wage_leg_share exceeds its "
                          "ai_leg_share",
            state_success="gain on the AI leg, sized by ai_leg_share, against a wage leg "
                          "loss sized by wage_leg_share",
            net_position_partial=round(a - w, 4),
            hedged_ratio_ai_over_wage=round(a / w, 3) if w > 0 else np.nan))
    P12 = pd.DataFrame(pay).sort_values("wage_leg_share", ascending=False)
    P12.to_csv(HERE / "payoff_table_by_holder.csv", index=False)

    # =================================================== summary and bounds
    fed_ai = float(central.loc["federal_government", "ai_leg_share"])
    fed_wage_holder = float(central.loc["federal_government", "wage_leg_share"])
    out = dict(
        status="PROVISIONAL. AI equity SCALE is SCENARIO; AI debt and bank commitments "
               "are sourced; off-balance-sheet financing is NOT sourced and every "
               "failure-state figure is a LOWER BOUND.",
        latest_year=summ["latest_year"],
        wage_leg=dict(labour_backed_bn=wage_total,
                      by_holder_share={k: round(float(v) / wage_total, 6)
                                       for k, v in wage_holder.items()},
                      sovereign_union_share=sov_ex["share_union"],
                      sovereign_held_or_guaranteed_share=sov_ex["share_held_or_guaranteed"],
                      sovereign_obligor_share=sov_ex["share_obligor"]),
        ai_leg=dict(
            equity_scale_is_scenario=True,
            ai_equity_share_grid=AI_EQUITY_SHARE_GRID,
            ai_equity_share_central=AI_EQUITY_SHARE_CENTRAL,
            nonfinancial_corporate_equity_bn=round(nfc_equity_bn, 1),
            ai_equity_central_bn=round(nfc_equity_bn * AI_EQUITY_SHARE_CENTRAL, 1),
            ai_onbalancesheet_debt_bn=round(ai_debt_onbs_bn, 1),
            ai_bank_commitments_bn=ai_bank_commit_bn,
            chicago_fed=CHICAGO_FED,
            federal_share_of_ai_leg=fed_ai),
        government_implicit_claim=dict(
            tau_k_operative=TAU_K_OPERATIVE, tau_k_sourced_max=TAU_K_SOURCED_MAX,
            pv_horizon_years=PV_HORIZON, pv_rate=PV_RATE,
            share_of_federal_wage_loss_hedged_at_operative_10pct_dose=round(hedge_operative, 4),
            share_of_federal_wage_loss_hedged_at_break_even_10pct_dose=round(hedge_be, 4)),
        financing_structure=fin,
        households_by_wealth_percentile=hh,
        equity_share_over_debt_share=ratio,
        B11_verdict=None, B12_verdict=None)

    # B11 test
    out["B11_verdict"] = dict(
        claim="The federal government holds or owes the majority of the wage leg and a "
              "negligible share of the AI leg, so it is the least hedged holder.",
        federal_wage_leg_union_share=sov_ex["share_union"],
        federal_ai_leg_share=fed_ai,
        federal_ai_leg_claim_is_tax_only=True,
        hedge_ratio_ai_over_wage=round(fed_ai / sov_ex["share_union"], 4),
        verdict="CONFIRMED" if (sov_ex["share_union"] > 0.5 and fed_ai < 0.05) else "REFUTED")
    # B12 test
    fed_row = P12[P12.holder == "federal_government"].iloc[0]
    out["B12_verdict"] = dict(
        claim="The federal government loses in all three states and holds almost none of "
              "the upside in the success state.",
        failure_state="loses: receipts fall. MEASURED anchors, corporate tax receipts fell "
                      f"{AN.loc[0,'corporate_tax_fall_pct']} percent after 2000 and "
                      f"{AN.loc[1,'corporate_tax_fall_pct']} percent after 2007",
        partial_state=f"loses: wage leg share {fed_row.wage_leg_share}, AI leg share "
                      f"{fed_row.ai_leg_share}, net {fed_row.net_position_partial}",
        success_state=f"loses on the wage leg and recovers only {hedge_operative:.1%} of "
                      f"that loss through capital tax at the operative rate",
        verdict="CONFIRMED" if (hedge_operative < 1.0 and fed_ai < 0.05) else "REFUTED")
    (HERE / "two_sided_bet.json").write_text(json.dumps(out, indent=1, default=str))

    checks = []

    def chk(n, ok, d):
        checks.append(dict(check=n, verdict="OK" if ok else "VIOLATION", detail=d))

    for s, g in B11.groupby("ai_equity_share_scenario"):
        chk(f"AI leg shares sum to 1 (scenario {s})", abs(g.ai_leg_share.sum() - 1) < 1e-5,
            f"{g.ai_leg_share.sum():.8f}")
        chk(f"wage leg shares sum to 1 (scenario {s})", abs(g.wage_leg_share.sum() - 1) < 1e-5,
            f"{g.wage_leg_share.sum():.8f}")
        chk(f"all shares in [0,1] (scenario {s})",
            bool(((g.ai_leg_share.between(0, 1)) & (g.wage_leg_share.between(0, 1))).all()), "")
    be = G[(G.tau_k_label == "break_even") & (G.case == "A")]
    chk("break-even rate exactly covers the GROSS fiscal loss by construction, case A",
        bool(np.allclose(be["share_of_gross_fiscal_loss_hedged"], 1.0, atol=0.02)),
        f"mean {be['share_of_gross_fiscal_loss_hedged'].mean():.4f}")
    chk("DFA equity shares sum to 1",
        abs(sum(v["equity_share"] for v in hh.values()) - 1) < 1e-5, "")
    chk("DFA household debt shares sum to 1",
        abs(sum(v["household_debt_share"] for v in hh.values()) - 1) < 1e-5, "")
    chk("debt-financed share of AI capex in [0,1]",
        0 <= fin["debt_financed_share_of_capex"] <= 1,
        f"{fin['debt_financed_share_of_capex']:.4f}")
    chk("both anchors show a fall in corporate tax receipts",
        bool((AN["corporate_tax_fall_pct"] < 0).all()),
        AN["corporate_tax_fall_pct"].tolist())
    Pc = pd.DataFrame(checks).sort_values("verdict")
    Pc.to_csv(HERE / "plausibility_ai_leg.csv", index=False)

    print("=== B11 two-sided bet, AI equity share scenario "
          f"{AI_EQUITY_SHARE_CENTRAL:.0%} ===")
    print(central[["wage_leg_share", "ai_leg_share"]].sort_values(
        "wage_leg_share", ascending=False).to_string())
    print(f"\nfederal wage leg UNION share   {sov_ex['share_union']:.4f}")
    print(f"federal AI leg share           {fed_ai:.4f}")
    print(f"B11 verdict                    {out['B11_verdict']['verdict']}")
    print(f"\nhedged at operative tau_k      {hedge_operative:.2%} of the federal wage loss")
    print(f"hedged at break-even tau_k     {hedge_be:.2%}")
    print(f"B12 verdict                    {out['B12_verdict']['verdict']}")
    print(f"\ndebt-financed share of AI capex {fin['debt_financed_share_of_capex']:.3f}"
          f"  (below OCF: {fin['companies_with_capex_above_ocf']})")
    print("\n=== measured historical anchors ===")
    print(AN[["anchor", "nfc_equity_fall_pct", "federal_receipts_fall_pct",
              "corporate_tax_fall_pct", "equity_fall_pct_of_gdp"]].to_string(index=False))
    print(f"\nplausibility: {len(Pc)} checks, {(Pc.verdict=='VIOLATION').sum()} violations")
    if (Pc.verdict == "VIOLATION").any():
        print(Pc[Pc.verdict == "VIOLATION"].to_string(index=False))


if __name__ == "__main__":
    main()
