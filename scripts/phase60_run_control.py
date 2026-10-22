"""Pause, resume and the power guard for detached Phase 60 learnability runs.

Operator tooling for a laptop that cannot stay on its charger. The wrappers
``scripts/phase60-pause.sh``, ``scripts/phase60-resume.sh`` and ``scripts/phase60-power-guard.sh``
run it with the pinned interpreter. It edits no pinned file: it drives the sealed launcher through
its command line and reads the launch files that launcher documents. Only the resume pre-check
imports the runner, to ask the questions the runner itself asks before it resumes an arm.

How a pause works (``launch_phase60_arm.py`` and ``pinn/verification/learnability_run.py``):

- A pause is one SIGINT to the arm's own python process (the owner pause of Plan 60-14). The arm
  checkpoints at its next safe point and exits 130, the supervisor ends the whole sequence, and
  ``--resume`` continues the arm from its checkpoint.
- The signal waits until the arm can take it: the process must be the current supervisor's child
  and must have written its own ``process.json`` at least a second earlier, which is when its stop
  handlers are installed. A signal before that kills the arm, and a killed arm never resumes.
- Each arm process gets at most one signal, ever. On its way out an arm puts the default handlers
  back, and a second signal then kills it. One lock shared by every pause and resume (by hand or by
  the guard) and a marker file per signalled process enforce this.
- An arm in its closing stretch (the scoring and records after the polish have no stop check)
  still completes, and the supervisor starts the next arm. The pause then stops that arm as soon as
  it can take the signal. A stop during an arm's timing run is resumable: the resume repeats it.

Usage::

    phase60_run_control.py pause [SEQUENCE]          pause every running sequence, or only SEQUENCE
    phase60_run_control.py resume [SEQUENCE]         resume the paused sequence, then start the guard
    phase60_run_control.py guard [start|stop|status] the power guard (start is the default)
"""

from __future__ import annotations

import argparse
import contextlib
import fcntl
import json
import os
import signal
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Iterator

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / ".planning/phases/60-single-system-learnability/evidence"
LAUNCHER = EVIDENCE / "launch_phase60_arm.py"
LAUNCH_ROOT = ROOT / "runs/.launch/phase60"
ARM_RUNS = ROOT / "runs/phase60"
CONTROL = ROOT / "runs/.phase60-control"  # the shared lock, signal markers, guard pid and log
GUARD_LOCK = CONTROL / "guard.lock"
GUARD_PID = CONTROL / "guard.pid"
GUARD_LOG = CONTROL / "guard.log"
GUARD_COMMAND = "phase60_run_control.py guard run"

GOVERNED_STOP_CODES = (129, 130, 143)  # launch_phase60_arm.GOVERNED_STOP_CODES
PAUSE_SIGNAL = signal.SIGINT  # Plan 60-14's owner pause; the arm exits 130
HANDLERS_SETTLED_SECS = 1.0  # the runner installs its handlers right after writing process.json
PAUSE_TIMEOUT_SECS = 30 * 60
RESUME_CONFIRM_SECS = 120
DAILY_PAUSE = (9, 0)  # the guard pauses once when the clock passes 09:00
GUARD_TICK_SECS = 30
GUARD_IDLE_EXIT_SECS = 10 * 60


class Refused(RuntimeError):
    """A resume that must not be launched."""


def say(message: str) -> None:
    print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {message}", flush=True)


def _read_json(path: Path) -> dict[str, Any] | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return payload if isinstance(payload, dict) else None


def _alive(pid: Any) -> bool:
    if not isinstance(pid, int) or isinstance(pid, bool) or pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def _run(argv: list[str], **kwargs: Any) -> subprocess.CompletedProcess:
    return subprocess.run(argv, stdin=subprocess.DEVNULL, capture_output=True, text=True, check=False, **kwargs)


def _launcher(*args: str) -> subprocess.CompletedProcess:
    return _run([sys.executable, "-B", str(LAUNCHER), *args], cwd=str(ROOT))


def _command_of(pid: int) -> str:
    return _run(["ps", "-o", "command=", "-p", str(pid)]).stdout.strip()


