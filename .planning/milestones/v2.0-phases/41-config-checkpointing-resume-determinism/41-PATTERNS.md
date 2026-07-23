# Phase 41: Config, Checkpointing, Resume & Determinism - Pattern Map

**Mapped:** 2026-07-18
**Files analyzed:** 17 (8 production + 9 test)
**Analogs found:** 15 / 17 (2 partial/no-analog, both flagged below)

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|---|---|---|---|---|
| `pinn/train.py` (NEW) | entry-point/controller | orchestration (one-shot batch run) | `pinn/data/stage_scan.py` | exact (CLI shape) |
| `pinn/training/config.py` (EXTEND) | config/model | transform (validate+construct) | itself + `pinn/runtime.py` `RuntimeSpec` | exact |
| `pinn/training/config_yaml.py` (NEW; discretion on filename) | utility/mapper | transform (dict→dataclass) + file-I/O (frozen copy) | `pinn/training/config.py` (validation idiom) + `_atomic_write` idiom | role-match |
| `pinn/training/checkpoint.py` (REPLACE naive impl) | service/store | file-I/O + CRUD (save/load/rollback + retention) | itself (Protocol) + `_atomic_write` idiom (`stage_scan.py`/`splits.py`/`gradcheck_probe.py`) | role-match |
| `pinn/training/resume.py` (NEW) | service/validator | transform (digest + diff) | `pinn/data/stage_scan.py::_split_file_evidence` (sha256) + `config.py` fail-closed idiom | partial-match |
| `pinn/training/guards.py` (NEW) | middleware/service | event-driven (per-step check → disposition) | `pinn/training/stage_exit.py` (`StageExitMachine`) + `pinn/data/adapter.py` (`memory_watermark` fractional knob) | role-match |
| `pinn/training/determinism.py` (NEW) | utility | transform/config (runtime side-effect) | `pinn/runtime.py` (`resolve_runtime`) + `pinn/network.py` (`build_network` seeded-Generator discipline) | role-match |
| `pinn/training/controllers.py` (EXTEND) | controller | event-driven/stateful loop | itself (`RunController.state_dict`/`load_state_dict`) + `grad_clip.py`/`scheduled_weights.py` `state_dict` idiom | exact |
| `tests/phase41/__init__.py` (NEW) | test | n/a | `tests/phase40/__init__.py` | exact |
| `tests/phase41/_fixtures.py` (NEW) | test | n/a | `tests/phase40/_fixtures.py` | exact |
| `tests/phase41/test_prohibitions.py` (NEW) | test | n/a | `tests/phase40/test_prohibitions.py` | exact |
| `tests/phase41/test_config_yaml.py` (NEW) | test | n/a | `tests/phase40/test_config.py` | exact |
| `tests/phase41/test_checkpoint.py` (NEW) | test | n/a | `tests/phase40/test_checkpoint.py` | exact |
| `tests/phase41/test_resume.py` (NEW) | test | n/a | `tests/phase40/test_config.py` (assertRaises + message-content style) | partial-match |
| `tests/phase41/test_guards.py` (NEW) | test | n/a | `tests/phase40/test_stage_exit.py` | role-match |
| `tests/phase41/test_determinism.py` (NEW) | test | n/a | `tests/phase40/test_config.py` (`ValidationTests`/flag-assertion style) | partial-match |
| `tests/phase41/test_train_entrypoint.py` (NEW) | test | n/a | `tests/phase39/test_stage_scan.py::StageScanCliContract` | role-match |

## Pattern Assignments

### `pinn/train.py` (entry-point, orchestration)

**Analog:** `pinn/data/stage_scan.py`

**CLI convention — argparse + `main(argv) -> int` + `if __name__` tail** (`pinn/data/stage_scan.py:573-593`, `609-611`, `712-716`):
```python
def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m pinn.data.stage_scan")
    parser.add_argument("--run-dir", required=True)
    ...
    parser.add_argument("--memory-watermark", type=float, default=0.7)
    parser.add_argument("--seed", type=int, default=0)
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the deterministic DATA-06 scan without reopening admitted records."""
    args = _parser().parse_args(argv)
    ...

if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())


__all__ = ["build_population_report", "main", "write_population_report"]
```
`pinn/train.py` should mirror this shape exactly: `_parser()` builds `--config` (required), `--resume` (default `None`), `--hold-stage` (`action="store_true"`); `main(argv=None) -> int` resolves config → `resolve_runtime` → `build_network` → `CurriculumController`/`RunController` → `CheckpointStore` → run; `if __name__ == "__main__": sys.exit(main())` at the tail. A single-file module (not a package) so `python -m pinn.train` resolves it directly, exactly as `python -m pinn.data.stage_scan` resolves `stage_scan.py`.

