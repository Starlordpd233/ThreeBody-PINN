# Phase 20 Plan Review Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Orchestrate 4 parallel review subagents to audit Phase 20 planning artifacts for correctness, governance, dependencies, and completeness, then synthesize findings into a structured report.

**Architecture:** Pre-work builds a source manifest. A single Workflow tool invocation dispatches 4 subagents in parallel, each scoped to one review dimension with curated sources. The orchestrator collects, deduplicates, severity-classifies, verifies CRITICAL findings, and writes a final report.

**Tech Stack:** Claude Code Workflow tool (parallel subagent dispatch), Read tool, Write tool, Bash tool.

---

## File Structure

**Files to Read (Phase 20 Plans - all 9 files):**
- `<home>/Desktop/3_body_problem/.planning/phases/20-architecture-and-normalization-cleanup/20-CONTEXT.md`
- `<home>/Desktop/3_body_problem/.planning/phases/20-architecture-and-normalization-cleanup/20-RESEARCH.md`
- `<home>/Desktop/3_body_problem/.planning/phases/20-architecture-and-normalization-cleanup/20-GAPS.md`
- `<home>/Desktop/3_body_problem/.planning/phases/20-architecture-and-normalization-cleanup/20-DISCUSSION-LOG.md`
- `<home>/Desktop/3_body_problem/.planning/phases/20-architecture-and-normalization-cleanup/20-01-PLAN.md`
- `<home>/Desktop/3_body_problem/.planning/phases/20-architecture-and-normalization-cleanup/20-02-PLAN.md`
- `<home>/Desktop/3_body_problem/.planning/phases/20-architecture-and-normalization-cleanup/20-03-PLAN.md`
- `<home>/Desktop/3_body_problem/.planning/phases/20-architecture-and-normalization-cleanup/20-04-PLAN.md`
- `<home>/Desktop/3_body_problem/.planning/phases/20-architecture-and-normalization-cleanup/20-05-PLAN.md`

**Files to Create:**
- `<home>/Desktop/3_body_problem/docs/findings/milestone_v1.4/reviewing_phase20_plans/phase20_review.md` (Final report)

---

### Task 1: Build Source Manifest & Subagent Prompts

This task defines the exact source files per dimension and constructs the 4 subagent prompts.

**Files:**
- Reference: `<home>/Desktop/3_body_problem/docs/superpowers/specs/2026-06-04-phase20-review-framework-design.md`

- [ ] **Step 1: Define the Source Manifest**

Use the following manifest to construct subagent prompts in Task 2. Do not write this to disk; hold it in context.

**Dimension 1: Correctness & Coherence Sources**
```
<home>/Desktop/3_body_problem/pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md
<home>/Desktop/3_body_problem/pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md
<home>/Desktop/3_body_problem/pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md
<home>/Desktop/3_body_problem/pinn_instruction/issues/01-architecture-and-physics-foundations.md
```

**Dimension 2: Governance Compliance Sources**
```
<home>/Desktop/3_body_problem/CLAUDE.md (focus on CRITICAL GOVERNANCE block)
<home>/Desktop/3_body_problem/.planning/phases/20-architecture-and-normalization-cleanup/20-GAPS.md
<home>/Desktop/3_body_problem/.planning/milestones/v1.4-GAPS.md
```

**Dimension 3: Cross-Phase Dependencies Sources**
```
<home>/Desktop/3_body_problem/.planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md
<home>/Desktop/3_body_problem/.planning/REQUIREMENTS.md
<home>/Desktop/3_body_problem/.planning/ROADMAP.md
<home>/Desktop/3_body_problem/.planning/phases/18-frame-and-gauge-contracts/18-CONTEXT.md
<home>/Desktop/3_body_problem/.planning/phases/19-physics-and-loss-contracts/19-CONTEXT.md
```
*Note for Dimension 3:* Evidence packets B-01, B-10, M5, M8, M9, M10 **DO NOT EXIST** in `.planning/phases/16-evidence-framework-and-issue-adjudication/evidence/`. Only B-02..B-09 and M1..M4 exist. This is a known state the plans must account for.

