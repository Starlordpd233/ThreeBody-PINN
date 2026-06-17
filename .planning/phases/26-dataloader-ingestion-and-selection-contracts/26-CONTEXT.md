# Phase 26: DataLoader Ingestion and Selection Contracts - Context

**Gathered:** 2026-06-12
**Status:** Ready for planning
**Mode:** `--all --auto` — all gray areas auto-selected; recommended options chosen by Claude per explicit user instruction (provide context, stop before planning) and logged in `26-DISCUSSION-LOG.md`. Every decision below is grounded in REQUIREMENTS.md / ROADMAP.md / PROJECT.md / committed Phase 24, 24.5, 25 artifacts wherever possible and marked Claude's discretion otherwise. The two findings that REQUIREMENTS/ROADMAP reserve for the user (D-03 format choice, M13 fallback) are explicitly NOT auto-decided here — they are structured as execution-time user gates (see D-11/D-12).

<domain>
## Phase Boundary

`ctl_instruction.md` / `pinn_architecture.md` state one coherent DataLoader ingestion-and-selection contract — which trajectories load, how they are addressed, validated, excluded, and what storage format they take — each grounded in verified dataset facts. Six contracts, six requirements:

1. **PIPE-01 / B-06** — Stage 4→5 trajectory-validation (admission) gate: final-timestamp threshold, stage-dependent snapshot minimums, rejection logging.
2. **PIPE-02 / B-11** — ID-resolution: `id_to_path` built from filesystem scan; invariant that trajectory ID ≠ array index.
3. **PIPE-03 / M11** — Blacklist exclusion: load at DataLoader init, exclude, log count, fail loudly if a blacklisted ID reaches a batch (EVID-10 ruling already locked: BLOCKING STANDS).
4. **PIPE-05 / M13** — Gold-counterpart: Stage-5 gold-existence check + fallback policy; if sources are silent/conflicting on the fallback, STOP gap for user decision — never invented.
5. **PIPE-06 / D7** — Footer/parameter heterogeneity: `Result:` footer precedence, folder-default fallback, `tol_confidence` (`direct` vs `inferred`), footer-as-metadata-only.
6. **PIPE-10 / D-03** — Training-data format (HDF5 vs `.npy` vs txt/json): presented to the user with verified evidence; **the user decides**; locked choice recorded in the specs.

**In-scope ledger rows (10):** B-06, B-11, M11, M13, D7, D-03 plus synthesis rows G1→B-06, G2→B-11, G3→M11, G4→M13 (close with parents, no separate packets). G5 belongs to Phase 27 (parent M12).

**Not this phase:** Phase 27 contracts (M12 points-per-trajectory, precision/Decimal, dt_out/stage-query, `compute_globals` — the M12 and D=6.694 EVID-10 records are consumed as locked constraints here, their spec edits land in Phase 27); Phase 28 validation-metrics contracts; Phase 29 acceptance-suite execution, SI-ledger reconciliation, and handoff; FUT-01 implementation of any contract (DataLoader/TrajectoryValidator/TrajectoryIndex code); doc-03 items (M16 collocation scaling, G6 causal training, training-loop metric usage — SCOPE-11); any edit to `sampling_method.md` (SCOPE-08), `data_quality_assessment.md` (SCOPE-09), or `pinn/` (SCOPE-10).

**Hard gate status:** Phase 24.5 passed READY-WITH-CAVEATS (2026-06-11); Phase 25 complete with UAT 9/9 (2026-06-12). Phase 26 is unblocked. Tag `v1.5-pre-phase-26` is cut from `milestone/v1.5` HEAD at execution start (see D-10).

**Governance:** v1.5 runs under the full STOP protocol (AGENTS.md/CLAUDE.md "CRITICAL GOVERNANCE", v1.5 applicability). Source-silent semantic / process-schema / cross-phase decisions are surfaced in `26-GAPS.md` (phase-local, create on first gap) + `.planning/milestones/v1.5-GAPS.md` (milestone index), never invented. Subagents return findings to the parent; only the parent writes gap registers.

</domain>

<decisions>
## Implementation Decisions

