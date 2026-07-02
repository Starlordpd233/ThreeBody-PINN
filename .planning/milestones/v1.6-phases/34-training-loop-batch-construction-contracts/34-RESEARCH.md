# Phase 34: Training-Loop & Batch-Construction Contracts - Research

**Researched:** 2026-06-24
**Domain:** v1.6 training-loop / batch-construction framework-spec contracts (specwork-only transcription + adjudication)
**Confidence:** HIGH

<user_constraints>
## User Constraints (from CONTEXT.md)

Source: copied from `.planning/phases/34-training-loop-batch-construction-contracts/34-CONTEXT.md`. [VERIFIED: `34-CONTEXT.md:1-421`]

### Locked Decisions (D-34-01 .. D-34-18, verbatim summary)

- **D-34-01:** Transcribe each LOOP contract at its **adjudicated verdict + status** with source citations — NEVER the issue-doc "preview" proposal. The discussion caught two preview→verdict mismatches (LOOP-04 `8.5`; LOOP-06 `n_col` formula), both corrected in `34-SPEC.md` (commit `0ffa3d8`). Transcribe the corrected SPEC. [VERIFIED: `34-CONTEXT.md:74-78`]
- **D-34-02 (LOOP-04/M14):** Lock ONLY the structural merge `clip_value = C_stage · median(recent global gradient norms)` (Adam-only; no L-BFGS clipping; rolling window). Preserve `7-10 / 5 / 3`; treat `5.0` as the Stage-2/3 instance/fallback. Do NOT canonize `8.5`. Defer exact early-`C` / bootstrap / lower floor (`1e-6`) / history-reset → Phase 34/FUT, citing M14 owner-route + §1.8 (GAP-08). NOT a STOP gap — source explicitly routes these. [VERIFIED: `34-CONTEXT.md:80-88`]
- **D-34-03 (LOOP-06/M16):** Follow M16 §1.10 `defer`. `n_col ∝ dt_base/dt_out` is the deferred candidate direction only (NOT transcribed, NOT probe-able); inverse form not adopted; v1.5 SCOPE-11/PIPE-08 forward-reference realized-as-deferred. M16 has no Phase-32 verdict — confirm `defer` against §1.10 at packet-authoring. [VERIFIED: `34-CONTEXT.md:89-93`]
- **D-34-04 (LOOP-04 split, SCOPE-13):** Mechanism stated EXACTLY ONCE canonical in `pinn_architecture.md` §4.4; C-schedule (`7-10/5/3`) stated EXACTLY ONCE in `ctl_instruction.md`. Collapse the two current ctl C-schedule locations to ONE canonical statement + a pointer. Bidirectional stable-anchor cross-refs (heading + `AC-LOOP-04`, NEVER line numbers). Status-tag parity. Win condition: one coherent rule recoverable from two halves, zero duplicated normative text. [VERIFIED: `34-CONTEXT.md:97-115`]
- **D-34-05 (SI-PINN-003/R9):** `ctl_instruction.md` Mini-Batch Construction is canonical (B07-04 rejects pinn §3.1). In pinn §3.1: remove author comment (line 351), replace Listing-2 batch description with a pointer extending the existing PIPE-04 note (line 352), mark SI-PINN-003 (line 1005) RESOLVED. Reject two-synchronized-copies. [VERIFIED: `34-CONTEXT.md:116-124`]
- **D-34-06:** D-34-04 and D-34-05 follow the SAME anti-duplication discipline: single canonical home + pointer. [VERIFIED: `34-CONTEXT.md:125-127`]
- **D-34-07:** Reuse Phase-33 blockquote-callout verbatim: `> **Phase 34 contract: <name> (LOOP-NN; <verdict>; AC-NN; grounded by <source>).**` with inline status tag + grounded-by citation (consistent with CURR callouts at `ctl_instruction.md` 1630/1832). [VERIFIED: `34-CONTEXT.md:131-137`]
- **D-34-08:** Transcribed pseudocode rendered in a fenced block labeled `normative spec contract — not executable; FUT-01/FUT-04 implements` (SCOPE-14). [VERIFIED: `34-CONTEXT.md:138-140`]
- **D-34-09 (bounded allowance):** For pure-deferral / owner-pending sub-parts (LOOP-03 collocation-50/50, LOOP-05 ALM-in-default-loss, LOOP-06 M16, LOOP-08 SASD), the callout uses the deferred/owner-pending tag and records the deferral + forward-reference in the body instead of a pseudocode block — same convention, status-driven body. ONLY adaptation. [VERIFIED: `34-CONTEXT.md:141-146`]
- **D-34-10:** Only M14 is pre-adjudicated. B-07, B-08, M16, ALM-μ_p-clamp are seeded PENDING — Phase 34 authors ONE evidence packet per finding (EVID-11/12) BEFORE any spec edit, then closes each ledger row `PENDING → IN_PROGRESS → FIX_APPLIED → VERIFIED`. Use existing EVID/AC reservation scheme; do NOT mint a new ID schema. [VERIFIED: `34-CONTEXT.md:150-158`]
- **D-34-11:** Packets CONSUME resolution-doc verdicts (§1.4 B-07 modified; §1.5 B-08 modified; §1.10 M16 defer; §1.18 ALM defer) — do NOT re-litigate. If a packet surfaces a NEW conflict, STOP per EVID-15 and record a `34-GAPS.md` gap. [VERIFIED: `34-CONTEXT.md:159-165`]
- **D-34-12:** LOOP-04 consumes the existing M14 verdict — no new M14 packet. [VERIFIED: `34-CONTEXT.md:166-167`]
- **D-34-13:** LOOP-07 (IPR/PSC) and LOOP-08 (SASD) are v1.5 carry-forwards (VAL-02/03/04), NOT issue-03 findings — no ledger row, no packet. Direct transcription tagged `provisional` with VAL citations; recalibration FUT (SCOPE-15). [VERIFIED: `34-CONTEXT.md:170-174`]
- **D-34-14:** VERIFY each training-side role against v1.5 contracts + existing spec. Source establishes role → transcribe provisional. Source silent on a role → `34-GAPS.md` STOP gap (owner-pending), NOT invented. LOOP-08 SASD: deferred/provisional, NO weighting formula. Default = no packet; v1.5-vs-current-spec CONFLICT → packet + EVID-15. [VERIFIED: `34-CONTEXT.md:175-184`]
- **D-34-15:** AUGMENT the existing ctl Total-Loss / Data-Flow section with the per-step ordering skeleton (forward → `L_total` assembly → backward → Adam-only median-clip → optimizer.step → optional scalar-ALM). Ordering ONLY: loss terms opaque, Phase-35 forward-ref; do NOT define loss components / `λ_E` / Huber-δ. Clip step cross-references pinn §4.4; ALM step optional/deferred. Reject a new separate subsection. [VERIFIED: `34-CONTEXT.md:188-196`]
- **D-34-16:** Two distinct classes: (a) batch edge cases (final-stage, undersized lookahead <16, replacement policy) = genuinely SOURCE-SILENT → `34-GAPS.md` STOP gap + `v1.6-GAPS.md` index, owner-pending. (b) M14-deferred constants = NOT source-silent (M14 routes them) → deferred → FUT in the LOOP-04 body, NO new `34-GAPS.md` entry. [VERIFIED: `34-CONTEXT.md:200-211`]
- **D-34-17 (probe scope, SCOPE-15):** Probe ONLY locked formulas: LOOP-01 `min(n_pts_cap, n_snapshots)`; LOOP-03 data-fidelity 50/50; LOOP-04 `clip_value = C_stage·median(...)`. LOOP-05/06/08 deferred = NO probe. LOOP-02/07 structural grep. IPR `1e-3` / PSC grid carried, not recalibrated. NO `n_col` probe. [VERIFIED: `34-CONTEXT.md:212-224`]
- **D-34-18:** `.planning/STATE.md` carries a user-owned uncommitted modification — NOT mutated or committed here. Only the SPEC fix, CONTEXT, and DISCUSSION-LOG are committed via `scripts/agent-commit` with explicit owned paths. [VERIFIED: `34-CONTEXT.md:228-232`]

### Claude's Discretion

- Number of Phase-34 plan files and task grouping, provided every LOOP-01..08 + SI-PINN-003 appears in a plan `requirements` field, packet-before-edit precedes each spec edit (D-34-10), and the plan is executable by `gsd-execute-phase`. [VERIFIED: `34-CONTEXT.md:234-239`]
- Exact evidence-packet filename slugs (stable, grep-friendly, mapped in the ledger), exact ledger Markdown layout, and exact deterministic check commands — provided they satisfy D-34-16/17. [VERIFIED: `34-CONTEXT.md:240-242`]

### Deferred Ideas (OUT OF SCOPE)

