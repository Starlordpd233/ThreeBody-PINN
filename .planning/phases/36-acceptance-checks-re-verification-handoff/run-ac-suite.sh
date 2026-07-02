#!/usr/bin/env bash
# run-ac-suite.sh — re-run the full v1.6 acceptance suite as fresh disposable Phase-36 probes
# and emit one result line per acceptance check (VER-13 / VER-15, D-36-05).
#
# Suite = 26 probes (one per manifest row + protected-path guard).
# No probe touches pinn/ production code (VER-15 / SCOPE-10). Probes read only
# ctl_instruction.md, pinn_architecture.md, and the probes/ directory itself.

cd "$(git rev-parse --show-toplevel)" || exit 2
H=".planning/phases/36-acceptance-checks-re-verification-handoff/probes"
LOG="$(mktemp -t ac-suite.XXXXXX)"
trap 'rm -f "$LOG"' EXIT

PASS=0
FAIL=0

line() { # $1 = label, $2... = command
  local label="$1"; shift
  if "$@" >>"$LOG" 2>&1; then
    echo "$label: PASS"
    PASS=$((PASS + 1))
  else
    echo "$label: FAIL"
    FAIL=$((FAIL + 1))
  fi
}

echo "=== v1.6 Acceptance Suite — fresh Phase-36 re-run ($(date -u +%Y-%m-%dT%H:%M:%SZ)) ==="

# CURR probes
line "AC-CURR-01" bash "$H/ac-curr-01.sh"
line "AC-CURR-02-LMAX" python3 "$H/ac-curr-02-lmax.py"
line "AC-CURR-02-M7" bash "$H/ac-curr-02-m7.sh"
line "AC-CURR-03" bash "$H/ac-curr-03.sh"
line "AC-CURR-04" bash "$H/ac-curr-04.sh"
line "AC-CURR-05" bash "$H/ac-curr-05.sh"

# LOOP probes
line "AC-LOOP-01" bash "$H/ac-loop-01.sh"
line "AC-LOOP-02" bash "$H/ac-loop-02.sh"
line "AC-LOOP-04" python3 "$H/ac-loop-04.py"
line "AC-LOOP-05" bash "$H/ac-loop-05.sh"
line "AC-LOOP-06" bash "$H/ac-loop-06.sh"
line "LOOP-07" bash "$H/ac-loop-07.sh"
line "LOOP-08" bash "$H/ac-loop-08.sh"

# LOSS probes
line "AC-LOSS-01" bash "$H/ac-loss-01.sh"
line "AC-LOSS-01-AD" python3 "$H/ac-loss-01-ad.py"
line "AC-LOSS-02" python3 "$H/ac-loss-02.py"
line "AC-LOSS-03" bash "$H/ac-loss-03.sh"
line "AC-LOSS-04" bash "$H/ac-loss-04.sh"

# EVID-15 headline probes
line "AC-EVID-15-D-CONFLICT" bash "$H/ac-evid-15-d-conflict.sh"
line "AC-EVID-15-D05" bash "$H/ac-evid-15-d05.sh"
line "AC-EVID-15-D06" bash "$H/ac-evid-15-d06.sh"

# SI probes
line "SI-CTL-001" bash "$H/ac-si-ctl-001.sh"
line "SI-PINN-002" bash "$H/ac-si-pinn-002.sh"
line "SI-PINN-003" bash "$H/ac-si-pinn-003.sh"
line "SI-DQA-003" bash "$H/ac-si-dqa-003.sh"

# Protected-path guard
line "PROTECTED-PATH-GUARD" bash "$H/ac-protected-path-guard.sh"

echo "=== summary: ${PASS} pass / ${FAIL} fail (expect 26 pass, 0 fail) ==="
[ "$FAIL" -eq 0 ]