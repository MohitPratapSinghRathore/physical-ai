"""SIPP household stress test: balances, buffers, runway and vehicle debt under displacement.

Companion to src/stress/acs_engine.py. ACS carries the payment side (mortgage service, gross
rent) on a very large sample; SIPP carries the balance sheet (liquid assets, vehicle debt,
unsecured debt) on a small one. Neither alone answers the question, so both are run and the
claims checklist requires any headline to clear both where both can measure it.

RUNWAY, defined twice on purpose and with no invented parameter.

    runway_shortfall  liquid and non-retirement financial assets divided by the MONTHLY
                      INCOME SHORTFALL created by the shock. This is the number of months a
                      household can hold its pre-shock spending. Undefined (infinite) when
                      the shock creates no shortfall.
    runway_housing    the same assets divided by the monthly housing payment (TRENTMORT).
                      This is the number of months the housing bill can be paid out of
                      savings with no income at all. It ignores every other outgoing and is
                      therefore an upper bound.

A consumption floor would give a third and more realistic figure, and it is deliberately not
computed, because the repository has no measured US household consumption floor and
inventing one would breach the no-invented-numbers rule. Both bounds are reported instead.

Assets counted: THVAL_BANK plus THVAL_STMF. Retirement balances (THVAL_RET) are EXCLUDED,
per the specification, because reaching them incurs penalty and is not a liquidity response
at a three to twelve month horizon.

Intervals: Fay balanced repeated replication, rho = 0.5, 240 replicates,
V = (1 / 60) sum_r (theta_r - theta)^2, on the restricted sample only.

CAVEAT on every cognitive configuration: AIOE and Eloundou GPT measure TASK OVERLAP, not
displacement and not timing.
"""
import io, json, pathlib, zipfile
import numpy as np
import pandas as pd
import importlib.util

ROOT = pathlib.Path(__file__).parents[2]
RAW, OUT = ROOT / "data" / "raw", ROOT / "data" / "processed"
SIPP = RAW / "sipp"
RHO_FAY, NREP = 0.5, 240
SEED = 20260919
R_DRAWS = 60
DSTI_THRESHOLDS = (0.30, 0.40, 0.50)
RUNWAY_MONTHS = (3, 6, 12)


def _mod(name, fn):
    s = importlib.util.spec_from_file_location(name, ROOT / "src" / fn)
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
    return m


def load():
    sb2 = _mod("sb2", "sipp_buffers_v2.py")
    ci = _mod("ci", "sipp_v2_ci.py")
    D, _ = sb2.load()
    hh = sb2.build_hh(D)
    D["hh"] = D["SSUID"].astype(str) + "_" + D["ERESIDENCEID"].astype(str)

    # person-level worker frame
    P = D[["hh", "occ", "TPEARN", "WPFINWGT", "TAGE", "employed"]].copy()
    P["wage"] = pd.to_numeric(P["TPEARN"], errors="coerce").fillna(0.0) * 12.0
    P["pwgt"] = pd.to_numeric(P["WPFINWGT"], errors="coerce").fillna(0.0)
    P = P[(P["wage"] > 0) & P["occ"].notna() & P["employed"]].reset_index(drop=True)
    P["occ"] = P["occ"].astype(int)
    P = P.sort_values(["occ", "wage"], kind="mergesort").reset_index(drop=True)
    g = P.groupby("occ", sort=False)["pwgt"]
    cum = g.cumsum().to_numpy(float) - 0.5 * P["pwgt"].to_numpy(float)
    tot = g.transform("sum").to_numpy(float)
    P["wage_pctile_in_occ"] = np.where(tot > 0, cum / tot, 0.5)

    hh["hh_wage_a"] = (pd.to_numeric(D["TPEARN"], errors="coerce").fillna(0.0)
                       .groupby(D["hh"]).sum() * 12.0).reindex(hh.index).fillna(0.0)
    hh["hh_inc_a"] = hh["hh_inc_m"].fillna(0.0) * 12.0
    hh["nonwage_a"] = hh["hh_inc_a"] - hh["hh_wage_a"]
    hh["housing_m"] = pd.to_numeric(hh["rentmort"], errors="coerce").fillna(0.0)
    hh["liquid"] = (hh["liquid_bank"].fillna(0.0) + hh["stocks_mutual"].fillna(0.0))

    # replicate weights keyed on the reference person
    ref = D[pd.to_numeric(D["ERELRPE"], errors="coerce").isin([1, 2])]
    ref = ref.sort_values("WPFINWGT").groupby("hh").tail(1).set_index("hh")
    hh["key"] = (ref["SSUID"].astype(str) + "|" + ref["PNUM"].astype(str)).reindex(hh.index)
    RW = ci.load_rep().reindex(hh["key"]).to_numpy(float)
    return P, hh, RW


