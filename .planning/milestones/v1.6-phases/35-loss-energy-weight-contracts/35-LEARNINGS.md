---
phase: 35
phase_name: "loss-energy-weight-contracts"
project: "3-body-problem"
generated: "2026-07-02T10:52:32+00:00"
counts:
  decisions: 6
  lessons: 4
  patterns: 5
  surprises: 3
missing_artifacts: []
---

# Phase 35 Learnings: Loss & Energy-Weight Contracts

## Decisions

### Four loss evidence packets transcribe the resolution doc without inventing new verdicts
**What was decided:** M15 (energy-weight schedule), NS-12 (componentwise AD), NS-13 (energy Huber-delta), and NS-18 (loss-scaling units) evidence packets were authored purely as transcriptions of the resolution doc's verdicts plus the already owner-ratified GAP-32-01 Option A for D-04 — no new semantic decision was made in authoring them.
**Rationale:** Packet-first discipline (established in Phase 32) requires evidence to exist before any spec edit; transcribing rather than adjudicating keeps the packet a faithful record of what the candidate source actually says.
**Source:** 35-01-SUMMARY.md "Decisions Made"

### Component math homed in pinn_architecture.md, assembly in ctl_instruction.md
**What was decided:** All LOSS-01..04 component formula bodies live in `pinn_architecture.md`; `ctl_instruction.md` carries only the total-loss assembly methodology and points back to `pinn_architecture.md` for the formulas.
**Rationale:** Reuses the same canonical-home split pattern established in Phase 34 (LOOP-04): one file owns formula bodies, the other owns ordering/methodology, linked by stable AC-ID anchors.
**Source:** 35-02-SUMMARY.md, 35-03-SUMMARY.md "Accomplishments"

### GAP-35-01 resolved: refined de-duplication of the causal-weight formula
**What was decided:** The `ctl_instruction.md` LOSS-04 callout now points to `pinn_architecture.md`'s Physics Residual Term as the single canonical home and cites only the `w_1 = 1` / `eta_c = 1` parameters — the full `w_n = exp(...)` formula body is no longer restated in the assembly file. A dedicated causal-weight single-home sentinel was added to the D-35-05 verifier alongside the existing energy-Huber sentinel.
**Rationale:** A git-grounded re-evaluation found the disputed `ctl_instruction.md` occurrence was Phase-35-authored content (not Phase-34-locked D-34-15 content as first assumed), so de-duplicating it required no locked-content gate — it realized the adversarial review's Option-B drift-elimination intent at a fraction of the assumed cost.
**Source:** 35-GAPS.md GAP-35-01 (RESOLVED-WITH-INSTRUCTION 2026-06-29), "Resolution reconciliation" section

### M15 cap-table/high-weight replacement rejected
**What was decided:** The issue-doc's proposal to replace the scheduled conservation weights with a cap-table/high-weight scheme was rejected; PHYS-05's scheduled conservation weights remain at or below one.
**Rationale:** Directly grounded in the resolution doc's rejection of the issue-doc's cap-table replacement.
**Source:** 35-01-SUMMARY.md Task 1, 35-02-SUMMARY.md "Decisions Made"

### NS-13 energy Huber-delta calibration deferred, delta_E = 1.0 retained as baseline
**What was decided:** `delta_E = 1.0` is preserved as the baseline value; empirical/median-scaled calibration was explicitly not selected in this phase.
**Rationale:** The resolution doc defers the calibration question rather than settling it; transcribing a calibrated value here would invent an unsupported number.
**Source:** 35-01-SUMMARY.md, 35-02-SUMMARY.md "Decisions Made"

### D-04/LOSS-04 causal mode transcribed directly from the already-resolved GAP-32-01
**What was decided:** `ctl_instruction.md` now states D-04/LOSS-04 as `RESOLVED-WITH-INSTRUCTION` (owner-ratified Option A), replacing the earlier "owner-pending Phase 35" forward-reference wording entirely.
**Rationale:** GAP-32-01 was already resolved with explicit user instruction in Phase 32; Phase 35's job is transcription of that verdict into the loss contract, not re-adjudication.
**Source:** 35-03-SUMMARY.md "Accomplishments", "Decisions Made"

---

## Lessons

### A verified phase can be validly reopened when the cost premise behind its original resolution turns out to be stale
**What was learned:** GAP-35-01 was first resolved as "Option A, accept as-is" at the execution-readiness gate, then reopened and given a refined resolution after a git-grounded re-check showed the disputed `ctl_instruction.md` occurrence was Phase-35-local content, not Phase-34-locked content as originally assumed — which removed the exact cost (a locked-content edit gate) that had made Option A look like the only cheap choice.
**Context:** The gap register explicitly notes this "supersedes the earlier ... note, which was not owner-grounded" — a real example of a resolution being revised once better grounding became available, rather than treated as immutable once written.
**Source:** 35-GAPS.md GAP-35-01 resolution note

### "Zero duplication" needs a canonical-home definition, not a literal occurrence count
**What was learned:** The causal-weight formula legitimately appears three times inside `pinn_architecture.md` alone (a display, a callout, and a catalog entry) under an accepted verdict-callout/catalog convention — this is not the drift vector the D-35-05 "zero duplicated normative body text" rule was written to prevent, which governs a single canonical *authoritative* home across the two spec files, not literal single-occurrence within one file.
**Context:** A literal reading of "zero" duplication could have wrongly flagged this internal-to-one-file repetition as a violation.
**Source:** 35-GAPS.md "Resolution reconciliation" point 2

