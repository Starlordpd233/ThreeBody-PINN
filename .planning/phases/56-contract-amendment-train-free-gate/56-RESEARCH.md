# Phase 56: Contract Amendment & Train-Free Gate - Research

**Researched:** 2026-09-06
**Domain:** Framework-spec contract amendment (SCOPE-38 discipline) over a locked physics/ML training spec, plus a train-free verification gate (`pinn/verification/`) that fires an existing measurement probe against a re-derived reference scale.
**Confidence:** HIGH for everything transcription-scoped and for GATE-04 conditions (i)/(iii); by design NOT APPLICABLE to condition (ii)'s numeric threshold or the §2.4 convention question — those are open owner gaps this research feeds, not resolves (see Parts (b) and (c)).

## Summary

Phase 56 has two structurally different halves. The first half — landing `54-RULING.md`'s ratified recalibration into `pinn_architecture.md` §2.2/§3.2 as a SCOPE-38 contract amendment, and wiring GATE-04's conditions (i) [no floor-pinned weight] and (iii) [front capability] — is fully grounded: the exact spec anchors were re-verified by direct read this session (they match `54-RULING.md`'s stated line numbers exactly, with no further drift since Phase 54 wrote them), the four re-ratification blocks' text is finished prose the executor transcribes rather than authors, and the trainer's own `causal_physics_loss`/`resolve_causal_clip_facts` functions in `pinn/loss_catalog.py` already implement the exact prefix-sum/exp/clamp formula GATE-04 needs — reused, not reimplemented, exactly as Phase 55's probe already does for the old 16-point recipe.

The second half is GATE-04 condition (ii) — "a weight vector carrying differential information (not all-floor, not degenerate)" — which no source operationalizes into a number. This research does not resolve that gap (`GAP-56-01`, `56-GAPS.md`, OPEN); per the phase's explicit constraint it instead **computes and reports** what the six audited cases' actual weight vectors look like under the ratified recipe, using the repo's own vetted Phase-55 helpers (`stratified_collocation_times`, `bin_mean_residuals`) and the trainer's own loss function — never a parallel reimplementation. The headline finding, computed this session and cross-checked against the committed Phase-55 evidence: under the ratified recipe, all six audited cases produce a monotone, graded, non-floor-pinned weight vector (5.9–10.7 decades of dynamic range, coefficient of variation 1.99–3.10 on `w_2..w_16`) — a qualitatively different picture from the pre-amendment all-floor degeneracy this milestone exists to fix. But "graded" is not itself a number, and this research supplies the data without picking one. `GAP-56-02` (the §2.4 Table 1 convention question) is noted as out-of-scope-pending-owner-decision without a mechanism choice.

**Primary recommendation:** Transcribe `54-RULING.md`'s four SCOPE-38 blocks verbatim (do not paraphrase) into the exact spec anchors verified below; build `pinn/verification/gate04_train_free.py` as a new standalone `*_probe.py`-style module that imports `architecture_characterization_probe`'s six-case machinery and `loss_catalog`'s causal-weight functions to implement conditions (i) and (iii) now; wire condition (ii) as an explicit, clearly-labeled placeholder pending the owner's GAP-56-01 ruling (Part (b) supplies the six real vectors for that ruling — do not invent a threshold to unblock it); and leave §2.4 Table 1 untouched pending GAP-56-02.

## Architectural Responsibility Map

This is not a client/server application; the "tiers" below are the framework's own layers, adapted from the standard map for a scientific-computing/spec-governance codebase.

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Contract amendment text (§2.2/§3.2 prose, re-issued ACs) | Framework-Spec / Contract Layer (`pinn_instruction/markdown_conversion/framework-specs/`) | — | Source-of-truth documentation every other tier is built against; SCOPE-33 scopes the edit narrowly to this layer only |
| Ratified causal-weight computation (`ratified_causal_weights`-style function) | Verification/Tooling Layer (`pinn/verification/`) | Training/Loss Layer (`pinn/loss_catalog.py`, reused not reimplemented) | A pure measurement function that derives from, but must not fork, the trainer's own loss implementation (SC3-equivalent discipline carried from Phase 55) |
| GATE-04 verdict logic (`gate04_train_free.py`) | Verification/Tooling Layer (`pinn/verification/`) | — | Standalone script, no CI/service wiring — matches every existing `*_probe.py`; Phase 57 imports it directly |
| `R_ref` persistence (JSON artifact + provenance) | Storage/Artifact Layer (`pinn/verification/artifacts/`) | Verification/Tooling Layer (writer) | A committed, version-controlled data artifact — analogous to a config store, not a live database; precedent is `runs/.calibration/stage0-timing.json` |
| Render-oracle spec-conformance check | CI/Tooling Layer (`tools/spec-render-check/`) | Framework-Spec Layer (consumer of its output) | Static, pre-commit-style check over the spec's rendered markdown/KaTeX; must be re-run after any spec edit |
| RUN-04's consumption of GATE-04's verdict (Phase 57, out of this phase's scope) | Training Orchestration Layer (`pinn/train.py`, not touched this phase) | Verification/Tooling Layer (import source) | GATE-04 is the callee; Phase 56 builds it, Phase 57 is the caller — the phase boundary is exactly this import edge |

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

> Copied verbatim from `56-CONTEXT.md` `<decisions>` (the "Implementation Decisions" section, including the "Open Decisions surfaced to the owner" subsection). This is the planner's binding scope; do not re-derive or reinterpret it.

#### 1. Contract-amendment structure (SPEC-01, SCOPE-38)

- **D-01: Transcribe, don't compose.** The amendment text is dictated by
  `54-RULING.md`. Each of the four SCOPE-38 blocks is handled exactly as the
  ruling's "SCOPE-38 re-ratification lines" section states:
  - **Block 1 — `η_c` (§3.2, Phase 35 contract block, currently `:445`):**
    **AMENDED.** Retain the fixed value `η_c = 1`. Amend what the exponent
    consumes: from raw per-point `R̄` → the frozen-reference, 16-bin residual
    `R̃_b = R̄_b / R_ref`, with one batch-global exclusive 16-bin prefix. Name
    the superseded ruling (Phase 35 D-04 RESOLVED-WITH-INSTRUCTION /
    owner-ratified Option A / LOSS-04 / AC-LOSS-04). Record provenance (owner
    delegation 2026-09-04 → Codex checkpoint-② adjudication → `A1 + B2
    (residual-wide) + C1 + D3 + E1`). Re-issue AC-LOSS-04 **verbatim** from
    `54-RULING.md` Block 1's "Re-issued acceptance criterion" paragraph (no new
    identifier).
  - **Block 2 — `first_omega_0` fixed-at-30 sentence (§2.2, currently `:181`):**
    **NOT AMENDED.** Record "not amended"; Phase 20 ARCH-01 remains the AC.
  - **Block 3 — clip underflow-only purpose (§ loss catalog, currently
    `:668-671`):** **NOT AMENDED.** Record "not amended." Note that GATE-04
    logging + refusal-on-bind is observability, not repurposing.
  - **Block 4 — DATA-05 collocation allocation / time-draw:** the *spec*
    expression is §3.2's `n_col`. Write into §3.2: `n_col = 4096` is the
    **total per training batch** (not per-trajectory); `M = 16` fixed equal-`u`
    bins `[b/16, (b+1)/16)` for `b = 0..14` and `[15/16, 1]` for `b = 15`;
    exactly 256 rows per bin; one batch-global exclusive 16-term prefix over the
    16 per-bin mean residuals (never over 4096 rows, never a flattened order);
    the 240-slot replay-only construction (seeded 3840 + 256 remainder rule);
    energy reuses the same set; microbatching preserves complete bin aggregates
    and never resets the prefix. This supersedes GAP-39-12 Option C **only** as
    to its independent full-domain time-draw clause. Re-issue that block's AC
    verbatim from `54-RULING.md` Block 4.
  — **Reversibility:** one-way — a published framework-spec contract amendment
  that downstream FUT-01 code and Phase 57 are built against; a wrong
  transcription propagates as spec drift across phases, which is exactly the
  cost SCOPE-38 exists to prevent. The mitigation is that the source text is
  fixed, so the executor copies rather than authors.

- **D-02: `R_ref` definition goes in §3.2 alongside the normalization.** The
  spec has no residual normalization today. Add it in §3.2 where the `w_n` and
  `L_phys^causal` formulae live: define `R̃_b = R̄_b / R_ref`; define `R_ref`
  as the finite positive **median of the 96 raw bin means** produced at
  initialization by the fixed six-case GATE-04 seed/IC probe (6 cases × `M = 16`
  bins), each case using its recorded probe seed and exactly 4096 stratified
  times (256 per bin); state that `R_ref` is **detached and frozen for all of
  Stage 0**, used in both the causal exponent and the outer physics loss, never
  updated online; and transcribe the full invalidation-trigger list from
  `54-RULING.md` "Reference invalidation" (any change to `first_omega_0`, depth,
  width, power-skip exponent, LayerNorm placement/stabilizer, init bounds, `D`,
  `T`, `epsilon_soft`, IC13 normalization, `n_col`, `M`, count unit,
  selected-slot semantics, or bin/allocation semantics → re-measure `R_ref` and
  re-run GATE-04). State the `N_t` the calibration binds to (4096-total) and the
  re-check trigger (SC3, SPEC-06).

- **D-03: Reconcile `collocation_count = 16` in prose only.** SC3 requires the
  amended spec to "reconcile `pinn/train.py:1033`'s `collocation_count = 16`
  against §3.2's `n_col = 4096`." Do this as a spec sentence recording that the
  current run driver uses 16, that the ratified calibration binds to
  4096-total-per-batch with the 16-bin prefix, and that the FUT-01 trainer
  rebuild must honour the ratified structure. **Do not edit `pinn/train.py`**
  (SCOPE-33; live code is not a v2.3 grounding source or edit target).

#### 2. GATE-04 implementation (GATE-04)

- **D-04: New standalone module `pinn/verification/gate04_train_free.py`.**
  Follows the established `pinn/verification/*_probe.py` convention exactly:
  `argparse`-based `main(argv=None)` + `if __name__ == "__main__":`, importable
  functions/dataclass in `__all__`, a `TrajectoryGateMetrics`-style frozen
  result dataclass with an exhaustive docstring naming every threshold, and a
  fail-closed verdict object (`PASS` / `BLOCK` + per-condition reasons). It is
  **not** wired into any automated verify ladder or CI gate — no
  `pinn/verification/` probe is (confirmed in 55-CONTEXT code_context). Phase
  57's RUN-04 path imports and calls it as an explicit precondition.
  — **Reversibility:** reversible — a new tool module; nothing depends on it
  until Phase 57.

- **D-05: The ratified-recipe `w_n` computation is a new pure function in the
  Phase 55 probe module, not a trainer edit.** Add
  `ratified_causal_weights(...)` (or similar) to
  `pinn/verification/architecture_characterization_probe.py` as a peer of the
  already-committed `stratified_collocation_times` / `bin_mean_residuals` /
  `RATIFIED_N_BINS` helpers (Phase 55 plan 55-03). It takes per-point residuals
  + a frozen `R_ref`, forms the 16 bin-mean `R̄_b`, computes `R̃_b`, builds the
  batch-global exclusive 16-term prefix, and evaluates `w_n` reusing the
  trainer's own exp/clip facts via `resolve_causal_clip_facts(dtype, device)`
  (already imported by the probe). This keeps GATE-04 measuring the *ratified
  formula as specified* without a trainer that implements it yet, and keeps the
  probe's public API the single source of the recipe arithmetic (55-CONTEXT
  integration-point: "keep the public API stable — Phase 56 is a hard downstream
  consumer").
  — **Reversibility:** costly — extends a public API two later phases consume;
  name and signature should be settled once and held.

- **D-06: GATE-04 conditions (i) and (iii) — grounded, implement as stated.**
  - (i) **No causal weight pinned at the dtype clamp floor:** for every case,
    every entry of `w_n` is strictly greater than
    `resolve_causal_clip_facts(dtype, device)['causal_clip_min_weight']`
    (never a copied literal — read it from the runtime, matching the Phase 55
    probe convention). Also fail closed on any non-finite entry in the residual,
    prefix, or weight vector, and reject non-finite residuals/prefixes *before*
    clipping (`54-RULING.md` Block 3 re-issued AC).
  - (iii) **`front_idx` able to advance:** `front_idx` is the trainer formula
    (`max(n : w_n > 0.5)`, `controllers.py`). "Able to advance" is a
    *capability* claim, not `front_idx > 0` at init — the healthy-init
    expectation is a graded weight vector, not an advanced front. The concrete
    test for capability is part of GAP-56-01 (below).
  - Log the normalized unclipped exponent and a per-step guard-binding count;
    any binding at initialization fails GATE-04 (`54-RULING.md` `E1`).

- **D-07: GATE-04 runs the six audit cases as its built-in default, config-
  driven for more.** Mirrors Phase 55 D-02: calling GATE-04 with no case
  arguments runs exactly the six audited `(seed, masses, IC13-mode)` rows
  (`architecture_characterization_probe.DEFAULT_CASES`); a Python/CLI config
  surface accepts an arbitrary case list. `float64` / CPU / no-training, matching
  the probe.

- **D-08: SC5 demonstration — assert `BLOCK` on the pre-amendment recipe.**
  Fire GATE-04's verdict logic against the *pre-amendment* path (raw per-point
  `R̄`, `n_col = 16`, no `R_ref`) — i.e. the existing
  `architecture_characterization_probe` output the audit reproduces (15/16
  weights at the float32 clamp floor, `front_idx = 0` on all six rows). GATE-04
  must return `BLOCK` tripping condition (i) and the degeneracy condition.
  Capture as a committed test in `tests/phase56/` + an evidence artifact.
  — **Reversibility:** reversible — test-only.