- Phase 35 (LOSS): loss-component scaling, capped-hybrid `λ_E` schedule, Huber-δ calibration, causal-training-mode (D-04) contract. [VERIFIED: `34-CONTEXT.md:397-399`]
- FUT-01/FUT-04 (trainex): the actual DataLoader, batch constructor, ALM update mechanics, causal-window mechanics, Stage-0 pilot calibration. [VERIFIED: `34-CONTEXT.md:400-402`]
- FUT/SCOPE-15: adaptive-stage-assignment EDA, threshold/IPR/PSC/SASD recalibration. [VERIFIED: `34-CONTEXT.md:403-404`]
- Owner-pending / deferred contract holes carried (not filled): M14-deferred clipping constants (D-34-16b, body-deferred); source-silent batch edge cases (D-34-16a, `34-GAPS.md`). [VERIFIED: `34-CONTEXT.md:405-408`]
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| LOOP-01 | Replay/lookahead batch-construction contract in `ctl_instruction.md` (`B_replay=240`, `B_lookahead=16`, `has_stage(k+1)` guard) tagged **provisional** (B-07 `modified`); causal-mode compatibility not selection (Phase 35 owner-pending). [VERIFIED: `34-SPEC.md:23-26`, `.planning/REQUIREMENTS.md:49`] | Current Mini-Batch block already carries 240/16/cap=32/Gumbel-top-k. Author B-07 packet (PENDING) before edit; consume §1.4. Record source-silent edge cases as `34-GAPS.md` gap. [VERIFIED: `ctl_instruction.md:1770-1784`, `03-final-resolution.md:36-38`, `32-ISSUE-LEDGER.md:18`] |
| LOOP-02 | Two-independent-point-set contract (data-fidelity vs collocation) with single-forward-pass allowance; `8192/4096` tagged **provisional** (B-08 `modified`). [VERIFIED: `34-SPEC.md:28-31`, `.planning/REQUIREMENTS.md:50`] | Author B-08 packet (PENDING) before edit; consume §1.5. Reconcile with SI-PINN-003 canonical (ctl). [VERIFIED: `03-final-resolution.md:40-42`, `32-ISSUE-LEDGER.md:19`] |
| LOOP-03 | Mixed time-sampling: data-fidelity 50/50 **retained** (B-07); collocation 50/50 **deferred** (B-08). [VERIFIED: `34-SPEC.md:33-36`, `.planning/REQUIREMENTS.md:51`] | Data 50/50 already present (Gumbel-top-k). Reconcile ROADMAP "both sets" wording to split status. Probe data-fidelity 50/50 only (D-34-17). [VERIFIED: `ctl_instruction.md:1775`, `03-final-resolution.md:40-42`] |
| LOOP-04 | Merged median-clipping: lock structural merge (Adam-only) `locked`; preserve `7-10/5/3`; `8.5` ABSENT both files; defer early-`C`/bootstrap/floor/history-reset → FUT (GAP-08); single canonical home per half, bidirectional anchors. [VERIFIED: `34-SPEC.md:38-41`, `.planning/REQUIREMENTS.md:52` (NOTE conflict below)] | Consume existing M14 packet (no new packet). Mechanism canonical in pinn §4.4; C-schedule canonical in ctl (collapse 2 ctl locations). Probe `clip_value=C_stage·median(...)` (D-34-17). [VERIFIED: `evidence/m14-gradient-clipping.md:82-118`, `03-final-resolution.md:52-54`] |
| LOOP-05 | ALM `λ_p`/`μ_p` update + `μ_p` clamp `[1e-4,100]` at status `defer`; dense-residual ALM REJECTED from default loss; ALM optional scalar-conservation only. [VERIFIED: `34-SPEC.md:43-46`, `.planning/REQUIREMENTS.md:53`] | Author ALM-μ_p-clamp packet (PENDING) before edit; consume §1.18. Default training-step contract excludes dense-residual ALM. NO probe (deferred). [VERIFIED: `03-final-resolution.md:92-94`, `32-ISSUE-LEDGER.md:32`] |
| LOOP-06 | `dt_out`-aware collocation-scaling realized-as-deferred (M16 §1.10 `defer`); `n_col ∝ dt_base/dt_out` deferred candidate direction only, NOT transcribed, NOT probe-able; inverse not adopted. [VERIFIED: `34-SPEC.md:48-51`, `.planning/REQUIREMENTS.md:54` (NOTE conflict below)] | Author M16 packet (PENDING) before edit; confirm `defer` against §1.10. Record M16 disposition, NO formula, NO probe. [VERIFIED: `03-final-resolution.md:60-62`, `32-ISSUE-LEDGER.md:24`] |
| LOOP-07 | Training-side IPR (ALM-convergence/noise-floor, provisional `1e-3`) + PSC (replay-buffer governance, provisional grid/normalization/SCR), tagged `provisional`, VAL-03/VAL-04 citations; recalibration FUT. [VERIFIED: `34-SPEC.md:53-56`, `.planning/REQUIREMENTS.md:55`] | v1.5 carry-forward (no packet). IPR/PSC roles + `IPR_train` noise-floor deferral already present; direct transcription. Probe = structural grep only. [VERIFIED: `ctl_instruction.md:684-718` (IPR), `ctl_instruction.md:719-764` (PSC), D-34-13] |
| LOOP-08 | SASD training-side collocation-weighting role tagged `provisional`/forward-referenced (VAL-02); NO weighting formula invented. [VERIFIED: `34-SPEC.md:58-61`, `.planning/REQUIREMENTS.md:56`] | v1.5 carry-forward (no packet). SASD-weighted collocation already deferred to doc-03; transcribe deferral + VAL-02 citation only. [VERIFIED: `ctl_instruction.md:680-682`, D-34-14] |
| SI-PINN-003 (R9) | Reconcile batch-construction inconsistency; `ctl_instruction.md` canonical; pinn §3.1 references it, author comment removed, SI-PINN-003 log marked RESOLVED. [VERIFIED: `34-SPEC.md:63-66`] | pinn §3.1 carries author comment (line 351) + PIPE-04 pointer seed (line 352); SI-PINN-003 logged (line 1005); also referenced in SI-PINN-002 item 3 (line 1002). Extend PIPE-04 pointer; do NOT duplicate ctl text. [VERIFIED: `pinn_architecture.md:351-352`, `pinn_architecture.md:1002`, `pinn_architecture.md:1005-1009`] |
</phase_requirements>

## Summary

Phase 34 is a specwork-only **transcription + adjudication** phase: it lands the training-loop and batch-construction contracts (LOOP-01..08 + SI-PINN-003) into `ctl_instruction.md` and `pinn_architecture.md`, each at its *adjudicated verdict and status*, with source citations — not the raw issue-doc proposals. [VERIFIED: `34-SPEC.md:7-9`] The hardest planning hazard is identical to Phase 33's: **source discipline, not implementation complexity.** The ROADMAP and REQUIREMENTS success-criteria for LOOP-04 / LOOP-06 / LOOP-03 still carry SUPERSEDED "preview" positions (`8.5`, `n_col ∝ dt_base/dt_out`, "both point sets"); the corrected source is `34-SPEC.md` + the resolution doc + Phase 32 ledger, which `modified`/`deferred` all three. [VERIFIED: `.planning/REQUIREMENTS.md:51-54`, `.planning/ROADMAP.md:188-189`, `34-SPEC.md:38-51`, `34-CONTEXT.md:28-37`]

The mechanism is the Phase-33 machine reused unchanged: **packet-before-edit** for the four PENDING findings (B-07, B-08, M16, ALM-μ_p-clamp), each authored into a Phase-34 `evidence/` directory mirroring the Phase-32 template, then the ledger row closed `PENDING → IN_PROGRESS → FIX_APPLIED → VERIFIED`; then tightly-scoped spec edits using the Phase-33 blockquote-callout convention verbatim; then deterministic `rg`/`python3` source checks + forbidden-path guards. LOOP-04 consumes the existing M14 packet (no new packet); LOOP-07/08 are v1.5 carry-forwards (no ledger row, no packet). [VERIFIED: `34-CONTEXT.md:150-174`, `32-ISSUE-LEDGER.md:18-32`, `evidence/m14-gradient-clipping.md:82-118`]

The two highest-risk transcription tasks are LOOP-04 (the `8.5` trap + the cross-file single-canonical-home guardrail that must NOT itself become a second SI-PINN-003) and SI-PINN-003/R9 (resolve the inconsistency via a pointer, never two synchronized copies). Both are governed by the same anti-duplication discipline: **single canonical home per value/formula + a verifier that proves zero duplication.** [VERIFIED: `34-SPEC.md:38-41`, `34-CONTEXT.md:97-127`]

**Primary recommendation:** Plan Phase 34 as evidence-packet-first spec editing in dependency order — (1) author B-07/B-08/M16/ALM packets + open the ledger rows; (2) LOOP-04 cross-file clipping edit (pinn §4.4 mechanism canonical + ctl C-schedule collapse to one home) + LOOP-01/02/03 ctl batch contract; (3) SI-PINN-003 pinn §3.1 pointer + log resolution; (4) LOOP-05 ALM + LOOP-06 M16 deferral bodies; (5) LOOP-07/08 v1.5-carry-forward transcription; (6) the ctl total-loss ordering skeleton (D-34-15); then deterministic source/consistency/regression/scope checks with the LOOP-04 (c)/(d)/(e) re-verify-after-every-batch loop. Record the source-silent batch edge cases as a `34-GAPS.md` STOP gap; carry M14-deferred constants as body-deferred (no gap). [VERIFIED: `34-SPEC.md:68-103`, `34-CONTEXT.md:150-224`]

## Project Constraints (from AGENTS.md / CLAUDE.md)

| Directive | Planning Impact |
|-----------|-----------------|
| v1.6 phases must NOT invent content where sources are silent/ambiguous; STOP protocol governs. [VERIFIED: `AGENTS.md` v1.6 applicability block; `34-SPEC.md:88-90`] | Any new semantic / process-schema / cross-phase decision during planning or execution produces `## RESEARCH BLOCKED` or a `34-GAPS.md` STOP gap, not a guessed contract. |
| v1.6 specwork edits limited to `ctl_instruction.md` + `pinn_architecture.md` (SCOPE-13); `sampling_method.md` frozen, `data_quality_assessment.md`/`review-of-framework.md`/`stage-strat-revision.md` read-only, `pinn/` live code forbidden, no training-loop code (SCOPE-14), no EDA/Stage-0 pilot (SCOPE-15). [VERIFIED: `.planning/REQUIREMENTS.md:93-95`, `34-SPEC.md:77-83`] | Plans must include forbidden-path checks and must NOT schedule implementation tasks. Transcribed pseudocode is labeled non-executable (D-34-08). |
| Locked v1.4/v1.5 outcomes are hard constraints (SCOPE-12): 14D `[τ,IC₁₃]`, Jacobi IC₁₃, mass-weighted COM head, `eps_soft=1e-5`, SCS gate, raw-mass `D≈4.6416` (`6.694` rejected), PIPE-01..10, VAL-01..04. [VERIFIED: `.planning/REQUIREMENTS.md:16`, `34-SPEC.md:88`] | Locked-convention regression guard required in verification (`D≈4.6416` present / `6.694` absent; 14D input; Jacobi COM head; eps_soft; SCS gate; PIPE/VAL refs intact). |
| Live `pinn/` code is NOT a grounding source. [VERIFIED: `AGENTS.md`; `.claude/rules/pinn-reference.md`] | Plans may only mention live code in FUT-01/FUT-04 hand-off contexts, never as evidence. |
| Packet-before-edit: owner phase authors the evidence packet + updates the ledger before editing any spec section for that row; Phase 36 rejects unlinked edits. [VERIFIED: `32-ISSUE-LEDGER.md:34-36`, `evidence/README.md:90-94`] | Make packet/ledger tasks the first wave; B-07/B-08/M16/ALM each get a packet before the matching spec edit. |
| STOP gaps require `34-GAPS.md` + `v1.6-GAPS.md` index entries with all required fields; AGENTS step-2 understanding checks first. [VERIFIED: `evidence/README.md:76-84`, `AGENTS.md` STOP protocol] | Verification inspects any new `34-GAPS.md`/`v1.6-GAPS.md` edits for complete STOP fields. The batch-edge-case gap (D-34-16a) is the one anticipated entry. |
| Session-start git state surfaced; unrelated changes preserved; `.planning/STATE.md` carries a user-owned uncommitted change (D-34-18). [VERIFIED: `34-CONTEXT.md:228-232`, local `git status`] | Executor must NOT mutate/commit `STATE.md`; treat as someone else's work. Commits via `scripts/agent-commit` with `GIT_AGENT_ID` + `GIT_AGENT_OWNED_PATHS`, explicit owned paths, no broad staging. |

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|--------------|----------------|-----------|
| Evidence packet + ledger lifecycle (B-07, B-08, M16, ALM) | Planning artifacts (`evidence/`, `32-ISSUE-LEDGER.md`) | Framework specs | Ledger mandates a packet before spec edits for each owned PENDING row. [VERIFIED: `32-ISSUE-LEDGER.md:18-32,34-36`] |
| Batch-construction contract (LOOP-01/02/03) + total-loss skeleton (D-34-15) | `ctl_instruction.md` (CANONICAL) | B-07/B-08 packets; pinn §3.1 cross-link | ctl Mini-Batch Construction is canonical; pinn §3.1 references it. [VERIFIED: `ctl_instruction.md:1770-1784`, `pinn_architecture.md:352`, `03-final-resolution.md:122` (B07-04)] |
| Gradient-clipping MECHANISM (LOOP-04) | `pinn_architecture.md` §4.4 (CANONICAL) | M14 packet; ctl cross-ref | M14 packet locates the merged mechanism canonical in pinn §4.4. [VERIFIED: `pinn_architecture.md:700-723`, `evidence/m14-gradient-clipping.md:35`, `03-final-resolution.md:52-54`] |
| Gradient-clipping C-SCHEDULE (LOOP-04) | `ctl_instruction.md` (CANONICAL, ONE home) | pinn §4.4 cross-ref | C-schedule `7-10/5/3` is ctl-owned; two current ctl locations collapse to one. [VERIFIED: `ctl_instruction.md:1792-1798`, `ctl_instruction.md:1909-1913`, `34-CONTEXT.md:97-115`] |
| ALM optional/deferred contract (LOOP-05) | `pinn_architecture.md` §4.2 (existing) + ctl total-loss skeleton optional step | ALM packet | pinn §4.2 already records optional/OFF ALM; ctl skeleton marks the ALM step optional. [VERIFIED: `pinn_architecture.md:671-682`, `34-CONTEXT.md:188-196`] |
| `dt_out` collocation-scaling deferral (LOOP-06) | `ctl_instruction.md` (forward-interface note) | M16 packet | ctl Mini-Batch already exposes `dt_out`/`n_snapshots` metadata as the deferred-M16 forward interface. [VERIFIED: `ctl_instruction.md:1775`, `03-final-resolution.md:60-62`] |
| IPR/PSC/SASD training-side roles (LOOP-07/08) | `ctl_instruction.md` (Data-side metric contracts) | pinn §3.4 dual-epsilon cross-ref | v1.5 VAL-02/03/04 contracts live in ctl; training-side roles already deferred to doc-03. [VERIFIED: `ctl_instruction.md:636-764`, `pinn_architecture.md:537`] |
| SI-PINN-003 reconciliation (R9) | `pinn_architecture.md` §3.1 + SI log | ctl canonical contract | Author comment + SI-PINN-003 log live in pinn; ctl is canonical. [VERIFIED: `pinn_architecture.md:351-352,1005-1009`] |
| Verification | Local `rg`/`python3`/git checks | — | Specwork verification = deterministic source checks + forbidden-path guards, not runtime training probes. [VERIFIED: `33-RESEARCH.md:418-448`, `34-CONTEXT.md:355-358`] |

