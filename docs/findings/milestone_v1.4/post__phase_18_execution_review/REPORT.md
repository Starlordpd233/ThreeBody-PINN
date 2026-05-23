---
review: phase-18-post-execution-consolidated
date: 2026-05-21
consolidated_from: REPORT.md (01:50), post__phase_18_execution_review.md (01:52), REVIEW.md (02:04)
reviewer: Claude Opus 4.7 (ultrathink) — deep review via 6 parallel subagents + independent 4-agent audit cross-check
scope: All Phase 18 framework-spec edits, evidence packets, ledger transitions, gap register, divergence inventory, summaries, and verification artifacts
method: 6 parallel subagents + direct verification-suite execution + governance compliance check + cross-check against independent 4-agent audit
verdict: PASS-WITH-ISSUES — substantive spec work is flawless; 1 critical traceability issue (unreplaced ${EDIT_SHA} placeholders), 3 moderate process-quality issues, 4 minor documentation inconsistencies. 0 content correctness issues.
---

# Phase 18 Post-Execution Review (Consolidated)

## Executive Summary

Phase 18 (Frame and Gauge Contracts) has been executed **successfully on substance, with process-artifact quality issues**. The framework-spec edits, evidence packets, gap resolutions, and ledger closures are correct and complete. All 7 planned deliverables pass content verification. Eight issues were found — one critical traceability gap (unreplaced placeholder commit SHAs in the issue ledger), three moderate process-quality issues, and four minor documentation inconsistencies. No content-correctness issues. All five governance gaps are properly resolved with full STOP protocol compliance.

## Review Methodology

Three independent review passes were conducted and consolidated into this report:

| Pass | Agents | Scope | Key Contribution |
|------|--------|-------|-----------------|
| Pass 1 (REPORT.md) | 5 parallel subagents | Framework specs, evidence, boundaries, gaps, divergence | Baseline content verification; 1 cosmetic finding |
| Pass 2 (post__phase_18_execution_review.md) | 4 parallel verification agents | Spec content, evidence/ledger, process/governance, cross-reference consistency | Caught critical SHA placeholders, fabricated timestamps, stale validation table, missing commit reference |
| Pass 3 (REVIEW.md) | 6 parallel subagents + independent audit cross-check | All Phase 18 artifacts + strict full suite execution + governance compliance | Deepest pass; verified fixes applied, cross-checked against Pass 2, added commit inventory |

All three passes agree: **the substantive spec work is correct and complete.** All issues are in process artifacts, not in the framework specs themselves.

---

## Requirement-by-Requirement Verification

### FRAME-01 — Unified Preprocessing Pipeline: PASS

`ctl_instruction.md` contains exactly one `## Step 2: Unified Preprocessing Pipeline` (line 382) with six substeps (2.1–2.6) implementing the fixed-order pipeline:

- **2.1** Mass-invariance check (`max_t,i |m_i(t) - m_i(0)| < 1e-15`, line 404)
- **2.2** COM recenter and zero-momentum boost (lines 414–437)
- **2.3** Canonical ordering with original-file-order as final tie-break (lines 444–448)
- **2.4** Canonical rotation gauge with `η_gauge = 1e-8`, dimensionless thresholds, `gauge_degenerate_rho` reject/quarantine, deterministic `e_y` sign-flip, and FRAME-04 3D Cartesian output guard (lines 457–571)
- **2.5** Global scaling with D and V definitions (lines 573–596)
- **2.6** COM assertions (`||sum_i m_i r_i'|| < 1e-12`, `||sum_i m_i v_i'|| < 1e-12`) and 17 stored metadata keys (lines 598–636)

Old `Step 2.5: Verify Center-of-Mass (COM) Frame` is absent. Old Step 4 canonical ordering was removed and replaced with a pointer to Step 2.3 (D-04, line 893).

### FRAME-02 — COM/Momentum Assertions: PASS

