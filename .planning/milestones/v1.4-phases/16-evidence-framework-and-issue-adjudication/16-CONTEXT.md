# Phase 16: Evidence Framework and Issue Adjudication - Context

**Gathered:** 2026-05-15
**Status:** Ready for planning
**Mode:** `--all --auto` (all gray areas auto-selected; recommended option chosen per gray area in a single pass)

<domain>
## Phase Boundary

Phase 16 delivers the **evidence framework** that every Issue 01 fix in Phases 17–21 must use. It does NOT adjudicate or fix any framework-spec content. Specifically it produces:

1. The Issue Ledger schema and the live ledger file with one row per in-scope finding, status, verdict slot, dependency map, and named acceptance check.
2. The Evidence Packet template enforcing 4-source line-range citations, the fixed verdict enum from EVID-02, and the EVID-05 conflict-adjudication sections.
3. The protocol documents that operationalize EVID-05 (when adjudication triggers, what it records, where it lives) and VER-05 (status transitions, batch regression-detection, phase-exit gates).
4. The traceability verification statement confirming 30/30 v1.4 requirements are mapped exactly once (REQUIREMENTS.md §Traceability is the source of truth — not duplicated here).
5. Path reconciliation for the ledger directory.

Phase 16 produces **no spec edits, no code edits, and no adjudications**. Those start in Phase 17.

</domain>

<decisions>
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
  4. **FUT-01 Hand-off Note** (formerly "Code evidence"; renamed 2026-05-19 per user directive — live code is NOT v1.4 evidence) — if the finding's new framework-spec contract diverges from v1.3-era code and FUT-01 will need to rewrite something, note the relevant `pinn/` paths with line ranges so `NN-CODE-DIVERGENCE.md` (or the eventual `pinn/STATUS.md`) can index them. Forward-pointing reference only; NOT a basis for the v1.4 verdict. Use `Not FUT-01-applicable` when this finding creates no code-rewrite gap (e.g., process-artifact decisions like AC naming).
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

### Claude's Discretion

- Exact column ordering in the ledger table (within the column set defined in D-02) and exact YAML key ordering in the frontmatter (within the keys defined in D-03) — pick whatever reads cleanest.
- Whether to use `<details>` collapse blocks for the per-finding subsections in `16-ISSUE-LEDGER.md` — fine to use if the file gets long.
- Subsection ordering within `evidence/_TEMPLATE.md` (within the 12 required sections defined in D-06) — pick a flow that prompts the agent to do the source-quote step before the verdict step.
- Wording of the deferral blocker text for M6/M7 — must contain the substantive reason; exact phrasing is flexible.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Primary sources (neither is authoritative — see D-17)
- `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md` — Most recent candidate adjudication of Issue 01. Read fully; verify every claim against the spec and code.
- `pinn_instruction/issues/01-architecture-and-physics-foundations.md` — Thematic consolidation of original audit findings. Read fully; verify every claim against the spec and code.

### Supporting evidence (cite when helpful, not as a verdict source)
- `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/master_consolidation_report.md` — Earlier multi-AI consolidation consumed by the resolution doc. Read for traceability and to verify the resolution doc's claims about prior consensus, not as a verdict source.
- `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/chatgpt_research_report.md` — Consult only for findings the consolidation map records as ambiguous (M6, M7).
- `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/claude_research_report.md` — Same usage rule as above.
- `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/claude_research_report_2.md` — Same usage rule as above.
- `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/gemini_research_report.md` — Same usage rule as above.

### Current framework specs (the thing being changed by Phases 17–21)
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` — CTL methodology spec. Phases 17–19 edit sections governing input vector, scaling, COM, softening, constraint counting.
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` — PINN architecture spec. Phases 17, 19, 20 edit sections governing input width, COM projection head, AD contract, energy regularizer, LayerNorm attribution, omega0 schedule.
- `pinn_instruction/markdown_conversion/framework-specs/sampling_method.md` — Sampling spec. Phase 18 edits the narrow FRAME-03 section per SCOPE-02 only.

### v1.3-era live code (NOT v1.4 evidence; FUT-01 hand-off reference only, per directive 2026-05-19)
- `pinn/basic_architecture.py` — v1.3-era SQR-SkipResNet-SIREN model. **NOT** authoritative or evidence during v1.4. Referenced only in forward-pointing FUT-01 hand-off documents (`NN-CODE-DIVERGENCE.md`).
- `pinn/data-processing-pipeline-full.py` — v1.3-era data pipeline. Same — NOT authoritative or evidence; FUT-01 hand-off reference only.
- FUT-01 will rebuild both files from the v1.4 framework specs after v1.4 ships.

