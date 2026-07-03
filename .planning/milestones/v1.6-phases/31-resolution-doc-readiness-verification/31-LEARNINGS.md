---
phase: 31
phase_name: "resolution-doc-readiness-verification"
project: "3-body-problem"
generated: "2026-07-02T10:45:12+00:00"
counts:
  decisions: 6
  lessons: 4
  patterns: 5
  surprises: 3
missing_artifacts: []
---

# Phase 31 Learnings: Resolution-Doc Readiness Verification

## Decisions

### Gate verdict READY-WITH-CAVEATS via fixed precedence
**What was decided:** Derive the exec-summary verdict mechanically: any NOT-READY trigger (silent finding / verified-fact contradiction / locked-convention violation) dominates; else any caveat yields READY-WITH-CAVEATS; else READY. All four checks passed clean but 12 non-blocking caveats (3 surface_to_user + 3 defer + more) were present, so the verdict landed READY-WITH-CAVEATS.
**Rationale:** Prevents a rubber-stamp verdict; the verdict must be re-derivable from the four check tables by a reviewer, not asserted.
**Source:** 31-01-PLAN.md Task 7, 31-01-SUMMARY.md "Gate verdict derivation"

### §1.16 read fresh rather than trusting research-phase characterization
**What was decided:** Re-read the resolution doc's §1.16 verbatim during execution instead of assuming the earlier research-phase summary of its position on the `D` convention.
**Rationale:** STOP-protocol compliance requires the doc's actual text, not a presumed verdict; confirmed the doc makes `D ≈ 4.6416` mandatory and rejects `6.694`, matching SCOPE-12 convention 6.
**Source:** 31-01-PLAN.md Task 5 (finding M), 31-01-SUMMARY.md key-decisions

### R4 figure-consistency check treats doc citations as provenance anchors, not verified restatements
**What was decided:** The resolution doc's 13 CLM/VF ID citations are provenance anchors only; the check verdict rests on whether the doc ever restates a verified numeric value with a contradicting number (it never does), not on a naive ID-to-ID mapping.
**Rationale:** Corrects an initial mapping mistake (see Lessons) while preserving the true PASS verdict.
**Source:** 31-01-SUMMARY.md key-decisions, 31-VERIFICATION.md Truth #5

### Task 8 (gate application) deferred to orchestrator as a human checkpoint
**What was decided:** Tasks 1–7 (the four checks + two deliverables) run autonomously; Task 8 (STATE/ROADMAP update + commit) is deliberately left for the orchestrator under `autonomous: false`, so the gate decision itself gets a human confirmation point before Phases 32–36 unblock.
**Rationale:** The gate DECISION is the one place in the phase that should not be fully autonomous, even though the underlying checks are.
**Source:** 31-01-PLAN.md objective, 31-01-SUMMARY.md "Commit-deferral note"

### Named gsd-tools state handlers used with a counter-integrity guard
**What was decided:** Record the gate outcome via the specific handlers `state complete-phase` / `state add-blocker` and `roadmap update-plan-progress`, wrapped in a mandatory snapshot-before / diff-after / restore-if-regressed guard, rather than a generic "update STATE.md" instruction or direct Write/Edit.
**Rationale:** This project's gsd-tools `state` mutators are documented to silently regress STATE.md progress counters; the guard catches and repairs any regression before commit.
**Source:** 31-01-PLAN.md Task 8 (finding C.1/C.2), 31-VERIFICATION.md "STATE/ROADMAP Counter-Integrity Check"

### Deliverable byte-structure modeled on the verified v1.5 Phase 24.5 analog
**What was decided:** Both `31-RESOLUTION-MAP.md` and `31-READINESS-REPORT.md` reuse the section structure of the user-accepted `24.5-RESOLUTION-MAP.md` / `24.5-READINESS-REPORT.md` templates rather than inventing a new schema.
**Rationale:** Grounds the deliverable schema in a prior user-accepted analog instead of an invented process-artifact schema, which the STOP protocol classifies as a MUST-surface decision if invented from scratch.
**Source:** 31-01-PLAN.md Task 6/Task 7 ("model on the user-accepted analog, do not invent a schema"), 31-01-SUMMARY.md tech-stack patterns

