#!/usr/bin/env bash
# Phase 60: pause the running learnability sequence so it can resume later from its checkpoint.
#
# Usage: scripts/phase60-pause.sh [SEQUENCE]     (default: every running Phase 60 sequence)
#
# It asks the running arm to stop at its next safe point (one SIGINT, sent only once the arm can
# take it), waits until the whole sequence has stopped, and reports whether the stop can resume.
# This usually takes seconds and can take several minutes. If the command is interrupted, run it
# again: it never signals an arm twice. Never signal an arm by hand on top of it.
#
# Exit 0: nothing is training, and every stopped sequence can resume (or is complete).
# Exit 1: a stop the owner must look at. Exit 3: still stopping after 30 minutes (run it again).
# How it works: scripts/phase60_run_control.py.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec <home>/miniforge3/envs/pinn-train/bin/python -B "$ROOT/scripts/phase60_run_control.py" pause "$@"
