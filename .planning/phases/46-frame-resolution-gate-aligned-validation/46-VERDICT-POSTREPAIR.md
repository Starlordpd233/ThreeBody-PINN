# CONF-01 Post-Repair Target-Frame Verdict — Phase 46 Plan 09

**Machine verdict: `VERDICT_NON_FRAME_DIVERGENCE`** — measured over **1651**
eligible Stage-0 trajectories. **Branch: D-09, rule 5.** This is not a clean
raw or scaled verdict, and no validation frame is ratified by this plan.

The CONF-08 repair itself is visible and exact: the resident position array
matches the ordered COM/boost intermediate (`r_bar_perm`) for all 1651
trajectories (`stepwise_attribution.plus_permutation = 0.0`). The unchanged
probe nevertheless classifies every resident as `identity_neither` because its
identity checks recognize only parsed file-order raw arrays or the fully
rotated/scaled canonical output. Its pre-repair pairing discriminators also
retain their original semantics: `permutation_identity` describes whether the
canonical permutation is mathematically the identity, and the
permutation-"corrected" raw arm always inverse-permutes the stored masses. Those
tests do not mean the repaired resident is still mis-paired.

## Evidence citation

- **Run directory:** `.planning/phases/46-frame-resolution-gate-aligned-validation/evidence/target-frame/20260728T014532Z/`
  (`raw.json`, `summary.md`)
- **raw.json SHA-256:** `11b6690add8bb18181efadd2e7848a5c04439e7c8d501cfd9c22ebe69a402654`
- **Repository commit measured against:**
  `a7a211ed3e755fc3c5bd090b6d8b9ffe3f221ed5`
- **Probe SHA-256, both worktree and commit `997c731b`:**
  `828ed22cfb58d088a2cf47c6f4deb23ea0a44ee1883f0b7455eddef83f9a0396`
- **Manifest set (unchanged GAP-46-02 Option A population):**
  - `runs/stage0-pilot-seed41/splits.json` —
    `c25568a18f3c4e31bcef5bf36f71591f0978edca4ca6cd490a28ec88ea276c86`
  - `runs/stage0-pilot-seed42/splits.json` —
    `5846ae5b55104e55a85d644875c3da187200c3d521f52a9298876d656c6d8903`
  - `runs/stage0-pilot-seed43/splits.json` —
    `a8618b0c6d0f0f1487fe4e3f8c0409a3e3398c7e8cb8bee2b4d3d7962a576172`
- **Blacklist SHA-256:**
  `238efd128cd04307708f74bbb54c23cad2cfec8b1cd6cfb09df62d830bae3e44`
- **Invocation (path-redacted, exactly as serialized by the probe):**

  ```text
  python -m pinn.verification.target_frame_probe \
    --manifest runs/stage0-pilot-seed41/splits.json \
    --manifest runs/stage0-pilot-seed42/splits.json \
    --manifest runs/stage0-pilot-seed43/splits.json \
    --blacklist-path problematic_ics_blacklist.json
  ```

- **Environment:** data-root source `git_common_dir_default`; torch `2.12.0`;
  resident dtype/device `float32`/`cpu`; probe mathematics `float64`;
  schema `phase46-target-frame/v1`.

## Symmetric hypothesis table (D-03)

| measure | scaled hypothesis | raw hypothesis | positive control | provenance control |
|---|---|---|---|---|
| position | `r_prime_as_resident` | `resident_over_D` | `preprocess_r_gauge` | `parsed_over_D` |
| time | `u_eq_t_over_T` | `u_eq_t_over_T` | `u_eq_t_parsed_over_T` | `u_eq_t_parsed_over_T` |
| velocity | `d2r_prime_du2_via_second_difference` | `d2r_prime_du2_via_second_difference` | `d2r_prime_du2_via_second_difference` | `d2r_prime_du2_via_second_difference` |
| masses | `ordered_raw_as_stored` | `ordered_raw_as_stored` | `preprocess_masses_ordered` | `parsed_file_order` |
| force softening | 1e-05 | 1e-05 | 1e-05 | 1e-05 |
| median of per-trajectory median residuals | 0.9893581923969974 | 0.0802249105713925 | 0.08022618097116868 | 0.08022618097116782 |
| max of per-trajectory max residuals | 1.0398406116001933 | 22.603496469372814 | 22.603484385047974 | 22.603484385047963 |
| trajectories consistent | 46 / 1651 | 1086 / 1651 | 1651 / 1651 | 1651 / 1651 |
| trajectories separated | 1605 / 1651 | 565 / 1651 | 0 / 1651 | 0 / 1651 |

