"""Phase 42 fixtures — extend phase40/41 stubs with divergence/HALT knobs
plus subprocess helpers for the wired-system edge tests (plans 42-09).

Re-exports the phase40/41 builders (``make_stub_source``,
``make_stub_split_sources``, ``make_stub_model``,
``make_synthetic_stage0_loop``) rather than duplicating their bodies, and adds:

- ``inject_forced_divergence(run_controller, step)`` — monkey-patches the loss
  to return NaN on a chosen step, reusing the Phase-40 injection seam.
- ``inject_forced_halt(run_controller, step)`` — drives a guard HALT
  disposition on a chosen step, reusing the existing injection seam.
- ``run_synthetic_steps(loop, n_steps)`` — a small multi-step synthetic run
  driver reused across the signal / heartbeat / contract tests.

Subprocess helpers (used by the E2/E4/must-NOT tests that drive a real
``python -m pinn.train``):

- ``write_train_config(path, **overrides)`` — keyed YAML config matching the
  phase41 ``_write_config`` shape, with Phase-42 ``run.monitor`` knobs.
- ``make_runner_wrapper(tmpdir)`` — writes a tiny wrapper script that sets
  ``pinn.train._RUNS_ROOT`` before importing (so each subprocess uses an
  isolated temp runs-root instead of the worktree ``runs/``).
- ``launch_train(cfg_path, runs_root)`` — launches the wrapper as a
  ``subprocess.Popen`` and returns it. The subprocess PID matches the ``pid``
  field written to ``runs/<name>/status.json``.
"""

from __future__ import annotations

import math
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

# Re-export phase40/41 fixtures (do not duplicate bodies).
from tests.phase40._fixtures import (  # noqa: F401
    make_stub_model,
    make_stub_source,
    make_stub_split_sources,
)
from tests.phase41._fixtures import (  # noqa: F401
    StubClock,
    StubStepCounter,
    make_synthetic_stage0_loop,
)

__all__ = [
    "StubClock",
    "StubStepCounter",
    "inject_forced_divergence",
    "inject_forced_halt",
    "launch_train",
    "make_runner_wrapper",
    "make_synthetic_stage0_loop",
    "poll_run_status",
    "run_synthetic_steps",
    "wait_for_status",
    "write_train_config",
]

# Path to the pinn-train conda env's python (tests run outside the env's
# shell, so the direct binary path is more reliable than ``conda run``).
_CONDA_PYTHON = os.path.expanduser(
    "~/miniforge3/envs/pinn-train/bin/python"
)


def write_train_config(path: Path, **overrides) -> Path:
    """Write a minimal keyed YAML config (float64/cpu for deterministic tests).

    Extends the phase41 ``_write_config`` shape with the Phase-42
    ``run.monitor`` sub-config (CTX-80).
    """
    run = {
        "seed": 11,
        "precision": "float64",
        "device": "cpu",
        "strict_cpu_determinism": False,
        # Phase-42 exercises operator mechanics, not duration authorization.
        # The production smoke exemption keeps these isolated launches honest;
        # Phase-43 gate tests explicitly override this field to False.
        "smoke": True,
        "log_every": 1,
        "run_name": "test-run",
        "monitor": {
            "heartbeat_secs": 5,
            "staleness_factor": 3,
        },
        "checkpoint": {
            "every_n_steps": 1,
            "wall_clock_ceiling_s": 3600.0,
            "rolling_keep": 200,
            "failure_keep": 10,
        },
        "guards": {
            "loss_explosion_ceiling": 1.0e12,
            "disk_floor_fraction": 0.01,
            "memory_watermark_fraction": 0.99,
        },
    }
    stage = {
        "max_epochs": 2,
        "n_adam": 2,
        "stagnation_window": 10_000,
        "percentile_10_relaxation": 0.1,
        "beta": 0.9,
        "patience": 50,
        "eps_plateau": 1e-5,
        "eps_phys": 1e-4,
        "eps_energy": 1e-4,
    }
    opt = {
        "validation_every": 1,
        "lbfgs_max_iter": 2,
        "lbfgs_chunk_size": 4,
    }
    loss = {"lambda_e_max": 1.0}
    for key, val in overrides.items():
        if key == "run":
            run.update(val)
            # Strict-CPU tests must exercise the effective-runtime gate with
            # their real cpu/float64 calibration, never the smoke exemption.
            if val.get("strict_cpu_determinism") is True and "smoke" not in val:
                run["smoke"] = False
        elif key == "stage":
            stage.update(val)
        elif key == "opt":
            opt.update(val)
        elif key == "loss":
            loss.update(val)
        elif key == "guards":
            # ``guards`` lives under ``run.guards`` in the YAML schema; merge
            # rather than replace so unset thresholds keep their defaults.
            run["guards"].update(val)
    doc = {"run": run, "stage": stage, "opt": opt, "loss": loss}
    path.write_text(_safe_dump(doc), encoding="utf-8")
    return path


