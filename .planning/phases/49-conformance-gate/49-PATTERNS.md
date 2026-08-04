# Phase 49: Conformance Gate - Pattern Map

**Mapped:** 2026-08-04
**Files analyzed:** 22 (8 new source, 8 modified source, 1 new data artifact, 7 new test modules — test files grouped as one row)
**Analogs found:** 22 / 22 — every file has a same-repo analog; RESEARCH.md already verified zero unlocatable seams, so this map adds copy-exactly code excerpts rather than proposing new design.

Note: 49-RESEARCH.md already pins exact insertion line numbers/signatures in
`pinn/train.py` and `pinn/training/controllers.py` (D-05 site 1/2, D-17
checkpoint payload). This document does not repeat those line numbers; it
supplies the **style/idiom** to copy at each of those sites, pulled from the
actual analog source this session (byte-for-byte, not paraphrased).

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|---|---|---|---|---|
| `pinn/conformance/__init__.py` | config (package marker) | n/a | `pinn/training/__init__.py`-style empty/marker package | exact |
| `pinn/conformance/table.py` (GATE-01) | service (assertion) | transform | `pinn/training/run_metadata.py` `_validate_causal_clip_facts` | exact |
| `pinn/conformance/census.py` (GATE-02) | service (assertion) | transform | `pinn/training/run_metadata.py` (validate-then-raise) + `pinn/training/config.py` `provisional_fields()` (cross-check source) | exact + role-match |
| `pinn/conformance/register.py` (INST-03) | model/service (schema-validated data loader) | file-I/O | `pinn/training/run_metadata.py` (whole-file pattern: schema_version + frozenset keys + atomic write + re-validate-on-load) | exact |
| `pinn/conformance/preflight.py` (D-27) | service (composer + writer) | file-I/O | `pinn/training/run_metadata.py` `write_training_metadata`/`load_training_metadata` pair | exact |
| `pinn/conformance/divergence_register.json` (data) | config (data artifact) | file-I/O | shape of `run_metadata.py`'s `training_metadata.json` payload (sorted keys, schema_version) | exact |
| `pinn/constants.py` (+D-01 table) | config | n/a (static) | `pinn/constants.py` itself (house style) | exact — self-extension |
| `pinn/training/guards.py` (+2 HALT guards, `causal_stats_missing`) | middleware (per-step interceptor) | event-driven | `pinn/training/guards.py` itself (`StepGuards.check`, `_GUARD_ORDER`, `_HALT_FAMILY`) | exact — self-extension |
| `pinn/training/config.py` (+`InvariantsConfig`) | config | CRUD (load/validate) | `GuardConfig` (sibling nested frozen dataclass) + `RunConfig.run_name: Optional[str] = None` (no-default-is-valid idiom, D-20/Pitfall 4) | exact |
| `pinn/training/config_yaml.py` (+register `InvariantsConfig`) | config | CRUD (load/validate) | `_resolve_nested_cls`'s `known` dict | exact — mechanical addition |
| `pinn/training/summary.py` (+`conformance` block, `eval01_precondition_i`) | service (projection) | transform | `_GATE_KEYS`/`_eval01_precondition_iii`/`_compose`/`_render_md` (Validation summary section) | exact — self-extension |
| `pinn/training/step_log.py` (possible field extension) | config (registry) | streaming (JSONL) | `STEP_LOG_FIELDS` itself | exact — self-extension (research finds no new field strictly required; extend here, never a second log, if the plan adds one) |
| `pinn/training/checkpoint.py` (`CHECKPOINT_SCHEMA_VERSION` bump) | model (schema) | file-I/O | `checkpoint.py`'s own symbolic-reference discipline (`_is_structurally_valid`) | exact — self-extension |
| `pinn/training/controllers.py` (D-05 site 2, `build_checkpoint_payload`, invariant-B state threading) | controller | event-driven | `CurriculumController.step()`'s existing `check_stage_preflight(self._stage)` seam + `build_checkpoint_payload` itself | exact — self-extension |
| `pinn/train.py` (D-05 site 1, `guard_hook` extension) | controller (composition root) | request-response / batch | `main()`'s existing `except ValueError as exc: ...; return finish_run("failed", 1)` refusal shape + `checkpoint_hook`'s `getattr(controller, "_last_val_total", None)` idiom | exact — self-extension |
| `tests/phase49/*.py` (7 modules) | test | n/a | `tests/phase41/test_guards.py` (`_guard_cfg`/`_make_guards`/`test_X_trips_Y`) + `tests/phase40/_fixtures.py` (`_StubSource`/`make_stub_split_sources`) | exact |

## Pattern Assignments

### `pinn/conformance/table.py` (service, transform) — GATE-01

**Analog:** `pinn/training/run_metadata.py` — `_validate_causal_clip_facts` (the exact-equality-against-canonical-derivation discipline D-04 names by name).

**The discipline to copy verbatim** (`pinn/training/run_metadata.py:201-213`):
```python
if enforce_canonical:
    # The representable exponent floor is dtype-defined and therefore
    # backend-independent.  The final ``exp`` result is an active-backend
    # fact (torch 2.12.1's CPU and MPS float32 kernels differ by one ulp),
    # so its exact value is validated by the live expectation comparison
    # rather than regenerated on a different backend here.
    for name in ("causal_clip_exponent_floor",):
        if float(facts[name]) != float(canonical[name]):
            raise ValueError(
                f"{context} {name} does not match the canonical runtime-derived "
                f"value; got {facts[name]!r}; regenerate run metadata via fresh "
                "setup"
            )
```
Copy: **`!=` exact equality, never `math.isclose`**; the raised `ValueError`
names the offending field, its actual value, and what to do about it
("regenerate … via fresh setup" → for the table, the equivalent action is
"the stage's `ScheduledWeights` was not rebound for this stage").

