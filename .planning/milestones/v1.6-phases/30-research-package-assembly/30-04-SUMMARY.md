---
phase: 30-research-package-assembly
plan: 04
subsystem: docs
tags: [erw, specwork, doc-03, curriculum, training-loop, pkg-06, pkg-07, claims-register, framed-questions, scope-12]

# Dependency graph
requires:
  - phase: 30-03
    provides: "research_package/specs/ byte-for-byte snapshots, consolidated-context.md, verified-facts-reference.md (the grounding companions the framed questions cite by bare filename + section anchor)"
  - phase: 30-02
    provides: "D-09 APPROVED record — MULTI-COMPANION package form locked; ALM-clamp INCLUDED; no declined findings"
  - phase: 30-01
    provides: "30-CLAIMS-INVENTORY.md provisional seed (CLM-01..CLM-19); 30-REPORTS-CHARACTERIZATION.md"
provides:
  - "framed-research-questions.md — PKG-06 neutral framed questions in issue-03 section order, three named decisions + D conflict posed UNSETTLED with locked/open delineation"
  - "scope-12-hard-constraints.md — verbatim SCOPE-12 locked-outcomes preamble + non-literal SCOPE-10 override + locked-vs-revisable distinction"
  - "resolution-doc-skeleton.md — non-binding per-finding skeleton with finding→phase(32-36) map and v1.4/v1.5 format precedents"
  - "claims-register.md — uploaded grounding-class PKG-07 register (CLM-01..CLM-20) with verified-row v1.5 provenance and the D-17 boundary"
  - "30-CLAIMS-INVENTORY.md extended (no longer provisional): CLM-20 added, non-dataset exclusion note recorded"
affects: [30-05 master/prompt/delivery assembly, Phase 31 resolution-doc readiness verification, Phases 32-36 adjudication]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "MULTI-COMPANION ERW package: authored companions referenced by bare filename; zero repo paths in authored uploads"
    - "Neutral two-position framing (issue-doc position + spec position cited by bare filename + section anchor); no presupposed verdict"
    - "Locked/open delineation for contested values: SCOPE-12-locked sub-part fixed, only reconciliation under the locked value is open"
    - "Descriptive decision naming (F15): never internal D-04/D-05/D-06 numbering in upload-class files"

key-files:
  created:
    - "pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_package/framed-research-questions.md"
    - "pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_package/scope-12-hard-constraints.md"
    - "pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_package/resolution-doc-skeleton.md"
    - "pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_package/claims-register.md"
  modified:
    - ".planning/phases/30-research-package-assembly/30-CLAIMS-INVENTORY.md"

key-decisions:
  - "All framings posed neutrally with both positions; no contested finding settled and no locked value re-opened (STOP protocol honored — no gap)"
  - "Causal-training-mode question surfaces the spec/issue-doc divergence (spec baseline is PHYS-05 causal weighting with dense-residual ALM rejected; issue doc frames Option B global+ALM as current SOT) without resolving it"
  - "F6 register extension: added CLM-20 (M16 collocation-scaling factors); recorded an explicit non-dataset exclusion note for spec/design parameters (strict-criteria constants, τ_L split softening, μ_p clamp, clip factors, PHYS-05 schedule)"

patterns-established:
  - "Every inline CLM-NN in framed questions resolves to a row in the uploaded grounding-class claims-register.md (F1)"
  - "Grounding-class companion retains verified-row provenance citations by design (D-10) and is exempt from the strict master/prompt VC-01 grep"

requirements-completed: [PKG-06, PKG-07]

# Metrics
duration: ~45min
completed: 2026-06-18
---

# Phase 30 Plan 04: Framed Questions, SCOPE-12 Preamble, Skeleton, Claims Register Summary

**Authored the four upload companions for the doc-03 ERW package: 19 neutrally-framed research questions in issue-03 section order (three named decisions + the D conflict posed unsettled with locked/open delineation), the verbatim SCOPE-12 hard-constraints preamble, a non-binding per-finding resolution-doc skeleton, and the uploaded PKG-07 claims register — with the claims seed extended after the full issue-03 read.**

## Performance

- **Duration:** ~45 min
- **Completed:** 2026-06-18
- **Tasks:** 4
- **Files modified:** 5 (4 created, 1 extended)

