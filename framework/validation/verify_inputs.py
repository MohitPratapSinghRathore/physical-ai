"""
Step 1 of the run: verify every input before any outcome is opened.

Checks the four owner-fetched files against the checksums recorded in
SESSION2_PLAN.md and the engine file against the hash pinned in
PREREGISTRATION.md 13.4, then records a full manifest of every input.

Exits non-zero if any pinned check fails.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "validation"
OUT = ROOT / "framework" / "validation"

PINNED_OWNER = {
    "laus/la.data.64.County":
        "7e5a532fa79e41b2e7a4dd8db3bb231ce19b18ee969defb2510873f8f01c9858",
    "laus/la.series":
        "2b11e414cd4fba4e70b6e80280e88d274a78b8c91543b665ff0d658a97db77a4",
    "laus/la.area":
        "7f1dcbd6a2506d92d65641609cf08bd04f0a534503c6d0f23497f284dce1fc45",
    "fhfa/hpi_at_county.xlsx":
        "534e9fd3224c4d9365300cc1be471bcfe4455b72311263a35e9cb50adf79afd1",
}
PINNED_ENGINE_SHA = \
    "a70b6ca41a4bb57dde30393428e41f27cb340c9316f7e614ce4a37c09ef37726"
PINNED_ENGINE_BLOB = "233e413becfec072b4a5f4cc6357f9f6e7499f79"

OTHER_INPUTS = [
    "fdic_financials_20140630.csv", "fdic_sod_2014.csv", "CAINC4.zip",
    "CAINC5N.zip", "qcew_2013_annual.zip", "efa/household-debt.zip",
    "pums2013/csv_hus.zip", "pums2013/csv_pus.zip",
    "crosswalk/2010_tract_to_2010_puma.txt",
    "crosswalk/Gaz_tracts_national.zip",
]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def git(*args):
    return subprocess.run(["git", "-C", str(ROOT), *args],
                          capture_output=True, text=True).stdout.strip()


def main():
    failures, manifest = [], {}

    print("OWNER-FETCHED FILES, against SESSION2_PLAN section 1")
    for rel, want in PINNED_OWNER.items():
        p = RAW / rel
        if not p.exists():
            failures.append(f"MISSING {rel}")
            print(f"  MISSING   {rel}")
            continue
        got = sha256(p)
        ok = got == want
        manifest[rel] = {"sha256": got, "bytes": p.stat().st_size,
                         "pinned": True, "match": ok}
        print(f"  {'OK      ' if ok else 'MISMATCH'}  {rel}  {got[:12]}…")
        if not ok:
            failures.append(f"CHECKSUM MISMATCH {rel}: want {want} got {got}")

    print("\nENGINE FILE, against PREREGISTRATION 13.4")
    eng = subprocess.run(
        ["git", "-C", str(ROOT), "show",
         "origin/master:data/processed/verify/hand_check_credit.csv"],
        capture_output=True)
    eng_sha = hashlib.sha256(eng.stdout).hexdigest()
    eng_blob = git("rev-parse",
                   "origin/master:data/processed/verify/hand_check_credit.csv")
    sha_ok = eng_sha == PINNED_ENGINE_SHA
    blob_ok = eng_blob == PINNED_ENGINE_BLOB
    manifest["ENGINE hand_check_credit.csv"] = {
        "sha256": eng_sha, "blob": eng_blob,
        "pinned": True, "match": sha_ok and blob_ok,
        "master_head": git("rev-parse", "--short", "origin/master")}
    print(f"  sha256 {'OK' if sha_ok else 'MISMATCH'}  {eng_sha}")
    print(f"  blob   {'OK' if blob_ok else 'MISMATCH'}  {eng_blob}")
    if not (sha_ok and blob_ok):
        failures.append("ENGINE FILE CHANGED since the pinned hash")

    print("\nOTHER INPUTS (recorded, not pinned)")
    for rel in OTHER_INPUTS:
        p = RAW / rel
        if not p.exists():
            failures.append(f"MISSING {rel}")
            print(f"  MISSING   {rel}")
            continue
        got = sha256(p)
        manifest[rel] = {"sha256": got, "bytes": p.stat().st_size,
                         "pinned": False, "match": None}
        print(f"  recorded  {rel:44s} {got[:12]}…  "
              f"{p.stat().st_size/1048576:8.1f} MB")

    print("\nREPO STATE")
    for k, v in [("HEAD", git("rev-parse", "HEAD")),
                 ("origin/master", git("rev-parse", "origin/master")),
                 ("PREREGISTRATION.md sha256",
                  sha256(OUT / "PREREGISTRATION.md")),
                 ("SESSION2_PLAN.md sha256", sha256(OUT / "SESSION2_PLAN.md")),
                 ("working tree clean",
                  str(git("status", "--porcelain") == ""))]:
        manifest[k] = v
        print(f"  {k}: {v}")

    (OUT / "input_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8")

    print()
    if failures:
        print("VERIFICATION FAILED")
        for f in failures:
            print(f"  {f}")
        sys.exit(1)
    print("VERIFICATION PASSED. Outcomes may be opened.")


if __name__ == "__main__":
    main()
