# Phase 30: Research Package Assembly - Context

**Gathered:** 2026-06-18
**Status:** Ready for planning
**Mode:** `--auto --all` — all gray areas auto-selected; recommended options chosen by Claude and logged in `30-DISCUSSION-LOG.md`. The user did not interactively ratify these; every decision is grounded in `30-SPEC.md` / `.planning/ROADMAP.md` / `.planning/REQUIREMENTS.md` / the ERW runbook / the v1.5 Phase 23 precedent, and marked Claude's discretion otherwise. **No source-silent semantic decision arose** — all decisions below are operational / presentation form, so the STOP protocol recorded no gap (nothing invented). Run from the isolated `milestone/v1.6` worktree (`../3_body_problem-v1.6`).

<domain>
## Phase Boundary

Deliver a complete, self-contained, ERW-conformant external-research package for issue-03 (curriculum + training loop), then hand it off to the user — on delivery the external resolution-doc gate opens. The package contains: (1) an annotated document list — every document needed to adjudicate the issue-03 findings, each role-annotated, scattered fragments consolidated into a single context file with the consolidation plan surfaced to the user before assembly (PKG-05); (2) framed research questions — each contested/unverified finding posed as an explicit neutral question, by issue-03's own section order, with the locked v1.4 + v1.5 outcomes as verbatim hard constraints, and D-04/D-05/D-06 + the `D = 6.694` conflict posed unsettled (PKG-06); (3) a non-binding per-finding resolution-doc skeleton (PKG-06 support); (4) a claimed-vs-verified figure register, every figure `claimed-unverified` unless v1.5-verified (PKG-07); (5) a read-only characterization of `review_of_framework.md` + `stage_strat_revision.md` reported to the user (PKG-08); (6) delivery + gate-open STATE record.

**Not this phase:** any adjudication, verdict, evidence packet, or framework-spec edit (Phases 32–36); any empirical verification of a dataset figure (there is **no Phase-24 analog in v1.6** — verification is delegated to external research / FUT); any edit to `ctl_instruction.md` / `pinn_architecture.md` (Phases 33–35), `sampling_method.md` (SCOPE-08), `data_quality_assessment.md` / the two reports (SCOPE-09); any `pinn/` reference as grounding (SCOPE-10); running probes (Phases 33–36).

**Governance:** v1.6 runs under the full STOP protocol (`CLAUDE.md`/`AGENTS.md` "CRITICAL GOVERNANCE", adjudication-milestone applicability). Source-silent semantic / process-schema / cross-phase decisions are surfaced as gaps in `30-GAPS.md` + `.planning/milestones/v1.6-GAPS.md` (create on first gap), never invented.

</domain>

<spec_lock>
## Requirements (locked via SPEC.md)

**6 requirements are locked** (PKG-05, PKG-06, PKG-07, PKG-08, the non-binding resolution-doc skeleton, and the operational delivery / gate-open requirement). See `30-SPEC.md` for full requirements, boundaries, and acceptance criteria (ambiguity score 0.105, gate ≤ 0.20).

Downstream agents MUST read `30-SPEC.md` before planning or implementing. Requirements are not duplicated here.

**In scope (from SPEC.md):**
- An ERW-conformant package at `framework-revisions/research_reports/03-curriculum-and-training-loop/` (`DELIVERY-NOTE.md`, `RESEARCH-CONTEXT-MASTER.md`, `RESEARCH-AGENT-PROMPT.md`, `specs/` commit-pinned snapshots).
- The annotated document list with the locked input set (issue-03 + the two intact spec targets + the two reports + `sampling_method.md` + v1.5-verified-facts reference + consolidated fragments as needed).
- Neutrally-framed research questions (by issue-03 section order) + the SCOPE-12 hard-constraints preamble.
- The non-binding per-finding resolution-doc skeleton.
- The claimed-vs-verified figure register.
- The read-only characterization of `review_of_framework.md` and `stage_strat_revision.md`.
- Delivery note + gate-open STATE record (via gsd-tools handlers).

**Out of scope (from SPEC.md):** empirical verification of any dataset figure (no Phase-24 analog); any adjudication / verdict / evidence packet / framework-spec edit (Phases 32–36); editing `ctl_instruction.md` / `pinn_architecture.md` (they ship as intact snapshots only); editing `review_of_framework.md` / `stage_strat_revision.md` / `sampling_method.md` / `data_quality_assessment.md`; any `pinn/` reference as grounding (SCOPE-10); running probes; prescribing a binding resolution-doc schema; settling D-04 / D-05 / D-06 or the `D` conflict.

</spec_lock>

<decisions>
## Implementation Decisions

