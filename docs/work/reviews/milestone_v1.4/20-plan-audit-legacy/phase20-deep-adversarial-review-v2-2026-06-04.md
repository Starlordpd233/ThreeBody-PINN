---
status: consumed
purpose: other
created: unknown
milestone: v1.4
phase: 20-plan-audit-legacy
retirement_trigger: milestone complete; superseded by subsequent work
---

# Phase 20 Deep Adversarial Review v2 — Architecture and Normalization Cleanup

**Date:** 2026-06-04
**Reviewer:** Claude (kimi-for-coding), 6-dimension parallel review
**Scope:** `.planning/milestones/v1.4-phases/20-architecture-and-normalization-cleanup/` (9 files, 1,626 lines)
**Framework:** 7-phase adversarial review with 6 parallel dimensional agents
**Classification:** ERROR / GAP / SOURCE_CONFLICT / SUSPECTED / IMPROVEMENT

---

## Executive Summary

| Dimension | Agent | Status | Key Finding |
|-----------|-------|--------|-------------|
| Source Fidelity | A1 | ✅ Mostly clean | 1 IMPROVEMENT + 1 SUSPECTED |
| Mathematical Correctness | A2 | ⚠️ Issues found | 1 ERROR + 1 SOURCE_CONFLICT in live spec |
| Cross-Phase Consistency | A3 | ✅ Clean | 2 non-blocking IMPROVEMENTS |
| Executability & Dependencies | A4 | ✅ Executable | 2 SUSPECTED + 2 IMPROVEMENTS |
| Structural Integrity | A5 | ⚠️ Issues found | 1 ERROR + 1 GAP + 1 SOURCE_CONFLICT + 2 IMPROVEMENTS |
| Temporal Consistency | A6 | ✅ Clean | 1 stale status line (SUSPECTED) |

**Bottom line:** The Phase 20 planning artifacts are well-structured, properly grounded, and executable. No blockers for plans 20-01 through 20-04. However, the **live spec `ctl_instruction.md:768` contains a mathematical error** (`I_3 ∈ [-1, 1]` for the ratio form, which is actually `[0, 1/3]`) that Phase 20-03 correctly identifies and plans to fix. The **three-way I_3 definition mismatch** is the most consequential finding — it requires careful EVID-05 adjudication.

---

## Critical Findings (CRITICAL / MAJOR)

### FIND-20-01: `ctl_instruction.md:768` — Mathematical Error in Live Spec

- **Severity:** MAJOR
- **Classification:** ERROR
- **Location:** `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:768`
- **Dimension:** Mathematical Correctness
- **Evidence:**
  ```
  I_3 = (d_short + d_mid - d_long) / (d_short + d_mid + d_long) ∈ [-1, 1]
  ```
- **Source Check:** Resolution doc `:614` states ratio-form `I_3 ∈ [0, 1/3]` (0 = collinear, 1/3 = equilateral). The `[-1, 1]` annotation conflates the raw ratio-form range with the mapped value `I_3^in = 6·I_3 − 1`.
- **Impact:** If uncorrected, downstream implementers may assume the raw ratio-form quantity already spans `[-1, 1]`, leading to incorrect normalization or curriculum staging. Phase 20-03 Task 2 Step 1 correctly plans to change this to `∈ [0, 1/3]`.
- **Resolution:** Already addressed in 20-03 plan. Verify the edit lands correctly.

### FIND-20-02: Three-Way I₃ Definition Mismatch — EVID-05 Adjudication Required

- **Severity:** CRITICAL
- **Classification:** SOURCE_CONFLICT
- **Location:** `20-03-PLAN.md` (M5 adjudication); `20-RESEARCH.md:178-179`
- **Dimension:** Source Fidelity / Mathematical Correctness
- **Evidence:**

| Source | I₃ Definition | Claimed Range | Mapping |
|--------|---------------|---------------|---------|
| Resolution doc `:608-620` | Ratio form `(d_s+d_m−d_l)/(d_s+d_m+d_l)` | `[0, 1/3]` | `6x − 1` |
| Issue doc M5 `:87` | Sorted distance (normalized by char. length) | `[0, 1]` | `2x − 1` |
| Issue doc code `:536-542` | Sorted mutual distances `sorted([r₀₁, r₁₂, r₂₀])` | N/A (raw) | `2·(Iᵢ/I_max) − 1` |
| `ctl_instruction.md:768` | Ratio form | `[-1, 1]` (ERROR) | Unclear |

