# Roadmap: 3-Body Problem Physics-Inspired LLM

## Milestones

- ✅ **v1.0 Codebase Cleanup** — Phases 1–4 (shipped 2026-03-20; [archive](milestones/v1.0-ROADMAP.md))
- ✅ **v1.1 LaTeX Modularization Verification** — Phases 5–8 (shipped 2026-03-22)
- ✅ **v1.2 PINN Implementation Readiness** — Phase 9 (shipped 2026-05-08)
- ✅ **v1.3 Markdown Conversion Verification & Correction** — Phases 10–15, 15.1 (shipped 2026-05-08; [archive](milestones/v1.3-ROADMAP.md))
- ✅ **v1.4 Resolving 01 Architecture and Physics Foundations** — Phases 16–22, including 20.5 (shipped 2026-06-09; [roadmap archive](milestones/v1.4-ROADMAP.md), [requirements archive](milestones/v1.4-REQUIREMENTS.md), [phase archive](milestones/v1.4-phases/))
- 🚧 **v1.5 Resolving 02 Data Pipeline and Validation** — Phases 23–29 (in progress; planning)
- 🔮 **Final Publication LaTeX Sync** — deferred until implementation, network/training design, training, and research-result interpretation are complete

## Deferred: Final Publication LaTeX Sync

**Goal:** Refresh LaTeX/PDF publication sources from the final authoritative markdown framework specs.

**Preconditions:**

- Implementation complete (FUT-01 or successor milestone)
- Network design stable
- Training and research results complete
- No active framework-spec iteration expected

**Non-goal:** Maintaining `.tex` parity during active development milestones.

**Source of truth:** Markdown framework specs (`pinn_instruction/markdown_conversion/framework-specs/*.md`) at final sync start.

**Historical note:** This supersedes the earlier draft `v1.6.5-latex-sync` timing from the May 24, 2026 design document.

---

## 🚧 v1.5 Resolving 02 Data Pipeline and Validation (Planning)

**Milestone Goal:** Critically examine each finding in `pinn_instruction/issues/02-data-pipeline-and-validation.md` — treating the issue doc as non-authoritative — verify every claim empirically against the on-disk dataset, the `simulation_data/` scripts that generated it, the v1.4-revised framework specs, and first principles; adjudicate against the user-produced external resolution doc once it lands; apply evidence-backed edits limited to `ctl_instruction.md` and `pinn_architecture.md`; and verify each fix with disposable acceptance probes before closing. v1.5 settles the data-pipeline/validation design contracts; it does **not** implement production DataLoader/training code (that remains FUT-01).

**Granularity:** standard
**Coverage:** 36/36 v1.5 requirements mapped (Phases 23–29)
**Branch:** `milestone/v1.5` (cut from master HEAD `b8b39a4`); tag `v1.5-pre-phase-NN` from branch HEAD before each phase; one atomic commit per plan via `scripts/agent-commit`; `--no-ff` merge to master at milestone end.

### Source treatment & STOP protocol (applies to every phase)

- **Neither source is authoritative.** The issue doc (`02-data-pipeline-and-validation.md`) may contain errors (known seed: ratio-based SCS thresholds conflicting with the locked post-v1.3 gate). The forthcoming resolution doc is the **candidate verdict source** — same standing `ctl_pinn_resolution.md` had in v1.4 — transcribed unless evidence shows a position fails, never authoritative.
- **Grounding for v1.5:** the on-disk `simulation_data/` dataset (SCOPE-06), `simulation_data/Scripts/` (SCOPE-07: `metrics_calculation/`, `Validation/prescreening/`, `brutus_runners/`, `ic_generation/`), the v1.4-revised framework specs, prior user decisions, and short first-principles derivations. **`pinn/` live code is NOT grounding** (SCOPE-10) — issue 02's "Canonical" citation of `data-processing-pipeline-full.py` is overridden; live-code references stay confined to forward-pointing FUT-01 hand-off documents.
- **Frozen / read-only spec targets:** edits land in `ctl_instruction.md` and `pinn_architecture.md` ONLY. `sampling_method.md` is frozen by default (SCOPE-08); `data_quality_assessment.md` is read-only and only characterized (SCOPE-09).
- **STOP protocol in full** (AGENTS.md "CRITICAL GOVERNANCE"): source-silent semantic / process-schema / cross-phase decisions are surfaced as gaps in phase-local `NN-GAPS.md` registers and the milestone index `.planning/milestones/v1.5-GAPS.md`; nothing is invented where sources are silent.
- **Doc-03 boundary** (SCOPE-11): v1.5 settles data-side contracts only. M16 collocation-scaling, G6 causal-training, and training-loop usage of SCS/SASD/IPR/PSC stay with the future doc-03 milestone, each with a recorded forward-reference.

