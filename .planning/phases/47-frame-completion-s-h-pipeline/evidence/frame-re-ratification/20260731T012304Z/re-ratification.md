# RATIFIED_VALIDATION_FRAME re-ratification record — Phase 47 Plan 01 (CONF-09)

**Recorded:** 2026-07-31 (UTC directory stamp `20260731T012304Z`)
**Artifact class:** bookkeeping on an existing owner ruling (47-CONTEXT.md D-07).
**Not** a new gap, **not** a new CONF-01 verdict, **not** a new decision.

---

## 1. What superseded what

`pinn/training/validation_gate.py::RATIFIED_VALIDATION_FRAME` moved, in the same
commit as the CONF-09 residency swap, from

| field | before (Phase 46 plan 46-07) | after (Phase 47 plan 47-01) |
|---|---|---|
| `position_frame` | `POSITION_FRAME_RAW` = `"r_raw"` | `POSITION_FRAME_SCALED` = `"r_prime"` |
| `time_coord` | `TIME_COORD_RAW` = `"t_native"` | `TIME_COORD_NORMALIZED` = `"u_t_over_T"` |
| `mass_convention` | `MASS_CONVENTION_ORDERED_RAW` = `"ordered_raw"` | `MASS_CONVENTION_ORDERED_RAW` = `"ordered_raw"` (unchanged — the mass encoding never moves) |
| `conf01_evidence_ref` | `.planning/phases/46-frame-resolution-gate-aligned-validation/evidence/target-frame/20260728T014532Z/raw.json` | this file |

Tuple form: `("r_raw", "t_native", "ordered_raw")` → `("r_prime", "u_t_over_T",
"ordered_raw")`. Both pairs are members of `COHERENT_FRAME_PAIRS`
(`validation_gate.py`, the `POSITION_FRAME_*` / `TIME_COORD_*` block); the
scaled pair is the locked contract, and the raw pair existed only to express the
owner-ratified D-09 branch outcome.

**Why it had to be the same commit.** The constant describes what the adapter
actually serves. The CONF-09 swap changed that: `AdmittedSetAdapter` residency
moved to `preprocess_trajectory`'s fully rotation-gauged, `D`/`V`-scaled output,
paired with the `u = t/T` normalization already applied at the sampling
boundary. A tree in which residency has moved and this constant has not is a
tree whose `COHERENT_FRAME_PAIRS` admission check is lying about the
measurement it admits (47-CONTEXT.md D-05).

## 2. On whose authority

The **GAP-46-07 owner ruling of 2026-07-28, option A**, recorded in
`.planning/milestones/v2.2-GAPS.md` (GAP-46-07) and in full in
`.planning/phases/46-frame-resolution-gate-aligned-validation/46-GAPS.md`. That
ruling re-scoped Phase 47 so the frame condition Phase 47 was waiting on is
satisfied *by* Phase 47: CONF-09 completes the residency transform first, and
`S_H` is then computed once in the canonical scaled frame.

The staleness condition was **declared in advance** by GAP-46-06's own constant.
The superseded comment block above `RATIFIED_VALIDATION_FRAME` read:

> Re-ratification is REQUIRED if Phase 47/48 moves residency to the locked
> canonical scaled contract (r' with u = t/T); this constant then goes stale.

`.planning/ROADMAP.md` (Phase 46 amendment, 2026-07-28) states the same standing
consequence: *"`RATIFIED_VALIDATION_FRAME` goes stale if Phase 47/48 moves
residency to the locked canonical scaled contract, and re-ratification is then
required under the same D-12 discipline."* This record is that re-ratification,
executed under the same discipline: the values are quoted from the locked
requirement text, never inferred from any measurement.

Grounding for the destination values: `.planning/REQUIREMENTS.md` CONF-09 and
`.planning/ROADMAP.md` Phase 47 SC-2, both naming
`(POSITION_FRAME_SCALED, TIME_COORD_NORMALIZED, MASS_CONVENTION_ORDERED_RAW)`.

## 3. What is NOT changed by this record (D-27)

CONF-01's Complete status and its mandatory EVAL-01 precondition-(ii) qualification are unchanged by this phase.
CONF-09 *applies* CONF-01's answer; it does not
re-decide it. The Phase 46 machine verdict `VERDICT_NON_FRAME_DIVERGENCE`
recorded in `46-VERDICT-POSTREPAIR.md` is not overwritten, not revisited, and
not superseded by anything in this file. This artifact is bookkeeping on an
existing ruling — it is **not** a new gap and **not** a new CONF-01 verdict.

Also unchanged in this plan: `COHERENT_FRAME_PAIRS`, `_validate_frame`, every
other function in `validation_gate.py`, `pinn/data/preprocessing.py` (the
`r_com_ordered` / `v_com_ordered` intermediate fields survive per D-03), the
`IC₁₃`/`E` construction in `pinn/data/adapter.py`, the `u = t/T` normalization
boundary in `pinn/data/batches.py`, and
`pinn/verification/target_frame_probe.py`.

## 4. Regression evidence (D-22/D-23)

*Appended by plan 47-01 task 3. The implementation was frozen before any number
below was observed — the probe records repository commit `1c68368d`, which is
the task-2 test commit, i.e. everything this plan ships. That ordering is the
defence SCOPE-29 requires: nothing ships after these numbers, so they cannot
have steered an implementation choice.*

### 4.1 D-22 — the one-shot CONF-01 re-probe

**Framing, mandatory and load-bearing.** This is a **regression check that
residency equals the canonical preprocessing output**. `identity_scaled` is
**true by construction** after the CONF-09 swap — the adapter now serves exactly
`preprocess_trajectory`'s `r_gauge`/`v_gauge`, which is the array the probe's
`identity_scaled` test compares against. It is therefore **NOT a frame test**,
and it is **not a new CONF-01 verdict** and must never be cited as one (D-22,
D-27, SCOPE-29). CONF-01's Complete status is untouched; Plan 46-09's machine
verdict stands unamended.

**Run count: exactly one.** Exit 0 on the first invocation; no retry, no loop.

**Preflight (convergence cycle-2 requirement).** Before invoking, each input was
resolved the way the probe itself resolves it:

| input | resolution rule | resolved location | sha256 | matches Phase 46? |
|---|---|---|---|---|
| manifest 1 | `--manifest` path as given (CWD-relative) | `runs/stage0-pilot-seed41/splits.json` | `c25568a18f3c4e31bcef5bf36f71591f0978edca4ca6cd490a28ec88ea276c86` | yes |
| manifest 2 | same | `runs/stage0-pilot-seed42/splits.json` | `5846ae5b55104e55a85d644875c3da187200c3d521f52a9298876d656c6d8903` | yes |
| manifest 3 | same | `runs/stage0-pilot-seed43/splits.json` | `a8618b0c6d0f0f1487fe4e3f8c0409a3e3398c7e8cb8bee2b4d3d7962a576172` | yes |
| blacklist | see below | `<main-repo-root>/simulation_data/Documentation/problematic_ics_blacklist.json` | `238efd128cd04307708f74bbb54c23cad2cfec8b1cd6cfb09df62d830bae3e44` | yes |
| corpus data root | `default_data_root()` = parent of `git rev-parse --git-common-dir` + `simulation_data/Data` | `<main-repo-root>/simulation_data/Data` | — | yes (`data_root_source = git_common_dir_default`) |

The blacklist was the case the cycle-2 review anticipated. A literal CWD-relative
`test -f problematic_ics_blacklist.json` MISSES in this worktree, and so does the
probe's own default `adapter.data_root / DEFAULT_BLACKLIST_NAME`. The file is
nevertheless **not genuinely missing**: it lives under
`simulation_data/Documentation/` and its sha256 is byte-identical to the one
Phase 46 recorded. The bare basename in Phase 46's serialized invocation is a
redaction artifact, not a location: `_reduce_path` returns the BASENAME for any
path outside the probe's repo root (`target_frame_probe.py:1560-1571`), and the
main-repo `simulation_data/` tree is outside this worktree's root. STOP-and-
surface therefore did NOT fire — the condition for it is a file the probe's own
resolution cannot find at all.

*(Absolute paths are written repo-anchored above rather than host-absolute. This
is not evasion: the probe's own evidence writer refuses to serialize a
host-absolute source root, username, or hostname (T-46-04-02,
`_guard_serialized_bytes`), so a host-absolute literal here would contradict the
instrument this record is about. `<main-repo-root>` is the parent of
`git rev-parse --git-common-dir`, which is exactly how the probe resolves it, so
the path is re-derivable on any checkout.)*

**Invocation, as serialized by the probe** (path-reduced by the instrument):

```text
python -m pinn.verification.target_frame_probe \
  --manifest runs/stage0-pilot-seed41/splits.json \
  --manifest runs/stage0-pilot-seed42/splits.json \
  --manifest runs/stage0-pilot-seed43/splits.json \
  --blacklist-path problematic_ics_blacklist.json \
  --evidence-root .planning/phases/47-frame-completion-s-h-pipeline/evidence/target-frame
```

Identical to the Phase 46 invocation recorded in `46-VERDICT-POSTREPAIR.md`
except for `--evidence-root`. That flag is required — the probe's default
evidence root is the **Phase 46** tree, and writing there would both contaminate
Phase 46's retained evidence and violate this plan's one-directory cap. It
changes the output destination only; the instrument, the population, and the
measurement are untouched. `pinn/verification/target_frame_probe.py` has no diff
across this entire plan.

**Evidence:**
`.planning/phases/47-frame-completion-s-h-pipeline/evidence/target-frame/20260731T014625Z/`
(`raw.json`, `summary.md`). Repository commit measured against: `1c68368d7b1b19427fbcb59205387f7892051232`.
Environment: data-root source `git_common_dir_default`; torch `2.12.0`; resident
dtype/device `float32`/`cpu`; probe mathematics `float64`; schema
`phase46-target-frame/v1`. Population: **1651** eligible Stage-0 trajectories —
the same GAP-46-02 Option A population Phase 46 measured.

**Recorded fields (D-22 requires `identity_scaled` and `first_diverging_step`):**

| field | Phase 46 post-repair | Phase 47 post-CONF-09 |
|---|---|---|
| `identity_scaled` | false for 1651/1651 (`identity_neither`) | **true for 1651/1651** |
| `first_diverging_step` | — (`identity_neither`) | **`null` for 1651/1651** — no step diverges |
| `identity_max_abs_diff.positions_vs_r_gauge` | — | **0.0** (max over all 1651) |
| `identity_max_abs_diff.velocities_vs_v_gauge` | — | **0.0** (max over all 1651) |
| `stepwise_attribution.plus_permutation` | 0.0 for 1651/1651 | non-zero (expected: residency is no longer the pre-rotation intermediate) |
| `stepwise_attribution.plus_scale` | non-zero | **0.0 for 1651/1651** |

The exact-zero `positions_vs_r_gauge` / `velocities_vs_v_gauge` across the whole
population is the regression statement this run exists to make: **residency IS
the canonical preprocessing output, bit for bit.** The `plus_permutation` →
`plus_scale` handover is the same statement read through the stepwise
attribution — the chain now matches at the final step instead of the
permutation step.

Both control arms reproduce their Phase 46 values to serialized precision
(positive-control residual median `0.08022618097116868`, provenance-control
`0.08022618097116782`; both `1651/1651` consistent, `0/1651` separated), so the
instrument and the population did not move.

**Machine verdict: `VERDICT_AMBIGUOUS`.** Recorded verbatim and NOT interpreted.
Per D-22/D-27 this is not a frame verdict and is not routed as one: the probe's
verdict rules were written for the pre-CONF-09 world, in which the scaled
hypothesis was the open question. It is preserved here only so the record is
complete.

### 4.2 D-23 — the measured D-08 before/after gate-metric comparison

**Method.** The dual-arm, train-free computation is the committed
`tests/phase47/test_conf09_frame_completion.py::dual_arm_frame_comparison`; the
per-trajectory bound is the committed `frame_drift_tolerance` helper in the same
module. Nothing was reimplemented for this record.

* OLD arm — `{position: r_com_ordered, time: t_native, velocity: v_com_ordered, masses: ordered_raw}`
* NEW arm — `{position: r_prime, time: u = t/T, velocity: dr_prime_du, masses: ordered_raw}`
* validation-side reading — `pinn.verification.gate_metrics` at its own `EPS_INV = 1e-10` (velocity by finite difference of positions)
* loss-side reading — `pinn.loss_catalog._matched_plummer_hamiltonian` at its own `EPS_SOFT = 1e-5` (stored velocities)

**Population and sample rule (deterministic, documented).** Eligible = Stage-0
records that are train-or-validation in **every** one of the three manifests,
minus the blacklisted physical keys — the probe's own eligibility rule, giving
the same **1651** trajectories. Every eligible record is `hierarchical`/`base`
(standard-variant groups carry `base_stage = UNASSIGNED`). Runtime demands a
subset, so the sample is an evenly-spaced deterministic stride over the sorted
eligible list: index `round(i * (N-1) / (k-1))` for `i = 0 … k-1`, `N = 1651`,
`k = 50`. No RNG, no hand-picking.

**Summary.**

| reading | eps | median `eps_H` OLD | median `eps_H` NEW | max abs difference | min derived bound | max derived bound | max difference/bound | within bound |
|---|---|---|---|---|---|---|---|---|
| validation-side | 1e-10 | 1.470877e-01 | 1.470877e-01 | 1.724e-14 | 2.296e-15 | 4.820e-15 | 4.7611 | **41/50** |
| loss-side | 1e-05 | 4.942078e-10 | 1.064725e-08 | 5.687e-08 | 9.449e-09 | 1.627e-07 | 0.6693 | 50/50 |

**What the measurement says about the physics.** The relative-drift metric is
frame-invariant to the precision the arithmetic can express. The validation-side
`eps_H` agrees between the two arms to ~13 significant digits on every sampled
trajectory (medians identical to all seven printed digits; absolute differences
1e-17 … 1e-14 on values of order 1e-1). The loss-side arm shows the visible
softening-floor asymmetry D-08 predicted — `eps_H` rises from ~5e-10 to ~1e-8 —
because at `EPS_SOFT = 1e-5` the same numeric `eps` acts as an effective
`D*eps ≈ 4.6e-5` in old-frame units, and that arm stays inside its derived bound
on all 50 trajectories. **The D-08 claim itself is confirmed.**

**FINDING — SURFACED TO THE OWNER, NOT RESOLVED HERE.** The derived bound is
**exceeded on the validation-side reading for 9 of 50 sampled real
trajectories** (max ratio 4.76; median ratio 0.47). The excess is diagnosed, from
the derivation itself and not from the numbers, as an omission in Step 4: its
operation counts (`4` for the `D` identity, `8` for the `H` assembly) cover the
frame identity and the Hamiltonian assembly, but the validation-side reading
derives velocity by a **divided difference of positions**
(`gate_metrics.py:84-123`). On real Brutus sampling (`dt_out ≈ 0.01 … 0.08` over
`t ∈ [0, 10]`) the numerator `pos[k+1] - pos[k-1]` is a cancelling subtraction of
O(1) operands, so the finite-difference velocity carries a relative error
amplified by roughly `|r| / |Δr| ≈ 10² … 10³` unit round-offs — a term Step 4
does not contain. The loss-side reading consumes STORED velocities, incurs no
such cancellation, and stays inside the bound, which is exactly the signature
this diagnosis predicts. The tiny-corpus unit fixture samples 12–24 snapshots
over the same horizon, so its `h ≈ 0.9` produces almost no cancellation and
`test_gate_metric_near_invariance` passes on its own fixtures.

**Nothing was changed in response.** `frame_drift_tolerance` was not widened, its
operation counts were not raised, and the unit test was not relaxed —
SCOPE-29/D-26 forbid letting an observed number steer the tolerance, and the plan
pins the derivation explicitly. Extending Step 4 with a finite-difference
cancellation term, or narrowing the D-08 claim to the loss-side reading, is a
change to a derivation this plan was told not to change after observing numbers.
It is routed to the owner.

**Per-trajectory record** (both readings; `bound` is the computed
`frame_drift_tolerance` column, which varies with each trajectory's closest
approach and `|H_old(0)|` — it is not one constant):

| variant | fidelity | id | reading | eps_H old | eps_H new | abs difference | derived bound |
|---|---|---|---|---|---|---|---|
| hierarchical | base | 0000 | validation | 8.698750e-02 | 8.698750e-02 | 2.068e-15 | 3.450e-15 |
| hierarchical | base | 0000 | loss | 1.583116e-10 | 3.410926e-09 | 3.253e-09 | 1.528e-08 |
| hierarchical | base | 0118 | validation | 8.496125e-02 | 8.496125e-02 | 2.595e-15 | 3.715e-15 |
| hierarchical | base | 0118 | loss | 2.778112e-10 | 5.984886e-09 | 5.707e-09 | 1.801e-08 |
| hierarchical | base | 0210 | validation | 9.346796e-02 | 9.346796e-02 | 4.066e-15 | 3.308e-15 |
| hierarchical | base | 0210 | loss | 9.253670e-11 | 1.993463e-09 | 1.901e-09 | 2.324e-08 |
| hierarchical | base | 0302 | validation | 3.960054e-01 | 3.960054e-01 | 8.327e-16 | 3.964e-15 |
| hierarchical | base | 0302 | loss | 2.224042e-09 | 4.791554e-08 | 4.569e-08 | 8.604e-08 |
| hierarchical | base | 0420 | validation | 1.717153e-01 | 1.717153e-01 | 1.749e-15 | 2.296e-15 |
| hierarchical | base | 0420 | loss | 2.189578e-09 | 4.717339e-08 | 4.498e-08 | 1.627e-07 |
| hierarchical | base | 0542 | validation | 2.508478e-01 | 2.508478e-01 | 1.277e-15 | 3.771e-15 |
| hierarchical | base | 0542 | loss | 6.780479e-10 | 1.460817e-08 | 1.393e-08 | 5.315e-08 |
| hierarchical | base | 0661 | validation | 9.918881e-02 | 9.918881e-02 | 1.724e-14 | 3.620e-15 |
| hierarchical | base | 0661 | loss | 5.655556e-10 | 1.218431e-08 | 1.162e-08 | 2.510e-08 |
| hierarchical | base | 0743 | validation | 3.824582e-02 | 3.824582e-02 | 2.054e-15 | 3.619e-15 |
| hierarchical | base | 0743 | loss | 2.508583e-10 | 5.404306e-09 | 5.153e-09 | 1.154e-08 |
| hierarchical | base | 0863 | validation | 6.072469e-02 | 6.072469e-02 | 7.563e-16 | 3.286e-15 |
| hierarchical | base | 0863 | loss | 1.416211e-10 | 3.050892e-09 | 2.909e-09 | 1.890e-08 |
| hierarchical | base | 0969 | validation | 3.673960e-01 | 3.673960e-01 | 1.887e-15 | 4.126e-15 |
| hierarchical | base | 0969 | loss | 8.511085e-10 | 1.833687e-08 | 1.749e-08 | 6.091e-08 |
| hierarchical | base | 1089 | validation | 6.551244e-02 | 6.551244e-02 | 6.925e-15 | 3.254e-15 |
| hierarchical | base | 1089 | loss | 3.723113e-11 | 8.019161e-10 | 7.647e-10 | 1.571e-08 |
| hierarchical | base | 1191 | validation | 4.519053e-02 | 4.519053e-02 | 4.864e-15 | 3.367e-15 |
| hierarchical | base | 1191 | loss | 1.119337e-10 | 2.411362e-09 | 2.299e-09 | 1.271e-08 |
| hierarchical | base | 1297 | validation | 2.468056e-01 | 2.468056e-01 | 1.499e-15 | 3.701e-15 |
| hierarchical | base | 1297 | loss | 1.485461e-09 | 3.200351e-08 | 3.052e-08 | 6.679e-08 |
| hierarchical | base | 1402 | validation | 4.199852e-01 | 4.199852e-01 | 1.166e-15 | 3.506e-15 |
| hierarchical | base | 1402 | loss | 2.746086e-09 | 5.916294e-08 | 5.642e-08 | 1.406e-07 |
| hierarchical | base | 1510 | validation | 6.639016e-02 | 6.639016e-02 | 5.829e-16 | 3.245e-15 |
| hierarchical | base | 1510 | loss | 1.318127e-10 | 2.839995e-09 | 2.708e-09 | 1.989e-08 |
| hierarchical | base | 1611 | validation | 1.433227e-01 | 1.433227e-01 | 6.717e-15 | 3.291e-15 |
| hierarchical | base | 1611 | loss | 7.843234e-11 | 1.689588e-09 | 1.611e-09 | 3.635e-08 |
| hierarchical | base | 1692 | validation | 1.399537e-01 | 1.399537e-01 | 8.327e-17 | 3.312e-15 |
| hierarchical | base | 1692 | loss | 9.544585e-10 | 2.056319e-08 | 1.961e-08 | 4.304e-08 |
| hierarchical | base | 1787 | validation | 9.738787e-02 | 9.738787e-02 | 3.234e-15 | 3.312e-15 |
| hierarchical | base | 1787 | loss | 3.443859e-10 | 7.419455e-09 | 7.075e-09 | 2.794e-08 |
| hierarchical | base | 1888 | validation | 8.620874e-02 | 8.620874e-02 | 1.005e-14 | 3.383e-15 |
| hierarchical | base | 1888 | loss | 5.276289e-10 | 1.136721e-08 | 1.084e-08 | 2.370e-08 |
| hierarchical | base | 1984 | validation | 1.061494e-01 | 1.061494e-01 | 5.551e-17 | 3.555e-15 |
| hierarchical | base | 1984 | loss | 6.688888e-10 | 1.441074e-08 | 1.374e-08 | 2.965e-08 |
| hierarchical | base | 2107 | validation | 7.035847e-02 | 7.035847e-02 | 7.591e-15 | 3.517e-15 |
| hierarchical | base | 2107 | loss | 4.607866e-10 | 9.927289e-09 | 9.467e-09 | 2.029e-08 |
| hierarchical | base | 2197 | validation | 1.231975e-01 | 1.231975e-01 | 4.718e-16 | 3.558e-15 |
| hierarchical | base | 2197 | loss | 1.600642e-10 | 3.448688e-09 | 3.289e-09 | 2.217e-08 |
| hierarchical | base | 2300 | validation | 1.508278e-01 | 1.508278e-01 | 5.829e-16 | 3.426e-15 |
| hierarchical | base | 2300 | loss | 2.002443e-09 | 4.314129e-08 | 4.114e-08 | 6.146e-08 |
| hierarchical | base | 2390 | validation | 1.717301e-01 | 1.717301e-01 | 4.441e-16 | 3.455e-15 |
| hierarchical | base | 2390 | loss | 1.859835e-09 | 4.006876e-08 | 3.821e-08 | 5.747e-08 |
| hierarchical | base | 2496 | validation | 2.028867e-01 | 2.028867e-01 | 2.026e-15 | 3.709e-15 |
| hierarchical | base | 2496 | loss | 2.757386e-10 | 5.940756e-09 | 5.665e-09 | 3.099e-08 |
| hierarchical | base | 2602 | validation | 1.587900e-01 | 1.587900e-01 | 1.055e-15 | 3.300e-15 |
| hierarchical | base | 2602 | loss | 3.642758e-10 | 7.848301e-09 | 7.484e-09 | 3.965e-08 |
| hierarchical | base | 2687 | validation | 3.933138e-01 | 3.933138e-01 | 3.886e-16 | 4.171e-15 |
| hierarchical | base | 2687 | loss | 1.651835e-09 | 3.558763e-08 | 3.394e-08 | 8.729e-08 |
| hierarchical | base | 2790 | validation | 2.754251e-01 | 2.754251e-01 | 0.000e+00 | 3.328e-15 |
| hierarchical | base | 2790 | loss | 8.300529e-10 | 1.788328e-08 | 1.705e-08 | 8.219e-08 |
| hierarchical | base | 2927 | validation | 2.713511e-01 | 2.713511e-01 | 9.437e-16 | 2.994e-15 |
| hierarchical | base | 2927 | loss | 1.368010e-09 | 2.947277e-08 | 2.810e-08 | 9.073e-08 |
| hierarchical | base | 3012 | validation | 4.822827e-02 | 4.822827e-02 | 5.065e-16 | 3.389e-15 |
| hierarchical | base | 3012 | loss | 2.060542e-10 | 4.439157e-09 | 4.233e-09 | 1.115e-08 |
| hierarchical | base | 3119 | validation | 2.704379e-01 | 2.704379e-01 | 1.721e-15 | 3.245e-15 |
| hierarchical | base | 3119 | loss | 9.928095e-10 | 2.138947e-08 | 2.040e-08 | 8.643e-08 |
| hierarchical | base | 3216 | validation | 2.828551e-01 | 2.828551e-01 | 1.443e-15 | 3.356e-15 |
| hierarchical | base | 3216 | loss | 6.406792e-10 | 1.380264e-08 | 1.316e-08 | 6.394e-08 |
| hierarchical | base | 3326 | validation | 2.960013e-01 | 2.960013e-01 | 6.661e-16 | 3.453e-15 |
| hierarchical | base | 3326 | loss | 9.657041e-10 | 2.080547e-08 | 1.984e-08 | 7.042e-08 |
| hierarchical | base | 3415 | validation | 4.333210e-02 | 4.333210e-02 | 2.165e-15 | 3.396e-15 |
| hierarchical | base | 3415 | loss | 1.834468e-10 | 3.952230e-09 | 3.769e-09 | 1.233e-08 |
| hierarchical | base | 3508 | validation | 6.262754e-02 | 6.262754e-02 | 3.192e-15 | 3.242e-15 |
| hierarchical | base | 3508 | loss | 1.300444e-10 | 2.801640e-09 | 2.672e-09 | 1.933e-08 |
| hierarchical | base | 3596 | validation | 1.429867e-01 | 1.429867e-01 | 8.327e-16 | 3.373e-15 |
| hierarchical | base | 3596 | loss | 3.890286e-10 | 8.381534e-09 | 7.993e-09 | 3.472e-08 |
| hierarchical | base | 3703 | validation | 1.908436e-01 | 1.908436e-01 | 6.023e-15 | 3.393e-15 |
| hierarchical | base | 3703 | loss | 1.532475e-09 | 3.301577e-08 | 3.148e-08 | 5.720e-08 |
| hierarchical | base | 3813 | validation | 1.898802e-02 | 1.898802e-02 | 1.461e-15 | 3.320e-15 |
| hierarchical | base | 3813 | loss | 9.382299e-11 | 2.021370e-09 | 1.928e-09 | 9.449e-09 |
| hierarchical | base | 3906 | validation | 5.453949e-02 | 5.453949e-02 | 2.547e-15 | 3.329e-15 |
| hierarchical | base | 3906 | loss | 1.586776e-10 | 3.418902e-09 | 3.260e-09 | 1.336e-08 |
| hierarchical | base | 4004 | validation | 1.901634e-01 | 1.901634e-01 | 6.106e-16 | 3.649e-15 |
| hierarchical | base | 4004 | loss | 3.652559e-10 | 7.869144e-09 | 7.504e-09 | 3.025e-08 |
| hierarchical | base | 4123 | validation | 3.575128e-01 | 3.575128e-01 | 5.551e-16 | 4.820e-15 |
| hierarchical | base | 4123 | loss | 1.560769e-09 | 3.362578e-08 | 3.207e-08 | 6.685e-08 |
| hierarchical | base | 4262 | validation | 3.891017e-01 | 3.891017e-01 | 2.109e-15 | 3.836e-15 |
| hierarchical | base | 4262 | loss | 2.768018e-09 | 5.963555e-08 | 5.687e-08 | 1.123e-07 |
| hierarchical | base | 4357 | validation | 1.433476e-01 | 1.433476e-01 | 5.551e-16 | 3.354e-15 |
| hierarchical | base | 4357 | loss | 3.851655e-10 | 8.298077e-09 | 7.913e-09 | 3.235e-08 |
| hierarchical | base | 4428 | validation | 9.450085e-02 | 9.450085e-02 | 2.276e-15 | 3.284e-15 |
| hierarchical | base | 4428 | loss | 7.923181e-11 | 1.706744e-09 | 1.628e-09 | 2.409e-08 |
| hierarchical | base | 4520 | validation | 2.794586e-01 | 2.794586e-01 | 1.887e-15 | 3.914e-15 |
| hierarchical | base | 4520 | loss | 1.773146e-09 | 3.820149e-08 | 3.643e-08 | 6.705e-08 |
| hierarchical | base | 4609 | validation | 2.250630e-01 | 2.250630e-01 | 4.718e-15 | 3.486e-15 |
| hierarchical | base | 4609 | loss | 1.419339e-09 | 3.057865e-08 | 2.916e-08 | 5.676e-08 |
| hierarchical | base | 4717 | validation | 5.550861e-02 | 5.550861e-02 | 1.860e-15 | 3.395e-15 |
| hierarchical | base | 4717 | loss | 2.371746e-10 | 5.109811e-09 | 4.873e-09 | 1.496e-08 |
| hierarchical | base | 4816 | validation | 2.366017e-01 | 2.366017e-01 | 3.608e-15 | 4.206e-15 |
| hierarchical | base | 4816 | loss | 6.642784e-10 | 1.431154e-08 | 1.365e-08 | 3.457e-08 |
| hierarchical | base | 4907 | validation | 2.093957e-01 | 2.093957e-01 | 8.882e-16 | 3.167e-15 |
| hierarchical | base | 4907 | loss | 2.956644e-10 | 6.369771e-09 | 6.074e-09 | 7.339e-08 |
| hierarchical | base | 4999 | validation | 2.220967e-01 | 2.220967e-01 | 2.581e-15 | 3.239e-15 |
| hierarchical | base | 4999 | loss | 1.020313e-09 | 2.198149e-08 | 2.096e-08 | 7.594e-08 |

**Reproduction.** Everything above re-derives from committed state:

```python
# PYTHONPATH=<repo root>, .venv/bin/python
from pinn.data.adapter import parse_brutus_file, default_data_root
from pinn.data.preprocessing import preprocess_trajectory
from tests.phase47.test_conf09_frame_completion import dual_arm_frame_comparison
parsed = parse_brutus_file(path, root=default_data_root())
pre = preprocess_trajectory(parsed.times, parsed.positions,
                            parsed.velocities, parsed.masses)
dual_arm_frame_comparison(pre, parsed.times)   # -> {"validation": {...}, "loss": {...}}
```

with the sample selected by the stride rule stated above over the three
manifests' shared train-or-validation Stage-0 population.

### 4.3 What the two records answer together

* **Did residency change?** Yes, exactly and everywhere — `identity_scaled` true
  for 1651/1651 with a zero maximum absolute difference against
  `r_gauge`/`v_gauge` (§4.1).
* **Did anything observable change that shouldn't have?** No. The relative-drift
  metric is invariant to ~13 significant digits on the validation-side reading,
  and moves on the loss-side reading only by the softening-floor asymmetry D-08
  predicted, inside its derived bound (§4.2). The one open item is the
  bound's own float64 allowance for the finite-difference reading, surfaced
  above and left for the owner.
