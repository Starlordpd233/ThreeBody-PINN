---
phase: 42-operator-runbook-surface-monitoring
verified: 2026-07-20
status: human_needed
score: 4/4 success criteria verified
behavior_unverified: 0
overrides_applied: 0
gaps:
  - id: GAP-42-01
    truth: "A periodic `mem:` line appears in `train.log` (OPS-04 / SPEC AC 6)"
    missing: "`emit_mem_line` (pinn/training/heartbeat.py:176) has no caller anywhere in `pinn/`, and `MonitorConfig.mem_every` (pinn/training/config.py:255) is parsed and validated but never read by a producer."
    evidence: "Two real runs of `python -m pinn.train` with `mem_every` set — 251 steps on mps and 252 steps on cpu — produced ZERO `mem:` lines in `runs/<name>/logs/train.log`. The memory FIELDS do reach `status.json` (`heartbeat.update(mem=…)` is wired); only the log line is missing."
    why_tests_missed_it: "`test_mem_field_mirrored_and_mem_line_emitted` calls `emit_mem_line` directly and asserts it formats a line. Nothing asserted that the training loop calls it — a presence test standing in for a wiring test."
    severity: critical
    status: resolved
    resolved_by: "0fae07f — emit_mem_line wired into guard_hook at the mem_every step cadence, plus an end-to-end test asserting the line reaches a real run's train.log"
    resolution_evidence: "Negative control: with the new call site replaced by `pass`, test_mem_line_emitted_into_real_run_train_log fails ('no periodic mem: line in train.log'); restored, it passes. Full suite 38 tests OK."
human_verification:
  - test: "Reviewer-executes-Launch: run `python -m pinn.train --config configs/stage0-example.yaml`, Ctrl-C once mid-run, then `tensorboard --logdir runs/<name>/tb`"
    expected: "The runbook's Launch/Monitor/Resume steps work as written for a reader who has not seen the code; the residual panel plots legibly"
    why_human: "42-VALIDATION Manual-Only: rendering and runbook legibility are visual/UX judgments. Emission and the Ctrl-C contract are automated (test_residual_panel.py, test_signals.py); only the human reading is manual. NON-blocking for phase closure"
  - test: "Sleep prevention: launch `scripts/train-unattended.sh`, then confirm via `pmset -g assertions` that THAT caffeinate pid holds PreventUserIdleSystemSleep, and that an unwrapped `python -m pinn.train` adds no such assertion"
    expected: "The wrapper's own caffeinate holds the assertion for the run's lifetime; the unwrapped launch does not"
    why_human: "42-VALIDATION Manual-Only. NOTE: the original row said 'close lid on AC power' — that contradicts OPS-02's stated lid-OPEN + AC rule and the runbook's 'keep the lid open', and caffeinate does not assert against clamshell sleep, so a literal lid-close would fail for reasons unrelated to the wrapper. This machine also has AC `sleep 0`, `ttyskeepawake 1`, and powerd/duet assertions already held, which makes a wait-for-sleep test vacuous. The assertion-identity check above is the decidable form. NON-blocking for phase closure"
---

# Phase 42: Operator Runbook Surface & Monitoring — Verification Report

**Phase Goal:** A non-expert operator can run, watch, and hand over a training run through five single-command entry points, an unattended-safe launch, canonical logging, and a written runbook — with the `runs/<name>/` directory as the reproducibility contract.

**Verified:** 2026-07-20
**Status:** `human_needed` — all four success criteria verified. GAP-42-01 (the periodic `mem:` line was never emitted) is **resolved** in `0fae07f`; the two Manual-Only items (visual TensorBoard render, real sleep-prevention check) remain and are non-blocking per `42-VALIDATION.md`.
**Branch / HEAD:** `milestone/v2.0` @ `0fae07f` (GAP-42-01 fix)

## Goal Achievement

### Success Criteria

| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 1 | Five entry points each run as a single command; unattended launch under `caffeinate -is`; SIGTERM treated as one graceful Ctrl-C → checkpoint (OPS-01, OPS-02) | ✓ VERIFIED | Runbook §"The Five Entry Points" gives exactly one command per point: `./setup.sh`, `cp configs/stage0-example.yaml …`, `python -m pinn.train --config …`, `tail -f runs/<name>/logs/train.log`, `--resume latest`. All referenced artifacts exist (`setup.sh`, `configs/stage0-example.yaml`, `--resume` at `pinn/train.py:73`). `scripts/train-unattended.sh:9` is `exec caffeinate -is python -m pinn.train "$@"` — no new subcommand surface. SIGTERM: `test_sigterm_graceful_exit_143` asserts exit 143 + `checkpoints/latest.pt` + `status.state == interrupted`. |
| 2 | Widened field set to canonical JSONL with a TensorBoard secondary view; `status.json` heartbeat, `mem:` line, and per-time-bin residual panel make health observable (OPS-03, OPS-04) | ✓ VERIFIED | JSONL, TB panel, and heartbeat all verified — `test_ops03_happy_path_field_presence` + `test_ops03_registry_parity_and_no_residuals_leak` pin the field set against the `STEP_LOG_FIELDS` registry; `test_e1_nonfinite_whole_file_parseability` proves parseability under NaN/Inf; `test_ops04b_panel_present_via_event_accumulator` and `test_ops04b_collapse_nan_roundtrip` read the panel back through `EventAccumulator`; `test_state_sequence_reader_classification_and_staleness_arithmetic`, `test_no_torn_read_under_concurrent_rewrites`, and `test_frozen_step_count_still_refreshes_timestamp` cover the heartbeat. The `mem:` line clause initially failed (GAP-42-01) and is now wired and covered end-to-end by `test_mem_line_emitted_into_real_run_train_log`. |
| 3 | Each run produces the `runs/<name>/` contract that reproduces the result when handed over (OPS-05) | ✓ VERIFIED | `test_success_summary_has_full_member_list` now asserts the directory membership itself — `config.yaml`, `checkpoints/`, `logs/train.log`, `logs/train.log.jsonl`, `tb/` (with real `events.out.tfevents*` data), `summary.md`, `summary.json`, `status.json`, `failure/` — plus the ratified `summary.json` header, six non-null final loss terms, and curriculum progression. Under-failure presence is held by the three SIGKILL-barrier tests and the two honesty tests. |
| 4 | A written runbook under `docs/runbooks/` covers the mental model, five entry points, categorized error surface, and M5-Pro notes (OPS-06) | ✓ VERIFIED | `docs/runbooks/training/2026-07-18-stage0-training-operator-runbook.md` carries all four sections (verified by heading inspection and by `test_runbook_has_mandated_sections`); `test_runbook_config_loads` validates `configs/stage0-example.yaml` through `config_yaml.load_config`. |

**Score:** 4/4 criteria verified (0 present-but-behavior-unverified)

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|----|--------|---------|
| training step loop | `status.json` memory fields | `heartbeat.update(mem=…)` | ✓ WIRED | Real runs show populated `memory.driver_bytes` / `current_bytes` on mps |
| training step loop | `train.log` `mem:` line | `emit_mem_line(...)` at `monitor.mem_every` cadence | ✓ WIRED (`0fae07f`) | Was NOT WIRED at first verification — no caller existed and 251-step (mps) / 252-step (cpu) runs produced zero `mem:` lines. Now emitted from `guard_hook` beside the existing `heartbeat.update(mem=…)`; asserted end-to-end. |

### Critical Gaps (resolved)

1. **GAP-42-01 — the periodic `mem:` line was never emitted** — RESOLVED in `0fae07f`
   - Missing: a production caller for `emit_mem_line` (`pinn/training/heartbeat.py:176`) on the `monitor.mem_every` cadence (`pinn/training/config.py:255`).
   - Impact: OPS-04 and SPEC acceptance criterion 6 both name a periodic `mem:` line in `train.log` as part of how the operator answers "is it alive / healthy?". An operator tailing `train.log` — the runbook's own Monitor step — never sees memory pressure. The `status.json` mirror still works, so the gap is one surface, not the whole requirement.
   - Fix: call `emit_mem_line(mem_fields)` from the same main-thread update that already pushes `mem=` into the heartbeat, gated on `step % monitor.mem_every == 0`; then add a test that asserts the line appears in a real run's `train.log`, not one that calls the emitter directly.

### How this was missed

`test_mem_field_mirrored_and_mem_line_emitted` calls `emit_mem_line` itself and asserts the output format. That proves the function works; it says nothing about whether anything invokes it. The gap surfaced only when a real `python -m pinn.train` was run and its `train.log` grepped. Every other OPS-04 clause has an end-to-end assertion; this one did not.

### SPEC Acceptance Criteria

All eleven `42-SPEC.md` acceptance criteria have automated coverage in `tests/phase42`:

