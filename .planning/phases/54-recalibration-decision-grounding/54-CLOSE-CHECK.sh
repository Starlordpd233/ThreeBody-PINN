#!/usr/bin/env bash
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
cd "$repo_root"

phase_dir=.planning/phases/54-recalibration-decision-grounding
ruling="$phase_dir/54-RULING.md"
gaps="$phase_dir/54-GAPS.md"
gap_index=.planning/milestones/v2.3-GAPS.md
candidate=pinn_instruction/markdown_conversion/framework-specs/trainex-r3/trainex-r3-resolution-doc.md
rule19=docs/work/reviews/milestone_v2.3/54-recalibration-decision-grounding/2026-09-02-trainex-r3-rule19-claim-verification.md
security="$phase_dir/54-SECURITY.md"
validation="$phase_dir/54-VALIDATION.md"
uat="$phase_dir/54-UAT.md"
verification="$phase_dir/54-VERIFICATION.md"

fail() {
  printf 'PHASE54-CLOSE-FAIL %s\n' "$1" >&2
  exit 1
}

for required in \
  "$ruling" "$gaps" "$gap_index" "$candidate" "$rule19" \
  "$security" "$validation" "$uat" "$verification"; do
  test -f "$required" || fail "missing=$required"
done

status="$(awk -F': ' '/^status:/{print $2; exit}' "$ruling")"
test "$status" = CHECKPOINT-2-DISCHARGED || fail "ruling_status=$status"

dispositions="$(sed -n '/^## Checkpoint ② —/,/^This section is filled/p' "$ruling" | grep -c '| \*\*RATIFIED')"
test "$dispositions" -eq 5 || fail "dispositions=$dispositions"

reratifications="$(sed -n '/^## SCOPE-38 re-ratification lines/,/^## Anchor-drift warning/p' "$ruling" | grep -c '^\*\*Block [1-4] ')"
provenance_fields="$(sed -n '/^## SCOPE-38 re-ratification lines/,/^## Anchor-drift warning/p' "$ruling" | grep -c '^- \*\*New decision provenance:\*\*')"
criterion_fields="$(sed -n '/^## SCOPE-38 re-ratification lines/,/^## Anchor-drift warning/p' "$ruling" | grep -c '^- \*\*Re-issued acceptance criterion:\*\*')"
pending_reratifications="$(sed -n '/^## SCOPE-38 re-ratification lines/,/^## Anchor-drift warning/p' "$ruling" | grep -c 'PENDING' || true)"
test "$reratifications" -eq 4 || fail "reratifications=$reratifications"
test "$provenance_fields" -eq 4 || fail "provenance_fields=$provenance_fields"
test "$criterion_fields" -eq 4 || fail "criterion_fields=$criterion_fields"
test "$pending_reratifications" -eq 0 || fail "pending_reratifications=$pending_reratifications"

gap_ids="$(grep -oE '^## GAP-54-[0-9]+' "$gaps" | awk '{print $2}' | LC_ALL=C sort -u | wc -l | tr -d ' ')"
resolved_gaps="$(grep -c '^- \*\*Status:\*\* RESOLVED-WITH-INSTRUCTION$' "$gaps")"
deferred_gaps="$(grep -c '^- \*\*Status:\*\* DEFERRED$' "$gaps")"
open_gaps="$(grep -c '^- \*\*Status:\*\* OPEN$' "$gaps" || true)"
resolution_notes="$(grep -c '^- \*\*Resolution note:\*\*' "$gaps")"
index_resolved="$(grep -c '^| GAP-54-.*| RESOLVED-WITH-INSTRUCTION (2026-09-04) |' "$gap_index")"
index_deferred="$(grep -c '^| GAP-54-06 .*| DEFERRED (2026-09-04;' "$gap_index")"
index_open="$(grep -c '^| GAP-54-.*| OPEN' "$gap_index" || true)"
test "$gap_ids" -eq 11 || fail "gap_ids=$gap_ids"
test "$resolved_gaps" -eq 10 || fail "resolved_gaps=$resolved_gaps"
test "$deferred_gaps" -eq 1 || fail "deferred_gaps=$deferred_gaps"
test "$open_gaps" -eq 0 || fail "open_gaps=$open_gaps"
test "$resolution_notes" -eq 11 || fail "resolution_notes=$resolution_notes"
test "$index_resolved" -eq 10 || fail "index_resolved=$index_resolved"
test "$index_deferred" -eq 1 || fail "index_deferred=$index_deferred"
test "$index_open" -eq 0 || fail "index_open=$index_open"

