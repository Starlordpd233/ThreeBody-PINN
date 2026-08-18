---
phase: 50-valid-stage-0-re-run
verified: 2026-08-15T03:42:00Z
status: gaps_found
score: 2/4 must-haves verified
behavior_unverified: 0
decision_coverage:
  honored: 0
  total: 28
  not_honored: []
  note: "Non-blocking parser warning — check.decision-coverage-verify returned reason could-not-parse on two wrapped D-03/D-07 bullets."
---

# Phase 50: Valid Stage-0 Re-Run Verification Report

**Phase Goal:** Stage-0 runs end-to-end under the corrected recipe — the first run that is actually the specified experiment.
**Verified:** 2026-08-15T03:42:00Z
**Status:** gaps_found

Tasks completed. The specified experiment did not. Generation 3 is an honest terminal record after seed 41 HALTed on invariant B at step 501. Seeds 42 and 43 were never launched. `final_band_generation` is null. GAP-50-03 Option A accepts that HALT as the durable record; it does not rewrite ROADMAP success criteria 2 or 3, and it does not discharge RUN-01 or RUN-02.

## Goal Achievement

ROADMAP success criteria are the contract and override PLAN-level `must_haves` when both exist. The four truths below are those criteria.

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | Preflight is clean with zero unwaived divergences at run start and across stage boundaries (RUN-01). | ✓ VERIFIED | Generation-3 smoke and seed 41 both wrote `preflight_status=passed`. Seed 41 `summary.json` has `eval01_precondition_i=true`. Open register entries that travel with the run are `kind: qualification` (`STAGE0-BUDGET-DELTA`, `VALIDATION-TRAIN-RNG-COUPLING`, `VALIDATION-SNAPSHOT-RESAMPLING`) and do not enter `evaluate_eval01_precondition_i`. No Stage-0 `ADVANCE` occurred, so no stage-boundary preflight event exists to fail; that absence is a consequence of truth 2, not a dirty preflight. |
| 2 | Invariants A/B hold for a full run — no causal weight exactly zero, the causal front advances within N steps (RUN-01). | ✗ FAILED | The only graded launch, generation-3 seed 41 attempt 2, HALTed at step 501. `evidence/attempts/stage0-rerun-seed41-attempt-02/failure/trip.json` records `guard=invariant_b`, `disposition=HALT`, `metric=steps_since_front_advance`, `threshold=500.0`, `threshold_provisional=false`, `reason="causal front high-water mark did not advance within N=500 steps"`. Ledger reason: `front_idx=0` on all 502 logged steps. `disposition` in `summary.json` is `failed`. No 1000-step finished graded run exists. D-20 / GAP-50-03 Option A correctly forbids changing `N`; they do not convert the HALT into a held invariant. |
| 3 | Validation ε_H is recorded and characterized across three seeds, re-establishing the three-seed band matching the v2.0 protocol so the runs are comparable (RUN-02). | ✗ FAILED | `final_band_generation` is null. `in_final_band` count is 0. `runs/stage0-rerun-seed42` and `runs/stage0-rerun-seed43` do not exist. `evidence/band-record.md` and `evidence/candidate-receipt.json` do not exist (50-03 terminal branch; `TERMINAL-EVIDENCE-OK`). D-16 (`s_h` / `n_train` smoke vs seed 42) is undischarged. Even the launched seed did not record validation ε_H: `runs/stage0-rerun-seed41/validation.jsonl` has five events with `gate_status=failed:TypeError` and no `gate_eps_h`; `validation_gate/` is absent; `summary.validation` is `None`; `eval01_precondition_iii` is absent. Train-split `training_metadata.eps_h=0.002197…` is not the validation characterization this criterion names. |
| 4 | Every iteration inside the phase is conformance-only — no hyperparameter adjusted against observed results (SCOPE-29). | ✓ VERIFIED | C-09 repaired a spec divergence (`ctl_instruction.md` training-batch vs held-out validation set) without setting any constant from the observed 227. Graded `stage.replay_count` remains unset (DATA-05 default 240). `front_advance_window_n` remains 500. GAP-50-03 Option A accepted the HALT and forbade changing `N`, launching 42/43 at this head, or opening a new generation without a separate owner authorization. 50-03 did not synthesize a partial band. |

**Score:** 2/4 truths verified (0 present, behavior-unverified)

### Why GAP-50-03 Option A is not a pass