**Fail-closed CLI validation BEFORE construction** (`pinn/data/stage_scan.py:609-619`):
```python
if not math.isfinite(args.memory_capacity_bytes) or args.memory_capacity_bytes <= 0:
    print(
        f"error: --memory-capacity-bytes must be positive and finite; "
        f"got {args.memory_capacity_bytes}",
        file=sys.stderr,
    )
    return 1
```
Apply the same shape for `--resume`'s missing-path typed error (CTRL-05 AC): validate before touching the checkpoint store, print to `sys.stderr`, return a non-zero exit code (or raise the typed error CONTEXT.md specifies — match whichever error-reporting convention the planner picks for `pinn.train`, but validate-before-construct is the load-bearing shape here).

**Freshness/identity stamping pattern** (`pinn/data/stage_scan.py:653-657`):
```python
run_timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
run_nonce = secrets.token_hex(8)
```
Reusable for the run-folder / `config_identity` timestamp fields if the planner wants one.

---

### `pinn/training/config.py` (EXTEND — config/model)

**Analog:** itself (existing frozen-dataclass idiom) + `pinn/runtime.py::RuntimeSpec`

**Frozen dataclass + fail-closed `__post_init__` idiom** (`pinn/training/config.py:78-92`, `210-227`):
```python
@dataclass(frozen=True)
class RunConfig:
    """Run-level knobs (seed, logging cadence). No precision/device."""

    seed: int = 0
    log_every: int = 1

    def __post_init__(self) -> None:
        if not isinstance(self.seed, int) or isinstance(self.seed, bool):
            raise ValueError(f"run.seed must be an int (got {self.seed!r})")
        if not isinstance(self.log_every, int) or self.log_every < 1:
            raise ValueError(
                f"run.log_every must be a positive int (got {self.log_every!r})"
            )
```
```python
@dataclass(frozen=True)
class LossConfig:
    """Loss-side caps. Enforces λ_E^max ≤ 1 (PHYS-05)."""

    lambda_e_max: float = 1.0

    def __post_init__(self) -> None:
        v = float(self.lambda_e_max)
        if not math.isfinite(v):
            raise ValueError(f"lambda_e_max must be finite (got {self.lambda_e_max!r})")
        ...
        object.__setattr__(self, "lambda_e_max", v)
```
CTX-50 adds `precision`/`device` fields to `RunConfig` (or a new section) following this exact idiom: raise `ValueError` naming the offending field, `object.__setattr__` to re-bind coerced values on a frozen dataclass. `RuntimeSpec` (`pinn/runtime.py:23-38`) is the sibling frozen-spec pattern CTX-50's docstring cites directly — same shape, no divergence needed.

**Existing required-field error type to extend, not duplicate** (`pinn/training/config.py:22-30`):
```python
class ConfigRequiredError(ValueError):
    """Raised when a CTX-39 config-required field is unset."""

    def __init__(self, field_name: str, provenance: str = "") -> None:
        self.field_name = field_name
        msg = f"TrainingConfig required field unset: {field_name}"
        if provenance:
            msg = f"{msg} ({provenance})"
        super().__init__(msg)
```
CTX-50's "typed error naming the offending path" for unknown/misspelled YAML keys should be a **sibling** exception (e.g. `ConfigKeyError` per RESEARCH.md Pattern 1), not a repurposing of `ConfigRequiredError` (that one is for *missing* required fields; the new one is for *unknown* keys) — keep the two failure modes distinguishable in tests.

---

### `pinn/training/config_yaml.py` (NEW — utility/mapper)

**Analog A (validation-against-known-fields idiom):** `pinn/training/config.py` (`dataclasses.fields` pattern used throughout `__post_init__`)

