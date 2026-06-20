# Phase 31: Resolution Doc Readiness Verification - Context

**Gathered:** 2026-06-20
**Status:** Ready for planning
**Mode:** `--auto --all` — all gray areas auto-selected; recommended options chosen by Claude and logged in `31-DISCUSSION-LOG.md`. The user did not interactively ratify these; every decision is grounded in `31-SPEC.md` / `.planning/ROADMAP.md` (Phase 31 SC1–SC4) / `.planning/REQUIREMENTS.md` (SCOPE-12) / the **verified** v1.5 Phase 24.5 analog (`24.5-PLAN.md`, `24.5-READINESS-REPORT.md`, `24.5-RESOLUTION-MAP.md`) / the Phase 30 precedent (`30-CONTEXT.md`), and marked Claude's discretion otherwise. **No source-silent semantic decision arose** — the three open decisions (report/map markdown, line-range capture, four-check order) are operational / presentation form whose *schema* is already fixed by the SPEC and the verified analog, so the STOP protocol recorded no gap (nothing invented). Run from the isolated `milestone/v1.6` specwork worktree.

<domain>
## Phase Boundary

Produce a pass/fail **readiness verdict** on the landed issue-03 resolution doc (`research_result/03-final-resolution.md`, 282 lines / 48,049 bytes, §0–§7 with §1.1–§1.18 per-finding subsections) — confirming all **18 selected findings** are covered, **zero** v1.5-verified dataset facts are contradicted, and **zero** locked v1.4/v1.5 conventions are violated — plus a standalone quick-reference map, so that adjudication Phases 32–36 are either **unblocked** (`READY` / `READY-WITH-CAVEATS`) or **held** with routed fix instructions (`NOT-READY`). Phase 31 is the operational readiness gate between the external ERW research and adjudication — the **v1.5 Phase 24.5 analog** (operational, 0 requirement IDs). It **verifies and maps** the candidate verdict source; **it adjudicates nothing**.