| AC | Automated evidence |
|----|--------------------|
| Runbook documents five entry points, no new CLI beyond the wrapper | `test_runbook_has_mandated_sections` + heading inspection |
| Committed `caffeinate -is` wrapper | `scripts/train-unattended.sh` (tracked); `test_guard_trip_returns_nonzero_exit` |
| SIGINT-once / SIGINT-twice / SIGTERM contract | `test_signals.py` — 8 cases incl. the deterministic `note_signal` bracket |
| Widened JSONL field set + human mirror line | `test_ops03_happy_path_field_presence`, `test_ops03_registry_parity_and_no_residuals_leak` |
| `tb/` event data incl. residual panel + `w_n` scalars under collapse | `test_ops04b_panel_present_via_event_accumulator`, `test_ops04b_collapse_nan_roundtrip` |
| `status.json` running-vs-stalled from timestamp age; state transitions; periodic `mem:` line | `test_state_sequence_reader_classification_and_staleness_arithmetic`, `test_mem_field_mirrored_and_mem_line_emitted`, the three SIGKILL-barrier tests |
| Complete `runs/<name>/` contract; `summary.md` present even on failure | `test_success_summary_has_full_member_list`, `test_sigkill_*_presence_and_staleness` |
| Runbook four sections + example config validates | `test_runbook_has_mandated_sections`, `test_runbook_config_loads` |
| must-NOT #1 — no false-green | `test_forced_halt_catchable_state_not_finished_and_no_fabricated_metrics`, `test_forced_divergence_catchable_state_not_finished` |
| must-NOT #2 — no leaked paths/hostnames/secrets | `test_no_forbidden_shapes_in_artifacts`, `test_summary_md_has_no_env_fingerprint` |
| must-NOT #3 — wrapper does not swallow non-zero exit | `test_guard_trip_returns_nonzero_exit` |

## Validation Evidence

```
<home>/miniforge3/bin/conda run -n pinn-train \
    python -m unittest discover -s tests/phase42 -p 'test_*.py' -v
Ran 37 tests — OK   (no skips)
```

Repository-wide regression (`-s tests`): **840 tests, 1 failure** —
`phase39.test_prohibitions.SoleReaderAuditTests.test_only_allowed_modules_parse_the_corpus`
flags `pinn/training/guards.py` as an unauthorized corpus reader.

**This failure is pre-existing and unrelated to Phase 42.** The detector treats the bare
substring `.txt` as evidence that a module parses the Brutus corpus
(`tests/phase39/test_prohibitions.py:63`). `guards.py` never reads the corpus; it *writes*
`failure/README.txt`, the Tier-A failure bundle introduced by Phase 41 (`46f83667`,
`guards.py:452`). Neither `pinn/` nor `tests/phase39/` is touched by any Phase-42 commit,
and both files last changed on 2026-07-15 / 2026-07-18. Left for a Phase-39 or Phase-43
follow-up: the fix is to narrow `_CORPUS_TOKENS` to a read-shaped pattern (or to exempt
write targets), not to rename the failure-bundle artifact.

## Findings Recorded, Not Acted On

Two production-code observations surfaced while realizing the held-out tests. Both are
outside plan 42-09's tests-only scope and neither breaks a Phase-42 criterion:

1. **L-BFGS `strong_wolfe` line-search stall.** On the synthetic Stage-0 landscape a large
   `lbfgs_max_iter` makes the first `optimizer.step(closure)` run far past a 120 s window.
   Real pathological losses could do the same. Worth a Phase-43 look; the stop seam itself
   is proven to fire between closure evaluations (`test_sigint_mid_lbfgs_closure_stops_between_evals`).
2. **Post-`restore_handlers()` SIGINT window.** `finish_run` restores the default SIGINT
   disposition last (`pinn/train.py:380`), so a further Ctrl-C during interpreter teardown
   kills the process by signal rather than via `sys.exit(130)`. Everything durable —
   checkpoint, `status.json` terminal transition, summary — has already been written by then,
   so the run contract holds; the shell reports 130 either way. Hardening would mean holding
   handlers through teardown, a production change outside this plan.

## Human Verification Required

Both items are the `42-VALIDATION.md` Manual-Only rows and are **non-blocking** for closure:
the TensorBoard render is a visual judgment (emission is automated) and the lid-close sleep
test needs real hardware state (the wrapper's exit-status propagation is automated).
