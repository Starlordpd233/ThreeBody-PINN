---
title: "Phase 20 Planning Artifacts — Independent Review Report"
created: 2026-06-03
scope: "All 9 Phase 20 planning artifacts (CONTEXT, RESEARCH, GAPS, DISCUSSION-LOG, 5 plans)"
review_type: "Multi-dimensional review with source-of-truth verification"
verifier: "Claude Opus 4.6 with 4 parallel verification subagents"
status: "Complete"
---

# Phase 20 Planning Artifacts — Independent Review Report

## Executive Summary

Phase 20 planning artifacts (9 files: CONTEXT, RESEARCH, GAPS, DISCUSSION-LOG, and 5 plan files) were reviewed across 7 dimensions: grounding compliance, internal consistency, evidence protocol correctness, STOP protocol adherence, dependency graph correctness, threat model completeness, and cross-reference accuracy. Four parallel subagents independently verified all source-of-truth claims against the Phase 16 Issue Ledger, REQUIREMENTS.md, ROADMAP.md, the evidence template, and both framework specs.

**Overall assessment:** The Phase 20 plans are **exceptionally well-constructed**. Every source-of-truth claim tested — Phase 16 ledger rows, requirement text, roadmap success criteria, line-number references in both framework specs, evidence template structure, and missing packet confirmations — was verified with **zero discrepancies**. The STOP protocol is properly deployed at every decision point. The evidence-first workflow is consistently applied across all executable plans.

**Critical errors found: 0.**

**High-priority findings: 2** (one grey-area grounding concern, one missing dependency).

**Medium-priority findings: 5** (pre-adjudication risk, template section gap, ledger concurrency, severity choices, partial-blocker handling).

**Low-priority findings: 4** (status-log format, cross-reference path, wave-drift note, regex coverage).

**Grey areas for discussion: 3** (D-06 framing classification, I₃ derivation boundary, ARCH-04 deferral strategy).

---

## 1. Verification Results

### 1.1 Phase 16 Ledger Cross-Reference

All 11 claims verified against `16-ISSUE-LEDGER.md`:

| Claim | Lines Cited | Verified | Discrepancy |
|-------|-------------|----------|-------------|
| B-01 reserved (AC-ARCH-01, pinn_architecture.md) | ~19 | ✅ | None |
| B-10 reserved (AC-ARCH-01, pinn_architecture.md) | ~28 | ✅ | None |
| M5 reserved, EVID-05 required (AC-ARCH-03) | ~33 | ✅ | None |
| M8 reserved (AC-ARCH-02, pinn_architecture.md) | ~36 | ✅ | None |
| M9 reserved (AC-ARCH-05, ctl_instruction.md) | ~37 | ✅ | None |
| M10 reserved (AC-ARCH-05, ctl_instruction.md) | ~38 | ✅ | None |
| B-01/B-10 shared AC-ARCH-01 per-finding notes | ~64–73 | ✅ | None |
| M5 contested status per-finding notes | ~279–285 | ✅ | None |
| M8 per-finding notes | ~320–324 | ✅ | None |
| M9/M10 per-finding notes | ~329–349 | ✅ | None |
| No D-02 / ARCH-04 / I_norm row exists | (full file search) | ✅ | None |

**Bonus finding:** Ledger line 33 annotates M5's spec section as `data-processing-pipeline-full.py *(pre-2026-05-19; now v1.3-era artifact, not spec)*`. Plan 20-03's threat model (line 84) correctly identifies this and warns executors not to cite it. ✅

### 1.2 REQUIREMENTS.md and ROADMAP.md

All ARCH-01 through ARCH-05 requirements verified at lines 47–51 with exact text match. Phase 20 goal, dependencies, success criteria (lines 202–215), and plan listing all verified. GAP-20-01 is present in `v1.4-GAPS.md` milestone index (lines 58–64). ✅

### 1.3 Evidence Template Structure

The template (`_TEMPLATE.md`, 103 lines) was verified to contain all sections referenced by the plans: Header (with 8+1 fields), Source Positions (3-column table), Spec Evidence, Verdict (5-value enum matching exactly), Before/After Spec Note, Named Acceptance Check, Status Transition Log, and all 4 EVID-05-required sections.

