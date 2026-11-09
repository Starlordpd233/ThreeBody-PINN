---
phase: 66
phase_name: "Small-Network Control"
project: "Three-Body Physics-Informed LLM"
generated: "2026-11-08"
counts:
  decisions: 6
  lessons: 5
  patterns: 5
  surprises: 4
missing_artifacts:
  - "66-UAT.md"
---

# Phase 66 Learnings: Small-Network Control

Phase 66 executed `EXP-01`, testing whether a shallow, smaller-parameter SIREN (`exp01-d1-w384-o1000`: 1 hidden layer of width 384, `157,065` parameters vs `795,657` locked, `first_omega_0 = 1000`, constant Adam `lr = 1e-4`, raw `[tau, IC13]`) can fit a single Stage-0 training orbit on `[0, 10]`. After a blind 5,200-step timing run (`0.004238 s/step`) set the cost-only common budget to `N = 465,000` steps under the 3,300-second cap, all three single-look science runs (`1632/s42`, `851/s42`, and `1632/s41`) reached settled Tier 1 (`E = 0.01143`, `0.01721`, `0.07898`; valid horizon `10.0`, `still_improving = false`), mechanically confirming `route = phase67-as-planned`. At Owner Checkpoint 1 (`66-CHECKPOINT-1-RULING.md`), the owner accepted the recorded proposal (`Accept the recorded proposal`). Extracted from `66-01..05-PLAN.md`, `66-01..05-SUMMARY.md`, `66-TIMING-PREDICTION.md`, `66-PREDICTION.md`, `66-RESULT.md`, `66-CHECKPOINT-1-RULING.md`, `66-VALIDATION.md`, `66-VERIFICATION.md`, and `STATE.md`. No UAT file exists for this phase.

## Decisions

### Freeze all seven Phase 66 harness modules before committing the first prediction page or registration
All code edits to `diagnostic_fit.py`, `diagnostic_phase66.py`, and `diagnostic_power.py` were completed and frozen at commit `734cb7da` (Plan 66-02) before `66-TIMING-PREDICTION.md` and `timing-registration.json` were authored in Plan 66-03.

**Rationale:** every Phase 66 registration pins seven module SHA-256 digests (`fit`, `guard`, `data`, `variants`, `similarity`, `phase66`, `power`); any code edit after registration retires live admission and forces fresh prediction pages and registrations.
**Source:** 66-01-SUMMARY.md, 66-02-SUMMARY.md, STATE.md (Decisions from 66-01, 66-02)

### Gate all real timing and science launches on AC power and the America/Chicago weekend window in code
`diagnostic_power.py` checks `pmset -g batt` first line for `AC Power` and `require_weekend_window` for Saturday `00:00` through Sunday `22:00 America/Chicago` (refusing naive clocks or unloadable timezones) before repository resolution, output-exists precheck, registration admission, exclusive `power-gate.json` receipt creation, and `caffeinate` child launch.

**Rationale:** enforces the owner's standing operational rule (D-08) deterministically so an accidental weekday or battery invocation refuses with `POWER-REFUSED` before creating any directory or claim.
**Source:** 66-01-SUMMARY.md, 66-02-SUMMARY.md, STATE.md (Decisions from 66-02)

### Size the step budget `N = 465,000` strictly from timing-run cost arithmetic with timing scores unread
`compute_budget` calculates the largest multiple of `1,000` steps whose projected wall (timing launch overhead + warmup + measured steps at `1.25 × seconds_per_step` + 14-entry cadence logging cost) fits within `0.75 × 3,300 s = 2,475 s`, while `loss_trace_stride = ceil(N / 10,000) = 47` bounds record size below the `1,307,538`-byte ceiling independently of `N`. `check-run` verifies the timing run without printing or reading its score.

**Rationale:** sizing `N` purely from wall-clock throughput prevents adaptive stopping on fit quality, and bounding `loss_trace` stride at source ensures record-size limits never truncate a fast model's step budget.
**Source:** 66-02-SUMMARY.md, 66-03-SUMMARY.md, STATE.md (Decisions from 66-02, 66-03)

### Pre-register a mechanical five-label reading rule and three-run confirmation gate
`classify_exp01` assigns each run to `tier1` (`E <= 0.1`), `near` (`0.1 < E <= 0.25`), `between` (`0.25 < E < 0.85 × E_const`), `other`, or `unsettled` (when output-movement growth from the last cadence entry at or before `0.75·N` to `N` exceeds `0.01`, provided no mechanical or setting problem exists), and `confirm` requires all three runs (`1632/s42`, `851/s42`, `1632/s41`) to share `tier1` or `near` before routing `phase67-as-planned` or `propose-66.1`.

**Rationale:** fixing the reading and routing function in tested code before any run prevents post-hoc reinterpretation of partial or single-seed improvements.
**Source:** 66-02-SUMMARY.md, 66-PREDICTION.md, 66-RESULT.md

