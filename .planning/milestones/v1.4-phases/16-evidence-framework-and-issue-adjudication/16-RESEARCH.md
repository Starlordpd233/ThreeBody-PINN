# Phase 16: evidence-framework-and-issue-adjudication - Research

**Researched:** 2026-05-16
**Domain:** Evidence governance, issue-ledger protocol, documentation traceability [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:7-18]
**Confidence:** HIGH [VERIFIED: local source docs, planning docs, and repo scans completed 2026-05-16]

<user_constraints>
## User Constraints (from CONTEXT.md)

Provenance for the verbatim constraints in this section: [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md]

### Locked Decisions
## Implementation Decisions

### Ledger directory and path reconciliation

- **D-01:** Canonical ledger path is `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md` (matches the actual phase slug from `init.phase-op`). The shorter path `.planning/milestones/v1.4-phases/16-evidence-framework/16-ISSUE-LEDGER.md` referenced in ROADMAP.md §"Phase 16" / REQUIREMENTS.md §VER-05 / PROJECT.md "v1.4 phase summary" is a stale draft path from before the phase was created. Phase 16 updates those three references to match.
  - **Why:** Two paths for the same artifact creates drift the moment anything else cites the ledger. Pick one — the slug — and reconcile upstream docs.
  - **How to apply:** Phase 16 plan must include doc edits to ROADMAP.md, REQUIREMENTS.md (VER-05 line), and PROJECT.md (Active section + Phase Summary table) that replace `16-evidence-framework/` with `16-evidence-framework-and-issue-adjudication/`. No content change beyond the path.

### Ledger schema and file layout

- **D-02:** `16-ISSUE-LEDGER.md` is a single Markdown file with two sections:
  1. **Status Table** — one row per in-scope finding with columns: `ID | Title | Phase | Status | Verdict | Sources Disagree? | Evidence Packet | Acceptance Check | Spec Section | Dependents | Last Updated`. Status uses the fixed enum `PENDING | IN_PROGRESS | FIX_APPLIED | VERIFIED | DEFERRED`. Verdict uses the EVID-02 enum `accept-resolution | accept-issue-doc | accept-third-position | reject-both-as-unsupported | defer-with-blocker` (or `-` while `PENDING`).
  2. **Per-finding notes** — one H3 subsection per finding containing only metadata that does NOT fit the table: deferral reason (for `DEFERRED`), status-transition log (timestamped entries appended at each transition), and links to the evidence packet plus any related plans/commits.
- **D-03:** YAML frontmatter at the top of the ledger lists `total_findings`, `in_scope_findings`, `deferred_findings`, `last_verified_traceability` (the VER-02 statement: "30/30 v1.4 requirements mapped exactly once — verified `<date>` against REQUIREMENTS.md §Traceability").
- **D-04:** Status transitions are explicit ledger edits performed in the same commit as the underlying spec/code change. "Fix applied" without a corresponding ledger update is a phase-exit blocker; phase verifiers reject the exit. The transition log inside the per-finding subsection records who/what changed status (commit short SHA) and when.

### Evidence packet location and granularity

- **D-05:** One file per finding under `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/evidence/{finding-id}.md`. Example paths: `evidence/B-02.md`, `evidence/B-09.md`, `evidence/M5.md`. Greppable, scales naturally, isolates contested adjudications, and keeps the ledger table lean.
  - **Why:** Embedding packets inside `16-ISSUE-LEDGER.md` would make the file grow past readability and force every status-table edit to compete for diff space with packet prose. Two files, one job each.
  - **How to apply:** Phase 16 creates the `evidence/` directory, a `_TEMPLATE.md` (D-06), and a `README.md` that documents the protocol. Phase 17 onward fills in one packet per finding as it is worked.

### Evidence packet template (fixed schema)

