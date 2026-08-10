---
phase: 49-conformance-gate
verified: 2026-08-10T09:38:31Z
status: gaps_found
score: 4/6 must-haves verified
behavior_unverified: 0
overrides_applied: 0
gaps:
  - truth: "An EVAL-01-eligible run enforces invariant B with the owner-ratified N = 500; an N-unset run remains ineligible."
    status: failed
    reason: "The shipped record-only state (run.invariants.front_advance_window_n = None) no longer carries INV-B-N-UNSET as an open divergence after the global register entry was closed. A real synthetic main() run with N unset finished with eval01_precondition_i = true, even though invariant B was record-only."
    artifacts:
      - path: "configs/smoke.yaml"
        issue: "Shipped config intentionally leaves front_advance_window_n unset."
      - path: "pinn/conformance/divergence_register.json"
        issue: "INV-B-N-UNSET is globally closed, independent of the run-local config."
      - path: "pinn/conformance/preflight.py"
        issue: "The config/register mismatch is only a non-blocking finding; the accessor also reads config.invariants instead of config.run.invariants."
      - path: "pinn/training/summary.py"
        issue: "_eval01_precondition_i ignores the run-local invariant-B setting and consistency findings."
    missing:
      - "Bind EVAL-01 precondition (i) to the run-local owner-ratified invariant-B window, or preserve an open run-local INV-B-N-UNSET divergence whenever N is absent."
      - "Add a real-main regression proving N=None produces eval01_precondition_i = false after the global register entry is closed."
      - "Read the actual TrainingConfig path (config.run.invariants.front_advance_window_n) when recording consistency evidence."
  - truth: "EVAL-01 eligibility can be true only when the artifact proves the run-start PHYS-05 table and census actually executed."
    status: failed
    reason: "The preflight loader accepts a passed assertion stream whose first and only event is stage_boundary with census = null. _eval01_precondition_i then returns true because it checks only non-empty/all-passed events and open divergences, not the required run_start event or census evidence."
    artifacts:
      - path: "pinn/conformance/preflight.py"
        issue: "_validate_payload validates event shapes but not required run_start presence or event-stream semantics."
      - path: "pinn/training/summary.py"
        issue: "_eval01_precondition_i accepts any non-empty all-passed assertion list."
      - path: "tests/phase49/test_preflight_integrity.py"
        issue: "No regression covers a stage_boundary-only passed artifact or missing run-start census evidence."
    missing:
      - "Fail closed unless the assertion history begins with a passed run_start event carrying the required locked table checks and a passed census."
      - "Define and validate legal append-only resume ordering without allowing a history that never contains run_start evidence."
      - "Add a regression proving a stage_boundary-only artifact cannot make eval01_precondition_i true."
---

# Phase 49: Conformance Gate Verification Report

**Phase Goal:** A preflight + runtime gate exists that makes an invalid run structurally unable to spend the single look — the minimum enforcement subset, coordinated with the charter workstream.

**Verified:** 2026-08-10T09:38:31Z

**Status:** gaps_found

**Re-verification:** No — initial verification

## Goal Achievement

The table, census, runtime guards, checkpoint continuity, register, and real `main()` composition all exist and have passing behavioral evidence. The phase goal is nevertheless not achieved: two independent disconfirmation probes made `eval01_precondition_i` true without all required run-local evidence.

### Observable Truths

The five roadmap success criteria were merged with the plan-specific structural eligibility seam into six non-overlapping outcome truths.

| # | Truth | Status | Evidence |
|---|---|---|---|
| 1 | The full PHYS-05 per-stage table is asserted at run start and every stage boundary. | ✓ VERIFIED | `pinn/constants.py` → `pinn/conformance/table.py` → `run_start_preflight` and `CurriculumController.conformance_hook` are wired. Three named integration tests passed, including run start, ordered boundaries, and deliberate Stage-2 refusal. |
| 2 | The placeholder census resolves every required loss quantity through concrete producers or blocks/names an explicit waiver. | ✓ VERIFIED | `CENSUS_MANIFEST` has 28 ordered entries; the real-main seam carries a passed census. Named real-producer/pass and placeholder-block tests both passed. |
| 3 | Runtime invariants fail loud and early, including front advancement within the owner-ratified N for every eligible run. | ✗ FAILED | Invariant A/B, causal-stat-missing, and resume mechanics pass named tests, but a real `main()` run with `N=None` was record-only and still emitted `eval01_precondition_i=True`. |
| 4 | The known-divergence register is maintained and every open entry is surfaced in the run record. | ✓ VERIFIED | The validated 16-entry register has 11 closed proof-backed entries and three open qualifications. Run-start preflight copies all open entries, and the summary projects the payload verbatim. The composed-register, summary-surface, and executable-proof tests passed. |
| 5 | The SCOPE-32 coordination decision is recorded without duplicating the charter's general regime. | ✓ VERIFIED | `49-CONTEXT.md` D-31/D-32 and `49-01-PLAN.md` record that only the charter existed, so Phase 49 implemented the narrow `pinn/conformance/` subset. Current inspection still finds only the charter in the workstream directory. |
| 6 | Eligibility proves the required run-start gate actually ran; a shaped but incomplete artifact cannot claim conformance. | ✗ FAILED | A schema-valid, passed, `stage_boundary`-only artifact with `census=null` loaded successfully and `_eval01_precondition_i` returned `True`. |

