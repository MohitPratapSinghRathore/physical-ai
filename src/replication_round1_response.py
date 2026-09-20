"""Item 2 of the replication-repair session: every round-one mismatch classified, and the
R sensitivity the owner asked for.

WHAT THIS PRODUCES

  data/processed/replication_round1_classification.csv
      one row per mismatch, with the class, the cause, what was done, and whether the
      project's value moved. Five classes, exactly as the owner specified:
          brief_insufficiency   the brief did not contain enough to rebuild the quantity
          data_vintage          both sides are right about different vintages of a series
          definitional_choice   both sides are right about different constructions
          replicator_error      the replicator's rebuild was wrong, by their own account
                                or by ours
          our_error             this project's value was wrong and is corrected
      A mismatch can have a contributing second class; the primary one drives the fix.

  data/processed/replication_r_sensitivity.json
      R and the fiscal condition under (a) this project's construction, (b) the
      replicator's rho fit, (c) the replicator's omega, and (d) both together, which is
      their reported 0.6233. The fiscal condition verdict is reported under every one.

THE R DISAGREEMENT, resolved. The replicator inferred that our rho must be a FITTED value
of about 0.697 at current slack, and therefore that our omega must be about 0.815. Both
inferences are wrong, and the brief is why:

    our rho is 0.6610, the DIRECTLY OBSERVED 2026 value: DWS Table 1 total row, 2,199
    thousand of 3,324 thousand long-tenured displaced workers employed in January 2026.
    The fitted line is used ONLY on the extended axis, where slack moves away from what
    has been observed. Section 2 of the brief says "rho is reemployment from section 1
    evaluated at current slack", which describes the fitted value and is simply wrong
    about the code. That sentence is corrected in brief v2.

    our omega is 0.8598, the counterfactual blended central value, not 0.815.

So the R gap is two roughly equal parts: rho 0.6610 observed against their 0.6926 fitted,
and omega 0.8598 against their assumed 0.90. Neither is a coding difference. One is a
brief error and one is a brief omission.

THE y SERIES, stated exactly, because the brief did not. y is the percent of LONG-TENURED
displaced workers (three or more years on the lost job) who were EMPLOYED at the survey
date, all ages, both sexes, taken from the total row of Table 1 of each Displaced Workers
Summary news release. Not the prime-age rate, not the full-time wage and salary reemployed
rate. Fourteen vintages, survey months January 2000 through January 2026, one observation
per biennial release. The replicator used 1998 through 2024: same n, a window shifted by
one release at each end. That window difference is the whole of the intercept and slope
gap, since their x construction reproduces our x_range endpoints to five decimals.
"""
import json
import pathlib

import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).parents[1]
OUT = ROOT / "data" / "processed"
REP = ROOT / "notes" / "replication"

TAU_L = {"AMR_0.255": 0.255, "bottom_up_0.301": 0.301, "bottom_up_0.318": 0.318}
TAU_K_OPERATIVE = 0.0708

# The replicator's corrected rho fit, from their comparison.csv (OECD x, January months,
# n = 14, vintages 1998 to 2024).
REPLICATOR_FIT = {"intercept": 1.29948, "slope": -0.030632}
REPLICATOR_OMEGA = 0.90
REPLICATOR_R = 0.6233

