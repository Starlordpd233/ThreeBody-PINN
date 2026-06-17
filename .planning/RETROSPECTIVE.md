# Project Retrospective

*A living document updated after each milestone. Lessons feed forward into future planning.*

## Milestone: v1.0 — Codebase Cleanup

**Shipped:** 2026-03-20
**Phases:** 4 | **Plans:** 10 | **Sessions:** 3

### What Was Built
- Consolidated IC folders from 4 to 2 (removed duplicate gold IC folders)
- Externalized raw ICs via `IC_RAW_DIR` environment variable
- Added 184-ID gold subset exclusion for standard quasi-random configurations
- Removed legacy directories (`old_templates/`, `brutus_simulation_documentation/`) and build artifacts
- Fixed all stale code imports, documentation references, and agent instruction file drift

### What Worked
- Strict phase ordering (code → docs → deletion) prevented broken references
- Wave-based parallelization of independent plans within phases
- Verification agents caught stale references that phase-level verifiers missed (Phase 4 gap closure)
- Archiving milestone artifacts kept ROADMAP.md and REQUIREMENTS.md at constant size

### What Was Inefficient
- Phase 4 (stale reference fixes) shouldn't have been needed — Phase 1 verifiers should have caught renamed file references in docs and agent files
- Agent instruction file drift (AGENTS.md diverging from CLAUDE.md) happened because Section 3.2 was updated in 3 of 4 files during Phase 2

### Patterns Established
- Phase ordering: code rewrites → documentation → destructive deletion (strict dependency)
- Agent instruction files must be updated identically (all 4 files, same section)
- Verification agents run after phase completion to catch cross-file reference drift
- Milestone archival: roadmap + requirements → `milestones/v{X}-*.md`, originals collapsed/deleted

### Key Lessons
1. Grep-based verification should run across ALL file types (code, docs, agent files) during phase verification, not just code
2. When renaming files, track both import references AND documentation filename mentions separately
3. Agent instruction files with duplicated sections (like Section 3.2) are a maintenance risk — one missed update creates drift

### Cost Observations
- Model mix: primarily sonnet (planning/execution), opus used for verification agents
- Sessions: 3 (spread across 2026-03-18 to 2026-03-20)
- Notable: 10 plans executed with zero regressions; Phase 4 was the only "rework" and it was pre-planned gap closure

---

## Milestone: v1.4 — Resolving 01 Architecture and Physics Foundations

**Shipped:** 2026-06-09
**Phases:** 8 | **Plans:** 26 | **Tasks:** 65

### What Was Built
- Evidence-backed adjudication and STOP-gap governance for every Issue 01 decision
- Coherent input/output, frame/gauge, sampling, physics/loss, architecture, and normalization contracts
- Five executable acceptance probes with recorded evidence and full requirement traceability
- FUT-01 implementation-divergence and FUT-05 author-comment handoffs
- A presentation-preserving cleanup pass with all milestone gates green

### What Worked
- The ledger lifecycle prevented `FIX_APPLIED` from being mistaken for completion
- Dependency-scoped STOP gaps allowed independent work to continue without inventing semantic decisions
- Phase-local verification plus the final milestone audit caught missing validation metadata and handoff links
- Keeping live `pinn/` code outside the grounding set prevented v1.3 assumptions from contaminating the v1.4 specs

### What Was Inefficient
- Several closure artifacts required late repair because plan-count and validation heuristics were not checked early enough
- Phase 20.5 naming and summary conventions needed remediation before GSD could resolve the phase correctly
- The generated milestone accomplishment list required manual consolidation because summary metadata was inconsistent across phases

### Patterns Established
- Candidate verdict sources are evidence, not authority
- Semantic and process-schema silence triggers the STOP protocol
- Acceptance checks must include executable evidence when the contract is empirically consequential
- Completed milestone phase directories move intact to `.planning/milestones/v{version}-phases/`

### Key Lessons
1. Validate GSD artifact naming and summary discovery at phase start, not only at milestone close.
2. Record acceptance commands, stdout, hashes, and pass criteria together so closure remains reproducible.
3. Keep future implementation divergence explicit and forward-pointing rather than treating old code as specification evidence.

### Cost Observations
- Model mix: not captured reliably
- Sessions: not captured reliably
- Notable: 198 branch commits produced 32/32 satisfied requirements, 8/8 verified phases, and 25/25 resolved STOP gaps.

---

## Milestone: v1.5 — Resolving 02 Data Pipeline and Validation

