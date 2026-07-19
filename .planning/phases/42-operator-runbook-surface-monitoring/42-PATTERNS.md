# Phase 42: Operator Runbook Surface & Monitoring — Pattern Map

**Mapped:** 2026-07-18
**Files analyzed:** 16 new/modified artifacts (13 new, 3 modified-existing seams)
**Analogs found:** 13 strong/role-match · 3 wiring-only (mechanism is first-of-kind in repo) / 16

**Governing principle (repeated across every row below):** Phase 42 EXTENDS four
existing seams — the `pinn.training.*` logger tree (CTX-45), the `run.guards`/
`run.checkpoint` nested-config pattern, `atomic_io.atomic_write_text`, and the
`train.py main()` composition root. No new file in this phase invents a second
emission path, a second config-loading mechanism, or a second atomic-write
primitive. Where a mechanism has **no existing analog** (TensorBoard, background
threads, POSIX signal handling), that is called out explicitly — build it from
the SPEC/CONTEXT design, not from an invented "closest" analog.

---

## File Classification

| New/Modified File (illustrative name — exact split is discretion) | Role | Data Flow | Closest Analog | Match Quality |
|---|---|---|---|---|
| `pinn/training/step_log.py` — `STEP_LOG_FIELDS` registry + step-record assembly | model/registry | transform | `pinn/training/resume.py` `RESUME_FIELD_REGISTRY` + `resume_field_classification_provisional_entry()` | role-match (strong) |
| `pinn/training/step_log.py` (or sibling) — JSONL `logging.Handler` + non-finite sanitizer | hook/utility | streaming | `pinn/training/controllers.py` `_log_step`'s `extra=` convention; **anti-pattern ref** `guards._json_safe_scalar` | role-match |
| `pinn/training/step_log.py` (or sibling) — human `train.log` `logging.Formatter` | hook/utility | streaming | `pinn/training/guards.py` `write_failure_bundle`'s `readme_line` f-string template | partial-match (no verbatim template exists) |
| `pinn/training/monitor.py` — TensorBoard sink (wraps `SummaryWriter`) | utility/sink | streaming | none for the mechanism; wiring shape = `train.py` hook-closures | **no analog** (first TB usage in repo) |
| `pinn/loss_catalog.py` — additive `return_details=` path on `causal_physics_loss` | model/utility (MODIFIED) | transform | itself (existing function, lines 208–261) | exact (self-extension) |
| `pinn/training/monitor.py` — `status.json` heartbeat writer + daemon-thread loop | service/utility | file-I/O + event-driven | write-mechanics: `guards.write_failure_bundle` (dict→`json.dumps`→`atomic_write_text`); threading itself = **no analog** | role-match (write path) / no analog (thread) |
| `pinn/training/summary.py` — `summary.md`/`summary.json` stub-then-finalize writer | service/utility | file-I/O | `guards.write_failure_bundle` (Tier-A always-write) + `config_yaml.freeze_resolved_config` | role-match (strong) |
| `pinn/training/signals.py` — debounce/stop-flag pure helper | utility | event-driven | closure-dict idiom in `train.py` (`curriculum_holder`, `best_val_cell`); `signal.signal()` registration itself = **no analog** | partial-match |
| `pinn/training/config.py` — add `MonitorConfig` + `RunConfig.monitor` (MODIFIED) | config | transform | `GuardConfig` / `CheckpointCadence` in the same file (lines 177–239) | exact |
| `pinn/training/config_yaml.py` — register `MonitorConfig` in `_resolve_nested_cls` (MODIFIED) | config | transform | existing known-name dict entries (lines 92–105) | exact |
| `pinn/train.py` `main()` — signals, dir scaffolding, sink attach, heartbeat start, terminal finalize (MODIFIED) | controller/composition-root | request-response + event-driven | itself — `checkpoint_hook`/`guard_hook`/`curriculum_holder` wiring (lines 369–481) | exact (self-extension) |
| `pinn/training/controllers.py` `_log_step` — widen `extra=` payload (MODIFIED) | controller | event-driven | itself (lines 570–595) | exact (self-extension) |
| `scripts/train-unattended.sh` (name discretionary) | script | request-response | `scripts/agent-claim` / `scripts/agent-release` | exact |
| `configs/stage0-example.yaml` | config | transform (load) | `tests/phase41/test_train_entrypoint.py::_write_config` inline dict (lines 37–86) | role-match (only config-shaped analog in repo) |
| `docs/runbooks/training/<date>-stage0-training-operator-runbook.md` | doc | n/a | `docs/runbooks/external-research/2026-06-11-external-research-workflow.md` (frontmatter) + `docs/runbooks/maintenance/doc-integrity-audit-runbook.md` (checklist structure) | role-match |
| `tests/phase42/{__init__.py,_fixtures.py,test_*.py}` | test | n/a | `tests/phase41/` wholesale | exact |

---

## Anti-Patterns (explicit — do not fork these seams)

1. **Do not reuse `guards._json_safe_scalar`'s string-sentinel behavior in the
   JSONL formatter (CTX-67).** `guards.py:124-140` converts non-finite floats to
   the strings `"NaN"`/`"Inf"`/`"-Inf"` — that is a `trip.json`-local convention
   for the failure bundle only. The JSONL step log MUST serialize non-finite
   values as JSON `null` via `json.dumps(..., allow_nan=False)`, adding
   `"finite": false` + `"nonfinite_keys": [...]` to the record instead. String
   sentinels in the canonical log break typed parsers — this is the SPEC's E1
   rejection, not a style preference.