- **D-06:** Every packet `evidence/{id}.md` follows this fixed schema. Required sections are MANDATORY — no packet is accepted at phase exit without each non-conditional section filled.
  1. **Header** — `ID`, `title`, `severity` (BLOCKING/MAJOR/MINOR/INFO), `current status`, `current verdict`, `phase` (17/18/19/20/21), `acceptance check ID`, `spec sections touched`, `code paths touched (if any)`.
  2. **Source positions** — verbatim quote with line-range citation from `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md` AND from `pinn_instruction/issues/01-architecture-and-physics-foundations.md`. Both are required even when the verdict will be `accept-resolution` or `accept-issue-doc` — proving the disagreement (or lack thereof) is part of the audit.
  3. **Spec evidence** — line-range citations from the current framework specs (`pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md`, `pinn_architecture.md`, `sampling_method.md`) showing the convention being changed (or kept).
  4. **Code evidence** — line-range citations from `pinn/basic_architecture.py` and/or `pinn/data-processing-pipeline-full.py` ONLY when the finding's verdict can be checked against live code (e.g., B-01 SIREN init, M5 `I3_norm` mapping, IO-03 COM projection head). Skip with explicit "Not code-applicable" otherwise. *(Pre-2026-05-19; superseded by no-live-code directive. Renamed to "FUT-01 Hand-off Note" in the updated template.)*
  5. **First-principles physics check** — REQUIRED for EVID-05 contested findings (B-02 D formula, B-04 orientation slots, B-09 softening, M5 `I3` mapping, plus any further conflict discovered). The check names the physical law or dimensional argument applied (Newtonian N-body equations, dimensional analysis, SIREN initialization variance, ALM constraint theory) and shows the worked argument or numerical comparison.
  6. **Verdict** — one of `accept-resolution`, `accept-issue-doc`, `accept-third-position`, `reject-both-as-unsupported`, `defer-with-blocker`. EVID-02 enum is enforced.
  7. **Root-cause framework ambiguity** — REQUIRED for EVID-05; a one-paragraph statement naming the specific spec passage or contract whose ambiguity allowed the two sources to disagree.
  8. **Locked convention** — REQUIRED for EVID-05; the explicit convention now adopted, stated in spec-edit-ready prose.
  9. **Which source was correct / which was wrong** — REQUIRED for EVID-05; assigns correctness on a per-claim basis with reasoning. May say "both were correct on X, both were wrong on Y, neither addressed Z".
  10. **Before / after spec note** — for accepted edits, the spec section name + a short summary of the contract it now enforces. For `accept-resolution`-as-no-change findings (false positives), names the section and confirms no edit.
  11. **Named acceptance check** — the AC-ID reserved here (e.g., `AC-PHYS-02-COMP-AD`); pass criteria defined fully in Phase 21 per VER-01.
  12. **Status transition log** — appended on each transition with date and commit short SHA (mirrored in the ledger row's per-finding subsection).

### Initial finding inventory (seed for the ledger)

- **D-07:** The Phase 16 ledger ships with one row per finding from the master list below. Phases 17–21 update statuses, verdicts, and add packets — they do NOT add or remove rows except by explicit scope change recorded in the ledger subsection. The inventory is locked here so downstream phases work against a known surface.

  - **BLOCKING (B-series):** B-01, B-02, B-03, B-04, B-05, B-06, B-07, B-08, B-09, B-10 (each mapped to its phase per the phase→requirements table; B-11 listed in the issue doc's cross-issue interactions is folded into B-05 since both concern COM/mass consistency — explicit note in the B-05 subsection records the fold).
  - **MAJOR (M-series):** M1, M2, M3, M4, M5, M8, M9, M10 — all active and in scope.
  - **DEFERRED with written blocker (per VER-03):** M6, M7 — status `DEFERRED`, verdict `defer-with-blocker`, blocker text: "Not adjudicable from supplied files. The accessible consolidation map does not expose standalone M6 or M7 semantic categories (per ctl_pinn_resolution.md §M6 and M7). v1.4 records as explicit deferral; revisit when source material is available."
  - **MINOR / INFO:** Not enumerated in the seed; if any are referenced by a Phase 17–21 fix, the executing phase adds the row at that point with a "added in Phase NN" subsection note.

### Known contested findings (EVID-05 pre-flagged)

- **D-08:** Phase 16 pre-flags these four findings in the ledger's `Sources Disagree?` column as `YES — EVID-05 required` so the executing phase knows the adjudication must be done before any spec edit:
  - **B-02 (D formula)** — resolution doc keeps `D=(G*T^2)^(1/3)`; issue doc demands `D=(G*M_tot*T^2)^(1/3)=6.694`. Phase 19 adjudicates per PHYS-01.
  - **B-04 (input-vector orientation slots)** — resolution doc's Option B (shape invariants + direction cosines / velocity scalars c_1/c_2 — exact form locked during adjudication); issue doc's Option A (trig encoding for 3 angles). Phase 17 adjudicates per IO-02.
  - **B-09 (softening strategy)** — resolution doc's single matched `r_safe`; issue doc's dual-context `eps=1e-10` / `eps_soft=1e-5`. Phase 19 adjudicates per PHYS-03.
  - **M5 (`I_3` normalization map)** — resolution doc `I3_norm = 6*I3 - 1`; issue doc `I3_norm = 2*I3 - 1`. Phase 20 adjudicates per ARCH-03.

  Phase 16 does NOT pre-judge any verdict for these — it only reserves the EVID-05 slots so the receiving phase cannot accidentally skip the adjudication.

### VER-05 lifecycle and batch regression policy

- **D-09:** Status enum is exactly `PENDING → IN_PROGRESS → FIX_APPLIED → VERIFIED` (forward path) plus `DEFERRED` as an absorbing state with required written blocker. No other states. `VERIFIED` requires the corresponding AC-ID to have passed; "edit committed" is not a transition trigger.
- **D-10:** Each ledger row carries a `Dependents:` field listing other finding IDs that share a spec section, a contract, or a formula. Initial seed dependencies (Phase 16 fills these from the cross-issue interactions table in `ctl_pinn_resolution.md` §"Cross-Issue Interactions"):
  - `B-02 → B-09, M3` (D scaling drives epsilon-aware close-encounter thresholds and the M3 scaling step)
  - `B-03 → B-04, M1, M2` (dimension affects composition)
  - `B-04 → B-03, M1, M2` (composition affects dimension)
  - `B-05 → M3, B-11-folded-into-B-05` (COM transform order)
  - `B-09 → B-02, PHYS-04, PHYS-05` (softening choice cascades into energy regularizer + ALM)
  - `B-01 → B-10` (init formula must lock before omega0 schedule decision)
  - `M8 → ARCH-02` (LayerNorm attribution drives the affine default)
  Later phases may add dependents as new shared sections emerge — must annotate the addition in the per-finding subsection.
- **D-11:** Regression policy: after every batch of spec edits in Phases 17–21, the executing agent runs each `VERIFIED` finding's acceptance check IF that finding appears as a transitive dependent of any finding the batch edited. Failed re-runs revert the finding to `IN_PROGRESS` and block phase exit. A "batch" is the set of edits committed in a single GSD plan (`NN-NN-PLAN.md`).
- **D-12:** Phase-exit gate: no phase 17–21 exits with any in-scope finding still at `IN_PROGRESS` or `FIX_APPLIED`. Allowed exit states are `VERIFIED` or `DEFERRED`. Phase verifiers enforce this by re-reading the ledger at the verification step.

### Acceptance check naming policy

- **D-13:** Reserve names `AC-{REQ-ID}[-{NN}]` — examples: `AC-IO-01`, `AC-PHYS-02-COMP-AD`, `AC-FRAME-01`, `AC-ARCH-03`. The naming is reserved in Phase 16; pass criteria, runnable command, and data fixture are defined in Phase 21 per VER-01. Phases 17–20 cite the AC-ID their fix targets so Phase 21 has a complete index when it builds the executable suite.
- **D-14:** Every in-scope finding in the ledger has exactly one named AC-ID. Multiple findings may share an AC-ID when a single check covers them (e.g., `AC-IO-01` may cover B-03, M1, M2 if a dimension-width assertion is enough). Sharing is annotated in the per-finding subsection.

### VER-02 traceability artifact

- **D-15:** No separate `TRACEABILITY.md`. The ledger frontmatter's `last_verified_traceability` line plus a one-paragraph statement in the per-finding `## Notes` zone of the ledger ("30/30 v1.4 requirements mapped exactly once — see REQUIREMENTS.md §Traceability") is the artifact. REQUIREMENTS.md §Traceability remains the source of truth; duplicating the table is drift-prone.
- **D-16:** Phase 16 also re-verifies the existing table by counting rows and confirming each requirement appears exactly once and is mapped to a phase in `[16, 17, 18, 19, 20, 21]`. The verification produces a checkbox in the ledger frontmatter and a commit message scope `(16): verify VER-02 traceability`.

### "Neither source is authoritative" operationalization

- **D-17:** The evidence-packet template enforces side-by-side citation of BOTH source docs before any verdict. The template has no "primary source" field; the verdict enum (D-06 §6) is the only place a source preference is recorded, and even then the EVID-05 sections require the agent to show its work for contested findings.
- **D-18:** `master_consolidation_report.md` is treated as supporting evidence only — it MAY be cited in `evidence/{id}.md` §5 (first-principles physics check) when its argumentation helps, but it is not a substitute for the two primary sources in §2.

### Phase 16 deliverables (exhaustive)

- **D-19:** Phase 16 ships exactly these files:
  1. `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md` — schema + seeded inventory + dependency map + traceability statement.
  2. `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/evidence/README.md` — protocol overview: verdict enum, EVID-05 trigger conditions, VER-05 lifecycle, batch regression policy, AC-ID naming policy, "neither authoritative" rule.
  3. `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/evidence/_TEMPLATE.md` — the fixed-schema packet template per D-06.
  4. Doc edits to `.planning/ROADMAP.md`, `.planning/REQUIREMENTS.md`, `.planning/PROJECT.md` to reconcile the ledger path (D-01).
  5. The phase's own `16-PLAN.md`, `16-RESEARCH.md` (if research-phase is enabled), `16-VALIDATION.md`, `16-VERIFICATION.md`, `16-SUMMARY.md` — standard GSD artifacts, produced by downstream skills.

  Phase 16 does NOT ship: spec edits, code edits, adjudication records for any finding, executable acceptance-check scripts, lint tooling for the ledger.

### the agent's Discretion
- Exact column ordering in the ledger table (within the column set defined in D-02) and exact YAML key ordering in the frontmatter (within the keys defined in D-03) — pick whatever reads cleanest.
- Whether to use `<details>` collapse blocks for the per-finding subsections in `16-ISSUE-LEDGER.md` — fine to use if the file gets long.
- Subsection ordering within `evidence/_TEMPLATE.md` (within the 12 required sections defined in D-06) — pick a flow that prompts the agent to do the source-quote step before the verdict step.
- Wording of the deferral blocker text for M6/M7 — must contain the substantive reason; exact phrasing is flexible.

### Deferred Ideas (OUT OF SCOPE)
## Deferred Ideas

- **Ledger linter / CI check that validates verdict enum and status enum** — not in v1.4 requirements; would be nice but is out of scope. Capture for future tooling work after v1.4 ships.
- **Auto-generated traceability table from REQUIREMENTS.md** — would prevent manual drift but adds a build step. Defer until traceability drift is shown to be a real problem.
- **Cross-issue dependency graph visualization** — the table-based `Dependents:` field is enough for VER-05. A graphviz output is nice-to-have, not required.
- **Migration of `master_consolidation_report.md` into the supporting-evidence directory structure** — currently lives at the same level as the resolution doc; demoting it physically would match its demoted authoritative status. Out of Phase 16 scope (no spec/file moves except the ledger path reconciliation).
- **Acceptance check executable suite (Phase 21 territory)** — Phase 16 reserves names; Phase 21 writes the scripts.
- **Re-opening M6/M7 with new source material** — explicitly deferred per VER-03. If new material surfaces during v1.4, the executing phase adds an addendum to the M6/M7 ledger subsection but does NOT change the `DEFERRED` status without explicit milestone-level approval.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| EVID-01 | Record direct evidence from both Issue 01 sources, current specs, and relevant live code before edits. [VERIFIED: .planning/REQUIREMENTS.md:14] | Use the packet template with mandatory source/spec/code citation sections and seed ledger rows without verdicts. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:47-59] |
| EVID-02 | Assign every issue a fixed-enum verdict with recorded reasoning. [VERIFIED: .planning/REQUIREMENTS.md:15] | Enforce the verdict enum in both ledger and packet template; leave `-` only while `PENDING`. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:33-35] |
| EVID-03 | Document false positives as intentional non-changes with evidence-backed reasons. [VERIFIED: .planning/REQUIREMENTS.md:16] | Use the before/after spec note section for `accept-resolution` as no-change findings. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:57] |
| EVID-04 | Tie accepted issues to before/after spec-section notes, contracts, and verification steps. [VERIFIED: .planning/REQUIREMENTS.md:17] | Reserve AC-IDs now and defer runnable criteria to Phase 21 per VER-01. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:97-98] |
| EVID-05 | For source conflicts, require both-source reading, current-spec/live-code/physics verification, root-cause ambiguity, locked convention, and source correctness record before edits. [VERIFIED: .planning/REQUIREMENTS.md:18] | Pre-flag B-02, B-04, B-09, and M5 as `YES - EVID-05 required`; template must make root-cause/locked-convention/source-correctness sections non-skippable. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:52-56,72-78] |
| VER-02 | Map every v1.4 requirement to exactly one phase beginning at Phase 16. [VERIFIED: .planning/REQUIREMENTS.md:54] | Emit a ledger frontmatter statement and verify the REQUIREMENTS traceability table count rather than duplicating it. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:102-103] |
| VER-05 | Track every fix through `PENDING -> IN_PROGRESS -> FIX_APPLIED -> VERIFIED`; applied edits are not closure and regressions reopen findings. [VERIFIED: .planning/REQUIREMENTS.md:57] | Put status enum, dependents, transition log, batch regression policy, and phase-exit gate in the ledger/protocol. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:82-93] |
</phase_requirements>