**Score:** 4/6 truths verified (0 present, behavior-unverified)

## Required Artifacts

| Artifact | Expected | Status | Details |
|---|---|---|---|
| `pinn/constants.py` | Canonical seven-stage PHYS-05 literals | ✓ VERIFIED | Exact table, locked `lambda_data`, advisory `lambda_ic`, and warmup constants are substantive and consumed by `table.py`. |
| `pinn/conformance/table.py` | Exact table assertion | ✓ VERIFIED | Reads live `ScheduledWeights.state_dict()`, rejects missing/malformed values, uses exact equality, and is called at both required sites. |
| `pinn/conformance/preflight.py` | Atomic fail-closed evidence spine | ⚠️ PARTIAL | Real-path composition and failure-first persistence are substantive, but payload semantics do not require run-start evidence and run-local N mismatch is non-blocking. |
| `pinn/conformance/census.py` | Explicit producer-backed placeholder census | ✓ VERIFIED | 28-entry manifest traces into real controller/model/data producers; unresolved placeholders and malformed producer values block. |
| `pinn/conformance/register.py` and `divergence_register.json` | Validated divergence register with proof-backed closure | ✓ VERIFIED | Schema/proof resolution is wired into run-start preflight; all closed proof nodes passed the meta-test. |
| `pinn/training/guards.py` | Invariants A/B and missing-stat HALTs | ✓ VERIFIED | Guard logic is substantive, wired through the real controller hook, and named transition tests pass. |
| `pinn/training/checkpoint.py` and `pinn/training/controllers.py` | Invariant-B state persistence and stage-boundary dispatch | ✓ VERIFIED | Schema-v2 state is saved/restored; boundary and resume transitions pass named tests. |
| `pinn/training/summary.py` | Verbatim conformance projection and fail-closed EVAL-01 fact | ⚠️ PARTIAL | Projection is wired, but eligibility does not require run-start/census evidence or the run-local N setting. |
| `pinn/train.py` | Production composition root | ✓ VERIFIED | Builds real controller and guards, invokes run-start preflight before curriculum/resume, and wires boundary/guard/checkpoint hooks. |
| `tests/phase49/test_e2e_seam.py` | Real synthetic `main()` ordering seam | ✓ VERIFIED | Passed independently (`1 passed in 3.14s`). |
| `tests/phase49/_fixtures.py` | Optional shared fixture module | N/A | Plan 49-06 explicitly says “created only if the seam test needs shared fixtures”; the seam uses local helpers and passes without it. |

## Key Link Verification

| From | To | Via | Status | Details |
|---|---|---|---|---|
| `pinn/constants.py` | `pinn/conformance/table.py` | `PHYS05_*` imports and exact comparisons | ✓ WIRED | No `isclose`, `allclose`, or absolute-difference tolerance exists. |
| `pinn/conformance/table.py` | `pinn/train.py` / `pinn/training/controllers.py` | run-start call and stage-boundary closure | ✓ WIRED | Named run-start/boundary/refusal tests passed. |
| `pinn/conformance/census.py` | real `RunController` producers | `run_start_preflight(..., controller=run_controller)` | ✓ WIRED | Real-main seam and concrete-producer census test passed. |
| `run.invariants.front_advance_window_n` | `StepGuards` | `_extract_invariant_window` | ✓ WIRED | Enforcing N=500 branch trips; record-only N=None branch is also reachable. |
| `StepGuards` | checkpoint payload | `invariant_b_state_dict` / restore | ✓ WIRED | Trip and cross-resume continuity tests passed. |
| divergence register | `preflight.json` | `load_divergence_register` → run-start `open_divergences` | ✓ WIRED | Open entries are copied and projected in the run record. |
| `preflight.json` | EVAL-01 precondition (i) | `_eval01_precondition_i` | ✗ NOT FAIL-CLOSED | Run-local N and required run-start/census semantics are not checked; both bypass probes returned `True`. |

## Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
|---|---|---|---|---|
| PHYS-05 assertion | scheduler state | live `ScheduledWeights.state_dict()` | Yes | ✓ FLOWING |
| Census | 28 manifest quantities | live config, metadata, controller batches/model/collocation/anchor/loss producers | Yes | ✓ FLOWING |
| Runtime invariants | `w_n_stats`, `front_idx`, `n_colloc` | controller's widened loss details → `guard_hook` → `StepGuards.check` | Yes | ✓ FLOWING |
| Invariant-B resume state | initialized/high-water/last-advance fields | `StepGuards` → checkpoint schema v2 → restore | Yes | ✓ FLOWING |
| Run record | `conformance`, `eval01_precondition_i` | validated `preflight.json` | Partly | ⚠️ HOLLOW AT ELIGIBILITY SEAM — artifact contents flow, but the predicate accepts incomplete semantics. |
| N/register consistency | `front_advance_window_n` | intended `TrainingConfig.run.invariants` | No | ⚠️ MISREAD — `_consistency_finding` reads `config.invariants`; even the N=500 shipped config is reported as `config_value: None`. |

## Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|---|---|---|---|
| Complete Phase 49 suite | `.venv/bin/python -m pytest -q tests/phase49` | `176 passed in 13.18s` | ✓ PASS |
| Real production composition seam | `.venv/bin/python -m pytest -q tests/phase49/test_e2e_seam.py` | `1 passed in 3.14s` | ✓ PASS |
| Run-start, ordered boundaries, Stage-2 refusal | `.venv/bin/python -m pytest -q tests/phase49/test_gate01_table.py::EntrypointTests::test_run_start_writes_passed_preflight_artifact tests/phase49/test_gate01_table.py::test_controller_stage_boundary_events_follow_entered_order tests/phase49/test_gate01_table.py::test_stage2_fails_without_rebound_scheduler` | `3 passed in 3.36s` | ✓ PASS |
| Concrete census and placeholder refusal | `.venv/bin/python -m pytest -q tests/phase49/test_gate02_census.py::test_census_passes_with_real_manifest_and_validated_metadata tests/phase49/test_gate02_census.py::test_placeholder_blocks_without_explicit_waiver` | `2 passed in 0.90s` | ✓ PASS |
| Invariant-B trip and resume continuity | `.venv/bin/python -m pytest -q tests/phase49/test_gate03_invariants.py::test_invariant_b_trips_after_window_and_marks_threshold_nonprovisional tests/phase49/test_gate03_resume.py::test_restore_preserves_stall_window_across_resume_boundary` | `2 passed in 0.40s` | ✓ PASS |
| Invariant-A and causal-stat-missing HALTs | `.venv/bin/python -m pytest -q tests/phase49/test_gate03_invariants.py::test_invariant_a_trips_on_zero_and_nonfinite_weight_stats tests/phase49/test_gate03_invariants.py::test_guard_hook_wiring_stripped_stats_trips_causal_stats_missing` | `2 passed in 0.67s` | ✓ PASS |
| Register composition, run-record projection, all closure proofs | `.venv/bin/python -m pytest -q tests/phase49/test_inst03_register.py::test_preflight_composes_census_and_every_open_register_entry tests/phase49/test_inst03_register.py::test_surfaces_in_run_record tests/phase49/test_inst03_register.py::test_every_closed_register_entry_has_a_real_passing_proof_test` | `3 passed in 9.12s` | ✓ PASS |
| No Phase-46 key collision | `.venv/bin/python -m pytest -q tests/phase49/test_inst03_register.py::test_no_gate_collision_in_preflight_and_register_payload` | `1 passed in 0.83s` | ✓ PASS |
| N-unset real-main disconfirmation | `.venv/bin/python - <<'PY'` (write the Phase-49 synthetic config, set `run.invariants={}`, invoke `pinn.train.main`, load summary/preflight) | `exit_code=0`, `N=None`, `INV-B-N-UNSET open=False`, `eval01_precondition_i=True` | ✗ FAIL |
| Missing-run-start disconfirmation | `.venv/bin/python - <<'PY'` (write a schema-v1 passed artifact containing only one `stage_boundary` event, then call `load_preflight` and `_eval01_precondition_i`) | `has_run_start=False`, `eval01_precondition_i=True` | ✗ FAIL |

