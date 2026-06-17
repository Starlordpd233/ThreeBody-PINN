---
phase: 23-research-package-assembly
reviewed: 2026-06-10T09:08:00Z
depth: standard
files_reviewed: 10
files_reviewed_list:
  - pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/research_package/DELIVERY-NOTE.md
  - pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/research_package/README.md
  - pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/research_package/claims-table.md
  - pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/research_package/consolidated-context.md
  - pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/research_package/framed-research-questions.md
  - pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/research_package/specs/02-data-pipeline-and-validation.md
  - pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/research_package/specs/ctl_instruction.md
  - pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/research_package/specs/data_quality_assessment.md
  - pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/research_package/specs/pinn_architecture.md
  - pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/research_package/specs/sampling_method.md
findings:
  critical: 1
  warning: 4
  info: 4
  total: 9
status: issues_found
---

# Phase 23: Code Review Report

**Reviewed:** 2026-06-10T09:08:00Z
**Depth:** standard
**Files Reviewed:** 10
**Status:** issues_found

## Summary

Reviewed the issue-02 research package: five generated documents (manifest, delivery note,
claims table, consolidated context, framed research questions) plus five frozen spec
snapshots checked for package-level integrity only (per scope note).

**Integrity checks that PASSED** (verified empirically, not assumed):

- All five `specs/*.md` snapshots are **byte-for-byte identical** to their canonical sources
  at the manifest's package-wide pin `96f9150a` (verified via `git show | diff`).
- All five **per-file source-commit hashes** in the README manifest match each source file's
  actual last-touch commit at the pin (`d43afcd6`, `192c7c3c` ×2, `916d3f84`, `d3fcff99`).
- The README manifest enumerates **all 10 package files** (including itself); no orphan or
  missing entries.
- The **184-ID list** in `consolidated-context.md` is an exact, order-preserving transcription
  of `standard_quasi_random_ids_not_in_gold.md` (verified programmatically).
- The **blacklist summary** (2 hierarchical: 123, 253; 63 standard, first entries 21, 30, 52;
  total 65) matches `problematic_ics_blacklist.json` exactly.
- The **Brutus footer parameter-set counts** in `consolidated-context.md` (3,307/1,550;
  4,146/649/34/27/1; 1,126/922/701; 1,754/592/219) match the dataset README exactly.
- `data_quality_assessment.md` line citations (120, 130, 234, 328 / SI-DQA-003) are exact;
  the ctl `D ≈ 6.694` rejection citation (597–598), input-contract equation (1005), IC13
  raw-mass statement (1011–1019), PHYS-06 note (961), and dual-epsilon note (~703) all land
  correctly; spot-checked issue-doc citations (lines 57–60, 65–66, 68, 76–77, 133–134, 216,
  231, 258, 283–292, 297, 311–312, 326, 341–342, 357) are accurate.
- **Neutral-framing audit:** all 14 question blocks (Q-A1..Q-A6, Q-B1..Q-B4, Q-C1..Q-C4) pose
  contested findings as questions; issue-doc proposals are consistently tagged
  "(non-authoritative)"; the two KNOWN CONFLICTs (SCS gate, D convention) present both
  positions without settling; the M13 STOP-gap candidate is correctly marked "do not assert a
  fallback here". No imperative leakage found in the question blocks.

**Key defect:** the package contains one serious data error — the CLM-09 folder-default
table swaps `tol` and `dt_out` in every row, in both `claims-table.md` (where the row is
marked `verified`) and `consolidated-context.md`. Details below, plus four warnings on
citation accuracy and register precision.

## Critical Issues

### CR-01: CLM-09 folder-default `tol` and `dt_out` values are swapped in every row, yet the row is marked `verified`

**File:** `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/research_package/claims-table.md:29` and `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/research_package/consolidated-context.md:107-113`
**Issue:** The package states the folder-default parameters as:

> std: tol=0.17, dt_out=1e-13; hier base: tol=0.08, dt_out=1e-15; gold: tol=0.01, dt_out=1e-13

and `consolidated-context.md` carries the same inversion in its synthesized
"Folder-default parameters (CLM-09)" table (`| Standard quasi-random | 0.17 | 1e-13 |` etc.).
Every row has `tol` and `dt_out` exchanged. Ground truth (verified against the cited source,
`simulation_data/Documentation/README.md` lines 584–628 footer sets, e.g.
`(tol=1e-13, Lw=118, dt_out=0.17, ...)`) is: std base tol=1e-13 / dt_out=0.17; hierarchical
base tol=1e-15 / dt_out=0.08; gold tol=1e-13 / dt_out=0.01. The README contains no
folder-default table at all — this table is a Phase-23 synthesis, and the swap was
introduced by the package, not inherited from a source.