**One unclaimed section found:** `FUT-01 Hand-off Note (formerly "Code Evidence")` — see Finding F-04 below.

All 6 claimed-missing evidence packets confirmed absent from disk. ✅

### 1.4 Framework Spec Surface Spot-Checks

All 15 line-number references in both `pinn_architecture.md` and `ctl_instruction.md` were spot-checked:

| Surface | File | Claimed Line(s) | Found | Drift |
|---------|------|-----------------|-------|-------|
| `update_omega0` listing | pinn_arch | 172 | ✅ | None |
| hidden_omega_0 prose | pinn_arch | 195 | ✅ | None |
| Hyperparameter table omega0 rows | pinn_arch | 269–270 | ✅ | None |
| Architecture summary init table | pinn_arch | 945–947 | ✅ | None |
| LayerNorm skip/power formula | pinn_arch | 214–228 | ✅ | None |
| LayerNorm rationale | pinn_arch | 237–268 | ✅ | None |
| `elementwise_affine=True` default | pinn_arch | 268 | ✅ | None |
| Architecture summary LayerNorm | pinn_arch | 938–941 | ✅ | None |
| Repeated input normalization note | pinn_arch | 773 | ✅ | None |
| I_norm / I_3 surfaces | ctl_inst | 644–768 | ✅ | None |
| Network-facing normalization table | ctl_inst | 1000–1032 | ✅ | None |
| I_3 `∈ [-1, 1]` annotation | ctl_inst | 768 | ✅ | None |
| `E_scale` definition | both | various | ✅ | None |
| `compute_normalized_inertia` | ctl_inst | 736 | ✅ | None |
| `I_norm_raw` occurrences | ctl_inst | 644, 750, 755, 1032 | ✅ | None |

**Zero line-number drift across all 15 spot-checks.**

---

## 2. High-Priority Findings

### F-01: D-06 "Realized Support" Framing Exceeds Source Grounding

**Severity:** HIGH — Grey-area grounding concern

**Description:** Plan 20-04's core framing — "energy and mass normalization ranges are documented as realized dataset support, not correctness failures" — introduces a statistical-learning concept ("realized support of a distribution") that **does not appear in either primary source document**.

**Evidence:**

The issue document says:
- M9: *"Acceptable for SIREN. Document that positive range is unused."* (line 89)
- M10: *"Acceptable — asymmetry carries mass hierarchy information."* (line 90)

The resolution document prescribes the formulas (`tanh(E/E_scale)`, `tanh((m_i - μ)/(σ + 10⁻⁸))`) but says nothing about "realized support," "universal physics bounds," or the three-way distinction (formula-available / dataset-occupied / physics-bounds) that organizes Plan 20-04.

The word **"realized" does not appear anywhere** in either the resolution document or the issue document.

**Impact:** Under CLAUDE.md governance, this is a grey area. The underlying observation (the ranges are empirically what the dataset produces) is grounded. But the **framing language** ("realized support") and the **three-way conceptual distinction** are Phase 20 D-06 policy decisions, not source findings. This is a "framing" invention applied to source material — arguably mechanical/presentation, but close to the "semantic" boundary.

**Recommendation:** Plan 20-04 should explicitly acknowledge that "realized support" is a D-06 framing policy and instruct the executor to validate that the M9/M10 verdicts are consistent with applying this framing before editing. If the M9/M10 source review reveals the sources use a different framing (e.g., "acceptable for engineering reasons"), the executor should record a gap rather than impose the D-06 framing.

### F-02: Wave 2 Concurrent-Edit Risk on pinn_architecture.md

**Severity:** HIGH — Missing dependency in plan graph

**Description:** Plan 20-02 (LayerNorm, wave 2) and Plan 20-04 (energy/mass support, wave 2) both list `pinn_architecture.md` in `files_modified`. Plan 20-04's `depends_on` is `["20-03"]` only — it does not include 20-02.

**Evidence:**
- 20-02 edits `pinn_architecture.md` §2.3, §2.4, and summary table (lines ~214–268, ~938–941)
- 20-04 conditionally edits `pinn_architecture.md` ~line 773 (the repeated input normalization note)
- Both are wave 2 with no enforced ordering between them