## Summary

Phase 16 should be planned as a documentation-governance phase, not a physics adjudication or implementation phase. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:10-18] The plan should create the ledger, evidence directory README, and evidence packet template, then make only the locked path-reconciliation edits to planning docs. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:112-119]

The ledger seed must inventory findings without deciding them. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:63-78] The practical planning rule is: populate rows, statuses, AC-ID slots, source-disagreement flags, and dependency metadata, but leave verdicts as `-` except the explicitly deferred M6/M7 rows. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:33-36,63-78]

Traceability is already countable from REQUIREMENTS.md: the traceability table has 30 rows and no duplicate requirement IDs in the 2026-05-16 audit command. [VERIFIED: awk traceability audit run 2026-05-16 against .planning/REQUIREMENTS.md:86-119] The research found an additional stale ledger path in `.planning/STATE.md`; because the locked deliverables list only ROADMAP, REQUIREMENTS, and PROJECT for path reconciliation, the planner should treat STATE as an open workflow-state sync question rather than silently broadening Phase 16. [VERIFIED: rg path audit 2026-05-16; .planning/STATE.md:151; .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:27-29,112-119]

**Primary recommendation:** Plan Phase 16 as four document tasks: path reconciliation, ledger creation, evidence protocol/template creation, and traceability/status-regression validation. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:27-29,33-43,47-59,82-103]

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|--------------|----------------|-----------|
| Issue ledger state | GSD planning docs | Downstream phase verifiers | The ledger is a Markdown phase artifact consumed as the entry/exit checklist for Phases 17-21. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:181-183] |
| Evidence packet schema | GSD planning docs | Current specs and live code as cited evidence | Packet files live under the Phase 16 `evidence/` directory and cite, but do not modify, source/spec/code artifacts in Phase 16. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:41-59,119] |
| EVID-05 conflict protocol | GSD planning docs | Phases 17-20 execution | Phase 16 pre-flags contested findings and supplies mandatory sections; later phases perform adjudication. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:72-78] |
| VER-05 status lifecycle | GSD planning docs | Phase verification steps | The lifecycle and batch regression policy live in the ledger/protocol and are enforced by verifiers reading the ledger. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:82-93] |
| VER-02 traceability statement | REQUIREMENTS.md traceability table | Ledger frontmatter | REQUIREMENTS.md remains source of truth; the ledger records verification, not a duplicated table. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:102-103] |
| Path reconciliation | Planning docs | Phase 16 artifact path | D-01 locks the canonical phase slug path and authorizes narrow edits to ROADMAP, REQUIREMENTS, and PROJECT. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:27-29] |

