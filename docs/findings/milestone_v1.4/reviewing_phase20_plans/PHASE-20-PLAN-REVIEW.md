# Phase 20 Plan Review — Adversarial Multi-Dimensional Assessment

**Date:** 2026-06-03
**Reviewer:** Claude Code (5 parallel adversarial agents)
**Artifacts reviewed:** 9 files in `.planning/phases/20-architecture-and-normalization-cleanup/`
**Method:** Internal consistency, governance/grounding, source-anchor verification, execution feasibility, scope/cross-phase

---

## Executive Summary

Phase 20 plans are **structurally sound** — the evidence-first workflow, verdict-gating, wave ordering, and STOP-protocol compliance are correctly implemented across all five plans. However, the review identified **one critical gap** (the M5/I₃ adjudication faces a three-way definition conflict the plans describe as two-way), **one critical label collision** (D-02 used for two unrelated concepts), and several HIGH findings that should be addressed before execution.

**Verdict: Plans are executable with noted caveats. The two CRITICAL findings should be resolved or acknowledged before execution begins.**

---

## Findings Summary

| Severity | Count | Key Themes |
|----------|-------|------------|
| CRITICAL | 2 | I₃ three-way definition conflict; D-02 label collision |
| HIGH | 6 | Biased "expected verdict" language; implicit phase exit for ARCH-04; audit false positives; concurrent-edit risk |
| MEDIUM | 9 | Commit message assumptions; approximate line ranges; judgment-based audits; incomplete first-principles scope |
| LOW | 5 | Non-standard plan type; commit-message parseability; packet-state table cosmetics |
| PASS | 10+ | Evidence gating, live-code firewall, GAP-20-01 adequacy, verdict enum, EVID-05 sections, ledger reservations, wave/dep structure, requirements mapping |

---

## CRITICAL Findings

### C-01: I₃ Conflict Is Three-Way, Not Two-Way

**Where:** `20-CONTEXT.md` D-04 (line 53); `20-03-PLAN.md` Task 1 Steps 4–6; `20-RESEARCH.md` ARCH-03 section

**What:** The plans describe the M5/I₃ conflict as two-way (resolution doc vs issue doc). It is actually **three-way**:

| Source | I₃ Definition | Claimed Range | Normalization Map |
|--------|---------------|---------------|-------------------|
| Resolution doc (`ctl_pinn_resolution.md:608,614`) | `(d_short + d_mid - d_long) / (d_short + d_mid + d_long)` — dimensionless ratio | [0, 1/3] | `6·I₃ - 1` |
| Issue doc (`01-architecture-and-physics-foundations.md:87,536`) | `I₃ = sorted([r₀₁, r₁₂, r₂₀])` — raw mutual distance (I₃ = d_long) | [0, 1] | `2·(I₃/I_max) - 1` |
| Current spec (`ctl_instruction.md:768`) | Uses the ratio formula but annotates it | ∈ [-1, 1] (no mapping needed) | None stated |

**Why this matters:** The first-principles geometry check in 20-03 Step 4 only derives the range for the resolution doc's ratio formula ([0, 1/3]). It does not address the issue doc's definition (raw distance, range depends on physical scale). If the sources disagree on the **definition** of I₃ — not just the range annotation — the Root-Cause Framework Ambiguity (Step 5) will mischaracterize the conflict as "annotation confusion" rather than "definition conflict."

**Impact:** An executor who follows the plan mechanically will derive [0, 1/3] for the ratio formula, record `accept-resolution`, edit the spec, and never surface that the issue doc defines I₃ as a fundamentally different quantity. The M5 EVID-05 adjudication would be incomplete.

**Recommendation:** Add an explicit definition-comparison step between current Steps 3 and 4 of 20-03 Task 1:
> "Compare the issue doc's I₃ formula against the resolution doc's I₃ formula. If they define I₃ as different quantities, this is a definition conflict, not a range-annotation conflict. Record this distinction in Root-Cause Framework Ambiguity and factor it into the verdict."

**Confidence:** HIGH — verified by reading both source documents at the cited lines.

---

### C-02: D-02 Label Collision

**Where:** `20-CONTEXT.md` line 22 vs line 71; propagates to `20-GAPS.md`, `20-RESEARCH.md`, `20-05-PLAN.md`