**Impact:** If 20-02 and 20-04 execute concurrently (both depend on wave-1 plans, not on each other), they could produce concurrent-edit conflicts on `pinn_architecture.md`. The sections are non-overlapping (~500 lines apart) and 20-04's touch is conditional, so the risk is low-probability but the structural gap exists.

**Recommendation:** Either:
- (a) Add `"20-02"` to 20-04's `depends_on` (conservative safety, harmless if unnecessary), or
- (b) Add an explicit note to 20-04's threat model: "If 20-02 has not completed, do not edit pinn_architecture.md until it has. The conditional support-range check at ~line 773 is independent of the LayerNorm edits but shares the same file."

---

## 3. Medium-Priority Findings

### F-03: Pre-Embedded I₃ Geometry Derivation Risks Pre-Adjudication

**Severity:** MEDIUM

**Description:** Plan 20-03, Task 1, Step 4 embeds a complete first-principles geometry derivation that concludes `I_3 ∈ [0, 1/3]` with the linear map `I_3^{in} = 6·I_3 − 1`. While mathematically correct, presenting the full derivation and conclusion in the plan before execution risks biasing the EVID-05 adjudication.

**Evidence:**
- The plan's threat model (line 80) correctly warns: "Treating the first-principles range check as the verdict | HIGH"
- But Step 4 then provides 12 lines of completed geometric reasoning with the conclusion baked in
- An executor following the plan step-by-step would copy this derivation into the M5 packet and might treat it as having already settled the question

**Impact:** The executor might skip the independent verification step or weight the pre-written derivation too heavily when weighing the two primary sources. The EVID-05 process requires citing and weighing BOTH sources plus the "Which Source Was Correct/Wrong" determination — the derivation alone is not the verdict.

**Recommendation:** Consider presenting the derivation as an outline with verification instructions:

```
Executor: derive the range of I_3 = (d_short + d_mid - d_long) / (d_short + d_mid + d_long)
using the triangle inequality for points in Euclidean space.
Hint: sort distances, find min (collinear) and max (equilateral).
Then derive the linear map f: [I_3_min, I_3_max] → [-1, 1].
Record your derivation and verify it matches or contradicts the cited sources.
```

### F-04: Missing FUT-01 Hand-off Note Handling in Packet Creation

**Severity:** MEDIUM

**Description:** The evidence template contains a `FUT-01 Hand-off Note (formerly "Code Evidence")` section (lines 36–44 of `_TEMPLATE.md`) that **no plan mentions**. This section has v1.4-specific guidance: live `pinn/` code is NOT evidence and the section should be marked accordingly.

**Evidence:**
- Template lines 36–44: the section instructs that live code citations should note the v1.4 directive
- Plans 20-01, 20-02, 20-03, 20-04 all have detailed step-by-step packet creation instructions but none mention this section
- The executor creating packets from the template will encounter an unaddressed section

**Impact:** The executor might:
- Leave it blank (acceptable but undocumented)
- Try to fill it with `pinn/` code evidence (violates v1.4 directive)
- Delete it (loses the v1.4 guidance for future use)

**Recommendation:** Add a step to each packet-creation task: "In the FUT-01 Hand-off Note section, write: `Not applicable — Phase 20 does not edit or cite live pinn/ code per v1.4 directive (2026-05-19).`"

### F-05: Wave 1 Ledger Concurrent-Edit Risk

**Severity:** MEDIUM

**Description:** Plans 20-01 and 20-03 are both wave 1 (no dependencies) and both modify `16-ISSUE-LEDGER.md`. Plan 20-01 updates B-01 and B-10 rows; Plan 20-03 updates M5. Different rows, but the same file.

**Evidence:**
- 20-01 Task 1, Step 7: "change the B-01 and B-10 rows"
- 20-03 Task 1, Step 8: "Advance M5 row"
- Both commit the ledger as part of their Task 1

**Impact:** If executed by parallel subagents, git conflicts on `16-ISSUE-LEDGER.md` are possible. The conflict would be trivially resolvable (different rows), but it could halt automated execution.

