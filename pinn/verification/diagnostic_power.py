"""Phase 66 (D-08): the fail-closed AC-power launch gate for diagnostic fits.

A registered Phase 66 run starts only through ``launch``, which first reads
``/usr/bin/pmset -g batt``, accepts only an unambiguous first line naming
exactly ``AC Power`` (anything else — battery, UPS, a missing or garbled read,
a nonzero exit or a timeout — refuses before any receipt or run, so nothing is
created), then writes the ``power-gate.json`` receipt beside the declared
output record through the harness's exclusive, canonical, redacted JSON writer
(repo-relative paths only; the redaction guard refuses home-directory text, so
the interpreter path is never recorded), and only then starts the fit CLI as a
child: ``caffeinate -is <interpreter> -B -m pinn.verification.diagnostic_fit
run`` over a fixed argv list with no shell and the repository root as the
child's working directory.

Plan 66-02 completes the gate (D-08): launch also enforces the owner's verbatim
compute window in code — ``require_weekend_window`` passes only on Saturday or
on Sunday before 22:00 in ``WINDOW_TIMEZONE``, refusing a naive clock or an
unloadable zone — and runs, before the receipt, the output-exists precheck and
the metadata-only ``check_fit_registration`` admission precheck, so a spent
directory or an inadmissible registration creates nothing. The read-only
``check`` subcommand prints the gate's verdict and writes nothing. The gate
checks at launch only; the receipt (which now records the window) makes
compliance auditable.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

from pinn.verification.learnability_arms import FirstResultExists, write_record_exclusive

__all__ = [
    "AC_SOURCE",
    "CAFFEINATE",
    "FIT_MODULE",
    "PMSET",
    "RECEIPT_NAME",
    "RECEIPT_SCHEMA",
    "PowerRefused",
    "WINDOW_SUNDAY_LAST_HOUR",
    "WINDOW_TIMEZONE",
    "launch",
    "main",
    "power_source",
    "require_ac_power",
    "require_remaining_window",
    "require_weekend_window",
    "weekend_closing_utc",
]

PMSET = "/usr/bin/pmset"
CAFFEINATE = "/usr/bin/caffeinate"
AC_SOURCE = "AC Power"
RECEIPT_NAME = "power-gate.json"
RECEIPT_SCHEMA = "phase66-power-gate/v1"
FIT_MODULE = "pinn.verification.diagnostic_fit"

#: The owner's compute window (D-08, verbatim: plugged in "for the weekend
#: only. not weekdays"), checked in code as the conservative reading.
WINDOW_TIMEZONE = "America/Chicago"
#: Sunday's last admitted local hour: the window ends at 22:00. Every admitted
#: registration's whole-run cap is strictly below 3,600 seconds, so a run
#: launched before Sunday 22:00 ends before Sunday 23:00 even at the full cap
#: plus termination grace — no run spills into a weekday.
WINDOW_SUNDAY_LAST_HOUR = 22

#: The only acceptable pmset first line: an anchored positive match, first
#: line only, so a later-line mention never reads as safe.
_POWER_LINE = re.compile(r"^Now drawing from '([^']+)'$")


class PowerRefused(RuntimeError):
    """The AC-power precondition does not hold; nothing is written or run."""


def power_source(text):
    """The quoted power source in ``text``'s first line, or ``None``."""
    first = text.splitlines()[0] if text else ""
    match = _POWER_LINE.match(first)
    return match.group(1) if match else None


def _read_pmset_text():
    """The default pmset read: fixed argv, no shell, 10-second bound."""
    completed = subprocess.run(
        [PMSET, "-g", "batt"],
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        check=False,
        timeout=10.0,
    )
    if completed.returncode != 0:
        raise PowerRefused(
            f"{PMSET} -g batt exited {completed.returncode}; refusing to launch"
        )
    return completed.stdout


