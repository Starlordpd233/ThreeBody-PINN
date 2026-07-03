# Phase 34: Training-Loop & Batch-Construction Contracts - Context

**Gathered:** 2026-06-24
**Status:** Ready for planning
**Mode:** `/gsd-discuss-phase 34 --all`

<domain>
## Phase Boundary

Phase 34 transcribes the training-loop and batch-construction contracts
(LOOP-01..08 + SI-PINN-003) into `ctl_instruction.md` and `pinn_architecture.md`
as **normative spec contracts**, each at its **adjudicated verdict and status**
(locked / provisional / deferred / owner-pending) with source citations. It is
specwork-only: no training-loop code, no DataLoader/ALM/causal-window mechanics,
no EDA/Stage-0 pilot, no recalibration. Phase 34 consumes the Phase 33 curriculum
contracts and the Phase 32 issue-ledger verdicts; it does not re-decide them.

</domain>

<spec_lock>
## Requirements (locked via SPEC.md)

**9 requirements are locked.** See `34-SPEC.md` for full requirements,
boundaries, edge coverage, prohibitions, and acceptance criteria. Downstream
agents MUST read `34-SPEC.md` before planning or implementing. Requirements are
not duplicated here.

> **SPEC corrected during this discussion (commit `0ffa3d8`).** Two requirements
> had transcribed issue-doc *preview* positions ahead of the adjudicated
> verdicts; both were reconciled on explicit user instruction:
> - **LOOP-04** — was "lock `C_table` = 8.5/5.0/3.0"; now locks only the M14
>   structural merge, preserves `7-10/5/3`, does NOT canonize `8.5`, defers exact
>   early-stage `C`/bootstrap/floor/history-reset to FUT, and carries the
>   single-canonical-home cross-file SPEC-CONSISTENCY check.
> - **LOOP-06** — was "transcribe `n_col ∝ dt_base/dt_out` provisional"; now
>   records the M16 §1.10 `defer` (formula NOT transcribed, no probe;
>   realized-as-deferred).

**In scope (from SPEC.md):**
- Transcribing LOOP-01..08 into `ctl_instruction.md` and `pinn_architecture.md`
  as normative spec contracts, each at its adjudicated verdict + status with
  source citations.
- Reconciling SI-PINN-003 with `ctl_instruction.md` canonical (R9).
- The per-step total-loss **assembly skeleton** (where `L_total` enters
  backward → gradient-clip → optimizer.step → optional ALM), treating loss terms
  as opaque inputs with a Phase-35 forward-reference.
- Recording the source-silent batch-construction edge cases (final stage,
  undersized lookahead, replacement policy) as a documented deferred/owner-pending
  contract gap (candidate `34-GAPS.md`).
- Disposable formula-sanity probes (SCOPE-15) only.

**Out of scope (from SPEC.md):**
- Loss-component scaling, the `λ_E` schedule, Huber-δ calibration, and the
  causal-training-mode selection — Phase 35 (forward-reference only).
- Curriculum-stage definitions / `tau_L` / `L_max` / stage-transition state
  machine — locked by Phase 33; Phase 34 consumes, does not re-decide.
- Any FUT-01/FUT-04 implementation — DataLoader, batch constructor, ALM update
  mechanics, causal-window mechanics (SCOPE-14: contracts only, no code).
- The adaptive-stage-assignment EDA, Stage-0 pilot, threshold calibration
  (SCOPE-15).
- Editing `sampling_method.md` (frozen, SCOPE-08), `data_quality_assessment.md`,
  `review-of-framework.md`, `stage-strat-revision.md` (read-only, SCOPE-09), or
  any `pinn/` live code.
- Re-adjudicating D-04 / D-05 / D-06 / M14 / the D-value conflict — locked by
  Phase 32; the issue ledger is canonical.

</spec_lock>

<decisions>
## Implementation Decisions

### Fidelity & grounding corrections (the central pattern)

- **D-34-01:** Transcribe each LOOP contract at its **adjudicated verdict +
  status** with source citations — NEVER the issue-doc "preview" proposal. This
  discussion grounding-verified the SPEC against the Phase 32 ledger and caught
  two preview→verdict mismatches, both corrected in `34-SPEC.md` (commit
  `0ffa3d8`). The planner must transcribe the corrected SPEC, not any earlier
  proposal wording.
