---
phase: 42
reviewers: [grok, codex, agy, claude, claude-glm]
rerun_reviewers: [claude, grok, codex, claude-glm, agy]
reviewed_at: 2026-07-19T07:03:00Z
generated_by: xreview
xreview_run_dir: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260719T065558Z-86190
merged_existing_reviews: true
---

# Cross-AI Plan Review — Phase 42

## grok Review

I'll review the Phase 42 plans from the filesystem, starting with the plan files and consulting context only where needed to verify concerns.

---

## codex Review

## 1. Summary

The Phase 42 plans are detailed and mostly aligned with the phase goal: they build the operator surface, monitoring artifacts, honesty layer, and held-out edge tests without obvious scope creep. No inspected file was unreadable.

I would not execute as-is yet. Two issues can let the phase appear complete while missing required behavior: Plan 9’s dependency graph skips Plan 7, and Plan 8’s L-BFGS signal seam does not meet the stronger CTX-71 interrupt requirement.

## 2. Strengths

- Strong “spine before sinks” design: widened `_log_step` feeds JSONL, human logs, TensorBoard, heartbeat, and summary consistently.
- Good honesty and safety coverage: non-finite JSON null policy, false-green checks, SIGKILL realism, redaction tests, handler cleanup.
- Scope is disciplined: Phase 43 gates/comparison stay out of Phase 42; no new CLI framework beyond the wrapper.
- Plans preserve existing Phase 40/41 behavior with focused regression checks.

## 3. Concerns tagged HIGH / MEDIUM / LOW

- **HIGH:** [42-09-PLAN.md](<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/42-operator-runbook-surface-monitoring/42-09-PLAN.md:6) depends only on `42-03` and `42-08`, but its full-suite gate claims coverage for `test_wrapper_exit` and `test_runbook_config`, which are owned by [42-07-PLAN.md](<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/42-operator-runbook-surface-monitoring/42-07-PLAN.md:8). If execution follows `depends_on`, Plan 9 can run before wrapper/runbook/config tests are realized.

- **HIGH:** The L-BFGS stop seam is weaker than CTX-71. [42-CONTEXT.md](<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/42-operator-runbook-surface-monitoring/42-CONTEXT.md:144) says L-BFGS should check between closure evaluations, but [42-08-PLAN.md](<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/42-operator-runbook-surface-monitoring/42-08-PLAN.md:157) only checks before `optimizer.step(closure)`. In current code, `optimizer.step(closure)` owns repeated closure calls, so first SIGINT may not stop promptly during a long L-BFGS step.

- **MEDIUM:** E4 subprocess timing tests are underspecified. [42-09-PLAN.md](<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/42-operator-runbook-surface-monitoring/42-09-PLAN.md:120) requires SIGKILL “immediately after launch” and “mid-checkpoint-write,” but does not define deterministic barriers. Sleep/poll timing can flake or miss the intended window.

- **MEDIUM:** Plan 8 cleans up logging handlers and heartbeat threads, but does not restore previous SIGINT/SIGTERM handlers after in-process `main()` returns. That leaves stale process-global signal handlers in test harnesses or repeated invocations.

## 4. Suggestions

- Add `42-07` to `42-09`’s `depends_on`, or otherwise make the wave/graph invariant explicit. Also require zero placeholder skips for Phase 42 tests, not only “no placeholder skip on an existing symbol.”
- Move the L-BFGS `should_stop` check into or around the closure loop, using a controlled stop exception caught around `optimizer.step(closure)` if needed. Add a test that signals during L-BFGS closure execution, not only at easier epoch boundaries.
- Define deterministic SIGKILL test barriers: wait for `status.json` `initializing`, a logged Adam step, and a controlled checkpoint-write pause or observable temp-file point.
- Have `install_signal_handlers` return previous handlers or a restore callback, and restore them in Plan 8’s non-`os._exit` `finally`.

## 5. Overall Risk (LOW/MEDIUM/HIGH)

**HIGH** until the Plan 9 dependency and L-BFGS interrupt-seam issues are fixed. After those are addressed, the remaining risk drops to **MEDIUM** due to subprocess timing complexity.

---

## agy Review

# Cross-AI Plan Review: Phase 42 (Operator Runbook Surface & Monitoring)

## 1. Summary
The Phase 42 plans are comprehensive, well-structured, and strictly aligned with the specification. They correctly sequence the work across four waves, establishing the emission payload (Wave 1), building the configuration and sink components independently (Wave 2), wiring them safely into the composition root (Wave 3), and finally realizing the held-out edge/prohibition tests (Wave 4). The architectural choices around graceful signal handling, async TensorBoard, and heartbeat staleness are solid. 

