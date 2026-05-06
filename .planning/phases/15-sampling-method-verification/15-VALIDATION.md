---
phase: 15
slug: sampling-method-verification
status: complete
nyquist_compliant: true
wave_0_complete: true
created: 2026-05-05
---

# Phase 15 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution. This is a documentation/verification phase — verification uses CLI tooling (`diff`, `grep`, `python` one-liners) against the LaTeX source and markdown candidates, not a unit-test framework. See `15-RESEARCH.md` § Validation Architecture for full details.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | shell + python one-liners (`diff`, `grep`, `wc`, `python -c "..."`) |
| **Config file** | none — verification commands embedded in plan acceptance criteria |
| **Quick run command** | `bash .planning/phases/15-sampling-method-verification/scoring_script.sh` (created Wave 1) |
| **Full suite command** | `bash .planning/phases/15-sampling-method-verification/verify_all.sh` (created Wave 3) |
| **Estimated runtime** | < 10 seconds (file-size verification only) |

---

## Sampling Rate

- **After every task commit:** Run the matching grep / diff acceptance check from the task's `<automated>` block
- **After every plan wave:** Re-run `bash scoring_script.sh` (Wave 1) or section-by-section diff harness (Wave 2)
- **Before `/gsd-verify-work`:** Full zero-diff `diff <corrected.md> <reference-extract.txt>` must return exit 0 (or document acceptable variances)
- **Max feedback latency:** < 30 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 15-01-01 | 01 | 1 | CAND-01 | — | N/A | shell | `test -f .planning/phases/15-sampling-method-verification/diff-score-report.md` | ❌ W0 | ⬜ pending |
| 15-02-01..N | 02 | 2 | AUDIT-01..03, FIDEL-01..06 | — | N/A | shell | per-section `diff` and `grep` checks (see PLAN.md) | ❌ W0 | ⬜ pending |
| 15-03-01..N | 03 | 3 | CLEAN-01..03, CROSS-01..02 | — | N/A | shell | `test -d _archive/` and `git log --oneline` checks | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

*Detailed task-level rows are populated by the planner in each PLAN.md `<automated>` block; this VALIDATION.md tracks coverage at plan granularity.*

---

## Wave 0 Requirements

- [ ] `scoring_script.sh` — diff-score harness for CAND-01 (created in Wave 1, plan 15-01)
- [ ] `verify_all.sh` — final zero-diff check (created in Wave 3, plan 15-03)

*No external framework install required — the project already uses shell + python for verification per Phases 10–13.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Math semantic equivalence (display vs inline `align*` blocks) | FIDEL-04 | LaTeX-to-markdown math rendering varies; symbolic equivalence cannot be checked by string diff | Compare each `align*` block in source against the markdown's `$$...$$` block; confirm operator-by-operator equivalence |
| `\authcomment{...}` preservation policy | FIDEL-06 | Project-level convention; the executor must confirm the chosen rendering matches Phase 12's precedent | Read Phase 12's RESEARCH.md decision and apply the same rule |
| Unselected candidate provenance README content | CLEAN-02 | README must accurately describe how the candidate was generated (pandoc vs custom script); requires git-log inspection | Inspect `git log -- pinn_instruction/markdown_conversion/` and document tool of origin |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 30s
- [x] `nyquist_compliant: true` set in frontmatter (set after planner verifies all tasks have automated checks)

**Approval:** approved 2026-05-06