**Analog B (atomic frozen-copy write):** the `_atomic_write` idiom, verified identical in three places:
- `pinn/data/stage_scan.py:463-481`
- `pinn/data/splits.py:753-770`
- `pinn/verification/gradcheck_probe.py:51` (same shape)

```python
def _atomic_write(path: Path, content: str) -> None:
    temporary = path.with_name(path.name + f".tmp.{os.getpid()}")
    try:
        with open(temporary, "w", encoding="utf-8") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        directory_fd = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass
```
CTX-51's frozen-copy write (`runs/<name>/config.yaml`) should call this exact idiom with `yaml.safe_dump(...)` as the `content` argument, imported (not re-implemented) if the planner promotes `_atomic_write` to a shared helper — or copied verbatim per-module if the codebase's convention (three independent copies, one per module) is preserved instead. RESEARCH.md's "Don't Hand-Roll" table explicitly favors reuse.

**No direct analog for YAML parsing itself** — no `yaml.safe_load` call exists anywhere in `pinn/` today (confirmed by RESEARCH.md and this scan: PyYAML is a new import for this phase). The unknown-key fail-loud walk (RESEARCH.md Pattern 1, `dataclasses.fields(cls)` diff) is the closest available blueprint; there is no in-repo precedent to copy verbatim for the parse step itself.

---

### `pinn/training/checkpoint.py` (REPLACE naive impl — service/store)

**Analog:** itself (Protocol + naive impl to preserve the interface) + the `_atomic_write` idiom generalized to binary payloads

**`CheckpointStore` Protocol — DO NOT change this shape** (`pinn/training/checkpoint.py:27-41`):
```python
@runtime_checkable
class CheckpointStore(Protocol):
    """Narrow seam for Phase-41 swap (CTX-43)."""

    def save(self, state: Any) -> str:
        """Persist ``state``; return a checkpoint id."""
        ...

    def load_latest(self) -> Any:
        """Return the most recently saved well-formed state."""
        ...

    def rollback(self) -> Any:
        """Return the last well-formed saved state (RECOVER target)."""
        ...
```
`CurriculumController` (`pinn/training/controllers.py:797`, `824`, `849`, `911`, `925`, `938`) calls `checkpoint_store.save(...)` and `checkpoint_store.rollback()` exactly as shown below — the production store MUST keep this exact call surface so `controllers.py` needs **no signature changes**, only a richer payload underneath:
```python
self._checkpoint_store.save(self._checkpoint_payload(f"stage-{k}-final", k))
...
restored = self._checkpoint_store.rollback()
```

**Existing `weights_only=True` discipline to preserve at every load site** (`pinn/training/checkpoint.py:72-90`):
```python
def load_latest(self) -> Any:
    import torch
    if not self._ids:
        raise EmptyCheckpointStore(
            "load_latest on empty CheckpointStore (no successful save yet)"
        )
    path = self._root / f"{self._ids[-1]}.pt"
    return torch.load(path, weights_only=True)
```

**Atomic-write idiom to extend to binary `torch.save` payloads** (same three-site idiom as `config_yaml.py` above — `stage_scan.py:463-481`). The existing idiom writes `str` content; CTRL-03's production store needs a binary variant (`torch.save(payload, tmp)` in place of `handle.write(content)`, same `fsync`→`os.replace`→dir-`fsync` ordering) — this exact sequence was independently verified this research session (see RESEARCH.md "Code Examples" — full round-trip of all four RNG streams through `weights_only=True` succeeded with this ordering).

**`EmptyCheckpointStore` — reuse verbatim, do not redefine** (`pinn/training/checkpoint.py:23-24`):
```python
class EmptyCheckpointStore(RuntimeError):
    """Raised when load_latest/rollback is called with no successful save yet."""
```

---

### `pinn/training/resume.py` (NEW — service/validator)

**Analog (partial — sha256 canonicalization precedent):** `pinn/data/stage_scan.py::_split_file_evidence`

