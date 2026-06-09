---
phase: 21
phase_name: "Acceptance Checks and Handoff"
project: "3-body-problem"
generated: "2026-06-09"
counts:
  decisions: 7
  lessons: 5
  patterns: 6
  surprises: 4
missing_artifacts: []
---

# Phase 21 Learnings: Acceptance Checks and Handoff

## Decisions

### Force-Energy Pass Criterion Refined to Matched-Plummer Contract
The force-energy acceptance check's pass criterion was refined from a generic energy-conservation test to the grounded "matched-Plummer finite-Hamiltonian and force-gradient consistency contract" — meaning the analytic matched-Plummer Hamiltonian must be finite, and its negative position gradient must yield accelerations matching the physical force residual with the same training-time Plummer softening.

**Rationale:** The original criterion was not physically grounded in the v1.4 framework specs. The matched-Plummer formulation is derivable from first principles and ties directly to what the PINN will actually compute at training time.
**Source:** 21-01-SUMMARY.md

---

### Handoff Classifies Issue 01 Findings into Fixed / Intentionally Unchanged / Deferred
The validation handoff document (`21-HANDOFF.md`) was structured into three explicit sections: (1) Fixed — findings that resulted in explicit spec changes, (2) Intentionally Unchanged — findings that were false positives or valid existing conventions, (3) Deferred — findings like M6/M7 not adjudicable from supplied files or requiring future empirical validation.

**Rationale:** Phase 22 needs a definitive, structured list of what changed, what didn't and why, and what remains open. The three-bucket classification prevents ambiguous "sort of addressed" findings from drifting into the next phase.
**Source:** 21-02-PLAN.md

---

### Resolved SI-* Ledger Entries Retired with Back-References; Unrelated Entries Preserved Untouched
For SI-* entries related to Issue 01 (e.g., `SI-CTL-001`, `SI-SSR-001`): heading preserved, content replaced with a back-reference to the resolving v1.4 finding (e.g., B-03, B-04, M5). For SI-* entries unrelated to Issue 01 (e.g., `SI-PINN-002`, `SI-DQA-002`, `SI-DQA-003`): preserved completely untouched.

**Rationale:** Deleting SI headings would break traceability; replacing with back-references maintains the audit trail while marking resolution. Touching unrelated entries would risk introducing new errors during a reconciliation pass.
**Source:** 21-02-PLAN.md

---

### M6 and M7 Explicitly Deferred as Not Adjudicable from Supplied Files
M6 and M7 were classified as Deferred rather than resolved, because "the accessible consolidation map does not expose standalone M6 or M7 semantic categories." They are to be revisited when source material is available.

**Rationale:** The v1.4 governance protocol forbids inventing adjudications where source materials are silent. Rather than force a resolution, the findings are explicitly preserved for future work.
**Source:** 21-02-SUMMARY.md

---

### SI-PINN-001 Not Synthesized Despite VER-06 Listing It as Candidate
`VER-06` listed `SI-PINN-001` as a candidate for retirement, but `git grep` at v1.4-pre-phase-21 and the current tree found it only in planning references, not in any framework-spec Source Issues section. The decision was to record the absence rather than create a new retired entry.

**Rationale:** Creating a new retired entry would fabricate source-issue provenance that never existed in the specs. Recording the absence is the honest audit outcome.
**Source:** 21-VERIFICATION.md

---

### Disposable Validation Probes Run in Isolated Environment
Validation probes are defined as disposable scripts in `.planning/milestones/v1.4-phases/21-acceptance-checks-and-handoff/probes/` that must run in an isolated environment without mutating the dataset or live code.

**Rationale:** The STRIDE threat model (T-21-01) identified tampering of validation probes as a threat. Isolation ensures probes verify specs without side effects on the data or codebase they validate.
**Source:** 21-01-PLAN.md

---

### Probe Results Are Summary-Only; Raw Stdout with SHA-256 Hashes Is the Re-Derivable Evidence
`21-PROBE-RESULTS.md` records summary metrics and SHA-256 hashes. The actual re-derivable evidence lives in per-probe stdout files under `evidence/`.

**Rationale:** Summaries can be edited; raw stdout with cryptographic hashes provides tamper-evident, re-derivable proof that a probe actually passed with specific outputs.
**Source:** 21-VERIFICATION.md

---

## Lessons

### Prior Handoff Depended on Ungrounded PASS Evidence
The initial Phase 21 handoff claimed all checks passed but did not cite real probe execution outputs or ledger state. The repair pass replaced these ungrounded claims with actual stdout evidence and verified ledger state.

**Context:** This was discovered during the Phase 21 Plan 02 repair execution. The original handoff had asserted compliance without the underlying evidence artifacts.
**Source:** 21-02-SUMMARY.md

---

### Section 10 Already Existed from Prior Commit — Repair Was Needed, Not Creation
The 21-01 plan assumed Section 10 needed to be appended to `pinn_architecture.md`, but it already existed from a prior Phase 21 commit. The actual work was a repair pass: correcting executable commands and refining the force-energy criterion.

**Context:** This meant the plan's Task 1 action description was partially stale by execution time. The agent adapted by repairing rather than creating.
**Source:** 21-01-SUMMARY.md

---

### Executable Commands Required `.venv/bin/python` Not Bare `python`
The repair pass for Section 10 corrected the executable commands to explicitly use `.venv/bin/python` rather than relying on the bare `python` command, which would not resolve correctly in the project's environment.

**Context:** Without the explicit venv path, the acceptance check commands would fail or use the wrong Python interpreter, making the checks non-reproducible.
**Source:** 21-01-SUMMARY.md

---