#### 3. `R_ref` persistence & governance

- **D-09: `R_ref` is a committed JSON artifact with full provenance, written
  by GATE-04, under `pinn/verification/`.** Proposed path
  `pinn/verification/artifacts/r_ref_stage0.json` (create the directory;
  precedent: the calibration-JSON pattern used by `runs/.calibration/
  stage0-timing.json` for the duration gate). Contents: the `R_ref` value; the
  6 cases; all 96 raw bin means; the statistic (`median`, `numpy.median`
  even-N convention); the stratification/config provenance (seeds, bin edges,
  256-per-bin, `float64`/CPU); the git worktree/branch/commit identity; and the
  verbatim invalidation-trigger list. Committed so the value that gates RUN-04
  is re-derivable and version-controlled (GAP-54-03: "derive `R_ref` from the
  fixed GATE-04 initialization probe"; `54-RULING.md` `B2`: "persist its value,
  cases, statistic, tree/config identity, and invalidation inputs").
  — **Reversibility:** costly — Phase 57 RUN-04 and every downstream training
  run read this value; regenerating it after a structural change is required by
  contract but a silent path/format change would break the consumer.
  — **Owner visibility:** the *procedure* is fully grounded; only the artifact
  location/format is a Claude call. Flagged here (not a blocking gap) because it
  is a governed, run-gating value — see "Open Decisions" note.

#### 4. Secondary wordings the amendment forces

- **D-10: `§4.1` `η_c = 1` default wording (currently `:647`).** 53-RESEARCH
  flagged this as a SCOPE-38-marked, Phase-56-coupled site. `η_c` keeps the
  value `1` but its exponent argument changes; update this line's cross-
  reference/wording so it is consistent with the amended §3.2 block (point at
  the re-issued AC; do not restate the formula). Byte-preserve the value.
  **Session anchor note:** verified by direct read this session — the current
  live-tree line for this sentence is `pinn_architecture.md:668` ("`$\eta_c = 1$`
  default."), not `:647`; re-derive by content match as always (see the
  Anchor-Drift Pitfall below).

- **D-11: `§3.2` "recommended: 2048–4096" prose (Listing 3 docstring, currently
  `:461`).** Now that `n_col = 4096` is a *fixed total per training batch*
  (D3), the "recommended range" language is superseded. Reconcile: keep the
  code listing runnable but add a spec sentence that the ratified value is
  `4096` total (not a tunable range) and that the range wording is historical.
  Un-swept inventory item 5 ("SPEC-06 territory").

### Claude's Discretion

- Exact section placement and heading text of the new amendment sub-blocks
  within §2.2 / §3.2, and the exact prose of the provenance paragraph (the
  facts are fixed by `54-RULING.md`; the wording is editorial within an
  already-decided change).
- The `gate04_train_free.py` result-dataclass field names and CLI flag names
  (follow `gate_metrics.py` / `*_probe.py` conventions).
- `ratified_causal_weights` exact signature (settle once per D-05).
- Evidence-directory layout under `.planning/phases/56-*/evidence/` (follow the
  established `evidence/<category>/<timestamp>/` convention).
- Test file locations: `tests/phase56/` per the per-phase test-dir convention.
- Whether GATE-04's "controlled residual reduction" probe (once GAP-56-01 is
  ratified) lives in the probe module or the gate module.

### Open Decisions surfaced to the owner (STOP protocol — not invented)

Two decisions below are **acceptance-check-schema / spec-convention** calls not
answered by any grounding source. They are recorded in `56-GAPS.md` and
`.planning/milestones/v2.3-GAPS.md`. Blocking is dependency-scoped: the core
§2.2/§3.2 transcription (D-01, D-02) and the GATE-04 structural scaffolding
(D-04, D-05, D-07) proceed; only the items named below wait.

- **GAP-56-01 (HIGH) — GATE-04 condition (ii) operationalization.** Conditions
  (i) [no floor-pinned weight] and (iii) [front capability] and the
  non-finite checks are grounded and precise. Condition (ii) — "a weight vector
  carrying **differential information** (not all-floor, not degenerate)" and
  the `54-RULING.md` re-issued-AC phrase "a front that cannot respond to
  **controlled residual reduction**" — has no numeric or structural definition
  in any source. This threshold *is* the SCOPE-35 single-look protection: too
  loose and a saturated recipe passes and wastes the one preserved run; too
  tight and it false-blocks a healthy recipe. The gsd-phase-researcher should
  assemble concrete candidate definitions (e.g. a coefficient-of-variation
  floor on the non-boundary weights `w_2..w_16`; a minimum count of distinct
  non-floor weights; monotone-decreasing + a minimum dynamic-range span in
  decades; and a design for the controlled-reduction response test — apply a
  known `−δ` to the bin residuals and require `front_idx` to move by `≥ 1` or
  the weight vector to shift measurably). **The owner ratifies the numeric
  bound before the executor wires it.** This blocks: the GATE-04 pass/fail
  threshold for condition (ii), the controlled-reduction test, and SC5 tuning
  of the demonstration margin. **See Part (b) below for the requested six-case
  grounding data — computed and reported, not resolved.**

- **GAP-56-02 (MEDIUM) — §2.4 Table 1 locked-vs-default convention scope.**
  53-UNSWEPT-INVENTORY item 1 routed §2.4 Table 1's "**Recommended Value**"
  header + the `first_omega_0 | 30` row to Phase 56 as an owner-visible item.
  Applying Phase 53's `**[LOCKED]**` / `**[DEFAULT]**` convention to §2.4
  requires generalizing that convention beyond its single §4.1 application
  site — and GAP-45-03 consequence 5 **explicitly left convention
  generalization undecided**. `first_omega_0` is NOT AMENDED (D3-A), so this is
  a consistency-only question: does Phase 56 (a) mark the row `[LOCKED]` and
  clarify the header, (b) add a one-line note pointing to the §2.2 lock without
  touching the table convention, or (c) leave §2.4 as-is and re-route the item?
  Recommendation: (b) — minimal, avoids an un-ratified convention
  generalization. **Owner confirms the scope.** This blocks only the §2.4
  cosmetic edit; nothing else in the phase. **See Part (c) below — noted as
  out-of-scope-pending-owner-decision, not resolved.**

### Deferred Ideas (OUT OF SCOPE)

> Copied verbatim from `56-CONTEXT.md` `<deferred>`.

- **Second-optimizer-phase / L-BFGS causal-weight recomputation semantics** —
  GAP-54-06, DEFERRED to Phase 57 owner checkpoint ③, before RUN-04. Not Phase
  56.
- **Invariant-B monitoring window (`N = 500`) re-ratification** and the
  **front-monitoring aggregation estimator** — Phase 57 owner checkpoint ③.
- **Pre-registration of the EVAL-02 spending seed** — Phase 57 owner
  checkpoint 4.
- **Power-skip stack as a capacity surface** — GAP-54-02 closed it as a future
  ablation; not reopened.

#### Reviewed Todos (not folded)

- **d-06-static-epsilon-sensitivity-check** (score 0.6, keyword-only match on
  "check"/"over"/"phase") — a spec-side `epsilon_soft` dual-context sensitivity
  question with no VER-20 routing; folding it would breach SCOPE-33's narrow
  spec-edit authorization. Phase 55 also reviewed and did not fold it. Remains
  in `.planning/todos/pending/`; revisit at milestone close.
- **trainex-r1-research-handoff** (the r1b tuning round) — unrelated to Phase
  56 scope; not folded.