**Not this phase:** any adjudication, verdict, evidence packet, or root-cause conflict resolution (Phases 32–36); deciding the three `surface_to_user` decisions D-04/D-05/D-06 (confirmed-present-and-flagged here, **adjudicated in Phase 32 / EVID-15**); editing `ctl_instruction.md` / `pinn_architecture.md` (Phases 33–35); editing or re-writing the resolution doc (the user's external product — read and map only; if `NOT-READY`, route fixes to the consolidation agent); empirical verification / re-measurement of any dataset figure (no Phase-24 analog in v1.6 — figures are checked only for *contradiction* of already-v1.5-verified facts, never re-measured; re-measuring is FUT); re-opening any locked v1.4/v1.5 convention incl. `D = 6.694` (SCOPE-12; only Phase 32 EVID-15 may revisit one); running formula-sanity probes against `pinn/` (SCOPE-15, Phases 33–36).

**Governance:** v1.6 runs under the full STOP protocol (`CLAUDE.md`/`AGENTS.md` "CRITICAL GOVERNANCE", adjudication-milestone applicability). Source-silent semantic / process-schema / cross-phase decisions are surfaced as gaps in `31-GAPS.md` + `.planning/milestones/v1.6-GAPS.md` (create on first gap), never invented. A `silent` finding is always reported as a gap, never filled.

</domain>

<spec_lock>
## Requirements (locked via SPEC.md)

**8 requirements are locked** (R1 pre-execution gate; R2 presence/structural check; R3 finding-coverage crosswalk over 18 findings; R4 dataset-figure consistency vs the archived v1.5 verified-facts register; R5 locked-convention compliance; R6 resolution-doc quick-reference map; R7 readiness report + gate decision; R8 phase boundary + governance). Ambiguity score 0.09 (gate ≤ 0.20). See `31-SPEC.md` for full requirements, boundaries, constraints, acceptance criteria, edge coverage, and prohibitions.

Downstream agents MUST read `31-SPEC.md` before planning or implementing. Requirements are not duplicated here.

**In scope (from SPEC.md):**
- The two deliverables: `31-READINESS-REPORT.md` and `31-RESOLUTION-MAP.md`.
- The pre-execution gate (doc-present-and-canonical + Phase-30-complete).
- The four readiness checks: presence/structural; finding-coverage crosswalk (18 findings); dataset-figure consistency vs the archived v1.5 verified-facts register; locked v1.4 + v1.5 convention compliance.
- The gate decision (`READY` / `READY-WITH-CAVEATS` / `NOT-READY`) with fix-routing and an affected-only re-check protocol.
- The STATE/ROADMAP gate-state update reflecting the outcome (via gsd-tools handlers).

**Out of scope (from SPEC.md):** adjudication / verdicts / evidence packets / root-cause conflict resolution (Phases 32–36; D-04/D-05/D-06 → Phase 32 EVID-15); editing `ctl_instruction.md` / `pinn_architecture.md` (Phases 33–35); editing or re-writing the resolution doc; empirical verification of any dataset figure (no Phase-24 analog; figures checked for contradiction only, never re-measured — FUT); re-opening / re-adjudicating any locked v1.4/v1.5 convention incl. `D = 6.694` (SCOPE-12; only Phase 32 EVID-15); running formula-sanity probes against `pinn/` (SCOPE-15, Phases 33–36).

</spec_lock>

<decisions>
## Implementation Decisions

> All decisions are HOW-to-execute choices (the SPEC locks WHAT and the pass/fail criteria). Each is grounded in `31-SPEC.md` + the **verified** v1.5 Phase 24.5 analog (`24.5-VERIFICATION.md` PASSED) unless marked Claude's discretion. The *schema* of every deliverable is already fixed (SPEC R6/R7 + the analog), so these settle *rendering / mechanics / ordering* only — none defines a new process-artifact schema, so none is a MUST-surface decision.

### Plan decomposition
- **D-01:** **Single plan, single wave** (`31-01-PLAN.md`), mirroring the analog `24.5-01-PLAN.md`. Phase 31 is a lightweight, single-agent, read-and-check pass (no probe authoring, no spec edits); the four checks are independent reads of one document and do not warrant wave parallelization. The planner MAY split into ordered tasks within the one plan (the analog used 7 tasks) but SHOULD NOT fan out into multiple plans.

### Exact report/map markdown (SPEC "Next step" item 1)
- **D-02:** **Model both deliverables byte-structure on the verified v1.5 24.5 analog**, adapted to v1.6's 18-finding set and the doc's §0–§7 / §1.1–§1.18 structure. This *grounds* the markdown in a user-accepted precedent rather than inventing a schema.
- **D-03:** `31-READINESS-REPORT.md` sections (from `24.5-READINESS-REPORT.md` + SPEC R7): **(1)** executive-summary verdict (`READY` / `READY-WITH-CAVEATS` / `NOT-READY`); **(2)** pre-execution gate table (`Gate condition | Result | Evidence` — record path + byte count for the doc, STATE Phase-30-complete citation); **(3)** check results — a summary table (`# | Check (R-task) | Result`) followed by per-check detail for R2–R5 (the crosswalk table, the consistency table, the compliance table); **(4)** gap list (`ID | Caveat/Gap | Affects (finding/convention) | Owner / route | Blocking?`); **(5)** fix instructions (per gap — what is missing, which finding it affects, what the fix should produce); **(6)** re-check protocol (affected-only re-run + line-range refresh on re-pagination); **(7)** gate decision; **(8)** acceptance-criteria check against the SPEC's 9 criteria.
- **D-04:** `31-RESOLUTION-MAP.md` sections (from `24.5-RESOLUTION-MAP.md` + SPEC R6): **resolution-doc identity** (path, byte count, committed revision, date — the line-range anchor); **§1 section index** (`§ | Lines | Covers`); **§2 finding→section mapping** over all **18** findings (`Finding ID | Title | Resolution-Doc Section | Lines | Coverage`); **§3 citation guide** (verbatim file path, §/finding-ID anchors, a concrete `…/03-final-resolution.md:START–END` example for EVID-11); **§4 verdict-direction preview** (`Finding | Direction | one-line note` — one word per finding); **§5 out-of-scope / forward-reference notes**; **§6 open-items carry-forward** drawn from the doc's own §4 gap register + §6 non-independent-input note.
- **D-05:** The gate-verdict precedence is **fixed by SPEC R7 and is not a discretion item**: any `NOT-READY` trigger (a `silent` finding, a contradiction of a v1.5-verified fact, or a locked-convention violation) → `NOT-READY` regardless of how many checks pass; absent any trigger, any caveat (`surface_to_user` / `defer` rows, non-contradicting unverified figures, scope observations, the §6 non-independence note) → `READY-WITH-CAVEATS`; all-clean → `READY`. The exec-summary verdict MUST be re-derivable from the four check tables by this precedence (no rubber-stamp).

### Line-range capture method (SPEC "Next step" item 2)
- **D-06:** Capture each section's line range directly from the **committed** resolution doc (e.g. `grep -n` on the §0–§7 and §1.1–§1.18 headers, or a line-numbered read), and record it in the map's §1 section index and §2 mapping.
- **D-07:** **Anchor line ranges to the committed revision** — the map's identity block records the byte count (48,049) + commit/date the line numbers are valid for (SPEC R6). The **stable citation key is the §/finding-ID anchor**, not the line number: §/finding-ID anchors survive re-pagination, line numbers do not. On a `NOT-READY` re-delivery, only the line ranges are refreshed (affected-only re-check, D-03 §6).

### Four-check task order (SPEC "Next step" item 3)
- **D-08:** Execution order, derived from data dependencies and matching the analog's 7-task sequence: **pre-exec gate (R1) → presence/structural (R2) → finding-coverage crosswalk (R3) → dataset-figure consistency (R4) → locked-convention compliance (R5) → resolution-doc map (R6, consumes R3's mapping) → readiness report (R7, consolidates R2–R5) → gate decision + STATE/ROADMAP update (R7 close)**. Rationale: the gate precedes all checks (a stub/empty doc or missing Phase-30 marker STOPs before any check runs); R2 precedes R3–R5 (a structurally incoherent doc makes the crosswalk meaningless); R3–R5 are mutually independent and run in SPEC order; the map derives from the crosswalk; the report consolidates everything; the gate decision is last.