## Standard Stack

### Core

| Artifact | Version | Purpose | Why Standard |
|----------|---------|---------|--------------|
| `ctl_instruction.md` | v1.6 active framework spec (2067 lines) | CANONICAL edit target for batch construction, C-schedule, IPR/PSC/SASD, total-loss skeleton. [VERIFIED: `local wc -l` = 2067; `.planning/REQUIREMENTS.md:93`] | SCOPE-13 + SI-PINN-003 designate ctl canonical for batch construction. [VERIFIED: `34-SPEC.md:87`, `03-final-resolution.md:122`] |
| `pinn_architecture.md` | v1.6 active framework spec (1013 lines) | CANONICAL edit target for clipping MECHANISM (§4.4), ALM ablation (§4.2), SI-PINN-003 reconciliation (§3.1). [VERIFIED: `local wc -l` = 1013] | SCOPE-13 routes gradient clipping + training strategy here. [VERIFIED: `.planning/REQUIREMENTS.md:93`] |
| Phase 32 evidence protocol + ledger | v1.6 Phase 32 | Packet-before-edit governance + template + lifecycle for the 4 new packets. [VERIFIED: `evidence/README.md:1-132`, `evidence/_TEMPLATE.md:1-139`] | B-07/B-08/M16/ALM rows are seeded PENDING there for Phase 34 ownership. [VERIFIED: `32-ISSUE-LEDGER.md:18-32`] |
| `03-final-resolution.md` | issue-03 candidate verdict source | Source of the adjudicated verdicts (§1.4/1.5/1.8/1.10/1.18 + claim matrix B07-04). [VERIFIED: `03-final-resolution.md:36-94,122`] | The candidate verdict source the packets consume (not authority). [VERIFIED: `evidence/README.md:25,32`] |
| `rg` | 15.1.0 | Deterministic source-token + forbidden-path checks. [VERIFIED: local `rg --version`] | Phase 32/33 precedent. [VERIFIED: `33-RESEARCH.md:151`] |
| `python3` | 3.14.5 | Parser-backed token/negative-token/duplication assertions + formula-sanity probes. [VERIFIED: local `python3 --version`] | Phase 32/33 precedent. [VERIFIED: `33-RESEARCH.md:152`] |
| `git` | 2.54.0 | Scoped status, diff, protected-path guards. [VERIFIED: local `git --version`] | AGENTS git-state + explicit-path discipline. [VERIFIED: `34-CONTEXT.md:359`] |

### Supporting

| Artifact | Version | Purpose | When to Use |
|----------|---------|---------|-------------|
| `scripts/agent-commit` | present, executable | Commit wrapper for execution (not this research). [VERIFIED: `33-RESEARCH.md:159`, `34-CONTEXT.md:359`] | Only if execution commits Phase 34 work; set `GIT_AGENT_ID` + `GIT_AGENT_OWNED_PATHS`. |
| `.planning/milestones/v1.6-GAPS.md` | active (Phase 32/33 sections, 0 OPEN) | Milestone STOP index — add a Phase 34 section on the first STOP gap. [VERIFIED: `local read v1.6-GAPS.md:16-34`] | Update for the anticipated batch-edge-case gap (D-34-16a). |
| `evidence/m14-gradient-clipping.md` | Phase 32, `accept-resolution` | The M14 verdict LOOP-04 consumes — no new packet. [VERIFIED: `evidence/m14-gradient-clipping.md:64-118`] | Cite for AC-LOOP-04; do not re-author. |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Evidence-packet-first spec editing | Edit specs directly from ROADMAP/REQUIREMENTS text | NOT acceptable: ledger mandates packets first, and ROADMAP/REQUIREMENTS LOOP-04/06/03 wording is SUPERSEDED. [VERIFIED: `32-ISSUE-LEDGER.md:34-36`, `.planning/REQUIREMENTS.md:51-54`] |
| Local deterministic source checks | Runtime training / EDA / Stage-0 probes | Out of scope (SCOPE-14/15); only disposable formula-sanity probes permitted. [VERIFIED: `.planning/REQUIREMENTS.md:94-95`, `34-CONTEXT.md:212-224`] |
| Single canonical home + pointer (clipping, batch) | Two synchronized copies across files | Rejected — that is the exact SI-PINN-003 hazard. [VERIFIED: `34-CONTEXT.md:116-124`, `34-SPEC.md:41`] |

**Installation:** No package installation is needed for Phase 34. [VERIFIED: `34-SPEC.md:68-103`, local tool probes]

## Package Legitimacy Audit

No external packages are recommended or installed for Phase 34. [VERIFIED: `34-SPEC.md` boundaries; specwork-only]

| Package | Registry | Age | Downloads | Source Repo | Verdict | Disposition |
|---------|----------|-----|-----------|-------------|---------|-------------|
| none | n/a | n/a | n/a | n/a | n/a | No package work in scope. |

**Packages removed due to [SLOP] verdict:** none.
**Packages flagged as suspicious [SUS]:** none.

## Architecture Patterns

### System Architecture Diagram

```text
Phase 34 plan entry
  -> read 34-SPEC / 34-CONTEXT / 34-RESEARCH / AGENTS.md
  -> read 03-final-resolution.md (§1.4/1.5/1.8/1.10/1.18, claim matrix) + 32-ISSUE-LEDGER + M14 packet
  -> WAVE 1: packet-before-edit (no spec edit yet)
       author evidence/b-07-*.md   (consume §1.4 B-07 modified) -> open ledger B-07 row
       author evidence/b-08-*.md   (consume §1.5 B-08 modified) -> open ledger B-08 row
       author evidence/m16-*.md    (consume §1.10 M16 defer)    -> open ledger M16 row
       author evidence/alm-*.md    (consume §1.18 ALM defer)    -> open ledger ALM row
       (LOOP-04 consumes existing M14 packet; LOOP-07/08 = v1.5 carry-forward, no packet)
       IF a packet surfaces a NEW conflict -> STOP, 34-GAPS.md (EVID-15)
  -> WAVE 2: spec edits (each cites its packet/verdict)
       LOOP-04: pinn §4.4 mechanism (canonical, exactly once)
                + ctl C-schedule collapse to ONE home + pointer
                + bidirectional anchors (heading + AC-LOOP-04)
       LOOP-01/02/03: ctl Mini-Batch contract (provisional tags + citations)
       SI-PINN-003 (R9): pinn §3.1 remove author comment + extend PIPE-04 pointer
                + mark SI-PINN-003 log RESOLVED (also SI-PINN-002 item 3)
       LOOP-05: ALM optional/deferred (default loop excludes dense-residual ALM)
       LOOP-06: M16 realized-as-deferred body (NO formula, NO probe)
       LOOP-07/08: IPR/PSC/SASD training-side roles provisional (VAL-02/03/04)
       D-34-15: ctl total-loss ORDERING skeleton (loss terms opaque, Phase-35 fwd-ref)
       record source-silent batch edge cases -> 34-GAPS.md + v1.6-GAPS.md (D-34-16a)
       carry M14-deferred constants -> body-deferred, NO gap (D-34-16b)
  -> WAVE 3: deterministic verification (re-run LOOP-04 (c)/(d)/(e) after EVERY batch)
       source-token + negative-token checks (8.5 absent; 7-10/5/3 present; tags)
       no-duplication check (each formula/value one canonical home)
       bidirectional-anchor resolve check
       locked-convention regression guard (D≈4.6416 / no 6.694 / 14D / COM / eps_soft / SCS / PIPE / VAL)
       forbidden-path scope check (only ctl + pinn modified)
       disposable formula-sanity probes (LOOP-01/03/04 only)
       ledger closure PENDING->...->VERIFIED with packet link + AC ID
  -> summary / handoff (Phase 36 consumes closed ledger + AC list)
```

This flow reflects the ledger packet-before-edit rule, the SI-PINN-003 single-canonical-home discipline, and the LOOP-04 re-verify-after-every-batch ROADMAP requirement. [VERIFIED: `32-ISSUE-LEDGER.md:34-36`, `34-SPEC.md:41`, `34-CONTEXT.md:389-391`]