---

## Lessons

### A same-numbered ID scheme across two different registers caused a real defect
**What was learned:** The resolution doc's own `CLM-NN`/`VF-N` citation IDs (from its `CLAIMS-AND-FACTS-BUNDLE.md` package) reuse the same numbering scheme as the unrelated v1.5 `24-VERIFIED-FACTS.md` register — e.g. doc-03 CLM-10 is a grad-clip value while v1.5 CLM-10 is snapshot medians. The original R4 consistency table conflated the two, producing an unsound 12-row table even though the check's PASS verdict (0 contradictions) still held on the merits.
**Context:** Discovered by a concurrent re-check session and corrected in place in `31-READINESS-REPORT.md` (322 → 335 lines); only 3 of the 12 originally-listed figures genuinely cross-walk to a v1.5-verified fact.
**Source:** 31-VERIFICATION.md correction note, 31-01-SUMMARY.md mechanical/presentation choices

### An "independent" re-check can silently inherit an upstream defect
**What was learned:** The Phase 31 UAT (meta-verification) re-ran the structural, crosswalk, SCOPE-12, zero-edit, and counter checks genuinely independently, but its R4 spot-check trusted the report's CLM→v1.5-CLM mapping at face value and thereby reproduced the same register-conflation defect it was meant to catch.
**Context:** The gate verdict still stood (goal was achieved), but the verification's own claim of independence was weaker than stated for that one check.
**Source:** 31-UAT.md Test #3, "Honest caveat on this meta-verification's independence"

### Progress-table reconciliation via gsd-tools handlers does not reconcile narrative text elsewhere
**What was learned:** Running `roadmap update-plan-progress` correctly updated the ROADMAP progress table rows (Phase 30 → 5/5 Complete, Phase 31 → 1/1 Complete) but left an unrelated Phase 30 narrative checkbox (`[ ]`) and phrasing ("5/6 plans executed") stale and inconsistent with the table.
**Context:** Flagged as a minor UAT gap; does not affect correctness or the gate outcome but shows automated reconciliation tools can leave adjacent free-text out of sync.
**Source:** 31-UAT.md Test #10 / Gaps

### gsd-tools `state` mutators require an explicit before/after counter-integrity check
**What was learned:** `state complete-phase`, `state update-progress`, `state add-decision`/`add-blocker`, `state record-session`, and `state planned-phase` are all documented as counter-unsafe (capable of silently regressing `progress` counters or injecting false status fields) in this project.
**Context:** Required a mandatory snapshot → handler call → diff → restore-and-hand-correct sequence around every state mutation in Task 8, rather than trusting the handler's output directly.
**Source:** 31-01-PLAN.md Task 8 (finding C.2), user memory `gsd-state-planned-phase-bug` referenced in read_first

---

## Patterns

### Verified-analog byte-structure reuse for process-artifact deliverables
**Pattern:** When a phase must produce a new document with a schema-like structure (report sections, map sections), model the byte-structure on a prior user-accepted/verified analog artifact rather than inventing a new schema from scratch.
**When to use:** Any adjudication-milestone phase producing a structured deliverable (readiness report, resolution map) that has a prior-milestone precedent — avoids an invented process-artifact-schema decision that would otherwise require STOP-protocol surfacing.
**Source:** 31-01-PLAN.md Task 6/7, 31-01-SUMMARY.md patterns-established

