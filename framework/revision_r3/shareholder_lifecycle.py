"""REFEREE ITEM B2. Decompose the shareholder layer by holder type and tax treatment,
instead of applying one taxable share and one deferral factor to everything.

THE REFEREE POINTS, each addressed below.
  1. Being outside the current shareholder capital-gains base is not the same as generating
     no federal receipts, because retirement distributions are taxable.
  2. Separate taxable accounts, traditional arrangements, Roth arrangements, nonprofits and
     foreign holders, and state which taxes count and when.
  3. Applying one capital-gains deferral factor to the whole layer needs dividends treated
     explicitly, since dividends are taxed currently and carry no deferral benefit.

WHAT THE DECOMPOSITION FINDS. Three corrections, and all three raise the layer.

  A. TRADITIONAL RETIREMENT IS THE SAME STRUCTURE AS EXPENSING. A deductible contribution
     grown at r and taxed on withdrawal at the same rate leaves the return untaxed: the
     government is a pro-rata co-investor, so the MARGINAL effective rate on the inside
     build-up is zero. That is the standard result, and the treatment of retirement assets
     as outside the base is correct ON THE MARGIN. It is wrong for annual revenue, because
     in a mature system distributions are taxed at ordinary rates every year. This is the
     entity-level expensing problem of the annual-counterpart section appearing again at the
     shareholder level, with the same resolution: zero marginal rate, positive annual
     receipts.

  B. FOREIGN WITHHOLDING IS ALREADY IDENTIFIED BUT ONLY ONE AT A TIME. The base assembly
     sets the shareholder layer to theta_taxable x rate x deferral with theta_taxable = 0.27,
     which assigns no shareholder tax to the 0.42 of US equity held abroad. The paper does
     not hide this: it states that the base construction treats foreign holders as bearing
     no owner-level tax although dividends to them bear withholding, and it sizes the effect
     as a one-at-a-time sensitivity. Nothing here is a charge of omission. What is new is
     that the correction is folded into the layer rather than reported beside it, and that it
     is taken TOGETHER with C below, which is the joint treatment the referee asks for.
     Portfolio capital gains of foreign holders are not US-taxed, so the correction is
     confined to the dividend component.

  C. DEFERRAL WAS APPLIED TO DIVIDENDS. Dividends are taxed on receipt. Splitting the
     taxable-account layer into a currently taxed dividend part and a deferred gains part
     raises it.

STATUS. The holder shares and the Roth share are SOURCED. The dividend payout share, the
effective foreign withholding rate, the ordinary rate on retirement distributions and the
Roth share of defined contribution assets are SWEPT, because no aggregate figure for them
was located, and every output is reported as a range over that box.
"""
import itertools
import json
import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tau_k"))
import components as K
import assemble as A

OUT = pathlib.Path(__file__).resolve().parents[2] / "data" / "release" / "revision_r3"

# ---- SOURCED. Rosenthal and Mucciolo 2024, Table 5, total US equity outstanding, 2022.
HOLDERS = {"foreign": 0.42, "ira": 0.11, "defined_benefit": 0.07,
           "defined_contribution": 0.07, "nonprofits": 0.04,
           "life_insurance_separate": 0.02, "government_and_529": 0.01,
           "taxable_accounts": 0.27}
ROTH_SHARE_OF_IRA = 0.10          # ICI 2024: Roth IRAs 1.4 of 13.6 trillion at end-2023
GAINS_STEP_UP = 0.469             # CBO 2014, accrued gains never taxed at death
WITHHOLDING_STATUTORY = 0.30      # 26 USC 871(a) and 881(a)
WITHHOLDING_TREATY_STD = 0.15     # standard portfolio rate in the major US treaties

# ---- SWEPT, with the reason each could not be sourced recorded in the paper.
BOX = {
    "payout": [0.35, 0.55],             # dividend share of after-tax corporate earnings
    "withholding_eff": [0.05, 0.20],    # effective collected rate, treaty standard 0.15
    "ordinary_rate_retirement": [0.12, 0.24],
    "roth_share_of_dc": [0.05, 0.15],
    "gains_rate": list(K.U["shareholder_rate"]["range"]),
}
CEN = {k: float(np.mean(v)) for k, v in BOX.items()}
CEN["withholding_eff"] = WITHHOLDING_TREATY_STD
NAMES = list(BOX)