## Project Constraints (from AGENTS.md)

| Directive | Planning Impact |
|-----------|-----------------|
| Source-of-truth files include `simulation_data/Documentation/README.md`, `pinn/data-processing-pipeline-full.py` *(AGENTS.md pre-2026-05-19; superseded by no-live-code directive)*, `pinn/basic_architecture.py` *(AGENTS.md pre-2026-05-19; superseded by no-live-code directive)*, and the three framework specs. [VERIFIED: AGENTS.md:38-45] | Evidence template examples should cite these exact paths where relevant. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:146-153] |
| PINN input-vector logic in `pinn/data-processing-pipeline-full.py` overrides comments in `pinn/basic_architecture.py` if they differ. *(AGENTS.md pre-2026-05-19; superseded by no-live-code directive.)* [VERIFIED: AGENTS.md:202] | EVID-05/B-04 and M5 packet instructions must prefer pipeline code for live-code input-vector evidence. *(Pre-2026-05-19; superseded by no-live-code directive. Neither file is v1.4 evidence.)* [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:151-153] |
| Brutus output completeness uses final timestamp `>= 9.5`, and `Result:` footers are metadata only. [VERIFIED: AGENTS.md:145-148] | Phase 16 should not build validation over Brutus footer assumptions; any future acceptance-check evidence should cite live parsed data rules explicitly. [VERIFIED: AGENTS.md:145-148] |
| Result footer paths can be OS-dependent and not authoritative mappings. [VERIFIED: AGENTS.md:274] | Evidence packets should avoid relying on footer filenames as canonical issue/data mapping evidence. [VERIFIED: AGENTS.md:274] |
| Hierarchical COM and total momentum are not exactly zero after perturbation. [VERIFIED: AGENTS.md:275] | B-05/FRAME evidence examples should include dataset README and sampling-spec anchors instead of assuming exact COM for hierarchical ICs. [VERIFIED: simulation_data/Documentation/README.md:333-335,718-724] |
| Project-defined skill directories `.codex/skills/` and `.agents/skills/` were absent in this workspace audit. [VERIFIED: `ls -ld .codex/skills .agents/skills` returned no entries on 2026-05-16] | No project-local skill rules need to be incorporated beyond AGENTS.md for Phase 16 planning. [VERIFIED: project-skills-discovery audit 2026-05-16] |

## Standard Stack

### Core

| Library / Tool | Version | Purpose | Why Standard |
|----------------|---------|---------|--------------|
| Markdown files | N/A | Human-reviewed ledger, protocol, and packet template artifacts. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:33-43,112-115] | Existing planning and issues docs are Markdown, and Phase 16 artifacts are locked as Markdown. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:176-179] |
| YAML frontmatter | N/A | Machine-readable ledger counts and traceability statement. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:36] | Context deliberately allows frontmatter for ledger structure because it carries counts and a traceability checkbox. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:174] |
| `gsd-sdk` | v1.42.2 | Phase metadata and workflow integration. [VERIFIED: `gsd-sdk --version` on 2026-05-16] | `init.phase-op 16` resolved the actual slug and canonical phase directory. [VERIFIED: `gsd-sdk query init.phase-op "16"` on 2026-05-16] |
| `rg` | 15.1.0 | Fast path, issue-ID, and stale-reference verification. [VERIFIED: `rg --version` on 2026-05-16] | Repo instructions prefer `rg` for search. [VERIFIED: user-provided AGENTS.md Tool Guidelines] |
| `awk` / shell | macOS shell tools | Count traceability rows and duplicates without adding tooling. [VERIFIED: traceability audit command run 2026-05-16] | Phase 16 explicitly defers ledger linter and auto-generated traceability tooling. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:202-203] |

### Supporting

| Library / Tool | Version | Purpose | When to Use |
|----------------|---------|---------|-------------|
| Git | 2.50.1 | Inspect dirty state and provide commit short SHAs for future transition logs. [VERIFIED: `git --version` and `git status --short` on 2026-05-16] | Later phases use commit short SHA in status logs. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:37,193] |
| Python 3 | 3.12.2 | Existing project validation style uses custom Python scripts. [VERIFIED: `python3 --version` and tests/test_phase12_validation.py:1-7] | Phase 16 does not need new Python scripts; use only if a future verifier wants a quick local doc check. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:119,202] |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Markdown ledger | JSON/YAML ledger | Rejected for Phase 16 because current planning docs and required deliverables are Markdown. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:112-115,176-179] |
| One packet file per finding | Embed packets inside ledger | Rejected because D-05 locks one file per finding and keeps the ledger lean. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:41-43] |
| Manual traceability statement | Auto-generated traceability table | Deferred because REQUIREMENTS.md remains source of truth and duplication is drift-prone. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:102-103,203] |
| Shell validation | New linter / CI check | Deferred because ledger lint tooling is explicitly out of Phase 16 scope. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:202] |

**Installation:**
```bash
# No package installation is required for Phase 16. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:119,185]
```

**Version verification:** No npm package versions are recommended for this phase. [VERIFIED: no installable JavaScript stack found in Phase 16 scope; .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:119,185]

## Architecture Patterns

### System Architecture Diagram

```text
GSD Phase 16 scope
  |
  v
Read CONTEXT locked decisions + requirements + roadmap
  |
  v
Create 16-ISSUE-LEDGER.md
  |-- seed one row per in-scope B/M finding
  |-- set status/verdict/dependents/AC-ID slots
  |-- mark B-02, B-04, B-09, M5 as EVID-05-required
  |-- mark M6/M7 as DEFERRED with blocker
  |
  v
Create evidence/README.md + evidence/_TEMPLATE.md
  |-- require two primary source citations
  |-- require current spec/code evidence where applicable
  |-- require EVID-05 root-cause/locked-convention/source-correctness sections
  |
  v
Reconcile stale ledger path in locked planning docs
  |
  v
Validate:
  traceability count == 30 and duplicates == 0
  ledger path references use canonical slug
  no spec/code/adjudication files changed
```

The diagram reflects the locked Phase 16 boundary and deliverables. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:10-18,112-119]

### Recommended Project Structure

