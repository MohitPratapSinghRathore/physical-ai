"""Item 3: ONE DRIVER, TWO FINDINGS. How much of each exposure-type contrast is about
exposure type, and how much is about pay?

THE PROBLEM. The project reports two exposure-type contrasts and presents them as two
findings.

  A41, result 2. Embodied displacement is about 1.8 times more distress-efficient than
  cognitive AIOE displacement per dollar of wage income destroyed: 0.00613 percentage
  points of DSTI-50 crossings per billion dollars against 0.00342.

  A84. Embodied displacement costs the OASDI trust fund 17 to 20 percent more per displaced
  wage dollar, because 97.75 percent of the embodied wage bill sits under the contribution
  and benefit base against 81.19 percent of the cognitive AIOE wage bill.

Both have the same proximate cause: EMBODIED WORK IS LOWER PAID. Low pay puts a household
closer to its debt service threshold and it puts a wage dollar under the earnings cap. If
that is the whole story then the paper has one finding about pay, not two about exposure
type, and it should say so.

THE TEST. Reweight one exposure group so that its distribution across wage deciles matches
the other's, then recompute the contrast. What survives the reweighting is about exposure
type. What disappears is about pay. This is the standard reweighting decomposition; the
weights are constructed on deciles of individual annual wage income, computed on the
population of employed wage earners.

    raw gap        = statistic(embodied) - statistic(cognitive)
    reweighted gap = statistic(embodied) - statistic(cognitive reweighted to embodied pay)
    share of the gap that is about pay = 1 - reweighted gap / raw gap

WHAT THE TEST CANNOT DO. Reweighting on wage deciles holds PAY fixed; it does not hold
fixed everything that travels with pay, such as education, tenure, household structure or
the number of earners. A contrast that survives this test is not thereby shown to be causal
in exposure type; it is shown not to be an arithmetic consequence of the pay distribution
alone. That is the claim made here and no more.

COGNITIVE EXPOSURE MEASURES TASK OVERLAP, not displacement and not timing.

THE DISTRESS MEASURE. For the pay control the household engine's stochastic simulation is
replaced by its deterministic expectation, so that the statistic is a clean function of each
worker's own wage. Worker i in household h is displaced; the household loses (1 - rho*omega)
times that worker's wage; the household crosses if its obligation to income ratio passes 50
percent when it did not before. Summed over workers with person weights, and divided by the
wage income destroyed, this is the same pp-per-dollar object A41 reports. The LEVEL differs
slightly from A41 because A41 averages over draws of who is displaced; the CONTRAST is what
is tested here and the reweighting is applied identically to both groups.
"""
import io, json, pathlib, sys, zipfile
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).parents[1]
RAW, OUT = ROOT / "data" / "raw", ROOT / "data" / "processed"
sys.path.insert(0, str(ROOT))

RHO, OMEGA = 0.6616, 0.9554      # observed reemployment and reemployment wage, scenarios.py
DSTI_T = 0.50
OASDI_CAP = 184_500.0
NDEC = 10


def decile_edges(w, wt, n=NDEC):
    o = np.argsort(w)
    w, wt = w[o], wt[o]
    c = np.cumsum(wt) / wt.sum()
    return np.interp(np.linspace(0, 1, n + 1)[1:-1], c, w)


def reweight(src_dec, src_wt, tgt_dec, tgt_wt, n=NDEC):
    """Weights that move the source group onto the target group's decile distribution."""
    s = np.array([src_wt[src_dec == d].sum() for d in range(n)], float)
    t = np.array([tgt_wt[tgt_dec == d].sum() for d in range(n)], float)
    s_sh, t_sh = s / s.sum(), t / t.sum()
    f = np.divide(t_sh, s_sh, out=np.zeros_like(t_sh), where=s_sh > 0)
    return src_wt * f[src_dec]


def wmean(x, w):
    return float(np.sum(x * w) / np.sum(w)) if np.sum(w) > 0 else np.nan


