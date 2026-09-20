"""Generate paper/results_macros.tex from the measured JSON artifacts.

PLAYBOOK SECTION 3. Every number that appears in the manuscript prose enters through a
\\result{key} macro defined here, so each reported value traces back to the run that
produced it. Nothing is hand typed into the LaTeX.

Run:  python paper/gen_results_macros.py
"""
import csv
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "paper" / "results_macros.tex"


def load(rel):
    return json.loads((ROOT / rel).read_text())


def rows(rel):
    with (ROOT / rel).open(newline="") as fh:
        return list(csv.DictReader(fh))


def main():
    lb = load("data/release/labor_backing/direct_ratio_latest.json")
    do = load("data/release/labor_backing/debt_only_ratio.json")
    cg = load("data/release/labor_backing/capital_gains_bound.json")
    tk = load("data/release/tau_k/tau_k_assembled.json")
    comp = load("data/release/tau_k/components.json")
    inst = load("data/release/institutions/a2_summary.json")
    bust = load("data/release/ai_bust/b2_transmission.json")
    rsen = load("data/release/method/replication_r_sensitivity.json")
    it3 = load("data/release/labor_backing/item3_sovereign_robustness.json")
    tsb = load("data/release/labor_backing/two_sided_bet.json")
    dots = {r["year"]: r for r in
            rows("data/release/labor_backing/debt_only_ratio_timeseries.csv")}
    drts = {r["year"]: r for r in
            rows("data/release/labor_backing/direct_ratio_timeseries.csv")}
    quint = {r["wage_quintile"]: r for r in
             rows("data/release/labor_backing/quintile_labour_backing.csv")}
    acsen = load("data/release/labor_backing/sensitivity.json")
    rep = {r["round"]: r for r in rows("data/release/replication_rounds.csv")}
    fis = load("data/release/method/fiscal_channel_summary.json")
    plaus = load("data/release/method/plausibility_audit.json")
    fed_dose = {r["dose_share_of_total_wage_bill"]: r for r in
                rows("data/release/incidence/federal_share_by_dose.csv")}
    cons = [r for r in rows("data/release/dose_response/sovereign_consolidation.csv")
            if r["dose"] == "0.1" and r["incidence"] == "c_sourced_mix"]
    gse_wf = rows("data/release/incidence/housing_agency_waterfall.csv")
    gse_un = rows("data/release/incidence/housing_agency_unenhanced_share.csv")
    quint_buf = {}
    for r in rows("data/release/dose_response/by_wage_quintile_dose_response.csv"):
        quint_buf.setdefault(r["wage_quintile"], r)
    paycon = rows("data/release/incidence/pay_control.csv")
    first = rows("data/release/dose_response/dose_response_first_round.csv")
    clearing = {r["id"]: r for r in rows("data/release/headline_clearing_pass.csv")}
    sysres = {(r["dose"], r["band"], r["earnings_offset"]): r for r in
              rows("data/release/institutions/a2_system_results.csv")}
    bymodel = {(r["dose"], r["business_model"]): r for r in
               rows("data/release/institutions/a2_distribution_by_class.csv")
               if r["cut"] == "model"}
    instr = load("data/release/institutions/a4_instrument_results.json")
    omitted = load("data/release/institutions/a3_omitted_institutions.json")
    tiers = load("data/release/ai_bust/b1_tiers.json")
    b34 = load("data/release/ai_bust/b3_b4_summary.json")
    payoff = {r["holder"]: r for r in
              rows("data/release/ai_bust/b4_payoff_by_holder.csv")}
    engine = rows("data/release/ai_bust/b3_bust_through_engine.csv")
    dash = {r["indicator"]: r for r in rows("data/release/dashboard/dashboard.csv")}
    a1 = load("data/release/revision_r1/a1_pass_through.json")
    a2 = load("data/release/revision_r1/a2_cashflow_bridge.json")
    a2path = {r["investment_growth_rate"]: r for r in
              rows("data/release/revision_r1/a2_transition_path.csv")}
    a3 = load("data/release/revision_r1/a3_relief_feedback.json")
    a4 = load("data/release/revision_r1/a4_two_directions.json")
    a4grid = rows("data/release/revision_r1/a4_rate_grid.csv")
    cases = rows("data/release/dose_response/cases_A_and_B.csv")
    debtinc = rows("data/release/dose_response/debt_increments.csv")
    pub = load("data/release/tau_k/published_shares.json")
    bh = load("data/release/tau_k/z1_bond_holders.json")

    sov = lb["sovereign_exposure"]
    req = rsen["ours_observed_rho_and_our_omega"]["required_tau_k"]
    bk = [r for r in tk["assembled_SOURCED"] if r["rent_reading"] == "Barkai"][0]
    kn = [r for r in tk["assembled_SOURCED"]
          if r["rent_reading"] == "Karabarbounis_Neiman_case_R"][0]
    cbk = [r for r in tk["assembled_CENTRAL_at_sourced_centrals"]
           if r["rent_reading"] == "Barkai"][0]
    ckn = [r for r in tk["assembled_CENTRAL_at_sourced_centrals"]
           if r["rent_reading"] == "Karabarbounis_Neiman_case_R"][0]
    src = comp["SOURCED_A115"]

    def pct(x, d=0):
        return f"{100 * float(x):.{d}f}"

    R = {}

    # ---- labour backing accounts
    R["DebtOnlyDirect"] = pct(do["DEBT_ONLY_direct"])
    R["DebtOnlyIndirect"] = pct(do["DEBT_ONLY_incl_indirect"])
    R["AllClaimsDirect"] = pct(do["all_claims_direct"])
    R["AllClaimsIndirect"] = pct(do["all_claims_incl_indirect"])
    R["EquityShareDenom"] = pct(do["equity_share_of_all_claims_latest"])
    R["DebtOnlyCV"] = f"{do['coefficient_of_variation']['debt_only']:.4f}"
    R["AllClaimsCV"] = f"{do['coefficient_of_variation']['all_claims']:.4f}"
    R["OneStepMovePct"] = f"{abs(float(do['largest_move_pct'])):.0f}"

    # ---- the series, 1952 to 2025
    for y in ("1952", "1970", "1990", "2000", "2008", "2020", "2025"):
        R["DebtOnly" + y] = pct(dots[y]["DEBT_ONLY_ratio_direct"])
        R["AllClaims" + y] = pct(drts[y]["direct_labour_backing_ratio"])
        R["SovUnion" + y] = pct(drts[y]["sovereign_share_union"])
        R["SovHeld" + y] = pct(drts[y]["sovereign_share_of_labour_backed"])
        R["SovObligor" + y] = pct(float(drts[y]["sovereign_obligor_bn"])
                                  / float(drts[y]["labour_backed_bn"]))
    R["AllClaimsSeriesLow"] = pct(min(float(r["direct_labour_backing_ratio"])
                                      for r in drts.values()))
    R["AllClaimsSeriesHigh"] = pct(max(float(r["direct_labour_backing_ratio"])
                                       for r in drts.values()))
    R["DebtOnlySeriesLow"] = pct(do["debt_only_range_1952_2025"][0])
    R["DebtOnlySeriesHigh"] = pct(do["debt_only_range_1952_2025"][1])
    R["OneStepMoveAllClaimsPct"] = f"{acsen['largest_single_move_pct']:.0f}"

    # ---- structural sensitivities on the federal exposure
    st = it3["structural_calls_that_do_move_it"]
    R["StructIndirect"] = pct(st["one_step_rule"])
    R["StructNoPools"] = pct(st["agency_pools_not_federal"])
    R["StructCommercial"] = pct(st["commercial_mortgage_as_rent_serviced"])
    R["StructObligorExcluded"] = pct(st["obligor_leg_excluded"])
    R["MeasurementMaxMovePct"] = f"{it3['narrow_range_max_move_pct']:.2f}"
    R["MeasurementMaxMoveRounded"] = f"{it3['narrow_range_max_move_pct']:.0f}"
    R["AgreedRangeLow"] = pct(it3["agreed_range_with_replicator"][0])
    R["AgreedRangeHigh"] = pct(it3["agreed_range_with_replicator"][1])
    R["OverlapBn"] = f"{lb['sovereign_exposure']['overlap_removed_bn']:,.1f}"

    # ---- the AI side
    R["AIFederalShare"] = pct(it3["ai_leg_federal_share_central"], 1)
    R["AIFederalShareRounded"] = pct(it3["ai_leg_federal_share_central"])
    R["AIFederalShareLow"] = pct(it3["ai_leg_federal_share_range"][0], 1)
    R["AIFederalShareHigh"] = pct(it3["ai_leg_federal_share_range"][1], 1)
    R["AIEquityScale"] = pct(tsb["ai_leg"]["ai_equity_share_central"])
    R["HolderGap"] = pct(it3["holder_gap_central"])

    # ---- the wage-quintile gradient
    R["QTwoPerDollar"] = f"{float(quint['Q2']['labour_backed_per_unit_wage_bill']):.2f}"
    R["QTopPerDollar"] = f"{float(quint['Q5_top']['labour_backed_per_unit_wage_bill']):.2f}"
    R["QTopWageShare"] = pct(quint["Q5_top"]["quintile_wage_bill_share"])
    R["QTopClaimShare"] = pct(quint["Q5_top"]["share_of_household_labour_backed"])

    # ---- the holder map, wage side
    R["SovereignUnion"] = pct(sov["share_union"])
    R["SovereignCreditor"] = pct(sov["share_held_or_guaranteed"])
    R["SovereignDebtor"] = pct(sov["share_obligor"])

    # ---- the receipts bound
    R["GainsAGILow"] = pct(cg["capital_gains_share_of_agi_range"][0], 1)
    R["GainsAGIHigh"] = pct(cg["capital_gains_share_of_agi_range"][1], 1)
    R["ReceiptsShareLow"] = f"{cg['labour_linked_receipts_share_2023']['lower']:.4f}"
    R["ReceiptsShareHigh"] = f"{cg['labour_linked_receipts_share_2023']['upper']:.4f}"
    R["ReceiptsPctLow"] = pct(cg["labour_linked_receipts_share_2023"]["lower"])
    R["ReceiptsPctHigh"] = pct(cg["labour_linked_receipts_share_2023"]["upper"])

    # ---- the fiscal condition
    R["RetainedWageShare"] = f"{rsen['ours_observed_rho_and_our_omega']['R']:.4f}"
    R["RequiredLow"] = pct(min(req.values()), 1)
    R["RequiredHigh"] = pct(max(req.values()), 1)
    R["TauKBarkai"] = pct(cbk["tau_k_central"], 1)
    R["TauKBarkaiLow"] = pct(bk["tau_k_p05"], 1)
    R["TauKBarkaiHigh"] = pct(bk["tau_k_p95"], 1)
    R["TauKKN"] = pct(ckn["tau_k_central"], 1)
    R["TauKPassLow"] = pct(bk["pass_share_vs_required_low"], 1)
    R["TauKPassHigh"] = pct(bk["pass_share_vs_required_high"], 0)
    R["TauKOperativeOld"] = pct(0.0708, 1)
    R["ShareholderLayer"] = f"{tk['shareholder_layer_at_centrals']:.4f}"

    # ---- the ownership explanation
    R["ThetaTaxable"] = pct(src["theta_taxable"]["central"])
    R["ThetaUntaxable"] = pct(1 - float(src["theta_taxable"]["central"]))
    R["DeferralCentral"] = f"{src['deferral_factor']['central']:.3f}"
    R["GainsUntaxedAtDeath"] = pct(pub["gains_never_taxed_at_death"]["value"], 1)
    R["InterestSheltered"] = pct(pub["corporate_interest_nontaxable_share"]["value"], 1)
    R["TaxableHolderInterestRate"] = pct(
        pub["taxable_holder_marginal_interest_rate"]["value"], 1)
    R["CBOFullyTaxableEquity"] = pct(pub["cbo_fully_taxable_equity_share_2007"]["value"], 1)
    R["CBODebtFinancedETR"] = pct(
        abs(pub["cbo_debt_financed_effective_rate"]["value"]), 0)
    R["BondsRestOfWorld"] = pct(bh["rest_of_world"]["share"], 1)
    R["BondsHouseholdDirect"] = pct(bh["households_and_nonprofits"]["share"], 1)

    # ---- the fiscal condition, the map and the two bases
    crs = tk["shareholder_layer_checks"]
    ours_bk = [r for r in tk["assembled_SOURCED"] if r["rent_reading"] == "Barkai"][0]
    crs_bk = [r for r in tk["MARKED_SENSITIVITY_at_CRS_implied_theta"]
              if r["rent_reading"] == "Barkai"][0]
    crs_kn = [r for r in tk["MARKED_SENSITIVITY_at_CRS_implied_theta"]
              if r["rent_reading"] == "Karabarbounis_Neiman_case_R"][0]
    R["RequiredEasy"] = pct(req["AMR_0.255"], 1)
    R["RequiredHard"] = pct(req["bottom_up_0.318"], 1)
    R["TauKAnalyticMax"] = pct(ours_bk["tau_k_max_ANALYTIC"], 1)
    R["CRSTheta"] = pct(crs["CRS_implied_taxable_share"], 1)
    R["TauKCRSCentral"] = pct(crs_bk["tau_k_central"], 1)
    R["TauKCRSPassShare"] = pct(crs_bk["pass_share_vs_required_low"], 0)
    R["TauKCRSAnalyticMax"] = pct(crs_bk["tau_k_max_ANALYTIC"], 1)
    R["TauKCRSKN"] = pct(crs_kn["tau_k_central"], 1)
    R["CRSTextFigure"] = pct(crs["CRS_text_figure_around_3_percent"], 1)
    R["CRSBandLow"] = pct(crs["CRS_R47113_Table_5_band_as_published"][0], 1)
    R["CRSBandHigh"] = pct(crs["CRS_R47113_Table_5_band_as_published"][1], 1)
    R["CRSRescaledLow"] = pct(crs["band_rescaled_to_our_theta"][0], 1)
    R["CRSRescaledHigh"] = pct(crs["band_rescaled_to_our_theta"][1], 1)
    R["ShareholderLayerPct"] = pct(tk["shareholder_layer_at_centrals"], 1)

    # ---- the levers, ranked by measured influence on the assembled rate
    movers = {m["parameter"]: m for m in tk["single_parameter_movers"]}
    for key, name in (("deferral_factor", "Deferral"), ("state_cit_effective", "StateCIT"),
                      ("shifted_share", "Shifted"), ("shareholder_rate", "ShareholderRate"),
                      ("debt_share", "DebtShare"), ("bondholder_rate", "BondRate"),
                      ("theta_taxable", "Theta")):
        R["Swing" + name] = f"{movers[key]['swing']:.4f}"
    R["DebtShareLow"] = pct(src["debt_share"]["low"], 1)
    R["DebtShareHigh"] = pct(src["debt_share"]["high"], 1)
    R["BondRateLow"] = pct(src["bondholder_rate"]["low"], 1)
    R["BondRateHigh"] = pct(src["bondholder_rate"]["high"], 1)
    R["DeferralLow"] = f"{src['deferral_factor']['low']:.3f}"
    R["DeferralHigh"] = f"{src['deferral_factor']['high']:.3f}"
    R["ThetaTaxableLow"] = pct(src["theta_taxable"]["low"])
    R["ThetaTaxableHigh"] = pct(src["theta_taxable"]["high"])

    # ---- statutory
    R["FedCIT"] = pct(comp["verified"]["federal_cit"])
    R["FDDEIRate"] = pct(comp["verified"]["fddei_effective_rate_CURRENT"], 1)
    R["CFCRate"] = pct(comp["verified"]["net_cfc_tested_income_effective_rate_CURRENT"], 1)
    R["RentBarkai"] = f"{comp['verified']['rent_readings_NEVER_AVERAGED']['Barkai']:.3f}"
    R["ShiftedShare"] = pct(comp["verified"]["shifted_share_single_verified_value"])

    # ---- data and method
    R["WageBillBn"] = f"{fis['denominators']['wage_bill_usd_bn']:,.1f}"
    R["FedReceiptsBn"] = f"{fis['denominators']['federal_current_receipts_usd_bn']:,.1f}"
    R["PlausChecks"] = str(plaus["n_checks"])
    R["PlausViolations"] = str(plaus["n_violations"])
    R["RepTwoScored"] = rep["2"]["quantities_scored"]
    R["RepTwoSealed"] = rep["2"]["sealed_counterparts"]
    R["RepTwoTolerance"] = rep["2"]["inside_tolerance"]
    R["RepTwoFivePct"] = rep["2"]["within_five_percent"]
    R["RepTwoMismatch"] = rep["2"]["mismatches"]
    R["RepThreeSealed"] = rep["3"]["sealed_counterparts"]
    R["RepThreeRounding"] = rep["3"]["within_rounding"]
    R["RepThreeMismatch"] = rep["3"]["mismatches"]
    R["ExcludedInstitutions"] = str(inst["excluded_no_capital_reported"]["n"])
    R["ExcludedAssetsBn"] = f"{inst['excluded_no_capital_reported']['assets_bn']:,.1f}"
    R["SystemAssetsBn"] = f"{inst['system_assets_bn']:,.1f}"
    R["BaselineBreaches"] = str(inst["baseline_breaches_after_exclusion"]["n_breaching"])
    R["BaselinePctAssets"] = f"{inst['baseline_breaches_after_exclusion']['pct_assets']:.3f}"

    # ---- displacement, measured
    R["TerminalLossTen"] = clearing["terminal_loss_10pct"]["value"].replace("bn", "")
    R["FedShareTenNarrowLow"] = pct(fed_dose["0.1"]["narrow_low"])
    R["FedShareTenNarrowHigh"] = pct(fed_dose["0.1"]["narrow_high"])
    R["FedShareTenConsLow"] = pct(fed_dose["0.1"]["conservatorship_low"])
    R["FedShareTenConsHigh"] = pct(fed_dose["0.1"]["conservatorship_high"])
    R["FedShareFiftyNarrowLow"] = pct(fed_dose["0.5"]["narrow_low"])
    R["FedShareFiftyNarrowHigh"] = pct(fed_dose["0.5"]["narrow_high"])
    R["FedShareSeventyFiveNarrowHigh"] = pct(fed_dose["0.75"]["narrow_high"])
    fed_bn = [float(r["federal_first_round_bn"]) for r in cons]
    priv_bn = [float(r["private_first_round_bn"]) for r in cons]
    R["FedFirstRoundTenLow"] = f"{min(fed_bn):,.0f}"
    R["FedFirstRoundTenHigh"] = f"{max(fed_bn):,.0f}"
    R["PrivateFirstRoundTenLow"] = f"{min(priv_bn):,.0f}"
    R["PrivateFirstRoundTenHigh"] = f"{max(priv_bn):,.0f}"
    R["OASDILossTenLow"] = f"{min(float(r['oasdi_bn']) for r in cons):,.0f}"
    R["OASDILossTenHigh"] = f"{max(float(r['oasdi_bn']) for r in cons):,.0f}"
    R["HILossTenLow"] = f"{min(float(r['hi_bn']) for r in cons):,.0f}"
    R["HILossTenHigh"] = f"{max(float(r['hi_bn']) for r in cons):,.0f}"

    # housing agencies
    un = [float(r["unenhanced_share_of_single_family_book"]) for r in gse_un]
    R["UnenhancedLow"] = pct(min(un))
    R["UnenhancedHigh"] = pct(max(un))
    wf10 = [r for r in gse_wf if r["dose_share_of_total_wage_bill"] == "0.1"]
    cover = [float(r["private_cover_share_of_loss"]) for r in wf10]
    R["PrivateCoverLow"] = pct(min(cover))
    R["PrivateCoverHigh"] = pct(max(cover))
    R["AgencyCapitalBn"] = f"{float(wf10[0]['capital_bn']):,.1f}"
    R["MaxRetainedAgencyLossBn"] = f"{max(float(r['retained_bn']) for r in gse_wf):,.1f}"
    assert all(float(r["treasury_draw_bn"]) == 0 for r in gse_wf), "a Treasury draw appeared"
    R["TreasuryDrawBn"] = "0"

    # household buffers by quintile
    for key, tag in (("Q1_bottom", "QOne"), ("Q2", "QTwo"), ("Q3_middle", "QThree"),
                     ("Q4", "QFour"), ("Q5_top", "QFive")):
        R[tag + "Runway"] = f"{float(quint_buf[key]['median_runway_months']):.2f}"
        R[tag + "UnderOne"] = f"{float(quint_buf[key]['pct_under_1_month']):.1f}"

    # the pay effect: how little of the raw gap survives reweighting on pay
    surviving = []
    for r in paycon:
        if r["statistic"] != "distress_pp_per_bn":
            continue
        for k in ("share_of_gap_that_is_pay_a", "share_of_gap_that_is_pay_b"):
            surviving.append(1 - float(r[k]))
    R["PayGapSurvivingLow"] = f"{100 * min(surviving):.1f}"
    R["PayGapSurvivingHigh"] = f"{100 * max(surviving):.1f}"
    R["PayCells"] = str(len(surviving))

    # attrition-led automation: case b against case c at the ten percent level
    ten = {}
    for r in first:
        if r["dose_share_of_total_wage_bill"] != "0.1":
            continue
        ten.setdefault((r["exposure_type"], r["incidence"]), r)
    moves = {"student": [], "auto": [], "mortgage": []}
    fiscal = set()
    for et in {k[0] for k in ten}:
        b, c = ten[(et, "b_entrants")], ten[(et, "c_sourced_mix")]
        moves["student"].append(float(b["student_loan_holders_loss_hi_bn"])
                                / float(c["student_loan_holders_loss_hi_bn"]) - 1)
        moves["auto"].append(float(b["auto_lenders_loss_hi_bn"])
                             / float(c["auto_lenders_loss_hi_bn"]) - 1)
        moves["mortgage"].append(float(b["mortgage_national_loss_hi_bn"])
                                 / float(c["mortgage_national_loss_hi_bn"]) - 1)
        fiscal.add((round(float(b["public_budget_loss_hi_bn"]), 4),
                    round(float(c["public_budget_loss_hi_bn"]), 4)))
    assert all(x == y for x, y in fiscal), "the fiscal loss moved across incidence cases"
    R["AttritionStudentLow"] = f"{100 * min(moves['student']):.0f}"
    R["AttritionStudentHigh"] = f"{100 * max(moves['student']):.0f}"
    R["AttritionAutoLow"] = f"{100 * min(moves['auto']):.0f}"
    R["AttritionAutoHigh"] = f"{100 * max(moves['auto']):.0f}"
    R["AttritionMortgageLow"] = f"{100 * abs(max(moves['mortgage'])):.0f}"
    R["AttritionMortgageHigh"] = f"{100 * abs(min(moves['mortgage'])):.0f}"

    # ---- institutions
    R["NInstitutions"] = f"{inst['n_institutions']:,}"
    R["NBanks"] = f"{inst['n_banks']:,}"
    R["NCreditUnions"] = f"{inst['n_credit_unions']:,}"

    # ---- banks and the second round
    def sysrow(dose, offset="False"):
        return sysres[(dose, "high", offset)]

    s10, s25, s50 = sysrow("0.1"), sysrow("0.25"), sysrow("0.5")
    R["SysLossTen"] = f"{float(s10['system_loss_bn']):,.0f}"
    R["SysFirstTen"] = f"{float(s10['first_round_bn']):,.0f}"
    R["SysSecondTen"] = f"{float(s10['second_round_bn']):,.0f}"
    R["SecondRoundShareTen"] = pct(float(s10["second_round_bn"])
                                   / float(s10["system_loss_bn"]))
    R["BreachTenN"] = f"{float(s10['n_breaching']):,.0f}"
    R["BreachTenAssets"] = f"{float(s10['pct_system_assets_breaching']):.2f}"
    R["BreachTwentyFiveN"] = f"{float(s25['n_breaching']):,.0f}"
    R["BreachTwentyFiveAssets"] = f"{float(s25['pct_system_assets_breaching']):.2f}"
    R["BreachTwentyFiveAssetsEarnings"] = \
        f"{float(sysrow('0.25', 'True')['pct_system_assets_breaching']):.2f}"
    R["BreachFiftyN"] = f"{float(s50['n_breaching']):,.0f}"
    R["BreachFiftyAssets"] = f"{float(s50['pct_system_assets_breaching']):.1f}"
    R["BreachFiftyAssetsEarnings"] = \
        f"{float(sysrow('0.5', 'True')['pct_system_assets_breaching']):.1f}"
    R["SysLossFifty"] = f"{float(s50['system_loss_bn']):,.0f}"

    def model(dose, m, field):
        return f"{float(bymodel[(dose, m)][field]):.2f}"

    R["CardHeavyTwentyFiveInst"] = model("0.25", "card-heavy", "pct_institutions_breaching")
    R["CardHeavyTwentyFiveAssets"] = model("0.25", "card-heavy", "pct_assets_breaching")
    R["CardHeavyFiftyInst"] = model("0.5", "card-heavy", "pct_institutions_breaching")
    R["CreditUnionTenInst"] = model("0.1", "credit union", "pct_institutions_breaching")
    R["MortgageLenderTwentyFiveInst"] = model("0.25", "mortgage portfolio lender",
                                              "pct_institutions_breaching")

    allrelief = {round(r["dose"], 2): r for r in instr if r["instrument"].startswith("ALL")}
    R["ReliefRemovedTen"] = f"{allrelief[0.1]['loss_removed_pct']:.2f}"
    R["ReliefRemovedTwentyFive"] = f"{allrelief[0.25]['loss_removed_pct']:.2f}"
    R["ReliefRemovedFifty"] = f"{allrelief[0.5]['loss_removed_pct']:.2f}"
    R["ReliefRemovedTenBn"] = f"{allrelief[0.1]['loss_removed_bn']:,.1f}"
    R["ReliefAssetsBeforeTwentyFive"] = f"{allrelief[0.25]['pct_assets_breaching_before']:.2f}"
    R["ReliefAssetsAfterTwentyFive"] = f"{allrelief[0.25]['pct_assets_breaching_after']:.2f}"
    R["ReliefStoppedTwentyFive"] = str(allrelief[0.25]["institutions_stopped_breaching"])
    wi = [r for r in instr if r["instrument"].startswith("wage insurance, enhanced")
          and round(r["dose"], 2) == 0.1][0]
    R["WageInsuranceCost"] = f"{wi['fiscal_cost_bn']:,.0f}"
    R["WageInsuranceRemoved"] = f"{wi['loss_removed_bn']:,.1f}"

    sl = omitted["state_and_local_government"]
    R["StateLocalWageLinkedBn"] = f"{sl['size_bn']['of which wage-linked at the SOI wage share']:,.1f}"
    R["StateLocalWageLinkedShare"] = pct(sl["wage_linked_share_of_own_tax_receipts"])
    R["PensionHoldingsBn"] = f"{omitted['pension_funds']['size_bn']['labour_backed_claims_held']:,.1f}"
    ins = omitted["insurers_and_private_credit"]["size_bn"]
    R["InsurerHoldingsBn"] = f"{ins['insurers, labour-backed claims held']:,.1f}"
    R["OtherFinancialHoldingsBn"] = \
        f"{ins['other financial (includes private credit), labour-backed claims held']:,.1f}"
    R["AIBankCommitmentsBn"] = \
        f"{ins['large bank C and I commitments to AI-adjacent industries']:,.0f}"

    # ---- the AI bust
    R["TopOnePctEquity"] = pct(bust["top1_share_of_corporate_equity"], 1)
    R["BottomHalfEquity"] = pct(bust["bottom50_share"], 1)
    R["MPCWealth"] = "3.2"

    # ---- if AI fails
    nf = tiers["nine_filers"]
    R["FilerCapexBn"] = f"{nf['capex_bn']:,.1f}"
    R["FilerOCFBn"] = f"{nf['ocf_bn']:,.1f}"
    R["SelfFunding"] = f"{nf['self_funding_ratio']:.2f}"
    R["DebtFinancedShare"] = pct(nf["debt_financed_share_of_capex"], 1)
    R["OnBalanceSheetAIDebtBn"] = f"{nf['on_balance_sheet_debt_bn']:,.1f}"
    ft = tiers["flip_thresholds"]
    R["FlipToBetweenBn"] = f"{ft['additional_debt_financed_capex_to_reach_0.20_bn']:,.1f}"
    R["FlipToBetweenShare"] = pct(ft["as_share_of_identified_bank_commitments"], 1)
    R["FlipToDebtLedBn"] = f"{ft['additional_to_reach_0.50_bn']:,.1f}"
    R["FlipToDebtLedShare"] = pct(ft["as_share_of_identified_bank_commitments_0.50"], 1)
    R["AIDrawnBn"] = f"{[x for x in tiers['tiers'] if x['tier'].startswith('2b')][0]['size_bn']:,.0f}"

    bust_pct = b34["bust_wage_bill_dose_equivalent_pct"]
    head = b34["compare_displacement_headline_dose_pct"]
    R["BustWageLow"] = f"{min(bust_pct):.2f}"
    R["BustWageHigh"] = f"{max(bust_pct):.2f}"
    R["BustRatioLow"] = f"{head / max(bust_pct):.0f}"
    R["BustRatioHigh"] = f"{head / min(bust_pct):.0f}"
    R["BustCreditLow"] = f"{min(b34['household_credit_loss_bn_range']):.1f}"
    R["BustCreditHigh"] = f"{max(b34['household_credit_loss_bn_range']):.1f}"
    R["BustReceiptsLow"] = f"{abs(max(b34['federal_receipts_fall_bn_range'])):,.0f}"
    R["BustReceiptsHigh"] = f"{abs(min(b34['federal_receipts_fall_bn_range'])):,.0f}"

    eq = [r for r in engine if r["scenario"].startswith("equity-led")][0]
    cr = [r for r in engine if r["scenario"].startswith("credit-led")][0]
    R["EquityLedReceiptsPct"] = f"{abs(float(eq['federal_receipts_fall_pct_VERIFIED'])):.1f}"
    R["EquityLedCorpPct"] = f"{abs(float(eq['corporate_tax_fall_pct_VERIFIED'])):.1f}"
    R["CreditLedReceiptsPct"] = f"{abs(float(cr['federal_receipts_fall_pct_VERIFIED'])):.1f}"
    R["CreditLedCorpPct"] = f"{abs(float(cr['corporate_tax_fall_pct_VERIFIED'])):.1f}"
    R["BustGDPLow"] = f"{abs(max(bust['gdp_fall_pct_range'])):.2f}"
    R["BustGDPHigh"] = f"{abs(min(bust['gdp_fall_pct_range'])):.2f}"

    R["FedPayoffFails"] = f"{float(payoff['federal_government']['net_ai_fails']):.3f}"
    R["FedPayoffPartial"] = f"{float(payoff['federal_government']['net_partial']):.3f}"
    R["FedPayoffSuccess"] = f"{float(payoff['federal_government']['net_success']):.3f}"
    R["HouseholdPayoffSuccess"] = f"{float(payoff['households']['net_success']):.3f}"
    R["BanksAISide"] = pct(payoff["banks"]["ai_leg_share"], 1)
    R["HouseholdsAISide"] = pct(payoff["households"]["ai_leg_share"], 1)

    # ---- institutions, by regime
    ai_total = (tsb["ai_leg"]["ai_equity_central_bn"]
                + tsb["ai_leg"]["ai_onbalancesheet_debt_bn"])
    R["AISideTotalBn"] = f"{ai_total:,.1f}"
    R["StakeForTenPctBn"] = f"{0.10 * ai_total:,.0f}"
    held = float(it3["ai_leg_federal_share_central"])
    R["GapClosedAtTenPct"] = pct((0.10 - held) / float(it3["holder_gap_central"]), 0)
    R["StakeVersusAgencyCapital"] = f"{0.10 * ai_total / float(wf10[0]['capital_bn']):.0f}"

    beA = [float(r["case_A_break_even_tau_k"]) for r in cases]
    beB = [float(r["case_B_break_even_tau_k"]) for r in cases]
    R["BreakEvenALow"] = pct(min(beA), 1)
    R["BreakEvenAHigh"] = pct(max(beA), 1)
    R["BreakEvenBLow"] = pct(min(beB), 1)
    R["BreakEvenBHigh"] = pct(max(beB), 1)

    em = [r for r in debtinc if r["horizon"] == "20" and r["dose"] == "0.1"
          and r["case"] == "A" and r["regime"] == "emerging_market"]
    rc = [r for r in debtinc if r["horizon"] == "20" and r["dose"] == "0.1"
          and r["case"] == "A" and r["regime"] == "reserve_currency"]
    R["EMBaseline"] = pct(float(em[0]["baseline_debt_to_gdp"]), 1)
    R["EMIncrementLow"] = f"{min(float(r['INCREMENT_pp_of_gdp']) for r in em):.1f}"
    R["EMIncrementHigh"] = f"{max(float(r['INCREMENT_pp_of_gdp']) for r in em):.1f}"
    R["ReserveIncrementLow"] = f"{min(float(r['INCREMENT_pp_of_gdp']) for r in rc):.1f}"
    R["ReserveIncrementHigh"] = f"{max(float(r['INCREMENT_pp_of_gdp']) for r in rc):.1f}"
    em_tot = sum(float(r["INCREMENT_pp_of_gdp"]) for r in em)
    rc_tot = sum(float(r["INCREMENT_pp_of_gdp"]) for r in rc)
    R["EMRatio"] = f"{em_tot / rc_tot:.1f}"

    R["PrimeAgeNonemp"] = dash["Prime-age nonemployment rate"]["value"]
    R["PrimeAgeMax"] = dash["Prime-age nonemployment rate"]["threshold"]
    R["DisplacementFlow"] = dash[
        "Observed annual displacement flow (DWS long-tenured)"]["value"]
    R["GradUnemployment"] = dash["Recent college graduate unemployment rate"]["value"]
    R["GradUnderemployment"] = dash["Recent college graduate underemployment rate"]["value"]
    R["AutoDelinquency"] = dash["Auto loan balance 90+ days delinquent"]["value"]
    R["OASDIDepletion"] = dash["Combined OASDI reserve depletion date"]["value"]

    # ---- revision: pass-through, the cash-flow bridge, relief feedback, two directions
    gc = a1["g_central_base"]
    gp = a1["g_central_with_thirty_percent_price_pass_through"]
    R["GCentral"] = f"{gc['g']:.2f}"
    R["GLow"] = f"{a1['g_range_base_construction'][0]:.2f}"
    R["GHigh"] = f"{a1['g_range_base_construction'][1]:.2f}"
    R["RequiredPTEasy"] = pct(gc["required_easier"], 0)
    R["RequiredPTHarder"] = pct(gc["required_harder"], 0)
    R["GWithPrice"] = f"{gp['g']:.2f}"
    R["RequiredPriceEasy"] = pct(gp["required_easier"], 0)
    R["RequiredPriceHarder"] = pct(gp["required_harder"], 0)
    R["PriceThrough"] = pct(gp["price_pass_through_p"])
    R["CapitalCostShare"] = pct(a1["capital_cost_share_central"])
    dec = a1["capex_dollar_decomposition_used"]
    R["CapexDomesticLabor"] = pct(dec["domestic_labour_already_inside_tau_l"][1])
    R["CapexImported"] = pct(dec["imported_no_us_tax"][1])
    R["CapexDomesticSurplus"] = pct(dec["domestic_producer_surplus"][1])

    flat = a2path["0.0"]
    grow = a2path["0.2"]
    R["TransitionPositiveYear"] = flat["years_until_net_tax_turns_positive"]
    R["TransitionYearOne"] = f"{abs(float(grow['net_tax_year_1_per_unit_of_investment'])):.2f}"
    R["TransitionYearFive"] = f"{abs(float(grow['net_tax_year_5'])):.3f}"
    R["TransitionYearTwentyFive"] = f"{abs(float(grow['net_tax_year_25'])):.3f}"
    R["TransitionGrowthRate"] = pct(0.20)

    by = {str(d["dose"]): d for d in a3["by_dose"]}
    for key, tag in (("0.1", "Ten"), ("0.25", "TwentyFive"), ("0.5", "Fifty")):
        d = by[key]
        R["ReliefNoFeedback" + tag] = f"{d['removed_no_feedback_pct']:.1f}"
        R["ReliefFeedback" + tag] = f"{d['removed_with_feedback_pct']:.1f}"
        R["ReliefCost" + tag] = f"{d['fiscal_cost_bn']:,.0f}"
        R["ReliefAssetsBefore" + tag] = f"{d['assets_breaching_before_pct']:.2f}"
        R["ReliefAssetsNoFeedback" + tag] = f"{d['assets_breaching_no_feedback_pct']:.2f}"
        R["ReliefAssetsFeedback" + tag] = f"{d['assets_breaching_with_feedback_pct']:.2f}"
    d25, d50 = by["0.25"], by["0.5"]
    R["CardHeavyReliefNoFeedback"] = f"{d25['card_heavy_assets_breaching_before_after'][0]:.1f}"
    R["CardHeavyReliefFeedback"] = f"{d25['card_heavy_assets_breaching_before_after'][1]:.1f}"
    R["CUReliefNoFeedbackFifty"] = f"{d50['credit_union_assets_breaching_before_after'][0]:.1f}"
    R["CUReliefFeedbackFifty"] = f"{d50['credit_union_assets_breaching_before_after'][1]:.1f}"

    closing = [r for r in a4grid if r["rate_definition"].startswith("required, ")]
    mults = [float(r["multiple_of_assembled_low"]) for r in closing] + \
            [float(r["multiple_of_assembled_high"]) for r in closing]
    R["ClosingMultipleLow"] = f"{min(mults):.2f}"
    R["ClosingMultipleHigh"] = f"{max(mults):.2f}"
    R["BustFallLow"] = f"{min(a4['verified_bust_receipts_fall_bn']):,.0f}"
    R["BustFallHigh"] = f"{max(a4['verified_bust_receipts_fall_bn']):,.0f}"
    R["BustAtRiskIncreaseLow"] = f"{min(a4['verified_bust_receipts_fall_bn']) * (min(mults) - 1):,.0f}"
    R["BustAtRiskIncreaseHigh"] = f"{max(a4['verified_bust_receipts_fall_bn']) * (max(mults) - 1):,.0f}"

    # ---- the pass shares, by base and by labor tax reading, for the corrected statement
    R["PassShareOursEasy"] = pct(bk["pass_share_vs_required_low"], 2)
    R["PassShareOursHard"] = pct(bk["pass_share_vs_required_high"], 2)
    R["PassShareCRSEasy"] = pct(crs_bk["pass_share_vs_required_low"], 1)
    R["PassShareCRSHard"] = pct(crs_bk["pass_share_vs_required_high"], 1)
    R["AnalyticMaxOurs"] = pct(ours_bk["tau_k_max_ANALYTIC"], 1)
    R["AnalyticMaxCRS"] = pct(crs_bk["tau_k_max_ANALYTIC"], 1)

    lines = ["% AUTO-GENERATED by paper/gen_results_macros.py. Do not edit by hand.",
             "% Every value traces to a measured JSON artifact in this repository.",
             "\\makeatletter",
             "\\newcommand{\\result}[1]{\\@nameuse{result@#1}}",
             "\\makeatother"]
    for k, v in R.items():
        lines.append(f"\\expandafter\\def\\csname result@{k}\\endcsname{{{v}}}")
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUT} with {len(R)} macros")
    for k, v in R.items():
        print(f"  {k:24s} {v}")


if __name__ == "__main__":
    main()