def on_battery() -> bool:
    try:
        return "Battery Power" in _run(["pmset", "-g", "batt"]).stdout
    except OSError:
        return False


def notify(message: str) -> None:
    """A macOS notification; best effort."""
    script = f'display notification "{message}" with title "Phase 60 training"'
    with contextlib.suppress(OSError):
        _run(["osascript", "-e", script])


@contextlib.contextmanager
def control_lock() -> Iterator[None]:
    """Serialize every pause and resume, whether started by hand or by the guard."""
    CONTROL.mkdir(parents=True, exist_ok=True)
    with (CONTROL / "control.lock").open("a") as handle:
        try:
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            say("another pause or resume is in progress; waiting for it to finish")
            fcntl.flock(handle, fcntl.LOCK_EX)
        yield


# The launch files, read the way launch_phase60_arm.py documents them, without a subprocess.


@dataclass(frozen=True)
class Peek:
    sequence: str
    invocation: Path | None
    running: bool  # no exit.json yet and a live supervisor
    supervisor_pid: int | None
    arm_id: str | None  # the arm the supervisor is on


def launched_sequences() -> list[str]:
    if not LAUNCH_ROOT.is_dir():
        return []
    return sorted(path.name for path in LAUNCH_ROOT.iterdir() if path.is_dir())


def _latest_invocation(sequence: str) -> Path | None:
    found = [
        path for path in (LAUNCH_ROOT / sequence).glob("invocation-*")
        if path.name.removeprefix("invocation-").isdigit()
    ]
    return max(found, key=lambda path: int(path.name.removeprefix("invocation-")), default=None)


def peek(sequence: str) -> Peek:
    invocation = _latest_invocation(sequence)
    if invocation is None or (invocation / "exit.json").exists():
        return Peek(sequence, invocation, False, None, None)
    supervisor_pid = (_read_json(invocation / "process.json") or {}).get("supervisor_pid")
    arm_ids = (_read_json(invocation / "launch.json") or {}).get("arm_ids") or []
    finished = sum(1 for _ in invocation.glob("arm-*.json"))
    arm_id = arm_ids[finished] if finished < len(arm_ids) else None
    return Peek(sequence, invocation, _alive(supervisor_pid), supervisor_pid, arm_id)


def running_sequences() -> list[str]:
    return [sequence for sequence in launched_sequences() if peek(sequence).running]


def _children(pid: int | None) -> set[int]:
    if not isinstance(pid, int):
        return set()
    return {int(word) for word in _run(["pgrep", "-P", str(pid)]).stdout.split() if word.isdigit()}


def arm_process(arm_id: str) -> dict[str, Any]:
    return _read_json(ARM_RUNS / arm_id / "process.json") or {}


def ready_arm_pid(view: Peek) -> int | None:
    """The running arm's PID once it can take the pause signal; None means wait and look again.

    The PID in ``runs/phase60/<arm>/process.json`` must be the current supervisor's child (a
    resumed arm's file still names the earlier process until the new one rewrites it), the file
    must be old enough that the stop handlers are installed, and the arm must not have written its
    record yet (an arm with a record is on its way out).
    """
    if not view.running or view.arm_id is None:
        return None
    path = ARM_RUNS / view.arm_id / "process.json"
    pid = arm_process(view.arm_id).get("pid")
    if not isinstance(pid, int) or pid not in _children(view.supervisor_pid):
        return None
    try:
        age = time.time() - path.stat().st_mtime
    except OSError:
        return None
    if age < HANDLERS_SETTLED_SECS or (EVIDENCE / "arms" / view.arm_id / "record.json").exists():
        return None
    return pid