**Existing sha256 usage pattern in this codebase** (`pinn/data/stage_scan.py:495-504`):
```python
def _split_file_evidence(path: Path) -> dict[str, Any]:
    first = path.read_bytes()
    second = path.read_bytes()
    if first != second:
        raise RuntimeError("splits.json changed while recording byte identity")
    return {
        "sha256": hashlib.sha256(first).hexdigest(),
        "bytes": len(first),
        "byte_identity": True,
    }
```
This is byte-hashing (a file), not payload-canonicalization-then-hashing (a dict) — CTX-53's `config_identity` digest needs `json.dumps(payload, sort_keys=True, separators=(",", ":")) → hashlib.sha256(...).hexdigest()` (RESEARCH.md Pattern 2), which has no exact in-repo precedent but reuses the same `hashlib` import and hex-digest convention already established.

**Fail-closed refuse pattern to reuse** (`pinn/training/config.py` `ValueError` idiom, e.g. lines 136-140): the resume config-diff's "unclassified → refuse" and "identity field changed → refuse" paths should raise a typed error naming the offending field, following the exact `ConfigRequiredError`/bare-`ValueError` convention already established in `config.py` — do not introduce a third error-message shape.

**No direct in-repo analog for a multi-module identity payload** (RESEARCH.md Pattern 2 flags that identity fields span `config.py` AND `pinn/architecture_spec.py` AND `pinn/constants.py` — no existing function composes across these three modules). Build fresh per RESEARCH.md's `build_identity_payload`/`identity_digest` sketch; there is nothing to copy verbatim here beyond the `hashlib`/`json.dumps(sort_keys=True)` convention.

---

### `pinn/training/guards.py` (NEW — middleware/service, event-driven)

**Analog A (decision-machine shape):** `pinn/training/stage_exit.py::StageExitMachine`

**Duck-typed config + frozen-outcome-dataclass + three-way disposition idiom** (`pinn/training/stage_exit.py:38-52`, `128-149`):
```python
@dataclass(frozen=True)
class StageExitOutcome:
    """Result of one stage-exit poll.

    ``disposition is None`` means mid-flight / keep training
    (GAP-40-01 → B). The three enum members are the only exit decisions.
    Per-criterion diagnostics let callers log which gate clause failed.
    """

    disposition: Optional[StageDisposition]
    train_plateau: bool
    val_stable: bool
    phys_ok: bool
    energy_ok: bool


class StageExitMachine:
    """Four-criterion ADVANCE gate + RECOVER / HALT routing.

    Config is duck-typed: any object exposing ``beta``, ``patience``,
    ``eps_plateau``, ``eps_phys``, ``eps_energy``, ``max_epochs`` (and
    optionally ``stagnation_window``, ``energy_floor``) works.
    """

    def __init__(self, config) -> None:
        self._cfg = config

    def evaluate(self, ...) -> StageExitOutcome:
        # 1) NaN/Inf → RECOVER first (CTX-41), regardless of optimizer phase.
        if had_nan_inf:
            return StageExitOutcome(disposition=StageDisposition.RECOVER, ...)
        ...
```
`guards.py`'s per-step Tier-1/Tier-2 callback should follow this exact shape: a duck-typed config surface (thresholds read from config, never hardcoded — CTX-60/61's ⚖ placeholder requirement maps directly onto `stage_exit.py`'s "thresholds are read from an injected duck-typed config surface — never hardcoded here" docstring convention), a frozen outcome dataclass, and NaN/Inf checked first (mirroring `had_nan_inf` being checked before any other criterion).

**Analog B (fractional-threshold knob convention for the memory-watermark guard):** `pinn/data/adapter.py`

```python
MEMORY_WATERMARK_DEFAULT = 0.7
...
def _validate_adapter_config(capacity_bytes, memory_watermark, interim_s0, device):
    ...
    # memory_watermark: finite in (0, 1].
    if isinstance(memory_watermark, bool) or not isinstance(memory_watermark, (int, float)):
        raise ...(f"memory_watermark must be a finite float in (0, 1]; got {memory_watermark!r}")
    if not math.isfinite(memory_watermark) or not (0 < memory_watermark <= 1):
        raise ...(f"memory_watermark must be in (0, 1] and finite; got {memory_watermark!r}")
```
(`pinn/data/adapter.py:504`, `507-529`.) The disk-floor / memory-watermark Tier-2 guard's threshold should be validated with this exact finite-in-`(0, 1]` shape (a fraction of capacity), matching the project's one existing precedent for a watermark-style guard knob.