2. **Do not rename `run.log_every` to `log_freq` (CTX-66).** The SPEC's prose
   calls the cadence knob `log_freq`; the concrete field is `RunConfig.log_every`
   (`config.py:253`) and it stays that name. `log_freq` is a SPEC-doc synonym,
   never a schema key.
3. **Do not add a third hook-closure constructor parameter to `RunController`.**
   `checkpoint_hook` and `guard_hook` (`train.py:388-481`, `controllers.py`
   constructor) are the ESTABLISHED hook-injection mechanism, but CTX-65 is
   explicit that the widened step record has **no new hook closure, no second
   emission path**. JSONL/human/TensorBoard sinks attach as `logging.Handler`
   instances on the existing `pinn.training` logger tree
   (`logging.getLogger("pinn.training")`), consuming the `extra=` dict
   `_log_step` already widens — they do NOT become new `RunController`
   constructor arguments.
4. **Do not use `atomic_io.atomic_write_text` for `train.log.jsonl`.** That
   primitive does a full temp-write + `os.replace` per call — correct for
   `status.json`/`summary.*`/`config.yaml` (rewritten-in-place artifacts) but
   wrong for an **append-only, ever-growing** log (CTX-66: "append-mode text
   stream, flushed per logged step, no per-line fsync — `status.json` is the
   atomic surface, the JSONL is append-only"). Open once in `"a"` mode, write +
   `flush()` per record; do not call the atomic-replace path per line.
5. **Do not add process-level side effects to `pinn/training/` library
   modules.** No `signal.signal(...)`, no `threading.Thread(...).start()`, no
   `SummaryWriter(...)` construction, no `logging.getLogger(...).addHandler(...)`
   at module import time or inside any `pinn/training/*.py` class method that
   isn't explicitly invoked by the composition root. `pinn/training/__init__.py`
   states this discipline outright (`__init__.py:11-16`: "performs NO model
   build and NO dataset discovery... side-effect-free"); Phase 42 extends the
   same discipline to signals/threads/sinks — those are wired ONLY inside
   `pinn/train.py main()`.
6. **Do not forget to register `MonitorConfig` in `config_yaml.py`'s
   `_resolve_nested_cls` known-name dict** (`config_yaml.py:92-105`). Because
   the module uses `from __future__ import annotations`, every dataclass field
   annotation is a string at runtime; nested types are resolved by NAME through
   that dict. `GuardConfig`/`CheckpointCadence`/etc. are hand-listed there —
   adding `MonitorConfig` to `RunConfig` without adding it to this dict means
   `run.monitor.*` YAML keys silently fail to map onto the dataclass (the
   nested-mapping branch in `_map_section` is simply never reached).
7. **Do not fabricate pre-step-0 losses in the `initializing` status.json
   state.** CTX-74: `state: "initializing"` is written immediately after
   run-dir creation, before model/data build, with `step: null` and loss fields
   `null` — never a placeholder `0.0` or copied stale value.

---

## Pattern Assignments

### 1. `STEP_LOG_FIELDS` registry (⚖ owner-attention seam)

**Analog:** `pinn/training/resume.py` (`RESUME_FIELD_REGISTRY` + its
`provisional_fields()` bridge) — this is the SAME B-5 pattern CTX-68 names
explicitly.

**Registry-dict pattern** (`pinn/training/resume.py:42-53`):
```python
# ⚖ PROVISIONAL — CTX-57 Conservative identity line + operational whitelist.
# Owner-ratify before run #1. Fail-safe: any field NOT in this registry
# defaults to UNCLASSIFIED → refuse.
# Each entry: {"class": ..., "coverage": ... (IDENTITY only), "provisional": True}
RESUME_FIELD_REGISTRY: dict[str, dict[str, Any]] = {
    # ---- IDENTITY (REPRESENTED — concrete fields in build_identity_payload) ----
    "run.seed": {
        "class": CLASS_IDENTITY,
        "coverage": COVERAGE_REPRESENTED,
        "provisional": True,
    },
    "run.precision": {
        "class": CLASS_IDENTITY,
    ...
```
`STEP_LOG_FIELDS` copies this shape: a module-level `dict[str, ...]` (or tuple
of field-descriptor dataclasses) naming each canonical key (`step`, `stage`,
`phase`, `epoch`, `data`, `ic`, `phys`, `energy`, `angmom`, `total`, the λ
vector components, `grad_norm`, the `w_n` stats, `lr`, `s_per_step`,
`eta_seconds`), each tagged provisional with a provenance string.

**Owner-attention bridge pattern** (`pinn/training/resume.py:593-609`):
```python
def resume_field_classification_provisional_entry() -> dict[str, Any]:
    """⚖ provisional_fields() entry for the B-5 registry seam."""
    return {
        "name": "resume_field_classification_registry",
        "value": "PROVISIONAL",
        "provisional": True,
        "provenance": (
            "⚖ PROVISIONAL (B-5 / CTX-57 Conservative identity line): "
            "RESUME_FIELD_REGISTRY in pinn.training.resume covers architecture, "
            ...
        ),
    }
```
This function is appended into `TrainingConfig.provisional_fields()`
(`config.py:520-539`) via a try/`ImportError`-guarded import, which is itself
logged at run start by `CurriculumController._log_run_start`
(`controllers.py:1193-1202`). `STEP_LOG_FIELDS` needs the identical bridge: a
`step_log_fields_provisional_entry()`-shaped function appended the same way, so
the widened field set shows up in the SAME run-start owner-attention log line
operators already see — do not invent a second "provisional seam" logging
mechanism.

**Copy exactly:** the dict-of-descriptors + provisional/provenance shape, the
`provisional_fields()` append-with-`ImportError`-guard idiom
(`config.py:520-539`), and the fact that additive keys are non-breaking (JSONL
readers ignore unknown keys — no schema-version bump needed for new fields).

---

### 2. JSONL step-log handler + non-finite sanitizer (OPS-03, E1)

**Analog:** the existing `_LOGGER.info(..., extra={...})` emission convention
already used at the ONE place this phase widens, plus the CTX-45 logger-tree
design. **Explicit anti-pattern:** `guards._json_safe_scalar` (see Anti-Patterns
#1 above) — read it to understand what NOT to copy.

**Existing emission point to widen** (`pinn/training/controllers.py:570-595`):
```python
def _log_step(self, *, step: int, loss_terms: Any, lr: Optional[float], phase: str) -> None:
    """CTX-52 minimal functional step log (canonical JSONL is Phase 42)."""
    try:
        total = float(loss_terms.total.detach()) if hasattr(loss_terms, "total") else float("nan")
        terms = {
            "data": float(loss_terms.data.detach()) if hasattr(loss_terms, "data") else None,
            ...
        }
    except Exception:
        total = float("nan")
        terms = {}
    _LOGGER.info(
        "step=%s phase=%s total=%s lr=%s terms=%s",
        step, phase, total, lr, terms,
        extra={
            "event": "step",
            "step": step,
            "phase": phase,
            "total": total,
            "lr": lr,
            **{f"loss_{k}": v for k, v in terms.items()},
        },
    )
```
Widen the `extra={...}` dict in place (add `stage`, λ vector, `grad_norm`,
`w_n` stats, per-bin residuals, `s_per_step`, `eta_seconds`, `epoch`) — do not
add a parallel emission call. `_LOGGER = logging.getLogger("pinn.training.controllers")`
(`controllers.py:970`) is a child of the `pinn.training` tree the JSONL handler
attaches to.

**Handler attach point** — mirrors how `train.py` already constructs
long-lived objects once and holds them via closures (`checkpoint_hook`,
`guard_hook`, `store = TorchSaveCheckpointStore(...)` at `train.py:354`):
```python
# In pinn/train.py main(), after run_dir/logs/ exist:
logger = logging.getLogger("pinn.training")
logger.addHandler(JsonlStepHandler(run_dir / "logs" / "train.log.jsonl"))
logger.addHandler(HumanStepHandler(run_dir / "logs" / "train.log"))
```

**Non-finite policy (CTX-67, do not deviate):** `json.dumps(record, allow_nan=False)`
on a record where any non-finite value has ALREADY been replaced by Python
`None` (→ JSON `null`) before serialization, with `"finite": false` and
`"nonfinite_keys": [...]` added to the same record. `allow_nan=False` is a
belt-and-suspenders assertion, not the primary sanitization mechanism — the
sanitize step must run first or `json.dumps` raises on a raw `float('nan')`.

**Append-only write mechanics (CTX-66, contrast with atomic_io):** open the
file once in `"a"` (append) mode at handler construction, `write()` + `flush()`
per emitted record, no `os.fsync`, no temp+rename. This deliberately does NOT
reuse `atomic_io.atomic_write_text` — see Anti-Patterns #4.

---

### 3. Human `train.log` mirror

**Analog:** `pinn/training/guards.py` `write_failure_bundle`'s single-line
f-string template assembly (`guards.py:449`):
```python
readme_line = f"guard={guard} step={step} stage={stage} reason={reason}\n"
```
This is the closest EXISTING precedent for "assemble one human-readable line
from a flat dict of scalars" in the codebase — there is no repo-wide log-line
formatter to inherit from, so the design-§5.4 shape is new text, built the same
way: pull fields out of the SAME widened record the JSONL handler consumes,
join with the documented `|`-delimited shape (`step N | stage k phase 2a |
total=… data=… ic=… phys=… energy=… angmom=… | lr=… | 1.2 s/step | ETA
01:23:45`), and log it as a second handler on the SAME `pinn.training` logger
(a `logging.Formatter`, not a second `_LOGGER.info()` call site).

Non-step events (run start, provisional-threshold set, stage dispositions,
`mem:` lines, guard trips) already flow through this same logger tree — see
`controllers.py:1193-1229` (`_log_run_start`, `_log_stage_exit`,
`_log_handoff_if_any`) for the established "one `_LOGGER.info(msg, extra={...})`
call per event kind" idiom the human formatter must render sensibly for
non-step records too.

---

### 4. TensorBoard sink + per-time-bin residual panel (OPS-03/04b, no analog)

**No existing analog** — confirmed by repository-wide search: no
`SummaryWriter`, no `torch.utils.tensorboard` import anywhere under `pinn/`.
Build directly from CTX-69/70, not from a "closest" file.

**Construction/wiring shape to copy** (structural precedent only — the
"construct once at composition root, invoke every logged step" idiom already
used for `store`/`step_guards` in `train.py:354-355`):
```python
store = TorchSaveCheckpointStore(ckpt_dir, config=config)
step_guards = StepGuards(config, disk_root=run_dir)
```
The TB writer follows the same shape: `SummaryWriter(log_dir=run_dir / "tb")`
constructed once in `main()`, held by a closure/handler, fed `add_scalar` calls
from the same widened step record.

**Exposure mechanism — the one MODIFIED existing file in this component**
(`pinn/loss_catalog.py:208-261`, `causal_physics_loss`): add an additive
`return_details=` keyword (default `False`, unchanged return type by default —
Phase 38/40 tests untouched) that additionally returns **detached** per-bin
`Rbar_n` and `w_n` tensors:
```python
def causal_physics_loss(residuals_per_time, *, eta_c=CAUSAL_ETA_C, times=None,
                        dtype, device):
    ...
    rbar = torch.as_tensor(residuals_per_time, dtype=dtype, device=device).reshape(-1)
    ...
    detached = rbar.detach()
    cumsum = torch.cumsum(detached, dim=0)
    zeros = torch.zeros(1, dtype=dtype, device=device)
    cumsum_excl = torch.cat([zeros, cumsum[:-1]], dim=0)
    weights = torch.exp(-eta * cumsum_excl)
    _ = CAUSAL_W1
    return (weights * rbar).mean()
```
`weights` (== `w_n`) and `rbar` are already computed locally and already
`.detach()`-able — the additive path returns `weights.detach()` and
`rbar.detach()` alongside the scalar loss (e.g. via a `sibling helper` or a
`return_details=True` branch returning a small namedtuple/dataclass), never
retaining the autograd graph. Panel tag names are CTX-70-mandated:
`residuals/bin_{n:02d}`, `causal/w_min`, `causal/w_mean`, `causal/w_max`,
`causal/front_idx`.

**Emission ordering (do not violate):** the panel must emit even when a guard
trips or `w_n` collapses toward zero — wire the TB `add_scalar` calls at the
SAME point `_log_step` fires (after loss computation, before/regardless of the
guard early-return), not gated behind "no guard tripped".

---

### 5. `status.json` heartbeat writer + daemon thread (OPS-04a, E3)

**Write-mechanics analog (strong):** `pinn/training/guards.py`
`write_failure_bundle`'s Tier-A always-write pattern
(`guards.py:451-456`):
```python
# ---- Tier-A ALWAYS ----
atomic_write_text(fail_dir / "README.txt", readme_line)
atomic_write_text(
    fail_dir / "trip.json",
    json.dumps(info, sort_keys=True, indent=2, default=str) + "\n",
)
```
`status.json` reuses `atomic_io.atomic_write_text` (`atomic_io.py:41-64`)
UNCHANGED — build the snapshot dict, `json.dumps(...)`, hand the string to
`atomic_write_text(status_path, text)`. This is exactly the "temp + fsync +
os.replace + dir fsync" idiom (`atomic_io.py:7-9,25-38`) the SPEC's "reader
never sees truncated JSON" acceptance criterion requires — do not write a
second atomic-write implementation.

**Threading itself — no analog** (confirmed: no `threading.Thread` usage
anywhere in `pinn/`). Build per CTX-74: a daemon thread rewriting
`status.json` every `heartbeat_secs` from a mutex-guarded snapshot the step
loop updates, PLUS synchronous rewrites at every state transition and every
logged step. The thread is started/stopped ONLY in `train.py main()` (Anti-
Pattern #5) — the snapshot-dict-builder and the `atomic_write_text` call are
pure functions importable from `pinn/training/monitor.py`; only
`threading.Thread(...).start()` is composition-root code.

**Schema fields (CTX-75):** `schema_version`, `run_name`, `pid`, `state`,
`timestamp_utc`, `timestamp_epoch`, `heartbeat_interval_secs`,
`staleness_threshold_secs`, `step`, `stage`, `phase`, `epoch`, latest losses
(null-policy per Anti-Pattern #7 / CTX-67), `lr`, `s_per_step_ema`,
`eta_seconds`, memory fields.

**`mem:` line source** (`pinn/training/guards.py:143-161`,
`_default_memory_signal`):
```python
def _default_memory_signal() -> Optional[int]:
    try:
        import torch
    except ImportError:
        return None
    if not hasattr(torch, "mps"):
        return None
    try:
        return int(torch.mps.driver_allocated_memory())
    except Exception:
        return None
```
Reuse this exact signal (or the already-wired `StepGuards` internal call to
it) for the periodic `mem:` line in `train.log` and the mirrored `status.json`
memory fields — no `psutil`, no new dependency (CTX-76 is explicit).

---

### 6. `summary.md` / `summary.json` stub-then-finalize writer (OPS-05, E4)

**Analog:** `pinn/training/guards.py` `write_failure_bundle` end-to-end
(`guards.py:407-472`) for the "always-write, honest content, atomic per-file"
shape, plus `pinn/training/config_yaml.py` `freeze_resolved_config`
(`config_yaml.py:263-282`) for the "write a derived artifact via
`atomic_write_text` at one defined lifecycle moment" idiom:
```python
def freeze_resolved_config(config: TrainingConfig, run_dir: PathLike) -> Path:
    destination_dir = Path(run_dir)
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination = destination_dir / "config.yaml"
    plain = resolved_config_to_dict(config)
    text = yaml.safe_dump(plain, sort_keys=True, allow_unicode=True)
    atomic_write_text(destination, text)
    return destination
```
`summary.md`/`summary.json` follow the SAME shape twice: once at launch (honest
"in progress" stub, called from `train.py main()` right after `logs/`/`tb/`/
`failure/` are created) and once at the terminal transition (atomic replace
with the final one-pager). Both calls go through `atomic_write_text` — never a
raw `open(...).write()`.

**Content source for curriculum progression:** `runs/<name>/curriculum.jsonl`
(CTX-56, already produced by Phase 41) — render, don't recompute.

**Honesty invariant (must-NOT #1, do not violate):** a failed/interrupted run's
`summary.md` uses the SAME writer with a different (still-honest) template —
never write partial/placeholder numeric fields; use the CTX-67 null policy for
any loss term that never finalized.

---

### 7. Signal handling + `caffeinate -is` wrapper (OPS-01/02, E2)

**Signal-state helper — weak analog only.** The closure-held-mutable-dict idiom
already used twice in `train.py` (`curriculum_holder`, `best_val_cell`,
`train.py:369-386,400-408`) is the closest existing precedent for "small piece
of mutable state closed over by callbacks registered at the composition root":
```python
curriculum_holder: dict[str, Any] = {"curriculum": None}
...
best_val_cell: dict[str, float] = {"best": float("inf")}
```
A `SignalState` (first-SIGINT timestamp, stop-requested flag, escalate flag)
follows the same shape — a small dataclass or dict constructed in `main()`,
mutated by the handler closures, read by the step-boundary check. **Actual
`signal.signal(SIGINT, ...)` / `signal.signal(SIGTERM, ...)` registration has
no analog anywhere in the repo** — install it directly in `pinn.train main()`
per CTX-71 (library stays signal-free and importable, per Anti-Pattern #5).

**Graceful checkpoint reuse (CTX-72, do not invent a new flavor):**
`pinn/training/checkpoint.py` `save_rolling` (`checkpoint.py:349-358`):
```python
def save_rolling(self, payload: Any, step: int) -> str:
    """Write ``step-{step:06d}.pt``, refresh latest.pt, run rolling retention."""
    step = int(step)
    name = f"step-{step:06d}.pt"
    path = self._root / name
    atomic_write_torch(path, payload)
    atomic_write_torch(self._root / "latest.pt", payload)
    self._mark_written(step=step)
    self._evict_rolling()
    return name
```
On SIGINT/SIGTERM, call the SAME `store.save_rolling(build_checkpoint_payload(...))`
path `train.py`'s existing `checkpoint_hook` already uses
(`train.py:388-397`) — resume-after-interrupt is the ordinary `--resume latest`
flow (`train.py:288-292,488-514`), not a new resume mode.

**Wrapper script — exact analog found in `scripts/`:**
```bash
#!/usr/bin/env bash
set -euo pipefail
repo_root="$(git rev-parse --show-toplevel)"
exec python3 "$repo_root/scripts/git_policy/agent_claims.py" claim "$@"
```
(`scripts/agent-claim`, full file, 4 lines; `scripts/agent-release` is
byte-for-byte the same shape). Copy this EXACT idiom for
`scripts/train-unattended.sh`:
```bash
#!/usr/bin/env bash
set -euo pipefail
exec caffeinate -is python -m pinn.train "$@"
```
`exec` (removing the shell layer) is why the inner exit status propagates
verbatim — this is the must-NOT-#3 acceptance test (wrapper exit == inner
exit); do not wrap the `caffeinate` call in a function, subshell, or
`$(...)` capture that would swallow or transform the exit code. No
machine-specific absolute paths in the script (CTX-73) — contrast with
`scripts/agent-claim`'s `git rev-parse --show-toplevel` resolution, which
IS portable and may be reused if the wrapper needs the repo root, but
`caffeinate -is python -m pinn.train` itself needs no path resolution at all.

---

### 8. `MonitorConfig` under `run.monitor` (OPS-04a config seam)

**Analog:** `GuardConfig` and `CheckpointCadence` in the SAME file
(`pinn/training/config.py:177-239`) — copy this pattern verbatim, do not
invent a new config idiom.

**Frozen-dataclass + `__post_init__` validation pattern**
(`config.py:177-203`):
```python
@dataclass(frozen=True)
class GuardConfig:
    """R-1 guard thresholds (run.guards) — ⚖ provisional defaults.
    ...
    """

    loss_explosion_ceiling: float = _PROVISIONAL_LOSS_EXPLOSION_CEILING
    disk_floor_fraction: float = _PROVISIONAL_DISK_FLOOR_FRACTION
    memory_watermark_fraction: float = _PROVISIONAL_MEMORY_WATERMARK_FRACTION

    def __post_init__(self) -> None:
        prov = "⚖ PROVISIONAL R-1 guard threshold (owner-calibrate-at-Phase-43-pilot)"
        ceiling = _finite_positive(
            "loss_explosion_ceiling", self.loss_explosion_ceiling, prov
        )
        ...
        object.__setattr__(self, "loss_explosion_ceiling", ceiling)
```
`MonitorConfig` needs: `heartbeat_secs: int = 30`, `staleness_factor: int = 3`,
plus discretionary cadence knobs (TB histogram thinning etc.), each validated
through the SAME module-level helpers already imported/defined at the top of
`config.py` (`_require_int`, `_finite_positive`, `_finite_unit_interval`) —
reuse those, do not re-derive validation logic.

**Registration on `RunConfig`** (`config.py:241-284`, both the `field(...)`
declaration and the `__post_init__` `isinstance` guard):
```python
@dataclass(frozen=True)
class RunConfig:
    ...
    guards: GuardConfig = field(default_factory=GuardConfig)
    checkpoint: CheckpointCadence = field(default_factory=CheckpointCadence)

    def __post_init__(self) -> None:
        ...
        if not isinstance(self.guards, GuardConfig):
            raise TypeError(
                f"run.guards must be GuardConfig (got {type(self.guards)!r})"
            )
        if not isinstance(self.checkpoint, CheckpointCadence):
            raise TypeError(
                f"run.checkpoint must be CheckpointCadence "
                f"(got {type(self.checkpoint)!r})"
            )
```
Add `monitor: MonitorConfig = field(default_factory=MonitorConfig)` plus the
matching `isinstance` guard, following the exact two-line pattern above.

**YAML-loader registration (do not skip — see Anti-Pattern #6):**
`pinn/training/config_yaml.py:92-105`:
```python
if isinstance(annotation, str):
    known = {
        "GuardConfig": GuardConfig,
        "CheckpointCadence": CheckpointCadence,
        "RunConfig": RunConfig,
        "StageConfig": StageConfig,
        "OptConfig": OptConfig,
        "LossConfig": LossConfig,
    }
```
Add `"MonitorConfig": MonitorConfig` to this dict AND to the `config_yaml.py`
import block (`config_yaml.py:23-31`, currently imports `CheckpointCadence,
GuardConfig, LossConfig, OptConfig, RunConfig, StageConfig` from
`pinn.training.config`) — both edits are required for `run.monitor.*` keys to
resolve; the fail-closed unknown-key loader (`_map_section`,
`config_yaml.py:134-172`) stays untouched (additive schema only, per CTX-80).

**Classification:** operational, not identity — `run.monitor.*` belongs beside
`run.checkpoint`/`run.guards` cadence knobs in the B-5 operational whitelist
(`resume.py` `RESUME_FIELD_REGISTRY`), changeable on resume.

---

### 9. Example config `configs/stage0-example.yaml`

**Analog:** the only config-shaped artifact currently in the repo is the
inline dict `tests/phase41/test_train_entrypoint.py::_write_config`
(`test_train_entrypoint.py:37-86`) builds and dumps via `yaml.safe_dump`:
```python
def _write_config(path: Path, **overrides) -> Path:
    """Write a minimal keyed YAML config (float64/cpu for deterministic tests)."""
    run = {
        "seed": 11,
        "precision": "float32",
        "device": "mps",
        "strict_cpu_determinism": False,
        "log_every": 100,
        "run_name": "test-run",
        "checkpoint": {
            "every_n_steps": 1,
            "wall_clock_ceiling_s": 3600.0,
            "rolling_keep": 5,
            "failure_keep": 10,
        },
        "guards": {
            "loss_explosion_ceiling": 1.0e12,
            "disk_floor_fraction": 0.01,
            "memory_watermark_fraction": 0.99,
        },
        # monitor: {heartbeat_secs: 30, staleness_factor: 3, ...}  <- Phase 42 adds
    }
    stage = {"max_epochs": 2, "n_adam": 2, "stagnation_window": 10_000,
              "percentile_10_relaxation": 0.1, "beta": 0.9, "patience": 50,
              "eps_plateau": 1e-5, "eps_phys": 1e-4, "eps_energy": 1e-4}
    opt = {"validation_every": 1, "lbfgs_max_iter": 2, "lbfgs_chunk_size": 4}
    loss = {"lambda_e_max": 1.0}
    doc = {"run": run, "stage": stage, "opt": opt, "loss": loss}
```
(Values above shown with `precision`/`device`/`log_every` adjusted to the
committed example's documented production defaults per CTX-81 —
`log_every: 100`, `precision: float32`, `device: mps` — the raw test fixture
uses `float64`/`cpu`/`log_every: 1` for deterministic unit tests, which the
example config must NOT copy verbatim.) The four top-level keys (`run`,
`stage`, `opt`, `loss`) and the nested `run.checkpoint.*`/`run.guards.*` (soon
`run.monitor.*`) shape are exactly what `config_yaml.load_config`
(`config_yaml.py:175-225`) accepts — the committed example must be a real
`.yaml` file (not a Python dict) that round-trips through `load_config`
without raising `ConfigLoadError`/`ConfigKeyError`, with advanced/provisional
knobs commented out per CTX-81. Validate with the same fail-closed contract
`load_config` enforces: missing file, empty parse, missing section, or unknown
key at ANY depth all raise — the "loads without error" acceptance criterion is
literally `load_config(path)` not raising.

---

### 10. Operator runbook `docs/runbooks/training/<date>-....md`

**Frontmatter analog (use this one, not the maintenance one):**
`docs/runbooks/external-research/2026-06-11-external-research-workflow.md:1-7`
has the COMPLETE 6-field schema `docs/README.md` documents:
```yaml
---
status: active
purpose: runbook
created: 2026-06-11
milestone: untracked
phase: cross-cutting
retirement_trigger: superseded by a revised ERW runbook
---
```
(`docs/runbooks/maintenance/doc-integrity-audit-runbook.md:1-7` is MISSING the
`phase` key — an older file that predates full schema adoption; do not copy
its incomplete frontmatter.) The new runbook's frontmatter should read
`purpose: runbook`, `milestone: v2.0`, `phase: 42-operator-runbook-surface-monitoring`.

**Filename convention** (`docs/README.md:197-223`, `docs-conventions.md`):
`YYYY-MM-DD-<descriptive-slug>.md`, lowercase, no `review1.md`/`final.md`-style
bare names — CTX-81's suggested name
`docs/runbooks/training/<YYYY-MM-DD>-stage0-training-operator-runbook.md`
already follows this. `training/` is a NEW subfolder under
`docs/runbooks/` (`docs/README.md:84-90` shows `docs/runbooks/<category>/` is
the established layout: `migration/`, `setup/`, `maintenance/` already exist as
sibling categories — `training/` is a peer category addition, not a
convention break).

**Section-structure analog (checklist-shaped operational runbook):**
`docs/runbooks/maintenance/doc-integrity-audit-runbook.md` demonstrates the
target shape — short origin/plan pointers, then clearly-headed sections each
scoped to one operator concern (`## When to Run`, `## Verification Checklist`
broken into numbered tracks, `## Drift Handling`). Mirror this: `## Mental
Model`, `## The Five Entry Points` (Setup/Configure/Launch/Monitor/Resume, one
subsection each, each reducible to a single copy-pasteable command per CTX-81's
entry-point mapping), `## Error Surface` (a table: symptom → meaning → action,
same shape as the doc-integrity runbook's inventory table at lines 30-44),
`## M5-Pro Notes`.

**MUST read `docs/README.md` in full before creating this file** (already done
for this pattern map — see full text gathered above; the file is 422 lines,
governing rules at `docs/README.md:73-92` for `runbooks/` placement and
`docs/README.md:225-267` for the frontmatter/lifecycle schema).

---

### 11. `tests/phase42/` suite

**Analog:** `tests/phase41/` wholesale — same skip discipline, same fixture
re-export chain, same harness idiom.

**`__init__.py` — SOLE skip-phrase constant** (`tests/phase41/__init__.py`,
full file):
```python
"""Phase 41 — config / checkpointing / resume / determinism test suite (Wave 0).
...
"""

# The SOLE definition of the deferred-skip phrase. Imported by every localized
# ``_require`` helper in this package; never re-spelled independently.
_SKIP_PHRASE = "skipped Phase41 production symbol"

__all__ = ["_SKIP_PHRASE"]
```
`tests/phase42/__init__.py` copies this exactly with `_SKIP_PHRASE = "skipped
Phase42 production symbol"`.

**Deferred-import skip guard** (`tests/phase41/test_train_entrypoint.py:22,27-34`,
identical shape confirmed in `test_guards.py`):
```python
from tests.phase41 import _SKIP_PHRASE

TRAIN_MODULE = "pinn.train"


def _require(symbol, module=TRAIN_MODULE):
    try:
        mod = importlib.import_module(module)
    except ImportError:
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {module}.{symbol}")
    if not hasattr(mod, symbol):
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {module}.{symbol}")
    return getattr(mod, symbol)
```

**Fixture re-export chain (do not duplicate bodies):**
`tests/phase41/_fixtures.py:1-30` re-exports `tests/phase40/_fixtures.py`
builders rather than copying them:
```python
# Re-export phase40 fixtures (do not duplicate bodies).
from tests.phase40._fixtures import (  # noqa: F401
    make_stub_model,
    make_stub_source,
    make_stub_split_sources,
)
```
`tests/phase42/_fixtures.py` should re-export from `tests.phase41._fixtures`
(which itself chains from phase40) the same way, adding ONLY new phase-42
stubs (e.g. a synthetic multi-step run driver reused across signal/heartbeat/
contract tests) rather than re-deriving `make_stub_split_sources` etc.

**Harness idiom — tmp runs-root + monkeypatched module state**
(`test_train_entrypoint.py:89-115`):
```python
class _TrainHarness(unittest.TestCase):
    """Shared temp runs-root + config for entrypoint tests."""

    def setUp(self):
        self.main = _require("main")
        self.train_mod = importlib.import_module(TRAIN_MODULE)
        self.tmp = Path(tempfile.mkdtemp(prefix="phase41-train-"))
        self.runs_root = self.tmp / "runs"
        self.runs_root.mkdir()
        self.cfg_path = self.tmp / "cfg.yaml"
        _write_config(self.cfg_path)
        self._orig_runs = self.train_mod._RUNS_ROOT
        self.train_mod._RUNS_ROOT = self.runs_root

    def tearDown(self):
        self.train_mod._RUNS_ROOT = self._orig_runs
        shutil.rmtree(self.tmp, ignore_errors=True)
```
Signal-handling and heartbeat tests in `tests/phase42/` need this SAME harness
shape (`_TrainHarness`-derived, tmp `_RUNS_ROOT` monkeypatch) since they must
drive `pinn.train.main()` end-to-end against a synthetic run.

**Synthetic Stage-0 sources / population floor 240**
(`pinn/train.py:105-188`, `_synthetic_split_sources`):
```python
def _synthetic_split_sources(
    *, n_train: int = 240, n_validation: int = 240
) -> tuple[Any, Any]:
    """Dataset-free StageQuery-shaped sources (v2.0 falsifiability floor).

    Defaults meet the Stage-0 population floor (240) enforced by
    ``build_stage_batch`` for BOTH train and validation splits.
    """
```
and `tests/phase41/_fixtures.py:81-195` `make_synthetic_stage0_loop(...)` wires
stubs into a runnable `RunController`/`CurriculumController` pair without a
real dataset. `tests/phase42/` signal/heartbeat/contract tests should drive
THIS existing dataset-free path (or the smaller `make_stub_split_sources`
already re-exported), never touch `simulation_data/`.

**Logging assertion pattern** (`tests/phase40/test_controllers.py:428-434`):
```python
with self.assertLogs("pinn.training", level="INFO") as cm:
    controller.run()
joined = "\n".join(cm.output)
self.assertIn("provisional", joined.lower())
for field in config.provisional_fields():
    self.assertIn(field["name"], joined)
    self.assertIn(field["provenance"], joined)
```
Use `assertLogs("pinn.training", level="INFO")` (stdlib) to test that
`STEP_LOG_FIELDS` provisional entries and widened step-record keys appear on
the shared logger tree — do NOT invent a custom log-capture harness.

**Conda env invocation** (established convention, referenced in
`42-CONTEXT.md`'s Established Patterns, not literalized in any committed test
file): `<home>/miniforge3/bin/conda run -n pinn-train python -m
unittest discover tests/phase42` — same environment activation every phase-40/
41 test run already uses.

---

## Shared Patterns

### Atomic file writes
**Source:** `pinn/training/atomic_io.py:41-64` (`atomic_write_text`),
`:67-92` (`atomic_write_torch`).
**Apply to:** `status.json`, `summary.md`, `summary.json`, `configs/
stage0-example.yaml` is NOT written by training code (it's committed), but
`config.yaml` freezing already uses this. **Do NOT apply to** `train.log` /
`train.log.jsonl` (append-only — see Anti-Pattern #4).
```python
def atomic_write_text(path: PathLike, content: str) -> Path:
    destination = _as_path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(destination.name + f".tmp.{os.getpid()}")
    try:
        with open(temporary, "w", encoding="utf-8") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        _atomic_replace(temporary, destination)
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass
    return destination
```

### Frozen dataclass + `__post_init__` validation
**Source:** `pinn/training/config.py:177-239` (`GuardConfig`,
`CheckpointCadence`).
**Apply to:** `MonitorConfig`. Validate via the module's existing
`_require_int`/`_finite_positive`/`_finite_unit_interval` helpers
(`config.py:36-77`) — do not write new validation primitives.

### stdlib logging tree with `extra=` machine payloads
**Source:** `pinn/training/controllers.py:970` (`_LOGGER = logging.getLogger
("pinn.training.controllers")`), `:584-595` (`_log_step`), `:1193-1229`
(`_log_run_start`/`_log_stage_exit`/`_log_handoff_if_any`).
**Apply to:** every new logging call site (widened step record, `mem:` line,
signal/state-transition events) — always `logging.getLogger("pinn.training.<submodule>")`,
always `extra={"event": "<name>", ...}` for machine-parseable fields, message
string for humans. This tree is exactly what `assertLogs("pinn.training", ...)`
already tests against and what the JSONL/human handlers attach to.

### Composition-root-only side effects
**Source:** `pinn/training/__init__.py:11-16` (explicit discipline statement)
and `pinn/train.py:369-481` (closures/hooks constructed once in `main()`).
**Apply to:** signal handler registration, heartbeat thread start/stop,
`SummaryWriter` construction, `logging.Handler` attachment — all live ONLY in
`pinn/train.py main()`. `pinn/training/*.py` modules stay pure/importable:
functions and dataclasses only, no top-level or class-construction-time
process effects.

### Honesty-layer / always-write-something pattern
**Source:** `pinn/training/guards.py:407-472` (`write_failure_bundle`
Tier-A-always + Tier-B-best-effort).
**Apply to:** `summary.md`/`summary.json` (stub-then-finalize, never absent)
and `status.json` (`state` never claims `finished` without a real terminal
transition). The Tier-A/Tier-B split (always-write minimal honest artifact;
best-effort richer detail swallowed on failure) is the template for any
"must never be silently missing" artifact in this phase.

### ⚖ Provisional-registry + run-start owner-attention log
**Source:** `pinn/training/resume.py:46-53,593-609` (`RESUME_FIELD_REGISTRY` +
bridge function) and `pinn/training/config.py:478-539`
(`TrainingConfig.provisional_fields()`).
**Apply to:** `STEP_LOG_FIELDS` (CTX-68) — same dict-of-descriptors shape, same
`provisional_fields()` append pattern, surfaced through the SAME
`_log_run_start` call (`controllers.py:1193-1202`) operators already see at
run start.

### Deferred-import test skip guard
**Source:** `tests/phase41/__init__.py` (`_SKIP_PHRASE`),
`tests/phase41/test_train_entrypoint.py:27-34` (`_require`).
**Apply to:** every `tests/phase42/test_*.py` file — `unittest.SkipTest`, never
a bare `ImportError`/collection error, while production symbols don't exist
yet.

---

## No Analog Found

Mechanisms with no existing precedent in the codebase (confirmed by
repository-wide search — zero hits for `SummaryWriter`, `threading.Thread`,
`signal.signal`/`import signal` under `pinn/`). Build these directly from
`42-SPEC.md`/`42-CONTEXT.md` (CTX-69/70/71/74), using the wiring-shape analogs
noted in the Pattern Assignments above, not an invented code-level template:

| File/Component | Role | Data Flow | Reason |
|---|---|---|---|
| TensorBoard `SummaryWriter` sink | utility/sink | streaming | First `torch.utils.tensorboard` usage anywhere in `pinn/`; wiring shape (construct-once-at-composition-root) borrows from `checkpoint_hook`/`step_guards`, but the mechanism itself is new. |
| Heartbeat daemon thread | service | event-driven | First `threading.Thread` usage anywhere in `pinn/`; only the per-write payload (`atomic_write_text` + JSON dict) has an analog (`write_failure_bundle`). |
| Signal handler registration (`signal.signal`) | hook | event-driven | First POSIX-signal-handling code anywhere in `pinn/`; only the mutable-state-closure shape (`curriculum_holder`) has an analog. |
| Human `train.log` line micro-format | utility | streaming | The design-§5.4 line shape is net-new text; only the "assemble one f-string from a flat dict" idiom (`write_failure_bundle`'s `readme_line`) is precedented. |

---

## Metadata

**Analog search scope:** `pinn/train.py`, `pinn/training/*.py` (controllers,
config, config_yaml, guards, checkpoint, atomic_io, resume, scheduled_weights,
`__init__.py`), `pinn/loss_catalog.py`, `tests/phase40/`, `tests/phase41/`,
`docs/runbooks/**`, `docs/README.md`, `scripts/*` (top-level executables),
repository root for `configs/` (confirmed absent — genuinely new top-level
directory).
**Files scanned:** 8 production modules (full or targeted-section read), 6
test files (structure + targeted excerpts), 2 test `__init__.py` (full), 1
test `_fixtures.py` (full), 3 `docs/runbooks/*` files (2 full, 1 header-only),
`docs/README.md` (full), 5 `scripts/*` entries (3 full, 2 header-checked).
**Confirmed absent (repo-wide grep):** `SummaryWriter`, `threading.Thread`,
`signal.signal`, `import signal`, any `configs/` directory, any `caffeinate`
reference.
**Pattern extraction date:** 2026-07-18