### Spec-edit strategy (where and how the six contracts land)
- **D-01 — Candidate-edit consumption:** Each finding's spec edit starts from the resolution doc's part-6 "proposed specification text" as the **candidate** edit (`24.5-RESOLUTION-MAP.md` §3: "Phases 26–28 consume these as candidate edits, not as authority"). The candidate is transcribed unless current-spec evidence, `24-VERIFIED-FACTS.md` CLM/DATA rows, or first principles show the position fails (Phase 25 D-09 verdict discipline carried forward). A failing candidate routes to `accept-third-position` / `reject-both-as-unsupported` adjudication — and any newly discovered cross-source conflict triggers EVID-10 (full conflict sections in the packet before any edit).
- **D-02 — Hard constraints, not re-adjudicable:** the v1.4-locked conventions (14D input, Jacobi IC₁₃, mass-weighted COM head, PHYS-03 softening, PHYS-01 raw-mass D, post-v1.3 SCS gate) AND the Phase 25 EVID-10 locked conventions (SCS log gate stands; raw-mass `D ≈ 4.6416`; M12 `n_pts = min(n_pts_cap, n_snapshots)`; M11 BLOCKING severity). Where the B-06 admission gate interacts with snapshot minimums, the packet cites the locked M12 rule (`evidence/m11-m12-severity.md`) — Phase 26 does not re-decide sampling feasibility; M12's spec edit is Phase 27's. An adjudication outcome that would overturn any locked convention is a STOP gap, never an autonomous verdict.
- **D-03 — Placement:** `ctl_instruction.md` is the primary home for the DataLoader ingestion/selection contracts (all six ledger rows name it; the D-03 row names it alone); `pinn_architecture.md` is edited only where the candidate text requires an architecture-side statement (its ledger Spec Targets listing permits but does not mandate edits). Exact heading/numbering/section placement is presentation-level discretion, recorded in each packet's before/after note.
- **D-04 — Edit perimeter:** zero edits outside `ctl_instruction.md` / `pinn_architecture.md`. `data_quality_assessment.md` is citable as evidence but never editable; live-loader facts (OI-8) appear only in §4 FUT-01 Hand-off Notes, never as grounding.

### Evidence-packet workflow and batching
- **D-05 — Packet-before-edit:** one packet per finding at `.planning/phases/25-evidence-framework-and-issue-ledger/evidence/{finding-id}.md`, copied from `_TEMPLATE.md`, authored by Phase 26 **immediately before that finding's spec edit** (GAP-25-01 split reading; `evidence/README.md` D-03 enforcement). New packets expected for B-06, B-11, M13, D7, D-03 (filenames per the README sanitization rule; ID→filename map in `evidence/README.md` updated in the same commit that adds each packet).
- **D-06 — M11 reuses its existing packet:** the ledger's M11 row already links `evidence/m11-m12-severity.md` with verdict assigned (adjudicated-but-unfixed per the GAP-25-02 status legend). Phase 26 extends that record — M11-specific before/after note for the PIPE-03 edit + M11 status transitions — rather than authoring a duplicate. M12 content in the same file is untouched (Phase 27 owns it); transitions are logged per-finding so the shared file never conflates the two.
- **D-07 — Synthesis rows:** G1/G2/G3/G4 get no separate packets; each closes with its parent (B-06/B-11/M11/M13) and the closure is annotated in the per-finding ledger notes (Phase 25 D-12 carried forward).
- **D-08 — Batch and regression discipline:** a batch = one GSD plan. Ledger status edits + Evidence-Packet links travel in the same commit as the underlying change (splitting them is a process defect). After each plan's edits, previously `VERIFIED` findings sharing edited spec sections or `Dependents` links are re-verified; regression demotes to `IN_PROGRESS`. Phase exit permits only `VERIFIED` or `DEFERRED` for the ten in-scope rows.
- **D-09 — Ordering:** autonomous, well-grounded findings first — B-06 and B-11 (interlinked admission/indexing contracts), M11 (verdict already locked, edit-ready), then D7. The two user-interaction findings (M13 STOP-gap-shaped, D-03 user gate) sit in dedicated plans isolated from the autonomous chain so spec work never blocks on user availability (dependency-scoped blocking, per EDL/STOP practice). Exact wave structure is the planner's call.
- **D-10 — Operational mechanics (Phase 25 D-17/D-18 carried forward):** tag `v1.5-pre-phase-26` from `milestone/v1.5` HEAD at execution start (not during this discuss session); one atomic commit per plan via `scripts/agent-commit` (requires `GIT_AGENT_ID` + `GIT_AGENT_OWNED_PATHS`; no broad staging); commit scopes `26` / `26-NN`; STATE.md mutations only via gsd-tools handlers. Each plan preflights the commit wrapper and env vars before any file mutation.

