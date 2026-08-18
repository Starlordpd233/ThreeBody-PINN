# CONF-01 Target-Frame Verdict — Phase 46 Plan 06

**Machine verdict: `VERDICT_AMBIGUOUS`** — measured over **1651** eligible Stage-0
trajectories (the GAP-46-02 Option A conservative intersection of the three
retained pilot seed manifests). **Branch: D-09** — every frame-dependent piece
of work stops here; this is not the clean `VERDICT_TARGETS_ARE_SCALED` D-08
continuation.

The measurement leads; the source-code suspicion follows it. Before this run,
code inspection (`46-CONTEXT.md` D-04) suspected the resident target surface
might retain raw (unscaled) positions. The measured evidence below neither
confirms nor cleanly refutes that suspicion — it shows something more
specific: every one of the 1651 probed trajectories carries a body-order
permutation confound and a COM-recenter/boost gauge divergence between the
resident position array and its paired mass metadata, and that confound
prevents a unanimous verdict on the raw-vs-scaled question itself.

## Evidence citation

- **Run directory:** `.planning/phases/46-frame-resolution-gate-aligned-validation/evidence/target-frame/20260727T070221Z/`
  (`raw.json`, `summary.md`, both committed in `f106889b90b84dcc4889427a8e0272dc76f6e59b`)
- **raw.json SHA-256:** `3fa8251b464600fd2e99f5745bdfb1c315fb0073051de009d2b60a13a7dfcf08`
- **Repository commit measured against:** `7d9911ce83e674c0f2911157da5cd1eee914d770`
  (the probe reads `repo_commit` from `git rev-parse HEAD` at run time; this is
  the HEAD the probe actually ran against — the evidence-commit hash above is
  the *container* commit that later carried the artifact into history)
- **Manifest set with hashes (GAP-46-02 Option A — the sole legitimate
  population basis, quoted verbatim below):**
  - `runs/stage0-pilot-seed41/splits.json` — `c25568a18f3c4e31bcef5bf36f71591f0978edca4ca6cd490a28ec88ea276c86`
  - `runs/stage0-pilot-seed42/splits.json` — `5846ae5b55104e55a85d644875c3da187200c3d521f52a9298876d656c6d8903`
  - `runs/stage0-pilot-seed43/splits.json` — `a8618b0c6d0f0f1487fe4e3f8c0409a3e3398c7e8cb8bee2b4d3d7962a576172`
  - (`runs/stage0-smoke/splits.json` is byte-identical to seed-42 and is
    correctly omitted — it adds no independent exclusion constraint)
- **Population-decision provenance (46-GAPS.md § GAP-46-02, Status
  RESOLVED-WITH-INSTRUCTION, quoted verbatim):**

  > User instruction 2026-07-26 explicitly delegated the option selection to
  > Codex. **Option A — conservative intersection across the three retained
  > pilot manifests** ... An identity is eligible only when it is Stage 0 and
  > train-or-validation under **all three** pilot manifests; test under **any
  > one** excludes it. Direct manifest arithmetic records 2,265 Stage-0
  > physical identities, 2,039 non-test identities per individual seed, and a
  > 1,651-identity all-three intersection — 388 (19.0%) fewer than one seed's
  > train+validation view.

  This plan used exactly that basis; the measured `eligible_count = 1651`
  matches the resolution note's arithmetic exactly.
- **Blacklist:** `simulation_data/Documentation/problematic_ics_blacklist.json`
  (the retained pilot's own `data.blacklist_path` value, resolved against the
  resolved data root per `pinn/training/config.py`) — SHA-256
  `238efd128cd04307708f74bbb54c23cad2cfec8b1cd6cfb09df62d830bae3e44`
- **Invocation (path-redacted, exactly as recorded in the Task 2 commit):**
  ```
  python -m pinn.verification.target_frame_probe \
    --manifest runs/stage0-pilot-seed41/splits.json \
    --manifest runs/stage0-pilot-seed42/splits.json \
    --manifest runs/stage0-pilot-seed43/splits.json \
    --blacklist-path problematic_ics_blacklist.json
  ```
