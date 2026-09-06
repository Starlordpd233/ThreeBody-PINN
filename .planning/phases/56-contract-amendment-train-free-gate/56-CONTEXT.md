# Phase 56: Contract Amendment & Train-Free Gate - Context

**Gathered:** 2026-09-06
**Status:** Ready for planning — with two owner decisions open (GAP-56-01 HIGH, GAP-56-02 MEDIUM; see "Open Decisions" below and `56-GAPS.md`)

> **Discussion mode.** Serviced autonomously per owner instruction (2026-09-06):
> every gray area is dispositioned here with the best-reasoned option, grounded
> in `54-RULING.md`, `.planning/REQUIREMENTS.md`, the framework spec, and the
> Phase 55 tooling. The CLAUDE.md STOP protocol is **not** waived for this
> milestone: two decisions are non-grounded acceptance-check-schema / spec-
> convention calls and are surfaced as gaps rather than invented. Everything
> else below is a mechanical, operational, or test-design call in the
> discuss-phase's own lane.

<domain>
## Phase Boundary

Phase 56 does two things and demonstrates one:

1. **The contract amendment (SPEC-01 + SPEC-06).** Land the ratified
   recalibration `A1 + B2 (residual-wide) + C1 + D3 + E1` (from
   `54-RULING.md` checkpoint ②) into `pinn_architecture.md` §2.2 / §3.2 as a
   **formal SCOPE-38 contract amendment**, not a value edit: name the
   superseded ruling, record the new decision's provenance, carry a re-issued
   acceptance criterion. The `n_col` / `N_t` disposition is written in the
   **same** ratification (SPEC-06). What the amendment *says* is transcription
   of `54-RULING.md`, not fresh design.

2. **GATE-04 — the fail-closed train-free gate.** A gate that, before RUN-04
   (Phase 57) may spend the single preserved Stage-0 run, invokes the Phase 55
   INST-04 probe under the amended (SPEC-01/SPEC-06) recipe across at least the
   audit's six seed/IC cases and **blocks the run** unless the causal weight
   vector is healthy at initialization. It also computes and persists `R_ref`
   with full provenance.

3. **The demonstration (SC5).** GATE-04 fired against the *pre-amendment*
   recipe must produce a blocking failure, so a pass on the amended recipe is
   evidence rather than a no-op.

**Hard gates (both satisfied):** Phase 54 (`54-RULING.md` ratified, incl. the
`N_t` disposition — SCOPE-34) **and** Phase 55 (INST-04 probe committed,
tested, closed 2026-09-06 — the instrument GATE-04 fires).

**Out of the phase (grounded boundaries, not gray areas):**

- **No `pinn/` production-code edits.** v2.3 is framework-spec work (SCOPE-33:
  authorized edits are VER-20 items (a)–(e) + the `n_col`/`N_t` disposition
  coupled to (e)). `pinn/train.py:1033`'s `collocation_count = 16` is
  *reconciled in the amended spec prose* (SC3), not edited; the trainer rebuild
  is FUT-01. GATE-04 lives in `pinn/verification/` (a probe/tool area), never
  in the trainer.
- **No second-optimizer-phase / L-BFGS semantics.** GAP-54-06 is DEFERRED to
  Phase 57 owner checkpoint ③, before any RUN-04. `54-RULING.md`: "Phase 56
  may implement and gate the five ratified surfaces; it may not silently choose
  either second-optimizer-phase behavior." GATE-04 is Adam-initialization /
  train-free only.
- **No invariant-B window (`N = 500`) re-ratification, no front-monitoring
  aggregation choice.** Both are Phase 57 owner checkpoint ③. A resampled
  training-batch `front_idx` is diagnostic only (`54-RULING.md`
  "Front-monitoring boundary").
- **`first_omega_0` is NOT AMENDED.** Ratified `C1`/`D3-A`; Phase 20 ARCH-01
  remains its acceptance criterion. Phase 56 records "not amended," it does not
  delete the block (`54-RULING.md` Block 2).