**Dimension 4: Completeness & Improvement Sources**
Phase 20 plans only (internal quality check). No external governing sources.

- [ ] **Step 2: Draft the 4 Subagent Prompts**

Construct the following 4 prompts in memory. They will be passed to the Workflow tool in Task 2.

**Prompt 1: Correctness & Coherence**
```text
You are a meticulous plan reviewer for the 3-body problem project. Your focus is FACTUAL CORRECTNESS AND INTERNAL COHERENCE.

## Context
Phase 20 (Architecture and Normalization Cleanup) is a v1.4 adjudication milestone. It removes architecture and normalization ambiguity from framework specs without changing the SQR-SkipResNet-SIREN backbone unnecessarily. Live `pinn/` code is NOT a grounding source.

## Your Task
Read all 9 Phase 20 plan files listed below, then read the 4 governing source documents. Check every factual claim in the plans against the sources. Identify internal contradictions across plans.

## Phase 20 Files to Read
1. <home>/Desktop/3_body_problem/.planning/phases/20-architecture-and-normalization-cleanup/20-CONTEXT.md
2. <home>/Desktop/3_body_problem/.planning/phases/20-architecture-and-normalization-cleanup/20-RESEARCH.md
3. <home>/Desktop/3_body_problem/.planning/phases/20-architecture-and-normalization-cleanup/20-GAPS.md
4. <home>/Desktop/3_body_problem/.planning/phases/20-architecture-and-normalization-cleanup/20-DISCUSSION-LOG.md
5. <home>/Desktop/3_body_problem/.planning/phases/20-architecture-and-normalization-cleanup/20-01-PLAN.md
6. <home>/Desktop/3_body_problem/.planning/phases/20-architecture-and-normalization-cleanup/20-02-PLAN.md
7. <home>/Desktop/3_body_problem/.planning/phases/20-architecture-and-normalization-cleanup/20-03-PLAN.md
8. <home>/Desktop/3_body_problem/.planning/phases/20-architecture-and-normalization-cleanup/20-04-PLAN.md
9. <home>/Desktop/3_body_problem/.planning/phases/20-architecture-and-normalization-cleanup/20-05-PLAN.md

## Governing Sources to Read
A. <home>/Desktop/3_body_problem/pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md
B. <home>/Desktop/3_body_problem/pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md
C. <home>/Desktop/3_body_problem/pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md
D. <home>/Desktop/3_body_problem/pinn_instruction/issues/01-architecture-and-physics-foundations.md

## Specific Checks
1. **SIREN Contract**: Plans claim first_omega_0=30, hidden_omega_0=1, no scheduler, hidden-layer bounds divided by hidden_omega_0, standard init, stage-boundary retuning only. Verify against sources B and C.
2. **LayerNorm Contract**: Plans claim elementwise_affine=False, skip-path only, project-specific modification (not original SQR). Verify against source B.
3. **I₃ Consistency**: Check I₃ definition and range claims across ALL plans. Known risk: 3-way mismatch between ctl_instruction.md, issue doc, and plans. Flag every location where I₃ is defined or ranged.
4. **I_norm Naming**: Plans distinguish I_norm_raw (physics descriptor) from I_norm_in = tanh(I_norm_raw) (network input). Verify ARCH-04 work is blocked per GAP-20-01 and no plan oversteps by editing I_norm spec text without the proof vehicle.
5. **M9/M10 Vocabulary**: "Realized support" is planning shorthand only. Spec prose should use "dataset-occupied range" phrasing. Verify no plan treats "realized support" as a new technical term for the framework spec.
6. **Internal Contradictions**: Cross-check all 9 files against each other. Do any plans contradict 20-CONTEXT.md or each other on scope, definitions, or decisions?

## Output Format
Return a JSON array of findings. Each finding must have:
- "title": short descriptive title
- "dimension": "Correctness"
- "location": "file:line" or "file:line-line" (use absolute paths)
- "summary": what is wrong or contradictory
- "evidence": what the governing source actually says (quote it)
- "impact": what happens if unaddressed
- "recommendation": concrete fix
- "severity_hint": "CRITICAL" | "SIGNIFICANT" | "MINOR"

If no findings, return an empty JSON array [].
Return ONLY the JSON array, no markdown fences, no prose before or after.
```

