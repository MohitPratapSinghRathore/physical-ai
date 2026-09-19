"""ACS household stress-test engine: mortgage service and rent under displacement scenarios.

WHAT THIS REPLACES. Every earlier "debt at risk" figure in this repository was produced by
giving an exposure group a slice of national obligations equal to its slice of the national
wage bill. A39 showed that step is an aggregation artifact: obligation per wage dollar varies
six to eleven fold across wage deciles, so the slice is right only if displacement is drawn
wage-neutrally inside the group. This engine never forms a share. It simulates displacement
worker by worker, recomputes each household's income, and counts households and dollars.

METHOD

1. Person pass. Every ACS person with a valid OCCP and positive wage income is kept with
   their household id, wage, person weight, and within-occupation wage percentile.
2. Household pass. Mortgage payment (MRGP x 12), gross rent (GRNTP x 12), household income
   (HINCP), household weight and the 80 successive-difference replicate weights.
   Non-wage income is HINCP minus the household's own summed wage income, which is the
   quantity that survives a displacement shock: transfers, pensions, interest, self-employment.
3. Simulation. For each scenario configuration and each of R draws, every worker is displaced
   with probability p (src/stress/scenarios.py) and, if displaced, reemployed with
   probability rho at wage ratio omega. Post-shock household income is non-wage income plus
   surviving and reemployed wages.
4. Statistics. Debt service to income (DSTI) crossing 30, 40 and 50 percent, and the dollars
   of mortgage service and rent owed by households that cross. Averaged over draws, then
   weighted.

INTERVALS. Replicate intervals use the ACS successive-difference formula, V = (4/80) sum of
squared deviations, applied to the SAME simulated draws, so they are sampling intervals
CONDITIONAL on the simulation. Simulation variance is reported separately as the standard
deviation of the statistic across draws. The two are not added; they are different things and
both are printed. Intervals are computed for the headline configurations only, because the
replicate weight matrix must be streamed and the full grid has too many cells.

DENOMINATOR (prompt item 2). Households with no employed member aged 25 to 64 cannot be
displaced and are reported as a separate row, never folded into a pass-through rate. Their
mortgage and rent obligations are the "not wage-backed" portion. A38 put that at 19.7 percent
of mortgage service and 30.1 percent of rent. Their transfer and pension income is partly
payroll-tax funded, which links to the OASDI result; that link is stated in the findings and
is NOT added to any total here, to avoid double counting.

CAVEAT on every cognitive configuration: AIOE and Eloundou GPT measure TASK OVERLAP, not
displacement and not timing, and the conversion of that rank into a displacement probability
is an assumption of this engine, not a measurement.
"""
import io, json, pathlib, zipfile
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).parents[2]
RAW, OUT = ROOT / "data" / "raw", ROOT / "data" / "processed"
STRESS = OUT / "stress"
PPART = ["psam_pusa.csv", "psam_pusb.csv"]
HPART = ["psam_husa.csv", "psam_husb.csv"]
NREP = 80
SEED = 20260919
R_DRAWS = 30
DSTI_THRESHOLDS = (0.30, 0.40, 0.50)


def _chunks(zf, fn, cols, size=400_000):
    z = zipfile.ZipFile(RAW / "pums" / zf)
    with z.open(fn) as fh:
        for ch in pd.read_csv(io.TextIOWrapper(fh, encoding="utf-8", errors="replace"),
                              usecols=cols, dtype={"SERIALNO": str},
                              chunksize=size, low_memory=False):
            yield ch


