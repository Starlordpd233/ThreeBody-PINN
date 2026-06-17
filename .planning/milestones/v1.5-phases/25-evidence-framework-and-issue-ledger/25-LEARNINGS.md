---
phase: 25
phase_name: "Evidence Framework and Issue Ledger"
project: "3-body-problem"
generated: "2026-06-17"
counts:
  decisions: 11
  lessons: 7
  patterns: 6
  surprises: 4
missing_artifacts:
  - "25-VERIFICATION.md (not produced; UAT pass-1 finding 1 noted absence and was remediated at closure)"
---

# Phase 25 Learnings: Evidence Framework and Issue Ledger

## Decisions

### GAP-25-01 RESOLVED-WITH-INSTRUCTION (Option A: Split Reading)
The split reading means: Phase 25 mints the evidence-packet machinery (`_TEMPLATE.md`, `README.md`, the three EVID-10 records) but does NOT adjudicate every in-scope finding. The remaining 15 in-scope findings (B-06, B-11, M13, D7, G1, G2, G4, SASD, IPR, PSC, D-03, footer, mass-drift) have their evidence packets authored by the owning phase (26-28) immediately before its spec edits.

**Rationale:** A single-phase "adjudicate everything" reading would force Phase 25 to do spec-edit work for phases it does not own. The split reading keeps Phase 25 as machinery + the three EVID-10 records the resolution doc itself prescribes (SCS, D=6.694, M11/M12).
**Source:** 25-01-SUMMARY.md, 25-GAPS.md (GAP-25-01), 25-02-SUMMARY.md (key-decisions)

---

### GAP-25-02 RESOLVED-WITH-INSTRUCTION (PENDING Convention, Option A)
GAP-25-02 is the "owns records, not fixes" convention. Phase 25 produces verdict + spec-edit-ready prose; Phases 26/27/28 transcribe into ctl_instruction.md and pinn_architecture.md, citing the EVID-10 record by path. Phase 25 does not land spec edits.

**Rationale:** Splitting record-keeping from spec-editing keeps each phase's scope tight. Phase 25 mints the protocol and the three EVID-10 records; downstream phases own the spec transcription and the acceptance checks.
**Source:** 25-01-SUMMARY.md, evidence/README.md (Status Legend), 25-02-SUMMARY.md (D-02)

---

### D-11 Lifecycle Rules Block Re-Issued With Phase-Number Token Only
The v1.4 Lifecycle Rules block was re-issued by replacing ONLY the phase-number applicability token ("Phases 17-22, including Phase 20.5" → "Phases 26-28 (spec-edit phases; Phase 29 is the acceptance phase)"). The state machine, audit string, batch definition, and phase-exit gate are preserved VERBATIM (D-11 KEEP-VERBATIM list, Pitfall 6).

**Rationale:** Mechanical correction of stale applicability text only. The semantic content of the Lifecycle Rules is v1.4's and must not change.
**Source:** 25-01-SUMMARY.md (Task 3), 24-ISSUE-LEDGER.md (Lifecycle Rules block)

---

### D-04 Substitutions Applied to v1.4 Template
The v1.4 12-section evidence-packet template had its source paths swapped: issue-01 → issue-02, EVID-05 → EVID-10 conditional markers. `sampling_method.md` bullet dropped (frozen, SCOPE-08); `data_quality_assessment.md` added (citable, NEVER editable, SCOPE-09). New `### Dataset Evidence (§3b)` sub-block added referencing 24-VERIFIED-FACTS.md.

**Rationale:** The v1.4 template is the right shape; only the issue-specific markers need to change. The `sampling_method.md` drop honors its frozen status; the `data_quality_assessment.md` inclusion honors its read-only-citable status.
**Source:** 25-01-SUMMARY.md (key-decisions), evidence/_TEMPLATE.md

---

### D-03 Enforcement Encoded as New h3 Subsection
The D-03 downstream-enforcement rules are encoded as a new `### D-03 Downstream Enforcement` subsection under Phase-Exit Rule: packet-before-edit (EVID-06), phase-exit gate (VERIFIED/DEFERRED only), same-commit ledger edits. The rules are the D-03 contract for downstream spec-edit phases.

**Rationale:** Encoding the D-03 rules inline in the README makes them greppable and machine-checkable. The rules are not optional; the next phase that violates them will be caught.
**Source:** 25-01-SUMMARY.md (Task 2), evidence/README.md (D-03 subsection)

---

