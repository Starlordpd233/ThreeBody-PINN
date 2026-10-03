#!/usr/bin/env python3
"""Detached launcher for Phase-57 generation-7 training processes (GAP-57-12 L1).

The generation-6 graded seed 42 died silently because its trainer and its
stderr were tied to the agent session that launched it. This launcher starts a
small supervisor in its own session (no controlling terminal, its own process
group), so a closing terminal or agent session cannot deliver SIGHUP or a
process-group kill to the trainer. The supervisor runs the unchanged
generation-6-form trainer command, writes everything the trainer prints to a
retained log, and records the exit status the version-2 ledger requires.

Per invocation it writes ``runs/.launch/<run_name>/invocation-<n>/``:
``launch.json`` (command and identity), ``process.json`` (PIDs, session, start
time), ``output.log`` (trainer stdout+stderr), ``exit.json`` (exit code or
signal, end time), and ``supervisor.err`` (the supervisor's own stderr).

A deliberate stop still goes to the trainer PID (SIGINT or SIGTERM); the
supervisor forwards nothing and installs no signal handlers. Must run with
host-level Metal access, like every earlier generation.
"""

from __future__ import annotations

import argparse
import json
import os
import shlex
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[4]
LAUNCH_ROOT_REL = Path("runs/.launch")
LAUNCH_SCHEMA = "phase57-detached-launch/v1"
LAUNCH_MODE = "detached-session"
PINNED_PYTHON = "<home>/miniforge3/envs/pinn-train/bin/python"
RUN_NAMES = (
    "stage0-v23g7-smoke",
    "stage0-v23g7-seed42",
    "stage0-v23g7-seed41",
    "stage0-v23g7-seed43",
)
INTERRUPTED_EXIT_CODE = 130


