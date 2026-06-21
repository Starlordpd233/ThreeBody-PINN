# Phase 33 Gap Register

STOP-protocol gaps surfaced during Phase 33 (Curriculum-Stage Contracts).
Milestone index: `.planning/milestones/v1.6-GAPS.md`.

---

## GAP-33-01 - Adaptive population safeguard owner policy

- **Decision point:** Should Phase 33 lock the roadmap/requirements
  `>10%` per-stage population safeguard as a curriculum-stage contract, or
  treat the safeguard value and stage-mapping policy as an unresolved owner
  decision that must be settled after admitted-set EDA?
- **Where in artifact:** `.planning/ROADMAP.md` Phase 33 success criterion 1
  (line 170); `.planning/REQUIREMENTS.md` `CURR-01` (line 41).
- **Task context:** `$gsd-spec-phase 33 --auto` requirements gathering before
  writing `33-SPEC.md`.
- **Classification:** **semantic** - the selected population safeguard changes
  stage-label policy, underpopulated-cluster merging, and the admissible
  Stage 0-6 inventory.
- **Source silence:** `.planning/ROADMAP.md:170` and
  `.planning/REQUIREMENTS.md:41` state a `>10%` safeguard as if locked. The
  Phase 31 readiness report routes the "5% vs >10%" safeguard to Phase 33 for
  owner policy after admitted-set EDA (`31-READINESS-REPORT.md:217-220`). The
  candidate resolution doc permits offline EDA/clustering but says "the 5%
  versus >10% population safeguard is surfaced to the owner" and that
  `CLM-02..07` remain unverified (`03-final-resolution.md:80-82`);
  its evidence table marks `ADAPT-04` as `surface_to_user` and `ADAPT-07` as
  `defer` (`03-final-resolution.md:162-168`), and its gap list records
  `GAP-15` as owner-selected after admitted-set EDA (`03-final-resolution.md:233`).
- **Mathematical / engineering grounding:** PCA + clustering assigns a finite
  admitted trajectory set into curriculum buckets. A 5% floor, a `>10%` floor,
  and an EDA-selected floor are not equivalent: they produce different merge
  operations for sparse clusters, change the stage distribution seen by replay
  and transition gates, and can erase or preserve rare but important
  near-collision / chaotic regimes. Without the admitted-set distribution, the
  threshold is a policy choice rather than a derivable constant.
- **Agent was tempted to:** carry forward `>10%` because it appears in
  `CURR-01` and the Phase 33 roadmap. That would silently convert a
  source-marked owner decision into a locked contract.
- **What the user needs to decide:**
  - **A.** Lock the `>10%` per-stage safeguard now for Phase 33.
  - **B.** Keep Phase 33 packet-first: specify offline EDA + stable labels, but
    require an explicit owner decision before locking the population floor.
  - **C.** Select a different safeguard policy now (for example 5%, adaptive by
    admitted-set size, or another named rule).
- **Confidence of impact:** **HIGH** - this policy can change stage labels and
  therefore affects `CURR-01`, `CURR-04`, and Phase 36 acceptance evidence.
- **Status:** **OPEN**
- **Resolution note:**

---

## GAP-33-02 - tau_L estimator, time units, and shortcut policy

- **Decision point:** Should Phase 33 lock the roadmap/requirements
  shadow-trajectory `tau_L = 1/lambda_max` method, the
  `epsilon_pert = 1e-8` / `epsilon_soft = 1e-10` split, and the fast
  PCA+Rosenstein batch approximation, or should it preserve the current
  Rosenstein-style baseline until the owner selects the estimator, units, fit
  parameters, uncertainty flags, and threshold calibration?
- **Where in artifact:** `.planning/ROADMAP.md` Phase 33 success criterion 2
  (line 171); `.planning/REQUIREMENTS.md` `CURR-02` (line 42).
- **Task context:** `$gsd-spec-phase 33 --auto` requirements gathering before
  writing `33-SPEC.md`.
- **Classification:** **semantic** - the estimator and time-unit convention
  determine `tau_L` values, stage thresholds, and whether thresholds can be
  compared across datasets and trajectory lengths.
- **Source silence:** `.planning/ROADMAP.md:171` and
  `.planning/REQUIREMENTS.md:42` state a shadow-trajectory method and
  PCA+Rosenstein approximation as if locked. Phase 31 routes the
  Rosenstein-vs-shadow/Benettin and time-unit issue to Phase 32 EVID-15 plus
  Phase 33 owner decision (`31-READINESS-REPORT.md:207-213`). The Phase 32
  ledger says the `L_max / tau_L` row is still Phase 33-owned and must get an
  evidence packet before spec edits (`32-ISSUE-LEDGER.md:29-36`,
  `32-ISSUE-LEDGER.md:65-71`). The candidate resolution doc says the
  canonical `tau_L` estimator remains unresolved, the owner must select the
  method and time-unit convention, Rosenstein remains the current revisable
  baseline, and the issue shadow code plus unspecified PCA shortcut must not be
  adopted normatively (`03-final-resolution.md:88-90`);
  it records `TAUL-01` as `surface_to_user`, `TAUL-03` as `defer`, and the
  PCA shortcut as rejected/source-silent (`03-final-resolution.md:173-179`);
  its gap list records `GAP-18` for method/units/calibration
  (`03-final-resolution.md:236`).
