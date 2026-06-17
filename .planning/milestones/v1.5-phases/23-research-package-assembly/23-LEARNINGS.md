---
phase: 23
phase_name: "Research Package Assembly"
project: "3-body-problem"
generated: "2026-06-17"
counts:
  decisions: 10
  lessons: 7
  patterns: 6
  surprises: 4
missing_artifacts:
  - "23-VERIFICATION.md (not produced; gate held by Plan 05's verification table only)"
---

# Phase 23 Learnings: Research Package Assembly

## Decisions

### D-07 User Checkpoint Locks Both Inclusion Calls Before Assembly
The 6-candidate document list was surfaced to the user at the D-07 gate before any package directory was created. The user ratified sampling_method.md (FROZEN annotation, SCOPE-08) and data_quality_assessment.md (research-report annotation, SCOPE-09) for inclusion — both YES. Total deliverable files: 6 (5 intact snapshots + 1 consolidated context file).

**Rationale:** Issue-02 is an adjudication milestone; assembling the package before the user explicitly approved the document list would risk silent inclusion of a frozen or read-only source. The gate is the only place where inclusion is the user's call.
**Source:** 23-02-PLAN.md, 23-02-SUMMARY.md, 23-CONSOLIDATION-PLAN.md

---

### DQA Characterization Is Advisory, Not Authoritative
The data_quality_assessment.md characterization recommends INCLUDE with the annotation "research report, not authoritative spec (SCOPE-09); sole written home of the post-v1.3 SCS gate; metric definitions unverified against dataset" — advisory A3 only. The final inclusion call is the user's, not the agent's.

**Rationale:** SCOPE-09 explicitly marks DQA as read-only; the agent may characterize but not interpret authority. The advisory call preserves the user's choice while supplying the context to make it.
**Source:** 23-01-PLAN.md, 23-DQA-CHARACTERIZATION.md

---

### D-13 Conservative Verified Rule for CLM Register
13-row CLM register uses a conservative rule: rows are `claimed-unverified` unless grounded in Documentation/. Status is one of `{claimed-unverified, verified}`; CLM IDs are append-only and stable.

**Rationale:** Phase 23 performs no empirical probes; "verified" must be earned by Phase 24's probes, not asserted. The conservative rule keeps the register honest and the Phase 24 verification checklist well-bounded.
**Source:** 23-01-PLAN.md, 23-CLAIMS-INVENTORY.md

---

### D-09 SCOPE-10 Overrides pinn/ Canonical Citation
The package header and consolidated context state that `pinn/` is NOT authoritative during v1.4/v1.5. Any "Canonical" citation that points to v1.3-era `pinn/basic_architecture.py` or `pinn/data-processing-pipeline-full.py` is OVERRIDDEN — the framework specs (ctl_instruction.md, pinn_architecture.md) are the source of truth.

**Rationale:** v1.3-era live code was the reference, not authority, for v1.4. The override prevents a downstream external agent from treating the wrong source as binding.
**Source:** 23-04-PLAN.md, research_package/framed-research-questions.md, project CLAUDE.md (2026-05-19 directive)

---

### Hard-Constraints Preamble Reproduces Locked v1.4 Conventions Verbatim
The six locked v1.4 conventions (14D contract, Jacobi IC₁₃, mass-weighted COM projection head, PHYS-03 softening + dual-ε, post-v1.3 SCS gate, PHYS-01 D convention) are reproduced verbatim with spec citations in the framed-research-questions preamble. The SCS gate cites only data_quality_assessment.md (its only written home) with the read-only annotation.

**Rationale:** The preamble sets the boundary the external research must respect. Verbatim reproduction with citations prevents the external agent from "refining" a locked convention. The SCS gate citation to DQA (not an editable spec) honors SCOPE-09.
**Source:** 23-04-PLAN.md, research_package/framed-research-questions.md

---

