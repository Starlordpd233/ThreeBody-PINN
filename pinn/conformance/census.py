"""GATE-02 explicit placeholder census.

The manifest below is intentionally boring and explicit.  It is the reviewable
population of quantities consumed by the five-term loss; no list is inferred
from provisional configuration tags or Python reflection.
"""

from __future__ import annotations

import importlib
import inspect
import math
from collections.abc import Mapping, Sequence
from types import SimpleNamespace
from typing import Any

import numpy as np
import torch

from pinn.loss_catalog import CAUSAL_CLIP_FIELD_NAMES, LossWeights

try:  # D-10 defensive import: census construction must survive registry drift.
    from pinn.training.step_log import STEP_LOG_FIELDS as _STEP_LOG_FIELDS
except ImportError:  # pragma: no cover - exercised by import-isolation tooling
    _STEP_LOG_FIELDS = {}

STEP_LOG_FIELDS = _STEP_LOG_FIELDS

__all__ = ["CENSUS_MANIFEST", "STEP_LOG_FIELDS", "run_census"]


def _item(quantity: str, term: str, citation: str, expected: str, probe: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "quantity": quantity,
        "term": term,
        "spec_citation": citation,
        "expected_class": expected,
        "probe": dict(probe),
    }


# D-07/D-08: 28 quantities, in the declaration order of the population map.
CENSUS_MANIFEST: tuple[dict[str, Any], ...] = (
    _item("predicted_positions", "L_data", "pinn_architecture.md §3.1", "derived", {"kind": "producer", "name": "predicted_positions"}),
    _item("target_positions", "L_data", "pinn_architecture.md §3.1", "pipeline", {"kind": "producer", "name": "target_positions"}),
    _item("HUBER_DELTA_DATA", "L_data", "pinn_architecture.md §3.1", "spec-constant", {"kind": "constant", "module": "pinn.constants", "name": "HUBER_DELTA_DATA", "expected": 1.0}),
    _item("lambda_data", "L_data", "pinn_architecture.md §3.1", "spec-constant", {"kind": "loss_default", "name": "lambda_data", "expected": 1.0}),
    _item("true_r0", "L_IC", "pinn_architecture.md §3.3", "derived", {"kind": "producer", "name": "true_r0"}),
    _item("true_v0", "L_IC", "pinn_architecture.md §3.3", "derived", {"kind": "producer", "name": "true_v0"}),
    _item("IC13", "L_IC", "pinn_architecture.md §3.3", "pipeline", {"kind": "producer", "name": "IC13"}),
    _item("beta_v", "L_IC", "pinn_architecture.md §3.3", "spec-constant", {"kind": "signature_default", "module": "pinn.loss_catalog", "name": "ic_anchor_loss", "parameter": "beta_v", "expected": 1.0}),
    _item("lambda_ic", "L_IC", "pinn_architecture.md §4.1", "spec-constant", {"kind": "schedule_state", "name": "lambda_ic", "expected": 1.0, "advisory": True}),
    _item("masses_ordered", "L_phys^causal", "pinn_architecture.md §3.2", "pipeline", {"kind": "producer", "name": "masses_ordered"}),
    _item("EPS_SOFT", "L_phys^causal", "pinn_architecture.md §3.2", "spec-constant", {"kind": "constant", "module": "pinn.constants", "name": "EPS_SOFT", "expected": 1e-5}),
    _item("eta_c", "L_phys^causal", "pinn_architecture.md §3.2", "spec-constant", {"kind": "constant", "module": "pinn.constants", "name": "CAUSAL_ETA_C", "expected": 1.0}),
    _item("causal_clip_facts", "L_phys^causal", "pinn_architecture.md §4.1", "derived", {"kind": "metadata", "keys": CAUSAL_CLIP_FIELD_NAMES}),
    _item("D_CHARACTERISTIC_LENGTH", "L_phys^causal", "ctl_instruction.md §2.5", "spec-constant", {"kind": "constant", "module": "pinn.constants", "name": "D_CHARACTERISTIC_LENGTH", "positive": True}),
    _item("T_CHARACTERISTIC_TIME", "L_phys^causal", "pinn_architecture.md Table 2", "spec-constant", {"kind": "constant", "module": "pinn.constants", "name": "T_CHARACTERISTIC_TIME", "expected": 10.0}),
    _item("Rbar", "L_phys^causal", "pinn_architecture.md §3.2", "derived", {"kind": "producer", "name": "Rbar"}),
    _item("collocation set", "L_phys^causal", "ctl_instruction.md LOOP-02 / LOOP-06", "pipeline", {"kind": "producer", "name": "collocation set"}),
    _item("S_H", "L_E", "pinn_architecture.md §3.4", "pipeline", {"kind": "metadata", "keys": ("s_h", "n_train")}),
    _item("eps_H", "L_E", "pinn_architecture.md §3.4", "derived", {"kind": "metadata_product", "keys": ("eps_h", "s_h", "energy_floor_factor")}),
    _item("energy_floor_factor", "L_E", "pinn_architecture.md §3.4", "spec-constant", {"kind": "config", "path": ("stage", "energy_floor_factor"), "expected": 1e-4}),
    _item("h0", "L_E", "pinn_architecture.md §3.4", "derived", {"kind": "producer", "name": "h0"}),
    _item("HUBER_DELTA_ENERGY", "L_E", "pinn_architecture.md §3.4", "spec-constant", {"kind": "constant", "module": "pinn.constants", "name": "HUBER_DELTA_ENERGY", "expected": 1.0}),
    _item("l0", "L_L", "pinn_architecture.md §3.5", "derived", {"kind": "producer", "name": "l0"}),
    _item("EPS_L", "L_L", "pinn_architecture.md §3.5", "spec-constant", {"kind": "constant", "module": "pinn.constants", "name": "EPS_L", "expected": 1e-8}),
    _item("HUBER_DELTA_ANGMOM", "L_L", "pinn_architecture.md §3.5", "spec-constant", {"kind": "constant", "module": "pinn.constants", "name": "HUBER_DELTA_ANGMOM", "expected": 1.0}),
    _item("N_Adam,k", "schedule", "pinn_architecture.md §4.1", "pipeline", {"kind": "config", "path": ("stage", "n_adam"), "positive": True}),
    _item("I_warm", "schedule", "pinn_architecture.md §4.1", "derived", {"kind": "schedule_state", "name": "warmup_length"}),
    _item("D-01 table", "schedule", "pinn_architecture.md §4.1", "spec-constant", {"kind": "constant", "module": "pinn.constants", "name": "PHYS05_LAMBDA_PHYS_MAX", "length": 7}),
)

