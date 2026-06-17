---
status: archived
purpose: other
created: unknown
milestone: v1.4
phase: 20-plan-audit-legacy
retirement_trigger: milestone complete; superseded by subsequent work
date: 2026-06-04
reviewer: Claude Code + 3 Explore subagents
scope: "Phase 20 planning artifacts (.planning/milestones/v1.4-phases/20-architecture-and-normalization-cleanup/)"
method: "6-dimension structural review + source-file ground-truth verification"
---

# Phase 20 Plan Review — Comprehensive Findings Report

## Executive Summary

Phase 20 planning artifacts (20-CONTEXT.md, 20-GAPS.md, 20-RESEARCH.md, 20-DISCUSSION-LOG.md, 20-01 through 20-05 PLAN.md) are **well-structured and largely rigorous**, but contain **1 critical finding, 7 high-severity findings, 8 medium findings, and 3 low findings** across six review dimensions. The most significant issues are:

1. **CRITICAL**: 20-CONTEXT.md omits three decisions (D-09, D-10, D-11) that are recorded only in 20-DISCUSSION-LOG.md — an executor reading the canonical decision source would miss vocabulary directives, anchoring-bias safeguards, and autonomy justifications that directly affect plan execution.

2. **HIGH**: 20-04 Task 2 pre-writes a specific numeric mass range (`[-0.93, 0.585]`) that cannot be grounded in any cited source — violates the "no inventing numeric ranges" rule.

3. **HIGH**: 20-03's I₃ negative-audit regex is too broad and will false-positive on the correctly-mapped staging range.

4. **HIGH**: The I₃ definitional divergence (ratio-form vs. sorted raw distance) is more severe than characterized — the issue doc defines I₃ as the largest sorted mutual distance, which normalizes to a constant (1.0) with zero shape information. This is a definitional identity crisis, not merely a range disagreement.

---

## Dimension 1: Internal Consistency & Coherence

### CRITICAL-01: Decisions D-09/D-10/D-11 missing from 20-CONTEXT.md

**Location**: 20-CONTEXT.md `<decisions>` section (lines 10-78) vs. 20-DISCUSSION-LOG.md "Deep Review Decisions" (lines 83-117)

**Finding**: 20-CONTEXT.md declares decisions D-01 through D-08 in its `<decisions>` block. Three additional decisions are recorded in 20-DISCUSSION-LOG.md but NOT merged into 20-CONTEXT.md:

- **D-09** ("Realized Support" Is Planning Shorthand): Directly affects 20-04 Task 2's prose wording — the executor must use issue-doc language, not "realized support" as a spec term. This is an execution-affecting decision.
- **D-10** (I₃ Derivation Moved to Research): Affects 20-03 Task 1's workflow — the agent must not see the derivation before completing the source-definition comparison.
- **D-11** (20-04 Remains autonomous:true): Affects the executor's understanding of why 20-04 is safe to run autonomously despite framing choices.

**Impact**: 20-CONTEXT.md is cited as a canonical reference by all four executable plans. If an executor reads only 20-CONTEXT.md (as `@20-CONTEXT.md` context includes), it misses D-09's vocabulary directive (which changes what prose the executor writes in 20-04 Task 2), D-10's anti-anchoring safeguard, and D-11's autonomy rationale.

**Recommendation**: Merge D-09, D-10, D-11 into 20-CONTEXT.md's `<decisions>` section.

---

### HIGH-01: 20-02 Task 2 Step 1 bundles attribution AND branch-scope in one edit

**Location**: 20-02-PLAN.md Task 2 Step 1

**Finding**: The pre-written attribution edit adds both "project-specific/author modification" AND "applied on the skip/power branch only" in a single edit block. D-03 says skip-path scope only "if supported by the source-backed architecture contract." If M8's source review supports attribution but not the branch-scope specificity, this edit overreaches. Steps 3 and 4 correctly have conditional "only if M8-supported" language, but Step 1 does not.

**Recommendation**: Add conditional language to Step 1's branch-scope clause, matching Steps 3-4's pattern.

---

### MEDIUM-01: 20-04 pre-commit diff check is weak

**Location**: 20-04-PLAN.md Task 2 Step 4