Owner ruling 2026-08-15, Option A: accept the generation-3 HALT record; no band; seeds 42/43 stay unlaunched; `N=500` unchanged; 50-03 stays on its terminal branch; no later generation until separately authorized.

That ruling is the correct D-20 response. It is **not** a redefinition of the phase goal. ROADMAP still requires a full run on which invariants A/B hold and a three-seed validation-ε_H band. Those statements are false on the shipped evidence. Closing Phase 50 as passed would treat an honest stop as experiment completion.

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `pinn/train.py` / `pinn/training/controllers.py` | `--stage-0-only` ceiling + C-09 `_validation_batch` | ✓ EXISTS + SUBSTANTIVE + WIRED | `stage_0_only` CLI rejects `--resume`. Guarded ADVANCE persists `stage-0-final` and returns before Stage-1 side effects. `_run_validation` calls `_validation_batch`, not `_stage_batch`. |
| `pinn/data/batches.py::select_validation_records` | Full held-out Stage-≤k pool, no sample / no lookahead | ✓ EXISTS + SUBSTANTIVE + WIRED | Signature is `(source, *, stage)`. Source contains neither `_sample_keys` nor `has_stage`. |
| `pinn/data/types.py::ValidationPoolEmpty` | Empty-pool fail-closed | ✓ EXISTS + SUBSTANTIVE | Used by the selector; covered by `test_empty_validation_pool_raises_validation_pool_empty`. |
| `tests/phase50/test_validation_full_pool.py` | C-09 proof suite | ✓ EXISTS + SUBSTANTIVE | 7/7 passed (2026-08-15). No skipped tests. |
| `configs/stage0-rerun-smoke.yaml` and `configs/stage0-rerun-seed{41,42,43}.yaml` | Exact-delta recipe | ✓ EXISTS + SUBSTANTIVE | Graded: `max_epochs=1000`, `n_adam=1000`, `replay_count` unset, `front_advance_window_n=500`, `lambda_e_max=0.0`, `data.source=admitted`. Smoke: `replay_count=32`, seed 42. Sources `configs/smoke.yaml` / `configs/stage0-example.yaml` remain unedited. |
| `50-PRE-REGISTRATION.md` / `50-CONFIG-DELTA.md` | D-07..D-12 + D-03 confound | ✓ EXISTS + SUBSTANTIVE | Generation-3 amendment keeps `selection_policy` byte-identical; config delta is verified identical to generation 2. |
| `pinn/conformance/divergence_register.json` | C-09 closed + qualifications open | ✓ EXISTS + SUBSTANTIVE | `C-09` closed with proof test `tests/phase50/…test_validation_pool_below_replay_count_no_longer_raises`. `STAGE0-BUDGET-DELTA`, `VALIDATION-TRAIN-RNG-COUPLING`, `VALIDATION-SNAPSHOT-RESAMPLING` open. |
| `evidence/run-ledger.md` | phase50-run-ledger/v2 | ✓ EXISTS + SUBSTANTIVE | `final_band_generation: null`. Generations 1–3 all `status=terminal`. Six records, six invocations, zero `in_final_band`. |
| `evidence/terminal-manifest.json` | Terminal forensic identity | ✓ EXISTS + SUBSTANTIVE | Root generation-2 section plus appended `generation_3.terminal_reason=invariant-b-halt-front-idx-stalled-n-500`. Seeds 42/43 marked inapplicable. `verify_phase50_evidence.py terminal` printed `TERMINAL-EVIDENCE-OK`. |
| `evidence/build_phase50_evidence.py` / `verify_phase50_evidence.py` | Independent builder/verifier | ✓ EXISTS + SUBSTANTIVE | Terminal branch executed. Normal-mode `extract`/`band`/`candidate` refuse when the final generation is null. |
| `evidence/corpus/generation-3.json` / `environment/generation-3.json` / calibration + transcripts + attempt copies | Generation-3 protocol evidence | ✓ EXISTS | Smoke attempt 4 and seed-41 attempt 2 forensic copies present, including `failure/trip.json`. |
| `runs/stage0-rerun-smoke/` / `runs/stage0-rerun-seed41/` | Gitignored live run dirs | ✓ EXISTS (on disk) | Smoke finished; seed 41 HALTed. Checkpoints remain uncommitted. |
| `runs/stage0-rerun-seed42/` / `runs/stage0-rerun-seed43/` | Graded band members | ✗ MISSING | Never launched after the D-20 HALT. |
| `evidence/band-record.md` / `candidate-receipt.json` / `source-manifest.json` / `manifest.json` | Normal-mode RUN-02 / Phase-51 handoff | ✗ MISSING (protocol-correct absence) | 50-03 terminal exemption applies. The absence is honest. It is still a phase-goal miss: there is no descriptive three-seed record and no candidate. |

