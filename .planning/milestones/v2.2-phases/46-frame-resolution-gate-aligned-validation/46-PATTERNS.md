# Phase 46: Frame Resolution & Gate-Aligned Validation - Pattern Map

**Mapped:** 2026-07-25
**Files analyzed:** 11 new/modified production files + 5 new test files (Wave 0 gaps per RESEARCH.md)
**Analogs found:** 11 / 11 (production); 5 / 5 (tests) — all files have a strong same-repo analog; none fall into "No Analog Found"

This map builds on `46-RESEARCH.md`'s call-chain tracing (already file:line-grounded) and
does not restate its Architecture Patterns / Pitfalls sections. It adds the concrete
excerpts a planner copies into each new file's action section, and flags two places
where the nearest-by-name analog is the WRONG thing to copy.

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|---|---|---|---|---|
| `pinn/verification/target_frame_probe.py` (new, CONF-01) | verification / probe | batch (population census) + transform | `pinn/verification/residual_probe.py` | role-match (physics-residual seam; loader differs — see Anti-Pattern below) |
| CONF-01 evidence artifact writer (inside the probe module) | utility / persistence | file-I/O | `pinn/verification/residual_probe.py::_atomic_write` / `_write_evidence` / `_new_run_dir` | exact (same evidence-tree shape: `raw.json` + `summary.md`) |
| `pinn/training/validation_gate.py` (new, INST-01 full-pool pass + sidecar writer) | service / orchestration composition | CRUD (traverse pool) + batch | `pinn/evaluate.py::evaluate_run` (per-trajectory loop, READ-ONLY pattern source — never invoke/import) | role-match (nearest full-population gate-metrics composition loop in the repo) |
| `pinn/training/controllers.py::checkpoint_hook` hook point (modified, in `pinn/train.py`) | controller / event boundary | event-driven | `pinn/train.py:786-819` (`checkpoint_hook`, itself) | exact (extend in place, same `if` branch) |
| `pinn/train.py::_append_validation_record` (extended schema) | model / persistence | event-driven + file-I/O (append) | `pinn/train.py:75-103` (itself) | exact (extend in place) |
| `pinn/training/summary.py::_compose`/`_render_md` (extended for D-19 projection) | provider / render | transform (render-don't-recompute) | `pinn/training/summary.py::_test_preview` (`summary.py:203-216`) + `_validation_summary` (`summary.py:185-200`) | exact (same file, same render-don't-recompute idiom; do NOT reuse `_null_if_nonfinite` for the new fields — see Anti-Pattern) |
| `tests/phase46/__init__.py` (new) | test / scaffold | n/a | `tests/phase43/__init__.py` | exact |
| `tests/phase46/_fixtures.py` (new) | test / fixture | n/a | `tests/phase40/_fixtures.py::_StubSource` (StageIndex-shaped) | exact for gate-composition/isolation; needs a **second**, separate synthetic raw-vs-scaled fixture for frame-probe tests (no existing analog — see below) |
| `tests/phase46/test_frame_probe.py` (new, D-21) | test / unit | transform | `tests/phase43/test_gate_boundary.py` (style: `_require`, `_SKIP_PHRASE`, boundary-focused `TestCase` classes) | role-match (style analog; no prior frame-probe test exists) |
| `tests/phase46/test_gate_composition.py` (new, D-22) | test / unit+integration | CRUD | `tests/phase43/test_gate_boundary.py` (`ComputeTrajectoryGateMetricsTests`, `AggregateGateVerdictTests`) | exact (same functions under test, new caller) |
| `tests/phase46/test_isolation.py` (new, D-23) | test / unit | event-driven | `tests/phase40/test_prohibitions.py` (AST-based `try/finally` model-mode-restoration enforcement, `test_prohibitions.py:180-196`) | role-match, verified (see excerpt below) |
| `tests/phase46/test_artifacts.py` (new, D-24) | test / unit | file-I/O | `tests/phase43/test_summary_honesty.py::SummaryHonestyTests` + `tests/phase43/test_summary_enrichment.py::SummaryEnrichmentTests` | role-match, verified (both files/classes confirmed to exist; see excerpt below) |

## Pattern Assignments

### `pinn/verification/target_frame_probe.py` (new — CONF-01)

**Primary analog:** `pinn/verification/residual_probe.py` (full file read, 329 lines)
**Secondary analog (positive-control transform, not the residency read):** `pinn/data/preprocessing.py::preprocess_trajectory`
**Secondary analog (population source):** `pinn/data/splits.py::StageIndex`

**Imports pattern** (`pinn/verification/residual_probe.py:1-28`):
```python
from __future__ import annotations

# This must precede Torch and pinn.runtime imports: it is the only reliable
# record of the fallback environment that existed before Torch initialization.
import os as _os

_PRE_IMPORT_FALLBACK = _os.environ.get("PYTORCH_ENABLE_MPS_FALLBACK") or None

import argparse
import datetime as dt
import json
from pathlib import Path
import sys

import torch

from pinn.constants import D_CHARACTERISTIC_LENGTH, EPS_SOFT, T_CHARACTERISTIC_TIME
from pinn.physics_residual import softened_acceleration
from pinn.runtime import resolve_runtime
from pinn.verification.fixture_loader import load_trajectory
```
**Do NOT copy the last import** (`fixture_loader.load_trajectory`) — D-01 requires probing
`StageIndex.snapshot_positions`/`snapshot_times`/`snapshot_velocities` (the production
adapter surface), not the probe-local fixture reader. Replace with:
```python
from pinn.data.adapter import AdmittedSetAdapter
from pinn.data.splits import SplitManifest, StageIndex
from pinn.data.preprocessing import preprocess_trajectory
```

