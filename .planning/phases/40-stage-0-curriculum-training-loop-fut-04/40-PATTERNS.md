# Phase 40: Stage-0 Curriculum Training Loop (FUT-04) - Pattern Map

**Mapped:** 2026-07-17
**Files analyzed:** 19 (9 production `pinn/training/*` modules + 10 `tests/phase40/*` files)
**Analogs found:** 18 / 19 (1 file — `checkpoint.py` — has no direct codebase precedent; nearest structural analog noted below)

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|---|---|---|---|---|
| `pinn/training/__init__.py` | config (package marker/barrel) | N/A (module wiring) | `pinn/data/__init__.py` | exact |
| `pinn/training/config.py` | config | transform (construction-time validation) | `pinn/architecture_spec.py` + `pinn/runtime.py` | exact |
| `pinn/training/controllers.py` (`CurriculumController`, `RunController`) | controller | event-driven (outer/inner loop) | `pinn/data/admission.py` (dispatch shape) + `pinn/verification/overfit_probe.py` (Adam loop shape) | role-match (composite) |
| `pinn/training/scheduled_weights.py` | service (PHYS-05 schedule) | transform | `pinn/loss_catalog.py` | exact |
| `pinn/training/collocation_sampler.py` | service | CRUD (sampling) | `pinn/data/batches.py` | exact |
| `pinn/training/grad_clip.py` | utility | transform | `pinn/data/admission.py` (pure-function + typed-outcome shape) | partial |
| `pinn/training/stage_exit.py` | controller (state machine) | event-driven | `pinn/data/admission.py` | exact |
| `pinn/training/slbfgs_preflight.py` | utility (typed refusal) | request-response | `pinn/data/stages.py` + `pinn/data/types.py` (`StageZeroUnderpopulated`) | exact |
| `pinn/training/checkpoint.py` (`CheckpointStore` protocol + naive impl) | service | file-I/O | none exact — nearest structural precedent `pinn/runtime.py` (frozen resolver-as-seam) | no analog (flagged) |
| `tests/phase40/__init__.py` | test | N/A | `tests/phase39/__init__.py` | exact |
| `tests/phase40/_fixtures.py` | test (fixture builder) | N/A | `tests/phase39/test_batches.py` `_Query`/`_DataQuery` stub classes | role-match |
| `tests/phase40/test_controllers.py` | test | event-driven | `tests/phase39/test_admission.py` (dispatch tests) + deferred-import pattern | role-match |
| `tests/phase40/test_optimizer_phase.py` | test | event-driven | `tests/phase38/test_overfit_probe.py` (Adam-loop exercise/spy pattern) | role-match |
| `tests/phase40/test_scheduled_weights.py` | test | transform | `tests/phase38/test_loss_catalog.py` | exact |
| `tests/phase40/test_collocation_sampler.py` | test | CRUD | `tests/phase39/test_batches.py` | exact |
| `tests/phase40/test_grad_clip.py` | test | transform | `tests/phase39/test_admission.py` (`ConservationBoundaryTests`) | role-match |
| `tests/phase40/test_stage_exit.py` | test | event-driven | `tests/phase39/test_admission.py` | exact |
| `tests/phase40/test_slbfgs_preflight.py` | test | request-response | `tests/phase39/test_batches.py` typed-exception assertions (`StageZeroUnderpopulated`) | role-match |
| `tests/phase40/test_prohibitions.py` | test | N/A (mechanical audit) | `tests/phase39/test_prohibitions.py` | exact |

## Pattern Assignments

### `pinn/training/__init__.py` (config, N/A)

**Analog:** `pinn/data/__init__.py` (whole file, 65 lines) and `pinn/verification/__init__.py` (whole file, 21 lines)

**Minimal barrel + explicit public-surface docstring** (`pinn/data/__init__.py:1-22`):
```python
"""Phase 39 data-ingestion package (v2.0 BUILD milestone, FUT-01).
...
Public surface (39-PATTERNS.md ``pinn/data/__init__.py`` assignment, mirroring
the minimal ``pinn/verification/__init__.py`` analog): the Plan-02 frozen shared
contracts plus the production ``AdmittedSetAdapter``. Parser helpers
(``parse_brutus_text``/``parse_footer``/...) are intentionally NOT re-exported —
they belong to the adapter's internal ingestion surface.

Importing this package (or any submodule) binds these names but performs NO
corpus discovery and NO adapter initialization...
"""

from pinn.data.adapter import (
    AdmittedSetAdapter,
    EvidenceRedactionError,
)
from pinn.data.types import (
    AdmittedRecord, DataFidelityPoints, ... StageQuery, StageZeroUnderpopulated, Variant,
)

__all__ = [ ... ]
```