_REQUIRED_INSTRUMENTATION = (
    "grad_norm_raw_data",
    "grad_norm_raw_ic",
    "grad_norm_raw_phys",
    "grad_norm_raw_energy",
    "grad_norm_raw_angmom",
    "grad_norm_applied_data",
    "grad_norm_applied_ic",
    "grad_norm_applied_phys",
    "grad_norm_applied_energy",
    "grad_norm_applied_angmom",
    "grad_stats_complete",
    "w_min",
    "w_mean",
    "w_max",
    "front_idx",
)

_PRODUCER_QUANTITIES = (
    "predicted_positions",
    "target_positions",
    "true_r0",
    "true_v0",
    "IC13",
    "masses_ordered",
    "Rbar",
    "collocation set",
    "h0",
    "l0",
)


class CensusBlockError(ValueError):
    """A census refusal carrying the report that must be persisted first."""

    def __init__(self, message: str, report: dict[str, Any]):
        super().__init__(message)
        self.report = report


class _ProducerContractViolation(ValueError):
    """A deterministic producer-boundary mismatch safe to persist as evidence."""


def _get_path(value: Any, path: Sequence[str]) -> Any:
    current = value
    for part in path:
        current = getattr(current, part)
    return current


def _finite(value: Any, *, positive: bool = False) -> bool:
    if isinstance(value, bool):
        return False
    try:
        number = float(value)
    except (TypeError, ValueError):
        return False
    return math.isfinite(number) and (not positive or number > 0.0)