**Evidence-root guard + atomic write pattern** (`residual_probe.py:43-74`):
```python
def _reject_dataset_evidence_root(evidence_root: Path) -> None:
    """Prevent an untrusted evidence-root from writing into simulation_data."""
    dataset_root = (_REPO_ROOT / "simulation_data").resolve()
    try:
        evidence_root.resolve().relative_to(dataset_root)
    except ValueError:
        return
    raise ValueError("evidence-root must not be inside simulation_data")


def _atomic_write(path: Path, content: str) -> None:
    temporary = path.with_suffix(path.suffix + f".tmp.{_os.getpid()}")
    with open(temporary, "w", encoding="utf-8") as handle:
        handle.write(content)
        handle.flush()
        _os.fsync(handle.fileno())
    _os.replace(temporary, path)


def _new_run_dir(evidence_root: Path) -> Path:
    """Allocate a non-overwriting UTC run directory, including same-second runs."""
    _reject_dataset_evidence_root(evidence_root)
    run_id = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    for suffix in range(1000):
        name = run_id if suffix == 0 else f"{run_id}-{suffix:03d}"
        candidate = evidence_root / name
        try:
            candidate.mkdir(parents=True, exist_ok=False)
        except FileExistsError:
            continue
        return candidate
    raise FileExistsError(f"could not allocate exclusive evidence directory under {evidence_root}")
```
**Reusability note:** prefer `pinn.training.atomic_io.atomic_write_text` (verified shared
primitive, `pinn/training/atomic_io.py:41-64`) over hand-rolling `_atomic_write` a second
time — `residual_probe.py`'s own copy predates `atomic_io.py`'s promotion to a shared
module (see its docstring: "Promotes the verified three-site idiom from `stage_scan.py`
/ `splits.py` / `gradcheck_probe.py`"). D-05/D-17 both point at the same shared helper;
use it for both strands rather than reintroducing a fourth divergent copy.

**Evidence-serialization pattern** (`residual_probe.py:77-95`, D-05's "stable key ordering,
deterministic serialization" requirement):
```python
def _write_evidence(raw: dict, evidence_root: Path) -> Path:
    run_dir = _new_run_dir(evidence_root)
    _atomic_write(run_dir / "raw.json", json.dumps(raw, sort_keys=True, indent=2) + "\n")
    summary = (
        "# Phase 38 Rung 3: Residual on Ground Truth\n\n"
        f"- Gate A: {'PASS' if raw['gate_a']['passed'] else 'FAIL'} "
        ...
    )
    _atomic_write(run_dir / "summary.md", summary)
    (run_dir / "summary.md").chmod(0o600)
    return run_dir
```
Copy the shape (`raw.json` sort_keys, `summary.md` narrative render, both atomic,
`0o600` on the Markdown) but retarget the evidence root to the Phase 46 evidence tree
(e.g. `.planning/phases/46-frame-resolution-gate-aligned-validation/evidence/target-frame/`)
and rewrite `summary` to render D-05's required fields (repo commit, split identities +
hashes, locked D/T, dtype/device, arm definitions, trajectory counts, excluded-snapshot
reasons, aggregate distributions) rather than the Gate A/B two-line summary above.

**Residual/finite-difference seam to extract, not duplicate** (`residual_probe.py:139-176`):
```python
def _u_leaf_acceleration(velocities_raw: torch.Tensor, times_raw: torch.Tensor) -> torch.Tensor:
    """Central-difference v'=v_raw*(T/D) on u=t/T, one-sided at endpoints."""
    u = times_raw / T_CHARACTERISTIC_TIME
    velocity_physics = velocities_raw * (T_CHARACTERISTIC_TIME / D_CHARACTERISTIC_LENGTH)
    if u.numel() < 2:
        raise ValueError("residual probe needs at least two trajectory snapshots")
    acceleration = torch.empty_like(velocity_physics)
    acceleration[0] = (velocity_physics[1] - velocity_physics[0]) / (u[1] - u[0])
    acceleration[-1] = (velocity_physics[-1] - velocity_physics[-2]) / (u[-1] - u[-2])
    if u.numel() > 2:
        denominator = (u[2:] - u[:-2]).reshape(-1, 1, 1)
        acceleration[1:-1] = (velocity_physics[2:] - velocity_physics[:-2]) / denominator
    return acceleration
```
This is the model for CONF-01's "raw-arm" hypothesis discriminator (positions treated as
raw `r`, requiring `/D` before the dimensionless comparison per D-03). Build the
symmetric "already-`r'`" arm the same way but without the `/D`/`*(T/D)` conversions — D-03
requires reporting BOTH arms without privileging one in code, so both branches should be
structurally parallel functions/paths, not an `if/else` inside one function.