**On-demand (heavy) submodule deferral** (`pinn/verification/__init__.py:1-21`): only the lightweight `componentwise_ad` is re-exported at package-import time; the Torch-heavy rung modules (`fixture_loader`, probes) are imported on demand by callers, not by `__init__`. Apply the same discipline to `pinn/training/__init__.py`: export `TrainingConfig`, `CurriculumController`, `RunController`, `CheckpointStore` (the Phase-41 seam types) but do NOT force-import anything that pulls in a full model/dataset at package-import time.

---

### `pinn/training/config.py` (config, transform)

**Analog:** `pinn/architecture_spec.py:35-141` (`ArchitectureSpec`) and `pinn/runtime.py:23-96` (`RuntimeSpec` + `resolve_runtime`)

**Frozen dataclass + fail-closed `__post_init__`** (`pinn/architecture_spec.py:35-70`):
```python
@dataclass(frozen=True)
class ArchitectureSpec:
    """Immutable, validated SQR-SkipResNet-SIREN topology specification. ..."""
    input_dim: int = 14
    output_dim: int = 9
    hidden_depth: int = 12
    ...
    seed: int = _DEFAULT_SEED

    def __post_init__(self) -> None:
        """Fail-closed validation — raise before any downstream build."""
        if self.input_dim != 14:
            raise ValueError(
                f"ArchitectureSpec.input_dim must be 14 (got {self.input_dim!r}); "
                "locked topology is 14 → 256×12 → 9 (pinn_architecture.md §2.3/§2.4)"
            )
        ...
```
Every raise names the offending field and cites the spec section — carry this discipline into `TrainingConfig`'s nested dataclasses (`run`/`stage`/`opt`/`loss` sections per CTX-42), including the CTX-39 config-required fields (`MAX_EPOCHS`, stagnation window, percentile-10 relaxation, `T_max = N_Adam,k`) that must raise at construction if unset rather than defaulting.

**Nested immutable resolver with a fixed allowed-set + descriptive error** (`pinn/runtime.py:23-96`, full file): `RuntimeSpec` is the frozen output type; `resolve_runtime` validates a mandatory-both-arguments contract and raises `ValueError` naming the two allowed pairs before any tensor is built. `TrainingConfig`'s per-section validation should follow the same "reject before any downstream build, name the allowed set" idiom, and per CTX-42 must NOT itself parse YAML or carry a precision/device field (that stays in `resolve_runtime`).

---

### `pinn/training/controllers.py` (`CurriculumController` / `RunController`) (controller, event-driven)

**Analog 1 — multi-criterion dispatch → typed disposition:** `pinn/data/admission.py:106-240` (`AdmissionOutcome` + `evaluate_admission`)

```python
@dataclass
class AdmissionOutcome:
    disposition: str          # "admit" | "reject" | "quarantine"
    reasons: tuple = field(default_factory=tuple)
    warnings: tuple = field(default_factory=tuple)
    dropped_samples: int = 0
    eps_H: Any = None
    scs: Any = None
    grade: Any = None
    marginal: bool = False


def _reject(reasons, dropped_samples=0):
    return AdmissionOutcome(disposition="reject", reasons=tuple(reasons),
                             dropped_samples=dropped_samples)


def _quarantine(reasons, dropped_samples=0):
    return AdmissionOutcome(disposition="quarantine", reasons=tuple(reasons),
                             dropped_samples=dropped_samples)


def evaluate_admission(parsed, *, blacklist=frozenset(), ...):
    """Evaluate all seven Step-1A clauses over one parsed float64 trajectory. ..."""
    # Clause 1: identity & blacklist (fail-closed exclusion).
    if physical_key in blacklist:
        return _reject(("blacklisted",))
    # Clause 2: ...
    ...
    return AdmissionOutcome(disposition="admit", reasons=(), ...)
```
This is the strongest analog in the codebase for `StageExitMachine`'s ADVANCE/RECOVER/HALT evaluator: a pure function that walks clauses **in a fixed, documented order**, short-circuits to a typed outcome constructor as soon as a clause fires, and returns one immutable disposition object carrying every diagnostic (`eps_H`, `scs`, `grade`) needed by the caller/logger. `CurriculumController`'s dispatch loop (`match disposition: ADVANCE -> ...; RECOVER -> ...; HALT -> ...`) should mirror `evaluate_admission`'s "one evaluator function, one typed result, caller dispatches on `.disposition`" shape rather than an ad hoc if/elif chain scattered through the loop body.