The two controls reproduce the pre-repair run exactly, to their serialized
precision. The instrument and population did not move.

## Population and exclusion accounting

- **Rule:** A Stage-0 record is eligible iff its `RecordKey` appears in the
  train-or-validation view of every supplied manifest; test under any supplied
  manifest excludes it.
- **Eligible trajectories:** 1651
- **Per-manifest distribution:** seed 41 = 1473 train / 178 validation;
  seed 42 = 1459 / 192; seed 43 = 1464 / 187.
- **Population exclusions:** `test_under_splits` = 759,
  `test_under_splits~2` = 759, `test_under_splits~3` = 759. These overlap by
  construction.
- **Snapshot exclusions:** `endpoint` = 3302 under the shared qualifying mask.
- **Observed eligible surface:** all 1651 records are
  `variant=hierarchical, fidelity=base`, unchanged from the pre-repair run.

## Pre/post comparison

The table reports the exact serialized aggregate values from the 46-06 and
46-09 `raw.json` files.

| arm | measure | pre-repair 46-06 | post-repair 46-09 | movement |
|---|---|---:|---:|---:|
| scaled hypothesis | median residual | 0.9780023386528649 | 0.9893581923969974 | +0.0113558537441325 |
| scaled hypothesis | max residual | 1.0602956610091072 | 1.0398406116001933 | -0.0204550494089139 |
| scaled hypothesis | consistent | 47 | 46 | -1 |
| scaled hypothesis | separated | 1604 | 1605 | +1 |
| raw hypothesis | median residual | 1.347556618853727 | 0.0802249105713925 | -1.2673317082823345 |
| raw hypothesis | max residual | 52.409959695713795 | 22.603496469372814 | -29.80646322634098 |
| raw hypothesis | consistent | 0 | 1086 | +1086 |
| raw hypothesis | separated | 1651 | 565 | -1086 |
| positive control | median residual | 0.08022618097116868 | 0.08022618097116868 | 0 |
| positive control | max residual | 22.603484385047974 | 22.603484385047974 | 0 |
| positive control | consistent | 1651 | 1651 | 0 |
| positive control | separated | 0 | 0 | 0 |
| provenance control | median residual | 0.08022618097116782 | 0.08022618097116782 | 0 |
| provenance control | max residual | 22.603484385047963 | 22.603484385047963 | 0 |
| provenance control | consistent | 1651 | 1651 | 0 |
| provenance control | separated | 0 | 0 | 0 |

Three required confound measures:

| measure | pre-repair 46-06 | post-repair 46-09 | interpretation |
|---|---|---|---|
| `permutation_identity = false` | 1651 / 1651 | 1651 / 1651 | Unchanged because the probe tests whether `pre.permutation == [0,1,2]`, not whether resident bodies and masses are paired. |
| `first_diverging_step` | `com_recenter_boost`: 1651 / 1651 | `com_recenter_boost`: 1651 / 1651 | Unchanged because the probe returns the first earlier canonical intermediate from which the resident differs. An ordered resident necessarily differs from unpermuted `r_bar`, even when it exactly equals `r_bar_perm`. |
| corrected-raw consistency | 1100 / 1651 (66.6%) | 0 / 1651 (0%) | The unconditional inverse-permutation correction repaired the old mismatch but now introduces one. The uncorrected raw hypothesis moved from 0 to 1086 consistent. |