**What:** The label `D-02` is used for two completely different concepts within the same Phase 20 document set:

1. **20-CONTEXT.md line 22:** D-02 = the SIREN/omega0 contract decision (ARCH-01, AC-ARCH-01) — fixed omega0, no scheduler.
2. **20-CONTEXT.md line 71:** D-02 = the issue-doc finding about I_norm raw-vs-tanh naming (ARCH-04).

**Why this matters:** A reader implementing 20-01-PLAN could misinterpret "D-02" as the I_norm finding. An executor of 20-05-PLAN could misinterpret "D-02" as the SIREN contract. The context usually disambiguates (20-01 surrounds D-02 with SIREN language; 20-05 surrounds it with I_norm language), but the shared identifier across the same document set creates a genuine ambiguity risk, especially for subagents or automated tooling.

**Recommendation:** Rename one of them. Simplest fix: rename the issue-doc `D-02` references to `Issue-D-02` or `D-02-I_norm` everywhere except where quoting the issue doc's own heading verbatim. Specifically update: `20-CONTEXT.md`, `20-GAPS.md`, `20-RESEARCH.md`, `20-05-PLAN.md`.

**Confidence:** HIGH — verified by reading both usages in context.

---

## HIGH Findings

### H-01: "Expected Verdict" Language Pre-Supposes Outcomes

**Where:** `20-RESEARCH.md:209`; `20-CONTEXT.md:85,39`

**What:** Multiple instances of "confirm the expected verdict" and "assuming M8 confirms the source-backed verdict" language pre-suppose the verdict before evidence packets are created. The governance rule requires verdicts be grounded after evidence review, not assumed before it.

**Affected findings:** M8 (LayerNorm), M9 (energy), M10 (mass) — all uncontested findings where the sources likely agree.

**Recommendation:** Replace "If M9/M10 confirm the expected verdict" with "After M9/M10 record their verdicts, if the verdict confirms the source-backed position..." Replace "assuming M8 confirms" with "if M8 confirms."

---

### H-02: Phase 20 Exit Criterion for Blocked ARCH-04 Is Implicit

**Where:** `ROADMAP.md:206-215`; `20-05-PLAN.md:71`

**What:** ROADMAP.md lists ARCH-04 as a Phase 20 requirement and success criterion 4 as a pass condition. Plan 20-05 asserts "Phase exit must account for ARCH-04 as blocked/deferred, not silently complete." But the ROADMAP itself does not state what happens when Phase 20 exits with ARCH-04 still blocked. This is a plan-level assertion, not a ROADMAP-level exit gate.

**Why this matters:** Phase 21 (VER-05) requires all in-scope findings to be VERIFIED or explicitly DEFERRED with a written blocker. Without a ROADMAP-level statement, the Phase 20→21 transition relies on the plan's self-declared exit rule.

**Recommendation:** Add a note to ROADMAP.md Phase 20 section: "Phase 20 may complete when ARCH-01/02/03/05 are closed and ARCH-04 is either closed or explicitly DEFERRED with a recorded blocker (GAP-20-01) in the gap register."

---

### H-03: Negative Scheduler Audit Returns False Positives

**Where:** `20-01-PLAN.md` Task 3 Step 2

**What:** The audit pattern `rg -ni "schedul|..."` will match unrelated scheduling language in `pinn_architecture.md` at lines ~365 (conservation-term scheduling), ~656, and ~669 (warmup scheduling). The plan says "zero active/normative matches" but the broad pattern returns 3-4 non-omega0 hits. The executor must manually filter.

**Recommendation:** Either narrow the pattern to `omega0.*schedul|schedul.*omega0` or add an expected-hits note: "Expected: 3-4 hits from unrelated scheduling language; verify none relate to omega0."

---

### H-04: 20-04-PLAN Concurrent-Edit Risk With 20-02

**Where:** `20-04-PLAN.md` frontmatter `depends_on`; Task 2 Step 3