**Analog 2 — Adam training-loop shape + explicit fail-loud diagnostics:** `pinn/verification/overfit_probe.py:288-407` (`run_overfit`)

```python
# pinn/verification/overfit_probe.py:326-371
model = build_network(ArchitectureSpec(), dtype=dtype, device=torch_device)
optimizer = torch.optim.Adam(model.parameters(), lr=lr)

def data_loss_value():
    tau_ic13 = _build_tau_ic13(u_points, dtype=dtype, device=torch_device)
    pred = model(tau_ic13, masses).reshape(-1, _N_BODIES, _N_DIMS)
    return data_huber_loss(pred, true_pos, dtype=dtype, device=torch_device)

...
model.train()
loss0 = data_loss_value()
if not bool(torch.isfinite(loss0).all()):
    raise OverfitFail("non_finite_data_loss", step=0)
l0 = float(loss0.detach().cpu())
...
for step in range(1, int(max_steps) + 1):
    optimizer.zero_grad(set_to_none=True)
    loss = data_loss_value()
    if not bool(torch.isfinite(loss).all()):
        raise OverfitFail("non_finite_data_loss", step=step)
    loss.backward()
    optimizer.step()
    ...
```
This is the only existing training loop in the codebase using `torch.optim.Adam` + `model.train()`/`.eval()` toggling + `zero_grad(set_to_none=True)` + a fail-loud `isfinite` check on every step before `optimizer.step()`. `RunController`'s Phase-2a Adam loop should reuse this exact step ordering (`zero_grad` → forward → finite-check → `backward()` → clip → `optimizer.step()` → `scheduler.step()`), and its typed failure class (`OverfitFail` at `pinn/verification/overfit_probe.py:70-76`) is the direct precedent for how a training-loop-local typed exception carries `reason` + arbitrary `**fields`.

