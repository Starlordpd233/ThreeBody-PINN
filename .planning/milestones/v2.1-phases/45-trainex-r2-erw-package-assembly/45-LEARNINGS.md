---
phase: 45
phase_name: "trainex-r2 ERW Package Assembly"
project: "Three-Body Physics-Informed LLM"
generated: "2026-07-25"
counts:
  decisions: 7
  lessons: 7
  patterns: 6
  surprises: 5
missing_artifacts:
  - "45-UAT.md (no UAT artifact exists for this phase)"
---

# Phase 45 Learnings: trainex-r2 ERW Package Assembly

Phase 45 assembled the trainex-r2 External Research Workflow (ERW) package — commit-pinned snapshots, neutral research questions, a claims register, and a delivery note — for an external research agent, then verified the returned Route B (open-book) report. Extracted from 45-01..04 PLAN/SUMMARY, 45-VERIFICATION, 45-GAPS, 45-AUDIT. STATE.md was not consulted (unrelated pending changes); UAT does not exist for this phase.

## Decisions

### Package assembled per the canonical ERW runbook (PKG-09/10/11)
Three requirements frame the deliverable: PKG-09 commit-pinned snapshot set; PKG-10 neutrally framed research questions + prompt contract; PKG-11 claims register + delivery note with provenance and return format. Delivery opens the external-research gate and closes the v2.1 milestone.

**Rationale:** the ERW runbook is the canonical route for research-grade decisions; a self-contained, pinned, neutral package is the contract an external agent with zero repo access can act on.
**Source:** 45-VERIFICATION (Requirements Coverage; Phase Goal), 45-AUDIT Check 10

### Phase-wide `source_baseline` provenance pin
A single git commit pin (`9b1f0e7a4735df1c54867530cfd1f13b390e1514`) records the exact state of every snapshotted/excerpted source, and is recorded identically in the master, both bundles, the claims register, and the delivery note.

**Rationale:** one shared baseline makes drift detectable and every snapshot traceable to a fixed repo state.
**Source:** 45-01-SUMMARY (source_baseline), 45-AUDIT Check 6

### Diagnosis snapshot must be byte-identical to the Phase 44 original (D-08)
The shipped `44-DIAGNOSIS.md` snapshot's SHA-256 (`466000bc…`) must match the Phase 44 original exactly; any difference is a hard FAIL (RESEARCH Pitfall 1).

**Rationale:** the package must not silently alter the diagnosis it asks the researcher to evaluate; byte-identity is the integrity proof.
**Source:** 45-AUDIT Check 4, 45-VERIFICATION (Required Artifacts)

### Claims register by direct tag-lift, never re-derivation (D-09)
Walk the diagnosis snapshot and lift EVERY inline `[FACT]`/`[HYP]` tag occurrence (23 FACT + 7 HYP → 16 F-rows + 8 H-rows after merge), with reconciliation arithmetic. Never re-judge a claim's status. The standalone register is never uploaded (durable in-repo record); the master folds the same content verbatim.

**Rationale:** re-deriving fact/hypothesis status from scratch is a RESEARCH anti-pattern; the diagnosis's own tagging is the only source of status.
**Source:** 45-02-SUMMARY (Claims-register reconciliation), 45-all-PLAN (Task 1)

### D-13 owner decisions are NON-DISCRETIONARY and blocking
Two owner questions (Q1: add r1b references? Q2: add a 6th research question?) must be surfaced as A/B/C questions and answered by the owner — never auto-approved; answers recorded verbatim with dates. T-45-10 (Elevation of Privilege) explicitly marks the checkpoint "not-auto-approvable."

**Rationale:** package-scope changes (extra references, extra questions) are owner calls; D-13 overrides any auto-approve/yolo mode.
**Source:** 45-04-SUMMARY (Owner decisions), 45-all-PLAN (T-45-10, 45-04 must_haves)

### Owner added a 6th research question (Q2 = A), overriding the locked five-question set
The locked five-question set (D-05) was explicitly overridden: a 6th neutral question block was added to the master, with the override provenance (owner instruction, date) recorded. The addition changes NO attachment count (it lives inside existing files).

**Rationale:** the lock yields to an explicit owner override, but the override is recorded, not silent.
**Source:** 45-04-SUMMARY (Amendments applied — Q2 = A)