### Verification protocol (applies to every adjudication phase, 25–29)

Every selected finding follows the v1.4-style loop:

1. **Adjudicate** — record an evidence packet (issue-doc citation, resolution-doc verdict, current framework-spec evidence, DATA-xx dataset evidence) and an explicit verdict from `{accept-resolution, accept-issue-doc, accept-third-position, reject-both-as-unsupported, defer-with-blocker}`. Where sources conflict, perform root-cause adjudication (EVID-10) before editing.
2. **Fix** — apply the framework-spec edit to `ctl_instruction.md` / `pinn_architecture.md` only.
3. **Verify** — run the finding's numerically-defined acceptance check via a disposable probe (dataset probe or spec-consistency probe); probes never touch `pinn/`.
4. **Re-verify after every batch** — re-run the acceptance check on every previously `VERIFIED` finding the new batch could have regressed; any regression reverts that finding to `IN_PROGRESS`.
5. **Ledger discipline** — each finding moves `PENDING → IN_PROGRESS → FIX_APPLIED → VERIFIED` (or `DEFERRED` with a written blocker) in the issue ledger held at a stable path under the Phase 24 (empirical-dataset-verification) directory. "Fix applied" is **not** closure; "the acceptance check passed" is. No phase exits with an in-scope finding still open.

## Phases

**Phase Numbering:**

- Integer phases (23, 24, …): planned v1.5 work, continuing from v1.4's Phase 22.
- Decimal phases (e.g., 24.5): inserted checkpoints or urgent insertions (marked INSERTED), placed between their surrounding integers.

- [x] **Phase 23: Research Package Assembly** — Assemble the annotated document list and framed research questions (dataset figures marked "claimed, unverified"), plus a read-only DQA characterization, then hand off for the user's external multi-AI research. First v1.5 phase; its delivery opens the external gate. (completed 2026-06-10; research context consolidated to single master file on 2026-06-11)

> ⛔ **External gate — resolution doc.** On Phase 23 delivery, the **USER** begins external multi-AI research and delivers the resolution doc to `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/`. The gate opens here, when package delivery starts the user's research. **Phase 24 runs in parallel during the gate window** (it gates on nothing external). **Phase 24.5** (INSERTED) verifies the consolidated resolution doc is ready before adjudication begins. Phases 25–29 (all adjudication and spec-edit work) **cannot start** until Phase 24.5 passes (which requires BOTH the consolidated doc landing AND Phase 24 completion). The doc is the candidate verdict source, not authoritative.

- [x] **Phase 24: Empirical Dataset Verification and Correction Addendum** — Verify every empirical issue-02 claim against the on-disk dataset and compile the DATA-07 correction addendum for the in-flight external research; runs in parallel with the user's research (gates on nothing external) and seeds the issue ledger. (completed 2026-06-11)

- [x] **Phase 24.5: Resolution Doc Readiness Verification** (INSERTED) — COMPLETE 2026-06-11, READY-WITH-CAVEATS. Verified the consolidated resolution doc is structurally sound, covers all 19 issue-02 findings (0 silent), is consistent with Phase 24 verified facts (0 contradictions), and respects v1.4-locked conventions (0 violations). Produced `24.5-READINESS-REPORT.md` and `24.5-RESOLUTION-MAP.md`. No fix package routed (no blocking gap; optional OI-12 addendum erratum noted). Phases 25–29 unblocked.