### Crosswalk finding set (locked, restated for the planner)
- **D-09:** The crosswalk checks exactly **18** findings = the 15 ROADMAP-SC1 findings (B-07, B-08, M6, M7, M14, M15, M16, D5, NS-12, NS-13, NS-18, D-04, D-05, D-06, `D = 6.694`) **plus** the 3 contract-phase extras (adaptive stage assignment §1.15 → CURR-01; `L_max`/`tau_L` formulas §1.17 → CURR-02; ALM `mu_p` clamp §1.18 → LOOP-05). Matching is by finding **identity**, not literal heading text (e.g. doc §1.12 "componentwise automatic differentiation" = NS-12; §1.1 "Causal-training mode" = D-04). A `surface_to_user` verdict (D-04/D-05/D-06) is `covered`-as-routed-human-approval; a `defer` verdict is `covered`-with-routing — **neither is `silent`**. No selected finding may be silently dropped (row count over the selected set = 18).

### Verified-facts source (locked, restated for the planner)
- **D-10:** The dataset-figure consistency check (R4) runs against the **archived v1.5** register `.planning/milestones/v1.5-phases/24-empirical-dataset-verification-and-correction-addendum/24-VERIFIED-FACTS.md` (CLM-01..13 + DATA-05) — the only in-repo verified-facts source (v1.6 has no Phase-24 analog). Contradiction-only fails; agreement within the verified fact's stated precision (e.g. doc `~2,565` vs verified `~2,565`) is consistent; a figure v1.5 never verified is an unverified-(claimed) caveat flagged FUT, **not a failure**; zero mapped figures = a recorded vacuous pass.