**What:** 20-04 conditionally edits `pinn_architecture.md` (normalization note at ~line 773) and declares dependency only on 20-03. But 20-02 also edits `pinn_architecture.md` in wave 2. Both 20-02 and 20-04 run in wave 2 with no dependency between them. The edit regions are disjoint (20-02 targets §2.3/2.4 LayerNorm; 20-04 targets §5.2 normalization note), so a semantic conflict is unlikely, but the concurrent-file-modification risk is not surfaced in 20-04's threat model.

**Recommendation:** Add a threat-model entry or dependency note in 20-04 acknowledging concurrent `pinn_architecture.md` editing with 20-02 and confirming the edit regions do not overlap.

---

### H-05: RESEARCH Source Anchor `:126` Is Summary, Not Authoritative Directive

**Where:** `20-RESEARCH.md:55`

**What:** The resolution doc line 126 is the consolidation-table summary row ("remove scheduler and author doubts"), while line 685 is the actual authoritative directive ("Remove all epochwise or optimizer-step omega0 scheduling"). The RESEARCH groups them as equivalent anchors.

**Recommendation:** Separate the `:126` citation with a note that it is the consolidation-table summary, while `:685` and `:1227-1234` are the authoritative directive text.

---

### H-06: README.md Line-Number Anchors May Have Drifted

**Where:** `20-04-PLAN.md` Task 1 `read_first` block; `20-RESEARCH.md:202`

**What:** Specific line ranges in `simulation_data/Documentation/README.md` (~245, ~317-324, ~423-443) are cited. If the README has been edited since research, these anchors are stale. The plan does mention using `rg` search, but the `read_first` block lists line numbers as the primary instruction without a fallback.

**Recommendation:** Add a fallback note: "If line-number anchors do not match, re-locate by searching README.md for `unit mass`, `total mass`, `hierarchical`, `prescreening`, or `energy error`."

---

## MEDIUM Findings

### M-01: 20-03 Step 7 Convention Example Only for `accept-resolution`

**Where:** `20-03-PLAN.md` Task 1 Step 7

The Locked Convention example provides filled-in text only for `accept-resolution`. The other four verdicts have no convention example. This creates asymmetry that biases the executor toward one outcome. Recommendation: Either provide examples for all five verdicts or provide none.

### M-02: 20-03 Commit Message Hardcodes `accept-resolution` Wording

**Where:** `20-03-PLAN.md` Task 2 Step 4

The commit message `"spec(20): I_3 raw range [0,1/3] + staging map 6*I_3-1; metadata-only (ARCH-03)"` assumes `accept-resolution`. If the verdict is different, the message is inaccurate. Recommendation: Use a generic message like `"spec(20): align I_3 range/mapping to M5 verdict (ARCH-03)"`.

### M-03: LayerNorm Surface Range Citation Discrepancy

**Where:** `20-RESEARCH.md:107` vs `20-CONTEXT.md:143`

RESEARCH cites `pinn_architecture.md:237-256` for LayerNorm rationale. CONTEXT cites `:237-268`. The narrower range in RESEARCH misses line 268 which contains the `elementwise_affine=True` default — a critical audit surface. Recommendation: Align both to the wider range `:237-268`.

### M-04: First-Principles Derivation Only Covers Resolution-Doc Formula

**Where:** `20-03-PLAN.md` Task 1 Step 4

The derivation proves `I₃ ∈ [0, 1/3]` for the resolution doc's ratio formula. It does not separately derive the range for the issue doc's raw-distance formula (which would be scale-dependent, hence [0, ∞) or [0, d_max]). The EVID-05 "Which Source Was Correct/Wrong" section requires addressing both. See C-01.

### M-05: 20-01 Task 2 Verify Pattern Has Dead Sub-Pattern

**Where:** `20-01-PLAN.md` Task 2 verify block

The pattern `"dynamically schedule"` matches nothing in the file. The actual text is `"schedule the initial frequency parameter"`. The broader pattern covers this via other terms (`update_omega0`, `exponential decay`), so the overall verification still works. Cosmetic.

### M-06: 20-04 Negative Audit Regex May Miss Failure-Framing Variants

**Where:** `20-04-PLAN.md` Task 3 Step 2

The regex `normalization (bug|error|failure)` requires exact word order. Variants like "bug in normalization" would not match. Consider broadening to bidirectional patterns.

### M-07: 20-01 Cross-Reference Regression Check Is Loose