**Analog C (atomic write, for the `failure/` bundle):** the same `_atomic_write` idiom (`pinn/verification/gradcheck_probe.py:51-86` writes both `raw.json` and `summary.md` this way) — the Tier-A `trip.json`/`README.txt` and Tier-B `tail.log` files should each go through `_atomic_write`, consistent with how the verification probes already write their evidence bundles:
```python
_atomic_write(run_dir / "raw.json", json.dumps(raw, sort_keys=True, indent=2) + "\n")
...
_atomic_write(run_dir / "summary.md", summary)
```

---

### `pinn/training/determinism.py` (NEW — utility, transform/config)

**Analog A:** `pinn/runtime.py::resolve_runtime`

**Fail-closed, explicit-only resolution over an allowed set** (`pinn/runtime.py:65-95`):
```python
def resolve_runtime(precision, device):
    if precision is None or device is None:
        raise ValueError(
            f"resolve_runtime requires both precision and device; got "
            f"precision={precision!r}, device={device!r}. {_ALLOWED_PAIR_DESCRIPTION}"
        )
    factory = _ALLOWED_PROFILES.get((precision, device))
    if factory is None:
        raise ValueError(
            f"unsupported (precision, device) pair "
            f"({precision!r}, {device!r}); {_ALLOWED_PAIR_DESCRIPTION}."
        )
    return factory()
```
`strict_cpu_determinism`'s device-forcing at `pinn.train` startup should call `resolve_runtime("float64", "cpu")` directly (the existing escape-hatch pair) rather than inventing a third code path — CTX-63 already specifies this.

**Analog B (local-seeded-Generator discipline for the RNG-recording half):** `pinn/network.py::build_network`
```python
generator = torch.Generator(device=device)
generator.manual_seed(int(spec.seed))
```
(`pinn/network.py:253-254`.) This is the existing precedent for "a local seeded generator, never global state" — `determinism.py`'s RNG capture/restore helpers must follow the same discipline: `RunController._rng.bit_generator.state` (numpy), `torch.get_rng_state()`/`torch.mps.get_rng_state()`, `random.getstate()` are all captured/restored explicitly, never through `np.random.seed()`/legacy globals (confirmed via grep this session: no `np.random.seed(` call exists anywhere in `pinn/` outside the `strict_cpu_determinism` debug path itself, per RESEARCH.md Anti-Patterns).

---

### `pinn/training/controllers.py` (EXTEND — controller, event-driven/stateful loop)

**Analog:** itself — the existing `RunController.state_dict()`/`load_state_dict()` pair, and the sibling `state_dict`/`load_state_dict` idiom in `grad_clip.py`/`scheduled_weights.py`.

**Current composition to extend (NOT replace)** (`pinn/training/controllers.py:280-290`):
```python
def state_dict(self) -> dict[str, Any]:
    return {
        "model": self._model.state_dict(),
        "scheduled_weights": self._scheduled_weights.state_dict(),
        "clipper": self._grad_clipper.state_dict(),
    }

def load_state_dict(self, state: dict[str, Any]) -> None:
    self._model.load_state_dict(state["model"])
    self._scheduled_weights.load_state_dict(state["scheduled_weights"])
    self._grad_clipper.load_state_dict(state["clipper"])
```
Add `"optimizer"` and `"rng"` keys following this exact plain-dict shape (RESEARCH.md Pattern 4 gives the precise diff). The `self._rng` attribute already exists (`controllers.py:273`: `self._rng = rng if rng is not None else np.random.default_rng(config.run.seed)`) — expose `self._rng.bit_generator.state`, do not construct a second RNG.

**Sibling `state_dict`/`load_state_dict` idiom to match exactly (plain-python-scalar payloads, weights_only-clean)** — `pinn/training/scheduled_weights.py:246-271`:
```python
def state_dict(self) -> dict[str, Any]:
    """Serialize schedule state into a plain dict of python scalars."""
    return {
        "n_adam_k": self._n_adam_k,
        "warmup_length": self._warmup_length,
        ...
        "frozen": self._frozen,
        "frozen_ramp": self._frozen_ramp,
        "last_epoch": self._last_epoch,
    }

def load_state_dict(self, state: dict[str, Any]) -> None:
    """Restore schedule state from a ``state_dict()`` dict (round-trip)."""
    self._n_adam_k = int(state["n_adam_k"])
    ...
```
And `grad_clip.py:292-344` for the same pattern with a dtype-string closed-map guard (`_DTYPE_TO_NAME`/`_NAME_TO_DTYPE`) — useful precedent if the optimizer `state_dict()` needs any non-tensor coercion.