**Positive-control transform** (`pinn/data/preprocessing.py:171-217`, `preprocess_trajectory`):
```python
def preprocess_trajectory(times, positions, velocities, masses):
    ...
    r_bar, v_bar, R_COM0, V_COM = _com_recenter_and_boost(times, positions, velocities, masses)
    permutation = _canonical_order(masses, r_bar[0], v_bar[0])
    masses_ordered = masses[permutation]
    r_bar = r_bar[:, permutation, :]
    v_bar = v_bar[:, permutation, :]
    ...
    return PreprocessedTrajectory(
        masses_ordered=masses_ordered, permutation=permutation,
        r0_gauge=r_scaled[0], v0_gauge=v_scaled[0],
        r_gauge=r_scaled, v_gauge=v_scaled,
        R0=R0, R_COM0=R_COM0, V_COM=V_COM, D=D, T=T, V=V,
    )
```
`PreprocessedTrajectory.permutation` (`preprocessing.py:67`) is the exact field D-04's
permutation-confound discriminator needs — compare it against `np.arange(3)` (identity)
per trajectory; do not re-derive the sort key. `preprocessing.py:109-120`
(`_canonical_order`) documents the actual sort-key precedence (`-masses` primary,
`file_order` last tie-break via `np.lexsort`'s last-key-first ranking) if the discriminator
needs to explain a non-identity permutation, not just detect one.

**Population traversal seam** (`pinn/data/splits.py:170-186`, `StageIndex.from_split`, and
`splits.py:200-233`, the snapshot accessors):
```python
@classmethod
def from_split(cls, source, manifest, split_name="train"):
    """Build one split-restricted index directly from the admitted adapter."""
    if split_name not in _SPLIT_NAMES:
        raise ValueError(f"split_name must be one of {_SPLIT_NAMES}; got {split_name!r}")
    records = _materialize_records(source)
    ...
    return cls._with_blacklist(selected, blacklist, source)

def record_keys(self) -> tuple[RecordKey, ...]:
    return tuple(self._records)

def snapshot_times(self, key: RecordKey):
    return self._source_value("snapshot_times", key)

def snapshot_positions(self, key: RecordKey):
    return self._source_value("snapshot_positions", key)

def snapshot_velocities(self, key: RecordKey):
    return self._source_value("snapshot_velocities", key)
```
`record_keys()` does NOT return keys pre-sorted (`tuple(self._records)`, dict insertion
order) — D-02's "sorted by canonical `RecordKey`" requirement means the probe (and
INST-01, see below) must explicitly `sorted(...)` the key tuple. `RecordKey` is
`@dataclass(frozen=True, order=True)` (`pinn/data/types.py:122-137`, fields
`variant, fidelity, id`), so `sorted(keys)` is well-defined and stable without a custom
key function.

**Exact resident-target surface being probed** (`pinn/data/adapter.py:923-938`, confirms
RESEARCH.md's finding — cite this verbatim in the evidence artifact's methodology
section, do not paraphrase):
```python
for cand in candidates:
    times_t = torch.tensor(
        np.asarray(cand.times, dtype=np.float64), dtype=self._dtype, device=self._device)
    pos_t = torch.tensor(
        np.asarray(cand.positions, dtype=np.float64), dtype=self._dtype, device=self._device)
    vel_t = torch.tensor(
        np.asarray(cand.velocities, dtype=np.float64), dtype=self._dtype, device=self._device)
    ...
    masses_t = torch.tensor(
        np.asarray(cand.masses_ordered, dtype=np.float64), dtype=self._dtype,
        device=self._device)
    ...
    self._trajectory_tensors[cand.record_key] = (times_t, pos_t, vel_t)
```
and `adapter.py:861-865`:
```python
candidates.append(SimpleNamespace(
    record_key=record_key, variant=variant, fidelity=fidelity,
    times=parsed_brutus.times, positions=parsed_brutus.positions,
    velocities=parsed_brutus.velocities,
    masses_ordered=pre.masses_ordered, raw_ic13=raw_ic13,
    ...))
```
`cand.positions`/`cand.velocities` are `parsed_brutus.positions`/`.velocities` (untouched
parse, file order) while `cand.masses_ordered` is `pre.masses_ordered` (from
`preprocess_trajectory`, canonically reordered) — the exact metadata-pairing divergence
D-04 requires the probe to distinguish from a pure `D`-scale mismatch.