### Project planning context (read once at phase start)
- `.planning/PROJECT.md` — Project overview, v1.4 milestone goal, key decisions including "Resolution doc is NOT authoritative in v1.4" and the iterative re-verification protocol.
- `.planning/REQUIREMENTS.md` — All 30 v1.4 requirements (EVID-01..05, IO-01..04, FRAME-01..04, PHYS-01..06, ARCH-01..05, VER-01..06). §Traceability is the source of truth for VER-02 verification.
- `.planning/ROADMAP.md` §"v1.4 Resolving 01 Architecture and Physics Foundations" — Phase definitions, dependencies, success criteria, verification protocol.
- `.planning/STATE.md` — Current milestone state, post-v1.3 SCS gate correction shipped 2026-05-15.
- `CLAUDE.md` — Source-of-truth file paths for data formats, pipeline stages, PINN architecture specifics. Pinned constraint: PINN input-vector logic in `pinn/data-processing-pipeline-full.py` overrides comments in `pinn/basic_architecture.py`. *(Pre-2026-05-19; superseded by no-live-code directive. Both files are v1.3-era artifact, not v1.4 evidence.)*

### Auxiliary context (cite when relevant)
- `simulation_data/Documentation/README.md` — Dataset spec including hierarchical COM offset (relevant to FRAME-03 and B-05).
- `pinn_instruction/issues/MIGRATION.md` and `pinn_instruction/issues/README.md` — Document how the 7 original issue files were consolidated into the three thematic docs; useful when tracing where a finding ID first appeared.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `.planning/phases/09-issues-directory-consolidation/` — Phase 9 already established a pattern for shipping consolidated documentation artifacts (MIGRATION.md + README.md + thematic .md files). Phase 16 can mirror this for the `evidence/` directory: a README.md inside `evidence/` explaining protocol, plus a `_TEMPLATE.md` (analogous to MIGRATION.md as a structure document).
- `.planning/codebase/CONVENTIONS.md` — Commit message conventions are Conventional Commits with phase-numbered scope. Phase 16 commits follow `docs(16): <description>` or `docs(16-NN): <description>` for sub-plans. Use imperative mood, lowercase, no trailing period.
- Existing planning markdown convention — frontmatter is uncommon in this repo's planning docs but allowed where structure matters (see `.planning/STATE.md`). The ledger's YAML frontmatter (D-03) is a deliberate exception because it carries machine-readable counts and a traceability checkbox.