**Analog 3 — the exact call surface `RunController` consumes each epoch:** `pinn/data/batches.py:355-390` (`build_stage_batch`)
```python
def build_stage_batch(source, *, stage: int, rng: np.random.Generator, dtype, device,
                       collocation_count: int = 4096) -> FixedBatch:
    """Build one DATA-05 fixed batch without owning epochs or adaptive density."""
    selected = select_stage_records(source, stage=stage, rng=rng)
    ...
    return FixedBatch(data_points=data_points, collocation_points=collocation_points,
                       replay_keys=selected.replay, lookahead_keys=selected.lookahead)
```
Call this unchanged, once per epoch with a freshly-advanced seeded RNG (DATA-04 per-epoch shuffle — not Phase-40 discretion per CTX's "Claude's Discretion" carve-out).

---

### `pinn/training/scheduled_weights.py` (service, transform)

**Analog:** `pinn/loss_catalog.py:64-101` (`LossWeights`) and `:299-327` (`compose_total`)

```python
@dataclass(frozen=True)
class LossWeights:
    """Five-field named λ container matching Phase 40's PHYS-05 weight vector.
    ``lambda_data`` is FIXED at 1.0 by §3.1 ..."""
    lambda_data: float = 1.0
    lambda_ic: float = 1.0
    lambda_phys: float = 1.0
    lambda_e: float = 1.0
    lambda_l: float = 1.0

    def __post_init__(self) -> None:
        fields = (("lambda_data", self.lambda_data), ...)
        for name, value in fields:
            try:
                finite = math.isfinite(float(value))
            except (TypeError, ValueError):
                finite = False
            if not finite or float(value) < 0.0:
                raise ValueError(
                    f"LossWeights.{name} must be finite and non-negative; "
                    f"got {value!r} (a negative lambda silently flips the term "
                    f"into gradient ascent)"
                )
```
`LossWeights` (which the docstring literally says was "built FOR this phase") is the *container* `ScheduledWeights.current(epoch)` must emit each step; do not redefine a parallel weight type. `compose_total(terms, weights)` (`pinn/loss_catalog.py:299-327`) is a **pure function of a supplied weights value** — the same purity discipline (no internal scheduling/warmup state) should shape `ScheduledWeights`: it owns the warmup/λ^max/freeze/re-warm *state machine*, but each `current(epoch)` call returns a fresh, already-validated `LossWeights` instance that `compose_total` consumes unchanged.

---

### `pinn/training/collocation_sampler.py` (service, CRUD/sampling)

**Analog:** `pinn/data/batches.py:289-352` (`sample_collocation_points`) and `:33-36` (`_require_local_rng`)

**Caller-owned RNG discipline** (`pinn/data/batches.py:33-36`):
```python
def _require_local_rng(rng) -> np.random.Generator:
    if not isinstance(rng, np.random.Generator):
        raise TypeError("rng must be a caller-owned numpy.random.Generator")
    return rng
```

**Uniform sampling + validated identities** (`pinn/data/batches.py:289-330`):
```python
def sample_collocation_points(source, record_keys, *, rng, dtype, device,
                               collocation_count: int = 4096) -> PhysicsCollocationPoints:
    rng = _require_local_rng(rng)
    if collocation_count <= 0:
        raise ValueError("collocation_count must be positive")
    per_slot_quotas = allocate_collocation_quota(len(record_keys), collocation_count, rng)
    assigned: list[tuple[RecordKey, float]] = []
    for key, per_slot_count in zip(record_keys, per_slot_quotas):
        if not isinstance(key, RecordKey):
            raise TypeError(f"collocation member must be RecordKey; got {key!r}")
        ...
        for value in rng.uniform(0.0, T_CHARACTERISTIC_TIME, size=per_slot_count):
            assigned.append((key, float(value)))
```
The **uniform** collocation mode (TRAIN-04) should reuse this exact `rng.uniform(0.0, T_CHARACTERISTIC_TIME, size=...)` idiom and caller-owned-RNG type check. For the **adaptive** `(model, last_residuals)` hook, follow the same fail-closed validation-before-sampling ordering this module uses throughout (validate pool → validate counts → sample → validate result), but there is no existing adaptive-density precedent in the codebase (RESEARCH.md Assumption A4 — internal algorithm is genuinely open, low risk since the AC only tests the hook signature/count/bounds).

---

### `pinn/training/grad_clip.py` (utility, transform)

**Analog:** `pinn/data/admission.py:46-73` (`ConservationOutcome` + `evaluate_conservation`) for the "pure function returning a small typed numeric outcome" shape:
```python
@dataclass(frozen=True)
class ConservationOutcome:
    rejected: bool
    marginal: bool
    grade: str
    scs: float
    eps_H: float


def evaluate_conservation(eps_H: float) -> ConservationOutcome:
    """SCS = log10(eps_H). Reject only ``SCS > -5``; ..."""
    if eps_H == 0.0:
        return ConservationOutcome(rejected=False, marginal=False, grade="Excellent",
                                    scs=-math.inf, eps_H=0.0)
    scs = math.log10(eps_H)
    rejected = scs > -5.0
    ...
```
No codebase module wraps `torch.nn.utils.clip_grad_norm_` yet; RESEARCH.md's Pattern 2 (verified against PyTorch 2.12 docs) is the authoritative source for the formula itself:
```python
# RESEARCH.md "Pattern 2" — pinn_architecture.md §4.4 Listing 6 (normative) + context7-verified API
total_norm = torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=float("inf"))
grad_history.append(total_norm.detach())
if len(grad_history) > 100:
    grad_history.pop(0)
clip_value = C_stage * torch.median(torch.stack(grad_history))
torch.nn.utils.clip_grad_norm_(model.parameters(), clip_value)
```
Combine: a small frozen result type (`ConservationOutcome`-style) carrying `clip_value`/`total_norm`/`window_len`, produced by a pure function, called by `controllers.py` only during the Adam phase. **Use `torch.median`, never `numpy.median`/`statistics.median`** — see Common Pitfall 1 in RESEARCH.md; this is load-bearing for the CTX-35 partial-window bootstrap test.

---

### `pinn/training/stage_exit.py` (controller/state machine, event-driven)

**Analog:** `pinn/data/admission.py:106-240` (full file section) — same citation as Controllers Analog 1 above; this is the file's primary and strongest home. Reread emphasis: the seven-clause `evaluate_admission` fixes ONE evaluation order, returns EARLY on the first disqualifying clause, and only reaches the "admit" (here: ADVANCE) path after every gate passes — directly mirroring CURR-03's four-criterion conjunction (`β-smoothed plateau`, `ε_phys`, `ε_energy` with floor, patience) where ALL FOUR must hold simultaneously for ADVANCE, any NaN/Inf routes to RECOVER regardless of which phase produced it (Adam or L-BFGS, per CTX-41), and exhausting the criteria without an ADVANCE never silently falls through to advancement (TRAIN-06 "no fallback advancement" — mirrors `evaluate_admission` never defaulting to `"admit"` when a clause is ambiguous).

**Test-pattern analog** for the *boundary* tests (SCS `-5` marginal-but-admitted edge, `eps_H == 0` Excellent edge): `tests/phase39/test_admission.py:37-60` (`ConservationBoundaryTests`) — the same "evaluate the pure function at the exact boundary value, assert the documented tie-break" style applies directly to CURR-03's `ε_plateau`/`ε_phys`/`ε_energy` boundary tests and CTX-35's partial-window backstop.

---

### `pinn/training/slbfgs_preflight.py` (utility/typed refusal, request-response)

**Analog 1 — small, single-purpose predicate module:** `pinn/data/stages.py` (whole file, 87 lines):
```python
def classify_stage_label(record: Any, interim_s0: float = 0.01) -> StageLabel:
    """Classify one admitted record's CTL Stage-0/1 membership. ..."""
    if record.variant != Variant.HIERARCHICAL or record.fidelity != Fidelity.BASE:
        return StageLabel.UNASSIGNED
    ...
```
`slbfgs_preflight.py`'s `check_stage_preflight(stage)` should be exactly this shape: one small function, one closed set of outcomes, heavily-commented authoritative-membership docstring citing the spec line range it transcribes (mirrors `pinn/data/stages.py:1-24`'s docstring discipline).