**Anti-pattern — do not point the probe at `fixture_loader`:**
`pinn/verification/fixture_loader.py::load_trajectory` is a SEPARATE, probe-local reader
(confirmed by RESEARCH.md's Pattern 1 and this session's grep of `residual_probe.py`'s
import block). It is the closest-NAMED sibling of the module CONF-01 needs to write, but
using it would violate D-01 ("neither code inspection nor a raw-file-only check may
substitute for the residual evidence over the resident target surface") — it does not
read through `StageIndex`/`AdmittedSetAdapter` at all.

---

### `pinn/training/validation_gate.py` (new — INST-01 full-pool pass + sidecar writer)

**Primary analog for the per-trajectory loop shape (READ-ONLY reference; never invoke,
import, or modify `pinn/evaluate.py` — D-16 hard constraint):**
`pinn/evaluate.py::evaluate_run`, `pinn/evaluate.py:401-434`
```python
per_trajectory: list[dict[str, Any]] = []
model.eval()
try:
    with torch.no_grad():
        for key in test_keys:
            record = test_index.get(key)
            times_native = test_index.snapshot_times(key)
            tau_ic13 = _build_tau_ic13(
                times_native, record.ic13,
                dtype=runtime_spec.dtype, device=runtime_spec.torch_device,
            )
            times_t = torch.as_tensor(
                times_native, dtype=runtime_spec.dtype, device=runtime_spec.torch_device
            ).reshape(-1)
            masses_row = torch.as_tensor(
                record.masses, dtype=runtime_spec.dtype, device=runtime_spec.torch_device
            ).reshape(1, 3)
            masses_batch = masses_row.expand(times_t.shape[0], 3)

            predicted = model(tau_ic13, masses_batch)
            positions = predicted.reshape(-1, 3, 3).detach()

            trajectory_metrics = gate_metrics.compute_trajectory_gate_metrics(
                positions, times_t.detach(), masses_row.reshape(3).detach(),
            )
            per_trajectory.append(
                {"record_key": key, "eps_h": trajectory_metrics.eps_h}
            )
finally:
    model.train()

aggregate = gate_metrics.aggregate_gate_verdict(
    [item["eps_h"] for item in per_trajectory]
)
```
**Critical divergence required by D-12 (this is THE anti-pattern to name explicitly in the
plan):** `evaluate.py:407` passes `times_native` (raw native seconds, from
`test_index.snapshot_times(key)`) directly into `gate_metrics.compute_trajectory_gate_metrics`
alongside physics-frame `positions` — this is Candidate Gap C1 in RESEARCH.md, a real
`r'`-paired-with-raw-`t` unit mismatch in the ONE existing production caller. INST-01 MUST
NOT copy this pairing. Construct `u = times_t / T_CHARACTERISTIC_TIME` explicitly and pass
`u` (never `times_t` directly) to `gate_metrics.finite_difference_velocity` /
`compute_trajectory_gate_metrics`, per D-12's locked `dr'/du` contract. `T_CHARACTERISTIC_TIME`
is imported from `pinn.constants` (already imported in both `evaluate.py:58` and
`residual_probe.py:25`).

**model.eval()/no_grad() bracket — copy this eval()/no_grad()/try-finally shape, NOT
`_run_validation`'s (see Anti-Pattern below):**
```python
model.eval()
try:
    with torch.no_grad():
        ...
finally:
    model.train()
```

**Gate-metrics composition surface (import + call, never reimplement — D-13/D-26):**
`pinn/verification/gate_metrics.py:40-54` (module `__all__`):
```python
__all__ = [
    "EPS_INV", "GATE_EPS_H_REJECT_THRESHOLD", "GATE_SCS_REJECT_THRESHOLD",
    "TrajectoryGateMetrics", "AggregateGateMetrics",
    "finite_difference_velocity", "matched_plummer_hamiltonian_series",
    "trajectory_eps_h", "compute_trajectory_gate_metrics",
    "aggregate_test_eps_h", "scs_from_eps_h", "gate_verdict", "aggregate_gate_verdict",
]
```
`compute_trajectory_gate_metrics(positions, times, masses, *, eps_inv=EPS_INV)` at
`gate_metrics.py:211-222` is pure composition (`finite_difference_velocity` ->
`matched_plummer_hamiltonian_series` -> `trajectory_eps_h`) — call it once per trajectory
with `(positions, u, masses)`. `aggregate_gate_verdict(per_trajectory_eps_h)` at
`gate_metrics.py:280-287` returns the `AggregateGateMetrics(eps_h, scs, verdict)` dataclass
in one call — do not hand-roll the worst-case-max -> `log10` -> threshold chain; D-14's
"derive aggregate SCS from that single value" is exactly this function's contract
(`scs_from_eps_h` is called internally on the already-aggregated `eps_h`, never averaged).

**Full-pool traversal — copy `StageIndex.records_at_or_below`, NOT
`AdmittedSetAdapter.records_at_or_below` (the anti-analog RESEARCH.md's Pitfall 1
identifies):**
`pinn/data/splits.py:254-261` (the correct one — accepts a plain int):
```python
def records_at_or_below(self, stage) -> tuple[RecordKey, ...]:
    numeric = _numeric_stage(stage)
    return tuple(
        key
        for key in self._records
        if self._labels[key] is not StageLabel.UNASSIGNED
        and int(self._labels[key].value) <= numeric
    )
```
versus `pinn/data/adapter.py:1074-1078` (the WRONG one for this purpose — requires
`stage.value`, i.e. a `StageLabel`, not a plain int):
```python
def records_at_or_below(self, stage):
    return tuple(
        k for k, r in sorted(self._records.items())
        if r.stage_label is not StageLabel.UNASSIGNED
        and r.stage_label.value <= stage.value)
```
`RunController._validation_source` is always constructed as a `StageIndex`
(`pinn/train.py::_build_admitted_sources`, confirmed at `train.py:322-360`), so INST-01's
`validation_gate.py` should accept/type its argument as the `StageIndex` seam and call
`records_at_or_below(k)` (plain int `k`, e.g. `int(controller._active_epoch)`'s stage or
whatever numeric stage value the checkpoint_hook has in scope) — never re-derive a
`StageLabel` to call the adapter's version directly. Also note `records_at_or_below`
returns keys in **dict-insertion order**, not sorted — D-11's "sorted `RecordKey` order"
requires the caller to `sorted(...)` the returned tuple explicitly (same caveat as the
CONF-01 probe above).

**Anti-pattern — do NOT reuse `RunController._run_validation`'s `model.eval()` bracket
for the gate pass:** `pinn/training/controllers.py:652-662`:
```python
def _run_validation(self, k: int, weights) -> LossTerms:
    self._model.eval()
    try:
        batch = self._stage_batch(
            self._validation_source, stage=k, collocation_count=1,
        )
        anchor_ctx = self._build_anchor_context(self._validation_source, batch, None)
        loss_terms = self._compose_loss_terms(batch, anchor_ctx, weights)
    finally:
        self._model.train()
    return loss_terms
```
This is the RIGHT model-mode-restoration idiom (`try/finally`) but the WRONG population
(sampled replay/lookahead batch via `_stage_batch`/`select_stage_records` — RESEARCH.md
Pitfall 3) and, per `controllers.py:43-54`'s own module docstring, it is deliberately
**not** wrapped in `torch.no_grad()` because its physics/IC/energy terms need live
autograd. INST-01's gate pass needs neither AD nor a sampled batch — copy the
`try/finally` model-mode-restoration SHAPE from here, but the `.eval()`+`torch.no_grad()`+
full-population-loop CONTENT from `evaluate.py` above. Do not accidentally wrap the gate
pass in a live-AD context (wasted compute + graph retention) or leave `torch.no_grad()`
off (breaks the "detached ... full-trajectory forward pass" D-12 requires).

**Validation event hook boundary (extend in place, same `if` branch):**
`pinn/train.py:786-810` (`checkpoint_hook`):
```python
def checkpoint_hook(controller: RunController, global_step: int) -> None:
    ...
    val = getattr(controller, "_last_val_total", None)
    validation_every = int(config.opt.validation_every)
    if (
        val is not None
        and int(global_step) % validation_every == 0
        and validation_state_cell["last_step"] != int(global_step)
    ):
        validation_state_cell["previous"] = _append_validation_record(
            run_dir / "validation.jsonl",
            step=int(global_step),
            final_val_loss=float(val),
            previous_val_loss=validation_state_cell["previous"],
        )
        validation_state_cell["last_step"] = int(global_step)
        # <-- NEW: full-pool gate-metrics pass + sidecar write belongs here.
```
Add the new pass inside this exact `if` block, gated by the same condition, calling into
`pinn/training/validation_gate.py`'s new composed function — do not add a second
`validation_every`-style config option (D-10) and do not hook it into
`RunController._run_validation` itself (wrong population/cadence granularity per Pitfall 3).

**Atomic sidecar write (D-17) — reuse directly, do not hand-roll a third copy:**
`pinn/training/atomic_io.py:41-64` (`atomic_write_text`, full function already quoted
above under `atomic_io.py`) — call `atomic_write_text(sidecar_path, json.dumps(payload,
sort_keys=True, ...))` BEFORE appending the compact pointer record to `validation.jsonl`
(D-17's ordering requirement; mirrors the Security Domain note in RESEARCH.md: "a
partially-written sidecar advertised by a `validation.jsonl` pointer before it is durable"
is the threat this ordering prevents).

**Compact `validation.jsonl` append pattern to extend (D-18):**
`pinn/train.py:75-103` (`_append_validation_record`, full function):
```python
def _append_validation_record(
    path: Path,
    *,
    step: int,
    final_val_loss: float,
    previous_val_loss: Optional[float],
) -> float:
    """Persist one validation observation and its contemporaneous trend."""
    value = float(final_val_loss)
    if not math.isfinite(value):
        return value
    if previous_val_loss is None or not math.isfinite(float(previous_val_loss)):
        trend = "unavailable"
    elif value < float(previous_val_loss):
        trend = "improving"
    elif value > float(previous_val_loss):
        trend = "worsening"
    else:
        trend = "flat"
    record = {
        "step": int(step),
        "final_val_loss": value,
        "trend": trend,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True, allow_nan=False) + "\n")
        handle.flush()
    return value
