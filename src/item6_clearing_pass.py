"""Item 6 of the final analysis session. The clearing pass.

Every number intended for the abstract, the introduction or a headline table is marked
REPLICATED, STANDING or SCENARIO. Anything that is none of the three is REMOVED from the
headline set and listed.

The three tags mean exactly this and nothing else:

  REPLICATED  an instance that did not write the code rebuilt it from raw data and the
              brief alone, and landed inside the project's own stated tolerance. Round one
              or round two. The tag is about provenance, not about being right.
  STANDING    it clears every applicable check on the standing checklist, is not
              contradicted, and is measured from data. It has NOT been independently
              rebuilt, either because no replicator attempted it or because the brief did
              not give them enough to attempt it.
  SCENARIO    it is conditional on an assumption that is chosen rather than measured: a
              dose, an AI equity scale, an adoption path, a policy response. The number is
              arithmetic given the assumption and carries no claim about likelihood.

  REMOVED     none of the three. It is withdrawn from the headline set here and listed with
              the reason.

The replication verdicts are read from notes/replication/round2/comparison_round2.csv so
that the REPLICATED tag is never asserted by hand.
"""
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"
REP = ROOT / "notes" / "replication" / "round2" / "comparison_round2.csv"
OUTD = ROOT / "data" / "release"