def require_ac_power(read_power=None):
    """The pmset first line, and only when it names exactly ``AC_SOURCE``.

    Fail closed: an OSError, a timeout, a nonzero exit or any other power
    source raises :class:`PowerRefused` before a receipt or a run. Returns the
    first line of the pmset text. The Phase 60 ``on_battery`` helper is
    fail-open and is deliberately not reused.
    """
    reader = _read_pmset_text if read_power is None else read_power
    try:
        text = reader()
    except PowerRefused:
        raise
    except Exception as exc:  # OSError, timeout, or an injected reader: fail closed
        raise PowerRefused(
            f"the pmset power read failed: {type(exc).__name__}: {exc}"
        ) from exc
    source = power_source(text)
    if source != AC_SOURCE:
        raise PowerRefused(
            f"the Mac is not on AC power; pmset reports {source!r}; refusing to launch"
        )
    return text.splitlines()[0]


def require_weekend_window(now=None):
    """The owner's weekend compute window (D-08): Saturday, Sunday to 22:00.

    ``now`` is an injected clock: a zero-argument callable returning an aware
    ``datetime``. The default clock is ``datetime.now(ZoneInfo(WINDOW_TIMEZONE))``.
    The instant — whichever clock gave it — is converted to
    ``WINDOW_TIMEZONE`` before the check, so a UTC instant reads as its Chicago
    local time. It passes on isoweekday 6 (Saturday) and on isoweekday 7
    (Sunday) before ``WINDOW_SUNDAY_LAST_HOUR``:00 local, returning the local
    datetime. A naive datetime, a failed zone lookup, or any time outside the
    window raises :class:`PowerRefused` naming the local time; nothing is
    written or run by the caller on a refusal.
    """
    try:
        zone = ZoneInfo(WINDOW_TIMEZONE)
    except Exception as exc:  # ZoneInfoNotFoundError and friends: fail closed
        raise PowerRefused(
            f"the window time zone {WINDOW_TIMEZONE!r} cannot be loaded: "
            f"{type(exc).__name__}: {exc}"
        ) from exc
    moment = datetime.now(zone) if now is None else now()
    if moment.tzinfo is None or moment.tzinfo.utcoffset(moment) is None:
        raise PowerRefused(
            "the window clock gave a naive datetime; refusing to launch"
        )
    local = moment.astimezone(zone)
    weekday = local.isoweekday()
    if weekday == 6 or (weekday == 7 and local.hour < WINDOW_SUNDAY_LAST_HOUR):
        return local
    raise PowerRefused(
        f"the local time {local.isoformat(timespec='seconds')} is outside the "
        "owner's weekend window (Saturday, or Sunday before "
        f"{WINDOW_SUNDAY_LAST_HOUR:02d}:00 in {WINDOW_TIMEZONE}); refusing to launch"
    )


def weekend_closing_utc(local):
    """This weekend's Sunday 22:00 closing instant, as an aware UTC datetime.

    ``local`` is the aware local datetime the weekend window check returned
    (Saturday or Sunday in ``WINDOW_TIMEZONE``). A Saturday derives the next
    day's 22:00; a Sunday the same day's. The closing instant is constructed
    on the Chicago wall clock (so a DST transition inside the weekend is
    exact) and converted to UTC, where all duration arithmetic happens.
    """
    if not isinstance(local, datetime) or local.tzinfo is None \
            or local.tzinfo.utcoffset(local) is None:
        raise PowerRefused("the closing instant needs an aware local datetime")
    if local.isoweekday() == 6:
        day = local.date() + timedelta(days=1)
    elif local.isoweekday() == 7:
        day = local.date()
    else:
        raise PowerRefused(
            f"the local time {local.isoformat(timespec='seconds')} has no "
            "weekend closing instant; it is outside the owner's window"
        )
    closing = datetime(
        day.year, day.month, day.day,
        int(WINDOW_SUNDAY_LAST_HOUR), 0, 0,
        tzinfo=ZoneInfo(WINDOW_TIMEZONE),
    )
    return closing.astimezone(timezone.utc)


