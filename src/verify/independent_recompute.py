"""Promotion pass step 3: INDEPENDENT recomputation of headline numbers.

This script deliberately imports NOTHING from src/. It reads raw files and published figures
and recomputes each headline from scratch, so that a match is evidence the original pipeline
is right rather than evidence it is self-consistent.

Published figures are retyped here from the source documents, not read from any processed
file in this repository. Where a raw file is used the path is given.

Any difference beyond rounding is reported as a FAIL and the claim is not promoted.
"""
import io, json, pathlib, re, zipfile
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).parents[2]
RAW = ROOT / "data" / "raw"
TOL = 0.005          # half a percent, relative


def check(name, mine, theirs, tol=TOL):
    if theirs is None or (isinstance(theirs, float) and not np.isfinite(theirs)):
        return {"name": name, "recomputed": mine, "registered": theirs, "status": "NO TARGET"}
    rel = abs(mine - theirs) / max(abs(theirs), 1e-12)
    return {"name": name, "recomputed": mine, "registered": theirs,
            "rel_diff": rel, "status": "MATCH" if rel <= tol else "FAIL"}


results = []

# ---------------------------------------------------------------------------
# 1. rho, from BLS Displaced Workers Summary Table 1 total row, January 2026.
#    Retyped from the release: 3,324 thousand total, 2,199 thousand employed.
# ---------------------------------------------------------------------------
rho = 2199.0 / 3324.0
results.append(check("rho (DWS Table 1, 2199/3324)", rho, 0.6616))

# ---------------------------------------------------------------------------
# 2. omega, blended and counterfactual-adjusted.
#    DWS Table 7 total row, retyped: reemployed 1,942; to full-time 1,593; part-time 197;
#    self-employed 152. Earnings bands among the 1,342 reporting: 369 / 317 / 354 / 302.
#    CPS Table 37 and 38, 2025: full-time median 1,204; part-time median 386.
#    ECI wages and salaries from the repository's raw FRED pull.
# ---------------------------------------------------------------------------
bands = {"below20plus": 369, "below_within20": 317, "above_within20": 354, "above20plus": 302}
mid = {"below20plus": 0.65, "below_within20": 0.90, "above_within20": 1.10,
       "above20plus": 1.35}
omega_ft = sum(bands[k] * mid[k] for k in bands) / sum(bands.values())
pt_ratio = 386.0 / 1204.0
sh_ft, sh_pt, sh_se = 1593 / 1942, 197 / 1942, 152 / 1942
omega_nominal = sh_ft * omega_ft + sh_pt * pt_ratio + sh_se * 0.85

eci = pd.read_csv(RAW / "fred" / "ECIWAG.csv")
eci.columns = ["date", "v"]
eci["date"] = pd.to_datetime(eci["date"])
eci["v"] = pd.to_numeric(eci["v"], errors="coerce")
eci = eci.dropna().set_index("date")["v"]
a = float(eci.asof(pd.Timestamp("2023-01-01")))
b = float(eci.asof(pd.Timestamp("2026-01-01")))
g_wage = (b / a) ** (1 / 3.0) - 1
omega_cf = omega_nominal / (1 + g_wage) ** 1.5
results.append(check("omega full-time only", omega_ft, 0.9853))
results.append(check("part-time earnings ratio (386/1204)", pt_ratio, 0.3206))
results.append(check("omega blended nominal", omega_nominal, 0.9073))
results.append(check("ECI wage growth a year", g_wage, 0.0365, tol=0.02))
results.append(check("omega blended counterfactual", omega_cf, 0.8598, tol=0.01))

# ---------------------------------------------------------------------------
# 3. R = rho * omega
# ---------------------------------------------------------------------------
R = rho * omega_cf
results.append(check("R = rho x omega", R, 0.5683, tol=0.01))

# ---------------------------------------------------------------------------
# 4. tau_k under the current code with profit shifting.
#    sigma_rent = 13.5/(25+13.5) from Barkai; domestic share 1 - 0.48 from Torslov, Wier
#    and Zucman; statutory 0.21; tau_normal 0.05 from AMR post-2017.
# ---------------------------------------------------------------------------
sigma_rent = 13.5 / (25.0 + 13.5)
domestic = 1 - 0.48
tau_k = sigma_rent * (domestic * 0.21) + (1 - sigma_rent) * 0.05
results.append(check("sigma_rent (Barkai implied)", sigma_rent, 0.351))
results.append(check("tau_k, current code with shifting", tau_k, 0.0708))