**Reading the live caps correctly (Common Pitfall 1 from RESEARCH — the state_dict, not `.current()`)** — `pinn/training/scheduled_weights.py:246-258`:
```python
def state_dict(self) -> dict[str, Any]:
    """Serialize schedule state into a plain dict of python scalars."""
    return {
        "n_adam_k": self._n_adam_k,
        "warmup_length": self._warmup_length,
        "lambda_phys_max": self._lambda_phys_max,
        "lambda_e_max": self._lambda_e_max,
        "lambda_l_max": self._lambda_l_max,
        "lambda_ic": self._lambda_ic,
        "frozen": self._frozen,
        "frozen_ramp": self._frozen_ramp,
        "last_epoch": self._last_epoch,
    }
```
and the two public properties that ARE safe to read directly —
`pinn/training/scheduled_weights.py:172-180`:
```python
@property
def warmup_length(self) -> int:
    """``I_warm = min(2000, floor(0.1 * N_Adam,k))`` (PHYS-05)."""
    return self._warmup_length

@property
def n_adam_k(self) -> int:
    """The configured Adam epoch budget for this stage."""
    return self._n_adam_k
```
`table.py` should read `scheduled_weights.state_dict()["lambda_phys_max"]` /
`["lambda_e_max"]` / `["lambda_l_max"]` / `["lambda_ic"]` — never
`scheduled_weights.current(0)`, which returns the *ramped* (epoch-0-zero)
value regardless of the cap.

**Refusal message shape to copy** — every `run_metadata.py` `ValueError` names
(a) what failed, (b) the actual value, (c) the corrective action. Apply the
same three-part shape to a table-row mismatch: which `k`, which λ, expected
vs. actual, and "the entered stage's `ScheduledWeights` was not reconfigured
for stage `k`" (this is D-06's *intended* Stage-2 refusal — the message
should make that reading obvious to whoever reads `preflight.json` later).

---

### `pinn/conformance/census.py` (service, transform) — GATE-02

**Analog 1 (validate-then-raise shape):** same `run_metadata.py` idiom as
`table.py` — a validator function per quantity, always raising `ValueError`
with a specific reason, never returning a sentinel.

