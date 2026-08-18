# Phase 47: Frame Completion & S_H Pipeline - Context

**Gathered:** 2026-07-29
**Status:** Ready for planning

**Discussion mode:** the owner elected a non-interactive session — *"discuss and
surface all sections and areas; then, automatically choose the best option
following your own best judgement."* Every gray area below was surfaced and
resolved in one pass without an interactive selection round.

**How to read the decisions:** each carries a provenance tag.

- **[GROUNDED]** — the answer is stated in a spec, requirement, roadmap entry, or
  owner ruling. Cited inline. **Not** an agent choice; a planner may not vary it.
- **[JUDGEMENT]** — genuinely undetermined by any source; chosen by the agent
  under the owner's delegation, with the rationale recorded. Revisable by the
  owner without disturbing any [GROUNDED] decision.

<domain>
## Phase Boundary

Two changes, in a load-bearing order.

**First (CONF-09)** the training path starts running in the frame the specs
lock. The resident position and velocity series move from the intermediate
COM/boost-gauged, canonically-ordered arrays to the fully rotation-gauged and
`D`/`V`-scaled arrays the preprocessing pipeline already computes, and
`RATIFIED_VALIDATION_FRAME` is re-ratified to the scaled contract in the same
change.

**Then (CONF-02, CONF-03)** the loss's energy scale becomes a real dataset
statistic computed in that completed frame: `S_H = median_train(K0 + Uabs0)`,
persisted in training metadata with fail-closed validation, consumed as
`ε_H = 1e-4 · S_H`, with the spec-prohibited `+1e-12` additive floor removed.

The order is not stylistic. `S_H` is frame-dependent (`H' = D·H`), so computing
it before the frame is completed means computing it twice.

**Not in this phase:** any training run, any held-out evaluation, any
framework-spec edit, any loss-math repair beyond the `ε_H` wiring (CONF-04..07
are Phase 48), and any hyperparameter chosen against an observed result.

</domain>

<decisions>
## Implementation Decisions

### CONF-09 — residency completion

- **D-01 [GROUNDED — `.planning/REQUIREMENTS.md` CONF-09]** The resident series
  move from `pre.r_com_ordered` / `pre.v_com_ordered` to `pre.r_gauge` /
  `pre.v_gauge` at `pinn/data/adapter.py:865-866`. The two snapshot-count
  references at `:871` and `:875` re-point to `pre.r_gauge.shape[0]` in the same
  change — identical value, but the residency source must be named once.

- **D-02 [GROUNDED — ROADMAP Phase 47 SC-1]** Time handling does **not** move.
  Residents keep native `parsed_brutus.times`; the `u = t/T` normalization stays
  at the sampling boundary in `pinn/data/batches.py`. CONF-09 is what makes the
  existing arrangement coherent rather than something to work around: with
  scaled positions, `dr'/du = (T/D)·v_rot = v_gauge` holds exactly, so the
  velocity target is `pre.v_gauge` precisely because the AD derivative is taken
  with respect to `u`. A plan that also rewrites time normalization has
  misread the defect.

- **D-03 [JUDGEMENT]** `r_com_ordered` / `v_com_ordered` remain on
  `PreprocessedTrajectory` after the swap. They stop being the residency source
  but are still the intermediate the CONF-08 evidence and its tests are written
  against. Deleting them is a separate cleanup that would widen this diff into
  files CONF-09 has no reason to touch. Note them as no-longer-resident in the
  plan summary instead.

- **D-04 [GROUNDED — verified against source]** `IC₁₃` and `E` are **unchanged**
  by CONF-09 and the phase must assert that rather than adjust them.
  `pinn/data/adapter.py:847-849` already builds both from `pre.r0_gauge` /
  `pre.v0_gauge`, and `pinn/data/preprocessing.py:217-219` sets
  `r0_gauge = r_scaled[0]` with `r_gauge = r_scaled` — so `pre.r_gauge[0]` **is**
  `pre.r0_gauge`, elementwise. The input side has always been canonical; CONF-09
  closes the gap between a canonical input and a raw-frame target. Any plan that
  edits `IC₁₃` construction is outside the contract.

### CONF-09 — frame re-ratification and test correction