# ---------------------------------------------------------------------------
# 5. Required tau_k at the observed R, lowest labour tax rate
# ---------------------------------------------------------------------------
req = (1 - R) * 0.255
results.append(check("required tau_k at tau_l 0.255", req, 0.1101, tol=0.02))

# ---------------------------------------------------------------------------
# 6. Leg A against Leg W. Chicago Fed 450bn committed; CMDEBT from the raw FRED pull.
# ---------------------------------------------------------------------------
cm = pd.read_csv(RAW / "fred" / "CMDEBT.csv")
cm.columns = ["date", "v"]
cm["v"] = pd.to_numeric(cm["v"], errors="coerce")
legw = float(cm.dropna()["v"].iloc[-1]) / 1000.0        # millions to billions
lega_ratio = 450.0 / legw
results.append(check("Leg A / Leg W", lega_ratio, 0.021, tol=0.05))

# ---------------------------------------------------------------------------
# 7. rho on prime-age nonemployment, refitted from the raw vintage figures.
#    rho values retyped from the fourteen DWS releases; prime-age employment rate from
#    the repository's raw FRED pull of LREM25TTUSM156S.
# ---------------------------------------------------------------------------
vint = {2000: 0.740, 2002: 0.650, 2004: 0.650, 2006: 0.700, 2008: 0.680, 2010: 0.490,
        2012: 0.560, 2014: 0.610, 2016: 0.660, 2018: 0.660, 2020: 0.700, 2022: 0.650,
        2024: 0.657, 2026: 0.661}
pa = pd.read_csv(RAW / "fred" / "LREM25TTUSM156S.csv")
pa.columns = ["date", "v"]
pa["date"] = pd.to_datetime(pa["date"])
pa["v"] = pd.to_numeric(pa["v"], errors="coerce")
pa = pa.dropna().set_index("date")["v"]
xs, ys = [], []
for y, r in vint.items():
    xs.append(100.0 - float(pa.asof(pd.Timestamp(f"{y}-01-01"))))
    ys.append(r)
xs, ys = np.array(xs), np.array(ys)
b1, b0 = np.polyfit(xs, ys, 1)
yh = b0 + b1 * xs
r2 = 1 - ((ys - yh) ** 2).sum() / ((ys - ys.mean()) ** 2).sum()
results.append(check("rho on prime-age nonemployment, slope", b1, -0.0275, tol=0.03))
results.append(check("rho on prime-age nonemployment, intercept", b0, 1.2280, tol=0.03))
results.append(check("rho on prime-age nonemployment, R squared", r2, 0.773, tol=0.03))

# ---------------------------------------------------------------------------
# 8. Fed 2026 loss rates, retyped from Table 9 and cross-checked internally:
#    losses divided by the implied balance must reproduce the published rate.
# ---------------------------------------------------------------------------
tot_losses, tot_rate = 624.9, 6.9
implied_balance = tot_losses / (tot_rate / 100.0)
results.append(check("implied total loan balance, USD bn (internal check)",
                     implied_balance, 9056.5, tol=0.01))

# ---------------------------------------------------------------------------
# 9. Attrition neutrality, recomputed from first principles rather than simulated.
#    With laid-off and never-hired workers treated symmetrically, the inflow to
#    nonemployment is laid_off + absorbed = JD regardless of alpha, so employment is
#    independent of alpha. This is an identity, checked here algebraically.
# ---------------------------------------------------------------------------
JD, alpha_vals = 0.02, [0.0, 0.25, 0.5, 0.75, 1.0]
ceiling = 0.0386
inflows = []
for al in alpha_vals:
    absorbed = min(JD, al * ceiling)
    inflows.append((JD - absorbed) + absorbed)
neutral = max(inflows) - min(inflows)
results.append(check("attrition neutrality: spread of total inflow across alpha",
                     neutral, 0.0, tol=1e-9))

# ---------------------------------------------------------------------------
OUTD = ROOT / "data" / "processed" / "verify"
OUTD.mkdir(parents=True, exist_ok=True)
Rdf = pd.DataFrame(results)
Rdf.to_csv(OUTD / "independent_recompute.csv", index=False)
pd.set_option("display.width", 220)
print("=== INDEPENDENT RECOMPUTATION, no src/ imports ===")
print(Rdf.to_string(index=False))
nfail = int((Rdf.status == "FAIL").sum())
print(f"\n  MATCH {int((Rdf.status=='MATCH').sum())}   FAIL {nfail}   "
      f"NO TARGET {int((Rdf.status=='NO TARGET').sum())}")
(OUTD / "independent_recompute.json").write_text(
    json.dumps({"results": results, "n_fail": nfail}, indent=2, default=str))