## 2. Strengths
- **Safe Signal Handling:** The decision to coalesce SIGINTs within a debounce window and escalate to a synchronous `os._exit(130)` without writing a second checkpoint perfectly handles hung threads without corrupting data.
- **Strict Honesty & Validation:** The plans aggressively enforce the "no false-green" must-NOT prohibitions, ensuring failed-run templates are honest and metrics are never fabricated.
- **Excellent Test Strategy:** Wave 0's skip-guarded test stubs unblock TDD for downstream tasks, and Wave 4 provides rigorous validation of the final wired system (kill-timing, atomic checkpoints, redaction).
- **Clean Composition:** All process-level side effects (signals, threads, sink attachment) are confined to `main()`, preserving the purity and testability of the `pinn.training` modules.

## 3. Concerns
- **HIGH:** `json.dumps` crash on PyTorch Tensors (42-01 & 42-04). Plan 01 instructs stashing "detached scalars" for `w_n_stats` and `residuals_per_bin`. If these are not explicitly converted to native Python types via `.item()` and `.tolist()`, the `json.dumps(allow_nan=False)` call in Plan 04's JSONL handler will raise a `TypeError` and crash the logger.
- **HIGH:** `front_idx` calculation crash on collapse (42-01). Plan 01 specifies `front_idx = max{n : w_n > 0.5}`. When causal weights collapse toward zero (an edge case explicitly tested in 42-05), the set will be empty. Calling Python's `max()` on an empty sequence raises a `ValueError`, which will crash the step loop.
- **MEDIUM:** Inefficient JSONL parsing at terminal exit (42-08). Plan 08 instructs `main()` to determine failure by checking if "the last parseable line of `train.log.jsonl` has `finite == false`". Reading the last line of a potentially massive log file is brittle and risks loading the whole file into memory. 
- **LOW:** Thread race on `atomic_write_text` (42-06). The `HeartbeatThread` daemon writes periodically, while `transition(state)` forces a synchronous write from the main thread. Unless the internal snapshot mutex also guards the actual `atomic_write_text` call (or the atomic writer uses unique `.tmp` suffixes), these could race on temporary file creation.

## 4. Suggestions
- **Fix Tensor Serialization:** In 42-01 (Task 2), explicitly mandate calling `.item()` and `.tolist()` on the detached tensors before stashing them in `self._last_widened_details`.
- **Provide `front_idx` Fallback:** In 42-01 (Task 2), specify a safe fallback for the `front_idx` calculation (e.g., `max([n for n, w in enumerate(w_n) if w > 0.5], default=-1)`).
- **Track Finite Status in Memory:** In 42-08 (Task 3), avoid parsing the JSONL file from disk. Instead, have `RunController` (or the step log handler) expose a `last_step_finite` boolean flag that `main()` can read directly for the discriminator.
- **Guard File Writes:** In 42-06 (Task 1), ensure the mutex in `HeartbeatThread` guards both the snapshot generation *and* the `write_status` I/O operation to prevent concurrent writes.

## 5. Overall Risk
**MEDIUM.** The architectural design and phase boundary adherence are exceptional. However, the two implementation pitfalls in 42-01 (Tensor JSON serialization and `max()` on an empty sequence) are highly likely to cause runtime crashes during implementation if not preemptively corrected.

---

## claude Review

I have read all nine plans, the SPEC, and verified the key structural claims against the live source. Here is the review.

---

# Cross-AI Plan Review — Phase 42 (Operator Runbook Surface & Monitoring)

## 1. Summary

