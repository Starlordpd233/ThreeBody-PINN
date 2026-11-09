---
phase: 67
phase_name: "Design & Settings Ladders"
project: "Three-Body Physics-Informed LLM"
generated: "2026-11-08"
counts:
  decisions: 8
  lessons: 6
  patterns: 6
  surprises: 5
missing_artifacts:
  - "67-UAT.md"
---

# Phase 67 Learnings: Design & Settings Ladders

Phase 67 built the multi-experiment ladder harness (`pinn/verification/diagnostic_phase67*.py`) pinned by a 41-file freeze manifest and executed four one-factor-at-a-time ladders (`EXP-02` depth `2/4/6/8/12`, `EXP-03` learning rate `1e-3/3e-4/1e-4/3e-5/1e-5`, `EXP-04` raw vs orbit-scaled Fourier time inputs on both `locked-12` and `exp01` backbones, and `EXP-05` exact signed-lap windows `1/2/5/10` inner laps) across the three Stage-0 cases (`main-1632-s42`, `repeat-851-s42`, `repeat-1632-s41`) — totaling 4 guarded metadata captures, 60 blind timing rows, and 60 single-look science rows (`28.30 hours` combined wall). `EXP-03` produced a confirmation-grade `REFUTED-LEAD`: `lr = 1e-3` (the v2.4 learning rate) was confirmed-worsening across all three cases (`E = 1.4552, 1.2422, 1.1583`, all settled Tier 0), while the **locked `12×256` control at `lr = 1e-4` reached settled Tier 1 on all three cases** (`E = 0.04069, 0.09550, 0.03492`). Following the owner's `67-EXP03-RULING.md` (`proceed with option 1`), `EXP-04` and `EXP-05` completed on their registered unsettled-continue routes, and `67-16` closed the phase with `PHASE67-AUDIT-OK`. Extracted from `67-01..16-PLAN.md`, `67-01..16-SUMMARY.md`, `67-EXP02..05-PREDICTION.md`, `67-EXP02..05-RESULT.md`, `67-EXP03-RULING.md`, `67-FINDINGS.md`, `67-VALIDATION.md`, `67-VERIFICATION.md`, and `STATE.md`. No UAT file exists for this phase.

## Decisions

### Pin a 41-file harness freeze manifest (`evidence/harness-freeze.json`) before registering any Phase 67 experiment
Plan 67-07 froze all 13 diagnostic modules, the frozen scorer/scorecard/protocol, production locks, retained normalizers, and historical Phase 65/66 evidence artifacts in `evidence/harness-freeze.json` (`verify_harness_freeze`) before any `EXP-02..05` timing or science registration was created.

**Rationale:** prevents mid-experiment code drift across 120 timing and science launches while keeping a single auditable manifest for any defect-repair re-pin.
**Source:** 67-07-SUMMARY.md, STATE.md (Decisions from 67-07)

### Size each experiment's common step budget `N` purely from its own worst-case timing row
`phase67_budget` computes a single common step count `N` (in 100-step quanta, `warmup = 200`) for all rows of an experiment such that the slowest row in the experiment's complete timing matrix fits within `0.75 × 3,540 s = 2,655 s` (`N = 152,900` for `EXP-02`, `155,100` for `EXP-03`, `112,700` for `EXP-04`, `148,700` for `EXP-05`), without reading any timing score or borrowing rates across experiments.

**Rationale:** holding `N` constant across all arms and cases within an experiment eliminates step-budget confounding while guaranteeing every arm respects the 59-minute supervised cap.
**Source:** 67-04-SUMMARY.md, 67-08-SUMMARY.md, 67-10-SUMMARY.md, 67-12-SUMMARY.md, 67-14-SUMMARY.md

### Require 5% final-quarter relative `E` settlement (`(E_3N/4 - E_N) / E_3N/4 <= 0.05`) on all six paired endpoints for confirmation
`phase67_improvement_check` marks an endpoint `unsettled` if `E` improves by strictly more than `5%` between step `3N/4` and `N`. `phase67_contrast` confirms an arm as `confirmed-improving` or `confirmed-worsening` only when all three cases (`1632/s42`, `851/s42`, `1632/s41`) agree in direction, each qualifies by a tier change or `>= 20%` relative `E` effect, and all six paired arm/control endpoints are settled and mechanically clean.