def require_remaining_window(cap_seconds, *, local=None, now=None):
    """The full-cap remaining-window admission (plan 67-06, D-07/D-10).

    The existing launch-time weekend check establishes only that the instant
    sits inside the window; this check establishes that the ENTIRE
    registered whole-launch allowance fits before the weekend closes:
    ``current_instant + cap_seconds <= closing_instant`` with the closing
    instant derived as Sunday 22:00 ``WINDOW_TIMEZONE`` and every duration
    computed between aware UTC instants (a DST transition inside the weekend
    is therefore exact). Exact equality is admitted; the next instant beyond
    the boundary refuses. Returns the closing instant, the remaining
    allowance and the cap, so a receipt can record independently recheckable
    evidence. Raises :class:`PowerRefused` (never a silent pass).
    """
    if isinstance(cap_seconds, bool) or not isinstance(cap_seconds, (int, float)) \
            or not 0 < float(cap_seconds):
        raise PowerRefused(
            f"the whole-launch cap must be a positive number of seconds; "
            f"got {cap_seconds!r}"
        )
    cap = float(cap_seconds)
    if local is None:
        local = require_weekend_window(now)
    closing = weekend_closing_utc(local)
    current = local.astimezone(timezone.utc)
    remaining = (closing - current).total_seconds()
    if current + timedelta(seconds=cap) > closing:
        raise PowerRefused(
            f"the remaining weekend allowance is {remaining:g} seconds before "
            f"the Sunday {WINDOW_SUNDAY_LAST_HOUR:02d}:00 closing instant "
            f"({closing.isoformat()}); the registered {cap:g}-second "
            "whole-launch allowance does not fit, so nothing is launched"
        )
    return {
        "cap_seconds": cap,
        "closing_utc": closing.isoformat(),
        "remaining_allowance_seconds": remaining,
    }


def _default_run(argv, *, cwd):
    """The default runner: a fixed argv child under caffeinate, no shell."""
    return subprocess.run(argv, cwd=str(cwd), check=False).returncode


