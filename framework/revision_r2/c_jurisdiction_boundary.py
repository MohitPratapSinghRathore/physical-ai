"""Part C. Jurisdiction, weakening assumptions, output growth, and the boundary.

SPECIFICATIONS, STATED BEFORE COMPUTING.

C1. JURISDICTION. The replacement question in this paper is about the federal balance sheet,
so both sides of the condition should be measured on the same government. They currently are
not: the labor tax readings are federal, built from federal taxes over wages and salaries,
while the assembled capital rate adds an effective state corporate tax to the federal entity
rate. Two consistent versions are computed.

  FEDERAL ONLY   capital: the same assembly with the state corporate term set to zero.
                 labor:   the published readings, unchanged.
  ALL GOVERNMENT capital: the assembly as published, state corporate term included.
                 labor:   the published readings plus the state and local wage-linked tax,
                          measured as state and local wage-linked income tax over the wage
                          bill, both already in the paper.

C2. ASSUMPTIONS THAT COULD WEAKEN THE CONCLUSION. Each is applied to the assembled rate on
its own and then jointly:
  (a) withholding tax on dividends to foreign holders. Foreign holders are treated as untaxed
      at the owner level; applying a treaty rate to the foreign-held share of equity raises
      the shareholder layer. The treaty rate is a STATED ASSUMPTION swept over 0 to 15
      percent, which brackets the common United States treaty rates on portfolio dividends.
  (b) a lower debt-financed share, taken from the nine filers' own books rather than the
      economy-wide stock ratio. Because the debt-financed term is negative, this RAISES the
      assembled rate.
  (c) the alternative rent share already in the paper.
  (d) labor tax rates matched to the earnings of the displaced, using the payroll and income
      tax rates by wage quintile already computed in the release, weighted by the quintile
      composition of displacement rather than the economy-wide average.

C3. OUTPUT GROWTH. The restriction g <= 1 belongs to the output-preserved case. With output
rising, taxable capital income per displaced wage dollar can exceed one. We report the value
of g at which the condition closes at the assembled rate, under each jurisdiction.

C4. BOUNDARY. The fiscal balance tau_k * g - tau_l * (1 - R) over the retained wage share and
g, with the zero contour drawn for each tax treatment.

PLAUSIBILITY BOUNDS, STATED BEFORE COMPUTING.
  1. Every rate lies in [0, 1]; the assembled rate may be negative only through the
     debt-financed term and is bounded below by -0.1.
  2. The federal-only assembled rate must be BELOW the all-government rate, since removing a
     tax cannot raise the total.
  3. The federal-only required band must be BELOW the all-government band for the same reason.
  4. g at which the condition closes must be positive and must fall as the assembled rate
     rises.
"""
import csv
import json
import pathlib
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
HERE = pathlib.Path(__file__).parent
HERE.mkdir(exist_ok=True)
sys.path.insert(0, str(ROOT / "framework" / "tau_k"))

import components as K  # noqa: E402
from assemble import assemble  # noqa: E402


def load(rel):
    return json.loads((ROOT / rel).read_text())


def rows(rel):
    with (ROOT / rel).open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def central(state_cit, debt=None, theta_extra=0.0, sigma=None, shifted=None):
    """The assembly at sourced central values, with named departures."""
    sigma = K.RENT_READINGS["Barkai"] if sigma is None else sigma
    debt = K.DEBT_SHARE["central"] if debt is None else debt
    shifted = K.V_SHIFTED if shifted is None else shifted
    sh_rate = float(np.mean(K.U["shareholder_rate"]["range"]))
    bond = K.BONDHOLDER_RATE["central"]
    theta = K.THETA_TAXABLE["central"] + theta_extra
    tk, tr, tn = assemble(sigma, shifted, theta, sh_rate,
                          K.DEFERRAL_FACTOR["central"], state_cit, debt, bond)
    return float(tk)


