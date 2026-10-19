---
phase: "60"
slug: "single-system-learnability"
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: draft
nyquist_compliant: false
wave_0_complete: false
created: "2026-10-18"
---

# Phase 60 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
> It is seeded from `60-RESEARCH.md` "Validation Architecture". The planner
> binds each row to a task ID.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Python stdlib `unittest` (`TestCase` classes). `pytest` is not installed |
| **Config file** | None. New package `tests/phase60/`, created by the first plan that adds a test |
| **Quick run command** | `<home>/miniforge3/envs/pinn-train/bin/python -B -m unittest tests.phase60.<module> -v` |
| **Full suite command** | `<home>/miniforge3/envs/pinn-train/bin/python -B -m unittest discover -s tests/phase60 -t . -v` |
| **Adjacent regression** | `tests.phase39.test_prohibitions` (31 tests, about 0.9 s) and four named tests of `tests.phase38.test_prohibitions` (see the note below). The scorer-dependent Phase 59 suites, about 35 s together: `test_scorer_network`, `test_scorer_known_errors`, `test_baselines`, `test_diag07`, `test_diag07_panels`, `test_two_kepler`, `test_nn_copy`, `test_scorecard_rules` and `test_static_guards` |
| **Evidence verifiers** | `python .planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py final` (about 644 s, detached). The Phase 60 evidence verifier's `records`, `g2`, `rescore` and `final` subcommands |
| **Estimated runtime** | The unit suite is under about 60 s. Integration runs (the INST-05 (d) short run, refusals and resume) take 10–40 s each. Real arms take hours and are not part of any suite |

**Pre-existing failures (not regressions):** `tests.phase38.test_prohibitions`
has two tests that fail at HEAD for unrelated reasons:

- `test_spec_byte_identity_endpoint_sha256`
- `test_spec_history_no_touch_since_phase_base`

Both are stale spec byte checks, broken by later, legitimate spec amendments.
The gate is the other four tests:

- `test_discovered_modules_superset_of_known_phase38`
- `test_no_precision_default_in_discovered_modules`
- `test_no_v1_3_era_imports_in_discovered_modules`
- `test_write_spy_no_simulation_data_writes`

---

## Sampling Rate

- **After every task commit:**
  - Run the task's own test module.
  - If a `pinn/` module changed, also run `tests.phase39.test_prohibitions`.
- **After every plan wave:**
  - Run the full `tests/phase60` discovery.
  - Run the scorer-dependent Phase 59 suites.
  - Run the four named `tests.phase38.test_prohibitions` tests.
- **Before `/gsd-verify-work`:**
  - Run the full suite.
  - Run the Phase 60 evidence verifier's `final`.
  - Run Phase 59's `final` (detached, with its output retained).
  - Run both prohibition suites.
- **Max feedback latency:** about 60 s for unit tests.
- **Expensive commands** (over 60 s) run once, detached, with their full
  output retained outside the repository. That output is reused while the
  inputs are unchanged. The expensive commands are:
  - Phase 59's `final`;
  - `tests.phase59.test_evidence_verifier` (about 70 s);
  - `baselines --check` (about 66 s);
  - the D-07 re-measure;
  - every timing run and real arm;
  - every `rescore`.
- **Isolation:** no expensive command runs during a timing run or a real arm.

---

## Per-Task Verification Map

