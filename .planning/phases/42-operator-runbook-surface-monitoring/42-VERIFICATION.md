---
phase: 42-operator-runbook-surface-monitoring
verified: 2026-07-20
status: human_needed
score: 4/4 success criteria verified
behavior_unverified: 0
overrides_applied: 0
gaps: []
deferred: []
human_verification:
  - test: "Reviewer-executes-Launch: run `python -m pinn.train --config configs/stage0-example.yaml`, Ctrl-C once mid-run, then `tensorboard --logdir runs/<name>/tb`"
    expected: "The runbook's Launch/Monitor/Resume steps work as written for a reader who has not seen the code; the residual panel plots legibly"
    why_human: "42-VALIDATION Manual-Only: rendering and runbook legibility are visual/UX judgments. Emission and the Ctrl-C contract are automated (test_residual_panel.py, test_signals.py); only the human reading is manual. NON-blocking for phase closure"
  - test: "macOS sleep actually prevented under `caffeinate -is` with the lid closed on AC power"
    expected: "The run continues across a lid-close on AC power"
    why_human: "42-VALIDATION Manual-Only: requires real hardware sleep/lid state. The wrapper's exit-status propagation IS automated (test_wrapper_exit.py). NON-blocking for phase closure"
---

# Phase 42: Operator Runbook Surface & Monitoring — Verification Report

**Phase Goal:** A non-expert operator can run, watch, and hand over a training run through five single-command entry points, an unattended-safe launch, canonical logging, and a written runbook — with the `runs/<name>/` directory as the reproducibility contract.

**Verified:** 2026-07-20
**Status:** `human_needed` — all four success criteria verified against live code and a green suite; the two carried Manual-Only items (visual TensorBoard render, real lid-close sleep test) remain and are non-blocking per `42-VALIDATION.md`.
**Branch / HEAD:** `milestone/v2.0` @ `4e977d3d`

## Goal Achievement

### Success Criteria

| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 1 | Five entry points each run as a single command; unattended launch under `caffeinate -is`; SIGTERM treated as one graceful Ctrl-C → checkpoint (OPS-01, OPS-02) | ✓ VERIFIED | Runbook §"The Five Entry Points" gives exactly one command per point: `./setup.sh`, `cp configs/stage0-example.yaml …`, `python -m pinn.train --config …`, `tail -f runs/<name>/logs/train.log`, `--resume latest`. All referenced artifacts exist (`setup.sh`, `configs/stage0-example.yaml`, `--resume` at `pinn/train.py:73`). `scripts/train-unattended.sh:9` is `exec caffeinate -is python -m pinn.train "$@"` — no new subcommand surface. SIGTERM: `test_sigterm_graceful_exit_143` asserts exit 143 + `checkpoints/latest.pt` + `status.state == interrupted`. |
| 2 | Widened field set to canonical JSONL with a TensorBoard secondary view; `status.json` heartbeat, `mem:` line, and per-time-bin residual panel make health observable (OPS-03, OPS-04) | ✓ VERIFIED | `test_ops03_happy_path_field_presence` + `test_ops03_registry_parity_and_no_residuals_leak` pin the field set against the `STEP_LOG_FIELDS` registry (`pinn/training/step_log.py`); `test_e1_nonfinite_whole_file_parseability` proves the whole file stays parseable under NaN/Inf. Panel: `test_ops04b_panel_present_via_event_accumulator` and `test_ops04b_collapse_nan_roundtrip` read back through `EventAccumulator`, so emission survives `w_n` collapse. Heartbeat: `test_state_sequence_reader_classification_and_staleness_arithmetic`, `test_no_torn_read_under_concurrent_rewrites`, `test_frozen_step_count_still_refreshes_timestamp`, `test_mem_field_mirrored_and_mem_line_emitted`. |
| 3 | Each run produces the `runs/<name>/` contract that reproduces the result when handed over (OPS-05) | ✓ VERIFIED | `test_success_summary_has_full_member_list` now asserts the directory membership itself — `config.yaml`, `checkpoints/`, `logs/train.log`, `logs/train.log.jsonl`, `tb/` (with real `events.out.tfevents*` data), `summary.md`, `summary.json`, `status.json`, `failure/` — plus the ratified `summary.json` header, six non-null final loss terms, and curriculum progression. Under-failure presence is held by the three SIGKILL-barrier tests and the two honesty tests. |
| 4 | A written runbook under `docs/runbooks/` covers the mental model, five entry points, categorized error surface, and M5-Pro notes (OPS-06) | ✓ VERIFIED | `docs/runbooks/training/2026-07-18-stage0-training-operator-runbook.md` carries all four sections (verified by heading inspection and by `test_runbook_has_mandated_sections`); `test_runbook_config_loads` validates `configs/stage0-example.yaml` through `config_yaml.load_config`. |

**Score:** 4/4 criteria verified (0 present-but-behavior-unverified)

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