### GAP-45-01..04 resolved — the four post-delivery gaps
All four source-silent gaps resolved by owner instruction 2026-07-24. Determinative rulings: GAP-45-02 Option C (`λ_E^max = 1.0` provenance unrecoverable → treated as drift; conformance finding C-05 is a defect, not a variable); GAP-45-03 Option A (the per-stage `λ^max(k)` values ARE locked → C-05 is a defect; preflight must assert the entire per-stage table, not just the ≤1 cap).

**Rationale:** these were source-silent physics/spec-lock adjudications; only the owner could set the lock granularity and the drift-vs-authorization status.
**Source:** 45-GAPS GAP-45-01..04

## Lessons

### Gaps surfaced AFTER delivery, during mandatory return-report verification (ERW Rule 19)
All four Phase 45 gaps surfaced after package delivery, during verification of the returned Route B (open-book) report — not during assembly. Phase 45 owns the delivery AND its return path, so post-delivery gaps land here even when they are about content owned elsewhere (framework specs, v2.0 build phases).

**Context:** the verification-of-return step is itself a gap-discovery surface, not just a sign-off.
**Source:** 45-GAPS (header)

### Distinguish "provenance unrecoverable" from "proven absent"
GAP-45-02: the owner does not recall authorizing `λ_E^max = 1.0`, and no retained artifact records an authorization — but absence of a record is not proof no decision was made. The entry states exactly what could and could not be established, and treats the value as drift for correctness purposes.

**Context:** a neutral gap entry must not convert "I can't find the authorization" into "no authorization existed."
**Source:** 45-GAPS GAP-45-02 (Resolution)

### The run-record format does not capture WHY a config value deviates from spec
GAP-45-02 follow-on hygiene: the run record stores the value, never its provenance or authorization. This gap is the concrete motivating case for the verification charter's preflight placeholder-census and waiver policy.

**Context:** a format limitation became a conformance loophole; fixing it is deferred to the charter, with this as the tracked motivating case.
**Source:** 45-GAPS GAP-45-02 (Resolution, point 5)

### Lock-boundary granularity is itself a spec decision
Whether PHYS-05 locks the per-stage λ values or only the schedule form + ≤1 cap determines whether C-05 is a defect or a configuration choice, what preflight may enforce, and how future spec tables declare lock granularity. Owner ruling (GAP-45-03 Option A): per-stage values are locked.

**Context:** "locked" is ambiguous until the granularity is stated; the ambiguity was itself source-silent.
**Source:** 45-GAPS GAP-45-03

### An existing test can be under-specified once a boundary is tightened
`tests/phase40/test_scheduled_weights.py` asserts only that the cap fails closed — under-specified once GAP-45-03 Option A locks the entire per-stage table; the test must assert the whole table at run start and at every stage boundary.

**Context:** tightening a spec lock can invalidate a previously-adequate test's coverage claim.
**Source:** 45-GAPS GAP-45-03 (Resolution)

### A neutral research question must not smuggle a build directive
Neutrality re-audit (D-04 / SCOPE-26): no numeric value, schedule, direction, or preferred candidate in any "what a complete answer specifies" block; every DIAG-04 candidate mention hypothesis-labeled; every discriminating-test mention proposal-only.

**Context:** the line between "framing a question" and "baking in the answer" is policed per question.
**Source:** 45-AUDIT Check 7, 45-02-SUMMARY (Per-question neutrality attestation)

### Ambiguous owner instructions are re-surfaced, never filled in
If an owner pick's content instruction is silent or ambiguous on wording, placement, or extent: STOP — record the gap in 45-GAPS.md + v2.1-GAPS.md and re-surface; never fill in the blank.

**Context:** STOP protocol + RESEARCH Pitfall 6 applied to owner-instructed amendments.
**Source:** 45-all-PLAN (45-04 Task 2 action)

## Patterns

### Commit-pinned `source_baseline` for cross-file provenance consistency
One git commit hash recorded identically across master, bundles, claims register, and delivery note; a drift check (`git diff <baseline>..HEAD -- <path>`) confirms no snapshotted source changed since baseline.

