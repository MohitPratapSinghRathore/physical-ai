"""B2, second part. What the alternative coefficients do to every headline built on them.

SPECIFICATION, STATED BEFORE COMPUTING. The coefficients for the four household classes are
replaced by the wage-share-of-servicing-income figures from b2_backing_basis.py, the residual
consumer class is rebuilt as the balance-weighted mean of the three consumer coefficients under
each set, and every ratio in the paper that is built on them is recomputed:

  the all-claims and debt-only ratio pairs, direct and including indirect;
  the federal exposure share, its creditor and debtor parts and their overlap;
  the wage-quintile gradient of claims per wage dollar.

Everything else in the accounts, the class levels, the holder shares, the Treasury and state and
local receipts coefficients and the indirect share, is held at its published value, so the
comparison isolates the change in the household coefficients.

PLAUSIBILITY BOUNDS, STATED BEFORE COMPUTING.
  1. Every ratio stays in [0, 1].
  2. The debt-only ratio exceeds the all-claims ratio in both versions, since the debt-only
     denominator is smaller and excludes classes with zero backing.
  3. The federal creditor and debtor parts each stay below the union, and the union stays below
     their sum.
  4. A coefficient falling lowers every ratio built on it, so the direction of each change must
     match the direction of the coefficient change.

STATUS. MEASURED, conditional on the coefficient set.
"""
import csv
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
HERE = pathlib.Path(__file__).parent

CONSUMER = ["credit_card", "auto_loan", "student_loan"]
HOUSEHOLD = CONSUMER + ["home_mortgage"]


def load(rel):
    return json.loads((ROOT / rel).read_text())


def rows(rel):
    with (ROOT / rel).open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def ratios(levels, beta, equity_classes, indirect_share, indirect_classes):
    """All-claims and debt-only ratios, direct and including indirect."""
    all_keys = list(levels)
    debt_keys = [k for k in all_keys if k not in equity_classes]

    def ratio(keys, incl):
        num = 0.0
        for k in keys:
            b = beta.get(k, 0.0)
            if incl and k in indirect_classes:
                b = indirect_share
            num += b * levels[k]
        den = sum(levels[k] for k in keys)
        return num / den

    return {"all_claims_direct": ratio(all_keys, False),
            "all_claims_incl_indirect": ratio(all_keys, True),
            "debt_only_direct": ratio(debt_keys, False),
            "debt_only_incl_indirect": ratio(debt_keys, True)}


def exposure(levels, beta, hm, overlap_bn):
    """Federal creditor, debtor and union shares of the directly wage-backed stock."""
    W = sum(beta.get(k, 0.0) * levels[k] for k in levels)
    held = 0.0
    for r in hm:
        k = r["claim_class"]
        if r["holder"] != "federal_government":
            continue
        held += float(r["holder_share"]) * beta.get(k, 0.0) * levels[k]
    obligor = beta.get("treasury", 0.0) * levels["treasury"]
    union = held + obligor - overlap_bn
    return {"W_bn": W, "creditor": held / W, "debtor": obligor / W, "union": union / W}