```text
.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/
├── 16-CONTEXT.md        # existing locked phase decisions [VERIFIED]
├── 16-RESEARCH.md       # this research artifact [VERIFIED]
├── 16-ISSUE-LEDGER.md   # create in Phase 16 execution [VERIFIED]
└── evidence/
    ├── README.md        # protocol overview [VERIFIED]
    └── _TEMPLATE.md     # copy source for future packet files [VERIFIED]
```

This structure matches D-05 and D-19. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:41-43,112-115]

### Pattern 1: Ledger as Index, Not Evidence Body

**What:** Keep `16-ISSUE-LEDGER.md` as a status/dependency/AC-ID index, and place substantive evidence in `evidence/{finding-id}.md`. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:33-43]
**When to use:** Use this for every seeded finding, including findings that remain `PENDING`, because Phase 16 locks inventory before later adjudication. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:63-68]
**Example:**
```markdown
| ID | Title | Phase | Status | Verdict | Sources Disagree? | Evidence Packet | Acceptance Check | Spec Section | Dependents | Last Updated |
|----|-------|-------|--------|---------|-------------------|-----------------|------------------|--------------|------------|--------------|
| B-02 | Characteristic length D | 19 | PENDING | - | YES - EVID-05 required | evidence/B-02.md | AC-PHYS-01 | ctl_instruction.md scaling | B-09, M3 | 2026-05-16 |
```
The row shape is locked by D-02, and the B-02 EVID-05 flag is locked by D-08. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:33-35,72-78]

### Pattern 2: Template Gate for EVID-05

**What:** Make contested-only sections visible and mandatory in `_TEMPLATE.md` using strong headings plus HTML comments. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:47-59,195]
**When to use:** Use this for B-02, B-04, B-09, M5, and any later source conflict discovered during the walkthrough. [VERIFIED: .planning/REQUIREMENTS.md:18]
**Example:**
```markdown
## First-Principles Physics Check
<!-- REQUIRED for EVID-05. Name the law/dimensional argument and show the worked check. -->

## Root-Cause Framework Ambiguity
<!-- REQUIRED for EVID-05. Name the spec passage or missing contract that allowed disagreement. -->

## Locked Convention
<!-- REQUIRED for EVID-05. State the adopted convention in spec-edit-ready prose. -->

## Which Source Was Correct / Wrong
<!-- REQUIRED for EVID-05. Assign correctness per claim; do not mark either source authoritative. -->
```
These sections operationalize EVID-05 without adjudicating any specific finding during Phase 16. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:52-56,78,119]

### Pattern 3: Traceability Statement, Not Table Copy

**What:** Record the VER-02 result in ledger frontmatter and notes, but keep the traceability table only in REQUIREMENTS.md. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:102-103]
**When to use:** Use this for the Phase 16 ledger frontmatter and a short notes paragraph. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:36,102-103]
**Example:**
```yaml
last_verified_traceability: "30/30 v1.4 requirements mapped exactly once - verified 2026-05-16 against REQUIREMENTS.md Traceability"
traceability_verified: true
```
The current REQUIREMENTS.md traceability table contains 30 rows and no duplicate requirement IDs in the 2026-05-16 audit. [VERIFIED: awk traceability audit 2026-05-16; .planning/REQUIREMENTS.md:86-119]

### Anti-Patterns to Avoid

- **Adjudicating while seeding:** Do not put final verdicts or physics reasoning into Phase 16 rows except M6/M7 deferrals; later phases own adjudication. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:63-78,119]
- **Duplicating traceability:** Do not create `TRACEABILITY.md` or copy the 30-row table into the ledger. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:102-103]
- **Creating a second ledger path:** Do not create `.planning/milestones/v1.4-phases/16-evidence-framework/`; reconcile stale references to the actual slug path. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:27-29]
- **Building a linter:** Do not add executable enum/status validation tooling in Phase 16. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:202]
- **Editing specs or code:** Do not modify framework specs or `pinn/` code in Phase 16. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:18,119,185]

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Evidence storage | Custom database, JSON schema, or generated site | Markdown ledger plus one Markdown packet per finding | D-02/D-05/D-19 lock Markdown artifacts and one-packet-per-finding storage. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:33-43,112-115] |
| Enum enforcement | New linter or CI job | Table/template text plus phase verification checklist | Linter tooling is deferred out of Phase 16. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:202] |
| Traceability | Separate generated traceability artifact | Ledger verification statement referencing REQUIREMENTS.md | D-15 rejects a separate traceability file. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:102-103] |
| Conflict adjudication | Phase 16 mini-adjudications | EVID-05 template sections reserved for Phases 17-20 | Phase 16 reserves EVID-05 slots and does not pre-judge verdicts. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:72-78,119] |
| Acceptance checks | Runnable acceptance-check suite | AC-ID names only | Phase 21 defines and executes acceptance checks; Phase 16 reserves names. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:97-98,206] |

**Key insight:** Phase 16 reduces future risk by constraining evidence collection and status transitions, not by resolving physics findings. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:10-18,72-78,119]

## Runtime State Inventory

| Category | Items Found | Action Required |
|----------|-------------|-----------------|
| Stored data | None found for the stale ledger path or `16-ISSUE-LEDGER` in databases/datastores; repo scan found Markdown references only. [VERIFIED: `rg -n "16-evidence-framework/16-ISSUE-LEDGER|16-evidence-framework" --hidden -g '!reference-code/**' -g '!.git/**'` on 2026-05-16] | No data migration. [VERIFIED: same scan] |
| Live service config | None found in environment variables, launchd registrations, or running service command lines beyond editor processes for the repo. [VERIFIED: `env`, `launchctl list`, and `ps aux` audits on 2026-05-16] | No external service patch. [VERIFIED: same audits] |
| OS-registered state | None found for the stale path in launchd output. [VERIFIED: `launchctl list | rg "16-evidence-framework|ISSUE-LEDGER|3_body_problem|gsd"` on 2026-05-16] | No re-registration. [VERIFIED: same audit] |
| Secrets/env vars | No `.env*`, SOPS, or secret files with the stale path were found; `.github/workflows/*` exists but path scan found no stale ledger reference there. [VERIFIED: `rg --files --hidden -g '.env*' -g '*secret*' -g '*secrets*' -g '*.sops.*' -g '.github/workflows/**'` and stale-path `rg` audit on 2026-05-16] | No secret/env rename. [VERIFIED: same audits] |
| Build artifacts | No files named `*16-evidence-framework*` or `*ISSUE-LEDGER*` exist beyond the phase directory itself before Phase 16 execution. [VERIFIED: `find . -maxdepth 4 \( -name '*16-evidence-framework*' -o -name '*ISSUE-LEDGER*' \)` on 2026-05-16] | No artifact cleanup. [VERIFIED: same audit] |

**Nothing found in category:** Runtime categories are clean; only repository Markdown references require reconciliation. [VERIFIED: audits listed above]

## Common Pitfalls