- **D-05 [GROUNDED — REQUIREMENTS CONF-09; ROADMAP SC-2]**
  `RATIFIED_VALIDATION_FRAME` is re-ratified to
  `(POSITION_FRAME_SCALED, TIME_COORD_NORMALIZED, MASS_CONVENTION_ORDERED_RAW)`
  in the **same change** as the residency swap, per
  `pinn/training/validation_gate.py:526-528`. Not a follow-up commit: a tree in
  which residency has moved and the frame constant has not is a tree whose
  `COHERENT_FRAME_PAIRS` check is lying.

- **D-06 [JUDGEMENT]** `tests/phase46/test_pairing_repair.py` — the only file in
  the tree encoding the current resident pairing — is **corrected in place**, not
  superseded by a new Phase 47 file. A parallel test asserting the opposite frame
  would leave two competing oracles for the same property, which is the exact
  "competing metric oracle" failure `46-CONTEXT.md` warns against. Its CONF-08
  assertions that remain true (permutation applied, `plus_permutation = 0.0`,
  membership and accounting unchanged) stay as-is; only the assertions encoding
  *"deliberately without rotation gauge or D/V scaling"* move to the completed
  contract. New invariants get new Phase 47 tests.

- **D-07 [JUDGEMENT]** Re-ratification is recorded as a Phase 47 artifact stating
  what superseded what and on whose authority (the GAP-46-07 owner ruling of
  2026-07-28, option A), under the same D-12 discipline GAP-46-06 used. This is
  bookkeeping on an existing ruling, **not** a new gap and not a new decision to
  surface — GAP-46-06's own constant declared this staleness condition in
  advance.

- **D-08 [GROUNDED on the claim, JUDGEMENT on the check]** The ROADMAP states
  gate metrics are unchanged in value because `ε_H` is a relative drift,
  invariant under uniform `H → D·H`. Record a measured before/after comparison
  as regression evidence — but assert **approximate** invariance with a stated
  tolerance, not exact equality. The softening is not uniformly scaled:
  `EPS_SOFT = 1e-5` is a scaled-frame softening currently applied to raw
  positions, so the `r_safe = √(‖Δr‖² + ε²)` floor contributes differently in the
  two frames. Expect agreement to well within tolerance for ordinary separations
  and a visible difference only where the softening floor binds. A strict
  equality assertion here would fail for a correct implementation.

### CONF-02 — computing S_H

The governing text is `pinn_architecture.md` §3.4, lines 539-542, verbatim:

> *"$S_H$ is computed once in float64 after final COM/zero-momentum/gauge/scaling
> preprocessing over the training split using the matched-Plummer Hamiltonian
> components with $\epsilon_{train} = 10^{-5}$."*

Nearly every choice this phase might have deliberated is settled there.

- **D-09 [GROUNDED — `pinn_architecture.md:539-542`, reinforced at `:544`]**
  `S_H` uses the **matched-Plummer Hamiltonian components** at
  `ε_train = EPS_SOFT = 1e-5`. It does **not** use `EPS_INV = 1e-10`.
  `pinn/data/preprocessing.py::compute_invariants` is therefore **not** the
  source for these terms despite computing structurally identical ones — it
  softens at `EPS_INV = 1e-10` and returns only the signed sum `E`. §3.4's
  dual-epsilon note (VAL-03, line 544) makes conflating the two softenings an
  explicit conformance error, and `pinn/verification/gate_metrics.py:145` carries
  the matching "NEVER" warning on the other side. This is the single easiest way
  to silently mis-scale `ε_H` across the whole milestone.

- **D-10 [GROUNDED — `pinn_architecture.md:533`]** `K0 + Uabs0` is evaluated at
  the **initial snapshot** in the completed frame: `K0` is the dimensionless
  kinetic term `½ Σᵢ mᵢ‖v'ᵢ‖²`, and `Uabs0` is the **absolute value** of the
  softened potential. Since `V_ε < 0`, `Uabs0 = −potential`. Note
  `K0 + Uabs0 ≠ H_0` — `H_0 = K0 + V_ε` is the signed sum and is a different
  quantity that appears separately in the same denominator. Conflating them is a
  live risk because both are computed by the same helper.