- **Environment:** interpreter resolved as `$(dirname "$(git rev-parse
  --git-common-dir)")/.venv/bin/python` (torch 2.12.0, numpy 2.2.0 — matches
  the 46-01 SUMMARY's recorded interpreter and versions exactly); probe
  arithmetic performed in `float64`; resident dtype/device `float32`/`cpu`.

## Symmetric hypothesis table (D-03)

Every arm's coordinate tuple, exactly as recorded in `raw.json`'s `arms` block
and rendered by the CLI's own `summary.md`:

| measure | scaled hypothesis | raw hypothesis | positive control | provenance control |
|---|---|---|---|---|
| position | `r_prime_as_resident` | `resident_over_D` | `preprocess_r_gauge` | `parsed_over_D` |
| time | `u_eq_t_over_T` | `u_eq_t_over_T` | `u_eq_t_parsed_over_T` | `u_eq_t_parsed_over_T` |
| velocity | `d2r_prime_du2_via_second_difference` (all arms; second-difference acceleration, not first-difference velocity) |
| masses | `ordered_raw_as_stored` | `ordered_raw_as_stored` | `preprocess_masses_ordered` | `parsed_file_order` |
| force softening | 1e-05 | 1e-05 | 1e-05 | 1e-05 |
| median of per-trajectory median residuals | 0.978002 | 1.34756 | 0.0802262 | 0.0802262 |
| max of per-trajectory max residuals | 1.0603 | 52.41 | 22.6035 | 22.6035 |
| trajectories consistent (residual ≤ tolerance) | 47 / 1651 | 0 / 1651 | 1651 / 1651 | 1651 / 1651 |
| trajectories separated (own residual > tolerance) | 1604 / 1651 | 1651 / 1651 | 0 / 1651 | 0 / 1651 |

The two controls (positive: fully preprocessed ordered/gauged/scaled
trajectory; provenance: parsed raw positions with matching raw metadata) are
both fully self-consistent (1651/1651), as expected of a control — this is
not new information, it verifies the probe's own measurement apparatus is
sound. Neither hypothesis arm achieves unanimous consistency across the
population.

## Population and exclusion accounting

- **Rule (module constant `POPULATION_RULE`, quoted verbatim):** "A Stage-0
  record is eligible iff its RecordKey appears in the train-or-validation view
  of EVERY supplied manifest; a record whose physical key is in ANY supplied
  manifest's test partition is excluded, with the exclusion counted and
  attributed as test_under_<label>."
- **Eligible trajectories:** 1651
- **Per-manifest per-split distribution of the 1651 eligible identities**
  (a given identity can carry a different train/validation label under each
  manifest; the rule only requires it be non-test under all three):
  - `splits` (seed41): train 1473, validation 178 (sums to 1651)
  - `splits~2` (seed42): train 1459, validation 192 (sums to 1651)
  - `splits~3` (seed43): train 1464, validation 187 (sums to 1651)
- **Population-level exclusions (test-under-any-manifest):**
  `test_under_splits` = 759, `test_under_splits~2` = 759,
  `test_under_splits~3` = 759 (these counts overlap across manifests by
  construction; they are not additively disjoint)
- **Snapshot-level exclusions (shared qualifying mask across all arms):**
  `endpoint` = 3302 (finite-difference edge snapshots, excluded from every arm
  identically so no arm gets a favorable mask)
- **Measured fact not previously recorded anywhere in Phase 46 artifacts:**
  all 1651 eligible identities are `variant=hierarchical, fidelity=base`. No
  `standard` or `gold_standard` identity survives the three-manifold
  intersection at Stage 0. This is reported as a measured population fact; it
  is not interpreted as a defect or an intended design property in this
  document — the two candidate readings (a genuine Stage-0 curriculum
  restriction, or a Stage-0-labeling artifact) are both plausible and neither
  is decidable from this evidence alone.

## Confound register (D-04)

The full confound register (`raw.json.confound_register`, 3302 entries, 2 per
trajectory) covers **every one of the 1651 eligible trajectories** — there is
no confound-free subset:

- **Body-permutation prevalence: 1651 / 1651 (100%).** Every trajectory's
  `permutation_identity` is `false` — the mass vector paired with the resident
  positions is NOT in the same body order as the positions themselves.
  Measured permutation distribution: `(2, 0, 1)` for 1547 trajectories,
  `(0, 2, 1)` for 104 trajectories. Zero trajectories show the identity
  permutation `(0, 1, 2)`.
- **Mass-pairing confound: 0 / 1651.** `mass_convention = "ordered"` for every
  trajectory (the stored masses are the canonically-ordered
  `preprocess.masses_ordered` convention, not file-order) — this is not itself
  a mismatch; it is the permutation applied specifically to masses-vs-positions
  (the row above) that is the confound, consistent with the pre-existing
  code-inspection observation in `46-CONTEXT.md` D-04 (adapter residency
  retains `parsed_brutus.positions` while pairing them with
  `pre.masses_ordered`).
- **COM/gauge attribution: 1651 / 1651 (100%).** Every trajectory's
  `first_diverging_step` is `com_recenter_boost` — the first processing step
  at which the resident trajectory diverges from the canonical
  ordered/gauged/scaled pipeline is COM re-centering plus boost removal, for
  every single eligible trajectory, with no exception.
- **Identity classification (train-free, per D-01's exact resident surface):**
  `identity_raw = true` for 1651 / 1651; `identity_scaled = false` for
  1651 / 1651; `identity_neither = false` for 1651 / 1651. Structurally, every
  probed identity classifies as "raw-shaped" rather than "scaled-shaped," but
  **after correcting for the measured permutation confound**, the raw
  residual clears the numerical tolerance for only 1100 / 1651 (66.6%) of
  trajectories — short of the unanimity `decide_verdict` rule 4 requires for a
  clean `VERDICT_TARGETS_ARE_RAW`. This is the specific reason the verdict
  falls through to the rule-6 fail-closed catch-all (`VERDICT_AMBIGUOUS`)
  rather than resolving cleanly to either D-08 or the raw branch of D-09:
  100% permutation + COM/boost confound prevalence pushes 33.4% of
  corrected-raw residuals over the numerical tolerance, which is not the same
  question as which frame the targets are stored in.

## Numerical tolerance derivation (D-06, GAP-46-03)

Quoted verbatim from `raw.json.tolerance_derivation`:

> numerical_tolerance = tolerance_floor + tolerance_fp32_increment, where
> tolerance_floor = max(positive_control_median_residual,
> provenance_control_median_residual) under the shared qualifying-snapshot
> mask and tolerance_fp32_increment = max(0.0, measured
> fp32-cast-then-float64-restored provenance-control median residual
> increase). No safety multiplier, population-fitted percentile, imported
> physics threshold, Phase 38 threshold, or theory-predicted ~21x / ~99x
> separation enters (GAP-46-03 Option A guardrails 1-3).

**Separately, and explicitly:** no physics acceptance threshold was applied at
any point in this measurement. The tolerance above answers only whether two
measurements agree within the numerical resolution of the finite-difference
operator and the represented dtype (fp32 round-trip term). It is not a
physics-acceptance, target-quality, Hamiltonian, or training threshold
(D-06, GAP-46-03 guardrail 4). The raw-vs-scaled theoretical separation
(~21x / ~99x, from the 46-01 SUMMARY's closed-form Lagrange-equilateral
derivation) appears only as a `role: descriptive_diagnostic` field in
`raw.json.aggregates` and was never promoted into the tolerance or the
verdict logic.

## Branch: D-09 (owner scope decision required)

The machine verdict is `VERDICT_AMBIGUOUS`, not `VERDICT_TARGETS_ARE_SCALED`
with an empty confound register. Per D-09, this is recorded as an unresolved
ambiguity (not a confirmed defect and not a confirmed-conformant frame) and
all frame-dependent work — Plan 46-07 (INST-01 production wiring) and Phase 47
(the target-frame repair phase) — stops here. No `46-GAPS.md` entry and no
`.planning/milestones/v2.2-GAPS.md` entry were written by this executor; per
the plan's explicit prohibition, gap-register writes are orchestrator-owned.
The full STOP-protocol block is returned in this plan's completion message
under the heading `## CONF-01 BRANCH: OWNER SCOPE DECISION REQUIRED`.

No repair, correction, or "for clarity" rewrite was made to any file under
`pinn/` in producing this verdict (verified: `git status --short -- pinn/`
shows no change from this plan).

## GAP-46-01 consequence note

GAP-46-01 (RESOLVED-WITH-INSTRUCTION 2026-07-26) conditions the held-out
evaluator's position/time pairing on CONF-01's own verdict, offering two
readings: (i) if CONF-01 finds targets are the locked `r'`, the historical
`evaluate.py` raw-time pairing was incoherent; (ii) if CONF-01 finds targets
are raw `r`, that pairing was historically coherent but the defect moves to
the training targets instead.

**The measured verdict here selects neither reading cleanly.** It is not
`VERDICT_TARGETS_ARE_SCALED`, so reading (i) is not selected. It is also not
a clean `VERDICT_TARGETS_ARE_RAW` (rule 4 requires unanimous corrected-raw
consistency across all 1651 trajectories; only 1100/1651 = 66.6% clear
tolerance), so reading (ii) is not cleanly selected either — though the
underlying identity classification (`identity_raw = true` for 100% of
trajectories, `identity_scaled = false` for 100%) is structurally much
closer to reading (ii)'s premise than to reading (i)'s. This is recorded here
as information for Phase 50/51 planning, which owns GAP-46-01's resolution
before any held-out evaluator access; it does not resolve GAP-46-01, and no
change was made to `pinn/evaluate.py` or any evaluator path by this plan
(D-16 unaffected).

---

*Phase: 46-frame-resolution-gate-aligned-validation*
*Plan: 46-06*
*Verdict recorded: 2026-07-27*
