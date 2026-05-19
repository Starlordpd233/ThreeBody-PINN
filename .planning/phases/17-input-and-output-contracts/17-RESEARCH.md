# Phase 17: Input and Output Contracts - Research

**Researched:** 2026-05-19 [VERIFIED: local date context]
**Domain:** CTL-PINN framework-spec input/output contract adjudication [VERIFIED: .planning/ROADMAP.md:137-148]
**Confidence:** HIGH for plan readiness after the 2026-05-19 gap-resolution batch; HIGH for locked D-01/D-02/D-03 facts. This file was originally researched while ten Phase 17 gaps were OPEN, but `17-GAPS.md` now records all ten as `RESOLVED-WITH-INSTRUCTION`. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:51-70; .planning/phases/17-input-and-output-contracts/17-GAPS.md:1-10]

> **Post-research update (2026-05-19):** The user instructed the agent to auto-advance without further user prompts. Phase 17 recorded that instruction by resolving GAP-17-01 through GAP-17-10 with each entry's agent-recommended option. Planner/executor agents should treat D-04 through D-14 as actionable unless they discover a new source-silent decision that triggers the STOP protocol.

<user_constraints>
## User Constraints (from CONTEXT.md)

All rows and bullets in this section are copied verbatim from `17-CONTEXT.md`; this section is the phase-specific constraint source for the planner. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:47-70; .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:174-179; .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:248-257]

### Locked Decisions

| Decision | Status | Linked gap(s) | Plan-phase / execute-phase action |
|----------|--------|---------------|-----------------------------------|
| **D-01** B-04 verdict = Option C (Jacobi-state IC₁₃) | ✅ LOCKED | — | Actionable. User-approved (Tier A1) + resolution-doc-grounded (`ctl_pinn_resolution.md:71–72, 459–465, 517–524`). |
| **D-02** IO-03 = hard COM projection head | ✅ LOCKED | — | Actionable. User-approved (Tier A2) + resolution-doc-grounded (`:687–720`). |
| **D-03** τ semantics fully locked: leaf=u, τ=2u−1 | ✅ LOCKED | — | Actionable. User-approved (Tier A3) + resolution-doc-grounded (`:209–250`). |
| **D-12** 3-plan decomposition: P01 input / P02 output / P03 cleanup | ✅ LOCKED | — | Actionable. User-approved. |
| **D-15** `pinn/STATUS.md` deferred to v1.4 ship; no physical move | ✅ LOCKED | — | Actionable. User-approved. |
| **D-16** Phase 16 amendment 2026-05-18 acknowledgement | ✅ LOCKED | — | Actionable. User-approved (amendment itself approved earlier). |

### Gated Decisions

| Decision | Status | Linked gap(s) | Plan-phase / execute-phase action |
|----------|--------|---------------|-----------------------------------|
| **D-04** IC composition primary in `ctl_instruction.md` | ⚠️ OPEN | GAP-17-06 | Do not act until resolved. Topical split was user-approved abstractly; specific topic→file assignment is gated. |
| **D-05** Network I/O width primary in `pinn_architecture.md` | ⚠️ OPEN | GAP-17-06 | Do not act until resolved (same gap as D-04). |
| **D-06** Per-slot tanh normalization form + symbolic μ/σ | ⚠️ PARTIAL | GAP-17-07 | Formula form is grounded (act on it). Numerical μ/σ statistics are gated — leave symbolic until GAP-17-07 resolves. |
| **D-07** Mass slots: ordered, raw, pre-normalization | ⚠️ OPEN | GAP-17-01 | Do not act until resolved. **HIGH-impact semantic gap** (raw vs fraction). |
| **D-08** Forward-ref to Phase 18 FRAME-01 | ⚠️ OPEN | GAP-17-08 | Coordination point is real; specific wording in framework specs is gated. |
| **D-09** Forward-ref to Phase 19 PHYS-02 | ⚠️ OPEN | GAP-17-09 | Same as D-08. |
| **D-10** M5 reframed to metadata-only under Jacobi IC | ⚠️ OPEN | GAP-17-05 | Do not act until resolved. **HIGH-impact cross-phase reframing** (changes Phase 20 scope). |
| **D-11** Forward-ref to Phase 21 VER-04 | ⚠️ OPEN | GAP-17-10 | Same as D-08/D-09. |
| **D-13** AC-IO-01/02/03 pass criteria + AC-IO-04 invention | ⚠️ OPEN | GAP-17-02, GAP-17-03 | AC name reservations from Phase 16 are grounded. AC-IO-04 invention is gated (GAP-17-02). Pass-criteria wording is gated (GAP-17-03). |
| **D-14** `17-CODE-DIVERGENCE.md` schema | ⚠️ OPEN | GAP-17-04 | Mechanism is user-approved; specific schema fields are gated. Do not create the file with the proposed schema until GAP-17-04 resolves. |

### the agent's Discretion

- Exact section-break placement of the IC₁₃ definition inside `ctl_instruction.md` Step 4 — preserve the existing section's flow; the IC vector is the natural sub-step.
- Exact wording of forward references to Phases 18/19/20 — must be unambiguous about which downstream phase locks the deferred concept, but specific phrasing is flexible.
- Whether to use a Markdown table or an enumerated list for the per-slot normalization formula in `ctl_instruction.md` — pick whichever reads cleaner in context.
- Exact ordering of evidence-packet sections (within the 12 required from `16-CONTEXT.md` D-06 of Phase 16) for B-03, B-06, M1, M2 (non-EVID-05 findings, so sections 5/7/8/9 of the template are skipped with `Not contested` markers).

### Deferred Ideas (OUT OF SCOPE)