**Rationale:** prevents declaring a factor confirmed when either the treatment arm or the control baseline is still actively descending at the end of the finite budget.
**Source:** 67-05-SUMMARY.md, STATE.md (Decisions from 67-05)

### Resolve the `EXP-03` `REFUTED-LEAD` branch via a digest-bound owner ruling (`67-EXP03-RULING.md`)
When `EXP-03` confirmed `lr1e-3` as worsening (`scope49_disposition = proposal-pending`, `dependent_launch_allowed = false`), execution halted before `EXP-04` and surfaced the reserved decision to the owner. The owner's verbatim reply `"proceed with option 1"` (`authorize-recorded-proposal`) was committed in `67-EXP03-RULING.md` (`eab52f7d`), unblocking `EXP-04` under its existing registration.

**Rationale:** under `SCOPE-49`, a confirmed refutation of a registered hypothesis requires explicit owner authorization before spending compute on dependent experiments.
**Source:** 67-11-SUMMARY.md, 67-EXP03-RULING.md, STATE.md (Decisions from 67-11)

### Define `EXP-05` lap windows as exact first-crossing gold sample prefixes with global `T` normalization preserved
`first_lap_prefixes` accumulates signed `atan2` turns about the initial inner-binary orbit normal from `t = 0` and selects the earliest existing gold timestamp reaching `1, 2, 5, 10` cumulative signed turns, keeping the exact `physical_window` sample prefix and the global `T_CHARACTERISTIC_TIME` normalization (`tau = 2*(t/T) - 1`) without interpolation or `tau` rescaling.

**Rationale:** rescaling `tau` to `[-1, 1]` on a short window would change the effective frequency of every SIREN layer (`first_omega_0`), confounding window length with frequency scaling (`D-06`).
**Source:** 67-03-SUMMARY.md, 67-14-SUMMARY.md, STATE.md (Decisions from 67-03, 67-14)

### Cross-check same-window constant and two-Kepler baselines on every prefix before scoring
`same_window_expectations` computes the window-mean constant and frozen `two_kepler_prediction` baselines on the exact retained sample grid for each window prefix and cross-checks them against `_comparison_rows` to within `rtol = 1e-8, atol = 1e-10`.

**Rationale:** `E` is normalized by reference scale on the scored window, so short-window fits must be compared against baselines evaluated on that exact prefix rather than the full `[0, 10]` horizon.
**Source:** 67-03-SUMMARY.md, STATE.md (Decisions from 67-03)