**Finding**: The verify step `git diff -- ctl_instruction.md | rg "tanh|E_scale" || true` would match ANY line containing "tanh" or "E_scale", including the newly-added explanatory prose that preserves the formulas. It doesn't verify that the formulas themselves weren't changed — only that those strings appear somewhere in the diff.

**Recommendation**: Use a more targeted check, e.g., comparing the actual formula lines before and after.

---

### LOW-01: Planning artifacts lifecycle not addressed

**Location**: All plans

**Finding**: No plan specifies what happens to 20-CONTEXT.md, 20-RESEARCH.md, or 20-DISCUSSION-LOG.md after execution — whether they're updated, archived, or left as historical record.

---

## Dimension 2: Governance Compliance

### MEDIUM-02: 20-03's semantic-judgment boundary is fuzzy

**Location**: 20-03-PLAN.md Task 1 Step 5-6

**Finding**: Step 5 says "Record whichever physics check applies as verdict evidence." Step 6 says "if grounding the verdict requires semantic judgment the sources do not settle, record defer-with-blocker." The boundary between these two is unclear for a contested I₃ where sources define DIFFERENT quantities. The agent must decide whether the geometry check resolves the dispute or merely applies to one side — that IS semantic judgment. The plan could more explicitly define: "If Step 4 reveals the sources define different quantities, the geometry check does NOT resolve the dispute — record defer-with-blocker."

---

### LOW-02: 20-04 includes pinn_architecture.md as context

**Location**: 20-04-PLAN.md `<context>` block

**Finding**: The @include of pinn_architecture.md is correct for the read-only audit but could be misinterpreted as edit permission. The threat model correctly mitigates this, but a reinforcement in the task instructions would be safer.

---

## Dimension 3: Dependency & Wave Correctness

### CORRECT: Dependency DAG is sound

The DAG `20-01 → {20-02, 20-03} → 20-04` correctly reflects:
- 20-02 and 20-03 edit different files (parallel-safe)
- 20-04 needs both files in their final state
- Transitive dependencies are complete
- 20-05 is correctly blocked with no wave

---

## Dimension 4: Execution Feasibility

### HIGH-02: 20-03's negative-audit regex will false-positive on the correct mapped range

**Location**: 20-03-PLAN.md Task 3 Step 2

**Finding**: The regex `I_3.*\[-1, ?1\]` will match BOTH:
- The WRONG raw annotation: `I_3 = ... ∈ [-1, 1]` (should be caught)
- The CORRECT mapped annotation: `I_3^{in} = 6·I_3 - 1 ∈ [-1, 1]` (should NOT be caught)

After 20-03 Task 2 Step 2 adds the staging-metadata mapping prose, the file WILL contain `[-1, 1]` — correctly, for the mapped range. The audit will then fail on a correct annotation.

**Recommendation**: Narrow the regex to catch only raw-formula annotations, e.g.:
```
rg -n "I_3 = .*\in \[-1, ?1\]"
```
or exclude the mapped form:
```
rg -n "I_3.*\[-1, ?1\]" | grep -v "I_3^{in}"
```

---

### HIGH-03: 20-01 Task 1 bundles two evidence packets in one task

**Location**: 20-01-PLAN.md Task 1

**Finding**: Creating B-01 AND B-10 in one task requires ~14 sub-steps across two independent evidence packets. Each packet needs: template copy, source positions, spec evidence, verdict, FUT-01, Before/After, AC, status log. Splitting into Task 1a (B-01) and Task 1b (B-10) would be cleaner and allow parallel subagent execution.

---

### MEDIUM-03: Skill mismatch for evidence-gated workflows

**Location**: All executable plans' "For agentic workers" note

**Finding**: Plans recommend `superpowers:subagent-driven-development` or `superpowers:executing-plans`. Neither skill is designed for verdict-dependent STOP-gated workflows. `executing-plans` is closer but doesn't model the conditional "if verdict ≠ accept-resolution, derive from Locked Convention" fallback pattern. This increases the risk that an agent applies pre-written prose regardless of the actual verdict.

---

## Dimension 5: Closure-Proof Soundness

### HIGH-04: 20-04 Task 2 Step 2 invents a specific numeric mass range

**Location**: 20-04-PLAN.md Task 2 Step 2

**Finding**: The pre-written prose states:
> "approximately `[-0.93, 0.585]`, not centered on 0"