**Analog 2 (the D-09 cross-check, not adopt, source):**
`pinn/training/config.py` `TrainingConfig.provisional_fields()`
(`pinn/training/config.py:618-680`) is the enumerate-with-provenance surface
census must read and **compare against**, never delegate to. Full excerpt of
the shape to consume (note the `{name, value, provisional, provenance}` dict
shape — this is exactly what a disagreement-finding needs to diff against the
manifest's own classification):
```python
def provisional_fields(self) -> Sequence[Mapping[str, Any]]:
    lookup = {
        "stage.beta": self.stage.beta,
        "stage.patience": self.stage.patience,
        "stage.eps_plateau": self.stage.eps_plateau,
        "stage.eps_phys": self.stage.eps_phys,
        "stage.eps_energy": self.stage.eps_energy,
        "stage.energy_floor_factor": self.stage.energy_floor_factor,
        ...
    }
    out = []
    for name, _default, provenance in _PROVISIONAL:
        out.append(
            {
                "name": name,
                "value": lookup[name],
                "provisional": True,
                "provenance": provenance,
            }
        )
    ...
    return out
```
`census.py` cross-checks its own D-09 class-4 (`placeholder`) verdict on
`stage.energy_floor_factor` against this registry's `provisional=True` entry
and **records the disagreement as a finding** rather than adopting either
side's classification as final — this is the exact case CONTEXT.md/RESEARCH.md
both name (§3.4 locks it, `_PROVISIONAL` still tags it stale).

**Analog 3 (instrumentation-precondition sub-check, D-10):** confirm field
presence against the canonical registry the same way `provisional_fields()`
imports `step_log_fields_provisional_entry` defensively
(`pinn/training/config.py:681-699`):
```python
try:
    from pinn.training.step_log import (
        step_log_fields_provisional_entry,
    )
    out.append(step_log_fields_provisional_entry())
except ImportError:
    out.append({...})
```
Copy the `try/except ImportError` defensive-import shape when `census.py`
needs `STEP_LOG_FIELDS` — never a hard top-level import that could break
census construction if `step_log.py` changes shape later.

---

### `pinn/conformance/register.py` (model/service, file-I/O) — INST-03

**Analog:** `pinn/training/run_metadata.py`, entire module — this is the
**worked example named explicitly by CONTEXT.md D-22**.

**Schema constants shape to copy** (`run_metadata.py:47-70`):
```python
__all__ = [
    "TRAINING_METADATA_FILENAME",
    "TRAINING_METADATA_SCHEMA_VERSION",
    "compute_s_h",
    "validate_s_h",
    "write_training_metadata",
    "load_training_metadata",
]

TRAINING_METADATA_FILENAME = "training_metadata.json"
TRAINING_METADATA_SCHEMA_VERSION = 2

_METADATA_KEYS = frozenset(
    {
        "schema_version",
        "s_h",
        "eps_h",
        "n_train",
        "eps_train",
        "energy_floor_factor",
        "frame",
    } | set(CAUSAL_CLIP_FIELD_NAMES)
)
```
`register.py` mirrors this exactly: `DIVERGENCE_REGISTER_FILENAME =
"divergence_register.json"`, a `REGISTER_SCHEMA_VERSION` int, and a
`frozenset` of the D-23 entry field names (`id`, `kind`, `status`, `title`,
`spec_citation`, `authority`, `rationale`, `what_it_would_take`,
`proof_test`) plus the top-level envelope keys (`schema_version`, `entries`).

**Load/re-validate shape to copy** (`run_metadata.py:265-306`, trimmed to the
structural skeleton — the part that matters is the four-stage gauntlet: file
read → JSON parse → type check → exact key-set check, each with its own
`ValueError`):
```python
def load_training_metadata(run_dir, *, ...) -> dict:
    path = Path(run_dir) / TRAINING_METADATA_FILENAME
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise ValueError(f"training metadata not found: {path}") from exc
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"training metadata is not valid JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError("training metadata payload must be a JSON object")

    keys = set(payload)
    if keys != set(_METADATA_KEYS):
        raise ValueError(
            f"training metadata keys must be exactly {sorted(_METADATA_KEYS)}; "
            f"got {sorted(keys)}; regenerate run metadata via fresh setup"
        )
    if payload["schema_version"] != TRAINING_METADATA_SCHEMA_VERSION:
        raise ValueError(...)
    ...
```
`register.py`'s loader follows this exactly for `divergence_register.json`:
fail-closed on missing file, malformed JSON, wrong type, wrong key set, wrong
schema version, and (D-23) an unrecognized `kind`/`status` enum value or a
`closed` entry with an empty `proof_test` (D-25 — "the register must defend
itself"; this is register-load-time shape validation, not the D-25 CI
re-run of the cited tests, which is a separate meta-test in
`tests/phase49/test_inst03_register.py`).

**Write shape to copy** (`run_metadata.py:251-262`):
```python
payload = {
    "schema_version": TRAINING_METADATA_SCHEMA_VERSION,
    "s_h": s_h,
    ...
}
text = json.dumps(payload, sort_keys=True, indent=2) + "\n"
return atomic_write_text(Path(run_dir) / TRAINING_METADATA_FILENAME, text)
```
`sort_keys=True, indent=2` + trailing `"\n"` + `atomic_write_text` — copy
verbatim; this is also the shape `preflight.json` (below) must use.

**The atomic-write primitive itself** — `pinn/training/atomic_io.py:41-64`
(`atomic_write_text`), imported, never reimplemented:
```python
def atomic_write_text(path: PathLike, content: str) -> Path:
    """Atomically write UTF-8 text to ``path``.

    Verified idiom (stage_scan ``_atomic_write``): write to
    ``path.tmp.{pid}``, flush + ``os.fsync`` the file, ``os.replace`` onto the
    canonical name, then ``os.fsync`` the parent directory. A ``finally``
    unlinks any leftover temp so a failed replace cannot leave a partial
    artifact under the canonical name.
    """
```
Import as `from pinn.training.atomic_io import atomic_write_text` — this is
the "Don't Hand-Roll" item RESEARCH.md already flags; `register.py` and
`preflight.py` both use it, never a raw `open().write()`.

---

### `pinn/conformance/preflight.py` (service, file-I/O) — D-27

**Analog:** `run_metadata.py`'s `write_training_metadata` / `load_training_metadata` pair — same validate-before-write, re-validate-on-load shape, but composing THREE sources (table + census + register) into one `assertions` array rather than one flat payload.

**Ordering discipline to copy** (`write_training_metadata`,
`run_metadata.py:227-262` docstring + body — "validation precedes the
write"):
```python
def write_training_metadata(
    run_dir, *, s_h, n_train, energy_floor_factor, causal_clip_facts,
) -> Path:
    """Validate, then atomically persist ``run_dir/training_metadata.json``.

    Validation precedes the write (D-17: refusal precedes artifact — a
    partially-completed run must not leave records that read like evidence).
    ...
    """
    s_h = validate_s_h(s_h)
    n_train = _validate_positive_int(n_train, what="n_train")
    causal_clip_facts = _validate_causal_clip_facts(causal_clip_facts, context="write")
    ...
    payload = {...}
    text = json.dumps(payload, sort_keys=True, indent=2) + "\n"
    return atomic_write_text(Path(run_dir) / TRAINING_METADATA_FILENAME, text)
```
CONTEXT.md D-27 explicitly **inverts** this ordering for the refusal path
("a refusal writes the artifact first, then exits non-zero") — this is the
one place `preflight.py` must deliberately NOT mirror `run_metadata.py`
verbatim: `run_metadata.py` refuses *before* writing (no artifact on
failure), while `preflight.py` must write the failing assertion record
*then* refuse (evidence of why it was blocked). Both share the same atomic
write primitive and the same "never partial" guarantee — only the
raise-vs-write order differs, and that difference is the D-27 decision
itself, not a discretionary implementation detail.

**The `finish_run("failed", 1)` exit shape `preflight.py`'s caller in
`train.py` must reuse** — the pattern already used seven times in
`main()` per RESEARCH.md (`pinn/train.py:902-907` shape):
```python
except ValueError as exc:
    print(...)
    return finish_run("failed", 1)
```
`table.py`/`census.py` raise `ValueError`; `train.py`'s D-05-site-1 call
site catches it, calls `preflight.write(...)` (or equivalent) to persist the
failing record FIRST, then falls into this exact existing shape.

---

### `pinn/training/guards.py` (middleware, event-driven) — GATE-03

**Analog:** the module itself — invariant A/B are two more entries in the
same ordered-trip / disposition-family machinery already serving NaN/Inf,
loss-explosion, disk-floor, memory-watermark.

**The ordering + family tuples to extend** (`pinn/training/guards.py:44-52`):
```python
_GUARD_ORDER = (
    "nan_inf",
    "loss_explosion",
    "disk_floor",
    "memory_watermark",
)

_HALT_FAMILY = frozenset({"disk_floor", "memory_watermark"})
_RECOVER_FAMILY = frozenset({"nan_inf", "loss_explosion"})
```
Extend to `_GUARD_ORDER = (..., "invariant_a", "invariant_b",
"causal_stats_missing")` (or discretionary names) and add all three to
`_HALT_FAMILY` (D-15: HALT-family, never RECOVER).

**`GuardOutcome` — reuse this dataclass verbatim, no new type**
(`guards.py:164-187`):
```python
@dataclass(frozen=True)
class GuardOutcome:
    disposition: Optional[StageDisposition]
    guard: Optional[str] = None
    tier: Optional[int] = None
    metric: Optional[str] = None
    value: Optional[float] = None
    threshold: Optional[float] = None
    threshold_provisional: bool = True
    step: Optional[int] = None
    stage: Optional[int] = None
    phase: Optional[str] = None
    reason: str = ""
    tripped_guards: tuple[str, ...] = ()
    loss_terms: Optional[Mapping[str, Any]] = None
    grad_norm: Optional[float] = None
    extras: Mapping[str, Any] = field(default_factory=dict)
```
`threshold_provisional` is exactly D-20's `N`-unset signal: invariant B's
`GuardOutcome` sets `threshold_provisional=True` when `N` is unset
(record-only mode) and `False` when the owner has set `N` and it is
enforcing — the field already exists for exactly this purpose, per
RESEARCH.md's own observation.

**The per-guard trip-dict shape to copy for invariant A/B** — one Tier-2
HALT example, `disk_floor` (`guards.py:298-318`):
```python
floor = float(self._thresholds["disk_floor_fraction"])
try:
    usage = shutil.disk_usage(str(root))
    free_frac = float(usage.free) / float(usage.total) if usage.total else 0.0
except OSError:
    free_frac = None
if free_frac is not None and free_frac < floor:
    trips.append(
        {
            "guard": "disk_floor",
            "tier": 2,
            "metric": "disk_free_fraction",
            "value": free_frac,
            "threshold": floor,
            "disposition": StageDisposition.HALT,
            "reason": (
                f"disk free fraction {free_frac} < ⚖ floor {floor}"
            ),
        }
    )
```
Invariant A/B trips append the same six-key dict shape
(`guard`/`tier`/`metric`/`value`/`threshold`/`disposition`/`reason`) into
the same `trips` list inside `StepGuards.check`, so the existing
ordering/HALT-wins-tie logic at `guards.py:364-395` (below) needs zero
changes to absorb them.

**HALT-wins-tie disposition logic — do not reimplement, this already does
the right thing** (`guards.py:364-395`):
```python
order_index = {name: i for i, name in enumerate(_GUARD_ORDER)}
trips.sort(key=lambda t: order_index.get(t["guard"], 99))
tripped_names = tuple(t["guard"] for t in trips)

has_halt = any(t["guard"] in _HALT_FAMILY for t in trips)
if has_halt:
    primary = next(t for t in trips if t["guard"] in _HALT_FAMILY)
    disposition = StageDisposition.HALT
else:
    primary = trips[0]
    disposition = StageDisposition.RECOVER
```
Once invariant A/B/`causal_stats_missing` are added to `_GUARD_ORDER` and
`_HALT_FAMILY`, this loop automatically makes any of them win a tie against
an existing RECOVER-family trip — no new branch needed.

**`check()`'s new required kwarg** — model the addition on the existing
signature style (`guards.py:231-240`):
```python
def check(
    self,
    step: int,
    stage: int,
    phase: str,
    loss_terms: Optional[Mapping[str, Any]] = None,
    grad_norm: Optional[float] = None,
    *,
    disk_root: Optional[PathLike] = None,
) -> GuardOutcome:
```
Add `w_n_stats: Optional[Mapping[str, float]] = None` and (if the plan
needs it) `n_colloc: Optional[int] = None` as keyword-only params after
`disk_root`, following the exact `*, disk_root: Optional[PathLike] = None`
keyword-only convention already used here — this is D-16's "explicit input"
requirement.

**`write_failure_bundle` — reuse unchanged** (`guards.py:407-472`, the
Tier-A-always / Tier-B-best-effort split): no code changes needed; invariant
A/B HALTs flow through this exact function via the existing `guard_hook` →
`write_failure_bundle(run_dir, outcome)` call.

---

### `pinn/training/config.py` (config, CRUD) — `InvariantsConfig`

**Analog 1 (sibling nested dataclass shape):** `GuardConfig`
(`pinn/training/config.py:208-236`):
```python
@dataclass(frozen=True)
class GuardConfig:
    loss_explosion_ceiling: float = _PROVISIONAL_LOSS_EXPLOSION_CEILING
    disk_floor_fraction: float = _PROVISIONAL_DISK_FLOOR_FRACTION
    memory_watermark_fraction: float = _PROVISIONAL_MEMORY_WATERMARK_FRACTION

    def __post_init__(self) -> None:
        prov = "⚖ PROVISIONAL R-1 guard threshold (owner-calibrate-at-Phase-43-pilot)"
        ceiling = _finite_positive(
            "loss_explosion_ceiling", self.loss_explosion_ceiling, prov
        )
        disk = _finite_unit_interval(
            "disk_floor_fraction", self.disk_floor_fraction, prov
        )
        mem = _finite_unit_interval(
            "memory_watermark_fraction", self.memory_watermark_fraction, prov
        )
        object.__setattr__(self, "loss_explosion_ceiling", ceiling)
        object.__setattr__(self, "disk_floor_fraction", disk)
        object.__setattr__(self, "memory_watermark_fraction", mem)
```
`InvariantsConfig` copies this `@dataclass(frozen=True)` +
`__post_init__` + `object.__setattr__` re-binding shape exactly.

**Analog 2 (the "field genuinely optional, no default-on-None error" idiom
— Common Pitfall 4 / D-20)** — `RunConfig.run_name`
(`pinn/training/config.py:329`, validated at `359`):
```python
run_name: Optional[str] = None
...
object.__setattr__(self, "run_name", _validate_run_name(self.run_name))
```
where `_validate_run_name` (`config.py:86-100`) is the model for a
"validate-only-when-present, `None` is a defined valid state" helper:
```python
def _validate_run_name(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError(f"run_name must be a str or None (got {value!r})")
    stripped = value.strip()
    if not stripped:
        raise ValueError(f"run_name must be a non-empty str (got {value!r})")
    ...
```
`InvariantsConfig.front_advance_window_n: Optional[int] = None` needs the
same shape: a private `_validate_front_advance_window_n(value)` that returns
`None` immediately when `value is None`, and validates int/positive only
when present — **do NOT route this through `_require_int`**
(`pinn/training/config.py:36-43`), which raises `ConfigRequiredError` on
`None` and is therefore the wrong helper for a field whose `None` state is
D-20's defined, fail-open-to-record-only state:
```python
def _require_int(name: str, value: Any, provenance: str) -> int:
    if value is None:
        raise ConfigRequiredError(name, provenance)  # <-- wrong for N
    ...
```

**Analog 3 (`RunConfig.__post_init__`'s type-check-and-attach shape for a
nested field)** — `pinn/training/config.py:360-373`:
```python
if not isinstance(self.guards, GuardConfig):
    raise TypeError(
        f"run.guards must be GuardConfig (got {type(self.guards)!r})"
    )
```
`RunConfig.invariants: InvariantsConfig = field(default_factory=InvariantsConfig)`
needs the identical `isinstance` guard added alongside the three existing
ones (`guards`/`checkpoint`/`monitor`).

**Analog 4 (`ConfigRequiredError` itself, for contrast — this is NOT what
`InvariantsConfig` uses, but is the sibling error type census/table DO use
when a truly-required field is absent)** — `pinn/training/config.py:25-33`:
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

---

### `pinn/training/config_yaml.py` (config, CRUD) — register `InvariantsConfig`

**Analog:** the `known` dict inside `_resolve_nested_cls`
(`pinn/training/config_yaml.py:102-117`), the exact site Common Pitfall 3
names:
```python
if isinstance(annotation, str):
    known = {
        "GuardConfig": GuardConfig,
        "CheckpointCadence": CheckpointCadence,
        "MonitorConfig": MonitorConfig,
        "RunConfig": RunConfig,
        "StageConfig": StageConfig,
        "OptConfig": OptConfig,
        "LossConfig": LossConfig,
    }
    # Strip Optional[...] wrappers loosely.
    name = annotation
    if name.startswith("Optional[") and name.endswith("]"):
        name = name[len("Optional[") : -1]
    return known.get(name)
```
Two mechanical edits, both required (Pitfall 3's whole point — one edit
alone silently constructs a plain `dict` instead of `InvariantsConfig`):
1. import `InvariantsConfig` alongside the existing import block
   (`config_yaml.py:27-37`);
2. add `"InvariantsConfig": InvariantsConfig` to the `known` dict above.

**`ConfigKeyError` — the fail-closed unknown-key error `InvariantsConfig`
inherits automatically once registered** (`config_yaml.py:57-67`):
```python
class ConfigKeyError(ValueError):
    """Raised when a YAML key is unknown (sibling of ConfigRequiredError).
    ...
    """
    def __init__(self, dotted_path: str, message: Optional[str] = None) -> None:
        self.dotted_path = dotted_path
        msg = message or f"unknown config key: {dotted_path}"
        super().__init__(msg)
```
`_map_section`'s unknown-key check (`config_yaml.py:163-168`) fires this
with the full dotted path (e.g. `run.invariants.typo_field`) automatically
once `InvariantsConfig` is registered — no new validation code needed here
beyond the registration itself.

**`configs/stage0-example.yaml` sibling shape** — the `run.guards:` block
`run.invariants:` sits directly beside (`configs/stage0-example.yaml:26-33`):
```yaml
  # R-1 is OWNER-RATIFIED (2026-07-22) from the 43-07 pilot evidence.
  # The run banner reprints all three values at every launch. The
  # loss-explosion ceiling stops a diverging run early; read
  # runs/<name>/failure/ before changing it.
  guards:
    loss_explosion_ceiling: 100000000000.0
    disk_floor_fraction: 0.05
    memory_watermark_fraction: 0.7
```
`run.invariants:` follows immediately after (or before) `guards:` at the
same nesting depth, with a comment block explaining D-20's "no default,
absent means record-only" semantics — e.g. `# front_advance_window_n: <owner
sets N here; absent = record-only invariant B, per D-20>` commented out by
default, matching the file's existing convention of showing the
owner-carved slot commented out (see the `recover_retries:` comment block at
lines 9-11).

---

### `pinn/training/summary.py` (service, transform) — `conformance` block + `eval01_precondition_i`

**Analog:** `_GATE_KEYS` / `_eval01_precondition_iii` / `_compose` /
`_render_md` — the exact D-27 "verbatim passthrough, never recomputed, never
null-collapsed" precedent CONTEXT.md cites by name.

**The passthrough-tuple + fixed-render-order pair to mirror**
(`pinn/training/summary.py:65-88`):
```python
# Phase 46 gate keys projected verbatim from the last validation record (D-19).
# Persisted-bytes passthrough: never recomputed, never null-collapsed (D-20).
_GATE_KEYS = (
    "gate_schema_version",
    "gate_eps_h",
    "gate_scs",
    "gate_verdict",
    "gate_status",
    "gate_n_trajectories",
    "gate_n_nonfinite",
    "gate_sidecar",
)

# Fixed render order for summary.md (differs from _GATE_KEYS: metrics first).
_GATE_MD_ORDER = (
    "gate_eps_h",
    "gate_scs",
    "gate_verdict",
    "gate_status",
    "gate_n_trajectories",
    "gate_n_nonfinite",
    "gate_sidecar",
    "gate_schema_version",
)
```
D-28 forbids reusing this exact tuple/name (`gate_*` is Phase 46's
vocabulary) — but the SHAPE (a frozen tuple of key names + a separate
render-order tuple) is exactly what a `_CONFORMANCE_KEYS` /
`_CONFORMANCE_MD_ORDER` pair should copy, all prefixed `conformance_*` /
`preflight_*` per D-28.

**The fail-closed-render-never-raises idiom to copy exactly**
(`pinn/training/summary.py:254-274`, docstring + guard clauses of
`_eval01_precondition_iii`):
```python
def _eval01_precondition_iii(
    record: Mapping[str, Any], path: Optional[PathLike]
) -> bool:
    """True only for the SAME event's exact, contained, fully valid sidecar.
    ...
    Any import, read, parse, validation, identity, or equality failure renders
    False -- never raises.
    """
    if path is None:
        return False
    try:
        from pinn.training import validation_gate as vg
        ...
        return True
    except Exception:
        return False
```
`eval01_precondition_i` (reads `preflight.json`'s open-divergence count,
per D-27/D-20) must follow the identical contract: a `preflight.json` that
is missing, malformed, or fails any check renders `False`, never raises —
the summary render must survive every death mode (this is the same
mandate `summary.py`'s own module docstring states at lines 1-14, "presence
is guaranteed under every death mode").

**`_compose`'s key-insertion point** (`pinn/training/summary.py:408-449`,
the dict literal `_compose` returns) — add the two new keys at the same
flat level as the existing `"validation": ...` line:
```python
payload: Dict[str, Any] = {
    "schema_version": SCHEMA_VERSION,
    "disposition": disposition,
    "run_name": hdr.get("run_name"),
    "header": {...},
    "final_losses": _final_losses_dict(final_losses if success else None),
    "validation": _validation_summary(validation_records_path) if success else None,
    "curriculum": curriculum if success else [],
    "test_preview": preview,
    "comparison": (...),
}
```
Add `"conformance": <verbatim preflight.json bytes or None>,` and
`"eval01_precondition_i": bool(...)`. Note `"conformance"` is populated
regardless of `success` (unlike `"validation"`/`"curriculum"`, which are
gated on `disposition == "finished"`) — a REFUSED run (D-27: "a refusal
writes the artifact first") still has a `preflight.json` to project, and
the whole point of INST-03/D-20 is that a run can carry
`eval01_precondition_i = False` while otherwise looking healthy.

**`_render_md`'s per-section shape to copy** — the "## Validation summary"
block (`pinn/training/summary.py:485-500`):
```python
lines.append("## Validation summary")
lines.append("")
if isinstance(validation, Mapping):
    value = validation.get("final_val_loss")
    lines.append(f"- final_val_loss: {value if value is not None else 'null'}")
    ...
    for key in _GATE_MD_ORDER:
        gate_value = validation.get(key)
        lines.append(f"- {key}: {gate_value if gate_value is not None else 'null'}")
    lines.append(
        "- eval01_precondition_iii: "
        f"{bool(validation.get('eval01_precondition_iii'))}"
    )
else:
    lines.append("- (validation records unavailable)")
```
A new `## Conformance` section mirrors this exactly: an `isinstance(...,
Mapping)` guard, a `for key in _CONFORMANCE_MD_ORDER: ... 'null'` loop, and
an explicit `eval01_precondition_i: {bool(...)}` line — never omit the
section, render "(conformance record unavailable)" the same way an absent
validation record does.

---

### `pinn/training/checkpoint.py` (model, file-I/O) — `CHECKPOINT_SCHEMA_VERSION` bump (D-17)

**Analog:** the module's OWN existing symbolic-reference discipline — every
consumer imports `CHECKPOINT_SCHEMA_VERSION`, never a literal. RESEARCH.md's
"D-17 Verdict" section already did the exhaustive grep proving this is
cheap; the pattern to copy is simply: **bump the one constant, add one
additive dict key, add zero literal-`1` call sites** (there are none —
confirmed by grep this session's predecessor).

**`build_checkpoint_payload`'s additive-key shape** (already given verbatim
in 49-RESEARCH.md `## Code Examples`; the discipline to copy is "new
parameter defaults to `None`, existing 6 call sites need zero edits" — same
family of change as `GuardOutcome.extras: Mapping[str, Any] =
field(default_factory=dict)` in `guards.py:187`, which exists for exactly
this "add a field without breaking existing constructors" purpose).