**Where:** `20-01-PLAN.md` Task 3 Step 3

`rg -n "Network Input Contract|14-dimensional|SQR-SkipResNet"` returns ~10+ hits. This confirms strings exist, not that they are unchanged. A `git diff` on specific lines would be more precise.

### M-08: 20-02 Task 2 Step 3 Contains Conditional Gap-Recording in Autonomous Plan

**Where:** `20-02-PLAN.md` Task 2 Step 3

Step 3 says "Keep `Applied only to odd layers` only if the cited sources support... otherwise record a gap." This conditional gap-recording in an `autonomous: true` plan is an edge case. The threat model warns about it, and the resolution doc does support the scope, so this is unlikely to trigger.

### M-09: RESEARCH `ctl_instruction.md:644-768` Lumps ARCH-03 and ARCH-04 Surfaces

**Where:** `20-RESEARCH.md`; `20-CONTEXT.md:144`

The range lumps I_norm surfaces (ARCH-04) and I₃ surfaces (ARCH-03) without distinguishing which lines belong to which requirement. Recommendation: Split into ARCH-03-specific (`:758-768`) and ARCH-04-specific (`:644, :667, :736-755`) line references.

---

## LOW Findings

### L-01: 20-05 Uses Non-Standard Plan Type
`type: blocked-placeholder` is not one of the standard GSD plan types. Reasonable extension but could confuse tooling expecting only `type: execute`.

### L-02: Wave 1 Parallel Execution Could Cause Ledger Race Conditions
Plans 20-01 and 20-03 both modify `16-ISSUE-LEDGER.md` and run in wave 1 with no dependency. If executed by separate concurrent agents, this creates a merge conflict risk. Low severity because the expected workflow is sequential execution by a single agent, and the plans edit different ledger rows.

### L-03: RESEARCH Packet-State Table Combines Two Hypothetical Filenames
`evidence/D-02.md / evidence/ARCH-04.md` in one table cell. Could be read as two missing packets. Surrounded by clear "do not create" instructions, so cosmetic only.

### L-04: 20-04 Task 3 Step 2 Negative Audit Self-Matches Inserted Prose
The inserted realized-support prose includes "not a normalization correctness failure" which contains the exact phrase `"correctness failure"` searched for in the negative audit. This is intentional (the sentence uses the term to disclaim it) but could confuse an executor seeing the self-match.

### L-05: CONTEXT Line-Number References Are Approximate
Several cited ranges (`:214-228`, `:269-270`) are slightly off from the actual content boundaries. The plans correctly instruct using `rg` rather than line numbers, so this is orientation-only.

---

## Verified as Correct (PASS Items)

These items were verified and found correct:

1. **Evidence gating:** All plans correctly gate spec edits on recorded verdicts. No plan can edit before evidence.
2. **Live code firewall:** No plan treats `pinn/` code as evidence. Consistently enforced across all documents.
3. **GAP-20-01 adequacy:** All required STOP-protocol fields present. Classification (`process-artifact schema`) is correct.
4. **Verdict enum completeness:** All 5 verdict options listed; `defer-with-blocker` path complete with STOP instructions.
5. **EVID-05 required sections:** 20-03 Task 1 mandates all required sections from the evidence template.
6. **Ledger reservations:** B-01, B-10, M5, M8, M9, M10 all verified as reserved for Phase 20 at the cited ledger lines.
7. **No D-02/ARCH-04 ledger row:** Confirmed absent, validating GAP-20-01's claim.
8. **Wave/dependency structure:** Wave 1 (20-01, 20-03) edits different files; wave 2 (20-02→20-01, 20-04→20-03) correctly serializes shared-file edits. No circular dependencies.
9. **Requirements mapping:** Each plan maps to exactly the correct ARCH requirement.
10. **`autonomous: false` on 20-03:** Correct for a contested EVID-05 adjudication. All others correctly `autonomous: true`.
11. **Source anchor accuracy:** 23 of 27 checked source anchors verified at cited locations. 2 minor drifts, 1 substantively correct but mischaracterized conflict (see C-01).
12. **Phase 20.5 isolation:** No Phase 20 plan touches `sampling_method.md` or Phase 20.5 artifacts.
13. **I₃ geometry derivation math:** The derivation of I₃ ∈ [0, 1/3] is mathematically correct. The linear map `f(x) = 6x - 1` correctly sends [0, 1/3] → [-1, 1].
14. **Scope alignment:** No scope creep detected. All 5 success criteria have assigned plans. All deferred items are appropriate deferrals.