- **D-34-02 (LOOP-04 / M14):** Follow the Phase 32 M14 `accept-resolution`
  verdict. Lock ONLY the structural merge `clip_value = C_stage · median(recent
  global gradient norms)` (Adam-only; no L-BFGS clipping; rolling window).
  **Preserve `7-10 / 5 / 3`**; treat `5.0` as the Stage-2/3 instance/fallback.
  **Do NOT canonize `8.5`** (M14 + resolution-doc §1.8 reject the midpoint). The
  exact early-stage `C`, bootstrap median fallback, lower floor (`1e-6`), and
  history-reset mechanics are **deferred → Phase 34/FUT** in the contract body,
  citing the M14 packet owner-route + §1.8 (GAP-08). This is NOT a STOP gap — the
  source explicitly routes these.
- **D-34-03 (LOOP-06 / M16):** Follow the M16 §1.10 `defer` verdict. Record the
  deferral; `n_col ∝ dt_base/dt_out` is the **deferred candidate direction only**
  (NOT transcribed as a locked or probe-able contract); the inverse form is not
  adopted; the v1.5 SCOPE-11/PIPE-08 forward-reference is **realized-as-deferred**.
  M16 has no Phase-32 verdict — confirm `defer` against §1.10 at packet-authoring.

### Cross-file split & placement — the SI-PINN-003-prevention guardrail

- **D-34-04 (LOOP-04 split, SCOPE-13):** The merged-clipping **mechanism** is
  stated EXACTLY ONCE, canonical in `pinn_architecture.md` §4.4; the per-stage
  **C-schedule** (`7-10/5/3`) is stated EXACTLY ONCE in `ctl_instruction.md`. The
  two current ctl locations (prose ~1786-1798 and the Consolidated Hyperparameter
  table ~1909-1913) **collapse to one canonical schedule statement**; the other
  carries values with a pointer, never an independent normative copy. Each file
  names the other for the half it does not own via **bidirectional stable-anchor
  cross-references** (section heading + `AC-LOOP-04`, NEVER line numbers).
  **Status-tag parity** across halves (structure `locked`; exact C / bootstrap /
  floor / history-reset `deferred`/owner-pending; neither file tags the
  early-stage value `locked`). **Win condition:** the merged contract is
  recoverable as one coherent rule from the two cross-referenced halves with
  **zero duplicated normative text** — not merely "8.5 removed / 7-10/5/3 present".
  This guardrail exists because the mechanism/schedule split could itself become
  a second SI-PINN-003; the key move is *single canonical home per value/formula*
  + a verifier that *proves no duplication* (a bidirectional arrow alone does not
  stop drift). Encoded as the disposable SPEC-CONSISTENCY check (a)–(e) in
  `34-SPEC.md` LOOP-04 acceptance; re-run after every Phase-34 batch and at
  Phase 36.
- **D-34-05 (SI-PINN-003 / R9):** `ctl_instruction.md` Mini-Batch Construction is
  **canonical** for batch construction (SCOPE-13; resolution-doc claim matrix
  **B07-04 rejects** the `pinn_architecture.md` §3.1 batch construction). In pinn
  §3.1: remove the author comment (line 351, now resolved-and-false), replace the
  Listing-2 batch description with a **pointer extending the existing PIPE-04
  note** (line 352), and mark SI-PINN-003 (line 1005) RESOLVED with a
  back-reference to the canonical ctl contract. A verifier confirms the two files
  agree on batch construction. Reject two-synchronized-copies (that is the very
  hazard SI-PINN-003 names).
- **D-34-06:** D-34-04 (clipping split) and D-34-05 (batch construction) follow
  the SAME anti-duplication discipline — single canonical home + pointer, no
  duplicated normative rule text.

### Transcription conventions

- **D-34-07:** Reuse the Phase-33 blockquote-callout convention **verbatim** for
  LOOP-01..08: `> **Phase 34 contract: <name> (LOOP-NN; <verdict>; AC-NN;
  grounded by <source>).**` with an inline status tag
  (locked/provisional/deferred/owner-pending) and a grounded-by citation —
  file-internal consistency with the CURR callouts at `ctl_instruction.md`
  lines 1630 and 1832.
