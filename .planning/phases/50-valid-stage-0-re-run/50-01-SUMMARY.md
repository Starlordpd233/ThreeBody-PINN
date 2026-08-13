---
phase: 50-valid-stage-0-re-run
plan: 01
subsystem: training-orchestration
tags: [pinn, curriculum-controller, cli, yaml-config, divergence-register, pre-registration, run-ledger, unittest]

# Dependency graph
requires:
  - phase: 49-conformance-gate
    provides: GATE-01..03/INST-03 conformance gate, invariant-B N=500 ratification, divergence register API
  - phase: 47-frame-completion-s-h-pipeline
    provides: S_H/eps_H pipeline, CONF-09/CONF-02/CONF-03 conformant loss wiring
provides:
  - "--stage-0-only fresh-run Stage-0 ceiling on CurriculumController/pinn.train (SCOPE-27 enforcement)"
  - "Four committed Phase-50 configs (1 smoke + 3 graded) encoding D-01..D-06/D-15 exactly, with a captured D-04 diff receipt"
  - "50-PRE-REGISTRATION.md: seed/checkpoint/fallback-order selection policy fixed before any graded run, with a machine-parseable JSON policy block"
  - "50-CONFIG-DELTA.md: every deliberate delta from the frozen v2.0 pilot config, derived by structural diff, not assumption"
  - "STAGE0-BUDGET-DELTA divergence-register qualification entry (open) carrying the 1000-vs-300 budget confound forward"
  - "evidence/run-ledger.md and evidence/README.md scaffolds (empty, schema-valid) for plan 50-02 to append into"
affects: [50-02-run-the-band, 50-03-evidence-extraction, 51-authorized-evaluation, 52-diag-05-re-derivation]

# Actuals (#2632)
actuals:
  tokens: 21677
  tasks: 3
  commits: 1

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Fresh-run-only conformance ceiling as a narrow constructor flag (stage_0_only) plus a matching CLI flag, gated to a single branch inside an existing dispatch method rather than a new control-flow layer"
    - "Config-delta derivation via structural comparison of two load_config()-resolved TrainingConfig objects (dataclass-field-flattened), not a literal-YAML-key diff, so silently-defaulted deltas (e.g. stage.replay_count) are caught"
    - "Pre-registration selection-policy self-hashing (selection_policy_sha256 over canonical compact sorted JSON) so a later byte-level edit to the policy is self-detecting"
    - "Divergence-register writes exclusively through load_divergence_register()/write_divergence_register() (never hand-edited JSON), relying on _validate_payload's fail-closed schema check"

key-files:
  created:
    - configs/stage0-rerun-smoke.yaml
    - configs/stage0-rerun-seed41.yaml
    - configs/stage0-rerun-seed42.yaml
    - configs/stage0-rerun-seed43.yaml
    - .planning/phases/50-valid-stage-0-re-run/50-PRE-REGISTRATION.md
    - .planning/phases/50-valid-stage-0-re-run/50-CONFIG-DELTA.md
    - .planning/phases/50-valid-stage-0-re-run/evidence/README.md
    - .planning/phases/50-valid-stage-0-re-run/evidence/run-ledger.md
    - .planning/phases/50-valid-stage-0-re-run/evidence/config-band-diff.txt
  modified:
    - pinn/train.py
    - pinn/training/controllers.py
    - tests/phase40/test_controllers.py
    - tests/phase41/test_train_entrypoint.py
    - pinn/conformance/divergence_register.json

