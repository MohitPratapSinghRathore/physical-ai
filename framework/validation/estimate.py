"""
SESSION2_PLAN steps 9-15. The confirmatory estimation.

Order is fixed by the run instruction:
  1. plausibility bounds and violations, reported first
  2. realised intra-cluster correlation and design effect, and the power branch,
     BEFORE any coefficient is reported
  3. the Gap-form confirmatory test
  4. the business-loan contrast
  5. the structural calibration test
  6. robustness and shift-share diagnostics
  7. secondaries with Romano-Wolf

No specification searching. Every model here is the one written in the
pre-registration.
"""
from pathlib import Path
import io
import json
import zipfile
import numpy as np
import numpy.linalg as la
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "validation"
OUT = ROOT / "framework" / "validation"

WINDOW = [(y, q) for y in (2015, 2016, 2017) for q in (1, 2, 3, 4)]
CONTROLS = ["sh_resre", "sh_consumer", "sh_cre", "sh_constr", "sh_ci",
            "sh_ag", "sh_sec", "tier1_lev", "cre_conc", "log_assets",
            "dep_assets", "brokered", "loans_assets", "unemp_2013",
            "pi_per_cap_2013", "hpi_growth_11_13", "dti_rank_2013"]
WINSOR = (0.01, 0.99)
ENGINE = {  # pinned, PREREGISTRATION 13.4
    "mortgage": {"u": 0.0830386, "lo": 0.25, "hi": 0.40},
    "card":     {"u": 0.0813974, "lo": 0.80, "hi": 1.00},
    "auto":     {"u": 0.0822220, "lo": 0.45, "hi": 0.65},
    "student":  {"u": 0.0800902, "lo": 0.75, "hi": 1.00},
}
ITEM_ENGINE = {"LNRERES": ("home_mortgage", "mortgage"),
               "LNREMULT": ("multifamily_mortgage", "mortgage"),
               "LNCRCD": ("credit_card", "card"),
               "LNAUTO": ("auto_loan", "auto"),
               "LNCONOTH": ("other_consumer", "student")}


# ---------------------------------------------------------------- utilities
def ols(y, X):
    b, *_ = la.lstsq(X, y, rcond=None)
    e = y - X @ b
    return b, e


def cluster_vcov(X, e, groups):
    XtX_inv = la.pinv(X.T @ X)
    meat = np.zeros((X.shape[1], X.shape[1]))
    for g in np.unique(groups):
        m = groups == g
        s = X[m].T @ e[m]
        meat += np.outer(s, s)
    G = len(np.unique(groups))
    n, k = X.shape
    c = (G / (G - 1)) * ((n - 1) / (n - k))
    return c * XtX_inv @ meat @ XtX_inv


def hc_vcov(X, e):
    XtX_inv = la.pinv(X.T @ X)
    meat = (X * (e ** 2)[:, None]).T @ X
    return XtX_inv @ meat @ XtX_inv


def akm_vcov(X, e, S):
    """Adao-Kolesar-Morales exposure-robust variance.
    S is the n x K matrix of bank exposure shares to the K shocks."""
    XtX_inv = la.pinv(X.T @ X)
    meat = np.zeros((X.shape[1], X.shape[1]))
    for k in range(S.shape[1]):
        w = S[:, k]
        s = X.T @ (w * e)
        meat += np.outer(s, s)
    return XtX_inv @ meat @ XtX_inv


def tsls(y, X_endog, X_exog, Z, groups=None, S=None):
    """Two-stage least squares. Returns dict with coefs and three vcovs."""
    X = np.column_stack([X_exog, X_endog])
    W = np.column_stack([X_exog, Z])
    P = W @ la.pinv(W.T @ W) @ W.T
    Xhat = P @ X
    b, *_ = la.lstsq(Xhat, y, rcond=None)
    e = y - X @ b
    res = {"beta": b, "resid": e, "n": len(y)}
    res["V_hc"] = hc_vcov(Xhat, e)
    if groups is not None:
        res["V_cl"] = cluster_vcov(Xhat, e, groups)
    if S is not None:
        res["V_akm"] = akm_vcov(Xhat, e, S)
    return res


def first_stage_F(X_endog, X_exog, Z, groups):
    """Cragg-Donald-style F for each endogenous regressor, cluster-robust."""
    Fs = []
    for j in range(X_endog.shape[1]):
        y = X_endog[:, j]
        Wf = np.column_stack([X_exog, Z])
        b, e = ols(y, Wf)
        V = cluster_vcov(Wf, e, groups)
        k0 = X_exog.shape[1]
        idx = list(range(k0, Wf.shape[1]))
        bz = b[idx]
        Vz = V[np.ix_(idx, idx)]
        Fs.append(float(bz @ la.pinv(Vz) @ bz / len(idx)))
    return Fs


def winsor(s, lo=WINSOR[0], hi=WINSOR[1]):
    a, b = s.quantile(lo), s.quantile(hi)
    return s.clip(a, b)


def r2_oos(y, yhat):
    ss_res = ((y - yhat) ** 2).sum()
    ss_tot = ((y - y.mean()) ** 2).sum()
    return 1 - ss_res / ss_tot


def icc_oneway(y, groups):
    """One-way random effects intra-cluster correlation."""
    df = pd.DataFrame({"y": y, "g": groups})
    grand = df["y"].mean()
    gm = df.groupby("g")["y"].agg(["mean", "count"])
    k = len(gm)
    n = len(df)
    msb = (gm["count"] * (gm["mean"] - grand) ** 2).sum() / (k - 1)
    within = df.merge(gm["mean"].rename("gmean"), left_on="g",
                      right_index=True)
    msw = ((within["y"] - within["gmean"]) ** 2).sum() / (n - k)
    m0 = (n - (gm["count"] ** 2).sum() / n) / (k - 1)
    icc = (msb - msw) / (msb + (m0 - 1) * msw)
    return float(icc), float(m0)