### Revision-anchored citation keys (stable ID + scoped line numbers)
**Pattern:** Use a stable §/finding-ID anchor as the durable citation key, and treat line numbers as scoped to a specific commit revision, refreshed only on re-pagination.
**When to use:** Any cross-phase citation into a document expected to be re-paginated or lightly revised later (e.g. a landed research/resolution doc consumed by multiple downstream phases).
**Source:** 31-01-PLAN.md Task 6, 31-01-SUMMARY.md patterns-established

### By-identity matching instead of literal-text matching for crosswalks
**Pattern:** Match findings to document sections by semantic identity (e.g. "§1.12 componentwise automatic differentiation" = NS-12) rather than requiring literal heading-text equality, since a doc author's wording can drift from the tracking ID's original phrasing.
**When to use:** Any crosswalk/coverage check between a canonical finding list and prose sections whose headings weren't written to match that list verbatim.
**Source:** 31-01-PLAN.md Task 3, 31-CONTEXT.md D-09

### Fixed gate-verdict precedence with a mechanical anti-rubber-stamp backstop
**Pattern:** Pair a fixed verdict-precedence rule (trigger dominates > caveat > clean) with a cheap structural invariant check (e.g. a NOT-READY verdict must co-occur with at least one row flagged `Blocking? = yes`) so an inflated or deflated verdict is caught mechanically, not only by reviewer judgment.
**When to use:** Any gate/readiness-check phase producing a pass/fail-with-caveats verdict from multiple sub-checks.
**Source:** 31-01-PLAN.md Task 7 (finding B), 31-VERIFICATION.md "Gate-Verdict Derivability Check"

### Snapshot-diff-restore guard around known-unsafe state mutators
**Pattern:** Before calling a tool/handler documented to have a regression bug, snapshot the file it mutates, run the handler, diff the result against the snapshot, and restore + hand-correct if the diff shows unintended regression — rather than avoiding the handler entirely or trusting it blindly.
**When to use:** Any workflow step that must call a known-flaky state-mutation tool where a hand-rolled alternative would violate a "handlers only, no direct edits" governance rule.
**Source:** 31-01-PLAN.md Task 8, 31-VERIFICATION.md "STATE/ROADMAP Counter-Integrity Check"

---

## Surprises

### A same-numbered but unrelated ID register caused an unsound (but verdict-preserving) table
**What was surprising:** Two entirely separate registers (the resolution doc's own doc-03 `CLAIMS-AND-FACTS-BUNDLE.md` and the unrelated v1.5 `24-VERIFIED-FACTS.md`) happened to reuse the same `CLM-NN` numbering scheme for different claims, which caused an initially-unsound 12-row consistency table even though the underlying pass/fail verdict was correct throughout.
**Impact:** Required an in-place correction to both `31-READINESS-REPORT.md` and `31-VERIFICATION.md` after initial verification had already marked the phase "passed"; the UAT reproduced the same mistake independently before it was caught.
**Source:** 31-VERIFICATION.md correction note (top of file), 31-UAT.md concurrent-correction notice

### Legitimate documentation text tripped a prompt-injection detector
**What was surprising:** The R5 compliance-table phrasing "treat the 14D contract as a fixed input" triggered a benign prompt-injection detector flag on the substring "act as," despite describing the resolution doc's posture toward a locked contract rather than containing any embedded instruction.
**Impact:** Required manual confirmation that the flag was a false positive; no content change was made.
**Source:** 31-01-SUMMARY.md "Mechanical / presentation choices"

### The autonomous phase left its own deliverables uncommitted by design
**What was surprising:** Even though Tasks 1–7 ran fully autonomously and produced both deliverables, the plan's `autonomous: false` frontmatter meant the executor deliberately performed no `git commit` at all — the two Phase 31 artifacts sat uncommitted in the working tree awaiting an orchestrator-owned Task 8 checkpoint.
**Impact:** Downstream tooling or a naive "is Phase 31 done?" check reading only committed state would have seen no Phase 31 output at all until the orchestrator ran Task 8.
**Source:** 31-01-SUMMARY.md "Commit-deferral note", "Self-check" (no git commit performed)
