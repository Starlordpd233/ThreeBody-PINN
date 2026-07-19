---
phase: 42
reviewers: [grok, codex, agy]
rerun_reviewers: [grok, codex, agy]
reviewed_at: 2026-07-19T05:39:24Z
generated_by: xreview
xreview_run_dir: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260719T053405Z-28773
---

# Cross-AI Plan Review — Phase 42

## grok Review

I'll review Phase 42 by reading the nine plan files first, then pull CONTEXT/SPEC/roadmap only where needed to verify concerns.

---

## codex Review

## 1. Summary

Phase 42 is well-scoped around the operator surface and monitoring layer, and the plan set has a strong substrate-to-wiring progression. All listed phase plan files were readable.

The main risk is not missing coverage; it is that several later plans assume control-flow and death-mode behaviors that the current `pinn.train` / controller API does not yet expose explicitly.

## 2. Strengths

- Clear wave structure: logging substrate, config seams, tests, sinks, heartbeat/summary, runbook, composition wiring, then held-out edge tests.
- Strong attention to data integrity: atomic `status.json` / `summary.*`, strict JSONL non-finite handling, append-only logs, and redaction tests.
- Good preservation of prior seams: `run.log_every` is retained, `B-2` field ownership is treated as provisional, and no new dependency is introduced.
- The validation map covers the important negative cases: non-finite logs, signal races, torn status writes, partial runs, false-green artifacts, leaked local identity, and wrapper exit propagation.

## 3. Concerns Tagged HIGH / MEDIUM / LOW

- **HIGH**: `42-08` assumes `SignalState.stop_requested` is checked at step boundaries, but it only owns `pinn/train.py` and `pinn/training/signals.py`. The current loop calls `curriculum.run()` once from `main()` and has no stop-check hook in `RunController` / `CurriculumController`; `checkpoint_hook` cannot stop the loop, and `guard_hook` only returns guard dispositions. As written, SIGINT/SIGTERM wiring may not interrupt promptly or produce exit 130/143.

- **HIGH**: terminal state mapping is underspecified. Existing `StageDisposition` has only `ADVANCE`, `RECOVER`, and `HALT`; `CurriculumController.run()` returns terminal `HALT` normally. `42-08` requires distinguishing normal completion → `finished` from guard HALT / exception → `failed`, but the plan does not define a reliable terminal-cause signal.

- **HIGH**: `42-09` expects SIGKILLed runs to have `status.json state` in `{failed, interrupted}` and a failed-run summary template. SIGKILL is uncatchable, so the process cannot finalize status or summary after the kill. The launch stub can guarantee presence and “not finished,” but not a post-kill failed/interrupted transition.

- **MEDIUM**: global logger handler lifecycle is not specified. `42-08` attaches JSONL, human, and TensorBoard handlers to `logging.getLogger("pinn.training")`, but does not require remove/close in a `finally` path. Existing tests call `main()` repeatedly in-process, so stale handlers can duplicate log lines or write into old temp run directories.

- **MEDIUM**: `step_completed` is introduced by `42-01`, but omitted from the `STEP_LOG_FIELDS` registry in `42-02`. Since the widened field set is an owner-ratified seam, every canonical emitted field should either be provisional-registered or explicitly marked as non-B-2 metadata.

- **MEDIUM**: L-BFGS widened metrics are still vague. The current L-BFGS path logs `_scalar_loss_terms(total)` only; the plans require full loss terms, residual bins, and `w_n` stats from both optimizer phases, but do not specify how the closure captures those details safely across multiple closure invocations.

## 4. Suggestions

- Add an explicit interruption seam to the controller layer, or expand `42-08` to modify `RunController` / `CurriculumController` with a `stop_requested` callback checked at Adam step boundaries and L-BFGS-safe boundaries.
- Add a terminal-cause record separate from `StageDisposition`, so `main()` can map outcomes to `finished`, `failed`, or `interrupted` without guessing from `HALT`.
- Revise E4 SIGKILL acceptance to assert: artifacts created before kill are present, `status.json` is parseable and not `finished`, staleness is inferable from timestamp age, and `summary.md` is the launch stub. Keep `failed` / `interrupted` expectations for catchable failures and signals.
- Require handler cleanup: remove handlers from the `pinn.training` logger and close JSONL/human/TB sinks on all non-`os._exit` paths; add a repeated-`main()` regression.
- Add `step_completed` to `STEP_LOG_FIELDS` or remove it from canonical JSONL. Add a test asserting L-BFGS records contain the same widened field set as Adam records.