### Recommended Project Structure

```text
.planning/phases/34-training-loop-batch-construction-contracts/
├── 34-RESEARCH.md          # this artifact
├── 34-SPEC.md / 34-CONTEXT.md / 34-DISCUSSION-LOG.md   # existing
├── 34-*-PLAN.md            # planner output; count/grouping is planner discretion (D-34 discretion)
├── 34-GAPS.md              # created on first STOP gap (D-34-16a batch edge cases anticipated)
├── 34-VERIFICATION.md      # durable verification record (Phase-32/33 precedent)
└── evidence/               # FOUR new packets: b-07, b-08, m16, alm (mirror Phase-32 schema)
```

There is currently NO `evidence/` subdirectory and NO `34-GAPS.md` under the Phase-34 directory. [VERIFIED: local `ls .planning/phases/34-*/` shows only `34-CONTEXT.md`, `34-DISCUSSION-LOG.md`, `34-SPEC.md`] Mirror Phase-32 `evidence/_TEMPLATE.md` + `README.md`; do NOT invent a new schema (D-34-10). [VERIFIED: `evidence/README.md:96-120`, `34-CONTEXT.md:150-158`]

### Pattern 1: Packet-Before-Spec-Edit

**What:** Before editing a spec section for a PENDING owned row, copy `_TEMPLATE.md` to `evidence/{finding-id}.md`, fill every required section with line-range citations, consume the resolution-doc verdict, set the verdict token + status, and open the ledger row (`PENDING → IN_PROGRESS`). [VERIFIED: `evidence/README.md:110-120`, `evidence/_TEMPLATE.md:1-139`]

**When to use:** For B-07 (LOOP-01), B-08 (LOOP-02/03), M16 (LOOP-06), ALM-μ_p-clamp (LOOP-05). NOT for LOOP-04 (consumes existing M14 packet), NOT for LOOP-07/08 (v1.5 carry-forwards, no ledger row). [VERIFIED: `34-CONTEXT.md:150-174`, `32-ISSUE-LEDGER.md:18-32`]

**Example:**
```bash
# Source: Phase 32 packet-before-edit verification pattern.
rg -n "B-07|B-08|M16|ALM mu_p clamp|AC-LOOP" \
  .planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md
```

### Pattern 2: Single-Canonical-Home + Pointer (anti-duplication)

**What:** Each normative formula/value has EXACTLY ONE canonical home; every other location that needs it carries a stable-anchor pointer (section heading + AC ID), never an independent normative copy. A verifier PROVES zero duplication. [VERIFIED: `34-CONTEXT.md:97-127`, `34-SPEC.md:41`]

**When to use:** LOOP-04 (mechanism canonical in pinn §4.4; C-schedule canonical in ctl — collapse the two current ctl locations to one) and SI-PINN-003 (ctl Mini-Batch canonical; pinn §3.1 pointer). [VERIFIED: `ctl_instruction.md:1792-1798,1909-1913`, `pinn_architecture.md:352,700-723`]

**Win condition:** the merged rule is recoverable as ONE coherent rule from the two cross-referenced halves with zero duplicated normative text — not merely "8.5 removed / 7-10/5/3 present". [VERIFIED: `34-SPEC.md:41`, `34-CONTEXT.md:108-109`]

### Pattern 3: Status-Tagged Contract With Explicit Deferred/Owner-Pending Holes

**What:** Write normative structure, but tag each contract `locked` / `provisional` / `deferred` / `owner-pending` and route unresolved values to FUT explicitly rather than selecting defaults. [VERIFIED: `34-SPEC.md:94`, `33-RESEARCH.md:238-242`]

**When to use:** LOOP-01/02 (`provisional` defaults), LOOP-03 collocation (`deferred`), LOOP-04 early-`C`/bootstrap/floor/history-reset (`deferred → FUT`, body, no gap), LOOP-05 ALM (`deferred`/optional), LOOP-06 M16 (`deferred`), LOOP-07/08 (`provisional`). [VERIFIED: `34-SPEC.md:23-61`]

### Pattern 4: Phase-33 Blockquote-Callout (verbatim)

**What:** Each LOOP contract opens with `> **Phase 34 contract: <name> (LOOP-NN; <verdict>; AC-NN; grounded by <source>).**` plus inline status tag and grounded-by citation — file-internal consistency with CURR callouts. [VERIFIED: `34-CONTEXT.md:131-137`, `ctl_instruction.md:264-265,1630-1631,1832-1834`]

**Example (existing CURR-03 callout to mirror):**
```text
> **Phase 33 contract: dual-path stage-transition state machine (CURR-03;
> D-33-08, D-33-09; AC-CURR-03; grounded by the resolution doc §1.11 and
> `evidence/d5-stage-transitions.md`).**
```
[VERIFIED: `ctl_instruction.md:1832-1834`]

### Pattern 5: Protected-Path Guard

**What:** Scoped git checks proving Phase 34 touched ONLY `ctl_instruction.md` + `pinn_architecture.md` (plus `.planning/phases/34-*/` artifacts), not frozen/read-only specs, live `pinn/`, generated data, or the user-owned `STATE.md`. [VERIFIED: `34-SPEC.md:103`, `34-CONTEXT.md:228-232`]

### Anti-Patterns to Avoid

- **Re-locking `8.5`:** REQUIREMENTS LOOP-04 + ROADMAP success-criterion 3 still say "stages 0–1: 8.5" — both SUPERSEDED. `8.5` must be ABSENT from both files. [VERIFIED: `.planning/REQUIREMENTS.md:52`, `.planning/ROADMAP.md:188`, `34-SPEC.md:40`]
- **Transcribing `n_col ∝ dt_base/dt_out`:** REQUIREMENTS LOOP-06 + ROADMAP success-criterion 4 still say "transcribe the verbatim direction" — SUPERSEDED; it is a deferred candidate direction only, NOT transcribed, NOT probe-able. [VERIFIED: `.planning/REQUIREMENTS.md:54`, `.planning/ROADMAP.md:189`, `34-SPEC.md:50-51`]
- **Mandating collocation 50/50 "to both sets":** REQUIREMENTS LOOP-03 + ROADMAP say "applied to both point sets" — collocation 50/50 is DEFERRED, not mandated. [VERIFIED: `.planning/REQUIREMENTS.md:51`, `.planning/ROADMAP.md:187`, `34-SPEC.md:35`]
- **Creating a second SI-PINN-003:** duplicating the clipping mechanism or the batch contract across files. Use single-canonical-home + pointer. [VERIFIED: `34-CONTEXT.md:110-113`]
- **Spec edits before packets:** violates the ledger packet-before-edit mandate. [VERIFIED: `32-ISSUE-LEDGER.md:34-36`]
- **Inventing the batch edge-case policy:** final-stage / undersized-lookahead / replacement are source-silent → STOP gap, not a default. [VERIFIED: `03-final-resolution.md:38,223` (GAP-05), `34-SPEC.md:111`]
- **Opening a `34-GAPS.md` entry for M14-deferred constants:** they are source-routed, not source-silent → body-deferred only. [VERIFIED: `34-CONTEXT.md:206-211`, `evidence/m14-gradient-clipping.md:92-97`]
- **Using live `pinn/` code as evidence; running EDA / Stage-0 / training:** forbidden. [VERIFIED: `.planning/REQUIREMENTS.md:94-95,98`]
- **Treating the ROADMAP/REQUIREMENTS wording as newer than the SPEC/resolution doc:** the SPEC corrected the previews (commit `0ffa3d8`). [VERIFIED: `34-CONTEXT.md:28-37`]

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Evidence adjudication schema | New packet format / ad-hoc notes | Phase-32 `evidence/_TEMPLATE.md` + `README.md` | Ledger + Phase 36 handoff expect packet/verdict linkage. [VERIFIED: `evidence/README.md:8-14`, `32-ISSUE-LEDGER.md:34-36`] |
| AC / EVID ID scheme | New ID schema | Existing AC-LOOP-01..06 + EVID-11/12 reservations | D-34-10 forbids minting a new schema. [VERIFIED: `32-ISSUE-LEDGER.md:18-32`, `34-CONTEXT.md:156-158`] |
| STOP handling | Informal TODO / planner assumption | `34-GAPS.md` + `v1.6-GAPS.md` with all fields | AGENTS requires full STOP fields + milestone index. [VERIFIED: `evidence/README.md:76-84`] |
| Cross-file consistency (clipping, batch) | Two synchronized copies | Single canonical home + stable-anchor pointer + no-duplication verifier | Duplication IS the SI-PINN-003 hazard. [VERIFIED: `34-CONTEXT.md:110-124`] |
| Source validation | Manual eyeballing | `rg` + `python3 -c` token / negative-token / duplication assertions | Phase 32/33 precedent. [VERIFIED: `33-RESEARCH.md:264`] |
| Deferred numeric values | One-off defaults in prose | Explicit `deferred → FUT` / `owner-pending` holes | Early-`C`/bootstrap/floor/history-reset, collocation 50/50, ALM clamp, M16, IPR/PSC recalibration are all NOT Phase-34 decisions. [VERIFIED: `34-SPEC.md:40,45,50`, `03-final-resolution.md:226,224,237,228`] |
| Total-loss assembly | Rewriting loss components / `λ_E` / Huber-δ | Ordering skeleton with opaque terms + Phase-35 forward-ref | The 34↔35 boundary; Phase 35 owns components/weights. [VERIFIED: `34-CONTEXT.md:188-196`, `34-SPEC.md:78` ] |

**Key insight:** Phase 34's hardest work is preserving adjudication provenance while editing prose and proving zero cross-file duplication; custom shortcuts create spec drift (and second SI-PINN-003s) faster than they save time. [VERIFIED: `34-SPEC.md:38-41`, `AGENTS.md` STOP protocol]

## Current-State Survey (HIGH value — actual live-file content + real line numbers)

> The 34-CONTEXT anchors are approximate. The line numbers below are the REAL current positions (verified by `rg -n` / `Read` this session). The planner must re-grep at execution time since edits shift lines.

### `ctl_instruction.md` (2067 lines)

