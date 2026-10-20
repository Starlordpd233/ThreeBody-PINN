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

Usage, with the pinned interpreter from the repository root::

    launch_phase60_arm.py --sequence NAME             start a fresh invocation and return at once
    launch_phase60_arm.py --sequence NAME --resume    continue after a governed stop
    launch_phase60_arm.py --sequence NAME --dry-run   admit every arm in the foreground, start nothing
    launch_phase60_arm.py --sequence NAME --status    SEQUENCE-NOT-LAUNCHED, SEQUENCE-RUNNING (and
                                                      ARM-PID <pid>), SEQUENCE-COMPLETE or
                                                      SEQUENCE-STOPPED <arm-id> <code>

NAME is one of the closed sequence names in ``learnability_arms.SEQUENCES`` (``arm:<id>`` runs
one catalog arm). A resume is a new invocation that starts the stopped arm with ``--resume`` and
then the remaining arms. It is accepted only when the previous invocation's exit.json records a
stop by SIGHUP, SIGINT or SIGTERM (exit code 129, 130 or 143, the arm having exited by its own
handler) for a named arm. A completed sequence, a refused arm (2), an owner-routed arm (3), any
death by a signal (SIGKILL is 137), a supervisor that was lost, or any other ending refuses the
resume: that arm goes to the owner, and nothing is ever restarted silently.