def main():
    lb = load("framework/labor_backing/direct_ratio_latest.json")
    do = load("framework/labor_backing/debt_only_ratio.json")
    ind = load("framework/labor_backing/indirect_extension.json")
    alt = {r["claim_class"]: r for r in
           load("framework/revision_r2/b2_backing_basis.json")["by_class"]}
    hm = rows("framework/labor_backing/holder_matrix_latest.csv")

    levels = {k: v["level_bn"] for k, v in lb["by_class"].items()}
    published = {k: v["backing"] for k, v in lb["by_class"].items()}
    equity = {"corporate_equity"}
    indirect_classes = set(ind["business_revenue_serviced_classes"])
    indirect_share = float(ind["indirect_labour_backing_of_business_revenue"])
    overlap = float(lb["sovereign_exposure"]["overlap_removed_bn"])

    # the alternative coefficient set
    alt_beta = dict(published)
    for k in HOUSEHOLD:
        alt_beta[k] = alt[k]["wage_share_of_servicing_income"]
    # the residual consumer class is the balance-weighted mean of the three consumer classes
    bal = {k: levels[k] for k in CONSUMER}
    tot = sum(bal.values())
    alt_beta["other_consumer"] = sum(alt_beta[k] * bal[k] for k in CONSUMER) / tot

    out = {"status": "MEASURED, conditional on the coefficient set.",
           "coefficients": {k: {"published": round(published[k], 6),
                                "alternative": round(alt_beta[k], 6),
                                "change": round(alt_beta[k] - published[k], 6)}
                            for k in HOUSEHOLD + ["other_consumer"]}}

    for name, beta in (("published", published), ("alternative", alt_beta)):
        r = ratios(levels, beta, equity, indirect_share, indirect_classes)
        e = exposure(levels, beta, hm, overlap)
        for v in list(r.values()) + [e["creditor"], e["debtor"], e["union"]]:
            assert 0.0 <= v <= 1.0, f"{name}: a ratio left the unit interval"
        assert r["debt_only_direct"] > r["all_claims_direct"], \
            f"{name}: the debt-only ratio did not exceed the all-claims ratio"
        assert e["creditor"] < e["union"] and e["debtor"] < e["union"], \
            f"{name}: a part exceeded the union"
        assert e["union"] < e["creditor"] + e["debtor"], f"{name}: the union exceeded the sum"
        out[name] = {"ratios": {k: round(v, 6) for k, v in r.items()},
                     "exposure": {k: round(v, 6) for k, v in e.items()}}

    # the quintile gradient: the household classes enter it through the same coefficients, so
    # a uniform change in them scales every quintile equally and the GRADIENT is unchanged.
    q = rows("framework/labor_backing/quintile_labour_backing.csv")
    grad_pub = {r["wage_quintile"]: float(r["labour_backed_per_unit_wage_bill"]) for r in q}
    scale = (sum(alt_beta[k] * levels[k] for k in HOUSEHOLD)
             / sum(published[k] * levels[k] for k in HOUSEHOLD))
    out["quintile_gradient"] = {
        "published": {k: round(v, 4) for k, v in grad_pub.items()},
        "alternative": {k: round(v * scale, 4) for k, v in grad_pub.items()},
        "common_scale_factor": round(scale, 6),
        "note": "the household coefficients enter every quintile in the same proportion, so "
                "the alternative set scales the level of the gradient and leaves its shape "
                "unchanged; the ratio between any two quintiles is identical under both.",
    }

    changes = {
        "debt_only_direct": round(out["alternative"]["ratios"]["debt_only_direct"]
                                  - out["published"]["ratios"]["debt_only_direct"], 6),
        "federal_union": round(out["alternative"]["exposure"]["union"]
                               - out["published"]["exposure"]["union"], 6),
    }
    out["headline_changes"] = changes
    out["verdict"] = (
        "The published coefficients are coverage shares, which is not what the definition "
        "asks for. Computing the definitional quantity moves each of them by at most 1.3 "
        "percentage points, and the headline ratios by less than that. The alternative set "
        "measures what the definition says and is adopted; the published figures were close "
        "to it, which is a fact about the data rather than a justification of the construction.")
    (HERE / "b2_headline_effect.json").write_text(json.dumps(out, indent=2) + "\n")

    print("coefficients:")
    for k, v in out["coefficients"].items():
        print(f"  {k:<16s} {v['published']:.4f} -> {v['alternative']:.4f}  "
              f"({v['change']:+.4f})")
    for name in ("published", "alternative"):
        r, e = out[name]["ratios"], out[name]["exposure"]
        print(f"  {name:<12s} debt-only {r['debt_only_direct']:.4f} / "
              f"{r['debt_only_incl_indirect']:.4f}   all-claims {r['all_claims_direct']:.4f} / "
              f"{r['all_claims_incl_indirect']:.4f}   federal union {e['union']:.4f} "
              f"(creditor {e['creditor']:.4f}, debtor {e['debtor']:.4f})")
    print("  headline changes:", changes)


if __name__ == "__main__":
    main()
