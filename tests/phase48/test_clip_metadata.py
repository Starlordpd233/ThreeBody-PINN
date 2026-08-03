"""Strict causal-clip provenance and fresh/resume lifecycle tests."""

from __future__ import annotations

import json

import pytest
import torch

from pinn.loss_catalog import resolve_causal_clip_facts
from pinn.train import _assert_s_h_matches_artifact
from pinn.training.run_metadata import (
    TRAINING_METADATA_FILENAME,
    load_training_metadata,
    write_training_metadata,
)


class _Source:
    def __init__(self):
        self._rows = {"a": (1.0, 2.0), "b": (3.0, 4.0)}

    def records_at_or_below(self, stage):
        assert stage == 0
        return tuple(self._rows)

    def k0(self, key):
        return self._rows[key][0]

    def uabs0(self, key):
        return self._rows[key][1]


def _write_pristine(run_dir):
    facts = resolve_causal_clip_facts(torch.float64, torch.device("cpu"))
    write_training_metadata(
        run_dir,
        s_h=5.0,
        n_train=2,
        energy_floor_factor=1e-4,
        causal_clip_facts=facts,
    )
    path = run_dir / TRAINING_METADATA_FILENAME
    return path, json.loads(path.read_text(encoding="utf-8")), facts


def test_causal_clip_fresh_metadata_roundtrip(tmp_path):
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    source = _Source()
    facts = resolve_causal_clip_facts(torch.float64, torch.device("cpu"))

    write_training_metadata(
        run_dir,
        s_h=5.0,
        n_train=2,
        energy_floor_factor=1e-4,
        causal_clip_facts=facts,
    )
    payload = load_training_metadata(
        run_dir,
        expected_energy_floor_factor=1e-4,
        expected_causal_clip_facts=facts,
    )

    assert payload["causal_clip_precision"] == "float64"
    assert payload["causal_clip_exponent_floor"] == facts["causal_clip_exponent_floor"]
    assert payload["causal_clip_min_weight"] == facts["causal_clip_min_weight"]
    assert payload["causal_clip_formula"] == facts["causal_clip_formula"]
    assert payload["causal_clip_provenance"] == facts["causal_clip_provenance"]
    assert _assert_s_h_matches_artifact(
        run_dir,
        source,
        energy_floor_factor=1e-4,
        expected_causal_clip_facts=facts,
    ) == 5.0


def test_causal_clip_resume_refuses_mismatched_runtime_fact(tmp_path):
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    path, _, facts = _write_pristine(run_dir)

    mismatched = dict(facts)
    mismatched["causal_clip_exponent_floor"] = facts["causal_clip_exponent_floor"] + 1.0
    with pytest.raises(ValueError, match="causal_clip_exponent_floor.*regenerate"):
        load_training_metadata(
            run_dir,
            expected_energy_floor_factor=1e-4,
            expected_causal_clip_facts=mismatched,
        )

    assert path.is_file()


@pytest.mark.parametrize(
    ("label", "mutate", "message"),
    [
        ("missing", lambda payload: payload.pop("causal_clip_precision"), "keys must be exactly"),
        ("extra", lambda payload: payload.update({"unexpected": 1}), "keys must be exactly"),
        ("old-schema", lambda payload: payload.update({"schema_version": 1}), "schema_version.*regenerate"),
        ("wrong-precision", lambda payload: payload.update({"causal_clip_precision": "float32"}), "causal_clip_precision.*regenerate"),
        ("wrong-floor", lambda payload: payload.update({"causal_clip_exponent_floor": -1.0}), "causal_clip_exponent_floor.*regenerate"),
        ("wrong-minimum", lambda payload: payload.update({"causal_clip_min_weight": 0.0}), "causal_clip_min_weight.*regenerate"),
        ("wrong-formula", lambda payload: payload.update({"causal_clip_formula": "exp(x_n)"}), "causal_clip_formula.*regenerate"),
        ("wrong-provenance", lambda payload: payload.update({"causal_clip_provenance": "observed"}), "causal_clip_provenance.*regenerate"),
        ("malformed-floor", lambda payload: payload.update({"causal_clip_exponent_floor": "tiny"}), "causal_clip_exponent_floor.*regenerate"),
    ],
)
def test_causal_clip_metadata_refuses_invalid_content(tmp_path, label, mutate, message):
    """Every schema/clip-field violation refuses with regeneration guidance."""
    run_dir = tmp_path / label
    run_dir.mkdir()
    path, pristine, facts = _write_pristine(run_dir)

    payload = dict(pristine)
    mutate(payload)
    path.write_text(json.dumps(payload, sort_keys=True) + "\n", encoding="utf-8")
    expected_message = message

    with pytest.raises(ValueError, match=expected_message):
        load_training_metadata(
            run_dir,
            expected_energy_floor_factor=1e-4,
            expected_causal_clip_facts=facts,
        )


def test_causal_clip_metadata_refuses_corrupt_json(tmp_path):
    run_dir = tmp_path / "corrupt"
    run_dir.mkdir()
    path, _, facts = _write_pristine(run_dir)
    path.write_text("{not json", encoding="utf-8")

    with pytest.raises(ValueError, match="not valid JSON"):
        load_training_metadata(
            run_dir,
            expected_energy_floor_factor=1e-4,
            expected_causal_clip_facts=facts,
        )
