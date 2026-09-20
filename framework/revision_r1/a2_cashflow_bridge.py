"""A2. From an effective marginal rate to annual revenue.

THE PROBLEM. Under full expensing the deduction comes first and the income later. The
effective marginal rate we assemble is a present-value statement about the whole life of one
investment: it is the wedge between the pre-tax and post-tax return on a marginal project.
An annual revenue replacement coefficient is a different object. The two coincide only in a
steady state.

THE CASH FLOW, one project of size 1 placed in service at t = 0, expensed in full.

    t = 0 :  tax  = -tau_c                                (the deduction)
    t >= 1:  tax  = +tau_c * y_t                          (tax on the gross return)

with y_t the gross return in year t. Writing the discount rate r and the economic
depreciation rate delta, the present value of the project's tax is

    PV = -tau_c + tau_c * sum_t y_t / (1 + r)^t

which is zero for a project earning exactly the normal return, and positive only on rents.
That is the same statement as the expensing result the paper takes from the literature.

THE STEADY STATE WE RELY ON. With a constant flow of investment I per year and a constant
capital stock, deductions on new investment and tax on the income of existing capital are
both flows of the same size each year, so the annual revenue equals the present-value
statement applied to one year's investment. The paper's use of the rate as an annual
replacement coefficient is therefore a steady-state statement.

THE TRANSITION. While investment is growing at rate gamma, this year's deductions are
larger than the tax on the income of a capital stock built when investment was smaller. Net
revenue from the sector is lower than the steady-state figure, and can be negative. This
module computes that path for a geometric investment series using the paper's own
parameters, so that the size and the sign of the transition effect are visible.

STATUS. SCENARIO. The growth path is illustrative; the tax parameters are the ones used
elsewhere in the paper.
"""
import csv
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
HERE = pathlib.Path(__file__).parent


def load(rel):
    return json.loads((ROOT / rel).read_text())


def main():
    comp = load("framework/tau_k/components.json")
    tau_c_fed = float(comp["verified"]["federal_cit"])
    tk = load("framework/tau_k/tau_k_assembled.json")
    sigma = float(comp["verified"]["rent_readings_NEVER_AVERAGED"]["Barkai"])
    assembled = {r["rent_reading"]: r["tau_k_central"]
                 for r in tk["assembled_CENTRAL_at_sourced_centrals"]}

    r_disc = 0.03          # the discount rate used elsewhere in this project
    delta = 0.15           # economic depreciation for equipment and software, illustrative
    horizon = 25

    rows = []
    for gamma in (0.0, 0.10, 0.20, 0.30, 0.40):
        # geometric investment series, normalised so that year 0 investment is 1
        inv = [(1 + gamma) ** t for t in range(horizon + 1)]
        # capital stock and its gross return; the return is the normal return plus rents
        stock, net_tax = 0.0, []
        for t in range(horizon + 1):
            stock = stock * (1 - delta) + inv[t]
            # gross return on the stock: the normal return (r + delta) grossed up so that
            # a share sigma of the total return is economic rent
            gross_return = (r_disc + delta) * stock / max(1 - sigma, 1e-9)
            # tax base: expensing deducts this year's investment, taxes this year's return
            base = gross_return - inv[t]
            net_tax.append(tau_c_fed * base)
        rows.append({
            "investment_growth_rate": gamma,
            "net_tax_year_1_per_unit_of_investment": round(net_tax[1] / inv[1], 6),
            "net_tax_year_5": round(net_tax[5] / inv[5], 6),
            "net_tax_year_10": round(net_tax[10] / inv[10], 6),
            "net_tax_year_25": round(net_tax[25] / inv[25], 6),
            "negative_while_growing": bool(net_tax[5] < 0),
            "years_until_net_tax_turns_positive":
                next((t for t, v in enumerate(net_tax) if t > 0 and v > 0), None),
        })

    out = {
        "status": "SCENARIO. The growth path is illustrative; the tax parameters are those "
                  "used elsewhere in the paper.",
        "the_two_objects": {
            "effective_marginal_rate": "a present-value wedge over the life of one marginal "
                                       "investment, which is what the paper assembles",
            "annual_revenue_coefficient": "the tax collected from the sector in a year, "
                                          "which is what a revenue replacement question "
                                          "asks about",
        },
        "they_coincide": "only in a steady state, with investment flat and the capital stock "
                         "constant, where each year's deductions and each year's tax on "
                         "existing income are flows of the same size",
        "assembled_rate_is_a_steady_state_statement": True,
        "transition": "while investment grows, current deductions exceed the tax on income "
                      "from a smaller past stock, so net revenue from the sector is below "
                      "the steady-state figure and can be negative",
        "parameters": {"federal_entity_rate": tau_c_fed, "rent_share": sigma,
                       "discount_rate": r_disc, "depreciation_rate": delta,
                       "horizon_years": horizon},
        "assembled_tau_k_central": assembled,
        "which_statements_are_steady_state": [
            "the required rate tau_l (1 - R) / g and every comparison against it",
            "the assembled effective marginal rate and its component decomposition",
            "every statement of the form the rate falls short of what replacement needs",
        ],
        "which_statements_are_not_steady_state": [
            "any claim about revenue collected in a particular year during an investment "
            "boom, which this paper does not make and should not be read as making",
        ],
        "verdict": "The paper's comparison is a steady-state comparison and must say so. "
                   "During a period of rapidly growing AI investment the revenue actually "
                   "collected from the sector is lower than the assembled rate implies, and "
                   "on this illustrative path it is negative in the early years, so the "
                   "near-term position is worse than the steady-state statement, not better.",
    }
    (HERE / "a2_cashflow_bridge.json").write_text(json.dumps(out, indent=2) + "\n")
    with (HERE / "a2_transition_path.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    for r in rows:
        print(r)


if __name__ == "__main__":
    main()
