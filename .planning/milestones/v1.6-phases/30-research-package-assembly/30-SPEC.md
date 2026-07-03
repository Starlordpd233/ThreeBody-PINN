# Phase 30: Research Package Assembly — Specification

**Created:** 2026-06-17
**Ambiguity score:** 0.105 (gate: ≤ 0.20)
**Requirements:** 6 locked (PKG-05, PKG-06, PKG-07, PKG-08, the non-binding resolution-doc skeleton, and an operational delivery / gate-open requirement)
**Branch:** `milestone/v1.6` (isolated worktree `../3_body_problem-v1.6`)

## Goal

Deliver a complete, self-contained, ERW-conformant external-research package for issue-03 (curriculum + training loop) — an annotated document list, neutrally-framed research questions, a claimed-vs-verified figure register, a non-binding per-finding resolution-doc skeleton, and a read-only characterization of the two curriculum-relevant research reports — and hand it off to the user; on delivery the external resolution-doc gate opens (the user's multi-AI ERW research begins). The package assembles and frames existing materials only; it performs no adjudication, no empirical verification, and no framework-spec edits.

## Background

Grounded in the `milestone/v1.6` worktree as of HEAD `85f72f8`:

- **The subject exists, non-authoritative.** `pinn_instruction/issues/03-curriculum-and-training-loop.md` (711 lines) consolidates the 2026-04-27 audit (§§6–7), the Causal Training Mismatch blueprint, the stage-assignment methodology, and `next steps.txt` fragments. It carries known tensions — `D = 6.694` against the v1.5-locked raw-mass `D ≈ 4.6416`, and "Canonical" citations of `pinn/` live code that are overridden (SCOPE-10).
- **The two spec-edit targets exist** (intact package inputs): `framework-specs/ctl_instruction.md` (1868 lines), `framework-specs/pinn_architecture.md` (1013 lines).
- **The two PKG-08 characterization subjects exist:** `framework-revisions/review-of-framework/review_of_framework.md` and `framework-revisions/stage-strat-revision/stage_strat_revision.md`.
- **The gate is closed.** `framework-revisions/research_reports/` holds only `01-architecture-and-physics-foundations/` and `02-data-pipeline-and-validation/`; the doc-03 directory does not exist, so the external resolution doc is absent (as expected at milestone start).
- **No package exists yet.** The canonical assembly spec is the **ERW runbook** (`docs/runbooks/external-research/2026-06-11-external-research-workflow.md`). The direct precedent is **v1.5 Phase 23** (its `23-CONTEXT.md` decisions D-01..D-17, `23-CLAIMS-INVENTORY.md`, `23-DQA-CHARACTERIZATION.md`, `23-CONSOLIDATION-PLAN.md`).
- **One structural difference from the v1.5 analog:** v1.5 ran a parallel empirical-verification phase (Phase 24) that verified the package's claimed figures. **v1.6 has no such phase** — doc-03's dataset facts were settled in v1.5, and remaining empirical work is FUT/trainex. Therefore nothing in-milestone verifies Phase 30's "claimed, unverified" figures; the package itself must carry that status honestly and delegate verification downstream (external research / FUT). This shapes PKG-07.

## Requirements

1. **Annotated document list (PKG-05)**: The package delivers a complete annotated document list — every document needed to adjudicate the issue-03 findings, each with a role annotation — assembled as a self-contained, repo-blind upload set.
   - Current: No package or document list exists; the materials are scattered across `pinn_instruction/`, `framework-specs/`, `framework-revisions/`, and `simulation_data/Documentation/`.
   - Target: A list whose **always-intact inputs** are the issue-03 doc, `ctl_instruction.md`, and `pinn_architecture.md` (framework specs copied byte-for-byte, never consolidated), plus the locked **additional inputs**: `review_of_framework.md` and `stage_strat_revision.md` (each shipped with a baseline-critique mandate per ERW rule 6), `sampling_method.md` (annotated FROZEN/historical, SCOPE-08), and a consolidated **v1.5-verified-facts reference**. If the deliverable file set exceeds ~5 files or context is scattered across fragments, the fragments are consolidated into a single context file (framework specs never consolidated) and the **consolidation plan is surfaced to the user before assembly** (a hard checkpoint, the v1.5 D-07 analog).
   - Acceptance: The assembled package directory contains every listed document; each entry carries a role annotation and (for snapshots) a canonical source path + source commit hash; the consolidation checkpoint was presented to the user before assembly when triggered.

2. **Framed research questions (PKG-06)**: Each contested or unverified finding is posed as an explicit, neutral research question, organized **by issue-03's own section order**, with the locked v1.4 + v1.5 outcomes listed verbatim as hard constraints (SCOPE-12).
   - Current: The findings exist only inside the non-authoritative issue doc, interleaved with its own (non-authoritative) "Recommended Resolutions".
   - Target: A questions document following issue-03's structure (audit §§6–7 → Causal Training Mismatch blueprint → stage-assignment methodology → next-steps fragments). Coverage is **at least** the Phase-31-SC1 selected-finding set — B-07, B-08, M6, M7, M14, M15, M16, D5, NS-12/13/18, the human-approval decisions **D-04** (causal training mode: per-time-step / global+ALM / time-windowed hybrid), **D-05** (s_min frame), **D-06** (epsilon strategy), and the **`D = 6.694` vs `D ≈ 4.6416`** conflict — with the full finding inventory locked during assembly after reading issue-03 in full. The three human-approval decisions and the `D` conflict are **posed without being settled**. A shared preamble lists the SCOPE-12 hard constraints verbatim (14D input `[τ, IC₁₃]`, Jacobi IC₁₃, mass-weighted COM projection head, PHYS-03 `eps_soft = 1e-5`, post-v1.3 SCS gate `ε_H > 10⁻⁵` / `SCS > −5`, PHYS-01 raw-mass `D ≈ 4.6416`, PIPE-01..10, VAL-01..04).
   - Acceptance: Every selected finding maps to a neutral question that states the issue-doc position and the current framework-spec position without presupposing a resolution; D-04/D-05/D-06 and the `D` conflict appear unsettled; the SCOPE-12 hard-constraints preamble is present and verbatim; the questions follow issue-03 section order.

3. **Recommended resolution-doc skeleton (PKG-06 support; user-locked)**: The package ships a **non-binding** recommended structure for the resolution doc the external research will produce — one section per selected finding.
   - Current: No structure guidance exists; without it, Phase 31 readiness verification and Phase 32 packet-building must reverse-engineer the doc's organization.
   - Target: A per-finding skeleton (one section per selected finding) shipped in the package and explicitly marked non-binding ("the resolution doc remains the user's product; this is a suggestion to ease coverage-checking"), with v1.4 `ctl_pinn_resolution.md` / v1.5 `02-resolution-doc.md` cited as format precedents.
   - Acceptance: A per-finding skeleton is present, enumerates the selected findings, and is labelled non-binding; no schema is mandated.

4. **Claimed-vs-verified figure register (PKG-07)**: Every dataset/empirical figure stated anywhere in the package is explicitly marked **"claimed, unverified"** (the issue-doc value) unless already verified by v1.5, in which case it is stated as verified with its v1.5 citation. No unverified figure is presented as fact, and no in-milestone verification is performed.
   - Current: Issue-03 states dataset figures (e.g., stage trajectory counts, the `D = 6.694` derivation inputs) as if settled.
   - Target: A claims register with stable IDs; each figure rows as `claimed-unverified` or `verified` (citing the v1.5 grounding — e.g., the 184 standard IDs without gold, the ~2,565 quasi-random gold count, per-variant snapshot/`dt_out` distributions). All inline figure mentions reference their register ID. The package tells the external research that claimed-unverified figures are **unverified inputs** (not to be relied on as fact) and that any figure gating a verdict is flagged for FUT empirical check — because, unlike v1.5, **no in-milestone phase verifies them**.
   - Acceptance: Every package figure has a register row with value + source + `claimed-unverified | verified` status; every `verified` row cites a v1.5 grounding source; no figure is asserted as fact without such a citation; the register states the no-in-milestone-verification boundary.

5. **Read-only characterization of the two reports (PKG-08)**: `review_of_framework.md` and `stage_strat_revision.md` are characterized read-only — provenance, content map, and relation to the doc-03 findings — and reported to the user, with zero edits to either file.
   - Current: Both reports exist under `framework-revisions/` but their provenance, scope, and relevance to issue-03 are uncharacterized; issue-03 cites them as curriculum-relevant.
   - Target: A standalone phase artifact characterizing each report (git provenance/history, section-by-section content map, relation to the doc-03 findings, and a recommendation on its package role) — the v1.5 `23-DQA-CHARACTERIZATION.md` analog. The characterization outcome confirms each report's shipping annotation (baseline design intent vs hard constraint, per ERW rule 6).
   - Acceptance: A characterization artifact covers both reports with provenance + content map + doc-03 relation; both source files are byte-for-byte unchanged (hash-verified); the characterization is reported to the user.

6. **Delivery & gate-open record (operational — ROADMAP success criterion 5)**: The package is handed to the user and the milestone records that the external resolution-doc gate is now open.
   - Current: The gate is closed; STATE records Phase 30 not started.
   - Target: Delivery = package committed + a `DELIVERY-NOTE.md` (user-only, never uploaded) stating how to run the ERW handoff, that the resolution doc must land under `framework-revisions/research_reports/03-curriculum-and-training-loop/`, and that adjudication Phases 32–36 gate on the consolidated doc landing AND Phase 31 passing. The gate-open state is recorded in STATE.md **via gsd-tools handlers only** (no direct Write/Edit to STATE.md).
   - Acceptance: A `DELIVERY-NOTE.md` exists with the result-landing path and gate semantics; STATE.md reflects the gate-open state via gsd-tools; no uploaded file (master/prompt) contains any repo path.

## Boundaries

**In scope:**
- An ERW-conformant package at `framework-revisions/research_reports/03-curriculum-and-training-loop/` (`DELIVERY-NOTE.md`, `RESEARCH-CONTEXT-MASTER.md`, `RESEARCH-AGENT-PROMPT.md`, `specs/` commit-pinned snapshots).
- The annotated document list with the locked input set (issue-03 + the two intact spec targets + the two reports + `sampling_method.md` + v1.5-verified-facts reference + consolidated fragments as needed).
- Neutrally-framed research questions (by issue-03 section order) + the SCOPE-12 hard-constraints preamble.
- The non-binding per-finding resolution-doc skeleton.
- The claimed-vs-verified figure register.
- The read-only characterization of `review_of_framework.md` and `stage_strat_revision.md`.
- Delivery note + gate-open STATE record (via gsd-tools handlers).

**Out of scope:**
- **Empirical verification of any dataset figure** — v1.6 has no Phase-24 analog; figures are stated as claims or cite v1.5; verification is delegated to the external research / FUT.
- **Any adjudication, verdict, evidence packet, or framework-spec edit** — Phases 32–36; this phase frames questions, it does not answer them.
- **Editing `ctl_instruction.md` / `pinn_architecture.md`** — they ship as intact snapshots only; edits are Phases 33–35.
- **Editing `review_of_framework.md`, `stage_strat_revision.md`, `sampling_method.md`, or `data_quality_assessment.md`** — read-only / frozen (SCOPE-08/09).
- **Any `pinn/` reference as grounding** — SCOPE-10; issue-03's "Canonical" live-code citations are overridden and noted as a hard constraint to the external research.
- **Running probes** — formula-sanity probes (SCOPE-15) belong to the contract/acceptance phases (33–36); Phase 30 states claims only.
- **Prescribing a binding resolution-doc schema** — only a non-binding skeleton ships (user decision).
- **Settling D-04 / D-05 / D-06 or the `D` conflict** — posed neutrally; resolved later via the resolution doc + Phase 32 adjudication.

## Constraints

- **ERW runbook is canonical** (`2026-06-11-external-research-workflow.md`): self-containment of uploads (zero repo paths in masters/prompts; companion files referenced by bare filename; a manifest table with per-file treatment); one shared `specs/` snapshot set pinned to a commit hash in the master frontmatter; the prompt ships with the master ("a package without its prompt is incomplete"); source grading (hard constraint vs baseline design intent) with a baseline-critique mandate for report-quality inputs.
- **SCOPE-12 hard constraints** are listed verbatim in the package and never re-opened by this phase.
- **STATE.md mutated only via gsd-tools handlers** (no direct Write/Edit), per the project anti-pattern.
- **One atomic commit per plan via `scripts/agent-commit`** (`GIT_AGENT_ID` + `GIT_AGENT_OWNED_PATHS`; `.githooks` active); pre-phase recovery tag `v1.6-pre-phase-30` cut from `milestone/v1.6` HEAD before phase commits.
- **STOP protocol in full** (adjudication milestone): source-silent semantic / process-schema / cross-phase decisions are surfaced as gaps in `30-GAPS.md` + `.planning/milestones/v1.6-GAPS.md` (create on first gap), never invented.

## Acceptance Criteria

- [ ] An ERW-conformant package exists under `framework-revisions/research_reports/03-curriculum-and-training-loop/` (`DELIVERY-NOTE.md`, `RESEARCH-CONTEXT-MASTER.md`, `RESEARCH-AGENT-PROMPT.md`, `specs/` commit-pinned snapshots).
- [ ] The annotated document list is complete; each entry has a role annotation; the consolidation plan was surfaced to the user before assembly when the ~5-file / scattered-fragment trigger fired.
- [ ] Package inputs include the intact issue-03 doc + `ctl_instruction.md` + `pinn_architecture.md`, plus `review_of_framework.md` + `stage_strat_revision.md` (baseline-critique mandate), `sampling_method.md` (FROZEN annotation), and the v1.5-verified-facts reference.
- [ ] Framed questions follow issue-03 section order, cover at least {B-07, B-08, M6, M7, M14, M15, M16, D5, NS-12/13/18, D-04, D-05, D-06, `D = 6.694`}, and pose D-04/D-05/D-06 + the `D` conflict without settling them.
- [ ] The SCOPE-12 hard-constraints preamble is present and verbatim.
- [ ] A non-binding per-finding resolution-doc skeleton ships, marked non-binding, citing the v1.4/v1.5 format precedents.
- [ ] Every dataset/empirical figure is registered `claimed-unverified` or `verified` (with a v1.5 citation); no unverified figure is stated as fact; the register states that no in-milestone phase verifies the claims.
- [ ] Both `review_of_framework.md` and `stage_strat_revision.md` are characterized read-only and reported to the user; both files are byte-for-byte unchanged (hash-verified).
- [ ] A `DELIVERY-NOTE.md` states the doc-03 result-landing path and the Phase 31 / 32–36 gate semantics; STATE records the gate open via gsd-tools handlers; no uploaded file contains a repo path.
- [ ] Zero edits to `ctl_instruction.md`, `pinn_architecture.md`, `sampling_method.md`, `data_quality_assessment.md`, the two reports, or `pinn/` (this phase characterizes and packages only).

## Ambiguity Report

| Dimension          | Score | Min  | Status | Notes                                                                 |
|--------------------|-------|------|--------|-----------------------------------------------------------------------|
| Goal Clarity       | 0.90  | 0.75 | ✓      | PKG-05..08 + 5 ROADMAP success criteria; deliverable form fixed by ERW runbook |
| Boundary Clarity   | 0.92  | 0.70 | ✓      | SCOPE-08..15; package payload + question organization locked in Round 1 |
| Constraint Clarity | 0.85  | 0.65 | ✓      | ERW runbook canonical; SCOPE-12 verbatim; claimed-unverified + no-in-milestone-verification boundary |
| Acceptance Criteria| 0.90  | 0.70 | ✓      | 10 pass/fail checks; per-finding skeleton makes coverage falsifiable  |
| **Ambiguity**      | 0.105 | ≤0.20| ✓      | Gate passed; remaining open items are execution-level (exact consolidation, filenames) |

Status: ✓ = met minimum, ⚠ = below minimum (planner treats as assumption). No dimension is below minimum.

## Interview Log

| Round | Perspective     | Question summary                                   | Decision locked                                                                 |
|-------|-----------------|---------------------------------------------------|---------------------------------------------------------------------------------|
| Pre   | Researcher      | Which worktree does Phase 30 run in?              | `milestone/v1.6` worktree (`../3_body_problem-v1.6`); not `master` (user-confirmed) |
| 1     | Boundary Keeper | Which optional docs ship as package inputs?       | All four: `review_of_framework.md` + `stage_strat_revision.md` (baseline-critique mandate), `sampling_method.md` (FROZEN), v1.5-verified-facts reference |
| 1     | Researcher      | How prescriptive on resolution-doc structure?     | Non-binding recommended per-finding skeleton (no mandated schema)               |
| 1     | Boundary Keeper | How to organize framed questions?                 | By issue-03's own section order (per-finding skeleton carries the downstream mapping) |

---

*Phase: 30-research-package-assembly*
*Spec created: 2026-06-17*
*Next step: /gsd-discuss-phase 30 — implementation decisions (exact package file layout, the consolidation plan, which `simulation_data` excerpts enter the consolidated context file, filenames)*