</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| SPEC-01 | Implement the ratified causal-weight/SIREN-scale recalibration (VER-20 item **e**) as a `pinn_architecture.md` §2.2/§3.2 amendment under SCOPE-38 discipline: name the superseded ruling, record provenance, carry a re-issued AC. `[VERIFIED: .planning/REQUIREMENTS.md:90]` | Part A.2 (verbatim `54-RULING.md` blocks) + Part A.3 (session-verified anchors) supply the exact text and locations to transcribe. |
| SPEC-06 | Dispose of the `n_col` spec/code divergence (spec `n_col=4096` vs `pinn/train.py:1033`'s `collocation_count=16`) jointly with SPEC-01, recording the `N_t` the calibration binds to and the re-check trigger. `[VERIFIED: .planning/REQUIREMENTS.md:95]` | Part A.2 Block 4 + D-03/D-11 supply the exact reconciliation sentence content; Part A.9 flags the one pre-existing test-suite interaction this edit surfaces. |
| GATE-04 | Train-free acceptance gate: before RUN-04, INST-04's probe must show (i) no floor-pinned weight, (ii) differential/non-degenerate weight vector, (iii) front capable of advancing, across the six audit cases; fail closed. `[VERIFIED: .planning/REQUIREMENTS.md:100]` | Part A.4–A.6 ground conditions (i)/(iii) and the reusable formula; Part (b) supplies the six-case computed data GAP-56-01's condition-(ii) ruling needs — without resolving it. |

</phase_requirements>

## Part (a) — Grounded Findings the Planner Can Act On Directly

### A.1 Both hard gates are satisfied

`[VERIFIED: .planning/STATE.md:1-19, 28; .planning/ROADMAP.md:58]` Phase 54 (`54-RULING.md`, checkpoint ② discharged 2026-09-04) and Phase 55 (INST-04 probe, completed 2026-09-06) are both marked complete in `STATE.md`'s frontmatter (`completed_phases: 3`) and `ROADMAP.md` line 58 ("Phase 55... (completed 2026-09-06)"). Phase 56 may open.

### A.2 The ratified decision, verbatim (`54-RULING.md`)

`[VERIFIED: .planning/phases/54-recalibration-decision-grounding/54-RULING.md, read in full this session]`

The checkpoint-② table (lines 48-54) disposes of all five surfaces: `η_c` → **RATIFIED — A1** (retain `η_c=1`, amend what the exponent consumes); `R̄` normalization → **RATIFIED — B2, residual-wide** (frozen median-of-96-bin-means `R_ref`); `ω₀`/`first_omega_0` → **RATIFIED — C1/D3-A; NOT AMENDED**; `N_t`/`n_col` → **RATIFIED — D3, jointly with A1** (4096 total/batch, 16 fixed bins, 256/bin); causal-exponent clip → **RATIFIED — E1/D5-A; NOT AMENDED**.

The four SCOPE-38 re-ratification blocks (lines 197-233) are the literal amendment text. Transcribed here in full since D-01 instructs the executor to copy, not compose:

> **Block 1 — the `η_c` Phase 35 contract.** Contract marker: "This file keeps the per-time causal weighting component as the default: `w_1 = 1`, `w_n = exp(-eta_c * sum_{m<n} stopgrad(Rbar_m))`, and `eta_c = 1`." Location: `pinn_architecture.md:445`. Superseded ruling: Phase 35 D-04 RESOLVED-WITH-INSTRUCTION / owner-ratified Option A (LOSS-04; AC-LOSS-04). New decision provenance: "Owner instruction on 2026-09-04 expressly delegated checkpoint-② adjudication to the Codex primary agent using its best mathematical and scientific reasoning. After reading the trainex-r3 candidate document, Rule-19 verification report, premise adjudication, intake record, and routed gaps, that adjudication ratified `A1 + B2 (residual-wide) + C1 + D3 + E1`. This supersedes the Phase 35 ruling only as to the exponent's raw-residual argument and one-point-per-prefix-term structure; `η_c = 1` remains fixed." **Re-issued acceptance criterion (verbatim, no new identifier):** "AC-LOSS-04 is re-issued without a new identifier: the default Stage-0 causal loss uses exactly `η_c = 1`, `n_col = 4096` total per training batch, `M = 16` fixed equal-`u` bins with exactly 256 rows per bin, `R̃_b = R̄_b/R_ref`, one batch-global exclusive 16-bin prefix, and residual-wide normalization. Each of the fixed six initialization-probe cases uses exactly 4096 recorded-seed stratified times (256 per bin); `R_ref` is the finite positive median of the resulting 96 raw bin means, is detached and frozen, all 96 constituents and provenance are retained, and every trigger named in the checkpoint-② discharge section invalidates it. Raw and normalized diagnostics are both recorded; raw-unit thresholds are never silently applied to normalized values. GATE-04 must evaluate the actual full vectors and fail closed on any non-finite input, any floor-bound initialization weight, a degenerate weight vector, or a front that cannot respond to controlled residual reduction. A resampled training-batch front is diagnostic only; invariant-B evidence follows the fixed-monitor boundary above. GAP-54-06's L-BFGS question is not part of this criterion and must be settled at checkpoint ③ before RUN-04."

> **Block 2 — the `first_omega_0` fixed-at-30 sentence.** Contract marker: "`first_omega_0` is fixed at `30` and is not scheduled during training." Location: `pinn_architecture.md:181`. Superseded ruling: Phase 20 ARCH-01. **NOT AMENDED** — provenance and AC both explicitly "NOT AMENDED"; Phase 20 ARCH-01 remains the acceptance criterion.

> **Block 3 — the causal-exponent clip's underflow-only purpose.** Contract marker: "Clip the causal exponent to avoid underflow, but do not choose a numeric clipping bound in Phase 19; surface a gap if one is needed. The causal exponent clip is required only to avoid underflow." Location: `pinn_architecture.md:668-671`. Superseded ruling: the Phase 35 guard block. **NOT AMENDED** — but "implementations additionally reject non-finite values before clipping, log the unclipped exponent and binding count, and fail GATE-04 if the guard binds at initialization" (this addendum belongs in the amendment prose as an observability note, per D-01/D-06).

> **Block 4 — the DATA-05 collocation allocation and time-draw contract.** Contract marker: GAP-39-12 Option C's provisional total `C=4096`/batch, near-even quotas, independent continuous time draws. Location: `.planning/milestones/v2.0-phases/39-data-ingestion-stage-0-population-scan/39-GAPS.md:524-608`. Superseded ruling: GAP-39-12 RESOLVED-WITH-INSTRUCTION, Option C, **only as to its independent full-domain time-draw clause**. **Re-issued acceptance criterion (verbatim):** "A full 256-slot batch emits exactly 4096 physics rows as one independently sampled time in each of 16 fixed bins for every selected slot. A 240-slot replay-only batch uses the seeded 3840-plus-256 remainder construction stated above, yielding exactly 256 rows per bin and per-slot totals 17 or 18. Replacement multiplicity is preserved; every bin is non-empty by construction; each bin residual is the mean of exactly 256 rows; one batch-global exclusive prefix is formed over the 16 bin means; energy reuses the same set; and microbatching preserves complete bin aggregates and never resets the prefix."

The "Batch allocation and bin policy" paragraph (`54-RULING.md` lines 167-177), which `56-CONTEXT.md` "Specific Ideas" explicitly says to transcribe rather than paraphrase:

> "The fixed bins are `[b/16,(b+1)/16)` for `b=0…14` and `[15/16,1]` for the last. In a 256-slot batch, draw one point per selected slot inside every bin. In a replay-only 240-slot batch, first draw one point per slot in every bin (`3840` rows), then use one canonical seeded permutation of the 240 slots: bins 0–14 each give a second draw to the next disjoint 16-slot slice of that permutation, and bin 15 gives a second draw to its first 16 slots. Each bin therefore has exactly 256 rows; 224 slots have 17 rows and 16 slots have 18, matching GAP-39-12's near-even quota. A bin residual is the mean over its 256 rows. Empty bins are impossible, and the causal prefix is one batch-global 16-bin prefix. This re-ratifies the time allocation only; energy continues to reuse the physics set."

And the "Reference invalidation" trigger list (line 179-184, verbatim): "Re-measure `R_ref` and re-run GATE-04 after any change to `first_omega_0`, depth, width, power-skip exponent, LayerNorm placement or stabilizer, initialization bounds, `D`, `T`, `epsilon_soft`, IC13 normalization, `n_col`, `M`, count unit, selected-slot semantics, or bin/allocation semantics. A resource failure at the ratified total batch count is a fail-closed result, not permission to reduce the count silently."

**Explicitly deferred by `54-RULING.md` itself** (not Phase 56's to decide): the optimizer-phase boundary (GAP-54-06 → Phase 57 checkpoint ③) and the front-monitoring aggregation estimator (→ Phase 57 checkpoint ③, "not invented here").

### A.3 Exact spec anchors — session-verified, with drift warning honored

`[VERIFIED: pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md, read directly this session at offsets 163-307 and 383-522 and 632-801]`

`54-RULING.md`'s "Anchor-drift warning (for Phase 56)" (lines 235-246) states the four `REQUIREMENTS.md`/`ROADMAP.md`-quoted anchors (`:424`, `:167`, `:433`, `:440`) drifted after Phase 53's commits, with verified replacements `:445`, `:181`, `:454`, `:461`. This session independently re-verified all of them by direct `Read`, and they are **still accurate as of this research pass** — no further drift since `54-RULING.md` recorded them:

| Anchor | Line (session-verified) | Content (verbatim excerpt) |
|---|---|---|
| §2.2 `first_omega_0` fixed-at-30 sentence | `:181` | "The initial frequency parameter `first_omega_0` is fixed at `30` and is not scheduled during training." |
| §3.2 Phase 35 `η_c` contract block | `:445` | "> **Phase 35 contract: causal-training mode (LOSS-04; D-04 RESOLVED-WITH-INSTRUCTION / owner-ratified Option A; AC-LOSS-04...** This file keeps the per-time causal weighting component as the default: `w_1 = 1`, `w_n = exp(-eta_c * sum_{m<n} stopgrad(Rbar_m))`, and `eta_c = 1`." |
| §3.2 Listing 3 `n_col=4096` default | `:454` | `def sample_collocation_points(u_min=0.0, u_max=1.0, n_col=4096, strategy='uniform',` |
| §3.2 "recommended: 2048-4096" docstring | `:461` | `n_col: Number of collocation points (recommended: 2048-4096)` |
| §2.4 Table 1 header | `:267` | `| **Hyperparameter** | **Recommended Value** | **Rationale & Justification** |` |
| §2.4 Table 1 `first_omega_0` row | `:274` | `| first_omega_0 | 30 | A high initial frequency injects a high-frequency basis into the network, helping it overcome spectral bias from the outset.[1] |` |
| Loss-catalog clip underflow-only purpose | `:668-671` | "$\eta_c = 1$ default. Use `stopgrad` in weights by default. Clip the causal exponent to avoid underflow, but do not choose a numeric clipping bound in Phase 19; surface a gap if one is needed. The causal exponent clip is required only to avoid underflow." |
| §4.1 `η_c = 1` default cross-reference (D-10 target) | `:668` (same line as the clip sentence — one contiguous `where:` bullet) | (same excerpt as above — D-10's "currently `:647`" note is itself now stale; `:668` is current) |
| §4.1 Phase 53 locked-vs-default contract block | `:688` | "> **Phase 53 contract: PHYS-05 per-stage table locked and locked-vs-default convention (SPEC-02; SPEC-03...** ... This site is the locked-vs-default convention's first and only application in this phase..." |

**Pitfall, stated explicitly:** every one of these anchors will drift again the moment Phase 56's own first task edits the file (inserting the new §3.2 amendment prose pushes every subsequent line number down). Each task within Phase 56 that touches a *later* anchor must re-derive it by content match against its own then-current tree state, exactly as `54-RULING.md` itself instructs — never chain anchors from this table or from an earlier Phase-56 task's plan text.

### A.4 The trainer's actual causal-weight formula — reuse, don't reimplement

`[VERIFIED: pinn/loss_catalog.py:283-347, read in full this session]`

`causal_physics_loss(residuals_per_time, *, eta_c=CAUSAL_ETA_C, times=None, dtype, device, return_details=False)` already implements exactly the exclusive-prefix/exp/clamp formula the amendment needs — generically, over whatever `residuals_per_time` vector is passed:

```python
detached = rbar.detach()
cumsum = torch.cumsum(detached, dim=0)
zeros = torch.zeros(1, dtype=dtype, device=device)
cumsum_excl = torch.cat([zeros, cumsum[:-1]], dim=0)   # exclusive prefix
clip_facts = resolve_causal_clip_facts(dtype, device)
exponent = -eta * cumsum_excl
floor = torch.as_tensor(clip_facts["causal_clip_exponent_floor"], dtype=dtype, device=device)
weights = torch.exp(torch.clamp_min(exponent, floor))
```

This means **the ratified 16-bin recipe requires no new weight-computation logic** — only a new *input* to this same function: instead of 16 raw per-collocation-point `R̄_n` values, pass the 16 normalized bin-mean `R̃_b` values (with `times` as any strictly-ascending proxy for bin order — the function only uses `times` to assert ordering, confirmed by direct read of lines 309-321; the actual numeric values of `times` never enter the weight computation). This session's own computation (Part b.1) validates this by calling `causal_physics_loss` unmodified with bin-mean residuals as input and bin-center times as the ordering proxy.

`resolve_causal_clip_facts(dtype, device)` (`pinn/loss_catalog.py:77-115`) returns the dtype/device-derived floor — for `float64`/`cpu` this session measured `causal_clip_exponent_floor = -708.396419`, `causal_clip_min_weight = 2.225074e-308` (the float64 tiny value) — confirming GATE-04 condition (i) must read this from the runtime, never hardcode a literal, exactly as D-06 already states.

### A.5 The Phase-55 probe's reusable API

`[VERIFIED: pinn/verification/architecture_characterization_probe.py, read in full this session]`

Public surface (`__all__`, lines 104-117): `SweepCase`, `ArchitectureCharacterizationResult`, `DEFAULT_CASES`, `DEFAULT_N_COL`, `measure_case`, `run_sweep`, `load_cases_config`, `main`, `stratified_collocation_times`, `bin_mean_residuals`. Plus module constants `RATIFIED_N_BINS = 16`, `RATIFIED_PER_BIN = 256`, `RATIFIED_TOTAL = 4096` (lines 69-75).

`DEFAULT_CASES` (lines 250-262) is the exact six-row tuple GATE-04's D-07 default must reuse verbatim — do not re-declare a parallel list:

```python
DEFAULT_CASES: tuple[SweepCase, ...] = (
    SweepCase(label="41", seed=41, masses=(1.0, 1.0, 1.0), ic13_mode="zero"),
    SweepCase(label="42", seed=42, masses=(1.0, 1.0, 1.0), ic13_mode="zero"),
    SweepCase(label="43", seed=43, masses=(1.0, 1.0, 1.0), ic13_mode="zero"),
    SweepCase(label="0", seed=0, masses=(1.0, 1.0, 1.0), ic13_mode="zero"),
    SweepCase(label="7", seed=7, masses=(1.0, 1.0, 1.0), ic13_mode="zero"),
    SweepCase(label="41-variable-mass", seed=41, masses=(1.0, 0.8, 0.6), ic13_mode="random_tanh"),
)
```

`stratified_collocation_times(*, n_bins=RATIFIED_N_BINS, per_bin=RATIFIED_PER_BIN, rng, t_max=T_CHARACTERISTIC_TIME)` (lines 411-476) draws the ratified 4096-stratified times and returns `(times_sorted, bin_index_sorted)`; its own docstring states it "must not be reached from `run_sweep`, `measure_case`, or `main`" in Phase 55 — Phase 56 is exactly the phase authorized to wire it into a real six-case measurement (55-CONTEXT D-03).

`bin_mean_residuals(rbar_per_point, bin_assignment, *, n_bins=RATIFIED_N_BINS)` (lines 479-508) reduces per-point residuals to the 16 bin means, raising `ValueError` on an empty bin or a length/range mismatch (fail-closed, matching T-55-14 in `55-SECURITY.md`).

`tests/phase55/test_architecture_characterization.py` (46 tests, confirmed passing per `55-VERIFICATION.md`) already exercises both helpers against synthetic arrays (lines 523-587) and proves their unreachability from the production path (line 659, the two-name containment test) — this is the test suite GATE-04's own tests should sit beside (`tests/phase56/`), not duplicate.

### A.6 GATE-04 conditions (i) and (iii) — concretely computable now

Condition (i) is a direct per-entry comparison against `resolve_causal_clip_facts(...)['causal_clip_min_weight']` (A.4 above) plus a `math.isfinite`/`torch.isfinite` check on every residual, prefix, and weight entry, checked *before* the clamp per Block 3's re-issued AC.

Condition (iii)'s "able to advance" language is a capability claim `54-RULING.md` itself frames only as "a front that cannot respond to controlled residual reduction" (Block 1's re-issued AC) — i.e., it is inseparable from GAP-56-01's still-open response-test design. What IS grounded and computed this session (Part b.4-b.5): the mechanistic fact that `front_idx` (0-indexed: `max(n : w_n > 0.5, default=-1)` over the 16-entry vector, exactly `architecture_characterization_probe._front_idx`) only responds to reductions applied to bins *at or before* the index in question, because the weight at bin `n` depends only on the exclusive prefix over bins `0..n-1`. A controlled-reduction test that perturbs only late bins will show **zero** front-index response at any perturbation magnitude — confirmed empirically in Part (b) below, not merely asserted.

### A.7 `R_ref` persistence — code-grounded pattern precedent

`[VERIFIED: runs/.calibration/stage0-timing.json, read in full this session]`

The repo's existing calibration-JSON precedent (Phase 43's duration gate) has exactly the shape D-09 asks GATE-04's `R_ref` artifact to follow:

```json
{
  "schema_version": "phase43-stage0-timing/v1",
  "s_per_step": 0.18288215688329543,
  "full_stage0_steps": 300,
  "forecast_seconds": 54.86464706498863,
  "timestamp": "2026-08-15T02:51:01.296265+00:00",
  "fingerprint": {
    "device": "mps", "dtype": "torch.float32", "torch_version": "2.12.1",
    "python_version": "3.11.15", "git_head": "c4a1550b...", "git_head_available": true
  },
  "valid": true
}
```

A `schema_version` string, the computed value, a `fingerprint` block (device/dtype/versions/git identity), and a `valid` boolean — directly transferable to `pinn/verification/artifacts/r_ref_stage0.json`'s shape (value, 6 cases, 96 raw bin means, statistic name, seeds/bin-edges/precision-device provenance, git identity, invalidation-trigger list — per D-09). `[CITED: STATE.md "Decisions from 47-02"]` also references a stronger sibling pattern worth reusing for the *consumer* side: `pinn/training/run_metadata.py` persists via `atomic_write_text` "with re-validate-on-load and explicit `expected_energy_floor_factor`/`expected_eps_train` bindings" — i.e., Phase 57's RUN-04 should not merely read the `R_ref` JSON but re-validate it against its own expected invalidation-trigger fingerprint at load time, the same discipline already established for `s_h`/`eps_h`. `atomic_write_text` (already imported by the Phase-55 probe, `pinn/training/atomic_io.py`) is the write primitive to reuse — do not hand-roll a plain `open(...).write(...)`.

### A.8 Render-oracle interaction

`[VERIFIED: tools/spec-render-check/README.md and tools/spec-render-check/adjudications/22-02-pinn-architecture.json, read in full this session; command re-run this session, confirmed functional: node v24.16.0, "SELFTEST PASS (G1)"]`

Command: `node tools/spec-render-check/detect.mjs --adjudications tools/spec-render-check/adjudications/22-02-pinn-architecture.json pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` (or `--all` for the full-suite gate). The existing adjudication file has exactly 7 entries, **all in §2.2-§2.4 (lines 184, 202, 250, 252, 273, 274, 275)** — none inside §3.2 (which starts at line 383). Consequence: Phase 56's core §3.2 amendment (Block 1/4) will not require renumbering these 7 existing entries, **but** the new §3.2 prose is unadjudicated territory and must be re-run through the detector — new LaTeX/markdown in the amendment text could trigger fresh DEFINITE/REVIEW findings needing their own adjudication rows. If GAP-56-02 is later resolved in favor of touching §2.4 (rows 274-275's neighborhood), the 7 existing entries' line numbers would need re-verification at that time — flagged here, not resolved (see Part (c)).