## 5. Overall Risk (LOW/MEDIUM/HIGH)

**HIGH**. The plan set is strong conceptually, but the signal/terminal-state and SIGKILL assumptions need correction before execution, otherwise Phase 42 can produce impossible tests or a monitoring surface that cannot reliably distinguish finished, failed, and interrupted runs.

---

## agy Review

Here is the Cross-AI Plan Review for Phase 42 based on the provided plan files:

## 1. Summary
The Phase 42 plans present a highly robust and well-structured approach to implementing the operator runbook surface and monitoring. The architecture correctly isolates process-level side effects (signals, threads, handlers) to the composition root (`pinn/train.py`), ensuring the underlying library modules remain pure and testable. The use of atomic writes, a strict null-policy for non-finite metrics, and warn-once handlers demonstrates strong defensive programming. However, there are critical flaws in how immediate signal escalation (SIGINTx2) and `SIGKILL` test assertions are designed, which will lead to broken invariant guarantees and automated test failures.

## 2. Strengths
- **Resilient I/O (E3)**: Reusing `atomic_write_text` (temp + fsync + rename) for the heartbeat guarantees that polling readers never encounter a truncated or torn `status.json` or `summary.md`.
- **Strict Null Policy (E1)**: Converting `NaN`/`Inf` to `null` before `json.dumps(allow_nan=False)` ensures the canonical JSONL log remains strictly parseable under divergence, avoiding invalid JSON crashes.
- **Composition Root Purity**: Attaching handlers, threads, and signal callbacks exclusively in `main()` (42-08) correctly prevents side-effect leakage in the `pinn.training` library modules.
- **Fail-Safe Monitoring**: Wrapping TensorBoard `add_scalar` and heartbeat writes in warn-once guards ensures that a monitoring or disk failure never aborts the critical training loop.

## 3. Concerns

- **HIGH: Signal Escalation Defeated by Step-Boundary Polling (42-08)**
  In 42-08 Tasks 1 and 3, the design dictates that `install_signal_handlers` merely sets a `SignalState.escalate` flag, which `main()` is expected to check at the step boundary to trigger `os._exit(130)`. If the process is hung *inside* a step (e.g., an infinite loop or a stuck C++ extension), checking at the boundary will never occur, defeating the purpose of the immediate second-SIGINT escalation. The escalation actions (`status.json` flip, flush, `os._exit`) must execute synchronously inside the signal handler callback itself to bypass a hung main thread.

- **HIGH: Impossible `SIGKILL` Assertion in E4 Test (42-09)**
  In 42-09 Task 2, `test_runs_contract` sends a `SIGKILL` and then asserts `status.json state in {failed, interrupted}`. A `SIGKILL` is handled by the kernel and bypasses all user-space handlers (including `atexit` and `finally` blocks). The `main()` terminal transition will not execute, and the state will remain `running` (or `initializing`). The test will deterministically fail unless it is corrected to assert that the state is either explicitly terminal OR that the heartbeat is objectively stale.

- **MEDIUM: Inconsistent Artifacts on Escalation (42-08)**
  In 42-08 Task 3, the escalation path (second SIGINT) performs a "best-effort atomic `status.json` flip" and then calls `os._exit(130)`, deliberately omitting `finalize_summary`. This leaves `summary.md` as the launch stub ("in progress / did not complete") while `status.json` claims "interrupted". The escalation path should ideally make a best-effort attempt to finalize `summary.md` as interrupted, or the contradiction should be explicitly documented as accepted behavior.

- **LOW: Unhandled Missing `caffeinate` Utility (42-07)**
  The `train-unattended.sh` script executes `exec caffeinate ...` unconditionally. While this project targets M5-Pro (macOS), invoking this in a Linux environment or a stripped container will fail with a shell 127 "command not found", breaking portability unless a fallback or explicit failure message is added.

## 4. Suggestions
1. **Move Escalation Logic to the Signal Callback**: Modify 42-08 to inject an `on_escalate` callback into `install_signal_handlers`, or execute the `os._exit(130)` logic directly inside the `signals.py` SIGINT handler. This guarantees immediate termination even if the main thread is deadlocked.
2. **Fix E4 Kill-Timing Assertions**: Update 42-09 Task 2's `test_runs_contract` to correctly classify a `SIGKILL`ed process via staleness: assert that either `state in {failed, interrupted}` OR `(state == "running" and now - timestamp_epoch > staleness_threshold_secs)`. 
3. **Align Summary on Escalation**: In 42-08 Task 3, add a best-effort `finalize_summary(disposition="interrupted")` call right before `os._exit(130)` to keep `summary.md` consistent with `status.json`.
4. **Shell Script Portability Guard**: Add a quick `command -v caffeinate` check in `train-unattended.sh` (42-07) to provide a clear error message or cleanly bypass it if run on non-macOS environments.

