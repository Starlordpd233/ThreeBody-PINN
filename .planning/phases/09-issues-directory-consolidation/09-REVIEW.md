---
phase: 09-issues-directory-consolidation
reviewed: 2026-04-27T16:43:27Z
depth: standard
files_reviewed: 5
files_reviewed_list:
  - pinn_instruction/original_latex/review-of-framework/issues/01-architecture-and-physics-foundations.md
  - pinn_instruction/original_latex/review-of-framework/issues/02-data-pipeline-and-validation.md
  - pinn_instruction/original_latex/review-of-framework/issues/03-curriculum-and-training-loop.md
  - pinn_instruction/original_latex/review-of-framework/issues/MIGRATION.md
  - pinn_instruction/original_latex/review-of-framework/issues/README.md
findings:
  critical: 2
  warning: 7
  info: 6
  total: 15
status: issues_found
---

# Phase 9: Code Review Report

**Reviewed:** 2026-04-27T16:43:27Z
**Depth:** standard
**Files Reviewed:** 5
**Status:** issues_found

## Summary

The 5 consolidated documentation files were reviewed at standard depth, with cross-reference verification against the 7 archived originals and qualification-check confirmation against `09-VALIDATION.md`. The consolidation achieves most of its goals: the 3 thematic docs total 96.3 KB (within the 87-121 KB target), all 5 expected `[DECISION-NEEDED]` callouts are present (2 in 01, 1 in 02, 2 in 03), both live conflicts have "Considered Alternatives" subsections, MIGRATION.md covers all major section headings, the README is 32 lines (well under the 55-line cap), and no >5-line duplicate paragraphs exist across docs.

However, the review surfaced two BLOCKER findings and several internal-consistency issues that materially weaken the deliverable:

1. **Direct contradiction within `01-architecture-and-physics-foundations.md` between the synthesized normalization table (Option B: shape invariants + direction cosines) and the verbatim audit Section 5 (Option A: trigonometric encoding).** The doc explicitly tells downstream consumers to "quote directly" the verbatim section, while simultaneously recommending the opposite resolution. A reader implementing this will get incompatible instructions depending on which section they trust.

