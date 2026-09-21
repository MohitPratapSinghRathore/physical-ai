# The independent computational rebuilds

Three rebuild rounds were run against the measurements in this package. Each was carried
out by a separate run with no access to the project's code, working from raw data and a
published specification, and scored against expected values fixed before the round began.

**What they establish.** That the stated inputs and the stated construction produce the
stated numbers. **What they do not establish.** That the constructions are the right ones,
or that the economic assumptions behind them hold. The rebuild of a scenario is a rebuild
of arithmetic.

**Round one** established the protocol and produced no comparable values in several
modules, because the specification it worked from left definitions unstated.

**Round two** scored 127 quantities, 79 of them against fixed expected values: 45 came
within five percent and 28 inside the stated tolerance, while 34 did not match. The
mismatches had six root causes, the largest being an undefined universe for one household
object, a class omitted because the specification described the exclusion rule in prose
without enumerating the classes, and a Treasury level the rebuild could not know was the
sum of two published series. Three of the five quantities withdrawn from the paper were
withdrawn as a direct result.

**Round three** covered the two constructions the earlier rounds had not reached, the
debt-only ratio and the assembled capital tax rate, and matched all 32 quantities, 30
within rounding and the remainder inside tolerance.

**The blind was procedural, not enforced.** The rebuild ran on the same machine, with the
file of expected values reachable at a path the specification names. It was not attached
to the request and was reported unopened until the rebuild was final. On that basis these
quantities are described as independently rebuilt under a reported blind protocol, and
never as independently verified.

## Where the material is

- Specifications: `docs/rebuilds/replication_brief.md`,
  `docs/rebuilds/replication_brief_debt_only.md`, `docs/rebuilds/replication_brief_v2.md`,
  and `docs/rebuilds/replication_brief_v2_2_addendum.md`.
- Reports and comparison tables: `docs/rebuilds/replication_report.md`,
  `docs/rebuilds/comparison.csv`, `docs/rebuilds/round2/`, `docs/rebuilds/round3/`.
- The scoreboard the paper reads: `data/release/replication_rounds.csv`.

The files of expected values are not in this package. They are the instrument the rounds
were scored against, and releasing them would make any future round unscoreable.