## 5. Overall Risk
**HIGH** (Due to the structural flaw in the signal escalation mechanism that fails to resolve a hung process, and the physically impossible `SIGKILL` test assertions in the E4 coverage that will block successful CI/CD validation.)

---

## Consensus Summary
_Synthesize shared concerns across reviewers above (2+ agreement = highest priority)._

## xreview Diagnostics

### grok
- reviewer=grok
- exit_code=0
- elapsed_seconds=23
- timeout_seconds=360
- watchdog=not_triggered
- command=grok --no-auto-update --no-memory --no-subagents --disable-web-search --permission-mode plan --output-format json -m grok-4.5 --prompt-file /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260719T053405Z-28773/xreview-prompt-42.md 
- grok_json_parse=ok
- grok_raw_stdout_bytes=1024
- stdout_bytes=128
- stderr_bytes=0

### codex
- reviewer=codex
- exit_code=0
- elapsed_seconds=319
- timeout_seconds=360
- watchdog=not_triggered
- command=codex exec --ephemeral --dangerously-bypass-hook-trust --model gpt-5.5 -c model_reasoning_effort=\"xhigh\" --skip-git-repo-check - 
- stdout_bytes=4558
- stderr_bytes=573381

### agy
- reviewer=agy
- exit_code=0
- elapsed_seconds=100
- timeout_seconds=360
- watchdog=not_triggered
- stdout_bytes=4942
- stderr_bytes=0

## Verification coverage

Source-grounding pass (Step 3). Effective drift-guard authority = `grep` (existence
checkable by name; full signatures/behavioral claims are UNCHECKABLE). Under this
authority a MISSING verdict is `needs-acknowledgement` (hardBlock=false) and no verdict
hard-blocks. **Result: every cited existing-code symbol VERIFIED; 0 MISSING, 0 AMBIGUOUS;
no hallucinated references; no hard-block.** The two HIGH review claims about existing
code (`StageDisposition` membership; `CurriculumController.run()` returning HALT for every
terminal cause; absence of a controller stop-seam) are CONFIRMED against source — they are
grounded, not reviewer errors.

Reviewers that returned REAL reviews: codex, agy. grok STUBBED (128 B; preamble only, no
findings). claude, claude-glm SKIPPED (not installed / no profile).