**Prompt 2: Governance Compliance**
```text
You are a meticulous plan reviewer for the 3-body problem project. Your focus is GOVERNANCE COMPLIANCE.

## Context
Phase 20 is governed by the CRITICAL GOVERNANCE block in CLAUDE.md. Key rules: STOP protocol for source-silent semantic decisions, evidence-gating via Phase 16 ledger, no-live-code directive, no cross-phase reframing without surfacing.

## Your Task
Read all 9 Phase 20 plan files, then read the governance sources. Check every plan for compliance with governance rules.

## Phase 20 Files to Read
(Same 9 files as Prompt 1)

## Governing Sources to Read
A. <home>/Desktop/3_body_problem/CLAUDE.md (focus on CRITICAL GOVERNANCE: v1.4 block)
B. <home>/Desktop/3_body_problem/.planning/phases/20-architecture-and-normalization-cleanup/20-GAPS.md
C. <home>/Desktop/3_body_problem/.planning/milestones/v1.4-GAPS.md

## Specific Checks
1. **STOP Protocol**: Verify GAP-20-01 is OPEN in 20-GAPS.md and v1.4-GAPS.md. Verify ARCH-04 dependent work is explicitly blocked in all plans. Verify no plan invents an evidence vehicle (D-02.md, ARCH-04.md) or attaches ARCH-04 to M5.
2. **Evidence-Gating**: Plans must reference correct Phase 16 ledger rows and evidence packet paths BEFORE editing spec surfaces. Check that plans don't assume B-01, B-10, M5, M8, M9, M10 packets exist (they don't yet).
3. **No-Live-Code Directive**: Verify no plan treats `pinn/` code as a grounding source. Plans may mention live-code divergence only in forward-looking hand-off artifacts.
4. **Cross-Phase Reframing**: Verify no plan silently changes scope of another phase. Any cross-phase impact must be surfaced as a gap or discussion item.
5. **Semantic Decisions**: Verify all semantic decisions (mass encoding, physics derivations, etc.) are surfaced as gaps, not invented by the plans.
6. **Gap Classification**: Check GAP-20-01 classification as "process-artifact schema". Is this correct per governance definitions?

## Output Format
(Same JSON schema as Prompt 1, with "dimension": "Governance")
```

**Prompt 3: Cross-Phase Dependencies**
```text
You are a meticulous plan reviewer for the 3-body problem project. Your focus is CROSS-PHASE DEPENDENCIES.

## Context
Phase 20 depends on Phase 16 (evidence framework), Phase 18 (frame contracts), Phase 19 (physics contracts), and coordinates with Phase 20.5 (sampling). Concurrent execution of sub-plans 20-01 through 20-04 is intended.

## Your Task
Read all 9 Phase 20 plan files, then read the dependency sources. Check wave concurrency, forward-reference accuracy, and requirement mapping.

## Phase 20 Files to Read
(Same 9 files as Prompt 1)

## Governing Sources to Read
A. <home>/Desktop/3_body_problem/.planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md
B. <home>/Desktop/3_body_problem/.planning/REQUIREMENTS.md
C. <home>/Desktop/3_body_problem/.planning/ROADMAP.md
D. <home>/Desktop/3_body_problem/.planning/phases/18-frame-and-gauge-contracts/18-CONTEXT.md
E. <home>/Desktop/3_body_problem/.planning/phases/19-physics-and-loss-contracts/19-CONTEXT.md

## Specific Checks
1. **Wave Concurrency**: Can 20-01, 20-02, 20-03, 20-04 run concurrently? Check for implicit file-edit conflicts (e.g., two plans editing the same section of pinn_architecture.md or ctl_instruction.md).
2. **Phase 18/19 Forward-References**: Are references to Phase 18 and Phase 19 accurate? Does Phase 20 account for Phase 18's sampling_method.md FRAME-03 edits that shifted line numbers? (See v1.4-GAPS.md Phase 18 heads-up.)
3. **Phase 20.5 Separation**: Is the boundary between Phase 20 and Phase 20.5 clean? Any scope bleed?
4. **Evidence Packet Dependencies**: Plans reference evidence packets (B-01, B-10, M5, M8, M9, M10). These DO NOT EXIST yet. Do plans correctly instruct the executor to create/fill them per Phase 16 evidence workflow?
5. **Requirement/AC Mapping**: Does every ARCH-01 through ARCH-05 requirement in REQUIREMENTS.md map to a valid acceptance check (AC-ARCH-01 through AC-ARCH-05) in the plans?

## Output Format
(Same JSON schema as Prompt 1, with "dimension": "Dependencies")
```

