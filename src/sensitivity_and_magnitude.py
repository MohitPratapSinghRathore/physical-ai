"""A5 gate/weighting sensitivity and A7 magnitude reframing.

A5. The c = 1 exposure share is recomputed across embodiment gates at the 25th, 40th, 50th
and 60th percentile of P, with and without P-weighting. The word "ceiling" is retired: what
is reported is a range conditional on stated assumptions.

A7. Wage bill at risk at each c is expressed as a share of three denominators, with no
adjectives:
  (i)   aggregate household debt service
  (ii)  labor-linked federal receipts, SOI-corrected central estimate (Step 0, A8)
  (iii) total wages and salaries (NIPA WASCUR)
"""
import json, pathlib
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).parents[1]
OUT = ROOT / "data" / "processed"


def main():
    G = pd.read_csv(OUT / "paei_c.csv")
    G = G[G["employment"].notna() & (G["employment"] > 0)].copy()
    ver = json.loads((OUT / "paei_c_summary.json").read_text())["paei_c_version"]

    base = G[G["c"] == 0.0]
    gates = {q: float(np.percentile(base["embodiment_P"], q)) for q in [25, 40, 50, 60]}

    # ---------------- A5 ----------------
    rows = []
    for c in [0.2, 0.5, 0.8, 1.0]:
        g = G[G["c"] == c]
        for q, gate in gates.items():
            sel = g[g["embodiment_P"] >= gate]
            ex = sel["exposed_threshold_rank"] == 1
            emp_share = 100 * sel.loc[ex, "employment"].sum() / g["employment"].sum()
            pw_num = (sel.loc[ex, "employment"] * sel.loc[ex, "embodiment_P"]).sum()
            pw_den = (g["employment"] * g["embodiment_P"]).sum()
            wb = (sel.loc[ex, "wage_bill"] * sel.loc[ex, "embodiment_P"]).sum() / 1e9
            wb_unw = sel.loc[ex, "wage_bill"].sum() / 1e9
            rows.append({"c": c, "gate_pctile": q, "gate_P": gate,
                         "share_employment_unweighted_pct": emp_share,
                         "share_embodied_work_Pweighted_pct": 100 * pw_num / pw_den,
                         "wagebill_at_risk_Pweighted_usd_bn": wb,
                         "wagebill_at_risk_unweighted_usd_bn": wb_unw})
    A5 = pd.DataFrame(rows)
    A5.round(3).to_csv(OUT / "a5_gate_sensitivity.csv", index=False)

    c1 = A5[A5["c"] == 1.0]
    rng = {
        "paei_c_version": ver,
        "c1_share_embodied_work_Pweighted_pct": [float(c1["share_embodied_work_Pweighted_pct"].min()),
                                                 float(c1["share_embodied_work_Pweighted_pct"].max())],
        "c1_wagebill_Pweighted_usd_bn": [float(c1["wagebill_at_risk_Pweighted_usd_bn"].min()),
                                         float(c1["wagebill_at_risk_Pweighted_usd_bn"].max())],
        "c1_wagebill_unweighted_usd_bn": [float(c1["wagebill_at_risk_unweighted_usd_bn"].min()),
                                          float(c1["wagebill_at_risk_unweighted_usd_bn"].max())],
    }

    # ---------------- A7 ----------------
    F = pd.read_csv(OUT / "paei_c_frontier.csv")
    w = json.loads((OUT / "legW_us_derived.json").read_text())
    lt = json.loads((OUT / "labor_tax_share.json").read_text())

    # aggregate household debt service: TDSP (percent of DPI) x DPI
    hh_debt_service = w["hh_debt_service_pct_dpi"] / 100.0 * json.loads(
        (OUT / "us_series_meta.json").read_text())["DPI"]["value"]
    labor_receipts = lt["labor_linked_central_usd_bn"]
    wages = w["wage_bill_usd_bn"]

    A7 = F[["c", "wagebill_at_risk_usd_bn"]].copy()
    A7["pct_of_household_debt_service"] = 100 * A7["wagebill_at_risk_usd_bn"] / hh_debt_service
    A7["pct_of_labor_linked_federal_receipts"] = 100 * A7["wagebill_at_risk_usd_bn"] / labor_receipts
    A7["pct_of_total_wages_and_salaries"] = 100 * A7["wagebill_at_risk_usd_bn"] / wages
    A7.round(3).to_csv(OUT / "a7_magnitude.csv", index=False)

    denoms = {"household_debt_service_usd_bn": hh_debt_service,
              "labor_linked_federal_receipts_central_usd_bn": labor_receipts,
              "total_wages_and_salaries_nipa_usd_bn": wages}

    (OUT / "a5_a7_summary.json").write_text(json.dumps(
        {"a5_range_at_c1": rng, "a5_gates": gates, "a7_denominators": denoms}, indent=2))

    pd.set_option("display.width", 200)
    print(f"PAEI_C_VERSION = {ver}")
    print("\n=== A5: gate and weighting sensitivity ===")
    print(A5.round(2).to_string(index=False))
    print("\n  at c = 1, share of embodied work exposed ranges "
          f"{rng['c1_share_embodied_work_Pweighted_pct'][0]:.1f} to "
          f"{rng['c1_share_embodied_work_Pweighted_pct'][1]:.1f} percent across gates")
    print(f"  at c = 1, wage bill at risk ranges "
          f"{rng['c1_wagebill_Pweighted_usd_bn'][0]:,.0f} to "
          f"{rng['c1_wagebill_Pweighted_usd_bn'][1]:,.0f} USD bn (P-weighted), and "
          f"{rng['c1_wagebill_unweighted_usd_bn'][0]:,.0f} to "
          f"{rng['c1_wagebill_unweighted_usd_bn'][1]:,.0f} USD bn unweighted")

    print("\n=== A7: magnitude against three denominators ===")
    for k, v in denoms.items():
        print(f"  {k:48s} {v:,.1f}")
    print()
    print(A7[A7["c"].isin([0.0, 0.2, 0.5, 0.8, 1.0])].round(2).to_string(index=False))


if __name__ == "__main__":
    main()