- **Numerical acceptance probes for IO findings** — Phase 17 reserves AC-IO-01/02/03/04 with text/structural pass criteria (D-13). Phase 21 VER-04 may add disposable numeric probes (e.g., load a synthetic IC, compute the Jacobi state, verify the slot ordering and tanh normalization closes round-trip to ±1e-10). Out of Phase 17 scope.
- **`pinn/STATUS.md` archival marker file** — added at Phase 21 handoff per D-15, not during Phase 17. The accumulated `NN-CODE-DIVERGENCE.md` files from Phases 17/18/19/20 are its inputs.
- **Mass-fraction-vs-raw-mass rewrite of `pinn/data-processing-pipeline-full.py`** — FUT-01 work; Phase 17 records the divergence and the verdict (raw masses ordered with `tanh` normalization, not fractions). v1.4 does not edit code.
- **SI-CTL-001 / SI-PINN-001 retirement** — Phase 21 VER-06 retires these source-issue ledger entries with back-references to Phase 17's evidence packets. Phase 17 does NOT edit the `## Source Issues` sections of the framework specs (those edits happen in Phase 21's reconciliation step).
- **`I_3` and `I_norm` normalization-map adjudication (M5)** — Phase 20 ARCH-03 / ARCH-04, but now re-scoped per D-10: under Jacobi-state IC, these are metadata-only features; the contested formulas matter for curriculum-staging diagnostics, not network input.
- **Permutation-invariance discussion in `evidence/B-04.md` §5** — note that Jacobi coordinates impose a hierarchical body labeling that canonical ordering (Phase 18) makes deterministic. The body-label-asymmetry concern from sequentialthinking thought #9 is mentioned in the evidence packet but not resolved further in Phase 17 — Phase 18's canonical-ordering rule is the resolution.
- **Energy regularizer / HNN wording reconciliation (PHYS-04)** — Phase 19. The COM projection head locked here (D-02) automatically gives `Σ mᵢ vᵢ = 0` and `Σ mᵢ aᵢ = 0` for free; PHYS-04 in Phase 19 can rely on this when defining the energy-conservation regularizer rather than soft-enforcing momentum.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| IO-01 | Framework specs state one canonical network input contract: `14D = [tau, IC_13]`. [VERIFIED: .planning/REQUIREMENTS.md:22] | Resolution doc freezes width at one time scalar plus `IC13`; Phase 17 D-01/D-03 lock Jacobi `IC_13` and tau semantics. [VERIFIED: pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md:117-118; .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:53-55] |
| IO-02 | Framework specs define the 13-component IC vector in one consistent order with normalization rules. [VERIFIED: .planning/REQUIREMENTS.md:23] | Current Phase 17 context supersedes stale invariant/orientation-slot wording with the Jacobi-state `IC_13`; planner must not reintroduce angular-momentum, virial-ratio, shape-invariant, or velocity-angle slots as network inputs. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:78-82; pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md:514-530; .planning/REQUIREMENTS.md:23] |
| IO-03 | Framework specs distinguish position outputs from AD-derived velocities/accelerations and require mass-weighted COM projection before any output is consumed by a loss. [VERIFIED: .planning/REQUIREMENTS.md:24] | Resolution doc requires a 9D position-only raw head, hard mass-weighted COM projection before losses/metrics, and AD-derived velocities/accelerations after projection. [VERIFIED: pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md:687-719] |
| IO-04 | Obsolete 11D, 12D, or ambiguous 13D/14D wording is removed or labeled historical source-issue metadata. [VERIFIED: .planning/REQUIREMENTS.md:25] | Current target specs contain the stale 12D/11-component CTL passages and the 14D-but-wrong trig-angle architecture table that P03 must audit after P01/P02 edits. [VERIFIED: pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:669-676; pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:790-811; pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:812-815] |
| VER-05 | Each fix follows `PENDING -> IN_PROGRESS -> FIX_APPLIED -> VERIFIED`, and `FIX_APPLIED` is not closure. [VERIFIED: .planning/REQUIREMENTS.md:57] | Phase 16 evidence README and ledger require passing acceptance checks, status logs, and regression re-verification before phase exit. [VERIFIED: .planning/phases/16-evidence-framework-and-issue-adjudication/evidence/README.md:40-54; .planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md:44-54] |
</phase_requirements>

## Summary

Phase 17 is a documentation-adjudication phase, not an implementation phase: it edits framework specs and evidence/planning artifacts while treating `pinn/basic_architecture.py` and `pinn/data-processing-pipeline-full.py` as read-only live-code evidence. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:23-40; .planning/REQUIREMENTS.md:67-74]

The highest-confidence contract facts are: input width remains `14D = [tau, IC_13]`; `IC_13` is the reconstructive gauge-fixed Jacobi state; network output is 9D positions only; a hard mass-weighted COM projection is applied before losses/metrics; velocities and accelerations are AD-derived after projection; and autograd leaf semantics use `u=t/T` with `tau=2u-1` inside the wrapper. [VERIFIED: pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md:209-249; pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md:514-530; pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md:687-719]

Planning is now unblocked because `17-GAPS.md` records GAP-17-01 through GAP-17-10 as `RESOLVED-WITH-INSTRUCTION`; if any new source-silent decisions appear, the STOP protocol still applies. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:14-16; .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:49-70; .planning/phases/17-input-and-output-contracts/17-GAPS.md:1-10]

**Primary recommendation:** Draft the locked three-plan shape P01 input / P02 output / P03 cleanup. Do not add a Wave 0 gap-resolution gate for GAP-17-01 through GAP-17-10 because the user has resolved them; instead, include acceptance criteria that confirm the resolved choices are reflected in the plans and artifacts. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:137-143; .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:51-70]

## Project Constraints (from AGENTS.md)