# The headline set: everything a reader could meet in the abstract, the introduction or a
# headline table. `sealed_id` links to the replication comparison where one exists.
HEADLINE = [
    # ---- the central object
    dict(id="sovereign_share_union", label="The state holds 0.794 of the wage leg "
         "(agreed range 0.778 to 0.804)", value="0.794",
         sealed_id="labour_backing.sovereign_union", section="4"),
    dict(id="ai_leg_federal_share", label="The state holds 0.010 of the AI leg "
         "(range 0.0095 to 0.0102)", value="0.010", sealed_id=None, section="8",
         tag_override="SCENARIO",
         why="conditional on the AI equity scale, and a lower bound on the AI leg because "
             "off-balance-sheet financing is unmeasured"),
    dict(id="holder_gap", label="The holder gap, wage leg share minus AI leg share",
         value="0.784", sealed_id=None, section="1",
         tag_override="STANDING",
         why="arithmetic on one REPLICATED and one SCENARIO input; it inherits the weaker "
             "tag of its inputs on the AI side and is reported with both ranges"),
    # ---- the fiscal condition
    dict(id="R_2026", label="Retained wage share R in 2026", value="0.568316",
         sealed_id="fiscal.R_2026", section="5"),
    dict(id="condition_passes", label="The fiscal condition fails at the operative tau_k",
         value="false", sealed_id="fiscal.condition_passes", section="5"),
    dict(id="tau_k_sourced_low", label="Sourced effective capital tax rate, low",
         value="0.03245", sealed_id="fiscal.tau_k_sourced_low", section="5"),
    dict(id="tau_k_sourced_high", label="Sourced effective capital tax rate, high",
         value="0.20351", sealed_id="fiscal.tau_k_sourced_high", section="5"),
    dict(id="required_tau_k", label="Required capital tax rate to close the condition, "
         "0.110 to 0.137, above the operative 0.0708 and below the sourced top",
         value="0.110 to 0.137", sealed_id=None, section="5",
         tag_override="STANDING",
         why="the replicator confirmed the DIRECTION and both halves of the verdict; the "
             "grid itself has no sealed counterpart"),
    dict(id="debt_to_gdp_start", label="Debt to GDP, start", value="1.214121",
         sealed_id="debt.debt_to_gdp_start", section="5"),
    dict(id="baseline_20y_em", label="Emerging market 20-year baseline debt path",
         value="376.74 pct", sealed_id="debt.baseline_20y_emerging_market", section="9"),
    # ---- the labour backing scaffold
    dict(id="home_mortgage_backing", label="Home mortgage labour backing",
         value="0.840223", sealed_id="labour_backing.backing.home_mortgage",
         section="4"),
    dict(id="multifamily_backing", label="Multifamily mortgage labour backing",
         value="0.72754", sealed_id="labour_backing.backing.multifamily_rent",
         section="4"),
    dict(id="direct_ratio", label="Direct labour backing ratio", value="0.270271",
         sealed_id=None, section="4", tag_override="STANDING",
         why="NOT comparable across the two rebuilds. The replicator's 0.168 differs almost "
             "entirely through the TOTAL-CLAIMS denominator, 212,644bn against our "
             "149,407bn, driven by corporate equity at a 2026Q2 market value of 123,687bn "
             "against our 2025 annual 71,995bn. The numerator agrees; the denominator is a "
             "different vintage of an asset-price series"),
    # ---- households and incidence
    dict(id="federal_student_share", label="Federal share of the student loan book",
         value="0.972808", sealed_id="sovereign.federal_student_share", section="5"),
    dict(id="under_reporting_factors", label="The four survey under-reporting factors",
         value="4 factors", sealed_id="under_reporting.mortgage", section="3"),
    dict(id="incidence_count_spread", label="Incidence moves household counts by 5 to 9 "
         "percent, so the count figures are robust to it",
         value="1.049 to 1.092", sealed_id=None, section="6",
         tag_override="REMOVED",
         why="NOT REPRODUCIBLE. The replicator's most natural reading of case (c) gives a "
             "spread of 59 percent, which removes the robustness the claim rests on. The "
             "brief does not say which reading is intended. Until it does, the sentence "
             "must not be published"),
    # ---- the dose-response table
    dict(id="terminal_loss_10pct", label="Terminal-year fiscal loss at the 10 percent dose",
         value="85.168bn",
         sealed_id="fiscal_magnitudes.terminal_year_loss_bn_at_10pct", section="7"),
    dict(id="terminal_loss_25pct", label="Terminal-year fiscal loss at the 25 percent dose",
         value="301.89bn", sealed_id=None, section="7",
         tag_override="SCENARIO",
         why="outside the observed data for the embodied group. Item 2 withdraws the point "
             "estimate there and replaces it with a band; the cognitive rows survive as "
             "point estimates at this dose and the embodied row does not"),
    dict(id="rho_50pct", label="The reemployment rate at the 50 percent dose",
         value="n/a", sealed_id=None, section="7",
         tag_override="REMOVED",
         why="THERE IS NO SUCH NUMBER. Item 2: at a 50 percent dose no exposure type has a "
             "fixed point inside the observed range of rho, and the embodied group has no "
             "admissible fixed point at all. Only the band 0 to 0.49 can be reported"),
    dict(id="federal_share_first_round", label="Federal share of first-round losses, "
         "by dose: 0.785 to 0.870 at 10 percent, 0.855 to 0.925 at 50 percent, narrow "
         "reading", value="by dose", sealed_id=None, section="7",
         tag_override="STANDING",
         why="item 4. The replicator's independent by-dose result, 0.78 rising to 0.90, "
             "sits inside our range at both ends, but the sealed object was a min and max "
             "over an unstated sweep and so has no clean sealed counterpart"),
    dict(id="demand_event_first_share", label="The demand event is 0.7407 of the first "
         "round", value="0.740741",
         sealed_id="second_round.demand_event_first_share", section="7"),
    dict(id="second_round_levels", label="Second-round bank losses, 173bn to 1,565bn",
         value="173 to 1565bn", sealed_id=None,
         section="7", tag_override="SCENARIO",
         why="the replicator reproduced the FACTOR of nine and the construction, and missed "
             "the LEVELS by 5.77 percent through one input; the levels are conditional on "
             "the dose and on a convex mapping that is assumed, not measured"),
    # ---- the agency book
    dict(id="gse_retained", label="Retained agency loss at the 10 percent dose, 3.3 to "
         "12.5 percent of Enterprise net worth", value="5.85 to 22.48bn", sealed_id=None,
         section="9", tag_override="STANDING",
         why="item 1, rebuilt loan class by loan class from the 2025 Form 10-Ks. It "
             "SUPERSEDES the published 29.7 percent, which was a gross loss before any "
             "transfer. No sealed counterpart exists; the replicator asked for one"),
    dict(id="gse_beyond", label="Treasury draw on the agency book", value="0 at every dose",
         sealed_id=None, section="9", tag_override="STANDING",
         why="item 1. Now a result rather than dead code: 179.4bn of capital against a "
             "maximum retained first-round loss of 109.0bn, on the statutory negative-net-"
             "worth trigger. FIRST ROUND ONLY, house prices held fixed"),
    # ---- the taxation argument
    dict(id="break_even_case_A", label="Break-even capital tax rate, case A, 0.125 to 0.301",
         value="0.125 to 0.301", sealed_id="cases.break_even_tau_k_case_A_max",
         section="9", tag_override="SCENARIO",
         why="the formula and every bound reproduce; the replicator's grid did not span R "
             "down to zero, so the MAXIMUM did not match. It is a break-even under an "
             "assumed output path"),
    dict(id="break_even_case_B", label="Break-even capital tax rate, case B, 0.182 to 0.650",
         value="0.182 to 0.650", sealed_id=None, section="9", tag_override="SCENARIO",
         why="same construction, output falling. All eight bounds hold, zero breaches"),
    # ---- what the replicator could not attempt
    dict(id="hedge_ratio_at_operative", label="Share of the federal wage loss hedged at the "
         "operative tau_k", value="0.36", sealed_id=None, section="8",
         tag_override="REMOVED",
         why="the input `surplus` is UNDEFINED in the brief. The replicator computed 0.5447 "
             "from a self-consistent reading that satisfies our own stated check, and "
             "back-solving from 0.36 implies a surplus we never defined. Insufficiency "
             "I-12. Cannot be a headline until `surplus` is defined"),
    dict(id="quintile_labour_backed_Q1", label="Bottom-quintile labour-backed claims per "
         "wage dollar", value="4.1489", sealed_id=None, section="6",
         tag_override="REMOVED",
         why="the replicator's independent rebuild lands at 1.21 to 1.64, a factor of 2.5 "
             "to 3.4 away. The universe and normalisation of this object are defined "
             "nowhere in the brief. The Q5 figure is within 13 to 18 percent and survives; "
             "Q1 does not"),
    dict(id="exposure_index_scores", label="The two cognitive index scores by occupation",
         value="various", sealed_id=None, section="3",
         tag_override="REMOVED",
         why="eleven mismatches, the replicator's largest unexplained cluster, running in "
             "OPPOSITE directions on the two indices so it is not a single weighting error. "
             "Two strong controls pass, so the wage machinery is right and the index scores "
             "are not settled. Cannot be a headline until the occupation-level index table "
             "is published and checked"),
]