class LaunchError(RuntimeError):
    """Fail-closed launch refusal."""


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    with path.open("x", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")


def trainer_argv(run_name: str, *, resume: bool) -> list[str]:
    """The generation-6 command form, with ``--resume latest`` for a resume."""
    if run_name not in RUN_NAMES:
        raise LaunchError(f"unknown generation-7 run name: {run_name!r}")
    argv = [
        "/usr/bin/caffeinate", "-is", PINNED_PYTHON, "-m", "pinn.train",
        "--config", f"configs/{run_name}.yaml", "--stage-0-only",
    ]
    return argv + ["--resume", "latest"] if resume else argv


def next_invocation_dir(root: Path, run_name: str, *, resume: bool) -> tuple[int, Path]:
    """Refuse a fresh launch over existing output and a resume without a governed stop."""
    run_dir = root / "runs" / run_name
    launch_dir = root / LAUNCH_ROOT_REL / run_name
    previous = sorted(
        (path for path in launch_dir.glob("invocation-*") if path.name.removeprefix("invocation-").isdigit()),
        key=lambda path: int(path.name.removeprefix("invocation-")),
    ) if launch_dir.is_dir() else []
    if not resume:
        if run_dir.exists() or launch_dir.exists():
            raise LaunchError(f"fresh launch target already exists: {run_dir} or {launch_dir}")
        return 1, launch_dir / "invocation-1"
    if not run_dir.is_dir() or not previous:
        raise LaunchError(f"resume has no earlier launched invocation of {run_name}")
    ordinal = len(previous) + 1
    if previous[-1].name != f"invocation-{ordinal - 1}":
        raise LaunchError(f"launch invocations of {run_name} are not consecutive")
    exit_path = previous[-1] / "exit.json"
    if not exit_path.is_file():
        raise LaunchError(f"previous invocation has not exited: {previous[-1]}")
    exit_record = json.loads(exit_path.read_text(encoding="utf-8"))
    if exit_record.get("exit_code") != INTERRUPTED_EXIT_CODE:
        raise LaunchError(
            "resume must follow a governed interrupted process (exit code "
            f"{INTERRUPTED_EXIT_CODE}); previous exit was {exit_record.get('exit_code')!r}"
        )
    return ordinal, launch_dir / f"invocation-{ordinal}"


def start(invocation_dir: Path, argv: list[str], *, cwd: Path, identity: dict[str, Any],
          wait_secs: float = 30.0) -> dict[str, Any]:
    """Write launch.json, start the detached supervisor, and return process.json."""
    invocation_dir.mkdir(parents=True, exist_ok=False)
    _write_json(invocation_dir / "launch.json", {
        "schema": LAUNCH_SCHEMA,
        "mode": LAUNCH_MODE,
        **identity,
        "argv": list(argv),
        "command": shlex.join(argv),
        "cwd": str(cwd),
        "launcher_pid": os.getpid(),
        "requested_utc": _utc_now(),
    })
    with (invocation_dir / "supervisor.err").open("wb") as supervisor_err:
        supervisor = subprocess.Popen(
            [sys.executable, str(Path(__file__).resolve()), "--supervise", str(invocation_dir)],
            cwd=str(cwd),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=supervisor_err,
            start_new_session=True,
            close_fds=True,
        )
    process_path = invocation_dir / "process.json"
    deadline = time.monotonic() + wait_secs
    while time.monotonic() < deadline:
        if process_path.is_file():
            return json.loads(process_path.read_text(encoding="utf-8"))
        if supervisor.poll() is not None and not process_path.is_file():
            raise LaunchError(f"supervisor exited before starting the trainer; see {invocation_dir / 'supervisor.err'}")
        time.sleep(0.05)
    raise LaunchError(f"trainer did not start within {wait_secs}s; see {invocation_dir}")


def supervise(invocation_dir: Path) -> int:
    """Run in the detached session: start the trainer, wait, record its exit."""
    launch = json.loads((invocation_dir / "launch.json").read_text(encoding="utf-8"))
    with (invocation_dir / "output.log").open("xb") as output:
        started = time.monotonic()
        start_utc = _utc_now()
        trainer = subprocess.Popen(
            launch["argv"],
            cwd=launch["cwd"],
            stdin=subprocess.DEVNULL,
            stdout=output,
            stderr=subprocess.STDOUT,
            close_fds=True,
        )
    _write_json(invocation_dir / "process.json", {
        "supervisor_pid": os.getpid(),
        "trainer_pid": trainer.pid,
        "session_id": os.getsid(0),
        "process_group": os.getpgid(0),
        "start_utc": start_utc,
    })
    returncode = trainer.wait()
    signal_name = signal.Signals(-returncode).name if returncode < 0 else None
    _write_json(invocation_dir / "exit.json", {
        "trainer_pid": trainer.pid,
        "returncode": returncode,
        "exit_code": returncode if returncode >= 0 else 128 - returncode,
        "signal": signal_name,
        "end_utc": _utc_now(),
        "wall_clock_secs": time.monotonic() - started,
    })
    return 0


def _assert_host_mps() -> None:
    probe = (
        "import torch; ok = torch.backends.mps.is_available() and torch.mps.device_count() > 0; "
        "raise SystemExit(0 if ok else 1)"
    )
    result = subprocess.run([PINNED_PYTHON, "-c", probe], cwd=str(REPO_ROOT), check=False)
    if result.returncode != 0:
        raise LaunchError("this process cannot see the host Metal device; launch with host-level access")


def _git_head() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=str(REPO_ROOT), capture_output=True, text=True, check=False,
    )
    if result.returncode != 0:
        raise LaunchError(f"cannot resolve git HEAD: {result.stderr.strip()}")
    return result.stdout.strip()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--run-name", choices=RUN_NAMES)
    parser.add_argument("--resume", action="store_true", help="continue after a governed interrupted stop")
    parser.add_argument("--supervise", type=Path, help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    if args.supervise is not None:
        return supervise(args.supervise)
    if args.run_name is None:
        parser.error("--run-name is required")
    try:
        _assert_host_mps()
        ordinal, invocation_dir = next_invocation_dir(REPO_ROOT, args.run_name, resume=args.resume)
        process = start(
            invocation_dir,
            trainer_argv(args.run_name, resume=args.resume),
            cwd=REPO_ROOT,
            identity={
                "run_name": args.run_name,
                "invocation_ordinal": ordinal,
                "launch_kind": "resume" if args.resume else "fresh",
                "git_head": _git_head(),
            },
        )
    except LaunchError as exc:
        print(f"launch_phase57_run FAIL-CLOSED: {exc}", file=sys.stderr)
        return 1
    print(json.dumps({"invocation_dir": str(invocation_dir.relative_to(REPO_ROOT)), **process}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
