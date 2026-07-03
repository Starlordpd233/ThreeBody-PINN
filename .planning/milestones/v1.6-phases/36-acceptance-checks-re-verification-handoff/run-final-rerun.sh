#!/usr/bin/env bash
# run-final-rerun.sh — final batch re-verify for Plan 36-05 (Task 3).
# Writes to evidence/final-rerun/ (NOT overwriting 36-02's sealed evidence/).
# PYTHONHASHSEED=0 for hash/dict ordering determinism.

cd "$(git rev-parse --show-toplevel)" || exit 2

export PYTHONHASHSEED=0
H=".planning/phases/36-acceptance-checks-re-verification-handoff/probes"
EVID=".planning/phases/36-acceptance-checks-re-verification-handoff/evidence/final-rerun"
mkdir -p "$EVID" || exit 2

PASS=0; FAIL=0
line() {
  local label="$1"; local ev="$EVID/${label}.stdout.txt"; shift
  if "$@" >"$ev" 2>&1; then
    echo "$label: PASS"
    PASS=$((PASS+1))
  else
    echo "$label: FAIL"
    FAIL=$((FAIL+1))
  fi
}

echo "=== v1.6 Final Re-verify — $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "Python environment:"
python3 --version | tee "$EVID/python_environment.stdout.txt"
git rev-parse HEAD >> "$EVID/python_environment.stdout.txt"
echo "PYTHONHASHSEED=0" >> "$EVID/python_environment.stdout.txt"

# CURR
line "AC-CURR-01" bash "$H/ac-curr-01.sh"
line "AC-CURR-02-LMAX" python3 "$H/ac-curr-02-lmax.py"
line "AC-CURR-02-M7" bash "$H/ac-curr-02-m7.sh"
line "AC-CURR-03" bash "$H/ac-curr-03.sh"
line "AC-CURR-04" bash "$H/ac-curr-04.sh"
line "AC-CURR-05" bash "$H/ac-curr-05.sh"

# LOOP
line "AC-LOOP-01" bash "$H/ac-loop-01.sh"
line "AC-LOOP-02" bash "$H/ac-loop-02.sh"
line "AC-LOOP-04" python3 "$H/ac-loop-04.py"
line "AC-LOOP-05" bash "$H/ac-loop-05.sh"
line "AC-LOOP-06" bash "$H/ac-loop-06.sh"
line "LOOP-07" bash "$H/ac-loop-07.sh"
line "LOOP-08" bash "$H/ac-loop-08.sh"

# LOSS
line "AC-LOSS-01" bash "$H/ac-loss-01.sh"
line "AC-LOSS-01-AD" python3 "$H/ac-loss-01-ad.py"
line "AC-LOSS-02" python3 "$H/ac-loss-02.py"
line "AC-LOSS-03" bash "$H/ac-loss-03.sh"
line "AC-LOSS-04" bash "$H/ac-loss-04.sh"

# EVID-15
line "AC-EVID-15-D-CONFLICT" bash "$H/ac-evid-15-d-conflict.sh"
line "AC-EVID-15-D05" bash "$H/ac-evid-15-d05.sh"
line "AC-EVID-15-D06" bash "$H/ac-evid-15-d06.sh"

# SI
line "SI-CTL-001" bash "$H/ac-si-ctl-001.sh"
line "SI-PINN-002" bash "$H/ac-si-pinn-002.sh"
line "SI-PINN-003" bash "$H/ac-si-pinn-003.sh"
line "SI-DQA-003" bash "$H/ac-si-dqa-003.sh"

# Protected-path
line "PROTECTED-PATH-GUARD" bash "$H/ac-protected-path-guard.sh"

# Companion traceability probe
line "AC-TRACEABILITY" python3 "$H/ac-traceability.py"

echo "=== summary: ${PASS} pass / ${FAIL} fail ==="
[ "$FAIL" -eq 0 ]