grep -q 'GAP-39-12' "$ruling" || fail 'gap39_contract_missing'
grep -q 'total per training batch' "$ruling" || fail 'n_col_unit_missing'
grep -q 'training-batch.*diagnostic' "$ruling" || fail 'training_front_boundary_missing'
grep -q 'checkpoint ③' "$ruling" || fail 'checkpoint3_routing_missing'
grep -q 'Optimizer-phase boundary — explicitly deferred' "$ruling" || fail 'optimizer_scope_deferral_missing'
grep -q '^- \*\*Status:\*\* DEFERRED$' "$gaps" || fail 'gap54_06_deferral_missing'

candidate_picks="$(awk -F'|' '/CANDIDATE-SHEET/{f=1} /END-CANDIDATE-SHEET/{f=0} f&&/^\| /&&!/^\|[- :|]*$/{c=$(NF-1); gsub(/^[ \t]+|[ \t]+$/,"",c); if(c!="" && c !~ /^Owner/){n++}} END{print n+0}' "$candidate")"
attribution_tags="$(grep -oE '\{src:[a-z0-9|+-]+\}' "$candidate" | wc -l | tr -d ' ')"
test "$candidate_picks" -eq 0 || fail "candidate_picks=$candidate_picks"
test "$attribution_tags" -eq 230 || fail "attribution_tags=$attribution_tags"

validation_status="$(awk -F': ' '/^status:/{print $2; exit}' "$validation")"
nyquist="$(awk -F': ' '/^nyquist_compliant:/{print $2; exit}' "$validation")"
wave_zero="$(awk -F': ' '/^wave_0_complete:/{print $2; exit}' "$validation")"
validation_rows="$(grep -c '^| 54-.*| ✅ green |$' "$validation")"
validation_pending="$(grep -c '^| 54-.*| ⬜ pending |$' "$validation" || true)"
test "$validation_status" = validated || fail "validation_status=$validation_status"
test "$nyquist" = true || fail "nyquist=$nyquist"
test "$wave_zero" = true || fail "wave_zero=$wave_zero"
test "$validation_rows" -eq 40 || fail "validation_rows=$validation_rows"
test "$validation_pending" -eq 0 || fail "validation_pending=$validation_pending"

security_status="$(awk -F': ' '/^status:/{print $2; exit}' "$security")"
threats_open="$(awk -F': ' '/^threats_open:/{print $2; exit}' "$security")"
threat_rows="$(grep -c '^| T-54-' "$security")"
threat_ids="$(grep '^| T-54-' "$security" | cut -d'|' -f2 | tr -d ' ' | LC_ALL=C sort -u | wc -l | tr -d ' ')"
test "$security_status" = verified || fail "security_status=$security_status"
test "$threats_open" -eq 0 || fail "threats_open=$threats_open"
test "$threat_rows" -eq 55 || fail "threat_rows=$threat_rows"
test "$threat_ids" -eq 55 || fail "unique_threat_ids=$threat_ids"

uat_status="$(awk -F': ' '/^status:/{print $2; exit}' "$uat")"
uat_passes="$(grep -c '^result: pass$' "$uat")"
verification_status="$(awk -F': ' '/^status:/{print $2; exit}' "$verification")"
test "$uat_status" = complete || fail "uat_status=$uat_status"
test "$uat_passes" -eq 10 || fail "uat_passes=$uat_passes"
test "$verification_status" = passed || fail "verification_status=$verification_status"

plans="$(find "$phase_dir" -maxdepth 1 -name '54-*-PLAN.md' | wc -l | tr -d ' ')"
summaries="$(find "$phase_dir" -maxdepth 1 -name '54-*-SUMMARY.md' | wc -l | tr -d ' ')"
test "$plans" -eq 13 || fail "plans=$plans"
test "$summaries" -eq 13 || fail "summaries=$summaries"

