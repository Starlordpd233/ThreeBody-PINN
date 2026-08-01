# Phase 48: Loss-Math Conformance - Pattern Map

**Mapped:** 2026-08-01
**Files analyzed:** 13 new/modified files
**Analogs found:** 13 / 13 at file level

## Mapping Resolution Note

The float32/MPS clip question is grounded and does not block planning. The owner
authorized the implementer to choose and record any clip satisfying invariant A
in `.planning/milestones/v2.1-phases/45-trainex-r2-erw-package-assembly/45-GAPS.md:423-448`.
Phase 48 D-08 then delegates a dtype-derived exponent floor. Use upward-directed
representable rounding of the mathematical `log(torch.finfo(dtype).tiny)`
bound, keep it non-tunable, record the resolved value, and require a real-MPS
regression under the target torch lock.

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|---|---|---|---|---|
| `pinn/loss_catalog.py` | utility/service | transform | same-file loss helpers and causal consumer | exact, in-place |
| `pinn/train.py` | controller / composition root | batch + file-I/O | same-file Phase-47 runtime/metadata setup | exact, in-place |
| `pinn/training/controllers.py` | controller | batch + event-driven | same-file Adam/L-BFGS and loss-assembly paths | exact, in-place |
| `pinn/training/config.py` | config | transform/validation | same-file `LossConfig` | exact, in-place |
| `pinn/training/run_metadata.py` | utility | file-I/O | same-file strict metadata schema | exact, in-place |
| `pinn/training/step_log.py` | provider/utility | event-driven + file-I/O | same-file canonical JSONL registry/sanitizer | exact, in-place |
| `configs/smoke.yaml` | config | file-I/O | `configs/stage0-example.yaml` loss stanza | exact |
| `configs/stage0-example.yaml` | config | file-I/O | `configs/smoke.yaml` loss stanza | exact |
| `tests/phase48/__init__.py` | config | transform | `tests/phase47/__init__.py` | exact |
| `tests/phase48/test_loss_math_conformance.py` | test | transform + request-response | Phase-38 loss tests + Phase-47 assembly test | exact |
| `tests/phase48/test_gradient_observability.py` | test | event-driven | `tests/phase40/test_optimizer_phase.py` | role-match |
| `tests/phase48/test_stage0_energy_config.py` | test | config + transform | Phase-40 config/scheduler + Phase-41 YAML tests | exact |
| `tests/phase48/test_clip_metadata.py` | test | batch + file-I/O | Phase-47 strict metadata tests | exact |

## Pattern Assignments

### `pinn/loss_catalog.py` (utility/service, transform)

**Analog:** same file, especially the shared-helper pattern at
`pinn/loss_catalog.py:140-172` and causal seam at
`pinn/loss_catalog.py:265-276`.

**Imports pattern** (`pinn/loss_catalog.py:25-33`):

```python
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Mapping

import torch

from pinn.constants import (...)
```

No dependency is needed. Keep numerical tensor construction explicit about
`dtype` and `device`, as at `pinn/loss_catalog.py:120-126`:

```python
delta_t = torch.as_tensor(delta, dtype=dtype, device=device)
return torch.where(abs_diff <= delta_t, quadratic, linear)
```

**One-home helper pattern** (`pinn/loss_catalog.py:140-172`):

```python
def _matched_plummer_components(...):
    ...
    return kinetic, potential


def _matched_plummer_hamiltonian(...):
    kinetic, potential = _matched_plummer_components(...)
    return kinetic + potential
```

Apply the same ownership pattern to one causal-exponent-floor helper. Both
`causal_physics_loss` and run setup must call that helper; do not duplicate the
rounding formula in `pinn/train.py`.

**Causal insertion seam** (`pinn/loss_catalog.py:265-276`):

```python
detached = rbar.detach()
cumsum = torch.cumsum(detached, dim=0)
zeros = torch.zeros(1, dtype=dtype, device=device)
cumsum_excl = torch.cat([zeros, cumsum[:-1]], dim=0)
weights = torch.exp(-eta * cumsum_excl)
```