### VER-06 Requirement Did Not Match Reality for SI-PINN-001
The VER-06 requirement listed `SI-PINN-001` as a candidate SI entry to reconcile, but it did not exist in any framework-spec Source Issues section. The verification passed by recording the absence rather than manufacturing a match.

**Context:** This highlights that requirements documents can reference artifacts that don't exist in practice. The correct response is to document the gap, not fabricate compliance.
**Source:** 21-VERIFICATION.md

---

### Weak-Probe Regression Guards Are Necessary
Three specific degenerate probe patterns were identified and checked as automated verification gates: (1) `T=1` scaling tautology — a scaling test with only one data point that trivially passes, (2) `DummyPINN` — a probe using a dummy network instead of the real SIREN architecture, (3) `nn.Linear(14, 9)` dummy loss — a probe that reduces to a simple linear layer instead of exercising the full physics loss.

**Context:** These guards prevent probes from passing vacuously — a probe must actually exercise the architecture and physics it claims to validate.
**Source:** 21-VERIFICATION.md

---

## Patterns

### Disposable Validation Probe Pattern
Define acceptance checks as small, standalone Python scripts in the phase directory that: (1) exercise a specific physics/math invariant, (2) print a numeric result to stdout, (3) exit with code 0 on pass, (4) capture stdout as evidence with SHA-256 hash. Probes are non-mutating and disposable.

**When to use:** When a framework spec needs to be proven internally consistent and implementable without running the full training pipeline. Each probe tests one invariant in isolation.
**Source:** 21-01-PLAN.md

---

### Three-Section Handoff Classification (Fixed / Intentionally Unchanged / Deferred)
Structure cross-phase handoff documents around three exhaustive buckets for every finding: Fixed (spec was changed), Intentionally Unchanged (finding was false positive or valid convention), Deferred (not adjudicable or requires future work).

**When to use:** When closing a phase that adjudicated a set of issue findings and the next phase needs to know exactly what changed and what didn't.
**Source:** 21-02-PLAN.md

---

### SI-Ledger Reconciliation: Retire with Back-Reference, Preserve Unrelated
When closing out issue-tracking markers (SI-* entries) in specs: for resolved entries, keep the heading but replace content with a back-reference to the resolving finding; for unrelated entries, preserve completely untouched.

**When to use:** When an issue-adjudication milestone is closing and the SI markers in framework specs need to reflect resolution status without losing audit trail or disturbing unrelated markers.
**Source:** 21-02-PLAN.md

---

### Source-Level Weak-Probe Regression Check
Before accepting probe results, run an automated source-level check that rejects known degenerate probe patterns (tautological parameter choices, dummy networks, trivial loss functions).

**When to use:** When validation probes are written as part of an acceptance-check phase and there is a risk that probes could pass vacuously without exercising the real architecture or physics.
**Source:** 21-VERIFICATION.md

---

### VER-05 Iterative Spec Correction Loop
Probe failures trigger spec correction rather than probe adjustment. If a probe fails against the framework spec, the spec is wrong and must be fixed — the probe is the oracle.

**When to use:** When acceptance-check probes are defined before spec finalization and the probes test grounded physical/mathematical invariants that the spec must satisfy.
**Source:** 21-01-PLAN.md

---

### GSD Completion Shape Audit
A phase is considered structurally complete only when it has all required GSD artifacts: context, research, discussion log, gaps, validation, verification, UAT, code divergence, and per-plan summaries.

**When to use:** During the final UAT pass for any phase to ensure no structural artifact is missing before declaring the phase complete.
**Source:** 21-UAT.md

---

## Surprises

### Prior Handoff Contained Ungrounded PASS Claims
The initial Phase 21 handoff document asserted that all checks passed but had no actual probe execution evidence behind the claims. This was only caught when Phase 21 Plan 02 attempted to reconcile the handoff against real ledger state and probe outputs.

**Impact:** Required a full repair pass of the handoff document. The ungrounded claims were replaced with citations to real stdout evidence and ledger state. This reinforced the v1.4 governance principle that every assertion must be grounded in traceable evidence.
**Source:** 21-02-SUMMARY.md

---

### All Five Probes Achieved Machine-Precision Results
Every probe returned results at or near machine epsilon: scaling `max_relative_error = 2.22e-16`, COM magnitude `7.90e-17`, AD `relative_error: 0.00e+00`, force-energy `relative_error: 1.62e-16`. The pass criteria ranged from `< 1e-5` to `< 1e-10`, so all passed by many orders of magnitude.

**Impact:** This confirms the v1.4 framework specs are internally mathematically consistent at the level of the probes. However, it also means the probes are validating analytic identities (not numerical robustness), so they cannot detect issues that would only appear at larger error magnitudes during actual training.
**Source:** 21-VERIFICATION.md

---

### No Intentionally Unchanged Findings Found in Ledger
The handoff's "Intentionally Unchanged" section was expected to list findings from Issue 01 that were determined to be false positives or valid existing conventions. In practice, no Issue 01 findings fell into this category — every finding was either Fixed or Deferred.

**Impact:** The three-bucket classification still works structurally, but the empty middle bucket suggests the Issue 01 findings were either clearly actionable or clearly non-adjudicable, with no ambiguous middle ground.
**Source:** 21-VERIFICATION.md

---

### Section 10 Assumed to Need Creation but Already Existed
The 21-01 plan was written assuming Section 10 of `pinn_architecture.md` needed to be created from scratch. In reality, a prior Phase 21 commit had already added it. The actual work was repair (fixing commands and refining criteria), not creation.

**Impact:** The plan required adaptation at execution time. The deviation was benign but highlights that plans written against a moving target (the same phase's earlier commits) can become partially stale before execution begins.
**Source:** 21-01-SUMMARY.md