- **D-11 [JUDGEMENT]** Expose the two components through a component-returning
  seam in `pinn/loss_catalog.py` that the existing
  `_matched_plummer_hamiltonian` delegates to, preserving its current signature
  and return value exactly. Its body already computes `kinetic` and `potential`
  as separate locals before summing them, so this is an extraction, not new
  physics. Rationale: one home for the softened-potential loop. A second
  implementation of that pairwise sum is how the two softenings drift apart.

- **D-12 [GROUNDED on float64, JUDGEMENT on placement]** Per-trajectory
  `(K0, Uabs0)` are computed in **float64 at admission**, from
  `pre.r_gauge[0]` / `pre.v_gauge[0]` where the float64 preprocessing output is
  in hand, carried on the candidate record, and exposed through a `StageIndex`
  accessor following the established `_source_value` pattern
  (`pinn/data/splits.py:209`). Rationale: `StageIndex.snapshot_positions`
  returns the **fp32** resident tensors, so reducing the median from residents
  would violate §3.4's float64 requirement while looking perfectly reasonable.
  Computing at admission also satisfies "after final … preprocessing" literally
  — these are that stage's outputs.

- **D-13 [GROUNDED — `pinn_architecture.md:539-540`, `:548`]** The median reduces
  over the **train split only**, once, at run setup before step 1, via
  `StageIndex.from_split(adapter, manifest, "train")` (`pinn/data/splits.py:170`)
  intersected with the Stage-0 admitted set. Never per-minibatch, never
  per-stage, never recomputed mid-run — §3.4:548 names "computes `S_H` per
  minibatch" and "from a different split or preprocessing stage" as divergences
  the FUT-01 handoff must flag.

- **D-14 [JUDGEMENT]** Median convention: `numpy.median` in float64 over the
  train-split component sums, which averages the two central values on an even
  population. Persist `N_train` beside `S_H` so the value is re-derivable from
  the split manifest without re-running admission.

### CONF-02 — persistence and fail-closed validation

- **D-15 [GROUNDED — `pinn_architecture.md:542`]** **Both** `S_H` **and** `ε_H`
  persist in training metadata. Not `S_H` alone — §3.4:547 flags metadata that
  "omits `S_H` or `ε_H`" as divergent.

- **D-16 [JUDGEMENT]** Persist to a dedicated `run_dir/training_metadata.json`,
  written once at setup before step 1, carrying `S_H`, `ε_H`, `N_train`,
  `eps_train`, the `energy_floor_factor` used, and the ratified frame tuple.
  Rationale: `config.yaml` is the frozen *config* and `S_H` is derived data, not
  configuration; `status.json` is run status; `splits.json` is the split
  manifest. A dedicated artifact gives the §3.4:546-550 divergence check exactly
  one path to look at. The planner may instead extend an existing run-metadata
  artifact if one already fills this role — provided both values are present,
  float64-exact, and fail-closed.

- **D-17 [GROUNDED on the predicate, JUDGEMENT on timing]** Non-finite or `≤ 0`
  `S_H` is a preprocessing/metadata validation failure. No fallback floor, no
  `max()`, no clamp — §3.4:542 says *"Do not apply a fallback numeric floor"* and
  `:549` names a "max/fallback floor" as divergent. Failure happens at
  **setup, before step 1**, not lazily at first use: a run that cannot produce a
  valid `ε_H` must never emit a single step, because a partially-completed run
  leaves artifacts that read like real evidence.

- **D-18 [JUDGEMENT]** The reader re-validates on load under the same
  predicate, so a truncated or hand-edited metadata file cannot silently
  re-enter the loss. This mirrors the semantic-recomputation discipline Phase 46
  established in `validate_sidecar_payload` — a persisted number is trusted only
  after it has been re-checked, never because it is present.

### CONF-03 — ε_H wiring and floor removal

- **D-19 [GROUNDED — REQUIREMENTS CONF-03; `pinn_architecture.md:531`]**
  `pinn/training/controllers.py:482` becomes `ε_H = 1e-4 · S_H` sourced from the
  validated metadata, and the `+ 1e-12` term is deleted outright rather than
  made configurable or conditional. `stage.energy_floor_factor`
  (`pinn/training/config.py:161`, value `1e-4`) remains the named home of the
  `1e-4` factor. The comment at `:480-481` calling the floor "a numeric-safety
  zero-denominator guard" is the exact rationalization §3.4 prohibits, and goes
  with the line.

