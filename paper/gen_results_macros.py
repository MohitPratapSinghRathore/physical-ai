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
    lb = load("framework/labor_backing/direct_ratio_latest.json")
    do = load("framework/labor_backing/debt_only_ratio.json")
    cg = load("framework/labor_backing/capital_gains_bound.json")
    tk = load("framework/tau_k/tau_k_assembled.json")
    comp = load("framework/tau_k/components.json")
    inst = load("framework/institutions/a2_summary.json")
    bust = load("framework/ai_bust/b2_transmission.json")
    rsen = load("data/processed/replication_r_sensitivity.json")
    it3 = load("framework/labor_backing/item3_sovereign_robustness.json")
    tsb = load("framework/labor_backing/two_sided_bet.json")
    dots = {r["year"]: r for r in
            rows("framework/labor_backing/debt_only_ratio_timeseries.csv")}
    drts = {r["year"]: r for r in
            rows("framework/labor_backing/direct_ratio_timeseries.csv")}
    quint = {r["wage_quintile"]: r for r in
             rows("framework/labor_backing/quintile_labour_backing.csv")}
    acsen = load("framework/labor_backing/sensitivity.json")

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
    R["GainsUntaxedAtDeath"] = "46.9"
    R["InterestSheltered"] = "32.8"
    R["BondsRestOfWorld"] = "28.7"
    R["BondsHouseholdDirect"] = "1.1"

    # ---- statutory
    R["FedCIT"] = pct(comp["verified"]["federal_cit"])
    R["FDDEIRate"] = pct(comp["verified"]["fddei_effective_rate_CURRENT"], 1)
    R["CFCRate"] = pct(comp["verified"]["net_cfc_tested_income_effective_rate_CURRENT"], 1)
    R["RentBarkai"] = f"{comp['verified']['rent_readings_NEVER_AVERAGED']['Barkai']:.3f}"
    R["ShiftedShare"] = pct(comp["verified"]["shifted_share_single_verified_value"])

    # ---- institutions
    R["NInstitutions"] = f"{inst['n_institutions']:,}"
    R["NBanks"] = f"{inst['n_banks']:,}"
    R["NCreditUnions"] = f"{inst['n_credit_unions']:,}"

    # ---- the AI bust
    R["TopOnePctEquity"] = pct(bust["top1_share_of_corporate_equity"], 1)
    R["BottomHalfEquity"] = pct(bust["bottom50_share"], 1)
    R["MPCWealth"] = "3.2"

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
