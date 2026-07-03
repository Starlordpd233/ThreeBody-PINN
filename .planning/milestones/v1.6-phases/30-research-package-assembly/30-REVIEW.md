---
phase: 30-research-package-assembly
reviewed: 2026-06-18T00:00:00Z
depth: deep
status: issues-found
purpose: review-findings
created: 2026-06-18
milestone: v1.6
files_reviewed: 15
files_reviewed_list:
  - pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/DELIVERY-NOTE.md
  - pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_package/RESEARCH-CONTEXT-MASTER.md
  - pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_package/RESEARCH-AGENT-PROMPT.md
  - pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_package/framed-research-questions.md
  - pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_package/scope-12-hard-constraints.md
  - pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_package/resolution-doc-skeleton.md
  - pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_package/claims-register.md
  - pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_package/verified-facts-reference.md
  - pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_package/specs/consolidated-context.md
  - pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_package/specs/03-curriculum-and-training-loop.md
  - pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_package/specs/ctl_instruction.md
  - pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_package/specs/pinn_architecture.md
  - pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_package/specs/sampling_method.md
  - pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_package/specs/review_of_framework.md
  - pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_package/specs/stage_strat_revision.md
findings:
  critical: 0
  warning: 1
  info: 4
  total: 5
---

# Phase 30: Code Review Report — doc-03 Research Package

**Reviewed:** 2026-06-18
**Depth:** deep (cross-document consistency + reference-graph + provenance integrity)
**Files Reviewed:** 15
**Status:** issues-found

## Summary

This is the doc-03 ("Curriculum and Training Loop") ERW research package: 9 authored
artifacts plus 6 byte-for-byte source snapshots. I performed a deep cross-document audit:
provenance/hash integrity, reference-graph completeness (every inline `CLM-NN` and every
cited section anchor), Markdown structural integrity, the upload-hygiene zero-repo-path
rule (scoped to authored uploads), and placeholder/draft-marker leakage.

The package is in strong shape. **Verified clean:**

- **Provenance integrity (PASS).** All 6 `specs/` snapshots reproduce their recorded
  SHA-256 hashes in `30-SNAPSHOT-HASHES.txt` exactly, and `cmp` confirms each is
  byte-identical to its live repository source. The package-wide `source_baseline` pin
  (`522cea71…`) and every per-file source commit in the master manifest match the hash
  ledger. No snapshot is truncated or corrupted.
- **Reference graph (PASS).** Every inline `CLM-NN` reference in
  `framed-research-questions.md` (CLM-01, 02–07 via range, 08, 09, 10, 11, 12, 17, 19)
  resolves to a row in `claims-register.md`. Every spec section anchor cited in the
  authored questions (`ctl_instruction.md` §2.5, Step 3/4/5, Loss Function Formulation,
  Mini-Batch Construction, Adaptive Median-Based Gradient Clipping, Stage Transition
  Criteria, Multi-Stage Data Stratification; `pinn_architecture.md` §3.1/3.2/3.4/4.1/4.2/
  4.4/5.3.1) exists in the corresponding snapshot.
- **Numeric consistency (PASS).** `dt_out` (0.17/0.08/0.01/0.01), median snapshot counts
  (61/127/1003 vs issue-doc ~59/~125/~1000), the 184-gap / 2,565 / 2,749 figures, the
  stage counts, and the design-constant tables (`C_table`, `λ_E cap_table`, `MAX_EPOCHS`,
  per-stage thresholds) are stated identically across `claims-register.md`,
  `verified-facts-reference.md`, `consolidated-context.md`, and `framed-research-questions.md`.
- **The intentional `D = 6.694` vs `D ≈ 4.6416` conflict** is correctly and consistently
  surfaced as the adjudication subject (CLM-01 vs CLM-19), never as an error. Not flagged.
- **No placeholder/TODO/TBD/draft markers** in any file; **no malformed tables or
  unbalanced code fences**; **no genuine repo-path leakage** in the two strictly-swept
  authored entry points (`RESEARCH-CONTEXT-MASTER.md`, `RESEARCH-AGENT-PROMPT.md`).

One Warning and four Info items remain — all about internal-consistency precision in the
authored orientation files, none affecting the snapshots or the package's core usability.

## Critical Issues

None. Provenance is intact, no broken references, no repo-path leakage in swept uploads,
no corrupted snapshots.

## Warnings

### WR-01: Master overstates the zero-repo-path guarantee, contradicting its own companions

**File:** `research_package/RESEARCH-CONTEXT-MASTER.md:26`
**Issue:** The entry-point master states, as an absolute, "No file in this package, other
than the never-uploaded delivery note, names a repository path." This is factually false.
Three grounding companions deliberately retain repository paths as provenance labels:
`claims-register.md` (e.g., `simulation_data/Documentation/standard_quasi_random_ids_not_in_gold.md`),
`verified-facts-reference.md` (same plus `24-VERIFIED-FACTS.md`), and
`consolidated-context.md` (e.g., `pinn_instruction/issues/03-curriculum-and-training-loop.md`).
The master's blanket claim is also self-contradicted: its own manifest treatment columns
(lines 126–127, 139) acknowledge those companions "retain v1.5 provenance citations / source
labels," and its later Self-Contained Guarantee (line 160) states the *correct, narrower*
property — that no uploaded file points a repo-blind agent at a path "that would dangle."
The package's true hygiene contract (stated in `claims-register.md`'s header) scopes the
strict zero-path sweep to the master and prompt only; the companions are exempt by design.
**Why it matters:** The master is the single uploaded entry point and the first file the
external researcher reads. An absolute claim it then violates three files later erodes trust
in the orientation document and could make the researcher second-guess whether the
provenance paths are fetchable links or a packaging mistake.
**Suggested remediation (do not apply):** Scope the line-26 sentence to match the package's
actual contract and its own line-160 wording — i.e., state that the authored entry points
(this master, the prompt) name no repository path, while grounding companions retain
repo-relative provenance *labels* (non-navigable, by design), rather than asserting that no
file names a repository path at all.

