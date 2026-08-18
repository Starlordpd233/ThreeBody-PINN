# Phase 47: Frame Completion & S_H Pipeline - Research

**Researched:** 2026-07-29
**Domain:** Internal conformance repair — training-data residency frame + a dataset-wide loss-scale statistic (CTL-PINN training pipeline, `pinn/`)
**Confidence:** HIGH — every claim below was checked directly against the current file:line in this worktree (`milestone/v2.2`, `.worktrees/trainex`) during this research session, not recalled from training data or the audit report alone.

<user_constraints>
## User Constraints (from CONTEXT.md)

`47-CONTEXT.md` is the authoritative decision source for this phase (owner session, non-interactive, "discuss and surface all sections and areas; then, automatically choose the best option following your own best judgement"). Every decision below carries a provenance tag: **[GROUNDED]** — fixed by a source, may not be varied by the planner; **[JUDGEMENT]** — chosen by the agent under owner delegation, revisable by the owner without disturbing any [GROUNDED] decision. This research does not re-open, re-litigate, or propose alternatives to any [GROUNDED] decision below.

### Locked Decisions (verbatim from CONTEXT.md `<decisions>`)

**CONF-09 — residency completion**
- **D-01 [GROUNDED — `.planning/REQUIREMENTS.md` CONF-09]** The resident series move from `pre.r_com_ordered` / `pre.v_com_ordered` to `pre.r_gauge` / `pre.v_gauge` at `pinn/data/adapter.py:865-866`. The two snapshot-count references at `:871` and `:875` re-point to `pre.r_gauge.shape[0]` in the same change — identical value, but the residency source must be named once.
- **D-02 [GROUNDED — ROADMAP Phase 47 SC-1]** Time handling does **not** move. Residents keep native `parsed_brutus.times`; the `u = t/T` normalization stays at the sampling boundary in `pinn/data/batches.py`. CONF-09 is what makes the existing arrangement coherent rather than something to work around: with scaled positions, `dr'/du = (T/D)·v_rot = v_gauge` holds exactly, so the velocity target is `pre.v_gauge` precisely because the AD derivative is taken with respect to `u`. A plan that also rewrites time normalization has misread the defect.
- **D-03 [JUDGEMENT]** `r_com_ordered` / `v_com_ordered` remain on `PreprocessedTrajectory` after the swap. They stop being the residency source but are still the intermediate the CONF-08 evidence and its tests are written against. Deleting them is a separate cleanup that would widen this diff into files CONF-09 has no reason to touch. Note them as no-longer-resident in the plan summary instead.
- **D-04 [GROUNDED — verified against source]** `IC₁₃` and `E` are **unchanged** by CONF-09 and the phase must assert that rather than adjust them. `pinn/data/adapter.py:847-849` already builds both from `pre.r0_gauge` / `pre.v0_gauge`, and `pinn/data/preprocessing.py:217-219` sets `r0_gauge = r_scaled[0]` with `r_gauge = r_scaled` — so `pre.r_gauge[0]` **is** `pre.r0_gauge`, elementwise. The input side has always been canonical; CONF-09 closes the gap between a canonical input and a raw-frame target. Any plan that edits `IC₁₃` construction is outside the contract.