The long 448-second cross-phase command documented in `49-VALIDATION.md` was not re-run; that document's prior green claim was not used to override either independently reproduced blocker.

## Probe Execution

| Probe | Command | Result | Status |
|---|---|---|---|
| Phase-declared shell probes | `find scripts -path '*/tests/probe-*.sh' ...` plus PLAN/SUMMARY search | No Phase 49 `probe-*.sh` path declared or discovered | N/A |

## Requirements Coverage

| Requirement | Source Plan(s) | Description | Status | Evidence |
|---|---|---|---|---|
| GATE-01 | 49-01, 49-06, 49-07, 49-08 | Full PHYS-05 table at run start and every boundary | ✓ SATISFIED | Both production sites are wired and named pass/trip tests pass. |
| GATE-02 | 49-04, 49-06, 49-08 | Producer-backed placeholder census | ✓ SATISFIED | 28-entry real-producer census passes; placeholder and malformed-producer paths block. |
| GATE-03 | 49-02, 49-03, 49-06, 49-07 | Invariants A/B, owner N, resume continuity | ✗ BLOCKED | Guard machinery works, but N-unset remains record-only while the run can report EVAL-01 precondition (i) true. |
| INST-03 | 49-04, 49-05, 49-06, 49-07, 49-08 | Known-divergence register surfaced in every run record | ✓ SATISFIED | Validated register flows into run-start evidence and summary; proof meta-test passes. |

No orphaned Phase 49 requirement was found: ROADMAP/REQUIREMENTS and all plan frontmatter map exactly GATE-01, GATE-02, GATE-03, and INST-03.

## Prohibition Checks

| Prohibition | Status | Evidence |
|---|---|---|
| Do not reuse Phase-46 `gate_*` keys | ✓ VERIFIED | Dedicated recursive collision test passed. |
| Do not weaken exact table equality | ✓ VERIFIED | Source search found no `isclose`, `allclose`, or `abs(` tolerance in `table.py`; one-ULP trip test is in the green suite. |
| Do not implement Stage-1+ platform work or hide Stage-2 refusal | ✓ VERIFIED | No stage factory was added to make Stage 2 conform; the explicit refusal test passed. |
| Do not invent or adjust the owner-selected N | ✓ VERIFIED | `configs/stage0-example.yaml` retains the recorded N=500 ruling. |
| Do not contact the admitted corpus or held-out evaluator | ✓ VERIFIED | All executed checks used synthetic/temp data; Phase 49 code does not invoke `pinn.evaluate`. |

## Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|---|---:|---|---|---|
| `pinn/conformance/preflight.py` | 384 | Wrong config path in `_consistency_finding` | ⚠️ Warning | Reads `config.invariants` rather than `config.run.invariants`; an explicit check showed the shipped N=500 config reported `config_value: None`. |
| `pinn/conformance/preflight.py` | 305 | Partial read-error normalization | ⚠️ Warning | `FileNotFoundError` and JSON decode are normalized, but other I/O/Unicode failures retain native exceptions (known review WR-02); summary catches them fail-closed. |
| Phase-modified files | — | `TBD` / `FIXME` / `XXX` debt markers | None | No unreferenced blocker marker found. Test-only “not available” failure messages are not stubs. |

## Human Verification Required

None. The two blocking failures are deterministic and reproduced programmatically; the remaining observable truths have direct behavioral evidence.

## Deferred-Item Check

Phases 50–52 were checked. None explicitly owns repairing run-local N binding or preflight event-stream integrity. Phase 51 consumes precondition (i), so these defects cannot be conservatively deferred to it.

## Gaps Summary

Two related integrity gaps leave the phase goal unmet:

1. The owner-ratified invariant-B decision is stored globally in the divergence register, while enforcement is configured per run. Once the global entry is closed, a run may omit N, execute record-only, and still appear eligible.
2. Eligibility trusts a shape-valid assertion list without proving it contains the mandatory run-start table and census event. A `stage_boundary`-only artifact is enough to obtain `True`.

Both gaps sit at the same critical seam: translating real gate evidence into the EVAL-01 precondition-(i) fact. Passing subsystem and end-to-end happy-path tests do not falsify either negative case.

---

_Verified: 2026-08-10T09:38:31Z_

_Verifier: the agent (gsd-verifier)_