- **Input side**: `ctl_instruction.md` Step 2.6 asserts `||sum_i m_i r_i'|| < 1e-12` and `||sum_i m_i v_i'|| < 1e-12` for preprocessed samples (lines 603–609).
- **Output side**: `pinn_architecture.md` Section 5.3 defines the hard mass-weighted COM projection with explicit "Phase 18 FRAME-02 assertion" naming (lines 800–820). The formula, the "hard" (architectural, not soft penalty) designation, and the Phase 17 D-02 lineage are all present.
- **Cross-reference note**: Section 5.3 does not back-reference `ctl_instruction.md` Step 2.6 by name. The plan's own verification command (18-01-PLAN.md:379) only requires the markers `FRAME-02 assertion|mass-weighted position COM is zero|automatic derivatives of the projected positions|Phase 21 executes the numerical acceptance checks`, all of which are present. PASS per plan criteria.

### FRAME-03 — Sampling-Frame Reconciliation: PASS

`sampling_method.md` contains both required frame notes:

- **Hierarchical** (lines 71–79): COM enforced before perturbation, Gaussian `N(0, 0.01)` perturbation moves out of COM, observed offsets (`|COM|` median ~9e-3, `|P|` median ~3e-2), FRAME-01 pipeline recenters.
- **Quasi-random** (lines 133–138): `p3 = -(p1+p2)` for COM by construction, `v1 = -v2/2`, `v3 = -v2/2` for zero momentum by construction, FRAME-01 pipeline still applies.
- **Sobol coordinate-allocation text preserved** (lines 119, 125–131): `u_4, u_5, u_6` triplet intact for Phase 20.5.
- **Global Scaling paragraph preserved** (lines 118–121): untouched.
- **Correction applied**: Commit `34cd746` fixed one inherited quasi-random momentum sentence that conflicted with `simulation_data/` generator behavior (per D-10 authority). The Phase 20.5 Sobol target text remains untouched.

### FRAME-04 — 3D Cartesian Output Guard: PASS

`ctl_instruction.md` Step 2.4 (lines 564–571) contains the dedicated `#### FRAME-04 3D-Cartesian output guard`:
- "The Jacobi velocities remain fully 3D, the trajectory evolves in full 3D, and the model output remains 9D Cartesian positions"
- "The output is **not planar** and **not invariant-only**"
- `pinn_architecture.md` lines 765–767 and 862 independently confirm the 9D Cartesian output.

### VER-05 — Lifecycle Closure (B-05, M3): PASS

| Evidence Packet | Status | Verdict | AC | Resolution Doc Citations |
|----------------|--------|---------|-----|--------------------------|
| B-05.md | VERIFIED | accept-resolution | AC-FRAME-01 | ctl_pinn_resolution.md:255-443, :1125-1137 |
| M3.md | VERIFIED | accept-resolution | AC-FRAME-01 | ctl_pinn_resolution.md:255-443, :1125-1137 |

Both packets:
- Cite the resolution document by line number, NOT pinn/ live code
- Include FUT-01 hand-off disclaimers ("Live code in `pinn/` is NOT a v1.4 evidence source")
- Mark all contested sections as "Not contested"
- Reserve AC-FRAME-01 with full named acceptance check sections

Ledger rows (16-ISSUE-LEDGER.md lines 23, 31): Both B-05 and M3 are `VERIFIED | accept-resolution`.
AC-FRAME-02/03/04 reservation note present (lines 133–137).

GAP-18-03 authorization was obtained before B-05/M3 closure: the gap is `RESOLVED-WITH-INSTRUCTION` (18-GAPS.md line 97, user approved Phase 18-local structural closure criteria for AC-FRAME-01 only on 2026-05-21).

### D-06 / M4 Preservation: PASS

The M4 sentence is preserved at `ctl_instruction.md` lines 914–915:
> "The 13 constraints for an 8-dimensional reduced phase space ensure over-determination and uniqueness."

Verified with wrap-tolerant ripgrep (`rg -nU`). M4 content was never edited; GAP-18-05 resolved the regex mismatch without touching M4 text.

### 18-CODE-DIVERGENCE.md: PASS

File exists at `.planning/phases/18-frame-and-gauge-contracts/18-CODE-DIVERGENCE.md` with:
- Five-column schema (Surface, Live code file:line, Spec target, FUT-01 item, FUT-01 priority)
- All six required divergence surfaces: COM/boost preprocessing, Scaling order, Canonical ordering, Rotation gauge, Stored metadata, Output metadata threading
- Preamble establishes FUT-01 handoff-only purpose; all `pinn/` paths are coordinates only
- Every row maps to a Phase 18 decision (D-01 through D-07, D-14)

