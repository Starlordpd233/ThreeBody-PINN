---
phase: 34
slug: training-loop-batch-construction-contracts
status: active
nyquist_compliant: true
wave_0_complete: true
created: 2026-06-24
---

# Phase 34 - Validation Strategy

> Per-phase validation contract for training-loop & batch-construction specwork
> planning and execution. Source: `34-RESEARCH.md` `## Validation Architecture`.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | shell + Python source-token / negative-token / no-duplication checks + git protected-path guards + disposable formula-sanity probes (D-34-17). NOT runtime training tests (SCOPE-14). |
| **Config file** | none (`.planning/config.json`: `workflow.nyquist_validation: true`, `commit_docs: true`) |
| **Quick run command** | `rg -n "LOOP-0[1-8]\|SI-PINN-003" .planning/phases/34-training-loop-batch-construction-contracts/34-*-PLAN.md` |
| **Full suite command** | plan coverage check, framework-spec token checks, the LOOP-04 (a)–(e) cross-file consistency suite, the locked-convention regression guard, forbidden-path git-diff guard, and STOP-gap completeness checks if new gaps are opened |
| **Estimated runtime** | ~15 seconds |

---

## Sampling Rate

- **After every task commit:** task-local source-token + negative-token checks + the forbidden-path `git diff --name-only` status guard.
- **After every plan wave / every batch that edits a LOOP-04 half:** the full structural check set below, INCLUDING the LOOP-04 (c)/(d)/(e) re-verify-after-every-batch suite + the locked-convention regression guard.
- **Before `/gsd-verify-work`:** full structural/source suite must be green (all 9 requirement checks), every Phase-32 ledger row for B-07/B-08/M16/ALM closed `VERIFIED`/`DEFERRED`, or every failure recorded as a blocker/STOP gap.
- **Max feedback latency:** ~15 seconds.

---

## Structural Check Set

### Planning Artifact Coverage

```bash
test -f .planning/phases/34-training-loop-batch-construction-contracts/34-SPEC.md
test -f .planning/phases/34-training-loop-batch-construction-contracts/34-CONTEXT.md
test -f .planning/phases/34-training-loop-batch-construction-contracts/34-RESEARCH.md
python3 - <<'PY'
from pathlib import Path
root = Path(".planning/phases/34-training-loop-batch-construction-contracts")
plans = sorted(root.glob("34-*-PLAN.md"))
assert plans, "no Phase 34 plans found"
txt = "\n".join(p.read_text() for p in plans)
required = ["LOOP-01","LOOP-02","LOOP-03","LOOP-04","LOOP-05","LOOP-06","LOOP-07","LOOP-08","SI-PINN-003"]
missing = [req for req in required if req not in txt]
assert not missing, missing
PY
```

### LOOP-04 Cross-File Consistency Suite (a)–(e) — re-run after every batch that edits either half

```bash
python3 - <<'PY'
import re
from pathlib import Path
ctl = Path("pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md").read_text()
pinn = Path("pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md").read_text()
# (b) 8.5 absent from BOTH files; the per-stage C-schedule 7-10 / 5 / 3 survives in ctl.
assert "8.5" not in ctl, "8.5 leaked into ctl_instruction.md"
assert "8.5" not in pinn, "8.5 leaked into pinn_architecture.md"
# Discriminating C-schedule check (NOT bare "5"/"3", which are trivially present in any large
# Markdown file): assert the 7-10 schedule value has exactly ONE canonical home after the
# Consolidated-table collapse (mirrors the stronger per-batch gate in 34-03 / 34-05), and that
# the 5 and 3 per-stage values survive as right-aligned C-schedule table cells.
n_seven_ten = len(re.findall(r"7\s*-\s*10", ctl)) + len(re.findall(r"7--10", ctl))
assert n_seven_ten == 1, f"7-10 C-schedule must have exactly one canonical home in ctl; found {n_seven_ten}"
assert re.search(r"\|\s*5\s*\|", ctl), "per-stage C-schedule value 5 missing as a table cell in ctl"
assert re.search(r"\|\s*3\s*\|", ctl), "per-stage C-schedule value 3 missing as a table cell in ctl"
# (a) mechanism formula appears exactly once, canonical in pinn §4.4
mech = "C_stage"
# (c) bidirectional cross-refs resolve (heading + AC-LOOP-04)
assert "AC-LOOP-04" in ctl and "AC-LOOP-04" in pinn, "AC-LOOP-04 anchor missing in one half"
# (d)/(e) no-duplication + status-tag parity are judgment+grep checks the executor records per-batch.
print("LOOP-04 (b)/(c) green; (a)/(d)/(e) recorded per-batch by executor")
PY
```