def _as_finite_array(value: Any, *, name: str, shape: tuple[int | None, ...]) -> np.ndarray:
    if isinstance(value, torch.Tensor):
        value = value.detach().cpu().numpy()
    try:
        array = np.asarray(value)
    except (TypeError, ValueError) as exc:
        raise _ProducerContractViolation(f"{name} is not array-like") from exc
    if array.ndim != len(shape) or any(
        expected is not None and actual != expected
        for actual, expected in zip(array.shape, shape)
    ):
        raise _ProducerContractViolation(
            f"{name} shape {array.shape!r} does not match {shape!r}"
        )
    if not np.issubdtype(array.dtype, np.number) or not np.all(np.isfinite(array)):
        raise _ProducerContractViolation(f"{name} must contain only finite numbers")
    return array


def _producer_failure(label: str, exc: Exception) -> tuple[bool, str]:
    if isinstance(exc, _ProducerContractViolation):
        return False, str(exc)
    return False, f"{label} producer raised {type(exc).__name__}"


def _producer_contracts(controller: Any) -> dict[str, tuple[bool, str]]:
    """Exercise one resident identity through the real loss-input producers.

    This is a structural run-start check. It consumes the controller's already
    materialized source and performs no corpus scan or admission decision.
    """

    from pinn.data import preprocessing
    from pinn.data.batches import sample_collocation_points, sample_data_points

    results = {
        name: (False, "producer contract was not evaluated")
        for name in _PRODUCER_QUANTITIES
    }
    try:
        source = controller._train_source
        keys = tuple(sorted(source.record_keys()))
        if not keys:
            raise _ProducerContractViolation("training source has no resident records")
        key = keys[0]
        record = source.get(key)
        if getattr(record, "record_key", None) != key:
            raise _ProducerContractViolation("record identity does not match its source key")
        if getattr(record, "physical_key", None) != key.physical_key:
            raise _ProducerContractViolation("record physical identity is misaligned")
    except Exception as exc:
        failure = _producer_failure("resident record", exc)
        return {name: failure for name in _PRODUCER_QUANTITIES}

    try:
        masses = _as_finite_array(record.masses, name="masses_ordered", shape=(3,))
        if np.any(masses <= 0.0):
            raise _ProducerContractViolation("masses_ordered must be strictly positive")
        ic13 = _as_finite_array(record.ic13, name="normalized IC13", shape=(13,))
        raw_ic13 = _as_finite_array(record.raw_ic13, name="raw IC13", shape=(13,))
        if not np.array_equal(raw_ic13[:3], masses):
            raise _ProducerContractViolation(
                "raw IC13 mass slots do not preserve masses_ordered body order"
            )
        fixture_ic13 = preprocessing.build_raw_ic13(
            np.array([1.0, 2.0, 3.0], dtype=np.float64),
            np.array(
                [[0.0, 0.0, 0.0], [3.0, 0.0, 0.0], [1.0, 4.0, 0.0]],
                dtype=np.float64,
            ),
            np.array(
                [[0.0, 0.0, 0.0], [0.0, 3.0, 0.0], [1.0, 0.0, 5.0]],
                dtype=np.float64,
            ),
            -7.0,
        )
        expected_fixture_ic13 = np.array(
            [1.0, 2.0, 3.0, 3.0, -1.0, 4.0, 0.0, 3.0, 0.0, 1.0, -2.0, 5.0, -7.0],
            dtype=np.float64,
        )
        if not np.array_equal(fixture_ic13, expected_fixture_ic13):
            raise _ProducerContractViolation(
                "raw IC13 producer does not preserve the locked 13-slot order"
            )
        results["masses_ordered"] = (
            True,
            "resident producer emitted finite positive (3,) masses in raw-IC13 order",
        )
        results["IC13"] = (
            True,
            "resident producer emitted finite normalized/raw (13,) IC13 values",
        )
    except Exception as exc:
        failure = _producer_failure("IC13/masses_ordered", exc)
        results["masses_ordered"] = failure
        results["IC13"] = failure

    try:
        positions = _as_finite_array(
            source.snapshot_positions(key),
            name="snapshot_positions",
            shape=(None, 3, 3),
        )
        velocities = _as_finite_array(
            source.snapshot_velocities(key),
            name="snapshot_velocities",
            shape=(positions.shape[0], 3, 3),
        )
        times = _as_finite_array(
            source.snapshot_times(key),
            name="snapshot_times",
            shape=(positions.shape[0],),
        )
        if positions.shape[0] < 2 or np.any(np.diff(times) <= 0.0):
            raise _ProducerContractViolation(
                "snapshot series must contain at least two strictly ordered times"
            )
        if int(source.n_snapshots(key)) != positions.shape[0] or int(
            record.n_snapshots
        ) != positions.shape[0]:
            raise _ProducerContractViolation(
                "declared snapshot counts do not match resident positions"
            )
        points = sample_data_points(
            source,
            (key,),
            rng=np.random.default_rng(0),
            dtype=controller._dtype,
            device=controller._device,
            n_pts_cap=4,
        )
        targets = _as_finite_array(
            points.targets,
            name="data targets",
            shape=(len(points.record_keys), 9),
        )
        point_masses = _as_finite_array(
            points.masses,
            name="data masses",
            shape=(len(points.record_keys), 3),
        )
        point_inputs = _as_finite_array(
            points.tau_ic13,
            name="data tau_ic13",
            shape=(len(points.record_keys), 14),
        )
        if not (
            len(points.snapshot_indices)
            == len(points.sampling_kinds)
            == len(points.record_keys)
            == targets.shape[0]
        ):
            raise _ProducerContractViolation("data-point provenance lengths disagree")
        for index, (record_key, snapshot_index) in enumerate(
            zip(points.record_keys, points.snapshot_indices)
        ):
            if record_key != key:
                raise _ProducerContractViolation("data target record identity is misaligned")
            if not np.array_equal(targets[index], positions[snapshot_index].reshape(9)):
                raise _ProducerContractViolation(
                    "data target body/component order disagrees with snapshot provenance"
                )
            if not np.array_equal(point_masses[index], masses):
                raise _ProducerContractViolation("data masses disagree with record body order")
            if not np.array_equal(point_inputs[index, 1:], ic13):
                raise _ProducerContractViolation("data IC13 rows disagree with the record")
        results["target_positions"] = (
            True,
            f"batch producer emitted {targets.shape[0]} finite (9,) targets aligned to provenance",
        )
    except Exception as exc:
        results["target_positions"] = _producer_failure("target_positions", exc)

    try:
        model_input = torch.zeros(
            (1, 14), dtype=controller._dtype, device=controller._device
        )
        model_input[:, 1:] = torch.as_tensor(
            ic13, dtype=controller._dtype, device=controller._device
        )
        model_masses = torch.as_tensor(
            masses, dtype=controller._dtype, device=controller._device
        ).reshape(1, 3)
        predicted = controller.model(model_input, model_masses)
        _as_finite_array(
            predicted, name="predicted_positions", shape=(1, 9)
        )
        results["predicted_positions"] = (
            True,
            "model producer emitted finite (1,9) predicted positions",
        )
    except Exception as exc:
        results["predicted_positions"] = _producer_failure(
            "predicted_positions", exc
        )

    try:
        collocation = sample_collocation_points(
            source,
            (key,),
            rng=np.random.default_rng(1),
            dtype=controller._dtype,
            device=controller._device,
            collocation_count=2,
        )
        collocation_times = _as_finite_array(
            collocation.times, name="collocation times", shape=(2,)
        )
        collocation_inputs = _as_finite_array(
            collocation.tau_ic13, name="collocation tau_ic13", shape=(2, 14)
        )
        collocation_masses = _as_finite_array(
            collocation.masses, name="collocation masses", shape=(2, 3)
        )
        if tuple(collocation.record_keys) != (key, key):
            raise _ProducerContractViolation("collocation identities are misaligned")
        if not np.all(collocation_masses == masses) or not np.all(
            collocation_inputs[:, 1:] == ic13
        ):
            raise _ProducerContractViolation(
                "collocation masses/IC13 do not preserve record alignment"
            )
        if np.any(collocation_times < 0.0) or np.any(collocation_times > 10.0):
            raise _ProducerContractViolation("collocation times are outside [0,10]")
        results["collocation set"] = (
            True,
            "collocation producer emitted two finite aligned rows in [0,10]",
        )
    except Exception as exc:
        results["collocation set"] = _producer_failure("collocation set", exc)

    anchor_context = None
    try:
        anchor_batch = SimpleNamespace(
            replay_keys=(key,),
            lookahead_keys=(),
            data_points=SimpleNamespace(record_keys=(key,)),
        )
        fixed_times = np.array([2.5, 7.5], dtype=np.float64)
        anchor_context = controller._build_anchor_context(
            source, anchor_batch, fixed_times
        )
        true_r0 = _as_finite_array(
            anchor_context.true_r0, name="true_r0", shape=(3, 3)
        )
        true_v0 = _as_finite_array(
            anchor_context.true_v0, name="true_v0", shape=(3, 3)
        )
        anchor_masses = _as_finite_array(
            anchor_context.masses, name="anchor masses", shape=(3,)
        )
        h0 = _as_finite_array(anchor_context.h0, name="h0", shape=())
        l0 = _as_finite_array(anchor_context.l0, name="l0", shape=(3,))
        anchor_times = _as_finite_array(
            anchor_context.collocation_times,
            name="anchor collocation times",
            shape=(2,),
        )
        expected_positions = _as_finite_array(
            source.snapshot_positions(key),
            name="anchor source positions",
            shape=(None, 3, 3),
        )
        expected_velocities = _as_finite_array(
            source.snapshot_velocities(key),
            name="anchor source velocities",
            shape=(expected_positions.shape[0], 3, 3),
        )
        if not np.array_equal(true_r0, expected_positions[0]):
            raise _ProducerContractViolation("true_r0 is not source snapshot zero")
        results["true_r0"] = (True, "anchor producer emitted finite aligned (3,3) true_r0")
        if not np.array_equal(true_v0, expected_velocities[0]):
            raise _ProducerContractViolation("true_v0 is not source snapshot zero")
        results["true_v0"] = (True, "anchor producer emitted finite aligned (3,3) true_v0")
        if not np.array_equal(anchor_masses, masses):
            raise _ProducerContractViolation("anchor masses do not preserve body order")
        results["h0"] = (True, f"anchor producer emitted finite scalar h0 ({h0.shape!r})")
        results["l0"] = (True, f"anchor producer emitted finite (3,) l0 ({l0.shape!r})")
        if not np.array_equal(anchor_times, fixed_times):
            raise _ProducerContractViolation("anchor collocation ordering changed")
    except Exception as exc:
        failure = _producer_failure("anchor context", exc)
        for name in ("true_r0", "true_v0", "h0", "l0"):
            results[name] = failure

    if anchor_context is not None:
        try:
            terms = controller._non_data_terms(anchor_context)
            if not isinstance(terms, Mapping) or set(terms) != {
                "ic",
                "phys",
                "energy",
                "angmom",
            }:
                raise _ProducerContractViolation("non-data term mapping is incomplete")
            for name, value in terms.items():
                _as_finite_array(value, name=f"{name} loss", shape=())
            details = controller._last_widened_details
            if not isinstance(details, Mapping):
                raise _ProducerContractViolation("non-data producer omitted residual details")
            residuals = _as_finite_array(
                details.get("residuals_per_bin"), name="Rbar", shape=(2,)
            )
            results["Rbar"] = (
                True,
                f"non-data producer emitted {residuals.shape[0]} finite Rbar values",
            )
        except Exception as exc:
            results["Rbar"] = _producer_failure("Rbar", exc)

    return results


