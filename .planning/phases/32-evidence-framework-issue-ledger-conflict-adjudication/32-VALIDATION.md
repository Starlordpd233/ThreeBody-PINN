---
phase: 32
slug: evidence-framework-issue-ledger-conflict-adjudication
status: active
nyquist_compliant: true
wave_0_complete: true
created: 2026-06-21
---

# Phase 32 - Validation Strategy

> Per-phase validation contract for evidence-framework planning and execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | shell + Python structural checks |
| **Config file** | none |
| **Quick run command** | `python3 - <<'PY' ... PY` structural probes recorded in `32-VERIFICATION.md` |
| **Full suite command** | artifact existence, verdict/lifecycle enum, ledger coverage, forbidden-path status, dirty-doc baseline, and packet source-discipline checks |
| **Estimated runtime** | ~10 seconds |

---

## Sampling Rate

- **After every task commit:** Run the task-local artifact existence and forbidden-path status check.
- **After every plan wave:** Run the full structural check set below.
- **Before `$gsd-verify-work`:** `32-VERIFICATION.md` must record all structural checks as passing, or record explicit deferred blockers.
- **Max feedback latency:** 10 seconds.

---

## Structural Check Set

### Required Artifact Existence

```bash
test -f .planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence/README.md
test -f .planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence/_TEMPLATE.md
test -f .planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md
test -f .planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-VERIFICATION.md
```

### Headline Packet Coverage

```bash
for f in d-04-causal-training-mode d-05-s-min-frame d-06-epsilon-strategy m14-gradient-clipping d-6-694-conflict; do
  test -f ".planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence/$f.md"
done
```

### Verdict and Lifecycle Tokens

```bash
python3 - <<'PY'
from pathlib import Path
root = Path(".planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication")
txt = (root / "evidence/README.md").read_text()
required = [
    "accept-resolution",
    "accept-issue-doc",
    "accept-third-position",
    "reject-both-as-unsupported",
    "defer-with-blocker",
    "PENDING",
    "IN_PROGRESS",
    "FIX_APPLIED",
    "VERIFIED",
    "DEFERRED",
]
missing = [token for token in required if token not in txt]
assert not missing, missing
PY
```

### Ledger Coverage and Terminal-State Guard

```bash
python3 - <<'PY'
from pathlib import Path
p = Path(".planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md")
txt = p.read_text()
required = [
    "D-04",
    "D-05",
    "D-06",
    "B-07",
    "B-08",
    "M6",
    "M7",
    "M14",
    "M15",
    "M16",
    "D5",
    "NS-12",
    "NS-13",
    "NS-18",
    "adaptive stage assignment",
    "D = 6.694",
    "L_max / tau_L",
    "ALM mu_p clamp",
]
missing = [item for item in required if item not in txt]
assert not missing, missing
assert "| FIX_APPLIED |" not in txt or "FIX_APPLIED is not terminal" in txt
PY
```

### Forbidden-Path Status Guard

```bash
test -z "$(git status --short -- \
  pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md \
  pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md \
  pinn_instruction/markdown_conversion/framework-specs/sampling_method.md \
  pinn_instruction/markdown_conversion/framework-revisions/data_quality_assessment.md \
  pinn_instruction/markdown_conversion/framework-revisions/review-of-framework/review_of_framework.md \
  pinn_instruction/markdown_conversion/framework-revisions/stage-strat-revision/stage_strat_revision.md \
  pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md \
  .planning/STATE.md \
  pinn/)"
```

### Dirty Docs Baseline Guard

Record this baseline at Phase 32 start in `32-VERIFICATION.md`, then compare it at closeout. The closeout check fails if either value changes.

```bash
python3 -c "from pathlib import Path; import subprocess, hashlib; doc='docs/work/plans/cross_cutting/gsd-cross-ai-review-resilience/2026-06-20-gsd-review-dispatch-resilience-plan.md'; status=subprocess.check_output(['git','status','--short','--',doc], text=True).strip(); patch_hash=hashlib.sha256(subprocess.check_output(['git','diff','--',doc])).hexdigest(); print(f'Dirty docs baseline status: {status}'); print(f'Dirty docs baseline patch-sha256: {patch_hash}')"
```

### Packet Source Discipline

```bash
if rg -n "pinn/(basic_architecture|data-processing-pipeline-full)\\.py" .planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence; then
  rg -n "NOT grounding|FUT" .planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence
fi
```

---

## Per-Plan Verification Map

| Plan | Wave | Requirement | Test Type | Automated Command | Status |
|------|------|-------------|-----------|-------------------|--------|
| 32-01 | 1 | EVID-11, EVID-12 | artifact schema | required artifact existence; verdict and lifecycle token checks | pending |
| 32-02 | 2 | EVID-13, EVID-14, EVID-15 | packet coverage | headline packet coverage; D-conflict and M14 packet source checks | pending |
| 32-03 | 3 | EVID-11, EVID-12, EVID-15 | STOP-safe packet coverage | D-04/D-05/D-06 packet checks plus gap-register checks if any source-silent semantic decision is opened | pending |
| 32-04 | 4 | EVID-11..15 | full structural verification | all structural checks; forbidden-path status guard; dirty-doc baseline comparison; `32-VERIFICATION.md` updated | pending |

---

## Wave 0 Requirements

Existing infrastructure covers all phase requirements:

- `rg` is available for source and artifact checks.
- `python3` is available for deterministic Markdown/token probes.
- Git hooks are configured through `.githooks`.
- Commits must use `scripts/agent-commit` with explicit owned paths.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| D-04/D-05/D-06 owner decisions | EVID-15 | Semantic owner-routed decisions cannot be selected by structural tests. | Confirm packets either cite explicit user instruction or record `defer-with-blocker` / STOP gaps. |
| First-principles contradiction against v1.5 `D ~= 4.6416` | EVID-15 | A genuine contradiction requires physics reasoning and user instruction before overturning SCOPE-12. | Read `d-6-694-conflict.md`; verify it preserves v1.5 EVID-10 unless a fully surfaced gap is resolved. |

---

## Validation Sign-Off

- [x] All plans have automated structural verification hooks.
- [x] Sampling continuity: every plan has at least one automated check.
- [x] Wave 0 has no missing test framework dependency.
- [x] No watch-mode flags.
- [x] Feedback latency < 10s.
- [x] `nyquist_compliant: true` set in frontmatter.

**Approval:** approved 2026-06-21 for planning.