LIMITATIONS = [
    dict(id="L1", title="Off-balance-sheet and GPU-backed AI financing is unmeasured",
         text="The AI leg is built from nine SEC registrants' us-gaap facts, which is "
              "on-balance-sheet Tier 2 only. BIS QR March 2026 identifies off-balance-sheet "
              "SPV structures as dominant in data centre financing, and none of them appear "
              "in these filings. GPU-backed lending and data centre ABS and CMBS are "
              "likewise absent. Every AI-leg level in this paper is therefore a labelled "
              "LOWER BOUND, and every federal share of the AI leg is correspondingly an "
              "UPPER bound. The 5 percent kill criterion in the project brief is not "
              "evaluable until Tier 1 and Tier 2b exist. We do not know the sign of the "
              "error on the holder gap, only that the gap is measured against a leg we can "
              "only bound from below."),
    dict(id="L2", title="Capital gains receipts are unsourced",
         text="The labour-linked share of federal receipts splits the individual income tax "
              "using the SOI wage share of AGI, available for 2021 to 2023 only. Realised "
              "capital gains are inside AGI and inside the individual income tax, and we do "
              "not separate them. That makes the labour-linked share of receipts, 0.657788 "
              "on the Treasury class, an overstatement of the labour share in years with "
              "large realisations and an understatement in years without. The 77.7 percent "
              "upper bound is carried throughout as the alternative reading and moves the "
              "sovereign share by 0.71 percent, so the headline is not sensitive to it. The "
              "fiscal magnitudes are more sensitive and we have not bounded that."),
    dict(id="L3", title="The labour backing ratio's novelty is 'none located', pending a "
                        "systematic search",
         text="The claim that no published work constructs a labour backing ratio over the "
              "whole claim structure rests on a NON-SYSTEMATIC search. It is 'none located', "
              "not 'none exists'. A PRISMA-protocol search for this specific question, with "
              "databases, query strings, dates and counts at each stage, has not been run "
              "and is stated as future work. The related-work audit did locate prior work on "
              "the FISCAL MECHANISM and that priority claim has already been retired; the "
              "same could happen here."),
    dict(id="L4", title="The holder proxy residual",
         text="The mortgage holder split reads three of four shares from a publisher and "
              "takes the fourth, 24.88 percent or 3,259bn, as the arithmetic remainder. It "
              "is treated as PRIVATE in full, which is the conservative choice for the "
              "sovereign claim: any federal fraction inside it would raise the federal share "
              "rather than lower it. We have not identified what is in it. The same "
              "structure appears on the AI leg, where a residual_unallocated holder class "
              "carries 1.6 percent of the wage leg and 9.8 percent of the AI leg."),
    dict(id="L5", title="Effective labour tax rates by income are not taken from CBO",
         text="tau_l is a single economy-wide effective rate, built bottom-up as federal "
              "taxes over FRED WASCUR wages and salaries, with a top-down alternative "
              "carried alongside. It does not vary by position in the wage distribution. CBO "
              "publishes effective federal tax rates by income group and we have not used "
              "them. Because displacement is not uniform across the wage distribution, and "
              "because the incidence section shows it concentrated away from the top, a flat "
              "rate probably OVERSTATES the revenue loss from displacing low-wage workers "
              "and understates it from displacing high-wage workers. We have not signed or "
              "bounded the net effect."),
]


