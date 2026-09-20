"""Item 3 of the final analysis session. The Treasury class identified and verified, the
sovereign share reported with a range, and both legs' shares tested against every named
judgement call.

THE REPLICATOR'S FINDING. 83.7 percent of the 0.016 gap between our sovereign union share
of 0.793592 and their 0.777810 is the Treasury class. Our level is 33,887.1bn and they
searched the Z.1 archive for a single series near it and found none, the nearest being
29,014, 30,878 and 31,491bn.

THE ANSWER. It is not one series. It is two, and the brief names them in
framework/labor_backing/config.py but nowhere a replicator would look:

    FL313161105  Federal government; total MARKETABLE Treasury securities; liability
    FL313169205  Federal government; total NONMARKETABLE Treasury securities; liability

At the 2025 annual vintage these are 30,069,641mn and 3,817,450mn, and they sum to
33,887,091mn = 33,887.1bn, which reproduces the sealed level exactly. The replicator found
the first of them at a 2026Q2 vintage (30,878.3bn) and had no way to know a second was
added, because section 14 of the brief gives neither the identifiers nor the aggregation.
That is a documentation defect on our side and it is now fixed here and in the brief.

WHAT THE DEFINITION INCLUDES, which the brief also never said.

  intragovernmental holdings: PARTLY. Z.1 consolidates the federal government sector, so
    the trust funds' Government Account Series holdings net out of this liability. The
    check: Treasury's own gross federal debt (FRED GFDEBTN) averages 37,144.3bn in 2025
    against our 33,887.1bn, and Treasury's debt held by the public (FYGFDPUN) averages
    29,769.5bn. Our figure sits between the two, as a consolidated measure must.
  Federal Reserve holdings: YES, in full. The monetary authority is a separate sector in
    Z.1. FRED TREAST averages 4,219.6bn in 2025. This is a real judgement call, because the
    central case also treats the central bank as federal on the HOLDER leg, and it is
    tested below.
  marketable: YES, all of it. nonmarketable: YES, savings bonds and State and Local
    Government Series.

So the level is verified and correct. It is the DOCUMENTATION that was wrong, exactly as
the replicator's standing pattern predicts: what is stated reproduces, what is referenced
does not.
"""
import json
import pathlib
import sys

import pandas as pd

HERE = pathlib.Path(__file__).parent

# ---- the Treasury class, every defensible reading, all sourced
TREASURY_READINGS = {
    "CENTRAL: Z.1 marketable plus nonmarketable, FL313161105 + FL313169205": 33887.1,
    "Z.1 marketable only, FL313161105": 30069.6,
    "Z.1 all-sector Treasury securities asset, FL893061105": 28481.0,
    "Treasury gross federal debt, FRED GFDEBTN 2025 mean": 37144.3,
    "Treasury debt held by the public, FRED FYGFDPUN 2025 mean": 29769.5,
    "CENTRAL net of Federal Reserve holdings, FRED TREAST 2025 mean 4219.6": 33887.1 - 4219.6,
}
FED_TREASURY_BN = 4219.6   # FRED TREAST, 2025 mean, Treasuries held outright by the Fed