### No pinn/ Diff: PASS

Zero staged or unstaged diffs in `pinn/` directory. Verified via `git diff` and `git diff --cached`.

### Phase 17 Forward-References: PASS

All Phase 17 forward-references in `ctl_instruction.md` that previously pointed to not-yet-written Phase 18 content are now satisfied. The pipeline, IC13 contract, FRAME-01 preprocessing contract, and ordered raw masses are all defined within the document or `pinn_architecture.md`.

### Gap Register: PASS

| Gap | Status |
|-----|--------|
| GAP-18-01 | RESOLVED-WITH-INSTRUCTION |
| GAP-18-02 | RESOLVED-WITH-INSTRUCTION |
| GAP-18-03 | RESOLVED-WITH-INSTRUCTION |
| GAP-18-04 | RESOLVED-WITH-INSTRUCTION |
| GAP-18-05 | RESOLVED-WITH-INSTRUCTION |

18-GAPS.md frontmatter: `open_gaps: 0`, `resolved_gaps: 5`. All 16 milestone-level gaps resolved (v1.4-GAPS.md: `open_gaps: 0`, `resolved_gaps: 16`).

---

## Issues Found

### Issue 1 — CRITICAL: Unreplaced `${EDIT_SHA}` Placeholder Tokens in Issue Ledger

**Location**: `.planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md`, lines 142, 144, 236, 238

**Problem**: The B-05 and M3 transition logs contain `${EDIT_SHA}` placeholders that were never substituted with actual commit SHAs:

| Line | Placeholder | Should Be | Commit Description |
|------|------------|-----------|--------------------|
| 142 | `EDIT_SHA_18_01_T1` | `d31e82c` | Open frame evidence packets |
| 144 | `EDIT_SHA_18_03_T2` | `98bc955` | Verify frame gauge contracts |
| 236 | `EDIT_SHA_18_01_T1` | `d31e82c` | Open frame evidence packets |
| 238 | `EDIT_SHA_18_01_T3` | `26d9627` | Verify scaling order frame contract |

**Impact**: Breaks traceability between the issue ledger and git history. A future auditor cannot determine which commits performed the lifecycle transitions without cross-referencing SUMMARY files.

**Root Cause**: The plan templates (`18-01-PLAN.md` Tasks 1 and 3 action blocks) used `${EDIT_SHA}` substitution tokens; the executing agent never replaced them with actual SHAs before committing the ledger.