def _safe_dump(doc: Dict[str, Any]) -> str:
    """YAML-safe dump without importing yaml at module top (defensive)."""
    import yaml

    return yaml.safe_dump(doc, sort_keys=True)


def make_runner_wrapper(tmpdir: Path) -> Path:
    """Write a wrapper script that sets ``pinn.train._RUNS_ROOT`` then runs main().

    The wrapper accepts ``<runs_root>`` as its first positional arg followed by
    the usual ``pinn.train`` argv (``--config ...``). The subprocess PID is the
    PID of the python process running ``pinn.train.main()``, so it matches the
    ``pid`` field in ``status.json``.

    The wrapper prepends ``$PHASE42_REPO_ROOT`` to ``sys.path`` (set by
    :func:`launch_train`) so ``import pinn.train`` works regardless of the
    subprocess working directory or conda env activation state.
    """
    wrapper = tmpdir / "run_train.py"
    wrapper.write_text(
        "import os\n"
        "import sys\n"
        "from pathlib import Path\n"
        "# launch_train injects the repo root via PHASE42_REPO_ROOT so the\n"
        "# wrapper can import pinn.train without relying on cwd/conda activation.\n"
        "repo_root = os.environ.get('PHASE42_REPO_ROOT')\n"
        "if repo_root:\n"
        "    sys.path.insert(0, repo_root)\n"
        "import pinn.train\n"
        "pinn.train._RUNS_ROOT = Path(sys.argv[1])\n"
        "# sys.argv: [script, runs_root, --config, <path>, ...]. Drop runs_root\n"
        "# so argparse sees only pinn.train flags.\n"
        "sys.argv = [sys.argv[0]] + sys.argv[2:]\n"
        "sys.exit(pinn.train.main())\n",
        encoding="utf-8",
    )
    return wrapper


# Repo root: three levels above this file (tests/phase42/_fixtures.py).
# Computed once at import time — the test process already has `pinn` on its
# path, so this resolves reliably.
_REPO_ROOT = str(Path(__file__).resolve().parent.parent.parent)


def launch_train(
    cfg_path: Path,
    runs_root: Path,
    *,
    extra_args: Optional[List[str]] = None,
) -> subprocess.Popen[str]:
    """Launch ``python -m pinn.train --config <cfg>`` in a temp runs-root.

    Returns the ``subprocess.Popen``. Use ``poll_run_status`` /
    ``wait_for_status`` to block until the run is ready before signaling.

    The subprocess inherits the current env with ``PHASE42_REPO_ROOT`` injected
    so the wrapper can locate the ``pinn`` package even when the bare conda
    python binary is used (no ``conda run`` env setup).
    """
    tmpdir = Path(tempfile.mkdtemp(prefix="phase42-train-"))
    wrapper = make_runner_wrapper(tmpdir)
    argv = [
        _CONDA_PYTHON,
        str(wrapper),
        str(runs_root),
        "--config",
        str(cfg_path),
    ]
    if extra_args:
        argv.extend(extra_args)
    env = dict(os.environ)
    env["PHASE42_REPO_ROOT"] = _REPO_ROOT
    return subprocess.Popen(
        argv,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env,
    )