- **D-34-08:** Any transcribed pseudocode (the verbatim audit "Section 6" batch
  construction, etc.) is rendered in a fenced block **explicitly labeled
  "normative spec contract — not executable; FUT-01/FUT-04 implements"**
  (SCOPE-14).
- **D-34-09 (bounded allowance):** For pure-deferral / owner-pending contracts or
  sub-parts (LOOP-03 collocation-50/50, LOOP-05 ALM-in-default-loss, LOOP-06 M16,
  LOOP-08 SASD), the callout uses the deferred/owner-pending status tag and
  records the deferral + forward-reference **in the body instead of a pseudocode
  block** — same convention, status-driven body. This is the ONLY adaptation; do
  not otherwise restructure.

### Adjudication: packet-before-edit & ledger lifecycle

- **D-34-10:** Only **M14 is pre-adjudicated** (Phase 32). **B-07 (LOOP-01),
  B-08 (LOOP-02/03), M16 (LOOP-06), ALM-μ_p-clamp (LOOP-05)** are seeded PENDING
  with no verdict — Phase 34 authors **one evidence packet per finding** in a
  Phase-34 `evidence/` dir (EVID-11/12), **before any spec edit**, then closes
  each ledger row `PENDING → IN_PROGRESS → FIX_APPLIED → VERIFIED` with packet
  link + AC ID. Use the existing EVID/AC reservation scheme — do NOT mint a new
  ID schema. (Phase 32 D-04 "no umbrella packet" + Phase 33 precedent.) This
  sequencing is what prevents transcribing a "preview" verdict as locked — the
  failure mode caught in LOOP-04's 8.5.
- **D-34-11:** Packets **consume** the resolution-doc verdicts (**§1.4 B-07
  modified; §1.5 B-08 modified; §1.10 M16 defer; §1.18 ALM defer**) — formalize
  each into the ledger (packet + AC + state transitions); do NOT re-litigate. The
  packet's job is traceability: issue-doc citation + resolution-doc verdict +
  current-spec evidence + locked-convention check. **If a packet surfaces a NEW
  conflict** (e.g., a v1.5-verified fact contradicting the resolution-doc verdict),
  STOP per EVID-15 and record a `34-GAPS.md` gap; otherwise consume and transcribe.
- **D-34-12:** LOOP-04 **consumes the existing M14 verdict** — no new M14 packet.

### LOOP-07 / LOOP-08 (v1.5 forward-references, not issue-03 findings)

- **D-34-13:** LOOP-07 (IPR/PSC) and LOOP-08 (SASD) are **v1.5 carry-forwards**
  (VAL-02/03/04 left provisional with doc-03 forward-refs), NOT issue-03 findings
  — no ledger row, no adjudication packet, no conflict to resolve. **Direct
  transcription** of the training-side roles tagged `provisional` with VAL-02/03/04
  citations; recalibration is FUT (SCOPE-15), explicitly not done in-phase.
- **D-34-14:** VERIFY each training-side role against the v1.5 contracts + existing
  spec text: IPR-as-ALM-convergence/noise-floor (provisional `1e-3` carried);
  PSC-for-replay-buffer-governance (provisional grid/normalization/SCR carried);
  SASD-collocation-weighting. Source establishes the role → transcribe provisional.
  Source **silent** on a specific role → that is a `34-GAPS.md` STOP gap
  (owner-pending), NOT an invented transcription. Keep LOOP-08 (SASD training-side
  collocation weighting) consistent with the M16 deferral — record the
  deferred/provisional role + VAL-02 / M16 citation, **NO weighting formula** (same
  discipline as LOOP-06). Default = no packet; if transcription surfaces a
  v1.5-vs-current-spec CONFLICT on a role → packet + EVID-15.

### Total-loss assembly skeleton (LOOP boundary with Phase 35)

