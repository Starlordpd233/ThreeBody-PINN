---
phase: 56-contract-amendment-train-free-gate
plan: 01
subsystem: verification
tags: [gate-04, causal-weights, r-ref, fail-closed, train-free-gate, tdd, tracer]

requires:
  - phase: 55-architecture-characterization-probe
    provides: DEFAULT_CASES, stratified_collocation_times, bin_mean_residuals, SweepCase, the probe module this plan extends
  - phase: 54-recalibration-decision-grounding
    provides: 54-RULING.md — the ratified A1+B2+C1+D3+E1 recipe, the re-issued acceptance criteria, and the reference-invalidation list
provides:
  - ratified_causal_weights (probe helper; the ratified-recipe weight vector via the trainer's own causal_physics_loss)
  - pinn/verification/gate04_train_free.py — Gate04Verdict / Gate04CaseResult / VERDICT_PASS / VERDICT_BLOCK / gate04_verdict / compute_r_ref / evaluate_case / run_gate / write_r_ref_artifact
  - pinn/verification/artifacts/r_ref_stage0.json (schema phase56-r-ref-stage0/v1; R_ref = 1.9749775821244170e+10, PASS, full provenance)
  - tests/phase56/ contract suite (12 tests, 0 skips)
affects: [phase-56-02, phase-56-03, phase-56-04, phase-56-06, phase-57-run-04]

actuals:
  tokens: 13574
  tasks: 2
  commits: 2
  plan_head_before: 8c24609c435cb971ce0bfdca2db18522733d4de4

tech-stack:
  added: []
  patterns:
    - "Single-verdict-function convention (gate_metrics.gate_verdict) applied to a multi-condition gate: gate04_verdict is the only PASS/BLOCK source, backed by a rule-ordered private reasons audit"
    - "Reuse-not-reimplement: the gate reaches the trainer's exp/prefix/clamp arithmetic only through the probe helper; the dtype floor is read from resolve_causal_clip_facts at call time"
    - "Governed-artifact writer integrity: write_r_ref_artifact refuses to persist a verdict whose r_ref is not exactly numpy.median of the recorded bin means, or whose cases are not identifiable against DEFAULT_CASES"
    - "Verdict-object coherence construction: Gate04Verdict.__post_init__ rejects a PASS with no cases / bad r_ref / non-empty reasons, and a BLOCK with no reasons"

key-files:
  created:
    - pinn/verification/gate04_train_free.py
    - pinn/verification/artifacts/r_ref_stage0.json
    - tests/phase56/__init__.py
    - tests/phase56/test_gate04_train_free.py
  modified:
    - pinn/verification/architecture_characterization_probe.py

key-decisions:
  - "Task 1 contract checkpoint answered by the owner with the literal word 'confirmed' (2026-09-06): the proposed three-part public contract was accepted exactly as written (option accept-proposed); no name, field, path, or schema string was amended"
  - "gate04_verdict returns the verdict STRING (mirroring gate_metrics.gate_verdict); the frozen signature (case_results, *, causal_clip_min_weight) cannot construct a full Gate04Verdict (r_ref/precision/device are not its inputs), and the plan's own acceptance criteria read gate04_verdict([]) == \"BLOCK\"; blocking reasons reach callers through run_gate's Gate04Verdict, computed by the same private rule-ordered audit so the verdict string and the reasons can never drift"
  - "INVALIDATION_TRIGGERS holds exactly the fifteen named surfaces from 54-RULING.md 'Reference invalidation' (the same enumeration 56-CONTEXT.md D-02 gives); the ruling's closing resource-failure policy sentence is carried verbatim in the module docstring, not as a sixteenth tuple entry, because it is a run policy rather than a named surface"
  - "__all__ lists exactly the symbols this plan defines; the artifacts table's naming of 56-02's future symbols is honored as a naming freeze (56-02 appends those exact names), since listing undefined names would break star-imports with AttributeError"
  - "evaluate_case re-measures its case rather than receiving compute_r_ref's arrays: the frozen decomposition (compute_r_ref / evaluate_case signatures) makes the two passes structurally required, and both are deterministic (same recorded seeds), so the duplicated measurement is exact, not approximate"

patterns-established:
  - "Fail-closed gate composition: measurement raises convert to BLOCK verdicts inside run_gate; argument-contract violations (unknown precision/device) still raise before any measurement"
  - "Prefix-finiteness audit: the exclusive-prefix intermediates are re-accumulated as plain Python floats for inspection only — never as a second implementation of the weight formula"

requirements-completed: [GATE-04]

coverage:
  - id: D1
    description: "ratified_causal_weights probe helper — flat-profile exclusive-prefix identity exp(-arange(16)) and fail-closed input validation"
    requirement: GATE-04
    verification:
      - kind: unit
        ref: "tests/phase56/test_gate04_train_free.py::RatifiedCausalWeightsTests (4 tests, 13 subtests with siblings)"
        status: pass
    human_judgment: false
  - id: D2
    description: "gate04_verdict fail-closed rules — strict floor boundary, non-finite residual/prefix/weight, empty case set"
    requirement: GATE-04
    verification:
      - kind: unit
        ref: "tests/phase56/test_gate04_train_free.py::Gate04VerdictTests (4 tests)"
        status: pass
    human_judgment: false
  - id: D3
    description: "run_gate end-to-end over the six audited DEFAULT_CASES at float64/cpu — PASS with per-case min_weight strictly above the call-time floor and r_ref == numpy.median of the recorded 96 means"
    requirement: GATE-04
    verification:
      - kind: integration
        ref: "tests/phase56/test_gate04_train_free.py::RunGateEndToEndTests::test_run_gate_six_default_cases_pass"
        status: pass
    human_judgment: false
  - id: D4
    description: "Committed R_ref artifact with the frozen 10-key schema, written atomically with full provenance"
    requirement: GATE-04
    verification:
      - kind: integration
        ref: "tests/phase56/test_gate04_train_free.py::RRefArtifactTests::test_write_r_ref_artifact_frozen_schema"
        status: pass
      - kind: other
        ref: ".venv/bin/python -c \"import json,pathlib; ...\" artifact assertion -> R_REF_ARTIFACT_OK (run against the committed artifact)"
        status: pass
    human_judgment: false

duration: 42 min
completed: 2026-09-06
status: complete
---

# Phase 56 Plan 01: GATE-04 Train-Free Gate — Condition-(i) Tracer Slice Summary

**GATE-04's condition-(i) path proven end to end on its thinnest real slice: the six audited cases measured through the trainer's own loss function render one fail-closed PASS verdict, and R_ref = 1.9749775821244170e+10 (median of the 96 raw bin means) is persisted as a governed, atomically-written, self-consistent artifact.**

## Performance

- **Duration:** 42 min
- **Started:** 2026-09-06T12:33:47Z
- **Completed:** 2026-09-06T13:15:19Z
- **Tasks:** 2/2 (Task 1 decision checkpoint closed with the owner's answer; Task 2 tracer TDD)
- **Files modified:** 5 (3 created code/data + 1 modified + 1 created package marker)

## Task 1 — Contract checkpoint, owner answer (verbatim record)

Task 1 was a `checkpoint:decision` (gate="blocking") freezing the Phase-57-facing
public contract before any of it was written. The orchestrator presented it; the
owner's answer, received 2026-09-06 and recorded here verbatim, was:

> **confirmed**

i.e. option `accept-proposed`: the proposed three-part public contract in
56-01-PLAN.md Task 1's `<action>` block is accepted **exactly as written** —
Part 1 the probe helper `ratified_causal_weights(raw_bin_means, r_ref, *,
eta_c=CAUSAL_ETA_C, dtype, device, t_max=T_CHARACTERISTIC_TIME)`; Part 2 the
gate surface (`Gate04Verdict`, `Gate04CaseResult`, `VERDICT_PASS`/`VERDICT_BLOCK`,
`gate04_verdict(case_results, *, causal_clip_min_weight)`, two-value verdict
vocabulary per D-04); Part 3 the artifact path
`pinn/verification/artifacts/r_ref_stage0.json` with schema_version
`"phase56-r-ref-stage0/v1"` and the frozen ten top-level keys. Because the
contract was accepted unamended, Task 1's second acceptance clause (no surviving
renamed symbols) is vacuously satisfied, and the confirmed names are exactly the
names Task 2 wrote. Task 1 produced no production code by design; its record is
this section.

## Task Commits

1. **Task 2 RED: failing contract tests** — `62f94880` (`test(56-01)`) — 12 tests; 5 failed on the planned-behavior seam (probe helper absent), 7 skipped via the deferred-import scaffold (gate module not landed). RED evidence record verified by `gsd-tools check tdd-red-evidence` → **RED_EVIDENCE_OK** (`target_test_failed`; record + raw pytest output retained at `/tmp/gsd-56-01/red-record.json` and `/tmp/gsd-56-01/red-pytest.txt`).
2. **Task 2 GREEN: implementation + artifact** — `bbb572bc` (`feat(56-01)`) — probe helper, gate module, and the committed `r_ref_stage0.json` from a real six-case PASS run.

**Plan metadata:** committed with this SUMMARY (`docs(56-01)`).

No REFACTOR commit — the implementation landed clean; no cleanup changes were needed.

## TDD Gate Compliance

- RED gate: `test(56-01)` commit `62f94880` precedes GREEN; the target test (`RatifiedCausalWeightsTests::test_flat_profile_matches_exclusive_prefix`) failed as a real, distinctly-named assertion for the planned behavior; checker verdict `RED_EVIDENCE_OK`. The seven gate-module tests skipped (not crashed) in RED by the plan's own deferred-import design, and the post-GREEN verify runs report **0 skipped** — the suite's green state contains no hidden skips.
- GREEN gate: `feat(56-01)` commit `bbb572bc`; full suite 12 passed / 13 subtests / 0 skipped (196–203s per run, dominated by the twelve 4096-point initialization measurements).
- REFACTOR gate: not applicable (no changes).
- Tracer feedback gate (#3299 precedence): Task 2 carries no `gate="blocking-human"`; auto mode is inactive (`workflow._auto_chain_active: false`); `human_verify_mode` is `end-of-phase` and the task's `<verify>` is automated-only → row 3 applied: all four `<verify>` commands re-ran end-to-end **after** the GREEN commit and passed (12 passed/0 skipped; phase55 46 passed; `R_REF_ARTIFACT_OK`; fork-grep 0). ⚡ Tracer verified end-to-end — no expansion task follows in this plan.

## Files Created/Modified

- `pinn/verification/architecture_characterization_probe.py` (modified) — added `ratified_causal_weights` immediately after `bin_mean_residuals` (fail-closed validation before any tensor; the exp/prefix/clamp arithmetic delegated to `causal_physics_loss` unmodified; bin-centre ordering proxy), appended it to the existing `__all__`, and added `CAUSAL_ETA_C` to the constants import.
- `pinn/verification/gate04_train_free.py` (created) — the frozen public surface plus `compute_r_ref` (numpy.median of the 96 raw bin means), `evaluate_case`, `run_gate` (fail-closed; empty case list and any evaluation failure return BLOCK), `write_r_ref_artifact` (atomic, integrity-checked), `INVALIDATION_TRIGGERS` (the fifteen verbatim surfaces), and the module docstring's fail-closed resource-failure policy.
- `pinn/verification/artifacts/r_ref_stage0.json` (created, git-tracked) — real run output: PASS, `r_ref = 19749775821.24417`, six enriched case entries, all 96 raw bin means, configuration (seeds, bin edges, per-bin count, precision/device, torch/numpy versions, eta_c, t_max), provenance (git sha, worktree-dirty flags, timestamp), the fifteen invalidation triggers, `valid: true`.
- `tests/phase56/__init__.py`, `tests/phase56/test_gate04_train_free.py` (created) — 12 contract tests covering every behavior in the plan's `<behavior>` block plus the frozen public-contract names.

## Verification Evidence

| Check | Result |
|---|---|
| `pytest tests/phase56/test_gate04_train_free.py -x -q` | **12 passed, 13 subtests, 0 skipped** (run twice post-implementation: 196.8s and 203.3s) |
| `pytest tests/phase55/ -q` | **46 passed** (committed baseline held — the probe edit broke no sibling) |
| Artifact schema assertion (plan `<verify>` command 3) | **R_REF_ARTIFACT_OK** |
| Forked-arithmetic grep (`torch.cumsum\|torch.clamp_min\|2.225074\|-708.39`) | **0** |
| Bypass-vocabulary grep (`force\|skip_gate\|allow_block\|ignore_verdict`) | **0** (after deviation 1) |
| Import criterion | **IMPORT_OK** |
| Probe `__all__` criterion | **ALL_OK** |
| `gate04_verdict([]) == "BLOCK"` | **EMPTY_BLOCKS_OK** |
| `run_gate()` PASS + every case's `min_weight` strictly above the floor | PASS; per-case min weights 1.3e-06 … 2.1e-11 vs floor 2.2e-308 |
| Artifact git-tracked (`git ls-files`) | tracked |

The real run's `R_ref` and per-case min weights reproduce 56-RESEARCH.md Part
(b)'s session-computed illustrative figures to all displayed digits (same
deterministic seeds, same environment) — independent confirmation of the
research data the GAP-56-01 grounding rests on. `front_idx = 0` on all six
cases, as expected at initialization (Pitfall 3: not a gate failure).

## Decisions Made

Recorded in frontmatter `key-decisions`; the load-bearing ones: the owner's
verbatim "confirmed" contract freeze; `gate04_verdict` returning the verdict
string in the `gate_metrics.gate_verdict` convention; `INVALIDATION_TRIGGERS`
as exactly the fifteen named surfaces; `__all__` listing only this plan's
defined symbols.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 — Blocking] Renamed the `_measure_raw_bin_means` local `force` → `f_grav`**
- **Found during:** Task 2 acceptance-criteria loop
- **Issue:** the plan's own bypass-vocabulary acceptance grep (`grep -cE 'force|skip_gate|allow_block|ignore_verdict'` must return 0) counted 2 — the local variable holding `softened_acceleration`'s result (`force = ...`), the F_grav physics term.
- **Fix:** renamed the two references to `f_grav`. Pure identifier rename; zero semantic change (the artifact values were computed before the rename and are unaffected, since the rename cannot alter arithmetic).
- **Files modified:** `pinn/verification/gate04_train_free.py`
- **Verification:** both negative greps return 0; full phase56 suite re-run after the fix (12 passed, 0 skipped); phase55 suite still 46 passed.
- **Committed in:** `bbb572bc`