```
Note `json.dumps(..., allow_nan=False)` at line 101 — any new non-finite aggregate field
(D-18's "worst-case aggregate `epsilon_H`") added to this record MUST be pre-converted to
a JSON-safe value (string sentinel or similar) before this call, or `allow_nan=False` will
raise `ValueError` on a genuinely non-finite `epsilon_H`. This is exactly why the
`_json_safe_float` pattern below is load-bearing, not optional polish.

**JSON-safe non-finite encoding (D-18/D-20's "retained as numeric evidence with FAIL
status" — the CORRECT precedent):**
`pinn/evaluate.py:296-302`:
```python
def _json_safe_float(value: float):
    v = float(value)
    if math.isnan(v):
        return "NaN"
    if math.isinf(v):
        return "Infinity" if v > 0 else "-Infinity"
    return v
```
Use this pattern (or import/reuse it if the planner chooses to promote it to a shared
location — it currently exists only as a private helper in `evaluate.py`, which INST-01
must not import from) for both the sidecar's per-trajectory `epsilon_H`/SCS values and any
non-finite aggregate field written into the extended `validation.jsonl` record.

**Anti-pattern — do NOT reuse `pinn/training/summary.py::_null_if_nonfinite` for the
sidecar or the `validation.jsonl` gate fields:**
`pinn/training/summary.py:71-81`:
```python
def _null_if_nonfinite(value: Any) -> Optional[float]:
    """CTX-67 null policy for a single scalar: None / NaN / Inf → JSON null."""
    if value is None:
        return None
    try:
        fv = float(value)
    except (TypeError, ValueError):
        return None
    if fv != fv or fv in (float("inf"), float("-inf")):  # NaN / ±Inf without math
        return None
    return fv
