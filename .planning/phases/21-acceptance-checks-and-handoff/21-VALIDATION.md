---
phase: 21
slug: acceptance-checks-and-handoff
status: passed
nyquist_compliant: true
created: 2026-06-08
---

# Phase 21 - Validation Strategy

## Test Infrastructure

| Property | Value |
|---|---|
| Framework | disposable Python probes plus shell/rg doc checks |
| Python | `.venv/bin/python` |
| Evidence directory | `.planning/phases/21-acceptance-checks-and-handoff/evidence/` |
| Quick run command | `for p in probe_scaling.py probe_com.py probe_ad.py probe_force_energy.py probe_loss_stability.py; do .venv/bin/python .planning/phases/21-acceptance-checks-and-handoff/probes/$p; done` |
| Estimated runtime | under 10 seconds |

## Strict Full Suite Command

```bash
bash <<'BASH'
set -u
E=0
P21=.planning/phases/21-acceptance-checks-and-handoff
SPEC=pinn_instruction/markdown_conversion/framework-specs
REV=pinn_instruction/markdown_conversion/framework-revisions

require_file() {
  if [ ! -f "$1" ]; then
    echo "FAIL missing file: $1"
    E=1
  else
    echo "PASS file: $1"
  fi
}

require_match() {
  label="$1"
  pattern="$2"
  file="$3"
  if rg -q "$pattern" "$file"; then
    echo "PASS $label"
  else
    echo "FAIL $label"
    E=1
  fi
}

echo "=== Required Phase 21 files ==="
for f in \
  "$P21/21-CONTEXT.md" \
  "$P21/21-RESEARCH.md" \
  "$P21/21-DISCUSSION-LOG.md" \
  "$P21/21-GAPS.md" \
  "$P21/21-VALIDATION.md" \
  "$P21/21-VERIFICATION.md" \
  "$P21/21-UAT.md" \
  "$P21/21-CODE-DIVERGENCE.md" \
  "$P21/21-01-SUMMARY.md" \
  "$P21/21-02-SUMMARY.md" \
  "$P21/21-PROBE-RESULTS.md"; do
  require_file "$f"
done

echo "=== Section 10 commands and criteria ==="
require_match "scaling command" "\\.venv/bin/python .*probe_scaling.py" "$SPEC/pinn_architecture.md"
require_match "COM command" "\\.venv/bin/python .*probe_com.py" "$SPEC/pinn_architecture.md"
require_match "AD command" "\\.venv/bin/python .*probe_ad.py" "$SPEC/pinn_architecture.md"
require_match "force-energy command" "\\.venv/bin/python .*probe_force_energy.py" "$SPEC/pinn_architecture.md"
require_match "loss command" "\\.venv/bin/python .*probe_loss_stability.py" "$SPEC/pinn_architecture.md"
require_match "force-energy gradient wording" "negative position gradient" "$SPEC/pinn_architecture.md"

echo "=== Probe source fidelity ==="
if rg -q "T = 1\\.0|expected_D = 1\\.0|DummyPINN|nn\\.Linear\\(14, 9\\)" "$P21/probes"; then
  echo "FAIL stale weak probe implementation remains"
  E=1
else
  echo "PASS no stale weak probe implementation"
fi
require_match "SineLayer in loss probe" "class SineLayer" "$P21/probes/probe_loss_stability.py"
require_match "LayerNorm in loss probe" "LayerNorm\\(.*elementwise_affine=False" "$P21/probes/probe_loss_stability.py"

echo "=== Run probes ==="
for p in probe_scaling.py probe_com.py probe_ad.py probe_force_energy.py probe_loss_stability.py; do
  echo "--- $p"
  if .venv/bin/python "$P21/probes/$p"; then
    echo "PASS $p"
  else
    echo "FAIL $p"
    E=1
  fi
done

echo "=== Evidence files ==="
for f in "$P21"/evidence/*.stdout.txt; do
  require_file "$f"
  require_match "exit code recorded for $f" "exit_code=0" "$f"
done
require_match "results hashes recorded" "SHA-256" "$P21/21-PROBE-RESULTS.md"

echo "=== SI ledger reconciliation ==="
require_match "SI-CTL-001 retired" "Resolved by v1\\.4 finding B-03" "$SPEC/ctl_instruction.md"
require_match "SI-SSR-001 retired" "Resolved by v1\\.4 finding M5" "$REV/stage-strat-revision/stage_strat_revision.md"
if rg -q "SI-PINN-001" "$SPEC/pinn_architecture.md"; then
  echo "FAIL SI-PINN-001 unexpectedly present in framework spec"
  E=1
else
  echo "PASS SI-PINN-001 absent from framework-spec SI section"
fi
require_match "SI-PINN-002 preserved" "SI-PINN-002" "$SPEC/pinn_architecture.md"
require_match "SI-PINN-003 preserved" "SI-PINN-003" "$SPEC/pinn_architecture.md"
require_match "SI-DQA-002 preserved" "SI-DQA-002" pinn_instruction/markdown_conversion/framework-revisions/data_quality_assessment.md
require_match "SI-DQA-003 preserved" "SI-DQA-003" pinn_instruction/markdown_conversion/framework-revisions/data_quality_assessment.md

echo "=== Phase 21 verification status ==="
require_match "verification passed" "status: passed" "$P21/21-VERIFICATION.md"
require_match "no open gaps" "open_gaps: 0" "$P21/21-GAPS.md"

if [ "$E" -eq 0 ]; then
  echo "=== PHASE 21 STRICT FULL SUITE: ALL PASS ==="
else
  echo "=== PHASE 21 STRICT FULL SUITE: FAILURES DETECTED ==="
fi
exit "$E"
BASH
```

## Per-Task Verification Map

| Task ID | Plan | Requirement | Automated Command | Status |
|---|---|---|---|---|
| 21-01-01 | 01 | VER-01 | `rg -n "# 10\\. Numerical Acceptance Checks|10\\.1|10\\.5" pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` | green |
| 21-01-02 | 01 | VER-04 | `.venv/bin/python` each probe under `probes/` | green |
| 21-02-01 | 02 | VER-06 | `rg -n "SI-CTL-001|SI-SSR-001|SI-PINN-00[23]|SI-DQA-00[23]" pinn_instruction/markdown_conversion` | green |
| 21-02-02 | 02 | VER-03 | `rg -n "M6|M7|Fixed|Deferred" .planning/phases/21-acceptance-checks-and-handoff/21-HANDOFF.md` | green |

## Validation Sign-Off

- [x] All five probes have captured stdout evidence.
- [x] The probe interpreter is recorded.
- [x] The weak-probe regression checks are included in the strict suite.
- [x] The SI reconciliation check preserves unrelated SI entries.
- [x] No live `pinn/` implementation file is used as v1.4 grounding evidence.