### User-decision findings (NOT auto-decidable)
- **D-11 — PIPE-10 / D-03 is a mandatory user gate:** REQUIREMENTS.md PIPE-10 verbatim: "presented to the user with verified evidence; the user decides; the locked choice is recorded in the framework specs." Structure: a dedicated non-autonomous plan (`autonomous: false`; precedent 23-02 and 24-04) presenting HDF5 vs `.npy`/`.npz` vs txt/json with verified evidence (DATA-06 snapshot/`dt_out` distributions, dataset-scale facts from `24-VERIFIED-FACTS.md`) and the resolution doc §3.6 Q-A6 position (HDF5 canonical, `.npy`/`.npz` derived, JSON inspection-only) presented as the **candidate recommendation, not a pre-locked choice**. No execution mode (including `--auto`) may select for the user. The user-locked choice is then recorded in `ctl_instruction.md`, the D-03 packet, and the ledger in one commit.
- **D-12 — PIPE-05 / M13 decision rule:** the packet is authored from a full read of resolution doc §3.4 Q-A4 (`02-resolution-doc.md:255–293`) plus OI-7 (the Q-A4 label-semantics "STOP-gap defeater" + gold-rerun residue). Then: (a) if the resolution doc's position — no fallback exists under the locked stage definitions; both issue-doc options rejected — is fully grounded and consistent with locked conventions, it is adopted as the candidate verdict and the contract defines the Stage-5 gold-existence check plus an explicit no-fallback policy; (b) if **any** facet of the fallback choice remains source-silent or conflicting — including whether OI-7's "defeater" genuinely disposes of the roadmap's STOP-gap expectation (Phase 26 success criterion 4 wording controls) — it is surfaced as `GAP-26-NN` for user decision, never invented. Pre-registered as the phase's most likely STOP gap.
- **D-13 — Caveat propagation (Phase 25 D-15 pattern):** before adjudicating each finding, the carried resolution-doc caveats are propagated into its packet — OI-6 (no-footer probe-coverage gap) → D7; OI-7 → M13; OI-8 (M11 live-loader consumption status, outside grounding) → M11's §4 FUT-01 Hand-off Note only; the OI-9 note (DATA-05 70-file rerun executed + validated 2026-06-11; quarantine clause liftable on re-verification) is recorded wherever D7's footer evidence touches the rerun files.

### Acceptance checks (VER-07 definitions + per-finding execution)
- **D-14 — Define AND run per finding:** each packet defines its reserved acceptance check (AC-PIPE-01/02/03/05/06/10 — no new AC-IDs) numerically per VER-07: pass criterion, the data it runs on, the exact command/function. The resolution doc's part-5 "verification suggestion" is consumed as the candidate check design. Per the roadmap verification protocol (step 3), Phase 26 **executes** each finding's check via a disposable probe to move its row to `VERIFIED` before phase exit; Phase 29 later builds and re-executes the full acceptance suite (VER-09). Checks are spec-consistency probes and/or dataset probes reusing Phase 24 probe commands where applicable; no probe touches `pinn/`.
- **D-15 — Probe hygiene:** every probe's command + output is captured re-derivably in the packet (SCOPE-06 discipline: method and command recorded so claims re-derive); disposable probe scripts, if any, live under the phase directory, never under `pinn/`.

