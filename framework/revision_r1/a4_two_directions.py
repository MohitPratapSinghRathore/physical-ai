"""A4. The two-directions claim, tested.

THE CLAIM UNDER TEST. The paper has said that one capital tax rate is being asked to do two
opposite jobs: raised, it closes the revenue gap after displacement; raised, it also
increases what the state loses when AI capital income falls. That is a claim about a
trade-off, and a trade-off has to be sized.

THE ARITHMETIC. Let B be US AI capital income in the success state and B' the same quantity
in a bust, with a fall of dB = B - B'. At an effective rate tau the state collects tau * B
in the success state and loses tau * dB in a bust. Both are linear in tau, so:

  1. Revenue at risk in a bust rises one for one with the rate. Moving the rate from the
     assembled level to the level that would close the displacement-side condition
     multiplies bust-state revenue at risk by that ratio.
  2. The RATIO of bust-state exposure to success-state revenue, dB / B, does not depend on
     the rate at all. Raising the rate does not make the state relatively more exposed to a
     bust; it scales both sides of its position together.

WHY WE CANNOT PUT A DOLLAR FIGURE ON IT. B is the AI capital income base, and this project
has never been able to define it: the same undefined base caused the withdrawal of an
earlier hedging ratio. We therefore report the multipliers, which are exact, and an
illustrative scale from the verified historical receipts falls, labelled as illustrative
because those falls were generated at economy-wide effective rates rather than at the rate
on AI surplus.

STATUS. SCENARIO. The multipliers are arithmetic; the illustrative scale is not a measured
counterfactual.
"""
import csv
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
HERE = pathlib.Path(__file__).parent


def load(rel):
    return json.loads((ROOT / rel).read_text())


def main():
    tk = load("framework/tau_k/tau_k_assembled.json")
    b34 = load("framework/ai_bust/b3_b4_summary.json")
    a1 = load("framework/revision_r1/a1_pass_through.json")

    assembled = {r["rent_reading"]: r["tau_k_central"]
                 for r in tk["assembled_CENTRAL_at_sourced_centrals"]}
    tau_a = assembled["Barkai"]
    req = tk["required_tau_k"]["by_labour_reading"]
    econ_wide = (0.20, 0.22)          # the economy-wide average capital rate, as reported
    req_pt = a1["g_central_case"]     # the required rate once pass-through is explicit

    fall = [abs(x) for x in b34["federal_receipts_fall_bn_range"]]
    fall_lo, fall_hi = min(fall), max(fall)

    rates = [
        ("assembled rate on AI surplus", tau_a, tau_a),
        ("required, easier labor tax reading, full pass-through",
         req["AMR_0.255"], req["AMR_0.255"]),
        ("required, harder labor tax reading, full pass-through",
         req["bottom_up_0.318"], req["bottom_up_0.318"]),
        ("required at the central pass-through case",
         req_pt["required_tau_k_easier"], req_pt["required_tau_k_harder"]),
        ("economy-wide average capital rate", econ_wide[0], econ_wide[1]),
    ]

    rows = []
    for name, lo, hi in rates:
        rows.append({
            "rate_definition": name,
            "rate_low": round(lo, 6), "rate_high": round(hi, 6),
            "multiple_of_assembled_low": round(lo / tau_a, 4),
            "multiple_of_assembled_high": round(hi / tau_a, 4),
            "illustrative_bust_revenue_at_risk_low_bn": round(fall_lo * lo / tau_a, 1),
            "illustrative_bust_revenue_at_risk_high_bn": round(fall_hi * hi / tau_a, 1),
        })

    base_row = rows[0]
    closing = rows[1], rows[2]
    mult_lo = closing[0]["multiple_of_assembled_low"]
    mult_hi = closing[1]["multiple_of_assembled_high"]

    out = {
        "status": "SCENARIO. The multipliers are arithmetic; the dollar scale is "
                  "illustrative and is not a measured counterfactual.",
        "assembled_rate": tau_a,
        "required_rates_full_pass_through": req,
        "required_rates_central_pass_through": {
            "easier": req_pt["required_tau_k_easier"],
            "harder": req_pt["required_tau_k_harder"]},
        "economy_wide_average_capital_rate": list(econ_wide),
        "verified_bust_receipts_fall_bn": [fall_lo, fall_hi],
        "result_1_levels": (
            f"Closing the displacement-side condition at full pass-through means moving the "
            f"rate from {tau_a:.4f} to between {req['AMR_0.255']:.4f} and "
            f"{req['bottom_up_0.318']:.4f}, a multiple of {mult_lo:.2f} to {mult_hi:.2f}. "
            f"Revenue at risk in a bust is linear in the rate, so it rises by the same "
            f"multiple. On the illustrative scale that is an increase of "
            f"{fall_lo * (mult_lo - 1):,.0f} to {fall_hi * (mult_hi - 1):,.0f} billion "
            f"dollars of capital-linked receipts at risk."),
        "result_2_ratio": (
            "The ratio of bust-state exposure to success-state revenue is the fall in the "
            "base over the base itself, and does not depend on the rate. Raising the rate "
            "does not make the state relatively more exposed to a bust."),
        "why_no_dollar_figure": (
            "The AI capital income base is undefined in this project's data. The same gap "
            "caused an earlier hedging ratio to be withdrawn, and it is not closed here."),
        "verdict_on_the_framing": (
            "The trade-off is real in levels and absent in ratio. Because we cannot size the "
            "base, we cannot say the trade-off is material in dollars, and a slogan that "
            "turns on materiality is not supported. 'One rate, two opposite jobs' is "
            "WITHDRAWN and replaced by 'fiscally exposed in both states through different "
            "tax bases', with the proportional result reported alongside."),
    }
    (HERE / "a4_two_directions.json").write_text(json.dumps(out, indent=2) + "\n")
    with (HERE / "a4_rate_grid.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    print(f"assembled {tau_a:.4f}; closing multiple {mult_lo:.2f} to {mult_hi:.2f}")
    for r in rows:
        print(f"  {r['rate_definition']:<52s} {r['rate_low']:.4f}-{r['rate_high']:.4f}  "
              f"x{r['multiple_of_assembled_low']:.2f}-{r['multiple_of_assembled_high']:.2f}")
    print(out["verdict_on_the_framing"])


if __name__ == "__main__":
    main()