Insert the floor between exponent construction and `torch.exp`. Preserve the
exclusive detached prefix, ascending-time validation, `w_1 = 1`, and the
verified `(weights * rbar).mean()` consumer.

**Authorized new numerical subpattern** (Phase-48 research
`48-RESEARCH.md:544-561`; no exact production analog):

```python
target = math.log(torch.finfo(dtype).tiny)
floor = torch.tensor(target, dtype=dtype, device=device)
if float(floor.detach().cpu()) < target:
    floor = torch.nextafter(
        floor,
        torch.tensor(math.inf, dtype=dtype, device=device),
    )
x_clipped = torch.clamp_min(x, floor)
w_n = torch.exp(x_clipped)
```

This is directed representable rounding, not a tuned constant. Expose enough
detached detail for metadata/tests to prove precision, exponent floor, and
minimum weight.

**`L_data` pattern:** preserve the existing all-element
`_huber(predicted - target, ...).mean()`. Replace provisional wording with
GAP-45-01 provenance; do not introduce a numerical multiply-by-nine change.

---

### `pinn/training/controllers.py` (controller, batch + event-driven)

**Analog:** same-file `_non_data_terms`, `_compose_loss_terms`, Adam path,
L-BFGS closure state, and `_log_step`.

**Imports pattern** (`pinn/training/controllers.py:59-88`):

```python
from __future__ import annotations

import logging
import math
import time
from dataclasses import dataclass, replace
from typing import Any, Callable, Mapping, Optional, Sequence

import numpy as np
import torch

import pinn.loss_catalog as loss_catalog
from pinn.loss_catalog import (..., causal_physics_loss, compose_total, ...)
```

Keep the helper private to this module unless both controller and run setup
truly need it. The causal floor itself belongs in `loss_catalog.py`.

**Correct producer seam** (`pinn/training/controllers.py:519-553`):

```python
residual = accel - force
rbar = (residual ** 2).mean(dim=(-2, -1))
...
phys_term, phys_details = causal_physics_loss(
    rbar,
    times=times_tensor,
    dtype=self._dtype,
    device=self._device,
    return_details=True,
)
```

Replace only the reduction:

```python
rbar = (residual ** 2).sum(dim=(-2, -1)) / 3
```

The closest existing divide-by-body-count math is
`pinn/loss_catalog.py:205-220`:

```python
three = torch.as_tensor(float(_N_BODIES), dtype=dtype, device=device)
l_r = ((pr - tr) ** 2).sum() / three
l_v = ((pv - tv) ** 2).sum() / three
```

**Five live term tensors** (`pinn/training/controllers.py:599-613`):

```python
data_term = self._data_term(batch.data_points)
others = self._non_data_terms(anchor_ctx)
terms = {"data": data_term, **others}
return compose_total(terms, weights)
```

Use these unweighted tensors as the sole gradient-statistics inputs. Do not
create a parallel loss catalog.

**Adam insertion ordering** (`pinn/training/controllers.py:898-975`):

```python
optimizer.zero_grad(set_to_none=True)
loss_terms = self._compose_loss_terms(batch, anchor_ctx, weights)
...
loss_terms.total.backward()
clip_outcome = self._grad_clipper.clip(...)
...
optimizer.step()
```

Compute five raw detached norms after composition and before total backward.
Use `torch.autograd.grad(..., create_graph=False, retain_graph=True,
allow_unused=True, materialize_grads=False)`; `None` parameters contribute
zero within a valid statistic. Let errors propagate and never mutate
parameter `.grad`.

**L-BFGS last-closure convention** (`pinn/training/controllers.py:1014-1043`):

```python
def closure():
    optimizer.zero_grad(set_to_none=True)
    weighted_data = accumulate_chunked_data_term(...)
    other_total = self._weighted_non_data_terms(anchor_ctx, weights)
    other_total.backward()

    total = weighted_data + other_total.detach()
    closure_state["last_loss"] = float(total.detach())
    closure_state["data_detached"] = float(weighted_data.detach())
```

