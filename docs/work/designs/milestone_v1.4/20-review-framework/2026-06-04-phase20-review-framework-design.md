---
status: consumed
purpose: other
created: 2026-06-04
milestone: v1.4
phase: 20-review-framework
retirement_trigger: milestone complete; superseded by subsequent work
---

# Phase 20 Plan Review Framework — Design

**Date:** 2026-06-04
**Topic:** phase20-plan-review
**Status:** Approved

## Architecture

**Method**: 4 parallel subagents via Workflow tool, each scoped to one review dimension. Each agent receives all 9 Phase 20 plan files as required reading plus a curated subset of governing source documents.

**Orchestration**: Fan out all 4 dimensions in parallel, collect findings, deduplicate cross-cutting issues, severity-classify, and write a single structured report.

**Pre-work**: Build a source manifest mapping every governing doc path to its relevance per dimension, so subagents read only what they need.

## Review Dimensions & Source Mapping

### Dimension 1: Correctness & Coherence
- Factual claims about SIREN (first_omega_0=30, hidden_omega_0=1, no scheduler) match sources
- LayerNorm contract claims (elementwise_affine=False, skip-path only, attribution) match sources
- I₃ definition/range consistency across all plans (known 3-way mismatch: obs #28-31)
- I_norm raw-vs-bounded naming follows D-05 without overstepping GAP-20-01 block
- M9/M10 "realized support" vocabulary follows D-06 user decision
- Internal contradictions across plans and 20-CONTEXT.md

**Sources**: `ctl_pinn_resolution.md`, `pinn_architecture.md`, `ctl_instruction.md`, `pinn_instruction/issues/01-architecture-and-physics-foundations.md`

### Dimension 2: Governance Compliance
- STOP protocol: GAP-20-01 OPEN, ARCH-04 blocked, no invented evidence vehicles
- Evidence-gating: correct Phase 16 ledger row and evidence packet references
- No-live-code directive: pinn/ code not treated as grounding source
- Cross-phase reframing: no silent scope changes
- Semantic decisions surfaced, not invented
- Gap classification accuracy

**Sources**: `AGENTS.md` CRITICAL GOVERNANCE block, `20-GAPS.md`, `v1.4-GAPS.md`

### Dimension 3: Cross-Phase Dependencies
- Wave concurrency: 20-01 through 20-04 concurrent feasibility, implicit file-edit conflicts
- Phase 18/19 dependencies: forward-reference accuracy, sampling_method.md line-number shift
- Phase 20.5 separation: boundary cleanliness
- Evidence packet dependencies: ledger rows vs packets needing creation
- Requirement/AC mapping: ARCH-01..05 → valid acceptance checks

**Sources**: `16-ISSUE-LEDGER.md`, `REQUIREMENTS.md`, `ROADMAP.md`, Phase 18/19 context files

### Dimension 4: Completeness & Improvement
- Acceptance criteria provability and specificity
- Task granularity and sizing
- Missing scope
- Clarity, organization, redundancy
- Discussion log completeness
- Research artifact readiness per D-08

**Sources**: Phase 20 plans only (internal quality)

## Finding Classification

| Severity | Definition | Action |
|----------|-----------|--------|
| CRITICAL | Factual error, governance violation, or execution blocker | Must fix before plans usable |
| SIGNIFICANT | Gap, ambiguity, or risk needing user decision | Should address |
| MINOR | Improvement, redundancy, clarity | Nice to fix |

**Finding schema**: Title, Dimension, Location (file:line), Summary, Evidence, Impact, Recommendation.

## Report Output

**Path**: `docs/work/reviews/milestone_v1.4/20-plan-audit-legacy/phase20-review.md` (absolute; directory already exists)

**Structure**:
1. Executive Summary
2. Methodology
3. CRITICAL Findings
4. SIGNIFICANT Findings
5. MINOR Findings / Improvements
6. Cross-Cutting Themes
7. Grey Areas for Discussion
8. Per-Plan Summary

## Execution Flow

1. Build source manifest
2. Dispatch 4 subagents in parallel via Workflow
3. Collect & deduplicate findings
4. Verify CRITICAL findings against sources
5. Write structured report
6. Commit atomically