### Claude's Discretion
- Exact column headers, table vs. bulleted rendering, and heading capitalization **within** the fixed section set of each report (presentation-only; the analog headers are the recommended default).
- The precise grep/read mechanism used to capture line ranges (D-06) — any method that yields revision-anchored ranges is acceptable.
- Whether the per-check detail tables live inline under §3 of the report or in clearly-labeled subsections (recommended: inline, mirroring `24.5-READINESS-REPORT.md`).

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase requirements & protocol (read first)
- `.planning/phases/31-resolution-doc-readiness-verification/31-SPEC.md` — the 8 LOCKED requirements (R1–R8), boundaries, constraints, acceptance criteria, edge coverage, prohibitions, gate-verdict precedence. Read before anything else.
- `.planning/ROADMAP.md` §"Phase 31" — goal + SC1–SC4 (the 18-finding set, no-contradiction/no-violation, the quick-reference map, NOT-READY fix-routing); the ⛔ external-gate semantics; Phases 32–36 gate on this passing.
- `.planning/REQUIREMENTS.md` — SCOPE-12 (the locked v1.4 + v1.5 outcomes that R5 checks), VER-13..18 traceability, source-treatment policy.
- `CLAUDE.md` / `AGENTS.md` §"CRITICAL GOVERNANCE" — the STOP protocol (adjudication-milestone, v1.6 applicability). Gap registers: `31-GAPS.md` (phase-local) + `.planning/milestones/v1.6-GAPS.md` (milestone index) — neither exists yet; create on first gap.

### The subject (verified, never edited)
- `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md` — the **candidate verdict source** (282 lines / 48,049 bytes; §0 method, §1.1–§1.18 per-finding, §2 claim matrix, §3 disagreement register, §4 gap register, §5 source-coverage, §6 non-independence note, §7 deliverable index). Read and map only; **never edit**. Candidate, not authoritative.

### Verified-facts source for the consistency check (R4)
- `.planning/milestones/v1.5-phases/24-empirical-dataset-verification-and-correction-addendum/24-VERIFIED-FACTS.md` — CLM-01..13 + DATA-05; the only in-repo verified-facts register (no Phase-24 analog in v1.6).

### The analog (format + process — directly reusable, verified precedent)
- `.planning/milestones/v1.5-phases/24.5-resolution-doc-readiness-verification/24.5-PLAN.md` — the 7-task execution template (pre-exec gate → 4 checks → map → report → gate decision); grounds the four-check order (D-08).
- `.planning/milestones/v1.5-phases/24.5-resolution-doc-readiness-verification/24.5-READINESS-REPORT.md` — the report markdown template (grounds D-03).
- `.planning/milestones/v1.5-phases/24.5-resolution-doc-readiness-verification/24.5-RESOLUTION-MAP.md` — the map markdown template incl. the citation guide (grounds D-04, D-06, D-07).
- `.planning/milestones/v1.5-phases/24.5-resolution-doc-readiness-verification/24.5-VERIFICATION.md` — confirms the analog passed; why the structure is a safe, grounded precedent.

### Upstream phase context (carry-forward)
- `.planning/phases/30-research-package-assembly/30-CONTEXT.md` — Phase 30 decisions: the resolution doc's required landing path, the ≥SC1 finding set, the no-in-milestone-verification boundary (D-17), the format precedents, STATE-via-handlers, agent-commit.

### Resolution-doc format precedents (referenced by the map's citation guide)
- `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md` — v1.4 resolution-doc precedent.
- `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/02-resolution-doc.md` — v1.5 resolution-doc precedent.

</canonical_refs>

<code_context>
## Existing Code Insights

> Phase 31 is a documentation-verification phase; the relevant "assets" are planning artifacts and tooling, not application code. `.planning/codebase/` maps (Python/C++ stack) are not relevant here.

### Reusable Assets
- The verified v1.5 24.5 deliverables (`24.5-READINESS-REPORT.md`, `24.5-RESOLUTION-MAP.md`, `24.5-PLAN.md`) — concrete templates for the v1.6 report, map, and task order (D-02..D-08).
- `scripts/agent-commit` — mandatory commit path (set `GIT_AGENT_ID` + `GIT_AGENT_OWNED_PATHS`; `.githooks` active); one atomic commit for the plan; no commit touches `pinn/` or the framework specs.
- gsd-tools STATE/ROADMAP handlers — the only sanctioned way to record the gate-state outcome (no direct STATE.md Write/Edit).

