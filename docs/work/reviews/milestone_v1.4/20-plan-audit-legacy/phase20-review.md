# Phase 20 Plan Review Report

**Date:** 2026-06-04
**Reviewer:** Multi-agent parallel review (4 dimensions: Correctness, Governance, Dependencies, Completeness)
**Scope:** All 9 Phase 20 planning artifacts at `.planning/milestones/v1.4-phases/20-architecture-and-normalization-cleanup/`

## 1. Executive Summary

- **CRITICAL findings:** 0
- **SIGNIFICANT findings:** 3
- **MINOR findings:** 3
- **Top blockers:** None (no CRITICAL findings)
- **Overall assessment:** Phase 20 plans are well-structured, evidence-gated, and internally consistent. The three SIGNIFICANT findings concern execution hazards (Wave 2 ledger coordination, ungrounded numeric range) that require plan amendments before execution. MINOR findings are metadata and schema noise that should be cleaned up.

## 2. Methodology

**Approach:** 4 parallel subagents dispatched via Workflow tool, each scoped to one review dimension:
- **Correctness & Coherence:** Factual accuracy against governing sources (ctl_pinn_resolution.md, pinn_architecture.md, ctl_instruction.md, issue doc). Cross-checks all 9 Phase 20 files against each other.
- **Governance Compliance:** STOP protocol compliance, evidence-gating via Phase 16 ledger, no-live-code directive, no cross-phase reframing without surfacing.
- **Cross-Phase Dependencies:** Wave concurrency, forward-reference accuracy, Phase 18/19 coordination, Phase 20.5 boundary, requirement-to-AC mapping.
- **Completeness & Improvement:** Task specificity, acceptance criteria provability, discussion log completeness, research artifact readiness, missing scope.

**Sources audited:**
- `ctl_pinn_resolution.md` — candidate verdict source for v1.4
- `pinn_architecture.md`, `ctl_instruction.md` — active framework specs
- `pinn_instruction/issues/01-architecture-and-physics-foundations.md` — issue doc
- `CLAUDE.md` — CRITICAL GOVERNANCE rules
- `16-ISSUE-LEDGER.md`, `REQUIREMENTS.md`, `ROADMAP.md` — planning framework
- `18-CONTEXT.md`, `19-CONTEXT.md` — cross-phase coordination

**Severity classification:**
- **CRITICAL:** Factual error contradicting a governing source, governance violation, or execution blocker (e.g., two plans editing the same lines concurrently with no coordination).
- **SIGNIFICANT:** Gap, ambiguity, or risk that could cause executor confusion. Missing evidence packet handling. Unclear acceptance criteria. Cross-phase reference that's technically correct but misleading.
- **MINOR:** Redundancy between plans, clarity improvements, organization suggestions, missing discussion log entries.

**Note:** One subagent (Completeness) failed to produce structured output due to schema validation errors. Its dimension was reviewed inline by the orchestrator. All other dimensions produced verified findings.

## 3. CRITICAL Findings

No CRITICAL findings identified. All factual claims in the plans match their governing sources. No governance violations detected.

## 4. SIGNIFICANT Findings

### [S-01] Wave 2 Concurrent Ledger Write Coordination Gap Between 20-02 and 20-03