### Per-Finding Neutral Question Block as Mandatory Framing
Every in-scope issue-02 finding is posed as a neutral question: (i) issue-doc position + line citation, (ii) framework-spec position or silent, (iii) dataset facts by CLM ID. No agent decision is smuggled. Both known conflicts (SCS ratio thresholds, D=6.694) and the M13 fallback are posed with both positions and the locked counter-position cited, unsettled.

**Rationale:** The external research must be invited to settle, not pre-decided. A neutral question block is the only framing that preserves D-09 (verdict-grounding independence from any one source) while still giving the external agent a complete picture.
**Source:** 23-04-PLAN.md, research_package/framed-research-questions.md

---

### SCOPE-07 Inclusion Matrix in Consolidated Context
The consolidated-context.md file includes an explicit SCOPE-07 inclusion matrix explaining which scripts excerpts were included and why prescreening and runner excerpts were NOT needed (README coverage sufficient for those finding areas).

**Rationale:** The matrix is a re-derivability artifact: a future agent can read the matrix and reconstruct why each fragment was or wasn't included without re-reading SCOPE-07.
**Source:** 23-03-SUMMARY.md, research_package/consolidated-context.md

---

### Deterministic Blacklist Composition Cited, Not Asserted
The blacklist summary (2 hier + 63 std = 65) is re-derived deterministically from the JSON file and marked `claimed-unverified` per D-13. Phase 23 performs no empirical probes; DATA-02 in Phase 24 owns the verification verdict.

**Rationale:** The JSON is provenance, not verified truth. Keeping the assertion claimed-unverified preserves the gate between Phase 23's re-derivation and Phase 24's empirical verification.
**Source:** 23-01-SUMMARY.md, 23-03-SUMMARY.md

---

### D-02 Self-Contained Package for Repo-Blind Consumers
The package header in claims-table.md and the README is self-contained: it explains the CLM-ID scheme, the statuses, and the provenance convention inline, so a repo-blind external agent can consume the package without an external pointer. All paths are inline code spans; zero markdown links escape the package.

**Rationale:** The external research is conducted outside the repo by an agent that may not have repo context. Self-containment is the only way to guarantee the package is consumable.
**Source:** 23-05-SUMMARY.md, research_package/README.md, D-02

---

### D-16/D-17 STATE.md Mutated Only via gsd-tools Handlers
The STATE.md gate-open record (decision + blocker + metric + position) is set only via gsd-tools state handlers (`state add-decision`, `state add-blocker`, `state record-metric`, `state record-session`, `state advance-plan`, `state update-progress`) — never hand-edited.

**Rationale:** Hand-editing STATE.md breaks GSD's reconciliation model. The handlers are the only path that keeps STATE.md consistent with the rest of the planning artifacts.
**Source:** 23-05-SUMMARY.md, D-17

---

## Lessons

### Summary Reconstruction Pattern at Phase Closure
Plan 23-01's SUMMARY.md was authored at Phase 23 closure (2026-06-10), not at plan-execution time, reconstructed from the committed artifacts (5744feb), the verified-facts register, and 23-UAT.md re-verification. This is a Phase 24-style pattern adopted in v1.5.

**Context:** During early v1.5 phases, summary authoring was deferred and reconstructed at closure. The pattern continued in Phase 24-01..24-04 (and later abandoned as the workflow matured).
**Source:** 23-01-SUMMARY.md, 23-04-SUMMARY.md

---

### Both Known Conflicts Posed with Both Sides, Never Pre-Settled
The two known conflicts (SCS ratio thresholds, D=6.694) and the M13 fallback were all posed in framed-research-questions.md without settling. M13 was explicitly annotated as a Phase-26 STOP-gap candidate rather than a settled policy.

**Context:** The framing passed its own STOP-Protocol gate — no source-silent semantic, process-schema, or cross-phase decision was forced.
**Source:** 23-04-SUMMARY.md, 23-GAPS.md

---

### Doc-03 Boundary Stated Explicitly in the Preamble
M16, G6, and training-loop metric usage were stated as deferred forward-references to doc-03, not as questions. The boundary prevents the external research from spending effort on a milestone the agent is not adjudicating.