def _probe(
    item: Mapping[str, Any],
    config: Any,
    scheduler: Any,
    metadata: Mapping[str, Any],
    producer_contracts: Mapping[str, tuple[bool, str]],
) -> tuple[bool, str]:
    probe = item["probe"]
    kind = probe["kind"]
    if kind == "placeholder":
        return False, "probe resolves to a class-4 placeholder"
    if kind == "missing":
        return False, "probe resolves to nothing"
    if kind == "producer":
        return producer_contracts.get(
            probe["name"],
            (False, f"producer contract {probe['name']!r} is not registered"),
        )
    if kind == "constant":
        try:
            module = importlib.import_module(probe["module"])
            value = getattr(module, probe["name"])
        except (ImportError, AttributeError) as exc:
            return False, f"constant unavailable: {exc}"
        if "expected" in probe and value != probe["expected"]:
            return False, f"expected {probe['expected']!r}, got {value!r}"
        if isinstance(value, (tuple, list)):
            if not value or not all(_finite(item, positive=bool(probe.get("positive"))) for item in value):
                return False, f"constant is not a finite sequence: {value!r}"
        elif not _finite(value, positive=bool(probe.get("positive"))):
            return False, f"constant is not finite/positive: {value!r}"
        if "length" in probe and len(value) != probe["length"]:
            return False, f"expected length {probe['length']}, got {len(value)}"
        return True, f"constant {probe['name']}={value!r}"
    if kind == "loss_default":
        from dataclasses import fields

        field = next((field for field in fields(LossWeights) if field.name == probe["name"]), None)
        if field is None or field.default != probe.get("expected"):
            return False, f"LossWeights.{probe['name']} default is not {probe.get('expected')!r}"
        return True, f"LossWeights.{probe['name']} default={field.default!r}"
    if kind == "signature_default":
        try:
            function = getattr(importlib.import_module(probe["module"]), probe["name"])
            default = inspect.signature(function).parameters[probe["parameter"]].default
        except (ImportError, AttributeError, KeyError, ValueError) as exc:
            return False, f"signature probe unavailable: {exc}"
        if default != probe.get("expected"):
            return False, f"expected default {probe.get('expected')!r}, got {default!r}"
        return True, "house-style function default resolves"
    if kind == "schedule_state":
        state = scheduler.state_dict() if hasattr(scheduler, "state_dict") else {}
        name = probe["name"]
        if name not in state:
            return False, f"ScheduledWeights.state_dict missing {name}"
        value = state[name]
        if "expected" in probe and value != probe["expected"] and not probe.get("advisory"):
            return False, f"expected {probe['expected']!r}, got {value!r}"
        if not _finite(value) or (name == "warmup_length" and float(value) < 0.0):
            return False, f"schedule value is not finite: {value!r}"
        return True, f"schedule {name}={value!r}"
    if kind == "metadata":
        missing = [key for key in probe["keys"] if key not in metadata]
        return (not missing, f"metadata keys present: {list(probe['keys'])}" if not missing else f"missing metadata keys: {missing}")
    if kind == "metadata_product":
        missing = [key for key in probe["keys"] if key not in metadata]
        if missing:
            return False, f"missing metadata keys: {missing}"
        try:
            valid = float(metadata["eps_h"]) == float(metadata["energy_floor_factor"]) * float(metadata["s_h"])
        except (TypeError, ValueError):
            valid = False
        return valid, "eps_h equals energy_floor_factor * s_h" if valid else "eps_h product mismatch"
    if kind == "config":
        try:
            value = _get_path(config, probe["path"])
        except AttributeError as exc:
            return False, f"config path unavailable: {exc}"
        if not _finite(value, positive=bool(probe.get("positive"))):
            return False, f"config value is not finite/positive: {value!r}"
        if "expected" in probe and value != probe["expected"]:
            return False, f"expected {probe['expected']!r}, got {value!r}"
        return True, f"config {'.'.join(probe['path'])}={value!r}"
    raise ValueError(f"unknown census probe kind {kind!r}")