---

### `pinn/training/controllers.py` (controller, event-driven) — D-05 site 2 / D-17 threading

**Analog:** `CurriculumController.step()`'s own existing top-of-step seam —
`check_stage_preflight(self._stage)` is already called at precisely the
right moment (top of `step()`, before `_get_disposition`); the D-01 table
assertion is inserted immediately after it, following the identical
"synchronous call that raises `ValueError`/refusal-shaped exception before
any step-1 work happens" contract `check_stage_preflight` itself
establishes (`pinn/training/slbfgs_preflight.py`, not modified — cited only
as the shape to match, never edited per D-05).

**Keyword-only optional constructor parameter idiom to copy** — the
existing `stage_factory`/`forced_disposition` precedent RESEARCH.md already
quotes (`controllers.py:1587-1598`): both keyword-only, both default
`None`. A new `conformance_hook: Optional[Callable[[int], None]] = None`
(or the D-17 invariant-B-state threading parameter) must follow this exact
convention — keyword-only, `None` default, so every existing test
constructor call and every existing production call site needs zero edits.

---

### `pinn/train.py` (controller, request-response) — D-05 site 1

**Analog 1 (the refusal shape already used seven times in `main()`):**
```python
except ValueError as exc:
    print(...)
    return finish_run("failed", 1)
```
D-05 site 1's table+census call is wrapped in this identical
try/except/return shape — no new exception-handling idiom invented.