| Region | Real lines | Current content (verbatim/quoted) | Phase-34 action |
|--------|-----------|-----------------------------------|-----------------|
| Data Flow During Training | 1685-1716 | 4-step per-training-step flow: Input (14D `[τ,IC₁₃]`) → Network Prediction (COM head) → Loss Computation (lists `L_data/L_IC/L_phys^causal/L_E/L_L`) → Backpropagation. [VERIFIED: `ctl_instruction.md:1685-1716`] | LOOP/D-34-15 host: augment with ordering skeleton (see below). |
| Loss Function Formulation / Total Loss | 1718-1745 | `L_total = L_data + λ_IC·L_IC + λ_phys·L_phys^causal + λ_E·L_E + λ_L·L_L`; terms defined by name in PHYS-05 catalog in `pinn_architecture.md`; optimizer-phase + causal-weighting notes; **pseudo-ALM formulation already REJECTED** at line 1745 ("squaring a nonnegative MSE produces a quartic residual…Optional ALM for scalar conservation constraints only…P2 ablation"). [VERIFIED: `ctl_instruction.md:1718-1745`] | D-34-15 augment ordering skeleton here; ALM already rejected — LOOP-05 reinforces optional/deferred. |
| Mini-Batch Construction with Lookahead Sampling | 1770-1784 | Heading 1770. Block: batch size B (256), `ρ_lookahead` 5%. Callout (1775): `n_pts(traj) = min(n_pts_cap, n_snapshots(traj))` without replacement; `n_pts_cap` default 32 (example, not evidence-based, config knob); **50/50 composition** = `k_w = floor(n_pts/2)` accel-norm-weighted (Gumbel-top-k) + uniform remainder, seeded; loader exposes `n_snapshots(traj)` + `dt_out(traj)` metadata ("**forward interface for the deferred M16 collocation-density question — doc-03; not used here**"); "No `0.5 x n_snapshots` factor". Citation (1777): M12 verdict (Phase 25 EVID-10), medians 61/127/1003. Table (1779-1782): Replay set `B_≤k` = 240; Look-ahead `B_{k+1}` = 16. [VERIFIED: `ctl_instruction.md:1770-1784`] | LOOP-01/02/03 host. 240/16/cap=32/Gumbel-top-k/M16-metadata-fwd-ref ALL ALREADY PRESENT. Add B-07 provisional tags + has_stage(k+1) guard + edge-case gap; reconcile B-08 two-point-set + SI-PINN-003 canonical. |
| Adaptive Median-Based Gradient Clipping (prose) | 1786-1798 | Heading 1786. Prose (1788-1790): "threshold is `C` times the moving median of recent norms". **C-schedule table (1792-1798): 0-1 → 7-10; 2-3 → 5; 4-6 → 3.** [VERIFIED: `ctl_instruction.md:1786-1798`] | LOOP-04 C-schedule canonical home (D-34-04). Collapse with the Consolidated table below to ONE home. |
| L-BFGS no-clipping note | 1827-1828 | "**No gradient clipping during L-BFGS, as line-search creates a trust region.**" [VERIFIED: `ctl_instruction.md:1827-1828`] | Supports LOOP-04 Adam-only scope. |
| Consolidated Hyperparameter Schedule (table) | 1907-1915 | Table 1909-1913: rows 0-1 / 2-3 / 4-6 with **Clip `C` = 7-10 / 5 / 3** (a SECOND copy of the C-schedule). [VERIFIED: `ctl_instruction.md:1907-1915`] | LOOP-04 D-34-04: this is the duplicate. Collapse to a pointer to the canonical C-schedule (or vice-versa) — exactly ONE normative copy. |
| IPR / PSC / SASD data-side metric contracts | 636-764 | SASD (652-682, VAL-02; SASD-weighted collocation sampling "**deferred to the doc-03 milestone**" at 680-682); IPR (684-718, VAL-03; provisional `IPR > 1e-3` flag at 712-714; **`IPR_train` ALM-noise-floor role "deferred to doc-03"** at 705-710); PSC (719-764, VAL-04; "**Replay-governance and training-side use of PSC is deferred to the doc-03 milestone**" at 764). [VERIFIED: `ctl_instruction.md:636-764`] | LOOP-07/08 host. The training-side roles ARE already established here as doc-03 deferrals — direct provisional transcription (no invention). |
| `8.5` | (none) | **`rg -n "8\.5"` returns NO match in ctl_instruction.md.** [VERIFIED: local `rg`] | LOOP-04: `8.5` already absent — preserve absence; no removal needed in ctl. |
| Phase-33 callouts (convention examples) | 264-265, 283-284, 313-314, 1161-1163, 1309-1311, 1630-1631, 1832-1834 | Verbatim `> **Phase 33 contract: … (CURR-NN; D-33-…; AC-CURR-…; grounded by …).**` blocks. [VERIFIED: local `rg`] | Copy convention verbatim for Phase-34 callouts (D-34-07). |

### `pinn_architecture.md` (1013 lines)

| Region | Real lines | Current content (verbatim/quoted) | Phase-34 action |
|--------|-----------|-----------------------------------|-----------------|
| §3.1 Data Fidelity / Batch Construction | 292, 323-357 | "Batch Construction:" (323); Listing 2 `get_batch(batch_size, points_per_trajectory=32)` (328-345) with `N_data = batch_size * points_per_trajectory  # e.g., 256 * 32 = 8192` (344). **Author comment (351): "[Author Comment: This above batch construction is not consistent with the CTL instruction plan. Look into this.]"** **PIPE-04 note (352, the pointer SEED):** "`points_per_trajectory=32` is a code default, not the spec contract. The operative … rule is `n_pts(traj) = min(n_pts_cap, n_snapshots(traj))` … defined in `ctl_instruction.md` Mini-Batch Construction. … exposes `sample_replay(n, max_stage)` and `sample_lookahead(n, stage)` … (PIPE-08, `ctl_instruction.md` §2.6)." [VERIFIED: `pinn_architecture.md:323-352`] | SI-PINN-003/R9 + LOOP-02 host. Remove author comment (351); EXTEND PIPE-04 note (352) into the canonical pointer; do NOT copy ctl contract text. |
| §4.2 Optional ALM Ablation (P2) | 671-682 | "an augmented Lagrangian method may be applied to **scalar conservation constraints only**"; constraints `c_E`, `c_{L,α}` (RMS); "**Never apply ALM to the dense ODE residual.**" (676); dual updates only between Adam epochs / never in L-BFGS (677); "**Default: ALM is OFF.**" (679); "not part of the baseline training contract" (681). Author comment at 675 (markdown-syntax nit). [VERIFIED: `pinn_architecture.md:671-682`] | LOOP-05 host. ALM already optional/OFF/scalar-only/no-dense-residual. Transcribe `λ_p`/`μ_p` update + `[1e-4,100]` clamp as **deferred/conditional** (NOT default); do not adopt into default loop. |
| §4.4 Adaptive Gradient Clipping (mechanism) | 700-723 | Heading 700. Prose (702-706): clip global L2 norm relative to recent typical magnitude. Listing 6 (708-722): `grad_history` last 100; `total_norm = …`; "**Clip norm to 5x the median of recent norms**"; `clip_value = 5.0 * torch.median(torch.stack(grad_history))` (719); `clip_grad_norm_` (720); "Then, call optimizer.step()" (722). [VERIFIED: `pinn_architecture.md:700-723`] | LOOP-04 MECHANISM canonical home (D-34-04). Merge to `clip_value = C_stage · median(recent global grad norms)` (Adam-only), with `5.0` as Stage-2/3 instance/fallback; label pseudocode non-executable (D-34-08); add bidirectional anchor to ctl C-schedule. |
| §3.4 dual-epsilon IPR cross-ref | 537 | "training-time softening `ε_train = 1e-5` … distinct from data-side validation `ε_inv = 1e-10` … IPR … any training-loop `IPR_train` noise-floor role (training, ε_train=1e-5, **deferred to doc-03**) …". [VERIFIED: `pinn_architecture.md:537`] | LOOP-07 cross-reference target; do not regress eps_train/eps_inv. |
| `8.5` | (none) | **`rg -n "8\.5"` returns NO match in pinn_architecture.md.** [VERIFIED: local `rg`] | LOOP-04: `8.5` already absent — preserve. |
| SI-PINN-002 item 3 (same comment) | 1002 | "3. 'Comment: This above batch construction is not consistent with the CTL instruction plan' (Section 3)" listed under SI-PINN-002 author-comment preservation log. [VERIFIED: `pinn_architecture.md:1002`] | When resolving SI-PINN-003, also reconcile this log reference so the two SI entries agree. |
| SI-PINN-003 log entry | 1005-1009 | "### SI-PINN-003: Batch construction inconsistency with CTL instruction plan … Status: Documented for future reconciliation". [VERIFIED: `pinn_architecture.md:1005-1009`] | R9: mark RESOLVED with a back-reference to the canonical ctl contract. |

## Grounding-Verification (HIGH value — SPEC/CONTEXT claims vs actual source text)

| 34-SPEC claim | Source text confirms? | Citation |
|---------------|----------------------|----------|
| §1.4 B-07 `modified`: keep 240/16, `n_pts_cap=32`, `min(n_pts_cap, n_snapshots)` without replacement, current weighted/uniform split; final-stage/undersized/replacement "must be made deterministic". | **CONFIRMED.** | `03-final-resolution.md:36-38`; claim B07-02 `modified`, B07-05 `defer` source_silent: `03-final-resolution.md:120,123`; GAP-05 (replay edge cases) defer: `03-final-resolution.md:223` |
| §1.5 B-08 `modified`: two independent point sets, single concatenated forward pass permitted (no merged loss roles), `8192/4096` provisional, mandatory 50/50 mixed continuous sampler **deferred**. | **CONFIRMED.** | `03-final-resolution.md:40-42`; GAP-06 (collocation budget/mix) defer: `03-final-resolution.md:224` |
| §1.8 M14 `modified`: `clip_value = C_stage × median(recent global gradient norms)` Adam-only, no L-BFGS clip, `5.0` = Stage-2/3 instance/fallback, preserve `7-10/5/3`, **do NOT canonize `8.5`**, bootstrap/lower-floor/history-reset OPEN. | **CONFIRMED.** Resolution doc §1.8 + M14 packet agree verbatim. | `03-final-resolution.md:52-54`; `evidence/m14-gradient-clipping.md:26,72-75,84-97`; GAP-08 defer: `03-final-resolution.md:226` |
| §1.10 M16 `defer`: `dt_out` does not establish a scaling objective/direction; keep fixed/configurable budget; do NOT adopt `dt_base/dt_out` or its inverse. | **CONFIRMED.** | `03-final-resolution.md:60-62`; M16-02 defer, M16-03 rejected: `03-final-resolution.md:144-145`; GAP-10 defer: `03-final-resolution.md:228` |
| §1.18 ALM `defer`: default loss has NO `μ_p` (dense-residual ALM rejected); clamp applies only to optional scalar-conservation ALM after the ablation defines its update law; `[1e-4,100]` + RMSprop update NOT adopted. | **CONFIRMED.** | `03-final-resolution.md:92-94`; ALM-03 defer: `03-final-resolution.md:182`; GAP-19 defer: `03-final-resolution.md:237` |
| Claim-matrix B07-04 REJECTS `pinn_architecture.md` §3.1 batch construction. | **CONFIRMED.** "B07-04 … rejected … S5::pinn_architecture.md §3.1 PIPE-04/SI-PINN-003". | `03-final-resolution.md:122` |
| M14 packet named acceptance check = AC-LOOP-04, owner Phase 34, routes the deferred constants. | **CONFIRMED.** Header AC-ID = `AC-LOOP-04`; "Owner-routed downstream details: Bootstrap … Exact early-stage `C` … Lower floor … Stage-history reset … Phase 34/FUT". | `evidence/m14-gradient-clipping.md:15,92-97,111-118` |
| Ledger: B-07/B-08/M16/ALM PENDING (no verdict, "Owner must author packet before spec edits"); M14 PENDING + `accept-resolution`; LOOP-07/08 have NO ledger row. | **CONFIRMED.** | `32-ISSUE-LEDGER.md:18-19,22,24,32`; no IPR/PSC/SASD/VAL row exists in the ledger [VERIFIED: local `rg` of ledger] |