```
This COLLAPSES non-finite to `null` — correct for `summary.py`'s own human-readable
"never fabricate a number" policy (CTX-67, applies to loss terms that never finalized) but
WRONG for D-20's "a genuinely computed non-finite `epsilon_H` is instead retained as
numeric evidence with FAIL status" — using `_null_if_nonfinite` here would make a real
FAIL indistinguishable from "never computed" (RESEARCH.md Pitfall 4). The two functions
look almost identical in shape but encode opposite policies; do not let the proximity of
`summary.py` at the D-19 projection step tempt reuse of this specific helper for the
gate's own persisted values (it is fine, and intended, for `summary.py`'s OTHER pre-existing
fields).

---

### `pinn/training/summary.py` (extended — D-19 EVAL-01 precondition projection)

**Analog:** `pinn/training/summary.py::_test_preview` (`summary.py:203-216`) — the existing
"project one committed artifact's key fields into the summary payload" pattern, structurally
identical to what D-19 needs for the validation-gate sidecar pointer:
```python
def _test_preview(path: Optional[PathLike]) -> Optional[Dict[str, Any]]:
    """Project the committed evaluation artifact into the summary payload."""
    metrics = _read_json_mapping(path)
    if metrics is None:
        return None
    verdict = metrics.get("verdict")
    if verdict not in ("PASS", "FAIL"):
        verdict = None
    return {
        "eps_h": _null_if_nonfinite(metrics.get("eps_h")),
        "scs": _null_if_nonfinite(metrics.get("scs")),
        "verdict": verdict,
        "n_test_trajectories": metrics.get("n_test_trajectories"),
    }
```
and `_validation_summary` (`summary.py:185-200`), the existing render of the LATEST
`validation.jsonl` record (already what D-19 extends, not replaces):
```python
def _validation_summary(path: Optional[PathLike]) -> Optional[Dict[str, Any]]:
    """Select the last persisted validation record; never infer a trend."""
    records = _read_jsonl_mappings(path)
    if not records:
        return None
    record = records[-1]
    final_val_loss = _null_if_nonfinite(record.get("final_val_loss"))
    trend = record.get("trend")
    if not isinstance(trend, str) or not trend:
        trend = None
    step = record.get("step")
    return {
        "final_val_loss": final_val_loss,
        "trend": trend,
        "step": step,
    }
```
Add the new compact gate fields (worst-case `epsilon_H`, aggregate SCS, PASS/FAIL, sidecar
pointer, schema version) to this SAME function's returned dict (it already reads the last
`validation.jsonl` record — INST-01 puts the new fields inline in that same record per
D-17, so `_validation_summary` picking them up is a same-function extension, not a new
projection path). This IS `summary.py`'s existing "render, never recompute" contract
(module docstring, `summary.py:1-32`): read the persisted fields, do not recompute
`epsilon_H`/verdict here. Wire the extended dict into `_render_md` (`summary.py:335-344`,
the existing "## Validation summary" section) so D-19's "inspectable ... in the terminal
run summary" lands in `summary.md` as well as `summary.json`.

**Non-finite policy for THESE new fields:** use the `_json_safe_float`/string-sentinel
approach (imported/reused from the sidecar layer), NOT `_null_if_nonfinite` — same
Anti-Pattern as above, restated here because this is the second site (`summary.py`) where
the wrong helper is one line away by proximity.

---

### `tests/phase46/__init__.py` (new)

**Analog:** `tests/phase43/__init__.py` (full file, 29 lines) — copy verbatim, substituting
`Phase43` -> `Phase46`:
```python
# The SOLE definition of the deferred-skip phrase. Imported by every localized
# ``_require`` helper in this package; never re-spelled independently.
_SKIP_PHRASE = "skipped Phase46 production symbol"

__all__ = ["_SKIP_PHRASE"]
```
(module docstring above it, `tests/phase43/__init__.py:1-22`, documents the `_require`
convention every `tests/phase46/test_*.py` module should reuse — one skip phrase, no
`ImportError`/ERROR on an absent not-yet-landed symbol.)

### `tests/phase46/_fixtures.py` (new)

**Analog for the gate-composition/isolation-test StageIndex stub:**
`tests/phase40/_fixtures.py::_StubSource` (full file, 177 lines) — the exact duck-typed
surface (`has_stage`, `records_at`, `records_at_or_below`, `record_keys`, `get`,
`n_snapshots`, `snapshot_times`, `snapshot_positions`, `snapshot_velocities`,
`acceleration_magnitudes`, `stage_label`, `is_blacklisted`,
`blacklisted_physical_keys` property, `gold_numeric_stage_count` property) that
`StageIndex`-consuming code dereferences. `make_stub_split_sources` (`_fixtures.py:144-158`)
already returns the disjoint `(train_source, validation_source)` pair shape D-23's
isolation tests need ("the helper sees validation only").

**No existing analog for the frame-probe fixture** (D-21's "synthetic trajectories encoded
once as raw positions and once as locked processed/scaled targets with the same D/T"): this
is new fixture surface. Model it on `_StubSource.snapshot_positions`/`snapshot_velocities`
(`_fixtures.py:99-112`, deterministic closed-form positions as a function of `times`) but
add a second synthetic encoding scaled by the SAME `D_CHARACTERISTIC_LENGTH`/
`T_CHARACTERISTIC_TIME` constants the production probe imports from `pinn.constants`, so
the two encodings are genuinely the same underlying trajectory in two frames (not two
unrelated fixtures that happen to both exist).

### `tests/phase46/test_frame_probe.py`, `test_gate_composition.py`

**Style analog:** `tests/phase43/test_gate_boundary.py` (full file, 342 lines) — the
`_require(symbol, module)` skip-not-error helper (lines 27-34), one `TestCase` class per
behavior cluster, and the explicit strict-boundary tests (`test_eps_h_equality_boundary_passes`,
`test_gate_verdict_is_never_rendered_backwards`) are the exact style D-14/D-22's
"strict threshold direction" and boundary assertions should mirror:
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
Reuse `aggregate_gate_verdict`'s existing test pattern (`AggregateGateVerdictTests`,
`test_gate_boundary.py:320-337`) directly for D-22's "aggregate SCS derivation" and
"worst-case aggregation" assertions:
```python
class AggregateGateVerdictTests(unittest.TestCase):
    def test_worst_trajectory_drives_the_aggregate_verdict(self):
        aggregate_gate_verdict = _require("aggregate_gate_verdict")
        result = aggregate_gate_verdict([1e-8, 1e-6, 2.0e-5])
        self.assertEqual(result.eps_h, 2.0e-5)
        self.assertEqual(result.verdict, "FAIL")
