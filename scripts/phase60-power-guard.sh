#!/usr/bin/env bash
# Phase 60 power guard: pause training automatically when the laptop cannot stay on its charger.
#
# Usage: scripts/phase60-power-guard.sh [start|stop|status]    (default: start)
#
# start   Start the guard in the background (once; a second start reports the running one).
#         scripts/phase60-resume.sh starts it by itself; after a fresh launch, start it by hand.
# stop    Stop it, for a day when training should run on past 09:00.
# status  Whether it runs, and the last lines of runs/.phase60-control/guard.log.
#
# Every 30 seconds it looks for a running Phase 60 sequence (any sequence). It pauses the way
# scripts/phase60-pause.sh does when the Mac is on battery power, and once when the clock passes 09:00
# (a run resumed after 09:00 keeps going until the next day's 09:00). It never resumes anything,
# and it exits once nothing has run for 10 minutes.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec <home>/miniforge3/envs/pinn-train/bin/python -B "$ROOT/scripts/phase60_run_control.py" guard "$@"
