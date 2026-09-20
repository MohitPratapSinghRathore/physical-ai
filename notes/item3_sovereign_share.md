# Item 3. The sovereign share: the Treasury class identified, verified, and the share made a range

Code: `framework/labor_backing/item3_sovereign_robustness.py`. Outputs:
`item3_sovereign_robustness.csv`, `item3_sovereign_robustness.json`.

## 1. The Treasury series, stated exactly

It is not one series. It is two, summed:

| Z.1 series | description | 2025, mn |
|---|---|---|
| **FL313161105** | Federal government; total **marketable** Treasury securities; liability | 30,069,641 |
| **FL313169205** | Federal government; total **nonmarketable** Treasury securities; liability | 3,817,450 |
| | **sum** | **33,887,091 = 33,887.1bn** |

That reproduces the published level to the last digit. **Vintage: Z.1 annual, 2025**, the
latest complete year, which is also what the sealed block states and what section 14 of the
brief does not.

The replicator searched for a single series and found FL313161105 at a 2026Q2 vintage,
30,878.3bn, with no way of knowing a second series was added. The identifiers are in
`framework/labor_backing/config.py` and nowhere a replicator would look. **The level is
correct; the documentation was wrong.** This is the third instance of the replicator's
standing pattern: what is stated reproduces, what is referenced does not.

## 2. What the definition includes, which was never stated

| | |
|---|---|
| **marketable** | yes, all of it |
| **nonmarketable** | yes: savings bonds and the State and Local Government Series |
| **intragovernmental holdings** | **partly.** Z.1 consolidates the federal government sector, so the trust funds' Government Account Series holdings net out of this liability |
| **Federal Reserve holdings** | **yes, in full.** The monetary authority is a separate sector in Z.1 |

Three independent cross-checks confirm the consolidation, all from FRED at the same 2025
annual mean:

| | bn |
|---|---|
| Treasury gross federal debt, GFDEBTN | 37,144.3 |
| **our figure** | **33,887.1** |
| Treasury debt held by the public, FYGFDPUN | 29,769.5 |
| Z.1 all-sector Treasury securities asset, FL893061105 | 28,481.0 |
| Federal Reserve holdings outright, TREAST | 4,219.6 |

Our figure sits between gross federal debt and debt held by the public, which is exactly
where a consolidated measure must sit. It is not gross debt, so it does not double-count the
trust funds, and it is not held-by-the-public, so it does not drop the nonmarketable series
held outside the federal sector. **Verified and correct.**

## 3. The other_consumer class, now explicit

The replicator omitted it entirely and it is 6.6 percent of the gap.

| | |
|---|---|
| class | **other_consumer**, other non-revolving consumer credit |
| Z.1 series | **FL153166205** |
| level | 377.6bn |
| labour backing | 0.815554 |
| rule | serviced from household income; no separate survey measure exists for this residual, so it carries the balance-weighted mean of the card, auto and student working-core shares. **FLAGGED as a proxy.** |

The brief lists the zero-rule classes in prose and never enumerates the thirteen. **The
thirteen are now enumerated in the brief:** home_mortgage, credit_card, auto_loan,
student_loan, other_consumer, multifamily_mortgage, treasury, state_local_debt,
corporate_bonds, corporate_loans, noncorporate_business_debt, commercial_mortgage,
corporate_equity.

## 4. The sovereign share, with a range

Central, reproduced exactly from the published components: **0.793593**.

**Measurement uncertainty about the same object**, every named call taken one at a time:

| judgement call | sovereign union | move |
|---|---|---|
| **CENTRAL** | **0.7936** | 0 |
| Treasury: marketable only | 0.7895 | -0.52 pct |
| Treasury: all-sector asset | 0.7876 | -0.75 pct |
| Treasury: gross federal debt | 0.7967 | +0.39 pct |
| Treasury: debt held by the public | 0.7892 | -0.56 pct |
| Treasury: net of Federal Reserve holdings | 0.7890 | -0.57 pct |
| **central bank NOT federal** | **0.7936** | **exactly 0** |
| federal receipts: 77.7 percent upper bound | 0.7992 | +0.71 pct |
| home mortgage backing: SIPP balances | 0.7990 | +0.68 pct |
| home mortgage backing: superseded A38 | 0.8038 | +1.29 pct |
| rent backing: A38 definition | 0.7950 | +0.17 pct |
| state and local: all personal current taxes | 0.7877 | -0.74 pct |
| other consumer: card share alone | 0.7942 | +0.07 pct |

**No measurement call moves the sovereign share by more than 1.3 percent.** The whole
Treasury definitional question, which drove 83.7 percent of the replication gap, is worth
0.009 on the share.

**Two invariances worth reporting.**

1. **Whether the central bank counts as federal moves the share by exactly zero.** Federal
   Reserve Treasury holdings are the state holding its own debt, so they enter the held leg
   and the overlap in equal measure and cancel. That is a structural property of the union
   construction, not a coincidence, and it removes one of the objections a referee will raise
   first.
2. **The Treasury level can vary from 28,481 to 37,144bn, a 30 percent spread, and the share
   stays inside 0.788 to 0.797.** The share is a ratio within labour-backed claims and the
   Treasury class is large on both the numerator and the denominator.

**THE AGREED SOVEREIGN SHARE, with the replicator's independent rebuild:**

> **0.778 to 0.804, centred on 0.794.** Our 0.793593, the replicator's independent 0.777810,
> and every measurement variant of the same object all lie inside it. The width is 0.026.

## 5. What it is NOT robust to, stated plainly

Four structural calls change the object rather than measure it, and all four move it a lot:

| call | sovereign union | move |
|---|---|---|
| **THE ONE-STEP RULE**: business classes take the B2 indirect share instead of zero | **0.4517** | **-43.1 pct** |
| commercial mortgage treated as rent-serviced rather than zero | 0.7408 | -6.6 pct |
| agency pools NOT federal (the guarantee ignored) | 0.5865 | -26.1 pct |
| obligor leg EXCLUDED (held or guaranteed only) | 0.3215 | -59.5 pct |

**The sovereign share is a robust measurement under a stated accounting convention, and the
convention does the heavy lifting.** Both halves of that sentence must appear wherever the
share appears. The one-step rule is the same call that moves the labour backing ratio by 76
percent, and it is the single largest judgement in the whole project.

## 6. The AI leg

| AI equity scale | federal share of the AI leg |
|---|---|
| 10 percent of US nonfinancial corporate equity | 0.00952 |
| **20 percent (central)** | **0.01001** |
| 30 percent | 0.01019 |

**0.0095 to 0.0102.** The AI-leg federal share is robust to the only scenario axis it has, a
threefold variation in the assumed AI equity scale, because the federal government holds
almost none of the AI leg under any scale. The limitation is not the scale: it is that
off-balance-sheet and GPU-backed financing is unmeasured, so this is a lower bound on the AI
leg and therefore an upper bound on the federal share of it.

## 7. The holder gap, which is the paper's central object

> **The federal government is exposed, as holder, guarantor or debtor, on 0.794 of the claims
> paid directly from wages (agreed range 0.778 to 0.804), of which 0.321 as creditor or
> guarantor and 0.552 as obligor, and holds 0.010 of the claims on AI capital (range 0.0095 to
> 0.0102, an UPPER bound because that side is on-balance-sheet only). The gap is 0.784.**

**Recorded as the paper's central object.** It qualifies on three grounds: it is
independently replicated to within 0.016 by a rebuild with no code access; it is robust to
every measurement call at under 1.3 percent; and the two conventions it does depend on, the
one-step rule and the treatment of the federal guarantee, are named, quantified and travel
with it.