**Prompt 4: Completeness & Improvement**
```text
You are a meticulous plan reviewer for the 3-body problem project. Your focus is COMPLETENESS AND IMPROVEMENT.

## Context
Phase 20 plans should be implementation-ready, with specific tasks, provable acceptance criteria, and clear organization.

## Your Task
Read all 9 Phase 20 plan files. Evaluate internal quality: task specificity, acceptance criteria, missing scope, organization, and discussion log completeness. No external sources needed.

## Phase 20 Files to Read
(Same 9 files as Prompt 1)

## Specific Checks
1. **Acceptance Criteria**: Are AC-ARCH-01 through AC-ARCH-05 closure conditions specific and provable? Can an executor definitively demonstrate closure?
2. **Task Granularity**: Are tasks appropriately sized (2-5 minutes each)? Any task too vague or too large?
3. **Missing Scope**: What's not covered that should be? Any requirement from REQUIREMENTS.md (ARCH-01..05) unaddressed by the plans?
4. **Clarity & Organization**: Is there redundancy between plans? Could organization be improved?
5. **Discussion Log**: Does 20-DISCUSSION-LOG.md capture key decisions and their rationale?
6. **Research Artifact**: Is 20-RESEARCH.md implementation-ready per D-08 in 20-CONTEXT.md? Does it map ARCH-01..05 to sources, ledger rows, and proof requirements?

## Output Format
(Same JSON schema as Prompt 1, with "dimension": "Completeness")
```

- [ ] **Step 3: Commit nothing yet**

This task produces only in-context artifacts (prompts). No files to commit.

---

### Task 2: Dispatch Parallel Subagents via Workflow

**Files:**
- Read: All Phase 20 plan files (by subagents)
- Read: All governing sources (by subagents)

- [ ] **Step 1: Execute the Workflow tool**

Invoke the `Workflow` tool with the following script. The 4 prompts from Task 1 Step 2 must be injected verbatim into the `agent()` calls below.

```javascript
export const meta = {
  name: 'phase20-plan-review',
  description: 'Review Phase 20 plans across 4 dimensions in parallel',
  phases: [{ title: 'Review' }]
};

// Inject the 4 prompts from Task 1 Step 2 here as template literals
const promptCorrectness = `<INSERT_PROMPT_1>`;
const promptGovernance = `<INSERT_PROMPT_2>`;
const promptDependencies = `<INSERT_PROMPT_3>`;
const promptCompleteness = `<INSERT_PROMPT_4>`;

const FINDING_SCHEMA = {
  type: 'array',
  items: {
    type: 'object',
    properties: {
      title: { type: 'string' },
      dimension: { type: 'string' },
      location: { type: 'string' },
      summary: { type: 'string' },
      evidence: { type: 'string' },
      impact: { type: 'string' },
      recommendation: { type: 'string' },
      severity_hint: { type: 'string' }
    },
    required: ['title', 'dimension', 'location', 'summary', 'impact', 'recommendation', 'severity_hint']
  }
};

const results = await parallel([
  () => agent(promptCorrectness, { label: 'review:correctness', phase: 'Review', schema: FINDING_SCHEMA }),
  () => agent(promptGovernance, { label: 'review:governance', phase: 'Review', schema: FINDING_SCHEMA }),
  () => agent(promptDependencies, { label: 'review:dependencies', phase: 'Review', schema: FINDING_SCHEMA }),
  () => agent(promptCompleteness, { label: 'review:completeness', phase: 'Review', schema: FINDING_SCHEMA })
]);

return {
  correctness: results[0],
  governance: results[1],
  dependencies: results[2],
  completeness: results[3]
};
```