Requirement-level rows. The planner binds them to task IDs. Threat references
are bound in the plans' `<threat_model>` blocks.

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 60-03-01, 60-03-02 | 60-03 | 2 | SPEC R1 / GAP-60-01 | — | Each of the six amendment paragraphs is contained in its designated section, after NFC normalization and whitespace collapse. The scorecard SHA-256 equals `SCORECARD_SHA256` | unit | `... tests.phase60.test_amendment` | ❌ W0 | ⬜ pending |
| 60-02-01, 60-02-02 | 60-02 | 2 | SPEC R3 | — | `network_trajectory` runs on MPS float32 at all three widening sites. It is unchanged on CPU float64. No one-call widen remains | unit + static | `... tests.phase60.test_scorer_mps`; `tests.phase59.test_scorer_network`; `tests.phase59.test_diag07_panels` | ❌ W0 | ⬜ pending |
| 60-23-03 | 60-23 | 3 | INST-05 (b) | test-split exposure | A test-split key is refused before any path exists. There is no raw-path input. The attestation shows zero test opens | unit | `... tests.phase60.test_arm_spec`; `... test_data_seam` | ❌ W0 | ⬜ pending |
| 60-23-01, 60-23-02 | 60-23 | 3 | INST-05 (e) | unauthorized setting | An override is refused on any arm with a physics term. A non-30 `first_omega_0` is legal only on a data-only grid arm, or as the value named by the committed ruling | unit | `... tests.phase60.test_arm_spec` | ❌ W0 | ⬜ pending |
| 60-01-01 | 60-01 | 1 | INST-05 (d) | evidence overwrite | A short fixture run goes through Adam and the polish and scores both states. The record is valid and created exclusively, and is marked as a fixture, not a Rung-1 result | integration | `... tests.phase60.test_run_short` | ❌ W0 | ⬜ pending |
| 60-05-01, 60-05-02 | 60-05 | 4 | INST-05 (a) | — | Mutating each trainer function scales the harness output by the mutation factor. The function objects are the trainer's own. Per-term loss and `.grad` equal `RunController._run_adam_step_microbatched` on the stub source (CPU float64) | unit | `... tests.phase60.test_losses_trainer_functions` | ❌ W0 | ⬜ pending |
| 60-01-01, 60-23-01 | 60-01, 60-23 | 1, 3 | INST-05 (c) | record spoofing | `evaluate_run` and the production checkpoint load both refuse harness artifacts, including an override record. No `evaluation-attempt.json` appears | integration | `... tests.phase60.test_refusals` | ❌ W0 | ⬜ pending |
| 60-04-01, 60-04-02 | 60-04 | 3 | D-09 / GAP-60-02 | hash drift | The verifier accepts exactly one successor digest for one path. Other mismatches, a second successor, and an untracked or dirty record all fail | unit | `... tests.phase60.test_verifier_successor` | ❌ W0 | ⬜ pending |
| 60-04-03 (reused or re-run by 60-22-01) | 60-04 | 3 | D-09 end to end | — | Phase 59 evidence verifies at HEAD after the scorer edit | e2e (detached) | `python .planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py final` → `PHASE59-EVIDENCE-OK` | ✅ | ⬜ pending |
| 60-08-02 | 60-08 | 7 | D-01..D-05, GAP-60-03 | — | Checks: the `LR_k` values; cosine length B; warmup `min(2000, floor(0.1 B))`; no re-ramp past B; the second cosine equals the first; data-only arms use k = 0; probes use `LR_4` and `LR_6`; the clipper runs during Adam only, at the arm's stage | unit | `... tests.phase60.test_schedule` | ❌ W0 | ⬜ pending |
| 60-05-02, 60-11-01 | 60-05, 60-11 | 4, 10 | D-06 | memory exhaustion | A physics arm never halts on a causal-front rule. The frozen monitor is evaluated only at readings, in chunks of at most 256 rows | unit | `... tests.phase60.test_losses_trainer_functions` | ❌ W0 | ⬜ pending |
| 60-09-01, 60-09-02 (real run 60-19-02) | 60-09 | 8 | D-07 | governed artifact overwrite | The omega seam's default path leaves `r_ref_stage0.json` and existing behavior unchanged. A re-measure writes only to a Phase 60 path and never writes `terminal-state.json`. A BLOCK result stops | unit | `... tests.phase60.test_gate04_remeasure` | ❌ W0 | ⬜ pending |
| 60-08-01, 60-08-03 | 60-08 | 7 | SPEC R4, R5; GAP-60-04..06 | — | The budget driver: B comes from the timing run; cadence; complete, extend, inconclusive or diverged. It propagates `OwnerRouted`. Tier edges: E = 0.1 is Tier 1, non-finite E is Tier 0, and a non-finite `ε_H` caps the tier at 1. Polish improvement uses the objective; the polish state is the final iterate | unit | `... tests.phase60.test_budget_driver` | ❌ W0 | ⬜ pending |
| 60-23-03, 60-12-01, 60-12-02 | 60-23, 60-12 | 3, 11 | SPEC R8 | silent restart | Preflight blocks a missing, empty or unreadable record with no fallback. Resume keeps B, sums Adam time, and refuses a missing segment state or changed module digests | unit | `... tests.phase60.test_preflight`; `... test_resume` | ❌ W0 | ⬜ pending |
| 60-06-01, 60-06-02 | 60-06 | 5 | SPEC R6, R7; GAP-60-09 | — | Four sweep-pair cases. The confirmation is the highest Tier ≥ 1 setting; with none, there is no confirmation. A rescue raises and is not caught. A failed confirmation stops for the owner. The skip writer accepts only the two exact reasons and refuses once any Rung-2 arm has a state file. Probes never call `counts()`. `decision_verdict` gets no later-rung inputs on a stop | unit | `... tests.phase60.test_g2` | ❌ W0 | ⬜ pending |
| 60-11-02, 60-11-03, 60-10-02 | 60-11, 60-10 | 10, 9 | D-08, D-10, D-11, SPEC R4; GAP-60-07, -08, -10..-13 | ruling-file tampering | The record validator rejects any missing hash or version field. Weights use `.weights` and are digest-recorded. The ruling loader accepts only a tracked, clean file with a strict machine block. The probe record names the reference in force, `S_H`, and the normalizer digest | unit | `... tests.phase60.test_protocol_records` | ❌ W0 | ⬜ pending |
| 60-01-02 (rerun by every pinn plan) | 60-01 | 1 | Static | unsafe deserialization | Each new module's docstring begins "Phase 60". Loads use the literal `torch.load(..., weights_only=True)`. No evaluator or trainer-loop import, no corpus folder token, no `is_available`, and no `except OwnerRouted` | static | `... tests.phase60.test_static_guards`; `tests.phase39.test_prohibitions`; four named `tests.phase38.test_prohibitions` tests | ❌ W0 | ⬜ pending |
| 60-13-01, 60-14-04, 60-15-04, 60-16-04, 60-18-02, 60-19-03, 60-20-04, 60-21-04, 60-22-01 | 60-13..60-22 | 12-21 | FEAS-03, FEAS-04, FEAS-09 | — | Per real arm: the record is complete; attestation counts are zero; seed 42; the protocol and scorer SHA-256 match; the committed weights re-score to the recorded tier and `E`; `g2_fires` reproduces the recorded outcome | verifier | Phase 60 evidence verifier `records`, `g2`, `rescore`, `final` | ❌ W0 | ⬜ pending |
| 60-02-03 | 60-02 | 2 | Wave 0 / Assumption A1 | — | torch.optim.LBFGS with strong Wolfe, history 10 and max_iter 50 runs on MPS float32 (tiny and production network), stays finite, and its state_dict round-trips with weights_only=True; a failure stops for the owner | smoke | `... tests.phase60.test_mps_lbfgs_smoke` | ❌ W0 | ⬜ pending |
| 60-06-03 | 60-06 | 5 | D-11, GAP-60-09, GAP-60-11 | ruling-file tampering | The ruling loaders parse only one strict phase60-ruling block, keep the owner quote opaque, refuse untracked or dirty files and malformed values, and the branch table covers owner-decision, continue-gate and ladder | unit | `... tests.phase60.test_ruling`; `... tests.phase60.test_g2` | ❌ W0 | ⬜ pending |
| 60-07-01, 60-07-02 | 60-07 | 6 | SCOPE-44, SPEC R8 | silent restart | The detached supervisor runs one closed sequence one arm at a time, records every exit, resumes only after 129, 130 or 143, and survives a hangup and kill of the launching process group | integration | `... tests.phase60.test_launcher` | ❌ W0 | ⬜ pending |
| 60-10-01 | 60-10 | 9 | SPEC R4 | protocol drift | The run protocol is built from code constants and frozen inputs, round-trips, and refuses drift in any pinned module | unit | `... tests.phase60.test_protocol` | ❌ W0 | ⬜ pending |
| 60-10-02 | 60-10 | 9 | SPEC R8; D-08, D-11 | branch spoofing | The preflight writer blocks arms without substitution; admission enforces the branch, the uncovered system, the ruling value, skip records and the R_ref in force | unit | `... tests.phase60.test_admission` | ❌ W0 | ⬜ pending |
| 60-11-01 | 60-11 | 10 | D-01, D-05, D-06, GAP-60-05, GAP-60-12 | memory exhaustion | A fixture physics arm runs the warmup schedule, per-step collocation, the frozen monitor at readings, and the frozen-handoff polish | integration | `... tests.phase60.test_physics_arm` | ❌ W0 | ⬜ pending |
| 60-11-02 | 60-11 | 10 | SPEC R3, GAP-60-07 | score substitution | A tier or counts difference between the MPS score and the CPU float64 cross-check stops for the owner; probes never call counts() | unit | `... tests.phase60.test_cross_check` | ❌ W0 | ⬜ pending |
| 60-12-02 | 60-12 | 11 | SPEC R8, SCOPE-44 | concurrent arms | The command line takes only an arm id with --resume or --admit-only, admits first, holds the one-launch lock, writes process.json and maps owner-routed results to exit 3 without retry | unit + subprocess | `... tests.phase60.test_cli`; `... tests.phase60.test_resume` | ❌ W0 | ⬜ pending |
| 60-13-02, 60-13-04 | 60-13 | 12 | SPEC R4, R8 | pre-registration breach | The preflight and the run protocol are committed before any evidence/arms file, verified, and the Rung-1 arms are admitted | verifier | `verify_phase60_evidence.py preflight`; `verify_phase60_evidence.py protocol` | ❌ W0 | ⬜ pending |
| 60-13-03 | 60-13 | 12 | GAP-60-03, GAP-60-09; SCOPE-42 | pre-registration breach | Before the run protocol is committed, the owner keeps or vetoes gradient clipping in the data-only arms and pre-answers GAP-60-09 or leaves it open, in their own words; an unclear reply is asked again; the reply reaches the protocol only through the two write flags and is quoted verbatim in 60-RUN-PROTOCOL.md and the commit body | manual | owner reply recorded verbatim in the 60-13 SUMMARY | ✅ | ⬜ pending |
| 60-15-01, 60-16-01, 60-17-01, 60-18-01, 60-19-01, 60-20-01, 60-21-01 | 60-15..60-21 | 14-20 | Orchestrator constraint 5 | branch spoofing | Each conditional plan opens with the read-only branch query; NOT-TAKEN writes and commits a 'branch not taken' SUMMARY and ends cleanly; PENDING stops | cli | `python -B -m pinn.verification.learnability_g2 branch <name>` | ❌ W0 | ⬜ pending |
| 60-17-03 | 60-17 | 16 | D-11 | ruling-file tampering | The checkpoint ④ (and GAP-60-09) ruling is committed from the owner's words and selects exactly one of the stop and continue-gate branches | cli | committed-loader check printing RULING-OK; `learnability_g2 branch stop` and `branch continue-gate` | ❌ W0 | ⬜ pending |
| 60-22-02, 60-22-03 | 60-22 | 21 | SPEC R8 | — | 60-FINDINGS.md reports every arm's machine hours and seconds per step and the one-seed limit; progress marks change no requirement text | doc + unit | heading checks; `... tests.phase60.test_amendment` | ❌ W0 | ⬜ pending |
| 60-14-01 | 60-14 | 13 | SCOPE-44, SPEC R4 | — | The Rung-1 window is admitted on the sealed protocol (PROTOCOL-OK, PREFLIGHT-OK, SCORECARD-FROZEN-OK, three ADMIT-OK) with nothing else heavy running | cli | `verify_phase60_evidence.py protocol`; `launch_phase60_arm.py --sequence rung1 --dry-run` | ❌ W0 | ⬜ pending |
| 60-14-03, 60-15-03, 60-16-03, 60-20-03, 60-21-03 | 60-14..60-21 | 13-20 | SCOPE-44 | silent restart | Each sequence launches detached and returns at once; --status shows SEQUENCE-RUNNING with the arm's own PID | cli | `launch_phase60_arm.py --sequence <name> --status` | ❌ W0 | ⬜ pending |
| 60-14-02, 60-14-04, 60-15-02, 60-15-04, 60-16-02, 60-16-04, 60-17-02, 60-20-02, 60-20-04, 60-21-02, 60-21-04 | 60-14..60-21 | 13-20 | SCOPE-44; FEAS-03 checkpoint ④ | memory exhaustion | Owner memory confirmations (task 02 of 60-14, 60-15, 60-16, 60-20 and 60-21), checkpoint ④ (60-17-02), and the completion waits, which are the blocking-human wait stop inside task 04 of those five plans (its precondition: the status shows the sequence ended and the owner replied "finished"; see Manual-Only Verifications) | manual | owner reply recorded verbatim in each SUMMARY | ✅ | ⬜ pending |
| 60-18-03 | 60-18 | 17 | SPEC R8 | — | On a stop at G2, Phases 61-63 are marked skipped at G2 (not failed) and Phase 64 is next, by hand edits only | cli | marks count and `git diff --quiet` on ROADMAP.md and STATE.md | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/phase60/__init__.py` and the test modules named above.
- [ ] Reused fixtures, imported and not copied:
  - the tiny corpus (`tests/phase59/_corpus_fixtures.py`);
  - the stub `RunController` (`tests/phase57/_fixtures.py::build_run_controller`);
  - the rigid orbits (`tests/phase59/_fixtures.py`).
- [ ] An MPS smoke for `torch.optim.LBFGS` (strong Wolfe) on a tiny network
  before any real arm. No repository test or committed run has exercised
  L-BFGS on MPS yet (`60-RESEARCH.md` Assumption A1).
- [ ] A fixture-vs-real marker in every record, so a fixture run can never be
  mistaken for a rung result.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Free memory before each long arm | SCOPE-44; CONTEXT discretion | The footprint preflight is unreliable on this macOS (`tests/phase57/test_resource_preflight.py`). The arm needs 6 GiB free; 4.63 GiB was available at research time | The owner closes browsers (Chrome, ChatGPT) and confirms that no other heavy job is running. The executor logs `evidence_io.available_memory_bytes()` as advisory |
| Checkpoint ④ answer | FEAS-03; D-11 | The owner's decision | The owner answers in their own words. The ruling file quotes them and names the approved `first_omega_0`. It is committed before any continue-path arm |
| A failed G2 confirmation, if it occurs | GAP-60-09 | The owner's decision; it could pre-empt the verdict | The phase stops. The owner reads the sweep curve and the confirmation record and decides whether it counts as a rescue or as no rescue |
| Detached long arms complete | FEAS-03, FEAS-04, FEAS-09 | They run for hours, outside any test run | Launch detached. Check completion in a later session and verify the record with the Phase 60 evidence verifier |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 60s for unit tests
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
