---
phase: 24.5
phase_name: "Resolution Doc Readiness Verification"
project: "3-body-problem"
generated: "2026-06-17"
counts:
  decisions: 6
  lessons: 4
  patterns: 4
  surprises: 2
missing_artifacts:
  - "24.5-UAT.md (not produced; the readiness report itself serves as the gate verdict)"
---

# Phase 24.5 Learnings: Resolution Doc Readiness Verification

## Decisions

### Gate Verdict: READY-WITH-CAVEATS
All four readiness checks pass; the gate verdict is READY-WITH-CAVEATS. The caveats are open items the resolution doc itself registers and routes downstream by design — OI-3 (calibration-pending constants), OI-6 (no-footer probe gap), OI-7 (Q-A4 label-semantics STOP-gap defeater + gold-rerun residue), OI-8 (M11 live-loader, outside grounding), OI-11 (CLM-13 → EVID-10/PIPE-09), OI-12 (optional addendum erratum). Phase 25 is unblocked.

**Rationale:** No NOT-READY trigger fired (no silent finding, no DATA-xx contradiction, no locked-convention violation). The caveats are downstream-routed, not blockers.
**Source:** 24.5-READINESS-REPORT.md, 24.5-SUMMARY.md

---

### Finding Coverage Crosswalk: 19/19 Covered, 0 Partial, 0 Silent
The crosswalk against Phase 24's 19-row issue ledger shows every finding is `covered` in the resolution doc. G1–G5 share their parents' sections per D-23; no finding is partially covered or silent.

**Rationale:** Coverage completeness is a precondition for adjudication. Partial or silent coverage would mean the resolution doc declines to address a finding, which is a gate failure.
**Source:** 24.5-READINESS-REPORT.md, 24.5-RESOLUTION-MAP.md, 24-ISSUE-LEDGER.md (19 rows)

---

### DATA-xx Consistency: 0 Contradictions With Verified CLM Values
The resolution doc names the DATA-07 addendum as authoritative and matches every verified value: CLM-10 medians 61/127/1003, DATA-05 70-ID quarantine, CLM-13 PENDING routed to EVID-10. Zero contradictions across CLM-01..13 + DATA-05.

**Rationale:** A resolution doc that contradicts the verified dataset facts cannot adjudicate; consistency is a non-negotiable precondition.
**Source:** 24.5-READINESS-REPORT.md (Task 3)

---

### Locked-Convention Compliance: HC-1..HC-6 Held, 0 Violations
The doc upholds all six locked v1.4 conventions (HC-1..HC-6) and rejects the issue-doc proposals that would breach them (SCS ratio thresholds, D=6.694). Zero scope observations requiring user decision.

**Rationale:** A resolution doc that violates a locked convention cannot adjudicate without overstepping. Compliance is the gate's hardest precondition.
**Source:** 24.5-READINESS-REPORT.md (Task 4)

---

### OI-12 Recorded as Optional, Non-Blocking Erratum
OI-12 (DATA-07 addendum CLM-08 summary-row slip) is recorded as an optional, non-blocking Phase-24-maintainer erratum. It is NOT routed as a fix package.

**Rationale:** An erratum in a non-load-bearing summary row is a maintainer concern, not a blocker. Routing it as a fix package would consume Phase 25's bandwidth for a non-consequential issue.
**Source:** 24.5-SUMMARY.md, 24.5-READINESS-REPORT.md (gap list)

---

### Resolution-Doc Map as Quick Reference for Phases 25-29
`24.5-RESOLUTION-MAP.md` is a quick-reference map: section index, finding-to-section mapping, EVID-06 citation guide, verdict-direction preview, doc-03 forward references, open-items carry-forward. The map is the primary input to Phase 25's evidence-packet authoring.

**Rationale:** Phase 25 needs to know which section of the resolution doc adjudicates which finding. The map is the only artifact that gives Phase 25 a fast lookup without re-reading the 820-line resolution doc.
**Source:** 24.5-RESOLUTION-MAP.md, 25-01-SUMMARY.md (consumes the map)

---

## Lessons

### Commit-Msg Policy Rejects Dotted Scope; planning Scope Used Instead
The repo's commit-msg policy (`scripts/git_policy/validate_commit_msg.py`) rejects a dotted scope (`24.5`). Commits use the fixed `planning` scope per the policy (phase scopes must be exactly two digits).

**Context:** Phase numbering with dot-segments (20.5, 24.5) is a directory-naming convention, not a commit-scope convention. The two-digit scope rule forces a fallback.
**Source:** 24.5-SUMMARY.md (Deviations), scripts/git_policy/validate_commit_msg.py