**Analog 2 — typed sentinel exception carrying diagnostic fields:** `pinn/data/types.py:165-177` (`StageZeroUnderpopulated`):
```python
class StageZeroUnderpopulated(Exception):
    """Typed fatal-class signal: admitted Stage-0 population below ``threshold``.

    Carries the fixed batch minimum (``threshold == 240``) and the observed
    Stage-0 count so the scan report and CLI exit are self-describing.
    """

    def __init__(self, observed: int, threshold: int = 240) -> None:
        self.observed = observed
        self.threshold = threshold
        super().__init__(
            f"Stage-0 population {observed} < required {threshold}"
        )
```
RESEARCH.md's Code Examples section already drafts `StochasticLBFGSNotImplemented` in this exact shape (constructor stores `self.stage`, message cites the deferred-PLAT-02 rationale) — copy that draft, not a bare `raise ValueError(...)`, so `test_slbfgs_preflight.py` can assert on `.stage` the same way `tests/phase39` asserts on `.observed`/`.threshold`.

---

### `pinn/training/checkpoint.py` (`CheckpointStore` protocol + naive impl) (service, file-I/O)

**No direct analog exists.** Grep confirms zero uses of `state_dict`/`torch.save`/`torch.load` and zero uses of `typing.Protocol` anywhere in `pinn/` today (the one class named `TimingProtocol` in `pinn/verification/componentwise_ad.py:98` is a plain frozen dataclass, not a `typing.Protocol`). Nearest structural precedent is the **frozen-value-as-seam** discipline of `pinn/runtime.py:23-96`: one small, explicit, dependency-free module that names its contract precisely and is the SOLE place a particular capability is resolved — `CheckpointStore` should follow the same "narrow seam, explicit args, no availability probing" spirit, using stdlib `typing.Protocol` (zero new dependency) for the interface and a deliberately minimal `torch.save`/`torch.load` pair for the naive implementation. CTX-44's `state_dict()`/`load_state_dict()` composition requirement is testable against `tests/phase38/test_network_structure.py:216-232`'s existing `state_dict()` equality assertions (`m1.state_dict()` / `m2.state_dict()` compared key-by-key) — reuse that comparison idiom for the nested multi-component checkpoint dict.

