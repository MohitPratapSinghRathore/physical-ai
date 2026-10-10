# Novelty check: result

**2026-09-21. Criterion in `NOVELTY_CRITERION.md`, fixed before searching.**

## Verdict

**Two narrowing conditions triggered. Under the pre-stated decision rule, that is "close to a
kill: the residual contribution is probably too thin for five sessions."**

**Recommendation: do not write the paper as scoped.**

---

## What was found

### NARROW-1 triggered — the US measurement exists, and is routine

**Acharya (2011), "Governments as Shadow Banks: The Looming Threat to Financial Stability",
Federal Reserve conference on Regulation of Systemic Risk.** Verified by fetch. Quantifies
the GSE footprint directly: Fannie and Freddie held "$1.43 trillion mortgage portfolio and
$3.50 trillion in mortgage-backed security guarantees", a combined **41.3 percent** of
residential mortgages at the crisis, rising to about **45 percent** by 2009.

**Urban Institute, *Housing Finance at a Glance*.** A monthly chartbook, running since 2013,
with 80-plus figures tracking the agency and GSE share of origination and of securitised
first liens. The GSE share of first-lien origination was 34.5 percent in 2025 Q2.

The US government's footprint in mortgage credit is not merely measured — it is **published
monthly**.

### NARROW-3 triggered — the link to capital regulation is already made

This is the more damaging one, and it lands on **option 1**, not only on the scoped paper.

Acharya (2011) explicitly connects government mortgage guarantees to the capital framework:
Basel rules accorded a **"20 percent Basel risk-weight on AAA-rated residential
mortgage-backed securities"**, which he characterises as "artificial leverage advantages for
housing assets — a deliberate regulatory subsidy mechanism favouring government-preferred
lending".

That is the guarantee-to-risk-weight argument, made in 2011, by name, with the weight quoted.
**Option 1 must be narrowed accordingly** — see the amendment below.

### NARROW-2 **not** triggered — the quantitative cross-country comparison is genuinely absent

- **OECD Economics Department WP 1693, "Mortgage finance across OECD countries" (2021).**
  Fetched. Describes policy instruments and market structures qualitatively. **No systematic
  cross-country table of the government-guaranteed share of the mortgage stock.**
- **Acharya (2011)** mentions Spain's *cajas*, Germany's *Landesbanken* and Asian state banks,
  but with "no specific figures comparing cross-national government credit exposure".
- **Bank of Canada WP 15-16, "Exploring Differences in Household Debt Across Euro Area
  Countries and the United States".** Fetched. Examines **only the debtor side** — prevalence,
  amounts, burden from HFCS and SCF — and "does not address who holds or guarantees that debt
  from the creditor perspective".

So the one thing genuinely not done is the quantitative **holder-side** comparison across
economies. That is a table, not a paper.

### Searches that returned nothing

No source was found expressing the government footprint as a share of **household claims in
total** (rather than of the mortgage market), or as a share of a **wage-backed** claim stock.
Recorded as an absence, which is weak evidence, not as established novelty.

---

## What survives, honestly

| Element | Status |
|---|---|
| US agency/GSE guarantee scale | **done, monthly** (Urban Institute; Acharya) |
| Guarantee → capital risk weight link | **done in 2011** (Acharya, explicitly) |
| Cross-country *qualitative* housing finance comparison | **done** (OECD) |
| Cross-country *quantitative* holder-side comparison | **not done** |
| Expressing the footprint on the **wage-backed** claim stock | **not done** |

Two items survive, and both are exhibits rather than papers.

---

## Amendment to option 1

`framework/regulatory_gap/RESULTS.md` says the sovereign-bank nexus literature holds the
concentration argument and claims novelty for "the income-source dimension". **That remains
correct but was under-stated.** Acharya (2011) is closer than the euro-area nexus papers cited
there: he connects the **US government mortgage guarantee specifically** to the **20 percent
risk weight specifically**, and calls it a regulatory subsidy.

**What option 1 can still claim, after this check:** that the wage-backed share of the claim
stock — 89.4 percent at a risk weight of 20 percent or below, 92.3 percent exempt from the
single-counterparty limit — has not been computed, and that no rule has a field for the income
that services a claim. **What it can no longer claim:** that connecting government guarantees
to favourable risk weights is new. It is fifteen years old.

The arithmetic in option 1 is unaffected. Its framing paragraph is.