- **D-20 [GROUNDED — `pinn_architecture.md:542`]** *"Use `ε_H` only in
  `|H_0| + ε_H`."* The per-anchor `abs(h0)` **stays** in the denominator at
  `pinn/loss_catalog.py:284`; what changes is only where the `ε` scale comes
  from — per-anchor `abs(h0) · 1e-4` becomes dataset-wide `1e-4 · S_H`. The
  present code is not wrong because it uses `h0` in the denominator; it is wrong
  because it uses `h0` as the *scale*, which makes every anchor its own
  yardstick.

- **D-21 [JUDGEMENT]** `_AnchorContext` keeps an `eps_h` field, injected with the
  run-level constant, rather than reading a module global. Identical value
  across anchors, but the existing per-test override seam that controller tests
  depend on survives.

### Regression evidence

- **D-22 [GROUNDED on permission, JUDGEMENT on spending it]** Run the permitted
  CONF-01 re-probe **once**, recorded explicitly as a regression check that
  residency equals the canonical preprocessing output. Per the ROADMAP's Phase 47
  boundaries, `identity_scaled` becomes true by construction and it is no longer
  a frame test — so it must not be presented as a new CONF-01 verdict, and its
  numbers may not steer implementation (SCOPE-29). Worth spending because it is
  the cheapest end-to-end confirmation that the swap reached the surface the
  probe reads.

- **D-23 [JUDGEMENT]** Record the D-08 before/after gate-metric comparison
  alongside it. Together the two answer "did residency change?" and "did anything
  observable change that shouldn't have?"

### Governance and scope locks

- **D-24 [GROUNDED — SCOPE-27..32]** No training run, no held-out evaluation, no
  framework-spec edit. Noted for routing, not for action: §3.4:542 contains an
  author comment — *"I am not sure why there is a duplicate 10^-5 here"* — which
  is a **VER-20 spec-amendment routing candidate**, not a Phase 47 edit. The
  `ε_train = 1e-5` value itself is unambiguous and is used as written.

- **D-25 [GROUNDED — Phase 46 D-26 precedent]** The conformance audit's
  verified-clean component section stays closed. This phase moves a frame and
  builds a statistic; it does not re-litigate force, Hamiltonian, projection, AD,
  or gate-formula math.

- **D-26 [GROUNDED — SCOPE-29]** Conformance-only. Loss magnitudes will move
  substantially, and that is the frame becoming the locked one — not a
  hyperparameter fitted to an observed result. No sensitivity sweep, no
  comparison shopping between softenings, no tuning of `1e-4`.

- **D-27 [GROUNDED — GAP-46-06/07]** CONF-01's Complete status and its mandatory
  EVAL-01 precondition-(ii) qualification are unchanged by this phase. CONF-09
  applies CONF-01's answer; it does not re-decide it.

### Claude's Discretion

The owner delegated all gray-area selection for this session. The
**[JUDGEMENT]** decisions are D-03, D-06, D-07, D-08 (check design), D-11, D-12
(placement), D-14, D-16, D-17 (timing), D-18, D-21, D-22 (spending), and D-23.
Each is revisable on owner instruction without disturbing any **[GROUNDED]**
decision.

Beyond those, the planner may choose module and helper names, the metadata
field layout inside the artifact chosen in D-16, test file organization, and
fixture construction — provided every decision above is preserved, no dependency
is added, and no new cadence, threshold, tuning signal, or evaluator path is
created.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase scope and owner-ratified boundaries

- `.planning/ROADMAP.md` §"Phase 47: Frame Completion & S_H Pipeline" (lines
  113-126) — goal, the five success criteria, the strict CONF-09 → CONF-02 →
  CONF-03 order, and the boundaries carried from the GAP-46-07 ruling.
- `.planning/REQUIREMENTS.md` — CONF-09 (line 44), CONF-02 (36), CONF-03 (37),
  the EVAL-01 policy, SCOPE-27..32, and the 2026-07-28 GAP-46-07 amendment
  (line 141).
- `.planning/PROJECT.md` — active v2.2 milestone, evaluation policy, branch
  timing.
- `docs/work/reviews/cross_cutting/stage0-conformance-audit/2026-07-28-conformance-divergence-verification-report.md`
  — the verification that surfaced CONF-09, with the derivations for all three
  defects it repairs.