def layers(p):
    """The shareholder layer on the marginal object and on the annual object."""
    h = HOLDERS
    trad = (h["ira"] * (1 - ROTH_SHARE_OF_IRA)
            + h["defined_benefit"]
            + h["defined_contribution"] * (1 - p["roth_share_of_dc"]))
    roth = h["ira"] * ROTH_SHARE_OF_IRA + h["defined_contribution"] * p["roth_share_of_dc"]
    exempt = h["nonprofits"] + h["life_insurance_separate"] + h["government_and_529"] + roth

    # taxable accounts: dividends taxed on receipt, gains deferred and partly stepped up
    gains_eff = p["gains_rate"] * (1 - GAINS_STEP_UP)
    taxable = h["taxable_accounts"] * (p["payout"] * p["gains_rate"]
                                       + (1 - p["payout"]) * gains_eff)
    # foreign: US withholding on the dividend component only
    foreign = h["foreign"] * p["payout"] * p["withholding_eff"]
    # traditional retirement: zero on the margin, ordinary rates annually
    trad_annual = trad * p["ordinary_rate_retirement"]

    return {"marginal": taxable + foreign,
            "annual": taxable + foreign + trad_annual,
            "trad_share": trad, "roth_share": roth, "exempt_share": exempt,
            "taxable_part": taxable, "foreign_part": foreign,
            "trad_annual_part": trad_annual}


def published_layer(p):
    """The layer as the paper currently assembles it, for comparison."""
    return A.tau_sh(K.THETA_TAXABLE["central"], p["gains_rate"],
                    K.DEFERRAL_FACTOR["central"])


def corners(fn):
    vals = [fn(dict(zip(NAMES, c))) for c in itertools.product(*[BOX[n] for n in NAMES])]
    return float(min(vals)), float(max(vals))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    c = layers(CEN)
    res = {
        "sourced": {"holder_shares_rosenthal_mucciolo_2024_table5": HOLDERS,
                    "roth_share_of_ira_ici_2024": ROTH_SHARE_OF_IRA,
                    "gains_never_taxed_at_death_cbo_2014": GAINS_STEP_UP,
                    "withholding_statutory": WITHHOLDING_STATUTORY,
                    "withholding_treaty_standard": WITHHOLDING_TREATY_STD},
        "swept": BOX,
        "central_parameters": {k: round(v, 4) for k, v in CEN.items()},
        "holder_groups": {"traditional_retirement": round(c["trad_share"], 4),
                          "roth": round(c["roth_share"], 4),
                          "never_taxed": round(c["exempt_share"], 4),
                          "taxable_accounts": HOLDERS["taxable_accounts"],
                          "foreign": HOLDERS["foreign"]},
        "layer": {
            "published_assembly": round(published_layer(CEN), 4),
            "marginal_decomposed": round(c["marginal"], 4),
            "annual_decomposed": round(c["annual"], 4),
            "marginal_range": [round(x, 4) for x in corners(lambda p: layers(p)["marginal"])],
            "annual_range": [round(x, 4) for x in corners(lambda p: layers(p)["annual"])],
            "of_which_taxable_accounts": round(c["taxable_part"], 4),
            "of_which_foreign_withholding": round(c["foreign_part"], 4),
            "of_which_traditional_retirement_annual": round(c["trad_annual_part"], 4)},
    }
    res["finding"] = (
        "The base shareholder layer is {:.4f}. Decomposed by holder and treatment it is "
        "{:.4f} on the marginal object, taking foreign withholding and the dividend split "
        "together rather than one at a time, and {:.4f} on the annual object, because "
        "traditional retirement distributions are taxed at ordinary rates. The headline "
        "ownership figure conflates three treatments: {:.3f} of US equity sits in traditional "
        "retirement arrangements, untaxed on the margin and taxed annually on distribution; "
        "{:.2f} is held abroad and bears withholding on dividends only; and only {:.3f} is "
        "never reached by any federal tax at all."
    ).format(published_layer(CEN), c["marginal"], c["annual"],
             c["trad_share"], HOLDERS["foreign"], c["exempt_share"])
    (OUT / "shareholder_lifecycle.json").write_text(json.dumps(res, indent=2))
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