def signal_once(pid: int, *, sequence: str, arm_id: str) -> bool:
    """Send the pause signal unless this process (PID and start time) was ever signalled before."""
    started = " ".join(_run(["ps", "-o", "lstart=", "-p", str(pid)], env={**os.environ, "LC_ALL": "C"}).stdout.split())
    if not started:
        return False
    marker = CONTROL / "signalled" / f"{pid}-{started.replace(' ', '-').replace(':', '')}.json"
    marker.parent.mkdir(parents=True, exist_ok=True)
    try:
        with marker.open("x", encoding="utf-8") as handle:
            json.dump({
                "pid": pid, "process_started": started, "sequence": sequence, "arm_id": arm_id,
                "signal": PAUSE_SIGNAL.name, "sent": datetime.now().isoformat(timespec="seconds"),
            }, handle)
    except FileExistsError:
        return False
    try:
        os.kill(pid, PAUSE_SIGNAL)
    except ProcessLookupError:
        marker.unlink()
        return False
    except PermissionError as exc:  # nothing was delivered, so a later pause must still be able to try
        marker.unlink()
        raise PermissionError(
            f"cannot signal arm {arm_id} (pid {pid}): {exc.strerror}; run this from a shell that can "
            "(outside the agent sandbox)"
        ) from exc
    return True


# The authoritative state comes from the launcher's own --status.


@dataclass(frozen=True)
class State:
    sequence: str
    line: str  # the launcher's state line, or its FAIL-CLOSED message
    resumable: bool
    ok: bool  # nothing for the owner to decide


def sequence_state(sequence: str) -> State:
    result = _launcher("--sequence", sequence, "--status")
    if result.returncode != 0:
        return State(sequence, " ".join((result.stderr or result.stdout).split()), False, False)
    line = (result.stdout.splitlines() or [""])[0].strip()
    if line.startswith("SEQUENCE-STOPPED"):
        invocation = _latest_invocation(sequence)
        record = (_read_json(invocation / "exit.json") if invocation else None) or {}
        # The launcher's rule: a governed code and no death by a signal (which also shows 130/143).
        resumable = record.get("stopped_code") in GOVERNED_STOP_CODES and record.get("signal") is None
        return State(sequence, line, resumable, resumable)
    return State(sequence, line, False, not line.startswith("SEQUENCE-RUNNING"))


def _last_stop(arm_id: str) -> str:
    markers = sorted(
        (ARM_RUNS / arm_id).glob("stop-*.json"),
        key=lambda path: int(path.stem.removeprefix("stop-")) if path.stem.removeprefix("stop-").isdigit() else -1,
    )
    marker = _read_json(markers[-1]) if markers else None
    if not marker:
        return ""
    return f" in its {marker.get('phase')} phase at step {marker.get('step')}"


def describe(state: State) -> str:
    words = state.line.split()
    if state.line.startswith("SEQUENCE-STOPPED") and len(words) >= 3:
        arm_id, code = words[1], words[2]
        if state.resumable:
            return (
                f"PAUSED {state.sequence}: arm {arm_id} stopped cleanly with exit {code}{_last_stop(arm_id)}; "
                "scripts/phase60-resume.sh continues it from its checkpoint"
            )
        invocation = _latest_invocation(state.sequence)
        record = (_read_json(invocation / "exit.json") if invocation else None) or {}
        how = f" (killed by {record['signal']})" if record.get("signal") else ""
        log = invocation.relative_to(ROOT) / "output.log" if invocation else "the launch files"
        return (
            f"NOT-RESUMABLE {state.sequence}: arm {arm_id} ended with exit {code}{how}, which is not a "
            f"pause; the launcher will not resume it and the owner decides (see {log})"
        )
    if state.line == "SEQUENCE-COMPLETE":
        return f"COMPLETE {state.sequence}: every arm finished"
    if state.line.startswith("SEQUENCE-RUNNING"):
        return f"RUNNING {state.sequence}"
    return f"OWNER-DECIDES {state.sequence}: {state.line}"


# pause