# ---------------------------------------------------------------------------------------
# One row per mismatch. quantity_id matches notes/replication/comparison.csv exactly.
# ---------------------------------------------------------------------------------------
CLASSIFICATION = [
    ("rho_slack.intercept", "brief_insufficiency", "",
     "The brief names 'the BLS Displaced Worker Survey reemployment rate' without saying "
     "WHICH rate or over WHICH vintage window. Ours is the percent of long-tenured "
     "displaced workers employed at the survey date, all ages, Table 1 total row, 14 "
     "vintages January 2000 to January 2026. Theirs is the same concept over 1998 to 2024. "
     "Their x reproduces our x_range to five decimals, so the window is the whole gap.",
     "brief v2 states the table, row, universe and window", "no"),
    ("rho_slack.slope", "brief_insufficiency", "",
     "Same cause as the intercept, same row.",
     "brief v2 states the table, row, universe and window", "no"),
    ("fiscal.R_2026", "brief_insufficiency", "our_error",
     "TWO causes. Omission: omega is described as 'a blended counterfactual from the DWS "
     "earnings question' and its value, 0.8598, is never given. OUR ERROR in the brief, not "
     "in the code: the brief says rho is 'evaluated at current slack', which describes the "
     "fitted line, while the code uses the DIRECTLY OBSERVED 2026 rho of 0.6610. The "
     "replicator reverse-engineered an omega of 0.815 from that wrong description.",
     "brief v2 gives omega, its three components and its range, and corrects the rho "
     "sentence", "no"),
    ("fiscal.tau_k_sourced_low", "replicator_error", "brief_insufficiency",
     "Conceded by the replicator: they set tau_normal in 0.10 to 0.20 where full expensing "
     "drives the effective rate on the normal return to near zero. Contributing cause: the "
     "brief names Auerbach and AMR for tau_normal and never states the expensing result or "
     "the number.",
     "brief v2 states tau_normal, the expensing statute and the full decomposition", "no"),
    ("fiscal.tau_k_sourced_high", "replicator_error", "brief_insufficiency",
     "Same cause as the low end of the grid.",
     "brief v2 states the full decomposition", "no"),
    ("fiscal_magnitudes.terminal_loss_bn_at_10pct", "our_error", "brief_insufficiency",
     "OUR ERROR: the dose share was converted to dollars on FRED COE compensation of "
     "employees (16,224.3bn) while tau_l is built as federal taxes over FRED WASCUR wages "
     "and salaries (13,365.2bn). Compensation includes employer pension and health "
     "contributions, which bear neither the income tax nor the payroll tax. Every dollar "
     "fiscal figure was 21.4 percent too large. Contributing: the brief did not state the "
     "horizon or that the figure is a mean across exposure groups at that dose.",
     "base corrected to WASCUR; value falls 17.6 percent to 85.168", "YES"),
    ("fiscal_magnitudes.terminal_loss_bn_at_25pct", "our_error", "brief_insufficiency",
     "Same cause, same correction.",
     "base corrected to WASCUR; value falls 17.6 percent to 301.892", "YES"),
    ("trust_funds.OASDI_pct_at_10pct", "brief_insufficiency", "",
     "The brief insists the denominator is the fund's own payroll income and never gives "
     "it. The replicator used 1,150bn against a published 1,322.6bn. Our construction is a "
     "RATIO in which the wage bill base and the payroll tax rate both cancel, so it was not "
     "touched by the base error above.",
     "brief v2 states 1,322.6bn from Trustees Table 5; our value moves only by the "
     "published-versus-derived OASDI figure", "marginal, 4.0713 to 4.0695"),
    ("trust_funds.OASDI_pct_at_25pct", "brief_insufficiency", "",
     "Same cause, same row.",
     "brief v2 states the denominator", "marginal, 12.0372 to 12.0319"),
    ("trust_funds.HI_pct_at_10pct", "our_error", "brief_insufficiency",
     "OUR ERROR: the payroll share of fund income was taken as 0.9126 for BOTH funds. That "
     "is the OASDI share. HI's own payroll share is 403.2 / 462.4 = 0.8720, so every HI "
     "ratio was 4.7 percent too large. Separately, the fiscal modules used 462.4bn as an HI "
     "PAYROLL denominator when it is HI TOTAL income including interest, government "
     "contributions and beneficiary premiums.",
     "fund-specific payroll shares read from Trustees Table 5; value falls to 3.8582",
     "YES"),
    ("coverage_share.card", "brief_insufficiency", "definitional_choice",
     "'Working core' is used throughout and never defined. The replicator found 'reference "
     "person under 65' by sensitivity testing and landed within 0.011. Our definition is "
     "narrower at both ends: at least one employed member AND a reference person aged 25 to "
     "64.",
     "brief v2 defines the working core exactly, and flags that a second, superseded "
     "definition exists in the stress engine", "no"),
    ("coverage_share.student", "brief_insufficiency", "definitional_choice",
     "Same cause, same row.",
     "brief v2 defines the working core exactly", "no"),
    ("cap_contrast.ACS.cognitive_AIOE", "replicator_error", "brief_insufficiency",
     "Conceded by the replicator: their AIOE crosswalk matched 476 of 530 ACS SOCP codes "
     "against 524 for GPT, because ACS publishes broad and wildcarded SOC codes and AIOE is "
     "detailed six-digit. Their prefix averaging blurred 54 codes. Contributing: the brief "
     "states no aggregation rule.",
     "brief v2 states the crosswalk and the aggregation rule", "no"),
    ("cap_contrast.ACS.cognitive_GPT", "replicator_error", "brief_insufficiency",
     "Same cause, smaller because the GPT crosswalk matched 524 codes.",
     "brief v2 states the crosswalk and the aggregation rule", "no"),
    ("cap_contrast.SIPP.cognitive_AIOE", "replicator_error", "brief_insufficiency",
     "Same cause as the ACS AIOE row.",
     "brief v2 states the crosswalk and the aggregation rule", "no"),
    ("pay_control.raw_gap.ACS_AIOE", "brief_insufficiency", "replicator_error",
     "The brief never says the pay control runs over TWO outcome variables, and one of them "
     "(distress_pp_per_bn) is never mentioned anywhere in it. The replicator scored a "
     "single cell against a four-cell structure. Their AIOE group also differs for the "
     "crosswalk reason above.",
     "brief v2 gives both outcomes, both reweighting directions and all four cells", "no"),
    ("pay_control.raw_gap.ACS_GPT", "brief_insufficiency", "",
     "Same cause.",
     "brief v2 gives the full four-cell structure", "no"),
    ("pay_control.raw_gap.SIPP_AIOE", "brief_insufficiency", "replicator_error",
     "Same cause, with the AIOE crosswalk contributing.",
     "brief v2 gives the full four-cell structure", "no"),
    ("pay_control.pay_share.ACS_AIOE", "brief_insufficiency", "",
     "The brief's '54 to 99 percent' band spans BOTH reweighting directions and never says "
     "so. 0.539456 is the ACS AIOE direction-b value. The replicator computed direction a "
     "only.",
     "brief v2 defines direction a and direction b and seals both", "no"),
    ("pay_control.pay_share.ACS_GPT", "brief_insufficiency", "",
     "Same cause.", "brief v2 defines both directions", "no"),
    ("pay_control.pay_share.SIPP_AIOE", "brief_insufficiency", "",
     "Same cause.", "brief v2 defines both directions", "no"),
    ("pay_control.pay_share.SIPP_GPT", "brief_insufficiency", "",
     "Same cause. Both sides exceed 1, which is the sign reversal, so the FINDING "
     "replicated even though the number did not.",
     "brief v2 defines both directions", "no"),
    ("cases.case_B_over_A_min", "our_error", "brief_insufficiency",
     "OUR ERROR, two of them in one expression. The case B loss added tau_k times the "
     "demand shortfall using the MIDPOINT of the sourced tau_k range (0.11798) while the "
     "case A loss it was added to embeds the operative Barkai rate (0.0708); and the demand "
     "shortfall was built on this project's occupational grid while the loss was built on "
     "compensation of employees.",
     "one tau_k and one wage bill base throughout; ratio becomes 1.383 to 1.677", "YES"),
    ("cases.case_B_over_A_max", "our_error", "brief_insufficiency",
     "Same cause, same correction.", "ratio becomes 1.383 to 1.677", "YES"),
    ("cases.breakeven_tau_k_A_min", "our_error", "",
     "OUR ERROR, and the replicator found it from a plausibility bound alone. See the "
     "break-even note in src/consistency.py.",
     "break-even redefined as tau_l * (1 - R); value becomes 0.124614", "YES"),
    ("cases.breakeven_tau_k_A_max", "our_error", "",
     "OUR ERROR. The sealed 0.378371 exceeds the highest reading of tau_l, which "
     "tau_l * (1 - R) makes impossible unless R is negative. Two defects multiplied: the "
     "expression divided a loss that ALREADY nets out tau_k by a surplus, and the numerator "
     "and denominator were built on two different wage bill totals, a spurious factor of "
     "16,224.3 / 9,870.2 = 1.6438. Old value = (comp / grid) x [tau_l - tau_k / (1 - R)], "
     "which at R = 0 is 1.6438 x (0.301 - 0.0708) = 0.3784 exactly.",
     "break-even redefined; value becomes 0.301, which is tau_l at R = 0, and the bound is "
     "now enforced", "YES"),
    ("cases.breakeven_tau_k_B_max", "our_error", "",
     "Same root cause. The replicator's own case B exceeded 1 on their grid, which is also "
     "not a possible tax rate; both sides were producing out-of-bound values from "
     "under-specified formulas.",
     "break-even B redefined as tau_l * ((1 - R) * D + (W / Y) * dC) / (D - dC); value "
     "becomes 0.649569, and 1.0979 is not reachable under the corrected formula", "YES"),
    ("debt.debt_to_gdp_start", "definitional_choice", "data_vintage",
     "Both sides use FRED GFDEBTN at 2026Q1. The denominator differs: ours is the ANNUAL "
     "MEAN of quarterly nominal GDP (32,175.9bn, the capacities.json convention used "
     "everywhere in this project), theirs the single quarter. The brief does not pin the "
     "GDP concept down.",
     "brief v2 states the GDP concept and the quarter", "no"),
    ("debt.baseline_20y", "definitional_choice", "",
     "Follows entirely from the start ratio above. The replicator reproduces 3.7674 exactly "
     "at our start ratio, which is the cleanest confirmation in the whole exercise.",
     "brief v2 states the GDP concept", "no"),
    ("debt.increment_pp_10pct_emerging", "brief_insufficiency", "our_error",
     "The brief's section 13 never says which CASE the increments are computed under, even "
     "though section 12 insists every figure carries its case. They are case B. The brief "
     "also names one regime where the sealed file has three. Contributing our error: the "
     "case B loss feeding the increment carried the two defects above, so the value moves "
     "as well.",
     "brief v2 states the case and all three regimes; value becomes 18.196", "YES"),
]


