# Requirements: Three-Body Physics-Informed LLM v1.5

**Defined:** 2026-06-10
**Core Value:** The simulation dataset and data pipeline must be clean, well-validated, and correctly processed; the data-pipeline/validation design contracts must be verified against the actual dataset before implementation work depends on them.

**Current workflow state:** v1.4 shipped 2026-06-09 and is merged to master. v1.5 runs on branch `milestone/v1.5` and targets `pinn_instruction/issues/02-data-pipeline-and-validation.md`.

## Source treatment policy

The issue doc (`pinn_instruction/issues/02-data-pipeline-and-validation.md`) is **NOT authoritative** — it may contain errors (known seed: ratio-based SCS thresholds conflicting with the locked post-v1.3 gate). Every finding is verified before any fix is applied.

**No resolution doc existed at milestone start.** The user produces one via external multi-AI research, working from an agent-prepared research package (PKG-01..03). The resulting doc — expected under `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/` — becomes the **candidate verdict source** with the same standing `ctl_pinn_resolution.md` had in v1.4: default verdict source, transcribed unless evidence shows a position fails, never authoritative. Adjudication phases gate on its arrival.

**Live code in `pinn/` is NOT grounding** (directive 2026-05-19, persists in v1.5). Issue 02's "Canonical" citation of `pinn/data-processing-pipeline-full.py` is overridden. The on-disk dataset and `simulation_data/Scripts/` ARE grounding for v1.5 (SCOPE-06/07).

**STOP protocol applies in full** (AGENTS.md "CRITICAL GOVERNANCE"): source-silent decisions are surfaced as gaps in phase-local `NN-GAPS.md` registers and the milestone index `.planning/milestones/v1.5-GAPS.md`; nothing is invented.

## v1.5 Requirements

### Research Package and External Resolution

- [x] **PKG-01**: The research package delivers a complete annotated document list for the user's external research agent — every document needed to adjudicate the issue-02 findings, each with a role annotation. If the list would exceed ~5 files or the necessary context is scattered across fragments, the fragments are consolidated into a single context file (framework specs are passed intact, never consolidated) and the consolidation is surfaced to the user before assembly.
- [x] **PKG-02**: The package frames the research questions: each contested or unverified finding is posed as an explicit question, with locked v1.4 conventions listed as hard constraints the research must respect (14D input contract, Jacobi IC₁₃, mass-weighted COM projection head, the PHYS-03 softening outcome, the post-v1.3 SCS gate `\epsilon_H > 10^{-5}` / `SCS > -5`, the PHYS-01 D convention) and the doc-03 scope boundary stated.
- [x] **PKG-03**: The package presents dataset figures as explicitly-marked **"claimed, unverified"** issue-doc values wherever empirical verification has not yet run — the package phase precedes verification by user decision 2026-06-10 (urgency of starting the external research, which gates everything downstream). A figure already verified by a prior grounded source may be stated as verified with its citation. No unverified figure is presented as fact. The post-verification correction addendum is DATA-07.
- [x] **PKG-04**: `data_quality_assessment.md` is characterized read-only — its provenance, content map, and relation to the (not-yet-performed) dataset ↔ framework compatibility verification — and the characterization is reported to the user. No edits to the file.

### Empirical Dataset Verification

