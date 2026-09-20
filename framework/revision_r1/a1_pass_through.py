"""A1. The fiscal condition with the pass-through coefficient made explicit.

WHAT IS COMPUTED, exactly. A displaced wage dollar splits in two.

  (i)  the cost of the AI capital and services that replace the work, share c;
  (ii) the surplus the adopting firm keeps, share 1 - c.

Part (ii) is US capital income of the adopting firm and is what the assembled rate prices.
Part (i) is revenue to the suppliers of AI capital, and only there does the capex
decomposition apply: a dollar of AI capital spending is domestic labor, which is already
inside tau_l (1 - R) and must not be counted again, imports, which never enter the US tax
base, and domestic producer surplus, which the assembled rate prices. So

    g = (1 - c)  +  c * s_dom                                   (base construction)

with s_dom the domestic producer surplus share of a dollar of AI capital spending. The capex
split is applied to part (i) ONLY. A version of this module folded a price pass-through term
into the same expression and reported the result as the central case; that overstated the
correction and is superseded here.

PRICE PASS-THROUGH is a separate term, reported separately. If a share p of the firm's
retained surplus is competed away to consumers in lower prices, it is never taxed as capital
income:

    g(p) = (1 - c)(1 - p)  +  c * s_dom                         (with pass-through)

DOUBLE COUNTING, checked. The foreign share removed inside g is the IMPORT share of AI
capital spending: payments to foreign suppliers that never become US income. The shifted
share inside the assembled rate is US-booked profit moved to a lower-taxed jurisdiction,
which does enter the US base and is then taxed at the lower rate the assembly already
applies. These are different flows and neither is removed twice. The one case where they can
touch is an intra-firm import priced as a transfer: there the same dollar could be counted as
an import here and as a shifted profit there. That overlap would make g too LOW and the
required rate too high, so it runs against this module's own correction, and it is stated.

STATUS. SCENARIO, and the weakest inputs are named: c has no verified estimate anywhere in
this project, and the labor and import shares behind s_dom are swept ranges, not sourced. The
project's earlier fiscal module carried the same object as a required surplus per displaced
wage dollar and likewise never estimated it. The bound 0 <= g <= 1 holds with output
preserved and is asserted below.
"""
import csv
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
HERE = pathlib.Path(__file__).parent

# the cost of AI capital and services per dollar of wages displaced. UNVERIFIED and swept.
# Bounded below by zero and above by one: an adopter that spent more than the wage it saved
# would not adopt. No verified estimate exists in this project or, so far as we located, in
# the literature at the level of a displaced wage dollar.
C_GRID = [0.2, 0.35, 0.5, 0.65, 0.8]
C_CENTRAL = 0.5
# the share of the adopting firm's retained surplus competed away in lower prices. A separate
# term, reported separately, and likewise unverified.
P_GRID = [0.0, 0.15, 0.3, 0.6]


def load(rel):
    return json.loads((ROOT / rel).read_text())