**Context:** The forward-reference framing respects D-09 (verdict-grounding) and keeps the external research scope-bounded to issue-02.
**Source:** 23-04-SUMMARY.md, research_package/framed-research-questions.md

---

### DQA Snapshot Included Despite SCOPE-09 Read-Only Status
The user's D-07 gate explicitly approved data_quality_assessment.md inclusion. The package carries it with the read-only annotation and a "sole written home of the post-v1.3 SCS gate" caveat. SCS is a locked convention; the DQA is the only place that holds the gate's home text, so the snapshot is essential to the package even though the spec cannot be edited.

**Context:** This is a case where SCOPE-09 (DQA read-only) and the need to include a stable snapshot of a locked convention's home text both hold. The inclusion is the only way to give the external research access to the SCS gate's authoritative source.
**Source:** 23-01-PLAN.md, 23-CONSOLIDATION-PLAN.md, 23-DQA-CHARACTERIZATION.md

---

### Issue-Doc Proposals Qualified Non-Authoritatively Throughout
Every issue-doc proposal in the framed-research-questions is qualified as "the issue doc proposes/recommends X (non-authoritative)"; no imperative carried. The framing holds even in the worked-example seed conflict for SCS thresholds.

**Context:** The neutral framing survives direct contact with the issue doc's recommended resolutions: P1-1..P2-2 are mapped to questions, not directives.
**Source:** 23-04-SUMMARY.md

---

### CLM-13 Recorded as a Contested Convention Conflict, Not a Dataset Count
D=6.694 is recorded as CLM-13 with status `claimed-unverified`, flagged as a contested convention conflict with the locked PHYS-01 counter-position D ~ 4.6416 (ctl_instruction.md section 2.5, line 598). The convention conflict is the load-bearing fact, not the numeric value.

**Context:** Phase 25's EVID-10 record later resolved this (D=6.694 verdict: accept-resolution; CLM-13 ratified convention-rejected). The Phase 23 conservative posture held.
**Source:** 23-01-SUMMARY.md, 23-CLAIMS-INVENTORY.md

---

### Post-Delivery Consolidation into Single Master File
On 2026-06-11 (the day after Phase 23 closure), a post-delivery accuracy and consolidation pass replaced the five source files with a single `RESEARCH-CONTEXT-MASTER.md`. The consolidation made the context easier for external agents to consume and Phase 23 remains marked complete.

**Context:** The consolidation was an accuracy/completeness improvement, not a re-execution. The package's byte-stability (against 605c0227) held across the consolidation.
**Source:** 23-05-SUMMARY.md (Post-Delivery Remediation section)

---

## Patterns

### Byte-for-Byte Snapshot with Hash-Object Provenance
`cp` source to `specs/`, verify with `diff -q` + `git hash-object` equality, then record per-snapshot provenance in `23-SNAPSHOT-HASHES.txt` (basename | source path | source commit hash). The package-wide commit pin anchors all snapshots to a single commit.

**When to use:** When packaging spec snapshots for external research, where the external agent needs to know the exact byte content and provenance of every included file.
**Source:** 23-03-PLAN.md, 23-SNAPSHOT-HASHES.txt

---

### CLM Stable-ID Claims Register with Append-Only IDs
One row per dataset figure, status in {claimed-unverified, verified}, IDs append-only and stable. The register doubles as a Phase 24 verification checklist (D-12). ID stability is what makes a downstream probe or citation findable.

**When to use:** When a research package needs to track which claimed figures are verified and which are still claims, and downstream phases will re-derive them.
**Source:** 23-01-PLAN.md, 23-CLAIMS-INVENTORY.md

---

### Read-Only File Characterization Pattern
Provenance + section map + compatibility relation + inclusion recommendation, zero edits to source. Characterizing a read-only file means describing its role in the package, not interpreting its authority.

**When to use:** When a research package must include a frozen or read-only source, and the downstream agent needs to know what the file is, what it contains, and what to do with it — without modifying the source.
**Source:** 23-01-PLAN.md, 23-DQA-CHARACTERIZATION.md