- [ ] **DATA-01**: ID-gap claims are verified against the on-disk dataset (claimed: 1,250 gaps / 4,000 standard quasi-random; 143 / 5,000 hierarchical), with recorded counts and the counting method.
- [ ] **DATA-02**: The blacklist is verified — `problematic_ics_blacklist.json` located, the 65-ID claim confirmed or corrected, and its current consumption status recorded (within grounding limits: `simulation_data/Scripts/` runners are grounding; `pinn/` is not).
- [ ] **DATA-03**: The gold-counterpart gap is verified — the 184-standard-IDs-without-gold claim, the 2,565 vs 2,749 folder counts, cross-checked against `simulation_data/Documentation/standard_quasi_random_ids_not_in_gold.md`.
- [ ] **DATA-04**: Footer-schema variance is verified — minimal footers (claimed 219 standard gold files), `eta`/`tol` omissions, folder-default tolerance values, OS-dependent footer paths.
- [ ] **DATA-05**: The mass-drift probe is executed — `m_IC` vs `m_Brutus(t=0)` compared with `np.allclose(rtol=1e-15)` on a documented sample; the verdict (IC masses canonical vs `decimal.Decimal` parsing required) is recorded and feeds PIPE-07.
- [ ] **DATA-06**: Snapshot-count and `dt_out` distributions are verified per dataset variant (claimed ~59 / ~125 / ~1000 snapshots; `final_timestep >= 9.5` prevalence) — recorded as distributions, not single examples; feeds PIPE-04.
- [ ] **DATA-07**: After the DATA-01..06 probes complete, every package-stated dataset claim that verification contradicted is compiled into a correction addendum delivered to the user for forwarding to the in-flight external research; if no claim is contradicted, a nil addendum records that all package-stated claims were confirmed. Verification runs in parallel with the user's external research — the addendum ships as soon as the probes finish, not after the resolution doc lands.

### Adjudication (continuing v1.4 EVID numbering)

- [x] **EVID-06**: For each issue-02 finding selected for remediation, the agent records direct evidence — issue-doc citation, resolution-doc verdict (once landed), current framework-spec evidence, and dataset evidence (DATA-xx) — before editing. Evidence packets cite line ranges, not whole files.
- [x] **EVID-07**: Each finding receives an explicit verdict from the fixed set — `accept-resolution`, `accept-issue-doc`, `accept-third-position`, `reject-both-as-unsupported`, or `defer-with-blocker` — with reasoning recorded in the evidence packet.
- [x] **EVID-08**: False positives in either source are documented as intentional non-changes, including why the current convention remains valid and which source(s) misread it.
- [x] **EVID-09**: Every accepted finding has a before/after evidence note naming the changed spec section, the contract it now enforces, and the verification step that confirms the fix.
- [x] **EVID-10**: When sources conflict — issue doc vs resolution doc vs v1.4-locked conventions vs dataset evidence — the agent performs root-cause adjudication: reads all positions in full, verifies each against specs, dataset, and first principles, names the root-cause ambiguity, locks the convention, and records which source was right, which wrong, and why. Known seed conflicts: ratio-based SCS thresholds (`SCS > 1e-6` / `< 1e-8`) vs the locked log-based gate; `compute_globals` `D = 6.694` vs the v1.4 PHYS-01 D convention; the M11/M12 severity reclassifications.

### Pipeline and DataLoader Contracts (spec-side; FUT-01 implements)

- [ ] **PIPE-01**: Framework specs define the Stage 4→5 trajectory-validation gate contract (B-06): final-timestamp threshold, stage-dependent snapshot minimums, and rejection logging — as a DataLoader design contract.
- [ ] **PIPE-02**: Framework specs define the ID-resolution contract (B-11): `id_to_path` mapping built from the filesystem scan, with the explicit invariant that trajectory ID is never assumed equal to array index.
- [x] **PIPE-03**: Framework specs define the blacklist-exclusion contract (M11): load at DataLoader init, exclude, log the exclusion count, fail loudly if a blacklisted ID reaches a batch.
- [ ] **PIPE-04**: Framework specs define the points-per-trajectory contract (M12): an adjudicated sampling-feasibility rule (candidate: `n_pts = min(32, int(0.5 * n_snapshots))`) consistent with the verified snapshot distributions from DATA-06.
- [ ] **PIPE-05**: Framework specs define the gold-counterpart contract (M13): Stage-5 gold-existence check plus the fallback policy (skip to Stage 6 vs flagged low-fidelity fallback). If the sources are silent or conflicting on the fallback choice, it is surfaced as a gap for user decision, not invented.
- [x] **PIPE-06**: Framework specs define the footer/parameter-heterogeneity contract (D7): `Result:` footer precedence, folder-default fallback, `tol_confidence` flag (`direct` vs `inferred`), and footer-as-metadata-only (completeness gate never depends on footer presence).
- [ ] **PIPE-07**: Framework specs define the precision contract: float64 sufficiency rationale for validation metrics and the Decimal-for-masses policy, grounded in the DATA-05 verdict.
- [ ] **PIPE-08**: Framework specs define the data-side dt_out and stage-query contract: the DataLoader exposes per-trajectory `dt_out` metadata and the `sample_replay(n, max_stage)` / `sample_lookahead(n, stage)` interface. The collocation-scaling policy that consumes this metadata (M16) stays with the doc-03 milestone.
- [ ] **PIPE-09**: Framework specs define the global-scale computation contract (`compute_globals`): consistent with the v1.4-locked PHYS-01 D convention; the issue-02 claim that scales must be recomputed with `D = 6.694` is adjudicated (verified, corrected, or rejected) rather than transcribed.
- [x] **PIPE-10**: The training-data format decision (D-03: HDF5 vs .npy vs txt/json) is presented to the user with verified evidence; the user decides; the locked choice is recorded in the framework specs.