The direct repair discriminator did move: `plus_permutation` fell from
0.4663776457309723–3.686533808708191 before repair to exactly `0.0` for
1651/1651 after repair. This proves that the resident is exactly the
COM/boost-gauged, canonically ordered raw-scale intermediate the repair was
specified to expose.

## Confound register (D-04)

The serialized register still has 3302 entries: one `permutation` and one
`gauge_attribution` entry per trajectory. Post-repair these labels require the
algorithmic qualification above:

- `permutation_identity = false` for 1651/1651 records means all canonical
  permutations are nonidentity. It no longer indicates resident/mass
  mis-pairing; `plus_permutation = 0.0` for 1651/1651 is the pairing-status
  measurement.
- `first_diverging_step = com_recenter_boost` for 1651/1651 is produced by
  comparing the ordered resident to unpermuted `r_bar` first. It does not
  contradict the exact match to the next intermediate, `r_bar_perm`.
- `identity_raw = false`, `identity_scaled = false`, and
  `identity_neither = true` for 1651/1651. The resident is neither parsed
  file-order raw nor fully rotated/scaled; it is a third, deliberately exposed
  canonical intermediate.
- Restoring-permutation distribution is `[1,2,0]` for 1547 and `[0,2,1]` for
  104 trajectories, unchanged. Applying it to already ordered masses is the
  reason corrected-raw consistency falls to zero.

## Numerical tolerance derivation (D-06, GAP-46-03)

Quoted verbatim from `raw.json.tolerance_derivation`:

> numerical_tolerance = tolerance_floor + tolerance_fp32_increment, where
> tolerance_floor = max(positive_control_median_residual,
> provenance_control_median_residual) under the shared qualifying-snapshot mask
> and tolerance_fp32_increment = max(0.0, measured
> fp32-cast-then-float64-restored provenance-control median residual increase).
> No safety multiplier, population-fitted percentile, imported physics
> threshold, Phase 38 threshold, or theory-predicted ~21x / ~99x separation
> enters (GAP-46-03 Option A guardrails 1-3).

No physics acceptance threshold was used. The tolerance is solely a
representation/finite-difference comparison threshold.

## Branch: D-09 (owner decision required)

`decide_verdict` rule 5 returns `VERDICT_NON_FRAME_DIVERGENCE` because
`identity_neither` is unanimous and every record has a non-null stepwise
attribution. This is an explicit D-09 route in the unchanged instrument.

The verdict selects neither ratifiable pair:

- It does not establish parsed raw `r` with native `t`.
- It does not establish fully canonical scaled `r'` with normalized `u=t/T`.
- It does establish that residency now holds canonically ordered,
  COM/boost-gauged positions at raw dimensional scale, with paired ordered
  masses and without rotation or global scaling.

GAP-46-06 records the missing owner decision about whether to revise the
post-repair measurement contract, ratify an operational frame by instruction,
authorize another conformance transform, or defer. Plan 46-07, Phase 47, and
every frame-dependent successor remain blocked. No `RATIFIED_VALIDATION_FRAME`
was written, no probe parameter was changed, and no second measurement was
taken.

## GAP-46-01 consequence note

The post-repair verdict still selects neither historical reading from
GAP-46-01. `VERDICT_NON_FRAME_DIVERGENCE` is not a clean
`VERDICT_TARGETS_ARE_RAW` or `VERDICT_TARGETS_ARE_SCALED`; the repaired resident
is an ordered/gauged raw-scale intermediate that the current classifier
deliberately treats as neither identity. The future EVAL-01 obligation remains
locked and unchanged: a corrected conformant model must emit canonical `r'`
and the evaluator must pair it with `u=t/T`. What remains unresolved is the
historical diagnosis and the owner-authorized route from the repaired
intermediate to a ratified Phase 46 frame.

---

*Phase: 46-frame-resolution-gate-aligned-validation*  
*Plan: 46-09*  
*Verdict recorded: 2026-07-27*