key-decisions:
  - "Under --stage-0-only, CurriculumController.step()'s ADVANCE branch persists stage-0-final (unchanged) then returns immediately -- skipping the stage increment, stage_factory/Stage-1 conformance_hook call, stage-1-init write, 0->1 promotion, AND the k->k+1 record_disposition call (not just the checkpoint writes), so no ledger row ever names stage 1 (acceptance criterion 'no stage > 0 record')"
  - "run() terminates the loop on any guarded ADVANCE rather than looping into a second run_stage(0) call -- self._stage staying 0 after a guarded ADVANCE is the signal run() reads, since the ordinary path always increments it"
  - "50-CONFIG-DELTA.md's table was derived by loading both the pilot config and the Phase-50 seed42 config through pinn.training.config_yaml.load_config and structurally diffing the resolved dataclasses field-by-field, per the plan's 'read the actual pilot file -- do not assume its contents' instruction; this surfaced one delta beyond the plan's named minimum list (run.checkpoint.rolling_keep: 4 -> 3, a 43-06 ACC-02 smoke-specific tuning never carried into configs/stage0-example.yaml) and confirmed run.log_every is NOT a pilot-vs-Phase-50 difference (both are 50; only stage0-example.yaml's own un-modified default of 100 differs)"
  - "REQUIREMENTS.md RUN-01/RUN-02 checkboxes deliberately NOT flipped by this plan -- 50-CONTEXT.md D-30 reserves that to the phase verification act (Phase-47/49 precedent), and substantively neither requirement's outcome exists yet: this plan lands pre-band commits only, no run has executed"

requirements-completed: []

duration: ~50min
completed: 2026-08-13
status: complete
---

# Phase 50 Plan 01: Fresh-Run Stage-0 Ceiling, Configs, Pre-Registration, and Wave-1 Commit Summary

**Added the `--stage-0-only` conformance guard, committed the four exact-delta Stage-0 configs with a captured D-04 diff receipt, authored the pre-registration and config-delta governance records with a fenced machine-parseable JSON policy block, appended the STAGE0-BUDGET-DELTA register qualification via the API, and scaffolded the run-ledger/evidence-README so plan 50-02 can open the first Phase-50 band generation with every prerequisite commit already in git history.**

## Performance

- **Duration:** ~50 min
- **Completed:** 2026-08-13T04:03:47Z
- **Tasks:** 3 (all `type="auto"`, no checkpoints)
- **Files modified:** 15 (5 modified, 9 created, this SUMMARY)

## Accomplishments

- **SCOPE-27 fresh-run Stage-0 ceiling** (`pinn/train.py`, `pinn/training/controllers.py`): a new `--stage-0-only` CLI flag, refused before construction when combined with `--resume`, threaded into `CurriculumController(stage_0_only=...)`. On a guarded Stage-0 `ADVANCE`, `step()` persists the ordinary `stage-0-final` boundary, logs the exit, and returns immediately — before the stage increment, any `stage_factory`/Stage-1 `conformance_hook` call, the `stage-1-init` write, the `0->1` promotion, the `k->k+1` disposition record, or the Stage-1 rewarm; `run()` then terminates on that ADVANCE instead of looping into a second `run_stage(0)` call. The unguarded default path is untouched.
- **Four committed configs** encoding D-01..D-06/D-15 exactly: `configs/stage0-rerun-smoke.yaml` (copied from `configs/smoke.yaml`, `run_name` renamed, `front_advance_window_n: 500` set) and `configs/stage0-rerun-seed{41,42,43}.yaml` (copied from `configs/stage0-example.yaml`, `seed`/`run_name`/`log_every: 50` set, and the `data: {source: admitted, blacklist_path: ...}` block appended). `evidence/config-band-diff.txt` captures the literal `diff` proof that the three graded configs vary only in `seed`/`run_name`. Both source templates (`configs/smoke.yaml`, `configs/stage0-example.yaml`) are byte-unchanged.
- **50-PRE-REGISTRATION.md**: the seed-42 candidate, the `checkpoints/best.pt` checkpoint rule, the 42->41->43 ineligibility-only fallback order with the four D-10 conditions, the D-11 no-eligible-seed owner-checkpoint rule, the D-12 splits-hash table (cross-checked against the seed-42 v2.0 evaluation receipt), the `source_config_sha256`-vs-`frozen_config_sha256` distinction, and the full D-21/D-30 recovery/attempt policy (the once-per-generation transient-retry rule, the dormant-fallback statement, and the no-resume rule with its `CollocationSampler` RNG gap) — closed by one fenced `phase50-pre-registration/v2` JSON block whose `selection_policy_sha256` self-verifies.
- **50-CONFIG-DELTA.md**: every field that actually differs between the Phase-50 graded configs and the frozen `runs/stage0-pilot-seed42/config.yaml`, derived by structurally diffing two `load_config()`-resolved `TrainingConfig` objects (not literal YAML keys), plus the separate `--stage-0-only` execution-protocol row, the full I_warm/T_max/validation-opportunities budget-confound explanation, the `log_every` dual-fact clarification, and the `STAGE0-BUDGET-DELTA` cross-reference.
- **`STAGE0-BUDGET-DELTA` register entry**: appended via `load_divergence_register()`/`write_divergence_register()` only (never hand-edited), `kind: qualification`, `status: open`, `proof_test: null` — confirmed excluded from `evaluate_eval01_precondition_i`'s open-divergence census (that predicate scopes to `kind == "divergence"`).
- **`evidence/run-ledger.md` and `evidence/README.md`** scaffolds: an empty, schema-valid `phase50-run-ledger/v2` ledger with the full band-generation/attempt/invocation/retry-authorization field contract documented in prose (for plan 50-02 to append into as uncommitted edits, per D-17), and a layout index for the whole Phase-50 evidence tree.
- **Focused tests** (`tests/phase40/test_controllers.py::StageZeroOnlyGuardTests`, `tests/phase41/test_train_entrypoint.py::StageZeroOnlyCliTests`): the guarded ADVANCE saves only `stage-0-final` and stays at stage 0 with `promote`/`record_disposition` never called and the Stage-1 `conformance_hook` call never fired; `run()` terminates normally with no second `run_stage()` call; a live-`RunController` construct proves `stage_factory` is never invoked under the guard; the unguarded (`stage_0_only=False`) controller still advances to stage 1 exactly as before (regression); the CLI accepts a fresh `--stage-0-only` launch; `--stage-0-only --resume latest` refuses before any run directory is created.
- **Wave-1 commit**: every file above landed in one commit on `milestone/v2.2` via `scripts/agent-commit`, completing the D-17 pre-band commit window before plan 50-02 may open the first band generation.