**Shipped:** 2026-06-17
**Phases:** 8 | **Plans:** 27

### What Was Built
- Research package that opened the external resolution-doc gate; empirical dataset verification with re-derivable probes (DATA-01..07, including a 70-file base-hierarchical rerun for DATA-05)
- Evidence-packet / EVID-10 root-cause adjudication machinery and the re-verification issue ledger; SCS-threshold, D=6.694, and M11/M12 conflicts adjudicated at root cause
- Locked DataLoader ingestion/selection contracts and sampling/precision/global-scale contracts in `ctl_instruction.md` / `pinn_architecture.md`
- Canonical SCS/SASD/IPR/PSC validation-metric contracts with training-loop usage deferred to doc-03
- Executed the 13-check acceptance suite (G1–G8 gate PASS), closed the 19-row ledger, reconciled SI dispositions, and produced the two-artifact FUT-01 handoff

### What Worked
- The v1.4 adjudication machinery (evidence packets, EVID-10, ledger lifecycle, STOP protocol) carried over cleanly and kept every decision grounded
- Running empirical verification (Phase 24) in parallel with the external research gate compressed the critical path
- The G1–G8 milestone-closure gate with fresh re-execution caught reconciliation drift (unchecked requirement checkboxes, stale traceability rows) before archive

### What Was Inefficient
- The milestone audit found unchecked DATA/PIPE checkboxes and stale Phase-24.5-gated traceability rows that should have been flipped at each phase close, not at the milestone audit
- Four phases (24, 25, 27, 28) lacked a phase-level VERIFICATION.md; the issue ledger carried verification, but this required an explicit audit interpretation
- The v1.5 learnings extraction (commit 01274c6) covered only phases 26-29; the phases 23-25 learnings and the audit file were left in a stash and had to be recovered at archive
- A concurrent-session phase-dir move staged probe-output files that the `outputs/*` policy blocks, stalling its commit until a coordinated takeover

### Patterns Established
- Candidate verdict sources remain evidence, not authority; the resolution doc was transcribed only where it survived empirical and first-principles checks
- Provisional thresholds (VAL-02/03/04) land with an explicit FUT-01/doc-03 recalibration forward-reference rather than blocking the milestone
- Gold is final in shape (117 validatable + 67 permanent-absent); the promotion cascade is a FUT-01 data-generation dependency, not a v1.5 closure blocker

### Key Lessons
1. Flip requirement checkboxes and advance traceability rows at each phase close, not deferred to the milestone audit.
2. A milestone learnings extraction must cover all phases in one pass, or the remainder lands in scratch and must be recovered at archive.
3. When two sessions share a worktree, a pre-commit hook rejection (e.g., `outputs/*` policy) can stall one agent indefinitely — serialize commits via the `agent-commit` lock and coordinate takeovers explicitly.

### Cost Observations
- Model mix: not captured reliably
- Sessions: many (v1.5 spanned 2026-06-10 to 2026-06-17 with concurrent sessions)
- Notable: 36/36 requirements, 8/8 phases, G1–G8 gate PASS, 10/10 STOP gaps resolved; audit verdict `tech_debt` with all 3 non-blocking items closed at archive.

---

## Cross-Milestone Trends

### Process Evolution

| Milestone | Sessions | Phases | Key Change |
|-----------|----------|--------|------------|
| v1.0 | 3 | 4 | Established GSD workflow: strict phase ordering, wave parallelization, post-phase verification |
| v1.4 | not captured | 8 | Added evidence adjudication, STOP-gap governance, executable acceptance checks, and archived phase history |
| v1.5 | not captured | 8 | Extended adjudication to data-pipeline/validation contracts; empirical dataset verification in parallel with the research gate; G1–G8 milestone-closure gate |

### Cumulative Quality

| Milestone | Plans | Verification Score | Regressions |
|-----------|-------|-------------------|-------------|
| v1.0 | 10 | 9/9 (Phase 4) | 0 |
| v1.4 | 26 | 32/32 requirements; 8/8 phases | 0 open at close |
| v1.5 | 27 | 36/36 requirements; 8/8 phases; G1–G8 gate PASS | 0 open at close |

### Top Lessons (Verified Across Milestones)

1. Strict phase dependency ordering (code → docs → deletion) prevents broken references
2. Post-phase verification agents catch what inline verifiers miss
3. Duplicated content across files (agent instruction sections) creates drift risk
4. Source-silent semantic decisions must stop for user instruction rather than being inferred
5. Executable acceptance evidence is part of the specification closure contract