**CONF-09 — frame re-ratification and test correction**
- **D-05 [GROUNDED — REQUIREMENTS CONF-09; ROADMAP SC-2]** `RATIFIED_VALIDATION_FRAME` is re-ratified to `(POSITION_FRAME_SCALED, TIME_COORD_NORMALIZED, MASS_CONVENTION_ORDERED_RAW)` in the **same change** as the residency swap, per `pinn/training/validation_gate.py:526-528` (CONTEXT.md's citation — this research verified the current, drifted location is `:74-86`/`:788-796`; see Common Pitfalls). Not a follow-up commit: a tree in which residency has moved and the frame constant has not is a tree whose `COHERENT_FRAME_PAIRS` check is lying.
- **D-06 [JUDGEMENT]** `tests/phase46/test_pairing_repair.py` — the only file in the tree encoding the current resident pairing — is **corrected in place**, not superseded by a new Phase 47 file. A parallel test asserting the opposite frame would leave two competing oracles for the same property, which is the exact "competing metric oracle" failure `46-CONTEXT.md` warns against. Its CONF-08 assertions that remain true (permutation applied, `plus_permutation = 0.0`, membership and accounting unchanged) stay as-is; only the assertions encoding *"deliberately without rotation gauge or D/V scaling"* move to the completed contract. New invariants get new Phase 47 tests.
- **D-07 [JUDGEMENT]** Re-ratification is recorded as a Phase 47 artifact stating what superseded what and on whose authority (the GAP-46-07 owner ruling of 2026-07-28, option A), under the same D-12 discipline GAP-46-06 used. This is bookkeeping on an existing ruling, **not** a new gap and not a new decision to surface — GAP-46-06's own constant declared this staleness condition in advance.
- **D-08 [GROUNDED on the claim, JUDGEMENT on the check]** The ROADMAP states gate metrics are unchanged in value because `ε_H` is a relative drift, invariant under uniform `H → D·H`. Record a measured before/after comparison as regression evidence — but assert **approximate** invariance with a stated tolerance, not exact equality. The softening is not uniformly scaled: `EPS_SOFT = 1e-5` is a scaled-frame softening currently applied to raw positions, so the `r_safe = √(‖Δr‖² + ε²)` floor contributes differently in the two frames. Expect agreement to well within tolerance for ordinary separations and a visible difference only where the softening floor binds. A strict equality assertion here would fail for a correct implementation.

**CONF-02 — computing S_H**

The governing text is `pinn_architecture.md` §3.4, lines 539-542, verbatim: *"$S_H$ is computed once in float64 after final COM/zero-momentum/gauge/scaling preprocessing over the training split using the matched-Plummer Hamiltonian components with $\epsilon_{train} = 10^{-5}$."*

- **D-09 [GROUNDED — `pinn_architecture.md:539-542`, reinforced at `:544`]** `S_H` uses the **matched-Plummer Hamiltonian components** at `ε_train = EPS_SOFT = 1e-5`. It does **not** use `EPS_INV = 1e-10`. `pinn/data/preprocessing.py::compute_invariants` is therefore **not** the source for these terms despite computing structurally identical ones — it softens at `EPS_INV = 1e-10` and returns only the signed sum `E`. §3.4's dual-epsilon note (VAL-03, line 544) makes conflating the two softenings an explicit conformance error, and `pinn/verification/gate_metrics.py:145` carries the matching "NEVER" warning on the other side.
- **D-10 [GROUNDED — `pinn_architecture.md:533`]** `K0 + Uabs0` is evaluated at the **initial snapshot** in the completed frame: `K0` is the dimensionless kinetic term `½ Σᵢ mᵢ‖v'ᵢ‖²`, and `Uabs0` is the **absolute value** of the softened potential. Since `V_ε < 0`, `Uabs0 = −potential`. Note `K0 + Uabs0 ≠ H_0` — `H_0 = K0 + V_ε` is the signed sum and is a different quantity that appears separately in the same denominator. Conflating them is a live risk because both are computed by the same helper.
- **D-11 [JUDGEMENT]** Expose the two components through a component-returning seam in `pinn/loss_catalog.py` that the existing `_matched_plummer_hamiltonian` delegates to, preserving its current signature and return value exactly. Its body already computes `kinetic` and `potential` as separate locals before summing them, so this is an extraction, not new physics. Rationale: one home for the softened-potential loop. A second implementation of that pairwise sum is how the two softenings drift apart.
- **D-12 [GROUNDED on float64, JUDGEMENT on placement]** Per-trajectory `(K0, Uabs0)` are computed in **float64 at admission**, from `pre.r_gauge[0]` / `pre.v_gauge[0]` where the float64 preprocessing output is in hand, carried on the candidate record, and exposed through a `StageIndex` accessor following the established `_source_value` pattern (`pinn/data/splits.py:209`). Rationale: `StageIndex.snapshot_positions` returns the **fp32** resident tensors, so reducing the median from residents would violate §3.4's float64 requirement while looking perfectly reasonable. Computing at admission also satisfies "after final … preprocessing" literally — these are that stage's outputs.
- **D-13 [GROUNDED — `pinn_architecture.md:539-540`, `:548`]** The median reduces over the **train split only**, once, at run setup before step 1, via `StageIndex.from_split(adapter, manifest, "train")` (`pinn/data/splits.py:170`) intersected with the Stage-0 admitted set. Never per-minibatch, never per-stage, never recomputed mid-run — §3.4:548 names "computes `S_H` per minibatch" and "from a different split or preprocessing stage" as divergences the FUT-01 handoff must flag.
- **D-14 [JUDGEMENT]** Median convention: `numpy.median` in float64 over the train-split component sums, which averages the two central values on an even population. Persist `N_train` beside `S_H` so the value is re-derivable from the split manifest without re-running admission.

**CONF-02 — persistence and fail-closed validation**
- **D-15 [GROUNDED — `pinn_architecture.md:542`]** **Both** `S_H` **and** `ε_H` persist in training metadata. Not `S_H` alone — §3.4:547 flags metadata that "omits `S_H` or `ε_H`" as divergent.
- **D-16 [JUDGEMENT]** Persist to a dedicated `run_dir/training_metadata.json`, written once at setup before step 1, carrying `S_H`, `ε_H`, `N_train`, `eps_train`, the `energy_floor_factor` used, and the ratified frame tuple. Rationale: `config.yaml` is the frozen *config* and `S_H` is derived data, not configuration; `status.json` is run status; `splits.json` is the split manifest. A dedicated artifact gives the §3.4:546-550 divergence check exactly one path to look at. The planner may instead extend an existing run-metadata artifact if one already fills this role — provided both values are present, float64-exact, and fail-closed.
- **D-17 [GROUNDED on the predicate, JUDGEMENT on timing]** Non-finite or `≤ 0` `S_H` is a preprocessing/metadata validation failure. No fallback floor, no `max()`, no clamp — §3.4:542 says *"Do not apply a fallback numeric floor"* and `:549` names a "max/fallback floor" as divergent. Failure happens at **setup, before step 1**, not lazily at first use: a run that cannot produce a valid `ε_H` must never emit a single step, because a partially-completed run leaves artifacts that read like real evidence.
- **D-18 [JUDGEMENT]** The reader re-validates on load under the same predicate, so a truncated or hand-edited metadata file cannot silently re-enter the loss. This mirrors the semantic-recomputation discipline Phase 46 established in `validate_sidecar_payload` — a persisted number is trusted only after it has been re-checked, never because it is present.

**CONF-03 — ε_H wiring and floor removal**
- **D-19 [GROUNDED — REQUIREMENTS CONF-03; `pinn_architecture.md:531`]** `pinn/training/controllers.py:482` becomes `ε_H = 1e-4 · S_H` sourced from the validated metadata, and the `+ 1e-12` term is deleted outright rather than made configurable or conditional. `stage.energy_floor_factor` (`pinn/training/config.py:161`, value `1e-4`) remains the named home of the `1e-4` factor. The comment at `:480-481` calling the floor "a numeric-safety zero-denominator guard" is the exact rationalization §3.4 prohibits, and goes with the line.
- **D-20 [GROUNDED — `pinn_architecture.md:542`]** *"Use `ε_H` only in `|H_0| + ε_H`."* The per-anchor `abs(h0)` **stays** in the denominator at `pinn/loss_catalog.py:284`; what changes is only where the `ε` scale comes from — per-anchor `abs(h0) · 1e-4` becomes dataset-wide `1e-4 · S_H`. The present code is not wrong because it uses `h0` in the denominator; it is wrong because it uses `h0` as the *scale*, which makes every anchor its own yardstick.
- **D-21 [JUDGEMENT]** `_AnchorContext` keeps an `eps_h` field, injected with the run-level constant, rather than reading a module global. Identical value across anchors, but the existing per-test override seam that controller tests depend on survives.

**Regression evidence**
- **D-22 [GROUNDED on permission, JUDGEMENT on spending it]** Run the permitted CONF-01 re-probe **once**, recorded explicitly as a regression check that residency equals the canonical preprocessing output. Per the ROADMAP's Phase 47 boundaries, `identity_scaled` becomes true by construction and it is no longer a frame test — so it must not be presented as a new CONF-01 verdict, and its numbers may not steer implementation (SCOPE-29). Worth spending because it is the cheapest end-to-end confirmation that the swap reached the surface the probe reads.
- **D-23 [JUDGEMENT]** Record the D-08 before/after gate-metric comparison alongside it. Together the two answer "did residency change?" and "did anything observable change that shouldn't have?"

**Governance and scope locks**
- **D-24 [GROUNDED — SCOPE-27..32]** No training run, no held-out evaluation, no framework-spec edit. Noted for routing, not for action: §3.4:542 contains an author comment — *"I am not sure why there is a duplicate 10^-5 here"* — which is a **VER-20 spec-amendment routing candidate**, not a Phase 47 edit. The `ε_train = 1e-5` value itself is unambiguous and is used as written.
- **D-25 [GROUNDED — Phase 46 D-26 precedent]** The conformance audit's verified-clean component section stays closed. This phase moves a frame and builds a statistic; it does not re-litigate force, Hamiltonian, projection, AD, or gate-formula math.
- **D-26 [GROUNDED — SCOPE-29]** Conformance-only. Loss magnitudes will move substantially, and that is the frame becoming the locked one — not a hyperparameter fitted to an observed result. No sensitivity sweep, no comparison shopping between softenings, no tuning of `1e-4`.
- **D-27 [GROUNDED — GAP-46-06/07]** CONF-01's Complete status and its mandatory EVAL-01 precondition-(ii) qualification are unchanged by this phase. CONF-09 applies CONF-01's answer; it does not re-decide it.

### Claude's Discretion (verbatim from CONTEXT.md)

The owner delegated all gray-area selection for this session. The **[JUDGEMENT]** decisions are D-03, D-06, D-07, D-08 (check design), D-11, D-12 (placement), D-14, D-16, D-17 (timing), D-18, D-21, D-22 (spending), and D-23. Each is revisable on owner instruction without disturbing any **[GROUNDED]** decision.

Beyond those, the planner may choose module and helper names, the metadata field layout inside the artifact chosen in D-16, test file organization, and fixture construction — provided every decision above is preserved, no dependency is added, and no new cadence, threshold, tuning signal, or evaluator path is created.

### Deferred Ideas (OUT OF SCOPE, verbatim from CONTEXT.md)

- `R̄` correction, the causal-exponent clip, `λ_E^max`, and the `L_data` reduction (CONF-04..07) — Phase 48. CONF-05's bound must be chosen after both CONF-04 and CONF-09.
- Removing the now-unused `r_com_ordered` / `v_com_ordered` fields — a cleanup for whichever later phase already touches `PreprocessedTrajectory` (D-03).
- The §3.4:542 duplicate-`10^-5` author comment, and any other spec prose amendment — VER-20 routing list, never a v2.2 edit (D-24).
- Conformance-enforcement regime, placeholder census, known-divergence register, runtime invariants — Phase 49 / the concurrent verification charter.
- Stage-0 training, three-seed rerun, the single held-out evaluation — Phases 50-51.
- Recipe tuning and trainex-r2 remedy adjudication — v2.3 (SCOPE-29/31).
- `d-06-static-epsilon-sensitivity-check` and `trainex-r1-research-handoff` — explicitly held out of auto-mode folding; not v2.2 items.

**Explicitly excluded source:** `pinn_instruction/markdown_conversion/framework-specs/trainex-r2/` is **not** a grounding source (SCOPE-31) and was not consulted in this research.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| CONF-09 | Complete the residency transform to the locked canonical contract (`pre.r_gauge`/`v_gauge`), re-ratify `RATIFIED_VALIDATION_FRAME` in the same change, correct the one test encoding the superseded pairing. | Architecture Patterns (system diagram, Pattern 1), Code Examples (all three snippets), Common Pitfalls 1 and 4, Validation Architecture rows CONF-09 |
| CONF-02 | Build the `S_H = median_train(K0 + Uabs0)` pipeline: computed in float64 in the completed frame, over the train split only, persisted with fail-closed validation. | Architecture Patterns (Patterns 1-3), Don't Hand-Roll, Common Pitfalls 2-3, Code Examples (component extraction), Validation Architecture rows CONF-02 |
| CONF-03 | Wire `ε_H = 1e-4 · S_H` into the loss assembly at `controllers.py:482`; delete the `+1e-12` floor. | Architecture Patterns (system diagram bottom half), Common Pitfalls 5, Code Examples ("exact CONF-03 defect"), Validation Architecture rows CONF-03 |
</phase_requirements>

## Summary

Phase 47 is not a library-integration phase; it is a source-grounded conformance repair inside an already-built, already-tested internal codebase (`pinn/`). There is no new framework, no new package, and no external API to research — the entire "domain" is this repository's own data pipeline, loss catalog, and training controller, plus one governing paragraph of `pinn_architecture.md` §3.4. Research therefore consisted of verifying every code seam `47-CONTEXT.md` names against the live file (grep + Read), confirming line-number accuracy (one citation drifted — see Common Pitfalls), and tracing the exact wiring gap CONF-03 must close (there is currently NO channel for a run-computed statistic to reach `RunController`).

Three findings materially matter for planning. First, `RATIFIED_VALIDATION_FRAME` and its `COHERENT_FRAME_PAIRS` machinery live at `pinn/training/validation_gate.py:74-86` (constants) and `:788-796` (the ratified constant) — **not** `:526-528` as `47-CONTEXT.md` D-05 cites; the audit report's own line numbers have drifted since 2026-07-28 as later Phase 46 plans landed. Second, the exact test assertions D-06 must flip live in one method — `AdapterPairingRepairTests.test_resident_trajectory_is_not_rotation_gauged_or_globally_scaled` (`tests/phase46/test_pairing_repair.py:272-301`) — while a sibling method in the same class (`test_resident_positions_velocities_and_masses_share_one_body_order`, `:198-221`) also embeds a COM-only (non-rotated, non-scaled) oracle that will fail post-swap and needs its own fixture extended to rotation+scale, even though D-06's text names only the "deliberately without rotation gauge or D/V scaling" assertions. Third, `RunController` (`pinn/training/controllers.py:295-313`) has no constructor parameter for a run-computed scalar today — `_build_anchor_context` reads `self._config.stage.energy_floor_factor` (a static config default) directly at line 482; CONF-03 requires a genuinely new value (validated `S_H`/`ε_H`) to flow from wherever it is computed and validated (near `pinn/train.py:801`, right after `train_source` becomes available) into the `RunController(...)` call site (`pinn/train.py:964`) — this parameter does not exist yet and its absence is not a bug, just unbuilt plumbing.

**Primary recommendation:** Do the residency swap and frame re-ratification as the single, surgical three-line change D-01/D-05 describe, prove it with the three train-free assertions named in `47-CONTEXT.md` (IC₁₃ invariance, the `dr'/du = v_gauge` identity, approximate gate-metric invariance), then build `S_H` as a second admission-time pass (mirroring the existing `raw_ic13_population` → `compute_normalization_stats` two-pass shape at `pinn/data/adapter.py:801-922`, but reduced over the **train split only**, at run setup, not inside the adapter), persist it fail-closed to a dedicated `run_dir/training_metadata.json`, and thread the validated `ε_H` into `RunController` as a new explicit constructor argument rather than smuggling it into the frozen `config.stage.energy_floor_factor` (which is itself already correctly named and correctly valued — no config.py edit is needed for CONF-03).

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Residency array selection (which preprocessed fields become the training-visible position/velocity series) | Data / Admission (`pinn/data/adapter.py`) | Preprocessing (`pinn/data/preprocessing.py`, already computes both candidates) | The adapter is the sole place that decides what `StageIndex.snapshot_positions/velocities` return; `preprocess_trajectory` already computes the target output, it is not re-derived here |
| Frame contract / coherence enforcement | Training / Validation gate (`pinn/training/validation_gate.py`) | — | `RATIFIED_VALIDATION_FRAME` + `COHERENT_FRAME_PAIRS` is the single declared source of truth for which (position, time) pairing is legal; it must track residency, not the other way around |
| Dataset-wide statistic computation (`S_H`) | Data / Admission (per-record `K0`,`Uabs0`) + Training setup (median reduction) | — | Per-record values are a float64 preprocessing output (own the admission pass, mirroring `E`/`Q`/`l_ratio`/`min_separation`); the median is a **split**-scoped reduction and the adapter has no split knowledge, so it cannot live in the adapter alone (`StageIndex.from_split` is a `pinn/data/splits.py` concern) |
| Metadata persistence + fail-closed validation | Training / Run setup (`pinn/train.py`, new artifact) | — | Must happen once, before step 1, at the same point `splits.json`/`config.yaml` are frozen — a run that cannot validate `S_H` must never emit a step |
| Loss-term consumption of `ε_H` | Loss (`pinn/loss_catalog.py::soft_energy_loss`) | Controller (`pinn/training/controllers.py::_build_anchor_context`) | The controller supplies the scalar `eps_h`; the loss function only ever multiplies/divides — no physics or scale logic belongs in the loss catalog beyond what's already there |
| The two softening constants (`EPS_SOFT`, `EPS_INV`) | Constants (`pinn/constants.py`, `pinn/verification/gate_metrics.py`) | — | Both are already correctly defined and separated; the risk is a **consumer** picking the wrong one, not a definition-site defect |

## Standard Stack

Not applicable in the conventional sense — this phase adds **zero new external dependencies**. All work uses libraries already vendored in this worktree's `.venv` (`<home>/Desktop/3_body_problem/.venv`):

| Library | Verified version (`.venv`) | Purpose here |
|---------|------|--------------|
| numpy | 2.2.0 `[VERIFIED: .venv/bin/python -c "import numpy"]` | float64 admission-time computation of `K0`/`Uabs0`, `numpy.median` reduction for `S_H` |
| torch | 2.12.0 `[VERIFIED: .venv/bin/python -c "import torch"]` | resident fp32 tensors, `_matched_plummer_hamiltonian` (loss-side) |
| pytest | 9.1.1 `[VERIFIED: .venv/bin/python -m pytest --version]` | test runner (project convention: `pytest tests/phaseNN/ -q -rs`, confirmed at `.planning/phases/46-.../46-10-SUMMARY.md:103-108`) |

**Installation:** none required.

### Alternatives Considered

Not applicable — no library selection decision exists in this phase; every choice is either `[GROUNDED]` in `47-CONTEXT.md`/the spec, or a `[JUDGEMENT]` naming/placement call already made by the context-gathering session.

## Package Legitimacy Audit

**Not applicable.** This phase introduces no new external packages, so the Package Legitimacy Gate protocol has nothing to check. All code touches `numpy`/`torch`, both already present in the project's `.venv` and used pervasively elsewhere in `pinn/`.

## Architecture Patterns

### System Architecture Diagram

```
                    ┌─────────────────────────────────────────────┐
                    │  pinn/data/preprocessing.py                  │
                    │  preprocess_trajectory(times, pos, vel, m)   │
                    │  → PreprocessedTrajectory:                   │
                    │      r_com_ordered / v_com_ordered  (raw)    │
                    │      r_gauge      / v_gauge  (rot+D/V scaled)│  ALREADY COMPUTES BOTH
                    │      r0_gauge = r_gauge[0]  (identity, D-04) │
                    └───────────────────┬───────────────────────────┘
                                        │ pre.* (float64)
                    ┌───────────────────▼───────────────────────────┐
                    │ pinn/data/adapter.py :: _scan_and_admit()      │  PASS 1 (per record, float64)
                    │  candidates.append(positions=pre.r_gauge, ◄────┼─ CONF-09: swap from r_com_ordered
                    │                    velocities=pre.v_gauge,     │
                    │                    masses_ordered=..., raw_ic13)│
                    │  + NEW: (K0, Uabs0) via matched-Plummer        │  CONF-02: new per-record capture
                    │         components at r_gauge[0]/v_gauge[0]    │
                    │  raw_ic13_population.append(raw_ic13)          │  existing 2-pass precedent
                    └───────────────────┬───────────────────────────┘
                                        │ candidates (all admitted)
                    ┌───────────────────▼───────────────────────────┐
                    │ pinn/data/adapter.py :: _materialize()         │  PASS 2 (fp32 residency)
                    │  compute_normalization_stats(raw_ic13_pop, E)  │
                    │  torch.tensor(pos_t, dtype=float32) ◄──────────┼─ fp32 boundary — K0/Uabs0 must NOT
                    │  AdmittedRecord(ic13, masses, E, Q, ..., ◄─────┼─  be captured on this side (D-12)
                    │                 k0=, uabs0=)  NEW fields       │
                    └───────────────────┬───────────────────────────┘
                                        │ AdmittedSetAdapter (fp32 resident)
                    ┌───────────────────▼───────────────────────────┐
                    │ pinn/train.py :: _build_admitted_sources()     │
                    │  StageIndex.from_split(adapter, manifest,      │
                    │                        "train")  ◄─────────────┼─ split boundary; S_H reduces HERE
                    │  → train_source, validation_source             │  (D-13), never inside adapter.py
                    └───────────────────┬───────────────────────────┘
                                        │ train_source (StageIndex)
                    ┌───────────────────▼───────────────────────────┐
                    │ pinn/train.py :: run(), after line ~801        │  NEW: run-setup S_H pipeline
                    │  S_H = median(train_source K0+Uabs0 over       │
                    │               admitted-train ∩ Stage-0)        │
                    │  fail-closed: non-finite or ≤0 → refuse before │  D-17: before step 1, not lazy
                    │  any step is emitted                           │
                    │  atomic_write_text(run_dir/training_metadata   │  D-16/D-18: dedicated artifact,
                    │                    .json, {S_H, eps_H, ...})   │  re-validated on load
                    └───────────────────┬───────────────────────────┘
                                        │ validated S_H / eps_H (float)
                    ┌───────────────────▼───────────────────────────┐
                    │ pinn/train.py :: RunController(...) at :964    │  NEW constructor arg needed
                    │  ──► pinn/training/controllers.py               │  (does not exist today — D-19/D-21)
                    │      _build_anchor_context():482                │
                    │      eps_h = 1e-4 * S_H  (was: |h0|*factor+1e-12)│
                    └───────────────────┬───────────────────────────┘
                                        │ eps_h (run-level constant)
                    ┌───────────────────▼───────────────────────────┐
                    │ pinn/loss_catalog.py :: soft_energy_loss()     │
                    │  denom = h0.abs() + eps_h_t   (:284, D-20)     │  unchanged call site;
                    │  _matched_plummer_hamiltonian(..., EPS_SOFT)   │  only the SCALE of eps_h changed
                    └─────────────────────────────────────────────────┘

  Parallel track (same change, D-05):
  pinn/training/validation_gate.py :788-796  RATIFIED_VALIDATION_FRAME
     position_frame: POSITION_FRAME_RAW → POSITION_FRAME_SCALED
     time_coord:     TIME_COORD_RAW     → TIME_COORD_NORMALIZED
  Consumed by pinn/train.py:147 (validation_gate.RATIFIED_VALIDATION_FRAME)
  and pinn/training/validation_gate.py:199-292 (compute_validation_gate)
```

### Recommended Project Structure

No new directories. Files touched (all pre-existing):

```
pinn/data/adapter.py            # CONF-09 (residency swap, :864-866,871,875) + CONF-02 pass-1 capture
pinn/data/types.py               # CONF-02: AdmittedRecord gains k0/uabs0 float64 fields (after :230-231)
pinn/data/preprocessing.py       # comment-only: r_com_ordered docstring's "CONF-08 resident surface" note goes stale (:69)
pinn/loss_catalog.py             # CONF-02 D-11: extract kinetic/potential component seam (:140-157)
pinn/training/validation_gate.py # CONF-09 D-05: re-ratify RATIFIED_VALIDATION_FRAME (:788-796) + new evidence ref
pinn/training/controllers.py     # CONF-03 D-19/D-20/D-21: eps_h source + _AnchorContext field (:478-500)
pinn/training/config.py          # verify only — NO edit needed; energy_floor_factor already correct (:161,409)
pinn/train.py                    # CONF-02/03: new S_H pipeline call + training_metadata.json write + RunController wiring (near :801, :964)
tests/phase46/test_pairing_repair.py   # D-06: correct AdapterPairingRepairTests (see Common Pitfalls for exact methods)
tests/phase47/                   # NEW directory: CONF-09/02/03 assembly-boundary + regression tests
```

### Pattern 1: Two-Pass Admission Statistic (existing precedent — reuse, don't reinvent)

**What:** `AdmittedSetAdapter` already computes one dataset-wide statistic this way: collect a per-record float64 value during `_scan_and_admit` (pass 1), reduce once over the full population in `_materialize` (pass 2).

**When to use:** `K0`/`Uabs0` capture follows this shape exactly for the per-record half. The reduction half does **not** reuse `_materialize`, because `S_H` reduces over the **train split only**, and the adapter has no split knowledge (splits are computed downstream in `pinn/data/splits.py` via `StageIndex.from_split`). The precedent is the *shape*, not a literal call site.

**Example (existing precedent, verified):**
```python
# Source: pinn/data/adapter.py:801,873-875 (pass 1) and :919-922 (pass 2)
raw_ic13_population = []              # :801, per-record append at :873
...
raw_ic13_population.append(raw_ic13)  # :873
trajectory_energies.append(inv.E)     # :874
...
self._raw_ic13_population = raw_ic13_population   # :914
self._trajectory_energies = trajectory_energies   # :915
...
def _materialize(self, candidates):
    stats = compute_normalization_stats(                 # :919-922
        np.asarray(self._raw_ic13_population, dtype=np.float64),
        np.asarray(self._trajectory_energies, dtype=np.float64))
```
`K0`/`Uabs0` should be captured alongside `inv.E`/`inv.Q`/`inv.s_min` at the same point in `_scan_and_admit` (right after `pre = preprocess_trajectory(...)` succeeds, `pinn/data/adapter.py:844-849`), stored as new `AdmittedRecord` fields (`pinn/data/types.py:230-231` region, alongside `E`/`l_ratio`/`Q`/`min_separation`), and **not** reduced inside the adapter — the median reduction is a `StageIndex`/run-setup concern (see Pattern 2).

### Pattern 2: Split-Scoped Statistic Reduction

**What:** `StageIndex.from_split(adapter, manifest, "train")` (`pinn/data/splits.py:169-186`) is the existing mechanism that resolves the train-only record population from an admitted adapter and a `SplitManifest`. It is already called in `pinn/train.py::_build_admitted_sources` at `:414` (train) and `:415` (validation), which itself is called at `pinn/train.py:801` (`train_source, validation_source = _build_sources(config, run_dir)`).

**When to use:** the `S_H` median must be computed **after** this call returns `train_source`, using `train_source`'s exposed record keys intersected with the Stage-0 admitted set (`train_source.records_at_or_below(0)` per `pinn/data/splits.py:254-261`, or `records_at(0)` per `:251-252` — confirm against D-13's "Stage-0 admitted set" wording before choosing `at` vs `at_or_below`), and **before** `RunController` is constructed at `pinn/train.py:964`.

