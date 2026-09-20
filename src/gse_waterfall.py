"""Item 1 of the final analysis session. Rebuild of the agency mortgage waterfall, loan
class by loan class.

WHY THIS EXISTS. The superseded construction in src/capacity.py wrote the loss transfer as

    transferred = min(GSE loss, CRT risk in force + PMI risk in force)

with CRT risk in force 210.0bn and PMI risk in force 382.855bn. The independent replicator
showed that this makes the federal `beyond` term dead code: the 592.855bn layer is never
reached at any dose in [0, 1], so both our published figure (about 30 percent of GSE net
worth) and the replicator's zero are artefacts of the formula rather than results.

Three things were wrong with it.

  1. Risk in force is MAXIMUM COVERAGE, not a first-loss layer. Writing it as
     min(loss, RIF) grants both instruments first-dollar coverage at full notional.
  2. The 210.0bn CRT figure is the FHFA cumulative 2013 to 2023 risk transferred at
     ISSUANCE across both Enterprises. The OUTSTANDING back-end risk in force on the
     2025 books is 39bn (Fannie) plus 40.0bn (Freddie STACR and ACIS), about 79bn.
  3. PMI was assumed to cover about 6 percent of the single-family book. It does not.
     6 percent is risk in force OVER the book, which is the covered share TIMES the
     coverage depth. Fannie's mortgage insurance IN FORCE is 745.9bn, 21 percent of the
     book; Freddie's is 681.0bn, 22 percent. The coverage depth is about 26.6 percent.

Every input below is read from the Enterprises' own 2025 Form 10-K filings, retrieved to
data/raw/gse/. Quotes are given inline so each number can be checked against the source.
"""
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"

SOURCE = {
    "fnma": "Fannie Mae 2025 Form 10-K, accession 0000310522-26-000015, "
            "https://www.sec.gov/Archives/edgar/data/310522/000031052226000015/fnm-20251231.htm",
    "fmcc": "Freddie Mac 2025 Form 10-K, accession 0001026214-26-000021, "
            "https://www.sec.gov/Archives/edgar/data/1026214/000102621426000021/fmcc-20251231.htm",
}

# ---------------------------------------------------------------- 1. the books
# FANNIE MAE, "Single-Family Loans with Credit Enhancement, As of December 31, 2025"
#   Primary mortgage insurance            $756bn   21% of the SF conventional guaranty book
#   Connecticut Avenue Securities          859      24
#   Credit Insurance Risk Transfer         418      12
#   Other                                   28       1
#   Less loans with multiple enhancements (398)    (11)
#   Total with credit enhancement        $1,663     47%
# "The risk in force of our back-end single-family credit risk transfer transactions, which
#  refers to the maximum amount of losses that could be absorbed by credit risk transfer
#  investors, was approximately $39 billion as of December 31, 2025."
# "Our total mortgage insurance in force was $745.9 billion, or 21% of our single-family
#  conventional guaranty book of business ... our total mortgage insurance risk in force was
#  $201.4 billion."
#
# FREDDIE MAC, "Table 23 - Single-Family Mortgage Portfolio Credit Enhancement Coverage
# Outstanding, December 31, 2025" (UPB, % of portfolio, maximum coverage, $m):
#   Primary mortgage insurance   680,950  22%  181,462
#   STACR                      1,165,412  37    24,935
#   ACIS                         594,409  19    15,081
#   Other                         38,373   1    10,361
#   Less multiple / reconciling (552,393) (18)      --
#   Credit-enhanced            1,926,751  61   231,839
#   Non-credit-enhanced        1,229,539  39      N/A
#   Total                      3,156,290 100%  231,839
BOOKS = {
    "Fannie Mae": {
        # book implied by the table's own 1,663bn at 47 percent. The 10-K separately
        # reports an AVERAGE 2025 book of 3.59tn; this is the point-in-time figure
        # consistent with the credit enhancement table and is used for that reason.
        "book_bn": 1663.0 / 0.47,
        "pmi_upb_bn": 756.0,
        "pmi_rif_bn": 201.355,
        "crt_upb_bn": 859.0 + 418.0,          # CAS plus CIRT reference pools
        "crt_rif_bn": 39.0,                   # outstanding back-end risk in force
        "other_upb_bn": 28.0,
        "credit_enhanced_bn": 1663.0,
        "overlap_bn": 398.0,
        "net_worth_bn": 109.0,                # "our net worth was $109.0 billion"
        "gfee_income_bn": 23.595,             # total net interest income from guaranty book
        "ppe_bn": 14.36 + 3.62 + 1.61,        # net income + tax + provision, FY2025
    },
    "Freddie Mac": {
        "book_bn": 3156.290,
        "pmi_upb_bn": 680.950,
        "pmi_rif_bn": 181.462,
        "crt_upb_bn": 1165.412 + 594.409,     # STACR plus ACIS reference pools
        "crt_rif_bn": 24.935 + 15.081,
        "other_upb_bn": 38.373,
        "credit_enhanced_bn": 1926.751,
        "overlap_bn": 552.393,
        "net_worth_bn": 70.4,                 # "Net worth was $70.4 billion"
        "gfee_income_bn": 16.897,             # total guarantee net interest income
        "ppe_bn": 10.73 + 2.63 + 1.29,
    },
}