Copy the overwrite-on-every-closure state pattern. Store detached values only
and label their provenance `last_closure_evaluation`; do not claim the
accepted line-search point. The chunked data-only gradient already exists in
`.grad` immediately after `accumulate_chunked_data_term`
(`controllers.py:188-232,1019-1023`); take its global norm after full vector
accumulation, not per chunk.

**Canonical emission seam** (`pinn/training/controllers.py:690-706,791-812`):
pass one explicit step-local statistics mapping into `_log_step` and merge it
into the existing single `extra` record. Do not put gradient statistics in
`_last_widened_details`: validation can overwrite that stash before the
training step is logged.

---

### `pinn/train.py` (composition root, batch + file-I/O)

**Analog:** same-file Phase-47 resolved-runtime and metadata lifecycle.

**Effective-runtime pattern** (`pinn/train.py:591-598,802-807`):

```python
def _resolve_runtime_spec(config: TrainingConfig) -> RuntimeSpec:
    if config.run.strict_cpu_determinism:
        return determinism.apply_strict_cpu_determinism(int(config.run.seed))
    return resolve_runtime(config.run.precision, config.run.device)


runtime_spec = _resolve_runtime_spec(config)
```

Derive clip facts from `runtime_spec.precision`, `runtime_spec.dtype`, and
`runtime_spec.torch_device`, not from raw YAML strings.

**Fresh/resume artifact pattern** (`pinn/train.py:854-886`):

```python
if (run_dir / TRAINING_METADATA_FILENAME).is_file():
    s_h = _assert_s_h_matches_artifact(...)
else:
    s_h, n_train = compute_s_h(train_source)
    s_h = validate_s_h(s_h)
    write_training_metadata(...)
    _assert_s_h_matches_artifact(...)
```

Extend this single branch with the clip facts before controller construction.
Fresh runs write then reload; resumed runs rederive and compare. Do not create a
clip sidecar or silently upgrade old metadata.

**Explicit live-binding validation** (`pinn/train.py:445-472`):

```python
metadata = load_training_metadata(
    run_dir,
    expected_energy_floor_factor=float(energy_floor_factor),
)
live_s_h, live_n_train = compute_s_h(train_source)
...
return float(metadata["s_h"])
```

Pass expected clip facts explicitly into the metadata loader in the same style.

**Config-to-scheduler pass-through** (`pinn/train.py:893-896`):

```python
scheduled_weights = ScheduledWeights(
    int(config.stage.n_adam),
    lambda_e_max=float(config.loss.lambda_e_max),
)
```

Keep this unchanged. Stage-0 zero resolves upstream in config; no conditional or
shadow zero belongs here.

---

### `pinn/training/config.py` (config, transform/validation)

**Analog:** same-file frozen dataclass at `pinn/training/config.py:504-520`.

```python
@dataclass(frozen=True)
class LossConfig:
    """Loss-side caps. Enforces lambda_E^max <= 1 (PHYS-05)."""

    lambda_e_max: float = 1.0

    def __post_init__(self) -> None:
        v = float(self.lambda_e_max)
        if not math.isfinite(v):
            raise ValueError(...)
        if v > 1.0:
            raise ValueError(...)
        if v < 0.0:
            raise ValueError(...)
        object.__setattr__(self, "lambda_e_max", v)
```

Change only the default to `0.0`. Retain generic finite
`0 <= lambda_e_max <= 1` validation so later stages can still pass nonzero
caps. The keyed parser already delegates omitted fields to dataclass defaults
(`pinn/training/config_yaml.py:145-183`); no parser change is expected.

---

### `pinn/training/run_metadata.py` (utility, file-I/O)

**Analog:** same-file exact-key, atomic-write, fail-closed reload pattern.

**Imports** (`pinn/training/run_metadata.py:27-37`):

```python
import json
import math
from pathlib import Path

import numpy as np

from pinn.constants import EPS_SOFT
from pinn.training.atomic_io import atomic_write_text
from pinn.training.validation_gate import RATIFIED_VALIDATION_FRAME
```

