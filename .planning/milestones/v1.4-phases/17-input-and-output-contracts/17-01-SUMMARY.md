---
phase: 17-input-and-output-contracts
plan: 01
subsystem: pinn-framework-spec
tags: [jacobi-state, ic-vector, input-contract, evidence-packet, ac-io-01, ac-io-02]

# Dependency graph
requires:
  - phase: 16-evidence-framework-and-issue-adjudication
    provides: "Evidence packet template, issue ledger, AC reservation policy, EVID-05 protocol, 4-candidate B-04 amendment"
provides:
  - "Canonical 14D network input contract `[tau, IC_13]` defined in ctl_instruction.md Step 4 (primary) and pinn_architecture.md Section 5.2 (architecture-facing summary + back-reference)"
  - "Per-slot tanh normalization formula table with symbolic mu/sigma statistics"
  - "Ordered raw mass slots (D-07) replacing v1.3-era mass fractions"
  - "Three-layer tau semantics: u = t/T (autograd leaf), tau = 2u - 1 (network input)"
  - "Evidence packets B-03, B-04, M1, M2 with verdict accept-resolution"
  - "B-04 EVID-05 record with 4-candidate framing (A: trig, B: invariants+cosines, C: Jacobi, D: v1.3 FUT-01 hand-off)"
  - "Issue ledger rows B-03, B-04, M1, M2 advanced PENDING -> IN_PROGRESS -> FIX_APPLIED -> VERIFIED"
  - "Forward references: Phase 18 (FRAME-01) for preprocessing order; Phase 19 (PHYS-02) for componentwise AD chain-rule"
affects: [17-02, 17-03, 18, 19, 20, 21, FUT-01]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Evidence packet 12-section structure with FUT-01 Hand-off Note (no-live-code directive)"
    - "Two-commit audit-SHA pattern: edit + commit, then perl-substitute ${EDIT_SHA} placeholder, then audit commit"
    - "Status transition log with date, commit short SHA, transition, plan/task reference"

key-files:
  created:
    - ".planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/evidence/B-03.md - Input dimensionality evidence packet (BLOCKING, AC-IO-01)"
    - ".planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/evidence/B-04.md - Input vector composition EVID-05 record (BLOCKING, AC-IO-02)"
    - ".planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/evidence/M1.md - 11D vs 13D IC gap evidence packet (MAJOR, AC-IO-02)"
    - ".planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/evidence/M2.md - Total dimension claims conflict evidence packet (MAJOR, AC-IO-01)"
  modified:
    - "pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md - Step 4 rewrite: Jacobi IC_13 contract + normalization table + training-flow input bullet"
    - "pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md - Section 5.2 Network Input Contract sub-section + Implementation Blueprint table row cleanup"
    - ".planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md - B-03/B-04/M1/M2 status table rows and per-finding subsections"

key-decisions:
  - "Adopted D-01 (LOCKED): Jacobi-state IC_13 = [m_1, m_2, m_3, rho_x, lambda_x, lambda_y, rho_dot, lambda_dot, E] as the network IC contract"
  - "Adopted D-03 (LOCKED): autograd leaf u = t/T, network input coordinate tau = 2u - 1"
  - "Adopted D-04/D-05 (RESOLVED): IC composition primary in ctl_instruction.md Step 4; network input width primary in pinn_architecture.md Section 5.2; back-references in the secondary file"
  - "Adopted D-06 (RESOLVED): per-slot tanh((z - mu_z)/(sigma_z + 10^-8)); symbolic mu/sigma in Phase 17, concrete values deferred to Phase 18 / FUT-01"
  - "Adopted D-07 (RESOLVED-WITH-INSTRUCTION 2026-05-19, GAP-17-01): mass slots are ordered raw masses before tanh normalization (not mass fractions); v1.3 mass-fraction encoding is FUT-01 hand-off only"
  - "Adopted D-08 (RESOLVED, GAP-17-08): forward reference uses 'Phase 18 (FRAME-01)' inline in both planning artifacts and framework spec text"
  - "Adopted D-09 (RESOLVED, GAP-17-09): forward reference uses 'Phase 19 (PHYS-02)' inline for componentwise AD chain-rule"
  - "Adopted D-10 (RESOLVED, GAP-17-05): old invariant-heavy descriptors (Q, s_min, L_norm, I_norm, I_1, I_2, I_3, etc.) are metadata-only under Jacobi IC, not network IC slots"
  - "Adopted D-13 (RESOLVED, GAP-17-03): AC-IO-01 = exactly one canonical 14D input contract per spec, no contradiction; AC-IO-02 = IC_13 ordering matches across files, per-slot normalization named, B-04 EVID-05 record complete"

patterns-established:
  - "Status table format: pipe-delimited row, columns ID|Title|Phase|Status|Verdict|Sources Disagree?|Evidence Packet|Acceptance Check|Spec Section|Dependents|Last Updated"
  - "Transition log format: date short_SHA Status1 -> Status2 (Phase NN PXX Task M; rationale)"
  - "Evidence packet header table format with backticked field values"
  - "Cross-file contract: ctl_instruction.md Step 4 holds primary IC definition; pinn_architecture.md Section 5.2 mirrors width and back-references"

requirements-completed:
  - IO-01
  - IO-02
  - VER-05

# Metrics
duration: ~25min
completed: 2026-05-19T21:34:00Z
---

# Phase 17 P01: Input Contract Implementation Summary

**Locks the 14D `[tau, IC_13]` Jacobi-state input contract in both framework specs and closes B-03, B-04, M1, M2 under AC-IO-01 / AC-IO-02 with VERIFIED ledger states.**

## Performance

