# Phase 16: Evidence Framework and Issue Adjudication - Pattern Map

**Mapped:** 2026-05-16
**Files analyzed:** 6 implementation targets
**Analogs found:** 6 / 6
**Scope:** Documentation-only; no framework specs or code should be edited by Phase 16 except the locked planning-doc path reconciliation.

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|-------------------|------|-----------|----------------|---------------|
| `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md` | documentation ledger | event-driven + batch index | `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-VALIDATION.md` + `pinn_instruction/issues/01-architecture-and-physics-foundations.md` | role-match |
| `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/evidence/README.md` | documentation protocol | file-I/O reference | `pinn_instruction/issues/README.md` | exact structure-match |
| `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/evidence/_TEMPLATE.md` | documentation template | file-I/O template | `pinn_instruction/issues/MIGRATION.md` + `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-VALIDATION.md` | role-match |
| `.planning/ROADMAP.md` | planning doc | transform | `.planning/ROADMAP.md` | exact self-edit |
| `.planning/REQUIREMENTS.md` | requirements doc | transform | `.planning/REQUIREMENTS.md` | exact self-edit |
| `.planning/PROJECT.md` | project doc | transform | `.planning/PROJECT.md` | exact self-edit |

Standard GSD artifacts such as `16-PLAN.md`, `16-VERIFICATION.md`, and `16-SUMMARY.md` are workflow outputs, not Phase 16 implementation targets for this pattern map.

## Pattern Assignments

### `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md` (documentation ledger, event-driven + batch index)

**Primary analog:** `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-VALIDATION.md`
**Supplemental analogs:** `.planning/STATE.md`, `.planning/REQUIREMENTS.md`, `pinn_instruction/issues/01-architecture-and-physics-foundations.md`, `ctl_pinn_resolution.md`

**Frontmatter pattern** (`.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-VALIDATION.md` lines 1-8):
```markdown
---
phase: 16
slug: evidence-framework-and-issue-adjudication
status: draft
nyquist_compliant: true
wave_0_complete: false
created: 2026-05-16
---
```

Copy the frontmatter style, but use ledger-specific keys: `total_findings`, `in_scope_findings`, `deferred_findings`, `traceability_verified`, and `last_verified_traceability`.

**Status/index table pattern** (`16-VALIDATION.md` lines 37-47):
```markdown
## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 16-01-01 | 01 | 1 | EVID-01 | T-16-01 | Template cannot omit required evidence sections | doc-structure | `rg -n "ctl_pinn_resolution.md|01-architecture-and-physics-foundations.md|Spec evidence|Code evidence" .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/evidence/_TEMPLATE.md` | W0 | pending |
```

Use the same compact Markdown table style for the ledger status table, with the locked ledger columns: `ID | Title | Phase | Status | Verdict | Sources Disagree? | Evidence Packet | Acceptance Check | Spec Section | Dependents | Last Updated`.

**Finding inventory pattern** (`pinn_instruction/issues/01-architecture-and-physics-foundations.md` lines 65-90):
```markdown
### BLOCKING (Must resolve before implementation)

| ID | Severity | Finding | Location | Fix |
|----|----------|---------|----------|-----|
| B-01 | **BLOCKING** | The source architecture document's hidden-layer init table gives a wrong formula... | `main_pinn.tex` Table 1 / `sqr_skipresnet_siren_backbone.tex`; live code check: `pinn/basic_architecture.py:37` | Keep/verify `bound = np.sqrt(6.0 / n_in) / hidden_omega0` in code; update the architecture document when LaTeX is revised. |
```

> *Note:* The "live code check" and "Keep/verify ... in code" wording above is from the original issue doc (pre-2026-05-19). Superseded by no-live-code directive: `pinn/` files are v1.3-era artifact, not v1.4 evidence.

Use this as the closest existing finding-table shape, but do not copy verdicts from the issue doc. Seed rows from Phase 16 decisions: B-01..B-10, M1..M5, M8..M10 as active, and M6/M7 as `DEFERRED` with `defer-with-blocker`.

**Traceability statement pattern** (`.planning/REQUIREMENTS.md` lines 86-125):
```markdown
## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| EVID-01 | Phase 16 | Pending |
...
| VER-05 | Phase 16 (defined) / Phases 17-21 (applied) | Pending |

**Coverage:**
- v1.4 requirements: 30 total (5 EVID + 4 IO + 4 FRAME + 6 PHYS + 5 ARCH + 6 VER)
- Mapped to phases: 30
- Unmapped: 0
```

Do not duplicate this table in the ledger. The ledger should record a one-line verification statement that REQUIREMENTS remains the source of truth.