- [ ] **Step 2: Parse subagent outputs**

Each subagent returns a JSON array of findings (or null on error). Parse all 4 results into a single unified array. If a subagent returns null or errors, log the dimension as incomplete and continue with the remaining results.

- [ ] **Step 3: Commit nothing**

No files created yet.

---

### Task 3: Deduplicate & Classify Findings

- [ ] **Step 1: Merge findings**

Combine all findings from the 4 subagent results into a single array.

- [ ] **Step 2: Deduplicate cross-cutting findings**

Two findings are duplicates if they cite the same `location` (file:line) AND describe the same underlying issue. When duplicates are found:
- Keep one finding
- Append all relevant dimensions (e.g., `"dimension": "Correctness, Governance"`)
- Preserve the highest severity hint

- [ ] **Step 3: Finalize severity classification**

Apply these definitions strictly:
- **CRITICAL**: Factual error that contradicts a governing source, governance violation (e.g., ARCH-04 work proceeding without gap resolution), or execution blocker (e.g., two plans editing the same lines concurrently with no coordination).
- **SIGNIFICANT**: Gap, ambiguity, or risk that could cause executor confusion. Missing evidence packet handling. Unclear acceptance criteria. Cross-phase reference that's technically correct but misleading.
- **MINOR**: Redundancy between plans, clarity improvements, organization suggestions, missing discussion log entries.

Override subagent `severity_hint` if it doesn't match these definitions.

- [ ] **Step 4: Sort findings**

Order: CRITICAL first, then SIGNIFICANT, then MINOR. Within each severity, group by dimension.

---

### Task 4: Verify CRITICAL Findings

**Files:**
- Read: Cited Phase 20 plan locations
- Read: Cited governing source locations

- [ ] **Step 1: For each CRITICAL finding, verify against sources**

For every finding classified as CRITICAL:
1. Read the cited `location` in the Phase 20 plan file
2. Read the governing source that the finding claims is contradicted
3. Confirm the discrepancy exists

- [ ] **Step 2: Downgrade false positives**

If a CRITICAL finding cannot be confirmed:
- If the issue is real but less severe, reclassify as SIGNIFICANT
- If the finding is incorrect, remove it from the list
- Document the verification outcome in the finding's `evidence` field

- [ ] **Step 3: Count verified findings**

Record final counts: N CRITICAL, N SIGNIFICANT, N MINOR. These go in the Executive Summary.

---

### Task 5: Generate the Review Report

**Files:**
- Create: `<home>/Desktop/3_body_problem/docs/findings/milestone_v1.4/reviewing_phase20_plans/phase20_review.md`

- [ ] **Step 1: Write the report**

Generate the markdown report using the following structure. Populate with verified findings from Task 4.