def pause(only: str | None = None, *, reason: str = "asked by hand") -> int:
    """Pause every running sequence (or only ``only``). 0: all stopped and resumable or complete;
    1: something the owner must look at; 3: still stopping when the wait ran out."""
    with control_lock():
        launched = launched_sequences()
        if only is not None and only not in launched:
            say(f"{only} has never been launched; launched: {', '.join(launched) or 'none'}")
            return 1
        sequences = [only] if only is not None else launched
        pending = {sequence for sequence in sequences if peek(sequence).running}
        if pending:
            say(
                f"pausing {', '.join(sorted(pending))} ({reason}). This usually takes seconds and can "
                "take several minutes. If this command is interrupted, run it again: it never signals "
                "an arm twice."
            )
        deadline = time.monotonic() + PAUSE_TIMEOUT_SECS
        next_note = time.monotonic() + 60
        while pending and time.monotonic() < deadline:
            for sequence in sorted(pending):
                view = peek(sequence)
                if not view.running:
                    pending.discard(sequence)
                    continue
                pid = ready_arm_pid(view)
                try:
                    sent = pid is not None and signal_once(pid, sequence=sequence, arm_id=view.arm_id)
                except PermissionError as exc:
                    say(f"FAILED {sequence}: {exc}. Training is still running.")
                    return 1
                if sent:
                    say(f"{sequence}: asked arm {view.arm_id} (pid {pid}) to stop at its next safe point")
            if pending and time.monotonic() >= next_note:
                say(f"still stopping: {', '.join(sorted(pending))}")
                next_note += 60
            if pending:
                time.sleep(0.5)
        if pending:
            say(
                f"STILL-STOPPING {', '.join(sorted(pending))}: the stop request stands and the arm stops "
                "at its next safe point. Do not signal it by hand; run this command again to keep waiting."
            )
            return 3
        states = [sequence_state(sequence) for sequence in sequences]
        for state in states:
            say(describe(state))
        if not states:
            say("nothing has been launched; there is nothing to pause")
        still = running_sequences()
        if still:
            say(f"still running: {', '.join(still)}")
        if all(state.ok for state in states) and not still:
            say("No Phase 60 training is running. It is safe to unplug the charger.")
            return 0
        return 1


# resume


def precheck(arm_id: str) -> int:
    """Run, read-only, the checks the runner makes before it resumes ``arm_id``.

    The same calls in the same order as ``learnability_run.main`` and ``run_arm``: admission with
    ``resume=True``, the one-launch lock, and the checkpoint against the run protocol and the pinned
    module digests. A refusal here launches nothing, so the arm stays resumable once it is fixed;
    the same refusal inside a launched resume would end the arm for the owner.
    """
    sys.path.insert(0, str(ROOT))
    try:
        from pinn.verification import learnability_run as runner

        root = runner._repo_root()
        evidence = root / runner.EVIDENCE_REL
        admission = runner.admit_arm(arm_id, repo_root=root, evidence_root=evidence, resume=True)
        lock = runner.evidence_io._lock_path(evidence)
        if lock.exists():
            raise Refused(f"the launch lock is held: {' '.join(lock.read_text(encoding='utf-8').split())}")
        protocol = runner.load_protocol(repo_root=root, evidence_root=evidence)
        protocol_sha256, module_sha256 = runner._pin_facts(protocol)
        saved = runner.load_resume_checkpoint(
            runner.arm_run_dir(arm_id, repo_root=root), arm_id=arm_id,
            protocol_sha256=protocol_sha256, module_sha256=module_sha256,
        )
        recorded = saved.get("first_omega_0")
        if recorded is not None and float(recorded) != float(admission["first_omega_0"]):
            raise Refused(f"the checkpoint ran at first_omega_0 {recorded}, not {admission['first_omega_0']}")
        if saved["phase"] in ("adam", "polish") and int(saved["budget_steps"]) < 1:
            raise Refused(f"the checkpoint holds the step budget {saved['budget_steps']}")
    except Exception as exc:  # any refusal, of any type, leaves the arm untouched
        print(f"PRECHECK-REFUSED {arm_id}: {type(exc).__name__}: {' '.join(str(exc).split())}")
        return 1
    print(f"PRECHECK-OK {arm_id} {saved['phase']}")
    return 0


