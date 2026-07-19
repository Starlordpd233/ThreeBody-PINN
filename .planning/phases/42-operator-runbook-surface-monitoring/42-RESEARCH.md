# Phase 42: Operator Runbook Surface & Monitoring - Research

**Researched:** 2026-07-18
**Domain:** Operator surface + monitoring layer on a PyTorch/MPS training loop (signals, structured logging, TensorBoard, atomic status files)
**Confidence:** HIGH

> **Scope note.** `42-CONTEXT.md` (CTX-65..81) is exceptionally complete and is the
> locked mechanism set. This document does not restate it — it verifies the
> mechanisms against the actual code and the actual installed library versions,
> and reports the delta: three places where the current code contradicts or
> under-specifies what CTX-65..81 requires, one TensorBoard read-path quirk
> confirmed by direct execution, and the concrete Validation Architecture the
> nyquist step requires.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

Full rationale for every row lives in `42-CONTEXT.md` — this is a compact
index, not a restatement, so the planner can cross-reference without
re-reading ~250 lines of decision prose. Each entry is the decision's own
lead clause.

| CTX | Fills | Locked mechanism (lead clause, near-verbatim) |
|-----|-------|------------------------------------------------|
| CTX-65 | OPS-03 emission point | "The widened field set is produced at the existing single emission point — `RunController._log_step`... by widening its `extra` payload." Emission ordering: "the step record is emitted after loss computation **regardless of guard outcome**." |
| CTX-66 | OPS-03 sink formats | JSONL = one JSON object per logged step via `json.dumps(..., allow_nan=False)`, append-mode, flushed per step, no per-line fsync. Human `train.log` mirrors the design §5.4 line shape. Cadence = existing `run.log_every` — **do not rename the field**. |
| CTX-67 | E1 mechanism | NaN/Inf serializes as JSON `null` + `"finite": false` + `"nonfinite_keys": [...]`. String sentinels are prohibited in the canonical log; `guards._json_safe_scalar`'s sentinel is `trip.json`-local only — **must not** be reused for the JSONL formatter. |
| CTX-68 | B-2 seam | The field set ships as a `STEP_LOG_FIELDS` registry, tagged provisional, surfaced via `provisional_fields()`; **owner ratifies the final list before run #1** — not a Phase-42 pick. |
| CTX-69 | OPS-03 TB mechanism | `torch.utils.tensorboard.SummaryWriter`, constructed at the composition root, `log_dir=runs/<name>/tb/`, fed from the same widened record. JSONL stays canonical (D2); TB is derived and **always-on**. Any TB sink failure logs one warning and never aborts training. |
| CTX-70 | OPS-04b panel content | Per-bin residual scalars `residuals/bin_{n:02d}` (N_t=16 at Stage 0) + `causal/w_min`, `causal/w_mean`, `causal/w_max`, `causal/front_idx` (= max{n : w_n > 0.5}). Exposure: an **additive** `causal_physics_loss` details path returning **detached** per-bin `R̄_n`/`w_n` — default return type unchanged. Emission is **unconditional**, including under collapse/NaN. |
| CTX-71 | OPS-01/02/E2 signals | Handlers installed **only** in `pinn.train main()`. First SIGINT → stop-flag at step boundaries → checkpoint, `status.json→interrupted`, finalize `summary.md`, exit 130. SIGTERM ≡ first SIGINT (exit 143). **Second SIGINT** → best-effort atomic `status.json` flip, then `os._exit(130)`, no further checkpoint. Debounce ~1s (exact value: discretion). |
| CTX-72 | Graceful checkpoint | Reuses the **existing store path** (`build_checkpoint_payload` + rolling save) — no new checkpoint flavor; resume-after-interrupt is the ordinary `--resume latest` flow. |
| CTX-73 | Wrapper | `scripts/train-unattended.sh` (name: discretion): `exec caffeinate -is python -m pinn.train "$@"`. No machine-specific absolute paths in the script. |
| CTX-74 | OPS-04a/E3 heartbeat | Daemon thread rewriting `status.json` every K seconds (default 30) from a mutex-guarded snapshot, **plus** synchronous rewrites at every state transition and every logged step, via `atomic_write_text`. `state: "initializing"` written immediately after run-dir creation, before model/data build, `step: null`, no fabricated losses. |
| CTX-75 | status.json schema | `schema_version`, `run_name`, `pid`, `state` ∈ {initializing, running, finished, failed, interrupted}, `timestamp_utc` + `timestamp_epoch`, `heartbeat_interval_secs`, `staleness_threshold_secs` (default 3×K, file carries its own threshold), `step`, `stage`, `phase`, `epoch`, latest losses, `lr`, `s_per_step_ema`, `eta_seconds`, memory fields. |
| CTX-76 | `mem:` line | Reuses the **existing guard memory signal** (`torch.mps.driver_allocated_memory`), emitted to `train.log` at a periodic cadence, mirrored into `status.json`. **No new dependency (no psutil).** |
| CTX-77 | OPS-05/E4 summary lifecycle | `summary.md`/`summary.json` written at run start as an honest "did not complete" stub, **atomically replaced** at the terminal transition. Presence guaranteed under every death mode including SIGKILL. B-6/D-12 env-fingerprint fields live in `summary.json`'s run header. Generation lives in `pinn.train`, not controllers. |
| CTX-78 | Directory contract | `logs/`, `tb/`, and an **empty `failure/`** are created at launch. A contract test asserts the full member list on a synthetic run. |
| CTX-79 | must-NOT #2 redaction | All handoff artifacts record paths **relative to the run directory only** — no `/Users/…`, no hostnames, no secrets. A redaction-style negative test greps the artifacts of a synthetic run. |
| CTX-80 | Config | New knobs live in a nested `run.monitor` sub-config (pattern: `run.guards`/`run.checkpoint`): `heartbeat_secs` (default 30), `staleness_factor` (default 3), + discretionary cadence knobs. All **operational** under the locked B-5 classification. `run.log_every` stays the log cadence. |
| CTX-81 | OPS-01/06 | Runbook at `docs/runbooks/training/<YYYY-MM-DD>-stage0-training-operator-runbook.md`. Four mandated sections: mental model; five entry points; categorized error surface; M5-Pro notes. Entry-point mapping is **doc-only, no new CLI**. Example config `configs/stage0-example.yaml` must load through `load_config` without error. |