**Analog 2 (reading a private controller attribute defensively — the
`guard_hook` will need this same idiom to reach `w_n_stats`):** RESEARCH.md
already found the exact precedent at `pinn/train.py:961` inside
`checkpoint_hook`: `val = getattr(controller, "_last_val_total", None)`.
`guard_hook`'s new read of `controller._last_widened_details["w_n_stats"]`
follows the identical `getattr(controller, "_last_widened_details", None)`
defensive-access convention — never a direct attribute dereference that
could `AttributeError` on an unpopulated first step.

---

### `tests/phase49/*.py` (test) — D-16/D-29/D-30 trip-test + dataset-free conventions

**Analog 1 (the `test_X_trips_Y` naming + helper-factory convention):**
`tests/phase41/test_guards.py:43-78` — duck-typed config builders:
```python
def _guard_cfg(
    *,
    loss_explosion_ceiling: float = 1.0e6,
    disk_floor_fraction: float = 0.05,
    memory_watermark_fraction: float = 0.7,
):
    """Duck-typed GuardConfig surface — no TrainingConfig import required."""
    return SimpleNamespace(
        loss_explosion_ceiling=loss_explosion_ceiling,
        disk_floor_fraction=disk_floor_fraction,
        memory_watermark_fraction=memory_watermark_fraction,
    )


def _run_cfg(**kwargs):
    return SimpleNamespace(guards=_guard_cfg(**kwargs))


def _make_guards(cfg=None, *, disk_root=None, memory_total_bytes=24 * (1024**3), memory_signal=None):
    StepGuards = _require("StepGuards")
    if cfg is None:
        cfg = _run_cfg()
    ...
    return StepGuards(cfg, **kwargs)
```
and the trip-test shape itself (`tests/phase41/test_guards.py:96-127`):
```python
def test_nan_gradient_trips_recover_and_writes_bundle(self):
    guards = _make_guards(disk_root=self.tmp)
    outcome = guards.check(
        step=3, stage=0, phase="2a",
        loss_terms={"total": 1.0, "data": 0.5},
        grad_norm=float("nan"),
    )
    self.assertIsNotNone(outcome.disposition)
    self.assertEqual(outcome.disposition, self.StageDisposition.RECOVER)
    self.assertEqual(outcome.guard, "nan_inf")
    self.assertEqual(outcome.tier, 1)

    self.write_failure_bundle(self.tmp, outcome)
    readme = _bundle_dir(self.tmp) / "README.txt"
    trip = _bundle_dir(self.tmp) / "trip.json"
    self.assertTrue(readme.is_file())
    ...
```
`test_gate03_invariants.py`'s `test_invariant_a_trips_halt_on_zero_weight`
(or equivalent name) follows this exact shape: a duck-typed `_invariants_cfg`
helper (mirroring `_guard_cfg`), a `guards.check(..., w_n_stats={...})` call
that drives the trip, then asserting `outcome.disposition ==
StageDisposition.HALT` and `outcome.guard == "invariant_a"` — this is the
literal D-16 mandate ("every guard added by this phase must have a test
that drives it to actually trip").

**The module's `_require`/skip-if-absent scaffolding** (`test_guards.py:27-34`)
should also be copied for any Wave-0 test written against not-yet-existing
`pinn.conformance` symbols, so tests can be authored before the
implementation lands without a hard `ImportError` collapsing the whole
suite:
```python
def _require(symbol, module=MODULE):
    try:
        mod = importlib.import_module(module)
    except ImportError:
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {module}.{symbol}")
    if not hasattr(mod, symbol):
        raise unittest.SkipTest(f"{_SKIP_PHRASE} {module}.{symbol}")
    return getattr(mod, symbol)
```

**Analog 2 (dataset-free synthetic-source convention for `test_e2e_seam.py`,
D-30):** `tests/phase40/_fixtures.py`'s `_StubSource` + `make_stub_split_sources`
(full class read this session — `tests/phase40/_fixtures.py:37-158`). Key
excerpt, the disjoint-split factory the e2e seam test's `data.source:
synthetic` config needs:
```python
def make_stub_split_sources(n_train=300, n_validation=300):
    """Return a disjoint ``(train_source, validation_source)`` pair.
    ...
    """
    train_source = make_stub_source(n_stage0=n_train, id_offset=0)
    validation_source = make_stub_source(n_stage0=n_validation, id_offset=50000)
    return train_source, validation_source
```
and the module-import-is-side-effect-free discipline (`_fixtures.py:1-28`
docstring + `_StubSource.__init__`'s deferred `from pinn.data.types import
RecordKey, StageLabel`) — heavy imports deferred into `__init__`, never at
module scope, so importing `tests/phase49/_fixtures.py` (if created) never
requires a dataset or triggers unrelated heavy imports.

---

## Shared Patterns

### Atomic, schema-versioned JSON artifact (register.py, preflight.py)
**Source:** `pinn/training/run_metadata.py` (whole module) + `pinn/training/atomic_io.py:41-64` (`atomic_write_text`)
**Apply to:** `pinn/conformance/register.py`, `pinn/conformance/preflight.py`, `pinn/conformance/divergence_register.json`
```python
text = json.dumps(payload, sort_keys=True, indent=2) + "\n"
return atomic_write_text(Path(run_dir) / FILENAME, text)
```
Every load re-validates: exact key-set (`frozenset`), `schema_version` equality, then per-field type/range checks — never "trust because present."

### Exact-equality-against-canonical-derivation (no tolerance)
**Source:** `pinn/training/run_metadata.py:207-213` (`_validate_causal_clip_facts`)
**Apply to:** `pinn/conformance/table.py` (D-04: the λ-table check), any D-25 register self-defense check
```python
if float(facts[name]) != float(canonical[name]):
    raise ValueError(f"... does not match the canonical runtime-derived value; got {facts[name]!r}; ...")
```

### Guard extension inside existing `StepGuards`, never a second mechanism
**Source:** `pinn/training/guards.py` (`_GUARD_ORDER`, `_HALT_FAMILY`, `GuardOutcome`, the trip-dict-append-to-`trips` loop, `write_failure_bundle`)
**Apply to:** `pinn/training/guards.py` itself (invariant A/B, `causal_stats_missing`)
D-15 forbids a parallel per-step guard loop; every new HALT condition is one more entry in `_GUARD_ORDER`/`_HALT_FAMILY` and one more `trips.append({...})` block with the same six keys (`guard`/`tier`/`metric`/`value`/`threshold`/`disposition`/`reason`).

### Verbatim-passthrough run-record projection, never recomputed, never null-collapsed
**Source:** `pinn/training/summary.py:65-88, 254-313, 408-449, 485-500` (`_GATE_KEYS`, `_eval01_precondition_iii`, `_compose`, `_render_md`)
**Apply to:** `pinn/training/summary.py`'s new `conformance` block + `eval01_precondition_i`
A fixed key tuple + a fixed render-order tuple + a fail-closed-never-raises boolean helper + an `isinstance(..., Mapping)`-guarded markdown section that renders `'null'`/"(... unavailable)" rather than omitting the section.

### Nested frozen-dataclass config section + two-file YAML registration
**Source:** `pinn/training/config.py` (`GuardConfig`, `RunConfig.__post_init__`'s isinstance checks) + `pinn/training/config_yaml.py:102-117` (`known` dict in `_resolve_nested_cls`)
**Apply to:** `pinn/training/config.py` (`InvariantsConfig`) + `pinn/training/config_yaml.py` (register it)
Two edits in lockstep (Common Pitfall 3) — defining the dataclass alone is not sufficient; the YAML mapper's `known` dict is a second, easy-to-forget registration site.

### "None is a defined valid state, not a required-field violation"
**Source:** `pinn/training/config.py:329,359` (`RunConfig.run_name`) + `_validate_run_name` (`config.py:86-100`)
**Apply to:** `pinn/training/config.py` `InvariantsConfig.front_advance_window_n`
Do NOT route through `_require_int` (raises `ConfigRequiredError` on `None`, `config.py:36-43`) — model the validator on `_validate_run_name`'s `if value is None: return None` early return instead (D-20).

### Dataset-free test fixtures and skip-if-absent scaffolding
**Source:** `tests/phase40/_fixtures.py` (`_StubSource`, `make_stub_split_sources`) + `tests/phase41/test_guards.py:27-78` (`_require`, `_guard_cfg`, `_make_guards`)
**Apply to:** all of `tests/phase49/*.py`
Every fixture defers heavy imports into `__init__`/factory functions; every not-yet-implemented-symbol test uses `_require(symbol)` → `unittest.SkipTest` rather than a bare `ImportError` collapse.

## No Analog Found

None. Every file in the phase's expected file list resolved to a same-repo,
same-milestone analog this session. This matches 49-RESEARCH.md's own
finding ("No D-08 census quantity was unlocatable... every mechanism...
already exists in this codebase in a slightly different shape").

## Metadata

**Analog search scope:** `pinn/training/`, `pinn/`, `configs/`, `tests/phase40/`, `tests/phase41/` — directed by 49-RESEARCH.md's own file citations (no exploratory glob/grep needed; RESEARCH.md already named every analog file and line range this document reads from).
**Files scanned (full or targeted read this session):** `pinn/training/run_metadata.py` (full, 361 lines), `pinn/training/guards.py` (full, 510 lines), `pinn/training/atomic_io.py` (full, 92 lines), `pinn/constants.py` (full, 81 lines), `pinn/training/config_yaml.py` (full, 295 lines), `pinn/training/scheduled_weights.py` (full, 272 lines), `configs/stage0-example.yaml` (full, 57 lines), `tests/phase40/_fixtures.py` (full, 176 lines), `pinn/training/summary.py` (lines 1-120, 240-560 of 657), `pinn/training/config.py` (lines 1-100, 150-450, 559-700 of 700), `tests/phase41/test_guards.py` (lines 1-160 of 580).
**Pattern extraction date:** 2026-08-04