- `CLAUDE.md` / `AGENTS.md` — gap protocol, Git policy, source-of-truth rules.

### The governing spec contract

- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md`
  §3.4 lines 518-553 — **the single most important reference for this phase.**
  `ε_H = 1e-4·S_H` (531), `S_H = median_train(K0 + Uabs0)` (533), the
  computation contract (539-542), the dual-epsilon separation note (544), and
  the FUT-01 divergence list (546-550) which functions as the acceptance
  checklist.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md`
  — the one shared COM/boost/order/gauge/scale convention,
  `r_true_prime_ordered_gauge`, `u = t/T`; line 579 cross-references the same
  `ε_H = 1e-4·S_H` contract.

### Grounding and inherited rulings

- `.planning/milestones/v2.2-GAPS.md` — GAP-46-06 (frame ratification, option B)
  and GAP-46-07 (CONF-09, option A) in full.
- `.planning/phases/46-frame-resolution-gate-aligned-validation/46-CONTEXT.md`
  — Phase 46's locked decisions, reusable-asset inventory, and the
  "competing metric oracle" warning D-06 relies on.
- `.planning/phases/46-frame-resolution-gate-aligned-validation/46-VERDICT-POSTREPAIR.md`
  — the post-CONF-08 probe verdict CONF-09 builds on.
- `docs/work/reviews/cross_cutting/stage0-conformance-audit/2026-07-24-stage0-training-path-conformance-audit.md`
  — C-01..C-08 plus the equally binding verified-clean section (D-25).

### Code seams this phase touches

- `pinn/data/adapter.py:861-875` — the residency construction site (D-01).
- `pinn/data/preprocessing.py:174-220` — `preprocess_trajectory`, its transform
  order, and the `PreprocessedTrajectory` fields including the
  `r0_gauge = r_scaled[0]` identity D-04 depends on.
- `pinn/loss_catalog.py:141-160` (softened potential), `:275-284`
  (`denom = |h0| + ε_H`), and `_matched_plummer_hamiltonian` — the component
  extraction site (D-11) and the single legal `ε_H` use site (D-20).
- `pinn/training/controllers.py:455-500` — `h0`/`l0`/`eps_h` construction; line
  482 is the CONF-03 defect.
- `pinn/training/validation_gate.py:526-528` — `RATIFIED_VALIDATION_FRAME` and
  the `COHERENT_FRAME_PAIRS` admission check (D-05).
- `pinn/data/splits.py:170` (`from_split`), `:209` (`_source_value`) — the train
  split and the accessor pattern for D-12/D-13.
- `pinn/constants.py:38-39` (`EPS_SOFT = 1e-5`) and
  `pinn/verification/gate_metrics.py:59,145` (`EPS_INV = 1e-10` + its "NEVER"
  warning) — the two softenings D-09 must keep apart.
- `tests/phase46/test_pairing_repair.py` — the one test encoding the superseded
  pairing (D-06).

### Explicitly excluded source

- `pinn_instruction/markdown_conversion/framework-specs/trainex-r2/` is **not** a
  grounding source (SCOPE-31). Do not consult its tuning analysis.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets

- `preprocess_trajectory` already computes everything CONF-09 needs. `r_gauge` /
  `v_gauge` are returned today and currently flow only to the target-frame
  probe (`pinn/verification/target_frame_probe.py:505,635-640`). CONF-09 is a
  re-pointing of an existing output, not a new transform.
- `_matched_plummer_hamiltonian` already computes `kinetic` and `potential` as
  separate locals at the correct softening. D-11 extracts them.
- The adapter's `raw_ic13_population` → `compute_normalization_stats` two-pass
  (`adapter.py:801`, `:914`, `:920`) is the established precedent for a
  dataset-wide statistic: collect per-record in pass 1, reduce once in pass 2.
  `S_H` follows its shape, with one difference that matters — normalization
  stats reduce over **all admitted** records, while `S_H` reduces over the
  **train split only**, which the adapter has no knowledge of.
- `StageIndex.from_split(adapter, manifest, "train")` supplies that split, and
  `run_dir/splits.json` (`SplitManifest`) makes it reproducible.