def main():
    rep = pd.read_csv(REP)
    verdict = dict(zip(rep.quantity_id, rep.verdict))
    # A sealed_id that does not resolve would silently downgrade a REPLICATED claim to
    # STANDING, which is the quiet failure this whole pass exists to prevent.
    missing = [h["sealed_id"] for h in HEADLINE
               if h.get("sealed_id") and h["sealed_id"] not in verdict]
    if missing:
        raise SystemExit("sealed_id does not resolve in the comparison file: "
                         + ", ".join(missing))

    rows = []
    for h in HEADLINE:
        v = verdict.get(h.get("sealed_id")) if h.get("sealed_id") else None
        if h.get("tag_override"):
            tag, why = h["tag_override"], h.get("why", "")
        elif v and v.startswith("MATCH"):
            tag, why = "REPLICATED", f"round two: {v}"
        elif v:
            tag, why = "STANDING", (f"round two verdict was {v}; measured and unchallenged "
                                    "on substance")
        else:
            tag, why = "STANDING", "no sealed counterpart; measured and unchallenged"
        rows.append({"id": h["id"], "section": h["section"], "claim": h["label"],
                     "value": h["value"], "tag": tag,
                     "sealed_id": h.get("sealed_id") or "", "round2_verdict": v or "",
                     "basis": why})
    H = pd.DataFrame(rows)
    OUTD.mkdir(parents=True, exist_ok=True)
    H.to_csv(OUTD / "headline_clearing_pass.csv", index=False)
    pd.DataFrame(LIMITATIONS).to_csv(OUTD / "stated_limitations.csv", index=False)

    counts = H.tag.value_counts().to_dict()
    (OUTD / "headline_clearing_pass.json").write_text(json.dumps({
        "counts": counts,
        "headline_set_size": int((H.tag != "REMOVED").sum()),
        "removed": H[H.tag == "REMOVED"][["id", "claim", "basis"]].to_dict("records"),
        "limitations": [l["id"] + ": " + l["title"] for l in LIMITATIONS],
    }, indent=2))

    pd.set_option("display.width", 250)
    pd.set_option("display.max_colwidth", 62)
    print("CLEARING PASS")
    print(counts)
    for tag in ("REPLICATED", "STANDING", "SCENARIO", "REMOVED"):
        sub = H[H.tag == tag]
        print(f"\n=== {tag} ({len(sub)}) ===")
        print(sub[["section", "claim", "value"]].to_string(index=False))
    print("\n=== REMOVED, with reasons ===")
    for r in H[H.tag == "REMOVED"].itertuples():
        print(f"  {r.id}: {r.basis}")


if __name__ == "__main__":
    main()
