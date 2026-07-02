# Phase 30: Research Package Assembly — Research

**Researched:** 2026-06-18
**Domain:** ERW (External Research Workflow) package assembly — specwork channel; doc-03 (curriculum + training loop). Pure internal documentation-assembly phase (no web/library research).
**Confidence:** HIGH (all inputs are repo-internal, read directly this session)

> **Provenance note:** Every claim below is tagged `[VERIFIED: <path>]` (read directly from the repo this session), `[CITED: <path>:line]` (referenced location), or `[ASSUMED]` (inference flagged for the planner). There are no external/registry packages in this phase, so the Package Legitimacy Audit and Standard Stack sections are N/A by design.

---

<user_constraints>
## User Constraints (from CONTEXT.md)

> Copied from `.planning/phases/30-research-package-assembly/30-CONTEXT.md` (decisions D-01..D-22). The CONTEXT was gathered in `--auto --all` mode; all decisions are operational/presentation form, grounded in SPEC / ROADMAP / REQUIREMENTS / the ERW runbook / the v1.5 Phase 23 precedent. **No source-silent semantic decision arose** — the STOP protocol recorded no gap during discussion. These are LOCKED inputs the planner MUST honor.

### Locked Decisions (the HOW, D-01..D-22)

**Package location & delivery form**
- **D-01** Package at `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/` (absent today — gate closed; this phase creates it). Mirrors v1.4 `01-*/` and v1.5 `02-*/`.
- **D-02** ONE research package (NOT split a/b) — specwork issue-doc round, one package per issue.
- **D-03** ERW-fixed file set at round root: `DELIVERY-NOTE.md` (user-only, **never uploaded**), `RESEARCH-CONTEXT-MASTER.md` (single uploaded entry point), `RESEARCH-AGENT-PROMPT.md` (paste-ready; ships with the master), `specs/` (one shared commit-pinned snapshot set).
- **D-04** Snapshots in `specs/` pinned to a commit hash in the master frontmatter (`source_baseline`); refresh if a source changes. Framework specs (`ctl_instruction.md`, `pinn_architecture.md`, `sampling_method.md`) copied **byte-for-byte intact** — NEVER consolidated/excerpted/summarized (PKG-05 hard rule).
- **D-05** **Zero repo paths in any authored upload** (master + prompt); companion files referenced by **bare filename** in a manifest table with per-file treatment; all repo routing lives ONLY in `DELIVERY-NOTE.md`.

**Document list**
- **D-06** Inclusion criterion: a doc enters the list iff ≥1 issue-03 finding needs it. Final list locked at execution AFTER PKG-08 characterization (D-19) AND AFTER the consolidation checkpoint (D-09).
- **D-07** Locked input set: `03-curriculum-and-training-loop.md` (intact); `ctl_instruction.md` + `pinn_architecture.md` (intact spec-edit targets); `review_of_framework.md` + `stage_strat_revision.md` (each with a **baseline-critique mandate**, ERW rule 6); `sampling_method.md` (intact, annotated **FROZEN**/historical, SCOPE-08); a consolidated **v1.5-verified-facts reference**.
- **D-08** `pinn/` live code EXCLUDED; package states issue-03's "Canonical" `pinn/` citations are overridden (SCOPE-10). Issue-01/02 NOT included — their outcomes travel as the SCOPE-12 block + the intact specs.

**Consolidation + hard user checkpoint**
- **D-09** Deliverable set exceeds ~5 files → consolidation rule fires; scattered fragments → ONE context file (framework specs never consolidated). **Hard execution checkpoint: the consolidation plan is surfaced to the user BEFORE assembly** (the v1.5 D-07 analog). The planner MUST model this as a user gate.
- **D-10** The consolidated context file is a companion grounding (snapshot-class) file: it MAY retain internal per-fragment source-path provenance labels; the master/prompt carry zero repo paths and reference it by bare filename.

**Research-question framing (PKG-06)**
- **D-11** ONE questions document, organized by **issue-03's own section order** (audit §§6–7 → Causal Training Mismatch blueprint → stage-assignment methodology → next-steps fragments). Differs from Phase 23's contract-cluster grouping; the per-finding skeleton (D-13/D-14) carries the downstream finding→phase mapping. Coverage ≥ {B-07, B-08, M6, M7, M14, M15, M16, D5, NS-12/13/18, **D-04**, **D-05**, **D-06**, `D = 6.694` vs `D ≈ 4.6416`}; full inventory locked after reading issue-03 in full.
- **D-12** Neutral framing: each question states the issue-doc position AND the current framework-spec position WITHOUT presupposing a resolution; D-04/D-05/D-06 + the `D` conflict appear **unsettled**. Package tells the research that BOTH the issue doc and its "Recommended Resolutions" are non-authoritative; cite the `D = 6.694` vs locked `D ≈ 4.6416` (v1.5 Phase 25 EVID-10) as the worked seed-conflict example.
- **D-13** Shared hard-constraints preamble lists the SCOPE-12 locked v1.4 + v1.5 outcomes **verbatim**: 14D input `[τ, IC₁₃]`, Jacobi IC₁₃, mass-weighted COM projection head, PHYS-03 `eps_soft = 1e-5`, post-v1.3 SCS gate `ε_H > 10⁻⁵` / `SCS > −5`, PHYS-01 raw-mass `D ≈ 4.6416`, PIPE-01..10 / VAL-01..04 — plus the SCOPE-10 hard constraint.

**Resolution-doc skeleton (PKG-06 support; user-locked non-binding)**
- **D-14** Per-finding skeleton (one section per selected finding), explicitly **non-binding** ("the resolution doc remains the user's product; this is a suggestion to ease coverage-checking"), citing v1.4 `ctl_pinn_resolution.md` + v1.5 `02-resolution-doc.md` as format precedents. No schema mandated. Carries the finding → adjudication-phase (32–36) mapping.

**Claims register (PKG-07)**
- **D-15** Dedicated claims register with stable IDs (`CLM-01`…): every figure rows as `claimed-unverified` or `verified` (with its v1.5 citation); inline figure mentions reference their CLM ID.
- **D-16** Conservative verified-status rule — only v1.5-verified facts (committed v1.5 artifacts + `simulation_data/Documentation/`) count as "verified"; when in doubt, `claimed-unverified`.
- **D-17** **No-in-milestone-verification boundary (the single most important v1.6 ≠ v1.5 difference):** v1.6 has no Phase-24 analog; NO in-milestone phase verifies these claims. The register MUST state this; `claimed-unverified` figures are unverified inputs; any figure gating a verdict is flagged for FUT. Enumerate at minimum: the `D = 6.694` derivation inputs + stage trajectory counts (claimed-unverified); the v1.5 anchors as `verified` with citation (184 standard IDs without gold; ~2,565 quasi-random gold count; per-variant snapshot/`dt_out` distributions).

