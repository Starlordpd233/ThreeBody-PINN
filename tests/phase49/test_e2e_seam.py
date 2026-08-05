"""Phase 49 / D-30 composed conformance seam.

The test drives the production ``pinn.train.main`` composition root with its
existing synthetic source.  It deliberately leaves invariant-B's owner value
unset so the run remains record-only and structurally ineligible for EVAL-01.
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest import mock

import yaml


def _write_synthetic_config(path: Path) -> Path:
    """Write the smallest real-main config that still enters the Adam loop."""

    payload = {
        "run": {
            "seed": 49,
            "precision": "float64",
            "device": "cpu",
            "strict_cpu_determinism": False,
            "log_every": 1,
            "run_name": "phase49-e2e-seam",
            "checkpoint": {
                "every_n_steps": 1,
                "rolling_keep": 3,
                "failure_keep": 3,
                "wall_clock_ceiling_s": 3600.0,
            },
            "guards": {
                "loss_explosion_ceiling": 1.0e12,
                "disk_floor_fraction": 0.01,
                "memory_watermark_fraction": 0.99,
            },
            # D-20: an empty mapping is the explicit record-only state.  No
            # test fixture or shipped config may invent the owner's N.
            "invariants": {},
        },
        "stage": {
            "max_epochs": 2,
            "n_adam": 2,
            "stagnation_window": 10_000,
            "percentile_10_relaxation": 0.1,
            "beta": 0.9,
            "patience": 50,
            "eps_plateau": 1.0e-5,
            "eps_phys": 1.0e-4,
            "eps_energy": 1.0e-4,
            "replay_count": 8,
        },
        "opt": {
            "validation_every": 1,
            "lbfgs_max_iter": 2,
            "lbfgs_chunk_size": 4,
        },
        "loss": {"lambda_e_max": 0.0},
        "data": {"source": "synthetic"},
    }
    path.write_text(yaml.safe_dump(payload, sort_keys=True), encoding="utf-8")
    return path


def test_real_main_orders_preflight_table_boundary_and_first_guard(
    tmp_path, monkeypatch
):
    """One synthetic run proves the complete run-start-to-guard chain."""

    from pinn import train
    from pinn.conformance import preflight
    from tests.phase41._fixtures import write_duration_gate_calibration

    guard_calls = []
    real_guard_check = train.StepGuards.check

    def capture_guard_inputs(guards, *args, **kwargs):
        guard_calls.append(
            {
                "phase": args[2] if len(args) > 2 else kwargs.get("phase"),
                "w_n_stats": kwargs.get("w_n_stats"),
            }
        )
        return real_guard_check(guards, *args, **kwargs)

    runs_root = tmp_path / "runs"
    runs_root.mkdir()
    write_duration_gate_calibration(
        runs_root,
        precision="float64",
        device="cpu",
        full_stage0_steps=2,
    )
    config_path = _write_synthetic_config(tmp_path / "config.yaml")
    monkeypatch.setattr(train, "_RUNS_ROOT", runs_root)

    with mock.patch.object(train.StepGuards, "check", capture_guard_inputs):
        exit_code = train.main(["--config", str(config_path)])

    assert exit_code == 0
    run_dir = runs_root / "phase49-e2e-seam"
    record = preflight.load_preflight(run_dir)
    events = record["assertions"]

    run_start = events[0]
    assert run_start["event"] == "run_start"
    assert run_start["status"] == "passed"
    assert {
        check["name"] for check in run_start["checks"]
    } >= {"lambda_phys_max", "lambda_e_max", "lambda_l_max", "census"}
    assert all(check["passed"] for check in run_start["checks"])
    assert run_start["census"] is not None
    assert run_start["open_divergences"]
    assert any(
        entry["id"] == "INV-B-N-UNSET"
        and entry["kind"] == "divergence"
        and entry["status"] == "open"
        for entry in run_start["open_divergences"]
    )

    boundaries = [event for event in events if event["event"] == "stage_boundary"]
    assert boundaries
    assert boundaries[0]["stage"] == 0
    assert boundaries[0]["status"] == "passed"
    assert events.index(run_start) < events.index(boundaries[0])

    summary = json.loads((run_dir / "summary.json").read_text(encoding="utf-8"))
    assert summary["disposition"] == "finished"
    assert summary["conformance"] == record
    assert summary["eval01_precondition_i"] is False

    adam_calls = [call for call in guard_calls if call["phase"] == "2a"]
    assert adam_calls
    assert all(call["w_n_stats"] is not None for call in adam_calls)

    # A causal-stats omission or invariant-A/B trip writes a failure bundle and
    # makes the composition root non-successful.  A clean finished run is the
    # production observable that the first guard evaluation had its inputs.
    failure_dir = run_dir / "failure"
    assert not any(failure_dir.iterdir())