**Artifacts:** recipe, repair, and terminal-evidence artifacts verified; band-goal artifacts missing.

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|----|--------|---------|
| SCOPE-27 | Stage-0 ceiling | `--stage-0-only` → guarded ADVANCE | ✓ WIRED | Every ledgered generation-3 launch command contains `--stage-0-only` and no `--resume`. Seed 41 never wrote `stage-0-final` because ADVANCE never occurred. |
| `ctl_instruction.md` held-out validation set | `_run_validation` | `select_validation_records` / `_validation_batch` | ✓ WIRED | Live on generation-3 head `c4a1550b` (repair ancestor `312f3080`). Seed-41 first validation at step 100 completed without `StageZeroUnderpopulated`. |
| Smoke calibration | Duration gate | `runs/.calibration/stage0-timing.json` | ✓ WIRED | Generation-3 smoke `valid=true`, `git_head=c4a1550b`, gate input 182.9 s. Owner `proceed` recorded 2026-08-15T03:02:42Z before the graded launch. |
| Invariant B `N=500` | Seed-41 run | `front_advance_window_n` + `StepGuards` | ✓ WIRED — GATE FIRED | The gate did what D-20 said it might. Wiring is not the same as the invariant holding for a full run. |
| `final_band_generation = 3` | 50-03 band/candidate | ledger closeout | ✗ NOT WIRED | Closeout left the field null. 50-03 took the terminal branch and wrote no band or candidate. |
| Pre-registration 42→41→43 | Phase-51 candidate | D-10 structural facts | ✗ NOT WIRED | No eligible finished graded run. No `candidate-receipt.json`. Phase 51 has no handoff. |
| Seed-42 smoke `s_h`/`n_train` | Seed-42 graded metadata | D-16 | ✗ NOT WIRED | Seed 42 never ran. |

**Wiring:** recipe and C-09 links hold; the band-closeout and candidate links do not.

## Requirements Coverage

Every PLAN frontmatter `requirements:` list is `{RUN-01, RUN-02}`. Both IDs appear in REQUIREMENTS.md as Phase 50, both checkboxes remain unchecked, and both mapped-status rows remain `Pending`. No other requirement ID is claimed by this phase.

| Requirement | Status | Blocking Issue |
|-------------|--------|----------------|
| RUN-01: Stage-0 re-run under the corrected recipe, with conformance-only iteration (SCOPE-29). | ✗ BLOCKED | The corrected recipe and the C-09 repair landed, and iteration stayed conformance-only (truth 4). The re-run itself did not complete: invariant B HALTed the only graded seed at step 501, so ROADMAP SC2 is false. D-30 reserves flipping this checkbox to phase verification; it must stay unchecked. |
| RUN-02: Re-establish the three-seed band, matching the v2.0 protocol so the runs are comparable. | ✗ BLOCKED | One HALTed seed is not a three-seed band. No `band-record.md`, no candidate, `final_band_generation` null, D-16 undischarged. Even seed 41 did not record validation ε_H (`gate_status=failed:TypeError`, no sidecars). |

**Coverage:** 0/2 requirements satisfied

`50-04-SUMMARY.md` lists `requirements-completed: [RUN-01, RUN-02]`. That is an overclaim. Plan 50-04 landed a conformance repair, not the experiment. Treat the SUMMARY field as non-authoritative relative to this report and to REQUIREMENTS.md.

## Decision Coverage

`gsd-tools query check.decision-coverage-verify` returned `reason: could-not-parse` (`honored: 0`, `total: 28`, `blocking: false`). Two wrapped CONTEXT bullets (`D-03`, `D-07`) failed the `- **D-NN ...**` parser.

Manual check against shipped artifacts: D-01..D-06, D-13..D-15, D-17, D-19, D-20, D-22, D-23, D-27..D-30 are visible in the configs, register, ledger, and terminal closeout. D-16 (smoke vs seed 42), D-08..D-11 candidate selection, and D-24 band-record contents were not exercised because there is no band. Non-blocking for status; listed for drift review.

## Behavioral Verification