- **The clip's underflow-only purpose is NOT AMENDED.** Ratified `E1`/`D5-A`;
  the dtype/device normal-floor guard `B = -log(finfo(dtype).tiny)` and the
  Phase 35 deferred-numeric-bound guard stand. Added logging + GATE-04 refusal
  behavior is observability, "not a repurposing of the clip" (`54-RULING.md`
  Block 3).
- **No widening of GATE-04 to a physics-loss-magnitude condition.** The
  "surviving pathology" concern (a weight-vector repair that passes the gate
  while a gradient-magnitude imbalance survives) was adjudicated at GAP-54-02
  and closed: *do not widen the authorized surface set.* The ruling's `B2`
  (residual-wide) answer applies `R̃_b = R̄_b/R_ref` to the **outer training
  physics loss** as well as the causal exponent — that is the grounded
  response, not a new gate condition.
- **The single held-out evaluation stays unspent** (SCOPE-35). If GATE-04
  refuses, the milestone routes to a `rethink`-flavoured DIAG-06 with the
  evaluation preserved (Declared Terminal State).

</domain>

<decisions>
## Implementation Decisions

### 1. Contract-amendment structure (SPEC-01, SCOPE-38)

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

### 2. GATE-04 implementation (GATE-04)

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

### 3. `R_ref` persistence & governance

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

### 4. Secondary wordings the amendment forces

- **D-10: `§4.1` `η_c = 1` default wording (currently `:647`).** 53-RESEARCH
  flagged this as a SCOPE-38-marked, Phase-56-coupled site. `η_c` keeps the
  value `1` but its exponent argument changes; update this line's cross-
  reference/wording so it is consistent with the amended §3.2 block (point at
  the re-issued AC; do not restate the formula). Byte-preserve the value.

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
  of the demonstration margin.

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
  cosmetic edit; nothing else in the phase.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase scope & the ratified decision (authorizing sources)
- `.planning/phases/54-recalibration-decision-grounding/54-RULING.md` — **the
  authorizing source; Phase 56 may not proceed without it (SCOPE-34).** Read in
  full: the checkpoint-② table (per-surface dispositions `A1`/`B2`/`C1`/`D3`/
  `E1`), the "Checkpoint ② discharge — scientific basis" section (5 decisive
  mechanics, the batch-allocation/bin policy, the reference-invalidation
  trigger list, the optimizer-phase and front-monitoring boundaries), the four
  "SCOPE-38 re-ratification lines" blocks (Block 1 & Block 4 carry the two
  verbatim re-issued acceptance criteria), and the **"Anchor-drift warning
  (for Phase 56)"** section at the end.
- `.planning/ROADMAP.md` "Phase 56: Contract Amendment & Train-Free Gate" —
  goal, dependencies, the 5 success criteria (SC1–SC5), execution-order note.
- `.planning/REQUIREMENTS.md` — SPEC-01, SPEC-06, GATE-04 (verbatim);
  SCOPE-33 (narrow spec-edit authorization), SCOPE-34 (owner-ratified
  decision + the checkpoint-② delegation exception), SCOPE-35 (single held-out
  evaluation), SCOPE-37 (post-edit iteration is conformance-only), SCOPE-38
  (amend-a-locked-contract discipline); "Owner Checkpoints" 3 & 4 (Phase 57);
  "Declared Terminal State".
- `.planning/milestones/v2.3-GAPS.md` — GAP-54-01..11 dispositions; note
  GAP-54-02 (do not widen GATE-04), GAP-54-03 (`R_ref` from the GATE-04 probe),
  GAP-54-05 (`n_col = 4096` total, GAP-39-12 unit), GAP-54-06 (DEFERRED to
  Phase 57 ③).

