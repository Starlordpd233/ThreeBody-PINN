"""GATE-02 explicit-manifest census coverage."""

from __future__ import annotations

import json
from types import MethodType
from types import SimpleNamespace

import numpy as np
import pytest
import torch

from pinn.conformance import census
from pinn.data import preprocessing
from pinn.loss_catalog import resolve_causal_clip_facts
from pinn.training.scheduled_weights import ScheduledWeights
from tests.phase49._producer_fixture import make_producer_controller


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


@pytest.fixture
def producer_controller(tmp_path):
    return make_producer_controller(tmp_path)


def _run_census(controller, *, config=None, scheduler=None, metadata=None):
    return census.run_census(
        config or _config(),
        scheduler or _scheduler(),
        metadata or _metadata(),
        controller=controller,
    )


def _entry(report, quantity):
    return next(item for item in report["entries"] if item["quantity"] == quantity)


def test_census_passes_with_real_manifest_and_validated_metadata(producer_controller):
    report = _run_census(producer_controller)
    assert report["verdict"] == "passed"
    assert len(report["entries"]) == len(census.CENSUS_MANIFEST)
    assert all(item["resolved"] for item in report["entries"])
    assert "resolves to" not in _entry(report, "target_positions")["detail"]


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


def test_placeholder_blocks_without_explicit_waiver(monkeypatch, producer_controller):
    injected = {
        "quantity": "injected_placeholder",
        "term": "L_E",
        "spec_citation": "fixture §4",
        "expected_class": "placeholder",
        "probe": {"kind": "missing"},
    }
    monkeypatch.setattr(census, "CENSUS_MANIFEST", census.CENSUS_MANIFEST + (injected,))
    with pytest.raises(ValueError, match="injected_placeholder.*placeholder"):
        _run_census(producer_controller)


def test_provisional_disagreement_is_recorded_without_blocking(producer_controller):
    report = _run_census(producer_controller)
    findings = report["findings"]
    energy = [finding for finding in findings if finding.get("quantity") == "energy_floor_factor"]
    assert energy
    assert energy[0]["manifest_class"] == "spec-constant"
    assert energy[0]["provisional"] is True
    beta = [finding for finding in findings if finding.get("quantity") == "beta_v"]
    assert beta and beta[0]["kind"] == "house-style"


def test_instrumentation_preconditions_trip_when_registry_field_is_missing(
    monkeypatch, producer_controller
):
    fields = dict(census.STEP_LOG_FIELDS)
    fields.pop("grad_stats_complete")
    monkeypatch.setattr(census, "STEP_LOG_FIELDS", fields)
    with pytest.raises(ValueError, match="instrumentation.*grad_stats_complete"):
        _run_census(producer_controller)


def test_empty_manifest_fails_loud(monkeypatch, producer_controller):
    monkeypatch.setattr(census, "CENSUS_MANIFEST", ())
    with pytest.raises(ValueError, match="manifest.*empty"):
        _run_census(producer_controller)


def test_census_serialization_is_byte_stable_and_preserves_order(producer_controller):
    first = _run_census(producer_controller)
    second = _run_census(producer_controller)
    assert [item["quantity"] for item in first["entries"]] == [
        item["quantity"] for item in second["entries"]
    ]
    assert json.dumps(first, sort_keys=True, indent=2) == json.dumps(
        second, sort_keys=True, indent=2
    )


def test_nonfinite_target_positions_block_the_census(monkeypatch, producer_controller):
    source = producer_controller._train_source
    original = source.snapshot_positions

    def nonfinite_positions(key):
        return np.full_like(original(key), np.nan)

    monkeypatch.setattr(source, "snapshot_positions", nonfinite_positions)
    with pytest.raises(census.CensusBlockError, match="target_positions") as caught:
        _run_census(producer_controller)
    assert _entry(caught.value.report, "target_positions")["resolved"] is False


def test_raw_ic13_body_order_mismatch_blocks_the_census(
    monkeypatch, producer_controller
):
    source = producer_controller._train_source
    original = source.get

    def misordered_record(key):
        record = original(key)
        record.raw_ic13 = np.asarray(record.raw_ic13).copy()
        record.raw_ic13[:3] = record.raw_ic13[:3][::-1]
        return record

    monkeypatch.setattr(source, "get", misordered_record)
    with pytest.raises(census.CensusBlockError, match="IC13") as caught:
        _run_census(producer_controller)
    assert _entry(caught.value.report, "IC13")["resolved"] is False


def test_ic13_slot_order_corruption_in_the_producer_blocks_the_census(
    monkeypatch, producer_controller
):
    original = preprocessing.build_raw_ic13

    def misordered_ic13(*args, **kwargs):
        value = original(*args, **kwargs)
        return value[[0, 1, 2, 4, 3, 5, 6, 7, 8, 9, 10, 11, 12]]

    monkeypatch.setattr(preprocessing, "build_raw_ic13", misordered_ic13)
    with pytest.raises(census.CensusBlockError, match="IC13") as caught:
        _run_census(producer_controller)
    assert "slot order" in _entry(caught.value.report, "IC13")["detail"]


def test_missing_raw_ic13_contract_field_blocks_the_census(
    monkeypatch, producer_controller
):
    source = producer_controller._train_source
    original = source.get

    def record_without_raw_ic13(key):
        record = original(key)
        del record.raw_ic13
        return record

    monkeypatch.setattr(source, "get", record_without_raw_ic13)
    with pytest.raises(census.CensusBlockError, match="IC13") as caught:
        _run_census(producer_controller)
    assert _entry(caught.value.report, "IC13")["resolved"] is False


def test_anchor_producer_exception_blocks_instead_of_escaping(
    monkeypatch, producer_controller
):
    def broken_anchor(self, source, batch, fixed_collocation_times):
        raise OSError("injected anchor producer failure")

    monkeypatch.setattr(
        producer_controller,
        "_build_anchor_context",
        MethodType(broken_anchor, producer_controller),
    )
    with pytest.raises(census.CensusBlockError, match="true_r0") as caught:
        _run_census(producer_controller)
    assert "OSError" in _entry(caught.value.report, "true_r0")["detail"]


def test_nonfinite_rbar_from_non_data_producer_blocks_the_census(
    monkeypatch, producer_controller
):
    def nonfinite_non_data(self, anchor_ctx):
        self._last_widened_details = {"residuals_per_bin": [float("nan")]}
        zero = torch.zeros((), dtype=self._dtype, device=self._device)
        return {name: zero for name in ("ic", "phys", "energy", "angmom")}

    monkeypatch.setattr(
        producer_controller,
        "_non_data_terms",
        MethodType(nonfinite_non_data, producer_controller),
    )
    with pytest.raises(census.CensusBlockError, match="Rbar") as caught:
        _run_census(producer_controller)
    assert _entry(caught.value.report, "Rbar")["resolved"] is False
