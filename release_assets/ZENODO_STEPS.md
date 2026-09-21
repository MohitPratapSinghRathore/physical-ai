# Archiving on Zenodo: what to do, and when

Nothing in this file has been executed. No account, token or deposit has been created.
Two routes, and a recommendation.

## Recommended: (a) now, (b) on acceptance

**(a) During review.** Keep the GitHub repository private. Build the anonymous variant and
give the referees a file, either through the journal's own system or as a Zenodo record
with access set to restricted or embargoed.

```
make anon
cd dist/anon && zip -r ../labor-backing-replication-1.0.0-anon.zip .
```

On Zenodo: New upload, drag the zip in, set **Access** to *Restricted* (share a link with
the editor) or *Embargoed* until the expected publication date, paste the description from
`.zenodo.json`, and **reserve** a DOI without publishing if the journal wants one in the
submission. Do not add author names to a restricted record that referees can see.

**(b) On acceptance, or when the working paper is posted.** Make the named repository
public, then let Zenodo mint the DOI from the tag rather than uploading by hand.

1. In the repository settings on GitHub, make it public.
2. Sign in to Zenodo with GitHub, open **GitHub** in your Zenodo account, and switch the
   repository **on**. This must happen before the release is tagged.
3. Confirm the author block in `CITATION.cff` and `.zenodo.json`, including ORCIDs.
4. Tag and push:

```
git tag -a v1.0.0 -m "Replication package 1.0.0"
git push origin v1.0.0
```

5. Zenodo creates the record and mints the DOI within a few minutes.
6. Put that DOI in three places: the paper's data availability statement, `CITATION.cff`
   (`identifiers`), and the README. Replace the `10.0000/...` placeholders.
7. Add the paper's own DOI to `.zenodo.json` under `related_identifiers` once it exists.

## The archive commands

```
make named && cd dist/named && zip -r ../labor-backing-replication-1.0.0.zip .
make anon  && cd dist/anon  && zip -r ../labor-backing-replication-1.0.0-anon.zip .
```

Or, from the release repository's own history:

```
git archive --format=zip --prefix=labor-backing-replication-1.0.0/ \
    -o labor-backing-replication-1.0.0.zip main
```

Expected archive size: about 3 MB for either variant, well inside Zenodo's 50 GB limit.

## Checklist before publishing

- [ ] Author names, order, affiliations and ORCIDs confirmed in `CITATION.cff` and
      `.zenodo.json`
- [ ] Both DOI placeholders replaced, or left as placeholders deliberately
- [ ] `make headline` passes from a fresh clone
- [ ] `make anon` passes its own identity scan
- [ ] `RELEASE_NOTES.md` still carries the private-hash mapping in the **named** variant
      only, and the anonymous variant has it stripped
- [ ] Licences read as intended: MIT for code, CC BY 4.0 for documentation, derived data
      and figures
- [ ] `THIRD_PARTY.md` reviewed, in particular the New York Fed, FHFA and BIS rows
- [ ] No raw data in the archive, and nothing over 50 MB
