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
from typing import Any

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
    _item("predicted_positions", "L_data", "pinn_architecture.md §3.1", "derived", {"kind": "symbol", "module": "pinn.training.controllers", "name": "RunController._compose_loss_terms"}),
    _item("target_positions", "L_data", "pinn_architecture.md §3.1", "pipeline", {"kind": "symbol", "module": "pinn.data.adapter", "name": "AdmittedSetAdapter"}),
    _item("HUBER_DELTA_DATA", "L_data", "pinn_architecture.md §3.1", "spec-constant", {"kind": "constant", "module": "pinn.constants", "name": "HUBER_DELTA_DATA", "expected": 1.0}),
    _item("lambda_data", "L_data", "pinn_architecture.md §3.1", "spec-constant", {"kind": "loss_default", "name": "lambda_data", "expected": 1.0}),
    _item("true_r0", "L_IC", "pinn_architecture.md §3.3", "derived", {"kind": "symbol", "module": "pinn.training.controllers", "name": "RunController._build_anchor_context"}),
    _item("true_v0", "L_IC", "pinn_architecture.md §3.3", "derived", {"kind": "symbol", "module": "pinn.training.controllers", "name": "RunController._build_anchor_context"}),
    _item("IC13", "L_IC", "pinn_architecture.md §3.3", "pipeline", {"kind": "symbol", "module": "pinn.data.types", "name": "AdmittedRecord"}),
    _item("beta_v", "L_IC", "pinn_architecture.md §3.3", "spec-constant", {"kind": "signature_default", "module": "pinn.loss_catalog", "name": "ic_anchor_loss", "parameter": "beta_v", "expected": 1.0}),
    _item("lambda_ic", "L_IC", "pinn_architecture.md §4.1", "spec-constant", {"kind": "schedule_state", "name": "lambda_ic", "expected": 1.0, "advisory": True}),
    _item("masses_ordered", "L_phys^causal", "pinn_architecture.md §3.2", "pipeline", {"kind": "symbol", "module": "pinn.data.adapter", "name": "AdmittedSetAdapter"}),
    _item("EPS_SOFT", "L_phys^causal", "pinn_architecture.md §3.2", "spec-constant", {"kind": "constant", "module": "pinn.constants", "name": "EPS_SOFT", "expected": 1e-5}),
    _item("eta_c", "L_phys^causal", "pinn_architecture.md §3.2", "spec-constant", {"kind": "constant", "module": "pinn.constants", "name": "CAUSAL_ETA_C", "expected": 1.0}),
    _item("causal_clip_facts", "L_phys^causal", "pinn_architecture.md §4.1", "derived", {"kind": "metadata", "keys": CAUSAL_CLIP_FIELD_NAMES}),
    _item("D_CHARACTERISTIC_LENGTH", "L_phys^causal", "ctl_instruction.md §2.5", "spec-constant", {"kind": "constant", "module": "pinn.constants", "name": "D_CHARACTERISTIC_LENGTH", "positive": True}),
    _item("T_CHARACTERISTIC_TIME", "L_phys^causal", "pinn_architecture.md Table 2", "spec-constant", {"kind": "constant", "module": "pinn.constants", "name": "T_CHARACTERISTIC_TIME", "expected": 10.0}),
    _item("Rbar", "L_phys^causal", "pinn_architecture.md §3.2", "derived", {"kind": "symbol", "module": "pinn.training.controllers", "name": "RunController._non_data_terms"}),
    _item("collocation set", "L_phys^causal", "ctl_instruction.md LOOP-02 / LOOP-06", "pipeline", {"kind": "symbol", "module": "pinn.training.collocation_sampler", "name": "CollocationSampler"}),
    _item("S_H", "L_E", "pinn_architecture.md §3.4", "pipeline", {"kind": "metadata", "keys": ("s_h", "n_train")}),
    _item("eps_H", "L_E", "pinn_architecture.md §3.4", "derived", {"kind": "metadata_product", "keys": ("eps_h", "s_h", "energy_floor_factor")}),
    _item("energy_floor_factor", "L_E", "pinn_architecture.md §3.4", "spec-constant", {"kind": "config", "path": ("stage", "energy_floor_factor"), "expected": 1e-4}),
    _item("h0", "L_E", "pinn_architecture.md §3.4", "derived", {"kind": "symbol", "module": "pinn.training.controllers", "name": "RunController._build_anchor_context"}),
    _item("HUBER_DELTA_ENERGY", "L_E", "pinn_architecture.md §3.4", "spec-constant", {"kind": "constant", "module": "pinn.constants", "name": "HUBER_DELTA_ENERGY", "expected": 1.0}),
    _item("l0", "L_L", "pinn_architecture.md §3.5", "derived", {"kind": "symbol", "module": "pinn.training.controllers", "name": "RunController._build_anchor_context"}),
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


class CensusBlockError(ValueError):
    """A census refusal carrying the report that must be persisted first."""

    def __init__(self, message: str, report: dict[str, Any]):
        super().__init__(message)
        self.report = report


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


def _symbol(module_name: str, dotted_name: str) -> tuple[bool, str]:
    try:
        module = importlib.import_module(module_name)
        value: Any = module
        for part in dotted_name.split("."):
            value = getattr(value, part)
    except (ImportError, AttributeError) as exc:
        return False, f"{module_name}.{dotted_name} unavailable: {exc}"
    return True, f"{module_name}.{dotted_name} resolves to {type(value).__name__}"


def _probe(item: Mapping[str, Any], config: Any, scheduler: Any, metadata: Mapping[str, Any]) -> tuple[bool, str]:
    probe = item["probe"]
    kind = probe["kind"]
    if kind == "placeholder":
        return False, "probe resolves to a class-4 placeholder"
    if kind == "missing":
        return False, "probe resolves to nothing"
    if kind == "symbol":
        return _symbol(probe["module"], probe["name"])
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
        if not _finite(value, positive=(name == "warmup_length")):
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


def _findings(config: Any, entries: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
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
) -> dict[str, Any]:
    """Resolve every explicit manifest entry against validated setup inputs."""

    del provisional  # the config method is the canonical cross-check source
    manifest = CENSUS_MANIFEST
    if not manifest:
        raise ValueError("census manifest is empty; no quantity can pass")
    if not isinstance(metadata, Mapping):
        raise ValueError("census metadata must be a validated mapping")

    records: list[dict[str, Any]] = []
    for item in manifest:
        resolved, detail = _probe(item, config, scheduled_weights, metadata)
        records.append(
            {
                "quantity": item["quantity"],
                "spec_citation": item["spec_citation"],
                "expected_class": item["expected_class"],
                "resolved": bool(resolved),
                "detail": detail,
            }
        )
    findings = _findings(config, manifest)
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