### Established Patterns
- **Source of truth + verification, not duplication** — REQUIREMENTS.md §Traceability is the source for VER-02; PROJECT.md "Validated" section moves items post-phase. Phase 16 follows this by emitting a verification statement, not a copy of the table.
- **Phase artifact naming** — `{padded_phase}-{ARTIFACT}.md` in the phase directory; `evidence/{id}.md` follows finding-ID naming (the project's research/issues conventions use the same `B-NN`/`M-NN` IDs).
- **Markdown over YAML/JSON for human-edited records** — every existing planning doc is markdown; ledger and packets follow.

### Integration Points
- **Downstream phases (17–21) consume the ledger** as their entry/exit checklist. Phase 16 must produce a ledger that those phases can edit in-place without restructuring.
- **VER-04 in Phase 21** consumes the AC-ID name index from the ledger to know what disposable validation probes or commands to run. Phase 16 must reserve names that Phase 21 can execute without turning the probes into production framework code.
- **`gsd-discuss-phase` → `gsd-plan-phase` → `gsd-execute-phase` chain** — `--auto` triggers auto-advance after this context is committed.
- **No code path or build system is touched by Phase 16.** No Python imports change; no Makefile change; no env vars.

</code_context>

<specifics>
## Specific Ideas

- **The four pre-flagged contested findings (B-02, B-04, B-09, M5)** must reach Phases 17–20 with their `Sources Disagree? = YES — EVID-05 required` flag set, so the executing agent cannot skip adjudication. This is the single most important thing Phase 16 ships — it is the operational expression of the v1.4 milestone's central rule that neither source is authoritative.
- **Status transition log inside each per-finding subsection** uses one-line entries: `2026-MM-DD <SHA> PENDING → IN_PROGRESS (Phase 17 P01)`. Cheap to append, easy to grep across the file for an audit history.
- **Dependency map seeded from `ctl_pinn_resolution.md` §"Cross-Issue Interactions"** — that table already exists and lists exactly the kind of "if X changes, re-check Y" relationships that VER-05 regression detection needs. Phase 16 transcribes it into the ledger's `Dependents:` fields rather than reinventing.
- **The `evidence/_TEMPLATE.md` should be copy-pasted to start a new packet** — sections should be labeled with HTML comments (`<!-- REQUIRED for EVID-05; delete if not contested -->`) to remind the agent what to fill vs. skip.

</specifics>

<deferred>
## Deferred Ideas

- **Ledger linter / CI check that validates verdict enum and status enum** — not in v1.4 requirements; would be nice but is out of scope. Capture for future tooling work after v1.4 ships.
- **Auto-generated traceability table from REQUIREMENTS.md** — would prevent manual drift but adds a build step. Defer until traceability drift is shown to be a real problem.
- **Cross-issue dependency graph visualization** — the table-based `Dependents:` field is enough for VER-05. A graphviz output is nice-to-have, not required.
- **Migration of `master_consolidation_report.md` into the supporting-evidence directory structure** — currently lives at the same level as the resolution doc; demoting it physically would match its demoted authoritative status. Out of Phase 16 scope (no spec/file moves except the ledger path reconciliation).
- **Acceptance check executable suite (Phase 21 territory)** — Phase 16 reserves names; Phase 21 writes or records disposable probes only, with reusable packaging deferred until after v1.4.
- **Re-opening M6/M7 with new source material** — explicitly deferred per VER-03. If new material surfaces during v1.4, the executing phase adds an addendum to the M6/M7 ledger subsection but does NOT change the `DEFERRED` status without explicit milestone-level approval.

</deferred>

---

*Phase: 16-Evidence Framework and Issue Adjudication*
*Context gathered: 2026-05-15*
*Mode: --all --auto (single-pass, recommended option per gray area)*

---

## Amendment — 2026-05-18 (correction-of-record; no status change)

**Trigger:** Phase 17 discussion-phase research (`gsd-discuss-phase 17`) surfaced a mischaracterization in D-08's description of the B-04 EVID-05 conflict. Phase 16's verdicts and status assignments are unaffected; only the framing of *what the conflict is* is corrected here, before Phase 17 inherits the ledger.

**Mischaracterization in original D-08:**
> *B-04 (input-vector orientation slots) — resolution doc's Option B (shape invariants + direction cosines / velocity scalars c_1/c_2 — exact form locked during adjudication); issue doc's Option A (trig encoding for 3 angles).*

This sentence assigns "Option B = shape invariants + direction cosines / velocity scalars c_1/c_2" to the resolution doc. A full read of `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md` shows the resolution doc does **not** propose Option B. It rejects the invariant-only IC vector outright:

- `ctl_pinn_resolution.md:71–72` — "The original invariant-only 13D IC vector is rejected as the final model input. It may be kept only as metadata or as a later ablation."
- `ctl_pinn_resolution.md:459–465` — "The invariant-only vector `[masses, E, L_norm, Q, s_min, I_norm, I1, I2, I3, c1, c2]` is useful as metadata but not a mathematically safe final conditioning state."
- `ctl_pinn_resolution.md:517–524` — boxed final IC₁₃:
  `[m₁, m₂, m₃, ρ_x, λ_x, λ_y, ρ̇_x, ρ̇_y, ρ̇_z, λ̇_x, λ̇_y, λ̇_z, E]`
  (reconstructive Jacobi state — no shape invariants, no direction cosines, no orientation angles).

"Shape invariants + direction cosines" is actually the **issue doc's** Option B (`pinn_instruction/issues/01-architecture-and-physics-foundations.md:499–579`).

**Corrected framing of the B-04 EVID-05 conflict (4 candidates):**

| Tag | Candidate | Source | Form |
|-----|-----------|--------|------|
| Option A | Trig encoding for 3 angles | Issue doc (§5.3, lines 270–289 / 422–468) | `[sin θ_L, cos θ_L, sin φ_L, cos φ_L, sin γ_orb]` over the L̂-direction angles plus orbital phase of the heaviest body |
| Option B | Shape invariants + direction cosines | Issue doc (§"Recommended Option B", lines 499–579) | `[I₁, I₂, I₃, …, c₁, c₂]` style — shape invariants plus direction-cosine orientation slots |
| Option C | Reconstructive Jacobi state | Resolution doc (§5.2–5.4, lines 459–572) | `[m₁, m₂, m₃, ρ_x, λ_x, λ_y, ρ̇_x, ρ̇_y, ρ̇_z, λ̇_x, λ̇_y, λ̇_z, E]` — orientation implicit in the 6D velocity vector |
| Option D | Status quo (codify live code) | `pinn/data-processing-pipeline-full.py:1129–1146` *(pre-2026-05-19; now v1.3-era artifact only, not canonical)* | `(m₁_frac, m₂_frac, m₃_frac, E_norm, L_norm, Q_norm, s_min_norm, I₁_norm, I₂_norm, I₃, θ₁_norm, θ₂_norm, I_norm)` — hybrid: shape invariants + position-velocity angles for bodies 1, 2 |

**Important nuance:** The live code's `θ₁, θ₂` are NOT the orbital angles of issue-doc Option A and NOT direction cosines of issue-doc Option B. They are the angles between r and v for bodies 1 and 2 (`pinn/data-processing-pipeline-full.py:1062–1085`). This is a fifth shape that doesn't cleanly match any of the candidates above — Option D treats it as its own candidate.

**Source of correction:** Phase 17 discussion-phase parallel research:
- Resolution-doc deep read (`ctl_pinn_resolution.md` §3.3, §5.2–5.4, §6.3).
- Issue-doc deep read (`01-architecture-and-physics-foundations.md` §5.3 + "Recommended Option B").
- Live-code audit (`pinn/data-processing-pipeline-full.py` IC formulation lines 1062–1146; `pinn/basic_architecture.py` input/output dims and absent COM head). *(Pre-2026-05-19; superseded by no-live-code directive.)*

**Implication for Phase 17:**
- The EVID-05 record for B-04 (`evidence/B-04.md`) must include all four candidates above and the live-code position, not the original two-option framing.
- The B-04 verdict drawn from the EVID-02 enum (`accept-resolution` / `accept-issue-doc` / `accept-third-position` / `reject-both-as-unsupported` / `defer-with-blocker`) now has a richer candidate set: `accept-resolution` = Option C; `accept-issue-doc` = Option A or Option B (whichever the adjudication selects from the issue doc's two proposals); `accept-third-position` would cover Option D (codify status quo) or any other novel construction.

**Ledger effect:** No status change. B-04 remains `PENDING` with `Sources Disagree? = YES — EVID-05 required`. The 4-candidate framing is mirrored into the B-04 per-finding subsection in `16-ISSUE-LEDGER.md` so Phase 17's adjudication has the corrected starting set.

**Same correction does NOT affect** B-02, B-09, or M5. Their D-08 descriptions remain accurate per the resolution doc.

*Amendment recorded: 2026-05-18, Phase 17 discussion-phase research.*

---

## Amendment — 2026-05-19 (no-live-code directive)

**Trigger:** User directive 2026-05-19 issued during Phase 17 discussion-phase work: *"do not rely on any live code because that code will be updated as we build out and update the framework specs, which are the core documentation that I'm going to use to build the live code later, not during this stage."* Applies to every phase in v1.4 (Phases 17–21).

**Changes applied to this phase's artifacts:**

1. **D-06 (Evidence packet template — fixed schema)** — §4 ("Code evidence") renamed to "FUT-01 Hand-off Note" and repurposed for forward-pointing hand-off documentation only. Live code in `pinn/` is NOT v1.4 evidence. The reframed §4 instructs the agent to record v1.3-era code paths only when a FUT-01 code-rewrite gap exists, with explicit "NOT v1.4 evidence" framing. All other sections (1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12) are unchanged.

2. **"Load-bearing live code" subsection (Canonical References)** — renamed to "v1.3-era live code (NOT v1.4 evidence)" and reframed as FUT-01 hand-off reference only. The previous "Phase 16 cites for B-01 init formula" and "Phase 16 cites for B-04 input vector composition and M5 I3_norm map" framings are obsolete — Phase 16's verified status remains, but downstream phases (17–21) do NOT cite live code as evidence.

3. **Companion edits applied in same change-set:**
   - `evidence/_TEMPLATE.md` §"Code Evidence" → renamed to "FUT-01 Hand-off Note" with reframed content.
   - `evidence/README.md` — removed "live code when applicable" from the verdict-allowance clause and the packet-start procedure.
   - `CLAUDE.md` / `AGENTS.md` / `GEMINI.md` CRITICAL GOVERNANCE block — live code removed from grounding sources.
   - `CLAUDE.md` / `AGENTS.md` / `GEMINI.md` Part 2.1 (Source of Truth) and Part 6 (PINN architecture pinned constraint) — updated.
   - `.planning/PROJECT.md` v1.4 Target features / Supporting evidence / Key Decisions — updated.
   - `.planning/REQUIREMENTS.md` Resolution-doc treatment policy, EVID-01, EVID-05, VER-04, SCOPE-01 — updated.

**Implication for Phase 17+ evidence packets:**
- `evidence/{finding-id}.md` §4 (formerly Code evidence, now FUT-01 Hand-off Note) cannot supply evidence for a verdict. It supplies forward-pointing hand-off only.
- EVID-05 contested findings (B-02, B-04, B-09, M5) still require §5 (First-principles physics), §7 (Root-cause framework ambiguity), §8 (Locked convention), §9 (Which source was correct/wrong); these draw on framework specs + physics, NOT live code.

**Implication for Phase 16's prior verdicts:** Phase 16's `VERIFIED` status is unaffected. Phase 16 established the evidence framework; it did not actually USE live code as evidence for any finding's verdict (Phase 16 ships no verdicts — verdicts begin in Phase 17). The directive applies going forward.

**Source:** User chat instruction 2026-05-19; mirrored across all governance artifacts on the same date.

*Amendment recorded: 2026-05-19, Phase 17 discussion-phase governance update.*