- Phase 17 is governed by the v1.4 STOP protocol: do not invent content where source materials are silent or ambiguous, and stop affected work on non-grounded MUST-surface decisions. [VERIFIED: AGENTS.md:15-18]
- A decision is grounded only when explicitly answered by the resolution doc, issue doc, read-only SCOPE-01 live code, prior user decision, roadmap, or requirements entry. [VERIFIED: AGENTS.md:21-27]
- Semantic, process-artifact-schema, and cross-phase-reframing decisions must be surfaced rather than invented. [VERIFIED: AGENTS.md:28-35]
- Gap entries require decision point, artifact location, task context, classification, source silence, mathematical/engineering grounding, tempted choice, user decision options, confidence of impact, status, and resolution note. [VERIFIED: AGENTS.md:52-63]
- Subagents do not write gap registers directly; they return findings to the parent agent. [VERIFIED: AGENTS.md:69-72]
- Existing PINN implementation files are source-of-truth evidence for current v1.3 behavior, but v1.4 Phase 17 must not edit `pinn/` implementation files. [VERIFIED: AGENTS.md:107-114; .planning/REQUIREMENTS.md:71]

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Evidence packet creation for B-03/B-04/B-06/M1/M2 | Planning evidence layer | Framework specs | Phase 16 established one packet per finding under `evidence/{finding-id}.md`, and Phase 17 context requires evidence packets before spec edits. [VERIFIED: .planning/phases/16-evidence-framework-and-issue-adjudication/evidence/README.md:95-103; .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:217-220] |
| Canonical input contract | Framework spec layer | Planning ledger | Resolution doc defines `x=[tau,IC_13] in R^14`, while ledger rows B-03/M2 use `AC-IO-01` for dimensionality closure. [VERIFIED: pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md:527-530; .planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md:21; .planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md:29-30] |
| IC_13 composition and normalization | Framework spec layer | Read-only code evidence | Resolution doc defines the Jacobi-state IC and normalization formula, while live code documents the old mass-fraction/invariant/angle implementation as divergence evidence. [VERIFIED: pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md:514-572; pinn/data-processing-pipeline-full.py:1088-1146] |
| Output contract and COM projection | Framework spec layer | Read-only architecture evidence | Resolution doc requires COM projection before output consumption; live architecture currently emits final-layer outputs and only optionally transforms them. [VERIFIED: pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md:687-719; pinn/basic_architecture.py:185-192] |
| Obsolete-dimension cleanup | Framework spec layer | Planning validation layer | Target specs contain stale 11D/12D/ambiguous 14D passages, and IO-04 requires removal or historical labeling. [VERIFIED: pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:676; pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:801-811; pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:876-883; .planning/REQUIREMENTS.md:25] |
| Code-divergence handoff | Planning handoff layer | Future implementation layer | Phase 17 records spec-vs-live-code gaps for FUT-01 and must not patch `pinn/` during v1.4. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:151-164; .planning/REQUIREMENTS.md:60-64; .planning/REQUIREMENTS.md:71] |

## Standard Stack

### Core

| Library / Tool | Version | Purpose | Why Standard |
|----------------|---------|---------|--------------|
| Markdown planning artifacts | n/a | Store `17-RESEARCH.md`, future `17-NN-PLAN.md`, evidence packets, ledger updates, and verification records. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:223-225] | Existing GSD phases use Markdown artifacts with frontmatter, fixed tables, and shell-verifiable structure. [VERIFIED: .planning/phases/16-evidence-framework-and-issue-adjudication/16-PATTERNS.md:21-52] |
| Phase 16 evidence template | n/a | Seed `evidence/B-03.md`, `evidence/B-04.md`, `evidence/B-06.md`, `evidence/M1.md`, and `evidence/M2.md`. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:217-220] | Template requires both primary source positions, spec evidence, code evidence, EVID-05 sections, verdict, AC-ID, and status log. [VERIFIED: .planning/phases/16-evidence-framework-and-issue-adjudication/evidence/_TEMPLATE.md:17-100] |
| Phase 16 issue ledger | n/a | Track finding statuses, AC-IDs, dependents, and transition logs. [VERIFIED: .planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md:15-38] | VER-05 requires lifecycle and regression handling through the ledger. [VERIFIED: .planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md:44-54] |
| `rg` | 15.1.0 | Run fast structural searches over spec text and evidence artifacts. [VERIFIED: local command 2026-05-19] | Phase 16 validation uses grep-style doc-structure checks as the standard for documentation governance. [VERIFIED: .planning/phases/16-evidence-framework-and-issue-adjudication/16-VALIDATION.md:16-24; .planning/phases/16-evidence-framework-and-issue-adjudication/16-VALIDATION.md:37-47] |

### Supporting

| Library / Tool | Version | Purpose | When to Use |
|----------------|---------|---------|-------------|
| `git` | 2.50.1 | Inspect dirty state and support status-transition commit references if the executor commits. [VERIFIED: local command 2026-05-19] | Use before/after plan execution to avoid mixing unrelated changes into ledger/status updates. [VERIFIED: .planning/phases/16-evidence-framework-and-issue-adjudication/16-01-SUMMARY.md:38-42] |
| `gsd-sdk` | 1.42.3 | Load phase metadata and commit docs when the orchestrator authorizes commits. [VERIFIED: local command 2026-05-19] | Use for phase init and optional GSD commit flow; this research file was written without committing. [VERIFIED: local command 2026-05-19] |
| `python3` | 3.12.2 | Run standalone repository validation scripts when relevant. [VERIFIED: local command 2026-05-19] | Existing tests include a standalone Phase 12 validation script with `python3 tests/test_phase12_validation.py`, but Phase 17 should prefer doc-structure shell checks unless a new script is explicitly planned. [VERIFIED: tests/test_phase12_validation.py:1-7; tests/test_phase12_validation.py:250-282] |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Phase 16 evidence template | Ad hoc evidence packet | Ad hoc packets can omit both-source citations or EVID-05 sections, which Phase 16 explicitly designed the template to prevent. [VERIFIED: .planning/phases/16-evidence-framework-and-issue-adjudication/evidence/_TEMPLATE.md:17-26; .planning/phases/16-evidence-framework-and-issue-adjudication/evidence/_TEMPLATE.md:44-78] |
| Phase 16 ledger | Separate Phase 17-only status table | Separate tables would duplicate lifecycle state outside the canonical ledger and risk conflicting status for B-03/B-04/B-06/M1/M2. [VERIFIED: .planning/phases/16-evidence-framework-and-issue-adjudication/evidence/README.md:3-13; .planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md:21-30] |
| Structural `rg` checks | Full numeric validation probes in Phase 17 | Numerical probes for IO findings are explicitly deferred to Phase 21 VER-04; Phase 17 should use text/structural checks unless the user resolves otherwise. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:40; .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:251] |

**Installation:** none; Phase 17 needs no new package installation. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:34-40; local command 2026-05-19]

**Version verification:** No npm package versions apply to this documentation phase; local tool versions were verified for `rg`, `git`, `gsd-sdk`, `node`, `python3`, and `sed`. [VERIFIED: local command 2026-05-19]

## Architecture Patterns

### System Architecture Diagram

```text
17-CONTEXT + 17-GAPS
        |
        v
Phase 16 evidence template + 16-ISSUE-LEDGER
        |
        v
P01 evidence packets (B-03/B-04/M1/M2)
        |
        v
Input-contract spec edits
        |
        v
P02 evidence packet (B-06)
        |
        v
Output-contract spec edits + COM projection wording
        |
        v
P03 structural audit of obsolete dimensions and code divergence
        |
        v
17-VERIFICATION / ledger VERIFIED or DEFERRED states
```