Nine plans build the operator/monitoring layer on the existing v2.0 training loop across four waves: a shared emission **spine** (42-01/02), the **sinks** (JSONL+human 42-04, TensorBoard residual panel 42-05, heartbeat+summary 42-06, wrapper+config+runbook 42-07), the **composition-root wiring** (42-08), and the **held-out edge/prohibition tests** (42-03 scaffold + 42-09 realization). The decomposition ("spine before sinks before wiring before wired-system tests") is coherent, dependency edges are declared, and the plans already fold in a prior cross-AI review cycle (findings #1–#9 are cited and addressed). Grounding is strong: SPEC edges E1–E4 and the three must-NOTs each trace to a concrete test, and reused seams (`atomic_write_text`, `_default_memory_signal`, `provisional_fields`, `RESUME_FIELD_REGISTRY`, `_resolve_run_dir`) all exist as cited. Collectively the plans do achieve the phase goal.

The dominant weakness is a **canonical step-record field-vocabulary that is not reconciled** across the emitter (42-01), the registry (42-02), and the parity test (42-04) — verified against the live `_log_step`.

## 2. Strengths

- **Honesty layer is load-bearing and consistently enforced**: `initializing` with null (never fabricated) losses, stub-then-finalize `summary.md` present under every death mode, an *explicit* terminal-cause discriminator (finding #4) instead of guessing from the ambiguous `HALT` return, and a false-green test gating it.
- **Edge realism**: E4 correctly distinguishes catchable deaths (assert `state ∈ {failed,interrupted}`) from uncatchable SIGKILL (presence/parseable/not-`finished`/staleness only, finding #1) — a subtlety many plans get wrong.
- **Non-regression discipline**: every core-file change (`causal_physics_loss` `return_details`, `_log_step` widening, `should_stop` seam) is additive/default-off with "byte-for-byte Phase 40" assertions and the existing suites as the guard.
- **Reuse over reinvention**: append-mode JSONL (not `atomic_write_text`), atomic status/summary (via `atomic_write_text`), warn-once monitoring that never aborts training, and the E2 two-point debounce bracket (inside W/5–W/3 vs outside 1.5W–2W) are all well-specified.

## 3. Concerns

### HIGH
- **Field-name vocabulary is inconsistent across 42-01 / 42-02 / 42-04 → the parity test (finding #6) will likely fail as written.** The *current* `_log_step` (controllers.py:585) emits loss keys as `loss_data…loss_angmom` and includes an `event` key; `LossWeights` names its λ components `lambda_e`/`lambda_l` (loss_catalog.py:75-76), not `lambda_energy`/`lambda_angmom`. Meanwhile 42-02 registers bare `data/ic/phys/energy/angmom`, 42-01 emits per-bin `residuals_bin_{n:02d}` and `lambda_*` into the *same* `extra=` dict the JSONL serializes, and 42-04 asserts `set(obj) - {finite,nonfinite_keys} <= set(STEP_LOG_FIELDS)` — while 42-02's module comment claims `finite`/`nonfinite_keys` are the *only* non-registry keys. At least four concrete mismatches (`loss_*` prefix vs bare names; `event`; `residuals_bin_*` absent from the CTX-68 registry list 42-02 copies verbatim; `lambda_e/l` vs `lambda_energy/angmom`) mean the exact-match parity assertion cannot hold without a single pinned key vocabulary that none of the three plans establishes.
- **Per-bin residuals in the canonical JSONL contradict the OPS-03 field set.** SPEC OPS-03 enumerates the JSONL fields and does **not** include per-bin residuals (those are OPS-04b, *TensorBoard*). 42-01 routes `residuals_bin_*` through the shared `_log_step` `extra=` that the JSONL handler serializes, so they leak into `train.log.jsonl` — both a scope deviation and the driver of the parity failure above. The plans never specify that the JSONL handler filters to the OPS-03 set while TB gets the residual bins.

### MEDIUM
- **`torch.mps` called from the daemon heartbeat thread (42-06).** `_default_memory_signal` calls `torch.mps.driver_allocated_memory()` (guards.py:159), today on the main thread. 42-06 Task 1 both says the step loop pushes `mem` via `update()` *and* that `HeartbeatThread` sources mem from `_default_memory_signal` — ambiguous. If the daemon calls `torch.mps.*` concurrently with main-thread MPS compute, thread-safety/meaningfulness is unverified. Prefer: main loop samples mem, daemon reads only the cached snapshot.
- **E2 signal tests are inherently timing-fragile.** `test_signals` shells out to a real `python -m pinn.train`, must confirm handlers are installed *before* the first SIGINT, and sends the second signal inside/outside a ~1 s window. Under CI load this is a flakiness risk; the plan should specify a readiness handshake (e.g. poll `status.json state=="running"`) before signaling, not a fixed sleep.
- **Debounce window (~1 s) vs multi-second L-BFGS step.** The graceful first-SIGINT checkpoint only fires when the main thread next reaches a `should_stop` boundary — potentially seconds away during an L-BFGS line search (the exact scenario the heartbeat exists for). An operator who waits >1 s and presses again escalates to `os._exit` and **loses the graceful checkpoint**. This is the designed semantics, but the ~1 s "discretion" value may be miscalibrated against real step duration; worth an explicit owner note.

### LOW
- **Method-attribution drift**: 42-01 calls the L-BFGS block "the L-BFGS section of `run_stage`", but it is the separate method `_run_lbfgs_phase` (controllers.py:748; `run_stage` starts at 864). Line numbers are consistent and 42-08 names it correctly; an executor reading the file recovers, but the two plans describe the same code differently.
- **L-BFGS logged per-term breakdown may not correspond to the accepted step.** 42-01 reads `closure_state['data_detached']` from the *last* closure invocation; L-BFGS may evaluate the closure multiple times per step, so the logged decomposition can diverge from the accepted-point loss. Acceptable for a diagnostic, but worth a one-line caveat.
- **End-to-end Launch is manual-only.** OPS-01's "reviewer executes Launch/Resume verbatim against the example config" and the TB render need a real dataset run; all automated tests are synthetic/dataset-free. 42-09 acknowledges this as a manual gate — fine, but the phase cannot self-certify OPS-01's headline acceptance.

## 4. Suggestions

- Add a **Wave-1 reconciliation step**: define one canonical key vocabulary in `step_log.py` (single source), have 42-01 emit exactly those names (rename `loss_*`→bare or vice-versa; drop/whitelist `event`), decide residuals' home, and make the 42-04 parity check **family-aware** for dynamic keys (`residuals_bin_*`) or register the fixed bin count. This closes the HIGH findings together.
- Resolve residuals routing explicitly: JSONL handler serializes the OPS-03 set only; TB sink receives `residuals_bin_*` (either a separate emit path or an allow-list on each sink).
- Pin heartbeat memory sampling to the main loop's cached value; forbid `torch.mps.*` from the daemon thread.
- Give `test_signals` a readiness handshake and make the debounce window a documented `MonitorConfig`/owner-tunable seam calibrated against expected L-BFGS step time.

## 5. Overall Risk: **MEDIUM**

The architecture is sound, well-grounded, and already hardened by a prior review pass; nothing here requires redesign. But the field-vocabulary/parity inconsistency is a concrete, verified defect that would surface as a failing 42-04 test and a silent OPS-03 scope drift, and it spans three plans — so it needs an explicit reconciliation rather than executor-time improvisation. The `torch.mps`-from-daemon and E2 timing concerns are real but locally fixable. Resolve the HIGH items in Wave 1 and residual risk drops to LOW.

---

*Note: this review is a read-only snapshot; session `98f7` is concurrently converging these same files (cycle 2), so line numbers and some wording may shift after its next commit. I made no edits.*

---

## claude-glm Review

I verified three of my candidate concerns against the codebase before writing this up:
- `curriculum.jsonl` **does** exist — written by `pinn/training/checkpoint.py` (lines 261–270, 551). The 42-06/42-08 summary rendering has a real source.
- `_log_step` (controllers.py:570) **already** emits `extra={"event": "step", …}` (line 588), and `_log_run_start`/`_log_stage_exit` carry their own `event` values — so the `event=="step"` discriminator the 42-04/42-05 sinks key on is already in place; 42-01's widening is additive on top.
- `ScheduledWeights` and `caffeinate` (`/usr/bin/caffeinate`) are both present.

Those resolved my grounding worries, so the concerns below are the ones that survived.

---

# Phase 42 Plan Review — Operator Runbook Surface & Monitoring

## 1. Summary

Nine plans build the operator surface + monitoring layer on top of the existing v2.0 training loop, mapped cleanly onto OPS-01…06, edges E1–E4, and the three must-NOT prohibitions. The wave DAG is sound (W1: emission spine 01, config seams 02, test scaffold 03 ‖ W2: JSONL/human 04, TB panel 05, heartbeat/summary 06, wrapper/runbook 07 → W3: composition-root wiring 08 → W4: held-out edge/honesty/redaction tests 09), with `depends_on` matching the actual file/symbol contracts. Spot-checks confirm the plans are grounded in real prior-phase artifacts (`curriculum.jsonl`, the `event` log discriminator, `ScheduledWeights`, `caffeinate`). The honesty layer (terminal-cause discriminator, null-not-fabricated summary, atomic heartbeat) and the destructive-operation guard (exit-transparent wrapper) are well-defended. The phase goal is achievable as planned. The remaining concerns are refinements to the signal path and two unverified acceptance items, not blockers.

## 2. Strengths

- **Honesty layer is rigorously designed.** The explicit terminal-cause discriminator in 42-08 (stop_requested → `interrupted`; failure/non-finite/exception → `failed`; else `finished`) correctly avoids the trap of inferring success from the ambiguous `HALT` disposition. SIGKILL is honestly characterized as "presence + parseable + not-finished + staleness" rather than a fake terminal transition (42-09 finding #1) — this is the right call and a common mistake avoided.
- **Spine-before-sinks ordering.** 42-01 widens the single `_log_step` emission point (and fixes the L-BFGS total-only regression, finding #7) before any sink is built; JSONL, human log, and TB all fan out from one record → no divergent field sets.
- **Real loop-interrupt seam.** 42-08 adds `should_stop` checked at both optimizer epoch boundaries, byte-for-byte additive (`None` ⇒ Phase 40 preserved) — the first SIGINT actually breaks the `while True` curriculum loop instead of relying on handler-side magic.
- **Prohibitions are test-backed, not asserted.** All three must-NOTs (false-green, identity leak, masked exit) have dedicated negative tests in 42-09/42-07, with the parity test (42-04 finding #6) preventing a future canonical field from shipping without a registry entry.
- **Grounded seams stay owner-owned.** `STEP_LOG_FIELDS` and monitor thresholds are explicitly provisional/operational (B-2/B-5), surfaced through the existing run-start attention log — consistent with the project's MUST-surface governance for adjudication seams.

## 3. Concerns

**MEDIUM — Substantial I/O inside the SIGINT escalation handler (42-08 Task 1/3, `on_escalate`).**
The synchronous in-handler escalation does `write_status` (atomic temp+fsync+rename), `finalize_summary` (more atomic writes **+ reading `curriculum.jsonl`**), and `h.flush()` before `os._exit(130)`. The rationale (main thread may be stuck in an L-BFGS step) is valid, but performing file reads and re-entering the `logging` module from a signal handler risks re-entrancy: if the main thread is interrupted while it holds an internal logging lock or is mid-write to `curriculum.jsonl`, `on_escalate` can block. `try/except` catches *errors*, not *deadlocks* — and `os._exit` only runs after `on_escalate` returns, so a hang defeats the entire "escalation fires when the main thread is stuck" goal. The escalate test (42-09) asserts "immediate exit, no second checkpoint" but imposes no latency bound, so a hang would pass undetected. Suggested fix: in the handler, do *only* `os._exit(130)` (or at most a single best-effort status flip with no file reads / no lock acquisition); defer `finalize_summary` to the graceful path. Add a wall-clock timeout to the escalate test.

**MEDIUM — SIGTERM has no bounded-latency exit path (42-08, OPS-02).**
`should_stop` is checked only at the Adam and L-BFGS *epoch-loop* tops. Within one L-BFGS epoch, `optimizer.step(closure)` runs many un-interruptible line-search closure evaluations, so a stuck line search can delay the graceful SIGTERM indefinitely. Unlike SIGINT, SIGTERM "never escalates," so the only resolution is the OS promoting to SIGKILL — at which point only the launch stub survives (no `interrupted` transition, **no graceful checkpoint**). The OPS-02 acceptance "SIGTERM writes a checkpoint" therefore may not hold precisely when the heartbeat was designed to detect (the L-BFGS trap). Either qualify the acceptance ("checkpoint when a stop boundary is reachable") or add a finer stop-check (e.g., at the L-BFGS closure-invocation boundary).

**MEDIUM — "Monitoring must not materially degrade seconds-per-step" is asserted but never verified (SPEC Constraints).**
No plan contains an acceptance check or test for s/step non-degradation. The design is low-risk (async TB via the writer's background thread, append+flush JSONL with no per-line fsync, daemon heartbeat), but a regression here would be silent and is exactly the kind of constraint that erodes unobserved. A cheap before/after s/step smoke (monitoring on vs. a baseline run) in 42-09 would close it.

**LOW/MEDIUM — Canonical JSONL can have a torn final line under SIGKILL; reader tolerance is implied but untested.**
JSONL is correctly append+flush (Anti-Pattern #4 rejects atomic-rewrite for an append log), but under SIGKILL mid-flush the trailing line can be partial. 42-08's discriminator says "last *parseable* line" (tolerant wording), yet no test covers a non-parseable trailing line under SIGKILL — and `test_step_log_jsonl`'s E1 does `json.loads` *every* line. Since JSONL is the source of truth, a production reader that iterates every line (operator tooling, Phase 43) should be shown to skip a torn tail. Suggest a torn-tail fixture + reader-tolerance test.

**LOW — λ "current values" provenance (42-01 Task 2).**
`ScheduledWeights` stores per-stage *caps* (`_lambda_*_max`) plus a warmup ramp (`λ·min(1, i/I_warm)`); the "current value" at log time is the *ramped* value, not the cap. The plan says "current values from ScheduledWeights" without stating the ramp must be applied — an executor could log the raw caps. Make the ramp evaluation explicit.

**LOW — `config-identity digest` has no cited source (42-06 Task 2).**
The summary header references a "config-identity digest" but no existing digest helper is pointed at. If none exists, the executor invents one (minor scope addition); ground it on the already-frozen `config.yaml` hash or cite the function.

**LOW — Terminal-state precedence hides a divergence that was also interrupted.**
A run that diverged (`finite:false`) *and* then received SIGINT is labeled `interrupted` (stop_requested wins). Defensible, but the divergence then lives only in the JSONL, not in `status.json state` — an operator scanning status sees `interrupted`, not `failed`. Consider surfacing divergence in a secondary field, or document the precedence.

## 4. Suggestions

1. Minimize `on_escalate` to flush-only (or bare `os._exit`); move `finalize_summary` out of the signal handler. Add a bounded-time assertion to the 42-09 escalate case. (Highest-value change.)
2. Either qualify OPS-02's SIGTERM-checkpoint acceptance or add an intra-L-BFGS stop-check so SIGTERM latency is bounded.
3. Add a one-shot s/step non-degradation smoke to 42-09 (the SPEC constraint currently has no verification).
4. Add a torn-JSONL-tail reader-tolerance test; ensure the Phase-43 consumer is known to skip non-parseable trailing lines.
5. In 42-01, state explicitly that logged λ is the warmup-ramped value; in 42-06, ground or define the config-identity digest.
6. Minor doc clarity: 42-08 adds a `RunController.__init__` arg (`should_stop`) while 42-01's Anti-Pattern #3 says "no new constructor argument" — both are correct in context (different concerns) but a one-line note in 42-01 would prevent executor confusion.

## 5. Overall Risk: LOW–MEDIUM

The plans are thorough, well-ordered, grounded in verified prior-phase artifacts, and the honesty/safety-critical paths (false-green, exit-code masking, atomic status, path-traversal inheritance) are correctly defended with tests. The risk concentration is the signal path: I/O inside the escalation handler (re-entrancy/hang) and unbounded SIGTERM latency are the two findings most likely to surface as real bugs during execution. Neither is a blocker — worst case the run still dies honestly via SIGKILL → stub + `not-finished` + staleness — but both deserve the refinements above before/during Wave 3.

---

## Consensus Summary
_Synthesize shared concerns across reviewers above (2+ agreement = highest priority)._

## xreview Diagnostics

### grok
- reviewer=grok
- exit_code=0
- elapsed_seconds=20
- timeout_seconds=360
- watchdog=not_triggered
- command=grok --no-auto-update --no-memory --no-subagents --disable-web-search --permission-mode plan --output-format json -m grok-4.5 --prompt-file /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260719T065558Z-86190/xreview-prompt-42.md 
- grok_json_parse=ok
- grok_raw_stdout_bytes=890
- stdout_bytes=142
- stderr_bytes=0

### codex
- reviewer=codex
- exit_code=0
- elapsed_seconds=306
- timeout_seconds=360
- watchdog=not_triggered
- command=codex exec --ephemeral --dangerously-bypass-hook-trust --model gpt-5.5 -c model_reasoning_effort=\"xhigh\" --skip-git-repo-check - 
- stdout_bytes=3831
- stderr_bytes=482101

### agy
- reviewer=agy
- exit_code=0
- elapsed_seconds=97
- timeout_seconds=360
- watchdog=not_triggered
- stdout_bytes=3914
- stderr_bytes=0

### claude
- reviewer=claude
- exit_code=0
- elapsed_seconds=319
- timeout_seconds=360
- watchdog=not_triggered
- command=ccp pro --model claude-opus-4-8 -p - 
- stdout_bytes=8152
- stderr_bytes=0

### claude-glm
- reviewer=claude-glm
- exit_code=0
- elapsed_seconds=421
- timeout_seconds=540
- watchdog=not_triggered
- command=ccp glm -p - 
- stdout_bytes=9301
- stderr_bytes=192

---

## Verification coverage (cycle 2 source-grounding pass)

Authority resolved once: `drift-guard authority --raw` = **grep** (text-level adapter; a MISSING under grep authority = `needs-acknowledgement`, `hardBlock:false`). No hard-block possible from this pass.

**NEW artifacts (declared under `artifacts_produced`/`must_haves`) — intentionally EXCLUDED from MISSING checks:** `return_details` (42-01, loss_catalog), `RunController.should_stop`/`self._should_stop` (42-08), `self._last_widened_details` (42-01), `closure_state['data_detached']` (42-01), `step_completed` (42-01/02), `MonitorConfig` (42-02), `STEP_LOG_FIELDS`/`step_log_fields_provisional_entry` (42-02), `_sanitize_step_record`/`JsonlStepHandler`/`HumanStepHandler` (42-04), `TbSink` (42-05), `build_status_snapshot`/`write_status`/`HeartbeatThread`/`stub_summary`/`finalize_summary` (42-06), `SignalState`/`note_signal`/`install_signal_handlers`/`on_escalate` (42-08), `scripts/train-unattended.sh`, `configs/stage0-example.yaml`, `tests/phase42/*`.

### Existing-code symbols cited — all VERIFIED

| Symbol / anchor | Verdict | file:line |
|---|---|---|
| `causal_physics_loss` | VERIFIED | pinn/loss_catalog.py:208 |
| `CAUSAL_ETA_C` / `CAUSAL_W1` imports | VERIFIED | pinn/loss_catalog.py:34,35 |
| `weights = torch.exp(-eta*cumsum_excl)` | VERIFIED | pinn/loss_catalog.py:258 |
| `return (weights * rbar).mean()` | VERIFIED | pinn/loss_catalog.py:261 |
| `LossWeights.lambda_e` / `lambda_l` (NOT `lambda_energy`/`lambda_angmom`) | VERIFIED | pinn/loss_catalog.py:75,76 |
| `RunController` | VERIFIED | pinn/training/controllers.py:275 |
| `_log_step` (def) | VERIFIED | pinn/training/controllers.py:570 |
| current `_log_step` emits `event:"step"` + `loss_{k}` prefixed loss keys | VERIFIED | pinn/training/controllers.py:588,593 |
| `_non_data_terms` | VERIFIED | pinn/training/controllers.py:470 |
| `_compose_loss_terms` | VERIFIED | pinn/training/controllers.py:520 |
| `_scalar_loss_terms` | VERIFIED | pinn/training/controllers.py:597 |
| `_run_adam_phase` | VERIFIED | pinn/training/controllers.py:614 |
| `_make_lbfgs_closure` (`weighted_data`:729, `total`:737, `closure_state['last_loss']`:738) | VERIFIED | pinn/training/controllers.py:726 |
| `_run_lbfgs_phase` (separate method; 42-01 mislabels as "run_stage section") | VERIFIED | pinn/training/controllers.py:748 |
| `run_stage` | VERIFIED | pinn/training/controllers.py:864 |
| `CurriculumController` / `.run` | VERIFIED | pinn/training/controllers.py:1021,1346 |
| `build_checkpoint_payload` | VERIFIED | pinn/training/controllers.py:225 |
| `_LOGGER = logging.getLogger("pinn.training.controllers")` | VERIFIED | pinn/training/controllers.py:970 |
| `_global_step` init / Adam-inc / L-BFGS-inc | VERIFIED | pinn/training/controllers.py:324,691,791 |
| `_wall_clock_baseline` | VERIFIED | pinn/training/controllers.py:328 |
| `checkpoint_hook`/`guard_hook` ctor params (stored 329-330) | VERIFIED | pinn/training/controllers.py:298,299 |
| Adam epoch loop `for epoch in range(...)` | VERIFIED | pinn/training/controllers.py:630 |
| Adam guard returns | VERIFIED | pinn/training/controllers.py:665,669,675,680,685 |
| Adam `_log_step` call | VERIFIED | pinn/training/controllers.py:709 |
| L-BFGS epoch loop `for _lbfgs_epoch in range(...)` | VERIFIED | pinn/training/controllers.py:782 |
| `optimizer.step(closure)` | VERIFIED | pinn/training/controllers.py:789 |
| guard-bridge `_scalar_loss_terms(total_for_guard)` | VERIFIED | pinn/training/controllers.py:805 |
| L-BFGS guard returns | VERIFIED | pinn/training/controllers.py:814,818,822 |
| L-BFGS log-site `_scalar_loss_terms(...)` (:838) / `_log_step` call (:836) | VERIFIED | pinn/training/controllers.py:836,838 |
| `GuardConfig`/`CheckpointCadence`/`RunConfig`/`log_every` | VERIFIED | pinn/training/config.py:178,206,242,253 |
| `_require_int`/`_finite_positive`/`_finite_unit_interval` | VERIFIED | pinn/training/config.py:36,58,65 |
| `TrainingConfig.provisional_fields` (ImportError-guarded append idiom) | VERIFIED | pinn/training/config.py:478 |
| `_resolve_nested_cls` known-name dict (GuardConfig/CheckpointCadence/RunConfig/StageConfig/OptConfig/LossConfig) | VERIFIED | pinn/training/config_yaml.py:76 (dict ~93-105) |
| `_map_section` | VERIFIED | pinn/training/config_yaml.py:134 |
| `load_config` | VERIFIED | pinn/training/config_yaml.py:175 |
| `freeze_resolved_config` | VERIFIED | pinn/training/config_yaml.py:263 |
| `RESUME_FIELD_REGISTRY` | VERIFIED | pinn/training/resume.py:46 |
| `resume_field_classification_provisional_entry` | VERIFIED | pinn/training/resume.py:593 |
| `atomic_write_text` | VERIFIED | pinn/training/atomic_io.py:41 |
| `_json_safe_scalar` (do-not-reuse contrast) | VERIFIED | pinn/training/guards.py:124 |
| `_default_memory_signal` (`torch.mps.driver_allocated_memory`) | VERIFIED | pinn/training/guards.py:143,159 |
| `write_failure_bundle` | VERIFIED | pinn/training/guards.py:407 |
| `save_rolling` / `TorchSaveCheckpointStore` | VERIFIED | pinn/training/checkpoint.py:349,188 |
| `StageDisposition` (ADVANCE/RECOVER/HALT only) | VERIFIED | pinn/training/stage_exit.py:30-35 |
| `main` | VERIFIED | pinn/train.py:246 |
| `_resolve_run_dir` (traversal guard) | VERIFIED | pinn/train.py:86 |
| `store = TorchSaveCheckpointStore(...)` | VERIFIED | pinn/train.py:354 |
| `RunController(...)` construction (guard_hook kwarg :480) | VERIFIED | pinn/train.py:467 |
| `checkpoint_hook` / `guard_hook` closures | VERIFIED | pinn/train.py:388,410 |
| `write_failure_bundle(...)` call into `failure/` | VERIFIED | pinn/train.py:444 |
| `curriculum_holder` / `best_val_cell` | VERIFIED | pinn/train.py:369,386 |
| terminal block `try: curriculum.run() except: return 1; print(...); return 0` | VERIFIED | pinn/train.py:533-543 |
| `--resume` flow | VERIFIED | pinn/train.py:251,288 |
| `CONTEXT.md` CTX-71 L-BFGS "between closure evaluations, aborting the in-progress optimizer step" | VERIFIED (grounding contradiction w/ 42-08) | 42-CONTEXT.md:144-145 |
| SPEC OPS-03 JSONL field set (NO per-bin residuals) / OPS-04b residual panel = TensorBoard | VERIFIED | 42-SPEC.md:31,41,90,91 |
| `tests/phase41.__init__._SKIP_PHRASE` / `__all__` | VERIFIED | tests/phase41/__init__.py:27,29 |
| `tests/phase41._fixtures.make_synthetic_stage0_loop` / `make_stub_split_sources` | VERIFIED | tests/phase41/_fixtures.py:81,21 |
| `tests/phase41.test_train_entrypoint._require` (raises SkipTest) / `_write_config` / `_TrainHarness` / `_RUNS_ROOT` monkeypatch | VERIFIED | tests/phase41/test_train_entrypoint.py:27,37,89,100 |

### UNCHECKABLE (grep adapter cannot analyze; NOT counted as missing)
- `torch.mps.current_allocated_memory()` — external torch API (42-06 secondary mem field); not a repo symbol. UNCHECKABLE.
- `caffeinate` / `command -v caffeinate` — external macOS binary (42-07 wrapper + preflight); claude-glm independently confirmed `/usr/bin/caffeinate` present. UNCHECKABLE by repo grep.
- design §5.4 human-log line shape — external design-doc reference, not a code symbol. UNCHECKABLE.

### MISSING / AMBIGUOUS (existing-code)
- None. Every existing-code symbol cited across the nine plans resolves at (or within a few lines of) its cited location.

### Grounding-derived findings (verified, feed the review verdict — not "missing symbols")
1. **Field-record vocabulary/scope is unreconciled** across 42-01 (emitter keeps `event` + `loss_*` prefix + `residuals_bin_*` + `lambda_*` in the shared `extra=`), 42-02 (`STEP_LOG_FIELDS` registers bare `data/ic/phys/energy/angmom`, no `event`, no `residuals_bin_*`), and 42-04 (parity assert `set(obj)-{finite,nonfinite_keys} <= set(STEP_LOG_FIELDS)`). Verified against live `_log_step` (:588,:593) + `LossWeights` (:75-76) + SPEC OPS-03/04b scope. The 42-04 parity test cannot pass as written; per-bin residuals also drift out of OPS-03 (JSONL) scope into the canonical log. → HIGH.
2. **L-BFGS `should_stop` granularity contradicts CTX-71 grounding**: 42-08 checks only at the `_run_lbfgs_phase` epoch-loop top (before `optimizer.step(closure)`:789), but CTX-71 (42-CONTEXT.md:144-145) mandates the check "between closure evaluations, aborting the in-progress optimizer step." A first SIGINT/SIGTERM is not honored during a multi-call L-BFGS line search. → HIGH.
