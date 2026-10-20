"""Phase 60 (SCOPE-44): detached, one-at-a-time launcher for learnability arm sequences.

Generation 6 of the earlier training was lost silently because its process and its error
output were tied to the agent session that launched it. This launcher starts a small supervisor
in its own session (no controlling terminal, its own process group, standard input from
/dev/null), so a closing terminal or agent session cannot deliver a hangup or a process-group
kill to an arm. The supervisor runs the arms of one closed sequence strictly one at a time, each
as ``/usr/bin/caffeinate -is <pinned python> -B -m pinn.verification.learnability_run <arm-id>``,
stops at the first non-zero exit, and records how every arm ended. It uses argv lists only,
never a shell, and installs no signal handlers: a deliberate stop goes to the arm's own python
process id (SIGHUP, SIGINT or SIGTERM), never to the supervisor or to caffeinate.

Per invocation it writes ``runs/.launch/phase60/<sequence>/invocation-<n>/``, which stays
untracked (``runs/`` is ignored and the staged-path policy blocks it): ``launch.json`` (the
plan), ``process.json`` (supervisor process id and session), ``arm-<i>.json`` (how arm ``i``
ended), ``output.log`` (every arm's output), ``exit.json`` (written last), ``supervisor.out``
and ``supervisor.err``. Every JSON file is created exclusively and never rewritten.
"""

from __future__ import annotations

import argparse
import json
import os
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence

if __package__ in (None, ""):
    _ROOT = Path(__file__).resolve().parents[4]
    if str(_ROOT) not in sys.path:
        sys.path.insert(0, str(_ROOT))

REPO_ROOT = Path(__file__).resolve().parents[4]
LAUNCH_ROOT_REL = Path("runs/.launch/phase60")
LAUNCH_SCHEMA = "phase60-detached-launch/v1"
PINNED_PYTHON = "<home>/miniforge3/envs/pinn-train/bin/python"
CAFFEINATE = "/usr/bin/caffeinate"
RUNNER_MODULE = "pinn.verification.learnability_run"
# SIGHUP, SIGINT and SIGTERM as exit codes (128 + signal number): the only endings that allow a
# resume. A test pins these to learnability_arms.EXIT_SIGHUP, EXIT_SIGINT and EXIT_SIGTERM.
GOVERNED_STOP_CODES = (129, 130, 143)