def _confirm_resumed(sequence: str, arm_id: str) -> int:
    deadline = time.monotonic() + RESUME_CONFIRM_SECS
    while time.monotonic() < deadline:
        view = peek(sequence)
        if not view.running:
            log = view.invocation.relative_to(ROOT) / "output.log" if view.invocation else "the launch files"
            say(f"{describe(sequence_state(sequence))}; the resumed arm did not keep running (see {log})")
            return 1
        record = arm_process(arm_id)
        if record.get("resume") is True and record.get("pid") in _children(view.supervisor_pid):
            say(f"RESUMED {sequence}: arm {arm_id} is training again (pid {record['pid']}), from where it stopped")
            return 0
        time.sleep(0.5)
    say(f"the resume was launched but arm {arm_id} has not started yet; check the launcher's --status")
    return 0


def resume(only: str | None = None) -> int:
    with control_lock():
        if on_battery():
            say(
                "REFUSED: the Mac is on battery power, so nothing was resumed. Plug in the charger and run "
                "this again (training on battery is slower, and each arm's step budget and polish length "
                "depend on its measured speed)."
            )
            return 1
        launched = launched_sequences()
        if only is not None and only not in launched:
            say(f"REFUSED: {only} has never been launched; launched: {', '.join(launched) or 'none'}")
            return 1
        running = [sequence for sequence in launched if peek(sequence).running]
        if running:
            if only is not None and only not in running:
                say(f"REFUSED: {', '.join(running)} is running; only one sequence runs at a time")
                return 1
            say(f"{', '.join(running)} is already running; nothing to resume")
        else:
            states = [sequence_state(sequence) for sequence in ([only] if only else launched)]
            paused = [state for state in states if state.resumable]
            if len(paused) != 1:
                for state in states:
                    say(describe(state))
                say(
                    "REFUSED: nothing is paused" if not paused
                    else "REFUSED: more than one sequence is paused; name the one to resume"
                )
                return 1
            stopped = paused[0]
            arm_id = stopped.line.split()[1]
            check = _run([sys.executable, "-B", str(Path(__file__).resolve()), "precheck", arm_id], cwd=str(ROOT))
            if check.returncode != 0:
                say(
                    f"REFUSED: the runner would refuse to resume {arm_id}, so nothing was launched and the arm "
                    f"is still resumable once this is fixed: {' '.join((check.stdout + check.stderr).split())}"
                )
                return 1
            launched_resume = _launcher("--sequence", stopped.sequence, "--resume")
            if launched_resume.returncode != 0:
                say(f"REFUSED: {' '.join((launched_resume.stderr or launched_resume.stdout).split())}")
                return 1
            say(launched_resume.stdout.strip())  # the LAUNCHED <sequence> invocation-<n> line
            if _confirm_resumed(stopped.sequence, arm_id) != 0:
                return 1
    return guard_start()


# the power guard


def passed_daily_pause(last: float, now: float) -> bool:
    """Whether the clock passed the daily pause time after ``last`` and by ``now`` (epoch seconds).

    Only a crossing counts, so a run resumed after 09:00 keeps running until the next day's 09:00.
    """
    current = datetime.fromtimestamp(now)
    mark = current.replace(hour=DAILY_PAUSE[0], minute=DAILY_PAUSE[1], second=0, microsecond=0)
    if mark > current:
        mark -= timedelta(days=1)
    return last < mark.timestamp() <= now


def guard_pid() -> int | None:
    try:
        pid = int(GUARD_PID.read_text(encoding="utf-8").strip())
    except (OSError, ValueError):
        return None
    return pid if _alive(pid) and GUARD_COMMAND in _command_of(pid) else None