# ---------------------------------------------------------------- ACS
def acs_panel():
    from src.stress import acs_engine as AE
    from src.stress import scenarios as SC
    _, groups = SC._h3().build_groups()
    P, H = AE.load_acs(with_reps=False)
    P, hh_idx = AE.link(P, H)
    oblig = (H["mort"].to_numpy(np.float64) + H["rent"].to_numpy(np.float64))[hh_idx]
    hinc = H["hincp"].to_numpy(np.float64)[hh_idx]
    core = H["working_core"].to_numpy(bool)[hh_idx]
    wage = P["wage"].to_numpy(np.float64)
    wt = P["pwgtp"].to_numpy(np.float64)

    loss = (1.0 - RHO * OMEGA) * wage
    post = np.maximum(hinc - loss, 0.0)
    with np.errstate(divide="ignore", invalid="ignore"):
        d0 = np.where(hinc > 0, oblig / np.maximum(hinc, 1e-9), np.inf)
        d1 = np.where(post > 0, oblig / np.maximum(post, 1e-9), np.inf)
    crosses = (oblig > 0) & core & (d0 <= DSTI_T) & (d1 > DSTI_T)

    return pd.DataFrame({"occp": P["occp"].to_numpy(), "wage": wage, "wt": wt,
                         "loss": loss, "crosses": crosses.astype(float),
                         "taxable": np.minimum(wage, OASDI_CAP)}), groups


# ---------------------------------------------------------------- SIPP
def sipp_panel():
    from src.stress import scenarios as SC
    _, groups = SC._h3().build_groups()
    cols = ["MONTHCODE", "WPFINWGT", "RMESR", "TJB1_OCC", "TPEARN"]
    z = zipfile.ZipFile(RAW / "sipp" / "pu2025_csv.zip")
    rows = []
    with z.open("pu2025.csv") as fh:
        txt = io.TextIOWrapper(fh, encoding="utf-8", errors="replace")
        header = txt.readline().rstrip("\n").split("|")
        idx = {c: header.index(c) for c in cols}
        mc = idx["MONTHCODE"]
        for line in txt:
            f = line.rstrip("\n").split("|")
            if len(f) <= mc or f[mc] != "12":
                continue
            rows.append([f[idx[c]] for c in cols])
    D = pd.DataFrame(rows, columns=cols)
    for c in cols:
        D[c] = pd.to_numeric(D[c], errors="coerce")
    D = D[D["RMESR"].isin([1, 2, 3, 4, 5])]
    wage = D["TPEARN"].fillna(0).to_numpy(np.float64) * 12.0
    wt = D["WPFINWGT"].fillna(0).to_numpy(np.float64)
    m = (wage > 0) & (wt > 0)
    return pd.DataFrame({"occp": D["TJB1_OCC"].to_numpy()[m], "wage": wage[m],
                         "wt": wt[m], "taxable": np.minimum(wage[m], OASDI_CAP)}), groups


# ---------------------------------------------------------------- the test
def contrast(panel, groups, stat, label, cog="cognitive_AIOE"):
    """stat(df, w) -> float. Returns the raw gap, the gap after reweighting the cognitive
    group onto the embodied pay distribution, and the share of the gap that is about pay."""
    edges = decile_edges(panel["wage"].to_numpy(), panel["wt"].to_numpy())
    dec = np.digitize(panel["wage"].to_numpy(), edges)
    E = panel["occp"].isin(groups["embodied"]).to_numpy()
    C = panel["occp"].isin(groups[cog]).to_numpy()

    e_stat = stat(panel[E], panel["wt"].to_numpy()[E])
    c_stat = stat(panel[C], panel["wt"].to_numpy()[C])
    w_c_rw = reweight(dec[C], panel["wt"].to_numpy()[C], dec[E], panel["wt"].to_numpy()[E])
    c_rw = stat(panel[C], w_c_rw)
    # and the mirror: embodied moved onto cognitive pay
    w_e_rw = reweight(dec[E], panel["wt"].to_numpy()[E], dec[C], panel["wt"].to_numpy()[C])
    e_rw = stat(panel[E], w_e_rw)

    raw = e_stat - c_stat
    rw1 = e_stat - c_rw
    rw2 = e_rw - c_stat
    return {"statistic": label, "index": cog,
            "embodied": e_stat, "cognitive": c_stat,
            "cognitive_reweighted_to_embodied_pay": c_rw,
            "embodied_reweighted_to_cognitive_pay": e_rw,
            "raw_gap": raw, "gap_after_reweighting_cognitive": rw1,
            "gap_after_reweighting_embodied": rw2,
            "share_of_gap_that_is_pay_a": 1 - rw1 / raw if raw else np.nan,
            "share_of_gap_that_is_pay_b": 1 - rw2 / raw if raw else np.nan,
            "mean_wage_embodied": wmean(panel["wage"].to_numpy()[E],
                                        panel["wt"].to_numpy()[E]),
            "mean_wage_cognitive": wmean(panel["wage"].to_numpy()[C],
                                         panel["wt"].to_numpy()[C])}


