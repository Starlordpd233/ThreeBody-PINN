---
phase: 42-operator-runbook-surface-monitoring
plan: 06
status: complete
completed: 2026-07-19
---

# Plan 42-06 Summary

## What was built

The liveness + honesty surface (OPS-04a / OPS-05 / Edge E3): a `status.json`
timestamped heartbeat that answers "is it alive / healthy?" from a single
atomically-rewritten file (freshness ≡ process liveness, robust to the L-BFGS
line-search trap), the periodic `mem:` line, and the stub-then-finalize
`summary.md` / `summary.json` one-pager that is present under every death mode and
never reports success it did not observe. Pure schema/render/write functions + the
daemon thread class; the thread is started/stopped at the composition root (42-08).

### 1. heartbeat.py (`pinn/training/heartbeat.py`)

- `build_status_snapshot(...)` — pure builder returning the CTX-75 schema dict:
  `schema_version`, `run_name`, `pid`, `state` ∈ {initializing, running, finished,
  failed, interrupted}, `timestamp_utc` (ISO-8601) + `timestamp_epoch` (float),
  `heartbeat_interval_secs`, `staleness_threshold_secs = heartbeat_secs *
  staleness_factor` (the file carries its own threshold so a reader needs no
  external constant), `step`/`stage`/`phase`/`epoch`, the five loss terms + `total`
  under the CTX-67 null policy, `lr`/`s_per_step_ema`/`eta_seconds`, and the memory
  fields. The `initializing` snapshot has `step: null` and null losses (never
  fabricated — Anti-Pattern #7).
- `write_status(path, snapshot)` — serializes with `allow_nan=False` and reuses
  `atomic_io.atomic_write_text` (temp + fsync + os.replace + dir fsync); the rename
  is the only state-visible mutation, so a reader never sees truncated JSON (E3).
  Atomic write is reused, NOT reimplemented (`grep -c 'def atomic_write_text'` = 0).
- `HeartbeatThread(threading.Thread, daemon=True)` — rewrites `status.json` on the
  K-second cadence from a mutex-guarded snapshot; `update(**fields)` (step loop
  pushes step/losses/mem; synchronous rewrite at every logged step), `transition(
  state)` (synchronous rewrite at a state transition), `write_initial()` (startup
  `initializing` snapshot), and `stop()`. A write exception is swallowed warn-once —
  the monitoring thread never crashes the process (threat T-42-04).
  - **Memory-sampling discipline (cycle-2, claude MEDIUM):** the daemon `run()` body
    contains ZERO `torch.mps.*` calls (verified via `inspect.getsource`). MPS APIs
    are main-thread-affine; the MAIN step loop samples once per logged step via
    `sample_memory_fields()` (reusing `guards._default_memory_signal` for
    driver-allocated + `torch.mps.current_allocated_memory` as the secondary field;
    no new dependency) and pushes the cached value via `update(mem=...)`.
    `build_status_snapshot` takes the pre-sampled `mem` and performs no MPS query.
  - **Thread-safety (cycle-2, agy LOW):** one mutex guards BOTH snapshot generation
    AND the `write_status` I/O — the daemon tick, `update(...)`, and `transition(
    state)` each take the same lock, build the snapshot, and write UNDER it, so a
    synchronous main-thread `transition()` and a daemon tick never race on
    `atomic_write_text`'s shared `.tmp.{pid}` suffix (preserving E3 under
    contention).
- `emit_mem_line(mem_fields)` — emits the periodic `mem:` line to `train.log` via
  `logging.getLogger("pinn.training.heartbeat")` from the SAME main-thread update
  that cached the value (never from the daemon).

### 2. summary.py (`pinn/training/summary.py`)

- `stub_summary(run_dir, *, header)` — writes `summary.md` + `summary.json` at
  launch marked "in progress / did not complete" with no fabricated metrics, via
  `atomic_write_text`. Presence is thereby guaranteed under every death mode
  including SIGKILL (E4) — a write-at-exit-only design cannot satisfy this.
