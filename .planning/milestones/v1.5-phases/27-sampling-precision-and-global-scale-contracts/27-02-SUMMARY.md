---
phase: 27
plan: 02
subsystem: sampling-precision-and-global-scale-contracts
tags: [PIPE-07, precision, float64, decimal.Decimal, DATA-05]
dependency_graph:
  requires: [27-01]
  provides: [27-03, 27-04]
  affects: [ctl_instruction.md §2.1, 24-ISSUE-LEDGER.md mass-drift/footer rows, evidence/data05-precision.md]
tech_stack:
  added: []
  patterns: [spec-string acceptance check (grep-based), same-commit discipline, two-phase SHA backfill]
key_files:
  created: []
  modified:
    - pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md
    - .planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-ISSUE-LEDGER.md
    - .planning/phases/25-evidence-framework-and-issue-ledger/evidence/data05-precision.md
decisions:
  - "Transcribed precision note verbatim from data05-precision.md Locked Convention (resolution-doc §4.3:481-489) after ctl §2.1 mass-invariance gate"
  - "Used two-phase SHA backfill pattern (F-08): substantive commit b6fe225d writes <pending-27-02-sha> placeholder; provenance commit 70dd29b backfills the real SHA"
  - "D7 regression AC-PIPE-06 PASS: no shared footer/param_provenance text was touched by the §2.1 edit"
  - "Footer row advanced to VERIFIED: both PIPE-06 (already VERIFIED via D7 Phase 26) and PIPE-07 (closed here) facets are complete"
metrics:
  duration: "15 minutes"
  completed_date: "2026-06-14"
---

# Phase 27 Plan 02: PIPE-07 Precision Contract Summary

**One-liner:** Landed the float64-sufficiency / Decimal-as-classifier precision contract into `ctl_instruction.md` §2.1 as an additive note after the mass-invariance gate, with the DATA-05 70/70 rerun validation cited as evidence-of-record.

## What Changed

1. **`ctl_instruction.md` §2.1 precision note (appended after line 576):**
   - Added a blockquote note stating: `float64` is the data-side precision contract for all validation metrics and invariants.
   - `decimal.Decimal` is reserved **only** as the failure classifier for the IC↔Brutus `t=0` mass-consistency gate, never as the routine parsing or metric-computation path.
   - Current IC masses are canonical; the 70 historical base-hier mismatches were stale artifacts (0.1–1.0 mass units), not a precision failure.
   - A future IC↔Brutus mass-gate mismatch is a **fail** condition (quarantine), not a trigger to switch to Decimal.
   - Cites `24-DATA05-RERUN-VALIDATION.md` (70/70 PASS) as evidence-of-record.
   - The existing §2.1 float64 `1e-15` absolute mass-invariance gate is preserved verbatim — this is an additive clarification, not a convention change.

2. **`24-ISSUE-LEDGER.md` mass-drift row (line 41):**
   - Status: `PENDING` → `IN_PROGRESS` → `FIX_APPLIED` → `VERIFIED`
   - Evidence-Packet: linked to `evidence/data05-precision.md`
   - Verdict: `accept-resolution`
   - AC-PIPE-07: PASS

3. **`24-ISSUE-LEDGER.md` footer row (line 40):**
   - Status: `PENDING` → `VERIFIED` (F-16: both facets closed — PIPE-06 via D7 Phase 26, PIPE-07 via AC-PIPE-07)
   - Evidence-Packet: linked to `evidence/data05-precision.md`
   - AC-PIPE-07: PASS

4. **`evidence/data05-precision.md` pointer packet:**
   - Current Status: `VERIFIED`
   - Status Transition Log: forward transitions `PENDING → IN_PROGRESS → FIX_APPLIED → VERIFIED` with SHA `b6fe225d` (backfilled by provenance commit `70dd29b`)
   - The first entry's authoring SHA (`09e37f8`) was left intact per F-08

## Deviations from Plan

**None — plan executed exactly as written.**

No source-silent decisions were encountered; all text was transcribed verbatim from the locked `data05-precision.md` Locked Convention paragraph. No `pinn_architecture.md` edit was needed (precision is data-side only, per D-02/D-04).

## Verification Results

### AC-PIPE-07 (run against edited `ctl_instruction.md`)

| Assertion | Status |
|-----------|--------|
| float64 sufficiency stated | PASS |
| Decimal classifier-only scope | PASS |
| current ICs canonical | PASS |
| stale artifacts interpretation | PASS |
| fail condition for future mismatch | PASS |
| DATA-05 citation present | PASS |
| 70/70 validation cited | PASS |
| **Negative control:** decimal.Decimal appears exactly once (classifier context only) | PASS |
| **Existing §2.1 gate preserved** | PASS |
| **Overall** | **PASS** |

### AC-PIPE-06 D7 Regression (run against shared footer/param_provenance text)

| Assertion | Status |
|-----------|--------|
| `param_provenance` tokens present | PASS (2 mentions) |
| `direct`/`inferred`/`absent`/`measured` values present | PASS |
| D7 row still VERIFIED | PASS |
| **Overall** | **PASS** |

## Commits

| SHA | Type | Description |
|-----|------|-------------|
| `b6fe225d` | `spec(27-02)` | Land PIPE-07 float64 precision contract after ctl §2.1 |
| `70dd29b` | `verify(27-02)` | Backfill b6fe225d SHA into data05-precision.md and ledger transition logs |

## Self-Check: PASSED

- [x] `ctl_instruction.md` precision note exists at §2.1 (line 578)
- [x] `data05-precision.md` packet status is VERIFIED
- [x] `24-ISSUE-LEDGER.md` mass-drift row is VERIFIED with data05-precision.md link
- [x] `24-ISSUE-LEDGER.md` footer row is VERIFIED with data05-precision.md link
- [x] D7 row remains VERIFIED (no regression)
- [x] Both commits exist in git log
- [x] AC-PIPE-07 PASS (all 7 positive assertions + negative control)
- [x] AC-PIPE-06 regression PASS

## Next-Wave Readiness

- **Wave 3 (PIPE-08 stage-query):** Ready. The `dt_out`/`n_snapshots` metadata contract and `sample_replay`/`sample_lookahead` method signatures are the next deliverables. No dependency on this wave's completion.
- **Wave 4 (PIPE-09 compute_globals):** Ready. The §2.5 global-scale D convention and `E_scale` floor canonicalization are independent of this wave.

## Threat Surface

No new security-relevant surface introduced. All changes are Markdown spec text and process-ledger updates.

## Known Stubs

None. All PIPE-07 precision contract text is fully wired to its evidence sources.