The error contradicts four other statements **inside the same package**: the footer
transcriptions four lines above the table (`(1e-13, 118, 0.17, 10.03, ...)`), the
`calculate_metrics.py` excerpt ("Standard: tolerance=1e-13, dt_out=0.17"), the issue-doc
snapshot's Dataset Inventory (line 312), and Q-A5's "folder-level default `tol=1e-13`".
CLM-09 is consumed by four research questions (Q-A5, Q-B1, Q-B2, Q-B3) as the dataset fact
for footer-fallback and precision adjudication; an external researcher who trusts the
`verified` claims-register row (the package's own rule: "No figure is presented as fact
unless its CLM row is marked `verified`") receives a physically nonsensical Brutus tolerance
of 0.17 and a `dt_out` of 1e-13. The `verified` status is also self-undermining: the row
misstates the very source it cites as verification.
**Fix:** Swap the column values back in both files:

```markdown
| CLM-09 | Folder-default tol / dt_out values | std: tol=1e-13, dt_out=0.17; hier base: tol=1e-15, dt_out=0.08; gold: tol=1e-13, dt_out=0.01 | ... |
```

```markdown
| Variant | Default tol | Default dt_out |
|---------|------------|----------------|
| Standard quasi-random | 1e-13 | 0.17 |
| Hierarchical base | 1e-15 | 0.08 |
| Gold standard (both) | 1e-13 | 0.01 |
```

If the package has already been handed off, the correction must also flow through the same
channel Phase 24 uses for DATA-07 addenda, keyed to CLM-09. (Note: per the project STOP
protocol, the reviewer does not edit package files; this fix is for the parent agent /
orchestrator to apply or surface.)

## Warnings

### WR-01: Q-B2 misstates P2-2's sample size (1000 vs 100) and misses an issue-doc-internal conflict

**File:** `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/research_package/framed-research-questions.md:304-309`
**Issue:** Q-B2 reports the issue doc as proposing "parsing ~1000 IC–Brutus pairs" and cites
"issue doc lines 196–207, P2-2 line 292". The issue doc is internally inconsistent: line 204
says "parse 1000 IC-Brutus pairs" while P2-2 (line 292) says "Batch-verify **100** IC-Brutus
mass pairs". The framed question attributes the 1000 figure to both citations, including the
one that says 100, and the conflict goes unsurfaced. Surfacing exactly this kind of
figure-level disagreement is the package's stated job; an external researcher answering Q-B2
on sample-size adequacy is working from a misreported claim.
**Fix:** Report both figures neutrally, e.g.: "the issue doc proposes parsing IC–Brutus
pairs — stated as 1000 pairs at line 204 but 100 pairs in P2-2 (line 292); the two statements
conflict — comparing `m_IC` vs `m_Brutus(t=0)` with `np.allclose(rtol=1e-15)` ...". Optionally
register the sample-size figure as a CLM row so the conflict is tracked.

### WR-02: Hard Constraint 3 cites the COM Invariance acceptance check at the wrong line (972 is a different check)

**File:** `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/research_package/framed-research-questions.md:92-94`
**Issue:** Hard Constraint 3 cites "the §10.2 'COM Invariance' acceptance check (line 972)"
in `specs/pinn_architecture.md`. In the snapshot, §10.2 COM Invariance is at line 967; line
972 is the heading of §10.3 "Componentwise AD on Synthetic Trajectory". The Hard Constraints
section promises conventions "reproduced verbatim with their citation into the intact spec
snapshots"; this pointer sends a repo-blind researcher to the wrong acceptance check.
**Fix:** Change the citation to "§10.2 'COM Invariance' acceptance check (lines 967–971)".

### WR-03: Q-B1 cites a nonexistent ctl section "§5.3.2"; the actual spec text says "(e.g., 32)", weaker than the framing implies

**File:** `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/research_package/framed-research-questions.md:292-293`
**Issue:** Q-B1's framework-spec position states "`specs/ctl_instruction.md` §5.3.2 carries
the batch point-count assumption". The ctl snapshot has no numbered §5.3.2 — its structure is
"Step 5: Curriculum Stage Assignment" with "### Mini-Batch Construction with Lookahead
Sampling" (line 1197). "§5.3.2" is the issue doc's stale numbering ("CTL Sec 5.3.2", issue
doc line 60) carried over uncorrected into the column that is supposed to state the
*framework-spec* position. The citation dangles for the external researcher. Substantively,
the spec text at line 1201 reads "$n_{\text{pts}}$ (e.g., 32) time points per trajectory" —
an illustrative example, not a hard 32-point contract; this nuance materially affects how
contested the M12 "infeasibility" finding actually is and should be visible to the researcher.
**Fix:** Replace with: "`specs/ctl_instruction.md` Step 5, 'Mini-Batch Construction with
Lookahead Sampling' (line ~1201) states '$n_{pts}$ (e.g., 32) time points per trajectory' —
the 32 appears as an example value; the spec is silent on an adaptive cap."

