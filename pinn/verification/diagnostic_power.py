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
child's working directory. The gate checks at launch only; the receipt makes
compliance auditable. Plan 66-02 adds the check subcommand, the
output-exists and admission prechecks, and the full refusal matrix.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from pinn.verification.learnability_arms import FirstResultExists, write_record_exclusive

__all__ = [
    "AC_SOURCE",
    "CAFFEINATE",
    "FIT_MODULE",
    "PMSET",
    "RECEIPT_NAME",
    "RECEIPT_SCHEMA",
    "PowerRefused",
    "launch",
    "main",
    "power_source",
    "require_ac_power",
]

PMSET = "/usr/bin/pmset"
CAFFEINATE = "/usr/bin/caffeinate"
AC_SOURCE = "AC Power"
RECEIPT_NAME = "power-gate.json"
RECEIPT_SCHEMA = "phase66-power-gate/v1"
FIT_MODULE = "pinn.verification.diagnostic_fit"

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


def _default_run(argv, *, cwd):
    """The default runner: a fixed argv child under caffeinate, no shell."""
    return subprocess.run(argv, cwd=str(cwd), check=False).returncode


def launch(registration, output, *, repo_root=None, read_power=None, run=None):
    """Gate, write the receipt, then start the fit CLI; return its exit code.

    Order is fixed: the AC check first; then the registration and output are
    resolved against the repository root (the directory three levels above
    this file by default) and refused if they resolve outside it; then the
    receipt is written exclusively beside the declared record; only then the
    runner starts the fit CLI with the repository root as its cwd. Any refusal
    before the runner prints ``POWER-REFUSED: <reason>`` to stderr and returns
    2, having created nothing (on battery nothing at all is created).
    """
    try:
        first_line = require_ac_power(read_power=read_power)
        source = power_source(first_line)
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
        write_record_exclusive(
            output_path.parent / RECEIPT_NAME,
            {
                "schema": RECEIPT_SCHEMA,
                "checked_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "power_source": source,
                "pmset_first_line": first_line,
                "registration": registration_relative,
                "output": output_relative,
                "load_average": [float(value) for value in os.getloadavg()],
                "launch": {"module": FIT_MODULE, "subcommand": "run"},
            },
        )
    except (PowerRefused, FirstResultExists) as exc:
        print(f"POWER-REFUSED: {exc}", file=sys.stderr)
        return 2
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


def main(argv=None, *, repo_root=None, read_power=None, run=None):
    """The launcher CLI: ``launch --registration R --output O`` (exit 0 or 2)."""
    parser = argparse.ArgumentParser(
        prog="diagnostic_power",
        description=(
            "AC-power launch gate: refuse on battery, write the power-gate "
            "receipt, then start the registered diagnostic fit."
        ),
    )
    commands = parser.add_subparsers(dest="command")
    launch_command = commands.add_parser("launch")
    launch_command.add_argument("--registration", required=False)
    launch_command.add_argument("--output", required=False)
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:  # argparse's own usage error carries exit code 2
        return int(exc.code) if isinstance(exc.code, int) else 2
    if args.command != "launch":
        print("POWER-REFUSED: choose launch", file=sys.stderr)
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
    )


if __name__ == "__main__":
    sys.exit(main())