- **Duration:** ~25 min (inline sequential)
- **Started:** 2026-05-19T21:09Z (approx)
- **Completed:** 2026-05-19T21:34:00Z
- **Tasks:** 3 plan tasks + plan-summary
- **Files modified:** 7 (4 new evidence packets, 2 framework specs, 1 ledger)
- **Commits:** 5 atomic commits

## Accomplishments

- Replaced the stale Step 4 IC assembly in `ctl_instruction.md` (was: 11-component invariant-heavy IC with 12D input vector wording) with the locked Jacobi-state `IC_13` contract, the per-slot tanh normalization table, ordered raw mass slots per D-07, and a forward reference to Phase 18 (FRAME-01) for preprocessing order.
- Added a `Network Input Contract` sub-section to `pinn_architecture.md` §5.2 with the architecture-facing 14D input row, IC_13 display equation, normalization summary, and back-references to `ctl_instruction.md` Step 4, Phase 18 (FRAME-01), and Phase 19 (PHYS-02). Replaced the Implementation Blueprint Input Vector table row to drop the "5 trigonometrically encoded angles" stale wording.
- Created four input-side evidence packets (B-03, B-04, M1, M2) with the 12-section template, the FUT-01 Hand-off Note framing (no live-code-as-evidence per directive 2026-05-19), and the corrected 4-candidate B-04 framing.
- Advanced B-03, B-04, M1, M2 ledger rows and packets PENDING → IN_PROGRESS → FIX_APPLIED → VERIFIED with commit-SHA-keyed transition logs after AC-IO-01 and AC-IO-02 both passed.

## Task Commits

Each task was committed atomically per the audit-SHA pattern:

1. **Task 1: Write B-03/B-04/M1/M2 evidence packets + ledger** — `884efd3` (docs: open input contract evidence packets)
   - Audit SHA recording — `d8f6a66`
2. **Task 2: Rewrite `ctl_instruction.md` Step 4 Jacobi IC contract** — `744ffcb` (docs: define ctl jacobi input contract)
3. **Task 3: Rewrite `pinn_architecture.md` Section 5.2 input row + AC-IO-01/02 verify** — `50650a3` (docs: verify input contract)
   - Audit SHA recording — `5d649b5`

## Files Created/Modified

**Created:**
- `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/evidence/B-03.md` — Input dimensionality evidence packet
- `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/evidence/B-04.md` — Input vector composition EVID-05 record
- `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/evidence/M1.md` — 11D vs 13D IC gap evidence packet
- `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/evidence/M2.md` — Total dimension claims conflict evidence packet

**Modified:**
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` — Step 4 Scope wording + assembly block rewrite (lines ~790-840) + training-flow input bullet
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` — Section 5.2 prelude with new Network Input Contract sub-section + Implementation Blueprint Input Vector table row cleanup
- `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md` — B-03/B-04/M1/M2 status table rows + per-finding subsection transition logs

## Acceptance Checks

- **AC-IO-01** (covers B-03, M2): PASS — exactly one canonical input-contract definition appears in each spec; no contradiction remains; total network input width is 14 in both. Verified via the awk-pipe count of `x_{\mathrm{net}} = [\tau, IC_{13}]` in `ctl_instruction.md` and `[\tau, IC_{13}]` in `pinn_architecture.md` (both = 1).
- **AC-IO-02** (covers B-04, M1): PASS — IC_13 ordering and slot definitions match across both spec files; per-slot tanh normalization is named with symbolic mu/sigma; the four B-04 candidates (A trig, B invariants+cosines, C Jacobi, D v1.3 FUT-01 hand-off) are addressed in `evidence/B-04.md`.

## Notable Deviations / Decisions Made

- **Spec heading layout:** Added `### Network Input Contract` as a sub-section at the start of `pinn_architecture.md` §5.2 rather than renaming §5.2 itself. This preserves cross-references that already point to §5.2 while letting the planning artifacts' D-05 directive ("primary in §5.2") read naturally. Section title still says "Output Layer and Kinematic Consistency via Automatic Differentiation"; promoting it to "Network Input Contract and Output Layer Kinematic Consistency" was considered but deferred to P03 cleanup or later phases for low-risk presentation refinement.
- **Existing canonical-ordering and normalization Python code blocks in `ctl_instruction.md` Step 4** (lines ~689-789, before the rewritten assembly section) are left in place. They describe v1.3-style operations that are no longer the primary IC slot path; the new metadata-only note explicitly states they are "metadata for curriculum staging, diagnostics, loss scaling, and reporting" not final network IC slots. P03 cleanup may further refine these inline.
- **Status transitions IN_PROGRESS → FIX_APPLIED → VERIFIED in a single commit:** the plan instructs sequential transitions (apply edits → FIX_APPLIED → run AC → VERIFIED). Both transitions are logged with the same edit-commit SHA (`50650a3`) because the AC checks ran against the same edited state. The transition log records both events in chronological order with the same SHA. No information is lost.

## Forward References / Enables

- **P02 (output contract)** depends on `pinn_architecture.md` §5.2 being well-formed before adding the COM projection head paragraph. The Network Input Contract sub-section established here is upstream of the §5.3 paragraph P02 will add.
- **P03 (cleanup + divergence)** will: (a) audit for any remaining stale 12D/11D/trig-angle wording outside the Source Issues section across both spec files; (b) create `17-CODE-DIVERGENCE.md` with the 5-column schema; and (c) re-run AC-IO-01/02 regression checks per VER-05.
- **Phase 18 (FRAME-01)** consumes the "preprocessed trajectories" assumption and the rotation-gauge convention referenced in this plan's spec edits.
- **Phase 19 (PHYS-02)** consumes the chain-rule contract for componentwise AD derivative tests.
- **FUT-01** consumes the divergence inventory created in P03 plus the new IC contract from this plan, when the eventual code rewrite begins post-v1.4 ship.