**When to use:** any package that excerpts or snapshots repo content for an external party.
**Source:** 45-AUDIT Check 5/6, 45-01-SUMMARY

### Direct-tag-lift claims register (standalone + verbatim master fold)
Lift every inline tag occurrence from the source; merge duplicates with reconciliation arithmetic; the standalone register mirrors the master's claims section verbatim so the two cannot diverge; the standalone copy is never uploaded (costs no attachment slot).

**When to use:** building a claims register from a tagged diagnosis or evidence doc.
**Source:** 45-02-SUMMARY, 45-all-PLAN (Task 1)

### Ten-check re-derivable final audit (command + observed output + PASS/FAIL)
`45-AUDIT.md` records the exact command and quoted output for each of 10 checks (tree completeness, upload count, self-containment, snapshot fidelity, drift, pin consistency, neutrality, claims sync, boundary attestation, requirement traceability), so each verdict is re-derivable.

**When to use:** certifying a package delivery against its success criteria.
**Source:** 45-AUDIT (Checks 1–10), 45-all-PLAN (Task 3)

### Self-containment grep over authored uploads
A repo-path-marker grep over authored upload files returns zero matches (the external agent has zero repo access); the verbatim diagnosis snapshot is exempt (D-08).

**When to use:** any artifact that will leave the repo for an untrusted/zero-access recipient.
**Source:** 45-AUDIT Check 3, 45-all-PLAN (Trust Boundaries)

### D-13 blocking checkpoint (explicit not-auto-approvable)
Owner-decision todos surfaced as A/B/C questions, gate = blocking, answers recorded verbatim only; D-13 overrides auto-approve/yolo modes (T-45-10).

**When to use:** package-scope decisions that must be the owner's, not the agent's.
**Source:** 45-all-PLAN (T-45-10), 45-04-SUMMARY

### Per-question neutrality attestation
A manual per-question pass attesting that no build directive is smuggled into any "what a complete answer specifies" block, with a recorded attestation line per question.

**When to use:** authoring or amending neutral research questions.
**Source:** 45-AUDIT Check 7, 45-02-SUMMARY

## Surprises

### The returned report's claims verified STRONGER than asserted
Post-delivery verification of the Route B report confirmed all six repository-derived claims; two were stronger than the report asserted. The package's evidence base held up beyond what was claimed.

**Impact:** raised confidence in the returned research and seeded the conformance audit that followed.
**Source:** 45-GAPS (supporting evidence: factw-verification report), 45-VERIFICATION

### A 6th research question was owner-added, overriding the locked 5-question set
The locked five-question set (D-05) was not immutable: the owner explicitly added Q6, with the override provenance recorded. The addition changed no attachment count because it lives inside existing files.

**Impact:** a "locked" question set can still move on an explicit owner override — the lock governs agent behavior, not the owner.
**Source:** 45-04-SUMMARY (Q2 = A)

### Four consequential spec/conformance gaps surfaced only at return-report verification
The L_data formula component reduction, the λ_E authorization, the PHYS-05 lock boundary, and the causal-exponent clip bound — all source-silent, all surfaced during Rule 19 verification of the returned report, not during package assembly.

**Impact:** the assembly phase looked complete until its return path exposed unresolved spec-lock questions.
**Source:** 45-GAPS (header, GAP-45-01..04)

### "Provisional seam awaiting pilot calibration" became a locked per-stage value
`pinn/training/scheduled_weights.py` described the per-stage caps as "provisional seams (CTX-38) awaiting pilot calibration," yet GAP-45-03 Option A locks them — so the executed pilot's deviations are defects, not calibration. The provisional-vs-locked status was itself unresolved until the owner ruling.

**Impact:** code-comment framing ("provisional") disagreed with the eventual spec ruling ("locked"); the comments are not authority.
**Source:** 45-GAPS GAP-45-02 (Source silence), GAP-45-03

### Two distinct identifiers coexist for the diagnosis (evidence pin vs snapshot SHA-256)
The diagnosis evidence pin (`8631576…`, commit/tree context) and the snapshot file SHA-256 (`466000bc…`, content identity) serve different roles and must both be consistent across the package files.

**Impact:** audit consistency checks must track both identifiers, not conflate them.
**Source:** 45-AUDIT Check 4/6