**2. [Rule 2 — Missing critical validation] `write_r_ref_artifact` refuses inconsistent or unidentified content**
- **Found during:** Task 2 implementation
- **Issue:** the plan specified serialization of the frozen key set through the atomic writer, but D-09 makes this artifact a governed, run-gating value; a writer that persists a verdict whose `r_ref` is not the median of the recorded means, or whose cases cannot be identified, would let a torn or hand-assembled object read as authoritative.
- **Fix:** the writer raises unless the verdict carries ≥1 case, every recorded bin mean is finite, `r_ref` equals `numpy.median` of the recorded means exactly, and every case matches exactly one `DEFAULT_CASES` entry by `(label, seed)` (enriching the record with masses/IC13 mode from the canonical definitions).
- **Files modified:** `pinn/verification/gate04_train_free.py`
- **Verification:** `RRefArtifactTests` exercises the writer end-to-end (frozen key set, 6×16 means, non-empty triggers, no temp residue); the real artifact passed the plan's schema assertion.
- **Committed in:** `bbb572bc`

**Total deviations:** 2 auto-fixed (1 Rule 3, 1 Rule 2). **Impact on plan:** none to scope or contract — both changes strengthen the plan's own fail-closed intent; every frozen name, field, path, and schema string is exactly as confirmed.