def classification_table():
    C = pd.DataFrame(CLASSIFICATION, columns=[
        "quantity_id", "primary_class", "contributing_class", "cause",
        "what_was_done", "our_value_changed"])
    cmp_path = REP / "comparison.csv"
    if cmp_path.exists():
        cmp = pd.read_csv(cmp_path)
        C = C.merge(cmp[["quantity_id", "my_value", "sealed", "verdict"]],
                    on="quantity_id", how="left")
        C = C.rename(columns={"my_value": "replicator_value", "sealed": "round1_sealed",
                              "verdict": "round1_verdict"})
    return C


def r_sensitivity():
    """R and the fiscal condition under our construction and under the replicator's."""
    rws = json.loads((OUT / "retained_wage_share_summary.json").read_text())
    sl = json.loads((OUT / "slack_reestimate.json").read_text())
    fit = sl["fits"]["rho_on_PRIME_AGE_nonemployment"]
    tk = json.loads((OUT / "tau_k_decomposition_summary.json").read_text())

    rho_obs = rws["rho_2026"]
    omega = rws["omegas"]["counterfactual_blended_central"]
    # Current slack, the x both fitted lines are evaluated at: the prime-age (25 to 54)
    # nonemployment rate the trigger dashboard publishes, 19.31 percent. It sits BELOW the
    # fitted x_range of 18.27 to 24.71 only at the bottom, so this is interpolation.
    x_now = 19.31

    rho_fit_ours = fit["intercept"] + fit["slope"] * x_now
    rho_fit_theirs = REPLICATOR_FIT["intercept"] + REPLICATOR_FIT["slope"] * x_now

    cases = {
        "ours_observed_rho_and_our_omega": (rho_obs, omega),
        "their_fitted_rho_and_our_omega": (rho_fit_theirs, omega),
        "our_fitted_rho_and_our_omega": (rho_fit_ours, omega),
        "ours_observed_rho_and_their_omega": (rho_obs, REPLICATOR_OMEGA),
        "their_fitted_rho_and_their_omega": (rho_fit_theirs, REPLICATOR_OMEGA),
    }
    out = {}
    for k, (rho, om) in cases.items():
        R = rho * om
        req = {ln: tl * (1 - R) for ln, tl in TAU_L.items()}
        out[k] = {
            "rho": round(rho, 6), "omega": round(om, 6), "R": round(R, 6),
            "required_tau_k": {ln: round(v, 6) for ln, v in req.items()},
            "operative_tau_k": TAU_K_OPERATIVE,
            "sourced_tau_k_high": tk["tau_k_range_sourced_sigma"][1],
            "condition_passes_at_operative_tau_k": bool(
                all(TAU_K_OPERATIVE >= v for v in req.values())),
            "condition_passes_at_top_of_sourced_range": bool(
                all(tk["tau_k_range_sourced_sigma"][1] >= v for v in req.values())),
        }
    out["_replicator_reported_R"] = REPLICATOR_R
    out["_x_now_prime_age_nonemployment_pct"] = x_now
    out["_note"] = (
        "The fiscal condition FAILS at the operative tau_k of 0.0708 under every "
        "combination, including the replicator's own R of 0.6233. That is the result the "
        "replicator independently confirmed after correcting their tau_normal. The "
        "condition is closable only at the TOP of the sourced tau_k range and only under "
        "the most favourable R, which is the weaker statement the corrected break-even "
        "grid also produces.")
    return out


