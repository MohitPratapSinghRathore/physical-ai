"""Item 4 of the final analysis session. The federal share of first-round losses, reported
BY DOSE rather than as one range, recomputed under the item 1 GSE rebuild.

The published object sealed only a min and a max over an unstated sweep, which is exactly
what the replicator could not reproduce (their insufficiency I-6). A single range hides the
one thing the number actually does: it RISES with the dose, because the fiscal component
grows faster than linearly while credit losses grow roughly linearly.

TWO READINGS OF THE AGENCY BOOK, and both are reported because item 1 showed they differ.

  NARROW, as published. Only the loss BEYOND Enterprise capital plus a year of earnings is
    federal. Everything the Enterprises absorb, and everything private cover takes, is
    private. Under the item 1 rebuild the beyond layer is still zero at every dose, now for
    a real reason (179.4bn of capital against a maximum retained loss of 109.0bn) rather
    than because of a phantom 592.855bn transfer layer.

  CONSERVATORSHIP. The RETAINED Enterprise loss is federal in substance. The Enterprises are
    in conservatorship, their net worth stands behind the Treasury senior preferred
    agreements, and there are no private shareholders positioned to absorb anything. Only
    what private cover actually takes, the PMI claim payments and the CRT band, is private.

The narrow reading is a lower bound on the federal share and the conservatorship reading is
the upper bound. Both travel together.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

from gse_waterfall import waterfall

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "processed"

FEDERAL_STUDENT_SHARE = 1605.134 / 1650.0   # FRED FGCCSAQ027S over NY Fed total
STUDENT_BANK_SHARE = 0.449


def rows_for(d, reading):
    """One dose-response row to a federal and private first-round split."""
    student_total = d.student_loan_holders_loss_hi_bn / STUDENT_BANK_SHARE
    student_fed = student_total * FEDERAL_STUDENT_SHARE

    gse_loss = float(d.mortgage_agency_loss_hi_bn)
    w = waterfall(gse_loss)
    private_cover = w["transferred_bn"]         # PMI claims plus the CRT band
    retained = w["retained_bn"]                 # what the Enterprises keep
    beyond = w["federal_beyond_bn"]             # still zero, see the docstring

    if reading == "narrow":
        gse_fed, gse_priv = beyond, private_cover + retained - beyond
    elif reading == "conservatorship":
        gse_fed, gse_priv = retained, private_cover
    else:
        raise ValueError(reading)

    fha = float(d.get("mortgage_FHA_loss_hi_bn", 0.0))
    fed = (d.public_budget_loss_hi_bn + d.oasdi_loss_hi_bn + d.hi_loss_hi_bn
           + student_fed + fha + gse_fed)
    priv = (d.mortgage_bank_held_loss_hi_bn
            + d.get("mortgage_residual_holders_loss_hi_bn", 0.0)
            + d.auto_lenders_loss_hi_bn + d.card_consumer_lenders_loss_hi_bn
            + (student_total - student_fed) + gse_priv)
    return {"reading": reading, "federal_bn": float(fed), "private_bn": float(priv),
            "federal_share": float(fed / (fed + priv)),
            "gse_loss_bn": gse_loss, "gse_private_cover_bn": private_cover,
            "gse_retained_bn": retained, "gse_beyond_bn": beyond}


def main():
    D = pd.read_csv(OUT / "dose_response_first_round.csv")
    out = []
    for _, d in D.iterrows():
        for reading in ("narrow", "conservatorship"):
            out.append({"exposure_type": d.exposure_type, "incidence": d.incidence,
                        "dose": d.dose_share_of_total_wage_bill,
                        "inside_observed_data_range": bool(d.inside_observed_data_range),
                        **rows_for(d, reading)})
    F = pd.DataFrame(out)
    F.round(6).to_csv(OUT / "item4_federal_share_by_dose.csv", index=False)

    # BY DOSE, which is the point of the item
    bydose = (F.groupby(["reading", "dose"])
                .agg(federal_share_min=("federal_share", "min"),
                     federal_share_max=("federal_share", "max"),
                     federal_share_median=("federal_share", "median"),
                     inside=("inside_observed_data_range", "any"))
                .reset_index())
    bydose.round(6).to_csv(OUT / "item4_federal_share_summary.csv", index=False)

    # and by dose AND exposure type, because the axis matters
    byboth = (F.groupby(["reading", "dose", "exposure_type"])
                .agg(lo=("federal_share", "min"), hi=("federal_share", "max"))
                .reset_index())

    nar = bydose[bydose.reading == "narrow"]
    con = bydose[bydose.reading == "conservatorship"]
    summ = {
        "headline_depends_on_the_dose": True,
        "by_dose_narrow": {str(r.dose): [round(r.federal_share_min, 4),
                                         round(r.federal_share_max, 4)]
                           for r in nar.itertuples()},
        "by_dose_conservatorship": {str(r.dose): [round(r.federal_share_min, 4),
                                                  round(r.federal_share_max, 4)]
                                    for r in con.itertuples()},
        "inside_data_doses": sorted(
            float(x) for x in bydose[bydose.inside].dose.unique()),
        "single_range_that_hides_it_narrow": [round(float(F[F.reading == "narrow"]
                                                          .federal_share.min()), 4),
                                              round(float(F[F.reading == "narrow"]
                                                          .federal_share.max()), 4)],
        "replicator_by_dose": {"0.10": 0.8373, "0.25": 0.8792, "0.50": 0.8956},
        "gse_rebuild_effect_on_narrow_reading":
            "none. The beyond layer is zero before and after, so reallocating the GSE loss "
            "between private cover and Enterprise capital leaves both on the private side "
            "under the narrow reading. The rebuild changes the CONSERVATORSHIP reading.",
    }
    (OUT / "item4_federal_share_summary.json").write_text(json.dumps(summ, indent=2))

    pd.set_option("display.width", 200)
    print("FEDERAL SHARE OF FIRST-ROUND LOSSES, BY DOSE")
    print(bydose.round(4).to_string(index=False))
    print()
    print("BY DOSE AND EXPOSURE TYPE")
    print(byboth.round(4).to_string(index=False))
    print()
    print("GSE layers under the rebuild, high end by dose")
    g = (F[F.reading == "conservatorship"].groupby("dose")
         .agg(gse_loss=("gse_loss_bn", "max"), cover=("gse_private_cover_bn", "max"),
              retained=("gse_retained_bn", "max"), beyond=("gse_beyond_bn", "max")))
    print(g.round(3).to_string())


if __name__ == "__main__":
    main()