**Example (accessor pattern to extend, verified):**
```python
# Source: pinn/data/splits.py:209-224 (_source_value delegation, existing pattern)
def _source_value(self, accessor: str, key: RecordKey):
    if key not in self._records:
        raise KeyError(key)
    if self._source is None:
        record = self._records[key]
        if hasattr(record, accessor):
            value = getattr(record, accessor)
            return value() if callable(value) else value
        raise TypeError(...)
    value = getattr(self._source, accessor, None)
    if not callable(value):
        raise TypeError(f"admitted source does not expose {accessor}(key)")
    return value(key)
```
A new `StageIndex.k0(key)` / `.uabs0(key)` accessor pair (mirroring `snapshot_positions`/`snapshot_velocities` at `:229-233`) is the D-12-mandated surface: "exposed through a `StageIndex` accessor following the established `_source_value` pattern."

### Pattern 3: Component-Returning Extraction (D-11 seam)

**What:** `_matched_plummer_hamiltonian` (`pinn/loss_catalog.py:140-157`) already computes `kinetic` (line 148) and `potential` (accumulated in the loop at 151-156) as separate locals before returning their sum. D-11 requires exposing both without changing this function's signature or return value.

**Example — minimal extraction shape (verified against current source, not yet applied):**
```python
# Source: pinn/loss_catalog.py:140-157 (current, unmodified)
def _matched_plummer_hamiltonian(positions, velocities, masses, *, dtype, device,
                                 eps_soft=EPS_SOFT) -> torch.Tensor:
    """Matched-Plummer H_eps = T' + V_eps per snapshot; returns (N_t,)."""
    p = _as_positions(positions, dtype=dtype, device=device)
    v = _as_positions(velocities, dtype=dtype, device=device)
    m = torch.as_tensor(masses, dtype=dtype, device=device)
    speed_sq = (v * v).sum(dim=-1)
    kinetic = torch.as_tensor(0.5, dtype=dtype, device=device) * (m * speed_sq).sum(dim=-1)
    eps = torch.as_tensor(eps_soft, dtype=dtype, device=device)
    potential = torch.zeros(p.shape[0], dtype=dtype, device=device)
    for i in range(_N_BODIES):
        for j in range(i + 1, _N_BODIES):
            delta = p[:, j] - p[:, i]
            r_safe = torch.sqrt((delta * delta).sum(dim=-1) + eps * eps)
            potential = potential - (m[i] * m[j] / r_safe)
    return kinetic + potential
```
D-11's seam: factor `kinetic`/`potential` computation into a helper (e.g. `_matched_plummer_components(...) -> (kinetic, potential)`) that `_matched_plummer_hamiltonian` calls and sums (`return kinetic + potential` becomes `k, v = _matched_plummer_components(...); return k + v`). **D-10 is the critical semantic point here:** `S_H` uses `K0 + Uabs0` where `Uabs0 = |potential|` (since `potential = V_ε < 0`); `K0 + Uabs0 ≠ H_0 = K0 + potential`. Any reuse of this seam for `S_H` capture must take `abs(potential)`, not `potential`, at the call site — this is the single easiest place to silently swap a signed sum for an absolute one.