## Task Commits

Per the plan's explicit Task 3 instruction (D-17: "land every code/config commit the phase needs" as a single pre-band landing), all three tasks' work was committed together in **one** wave-1 commit rather than per-task commits:

1. **`feat(50-01): enforce stage-zero rerun protocol`** — Task 1 (Stage-0 ceiling + tests + configs + diff receipt), Task 2 (pre-registration + config-delta + register entry), and Task 3 (ledger + README scaffolds + this SUMMARY) combined.

## Files Created/Modified

- `pinn/train.py` — added `--stage-0-only` argparse flag, the resume-combination refusal, and the `stage_0_only` pass-through into `CurriculumController(...)`
- `pinn/training/controllers.py` — added `CurriculumController(stage_0_only=...)`, the guarded early-return branch inside `step()`'s ADVANCE dispatch, and the matching terminal check inside `run()`'s loop
- `tests/phase40/test_controllers.py` — added `StageZeroOnlyGuardTests` (4 tests)
- `tests/phase41/test_train_entrypoint.py` — added `StageZeroOnlyCliTests` (2 tests)
- `pinn/conformance/divergence_register.json` — appended `STAGE0-BUDGET-DELTA` via the register API (the diff also re-encodes pre-existing non-ASCII characters to `\uXXXX` escapes — an atomic-rewrite formatting side effect, not a content change)
- `configs/stage0-rerun-smoke.yaml` — new; copy of `configs/smoke.yaml` with `run_name`/`front_advance_window_n` deltas and a Phase-50 data-root header note
- `configs/stage0-rerun-seed41.yaml`, `configs/stage0-rerun-seed42.yaml`, `configs/stage0-rerun-seed43.yaml` — new; copies of `configs/stage0-example.yaml` with `seed`/`run_name`/`log_every`/`data` deltas
- `.planning/phases/50-valid-stage-0-re-run/50-PRE-REGISTRATION.md` — new; the full selection-policy pre-registration record
- `.planning/phases/50-valid-stage-0-re-run/50-CONFIG-DELTA.md` — new; the derived config-delta table and confound explanation
- `.planning/phases/50-valid-stage-0-re-run/evidence/README.md` — new; evidence-tree layout index
- `.planning/phases/50-valid-stage-0-re-run/evidence/run-ledger.md` — new; empty schema-valid ledger scaffold
- `.planning/phases/50-valid-stage-0-re-run/evidence/config-band-diff.txt` — new; captured `diff` receipt

## Decisions Made

