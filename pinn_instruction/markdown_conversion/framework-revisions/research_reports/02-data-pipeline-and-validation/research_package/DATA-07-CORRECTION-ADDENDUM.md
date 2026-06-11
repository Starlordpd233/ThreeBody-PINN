---
title: DATA-07 Correction Addendum
package_for: issue-02
role: Phase-24 CLM-keyed correction addendum; supersedes RESEARCH-CONTEXT-MASTER.md "Correction Provenance And Verification Boundaries" section
status: active
created: 2026-06-11
supersedes: RESEARCH-CONTEXT-MASTER.md "Correction Provenance And Verification Boundaries" section
is_manifest_member: false
byte_stable_against: 605c0227
---

# DATA-07 Correction Addendum — 2026-06-11

**Scope:** CLM-keyed corrections to package-stated dataset claims, established by Phase 24
read-only probes (`probes/data0{1..6}_*.py`, run via `.venv/bin/python`). Added sibling file
only: no delivered package file modified; per-file source hashes in the master's Per-File
Manifest remain valid; this addendum is intentionally not in that manifest (D-18).

**Supersession:** This addendum **supersedes** the master's
["Correction Provenance And Verification Boundaries"](#correction-provenance-and-verification-boundaries)
section for any claim it covers, folding in the master's two 2026-06-10 erratum corrections
re-stated from Phase 24's own re-probed evidence (D-07). The master file is not edited in
place by this addendum; it is delivered as a sibling per D-18.

**Verdict vocabulary (D-08):** `confirmed` (observed matches claim) | `corrected` (observed
differs; both recorded) | `unverified` (probe could not run within grounding limits, reason
recorded — never a shortcut for "didn't get to it"). The `~` prefix on approximations is
preserved; integer-rounded MEDIAN is the authoritative D-09 statistic (D-09 lock 2026-06-11).

**Re-derivability (D-02):** every corrected/confirmed row carries the exact repo-root probe
command, the dataset path it ran against, the observed value, and the run date
(2026-06-11) — see the Phase 24 verified-facts register at
`.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-VERIFIED-FACTS.md`.

---

## Correction 1 — Gold-standard Brutus output filenames carry no `_gold_` infix

**Affects:** the file-naming narrative in the master's "Consolidated Dataset Context" section
("File Naming Conventions and Mapping" fragment). No CLM row carries this claim directly.

**Package states (the master's previous claim, as corrected 2026-06-10):** the package
originally stated that gold-standard Brutus output folders use a `_gold_` infix in filenames
(`brutus_hierarchical_gold_XXXX.txt`, `brutus_standard_gold_XXXX.txt`) and that gold-standard
status is encoded in both folder and filename. (Source: master's "Correction Provenance" §
Correction 1 — 2026-06-10 erratum.)

**Corrected disk fact:** 0/4,857 `brutus_hierarchical_gold_standard` files and 0/2,565
`brutus_standard_quasi_random_gold_standard` files contain a `_gold_` infix in their filename.
All four Brutus output folders use the base filename prefixes
(`brutus_hierarchical_XXXX.txt`, `brutus_standard_XXXX.txt`); gold-standard status is encoded
**only** by the parent folder name. The numeric-ID mapping itself is unchanged (same filename
in the base and gold folders).

**Evidence:** Phase 24 re-probe
`.venv/bin/python .planning/phases/24-empirical-dataset-verification-and-correction-addendum/probes/data0{1,3,4,5,6}_*.py`
(footer/filename/snapshot/mass-drift probes all read the four Brutus output folders by
listing contents and parsing IDs — every listing confirms 0/4,857 + 0/2,565 `_gold_` matches;
specifically: `probes/data04_footers.py` enumerates the standard-gold folder as 2,565 files
of form `brutus_standard_*.txt`, none with `_gold_`). Run date 2026-06-11. The dataset
documentation README was corrected on user sign-off in commits `d18f676` and `31b2cff`
(2026-06-10).

**Verdict:** **confirmed** — Phase 24 re-probe verifies the master's corrected disk fact
(the no-`_gold_`-infix claim). No correction; this is a fold-in of the master's existing
correction, re-derived.

---

## Correction 2 — 1,550 / 701 / 219 "partial"/"minimal" footer populations have no `Result:` footer at all

**Affects:**
- CLM register row **CLM-07** ("Standard-gold files with no `Result:` footer — 219 files").
  The **count of 219 stands**; the original "minimal footer" characterization is corrected —
  these files contain no `Result:` line and no parameter fields anywhere in the file
  (`eta`/`tol`/`Lw`/energy fields are all absent).
- The master's "Consolidated Dataset Context" §"Brutus Parameters by Variant" — the original
  statement "All Brutus output files contain a `Result:` footer", the "partial footer"
  entries for 1,550 / 701 files, and the "minimal footer" attribution of the 219 standard-gold
  files are all superseded.

**Package states (the master's previous claim, as corrected 2026-06-10):** the package
originally stated that all Brutus output files end with a `Result:` footer and that 1,550
hierarchical-base, 701 standard-base, and 219 standard-gold files have a "partial" or
"minimal" footer with parameters still parseable. (Source: master's "Correction Provenance" §
Correction 2 — 2026-06-10 erratum.)

**Corrected disk fact:** exactly 1,550 (hierarchical base), 701 (standard base), and 219
(standard gold) files end with their final snapshot block and contain **no `Result:` line and
no parameter fields anywhere in the file** (`eta`, `tol`, `Lw`, and energy fields are all
absent). tol/Lw/dt are **not** parseable from these files; the folder-level defaults must be
assumed for them. Footers that are present carry the full schema, including `eta` and `tol`.
The "different Brutus build" provenance explanation is unverifiable from the artifacts and
has been removed from the corrected source. **CLM-07 count of 219 stands; characterization
corrected.**

**Evidence:** Phase 24 re-probe
`.venv/bin/python .planning/phases/24-empirical-dataset-verification-and-correction-addendum/probes/data04_footers.py`
scanned all 15,028 files across the four Brutus output folders; per-variant no-footer counts
exactly match 1,550 / 701 / 219, agreeing with the 2025-12-24 footer audit record
(`footer_audit_20251224_170141.md`, "Missing Footer" column). Probe run 2026-06-11. The dataset
documentation README was corrected on user sign-off in commit `ae609f3` (2026-06-10).

**Verdict:** **confirmed** (CLM-07 count = 219; characterization corrected) — Phase 24
re-probe verifies the master's corrected disk fact. The CLM-07 row's `verified` status in the
master is preserved.

---

## Correction 3 — CLM-10 snapshot counts: medians depart from `~59 / ~125 / ~1000` at integer-rounded level

**Affects:** CLM register row **CLM-10** ("Snapshot counts per trajectory ~59 (standard) /
~125 (hierarchical) / ~1000 (gold)").

**Package states (the master's claim):** the issue doc states `~59` standard, `~125`
hierarchical, `~1000` gold snapshots per trajectory (issue doc lines 13, 60, 311-312). The
README explicitly warns against hard-coding snapshot counts (Snapshot Count Note, master's
"Consolidated Dataset Context" §"Snapshot count warning"). The `~` prefix signals
approximation.

**Corrected disk fact (D-09; integer-rounded MEDIAN is authoritative; lock 2026-06-11):**
- `brutus_standard_quasi_random` — **median = 61** (mode = 61, n = 2,048; min = 59, max = 61)
- `brutus_standard_quasi_random_gold_standard` — **median = 1003** (mode = 1003, n = 2,346; min = 1002, max = 1003)
- `brutus_hierarchical` — **median = 127** (mode = 127, n = 3,307; min = 126, max = 127)
- `brutus_hierarchical_gold_standard` — **median = 1003** (mode = 1003, n = 4,857; min = 1003, max = 1003)

The standard median of 61 (vs claim `~59`) and the hierarchical median of 127 (vs claim
`~125`) depart from the claim; the gold median of 1003 (vs claim `~1000`) matches at the
stated precision but is a small correction at integer-rounded level. The `~` prefix is
preserved in the addendum; the integer-rounded medians are the authoritative D-09 statistic.
No grounding source selects median vs mode as the one "central value"; per D-09 both are
recorded, and the MEDIAN is the locked authoritative statistic.

**Evidence:** Phase 24 probe
`.venv/bin/python .planning/phases/24-empirical-dataset-verification-and-correction-addendum/probes/data06_snapshots.py`
run 2026-06-11 over all four Brutus output folders. Full per-variant min/median/mode/max
distributions recorded in the verified-facts register's CLM-10 row.

**Verdict:** **corrected** — standard 59→61, hierarchical 125→127; gold 1000→1003 (also a
small correction at integer-rounded precision). The `~` prefix is preserved; the
integer-rounded medians are the authoritative D-09 statistic. No README correction is
proposed at this time — the empirical observation outranks the doc text, but the package
claim is not contradicted in the strict sense (the `~` prefix signals approximation); only
refined (D-11).

---

## DATA-05 (resolved with remediation required) — base-hierarchical mass-drift

**Affects:** DATA-05 mass-drift verdict (PIPE-07-feeding). No package-stated claim asserts
that m_IC = m_Brutus(t=0) at all 4,857 IDs, so this is not a package-claim correction. It
is a D-12 anomaly plus a resolved D-16 decision: **GAP-24-01 is
RESOLVED-WITH-INSTRUCTION** as of 2026-06-11.

**Package states:** no package-stated claim — this is a discrepancy Phase 24 detected, not
a package claim. Surfaced per D-12 (anomaly) and recorded as a STOP gap (GAP-24-01), then
resolved by user instruction on 2026-06-11.

**Observed disk fact:** 70 / 4,857 files in `brutus_hierarchical` show
m_Brutus(t=0) != m_IC at `np.allclose(rtol=1e-15)` (differences 0.1-1.0 in mass units; e.g.,
id 5: m_IC = 0.9056088426088029, m_Brutus_t0 = 1.2569378670807108, abs_diff approx 0.351 - too
large for float64 round-trip and not explainable by perturbation which does not touch
masses per `ic_generation_utils.py:417-420`). **Crucially**, the gold-hier variant for the
same 70 IDs matches the IC perfectly (0/4,857 mismatches), ruling out a generation-side error
in the IC files. Total compared: 15,028; total mismatch: 70 (all in `brutus_hierarchical`).

**Evidence:** Phase 24 probe
`.venv/bin/python .planning/phases/24-empirical-dataset-verification-and-correction-addendum/probes/data05_mass_drift.py`
run 2026-06-11 over the full population (D-15: default full population, 15,028 trajectory-IC
pairs). Per-variant mismatch counts: base-hier 70/4,857; gold-hier 0/4,857; base-std 0/2,749;
gold-std 0/2,565.

**Verdict:** **corrected / RESOLVED-WITH-INSTRUCTION** for the DATA-05 decision. User
instruction 2026-06-11: current IC files are canonical; the 70 affected base-hier outputs
(`0005`-`0059`, `0061`-`0075`) are invalid/stale artifacts requiring targeted rerun from
current ICs; they are not a `decimal.Decimal` precision problem and should not be skipped
permanently. Until rerun validation passes, the old 70 base-hier artifacts are quarantined
from training, metrics, and PIPE-07. See
`.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-GAPS.md`,
`.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-DATA05-RERUN-REMEDIATION.md`,
and `.planning/milestones/v1.5-GAPS.md`.

---

## Confirmed-Claims Summary (D-19)

The following CLM rows were verified by Phase 24's read-only probes against the on-disk
`simulation_data/` dataset (per the verified-facts register
`24-VERIFIED-FACTS.md`). Each row preserves the master's stated `verified` status (where
present); the empirical re-probe is the Phase 24 evidence. **The CLM-05 row is split per
WR-04 user decision (24-WR-DECISIONS.md, RESOLVED-WITH-INSTRUCTION 2026-06-11) into
CLM-05a (IC folder counts) and CLM-05b (Brutus output folder/file counts); CLM-05 is
preserved as a historical parent/alias in the register's traceability column — no
renumbering of other CLM IDs.**

| CLM ID | Verdict | Key observed value | Register row (probe / dataset path) |
| --- | --- | --- | --- |
| CLM-01 | **confirmed** | 1,250 gaps in `brutus_standard_quasi_random` (gaps[0..max]); n=2,749 | `24-VERIFIED-FACTS.md` row 14 / `probes/data01_id_gaps.py` |
| CLM-02 | **confirmed** | 143 gaps in `brutus_hierarchical` (gaps[0..max]); n=4,857 | `24-VERIFIED-FACTS.md` row 15 / `probes/data01_id_gaps.py` |
| CLM-03 | **confirmed** | 65 IDs (2 hier + 63 std) in `problematic_ics_blacklist.json` | `24-VERIFIED-FACTS.md` row 16 / `probes/data02_blacklist.py` |
| CLM-04 | **confirmed** | 184 standard IDs without gold counterpart; doc list matches set exactly | `24-VERIFIED-FACTS.md` row 17 / `probes/data03_gold_gap.py` |
| **CLM-05a** | **confirmed** | IC folder counts: `ic_standard_quasi_random` = 2,749 | `24-VERIFIED-FACTS.md` row 18 / `probes/data03_gold_gap.py` |
| **CLM-05b** | **confirmed** | Brutus output counts: base = 2,749, gold = 2,565, base−gold = 184 | `24-VERIFIED-FACTS.md` row 18 / `probes/data03_gold_gap.py` |
| CLM-06 | **confirmed** | 4,857 files in `brutus_hierarchical` (max_id=4,999) | `24-VERIFIED-FACTS.md` row 19 / `probes/data01_id_gaps.py` |
| CLM-07 | **confirmed** (count 219; D-07 characterization corrected — no footer at all) | 219 standard-gold files with no `Result:` footer AND no parameter fields | `24-VERIFIED-FACTS.md` row 20 / `probes/data04_footers.py` |
| CLM-08 | **confirmed** | 592 `tol=1e-14` standard-gold files; 2,346 `tol=1e-13` standard-gold | `24-VERIFIED-FACTS.md` row 21 / `probes/data04_footers.py` |
| CLM-09 | **confirmed** | Folder-default `tol`/`dt_out` per variant match observed modal values | `24-VERIFIED-FACTS.md` row 22 / `probes/data04_footers.py` |
| CLM-11 | **confirmed** (prevalence 100% across the probe-applicable population) | `final_timestep >= 9.5` prevalence: 1.000 across probe-applicable files | `24-VERIFIED-FACTS.md` row 24 / `probes/data06_snapshots.py` |
| CLM-12 | **confirmed** | Standard observed max_id=3,998 (→~4,000); hierarchical max_id=4,999 (→~5,000) | `24-VERIFIED-FACTS.md` row 25 / `probes/data01_id_gaps.py` |
| **CLM-10** | **corrected** (see Correction 3 above) | medians: 61 / 127 / 1003 (standard / hier / gold) | `24-VERIFIED-FACTS.md` row 23 / `probes/data06_snapshots.py` |
| **DATA-05** | **corrected / RESOLVED-WITH-INSTRUCTION** (see Correction 4 above) | 70/4,857 base-hier mismatches; current ICs canonical; affected old base outputs quarantined pending rerun | `24-VERIFIED-FACTS.md` row 31 / `probes/data05_mass_drift.py` / `24-DATA05-RERUN-REMEDIATION.md` |

### PENDING — CLM-13 (D-05; not probed, routed)

| CLM ID | Verdict | Status | Routing |
| --- | --- | --- | --- |
| CLM-13 | **PENDING — not probed, not corrected, not confirmed** | `D = 6.694` convention conflict; not a dataset count | Phase 25 (EVID-10) / Phase 27 (PIPE-09) per D-05 |

### PENDING — M11 (DATA-02 consumption; not a CLM row)

The CLM-03 count (65 IDs) is **confirmed**. The M11 finding (blacklist not loaded at
training time) is **`unverified — outside grounding limits (SCOPE-10)`**; deferred to Phase 25
adjudication and the FUT-01 handoff. D-10 boundary explicitly excludes `pinn/` from v1.5
grounding. Recorded in `24-VERIFIED-FACTS.md` "DATA-02 Nuanced Consumption Map" — no
addendum correction entry.

---

## Non-CLM Appendix — WR-01 / WR-02 / WR-03 (D-11, D-18)

The four 2026-06-10 Phase 23 review warnings routed to Phase 24 DATA-07 are folded here via
the user-chosen non-CLM channel (24-WR-DECISIONS.md, all four `RESOLVED-WITH-INSTRUCTION`
2026-06-11). The delivered `RESEARCH-CONTEXT-MASTER.md` is not edited in place — the
addendum is the correction channel (D-18, D-11).

### WR-01 — sample-size conflict (1000 vs 100)

**Affects:** `framed-research-questions.md` Q-B2 (master's "Framed Research Questions" Q-B2,
reporting the issue doc's footer/mass-drift protocol). The issue doc is internally
inconsistent: protocol prose at line 202 says "parse 1000 IC-Brutus pairs", while P2-2 at
line 292 says "Batch-verify 100 IC-Brutus mass pairs".

**Channel:** per user decision 2026-06-11, WR-01 is **surfaced neutrally** in the master's
Q-B2 (already integrated 2026-06-11). No new CLM row was created — CLM is scoped to dataset
claims, and the 1000-vs-100 is a methodology/sample-size disagreement internal to the
issue document, not a dataset observation figure.

**Researchers should note:** the 1000-vs-100 sample-size conflict remains an open
issue-doc-internal conflict. Treat both figures as candidates; do not assume either is
correct without checking the user's resolution doc when it lands.

### WR-02 — Hard-Constraint 3 citation 972→967

**Affects:** `framed-research-questions.md` "Hard Constraints" (master's "Framed Research
Questions" §"Hard Constraints — Locked v1.4 Conventions (verbatim)", constraint 3, citing
`specs/pinn_architecture.md` §10.2 "COM Invariance" acceptance check at line 972).

**Corrected citation:** the section heading is at **line 967** (verified against the
`specs/pinn_architecture.md` snapshot at master commit `605c0227`); the section spans
**lines 967-971**. The Hard Constraint 3 text now carries the corrected line citation
(consolidated 2026-06-11; see master's "Citation Corrections Applied At Consolidation"
2026-06-11).

**Researchers should note:** cite the §10.2 "COM Invariance" section at lines 967-971 of
`specs/pinn_architecture.md` (not 972).

### WR-03 — Q-B1 framework-spec citation §5.3.2 → Step 5 "Mini-Batch Construction" line ~1201

**Affects:** `framed-research-questions.md` Q-B1 (master's "Framed Research Questions"
Q-B1) framework-spec position — the issue doc's stale "§5.3.2" numbering does not exist in
the spec snapshot.

**Corrected citation:** the actual section in `specs/ctl_instruction.md` is
**"Mini-Batch Construction with Lookahead Sampling" (line 1197)** (verified against the
snapshot). The "(e.g., 32)" at line ~1201 is **an example, not a hard 32-point contract**
— the 32-pt number is the issue doc's read, not a spec invariant. Researchers should not
treat 32 as a fixed contract; the spec is silent on a hard 32-pt cap and the adjudicated
points-per-trajectory contract is PIPE-04 (Phase 27).

**Researchers should note:** the `~1201` line-cite is an example, not a 32-pt contract.
Q-B1 above carries the corrected citation.

---

## Not affected — do not over-discount (D-19)

Re-verified correct by Phase 24's probes (no contradiction, no correction needed):

- **CLM-09** — the folder-default `tol` / `dt_out` values per variant (std tol=1e-13 dt_out=0.17;
  hier base tol=1e-15 dt_out=0.08; both gold tol=1e-13 dt_out=0.01). Observed modal values
  match the claim. (Confirmed-row table above.)
- **The file counts behind CLM-05a / CLM-05b and CLM-06** (2,749 ICs, 2,749 base outputs, 2,565
  gold outputs; 4,857 hierarchical outputs).
- **The CLM-07 count of 219 standard-gold no-footer files** (the count stands; only the
  characterization was corrected by the master's 2026-06-10 erratum, folded as Correction 2
  above).
- **The CLM-08 count of 592 `tol=1e-14` standard-gold files.**
- **All full-schema footer parameter tuples** listed in the master's "Consolidated Dataset
  Context" — re-derived exactly as stated for every present-footer file across all four
  variants.

No other package content is touched by these corrections.

---

## Closing Statement

Phase 24 verified 11 of 13 CLM rows via the on-disk dataset; CLM-10 was corrected
(snapshot-count medians: 61 / 127 / 1003); CLM-13 is PENDING (contested convention, not a
dataset count; routed Phase 25 EVID-10 / Phase 27 PIPE-09 per D-05); **DATA-05 is resolved
with remediation required** (current ICs canonical; 70 old base-hier outputs quarantined
pending targeted rerun). Two 2026-06-10 erratum corrections are
folded (no-`_gold_`-infix filenames; 1,550 / 701 / 219 no-footer populations — counts
unchanged, characterizations corrected per D-07). WR-01 / WR-02 / WR-03 are folded in the
non-CLM appendix per the user-chosen channel (24-WR-DECISIONS.md). The DATA-05 decision is
no longer open; the data-remediation boundary is recorded in `24-GAPS.md`,
`24-DATA05-RERUN-REMEDIATION.md`, and `.planning/milestones/v1.5-GAPS.md`.

The addendum does **not** claim that "all package-stated claims are confirmed" because
CLM-10 is corrected, CLM-13 is pending, and DATA-05 still requires data remediation before
training/PIPE-07 use. The master file `RESEARCH-CONTEXT-MASTER.md` is unchanged (D-18);
this addendum is a sibling file and is intentionally not in the master's Per-File Manifest.

---

## Addendum Provenance

- **Authored by:** Phase 24 plan 24-03 (Wave 3), 2026-06-11.
- **Source of every corrected/confirmed row:** the Phase 24 verified-facts register
  `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-VERIFIED-FACTS.md`
  (the dataset-evidence annex of the issue ledger).
- **Source of every WR channel decision:** the user decision record
  `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-WR-DECISIONS.md`
  (all four `RESOLVED-WITH-INSTRUCTION` 2026-06-11).
- **Byte-stability reference:** baseline commit `605c0227`; `git diff --quiet 605c0227 -- .../RESEARCH-CONTEXT-MASTER.md .../DELIVERY-NOTE.md .../specs/` returns exit 0 (verified 2026-06-11).
- **Hand-off:** this addendum is delivered to the user (24-03 / D-21) for forwarding to the
  in-flight external research. The agent sends nothing externally itself.
