#!/usr/bin/env bash
# Phase 60: resume a paused learnability sequence from its checkpoint, then start the power guard.
#
# Usage: scripts/phase60-resume.sh [SEQUENCE]    (default: the one paused sequence)
#
# It refuses on battery power. Before it launches anything it asks the runner, read-only, the
# questions the runner asks before it resumes (admission, the launch lock, the checkpoint against
# the run protocol and the pinned modules), so a resume that would be refused launches nothing and
# the arm stays resumable. It then runs the launcher's --resume (printing its LAUNCHED line),
# confirms the arm is training again, and starts scripts/phase60-power-guard.sh.
#
# Exit 0: resumed (or already running). Exit 1: refused, and why.
# How it works: scripts/phase60_run_control.py.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec <home>/miniforge3/envs/pinn-train/bin/python -B "$ROOT/scripts/phase60_run_control.py" resume "$@"