### Established Patterns
- Phase artifacts named `NN-*.md` in `.planning/phases/NN-slug/` (`31-READINESS-REPORT.md`, `31-RESOLUTION-MAP.md`, and — only if a gap arises — `31-GAPS.md`).
- STATE.md mutated only via gsd-tools handlers (universal anti-pattern 15).
- The candidate-verdict-source standing: verify *readiness*, never ratify verdicts (same standing `ctl_pinn_resolution.md` held in v1.4, `02-resolution-doc.md` in v1.5).
- §/finding-ID anchors are the stable citation key; line numbers are revision-scoped (D-07).

### Integration Points
- **Phase 32** (EVID) consumes `31-RESOLUTION-MAP.md` to begin evidence-packet construction (EVID-11 line-range citations) without re-reading the full doc; it adjudicates D-04/D-05/D-06 + `D = 6.694` (EVID-15) that Phase 31 only flags.
- **Phases 32–36** are **blocked** until Phase 31 returns `READY` / `READY-WITH-CAVEATS`; on `NOT-READY` they stay blocked until the routed fix lands and an affected-only re-check passes.
- The gate-state outcome is recorded to STATE/ROADMAP via gsd-tools handlers (R7 acceptance).

</code_context>

<specifics>
## Specific Ideas

- The two reports must let Phase 32 **start without re-reading the full resolution doc** — the map is a navigation aid, the report is the gate verdict. Optimize both for a downstream agent that has not read `03-final-resolution.md`.
- Phase 31 **invents no coverage and no verdict**: a `silent` finding is a gap row, never an inferred position; a "claimed, unverified" figure is never presented as a verified fact and never fails the figure check on its own.
- The `D = 6.694` vs locked raw-mass `D ≈ 4.6416` conflict is **confirmed-compliant-and-flagged only** here (the doc §1.16 upholds `≈ 4.6416` and rejects `6.694`); Phase 31 does **not** re-adjudicate it — that is Phase 32 EVID-15.
- A recommendation in the doc to *change* a locked convention is a recorded **scope observation** (surfaced to the user, never a failure); a *silent breach* of one is a **violation** (a `NOT-READY` trigger).

</specifics>

<deferred>
## Deferred Ideas

- Adjudicating the three `surface_to_user` decisions (D-04 causal training mode, D-05 s_min frame, D-06 epsilon strategy) and the `D = 6.694` conflict — Phase 32 (EVID-15), not here. Phase 31 confirms they are present and flags them.
- Re-measuring / empirically verifying any dataset figure — no Phase-24 analog in v1.6; delegated to FUT / trainex. Phase 31 checks contradiction-against-verified only.
- Editing the resolution doc to close a gap — the doc is the user's external product; Phase 31 routes fix instructions to the consolidation agent, it does not edit.

### Reviewed Todos (not folded)
- **"Review and hand off the trainex-r1 research sub-packages (r1a + r1b)"** (`.planning/todos/.../trainex-r1-research-handoff.md`, match score 0.6) — REVIEWED, **NOT folded**. It belongs to the **trainex track** (training-execution; the ERW build-design channel; packages under `framework-specs/trainex-r1/`), a different track from this phase's **specwork / doc-03** readiness verification (`research_reports/03-*/`). It keyword-matched only on "research, source" — the same false match Phase 30 reviewed-and-rejected (`30-CONTEXT.md`). The `31-SPEC` scope locks Phase 31 to the doc-03 readiness checks, and ERW channel separation is absolute, so auto-folding this cross-track item (despite score ≥ 0.4) would breach the locked phase boundary. It remains an open trainex-track user action, untouched by Phase 31.

</deferred>

---

*Phase: 31-resolution-doc-readiness-verification*
*Context gathered: 2026-06-20*