- Phase 46's `validate_sidecar_payload` is the model for D-18's
  re-validate-on-load discipline.

### Established Patterns

- Residency is **fp32**; the preprocessing pipeline is **float64**. Any
  dataset-wide statistic required in float64 must be captured on the float64
  side of that boundary (D-12).
- `StageIndex` exposes per-record values through `_source_value(accessor, key)`
  delegation, so new per-record data is surfaced by adding an accessor rather
  than by reaching into the adapter.
- Fail-closed is the house style: refuse rather than substitute, and re-derive
  rather than trust a persisted number.
- Tests use stdlib `unittest` with synthetic duck-typed `StageIndex`-like
  sources and dataset-free fixtures; extend existing fixtures rather than
  standing up a competing oracle.

### Integration Points

- **Admission → statistic:** per-trajectory `(K0, Uabs0)` captured in
  `adapter.py`'s candidate construction, surfaced via a `StageIndex` accessor.
- **Split → reduction:** the median taken once at run setup, where the split
  manifest is already resolved.
- **Metadata → loss:** the validated `S_H`/`ε_H` reaching
  `controllers.py:482` as a run-level constant, then flowing unchanged into
  `loss_catalog.py:284`'s denominator.
- **Residency → gate:** the same swap changes what `validation_gate.py` observes,
  which is why the frame constant moves in the same change (D-05) and why D-08's
  before/after comparison is the natural regression check.

</code_context>

<specifics>
## Specific Ideas

- The frame swap is a **three-line change with milestone-wide consequences**.
  The plan should treat the surrounding assertions — not the swap itself — as the
  real work: `IC₁₃` invariance (D-04), gate-metric near-invariance (D-08), and
  the velocity identity `dr'/du = v_gauge` (D-02) are each independently
  checkable and together they prove the swap was a pure frame completion.
- Record an explicit coordinate tuple for every new calculation, as Phase 46
  did: `{position: r_prime, time: u, velocity: dr_prime_du, masses: ordered_raw}`.
  A numerically plausible result assembled from incoherent units is the exact
  failure this milestone exists to remove.
- `S_H` should be reported in the plan and run record with its inputs visible —
  `N_train`, the population median, and the resulting `ε_H` — so a later reader
  can tell a correct value from a plausible one without re-running admission.
- Keep the two softenings visually distinct wherever both appear. They differ by
  five orders of magnitude, both are named `eps`-something, and the spec devotes
  a dedicated note (VAL-03) to the fact that people conflate them.

</specifics>

<deferred>
## Deferred Ideas

- `R̄` correction, the causal-exponent clip, `λ_E^max`, and the `L_data`
  reduction (CONF-04..07) — Phase 48. CONF-05's bound must be chosen after both
  CONF-04 and CONF-09.
- Removing the now-unused `r_com_ordered` / `v_com_ordered` fields — a cleanup
  for whichever later phase already touches `PreprocessedTrajectory` (D-03).
- The §3.4:542 duplicate-`10^-5` author comment, and any other spec prose
  amendment — VER-20 routing list, never a v2.2 edit (D-24).
- Conformance-enforcement regime, placeholder census, known-divergence register,
  runtime invariants — Phase 49 / the concurrent verification charter.
- Stage-0 training, three-seed rerun, the single held-out evaluation —
  Phases 50-51.
- Recipe tuning and trainex-r2 remedy adjudication — v2.3 (SCOPE-29/31).

### Reviewed Todos (not folded)

Auto-mode would fold both matched todos on relevance score alone. Both are held
out instead, because `.planning/REQUIREMENTS.md` leaves the carried-forward todos
unlinked to v2.2 and folding them would widen owner-ratified scope — the same
call Phase 46 made on the same todo.

- **`d-06-static-epsilon-sensitivity-check`** (score 0.60) — thematically close
  to §3.4's dual-epsilon note, which makes it tempting. Not folded: a
  sensitivity check on `ε` is precisely the tuning-shaped work SCOPE-29 forbids
  in this milestone, and CONF-02/03 need the spec's value used as written, not
  characterized.
- **`trainex-r1-research-handoff`** (score 0.40) — research hand-off
  administration, unrelated to the frame or the statistic.

</deferred>

---

*Phase: 47-frame-completion-s-h-pipeline*
*Context gathered: 2026-07-29*