### EVID-10 Trigger Table Carries Exactly 3 v1.5 Conflicts
The EVID-10 trigger table has three rows: SCS, D=6.694, M11/M12. This is the v1.5 set, not the v1.4 set. The D-08 confinement of the work list to the three EVID-10 records held.

**Rationale:** The v1.4 trigger table had more rows; v1.5 narrows to the three conflicts the resolution doc itself prescribes. The other in-scope findings are routed to the owning phase's spec-edit plan.
**Source:** 25-01-SUMMARY.md (Task 2), evidence/README.md (EVID-10 Trigger Table)

---

### D-13 Enforced: Phase 25 Mints No New AC-IDs
Phase 25 mints zero new acceptance check IDs. The seeded AC-PIPE-01..10 and AC-VAL-01..04 stand. The evidence-packet template's "Named Acceptance Check" section cites the existing AC-IDs by name.

**Rationale:** New AC-IDs would conflict with the reserved set in Phase 21 / Phase 26. Honoring D-13 keeps the AC-ID namespace stable.
**Source:** 25-01-SUMMARY.md (key-decisions), 25-CONTEXT.md

---

### D-17 Recovery Tag Cut Before Any Phase 25 Mutation
Tag `v1.5-pre-phase-25` was cut from milestone/v1.5 HEAD (16f78284) before any Phase 25 mutation. No `-f`, no push. The tag is the recovery point for any Phase 25 rollback.

**Rationale:** A recovery tag is the only safe way to roll back a multi-commit phase. Cutting it before any mutation guarantees a clean starting point.
**Source:** 25-01-SUMMARY.md (Task 0), D-17

---

### SCS Verdict: accept-resolution (Post-v1.3 Gate Is Constraint-Entailed)
SCS verdict is `accept-resolution`. The locked post-v1.3 gate SCS > -5 is constraint-entailed; the issue doc's 1e-6 is the Acceptable/Marginal boundary (log10(1e-6) = -6), not a band edge; 1e-8 = log10(1e-8) = -8 falls inside Acceptable, not a band edge.

**Rationale:** The verdict grounds in dqa §3.1 band-table re-derivation, not on the resolution doc's recommendation alone (D-09). The first-principles check is the gate's authority.
**Source:** 25-02-SUMMARY.md, evidence/scs-thresholds.md

---

### D=6.694 Verdict: accept-resolution + CLM-13 Ratified Convention-Rejected
D=6.694 verdict is `accept-resolution`; CLM-13 is formally ratified `convention-rejected`. Raw-mass D = (G·T²)^(1/3) ≈ 4.6416 is constraint-entailed by Newton's-equation dimensional analysis (for G=1, T=10). The 6.694 value is arithmetically correct under the rejected mass-fraction convention and has three verified defects (mixed convention, additive-eps anti-pattern, E_scale outlier).

**Rationale:** The verdict grounds in Newton's-equation dimensional analysis, the ctl §2.5 explicit rejection, and three verified defects. D-09 holds.
**Source:** 25-02-SUMMARY.md, evidence/compute-globals-D.md

---

### M11 Severity Ruling: BLOCKING STANDS (Data-Integrity Grounds)
M11 explicit severity ruling: MAJOR → BLOCKING reclassification STANDS. The data-integrity argument is sufficient and grounded: byte-identical-subset, before-statistics ordering, fail-closed. Architectural-harm narratives are explicitly NOT load-bearing.

**Rationale:** The resolution doc explicitly defers the MAJOR→BLOCKING reclassification decision to EVID-10 (§3.3 line ~238). The data-integrity argument is the load-bearing rationale; architectural-harm is supplementary.
**Source:** 25-02-SUMMARY.md (key-decisions), evidence/m11-m12-severity.md

---

## Lessons

### D-09 Verdict-Grounding Independence From Resolution Doc
Every EVID-10 record's verdict rests on first-principles re-derivation + locked-spec citation + verified defects, not on the doc's recommendation. SCS grounds in band-table re-derivation; D=6.694 in Newton's-equation dimensional analysis + ctl §2.5; M12 in CLM-10 corrected medians; M11 in data-integrity arguments.

**Context:** The D-09 discipline is what makes the verdicts defensible to an external auditor who does not trust the resolution doc alone.
**Source:** 25-02-SUMMARY.md (key-decisions), project CLAUDE.md (STOP protocol)

---

