---
phase: 42
slug: operator-runbook-surface-monitoring
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: validated
nyquist_compliant: true
wave_0_complete: true
created: 2026-07-18
---

# Phase 42 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
> Full validation architecture (per-edge test design + Nyquist sampling logic) lives in
> `42-RESEARCH.md` → `## Validation Architecture`. This file is the executable sampling
> contract; the Per-Task Verification Map is finalized once the planner assigns task IDs.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Python stdlib `unittest` (deferred-import skip guards, per `tests/phase40`/`tests/phase41`) |
| **Config file** | none — tests are stdlib; conda env `pinn-train` provides torch/tensorboard/PyYAML |
| **Quick run command** | `<home>/miniforge3/bin/conda run -n pinn-train python -m unittest discover -s tests/phase42` |
| **Full suite command** | `<home>/miniforge3/bin/conda run -n pinn-train python -m unittest discover -s tests` |
| **Estimated runtime** | ~30–90 s (dataset-free synthetic Stage-0 loops; `_synthetic_split_sources`, population floor 240) |

---

## Sampling Rate

- **After every task commit:** Run the phase-42 quick command (the touched `tests/phase42/test_*.py`).
- **After every plan wave:** Run the full `tests/phase42` suite.
- **Before `/gsd-verify-work`:** Full suite green, including the E1–E4 held-out edge tests and the 3 must-NOT negative tests.
- **Max feedback latency:** ~90 s.

---

## Per-Task Verification Map

> Task IDs are assigned by the planner (`42-NN-MM`). Each requirement below maps to the
> `42-RESEARCH.md` Validation Architecture entry; `/gsd-validate-phase` finalizes the Task-ID
> and Threat-Ref columns after plans exist. Rows here are the requirement→test skeleton the
> planner MUST realize as `<automated>` verify blocks.

| Requirement | Edge / must-NOT | Secure/Correct Behavior | Test Type | Automated Target (tests/phase42/) | File Exists | Status |
|-------------|-----------------|-------------------------|-----------|-----------------------------------|-------------|--------|
| OPS-03 | E1 non-finite | Every JSONL line parses under NaN/Inf; `finite:false` + `nonfinite_keys` present; no string sentinels | unit | `test_step_log_jsonl.py` | ✅ | ✅ green |
| OPS-02 | E2 signal race | SIGINT-once → checkpoint + exit 130; SIGINT-twice → immediate exit; SIGTERM → one graceful checkpoint (exit 143); ~1 s debounce; checkpoint atomic (temp+rename) | integration | `test_signals.py` | ✅ | ✅ green |
| OPS-04a | E3 status.json | `initializing` before step 0 (null losses); atomic rewrite never truncated; `now − ts > threshold ⇒ stalled`; freshness ≡ process liveness under frozen step count | unit | `test_status_heartbeat.py` | ✅ | ✅ green |
| OPS-04b | (R5) panel-under-failure | Per-bin residual + `w_n` scalars emit even under collapse/NaN; **read back via `EventAccumulator`** (NaN reads as 0.0 through `EventFileLoader`) | unit | `test_residual_panel.py` | ✅ | ✅ green |
| OPS-05 | E4 partial run | Killed/failed run still yields honest `runs/<name>/`; `state ∈ {failed,interrupted}` for **catchable** deaths (SIGINT/SIGTERM, guard-HALT, divergence); SIGKILL is uncatchable so status.json keeps its last heartbeat state and staleness stays decidable from `timestamp_epoch` + `staleness_threshold_secs` — never a fabricated terminal state (ratified in 42-09-PLAN E4); `failure/` populated on guard trip; `summary.md` present as failed template | integration | `test_runs_contract.py` | ✅ | ✅ green |
| OPS-04/05 | must-NOT #1 false-green | NaN/guard-HALT run ⇒ `state ≠ finished` and no fabricated/placeholder metrics in `summary.*` | unit | `test_honesty_layer.py` | ✅ | ✅ green |
| OPS-03/04/05 | must-NOT #2 leak | `train.log(.jsonl)`, `status.json`, `summary.*`, `failure/` contain no `/Users/`, hostname, or secret | unit | `test_redaction.py` | ✅ | ✅ green |
| OPS-02 | must-NOT #3 masked exit | wrapper exit status == inner `train.py` exit status | unit | `test_wrapper_exit.py` | ✅ | ✅ green |
| OPS-01/06 | — | Runbook 4 sections present; example `configs/stage0-example.yaml` loads via `load_config` without error | unit | `test_runbook_config.py` | ✅ | ✅ green |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [x] `tests/phase42/__init__.py` + a shared synthetic Stage-0 fixture helper (`make_synthetic_stage0_loop` / reuse `_synthetic_split_sources`, population floor 240) — analog to `tests/phase41`.
- [x] `tests/phase42/test_*.py` stubs for the nine rows above (OPS-01..06 + E1–E4 + 3 must-NOT), each with the `tests/phase41` deferred-import skip-phrase guard so a missing `pinn-train` env skips rather than errors.
- [x] No framework install — stdlib `unittest` present; tensorboard 2.21.0 + PyYAML verified in `pinn-train`.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| macOS sleep actually prevented under `caffeinate -is` (lid-open + AC) | OPS-02 | Requires real hardware sleep/lid state; not reproducible in unittest | Launch the wrapper, close lid on AC power, confirm the run continues (runbook §M5-Pro notes). The wrapper's exit-code propagation IS automated (`test_wrapper_exit.py`). |
| TensorBoard renders the residual panel legibly | OPS-04b | Visual/UX judgment of the rendered panel | `tensorboard --logdir runs/<name>/tb`; confirm `residuals/bin_*` and `causal/*` scalars plot. Emission is automated; rendering is manual. |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 90s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** validated 2026-07-20 at phase closure — all nine rows green in the 37-test `tests/phase42` suite (0 skips). Feedback latency note: the realized suite runs ~5 min, not the ~90 s estimated at planning time, because the E2/E4 rows drive real subprocess training runs and real signal delivery; the per-module quick command stays well under a minute.
