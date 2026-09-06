#!/usr/bin/env bash
# Phase 55 (architecture characterization probe) stale-aware close predicate.
# Mirrors 54-CLOSE-CHECK.sh: mutating `gsd-tools` state verbs corrupt STATE.md in
# this checkout (see STATE.md "Note on this file's own history" / Phase-54
# transition note), so `phase complete` is NOT used. This script asserts the
# substantive close gates re-derivably; STATE.md / ROADMAP.md are then updated by
# hand. Terminal literal: PHASE55-CLOSE-PASS.
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
cd "$repo_root"

phase_dir=.planning/phases/55-architecture-characterization-probe
verification="$phase_dir/55-VERIFICATION.md"
validation="$phase_dir/55-VALIDATION.md"
security="$phase_dir/55-SECURITY.md"
uat="$phase_dir/55-UAT.md"
coverage="$phase_dir/55-COVERAGE.md"

# initial verification commit — every code/test/evidence covered file must be
# byte-identical to this tree (the re-verification at HEAD confirmed the same).
initial_verify_commit=48e3e2fa

fail() { printf 'PHASE55-CLOSE-FAIL %s\n' "$1" >&2; exit 1; }

for required in "$verification" "$validation" "$security" "$uat" "$coverage"; do
  test -f "$required" || fail "missing=$required"
done

# ── verification ──────────────────────────────────────────────────────────────
v_status="$(awk -F': ' '/^status:/{print $2; exit}' "$verification")"
v_score="$(awk -F': ' '/^score:/{print $2; exit}' "$verification")"
test "$v_status" = passed || fail "verification_status=$v_status"
case "$v_score" in 12/12*) ;; *) fail "verification_score=$v_score";; esac
grep -q '^re_verification:' "$verification" || fail 'no_reverification_block'

# code / test / evidence covered files unchanged since the initial verification
code_paths=(
  pinn/verification/architecture_characterization_probe.py
  tests/phase38/test_prohibitions.py
  tests/phase55/__init__.py
  tests/phase55/test_architecture_characterization.py
  tests/phase55/fixtures/six_case_baseline.json
  "$phase_dir/evidence/probe/20260906T035209Z/raw.json"
  "$phase_dir/evidence/probe/20260906T035209Z/summary.md"
  "$phase_dir"/55-0*-PLAN.md
  "$phase_dir"/55-0*-SUMMARY.md
  "$phase_dir/55-CONTEXT.md"
)
test -z "$(git diff "$initial_verify_commit" HEAD --stat -- "${code_paths[@]}")" \
  || fail 'code_covered_files_changed_since_initial_verification'

# ── validation (nyquist) ─────────────────────────────────────────────────────
val_status="$(awk -F': ' '/^status:/{print $2; exit}' "$validation")"
nyquist="$(awk -F': ' '/^nyquist_compliant:/{print $2; exit}' "$validation")"
test "$val_status" = validated || fail "validation_status=$val_status"
test "$nyquist" = true || fail "nyquist_compliant=$nyquist"

# ── security ─────────────────────────────────────────────────────────────────
sec_status="$(awk -F': ' '/^status:/{print $2; exit}' "$security")"
threats_open="$(awk -F': ' '/^threats_open:/{print $2; exit}' "$security")"
threat_rows="$(grep -c '^| T-55-' "$security")"
test "$sec_status" = verified || fail "security_status=$sec_status"
test "$threats_open" -eq 0 || fail "threats_open=$threats_open"
test "$threat_rows" -eq 21 || fail "threat_rows=$threat_rows"

# ── uat ──────────────────────────────────────────────────────────────────────
uat_status="$(awk -F': ' '/^status:/{print $2; exit}' "$uat")"
uat_passes="$(grep -c '^result: pass$' "$uat")"
test "$uat_status" = complete || fail "uat_status=$uat_status"
test "$uat_passes" -eq 20 || fail "uat_passes=$uat_passes"
grep -qi '^no external api integration' "$coverage" || fail 'coverage_declaration_missing'

# ── plans / summaries ────────────────────────────────────────────────────────
plans="$(find "$phase_dir" -maxdepth 1 -name '55-*-PLAN.md' | wc -l | tr -d ' ')"
summaries="$(find "$phase_dir" -maxdepth 1 -name '55-*-SUMMARY.md' | wc -l | tr -d ' ')"
test "$plans" -eq 4 || fail "plans=$plans"
test "$summaries" -eq 4 || fail "summaries=$summaries"

# ── REQUIREMENTS / ROADMAP closeout flips ────────────────────────────────────
grep -q '^- \[x\] \*\*INST-04\*\*' .planning/REQUIREMENTS.md || fail 'inst04_unchecked'
grep -q '^| INST-04 | Phase 55 | Complete |$' .planning/REQUIREMENTS.md || fail 'inst04_traceability'
grep -q '^- \[x\] \*\*Phase 55:' .planning/ROADMAP.md || fail 'roadmap_phase55_unchecked'

# ── canonical GSD predicates (read-only) ─────────────────────────────────────
GSD_TOOLS="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/gsd-core/bin/gsd-tools.cjs"
gsd_run() { node "$GSD_TOOLS" "$@"; }
gsd_run query verification.status "$phase_dir" | grep -q '"status": "passed"' \
  || fail 'canonical_verification_not_passed'
gsd_run phase uat-passed 55 --require-verification | grep -q '"passed": true' \
  || fail 'completion_predicate_false'

git diff --check || fail 'diff_check'

printf 'PHASE55-CLOSE-PASS verification=%s score=%s validation=%s nyquist=%s security=%s threats_open=%s uat=%s/%s plans=%s/%s next=56\n' \
  "$v_status" "$v_score" "$val_status" "$nyquist" "$sec_status" "$threats_open" \
  "$uat_passes" 20 "$plans" "$summaries"
