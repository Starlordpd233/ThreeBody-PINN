"""INST-03 fail-closed divergence-register and proof-test coverage."""

from __future__ import annotations

import json
import copy
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

import pytest
import torch

from pinn.conformance import census, preflight
from pinn.conformance import register
from pinn.loss_catalog import resolve_causal_clip_facts
from pinn.training.run_metadata import write_training_metadata
from pinn.training.scheduled_weights import ScheduledWeights


def _entry(*, status: str = "open", **overrides):
    value = {
        "id": "X-1",
        "kind": "divergence",
        "status": status,
        "title": "fixture",
        "spec_citation": "fixture §1",
        "authority": "test fixture",
        "rationale": "fixture rationale",
        "what_it_would_take": "fixture closure",
        "proof_test": None,
        "waiver": None,
    }
    value.update(overrides)
    if status == "closed" and "proof_test" not in overrides:
        value["proof_test"] = "tests/phase48/test_stage0_energy_config.py::test_loss_config_default_drives_stage0_zero_schedule"
    return value


def _write(tmp_path: Path, payload) -> Path:
    path = tmp_path / register.DIVERGENCE_REGISTER_FILENAME
    text = payload if isinstance(payload, str) else json.dumps(payload)
    path.write_text(text, encoding="utf-8")
    return path


def _payload(*entries):
    return {"schema_version": register.REGISTER_SCHEMA_VERSION, "entries": list(entries)}


@pytest.mark.parametrize(
    ("name", "setup", "pattern"),
    [
        ("missing", lambda tmp: tmp / "absent.json", "not found"),
        ("malformed", lambda tmp: _write(tmp, "{"), "not valid JSON"),
        ("non_object", lambda tmp: _write(tmp, []), "JSON object"),
        (
            "wrong_keys",
            lambda tmp: _write(tmp, {"schema_version": 1, "entries": [], "extra": 1}),
            "keys must be exactly",
        ),
        (
            "wrong_version",
            lambda tmp: _write(tmp, {"schema_version": 999, "entries": []}),
            "schema_version",
        ),
        (
            "unknown_kind",
            lambda tmp: _write(tmp, _payload(_entry(kind="mystery"))),
            "unknown kind",
        ),
        (
            "unknown_status",
            lambda tmp: _write(tmp, _payload(_entry(status="mystery"))),
            "unknown status",
        ),
        (
            "duplicate_id",
            lambda tmp: _write(tmp, _payload(_entry(), _entry(id="X-1"))),
            "duplicate id",
        ),
        (
            "closed_without_proof",
            lambda tmp: _write(tmp, _payload(_entry(status="closed", proof_test=None))),
            "closed.*proof_test",
        ),
        (
            "waived_without_authority",
            lambda tmp: _write(tmp, _payload(_entry(status="waived"))),
            "waived.*waiver",
        ),
    ],
)
def test_schema_rejections_are_distinct(tmp_path, name, setup, pattern):
    path = setup(tmp_path)
    with pytest.raises(ValueError, match=pattern):
        register.load_divergence_register(path)


def test_empty_schema_valid_register_loads(tmp_path):
    path = _write(tmp_path, _payload())
    assert register.load_divergence_register(path)["entries"] == []


def test_duplicate_ids_are_rejected_even_when_entries_differ(tmp_path):
    path = _write(tmp_path, _payload(_entry(), _entry(id="X-1", title="different")))
    with pytest.raises(ValueError, match="duplicate id"):
        register.load_divergence_register(path)


def test_committed_register_has_mandatory_entries_and_authorized_waivers():
    payload = register.load_divergence_register()
    by_id = {entry["id"]: entry for entry in payload["entries"]}
    assert {
        "CONF-01-QUALIFICATION",
        "PLAT-01-SINGLE-STAGE",
        "PLAT-02-SLBFGS",
        "INV-B-N-UNSET",
    } <= set(by_id)
    assert by_id["INV-B-N-UNSET"]["kind"] == "divergence"
    assert by_id["INV-B-N-UNSET"]["status"] == "open"
    assert by_id["INV-B-N-UNSET"]["waiver"] is None
    assert by_id["PLAT-01-SINGLE-STAGE"]["waiver"] == "SCOPE-27"
    assert "SCOPE-27" in by_id["PLAT-02-SLBFGS"]["waiver"]
    assert "EVAL-01" in by_id["CONF-01-QUALIFICATION"]["rationale"]
    assert "measured" in by_id["CONF-01-QUALIFICATION"]["rationale"]


def test_every_closed_register_entry_has_a_real_passing_proof_test():
    payload = register.load_divergence_register()
    closed = [entry for entry in payload["entries"] if entry["status"] == "closed"]
    assert closed
    for entry in closed:
        node = entry["proof_test"]
        assert node
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", node],
            cwd=Path(__file__).parents[2],
            text=True,
            capture_output=True,
            check=False,
        )
        assert result.returncode == 0, f"{entry['id']} proof failed:\n{result.stdout}\n{result.stderr}"