```
These test the SAME function INST-01 calls, so the new integration test only needs to
prove the multi-trajectory CALLER wiring, not re-test `gate_metrics` internals (D-13/D-26).

### `tests/phase46/test_isolation.py` (new, D-23)

**Analog, verified:** `tests/phase40/test_prohibitions.py:180-196`
(`catches_around_clip`, an AST-based detector already enforcing the exact
try/finally-without-except restoration contract this new file's tests need to prove for
the gate pass):
```python
def catches_around_clip(source_text):
    """AST over RAW text: True if a handler-bearing ``try`` contains a ``.clip`` call.

    Scoping to ``Try`` nodes with a NON-EMPTY ``handlers`` list is load-bearing:
    40-05 REQUIRES a bare ``try/finally`` (no handlers) to restore
    ``model.train()`` after the validation pass, and a blanket ban on ``Try``
    nodes would collide with it. A handler-less ``try/finally`` cannot swallow a
    signal — only an ``except`` can — so this detector bans exactly the contract
    violation and nothing else. Applied to ``pinn/training/controllers.py`` only,
    ``.is_file()``-guarded.
    """
    tree = ast.parse(source_text)
    for node in ast.walk(tree):
        if isinstance(node, ast.Try) and node.handlers:
            if _contains_clip_call(node):
                return True
    return False
```
This confirms the project convention D-23 must follow for `validation_gate.py`'s own
gate pass: a bare `try/finally` (no `except` handler) around the `model.eval()`/
`model.train()` bracket, so a signal or exception during the gate pass still restores
train mode (matches `evaluate.py`'s `try/finally` shape quoted above) — the isolation
test should assert this AST shape on the new module directly (mirroring this detector's
technique) or assert the runtime behavior (mode restored after a forced exception),
whichever the planner's existing `tests/phase46/` convention prefers. Also assert, per
D-16/D-23: the helper's accepted-source type is `StageIndex` for the VALIDATION split
only (construct it from `tests/phase40/_fixtures.py::make_stub_split_sources`'s
`validation_source`, never `train_source`), and that no `pinn.evaluate` import/attribute
appears anywhere in the new module's import graph (a static `ast`/`sys.modules` check is
consistent with the technique `test_prohibitions.py` already establishes).

### `tests/phase46/test_artifacts.py` (new, D-24)

**Analog, verified:** `tests/phase43/test_summary_honesty.py::SummaryHonestyTests`
(class exists, `test_summary_honesty.py:13`, with
`test_finished_summary_states_all_three_honesty_rules` and
`test_failed_and_interrupted_summaries_are_null_only_and_skip_metric_sections` at lines
22 and 38) and `tests/phase43/test_summary_enrichment.py::SummaryEnrichmentTests` (class
exists, `test_summary_enrichment.py:27`, with
`test_finished_summary_uses_one_payload_and_fixed_section_order` (line 53),
`test_missing_persisted_inputs_are_unavailable_and_empty_curriculum_is_named` (line 120),
`test_terminal_train_caller_passes_persisted_validation_and_curriculum` (line 142), and
`test_actual_evaluate_flow_refreshes_the_completed_run_summary_once` (line 149)). These
two files are the project's existing style for "summary render reflects exactly the
persisted artifact, missing/malformed input is a no-op, never a fabricated value" — the
same shape D-24 needs for sidecar publication, schema validation, JSON-safe non-finite
encoding, and fail-closed empty/missing/corrupt cases. Model `test_artifacts.py`'s
sidecar-specific assertions (atomicity, pointer-after-durable-write ordering) on
`pinn/training/atomic_io.py`'s own module docstring contract (`atomic_io.py:1-10`,
the tmp+fsync+replace+dir-fsync ordering) rather than inventing a new assertion style.

## Shared Patterns

### Atomic write (D-05 evidence artifact, D-17 sidecar)
**Source:** `pinn/training/atomic_io.py::atomic_write_text` (`atomic_io.py:41-64`)
**Apply to:** `target_frame_probe.py`'s evidence writer AND `validation_gate.py`'s sidecar
writer. Prefer this shared helper over `residual_probe.py`'s locally-duplicated
`_atomic_write`/`_new_run_dir` (which predates the shared module) — reuse the module, copy
only the evidence-tree LAYOUT convention (`raw.json` + `summary.md`, run-dir-per-invocation
via a UTC-timestamped subdirectory).

### JSON-safe non-finite encoding (D-18, D-20)
**Source:** `pinn/evaluate.py::_json_safe_float` (`evaluate.py:296-302`)
**Apply to:** every persisted `epsilon_H`/SCS/aggregate field in the CONF-01 evidence
artifact and the INST-01 sidecar/`validation.jsonl` extension.
**Do NOT apply:** `pinn/training/summary.py::_null_if_nonfinite` (`summary.py:71-81`) to
any of the above — it is the opposite policy (null-collapse), correct only for
`summary.py`'s pre-existing human-summary fields.

### Split-restricted, leakage-free traversal (D-01, D-02, D-11, D-16)
**Source:** `pinn.data.splits.StageIndex` (`records_at_or_below`, `snapshot_positions`,
`snapshot_times`, `snapshot_velocities`, `record_keys`, `splits.py:200-261`)
**Apply to:** both strands. Never `pinn.data.adapter.AdmittedSetAdapter.records_at_or_below`
directly (different argument contract, `adapter.py:1074-1078`) and never a test `StageIndex`
(D-16 — INST-01's helper signature should make constructing/accepting a test-labeled index
a type error or an explicit refusal, testable per D-23).

### Deterministic sort order (D-02, D-11, D-18)
**Source:** `RecordKey` is `@dataclass(frozen=True, order=True)` (`pinn/data/types.py:122-137`,
fields `variant, fidelity, id`).
**Apply to:** both strands — `StageIndex.record_keys()` and `records_at_or_below()` both
return dict-insertion order, NOT sorted; every population traversal must wrap the result in
`sorted(...)` explicitly. This is a real gap between what `StageIndex` returns and what
D-02/D-11/D-18 require — do not assume sortedness from the method name.

### Coherent `r'`/`u` pairing (D-12) — the one true contract, and the one place it's violated today
**Source of the correct pairing:** `residual_probe.py:139-151`'s `u = times_raw / T_CHARACTERISTIC_TIME`
construction, and `ctl_instruction.md`'s locked `u=t/T` contract (per CONTEXT.md canonical refs).
**Source of the WRONG pairing (READ-ONLY, do not copy, cite as the thing to avoid):**
`pinn/evaluate.py:407,423-425` passes raw `times_native` into `gate_metrics.compute_trajectory_gate_metrics`
alongside `r'`-frame `positions` — RESEARCH.md Candidate Gap C1, orthogonal to Phase 46's
write scope (evaluate.py is out of bounds) but directly informs what INST-01 must NOT
replicate in its own, new caller.