**Dependency map pattern** (`pinn_instruction/issues/01-architecture-and-physics-foundations.md` lines 316-327):
```markdown
## Cross-Issue Interactions

Several issues interact non-trivially and must be resolved together, not independently:

| Interaction | Issues | Description | Severity |
|-------------|--------|-------------|----------|
| D + epsilon + COM | B-02, B-05, B-09 | Incorrect D corrupts scaled positions; COM transform order affects whether offsets survive; softening mismatch changes potential at close encounters | **Critical** |
```

Use this to seed `Dependents` fields, but prefer the explicit dependency decisions in Phase 16 context when the table is less granular.

**Evidence citation pattern** (`ctl_pinn_resolution.md` lines 200-219):
```markdown
## 3. Verified Audit Matrix

| Issue family | Report aliases | Spec evidence | Classification | Final decision |
|---|---:|---|---|---|
| Characteristic length and mass scaling | B-02, M3 | `ctl_instruction.md:L393-L399`; raw masses in `ctl_instruction.md:L452-L469`; raw masses in PINN residual at `pinn_architecture.md:L418-L430`. | False Positive | Keep `D=(G*T^2)^(1/3)` and raw masses. |
```

Use the `path:Lx-Ly` citation style in evidence-packet references. Do not treat the `Final decision` column as authoritative for Phase 16.

**Status transition log pattern** (`.planning/STATE.md` lines 100-118):
```markdown
### Decisions

Recent decisions affecting current work:

- [v1.4-init]: Resolution doc is NOT authoritative; EVID-05 mandates critical examination...
- [v1.4-init]: Iterative re-verification loop (`PENDING -> IN_PROGRESS -> FIX_APPLIED -> VERIFIED`) codified in VER-05...
```

Each per-finding subsection should include a terse append-only status log. Use ASCII arrows in new text: `PENDING -> IN_PROGRESS`.

**Validation pattern** (`16-VALIDATION.md` lines 41-47):
```markdown
| 16-01-05 | 01 | 1 | EVID-05 | T-16-05 | Contested findings cannot skip adjudication sections | doc-structure | `rg -n "First-Principles Physics Check|Root-Cause Framework Ambiguity|Locked Convention|Which Source Was Correct|YES - EVID-05 required|B-02|B-04|B-09|M5" .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/evidence/_TEMPLATE.md` | W0 | pending |
```

The ledger should be greppable for status enum, verdict enum, EVID-05 flags, dependents, phase-exit rule, and traceability statement.

**Not applicable:** imports, auth, runtime error handling, and code validation are not applicable because this is a Markdown artifact.

---

### `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/evidence/README.md` (documentation protocol, file-I/O reference)

**Analog:** `pinn_instruction/issues/README.md`

**Directory overview pattern** (lines 1-13):
```markdown
# Issues Directory - Consolidated PINN Audit Documentation

Consolidated 2026-04-27 from 7 scattered audit/issue files (~246 KB) into 3 thematic documents grouped by system layer, with full per-section provenance tracking.

## Thematic Documents

- **[01-architecture-and-physics-foundations.md](01-architecture-and-physics-foundations.md)** - Network architecture...
```

For `evidence/README.md`, mirror this with a concise purpose statement, then list `16-ISSUE-LEDGER.md`, `_TEMPLATE.md`, and future `evidence/{finding-id}.md` files.

**Canonical references pattern** (lines 15-20):
```markdown
## Canonical References

- [CTL Instruction (Curriculum Training Framework)](../markdown_conversion/framework-specs/ctl_instruction.md)
- [PINN Architecture Plan (SQR-SkipResNet-SIREN)](../markdown_conversion/framework-specs/pinn_architecture.md)
- [Dataset Documentation (Simulation Data Pipeline)](../../simulation_data/Documentation/README.md)
```

Use this section style for primary and supporting sources. Make the rule explicit: neither primary Issue 01 source is authoritative.

**Interaction/protocol matrix pattern** (lines 21-32):
```markdown
## Cross-Doc Interaction Matrix

| Topic | Canonical Home | Also Referenced By |
|-------|---------------|--------------------|
| 14-D input vector specification | `01` §Input Vector Normalization Formulas | `02` (pipeline produces it), `03` (training consumes it) |
```

For the evidence README, use short tables for verdict enum, EVID-05 trigger conditions, VER-05 lifecycle, batch regression policy, and AC-ID naming.

**Validation pattern:** The README must satisfy the Phase 16 validation check from `16-VALIDATION.md` lines 45 and 47: it should contain `YES - EVID-05 required`, lifecycle states, `Dependents`, `regression`, `phase-exit`, and "fix applied" language.

**Not applicable:** imports, auth, and runtime error handling.

---

### `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/evidence/_TEMPLATE.md` (documentation template, file-I/O template)

**Primary analog:** `pinn_instruction/issues/MIGRATION.md`
**Supplemental analog:** `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-VALIDATION.md`