**Two seams stay owner-owned regardless of this research:** the B-2 field-list
ratification (before run #1, CTX-68) and all R-1/R-2/D4-a threshold values
(Phase-43 pilot). This research does not propose concrete values for either —
see Package Legitimacy Audit and Architecture Patterns for how the plan should
carry them as provisional registries.

### Claude's Discretion

Copied verbatim from `42-CONTEXT.md`:

> Module/file layout for the new code (e.g. `pinn/training/monitor.py` /
> `step_log.py` / `signals.py` under `pinn/training/`) — must extend existing
> seams, never fork them.
>
> Exact debounce window (~1 s), EMA constant for `s_per_step`, TB histogram
> cadence, heartbeat default within 15–60 s, `mem:` cadence, wrapper filename.
>
> ETA definition detail: **current-stage** remaining estimate (v2.0 is
> single-stage Stage-0); `eta_seconds` is null before the s/step EMA warms up.
>
> Human `train.log` line micro-format (must carry the design-§5.4 fields).
>
> TB tag taxonomy beyond the CTX-70 mandated tags.

This research's Recommended Project Structure (below) and Pitfall 8's
`colloc/t_min`/`colloc/t_max` suggestion are proposals *within* this
discretion — not new locked decisions.

### Deferred Ideas (OUT OF SCOPE)

Copied verbatim from `42-CONTEXT.md`:

> None new — discussion stayed within phase scope. (Test-set preview,
> ε_H/SCS gate rendering, run comparison, verify ladder, and threshold
> calibration are already Phase 43 by the roadmap.)
>
> Reviewed Todos (not folded): `d-06-static-epsilon-sensitivity-check.md` —
> a data/physics sensitivity probe, no operator-surface or monitoring
> content. `trainex-r1-research-handoff.md` — research process task, no
> Phase-42 surface.
</user_constraints>

## Summary

Phase 42 wires five new concerns onto the existing Phase 40/41 training loop: OS
signal handling, a widened structured step log (JSONL canonical + human mirror +
TensorBoard), a `status.json` heartbeat, the `runs/<name>/` contract's remaining
members (`logs/`, `tb/`, `summary.*`, populated `failure/`), and operator-facing
docs (`docs/runbooks/training/`, `configs/`). No new external dependency is
introduced — `tensorboard==2.21.0` and PyYAML are already pinned and already
verified importable in `pinn-train` (Phase 41 established PyYAML; an earlier
ENV phase established tensorboard). Every new module is stdlib-only otherwise
(`json`, `logging`, `signal`, `threading`, `time`).

Three findings from direct code inspection sharpen CTX-65..81 in ways the
planner needs at task-writing time, not discovery time:

1. **The current guard-trip control flow in `RunController` returns *before*
   calling `_log_step`, in both the Adam and L-BFGS phases.** CTX-65 requires
   the opposite ("a step that trips a guard still logs"). This is not a bug to
   report and stop on — it is exactly the code Phase 42 exists to change — but
   the planner must know the *exact* return statements that need to move
   relative to the (soon-to-be-widened) log call, or the SPEC's E1 backstop
   ("a NaN/Inf loss/grad step stays written and parseable") will silently fail
   task verification.
2. **`RunController` has no `self._stage` attribute anywhere.** The widened
   payload's `stage` field (CTX-65) cannot be read off `self` the way
   `_active_phase`/`_active_epoch` can — it must be threaded as a new explicit
   parameter from the two call sites, which both already have the stage index
   `k` in scope.
3. **TensorBoard's low-level event reader silently turns a written NaN scalar
   into `0.0`** (verified by direct round-trip in `pinn-train`, tensorboard
   2.21.0) — but only when read via `EventFileLoader.Load()`. The on-disk bytes
   are correct (verified via raw TFRecord parse), and the plugin-facing
   `EventAccumulator` API reads the NaN back correctly. Any Phase 42 test that
   verifies "the panel still emits under NaN" (SPEC AC, OPS-04b) must read back
   through `EventAccumulator`, not `EventFileLoader` — the wrong reader will
   make a correct panel implementation look broken.

**Primary recommendation:** widen `RunController._log_step` in place (thread a
new `stage: int` parameter; move the call ahead of every guard-trip
`return`), attach three sinks (JSONL, human, TensorBoard) to the
`pinn.training.*` logger tree at the `pinn.train` composition root exactly as
CTX-45/65 designed, and build the `status.json`/`summary.*` writers as thin
modules around the *already-existing* `atomic_io.atomic_write_text` — do not
introduce a second atomic-write implementation.

## Architectural Responsibility Map

This is a single-process local CLI tool, not a client/server web app, so the
standard browser/API/CDN tiers do not apply. The equivalent tiers for this
codebase (already established by CTX-45/CTX-65's "composition-root-only side
effects" rule) are:

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Signal handling (SIGINT/SIGTERM) | Composition root (`pinn/train.py main()`) | — | `signal.signal()` only works in the main thread of the main interpreter (verified, see Pitfall 4) — cannot live in a library module or a background thread |
| Widened step-record assembly | Domain library (`RunController._log_step`, `pinn/training/controllers.py`) | — | Single existing emission point (CTX-45); stays inside the pure/importable training package |
| JSONL / human / TensorBoard sinks | Composition root (`pinn.train main()`) | Domain library (formatter/handler classes importable from `pinn/training/`) | CTX-65: "sinks are attached at the composition root, never inside controllers" — the *classes* can live in `pinn/training/`, but *attachment* (constructing the writer, calling `addHandler`) is a `main()`-only side effect |
| `status.json` heartbeat | Composition root (owns the daemon thread lifecycle) | Domain library (schema builder function, pure) | A background thread is a process-level resource; only `main()` should start/stop it |
| `summary.md`/`summary.json` | Composition root (owns launch-time stub + terminal-transition finalize) | Domain library (rendering function, pure) | Needs to run inside every exit path (normal / exception / signal) — only `main()` sees all of them |
| `runs/<name>/` directory contract | Filesystem artifact layer | — | Already owned by `train.py:_resolve_run_dir` (path-traversal guard exists); Phase 42 only adds subdirectories/files under it |
| TensorBoard UI | External viewer process (`tensorboard --logdir`) | — | Out of process; reads the `tb/` artifact layer asynchronously, never talks to the training process |
| Operator docs (runbook, example config) | Documentation / operator layer (`docs/runbooks/`, `configs/`) | — | Consumed by a human, not imported by any module |

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| OPS-01 | Five single-command entry points, internals hidden | Confirmed doc-only surface is sufficient — no new CLI code needed beyond the wrapper; see Architecture Patterns → Entry-Point Mapping and the `docs/README.md` runbook-placement verification below |
| OPS-02 | `caffeinate -is` unattended launch + graceful signal semantics | `man caffeinate` (local, authoritative) confirms `-i`/`-s` semantics and that assertions persist exactly for the wrapped utility's lifetime; Python signal-threading behavior empirically verified; `os._exit` vs `sys.exit` semantics verified — see Pitfalls 4–5, Code Examples 3 and 6 |
| OPS-03 | Widened JSONL + human mirror + TensorBoard secondary view | `_log_step` current implementation read in full (exact line numbers below); `causal_physics_loss` signature read in full — the concrete diff needed to expose `w_n` is scoped precisely; `json.dumps(allow_nan=False)` behavior verified; TensorBoard async-writer internals verified from source | 
| OPS-04a | `status.json` heartbeat + `mem:` line | `atomic_io.atomic_write_text` read in full (reusable as-is); `torch.mps.driver_allocated_memory`/`current_allocated_memory` verified via official docs (context7) and live execution |
| OPS-04b | Per-time-bin residual panel | `_build_anchor_context`/`_non_data_terms` read in full — confirms collocation-time sort order and the Adam-phase resampling-per-epoch behavior that constrains what "bin index n" means; TensorBoard NaN round-trip verified empirically (the load-bearing finding for this requirement's must-emit-under-NaN AC) |
| OPS-05 | `runs/<name>/` contract + summary one-pager | `build_checkpoint_payload`, `TorchSaveCheckpointStore` cadence/`curriculum.jsonl` methods read; existing `pinn/verification/*_probe.py` summary.md precedent found (atomic write + `chmod(0o600)`) |
| OPS-06 | Runbook + example config | `docs/README.md` runbook section read in full; an existing runbook's frontmatter usage verified directly (precedent exists in practice beyond the README's literal `docs/work/`-only scope) |

</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| `tensorboard` | 2.21.0 `[VERIFIED: installed in pinn-train, import tensorboard; print(tensorboard.__version__)]` | Secondary monitoring view, `runs/<name>/tb/` | Already pinned (`requirements-lock.txt:17`), already the D2/CTX-69 locked choice; no alternative to research |
| PyYAML | 6.0.3 latest on PyPI `[VERIFIED: pip index versions pyyaml]`; project version already established by Phase 41 (CTX-50) | Nothing new for Phase 42 — `run.monitor` is additive keys on the existing `load_config` path | Confirms no re-verification of the YAML loader itself is needed; only the additive schema |

### Supporting (Python stdlib — no install needed)
| Module | Purpose | When to Use |
|--------|---------|-------------|
| `signal` | SIGINT/SIGTERM handler installation | `main()` only (verified main-thread-only restriction, Pitfall 4) |
| `threading` | Daemon heartbeat thread | `daemon=True` so it never blocks process exit; mutex-guard the snapshot the step loop writes into |
| `json` | JSONL serialization | `json.dumps(record, allow_nan=False)` — never the default `allow_nan=True` (Pitfall 1) |
| `logging` | Sink attachment point | Reuse the existing `pinn.training.*` tree (CTX-45); attach a `logging.Handler` subclass, do not create a parallel logging system |
| `time.monotonic()` | s/step EMA + ETA | `RunController` already tracks one `time.monotonic()` baseline (`self._wall_clock_baseline`, set once at `__init__`); Phase 42 needs a *second*, per-step-delta clock — see Pitfall 8 |

### Alternatives Considered
Already exhaustively covered in `42-DISCUSSION-LOG.md` (SummaryWriter vs. separate tailer process vs. synchronous matplotlib; per-bin scalars vs. histograms vs. rendered images) — not re-derived here. The one alternative worth flagging as newly informed by this research: a **separate tailer process reading `train.log.jsonl`** (the discussion log's rejected "purest derived view" option) would have sidestepped the TensorBoard NaN-readback quirk (Pitfall 3) entirely, since it would own its own read path. This does not change the locked decision (`SummaryWriter` fed from the same record, CTX-69) — the quirk is fully mitigated by using `EventAccumulator` in tests — but it explains *why* that quirk exists: `SummaryWriter`'s writer and a naive reader are two independently-evolved code paths inside the `tensorboard` package itself, not something this project's code caused.

**Installation:** None. `tensorboard` and `PyYAML` are already present; nothing to add to `environment.yml` / `requirements-lock.txt` for Phase 42.

**Version verification performed:**
```bash
<home>/miniforge3/bin/conda run -n pinn-train python -c \
  "import tensorboard, torch; print(tensorboard.__version__, torch.__version__)"
# -> 2.21.0 2.12.1
pip index versions tensorboard   # latest on PyPI: 2.21.0 (matches installed — current)
pip index versions pyyaml        # latest on PyPI: 6.0.3
```

## Package Legitimacy Audit

No new packages are installed by this phase. Both runtime dependencies Phase 42
activates for the first time as load-bearing (tensorboard) or extends (PyYAML)
were already present before this research ran. The legitimacy gate was still
run for completeness:

| Package | Registry | Age (per registry publish date) | Downloads | Source Repo | Verdict (seam) | Disposition |
|---------|----------|-----|-----------|-------------|---------|-------------|
| `tensorboard` | PyPI | Latest release (2.21.0) published 2026-06-29 (~3 weeks before this research) | seam reported `unknown-downloads` (API gap, not zero) | `github.com/tensorflow/tensorboard` | `[SUS]` (`too-new`, `unknown-downloads`) | **Approved — false positive, see note** |
| `pyyaml` | PyPI | Latest release 2025-09-25 | seam reported `unknown-downloads` (API gap) | `pyyaml.org` | `[SUS]` (`unknown-downloads`) | **Approved — false positive, see note** |

**Note on the SUS verdicts:** both flags are artifacts of the legitimacy seam's
automated signals, not genuine risk indicators, and neither package is being
newly installed by this phase:
- `tensorboard`'s `too-new` flag fires because TensorFlow ships tensorboard
  releases frequently; `pip index versions tensorboard` shows an unbroken,
  coherent version history back to `1.6.0` (2018), and the repo is the
  first-party `tensorflow/tensorboard` GitHub org — there is no slopsquatting
  signal here, just a fast release cadence.
- `unknown-downloads` on both packages reflects a gap in the seam's
  downloads-count probe (returned `null`, not a low number) for two of the
  most widely-used packages in the Python ML ecosystem; PyYAML in particular
  is already the CTX-50-mandated parser used throughout Phase 41.
- Neither package triggers a `pip install` in this phase's task list — both
  were installed by prior phases (an earlier ENV phase for tensorboard, Phase
  41/CTX-50 for PyYAML) and are already verified importable in `pinn-train`.

**Packages removed due to `[SLOP]` verdict:** none.
**Packages flagged as suspicious `[SUS]`:** `tensorboard`, `pyyaml` — both
false positives per the note above; **no `checkpoint:human-verify` task is
needed** since no new install action exists for either. A lightweight sanity
line in the runbook's Setup section ("verify `python -c 'import tensorboard;
print(tensorboard.__version__)'` prints `2.21.0`") is sufficient and is
already implied by OPS-06's Setup entry point.

## Architecture Patterns

### System Architecture Diagram

```
 process start (python -m pinn.train --config … [--resume …])
   │
   ▼
 ┌─────────────────────────────────────────────────────────────┐
 │ pinn/train.py main()  — composition root                     │
 │                                                                │
 │  1. install SIGINT/SIGTERM handlers (main thread only)        │
 │  2. resolve run_dir; create logs/, tb/, empty failure/         │
 │  3. write status.json state="initializing" (pre model-build)  │
 │  4. write summary.md/json launch-time stub (E4 presence)      │
 │  5. attach sinks to logging.getLogger("pinn.training"):        │
 │        JsonlHandler ──────► runs/<name>/logs/train.log.jsonl  │
 │        HumanFormatter ────► runs/<name>/logs/train.log        │
 │        TbSink (SummaryWriter) ─► runs/<name>/tb/  (async)      │
 │  6. start heartbeat daemon thread (rewrites status.json)       │
 │  7. curriculum.run() ──────────────────────────────────────┐  │
 └──────────────────────────────────────────────────────────┼──┘
                                                              ▼
                          ┌─────────────────────────────────────────┐
                          │ CurriculumController.step()               │
                          │  → RunController.run_stage(k)             │
                          │      Adam epoch loop ┐                    │
                          │      L-BFGS epoch loop┴─► _log_step(...)   │
                          │        (widened: stage, λ, grad_norm,     │
                          │         w_n stats, per-bin residuals,     │
                          │         s/step, ETA — emitted EVEN on a   │
                          │         guard trip, see Pitfall 2)        │
                          └─────────────────────────────────────────┘
                                     │ every logged step, unconditionally
                                     ▼
                    logging.getLogger("pinn.training.controllers").info(
                        msg, extra={...widened fields...})
                                     │  (stdlib logging fan-out)
              ┌──────────────────────┼───────────────────────┐
              ▼                      ▼                        ▼
    JsonlHandler.emit()    HumanFormatter writes      TbSink.emit()
    json.dumps(              a formatted line to        SummaryWriter.add_scalar(...)
      sanitized_record,      train.log                  per widened field + per-bin
      allow_nan=False)                                   residual + causal/* tags
    append to .jsonl                                     (own background thread —
                                                           never blocks this call
                                                           except on full queue,
                                                           see Pitfall 7)
              │
              ▼ (independent of the above — driven by a daemon thread, not by _log_step)
    status.json heartbeat: rewritten every heartbeat_secs (default candidate
    30s) AND at every state transition, via atomic_io.atomic_write_text
    (temp + fsync + os.replace + dir fsync — never a torn read)
              │
              ▼ (terminal transition: normal finish / guard HALT / signal)
    summary.md / summary.json finalized atomically (same atomic_io primitive)
    status.json flipped to finished|failed|interrupted (never fabricated)
```

A reader can trace the primary use case end to end: a step happens in
`RunController` → `_log_step` fires unconditionally → the stdlib logger fans
out to three independent sinks (JSONL canonical, human mirror, TensorBoard
async) → a fully separate daemon thread proves liveness via `status.json`
regardless of what the step loop is doing → on any exit path the same
atomic-write primitive finalizes `summary.*`/`status.json` honestly.

### Recommended Project Structure

```
pinn/training/
├── step_log.py        # STEP_LOG_FIELDS registry, record sanitizer (allow_nan=False-safe),
│                       # JsonlHandler + HumanFormatter (logging.Handler subclasses)
├── tb_sink.py          # TbSink: owns the SummaryWriter, fan-out from the widened record,
│                       # panel tags (residuals/bin_nn, causal/*), warn-once-on-failure
├── signals.py          # install_signal_handlers(...): stop-flag, debounce, escalation
├── heartbeat.py         # HeartbeatThread: daemon thread, status.json schema builder
└── run_summary.py       # stub_summary(...) / finalize_summary(...): summary.md/json,
                          # renders curriculum.jsonl into the progression section
configs/
└── stage0-example.yaml  # OPS-06 example config; log_every: 100, run.monitor defaults
docs/runbooks/training/
└── <YYYY-MM-DD>-stage0-training-operator-runbook.md
scripts/
└── train-unattended.sh  # exec caffeinate -is python -m pinn.train "$@"
```

Rationale: mirrors the established one-module-per-concern pattern already in
`pinn/training/` (`checkpoint.py`, `guards.py`, `resume.py`, `determinism.py`
are each a single well-scoped module, not one large file) and CTX-33's
precedent of a multi-module driver layer for a cohesive concern. This is a
**recommendation**, not a re-decision — module naming is explicitly Claude's
Discretion per `42-CONTEXT.md`.

### Pattern 1: Composition-root sink attachment via stdlib `logging.Handler`
**What:** Instead of a bespoke callback list, attach real `logging.Handler`
subclasses to the existing `pinn.training` logger. `RunController._log_step`
does not change *how* it logs (`_LOGGER.info(msg, extra={...})`), only *what*
it passes in `extra`.
**When to use:** Exactly the CTX-45/65 designed seam — this is not optional
Claude's Discretion, it is the locked mechanism; the pattern below documents
*how* to implement it correctly against stdlib `logging`.
**Example:**
```python
# pinn/training/step_log.py — sketch, not literal production code
import json
import logging

class JsonlHandler(logging.Handler):
    def __init__(self, path):
        super().__init__()
        self._fh = open(path, "a", encoding="utf-8")  # append-mode text stream

    def emit(self, record: logging.LogRecord) -> None:
        if record.__dict__.get("event") != "step":
            return  # non-step events (run start, handoff, stage-exit) skip JSONL
        payload = _sanitize_for_json(record.__dict__)  # NaN/Inf -> None + flags
        self._fh.write(json.dumps(payload, allow_nan=False, sort_keys=True) + "\n")
        self._fh.flush()  # per logged step; no fsync (non-degradation, CTX-66)
```
Composition root:
```python
# pinn/train.py main() — attachment only happens here
logger = logging.getLogger("pinn.training")
logger.addHandler(JsonlHandler(run_dir / "logs" / "train.log.jsonl"))
logger.addHandler(HumanFileHandler(run_dir / "logs" / "train.log"))
logger.addHandler(TbSink(run_dir / "tb"))  # SummaryWriter-backed
```

### Pattern 2: `allow_nan=False` as a hard backstop over explicit sanitization
**What:** Sanitize non-finite values to `None` + a `finite`/`nonfinite_keys`
flag pair *before* calling `json.dumps`, and *also* pass `allow_nan=False` so
a sanitization bug fails loudly (`ValueError`) instead of silently emitting
invalid-JSON `NaN`/`Infinity` tokens.
**When to use:** Every JSONL write (E1 backstop).
**Example (verified in this session):**
```python
>>> import json
>>> json.dumps({"x": float("nan")})              # DEFAULT allow_nan=True
'{"x": NaN}'                                       # NOT valid JSON (json.loads elsewhere would reject it)
>>> json.dumps({"x": float("nan")}, allow_nan=False)
ValueError: Out of range float values are not JSON compliant: nan
>>> json.dumps({"x": None, "finite": False, "nonfinite_keys": ["x"]}, allow_nan=False)
'{"finite": false, "nonfinite_keys": ["x"], "x": null}'   # parses under any strict parser
```
This directly validates CTX-67's design and is why `allow_nan=False` is not
optional — the stdlib default (`allow_nan=True`) is the one setting that would
silently violate the SPEC's E1 acceptance criterion.

### Pattern 3: Daemon-thread heartbeat with a self-describing staleness schema
**What:** `status.json` carries its own `heartbeat_interval_secs` and
`staleness_threshold_secs` so any reader (operator, a future dashboard, a
test) can classify staleness with zero external configuration.
**When to use:** OPS-04a / E3.
**Example (schema sketch, values are the CTX-75-described fields):**
```json
{
  "schema_version": 1,
  "run_name": "first-run",
  "pid": 40231,
  "state": "running",
  "timestamp_utc": "2026-07-18T22:14:03.512Z",
  "timestamp_epoch": 1784499243.512,
  "heartbeat_interval_secs": 30,
  "staleness_threshold_secs": 90,
  "step": 4200, "stage": 0, "phase": "2a", "epoch": 42,
  "losses": {"data": 0.0021, "ic": 0.0004, "phys": null, "energy": 0.0011, "angmom": 0.0002, "total": 0.0038},
  "finite": true,
  "lr": 0.00035, "s_per_step_ema": 1.21, "eta_seconds": 5382.0,
  "mem_driver_allocated_bytes": 3221225472, "mem_current_allocated_bytes": 2952790016
}
```
A reader computes `now - timestamp_epoch > staleness_threshold_secs` with no
other file or constant.

### Anti-Patterns to Avoid
- **A second atomic-write implementation:** `atomic_io.atomic_write_text`
  already does temp + fsync(file) + `os.replace` + fsync(dir). `status.json`
  and `summary.*` must call it, not reimplement it.
- **Reusing `guards._json_safe_scalar` for the JSONL formatter:** its
  non-finite policy is a string sentinel (`"NaN"`/`"Inf"`/`"-Inf"`) — correct
  and intentional for `failure/trip.json` (a one-shot diagnostic file, not a
  streamed machine log), but exactly the pattern the SPEC's E1 test rejects
  for the canonical step log (Pitfall 3 in `42-CONTEXT.md`; re-verified by
  reading the function body directly — see Pitfall 6 below for the exact
  contrast).
- **`matplotlib` or any synchronous plotting inside the step loop:** violates
  the SPEC's async constraint outright; not needed anyway — `SummaryWriter`'s
  own background thread is the async mechanism (verified, see Pitfall 7).
- **Verifying "TB emits under NaN" with `EventFileLoader`:** produces a false
  negative (Pitfall 3) — use `EventAccumulator`.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Atomic file rewrite | A second temp+rename helper inside `heartbeat.py`/`run_summary.py` | `pinn.training.atomic_io.atomic_write_text` | Already implements the exact fsync(file) → `os.replace` → fsync(dir) ordering E3 requires; a second implementation risks a subtly different (non-atomic) ordering |
| Async event writing | A custom queue + worker thread wrapping TB writes | `torch.utils.tensorboard.SummaryWriter` — its `add_scalar` enqueues onto the underlying `tensorboard.summary.writer.event_file_writer._AsyncWriter`'s `queue.Queue`, consumed by a dedicated background thread (verified from source, see Code Example below) | Reimplementing this duplicates a mechanism the dependency already provides correctly, and risks a subtly different failure mode on writer-thread death |
| Non-finite JSON handling | A regex-based JSON post-processor, or a custom encoder subclass that overrides `float.__repr__` | Pre-sanitize to `None`+flags, then `json.dumps(..., allow_nan=False)` | `allow_nan=False` is a one-keyword stdlib feature that turns a missed sanitization case into a loud exception instead of a silent invalid-JSON line |
| GPU memory signal | `psutil`, `resource.getrusage()` (macOS reports KB not bytes — a known gotcha) | `torch.mps.driver_allocated_memory()` (already the CTX-76/Phase-41 wiring) | Explicitly banned as a new dependency by CTX-76; the existing signal is already correct for macOS and already wired into `StepGuards` |
| Signal debouncing | A generic "event debouncer" utility class | A single timestamp comparison (`time.monotonic() - last_sigint_time < debounce_window`) inside the SIGINT handler | The debounce requirement here is narrow (coalesce a panic-mash, escalate a deliberate second press) — a generic utility adds indirection for a two-line check |

**Key insight:** every "don't hand-roll" item in this phase is a case of an
existing, already-verified-correct primitive one level down in the same
codebase or the same already-installed dependency. The phase's actual new
code surface is *composition* (wiring sinks to the logger tree, wiring the
heartbeat thread to `status.json`, wiring signal handlers to the stop flag),
not new low-level mechanism.

## Common Pitfalls

### Pitfall 1: `json.dumps` default silently emits invalid JSON for NaN/Inf
**What goes wrong:** A widened record with a raw `float("nan")` anywhere,
serialized with the stdlib default (`allow_nan=True`), produces
`{"phys": NaN}` — valid Python/JS, **not valid JSON** per RFC 8259. Any
downstream tool doing strict `json.loads` (including the E1 test itself)
raises on that line.
**Why it happens:** `allow_nan=True` is the Python stdlib default; it is easy
to call `json.dumps(record)` without noticing the non-default flag is needed.
**How to avoid:** Sanitize every field to `None` + `finite`/`nonfinite_keys`
*before* serialization, and always pass `allow_nan=False` (Code Pattern 2,
verified in this session with the exact error text).
**Warning signs:** A JSONL line that visually looks fine in a text editor but
fails `json.loads` — this is the E1 test's exact target.

### Pitfall 2: The current guard-trip control flow bypasses `_log_step` entirely
**What goes wrong:** Reading `pinn/training/controllers.py` as it exists
today: in `_run_adam_phase`, every guard-trip / non-finite-loss branch
(`return handoff_trigger, adam_epochs_used` at the lines following the guard
check, and the non-finite/clip-outcome checks) returns *before* reaching the
`self._log_step(...)` call later in the loop body. In the L-BFGS section of
`run_stage`, the same shape recurs: `return guard_outcome.disposition` and
`return StageDisposition.RECOVER` both precede the `self._log_step(...)` call
near the bottom of that loop iteration. **Today, a diverged step is never
logged at all** — the opposite of CTX-65's explicit requirement ("a step that
trips a guard still logs").
**Why it happens:** Phase 40/41 built the *minimal* log (CTX-52: "step, five
loss terms, total, lr") purely to observe healthy resume/guard-trip behavior
at the control-flow level (did the disposition come back correctly?) — logging
the diverged step's *values* was explicitly out of Phase 40/41's scope and
handed to Phase 42.
**How to avoid:** When widening `_log_step`, also move its call site (or add
a second call) so it fires immediately once `loss_terms`/`grad_norm` are known
— before the `return` — in both the Adam guard-check block and the L-BFGS
guard-check block. `loss_terms` (a `LossTerms` carrier with `.data/.ic/.phys/
.energy/.angmom/.total`) is already in scope at every one of these return
points; `grad_norm` is `None` specifically when the loss itself was non-finite
(backward() is correctly skipped in that case) — that is expected, not a bug,
and should serialize as `null` per the E1 policy, not be treated as a missing
field.
**Warning signs:** A synthetic-divergence test that asserts a JSONL line
exists for the guard-tripped step will fail with "no line written" rather than
"line written but malformed" — a different failure mode than what the SPEC's
E1 prose implies, worth distinguishing in the task's verification step.

### Pitfall 3: TensorBoard's low-level event reader silently zeroes NaN (verified)
**What goes wrong:** Reading back a written NaN scalar via
`tensorboard.backend.event_processing.event_file_loader.EventFileLoader.Load()`
returns `simple_value: 0.0`, not NaN, even though the on-disk bytes are
correct. A held-out test written naively against `EventFileLoader` will
report "the panel did not emit under NaN" when it actually did.
**Why it happens:** Verified empirically in this session (tensorboard 2.21.0,
torch 2.12.1, `pinn-train`): a raw TFRecord parse of the same file shows
`simple_value: nan` (correct, on-disk); `EventFileLoader.Load()` on the exact
same file returns `0.0` for that value; `EventAccumulator.Reload()` +
`.Scalars(tag)` on the exact same file returns `nan` (correct). The
discrepancy is confined to the low-level `EventFileLoader` iterator — root
cause not further isolated (not needed for the mitigation), but the effect is
reproducible and file-format-independent (the bytes are fine).
**How to avoid:** Any Phase 42 test asserting "the panel emits under NaN"
(OPS-04b AC) must read back via
`tensorboard.backend.event_processing.event_accumulator.EventAccumulator`
(`.Reload()` then `.Scalars(tag)`), not `EventFileLoader`, and not a
hand-rolled raw parse (works, but needlessly low-level for a test).
**Warning signs:** A flaky-looking test that reports "NaN became 0.0" only for
tags checked via the low-level reader.

### Pitfall 4: `signal.signal()` only works in the main thread (verified)
**What goes wrong:** If handler installation is attempted from inside a
background thread (e.g., accidentally inside the heartbeat daemon thread
instead of `main()`), Python raises immediately.
**Why it happens:** CPython restricts `signal.signal()` to "the main thread of
the main interpreter." Verified directly in this session:
```python
>>> # called from a non-main thread
ValueError: signal only works in main thread of the main interpreter
```
This also means: no matter which OS thread physically receives the signal,
the registered Python handler always executes on the main thread — a daemon
heartbeat thread can run concurrently with signal delivery/handling without
any special coordination beyond the stop-flag CTX-71 already specifies.
**How to avoid:** Install handlers only in `pinn/train.py main()` (already
CTX-71's design) — this pitfall confirms the design is not just a style
preference but a hard Python restriction. Nothing to fix; documented so the
planner does not "helpfully" move handler installation into a shared helper
that might be imported/called from a non-main-thread context in a future
phase.
**Warning signs:** `ValueError: signal only works in main thread...` at
startup if this is ever violated.

### Pitfall 5: `os._exit()` vs `sys.exit()` — the second-SIGINT escalation must use `os._exit`
**What goes wrong:** Using `sys.exit()` (raises `SystemExit`) for the
second-SIGINT escalation path would run `finally` blocks, `atexit` handlers,
and any wrapping exception handling — potentially triggering *another*
checkpoint write, which is exactly what "no further checkpoint" (SPEC OPS-02
AC) forbids.
**Why it happens:** `sys.exit()` is a *cooperative* exit (raises an exception
that unwinds normally); `os._exit()` terminates the process immediately with
no cleanup, no `atexit`, no buffer flush `[MEDIUM: tavily search, cross-
checked against well-established stdlib semantics]`.
**How to avoid:** CTX-71 already specifies `os._exit(130)` for the escalation
path — this pitfall is confirmation, not a new decision. The one operational
consequence worth surfacing: because `os._exit()` skips buffer flushing, any
JSONL/human-log handler using buffered file writes should flush proactively
*before* the escalation path calls `os._exit` (the CTX-71 "best-effort atomic
`status.json` flip to `interrupted`" already implies this ordering — flip
status, *then* exit).
**Warning signs:** A `.jsonl` file missing its last few lines after a
double-Ctrl-C exit, if a handler is buffering without an explicit flush before
`os._exit`.

### Pitfall 6: `guards._json_safe_scalar`'s sentinel policy is deliberately
### different from the JSONL policy — read both before reusing either
**What goes wrong:** `guards._json_safe_scalar` (used by
`_outcome_to_trip_dict` for `failure/trip.json`) converts non-finite floats to
the *strings* `"NaN"` / `"Inf"` / `"-Inf"`. If this exact function is imported
and reused for the canonical JSONL formatter, every line **would** parse under
`json.loads` (strings are valid JSON) — but it would violate CTX-67's design
(`null` + `finite:false` + `nonfinite_keys`, chosen specifically because
"string sentinels... break typed parsers" expecting a numeric or null field).
**Why it happens:** Both functions solve "make a non-finite float
JSON-safe," so it is natural to look for one shared helper — but they were
designed for genuinely different consumers (a one-shot diagnostic file where a
human-readable string is fine, vs. a streamed machine log where a
typed-schema reader expects `total: null`, not `total: "NaN"`).
**How to avoid:** Write a *separate*, small sanitizer for
`pinn/training/step_log.py` that implements the `null`+flags policy — do not
`from pinn.training.guards import _json_safe_scalar`.
**Warning signs:** A JSONL consumer written against a numeric-or-null schema
throwing a type error on a string `"NaN"`.

### Pitfall 7: TensorBoard's "asynchronous" writer can still block on a full queue
**What goes wrong:** `SummaryWriter`'s default `max_queue=10` — if the
background writer thread falls behind (e.g., a slow/contended disk), the
*next* `add_scalar` call blocks in `queue.Queue.put()` until space frees up.
"Asynchronous" does not mean "never blocks"; it means "usually returns
immediately."
**Why it happens:** Verified by reading `_AsyncWriter.write` source directly:
`self._byte_queue.put(bytestring)` — Python's `queue.Queue.put()` blocks by
default when the queue is full.
**How to avoid:** At `log_freq=100` (the CTX-66/design-doc default cadence),
each `add_scalar` batch (per-bin residuals + causal stats, ~20 scalars) is
infrequent relative to the queue's default 10-item depth and `flush_secs=120`
auto-flush — queue exhaustion under normal operation is unlikely. This is a
documented risk, not a required mitigation: `[ASSUMED]` that normal operation
never fills the queue (not independently load-tested under real GPU
contention this session — see Assumptions Log A1). If it becomes a real
concern, `SummaryWriter(max_queue=...)` accepts a larger value, and CTX-69's
"one warning then continue" wrapper (catch, log, skip) is the correct
backstop either way — it should wrap the `add_scalar` calls, not just
construction.
**Warning signs:** A step-loop stall correlated with disk I/O pressure and TB
writes in flight.

### Pitfall 8: The collocation-time-to-bin-index mapping is stable only during L-BFGS, not during Adam
**What goes wrong:** `_build_anchor_context` draws fresh i.i.d. collocation
times every call when `fixed_collocation_times is None` — and the Adam-phase
loop (`_run_adam_phase`) passes `None` every epoch (`anchor_ctx =
self._build_anchor_context(self._train_source, batch, None)`), meaning a
*new* random draw of `N_t=16` times happens every Adam epoch. The L-BFGS
phase, by contrast, draws collocation times *once* before its epoch loop
(`fixed_collocation_times = self._collocation_sampler.uniform()`,
called before the loop) and reuses that fixed set for the whole phase
(matches the "fixed-batch L-BFGS" design). In both cases the times are sorted
ascending (`order = np.argsort(colloc_times)`) before use, so
`residuals/bin_00..15` is always a valid ascending-time ordering *within one
step* — but during Adam, "bin 5" at step 100 and "bin 5" at step 200 are
generally *different τ values* (only their sorted rank position is
comparable), while during L-BFGS, "bin 5" means the *same* τ value for every
step of that phase.
**Why it happens:** This is the correct, intentional behavior for the
optimization (Adam wants resampled collocation points every epoch for
generalization; L-BFGS wants a fixed batch for closure consistency) — it is
not a bug. It is a semantic detail the panel design (CTX-70) does not call
out.
**How to avoid:** Not a required fix — CTX-70's panel is still meaningful
(rank-position trends and `w_n` collapse are visible either way), but the
operator runbook (OPS-06, "categorized error surface" / "mental model"
section) should mention this once: during Adam-phase steps, `bin_n` tracks
*relative* early/late position, not a fixed time; during L-BFGS-phase steps,
`bin_n` is a fixed τ. A cheap, in-scope enhancement (Claude's Discretion per
CTX-70's "TB tag taxonomy beyond the mandated tags") is a companion
`colloc/t_min` / `colloc/t_max` scalar pair per step, so a reader can sanity
check the current bin range without cross-referencing code.
**Warning signs:** An operator misreading a "bin 0 residual spike" during Adam
training as diagnostic of a *specific* early time, when it is actually just
"whichever of the 16 random draws that epoch happened to sort first."

## Code Examples

### Threading `stage` into the widened `_log_step` (the concrete Pitfall-2/CTX-65 fix shape)
```python
# Source: read directly from pinn/training/controllers.py (RunController), this session.
# RunController has NO self._stage attribute anywhere — verified by grep across the
# whole class body. `k` (the stage index) is only ever a local parameter of
# run_stage(self, k, ...) and _run_adam_phase(self, k, ...). The widened _log_step
# needs a new explicit `stage` parameter threaded from both call sites:

def _log_step(self, *, step, loss_terms, lr, phase, stage, ...widened fields...):
    ...

# Adam call site (inside _run_adam_phase, which already receives k):
self._log_step(step=self._global_step, loss_terms=loss_terms, lr=lr_now,
                phase="2a", stage=k, ...)

# L-BFGS call site (inside run_stage, which already receives k):
self._log_step(step=self._global_step, loss_terms=..., lr=None,
                phase="2b", stage=k, ...)
```

### The additive `return_details` shape for `causal_physics_loss`
```python
# Source: read directly from pinn/loss_catalog.py causal_physics_loss, this session.
# rbar (R̄_n, shape (N_t,)) is ALREADY computed by the CALLER
# (controllers.py:_non_data_terms, `rbar = (residual ** 2).mean(dim=(-2, -1))`)
# and handed IN as `residuals_per_time` — the caller does not need it back.
# The only value causal_physics_loss computes internally and does NOT currently
# expose is `weights` (w_n, line ~258: `weights = torch.exp(-eta * cumsum_excl)`).
# CTX-70's additive path therefore needs to expose `weights`, and can cheaply
# also echo back `rbar` for callers that don't already hold it:

def causal_physics_loss(residuals_per_time, *, eta_c=CAUSAL_ETA_C, times=None,
                         dtype, device, return_details: bool = False):
    ...  # UNCHANGED existing body through `weights = torch.exp(-eta * cumsum_excl)`
    loss = (weights * rbar).mean()
    if return_details:
        return loss, {"rbar": rbar.detach(), "w_n": weights.detach()}
    return loss  # default return type UNCHANGED — Phase 38/40 tests untouched
```
Call site in `controllers.py:_non_data_terms` only needs
`phys_term, details = causal_physics_loss(rbar, times=..., return_details=True)`
when a widened-logging consumer is attached — cheap either way since both
tensors are already computed as part of the existing forward pass; `.detach()`
prevents the autograd-graph retention CTX-70 calls out.

### `EventAccumulator`-based readback (the correct NaN-survives-a-round-trip test)
```python
# Source: verified directly in pinn-train, tensorboard 2.21.0, this session.
from tensorboard.backend.event_processing.event_accumulator import EventAccumulator

acc = EventAccumulator(str(tb_dir))
acc.Reload()
values = acc.Scalars("residuals/bin_00")
assert math.isnan(values[-1].value)   # correctly survives the round trip

# CONTRAST — do not use this reader for the same assertion:
# from tensorboard.backend.event_processing.event_file_loader import EventFileLoader
# EventFileLoader(path).Load() silently returns 0.0 for the same on-disk NaN.
```

### `caffeinate -is` wrapper (man-page-verified flag semantics)
```bash
#!/usr/bin/env bash
# scripts/train-unattended.sh — Source: `man caffeinate` (local, this machine), this session.
# `-i`: prevent idle sleep. `-s`: prevent sleep, valid only on AC power.
# "If a utility is specified, caffeinate creates the assertions on the
#  utility's behalf, and those assertions will persist for the duration of
#  the utility's execution" — i.e. exactly as long as `python -m pinn.train`
#  runs, no separate `-w <pid>` bookkeeping needed.
# `exec` replaces the shell process with caffeinate, so caffeinate's own exit
# status (which is the wrapped utility's exit status) becomes this script's
# exit status verbatim — satisfies the must-NOT "wrapper exit == inner exit" test.
exec caffeinate -is python -m pinn.train "$@"
```
Note: `-d` (prevent display sleep) is deliberately **not** included — an
unattended run has no one watching the screen; holding a display-sleep
assertion for a multi-hour run would needlessly keep the display awake/warm
for no operator benefit. This matches CTX-73/B-10 exactly; the man page
confirms `-d` is a distinct, independent assertion from `-i`/`-s`.

### `torch.mps` memory signals (official docs, verified live)
```python
# Source: docs.pytorch.org/docs/2.12 (context7) + live execution in pinn-train, this session.
torch.mps.driver_allocated_memory()   # total GPU memory allocated by the Metal driver
                                       # for the PROCESS, in bytes — includes cached
                                       # MPSAllocator-pool allocations (the Phase-41 guard signal)
torch.mps.current_allocated_memory()  # memory currently occupied by LIVE TENSORS only,
                                       # in bytes — tighter, excludes cache; a good
                                       # secondary status.json field distinct from the
                                       # guard's cache-inclusive signal
torch.mps.device_count()              # == 1 on this machine, verified live — confirms
                                       # the SPEC's single-MPS-device constraint empirically
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|---------------|--------|
| `torch.utils.tensorboard.SummaryWriter(new_style=False)` (default, `simple_value` scalar field) | `new_style=True` writes a `TensorProto` instead | Available since early SummaryWriter versions; PyTorch's own docs describe `new_style` as "could lead to faster data loading" | Not adopted here — `new_style` defaults to `False` and CTX-70 does not call for it; noted only because it is one plausible route to sidestep the `EventFileLoader` NaN quirk (untested this session) if it ever becomes a real problem. **Do not switch proactively** — `EventAccumulator`-based test readback already resolves the actual risk. |

**Deprecated/outdated:** none identified specific to this phase's stack —
`SummaryWriter`, `torch.mps.*`, and stdlib `signal`/`json`/`logging` are all
current, non-deprecated APIs in the installed versions.

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | At `log_freq=100` and the CTX-70 panel's tag count (~20 scalars/step), TensorBoard's default `max_queue=10` write buffer will not fill under normal M5 Pro operation, so `add_scalar` calls will not visibly block the step loop | Pitfall 7 | LOW — even if wrong, CTX-69's mandated "one warning then continue" wrapper around TB calls is the correct backstop either way; worst case is a documented, easily-diagnosed slowdown, not incorrect behavior or data loss (JSONL remains canonical and is unaffected) |

**All other claims in this research were verified this session** — either by
direct execution against the exact `pinn-train` environment and this exact
machine (tensorboard NaN round-trip, `torch.mps.device_count()==1`,
`signal.signal()` main-thread restriction, `json.dumps(allow_nan=False)`
behavior), by reading the actual source of the functions being modified
(`_log_step`, `causal_physics_loss`, `_build_anchor_context`,
`atomic_io.atomic_write_text`, `guards._json_safe_scalar`), by the local
authoritative `man caffeinate` page, or by official PyTorch 2.12 documentation
via context7.

## Open Questions

1. **Should the guard-tripped step's widened JSONL record use the
   pre-increment or would-be-post-increment `global_step` value?**
   - What we know: in the Adam phase, `self._global_step` is incremented
     *after* the guard checks (so a tripped step's record would use the
     step number that is *about to be attempted*, not yet completed); in the
     L-BFGS phase, `self._global_step` is incremented *before* the guard
     check (so a tripped step's record there would use the step number *as
     if it had completed*). These two phases are inconsistent with each other
     today.
   - What's unclear: whether the plan should normalize this (e.g., always log
     using "the step that was attempted," incrementing consistently) or treat
     it as acceptable given RECOVER immediately rolls back `global_step` from
     the restored checkpoint anyway, making the exact number on the diverged
     line transient/informational.
   - Recommendation: this is a small, self-contained implementation decision
     inside Phase 42's own scope (not a framework-spec question, not a
     STOP-protocol gap) — the planner should pick one convention explicitly
     (recommend: log the step number that identifies *this attempt*,
     consistently, and add a boolean `step_completed` field alongside
     `finite` so a JSONL consumer can distinguish "this step's optimizer
     update ran" from "this step was a diverged attempt") rather than leaving
     the inconsistency between Adam and L-BFGS unresolved.

2. **Exact value for `heartbeat_secs` / `staleness_factor` defaults.**
   - What we know: CTX-74 proposes a default of 30s with a 3× staleness
     factor (90s); this is explicitly Claude's Discretion within a 15–60s
     range per `42-CONTEXT.md`.
   - What's unclear: nothing blocking — this is a pre-cleared discretion
     range, not a research gap. Noted here only to confirm no external source
     contradicts the 15–60s range as reasonable (it does not — this is purely
     an operator-ergonomics choice with no correctness constraint either way).
   - Recommendation: 30s/90s is a reasonable middle of the discretion range;
     no further research needed.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| `tensorboard` | OPS-03/04b (TB sink, residual panel) | ✓ `[VERIFIED: live import]` | 2.21.0 | — |
| PyTorch (`torch`, `torch.mps`) | OPS-04a (memory signal), all training | ✓ `[VERIFIED: live import]` | 2.12.1 | — |
| PyYAML | OPS-06 (example config loads via `load_config`) | ✓ (Phase 41 established) | 6.0.3 latest on PyPI | — |
| `caffeinate` (macOS system utility) | OPS-02 (unattended wrapper) | ✓ `[VERIFIED: man caffeinate]` | `/usr/bin/caffeinate`, Darwin | — (no fallback needed; this project is single-machine macOS by design) |
| `pinn-train` conda env | All of the above | ✓ `[VERIFIED: conda run -n pinn-train python --version]` | Python 3.11.15 | — |
| MPS device | OPS-04a memory signal, `torch.mps.device_count()` | ✓ `[VERIFIED: device_count() == 1]` | — | — |

**Missing dependencies with no fallback:** none.
**Missing dependencies with fallback:** none — every dependency this phase
needs is already present and verified on the target machine.

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | stdlib `unittest`, matching the established `tests/phase40`/`tests/phase41` pattern exactly |
| Config file | none — no pytest/config file in this repo's test tree; `python -m unittest discover` |
| Quick run command | `<home>/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase42.test_step_log tests.phase42.test_prohibitions -v` (adjust module names per Wave 0 gaps below) |
| Full suite command | `<home>/miniforge3/envs/pinn-train/bin/python -m unittest discover -s tests/phase42 -p 'test_*.py' -v` |

Established precedent (verified by reading `tests/phase41/__init__.py` and
`tests/phase41/_fixtures.py` this session): every deferred test uses a
module-local `_require(symbol, module)` helper raising `unittest.SkipTest`
(never `ImportError`) while a later-wave production symbol is absent, with a
single shared `_SKIP_PHRASE` constant so a final grep can detect any
remaining skip. `tests/phase41/_fixtures.py` already provides
`make_synthetic_stage0_loop(...)` — a dataset-free, tiny synthetic Stage-0
`RunController`/`CurriculumController` pair. **Phase 42's tests should import
and extend this fixture, not rebuild a synthetic loop from scratch** — it
already wires stubs for exactly the "tiny synthetic Stage-0 runs, population
floor 240" pattern the CONTEXT specifies.

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| OPS-01 | Runbook documents 5 entry points, each one operator action; no new CLI beyond wrapper | doc-structure | `pytest`-free: `python -m unittest tests.phase42.test_runbook -v` (parses markdown headings) | ❌ Wave 0 |
| OPS-02 | `caffeinate -is` wrapper launches training with sleep prevented | manual + smoke | runbook-documented manual check (`ps` shows `caffeinate` holding the assertion); no automated macOS-sleep-state test in-repo | ❌ Wave 0 (smoke only) |
| OPS-02 / must-NOT #3 | Wrapper does not swallow non-zero exit | integration | `python -m unittest tests.phase42.test_wrapper -v` (subprocess, asserts `returncode` matches a deliberately-failing `pinn.train` invocation) | ❌ Wave 0 |
| E2 (signal race, R2) | SIGINT-once → checkpoint + exit 130; SIGINT-twice (within debounce) → immediate exit, no 2nd checkpoint; SIGTERM → graceful (exit 143) | integration (subprocess + signals) | `python -m unittest tests.phase42.test_signals -v` | ❌ Wave 0 |
| OPS-03 (widened JSONL) | ≥1 parseable JSON object with keys for all widened fields after `log_freq` steps | unit (synthetic loop) | `python -m unittest tests.phase42.test_step_log -v` | ❌ Wave 0 |
| E1 (non-finite JSONL, R3) | A NaN/Inf step still writes a parseable line with `finite:false` + `nonfinite_keys` | unit (forced-divergence synthetic loop) | `python -m unittest tests.phase42.test_step_log.NonFiniteTests -v` | ❌ Wave 0 |
| OPS-04a (status.json) | Reader classifies running-vs-stalled from timestamp age alone; `state` transitions correctly | unit + integration | `python -m unittest tests.phase42.test_heartbeat -v` | ❌ Wave 0 |
| E3 (status.json startup + atomicity, R4) | `initializing` pre-step-0 with null losses; every rewrite atomic (never truncated) | unit (concurrent-read stress) | `python -m unittest tests.phase42.test_heartbeat.AtomicityTests -v` | ❌ Wave 0 |
| OPS-04b (residual panel) | TB contains per-bin residual viz + `w_n`-vs-step scalars after ≥1 curriculum step | unit (`EventAccumulator` readback) | `python -m unittest tests.phase42.test_tensorboard_panel -v` | ❌ Wave 0 |
| OPS-04b must-emit-under-collapse | Panel still emits when `w_n` stats collapse toward zero / under NaN | unit (`EventAccumulator`, NOT `EventFileLoader` — Pitfall 3) | `python -m unittest tests.phase42.test_tensorboard_panel.CollapseTests -v` | ❌ Wave 0 |
| OPS-05 (`runs/` contract) | Successful run yields every listed file/dir; `summary.md` has header/losses/progression | unit (synthetic loop, full run) | `python -m unittest tests.phase42.test_run_contract -v` | ❌ Wave 0 |
| E4 (partial run, R6) | Killed run still yields honest contract; `state ∈ {failed, interrupted}`; `summary.md` present as failed template | integration (subprocess + SIGKILL at multiple kill-points) | `python -m unittest tests.phase42.test_run_contract.PartialRunTests -v` | ❌ Wave 0 |
| must-NOT #1 (false-green) | `status.json`/`summary.md` never read `finished`/healthy on divergence or incomplete termination; no fabricated metrics | unit (forced-divergence + forced-HALT synthetic loop) | `python -m unittest tests.phase42.test_prohibitions.FalseGreenTests -v` | ❌ Wave 0 |
| must-NOT #2 (redaction) | No `/Users/`, hostname, or secret-shaped strings in any handoff artifact | unit (grep-based negative test over a synthetic run's output tree) | `python -m unittest tests.phase42.test_prohibitions.RedactionTests -v` | ❌ Wave 0 |
| OPS-06 (example config) | `configs/stage0-example.yaml` validates via `load_config` without error | unit | `python -m unittest tests.phase42.test_config_yaml -v` | ❌ Wave 0 (extends `tests/phase41/test_config_yaml.py` pattern) |

### Nyquist Sampling Logic

The question this phase's monitoring layer exists to answer is "how often
must an observer look to reliably catch a given failure mode?" — each edge
backstop has a different answer:

- **E1 (non-finite JSONL):** not a rate question — a *coverage* one. A single
  malformed line anywhere in `train.log.jsonl` breaks the canonical-log
  contract, so the test must `json.loads()` **every line** of a multi-step
  synthetic run, not sample a subset or check only the last line.
- **E2 (signal debounce):** a genuine two-point Nyquist bracket. If the
  debounce window is `W` seconds (~1s, Claude's Discretion), the test suite
  needs (a) one case sending the second SIGINT well *inside* `W` (e.g.
  `W/5`–`W/3`) to prove coalescing, and (b) one case sending it well *outside*
  `W` (e.g. `1.5×W`–`2×W`) to prove escalation. A single sample at exactly `W`
  proves nothing (boundary ambiguity) — the test needs both sides of the
  threshold, clearly inside each region, not a single point.
- **E3 (heartbeat staleness):** the file declares `heartbeat_interval_secs =
  K` and `staleness_threshold_secs ≈ 3K`. For the *test* verifying atomicity
  specifically (not staleness classification), the read frequency must exceed
  the write frequency by a wide margin to have any chance of observing a torn
  read if atomicity were broken — poll at a small fraction of a second while
  the heartbeat thread rewrites on its normal K-second cadence (or, more
  efficiently, drive many rewrites in a tight loop from the test itself with
  polling threads racing the writer, rather than waiting out real K-second
  intervals). For staleness *classification* correctness, a single controlled
  test manipulating `timestamp_epoch` directly (rather than waiting real
  wall-clock time) is sufficient — this is a pure arithmetic check
  (`now - timestamp_epoch > staleness_threshold_secs`), not a timing-sensitive
  one.
- **E4 (partial-run honesty):** a *coverage-of-kill-timing* question, not a
  rate one. Because the summary/status stub is written at launch (before
  model build), the invariant must hold at **every** possible kill point —
  the test suite should kill the synthetic process at several representative
  points (immediately after launch, mid-Adam-epoch, mid-checkpoint-write) to
  demonstrate the invariant does not depend on *when* the interruption lands,
  rather than testing only one convenient kill point.

### Sampling Rate
- **Per task commit:** the quick-run command above (targeted `test_step_log`
  + `test_prohibitions` — the two modules most likely to regress from any
  later touch to the logging path).
- **Per wave merge:** the full-suite `discover` command.
- **Phase gate:** full suite green before `/gsd-verify-work`, plus one manual
  smoke run of the real `python -m pinn.train --config configs/stage0-example.yaml`
  against the synthetic/dataset-free path, Ctrl-C'd once mid-run to visually
  confirm the human `train.log` line shape and a real `tensorboard --logdir
  runs/<name>/tb` launch renders the panel (this manual step is not
  automatable inside `unittest` — it is the OPS-01 "reviewer can execute
  Launch verbatim from the runbook" acceptance criterion).

### Wave 0 Gaps
- [ ] `tests/phase42/__init__.py` + `_SKIP_PHRASE` constant (mirror
      `tests/phase41/__init__.py` exactly) — covers all Req IDs below
- [ ] `tests/phase42/_fixtures.py` — thin extension of
      `tests/phase41/_fixtures.py::make_synthetic_stage0_loop` adding a
      forced-divergence injection knob (a stub loss that returns NaN on a
      chosen step) and a forced-HALT injection knob, reusing the existing
      Phase 40 injection seam (TRAIN-01's forced-signal injection) rather than
      inventing a second one
- [ ] `tests/phase42/test_step_log.py` — covers OPS-03, E1
- [ ] `tests/phase42/test_tensorboard_panel.py` — covers OPS-04b (uses
      `EventAccumulator`, per Pitfall 3)
- [ ] `tests/phase42/test_signals.py` — covers OPS-02, E2 (subprocess-based;
      needs a minimal real `--config` pointing at the synthetic/dataset-free
      path so `python -m pinn.train` can actually start under a real OS
      process for signal delivery)
- [ ] `tests/phase42/test_heartbeat.py` — covers OPS-04a, E3
- [ ] `tests/phase42/test_run_contract.py` — covers OPS-05, E4
- [ ] `tests/phase42/test_prohibitions.py` — covers must-NOT #1, #2 (mirrors
      the `test_prohibitions.py` naming precedent from phase40/phase41)
- [ ] `tests/phase42/test_wrapper.py` — covers must-NOT #3 (the only test that
      genuinely shells out to `scripts/train-unattended.sh` and real
      `caffeinate`, since this project is single-machine and that is the
      actual target environment)
- [ ] `tests/phase42/test_runbook.py` — covers OPS-06 (doc-structure check)
- [ ] `tests/phase42/test_config_yaml.py` — covers OPS-06 (example config
      loads); may simply extend `tests/phase41/test_config_yaml.py`'s pattern
      rather than being a wholly separate module — planner's call

*(Framework install: none — `unittest` is stdlib; `tensorboard`/PyYAML already present.)*

## Security Domain

`security_enforcement` is absent from `.planning/config.json` → treated as
enabled.

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | No | Single-user local CLI tool; no authentication surface exists or is introduced |
| V3 Session Management | No | No session concept in this phase |
| V4 Access Control | No | No multi-user access-control surface |
| V5 Input Validation | Yes (extension, not new) | The new `run.monitor` nested config section (CTX-80) must follow the *existing* Phase-41 fail-closed pattern exactly: unknown keys raise `ConfigKeyError` naming the dotted path (`_map_section` in `config_yaml.py` already does this recursively for any new nested dataclass — no new validation code needed beyond defining `MonitorConfig` as a frozen dataclass alongside `GuardConfig`/`CheckpointCadence`) |
| V6 Cryptography | No | No cryptographic operations introduced by this phase (the existing `config_identity` sha256 digest is Phase 41's concern, untouched here) |
| V7 Error Handling / Logging (information disclosure) | Yes | Every handoff artifact (`train.log`, `train.log.jsonl`, `status.json`, `summary.*`, `failure/`) must record only run-directory-relative paths and no hostname/secret — this is exactly must-NOT #2 / CTX-79, already locked; the standard control is a negative grep test over a synthetic run's full output tree for `/Users/`, `socket.gethostname()`'s value, and common secret-token shapes |

### Known Threat Patterns for this stack

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Absolute path / hostname / secret leakage into a handed-off `runs/<name>/` directory | Information Disclosure | Run-directory-relative paths only in every emitted artifact; negative grep test (must-NOT #2) — already locked by CTX-79, re-verified as the correct control here |
| A monitoring-layer failure (TB writer exception, heartbeat thread crash) taking down the training process it is supposed to observe | Denial of Service (self-inflicted) | "One warning then continue" wrapper around every TB call (CTX-69) and around the heartbeat thread's write attempts — a monitoring exception must never propagate into the step loop or kill the process |
| A second SIGINT's `os._exit()` escalation leaving `status.json` mid-write | Tampering (of the artifact's own integrity, not an external actor) | Already covered by `atomic_io.atomic_write_text`'s temp+rename ordering (E2/E3) — an escalated exit either lands before or after a complete atomic rewrite, never mid-rewrite, because the rename step is the only state-visible mutation and it is a single syscall |
| Run-name path traversal (`run_name` containing `../`) | Tampering / path confusion | Already guarded by `train.py:_resolve_run_dir` (canon, owned by `/gsd-secure-phase` per the SPEC's own edge-coverage dismissal) — not re-litigated by this phase; Phase 42's new files (`logs/`, `tb/`, `summary.*`, `status.json`) are all written *under* the already-validated `run_dir`, inheriting its guarantee |

No new threat surface is introduced beyond what CTX-79's redaction policy and
CTX-69's "never abort training" rule already lock — this section confirms
those two locked decisions are, in fact, the complete and correct security
posture for this phase's scope, mapped onto the standard vocabulary.

## Sources

### Primary (HIGH confidence)
- Direct execution in the exact `pinn-train` conda environment on this
  machine, this session — `[VERIFIED: pinn-train env, tensorboard 2.21.0,
  torch 2.12.1, Python 3.11.15]`: TensorBoard `SummaryWriter`/`FileWriter`/
  `_AsyncWriter`/`EventFileLoader`/`EventAccumulator` source inspection and
  live NaN round-trip (write → raw-parse → `EventFileLoader` → `EventAccumulator`);
  `torch.mps.driver_allocated_memory`/`current_allocated_memory`/`device_count`
  live values; `signal.signal()` non-main-thread `ValueError`;
  `json.dumps(allow_nan=False)` exact error text.
- Direct reading of the actual source files this phase modifies, this
  session — `[VERIFIED: codebase]`: `pinn/train.py` (full), `pinn/training/
  controllers.py` (`_log_step`, `_run_adam_phase`, `run_stage` L-BFGS section,
  `_build_anchor_context`, `_non_data_terms`, `build_checkpoint_payload`,
  `CurriculumController._log_*`/`step`/`run`), `pinn/training/guards.py`
  (`_json_safe_scalar`, `_default_memory_signal`, `write_failure_bundle`),
  `pinn/loss_catalog.py` (`causal_physics_loss` in full), `pinn/training/
  config.py` (`GuardConfig`/`CheckpointCadence`/`RunConfig`/`TrainingConfig`/
  `provisional_fields`), `pinn/training/config_yaml.py` (full),
  `pinn/training/atomic_io.py` (full), `pinn/training/checkpoint.py`
  (cadence/`curriculum.jsonl` methods), `pinn/training/collocation_sampler.py`
  (`uniform`), `pinn/constants.py` (`CAUSAL_ETA_C`).
- `man caffeinate` (local, this machine) — `[VERIFIED: local authoritative
  source]`: `-i`/`-s`/`-w` semantics, assertion lifetime tied to the wrapped
  utility.
- PyTorch 2.12 official documentation via context7
  (`/websites/pytorch_2_12`) — `[VERIFIED: official docs, matches installed
  version]`: `torch.mps.driver_allocated_memory`/`current_allocated_memory`/
  `recommended_max_memory` signatures; `SummaryWriter` asynchronous-writing
  statement ("training programs can add data directly from the training loop
  without slowing down the training process").
- `docs/README.md` (this repo, full relevant sections read) —
  `[VERIFIED: project governance doc]`: `docs/runbooks/` placement rules;
  frontmatter scope.
- `docs/runbooks/external-research/2026-06-11-external-research-workflow.md`
  — `[VERIFIED: existing file, read directly]`: confirms frontmatter is used
  on runbooks in practice, extending the README's literal `docs/work/`-only
  text.
- `tests/phase41/__init__.py`, `tests/phase41/_fixtures.py` (docstrings +
  structure) — `[VERIFIED: codebase]`: skip-phrase discipline,
  `make_synthetic_stage0_loop` fixture.

### Secondary (MEDIUM confidence)
- Tavily web search, cross-checked against well-established stdlib semantics
  — `[CITED: tavily search results, adamj.eu/tech/2021/10/10, zetcode.com]`:
  `os._exit()` vs `sys.exit()` cleanup/flush/atexit distinction.
- Web search on Python's documented signal-and-threads model — `[CITED:
  general web search, consistent with the empirical Bash test above]`: "only
  the main thread receives signals" framing.

### Tertiary (LOW confidence)
- None used as load-bearing for any recommendation in this document.

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — no new packages; both existing dependencies verified
  live in the exact target environment.
- Architecture: HIGH — every pattern is either the already-locked CTX
  mechanism or a directly-verified library/stdlib behavior; the three
  code-level findings (Pitfalls 2, 3, 8) come from reading the actual
  functions being modified, not inference.
- Pitfalls: HIGH for 1–6 and 8 (verified by direct execution or direct source
  reading); MEDIUM for 7 (queue-blocking mechanism verified from source, but
  the "unlikely to matter at log_freq=100" judgment is an inference, logged
  as Assumption A1).

**Research date:** 2026-07-18
**Valid until:** 30 days (stable stdlib/PyTorch APIs; re-verify the
tensorboard NaN-readback quirk if `tensorboard` is ever upgraded past 2.21.0,
since it may be fixed or change shape in a later release).