### Anti-Patterns to Avoid

- **Computing `S_H` on fp32 residents:** `StageIndex.snapshot_positions`/`snapshot_velocities` return the fp32 resident tensors (`AdmittedRecord` construction at `pinn/data/adapter.py:942-953`, `self._dtype = torch.float32` at `:710`). §3.4 requires `S_H` "computed once in float64". Capture `K0`/`Uabs0` from `pre.r_gauge[0]`/`pre.v_gauge[0]` at admission time (float64, before the fp32 cast at `_materialize`), never by re-reading residents after materialization.
- **Reducing `S_H` inside `_materialize`:** `_materialize` has no split knowledge — it runs once per adapter construction, before any `SplitManifest` exists. Reducing there would compute the median over the *admitted* population, not the *train split*, silently violating D-13.
- **Mutating `config.stage.energy_floor_factor` to carry `S_H`:** the frozen `config.yaml` (`freeze_resolved_config`, `pinn/train.py:746-752`) is written from `config` before/at run start. `S_H` is **derived data**, not configuration (D-16's own rationale) — smuggling it into a config field would either corrupt the frozen-config identity check or require writing `config.yaml` twice with different content, both wrong. Thread `S_H`/`ε_H` as a separate value into whatever constructs `RunController`.
- **Reusing `pinn/data/preprocessing.py::compute_invariants`(`EPS_INV=1e-10`) for `K0`/`Uabs0`:** it is a structurally similar pairwise sum but softened at the WRONG epsilon and returns only the signed sum `E`, not split kinetic/potential. `pinn_architecture.md:539-542` requires `ε_train = EPS_SOFT = 1e-5`. Confirmed structurally distinct at `pinn/data/preprocessing.py:847` call site (`compute_invariants(pre.masses_ordered, pre.r0_gauge, pre.v0_gauge)` feeds `inv.E`, a different quantity than `H_0`/`K0`/`Uabs0`).

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Matched-Plummer kinetic/potential split | A second pairwise-softened-distance loop somewhere in `adapter.py` or `train.py` | The `_matched_plummer_hamiltonian` component seam (D-11), extracted once in `pinn/loss_catalog.py` | A second implementation of the softened pairwise sum is exactly how `EPS_SOFT` and `EPS_INV` (or a third stray epsilon) drift apart — the spec's own VAL-03 note exists because this has already happened conceptually once (validation vs training softening) |
| Train-split population resolution | Re-deriving which records are "train" from `splits.json` by hand in `train.py` | `StageIndex.from_split(adapter, manifest, "train")` (`pinn/data/splits.py:169-186`), already called at `pinn/train.py:414` | This is exactly the mechanism `RUN-03`/evaluation reconstruction also depends on; a parallel derivation risks disagreeing with it silently |
| Atomic metadata write | `open(...).write(...)` or `json.dump` direct to the final path | `pinn.training.atomic_io.atomic_write_text` (`pinn/training/atomic_io.py:41`), the same primitive `validation_gate.py`'s sidecar publisher uses | A partial write on crash mid-run is exactly the "run that emits a partially-completed artifact that reads like real evidence" failure D-17 explicitly names as unacceptable |
| Median convention | A custom sort+midpoint implementation | `numpy.median` (D-14, explicit) | Standard-library behavior (averages the two central values on an even population) is the documented convention; a hand-rolled median risks a silent off-by-one on even populations |

**Key insight:** every "don't hand-roll" item above already has a working, tested analog somewhere in `pinn/` from Phase 39/41/46. The risk in this phase is not missing infrastructure — it's *not noticing* the infrastructure already exists and building a second, subtly different copy next to it.

## Common Pitfalls

### Pitfall 1: Citing a stale line number for `RATIFIED_VALIDATION_FRAME`

**What goes wrong:** `47-CONTEXT.md` D-05 and the audit report both cite `pinn/training/validation_gate.py:526-528` for the re-ratification site.

**Why it happens:** the audit report was written 2026-07-28, before later Phase 46 plans (46-08 through 46-10) landed additional code in `validation_gate.py`, shifting the constant downward.

**How to avoid:** as of this research session (verified via `grep -n "RATIFIED_VALIDATION_FRAME\|COHERENT_FRAME_PAIRS"`), the frame constants (`POSITION_FRAME_SCALED`, `POSITION_FRAME_RAW`, `TIME_COORD_NORMALIZED`, `TIME_COORD_RAW`, `MASS_CONVENTION_ORDERED_RAW`, `COHERENT_FRAME_PAIRS`) are defined at `:74-86`, and the `RATIFIED_VALIDATION_FRAME = FrameConvention(...)` assignment itself is at `:788-796`. **The plan should grep for the symbol name, not trust either line number, since it may drift again before execution.**

**Warning signs:** an edit that touches `_validate_record_key_triple`/`_metrics_equal` (the functions that actually occupy `:482-530`) instead of the frame constant is a sign this citation was followed literally without verification.

### Pitfall 2: Conflating `K0 + Uabs0` with `H_0`

**What goes wrong:** `_matched_plummer_hamiltonian` and any component extraction of it naturally produce the *signed* sum `kinetic + potential = H_0`. `S_H = median_train(K0 + Uabs0)` requires `Uabs0 = |potential|` (D-10), a different, always-larger, always-positive quantity. Both are computed from the same helper, so it is easy to wire the signed sum into `S_H` by mistake and get a value that can be zero or negative (violating D-17's fail-closed predicate) or simply the wrong magnitude.

**Why it happens:** `H_0` (signed) is a real, separately-used quantity — it is exactly what `_build_anchor_context` computes and stores as `anchor_ctx.h0` (`pinn/training/controllers.py:468-473`) for the *per-anchor* denominator numerator (`Δ H_n = (H(u_n) - H_0)/...`). Two structurally similar float scalars, one signed and one built from an absolute value, both derived from the same helper, both flowing toward the same loss term — a natural place for a copy-paste error.

**How to avoid:** at the `K0`/`Uabs0` capture site, explicitly compute `uabs0 = abs(potential_component)`, never reuse a cached `h0`-shaped value. Name the two captured scalars `k0`/`uabs0`, never `h0_train` or similar — the naming itself should make the signed/absolute distinction impossible to lose in a diff.

**Warning signs:** a test asserting `S_H == median(h0_values)` (using the signed per-anchor `h0` machinery already in `controllers.py`) rather than an independently captured `K0+|potential|` — this would silently pass unit tests while implementing the wrong spec quantity, since both are floats of the same rough order of magnitude in the scaled frame.

### Pitfall 3: Conflating `EPS_SOFT` and `EPS_INV`

**What goes wrong:** two constants named similarly (`EPS_SOFT = 1e-5` at `pinn/constants.py:38-39`; `EPS_INV = 1e-10` at `pinn/verification/gate_metrics.py:59`) softening structurally identical `r_safe = √(‖Δr‖²+ε²)` expressions, five orders of magnitude apart. `S_H`/`ε_H`/the training loss term must use `EPS_SOFT`; the validation/admission-gate `eps_H`/SCS metric (ACC-03, a **different `eps_H`** despite the shared glyph — see `ctl_instruction.md:576-580`, "same glyph, different quantity") uses `EPS_INV`.

**Why it happens:** `gate_metrics.py:145` already carries an explicit "NEVER" warning about this exact substitution, meaning it has already been a live risk once in this codebase. `pinn_architecture.md:544` (VAL-03) devotes a dedicated note to it. Two independent authorities flagging the same failure mode is itself evidence it is easy to make.

**How to avoid:** `_matched_plummer_hamiltonian` (loss-catalog, training side) defaults `eps_soft=EPS_SOFT` and must stay that way; `K0`/`Uabs0` capture at admission must explicitly pass `eps_soft=EPS_SOFT` (or reuse the default) and must **never** import from `pinn.verification.gate_metrics`. Grep any new CONF-02 code for `EPS_INV` before considering it done — a hit is a defect.

**Warning signs:** an import of `pinn.verification.gate_metrics` inside `pinn/data/adapter.py` or `pinn/loss_catalog.py` (there is currently no such import — confirmed via `grep -n "gate_metrics" pinn/data/adapter.py pinn/loss_catalog.py` returning nothing).

### Pitfall 4: Under-correcting `tests/phase46/test_pairing_repair.py`

**What goes wrong:** D-06 names "the assertions encoding *deliberately without rotation gauge or D/V scaling*" as the ones that must move. Read literally, this points only at `AdapterPairingRepairTests.test_resident_trajectory_is_not_rotation_gauged_or_globally_scaled` (`:272-301`), which explicitly asserts `assertFalse(np.allclose(resident_positions, preprocessed.r_gauge))` etc. — these assertions become **false** (should become `assertTrue`/`np.testing.assert_array_equal`, since resident IS `r_gauge` post-swap) and must be corrected or the suite fails immediately, which is the intended fail-fast signal.

**Why it happens / the subtlety:** a second method in the same class, `test_resident_positions_velocities_and_masses_share_one_body_order` (`:198-221`), builds its own **independent oracle** via `_resident_fixture()` (`:166-195`), which applies COM-recenter + boost + canonical permutation **only** — no rotation gauge, no `D`/`V` scaling — then compares it byte-for-byte against `adapter.snapshot_positions(key)`/`snapshot_velocities(key)`. Post-swap, the adapter returns `r_gauge`/`v_gauge` (rotated + scaled), so this comparison will **also** fail unless `_resident_fixture()`'s independent derivation is extended to apply the same rotation gauge + D/V scaling `preprocess_trajectory` applies (`pinn/data/preprocessing.py:196-205`). This method is not named in D-06's prose but is affected by construction — it tests the same code path with a narrower (pre-rotation) oracle.

**Why it does NOT need to change:** `test_resident_trajectory_preserves_com_and_zero_momentum_gauge` (`:223-270`) checks the COM/momentum postcondition at `positions[0]`, which `preprocess_trajectory`'s own postcondition assertion already guarantees holds for `r_gauge`/`v_gauge` too (`pinn/data/preprocessing.py:207-213`) — this assertion should continue to pass unmodified, though the numeric round-off bound derivation (`:249-264`) is scale-relative and self-adjusts, so no numeric literal needs updating. `test_admission_keys_snapshot_counts_and_folder_accounting_are_unchanged` (`:303-362`) and every method in `PreprocessingPairingSeamTests` (`:80-152`, which tests `preprocess_trajectory` directly, not the adapter's residency choice) are unaffected by CONF-09 and must stay byte-identical.

**How to avoid:** treat "which test methods must change" as an empirical question to re-verify at implementation time (run the untouched test file against the post-swap adapter and read the failures), not a checklist transcribed from D-06's prose alone — the prose names the *category* of assertion that must move, not an exhaustive list of methods.

### Pitfall 5: No plumbing exists today for a run-computed scalar to reach `RunController`

**What goes wrong:** `_build_anchor_context` (`pinn/training/controllers.py:447-500`) computes `eps_h` at line 482 purely from `self._config.stage.energy_floor_factor` (a static `TrainingConfig` field, `pinn/training/config.py:409`) and a per-anchor `h0`. There is no existing constructor parameter, attribute, or config field anywhere in `RunController.__init__` (`pinn/training/controllers.py:295-313`, thirteen positional + five keyword parameters, none of which is `s_h` or `eps_h`) through which a run-computed `S_H`/`ε_H` value could arrive without either (a) adding a new parameter, or (b) polluting the frozen `TrainingConfig`.

**Why it happens:** this wiring genuinely does not exist yet — CONF-03 is not fixing a bug in existing plumbing, it is building the plumbing for the first time. `stage.energy_floor_factor` was always meant to be *the `1e-4` factor*, not the full `ε_H` value — that part is already correct (D-19 confirms: "`stage.energy_floor_factor` ... remains the named home of the `1e-4` factor").

**How to avoid:** the plan should add an explicit new parameter to `RunController.__init__` (e.g. `s_h: float` or `eps_h: float`, keyword-only, required — no default that could silently mask a missing validated value), threaded from `pinn/train.py` between the point `train_source` becomes available (`:801`) and the `RunController(...)` call (`:964`). `_build_anchor_context` then computes `eps_h = 1e-4 * self._s_h` (or reads a precomputed `self._eps_h` directly) instead of `abs(h0) * energy_floor_factor + 1e-12`. `_AnchorContext.eps_h` (D-21) keeps its field so the existing per-test override seam controller tests depend on survives unchanged.

**Warning signs:** any change that reads `S_H` off `config` (e.g. `config.stage.s_h`) — this reintroduces the config/derived-data conflation Pitfall/Anti-Pattern above warns against, and duplicates `freeze_resolved_config`'s single write with a second, differently-timed one.

## Code Examples

### Current (pre-CONF-09) residency construction — exact source

```python
# Source: pinn/data/adapter.py:861-876 (verified current state)
# CONF-08 repair: resident arrays carry COM/boost + canonical
# body order, deliberately without rotation gauge or D/V scaling.
candidates.append(SimpleNamespace(
    record_key=record_key, variant=variant, fidelity=fidelity,
    times=parsed_brutus.times, positions=pre.r_com_ordered,
    velocities=pre.v_com_ordered,
    masses_ordered=pre.masses_ordered, raw_ic13=raw_ic13,
    inv=inv, measured=measured,
    dt_reference=reference.get("dt_out"),
    dt_provenance=provenance.get("dt_out"),
    n_snapshots=int(pre.r_com_ordered.shape[0]),
    stage_label=label))
raw_ic13_population.append(raw_ic13)
trajectory_energies.append(inv.E)
self._total_admitted_snapshots += int(pre.r_com_ordered.shape[0])
```
The D-01 swap touches exactly `positions=`, `velocities=`, and the two `pre.r_com_ordered.shape[0]` occurrences (lines 871, 875) → `pre.r_gauge.shape[0]` (identical numeric value, per `preprocess_trajectory`'s construction — `r_gauge` and `r_com_ordered` share `Nt` on axis 0). The candidate comment (`# CONF-08 repair: ... deliberately without rotation gauge or D/V scaling`) must be corrected in the same change — it will otherwise misdescribe post-swap behavior.

### Current velocity-target construction (D-02's exact site)

```python
# Source: pinn/training/controllers.py:463-473 (verified current state)
positions_gt = np.asarray(source.snapshot_positions(anchor_key), dtype=np.float64)
velocities_gt = np.asarray(source.snapshot_velocities(anchor_key), dtype=np.float64)
true_r0 = torch.as_tensor(positions_gt[0], dtype=self._dtype, device=self._device)
true_v0 = torch.as_tensor(velocities_gt[0], dtype=self._dtype, device=self._device)

h0 = float(
    loss_catalog._matched_plummer_hamiltonian(
        true_r0.unsqueeze(0), true_v0.unsqueeze(0), masses_t,
        dtype=self._dtype, device=self._device,
    )[0]
)
```
No code change is required here for CONF-09 — `source.snapshot_positions`/`snapshot_velocities` automatically return `r_gauge`/`v_gauge` once the adapter-level swap lands, because this call is a pass-through to whatever the adapter stores. This is the concrete mechanism behind the report's "every derived anchor target self-consistent without a separate conversion table" claim.

### The exact CONF-03 defect and its call site

```python
# Source: pinn/training/controllers.py:478-482 (verified current state — the defect)
# WR-02: eps_h scale is the config-overridable StageConfig.energy_floor_factor
# (CTX-38 provisional default 1e-4 = ctl_instruction.md CURR-03 ε_H=1e-4·S_H).
# The +1e-12 additive floor is a numeric-safety zero-denominator guard, not
# the configurable scale.
eps_h = abs(h0) * float(self._config.stage.energy_floor_factor) + 1e-12
```
```python
# Source: pinn/loss_catalog.py:282-286 (verified current state — the single legal ε_H use site, D-20)
h0_t = torch.as_tensor(h0, dtype=dtype, device=device)
eps_h_t = torch.as_tensor(eps_h, dtype=dtype, device=device)
denom = h0_t.abs() + eps_h_t
delta_h = (h - h0_t) / denom
```
`loss_catalog.py:284`'s `denom = h0_t.abs() + eps_h_t` does **not** change (D-20: `abs(h0)` stays in the denominator). Only line 482 in `controllers.py` changes — `eps_h` becomes `1e-4 * S_H` sourced from validated run metadata, and the `+ 1e-12` term is deleted, not made conditional.

### `RATIFIED_VALIDATION_FRAME` — current value to re-ratify

```python
# Source: pinn/training/validation_gate.py:788-796 (verified current state, current line numbers)
RATIFIED_VALIDATION_FRAME = FrameConvention(
    position_frame=POSITION_FRAME_RAW,
    time_coord=TIME_COORD_RAW,
    mass_convention=MASS_CONVENTION_ORDERED_RAW,
    conf01_evidence_ref=(
        ".planning/phases/46-frame-resolution-gate-aligned-validation/"
        "evidence/target-frame/20260728T014532Z/raw.json"
    ),
)
```
D-05 requires `position_frame=POSITION_FRAME_SCALED, time_coord=TIME_COORD_NORMALIZED` (both symbols already defined at `:74,76`); `mass_convention` stays `MASS_CONVENTION_ORDERED_RAW` (unchanged — CONF-09 never touches mass encoding). `conf01_evidence_ref` should point at whatever Phase 47 artifact records the D-07 re-ratification bookkeeping (the field's docstring at `:110-112` — "carries the CONF-01 verdict/evidence reference that ratified this frame" — implies it should always point at the evidence backing the *currently active* frame, so this string must change too, not just the two frame fields). The preceding comment block (`:775-787`) narrating the D-09 branch and its 2026-07-28 justification will also read as stale once the constant changes and should be updated or clearly marked superseded in the same diff — leaving stale prose next to a changed constant is exactly the kind of drift this milestone exists to eliminate.

## State of the Art

Not applicable in the conventional "library evolved" sense. The relevant "state of the art" progression is internal to this milestone:

| Prior state | Current/target state | When changed | Impact |
|--------------|------------------|---------------|--------|
| Residents = `pre.r_com_ordered`/`v_com_ordered` (COM+boost+permutation only) | Residents = `pre.r_gauge`/`v_gauge` (+ rotation gauge + D/V scaling) | Phase 47 (this phase), per GAP-46-07 owner ruling 2026-07-28 | Every anchor target (`h0`, `l0`, `true_v0`, IC anchor loss) becomes frame-coherent with `IC₁₃` and with the AD `d/du` derivative for free |
| `RATIFIED_VALIDATION_FRAME = (r_raw, t_native, ordered_raw)` | `(r_prime, u_t_over_T, ordered_raw)` | Same change (D-05) | `COHERENT_FRAME_PAIRS` check stops silently permitting an incoherent training-side pairing |
| `ε_H = |h0| · 1e-4 + 1e-12` (per-anchor, spec-prohibited additive floor) | `ε_H = 1e-4 · S_H` (dataset-wide, no floor) | Phase 47, CONF-02/CONF-03 | Removes the "every anchor is its own yardstick" defect D-20 names; matches `pinn_architecture.md:531,542` literally |

**Deprecated/outdated:** `pre.r_com_ordered`/`v_com_ordered` as a **residency** source (D-03: the fields themselves are NOT deleted — they remain the intermediate the CONF-08 evidence and its tests are written against; only their role as the adapter's exported residency changes).

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | The D-08 "gate metrics unchanged in value" regression check refers to the **training-side** softened Hamiltonian (`_matched_plummer_hamiltonian` at `EPS_SOFT`, feeding `h0`/`S_H`/`ε_H`), not the **validation-side** ACC-03 gate (`gate_metrics.py`, `EPS_INV`) — the two are explicitly documented as distinct quantities sharing a glyph (`ctl_instruction.md:576-580`). CONTEXT.md's D-08 text names `EPS_SOFT` explicitly, which points at the training-side quantity, but the surrounding ROADMAP language ("gate metrics") is generic enough to also describe `compute_validation_gate`'s `aggregate_eps_h`/`aggregate_scs`. This research recommends the planner design the D-08 regression check as a **train-free deterministic comparison** (fixed trajectory, both frame pairings, `_matched_plummer_hamiltonian` at `EPS_SOFT`) rather than assume `compute_validation_gate` is the target, but flags this as unresolved. | Validation Architecture / Common Pitfalls | If the planner builds the wrong regression check, D-08's "approximate invariance" claim would be asserted against the wrong quantity, and the real risk (softening-floor asymmetry in the training-side `h0` computation) would go unverified |
| A2 | `StageIndex.records_at_or_below(0)` (not `records_at(0)`) is the correct accessor for "the Stage-0 admitted set" D-13 refers to, since Stage-0 is the lowest curriculum stage and the two are equivalent at stage 0 in this single-stage (Stage-0-only, SCOPE-27) milestone — but the exact call was not specified in `47-CONTEXT.md` and both methods exist (`pinn/data/splits.py:247-261`). | Pattern 2 | Low risk in practice (the milestone is Stage-0-only per SCOPE-27, so both accessors return the same set today), but the choice should be made deliberately, not by whichever the planner happens to type first, since `records_at_or_below` silently changes behavior once Stage-1+ work resumes post-v2.2 |
| A3 | `numpy.median`'s standard even-population averaging behavior is the correct interpretation of D-14's "averages the two central values on an even population" — this is documented numpy behavior, not verified against numpy's changelog in this session, but is standard, stable, decades-old behavior unlikely to have changed. | Don't Hand-Roll | Negligible — this is well-established stdlib-adjacent behavior; flagged only for completeness of the provenance ledger |

**Overall assessment:** every claim above is `[VERIFIED]` against this session's direct file reads except A1–A3, which are `[ASSUMED]` interpretive judgments the planner should confirm or explicitly re-decide (A1 in particular has execution-order consequences and should be resolved before the D-08 test is written, not discovered mid-implementation).

## Open Questions

1. **What exactly does D-08's "measured before/after gate-metric comparison" test?**
   - What we know: the ROADMAP/CONTEXT text names `EPS_SOFT` and the `r_safe` floor explicitly, pointing at the training-side `_matched_plummer_hamiltonian`. `INST-01`'s production validation-gate observation (`compute_validation_gate`, `pinn/training/validation_gate.py:199-292`) is also plausible since it literally consumes `RATIFIED_VALIDATION_FRAME` and its own `EPS_INV`-based metric would change in numeric value once `gate_time_coordinate` starts dividing by `T`.
   - What's unclear: whether "gate metrics" in this context means the ACC-03 validation gate (`gate_metrics.py`) or the training energy-loss term's implicit gate-like behavior.
   - Recommendation: design D-08 as a **train-free, deterministic, fixture-based** comparison (a fixed synthetic or real trajectory's snapshot-0, computed via `_matched_plummer_hamiltonian` under both the old and new residency pairing) rather than invoking `compute_validation_gate` (which requires a model forward pass and is therefore closer to "training run"-adjacent — SCOPE-27/28 caution warranted). This keeps the regression check unambiguously inside the "no training run, no held-out evaluation" boundary.

2. **Does the `conf01_evidence_ref` field on the re-ratified `RATIFIED_VALIDATION_FRAME` need a genuinely new evidence artifact, or can it point at an existing one?**
   - What we know: D-07 requires recording "what superseded what and on whose authority (the GAP-46-07 owner ruling of 2026-07-28, option A)" as a Phase 47 artifact, "under the same D-12 discipline GAP-46-06 used."
   - What's unclear: whether this is a new file under `.planning/phases/47-frame-completion-s-h-pipeline/evidence/` (mirroring the existing `.../46-.../evidence/target-frame/20260728T014532Z/raw.json` path shape) or whether the field can point directly at `.planning/milestones/v2.2-GAPS.md`'s GAP-46-07 entry.
   - Recommendation: the planner should follow the exact directory-naming convention Phase 46 used (`evidence/target-frame/<timestamp>/...`) for consistency, even though this re-ratification is not itself a new *measurement* — it's a bookkeeping artifact recording an owner ruling, not evidence output from a probe run.

3. **`records_at(0)` vs `records_at_or_below(0)` for the Stage-0 train-admitted population (D-13).**
   - See Assumption A2 above — low risk given SCOPE-27, but worth an explicit, recorded choice.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Python (`.venv`) | All `pinn/` code | ✓ | 3.14 (`.venv/bin/python`) `[VERIFIED]` | — |
| numpy | float64 admission-time computation, `numpy.median` | ✓ | 2.2.0 `[VERIFIED]` | — |
| torch | resident tensors, loss-catalog Hamiltonian | ✓ | 2.12.0 `[VERIFIED]` | — |
| pytest | test execution | ✓ | 9.1.1 `[VERIFIED]` | — |

Note: the bare system `/opt/homebrew/bin/python3` has none of these installed (`ModuleNotFoundError: No module named 'numpy'`, `pytest not found`) — **all commands must use `<home>/Desktop/3_body_problem/.venv/bin/python`** (or the equivalent `$(dirname "$(git rev-parse --git-common-dir)")/.venv/bin/python` form used in Phase 46's summaries), not a bare `python`/`pytest` invocation.

**Missing dependencies with no fallback:** none.
**Missing dependencies with fallback:** none.

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | pytest 9.1.1, collecting `unittest.TestCase`-style test classes (project convention — see `tests/phase46/test_pairing_repair.py`'s `unittest.TestCase` subclasses run via `pytest`) `[VERIFIED: .venv/bin/python -m pytest --version; tests/phase46/test_pairing_repair.py:12,80,198]` |
| Config file | none dedicated — no `pytest.ini`/`pyproject.toml [tool.pytest]` found at repo root; pytest runs with defaults `[VERIFIED: absence checked via `ls`/`grep`]` |
| Quick run command | `.venv/bin/python -m pytest tests/phase47/ -q -rs` (once Wave-0 creates the directory) or a targeted file, e.g. `.venv/bin/python -m pytest tests/phase46/test_pairing_repair.py -q -rs` |
| Full suite command | `.venv/bin/python -m pytest tests/phase41/ tests/phase42/ tests/phase43/ tests/phase46/ tests/phase47/ -q` (mirrors the dependency-scope pattern used at Phase 46 close, `46-10-SUMMARY.md:104-108`) |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| CONF-09 (D-04) | `IC₁₃`/`E` are byte-unchanged by the residency swap | unit / regression | `pytest tests/phase47/test_conf09_frame_completion.py::test_ic13_invariance -x` | ❌ Wave 0 |
| CONF-09 (D-02) | `dr'/du` at u=0 equals `v_gauge[0]` exactly (via `componentwise_du`, `pinn/physics_residual.py:102`) | unit | `pytest tests/phase47/test_conf09_frame_completion.py::test_velocity_identity -x` | ❌ Wave 0 |
| CONF-09 (D-08) | Approximate gate-metric invariance under the swap, tolerance stated (softening-floor asymmetry acknowledged, not exact equality) | regression (train-free, fixture-based per Open Question 1) | `pytest tests/phase47/test_conf09_frame_completion.py::test_gate_metric_near_invariance -x` | ❌ Wave 0 |
| CONF-09 (D-01/D-05) | Residency swap + frame re-ratification land together; `COHERENT_FRAME_PAIRS` accepts the new pairing | unit | `pytest tests/phase47/test_conf09_frame_completion.py::test_ratified_frame_is_coherent -x` | ❌ Wave 0 |
| CONF-09 (D-06) | `tests/phase46/test_pairing_repair.py` corrected in place (both affected methods, see Pitfall 4) | unit (existing file, corrected) | `pytest tests/phase46/test_pairing_repair.py -x -q -rs` | ✅ (correction, not new) |
| CONF-02 (D-09,D-10) | `S_H` uses `EPS_SOFT`, is `K0 + |potential|` (not the signed sum) | unit | `pytest tests/phase47/test_conf02_s_h_pipeline.py::test_uabs0_is_absolute_value -x` | ❌ Wave 0 |
| CONF-02 (D-12,D-13) | `(K0,Uabs0)` captured in float64 at admission; median reduces over train-split-only, once | unit | `pytest tests/phase47/test_conf02_s_h_pipeline.py::test_median_train_split_only -x` | ❌ Wave 0 |
| CONF-02 (D-17) | Non-finite or `≤0` `S_H` fails closed **before step 1** | unit / fail-closed | `pytest tests/phase47/test_conf02_s_h_pipeline.py::test_s_h_fails_closed -x` | ❌ Wave 0 |
| CONF-02 (D-15,D-16,D-18) | `S_H` and `ε_H` both persist in `training_metadata.json`; reader re-validates on load | unit | `pytest tests/phase47/test_conf02_s_h_pipeline.py::test_metadata_roundtrip_revalidates -x` | ❌ Wave 0 |
| CONF-03 (D-19,D-20,D-21) | `ε_H = 1e-4·S_H` reaches `soft_energy_loss`'s denominator unchanged (`|h0|+ε_H`); `+1e-12` deleted; `_AnchorContext.eps_h` still overridable per-test | unit (assembly-boundary, mirrors TEST-02's spirit though TEST-02 itself is Phase 48) | `pytest tests/phase47/test_conf03_eps_h_wiring.py::test_eps_h_assembly_value -x` | ❌ Wave 0 |

### Sampling Rate

- **Per task commit:** targeted file, e.g. `pytest tests/phase47/test_conf09_frame_completion.py -q -rs`
- **Per wave merge:** `pytest tests/phase46/ tests/phase47/ -q -rs`
- **Phase gate:** `pytest tests/phase41/ tests/phase42/ tests/phase43/ tests/phase46/ tests/phase47/ -q` green before `/gsd-verify-work` (the same dependency scope Phase 46 verified against at close, `46-10-SUMMARY.md:105,108` — 12 pre-existing environmental failures in `tests/phase43/` are a known, documented baseline, not new failures to chase)

### Wave 0 Gaps

- [ ] `tests/phase47/__init__.py` — new package
- [ ] `tests/phase47/test_conf09_frame_completion.py` — covers CONF-09 (D-01,D-02,D-04,D-05,D-08)
- [ ] `tests/phase47/test_conf02_s_h_pipeline.py` — covers CONF-02 (D-09..D-18)
- [ ] `tests/phase47/test_conf03_eps_h_wiring.py` — covers CONF-03 (D-19..D-21)
- [ ] `tests/phase46/test_pairing_repair.py` correction (D-06) — existing file, not new, but load-bearing before CONF-09 lands (a stale assertion here will fail-fast in a useful way, but should be fixed in the same change, not left red)
- Framework install: none — pytest/numpy/torch already present in `.venv`

## Security Domain

`security_enforcement` is absent from `.planning/config.json` → treated as enabled per policy, assessed below. This phase has no user-facing surface, no authentication, no network I/O, and no untrusted input beyond the on-disk Brutus corpus (already governed by Phase 39's admission/blacklist machinery, unaffected by this phase). Most ASVS categories are structurally not applicable to an internal, single-operator ML training pipeline with no external attack surface.

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-------------------|
| V2 Authentication | No | No auth surface in this phase |
| V3 Session Management | No | No sessions |
| V4 Access Control | No | Single-operator local training run |
| V5 Input Validation | **Yes** | Fail-closed validation of `S_H`/`ε_H` on read (D-17, D-18) — the closest analog to input validation here is treating a persisted metadata file as untrusted until re-checked, exactly the discipline `validate_sidecar_payload` (`pinn/training/validation_gate.py:541-...`) already establishes for the Phase 46 sidecar and that D-18 explicitly directs CONF-02's reader to mirror |
| V6 Cryptography | No | No secrets, no crypto in this phase |

### Known Threat Patterns for this stack

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|----------------------|
| A truncated or hand-edited `training_metadata.json` silently re-entering the loss with a stale/wrong `ε_H` | Tampering (of a local artifact, not a remote attacker — but the same fail-closed discipline applies) | Re-validate the fail-closed predicate (`math.isfinite(S_H) and S_H > 0`) on every load, not just at write time (D-18) — mirrors `validate_sidecar_payload`'s existing discipline exactly |
| A partially-written metadata file left behind by a crashed run being read as complete | Tampering / Denial of Service (of correctness, not availability) | Atomic write via `pinn.training.atomic_io.atomic_write_text` (same primitive already used for the Phase 46 sidecar), never a direct `open().write()` |
| A run silently proceeding past step 1 despite an invalid `S_H` | Repudiation (the run would produce artifacts that "read like real evidence" per D-17's own language, with no record that the precondition failed) | Fail at setup, before step 1, with a clear refusal — never lazily at first loss-term use (D-17 explicit) |

## Sources

### Primary (HIGH confidence — direct source-file verification this session)

- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:505-594` — §3.4 governing text, `K0`/`Uabs0`/`S_H`/`ε_H` formulas and prose, the "Initial Energy Calculation" reference listing
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:570-585` — the distinct admission-gate `eps_H` note ("same glyph, different quantity")
- `pinn/data/adapter.py:780-1038` — `_scan_and_admit`, `_materialize`, `AdmittedSetAdapter` accessors
- `pinn/data/preprocessing.py:63-222` — `PreprocessedTrajectory`, `preprocess_trajectory`
- `pinn/data/types.py:201-231` — `AdmittedRecord`
- `pinn/loss_catalog.py:100-300` — `LossTerms`, `_matched_plummer_hamiltonian`, `soft_energy_loss`
- `pinn/training/controllers.py:286-520` — `RunController.__init__`, `_build_anchor_context`, `_data_term`/`_non_data_terms`
- `pinn/training/validation_gate.py:1-796` — frame constants, `FrameConvention`, `gate_time_coordinate`, `compute_validation_gate`, `validate_sidecar_payload`, `RATIFIED_VALIDATION_FRAME`
- `pinn/data/splits.py:150-283,773-797` — `StageIndex.from_split`, `_source_value`, `write_split_manifest`
- `pinn/training/config.py:130-175,409` — `_PROVISIONAL` registry, `energy_floor_factor`
- `pinn/train.py:381-421,740-806,950-980` — `_build_admitted_sources`, run-setup sequence, `RunController` construction site
- `pinn/constants.py:1-45` — `EPS_SOFT`, `D_CHARACTERISTIC_LENGTH`, `T_CHARACTERISTIC_TIME`
- `pinn/verification/gate_metrics.py:1-70` — `EPS_INV`, its "NEVER" warning, gate contract docstring
- `pinn/physics_residual.py:102-127` — `componentwise_du`
- `tests/phase46/test_pairing_repair.py` (full file, 367 lines) — exact test methods affected by D-06
- `pinn/training/atomic_io.py:21-67` — `atomic_write_text` (the atomic-write primitive to reuse)
- `docs/work/reviews/cross_cutting/stage0-conformance-audit/2026-07-28-conformance-divergence-verification-report.md:85-307` — CONF-09 derivation, D-06a/D-06b/rotation-gauge finding, recommended repair table
- `.planning/phases/46-frame-resolution-gate-aligned-validation/46-10-SUMMARY.md:103-108` — the pytest invocation convention

### Secondary (MEDIUM confidence)

- `.planning/phases/47-frame-completion-s-h-pipeline/47-CONTEXT.md` — the owner-ratified decision set this research implements against (all D-01..D-27); treated as authoritative per the phase's own instructions, cross-checked against source where a code citation was given
- `.planning/REQUIREMENTS.md:33-45,137-141` — CONF-02/03/09 requirement text and the GAP-46-07 amendment narrative

### Tertiary (LOW confidence — none)

No claims in this document rely on unverified web search or training-data recall; this is an internal-codebase research task with no external library surface, so no tertiary sources were consulted.

## Metadata

**Confidence breakdown:**
- Standard stack: N/A (no new dependencies) — HIGH confidence that none are needed, verified by reading every touched module's imports
- Architecture: HIGH — every code seam named in `47-CONTEXT.md` was independently re-verified against the live file this session, and one line-citation drift was caught and corrected (Pitfall 1)
- Pitfalls: HIGH — five pitfalls identified, four fully grounded in direct source inspection (Pitfalls 2-5), one (Pitfall 1) is itself a verified citation-drift finding
- Validation architecture: MEDIUM — the test *shape* and file organization follow established Phase 46 convention with HIGH confidence; the exact D-08 regression-check target (Open Question 1 / Assumption A1) is a genuine unresolved interpretive question the planner should settle explicitly

**Research date:** 2026-07-29
**Valid until:** re-verify line-number citations if any additional Phase 46/47 commits land before planning begins — this codebase's line numbers have already been observed to drift once (Pitfall 1) between the 2026-07-28 audit report and this 2026-07-29 research session, roughly 24 hours apart. Otherwise the architectural findings (which files/functions are involved, what they currently do) are stable until the swap itself is implemented.