### Repair harness reader/materialization defects under the freeze re-pin protocol without touching evidence bytes
When Plan 67-12 hit two reader false-refusals (as-captured registration citation after a freeze re-pin, and static arm lookup on `851`'s orbit-specific Fourier frequencies) and Plan 67-14 hit lazy variant materialization in spawned subprocesses, the fixes landed with regression tests and updated `harness-freeze.json` plus unlaunched registrations while keeping all already-captured evidence bytes untouched.

**Rationale:** separates harness-code bug fixes from scientific evidence integrity; historical runs remain verifiable against their as-captured publication commits.
**Source:** 67-12-SUMMARY.md, 67-14-SUMMARY.md, STATE.md (Decisions from 67-12, 67-14)

### Recover completed on-disk attempts read-only after session interruption instead of relaunching
During Plan 67-11 overnight execution, the predecessor session hit a usage cap after row 5 (`main-1632-s42/lr1e-5`) had finished and published on disk. The continuation session verified row 5 read-only (`PHASE67-ROW-OK`) and committed its four artifacts directly without re-running.

**Rationale:** the single-look no-retry contract forbids re-running a completed attempt; verifying and committing the finished on-disk record preserves exact single-use provenance.
**Source:** 67-11-SUMMARY.md, STATE.md (Decisions from 67-11)

---

## Lessons

### The v2.4 `1e-3` learning rate — not the 12-layer SIREN architecture — caused the single-orbit time-constant collapse
In `EXP-03`, the locked `12×256` (`first_omega_0 = 30`) network at `lr = 1e-3` collapsed to settled Tier-0 constant-like predictions on all three cases (`E = 1.4552, 1.2422, 1.1583`), reproducing the v2.4 failure mode, whereas the exact same `12×256` network at `lr = 1e-4` achieved **settled Tier 1 on all three cases** (`E = 0.04069` on `1632/s42`, `0.09550` on `851/s42`, `0.03492` on `1632/s41`).

**Context:** the headline root-cause result of Milestone v2.5 (`EXP-03` in `67-EXP03-RESULT.md` and `67-FINDINGS.md`).
**Source:** 67-11-SUMMARY.md, 67-EXP03-RESULT.md, 67-FINDINGS.md, 67-VERIFICATION.md

### Unsettled control endpoints at finite budget block confirmation even when directional effects are large
In `EXP-02`, `d8` achieved lower `E` than `d12` on all three cases (`0.02581` vs `0.02689` on `1632/s42`, `0.06808` vs `0.10722` on `851/s42`, `0.01097` vs `0.03651` on `1632/s41`), and in `EXP-05`, shorter lap windows (`lap1`, `lap2`, `lap5`) beat `lap10` on all 9 case-contrast cells (`relative_E_effect = 0.14..0.88`). Yet both ladders read `unsettled` because `d12` / `lap10` on `1632/s42` improved by more than `5%` in the final quarter (`3N/4 -> N`).

**Context:** reviewing `EXP-02`, `EXP-04`, and `EXP-05` under the prospective 5% final-quarter settlement rule.
**Source:** 67-09-SUMMARY.md, 67-13-SUMMARY.md, 67-15-SUMMARY.md, 67-FINDINGS.md

### Spawned worker subprocesses do not inherit in-memory dynamic variant registrations
In Plan 67-14 (`EXP-05`), dynamic lap-window variants (`exp05-lap1..lap10`) were materialized in the parent process, but `diagnostic_fit.py` spawns a fresh Python interpreter that re-runs `validate_smoke_settings` in a clean process where those variants were not yet registered, causing a pre-attempt refusal. Moving materialization into a lazy hook inside `validate_smoke_settings` fixed the cross-process boundary cleanly.

**Context:** fixing the `EXP-05` subprocess settings-gate refusal in Plan 67-14 (`54d3cb40`, `bbf492d4`).
**Source:** 67-14-SUMMARY.md, STATE.md (Decisions from 67-14)

### Static arm lookup tables fail when variant declarations are orbit-specific
In `EXP-04`, the harmonic frequencies (`f = N_in / T`) depend on the target orbit (`1632` vs `851`), so `851` uses orbit-specific variant names (`*-851`). `check-matrix` initially looked up arms in a static `1632`-keyed table and refused the `851` rows until updated to resolve through `phase67_arm_variant(experiment, arm, orbit=orbit_key)` (`4ea20b05`).

**Context:** registering and checking the 18-row `EXP-04` timing matrix in Plan 67-12.
**Source:** 67-12-SUMMARY.md, STATE.md (Decisions from 67-12)

### Principal `atan2` step checks alone cannot detect `> π` phase-wrapping aliasing
Because `atan2(sin, cos)` always returns values in `(-π, π]`, an actual angular step larger than `π` wraps into a small apparent step. The `EXP-05` census aliasing guard therefore checks both the principal `atan2` increment and the trapezoid-integrated local angular rate `(r × v) / |r|²` against `π`.

**Context:** implementing `first_lap_prefixes` and the aliasing guard in Plan 67-03.
**Source:** 67-03-SUMMARY.md, STATE.md (Decisions from 67-03)

### Per-launch `caffeinate` inside the process group protects runs even if a session-level wake lock is killed
During the 8-hour `EXP-05` science batch (`67-15`), an outer session-level `caffeinate` process was terminated seven times between rows, but each in-flight launch's own process-group `caffeinate` child (`diagnostic_power.py`) held uninterrupted, so zero runs were lost or slept.

**Context:** running the 12-row `EXP-05` science matrix overnight in Plan 67-15.
**Source:** 67-15-SUMMARY.md, STATE.md (Decisions from 67-15)

---

## Patterns

### Thirteen-command state-machine CLI enforcing strict artifact-order gates
Structure a multi-experiment phase around a single CLI (`prepare-design -> check-design -> capture-metadata -> check-metadata -> register-timing -> check-matrix -> launch-row -> check-row -> budget -> check-budget -> review -> check-review -> audit-phase`) where each command refuses with exit code 2 before creating any file if its upstream prerequisite commit or artifact is missing.

**When to use:** large experimental matrices (120+ runs) that must maintain pre-registration, blind timing, and single-look review discipline across multiple sessions.
**Source:** 67-06-SUMMARY.md, STATE.md (Decisions from 67-06)

### Process-group supervisor (`start_new_session` + `SIGTERM`/`SIGKILL` group sweep)
Run every timed subprocess in its own process group under a monotonic deadline starting before admission; on timeout, send `SIGTERM` then `SIGKILL` to the entire process group, verify via `ps -g` that zero descendants survive, and mark `attempt.json` as `incomplete` (`wall_cap_expired`) with no retry.

**When to use:** bounding wall-clock execution of GPU/MPS training workers and their `caffeinate` children.
**Source:** 67-06-SUMMARY.md, STATE.md (Decisions from 67-06)

### DST-aware remaining-window admission (`closing_utc - checked_utc >= cap_seconds`)
Compute the window closing instant (`Sunday 22:00 America/Chicago` or an owner-amended cutoff) in wall-clock local time via `ZoneInfo`, convert both `checked_utc` and `closing_utc` to aware UTC instants, and require `closing_utc - checked_utc >= cap_seconds` before admitting a launch.

**When to use:** enforcing calendar execution windows across Daylight Saving Time transitions (such as the 2026-11-01 CST transition).
**Source:** 67-06-SUMMARY.md, STATE.md (Decisions from 67-06)

### Disjoint in-loop event timing (`timing.events` ledger for logging, scoring, and publication I/O)
Time each similarity-logging call (`5` events at `0, N/4, N/2, 3N/4, N`) and frozen-scoring call (`3` events at `N/2, 3N/4, N`, reusing step `N` as the final network score without a fourth call) as disjoint synchronized intervals inside the training loop, and verify that their sum plus update steps sits below total loop wall time.

**When to use:** attributing wall-clock cost accurately between optimizer updates and periodic diagnostic instrumentation.
**Source:** 67-04-SUMMARY.md, STATE.md (Decisions from 67-04)

### As-captured publication-commit registration verification
When a harness bug fix requires re-pinning `harness-freeze.json` and unlaunched registrations mid-phase, verify already-published run records against the registration blob committed at the record's own history ancestor rather than current working-tree bytes.

**When to use:** maintaining immutable verification of earlier experiment rows after fixing a harness defect for later rows.
**Source:** 67-12-SUMMARY.md, STATE.md (Decisions from 67-12)

### Byte-exact canonical JSON embedding in markdown result pages
Require `67-EXP0X-RESULT.md` to embed the exact `json.dumps(review, indent=2, sort_keys=True)` string of `review.json` inside a fenced block, verified by `check-review` (`PHASE67-REVIEW-ARTIFACTS-OK`).

**When to use:** guaranteeing that human-readable result pages cannot drift from machine-computed review verdicts.
**Source:** 67-09-SUMMARY.md, STATE.md (Decisions from 67-09)

---

## Surprises

### The locked `12×256` network (`first_omega_0 = 30`, raw `[tau, IC13]`) reached settled Tier 1 on all three cases simply by lowering `lr` from `1e-3` to `1e-4`
Without changing depth, width, `first_omega_0`, input features, or window length, the locked production architecture achieved settled Tier-1 position fits across the main orbit, repeat system, and repeat seed (`E = 0.04069` on `1632/s42`, `0.09550` on `851/s42`, `0.03492` on `1632/s41`, valid horizon `10.0`) at `lr = 1e-4` (`N = 155,100`).

**Impact:** proved that the locked 12-layer SIREN representation can represent and learn Stage-0 orbits when trained at `lr = 1e-4` on `L_data`, shifting the entire root-cause diagnosis from representation capacity to optimizer/recipe dynamics.
**Source:** 67-11-SUMMARY.md, 67-EXP03-RESULT.md, 67-FINDINGS.md

### `lr = 1e-3` was confirmed-worsening (`34.8x` worse `E` on `1632/s42`), refuting the "higher LR helps escape the mean" hypothesis
The prospective `EXP-03` hypothesis allowed that a higher learning rate might accelerate escape from the mean predictor; instead, `lr = 1e-3` was the only arm across all four Phase 67 ladders to reach a confirmation-grade verdict — and it confirmed **worsening** (`E = 1.4552` vs `0.04069` on `1632/s42`, `1.2422` vs `0.09550` on `851/s42`, `1.1583` vs `0.03492` on `1632/s41`, all settled Tier 0).

**Impact:** fired the reserved `REFUTED-LEAD` checkpoint (`67-EXP03-RULING.md`) and directly explained why Phase 60's `1e-3` cosine-schedule runs collapsed.
**Source:** 67-11-SUMMARY.md, 67-EXP03-RESULT.md, 67-EXP03-RULING.md

### Orbit-scaled Fourier time features (`EXP-04`) worsened `E` on `1632/s42` and `851/s42` relative to raw `tau`
Appending fundamental (`f1`) or fundamental+second-harmonic (`f12`) sin/cos features at the inner binary's orbital frequency `N_in / T` degraded `E` on both `1632/s42` and `851/s42` for both `locked-12` and `exp01` backbones (pushing `locked-f1` and `locked-f12` on `851/s42` from Tier 1 `E = 0.0897` back to Tier 0 `E = 0.1404` and `0.1180`), while improving only on the `1632/s41` repeat seed.

**Impact:** showed that naive harmonic time encoding does not improve single-orbit fitting over raw `tau` once the learning rate is set to `1e-4`.
**Source:** 67-13-SUMMARY.md, 67-EXP04-RESULT.md, 67-FINDINGS.md

### Depth `d8` (`532,489` params) achieved the lowest `E` across all three cases in `EXP-02`, while `d2` failed to Tier 0 at `first_omega_0 = 30`
At the locked `first_omega_0 = 30`, shallow depth `d2` worsened to Tier 0 on all three cases (`E = 0.1292, 0.2587, 0.1275`), whereas `d8` beat `d12` on all three cases (`E = 0.02581` vs `0.02689` on `1632/s42`, `0.06808` vs `0.10722` on `851/s42`, `0.01097` vs `0.03651` on `1632/s41`), though unsettled endpoints on `d12` prevented formal confirmation.

**Impact:** demonstrated that shallow networks at low `first_omega_0 = 30` lack bandwidth (unlike `EXP-01`'s `d1` at `first_omega_0 = 1000`), while moderate depth (`d8–d12`) at `first_omega_0 = 30` and `lr = 1e-4` fits cleanly.
**Source:** 67-09-SUMMARY.md, 67-EXP02-RESULT.md, 67-FINDINGS.md

### All 124 real Phase 67 timing, metadata, and science launches completed with zero burned science directories and zero retries
Across `4` metadata captures, `60` timing rows, and `60` science rows (`101,873` UTC seconds = `28.30 hours`), the AC/weekend power guard, remaining-window admission, and process-group supervisor produced zero mid-run science failures, zero burned science directories, and zero retries (the only two pre-attempt refusals — an AC-power pause in `67-08` timing and the subprocess materialization catch in `67-14` timing — occurred before `attempt.json` creation).

**Impact:** delivered a complete, gap-free 60-cell science matrix across all four ladders on the first and only look.
**Source:** 67-08..16-SUMMARY.md, 67-VERIFICATION.md
