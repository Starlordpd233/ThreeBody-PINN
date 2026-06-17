# Phase 25: Evidence Framework and Issue Ledger - Context

**Gathered:** 2026-06-11
**Status:** Ready for planning; execution blocked on Phase 24.5 passing and open Phase 25 gaps resolving
**Mode:** `--all --auto` — all gray areas auto-selected; recommended options chosen by Claude per explicit user instruction (auto-advance through discussion, stop before planning) and logged in `25-DISCUSSION-LOG.md`. Decisions are grounded in REQUIREMENTS.md / ROADMAP.md / PROJECT.md / committed Phase 16, 23, 24, 24.5 artifacts wherever possible and marked Claude's discretion otherwise. D-01 is now a formal user-decision gate (`GAP-25-01`), not an execution-time assumption.

<domain>
## Phase Boundary

Stand up the v1.5 adjudication machinery — the evidence-packet template and protocol (EVID-06..09), the fixed verdict enum (EVID-07), false-positive and before/after note conventions (EVID-08/09), and the operating rules for the re-verification ledger (VER-10) — and adjudicate the three known cross-source conflicts at root cause (EVID-10) before any spec edit lands: (1) ratio-based SCS thresholds vs the locked post-v1.3 log gate, (2) `compute_globals` `D = 6.694` vs the v1.4 PHYS-01 D convention, (3) the M11/M12 severity reclassifications. The ledger Phase 24 seeded (`24-ISSUE-LEDGER.md`, 19 findings, all `PENDING`) becomes operational under the protocol this phase establishes.