**Fixed-schema document pattern** (`MIGRATION.md` lines 1-7):
```markdown
# Migration Manifest

Per-section provenance map tracing every major heading from the 7 archived originals to their destination(s) in the 3 consolidated thematic docs.

**Doc keys:** `01` = 01-architecture-and-physics-foundations.md, `02` = 02-data-pipeline-and-validation.md, `03` = 03-curriculum-and-training-loop.md

---
```

Start `_TEMPLATE.md` with a clear title, a one-paragraph purpose, and a short key/enum legend before the packet sections.

**Provenance table pattern** (`MIGRATION.md` lines 11-22):
```markdown
| Original section | Destination | Notes |
|---|---|---|
| Executive Summary | 01, 02, 03 §Executive Summary | Synthesized |
| §8 Cross-Issue Interaction Matrix | README.md; 01, 02, 03 §Cross-Issue Interactions | Synthesized |
```

Use this pattern for source positions: require side-by-side entries for `ctl_pinn_resolution.md` and `01-architecture-and-physics-foundations.md`, with line-range citations.

**Completeness checklist pattern** (`MIGRATION.md` lines 24-27):
```markdown
**Unique findings preserved:**
- [x] B-01..B-11, M1..M16, D1..D10, 28 author uncertainties -> distributed across 01/02/03
- [x] §5 input vector spec reconciled (-> 01); §6 verbatim batch construction (-> 03)
```

Use checklists sparingly for packet completeness, especially mandatory EVID-05 sections.

**Manual verification pattern** (`16-VALIDATION.md` lines 62-67):
```markdown
## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Reviewer readability of ledger and packet template | EVID-01..05, VER-05 | Grep checks prove required fields exist, not that the workflow is understandable to future agents | Read `16-ISSUE-LEDGER.md`, `evidence/README.md`, and `evidence/_TEMPLATE.md`; confirm a future Phase 17-21 agent can identify required citations, verdict enum, EVID-05 sections, and status transition rules without external explanation. |
```

Use HTML comments in the template to mark required/conditional sections, but keep headings greppable exactly as validation expects.

**Required section order to copy into `_TEMPLATE.md`:**
```markdown
# Evidence Packet: <ID> - <Title>

## Header
## Source Positions
## Spec Evidence
## Code Evidence
## First-Principles Physics Check
## Verdict
## Root-Cause Framework Ambiguity
## Locked Convention
## Which Source Was Correct / Wrong
## Before / After Spec Note
## Named Acceptance Check
## Status Transition Log
```

**Not applicable:** imports, auth, and runtime error handling.

---

### `.planning/ROADMAP.md` (planning doc, transform)

**Analog:** `.planning/ROADMAP.md` itself

**Verification lifecycle pattern** (lines 86-95):
```markdown
#### Verification Protocol (applies to every phase)

Every issue and every edit in v1.4 follows this loop:

1. **Adjudicate** - for findings where the resolution doc and the issue doc disagree...
2. **Fix** - apply the spec edit...
3. **Verify** - run the acceptance check...
4. **Re-verify after every batch** - re-run the acceptance check...
5. **Ledger discipline** - each finding's status (...) lives in `.planning/milestones/v1.4-phases/16-evidence-framework/16-ISSUE-LEDGER.md`.
```

Only replace the stale path with `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md`. Preserve lifecycle wording.

**Phase detail pattern** (lines 107-120):
```markdown
### Phase 16: Evidence Framework and Issue Adjudication
**Goal**: Reviewers can trace every Issue 01 decision to direct evidence...
**Requirements**: EVID-01, EVID-02, EVID-03, EVID-04, EVID-05, VER-02, VER-05...
**Success Criteria** (what must be TRUE):
  1. Reviewer can inspect issue-by-issue evidence packets...
```

Only update the stale ledger path in success criterion 6. Do not rewrite phase goals or success criteria.

---

### `.planning/REQUIREMENTS.md` (requirements doc, transform)

**Analog:** `.planning/REQUIREMENTS.md` itself

**Requirement prose pattern** (lines 53-58):
```markdown
- [ ] **VER-05**: Every fix is closed through an iterative re-verification loop. The issue ledger tracks each finding through `PENDING -> IN_PROGRESS -> FIX_APPLIED -> VERIFIED`. ... The ledger lives at a stable path (recommended: `.planning/milestones/v1.4-phases/16-evidence-framework/16-ISSUE-LEDGER.md`) ...
```

Only replace the recommended stale path. Preserve the requirement semantics and status lifecycle.

**Traceability table pattern** (lines 86-125):
```markdown
## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| EVID-01 | Phase 16 | Pending |
...
**Coverage:**
- v1.4 requirements: 30 total (5 EVID + 4 IO + 4 FRAME + 6 PHYS + 5 ARCH + 6 VER)
- Mapped to phases: 30
- Unmapped: 0
```

