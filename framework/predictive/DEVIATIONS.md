# Deviations — broad predictive test

**Against `PREREGISTRATION.md`, SHA256
`b9f09ddc33a6619b0046617021df72f13aaeb0fcb4fb882852269dd424f3136a`, committed at `bb21c84`
before any outcome was downloaded.**

---

## D1. `LB` and `Rival` are the same construct

**Before any outcome was read.**

The pre-registration lists four constructs: `LB`, `Rival`, `Gap`, `LB payment-weighted`.

**`LB` and `Rival` are identical by construction.** Both are the composition leg times the
**population** wage share:

    LB_bank = [Σ_c w_c · β_c] · ω^pop
    Rival   = (Σ_c w_c · β_c) · ω^pop

That was the pilot's point — the accounts' bank-level measure *is* reproducible by the rival,
because it uses the population wage share. Listing them as two constructs would have counted
the same specification twice and inflated the curve.

**Substituted:** `LB`, `LB_debtor`, `Gap`, `LB_debtor_pw` (payment-weighted). Four constructs,
864 specifications, as pre-registered.

## D2. Debtor-specific wage shares are held constant across origin years

**Before any outcome was read.**

The debtor-specific county wage shares exist only for the ACS 2009–2013 vintage. They are
**held constant across all origin years 2001–2021**, exactly as the accounts hold the class
coefficients β constant across their own time series.

Population wage shares **do** vary by year, from BEA CAINC4.

**Consequence:** `Gap` varies across years only through loan composition and the population
wage share, not through changes in debtor composition. Any `Gap` result is conditional on
that, and it biases toward finding nothing rather than toward finding something.

## D3. Outcomes are calendar-year YTD charge-offs from December filings

**Before any outcome was read.**

The pilot needed the §14.4 year-to-date differencing rule because it used quarterly windows.
This test uses **December 31 YTD values, which are the calendar-year flow by construction**, so
no differencing is required and the trap is avoided rather than handled.

Cumulative outcomes over *t+1*..*t+3* are sums of three such annual figures.

## D4. The failure indicator is crude

**Before any outcome was read.**

`failed` is set where a bank has no December filing three years after the origin year. That
**conflates failure, acquisition, merger and any filing gap**. It appears only in the
specification curve, never in the confirmatory test, and no specification from the curve may
be reported as a finding in any case.

---

*Further deviations, if any, are appended after results are seen and marked as such.*

---

## Deviations recorded AFTER results were seen

These four are **implementation corrections, not design changes**. None alters a
threshold, an outcome definition, a construct or a decision rule in the
pre-registration. Each is recorded with what it was, why it was wrong, and what it
did to the result.

## D5. A minimum household and business book of $1m

**After the first run.** The first run reported mean ΔR² of **+958.01** for `LB` and
**+1146.93** for `Gap`, with 12/13 years positive, and printed "SUCCESS".

ΔR² cannot exceed 1. The run was not reported; it was diagnosed.

**Cause:** one observation. Bank CERT 27389, origin year 2017, had a household book of
**$4 thousand**, so `lag_nco` = charge-offs / book = **19,645**. In test year 2017 that
single row drove `r2_controls` to **−6,942,676.8** and the year's ΔR² to **+12,454.1**.
One year out of thirteen produced the entire "+958". 3,119 panel rows had a household
book under $1m.

**Correction:** require `hh_book >= 1000` and `bus_book >= 1000` ($1m in $000s), which is
the denominator rule the pilot's §14.1 already imposed for the same reason. 154,904 →
146,813 rows, 10,842 → 10,532 banks.

## D6. Controls winsorised at 1/99, as outcomes already were

**After the first run.** The pre-registration winsorised outcomes but not controls. A
control with an extreme value destroys an out-of-sample R² without carrying information.
Controls and the lagged term are now clipped at 1/99. Applied to the pooled panel, which
is a mild look-ahead; it affects the baseline and the LB model identically and so cannot
create a ΔR².

## D7. Two-way clustering by bank and origin year, replacing clustering by year

**After the first run.** The first run clustered on `origin_year`: **21 groups** for a
panel of 146,813 observations, 10,532 banks, about 14 observations per bank, with
**overlapping** *t+1*..*t+3* outcome windows.

Both one-way choices are wrong in opposite directions. Year alone ignores within-bank
serial correlation across overlapping windows. Bank alone ignores the common credit-cycle
shock, which every bank in the country shares — and in this panel that is the larger of
the two, which is why switching to bank clustering made the standard errors *smaller* and
the apparent significance *greater*.

**Correction:** Cameron–Gelbach–Miller two-way, V_bank + V_year − V_bank×year, falling
back to bank-only where the two-way meat loses positive definiteness.

No specification-curve count was reported under the year-clustered or bank-clustered
standard errors.

## D8. The confirmatory test is reported twice: raw and re-centred

**After the first run, and this is the finding.**

The corrected confirmatory test gives `LB` mean ΔR² **+0.00556**, 12/13 years positive —
above the kill line of 0.002 and below the success line of 0.01. Smooth and monotone
across years, robust to dropping the best year (+0.00462) and to dropping the best and
worst (+0.00508). Not an outlier.

But `r2_controls` is **negative in 10 of the 13 test years** (−0.11 to −0.41). The
baseline predicts worse than the test-year mean, because coefficients fitted on years
≤ T do not transfer to T+1 across the credit cycle. A gain measured against a baseline
worse than a constant can be a level correction rather than information about which
bank loses money.

**Two additional diagnostics, not pre-registered, reported because the pre-registered
statistic is uninterpretable without them:**

1. **Re-centred ΔR²** — both predictions shifted to the test-year mean, removing level
   drift and leaving only cross-sectional ranking. Mean ΔR² **−0.00043**, 6/13 positive.
2. **Out-of-sample Spearman rank correlation** between prediction and realised
   charge-off rate. Controls alone **+0.1620**; adding `LB` **+0.1558**. Adding LB makes
   the ranking worse in **13 of 13 years**, 0/13 positive.

The pre-registered +0.00556 was the construct absorbing the drift of a mis-calibrated
baseline. On the question the test was built to answer — which banks lose money — the
construct subtracts.