---

### `tests/phase40/__init__.py` (test, N/A)

**Analog:** `tests/phase39/__init__.py` (whole file, 37 lines):
```python
# The SOLE definition of the deferred-skip phrase. Imported by every localized
# ``_require`` helper in this package; never re-spelled independently (the
# Wave-5 grep in task 39-07-01 keys on this exact literal).
_SKIP_PHRASE = "skipped Phase39 production symbol"

__all__ = ["_SKIP_PHRASE"]
```
Define `_SKIP_PHRASE = "skipped Phase40 production symbol"` here once; every `tests/phase40/test_*.py` file's local `_require`/`_import_symbol` helper imports this single constant so a final grep can detect any remaining skip without phrase drift (same discipline Phase 39 used).

---

### `tests/phase40/_fixtures.py` (test fixture, N/A)

**Analog:** `tests/phase39/test_batches.py:114-161` (`_Query`) and `:256-279` (`_DataQuery`):
```python
class _Query:
    """A minimal StageQuery over persisted base Set-1a labels."""
    def __init__(self, RecordKey, StageLabel, n_stage0=300, n_stage1=20,
                 blacklisted=(), inject_gold=False, inject_standard=False,
                 gold_numeric_stage_count=0):
        ...
    @property
    def blacklisted_physical_keys(self): ...
    def has_stage(self, k): ...
    def records_at(self, k): ...
    def records_at_or_below(self, k): ...
    def stage_label(self, key): ...
    def is_blacklisted(self, key): ...


class _DataQuery(_Query):
    """A StageQuery that also serves per-record trajectory data for assembly."""
    def record_keys(self): ...
    def get(self, key):
        return SimpleNamespace(record_key=key, physical_key=key.physical_key,
                                stage_label=self.stage_label(key),
                                n_snapshots=self.n_snapshots(key),
                                ic13=np.linspace(0.0, 1.2, 13, dtype=np.float64) + key.id / 10000.0,
                                masses=np.array([1.0 + key.id / 10000.0, 2.0, 3.0], dtype=np.float64))
    def n_snapshots(self, key): return 32
    def snapshot_times(self, key): ...
```
This `SimpleNamespace`-backed duck-typed `StageQuery` stub is exactly the "dataset-free batch source" `tests/phase40/_fixtures.py` needs — `pinn/data/batches.py`'s `build_stage_batch(source, ...)` accepts any object exposing this attribute/method surface, so Phase 40's fixture module should extend `_DataQuery` (or an equivalent minimal duck-typed stub) rather than build a `TinyCorpus`-style on-disk fixture (`tests/phase39/_fixtures.py`'s `TinyCorpus` is for the *on-disk corpus parser*, which Phase 40 never touches). Pair the stub source with either a tiny `nn.Module` stand-in or the real `build_network(ArchitectureSpec(), dtype=..., device=...)` on CPU/float64 (cheap enough for unit tests, per `pinn/verification/overfit_probe.py:326`) — RESEARCH.md's Wave-0-Gaps section explicitly recommends the latter.

---

### `tests/phase40/test_*.py` (deferred-import skip-guard pattern — apply verbatim to every test file)

**Analog:** `tests/phase38/test_loss_catalog.py:29-40` and `tests/phase39/test_admission.py:19-30` (identical idiom, module-scoped):
```python
MODULE = "pinn.loss_catalog"

def _import_symbol(name: str):
    """Deferred import so a missing symbol becomes a SKIP, not an ERROR."""
    try:
        mod = importlib.import_module(MODULE)
    except ImportError as exc:
        raise unittest.SkipTest(f"{MODULE} has not landed yet: {exc}") from exc
    if not hasattr(mod, name):
        raise unittest.SkipTest(f"{MODULE}.{name} has not landed yet")
    return getattr(mod, name)
```
Every `tests/phase40/test_controllers.py`, `test_optimizer_phase.py`, `test_scheduled_weights.py`, `test_collocation_sampler.py`, `test_grad_clip.py`, `test_stage_exit.py`, `test_slbfgs_preflight.py` file gets its own `MODULE = "pinn.training.<module>"` constant and this exact `_require`/`_import_symbol` helper (renamed to import `tests.phase40._SKIP_PHRASE` per the Phase-39 convention above, not the bare `"has not landed yet"` string Phase 38 used before Phase 39 centralized it).

**Optimizer-phase spy pattern:** `tests/phase38/test_prohibitions.py:157-282` (`test_write_spy_no_simulation_data_writes`) shows the established "monkeypatch a real callable, count/record invocations, assert on the recorded list" idiom (there: `builtins.open`/`os.mkdir`/etc.). `test_optimizer_phase.py`'s "clip-call count == 1 in Adam / 0 in L-BFGS" assertion (TRAIN-02/TRAIN-05, RESEARCH.md Pitfall 5) should use the same `mock.patch(...)` + call-count-recording style rather than inspecting private controller state.

---

### `tests/phase40/test_prohibitions.py` (mechanical audit, N/A)

**Analog:** `tests/phase39/test_prohibitions.py` (whole file, 466 lines) is the direct template — same purpose (AST-based mechanical audit run BEFORE and alongside production code) for the new `pinn/training/*` surface:
```python
# tests/phase39/test_prohibitions.py:172-184
def discover_pinn_modules():
    out = []
    for path in sorted((ROOT / "pinn").rglob("*.py")):
        rel = path.relative_to(ROOT).as_posix()
        if rel.endswith("__init__.py") or "data-handling" in rel.split("/") or rel in _LEGACY:
            continue
        out.append(path)
    return out

def discover_data_modules():
    return [p for p in discover_pinn_modules()
            if p.relative_to(ROOT).as_posix().startswith("pinn/data/")]
```
```python
# tests/phase39/test_prohibitions.py:69-77 — per-symbol deferred import for the audit's own SkipTest, not ERROR
def _require(symbol, module):
    try:
        mod = importlib.import_module(module)
    except ImportError:
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {module}.{symbol}")
    if not hasattr(mod, symbol):
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {module}.{symbol}")
    return getattr(mod, symbol)
```
Extend `discover_data_modules()`-style scoping to `discover_training_modules()` filtering on `pinn/training/`, and reuse `executable_source`/`executable_source_from_text` (docstring/comment stripping, `tests/phase39/test_prohibitions.py:84-99`) unchanged. `tests/phase38/test_prohibitions.py:49-122` additionally shows the "known-module superset" contract (`KNOWN_PHASE38_MODULES`, `_discover_phase38_modules`) and the v1.3-token ban list (`:305-320`) — Phase 40's prohibitions test must extend the SAME `_V1_TOKENS`-style ban (`basic_architecture`, `data-processing-pipeline-full`, `data-handling`) over `pinn/training/*.py`, per CTX-17's continuing prohibition.

---

## Shared Patterns

### Frozen dataclass + fail-closed `__post_init__` validation
**Source:** `pinn/architecture_spec.py:35-141`, `pinn/runtime.py:23-38`, `pinn/loss_catalog.py:64-101`
**Apply to:** `config.py` (`TrainingConfig` nested sections), `scheduled_weights.py`'s per-call weight output, any small typed result (`GradClipOutcome`, `StageExitOutcome`).
```python
@dataclass(frozen=True)
class LossWeights:
    lambda_data: float = 1.0
    ...
    def __post_init__(self) -> None:
        for name, value in fields:
            if not finite or float(value) < 0.0:
                raise ValueError(f"LossWeights.{name} must be finite and non-negative; got {value!r} ...")
```

### Caller-owned RNG discipline (never touch the global RNG)
**Source:** `pinn/data/batches.py:33-36` (`_require_local_rng`); confirmed test coverage `tests/phase39/test_batches.py:217-229` (`test_selection_is_seed_stable_and_does_not_touch_global_numpy_rng`)
**Apply to:** `collocation_sampler.py`, any per-epoch resampling call inside `controllers.py`. Every RNG argument must be an explicit `numpy.random.Generator` (or, for the L-BFGS-phase network init/`torch.Generator` case, an explicit `torch.Generator` per `pinn/network.py:253-255`'s `build_network` pattern) — never `np.random.seed`/global state.

### Explicit dtype/device threading, no `torch.set_default_dtype`, no availability probes
**Source:** `pinn/runtime.py:65-96` (`resolve_runtime`), enforced mechanically by `tests/phase38/test_prohibitions.py:289-303` (`test_no_precision_default_in_discovered_modules`) and `tests/phase39/test_prohibitions.py:114-115,215-218` (`has_global_default_mutation`)
**Apply to:** every `pinn/training/*.py` module — dtype/device always explicit keyword args, sourced only from `resolve_runtime`'s returned `RuntimeSpec`. `test_prohibitions.py` for Phase 40 must extend the identical `_GLOBAL_DEFAULT_TOKENS = ("set_default_dtype", "is_available")` ban.

### Fail-loud non-finite detection (raise, never silently pass through)
**Source:** `pinn/physics_residual.py:90-95` (`_require_finite`), `pinn/verification/overfit_probe.py:70-76` (`OverfitFail`) and `:348-349,357-358,365-366` (per-step `isfinite` checks before/after `optimizer.step()`)
**Apply to:** `grad_clip.py`'s NaN/Inf detection feeding RECOVER (use `clip_grad_norm_(..., error_if_nonfinite=True)` per RESEARCH.md's verified Code Example, not a manual `isnan` scan — this is also the Don't-Hand-Roll guidance), and `controllers.py`'s per-epoch loss finiteness gate.

### Typed sentinel exception carrying diagnostic fields
**Source:** `pinn/data/types.py:157-177` (`DataVersionHashMismatch`, `StageZeroUnderpopulated`)
**Apply to:** `slbfgs_preflight.py`'s `StochasticLBFGSNotImplemented(stage)`, and any other Phase-40 typed refusal (e.g. a config-required-field-unset error per CTX-39).

### Deferred-import `unittest` skip-guard (never ERROR on a not-yet-landed symbol)
**Source:** `tests/phase38/test_loss_catalog.py:29-40`, centralized further in `tests/phase39/__init__.py:32-37` (`_SKIP_PHRASE`) + every Phase-39 test module's local `_require`
**Apply to:** all 8 `tests/phase40/test_*.py` behavior files.

### Mechanical AST prohibition audit (glob-discover + docstring-stripped source scan)
**Source:** `tests/phase38/test_prohibitions.py` (whole file) and `tests/phase39/test_prohibitions.py` (whole file)
**Apply to:** `tests/phase40/test_prohibitions.py` — scoped to `pinn/training/*.py`, reusing `executable_source`/`discover_*_modules`/v1.3-token-ban verbatim.

## No Analog Found

| File | Role | Data Flow | Reason |
|---|---|---|---|
| `pinn/training/checkpoint.py` | service | file-I/O | No existing module in `pinn/` uses `torch.save`/`torch.load`, `state_dict()`/`load_state_dict()` composition, or `typing.Protocol` (grep-confirmed: zero hits for all three). Nearest structural precedent is `pinn/runtime.py`'s narrow-seam discipline (cited above); the planner should treat CTX-43's `CheckpointStore` as a genuinely new pattern for this codebase, built from stdlib `typing.Protocol` (zero new dependency) plus the `state_dict()` equality-testing idiom already exercised in `tests/phase38/test_network_structure.py:216-232`. |

## Metadata

**Analog search scope:** `pinn/` (all Phase 37/38/39 modules), `pinn/data/`, `pinn/verification/`, `tests/phase37/`, `tests/phase38/`, `tests/phase39/`.
**Files read directly:** `pinn/__init__.py`, `pinn/data/__init__.py`, `pinn/verification/__init__.py`, `pinn/architecture_spec.py`, `pinn/runtime.py`, `pinn/loss_catalog.py`, `pinn/network.py`, `pinn/physics_residual.py`, `pinn/constants.py`, `pinn/data/batches.py`, `pinn/data/types.py`, `pinn/data/admission.py`, `pinn/data/stages.py`, `pinn/data/adapter.py` (excerpt), `pinn/verification/overfit_probe.py`, `pinn/verification/componentwise_ad.py` (excerpt), `tests/phase38/test_prohibitions.py`, `tests/phase38/test_loss_catalog.py` (excerpt), `tests/phase39/__init__.py`, `tests/phase39/_fixtures.py`, `tests/phase39/test_batches.py`, `tests/phase39/test_admission.py` (excerpt), `tests/phase39/test_prohibitions.py`.
**Pattern extraction date:** 2026-07-17