No cited source provides these specific numbers:
- `simulation_data/Documentation/README.md:320-324` gives mass statistics (min ≈ 0.105, median ≈ 0.897, max ≈ 2.377) but these are RAW masses, not normalized values.
- The tanh normalization transforms these through dataset-wide statistics (μ, σ), which are NOT documented in any cited source.
- The numbers [-0.93, 0.585] appear to be computed from the raw mass statistics through an assumed normalization, but no source documents this computation or result.

This violates the governance rule: "Numeric support ranges are grounded in cited dataset documentation or replaced with qualitative realized-support wording — never invented."

**Recommendation**: Replace the specific numbers with qualitative wording ("asymmetric, with the negative side extending further than the positive side") OR cite the computation that produces [-0.93, 0.585] if it exists in a documented source. If the executor cannot ground these numbers, the prose must use qualitative language per D-06.

---

### HIGH-05: 20-04 Task 3 Step 2 negative audit includes pinn_architecture.md but 20-04 can't edit it

**Location**: 20-04-PLAN.md Task 3 Step 2

**Finding**: The negative audit regex sweeps both `ctl_instruction.md` AND `pinn_architecture.md` for defect-framing prose. If a match is found in `pinn_architecture.md`, 20-04 cannot fix it (it's not a 20-04 write target). The threat model says to "record that as follow-up for the owning pinn_architecture.md plan" — but 20-01 and 20-02 have already committed. There's no mechanism to trigger a follow-up edit to pinn_architecture.md after all Wave 2 plans complete.

**Recommendation**: Clarify the follow-up mechanism — either (a) make 20-02's scope include this check, (b) add a Wave 3 cleanup plan for cross-file consistency, or (c) explicitly document the follow-up as a Phase 21 action item.

---

### MEDIUM-04: AC-ARCH-05 partial-blocker handling is under-specified

**Location**: 20-04-PLAN.md Task 3 Step 3

**Finding**: The plan says "do NOT close AC-ARCH-05 until both M9 and M10 are resolved" but doesn't specify what status to record for the AC if one packet is VERIFIED and the other is blocked. Should the ledger row be HALF-VERIFIED? Should it stay IN_PROGRESS? The Phase 16 evidence template doesn't define a partial-verification status.

---

### LOW-03: Closure proofs correctly defer numeric criteria to Phase 21

All four executable plans explicitly state that "Numeric AC criteria/probes remain Phase 21 (VER-01)." This is consistent with the governance framework and correctly scoped.

---

## Dimension 6: Completeness & Edge Cases (Source-Verified)

### HIGH-06: I₃ definitional divergence is more severe than characterized

**Location**: 20-RESEARCH.md "Known source-definition discrepancy" (lines 235-242); 20-03-PLAN.md Task 1 Step 4

**Subagent-verified findings from ground-truth source files:**

The issue doc (`01-architecture-and-physics-foundations.md`) defines I₃ in **two genuinely different ways**:

1. **Sorted raw distance** (lines 536-542): `I_3 = max(r_01, r_12, r_20)` — a raw distance in physical units. Normalized as `2*(I_3/I_max) - 1 = 1.0` (a CONSTANT with zero shape information).
2. **Ratio form** (line 87): References `I_3 ∈ [0, 1]` with `I3_norm = 2*I3 - 1`.

The resolution doc and current spec use the **ratio form**: `I_3 = (d_short + d_mid - d_long) / (d_short + d_mid + d_long)`.

The conflict is not just about ranges ([-1,1] vs [0,1/3] vs [0,1]) — it's about whether the sources are even defining the **same quantity**. The sorted-distance formulation produces a constant after normalization (1.0), which means it's not a useful shape invariant at all. The ratio form produces a genuine shape descriptor in [0, 1/3].

The plans characterize this as a "range dispute" when it's potentially a "we're not even talking about the same mathematical object" crisis. 20-03's Step 4 comparison is the critical gate, but the pre-written edits in Task 2 already assume the ratio-form definition is correct — creating anchoring pressure even with autonomous:false.

**Recommendation**: Strengthen Step 4's gate language to explicitly state: "If the sources define genuinely different quantities (ratio-form vs. sorted raw distance), and the issue doc's sorted-distance definition produces a constant after normalization (I_3/I_max = 1), record defer-with-blocker with the finding that the issue doc's formulation is degenerate for I₃. Do NOT proceed to Task 2."

---

### MEDIUM-05: E_scale epsilon inconsistency uncaptured

**Subagent-verified**: ctl_instruction.md line 1030 uses `10^-8` for E_scale denominator; ctl_pinn_resolution.md line 607 uses `1e-10`. This is a 100x difference. Phase 20 doesn't claim to fix this (it's not in any ARCH requirement), but if the plan is doing comprehensive normalization-surface cleanup, this inconsistency should at least be noted.

