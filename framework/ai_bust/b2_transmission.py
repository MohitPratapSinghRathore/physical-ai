"""MODULE B2. Transmission of an AI bust to the real economy. Two scenarios.

SCENARIO throughout. The wealth distribution and the historical anchors are MEASURED; the
bust sizes, the marginal propensity to consume out of wealth, and the investment fall are
assumptions, each labelled and each bounded by a verified episode.

THE TWO SCENARIOS, and why they are the right two. The project's own historical anchors are
an equity-financed bust (2000 to 2002) and a debt-financed one (2007 to 2009), and they
differ in what they do to the federal budget by a factor of nearly two: receipts fell 9.5
percent in the first and 16.0 in the second. So the split is not decorative.

  EQUITY-LED. AI-exposed equity falls; the loss lands on holders; consumption falls through
    a wealth effect; investment falls because the financing was equity. Bank credit losses
    are second-order because the debt was never there. Bounded by 2000 to 2002.
  CREDIT-LED. The same equity fall plus the debt. Leverage forces the adjustment faster,
    bank losses arrive directly, and the corporate tax base falls much further. Bounded by
    2007 to 2009.

THE MPC OUT OF STOCK WEALTH IS NOW SOURCED AND VERIFIED, replacing the stated assumption
this module previously carried. Chodorow-Reich, Nenov and Simsek (2021, American Economic
Review 111(5): 1613-57, DOI 10.1257/aer.20200208) estimate an **MPC of 3.2 cents per year**
out of stock market wealth, from a local labour market design. The abstract was read from the
AEA article page and the figure verified before use. The previous assumption was a range of
1 to 5 cents with a central of 3, so the sourced value lands almost exactly on the old
central and the module's results barely move. The bracketing low and high are retained as a
sensitivity and are labelled as NOT part of the sourced estimate. The check against the two
verified episodes is still printed.

WHY THE DISTRIBUTION MATTERS MORE THAN THE MPC. Corporate equity is extraordinarily
concentrated: at 2026Q2 the top 1 percent hold about 51 percent of it and the bottom 50
percent about 0.6 percent. A wealth shock therefore lands almost entirely on households with
the LOWEST marginal propensity to consume, which is why an equity-led bust transmits weakly
to demand and a credit-led one, which reaches balance sheets that are leveraged, does not.
"""
import io
import json
import zipfile
from pathlib import Path

import pandas as pd

HERE = Path(__file__).parent
PROC = Path(__file__).resolve().parents[2] / "data" / "processed"
LB = Path(__file__).resolve().parents[1] / "labor_backing"

# SOURCED AND VERIFIED, replacing the stated assumption this module previously carried.
# Chodorow-Reich, Gabriel, Plamen T. Nenov, and Alp Simsek. 2021. "Stock Market Wealth and
# the Real Economy: A Local Labor Market Approach." American Economic Review 111 (5):
# 1613-57. DOI 10.1257/aer.20200208. Abstract verified from the AEA article page on
# 2026-09-20: "these responses imply an MPC of 3.2 cents per year".
# The 0.032 point estimate is the CENTRAL value. The low and high are a bracketing
# sensitivity, NOT part of the sourced estimate, and are labelled as such.
MPC_WEALTH = {"bracket_low": 0.01,
              "SOURCED central, Chodorow-Reich Nenov Simsek 2021": 0.032,
              "bracket_high": 0.05}

# Okun coefficients, the same set used elsewhere in this project
# (Ball, Leigh and Loungani, "Okun's Law: Fit at 50?", in data/raw/manual/).
OKUN = {"BLL_hp1000": 0.372, "BLL_firstdiff": 0.402, "BLL_hp100": 0.421,
        "earlier_assumption": 0.50}

# AI-related investment as a share of recent GDP GROWTH. STATED ASSUMPTION, swept, because
# this project has not verified a source for it. The sweep spans the range the public debate
# uses. It enters only through the investment channel and is reported separately so a reader
# can substitute their own number.
AI_INV_SHARE_OF_GROWTH = {"low": 0.10, "central": 0.25, "high": 0.40}


def equity_by_wealth():
    z = zipfile.ZipFile(LB / "_dfa_cache.zip")
    d = pd.read_csv(io.BytesIO(z.read("dfa-networth-levels.csv")))
    last = d[d.Date == d.Date.max()]
    col = "Corporate equities and mutual fund shares"
    s = last.set_index("Category")[col] / 1e3          # millions -> bn
    tot = float(s.sum())
    return s.round(1).to_dict(), tot, {k: round(v / tot, 4) for k, v in s.items()}