> All decisions are HOW-to-assemble choices (the SPEC locks WHAT). Each is grounded in the ERW runbook + the v1.5 Phase 23 precedent (`23-CONTEXT.md` D-01..D-17) unless marked Claude's discretion.

### Package location & delivery form
- **D-01:** Package lives at `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/` — co-located with where the resolution doc must land, mirroring the v1.4 (`research_reports/01-*/`) and v1.5 (`research_reports/02-*/`) layout. (Dir is absent today — gate closed; this phase creates it.)
- **D-02:** **One** research package (NOT split into `research_package_a/_b`). Rationale: this is a **specwork** issue-doc round (the issue-01 / issue-02 convention is one package per issue), not a build-design foundational round; the ERW rule-10 split targets `trainex`-style build-design rounds. The SPEC's deliverable list is a single package.
- **D-03:** ERW-fixed file set at the round root: `DELIVERY-NOTE.md` (user-only, **never uploaded**), `RESEARCH-CONTEXT-MASTER.md` (the single uploaded entry point), `RESEARCH-AGENT-PROMPT.md` (paste-ready; **ships with the master — a package without its prompt is incomplete**), `specs/` (one shared commit-pinned snapshot set).
- **D-04:** Self-contained snapshots in `specs/`, pinned to a commit hash recorded in the master frontmatter (`source_baseline`); if a source is edited after packaging, refresh the snapshot (ERW rule 5). Framework specs (`ctl_instruction.md`, `pinn_architecture.md`, `sampling_method.md`) are copied **byte-for-byte intact** — NEVER consolidated, excerpted, or summarized (PKG-05 hard rule).
- **D-05:** **Zero repo paths in any authored upload** (master + prompt); companion files referenced by **bare filename** in a manifest table with per-file treatment instructions; all repo routing lives ONLY in `DELIVERY-NOTE.md` (ERW rules 1–2).

### Document list (candidate inventory; final list locked at execution)
- **D-06:** Inclusion criterion — a document enters the list iff at least one issue-03 finding needs it for adjudication (PKG-05). The final list is locked during execution AFTER the PKG-08 reports characterization (D-19/D-20) and AFTER the consolidation plan is surfaced to the user (D-09).
- **D-07:** Locked input set (from `30-SPEC.md`): `03-curriculum-and-training-loop.md` (intact); `ctl_instruction.md` + `pinn_architecture.md` (intact spec-edit targets, carry the locked v1.4/v1.5 conventions); `review_of_framework.md` + `stage_strat_revision.md` (each shipped with a **baseline-critique mandate**, ERW rule 6); `sampling_method.md` (intact, annotated **FROZEN**/historical, SCOPE-08); and a consolidated **v1.5-verified-facts reference**.
- **D-08:** `pinn/` live code is EXCLUDED. The package states, as a hard constraint to the external research, that issue-03's "Canonical" citations of `data-processing-pipeline-full.py` / `basic_architecture.py` are overridden (SCOPE-10, directive 2026-05-19) and the framework specs are source of truth. Issue-01 (doc-01) and issue-02 (doc-02) are NOT included — resolved; their outcomes travel as the SCOPE-12 locked-constraints block + the intact specs.

### Consolidation plan + hard user checkpoint
- **D-09:** The deliverable set exceeds ~5 files, so the PKG-05 consolidation rule fires: scattered fragments consolidate into ONE context file (framework specs never consolidated, per D-04). **Hard execution checkpoint: the consolidation plan (what gets consolidated vs. stays standalone) is surfaced to the user BEFORE assembly** — a PKG-05 requirement, not a courtesy (the v1.5 D-07 analog). The planner MUST model this as a user gate.
- **D-10:** The consolidated context file is a companion **grounding** (snapshot-class) file: per ERW rule 1 it MAY retain internal per-fragment source-path provenance labels; the **master and prompt** carry zero repo paths and reference it by bare filename.