### Framework-Spec Contract Tokens (per-requirement)

```bash
python3 - <<'PY'
from pathlib import Path
ctl = Path("pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md").read_text()
pinn = Path("pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md").read_text()
checks = {
    "LOOP-01 replay/lookahead (ctl)": (ctl, ["B_replay", "B_lookahead", "has_stage", "provisional"]),
    "LOOP-02 two point sets (ctl)":   (ctl, ["collocation", "data-fidelity", "provisional"]),
    "LOOP-03 mixed sampling (ctl)":   (ctl, ["50/50", "deferred"]),
    "LOOP-04 mechanism (pinn §4.4)":  (pinn, ["C_stage", "median", "AC-LOOP-04"]),
    "LOOP-05 ALM optional (pinn)":    (pinn, ["ALM", "optional", "deferred"]),
    "LOOP-06 M16 deferred (ctl)":     (ctl, ["realized-as-deferred", "deferred"]),
    "LOOP-07 IPR/PSC (ctl)":          (ctl, ["IPR", "PSC", "provisional", "VAL-0"]),
    "LOOP-08 SASD (ctl)":             (ctl, ["SASD", "provisional", "VAL-02"]),
    "SI-PINN-003 reconciled (pinn)":  (pinn, ["RESOLVED", "ctl_instruction"]),
}
missing = {name: [t for t in toks if t not in src] for name, (src, toks) in checks.items()}
missing = {name: toks for name, toks in missing.items() if toks}
assert not missing, missing
PY
```

### Negative / Owner-Pending Checks

```bash
python3 - <<'PY'
from pathlib import Path
ctl = Path("pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md").read_text()
pinn = Path("pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md").read_text()
# LOOP-04: 8.5 never canonized (also covered above); no early-stage C tagged "locked"
assert "8.5" not in ctl and "8.5" not in pinn
# LOOP-06: no probe-able n_col formula transcribed as a locked contract
# (the candidate direction may appear ONLY tagged deferred — executor confirms by context)
# LOOP-05: default training step must NOT include a dense-residual ALM update
for forbidden in ["dense-residual ALM in the default loss", "ALM is enabled by default"]:
    assert forbidden not in pinn, forbidden
# SI-PINN-003: the resolved author-comment inconsistency string is gone from pinn §3.1
assert "is not consistent with the CTL instruction plan" not in pinn, "SI-PINN-003 author comment still present"
PY
```

### Locked-Convention Regression Guard (SCOPE-12)

```bash
python3 - <<'PY'
import subprocess
from pathlib import Path
ctl = Path("pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md").read_text()
pinn = Path("pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md").read_text()
head_ctl = subprocess.check_output(
    ["git", "show", "HEAD:pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md"]
).decode()
# SCOPE-12 / EVID-10: ctl legitimately documents the REJECTED D = 6.694 provenance
# (4 occurrences at HEAD). A real regression is introducing 6.694 as an ACTIVE scale, so
# guard against a NEW occurrence vs the committed baseline rather than absolute absence.
assert ctl.count("6.694") <= head_ctl.count("6.694"), (
    "SCOPE-12/EVID-10: no NEW active-convention 6.694 may be added to ctl "
    "(rejected-provenance occurrences are preserved)"
)
# pinn has zero 6.694 occurrences; any introduction there is a true regression.
assert "6.694" not in pinn, "D=6.694 reintroduced in pinn_architecture.md"
# D ~= 4.6416 must remain present as the canonical raw-mass scale in ctl
assert "4.6416" in ctl, "raw-mass D ~= 4.6416 regressed out of ctl"
PY
```

### Forbidden-Path Status Guard (SCOPE-08/09/13 + no-live-code)

```bash
git diff --name-only -- \
  pinn_instruction/markdown_conversion/framework-specs/sampling_method.md \
  pinn_instruction/markdown_conversion/framework-revisions/data_quality_assessment.md \
  pinn_instruction/markdown_conversion/framework-revisions/review-of-framework/review_of_framework.md \
  pinn_instruction/markdown_conversion/framework-revisions/stage-strat-revision/stage_strat_revision.md \
  pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md \
  pinn/
```

Expected output: empty. Only `ctl_instruction.md` and `pinn_architecture.md` may change among framework files (SCOPE-13).

### STOP Gap Completeness

Run only if Phase 34 opens a new `OPEN` gap during execution (the batch edge-case gap, D-34-16a, is anticipated).