### Pitfall 1: Ledger Seed Becomes Adjudication
**What goes wrong:** The planner asks execution to fill verdicts, physics checks, or spec changes while creating seed rows. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:63-78,119]
**Why it happens:** The ledger has verdict and evidence-packet columns even though later phases own the actual adjudications. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:33-35,72-78]
**How to avoid:** Seed `PENDING` rows with `Verdict = -` except M6/M7 deferrals, and create only `_TEMPLATE.md` plus protocol docs. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:33-35,63-78,112-119]
**Warning signs:** Evidence packet files other than `_TEMPLATE.md` are created in Phase 16, or a contested finding receives a final verdict before Phase 17. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:43,72-78,119]

### Pitfall 2: EVID-05 Sections Are Optional in Practice
**What goes wrong:** Future packets cite both sources but skip root-cause ambiguity, locked convention, or source-correctness sections. [VERIFIED: .planning/REQUIREMENTS.md:18]
**Why it happens:** Those sections are conditional on a conflict and are easy to omit unless the template makes them prominent. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:52-56,195]
**How to avoid:** Use explicit headings and comments marking each EVID-05 section as required when `Sources Disagree? = YES - EVID-05 required`. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:52-56,72-78,195]
**Warning signs:** A packet records only `accept-resolution` or `accept-issue-doc` for B-02/B-04/B-09/M5 without a worked first-principles check. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:52-56,72-78]

### Pitfall 3: Stale Path Reconciliation Broadens Silently
**What goes wrong:** Execution touches many planning files or creates a second phase directory to satisfy old path mentions. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:27-29,112-119]
**Why it happens:** Stale path references exist in ROADMAP, REQUIREMENTS, PROJECT, and also STATE; D-01 authorizes only ROADMAP/REQUIREMENTS/PROJECT edits. [VERIFIED: rg path audit 2026-05-16; .planning/STATE.md:151; .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:27-29,112-119]
**How to avoid:** Plan the three D-01 doc edits exactly, and handle STATE only as an open workflow-state sync decision. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:27-29,112-119]
**Warning signs:** `.planning/milestones/v1.4-phases/16-evidence-framework/` is created or unrelated roadmap prose changes appear. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:27-29]

### Pitfall 4: Dependency Map Source Is Cited Too Literally
**What goes wrong:** The plan tells execution to copy a `Cross-Issue Interactions` heading from `ctl_pinn_resolution.md`, but that exact heading was not found there. [VERIFIED: `rg -n "Cross-Issue Interactions" ctl_pinn_resolution.md` returned no match on 2026-05-16]
**Why it happens:** D-10 names `ctl_pinn_resolution.md` as the cross-issue table source, while the exact `## Cross-Issue Interactions` heading exists in `pinn_instruction/issues/01-architecture-and-physics-foundations.md`. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:83-90; pinn_instruction/issues/01-architecture-and-physics-foundations.md:316-327]
**How to avoid:** Seed dependencies from D-10 as locked decisions, and cite the issue doc cross-issue table plus the resolution doc audit matrix/implementation roadmap as supporting anchors. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:83-90; pinn_instruction/issues/01-architecture-and-physics-foundations.md:316-327; pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md:200-219,962-990]
**Warning signs:** A task blocks because it cannot find `ctl_pinn_resolution.md §Cross-Issue Interactions`. [VERIFIED: same source audit]

### Pitfall 5: VER-02 Duplicates the Table
**What goes wrong:** Phase 16 creates a second traceability table that can drift from REQUIREMENTS.md. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:102-103]
**Why it happens:** The success criterion asks reviewers to see traceability, but D-15 locks the artifact as a statement, not a table copy. [VERIFIED: .planning/ROADMAP.md:119; .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:102-103]
**How to avoid:** Use a count/duplicate audit command and store the result in ledger frontmatter/notes. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:102-103]
**Warning signs:** A new `TRACEABILITY.md` appears or the ledger contains all 30 traceability rows. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:102-103]

## Code Examples

Verified patterns from local sources:

### Traceability Count Check
```bash
awk 'BEGIN{in_trace=0} /^## Traceability/{in_trace=1; next} in_trace && /^---/{in_trace=0} in_trace && /^\| [A-Z]+-[0-9][0-9]/{gsub(/^\| /,""); gsub(/ \|.*/,""); print}' .planning/REQUIREMENTS.md | sort
```
This command extracts the 30 v1.4 requirement IDs from the REQUIREMENTS.md traceability table. [VERIFIED: command run 2026-05-16; .planning/REQUIREMENTS.md:86-119]

### Stale Ledger Path Check
```bash
rg -n "16-evidence-framework/16-ISSUE-LEDGER|16-evidence-framework" --hidden -g '!reference-code/**' -g '!.git/**'
```
This command found stale ledger-path references in ROADMAP, REQUIREMENTS, PROJECT, STATE, and Phase 16 discussion/context files. [VERIFIED: rg audit 2026-05-16]

### Ledger Row Skeleton
```markdown
| ID | Title | Phase | Status | Verdict | Sources Disagree? | Evidence Packet | Acceptance Check | Spec Section | Dependents | Last Updated |
|----|-------|-------|--------|---------|-------------------|-----------------|------------------|--------------|------------|--------------|
| M6 | Deferred finding placeholder | 21 | DEFERRED | defer-with-blocker | NO | - | AC-VER-03 | - | - | 2026-05-16 |
```
The skeleton reflects D-02 status/verdict columns and D-07 M6/M7 deferral treatment. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:33-36,63-68]

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Treat `ctl_pinn_resolution.md` as a candidate fix list with risk of being used authoritatively. [VERIFIED: .planning/PROJECT.md:153] | Treat neither `ctl_pinn_resolution.md` nor `01-architecture-and-physics-foundations.md` as authoritative; require critical evidence before edits. [VERIFIED: .planning/REQUIREMENTS.md:10-18] | v1.4 initialization on 2026-05-15. [VERIFIED: .planning/REQUIREMENTS.md:129; .planning/STATE.md:114-115] | Phase 16 must create evidence packets and EVID-05 protocol before spec edits begin. [VERIFIED: .planning/ROADMAP.md:90-98] |
| Close issues when a fix is applied. [VERIFIED: .planning/ROADMAP.md:94-96] | Close only when acceptance check passes; regressions revert to `IN_PROGRESS`. [VERIFIED: .planning/REQUIREMENTS.md:57] | v1.4 initialization on 2026-05-15. [VERIFIED: .planning/STATE.md:115] | Ledger must distinguish `FIX_APPLIED` from `VERIFIED`. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:82-93] |
| Recommended stale ledger path `.planning/milestones/v1.4-phases/16-evidence-framework/16-ISSUE-LEDGER.md`. [VERIFIED: .planning/REQUIREMENTS.md:57; .planning/ROADMAP.md:94,118; .planning/PROJECT.md:81] | Canonical path `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md`. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:27] | Phase 16 context gathered 2026-05-15. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:3-5] | Planner must include narrow path reconciliation. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:27-29] |