2. **Broken canonical cross-links in `01-architecture-and-physics-foundations.md` and `03-curriculum-and-training-loop.md`** — 4 references use `markdown_conversions/` (with 's') and omit the `pandoc_conversion/` subdirectory. The actual path is `markdown_conversion/pandoc_conversion/`. README.md uses the correct path; the thematic docs do not. (Note: the project's own `CLAUDE.md` propagates the same wrong path, but the README correction proves the executor knew the right path.)

The remaining concerns are duplicate finding-IDs across docs with diverging severity (M4: MAJOR in 01 vs MINOR in 03; M16 duplicated between 02 and 03), executive-summary blocker counts that don't match the tables they introduce, and a stale `B-04/B-05` row label whose ID assignment contradicts the audit's actual B-numbering.

The qualification-check carryover from `09-REVIEWS.md` (Plan 01 `must_haves.artifacts` claiming `03-curriculum-and-training-loop.md`) appears to have been fixed since the review was filed — the current `09-01-PLAN.md` artifact list at lines 28-37 lists only `01-...` and `02-...`. Confirmed RESOLVED.

## Critical Issues

### CR-01: Internal contradiction on input-vector composition in `01-architecture-and-physics-foundations.md`

**File:** `pinn_instruction/original_latex/review-of-framework/issues/01-architecture-and-physics-foundations.md:121-132, 169-204, 309-389`
**Issue:** The doc presents two mutually exclusive 14-D input-vector specifications and instructs the reader to use both:

- **Synthesized normalization formulas table (lines 121-132)** — uses Option B: `m(3) + E + L + Q + s_min + I_norm + I_1,I_2,I_3 (shape invariants) + cos(θ),sin(θ) (direction cosines)` = 13D IC + t' = 14D.
- **Open Decisions callout (lines 169-204)** — recommends adopting Option B and explicitly classifies Option A under "Considered Alternatives."
- **Verbatim Reference Specification (lines 309-389)** — uses Option A: `m(3) + E + L + Q + s_min + I_norm + trig_vec(5)` = 13D IC + t' = 14D. Section 5.5 (line 385-388) explicitly says "I_1, I_2, I_3 (shape invariants): Replaced by trig_vec which encodes orientation."
- **Header text at line 311** declares the verbatim section "the authoritative 14-D input vector specification that downstream implementation phases should quote directly."

A downstream phase quoting the "authoritative" verbatim spec implements Option A (trig encoding); a phase reading the synthesized resolution implements Option B. The same document tells them to do incompatible things.

**Fix:** Pick one of the following:
1. **Drop Section 5 verbatim** and replace it with a synthesized "Final Input Vector Specification" that matches the resolved Option B (shape invariants + direction cosines). Note in MIGRATION.md that audit §5 was synthesized rather than copied verbatim because the audit's Option A was rejected.
2. **Keep verbatim Section 5** but explicitly mark it as "Historical / Audit Reference — superseded by Option B above" and remove the line claiming it is authoritative. Add a banner at line 309 telling implementers NOT to use this section as-is.

The current state is not safely usable for implementation phases.

---

### CR-02: Broken canonical cross-links in `01-` and `03-`

**File:** `pinn_instruction/original_latex/review-of-framework/issues/01-architecture-and-physics-foundations.md:288-289`, `pinn_instruction/original_latex/review-of-framework/issues/03-curriculum-and-training-loop.md:494`
**Issue:** Four canonical-reference links resolve to non-existent paths:

```
01-...md:288: ../../../markdown_conversions/PINN_architecture_plan.md   [BROKEN]
01-...md:289: ../../../markdown_conversions/CTL-instruction-final.md    [BROKEN]
03-...md:494: ../../../markdown_conversions/CTL-instruction-final.md    [BROKEN]
```

Two failures combined:
1. Wrong directory name: `markdown_conversions` (with trailing `s`) — the actual directory is `markdown_conversion` (singular).
2. Missing subdirectory: the canonical Markdown copies live in `pandoc_conversion/`, not directly under `markdown_conversion/`.

`README.md:17-18` and `03-...md:495` use the correct path `../../../markdown_conversion/pandoc_conversion/...`, proving the executor knew the right location for at least some references. The same doc (03-) uses the correct path on one line and the broken path on the very next line.

**Fix:** In `01-...md` and `03-...md`, replace:
```
../../../markdown_conversions/CTL-instruction-final.md
../../../markdown_conversions/PINN_architecture_plan.md
```
with:
```
../../../markdown_conversion/pandoc_conversion/CTL-instruction-final.md
../../../markdown_conversion/pandoc_conversion/PINN_architecture_plan.md
```

Note: the project-level `CLAUDE.md` Section 2.1 also uses the wrong path; consider correcting it in a follow-up commit.

---

## Warnings

### WR-01: `B-04/B-05` row in 01 misuses audit finding-IDs

**File:** `pinn_instruction/original_latex/review-of-framework/issues/01-architecture-and-physics-foundations.md:22-23`
**Issue:** Line 22 labels the input-vector composition row as `B-04/B-05`, then line 23 uses the same `B-05` label for the COM-frame-violation row. The audit at `archive/three_body_pinn_pre-implementation_audit_2026-04-27.md:70-86` defines:
- B-04 = Trigonometric Angle Encodings — Missing from CTL Entirely
- B-05 = COM Frame Violation in Hierarchical ICs

So input-vector composition is exclusively `B-04`, and `B-05` is exclusively COM frame. The "/B-05" suffix on line 22 is wrong; it duplicates the B-05 label and conflates two unrelated audit findings into a single row.

**Fix:** Change line 22 row label from `B-04/B-05` to just `B-04`. (Optionally also reference `B-03` since input-vector dimensionality is part of B-03, but do not double-list B-05.)

### WR-02: Severity drift for finding M4 between 01 and 03

**File:** `pinn_instruction/original_latex/review-of-framework/issues/01-architecture-and-physics-foundations.md:34`, `pinn_instruction/original_latex/review-of-framework/issues/03-curriculum-and-training-loop.md:38`
**Issue:** The constraint-counting error (M4) is documented in both `01-...md:34` (severity MAJOR) and `03-...md:38` (severity MINOR). The audit lists it as MAJOR. CTL ownership-model from `09-RESEARCH.md` Appendix maps M4 to `01-` (not 03-). Having the same finding ID at two different severities in two docs creates an ambiguous source of truth.

**Fix:** Pick one canonical home (recommend 01 since it is architecture/physics foundations) and remove the duplicate from the other doc. If 03 needs to reference M4 for context, use a one-line cross-link instead of a separate table row.

### WR-03: Severity-classification mismatch — M11/M12 elevated to BLOCKING in 02

**File:** `pinn_instruction/original_latex/review-of-framework/issues/02-data-pipeline-and-validation.md:31-32`
**Issue:** Audit lines 158-159 classify M11 (blacklist not loaded) and M12 (32-pts-per-trajectory infeasibility) as MAJOR. `02-...md:31-32` re-classifies them as `**BLOCKING**` and places them in the BLOCKING table. This may be a deliberate editorial elevation, but no rationale is documented and the `M`-prefix ID is from the audit's MAJOR series. A reader cross-referencing the audit will see a severity inconsistency.

**Fix:** Either (a) explain the elevation inline ("Re-classified as BLOCKING for this consolidation because the DataLoader cannot ship without these fixes"), or (b) keep them as MAJOR in the MAJOR table. Same applies to `M13` at `02-...md:33` which is labeled `MAJOR` but placed inside the BLOCKING table.

### WR-04: Executive-summary blocker count in 01 doesn't match the table

**File:** `pinn_instruction/original_latex/review-of-framework/issues/01-architecture-and-physics-foundations.md:9`
**Issue:** Line 9 says "Three blocking issues must be resolved before coding begins... Seven additional critical blockers are documented below," implying 3 + 7 = 10 BLOCKING items total. The actual BLOCKING table has 7 rows (B-01, B-02, B-03, B-04/B-05, B-05, B-09, B-10). The 3 top items cited in the summary are already among those 7 — there are NOT 7 additional items beyond them. The wording "seven additional" is off by 3.

**Fix:** Replace "Seven additional critical blockers are documented below" with "Four additional critical blockers (totaling seven blockers documented below)." Or list a clean count: "Seven blockers documented in the table below; the three highest-priority are summarized above."

### WR-05: Executive-summary in 03 misclassifies a DECISION-NEEDED as a BLOCKING

**File:** `pinn_instruction/original_latex/review-of-framework/issues/03-curriculum-and-training-loop.md:9`
**Issue:** Line 9 says "Three critical blockers must be resolved before implementation: batch construction is unimplemented, data-fidelity and collocation points are conflated, and the causal training methodology remains unresolved (per-time-step causal weighting vs. global ALM)." But the third item (causal training) is documented as `[DECISION-NEEDED]` in Open Decisions (line 368), not as a BLOCKING in the Confirmed Findings table. The actual BLOCKING table has 3 entries: B-07, B-08, and an unnamed "No replay = catastrophic forgetting" row — none of which is the causal training mode.

**Fix:** Either move the causal-training decision into the BLOCKING table (and remove or downgrade the [DECISION-NEEDED] callout), or rephrase the summary to "Two critical blockers (B-07 batch construction; B-08 data-fidelity/collocation conflation) plus one unresolved architectural decision (causal training mode) must be addressed before implementation."

### WR-06: Internal-inconsistency between resolved I_norm decision and verbatim spec

**File:** `pinn_instruction/original_latex/review-of-framework/issues/01-architecture-and-physics-foundations.md:129-130, 193-204, 335`
**Issue:** The synthesized table at line 129 says I_norm is "**See Open Decision below**" and the [DECISION-NEEDED] callout (lines 193-204) says the question is "still unresolved." However, the verbatim Section 5.2 at line 335 already adopts the `tanh(I_trace / (M_tot * r_char^2))` form — the resolution recommended by the [DECISION-NEEDED] callout. The decision is effectively "already taken" in the same document, contradicting the framing that it is open.

**Fix:** Either (a) remove the I_norm [DECISION-NEEDED] callout and document it as resolved (the verbatim section already shows the answer), or (b) update the verbatim section to flag the I_norm row as still pending.

### WR-07: Duplicate finding-ID M16 across 02 and 03 with near-identical content

**File:** `pinn_instruction/original_latex/review-of-framework/issues/02-data-pipeline-and-validation.md:40`, `pinn_instruction/original_latex/review-of-framework/issues/03-curriculum-and-training-loop.md:31`
**Issue:** M16 (dt_out heterogeneity / collocation density) appears in both 02 and 03 as MAJOR-severity table rows with similar (not identical) text. Per the consolidation's ownership model in `09-RESEARCH.md` Appendix line 397, M16 should sit in `03-...` since it is a training-loop concern. Having it in both creates ambiguous canonical ownership.

**Fix:** Keep M16 in `03-...md:31` (training loop is the implementer of dt_out-aware collocation scaling). In `02-...md`, replace the M16 row with a one-line cross-link: "dt_out heterogeneity drives collocation scaling — see M16 in `03-curriculum-and-training-loop.md`." This matches the established cross-link pattern used elsewhere.

---

## Info

### IN-01: Typo "verabtim" in 03 end marker

**File:** `pinn_instruction/original_latex/review-of-framework/issues/03-curriculum-and-training-loop.md:645`
**Issue:** Line 645 reads `*End of verabtim audit Section 6.*` — should be "verbatim".
**Fix:** Replace `verabtim` with `verbatim`.

### IN-02: Doc-03 marginally over the 30-40 KB plan target

**File:** `pinn_instruction/original_latex/review-of-framework/issues/03-curriculum-and-training-loop.md`
**Issue:** Doc 03 is 40,794 bytes (40.8 KB), 794 bytes over the 40 KB upper bound from the size budget in `09-RESEARCH.md` Appendix. The total of 3 docs (96.3 KB) is well within the 87-121 KB combined target, so this is cosmetic.
**Fix:** Trim ~1 KB of redundant prose if exact compliance with the per-file budget is required. Otherwise document that the budget was a guideline, not a hard cap.

### IN-03: 02 Confirmed Findings — `M13` mis-placed in BLOCKING table

**File:** `pinn_instruction/original_latex/review-of-framework/issues/02-data-pipeline-and-validation.md:33`
**Issue:** Line 33 places `| M13 | **MAJOR** |` inside the table headed `### BLOCKING (Must resolve before training)`. The severity column says MAJOR but the table title says BLOCKING — readers may conclude either that M13 is BLOCKING (matching table title) or that it is MAJOR misplaced (matching severity column).
**Fix:** Move the M13 row to the MAJOR table at line 35-37, or add a "(promoted from MAJOR for this consolidation)" note in the rationale column.

### IN-04: Executive summary of 02 lists redundant items

**File:** `pinn_instruction/original_latex/review-of-framework/issues/02-data-pipeline-and-validation.md:9`
**Issue:** "Four critical blockers (B-06, B-11, missing validation gate, ID handling)" — but B-06 IS the validation gate and B-11 IS the ID handling issue. The list collapses to 2 unique items, named twice. Reads as 4 distinct blockers when it is actually 2.
**Fix:** Replace with "Two critical blockers (B-06 missing validation gate, B-11 non-contiguous ID handling) plus several major inconsistencies must be resolved..."

### IN-05: Domain notation `[-1/3, -1/3]` is a single point, not a range

**File:** `pinn_instruction/original_latex/review-of-framework/issues/01-architecture-and-physics-foundations.md:124, 330`
**Issue:** The Mass row in both the synthesized table and the verbatim Section 5.2 lists the equal-mass domain as `[-1/3, -1/3]`. With m_i = M_tot/3 for all bodies, `2*(1/3) - 1 = -1/3`, so all three components are exactly `-1/3`. Notation `[-1/3, -1/3]` is technically a degenerate interval; a clearer notation would be `{-1/3}` or "exactly -1/3 (degenerate)".
**Fix:** Cosmetic. Replace `[-1/3, -1/3]` with `{-1/3}` or note "all 3 components = -1/3 for equal-mass case."

### IN-06: MIGRATION.md groups Causal_Trainingmismatch sub-mechanisms into a single row

**File:** `pinn_instruction/original_latex/review-of-framework/issues/MIGRATION.md:33-48`
**Issue:** The Causal_Trainingmismatch source has 24 top-level `#` sections including "Localized ALM Execution," "Causal Gating Mechanism," and "Structural State Propagation" as distinct sections. MIGRATION groups them under a single "Resolution: Time-Windowed Causal-ALM Hybrid" row. Per `09-CONTEXT.md` D-09 ("every major section heading"), this is borderline acceptable since the source uses single-`#` headers for both major and minor sections, but a stricter completeness check would expect them to appear as individual rows.
**Fix:** Either (a) expand the MIGRATION row into 4 rows for the 4 sub-mechanisms (Localized ALM, Causal Gating, Structural State Propagation, plus the parent Time-Windowed Causal-ALM Hybrid), or (b) add a note in MIGRATION's preamble explaining that single-`#` headings in Causal_Trainingmismatch were grouped by topic to avoid 24 trivially-similar rows.

---

## Qualification Check Verification

Each phase-gate check from `09-VALIDATION.md`:

| # | Check | Status | Notes |
|---|-------|--------|-------|
| 1 | Completeness — MIGRATION.md covers every major section in 7 originals | PASS (with caveat) | All audit §1-§9 are mapped. Causal_Trainingmismatch's 24 single-`#` sections are grouped — see IN-06. Smaller .txt sources have no headers; logical grouping is acceptable. |
| 2 | Unique findings preserved — every bullet in `09-RESEARCH.md` Appendix appears in 3 new docs | PASS | Spot-checked tau_L formulas (03), 5-OoM softening (01), AD chain-rule factor (01), data-driven stage assignment (03), shape invariants alternative (01), input vector normalization table (01), AD chain-rule (01) — all present. |
| 3 | Conflict resolution — both live conflicts have "Considered Alternatives" subsections | PASS | Input vector encoding → 01 §Considered Alternatives (lines 295-305). s_min frame → 03 §Considered Alternatives (lines 503-511). |
| 4 | Decision callouts — all 5 [DECISION-NEEDED] items from D-12 present | PASS | 01 has 2 (input vector, I_norm); 02 has 1 (file format); 03 has 2 (causal training mode, s_min frame). 5 total. |
| 5 | No duplicates — no identical paragraphs >5 lines across the 3 new docs | PASS | Programmatic sliding-window check found zero duplicate 5-line blocks across (01,02), (01,03), (02,03). |
| 6 | Cross-links — each of 01/02/03 references the other two at least once | PASS | All 3 docs have References sections that link to the other two. Body text also contains inline cross-links. |

**Plan-01 metadata carryover (from `09-REVIEWS.md` cycle-2):** **RESOLVED.** The current `09-01-PLAN.md` artifact list at lines 28-37 lists only `01-architecture-and-physics-foundations.md` and `02-data-pipeline-and-validation.md`. The previously-flagged `03-curriculum-and-training-loop.md` claim has been removed. The reviewer's M2 concern is no longer present in the plan file.

**Size budgets (`09-VALIDATION.md` automated check):**
- 01-...md = 30,806 B (target 30-40 KB) — at floor, OK
- 02-...md = 24,690 B (target 20-30 KB) — OK
- 03-...md = 40,794 B (target 30-40 KB) — 794 B over hard cap; see IN-02
- MIGRATION.md = 7,688 B (target 5-8 KB) — OK
- README.md = 3,218 B / 32 lines (target 2-3 KB / ≤55 lines) — OK
- Total 3 docs = 96,290 B (target <120 KB combined) — OK

---

## Source-of-Truth Spot Checks

Verified against archived originals:

| Claim | Verification | Result |
|-------|--------------|--------|
| D = 6.694 = (G·M_tot·T²)^(1/3) | Audit line 59 confirms | OK |
| eps=1e-10 (static) / eps_soft=1e-5 (dynamic) | Causal_Trainingmismatch line 215 confirms | OK |
| SIREN init bug: `bound = sqrt(6/n) / omega0` (divide, not multiply) | Audit line 47 confirms | OK |
| ALM update: mu_p clipped to [1e-4, 100.0] | Audit line 369 confirms | OK |
| 184 standard IDs missing from gold | CLAUDE.md "2,565 / 2,749" gap = 184 — confirmed | OK |
| L_max = M_tot · r_char · v_char | next steps.txt Issue 1 line 142 confirms | OK |
| First/hidden omega_0 = 30 / 1, fixed (no scheduling) | Audit B-10 confirms | OK |
| Replay/lookahead 240+16 batch split | Audit Section 6.2 line 304 confirms | OK |

No factual errors detected in the spot-checked physics/architecture claims.

---

_Reviewed: 2026-04-27T16:43:27Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