# ---------------------------------------------------------- 2. coverage structure
# PMI. "Our Charter generally requires credit enhancement on any single-family conventional
# mortgage loan that we purchase or securitize if it has an LTV ratio over 80% at the time
# of acquisition" (Fannie); Freddie's Charter clause is the same. So PMI is present ONLY on
# the above-80 LTV slice, which is what the 21 and 22 percent covered shares measure, and it
# pays a COVERAGE PERCENTAGE of the claim rather than the whole loss. The depth is read off
# the filings directly as risk in force over insurance in force.
#
# CRT attachment. Fannie: "In CIRT deals, we generally retain an initial portion of losses on
# the loans in the pool (for example, the first 0.75% of the initial pool UPB). Reinsurers
# cover losses above this retention amount up to a detachment point (for example, the next
# 4.0% of the initial pool UPB). We retain all losses above this detachment point."
# Freddie: "we transfer to third-party investors a portion of the credit risk between a
# specified attachment point and a detachment point ... We generally retain the initial loss
# position and at least 5% of the credit risk of all the positions sold."
# Both: "We retain a portion of the future credit losses on all loans covered by CAS and CIRT
# transactions, including all or a portion of the first loss positions in most transactions."
CRT_ATTACHMENT = 0.0075        # 0.75 percent of pool UPB, the filing's own example
CRT_VERTICAL_RETAINED = 0.05   # Freddie's stated minimum vertical retention of sold positions
OTHER_DEPTH = 0.27             # Freddie's "Other" is 10,361 / 38,373 = 27.0 percent; applied
                               # to Fannie's undisclosed "Other" as the only sourced analogue

# Loss intensity by class. Freddie, "Serious Delinquency Rates for Credit-Enhanced and
# Non-Credit-Enhanced Loans in Our Single-Family Mortgage Portfolio, December 31, 2025":
#   Primary mortgage insurance 22% of portfolio, SDQ 1.19%
#   CRT and other              52%,              SDQ 0.68%
#   Non-credit-enhanced        39%,              SDQ 0.40%
# PMI loans default about three times as often as uninsured loans, because they are the
# high-LTV slice. Allocating a shock pro rata by UPB would understate the share of losses
# landing where the cover is, so relative SDQ is used as the class loss weight, with a flat
# pro-rata alternative reported as the sensitivity.
SDQ = {"pmi": 1.19, "crt": 0.68, "other": 0.68, "none": 0.40}


def classes(e):
    """Partition one Enterprise's single-family book into five mutually exclusive classes.

    The filings give the credit enhancement buckets GROSS and then a single combined
    'loans covered by multiple credit enhancements' deduction, without saying which pairs
    overlap. ASSUMPTION, stated: the whole overlap is PMI and CRT together. That is the
    economically dominant pair, because both instruments select the same high-LTV loans,
    and it is bounded: the overlap cannot exceed the PMI bucket, and for both Enterprises
    it does not.
    """
    pmi, crt, oth, ov = e["pmi_upb_bn"], e["crt_upb_bn"], e["other_upb_bn"], e["overlap_bn"]
    assert ov <= pmi, "overlap exceeds the PMI bucket, the assumption fails"
    out = {
        "pmi_only": pmi - ov,
        "pmi_and_crt": ov,
        "crt_only": crt - ov,
        "other_only": oth,
        "none": e["book_bn"] - e["credit_enhanced_bn"],
    }
    check = sum(v for k, v in out.items() if k != "none")
    assert abs(check - e["credit_enhanced_bn"]) < 1e-6, (check, e["credit_enhanced_bn"])
    return out