This data flow matches the locked P01/P02/P03 decomposition and Phase 16 requirement that packets and ledger transitions precede closure. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:137-143; .planning/phases/16-evidence-framework-and-issue-adjudication/evidence/README.md:95-103]

### Recommended Project Structure

```text
.planning/phases/17-input-and-output-contracts/
├── 17-RESEARCH.md             # this artifact [VERIFIED: gsd init output 2026-05-19]
├── 17-CONTEXT.md              # locked/gated decisions [VERIFIED: .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:1-16]
├── 17-GAPS.md                 # open STOP-protocol gates [VERIFIED: .planning/phases/17-input-and-output-contracts/17-GAPS.md:1-10]
├── 17-01-PLAN.md              # future P01 input contract plan [VERIFIED: .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:137-140]
├── 17-02-PLAN.md              # future P02 output contract plan [VERIFIED: .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:141-142]
├── 17-03-PLAN.md              # future P03 cleanup plan [VERIFIED: .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:142-143]
└── 17-CODE-DIVERGENCE.md      # gated by GAP-17-04 before creation [VERIFIED: .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:65-66]
```

### Pattern 1: Evidence Packet Before Spec Edit

**What:** Create or update the finding evidence packet, cite both primary sources, capture current-spec and live-code evidence, record verdict and AC-ID, then edit framework specs. [VERIFIED: .planning/phases/16-evidence-framework-and-issue-adjudication/evidence/README.md:95-103]

**When to use:** Use for P01 B-03/B-04/M1/M2 and P02 B-06 before any `ctl_instruction.md` or `pinn_architecture.md` edit. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:137-143; .planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md:21-30]

**Example:**

```bash
cp .planning/phases/16-evidence-framework-and-issue-adjudication/evidence/_TEMPLATE.md \
  .planning/phases/16-evidence-framework-and-issue-adjudication/evidence/B-04.md
rg -n "IC_\\{13\\}|Gauge-fixed Jacobi|Input Vector" \
  pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md \
  pinn_instruction/issues/01-architecture-and-physics-foundations.md
```

Source: Phase 16 packet start procedure and template source-position requirements. [VERIFIED: .planning/phases/16-evidence-framework-and-issue-adjudication/evidence/README.md:95-103; .planning/phases/16-evidence-framework-and-issue-adjudication/evidence/_TEMPLATE.md:17-26]

### Pattern 2: Locked Fact vs Gated Decision

**What:** Treat D-01/D-02/D-03/D-12/D-15/D-16 as actionable, D-06 formula-only as partially actionable, and D-04/D-05/D-07/D-08/D-09/D-10/D-11/D-13/D-14 as blocked until linked gaps are resolved. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:51-70]

**When to use:** Use in every plan task precondition so the planner does not accidentally execute a source-silent semantic or process decision. [VERIFIED: AGENTS.md:28-40; .planning/phases/17-input-and-output-contracts/17-GAPS.md:15-24]

**Example:**

```markdown
Precondition: GAP-17-01 resolved before changing mass-slot wording.
Precondition: GAP-17-06 resolved before assigning primary spec home for IC_13.
Precondition: GAP-17-04 resolved before creating 17-CODE-DIVERGENCE.md.
```

Source: Phase 17 decision status table and gap register. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:56-66; .planning/phases/17-input-and-output-contracts/17-GAPS.md:26-180]

### Pattern 3: Structural Validation with Grep

**What:** Verify presence of canonical phrases and absence of unqualified stale phrases using `rg` after each plan batch. [VERIFIED: .planning/phases/16-evidence-framework-and-issue-adjudication/16-VALIDATION.md:28-47]

**When to use:** Use for IO-01 through IO-04 because Phase 17 acceptance is text/structural and Phase 21 owns numeric probes. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:145-149; .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:251]

**Example:**

```bash
rg -n "12D input vector|12-dimensional input vector|11-component IC|outputs.*velocities|5 values for 3 trigonometrically encoded angles" \
  pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md \
  pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md
```

Source: Current stale passages and Phase 16 validation style. [VERIFIED: pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:676; pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:801-811; pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:876-883; pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:812-815; .planning/phases/16-evidence-framework-and-issue-adjudication/16-VALIDATION.md:20-24]

### Anti-Patterns to Avoid

- **Using stale requirements text as the IC contract:** `REQUIREMENTS.md` IO-02 and `ROADMAP.md` success criterion 2 still describe the old invariant/orientation-slot framing, while `17-CONTEXT.md` D-01 locks the Jacobi-state IC_13. [VERIFIED: .planning/REQUIREMENTS.md:23; .planning/ROADMAP.md:144-146; .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:78-82]
- **Patching `pinn/` to match the spec:** SCOPE-01 forbids existing `pinn/` implementation edits in v1.4; record divergences for FUT-01 instead. [VERIFIED: .planning/REQUIREMENTS.md:71; .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:153-164]
- **Treating the resolution doc as unquestionable authority:** The project policy says neither primary source is authoritative, even though Phase 17 uses the resolution doc as the default candidate verdict source. [VERIFIED: .planning/PROJECT.md:74-88; .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:74-76]
- **Creating AC-IO-04 or divergence schema before gap resolution:** GAP-17-02 and GAP-17-04 gate those process artifacts. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:65-66; .planning/phases/17-input-and-output-contracts/17-GAPS.md:144-252]
- **Leaving velocity-output confusion in CTL prose:** `ctl_instruction.md` currently says the network outputs positions and velocities, contradicting the position-only contract. [VERIFIED: pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:880-883; pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md:73-77]

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Evidence schema | Custom packet headings | Phase 16 `_TEMPLATE.md` | The template already encodes both-source citation, EVID-05 sections, verdict enum, before/after note, AC-ID, and status log. [VERIFIED: .planning/phases/16-evidence-framework-and-issue-adjudication/evidence/_TEMPLATE.md:1-100] |
| Finding lifecycle | New Phase 17 status table | `16-ISSUE-LEDGER.md` | Ledger rows already exist for B-03, B-04, B-06, M1, and M2 with AC-IDs and dependents. [VERIFIED: .planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md:21-30] |
| Gap handling | Informal TODOs | `17-GAPS.md` and STOP protocol | Gap entries already carry source silence, grounding, user options, and OPEN status. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-GAPS.md:15-24; AGENTS.md:52-72] |
| Input vector semantics | Custom invariant/angle hybrid | Resolution-doc Jacobi-state IC_13, subject to locked/gated context | Resolution doc rejects invariant-only IC as final input and defines the network-facing Jacobi-state IC_13. [VERIFIED: pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md:459-465; pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md:514-530] |
| COM enforcement | Soft loss-only COM correction | Hard mass-weighted COM projection head | Resolution doc projects raw 9D positions before all losses/metrics and gets position, velocity, and acceleration COM constraints by construction/AD. [VERIFIED: pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md:695-719] |