**Not this phase:** framework-spec edits of any kind (the EVID-10 locked conventions are recorded in spec-edit-ready prose; the corresponding edits land in Phases 26–28); per-finding evidence packets and verdicts for the non-conflict findings (authored by their owning phases 26–28 using this phase's machinery — see D-01); acceptance-check execution (Phase 29); dataset probes (Phase 24, complete); resolution-doc readiness verification (Phase 24.5, gates this phase); any edit to `sampling_method.md` (SCOPE-08), `data_quality_assessment.md` (SCOPE-09), or `pinn/` (SCOPE-10).

**Hard gate:** Phase 25 execution cannot start until Phase 24.5 passes (READY or READY-WITH-CAVEATS per `24.5-PLAN.md` Task 7). As of 2026-06-11 the consolidated resolution doc has landed (`02-resolution-doc.md`, commit `0e691a45`) but Phase 24.5 has NOT yet executed. Planning artifacts may be prepared; the executor must confirm the gate (readiness-report verdict + STATE.md) before any adjudication work.

**Governance:** v1.5 runs under the full STOP protocol (AGENTS.md/CLAUDE.md "CRITICAL GOVERNANCE", v1.5 applicability section). Source-silent semantic / process-schema / cross-phase decisions are surfaced as gaps in `25-GAPS.md` (phase-local, create if absent, append if present) + `.planning/milestones/v1.5-GAPS.md` (milestone index, currently 2 open Phase 25 gaps), never invented. Subagents return findings to the parent; only the parent writes gap registers.

</domain>

<decisions>
## Implementation Decisions

### Phase-scope split (what Phase 25 adjudicates vs. what it only enables)
- **D-01:** Phase 25 delivers the **machinery plus the three known EVID-10 conflict adjudications only**. Per-finding evidence packets and verdicts for the remaining findings are authored by their owning phases (26–28) using this machinery, immediately before their spec edits ("evidence before editing", EVID-06). Basis: the roadmap's Verification protocol assigns the adjudicate→fix→verify loop to every phase 25–29 (step 1 would be vacuous in 26–28 if Phase 25 pre-assigned all verdicts); Phase 27 criterion 4 and Phase 28 criterion 1 say the D=6.694 and SCS edits are applied "per the EVID-10 record" (a Phase 25 product); the Phase 25 goal sentence says the machinery "is established" and "the known cross-source conflicts are adjudicated"; v1.4 precedent (Phase 16 shipped no verdicts; EVID-01..05 mapped to Phase 16 as "defined", operated in 17–21).
  **Execution gate:** `GAP-25-01` records that this is a cross-phase scope decision requiring user confirmation. Do not execute Phase 25 mutations until the user resolves `GAP-25-01` (confirm split reading, choose literal all-19 reading, or define a hybrid).
- **D-02:** Phase 25 makes **zero framework-spec edits**. EVID-10 records stop at "locked convention" stated in spec-edit-ready prose; Phases 27 (PIPE-09) and 28 (VAL-01) land the corresponding edits (roadmap Phase 25 criterion 4 parenthetical). The M11/M12 record informs Phase 26 prioritization.
- **D-03:** The protocol README (D-05) explicitly encodes the downstream enforcement of EVID-06..09: no spec edit in Phases 26–28 without a completed packet + verdict for the finding; phase-exit gate permits only `VERIFIED` or `DEFERRED` for in-scope findings; ledger status edits travel in the same commit as the underlying change. Downstream planners inherit these as plan-level constraints.

### Evidence-packet machinery (template, location, linkage)
- **D-04:** The v1.5 packet template instantiates the v1.4 12-section schema (`16-CONTEXT.md` D-06, as amended 2026-05-19) with these substitutions — no structural redesign. Canonical count: 12 `##` sections plus the `#` title; the new `### Dataset evidence (§3b)` is a sub-block under `## Spec Evidence` and does not add a new `##` section.
  - §2 Source positions: verbatim quotes + line ranges from `pinn_instruction/issues/02-data-pipeline-and-validation.md` AND `research_reports/02-data-pipeline-and-validation/02-resolution-doc.md` (both required even for uncontested verdicts).
  - §3 Spec evidence: line-range citations from current `ctl_instruction.md` / `pinn_architecture.md` (and read-only `data_quality_assessment.md` where it is the sole written home of a convention — see SCS note in specifics).
  - **New §3b Dataset evidence:** DATA-xx citations from `24-VERIFIED-FACTS.md` rows and probe outputs, line-cited — this is EVID-06's fourth source, which v1.4 packets did not have.
  - §4 FUT-01 Hand-off Note: retained unchanged — forward-pointing only, `pinn/` is never evidence (SCOPE-10); these notes feed VER-11's divergence records.
  - §5–§9 EVID-10 sections (first-principles check, root-cause ambiguity, locked convention, which-source-right/wrong): REQUIRED where the ledger row says `Sources Disagree? = YES`; optional otherwise.
  - §6 Verdict: the EVID-07 enum exactly — `accept-resolution | accept-issue-doc | accept-third-position | reject-both-as-unsupported | defer-with-blocker`.
  - §10 Before/after note doubles as the EVID-08 false-positive record: for intentional non-changes it names the spec section, confirms no edit, states why the current convention stands and which source misread it.
- **D-05:** Packets live at `.planning/phases/25-evidence-framework-and-issue-ledger/evidence/{finding-id}.md`, with `evidence/_TEMPLATE.md` and `evidence/README.md` (protocol doc), mirroring the v1.4 layout (`16-.../evidence/`). Phases 26–28 write into this directory.
- **D-06:** The ledger stays at its stable path (`24-ISSUE-LEDGER.md` under the Phase 24 directory — locked by roadmap and Phase 24 D-22). Its `Evidence Packet` column is filled with relative links as packets are created; status transitions are explicit ledger edits in the same commit as the underlying change, logged with date + commit-audit label in the per-finding subsection (v1.4 D-04 discipline). The adjudicated-but-unfixed status convention is blocked on `GAP-25-02`; do not apply `PENDING + Verdict` / `PENDING -> PENDING` semantics until the user resolves it.
- **D-07:** Resolution-doc citations follow the citation guide in `24.5-RESOLUTION-MAP.md` (Phase 24.5 deliverable). Packets cite section + line ranges, never whole files (EVID-06).

### EVID-10 root-cause adjudications (the three known conflicts)
- **D-08:** The Phase 25 EVID-10 work list is exactly the three conflicts named in roadmap Phase 25 criterion 4: (1) ratio-based SCS thresholds (`SCS > 1e-6` reject / `< 1e-8` Stage 5) vs the locked post-v1.3 gate (`ε_H > 10⁻⁵` / `SCS > −5`) — resolution doc §5.1 (Q-C1, marked KNOWN CONFLICT); (2) `compute_globals` `D = 6.694` vs the v1.4 PHYS-01 D convention — resolution doc §4.4 (Q-B4, marked KNOWN CONFLICT); ledger notes `ctl_instruction.md` §2.5 line 598 explicitly rejects the 6.694 form; (3) the M11/M12 severity reclassifications. Each produces a full evidence packet including the first-principles check, named root-cause ambiguity, locked convention in spec-edit-ready prose, and per-claim right/wrong assignment.
- **D-09:** Verdict grounding discipline: the resolution doc is the **candidate** verdict source — its verdict is transcribed unless spec evidence, DATA-xx facts, or first principles show the position fails (REQUIREMENTS.md source-treatment policy). The v1.4-locked conventions and the post-v1.3 SCS gate are **hard constraints**: an adjudication outcome that would overturn a locked convention is a STOP gap for user decision, never an autonomous verdict (mirrors 24.5-PLAN Task 4's "scope observation" handling).
- **D-10:** Where the resolution doc is silent or hedged on a conflict facet — including anything it routes to its own "Open Items register" or "Additional Input Needed" sections (§ lines 756–781) — the outcome is `defer-with-blocker` or a STOP gap per the governance classification, never invention.

### Ledger operation under VER-10 (re-verification protocol)
- **D-11:** Phase 25 re-issues the ledger's Lifecycle Rules block for v1.5: the seeded block carries stale v1.4 applicability text ("Phases 17-22, including Phase 20.5") — update it to the v1.5 spec-edit phases (26–28) and acceptance phase (29), keeping verbatim the state machine (`PENDING → IN_PROGRESS → FIX_APPLIED → VERIFIED`, `DEFERRED` absorbing with written blocker), the batch definition (one GSD plan), transitive-dependent re-verification with regression demotion to `IN_PROGRESS`, and the phase-exit gate. This is a mechanical correction of stale applicability text (Phase 24 D-24 assigned the operating protocol to Phase 25); the change is noted in the ledger's Notes section.
- **D-12:** G1–G5 synthesis rows get **no separate evidence packets**; each closes with its parent finding (G1→B-06, G2→B-11, G3→M11, G4→M13, G5→M12) and the closure is annotated in the per-finding notes (per the ledger seed: "synthesis view, not a duplicate contract").
- **D-13:** Phase 25 mints **no new AC-IDs**; the seeded assignments stand (AC-PIPE-01..10, AC-VAL-01..04). EVID-10 records verify through the owning phase's acceptance check (D=6.694 → AC-PIPE-09; SCS thresholds → AC-VAL-01; M11/M12 → AC-PIPE-03/04). Numeric pass criteria are defined by owning phases under VER-07 and executed in Phase 29.
- **D-14:** Phase 25 may extend `Dependents:` fields when adjudication reveals shared contracts (e.g., SCS ↔ `compute_globals` D, if the EVID-10 work shows the drift normalization couples them); every addition is annotated in the per-finding subsection (v1.4 D-10 pattern).

### Gate compliance and sequencing
- **D-15:** Phase 25 **execution** starts only after Phase 24.5 passes. READY-WITH-CAVEATS is a pass: each caveat whose affected finding is among the three Phase 25 EVID-10 conflicts is propagated into that finding's record before adjudication; caveats for findings outside those three are explicitly noted as carried forward to the owning Phase 26-28 packet. NOT-READY keeps Phase 25 blocked while fix instructions round-trip to the external consolidation agent.
- **D-16:** Phase 25 consumes both Phase 24.5 deliverables: `24.5-RESOLUTION-MAP.md` (section index, finding-to-section mapping, citation guide, verdict-direction preview — the entry point before any full-doc read) and `24.5-READINESS-REPORT.md` (caveat list). Phase 25's planner should treat the map as the navigation contract for the 820-line resolution doc.
- **D-17:** Tag `v1.5-pre-phase-25` is cut from `milestone/v1.5` HEAD at Phase 25 **execution start, after 24.5 passes** — not during this discuss session (deviation from Phase 24's D-25 timing, justified: Phase 24.5 commits will land between now and Phase 25 start, and the tag must capture the true pre-phase state).
- **D-18:** One atomic commit per plan via `scripts/agent-commit` (requires `GIT_AGENT_ID` and `GIT_AGENT_OWNED_PATHS`); STATE.md mutations only via gsd-tools handlers; commit scopes `25` / `25-NN`. Each plan preflights that `scripts/agent-commit` is executable and the required env vars are set before file mutation.

### Claude's Discretion
- Packet filenames for findings whose ledger IDs are not simple letter-number codes (`SCS`, `SASD`, `IPR`, `PSC`, `D-03`, `D=6.694`, `footer`, `mass-drift`) — sanitize to filesystem-safe, self-describing names (e.g., `evidence/compute-globals-D.md` for `D=6.694`) and record the ID→filename mapping in `evidence/README.md`.
- Exact wording/ordering inside `_TEMPLATE.md` and `README.md` within the D-04 section set; HTML comment markers for conditional sections (v1.4 pattern).
- Whether the EVID-10 records for the three conflicts are three separate packets or packets-plus-a-summary note — as long as each conflict has a complete EVID-10 record at a citable path.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase requirements & protocol (read first)
- `.planning/REQUIREMENTS.md` — EVID-06..10 and VER-10 (this phase's six requirements, verbatim), source-treatment policy, SCOPE-06..11 boundaries.
- `.planning/ROADMAP.md` §"Phase 25: Evidence Framework and Issue Ledger" — goal, five success criteria; §"Source treatment & STOP protocol"; §"Verification protocol (applies to every adjudication phase, 25–29)".
- `CLAUDE.md` / `AGENTS.md` §"CRITICAL GOVERNANCE: v1.4 and similar adjudication milestones" — STOP protocol with v1.5 substitutions (gap registers: `25-GAPS.md` phase-local — exists with open Phase 25 gaps, append future gaps; `.planning/milestones/v1.5-GAPS.md` milestone index — mirrors the open/resolved status).

### Candidate verdict source and research inputs
- `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/02-resolution-doc.md` — the consolidated resolution doc (820 lines; landed 2026-06-11, commit `0e691a45`). Candidate verdict source, NOT authoritative. Structure: §0 scope/evidence standard, §1 executive summary, §2 decision matrix, §3 Cluster A (Q-A1..A6 → Phase 26), §4 Cluster B (Q-B1..B4 → Phase 27; §4.4 = D=6.694 KNOWN CONFLICT), §5 Cluster C (Q-C1..C4 → Phase 28; §5.1 = SCS KNOWN CONFLICT), §6 cross-cutting findings, Open Items register, References.
- `.../02-data-pipeline-and-validation/research_results/` — 8 individual AI research reports (Stage-1 inputs). Supporting evidence only: consulted when the consolidated doc's provenance records ambiguity (v1.4 precedent: model reports beside `ctl_pinn_resolution.md`).
- `.../research_package/RESEARCH-CONTEXT-MASTER.md` — framed questions Q-A1..Q-C4 (ledger `Dependents` keys), hard-constraints block (locked v1.4 conventions verbatim), CLM claims register.
- `.../research_package/DATA-07-CORRECTION-ADDENDUM.md` — the correction addendum forwarded to the in-flight research; records which package claims were corrected.

### Adjudication subject
- `pinn_instruction/issues/02-data-pipeline-and-validation.md` — NON-authoritative issue doc; line-cited source for §2 of every packet.

### Phase 24 artifacts (the operating surface)
- `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-ISSUE-LEDGER.md` — THE ledger (19 findings seeded `PENDING`; stable path; Lifecycle Rules block to be re-issued per D-11; per-finding notes carry the AC-IDs and Q-references).
- `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-VERIFIED-FACTS.md` — dataset-evidence annex (CLM-01..12 verdicts + DATA-05 row); the §3b source for every packet.
- `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-DATA05-RERUN-REMEDIATION.md` — resolved DATA-05 boundary (70 base-hier reruns executed + validated 2026-06-11; all eight gates closed); the `footer` and `mass-drift` rows consume this resolved state.

### Phase 24.5 artifacts (gate; two are pending creation)
- `.planning/phases/24.5-resolution-doc-readiness-verification/24.5-PLAN.md` — the 7-task readiness check; Task 7 gate decision rules (READY / READY-WITH-CAVEATS / NOT-READY).
- `.planning/phases/24.5-resolution-doc-readiness-verification/24.5-RESOLUTION-MAP.md` — (pending 24.5 execution) navigation + citation contract for the resolution doc (D-07/D-16).
- `.planning/phases/24.5-resolution-doc-readiness-verification/24.5-READINESS-REPORT.md` — (pending 24.5 execution) gate verdict + caveat list (D-15).

### Current framework specs (spec-evidence source; edited only in Phases 26–28)
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` — §2.5 line 598 explicitly rejects the 6.694 D form (EVID-10 conflict 2 spec evidence).
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` — carries v1.4-locked input/output/COM/softening contracts.
- `pinn_instruction/markdown_conversion/framework-revisions/data_quality_assessment.md` — READ-ONLY (SCOPE-09); per the ledger SCS row it is the sole written home of the locked post-v1.3 gate — citable as spec evidence, never editable.

### v1.4 precedents (machinery to instantiate, not redesign)
- `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md` — D-02..D-19: ledger schema, packet template (12 sections), lifecycle, AC naming; plus the 2026-05-19 no-live-code amendment.
- `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/evidence/_TEMPLATE.md` and `evidence/README.md` — the concrete files D-04/D-05 adapt.
- `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md` — operated-ledger end-state reference (what "done" looked like in v1.4).

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- v1.4 `evidence/_TEMPLATE.md` + `evidence/README.md` — adapt per D-04/D-05; the 12 `##` section headings and EVID-05→EVID-10 section mapping carry over exactly except for the enumerated v1.5 substitutions.
- `24-ISSUE-LEDGER.md` — arrives pre-seeded with 19 rows, AC-ID assignments, Q-reference dependents, and per-finding notes; Phase 25 operates it, never rebuilds it.
- `24-VERIFIED-FACTS.md` — pre-packaged dataset evidence with per-row probe citations; packets cite rows, never re-derive.
- `scripts/agent-commit` — mandatory commit path (`GIT_AGENT_ID` required); one atomic commit per plan.

### Established Patterns
- Phase artifacts named `25-*.md` in `.planning/phases/25-evidence-framework-and-issue-ledger/`.
- One evidence file per finding under `evidence/`, greppable by finding ID (v1.4).
- Line-range citations, never whole-file citations (EVID-06; v1.4 packet discipline).
- Ledger status edits in the same commit as the underlying change; transition log entries use `date commit-audit-label status→status (actor/plan)`.
- STATE.md mutations only via gsd-tools handlers (universal anti-pattern 15).

### Integration Points
- EVID-10 records → Phase 27 (PIPE-09 edit "per the EVID-10 record") and Phase 28 (VAL-01 edit "resolved through the EVID-10 record, not transcribed"); M11/M12 record → Phase 26 prioritization.
- `evidence/README.md` protocol → Phases 26–28 planners inherit packet-before-edit and phase-exit gates (D-03).
- Operated ledger → Phase 29 closure (VER-09/VER-11: nothing closes while in-scope findings are not `VERIFIED`/`DEFERRED`).
- §4 FUT-01 Hand-off Notes → VER-11 divergence records for every DataLoader-implementation-shaped finding.

</code_context>

<specifics>
## Specific Ideas

- **ID-namespace caution:** issue-01 (v1.4) and issue-02 (v1.5) reuse letter-number IDs (e.g., both have a "B-06"). No path collision (different `evidence/` dirs), but every cross-document citation must be directory-qualified so a v1.5 packet is never confused with its v1.4 namesake.
- **SCS gate's written home:** the locked post-v1.3 gate lives only in read-only `data_quality_assessment.md`. The EVID-10 SCS record should note this explicitly — Phase 28's VAL-01 edit must create a canonical SCS contract in the editable specs without touching DQA (SCOPE-09), which is precisely why the root-cause record matters before the edit.
- **Stale lifecycle text:** the seeded ledger's Lifecycle Rules block still reads "Phases 17-22, including Phase 20.5" — v1.4 text carried over by the seed. D-11 fixes this as part of protocol establishment; nothing else in the block changes.
- **Resolution doc self-declared gaps:** the doc carries an "Open Items register" and "Additional Input Needed (this pass)" section — Phase 25's planner should expect some findings to route to `defer-with-blocker` or STOP gaps through D-10 rather than forcing verdicts.
- **The three EVID-10 conflicts are the phase's center of gravity** — they are the v1.5 analogue of v1.4's pre-flagged B-02/B-04/B-09/M5 set, and the ledger already carries `Sources Disagree? = YES — EVID-10 required` on the SCS and D=6.694 rows so executing phases cannot skip them.

</specifics>

<deferred>
## Deferred Ideas

- Framework-spec edits for all findings — Phases 26–28 (PIPE-xx, VAL-xx).
- Per-finding packets/verdicts for non-conflict findings — owning phases 26–28 (D-01).
- Acceptance-check numeric pass criteria and execution — VER-07 definitions in owning phases; execution in Phase 29.
- Ledger linter / CI enum validation — deferred in v1.4 (Phase 16), still out of scope.
- M16 collocation-scaling, G6 causal-training, training-loop metric usage — doc-03 milestone (SCOPE-11).

### Reviewed Todos (not folded)
- **"Review and hand off the trainex-r1 foundational research package"** (`.planning/todos/pending/trainex-r1-research-handoff.md`; at fold time titled "Review and hand off the PH-1 ML-framework research package" at `ph1-framework-research-handoff.md`, renamed 2026-06-11; matched at score 0.6 on the keyword "framework") — NOT folded. It belongs to the parallel training-execution (trainex) stream, not the issue-02 adjudication; folding it would breach the formalized training-execution parallel-work boundary. Deliberate deviation from the auto-fold rule (score ≥ 0.4), logged here for audit.

</deferred>

---

*Phase: 25-Evidence Framework and Issue Ledger*
*Context gathered: 2026-06-11*