def cover(cls, upb, loss, e):
    """Loss absorbed by private cover on one class, and the residue left to the Enterprise.

    loss is the dollar loss falling on this class. All returns are in bn.
    """
    if upb <= 0 or loss <= 0:
        return 0.0, max(loss, 0.0)
    lam = loss / upb                               # loss rate on the class
    d_pmi = e["pmi_rif_bn"] / e["pmi_upb_bn"]      # coverage depth, ~0.266
    w_crt = e["crt_rif_bn"] / e["crt_upb_bn"]      # outstanding band width as a share of pool
    a, det = CRT_ATTACHMENT, CRT_ATTACHMENT + w_crt

    def crt_band(rate):
        """Investor share of a loss rate, mezzanine: nothing below attachment, nothing
        above detachment, and the Enterprise keeps a vertical slice of what is sold."""
        band = max(0.0, min(rate, det) - a)
        return band * (1.0 - CRT_VERTICAL_RETAINED)

    if cls == "none":
        return 0.0, loss
    if cls == "pmi_only":
        absorbed = min(d_pmi * lam, d_pmi) * upb
    elif cls == "other_only":
        absorbed = min(OTHER_DEPTH * lam, OTHER_DEPTH) * upb
    elif cls == "crt_only":
        absorbed = crt_band(lam) * upb
    elif cls == "pmi_and_crt":
        # PMI is front-end. The 10-K nets it before the reference pool loss is struck:
        # CRT transactions are stated to be net of "any proceeds received from front-end
        # credit enhancements, such as primary mortgage insurance".
        pmi_abs = min(d_pmi * lam, d_pmi)
        absorbed = (pmi_abs + crt_band(lam - pmi_abs)) * upb
    else:
        raise ValueError(cls)
    absorbed = min(absorbed, loss)
    return absorbed, loss - absorbed


def waterfall(agency_loss_bn, pro_rata=False):
    """Run the rebuilt waterfall for a total agency (Fannie plus Freddie) dollar loss."""
    tot_book = sum(e["book_bn"] for e in BOOKS.values())
    rows, transferred, retained = [], 0.0, 0.0
    for name, e in BOOKS.items():
        ent_loss = agency_loss_bn * e["book_bn"] / tot_book     # split by book size
        cl = classes(e)
        if pro_rata:
            wts = dict(cl)
        else:
            key = {"pmi_only": "pmi", "pmi_and_crt": "pmi", "crt_only": "crt",
                   "other_only": "other", "none": "none"}
            wts = {k: v * SDQ[key[k]] for k, v in cl.items()}
        wsum = sum(wts.values())
        for k, upb in cl.items():
            cls_loss = ent_loss * wts[k] / wsum
            abs_, res = cover(k, upb, cls_loss, e)
            transferred += abs_
            retained += res
            rows.append({"enterprise": name, "loan_class": k, "upb_bn": upb,
                         "share_of_book": upb / e["book_bn"], "loss_bn": cls_loss,
                         "private_cover_bn": abs_, "enterprise_retains_bn": res})
    cap = sum(e["net_worth_bn"] for e in BOOKS.values())
    ppe = sum(e["ppe_bn"] for e in BOOKS.values())
    gfee = sum(e["gfee_income_bn"] for e in BOOKS.values())
    # Guarantee fee income is a flow already inside pre-provision pre-tax earnings, so it is
    # NOT added again. It is reported separately because it is the annual replenishment rate
    # of the buffer and it is what a scenario would have to impair to change the answer.
    absorbed = min(retained, cap + ppe)
    beyond = max(0.0, retained - cap - ppe)
    return {"agency_loss_bn": agency_loss_bn, "transferred_bn": transferred,
            "retained_bn": retained, "capital_bn": cap, "one_year_ppnr_bn": ppe,
            "gfee_income_bn": gfee, "absorbed_bn": absorbed, "federal_beyond_bn": beyond,
            "retained_share_of_loss": retained / agency_loss_bn if agency_loss_bn else 0.0,
            "retained_pct_of_net_worth": 100 * retained / cap,
            "rows": rows}


