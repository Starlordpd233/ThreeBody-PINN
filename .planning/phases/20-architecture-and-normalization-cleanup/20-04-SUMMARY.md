---
phase: 20
plan: "04"
subsystem: "Architecture and Normalization Cleanup"
tags:
  - ARCH-05
  - energy-normalization
  - mass-normalization
  - realized-support
  - evidence-gated
dependency_graph:
  requires:
    - "20-02"
    - "20-03"
  provides:
    - "AC-ARCH-05 closure"
    - "M9 VERIFIED"
    - "M10 VERIFIED"
  affects:
    - "20-05 (reads ctl_instruction.md after 20-04 edits)"
tech_stack:
  added: []
  patterns:
    - "evidence-first spec cleanup with separate packets sharing one AC"
    - "dataset-occupancy framing for normalization support ranges"
key_files:
  created:
    - ".planning/phases/16-evidence-framework-and-issue-adjudication/evidence/M9.md"
    - ".planning/phases/16-evidence-framework-and-issue-adjudication/evidence/M10.md"
  modified:
    - ".planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md"
    - "pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md"
decisions:
  - "M9 and M10 remain separate evidence/verdict records sharing AC-ARCH-05"
  - "Dataset-occupancy framing uses issue-doc language, not the planning term 'realized support'"
  - "No numeric v1.4 mass range stated because exact range depends on dataset μ and σ per slot"
  - "Energy occupancy: E_norm in [-1, 0) for bound systems; positive tanh range unused; acceptable for SIREN"
metrics:
  duration: "~1h"
  tasks_completed: 3
  tasks_total: 3
  files_created: 2
  files_modified: 2
  completed: "2026-06-05"
---

# Phase 20 Plan 04: Energy and Mass Realized-Support Cleanup Summary

**One-liner:** Energy and mass normalization support ranges framed as dataset-occupancy facts with separate M9/M10 evidence packets, verdict-gated spec edits, and combined AC-ARCH-05 audit closure.

## Objective

Close AC-ARCH-05 by documenting that the energy normalization produces `E_norm` in `[-1, 0)` for the bound-system dataset (positive tanh range unused) and that the mass normalization produces asymmetric `m_norm` ranges for hierarchical ICs (carrying mass hierarchy information), framing both as properties of the data-generation regimes rather than normalizer defects.

## Execution Summary

### Task 1: Create and fill M9 and M10 evidence packets

Created separate evidence packets for energy (M9) and mass (M10) normalization realized support. Each packet includes:

- Severity rationale (MINOR — formula correct, documentation gap only)
- Source positions citing resolution doc and issue doc with line ranges
- Spec evidence citing the `tanh(E / E_scale)` and `tanh((m_i - mu)/(sigma + 1e-8))` rows
- Dataset-support notes citing README.md for bound-system energy and hierarchical/standard mass regimes
- FUT-01 hand-off note (not applicable — no formula change)
- Recorded verdict: `accept-resolution` for both (sources agree)
- Before/After spec notes documenting the intended prose additions

Ledger updated: M9 and M10 rows advanced PENDING → IN_PROGRESS with verdicts recorded.

**Commit:** `69f9e2b` — evidence(20): fill M9/M10 energy+mass realized-support packets and record verdicts

### Task 2: Edit support-range framing in ctl_instruction.md

Verdict-gated spec edits applied:

- **Energy (line 1038):** Added prose documenting that `E_norm` occupies `[-1, 0)` for the bound-system dataset, the positive tanh range is unused, this is acceptable for SIREN, and is not a normalizer correctness failure. References README.md for data-generation regimes.
- **Mass (line 1040):** Added prose documenting that hierarchical IC mass slots produce asymmetric `m_norm` ranges, this asymmetry carries mass hierarchy information, and is not a centering or correctness failure.
- **Negative audit:** Searched for defect-framing prose; none found (confirmed no-op as expected from prior review).
- **Pre-commit diff verified:** No `tanh`, `E_scale`, or `sigma` formulas were changed — only explanatory prose added.

**Commit:** `a685bd0` — spec(20): document energy/mass normalization as dataset occupancy facts (ARCH-05)

### Task 3: Combined support-range audit and AC-ARCH-05 verification

**Positive audit** confirmed dataset-occupancy framing present:
- `ctl_instruction.md:1038` — energy occupancy (`[-1, 0)`, unused positive range, acceptable for SIREN)
- `ctl_instruction.md:1040` — mass occupancy (asymmetric, carries hierarchy information)
- Formula-vs-dataset range distinction present in both

**Negative audit** confirmed no defect-framing text:
- Two matches found — both are explicitly negating/disclaiming prose ("is not a normalizer correctness failure", "is not a centering or correctness failure")
- Zero matches characterize M9/M10 support occupancy/asymmetry as a normalization defect
- `pinn_architecture.md` read-only audit: no defect-framing text found

Packets updated with combined-audit notes. Ledger M9/M10 advanced IN_PROGRESS → FIX_APPLIED → VERIFIED.

**Commit:** `8259adf` — verify(20): AC-ARCH-05 combined support-range audit passes; M9/M10 VERIFIED

## Deviations from Plan

None — plan executed exactly as written.

## Key Decisions

1. **Separate packets, shared AC:** M9 (energy) and M10 (mass) remain separate evidence records with separate verdicts, sharing only the AC-ARCH-05 closure audit.
2. **Issue-doc language in spec:** Spec prose uses plain descriptive wording ("dataset-occupied range", "acceptable for SIREN", "not a correctness failure"), not the planning shorthand "realized support."
3. **No numeric v1.4 mass range:** The exact `m_norm` range under the v1.4 `tanh((m_i - mu)/(sigma + 1e-8))` formula depends on dataset-wide μ and σ per slot. The conceptual finding (asymmetry carries hierarchy information) applies without stating a specific number.
4. **Energy occupancy grounded in physics:** Bound gravitational systems have `E < 0`; this maps through `tanh` to `[-1, 0)`. This is a direct consequence of the physics and dataset selection (prescreening for bound systems), not a normalizer design choice.

## Acceptance Check: AC-ARCH-05

**Status:** CLOSED

Evidence trail:
- Completed `evidence/M9.md` and `evidence/M10.md` as separate records with verdicts
- Ledger M9/M10 → VERIFIED
- Combined positive audit: realized-support framing present, formula-vs-dataset range distinction present
- Negative audit: no defect-framing of energy or mass support occupancy
- Every numeric range cited from README.md or stated qualitatively
- No `tanh` normalization formulas were changed (framing-only edits)

## Known Stubs

None. All evidence packets are complete with verdicts, source citations, dataset-support notes, and audit records.