**Key insight:** The hard work is not inventing a clever representation; the hard work is preserving the already-adjudicated contract while refusing to fill the open gaps silently. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:70-76; AGENTS.md:15-18]

## Runtime State Inventory

| Category | Items Found | Action Required |
|----------|-------------|------------------|
| Stored data | None found in Phase 17 scope; Phase 17 edits specs/evidence/planning artifacts and does not mutate datasets. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:34-40; .planning/REQUIREMENTS.md:71-74] | None for Phase 17; FUT-01 handles code/data-pipeline alignment after v1.4. [VERIFIED: .planning/REQUIREMENTS.md:60-64] |
| Live service config | None found; no external services are in Phase 17 scope. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:34-40] | None. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:34-40] |
| OS-registered state | None found; Phase 17 has no launchd/systemd/pm2/task registration surface. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:34-40] | None. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:34-40] |
| Secrets/env vars | None found for Phase 17; no secret or environment-variable rename is required by the contract edits. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:34-40] | None. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:34-40] |
| Build artifacts | None found for Phase 17; no build or installed package artifact carries the spec wording. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:34-40] | None. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:34-40] |

## Common Pitfalls

### Pitfall 1: Acting on OPEN Decisions

**What goes wrong:** A plan writes spec text for mass encoding, topic-to-file ownership, AC pass criteria, forward references, or divergence schema before the linked gap is resolved. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:56-66]

**Why it happens:** The context preserves proposed decision content below the status table, so it is easy to copy a tempting proposal while missing the OPEN gate. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:70-72]

**How to avoid:** Put explicit preconditions on each task for GAP-17-01 through GAP-17-10 as applicable. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-GAPS.md:1-24]

**Warning signs:** Plan text says "D-07 raw masses" or "AC-IO-04" as executable work while the linked gap remains OPEN. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:59; .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:65]

### Pitfall 2: Letting Old IO-02 Wording Override D-01

**What goes wrong:** The planner reintroduces angular momentum, virial ratio, minimum separation, inertia, shape invariants, or velocity-orientation scalars as network IC slots because `REQUIREMENTS.md` and `ROADMAP.md` still mention that older framing. [VERIFIED: .planning/REQUIREMENTS.md:23; .planning/ROADMAP.md:144-146]

**Why it happens:** `17-CONTEXT.md` is newer than `REQUIREMENTS.md` and locks the Jacobi-state IC_13, but the older requirement wording was not amended. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:3-5; .planning/REQUIREMENTS.md:129-130; .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:78-82]

**How to avoid:** Treat D-01 as the Phase 17 contract and treat the old IO-02/roadmap slot list as stale planning-context drift unless the user explicitly asks to amend requirements. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:53; .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:78-82]

**Warning signs:** Evidence or spec text describes "5 values for 3 trigonometrically encoded angles" or "shape invariants + direction cosines" as the final model input. [VERIFIED: pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:812-815; pinn_instruction/issues/01-architecture-and-physics-foundations.md:499-527]

### Pitfall 3: Using Live Code as the Target Instead of Evidence

**What goes wrong:** The plan aligns specs to the v1.3 live code's mass fractions, shape invariants, and velocity angles. [VERIFIED: pinn/data-processing-pipeline-full.py:1114-1146]

**Why it happens:** AGENTS says PINN input-vector logic in live code overrides comments for current-code evidence, but Phase 17 context says v1.4 specs supersede both live files for future implementation. [VERIFIED: AGENTS.md:107-114; .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:153-164]

**How to avoid:** Cite live code in evidence packets and divergence records, but write framework specs to the locked/gated Phase 17 target. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:151-164]

**Warning signs:** A proposed spec edit keeps `compute_velocity_angles` or `m_norm = 2 * (masses / m_total) - 1` as the future network input convention. [VERIFIED: pinn/data-processing-pipeline-full.py:1062-1085; pinn/data-processing-pipeline-full.py:1114-1116]

### Pitfall 4: Mistaking Positions+Velocities for Output Contract

**What goes wrong:** CTL training-loop prose continues saying the network outputs positions and velocities. [VERIFIED: pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:880-883]

**Why it happens:** `pinn_architecture.md` already says positions-only plus AD-derived kinematics, while `ctl_instruction.md` still has stale prose. [VERIFIED: pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:755-761; pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:880-883]

**How to avoid:** P02 must replace CTL's velocity-output claim with position-only plus AD-derived wording after the B-06 packet is created. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:141-142]

**Warning signs:** Any final Phase 17 grep still finds "network outputs ... velocities" in the two target spec files. [VERIFIED: local rg command 2026-05-19]

### Pitfall 5: Retiring `SI-*` Entries Too Early

**What goes wrong:** Phase 17 edits framework-spec source-issue sections to retire SI-CTL-001 or SI-PINN-* before Phase 21 VER-06. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:251-254]

**Why it happens:** IO-04 cleanup tempts broad source-issue cleanup, but the deferred ideas explicitly assign SI retirement to Phase 21. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:251-254; .planning/REQUIREMENTS.md:58]

**How to avoid:** Leave source-issue metadata sections untouched unless the user resolves otherwise. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:254]

**Warning signs:** A Phase 17 task edits `ctl_instruction.md` Source Issues or `pinn_architecture.md` Source Issues for retirement/back-reference rather than only contract body cleanup. [VERIFIED: pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1210-1218; pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:850-871]

## Code Examples

Verified patterns from project sources:

### Structural Stale-Wording Scan

```bash
rg -n "12D input vector|12-dimensional input vector|11-component IC|outputs.*velocities|5 values for 3 trigonometrically encoded angles" \
  pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md \
  pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md
```