| Check | Result | Detail |
|-------|--------|--------|
| `unittest discover -s tests/phase50` | 7 passed, 0 failed | Full-pool selector, no-lookahead, untouched 240+16 train path, empty-pool refusal, blacklist/non-Set-1a rejection. 0.608 s. |
| `unittest discover -s tests/phase40` | 170 passed, 0 failed | Broader than the 51-test controllers/optimizer subset named in 50-04. 28.928 s. |
| `unittest discover -s tests/phase41` | 197 passed, 0 failed | Entrypoint / `--stage-0-only` suite. 65.530 s. |
| `verify_phase50_evidence.py terminal` | ✓ | `TERMINAL-EVIDENCE-OK generations=3 records=6 invocations=6 attempt_copy_files=58 cleanliness=31 verify=2` |
| BAND-OK / three in-final-band finished seeds | ✗ | Ledger `final_band_generation is None`; seeds 42/43 absent. |
| Validation ε_H band record | ✗ | `band-record.md` absent; seed-41 events are `failed:TypeError`. |

Passing unit tests prove the C-09 repair and the Stage-0 ceiling. They do not prove a finished Stage-0 experiment.

### Test Quality Audit

| Test File | Linked Req | Active | Skipped | Circular | Assertion Level | Verdict |
|-----------|-----------|--------|---------|----------|----------------|---------|
| `tests/phase50/test_validation_full_pool.py` | RUN-01 (C-09 population) | 7 | 0 | no | Behavioral (identity set, no raise, train 240+16) | Sufficient for the repair, not for RUN-01 end-to-end |
| `tests/phase40/test_controllers.py` / `tests/phase41/test_train_entrypoint.py` | RUN-01 (`--stage-0-only`) | included in 170 / 197 | 0 found in phase50 | no | Behavioral | Sufficient for the ceiling |

**Disabled tests on requirements:** 0
**Circular patterns detected:** 0
**Insufficient assertions:** 0 for the repair; the missing proof is the experiment itself, not a weak unit test.

## Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| `50-04-SUMMARY.md` frontmatter | `requirements-completed` | Claims RUN-01/RUN-02 completed | ⚠️ Warning | Overstates phase-goal discharge; REQUIREMENTS.md correctly still pending |
| `ROADMAP.md` Phase 50 wave-4 blurb | ~221 | Still says `GAP-50-03 OPEN` | ⚠️ Warning | Stale vs `50-GAPS.md` / `v2.2-GAPS.md` (`RESOLVED-WITH-INSTRUCTION`, Option A) |
| seed-41 `validation.jsonl` | events 100–500 | `gate_status=failed:TypeError` | ⚠️ Warning | Validation ε_H / EVAL-01-iii evidence missing even for the launched seed; recorded, not used to retune (D-19) |

No TBD/FIXME/XXX blockers in phase-owned implementation files. “Placeholder” hits in 50-01/50-PATTERNS refer to the copied smoke-config comment, not stub code.

**Anti-patterns:** 3 found (0 blockers, 3 warnings)

## Human Verification Required

This is an experiment-execution phase, not a UI. There is no end-user UAT list. The following are owner-gated follow-ups, not a reason to mark the phase `human_needed` while SC2/SC3 remain false.

### 1. Later-generation authorization (GAP-50-03 Option A)
**Test:** Decide whether to authorize a new generation at all.
**Expected:** Either a dated authorization that amends the plan/acceptance criteria before any launch, or an explicit decision to leave RUN-01/RUN-02 pending and keep Phase 50 incomplete.
**Why human:** Option A forbids the agent from opening generation 4, launching 42/43 at this head, or changing `N`.

### 2. Validation-gate TypeError before any later band
**Test:** Classify the seed-41/smoke `gate_status=failed:TypeError` under D-19 (conformance repair vs source-silent).
**Expected:** A repair, if any, is justified without citing the HALT or the observed 227, then a fresh full generation is run. Or the defect is recorded as a new gap and left untouched.
**Why human:** A later finished seed that still lacks validation-gate sidecars would remain EVAL-01-iii ineligible.

## Gaps Summary

### Critical Gaps (Block Progress)

1. **Invariant B did not hold for a full graded run (ROADMAP SC2 / RUN-01)**
   - Missing: a finished 1000-step Stage-0 run on which the causal front advances within `N=500` and no causal weight is exactly zero.
   - Impact: the phase goal (“the first run that is actually the specified experiment”) is not true. The only graded seed HALTed at step 501 with `front_idx` stuck at 0.
   - Fix: not an agent edit of `N`. Per GAP-50-03 Option A, only a separately authorized later generation — or an explicit owner decision to leave RUN-01 pending — can change this.