Per invocation it writes ``runs/.launch/phase60/<sequence>/invocation-<n>/``, which stays
untracked (``runs/`` is ignored and the staged-path policy blocks it): ``launch.json`` (the
plan), ``process.json`` (supervisor process id and session), ``arm-<i>.json`` (how arm ``i``
ended), ``output.log`` (every arm's output), ``exit.json`` (written last), ``supervisor.out``
and ``supervisor.err``. Every JSON file is created exclusively and never rewritten. The
launcher does not itself stop two different sequences from being launched together; keeping two
arms from running at once is the job of the runner's one-launch lock (Plan 60-12).
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
from typing import Any, Callable, Sequence

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


def admit_argv(arm_id: str) -> list[str]:
    """The foreground admission command: the runner's ``--admit-only``. Nothing trains, so no caffeinate."""
    return [PINNED_PYTHON, "-B", "-m", RUNNER_MODULE, _catalog_arm(arm_id), "--admit-only"]


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


def _launch_dir(root: Path, sequence: str) -> Path:
    sequence_arms(sequence)  # closed names only, refused before anything is read or written
    return Path(root) / LAUNCH_ROOT_REL / sequence


def _invocations(launch_dir: Path) -> list[Path]:
    """The ``invocation-<n>`` directories of a sequence in numeric order; they must run 1..n without a gap."""
    if not launch_dir.is_dir():
        return []
    found = sorted(
        (path for path in launch_dir.glob("invocation-*") if path.name.removeprefix("invocation-").isdigit()),
        key=lambda path: int(path.name.removeprefix("invocation-")),
    )
    if [path.name for path in found] != [f"invocation-{n}" for n in range(1, len(found) + 1)]:
        raise LaunchError(f"launch invocations of {launch_dir.name} are not consecutive")
    return found


def _governed_stop(exit_record: dict[str, Any], where: str) -> str:
    """The stopped arm of a governed stop. Any other ending cannot resume and goes to the owner.

    A governed stop is an arm that handled SIGHUP, SIGINT or SIGTERM, checkpointed and exited with the
    matching code. An arm that was killed by a signal instead (``signal`` is set, even for SIGTERM and
    its code 143) never ran its handler, so no checkpoint was written and it cannot resume.
    """
    arm_id, code = exit_record.get("stopped_arm"), exit_record.get("stopped_code")
    died_by = exit_record.get("signal")
    if not arm_id or code not in GOVERNED_STOP_CODES or died_by is not None:
        raise LaunchError(
            f"arm cannot resume; owner decides: {where} ended with stopped_arm={arm_id!r}, "
            f"stopped_code={code!r} and signal={died_by!r}, and only an arm that exited with code "
            f"{', '.join(str(item) for item in GOVERNED_STOP_CODES)} by its own handler resumes"
        )
    return arm_id


def resume_arm_ids(previous_exit: dict[str, Any], sequence: str) -> tuple[str, ...]:
    """The stopped arm and every arm after it, in run order. Refuses a stop that is not governed."""
    arm_ids = sequence_arms(sequence)
    stopped = _governed_stop(previous_exit, f"the previous invocation of {sequence}")
    if stopped not in arm_ids:
        raise LaunchError(f"arm cannot resume; owner decides: {stopped!r} is not an arm of {sequence}")
    return arm_ids[arm_ids.index(stopped):]


def resume_argvs(
    previous_exit: dict[str, Any],
    sequence: str,
    *,
    argv_builder: Callable[..., list[str]] | None = None,
) -> list[list[str]]:
    """The commands of a resume: the stopped arm with ``--resume``, then the arms after it as fresh arms."""
    build = argv_builder or arm_argv
    stopped, *later = resume_arm_ids(previous_exit, sequence)
    return [build(stopped, resume=True)] + [build(arm_id, resume=False) for arm_id in later]


def next_invocation_dir(root: Path, sequence: str, *, resume: bool) -> tuple[int, Path]:
    """Refuse a fresh launch over existing launch files and a resume that does not follow a governed stop."""
    launch_dir = _launch_dir(root, sequence)
    previous = _invocations(launch_dir)
    if not resume:
        if launch_dir.exists():
            raise LaunchError(
                f"fresh launch target already exists: {LAUNCH_ROOT_REL / sequence}; "
                "only a resume after a governed stop continues it"
            )
        return 1, launch_dir / "invocation-1"
    if not previous:
        raise LaunchError(f"resume has no earlier launched invocation of {sequence}")
    latest = previous[-1]
    exit_path = latest / "exit.json"
    if not exit_path.is_file():
        raise LaunchError(
            f"arm cannot resume; owner decides: {latest.name} of {sequence} has recorded no exit "
            "(still running or lost)"
        )
    resume_arm_ids(_read_json(exit_path), sequence)
    ordinal = len(previous) + 1
    return ordinal, launch_dir / f"invocation-{ordinal}"


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


def _supervisor_alive(pid: Any) -> bool:
    """Whether ``pid`` names one live process. Zero and negative ids would address a whole group: never alive."""
    if not isinstance(pid, int) or isinstance(pid, bool) or pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def _arm_pid(root: Path, arm_id: str) -> int | None:
    """The process id the running arm wrote to its own process.json, when that file is present and holds one."""
    try:
        record = _read_json(_arms_module().arm_run_dir(arm_id, repo_root=root) / "process.json")
    except (LaunchError, ValueError):
        return None
    pid = record.get("pid")
    return pid if isinstance(pid, int) and not isinstance(pid, bool) else None


def _running_lines(root: Path, invocation: Path) -> list[str]:
    lines = ["SEQUENCE-RUNNING"]
    arm_ids = _read_json(invocation / "launch.json").get("arm_ids") or []
    finished = sum(1 for _ in invocation.glob("arm-*.json"))
    if finished < len(arm_ids):
        pid = _arm_pid(root, arm_ids[finished])
        if pid is not None:
            lines.append(f"ARM-PID {pid}")
    return lines


def _invocation_status(root: Path, invocation: Path) -> list[str]:
    exit_path = invocation / "exit.json"
    if not exit_path.exists():
        try:
            supervisor_pid = _read_json(invocation / "process.json").get("supervisor_pid")
        except LaunchError:
            supervisor_pid = None
        if _supervisor_alive(supervisor_pid):
            return _running_lines(root, invocation)
        if not exit_path.exists():  # it may have written exit.json and ended since the first look
            raise LaunchError(
                f"owner decides: {invocation.name} has no live supervisor and recorded no exit"
            )
    record = _read_json(exit_path)
    stopped = record.get("stopped_arm")
    if stopped is None:
        return ["SEQUENCE-COMPLETE"]
    code = record.get("stopped_code")
    if code is None:
        raise LaunchError(f"{invocation.name} names a stopped arm ({stopped!r}) but no stopped code")
    return [f"SEQUENCE-STOPPED {stopped} {code}"]


def status(sequence: str, *, repo_root: Path | None = None) -> list[str]:
    """Print the state of a sequence (exactly one state line, plus ARM-PID while it runs) and return the lines.

    Read-only: it creates nothing. A supervisor that is gone without having recorded an exit is
    refused rather than reported as a state, because it cannot resume and goes to the owner.
    """
    root = Path(repo_root) if repo_root is not None else REPO_ROOT
    launch_dir = _launch_dir(root, sequence)
    invocations = _invocations(launch_dir)
    if not launch_dir.exists():
        lines = ["SEQUENCE-NOT-LAUNCHED"]
    elif not invocations:
        raise LaunchError(f"owner decides: {LAUNCH_ROOT_REL / sequence} exists but holds no invocation")
    else:
        lines = _invocation_status(root, invocations[-1])
    for line in lines:
        print(line)
    return lines


def _admitted(returncode: int, stdout: str) -> bool:
    """A clean exit that printed an ADMIT-OK line and no ADMIT-REFUSED line."""
    tokens = [words[0] for words in (line.split() for line in stdout.splitlines()) if words]
    return (
        returncode == 0
        and "ADMIT-OK" in tokens
        and not any(token.startswith("ADMIT-REFUSED") for token in tokens)
    )


def dry_run(
    sequence: str,
    *,
    cwd: Path | None = None,
    command_builder: Callable[[str], list[str]] | None = None,
) -> None:
    """Admit every arm of the sequence in the foreground and start nothing.

    Each arm's command (the runner's ``--admit-only`` unless ``command_builder`` says otherwise) runs to
    completion and its output is relayed, so every ``ADMIT-OK <arm>`` or ``ADMIT-REFUSED: <reason>`` line
    is seen. Every arm is probed even after a refusal. Raises LaunchError unless every arm admitted.
    """
    build = command_builder or admit_argv
    where = Path(cwd) if cwd is not None else REPO_ROOT
    refused = []
    for arm_id in sequence_arms(sequence):
        completed = subprocess.run(
            build(arm_id), cwd=str(where), stdin=subprocess.DEVNULL, capture_output=True, text=True,
            errors="replace", check=False,
        )
        sys.stdout.write(completed.stdout)
        sys.stderr.write(completed.stderr)
        if not _admitted(completed.returncode, completed.stdout):
            refused.append(arm_id)
    if refused:
        raise LaunchError(f"not admitted: {', '.join(refused)}")


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


def launch(
    sequence: str,
    *,
    resume: bool,
    repo_root: Path | None = None,
    argv_builder: Callable[..., list[str]] | None = None,
    host_check: Callable[[], None] | None = None,
) -> tuple[int, Path]:
    """Start a fresh invocation, or a resume after a governed stop, and return ``(ordinal, directory)`` at once.

    The sequence name is checked first (a typo should not wait for a Metal probe), then the host can
    see the Metal device, then the invocation gate decides. ``argv_builder`` and ``host_check`` exist
    so tests can launch stub commands; a real launch leaves both unset.
    """
    root = Path(repo_root) if repo_root is not None else REPO_ROOT
    arm_ids = sequence_arms(sequence)
    (host_check or _assert_host_mps)()
    ordinal, invocation_dir = next_invocation_dir(root, sequence, resume=resume)
    build = argv_builder or arm_argv
    if resume:
        previous_exit = _read_json(invocation_dir.parent / f"invocation-{ordinal - 1}" / "exit.json")
        arm_ids = resume_arm_ids(previous_exit, sequence)
        argvs = resume_argvs(previous_exit, sequence, argv_builder=build)
    else:
        argvs = [build(arm_id, resume=False) for arm_id in arm_ids]
    start(
        invocation_dir,
        argvs,
        cwd=root,
        identity={
            "sequence": sequence,
            "arm_ids": list(arm_ids),
            "invocation_ordinal": ordinal,
            "launch_kind": "resume" if resume else "fresh",
            "git_head": _git_head(),
        },
    )
    return ordinal, invocation_dir


def main(
    argv: list[str] | None = None,
    *,
    repo_root: Path | None = None,
    command_builder: Callable[[str], list[str]] | None = None,
) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter, allow_abbrev=False,
    )
    parser.add_argument("--sequence", help="a closed sequence name (arm:<catalog id> runs one arm)")
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument("--resume", action="store_true", help="continue after a governed stop (129, 130, 143)")
    actions.add_argument(
        "--dry-run", action="store_true", help="run the runner's --admit-only for every arm; start nothing",
    )
    actions.add_argument("--status", action="store_true", help="print the state of the sequence")
    actions.add_argument("--supervise", type=Path, help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    if args.supervise is not None:
        return supervise(args.supervise)
    if args.sequence is None:
        parser.error("--sequence is required")
    root = Path(repo_root) if repo_root is not None else REPO_ROOT
    try:
        if args.status:
            status(args.sequence, repo_root=root)
        elif args.dry_run:
            dry_run(args.sequence, cwd=root, command_builder=command_builder)
        else:
            ordinal, _invocation_dir = launch(args.sequence, resume=args.resume, repo_root=root)
            print(f"LAUNCHED {args.sequence} invocation-{ordinal}")
    except LaunchError as exc:
        print(f"launch_phase60_arm FAIL-CLOSED: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
