---
phase: 33
slug: curriculum-stage-contracts
status: active
nyquist_compliant: true
wave_0_complete: true
created: 2026-06-22
---

# Phase 33 - Validation Strategy

> Per-phase validation contract for curriculum-stage specwork planning and execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | shell + Python source-token checks |
| **Config file** | none |
| **Quick run command** | `rg -n "CURR-01|CURR-02|CURR-03|CURR-04|CURR-05" .planning/phases/33-curriculum-stage-contracts/33-*-PLAN.md` |
| **Full suite command** | plan coverage check, framework-spec token checks, forbidden-path git diff checks, and STOP-gap completeness checks if new gaps are opened |
| **Estimated runtime** | ~10 seconds |

---

## Sampling Rate

- **After every task commit:** Run task-local source-token checks and the forbidden-path status guard.
- **After every plan wave:** Run the full structural check set below.
- **Before `$gsd-verify-work`:** Full structural/source suite must be green, or every failure must be recorded as a blocker/STOP gap.
- **Max feedback latency:** 10 seconds.

---

## Structural Check Set

### Planning Artifact Coverage

```bash
test -f .planning/phases/33-curriculum-stage-contracts/33-SPEC.md
test -f .planning/phases/33-curriculum-stage-contracts/33-CONTEXT.md
test -f .planning/phases/33-curriculum-stage-contracts/33-RESEARCH.md
python3 - <<'PY'
from pathlib import Path
root = Path(".planning/phases/33-curriculum-stage-contracts")
plans = sorted(root.glob("33-*-PLAN.md"))
assert plans, "no Phase 33 plans found"
txt = "\n".join(p.read_text() for p in plans)
required = ["CURR-01", "CURR-02", "CURR-03", "CURR-04", "CURR-05"]
missing = [req for req in required if req not in txt]
assert not missing, missing
PY
```

### Framework-Spec Contract Tokens

```bash
python3 - <<'PY'
from pathlib import Path
txt = Path("pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md").read_text()
checks = {
    "CURR-01 adaptive labels": ["record_key", "PCA", "clustering", "not locked"],
    "CURR-02 characteristic scale": ["characteristic", "L_max", "D ~= 4.6416", "tau_L", "IC13"],
    "CURR-03 transition state machine": ["ADVANCE", "RECOVER", "HALT", "REVIEW", "NaN", "Inf"],
    "CURR-04 raw L_norm guard": ["Stage 0", "Stage 6", "raw", "L_norm", "No global"],
    "CURR-05 s_min frame": ["unsoftened geometric", "s_min", "Phase 35", "matched-Plummer"],
}
missing = {name: [token for token in tokens if token not in txt] for name, tokens in checks.items()}
missing = {name: tokens for name, tokens in missing.items() if tokens}
assert not missing, missing
PY
```

### Owner-Pending Negative Checks

```bash
python3 - <<'PY'
from pathlib import Path
txt = Path("pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md").read_text()
for forbidden in [
    "population safeguard is locked at >10%",
    "global L_norm clamp",
    "D = 6.694 is the active scale",
    "PCA+Rosenstein shortcut is normative",
]:
    assert forbidden not in txt, forbidden
assert "np.clip(L_norm, 0, 1)" not in txt or "not locked" in txt
PY
```

### Forbidden-Path Status Guard

```bash
git diff --name-only -- \
  pinn_instruction/markdown_conversion/framework-specs/sampling_method.md \
  pinn_instruction/markdown_conversion/framework-revisions/data_quality_assessment.md \
  pinn_instruction/markdown_conversion/framework-revisions/review-of-framework/review_of_framework.md \
  pinn_instruction/markdown_conversion/framework-revisions/stage-strat-revision/stage_strat_revision.md \
  pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md \
  pinn/
```

Expected output: empty.

### STOP Gap Completeness

Run only if Phase 33 opens a new `OPEN` gap during execution.

```bash
python3 - <<'PY'
from pathlib import Path
phase_gap = Path(".planning/phases/33-curriculum-stage-contracts/33-GAPS.md")
milestone_gap = Path(".planning/milestones/v1.6-GAPS.md")
required = [
    "Decision point",
    "Where in artifact",
    "Task context",
    "Classification",
    "Source silence",
    "Mathematical / engineering grounding",
    "Agent was tempted to",
    "What the user needs to decide",
    "Confidence of impact",
    "Status",
]
txt = phase_gap.read_text()
if "Status:** **OPEN" in txt or "Status:** OPEN" in txt:
    missing = [token for token in required if token not in txt]
    assert not missing, missing
    assert "GAP-33" in milestone_gap.read_text()
PY
```

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 33-TBD-01 | planner-defined | planner-defined | CURR-01 | T-33-SD | Population floor remains owner-pending; adaptive labels are specified. | source-token / negative-token | See `Framework-Spec Contract Tokens` and `Owner-Pending Negative Checks`. | yes | pending |
| 33-TBD-02 | planner-defined | planner-defined | CURR-02 | T-33-SD | Characteristic `L_max`, `D ~= 4.6416`, and `tau_L` metadata exclusion are preserved. | source-token | See `Framework-Spec Contract Tokens`. | yes | pending |
| 33-TBD-03 | planner-defined | planner-defined | CURR-03 | T-33-SD | Stage transitions use ADVANCE / RECOVER / HALT/REVIEW and provisional thresholds. | source-token | See `Framework-Spec Contract Tokens`. | yes | pending |
| 33-TBD-04 | planner-defined | planner-defined | CURR-04 | T-33-SD | Raw `L_norm`, guard behavior, and no global clamp are preserved. | source-token / negative-token | See `Framework-Spec Contract Tokens` and `Owner-Pending Negative Checks`. | yes | pending |
| 33-TBD-05 | planner-defined | planner-defined | CURR-05 | T-33-SD | Unsoftened geometric `s_min` stage gate is separated from Phase 35 loss-side softening. | source-token | See `Framework-Spec Contract Tokens`. | yes | pending |

---

## Wave 0 Requirements

Existing infrastructure covers all phase requirements:

- `rg` is available for source-token scans.
- `python3` is available for deterministic Markdown/source assertions.
- `git` is available for forbidden-path and unrelated-dirty-file guards.
- No package install, test framework install, EDA run, Stage-0 pilot, or training run is required.

---

## Manual-Only Verifications

All Phase 33 behaviors have automated source-token or git-status verification. New STOP gaps, if opened, still require human owner resolution before dependent spec edits proceed.

---

## Validation Sign-Off

- [x] All planned tasks must have `<automated>` verify commands or this validation strategy as a source.
- [x] Sampling continuity: run task-local checks after every task commit and the full structural check set after every wave.
- [x] Wave 0 does not need new test files or installs.
- [x] No watch-mode flags.
- [x] Feedback latency < 10 seconds.
- [x] `nyquist_compliant: true` set in frontmatter.

**Approval:** approved 2026-06-22 for planning input; execution must update task statuses when checks run.