### Validation-Metrics Contracts

- [ ] **VAL-01**: Framework specs carry one canonical SCS contract — definition and threshold adjudicated against the locked post-v1.3 gate (`\epsilon_H > 10^{-5}` / `SCS > -5`); the issue-02 ratio-based thresholds are resolved through EVID-10, not transcribed.
- [ ] **VAL-02**: Framework specs define SASD — formula, data-side computation contract, and the low-resolution floor-effect caveat. Training-side collocation weighting is deferred to the doc-03 milestone with a recorded forward-reference.
- [ ] **VAL-03**: Framework specs define IPR — formula and dual-epsilon consistency with the v1.4 PHYS-03 outcome; its ALM noise-floor role is recorded as a doc-03 forward-reference.
- [ ] **VAL-04**: Framework specs define PSC — formula and data-side computation contract; replay-governance use is deferred to the doc-03 milestone with a recorded forward-reference.

### Verification and Handoff (continuing v1.4 VER numbering)

- [ ] **VER-07**: Every v1.5 contract has a numerically-defined acceptance check naming its pass criterion, the data it runs on, and the command or function that executes it — not just prose.
- [ ] **VER-08**: The roadmap maps every v1.5 requirement to exactly one phase, beginning at Phase 23.
- [ ] **VER-09**: The acceptance checks are **executed** using disposable probes (dataset probes and spec-consistency probes), each producing recorded pass/fail evidence. A failing check blocks phase completion and routes back to the originating phase; v1.5 does not ship while any required check fails. Probes test the specs and the dataset — they never touch `pinn/` production code.
- [x] **VER-10**: Every fix closes through the iterative re-verification loop: the issue ledger tracks each finding through `PENDING → IN_PROGRESS → FIX_APPLIED → VERIFIED`; after each batch of edits, previously `VERIFIED` findings that the batch could have regressed are re-verified and demoted on regression. The ledger lives at a stable path under the empirical-dataset-verification phase directory; nothing closes until all in-scope findings are `VERIFIED` or explicitly `DEFERRED` with a written blocker.
- [ ] **VER-11**: The milestone handoff identifies which findings were fixed, which were intentionally left unchanged, and which were deferred; FUT-01 divergence records are updated for every DataLoader-implementation-shaped finding.
- [ ] **VER-12**: The remaining framework-spec Source-Issue entries (`SI-DQA-002`, `SI-DQA-003`, `SI-PINN-002`) are reviewed for issue-02 relevance — each retired with a back-reference to the resolving phase/commit or preserved with a written reason. None is assumed resolved or assumed irrelevant.

## Future Requirements

Unchanged from v1.4 (see `.planning/milestones/v1.4-REQUIREMENTS.md` for full text):

- **FUT-01**: Rebuild `pinn/` implementation code from the settled framework specs (now including v1.5 data-pipeline contracts).
- **FUT-02**: Recompute curriculum statistics and stage thresholds after preprocessing and physics contracts are finalized.
- **FUT-03**: Package useful disposable validation probes into reusable scripts under `pinn/validation/`.
- **FUT-04**: Resume PINN training-loop implementation after the framework specs are coherent.
- **FUT-05**: Adjudicate the author comments preserved by v1.4 Phase 22 (`22-COMMENT-HANDOFF.md`).

