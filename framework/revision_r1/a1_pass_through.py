"""A1. The fiscal condition with the pass-through made explicit.

The condition as the paper has stated it, tau_k >= tau_l (1 - R), implicitly assumes that
every dollar of displaced wages reappears as a dollar of taxable US capital income. Write
that assumption down as a coefficient:

    tau_k * g  >=  tau_l * (1 - R),        required tau_k = tau_l (1 - R) / g

where g is the taxable US capital income generated per dollar of displaced wages. The
paper's published required band is the g = 1 case, which is the most favourable one.

DECOMPOSITION OF g. Per dollar of wages displaced, a firm spends k on AI capital services
and keeps 1 - k. Of what it keeps, a share p is competed away to consumers as lower prices
and is never taxed as capital income. Of the k it spends, the existing capex decomposition
(framework/tau_k/labor_component.json) splits a dollar of AI capital spending into domestic
labor, which is already inside tau_l (1 - R) and must not be counted again, an imported
share, which bears no US tax, and a domestic surplus share, which is what tau_k prices.

    g = (1 - k) (1 - p)  +  k * s_dom

STATUS. SCENARIO. s_dom is taken from the existing swept capex decomposition; k and p are
swept over stated ranges and are not sourced. The bound 0 <= g <= 1 holds with output
preserved: the displaced wage dollar cannot generate more than a dollar of income, and the
parts that are not domestic taxable capital income are labor income, imports or consumer
surplus.
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
HERE = pathlib.Path(__file__).parent


def load(rel):
    return json.loads((ROOT / rel).read_text())


def main():
    lab = load("framework/tau_k/labor_component.json")
    dec = lab["decomposition_of_one_dollar_of_ai_capex"]
    s_dom_lo, s_dom_mid, s_dom_hi = dec["domestic_surplus_PRICED_BY_tau_k"]
    imp_lo, imp_mid, imp_hi = dec["imported_LEAKAGE_no_us_labour_tax"]
    dlab_lo, dlab_mid, dlab_hi = dec["domestic_labour_ALREADY_COUNTED"]

    rsen = load("data/processed/replication_r_sensitivity.json")
    R = float(rsen["ours_observed_rho_and_our_omega"]["R"])
    required_at_one = rsen["ours_observed_rho_and_our_omega"]["required_tau_k"]
    tau_l = {k: v / (1 - R) for k, v in required_at_one.items()}

    tk = load("framework/tau_k/tau_k_assembled.json")
    assembled = {r["rent_reading"]: r["tau_k_central"]
                 for r in tk["assembled_CENTRAL_at_sourced_centrals"]}
    assembled_crs = {r["rent_reading"]: r["tau_k_central"]
                     for r in tk["MARKED_SENSITIVITY_at_CRS_implied_theta"]}

    # ---- the grid of g, and the required rate on it
    grid = [round(0.05 * i, 2) for i in range(2, 21)]      # 0.10 to 1.00
    by_g = []
    for g in grid:
        row = {"g": g}
        for name, tl in tau_l.items():
            row["required_" + name] = round(tl * (1 - R) / g, 6)
        by_g.append(row)

    # ---- g itself, swept over the two unsourced shares
    K = [0.3, 0.5, 0.7]          # AI capital cost per dollar of wages displaced
    P = [0.0, 0.3, 0.6]          # share competed away to consumers as lower prices
    cases = []
    for k in K:
        for p in P:
            for tag, s in (("low", s_dom_lo), ("central", s_dom_mid), ("high", s_dom_hi)):
                g = (1 - k) * (1 - p) + k * s
                assert 0.0 <= g <= 1.0, "g left the unit interval"
                cases.append({
                    "capital_cost_share_k": k, "price_pass_through_p": p,
                    "domestic_surplus_share_of_capex": round(s, 6),
                    "surplus_reading": tag, "g": round(g, 6),
                    "required_tau_k_easier": round(tau_l["AMR_0.255"] * (1 - R) / g, 6),
                    "required_tau_k_harder": round(tau_l["bottom_up_0.318"] * (1 - R) / g, 6),
                })
    gs = [c["g"] for c in cases]
    central = [c for c in cases if c["capital_cost_share_k"] == 0.5
               and c["price_pass_through_p"] == 0.3
               and c["surplus_reading"] == "central"][0]

    out = {
        "status": "SCENARIO. s_dom from the existing swept capex decomposition; k and p "
                  "swept and not sourced. The bound 0 <= g <= 1 holds under output "
                  "preserved and is asserted in the code.",
        "condition": "tau_k * g >= tau_l * (1 - R)",
        "retained_wage_share_R": R,
        "effective_labour_tax_readings": {k: round(v, 6) for k, v in tau_l.items()},
        "required_tau_k_at_g_equals_one": {k: round(v, 6) for k, v in
                                           required_at_one.items()},
        "what_g_equals_one_means": "every dollar of displaced wages reappears as a dollar "
                                   "of taxable US capital income. This is the assumption "
                                   "behind the required band the paper has published, and "
                                   "it is the most favourable case for closing the "
                                   "condition.",
        "capex_dollar_decomposition_used": {
            "domestic_labour_already_inside_tau_l": [dlab_lo, dlab_mid, dlab_hi],
            "imported_no_us_tax": [imp_lo, imp_mid, imp_hi],
            "domestic_surplus_priced_by_tau_k": [s_dom_lo, s_dom_mid, s_dom_hi],
        },
        "g_range_over_the_sweep": [round(min(gs), 6), round(max(gs), 6)],
        "g_central_case": central,
        "assembled_tau_k_central": assembled,
        "assembled_tau_k_central_domestic_holder_base": assembled_crs,
        "verdict": (
            "The required rate is inversely proportional to g, so any pass-through short of "
            "one raises it. At the central case the required rate is roughly double the "
            "published band, and the assembled rate does not reach it on either base or "
            "under either rent reading. The direction of the correction is against the "
            "paper's own published required band, which was computed at the most "
            "favourable value of g, and in favour of its conclusion that the condition "
            "fails."),
    }
    (HERE / "a1_pass_through.json").write_text(json.dumps(out, indent=2) + "\n")

    import csv
    with (HERE / "a1_required_by_g.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(by_g[0]))
        w.writeheader()
        w.writerows(by_g)
    with (HERE / "a1_g_cases.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(cases[0]))
        w.writeheader()
        w.writerows(cases)

    print(f"R = {R:.6f}")
    print("required at g = 1:", {k: round(v, 4) for k, v in required_at_one.items()})
    print(f"g over the sweep: {min(gs):.3f} to {max(gs):.3f}")
    print(f"central case g = {central['g']:.3f}, required "
          f"{central['required_tau_k_easier']:.4f} to {central['required_tau_k_harder']:.4f}")
    print("assembled central:", {k: round(v, 4) for k, v in assembled.items()})


if __name__ == "__main__":
    main()