**Fix**: See [Fixes Applied](#fixes-applied-during-this-review) below.

---

### Issue 2 — MODERATE: Fabricated Completion Timestamps in SUMMARY Frontmatter

**Location**: `18-01-SUMMARY.md`, `18-02-SUMMARY.md`, `18-03-SUMMARY.md`

**Problem**: The `completed:` timestamps in SUMMARY frontmatter do not match actual git committer dates:

| SUMMARY | Claimed Timestamp | Actual Git Commit | Delta |
|---------|-------------------|-------------------|-------|
| 18-01 | 2026-05-21T05:20:38Z | `96a3bca` at 05:21:52Z | -74 sec |
| 18-02 | 2026-05-21T05:23:56Z | `dc57496` at 05:24:43Z | -47 sec |
| 18-03 | 2026-05-21T05:27:17Z | `a426bb0` at 05:28:07Z | -50 sec |

**Impact**: Undermines trust in process-artifact metadata. The timestamps appear to be estimates rather than derived from `git log --format=%cI`.

**Root Cause**: The executing agent wrote estimated timestamps rather than querying git for the actual committer date after commit.

**Fix**: Update each SUMMARY's `completed:` field to match the actual committer date of its summary commit. See [Fixes Applied](#fixes-applied-during-this-review) below.

---

### Issue 3 — MODERATE: Post-Review Correction Committed After Phase Declared Complete

**Location**: Git history; commit `34cd746` vs summary commit `a426bb0`

**Problem**: Commit `34cd746` (`docs(18-02): align quasi-random momentum prose`) has committer date `2026-05-21T05:31:26Z`, which is **3 minutes 19 seconds after** the `18-03-SUMMARY.md` commit (`a426bb0` at `05:28:07Z`). The phase was declared complete before the mandatory review gate correction landed.

**Impact**: Temporal inconsistency. The substantive fix (`34cd746`) is correct; the issue is process ordering — completion was declared prematurely.

**Fix**: Noted in `18-VERIFICATION.md` Notes. No further action needed for the fix itself.

---

### Issue 4 — MODERATE: Stale Gap Narrative in Milestone Gap Index

**Location**: `.planning/milestones/v1.4-GAPS.md`, line 38

**Problem**: The narrative paragraph described GAP-18-05 as `OPEN` despite the frontmatter (`open_gaps: 0`) and table row correctly showing `RESOLVED-WITH-INSTRUCTION`.

**Status**: **FIXED** during this review (see [Fixes Applied](#fixes-applied-during-this-review)).

---

### Issue 5 — MINOR: Self-Reported Verification Claims Without External Evidence

**Location**: `18-01-SUMMARY.md` line 122; `18-02-SUMMARY.md` line 110; `18-03-SUMMARY.md` line 115

**Problem**: Each SUMMARY contains a "Self-Check: PASSED" section claiming verification passed without command logs, CI output, or shell transcripts. The verification claims are circular (the artifact claims it verified itself).

**Impact**: Low — spec content was independently verified as correct by this review's strict-full-suite execution.

---

### Issue 6 — MINOR: Stale Governance Notices Omit GAP-18-05

**Locations**: `18-CONTEXT.md:9`, `18-GAPS.md:9`

Both governance notice lines mention only 4 gaps (GAP-18-01 through 04) and omit GAP-18-05. Written before GAP-18-05 was discovered and never updated. Cosmetic only.

---

### Issue 7 — MINOR: Validation Document Shows Stale Per-Task Status

**Location**: `.planning/phases/18-frame-and-gauge-contracts/18-VALIDATION.md` lines 50-55

**Problem**: The "Per-Task Verification Map" table shows all three tasks (18-01-01, 18-02-01, 18-03-01) with Status `pending`. Yet `18-VERIFICATION.md` claims "Phase 18 strict full suite from `18-VALIDATION.md`" passed.

**Impact**: The validation document was not updated after execution, creating ambiguity about whether the formal per-task verification map was ever actually completed.

**Root Cause**: The executing agent ran the strict suite commands but never updated the per-task status table in `18-VALIDATION.md`.

**Fix**: Update the per-task verification map to show `green` status for all three tasks, or document why the formal map was bypassed.

---

### Issue 8 — MINOR: 18-03-SUMMARY Omits Post-Review Correction Commit

**Location**: `.planning/phases/18-frame-and-gauge-contracts/18-03-SUMMARY.md` lines 76-80

**Problem**: The "Task Commits" section lists only `0e569ba` and `98bc955`. It omits `34cd746` (`docs(18-02): align quasi-random momentum prose`), even though this commit is part of the Phase 18 work stream and is referenced in `18-REVIEW.md` and `18-VERIFICATION.md`.

**Impact**: Incomplete commit inventory in the final summary.

**Fix**: Add `34cd746` to the 18-03-SUMMARY Task Commits section with a note that it is the post-review correction inherited from the 18-02 review gate.

---

### Issue 9 — INFO: M4 Sentence Remains Per Resolution Doc §10.4 (Out of Scope)

The resolution doc §10.4 requires deleting and replacing the M4 constraint-counting sentence. Phase 18 correctly did NOT edit this per D-06 (Phase 19/PHYS-06 scope). NOT a Phase 18 violation.

---

### Issue 10 — INFO: Minor Wording Change to Step 4 Continuity Statement

The continuity statement changed from "All components vary continuously with the initial conditions" to "All network IC slots vary continuously with the preprocessed initial conditions." Benign terminology alignment; not a D-06 violation.

---

## Fixes Applied During This Review

| # | What | Where | Details |
|---|------|-------|---------|
| 1 | Stale GAP-18-05 narrative | `v1.4-GAPS.md:38` | Changed `is \`OPEN\`` → `is \`RESOLVED-WITH-INSTRUCTION\`` with accurate resolution summary |
| 2 | Unreplaced `${EDIT_SHA}` tokens | `16-ISSUE-LEDGER.md` lines 142,144,236,238 | Replaced `EDIT_SHA_18_01_T1` → `d31e82c`, `EDIT_SHA_18_03_T2` → `98bc955`, `EDIT_SHA_18_01_T3` → `26d9627` |
| 3 | Fabricated timestamps | `18-01-SUMMARY.md`, `18-02-SUMMARY.md`, `18-03-SUMMARY.md` | Updated `completed:` to match actual git committer dates |

### Non-Issues Investigated and Cleared

| Concern | Investigation | Conclusion |
|---------|--------------|------------|
| FRAME-02 doesn't back-reference Step 2.6 | Plan's own verification command (18-01-PLAN.md:379) doesn't require this | PASS per plan criteria |
| test_phase12_validation.py modified | Diff shows comment-only updates removing stale v1.3 closure audit references | Benign; no test logic changed |
| Pre-existing uncommitted changes | 18-02-PLAN.md, 18-RESEARCH.md, AGENTS.md were modified before Phase 18 execution | Separate from Phase 18 core work |
| Codebase drift warning | .gitignore, AGENTS.md, ANTIGRAVITY.md, GEMINI.md changes are pre-existing or unrelated | Advisory only; non-blocking by workflow contract |

---

## Verification Suite Execution

The strict full suite from 18-VALIDATION.md was run fresh during this review. All 10 commands pass:

1. Evidence/divergence files exist: PASS
2. Frame/gauge contract markers in ctl_instruction.md: PASS
3. Rotation-gauge algorithm markers: PASS
4. Sampling-frame text in sampling_method.md: PASS
5. 3D Cartesian output guard: PASS
6. B-05 and M3 VERIFIED in ledger: PASS
7. Phase 18/FRAME/FUT-01 in divergence inventory: PASS
8. Phase 20.5 heads-up in v1.4-GAPS.md: PASS
9. M4 text preserved (wrap-tolerant): PASS
10. No staged/unstaged pinn/ diff: PASS

---

## Commit Inventory

All Phase 18 commits on `milestone/v1.4` (chronological):

| Commit | Description |
|--------|-------------|
| `5d6a5b1` | Record phase 18 context session |
| `696fdb5` | Phase 18 planning artifacts |
| `4e6ef56` | Phase 18 plan review and Phase 20.5 analysis |
| `02291d6` | Resolve frame structural criteria gap (GAP-18-03) |
| `67f018e` | Close GAP-18-04 (rotation-gauge threshold contract) |
| `d31e82c` | Open frame evidence packets (B-05, M3) |
| `1d5a180` | Surface GAP-18-05 (M4 regex vs line-wrapped text) |
| `5f979f6` | Resolve GAP-18-05 (wrap-tolerant M4 check) |
| `83d6a0a` | Define unified preprocessing pipeline in ctl_instruction.md |
| `26d9627` | Verify scaling order frame contract (18-01) |
| `96a3bca` | Summarize frame gauge contract (18-01) |
| `a940474` | Reconcile sampling frame behavior (18-02) |
| `783c5a5` | Record sampling frame fix (18-02) |
| `dc57496` | Summarize sampling frame reconciliation (18-02) |
| `0e569ba` | Record frame gauge code divergence (18-03) |
| `98bc955` | Verify frame gauge contracts (18-03) |
| `a426bb0` | Summarize frame gauge verification (18-03) |
| `34cd746` | Align quasi-random momentum prose (review fix) |
| `162098c` | Add phase code review report |
| `18aacde` | Verify phase goal |
| `96236cd` | Complete phase execution |

---

## Verdict

**Phase 18 passes post-execution review.** All 7 planned deliverables exist and pass verification. All 5 requirements (FRAME-01/02/03/04, VER-05) are satisfied. All 5 governance gaps are resolved with full STOP protocol compliance verified across all gaps. Zero pinn/ files were modified. The M4 sentence is preserved. The Sobol coordinate-allocation text is untouched for Phase 20.5.

**Three fixes applied** during this review: stale GAP-18-05 narrative, unreplaced `${EDIT_SHA}` tokens, and fabricated timestamps.

**Five additional informational findings** (Issues 6-10) are cosmetic or out-of-scope and do not block the phase. Issues 7 and 8 (stale validation table, missing commit reference) are recommended cleanup but not required for phase closure.

**STOP protocol compliance verified**: All 5 gaps showed clean STOP/resume patterns — work halted upon gap discovery, resumed only after user instruction. No violations detected.

**No blocking issues. Phase 18 is complete and verifiably correct.**