- **Impact:** The EVID-05 adjudication must resolve which definition is authoritative before any spec edit proceeds. The 20-RESEARCH.md conditional lemma (ratio-form range derivation `[0, 1/3]`) is valid **only** for the resolution doc's ratio-form definition. If the issue doc's sorted-distance definition prevails, the lemma is irrelevant and a different derivation is needed.
- **Resolution:** 20-03 correctly gates all I₃ edits on the M5 verdict. The executor must:
  1. Complete Step 4 (source-definition comparison) before consulting the conditional lemma
  2. Record `defer-with-blocker` if definitions are too divergent to adjudicate
  3. Only apply the `6·I_3 − 1` map if `accept-resolution` is the verdict

---

## Findings by File

### `20-01-PLAN.md` (ARCH-01 SIREN/omega₀)

#### FIND-20-03: B-01/B-10 Severity Assignment vs. Issue Doc

- **Severity:** MINOR
- **Classification:** IMPROVEMENT
- **Location:** `20-01-PLAN.md` Task 1 Step 1 and Step 6
- **Dimension:** Source Fidelity / Structural Integrity
- **Evidence:** Plan assigns Severity `MINOR` to B-01 and B-10 evidence packets. Issue doc lists both B-01 (`:71`) and B-10 (`:77`) under the **"BLOCKING (Must resolve before implementation)"** category.
- **Impact:** LOW. The plan includes a self-correcting mechanism ("if source review reveals contestation, escalate severity"), but the initial `MINOR` assignment contradicts the issue doc without explicit rationale.
- **Resolution:** Either (a) start with `BLOCKING` and justify downgrading if warranted, or (b) add an explicit rationale in the plan for why the evidence-packet severity differs from the issue-doc category.

### `20-02-PLAN.md` (ARCH-02 LayerNorm)

All claims verified against resolution doc and issue doc. See FIND-20-11 for a minor presentation note.

### `20-03-PLAN.md` (ARCH-03 I₃ / M5 EVID-05)

#### FIND-20-04: I₃ Notation Inconsistency in Edit Instructions

- **Severity:** MINOR
- **Classification:** IMPROVEMENT
- **Location:** `20-03-PLAN.md` Task 2 Step 1 and Step 2
- **Dimension:** Structural Integrity
- **Evidence:** Step 1 shows the current spec line as raw text (`I_3 = ... ∈ [-1, 1]`). Step 2 shows the replacement using LaTeX math mode (`$I_3$`). This inconsistency could cause the executor to apply incorrect formatting.
- **Impact:** LOW. The actual edit is straightforward; this is a presentation issue.
- **Resolution:** Standardize notation in the plan — use the same format as the surrounding spec prose.

#### FIND-20-05: Missing Cross-Reference to Phase 17 Decision

- **Severity:** MINOR
- **Classification:** IMPROVEMENT
- **Location:** `20-03-PLAN.md` line 67
- **Dimension:** Cross-Phase Consistency
- **Evidence:** The plan cites `GAP-17-05` resolution but does not cross-reference `17-CONTEXT.md` D-10 (the M5 metadata-only reframe decision itself).
- **Impact:** LOW. Traceability could be stronger.
- **Resolution:** Add explicit reference to `17-CONTEXT.md` D-10 in addition to the gap register citation.

### `20-04-PLAN.md` (ARCH-05 Energy/Mass Support)

#### FIND-20-06: Pre-Written Numeric Range May Not Be Dataset-Grounded

- **Severity:** MINOR
- **Classification:** SUSPECTED
- **Location:** `20-04-PLAN.md` Task 2 Step 2
- **Dimension:** Source Fidelity / Executability
- **Evidence:** The pre-written prose includes `approximately [-0.93, 0.585]` for hierarchical mass range. Issue doc M10 `:90` states this range without a direct `README.md` citation. `README.md` `:317-324` confirms hierarchical masses vary but does not derive this normalized range.
- **Impact:** LOW. The plan is verdict-gated; STOP conditions direct the executor to use qualitative wording if the range cannot be grounded.
- **Resolution:** No plan change required, but executor should verify the range against `README.md` or use qualitative wording.

#### FIND-20-07: Audit Command Searches for "Realized Support" in Spec