**Missing per-step hook — the central architectural gap this phase must close** (`pinn/training/controllers.py:479-522`, `610-650`): `_run_adam_phase`/`_run_lbfgs_phase` run to completion with no external call site; `optimizer` is a local variable in `run_stage`, never stored on `self`. Add:
```python
# Inside _run_adam_phase / _run_lbfgs_phase, after each epoch/iteration:
#     self._optimizer = optimizer          # NEW — expose the live optimizer
#     if self._checkpoint_hook is not None:
#         self._checkpoint_hook(global_step)   # NEW — dual-trigger cadence check lives in the hook
```
This is Task-level scope, not a `checkpoint.py`-only change — see RESEARCH.md Architecture Patterns Pattern 4 for the full rationale.

---

### Test files

**`tests/phase41/__init__.py`, `tests/phase41/_fixtures.py`, `tests/phase41/test_prohibitions.py`** — copy the Phase-40 originals near-verbatim, updating only the phase number and skip phrase:

`tests/phase40/__init__.py` (full file, 35 lines):
```python
_SKIP_PHRASE = "skipped Phase40 production symbol"
__all__ = ["_SKIP_PHRASE"]
```
→ `tests/phase41/__init__.py` sets `_SKIP_PHRASE = "skipped Phase41 production symbol"`.

`tests/phase40/test_prohibitions.py:58-66` — the deferred-import skip-guard helper to reuse verbatim (or import directly if promoted to a shared test-utility module):
```python
def _require(symbol, module):
    """Per-symbol deferred import — SkipTest (never ERROR) until it lands."""
    try:
        mod = importlib.import_module(module)
    except ImportError:
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {module}.{symbol}")
    if not hasattr(mod, symbol):
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {module}.{symbol}")
    return getattr(mod, symbol)
```