### A wrong-checkout edit hazard recurred across multiple plans in this phase
**What was learned:** Both Plan 35-01 (file creation) and Plan 35-02 (patch application) independently hit the same failure mode — an editor/patch call resolving against the main `3_body_problem` checkout instead of the active `.worktrees/specwork` checkout — and had to detect and reverse the accidental edit before committing.
**Context:** Both were caught before any commit, but recurring across two separate plans in the same phase suggests this is a systemic risk in multi-worktree repos worth checking explicitly (verify the absolute path) before every edit, not just after something looks wrong.
**Source:** 35-01-SUMMARY.md "Issues Encountered", 35-02-SUMMARY.md "Issues Encountered", 35-03-SUMMARY.md "Issues Encountered"

### A hardcoded verification string can silently drift from a spec heading it's supposed to check
**What was learned:** An uncommitted plan-hardening pass re-introduced a comma-form heading string (`The Multi-Component, Physics-Constrained Loss Function`) into two plan files' anti-truncation guards, even though the heading had already been renamed to a paren-form (`The Multi-Component Loss Function (Physics-Constrained)`) in a prior committed plan — which would have raised a false truncation alarm if that guard had been re-run as written.
**Context:** Caught only because UAT independently re-derived the check against the actual committed heading rather than trusting the plan file's literal string; the committed `35-VERIFICATION.md` was unaffected since it had already used the correct heading.
**Source:** 35-UAT.md "Fixes Applied During UAT"

---

## Patterns

### Adversarial dual-review with an explicit cost/benefit table and flip conditions
**Pattern:** For a nontrivial gap with multiple plausible resolutions, run an independent evaluation that states a verdict, walks the core judgment question, models a concrete drift scenario, tabulates cost/benefit across every option, and explicitly states what evidence would flip the recommendation — rather than a single up-or-down recommendation.
**When to use:** Any STOP-protocol gap where the "obvious" answer and the "structurally correct" answer might diverge (e.g. a low-practical-risk exception to a categorical rule).
**Source:** 35-GAPS.md GAP-35-01 "Agent Analysis of Gap" section

### Formula-body vs. assembly-methodology canonical-home split
**Pattern:** When a contract spans both "what the formula computes" and "how it's used in the training loop," home the formula body in the architecture spec and the usage/ordering in the curriculum/training spec, linked by a stable AC-ID anchor — reused identically from Phase 34's LOOP-04 split.
**When to use:** Any spec-transcription phase whose subject naturally has both a mathematical-object half and a procedural-usage half.
**Source:** 35-02-SUMMARY.md, 35-03-SUMMARY.md tech_stack patterns

### Resolution-reconciliation addendum instead of silently overwriting a gap's resolution note
**Pattern:** When a later re-evaluation supersedes an earlier gap resolution, add a dated "Resolution reconciliation" section explaining what changed and why the new resolution differs from the recommendation on record, rather than deleting or silently rewriting the original note.
**When to use:** Any gap whose resolution is revisited after new grounding becomes available (e.g. a git-history check that changes the cost premise).
**Source:** 35-GAPS.md "Resolution reconciliation (2026-06-29)"

### One deterministic single-home sentinel per protected formula body
**Pattern:** Rather than one generic "no duplication anywhere" check, add a dedicated regex/token sentinel per specific formula body that must have exactly one canonical home, so a new formula needing protection is added as a new sentinel rather than expanding a monolithic check.
**When to use:** Any verification suite protecting multiple independent formulas from cross-file duplication.
**Source:** 35-GAPS.md GAP-35-01 resolution note ("causal-weight single-home sentinel ... added beside the energy-Huber sentinel")

### Grammatical subordination as a lightweight de-duplication fallback
**Pattern:** When full de-duplication (removing a formula body entirely from one file) is judged too costly, rewording the remaining occurrence so the pointer is the grammatical subject and the formula is a parenthetical restatement reduces (without eliminating) drift risk at much lower cost than a structural edit.
**When to use:** As a fallback when the ideal single-canonical-home edit is blocked by cost, scope, or governance friction, but leaving the duplication entirely unaddressed is also unacceptable.
**Source:** 35-GAPS.md GAP-35-01 "Agent Analysis of Gap" §6 "Missed Options" (Option F)

---

## Surprises

### The adversarial review's own recommended option was not the one ultimately adopted
**What was surprising:** A high-confidence independent evaluation concluded "Option B — full de-duplication — is the best resolution on the merits," but the actual resolution was neither pure Option A nor pure Option B — it was a refined middle path reached only after checking the live repository showed the review's cost premise (locked-content edit) no longer applied.
**Impact:** Demonstrates that even a rigorous, well-reasoned review's recommendation is only as good as the facts it was costed against — re-grounding against current repo state changed the answer.
**Source:** 35-GAPS.md GAP-35-01 "Agent Analysis of Gap" §1 vs. "Resolution reconciliation"

### A review's claimed inter-agent agreement was explicitly flagged as unverifiable and set aside
**What was surprising:** The gap resolution note explicitly states that the review's claim "both adversarial agents independently converged" on rejecting Option C is "uncorroborated by any artifact in the repo and was not relied upon" in reaching the final decision.
**Impact:** A specific, deliberate discipline of not trusting a persuasive-sounding claim inside a review artifact without independent evidence — even when the review's other reasoning was accepted.
**Source:** 35-GAPS.md "Resolution reconciliation" closing note

### A formula can legitimately repeat inside one file without being the duplication a rule targets
**What was surprising:** The causal-weight formula appears three separate times within `pinn_architecture.md` itself (display, callout, catalog) under an accepted convention — a literal count-based reading of "zero duplication" would have flagged this as already three-times violated before even considering the cross-file `ctl_instruction.md` occurrence.
**Impact:** Clarified that the D-35-05 rule's actual target is cross-file authoritative-home duplication, not intra-file repetition under an established presentation convention.
**Source:** 35-GAPS.md "Resolution reconciliation" point 2