- **`record_disposition` is skipped, not merely re-targeted, under the guard.** The plan's acceptance criterion "no stage > 0 record" ruled out calling `self._checkpoint_store.record_disposition(k, k + 1, ADVANCE, step)` under `--stage-0-only`, since that call's own arguments name stage `k+1`. `_log_stage_exit(ADVANCE, stage=k)` (a logging call, not a checkpoint-store ledger write) satisfies the plan's separate "log the Stage-0 exit" requirement without adding a stage-1-naming record.
- **`run()`'s termination check is `self._stage_0_only and disposition is ADVANCE`**, not an additional `self._stage == 0` check — because the guarded `step()` branch, by construction, never lets `self._stage` advance past 0, a guarded controller can never reach `run()`'s loop-continuation branch a second time with `self._stage >= 1`. This keeps the `run()` change to one condition rather than two.
- **Config-delta rows were derived, not transcribed from the plan's "expected minimum" list.** Loading both configs through `load_config()` and diffing the resolved dataclasses surfaced `run.checkpoint.rolling_keep` (4 -> 3) as a real delta the plan's named list didn't call out by key, and independently confirmed `run.log_every` is NOT a delta (both resolve to 50) — matching the plan's explicit "read the actual pilot file — do not assume its contents" instruction and its "plus any guards/checkpoint/recover_retries keys the pilot config predates" catch-all.
- **RUN-01/RUN-02 requirement checkboxes were not flipped.** `50-CONTEXT.md` D-30 reserves that to the phase verification act; separately, this plan's own work (pre-band commits only) does not make either requirement's outcome true yet.

## Deviations from Plan

### Orchestrator-directed test-runner substitution (not a plan deviation — an environment correction supplied by the orchestrator)

The plan's Task 1 `<automated>` verify block invokes
`python -m pytest tests/phase40/test_controllers.py tests/phase41/test_train_entrypoint.py -q`.
`pytest` is not installed in the `pinn-train` conda environment and both
suites are `unittest`-based. Per the orchestrator's `<orchestrator_corrections>`
(verified fact about this runtime, not re-litigated), every verify invocation
in this execution instead ran:

```
<home>/miniforge3/bin/conda run -n pinn-train python -m unittest tests.phase40.test_controllers tests.phase41.test_train_entrypoint
```

Result: 51 tests, all passing, exit 0 (run twice — once immediately after the
CurriculumController/CLI code changes and the new tests were added, and once
again after the config files existed — both runs identical: `OK`). No
`pip`/`conda install` was performed; the environment snapshot is unmodified,
preserving the plan's own T-50-SC prohibition against mutating the
environment `pinn.train`'s duration-gate calibration binds to.

No other deviations. Every value in this plan (seeds, thresholds, `N=500`,
`lambda_e_max=0.0`, the D-12 sha256 table, the sha256 hashes of the four
committed configs) was either copied verbatim from `50-CONTEXT.md` or
mechanically computed (sha256, structural config diff) — none was chosen or
tuned, per SCOPE-29/D-19.

## Known Stubs

None. `evidence/run-ledger.md`'s empty `records: []` / `band_generations: []`
/ `final_band_generation: null` is the **intended** state at scaffold time
(D-17/D-22: plan 50-02 appends into this schema once the band opens) — it is
a complete, schema-valid, verified-parseable skeleton, not a placeholder
standing in for missing work.

## Issues Encountered

None. `PYTHONPATH` needed to be set explicitly when invoking the register-
append script from an absolute path outside the repo (`python
/abs/path/script.py` puts the script's own directory, not the repo root, at
`sys.path[0]`) — an execution-environment detail, not a plan or code issue;
resolved by prefixing the invocation with
`PYTHONPATH=<repo-root>:$PYTHONPATH`.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

Plan 50-02 (run the smoke, then the three graded seeds) is unblocked: every
file its band-generation open-check needs is now in git history on
`milestone/v2.2` — the pre-registration record's `generation_binding`
identities, the four exact-delta configs, the `--stage-0-only` guard and its
tests, and the ledger scaffold plan 50-02 appends into. `git status` over
every phase-owned path is clean after the wave-1 commit (verified below), so
the D-17 "no commit between calibration and graded runs" window can open
cleanly. No blockers.

---
*Phase: 50-valid-stage-0-re-run*
*Completed: 2026-08-13*