def load_acs(with_reps=True):
    """Returns (P, H) with P person-level workers and H household-level obligations.

    with_reps=False skips the 80 replicate weight columns, which is roughly three times
    faster and is used by the comparison run, where no interval is needed.
    """
    print("  person pass ...")
    pp = []
    for fn in PPART:
        for ch in _chunks("csv_pus.zip", fn,
                          ["SERIALNO", "OCCP", "WAGP", "ADJINC", "PWGTP", "AGEP", "ESR"]):
            adj = pd.to_numeric(ch["ADJINC"], errors="coerce") / 1e6
            wage = pd.to_numeric(ch["WAGP"], errors="coerce").fillna(0.0) * adj
            esr = pd.to_numeric(ch["ESR"], errors="coerce")
            d = pd.DataFrame({
                "SERIALNO": ch["SERIALNO"].astype(str),
                "occp": pd.to_numeric(ch["OCCP"], errors="coerce"),
                "wage": wage.astype(np.float32),
                "pwgtp": pd.to_numeric(ch["PWGTP"], errors="coerce").fillna(0.0).astype(np.float32),
                "age": pd.to_numeric(ch["AGEP"], errors="coerce").astype(np.float32),
                "employed": esr.isin([1, 2, 4, 5]).to_numpy()})
            pp.append(d)
    P = pd.concat(pp, ignore_index=True)
    # household wage income and an employed-25-64 flag, from ALL persons
    hw = P.groupby("SERIALNO", sort=False).agg(
        hh_wage=("wage", "sum"),
        core=("employed", "max"))
    ages = P.loc[P["employed"], ["SERIALNO", "age"]]
    core_age = ages[(ages["age"] >= 25) & (ages["age"] <= 64)].groupby("SERIALNO").size()
    hw["working_core"] = hw.index.isin(core_age.index) & (hw["core"] > 0)

    print("  housing pass ...")
    repcols = [f"WGTP{i}" for i in range(1, NREP + 1)] if with_reps else []
    hh = []
    for fn in HPART:
        for ch in _chunks("csv_hus.zip", fn,
                          ["SERIALNO", "WGTP", "TEN", "MRGP", "GRNTP", "ADJHSG",
                           "ADJINC", "HINCP", "NP"] + repcols):
            adjh = pd.to_numeric(ch["ADJHSG"], errors="coerce") / 1e6
            adji = pd.to_numeric(ch["ADJINC"], errors="coerce") / 1e6
            ten = pd.to_numeric(ch["TEN"], errors="coerce")
            d = pd.DataFrame({
                "SERIALNO": ch["SERIALNO"].astype(str),
                "wgtp": pd.to_numeric(ch["WGTP"], errors="coerce").fillna(0.0).astype(np.float32),
                "mort": np.nan_to_num(np.where(
                    ten == 1, pd.to_numeric(ch["MRGP"], errors="coerce") * 12 * adjh, 0.0)).astype(np.float32),
                "rent": np.nan_to_num(np.where(
                    ten == 3, pd.to_numeric(ch["GRNTP"], errors="coerce") * 12 * adjh, 0.0)).astype(np.float32),
                "hincp": (pd.to_numeric(ch["HINCP"], errors="coerce").fillna(0.0) * adji).astype(np.float32),
                "np_persons": pd.to_numeric(ch["NP"], errors="coerce").fillna(0).astype(np.int16)})
            for i, c in enumerate(repcols, start=1):
                d[f"r{i}"] = pd.to_numeric(ch[c], errors="coerce").fillna(0.0).astype(np.float32)
            del ch
            hh.append(d)
    H = pd.concat(hh, ignore_index=True)
    # VACANT UNITS (NP = 0) are dropped. They carry a housing weight but no household,
    # no income and no occupant, and leaving them in inflates the household count by 9.6
    # percent (145.33m against a true occupied 131.33m) and makes every one of them look
    # like a zero-income non-working household. They have no TEN and therefore never
    # entered any obligated-household statistic, but they corrupted the counts.
    H = H[(H["wgtp"] > 0) & (H["np_persons"] > 0)].reset_index(drop=True)
    H = H.join(hw, on="SERIALNO")
    H["hh_wage"] = H["hh_wage"].fillna(0.0).astype(np.float32)
    H["working_core"] = H["working_core"].fillna(False).to_numpy(bool)
    H["nonwage"] = (H["hincp"] - H["hh_wage"]).astype(np.float32)

    # keep only workers that matter for the simulation
    P = P[(P["wage"] > 0) & P["occp"].notna() & P["employed"]].reset_index(drop=True)
    P["occp"] = P["occp"].astype(np.int32)
    # within-occupation wage percentile, person-weight weighted
    P = P.sort_values(["occp", "wage"], kind="mergesort").reset_index(drop=True)
    g = P.groupby("occp", sort=False)["pwgtp"]
    cum = g.cumsum().to_numpy(np.float64) - 0.5 * P["pwgtp"].to_numpy(np.float64)
    tot = g.transform("sum").to_numpy(np.float64)
    P["wage_pctile_in_occ"] = np.where(tot > 0, cum / tot, 0.5).astype(np.float32)
    return P, H