The SCOPE-38 negative-diff guard Phase 53 established (`53-01-PLAN.md`, cited in `56-CONTEXT.md` code_context) — `git diff -U0 ... | grep -E 'eta_c|first_omega_0|underflow'` must be empty for contract-marked lines NOT being amended — narrows for Phase 56 to Blocks 2/3 only (`first_omega_0`, `underflow`), since Block 1 (`eta_c`) is legitimately changing this phase.

### A.9 Pre-existing test-suite interaction — a stale v2.0-era guard (Common Pitfall, load-bearing)

`[VERIFIED: tests/phase38/test_prohibitions.py:1-46,136-159, read in full this session]`

This file implements a **Phase-38/v2.0-era SCOPE-18 mechanical guard** that asserts `pinn_architecture.md` and `ctl_instruction.md` are byte-identical to a frozen pre-v2.0 baseline and untouched in git history since:

```python
PHASE_BASE_REF = "9160a5200df5e515998e235eb13a31c664b67057"
SPEC_BASELINE_SHA256 = {
    "pinn_instruction/.../ctl_instruction.md": "0b73ba03...",
    "pinn_instruction/.../pinn_architecture.md": "e629b2fc...",
}

def test_spec_byte_identity_endpoint_sha256(self):
    ...
    self.assertEqual(got, expected, f"... SCOPE-18 prohibits Phase-38 edits to framework specs")

def test_spec_history_no_touch_since_phase_base(self):
    # git log --name-only PHASE_BASE_REF..HEAD -- <both specs> must be empty
```

**This guard is already broken and has been since Phase 53** — `55-VERIFICATION.md:197` records: `"Full-file pytest tests/phase38/test_prohibitions.py still shows 2 failed"`, explicitly disposed of as "Pre-existing SCOPE-18 spec-SHA failures on `pinn_architecture.md` (last touched by `3e9f94da`, Phase 53 — no Phase 55 commit touches it). ... Unrelated to Phase 55." Phase 56 will touch the same file again (that is the entire point of SPEC-01/SPEC-06), so **these same two tests will continue failing** — this is expected, pre-existing, and not a Phase-56 regression. **Do not** attempt to "fix" this by reverting the spec edit (that would defeat SPEC-01/SPEC-06 entirely), and do not let a full-suite `pytest` run's red result on these two tests be mistaken for a Phase-56-caused failure. The correct action is almost certainly to retire or update this v2.0-era test now that SCOPE-33 explicitly re-authorizes spec edits in v2.3 — but note that whether *retiring/updating this test file* is itself in Phase 56's SCOPE-33 grant (a `tests/phase38/` file, not a framework spec) is not addressed by any source consulted this session and is flagged here as a genuine open implementation question for the planner to scope explicitly (not a STOP-protocol semantic gap — a mechanical test-maintenance call, but one worth a deliberate task rather than silent scope creep).

### A.10 Test/evidence directory & commit conventions

`[VERIFIED: tests/phase55/, .planning/phases/55-architecture-characterization-probe/evidence/, .planning/phases/55-architecture-characterization-probe/55-VERIFICATION.md:152, all inspected this session]`

- Test invocation convention: `.venv/bin/python -m pytest tests/phase56/ -q` (mirrors the exact Phase-55 invocation `.venv/bin/python -m pytest tests/phase55/ -q` → `46 passed`).
- Test file location: `tests/phase56/` (new directory, needs its own `__init__.py`, per the `tests/phase55/` precedent).
- Evidence directory: `.planning/phases/56-contract-amendment-train-free-gate/evidence/<category>/<timestamp>/{raw.json,summary.md}` — mirrors the exact structure found at `.planning/phases/55-architecture-characterization-probe/evidence/probe/20260906T035209Z/`.
- Fixture pattern: Phase 55's exact-value regression fixture lives at `tests/phase55/fixtures/six_case_baseline.json`, protected by a session-scoped autouse SHA-256-unchanged assertion (T-55-16) — GATE-04's own SC5 pre-amendment-BLOCK demonstration test (D-08) should follow the same fixture-plus-integrity-guard pattern rather than re-deriving the pre-amendment numbers ad hoc in the test body.
- Commit convention (from CLAUDE.md, unchanged): spec edits are `spec(56)`; the `.venv` interpreter, not bare `python3`, is required for any `pinn.*` import (bare `python3` in this environment has no `torch`/`numpy` installed — confirmed this session; use `.venv/bin/python3` or `.venv/bin/python -m pytest`).

## Standard Stack

No new external dependency is introduced by this phase. GATE-04 and the spec amendment are pure-Python/stdlib (`json`, `argparse`, `dataclasses`) plus the already-pinned project dependencies `torch` (2.12.0, confirmed installed in `.venv` this session) and `numpy` (2.2.0, confirmed installed this session) — both already used identically by the Phase-55 probe this phase extends. The render-oracle (`tools/spec-render-check/`) is an existing, already-audited (Phase 22) Node toolchain; confirmed functional this session (`node v24.16.0`, `detect.mjs --selftest` → `SELFTEST PASS (G1)`).

## Package Legitimacy Audit

**Not applicable.** No `npm install`, `pip install`, or `cargo add` occurs in this phase. Every import GATE-04 needs already exists in the repo (`pinn.loss_catalog`, `pinn.verification.architecture_characterization_probe`, `pinn.training.atomic_io`, `pinn.verify`) or is a pinned, long-standing dependency (`torch`, `numpy`) already vetted by Phase 55's own `55-RESEARCH.md` Package Legitimacy Audit (`[SLOP]: none`, `[SUS]: none`). This mirrors that precedent exactly; the gate is not applicable for the same reason.

## Architecture Patterns

### System Architecture Diagram

```
54-RULING.md (ratified decision text, finished prose)
        |
        | (D-01: transcribe verbatim, do not compose)
        v
+-------------------------------------------+     +----------------------------------------------+
| TASK: spec amendment                       |     | TASK: GATE-04 module                          |
| pinn_architecture.md SS2.2/SS3.2           |     | pinn/verification/gate04_train_free.py (NEW)  |
|  - Block 1 (eta_c) AMENDED                 |     |  - argparse main(argv), __all__, frozen        |
|  - Blocks 2/3 (omega0, clip) NOT AMENDED   |     |    verdict dataclass (PASS/BLOCK + reasons)    |
|  - Block 4 (n_col/M/bins) AMENDED          |     +----------------+-------------------------------+
|  - R_ref definition + invalidation list    |                      |
+------------------+--------------------------+                      | imports
                   |                                                 v
                   | must re-run after edit          +---------------------------------------------+
                   v                                  | pinn/verification/                          |
     tools/spec-render-check/detect.mjs               |   architecture_characterization_probe.py    |
     (render-oracle; re-check + possibly              |   DEFAULT_CASES, stratified_collocation_     |
      new adjudication rows for SS3.2 prose)          |   times, bin_mean_residuals, RATIFIED_*      |
                                                       |   + NEW: ratified_causal_weights (D-05)      |
                                                       +---------------------+-----------------------+
                                                                             | calls (reuse, no fork)
                                                                             v
                                                       +---------------------------------------------+
                                                       | pinn/loss_catalog.py                         |
                                                       |   causal_physics_loss (prefix/exp/clamp)     |
                                                       |   resolve_causal_clip_facts (dtype floor)    |
                                                       +---------------------+-----------------------+
                                                                             |
                                                       6 cases x 16 bins --> 96 raw bin means
                                                                             |
                                                                             v
                                                       R_ref = median(96)  -->  persisted:
                                                       pinn/verification/artifacts/r_ref_stage0.json
                                                       (schema_version, value, cases, provenance,
                                                        invalidation triggers -- D-09)
                                                                             |
                                                                             v
                                                       per-case w_b vectors, front_idx,
                                                       conditions (i) [floor] / (ii) [OPEN: GAP-56-01]
                                                       / (iii) [front capability] evaluated
                                                                             |
                                                                             v
                                                       PASS / BLOCK verdict object
                                                                             |
                          +------------------------------------------------+
                          |
                          v
       Phase 57 RUN-04 imports gate04_train_free and calls it as a hard precondition
                          |
             +------------+-------------+
             |                          |
          BLOCK                       PASS
             |                          |
   Stage-0 run refused;      Stage-0 run may proceed;
   evaluation preserved      R_ref/verdict evidence
   (SCOPE-35)                carried forward
```