**Strict schema registry** (`pinn/training/run_metadata.py:48-62`):

```python
TRAINING_METADATA_FILENAME = "training_metadata.json"
TRAINING_METADATA_SCHEMA_VERSION = 1

_METADATA_KEYS = frozenset(
    {
        "schema_version",
        "s_h",
        "eps_h",
        "n_train",
        "eps_train",
        "energy_floor_factor",
        "frame",
    }
)
```

Bump the schema and extend the exact set with the recorded precision, exponent
floor, minimum weight, and a stable formula identifier.

**Validate-before-atomic-write** (`pinn/training/run_metadata.py:136-165`):

```python
payload = {
    "schema_version": TRAINING_METADATA_SCHEMA_VERSION,
    ...
}
text = json.dumps(payload, sort_keys=True, indent=2) + "\n"
return atomic_write_text(Path(run_dir) / TRAINING_METADATA_FILENAME, text)
```

Validate every clip field before constructing/writing the payload.

**Fail-closed reload** (`pinn/training/run_metadata.py:183-240`):

```python
payload = json.loads(text)
if not isinstance(payload, dict):
    raise ValueError(...)
if set(payload) != set(_METADATA_KEYS):
    raise ValueError(...)
if payload["schema_version"] != TRAINING_METADATA_SCHEMA_VERSION:
    raise ValueError(...)
...
if factor != float(expected_energy_floor_factor):
    raise ValueError(...)
```

Recompute the expected clip facts from the live resolved runtime and compare
exactly. Missing, extra, mistyped, non-finite, wrong-dtype, wrong-formula, or
mismatched values refuse before step 1.

---

### `pinn/training/step_log.py` (provider/utility, event-driven + file-I/O)

**Analog:** same-file registry, sanitizer, and filter.

**Registry pattern** (`pinn/training/step_log.py:33-41,150-157`):

```python
STEP_LOG_FIELDS: dict[str, dict[str, Any]] = {
    "event": {
        "provisional": True,
        "provenance": (...),
    },
    ...
    "grad_norm": {
        "provisional": True,
        "provenance": (...),
    },
}
```

Add exactly ten canonical fields: raw and applied norms for data, IC, physics,
energy, and angular momentum. Use one naming family consistently in
`controllers.py`, this registry, tests, and any optional mirror.

**Non-finite policy** (`pinn/training/step_log.py:240-271`):

```python
for k, v in record.items():
    try:
        nonfinite = not math.isfinite(v)
    except TypeError:
        nonfinite = False
    if nonfinite:
        out[k] = None
        nonfinite_keys.append(k)
    else:
        out[k] = v
out["finite"] = len(nonfinite_keys) == 0
out["nonfinite_keys"] = sorted(nonfinite_keys)
```

Preserve the actual non-finite values until this sanitizer turns them into JSON
`null`; do not substitute numeric zero. Before emission, a normal
`step_completed` must also require all ten statistics to be present and
finite.

**Canonical filter** (`pinn/training/step_log.py:305-319`):

```python
if getattr(record, "event", None) != "step":
    return
obj = {k: record.__dict__.get(k) for k in STEP_LOG_FIELDS}
sanitized = _sanitize_step_record(obj)
line = json.dumps(sanitized, allow_nan=False)
```

Adding keys only to `_log_step` is insufficient; unregistered keys are
silently filtered out.

---

### `configs/smoke.yaml` (config, file-I/O)

**Analog:** its existing loss stanza at `configs/smoke.yaml:45-46`.

```yaml
loss:
  lambda_e_max: 1.0
```

Change only the scalar to `0.0`. Keep the surrounding config shape and parser
path unchanged.

---

### `configs/stage0-example.yaml` (config, file-I/O)

**Analog:** its existing loss stanza at
`configs/stage0-example.yaml:56-57`.

```yaml
loss:
  lambda_e_max: 1.0
```

Change only the scalar to `0.0`. Both shipped Stage-0 entry configs must agree
with the resolved default.