Source: current stale passages and Phase 16 grep-validation pattern. [VERIFIED: pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:676; pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:801-811; pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:876-883; pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:812-815; .planning/phases/16-evidence-framework-and-issue-adjudication/16-VALIDATION.md:37-47]

### Evidence Packet Skeleton Creation

```bash
cp .planning/phases/16-evidence-framework-and-issue-adjudication/evidence/_TEMPLATE.md \
  .planning/phases/16-evidence-framework-and-issue-adjudication/evidence/B-04.md
```

Source: Phase 16 packet start procedure. [VERIFIED: .planning/phases/16-evidence-framework-and-issue-adjudication/evidence/README.md:95-103]

### Ledger Row Sanity Check

```bash
rg -n "^\\| (B-03|B-04|B-06|M1|M2) \\|" \
  .planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md
```

Source: Phase 16 ledger seeded rows for Phase 17 findings. [VERIFIED: .planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md:21-30]

### Source-Position Citation Search

```bash
rg -n "Final `IC13`|Gauge-fixed Jacobi|Output projection|Time spaces" \
  pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md
```

Source: source-position fields required by Phase 16 template. [VERIFIED: .planning/phases/16-evidence-framework-and-issue-adjudication/evidence/_TEMPLATE.md:17-26]

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Preserve 11/12D vs 13/14D source inconsistency as conversion metadata. [VERIFIED: .planning/PROJECT.md:151-152; pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1214-1218] | Reconcile Phase 17 framework specs to one canonical input/output contract. [VERIFIED: .planning/ROADMAP.md:137-148] | v1.4 Phase 17 after Phase 16 evidence framework. [VERIFIED: .planning/STATE.md:3-9; .planning/ROADMAP.md:101-102] | Specs become a coherent target for downstream phases and FUT-01. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:23-32] |
| Invariant-heavy `IC13` or trig/shape orientation slots as final network input. [VERIFIED: pinn_instruction/issues/01-architecture-and-physics-foundations.md:269-289; pinn_instruction/issues/01-architecture-and-physics-foundations.md:499-527] | Gauge-fixed Jacobi-state `IC_13` as final network input. [VERIFIED: pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md:514-530] | Locked in Phase 17 D-01. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:53; .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:78-82] | Old invariants remain metadata, not final input. [VERIFIED: pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md:574-588] |
| Position-output assumption without hard COM projection. [VERIFIED: pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:771-787] | Raw 9D position head followed by hard mass-weighted COM projection before losses/metrics. [VERIFIED: pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md:687-719] | Locked in Phase 17 D-02. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:54; .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:87-95] | COM constraints propagate to AD-derived velocities/accelerations. [VERIFIED: pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md:705-719] |

**Deprecated/outdated:**

- The CTL 11-component IC and 12-dimensional input claims are obsolete for Phase 17 planning. [VERIFIED: pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:790-811; .planning/REQUIREMENTS.md:25]
- The architecture table's "5 values for 3 trigonometrically encoded angles" is obsolete under the locked Jacobi-state IC_13. [VERIFIED: pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:812-815; .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:78-82]
- The CTL claim that the network outputs velocities is obsolete under the position-only output contract. [VERIFIED: pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:880-883; pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md:73-77]

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| - | No `[ASSUMED]` claims are used in this research; all substantive claims are tagged with verified local sources or command evidence. [VERIFIED: this RESEARCH.md] | All | Low; remaining uncertainty is represented as OPEN gaps rather than assumptions. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-GAPS.md:1-24] |

## Open Questions (RESOLVED)

| Item | What We Know | What's Unclear | Recommendation |
|------|--------------|----------------|----------------|
| GAP-17-01 | RESOLVED-WITH-INSTRUCTION: pre-tanh mass input is raw ordered mass. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-GAPS.md:67-68] | No unresolved question remains for Phase 17 planning. | Plans may use raw ordered mass wording directly. |
| GAP-17-02 | RESOLVED-WITH-INSTRUCTION: `AC-IO-04` is approved as a Phase 17-local acceptance check. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-GAPS.md:135-136] | No unresolved question remains for Phase 17 planning. | Plans may include AC-IO-04 as the IO-04 cleanup gate. |
| GAP-17-03 | RESOLVED-WITH-INSTRUCTION: proposed text/structural criteria for AC-IO-01/02/03 are approved. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-GAPS.md:169-170] | No unresolved question remains for Phase 17 planning. | Plans may use the approved criteria and must still enforce VER-05 lifecycle transitions. |
| GAP-17-04 | RESOLVED-WITH-INSTRUCTION: `17-CODE-DIVERGENCE.md` uses the five-column Markdown schema. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-GAPS.md:202-203] | No unresolved question remains for Phase 17 planning. | Plans may create the divergence inventory with Surface / Live code / Spec target / FUT-01 item / FUT-01 priority columns. |
| GAP-17-05 | RESOLVED-WITH-INSTRUCTION: Phase 20 M5 scope is staging metadata only under the Jacobi-state IC contract. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-GAPS.md:100-101] | No unresolved question remains for Phase 17 planning. | Plans may describe `I_3` as metadata-only while leaving Phase 20 formula work to Phase 20. |
| GAP-17-06 | RESOLVED-WITH-INSTRUCTION: the proposed topical split is confirmed. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-GAPS.md:233-234] | No unresolved question remains for Phase 17 planning. | Plans may make `ctl_instruction.md` primary for IC composition/normalization and `pinn_architecture.md` primary for network I/O. |
| GAP-17-07 | RESOLVED-WITH-INSTRUCTION: mu/sigma values remain symbolic in Phase 17. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-GAPS.md:262-263] | No unresolved question remains for Phase 17 planning. | Plans must not compute current-dataset numeric statistics in Phase 17. |
| GAP-17-08/09/10 | RESOLVED-WITH-INSTRUCTION: Phase 18 and Phase 19 names may appear inline; VER-04 appears only in planning artifacts. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-GAPS.md:289-324] | No unresolved question remains for Phase 17 planning. | Plans may include the resolved forward-reference wording. |
| Requirements/roadmap wording drift | `REQUIREMENTS.md` IO-02 and `ROADMAP.md` Phase 17 success criterion 2 still describe old invariant/orientation-slot content. [VERIFIED: .planning/REQUIREMENTS.md:23; .planning/ROADMAP.md:144-146] | Whether Phase 17 should amend planning docs to align with D-01 is not listed in D-12's plan decomposition. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:137-143] | Planner should not add planning-doc amendment tasks without surfacing this as a process-scope question. [VERIFIED: AGENTS.md:28-40] |

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|-------------|-----------|---------|----------|
| `rg` | Structural searches and validation checks | yes | 15.1.0 | `grep` if needed, but `rg` is available. [VERIFIED: local command 2026-05-19] |
| `git` | Dirty-state checks and optional commit SHA references | yes | 2.50.1 | No fallback needed. [VERIFIED: local command 2026-05-19] |
| `gsd-sdk` | Phase init and optional GSD commit flow | yes | 1.42.3 | Manual artifact write if SDK fails. [VERIFIED: local command 2026-05-19] |
| `node` | GSD graph tools if graph exists | yes | v22.22.1 | Skip graph context when no graph exists. [VERIFIED: local command 2026-05-19; local graph check 2026-05-19] |
| `python3` | Existing standalone validation scripts | yes | 3.12.2 | Shell-only checks for Phase 17 docs. [VERIFIED: local command 2026-05-19] |
| `pytest` | General Python test runner | no | - | Existing repo test script is standalone and Phase 17 validation should be shell/doc based. [VERIFIED: local command 2026-05-19; tests/test_phase12_validation.py:1-7] |