**Recommendation:** Add a note to both plans' threat models: "Wave-1 plans 20-01 and 20-03 both modify the ledger. If executing concurrently, sequence the ledger commits or use separate commits to minimize conflict risk."

### F-06: Severity Field Choices Unexplained

**Severity:** MEDIUM

**Description:** Plans assign severity to evidence packets (B-01: MINOR, B-10: MINOR, M5: MAJOR, M8: MINOR, M9: MINOR, M10: MINOR) without explaining the rationale. The severity choices appear reasonable but are undocumented.

**Evidence:**
- M5 is MAJOR because it's contested/EVID-05 — this is clearly correct
- M9 and M10 are MINOR despite being MAJOR in the issue document (lines 89–90: `M9 | MAJOR`, `M10 | MAJOR`)

**Impact:** If an executor encounters a contested M8 (e.g., the issue doc challenges LayerNorm attribution more strongly than expected), the MINOR severity may need to escalate. Without documented rationale, the executor has no guidance for when to change severity.

**Recommendation:** Add a brief note to each packet-creation step: "Severity MINOR reflects the expected non-contested adjudication. If the source review reveals contestation, escalate to MAJOR and consider EVID-05 applicability."

### F-07: Partial-Blocker Handling in Plan 20-04

**Severity:** MEDIUM

**Description:** Plan 20-04 creates two separate evidence packets (M9 for energy, M10 for mass) with separate verdicts but a combined closure audit. The plan does not address what happens if one verdict is `accept-resolution` and the other is `defer-with-blocker`.

**Evidence:**
- Task 2 precondition (line 159): "Apply each edit ONLY per the corresponding recorded verdict (energy → M9, mass → M10). If a verdict is a blocker, STOP that edit and follow its gap."
- This implies partial execution is possible (energy edit proceeds, mass edit stops)
- But Task 3's "combined support-range audit" assumes both edits completed

**Impact:** If M9 proceeds but M10 is blocked, can Task 3's combined audit partially proceed? The plan doesn't say. The executor would need to make this decision ad hoc.

**Recommendation:** Add to Task 3: "If only one of M9/M10 reached VERIFIED, perform a single-packet audit for the completed one and record the other as BLOCKED in the closure proof. AC-ARCH-05 cannot close until both are resolved."

---

## 4. Low-Priority Findings

### F-08: Status Transition Log Format vs. Template Requirements

**Severity:** LOW

**Description:** Plans specify transition text like `<today> <pending-commit> PENDING -> IN_PROGRESS (Phase 20 P01 Task 1)` but the template requires date, commit SHA, status transition, and actor. The plans use `<pending-commit>` as a SHA placeholder, which is reasonable, but the actor field is never mentioned.

**Recommendation:** Add "actor: Phase 20 executor" or similar to the status-log instructions.

### F-09: GAP-17-05 Cross-Reference Path Missing

**Severity:** LOW

**Description:** Plan 20-03 references "GAP-17-05 (RESOLVED-WITH-INSTRUCTION)" to constrain M5 scope but doesn't tell the executor where to find the full resolution text. The resolution is in `.planning/phases/17-input-and-output-contracts/17-GAPS.md` lines 87–128, cross-referenced in `v1.4-GAPS.md` line 26 and `17-CONTEXT.md` line 64.

**Recommendation:** Add the file path and line range to 20-03's `<interfaces>` section: `GAP-17-05 resolution: .planning/phases/17-input-and-output-contracts/17-GAPS.md:87-128`.

### F-10: Wave-2 Line-Drift Warning Incomplete

**Severity:** LOW

**Description:** Plan 20-02's threat model warns about line drift from 20-01 ("Line numbers drifted (and 20-01 already shifted this file)"), which is good. But Plan 20-04's threat model only warns about `ctl_instruction.md` drift from 20-03 — it doesn't warn about `pinn_architecture.md` drift from 20-01 and 20-02.

**Recommendation:** Add to 20-04's threat model: "Line numbers drifted in pinn_architecture.md (20-01 and 20-02 may have shifted this file). Locate surfaces by `rg`, not by quoted line numbers."

### F-11: Negative Audit Regex Coverage