**All eight 34-SPEC grounding claims are CONFIRMED against the actual source text. No SPEC-vs-source mismatch was found at the resolution-doc / ledger level.** The only mismatches are SPEC-vs-ROADMAP/REQUIREMENTS (see Open Questions / Findings — pre-authorized by the SPEC correction commit `0ffa3d8`, not a new gap).

## Packet Methodology (MEDIUM)

**Packet schema (reuse `evidence/_TEMPLATE.md` verbatim):** Header (ID, Title, Severity, Current Status, Current Verdict, Phase, Owner Phase, Consumer Phase, Acceptance Check ID, Spec Sections Touched, Code Paths Touched) → Source Positions (issue-doc + resolution-doc + 31-RESOLUTION-MAP line-range citations, "Neither source is authoritative") → Current Spec Evidence → Locked Convention / Dataset Evidence → FUT Hand-off Note (live `pinn/` NOT grounding) → First-Principles / Engineering Check → Verdict (one of the 5 tokens) → Root-Cause Ambiguity → Locked Convention or Owner Route → Which Source Correct/Wrong → Before/After → Named Acceptance Check → STOP/Gap Handling → Status Transition Log. [VERIFIED: `evidence/_TEMPLATE.md:5-138`]

**Ledger lifecycle (reuse exactly):** `PENDING → IN_PROGRESS → FIX_APPLIED → VERIFIED` (or `DEFERRED` with `defer-with-blocker`). `FIX_APPLIED` is never terminal; closure requires `VERIFIED` after the named acceptance check passes, or `DEFERRED` with a written blocker. Each transition recorded in BOTH the packet `Status Transition Log` and the ledger, with date, commit short SHA, and plan reference, traveling in the same commit as the change. [VERIFIED: `evidence/README.md:60-74`, `32-ISSUE-LEDGER.md:5-6`]

**Verdict enum:** `accept-resolution` / `accept-issue-doc` / `accept-third-position` / `reject-both-as-unsupported` / `defer-with-blocker`. For the four Phase-34 packets, the consumed verdicts map to: B-07 → `accept-resolution` (§1.4 modified); B-08 → `accept-resolution` (§1.5 modified); M16 → `defer-with-blocker` or `accept-resolution`-with-defer disposition (§1.10 defer); ALM → `defer-with-blocker`/defer disposition (§1.18 defer). The exact token is a packet-authoring choice that must match the consumed disposition; if a packet cannot map cleanly, that is a finding, not an invention. [VERIFIED: `evidence/README.md:46-58`, `03-final-resolution.md:36-94`]

**EVID/AC reservation scheme (do NOT mint new):** AC-LOOP-01 (B-07), AC-LOOP-02 (B-08), AC-LOOP-04 (M14/LOOP-04), AC-LOOP-05 (ALM), AC-LOOP-06 (M16) are already reserved in the ledger. LOOP-03 shares the B-08 row's AC-LOOP-02 (collocation) and the B-07 row's AC-LOOP-01 (data-fidelity split) — confirm at packet authoring; SI-PINN-003 reconciliation is verified under the batch-construction checks, not a separate ledger row. [VERIFIED: `32-ISSUE-LEDGER.md:18-19,22,24,32`]

**Filename slugs:** filesystem-safe, self-describing, lower-case, `[A-Za-z0-9_-]` only (e.g., `evidence/b-07-replay-lookahead-batching.md`, `evidence/b-08-data-vs-collocation-points.md`, `evidence/m16-dt-out-collocation-scaling.md`, `evidence/alm-mu-p-clamp.md`); map them in the ledger row. Exact slugs are planner discretion (D-34 discretion). [VERIFIED: `evidence/README.md:107-108`, `34-CONTEXT.md:240-242`]

**Confirmed PENDING / packet-before-edit:** B-07, B-08, M16, ALM-μ_p-clamp are PENDING with no verdict → packet required before any spec edit. M14 is PENDING + `accept-resolution` → LOOP-04 consumes it (no new packet). LOOP-07 (IPR/PSC) and LOOP-08 (SASD) have **no ledger row** → v1.5 carry-forwards, no packet, direct provisional transcription. [VERIFIED: `32-ISSUE-LEDGER.md:18-32`, `34-CONTEXT.md:166-174`]

## Common Pitfalls

### Pitfall 1: Re-Locking the Superseded `8.5` (the 8.5 trap)
**What goes wrong:** The plan copies REQUIREMENTS LOOP-04 / ROADMAP success-criterion 3 text ("stages 0–1: 8.5") and canonizes `8.5`. [VERIFIED: `.planning/REQUIREMENTS.md:52`, `.planning/ROADMAP.md:188`]
**Why it happens:** Those phrasings predate the SPEC correction (commit `0ffa3d8`) and the resolution-doc §1.8 explicit rejection of the midpoint. [VERIFIED: `34-CONTEXT.md:28-37`, `03-final-resolution.md:52-54`]
**How to avoid:** Preserve `7-10/5/3`; assert `8.5` ABSENT from both files. (Both files currently have NO `8.5` — preserve that.) [VERIFIED: local `rg "8\.5"` empty in both files]
**Warning signs:** Any plan/diff introduces `8.5`, or describes the early-stage `C` as `locked`.

### Pitfall 2: Transcribing the Deferred `n_col ∝ dt_base/dt_out`
**What goes wrong:** LOOP-06 is written as a transcribed/probe-able contract from the ROADMAP "verbatim direction" wording. [VERIFIED: `.planning/REQUIREMENTS.md:54`, `.planning/ROADMAP.md:189`]
**Why it happens:** ROADMAP/REQUIREMENTS still carry the preview; §1.10 `defer` supersedes. [VERIFIED: `03-final-resolution.md:60-62`, `34-SPEC.md:50-51`]
**How to avoid:** Record M16 `realized-as-deferred`; the formula appears tagged `deferred` candidate direction only; NO formula-sanity probe. [VERIFIED: `34-SPEC.md:50-51`, `34-CONTEXT.md:212-224`]
**Warning signs:** A LOOP-06 probe appears in any plan, or `n_col ∝ dt_base/dt_out` is written outside a deferred-candidate framing.

### Pitfall 3: Creating a Second SI-PINN-003 (cross-file duplication)
**What goes wrong:** The clipping mechanism (LOOP-04) or batch contract (SI-PINN-003) is copied into both files as synchronized normative text; they drift later. [VERIFIED: `34-CONTEXT.md:110-124`]
**Why it happens:** The mechanism/schedule split and the ctl-canonical/pinn-pointer split each tempt a "keep both copies in sync" approach — the exact hazard SI-PINN-003 names. [VERIFIED: `pinn_architecture.md:1005-1008`]
**How to avoid:** Single canonical home per value/formula + stable-anchor pointer (heading + AC-LOOP-04); a no-duplication verifier proves zero duplicated normative text; collapse the two ctl C-schedule locations (1792-1798 + 1909-1913) to one home. [VERIFIED: `34-SPEC.md:41`, `34-CONTEXT.md:97-115`]
**Warning signs:** The clip formula appears more than once across files; `7-10/5/3` appears as TWO independent normative copies; a cross-ref uses a line number instead of a heading anchor.

### Pitfall 4: Spec Edits Without a Linked Packet
**What goes wrong:** ctl/pinn batch, ALM, or M16 edits land without the B-07/B-08/ALM/M16 packet + ledger row. [VERIFIED: `32-ISSUE-LEDGER.md:34-36`]
**Why it happens:** Phase 32 seeded these rows PENDING for downstream ownership; the packet is the owner's job. [VERIFIED: `32-ISSUE-LEDGER.md:18-32`]
**How to avoid:** Packet-before-edit as the first wave; each spec edit cites its packet. LOOP-04 cites the existing M14 packet; LOOP-07/08 need none. [VERIFIED: `34-CONTEXT.md:150-174`]
**Warning signs:** A plan's first edit action targets `ctl_instruction.md`/`pinn_architecture.md` before referencing the ledger + an `evidence/` packet path.

### Pitfall 5: Regressing the Raw-Mass `D` / Locked Conventions
**What goes wrong:** A batch/loss/clip edit reintroduces `D = 6.694` or disturbs 14D `[τ,IC₁₃]`, the Jacobi COM head, `eps_soft=1e-5`, the SCS gate, or PIPE/VAL references. [VERIFIED: `.planning/REQUIREMENTS.md:16`, `33-RESEARCH.md:302-310`]
**How to avoid:** Run the locked-convention regression guard after every batch: `D≈4.6416` present / `6.694` absent / 14D input / COM head / `eps_soft=1e-5` / SCS gate / PIPE-01..10 / VAL-01..04 intact. [VERIFIED: `34-SPEC.md:102`, `34-CONTEXT.md:222-223`]
**Warning signs:** Any diff contains `6.694` outside a rejection/provenance note.

### Pitfall 6: UI-Gate False Positive
**What goes wrong:** The ui-plan-gate reports `frontend=true` and planning tries to create a UI spec / frontend tasks. [VERIFIED: `34-SPEC.md` edge coverage; `33-RESEARCH.md:312-320`]
**Why it happens:** Documented false positive for Markdown-only specwork (Phase 33 Pitfall 5). [VERIFIED: additional_context; `33-RESEARCH.md:312-320`]
**How to avoid:** Treat as a false positive; proceed without UI scope (use `--skip-ui` if the gate blocks). No frontend files, UI acceptance criteria, or visual review.
**Warning signs:** A Phase-34 plan includes any UI/frontend artifact.

### Pitfall 7: Opening a `34-GAPS.md` Entry for Source-Routed Constants
**What goes wrong:** The M14-deferred constants (early-`C`, bootstrap, lower floor, history-reset) are logged as a STOP gap, polluting the register. [VERIFIED: `34-CONTEXT.md:206-211`]
**Why it happens:** They look "unfilled", but M14 / §1.8 / GAP-08 explicitly ROUTE them to Phase 34/FUT — they are source-routed, not source-silent. [VERIFIED: `evidence/m14-gradient-clipping.md:92-97`, `03-final-resolution.md:226`]
**How to avoid:** Carry them as `deferred → FUT` in the LOOP-04 body citing the M14 owner-route + §1.8; NO `34-GAPS.md` entry. Reserve `34-GAPS.md` for the genuinely source-silent batch edge cases (D-34-16a). [VERIFIED: `34-CONTEXT.md:200-211`]
**Warning signs:** A `34-GAPS.md` entry references early-`C`/bootstrap/floor/history-reset.