def _findings(
    config: Any,
    entries: Sequence[Mapping[str, Any]],
    provisional: Sequence[Mapping[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    if provisional is None:
        try:
            provisional = config.provisional_fields()
        except (AttributeError, TypeError):
            provisional = ()
    by_quantity = {item["quantity"]: item for item in entries}
    for field in provisional:
        if not isinstance(field, Mapping):
            continue
        name = field.get("name")
        quantity = "energy_floor_factor" if name == "stage.energy_floor_factor" else None
        if quantity is None or quantity not in by_quantity:
            continue
        item = by_quantity[quantity]
        if field.get("provisional") is True and item["expected_class"] != "placeholder":
            findings.append(
                {
                    "kind": "classification-disagreement",
                    "quantity": quantity,
                    "manifest_class": item["expected_class"],
                    "provisional": True,
                    "provenance": field.get("provenance"),
                }
            )
    findings.append(
        {
            "kind": "house-style",
            "quantity": "beta_v",
            "manifest_class": "spec-constant",
            "detail": "beta_v resolves from a loss_catalog function default rather than pinn.constants",
        }
    )
    return findings


def _instrumentation_finding() -> tuple[bool, str]:
    missing = [name for name in _REQUIRED_INSTRUMENTATION if name not in STEP_LOG_FIELDS]
    if missing:
        return False, f"instrumentation STEP_LOG_FIELDS missing: {missing}"
    return True, f"instrumentation registry contains {len(_REQUIRED_INSTRUMENTATION)} required fields"


def run_census(
    config: Any,
    scheduled_weights: Any,
    metadata: Mapping[str, Any],
    provisional: Sequence[Mapping[str, Any]] | None = None,
    *,
    controller: Any,
) -> dict[str, Any]:
    """Resolve every explicit manifest entry against validated setup inputs."""

    manifest = CENSUS_MANIFEST
    if not manifest:
        raise ValueError("census manifest is empty; no quantity can pass")
    if not isinstance(metadata, Mapping):
        raise ValueError("census metadata must be a validated mapping")

    producer_contracts = _producer_contracts(controller)
    records: list[dict[str, Any]] = []
    for item in manifest:
        resolved, detail = _probe(
            item, config, scheduled_weights, metadata, producer_contracts
        )
        records.append(
            {
                "quantity": item["quantity"],
                "spec_citation": item["spec_citation"],
                "expected_class": item["expected_class"],
                "resolved": bool(resolved),
                "detail": detail,
            }
        )
    findings = _findings(config, manifest, provisional)
    instrumentation_ok, instrumentation_detail = _instrumentation_finding()
    findings.append(
        {
            "kind": "instrumentation",
            "quantity": "STEP_LOG_FIELDS",
            "detail": instrumentation_detail,
            "resolved": instrumentation_ok,
        }
    )

    report: dict[str, Any] = {
        "entries": records,
        "findings": findings,
        "verdict": "passed",
    }
    for item, record in zip(manifest, records):
        if item["expected_class"] == "placeholder" and not record["resolved"]:
            waiver = item.get("waiver")
            if not waiver:
                report["verdict"] = "blocked"
                raise CensusBlockError(
                    f"census quantity {item['quantity']!r} is a class-4 placeholder "
                    "without an explicit waiver citation",
                    report,
                )
        elif not record["resolved"]:
            report["verdict"] = "blocked"
            raise CensusBlockError(
                f"census quantity {item['quantity']!r} did not resolve in its "
                f"expected class {item['expected_class']!r}: {record['detail']}",
                report,
            )
    if not instrumentation_ok:
        report["verdict"] = "blocked"
        raise CensusBlockError(
            f"census instrumentation precondition failed: {instrumentation_detail}",
            report,
        )
    return report