**Severity:** LOW

**Description:** Plan 20-01's negative scheduler audit uses:
```
rg -ni "schedul|exponential decay|final_omega|decay_rate|update_omega0"
```
This covers known scheduler terminology but might miss creative phrasings like "adaptive omega," "frequency warm-up," "omega ramp," or "frequency annealing."

**Recommendation:** Consider broadening to include: `"omega.*adapt|frequency.*warm|omega.*ramp|frequency.*anneal|omega.*curriculum"` or performing a manual read of the full SIREN section as a final check.

---

## 5. Grey Areas for Discussion

### G-01: Is the D-06 "Realized Support" Framing Semantic or Mechanical?

**The question:** Under CLAUDE.md governance, "semantic" decisions must be surfaced and cannot be invented. The D-06 framing introduces:
- A new term ("realized support") not in any source
- A three-way conceptual distinction (formula-available / dataset-occupied / physics-bounds) not made by any source
- A re-interpretation of the sources' "acceptable" verdicts through a statistical-learning lens

**Arguments for "mechanical/presentation":**
- The underlying observations (energy range is one-sided, mass range is asymmetric) are grounded in the sources
- The re-framing doesn't change any formula, numeric value, or technical decision
- It's a documentation tone choice: "this is how the dataset works" vs. "this is a bug"

**Arguments for "semantic":**
- The framing language ("realized support") carries a specific statistical-learning meaning that the sources don't endorse
- Future agents reading the spec will infer that the sources explicitly authorized this framing
- The three-way distinction could influence downstream decisions about what "support" means for new datasets

**Assessment:** This is closer to the semantic boundary than other D-06 decisions. The framing is reasonable and consistent with the sources' intent, but it's an interpretive layer that should be validated by the M9/M10 verdicts before being applied to the spec.

### G-02: Is the I₃ Geometry Derivation "Short and Uncontroversial"?

**The question:** 20-CONTEXT D-04 authorizes a "short first-principles geometry/algebra range check if it is genuinely short and uncontroversial." The plan's derivation is 12 lines involving:
- Sorting three distances
- Applying the triangle inequality
- Optimizing a ratio (N/P) with a monotonicity argument
- Deriving the maximum at the equilateral configuration
- Constructing the affine map f(x) = 6x − 1

**Assessment:** The derivation is correct and uses standard Euclidean geometry. However, the optimization step ("N/P increases as d_long decreases; min d_long = d_mid; then with d_short ≤ d_mid, N/P is maximized at d_short = d_mid = d_long") skips several sub-steps. A non-geometry-specialist executor might struggle to verify the monotonicity claim independently. This is at the boundary of "short and uncontroversial" — the conclusion is uncontroversial, but the intermediate reasoning is not trivially verifiable.

### G-03: Should ARCH-04 Be Explicitly Recommended for Deferral?

**The question:** Plan 20-05 is a blocked placeholder. If GAP-20-01 remains open through Phase 20 execution, ARCH-04 becomes a Phase 21 concern by default. But the plan doesn't explicitly recommend deferral — it just says "BLOCKED."

**Assessment:** Given that ARCH-04 is documentation cleanup (naming convention, not a physics or architecture decision), and the source material already exists for a straightforward resolution once the evidence vehicle is authorized, explicit deferral to Phase 21 might be cleaner than leaving an indefinite block. This is a strategic question for the user.

---

## 6. Structural Observations

### 6.1 Strengths

The plans exhibit exceptional quality in several areas:

1. **Evidence-first workflow consistency:** Every executable plan follows the same rigorous pattern: create packet → cite sources → record verdict → edit per verdict → positive audit → negative audit → close. This consistency makes the plans easy to execute mechanically.

2. **STOP protocol deployment:** STOP conditions are placed at exactly the right points — after source citation but before any spec edit. No plan allows editing before a recorded verdict.

3. **Threat model quality:** Each plan has a specific, actionable threat model that addresses real risks (pre-deciding verdicts, line-number drift, live-code citation, orphaned scheduler prose). The mitigations are concrete and verifiable.

4. **Cross-phase reference handling:** GAP-17-05 is correctly cited and its resolution is faithfully reflected. The plan doesn't re-litigate the Phase 17 decision.

