"""Phase 43 fixtures — the shared Phase-43 test surface.

This module deliberately owns **no** fixture bodies of its own. It re-exports
the Phase-42 subprocess helpers (the only cross-phase assets Phase-43 plans
need: a real ``python -m pinn.train`` launch for the smoke / launch-gate tests)
plus the ``pinn-train`` interpreter path, so every Phase-43 test module reaches
one convention rather than re-deriving a launcher.

Re-exported from ``tests.phase42._fixtures`` (bodies live there, not here):

- ``write_train_config(path, **overrides)`` — keyed YAML config writer.
- ``make_runner_wrapper(tmpdir)`` — wrapper script that pins
  ``pinn.train._RUNS_ROOT`` to an isolated temp runs-root before importing.
- ``launch_train(cfg_path, runs_root, *, extra_args=None)`` — launches the
  wrapper as a ``subprocess.Popen``.
- ``poll_run_status(run_dir, ...)`` / ``wait_for_status(run_dir, ...)`` — the
  deterministic readiness barrier over ``runs/<name>/status.json``.
- ``CONDA_PYTHON`` — absolute path to the ``pinn-train`` conda env interpreter
  (tests run outside the env's shell, so the direct binary path is more
  reliable than ``conda run``).

Import discipline: dataset-free and I/O-free at import time. Nothing here
touches ``simulation_data/``, ``runs/``, or the network; the Phase-43 ladder
tests drive ``pinn.verify`` in-process with the probes patched, and only the
launch-path tests spend a subprocess.

No smoke harness lives here — ACC-02's smoke invocation is the ordinary
``pinn.train`` path (CTX-72) and is wired by plans 43-03/43-06, not by a
bespoke fixture.
"""

from __future__ import annotations

# Phase-42 subprocess helpers — re-exported, never duplicated.
from tests.phase42._fixtures import (  # noqa: F401
    _CONDA_PYTHON as CONDA_PYTHON,
    launch_train,
    make_runner_wrapper,
    poll_run_status,
    wait_for_status,
    write_train_config,
)

__all__ = [
    "CONDA_PYTHON",
    "launch_train",
    "make_runner_wrapper",
    "poll_run_status",
    "wait_for_status",
    "write_train_config",
]