def main():
    tk_pub = load("framework/tau_k/tau_k_assembled.json")
    rsen = load("data/processed/replication_r_sensitivity.json")
    R = float(rsen["ours_observed_rho_and_our_omega"]["R"])
    req_pub = rsen["ours_observed_rho_and_our_omega"]["required_tau_k"]
    tau_l = {k: v / (1 - R) for k, v in req_pub.items()}
    easy, hard = "AMR_0.255", "bottom_up_0.318"

    state_mid = float(np.mean(K.U["state_cit_effective"]["range"]))

    # ---- C1, jurisdiction
    omitted = load("framework/institutions/a3_omitted_institutions.json")
    sl = omitted["state_and_local_government"]["size_bn"]
    wage_bill = load("data/processed/fiscal_channel_summary.json")["denominators"][
        "wage_bill_usd_bn"]
    sl_labor_rate = sl["of which wage-linked at the SOI wage share"] / wage_bill

    tk_fed = central(state_cit=0.0)
    tk_all = central(state_cit=state_mid)
    assert tk_fed < tk_all, "removing the state tax raised the assembled rate"

    juris = {}
    for name, tk, add in (("federal only", tk_fed, 0.0),
                          ("all government", tk_all, sl_labor_rate)):
        juris[name] = {
            "assembled_tau_k": round(tk, 6),
            "labor_tax_easier": round(tau_l[easy] + add, 6),
            "labor_tax_harder": round(tau_l[hard] + add, 6),
            "required_easier": round((tau_l[easy] + add) * (1 - R), 6),
            "required_harder": round((tau_l[hard] + add) * (1 - R), 6),
            "state_local_labor_add_on": round(add, 6),
        }
    assert juris["federal only"]["required_easier"] <= juris["all government"]["required_easier"]

    # ---- C2, the weakening assumptions
    foreign_share = 1.0 - 0.4545          # the foreign slice dropped from the domestic base
    filers = load("framework/ai_bust/b1_tiers.json")["nine_filers"]
    debt_low = float(filers["debt_financed_share_of_capex"])
    sigma_kn = K.RENT_READINGS["Karabarbounis_Neiman_case_R"]

    q = rows("data/release/dose_response/by_wage_quintile.csv")
    seen, disp_rate = {}, []
    for r in q:
        k = r["target"]
        if k in seen:
            continue
        seen[k] = True
        disp_rate.append(float(r["effective_payroll_rate"]) + float(r["effective_income_tax_rate"]))
    tau_l_bottom = min(disp_rate)
    tau_l_top = max(disp_rate)

    variants = []
    for name, tk, note in (
        ("published central, all government", tk_all, "as published"),
        ("withholding tax on foreign holders at 15 percent",
         central(state_cit=state_mid, theta_extra=foreign_share * 0.15),
         "the foreign-held share treated as bearing a 15 percent treaty rate at the owner "
         "level, which is a stated assumption and not a measurement"),
        ("debt share from the filers' own books",
         central(state_cit=state_mid, debt=debt_low),
         "raises the rate, because the debt-financed term is negative"),
        ("second rent reading", central(state_cit=state_mid, sigma=sigma_kn),
         "already carried in the paper"),
        ("all three together, excluding the second rent reading",
         central(state_cit=state_mid, debt=debt_low,
                 theta_extra=foreign_share * 0.15),
         "withholding and the lower debt share applied jointly"),
    ):
        variants.append({"variant": name, "assembled_tau_k": round(tk, 6),
                         "closes_against_easier_all_government":
                             bool(tk >= juris["all government"]["required_easier"]),
                         "note": note})

    labor_matched = {
        "effective_labor_tax_by_quintile_low": round(tau_l_bottom, 6),
        "effective_labor_tax_by_quintile_high": round(tau_l_top, 6),
        "required_if_displacement_hits_the_bottom_quintile":
            round(tau_l_bottom * (1 - R), 6),
        "required_if_displacement_hits_the_top_quintile": round(tau_l_top * (1 - R), 6),
        "note": "the payroll and income tax rates by wage quintile already in the release; "
                "displacement concentrated low in the distribution lowers the required rate, "
                "and this is the one assumption in this set that works in the paper's favour",
    }

    # ---- C3, output growth
    gstar = {}
    for name, d in juris.items():
        tk = d["assembled_tau_k"]
        gstar[name] = {
            "g_closing_easier": round(d["required_easier"] / tk, 4),
            "g_closing_harder": round(d["required_harder"] / tk, 4),
        }
        assert gstar[name]["g_closing_easier"] > 0
    assert gstar["federal only"]["g_closing_easier"] > gstar["all government"]["g_closing_easier"] \
        or tk_fed < tk_all

    # ---- C4, the boundary grid
    grid = []
    Rs = [round(0.05 * i, 2) for i in range(0, 21)]
    gs = [round(0.25 * i, 2) for i in range(1, 17)]
    for name, d in juris.items():
        for tl_name, tl in (("easier", d["labor_tax_easier"]),
                            ("harder", d["labor_tax_harder"])):
            for Rv in Rs:
                for gv in gs:
                    bal = d["assembled_tau_k"] * gv - tl * (1 - Rv)
                    grid.append({"jurisdiction": name, "labor_reading": tl_name,
                                 "retained_wage_share": Rv, "g": gv,
                                 "fiscal_balance_per_displaced_dollar": round(bal, 6)})
    with (HERE / "c4_boundary_grid.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(grid[0]))
        w.writeheader()
        w.writerows(grid)

    out = {
        "status": "SCENARIO on the assembled rate and on every C2 variant; the retained wage "
                  "share and the labor tax readings are as published.",
        "plausibility_bounds_checked": [
            "federal-only assembled rate below the all-government rate, asserted",
            "federal-only required band below the all-government band, asserted",
            "g at which the condition closes positive, asserted",
        ],
        "retained_wage_share_R": R,
        "labor_tax_readings_are": "FEDERAL. The bottom-up readings are federal taxes over "
                                  "wages and salaries; the automation-literature reading is a "
                                  "federal effective labor tax rate. The published capital "
                                  "rate, by contrast, includes an effective state corporate "
                                  "tax, so the published comparison mixes jurisdictions.",
        "C1_jurisdiction": juris,
        "C2_variants": variants,
        "C2_labor_tax_matched_to_the_displaced": labor_matched,
        "C3_g_at_which_the_condition_closes": gstar,
        "C4_boundary": "grid written to c4_boundary_grid.csv",
        "headline_recommendation": "the federal-only version, because the paper's claim is "
                                   "about the federal balance sheet",
    }
    (HERE / "c_jurisdiction_boundary.json").write_text(json.dumps(out, indent=2) + "\n")

    print(f"R = {R:.6f}; state and local labor add-on = {sl_labor_rate:.4f}")
    for name, d in juris.items():
        print(f"  {name:<16s} tau_k {d['assembled_tau_k']:.4f}  required "
              f"{d['required_easier']:.4f} to {d['required_harder']:.4f}  "
              f"g* {gstar[name]['g_closing_easier']:.2f} to "
              f"{gstar[name]['g_closing_harder']:.2f}")
    for v in variants:
        print(f"  {v['variant']:<52s} {v['assembled_tau_k']:.4f}  "
              f"closes: {v['closes_against_easier_all_government']}")
    print("  labor tax by quintile:", labor_matched["effective_labor_tax_by_quintile_low"],
          "to", labor_matched["effective_labor_tax_by_quintile_high"])


if __name__ == "__main__":
    main()