**Deprecated/outdated:**
- Creating `.planning/milestones/v1.4-phases/16-evidence-framework/` is outdated because D-01 locks the actual phase slug path. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:27-29]
- Duplicating REQUIREMENTS.md traceability is outdated because D-15 locks REQUIREMENTS.md as source of truth. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:102-103]
- Treating `master_consolidation_report.md` as co-equal primary evidence is outdated because D-18 demotes it to supporting evidence. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:107-108]

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | STATE.md path reconciliation should not be included in Phase 16 deliverables without explicit workflow-state sync approval because D-19 exhaustively lists ROADMAP/REQUIREMENTS/PROJECT doc edits only. [ASSUMED] | Summary, Pitfall 3, Open Questions | Leaving STATE stale may confuse a later progress report; editing it may exceed locked deliverables. |

## Open Questions (RESOLVED)

1. **RESOLVED — `.planning/STATE.md` stays outside Phase 16 path-reconciliation tasks and is left to workflow state sync.**
   - What we know: The stale path appears in STATE.md line 151, and D-01 explicitly lists ROADMAP.md, REQUIREMENTS.md, and PROJECT.md for Phase 16 path edits. [VERIFIED: rg path audit 2026-05-16; .planning/STATE.md:151; .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:27-29]
   - What's unclear: D-19 calls Phase 16 deliverables exhaustive and does not list STATE.md, but STATE.md is a planning doc visible to workflow users. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:112-119]
   - Resolution: Keep implementation tasks to the three locked doc edits and require `git diff -- .planning/STATE.md --exit-code` during path reconciliation. If STATE.md needs to be synchronized later, use a GSD state handler rather than direct edits. [RESOLVED: Phase 16 plan scope]

2. **RESOLVED — use D-10 locked dependency entries plus explicit source-caveat wording.**
   - What we know: The exact `## Cross-Issue Interactions` heading is in the issue doc, while `ctl_pinn_resolution.md` has a verified audit matrix and dependency-ordered roadmap but not that exact heading. [VERIFIED: pinn_instruction/issues/01-architecture-and-physics-foundations.md:316-327; pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md:200-219,962-990]
   - What's unclear: Whether the context intended the issue doc table or a renamed/implicit section in the resolution doc. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:83-90,194]
   - Resolution: Use the D-10 dependency entries as locked content. Cite `pinn_instruction/issues/01-architecture-and-physics-foundations.md` for the exact `Cross-Issue Interactions` table and cite `ctl_pinn_resolution.md` audit matrix / dependency-ordered roadmap as supporting evidence. [RESOLVED: source audit]

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|-------------|-----------|---------|----------|
| `gsd-sdk` | Phase metadata and optional commit workflow | yes | v1.42.2 [VERIFIED: `gsd-sdk --version` on 2026-05-16] | Manual path from CONTEXT if unavailable. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:27] |
| `rg` | Stale-reference and source-anchor scans | yes | 15.1.0 [VERIFIED: `rg --version` on 2026-05-16] | POSIX `grep` if unavailable. [ASSUMED] |
| `git` | Dirty-state inspection and future commit SHA log entries | yes | 2.50.1 [VERIFIED: `git --version` on 2026-05-16] | Manual timestamp-only transition logs if no commit exists. [ASSUMED] |
| `python3` | Existing custom validation style and optional doc checks | yes | 3.12.2 [VERIFIED: `python3 --version` on 2026-05-16] | Shell-only checks are sufficient for Phase 16. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:119,202] |

**Missing dependencies with no fallback:**
- None found for Phase 16 documentation work. [VERIFIED: environment audit 2026-05-16]

**Missing dependencies with fallback:**
- No root project package manager or test framework config was found; Phase 16 can use shell validation instead of adding tooling. [VERIFIED: root dependency/config scan 2026-05-16]

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | Custom shell/doc checks for Phase 16; existing `tests/test_phase12_validation.py` is a standalone Python script for Phase 12, not a reusable Phase 16 framework. [VERIFIED: tests/test_phase12_validation.py:1-7] |
| Config file | None at project root for pytest/tox/ruff; reference-code subprojects have their own configs and are out of Phase 16 scope. [VERIFIED: root dependency/config scan 2026-05-16] |
| Quick run command | `rg -n "16-evidence-framework/16-ISSUE-LEDGER|16-evidence-framework" --hidden -g '!reference-code/**' -g '!.git/**'` [VERIFIED: command run 2026-05-16] |
| Full suite command | Phase 16-specific validation should combine path scan, traceability count/duplicate check, file-existence checks for ledger/template/README, and no spec/code diff check. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:112-119] |

### Phase Requirements -> Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|--------------|
| EVID-01 | Evidence packet template requires both primary sources, current specs, and conditional code evidence. [VERIFIED: .planning/REQUIREMENTS.md:14] | doc-structure | `rg -n "ctl_pinn_resolution.md|01-architecture-and-physics-foundations.md|Spec evidence|Code evidence" .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/evidence/_TEMPLATE.md` [VERIFIED: planned command] | no - Wave 0 creates `_TEMPLATE.md`. [VERIFIED: current phase dir listing 2026-05-16] |
| EVID-02 | Ledger/template use the fixed verdict enum. [VERIFIED: .planning/REQUIREMENTS.md:15] | doc-structure | `rg -n "accept-resolution|accept-issue-doc|accept-third-position|reject-both-as-unsupported|defer-with-blocker" .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/evidence/_TEMPLATE.md` [VERIFIED: planned command] | no - Wave 0 creates ledger/template. [VERIFIED: current phase dir listing 2026-05-16] |
| EVID-03 | Template supports intentional non-change false-positive records. [VERIFIED: .planning/REQUIREMENTS.md:16] | doc-structure | `rg -n "False Positive|intentional non-change|accept-resolution.*no-change|current convention remains valid" .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/evidence/_TEMPLATE.md` [VERIFIED: planned command] | no - Wave 0 creates template. [VERIFIED: current phase dir listing 2026-05-16] |
| EVID-04 | Template ties accepted issues to before/after spec note and AC-ID. [VERIFIED: .planning/REQUIREMENTS.md:17] | doc-structure | `rg -n "Before / After Spec Note|Named Acceptance Check|AC-" .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/evidence/_TEMPLATE.md` [VERIFIED: planned command] | no - Wave 0 creates template. [VERIFIED: current phase dir listing 2026-05-16] |
| EVID-05 | Template and ledger force contested-finding adjudication sections and flags. [VERIFIED: .planning/REQUIREMENTS.md:18] | doc-structure | `rg -n "First-Principles Physics Check|Root-Cause Framework Ambiguity|Locked Convention|Which Source Was Correct|YES - EVID-05 required|B-02|B-04|B-09|M5" .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/evidence/_TEMPLATE.md` [VERIFIED: planned command] | no - Wave 0 creates ledger/template. [VERIFIED: current phase dir listing 2026-05-16] |
| VER-02 | Requirements traceability has 30 rows and no duplicates. [VERIFIED: .planning/REQUIREMENTS.md:86-119] | shell audit | `awk 'BEGIN{in_trace=0} /^## Traceability/{in_trace=1; next} in_trace && /^---/{in_trace=0} in_trace && /^\\| [A-Z]+-[0-9][0-9]/{gsub(/^\\| /,""); gsub(/ \\|.*/,""); print}' .planning/REQUIREMENTS.md | sort | uniq -d` and row count command. [VERIFIED: command run 2026-05-16] | yes - REQUIREMENTS.md exists. [VERIFIED: file read 2026-05-16] |
| VER-05 | Ledger contains status enum, transition log, dependents, regression policy, and phase-exit rule. [VERIFIED: .planning/REQUIREMENTS.md:57] | doc-structure | `rg -n "PENDING|IN_PROGRESS|FIX_APPLIED|VERIFIED|DEFERRED|Dependents|regression|phase-exit|fix applied" .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/evidence/README.md` [VERIFIED: planned command] | no - Wave 0 creates ledger/README. [VERIFIED: current phase dir listing 2026-05-16] |