## Cross-Project Documentation Requirements

- **REQ-DOC-01** (cross-project): Markdown framework specs are the authoritative design documents during active work; LaTeX sources are publication/archive derivatives synced only at the final publication stage. (Full text in `.planning/milestones/v1.4-REQUIREMENTS.md`.)

## Scope Boundaries

| Scope | Status |
|-------|--------|
| **SCOPE-06** On-disk dataset as grounding | **In scope as grounding** — the actual `simulation_data/` dataset files are a permitted evidence source for v1.5: empirical facts (file counts, ID gaps, footers, blacklist contents, snapshot distributions) are verified by direct observation. Probe outputs are recorded with method and command so claims are re-derivable. |
| **SCOPE-07** `simulation_data/Scripts/` carveout extension | **In scope as grounding** — extends the v1.4 SCOPE-05 carveout beyond `ic_generation/` to `metrics_calculation/`, `Validation/prescreening/`, and `brutus_runners/`. These scripts generated the fixed dataset and are provenance for data-pipeline specs. This remains a carveout from the `pinn/` no-live-code directive, not a general live-code exception. |
| **SCOPE-08** `sampling_method.md` | **Frozen by default** (user directive 2026-06-10) — it is the completed instruction file for the finished `simulation_data/` generation and is not an active design-revision target. It may be revised ONLY on explicit user instruction triggered by verified data-feasibility issues. Recorded in AGENTS.md Source of Truth and PROJECT.md Key Decisions. |
| **SCOPE-09** `data_quality_assessment.md` | **Read-only in v1.5** — characterized and reported (PKG-04), never edited. It is a research report in `framework-revisions/`, not an authoritative spec. |
| **SCOPE-10** `pinn/` live code | **Out of scope and NOT grounding** — the 2026-05-19 directive persists. Issue 02's "Canonical" citation of `pinn/data-processing-pipeline-full.py` is overridden. Live-code references permitted only in forward-pointing FUT-01 hand-off documents. |
| **SCOPE-11** Doc-03 boundary | **Data-side only** — v1.5 settles the DataLoader-facing contracts (dt_out metadata exposure, stage/replay query interface, metric definitions and data-side computation). M16 collocation-scaling policy, G6 causal-training, and training-loop usage of SCS/SASD/IPR/PSC stay with the future doc-03 milestone, each with a recorded forward-reference. |

## Out of Scope

| Feature | Reason |
|---------|--------|
| Brutus integrator changes | Issue 02 concerns the pipeline between Brutus output and training input, not the validated C++ integrator. |
| DataLoader / TrajectoryValidator / TrajectoryIndex implementation | v1.5 settles design contracts; implementation is FUT-01. |
| M16 collocation-scaling policy and G6 causal-training decision | Canonically owned by `03-curriculum-and-training-loop.md`; deferred to the doc-03 milestone (SCOPE-11). |
| LLM fine-tuning prep | Deferred until framework and data contracts are stable. |
| Data regeneration | Only via explicit user directive after verified data-feasibility findings; not assumed by any v1.5 fix. |
| Editing `sampling_method.md` or `data_quality_assessment.md` | SCOPE-08 / SCOPE-09. |

## Traceability

Filled by roadmap creation, revised by roadmap revision (`.planning/ROADMAP.md`, 2026-06-10 phase-order swap; 2026-06-11 Phase 24.5 insertion). Every v1.5 requirement maps to exactly one phase (satisfies VER-08). Phase 23 (research package) is first and ungated; Phase 24 (verification + DATA-07 addendum) runs in parallel with the external-research gate window and gates on nothing external. Phase 24.5 (INSERTED, resolution doc readiness verification) gates on the consolidated resolution doc landing and Phase 24 completion. Phases 25–29 gate on Phase 24.5 passing.