---

## Grey Areas Requiring User Attention

### GA-01: What Is the Right Verdict When Sources Define I₃ Differently?

The M5 EVID-05 adjudication must handle a definition conflict, not just a range-annotation conflict. If the sources genuinely use "I₃" for different quantities, the verdict options become:
- `accept-resolution` = adopt the dimensionless ratio formula
- `accept-issue-doc` = adopt the raw-distance formula (with scale-dependent range)
- `accept-third-position` = acknowledge both definitions exist and pick one
- `reject-both-as-unsupported` = neither source's definition is canonical
- `defer-with-blocker` = surface to user

The current plan biases toward `accept-resolution` via the geometry check. The user should decide whether the plan should explicitly instruct the executor to compare definitions before deriving ranges.

### GA-02: Phase 20 Exit Semantics With ARCH-04 Blocked

If GAP-20-01 remains OPEN at Phase 20 exit, what happens? Options:
- (a) Phase 20 cannot exit until ARCH-04 is resolved or deferred with user instruction
- (b) Phase 20 may exit with ARCH-04 explicitly marked DEFERRED, and the ROADMAP records this
- (c) ARCH-04 is carved out to Phase 21 or a later phase

The plan (20-05 line 71) asserts option (a/b) but the ROADMAP does not confirm this. The user should decide and record the exit gate.

### GA-03: Should 20-03 Task 2 Edit Instructions Be Verdict-Neutral?

Currently Task 2 provides concrete edit text for `accept-resolution` only, with a note to "derive from Locked Convention" for other verdicts. Should all five verdicts have pre-written edit instructions? This trades plan length for execution safety. Given that 20-03 is `autonomous: false` and the geometry derivation supports one outcome, the current approach is defensible — but the user should be aware of the bias.

---

## Recommendations Summary

### Before Execution (Critical)

1. **Resolve C-01:** Add a definition-comparison step to 20-03 Task 1 between Steps 3 and 4. Update D-04 and the Root-Cause Framework Ambiguity instructions to acknowledge the three-way conflict.
2. **Resolve C-02:** Rename one of the two `D-02` labels to eliminate the collision.

### Before Execution (Recommended)

3. **H-01:** Replace "expected verdict" language with neutral conditional framing in CONTEXT and RESEARCH.
4. **H-02:** Add explicit Phase 20 exit gate to ROADMAP.md for blocked ARCH-04.
5. **H-03:** Add expected-hits note to 20-01 Task 3 Step 2 scheduler audit.
6. **H-04:** Add concurrent-edit note to 20-04 threat model or dependency list.
7. **M-01/M-02:** Either generalize 20-03 Step 7/Task 2 for all verdicts or add explicit acknowledgment of bias.

### During Execution (Advisory)

8. **M-03:** Use the wider LayerNorm range (237-268) from CONTEXT rather than the narrower RESEARCH range.
9. **H-06:** Re-locate README anchors by content search if line numbers don't match.
10. **M-06/M-07:** Consider broadening audit regexes for more robust negative checks.

---

## Review Method

Five parallel adversarial agents reviewed the Phase 20 artifacts:

| Agent | Dimension | Files Read | Tool Calls |
|-------|-----------|------------|------------|
| Coherence Reviewer | Internal consistency | 8 Phase 20 files | 59 |
| Feasibility Reviewer | Governance + grounding | 12 files | 23 |
| Correctness Reviewer | Source anchor verification | 6 source files + Phase 20 | 28 |
| Pattern Recognition | Execution feasibility | 7 Phase 20 files | 59 |
| Scope Guardian | Scope + cross-phase | 7 Phase 20 files + ROADMAP/REQ | 21 |

**Total source anchors verified:** 27 (23 VERIFIED, 2 DRIFTED, 1 CONTRADICTED, 1 VERIFIED-with-caveat)
**Total findings:** 22 (2 CRITICAL, 6 HIGH, 9 MEDIUM, 5 LOW)