### Recommended Project Structure

```
pinn/verification/
├── architecture_characterization_probe.py   # Phase 55 (existing); + ratified_causal_weights (D-05, new function)
├── gate04_train_free.py                     # Phase 56 (new) — GATE-04 verdict logic, CLI, __all__
└── artifacts/
    └── r_ref_stage0.json                    # Phase 56 (new) — D-09 committed R_ref artifact

tests/phase56/
├── __init__.py                              # new, mirrors tests/phase55/__init__.py
├── test_gate04_train_free.py                # GATE-04 unit tests (conditions i/iii, SC5 BLOCK demonstration)
└── fixtures/
    └── pre_amendment_baseline.json          # D-08 fixture for the SC5 BLOCK-on-pre-amendment test

.planning/phases/56-contract-amendment-train-free-gate/
└── evidence/
    └── gate04/<timestamp>/{raw.json,summary.md}   # mirrors .../55-.../evidence/probe/<timestamp>/
```

### Pattern 1: Reuse the trainer's own loss function for a verification measurement

**What:** GATE-04 must never re-derive the causal-weight formula independently; it calls `pinn.loss_catalog.causal_physics_loss` with the ratified recipe's inputs (16 bin-mean residuals instead of 16 per-point residuals) and reads `return_details["w_n"]`.
**When to use:** Any verification tool measuring a trainer-owned formula (established by Phase 55's own SC3 discipline: "must derive from these, per SC3 — not reimplement").
**Example (session-verified working pattern — see Part b.1 for the full script):**
```python
# Source: pinn/loss_catalog.py:283-347 (unmodified); this call pattern verified
# working this session via .venv/bin/python3 against the live pinn package.
import numpy as np
import torch
from pinn.loss_catalog import causal_physics_loss

def ratified_causal_weights(raw_bin_means, r_ref, *, eta_c, dtype, device, t_max):
    n_bins = len(raw_bin_means)
    r_tilde = np.asarray(raw_bin_means, dtype=np.float64) / r_ref
    bin_centers = (np.arange(n_bins) + 0.5) / n_bins * t_max  # ordering proxy only
    times_t = torch.as_tensor(bin_centers, dtype=dtype, device=device)
    residual_t = torch.as_tensor(r_tilde, dtype=dtype, device=device)
    _loss, details = causal_physics_loss(
        residual_t, eta_c=eta_c, times=times_t, dtype=dtype, device=device,
        return_details=True,
    )
    return details["w_n"].detach().cpu().numpy()
```

### Pattern 2: Stratified sampling + bin reduction, already built, not yet wired for real

**What:** `stratified_collocation_times` + `bin_mean_residuals` (Phase 55) implement the exact 4096/256-per-bin/16-bin structure; GATE-04 is the first caller to wire them into a real six-case measurement.
**When to use:** Anywhere the ratified 16-bin structure is needed against real network output.
**Example:**
```python
# Source: pinn/verification/architecture_characterization_probe.py:411-508 (unmodified)
rng = np.random.default_rng(case.seed)  # "recorded probe seed" per 54-RULING.md B2
times_sorted, bin_index_sorted = stratified_collocation_times(
    n_bins=RATIFIED_N_BINS, per_bin=RATIFIED_PER_BIN, rng=rng, t_max=T_CHARACTERISTIC_TIME,
)
# ... compute rbar_np per-point exactly as measure_case() does (componentwise_du + softened_acceleration) ...
raw_bin_means = bin_mean_residuals(rbar_np, bin_index_sorted, n_bins=RATIFIED_N_BINS)
```

### Anti-Patterns to Avoid

- **Re-implementing the exp/clip formula inside `gate04_train_free.py`:** creates exactly the fork-drift risk Phase 55's T-55-03/SC3 discipline was built to prevent. Always call `causal_physics_loss`/`resolve_causal_clip_facts`.
- **Hardcoding `causal_clip_min_weight` as a literal:** the value is dtype/device-derived (`resolve_causal_clip_facts`); a copied literal silently goes stale if the runtime profile ever changes. `54-RULING.md`'s own Block 3 language and the Phase-55 probe both insist on this.
- **Trusting `54-RULING.md`'s or this document's line-number anchors after any Phase-56 edit lands:** re-derive by content match every time, per the anchor-drift warning (A.3).
- **Treating `tests/phase38/test_prohibitions.py`'s 2 failures as a Phase-56 regression signal:** they are pre-existing since Phase 53 (A.9).
- **Inventing a numeric threshold for GATE-04 condition (ii) to "unblock" the plan:** explicitly forbidden by this phase's own constraints; route to the owner using Part (b)'s data instead.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Causal-weight exp/clip/prefix-sum arithmetic | A parallel `w_n` formula inside GATE-04 | `pinn.loss_catalog.causal_physics_loss` | Already implements the exact exclusive-prefix + dtype-derived clamp; a second implementation can silently drift from the trainer's real behavior (exactly Phase 55's T-55-03 threat) |
| Dtype/device underflow floor | A hardcoded `-708.4` / `2.2e-308` literal | `pinn.loss_catalog.resolve_causal_clip_facts(dtype, device)` | Floor is derived from `torch.finfo(dtype).tiny`, not a constant; changes if the runtime profile changes (CTX-12's two allowed pairs) |
| 4096-stratified / 16-bin time sampling | A new sampler in `gate04_train_free.py` | `architecture_characterization_probe.stratified_collocation_times` | Already built, already unit-tested against synthetic arrays (Phase 55 D-03); Phase 56 is the authorized first real caller |
| Bin-mean reduction | Manual `np.mean` grouping loop | `architecture_characterization_probe.bin_mean_residuals` | Already fail-closed on empty bins / length mismatch (T-55-14) |
| JSON provenance writing | `open(path, "w").write(json.dumps(...))` | `pinn.training.atomic_io.atomic_write_text` | Atomic tmp-write + fsync + `os.replace` pattern already used by the Phase-55 probe's own evidence writer; prevents a torn/partial `R_ref` artifact |
| Case-list config validation | A new JSON schema check | `architecture_characterization_probe.SweepCase` / `load_cases_config` | Already fail-closed, validate-before-construct, tested (T-55-01, T-55-07) |
| Spec markdown/KaTeX render safety check | A manual visual inspection | `tools/spec-render-check/detect.mjs` | Purpose-built render-oracle, already audited (Phase 22), confirmed functional this session |

**Key insight:** every numerically load-bearing piece GATE-04 needs (the weight formula, the clip floor, the stratified sampler, the bin reducer) already exists, already tested, in the same repository — Phase 56's genuinely new code is the *composition* of these pieces plus the verdict/persistence layer around them, not new physics or new arithmetic.

## Common Pitfalls

### Pitfall 1: Anchor drift within the phase's own edits

**What goes wrong:** A later Phase-56 task cites a line number from an earlier task's plan or from this research document and edits the wrong content.
**Why it happens:** Every insertion into `pinn_architecture.md` shifts every subsequent line number; `54-RULING.md`'s own anchors already drifted once (Phase 53) and this document's anchors (A.3) will drift again the moment Phase 56's first spec-edit task lands.
**How to avoid:** Re-derive every anchor by content match (grep the contract-marker text) immediately before each edit, never by line number alone.
**Warning signs:** A diff that touches an unexpected line, or a render-oracle run that flags an unrelated location.

### Pitfall 2: Mistaking the SCOPE-18 pre-existing test failures for a Phase-56 regression

**What goes wrong:** A full `pytest` run shows 2 failures in `tests/phase38/test_prohibitions.py` after the spec edit lands, and the executor/verifier reads this as evidence the edit broke something.
**Why it happens:** That test file enforces a v2.0-era prohibition (SCOPE-18: "no framework-spec edits during Phase 38") that SCOPE-33 explicitly supersedes for v2.3 — but nobody has retired or updated the test itself since Phase 53 first triggered it.
**How to avoid:** Document the expected failure explicitly in the phase's verification record (as Phase 55 already did, `55-VERIFICATION.md:197`); scope a Phase-56 task to decide whether to update/retire this test file (a mechanical call, not a STOP-protocol gap — but one that should be an explicit decision, not silent scope creep, since `tests/phase38/` is not itself a framework spec under SCOPE-33's grant).
**Warning signs:** `pytest tests/phase38/test_prohibitions.py` reporting failures whose message contains "SCOPE-18 prohibits Phase-38 edits to framework specs."

### Pitfall 3: Treating `front_idx == 0` at initialization as a GATE-04 failure

**What goes wrong:** A naive implementation of condition (iii) checks `front_idx > 0` and blocks every case, including a perfectly healthy post-amendment recipe.
**Why it happens:** `front_idx` (0-indexed `max(n : w_n > 0.5)`) is 0 whenever only the trivially-always-1 first entry exceeds 0.5 — and this session's actual computation (Part b.3) shows **all six audited cases** produce `front_idx = 0` at initialization even under the ratified, non-degenerate recipe, because every case's second entry (`w_2` in spec terms) already falls below 0.5 (range 0.067-0.40 across cases).
**How to avoid:** Implement condition (iii) as the capability test `54-RULING.md` actually specifies ("a front that cannot respond to controlled residual reduction"), never as a static `front_idx > 0` check — exactly what D-06(iii) already states, now with computed confirmation of why the static check would be wrong.
**Warning signs:** GATE-04 blocking every one of the six audit cases even after the spec amendment lands correctly.

### Pitfall 4: A controlled-reduction test that perturbs only late bins will show no response, regardless of design

**What goes wrong:** A response test designed to perturb "the residuals" without specifying which bins reports zero front-index movement even at extreme perturbation magnitudes, and gets misread as evidence the recipe itself is unresponsive/broken.
**Why it happens:** `front_idx` at position `n` depends only on the exclusive prefix over bins `0..n-1` (A.6); reducing bins 8-15 can never move `front_idx` off whatever value bins 0-7 alone produce. This session's Part (b.5) computation confirms this empirically: reducing bins 8-15 by up to 100x produced **zero** front-index change in all six cases.
**How to avoid:** Any controlled-reduction test design (once GAP-56-01 is ratified) must perturb early bins (or apply uniformly) to exercise the capability it intends to test — a mechanistic, code-grounded fact, not a design recommendation this research is making.
**Warning signs:** A response test reporting "no sensitivity" when the perturbation shape itself structurally cannot produce sensitivity.

### Pitfall 5: `numpy.median`'s even-N convention vs `torch.median`

**What goes wrong:** `R_ref` (median of 96 values, even N) computed with `torch.median` silently returns the *lower* of the two central order statistics instead of their mean, producing a slightly different (and non-reproducible-by-hand) `R_ref`.
**Why it happens:** `torch.median` and `numpy.median` disagree on even-length inputs by design; the Phase-55 probe module's own docstring calls this out explicitly (`MEDIAN_CONVENTION`, lines 13-17).
**How to avoid:** Use `numpy.median` (or equivalently `float(np.median(np.concatenate(all_96_bin_means)))`) for `R_ref`, matching the already-established module convention.
**Warning signs:** A recomputed `R_ref` that doesn't match a from-scratch `numpy.median` check on the same 96 values.

## Code Examples

### Full worked computation (session-verified against the live `.venv`, not yet committed to the repo)

The following is the exact composition this session used to produce Part (b)'s data — a direct, working demonstration that `ratified_causal_weights` (D-05) can be built purely from existing, already-tested functions:

```python
# Source: composed this session from pinn/verification/architecture_characterization_probe.py
# (unmodified helpers) + pinn/loss_catalog.py (unmodified) + pinn/physics_residual.py
# (unmodified). Verified working via `.venv/bin/python3` against torch 2.12.0 / numpy 2.2.0.
from pinn.architecture_spec import ArchitectureSpec
from pinn.constants import T_CHARACTERISTIC_TIME, CAUSAL_ETA_C
from pinn.loss_catalog import causal_physics_loss, resolve_causal_clip_facts
from pinn.network import build_network
from pinn.physics_residual import componentwise_du, softened_acceleration
from pinn.runtime import resolve_runtime
from pinn.verification.architecture_characterization_probe import (
    DEFAULT_CASES, RATIFIED_N_BINS, RATIFIED_PER_BIN,
    stratified_collocation_times, bin_mean_residuals, _ic13_for_case,
)
import numpy as np, torch

def raw_bin_means_for_case(case, *, precision="float64", device="cpu"):
    runtime = resolve_runtime(precision, device)
    dtype, torch_device = runtime.dtype, runtime.torch_device
    model = build_network(ArchitectureSpec(seed=case.seed), dtype=dtype, device=torch_device)
    model.eval()
    ic13 = _ic13_for_case(case, dtype=dtype, device=torch_device)
    masses_t = torch.as_tensor(case.masses, dtype=dtype, device=torch_device)

    def traj(u_scalar):
        tau = (2.0 * u_scalar - 1.0).reshape(1)
        pos = model(torch.cat([tau, ic13], dim=0).unsqueeze(0), masses_t.unsqueeze(0))
        return pos.reshape(3, 3)

    times_sorted, bin_index = stratified_collocation_times(
        n_bins=RATIFIED_N_BINS, per_bin=RATIFIED_PER_BIN,
        rng=np.random.default_rng(case.seed), t_max=T_CHARACTERISTIC_TIME,
    )
    u_leaf = torch.as_tensor(times_sorted / T_CHARACTERISTIC_TIME, dtype=dtype, device=torch_device)
    _first, second = componentwise_du(traj, u_leaf)
    positions = torch.func.vmap(lambda s: traj(s).reshape(-1))(u_leaf).reshape(-1, 3, 3)
    force = softened_acceleration(positions, masses_t, dtype=dtype, device=torch_device)
    rbar = ((second.reshape(-1, 3, 3) - force) ** 2).sum(dim=(-2, -1)) / 3.0
    return bin_mean_residuals(rbar.detach().cpu().numpy(), bin_index, n_bins=RATIFIED_N_BINS)

# R_ref: median of 96 raw bin means across all six DEFAULT_CASES
all_96 = np.concatenate([raw_bin_means_for_case(c) for c in DEFAULT_CASES])
r_ref = float(np.median(all_96))   # numpy.median, NOT torch.median (Pitfall 5)
```

## Part (b) — GAP-56-01 Grounding Data: the Six Audited Cases' Real Post-Amendment Weight Vectors

**This section computes and reports facts only. It does not propose, invent, or select a numeric threshold, formula, or option among GAP-56-01's candidates A/B/C/D. The owner rules on condition (ii)'s pass criterion; this data is what that ruling should be made against.**

### b.1 Method

Computed this session (`.venv/bin/python3`, torch 2.12.0, numpy 2.2.0, CPU/float64) using **only** the repo's own vetted functions — `architecture_characterization_probe.DEFAULT_CASES`, `.stratified_collocation_times`, `.bin_mean_residuals`, `._ic13_for_case` (private, but the same code Phase 55's own tests exercise) and `pinn.loss_catalog.causal_physics_loss`/`resolve_causal_clip_facts` — never a reimplementation. For each of the six `DEFAULT_CASES`: built the network via `ArchitectureSpec(seed=case.seed)` (deterministic), drew exactly 4096 stratified times (256 per each of 16 fixed equal-`u` bins) seeded with `case.seed` (the "recorded probe seed" per `54-RULING.md` B2), computed the per-point residual exactly as `measure_case` does (`componentwise_du` + `softened_acceleration`), and reduced to 16 raw bin means via `bin_mean_residuals`. `R_ref` is the `numpy.median` of the resulting 96 values (6 × 16). Each case's `R̃_b = raw_bin_mean_b / R_ref`, and `w_b` is `causal_physics_loss(R̃, eta_c=1.0, times=<ascending bin-center proxy>, ...)`'s `return_details["w_n"]` — i.e., the trainer's own formula, unmodified, fed the ratified input.

**Cross-check (pre-amendment reproduction):** the same session first reproduced the *old* (`n_col=16`, unnormalized `R̄`) recipe via the already-committed `run_sweep(DEFAULT_CASES, n_col=16, ...)`. The result matches the **official committed Phase-55 evidence** (`.planning/phases/55-architecture-characterization-probe/evidence/probe/20260906T035209Z/summary.md`, committed the same day) to displayed precision exactly: `rbar_median` 1.301e10 / 1.938e10 / 1.440e10 / 1.387e10 / 1.370e10 / 1.224e10 for cases 41/42/43/0/7/41-variable-mass respectively, `front_idx=0` and 15/16 weights at the float64 tiny floor (`2.225074e-308`) for all six. (This differs slightly in exact value, but not in any qualitative respect, from the older 2026-08-17 ad-hoc audit table's numbers — `55-SECURITY.md` T-55-18 already documents this as expected, since "the original ad-hoc collocation scheme is unrecoverable"; this session's numbers agree exactly with the current committed Phase-55 artifact, which is the correct baseline to cite going forward.) This cross-check confirms the computation method (and this environment) is correct and consistent with the repo's own frozen record before trusting the new Part (b) numbers below.

### b.2 `R_ref` computed this session

```
R_ref = median of 96 raw bin means (6 cases x 16 bins) = 1.9749775821e+10
  (numpy.median even-N convention: mean of the two central order statistics
   of the sorted 96 values: 1.9597881495e+10 and 1.9901670148e+10)
  full 96-value range: min=7.035120e+09  max=9.600851e+10
causal_clip_min_weight (float64/cpu) = 2.225074e-308  (exponent floor = -708.396419)
```

**Important caveat, stated plainly:** this exact numeric `R_ref` is a byproduct of this session's specific run (this environment's `.venv`, this session's exact call sequence) and is **illustrative grounding data, not the value to hard-code into the spec or lock as "the" `R_ref`.** `54-RULING.md` ratifies the *procedure* (median of 96 raw bin means from the fixed six-case probe), not a number — GATE-04's own committed run, whenever it executes for real under Phase 56/57, computes and persists its own authoritative `R_ref` (D-09). The qualitative findings below (no floor-pinning, monotone graded vectors, the dynamic-range and dispersion figures) are expected to be robust to that recomputation — the mechanism is architectural, not RNG-sensitive, exactly as the original 2026-08-17 audit's own §6b table observed "across a different code state... for every seed and IC tried" — but the exact digits will not be bit-identical to a second real run unless the RNG seeding convention, torch build, and call sequence all match exactly.

### b.3 Per-case results — full vectors, computed this session

Summary (all six cases, ratified recipe):

| Case | seed | `front_idx` | CV(`w_2..w_16`) | Monotone non-increasing? | Dynamic range (decades) | `n` at floor (of 16) | min `w` | max `w` |
|---|---|---|---|---|---|---|---|---|
| 41 | 41 | 0 | 1.988 | Yes | 5.88 | 0 | 1.313e-06 | 1.000 |
| 42 | 42 | 0 | 3.099 | Yes | 10.68 | 0 | 2.100e-11 | 1.000 |
| 43 | 43 | 0 | 2.592 | Yes | 6.62 | 0 | 2.406e-07 | 1.000 |
| 0 | 0 | 0 | 2.618 | Yes | 7.29 | 0 | 5.102e-08 | 1.000 |
| 7 | 7 | 0 | 2.771 | Yes | 6.72 | 0 | 1.923e-07 | 1.000 |
| 41-variable-mass | 41 | 0 | 2.348 | Yes | 7.14 | 0 | 7.192e-08 | 1.000 |