- **D-34-15:** **Augment** the existing `ctl_instruction.md` Total-Loss / Data-Flow
  section (~1718-1745) with the per-step **ordering skeleton** (forward → `L_total`
  assembly → backward → Adam-only median-clip → optimizer.step → optional
  scalar-ALM). Ordering skeleton ONLY: loss terms stay **opaque** with a Phase-35
  forward-reference — do NOT define or rewrite loss components, `λ_E`, or Huber-δ
  (the 34↔35 boundary); do not disturb the existing PHYS-05 forward-refs. The clip
  step **cross-references** the canonical merged-clipping mechanism (pinn §4.4, per
  D-34-04); the ALM step is marked **optional/deferred** (LOOP-05). Reject a new
  separate subsection (fragments the training-step narrative).

### Source-silent routing & probe scope

- **D-34-16:** Two distinct classes — handle differently:
  - **(a) batch edge cases** (final-stage `has_stage(k+1)`=false, undersized
    next-stage lookahead pool `<16`, replacement policy): genuinely
    **SOURCE-SILENT** — B-07 §1.4 flags them "must be made deterministic" but gives
    no policy. Record as a **`34-GAPS.md` STOP gap + `v1.6-GAPS.md` index**,
    owner-pending/deferred, NOT invented (Phase-33 GAP-33-0x precedent + the SPEC
    edge-coverage table).
  - **(b) M14-deferred constants** (exact early-`C`, bootstrap floor, lower floor,
    history-reset): **NOT source-silent** — M14 explicitly routes them to
    Phase 34/FUT. Record as **deferred → FUT in the LOOP-04 contract body** citing
    the M14 packet owner-route + §1.8 (GAP-08). **No new `34-GAPS.md` entry** (the
    source already routed them; a STOP entry would pollute the register).
- **D-34-17 (probe scope, SCOPE-15 — disposable formula-sanity ONLY):** Probe ONLY
  the contracts transcribed as **locked formulas**:
  - LOOP-01: `min(n_pts_cap, n_snapshots)` on sample snapshot counts;
  - LOOP-03: the retained data-fidelity 50/50 split on a sample;
  - LOOP-04: `clip_value = C_stage · median(recent grad norms)` on a sample
    grad-norm history.
  LOOP-05 / 06 / 08 = **deferred** (record the deferral, NO probe). LOOP-02 / 07 =
  **structural** (spec-consistency grep, not numeric). LOOP-07 provisional values
  (IPR `1e-3`, PSC grid) are **carried, not recalibrated** (no numeric probe —
  SCOPE-15). All non-probe-able items = deterministic `rg`/grep consistency + the
  locked-convention regression guard (`D≈4.6416` present / `6.694` absent) +
  forbidden-path scope check. (There is intentionally **no** `n_col ∝ dt_base/dt_out`
  probe — LOOP-06 is deferred, nothing to probe.)

### State management

- **D-34-18:** `.planning/STATE.md` carries a **user-owned uncommitted
  modification** this session — it is NOT mutated or committed here (Phase 32 D-03
  precedent + concurrent-session governance). The user advances STATE.md. Only the
  SPEC fix, this CONTEXT, and the DISCUSSION-LOG are committed, via
  `scripts/agent-commit` with explicit owned paths (no broad staging).

### Claude's Discretion

- The planner may decide the number of Phase-34 plan files and task grouping, as
  long as every LOOP-01..08 + SI-PINN-003 requirement appears in a plan
  `requirements` field, **packet-before-edit precedes each spec edit** (D-34-10),
  and the plan is executable by `gsd-execute-phase`.
- Exact evidence-packet filename slugs (stable, grep-friendly, mapped in the
  ledger), exact ledger Markdown layout, and the exact deterministic check commands
  — provided they satisfy D-34-16/17.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Locked Phase Requirements

- `.planning/phases/34-training-loop-batch-construction-contracts/34-SPEC.md` —
  Locked Phase 34 requirements (LOOP-01..08 + SI-PINN-003), boundaries, edge
  coverage, prohibitions, acceptance criteria. **Read first.** Corrected this
  session for LOOP-04 + LOOP-06 (commit `0ffa3d8`).
- `.planning/ROADMAP.md` — v1.6 roadmap; Phase 34 goal, dependency, success
  criteria, verification protocol (re-verify-after-every-batch).
- `.planning/REQUIREMENTS.md` — LOOP-01..08, SCOPE-12 through SCOPE-15, EVID-11..15,
  VER-13..18, and v1.6 traceability.