## Info

### INFO-01: Two distinct `CLM-NN` namespaces coexist without an explicit reader caveat

**File:** `research_package/verified-facts-reference.md` (VF-1/VF-2/VF-3 Source lines);
`research_package/claims-register.md` (Source-citation column);
`research_package/specs/consolidated-context.md` (Fragment Source lines)
**Issue:** The package defines its own claim IDs `CLM-01..CLM-20`, but the grounding
companions also cite the (unattached) v1.5 source `24-VERIFIED-FACTS.md` using *its*
independent `CLM-NN` numbering. The two schemes collide on at least four IDs with different
meanings: package `CLM-04` = "Stage 2 trajectory count" but cited `24-VERIFIED-FACTS.md
CLM-04` grounds the 184-gap (package CLM-14); package `CLM-06` = "Stage 4 count" vs cited
`CLM-06` (hierarchical 4,857, package CLM-18); package `CLM-09` = "MAX_EPOCHS table" vs cited
`CLM-09` (per-variant `dt_out`, package CLM-17); package `CLM-10` = "`C_table`" vs cited
`CLM-10` (snapshot medians, package CLM-16).
**Why it matters:** A researcher grounding figures by CLM ID could, in principle, cross-wire
a Source-line citation with a package register row. The collision is well-mitigated in
practice — every cross-namespace citation carries the explicit `24-VERIFIED-FACTS.md`
filename prefix and the source file is not even attached — so this is a latent ambiguity, not
a likely misread.
**Suggested remediation:** Add one sentence to the claims-register provenance-label note
clarifying that `CLM-NN` numbers appearing inside `24-VERIFIED-FACTS.md` citations are that
source's own independent numbering, unrelated to this register's `CLM-NN` IDs.

### INFO-02: Two register rows (CLM-18, CLM-20) are referenced by no question or companion

**File:** `research_package/claims-register.md:58` (CLM-18); `:60` (CLM-20)
**Issue:** `claims-register.md` defines CLM-01..CLM-20, but CLM-18 ("Hierarchical Brutus
output 4,857 files", `verified`) and CLM-20 ("M16 `dt_out`-aware collocation-scaling factors",
`claimed-unverified`) appear nowhere else in the package — not in `framed-research-questions.md`,
`verified-facts-reference.md`, `consolidated-context.md`, or `resolution-doc-skeleton.md`.
The register's stated purpose is to resolve every inline `CLM-NN` reference in the questions;
these two rows are not referenced by any. CLM-20 is the more notable case: the M16 framed
question is precisely about `dt_out`-aware collocation scaling, yet it cites only CLM-17 (the
input `dt_out`), not CLM-20 (the derived scaling factors it grounds).
**Why it matters:** Orphan `verified`/`claimed-unverified` rows are harmless but add weight a
repo-blind researcher must reconcile; under-linking CLM-20 from the M16 question means a
researcher may not realize the derived scaling factors are already registered as
claimed-unverified.
**Suggested remediation:** Either cite CLM-20 from the M16 framed question (and CLM-18 from
wherever the hierarchical file count is relevant), or annotate both rows as context-only
anchors not tied to a specific question.

### INFO-03: Master's "every file is referenced by bare filename" contradicts its own manifest

**File:** `research_package/RESEARCH-CONTEXT-MASTER.md:105` vs `:133-139`
**Issue:** The master asserts (bold) "**Every file is referenced by bare filename.**" but the
`specs/` snapshot rows of the very same manifest use directory-prefixed names
(`specs/03-curriculum-and-training-loop.md`, `specs/ctl_instruction.md`, …). The companion
`RESEARCH-AGENT-PROMPT.md` attach-list, by contrast, lists those same snapshots by bare
filename, consistent with the stated convention.
**Why it matters:** Minor internal inconsistency in the orientation file. The `specs/` prefix
is a legitimate in-package location hint (not a repo path), so usability is unaffected; it
only contradicts the master's own stated bare-filename principle.
**Suggested remediation:** Either drop the `specs/` prefix in the manifest rows to honor the
bare-filename convention, or soften line 105 to note that snapshot rows carry their `specs/`
subdirectory prefix for location.

### INFO-04: Stage-5 trajectory count is absent from the stage-count set (faithful to source)

**File:** `research_package/claims-register.md:42-47` (CLM-02..CLM-07);
`research_package/specs/consolidated-context.md:57-64` (Fragment C)
**Issue:** The per-stage counts run Stage 0, 1, 2, 3, 4, then jump to Stage 6 (CLM-07,
"Unknown"); Stage 5 is not enumerated. This is consistent between the register and the
consolidated context and faithfully mirrors the non-authoritative issue-03 Stage Inventory
Summary, which omits Stage 5. It is **not** a package transcription defect.
**Why it matters:** Noted only because a repo-blind researcher may be puzzled by the missing
Stage 5 and wonder whether it is a packaging omission. The gap originates in the source.
**Suggested remediation:** Optionally add a one-line note to Fragment C / the CLM-02..07 row
notes stating that Stage 5 is not separately enumerated in the source issue doc, so the
absence is understood as faithful, not dropped.

---

_Reviewed: 2026-06-18_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: deep_
