# One page for the owner

**2026-09-21. Validation pilot, run session. Branch `validation-pilot`, not merged.**

## What was tested

Whether the labour backing accounts tell you anything about **risk** — specifically,
whether a bank's labour backing, measured *before* the 2014–2016 oil-price collapse,
predicted its subsequent credit losses better than the measures a supervisor already uses.

The design was pre-registered in full before any loss data was opened, across three
amendments, with numeric success and kill thresholds fixed in advance and a commitment that
a null would be reported as a null.

An earlier session had already established the hard part: because the accounts' class
coefficients are near-binary (about 0.80 on every household class, zero on every business
class), the bank-level measure is 94 percent reproducible by someone who never opens the
accounts. So the test was narrowed to the one thing only the accounts provide — the **Gap**,
the difference between the wage-dependence of a county's *debtors* and of its *population*.

## What was found

**The accounts add nothing, and the design failed its own validity check.**

- The Gap coefficient is **−0.0165**, interval [−0.0385, +0.0054], against a pre-registered
  threshold of 0.10. It includes zero and has the wrong sign.
- Adding the Gap **reduced** out-of-sample fit in the held-out oil states: −0.0122, against
  a required +0.02.
- The rival measure did worse still (−0.0330): adding it makes prediction in the oil states
  *worse than the conventional supervisory controls alone*. So the result is the **null**,
  not "local labour exposure works".
- The study was **powered** — realised minimum detectable effect 0.031, well inside the 0.10
  threshold — so this is **"no effect"**, not "we couldn't tell".
- Then the pre-registered **placebo test failed**: the same interactions are significant in
  the period *before* the shock. About 70 percent of the apparent rival effect was already
  there. The pre-registration says a significant placebo voids the primary result, so it is
  voided.

Nothing survived multiple-testing adjustment among the six secondary outcomes. Every
pre-specified robustness variation left the null unmoved. The held-out 2020 episode was
**uninformative** rather than confirmatory: its instrument is too weak to test anything
(two of three first stages below the pre-registered floor), because county wage bills
actually *rose* slightly in 2020.

The structural test of the manuscript's credit engine was inconclusive: the slope is around
0.6 with a wide interval, and the predicted-loss term has **no out-of-sample explanatory
power at all**. My own pre-registered prediction about that slope was wrong, for a reason
recorded in the results.

## What it means for the measurement paper

**It does not touch the paper's main finding.** The sovereign-concentration result — that
the federal government holds, guarantees or owes about four fifths of the labour-backed
claim stock — is a measurement of *who holds what*. It does not depend on predicting
anything, and nothing here bears on it.

**It does close off one claim.** The accounts are descriptive accounting of the claim stock.
On this evidence they are **not a risk measure**, and the paper should not imply that a
supervisor could use them to forecast who loses money when labour income falls. If any
wording in the manuscript leans that way, it should be removed or explicitly marked as an
untested conjecture with this null attached. That is the standing consequence the
pre-registration committed to in advance.

## What it means for a possible second paper

**Not this paper, not on this episode.** Three reasons, in order of weight.

1. **The design is a mining-exposure design, not a shift-share design.** Mining carries
   87.6 percent of the identifying weight. The instrument rests on one sector, so the
   second route to identification (many independent shocks) is unavailable, and the
   published critiques bite hard.
2. **The placebo failed.** Whatever this design measures, it was already measuring it
   before the shock. That has to be fixed before any result from it is publishable.
3. **The episode ran through firms, not households.** The clearest finding of the whole run
   is that the wage shock predicts *business* charge-offs about forty times more strongly
   than household ones. For testing a thesis about labour income backing *household* claims,
   the 2014–2016 oil collapse turned out to be the wrong episode — even though it was chosen
   on evidence and was the best of the four candidates on the pre-shock diagnostics.

**One thing worth keeping.** Changing the primary outcome in Amendment 3 — from total
charge-offs to household-class charge-offs — demonstrably prevented a false positive. The
energy-business channel is there in the data, exactly where the pre-registration predicted,
and a total-loss outcome would very likely have picked it up and called it a wage-channel
result. That is a reusable lesson for any future attempt.

**If there is a second paper, it is a different one.** A design with genuinely multiple
independent shocks, a household-side outcome measured directly (delinquency at the borrower
level rather than charge-offs at the bank level), and an episode where household income
falls without a simultaneous sectoral collapse. 2020 is now known to be worse than "wrong
policy environment" — the wage-bill shock barely exists there, so the design cannot even be
run on it. 2007–2010 has the wrong sign on oil exposure. That episode may not exist in US
data, which is itself worth knowing before more time is spent.

## Cost of being wrong here

Low, and that is the point of having done it this way. The pre-registration was committed
before any outcome was opened, the hypothesis was stated adversarially, and the null was
pre-written. Nothing in the manuscript was changed, nothing was merged to master, and the
claims register has no new entry. The accounts are exactly what they were, with one fewer
thing that can be claimed for them.