---

### `tests/phase48/__init__.py` (config, transform)

**Analog:** `tests/phase47/__init__.py:9-28`.

```python
Scope discipline
----------------
Every test here is dataset-free and train-free ...

Skip discipline
---------------
There is none: this suite ships green.

Oracle discipline
-----------------
The ... oracle is NOT duplicated here.
```

Copy the phase-package documentation pattern: state dataset-free/train-free
scope, no expected skips except an explicit unavailable-MPS backend arm, and
which existing `eps_H` proof remains canonical.

---

### `tests/phase48/test_loss_math_conformance.py` (test, transform + request-response)

**Analogs:**

- `tests/phase38/test_loss_catalog.py` for independent Huber and precision-arm
  tests.
- `tests/phase47/test_conf03_eps_h_wiring.py` for assembly-boundary proof.

**Independent Huber oracle** (`tests/phase38/test_loss_catalog.py:47-52,58-89`):

```python
def _huber_elementwise(diff: torch.Tensor, delta: float) -> torch.Tensor:
    abs_diff = diff.abs()
    quadratic = 0.5 * diff * diff
    linear = delta * (abs_diff - 0.5 * delta)
    return torch.where(abs_diff <= delta, quadratic, linear)

...
ref = _huber_elementwise(residual, HUBER_DELTA_DATA).mean()
self.assertTrue(torch.allclose(got, ref, rtol=1e-12, atol=1e-12))
```

Extend this with an explicit
`sum(elementwise_huber) / (9 * N_t)` hand oracle and cases on both sides of
the Huber transition.

**Assembly-boundary pattern**
(`tests/phase47/test_conf03_eps_h_wiring.py:71-103,131-154`):

```python
def _construction_inputs(...):
    ...
    return positional, kwargs, train_source, config


def _make_controller(...):
    positional, kwargs, train_source, config = _construction_inputs(...)
    return RunController(*positional, s_h=s_h, **kwargs), train_source, config


def test_eps_h_assembly_value():
    controller, train_source, config = _make_controller(...)
    ...
    assert ctx_a.eps_h == expected
    assert ctx_b.eps_h == expected
```

For `Rbar`, monkeypatch/intercept the actual
`controllers.causal_physics_loss` call from `_non_data_terms`. Use a
synthetic all-ones `(N_t,3,3)` residual: the locked value is `3`, while the
old mean is `1`. A direct component call is not sufficient.

**Precision/backend arms** (`tests/phase38/test_loss_catalog.py:43-44,354-359`):

```python
def _mps_available() -> bool:
    return bool(
        getattr(torch.backends, "mps", None)
        and torch.backends.mps.is_available()
    )

arms = [("float64", torch.float64, torch.device("cpu"))]
if _mps_available():
    arms.append(("float32", torch.float32, torch.device("mps")))
```

Add CPU float32/float64 cases plus a real-MPS float32 case proving
`0 < w_n <= 1`, `w_1 == 1`, underflow prevention, no-op behavior in the
normal region, sorting validation, and detached-prefix semantics. The MPS proof
must also run as a standalone target-lock probe when pytest is unavailable in
the locked environment.

---

### `tests/phase48/test_gradient_observability.py` (test, event-driven)

**Analogs:** `tests/phase40/test_optimizer_phase.py` for graph/optimizer
behavior and `tests/phase42/test_step_log_jsonl.py` for canonical registry,
sanitization, and parity.

**Cheap graph-connected terms** (`tests/phase40/test_optimizer_phase.py:105-125`):

```python
total = torch.zeros((), dtype=dtype, device=device)
for p in model.parameters():
    total = total + (p ** 2).sum() * 1e-6
zero = torch.zeros((), dtype=dtype, device=device)
return LossTerms(
    data=zero,
    ic=zero,
    phys=torch.tensor(float(phys_value), dtype=dtype, device=device),
    energy=zero,
    angmom=zero,
    total=total,
)
```