### Claude's Discretion
- Exact packet filenames for the five new packets (README sanitization rule governs; mapping recorded in `evidence/README.md`).
- Exact spec heading/numbering placement inside `ctl_instruction.md` (presentation-level; recorded in before/after notes).
- Wave structure and plan count (subject to D-09's ordering and D-11/D-12's isolation of user-gate work).
- Whether per-finding probes are inline commands in packets or small scripts under the phase dir (subject to D-15).

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase requirements & protocol (read first)
- `.planning/REQUIREMENTS.md` — PIPE-01/02/03/05/06/10 verbatim (this phase's six requirements), VER-07 wording, source-treatment policy, SCOPE-06..11 boundaries.
- `.planning/ROADMAP.md` §"Phase 26: DataLoader Ingestion and Selection Contracts" — goal + five success criteria; §"Source treatment & STOP protocol"; §"Verification protocol (applies to every adjudication phase, 25–29)".
- `CLAUDE.md` / `AGENTS.md` §"CRITICAL GOVERNANCE: v1.4 and similar adjudication milestones" — STOP protocol with v1.5 substitutions (gap registers: `26-GAPS.md` phase-local, create on first gap; `.planning/milestones/v1.5-GAPS.md` milestone index).

### Phase 25 machinery (the operating rules for every Phase 26 edit)
- `.planning/phases/25-evidence-framework-and-issue-ledger/evidence/README.md` — THE protocol: four EVID-06 sources, verdict enum, status lifecycle + GAP-25-02 adjudicated-but-unfixed legend, EVID-10 trigger table, regression policy, phase-exit rule, D-03 downstream enforcement (packet-before-edit, same-commit ledger edits), AC-ID reservations, ID→filename map, packet start procedure.
- `.planning/phases/25-evidence-framework-and-issue-ledger/evidence/_TEMPLATE.md` — the 12-section packet schema (§3b Dataset Evidence; §5–§9 EVID-10 sections required when sources disagree).
- `.planning/phases/25-evidence-framework-and-issue-ledger/evidence/m11-m12-severity.md` — the locked M11 ruling (BLOCKING STANDS; OI-8 carry-forward) Phase 26 extends for PIPE-03, and the locked M12 rule the B-06 packet cites (D-02).
- `.planning/phases/25-evidence-framework-and-issue-ledger/25-CONTEXT.md` — Phase 25 decisions D-01..D-18 (machinery design rationale; D-09 verdict discipline; D-12 synthesis-row closure; D-17/D-18 operational mechanics).
- `.planning/phases/25-evidence-framework-and-issue-ledger/25-GAPS.md` — GAP-25-01 (split reading: Phase 26 authors its own packets) and GAP-25-02 (adjudicated-but-unfixed semantics) resolutions.

### Ledger and verified facts (the status index and §3b evidence source)
- `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-ISSUE-LEDGER.md` — THE ledger at its stable path; ten Phase 26 rows (B-06, B-11, M11, M13, D7, D-03, G1–G4); same-commit status discipline; per-finding notes carry AC-IDs and Q-references.
- `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-VERIFIED-FACTS.md` — CLM/DATA verified rows; the §3b dataset-evidence source for every packet (cite rows, never re-derive).
- `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-DATA05-RERUN-REMEDIATION.md` — resolved DATA-05 boundary (70 base-hier reruns validated 2026-06-11); relevant where D7 footer evidence touches rerun files (OI-9 note).

### Candidate verdict source and navigation
- `.planning/phases/24.5-resolution-doc-readiness-verification/24.5-RESOLUTION-MAP.md` — navigation + citation contract: §3 Cluster A line map (Q-A1 105–177, Q-A2 178–220, Q-A3 221–254, Q-A4 255–293, Q-A5 294–344, Q-A6 345–382), 7-part subsection structure (part 6 = proposed spec text; part 5 = verification suggestion), citation format, verdict-direction preview.
- `.planning/phases/24.5-resolution-doc-readiness-verification/24.5-READINESS-REPORT.md` — gate verdict + caveat list (OI-3/6/7/8/11/12 dispositions).
- `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/02-resolution-doc.md` — the candidate verdict source (820 lines; NOT authoritative). Phase 26 scope: §3 Cluster A (lines 101–382) + Open Items register (756–779).
- `pinn_instruction/issues/02-data-pipeline-and-validation.md` — NON-authoritative issue doc; line-cited source for §2 of every packet.
- `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/research_results/` — 8 Stage-1 reports; supporting evidence only, consulted when consolidation provenance records ambiguity.

### Edit targets and spec evidence
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` — primary edit target (D-03 of this context).
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` — secondary edit target (architecture-side statements only).
- `pinn_instruction/markdown_conversion/framework-revisions/data_quality_assessment.md` — READ-ONLY (SCOPE-09); citable spec evidence, never editable.

### Commit machinery
- `scripts/agent-commit` — mandatory commit path (`GIT_AGENT_ID` + `GIT_AGENT_OWNED_PATHS`); one atomic commit per plan.
- `docs/git-guidelines.md` — full commit-message policy (scopes `26` / `26-NN`; body required for `.planning/` and spec commits).

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `evidence/_TEMPLATE.md` + `evidence/README.md` (Phase 25) — copy source and protocol; Phase 26 instantiates, never redesigns.
- `evidence/m11-m12-severity.md` — M11's packet already exists with verdict; Phase 26 extends, never duplicates (D-06).
- `24-ISSUE-LEDGER.md` + `24-VERIFIED-FACTS.md` — pre-seeded status index and dataset evidence; packets cite rows.
- Phase 24 probe commands (recorded per-row in `24-VERIFIED-FACTS.md`) — reusable as acceptance-check building blocks (D-14).
- `scripts/agent-commit` — commit wrapper with agent-policy enforcement.

### Established Patterns
- Phase artifacts named `26-*.md` in `.planning/phases/26-dataloader-ingestion-and-selection-contracts/`.
- One evidence file per finding under the Phase 25 `evidence/` dir, greppable by finding ID; line-range citations, never whole-file.
- Ledger status edits in the same commit as the underlying change; transition log entries `date commit-audit-label status→status (actor/plan)`.
- Non-autonomous user-gate plans (`autonomous: false`) for decisions reserved to the user — precedent 23-02, 24-04.
- STATE.md mutations only via gsd-tools handlers.

### Integration Points
- Phase 26 packets/edits → Phase 29 acceptance suite (AC-PIPE-01/02/03/05/06/10 definitions consumed by VER-09 execution).
- §4 FUT-01 Hand-off Notes in each packet → VER-11 divergence records (every DataLoader-implementation-shaped finding).
- B-06 admission-gate contract ↔ locked M12 rule (Phase 27 spec edit) — cite, don't re-adjudicate (D-02).
- D7 footer contract ↔ Phase 27 footer/mass-drift + precision work (Q-B2/Q-B3 share the footer evidence base) — keep contracts data-side and non-overlapping; flag overlap to the planner if candidate texts collide.
- Spec sections edited here are the regression surface for Phases 27–28 batches (Dependents fields in the ledger).

</code_context>

<specifics>
## Specific Ideas

- **ID-namespace caution (carried from Phase 25):** v1.4/issue-01 also had a "B-06". Every citation must be directory-qualified so a v1.5 packet is never confused with its v1.4 namesake.
- **Cross-phase file writes are by design:** the ledger lives under the Phase 24 directory and packets live under the Phase 25 `evidence/` directory; Phase 26 writes into both. This is locked by roadmap + Phase 25 D-05/D-06 — do not "fix" it by relocating files.
- **Resolution-doc line anchors:** the Cluster A line ranges are anchored to the committed 820-line revision (2026-06-11). If the doc is ever re-delivered, re-verify line numbers; §/Q-ID anchors are stable.
- **B-06 preview:** the resolution doc proposes a new "Step 1A — Trajectory Admission Gate" in `ctl_instruction.md` and rejects the `>=200` snapshot floor — the packet must reconcile this with the locked M12 rule by citation (D-02), not by re-opening sampling feasibility.
- **M13 is "defers-with-contract":** the one Cluster A finding where the resolution doc itself did not produce a normal recommendation. Expect `defer-with-blocker` or a STOP gap as a legitimate outcome; forcing a verdict would violate D-12.
- **D-03's ledger row names `ctl_instruction.md` alone** as spec target — the format contract has no architecture-side component.

</specifics>

<deferred>
## Deferred Ideas

- M12 points-per-trajectory, precision/Decimal, dt_out/stage-query, `compute_globals` spec edits — Phase 27 (PIPE-04/07/08/09; G5 closes there with M12).
- SCS/SASD/IPR/PSC canonical metric contracts — Phase 28 (VAL-01..04; the SCS EVID-10 record's spec edit lands there).
- Acceptance-suite build + full execution, ledger close, SI-ledger reconciliation (SI-DQA-002/003, SI-PINN-002), FUT-01 handoff — Phase 29 (VER-07/09/11/12).
- M16 collocation scaling, G6 causal training, training-loop usage of validation metrics — doc-03 milestone (SCOPE-11), each with a recorded forward-reference.
- DataLoader/TrajectoryValidator/TrajectoryIndex implementation — FUT-01.
- OI-3 calibration constants (SASD 0.5, IPR 1e-3, PSC grid, n_pts_cap=32) — owned by Phases 27/28 adjudication, not Phase 26.

</deferred>

---

*Phase: 26-DataLoader Ingestion and Selection Contracts*
*Context gathered: 2026-06-12*