- [ ] **Phase 25: Evidence Framework and Issue Ledger** — Stand up the adjudication machinery (evidence packets, verdict set, false-positive/before-after notes, root-cause conflict adjudication) and the re-verification ledger before any spec edit.
- [ ] **Phase 26: DataLoader Ingestion and Selection Contracts** — Lock the ingestion gate, ID-resolution, blacklist-exclusion, gold-counterpart, footer-heterogeneity, and training-data-format contracts.
- [ ] **Phase 27: Sampling, Precision, and Global-Scale Contracts** — Lock the points-per-trajectory, precision/Decimal, dt_out/stage-query metadata, and `compute_globals` global-scale contracts.
- [ ] **Phase 28: Validation-Metrics Contracts** — Define one canonical data-side contract each for SCS, SASD, IPR, and PSC, threshold-aligned to the locked gate and v1.4 physics outcomes.
- [ ] **Phase 29: Acceptance Checks, Re-verification, and Handoff** — Execute every contract's acceptance check, close the ledger, reconcile the SI-ledger, and produce the FUT-01 handoff.

## Phase Details

### Phase 23: Research Package Assembly

**Goal**: Deliver a complete, framed research package — annotated document list, framed questions, and a read-only DQA characterization — ready for the user's external multi-AI research; on delivery, the milestone enters the external resolution-doc gate. The package is the milestone critical path (user decision 2026-06-10: starting the external research gates all downstream adjudication), so it precedes empirical verification and presents dataset figures as issue-doc values explicitly marked "claimed, unverified".
**Depends on**: Nothing (first v1.5 phase; runs on `milestone/v1.5`). No external gate; no dependency on verification.
**Requirements**: PKG-01, PKG-02, PKG-03, PKG-04
**Success Criteria** (what must be TRUE):

  1. The package includes a complete annotated document list — every document needed to adjudicate the issue-02 findings, each with a role annotation; if the list would exceed ~5 files or context is scattered, fragments are consolidated into a single context file (framework specs passed intact, never consolidated) and the consolidation is surfaced to the user before assembly. The PKG-04 DQA characterization directly informs which documents the list includes.
  2. Each contested or unverified finding is posed as an explicit research question, with the locked v1.4 conventions listed as hard constraints (14D input contract, Jacobi IC₁₃, mass-weighted COM projection head, the PHYS-03 softening outcome, the post-v1.3 SCS gate `ε_H > 10⁻⁵` / `SCS > −5`, the PHYS-01 D convention) and the doc-03 scope boundary stated.
  3. Every dataset figure stated in the package is explicitly marked "claimed, unverified" (the issue-doc value), unless a prior grounded source already verified it (then stated as verified with its citation); no unverified figure is presented as fact. The Phase 24 verification and its DATA-07 correction addendum follow up after the package ships (PKG-03).
  4. `data_quality_assessment.md` is characterized read-only (provenance, content map, and its relation to the not-yet-performed dataset↔framework compatibility verification), reported to the user with zero edits to the file, and the characterization informs the document-list decision (PKG-04).
  5. The package is handed to the user, and the milestone records that the external resolution-doc gate is now open (user research starts) and that adjudication Phases 25–29 gate on BOTH the resolution doc landing under `framework-revisions/research_reports/02-data-pipeline-and-validation/` AND Phase 24 completion.**Plans**: 5 plans (Wave 1: 23-01 analysis; Wave 2: 23-02 D-07 consolidation checkpoint [user gate]; Wave 3: 23-03 package snapshots + claims table + consolidated context; Wave 4: 23-04 framed questions; Wave 5: 23-05 manifest + delivery + gate-open)

**Wave 1**

  - [x] 23-01-PLAN.md — DQA characterization (PKG-04) + CLM claims register (PKG-03) + consolidation plan

**Wave 2** *(blocked on Wave 1 completion)*

  - [x] 23-02-PLAN.md — D-07 consolidation & inclusion checkpoint (PKG-01; user gate, autonomous: false)

**Wave 3** *(blocked on Wave 2 completion)*

  - [x] 23-03-PLAN.md — package dir + byte-for-byte snapshots + claims table + consolidated context (PKG-01)

**Wave 4** *(blocked on Wave 3 completion)*

  - [x] 23-04-PLAN.md — framed research questions (PKG-02)

**Wave 5** *(blocked on Wave 4 completion)*

  - [x] 23-05-PLAN.md — manifest + delivery note + STATE.md gate-open (PKG-01)