Build distinct graph-connected terms so the five raw norms have independent
hand-computable values. Include an unused parameter and a zero-weight energy
term to distinguish a valid zero contribution from a missing statistic.

**Optimizer non-contamination spy pattern**
(`tests/phase40/test_optimizer_phase.py:383-417`):

```python
real_clip = controller._grad_clipper.clip
clip_spy = mock.Mock(wraps=real_clip)
torch_clip_spy = mock.Mock(wraps=torch.nn.utils.clip_grad_norm_)
...
self.assertEqual(marker["adam_clip_calls"], 1)
self.assertEqual(clip_spy.call_count, 0)
self.assertEqual(torch_clip_spy.call_count, 0)
```

Snapshot every parameter `.grad`, clip outcome, and optimizer update with
diagnostics enabled/disabled. Prove Adam and L-BFGS results are identical.

**Whole-vector chunked-gradient pattern**
(`tests/phase40/test_optimizer_phase.py:657-693`):

```python
full_loss.backward()
full_grads = [
    p.grad.clone() if p.grad is not None else torch.zeros_like(p)
    for p in model.parameters()
]
...
total = accumulate_chunked_data_term(...)
chunked_grads = [...]
for full_g, chunked_g in zip(full_grads, chunked_grads):
    torch.testing.assert_close(full_g, chunked_g, rtol=1e-6, atol=1e-9)
```

For L-BFGS, force multiple closure calls and assert the emitted detached values
come from the last evaluation with explicit provenance. Also run with
`validation_every=1` to prove validation cannot overwrite step-local training
statistics.

**Canonical record factory and parity**
(`tests/phase42/test_step_log_jsonl.py:40-75,168-198`):

```python
def _canonical_step_record(step: int, phase: str, stage: int = 0, **overrides):
    rec = {
        "event": "step",
        ...
        "grad_norm": 0.01,
        "step_completed": True,
    }
    rec.update(overrides)
    return rec

...
extra_keys = set(obj) - {"finite", "nonfinite_keys"}
self.assertTrue(extra_keys <= set(self.STEP_LOG_FIELDS))
```

Add all ten gradient fields to the factory and assert Adam/L-BFGS JSONL parity.
For NaN/Inf, reuse `tests/phase42/test_step_log_jsonl.py:200-243`: the values
become JSON null and appear in `nonfinite_keys`; missing or non-finite
statistics force `step_completed == false`.

---

### `tests/phase48/test_clip_metadata.py` (test, batch + file-I/O)

**Analog:** `tests/phase47/test_conf02_s_h_pipeline.py` for metadata
round-trip, tamper refusal, and resume.

**Strict metadata round-trip**
(`tests/phase47/test_conf02_s_h_pipeline.py:379-410,413-489`):

```python
write_training_metadata(...)
payload = load_training_metadata(...)
assert set(payload) == {...}
assert payload["schema_version"] == TRAINING_METADATA_SCHEMA_VERSION
...
unknown = mutated()
unknown["surprise"] = 1
write_payload(unknown)
with pytest.raises(ValueError, match="keys must be exactly"):
    load_training_metadata(...)
```

Extend the exact payload oracle and tamper matrix for every clip field,
including wrong precision, wrong bound/minimum pair, old schema, missing/extra
key, NaN/Inf, and a resume runtime mismatch.

---

### `tests/phase48/test_stage0_energy_config.py` (test, config + transform)

**Analogs:** `tests/phase40/test_config.py`,
`tests/phase40/test_scheduled_weights.py`, and
`tests/phase41/test_config_yaml.py`.

**Stage-0 schedule pattern**
(`tests/phase40/test_scheduled_weights.py:56-79`):

```python
stage_table = {
    0: (0.0, 0.0),
    1: (0.0, 0.0),
    2: (1e-2, 1e-2),
    ...
}
for stage, (le_max, ll_max) in stage_table.items():
    sched = ScheduledWeights(
        n_adam_k=500,
        lambda_e_max=le_max,
        lambda_l_max=ll_max,
    )
```