def guard_run() -> int:
    """The guard loop: pause on battery power and once when the clock passes 09:00; never resume."""
    CONTROL.mkdir(parents=True, exist_ok=True)
    handle = GUARD_LOCK.open("a")
    try:
        fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        say("a power guard is already running")
        return 0
    GUARD_PID.write_text(f"{os.getpid()}\n", encoding="utf-8")
    say(f"power guard started (pid {os.getpid()})")
    last = time.time()
    idle_since = None
    failing = False
    while True:
        now = time.time()
        try:
            running = running_sequences()
            if not running:
                idle_since = now if idle_since is None else idle_since
                if now - idle_since >= GUARD_IDLE_EXIT_SECS:
                    say("nothing is running; the power guard exits")
                    return 0
            else:
                idle_since = None
                if on_battery():
                    reason = "the Mac is on battery power"
                elif passed_daily_pause(last, now):
                    reason = f"the clock passed {DAILY_PAUSE[0]:02d}:{DAILY_PAUSE[1]:02d}"
                else:
                    reason = None
                if reason:
                    say(f"{reason}: pausing {', '.join(running)}")
                    code = pause(reason=reason)
                    notify(
                        f"Paused because {reason}. To continue, plug in and run scripts/phase60-resume.sh."
                        if code == 0 else
                        f"Pausing needs attention (because {reason}). See runs/.phase60-control/guard.log."
                    )
        except Exception as exc:  # a guard that dies quietly would let a run go on past 09:00
            say(f"guard error (it keeps watching and retries this check): {type(exc).__name__}: {exc}")
            if not failing:
                notify("The power guard hit an error. See runs/.phase60-control/guard.log.")
            failing = True
            time.sleep(GUARD_TICK_SECS)
            continue  # keep ``last``, so a 09:00 crossing during a failed check is still seen
        failing = False
        last = now
        time.sleep(GUARD_TICK_SECS)


def guard_start() -> int:
    pid = guard_pid()
    if pid is None:
        CONTROL.mkdir(parents=True, exist_ok=True)
        with GUARD_LOG.open("a", encoding="utf-8") as log:
            child = subprocess.Popen(
                [sys.executable, "-B", str(Path(__file__).resolve()), "guard", "run"],
                cwd=str(ROOT), stdin=subprocess.DEVNULL, stdout=log, stderr=subprocess.STDOUT,
                start_new_session=True, close_fds=True,
            )
        deadline = time.monotonic() + 10
        while pid is None and time.monotonic() < deadline and child.poll() is None:
            time.sleep(0.2)
            pid = guard_pid()
        pid = pid or guard_pid()
        if pid is None:
            say(f"the power guard did not start; see {GUARD_LOG.relative_to(ROOT)}")
            return 1
    say(
        f"the power guard is running (pid {pid}): it pauses training when the Mac goes on battery power "
        f"and when the clock passes {DAILY_PAUSE[0]:02d}:{DAILY_PAUSE[1]:02d}, never resumes it, and exits "
        f"once nothing has run for {GUARD_IDLE_EXIT_SECS // 60} minutes. Log: {GUARD_LOG.relative_to(ROOT)}"
    )
    return 0


def guard_stop() -> int:
    pid = guard_pid()
    if pid is None:
        say("the power guard is not running")
        return 0
    os.kill(pid, signal.SIGTERM)
    deadline = time.monotonic() + 10
    while guard_pid() is not None and time.monotonic() < deadline:
        time.sleep(0.2)
    if guard_pid() is not None:
        say(f"the power guard (pid {pid}) did not stop")
        return 1
    say("the power guard stopped; nothing pauses training automatically until it is started again")
    return 0


def guard_status() -> int:
    pid = guard_pid()
    say(f"the power guard is running (pid {pid})" if pid else "the power guard is not running")
    if GUARD_LOG.exists():
        for line in GUARD_LOG.read_text(encoding="utf-8").splitlines()[-5:]:
            print(f"  {line}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter, allow_abbrev=False,
    )
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("pause").add_argument("sequence", nargs="?")
    commands.add_parser("resume").add_argument("sequence", nargs="?")
    commands.add_parser("guard").add_argument(
        "action", nargs="?", default="start", choices=("start", "stop", "status", "run"),
    )
    commands.add_parser("precheck").add_argument("arm_id")
    args = parser.parse_args(argv)
    if args.command == "pause":
        return pause(args.sequence)
    if args.command == "resume":
        return resume(args.sequence)
    if args.command == "precheck":
        return precheck(args.arm_id)
    return {"start": guard_start, "stop": guard_stop, "status": guard_status, "run": guard_run}[args.action]()


if __name__ == "__main__":
    raise SystemExit(main())
