"""Strict causal-clip provenance and fresh/resume lifecycle tests."""

from __future__ import annotations

import math

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
    facts = resolve_causal_clip_facts(torch.float64, torch.device("cpu"))
    write_training_metadata(
        run_dir,
        s_h=5.0,
        n_train=2,
        energy_floor_factor=1e-4,
        causal_clip_facts=facts,
    )

    mismatched = dict(facts)
    mismatched["causal_clip_exponent_floor"] = facts["causal_clip_exponent_floor"] + 1.0
    with pytest.raises(ValueError, match="causal_clip_exponent_floor.*regenerate"):
        load_training_metadata(
            run_dir,
            expected_energy_floor_factor=1e-4,
            expected_causal_clip_facts=mismatched,
        )

    assert (run_dir / TRAINING_METADATA_FILENAME).is_file()