Assert `LossConfig().lambda_e_max == 0.0`, load both shipped YAMLs, pass each
resolved cap into `ScheduledWeights`, and assert `lambda_e == 0.0` exactly at
every sampled warmup/frozen point. Preserve separate explicit-nonzero tests:
they defend the generic later-stage scheduler and must not be globally rewritten.

## Shared Patterns

### Single Producer, Verified Consumer

**Sources:** `pinn/training/controllers.py:519-553`,
`pinn/loss_catalog.py:265-276`

Correct `Rbar` only at the controller assembly seam. Keep
`causal_physics_loss` as a consumer of a one-dimensional sequence and retain
its downstream mean.

### Resolved Runtime, Not Requested Runtime

**Source:** `pinn/train.py:591-598,802-807`

Any recorded numerical fact comes from the effective `RuntimeSpec`. This
matters when strict CPU determinism overrides requested precision/device.

### Atomic, Exact-Schema Metadata

**Sources:** `pinn/training/run_metadata.py:136-165,168-241`,
`tests/phase47/test_conf02_s_h_pipeline.py:379-489`

Validate first, atomically write once, reload immediately, and fail closed on
resume. Unknown keys and old schemas do not pass.

### One Canonical Step Event

**Sources:** `pinn/training/controllers.py:690-706,791-812`,
`pinn/training/step_log.py:305-319`

Losses, lambdas, total norm, and per-term norms travel through the same
step-local event. JSONL is durable and canonical; TensorBoard is optional.

### Failure Honesty

**Source:** `pinn/training/step_log.py:240-271`

Unused parameters contribute zero within a successfully computed term norm.
A missing whole statistic stays missing; NaN/Inf becomes JSON null and makes a
completed record ineligible.

### Dataset-Free Conformance Tests

**Sources:** `tests/phase47/__init__.py:9-28`,
`tests/phase47/test_conf03_eps_h_wiring.py:12-17`

Use synthetic tensors, stub sources, and controller seams. Phase 48 runs no
training and accesses no held-out evaluation data.

## No Exact Internal Analog

All planned files have file-level analogs. Two internal algorithms are new:

| Internal Pattern | Owning File | Closest Partial Analog | Required Source |
|---|---|---|---|
| Directed-up representable causal exponent floor | `pinn/loss_catalog.py` | `pinn/data/batches.py:195-202` uses `finfo.tiny` before log, but not torch/backend rounding | Owner GAP-45-04 + `48-RESEARCH.md:544-561` |
| Global per-term detached gradient norm | `pinn/training/controllers.py` | `pinn/physics_residual.py:150-186` uses `autograd.grad` for higher derivatives, but its `create_graph=True` flags do not apply | `48-CONTEXT.md` D-16..D-20 + `48-RESEARCH.md:503-523` |

Do not copy the partial analogs mechanically.

## Retain Unchanged

- `pinn/training/scheduled_weights.py`: zero cap already stays zero; retain
  the generic ramp and later-stage nonzero capability.
- The downstream `(weights * Rbar).mean()` in `causal_physics_loss`.
- `tests/phase47/test_conf03_eps_h_wiring.py::test_eps_h_assembly_value` as
  the canonical `eps_H` assembly proof.
- `pinn/training/tb_sink.py` unless the planner deliberately chooses the
  optional mirror; JSONL alone is mandatory.
- Force, Hamiltonian, IC-anchor, angular-momentum, projection, AD, and other
  verified-clean component math.

## Metadata

**Analog search scope:** `pinn/`, `configs/`, and
`tests/phase38`, `tests/phase40`, `tests/phase41`, `tests/phase42`,
`tests/phase43`, `tests/phase47`

**Files scanned:** 135

**Strong analog families retained:** 5

1. Same-file loss/controller/config seams.
2. Phase-47 strict metadata and assembly-boundary tests.
3. Phase-42 canonical JSONL registry/sanitizer tests.
4. Phase-38 loss-oracle and CPU/MPS precision tests.
5. Phase-40 optimizer and schedule tests.

**Pattern extraction date:** 2026-08-01