**Reports characterization (PKG-08)**
- **D-18** Deliverable: standalone phase artifact `.planning/phases/30-research-package-assembly/30-REPORTS-CHARACTERIZATION.md` (the `23-DQA-CHARACTERIZATION.md` analog) covering BOTH reports: git provenance, section-by-section content map, doc-03 relation, package-role recommendation (baseline design intent vs hard constraint). Zero edits; both files byte-for-byte unchanged, hash-verified in a `30-SNAPSHOT-HASHES.txt`. Reported to the user.
- **D-19** Sequencing — characterization completes BEFORE the document list is finalized (it confirms each report's shipping annotation). Early task.

**Gate-opening record & handoff**
- **D-20** Delivery = package committed + `DELIVERY-NOTE.md` (user-only) stating: how to run the ERW handoff; the resolution doc must land under `…/research_reports/03-curriculum-and-training-loop/`; v1.4/v1.5 resolution docs as format precedents (suggestion only); adjudication Phases 32–36 gate on the consolidated doc landing **AND** Phase 31 passing.
- **D-21** Gate-open state recorded in STATE.md via **gsd-tools state handlers only** (no direct Write/Edit).
- **D-22** `simulation_data` excerpts expected **minimal** for doc-03 (less dataset-centric than v1.5) — include only v1.5-verified facts the curriculum/training-loop contracts depend on (snapshot/`dt_out` distributions bounding `tau_L`/`L_max`/collocation scaling; stage-assignment-relevant counts) + claims-register anchors. Final selection rides the D-09 checkpoint.

### Claude's Discretion (research recommends; planner decides at assembly)
- Exact filenames / placement of the questions doc, SCOPE-12 preamble, claims register, resolution-doc skeleton — each a **named companion file** (bare-filename-referenced) or a **section of `RESEARCH-CONTEXT-MASTER.md`**. **CONTEXT recommends**: ship questions + preamble + skeleton + claims register as named companion files; final call at assembly. (NOTE: the delivered v1.5 package ultimately **consolidated** all of these into the single `RESEARCH-CONTEXT-MASTER.md` as a post-delivery remediation — see "v1.5 ≠ delivered form" below. Planner should weigh single-master vs multi-companion.)
- Which `simulation_data` / v1.5 excerpts enter the consolidated context file (D-22) — judged per-finding, shown at the D-09 checkpoint.
- Whether the v1.5-verified-facts reference is standalone or folded into the consolidated context — **recommended standalone** (reused by claims register + preamble).

### Deferred Ideas (OUT OF SCOPE)
- Prescribing a binding schema for the resolution doc — rejected (non-binding skeleton only, D-14).
- Any empirical probe or figure verification — no Phase-24 analog in v1.6; package states claims only.
- Settling D-04 / D-05 / D-06 or the `D` conflict — posed neutrally; resolved later (resolution doc + Phase 32).
- The trainex-r1 handoff todo — different track (build-design channel); NOT folded into Phase 30.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support (where this RESEARCH grounds it) |
|----|-------------|---------------------------------------------------|
| PKG-05 | Annotated document list; consolidate scattered fragments into one context file (framework specs never consolidated); surface the consolidation plan to the user before assembly | "Consolidation Map (PKG-05)" + "ERW Package Blueprint"; the v1.5 `23-CONSOLIDATION-PLAN.md` template is the exact reusable structure |
| PKG-06 | Frame each contested/unverified finding as a neutral question, by issue-03 section order; SCOPE-12 hard-constraints preamble verbatim; D-04/D-05/D-06 + the `D` conflict posed unsettled | "issue-03 Structural Map + Finding Inventory" gives the complete selected-set + section order; "SCOPE-12 preamble" exact text below |
| PKG-07 | Claimed-vs-verified figure register; every figure `claimed-unverified` unless v1.5-verified with citation; state the no-in-milestone-verification boundary | "Claims Register Seed (PKG-07)" — claimed-unverified rows + verified anchors with exact citation paths/lines |
| PKG-08 | Read-only characterization of `review_of_framework.md` + `stage_strat_revision.md`; provenance + content map + doc-03 relation; zero edits, hash-verified | "Reports Characterization Scope (PKG-08)" — size, provenance, section map, doc-03 relation for both |
| (skeleton) | Non-binding per-finding resolution-doc skeleton; v1.4/v1.5 resolution docs as format precedents | D-14; covered in blueprint + decomposition |
| (delivery) | Delivery + gate-open STATE record via gsd-tools handlers | "Recommended Plan Decomposition" final plan; "Risks/Landmines" STATE.md rule |
</phase_requirements>

---

## Summary

Phase 30 is a **pure internal documentation-assembly phase**: it frames and packages *existing* repo materials into a single, self-contained, repo-blind ERW package for issue-03, then hands it off. There is **no web or library research** — every input is a file already in the worktree, and the deliverable form is fixed by the ERW runbook (`docs/runbooks/external-research/2026-06-11-external-research-workflow.md`) and the directly-reusable v1.5 Phase 23 precedent. The phase performs **no adjudication, no empirical verification, and no framework-spec edits** — those are Phases 32–36.

The single most important structural fact for planning: **v1.6 has no Phase-24 analog.** In v1.5, a parallel empirical-verification phase (Phase 24) re-verified every claimed figure in the package. v1.6 has nothing equivalent — doc-03's dataset facts were settled in v1.5, and remaining empirical work is FUT/trainex. So the package must carry "claimed, unverified" honestly and delegate verification downstream; the claims register (PKG-07) must explicitly state this boundary, and the planner must not assume any later v1.6 phase will check a package figure (CONTEXT D-17).

The work decomposes cleanly along the v1.5 Phase 23 pattern: (1) read-only characterization of the two PKG-08 reports + seed the claims register [early, gates the doc list]; (2) build the consolidation plan and surface it at a **hard user gate** [D-09]; (3) take byte-for-byte commit-pinned snapshots into `specs/`; (4) author the framed-questions doc (issue-03 section order) + SCOPE-12 preamble + non-binding skeleton; (5) finalize the master + prompt + delivery note, commit, and record gate-open via gsd-tools. Two recurring landmines dominate: never consolidate a framework spec (D-04, PKG-05 hard rule), and never leak a repo path into an uploaded file (D-05, ERW rule 1).

**Primary recommendation:** Reuse the v1.5 Phase 23 artifacts as direct templates (`23-CONSOLIDATION-PLAN.md`, `23-CLAIMS-INVENTORY.md`, `23-DQA-CHARACTERIZATION.md`, `23-SNAPSHOT-HASHES.txt`, the delivered `02-*/` master + delivery note), substituting doc-03 content, and structure the plan as 5 plans with the D-09 consolidation checkpoint modeled as an explicit user gate between characterization and assembly.

---

## Architectural Responsibility Map

This is a documentation-assembly phase; the "tiers" are package layers, not software tiers. Mapping which artifact owns which requirement:

| Capability | Primary Artifact (owner) | Secondary Artifact | Rationale |
|------------|--------------------------|--------------------|-----------|
| Annotated document list (PKG-05) | `RESEARCH-CONTEXT-MASTER.md` Per-File Manifest | `30-CONSOLIDATION-PLAN.md` (phase artifact, surfaced at gate) | Manifest is the uploaded, repo-blind document index; consolidation plan is the planning artifact that the user ratifies |
| Byte-for-byte snapshots | `specs/` (one shared set) | `30-SNAPSHOT-HASHES.txt` | Specs ship intact; hashes prove read-only fidelity |
| Framed questions (PKG-06) | framed-questions companion **or** master section | — | CONTEXT recommends companion; v1.5 delivered as master section |
| SCOPE-12 hard-constraints preamble | preamble companion **or** master section | — | Must be verbatim; consumed by the external research as hard constraints |
| Claims register (PKG-07) | claims-register companion **or** master section | `30-CLAIMS-INVENTORY.md` (phase artifact, the v1.5 `23-CLAIMS-INVENTORY.md` analog) | Phase artifact is the source-of-truth register; package copy is the uploaded form |
| Resolution-doc skeleton (PKG-06 support) | skeleton companion **or** master section | — | Non-binding; carries finding→phase (32–36) map |
| Reports characterization (PKG-08) | `30-REPORTS-CHARACTERIZATION.md` (phase artifact, never uploaded) | manifest annotations on the two reports | Characterization confirms the shipping annotation (baseline intent vs hard constraint) |
| Repo routing / gate semantics | `DELIVERY-NOTE.md` (user-only, never uploaded) | STATE.md (via gsd-tools) | The ONLY place repo paths may appear |
| Gate-open record | STATE.md (via gsd-tools handlers) | `DELIVERY-NOTE.md` | Anti-pattern 15: no direct Write/Edit to STATE.md |

---

## ERW Package Blueprint

**Source:** `docs/runbooks/external-research/2026-06-11-external-research-workflow.md` [VERIFIED] + the delivered v1.5 `02-*/` package [VERIFIED].

### Required file set at the round root (D-03)

```
research_reports/03-curriculum-and-training-loop/        <- D-01 (created by this phase; absent today)
  DELIVERY-NOTE.md            user-only routing — NEVER uploaded (D-20)
  RESEARCH-CONTEXT-MASTER.md  the single uploaded entry point (manifest + preamble + questions + claims + skeleton, OR a thin master that points at companions)
  RESEARCH-AGENT-PROMPT.md    paste-ready prompt + attach-list header — ships with the master (a package without its prompt is incomplete)
  specs/                      ONE shared commit-pinned snapshot set (D-04)
    03-curriculum-and-training-loop.md   (issue doc, intact)
    ctl_instruction.md                   (intact, byte-for-byte)
    pinn_architecture.md                 (intact, byte-for-byte)
    sampling_method.md                   (intact, FROZEN annotation in manifest)
    review_of_framework.md               (intact; baseline-critique mandate)
    stage_strat_revision.md              (intact; baseline-critique mandate)
    <consolidated-context file>          (v1.5-verified-facts + minimal sim_data excerpts; MAY retain internal source-path labels — D-10)
  (research_results/  + 03-resolution-doc.md land later — created at delivery/result time, not by this phase)
```

> **Layout caveat for the planner:** the ERW runbook's canonical tree nests `RESEARCH-CONTEXT-MASTER.md`/`RESEARCH-AGENT-PROMPT.md`/`specs/` inside a `research_package/` subdir [CITED: runbook lines 53–62]. The *delivered* v1.5 package actually placed `RESEARCH-CONTEXT-MASTER.md`, `DELIVERY-NOTE.md`, and `specs/` inside a `research_package/` subdir of `02-*/` [VERIFIED: `…/02-data-pipeline-and-validation/research_package/`]. CONTEXT D-01/D-03 describe the file set "at the round root." This is a **mechanical/presentation choice** (single package, D-02) — the planner picks `03-*/research_package/` vs `03-*/` directly; either is ERW-conformant. Recommend matching the v1.5 delivered form (`03-*/research_package/`) for consistency, but flag as a Claude's-discretion presentation call, not a gap.

### The 14 ERW rules — which are load-bearing for THIS package

[CITED: runbook lines 76–146]. All 14 apply; the load-bearing ones for doc-03:

| # | Rule | Load-bearing here? | Why |
|---|------|--------------------|-----|
| 1 | ZERO repo paths in any authored upload; companion files by bare filename; `specs/` snapshots may retain internal cross-refs (never scrub) | **CRITICAL** | D-05; the dominant leak landmine. Snapshots keep their internal refs; the master/prompt must not name any repo path |
| 2 | Tell the agent "you work from attached files only"; manifest table with per-file treatment | **CRITICAL** | The repo-blind guarantee; manifest is PKG-05's uploaded form |
| 3 | ONE shared `specs/` set per round, never duplicated | High | D-02/D-04; single package means one specs set anyway |
| 4 | Snapshot only what the questions need | Medium | D-22 minimal sim_data excerpts |
| 5 | Pin snapshots to a commit hash in master frontmatter; refresh if a source changes | **CRITICAL** | D-04 `source_baseline`; the recovery-tag/HEAD caveat makes the pin commit matter |
| 6 | Grade every source hard-constraint vs baseline design intent; **baseline-critique mandate** for brainstorm-quality inputs | **CRITICAL** | The two PKG-08 reports ship WITH a baseline-critique mandate (D-07); the framework specs are hard constraints; the issue doc is non-authoritative |
| 7 | Build-design output contract (options menus, decision sheet) | **N/A** | This is specwork, not build-design (D-02) |
| 8 | Knowledge-package output contract | **N/A** | Specwork |
| 9 | Where attached materials are silent, the agent records the gap in the claims register — never invents (STOP culture extends to external agents) | High | The prompt must carry this instruction |
| 10 | Split into sub-packages once a round exceeds ~6–7 work items | **Considered, rejected** | D-02 explicitly: one package; rule-10 split targets trainex build-design rounds, not issue-doc specwork |
| 11 | Record consolidation join points in delivery note | Medium | Single package → trivial; the finding→phase map lives in the skeleton (D-14) |
| 12 | Naming: issue-doc rounds keep `<NN-issue-slug>` | High | `03-curriculum-and-training-loop/` |
| 13 | Specwork: resolution doc enters adjudication as candidate verdict source | High | D-20 gate semantics |
| 14 | Package directory is the durable record — keep master/prompt/note/snapshots/results/resolution together | High | D-01 co-location |

---

## issue-03 Structural Map + Finding Inventory

**Source:** `pinn_instruction/issues/03-curriculum-and-training-loop.md` (711 lines) [VERIFIED — read in full].

### Section order (this is the PKG-06 question-organization order, D-11)

| # | Section | Lines | Drives which questions |
|---|---------|-------|------------------------|
| 1 | Executive Summary | 3–10 | context only |
| 2 | Decisions Requiring Human Approval (D-04, D-05, D-06) | 12–86 | the three human-approval decisions — posed unsettled |
| 3 | Confirmed Findings (BLOCKING B-07/B-08; MAJOR M6/M7/M14/M15/M16/D5/NS-12/13/18; MINOR/INFO ALM-μ clamp, M4 cross-ref) | 88–117 | the core finding inventory |
| 4 | Causal Training Mismatch: Option A vs B (+ Hybrid C) | 121–152 | D-04 deep context; "Training Phases" list |
| 5 | Loss Component Scaling Contract (+ Huber-δ) | 155–181 | NS-18, NS-13 |
| 6 | Data-Driven Adaptive Stage Assignment | 185–225 | CURR-01-shaped question; cross-refs `stage_strat_revision.md` |
| 7 | tau_L and L_max Formula Resolution (carries `D = 6.694` at line 265/305) | 229–305 | M7, the `D` conflict, CURR-02 |
| 8 | Implementation Checklist (P3/P4 items) | 309–331 | maps findings to P-codes |
| 9 | Stage Transition Criteria (D5 dual-path) | 333–364 | D5 |
| 10 | Energy Loss Weight Schedule (M15 capped hybrid) | 366–379 | M15 |
| 11 | Open Decisions (D-04 causal; D-05 s_min) | 383–419 | D-04, D-05 verbatim decision text |
| 12 | Recommended Resolutions (non-authoritative) | 422–445 | the issue doc's own positions — package must mark non-authoritative |
| 13 | Cross-Issue Interactions | 448–460 | interaction context |
| 14 | Gradient Clipping — Merged Specification (M14) | 463–485 | M14 |
| 15 | ALM Parameter Update Specification (μ_p clamp) | 489–505 | LOOP-05 / MINOR clamp finding |
| 16 | References (carries overridden `pinn/` "Canonical" citations) | 509–516 | SCOPE-10 hard-constraint note |
| 17 | Considered Alternatives (unsoftened s_min) | 520–530 | D-05 context |
| 18 | Verbatim Audit §6 — Unified Batch Construction | 534–664 | B-07, B-08, LOOP-01/02/03, the `training_step` contract |
| 19 | Stage Inventory Summary (per-stage counts + dt_out) | 668–680 | stage trajectory counts (claimed-unverified); dt_out values |
| 20 | Decision Priority Queue | 689–705 | priority context |

### Complete finding inventory (table → drives PKG-06 + claims register)

| Finding ID | One-line description | Issue-03 location | In SPEC-locked selected set? |
|------------|----------------------|-------------------|------------------------------|
| **D-04** | Causal training mode: A (per-time-step) / B (global+ALM, current SOT) / C (time-windowed causal-ALM hybrid) | lines 16–40, 121–152, 385–410 | YES — posed unsettled |
| **D-05** | s_min frame: unsoftened stage gate + softened loss (matches SOT) vs softened everywhere | lines 42–63, 412–418, 520–530 | YES — posed unsettled |
| **D-06** | Epsilon strategy: `1e-5` everywhere / dual-context (`1e-10` static + `1e-5` dynamic) / `1e-10` everywhere | lines 65–86 | YES — posed unsettled |
| **B-07** | Batch construction not implemented (240 replay + 16 lookahead per CTL) | line 94 | YES |
| **B-08** | Data-fidelity (8192, L1) and collocation (4096, physics+energy) points conflated | line 95 | YES |
| **M6** | L_norm lacks `np.clip(L_norm,0,1)` before IC-vector mapping | line 102 | YES |
| **M7** | tau_L computed but dropped from IC vector — exclude by design | line 103 | YES |
| **M14** | Gradient-clipping divergence: PINN median-based vs CTL C-schedule → merge `C_stage·median(grad_norm_history)` | line 104, 463–485 | YES |
| **M15** | Energy loss λ_E may overwhelm; capped hybrid `min(10^(k-3), cap[k])` | line 105, 366–379 | YES |
| **M16** | dt_out varies 17× but collocation uniform → `n_col ∝ dt_base/dt_out` (audit verbatim direction) | line 106, 440 | YES |
| **D5** | Stage-transition criteria unattainable; dual-path strict + fallback; pilot Stage 0 | line 107, 333–364 | YES |
| **NS-12** | AD velocities/accelerations — no concrete 3-body PyTorch impl; component-wise AD | line 108 | YES |
| **NS-13** | Huber energy δ=1.0 too large; tune from `\|ΔH\|` quantiles 0.01–0.1 | line 109, 169–181 | YES |
| **NS-18** | Loss-component scaling contract across L_data/L_physics/L_energy | line 110, 155–167 | YES |
| **`D=6.694`** | tau_L code uses `D = cbrt(G·M_tot·T²) = 6.694`; conflicts with locked raw-mass `D ≈ 4.6416` | lines 265, 305 | YES — the worked seed-conflict; posed unsettled |
| ALM μ_p clamp | `mu_p = np.clip(mu_p, 1e-4, 100)` (MINOR/INFO) | line 117, 489–505 | Additional (feeds LOOP-05) — flag for inclusion |
| M4 (cross-ref) | Constraint-counting error — canonical in doc-01; no code impact here | line 116 | Cross-ref only; not a doc-03 question |

**Additional contested/unverified items the planner should flag** (beyond the SPEC-locked set):
- The **stage trajectory counts** in the Stage Inventory Summary (line 668–680): ~1,200 / ~2,000 / ~1,657 / ~600 / ~1,600 / ~2,565 / Unknown — **all claimed-unverified except the ~2,565 gold count** (v1.5-verified). [VERIFIED: issue-03:668–680]
- The **dt_out per-stage values** (0.08 / 0.01 / 0.17) — verifiable against v1.5 facts; mark `verified` where the per-variant `dt_out` distribution grounds them (CLM-09 analog).
- The **per-stage epsilon_phys/epsilon_energy thresholds** and **MAX_EPOCHS table** (lines 638–646, 634) — design hypotheses, explicitly "not fixed"; claimed-unverified, FUT-calibrated.
- The **C_table gradient-clip values** (8.5 / 5.0 / 3.0) and **λ_E cap_table** (line 475, 655) — design figures, claimed-unverified.
- The **240/16 replay/lookahead and 8192/4096 point counts** — design figures from audit §6 (claimed-unverified design constants, not dataset facts).

> **STOP-protocol note for the planner:** posing these as questions is execution work, NOT research work. This inventory does **not** answer or adjudicate any finding. The D-04/D-05/D-06 + `D` conflict remain unsettled by design.

---

## Consolidation Map (PKG-05)

**Source:** D-09/D-22 + the v1.5 `23-CONSOLIDATION-PLAN.md` template [VERIFIED].

### Ships standalone (byte-for-byte intact snapshots — NEVER consolidated, D-04)

| # | Document | Role annotation (lives in manifest, never in the file) | Source path (DELIVERY-NOTE only) |
|---|----------|--------------------------------------------------------|----------------------------------|
| 1 | `03-curriculum-and-training-loop.md` | Adjudication subject — NON-authoritative; may contain errors (incl. its "Recommended Resolutions") | `pinn_instruction/issues/03-curriculum-and-training-loop.md` |
| 2 | `ctl_instruction.md` | Spec-edit target; carries curriculum staging, tau_L/L_max, s_min gate, loss scaling, PHYS-01 `D ≈ 4.6416` | `…/framework-specs/ctl_instruction.md` (1868 lines) |
| 3 | `pinn_architecture.md` | Spec-edit target; carries gradient-clipping / training-strategy contracts | `…/framework-specs/pinn_architecture.md` (1013 lines) |
| 4 | `sampling_method.md` | FROZEN (SCOPE-08); historical record of dataset generation; not a revision target | `…/framework-specs/sampling_method.md` (281 lines) |
| 5 | `review_of_framework.md` | **Baseline design intent** (ERW rule 6) + baseline-critique mandate; curriculum-relevant research report (SCOPE-09) | `…/framework-revisions/review-of-framework/review_of_framework.md` (529 lines) |
| 6 | `stage_strat_revision.md` | **Baseline design intent** + baseline-critique mandate; data-driven stage-assignment report (SCOPE-09) | `…/framework-revisions/stage-strat-revision/stage_strat_revision.md` (427 lines) |

### Consolidated into ONE context file (the consolidation rule fires — ≥5 deliverable files, D-09)

The **v1.5-verified-facts reference** + minimal `simulation_data` excerpts. Per D-22, doc-03 is less dataset-centric than v1.5, so excerpts are minimal. Candidate fragments (final selection rides the D-09 checkpoint):

| Fragment | Source | Lines | What it contributes |
|----------|--------|-------|---------------------|
| Verified-facts register | `.planning/milestones/v1.5-phases/24-empirical-dataset-verification-and-correction-addendum/24-VERIFIED-FACTS.md` | full (table) | The authoritative v1.5 verified figures (CLM-01..13 verdicts), incl. snapshot/`dt_out` distributions, 184-gap, 2,749-vs-2,565 |
| Gold-gap record | `simulation_data/Documentation/standard_quasi_random_ids_not_in_gold.md` | full | 184 standard IDs without gold; 2,749 base / 2,565 gold counts |
| Per-variant Brutus params | `simulation_data/Documentation/README.md` | 146–153, 180+ | per-variant `dt_out` (std 0.17 / hier 0.08 / gold 0.01), tolerances, snapshot counts — grounds the stage `dt_out` figures |
| EVID-10 D-rejection | `.planning/milestones/v1.5-phases/25-evidence-framework-and-issue-ledger/` (EVID-10 record) | EVID-10 row | The committed v1.5 verdict that `D = 6.694` was rejected vs raw-mass `D ≈ 4.6416` — anchors the `D`-conflict framing |

> **Recommendation (Claude's discretion, D-83 analog):** keep the v1.5-verified-facts reference **standalone** (it is reused by both the claims register and the SCOPE-12 preamble), and fold only the minimal sim_data excerpts into the consolidated context file. Final call at the D-09 gate.

### Excluded from consolidation
- `pinn/` live code — EXCLUDED (SCOPE-10/D-08); package states the "Canonical" citations are overridden.
- Framework specs — NEVER consolidated (D-04); shipped intact.
- Issue-01 / issue-02 docs — resolved; their outcomes travel as the SCOPE-12 block + intact specs (D-08).

### The hard user checkpoint (PKG-05 requirement, NOT a courtesy — D-09)
The consolidation plan (this map, instantiated as `30-CONSOLIDATION-PLAN.md` with the open inclusion calls) is **surfaced to the user BEFORE assembly**. The v1.5 analog (`23-CONSOLIDATION-PLAN.md`) ended with a "D-07 APPROVED Record" block the user signed off. The planner MUST model this as an explicit user gate (a `checkpoint:human-approve`-style task) between the document-list-prep plan and the snapshot-assembly plan. Open inclusion calls to surface: (a) exact sim_data excerpt selection; (b) standalone-vs-folded for the verified-facts reference; (c) whether the ALM-μ-clamp MINOR finding gets its own question.

---

## Claims Register Seed (PKG-07)

**Source:** issue-03 [VERIFIED] + `24-VERIFIED-FACTS.md` [VERIFIED] + `ctl_instruction.md` [VERIFIED] + the v1.5 `23-CLAIMS-INVENTORY.md` template.

### `claimed-unverified` figures (issue-doc values; NO in-milestone verifier — D-17)

| Seed CLM | Figure | Claimed value | Issue-03 location | Why claimed-unverified |
|----------|--------|---------------|-------------------|------------------------|
| C-1 | `D = 6.694` derivation | `D = cbrt(G·M_tot_ref·T²)` with `M_tot_ref=3.0`, `T_scale=10` → 6.694 | lines 265, 305 | CONTESTED CONVENTION — conflicts with locked raw-mass `D ≈ 4.6416`; **rejected by v1.5 Phase 25 EVID-10**. Posed as the worked conflict, not verified |
| C-2 | Stage 0 count | ~1,200 | line 672 | dataset-derived count, not v1.5-verified |
| C-3 | Stage 1 count | ~2,000 | line 673 | not v1.5-verified |
| C-4 | Stage 2 count | ~1,657 | line 674 | not v1.5-verified |
| C-5 | Stage 3 count | ~600 | line 675 | not v1.5-verified |
| C-6 | Stage 4 count | ~1,600 | line 676 | not v1.5-verified |
| C-7 | Stage 6 count | Unknown | line 678 | explicitly unknown |
| C-8 | Stage epsilon_phys/energy thresholds | 5e-3 … 1e-4 per stage | lines 638–646 | design hypotheses, "not fixed", FUT-calibrated |
| C-9 | MAX_EPOCHS table | {0:500 … 6:1200} | line 634 | design hypothesis |
| C-10 | C_table clip values | 8.5 / 5.0 / 3.0 | line 475 | design figure |
| C-11 | λ_E cap_table | {0:1 … 6:500} | lines 372, 655 | design figure |
| C-12 | Replay/lookahead/point counts | 240 / 16 / 8192 / 4096 | lines 94–95, 554, 577 | audit §6 design constants |
| C-13 | snapshot-per-trajectory (issue-doc) | ~59 std / ~125 hier / ~1000 gold (referenced via stage table dt_out) | line 670+ | issue-doc approximations; **see verified anchor V-3 for corrected values** |

### `verified` anchors (state as verified WITH v1.5 citation — D-16/D-17)

| Seed CLM | Figure | Verified value | Citation (exact) | Verdict source |
|----------|--------|----------------|------------------|----------------|
| V-1 | Standard IDs without gold | **184** | `simulation_data/Documentation/standard_quasi_random_ids_not_in_gold.md` (Summary, line ~9) + `24-VERIFIED-FACTS.md` CLM-04 | v1.5 DATA-03 `confirmed` |
| V-2 | Quasi-random gold count | **2,565** (base 2,749; base−gold=184) | `…/standard_quasi_random_ids_not_in_gold.md` lines ~7–9; `24-VERIFIED-FACTS.md` CLM-05a/05b | v1.5 DATA-03/04 `confirmed` |
| V-3 | Per-variant snapshot counts | std median 61, hier 127, gold 1003 (issue-doc ~59/~125/~1000 **corrected**) | `24-VERIFIED-FACTS.md` CLM-10 | v1.5 DATA-06 `corrected` |
| V-4 | Per-variant `dt_out` | std 0.17 / hier 0.08 / hier-gold 0.01 / std-gold 0.01 | `24-VERIFIED-FACTS.md` CLM-09; `simulation_data/Documentation/README.md:180` + dataset-reference rule | v1.5 DATA-04 `confirmed` |
| V-5 | hierarchical Brutus output | 4,857 files | `24-VERIFIED-FACTS.md` CLM-06; `README.md:151` | v1.5 `confirmed` |
| V-6 | `D ≈ 4.6416` raw-mass convention (the locked counter to C-1) | `D = (G·T²)^(1/3) ≈ 4.6416`, locked Phase 19 PHYS-01 | `ctl_instruction.md:904–919` (§2.5; line 910 "With G=1, D ~ 4.6416"; line 915 "locked Phase 19, PHYS-01") | v1.4 locked; v1.5 Phase 25 EVID-10 reaffirmed |

> **Caveat (V-3):** mark snapshot counts `verified` at the v1.5-corrected values (61/127/1003), NOT the issue-doc `~59/~125/~1000`. The issue-doc figures are claimed; the v1.5 median is the verified fact. State both, cite CLM-10.

### The no-in-milestone-verification statement (MUST appear in the register — D-17)
Exact boundary the register must state: *"Unlike v1.5, v1.6 has no parallel empirical-verification phase. No phase in this milestone verifies any `claimed-unverified` figure. These figures are unverified inputs — do not rely on them as fact. Any figure that would gate a verdict is flagged for FUT empirical check (FUT-01/FUT-02/FUT-04)."* [grounds: CONTEXT D-17, SPEC req 4 acceptance].

---

## Reports Characterization Scope (PKG-08)

**Source:** both files read this session [VERIFIED]. Deliverable: `30-REPORTS-CHARACTERIZATION.md` (the `23-DQA-CHARACTERIZATION.md` analog, D-18). Read-only; hash-verified in `30-SNAPSHOT-HASHES.txt`.

### `review_of_framework.md` (529 lines)
**Apparent provenance** (planner: confirm via `git log --follow --oneline`, as the v1.5 DQA characterization did): titled "A Technical Review and Resolution Blueprint for the CTL-PINN Framework" — a design-blueprint research report under `framework-revisions/` (SCOPE-09; non-authoritative; **baseline design intent** per ERW rule 6).

**Section map** [VERIFIED via heading scan]:
| § | Lines | Content | doc-03 relation |
|---|-------|---------|-----------------|
| Exec Summary | 3–19 | framework review overview | context |
| §1 Foundational Physical Metrics | 20–131 | §1.1 tau_L + L/L_max computation; §1.2 **global scale (D) computation** | **directly grounds M7, CURR-02, the `D` conflict** |
| §2 Data Scaling & Normalization | 132–229 | §2.1 spatiotemporal normalization; §2.2 **softening eps_soft=1e-5 for ALL loss calcs** (the D-06 anchor); §2.3 IC normalization schema | **directly grounds D-06 epsilon strategy, D-05 s_min** |
| §3 SIREN Backbone Refinements | 230–261 | ω₀ schedule | curriculum/stage-init interaction (minor) |
| §4 Loss Function Framework | 262–392 | §4.1 scaled quantities in loss (NS-18); §4.2 ALM state mgmt; §4.3 AD reference impl (NS-12); §4.4 Huber-δ (NS-13) | **grounds NS-18, NS-12, NS-13, LOOP-05 ALM** |
| §5 Training & Sampling Strategy | 393+ | unified data/collocation sampling; global ALM (the D-04 Option B SOT anchor) | **grounds D-04, B-07, B-08** |

**doc-03 relevance:** HIGH and broad — review_of_framework is the SOT anchor that issue-03 repeatedly cites (D-04 §5.1-5.2, D-05 §2.2, D-06 §2.2 lines 185-191). It is the single most doc-03-relevant report. Recommended package role: **baseline design intent + baseline-critique mandate** (ERW rule 6); the external research may challenge it only via explicit option-vs-baseline proposals.

### `stage_strat_revision.md` (427 lines)
**Apparent provenance:** titled "A Data-Driven Stage Assignment Framework for Curriculum Transfer Learning" — a methodology research report under `framework-revisions/` (SCOPE-09; baseline design intent).

**Section map** [VERIFIED via heading scan]:
| Part | Lines | Content | doc-03 relation |
|------|-------|---------|-----------------|
| Abstract + Part I Foundations | 24–106 | rationale for adaptive curricula; difficulty-metric lexicon; PCA / clustering / quantile-binning techniques | grounds the "Data-Driven Adaptive Stage Assignment" section (issue-03 §6) |
| Part II Revised Workflow | 108–180 | Phase I invariant computation (incl. normalized virial ratio); Phase II EDA; correlation/PCA | **directly grounds CURR-01, the EDA methodology** |
| Part III Adaptive Criteria | 181–240 | hybrid stratification; stable subset (stages 0–1); complex subset (stages 2–6); population balancing | **grounds the >10%-per-stage safeguard, stage assignment** |
| Part IV Implementation & Validation | 241–420 | Python reference impl; curriculum validation protocol; conclusions | grounds CURR-01 contract |
| Source Issues | 421+ | SI-SSR-001 (I3 schema inconsistency) | SI reconciliation (VER-18, Phase 36) |

**doc-03 relevance:** HIGH for the stage-assignment finding cluster (CURR-01). It is the deep-dive companion to issue-03 §6 (the EDA pseudocode). Recommended role: **baseline design intent + baseline-critique mandate**.

> Both reports' shipping annotations (baseline vs hard constraint) are **confirmed by the characterization** before the document list is finalized (D-19 sequencing).

---

## v1.5 Phase 23 Template Extraction

Each reusable artifact and its concrete structure, so the planner can point executors at exact templates. All paths under `.planning/milestones/v1.5-phases/23-research-package-assembly/`.

| v1.5 artifact | doc-03 analog | Structure to reuse | Notes |
|---------------|---------------|--------------------|-------|
| `23-CONSOLIDATION-PLAN.md` | `30-CONSOLIDATION-PLAN.md` | Candidate doc list table → "what is consolidated vs standalone" → "open inclusion calls" → "why the rule fires" → "what this plan does NOT do" → **"D-07 APPROVED Record"** (user sign-off block) | The approved-record block is the user-gate proof. Reuse verbatim structure |
| `23-CLAIMS-INVENTORY.md` | `30-CLAIMS-INVENTORY.md` | Purpose + status-classification rule + scope + claims table (CLM ID / figure / value / source / status / [Phase-24 check]) + row notes | **DROP the "Phase-24 check" column** — no Phase-24 analog in v1.6 (D-17). Replace with a "FUT-flag" column for verdict-gating figures |
| `23-DQA-CHARACTERIZATION.md` | `30-REPORTS-CHARACTERIZATION.md` | Per-file: header (path/lines/location/governance) → Provenance (git-log table) → Section Map (table) → relation-to-findings → non-authoritative status → package-inclusion recommendation → "produced with zero edits (git diff --quiet)" footer | Cover BOTH reports (v1.5 covered one). Adds the baseline-critique-mandate confirmation per ERW rule 6 |
| `23-SNAPSHOT-HASHES.txt` | `30-SNAPSHOT-HASHES.txt` | `# basename \| canonical source path \| source commit hash` lines + a package-wide pin line | Hash-verify the two read-only reports are byte-for-byte unchanged (PKG-08 acceptance) |
| delivered `02-*/research_package/DELIVERY-NOTE.md` | `03-*/…/DELIVERY-NOTE.md` | frontmatter → "How To Use This Package" (read order) → "Where The Resolution Doc Lands" (exact path) → "Resolution-Doc Format" (precedent only, no schema) → gate semantics (Phases 32–36 gate on doc landing AND Phase 31) | **REMOVE the "Phase 24 runs in parallel" section** — no Phase-24 analog. ADD the no-in-milestone-verification note |
| delivered `02-*/research_package/RESEARCH-CONTEXT-MASTER.md` | `03-*/…/RESEARCH-CONTEXT-MASTER.md` | frontmatter (`source_baseline`, `self_contained: true`) → reading order → Package Orientation And Manifest (source-treatment preamble + per-file manifest table + self-contained guarantee) → Framed Questions → CLM Register → Consolidated Context → correction provenance | The v1.5 master was the **consolidated single-file** form (5 companions folded in). Planner decides single-master vs multi-companion (Claude's discretion above) |

**Plan decomposition pattern from v1.5 Phase 23** (5 plans, [VERIFIED via SUMMARY files]):
- 23-01: DQA characterization + claims inventory (PKG-03, PKG-04) — early, gates doc list
- 23-02: **D-07 User Gate — Consolidation Plan Approval** (the user checkpoint)
- 23-03: snapshot assembly into specs/ (PKG-01)
- 23-04: framed questions (PKG-02)
- 23-05: finalize manifest + deliver + gate-open

---

## Recommended Plan Decomposition

A recommendation for the planner (not binding). Honors CONTEXT sequencing: D-19 (characterization before doc-list), D-09 (consolidation user gate before assembly), D-21 (STATE via gsd-tools), one atomic commit per plan via `scripts/agent-commit`, recovery-tag confirm/re-cut.

> **Pre-flight (every plan):** confirm branch `milestone/v1.6`; before the FIRST phase commit, confirm/re-cut recovery tag `v1.6-pre-phase-30` (see Risks — it is currently stale).

| Plan | Goal | Requirements | Deliverables | Gate / sequencing |
|------|------|--------------|--------------|-------------------|
| **30-01** | Characterize the two PKG-08 reports + seed the claims register | PKG-08 (+ PKG-07 seed) | `30-REPORTS-CHARACTERIZATION.md`, `30-CLAIMS-INVENTORY.md`, `30-SNAPSHOT-HASHES.txt` (reports + verified-facts hashes) | EARLY (D-19) — confirms report annotations + verified anchors before doc list. Read-only; hash-verify reports unchanged |
| **30-02** | Build the consolidation plan + **surface it at the hard user gate** | PKG-05 (prep) | `30-CONSOLIDATION-PLAN.md` with open inclusion calls + a "D-09 APPROVED" sign-off block | **USER GATE (D-09)** — assembly may not proceed until approved. Model as `checkpoint:human-approve` |
| **30-03** | Take byte-for-byte commit-pinned snapshots into `specs/`; build the manifest | PKG-05 (assembly) | `specs/` (6 intact snapshots + consolidated-context file), manifest in master, updated `30-SNAPSHOT-HASHES.txt` | Gated on 30-02 approval. Specs NEVER consolidated; pin `source_baseline` in master frontmatter |
| **30-04** | Author framed questions (issue-03 section order) + SCOPE-12 preamble + non-binding resolution-doc skeleton | PKG-06 (+ skeleton) | framed-questions, SCOPE-12-preamble, resolution-doc-skeleton (companion files OR master sections) | D-04/D-05/D-06 + `D` conflict posed UNSETTLED; preamble verbatim |
| **30-05** | Finalize master + `RESEARCH-AGENT-PROMPT.md` + `DELIVERY-NOTE.md`; commit package; record gate-open | delivery (op) | complete package; gate-open in STATE.md **via gsd-tools handlers** | FINAL. Verify zero repo paths in master/prompt; prompt ships with master |

**Wave ordering:** 30-01 → [user gate] 30-02 → 30-03 → 30-04 → 30-05, strictly sequential (each plan's output feeds the next; the snapshot pin must be stable before questions reference figures). 30-03 and 30-04 could overlap in principle, but the manifest (30-03) and the questions (30-04) both feed the master (30-05), and keeping them sequential avoids cross-plan churn. The user gate after 30-02 is a hard serialization point.

---

## Common Pitfalls / Risks / Landmines

### Pitfall 1: Consolidating a framework spec
**What goes wrong:** Folding `ctl_instruction.md` / `pinn_architecture.md` / `sampling_method.md` into the consolidated context file, or excerpting/summarizing them.
**Why it happens:** They are large (1868/1013/281 lines) and the consolidation rule fires for the round.
**How to avoid:** D-04 / PKG-05 hard rule — framework specs ship **byte-for-byte intact, never consolidated**. Only scattered dataset fragments + verified-facts consolidate. **Warning sign:** any `specs/` framework-spec file whose hash differs from its source.

### Pitfall 2: Leaking a repo path into an uploaded file
**What goes wrong:** A repo path (`pinn_instruction/…`, `.planning/…`, `simulation_data/…`) appears in `RESEARCH-CONTEXT-MASTER.md` or `RESEARCH-AGENT-PROMPT.md`.
**Why it happens:** Natural to "cite the source" while writing the manifest/questions.
**How to avoid:** D-05 / ERW rule 1 — companion files referenced by **bare filename** only; all repo routing lives ONLY in `DELIVERY-NOTE.md` (never uploaded). The consolidated-context file MAY retain internal per-fragment source labels (D-10), but the master/prompt may not. **Warning sign:** `grep -E '(pinn_instruction|\.planning|simulation_data|framework-specs)/' RESEARCH-CONTEXT-MASTER.md RESEARCH-AGENT-PROMPT.md` returns any hit. The v1.5 delivery verified this via a prose sweep (CLM-14+ extension) — replicate.

### Pitfall 3: Presenting a claimed figure as fact
**What goes wrong:** Stating `D = 6.694`, stage counts, or threshold tables as settled.
**Why it happens:** issue-03 states them as if settled (e.g., line 305 "D = 6.694").
**How to avoid:** PKG-07 / D-15/D-17 — every figure rows in the claims register; inline mentions reference the CLM ID; `claimed-unverified` unless a v1.5 citation exists. **Warning sign:** a figure in the master with no CLM reference.

### Pitfall 4: Editing a read-only / frozen file
**What goes wrong:** Touching `review_of_framework.md`, `stage_strat_revision.md`, `sampling_method.md`, `data_quality_assessment.md`, `ctl_instruction.md`, `pinn_architecture.md`, or anything in `pinn/`.
**How to avoid:** This phase **characterizes and snapshots only** (SPEC AC: "zero edits"). Hash-verify in `30-SNAPSHOT-HASHES.txt`; `git diff --quiet <file>` after each read. The two PKG-08 reports must be byte-for-byte unchanged (PKG-08 acceptance).

### Pitfall 5: Direct Write/Edit to STATE.md
**What goes wrong:** Recording gate-open by editing `.planning/STATE.md` directly.
**How to avoid:** D-21 / anti-pattern 15 — STATE.md mutated **only via gsd-tools state handlers** (`gsd-tools` is on PATH at `<home>/.local/bin/gsd-tools`). [VERIFIED: STATE.md exists at `.planning/STATE.md`; gsd-tools resolves on PATH.]

### Pitfall 6: Stale recovery tag (CONFIRMED THIS SESSION)
**What goes wrong:** The recovery tag `v1.6-pre-phase-30` is assumed to point at the current pre-Phase-30 HEAD, but it is orphaned.
**Evidence [VERIFIED]:** `v1.6-pre-phase-30` → `85f72f88`; current HEAD → `4f260aa3`; `git merge-base --is-ancestor 85f72f88 HEAD` returns **NO** (the milestone branch was rebased onto `master` after the tag was cut; commits 53ef6689/72926d78/f48bc36a/4f260aa3 sit on the new line, and 85f72f88 is on the orphaned pre-rebase line).
**How to avoid:** Before the first Phase 30 commit, **re-cut** `v1.6-pre-phase-30` from the current `milestone/v1.6` HEAD (CONTEXT line 145). Re-cutting a tag requires `-f` (a destructive-ish ref move) — surface to the user per the project's destructive-git governance and obtain approval, OR cut a fresh distinctly-named tag. **Do NOT proceed assuming the existing tag is a valid recovery point.**

### Pitfall 7: Forgetting the no-Phase-24 difference
**What goes wrong:** A plan assumes a later v1.6 phase will verify a package figure (copying v1.5's "Phase 24 verifies everything anyway" posture).
**How to avoid:** D-17 — there is no Phase-24 analog. The claims register carries the boundary statement; the delivery note drops the "Phase 24 runs in parallel" section. **Warning sign:** any plan text deferring verification to an in-milestone phase.

### Pitfall 8: Prompt shipped without master, or master without prompt
**How to avoid:** ERW rule (D-03) — "a package without its prompt is incomplete"; always ship `RESEARCH-AGENT-PROMPT.md` with `RESEARCH-CONTEXT-MASTER.md`. The prompt's header lists exactly which files to attach (by bare filename).

---

## Runtime State Inventory

This phase **creates** new files; it does not rename/migrate existing runtime state. One category is load-bearing:

| Category | Items Found | Action Required |
|----------|-------------|------------------|
| Stored data | None — no datastores touched | none |
| Live service config | None | none |
| OS-registered state | None | none |
| Secrets/env vars | `scripts/agent-commit` requires `GIT_AGENT_ID` + `GIT_AGENT_OWNED_PATHS`; `.githooks` must be active | set per-commit per project git policy (not a code change) |
| Build artifacts | None | none |
| **Git refs** | Recovery tag `v1.6-pre-phase-30` is **orphaned** (points at 85f72f88, not an ancestor of HEAD 4f260aa3) | **Re-cut before first commit** (Pitfall 6) — the one real runtime-state action |

---

## Open Questions / Potential Gaps for the Orchestrator

> Per the governance constraints, I do not adjudicate these — I surface them with the consulted sources and why they did not answer. The orchestrator decides whether any is a STOP-protocol gap. None of these are semantic spec/physics adjudications (those are Phases 32–36); they are package-assembly presentation/process choices, most already covered by Claude's-discretion in CONTEXT.

1. **Package directory nesting — `03-*/` root vs `03-*/research_package/`.**
   - What we know: CONTEXT D-01/D-03 say "at the round root"; the ERW runbook tree (lines 53–62) and the *delivered* v1.5 package both nest the master/specs inside `research_package/`.
   - Why sources don't resolve it: D-02 locks "one package," and the runbook's `research_package[_a|_b]/` convention is for split rounds — for a single package the directory may collapse to the round root or keep the `research_package/` subdir. Neither SPEC nor CONTEXT names the exact subdir.
   - Classification (my read): **mechanical/presentation-only** — OK for the planner/executor to choose and note. Recommend matching the v1.5 delivered form (`03-*/research_package/`). Not a gap unless the orchestrator disagrees.

2. **Single-master vs multi-companion delivered form.**
   - What we know: CONTEXT recommends shipping framed-questions/preamble/skeleton/claims-register as **named companion files**; the *delivered* v1.5 package consolidated all of them into the single `RESEARCH-CONTEXT-MASTER.md` (a post-delivery remediation).
   - Why unresolved: CONTEXT marks this Claude's discretion ("final call at assembly"); the two precedents point opposite ways.
   - Classification: **mechanical/presentation** — planner's call at assembly. Flagging because it materially shapes how many companion files the plans produce.

3. **Whether the MINOR ALM-μ_p-clamp finding gets its own framed question.**
   - What we know: it is a MINOR/INFO finding (issue-03 line 117, 489–505), feeds LOOP-05, and is not in the SPEC-locked selected set (which is "at least" that set).
   - Why unresolved: PKG-06 says "each contested or unverified finding"; the clamp is a settled INFO recommendation, not contested — but it is a training-loop contract item.
   - Classification: **process/coverage choice** — recommend surfacing it as an open inclusion call at the D-09 checkpoint (the user decides coverage breadth). Not a semantic gap.

4. **Exact commit to pin `source_baseline` to, given the orphaned recovery tag.**
   - What we know: D-04 pins snapshots to a commit in the master frontmatter; the recovery tag is stale (Pitfall 6).
   - Why unresolved: the pin commit should be the package-creation HEAD, but the recovery-tag re-cut (a ref move needing user approval) and the pin interact.
   - Classification: **operational coordination** — resolve by pinning to the actual HEAD at assembly time (30-03) after the recovery tag is re-cut. Log the chosen pin in `30-SNAPSHOT-HASHES.txt`. Not a semantic gap, but the planner should sequence the tag re-cut before the pin.

---

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| `gsd-tools` | STATE.md gate-open record (D-21) | ✓ | on PATH (`<home>/.local/bin/gsd-tools`) [VERIFIED] | none needed |
| `scripts/agent-commit` | one atomic commit per plan | ✓ (referenced by repo git policy) | — | none — mandatory commit path |
| `git` | snapshots, hashes, provenance, tag re-cut | ✓ | — | none |
| Source files (issue-03, specs, reports, v1.5 facts) | every deliverable | ✓ all present [VERIFIED] | — | none |
| doc-03 target dir | package location (D-01) | ✗ (absent — gate closed) | — | this phase CREATES it |
| Web / package registries | — | N/A | — | not used; internal-only phase |

**Missing dependencies with no fallback:** none (all inputs present; the absent target dir is created by the phase, as expected).

---

## Validation Architecture

> `.planning/config.json` was not located with a `workflow.nyquist_validation` key in scope for this doc-assembly phase. This phase produces **documentation artifacts**, not code, so "tests" are acceptance-check sweeps, not a unit-test framework.

### Acceptance-check approach (from SPEC AC + ERW rules)
| Check | Command / method | Pass criterion |
|-------|------------------|----------------|
| Zero repo paths in uploads | `grep -E '(pinn_instruction\|\.planning\|simulation_data\|framework-specs\|pinn/)' RESEARCH-CONTEXT-MASTER.md RESEARCH-AGENT-PROMPT.md` | zero hits |
| Specs byte-for-byte intact | per-file SHA-256 in `30-SNAPSHOT-HASHES.txt` vs source | hashes match source-commit snapshot |
| Read-only reports unchanged | `git diff --quiet <report>` after characterization | exit 0 (no diff) |
| Every figure registered | manual sweep: each numeric figure in master references a CLM ID | no unregistered figure |
| SCOPE-12 preamble verbatim | diff preamble text vs the SCOPE-12 constraint list | exact match |
| Coverage ≥ selected set | checklist: B-07,B-08,M6,M7,M14,M15,M16,D5,NS-12/13/18,D-04,D-05,D-06,`D=6.694` each has a question | all present |
| D-04/D-05/D-06 + `D` unsettled | inspect each — states both positions, no resolution | no presupposed verdict |
| Delivery note has landing path + gate | inspect `DELIVERY-NOTE.md` | exact path + "Phases 32–36 gate on doc landing AND Phase 31" |
| Gate-open via gsd-tools | STATE.md changed only through handler | no direct Write/Edit to STATE.md |

### Wave 0 gaps
- None — no test framework needed; acceptance is doc-sweep + hash verification. The `30-SNAPSHOT-HASHES.txt` is created in 30-01/30-03 and is the standing evidence.

---

## Security Domain

This phase writes documentation artifacts and takes read-only snapshots; it runs no code, accepts no external input at runtime, and installs nothing. Standard application-security ASVS categories do not apply. The one security-adjacent concern is **information governance**, not software security:

| Concern | Control |
|---------|---------|
| Leaking internal repo structure to external AI agents | ERW rule 1 / D-05 — zero repo paths in uploads; all routing in the never-uploaded delivery note |
| Destructive git ref operation (recovery-tag re-cut) | Project destructive-git governance — surface and obtain approval before `git tag -f` (Pitfall 6) |
| Accidental edit to read-only source-of-truth specs | hash-verification + `git diff --quiet` (PKG-08 acceptance) |

No `security_enforcement` software controls are in scope for a doc-assembly phase.

---

## State of the Art / v1.6 ≠ v1.5 Deltas

| v1.5 (Phase 23) approach | v1.6 (Phase 30) approach | Why changed |
|--------------------------|--------------------------|-------------|
| Parallel Phase 24 verifies every claimed figure | **No Phase-24 analog**; figures carry `claimed-unverified` honestly, verification → FUT | doc-03 dataset facts settled in v1.5; remaining empirical work is FUT/trainex (D-17) |
| Claims inventory has a "Phase-24 check" column | Claims register has a "FUT-flag" column instead | no in-milestone verifier |
| Delivery note "Phase 24 runs in parallel" section | Delivery note drops it; adds no-in-milestone-verification note | same |
| Questions grouped by **contract cluster** (mirrors adjudication phases) | Questions grouped by **issue-03 section order**; finding→phase map lives in the skeleton | SPEC Round-1 lock (D-11) |
| One PKG-08 report characterized (DQA) | **Two** reports characterized (review_of_framework + stage_strat_revision) | doc-03 cites two curriculum-relevant reports |
| Optional `data_quality_assessment.md` inclusion | `data_quality_assessment.md` not a doc-03 input; two new reports instead | different finding domain |

---

## Sources

### Primary (HIGH confidence — read directly this session)
- `.planning/phases/30-research-package-assembly/30-SPEC.md` — 6 locked requirements, boundaries, AC
- `.planning/phases/30-research-package-assembly/30-CONTEXT.md` — D-01..D-22
- `.planning/REQUIREMENTS.md` — PKG-05..08, SCOPE-08..15, source-treatment policy, VER-14
- `.planning/ROADMAP.md` — v1.6 section, Phase 30/31 entries, external-gate semantics
- `docs/runbooks/external-research/2026-06-11-external-research-workflow.md` — the ERW runbook (14 rules, file set, channel)
- `pinn_instruction/issues/03-curriculum-and-training-loop.md` (711 lines) — full finding inventory + section order
- `.planning/milestones/v1.5-phases/23-research-package-assembly/{23-CONSOLIDATION-PLAN,23-CLAIMS-INVENTORY,23-DQA-CHARACTERIZATION,23-CONTEXT}.md` + `23-SNAPSHOT-HASHES.txt` — direct templates
- delivered v1.5 package `…/research_reports/02-data-pipeline-and-validation/research_package/{DELIVERY-NOTE,RESEARCH-CONTEXT-MASTER}.md` — concrete delivered form
- `.planning/milestones/v1.5-phases/24-empirical-dataset-verification-and-correction-addendum/24-VERIFIED-FACTS.md` — the v1.5-verified-facts source (CLM-01..13 verdicts)
- `pinn_instruction/markdown_conversion/framework-revisions/review-of-framework/review_of_framework.md` (529 lines) — PKG-08 subject
- `pinn_instruction/markdown_conversion/framework-revisions/stage-strat-revision/stage_strat_revision.md` (427 lines) — PKG-08 subject
- `pinn_instruction/markdown_conversion/framework-specs/{ctl_instruction,pinn_architecture,sampling_method}.md` — intact spec inputs (sizes/anchors verified)
- `simulation_data/Documentation/{README.md,standard_quasi_random_ids_not_in_gold.md}` — verified-anchor citations
- `git` ref state — recovery-tag orphaning confirmed (`v1.6-pre-phase-30` → 85f72f88; HEAD → 4f260aa3; not ancestor)

### Secondary / Tertiary
- None — no web search or external lookup performed (internal-only phase, per the objective).

## Metadata

**Confidence breakdown:**
- ERW package blueprint: HIGH — runbook + delivered v1.5 package read directly
- issue-03 finding inventory: HIGH — full doc read, line ranges verified
- Consolidation map: HIGH — D-09/D-22 + v1.5 template
- Claims register seed: HIGH — verified anchors carry exact v1.5 citations (24-VERIFIED-FACTS.md, ctl_instruction.md:910/915)
- PKG-08 characterization scope: HIGH — both reports' headings scanned; provenance to be confirmed via git-log at execution
- Plan decomposition: MEDIUM-HIGH — recommendation modeled on the verified v1.5 5-plan pattern; final shape is the planner's call
- Recovery-tag caveat: HIGH — confirmed by direct git inspection this session

**Research date:** 2026-06-18
**Valid until:** stable until the worktree HEAD moves or any input source is edited; re-confirm the `source_baseline` pin and recovery-tag state at assembly time (they are HEAD-sensitive).