- `.planning/STATE.md` — current project state and accumulated v1.6 decisions.
- `AGENTS.md` — STOP protocol, v1.6 source hierarchy, specwork-only boundary,
  commit protocol (`scripts/agent-commit`, owned paths, no broad staging).

### Phase 32 Evidence & Ledger (the verdicts Phase 34 consumes)

- `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md`
  — B-07 / B-08 / M14 / M16 / ALM-μ_p-clamp rows; the M14 row is the only
  pre-adjudicated LOOP verdict; B-07/B-08/M16/ALM are PENDING "Phase 34 must author
  the packet before spec edits."
- `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence/m14-gradient-clipping.md`
  — M14 `accept-resolution`: structural merge only, preserve `7-10/5/3`, do NOT
  canonize `8.5`, route exact `C`/bootstrap/floor/history-reset to Phase 34/FUT
  (GAP-08); the "Locked Convention or Owner Route" + "Named Acceptance Check"
  sections define AC-LOOP-04.
- `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence/_TEMPLATE.md`
  and `evidence/README.md` — packet schema + protocol/lifecycle to reuse when
  authoring the B-07/B-08/M16/ALM packets.

### Phase 34 Gap Register (to be created on the first STOP gap)

- `.planning/phases/34-training-loop-batch-construction-contracts/34-GAPS.md` —
  candidate for the source-silent batch edge cases (D-34-16a) and any new conflict
  a packet surfaces (D-34-11).
- `.planning/milestones/v1.6-GAPS.md` — milestone-wide gap index; add the Phase-34
  entry there per the standing trigger.

### Candidate verdict source (consume, do not re-litigate)

- `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md`
  — §1.4 (B-07 modified), §1.5 (B-08 modified), §1.8 (M14: preserve 7-10/5/3, no
  8.5; GAP-08), §1.10 (M16 defer), §1.18 (ALM defer), and the verbatim "Section 6"
  batch-construction pseudocode + claim matrix (B07-04 rejects pinn §3.1 batch
  construction).
- `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md`
  — finding→section line map + downstream ownership (M16/ALM defers routed to
  Phase 34).

### Framework specs — edit targets (SCOPE-13)

- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` —
  CANONICAL for batch construction + curriculum content. Key anchors: Total-Loss /
  Data-Flow ~1718-1745 (LOOP total-loss skeleton, D-34-15); Mini-Batch Construction
  ~1770-1784 (LOOP-01/02/03); Adaptive Median Clipping ~1786-1798 + Consolidated
  Hyperparameter table ~1909-1913 (LOOP-04 C-schedule, D-34-04); Phase-33 callout
  examples at 1630 / 1832.
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` —
  CANONICAL for the clipping **mechanism** (§4.4 ~700-720) and training strategy
  (§4); §3.1 Data Batch Construction (~323-352, author comment at 351, PIPE-04 note
  at 352) is the SI-PINN-003 reconciliation target; §4.2 Optional ALM Ablation
  ~671-679 (LOOP-05); SI-PINN-003 logged at ~1005.

### v1.5 contracts referenced by LOOP-07/08

- `pinn_instruction/markdown_conversion/framework-specs/` VAL-02 / VAL-03 / VAL-04
  contracts (SASD / IPR / PSC) — the provisional forward-references LOOP-07/08
  realize; cite, do not recalibrate.

### Read-only sources (SCOPE-09 / SCOPE-08)

- `pinn_instruction/issues/03-curriculum-and-training-loop.md` — non-authoritative
  issue doc; source positions only, via the source hierarchy.
- `pinn_instruction/markdown_conversion/framework-revisions/` — `review-of-framework.md`,
  `stage-strat-revision.md`, `data_quality_assessment.md` (read-only);
  `sampling_method.md` (frozen, SCOPE-08).

### Prior phase context

- `.planning/phases/33-curriculum-stage-contracts/33-CONTEXT.md` — the precedent
  this CONTEXT mirrors (callout convention, owner-pending discipline, deterministic
  checks, forbidden-path guards).

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets

- Phase 32 / Phase 33 evidence packets + the issue ledger show the expected
  adjudication style: line-range citations, before/after notes, named acceptance
  checks, STOP-safe owner routing. Reuse `evidence/_TEMPLATE.md` + `README.md` for
  the four Phase-34 packets.