**Missing dependencies with no fallback:** none identified for Phase 17 research/planning. [VERIFIED: local command 2026-05-19]

**Missing dependencies with fallback:** `pytest` is unavailable, but Phase 17 does not need it because validation is doc-structure oriented. [VERIFIED: local command 2026-05-19; .planning/phases/16-evidence-framework-and-issue-adjudication/16-VALIDATION.md:16-24]

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | Custom shell/doc checks modeled on Phase 16. [VERIFIED: .planning/phases/16-evidence-framework-and-issue-adjudication/16-VALIDATION.md:16-24] |
| Config file | none detected outside reference-code; standalone `tests/test_phase12_validation.py` exists but is Phase 12-specific. [VERIFIED: local command 2026-05-19; tests/test_phase12_validation.py:1-7] |
| Quick run command | `rg -n "12D input vector|12-dimensional input vector|11-component IC|outputs.*velocities|5 values for 3 trigonometrically encoded angles" pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` [VERIFIED: local rg command 2026-05-19] |
| Full suite command | Phase 17 should combine stale-wording grep, canonical-contract presence grep, evidence packet existence checks, ledger status checks for B-03/B-04/B-06/M1/M2, and a no-`pinn/`-diff check. [VERIFIED: .planning/phases/16-evidence-framework-and-issue-adjudication/16-VALIDATION.md:37-47; .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:217-232] |

### Phase Requirements -> Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|--------------|
| IO-01 | One canonical `14D = [tau, IC_13]` contract across target specs. [VERIFIED: .planning/REQUIREMENTS.md:22] | doc-structure | `rg -n "14D|14-dimensional|\\[tau, IC_13\\]|IC_\\{13\\}" pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` [VERIFIED: Phase 16 validation pattern at .planning/phases/16-evidence-framework-and-issue-adjudication/16-VALIDATION.md:37-47] | yes, target specs exist. [VERIFIED: local rg command 2026-05-19] |
| IO-02 | IC_13 ordering and normalization align with locked/gated Phase 17 contract. [VERIFIED: .planning/REQUIREMENTS.md:23; .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:78-82] | doc-structure + packet completeness | `rg -n "rho|lambda|E\\^\\{in\\}|tanh|B-04|accept-resolution" .planning/phases/16-evidence-framework-and-issue-adjudication/evidence/B-04.md pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` after packet/spec files exist. [VERIFIED: pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md:514-572] | no, evidence packets are Wave 0 gaps. [VERIFIED: local file listing 2026-05-19] |
| IO-03 | Output is 9D positions only, COM projection exists, and velocities/accelerations are AD-derived. [VERIFIED: .planning/REQUIREMENTS.md:24] | doc-structure | `rg -n "9D|9-dimensional|COM projection|mass-weighted COM|velocities.*AD|accelerations.*AD" pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` [VERIFIED: pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md:687-719] | yes, target specs exist. [VERIFIED: local rg command 2026-05-19] |
| IO-04 | No unqualified 11D/12D/ambiguous 13D/14D wording remains except historical metadata. [VERIFIED: .planning/REQUIREMENTS.md:25] | negative doc-structure | `! rg -n "12D input vector|12-dimensional input vector|11-component IC|5 values for 3 trigonometrically encoded angles|outputs.*velocities" pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` after P03 cleanup. [VERIFIED: current stale matches at local rg command 2026-05-19] | yes, target specs exist. [VERIFIED: local rg command 2026-05-19] |
| VER-05 | Ledger status transitions and regression checks gate closure. [VERIFIED: .planning/REQUIREMENTS.md:57] | ledger-structure | `rg -n "^\\| (B-03|B-04|B-06|M1|M2) \\|" .planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md` plus per-finding transition-log checks. [VERIFIED: .planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md:21-30; .planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md:86-137; .planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md:179-199] | yes. [VERIFIED: local rg command 2026-05-19] |

### Sampling Rate

- **Per task commit:** Run the quick stale-wording scan plus the task-owned packet/spec/ledger grep. [VERIFIED: .planning/phases/16-evidence-framework-and-issue-adjudication/16-VALIDATION.md:28-33]
- **Per wave merge:** Run full doc-structure checks and ledger status checks for all Phase 17 in-scope findings. [VERIFIED: .planning/phases/16-evidence-framework-and-issue-adjudication/16-VALIDATION.md:28-33; .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:137-143]
- **Phase gate:** All in-scope findings must be `VERIFIED` or `DEFERRED` before exit. [VERIFIED: .planning/phases/16-evidence-framework-and-issue-adjudication/evidence/README.md:77-81]

### Wave 0 Gaps

- [ ] Resolve relevant `17-GAPS.md` entries before executable spec edits. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:49-70]
- [ ] Create/fill `evidence/B-03.md`, `evidence/B-04.md`, `evidence/B-06.md`, `evidence/M1.md`, and `evidence/M2.md` before or during the owning plans. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:217-220; local file listing 2026-05-19]
- [ ] Create `17-VALIDATION.md` or equivalent phase-local verification artifact if the planner wants Nyquist-style tracking for Phase 17. [VERIFIED: .planning/config.json:1-10; .planning/phases/16-evidence-framework-and-issue-adjudication/16-VALIDATION.md:1-24]
- [ ] Decide whether to amend stale `REQUIREMENTS.md`/`ROADMAP.md` IO-02 language or leave it as known planning drift; this is not in locked D-12. [VERIFIED: .planning/REQUIREMENTS.md:23; .planning/ROADMAP.md:144-146; .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:137-143]