- `finalize_summary(run_dir, *, disposition, header, final_losses, curriculum_path)`
  — atomically replaces both files with the terminal one-pager (finished / failed /
  interrupted): run header (name, start/end UTC, wall-clock, device+precision, seed,
  config-identity digest), final five loss terms + total under the CTX-67 null
  policy (a term that never finalized stays null — never a placeholder), curriculum
  progression RENDERED from `runs/<name>/curriculum.jsonl` (not recomputed), and the
  terminal disposition.
  - **Config-identity digest:** `sha256((run_dir/"config.yaml").read_bytes())
    .hexdigest()[:16]` over the frozen resolved config that
    `config_yaml.freeze_resolved_config` writes at launch (cited in a comment at the
    computation site); a missing/unreadable file yields `null`, never an invented
    digest.
  - **Honesty (must-NOT #1):** the failed/interrupted templates name the state,
    leave metrics null, and deliberately avoid the substring "finished" so a
    non-success one-pager can never read as a success.
  - **B-6/D-12 env-fingerprint** (`sw_vers`, `python -V`, torch version/build) lives
    in the `summary.json` run header ONLY — never in `summary.md`.
  - **Redaction (must-NOT #2 / CTX-79):** the one-pager records run-directory-relative
    identity only; no `/Users/…` absolute paths, hostnames, or secrets are emitted.

### 3. test_status_heartbeat (`tests/phase42/test_status_heartbeat.py`)

Realized the 42-03 stub (production-symbol `_require` skip guard dropped; the
pinn-train availability guard kept). Ten tests:

- **OPS-04a state sequence + reader classification** — snapshots across
  initializing → running → finished/interrupted/failed; a test-local reader
  classifies running-vs-stalled from `now − timestamp_epoch >
  staleness_threshold_secs` using only the file's carried fields.
- **E3 staleness arithmetic** — the stalled classification is asserted by
  manipulating `timestamp_epoch` directly (no real wall-clock wait for K seconds).
- **E3 startup** — the `initializing` snapshot has `step: null` and null losses;
  non-finite (NaN/Inf) losses serialize as JSON `null` under `allow_nan=False`.
- **E3 atomicity** — a daemon on a fast cadence PLUS 400 synchronous main-thread
  `update()` rewrites run while a polling reader `json.loads` the file repeatedly;
  every read is a complete parseable object (no torn read).
- **mem field/line** — pre-sampled `mem` is mirrored into the snapshot memory
  fields; `emit_mem_line` emits a `mem:` line on the heartbeat logger;
  `sample_memory_fields` returns int-or-null.
- **Liveness (CTX-74)** — a frozen step count still refreshes `timestamp_epoch`
  (freshness ≡ process liveness; fresh ⇒ not stalled).
- **Memory discipline** — `inspect.getsource(HeartbeatThread.run)` contains no
  `torch.mps` call.
- **Thread-safety** — `transition()` forces a synchronous rewrite (no cadence wait).

## Execution notes

No plan deviations. Two within-plan discretions: (1) the running-vs-stalled reader
is a small test-local helper (the plan specifies the reader conceptually as the
arithmetic on the file's carried fields; no reader function is a heartbeat.py
artifact); (2) the E3 atomicity test drives rewrites through BOTH the daemon (fast
cadence) and the synchronous `update()` path — the two rewrite sources the plan
offers — to stress the mutex + atomic-rename invariant from two concurrent writers.

## Verification

Env: `conda run -n pinn-train`.

- `tests.phase42.test_status_heartbeat -v`: **10/10 pass**, not skipped ✓
- Phase 42 suite regression (`discover tests/phase42`): **25 tests, OK (8 skipped)**
  — the 8 skips are the not-yet-realized 42-07/08/09 stubs; no sibling broke ✓
- Task 1 inline smoke: `build_status_snapshot(state='initializing', …)` → `OK status`
  (null step, null losses, `staleness_threshold_secs == 90`, fresh `timestamp_epoch`,
  parses under `allow_nan=False`); `HeartbeatThread` class check → `OK thread class` ✓
- Task 2 inline smoke: `stub_summary` + `finalize_summary(disposition='failed')` →
  `OK summary` (stub marked in-progress; failed one-pager names `failed`, no
  `finished`) ✓
- Lifecycle smoke: `write_initial` (initializing, null losses) → `update(step=5)` →
  `transition('finished')`; every intermediate read parses complete ✓
- Grep gates: `grep -c 'def atomic_write_text' heartbeat.py` = 0; `grep -c
  'atomic_write_text' heartbeat.py` = 5 (≥1); `grep -c 'psutil' heartbeat.py` = 0;
  `grep -c 'atomic_write_text' summary.py` = 8 (≥1); `grep -c 'psutil' summary.py`
  = 0 ✓
- Daemon `run()` body `torch.mps` count (via `inspect.getsource`) = 0 ✓
- Adversarial honesty/redaction: failed path is redacted (no `/Users/`), env-
  fingerprint is JSON-only (absent from `summary.md`), config-identity digest is 16
  hex chars, final losses all null, curriculum rendered (2 records); finished path
  renders `total = 1.5` and keeps canonical loss terms only ✓
- `python -m py_compile` clean on `heartbeat.py`, `summary.py`,
  `test_status_heartbeat.py` ✓

## Files modified

- `pinn/training/heartbeat.py` (new) — `build_status_snapshot` (CTX-75 schema,
  null-loss `initializing`, self-describing `staleness_threshold_secs`),
  `write_status` (`atomic_write_text` reuse), `HeartbeatThread` (daemon;
  `write_initial`/`update`/`transition`/`stop`; mutex guards build + write; no MPS
  in `run()`), `sample_memory_fields` + `emit_mem_line` (main-thread `mem:` signal).
- `pinn/training/summary.py` (new) — `stub_summary` + `finalize_summary`
  (stub-then-finalize; finished/failed/interrupted templates; curriculum.jsonl
  render; config-identity digest from `freeze_resolved_config`'s frozen bytes;
  env-fingerprint in `summary.json` only; null-not-fabricated; redacted).
- `tests/phase42/test_status_heartbeat.py` — realized OPS-04a + E3 startup/atomicity/
  staleness tests (10 tests).