### The spec being amended
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` —
  §2.2 (SIREN init, `first_omega_0` fixed-at-30 sentence), §2.4 Table 1
  (hyperparameter table), §3.2 (per-time residual `R̄`, `w_n` causal-weight
  formula, `L_phys^causal`, the Phase 35 contract block, Listing 3 collocation
  sampling), §4.1 (`η_c = 1` default wording, the existing `**[LOCKED]**`
  markers + Phase 53 locked-vs-default contract block), the loss-catalog `where`
  block carrying the clip's "required only to avoid underflow" sentence.
  **Every anchor in the docs above is line-drifted — re-derive by content
  match, never trust a line number** (see `54-RULING.md` anchor-drift warning:
  `:424→:445`, `:167→:181`, `:433→:454`, `:440→:461`; Phase 53's `spec(53)`
  commits shifted lines again after that).

### The instrument GATE-04 fires
- `.planning/phases/55-architecture-characterization-probe/55-CONTEXT.md` —
  the probe's design decisions (D-01 two-tier regression gate, D-02
  config-driven sweep, **D-03: the 4096/16-bin capability was built but
  deliberately not exercised as a Phase-55 artifact — running it for real is
  Phase 56's job**), integration-point note (keep the public API stable).
- `pinn/verification/architecture_characterization_probe.py` — `__all__`:
  `SweepCase`, `ArchitectureCharacterizationResult`, `DEFAULT_CASES`,
  `measure_case`, `run_sweep`, `load_cases_config`,
  `stratified_collocation_times`, `bin_mean_residuals`; imports
  `resolve_causal_clip_facts` from `pinn.loss_catalog`.
- `pinn/verification/gate_metrics.py` — the dataclass-result + exhaustive-
  docstring-contract convention to mirror for GATE-04's result type.
- `pinn/loss_catalog.py::causal_physics_loss(..., return_details=True)` and
  `resolve_causal_clip_facts` — the trainer's own causal-weight + clip-facts
  functions; derive from these, never re-implement.

### The measurement being reproduced / demonstrated against
- `docs/work/reviews/milestone_v2.2/50-valid-stage-0-re-run/2026-08-17-residual-frame-conformance-audit.md`
  §6a (the retained seed-41 log: `w_min` at the float32 tiny clamp on 502/502
  steps, `front_idx = 0`), §6b (the six-row initialization table GATE-04's
  default cases come from), §6c (mechanism narrative).

### Prior-phase context
- `.planning/phases/53-narrow-spec-codification/53-UNSWEPT-INVENTORY.md` —
  item 1 (§2.4 Table 1 header + `first_omega_0` row → Phase 56) and item 5
  (§3.2 `n_col` "recommended" wording → Phase 56 / SPEC-06).
- `.planning/phases/53-narrow-spec-codification/53-01-PLAN.md` — the render-
  oracle gate (`node tools/spec-render-check/detect.mjs --adjudications
  tools/spec-render-check/adjudications/22-02-pinn-architecture.json ...`) and
  the SCOPE-38 negative-diff discipline (`git diff -U0 ... | grep -E
  'eta_c|first_omega_0|underflow'` must be empty *for contract-marked lines
  that are NOT being amended*) — carry both forward, adapted: Phase 56 *does*
  change the `eta_c` block, so the negative-diff guard applies to Blocks 2 & 3
  (first_omega_0, underflow) only.
- `.planning/phases/54-recalibration-decision-grounding/54-CONTEXT.md` Open
  Item 5 (anchor re-derivation is Phase 56's responsibility).

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- **`pinn/verification/architecture_characterization_probe.py`** — the whole
  Phase 55 probe. `run_sweep` / `measure_case` give the six-case initialization
  sweep; `stratified_collocation_times` + `bin_mean_residuals` +
  `RATIFIED_N_BINS` are the pre-built (Phase 55 plan 55-03) helpers for the
  4096-stratified / 256-per-bin / 16-bin structure GATE-04 needs. GATE-04 adds
  a `ratified_causal_weights`-style pure function here (D-05) and consumes the
  result dataclass.
- **`pinn/loss_catalog.py::resolve_causal_clip_facts(dtype, device)`** —
  returns `causal_clip_min_weight` (the dtype clamp floor) for the runtime;
  GATE-04 condition (i) compares against this, never a literal.
- **`pinn/loss_catalog.py::causal_physics_loss(rbar, times=..., return_details=
  True)`** — returns `{"w_n": ..., "rbar": ...}`; the trainer causal-weight
  path the probe already derives from.
- **`pinn/verification/gate_metrics.py`** — `TrajectoryGateMetrics` /
  `AggregateGateMetrics` frozen-dataclass + threshold-naming-docstring pattern.
- **`pinn/verification/target_frame_probe.py`** — a `*_probe.py` with a
  symmetric-arms + fail-closed verdict object; closest structural analog for
  GATE-04's `PASS`/`BLOCK` verdict.
- **`tools/spec-render-check/detect.mjs`** + `adjudications/22-02-pinn-
  architecture.json` — the spec render-oracle Phase 53 ran before every commit;
  Phase 56 re-runs it (the adjudicated-token baseline shifts because §2.2/§3.2
  change — expect to update the adjudication file, which is itself in scope as
  part of the edit).

### Established Patterns
- Every `pinn/verification/*_probe.py` is a standalone script (`argparse`
  `main(argv=None)`, `__all__` for library use) with **no wiring into any
  verify ladder or CI gate**. GATE-04 follows this; Phase 57 imports it.
- SCOPE-38 commit discipline (Phase 53): per-commit negative-diff assertion on
  contract-marked lines + render-oracle + `git diff --check`. Phase 56 adapts:
  the `eta_c`/§3.2 block is legitimately changing (Block 1/4), so the guard
  narrows to `first_omega_0` and `underflow` (Blocks 2/3, NOT AMENDED).
- Per-phase test dirs: `tests/phase56/`. Evidence:
  `.planning/phases/56-*/evidence/<category>/<timestamp>/`.
- `agent-commit` with `GIT_AGENT_ID` + `GIT_AGENT_OWNED_PATHS`; conventional
  commits, two-digit phase scope `56` (or `56-NN` per task); body required for
  `spec` / `plan` / `.planning/` touches. Spec edits are `spec(56)`.

### Integration Points
- **Phase 57 RUN-04** imports `gate04_train_free` and calls it as a hard
  precondition; its return contract (verdict + `R_ref` path) must be stable.
- **`R_ref` JSON** (D-09) is read by Phase 57 and every subsequent Stage-0 run;
  its schema is a downstream contract.
- **FUT-01 trainer rebuild** consumes the amended §3.2 as the spec of record
  for the causal loss — the amendment's precision is what FUT-01 builds from.

</code_context>

<specifics>
## Specific Ideas

- The two verbatim re-issued acceptance criteria already exist as finished text
  in `54-RULING.md` Block 1 ("Re-issued acceptance criterion: AC-LOSS-04 is
  re-issued without a new identifier: ...") and Block 4 ("Re-issued acceptance
  criterion: A full 256-slot batch emits exactly 4096 physics rows ..."). The
  executor copies these into the spec, it does not rewrite them.
- The bin-edge / empty-bin / 240-slot-replay policy is fully specified in
  `54-RULING.md` "Batch allocation and bin policy" — transcribe it into §3.2,
  do not paraphrase.

</specifics>

<deferred>
## Deferred Ideas

- **Second-optimizer-phase / L-BFGS causal-weight recomputation semantics** —
  GAP-54-06, DEFERRED to Phase 57 owner checkpoint ③, before RUN-04. Not Phase
  56.
- **Invariant-B monitoring window (`N = 500`) re-ratification** and the
  **front-monitoring aggregation estimator** — Phase 57 owner checkpoint ③.
- **Pre-registration of the EVAL-02 spending seed** — Phase 57 owner
  checkpoint 4.
- **Power-skip stack as a capacity surface** — GAP-54-02 closed it as a future
  ablation; not reopened.

### Reviewed Todos (not folded)
- **d-06-static-epsilon-sensitivity-check** (score 0.6, keyword-only match on
  "check"/"over"/"phase") — a spec-side `epsilon_soft` dual-context sensitivity
  question with no VER-20 routing; folding it would breach SCOPE-33's narrow
  spec-edit authorization. Phase 55 also reviewed and did not fold it. Remains
  in `.planning/todos/pending/`; revisit at milestone close.
- **trainex-r1-research-handoff** (the r1b tuning round) — unrelated to Phase
  56 scope; not folded.

</deferred>

---

*Phase: 56-Contract Amendment & Train-Free Gate*
*Context gathered: 2026-09-06*