def poll_run_status(
    run_dir: Path,
    *,
    expected_pid: Optional[int] = None,
    states: Optional[List[str]] = None,
) -> Optional[Dict[str, Any]]:
    """Read ``run_dir/status.json`` and return it as a dict, or None if absent.

    When ``expected_pid`` is given, returns None until the file's ``pid``
    matches (filters out a stale prior run's status). When ``states`` is given,
    returns None until ``status["state"]`` is in ``states``.
    """
    import json

    status_path = run_dir / "status.json"
    if not status_path.is_file():
        return None
    try:
        status = json.loads(status_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if expected_pid is not None and status.get("pid") != expected_pid:
        return None
    if states is not None and status.get("state") not in states:
        return None
    return status


def wait_for_status(
    run_dir: Path,
    *,
    pid: int,
    states: List[str],
    timeout: float = 60.0,
    poll_interval: float = 0.1,
) -> Dict[str, Any]:
    """Poll ``run_dir/status.json`` until ``state in states`` and ``pid`` match.

    This is the deterministic readiness barrier for the signal tests: once
    ``status.json`` carries the run's pid and a live state, the signal handlers
    installed in ``main()`` are guaranteed to be active (CTX-71).

    Raises ``TimeoutError`` if the barrier is not reached within ``timeout``.
    """
    import json

    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        status = poll_run_status(run_dir, expected_pid=pid, states=states)
        if status is not None:
            return status
        if proc := getattr(status, "poll", None):
            pass
        time.sleep(poll_interval)
    raise TimeoutError(
        f"wait_for_status: {run_dir}/status.json never reached "
        f"state in {states} with pid={pid} within {timeout}s"
    )


def inject_forced_divergence(
    run_controller: Any,
    step: int,
    *,
    field: str = "total",
) -> None:
    """Monkey-patch ``run_controller`` so ``step`` produces a NaN loss.

    Reuses the Phase-40 injection seam: wraps the existing ``_log_step`` to
    replace the loss value with ``float('nan')`` on the target step. The
    original ``_log_step`` is preserved and called for all other steps.

    Parameters
    ----------
    run_controller : RunController
        The controller whose ``_log_step`` will be patched.
    step : int
        The step number at which to inject NaN.
    field : str
        Which loss field to NaN (default ``"total"``).
    """
    original_log_step = run_controller._log_step

    def _patched_log_step(step_record: Dict[str, Any]) -> None:
        if step_record.get("step") == step:
            step_record[field] = float("nan")
        original_log_step(step_record)

    run_controller._log_step = _patched_log_step


def inject_forced_halt(
    run_controller: Any,
    step: int,
    *,
    reason: str = "forced test halt",
) -> None:
    """Monkey-patch ``run_controller`` so ``step`` triggers a guard HALT.

    Reuses the Phase-40 injection seam: wraps the existing guard hook to force
    a HALT disposition on the target step. The original guard hook is preserved
    for all other steps.

    Parameters
    ----------
    run_controller : RunController
        The controller whose guard hook will be patched.
    step : int
        The step number at which to trigger HALT.
    reason : str
        The HALT reason string.
    """
    original_guard = getattr(run_controller, "_guard_hook", None)
    if original_guard is None:
        return

    def _patched_guard(step_record: Dict[str, Any]) -> Optional[str]:
        if step_record.get("step") == step:
            return reason
        return original_guard(step_record)

    run_controller._guard_hook = _patched_guard


def run_synthetic_steps(
    loop: Dict[str, Any],
    n_steps: int = 5,
    *,
    log_every: int = 1,
) -> Dict[str, Any]:
    """Drive ``n_steps`` training steps on a synthetic Stage-0 loop.

    A small multi-step run driver reused across the signal / heartbeat /
    contract tests. Returns a summary dict with ``steps_run`` and
    ``final_step``.

    Parameters
    ----------
    loop : dict
        The dict returned by ``make_synthetic_stage0_loop``.
    n_steps : int
        Number of training steps to run.
    log_every : int
        Log cadence (passed to the run controller's config).

    Returns
    -------
    dict
        ``{"steps_run": int, "final_step": int}``
    """
    config = loop["config"]
    config.run.log_every = log_every

    run_controller = loop["run_controller"]
    curriculum = loop["curriculum"]

    # Drive steps through the curriculum controller's run_controller.
    for i in range(n_steps):
        # The synthetic loop's train_source has n_train records; cycle through.
        run_controller.run_one_step(step=i)

    return {"steps_run": n_steps, "final_step": n_steps - 1}