- **Dimension(s):** Dependencies, Completeness
- **Location:** `20-02-PLAN.md:1-15`, `20-03-PLAN.md:1-15`
- **Summary:** Plans 20-02 (ARCH-02 LayerNorm) and 20-03 (ARCH-03 I₃) are both labeled `wave: 2` with `depends_on: [20-01]`, implying they can run concurrently after Wave 1 completes. However, both plans modify the shared file `16-ISSUE-LEDGER.md` (20-02 advances the M8 row; 20-03 advances the M5 row). If dispatched as concurrent subagents, one plan's commit will clobber the other's ledger changes or create a git merge conflict. Neither plan's threat model acknowledges this shared-file hazard, and neither includes a coordination protocol.
- **Evidence:** Phase 19 faced the identical pattern (P01/P02 Wave 1 both touched the ledger) and explicitly mitigated it: `19-CONTEXT.md D-12` states "Shared 16-ISSUE-LEDGER.md and Issue Doc writes must be handled by a single coordination task or explicit serial order; P01/P02 parallelism applies only to disjoint spec-file edits." Phase 20 lacks equivalent coordination language.
- **Impact:** If an executor dispatches 20-02 and 20-03 concurrently, ledger status transitions for M5 and M8 will conflict. The Phase 16 ledger is the canonical status record; corrupted or lost transitions break VER-05 auditability. Because 20-04 depends on both 20-02 and 20-03, corrupted ledger state would propagate into Wave 3.
- **Recommendation:** Add a Wave 2 ledger-coordination note to both 20-02 and 20-03 (threat_model + a new task-level instruction), mirroring Phase 19 D-12. Either:
  - (a) Instruct the executor to run 20-02 Task 1 and 20-03 Task 1 sequentially (one completes its ledger commit before the other begins), or
  - (b) Designate one plan as the ledger owner for Wave 2 — e.g., 20-02 commits all Wave 2 ledger transitions (M8 AND M5) in a single serialized step after both plans' evidence packets are filled.
  Update both threat_models to list "Concurrent 16-ISSUE-LEDGER.md write with sister Wave 2 plan" as a MEDIUM threat.

---

### [S-02] 20-04 Pre-Written Spec Prose Contains Ungrounded Numeric Range for Hierarchical Mass Normalization

- **Dimension(s):** Dependencies, Correctness, Completeness
- **Location:** `20-04-PLAN.md:179-186`
- **Summary:** Plan 20-04 Task 2 Step 2 provides pre-written spec prose with the numeric range "approximately [-0.93, 0.585]" for the hierarchical-mass `m_norm` distribution. This number is not grounded in any cited source: 20-RESEARCH.md does not mention it, 20-CONTEXT.md does not mention it, and the cited `README.md` anchors (lines 245, 317-324) describe total mass support (standard masses = 1.0, hierarchical total mass near 3) but do not state per-slot `m_norm` realized ranges. The plan's own threat model says "Inventing numeric support ranges | HIGH | Every numeric range must cite README.md."
- **Evidence:** `20-CONTEXT.md D-06` requires "Numeric ranges must be grounded in cited sources/dataset documentation or replaced with qualitative realized-support wording." `20-04-PLAN.md` threat model line 91: "Inventing numeric support ranges | HIGH | Every numeric range must cite README.md; if a number cannot be grounded, use qualitative realized-support wording."
- **Impact:** If the executor applies the pre-written prose verbatim (the FALLBACK clause only triggers on non-accept-resolution verdicts, not on ungrounded numbers within an accept-resolution verdict), an ungrounded numeric range will be committed to the framework spec. This violates the D-06 governance rule and could mislead FUT-01 implementers about the actual dataset-occupied mass normalization range. The number may be correct (derived from a prior research artifact or dataset inspection not cited here), but without a citation it is indistinguishable from an invented value.
- **Recommendation:** Either:
  - (a) Replace "approximately [-0.93, 0.585]" with a placeholder like "[M10 executor: insert grounded range with README.md citation, or use qualitative wording per D-06]" so the executor knows to source the number during M10 packet creation, or
  - (b) Cite the source of the [-0.93, 0.585] range in the plan's `read_first` section and threat model so the executor can verify it.
  Option (a) is safer — it ensures the executor grounds the number before committing it to the spec.

---

### [S-03] 20-04 Wave Number Inconsistent with Dependency Graph

- **Dimension(s):** Dependencies
- **Location:** `20-04-PLAN.md:6-9`
- **Summary:** Plan 20-04 is labeled `wave: 2` but has `depends_on: [20-02, 20-03]`, where 20-02 and 20-03 are themselves wave 2. This means 20-04 cannot start until wave 2 plans complete, making it effectively a wave 3 plan. The wave field is misleading and inconsistent with Phase 19's precedent, where each wave number implies sequential ordering (P01/P02 = wave 1, P03 = wave 2, P04 = wave 3).
- **Evidence:** `20-04-PLAN.md` frontmatter: `wave: 2`, `depends_on: ["20-02", "20-03"]`. Phase 19 precedent (`ROADMAP.md` lines 201, 171-178): P01/P02 wave 1, P03 wave 2 (blocked on P02), P04 wave 3 (blocked on waves 1-2).
- **Impact:** An orchestrator or executor reading wave numbers may attempt to dispatch 20-04 concurrently with 20-02 and 20-03, violating the dependency graph. While the `depends_on` field is the actual gate, the misleading wave label creates confusion about the intended execution order and makes the plan set harder to reason about at a glance.
- **Recommendation:** Change 20-04 frontmatter from `wave: 2` to `wave: 3`. This matches Phase 19's convention, makes the execution order self-evident from the wave numbers alone, and eliminates the inconsistency between the wave label and the dependency graph.