## Accomplishments
- **PKG-06 framed questions** (`framed-research-questions.md`): one `### <finding>` section per item in issue-03 section order, covering B-07, B-08, M6, M7, M14, M15, M16, D5, NS-12, NS-13, NS-18 (each expanded to one question), the data-driven stage-assignment cluster, the ALM `μ_p`-clamp finding, the three named human-approval decisions, and the `D = 6.694` vs `D ≈ 4.6416` conflict. Each question states BOTH the issue-doc position AND the current framework-spec position, with the spec position cited by bare filename + section anchor (e.g. `ctl_instruction.md §2.5`, `pinn_architecture.md §4.4`). No verdict presupposed.
- **F5 locked/open delineation**: the D-conflict and epsilon-strategy questions each carry an explicit "LOCKED vs OPEN" block — the SCOPE-12-locked sub-part (`D ≈ 4.6416`; loss-side `eps_soft = 1e-5`) marked not-re-openable, the open question scoped to reconciliation/propagation under the locked value. Never framed as "which value is correct."
- **SCOPE-12 preamble** (`scope-12-hard-constraints.md`): the seven locked v1.4+v1.5 outcomes verbatim, the SCOPE-10 live-code override stated non-literally (the two `.py` files named bare, no path prefix), and the locked-vs-revisable distinction (SCOPE-13).
- **Non-binding skeleton** (`resolution-doc-skeleton.md`): one verdict slot per finding, the finding→adjudication-phase(32-36) map, v1.4/v1.5 resolution docs cited as format precedents only.
- **Uploaded claims register** (`claims-register.md`): grounding-class PKG-07 register (CLM-01..CLM-20), verified rows retaining their v1.5 provenance citations, the provenance-label convention note, and the D-17 no-in-milestone-verification boundary.
- **F6 extension**: `30-CLAIMS-INVENTORY.md` marked no-longer-provisional; added CLM-20 (M16 collocation-scaling factors) and a non-dataset exclusion note distinguishing spec/design parameters from registrable dataset figures.

## Task Commits

This plan ships as ONE atomic commit (per the orchestrator's commit protocol), not per-task commits:

1. **Task 1: SCOPE-12 hard-constraints preamble** — included in the atomic commit
2. **Task 2: framed research questions + register extension** — included in the atomic commit
3. **Task 3: non-binding resolution-doc skeleton** — included in the atomic commit
4. **Task 4: uploaded claims-register companion** — included in the atomic commit

**Atomic commit:** `docs(30-04): author framed questions, scope-12 preamble, skeleton, claims register`

## Files Created/Modified
- `research_package/framed-research-questions.md` — PKG-06 framed questions (issue-03 section order)
- `research_package/scope-12-hard-constraints.md` — SCOPE-12 verbatim preamble + non-literal SCOPE-10 override
- `research_package/resolution-doc-skeleton.md` — non-binding per-finding skeleton + finding→phase map
- `research_package/claims-register.md` — uploaded grounding-class PKG-07 register (CLM-01..CLM-20)
- `30-CLAIMS-INVENTORY.md` — extended (no longer provisional): CLM-20 + non-dataset exclusion note

## Decisions Made
- Surfaced (did not resolve) the causal-training-mode divergence: the current spec baseline is PHYS-05 causal weighting with dense-residual ALM explicitly rejected (`ctl_instruction.md`, `pinn_architecture.md §4.2`), whereas issue-03 frames Option B (global + ALM) as "current SOT." Both positions are stated; the question asks the research to reconcile, with no presupposed verdict.
- M6/M7 framed under the locked Phase-17 input contract: `L_norm` and `τ_L` are now metadata (not IC slots), so the questions confirm where the clamping/exclusion disciplines apply rather than re-asserting the IC-vector-mapping framing.
- Registered the M16 collocation-scaling factors as CLM-20 (claimed-unverified, derived from the verified `dt_out` CLM-17) and excluded spec/design numerical parameters from the register by design (D-15 scopes it to dataset/empirical figures).

## Deviations from Plan

None - plan executed exactly as written. All four task verifications, the coverage check, the VC-01 leak grep (three authored companions clean), the F5 delineation check, the F15 naming-discipline check (no D-04/05/06 in authored uploads), and the CLM-resolution cross-check all passed. The 30-03 specs/ snapshots and verified-facts-reference.md were not modified.

## Issues Encountered
None.

## STOP Protocol
No STOP-protocol gap encountered. Every framing is grounded: issue-doc positions read directly from `03-curriculum-and-training-loop.md`; framework-spec positions cited from the shipped snapshots by section anchor; locked sub-parts grounded in SCOPE-12 / CURR-02 / EVID-15 / the phase-local claims register. No semantic, process-schema, or cross-phase judgement call was required — both positions are stated and no contested finding is settled, so nothing was invented.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- The four authored companions are ready for 30-05 to reference by bare filename in `RESEARCH-CONTEXT-MASTER.md` and the `RESEARCH-AGENT-PROMPT.md` attach list.
- The selected-finding coverage set (≥ the SPEC-locked set, with NS-12/13/18 expanded and the ALM-clamp included) is ready for Phase 31's readiness checklist.
- No blockers.

---
*Phase: 30-research-package-assembly*
*Completed: 2026-06-18*