### Model-mode restoration under failure (D-23)
**Source:** `pinn/evaluate.py:402-430`'s `model.eval()` / bare `try: ... finally: model.train()`
bracket, and the project-wide convention that bracket enforces — confirmed by
`tests/phase40/test_prohibitions.py:180-196`'s AST detector, which specifically PERMITS a
handler-less (`except`-free) `try/finally` around a validation pass while banning any
handler-bearing `try` that wraps a gradient-clip call. `validation_gate.py`'s gate pass
should use the same handler-less `try/finally` shape.
**Apply to:** `validation_gate.py`'s full-pool forward pass.

## No Analog Found

None — every file in the recommended structure has at least a role-match analog in the
existing `pinn/verification/`, `pinn/training/`, `pinn/data/`, or `tests/phase40|43/` trees.
The one genuinely novel surface (the frame-probe's raw-vs-scaled synthetic fixture pair,
D-21) has no prior analog because no prior phase built a symmetric two-hypothesis probe;
it is called out above as new fixture surface to model on `_StubSource`'s deterministic
snapshot-generation style rather than copy verbatim.

## Metadata

**Analog search scope:** `pinn/verification/`, `pinn/training/`, `pinn/data/`, `pinn/`
(top-level: `train.py`, `evaluate.py`, `loss_catalog.py`, `constants.py`), `tests/phase40/`,
`tests/phase43/`.
**Files read in full or targeted-section for this map:** `pinn/verification/residual_probe.py`
(full), `pinn/verification/gate_metrics.py` (full), `pinn/training/atomic_io.py` (full),
`pinn/training/summary.py` (full), `pinn/evaluate.py` (targeted: 251-478),
`pinn/train.py` (targeted: 75-184, 780-909), `pinn/training/controllers.py` (targeted:
1-70, 610-684), `pinn/data/splits.py` (targeted: 1-274), `pinn/data/types.py` (targeted:
59-148), `pinn/data/adapter.py` (targeted: 172-192, 820-939, 1060-1089),
`pinn/data/preprocessing.py` (targeted: 63-222), `pinn/data/batches.py` (targeted:
209-287), `pinn/loss_catalog.py` (targeted: 165-194), `tests/phase43/__init__.py` (full),
`tests/phase43/test_gate_boundary.py` (full), `tests/phase40/_fixtures.py` (full),
`tests/phase40/test_prohibitions.py` (targeted: 175-204, grep-located),
`tests/phase43/test_summary_honesty.py` (grep-located: 13-40),
`tests/phase43/test_summary_enrichment.py` (grep-located: 27-200).
**Pattern extraction date:** 2026-07-25
