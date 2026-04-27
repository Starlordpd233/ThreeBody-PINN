---
phase: 09-issues-directory-consolidation
review_path: 09-REVIEW.md
fix_scope: critical_warning
findings_in_scope: 9
fixed: 9
skipped: 0
iteration: 1
status: all_fixed
fixed_at: 2026-04-27T18:00:00Z
---

# Phase 09: Code Review Fix Report

**Fix scope:** Critical + Warning (9 findings)
**Result:** All 9 findings resolved
**Files modified:** 3

## Critical Fixes

### CR-01: Internal contradiction on input-vector composition (01-...md)

**Fix:** Replaced the verbatim audit Section 5 (lines 309-389) with a synthesized "Final Resolved Input Vector Specification" aligned to Option B (shape invariants + direction cosines). The new Section 5:

- Uses the Option B 14-D breakdown: `[t', m_norm(3), E_norm, L_norm_norm, Q_norm, s_min_norm, I_norm, I_1, I_2, I_3, cos(θ), sin(θ)]`
- Provides shape invariant computation code (sorted mutual distances + normalization)
- Provides direction cosine computation code (L_hat projection + sin/cos derivation)
- Documents the gimbal-lock rationale for rejecting Option A's trig_vec
- Retains canonical ordering (Section 5.4) unchanged since it's option-independent
- Is labeled as the authoritative specification (no conflicting "verbatim" section remains)

**Side-effect resolutions:**
- WR-06: I_norm is now explicitly resolved (tanh form confirmed in Section 5.2 table)
- IN-05: Mass domain notation corrected from `[-1/3, -1/3]` to `{-1/3}`

### CR-02: Broken canonical cross-links (01-...md, 03-...md)

**Fix:** Corrected 3 broken links:
- `01-...md:288`: `markdown_conversions/PINN_architecture_plan.md` → `markdown_conversion/pandoc_conversion/PINN_architecture_plan.md`
- `01-...md:289`: `markdown_conversions/CTL-instruction-final.md` → `markdown_conversion/pandoc_conversion/CTL-instruction-final.md`
- `03-...md:494`: `markdown_conversions/CTL-instruction-final.md` → `markdown_conversion/pandoc_conversion/CTL-instruction-final.md`

03 line 495 already had the correct path — that line was left unchanged.

## Warning Fixes

### WR-01: B-04/B-05 row label misuse (01-...md:22)

**Fix:** Changed row label from `B-04/B-05` to `B-04`. Input vector composition is exclusively B-04 (Trigonometric Angle Encodings). B-05 (COM Frame Violation) is a separate row at line 23. The conflation was misleading.

### WR-02: Severity drift for M4 between 01 and 03 (03-...md:38)

**Fix:** Replaced the duplicate M4 row in 03's MINOR table with a one-line cross-link referencing the canonical M4 entry in `01-architecture-and-physics-foundations.md` MAJOR table. The audit classifies M4 as MAJOR; 01 is the architecture/physics canonical home.

### WR-03: M11/M12 severity elevation without rationale (02-...md:31-32)

**Fix:** Added inline rationale for both re-classifications:
- M11: "Re-classified from audit MAJOR to BLOCKING for this consolidation: the DataLoader cannot ship with silently-corrupted training data."
- M12: "Re-classified from audit MAJOR to BLOCKING for this consolidation: 54% sampling is infeasible and blocks batch construction."

### WR-04: Executive-summary blocker count (01-...md:9)

**Fix:** Replaced "Three blocking issues... Seven additional critical blockers" (implying 10 total when there are 7) with "Seven blockers documented in the table below; the three highest-priority are..."

### WR-05: Executive-summary misclassifies DECISION-NEEDED as BLOCKING (03-...md:9)

**Fix:** Rephrased from "Three critical blockers" to "Two critical blockers (B-07, B-08) plus one unresolved architectural decision (causal training mode)." The causal training mode is correctly identified as a [DECISION-NEEDED], not a BLOCKING table entry.

### WR-06: I_norm decision contradiction (01-...md:129-130, 193-204)

**Fix:** Resolved by CR-01 — Section 5 now uses the Option B table with `tanh(I_trace / (M_tot * r_char^2))` as canonical. The normalization table row was updated from "See Open Decision below" to the resolved formula. The [DECISION-NEEDED] callout was re-labeled [RESOLVED] with the resolution confirmed.

### WR-07: Duplicate M16 across 02 and 03 (02-...md:40)

**Fix:** Replaced the M16 table row in 02 with a cross-link: "dt_out heterogeneity (M16): ... canonical ownership live in `03-curriculum-and-training-loop.md` MAJOR table." M16 remains in 03 where it belongs (training loop is the implementer of dt_out-aware collocation scaling).

## Bonus Info-Level Fixes

The following info-level issues were fixed opportunistically since they touched the same lines as critical/warning fixes:

- **IN-01**: "verabtim" typo fixed in 03 line 645
- **IN-03**: M13 moved from BLOCKING table to MAJOR table in 02 (it was labeled MAJOR but placed under BLOCKING header)
- **IN-04**: Executive summary of 02 fixed from "Four critical blockers (B-06, B-11, missing validation gate, ID handling)" to "Two critical blockers (B-06 missing validation gate, B-11 non-contiguous ID handling)"
- **IN-05**: Mass domain notation corrected from `[-1/3, -1/3]` (degenerate interval) to `{-1/3}` (degenerate point)

## Remaining Info Issues (not in fix scope)

- **IN-02**: Doc 03 is 794 bytes over the 40 KB per-file budget. Cosmetic — combined total (96.3 KB) is well within the 87-121 KB target.
- **IN-06**: MIGRATION.md groups Causal_Trainingmismatch sub-mechanisms into a single row. Borderline acceptable per 09-CONTEXT.md D-09.

---

*Fix applied: 2026-04-27*
*Fixer: Claude (manual — mathematical grounding required per user instruction)*