def stat_taxable_share(df, w):
    return float(np.sum(df["taxable"].to_numpy() * w) / np.sum(df["wage"].to_numpy() * w))


def stat_distress_per_bn(df, w):
    num = float(np.sum(df["crosses"].to_numpy() * w))
    den = float(np.sum(df["loss"].to_numpy() * w)) / 1e9
    return 100.0 * num / den / _obligated_base


_obligated_base = 1.0


def main():
    global _obligated_base
    res = []
    print("=== ITEM 3: ONE DRIVER, TWO FINDINGS. Controlling the contrasts for pay ===")

    A, groups = acs_panel()
    # denominator for the pp statistic: weighted obligated working-core households, so the
    # units match A41's percentage points of the obligated working core
    from src.stress import acs_engine as AE
    _obligated_base = 1.0   # set below once the household base is known
    hb = json.loads((OUT / "stress" / "acs_sipp_reconciliation.json").read_text()) \
        if (OUT / "stress" / "acs_sipp_reconciliation.json").exists() else {}
    _obligated_base = 69.20e6    # A41, obligated working-core households, weighted
    print(f"\n  pay levels: embodied and cognitive mean annual wage, ACS")

    for cog in ("cognitive_AIOE", "cognitive_GPT"):
        res.append({"dataset": "ACS", **contrast(A, groups, stat_distress_per_bn,
                                                 "distress_pp_per_bn", cog)})
        res.append({"dataset": "ACS", **contrast(A, groups, stat_taxable_share,
                                                 "share_under_OASDI_cap", cog)})
    S, groups_s = sipp_panel()
    for cog in ("cognitive_AIOE", "cognitive_GPT"):
        res.append({"dataset": "SIPP", **contrast(S, groups_s, stat_taxable_share,
                                                  "share_under_OASDI_cap", cog)})
    R = pd.DataFrame(res)
    R.round(6).to_csv(OUT / "pay_control.csv", index=False)

    pd.set_option("display.width", 250)
    print("\n=== MEAN ANNUAL WAGE, the driver ===")
    for _, r in R.drop_duplicates(["dataset", "index"]).iterrows():
        print(f"  {r.dataset:5s} {r['index']:15s}  embodied {r.mean_wage_embodied:>9,.0f}  "
              f"cognitive {r.mean_wage_cognitive:>9,.0f}  "
              f"ratio {r.mean_wage_embodied / r.mean_wage_cognitive:.3f}")

    print("\n=== HOW MUCH OF EACH CONTRAST IS ABOUT PAY? ===")
    for _, r in R.iterrows():
        print(f"\n  {r.dataset} | {r.statistic} | {r['index']}")
        print(f"    embodied {r.embodied:.5f}   cognitive {r.cognitive:.5f}   "
              f"raw gap {r.raw_gap:+.5f}")
        print(f"    cognitive reweighted to embodied pay {r.cognitive_reweighted_to_embodied_pay:.5f}"
              f"  -> gap {r.gap_after_reweighting_cognitive:+.5f}")
        print(f"    embodied reweighted to cognitive pay {r.embodied_reweighted_to_cognitive_pay:.5f}"
              f"  -> gap {r.gap_after_reweighting_embodied:+.5f}")
        a, b = r.share_of_gap_that_is_pay_a, r.share_of_gap_that_is_pay_b
        print(f"    SHARE OF THE GAP THAT IS PAY: {a:.1%} and {b:.1%} "
              f"(the two directions of the reweighting)")
        surv = 1 - max(a, b)
        print(f"    SURVIVES the pay control: {surv:.1%} of the raw gap at the weaker end")

    (OUT / "pay_control_summary.json").write_text(
        json.dumps(R.round(6).to_dict("records"), indent=2, default=str))


if __name__ == "__main__":
    main()