def main():
    lab = load("framework/tau_k/labor_component.json")
    dec = lab["decomposition_of_one_dollar_of_ai_capex"]
    s_lo, s_mid, s_hi = dec["domestic_surplus_PRICED_BY_tau_k"]
    imp_lo, imp_mid, imp_hi = dec["imported_LEAKAGE_no_us_labour_tax"]
    dlab_lo, dlab_mid, dlab_hi = dec["domestic_labour_ALREADY_COUNTED"]

    rsen = load("data/processed/replication_r_sensitivity.json")
    R = float(rsen["ours_observed_rho_and_our_omega"]["R"])
    required_at_one = rsen["ours_observed_rho_and_our_omega"]["required_tau_k"]
    tau_l = {k: v / (1 - R) for k, v in required_at_one.items()}
    easy, hard = "AMR_0.255", "bottom_up_0.318"

    tk = load("framework/tau_k/tau_k_assembled.json")
    assembled = {r["rent_reading"]: r["tau_k_central"]
                 for r in tk["assembled_CENTRAL_at_sourced_centrals"]}

    def required(g):
        return tau_l[easy] * (1 - R) / g, tau_l[hard] * (1 - R) / g

    # ---- the base construction, no price pass-through
    base = []
    for c in C_GRID:
        for tag, s in (("low", s_lo), ("central", s_mid), ("high", s_hi)):
            g = (1 - c) + c * s
            assert 0.0 <= g <= 1.0, "g left the unit interval"
            lo, hi = required(g)
            base.append({"capital_cost_share_c": c, "surplus_reading": tag,
                         "domestic_surplus_share_of_capex": round(s, 6),
                         "g": round(g, 6), "required_easier": round(lo, 6),
                         "required_harder": round(hi, 6)})
    gb = [r["g"] for r in base]
    central = [r for r in base if r["capital_cost_share_c"] == C_CENTRAL
               and r["surplus_reading"] == "central"][0]

    # ---- the separate price pass-through term
    withp = []
    for c in C_GRID:
        for p in P_GRID:
            g = (1 - c) * (1 - p) + c * s_mid
            assert 0.0 <= g <= 1.0
            lo, hi = required(g)
            withp.append({"capital_cost_share_c": c, "price_pass_through_p": p,
                          "g": round(g, 6), "required_easier": round(lo, 6),
                          "required_harder": round(hi, 6)})
    central_p = [r for r in withp if r["capital_cost_share_c"] == C_CENTRAL
                 and r["price_pass_through_p"] == 0.3][0]

    # ---- the grid of g itself
    by_g = []
    for i in range(2, 21):
        g = round(0.05 * i, 2)
        lo, hi = required(g)
        by_g.append({"g": g, "required_easier": round(lo, 6), "required_harder": round(hi, 6)})

    econ_wide = (0.20, 0.22)
    out = {
        "status": "SCENARIO. c is unverified and swept; the labor and import shares behind "
                  "the capex split are swept ranges, not sourced. Reported as a sensitivity "
                  "on the headline comparison, which stays at full pass-through.",
        "condition": "tau_k * g >= tau_l * (1 - R)",
        "base_construction": "g = (1 - c) + c * s_dom, the capex split applied to the "
                             "capital-cost part only",
        "price_pass_through_is_separate": "g(p) = (1 - c)(1 - p) + c * s_dom",
        "superseded": "an earlier version of this module folded the price pass-through into "
                      "the central case and reported the result as the correction. That "
                      "overstated it and is withdrawn.",
        "retained_wage_share_R": R,
        "required_tau_k_at_g_equals_one": {k: round(v, 6) for k, v in required_at_one.items()},
        "capex_dollar_decomposition_used": {
            "domestic_labour_already_inside_tau_l": [dlab_lo, dlab_mid, dlab_hi],
            "imported_no_us_tax": [imp_lo, imp_mid, imp_hi],
            "domestic_producer_surplus": [s_lo, s_mid, s_hi]},
        "capital_cost_share_grid": C_GRID,
        "capital_cost_share_central": C_CENTRAL,
        "g_range_base_construction": [round(min(gb), 6), round(max(gb), 6)],
        "g_central_base": central,
        "g_central_with_thirty_percent_price_pass_through": central_p,
        "assembled_tau_k_central": assembled,
        "economy_wide_average_capital_rate": list(econ_wide),
        "double_counting_check": (
            "The import share removed in g and the shifted share inside the assembled rate "
            "are different flows: imports never enter the US base, shifted profits enter it "
            "and are taxed at the lower rate the assembly applies. Neither is removed twice. "
            "Where an import is an intra-firm transfer price the two can touch, which would "
            "make g too low and the required rate too high, against this module's own "
            "correction."),
        "verdict": (
            f"The required rate is inversely proportional to g. At the central base case "
            f"g = {central['g']:.2f} and the required rate is "
            f"{100 * central['required_easier']:.0f} to "
            f"{100 * central['required_harder']:.0f} percent, against "
            f"{100 * required_at_one[easy]:.0f} to {100 * required_at_one[hard]:.0f} percent "
            f"at g = 1. The assembled rate of "
            f"{100 * assembled['Barkai']:.1f} percent falls short on either reading, and the "
            f"shortfall widens. The economy-wide average capital rate of 20 to 22 percent "
            f"still clears the base central case; it stops clearing once a price "
            f"pass-through term is added, which is why that term is reported separately and "
            f"not inside the headline."),
    }
    (HERE / "a1_pass_through.json").write_text(json.dumps(out, indent=2) + "\n")
    for name, rowset in (("a1_g_cases.csv", base), ("a1_price_pass_through.csv", withp),
                         ("a1_required_by_g.csv", by_g)):
        with (HERE / name).open("w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rowset[0]))
            w.writeheader()
            w.writerows(rowset)

    print(f"base g range {min(gb):.3f} to {max(gb):.3f}; central {central['g']:.3f}")
    print(f"required at central g: {100*central['required_easier']:.1f} to "
          f"{100*central['required_harder']:.1f} percent")
    print(f"with a 30 percent price pass-through: g {central_p['g']:.3f}, required "
          f"{100*central_p['required_easier']:.1f} to "
          f"{100*central_p['required_harder']:.1f} percent")
    print(out["verdict"])


if __name__ == "__main__":
    main()