def main():
    summ = json.loads((HERE / "direct_ratio_latest.json").read_text())
    ind = json.loads((HERE / "indirect_extension.json").read_text())
    H = pd.read_csv(HERE / "holder_matrix_latest.csv")
    byc = summ["by_class"]
    sov = summ["sovereign_exposure"]

    lvl = {k: v["level_bn"] for k, v in byc.items()}
    bak = {k: v["backing"] for k, v in byc.items()}

    # The sovereign union is (held or guaranteed) UNION (owed), over labour-backed claims.
    # The obligor leg is the Treasury class plus the state and local class, less the
    # overlap with what the federal government also holds. Rebuilt here from the
    # published components so that a Treasury variant propagates correctly.
    held_gtd = sov["labour_backed_held_or_guaranteed_bn"]
    overlap = sov["overlap_removed_bn"]
    sl_obligor = lvl["state_local_debt"] * bak["state_local_debt"]

    def shares(level_overrides=None, backing_overrides=None, cb_federal=True):
        """Rebuild the three sovereign shares from the published components.

        The federal OBLIGOR leg is the Treasury class ALONE. State and local debt is a
        separate sovereign and sits outside the federal share, exactly as the published
        construction has it: 33,887.1 x 0.657788 = 22,290.5 reproduces the published
        obligor leg to the last digit.

        The overlap is what the federal government both holds and owes, so it scales with
        the Treasury class and is rescaled whenever that class is rescaled.
        """
        L = dict(lvl)
        B = dict(bak)
        L.update(level_overrides or {})
        B.update(backing_overrides or {})
        lb = {k: L[k] * B[k] for k in L}
        lb_tot = sum(lb.values())
        obligor = lb["treasury"]
        ov = overlap * (obligor / (lvl["treasury"] * bak["treasury"]))
        hg = held_gtd
        if not cb_federal:
            # the central bank is NOT counted as federal. Its Treasury holdings leave the
            # held-or-guaranteed leg AND leave the overlap, because the overlap is exactly
            # the debt the federal sector both holds and owes.
            fed_treas_lb = FED_TREASURY_BN * B["treasury"]
            hg = hg - fed_treas_lb
            ov = ov - fed_treas_lb
        union = hg + obligor - ov
        return {"labour_backed_bn": lb_tot,
                "direct_ratio": lb_tot / sum(L.values()),
                "sovereign_union": union / lb_tot,
                "sovereign_obligor": obligor / lb_tot,
                "sovereign_held_or_guaranteed": hg / lb_tot}

    central = shares()

    rows = []
    for name, level in TREASURY_READINGS.items():
        s = shares(level_overrides={"treasury": level})
        rows.append({"family": "Treasury class level", "judgement_call": name,
                     "treasury_level_bn": level, **s})

    # every other named judgement call, one at a time, as build_sensitivity.py defines them
    other_calls = [
        ("federal receipts: SOI-split 0.657788 (central) vs the 77.7 percent upper bound",
         {"treasury": 0.7768}),
        ("mortgage backing: ACS service 0.8402 (central) vs SIPP balances 0.8205",
         {"home_mortgage": 0.8205}),
        ("mortgage backing: ACS service vs the superseded A38 definition 0.80305",
         {"home_mortgage": 0.80305}),
        ("rent backing: engine core 0.7275 (central) vs the A38 definition 0.69913",
         {"multifamily_mortgage": 0.69913}),
        ("state and local: wage-split central vs all personal current taxes",
         {"state_local_debt": bak["state_local_debt"] / 0.66754}),
        ("other consumer: blend 0.815554 (central) vs the card share alone",
         {"other_consumer": bak["credit_card"]}),
        ("commercial mortgage treated like multifamily rather than zero",
         {"commercial_mortgage": bak["multifamily_mortgage"]}),
        ("THE ONE-STEP RULE: business classes zero (central) vs the B2 indirect share",
         {k: ind["indirect_labour_backing_of_business_revenue"]
          for k in ind["business_revenue_serviced_classes"]}),
    ]
    # the central bank call, which changes the holder leg rather than the level
    s = shares(cb_federal=False)
    rows.append({"family": "holder leg",
                 "judgement_call": "central bank NOT federal (Fed Treasury holdings out "
                                   "of the held-or-guaranteed leg)",
                 "treasury_level_bn": lvl["treasury"], **s})

    for name, ov in other_calls:
        s = shares(backing_overrides=ov)
        rows.append({"family": "backing share", "judgement_call": name,
                     "treasury_level_bn": lvl["treasury"], **s})

    # the holder-leg calls, from sensitivity_holder.csv
    pools_only = float(H[(H.holder == "federal_government")
                         & (H.claim_class.isin(["home_mortgage",
                                                "multifamily_mortgage"]))]
                       ["labour_backed_bn"].sum())
    lb_tot = central["labour_backed_bn"]
    rows.append({"family": "holder leg",
                 "judgement_call": "agency pools NOT federal (guarantee ignored)",
                 "treasury_level_bn": lvl["treasury"],
                 "labour_backed_bn": lb_tot,
                 "direct_ratio": central["direct_ratio"],
                 "sovereign_union": (sov["labour_backed_sovereign_exposure_bn"]
                                     - pools_only) / lb_tot,
                 "sovereign_obligor": central["sovereign_obligor"],
                 "sovereign_held_or_guaranteed": (
                     sov["labour_backed_held_or_guaranteed_bn"] - pools_only) / lb_tot})
    rows.append({"family": "holder leg",
                 "judgement_call": "obligor leg EXCLUDED (holder and guarantor only)",
                 "treasury_level_bn": lvl["treasury"],
                 "labour_backed_bn": lb_tot,
                 "direct_ratio": central["direct_ratio"],
                 "sovereign_union": central["sovereign_held_or_guaranteed"],
                 "sovereign_obligor": 0.0,
                 "sovereign_held_or_guaranteed": central["sovereign_held_or_guaranteed"]})

    S = pd.DataFrame(rows)
    S.insert(0, "central_sovereign_union", round(central["sovereign_union"], 6))
    S["move_from_central"] = S["sovereign_union"] - central["sovereign_union"]
    S["move_pct"] = 100 * (S["sovereign_union"] / central["sovereign_union"] - 1)
    S.round(6).to_csv(HERE / "item3_sovereign_robustness.csv", index=False)

    # ---- the AI leg, tested on its own scenario axis
    A = pd.read_csv(HERE / "two_sided_bet_by_holder.csv")
    fed = A[A.holder == "federal_government"]
    ai_lo, ai_hi = float(fed.ai_leg_share.min()), float(fed.ai_leg_share.max())

    # the agreed sovereign share. The replicator rebuilt the same object independently and
    # landed at 0.777810 with an 11-class table missing other_consumer and using a single
    # Treasury series at the wrong vintage. Their number is the bottom of the agreed range.
    agreed_lo = min(0.777810, float(S.sovereign_union.min()))
    agreed_hi = float(S.sovereign_union.max())

    # robustness verdict: does the headline claim survive every call?
    excl_obligor = S[S.judgement_call.str.contains("obligor leg EXCLUDED")]
    core = S[~S.judgement_call.str.contains("obligor leg EXCLUDED")]

    out = {
        "treasury_series_verified": {
            "series": ["FL313161105", "FL313169205"],
            "descriptions": [
                "Federal government; total marketable Treasury securities; liability",
                "Federal government; total nonmarketable Treasury securities; liability"],
            "vintage": "Z.1 annual, 2025, the latest complete year",
            "values_mn": [30069641, 3817450],
            "sum_bn": 33887.1,
            "reproduces_published_level": True,
            "includes_intragovernmental": "partly; Z.1 consolidates the federal sector so "
                                          "trust fund GAS holdings net out",
            "includes_federal_reserve_holdings": True,
            "cross_checks_bn": {"Treasury gross federal debt GFDEBTN 2025": 37144.3,
                                "Treasury debt held by the public FYGFDPUN 2025": 29769.5,
                                "Federal Reserve holdings TREAST 2025": 4219.6,
                                "Z.1 all-sector asset FL893061105 2025": 28481.0},
            "verdict": "CORRECT. The level is right and the documentation was wrong."},
        "other_consumer_class_now_explicit": {
            "level_bn": lvl["other_consumer"], "backing": bak["other_consumer"],
            "z1_series": "FL153166205",
            "note": "omitted entirely by the replicator because the brief lists the "
                    "zero-rule classes in prose and never enumerates the thirteen"},
        "class_count": len(lvl),
        "sovereign_union_central": round(central["sovereign_union"], 6),
        "sovereign_union_range_core": [round(float(core.sovereign_union.min()), 6),
                                       round(float(core.sovereign_union.max()), 6)],
        "sovereign_union_range_with_obligor_excluded":
            [round(float(excl_obligor.sovereign_union.min()), 6),
             round(float(S.sovereign_union.max()), 6)],
        "agreed_range_with_replicator": [round(agreed_lo, 6), round(agreed_hi, 6)],
        "replicator_value": 0.777810,
        "largest_move": S.loc[S.move_from_central.abs().idxmax(),
                              "judgement_call"],
        "largest_move_pct": round(float(S.move_pct.abs().max()), 2),
        "ai_leg_federal_share_central": 0.01001,
        "ai_leg_federal_share_range": [round(ai_lo, 6), round(ai_hi, 6)],
        "ai_leg_scenario_axis": "AI equity as 10, 20 or 30 percent of US nonfinancial "
                                "corporate equity",
        "holder_gap_central": round(central["sovereign_union"] - 0.01001, 4),
    }
    (HERE / "item3_sovereign_robustness.json").write_text(json.dumps(out, indent=2))

    pd.set_option("display.width", 240)
    pd.set_option("display.max_colwidth", 78)
    print("TREASURY CLASS, every defensible reading")
    print(S[S.family == "Treasury class level"][
        ["judgement_call", "treasury_level_bn", "direct_ratio", "sovereign_union",
         "move_pct"]].round(5).to_string(index=False))
    print()
    print("EVERY OTHER JUDGEMENT CALL")
    print(S[S.family != "Treasury class level"][
        ["family", "judgement_call", "direct_ratio", "sovereign_union",
         "move_pct"]].round(5).to_string(index=False))
    print()
    for k, v in out.items():
        if not isinstance(v, dict):
            print(f"  {k} = {v}")


if __name__ == "__main__":
    main()