def simulate(P, hh, p_worker, rho, omega, r_draws=R_DRAWS, seed=SEED):
    hh_pos = pd.Series(np.arange(len(hh)), index=hh.index)
    idx = P["hh"].map(hh_pos)
    keep = idx.notna().to_numpy()
    P2, idx = P[keep], idx[keep].to_numpy(int)
    p2 = np.asarray(p_worker)[keep]
    wage = P2["wage"].to_numpy(float)
    n = len(hh)
    nonwage = hh["nonwage_a"].to_numpy(float)
    housing_a = hh["housing_m"].to_numpy(float) * 12.0
    liquid = hh["liquid"].to_numpy(float)
    pre_inc = nonwage + np.bincount(idx, weights=wage, minlength=n)
    rng = np.random.default_rng(seed)
    acc = {f"dsti_{int(t*100)}": np.zeros(n) for t in DSTI_THRESHOLDS}
    acc.update({f"runway_short_under_{m}": np.zeros(n) for m in RUNWAY_MONTHS})
    acc.update({f"runway_house_under_{m}": np.zeros(n) for m in RUNWAY_MONTHS})
    acc["wage_loss"] = np.zeros(n)
    for _ in range(r_draws):
        d = rng.random(len(wage)) < p2
        re = rng.random(len(wage)) < rho
        kept = np.where(d, np.where(re, omega * wage, 0.0), wage)
        post = nonwage + np.bincount(idx, weights=kept, minlength=n)
        acc["wage_loss"] += pre_inc - post
        with np.errstate(divide="ignore", invalid="ignore"):
            dsti = np.where(post > 0, housing_a / np.maximum(post, 1e-9), np.inf)
        for t in DSTI_THRESHOLDS:
            acc[f"dsti_{int(t*100)}"] += (dsti > t) & (housing_a > 0)
        shortfall_m = np.maximum(pre_inc - post, 0.0) / 12.0
        with np.errstate(divide="ignore", invalid="ignore"):
            rw_s = np.where(shortfall_m > 0, liquid / np.maximum(shortfall_m, 1e-9), np.inf)
            rw_h = np.where(hh["housing_m"].to_numpy(float) > 0,
                            liquid / np.maximum(hh["housing_m"].to_numpy(float), 1e-9), np.inf)
        for m in RUNWAY_MONTHS:
            acc[f"runway_short_under_{m}"] += (rw_s < m) & (shortfall_m > 0)
            acc[f"runway_house_under_{m}"] += rw_h < m
    for k in acc:
        acc[k] /= r_draws
    return acc


def stats(hh, acc, w):
    v = hh["vehicle"].fillna(0.0).to_numpy(float)
    u = hh["unsecured_total"].fillna(0.0).to_numpy(float)
    m = hh["mortgage"].fillna(0.0).to_numpy(float)
    housing = hh["housing_m"].to_numpy(float) * 12.0
    has = housing > 0
    o = {"weighted_households": float(w.sum()),
         "wage_loss_dollars": float((acc["wage_loss"] * w).sum())}
    for t in DSTI_THRESHOLDS:
        k = f"dsti_{int(t*100)}"
        den = w[has].sum()
        o[f"share_{k}"] = float((acc[k] * w)[has].sum() / den) if den else np.nan
        o[f"housing_dollars_{k}"] = float((acc[k] * w * housing).sum())
        o[f"vehicle_balance_{k}"] = float((acc[k] * w * v).sum())
        o[f"unsecured_balance_{k}"] = float((acc[k] * w * u).sum())
        o[f"mortgage_balance_{k}"] = float((acc[k] * w * m).sum())
    for mo in RUNWAY_MONTHS:
        o[f"share_runway_short_under_{mo}"] = float(
            (acc[f"runway_short_under_{mo}"] * w).sum() / w.sum())
        o[f"share_runway_house_under_{mo}"] = float(
            (acc[f"runway_house_under_{mo}"] * w).sum() / w.sum())
    return o


def fay_interval(fn, w0, RW):
    theta = fn(w0)
    reps = np.array([fn(RW[:, i]) for i in range(RW.shape[1])], float)
    v = np.nansum((reps - theta) ** 2) / (NREP * (1 - RHO_FAY) ** 2)
    se = float(np.sqrt(v))
    return theta, se, theta - 1.96 * se, theta + 1.96 * se