### VERIFIED — existing-code symbols cited by the plans (file:line)
| Symbol | Verdict | Location |
|---|---|---|
| `causal_physics_loss` | VERIFIED | pinn/loss_catalog.py:208 |
| `CAUSAL_ETA_C` / `CAUSAL_W1` | VERIFIED | pinn/loss_catalog.py:34,35 |
| `weights = torch.exp(-eta * cumsum_excl)` | VERIFIED | pinn/loss_catalog.py:258 |
| `return (weights * rbar).mean()` (`rbar` in scope) | VERIFIED | pinn/loss_catalog.py:261 (see NOTE 1) |
| `class RunController` | VERIFIED | pinn/training/controllers.py:275 |
| `RunController._log_step` (params step/loss_terms/lr/phase) | VERIFIED | controllers.py:570 |
| `RunController._non_data_terms` | VERIFIED | controllers.py:470 |
| `RunController._scalar_loss_terms(total_value)` | VERIFIED | controllers.py:597 (grounds codex MED#6) |
| `RunController._run_adam_phase` | VERIFIED | controllers.py:614 |
| `RunController.run_stage` (-> StageDisposition) | VERIFIED | controllers.py:864 |
| `build_checkpoint_payload` | VERIFIED | controllers.py:225 |
| `_LOGGER` = getLogger("pinn.training.controllers") | VERIFIED | controllers.py:970 |
| `self._wall_clock_baseline` | VERIFIED | controllers.py:328 |
| `class CurriculumController` | VERIFIED | controllers.py:1021 |
| `CurriculumController.run` (only ever returns HALT) | VERIFIED | controllers.py:1346 (grounds codex HIGH#2) |
| `_scalar_loss_terms` used on L-BFGS path (total only) | VERIFIED | controllers.py:805,838 (grounds codex MED#6) |
| `guard_hook` invoked per-step (returns outcome) | VERIFIED | controllers.py:657,806; def train.py:410 |
| `checkpoint_hook` invoked per-step (returns None) | VERIFIED | controllers.py:715,844; def train.py:388 |
| No stop/interrupt/should_stop seam in controllers | VERIFIED-ABSENT | grep controllers.py (grounds codex HIGH#1) |
| `class StageDisposition` = {ADVANCE,RECOVER,HALT} only | VERIFIED | pinn/training/stage_exit.py:30 ("Do not add CONTINUE") |
| `ScheduledWeights` | VERIFIED | pinn/training/scheduled_weights.py:65 (import train.py:53) |
| `GuardConfig`/`CheckpointCadence`/`RunConfig` | VERIFIED | pinn/training/config.py:178,206,242 |
| `RunConfig.log_every` (default int=1) | VERIFIED | config.py:253 |
| `_require_int`/`_finite_positive`/`_finite_unit_interval` | VERIFIED | config.py:36,58,65 |
| `TrainingConfig` / `.provisional_fields()` | VERIFIED | config.py:423,478 |
| `ConfigKeyError`/`_resolve_nested_cls`/`_map_section`/`load_config` | VERIFIED | config_yaml.py:47,76,134,175 |
| `freeze_resolved_config` | VERIFIED | config_yaml.py:263 |
| `RESUME_FIELD_REGISTRY` / `resume_field_classification_provisional_entry` | VERIFIED | resume.py:46,593 |
| `_json_safe_scalar` / `_default_memory_signal` / `write_failure_bundle` | VERIFIED | guards.py:124,143,407 |
| `torch.mps.driver_allocated_memory` (referenced) | VERIFIED | guards.py:159 |
| `atomic_write_text` | VERIFIED | pinn/training/atomic_io.py:41 |
| `main` / `_resolve_run_dir` / `TorchSaveCheckpointStore` | VERIFIED | pinn/train.py:246,86,28/354 |
| `store.save_rolling` / `save_best` / `save_anchor` | VERIFIED | pinn/training/checkpoint.py:349,360,367 |
| `_SKIP_PHRASE` ("skipped Phase41 production symbol") | VERIFIED | tests/phase41/__init__.py:27 |
| `make_synthetic_stage0_loop` | VERIFIED | tests/phase41/_fixtures.py:81 |
| `make_stub_split_sources` / `make_stub_source` | VERIFIED | tests/phase40/_fixtures.py:144,132 (re-export phase41:21) |
| `_write_config` / `_TrainHarness` / `_RUNS_ROOT` | VERIFIED | tests/phase41/test_train_entrypoint.py:37,89,100 |

### UNCHECKABLE (grep authority cannot analyze — severity INFO, not treated as verified or missing)
- `caffeinate -is` (42-07) — external macOS CLI; not analyzable via repo grep (man-page-verified per 42-RESEARCH; single-machine macOS target env).
- `torch.mps.current_allocated_memory()` (42-06 secondary mem field) — external torch API, NOT yet referenced in repo; a NEW usage introduced this phase from RESEARCH. Real torch API but not grep-verifiable here.
- All full function/method **signatures** and behavioral claims — UNCHECKABLE under grep authority (existence-by-name only).

### Excluded from grounding — NEW artifacts this phase PRODUCES (per each plan's `artifacts_produced`)
`MonitorConfig`, `STEP_LOG_FIELDS`, `step_log_fields_provisional_entry`, `pinn/training/step_log.py`
(`_sanitize_step_record`, `JsonlStepHandler`, `HumanStepHandler`), `pinn/training/tb_sink.py`
(`TbSink`), `pinn/training/heartbeat.py` (`build_status_snapshot`, `write_status`,
`HeartbeatThread`), `pinn/training/summary.py` (`stub_summary`, `finalize_summary`),
`pinn/training/signals.py` (`SignalState`, `note_signal`, `install_signal_handlers`),
new params/fields `return_details=` and `step_completed`, `scripts/train-unattended.sh`,
`configs/stage0-example.yaml`, the operator runbook, and all `tests/phase42/*`.

NOTE 1: 42-01 Task 1 quotes the loss return as `loss = (weights * rbar).mean()`; the actual
code is a bare `return (weights * rbar).mean()` (no `loss =` binding). Symbols (`weights`,
`rbar`) are real and in scope — cosmetic quote imprecision, not a missing symbol.