### D-12 Close-With-Parent: Synthesis Views Share Parent's Packet
G3 closes with M11, G5 closes with M12. The synthesis-view rows do not get their own EVID-10 record. The Evidence-Packet cells in the ledger stay as `—` (no separate packet), and the per-finding note documents the close-with-parent.

**Context:** A synthesis view that shares a parent's evidence is not a separate adjudication. Closing with the parent is the only correct posture.
**Source:** 25-02-SUMMARY.md (key-decisions), D-12

---

### D-14 Conditional Dependents: No Shared Contract Discovered
The D-14 conditional Dependents section explicitly states "no shared contract discovered" for all three EVID-10 records. The Dependents cells in the ledger Status Table are preserved as Phase 25 seeded them.

**Context:** When two records do not share a contract, declaring a dependency is invention. The negative finding is recorded explicitly so a future verifier can re-check.
**Source:** 25-02-SUMMARY.md (key-decisions), D-14

---

### D-06 Same-Commit Discipline: SHA Backfill as Follow-Up Edit
The 3 evidence records + ledger wiring + per-finding notes land in one atomic commit. The final short SHA fills into the 4 per-finding status-transition log entries as a follow-up edit, not in the same commit (which would be self-referential).

**Context:** A commit cannot reference its own hash inline. The two-phase pattern (substantive commit + SHA-backfill follow-up) is the only path that keeps the audit label traveling with the work.
**Source:** 25-02-SUMMARY.md (deviations), D-06

---

### D-10 GUARD Triggers Recorded Explicitly Even When Not Fired
The M11 verdict section lists all four GUARD triggers and the negative result for each. The GUARD is "checked and not triggered" — required so a future verifier can re-check the guard, not re-derive it.

**Context:** A GUARD that is silently not-fired is indistinguishable from a GUARD that was never checked. Recording the negative result explicitly is the only honest posture.
**Source:** 25-02-SUMMARY.md (key-decisions), evidence/m11-m12-severity.md

---

### Worktree Base Mismatch (Cleared Prior to Resumption)
The worktree was on `16f78284` (v1.5-pre-phase-25 recovery tag) with the 3 evidence records content-complete but untracked, blocking the previous executor from completing the wiring. The mismatch was resolved before this executor resumed: the worktree moved to `da5a8203` (milestone/v1.5 HEAD) with the 3 evidence files still untracked and the recovery tag still at `16f78284` (verified after commit; SHA preserved).

**Context:** A worktree pinned to a recovery tag cannot complete wiring that requires the live HEAD. The recovery tag is for rollback, not for ongoing work.
**Source:** 25-02-SUMMARY.md (Issues Encountered)

---

### M12 Accept-Third-Position Verdict Is Distinct From accept-resolution
M12 verdict is `accept-third-position`: the issue doc's BLOCKING label is wrong AND its proposed fix is wrong, but a third position (locked spec / doc-cited) is correct. This is distinct from `accept-resolution` (issue doc correct) and `accept-issue-doc` (issue doc correct, spec needs edit).

**Context:** A "third position" verdict type is needed when both candidate texts are wrong. The 5-value verdict enum accommodates it.
**Source:** 25-02-SUMMARY.md (patterns-established), EVID-07

---

## Patterns

### EVID-10 Record Format With 12 Sections + Dataset Evidence (§3b)
The v1.5 evidence-packet template has 12 `##` sections: Header, Source Positions, Spec Evidence + Dataset Evidence (§3b), FUT-01 Hand-off Note, First-Principles Physics Check, Verdict, Root-Cause Framework Ambiguity, Locked Convention, Which Source Correct/Wrong, Before/After Spec Note, Named Acceptance Check, Status Transition Log. The `### Dataset Evidence (§3b)` sub-block is the v1.5 addition.

**When to use:** When authoring a v1.5 (or future) evidence-packet for a finding that needs both spec and dataset grounding.
**Source:** 25-01-SUMMARY.md (Task 1), evidence/_TEMPLATE.md

---

### Adjudicated-But-Unfixed Status Legend
A PENDING row with filled Verdict/Evidence-Packet columns is "adjudicated-but-unfixed" — the verdict is in, but the spec edit has not yet landed. The phase-exit gate distinguishes this from FIX_APPLIED (edit landed) and VERIFIED (AC passed).

**When to use:** When a finding's verdict is recorded but the spec edit is owned by a different phase. The status legend is the only way to track this state without re-adjudicating.
**Source:** 25-01-SUMMARY.md (patterns), evidence/README.md (Status Legend)

---