---

### Manifest Self-Containment via Inline Code Spans
All paths in the package README are inline code spans; zero markdown links escape the package. The README is a single point of consumption: a repo-blind reader can navigate the package without external context.

**When to use:** When a research package is consumed by an agent that may not have repo context, and links to other repo files would create a dependency on a workspace the consumer does not have.
**Source:** 23-05-SUMMARY.md, research_package/README.md

---

### Per-Finding Neutral Question Block with Three-Component Structure
For each in-scope finding: (i) issue-doc position + line citation, (ii) framework-spec position or silent, (iii) dataset facts by CLM ID. The structure forces the external agent to see both sources and the dataset facts before forming a verdict.

**When to use:** When a research package is sent to an external agent for adjudication, and the agent must consider both Issue-doc and Spec-doc sources plus empirical dataset facts before choosing a verdict.
**Source:** 23-04-PLAN.md, research_package/framed-research-questions.md

---

### Provenance Pinning at the Package Boundary
A single `23-SNAPSHOT-HASHES.txt` records every snapshot's source path and source commit hash. The package-wide commit pin (a single short SHA) anchors all snapshots. The README transcribes provenance verbatim from this file.

**When to use:** When a research package is consumed by an external agent that may receive a stale copy. The pin is the only way to detect and prevent stale-package use.
**Source:** 23-03-PLAN.md, 23-05-SUMMARY.md, 23-SNAPSHOT-HASHES.txt

---

## Surprises

### The 13-Row CLM Register Is Smaller Than the Finding Inventory
The findings inventory in 23-RESEARCH.md has more items than the 13 CLM rows. The CLM register tracks only dataset figures (countable values from the data), not methodology conflicts. The inventory is the superset; CLM is the subset that Phase 24 can probe.

**Impact:** A future agent looking for "where is finding X tracked?" must distinguish between the CLM register (data figures) and the findings inventory (broader scope). The two are linked but not identical.
**Source:** 23-CLAIMS-INVENTORY.md, 23-RESEARCH.md

---

### Both Locked v1.4 Conventions Conflict With the Issue Doc on SCS
The locked v1.4 SCS gate (post-v1.3) and the issue doc's SCS ratio thresholds (1e-6 / 1e-8) are in direct conflict. The framed-research-questions exposes the conflict with the worked-example seed, allowing the external research to see the conflict without being told which side to take.

**Impact:** The SCS conflict turned out to be one of the two most consequential issues in the v1.5 milestone; the external research was invited to resolve it.
**Source:** 23-04-PLAN.md, research_package/framed-research-questions.md, 25-evidence-framework-and-issue-ledger/evidence/scs-thresholds.md

---

### M13 Fallback Required Explicit Annotation as Phase-26 STOP-Gap Candidate
The M13 fallback (skip-to-Stage-6 vs flagged low-fidelity) was posed neutrally with both options. The agent did not assert either, and explicitly annotated the question as a Phase-26 STOP-gap candidate. The annotation was preserved in the framed-research-questions.md and was honored at Phase 26-04.

**Impact:** M13 became the most contentious finding in the v1.5 milestone, with a real STOP gap (GAP-26-01) raised at Phase 26-04 and resolved by the user on 2026-06-13.
**Source:** 23-04-SUMMARY.md, 26-04-SUMMARY.md (Resolution section)

---

### Post-Delivery Consolidation Identified Five Files Could Be One
The 2026-06-11 consolidation pass replaced 5 source files (issue doc, 4 spec snapshots, claims table, consolidated context) with a single `RESEARCH-CONTEXT-MASTER.md`. The agent had not originally planned this; the consolidation was an accuracy and consumption improvement surfaced after the package landed.

**Impact:** A future external research handoff should consider whether a single-master-file form is preferable to a multi-file package, especially when the external agent has limited context to navigate multiple files.
**Source:** 23-05-SUMMARY.md (Post-Delivery Remediation section)