- The Phase-33 blockquote-callout convention (`ctl_instruction.md` 1630, 1832) is
  the transcription template to copy verbatim (D-34-07).
- The existing PIPE-04 note (`pinn_architecture.md` §3.1 line 352) is the seed for
  the SI-PINN-003 pointer — extend it rather than write a new pointer (D-34-05).
- Existing GSD Phase-33 PLAN/ledger artifacts show the `<read_first>` / `<action>`
  / `<verify>` / `<acceptance_criteria>` task structure.

### Established Patterns

- **Packet-before-edit:** author the evidence packet (consuming the resolution-doc
  verdict) before any spec edit; downstream contract text cites the packet rather
  than re-deciding.
- Verification for specwork phases = deterministic `rg` / `python3` source checks +
  forbidden-path guards, not runtime training probes. Disposable formula-sanity
  probes only where a locked formula exists (D-34-17).
- Commits via `scripts/agent-commit` with `GIT_AGENT_ID` + `GIT_AGENT_OWNED_PATHS`,
  explicit owned paths, no broad staging; one atomic commit per logical unit.
- Owner-pending / source-silent values are **explicit contract holes with FUT
  routing**, never planner discretion.

### Integration Points

- `ctl_instruction.md` is canonical for batch construction + curriculum + the
  C-schedule; `pinn_architecture.md` is canonical for the clipping mechanism +
  training strategy. The two cross-reference via stable anchors (D-34-04/05/06).
- The Phase 32 issue ledger is the coordination point: Phase 34 closes the B-07 /
  B-08 / M14 / M16 / ALM rows; Phase 36 consumes the closed ledger + AC list.
- Phase 35 owns loss components / weights / `λ_E` / Huber-δ / causal mode — the
  total-loss skeleton (D-34-15) forward-references it, never defines it.

</code_context>

<specifics>
## Specific Ideas

- Use exact phrases in planned checks for the high-risk LOOP-04 prohibitions:
  `8.5` ABSENT from both files; `7-10 / 5 / 3` present in ctl; mechanism formula
  present **exactly once** in pinn §4.4; **no duplicated normative text** (each
  value/formula one canonical home); bidirectional cross-refs resolve to a real
  anchor; status tags agree across halves. **Win condition** = recoverable as one
  coherent rule, zero duplication — not merely "8.5 removed".
- Label every transcribed pseudocode block `normative spec contract — not
  executable; FUT-01/FUT-04 implements`.
- LOOP-06 must read as `realized-as-deferred`; no `n_col ∝ dt_base/dt_out` formula
  transcribed and no probe for it.
- Re-verify the LOOP-04 cross-file checks (c)/(d)/(e) after **every** Phase-34
  batch that edits either half (ROADMAP re-verify-after-every-batch).

</specifics>

<deferred>
## Deferred Ideas

- **Phase 35 (LOSS):** loss-component scaling, capped-hybrid `λ_E` schedule,
  Huber-δ calibration, causal-training-mode (D-04) contract.
- **FUT-01 / FUT-04 (trainex):** the actual DataLoader, batch constructor, ALM
  update mechanics, causal-window mechanics, Stage-0 pilot calibration.
- **FUT / SCOPE-15:** adaptive-stage-assignment EDA, threshold/IPR/PSC/SASD
  recalibration.
- **Owner-pending / deferred contract holes (carried, not filled in Phase 34):**
  the M14-deferred clipping constants (exact early-`C`, bootstrap, lower floor,
  history-reset — body-deferred, D-34-16b) and the source-silent batch edge cases
  (final-stage / undersized-lookahead / replacement policy — `34-GAPS.md`,
  D-34-16a).

### Reviewed Todos (not folded)

- `trainex-r1-research-handoff.md` ("Review and hand off the trainex-r1 research
  sub-packages") — matched at score 0.2 ("keywords: two"). **Not folded:** it is a
  trainex-track research-handoff item, not Phase-34 specwork LOOP-contract scope.

</deferred>

---

*Phase: 34-training-loop-batch-construction-contracts*
*Context gathered: 2026-06-24*