- **Severity:** MINOR
- **Classification:** ERROR
- **Location:** `20-04-PLAN.md` Task 3 Step 1 (line 218)
- **Dimension:** Structural Integrity
- **Evidence:** The positive audit command is: `rg -n "realized|support|occupied|data-generation" ctl_instruction.md`. Since D-09 explicitly prohibits introducing "realized support" as spec vocabulary, searching for the word "realized" in the spec is self-contradictory — the audit searches for a term that should be absent by design. The verify step at line 199 correctly uses a tighter search pattern without "realized".
- **Impact:** LOW. The verify step uses the correct pattern; this is a plan-internal inconsistency, not an executor-blocking defect.
- **Resolution:** Remove `"realized|"` from the Task 3 Step 1 audit command, matching the verify step at line 199.

#### FIND-20-08: Missing Forward-Reference to Phase 19

- **Severity:** MINOR
- **Classification:** IMPROVEMENT
- **Location:** `20-04-PLAN.md` Task 2
- **Dimension:** Cross-Phase Consistency
- **Evidence:** No explicit connection between energy support-range documentation and Phase 19 PHYS-04 (soft conservation regularizer).
- **Impact:** LOW. Not required for correctness.
- **Resolution:** Optional — add a forward-reference note connecting energy support-range to PHYS-04 for reader traceability.

#### FIND-20-09: Missing Shared Evidence-Packet Protocol Document

- **Severity:** MINOR
- **Classification:** GAP
- **Location:** All 4 executable plans (20-01, 20-02, 20-03, 20-04)
- **Dimension:** Structural Integrity
- **Evidence:** The evidence packet creation workflow is duplicated identically across all 4 executable plans: copy template → set header → fill source positions → fill spec evidence → record verdict → fill FUT-01 → fill Before/After → fill AC → status log → update ledger → commit. This is ~7–13 steps repeated 4 times with only packet IDs and section names changed. There is no shared protocol document that each plan could reference. Similarly, the ledger update procedure and the closure audit pattern (positive + negative audit) are duplicated.
- **Impact:** LOW. If the evidence protocol changes (e.g., a new required section is added), 4 plans must be updated independently. This is a maintenance risk, not an execution blocker.
- **Resolution:** Create a shared "Evidence Packet Creation Protocol" document under `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/` and have each Phase 20 plan reference it rather than inline the full procedure. Mark as non-blocking.

#### FIND-20-10: "Realized Support" Terminology Leak into Audit Commands

- **Severity:** MINOR
- **Classification:** SOURCE_CONFLICT
- **Location:** `20-04-PLAN.md` Task 1 Step 1 (line 133) and Task 3 Step 1 (line 218)
- **Dimension:** Structural Integrity
- **Evidence:** Task 1 Step 1 correctly includes the caveat: "'realized support' is a 20-CONTEXT D-06 planning-framing policy, not verbatim source language; if the M9/M10 source review shows the sources frame this incompatibly, record a gap rather than impose D-06." However, Task 3 Step 1's audit command includes `"realized"` in the search pattern. If the spec correctly avoids "realized support" per D-06, the audit may fail to match anything — which is the desired outcome but makes the audit command confusing. Conversely, if "realized" appears in a non-normative context, the audit would match it incorrectly. The verify step at line 199 correctly searches for `"unused|asymmetry carries|dataset-occupied|data-generation"` without `"realized"`.
- **Impact:** LOW. The verify step uses the correct pattern; this is a plan-internal inconsistency between the audit command and the D-06 vocabulary policy.
- **Resolution:** Align the Task 3 Step 1 audit command with the verify step at line 199. Remove `"realized|"` from the search pattern.

### `20-02-PLAN.md` (ARCH-02 LayerNorm) — Additional Finding

#### FIND-20-11: Comma-vs-"and" Inconsistency in LayerNorm Table vs Summary

- **Severity:** MINOR
- **Classification:** IMPROVEMENT
- **Location:** `20-02-PLAN.md` Task 2, Step 3 (line 167) vs Step 4 (line 168)
- **Dimension:** Structural Integrity
- **Evidence:** Step 3 (hyperparameter table) uses comma-separated values: `elementwise_affine=False, eps=1e-5`. Step 4 (summary row) uses "and": `with elementwise_affine=False and eps=1e-5`. This is a minor presentation inconsistency. The table format naturally uses commas; the prose summary naturally uses "and".
- **Impact:** LOW. Acceptable as intentional style matching (table = list, prose = sentence).
- **Resolution:** No action required. Note as intentional if desired.

### `20-05-PLAN.md` (ARCH-04 — BLOCKED)