### Phase 24: Empirical Dataset Verification and Correction Addendum

**Goal**: Establish verified, re-derivable dataset facts by checking every package-stated ("claimed, unverified") issue-02 figure against the on-disk dataset, and compile a correction addendum for any contradicted claim — delivered to the user for forwarding to the in-flight external research. Seeds the issue ledger that downstream adjudication consumes.
**Depends on**: Phase 23 (consumes the delivered package's claim list to know what to verify against). **NOT gated on the external resolution doc** — this phase runs during the gate window, in parallel with the user's external research; it gates on nothing external.
**Requirements**: DATA-01, DATA-02, DATA-03, DATA-04, DATA-05, DATA-06, DATA-07
**Success Criteria** (what must be TRUE):

  1. The ID-gap, blacklist, gold-counterpart, footer-variance, and snapshot/`dt_out` claims are each recorded with observed counts plus the probe command/method, and each marked confirmed / corrected / unverified against the issue-02 figures (claimed: 1,250/4,000 standard and 143/5,000 hierarchical ID gaps; 65 blacklist IDs; 184 standard IDs without gold and 2,565 vs 2,749 folders; 219 minimal standard-gold footers; ~59/~125/~1000 snapshots).
  2. The mass-drift probe verdict — IC masses canonical vs `decimal.Decimal` parsing required — is recorded from a documented `np.allclose(rtol=1e-15)` run on a stated sample and is available to feed the precision contract (PIPE-07).
  3. Every recorded fact is re-derivable: the exact probe command and dataset path are captured alongside each count so the user or a later probe can reproduce it; no fact is sourced from an unverified issue-doc claim.
  4. Every package-stated claim that verification contradicts is compiled into a correction addendum delivered to the user for forwarding to the in-flight external research; if nothing is contradicted, a nil addendum records that all package-stated claims were confirmed. The addendum ships as soon as the probes finish — not after the resolution doc lands (DATA-07).
  5. The verified facts and the enumerated issue-02 finding inventory are captured at the issue ledger's stable path under this (Phase 24, empirical-dataset-verification) phase directory, which the Phase 25 adjudication ledger consumes.

**Plans**: 4 plans (Wave 1: 24-01 filesystem/ID probes DATA-01/02/03 + register init ‖ 24-04 WR-01..04 user gate [autonomous: false]; Wave 2: 24-02 content probes DATA-04/05/06 + register completion; Wave 3: 24-03 DATA-07 addendum + issue-ledger seed)

**Wave 1**

  - [x] 24-01-PLAN.md — DATA-01 ID-gap / DATA-02 blacklist / DATA-03 gold-gap probes + verified-facts register init (read-only; D-13 nominal-range STOP-gap branch) — `0ca0e2d6`, 24-01-SUMMARY.md
  - [x] 24-04-PLAN.md — WR-01..04 carry-in user gate (DATA-07; surfaces the four OPEN decisions, autonomous: false; never decides them) — `d260701a`, 24-04-SUMMARY.md (all four RESOLVED-WITH-INSTRUCTION)

**Wave 2** *(blocked on Wave 1 — 24-02 shares the verified-facts register with 24-01)*

  - [x] 24-02-PLAN.md — DATA-04 footers / DATA-05 mass-drift (np.allclose rtol=1e-15, .venv) / DATA-06 snapshot distributions + register completion (D-16 mass-baseline STOP-gap branch; D-06 prose sweep CLM-14+) — `b1c948ee`, 24-02-SUMMARY.md (GAP-24-01 fired then RESOLVED-WITH-INSTRUCTION)

**Wave 3** *(blocked on Wave 2 register completion AND Wave 1 24-04 WR answers)*

  - [x] 24-03-PLAN.md — DATA-07 correction addendum (byte-stable sibling; supersedes erratum) + 24-ISSUE-LEDGER.md seed (full inventory PENDING; v1.4 schema) — `4b9143b5`, 24-03-SUMMARY.md

**Phase 24 status**: COMPLETE (2026-06-11) — 4/4 plans summarized; 24-UAT.md passed 12/12; GAP-24-01 RESOLVED-WITH-INSTRUCTION (DATA-05 rerun remediation executed + validated separately). Gates nothing external; Phases 25–29 gate on Phase 24.5 (which verifies the consolidated resolution doc).

### Phase 24.5: Resolution Doc Readiness Verification (INSERTED)

**Goal**: Verify the consolidated resolution doc (from the user's external research) is ready for use as the candidate verdict source in Phases 25–29. Produce a readiness report with pass/fail per check and fix instructions for any gaps, plus a quick-reference map so downstream phases know where the resolution doc is, what each section covers, and how to cite it.
**Depends on**: Phase 24 (verified dataset facts + seeded issue ledger) **and the consolidated resolution doc landing** (external gate). Cannot start until BOTH are present.
**Requirements**: Operational (supports EVID-06..10, PIPE-01..10, VAL-01..04, VER-07..12); no new requirement IDs.
**Success Criteria** (what must be TRUE):

  1. Every finding in the 19-row issue ledger (`24-ISSUE-LEDGER.md`) maps to a resolution doc section (covered or partial; silent entries are flagged as gaps).
  2. The verified-facts register (`24-VERIFIED-FACTS.md`) shows no unexplained contradictions between the resolution doc and verified dataset facts.
  3. The v1.4-locked convention check identifies zero violations (scope observations — recommendations to change a locked convention — are recorded but are not failures).
  4. A resolution-doc quick-reference map exists providing enough information for Phase 25 to start evidence-packet construction without reading the full resolution doc first.
  5. If any check fails, specific fix instructions are routed to the external consolidation agent via the readiness report, and Phase 25 remains blocked until the fix lands and re-check passes.

**Plans**: 1 plan (24.5-01 readiness verification; single wave, lightweight)

  - [x] 24.5-01-PLAN.md — presence/structure check + finding-coverage crosswalk + DATA-xx consistency + v1.4-locked convention compliance + resolution-doc map + readiness report + gate decision (executed 2026-06-11; all 7 tasks complete)

**Phase 24.5 status**: COMPLETE (2026-06-11) — 1/1 plan summarized; gate verdict READY-WITH-CAVEATS (all 4 checks pass, 0 blocking gaps; caveats OI-3/6/7/8/11/12 deferred by design). Phases 25–29 unblocked.

### Phase 25: Evidence Framework and Issue Ledger

**Goal**: The adjudication machinery — evidence packets, verdict set, false-positive and before/after notes, root-cause conflict adjudication, and the re-verification ledger — is established, and the known cross-source conflicts are adjudicated at root cause before any spec edit lands.
**Depends on**: Phase 24.5 (resolution doc readiness verification). Phase 24.5 gates on BOTH the consolidated resolution doc landing AND Phase 24 completion; Phase 25 cannot start until Phase 24.5 passes.
**Requirements**: EVID-06, EVID-07, EVID-08, EVID-09, EVID-10, VER-10
**Success Criteria** (what must be TRUE):

  1. Each issue-02 finding selected for remediation has an evidence packet citing line ranges (never whole files) from the issue doc, the resolution-doc verdict, current framework-spec evidence, and the DATA-xx dataset evidence from Phase 24.
  2. Every selected finding carries an explicit verdict from the fixed set — `accept-resolution`, `accept-issue-doc`, `accept-third-position`, `reject-both-as-unsupported`, or `defer-with-blocker` — with recorded reasoning.
  3. False positives in either source are documented as intentional non-changes (with the reason the current convention stands and which source misread it), and every accepted finding carries a before/after note naming the changed spec section, the contract it now enforces, and the verification step that confirms the fix.
  4. The known conflicts are adjudicated at root cause — ratio-based SCS thresholds (`SCS > 1e-6` / `< 1e-8`) vs the locked log-based gate, `compute_globals` `D = 6.694` vs the v1.4 PHYS-01 D convention, and the M11/M12 severity reclassifications — each naming the root-cause ambiguity, which source was right and which wrong, and the convention now locked (the corresponding spec edits land in Phases 27–28).
  5. The issue ledger exists at its stable path under the Phase 24 (empirical-dataset-verification) directory, tracking every in-scope finding through `PENDING → IN_PROGRESS → FIX_APPLIED → VERIFIED`, with the explicit rule that "fix applied" is not closure and that each edit batch re-verifies previously `VERIFIED` findings it could have regressed.

**Plans**: 2 plans (Wave 1: 25-01 machinery — packet template + protocol README + ledger Lifecycle-Rules re-issue; Wave 2: 25-02 the three EVID-10 root-cause records [SCS, D=6.694, M11/M12] + same-commit ledger wiring)

**Wave 1**

  - [ ] 25-01-PLAN.md — Evidence-packet template (`_TEMPLATE.md`) + protocol README (D-03 enforcement, EVID-10 trigger table) + `24-ISSUE-LEDGER.md` Lifecycle-Rules re-issue to v1.5 phases

**Wave 2** *(blocked on Wave 1 completion)*

  - [ ] 25-02-PLAN.md — Three EVID-10 root-cause records (SCS thresholds, `D=6.694`, M11/M12 severity) with the four-source citation, verdicts, and same-commit ledger Evidence-Packet links + verdict notes (D-06)

### Phase 26: DataLoader Ingestion and Selection Contracts

**Goal**: `ctl_instruction.md` / `pinn_architecture.md` state one coherent DataLoader ingestion-and-selection contract — which trajectories load, how they are addressed, validated, excluded, and what storage format they take — each grounded in verified dataset facts.
**Depends on**: Phase 25 (consumes the evidence framework and seeded ledger; Phase 25 is gated on Phase 24.5).
**Requirements**: PIPE-01, PIPE-02, PIPE-03, PIPE-05, PIPE-06, PIPE-10
**Success Criteria** (what must be TRUE):

  1. The Stage 4→5 trajectory-validation gate contract (B-06) is defined: final-timestamp threshold, stage-dependent snapshot minimums, and rejection logging, as a DataLoader design contract.
  2. The ID-resolution contract (B-11) is defined: `id_to_path` built from the filesystem scan, with the explicit invariant that trajectory ID is never assumed equal to array index.
  3. The blacklist-exclusion contract (M11) is defined — load at DataLoader init, exclude, log the exclusion count, fail loudly if a blacklisted ID reaches a batch — grounded in the DATA-02 verified blacklist.
  4. The gold-counterpart contract (M13) is defined: a Stage-5 gold-existence check plus the fallback policy; if the sources are silent or conflicting on the fallback choice, it is surfaced as a STOP gap for user decision, not invented.
  5. The footer/parameter-heterogeneity contract (D7) is defined — `Result:` footer precedence, folder-default fallback, `tol_confidence` (`direct` vs `inferred`), and footer-as-metadata-only so the completeness gate never depends on footer presence — and the training-data format decision (D-03: HDF5 vs `.npy` vs txt/json) is presented to the user with verified evidence and the user-locked choice recorded in the specs.

**Plans**: TBD

### Phase 27: Sampling, Precision, and Global-Scale Contracts

**Goal**: Framework specs lock the sampling, precision, metadata-exposure, and global-scale contracts consistent with the verified snapshot distributions and the v1.4 physics conventions.
**Depends on**: Phase 26 (continues post-gate adjudication; sequenced after ingestion to manage shared spec sections and regressions).
**Requirements**: PIPE-04, PIPE-07, PIPE-08, PIPE-09
**Success Criteria** (what must be TRUE):

  1. The points-per-trajectory contract (M12) is an adjudicated sampling-feasibility rule (candidate `n_pts = min(32, int(0.5 * n_snapshots))`) consistent with the verified DATA-06 snapshot distributions.
  2. The precision contract states the float64-sufficiency rationale for validation metrics and the Decimal-for-masses policy, grounded in the DATA-05 mass-drift verdict.
  3. The data-side `dt_out` and stage-query contract is defined: the DataLoader exposes per-trajectory `dt_out` metadata and the `sample_replay(n, max_stage)` / `sample_lookahead(n, stage)` interface, with the M16 collocation-scaling policy that consumes it explicitly deferred to the doc-03 milestone via a recorded forward-reference.
  4. The global-scale computation contract (`compute_globals`) is consistent with the v1.4-locked PHYS-01 D convention, and the issue-02 `D = 6.694` claim is adjudicated (verified, corrected, or rejected per the EVID-10 record) rather than transcribed.

**Plans**: TBD

### Phase 28: Validation-Metrics Contracts

**Goal**: Framework specs carry one canonical, data-side definition for each validation metric, threshold-aligned to the locked post-v1.3 gate and the v1.4 physics outcomes, with all training-loop usage deferred to doc-03.
**Depends on**: Phase 27 (the global-scale contract from PIPE-09 feeds the SCS definition).
**Requirements**: VAL-01, VAL-02, VAL-03, VAL-04
**Success Criteria** (what must be TRUE):

  1. The specs carry one canonical SCS contract — definition and threshold adjudicated against the locked post-v1.3 gate (`ε_H > 10⁻⁵` / `SCS > −5`); the issue-02 ratio-based thresholds are resolved through the EVID-10 record, not transcribed.
  2. SASD is defined with its formula, data-side computation contract, and the low-resolution floor-effect caveat; training-side collocation weighting is deferred to the doc-03 milestone with a recorded forward-reference.
  3. IPR is defined with its formula and dual-epsilon consistency with the v1.4 PHYS-03 outcome; its ALM noise-floor role is recorded as a doc-03 forward-reference.
  4. PSC is defined with its formula and data-side computation contract; its replay-governance use is deferred to the doc-03 milestone with a recorded forward-reference.

**Plans**: TBD

### Phase 29: Acceptance Checks, Re-verification, and Handoff

**Goal**: Every v1.5 contract has an executed, numerically-defined acceptance check; the issue ledger closes; the SI-ledger is reconciled; and the handoff records what was fixed, left unchanged, and deferred, with FUT-01 divergence updated.
**Depends on**: Phases 25–28 (all adjudication and spec edits complete).
**Requirements**: VER-07, VER-08, VER-09, VER-11, VER-12
**Success Criteria** (what must be TRUE):

  1. Every v1.5 contract has a numerically-defined acceptance check naming its pass criterion, the data it runs on, and the command or function that executes it — not just prose.
  2. The acceptance checks are **executed** with disposable dataset and spec-consistency probes, each producing recorded pass/fail evidence; a failing check blocks phase completion and routes back to the originating phase, and no probe touches `pinn/` production code.
  3. The milestone handoff identifies which findings were fixed, which were intentionally left unchanged, and which were deferred, and FUT-01 divergence records are updated for every DataLoader-implementation-shaped finding.
  4. The remaining Source-Issue entries (`SI-DQA-002`, `SI-DQA-003`, `SI-PINN-002`) are each reviewed for issue-02 relevance and either retired with a back-reference to the resolving phase/commit or preserved with a written reason — none assumed resolved or assumed irrelevant.
  5. Roadmap traceability is confirmed at closure: all 36 v1.5 requirements map to exactly one phase, beginning at Phase 23 (VER-08).

**Plans**: TBD

## Progress

**Execution Order:** 23 → ⛔gate opens (user research starts) ‖ 24 runs in parallel → 24.5 readiness check → 25 → 26 → 27 → 28 → 29.

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 23. Research Package Assembly | v1.5 | 5/5 | Complete (consolidated) | 2026-06-10 |
| 24. Empirical Dataset Verification and Correction Addendum | v1.5 | 4/4 | Complete | 2026-06-11 |
| 24.5. Resolution Doc Readiness Verification (INSERTED) | v1.5 | 1/1 | Complete    | 2026-06-11 |
| 25. Evidence Framework and Issue Ledger | v1.5 | 0/2 | Not started (unblocked — Phase 24.5 passed) | - |
| 26. DataLoader Ingestion and Selection Contracts | v1.5 | 0/TBD | Not started (gated on Phase 24.5) | - |
| 27. Sampling, Precision, and Global-Scale Contracts | v1.5 | 0/TBD | Not started (gated on Phase 24.5) | - |
| 28. Validation-Metrics Contracts | v1.5 | 0/TBD | Not started (gated on Phase 24.5) | - |
| 29. Acceptance Checks, Re-verification, and Handoff | v1.5 | 0/TBD | Not started (gated on Phase 24.5) | - |

---
*Last updated: 2026-06-11 after Phase 24.5 completion (resolution doc readiness verification; READY-WITH-CAVEATS; Phases 25–29 unblocked).*