### Pitfall 8: Inventing the Batch Edge-Case Policy
**What goes wrong:** Final-stage (`has_stage(k+1)`=false), undersized next-stage lookahead pool (<16), or replacement policy are filled with an invented default. [VERIFIED: `34-SPEC.md:111`, `03-final-resolution.md:38`]
**Why it happens:** B-07 §1.4 flags them "must be made deterministic" but gives NO policy (GAP-05 defer). [VERIFIED: `03-final-resolution.md:223`]
**How to avoid:** Record as a `34-GAPS.md` STOP gap + `v1.6-GAPS.md` index, owner-pending/deferred (D-34-16a); do NOT invent. [VERIFIED: `34-CONTEXT.md:200-205`]
**Warning signs:** A deterministic final-stage/undersized/replacement policy appears in the contract body without an owner decision.

## Code Examples

Verified local patterns for planner/executor commands (deterministic source checks — no runtime training).

### LOOP-04 cross-file consistency check — `8.5` absent / `7-10 5 3` present
```bash
# Source: 34-SPEC LOOP-04 acceptance (a)-(e); D-34-04.
python3 -c "
from pathlib import Path
ctl=Path('pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md').read_text()
pinn=Path('pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md').read_text()
assert '8.5' not in ctl and '8.5' not in pinn, '8.5 must be absent from both files'
assert '7-10' in ctl or '7--10' in ctl, '7-10 C-schedule must remain in ctl'
print('LOOP-04 8.5-absent / 7-10-present OK')
"
```

### No-duplication check — clip formula has exactly one canonical home
```bash
# Source: D-34-04 win condition (zero duplicated normative text).
# Count canonical clip-formula occurrences per file; mechanism canonical = pinn §4.4 only.
rg -n "clip_value\s*=\s*C_stage" pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md \
  && echo "WARN: clip mechanism formula found in ctl (should be a pointer, not a copy)" || echo "ctl carries no mechanism copy: OK"
rg -c "clip_value\s*=\s*C_stage" pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md
```

### Locked-convention regression guard
```bash
# Source: SCOPE-12 hard constraints; 34-SPEC acceptance.
python3 -c "
from pathlib import Path
for f in ['ctl_instruction.md','pinn_architecture.md']:
    t=Path('pinn_instruction/markdown_conversion/framework-specs/'+f).read_text()
    assert '6.694' not in t, f+': 6.694 must be absent'
print('no 6.694 in either file OK')
"
rg -n "4.6416" pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md
```

### Forbidden-path scope guard
```bash
# Source: SCOPE-13 + D-34-18 (STATE.md user-owned). Expect ONLY ctl + pinn (+ .planning/phases/34-*) changed.
git diff --name-only -- \
  pinn_instruction/markdown_conversion/framework-specs/sampling_method.md \
  pinn_instruction/markdown_conversion/framework-revisions/ \
  pinn/ simulation_data/ .planning/STATE.md
# Expected output: empty.
```

### Requirements-to-plan coverage check
```bash
# Source: D-34 discretion (every LOOP + SI-PINN-003 in a plan requirements field).
python3 -c "
from pathlib import Path
root=Path('.planning/phases/34-training-loop-batch-construction-contracts')
plans=list(root.glob('34-*-PLAN.md'))
text='\n'.join(p.read_text() for p in plans)
req=['LOOP-01','LOOP-02','LOOP-03','LOOP-04','LOOP-05','LOOP-06','LOOP-07','LOOP-08','SI-PINN-003']
missing=[r for r in req if r not in text]
assert plans,'no plans found'; assert not missing, missing
print('all 9 requirements present in plans')
"
```

## State of the Art

| Old (superseded) Approach | Current (adjudicated) Approach | When Changed | Impact |
|---------------------------|--------------------------------|--------------|--------|
| Lock `C_table` stages 0-1 = `8.5` (REQUIREMENTS LOOP-04 / ROADMAP crit 3). | Lock only the structural merge; preserve `7-10/5/3`; `8.5` rejected/absent; early-`C` deferred → FUT. | resolution-doc §1.8 + SPEC commit `0ffa3d8`. [VERIFIED: `03-final-resolution.md:52-54`, `34-CONTEXT.md:28-37`] | Prevents canonizing an ungrounded midpoint. |
| Transcribe `n_col ∝ dt_base/dt_out` provisional (REQUIREMENTS LOOP-06 / ROADMAP crit 4). | M16 `defer`; formula = deferred candidate direction only, NOT transcribed, NOT probe-able; v1.5 SCOPE-11/PIPE-08 realized-as-deferred. | resolution-doc §1.10 + SPEC commit `0ffa3d8`. [VERIFIED: `03-final-resolution.md:60-62`] | Prevents adopting an unsupported scaling objective. |
| Mixed 50/50 sampling "applied to BOTH point sets" (REQUIREMENTS LOOP-03 / ROADMAP crit 2). | Data-fidelity 50/50 retained; collocation 50/50 deferred (not mandated). | resolution-doc §1.5 B-08 modified. [VERIFIED: `03-final-resolution.md:40-42`] | Avoids mandating an unvalidated continuous sampler. |
| ALM update + `μ_p` clamp `[1e-4,100]` into the loop (REQUIREMENTS LOOP-05). | Dense-residual ALM rejected from default loss; ALM optional scalar-only; clamp deferred/conditional. | resolution-doc §1.18. [VERIFIED: `03-final-resolution.md:92-94`] | Keeps the default training step ALM-free. |

**Deprecated/outdated:** ROADMAP success criteria (lines 186-190) and REQUIREMENTS LOOP-03/04/05/06 (lines 51-54) carry the pre-adjudication previews; `34-SPEC.md` + `03-final-resolution.md` + `32-ISSUE-LEDGER.md` govern where they diverge. [VERIFIED: `.planning/ROADMAP.md:186-190`, `.planning/REQUIREMENTS.md:51-54`, `34-SPEC.md:38-51`]

## Assumptions Log

No `[ASSUMED]` claims. All substantive recommendations trace to internal project artifacts with file:line citations or local tool probes. [VERIFIED: local research process; zero web calls per CRITICAL_GOVERNANCE]

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| none | n/a | n/a | n/a |

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | No dedicated test framework; deterministic `rg`, `python3 -c` token/negative-token/duplication assertions, git protected-path checks, + disposable formula-sanity probes (D-34-17). NOT runtime training tests. [VERIFIED: `34-CONTEXT.md:355-358`, `.planning/config.json:11` `nyquist_validation: true`] |
| Config file | none for Phase 34; `.planning/config.json` `workflow.nyquist_validation: true`, `commit_docs: true`. [VERIFIED: `.planning/config.json:5,11`] |
| Quick run command | `rg -n "LOOP-0[1-8]\|SI-PINN-003" .planning/phases/34-*/34-*-PLAN.md` (coverage) + the LOOP-04 `8.5`-absent check. [VERIFIED: `34-SPEC.md:94-103`] |
| Full suite command | Per-plan `python3 -c` token + negative-token + no-duplication checks, the LOOP-04 (a)-(e) consistency suite, the locked-convention regression guard, and the forbidden-path scope guard. [VERIFIED: `34-SPEC.md:94-103`] |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|--------------|
| LOOP-01 | Replay/lookahead provisional contract; `min(n_pts_cap, n_snapshots)`; edge-case gap recorded. | source-token + **formula-sanity probe** (D-34-17) | `python3 -c "t=open('pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md').read_text(); assert 'min(n_pts_cap' in t.replace(' ',''.join([])) or 'min(n_pts_cap, n_snapshots' in t; assert 'has_stage' in t"` + probe `min(32, n)` on sample snapshot counts | ❌ embed in plan |
| LOOP-02 | Two-independent-point-set + single-forward-pass + `8192/4096` provisional. | source-token (structural) | `python3 -c "t=open('...ctl_instruction.md').read_text(); assert 'collocation' in t and 'data-fidelity' in t.lower() or 'data fidelity' in t.lower()"` | ❌ embed in plan |
| LOOP-03 | Data-fidelity 50/50 retained; collocation 50/50 deferred. | source-token + negative-token + **probe** (data 50/50 only) | assert ctl states `50/50` retained for data points AND `deferred` for collocation; probe `k_w=floor(n/2)` split sums to `n` on a sample | ❌ embed in plan |
| LOOP-04 | Mechanism canonical pinn §4.4 once; `7-10/5/3` ctl once; `8.5` absent both; bidirectional anchors; no duplication; tags agree. | source-token + negative-token + duplication + **probe** | LOOP-04 (a)-(e) suite (see Code Examples) + probe `clip_value=C_stage*median(hist)` on a sample grad-norm history | ❌ embed in plan; **re-run (c)/(d)/(e) after every batch** |
| LOOP-05 | ALM optional/deferred; `μ_p` clamp `[1e-4,100]` carried deferred; default loop excludes dense-residual ALM. | source-token + negative-token (NO probe) | assert pinn §4.2 "Default: ALM is OFF" + ctl skeleton ALM step marked optional/deferred; assert no dense-residual ALM in default loop | ❌ embed in plan |
| LOOP-06 | M16 realized-as-deferred; `n_col ∝ dt_base/dt_out` deferred candidate only; inverse not adopted. | source-token + negative-token (**NO probe**) | assert `deferred` + `realized-as-deferred` present; assert no probe-able `n_col` formula transcribed | ❌ embed in plan |
| LOOP-07 | IPR (`1e-3`) + PSC training-side roles provisional; VAL-03/04 cited; recalibration FUT. | source-token (structural; carried not recalibrated) | assert ctl IPR `1e-3` + PSC role present + `provisional` + `VAL-03`/`VAL-04` + `doc-03`/FUT | ❌ embed in plan |
| LOOP-08 | SASD training-side collocation-weighting role provisional; NO weighting formula. | source-token + negative-token | assert SASD role + `provisional` + `VAL-02`; assert no invented weighting formula | ❌ embed in plan |
| SI-PINN-003 | pinn §3.1 references canonical ctl; author comment removed; SI-PINN-003 log RESOLVED. | source-token + negative-token | assert author comment string ABSENT from pinn §3.1; assert SI-PINN-003 log marked RESOLVED with back-reference; assert pinn points to ctl Mini-Batch | ❌ embed in plan |

### Sampling Rate