## Security Domain

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|------------------|
| V2 Authentication | no | No authentication surface is introduced by Phase 17 docs-only edits. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:34-40] |
| V3 Session Management | no | No sessions or cookies are introduced. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:34-40] |
| V4 Access Control | no | No runtime authorization path is introduced. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:34-40] |
| V5 Input Validation | yes | Validate evidence/spec inputs through line-range citations, both-source checks, STOP protocol, and grep-based structural assertions. [VERIFIED: .planning/phases/16-evidence-framework-and-issue-adjudication/evidence/_TEMPLATE.md:17-48; AGENTS.md:21-40] |
| V6 Cryptography | no | No cryptographic operation or secret handling is introduced. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:34-40] |

### Known Threat Patterns for Phase 17 Documentation Governance

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Source-authority spoofing by treating one issue source as authoritative | Spoofing | Cite both primary sources before verdict and preserve "neither authoritative" policy. [VERIFIED: .planning/phases/16-evidence-framework-and-issue-adjudication/evidence/README.md:15-24] |
| Silent invention in source-silent semantic/process areas | Tampering | Apply STOP protocol and use `17-GAPS.md` rather than inventing. [VERIFIED: AGENTS.md:28-40; .planning/phases/17-input-and-output-contracts/17-GAPS.md:15-24] |
| Premature closure after spec edit | Repudiation | `FIX_APPLIED` is not closure; `VERIFIED` requires a passing acceptance check and ledger transition. [VERIFIED: .planning/phases/16-evidence-framework-and-issue-adjudication/evidence/README.md:40-54] |
| Regressing a previously verified dependent contract | Tampering | Re-run dependent acceptance checks after each batch. [VERIFIED: .planning/phases/16-evidence-framework-and-issue-adjudication/evidence/README.md:69-75] |

## Sources

### Primary (HIGH confidence)

- `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md` - checked final decision matrix, time spaces, Jacobi IC_13, normalization, metadata, and COM projection. [VERIFIED: pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md:112-129; pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md:209-249; pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md:459-572; pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md:576-636; pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md:687-719]
- `pinn_instruction/issues/01-architecture-and-physics-foundations.md` - checked Option A and Option B input-vector proposals. [VERIFIED: pinn_instruction/issues/01-architecture-and-physics-foundations.md:269-289; pinn_instruction/issues/01-architecture-and-physics-foundations.md:422-468; pinn_instruction/issues/01-architecture-and-physics-foundations.md:499-579]
- `pinn/basic_architecture.py` - checked current input/output dims, drifted docstring, raw final output path, and raw time derivative path. [VERIFIED: pinn/basic_architecture.py:97-104; pinn/basic_architecture.py:152-163; pinn/basic_architecture.py:185-192; pinn/basic_architecture.py:209-220]
- `pinn/data-processing-pipeline-full.py` - checked current shape invariants, velocity angles, mass fractions, IC vector assembly, and ordering wrapper. [VERIFIED: pinn/data-processing-pipeline-full.py:1036-1085; pinn/data-processing-pipeline-full.py:1088-1146; pinn/data-processing-pipeline-full.py:1149-1184]
- `AGENTS.md` - checked v1.4 STOP protocol and source-grounding rules. [VERIFIED: AGENTS.md:15-78]

### Secondary (MEDIUM-HIGH confidence)

- `.planning/phases/17-input-and-output-contracts/17-CONTEXT.md` - checked Phase 17 locked/gated decisions, plan decomposition, source references, and deferred scope. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:1-16; .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:47-70; .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:137-164; .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:248-257]
- `.planning/phases/17-input-and-output-contracts/17-GAPS.md` - checked ten open gap entries and their classifications. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-GAPS.md:1-24]
- `.planning/phases/16-evidence-framework-and-issue-adjudication/evidence/README.md` and `_TEMPLATE.md` - checked evidence workflow, template schema, verdict/status enums, and packet start procedure. [VERIFIED: .planning/phases/16-evidence-framework-and-issue-adjudication/evidence/README.md:1-107; .planning/phases/16-evidence-framework-and-issue-adjudication/evidence/_TEMPLATE.md:1-100]
- `.planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md` - checked seeded Phase 17 finding rows and lifecycle rules. [VERIFIED: .planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md:15-38; .planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md:44-58; .planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md:86-137; .planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md:179-199]
- `.planning/REQUIREMENTS.md`, `.planning/ROADMAP.md`, `.planning/PROJECT.md`, `.planning/STATE.md` - checked v1.4 requirements, phase scope, milestone policy, and active state. [VERIFIED: .planning/REQUIREMENTS.md:1-130; .planning/ROADMAP.md:82-150; .planning/PROJECT.md:72-97; .planning/STATE.md:1-24]

### Tertiary (LOW confidence)

- None used; no web-only or assumed external sources were used. [VERIFIED: this RESEARCH.md]

## Metadata

**Confidence breakdown:**

- Standard stack: HIGH - Phase 16 artifacts and local tool availability are verified directly. [VERIFIED: .planning/phases/16-evidence-framework-and-issue-adjudication/evidence/README.md:1-107; local command 2026-05-19]
- Architecture: HIGH for locked contract facts; MEDIUM for executable task sequencing because open gaps gate where and how edits land. [VERIFIED: pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md:514-530; pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md:687-719; .planning/phases/17-input-and-output-contracts/17-CONTEXT.md:51-70]
- Pitfalls: HIGH - pitfalls are directly visible in current target specs, Phase 17 gaps, and Phase 16 governance artifacts. [VERIFIED: pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:676; pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:801-811; pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:876-883; .planning/phases/17-input-and-output-contracts/17-GAPS.md:1-24]

**Research date:** 2026-05-19 [VERIFIED: local date context]
**Valid until:** 2026-06-02 or until any GAP-17 entry is resolved, whichever comes first. [VERIFIED: .planning/phases/17-input-and-output-contracts/17-GAPS.md:1-10]