---

### MEDIUM-06: I_norm naming inconsistency confirmed

**Subagent-verified**: ctl_instruction.md uses `I_norm_raw` (lines 644, 750, 755, 1032) and `$I_{\mathrm{norm}}$` (lines 722, 728, 667) interchangeably, with no `I_norm_in` anywhere. This confirms ARCH-04 is a real inconsistency. The 20-05 blocked placeholder correctly identifies the surfaces. No new finding — confirms existing gap analysis.

---

### MEDIUM-07: SIREN/LayerNorm contradictions confirmed

**Subagent-verified**:
- `pinn_architecture.md` has an active `update_omega0()` scheduler (lines 164-189) with exponential decay from 30→10. The resolution doc explicitly orders it deleted. Plans correctly target this.
- `pinn_architecture.md` specifies `elementwise_affine=True` (lines 268, 941). The resolution doc mandates `False`. Plans correctly target this.
- No unexpected contradictions found beyond what the plans already identify.

---

## Findings Summary

| ID | Severity | Dimension | Summary |
|----|----------|-----------|---------|
| CRITICAL-01 | CRITICAL | Consistency | D-09/D-10/D-11 missing from 20-CONTEXT.md |
| HIGH-01 | HIGH | Consistency | 20-02 Step 1 bundles attribution+branch-scope without conditional |
| HIGH-02 | HIGH | Feasibility | 20-03 negative-audit regex false-positives on correct mapped range |
| HIGH-03 | HIGH | Feasibility | 20-01 Task 1 bundles two evidence packets (B-01+B-10) |
| HIGH-04 | HIGH | Closure-proof | 20-04 invents ungrounded numeric mass range [-0.93, 0.585] |
| HIGH-05 | HIGH | Closure-proof | 20-04 can't fix pinn_architecture.md defect-framing if found |
| HIGH-06 | HIGH | Completeness | I₃ definitional divergence more severe than characterized |
| MEDIUM-01 | MEDIUM | Consistency | 20-04 pre-commit diff check is weak |
| MEDIUM-02 | MEDIUM | Governance | 20-03's semantic-judgment boundary is fuzzy |
| MEDIUM-03 | MEDIUM | Feasibility | Skill mismatch for evidence-gated workflows |
| MEDIUM-04 | MEDIUM | Closure-proof | AC-ARCH-05 partial-blocker status under-specified |
| MEDIUM-05 | MEDIUM | Completeness | E_scale epsilon inconsistency (1e-8 vs 1e-10) uncaptured |
| MEDIUM-06 | MEDIUM | Completeness | I_norm naming inconsistency confirmed (no new finding) |
| MEDIUM-07 | MEDIUM | Completeness | SIREN/LayerNorm contradictions confirmed (no new finding) |
| LOW-01 | LOW | Consistency | Planning artifacts lifecycle not addressed |
| LOW-02 | LOW | Governance | 20-04 context includes pinn_architecture.md |
| LOW-03 | LOW | Closure-proof | Numeric criteria correctly deferred to Phase 21 |

---

## Recommended Priority Fixes

1. **Merge D-09/D-10/D-11 into 20-CONTEXT.md** (CRITICAL-01) — one-line additions, prevents executor confusion.
2. **Narrow 20-03's negative-audit regex** (HIGH-02) — prevent false-positive on correct mapped range.
3. **Replace 20-04's numeric mass range with qualitative wording** (HIGH-04) — unless a source can be cited for [-0.93, 0.585].
4. **Strengthen 20-03 Step 4's gate language** (HIGH-06) — explicitly address the degenerate-normalization outcome of the sorted-distance definition.
5. **Split 20-01 Task 1 into 1a/1b** (HIGH-03) — cleaner subagent dispatch.
6. **Add conditional to 20-02 Task 2 Step 1** (HIGH-01) — match Steps 3-4's "only if M8-supported" pattern.