def link(P, H):
    """Map each worker to a row index in H. Workers in households absent from H are dropped."""
    idx = pd.Series(np.arange(len(H), dtype=np.int32), index=H["SERIALNO"].to_numpy())
    idx = idx[~idx.index.duplicated()]
    hh_idx = P["SERIALNO"].map(idx)
    keep = hh_idx.notna().to_numpy()
    return P[keep].reset_index(drop=True), hh_idx[keep].to_numpy(np.int32)


def simulate(P, H, hh_idx, p_worker, rho, omega, r_draws=R_DRAWS, seed=SEED):
    """Mean-over-draws household indicators. Returns a dict of per-household float arrays."""
    n_hh = len(H)
    wage = P["wage"].to_numpy(np.float64)
    nonwage = H["nonwage"].to_numpy(np.float64)
    mort = H["mort"].to_numpy(np.float64)
    rent = H["rent"].to_numpy(np.float64)
    oblig = mort + rent
    rng = np.random.default_rng(seed)
    acc = {f"dsti_{int(t*100)}": np.zeros(n_hh) for t in DSTI_THRESHOLDS}
    acc["wage_loss"] = np.zeros(n_hh)
    acc["neg_income"] = np.zeros(n_hh)
    per_draw = {f"dsti_{int(t*100)}": [] for t in DSTI_THRESHOLDS}
    w = H["wgtp"].to_numpy(np.float64)
    for _ in range(r_draws):
        d = rng.random(len(wage)) < p_worker
        re = rng.random(len(wage)) < rho
        kept = np.where(d, np.where(re, omega * wage, 0.0), wage)
        hh_kept = np.bincount(hh_idx, weights=kept, minlength=n_hh)
        hh_lost = np.bincount(hh_idx, weights=wage - kept, minlength=n_hh)
        inc = nonwage + hh_kept
        acc["wage_loss"] += hh_lost
        bad = inc <= 0
        acc["neg_income"] += bad
        with np.errstate(divide="ignore", invalid="ignore"):
            dsti = np.where(bad, np.inf, oblig / np.maximum(inc, 1e-9))
        for t in DSTI_THRESHOLDS:
            hit = (dsti > t) & (oblig > 0)
            acc[f"dsti_{int(t*100)}"] += hit
            per_draw[f"dsti_{int(t*100)}"].append(
                float((hit * w).sum() / w[oblig > 0].sum()))
    for k in acc:
        acc[k] /= r_draws
    acc["_sim_sd"] = {k: float(np.std(v)) for k, v in per_draw.items()}
    return acc


def weighted_stats(H, acc, mask=None):
    """Weighted headline statistics from the mean-over-draws indicators."""
    w = H["wgtp"].to_numpy(np.float64)
    if mask is not None:
        w = w * mask
    mort = H["mort"].to_numpy(np.float64)
    rent = H["rent"].to_numpy(np.float64)
    oblig = mort + rent
    has = oblig > 0
    out = {"households_weighted": float(w.sum()),
           "obligated_households_weighted": float(w[has].sum()),
           "wage_loss_dollars": float((acc["wage_loss"] * w).sum()),
           "neg_income_share": float((acc["neg_income"] * w).sum() / w.sum()) if w.sum() else np.nan}
    for t in DSTI_THRESHOLDS:
        k = f"dsti_{int(t*100)}"
        i = acc[k]
        den = w[has].sum()
        out[f"share_{k}"] = float((i * w)[has].sum() / den) if den else np.nan
        out[f"mortgage_dollars_{k}"] = float((i * w * mort).sum())
        out[f"rent_dollars_{k}"] = float((i * w * rent).sum())
    return out


def replicate_interval(H, acc, stat_fn):
    """ACS successive-difference variance, V = (4/80) sum (theta_k - theta)^2."""
    theta = stat_fn(H["wgtp"].to_numpy(np.float64))
    reps = []
    for i in range(1, NREP + 1):
        reps.append(stat_fn(H[f"r{i}"].to_numpy(np.float64)))
    reps = np.asarray(reps, float)
    v = (4.0 / NREP) * np.nansum((reps - theta) ** 2)
    se = float(np.sqrt(v))
    return theta, se, theta - 1.96 * se, theta + 1.96 * se