No findings. Correctly blocked by GAP-20-01.

### `20-CONTEXT.md`

#### FIND-20-09: Status Line Stale Relative to Plan Completion

- **Severity:** MINOR
- **Classification:** SUSPECTED
- **Location:** `20-CONTEXT.md` line 4
- **Dimension:** Temporal Consistency
- **Evidence:** Status says "Ready for research and planning" but planning is complete (plans 20-01 through 20-05 exist, dated 2026-06-03/04). `STATE.md` (2026-06-04) correctly reflects "Planned; ready to execute."
- **Impact:** LOW. Cosmetic inconsistency.
- **Resolution:** Update status line to match `STATE.md`.

### `20-RESEARCH.md`

No findings. Well-structured evidence map.

### `20-GAPS.md`

No findings. Correctly records GAP-20-01.

### `20-DISCUSSION-LOG.md`

No findings. All decisions (D-09, D-10, D-11) correctly reflected in plans.

---

## Cross-Cutting Issues

### CROSS-01: Evidence Packet Creation Workflow Duplication

- **Severity:** MINOR
- **Classification:** IMPROVEMENT
- **Dimension:** Structural Integrity
- **Evidence:** All 4 executable plans (20-01, 20-02, 20-03, 20-04) independently specify the same evidence packet creation workflow: copy template → fill header → fill source positions → fill spec evidence → record verdict → fill FUT-01 → fill Before/After → fill AC → status log → update ledger → commit.
- **Impact:** LOW. Duplication increases maintenance burden if the template changes.
- **Resolution:** Consider creating a shared "Evidence Packet Creation Protocol" document under `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/` that all plans reference, rather than repeating the pattern 4 times.

### CROSS-02: Ledger Commit Coordination in Wave 2

- **Severity:** MINOR
- **Classification:** IMPROVEMENT
- **Dimension:** Executability & Dependencies
- **Evidence:** Wave 2 plans (20-02, 20-03, 20-04) each edit `16-ISSUE-LEDGER.md`. While they edit different rows, the per-finding notes sections (which append status-log lines) could shift line numbers for subsequent plans.
- **Impact:** LOW. The commit-after-each-task policy mitigates this, but there is no explicit "commit after each plan before starting the next plan in the same wave" policy.
- **Resolution:** Add an explicit note to `20-CONTEXT.md` or `STATE.md`: "Wave 2 plans must each commit their ledger changes before the next plan begins."

### CROSS-03: Spec Drift in `pinn_architecture.md`

- **Severity:** MAJOR
- **Classification:** ERROR (in live spec, not in plans)
- **Dimension:** Mathematical Correctness / Source Fidelity
- **Evidence:**
  - `pinn_architecture.md:172` still contains the `update_omega0` dynamic scheduler that resolution doc `:685` mandates removing. Phase 20-01 correctly plans to remove it.
  - `pinn_architecture.md:268` shows `elementwise_affine=True` in the hyperparameter table, conflicting with resolution doc `:664` (`False` by default). Phase 20-02 correctly plans to change it.
- **Impact:** MEDIUM. These are pre-existing spec drift issues that Phase 20 plans correctly address. The plans are not at fault — they are the fix.
- **Resolution:** Verify 20-01 and 20-02 edits land correctly.

---

## Prioritized Recommendations

| Priority | Finding | Action | Owner |
|----------|---------|--------|-------|
| P1 (CRITICAL) | FIND-20-02: I₃ definition mismatch | Complete EVID-05 adjudication carefully; do not skip Step 4 definition comparison | 20-03 executor |
| P2 (MAJOR) | FIND-20-01: Spec error `I_3 ∈ [-1,1]` | Verify 20-03 Task 2 corrects to `∈ [0, 1/3]` | 20-03 executor |
| P2 (MAJOR) | CROSS-03: Spec drift (scheduler + affine default) | Verify 20-01 and 20-02 edits remove/fix | 20-01/20-02 executor |
| P3 (MINOR) | FIND-20-03: B-01/B-10 severity | Reconcile with issue doc BLOCKING label or add rationale | 20-01 plan author |
| P3 (MINOR) | FIND-20-06: Mass range grounding | Executor must verify or use qualitative wording | 20-04 executor |
| P4 (COSMETIC) | FIND-20-09: Stale status line | Update `20-CONTEXT.md` status to "Planned; ready to execute" | Phase 20 coordinator |
| P4 (COSMETIC) | FIND-20-09: Missing shared evidence-packet protocol | Create shared protocol document under Phase 16 | Phase 20 coordinator |
| P4 (COSMETIC) | FIND-20-04, 20-05, 20-07, 20-08, 20-10, 20-11, CROSS-01, CROSS-02 | Address at convenience | Phase 20 coordinator |