- **Per task commit:** task-local source-token + negative-token checks + `git diff --name-only` forbidden-path guard. [VERIFIED: `34-SPEC.md:103`]
- **Per wave / per batch:** full requirement-token suite + **LOOP-04 (c)/(d)/(e) re-verify-after-every-batch** + locked-convention regression guard. [VERIFIED: `34-SPEC.md:41`, `34-CONTEXT.md:389-391`]
- **Phase gate:** all 9 requirement checks green + ledger rows `VERIFIED`/`DEFERRED` + forbidden-path scope clean before `gsd-verify-work`; no EDA / Stage-0 pilot / training implementation. [VERIFIED: `.planning/REQUIREMENTS.md:94-95`]

### Disposable formula-sanity probes (SCOPE-15 — D-34-17, EXHAUSTIVE list)

- **LOOP-01:** `min(n_pts_cap, n_snapshots)` on sample snapshot counts. [VERIFIED: `34-CONTEXT.md:215`]
- **LOOP-03:** the retained data-fidelity 50/50 split (`k_w = floor(n_pts/2)` + uniform remainder sums to `n_pts`) on a sample. [VERIFIED: `34-CONTEXT.md:216`]
- **LOOP-04:** `clip_value = C_stage · median(recent grad norms)` on a sample grad-norm history. [VERIFIED: `34-CONTEXT.md:217-219`]
- **NO probe:** LOOP-05 (deferred), LOOP-06 (deferred — NO `n_col` probe), LOOP-08 (deferred). LOOP-02 / LOOP-07 = structural grep only (IPR `1e-3` / PSC grid carried, not recalibrated). [VERIFIED: `34-CONTEXT.md:218-224`]

### Wave 0 Gaps

- [ ] No dedicated Phase-34 validation script exists; each plan embeds deterministic `rg`/`python3 -c` commands + the LOOP-04 (a)-(e) suite. [VERIFIED: local file scan]
- [ ] No `evidence/` subdirectory exists under the Phase-34 directory; create it mirroring the Phase-32 packet schema before authoring B-07/B-08/M16/ALM. [VERIFIED: local `ls`]
- [ ] No `34-GAPS.md` exists; create it on the first STOP gap (the batch edge-case gap, D-34-16a is anticipated). [VERIFIED: local `ls`]

## Open Questions / Findings for Parent Triage

> The four items below are SPEC-vs-ROADMAP/REQUIREMENTS divergences. The brief pre-authorized treating the SPEC + resolution doc as governing and flagging the ROADMAP/REQUIREMENTS wording as a FINDING (not a fix). **None is a new source-silent semantic gap** — each is the *known, already-adjudicated* preview→verdict supersession that SPEC commit `0ffa3d8` corrected; the stale text lives in downstream tracking docs that the SPEC explicitly overrides. They are reported for the parent orchestrator to decide whether the ROADMAP/REQUIREMENTS text should be reconciled (likely a separate housekeeping task, possibly Phase 36), NOT for Phase 34 to silently edit (those files are outside SCOPE-13).

1. **REQUIREMENTS.md LOOP-04 (line 52) + ROADMAP success-criterion 3 (line 188) still say `C_table` stages 0-1 = `8.5`.** The adjudicated outcome (resolution-doc §1.8, M14 packet, `34-SPEC.md:40`) rejects `8.5` and preserves `7-10/5/3`. **Finding:** the tracking docs carry the superseded preview. Phase 34 transcribes the SPEC, not these lines. [VERIFIED: `.planning/REQUIREMENTS.md:52`, `.planning/ROADMAP.md:188`, `03-final-resolution.md:52-54`]

2. **REQUIREMENTS.md LOOP-06 (line 54) + ROADMAP success-criterion 4 (line 189) still say "`n_col ∝ dt_base/dt_out` … verbatim direction … transcribed".** §1.10 `defer` supersedes; the formula is NOT transcribed, NOT probe-able. **Finding:** superseded preview in tracking docs. [VERIFIED: `.planning/REQUIREMENTS.md:54`, `.planning/ROADMAP.md:189`, `03-final-resolution.md:60-62`]

3. **REQUIREMENTS.md LOOP-03 (line 51) + ROADMAP success-criterion 2 (line 187) still say mixed 50/50 "applied to both point sets".** §1.5 defers the collocation 50/50; only data-fidelity 50/50 is retained. **Finding:** superseded preview in tracking docs. [VERIFIED: `.planning/REQUIREMENTS.md:51`, `.planning/ROADMAP.md:187`, `03-final-resolution.md:40-42`]

4. **REQUIREMENTS.md LOOP-05 (line 53) states the ALM `μ_p` clamp `[1e-4,100]` + RMSprop update as the contract** without the "default-loss-excludes-it / optional-scalar-only" framing. §1.18 `defer` makes it optional/deferred, not a default-loop contract. **Finding:** the REQUIREMENTS phrasing under-specifies the deferred status; `34-SPEC.md:43-46` carries the corrected framing. [VERIFIED: `.planning/REQUIREMENTS.md:53`, `03-final-resolution.md:92-94`, `34-SPEC.md:45`]

**No source-silence or resolution-doc/ledger mismatch was found.** The eight 34-SPEC grounding claims all CONFIRM against the actual source text (see Grounding-Verification). The one *anticipated* genuine STOP gap during execution is the source-silent batch edge-case policy (final-stage / undersized-lookahead / replacement), which the SPEC already classifies as a deferred contract gap (D-34-16a → `34-GAPS.md`); it is NOT a planning-time blocker.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|-------------|-----------|---------|----------|
| `rg` | source-token / forbidden-path / duplication checks | ✓ | 15.1.0 [VERIFIED: local] | `grep -r` / Python text search (lower confidence) |
| `python3` | parser-backed assertions + formula-sanity probes | ✓ | 3.14.5 [VERIFIED: local] | POSIX shell for simple tokens (lower confidence) |
| `git` | status / forbidden-path guards | ✓ | 2.54.0 [VERIFIED: local] | none for git-state policy |
| `scripts/agent-commit` | later execution commits, if authorized | ✓ | executable [VERIFIED: `33-RESEARCH.md:159`] | no raw `git commit`; stop if unavailable and commit required |

**Missing dependencies with no fallback:** None for Phase 34 planning/execution. [VERIFIED: local tool probes]
**Missing dependencies with fallback:** None material; `pytest` not required (specwork uses deterministic source checks). [VERIFIED: `33-RESEARCH.md:408`]

## Security Domain

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|------------------|
| V2 Authentication | no | No auth surface; specwork-only docs. [VERIFIED: `34-SPEC.md:68-83`] |
| V3 Session Management | no | No session surface. |
| V4 Access Control | yes (repository write boundary) | Explicit allowed/forbidden paths + git status guards (SCOPE-13; STATE.md user-owned). [VERIFIED: `34-SPEC.md:103`, `34-CONTEXT.md:228-232`] |
| V5 Input Validation | yes (source-input discipline) | Line-range citations, source hierarchy, packet/verdict linkage, token checks. [VERIFIED: `evidence/README.md:34-44`] |
| V6 Cryptography | no | No cryptographic feature or secret handling. |

### Known Threat Patterns for Specwork

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Silent semantic default (invented edge-case policy / re-locked `8.5`) | Tampering | STOP protocol + gap register before dependent edits; negative-token checks. [VERIFIED: `34-CONTEXT.md:200-211`] |
| Unauthorized file modification (frozen/read-only specs, `pinn/`, STATE.md) | Tampering | Protected-path `git diff --name-only` guard. [VERIFIED: `34-SPEC.md:103`] |
| Evidence provenance confusion | Repudiation | Evidence packets with line ranges + ledger links. [VERIFIED: `32-ISSUE-LEDGER.md:34-36`] |
| Cross-file drift (second SI-PINN-003) | Tampering | Single canonical home + no-duplication verifier. [VERIFIED: `34-CONTEXT.md:110-124`] |
| Treating live code / stale ROADMAP as authority | Tampering | Ban live `pinn/` grounding; SPEC/resolution-doc govern over ROADMAP. [VERIFIED: `AGENTS.md`; `34-CONTEXT.md:28-37`] |

## Sources

### Primary (HIGH confidence)
- `.planning/phases/34-training-loop-batch-construction-contracts/34-SPEC.md` — locked requirements, boundaries, acceptance, edge coverage. [VERIFIED: local read]
- `.planning/phases/34-training-loop-batch-construction-contracts/34-CONTEXT.md` — D-34-01..18 implementation decisions. [VERIFIED: local read]
- `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md` — §1.4/1.5/1.8/1.10/1.18 verdicts + claim matrix (B07-04) + gap register (GAP-05/06/08/10/19). [VERIFIED: local read]
- `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md` — B-07/B-08/M14/M16/ALM rows; packet-before-edit mandate; LOOP-07/08 have no row. [VERIFIED: local read]
- `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence/m14-gradient-clipping.md` — M14 `accept-resolution`, AC-LOOP-04, GAP-08 routing. [VERIFIED: local read]
- `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence/_TEMPLATE.md` + `evidence/README.md` — packet schema + lifecycle. [VERIFIED: local read]
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` — current-state survey (real line numbers). [VERIFIED: local read + `rg -n`]
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` — current-state survey (real line numbers). [VERIFIED: local read + `rg -n`]
- `.planning/REQUIREMENTS.md` — LOOP-01..08, SCOPE-12..15, EVID-11..15, VER-13..18 (+ superseded LOOP-03/04/05/06 preview wording). [VERIFIED: local `rg`]
- `.planning/ROADMAP.md` — Phase 34 goal + success criteria (+ superseded preview positions). [VERIFIED: local `rg`]
- `AGENTS.md` / `CLAUDE.md` + `.claude/rules/*` — v1.6 STOP protocol, source hierarchy, SCOPE-12..15, commit protocol. [VERIFIED: system context + local rules]
- `.planning/phases/33-curriculum-stage-contracts/33-RESEARCH.md` — section-structure + pitfalls precedent mirrored here. [VERIFIED: local read]

### Secondary (MEDIUM confidence)
- None. No external web/package documentation was used; this is an internal-grounded specwork phase under the v1.6 STOP protocol (zero web calls). [VERIFIED: research process]

### Tertiary (LOW confidence)
- None.

## Metadata

**Confidence breakdown:**
- Current-state survey: HIGH — real line numbers + verbatim quotes from `Read`/`rg` this session. [VERIFIED: local]
- Grounding-verification: HIGH — all eight 34-SPEC claims cross-checked against actual source text; all CONFIRMED. [VERIFIED: local]
- Packet methodology: HIGH — Phase-32 template/README + ledger reused verbatim. [VERIFIED: `evidence/README.md`, `evidence/_TEMPLATE.md`]
- Validation architecture / pitfalls: HIGH — grounded in 34-SPEC/34-CONTEXT, the resolution doc, and Phase-33 precedent. [VERIFIED: local]

**Research date:** 2026-06-24
**Valid until:** 2026-07-24, unless 34-SPEC/34-CONTEXT, the Phase-32 ledger/M14 packet, the resolution doc, or v1.6 governance change first. [VERIFIED: local research date + active planning artifacts]