def main():
    dr = pd.read_csv(PROC / "dose_response_first_round.csv")
    doses = sorted(dr["dose_share_of_total_wage_bill"].unique())
    out, detail = [], []
    for dose in doses:
        d = dr[dr["dose_share_of_total_wage_bill"] == dose]
        lo = float(d["mortgage_agency_loss_lo_bn"].min())
        hi = float(d["mortgage_agency_loss_hi_bn"].max())
        inside = bool(d["inside_observed_data_range"].any())
        for tag, L in [("lo", lo), ("hi", hi)]:
            for prm, pr in [("sdq_weighted", False), ("pro_rata", True)]:
                w = waterfall(L, pro_rata=pr)
                out.append({"dose": dose, "end": tag, "weighting": prm,
                            "inside_observed_data_range": inside,
                            **{k: v for k, v in w.items() if k != "rows"}})
                if tag == "hi" and prm == "sdq_weighted":
                    for r in w["rows"]:
                        detail.append({"dose": dose, **r})
    o = pd.DataFrame(out)
    o.to_csv(PROC / "gse_waterfall_rebuilt.csv", index=False)
    pd.DataFrame(detail).to_csv(PROC / "gse_waterfall_classes.csv", index=False)

    # the structural table, independent of any dose
    struct = []
    for name, e in BOOKS.items():
        for k, upb in classes(e).items():
            struct.append({"enterprise": name, "loan_class": k, "upb_bn": round(upb, 1),
                           "share_of_book": round(upb / e["book_bn"], 4)})
    pd.DataFrame(struct).to_csv(PROC / "gse_book_structure.csv", index=False)

    summ = {
        "pmi_covered_share_of_book": {
            n: round(e["pmi_upb_bn"] / e["book_bn"], 4) for n, e in BOOKS.items()},
        "pmi_coverage_depth": {
            n: round(e["pmi_rif_bn"] / e["pmi_upb_bn"], 4) for n, e in BOOKS.items()},
        "crt_reference_pool_share_of_book": {
            n: round(e["crt_upb_bn"] / e["book_bn"], 4) for n, e in BOOKS.items()},
        "crt_outstanding_band_width_of_pool": {
            n: round(e["crt_rif_bn"] / e["crt_upb_bn"], 5) for n, e in BOOKS.items()},
        "crt_attachment": CRT_ATTACHMENT,
        "crt_vertical_retained": CRT_VERTICAL_RETAINED,
        "superseded_transfer_layer_bn": 592.855,
        "rebuilt_crt_risk_in_force_bn": round(
            sum(e["crt_rif_bn"] for e in BOOKS.values()), 3),
        "rebuilt_pmi_risk_in_force_bn": round(
            sum(e["pmi_rif_bn"] for e in BOOKS.values()), 3),
        "capital_bn": sum(e["net_worth_bn"] for e in BOOKS.values()),
        "one_year_ppnr_bn": round(sum(e["ppe_bn"] for e in BOOKS.values()), 3),
        "gfee_income_bn": round(sum(e["gfee_income_bn"] for e in BOOKS.values()), 3),
        "sources": SOURCE,
    }
    (PROC / "gse_waterfall_summary.json").write_text(json.dumps(summ, indent=2))

    pd.set_option("display.width", 200)
    print("STRUCTURE")
    print(pd.DataFrame(struct).to_string(index=False))
    print()
    print("HEADLINE COVERAGE PARAMETERS")
    for k in ["pmi_covered_share_of_book", "pmi_coverage_depth",
              "crt_reference_pool_share_of_book", "crt_outstanding_band_width_of_pool"]:
        print(" ", k, summ[k])
    print()
    print("WATERFALL")
    cols = ["dose", "end", "weighting", "inside_observed_data_range", "agency_loss_bn",
            "transferred_bn", "retained_bn", "retained_share_of_loss",
            "retained_pct_of_net_worth", "federal_beyond_bn"]
    print(o[cols].round(4).to_string(index=False))


if __name__ == "__main__":
    main()
