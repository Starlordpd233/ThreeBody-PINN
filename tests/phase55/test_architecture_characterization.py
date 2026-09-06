"""Contract tests for the Phase 55 architecture characterization probe."""

from __future__ import annotations

import importlib
import math
import pathlib
import unittest

import pytest


ROOT = pathlib.Path(__file__).resolve().parents[2]
MODULE = "pinn.verification.architecture_characterization_probe"


def _load_probe():
    """Defer production import so the RED suite skips before the module exists."""
    try:
        return importlib.import_module(MODULE)
    except ImportError as exc:
        raise unittest.SkipTest(f"{MODULE} has not landed yet: {exc}") from exc


def _tracer_case(probe):
    return probe.SweepCase(
        label="41",
        seed=41,
        masses=(1.0, 1.0, 1.0),
        ic13_mode="zero",
    )


def test_tracer_single_case_reports_all_seven_quantities():
    probe = _load_probe()
    result = probe.measure_case(_tracer_case(probe))

    assert isinstance(result, probe.ArchitectureCharacterizationResult)
    assert math.isfinite(result.r_norm_median)
    assert math.isfinite(result.v_norm_median)
    assert math.isfinite(result.a_norm_median)
    assert math.isfinite(result.f_grav_norm_median)
    assert math.isfinite(result.min_pairwise_separation_median)
    assert math.isfinite(result.rbar_median)
    assert isinstance(result.front_idx, int)
    assert result.front_idx == 0
    assert 1e9 < result.rbar_median < 1e11
    assert len(result.causal_weights) == result.n_col
    assert result.causal_weights[0] == 1.0
    times = result.collocation_times
    assert len(times) == result.n_col
    assert times == tuple(sorted(times))
    assert all(times[index] < times[index + 1] for index in range(len(times) - 1))


def test_tracer_case_is_deterministic_across_two_calls():
    probe = _load_probe()
    case = _tracer_case(probe)
    first = probe.measure_case(case)
    second = probe.measure_case(case)
    assert first == second


def test_sweep_case_rejects_malformed_fields():
    probe = _load_probe()
    SweepCase = probe.SweepCase
    valid = dict(label="41", seed=41, masses=(1.0, 1.0, 1.0), ic13_mode="zero")

    with pytest.raises(ValueError, match="label"):
        SweepCase(**{**valid, "label": ""})
    with pytest.raises(ValueError, match="label"):
        SweepCase(**{**valid, "label": 41})
    with pytest.raises(ValueError, match="seed"):
        SweepCase(**{**valid, "seed": -1})
    with pytest.raises(ValueError, match="seed"):
        SweepCase(**{**valid, "seed": True})
    with pytest.raises(ValueError, match="masses"):
        SweepCase(**{**valid, "masses": (1.0, 1.0)})
    with pytest.raises(ValueError, match="masses"):
        SweepCase(**{**valid, "masses": (1.0, 1.0, float("nan"))})
    with pytest.raises(ValueError, match="masses"):
        SweepCase(**{**valid, "masses": (1.0, 1.0, 0.0)})
    with pytest.raises(ValueError, match="ic13_mode"):
        SweepCase(**{**valid, "ic13_mode": "bogus"})