### Transition the Phase 65 smoke registration to historical run-commit verification after `diagnostic_fit.py` extension
When Plan 66-01 extended `diagnostic_fit.py` (six sites: registry-aware `validate_smoke_settings`, record/verify registry fields, and registration-declared `loss_trace_stride`), `tests/phase66/test_historical.py` pinned the Phase 65 smoke record's provenance at its run commit (`c919194d`) while asserting that live admission against current `HEAD` exits 2 naming only `diagnostic_fit.py`.

**Rationale:** preserves immutable Phase 65 evidence and proves that the live drift gate catches the exact edited module.
**Source:** 66-01-SUMMARY.md, STATE.md (Decisions from 66-01)

### Owner Checkpoint 1 ratifies `phase67-as-planned` with zero roadmap or requirement edits
After `66-RESULT.md` reported confirmed Tier 1 across all three runs, the owner replied verbatim `"Accept the recorded proposal"`, recorded in an opaque `owner-quote` fence in `66-CHECKPOINT-1-RULING.md` (`e40ebca2`). Phase 67 proceeds as planned with no `SCOPE-49` amendment.

**Rationale:** under `route = phase67-as-planned`, the pre-registered proposal is `none`; the ruling records owner sign-off without mutating `ROADMAP.md` or `REQUIREMENTS.md`.
**Source:** 66-05-SUMMARY.md, 66-CHECKPOINT-1-RULING.md, 66-VERIFICATION.md

---

## Lessons

### Parameter count (`157,065` vs `795,657`) was not the cause of the v2.4 single-orbit failure
A network roughly one-fifth the size of the locked 12-layer architecture (`157,065` parameters vs `795,657`), with a single hidden layer of width 384 (`first_omega_0 = 1000`, `lr = 1e-4`), fit both Stage-0 orbits to Tier 1 (`E = 0.01143` on `1632/s42`, `0.01721` on `851/s42`, `0.07898` on `1632/s41`) with valid horizon `10.0`.

**Context:** interpreting the confirmed `EXP-01` Tier-1 result in `66-RESULT.md`.
**Source:** 66-05-SUMMARY.md, 66-RESULT.md, 66-VERIFICATION.md

### Simultaneously changing depth (`12 -> 1`), width (`256 -> 384`), `first_omega_0` (`30 -> 1000`), and learning rate (`1e-3 -> 1e-4`) proves feasibility but leaves individual factors confounded
While `EXP-01` proved that the data pipeline, coordinate scaling, and `L_data` objective support Tier-1 single-orbit fits, it could not isolate whether shallow depth, high `first_omega_0`, or lower learning rate unlocked the fit—making Phase 67's one-factor-at-a-time ladders essential.

**Context:** the identifiability-limits section of `66-RESULT.md`.
**Source:** 66-RESULT.md, 66-05-SUMMARY.md

### Record-size ceilings must be enforced via trace-stride thinning rather than capping step count `N`
At `4.24 ms/step`, a 40-minute budget allows `465,000` steps. Logging every step's loss would exceed the 1.3 MiB committed-record ceiling and artificially cap `N`; introducing `loss_trace_stride = ceil(N / 10,000) = 47` kept the JSON record at `1.25 MiB` (`9,895` loss entries + `14` similarity entries) across the full `465,000` steps.

**Context:** resolving checker blocker 2 ("time alone sets N") in Plan 66-02.
**Source:** 66-02-SUMMARY.md, 66-03-SUMMARY.md, 66-04-SUMMARY.md

### Detached child processes must own their process group (`start_new_session=True`) to survive agent subshell termination
Before launching the real timing run in Plan 66-03, a survival test verified that the `diagnostic_power.py` child process kept `PGID == PID` and survived a group `SIGTERM` sent to the parent subshell. Without session isolation, tool-call timeouts would kill multi-minute runs mid-flight.

**Context:** verifying detached execution before the timing and science launches in Plans 66-03 and 66-04.
**Source:** 66-03-SUMMARY.md, STATE.md (Decisions from 66-03)

### Output movement settles near `1.0` well before `465,000` steps on a 1-layer SIREN
Across all three `EXP-01` science runs, output movement (the ratio of predicted trajectory RMS about its mean to ground-truth trajectory RMS about its mean) reached `0.996..1.001` by `0.75·N` (`348,750` steps) and changed by less than `0.002` over the final `116,250` steps (`still_improving = false`).

**Context:** evaluating the `0.01` output-movement settlement criterion in Plan 66-05.
**Source:** 66-05-SUMMARY.md, 66-RESULT.md

---

## Patterns

### Blind timing calibration (`check-run` without score emission)
Run a short registered timing job (`5,200` steps: `200` warmup + `5,000` measured) on the target hardware, verify its mechanical completion and read only `seconds_per_step` and `launch_wall_seconds` via a value-free `check-run` command that never prints `E` or `tier`, and commit the derived step budget `N` before launching science runs.

**When to use:** sizing compute-bounded experiments on hardware whose step throughput varies strongly with architecture depth/width.
**Source:** 66-02-SUMMARY.md, 66-03-SUMMARY.md, 66-04-SUMMARY.md