| Requirement | Phase | Status |
|-------------|-------|--------|
| PKG-01 | Phase 23 | Complete |
| PKG-02 | Phase 23 | Complete |
| PKG-03 | Phase 23 | Complete |
| PKG-04 | Phase 23 | Complete |
| DATA-01 | Phase 24 | Complete (2026-06-11) |
| DATA-02 | Phase 24 | Complete (2026-06-11) |
| DATA-03 | Phase 24 | Complete (2026-06-11) |
| DATA-04 | Phase 24 | Complete (2026-06-11) |
| DATA-05 | Phase 24 | Complete (2026-06-11; GAP-24-01 RESOLVED-WITH-INSTRUCTION) |
| DATA-06 | Phase 24 | Complete (2026-06-11) |
| DATA-07 | Phase 24 | Complete (2026-06-11) |
| EVID-06 | Phase 25 | Pending (gated on Phase 24.5) |
| EVID-07 | Phase 25 | Pending (gated on Phase 24.5) |
| EVID-08 | Phase 25 | Pending (gated on Phase 24.5) |
| EVID-09 | Phase 25 | Pending (gated on Phase 24.5) |
| EVID-10 | Phase 25 | Pending (gated on Phase 24.5) |
| VER-10 | Phase 25 | Pending (gated on Phase 24.5) |
| PIPE-01 | Phase 26 | Pending (gated on Phase 24.5) |
| PIPE-02 | Phase 26 | Pending (gated on Phase 24.5) |
| PIPE-03 | Phase 26 | Pending (gated on Phase 24.5) |
| PIPE-05 | Phase 26 | Pending (gated on Phase 24.5) |
| PIPE-06 | Phase 26 | Pending (gated on Phase 24.5) |
| PIPE-10 | Phase 26 | Pending (gated on Phase 24.5) |
| PIPE-04 | Phase 27 | Pending (gated on Phase 24.5) |
| PIPE-07 | Phase 27 | Pending (gated on Phase 24.5) |
| PIPE-08 | Phase 27 | Pending (gated on Phase 24.5) |
| PIPE-09 | Phase 27 | Pending (gated on Phase 24.5) |
| VAL-01 | Phase 28 | Pending (gated on Phase 24.5) |
| VAL-02 | Phase 28 | Pending (gated on Phase 24.5) |
| VAL-03 | Phase 28 | Pending (gated on Phase 24.5) |
| VAL-04 | Phase 28 | Pending (gated on Phase 24.5) |
| VER-07 | Phase 29 | Pending (gated on Phase 24.5) |
| VER-08 | Phase 29 | Satisfied by roadmap creation; confirmed at closure |
| VER-09 | Phase 29 | Pending (gated on Phase 24.5) |
| VER-11 | Phase 29 | Pending (gated on Phase 24.5) |
| VER-12 | Phase 29 | Pending (gated on Phase 24.5) |

**Coverage:**

- v1.5 requirements: 36 total (4 PKG + 7 DATA + 5 EVID + 10 PIPE + 4 VAL + 6 VER)
- Mapped to phases: 36/36 (phase-order swap 2026-06-10: research package first (Phase 23, PKG-01..04), verification + DATA-07 correction addendum second (Phase 24, DATA-01..07, runs in parallel with the external-research gate window))
- Phase distribution: Phase 23 = 4 (PKG-01..04); Phase 24 = 7 (DATA-01..07); Phase 24.5 = 0 (operational readiness check, no requirement IDs); Phase 25 = 6 (EVID-06..10, VER-10); Phase 26 = 6 (PIPE-01, 02, 03, 05, 06, 10); Phase 27 = 4 (PIPE-04, 07, 08, 09); Phase 28 = 4 (VAL-01..04); Phase 29 = 5 (VER-07, 08, 09, 11, 12)
- No orphans, no duplicates: every requirement appears in exactly one phase.
- Cross-project requirements: REQ-DOC-01 (not counted in v1.5 total)
- SCOPE-06 through SCOPE-11 are scope-boundary annotations, not numbered requirements.

---
*Requirements defined: 2026-06-10; traceability filled 2026-06-10 by roadmap creation; revised 2026-06-10 (phase-order swap, DATA-07 mapped); revised 2026-06-11 (Phase 24.5 insertion — gating updated from "resolution doc + Phase 24" to "Phase 24.5").*
