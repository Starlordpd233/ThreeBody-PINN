#!/usr/bin/env bash
set -euo pipefail

command -v caffeinate >/dev/null 2>&1 || {
  echo "error: caffeinate not found (macOS required for the unattended wrapper)" >&2
  exit 127
}

exec caffeinate -is python -m pinn.train "$@"
