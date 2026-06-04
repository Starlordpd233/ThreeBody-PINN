# Phase 20 Review Report Remediation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Validate Phase 20 review-report findings as hypotheses, apply only grounded planning fixes, and leave semantic adjudication decisions STOP-gated.

**Architecture:** This is a documentation/planning remediation pass. It updates milestone and Phase 20 process artifacts only; it does not edit framework specs, live code, evidence packets, or acceptance-check implementations.

**Tech Stack:** Markdown planning artifacts, YAML frontmatter, shell verification with `rg`, `sed`, and `git diff --check`.

---

## Validation Ledger

| Finding | Disposition | Action |
|---|---|---|
| `v1.4-GAPS.md` missing Phase 20.5 section | Valid. Phase 20.5 has `20-5-GAPS.md` with three resolved gaps, but the milestone index has no Phase 20.5 section. | Add Phase 20.5 section and update counts to 21 total / 1 open / 20 resolved / 0 deferred. |
| `20-04-PLAN.md` key link misses M10 | Valid. Existing key link pattern covers `M9.*AC-ARCH-05` only. | Add a separate M10 key link with `pattern: "M10.*AC-ARCH-05"`. |
| Suggested regex `M[9-10].*AC-ARCH-05` | Invalid as written. Character-class syntax would not express `M9` or `M10` correctly. | Do not use; prefer explicit M9 and M10 key links. |
| `20-03-PLAN.md` wave/dependency contradiction | Valid. Frontmatter says `wave: 1` while `depends_on` already requires `20-01`; both plans touch the shared ledger. | Change 20-03 to `wave: 2`, keep `depends_on: ["20-01"]`, and remove same-wave concurrency prose. |
| Ambiguous `D-02` references | Partly valid. Most references are already qualified; a few prose references still say bare `D-02` while meaning issue-doc `D-02`. | Qualify semantic prose references as `issue-doc D-02`; preserve literal unauthorized example filenames. |
| M5/I3 pre-written verdict concern | Already mitigated in current dirty tree. The derivation has been moved to `20-RESEARCH.md` as a conditional lemma, and `20-03-PLAN.md` gates it behind source-definition comparison. | Verify the process-first wording remains; do not adjudicate M5 here. |
| 20-01/20-02 accept-resolution wording | Already addressed in current plans. Both plans include verdict preconditions and fallback language. | Verify with `rg`; no edit unless gates are missing. |
| LayerNorm attribution source | Already addressed in current 20-02 plan. Source Positions require the issue doc attribution finding and resolution doc affine/default anchors. | Verify with `rg`; no edit unless citation instructions are missing. |

## Tasks

### Task 1: Add the Phase 20.5 milestone gap-index section

**Files:**
- Modify: `.planning/milestones/v1.4-GAPS.md`

- [ ] Update YAML frontmatter counts to `total_gaps: 21`, `open_gaps: 1`, `resolved_gaps: 20`, `deferred_gaps: 0`, `last_updated: 2026-06-04`.
- [ ] Add a `## Phase 20.5: Sampling Coordinate Allocation` section after Phase 20 with register path `.planning/phases/20-5-sampling-coordinate-allocation/20-5-GAPS.md`.
- [ ] Add rows for `GAP-20-5-01`, `GAP-20-5-02`, and `GAP-20-5-03`, all `RESOLVED-WITH-INSTRUCTION`, matching the local register summary.

### Task 2: Fix Phase 20 plan metadata and links

**Files:**
- Modify: `.planning/phases/20-architecture-and-normalization-cleanup/20-01-PLAN.md`
- Modify: `.planning/phases/20-architecture-and-normalization-cleanup/20-03-PLAN.md`
- Modify: `.planning/phases/20-architecture-and-normalization-cleanup/20-04-PLAN.md`

- [ ] Change `20-03-PLAN.md` frontmatter from `wave: 1` to `wave: 2`; keep `depends_on: ["20-01"]`.
- [ ] Update 20-01 threat-model wording so it no longer implies 20-01 and 20-03 are expected to run concurrently.
- [ ] Add an explicit M10 key link in `20-04-PLAN.md` with `pattern: "M10.*AC-ARCH-05"`.

### Task 3: Qualify remaining D-02 references

**Files:**
- Modify: `.planning/phases/20-architecture-and-normalization-cleanup/20-05-PLAN.md`
- Modify: `.planning/phases/20-architecture-and-normalization-cleanup/20-RESEARCH.md`

- [ ] Change bare semantic references to `issue-doc D-02` where the text means the `I_norm` naming issue.
- [ ] Preserve `evidence/D-02.md` as a literal unauthorized example filename only when its surrounding prose clearly says it must not be created without user instruction.

### Task 4: Verify no semantic adjudication was introduced

**Files:**
- Read/check: `.planning/phases/20-architecture-and-normalization-cleanup/20-01-PLAN.md`
- Read/check: `.planning/phases/20-architecture-and-normalization-cleanup/20-02-PLAN.md`
- Read/check: `.planning/phases/20-architecture-and-normalization-cleanup/20-03-PLAN.md`

- [ ] Confirm 20-03 still requires definition/range/mapping comparison before using the conditional ratio-form lemma.
- [ ] Confirm 20-01 and 20-02 still include verdict preconditions and fallback language.
- [ ] Confirm 20-02 still instructs M8 Source Positions to cite the issue-doc attribution finding.

### Task 5: Verification and commit

**Files:**
- Review all modified files.

- [ ] Run:

```bash
rg -n "^## Phase 20.5|GAP-20-5|total_gaps|open_gaps|resolved_gaps" .planning/milestones/v1.4-GAPS.md
rg -n "M9.*AC-ARCH-05|M10.*AC-ARCH-05" .planning/phases/20-architecture-and-normalization-cleanup/20-04-PLAN.md
sed -n '1,12p' .planning/phases/20-architecture-and-normalization-cleanup/20-03-PLAN.md
rg -n "D-02" .planning/phases/20-architecture-and-normalization-cleanup/20-05-PLAN.md .planning/phases/20-architecture-and-normalization-cleanup/20-RESEARCH.md
rg -n "PRECONDITION|FALLBACK|defer-with-blocker|Definition/range/mapping comparison|Issue-doc anchors|Source Positions" .planning/phases/20-architecture-and-normalization-cleanup/20-01-PLAN.md .planning/phases/20-architecture-and-normalization-cleanup/20-02-PLAN.md .planning/phases/20-architecture-and-normalization-cleanup/20-03-PLAN.md
git diff --check
```

- [ ] Review `git diff` for unrelated changes.
- [ ] Commit the remediation as one atomic commit.