def main():
    HERE.mkdir(parents=True, exist_ok=True)
    eq, eq_tot, eq_share = equity_by_wealth()
    A = pd.read_csv(LB / "historical_anchors.csv").set_index("anchor")
    tsb = json.loads((LB / "two_sided_bet.json").read_text())
    gdp = json.loads((PROC / "capacities.json").read_text())["gdp_bn"]
    ai_eq = tsb["ai_leg"]["ai_equity_central_bn"]
    ai_debt = tsb["ai_leg"]["ai_onbalancesheet_debt_bn"]

    # ---- the MPC check against the verified episodes
    checks = []
    for name, row in A.iterrows():
        dW = (row.household_equity_trough_tn - row.household_equity_peak_tn) * 1000
        checks.append({"episode": name, "household_equity_fall_bn": round(dW, 1),
                       "gdp_peak_bn": row.gdp_peak_bn,
                       "equity_fall_pct_of_gdp": row.equity_fall_pct_of_gdp,
                       "consumption_fall_implied_at_mpc_0.03_bn": round(0.03 * dW, 1),
                       "as_pct_of_gdp": round(100 * 0.03 * dW / row.gdp_peak_bn, 2)})

    rows = []
    for scen, eq_fall_pct, debt_impaired in [
            ("equity-led, bounded by 2000 to 2002", A.loc["2000_to_2002_equity_financed",
                                                          "nfc_equity_fall_pct"] / 100, 0.0),
            ("credit-led, bounded by 2007 to 2009", A.loc["2007_to_2009_debt_financed",
                                                          "nfc_equity_fall_pct"] / 100, 0.35)]:
        dEquity = ai_eq * eq_fall_pct                      # negative
        # the loss lands in proportion to holdings
        by_holder = {k: round(dEquity * v, 1) for k, v in eq_share.items()}
        for mk, mpc in MPC_WEALTH.items():
            dC = mpc * dEquity                             # negative
            for ik, ishare in AI_INV_SHARE_OF_GROWTH.items():
                # investment channel: AI investment stops growing and partly reverses.
                # sized as the share of recent GDP growth it accounted for, times GDP growth
                dI = -ishare * 0.025 * gdp                 # 2.5 pct nominal growth, stated
                dGDP = dC + dI
                dGDP_pct = 100 * dGDP / gdp
                for ok, okun in OKUN.items():
                    dU = -okun * dGDP_pct                  # unemployment rises
                    rows.append({
                        "scenario": scen, "mpc": mk, "mpc_value": mpc,
                        "ai_inv_share_of_growth": ik,
                        "okun": ok, "okun_value": okun,
                        "ai_equity_fall_bn": round(dEquity, 1),
                        "consumption_fall_bn": round(dC, 1),
                        "investment_fall_bn": round(dI, 1),
                        "gdp_fall_bn": round(dGDP, 1),
                        "gdp_fall_pct": round(dGDP_pct, 3),
                        "unemployment_rise_pp": round(dU, 3),
                        "ai_debt_impaired_bn": round(ai_debt * debt_impaired, 1),
                    })
    R = pd.DataFrame(rows)
    R.to_csv(HERE / "b2_transmission.csv", index=False)

    summ = {
        "status": "SCENARIO. Wealth distribution and anchors MEASURED; bust size, MPC and "
                  "investment share are stated assumptions",
        "equity_by_wealth_percentile_bn": eq,
        "equity_share_by_wealth_percentile": eq_share,
        "top1_share_of_corporate_equity": round(eq_share["TopPt1"]
                                                + eq_share["RemainingTop1"], 4),
        "bottom50_share": eq_share["Bottom50"],
        "mpc_wealth_SOURCED": MPC_WEALTH,
        "mpc_source": "Chodorow-Reich, Nenov and Simsek 2021, AER 111(5): 1613-57, "
                      "DOI 10.1257/aer.20200208. MPC of 3.2 cents per year, verified.",
        "mpc_check_against_verified_episodes": checks,
        "okun_range": OKUN,
        "ai_inv_share_of_growth_STATED": AI_INV_SHARE_OF_GROWTH,
        "gdp_fall_pct_range": [round(float(R.gdp_fall_pct.min()), 3),
                               round(float(R.gdp_fall_pct.max()), 3)],
        "unemployment_rise_pp_range": [round(float(R.unemployment_rise_pp.min()), 3),
                                       round(float(R.unemployment_rise_pp.max()), 3)],
        "the_distribution_point": "Corporate equity is extraordinarily concentrated: the "
                                  "top 1 percent hold "
                                  f"{100*(eq_share['TopPt1']+eq_share['RemainingTop1']):.1f} "
                                  f"percent and the bottom half "
                                  f"{100*eq_share['Bottom50']:.1f} percent. An equity shock "
                                  "therefore lands on the households with the LOWEST "
                                  "marginal propensity to consume, which is why the "
                                  "equity-led path transmits weakly to demand.",
    }
    (HERE / "b2_transmission.json").write_text(json.dumps(summ, indent=2, default=str))

    pd.set_option("display.width", 220)
    print("CORPORATE EQUITY BY WEALTH PERCENTILE, 2026Q2, MEASURED")
    for k in ["TopPt1", "RemainingTop1", "Next9", "Next40", "Bottom50"]:
        print(f"  {k:16s} {eq[k]:>12,.1f} bn   {100*eq_share[k]:>6.2f} pct")
    print(f"  top 1 pct hold {100*summ['top1_share_of_corporate_equity']:.1f} pct; "
          f"bottom 50 pct hold {100*eq_share['Bottom50']:.2f} pct")
    print("\nMPC CHECK against the verified episodes")
    print(pd.DataFrame(checks).to_string(index=False))
    print("\nTRANSMISSION, central MPC and central investment share")
    c = R[(R.mpc.str.startswith("SOURCED")) & (R.ai_inv_share_of_growth == "central")]
    print(c[["scenario", "okun", "ai_equity_fall_bn", "consumption_fall_bn",
             "investment_fall_bn", "gdp_fall_pct", "unemployment_rise_pp"]]
          .to_string(index=False))
    print(f"\nfull range across all assumptions: GDP {summ['gdp_fall_pct_range']} pct, "
          f"unemployment +{summ['unemployment_rise_pp_range']} pp")


if __name__ == "__main__":
    main()
