---
phase: 16
slug: evidence-framework-and-issue-adjudication
status: passed
nyquist_compliant: true
wave_0_complete: true
created: 2026-05-16
---

# Phase 16 - Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Custom shell/doc checks |
| **Config file** | none |
| **Quick run command** | `rg -n "16-evidence-framework/16-ISSUE-LEDGER|16-evidence-framework" --hidden -g '!reference-code/**' -g '!.git/**'` |
| **Full suite command** | Phase 16 path scan + traceability audit + artifact existence checks + doc-structure checks + no spec/code diff check |
| **Estimated runtime** | ~10 seconds |

---

## Sampling Rate

- **After every task commit:** Run the quick path scan plus a targeted `rg` check for the artifact touched by the task.
- **After every plan wave:** Run all Phase 16 doc-structure checks plus the traceability count/duplicate check.
- **Before `$gsd-verify-work`:** Full Phase 16 validation must pass.
- **Max feedback latency:** 30 seconds.

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 16-01-01 | 01 | 1 | EVID-01 | T-16-01 | Template cannot omit required evidence sections | doc-structure | `rg -n "ctl_pinn_resolution.md|01-architecture-and-physics-foundations.md|Spec evidence|Code evidence" .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/evidence/_TEMPLATE.md` | yes | green |
| 16-01-02 | 01 | 1 | EVID-02 | T-16-02 | Verdict enum is fixed and greppable | doc-structure | `rg -n "accept-resolution|accept-issue-doc|accept-third-position|reject-both-as-unsupported|defer-with-blocker" .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/evidence/_TEMPLATE.md` | yes | green |
| 16-01-03 | 01 | 1 | EVID-03 | False positives are recorded as evidence-backed non-changes | doc-structure | `rg -n "False Positive|intentional non-change|accept-resolution.*no-change|current convention remains valid" .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/evidence/_TEMPLATE.md` | yes | green |
| 16-01-04 | 01 | 1 | EVID-04 | Accepted issues link to before/after notes and AC-IDs | doc-structure | `rg -n "Before / After Spec Note|Named Acceptance Check|AC-" .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/evidence/_TEMPLATE.md` | yes | green |
| 16-01-05 | 01 | 1 | EVID-05 | Contested findings cannot skip adjudication sections | doc-structure | `rg -n "First-Principles Physics Check|Root-Cause Framework Ambiguity|Locked Convention|Which Source Was Correct|YES - EVID-05 required|B-02|B-04|B-09|M5" .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/evidence/_TEMPLATE.md` | yes | green |
| 16-01-06 | 01 | 1 | VER-02 | T-16-06 | Traceability count has no duplicate requirement IDs | shell-audit | `awk 'BEGIN{in_trace=0} /^## Traceability/{in_trace=1; next} in_trace && /^---/{in_trace=0} in_trace && /^\\| [A-Z]+-[0-9][0-9]/{gsub(/^\\| /,""); gsub(/ \\|.*/,""); print}' .planning/REQUIREMENTS.md | sort | uniq -d` | yes | green |
| 16-01-07 | 01 | 1 | VER-05 | T-16-07 | Ledger records status lifecycle, dependents, transition logs, and regression policy | doc-structure | `rg -n "PENDING|IN_PROGRESS|FIX_APPLIED|VERIFIED|DEFERRED|Dependents|regression|phase-exit|fix applied" .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/evidence/README.md` | yes | green |

*Status: pending / green / red / flaky*

---

## Wave 0 Requirements

- [x] `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md` - covers EVID-02, VER-02, and VER-05.
- [x] `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/evidence/README.md` - covers EVID-05 and VER-05 protocol.
- [x] `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/evidence/_TEMPLATE.md` - covers EVID-01 through EVID-05.
- [x] Framework install: none required.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Reviewer readability of ledger and packet template | EVID-01..05, VER-05 | Grep checks prove required fields exist, not that the workflow is understandable to future agents | Read `16-ISSUE-LEDGER.md`, `evidence/README.md`, and `evidence/_TEMPLATE.md`; confirm a future Phase 17-21 agent can identify required citations, verdict enum, EVID-05 sections, and status transition rules without external explanation. |

---

## Validation Sign-Off

- [x] All tasks have automated verification commands or Wave 0 dependencies.
- [x] Sampling continuity: no 3 consecutive tasks without automated verify.
- [x] Wave 0 covers all missing references.
- [x] No watch-mode flags.
- [x] Feedback latency < 30s.
- [x] `nyquist_compliant: true` set in frontmatter.

**Approval:** approved 2026-06-09 after retroactive execution of all seven checks.

## Validation Audit 2026-06-09

| Metric | Count |
|--------|-------|
| Gaps found | 7 pending task rows + incomplete Wave 0 metadata |
| Resolved | 7 task rows + 4 Wave 0 items |
| Escalated | 0 |