def test_register_serialization_is_deterministic(tmp_path):
    payload = _payload(_entry())
    first = tmp_path / "first.json"
    second = tmp_path / "second.json"
    register.write_divergence_register(first, payload)
    register.write_divergence_register(second, payload)
    assert first.read_bytes() == second.read_bytes()


def _preflight_config(n=None):
    return SimpleNamespace(
        stage=SimpleNamespace(n_adam=1000, energy_floor_factor=1e-4),
        invariants=SimpleNamespace(front_advance_window_n=n),
        provisional_fields=lambda: [
            {
                "name": "stage.energy_floor_factor",
                "value": 1e-4,
                "provisional": True,
                "provenance": "fixture",
            }
        ],
    )


def _preflight_run_dir(path: Path):
    path.mkdir()
    facts = resolve_causal_clip_facts(torch.float64, torch.device("cpu"))
    write_training_metadata(
        path,
        s_h=5.0,
        n_train=3,
        energy_floor_factor=1e-4,
        causal_clip_facts=facts,
    )
    return facts


def _walk_keys(value):
    if isinstance(value, dict):
        for key, child in value.items():
            yield key
            yield from _walk_keys(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_keys(child)


def test_preflight_composes_census_and_every_open_register_entry(tmp_path):
    run_dir = tmp_path / "run"
    _preflight_run_dir(run_dir)
    record = preflight.run_start_preflight(
        _preflight_config(), ScheduledWeights(1000, lambda_e_max=0.0), run_dir
    )
    assert record.events[0]["census"]["verdict"] == "passed"
    expected = [entry for entry in register.load_divergence_register()["entries"] if entry["status"] == "open"]
    assert record.events[0]["open_divergences"] == expected
    assert record.events[0]["findings"]
    payload = preflight.load_preflight(run_dir)
    assert payload["assertions"][0]["open_divergences"] == expected


def test_refusal_writes_failing_census_artifact_before_raise(tmp_path):
    run_dir = tmp_path / "run"
    _preflight_run_dir(run_dir)
    failure_report = {"entries": [], "findings": [], "verdict": "blocked"}
    error = census.CensusBlockError("injected placeholder", failure_report)
    with mock.patch.object(preflight, "run_census", side_effect=error):
        with pytest.raises(ValueError, match="injected placeholder"):
            preflight.run_start_preflight(
                _preflight_config(), ScheduledWeights(1000, lambda_e_max=0.0), run_dir
            )
    payload = preflight.load_preflight(run_dir)
    assert payload["preflight_status"] == "failed"
    assert payload["assertions"][0]["census"] == failure_report


def test_no_gate_collision_in_preflight_and_register_payload(tmp_path):
    run_dir = tmp_path / "run"
    _preflight_run_dir(run_dir)
    preflight.run_start_preflight(
        _preflight_config(), ScheduledWeights(1000, lambda_e_max=0.0), run_dir
    )
    payload = preflight.load_preflight(run_dir)
    register_payload = register.load_divergence_register()
    assert not [key for key in _walk_keys(payload) if isinstance(key, str) and key.startswith("gate_")]
    assert not [key for key in _walk_keys(register_payload) if isinstance(key, str) and key.startswith("gate_")]


def test_preflight_bytes_are_idempotent_for_identical_inputs(tmp_path):
    first_dir = tmp_path / "first"
    second_dir = tmp_path / "second"
    _preflight_run_dir(first_dir)
    _preflight_run_dir(second_dir)
    scheduler_a = ScheduledWeights(1000, lambda_e_max=0.0)
    scheduler_b = ScheduledWeights(1000, lambda_e_max=0.0)
    preflight.run_start_preflight(_preflight_config(), scheduler_a, first_dir)
    preflight.run_start_preflight(_preflight_config(), scheduler_b, second_dir)
    assert (first_dir / preflight.PREFLIGHT_FILENAME).read_bytes() == (
        second_dir / preflight.PREFLIGHT_FILENAME
    ).read_bytes()


@pytest.mark.parametrize("n,closed", [(50, False), (None, True)])
def test_n_register_consistency_is_a_finding_not_a_block(tmp_path, monkeypatch, n, closed):
    run_dir = tmp_path / "run"
    _preflight_run_dir(run_dir)
    base = register.load_divergence_register()
    modified = copy.deepcopy(base)
    entry = next(item for item in modified["entries"] if item["id"] == "INV-B-N-UNSET")
    entry["status"] = "closed" if closed else "open"
    entry["proof_test"] = (
        "tests/phase49/test_gate03_invariants.py::test_invariant_b_n_unset_record_only_still_tracks_state"
        if closed
        else None
    )
    monkeypatch.setattr(preflight, "load_divergence_register", lambda: modified)
    record = preflight.run_start_preflight(
        _preflight_config(n), ScheduledWeights(1000, lambda_e_max=0.0), run_dir
    )
    assert any(finding.get("kind") == "consistency" for finding in record.events[0]["findings"])