```bash
python3 - <<'PY'
from pathlib import Path
phase_gap = Path(".planning/phases/34-training-loop-batch-construction-contracts/34-GAPS.md")
milestone_gap = Path(".planning/milestones/v1.6-GAPS.md")
required = [
    "Decision point","Where in artifact","Task context","Classification",
    "Source silence","Mathematical / engineering grounding","Agent was tempted to",
    "What the user needs to decide","Confidence of impact","Status",
]
if phase_gap.exists():
    txt = phase_gap.read_text()
    if "Status:** OPEN" in txt or "Status: OPEN" in txt:
        missing = [t for t in required if t not in txt]
        assert not missing, missing
        assert "GAP-34" in milestone_gap.read_text()
PY
```

---

## Per-Requirement Verification Map

| Req | Plan | Wave | Test Type | Probe (D-34-17)? | Automated Command Source |
|-----|------|------|-----------|------------------|--------------------------|
| LOOP-01 | planner-defined | planner-defined | source-token + **probe** | YES — `min(n_pts_cap, n_snapshots)` on sample | `Framework-Spec Contract Tokens` |
| LOOP-02 | planner-defined | planner-defined | source-token (structural) | no | `Framework-Spec Contract Tokens` |
| LOOP-03 | planner-defined | planner-defined | source-token + negative + **probe** | YES — data-fidelity 50/50 split sums to n | `Framework-Spec Contract Tokens` + `Negative Checks` |
| LOOP-04 | planner-defined | planner-defined | token + negative + duplication + **probe** | YES — `clip_value = C_stage·median(hist)` on sample | `LOOP-04 (a)–(e) Suite` (re-run per batch) |
| LOOP-05 | planner-defined | planner-defined | source-token + negative (NO probe) | no | `Framework-Spec Contract Tokens` + `Negative Checks` |
| LOOP-06 | planner-defined | planner-defined | source-token + negative (NO probe) | no | `Framework-Spec Contract Tokens` + `Negative Checks` |
| LOOP-07 | planner-defined | planner-defined | source-token (structural; carried not recalibrated) | no | `Framework-Spec Contract Tokens` |
| LOOP-08 | planner-defined | planner-defined | source-token + negative | no | `Framework-Spec Contract Tokens` |
| SI-PINN-003 | planner-defined | planner-defined | source-token + negative | no | `Framework-Spec Contract Tokens` + `Negative Checks` |

*Status updated by the executor as checks run. Probe set is EXHAUSTIVE per D-34-17: LOOP-01/03/04 only; LOOP-05/06/08 deferred = NO probe; LOOP-02/07 structural grep; there is intentionally NO `n_col ∝ dt_base/dt_out` probe (LOOP-06 is deferred).*

---

## Wave 0 Requirements

Existing infrastructure covers all phase requirements:

- `rg` is available for source-token scans.
- `python3` is available for deterministic Markdown/source assertions (token / negative-token / no-duplication / formula-sanity probes).
- `git` is available for forbidden-path and unrelated-dirty-file guards.
- No package install, test framework install, EDA run, Stage-0 pilot, or training run is required (SCOPE-14/15).

Two artifacts must be created before any spec edit (not test infrastructure, but execution preconditions):
- `.planning/phases/34-training-loop-batch-construction-contracts/evidence/` — packet dir mirroring the Phase-32 schema (B-07, B-08, M16, ALM packets; LOOP-04 reuses the existing M14 packet).
- `.planning/phases/34-training-loop-batch-construction-contracts/34-GAPS.md` — created on the first STOP gap.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| LOOP-04 (d) no duplicated normative text across the two halves; (e) status-tag parity | LOOP-04 | Requires judgment that the merged rule is recoverable from the two cross-referenced halves with zero duplication — a grep proves token presence, not semantic single-sourcing. | After every LOOP-04 batch, a reviewer reads pinn §4.4 + the ctl C-schedule and confirms each value/formula has exactly one canonical home and the two status tags agree. |
| Faithful verdict+status transcription (no invented locks) | all | Anti-fabrication is a judgment check — each transcribed contract must carry its adjudicated status tag + citation. | Reviewer confirms every LOOP callout's status tag matches its Phase-32 ledger / resolution-doc verdict. |

New STOP gaps, if opened, require human owner resolution before dependent spec edits proceed.

---

## Validation Sign-Off

- [x] All planned tasks must carry `<verify>` commands or cite this validation strategy as their source.
- [x] Sampling continuity: task-local checks after every task commit; full structural set + LOOP-04 (c)/(d)/(e) after every batch that edits a LOOP-04 half.
- [x] Wave 0 needs no new test files or installs.
- [x] No watch-mode flags.
- [x] Feedback latency < 15 seconds.
- [x] `nyquist_compliant: true` set in frontmatter.

**Approval:** approved 2026-06-24 for planning input; execution must update per-requirement statuses when checks run.
