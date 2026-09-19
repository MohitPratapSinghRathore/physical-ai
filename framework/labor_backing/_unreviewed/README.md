# Quarantine folder. The Part B files were restored on 2026-09-19

A concurrent session quarantined the Part B files here at 23:07 on 2026-09-19, on the
premise that they were leftovers from an earlier parallel session and were built on the A70
amortisation error, the A75 loss conversion error and the saturated fiscal columns.

**That premise does not hold for these particular files, and copies of them have been
restored to the parent directory.** They were produced by the Part B definition-pass session
itself, minutes before the quarantine, and they read no fiscal magnitude at any point. The
labour backing ratio is built from three input families only:

- Z.1 Financial Accounts claim stocks and whom-to-whom holdings,
- NIPA and IRS SOI receipts composition (A8 and decision D15),
- the ACS and SIPP working-core splits (A43, A47, claim 42, plus a SIPP run made here).

None of A70, A75 or A77 enters the ratio.

The one place Part B touches the fiscal results is item B8, the re-expression of the results
already in the repository, and B8 uses **A74, A76, A77 and A78**, that is the
post-correction versions, and says so on every line.

The copies left in this folder are duplicates and are superseded by the parent-directory
versions. Nothing should read from this folder.

Owner decision needed: two sessions are writing `framework/labor_backing/` at the same time.

## Update, same day: the parallel session is actively regenerating these files

After the quarantine was applied, the same eight filenames reappeared in
`framework/labor_backing/`. A parallel session is evidently still writing there. **The copies
in this folder were NOT moved back and the live files were NOT moved again**: repeatedly
relocating another session's working files would be a destructive collision, not a fix.

What this means for the owner:

- The copies in `_unreviewed/` are a snapshot taken at quarantine time and are a record, not
  the live version.
- The live files in `framework/labor_backing/` are still unreviewed by the analysis sessions
  and are still built on fiscal inputs superseded by A72, A76, A77 and A79.
- **Two sessions are writing to the same directory.** That needs an owner decision about
  which session owns `framework/labor_backing/` before Part B is rerun.

Nothing in the analysis pipeline reads from either location.