### Sampling Rate

- **Per task commit:** Run path scan plus targeted `rg` check for the artifact touched by the task. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:112-119]
- **Per wave merge:** Run all Phase 16 doc-structure checks plus traceability count/duplicate check. [VERIFIED: .planning/REQUIREMENTS.md:54,57]
- **Phase gate:** Confirm no framework specs or `pinn/` code changed, all Phase 16 files exist, and ledger path references are reconciled per D-01. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:18,27-29,112-119]

### Wave 0 Gaps

- [ ] `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md` - covers EVID-02, VER-02, VER-05. [VERIFIED: current phase dir listing 2026-05-16]
- [ ] `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/evidence/README.md` - covers EVID-05 and VER-05 protocol. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:112-115]
- [ ] `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/evidence/_TEMPLATE.md` - covers EVID-01 through EVID-05. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:47-59,112-115]
- [ ] Framework install: none required. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:119,185]

## Security Domain

Security enforcement is enabled because `.planning/config.json` does not set `security_enforcement` to `false`. [VERIFIED: .planning/config.json read 2026-05-16] OWASP ASVS is a basis for testing web application technical security controls and secure-development requirements, and the latest stable version listed by OWASP is 5.0.0. [CITED: https://owasp.org/www-project-application-security-verification-standard/ lines 32-63,368-375]

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|------------------|
| V2 Authentication | no | Phase 16 creates local docs and no authentication surface. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:112-119] |
| V3 Session Management | no | Phase 16 has no session state or web runtime. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:119,185] |
| V4 Access Control | no | Phase 16 does not introduce an application authorization boundary. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:119,185] |
| V5 Validation, Sanitization and Encoding | yes | Validate human-edited enum/status/path fields with fixed Markdown schema and phase checks. [CITED: https://devguide.owasp.org/en/03-requirements/05-asvs/ lines 263-269] [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:33-59,82-93] |
| V6 Stored Cryptography | no | Phase 16 does not store secrets or add cryptography. [VERIFIED: runtime state inventory audits 2026-05-16] |

### Known Threat Patterns for Phase 16 Documentation Workflow

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Evidence omission in a packet | Tampering | Mandatory packet sections and phase-exit `rg` checks for required headings. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:47-59] |
| False closure by status jump | Repudiation | Transition log plus `FIX_APPLIED` not closure rule. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:37,82-93] |
| Path confusion between stale and canonical ledger path | Tampering | D-01 path reconciliation and no second directory. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:27-29] |
| Source-authority spoofing | Tampering | Template requires side-by-side citations and has no primary-source field. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:107-108] |

## Sources

### Primary (HIGH confidence)

- `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md` - locked Phase 16 decisions, boundaries, deliverables, and discretion. [VERIFIED: file read 2026-05-16]
- `.planning/REQUIREMENTS.md` - v1.4 requirements and traceability table. [VERIFIED: file read and awk audit 2026-05-16]
- `.planning/ROADMAP.md` - Phase 16 success criteria and v1.4 verification protocol. [VERIFIED: file read 2026-05-16]
- `.planning/PROJECT.md` - active v1.4 target features and stale path reference. [VERIFIED: file read 2026-05-16]
- `.planning/STATE.md` - current milestone state and additional stale path reference. [VERIFIED: file read and rg audit 2026-05-16]
- `AGENTS.md` - project constraints and source-of-truth directives. [VERIFIED: file read 2026-05-16]
- `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md` - resolution-doc issue matrix and implementation roadmap anchors. [VERIFIED: file scans 2026-05-16]
- `pinn_instruction/issues/01-architecture-and-physics-foundations.md` - issue-doc finding inventory and cross-issue interaction table. [VERIFIED: file scans 2026-05-16]

### Secondary (MEDIUM confidence)

- OWASP ASVS official project page - ASVS purpose, latest stable version, and requirement-reference guidance. [CITED: https://owasp.org/www-project-application-security-verification-standard/]
- OWASP Developer Guide ASVS page - ASVS category list and levels. [CITED: https://devguide.owasp.org/en/03-requirements/05-asvs/]
- `pinn_instruction/issues/README.md` and `pinn_instruction/issues/MIGRATION.md` - prior issues consolidation pattern and provenance style. [VERIFIED: files read 2026-05-16]
- `.planning/codebase/CONVENTIONS.md` - local conventions and lack of root linting config. [VERIFIED: file read 2026-05-16]

### Tertiary (LOW confidence)

- None used as authoritative research input. [VERIFIED: source review 2026-05-16]

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - Phase 16 uses local Markdown/GSD artifacts and verified local CLI tools; no package ecosystem choice is needed. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:112-119,185]
- Architecture: HIGH - Locked decisions define artifact layout, status lifecycle, and protocol ownership. [VERIFIED: .planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md:33-59,82-119]
- Pitfalls: MEDIUM - Most pitfalls are directly verified; STATE.md treatment remains an open workflow-scope question. [VERIFIED: rg path audit 2026-05-16] [ASSUMED: STATE.md handling recommendation]

**Research date:** 2026-05-16 [VERIFIED: environment current date]
**Valid until:** 2026-06-15 for local planning-doc facts; re-run path and traceability audits if planning docs change before execution. [ASSUMED]