## 5. MINOR Findings / Improvements

### [M-01] 20-GAPS.md Metadata Cites Wrong Governance File

- **Dimension(s):** Governance
- **Location:** `20-GAPS.md:9`
- **Summary:** 20-GAPS.md metadata references "AGENTS.md CRITICAL GOVERNANCE block" but the actual governance file is `CLAUDE.md` (the project's governing instructions file), not `AGENTS.md`.
- **Evidence:** `20-GAPS.md:9`: `governance: "Governed by AGENTS.md CRITICAL GOVERNANCE block: STOP protocol, source-grounding rules, and no-live-code directive for v1.4 spec decisions."` The actual file containing the CRITICAL GOVERNANCE block is `<home>/Desktop/3_body_problem/CLAUDE.md`.
- **Impact:** If a future agent or reviewer attempts to locate the governance rules by following the metadata reference to AGENTS.md, they will not find the file. This creates confusion about where the authoritative governance rules live, though the actual compliance is correct.
- **Recommendation:** Change line 9 from `governance: "Governed by AGENTS.md CRITICAL GOVERNANCE block..."` to `governance: "Governed by CLAUDE.md CRITICAL GOVERNANCE block..."` to correctly reference the actual governance file.

---

### [M-02] M8 Ledger Dependents Field Uses Requirement ID Instead of Finding/AC ID

- **Dimension(s):** Dependencies
- **Location:** `16-ISSUE-LEDGER.md:36` (M8 row)
- **Summary:** The Phase 16 ledger status table's "Dependents" column for the M8 row contains the string "ARCH-02", which is a requirement ID (`REQUIREMENTS.md` line 48) rather than a finding ID. All other non-empty Dependents entries in the ledger hold finding IDs (e.g., B-01 → "B-10", B-05 → "M3, B-11-folded-into-B-05") or, in one case (B-09), acceptance-check names ("B-02, PHYS-04, PHYS-05").
- **Evidence:** `16-ISSUE-LEDGER.md` status table column order: `| ID | Title | Phase | Status | Verdict | Sources Disagree? | Evidence Packet | Acceptance Check | Spec Section | Dependents | Last Updated |`. Dependents values for Phase 20 findings: B-01 → "B-10" (finding ID), B-10 → "-" (none), M5 → "-" (none), M8 → "ARCH-02" (requirement ID, not a finding ID), M9 → "-" (none), M10 → "-" (none).
- **Impact:** The inconsistency is a schema-level noise that can confuse a downstream agent (Phase 21 VER-05/VER-06 reconciliation, or a future ledger audit) that parses the Dependents column expecting finding or acceptance-check IDs. It does not block Phase 20 execution because the plans determine execution order from their `depends_on` headers and `20-CONTEXT.md`, not from the ledger's Dependents column. However, it sets a bad precedent for how future phases populate the ledger.
- **Recommendation:** Either:
  - (a) Change M8's Dependents cell from "ARCH-02" to "-" (no dependent findings), since ARCH-02 is the requirement M8 serves — which is already captured by the Acceptance Check column — and is not a dependent finding, or
  - (b) Align with the B-09 pattern and replace "ARCH-02" with the acceptance-check ID "AC-ARCH-02" if the intent was to name the downstream check.
  Apply the same interpretation consistently to any future Phase 20 ledger updates.

---

### [M-03] Discussion Log Could Benefit from Cross-Reference to 20-RESEARCH.md

- **Dimension(s):** Completeness
- **Location:** `20-DISCUSSION-LOG.md` (overall)
- **Summary:** The discussion log captures all 5 major decisions (SIREN, LayerNorm, I₃, Support ranges, Evidence/gap handling) plus 3 deep-review decisions (D-09, D-10, D-11) with clear option tables and rationale. However, it does not cross-reference `20-RESEARCH.md`, which contains the implementation-ready evidence map that operationalizes these decisions.
- **Evidence:** `20-DISCUSSION-LOG.md` ends with a "Deferred Ideas" section but no pointer to the research artifact. `20-RESEARCH.md` contains the route map by requirement, source anchors, and target spec surfaces that the executor will use.
- **Impact:** Low — the discussion log is marked "Audit trail only. Do not use as input to planning, research, or execution agents." However, a forward reference would improve traceability.
- **Recommendation:** Add a one-line pointer at the end of `20-DISCUSSION-LOG.md`: "For the implementation-ready evidence map that operationalizes these decisions, see `20-RESEARCH.md`."

## 6. Cross-Cutting Themes

### Theme 1: Phase 19 Precedent as the Coordination Gold Standard

Phase 19's explicit coordination mechanisms (D-12 for shared ledger writes, wave numbering convention, VER-05 audit trail) set a high bar that Phase 20 plans partially meet but do not fully replicate. The Wave 2 ledger race (S-01) and wave number inconsistency (S-03) both stem from Phase 20 not inheriting Phase 19's coordination patterns. Recommendation: add a "Phase 19 Precedent" section to `20-CONTEXT.md` that explicitly imports D-12 and the wave-numbering convention.

### Theme 2: Evidence Packet Creation Is Well-Instructed but Not Idempotent

All plans correctly instruct the executor to create/fill missing evidence packets (B-01, B-10, M5, M8, M9, M10) from `_TEMPLATE.md` before editing spec surfaces. However, none of the plans include an idempotency check — if a packet already exists (e.g., from a prior failed run), the executor might overwrite it. This is low-risk because the plans use `git add` for commits, but worth noting as an operational improvement for future phases.

### Theme 3: I₃/I_norm Terminology Ambiguity Is Properly Contained

The known 3-way mismatch between `ctl_instruction.md`, the issue doc, and the plans on I₃ definition is correctly isolated to plan 20-03 (ARCH-03 I₃ adjudication), which is marked `autonomous: false` and uses the EVID-05 contested adjudication workflow. ARCH-04 (raw vs bounded I_norm naming) is properly blocked by GAP-20-01. The plans do not attempt to resolve the ambiguity prematurely — this is governance compliance working as designed.

## 7. Grey Areas for Discussion

### Grey Area 1: ARCH-04 Evidence Vehicle (GAP-20-01)

**Status:** OPEN — blocking ARCH-04 dependent edits/proof.

**Context:** ARCH-04 is an explicit Phase 20 requirement and success criterion, but the Phase 16 ledger reserves no row, packet, or acceptance-check vehicle for the I_norm naming issue. The plans correctly surface this as GAP-20-01 and block ARCH-04 work.

**User decision needed:** Choose one of the 4 options recorded in `20-GAPS.md` GAP-20-01:
- (a) Add a Phase 16 ledger row for issue-doc D-02 / raw-vs-bounded I_norm with a named evidence packet + acceptance check.
- (b) Explicitly expand an existing Phase 16 row to cover ARCH-04.
- (c) Approve a Phase 20-local proof vehicle for ARCH-04 that is not a Phase 16 packet.
- (d) Defer ARCH-04 and record that Phase 20 cannot close it.

**Impact:** Until resolved, ARCH-04 remains blocked and Phase 20 cannot close it. Plans 20-01, 20-02, 20-03, and 20-04 are unaffected and can execute.

---

### Grey Area 2: M10 Realized Range Grounding

**Status:** Requires executor verification during 20-04 execution.

**Context:** The ungrounded numeric range [-0.93, 0.585] in 20-04 Task 2 Step 2 (S-02) must be grounded before being committed to the framework spec. The number may be correct — derived from a prior research artifact or dataset inspection not cited in the plan — but without a citation it is indistinguishable from an invented value.

**Executor action:** During M10 evidence packet creation, the executor must either:
- (a) Locate the source of the [-0.93, 0.585] range (e.g., dataset statistics, prior prescreening output) and cite it in the M10 packet, or
- (b) Replace the numeric range with qualitative wording per D-06 (e.g., "The hierarchical-mass m_norm range is asymmetric; this asymmetry carries mass hierarchy information").

**Impact:** If unaddressed, an ungrounded number enters the framework spec, violating D-06 and potentially misleading FUT-01 implementers.

## 8. Per-Plan Summary

### 20-CONTEXT.md

**Health:** ✅ Good. Contains all 8 implementation decisions (D-01 through D-08) with clear governance rules. The "Realized Support" vocabulary clarification (user decision 2026-06-03) is properly documented. Tooling hazard (GSD 20 → 20.5 mis-resolution) is flagged. Existing spec insights section provides accurate line numbers for active surfaces to audit.

### 20-RESEARCH.md

**Health:** ✅ Good. Implementation-ready evidence map per D-08. Route map by requirement clearly maps ARCH-01..05 to acceptance checks, ledger rows, evidence packets, and EVID-05 status. Source anchors cite specific line numbers in resolution doc and issue doc. Target spec surfaces are listed for each requirement. Packet state table correctly identifies all 6 missing packets (B-01, B-10, M5, M8, M9, M10) and notes that ARCH-04 has no authorized packet (GAP-20-01).

### 20-GAPS.md

**Health:** ✅ Good (with one MINOR fix). GAP-20-01 is properly OPEN with full STOP-protocol fields (decision point, where in artifact, task context, classification, source silence, mathematical/engineering grounding, agent was tempted to, user options, confidence of impact). Metadata cites wrong governance file (M-01) — should reference CLAUDE.md, not AGENTS.md.

### 20-DISCUSSION-LOG.md

**Health:** ✅ Good (with one MINOR improvement). Captures all 5 major decisions with option tables and rationale. Deep review decisions (D-09, D-10, D-11) are clearly documented. Could benefit from a cross-reference to 20-RESEARCH.md (M-03).

### 20-01-PLAN.md (ARCH-01 SIREN)

**Health:** ✅ Good. Wave 1, autonomous, depends on nothing. Frontmatter clearly states `must_haves` truths (B-01/B-10 packets exist, SIREN contract from D-02, no scheduler guidance remains, no pinn/ code read). Artifacts list includes all 3 files to create/modify. Key links pattern for ledger row B-01 → AC-ARCH-01 is correct.

### 20-02-PLAN.md (ARCH-02 LayerNorm)

**Health:** ⚠️ Needs coordination amendment (S-01). Wave 2, autonomous, depends on 20-01. Frontmatter and must_haves are correct (M8 packet, D-03 LayerNorm contract, elementwise_affine=False default, no pinn/ code read). However, shares 16-ISSUE-LEDGER.md write hazard with 20-03 — neither plan's threat model acknowledges the concurrent-write risk. Must add coordination note per S-01 recommendation.

### 20-03-PLAN.md (ARCH-03 I₃)

**Health:** ⚠️ Needs coordination amendment (S-01). Wave 2, non-autonomous (correctly — M5 is EVID-05 contested), depends on 20-01. Frontmatter correctly flags STOP protocol governance in the header. Must_haves include EVID-05 adjudication requirement, GAP-17-05 resolution (I₃ as metadata diagnostic), and defer-with-blocker safe default. Shares 16-ISSUE-LEDGER.md write hazard with 20-02 — must add coordination note per S-01 recommendation.

### 20-04-PLAN.md (ARCH-05 Support Ranges)

**Health:** ⚠️ Needs two fixes (S-02, S-03). Wave 2 (should be wave 3 per S-03), autonomous, depends on 20-02 and 20-03. Frontmatter and must_haves are correct (M9/M10 packets, D-06 realized-support framing, no pinn/ code read). However:
- Task 2 Step 2 pre-written prose contains ungrounded numeric range [-0.93, 0.585] that must be replaced with a placeholder or cited source (S-02).
- Wave number must be changed from 2 to 3 to match dependency graph (S-03).

### 20-05-PLAN.md (ARCH-04 I_norm — BLOCKED)

**Health:** ✅ Good (as a blocked placeholder). Correctly marked `type: blocked-placeholder`, `wave: null`, `blocked_by: GAP-20-01`, `autonomous: false`. Must_haves explicitly forbid inventing evidence vehicles or attaching ARCH-04 to M5. Unblock procedure lists all 4 GAP-20-01 options. Grounded facts section captures the candidate naming contract from D-05. Closure status correctly records ARCH-04 as BLOCKED.

---

*End of report.*
