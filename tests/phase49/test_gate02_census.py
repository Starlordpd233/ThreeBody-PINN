"""GATE-02 explicit-manifest census coverage."""

from __future__ import annotations

import json
from types import SimpleNamespace

import pytest
import torch

from pinn.conformance import census
from pinn.loss_catalog import resolve_causal_clip_facts
from pinn.training.scheduled_weights import ScheduledWeights


def _config(*, provisional=None, n_adam=1000):
    stage = SimpleNamespace(n_adam=n_adam, energy_floor_factor=1e-4)
    if provisional is None:
        provisional = [
            {
                "name": "stage.energy_floor_factor",
                "value": 1e-4,
                "provisional": True,
                "provenance": "fixture stale provisional tag",
            }
        ]
    return SimpleNamespace(stage=stage, provisional_fields=lambda: provisional)


def _metadata():
    facts = resolve_causal_clip_facts(torch.float64, torch.device("cpu"))
    return {
        "s_h": 5.0,
        "eps_h": 5e-4,
        "n_train": 3,
        "energy_floor_factor": 1e-4,
        "eps_train": 1e-5,
        **facts,
    }


def _scheduler():
    return ScheduledWeights(1000, lambda_e_max=0.0, lambda_l_max=0.0)


def test_census_passes_with_real_manifest_and_validated_metadata():
    report = census.run_census(_config(), _scheduler(), _metadata())
    assert report["verdict"] == "passed"
    assert len(report["entries"]) == len(census.CENSUS_MANIFEST)
    assert all(item["resolved"] for item in report["entries"])


def test_census_manifest_is_complete_and_declaration_ordered():
    quantities = [item["quantity"] for item in census.CENSUS_MANIFEST]
    assert len(quantities) == 28
    assert len(quantities) == len(set(quantities))
    assert quantities[:4] == [
        "predicted_positions",
        "target_positions",
        "HUBER_DELTA_DATA",
        "lambda_data",
    ]
    assert "S_H" in quantities
    assert "D-01 table" in quantities


def test_placeholder_blocks_without_explicit_waiver(monkeypatch):
    injected = {
        "quantity": "injected_placeholder",
        "term": "L_E",
        "spec_citation": "fixture §4",
        "expected_class": "placeholder",
        "probe": {"kind": "missing"},
    }
    monkeypatch.setattr(census, "CENSUS_MANIFEST", census.CENSUS_MANIFEST + (injected,))
    with pytest.raises(ValueError, match="injected_placeholder.*placeholder"):
        census.run_census(_config(), _scheduler(), _metadata())


def test_provisional_disagreement_is_recorded_without_blocking():
    report = census.run_census(_config(), _scheduler(), _metadata())
    findings = report["findings"]
    energy = [finding for finding in findings if finding.get("quantity") == "energy_floor_factor"]
    assert energy
    assert energy[0]["manifest_class"] == "spec-constant"
    assert energy[0]["provisional"] is True
    beta = [finding for finding in findings if finding.get("quantity") == "beta_v"]
    assert beta and beta[0]["kind"] == "house-style"


def test_instrumentation_preconditions_trip_when_registry_field_is_missing(monkeypatch):
    fields = dict(census.STEP_LOG_FIELDS)
    fields.pop("grad_stats_complete")
    monkeypatch.setattr(census, "STEP_LOG_FIELDS", fields)
    with pytest.raises(ValueError, match="instrumentation.*grad_stats_complete"):
        census.run_census(_config(), _scheduler(), _metadata())


def test_empty_manifest_fails_loud(monkeypatch):
    monkeypatch.setattr(census, "CENSUS_MANIFEST", ())
    with pytest.raises(ValueError, match="manifest.*empty"):
        census.run_census(_config(), _scheduler(), _metadata())


def test_census_serialization_is_byte_stable_and_preserves_order():
    first = census.run_census(_config(), _scheduler(), _metadata())
    second = census.run_census(_config(), _scheduler(), _metadata())
    assert [item["quantity"] for item in first["entries"]] == [
        item["quantity"] for item in second["entries"]
    ]
    assert json.dumps(first, sort_keys=True, indent=2) == json.dumps(
        second, sort_keys=True, indent=2
    )