class LaunchError(RuntimeError):
    """Fail-closed launch refusal."""


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    with path.open("x", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")


def _read_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise LaunchError(f"cannot read {path.name} in {path.parent.name}: {exc}") from exc
    if not isinstance(payload, dict):
        raise LaunchError(f"{path.name} in {path.parent.name} is not a JSON object")
    return payload


def _arms_module():
    """The arm catalog, imported on first use so the detached supervisor stays standard-library only."""
    from pinn.verification import learnability_arms

    return learnability_arms


def sequence_arms(name: str) -> tuple[str, ...]:
    """The arm ids of one closed sequence, in run order. Any other name is refused."""
    arms = _arms_module()
    if not isinstance(name, str) or name not in arms.SEQUENCES:
        raise LaunchError(
            f"unknown sequence {name!r}: it is not one of the {len(arms.SEQUENCES)} closed sequence names"
        )
    return tuple(arms.SEQUENCES[name])


def _catalog_arm(arm_id: str) -> str:
    arms = _arms_module()
    try:
        arms.arm_spec(arm_id)
    except arms.UnknownArm as exc:
        raise LaunchError(f"{arm_id!r} is not an arm of the closed catalog") from exc
    return arm_id


def arm_argv(arm_id: str, *, resume: bool) -> list[str]:
    """The command for one arm: caffeinate over the pinned runner, argv only, ``--resume`` on a resume."""
    argv = [CAFFEINATE, "-is", PINNED_PYTHON, "-B", "-m", RUNNER_MODULE, _catalog_arm(arm_id)]
    return argv + ["--resume"] if resume else argv


def describe_exit(returncode: int) -> tuple[int, str | None]:
    """``(exit_code, signal name)`` of a child: 128 plus the signal number for a death by signal."""
    if returncode >= 0:
        return returncode, None
    try:
        name = signal.Signals(-returncode).name
    except ValueError:
        name = f"SIG{-returncode}"
    return 128 - returncode, name


def _check_plan(argvs: Any, arm_ids: Any) -> None:
    """Refuse anything but one named, non-empty list-of-strings command per arm (never a shell string)."""
    if not isinstance(argvs, (list, tuple)) or not isinstance(arm_ids, (list, tuple)):
        raise LaunchError("a launch needs a list of commands and a list of arm ids")
    if not argvs or len(argvs) != len(arm_ids):
        raise LaunchError("a launch needs at least one arm and exactly one command per arm id")
    for arm_id, argv in zip(arm_ids, argvs):
        if not isinstance(arm_id, str) or not arm_id:
            raise LaunchError(f"an arm id must be a non-empty string; got {arm_id!r}")
        if not isinstance(argv, (list, tuple)) or not argv or not all(isinstance(item, str) for item in argv):
            raise LaunchError(f"the command for {arm_id} must be a non-empty list of strings (argv, no shell)")


def start(
    invocation_dir: Path,
    argvs: Sequence[Sequence[str]],
    *,
    cwd: Path,
    identity: dict[str, Any],
) -> dict[str, Any]:
    """Write launch.json, start the detached supervisor, record it in process.json and return at once.

    ``identity`` names the sequence and carries ``arm_ids``, one id per command in ``argvs``; its
    entries are copied into launch.json. The supervisor and every arm it runs use ``cwd`` as
    their working directory. Nothing is written when the plan is refused.
    """
    arm_ids = identity.get("arm_ids")
    _check_plan(argvs, arm_ids)
    if not Path(cwd).is_dir():
        raise LaunchError("the working directory of a launch must be an existing directory")
    invocation_dir.mkdir(parents=True, exist_ok=False)
    _write_json(invocation_dir / "launch.json", {
        **identity,
        "schema": LAUNCH_SCHEMA,
        "argvs": [list(argv) for argv in argvs],
        "requested_utc": _utc_now(),
    })
    with (invocation_dir / "supervisor.out").open("xb") as out, (invocation_dir / "supervisor.err").open("xb") as err:
        supervisor = subprocess.Popen(
            [sys.executable, str(Path(__file__).resolve()), "--supervise", str(invocation_dir)],
            cwd=str(cwd),
            stdin=subprocess.DEVNULL,
            stdout=out,
            stderr=err,
            start_new_session=True,
            close_fds=True,
        )
    try:
        session_id = os.getsid(supervisor.pid)
        process_group = os.getpgid(supervisor.pid)
    except ProcessLookupError as exc:
        raise LaunchError(
            f"the supervisor exited before it could be recorded; see {invocation_dir.name}/supervisor.err"
        ) from exc
    process = {
        "supervisor_pid": supervisor.pid,
        "session_id": session_id,
        "process_group": process_group,
        "start_utc": _utc_now(),
    }
    _write_json(invocation_dir / "process.json", process)
    return process


def supervise(invocation_dir: Path) -> int:
    """Run in the detached session: run each arm in turn, record how each ended, stop at the first failure."""
    launch = _read_json(invocation_dir / "launch.json")
    arm_ids, argvs = launch.get("arm_ids"), launch.get("argvs")
    _check_plan(argvs, arm_ids)
    started = time.monotonic()
    completed = 0
    stopped: tuple[str, int, str | None] | None = None
    with (invocation_dir / "output.log").open("xb") as output:
        for index, (arm_id, argv) in enumerate(zip(arm_ids, argvs), start=1):
            arm_started = time.monotonic()
            start_utc = _utc_now()
            child = subprocess.Popen(
                argv,
                stdin=subprocess.DEVNULL,
                stdout=output,
                stderr=subprocess.STDOUT,
                close_fds=True,
            )
            returncode = child.wait()
            exit_code, signal_name = describe_exit(returncode)
            _write_json(invocation_dir / f"arm-{index}.json", {
                "arm_id": arm_id,
                "pid": child.pid,
                "start_utc": start_utc,
                "end_utc": _utc_now(),
                "returncode": returncode,
                "exit_code": exit_code,
                "signal": signal_name,
                "wall_clock_secs": time.monotonic() - arm_started,
            })
            if returncode != 0:
                stopped = (arm_id, exit_code, signal_name)
                break
            completed += 1
    _write_json(invocation_dir / "exit.json", {
        "completed_arms": completed,
        "stopped_arm": stopped[0] if stopped else None,
        "stopped_code": stopped[1] if stopped else None,
        "signal": stopped[2] if stopped else None,
        "wall_clock_secs": time.monotonic() - started,
    })
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter, allow_abbrev=False,
    )
    parser.add_argument("--supervise", type=Path, required=True, help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    return supervise(args.supervise)


if __name__ == "__main__":
    raise SystemExit(main())