- **Mathematical / engineering grounding:** Rosenstein-style finite-time
  divergence estimation and shadow/Benettin integration estimate related but
  operationally different quantities. Time-axis normalization, fitting window,
  perturbation size, potential softening, and uncertainty handling all change
  the numeric `lambda_max` and therefore `tau_L = 1/lambda_max`. Because Phase
  33 stage thresholds use `tau_L`, locking a method also locks the scale of
  Stage 4/5/chaotic gates.
- **Agent was tempted to:** write `CURR-02` exactly as the roadmap phrases it,
  using shadow trajectories and PCA+Rosenstein. That would contradict the
  candidate resolution doc's explicit "do not normatively adopt" warning.
- **What the user needs to decide:**
  - **A.** Lock the roadmap's shadow-trajectory plus PCA+Rosenstein contract
    now, overriding the resolution-doc deferral.
  - **B.** Keep Phase 33 packet-first: retain the current Rosenstein-style
    baseline as revisable and require owner selection before final `tau_L`
    thresholds are locked.
  - **C.** Select a specific estimator/time-unit contract now (including fit
    window, perturbation, softening context, uncertainty flags, and calibration
    responsibility).
- **Confidence of impact:** **HIGH** - the choice affects `CURR-02`, `CURR-04`,
  stage thresholds, and Phase 36 numeric acceptance probes.
- **Status:** **OPEN**
- **Resolution note:**

---

## GAP-33-03 - L_norm clamp and metadata storage contract

- **Decision point:** Should Phase 33 lock the roadmap/requirements
  `np.clip(L_norm, 0, 1)` guard as a stage-gating contract, preserve raw
  `L_norm` metadata only, store both raw and derived-clipped values, or adopt a
  global clamp policy?
- **Where in artifact:** `.planning/ROADMAP.md` Phase 33 success criterion 4
  (line 173); `.planning/REQUIREMENTS.md` `CURR-04` (line 44).
- **Task context:** `$gsd-spec-phase 33 --auto` requirements gathering before
  writing `33-SPEC.md`.
- **Classification:** **semantic** - raw vs clipped angular-momentum metadata
  changes recorded invariants, stage-gate behavior, and downstream diagnostics.
- **Source silence:** `.planning/ROADMAP.md:173` and
  `.planning/REQUIREMENTS.md:44` state the M6 `np.clip(L_norm, 0, 1)` guard as
  part of the Stage 0-6 gating contract. Phase 31 marks raw-vs-clipped
  metadata as deferred and says the owner selects the storage contract
  (`31-READINESS-REPORT.md:217-220`). The Phase 32 ledger still has M6 as a
  Phase 33-owned row requiring an evidence packet before spec edits
  (`32-ISSUE-LEDGER.md:65-67`). The candidate resolution doc rejects the old
  "clamp before IC mapping" rationale, says no global clamp is authorized,
  preserves the current unclipped baseline until the owner selects raw-only,
  raw-plus-derived-clipped, or global-clipped storage, and requires explicit
  nonfinite / near-degenerate `L_max` handling (`03-final-resolution.md:44-46`);
  it records `M6-02` as `surface_to_user`, `M6-03` as `defer`, and DGR-07 as a
  deferred storage-policy disagreement (`03-final-resolution.md:129-131`,
  `03-final-resolution.md:196`); its gap list records `GAP-07` as unresolved
  (`03-final-resolution.md:225`).
- **Mathematical / engineering grounding:** `L_norm = L / L_max` can exceed 1
  when the characteristic scale is not a true maximum or when numerical /
  degenerate cases make `L_max` small. Raw storage preserves diagnostic truth,
  while clipping produces a bounded value suitable for thresholding but hides
  overshoot magnitude. A raw-plus-derived-clipped contract keeps both signals;
  a global clamp discards overshoot information and can mask formula or data
  issues. The choice changes what Stage 0-6 gates read and what downstream
  acceptance probes can verify.
- **Agent was tempted to:** lock a derived `np.clip(L_norm, 0, 1)` stage-gate
  value because the roadmap names it and bounded gates are operationally tidy.
  That would still choose between raw-only, raw-plus-derived, and global-clamp
  policies where the sources require owner selection.
- **What the user needs to decide:**
  - **A.** Store raw `L_norm` and use an explicit derived clipped value only for
    stage gating, with nonfinite / near-degenerate `L_max` handling specified.
  - **B.** Preserve raw-only metadata and avoid a clipped stage-gate contract
    until admitted-set evidence supports it.
  - **C.** Apply a global clipped `L_norm` storage policy.
- **Confidence of impact:** **HIGH** - this affects `CURR-04`, stage assignment,
  metadata semantics, and Phase 36 acceptance probes.
- **Status:** **OPEN**
- **Resolution note:**

---

*Phase: 33-curriculum-stage-contracts*
*Register opened: 2026-06-21*