grep -q '^current_phase: 55$' .planning/STATE.md || fail 'state_current_phase'
grep -q '^current_phase_name: Architecture Characterization Probe$' .planning/STATE.md || fail 'state_phase_name'
grep -q '^  completed_phases: 2$' .planning/STATE.md || fail 'state_completed_phases'
grep -q '^  percent: 33$' .planning/STATE.md || fail 'state_percent'
grep -q '^- \[x\] \*\*Phase 54:' .planning/ROADMAP.md || fail 'roadmap_phase54'
grep -q '^- \[ \] \*\*Phase 55:' .planning/ROADMAP.md || fail 'roadmap_phase55'
grep -q '^- \[ \] \*\*Phase 56:' .planning/ROADMAP.md || fail 'roadmap_phase56'
test ! -d .planning/phases/55-architecture-characterization-probe || fail 'phase55_opened'
test ! -d .planning/phases/56-contract-amendment-train-free-gate || fail 'phase56_opened'
grep -q '^- \[x\] \*\*ERW-01\*\*' .planning/REQUIREMENTS.md || fail 'erw01_incomplete'
grep -q '^- \[x\] \*\*ERW-02\*\*' .planning/REQUIREMENTS.md || fail 'erw02_incomplete'
grep -q '^| ERW-01 | Phase 54 | Complete |$' .planning/REQUIREMENTS.md || fail 'erw01_traceability'
grep -q '^| ERW-02 | Phase 54 | Complete |$' .planning/REQUIREMENTS.md || fail 'erw02_traceability'
grep -q 'Phase 54 complete (2026-09-04)' .planning/PROJECT.md || fail 'project_phase54'

protected_paths=(
  "$candidate"
  pinn_instruction/markdown_conversion/framework-specs/trainex-r3/research_results
  pinn_instruction/markdown_conversion/framework-specs/trainex-r3/research_package
  pinn_instruction/markdown_conversion/framework-specs/trainex-r3/specs
  "$rule19"
  pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md
  pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md
  pinn_instruction/markdown_conversion/framework-specs/sampling_method.md
  pinn
  simulation_data
  tests
)
test -z "$(git diff HEAD --stat -- "${protected_paths[@]}")" || fail 'protected_tracked_diff'
test -z "$(git status --porcelain -- "${protected_paths[@]}")" || fail 'protected_worktree_change'

gsd54_path="$(command -v gsd-tools 2>/dev/null || true)"
if test -n "$gsd54_path" && test -x "$gsd54_path"; then
  gsd54() { "$gsd54_path" "$@"; }
elif test -f "$HOME/.codex4/gsd-core/bin/gsd-tools.cjs"; then
  gsd54() { node "$HOME/.codex4/gsd-core/bin/gsd-tools.cjs" "$@"; }
else
  fail 'gsd_tools_missing'
fi

gsd54 query verification.status "$phase_dir" | grep -q '"status": "passed"' || fail 'canonical_verification'
gsd54 phase uat-passed 54 --require-verification | grep -q '"passed": true' || fail 'completion_predicate'

git diff --check || fail 'diff_check'

python3 - <<'PY'
import math

assert 16 * 256 == 4096
assert 240 * 16 + 16 * 16 == 4096
assert math.isclose(math.exp(-15), 3.059023205018258e-7, rel_tol=1e-15)
print(
    "MATH-PASS rows=4096 replay_only=4096 "
    f"exp(-15)={math.exp(-15):.12g} margin={87.33654 / 15:.6f}"
)
PY

printf 'PHASE54-CLOSE-PASS dispositions=%s reratifications=%s gaps=%s+%s-deferred candidate_picks=%s tags=%s validation_rows=%s threats=%s/%s uat=%s verification=%s phase_plans=%s/%s next=55 phase56=closed\n' \
  "$dispositions" "$reratifications" "$resolved_gaps" "$deferred_gaps" \
  "$candidate_picks" "$attribution_tags" "$validation_rows" "$threat_rows" \
  "$threats_open" "$uat_passes" "$verification_status" "$summaries" "$plans"