def launch(registration, output, *, repo_root=None, read_power=None, run=None, now=None):
    """Gate, precheck, write the receipt, then start the fit CLI.

    The order is fixed (D-08): 1 the AC check; 2 the weekend window; 3 the
    registration and output are resolved against the repository root (the
    directory three levels above this file by default) and refused if they
    resolve outside it; 4 the output-exists precheck; 5 the metadata-only
    ``check_fit_registration`` admission precheck; 6 the receipt is written
    exclusively beside the declared record (a ``FirstResultExists`` means the
    directory is spent); 7 ``POWER-OK`` is printed; 8 the runner starts the
    fit CLI with the repository root as its cwd. Any refusal before step 8
    prints ``POWER-REFUSED: <reason>`` to stderr and returns 2, having created
    nothing. The gate never converts a refusal into a different run: no CPU
    fallback, no other output and no retry.
    """
    try:
        first_line = require_ac_power(read_power=read_power)
        source = power_source(first_line)
        local = require_weekend_window(now)
        root = (
            Path(repo_root) if repo_root is not None
            else Path(__file__).resolve().parents[2]
        ).resolve()
        registration_path = Path(registration)
        output_path = Path(output)
        if not registration_path.is_absolute():
            registration_path = root / registration_path
        if not output_path.is_absolute():
            output_path = root / output_path
        registration_path = registration_path.resolve()
        output_path = output_path.resolve()
        try:
            registration_relative = registration_path.relative_to(root).as_posix()
            output_relative = output_path.relative_to(root).as_posix()
        except ValueError as exc:
            raise PowerRefused(
                "the registration and output must resolve inside the repository; "
                f"got {registration_path} and {output_path}"
            ) from exc
        if output_path.exists():
            raise PowerRefused(
                f"an output record already exists at {output_relative}; the first "
                "completed run is the result and a second run never replaces it"
            )
        # Deferred: the metadata-only admission precheck runs before the
        # receipt, so an inadmissible registration creates nothing.
        from pinn.verification.diagnostic_fit import (
            DiagnosticFitRefused,
            check_fit_registration,
        )
        from pinn.verification.diagnostic_guard import DiagnosticRegistrationRefused

        try:
            check_fit_registration(registration_path, repo_root=root)
        except (DiagnosticFitRefused, DiagnosticRegistrationRefused) as exc:
            raise PowerRefused(
                f"the registration does not admit a launch: {exc}"
            ) from exc
        receipt_path = output_path.parent / RECEIPT_NAME
        receipt_relative = receipt_path.relative_to(root).as_posix()
        write_record_exclusive(
            receipt_path,
            {
                "schema": RECEIPT_SCHEMA,
                "checked_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "power_source": source,
                "pmset_first_line": first_line,
                "registration": registration_relative,
                "output": output_relative,
                "load_average": [float(value) for value in os.getloadavg()],
                "launched": {"module": FIT_MODULE, "subcommand": "run"},
                "window": {
                    "timezone": WINDOW_TIMEZONE,
                    "local_time": local.isoformat(timespec="seconds"),
                    "isoweekday": int(local.isoweekday()),
                },
            },
        )
    except (PowerRefused, FirstResultExists) as exc:
        print(f"POWER-REFUSED: {exc}", file=sys.stderr)
        return 2
    print(
        f"POWER-OK source={source} isoweekday={local.isoweekday()} "
        f"receipt={receipt_relative}"
    )
    runner = _default_run if run is None else run
    argv = [
        CAFFEINATE,
        "-is",
        sys.executable,
        "-B",
        "-m",
        FIT_MODULE,
        "run",
        "--registration",
        str(registration_path),
        "--output",
        str(output_path),
    ]
    return int(runner(argv, cwd=str(root)))


def main(argv=None, *, repo_root=None, read_power=None, run=None, now=None):
    """The launcher CLI: ``launch --registration R --output O`` and ``check``.

    ``check`` is read-only: it runs the AC check and the weekend window only,
    prints the verdict token, and returns 0 or 2 (the gate's live verdict).
    An unknown command or missing flags return 2, mirroring the
    ``diagnostic_fit`` CLI's required-flags convention.
    """
    parser = argparse.ArgumentParser(
        prog="diagnostic_power",
        description=(
            "AC-power launch gate: refuse on battery or outside the weekend "
            "window, write the power-gate receipt, then start the registered "
            "diagnostic fit; check prints the read-only verdict."
        ),
    )
    commands = parser.add_subparsers(dest="command")
    launch_command = commands.add_parser("launch")
    launch_command.add_argument("--registration", required=False)
    launch_command.add_argument("--output", required=False)
    commands.add_parser("check")
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:  # argparse's own usage error carries exit code 2
        return int(exc.code) if isinstance(exc.code, int) else 2
    if args.command == "check":
        try:
            first_line = require_ac_power(read_power=read_power)
            source = power_source(first_line)
            local = require_weekend_window(now)
        except PowerRefused as exc:
            print(f"POWER-REFUSED: {exc}", file=sys.stderr)
            return 2
        print(f"POWER-OK source={source} isoweekday={local.isoweekday()}")
        return 0
    if args.command != "launch":
        print("POWER-REFUSED: choose launch or check", file=sys.stderr)
        return 2
    missing = [
        f"--{name}"
        for name in ("registration", "output")
        if getattr(args, name) is None
    ]
    if missing:
        print(
            f"POWER-REFUSED: missing required flags: {', '.join(missing)}",
            file=sys.stderr,
        )
        return 2
    return launch(
        args.registration,
        args.output,
        repo_root=repo_root,
        read_power=read_power,
        run=run,
        now=now,
    )


if __name__ == "__main__":
    sys.exit(main())