### WR-04: CLM-05 is used for two distinct observables (IC folder counts vs Brutus output file counts)

**File:** `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/research_package/claims-table.md:25` and `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/research_package/consolidated-context.md:89,98`
**Issue:** In the claims table, CLM-05 is "Standard folder counts | 2,749 base vs 2,565 gold"
sourced from `standard_quasi_random_ids_not_in_gold.md`, which counts **IC files**. In
`consolidated-context.md`, the same CLM-05 tag is applied to the **Brutus output** file
counts (`brutus_standard_quasi_random/` 2,749 files; `..._gold_standard/` 2,565 files). The
two observables happen to coincide today (the dataset README confirms both), but they are
produced by different pipeline stages and can diverge (failed Brutus runs are one of the
documented gap causes). Phase 24's DATA-07 correction addendum is keyed by CLM ID; CLM-05's
check ("count base and gold folders independently") does not say which folders, so a
verification verdict on CLM-05 would be ambiguous about what it verified.
**Fix:** Either split into two rows (CLM-05a IC folder counts, CLM-05b Brutus output counts)
or amend the CLM-05 figure/check text to name both observables explicitly and require the
DATA-04 probe to count and report IC and Brutus folders separately.

## Info

### IN-01: CLM-06 line citation "~607" points into the wrong subsection

**File:** `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/research_package/claims-table.md:26`
**Issue:** CLM-06 cites the hierarchical ~4,857-file count to "README Brutus Parameters by
Variant (line ~607)". The count is at README line 595 (`brutus_hierarchical/` heading); line
607 is a footer row inside the *gold-standard* subsection. Also note the README states the
count exactly ("4,857 files", and 4,857 in the inventory table at line 150), so the figure is
better supported than the "~" hedge implies.
**Fix:** Cite line ~595 (and/or the inventory table, lines 148–153).

### IN-02: Delivered task list still carries `status: DRAFT` frontmatter

**File:** `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/research_package/framed-research-questions.md:3`
**Issue:** The package has been formally delivered (DELIVERY-NOTE opens the gate window;
Plan 05 committed), but the framed-questions frontmatter still says `status: DRAFT`. An
external researcher may question whether they hold the final task list.
**Fix:** Update to a delivered/final status (or document that DRAFT is intentional pending
the DATA-07 addendum).

### IN-03: Inventory Coverage Table references a repo-internal artifact not shipped in the package

**File:** `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/research_package/framed-research-questions.md:415-416`
**Issue:** The coverage table's preamble defines completeness against "`23-RESEARCH.md`
§'Issue-02 Finding Inventory'" — a `.planning/` artifact not in the package. This is mild
tension with the README's self-containment guarantee ("no in-package file points a repo-blind
agent at a project path that would dangle"). The reference is informational (the researcher
does not need it to answer questions), but unlike `consolidated-context.md`'s source paths it
is not labeled as a provenance-only reference.
**Fix:** Add a provenance-label parenthetical, e.g. "(internal planning artifact; provenance
reference only — not shipped in this package)".

### IN-04: CLM-11 status value deviates from the declared two-value status enum

**File:** `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/research_package/claims-table.md:31`
**Issue:** The table header defines exactly two statuses (`claimed-unverified` / `verified`),
but CLM-11's Status cell reads `` `claimed-unverified` (prevalence) `` — a hybrid value
encoding that the rule is grounded while the prevalence is not. Any tooling or Phase-24
consumer that parses the Status column against the declared enum will mismatch on this row.
**Fix:** Set Status to plain `claimed-unverified` and keep the rule-vs-prevalence split in
the Figure column / Row Notes (where it is already explained).

---

_Reviewed: 2026-06-10T09:08:00Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