5. **ARCH-04 discipline:** The blocked placeholder (20-05) is exactly the right response to GAP-20-01 — visible, grounded, with a clear unblock procedure, and no invented process structure.

6. **Negative audit patterns:** The regex-based negative audits are well-designed, targeting specific language patterns that should have been removed. The combination of positive + negative audits provides strong closure proof.

7. **GAP-20-01 registration:** The gap is properly registered with all required fields (decision point, artifact location, task context, classification, source silence citations, math/engineering grounding, temptation record, user options, confidence of impact, and status).

### 6.2 Missing Structural Elements

1. **No Phase 20 exit checklist:** The plans close individual ARCH requirements but don't aggregate into an overall "Phase 20 exit criteria" document. After all plans execute, someone needs to verify: ARCH-01 ✅, ARCH-02 ✅, ARCH-03 ✅, ARCH-05 ✅, ARCH-04 blocked/deferred — and update STATE.md accordingly.

2. **No STATE.md update task:** None of the plans include a final task to update `.planning/STATE.md` to reflect Phase 20 completion. This should be added as a post-execution step.

3. **No rollback plan:** If a plan starts executing (creates packets, records verdicts) and then discovers a STOP condition mid-way, the plan doesn't describe how to handle the partially-created packet. The STOP conditions say "record a gap and halt Task 2," but the packet from Task 1 with a non-`accept-resolution` verdict is still committed to git.

---

## 7. Recommendations Summary

| # | Finding | Priority | Action |
|---|---------|----------|--------|
| R-01 | F-01: D-06 framing exceeds source | HIGH | Add executor instruction to validate framing against M9/M10 verdicts |
| R-02 | F-02: Wave 2 pinn_architecture.md concurrency | HIGH | Add `"20-02"` to 20-04's `depends_on` or add explicit sequencing note |
| R-03 | F-03: Pre-embedded I₃ derivation | MEDIUM | Soften to outline with "executor: verify and complete" guidance |
| R-04 | F-04: FUT-01 Hand-off Note gap | MEDIUM | Add handling step to all packet-creation tasks |
| R-05 | F-05: Wave 1 ledger concurrency | MEDIUM | Add threat model note about sequencing ledger commits |
| R-06 | F-06: Severity choices unexplained | MEDIUM | Add rationale note with escalation guidance |
| R-07 | F-07: Partial-blocker handling | MEDIUM | Add partial-audit instructions to 20-04 Task 3 |
| R-08 | F-08: Status-log format | LOW | Add actor field to transition text |
| R-09 | F-09: GAP-17-05 path | LOW | Add file path and line range to 20-03 interfaces |
| R-10 | F-10: Wave-2 drift warning | LOW | Add pinn_architecture.md drift warning to 20-04 |
| R-11 | F-11: Negative audit regex | LOW | Broaden scheduler detection patterns |
| R-12 | Phase 20 exit checklist | MEDIUM | Create post-execution aggregation task |
| R-13 | STATE.md update | LOW | Add post-execution STATE.md update step |

---

## 8. Conclusion

The Phase 20 planning artifacts represent a high-water mark for evidence-gated, governance-compliant planning. The source-of-truth verification is clean across all tested dimensions. The STOP protocol and evidence workflow are correctly applied. The dependency graph is mostly correct with one latent concurrency risk.

The most important finding (F-01) is a grey-area grounding concern about the D-06 "realized support" framing — the framing is reasonable and consistent with the sources' intent, but it introduces terminology and conceptual structure not explicitly present in the source documents. This should be flagged to the user as a framing-policy decision that the M9/M10 verdicts should validate before application.

The second most important finding (F-02) is a missing `depends_on` link between Plans 20-04 and 20-02, both of which touch `pinn_architecture.md` in wave 2.

Neither finding is a blocker. Both are addressable with small plan amendments before execution begins.

**Overall recommendation: Plans are ready for execution after addressing R-01 and R-02.**

---

*Review conducted 2026-06-03. Four parallel verification subagents checked 40+ individual claims against source documents. All findings are documented with evidence and actionable recommendations.*