### Ordered git-ancestry chain (`page -> timing reg -> timing record -> prediction page -> science regs -> science records -> result -> ruling`)
Commit each stage of an empirical experiment as a separate atomic commit and verify in code (`git merge-base --is-ancestor`) that every registration commit precedes its run commit and every run commit precedes the review/ruling commit.

**When to use:** pre-registered single-look experiments that must prove no registration or reading rule was altered after seeing results.
**Source:** 66-03-SUMMARY.md, 66-04-SUMMARY.md, 66-05-SUMMARY.md, 66-VERIFICATION.md

### Hardware/calendar launch receipt (`power-gate.json`) bound to the run directory
Write an exclusive `power-gate.json` receipt recording the raw `pmset -g batt` first line, aware UTC and `America/Chicago` timestamps, ISO weekday, and child `caffeinate` command before spawning the worker, and verify `checked_utc <= started_utc` during post-run audit.

**When to use:** unattended long runs subject to power and time-of-week governance rules.
**Source:** 66-01-SUMMARY.md, 66-02-SUMMARY.md, 66-04-SUMMARY.md

### Shared JSON-normal design block embedded verbatim in prediction pages (`DESIGN-OK` round-trip)
Define the experiment's canonical parameters in a pure Python function (`exp01_design()`), embed its `json.dumps(..., indent=2, sort_keys=True)` block inside a fenced block in `66-TIMING-PREDICTION.md` and `66-PREDICTION.md`, and verify byte-exact round-trip equality plus prose number consistency before admitting any registration.

**When to use:** keeping markdown prediction pages and machine-checked JSON registrations strictly synchronized.
**Source:** 66-02-SUMMARY.md, 66-03-SUMMARY.md

### Triple-keyed multi-run review (`(orbit_key, seed, registration_sha256)`)
Key multi-run confirmation reviews by the exact `(orbit_key, seed, registration_sha256)` tuple declared in the prediction page, refusing duplicate runs, retry directories when primary runs succeeded, or runs with any mechanical or setting problem.

**When to use:** aggregating main, repeat-system, and repeat-seed runs into a single confirmation verdict.
**Source:** 66-02-SUMMARY.md, 66-05-SUMMARY.md

---

## Surprises

### A 1-hidden-layer SIREN achieved `E = 0.0114` (`~9x` below the `0.10` Tier-1 bar) on `1632/s42`
After every 12-layer Phase 60 arm stalled at `E = 1.14..1.24` (Tier 0, valid horizon `0.0`), the 1-layer `exp01-d1-w384-o1000` control reached `E = 0.01143` on `1632/s42` and `E = 0.01721` on `851/s42`—tracking all three bodies across the entire 10-time-unit (`10–18` inner-lap) window with valid horizon `10.0` at both `10%` and `1%` thresholds.

**Impact:** immediately ruled out "network too small" and "broken Stage-0 data/scoring pipeline" as causes of the v2.4 failure.
**Source:** 66-05-SUMMARY.md, 66-RESULT.md

### The 1-hidden-layer network ran `3.3x` faster per step (`4.24 ms/step` vs `14.27 ms/step` for 12 layers)
Measured MPS step time dropped from `0.014265 s/step` on `locked-12` (Phase 65 smoke) to `0.004238 s/step` on `exp01-d1-w384-o1000`, allowing `465,000` updates inside a ~32-minute wall time (`1,957 s`, `1,734 s`, and `2,034 s` across the three science runs).

**Impact:** gave `EXP-01` over `4.6x` the 100,000-step sanity floor within a single 55-minute cap.
**Source:** 66-03-SUMMARY.md, 66-04-SUMMARY.md

### Even with a `E = 0.0114` Tier-1 position fit, autograd energy drift `eps_H` was `0.369..1.269` (`36,900x` above `10^-5`)
While `EXP-01` achieved Tier 1 in position accuracy (`E <= 0.1`), its FEAS-01 autograd Hamiltonian drift was `0.3693` (`1632/s42`), `0.5060` (`851/s42`), and `1.2689` (`1632/s41`)—still four to five orders of magnitude above the `10^-5` Tier-2 energy bar.

**Impact:** highlighted the gap between pure position fitting (`L_data` only) and differentiated energy conservation, feeding directly into Phase 68's yardstick audit and Phase 69's Direction A decision.
**Source:** 66-RESULT.md, 66-VERIFICATION.md

### Adjacent-time hidden cosine similarity on the successful 1-layer fit (`0.9647..0.9718`) was lower than the input layer's (`0.9963..0.9966`)
Unlike the failed 12-layer Phase 60 networks where hidden cosine similarity increased toward `1.0000` with depth, the 1-layer `first_omega_0 = 1000` network expanded adjacent-time feature separation below the raw input cosine (`0.9647` vs `0.9966` on `1632`), giving the linear output readout distinct features at every time sample.

**Impact:** confirmed that preserving distinct time representations at the final hidden layer is strongly associated with Tier-1 orbit fitting.
**Source:** 66-RESULT.md