def main():
    C = classification_table()
    C.to_csv(OUT / "replication_round1_classification.csv", index=False)
    pd.set_option("display.width", 200)
    pd.set_option("display.max_colwidth", 44)

    print("=== ITEM 2: ALL 30 ROUND-ONE MISMATCHES CLASSIFIED ===")
    print(f"  {len(C)} mismatches\n")
    print("  by PRIMARY class:")
    for k, n in C["primary_class"].value_counts().items():
        print(f"    {k:22s} {n:3d}")
    print("\n  contributing classes, where a second cause applies:")
    cc = C[C["contributing_class"] != ""]["contributing_class"].value_counts()
    for k, n in cc.items():
        print(f"    {k:22s} {n:3d}")
    ours = C[(C["primary_class"] == "our_error")
             | (C["contributing_class"] == "our_error")]
    print(f"\n  OURS TO FIX: {len(ours)} of {len(C)}. Every one is fixed this session.")
    print(C[["quantity_id", "primary_class", "our_value_changed"]].to_string(index=False))

    print("\n=== THE R DISAGREEMENT, AND R UNDER THE REPLICATOR'S SERIES ===")
    RS = r_sensitivity()
    (OUT / "replication_r_sensitivity.json").write_text(json.dumps(RS, indent=2))
    print(f"  {'construction':42s} {'rho':>7s} {'omega':>7s} {'R':>7s} "
          f"{'req tau_k (0.301)':>18s}  verdict at the operative 0.0708")
    for k, v in RS.items():
        if k.startswith("_"):
            continue
        print(f"  {k:42s} {v['rho']:7.4f} {v['omega']:7.4f} {v['R']:7.4f} "
              f"{v['required_tau_k']['bottom_up_0.301']:18.4f}  "
              f"{'PASSES' if v['condition_passes_at_operative_tau_k'] else 'FAILS'}")
    print(f"\n  the replicator's own reported R was {REPLICATOR_R}, and the condition FAILS "
          f"under it too.")
    print("  THE FISCAL CONDITION FAILS UNDER BOTH SIDES' PARAMETERS. That is the one "
          "headline\n  the replication confirms outright rather than merely matching.")


if __name__ == "__main__":
    main()