2. **No three-seed validation-ε_H band (ROADMAP SC3 / RUN-02)**
   - Missing: finished seeds 42 and 43; `final_band_generation=3`; `band-record.md`; `candidate-receipt.json`; D-16 smoke↔seed-42 equality; independently re-derived ε_H characterization.
   - Impact: Phase 51 has no candidate and no identity receipt. RUN-02 cannot close.
   - Fix: same as gap 1. Do not manufacture a partial band from smoke + HALTed seed 41.

3. **Launched seed 41 did not record validation ε_H**
   - Missing: `validation_gate/` sidecars, `gate_eps_h` / finite-only quantiles, `eval01_precondition_iii`.
   - Impact: even if invariant B had not HALTed, this seed would not have supplied the validation characterization SC3 names, and would have been structurally ineligible under D-10/EVAL-01-iii.
   - Fix: diagnose the `TypeError` as a possible D-19 conformance repair before any later generation. Do not retune thresholds from the failed events.

### Non-Critical Gaps (Can Defer)

1. **ROADMAP wave-4 still says GAP-50-03 OPEN**
   - Issue: index and `50-GAPS.md` already record Option A.
   - Impact: documentation drift only.
   - Recommendation: correct the blurb when the orchestrator next edits ROADMAP. Do not use that edit to mark the phase complete.

2. **`50-04-SUMMARY.md` overclaims RUN-01/RUN-02**
   - Issue: plan-local frontmatter vs D-30 checkbox ownership.
   - Impact: a later reader could treat the repair as experiment completion.
   - Recommendation: leave REQUIREMENTS.md unchecked; this report is the corrective record.

## Deferred Items

None. Phase 51 spends the single held-out look on a Phase-50 candidate. Phase 52 re-derives DIAG-05 from a conformant run. Neither later phase re-establishes the three-seed band or makes invariant B hold. These gaps stay here.

## Recommended Fix Plans

Do **not** execute either plan without a new owner authorization. GAP-50-03 Option A is still in force.

### 50-06-PLAN.md: Owner-authorized later generation (blocked)

**Objective:** If and only if the owner separately authorizes a new generation, run the full smoke + 41 → 42 → 43 window at one head after any D-19 repair, and close with either `final_band_generation = N` and three finished in-band records or another honest terminal.

**Tasks:**
1. Wait for a dated owner authorization. Do not launch on this verification.
2. If a D-19 repair is authorized, land it as a new source-identity commit with a pre-registration amendment that keeps `selection_policy` byte-identical.
3. Re-enter the 50-02/50-05 procedure for the new generation. Never `--resume`. Never change `N` or `replay_count` from a run outcome.

**Estimated scope:** Large (full band). **Blocked** until the owner authorizes.

### 50-07-PLAN.md: Classify the validation-gate TypeError

**Objective:** Decide whether `gate_status=failed:TypeError` is a conformance divergence that must be repaired before another graded launch.

**Tasks:**
1. Reproduce the TypeError from the committed seed-41/smoke validation events and the production `compute_validation_gate` path.
2. If a locked spec/owner contract already names the correct behavior, file a D-19 repair and a register entry. If the source is silent, STOP and write a gap.
3. Do not treat a repair as RUN-02 discharge; a later generation still has to run.

**Estimated scope:** Small–medium. Safe to plan; not safe to fold into a silent generation-4 launch.

---

## Verification Metadata

**Verification approach:** Goal-backward from ROADMAP Phase 50 success criteria (override PLAN `must_haves`)
**Must-haves source:** `.planning/ROADMAP.md` Phase 50 success criteria 1–4
**PLAN requirement IDs accounted for:** RUN-01, RUN-02 (both BLOCKED)
**Automated checks:** phase50 7 OK; phase40 170 OK; phase41 197 OK; `TERMINAL-EVIDENCE-OK`; ledger `final_band_generation=null`; seeds 42/43 absent
**Human checks required:** 2 owner follow-ups (listed; do not flip status to `human_needed`)
**Git HEAD at verify:** `922e03ea` (`docs(50): mark 50-03 complete after terminal evidence`) on `milestone/v2.2`
**Repair / generation-3 identities:** C-09 `312f3080`; generation-3 head `c4a1550b`; closeout `7d910485`; 50-03 terminal `9284d0ac`
**Total verification time:** ~20 min

---
*Verified: 2026-08-15T03:42:00Z*
*Verifier: Grok (gsd-verifier-50)*