### Research-question framing (PKG-06)
- **D-11:** ONE questions document, organized by **issue-03's own section order** (audit §§6–7 → Causal Training Mismatch blueprint → stage-assignment methodology → next-steps fragments) — per the SPEC's locked Round-1 decision. (This deliberately differs from Phase 23's contract-cluster grouping; the per-finding skeleton (D-13) carries the downstream finding→phase mapping instead.) Coverage is **at least** {B-07, B-08, M6, M7, M14, M15, M16, D5, NS-12/13/18, **D-04**, **D-05**, **D-06**, `D = 6.694` vs `D ≈ 4.6416`}; the full finding inventory is locked during assembly **after reading issue-03 in full**.
- **D-12:** Neutral framing rule — each question states the issue-doc position AND the current framework-spec position WITHOUT presupposing a resolution; D-04/D-05/D-06 + the `D` conflict appear **unsettled**. The package tells the external research that BOTH the issue doc and its "Recommended Resolutions" are non-authoritative and may contain errors, citing the `D = 6.694` vs locked raw-mass `D ≈ 4.6416` (v1.5 Phase 25 EVID-10) as the worked seed-conflict example.
- **D-13:** A shared hard-constraints preamble lists the SCOPE-12 locked v1.4 + v1.5 outcomes **verbatim**: 14D input `[τ, IC₁₃]`, Jacobi IC₁₃, mass-weighted COM projection head, PHYS-03 `eps_soft = 1e-5`, post-v1.3 SCS gate `ε_H > 10⁻⁵` / `SCS > −5`, PHYS-01 raw-mass `D ≈ 4.6416`, and the v1.5 data-side contracts PIPE-01..10 / VAL-01..04 — plus the SCOPE-10 hard constraint (`pinn/` citations overridden).

### Resolution-doc skeleton (PKG-06 support; user-locked non-binding)
- **D-14:** Ship a per-finding skeleton — one section per selected finding — explicitly marked **non-binding** ("the resolution doc remains the user's product; this is a suggestion to ease coverage-checking"), citing v1.4 `ctl_pinn_resolution.md` and v1.5 `02-resolution-doc.md` as format precedents. No schema mandated. The skeleton carries the downstream finding → adjudication-phase (32–36) mapping.

### Claims register (PKG-07)
- **D-15:** A dedicated claims register with stable IDs (`CLM-01`, `CLM-02`, …): every dataset/empirical figure stated anywhere in the package rows as `claimed-unverified` (issue-doc value) or `verified` (with its v1.5 citation); all inline figure mentions reference their CLM ID.
- **D-16:** Conservative verified-status rule — only v1.5-verified facts (committed v1.5 artifacts + `simulation_data/Documentation/`) count as "verified"; when in doubt, mark `claimed-unverified`.
- **D-17:** **No-in-milestone-verification boundary (the single most important v1.6 ≠ v1.5 difference):** v1.6 has no Phase-24 analog, so NO in-milestone phase verifies these claims. The register MUST state this — `claimed-unverified` figures are unverified inputs (not fact), and any figure that would gate a verdict is flagged for FUT empirical check. Enumerate at minimum the `D = 6.694` derivation inputs and the stage trajectory counts (claimed-unverified), and the v1.5 anchors stated as `verified` with citation (the 184 standard IDs without gold, the ~2,565 quasi-random gold count, per-variant snapshot/`dt_out` distributions).

### Reports characterization (PKG-08)
- **D-18:** Deliverable is a standalone phase artifact `.planning/phases/30-research-package-assembly/30-REPORTS-CHARACTERIZATION.md` (the `23-DQA-CHARACTERIZATION.md` analog) covering BOTH reports: git provenance/history, section-by-section content map, relation to the doc-03 findings, and a package-role recommendation (baseline design intent vs. hard constraint, ERW rule 6). Zero edits; both files byte-for-byte unchanged, hash-verified in a `30-SNAPSHOT-HASHES.txt` analog. Reported to the user.
- **D-19:** Sequencing — the characterization completes BEFORE the document list is finalized (it confirms each report's shipping annotation), so it is an early task (the D-15 Phase-23 sequencing analog).

### Gate-opening record & handoff
- **D-20:** Delivery = package committed + a `DELIVERY-NOTE.md` (user-only, never uploaded) stating: how to run the ERW multi-AI handoff; that the resolution doc must land under `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/`; that v1.4 `ctl_pinn_resolution.md` / v1.5 `02-resolution-doc.md` are format precedents (suggestion only — no required schema); and that adjudication Phases 32–36 gate on the consolidated doc landing **AND** Phase 31 passing.
- **D-21:** The gate-open state is recorded in STATE.md via **gsd-tools state handlers only** (no direct Write/Edit), per universal anti-pattern 15 and ROADMAP success criterion 5.

### Claude's Discretion
- Exact filenames / placement of the questions document, the SCOPE-12 preamble, the claims register, and the resolution-doc skeleton — whether each is a **named companion file** (referenced by bare filename, each a clean attachable unit) or a **section of `RESEARCH-CONTEXT-MASTER.md`**. Recommended: ship the framed questions + preamble + skeleton + claims register as named companion files alongside the master; final call at assembly. Keep names self-describing and kebab/snake-consistent with the repo + ERW conventions.
- Which `simulation_data` / v1.5 excerpts enter the consolidated context file (**D-22 below**) — judged per-finding during execution within the D-06 criterion and shown at the D-09 consolidation checkpoint.
- Whether the v1.5-verified-facts reference is a standalone companion file or folded into the consolidated context file — recommended standalone (it is reused by the claims register and the preamble).

### simulation_data excerpt selection (operational note)
- **D-22:** For doc-03 (curriculum + training loop), provenance is **less dataset-centric** than v1.5 (the data-pipeline milestone): the findings turn mostly on the framework specs and the audit pseudocode embedded in issue-03. So `simulation_data` excerpts are expected to be **minimal** — include only the v1.5-verified facts that the curriculum-staging / training-loop contracts depend on (e.g., per-variant snapshot / `dt_out` distributions that bound `tau_L` / `L_max` and `dt_out`-aware collocation scaling; stage-assignment-relevant counts) plus the claims-register anchors. Source v1.5-verified facts from `simulation_data/Documentation/` + committed v1.5 artifacts (D-16 conservative rule). Final selection rides the D-09 checkpoint.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase requirements & protocol (read first)
- `.planning/phases/30-research-package-assembly/30-SPEC.md` — the 6 LOCKED requirements (PKG-05..08 + skeleton + delivery), boundaries, constraints, acceptance criteria. Read before anything else.
- `.planning/REQUIREMENTS.md` — PKG-05..08 verbatim, SCOPE-08..15 boundaries, VER-14 traceability, source-treatment policy.
- `.planning/ROADMAP.md` §"v1.6 Resolving 03 Curriculum and Training Loop" — milestone goal, "Source treatment & STOP protocol", "Verification protocol", §"Phase 30" goal + the ⛔ external-gate semantics.
- `CLAUDE.md` / `AGENTS.md` §"CRITICAL GOVERNANCE" — the STOP protocol (adjudication-milestone applicability). Gap registers: `30-GAPS.md` (phase-local) + `.planning/milestones/v1.6-GAPS.md` (milestone index) — neither exists yet; create on first gap.

### Canonical assembly spec (the package blueprint)
- `docs/runbooks/external-research/2026-06-11-external-research-workflow.md` — the ERW runbook: package file set, the 14 hard-won rules, channel = **specwork** (candidate-verdict-source standing, full verification protocol applies downstream).

### Adjudication subject & spec-edit targets (package inputs — shipped intact)
- `pinn_instruction/issues/03-curriculum-and-training-loop.md` — the issue doc (711 lines; NON-authoritative); source of the framed questions. Carries the `D = 6.694` tension and the overridden `pinn/` "Canonical" citations.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` — spec-edit target (Phases 33–35); intact copy; carries curriculum-staging / `tau_L`/`L_max` / loss-scaling contracts.
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` — spec-edit target (Phases 34/35); intact copy; carries gradient-clipping / training-strategy contracts.
- `pinn_instruction/markdown_conversion/framework-specs/sampling_method.md` — FROZEN (SCOPE-08); intact copy, annotated historical.

### PKG-08 characterization subjects (read-only — characterize, never edit)
- `pinn_instruction/markdown_conversion/framework-revisions/review-of-framework/review_of_framework.md` — read-only; provenance + content map + doc-03 relation; baseline-critique mandate.
- `pinn_instruction/markdown_conversion/framework-revisions/stage-strat-revision/stage_strat_revision.md` — read-only; same characterization treatment.

### v1.5-verified facts (claims register + verified-facts reference)
- `simulation_data/Documentation/README.md` — canonical dataset spec.
- `simulation_data/Documentation/standard_quasi_random_ids_not_in_gold.md` — the 184 standard IDs without gold (v1.5-grounded anchor).
- `.planning/milestones/v1.5-phases/` — committed v1.5 artifacts that ground "verified" status (e.g., Phase 25 EVID-10 rejecting `D = 6.694`; dataset-fact verifications). Conservative rule D-16 applies.

### Precedents (format + process — directly reusable)
- `.planning/milestones/v1.5-phases/23-research-package-assembly/` — the DIRECT analog. Reuse: `23-CONTEXT.md` (D-01..D-17), `23-CONSOLIDATION-PLAN.md`, `23-CLAIMS-INVENTORY.md`, `23-DQA-CHARACTERIZATION.md`, `23-SNAPSHOT-HASHES.txt`, `23-DELIVERY-NOTE` patterns.
- `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md` — v1.4 resolution-doc format precedent.
- `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/02-resolution-doc.md` — v1.5 resolution-doc format precedent; the `02-*/` directory is the package layout precedent.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- The ERW package skeleton (`DELIVERY-NOTE.md` / `RESEARCH-CONTEXT-MASTER.md` / `RESEARCH-AGENT-PROMPT.md` / `specs/`) — reused verbatim in form from the runbook + the v1.5 `02-*/` package.
- The v1.4 (`research_reports/01-*/`) and v1.5 (`research_reports/02-*/`) directory layout — the layout `03-*/` mirrors (D-01).
- The v1.5 Phase 23 artifacts (`23-CONSOLIDATION-PLAN.md`, `23-CLAIMS-INVENTORY.md`, `23-DQA-CHARACTERIZATION.md`, `23-SNAPSHOT-HASHES.txt`) — concrete templates for the doc-03 analogs (consolidation plan, claims register, `30-REPORTS-CHARACTERIZATION.md`, `30-SNAPSHOT-HASHES.txt`).
- `scripts/agent-commit` — mandatory commit path (set `GIT_AGENT_ID` + `GIT_AGENT_OWNED_PATHS`; `.githooks` active); one atomic commit per plan.

### Established Patterns
- Phase artifacts named `NN-*.md` in `.planning/phases/NN-slug/` (characterization → `30-REPORTS-CHARACTERIZATION.md`; hashes → `30-SNAPSHOT-HASHES.txt`).
- STATE.md mutated only via gsd-tools handlers (anti-pattern 15).
- Snapshot hash-verification proves read-only files are byte-for-byte unchanged (PKG-08 acceptance).
- One uploaded entry point (the master) + bare-filename manifest; repo routing isolated to the never-uploaded delivery note.

### Integration Points
- **Phase 31** (Resolution Doc Readiness Verification) consumes the resolution-doc skeleton (D-14) + the framed-questions coverage set as its readiness checklist; the package's selected-finding set must be ≥ the Phase-31-SC1 set.
- **Phases 32–36** gate on the consolidated resolution doc landing at `research_reports/03-curriculum-and-training-loop/` **AND** Phase 31 passing — the `DELIVERY-NOTE.md` (D-20) must state this path + gate exactly.
- The claims register (D-15) flags FUT empirical checks (no in-milestone verifier, D-17) — this feeds the Phase 36 FUT-01/FUT-04 handoff.
- **Recovery-tag caveat:** `v1.6-pre-phase-30` exists but was likely cut before `milestone/v1.6` was rebased onto `master` (HEAD is now `53ef6689`); the planner/executor should confirm the tag points at the current pre-Phase-30 HEAD and re-cut it if the rebase orphaned it, before the first Phase 30 commit.

</code_context>

<specifics>
## Specific Ideas

- The package must be consumable by **repo-blind** external AI agents: self-contained snapshots, no repo-relative reference that dangles outside the upload set (D-05). The only place repo paths live is the never-uploaded `DELIVERY-NOTE.md`.
- The `D = 6.694` vs locked raw-mass `D ≈ 4.6416` conflict is the worked example of why the issue doc is non-authoritative — cite it explicitly in the source-treatment preamble (D-12).
- The defining structural difference from the v1.5 analog: **no in-milestone phase verifies the claims** (no Phase-24 analog). The package must carry "claimed, unverified" honestly and delegate verification to the external research / FUT (D-17). Plans must not assume any later v1.6 phase will check a package figure.

</specifics>

<deferred>
## Deferred Ideas

- Prescribing a binding schema for the user's resolution doc — rejected (user-locked: a non-binding per-finding skeleton only, D-14). If the adjudication phases later need a minimum structure, that is a Phase 31/32 concern.
- Any empirical probe or figure verification — out of scope; there is no Phase-24 analog in v1.6 (FUT / trainex). The package states claims only.
- Settling D-04 (causal training mode) / D-05 (s_min frame) / D-06 (epsilon strategy) or the `D` conflict — posed neutrally here; resolved later via the resolution doc + Phase 32 root-cause adjudication.

### Reviewed Todos (not folded)
- **"Review and hand off the trainex-r1 research sub-packages (r1a + r1b)"** (`.planning/todos/.../trainex-r1-research-handoff.md`, match score 0.6) — REVIEWED, **NOT folded**. It belongs to the **trainex track** (training-execution; the ERW **build-design** channel; packages under `framework-specs/trainex-r1/`), a different track from this phase's **specwork / doc-03** package (issue-03 adjudication; `research_reports/03-*/`). It keyword-matched only because both tracks cite the same ERW runbook. The `30-SPEC` scope locks Phase 30 to the doc-03 package, and ERW channel separation is absolute, so folding a cross-track deliverable would violate the locked boundary. It remains an open trainex-track user action, untouched by Phase 30.

</deferred>

---

*Phase: 30-research-package-assembly*
*Context gathered: 2026-06-18*