---

### STOP-Protocol Defeater Carried Forward, Not Filled
The doc's own refusal to invent an M13 fallback under silent locked stage definitions is preserved as a STOP-gap defeater (OI-7). The readiness report carries the defeater forward rather than filling the silence.

**Context:** A resolution doc that fills a source-silent gap with a default would violate the STOP protocol. Carrying the defeater forward is the only correct posture.
**Source:** 24.5-READINESS-REPORT.md (gap list), 24.5-SUMMARY.md (Governance section)

---

### Single-Coherent-Document Structure Re-Adjudicates CR-A + CR-B
The resolution doc is a single coherent 820-line document that re-adjudicates CR-A and CR-B together, with numbered line-citable §-sections and a fixed 7-part per-question structure.

**Context:** A multi-document resolution would have made the crosswalk much harder. A single coherent document keeps the adjudication in one place.
**Source:** 24.5-READINESS-REPORT.md (Task 1)

---

### Readiness Report Is the Gate Decision, Not a Separate Review
The 7-task readiness protocol culminates in Task 7 (gate decision). The report itself is the gate verdict; no separate review is needed.

**Context:** Phase 24.5 was a single-plan phase (24.5-01). The gate decision is the plan's final task, not a downstream artifact.
**Source:** 24.5-SUMMARY.md, 24.5-PLAN.md

---

## Patterns

### 7-Task Readiness Protocol for Adjudication Documents
Pre-execution gate (resolution doc present, Phase 24 COMPLETE) → Task 1 Structure → Task 2 Coverage crosswalk → Task 3 DATA-xx consistency → Task 4 Locked-convention compliance → Task 5 Resolution-doc map → Task 6 Readiness report → Task 7 Gate decision. Each task is a binary check; the protocol produces a single gate verdict.

**When to use:** When a milestone has a "candidate verdict source" that must be verified before the adjudication phases can begin, and the verification is structural, not substantive.
**Source:** 24.5-PLAN.md, 24.5-SUMMARY.md

---

### Finding Coverage Crosswalk as Pre-Adjudication Verification
For every finding in the issue ledger, check that the resolution doc has a `covered` marker (vs `partial` or `silent`). G1–G5 share their parents' sections per D-23; coverage is at the parent level, not the synthesis-view level.

**When to use:** When a resolution doc must adjudicate every finding in an issue ledger, and the agent needs a pre-adjudication check that the doc actually addresses every finding.
**Source:** 24.5-READINESS-REPORT.md (Task 2)

---

### Open-Items Carry-Forward in the Readiness Report
The readiness report lists open items (OIs) the resolution doc itself registers, with the caveat that they are downstream-routed by design. The OIs are not gate failures; they are forward obligations.

**When to use:** When a resolution doc carries open items that are by design deferred to later phases. The readiness report should distinguish "open by design" from "open by failure."
**Source:** 24.5-READINESS-REPORT.md (gap list), 24.5-RESOLUTION-MAP.md (open-items carry-forward)

---

### Resolution-Doc Map as the Phase 25 Input
A separate map artifact (section index, finding-to-section mapping, EVID-06 citation guide, verdict-direction preview) is the primary input to the adjudication phase. The map is not optional; it is the lookup table the next phase uses.

**When to use:** When a verification phase produces a large verdict-source document and the adjudication phase needs a fast lookup, not a re-read.
**Source:** 24.5-RESOLUTION-MAP.md, 25-01-SUMMARY.md

---

## Surprises

### 19/19 Coverage Required a Crosswalk, Not a Count
The 19/19 coverage was not a count from a single grep; it was a per-finding crosswalk that maps each row of the issue ledger to a section of the resolution doc. The crosswalk distinguishes `covered` from `partial` from `silent`.

**Impact:** A future agent who needs to verify coverage should re-run the crosswalk, not trust a single grep result. The crosswalk is the load-bearing artifact.
**Source:** 24.5-READINESS-REPORT.md (Task 2)

---

### CLM-13 Routing to EVID-10/PIPE-09 Was Already Decided in Phase 24
The readiness check found that CLM-13's routing to EVID-10 (Phase 25 evidence packet) and PIPE-09 (Phase 27 compute_globals) was already decided in Phase 24's verified-facts register. The resolution doc was consistent with this routing.

**Impact:** A future verification phase should check that the resolution doc's routing matches the verified-facts register's routing, not re-derive the routing. The routing is a Phase 24 decision.
**Source:** 24.5-READINESS-REPORT.md (Task 3), 24-VERIFIED-FACTS.md (CLM-13 row)
