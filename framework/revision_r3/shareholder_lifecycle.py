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

     THE FLOW DERIVATION, which a referee rightly asked for, because a holder share times a
     distribution rate does not on its own establish annual receipts per dollar of current
     capital income. Let the accounts hold stock A earning r*A, take contributions C and pay
     withdrawals W in the year. Deductible contributions cost revenue tau_ord*C; taxable
     withdrawals raise tau_ord*W. Net annual receipts attributable to the accounts are
     therefore

         tau_ord * (W - C).

     If the accounts are stationary in aggregate, so that the stock neither grows nor
     shrinks, then W = C + r*A and net receipts are exactly tau_ord * r*A, which is
     tau_ord per dollar of current capital income inside them. THAT is the condition under
     which share times rate is the right calculation, and it is the condition we are
     assuming.

     IT DOES NOT HOLD IN THE US, and the direction runs against this paper. US retirement
     balances have been accumulating, so C is large relative to W and W - C < r*A, which
     makes tau_ord an UPPER BOUND on the annual receipts per dollar rather than the value.
     Bounding the gap needs aggregate contribution and withdrawal flows we have not
     assembled. What we can say is that the paper's conclusion does not turn on it: setting
     the retirement term to zero, which is the extreme case of a fully accumulating system
     that collects nothing, still leaves the annual rate clearing the harder requirement on
     both jurisdictional bases. The term changes the number and not the answer.

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

STATUS. SOURCED: the holder shares, the Roth share of individual retirement accounts, the
step-up share, the dividend payout share (NIPA) and the effective withholding rate on
dividends paid abroad (IRS SOI, with both endpoints of its range published). STILL SWEPT:
the ordinary rate applying to retirement distributions and the Roth share of defined
contribution assets, because no aggregate figure for either was located. Every output is
reported as a range over the box.

Sourcing the first two moved the decomposed layer by 0.003 and narrowed every range. No
conclusion in the paper turns on them, which is the useful thing to be able to say.
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

# ---- NOW SOURCED. Two parameters that were swept in the first version.
#
# PAYOUT. NIPA net corporate dividend payments over corporate profits after tax, from the
# FRED series DIVIDEND and CPATAX. Summed over the window rather than averaging ratios:
#   2015-2024 0.6815   2020-2024 0.7083   2010-2024 0.6419
# The central value is the ten-year figure and the range spans the three windows. Note this
# is well above the 0.35 to 0.55 first swept, which raises the taxable-account layer because
# dividends are taxed on receipt with no deferral benefit.
PAYOUT_CENTRAL, PAYOUT_RANGE = 0.6815, [0.6419, 0.7083]
#
# WITHHOLDING. IRS SOI, Foreign Recipients of US Income under Chapter 3, Form 1042-S, CY
# 2019. Published figures: total US-source income to foreign persons 1,125.7 billion dollars
# of which dividends 245.2 billion; total tax withheld 21.1 billion; 89.8 percent of all
# income exempt from withholding; dividends 80.8 percent of the income that was subject to
# tax; and dividend income subject to withholding taxed at an average effective rate of 18.2
# percent. Those give dividends subject to tax of 92.8 billion, tax on dividends of 16.9
# billion, and an effective rate on ALL dividends paid abroad of 0.0689. The derivation
# cross-checks: 16.9 of 21.1 is 80.0 percent of all withholding from dividends, which is
# what the SOI narrative says. The range runs from that all-dividend rate to the published
# rate on the taxed subset, so both endpoints are sourced.
WITHHOLDING_ALL_DIVIDENDS = 0.0689
WITHHOLDING_RANGE = [0.0689, 0.1820]

# ---- STILL SWEPT, with the reason recorded in the paper.
BOX = {
    "payout": PAYOUT_RANGE,
    "withholding_eff": WITHHOLDING_RANGE,
    # no aggregate effective rate on retirement distributions was located
    "ordinary_rate_retirement": [0.12, 0.24],
    # no asset share located. ICI and Vanguard report that 86 percent of plans offer a Roth
    # option in 2024 but only 18 percent of eligible participants use it, and designated
    # Roth balances are young, so the asset share is well below the participation share.
    "roth_share_of_dc": [0.05, 0.15],
    "gains_rate": list(K.U["shareholder_rate"]["range"]),
}
CEN = {k: float(np.mean(v)) for k, v in BOX.items()}
CEN["payout"] = PAYOUT_CENTRAL
CEN["withholding_eff"] = WITHHOLDING_ALL_DIVIDENDS
NAMES = list(BOX)


def layers(p):
    """The shareholder layer on the marginal object and on the annual object."""
    h = HOLDERS
    trad = (h["ira"] * (1 - ROTH_SHARE_OF_IRA)
            + h["defined_benefit"]
            + h["defined_contribution"] * (1 - p["roth_share_of_dc"]))
    roth = h["ira"] * ROTH_SHARE_OF_IRA + h["defined_contribution"] * p["roth_share_of_dc"]
    # Roth is reported as its own group, so it must NOT also sit in the exempt group. An
    # earlier version added it to both, which made the five reported groups sum to 1.028
    # instead of the 1.01 the source itself rounds to. Referee caught it.
    exempt = h["nonprofits"] + h["life_insurance_separate"] + h["government_and_529"]

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
                          "no_owner_level_tax": round(c["exempt_share"], 4),
                          "taxable_accounts": HOLDERS["taxable_accounts"],
                          "foreign": HOLDERS["foreign"]},
        "groups_sum": round(c["trad_share"] + c["roth_share"] + c["exempt_share"]
                            + HOLDERS["taxable_accounts"] + HOLDERS["foreign"], 4),
        "source_shares_sum": round(sum(HOLDERS.values()), 4),
        "groups_note": ("The five groups partition the holder shares and sum to the same "
                        "1.01 the source itself rounds to; they are not forced to one. The "
                        "group carrying no owner-level tax is nonprofits, government and 529 "
                        "plans, and life insurance separate accounts. Those holdings still "
                        "bear the ENTITY-level tax, so the claim is about the shareholder "
                        "layer and not about federal tax in total."),
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
        "{:.2f} is held abroad and bears withholding on dividends only; and only {:.3f} bears "
        "no owner-level federal tax at all, those holdings still bearing the entity tax. The "
        "five groups sum to the 1.01 the source itself rounds to."
    ).format(published_layer(CEN), c["marginal"], c["annual"],
             c["trad_share"], HOLDERS["foreign"], c["exempt_share"])
    (OUT / "shareholder_lifecycle.json").write_text(json.dumps(res, indent=2))
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