## Known Stubs

- `Gate04CaseResult.condition_ii_diagnostics` / `condition_iii_diagnostics` are present-but-`None`, and `Gate04Verdict.unratified_conditions == ("ii", "iii")` — **intentional, by design**: GAP-56-01 (condition (ii)'s pass criterion) is an OPEN owner gap this plan must not resolve. The slots are structurally present so 56-02 fills them without a schema change; the verdict docstring states plainly that a PASS with non-empty `unratified_conditions` is an INCOMPLETE result. No test is skipped and no `<verify>` was left unrun because of this.

## Issues Encountered

None beyond the deviations above. (STATE.md's standing caution — `gsd-tools` mutating verbs can emit malformed output in this checkout — was handled per the file's own hand-maintenance note; see the metadata commit.)

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- The frozen contract Phase 57's RUN-04 will import now exists, is tested, and is committed: `run_gate`, `gate04_verdict`, `Gate04Verdict`, `VERDICT_PASS`, `VERDICT_BLOCK`, and the governed `r_ref_stage0.json`.
- **Ready for 56-04** (wave-1 sibling: the §3.2 contract amendment) and for 56-02 (conditions (ii)/(iii) slots + CLI), which expands from this proven slice.
- GAP-56-01 and GAP-56-02 remain OPEN and untouched, as designed.
- Note for 56-02: this plan's `run_gate` measures each case twice (once in `compute_r_ref`, once in `evaluate_case`) — deterministic and exact, ~200s total at float64/cpu; the CLI should expect that cost.

---
*Phase: 56-contract-amendment-train-free-gate*
*Completed: 2026-09-06*

## Self-Check: PASSED

All five claimed files exist on disk (`pinn/verification/gate04_train_free.py`, `pinn/verification/artifacts/r_ref_stage0.json`, `tests/phase56/__init__.py`, `tests/phase56/test_gate04_train_free.py`, this SUMMARY); both commits exist in `git log --all` (`62f94880`, `bbb572bc`); the probe module contains `ratified_causal_weights` (definition + `__all__` entry).