### Verdict-Ground Independence From Resolution Doc
Every EVID-10 record's verdict rests on first-principles re-derivation + locked-spec citation + verified defects, not on the resolution doc's recommendation. The discipline is encoded as D-09 in the v1.5 STOP protocol.

**When to use:** When a finding must be adjudicated against a candidate verdict source that may itself be wrong. The verdict must be defensible without trusting the candidate source.
**Source:** 25-02-SUMMARY.md (key-decisions), project CLAUDE.md (D-09)

---

### Phase-Exit Gate: Only VERIFIED or DEFERRED for In-Scope Findings
The phase-exit rule states that only `VERIFIED` or `DEFERRED` rows are allowed for in-scope findings at phase closure. PENDING / IN_PROGRESS / FIX_APPLIED rows block phase exit.

**When to use:** When closing a spec-edit phase, the ledger must show every in-scope row at a terminal state (VERIFIED or DEFERRED). A row at FIX_APPLIED with no passing AC is not closed.
**Source:** 25-01-SUMMARY.md (Task 2), evidence/README.md (Phase-Exit Rule)

---

### Packet-Before-Edit Enforcement
Every spec edit in Phases 26-28 must be preceded by an evidence packet for the affected finding. The packet is the citation source for the Before/After Spec Note in the spec.

**When to use:** When a spec edit's justification must be defensible to an external auditor. The packet is the only artifact that proves the edit was grounded.
**Source:** 25-01-SUMMARY.md (D-03 enforcement), evidence/README.md

---

### ID→Filename Map for Evidence Packets
Each evidence packet has a stable filename keyed by the finding ID: SCS → scs-thresholds.md; D=6.694 → compute-globals-D.md; M11+M12 → m11-m12-severity.md. The map is part of the README and is greppable for the owning phase.

**When to use:** When multiple evidence packets must be findable by finding ID. The map is the only way to keep the ID/filename relationship stable across phases.
**Source:** 25-01-SUMMARY.md (key-decisions), evidence/README.md (ID→Filename Map)

---

## Surprises

### Recovery Tag SHA Was Preserved Through Worktree Resumption
The `v1.5-pre-phase-25` recovery tag remained at `16f78284` after the substantive commit. The `evidence(25-02)` commit was layered on top of `da5a8203` (milestone/v1.5 HEAD at resumption) without rebasing or rewriting history. The tag's preservation is the load-bearing guarantee that the recovery point is still valid.

**Impact:** A future rollback can use the tag without worrying about whether it was moved by the substantive work.
**Source:** 25-02-SUMMARY.md (Metrics), D-17

---

### M11 Severity Ruling Made Here, Not Deferred Further
The resolution doc explicitly defers the MAJOR→BLOCKING reclassification decision to EVID-10 (§3.3 line ~238). The data-integrity argument is sufficient and grounded; the agent made the ruling here rather than deferring again. Deferring again would have been invention-by-procrastination.

**Impact:** M11 BLOCKING STANDS is the load-bearing decision for Phase 26 (PIPE-03 blacklist-exclusion). Without this ruling, the Phase 26 PIPE-03 work would have been blocked.
**Source:** 25-02-SUMMARY.md (key-decisions), evidence/m11-m12-severity.md

---

### M11 Architectural-Harm Narratives Explicitly Not Load-Bearing
The M11 packet's architectural-harm narratives (e.g., "blacklist not loaded at training time → model trains on excluded ICs") are explicitly flagged as not load-bearing. The data-integrity argument is the only rationale. The architectural-harm is supplementary context for the reader, not a verdict-grounding argument.

**Impact:** A future agent reading the M11 packet must distinguish between the verdict-grounding data-integrity argument and the supplementary architectural-harm narrative. Conflating them is a category error.
**Source:** 25-02-SUMMARY.md (key-decisions), evidence/m11-m12-severity.md

---

### Phase 25's Three EVID-10 Records Cover ~20% of In-Scope Findings
Phase 25 minted 3 EVID-10 records (SCS, D=6.694, M11/M12). The remaining 15 in-scope findings have their evidence packets authored by the owning phase (26-28) immediately before its spec edits, per GAP-25-01 Option A. The 3/18 ratio is a deliberate scope-narrowing.

**Impact:** A future milestone using the same template should plan the same scope-narrowing: the framework phase mints a small number of high-impact records; the spec-edit phases own the bulk of the per-finding packets.
**Source:** 25-02-SUMMARY.md (Next Phase Readiness)