Full per-case vectors (`b=0..15`; `raw_bin_means` in the network's native residual units, `R̃_b` normalized by the `R_ref` above, `w_b` the resulting causal weight):

```
--- case 41 (seed=41, masses=(1.0,1.0,1.0), ic13=zero) ---
raw_bin_means: [1.8362e10, 1.0060e10, 1.4712e10, 1.3957e10, 1.9902e10, 1.8964e10,
                2.8029e10, 1.2321e10, 2.3079e10, 1.1511e10, 9.0621e9, 2.7816e10,
                2.4808e10, 2.6028e10, 8.8588e9, 2.0194e10]
R_tilde_b:     [0.9297, 0.5094, 0.7449, 0.7067, 1.0077, 0.9602, 1.4192, 0.6239,
                1.1686, 0.5828, 0.4588, 1.4084, 1.2561, 1.3179, 0.4486, 1.0225]
w_b:           [1.0000e0, 3.9467e-1, 2.3714e-1, 1.1259e-1, 5.5535e-2, 2.0274e-2,
                7.7608e-3, 1.8774e-3, 1.0060e-3, 3.1268e-4, 1.7458e-4, 1.1034e-4,
                2.6980e-5, 7.6828e-6, 2.0566e-6, 1.3133e-6]

--- case 42 (seed=42, masses=(1.0,1.0,1.0), ic13=zero) ---
raw_bin_means: [5.1079e10, 3.7224e10, 2.5810e10, 3.2149e10, 2.7523e10, 2.4544e10,
                1.5984e10, 1.1063e10, 1.5602e10, 3.5264e10, 1.8374e10, 1.1720e10,
                2.4887e10, 7.0025e10, 8.4331e10, 9.6009e10]
R_tilde_b:     [2.5863, 1.8848, 1.3068, 1.6278, 1.3936, 1.2428, 0.8093, 0.5602,
                0.7900, 1.7855, 0.9303, 0.5934, 1.2601, 3.5456, 4.2699, 4.8612]
w_b:           [1.0000e0, 7.5298e-2, 1.1435e-2, 3.0952e-3, 6.0778e-4, 1.5084e-4,
                4.3531e-5, 1.9378e-5, 1.1067e-5, 5.0228e-6, 8.4238e-7, 3.3225e-7,
                1.8355e-7, 5.2058e-8, 1.5019e-9, 2.1000e-11]

--- case 43 (seed=43, masses=(1.0,1.0,1.0), ic13=zero) ---
raw_bin_means: [3.1511e10, 2.3385e10, 2.1816e10, 1.8654e10, 2.4390e10, 2.2506e10,
                1.0522e10, 1.4407e10, 1.6246e10, 1.7742e10, 1.2689e10, 2.3715e10,
                1.6251e10, 2.9302e10, 1.7853e10, 1.5315e10]
R_tilde_b:     [1.5955, 1.1841, 1.1046, 0.9445, 1.2350, 1.1396, 0.5328, 0.7295,
                0.8226, 0.8984, 0.6425, 1.2008, 0.8228, 1.4837, 0.9040, 0.7755]
w_b:           [1.0000e0, 2.0281e-1, 6.2066e-2, 2.0565e-2, 7.9969e-3, 2.3259e-3,
                7.4418e-4, 4.3681e-4, 2.1061e-4, 9.2521e-5, 3.7678e-5, 1.9818e-5,
                5.9644e-6, 2.6195e-6, 5.9411e-7, 2.4059e-7]

--- case 0 (seed=0, masses=(1.0,1.0,1.0), ic13=zero) ---
raw_bin_means: [3.3241e10, 2.2129e10, 2.2830e10, 2.8404e10, 3.5197e10, 1.5473e10,
                9.8074e9, 1.4311e10, 2.1263e10, 1.7978e10, 1.7510e10, 1.6752e10,
                3.2264e10, 1.4617e10, 2.9844e10, 3.0943e10]
R_tilde_b:     [1.6831, 1.1204, 1.1560, 1.4382, 1.7821, 0.7834, 0.4966, 0.7246,
                1.0766, 0.9103, 0.8866, 0.8482, 1.6336, 0.7401, 1.5111, 1.5668]
w_b:           [1.0000e0, 1.8580e-1, 6.0595e-2, 1.9072e-2, 4.5269e-3, 7.6179e-4,
                3.4801e-4, 2.1180e-4, 1.0262e-4, 3.4966e-5, 1.4071e-5, 5.7977e-6,
                2.4825e-6, 4.8463e-7, 2.3120e-7, 5.1019e-8]

--- case 7 (seed=7, masses=(1.0,1.0,1.0), ic13=zero) ---
raw_bin_means: [5.3453e10, 3.1477e10, 1.7613e10, 2.7501e10, 7.6111e9, 7.7951e9,
                9.2004e9, 7.0351e9, 1.0337e10, 7.5982e9, 7.9821e9, 3.2366e10,
                4.0309e10, 1.7667e10, 2.7472e10, 2.1865e10]
R_tilde_b:     [2.7065, 1.5938, 0.8918, 1.3925, 0.3854, 0.3947, 0.4658, 0.3562,
                0.5234, 0.3847, 0.4042, 1.6388, 2.0410, 0.8945, 1.3910, 1.1071]
w_b:           [1.0000e0, 6.6770e-2, 1.3565e-2, 5.5604e-3, 1.3815e-3, 9.3970e-4,
                6.3326e-4, 3.9743e-4, 2.7833e-4, 1.6491e-4, 1.1224e-4, 7.4927e-5,
                1.4551e-5, 1.8902e-6, 7.7272e-7, 1.9228e-7]

--- case 41-variable-mass (seed=41, masses=(1.0,0.8,0.6), ic13=random_tanh) ---
raw_bin_means: [1.7898e10, 1.4969e10, 1.9598e10, 2.8425e10, 2.7902e10, 2.6991e10,
                1.3309e10, 1.8473e10, 4.1329e10, 1.8343e10, 1.1503e10, 2.3036e10,
                1.4557e10, 1.6544e10, 3.1960e10, 3.5389e10]
R_tilde_b:     [0.9062, 0.7579, 0.9923, 1.4393, 1.4128, 1.3666, 0.6739, 0.9353,
                2.0926, 0.9288, 0.5825, 1.1664, 0.7371, 0.8377, 1.6183, 1.7919]
w_b:           [1.0000e0, 4.0404e-1, 1.8935e-1, 7.0194e-2, 1.6643e-2, 4.0521e-3,
                1.0331e-3, 5.2661e-4, 2.0667e-4, 2.5495e-5, 1.0071e-5, 5.6251e-6,
                1.7521e-6, 8.3841e-7, 3.6278e-7, 7.1920e-8]
```

**Observations, stated as observations, not as a threshold recommendation:**

- No case has any entry at or below the float64 clamp floor (`2.225e-308`) — every reported minimum weight is 6-11 orders of magnitude above it. Condition (i) is unambiguously satisfied by all six cases under this recipe, as measured this session.
- Every case's vector is monotone non-increasing (`b=0` always exactly `1.0`, decreasing thereafter) — none show the "all-equal/constant" degenerate shape GAP-56-01's mathematical-grounding section names as failure-shape 2.
- The dynamic range (5.9-10.7 decades) and dispersion (`CV` 1.99-3.10) vary meaningfully case to case — the `54-RULING.md` illustrative flat-profile estimate (endpoint weight `≈3×10⁻⁷`, "illustrative, not a guarantee") undershoots the actual observed spread in 5 of 6 cases and is close for the sixth (case 43); real per-case behavior is more extreme in some cases (case 42's minimum weight, `2.1×10⁻¹¹`, is ~4 decades past the flat-profile illustration) and less extreme in others.
- `front_idx = 0` for all six cases at initialization — consistent with, and now empirically grounding, `56-CONTEXT.md` D-06(iii)'s statement that "the healthy-init expectation is a graded weight vector, not an advanced front" (Pitfall 3, above).

### b.4 Controlled-residual-reduction sensitivity sweep (uniform scaling across all 16 bins)

Simulates "the network has partially learned, so every bin's residual shrinks together" by multiplying every case's `R̃_b` by a factor before recomputing `w_b`/`front_idx`. **Presented as raw sensitivity data only — not a proposed test design, `δ` value, or pass margin.**

| Uniform factor | 41 | 42 | 43 | 0 | 7 | 41-var-mass |
|---|---|---|---|---|---|---|
| 1.000 (no reduction) | 0 | 0 | 0 | 0 | 0 | 0 |
| 0.900 | 0 | 0 | 0 | 0 | 0 | 0 |
| 0.750 | 0 | 0 | 0 | 0 | 0 | 1 |
| 0.500 | 1 | 0 | 0 | 0 | 0 | 1 |
| 0.250 | 3 | 1 | 1 | 1 | 1 | 3 |
| 0.100 | 8 | 3 | 5 | 4 | 4 | 6 |
| 0.050 | 15 | 9 | 13 | 12 | 13 | 12 |
| 0.010 | 15 | 15 | 15 | 15 | 15 | 15 |
| 0.001 | 15 | 15 | 15 | 15 | 15 | 15 |

(cell values are `front_idx`, 0-indexed, max 15). Two structural observations: (1) `front_idx` responds monotonically to the reduction factor in every case — no case shows a non-monotone or erratic response to this perturbation shape; (2) the factor needed to move `front_idx` at all varies by roughly 2x across cases (case 41 needs only a 0.5x reduction to move off 0; cases 42/43/0/7 need 0.25x) — i.e., a fixed `δ` would not produce an identical response magnitude across all six cases, because the cases' real residual profiles differ (per the gap register's own observation that "the six audit cases have genuinely different dynamics").

### b.5 Localized late-bin reduction (alternative perturbation shape — structural finding, not a design choice)

Reducing **only** bins 8-15 (leaving bins 0-7 unchanged) by factors 0.5, 0.1, 0.01 produced `front_idx = 0` (unchanged from the unperturbed baseline) in **all six cases at every tested factor**. This is a direct consequence of the exclusive-prefix structure (A.6): `w_n` for `n ≤ 8` depends only on bins `0..n-1`, so nothing that happens to bins 8-15 can move `front_idx` off whatever bins 0-7 alone produce. This is reported as a mechanistic fact about the ratified formula, verified by direct computation — **not** as a recommendation that a controlled-reduction test should or shouldn't target particular bins; it simply means a test design that happens to perturb only late bins (for whatever reason) would report no sensitivity regardless of magnitude, and that finding would say nothing about whether the recipe is healthy.

### b.6 What this data does and does not establish

**Establishes (measured, this session, using the repo's own vetted functions — not reimplemented):** under the ratified recipe, the six audited cases produce non-floor-pinned, monotone, graded weight vectors with real case-to-case variation in dispersion and dynamic range; `front_idx = 0` at initialization is universal and expected, not a failure signal; a uniform residual reduction moves `front_idx` predictably and monotonically once a case-dependent threshold factor is crossed; a late-bin-only reduction cannot move `front_idx` regardless of magnitude, by construction.

**Does not establish:** any pass/fail numeric threshold for condition (ii); which of GAP-56-01's options A/B/C/D (or another option) the owner should choose; what `δ` or response-margin a controlled-reduction test should require; whether the specific `R_ref` value computed this session (b.2) is "the" value Phase 56's actual GATE-04 run will persist. All four of these remain for the owner to rule on, per the phase's explicit constraint.

## Part (c) — GAP-56-02 Note: §2.4 Table 1 Scope (Not Decided)

**Noted as out-of-scope-pending-owner-decision. This research does not choose a mechanism.**

Facts on record (verbatim provenance, not restated as a recommendation):

- `53-UNSWEPT-INVENTORY.md:19,29` routes §2.4 Table 1's "Recommended Value" header and the `first_omega_0 | 30` row to Phase 56 as an owner-visible item, explicitly stating that marking it during Phase 53 "would destroy the independence that is Phase 53's reason to exist" — and does not instruct Phase 56 to mark it or how.
- `pinn_architecture.md`'s existing §4.1 Phase-53 contract block (session-verified at `:688`) states: "This site is the locked-vs-default convention's first and only application in this phase... Generalization of the convention to other spec tables was explicitly NOT decided by this ruling (consequence 5), and remains open."
- `54-RULING.md:233` (session-verified) confirms the routing but adds no instruction: "Note: §2.4's hyperparameter-table row for `first_omega_0`... is already routed to Phase 56 by Phase 53's unswept inventory and is outside this file's four blocks."
- `first_omega_0` itself is ratified **NOT AMENDED** (Block 2, C1/D3-A) — so this is purely a documentation-consistency question (does a table calling a §2.2-locked constant "Recommended" need reconciling), never a value question.
- Three candidate mechanisms are already on record in `56-GAPS.md` (not this research's invention): (A) apply `[LOCKED]`/`[DEFAULT]` markers to the row and, for consistency, audit the rest of the table — generalizes the convention Phase 53 left open; (B) add a minimal header/footnote note pointing to the §2.2 lock without touching the convention; (C) leave §2.4 untouched and re-route the item to a future documentation pass. `56-CONTEXT.md`/`56-GAPS.md` already record a discuss-phase-authored lean toward (B) as "recommended" — that lean is on record from the discuss step, not from this research pass, and remains unratified.
- Session-verified render-oracle fact relevant to whichever mechanism is chosen: the existing 7 adjudication entries in `tools/spec-render-check/adjudications/22-02-pinn-architecture.json` include the exact `first_omega_0` row at line 274 and the header context at line 267 (A.8) — any edit to this table will need those entries re-verified against the post-edit line numbers, regardless of which mechanism (A/B/C) is chosen.

This research adds no new mechanism recommendation beyond what is already recorded in `56-GAPS.md`.

## State of the Art

| Old (pre-amendment) recipe | Ratified (post-amendment) recipe | When changed | Impact |
|---|---|---|---|
| `η_c` exponent consumes raw per-point `R̄_n` (unnormalized), 16 collocation points, exclusive prefix over points | `η_c` exponent consumes `R̃_b = R̄_b / R_ref` (frozen, detached), 16 fixed-`u` bins each the mean of 256 stratified points (4096 total), exclusive prefix over bins | `54-RULING.md` checkpoint ②, 2026-09-04 (Blocks 1 & 4) | Removes the ~10-decade initialization-scale mismatch between §2.2's SIREN second-derivative scale and §3.2's residual-magnitude assumption; session-computed data (Part b) shows this produces graded, non-floor-pinned vectors on all six audited cases, vs. 15/16 floor-pinned before |
| `n_col = 16` at runtime (`pinn/train.py:1033`), vs. spec's `n_col = 4096` ("recommended: 2048-4096") — an unreconciled divergence | `n_col = 4096` total per training batch is the ratified, non-tunable value; the divergence is reconciled in spec prose (FUT-01 must honor it); `pinn/train.py` itself is untouched this phase (SCOPE-33) | Same ruling (Block 4), SPEC-06 | Spec and (eventual) code converge on one number; the "recommended range" language becomes historical, not a live tunable |
| No committed, tested measurement of the initialization pathology existed anywhere in the repo — only an ad-hoc, uncommitted script behind the 2026-08-17 audit | `pinn/verification/architecture_characterization_probe.py` (Phase 55) is committed, tested (46 tests), and reproduces the audit's six-row table | Phase 55, completed 2026-09-06 | GATE-04 (this phase) is the first consumer of that committed instrument for a real governance decision |
| No fail-closed precondition existed before a Stage-0 run could be spent on a saturated recipe (v2.2's generation-3 run spent a run on exactly this pathology) | GATE-04 makes the probe a hard, fail-closed precondition on RUN-04 | This phase (GATE-04) | Directly targets the SCOPE-35 single-look-budget risk the milestone exists to close |

**Deprecated/outdated:** the §3.2 Listing-3 "recommended: 2048-4096" docstring language is superseded by the ratified fixed `4096`; the "not amended" note for `first_omega_0`/the clip means neither is deprecated — they remain exactly as locked by Phase 20/Phase 35.

## Assumptions Log

No claim in this research is tagged `[ASSUMED]`. Every factual claim is either `[VERIFIED: <path>:<lines>]` (a file this session opened with `Read` and quotes verbatim, or a computation this session ran and whose output is quoted above) or `[CITED: <path>]` (a cross-reference to another already-verified planning artifact's own characterization of a third source, e.g. `55-VERIFICATION.md`'s characterization of the pre-existing `tests/phase38` failures). No package-name, external-API, or compliance/security-standard claim occurs in this research (no new external dependency is introduced — see Package Legitimacy Audit). GAP-56-01 and GAP-56-02 are not "assumptions" in this table's sense — they are pre-existing, explicitly tracked owner gaps (`56-GAPS.md`) that this research supplies grounding data for (Parts b, c) without resolving, per the phase's hard constraint.

**This table is empty by design: no user confirmation is needed on any claim in this document.** GAP-56-01 and GAP-56-02 still require owner rulings, but that requirement is already tracked in `56-GAPS.md`/`.planning/milestones/v2.3-GAPS.md`, not newly surfaced here.

## Open Questions

1. **Is retiring/updating `tests/phase38/test_prohibitions.py`'s SCOPE-18 spec-freeze guard in Phase 56's scope?**
   - What we know: the guard is stale (superseded by SCOPE-33) and has been failing since Phase 53; Phase 55 documented it as pre-existing and out of its own scope without touching it.
   - What's unclear: whether SCOPE-33's "narrow spec-edit authorization" extends to editing this *test* file (not a framework spec itself), or whether that's a separate mechanical cleanup task outside this phase's grant.
   - Recommendation: the planner should make an explicit, deliberate scoping call here (in the plan, not silently) — either fold a small task to update the frozen baseline/retire the two stale assertions, or explicitly note the continuing failure as accepted/out-of-scope in the phase's verification record, mirroring Phase 55's precedent. This is a mechanical-scope question, not a STOP-protocol semantic gap.

2. **GATE-04 condition (ii)'s threshold and the controlled-reduction test design** — see Part (b); tracked as `GAP-56-01`, OPEN, owner-blocking for that specific wiring only.

3. **§2.4 Table 1 mechanism** — see Part (c); tracked as `GAP-56-02`, OPEN, owner-blocking for that specific cosmetic edit only.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Python (`.venv`) | All `pinn.*` imports, GATE-04, tests | Yes | Python (venv) with torch 2.12.0 | Bare `python3` on PATH has **no** torch/numpy installed (confirmed this session) — always use `.venv/bin/python3` / `.venv/bin/python -m pytest` |
| torch | Network construction, AD, loss formula | Yes | 2.12.0 (confirmed via `.venv/bin/python3 -c "import torch; print(torch.__version__)"`) | — |
| numpy | Stratified sampling, bin-mean reduction, median | Yes | 2.2.0 (confirmed same command) | — |
| Node.js | Render-oracle (`tools/spec-render-check/detect.mjs`) | Yes | v24.16.0 (confirmed via `node --version`); `--selftest` reran clean this session | — |
| pytest | Test execution | Yes (implied by Phase 55's own passing `pytest tests/phase55/` run recorded in `55-VERIFICATION.md`) | not independently re-verified this session (no direct `pytest --version` run) | `.venv/bin/python -m pytest` per established convention |

**Missing dependencies with no fallback:** none.
**Missing dependencies with fallback:** bare `python3`/`pip3` (system Python) lacks `torch`; always invoke via `.venv/bin/python3` or `.venv/bin/python -m pytest`.

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | pytest, invoked via `.venv/bin/python -m pytest` (no `pytest.ini`/`pyproject.toml` found at repo root — confirmed by direct search this session; matches Phase 55's identical setup) |
| Config file | none — pytest defaults, `unittest.TestCase`-based test classes (see `tests/phase55/test_architecture_characterization.py:1-20`) |
| Quick run command | `.venv/bin/python -m pytest tests/phase56/ -q` |
| Full suite command | `.venv/bin/python -m pytest -q` (repo-wide) — **expect exactly 2 pre-existing failures in `tests/phase38/test_prohibitions.py` unrelated to this phase's own correctness; see Pitfall 2** |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| SPEC-01 | §2.2/§3.2 amendment carries the four SCOPE-38 blocks, names the superseded ruling, re-issues the AC | render-oracle + content-match | `node tools/spec-render-check/detect.mjs --adjudications tools/spec-render-check/adjudications/22-02-pinn-architecture.json pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` | ✅ tool exists; ❌ Wave 0 needs a new content-assertion test (e.g. `tests/phase56/test_spec_amendment_contract.py`, grepping for the re-issued AC text and the "NOT AMENDED" markers) |
| SPEC-06 | `n_col` divergence reconciled in prose, re-check trigger stated | content-match | same render-oracle command; a grep-based assertion for the reconciliation sentence | ❌ Wave 0 — new test |
| GATE-04 (i)/(iii) | No floor-pinned weight; front-capability structure in place | unit | `.venv/bin/python -m pytest tests/phase56/test_gate04_train_free.py -x` | ❌ Wave 0 — new test file, new module |
| GATE-04 (ii) | Differential/non-degenerate weight vector | unit — **blocked pending GAP-56-01** | n/a until owner rules | ❌ cannot be written until the threshold exists |
| SC5 | GATE-04 BLOCKs the pre-amendment recipe | unit + fixture | `.venv/bin/python -m pytest tests/phase56/test_gate04_train_free.py -k pre_amendment_blocks -x` | ❌ Wave 0 — new fixture (`tests/phase56/fixtures/pre_amendment_baseline.json`, mirroring `tests/phase55/fixtures/six_case_baseline.json`'s pattern) |

### Sampling Rate

- **Per task commit:** `.venv/bin/python -m pytest tests/phase56/ -q`
- **Per wave merge:** `.venv/bin/python -m pytest tests/phase56/ tests/phase55/ tests/phase38/test_prohibitions.py -q` (include phase38 explicitly so the 2 pre-existing failures are visible and accounted for, not silently absent from the run)
- **Phase gate:** Full suite run before `/gsd-verify-work`, with the 2 pre-existing `tests/phase38` failures explicitly called out in the verification record (per Phase 55's precedent) rather than investigated as new.

### Wave 0 Gaps

- [ ] `tests/phase56/__init__.py` — new test package
- [ ] `tests/phase56/test_gate04_train_free.py` — GATE-04 conditions (i)/(iii), verdict object, provenance
- [ ] `tests/phase56/test_spec_amendment_contract.py` (or equivalent) — content-match assertions for the four SCOPE-38 blocks and the re-issued ACs
- [ ] `tests/phase56/fixtures/pre_amendment_baseline.json` — SC5's frozen pre-amendment comparison fixture
- [ ] Framework install: none — pytest already used identically by `tests/phase55/`

## Security Domain

This is not a network-facing or multi-user application; the ASVS web-application categories mostly do not apply. Following the exact convention Phase 55's own `55-SECURITY.md` established for this same `pinn/verification/` surface (STRIDE-categorized threat register at ASVS L1 grep-depth), adapted for Phase 56's two new surfaces (`gate04_train_free.py`, the `R_ref` JSON artifact).

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | No | No auth surface — local CLI tooling only |
| V3 Session Management | No | No sessions |
| V4 Access Control | No | No multi-principal access model |
| V5 Input Validation | Yes (narrow) | `SweepCase`/`load_cases_config`-style validate-before-construct (reuse, per Don't Hand-Roll), applied to any GATE-04 case-list config and to `R_ref` JSON on load |
| V6 Cryptography | No | No crypto surface; no secrets |

### Known Threat Patterns for this stack (STRIDE, matching `55-SECURITY.md`'s categorization convention)

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| A silently bypassable or fail-open GATE-04 (e.g., an optional flag or exception path that lets RUN-04 proceed without a verdict) | Elevation of Privilege | Fail-closed by construction: GATE-04's public return is a verdict object with no "skip" path; Phase 57's RUN-04 import must have no code path that proceeds without checking `verdict.passed` — exactly the requirement's own "fail closed... a probe failure blocks the run rather than warning about it" language |
| A corrupted or manually-edited `R_ref` JSON artifact silently accepted on load | Tampering | Re-validate-on-load against the recorded invalidation-trigger fingerprint (the `run_metadata.py` precedent, A.7) rather than trusting the file's contents unchecked |
| `R_ref` computed once but never re-checked after a structural change (architecture, `n_col`, bin count) that invalidates it | Tampering | Persist and re-check the full invalidation-trigger list verbatim from `54-RULING.md` (A.2/D-02); a load-time assertion that current runtime facts match the persisted fingerprint |
| Malformed/malicious `--cases-config` JSON for GATE-04 | Tampering | Reuse `architecture_characterization_probe.load_cases_config`'s validate-before-construct pattern (already fail-closed, tested — T-55-07) rather than a new parser |
| Non-finite intermediate (residual, prefix, or weight) silently propagating into a PASS verdict | Tampering / Repudiation | Explicit `isfinite` checks before the clamp, exactly as Block 3's re-issued AC requires ("reject non-finite residuals/prefixes before clipping") |
| Concurrent/overlapping evidence writes for the `R_ref` artifact or GATE-04 evidence | Tampering | Reuse `atomic_write_text` + non-overwriting run-directory allocation (`_new_run_dir`-style `mkdir(exist_ok=False)` + suffix retry), exactly as the Phase-55 probe already does (T-55-08) |
| Evidence/provenance record omitting git identity, dirty-tree state, or exact argv, making a GATE-04 verdict unreproducible/unauditable later | Repudiation | Reuse the probe's `_provenance()` shape (argv, command, git sha + availability, dirty flag, torch/numpy versions, timestamp) for GATE-04's own evidence writer |

No package-manager supply-chain threat applies (no new install this phase — see Package Legitimacy Audit).

## Sources

### Primary (HIGH confidence — direct `Read` this session)

- `.planning/phases/54-recalibration-decision-grounding/54-RULING.md` (full file) — the ratified decision, all four SCOPE-38 blocks, invalidation triggers, anchor-drift warning
- `.planning/phases/55-architecture-characterization-probe/55-CONTEXT.md` (full file) — Phase 55's design decisions and integration-point contract
- `pinn/verification/architecture_characterization_probe.py` (full file, 883 lines) — the reusable probe API
- `pinn/loss_catalog.py` (full file, 412 lines) — the trainer's actual causal-weight/clip formula
- `pinn/verification/gate_metrics.py` (full file) — the dataclass/docstring-contract convention
- `pinn/verification/target_frame_probe.py` (partial, header/docstring) — the symmetric-arms/fail-closed verdict precedent
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` (offsets 163-307, 383-522, 632-801) — §2.2, §2.4 Table 1, §3.2, §3.5, §4.1-4.4, all anchors re-verified
- `tests/phase38/test_prohibitions.py` (offsets 1-60, 130-160) — the stale SCOPE-18 spec-freeze guard
- `tests/phase55/test_architecture_characterization.py` (offset 1-55, plus targeted greps) — test conventions
- `runs/.calibration/stage0-timing.json` — the calibration-JSON persistence precedent
- `tools/spec-render-check/README.md`, `tools/spec-render-check/adjudications/22-02-pinn-architecture.json` — render-oracle usage and current adjudication scope
- `.planning/phases/55-architecture-characterization-probe/evidence/probe/20260906T035209Z/summary.md` — the official committed pre-amendment six-row baseline
- `.planning/phases/55-architecture-characterization-probe/55-SECURITY.md` (full file) — the security-review convention for this exact code area
- `.planning/REQUIREMENTS.md`, `.planning/ROADMAP.md` (Phase 56 sections), `.planning/STATE.md` (offsets 1-337), `.planning/phases/56-contract-amendment-train-free-gate/56-CONTEXT.md`, `56-GAPS.md` (all full files)
- `docs/work/reviews/milestone_v2.2/50-valid-stage-0-re-run/2026-08-17-residual-frame-conformance-audit.md` (offsets 115-204) — the original audit's §6a/6b/6c
- Direct computation this session: `.venv/bin/python3` running a script composed from the above unmodified functions (see Code Examples and Part b.1) — output captured verbatim into Parts b.2-b.5

### Secondary (MEDIUM confidence)

- `.planning/phases/55-architecture-characterization-probe/55-VERIFICATION.md` (targeted greps, lines 85-197) — cited for its own characterization of the pre-existing `tests/phase38` failures and exact test-invocation commands

### Tertiary (LOW confidence)

None — no WebSearch or external-only source was needed for this phase; the entire domain is in-repo.

## Metadata

**Confidence breakdown:**
- Standard stack / package legitimacy: HIGH — no new dependency, verified nothing new is needed
- Contract-amendment content (SPEC-01/SPEC-06 transcription text): HIGH — verbatim from `54-RULING.md`, session-cross-checked against the live spec anchors
- GATE-04 conditions (i)/(iii): HIGH — grounded in existing, session-read, session-executed code
- GATE-04 condition (ii) numeric threshold: N/A by design — explicitly not resolved (`GAP-56-01`); grounding data supplied instead
- §2.4 Table 1 mechanism (`GAP-56-02`): N/A by design — explicitly not resolved; facts-only note supplied
- Pitfalls (anchor drift, stale SCOPE-18 test, front_idx=0-at-init, late-bin-reduction insensitivity, median convention): HIGH — each is either a direct file quote or a this-session computed result

**Research date:** 2026-09-06
**Valid until:** Re-verify spec anchors (A.3) immediately before each edit — they are expected to drift within this same phase. The GAP-56-01 six-case data (Part b) should be treated as stable grounding evidence (the underlying architecture/formula is locked) but re-run if `54-RULING.md`'s reference-invalidation triggers fire before Phase 56 executes, or if the owner's eventual ruling asks for a different perturbation design than the two sampled here.

## RESEARCH COMPLETE