Use this table as the source of truth for the ledger traceability statement. Do not duplicate it in `16-ISSUE-LEDGER.md`.

---

### `.planning/PROJECT.md` (project doc, transform)

**Analog:** `.planning/PROJECT.md` itself

**Active milestone pattern** (lines 71-96):
```markdown
## Current Milestone: v1.4 Resolving 01 Architecture and Physics Foundations

**Goal:** Critically examine each Issue 01 finding against BOTH `ctl_pinn_resolution.md` AND `01-architecture-and-physics-foundations.md`...

**Target features:**
- Evidence packets for each issue before edits...
- Iterative re-verification: each finding moves through `PENDING -> IN_PROGRESS -> FIX_APPLIED -> VERIFIED` in `.planning/milestones/v1.4-phases/16-evidence-framework/16-ISSUE-LEDGER.md`; nothing closes on "fix applied," only on a passing acceptance check.
```

Only replace the stale ledger path in the target feature. Preserve the milestone framing.

**Decision log pattern** (lines 137-155):
```markdown
## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Resolution doc is NOT authoritative in v1.4 | The consolidated multi-AI resolution may contain errors... | - Active (v1.4) |
| Iterative re-verification protocol for v1.4 | Architecture/physics fixes will routinely need multiple attempts... | - Active (v1.4) |
```

Do not add new project decisions unless execution discovers a user-approved scope change. Phase 16 path reconciliation is already locked in context.

## Shared Patterns

### Markdown Tables
**Source:** `.planning/REQUIREMENTS.md` lines 86-125 and `16-VALIDATION.md` lines 37-47
**Apply to:** Ledger status table, protocol tables, packet source-position tables
```markdown
| Column | Column | Column |
|--------|--------|--------|
| Value | Value | Value |
```

### Frontmatter
**Source:** `.planning/STATE.md` lines 1-15 and `16-VALIDATION.md` lines 1-8
**Apply to:** `16-ISSUE-LEDGER.md`
```markdown
---
phase: 16
slug: evidence-framework-and-issue-adjudication
status: draft
created: 2026-05-16
---
```

### Evidence Citations
**Source:** `ctl_pinn_resolution.md` lines 202-219
**Apply to:** Evidence packet template and future packet references
```markdown
`ctl_instruction.md:L393-L399`; raw masses in `ctl_instruction.md:L452-L469`; raw masses in PINN residual at `pinn_architecture.md:L418-L430`.
```

### Lifecycle Discipline
**Source:** `.planning/ROADMAP.md` lines 86-96 and `.planning/REQUIREMENTS.md` line 57
**Apply to:** Ledger README and ledger per-finding notes
```markdown
PENDING -> IN_PROGRESS -> FIX_APPLIED -> VERIFIED
DEFERRED
```

`FIX_APPLIED` is not closure. `VERIFIED` requires a passing acceptance check. Regressed dependents return to `IN_PROGRESS`.

### Path Reconciliation
**Source:** `rg` scan of `.planning/ROADMAP.md`, `.planning/REQUIREMENTS.md`, `.planning/PROJECT.md`, `.planning/STATE.md`
**Apply to:** Locked edits in ROADMAP, REQUIREMENTS, PROJECT only
```markdown
old: .planning/milestones/v1.4-phases/16-evidence-framework/16-ISSUE-LEDGER.md
new: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md
```

Non-blocking warning for planner: `.planning/STATE.md` also contains the stale path at line 151, but Phase 16 context authorizes only ROADMAP, REQUIREMENTS, and PROJECT edits. Treat STATE as a workflow-state sync question, not an automatic implementation target.

### Scope Boundary
**Source:** `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md` and `16-RESEARCH.md`
**Apply to:** All Phase 16 tasks
```markdown
Do not edit framework specs.
Do not edit `pinn/` code.
Do not create evidence packets other than `evidence/_TEMPLATE.md`.
Do not adjudicate B-02, B-04, B-09, or M5 in Phase 16.
Do not build a ledger linter or executable acceptance-check suite.
```

## No Analog Found

No implementation target lacks a usable analog. `_TEMPLATE.md` has no exact evidence-packet predecessor, but `MIGRATION.md`, the issue finding tables, and `16-VALIDATION.md` provide sufficient fixed-schema, provenance, and verification patterns.

## Metadata

**Analog search scope:** `.planning/`, `pinn_instruction/issues/`, and `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/`
**Files scanned:** 50 Markdown/planning candidates via `rg --files`
**Strong analogs read:** 9 files
**Pattern extraction date:** 2026-05-16
**Dirty worktree note:** Existing unrelated changes were present before writing this file; only `16-PATTERNS.md` is created by this mapping step.