```markdown
# Phase 20 Plan Review Report

**Date:** 2026-06-04
**Reviewer:** Multi-agent parallel review (4 dimensions)
**Scope:** All 9 Phase 20 planning artifacts at `.planning/phases/20-architecture-and-normalization-cleanup/`

## 1. Executive Summary

- **CRITICAL findings:** [count]
- **SIGNIFICANT findings:** [count]
- **MINOR findings:** [count]
- **Top blockers:** [List CRITICAL finding titles, or "None" if zero]
- **Overall assessment:** [1-2 sentences on plan health]

## 2. Methodology

**Approach:** 4 parallel subagents dispatched via Workflow tool, each scoped to one review dimension:
- Correctness & Coherence: factual accuracy against governing sources
- Governance Compliance: STOP protocol, evidence-gating, no-live-code directive
- Cross-Phase Dependencies: wave concurrency, forward-references, requirement mapping
- Completeness & Improvement: task specificity, acceptance criteria, organization

**Sources audited:**
- `ctl_pinn_resolution.md` — candidate verdict source
- `pinn_architecture.md`, `ctl_instruction.md` — active framework specs
- `01-architecture-and-physics-foundations.md` — issue doc
- `CLAUDE.md` — CRITICAL GOVERNANCE rules
- `16-ISSUE-LEDGER.md`, `REQUIREMENTS.md`, `ROADMAP.md` — planning framework
- Phase 18/19 context files — cross-phase coordination

**Severity classification:** CRITICAL (blockers/errors), SIGNIFICANT (gaps/risks), MINOR (improvements)

## 3. CRITICAL Findings

[For each CRITICAL finding:]
### [C-NN] Finding Title
- **Dimension(s):** [dimension(s)]
- **Location:** `file:line`
- **Summary:** [what's wrong]
- **Evidence:** [what the source actually says]
- **Impact:** [what happens if unaddressed]
- **Recommendation:** [concrete fix]

## 4. SIGNIFICANT Findings

[Same format as Section 3, prefixed S-NN]

## 5. MINOR Findings / Improvements

[Same format as Section 3, prefixed M-NN]

## 6. Cross-Cutting Themes

[Identify patterns that span multiple dimensions or multiple plans. Examples: systematic over-reliance on a particular source, recurring ambiguity in I₃/I_norm terminology, evidence packet creation not properly instructed.]

## 7. Grey Areas for Discussion

[Items that need user adjudication — semantic decisions, process-artifact schema questions, or cross-phase reframing that the plans correctly surfaced but haven't resolved. Reference specific GAP entries where applicable.]

## 8. Per-Plan Summary

### 20-CONTEXT.md
[1-2 sentence health assessment]

### 20-RESEARCH.md
[1-2 sentence health assessment]

### 20-GAPS.md
[1-2 sentence health assessment]

### 20-DISCUSSION-LOG.md
[1-2 sentence health assessment]

### 20-01-PLAN.md
[1-2 sentence health assessment]

### 20-02-PLAN.md
[1-2 sentence health assessment]

### 20-03-PLAN.md
[1-2 sentence health assessment]

### 20-04-PLAN.md
[1-2 sentence health assessment]

### 20-05-PLAN.md
[1-2 sentence health assessment]
```

- [ ] **Step 2: Verify report completeness**

Check that:
- All verified findings appear in the correct severity section
- Finding IDs are sequential (C-01, C-02, S-01, S-02, M-01, M-02)
- Every plan has a per-plan summary
- Executive summary counts match the actual finding counts
- No placeholder text remains

---

### Task 6: Commit the Report

**Files:**
- Create: `<home>/Desktop/3_body_problem/docs/findings/milestone_v1.4/reviewing_phase20_plans/phase20_review.md`

- [ ] **Step 1: Stage and commit**

```bash
git add docs/findings/milestone_v1.4/reviewing_phase20_plans/phase20_review.md
git commit -m "docs(20): add Phase 20 plan review report

Multi-dimensional review across correctness, governance,
dependencies, and completeness. N CRITICAL, N SIGNIFICANT,
N MINOR findings."
```

Expected: Clean commit on `milestone/v1.4` branch.

---

## Self-Review Checklist

**1. Spec coverage:**
- ✅ Architecture: 4 parallel subagents (Task 2)
- ✅ Pre-work: source manifest (Task 1)
- ✅ Dimension 1 (Correctness): Prompt 1 with 4 governing sources
- ✅ Dimension 2 (Governance): Prompt 2 with CLAUDE.md + gap registers
- ✅ Dimension 3 (Dependencies): Prompt 3 with ledger + requirements + roadmap + Phase 18/19
- ✅ Dimension 4 (Completeness): Prompt 4 with plans only
- ✅ Finding classification: CRITICAL/SIGNIFICANT/MINOR (Task 3)
- ✅ Report structure: 8 sections (Task 5)
- ✅ Output path: absolute path to existing directory (Task 5)
- ✅ Verification: CRITICAL findings verified against sources (Task 4)
- ✅ Atomic commit (Task 6)

**2. Placeholder scan:** No TBD, TODO, "implement later", or "add appropriate" patterns. All prompts are complete. All file paths are absolute.

**3. Type consistency:** Finding schema is consistent across all 4 subagent prompts and the Workflow tool invocation. Severity definitions are consistent between Task 3 and Task 5.
