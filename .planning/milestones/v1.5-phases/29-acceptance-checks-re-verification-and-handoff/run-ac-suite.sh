#!/usr/bin/env bash
# run-ac-suite.sh — re-run the full v1.5 acceptance suite as fresh disposable Phase-29 probes
# and emit one result line per acceptance check (VER-07 / VER-09, D-02).
#
# Suite = 13 ledger-mapped checks. AC-PIPE-08 (stage-query) has no standalone ledger row; it
# is re-run inside the AC-PIPE-04 / G5 (M12) family line and noted under G5 (matching the
# 29-UAT table shape). The 3 already-persisted probes (ac-pipe-04/08/09.sh under Phase 27)
# are re-run in place; the other 10 are the lightweight probes authored in this phase dir.
#
# No probe touches pinn/ production code (VER-09 / SCOPE-10). Probes read only
# ctl_instruction.md, pinn_architecture.md, and simulation_data/.

cd "$(git rev-parse --show-toplevel)" || exit 2
H=".planning/phases/29-acceptance-checks-re-verification-and-handoff"
P27=".planning/phases/27-sampling-precision-and-global-scale-contracts"
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

echo "=== v1.5 Acceptance Suite — fresh Phase-29 re-run ($(date -u +%Y-%m-%dT%H:%M:%SZ)) ==="

line "AC-PIPE-01" bash "$H/ac-pipe-01.sh"
line "AC-PIPE-02" bash "$H/ac-pipe-02.sh"
line "AC-PIPE-03" bash "$H/ac-pipe-03.sh"

# AC-PIPE-04 line covers the M12/G5 family: AC-PIPE-04 plus the AC-PIPE-08 stage-query probe
# (noted under G5; no standalone ledger row). Both persisted probes must pass.
if bash "$P27/ac-pipe-04.sh" >>"$LOG" 2>&1 && bash "$P27/ac-pipe-08.sh" >>"$LOG" 2>&1; then
  echo "AC-PIPE-04: PASS (M12/G5 family; AC-PIPE-08 stage-query re-run PASS, noted under G5)"
  PASS=$((PASS + 1))
else
  echo "AC-PIPE-04: FAIL (M12/G5 family; includes AC-PIPE-08 stage-query)"
  FAIL=$((FAIL + 1))
fi

line "AC-PIPE-05" python3 "$H/ac-pipe-05.py"
line "AC-PIPE-06" bash "$H/ac-pipe-06.sh"
line "AC-PIPE-07" bash "$H/ac-pipe-07.sh"
line "AC-PIPE-09" bash "$P27/ac-pipe-09.sh"
line "AC-PIPE-10" bash "$H/ac-pipe-10.sh"
line "AC-VAL-01"  bash "$H/ac-val-01.sh"
line "AC-VAL-02"  bash "$H/ac-val-02.sh"
line "AC-VAL-03"  bash "$H/ac-val-03.sh"

# AC-VAL-04 is a two-axis split: structural executes now; numeric is deferred to FUT-01 FO-2.
if bash "$H/ac-val-04.sh" >>"$LOG" 2>&1; then
  echo "AC-VAL-04: STRUCTURAL PASS; NUMERIC: DEFERRED (FUT-01 FO-2)"
  PASS=$((PASS + 1))
else
  echo "AC-VAL-04: STRUCTURAL FAIL; NUMERIC: DEFERRED (FUT-01 FO-2)"
  FAIL=$((FAIL + 1))
fi

echo "=== summary: ${PASS} pass-or-structural-pass / ${FAIL} fail (expect 12 PASS + AC-VAL-04 split, 0 fail) ==="
[ "$FAIL" -eq 0 ]
