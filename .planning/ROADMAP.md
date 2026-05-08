# Roadmap: 3-Body Problem Physics-Inspired LLM

## Milestones

- ✅ **v1.0 Codebase Cleanup** — Phases 1–4 (shipped 2026-03-20)
- ✅ **v1.1 LaTeX Modularization Verification** — Phases 5–8 (shipped 2026-03-22)
- 🔄 **v1.2 PINN Implementation Readiness** — Phase 9 (in progress)
- ✅ **v1.3 Markdown Conversion Verification & Correction** — Phases 10–15 (shipped 2026-05-06)

## Phases

<details>
<summary>✅ v1.0 Codebase Cleanup (Phases 1–4) — SHIPPED 2026-03-20</summary>

- [x] Phase 1: Code Rewrites and Validation (3/3 plans) — completed 2026-03-18
- [x] Phase 2: Documentation Updates (3/3 plans) — completed 2026-03-19
- [x] Phase 3: Data Deletion and Legacy Cleanup (2/2 plans) — completed 2026-03-19
- [x] Phase 4: Stale Reference Fixes (2/2 plans) — completed 2026-03-20

Full details: `.planning/milestones/v1.0-ROADMAP.md`

</details>

<details>
<summary>✅ v1.1 LaTeX Modularization Verification (Phases 5–8) — SHIPPED 2026-03-22</summary>

- [x] **Phase 5: Content Completeness Verification** — Automated diff confirms no content lost across all 5 structures (completed 2026-03-21)
- [x] **Phase 6: Preamble Parity Verification** — Package, macro, and command declarations match between original and modular preambles (completed 2026-03-21)
- [x] **Phase 7: Structure Fidelity Verification** — Section hierarchy, labels, references, citations, and floats preserved (completed 2026-03-21)
- [x] **Phase 8: Compilability Verification** — All 5 modular structures compile cleanly with 0 errors and 0 new warnings (completed 2026-03-22)

</details>

<details>
<summary>🔄 v1.2 PINN Implementation Readiness (Phase 9) — IN PROGRESS</summary>

### Phase 9: Issues Directory Consolidation

**Goal:** Reorganize 7 scattered issue reports into 2–3 thematic documents eliminating duplication
**Depends on**: None
**Requirements**: CONSOL-01, CONSOL-02, CONSOL-03
**Success Criteria:**
  1. All 7 existing files merged into 2–3 new thematic files
  2. No unique findings lost in consolidation
  3. Each thematic document has distinct purpose with no overlapping coverage
  4. Original files archived or deleted with migration note

**Plans**: 3 plans
- [ ] 09-01-PLAN.md
- [ ] 09-02-PLAN.md
- [ ] 09-03-PLAN.md

</details>

<details>
<summary>✅ v1.3 Markdown Conversion Verification & Correction (Phases 10–15) — SHIPPED 2026-05-06</summary>

**Milestone Goal:** Verify every markdown conversion against its LaTeX source section-by-section, fix all errors to achieve one-to-one injection fidelity, and produce one authoritative `.md` file per source document.

- [x] **Phase 10: CTL-Instruction Verification** — 8 sections + appendix, 3 markdown candidates, heavy math — completed 2026-05-02
- [x] **Phase 11: Data-Quality-Assessment Verification** — 7 sections, 2 markdown candidates, cross-reference heavy — completed 2026-05-05
- [x] **Phase 12: PINN-Architecture Verification** — 7 active + 3 inactive sections, 3 markdown candidates, comment exclusion — completed 2026-05-05
- [x] **Phase 13: Review-of-Framework Verification** — 7 sections, 1 pandoc candidate, sub-document structure — completed 2026-05-05
- [x] **Phase 14: Stage-Strategy-Revision Verification** — 6 sections, 1 pandoc candidate, table normalization — completed 2026-05-05
- [x] **Phase 15: Sampling-Method Verification** — Monolithic source, 2 markdown candidates — completed 2026-05-06
- [x] **Phase 15.1: Markdown Conversion Correction** (INSERTED) — Resolve critical conversion errors and structural issues from v1.3 review reports (phases 10-15) to produce authoritative markdown files for handoff. New issues discovered after this scope are handled via GSD workflow, not this phase. — completed 2026-05-08

Full details: `.planning/milestones/v1.3-ROADMAP.md`

</details>

## Progress

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 1. Code Rewrites and Validation | v1.0 | 3/3 | Complete | 2026-03-18 |
| 2. Documentation Updates | v1.0 | 3/3 | Complete | 2026-03-19 |
| 3. Data Deletion and Legacy Cleanup | v1.0 | 2/2 | Complete | 2026-03-19 |
| 4. Stale Reference Fixes | v1.0 | 2/2 | Complete | 2026-03-20 |
| 5. Content Completeness Verification | v1.1 | 1/1 | Complete | 2026-03-21 |
| 6. Preamble Parity Verification | v1.1 | 1/1 | Complete | 2026-03-21 |
| 7. Structure Fidelity Verification | v1.1 | 2/2 | Complete | 2026-03-21 |
| 8. Compilability Verification | v1.1 | 1/1 | Complete | 2026-03-22 |
| 9. Issues Directory Consolidation | v1.2 | 0/3 | Not Started | — |
| 10. CTL-Instruction Verification | v1.3 | 3/3 | Complete | 2026-05-02 |
| 11. Data-Quality-Assessment Verification | v1.3 | 3/3 | Complete | 2026-05-05 |
| 12. PINN-Architecture Verification | v1.3 | 3/3 | Complete | 2026-05-05 |
| 13. Review-of-Framework Verification | v1.3 | 3/3 | Complete | 2026-05-05 |
| 14. Stage-Strategy-Revision Verification | v1.3 | 3/3 | Complete | 2026-05-05 |
| 15. Sampling-Method Verification | v1.3 | 3/3 | Complete | 2026-05-06 |
| 15.1 Markdown Conversion Correction | v1.3 | 3/3 | Complete | 2026-05-08 |

---
*Last updated: 2026-05-08 — Phase 15.1 complete*