---

## Gap Register Assessment

| Gap | Status | Assessment |
|-----|--------|------------|
| GAP-20-01 | OPEN ✅ | Correctly blocks ARCH-04. No new gaps identified by this review. |

**One GAP-level finding added post-report (Agent A5):** FIND-20-09 identifies a missing shared evidence-packet protocol document. This is a process-artifact schema gap — not a source-silent semantic question — and does not block Phase 20 execution. It is classified as a maintenance-risk GAP rather than a STOP-protocol blocker.

Otherwise, the review found no source-silent semantic questions requiring STOP protocol intervention. All other issues are either: (a) pre-existing spec errors that Phase 20 plans correctly address, (b) minor structural/terminology improvements, or (c) execution guidance for the executor.

---

## Appendix A: Methodology Notes

### Review Framework

This review followed a 7-phase adversarial framework:

1. **Phase 0: Pre-Review Sanity Check** — Verified all 9 files readable, all external references resolvable
2. **Phase 1: Contextual Grounding** — Indexed source materials per v1.4 governance hierarchy
3. **Phase 2: Rapid Sequential Scan** — Built claim-to-source dependency graph
4. **Phase 3: Dimensional Fan-Out** — Dispatched 6 parallel agents:
   - A1: Source Fidelity
   - A2: Mathematical Correctness
   - A3: Cross-Phase Consistency
   - A4: Executability & Dependencies
   - A5: Structural Integrity (completed after report — 5 findings)
   - A6: Temporal Consistency
5. **Phase 4: Synthesis** — Merged findings, applied conflict-resolution heuristics
6. **Phase 5: Adversarial Verification** — Challenged top findings for false positives
7. **Phase 6: Report Generation** — This document

### Classification Definitions

- **ERROR**: Objective, verifiable mistake
- **GAP**: Source-silent semantic question (STOP protocol applies)
- **SOURCE_CONFLICT**: Multiple sources contradict
- **SUSPECTED**: Suspected issue but cannot fully verify
- **IMPROVEMENT**: Suggestion for clarity or completeness

### Conflict-Resolution Heuristics Applied

- **H1**: A1 grounded + A2 wrong → source potentially erroneous (applied to FIND-20-01)
- **H2**: A3 consistent + A5 collision → structural defect wins (applied to FIND-20-04)
- **H3**: A2 "cannot-verify" → default to SUSPECTED or GAP, never ERROR

### Sources Consulted

- `ctl_pinn_resolution.md` (1,596 lines) — candidate verdict source
- `01-architecture-and-physics-foundations.md` — issue doc
- `pinn_architecture.md` — active framework spec
- `ctl_instruction.md` — active framework spec
- `16-ISSUE-LEDGER.md` — evidence framework
- `evidence/_TEMPLATE.md` — packet template
- `REQUIREMENTS.md` — requirements
- `ROADMAP.md` — success criteria
- `v1.4-GAPS.md` — milestone gap index
- Phase 16-19 gap registers and context files

---

## Appendix B: Verification Checklist for Phase 20 Execution

Before executing any Phase 20 plan, verify:

- [ ] All 6 missing evidence packets (B-01, B-10, M5, M8, M9, M10) are created from `_TEMPLATE.md`
- [ ] M5 uses full EVID-05 process (Steps 5-9: Physics Check, Root-Cause, Locked Convention, Which Source)
- [ ] M5 Step 4 definition comparison completes before any range derivation is consulted
- [ ] B-01/B-10 severity reconciled with issue doc BLOCKING label
- [ ] `ctl_instruction.md:768` corrected from `[-1, 1]` to `[0, 1/3]` (if accept-resolution)
- [ ] `pinn_architecture.md:172` scheduler removed (20-01)
- [ ] `pinn_architecture.md:268` elementwise_affine changed to False (20-02)
- [ ] No plan edits `pinn/` live code
- [ ] Each plan commits before next wave-2 plan begins
- [ ] GAP-20-01 remains OPEN; no ARCH-04 edits attempted

---

*Report generated by Phase 20 Deep Adversarial Review Framework v2.*
*All findings traceable to specific source document line numbers verified during review.*