`tests/phase40/_fixtures.py` — `make_stub_source`/`make_stub_split_sources`/`make_stub_model` (lines 132-177) extend directly (import from `tests.phase40._fixtures` or copy-adapt into `tests/phase41/_fixtures.py` per RESEARCH.md's "extend rather than duplicate" guidance); add a stub clock/step-counter fixture for the dual-trigger cadence tests (CTRL-02) and a tiny synthetic Stage-0 loop wrapper for the end-to-end resume/guard tests (CTRL-05/07).

**`tests/phase41/test_config_yaml.py`** — analog `tests/phase40/test_config.py` (full file read). Reuse:
- The `_require(...)` module-level binding block (lines 14-21).
- The `RequiredFieldTests`/`ValidationTests`/`ConstructionTests` class split (lines 43-172) as the structural template — add a `YamlMappingTests` class for CTRL-01's "keyed YAML resolves to `TrainingConfig`; unknown key fails loud; frozen copy re-parses equal" acceptance criteria.
- The `assertRaises(...) as ctx: ... self.assertIn(name, str(ctx.exception))` idiom (lines 44-52) for asserting the typed error names the offending dotted path.

**`tests/phase41/test_checkpoint.py`** — analog `tests/phase40/test_checkpoint.py` (full file, 137 lines). Reuse the four-class structure: `ProtocolShapeTests` (protocol-member presence), `RoundTripTests` (save→load_latest round trip with nested tensors), `EmptyStoreTests` (`EmptyCheckpointStore` on an empty store), and especially the `WeightsOnlyAndPayloadTests.test_load_path_uses_weights_only` source-introspection idiom (lines 94-99):
```python
def test_load_path_uses_weights_only(self):
    src = inspect.getsource(TorchSaveCheckpointStore)
    self.assertIn("weights_only=True", src)
    # Every torch.load call must pass the flag.
    self.assertEqual(src.count("torch.load"), src.count("weights_only=True"))
```
This exact assertion (counting `torch.load` call sites against `weights_only=True` occurrences) is the CTRL-03 "no `weights_only=False` escape hatch" prohibition test — copy verbatim against the new production `CheckpointStore` class name. Add new classes for dual-trigger cadence (CTRL-02), atomicity/fault-injection (CTRL-03, monkeypatch `os.replace`), and retention (rolling-3/best/latest/anchor).

**`tests/phase41/test_guards.py`** — analog `tests/phase40/test_stage_exit.py` (class list: `EnumShapeTests`, `AdvanceGateTests`, `RecoverTests`, `HaltAndMidFlightTests`, `StagnationWindowHaltTests`, `PlateauSmootherMechanismTests`, `SignatureAndConfigInjectionTests`). Mirror the per-criterion class-per-guard-family split (one class per guard: NaN/Inf, loss-explosion, disk-floor, memory-watermark) and the "config is duck-typed, thresholds injected" `SignatureAndConfigInjectionTests` pattern for asserting guard thresholds are config-read, not hardcoded.

**`tests/phase41/test_train_entrypoint.py`** — analog `tests/phase39/test_stage_scan.py::StageScanCliContract` (lines 373-421):
```python
class StageScanCliContract(unittest.TestCase):
    def setUp(self):
        self.main = _require("main")

    def _run(self, source, run_dir, *extra):
        adapter_factory = mock.Mock(return_value=source)
        stdout = io.StringIO()
        with mock.patch(
            "pinn.data.stage_scan.AdmittedSetAdapter",
            adapter_factory,
        ), mock.patch("sys.stdout", new=stdout):
            exit_code = self.main(["--run-dir", str(run_dir), *extra])
        return exit_code, stdout.getvalue(), adapter_factory

    def test_cli_full_pass_writes_manifest_report_and_hash_log(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            ...
            exit_code, stdout, _factory = self._run(source, run_dir)
            report = json.loads((run_dir / "stage_population.json").read_text())
            ...
        self.assertEqual(exit_code, 0)
```
This is the exact "invoke `main(argv_list)` directly, mock the heavy collaborator, assert exit code + on-disk artifacts" shape `test_train_entrypoint.py` needs for CTRL-01/02/05/08: mock `build_network`/the data sources, call `main(["--config", str(cfg_path), "--resume", str(ckpt_path)])`, and assert `runs/<name>/config.yaml`, `checkpoints/*.pt`, and `curriculum.jsonl` land correctly and the exit code is 0 (or the typed-error path for a missing `--resume`).

**`tests/phase41/test_resume.py`, `tests/phase41/test_determinism.py`** — no direct structural analog exists (no resume-diff or RNG-determinism test precedent anywhere in `tests/phase37-40`). Use `tests/phase40/test_config.py`'s `assertRaises(...) as ctx: ...; self.assertIn(name, str(ctx.exception))` idiom for the fail-safe-refuse assertions (test_resume.py) and its `ValidationTests`-style flag-assertion idiom for the `strict_cpu_determinism` off-by-default / forces-CPU assertions (test_determinism.py). Flagged below under "No Analog Found."

## Shared Patterns

### Atomic file write (tmp → fsync → os.replace → dir-fsync)
**Source:** `pinn/data/stage_scan.py:463-481` (identical in `pinn/data/splits.py:753-770`, `pinn/verification/gradcheck_probe.py:51`, `residual_probe.py:53`, `overfit_probe.py:88`)
**Apply to:** `config_yaml.py` (frozen `config.yaml` write), `checkpoint.py` (every `.pt` write, generalized to binary payloads), `guards.py` (`failure/` bundle: `README.txt`, `trip.json`, `tail.log`), and the `curriculum.jsonl` append (RESEARCH.md Pattern 3 uses a single-`write()`-then-`fsync()` variant of the same discipline for the append-only case).
```python
def _atomic_write(path: Path, content: str) -> None:
    temporary = path.with_name(path.name + f".tmp.{os.getpid()}")
    try:
        with open(temporary, "w", encoding="utf-8") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        directory_fd = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass
```

### `weights_only=True` at every `torch.load` call site
**Source:** `pinn/training/checkpoint.py:72-90` (both existing load sites)
**Apply to:** `checkpoint.py`'s production load, fallback-scan candidates, and any `--resume` path in `pinn/train.py`. Verify with the `inspect.getsource(...)` count-matching idiom from `tests/phase40/test_checkpoint.py:94-99`.

### Frozen dataclass + fail-closed `__post_init__` (raise `ValueError` naming the offending field; `object.__setattr__` to re-bind coerced values)
**Source:** `pinn/training/config.py` (all four section dataclasses), `pinn/runtime.py::RuntimeSpec`, `pinn/architecture_spec.py::ArchitectureSpec`
**Apply to:** every new/extended dataclass in `config.py` and `config_yaml.py`'s YAML→dataclass mapper.

### `state_dict()`/`load_state_dict()` — plain-python-scalar/tensor payloads, weights_only-clean
**Source:** `pinn/training/scheduled_weights.py:246-271`, `pinn/training/grad_clip.py:292-344`, `pinn/training/controllers.py:280-290`
**Apply to:** the extended `RunController.state_dict()` (optimizer + rng keys) and the overall `CheckpointStore` payload composition (CTX-53).

### Duck-typed config surface + frozen outcome dataclass + thresholds-never-hardcoded
**Source:** `pinn/training/stage_exit.py::StageExitMachine`/`StageExitOutcome`
**Apply to:** `guards.py`'s Tier-1/Tier-2 guard callback and its outcome type.

### `hashlib.sha256` + `json.dumps(..., sort_keys=True)` canonicalization
**Source:** `pinn/data/stage_scan.py:495-504` (`_split_file_evidence`; file-bytes hashing) — extend to payload-canonicalization for `resume.py`'s `config_identity` digest (dict, not file bytes; see RESEARCH.md Pattern 2 for the exact composition).
**Apply to:** `resume.py`, and `config_yaml.py`/`checkpoint.py` wherever `config_identity` is computed or compared.

## No Analog Found

| File | Role | Data Flow | Reason |
|---|---|---|---|
| `pinn/training/resume.py` (YAML/identity-digest composition across `config.py` + `architecture_spec.py` + `constants.py`) | service | transform | No existing function in the codebase composes an identity payload spanning three separate modules; nearest precedent (`_split_file_evidence`) hashes file bytes, not a canonicalized multi-module dict. Use RESEARCH.md Pattern 2's `build_identity_payload`/`identity_digest` sketch directly. |
| `tests/phase41/test_resume.py` (config-diff refuse/allow test structure) | test | n/a | No resume/rollback/config-diff test precedent exists in `tests/phase37-40`; compose from `test_config.py`'s `assertRaises` idiom (fail-safe-refuse assertions) — no full-class template to copy. |
| `tests/phase41/test_determinism.py` (RNG-stream + strict-CPU-switch test structure) | test | n/a | No RNG-capture/determinism-switch test precedent exists; the only RNG discipline precedent (`_fixtures.py`'s explicit-Generator convention) tests *usage*, not *capture/restore*. Build fresh per RESEARCH.md's verified round-trip code example. |
| YAML parsing itself (`yaml.safe_load` call + unknown-key walk) inside `config_yaml.py` | utility | transform | `pinn/` has never imported PyYAML before this phase (confirmed via RESEARCH.md and this scan); no in-repo YAML-parsing function exists to copy. Use RESEARCH.md Pattern 1's `_map_section` sketch (verified against the actual dataclass shapes) as the starting point. |

## Metadata

**Analog search scope:** `pinn/training/` (all 8 files), `pinn/` top-level (`runtime.py`, `architecture_spec.py`, `constants.py`, `network.py`), `pinn/data/` (`stage_scan.py`, `splits.py`, `adapter.py`), `pinn/verification/` (`gradcheck_probe.py`, `residual_probe.py`, `overfit_probe.py` — atomic-write idiom cross-check), `tests/phase37-40/`, `tests/phase39/test_stage_scan.py` (CLI-contract precedent).
**Files scanned (read in full or targeted):** 21 production/test files, ~7,800 lines scanned via `wc -l` + targeted `grep`/`Read` (no file re-read; large files — `controllers.py` 990 lines, `stage_scan.py` 716 lines, `adapter.py` 1091 lines, `test_controllers.py` 900 lines — read via non-overlapping `grep`-located ranges only).
**Pattern extraction date:** 2026-07-18
