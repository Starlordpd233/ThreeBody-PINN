# Phase 66: Small-Network Control - Research

**Researched:** 2026-10-31 (Saturday; the Mac was on AC power during the research)
**Domain:** A pre-registered positive-control fit on the INST-08 diagnostic harness: first-layer SIREN bandwidth, a registry extension for non-locked variants, a macOS AC-power launch gate, and a timing-run-to-budget sequence.
**Confidence:** MEDIUM-HIGH. Harness mechanics are HIGH (code read, baselines re-run). The architecture and `first_omega_0` recommendation is MEDIUM: it rests on committed census numbers and no-training synthetic probes, because no Stage-0 record may be opened during research.

Source tags: `[VERIFIED: path:lines]` = file opened with Read this session, value quoted; `[VERIFIED: local computation]` = computed this session (re-derivable from Appendix A); `[CITED: ...]` = official or committed documentation; `[ASSUMED]` = judgment or training knowledge, listed in the Assumptions Log.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

#### Decision ownership

- **D-01:** Phase 65 D-01 carries forward. Agents make the technical and
  scientific calls, recording evidence and rationale. The owner is asked only
  for scope, resource and other reserved choices. Owner checkpoint ① is the
  designed review after this experiment. It is not a technical questionnaire.

#### What the experiment is for

- **D-02:** Design EXP-01 as a positive control. The small network must be one
  that should fit orbit 1632 if the data and scoring path are sound and size
  is the only obstacle. The pre-registered branches then read cleanly:
  - Tier 1 refutes "too small" for one orbit. It also shows that the
    data-to-scorer path can produce a passing fit.
  - E near the constant predictor's points at the path from the data to the
    scorer. The agent then proposes the registered inserted phase (66.1).
  - Anything else goes to the owner.
- **D-03:** Read "from time alone" as a data-only fit of position against time,
  with no physics term. The input stays the production 14-input design,
  `[tau, IC13]`. On one orbit the 13 IC values are constant, so time is the
  only varying input. Changing the input design is EXP-04's question (Phase
  67), so EXP-01 does not change it.

#### The network

- **D-04:** Use the production layer types (`SQRSkipResNetSIREN` built
  through the INST-08 variant registry). Use at most 2 hidden layers, and fewer
  parameters than the locked network's approximately 0.8M, as EXP-01 requires.
  The 2-layer limit keeps the network below the depth where the probe found
  neighbour similarity collapsing (layers 2-3 onward, `65-FINDINGS.md`
  Section 1). The prediction page fixes the exact depth, width and parameter
  count.
- **D-05:** Set the first layer's frequency scale (`first_omega_0`, a
  diagnostic-only setting inside the harness, as in v2.4's G2 sweep) so that
  its starting time-frequency range covers the orbit's inner-lap rate. Without
  this, a shallow network would fail for a reason unrelated to size or to the
  pipeline. That would wrongly trigger the "near the constant predictor"
  branch.
  - **Why:** the production first layer initializes weights in
    `U[-1/n_in, 1/n_in]` with `n_in = 14` (`pinn/network.py`, `_SIRENLayer`).
    At `first_omega_0 = 30`, its fastest starting time frequency is about
    30/14 = 2.1 rad per unit tau, and its median is about half that. This
    agrees with Phase 65's measured median of 0.325 cycles over the window.
    The window [0, 10] maps to tau in [-1, 1]. Orbit 1632's 10.47 inner laps
    therefore need about 2*pi*10.47/2 = 33 rad per unit tau. That is about 15
    times the fastest starting frequency and 30 times the median. Orbit 851's
    18.61 laps need about 58.
  - The locked deep network does not have this problem in the same way: at
    `first_omega_0 = 480` (about 34 rad per unit tau at the fastest), the G2
    arm still ended at E 1.1575. Bandwidth alone therefore does not explain
    v2.4.
  - The shallow network at the locked 30 is EXP-02's 2-layer rung (locked
    layer types, everything else locked). It belongs to Phase 67.
  - The prediction page shows this calculation from the Phase 59 census and
    chooses one value that covers the faster of the two repeat systems (851).
    Research verifies the bandwidth argument before the page is committed. If
    research finds it wrong, the page follows the evidence and records why.
- **D-06:** Keep every other setting at its locked or harness value:
  - data-only;
  - constant-rate Adam at the locked 1e-4. The learning rate is EXP-03's
    factor;
  - the full [0, 10] window. The window is EXP-05's factor;
  - `hidden_omega_0 = 1.0`;
  - MPS float32, seed 42;
  - the 1,001-sample Stage-0 training gold record.

  One variant definition serves all three runs.

#### Repeats and reading

- **D-07:** Pre-register both repeats on the same prediction page as the main
  run, and run them whichever branch the main run lands in, so no repeat is
  chosen after a result is seen:
  - **System 851 at seed 42.** It is the next panel system by inner-lap count,
    as in the v2.4 G2 confirmation rule.
  - **System 1632 at seed 41.** It is the next seed in the 42, 41, 43 order
    of the `trainex-r4` ruling.

  The main result is reported as confirmed only if both repeats land in the
  same branch. Otherwise the disagreement goes to the owner at checkpoint ①.
- **D-08:** The run length is set by need, not by a fixed owner cap. Each
  variant's seconds-per-step is measured by its own registered timing run,
  because Phase 65's rate applies to `locked-12` only.
  - **Owner's answer (2026-10-31), verbatim:** "as long as you need. this mac
    will be plugged into power for the weekend only. not weekdays. i have
    classes weekdays".
  - **Consequences:**
    - Training runs happen only while the Mac is on AC power, which in
      practice means weekends. Each launch first confirms AC power and
      refuses on battery.
    - Work that is not compute (research, the prediction page, harness
      extensions, tests) may proceed at any time.
    - Prefer runs under one hour, the harness's existing cap. A small network
      gets several hundred thousand steps in that time, comparable to
      Rung 1's 794,350 Adam steps on the locked network.
    - A longer run, or a bounded extension rule ("still improving at the cap,
      run once more"), may be pre-registered on the prediction page if the
      timing evidence calls for it. Any run at or above one hour must first
      prove compatibility with the governed pause, resume and power-guard
      tooling (SCOPE-48, `65-CLOSEOUT.md` reuse conditions). The cap
      refusals are not loosened to avoid that check.
- **D-09:** The reading rule uses the frozen Tier 1 line (E <= 0.1). Before the
  first run, the prediction page defines "near the constant predictor's E"
  numerically on each system. The constant predictor scores 1.1538 on 1632
  and 1.2337 on 851; the two-Kepler formula scores 0.9168 on 1632. Results
  between Tier 1 and that band are explicitly routed to the owner. The page
  also states what each suspect predicts:
  - "too small" predicts failure;
  - a working pipeline, with the depth-linked lead, predicts Tier 1;
  - a pipeline defect predicts the constant-predictor band.

  No rule is re-set after a result is seen.

#### Scoring, records and isolation

- **D-10:** Score with the frozen FEAS-01 scorer, beside the window-mean
  constant predictor and the two-Kepler formula on the same orbit and window.
  Log the per-layer neighbour-similarity trace through the shared DIAG-09
  logger at a fixed cadence. Training loss is context only. `eps_H` is
  reported with the GAP-59-08 limitation stated, because the energy metric is
  adjudicated in Phase 68.
- **D-11:** Each experiment run uses a fresh committed registration, never the
  Phase 65 smoke registration. Phase 66 variants are added through
  `register_variant` without altering the sealed `locked-12` catalog. Harness
  changes that admit a registered non-locked variant need their own tests. The
  Phase 65 evidence, hashes and registrations stay unchanged. Access is
  Stage-0 TRAIN only, with the pre-open refusals retained. The WR-01 nested
  marker limitation stays a precondition for any graded use, not for this
  phase.

#### Review and plan change

- **D-12:** At checkpoint ①, record the branch taken, a plain-language reading
  and any SCOPE-49 proposal (for example, an inserted Phase 66.1 or re-aimed
  Phase 67 experiments), with the owner's answer. A proposal blocks only the
  work that depends on it.

### Claude's Discretion

- The exact depth (1 or 2), width, parameter count and `first_omega_0` value,
  justified on the prediction page.
- The timing-run length, similarity cadence, step budgets and any
  pre-registered extension rule, set from measured rates.
- The numeric constant-predictor band and the exact branch table.
- The smallest harness extension and AC-power launch check that admit Phase 66
  variants without weakening the Phase 65 refusals.

No source-silent semantic decision arose. EXP-01 assigns the architecture to
the prediction page, and the decisions above fall inside the pre-registered
branches. No gap is opened, and `.planning/milestones/v2.5-GAPS.md` is not
created.

### Deferred Ideas (OUT OF SCOPE)

- The locked-frequency shallow network, the depth ladder, the learning-rate
  ladder, time-input designs and window lengths: Phase 67.
- Energy-metric adjudication and pass bars: Phase 68. GAP-59-08 stays open.
- Repairing the governed pause/resume and power-guard tooling: only if a run
  at or above one hour is registered.

#### Reviewed todos, not folded

- `.planning/todos/pending/d-06-static-epsilon-sensitivity-check.md`: concerns
  stage labels and validation gates, outside this training-only, data-only
  phase. Same disposition as Phase 65.
- `.planning/todos/pending/trainex-r1-research-handoff.md`: stale handoff
  housekeeping. Same disposition as Phase 65.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| EXP-01 | The small-network control (tests "too small"): a network with fewer parameters and fewer layers than the locked one fits orbit 1632 from time alone; architecture fixed on the prediction page. Acceptance: tier, `E` against the constant predictor and the formula, and neighbour similarity recorded; Tier 1 (`E <= 0.1`) refutes "too small" for one orbit; result reviewed at owner checkpoint ①. [VERIFIED: .planning/REQUIREMENTS.md:115-121] | Variant `exp01-d1-w384-o1000` (157,065 parameters, 19.7% of locked) with the bandwidth evidence (Pattern 1); harness extension and tests (Pattern 2); AC gate (Pattern 3); timing-to-budget sequence (Pattern 4); page contents and numeric reading rule (Pattern 5); scoring fields (Pattern 6). |
| SC-1 | A prediction page is committed before the first run: architecture and parameter count, what each suspect predicts, the budget from the measured rate, the reading rule. [VERIFIED: .planning/ROADMAP.md:164] | Two-page sequence in Pattern 4; page contents in Pattern 5; ancestry check in Validation Architecture. |
| SC-2 | Result on orbit 1632 scored (tier, `E` against constant predictor and two-Kepler formula, neighbour-similarity trace); a confirming result repeated on a second panel system and a second seed. | `fit_diagnostic` already records all of it (Pattern 6); repeats 851/42 and 1632/41 (D-07). |
| SC-3 | Review recorded: branch taken, plain-language reading, any SCOPE-49 plan change with the owner's answer. | Branch table, confirmation rule and reading templates in Pattern 5; manual owner answer. |
</phase_requirements>

## Summary

Phase 66 needs no new training, scoring or logging code. The Phase 65 harness (`fit_diagnostic` plus the `diagnostic_fit` CLI) already fits one named variant data-only on a Stage-0 training orbit, scores it with the frozen FEAS-01 scorer beside the window-mean constant predictor and the two-Kepler formula, logs the DIAG-09 similarity trace at a registered cadence, and publishes an exclusive, marked record. What is missing is (a) a way for a registered, non-locked variant to pass `validate_smoke_settings`, (b) an AC-power launch gate, (c) a measured seconds-per-step for the new network, and (d) the committed pages that fix the architecture, the numeric reading rule and the budget before any experiment run.

The D-05 bandwidth arithmetic is correct and I confirmed it end to end (first-layer init, window-to-tau map, census lap counts, and an instantiation of the production class). It is directionally right but incomplete in two ways that matter for choosing the number: the fundamental is a floor rather than the Tier-1 bandwidth (the census separation extrema suggest highly eccentric inner orbits, so harmonics matter), and hidden layers supply extra bandwidth at initialization, so over-shooting `first_omega_0` hurts. No-training synthetic probes put the usable window at `first_omega_0` 819 to 1,200 for a 1-hidden-layer network, with 1,000 as the recommended point. The same probes show width 256 is borderline for system 851 and width 384 is comfortable, which fixes the recommended network: depth 1, width 384, 157,065 parameters.

The one genuinely consequential engineering fact: every extension that admits a variant through `validate_smoke_settings` must edit `diagnostic_fit.py`, which the Phase 65 smoke registration pins by SHA-256. After that edit, the Phase 65 smoke registration stops admitting against the live tree, exactly as the probe registration did in Plan 65-06. This is anticipated by `65-CLOSEOUT.md:86-89`, but the plan must record the disposition and add a historical-bytes test. Everything else in the extension is additive in new files.

**Resolutions to the seven assigned questions**

| # | Question | Resolution (detail in the pattern named) | Confidence |
|---|---|---|---|
| Q1 | D-05 bandwidth argument | Verified: first-layer time frequency is at most `first_omega_0/14` rad per unit tau (`first_omega_0/(14*pi)` cycles per window; 0.682 at 30). One inner lap is `pi` rad per tau, so the fundamentals are 32.9 (1632) and 58.5 (851) rad per tau; fundamental-covering `first_omega_0` is 460.6 and 818.6. Refinements: fundamentals are a floor; overshoot is harmful. Recommended range 819 to 1,200, point 1,000. (Pattern 1) | HIGH arithmetic, MEDIUM range |
| Q2 | Smallest harness extension | New `diagnostic_phase66.py` (variant, `register_variant`-derived registry, named-registry table) plus one edit to `diagnostic_fit.py` (about 25 lines: a registration-declared `variant_registry` lookup, registry fields on the record, a verify check). Sealed `REGISTRY` and the other four Phase 65 pins stay byte-identical. 19 named extension tests, plus the power, reading-rule and page tests. (Pattern 2) | HIGH mechanics, MEDIUM disposition |
| Q3 | AC-power check | Fail-closed parse of the first line of `pmset -g batt` (`Now drawing from 'AC Power'`), in a new `diagnostic_power.py`, composed as a `launch` command that precedes and execs `caffeinate -is ... diagnostic_fit run`, and writes a receipt. Do not reuse the fail-open `on_battery()`. (Pattern 3) | HIGH |
| Q4 | Timing run and criterion 1 | Own registration and own short page, then the main page with the measured budget. Criterion 1 can only mean "before the first experiment run", because the page must contain a measured rate. Freeze the scientific design in the timing page so it precedes every run. (Pattern 4) | MEDIUM |
| Q5 | Page contents | Variant JSON block, parameter breakdown, suspect table, numeric band (plus or minus 5 percent of the record's own constant-predictor E), branch table, repeats and confirmation rule, budget formula, cadence, retry rule, GAP-59-08 sentence. (Pattern 5) | MEDIUM-HIGH |
| Q6 | Scoring path | No new code. Fields to read are listed; the reading rule becomes one tested function. (Pattern 6) | HIGH |
| Q7 | SCOPE-48 at or above one hour | The diagnostic fit has no checkpoint, resume or SIGINT path, and the Phase 60 control scripts are hard-wired to the Phase 60 launcher. A one-hour-plus run needs new harness features plus a new control layer; stay under one hour. (Pattern 7) | HIGH |

**Primary recommendation:** Register one variant, `exp01-d1-w384-o1000` (depth 1, width 384, `first_omega_0 = 1000`, 157,065 parameters), through a new `diagnostic_phase66` catalog admitted by a registration-declared `variant_registry` lookup; gate every launch on a fail-closed AC check; run a separately registered 5,200-step timing run first; then run three pre-registered runs under one hour (1632 seed 42, 851 seed 42, 1632 seed 41) with the reading rule fixed on the page before any of them.

## Project Constraints (from CLAUDE.md)

- Use the Sequentialthinking MCP for any task of more than one step. [CITED: ./CLAUDE.md "Tooling"] (Not available to this researcher; the planner and executor should use it.)
- Orient in the owning worktree and surface Git state before work and before committing: this is `.worktrees/trainex` on `milestone/v2.5`; the existing modified and untracked files (`.planning/config.json`, a `docs/work/designs/milestone_v2.2/...` brief, `.agents/`, `.gsd/`, `.planning/state.json`, and others) are user-owned and must not be touched or staged. [CITED: ./CLAUDE.md "Git Branch Awareness"; VERIFIED: git status this session]
- Commit only through `scripts/agent-commit` with `GIT_AGENT_ID` and `GIT_AGENT_OWNED_PATHS`; stage explicit owned paths; no `git add .`/`-A`/`-u`; no `--no-verify`; no pushes from `milestone/*`. Message form `<type>(<scope>): <lowercase imperative subject>` (types `spec evidence verify plan docs feat fix refactor test chore`; scopes such as `66`, `66-01`, `pipeline`, `pinn`); body required for `.planning/` or multi-file commits; include `Agent-Assisted-By:` or `Co-Authored-By:`. `core.hooksPath` is already `.githooks`. [CITED: ./CLAUDE.md "Git Commit Protocol"; VERIFIED: git config this session]
- Destructive Git operations require exact approval plus the three `ALLOW_DESTRUCTIVE_GIT`, `GIT_DESTRUCTIVE_APPROVAL`, `GIT_RECOVERY_CHECKPOINT` markers. [CITED: ./CLAUDE.md]
- If the plan writes under `docs/`, follow `docs/README.md` placement and frontmatter rules. Phase 66 artifacts belong in `.planning/phases/66-small-network-control/`, so this normally does not apply. [CITED: ./CLAUDE.md "Docs plan-review-fix lifecycle"]
- Expensive-validation evidence reuse (global CLAUDE.md): any command expected to exceed 60 seconds (each training run) must keep complete stdout, stderr, exit status, command, directory and elapsed time in a session temp file outside the repository, and must not be rerun merely to reformat output. [CITED: ~/.claude-free/CLAUDE.md "Expensive validation evidence reuse"]
- `STATE.md` is maintained by hand in this checkout; the `gsd-tools` mutating verbs have corrupted it before. [VERIFIED: .planning/STATE.md:50-51 "**This file is maintained by hand in this checkout.** The `gsd-tools`"]
- Locked and pinned modules do not change: `pinn/network.py`, `pinn/architecture_spec.py` and `pinn/constants.py` are among the 33 `PINNED_MODULES`; the frozen scorer and scorecard are pinned. [VERIFIED: pinn/verification/learnability_protocol.py:145-179] SCOPE-46 forbids locked-value moves. [VERIFIED: .planning/REQUIREMENTS.md:181]
- Use the proven interpreter `<home>/miniforge3/envs/pinn-train/bin/python -B` from the trainex root. [VERIFIED: .planning/phases/65-probe-on-the-record-fit-harness/65-CLOSEOUT.md:95-96]
- STOP/gap protocol: v2.5 is not an adjudication milestone and `66-CONTEXT.md` opens no gap. If planning meets a source-silent semantic decision, surface it rather than inventing. [CITED: ./CLAUDE.md "CRITICAL GOVERNANCE"; 66-CONTEXT.md]

## Architectural Responsibility Map

This is a local research harness, so the tiers are the repository's own layers rather than client/server tiers.

| Capability | Primary tier | Secondary tier | Rationale |
|------------|-------------|----------------|-----------|
| What network is trained (variant definition) | `pinn/verification/diagnostic_phase66.py` (new catalog) | `diagnostic_variants.register_variant` | Variants are data; the sealed `REGISTRY` must not change. |
| Settings admission (is this run allowed) | `diagnostic_fit.validate_smoke_settings` | `diagnostic_guard.require_committed_registration` | One admission path; digest pins and refusals already live here. |
| Launch precondition (AC power) | New `diagnostic_power` launcher | macOS `pmset`, `caffeinate` | An environmental fact, not a registered fact; must precede the attempt claim. |
| Fit, score, record | `fit_diagnostic` and the frozen scorer | `diagnostic_similarity.measure_time_signal` | Unchanged; reuse is the point of INST-08. |
| Pre-registration (what is predicted) | Committed pages in the phase directory | Registrations that pin the page by SHA-256 | SCOPE-47. |
| Reading rule (which branch) | Page text | One tested function `classify_exp01` | One source of truth, unambiguous at boundaries. |
| Review and plan change | `66-REVIEW.md` plus the owner | `REQUIREMENTS.md`, `STATE.md` (by hand) | SCOPE-49 and owner checkpoint ①. |

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Python (pinn-train env) | 3.11.15 | Interpreter for harness, tests, tools | The proven interpreter for Phases 60-65. [VERIFIED: interpreter run this session] |
| torch | 2.12.1 (MPS available: True) | Production network, Adam, MPS float32 | Already provisioned; Phase 65 smoke ran on it. [VERIFIED: interpreter run this session] |
| numpy | 2.4.6 | Scorer inputs, comparison rows | Already provisioned. [VERIFIED: interpreter run this session] |
| `unittest` | stdlib | Test framework | Every `tests/phase*` suite uses it. [VERIFIED: 65-VALIDATION.md:19-24] |
| `pinn.verification.diagnostic_fit` / `_variants` / `_similarity` / `_data` / `_guard` | in repo | The harness | Phase 65, 204 tests green at closeout. [VERIFIED: 65-CLOSEOUT.md:105] |
| `/usr/bin/pmset`, `/usr/bin/caffeinate` | macOS Darwin 25.5.0 | Power source read; keep awake on AC | Present; the Phase 60 launcher already uses `caffeinate -is`. [VERIFIED: ls this session; .planning/phases/60-single-system-learnability/evidence/launch_phase60_arm.py:120] |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| `feasibility_scorer.score_network` / `score_trajectory` | frozen | Network score and comparison rows | Called by `fit_diagnostic`; never re-implemented. |
| `scripts/agent-commit` | in repo | Atomic commits under repo policy | Every commit by the executor. |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Registry-name lookup in `validate_smoke_settings` (recommended) | A zero-edit shim that validates a doctored `locked-12` copy of the registration | Keeps all five Phase 65 pins byte-identical, but it is a bypass, not an extension, and breaks as soon as lr or window differ (Phase 67). |
| Same | Clone the orchestration (about 300 lines) into a new module | Keeps the pins; duplicates `run_registered_smoke`, `_smoke_worker`, `_cmd_run`, `main`, `verify_fit_result` and invites drift. |
| Same | Rebind module globals on copies of the functions | Keeps the pins; metaprogramming a reviewer should reject. |

**Installation:** none. No package is added or upgraded; nothing recommended here needs more than the standard library and the existing pinned environment.

**Version verification:** not applicable to a registry; versions above were read from the interpreter in the pinned environment.

## Package Legitimacy Audit

Not applicable. This phase installs no external package, so no `package-legitimacy` check, registry lookup or postinstall inspection is required. `torch` and `numpy` are already present in the pinned environment and are not re-introduced. `pmset` and `caffeinate` are operating-system binaries, not packages.

**Packages removed due to [SLOP] verdict:** none
**Packages flagged as suspicious [SUS]:** none

## Architecture Patterns

### System Architecture Diagram

```
  non-compute work, any day                       compute, Mac on AC power (weekend)
  ------------------------                        ----------------------------------
  [A] harness extension + tests (TDD)
      tests/phase65 (204) + tests/phase66 green
  [B] 66-TIMING-PREDICTION.md (design block frozen)
      + timing-registration.json  --commit-->
                                                  diagnostic_power launch --registration R --output O
                                                    |  pmset -g batt: first line == "Now drawing from 'AC Power'" ?
                                                    |     no  --> REFUSE, exit 2, nothing created
                                                    |     yes --> write power-gate.json, exec caffeinate -is python -B -m
                                                    v             pinn.verification.diagnostic_fit run
                                                  _cmd_run: require_committed_smoke_registration
                                                    (committed-clean pins + parity receipt + validate_smoke_settings
                                                     [variant_registry lookup])
                                                    v
                                                  supervised worker (spawn, cap < 3600 s): claim attempt.json (O_EXCL)
                                                    -> Stage-0 TRAIN seam (1 gold record) -> fit_diagnostic
                                                       (Adam 1e-4, data-only, MPS fp32, synchronized timing,
                                                        similarity at registered cadence)
                                                    v
                                                  frozen score_network + window-mean constant + two-Kepler
                                                    -> record.json + diagnostic.weights   (+ verify-result)
  timing record --> budget --> [C] 66-PREDICTION.md (final) + 3 experiment registrations --commit-->
  main 1632/42, repeat 851/42, repeat 1632/41  (each: launch -> record -> verify-result -> commit)
  [D] 66-REVIEW.md: branch, plain-language reading, SCOPE-49 proposal --> owner checkpoint ①
```

### Recommended Project Structure
```
pinn/verification/
  diagnostic_phase66.py     # NEW: EXP01 variant, PHASE66_REGISTRY, REGISTRIES, classify_exp01, confirm
  diagnostic_power.py       # NEW: strict pmset parse, require_ac_power, launch (caffeinate exec), receipt
  diagnostic_fit.py         # EDIT (only existing file): ~25 lines, see Pattern 2
tests/phase66/
  __init__.py
  test_catalog.py  test_admission.py  test_records.py  test_reading_rule.py
  test_power.py    test_pages.py      test_historical.py
.planning/phases/66-small-network-control/
  66-TIMING-PREDICTION.md   66-PREDICTION.md   66-REVIEW.md
  evidence/timing/timing-registration.json   evidence/timing/<run>/{record.json,diagnostic.weights,attempt.json,power-gate.json}
  evidence/runs/{main-1632-s42,repeat-851-s42,repeat-1632-s41}/...   evidence/runs/*-registration.json
```

**Suggested wave order** (a sketch; the planner decides the plan split): (1) no compute, any day: harness extension, `diagnostic_power`, `classify_exp01` and `tests/phase66` test-first, both suites green, then the code freeze; (2) no compute: `66-TIMING-PREDICTION.md` with its frozen design block and `timing-registration.json`, committed; (3) AC window: timing launch, `verify-result`, commit the record; (4) no compute: `66-PREDICTION.md` with the measured budget and the three experiment registrations, committed; (5) AC window: main 1632/42, then 851/42, then 1632/41, each launched through the gate, verified and committed; (6) no compute: `66-REVIEW.md`, the SCOPE-49 proposal if any, and the owner's checkpoint ① answer; update `REQUIREMENTS.md` and `STATE.md` by hand. Waves 3 and 5 are the only ones that need AC power, and one weekend window covers both if waves 1, 2 and 4 are staged first.

### Pattern 1: Bandwidth and the `first_omega_0` choice (Q1)

**What was verified (each is a quoted source value or a computation):**

| Claim | Evidence |
|---|---|
| First-layer weights are `U[-1/n_in, 1/n_in]`; forward is `sin(omega_0 * (W x + b))` | `bound = 1.0 / self.in_features` [network.py:82]; `weight.uniform_(-bound, bound, generator=generator)` [:89]; `return torch.sin(omega * F.linear(x, self.weight, self.bias))` [:98]; input layer built as `_SIRENLayer(spec.input_dim, spec.hidden_width, omega_0=spec.first_omega_0, is_first=True, ...)` [:169-172]. With `input_dim = 14`, the time weight `W[j,0]` is `U[-1/14, 1/14]`. |
| tau is column 0 and the window maps to `[-1, 1]` | `tau = 2.0 * (times_t / T_CHARACTERISTIC_TIME) - 1.0` [diagnostic_data.py:555]; `tau_ic13=torch.cat((tau.reshape(-1, 1), ic13_rows), dim=1)` [:561]; `T_CHARACTERISTIC_TIME = 10.0` [constants.py:31]; "`tau` is computed with the locked `T_CHARACTERISTIC_TIME`, never rescaled to the shorter window" [diagnostic_data.py:45-47]. |
| Logger's frequency unit | `frequency = model.input_layer.weight[:, 0].detach().abs() * omega / math.pi` [diagnostic_similarity.py:225] ("cycles across the full normalized tau window", :77-80). So the logged `first_layer_frequency.max` is `omega_0/(14*pi)` in the same unit as a lap count. |
| Census lap counts | `"N_in": 10.471994061054543, "id": 1632` [panels.json:169-170]; `"N_in": 18.612048388702, "id": 851` [panels.json:176-177]; the same values in census rows 587 and 306. |
| Instantiated production class | `omega_0=30`: median 0.391, max 0.682 cycles (CPU float64 seed 42); over seeds 40 to 49 the median ranges 0.304 to 0.391 and the max 0.665 to 0.682; theory 0.341 and 0.682. The Phase 65 MPS smoke measured 0.325. [VERIFIED: local computation; 65-FINDINGS.md:73] |

**Resulting numbers** [VERIFIED: local computation]: one inner lap over the window is `pi` rad per unit tau, so the fundamentals are `pi*10.472 = 32.9` (1632) and `pi*18.612 = 58.5` (851) rad per unit tau. The ratios to the locked fastest starting frequency `30/14 = 2.143` are 15.35 and 27.29. The fundamental-covering `first_omega_0` is `14*pi*N_in` = 460.6 (1632) and 818.6 (851). D-05's arithmetic is exactly right, including the "15 times" and "30 times the median" figures.

**What D-05 leaves out (qualifications, not a reversal):**

1. *The fundamental is a floor.* The census gives separation extrema; with `e ~ (sep_max - sep_min)/(sep_max + sep_min)` the inner orbits are highly eccentric: `e ~ 0.768` (1632: `sep_min` 0.05552668574208042, `sep_max` 0.42347374305498314, census row 587) and `e ~ 0.854` (851: 0.0382007042892006, 0.48656026964633464, row 306). A Kepler-proxy Fourier truncation needs harmonics up to n = 4 (1632) and n = 6 (851) to keep the position error under 10 percent of the orbit's extent, n = 8 and 13 for 3 percent. [VERIFIED: local computation; the eccentricity estimate and the transfer to the real three-body orbit are [ASSUMED], A1.] A first layer alone would then need `first_omega_0` of about 1,842 and 4,912.
2. *Hidden layers supply bandwidth at initialization, and overshoot hurts.* A closed-form linear readout (the head is a linear map) on the production network's initial hidden features, fitted to a synthetic Kepler proxy on the 1001-point grid, gives a max readout error (relative to `1+e`) that falls to the plateau at `first_omega_0` of about 480 to 1,000 and then rises again (table below). Features from the input layer alone need the much larger values, as the harmonic estimate says. [VERIFIED: local computation, Appendix A]
3. *Training moves the first layer.* In v2.4 the trained median first-layer frequency was about 13 percent to 18 percent of `omega_0` in cycles per window for every `omega_0` from 30 to 480, an order of magnitude above initialization: 0.78 to 7.75 (w060), 1.56 to 16.80 (w120), 3.13 to 33.53 (w240), 6.25 to 66.38 (w480), 0.39 to 4.25 (r1-1632 polish), 0.39 to 3.98 (r1-851 adam), 0.39 to 5.29 (r1-4658 adam). [VERIFIED: .planning/phases/65-probe-on-the-record-fit-harness/65-PROBE-RESULT.md:48-63; ratios computed] A common absolute weight scale (median `|W[:,0]|` about 0.4 to 0.55) rather than a common absolute frequency is what that pattern looks like, so it is not evidence that the first layer sought the orbit's frequency. [ASSUMED], A3. The consequence for the choice: the end-of-training bandwidth scales with `omega_0`, so a very large value risks pushing the median above the gold-grid Nyquist limit of 500 cycles per window (1000 samples over the window gives 500 cycles); at 5,000 the same 0.14 ratio gives about 700.

**Readout-only error on the synthetic Kepler proxy (median over 3 seeds x 2 IC13 draws, width 256; lower is better; Tier-1 line is 0.1)** [VERIFIED: local computation]

| `first_omega_0` | max first-layer cycles | 1632 depth 1 | 1632 depth 2 | 851 depth 1 | 851 depth 2 |
|---|---|---|---|---|---|
| 30 (seed 42 only) | 0.7 | 0.841 | 0.355 | 0.803 | 0.744 |
| 240 | 5.5 | 0.064 | 0.015 | 0.170 | 0.085 |
| 480 | 10.9 | 0.016 | 0.015 | 0.084 | 0.084 |
| 819 | 18.6 | 0.015 | 0.022 | 0.084 | 0.091 |
| 1000 | 22.7 | 0.015 | 0.055 | 0.085 | 0.114 |
| 1200 | 27.3 | 0.015 | 0.104 | 0.086 | 0.152 |
| 1800 | 40.9 | 0.023 | 0.324 | 0.091 | 0.323 |
| 2400 | 54.6 | 0.110 | 0.518 | 0.132 | 0.440 |

Width scan at `first_omega_0` 819 and 1,000 (depth 1 / depth 2, same method):

| Width | Params (d1 / d2) | 1632 @819 | 1632 @1000 | 851 @819 | 851 @1000 |
|---|---|---|---|---|---|
| 128 | 19,593 / 36,105 | 0.075 / 0.327 | 0.081 / 0.430 | 0.223 / 0.391 | 0.207 / 0.450 |
| 256 | 71,945 / 137,737 | 0.015 / 0.022 | 0.015 / 0.055 | 0.084 / 0.091 | 0.085 / 0.114 |
| 384 | 157,065 / 304,905 | 0.004 / 0.005 | 0.005 / 0.007 | 0.046 / 0.048 | 0.045 / 0.052 |
| 512 | 274,953 / 537,609 | 0.003 / 0.002 | 0.002 / 0.002 | 0.038 / 0.027 | 0.027 / 0.029 |

**Recommendation.** Use `first_omega_0 = 1000` (max first-layer frequency 22.74 cycles per window, which is 1.22 times the 851 fundamental and 2.17 times the 1632 fundamental), inside the acceptable range 819 (the 851 fundamental, the minimum that satisfies D-05) to 1,200 (above which depth-2 features degrade). Do not choose 2,400 or more. At this value even a head-only fit on frozen initial features reaches 0.005 (1632) and 0.045 (851) on the proxy at depth 1, width 384, so a Tier-1 failure of the full Adam fit would not be a representational or bandwidth shortfall of the architecture. The proxy is not the real orbit, so this is a prior, not a certificate (A1). The logged step-0 `first_layer_frequency.max` must read at most 22.7364 and, with 384 uniform draws, at least 21.6 (0.95 of the bound; falling below it has probability about 3e-9); the CPU float64 seed-42 draw gave 22.734 and a median of 12.19 [VERIFIED: local computation, Appendix A.1]. A reading near 0.68 would mean the variant's `first_omega_0` did not reach the network.

**Depth and width (Claude's discretion; recommended).** Depth 1, width 384. Reasons: (i) in 5 of the 7 trained arms the h2 neighbour cosine is already near zero (0.017, -0.004, -0.000, -0.002, -0.000 for w060, w120, w240, w480, r1-4658; the other two read 0.351 for r1-1632 polish and 0.201 for r1-851 adam) [VERIFIED: 65-PROBE-RESULT.md:48-63], so depth 2 reaches the first collapsed layer and only depth 1 stays strictly below it; D-04's "2-layer limit keeps the network below the collapse depth" holds literally only at depth 1; (ii) depth 1 is flat across `first_omega_0` 480 to 1,800 where depth 2 is not; (iii) width 256 is borderline for 851 (0.084 against the 0.1 line) while 384 has margin; (iv) 157,065 parameters is 19.7 percent of the locked 795,657, so "fewer parameters" is unambiguous. Depth 1 also separates EXP-01 from EXP-02's locked-frequency 2-layer rung and gives EXP-04 a distinct "EXP-01 network".

**Parameter count (exact, from the production class, CPU float64)** [VERIFIED: local computation]: locked-12 = 795,657. The recommended variant is 157,065 = `input_layer.weight` (384, 14) 5,376 + bias 384 + `hidden_layers.0.siren.weight` (384, 384) 147,456 + bias 384 + `output_layer.weight` (9, 384) 3,456 + bias 9. The skip block's LayerNorm has no parameters (`layernorm_elementwise_affine` is `False`). There are 9,009 target numbers per orbit (1001 x 9), so the ratio is 17.4 parameters per target number.

### Pattern 2: The smallest harness extension (Q2)

**Why an edit to `diagnostic_fit.py` is unavoidable.** `validate_smoke_settings` resolves the registered variant with `variant = resolve_variant(variant_block["name"])` [diagnostic_fit.py:335], and `resolve_variant` for a string consults only the sealed catalog: `if variant not in REGISTRY:` ... `return REGISTRY[variant]` [diagnostic_variants.py:166-170]. `register_variant` returns a new immutable registry (`return MappingProxyType({**registry, variant.name: variant})` [:195]) and refuses duplicates (`if variant.name in registry:` [:190]); it cannot make a name resolvable by the sealed lookup. The call chain `_cmd_run` -> `require_committed_smoke_registration` -> `validate_smoke_settings` [diagnostic_fit.py:1456, 538-556, 554], `run_registered_smoke` [:1112-1115] and `verify_fit_result` [:1293-1296] all reach that one line, so a single change there admits the variant on every path.

**Recommended change set** (everything else is additive):

| File | Change | Lines |
|---|---|---|
| `pinn/verification/diagnostic_phase66.py` (new) | `EXP01_VARIANT = DiagnosticVariant(name="exp01-d1-w384-o1000", ...)`; `PHASE66_REGISTRY = register_variant(EXP01_VARIANT, into=REGISTRY)`; `REGISTRIES = MappingProxyType({"phase66": PHASE66_REGISTRY})`; `classify_exp01`, `confirm` (Pattern 5) | new |
| `pinn/verification/diagnostic_fit.py` | import `REGISTRIES`; helper `_named_registry(name)` (None -> the sealed `REGISTRY`); in `validate_smoke_settings` replace lines 334-337 with a registry-aware lookup; `fit_diagnostic(..., variant_registry=None)` records `"registered": resolved.name in registry` and `"registry"`; `run_registered_smoke` passes `settings.get("variant_registry")`; `verify_fit_result` checks the record's registry equals the registration's | about 25 |
| Existing four pins and `REGISTRY` | none | 0 |

A registration opts in with a new `settings.variant_registry` string (`"phase66"`). Absent or null (every Phase 65 registration) it resolves to the sealed `REGISTRY` object itself, so Phase 65 behaviour is unchanged, and a Phase 66 variant name then refuses as an unknown variant. Present but unknown or non-string it refuses. The registered-variant byte-agreement loop at [diagnostic_fit.py:338-343] runs unchanged against whichever registry was selected.

**What the edit costs, and what it does not.** The smoke registration lists these `code_dependencies` with SHA-256: `diagnostic_fit.py` `b00e45b4...34c2cd`, `diagnostic_guard.py` `8dd577a2...ef540`, `diagnostic_data.py` `47b9d99d...29836`, `diagnostic_variants.py` `ad8ed66c...cd5db`, `diagnostic_similarity.py` `e80079b6...d4b7` [VERIFIED: .planning/phases/65-probe-on-the-record-fit-harness/evidence/fit/smoke-registration.json code_dependencies]. Admission rejects a changed dependency: `on_disk = _sha256_file(root / relative_path)` / `if on_disk != recorded:` -> `"registration artifact changed since it was committed: "` [diagnostic_guard.py:405-409]. So after the edit, `check-registration` and `verify-result` on the Phase 65 smoke registration will refuse against the live tree. I confirmed both currently pass (`CHECK-REGISTRATION-OK registration-commit=ac4358cbe61159c0a4663c9e719f19a43182edfb`, `VERIFY-RESULT-OK`, this session). `65-CLOSEOUT.md:42-47` records the same effect for the probe registration and accepts it ("Historical `verify-result` passes; current `check-registration` correctly refuses"), and `:86-89` says a pinned-dependency change "must use a fresh registration; historical smoke evidence stays unchanged." No Phase 65 test reads the live smoke registration (the fit-admission tests build throwaway fixture repos with `_fit_registration_fixture`), and a grep of `tests/` for the five module file names found no hit. [VERIFIED: tests/phase65/test_fit_short.py:551-669, 716-733; grep this session] A regression run of the 204 Phase 65 tests after the edit is the proof. The four unedited modules stay byte-identical (provable by a test), and the Phase 65 evidence files stay unchanged (their 11 hashes are in `65-CLOSEOUT.md:127-139`). The plan must (a) record "the Phase 65 smoke registration is historical after the Phase 66 harness commit" in the Phase 66 closeout and (b) add `test_historical.py` so the historical identity is checked at the introducing commit (the pattern of `test_recorded_dependencies_match_the_historical_run_commit`, test_probe.py:1428-1465).

**Freeze rule.** Each Phase 66 registration pins `diagnostic_fit.py` and the two new modules by digest. Finish and commit all harness code before the first Phase 66 registration is written, and do not touch it afterwards; a later harness fix invalidates every earlier Phase 66 registration's live admission and forces fresh registrations.

**Tests the extension needs** (new package `tests/phase66/`, `__init__.py` mirroring `tests/phase65/__init__.py`; unittest; reuse `_fit_registration_fixture` and `_smoke_settings` from `tests/phase65/test_fit_short.py`, imported the way `test_contracts.py` imports `_loaded`):

| Class and test | Asserts |
|---|---|
| `test_catalog.Phase66CatalogTests.test_the_sealed_registry_is_unchanged_after_importing_phase66` | `list(REGISTRY) == ["locked-12"]`, `REGISTRY["locked-12"] is LOCKED_12`, item assignment raises `TypeError` |
| `...test_phase66_registry_is_a_register_variant_copy` | `PHASE66_REGISTRY is not REGISTRY`; names `["locked-12", "exp01-d1-w384-o1000"]`; `register_variant(EXP01_VARIANT)` against the sealed default leaves `REGISTRY` unchanged |
| `...test_duplicates_are_refused_in_both_directions` | re-registering `locked-12` or the EXP01 name raises `VariantRefused` |
| `...test_exp01_fields_match_the_page_and_are_below_locked` | depth 1, width 384, `first_omega_0 == 1000.0`, `hidden_omega_0 == 1.0`, lr `1e-4`, window `10.0`; `sum(p.numel())` from `build_variant` on CPU equals 157,065 and is less than 795,657 |
| `...test_exp01_builds_the_production_class_and_the_spec_stays_locked` | `isinstance(model, SQRSkipResNetSIREN)`; `model.input_layer.omega_0 == 1000.0`; `len(model.hidden_layers) == 1`; `ArchitectureSpec(hidden_depth=1)` still raises `ValueError` |
| `test_admission.Phase66AdmissionTests.test_a_committed_phase66_registration_admits` | fixture with `variant` = EXP01 JSON and `variant_registry="phase66"` passes `require_committed_smoke_registration` |
| `...test_the_same_variant_without_the_registry_key_refuses` | sealed default -> `DiagnosticFitRefused` |
| `...test_unknown_and_non_string_registry_names_refuse` | `"phase65"`, `""`, `7`, `["phase66"]` refuse; null behaves as the sealed default; locked-12 under `"phase66"` admits; EXP01 under the default or null refuses |
| `...test_variant_field_drift_refuses` | each of `name`, `time_features`, `depth`, `width`, `learning_rate`, `window_length`, `first_omega_0`, `hidden_omega_0` drifted from the registry entry |
| `...test_every_phase65_settings_refusal_still_applies` | the full `cases` dict of test_fit_short.py:811-834 re-run with the EXP01 variant (subTest) |
| `...test_cap_at_or_above_one_hour_still_refuses` | 3600 and 7200 refuse; 3599.5 passes the cap gate |
| `...test_scheduler_clipping_physics_polish_still_refuse` | the bounded smoke policy is intact |
| `...test_mps_without_mps_refuses` | `torch.backends.mps.is_available` patched to `False` |
| `test_records.Phase66RecordTests.test_fit_records_registry_and_registered_flag` | `fit_diagnostic(EXP01..., variant_registry="phase66")` -> `variant.registered is True`, `variant.registry == "phase66"`; default -> `registered is False` |
| `...test_record_has_input_and_h1_rows_scores_and_both_comparison_rows` | similarity rows `["input", "h1"]`; `scores.network`; `window_mean_constant` and `two_kepler` rows |
| `...test_verify_fit_result_checks_the_registry` | a record whose registry disagrees with the registration refuses; the Phase 65-shaped record (no `registry` key) still verifies |
| `test_historical.HistoricalPhase65Tests.test_four_unedited_pins_equal_the_recorded_digests` | live SHA-256 of `diagnostic_guard.py`, `_data.py`, `_variants.py`, `_similarity.py` equal the smoke registration |
| `...test_diagnostic_fit_matches_at_the_introducing_commit` | `git show <registration commit>:pinn/verification/diagnostic_fit.py` hashes to `b00e45b4...` |
| `...test_phase65_evidence_hashes_are_unchanged` | the 11 files of `65-CLOSEOUT.md:127-139` hash to the table |

Regression gate: `python -B -m unittest discover -s tests/phase65 -t .` must stay at 204 passing (about 33 s). [VERIFIED: 65-CLOSEOUT.md:105] Baseline this session: the registry and admission classes pass (24 tests, 7.06 s).

### Pattern 3: AC-power launch gate (Q3)

**Evidence.** On this Mac `pmset -g batt` prints `Now drawing from 'AC Power'` as its first line (byte check: `N o w   d r a w i n g   f r o m   ' A C   P o w e r ' \n`), then the battery line. [VERIFIED: command run this session] The Phase 60 precedent is `return "Battery Power" in _run(["pmset", "-g", "batt"]).stdout` with `except OSError: return False` [scripts/phase60_run_control.py:110-112], which is fail-open (a missing or unparseable `pmset` reads as "not on battery"), so it must not be the launch gate. `caffeinate -s` "prevent[s] the system from sleeping. This assertion is valid only when system is running on AC power" and `-i` prevents idle sleep. [CITED: man caffeinate(8), local] The Phase 60 launcher runs `[CAFFEINATE, "-is", PINNED_PYTHON, "-B", "-m", RUNNER_MODULE, _catalog_arm(arm_id)]` [launch_phase60_arm.py:120].

**Recommended design** (`pinn/verification/diagnostic_power.py`, new, no existing file edited):

- `power_source(text)`: match `^Now drawing from '([^']+)'$` on the first line only; return the quoted token or `None`.
- `require_ac_power(run=subprocess.run)`: run `["/usr/bin/pmset", "-g", "batt"]` with a timeout; refuse (raise a typed error) on `OSError`, nonzero exit, timeout, unparseable first line, or any source other than exactly `AC Power` (so `Battery Power` and `UPS Power` both refuse). Fail closed.
- `launch(registration, output)`: call `require_ac_power()`, write `power-gate.json` (checked UTC time, source, raw first line, repo-relative registration and output, load average) into the output directory, then `os.execv("/usr/bin/caffeinate", ["caffeinate", "-is", sys.executable, "-B", "-m", "pinn.verification.diagnostic_fit", "run", "--registration", R, "--output", O])`. The harness creates only `attempt.json`, `record.json` and `diagnostic.weights` in that directory, so the receipt does not collide; keep the home directory out of the receipt (the harness redaction guard refuses it in records; apply the same rule). Exit 2 with a plain message on refusal.
- Registered launch command: `python -B -m pinn.verification.diagnostic_power launch --registration R --output O`. Because the gate precedes `diagnostic_fit run`, a refusal happens before admission and before the attempt claim, so nothing is created; the harness is not modified for this.

**Composition and limits.** The gate checks at launch only (D-08). Runs under one hour need nothing more; `caffeinate -is` keeps the system awake while on AC. The gate is bypassable by calling `diagnostic_fit run` directly, so the pages and registrations state the launch command and the receipt makes compliance auditable. Mid-run unplugging is not governed here (A6).

**Tests** (`test_power.py`, no real `pmset`): AC first line passes; `Battery Power`, `UPS Power`, empty, garbage, a first line that is not `Now drawing from ...` with `'AC Power'` appearing later, nonzero exit, `FileNotFoundError`, timeout all refuse; `launch` on battery never calls `os.execv` nor `diagnostic_fit`; on AC it execs exactly the argv above (spy). The live check is an acceptance command at launch: `python -B -m pinn.verification.diagnostic_power check` -> exit 0 on AC. Scheduling: the owner's window is weekends only; a refusal on battery is a deferral to the next AC window, never a failure to be worked around. Today (2026-10-31) is a Saturday and the Mac is on AC.

### Pattern 4: Timing run, budget, and success criterion 1 (Q4)

**What the harness measures** (the Phase 65 smoke basis, unchanged): `timing.seconds_per_step` = sum of the measured synchronized update durations over the measured steps only (warmup, logging, scoring, setup, data load, publication excluded), `timing.end_to_end_seconds_per_completed_step` = total fit wall over completed steps, `timing.phases.{setup_seconds, logging_seconds, scoring_seconds, publish_seconds}` plus `data_load_seconds` added by the CLI. [VERIFIED: diagnostic_fit.py:939-971, 1164] The locked-12 smoke gave 0.014265412 s per measured step, 0.13597 s end to end, warmup 0.13147 s for 2 updates, logging 0.57212 s for 5 calls, scoring 1.21599 s, setup 0.52892 s, data load 0.25356 s, publication 0.01508 s; 18 steps "is not steady-state throughput". [VERIFIED: 65-FINDINGS.md:99-128; record.json timing block]

**Sequencing that satisfies criterion 1.** The page must "give ... the budget from the measured rate", and a measured rate for this variant can exist only after a run of it. So "committed before the first run" can only mean before the first experiment run; a timing run is an instrument calibration, not an experiment. Phase 65 set the precedent: `65-SMOKE-PREDICTION.md` plus `smoke-registration.json` were committed before the smoke ("the settings, the cap, the cadence and the reading rule are immutable after the run"). Recommended chain, enforced by git ancestry:

1. Commit `66-TIMING-PREDICTION.md` and `timing-registration.json` (mechanics and cost only: "no E value, tier, similarity figure or improvement is predicted or required"; the timing run's score is recorded but not read). Include in this never-amended page a **frozen design block**: the variant JSON, parameter count, the numeric band, the branch table, the repeats and confirmation rule. The scientific content is therefore committed before any run of any kind.
2. Run the timing launch; verify; commit the record.
3. Commit `66-PREDICTION.md` (the full page: repeats the design block verbatim, adds the budget computed from the timing record and cites its SHA-256) and the three experiment registrations. A test asserts the two pages agree on the design block.
4. Run the three experiments; verify each; commit each record.

The page is a separate file from the timing page because each registration pins its page by SHA-256 and admission re-checks it: amending the timing page after the timing registration would make the timing registration refuse live verification.

**Timing-run settings.** Same variant, seed 42, MPS float32, orbit `hierarchical/gold/1632`, window [0, 10], constant Adam 1e-4; 200 warmup plus 5,000 measured steps (5,200 total; the v2.4 floor was 50 and Phase 60 used 500-step timing runs); cadence `[0, 1300, 2600, 3900, 5200]` (five entries, like the smoke, so `logging_seconds/5` is a per-call cost); whole-run cap 600 s. [ASSUMED], A10. Expected duration is seconds to under a minute.

**Budget formula** (page text; the numbers come from the record). Let `s_m = timing.seconds_per_step`, `s_log = phases.logging_seconds / 5`, `T_fixed = data_load + setup + scoring + publish + process start-up (read from the launch wall time)`, `K` cadence entries, safety margin `m = 25 percent` (Phase 60's sustained rates, 0.0104 to 0.0116 s per step, were faster than the 500-step timed rate on six of seven arms, by up to about 14 percent, and slower on one by 1.4 percent [VERIFIED: 60-FINDINGS.md:93-105; percentages computed]; the margin is deliberately wider than anything observed), cap `C = 3,300 s` (strictly below 3,600). Choose the largest `N` with `T_fixed + warmup_seconds + (N - warmup)*s_m*(1+m) + K*s_log <= 0.75*C`, where `warmup_seconds` is the timing record's `timing.warmup_seconds`. Illustration only, with an assumed `s_m` of 4 ms (A2) and `T_fixed` 20 s: `N = floor((2475 - 20) / (1.25*0.004)) = 491,000`. The measured value replaces the assumption. The harness cannot extend or resume a run, so an "extension" is a fresh from-scratch run at double the steps (the same seed fixes the initialization; MPS float32 is not guaranteed bitwise reproducible), which fits under the hour only if the base run is about 25 minutes or less. Recommendation: no automatic extension rule; size one run to about 40 minutes, and report "still improving" (loss trace over the last quarter) as a description, not a branch. The `E` trace is not recorded (only the final E), unlike v2.4's every-100-steps scoring, so any such rule can only use the loss trace, which D-10 calls context. [VERIFIED: diagnostic_fit.py:917-928, 1008 `"loss": {"final": losses[-1], "trace": losses}`]

**Record size.** Canonical JSON is `indent=2` [VERIFIED: pinn/verification/evidence_io.py:131-142], so each loss-trace entry costs about 28 bytes and each similarity entry (two 1001-float arrays) about 66 KB (the 5-entry smoke record is 418,595 bytes). At 491,000 steps and 14 entries a record is about 14.7 MB; three runs are about 44 MB of committed JSON. Keep the cadence to about 14 entries and flag the size to the executor.

### Pattern 5: Prediction page contents (Q5)

Put these in `66-PREDICTION.md` (and the frozen subset in `66-TIMING-PREDICTION.md`). Numbers marked "rec." are the recommendation for the page author.

1. **Variant block** (machine-checkable JSON, compared with `EXP01_VARIANT.to_json_dict()` by a test): `{"name": "exp01-d1-w384-o1000", "time_features": "raw_tau_ic13", "depth": 1, "width": 384, "learning_rate": 0.0001, "window_length": 10.0, "first_omega_0": 1000.0, "hidden_omega_0": 1.0}`. The name matches `[a-z0-9][a-z0-9-]*` [VERIFIED: diagnostic_variants.py:50] and `raw_tau_ic13` is the only supported declaration [:56]. Stack: input SIREN 14 to 384 (omega 1000), one SQR-SkipResNet block 384 to 384 (omega 1.0, LayerNorm without affine), linear head 384 to 9, then the mass-weighted COM projection. Parameters 157,065 (19.7 percent of locked 795,657); per-tensor breakdown from Pattern 1.
2. **Bandwidth calculation** (Pattern 1) and the choice of 1,000, stated as covering the faster repeat system 851.
3. **What each suspect predicts** (D-09, with numbers):

| Suspect or lead | Predicts for the main run (1632, seed 42) | Observable |
|---|---|---|
| "Too small" | The 19.7 percent, 1-hidden-layer network does no better than the locked one: no Tier 1 (NEAR or BETWEEN) | `scores.network.E` |
| Working pipeline plus the depth-linked lead | Tier 1 | `E <= 0.1`; output movement near 1, not 0.003 |
| Pipeline defect (data to scorer, or recipe) | The constant-predictor band regardless of size | `E` within plus or minus 5 percent of the record's constant-predictor E; output movement about 0.003 [VERIFIED: 64-VERDICT.md:95] |
| "Metrics too harsh" | Not tested on `E` (Tier 1 uses `E` only). If a fit exists, `E` is passable and `eps_h` stays far above 1e-3, so Tiers 2 and 3 stay out of reach. Reported, not read. | `eps_h` (autograd, gold grid) |

   State the identifiability limit in plain words: a failure is predicted by both "too small" and "pipeline defect", so EXP-01 can refute "too small" (Tier 1) but cannot confirm it. A failed positive control routes to checking the data-to-scorer path first, which is exactly the pre-registered branch.
4. **Numeric reading rule** (inclusive edges; `E_const` is the record's own `comparisons[window_mean_constant].score.E`; the page numbers predict it to 1e-6; full-precision values are the Phase 64 CPU float64 entries `cpu.const.1632.E` and `cpu.const.851.E` [VERIFIED: .planning/phases/64-feasibility-verdict/evidence/numbers.json, parsed], and 1632's also appears as `comparisons[window_mean_constant].score.E` = 1.1538408194255343 in the Phase 65 smoke record):

| Branch | Rule | 1632 (E_const 1.1538408194255343) | 851 (E_const 1.233696866477104) |
|---|---|---|---|
| TIER1 | `scores.network.tier >= 1`, i.e. `E <= 0.1` (`"comparison": "inclusive_le"`, `{"E_max": 0.1, "eps_h_max": null, "tier": 1}` [feasibility_scorecard_v1.json:614, 626-630]) | `E <= 0.1` | `E <= 0.1` |
| NEAR (rec.) | `0.95*E_const <= E <= 1.05*E_const` | 1.096149 to 1.211533 | 1.172012 to 1.295382 |
| BETWEEN | `0.1 < E < 0.95*E_const` -> owner | 0.1 to 1.096149 | 0.1 to 1.172012 |
| OTHER | `E > 1.05*E_const` or non-finite, or the attempt is incomplete -> owner | above 1.211533 | above 1.295382 |

   Basis for plus or minus 5 percent (rec.): all 14 trained v2.4 states (7 arms x Adam and polish) lie between 0.005 percent and 0.586 percent above `E_const` (1632: 1.1539 to 1.1606; 851: 1.2375, 1.2384; 4658: 1.1432, 1.1439 against 1.1396) [VERIFIED: 60-FINDINGS.md:35-41, 66-73; 64-VERDICT.md:89-93; percentages computed], about eight times the largest observed deviation, while the two-Kepler formula (1632 E 0.9168, 20 percent below `E_const`) falls in BETWEEN. See A4. Boundary behaviour (0.1 exactly, the band edges) is fixed by `classify_exp01` and its tests.
5. **Branch table** (pre-registered, from `REQUIREMENTS.md:198-204` and the ROADMAP gate): TIER1 on 1632 -> "too small" refuted for one orbit; Phase 67 runs as planned. NEAR -> the lead does not explain the failure alone; the agent proposes an inserted Phase 66.1 checking the path from the data to the scorer. BETWEEN or OTHER -> the owner decides at checkpoint ①.
6. **Repeats and confirmation** (D-07): R1 = system 851 at seed 42, R2 = system 1632 at seed 41, both run whichever branch the main run lands in. Confirmed iff the main branch is TIER1 or NEAR and R1 and R2 land in that same branch; otherwise the disagreement goes to the owner with all three results.
7. **Budget** from the timing record (formula in Pattern 4); cap strictly below 3,600 s; same steps for all three runs; similarity cadence fixed (rec.: `0, 100, 300, 1000, 3000, 10000, 30000, 100000`, then evenly spaced to the final step, about 14 entries, because v2.4 E fell 25-fold to 48-fold in the first 5 percent of training [VERIFIED: 64-VERDICT.md:105]).
8. **Record readout** (Pattern 6) and the GAP-59-08 sentence: "`eps_h` here is the frozen scorer's autograd-velocity value on the gold grid; it is not the production gate's finite-difference value, GAP-59-08 (owner-routed, Phase 68) is open, and `eps_h` does not measure correctness for a near-constant predictor." [CITED: 65-FINDINGS.md:143-156; 64-VERDICT.md:83]
9. **Mechanical failure rule** (rec.): an incomplete attempt (power loss, cap expiry from an under-measured rate, interruption) is not a result; identical settings may be re-registered once under a new registration and a new output directory (the old directory's `attempt.json` is spent), with the same page. A cap expiry attributable to an under-measured rate is reported to the owner, not silently re-sized.
10. **Plain-language reading per branch** (for SC-3): TIER1 "a network one-fifth the size, one hidden layer, fits the orbit, so size is not what stopped v2.4; the data and scoring path can produce a passing fit"; NEAR "even a small network that should fit returns only the average position, so the fault is probably upstream of the network"; otherwise "the result sits between the lines; the owner decides".

### Pattern 6: Scoring path (Q6)

`fit_diagnostic` already does all of D-10; Phase 66 adds nothing. [VERIFIED: diagnostic_fit.py:916-929] Read these fields from each `record.json` and quote them in the review:

| Item | Field |
|---|---|
| Tier, E, eps_h | `scores.network.tier`, `.E`, `.eps_h` (frozen `score_network`, autograd velocities, gold grid, 1001 times) |
| Constant predictor | `comparisons[comparison == "window_mean_constant"].score.E` (zero velocities, same window) |
| Two-Kepler | `comparisons[comparison == "two_kepler"]`: `.score.E`, or `applicable: false` with `reason` (`NotApplicable` or solver non-convergence is a recorded outcome, never a score) |
| Neighbour similarity | `similarity.entries[*].layers[*].adjacent_cosine_mean` (rows `input`, `h1`), `first_layer_frequency.{median,max}`, `output_movement.value`, `output_rate_ratio.value` at the registered cadence |
| Loss (context) | `loss.final`, `loss.trace` |
| Timing | `timing.seconds_per_step`, `.end_to_end_seconds_per_completed_step`, `.phases.*` |
| Access | `access.reads`, `access.attestation`, `access.stage0` (one open, zero validation or test opens) |
| Variant identity | `variant` (name, fields, `registered`, `registry`), `seed`, `runtime`, `registration.sha256` |

The branch comes from one function, `classify_exp01(E, E_const)` returning `tier1 | near | between | other`, plus `confirm(main, r1, r2)`; both tested at the boundaries (E equal to 0.1, to each band edge, just inside and outside, NaN and infinity). Official `E` is the MPS float32 value the run records; in v2.4 the official E exceeded the CPU float64 constant-predictor E by only 0.0035 to 0.0038 [VERIFIED: 64-VERDICT.md:95], far inside the 5 percent band, so the runtime difference cannot move a branch except at a knife edge.

### Pattern 7: SCOPE-48 conditions if a run at or above one hour were registered (Q7)

Runs under one hour are preferred and need none of this. A run at or above one hour would need, in order:

1. *The cap refusals stay.* `HOUR_SECONDS = 3600.0` [diagnostic_fit.py:134] gates `validate_smoke_settings` (`not 0 < float(cap) < HOUR_SECONDS` [:409-410]) and `fit_diagnostic` (`not 0 < float(deadline_seconds) < HOUR_SECONDS` [:813]); tests `test_cap_at_or_above_one_hour_refuses_before_any_access` (test_fit_short.py:790) and `test_a_deadline_at_or_above_one_hour_is_refused` (:1006). They are not loosened (D-08, 65-CLOSEOUT.md:90-91); a governed path would be a separate, explicitly named code path.
2. *Pause and resume do not exist for the diagnostic fit.* The worker converts only SIGTERM, into an incomplete attempt that publishes nothing (`_WorkerTerminated`, `_smoke_worker` [diagnostic_fit.py:1202-1243]); there is no checkpoint, no SIGINT path and no `--resume`; the contract says an attempt is "never retried, extended or resumed" (smoke-registration reading rule). The Phase 60 pattern is SIGINT to the arm's process, exit 130, then `--resume` from a checkpoint (`GOVERNED_STOP_CODES = (129, 130, 143)`, `PAUSE_SIGNAL = signal.SIGINT` [phase60_run_control.py:58-59]).
3. *The Phase 60 control scripts are hard-wired to the Phase 60 launcher*: `EVIDENCE = ROOT / ".planning/phases/60-single-system-learnability/evidence"`, `LAUNCHER = EVIDENCE / "launch_phase60_arm.py"`, `LAUNCH_ROOT = ROOT / "runs/.launch/phase60"`, `ARM_RUNS = ROOT / "runs/phase60"`, `CONTROL = ROOT / "runs/.phase60-control"` [:48-52]. A Phase 66 run is invisible to `running_sequences()`, so the guard would never pause it. The guard also pauses once when the clock passes 09:00 (`DAILY_PAUSE = (9, 0)` [:63]), which would interrupt a weekend run that spans 09:00. `tests/phase60/test_resume.py` and the pinned `pinn/verification/learnability_run.py` reference these scripts [VERIFIED: grep this session], so a Phase 66 control layer should be separate rather than an edit to the Phase 60 one.
4. *Compatibility is proven before registration*: a synthetic pause, exit, resume, complete cycle for the new run type and a guard that recognises it, with tests, before any such registration is committed.
5. *Unchanged scope rules*: Mac only (no cloud route costed or proposed), budget from the measured rate, and Stage-0 TRAIN-only access. [VERIFIED: .planning/REQUIREMENTS.md:183]

Effort is substantial (new checkpoint and resume in the fit, a new launcher and guard). That is the reason to size the runs under one hour.

### Anti-Patterns to Avoid
- **Re-using the Phase 65 smoke registration or editing it** to cover Phase 66; D-11 requires fresh registrations and unchanged Phase 65 artifacts.
- **Amending a page after a registration pins it.** The registration's `page.sha256` is re-checked on admission.
- **A zero-edit shim or global rebinding** to dodge the digest effect (Pattern 2).
- **Using the fail-open `on_battery()`** as a launch gate.
- **Defining "near the constant predictor" after seeing a result**, or with a hand-typed constant instead of the record's own `E_const`.
- **Deriving a budget from `end_to_end_seconds_per_completed_step` of a short timing run**; it includes the fixed costs. Use `seconds_per_step` plus explicit fixed terms.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Fitting, scoring, comparison rows, similarity, exclusive records | A new training or scoring loop | `fit_diagnostic` and the `diagnostic_fit` CLI | Frozen scorer, marker, exclusivity, deadline and Stage-0 isolation are already tested. |
| Variant construction | A new network class | `build_variant` (production `SQRSkipResNetSIREN`) | Keeps `locked-12` parity and the architecture locks. |
| Registry growth | Editing `REGISTRY` | `register_variant(..., into=REGISTRY)` | Returns a copy, refuses duplicates. |
| Registration admission and pins | A second admission path | `require_committed_registration` and `validate_smoke_settings` | Digest, ancestry, receipt, cap, cadence and policy refusals. |
| Power state parsing | Scattered ad hoc `pmset` greps | One strict `power_source` / `require_ac_power` | Fail-closed, tested once. |
| Reading-rule arithmetic | Hand classification in the review | `classify_exp01` and `confirm` | Boundaries fixed before results. |
| Keeping the Mac awake | Custom sleep handling | `/usr/bin/caffeinate -is` | Phase 60 precedent; AC-scoped by the OS. |
| Pause, resume, power guard for 1h+ | Copying `phase60_run_control.py` | Nothing now; stay under one hour | Coupled to the Phase 60 launcher. |

**Key insight:** every guarantee this phase needs (isolation, exclusivity, frozen scoring, digest-pinned provenance) is already built and tested in Phase 65; the work is to admit one more named design through the existing door without weakening it.

## Common Pitfalls

### Pitfall 1: A pinned file changes after the registration is committed
**What goes wrong:** admission refuses with "registration artifact changed since it was committed" [diagnostic_guard.py:407-409], or "untracked or dirty" for an uncommitted edit. **Why:** the registration pins code, page, receipt and frozen files by SHA-256 and requires them tracked and clean. **Avoid:** finalize and commit code and pages, then compute digests, then write and commit the registration, then run; code freeze before the first registration. **Warning sign:** `check-registration` fails after any edit.

### Pitfall 2: The Phase 65 smoke registration stops admitting
**What goes wrong:** `check-registration` and `verify-result` on the smoke registration refuse once `diagnostic_fit.py` changes. **Why:** it pins that file's digest. **Avoid:** accept and document it (Pattern 2), add the historical-bytes test, do not edit the registration. **Warning sign:** a plan task that "fixes" the smoke registration.

### Pitfall 3: A cap expiry wastes the AC window
**What goes wrong:** an under-measured rate exceeds the cap; the supervisor terminates; the attempt is incomplete and publishes nothing. **Why:** the cap covers admission through publication and is enforced twice. **Avoid:** the 25 percent margin, the 0.75*C target, and a timing run that is long enough (5,000 measured steps). **Warning sign:** a measured rate from fewer than a few hundred steps.

### Pitfall 4: A burned output directory
**What goes wrong:** a second attempt in the same directory refuses at `attempt.json` (`O_EXCL`). **Avoid:** distinct output directories per run role and seed, and a new registration for a permitted retry. Note `run_id` is `<variant>-<record slug>` and does not include the seed, so use directory names with role and seed.

### Pitfall 5: Reading the wrong constant-predictor number
**What goes wrong:** a band built from a 4-digit figure or a different window. **Avoid:** the band edges come from the record's own `E_const`; the page numbers are predictions of it (1632: 1.1538408194255343, identical in the Phase 65 smoke record and in Phase 64's CPU float64 re-derivation; 851: 1.233696866477104 from Phase 64).

### Pitfall 6: Over-large `first_omega_0`
**What goes wrong:** at 2,400 or more the initial features degrade (Pattern 1) and the end-of-training bandwidth scales toward the Nyquist limit. **Avoid:** the range 819 to 1,200 and a step-0 check that the logged `first_layer_frequency.max` matches `omega_0/(14*pi)`.

### Pitfall 7: Record and commit weight
**What goes wrong:** about 14.7 MB per record at about 491,000 steps. **Avoid:** about 14 cadence entries; commit only the record, weights, attempt and receipt per run; tell the executor in the plan. The estimate is [ASSUMED] A7 until the timing record shows the actual size.

### Pitfall 8: Concurrent heavy jobs perturb timing
**What goes wrong:** memory pressure or other MPS work changes the rate (Phase 60 measured under swap, 60-FINDINGS.md:118). **Avoid:** nothing else heavy during the timing run and the three experiments; the receipt records the load average.

### Pitfall 9: Verifier hardening gaps
`65-CLOSEOUT.md:74-75` defers WR-03 (malformed result CLI exceptions: "Before expanding these CLIs beyond the known committed records, test and normalize malformed/missing/unmarked-result refusals") and WR-04 (record-supplied verification paths: "Current committed records use the expected paths"). Phase 66 runs `verify-result` on records its own harness just wrote at registered paths, which stays inside that wording on a reasonable reading; the plan should say so explicitly. If the planner prefers, the two fixes with regression tests are cheap while `diagnostic_fit.py` is open, but they enlarge the diff (A9).

### Pitfall 10: Hand-maintained state
`STATE.md` is edited by hand here; do not use `gsd-tools` mutating verbs on it. [VERIFIED: STATE.md:50-51]

## Code Examples

Sketches only; the executor writes and tests the real code.

### Registry-aware lookup in `validate_smoke_settings` (replaces diagnostic_fit.py:334-337)
```python
# Source: derived from diagnostic_fit.py:334-343 and diagnostic_variants.py:166-195
def _named_registry(name):
    if name is None:
        return REGISTRY                      # exactly the Phase 65 behaviour
    if not isinstance(name, str) or name not in REGISTRIES:
        raise DiagnosticFitRefused(
            f"unknown variant registry {name!r}; known: {list(REGISTRIES)}")
    return REGISTRIES[name]

registry = _named_registry(settings.get("variant_registry"))
variant_name = variant_block["name"]
if variant_name not in registry:
    raise DiagnosticFitRefused(
        f"unknown diagnostic variant {variant_name!r}; registered: {list(registry)}")
variant = registry[variant_name]             # then the unchanged byte-agreement loop
```

### Catalog module
```python
# Source: diagnostic_variants.register_variant semantics (new copy, duplicates refused)
EXP01_VARIANT = DiagnosticVariant(
    name="exp01-d1-w384-o1000", time_features="raw_tau_ic13", depth=1, width=384,
    learning_rate=1e-4, window_length=10.0, first_omega_0=1000.0)
PHASE66_REGISTRY = register_variant(EXP01_VARIANT, into=REGISTRY)
REGISTRIES = MappingProxyType({"phase66": PHASE66_REGISTRY})
```

### Strict power parse
```python
_SOURCE = re.compile(r"^Now drawing from '([^']+)'$")
def power_source(text):
    first = text.splitlines()[0] if text else ""
    m = _SOURCE.match(first)
    return m.group(1) if m else None          # require_ac_power: source == "AC Power", else refuse
```

### Reading rule
```python
def classify_exp01(e, e_const, band=0.05):
    if not math.isfinite(e): return "other"
    if e <= 0.1: return "tier1"
    if (1 - band) * e_const <= e <= (1 + band) * e_const: return "near"
    return "between" if e < (1 - band) * e_const else "other"
```

### Evidence-order check (run by the executor after the evidence exists)
```bash
first() { git log --diff-filter=A --format=%H -1 -- "$1"; }
anc()   { git merge-base --is-ancestor "$1" "$2"; }
anc "$(first <timing page>)" "$(first <timing registration>)" && anc "$(first <timing registration>)" "$(first <timing record>)" \
 && anc "$(first <timing record>)" "$(first 66-PREDICTION.md)" && anc "$(first 66-PREDICTION.md)" "$(first <each experiment registration>)" \
 && anc "$(first <each experiment registration>)" "$(first <its record>)"
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| One registry, locked-12 only | Sealed catalog plus a `register_variant`-derived copy per phase, selected by a registration-declared name | Phase 66 | Later phases add variants without touching the sealed catalog. |
| Negative power check (`"Battery Power" in stdout`) | Positive, fail-closed parse of the first line | Phase 66 | A missing or garbled `pmset` can no longer read as safe. |
| Budget from a 500-step wall-time timing run (v2.4) | Registered timing run with the synchronized, warmup-excluded basis plus fixed-cost terms | Phase 65 harness | Fixed costs no longer inflate the per-step rate. |
| SIREN default `omega_0 = 30` | Frequency scaled to the input dimension and the signal (here `omega_0/14` is the first-layer ceiling) | Phase 66 research | The 13 constant IC inputs dilute the time weight 14-fold. [CITED: 3d.bk.tudelft.nl/nail/siren for the default 30 and the first-layer init] |

**Deprecated or outdated:** the Phase 60 power guard for diagnostic runs (it only sees Phase 60 sequences); the `on_battery()` helper as a launch gate.

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | The Kepler-proxy harmonic counts (n = 4 and 6) and the synthetic readout errors transfer to the real 1632 and 851 orbits; eccentricity is estimated from census separation extrema | Pattern 1 | The usable `first_omega_0` window shifts; mitigated by the flat plateau and by margin at width 384. |
| A2 | The 1-hidden-layer network runs in roughly 3 to 6 ms per step (launch-bound; locked-12 is 14 ms with 28 parameter tensors and 13 sine layers, this has 6 tensors and 2 sine layers) | Pattern 4 | Only the illustrative step count changes; the timing run replaces it. |
| A3 | The v2.4 first-layer drift (trained median about 0.13 to 0.18 of `omega_0` cycles) recurs in the shallow network; its cause is weight diffusion rather than frequency seeking | Pattern 1 | Secondary argument against very large `omega_0` weakens; the range is justified without it. |
| A4 | The plus or minus 5 percent two-sided band, with OTHER including large `E` | Pattern 5 | The owner may prefer another width; BETWEEN and OTHER both route to the owner, so a mis-set band changes routing, not safety. |
| A5 | `pmset -g batt` keeps the `Now drawing from '...'` first line on other macOS versions | Pattern 3 | The gate refuses (fail-closed), never mis-permits. |
| A6 | `caffeinate -is` keeps a sub-hour run alive on AC; a mid-run unplug is not handled | Pattern 3 | An unplugged run may sleep or stall; it ends incomplete at the cap, not wrong. |
| A7 | About 28 bytes per loss entry and 66 KB per similarity entry | Pattern 4 | Record size estimate only. |
| A8 | No automatic extension rule is recommended | Pattern 4 | A "still improving" run needs an owner-approved follow-up at checkpoint ①. |
| A9 | Editing `diagnostic_fit.py` (and leaving WR-03 and WR-04 deferred) is acceptable under the delegation | Pattern 2, Pitfall 9 | If the owner objects to the Phase 65 smoke registration going historical, the only alternative is the 300-line clone. |
| A10 | The timing run length (200 plus 5,000 steps) and the 25 percent margin suffice | Pattern 4 | A wasted AC window if the sustained rate is worse than 25 percent below the timed rate. |
| A11 | Depth 1, width 384, `first_omega_0` 1,000 are the right discretionary choices | Pattern 1 | A near-constant result would be partly attributable to a poor setting; the pre-registered branches still apply. |

## Open Questions (RESOLVED)

Every question below has a recorded disposition from planning (plans 66-01 to 66-05, revision 1). None is open.

1. **Final architecture numbers.** What we know: the evidence above favours depth 1, width 384, `first_omega_0` 1,000 (acceptable 819 to 1,200). What is unclear: no real-orbit confirmation is allowed during research. Recommendation: fix these on the page; the planner may widen to 512 if more margin on 851 is wanted (274,953 parameters, 34.6 percent of locked).
   **RESOLVED:** depth 1, width 384 and `first_omega_0` 1,000 are fixed in `EXP01_VARIANT` (plan 66-01) and frozen on the timing page (plan 66-03). Width 512 was not adopted: 384 already reads 0.045 on 851 against the 0.1 line, and the smaller network keeps "fewer parameters" unambiguous. The remaining uncertainty (A1, A11) is handled on the timing page. Its setting checks (the census arithmetic and the step-0 first-layer bound) and its improvement check make any non-Tier-1 run that fails them read unsettled, and such a run goes to the owner. The page states that capacity on the real orbit is the "too small" question itself.
2. **Optional hedge, not recommended by default:** a head-only closed-form fit of this architecture on the real 1632 record (seconds on CPU) would turn the synthetic prior into a real-data capacity check before spending weekend compute. It needs a Stage-0 TRAIN read and its own registration and prediction, and it pre-empts part of what EXP-01 tests; the known-answer scorer checks belong to YARD-01 (Phase 68).
   **RESOLVED (not adopted):** it would need its own Stage-0 read, registration and prediction, and it pre-empts part of what EXP-01 tests. Instead, the frozen timing page pre-registers the reading safeguards (plans 66-02 and 66-03). A non-Tier-1 run that was still improving when its steps ran out, judged by the DIAG-09 output movement rather than the loss, reads unsettled and goes to the owner at checkpoint ①, never to the 66.1 proposal. A non-Tier-1 run whose step-0 bandwidth check fails also reads unsettled; a Tier-1 run that fails it reads out-of-branch. Both go to the owner.
3. **Where to record the Phase 65 smoke registration's historical status.** Recommendation: the Phase 66 closeout, not `65-CLOSEOUT.md` (a Phase 65 artifact that must stay unchanged).
   **RESOLVED:** it is recorded in Phase 66's own artifacts: 66-01-SUMMARY.md (the last live passes and the first live refusals), the timing page's "Harness provenance" (plan 66-03) and 66-RESULT.md (plan 66-05). `65-CLOSEOUT.md` stays byte-identical, which `tests/phase66/test_historical.py` checks (plan 66-01).
4. **Weekend scheduling.** The first available AC window is the current weekend if planning finishes in time; otherwise the next. Stage all non-compute work (harness, tests, pages, registrations) first so all four compute launches fit one window. A battery refusal defers, never bypasses.
   **RESOLVED:** all non-compute work is staged first (plans 66-01 to 66-03). The launch gate refuses in code on battery and outside the owner's window (Saturday, or Sunday before 22:00, America/Chicago), so a refusal defers and never bypasses (plan 66-02). Each launch runs detached in its own session after a survival test (plans 66-03 and 66-04).
5. **Phase 67 reuse.** Phase 67 will register more variants. Decide in Phase 67 whether to add a module and a table entry (which invalidates Phase 66 registrations' live admission, by design) or to restructure the table.
   **RESOLVED (deferred to Phase 67 by design):** Phase 66 adds exactly one table entry, `REGISTRIES["phase66"]` (plan 66-01). How Phase 67 extends the table is decided in Phase 67's own planning; it is not a Phase 66 decision.
6. **Commit weight of three roughly 15 MB records.** Flag to the owner or executor; no tooling change recommended.
   **RESOLVED:** removed at the source by a pre-freeze harness change inside the Phase 66 extension (plan 66-01, Site F). A registration-declared loss-trace stride of ceil(N / 10,000) keeps at most 10,001 loss entries, and the bounded similarity cadence keeps at most 14 entries (plan 66-02). Every record therefore stays far below the 10 MiB staged-blob limit at any step count the time budget allows. Run length is set by time alone (D-08), and `MAX_BLOB_BYTES` and the commit policy are unchanged.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Python (pinn-train) | harness, tests | yes | 3.11.15 | none needed |
| torch with MPS | the four compute runs | yes (`mps.is_available()` True) | 2.12.1 | none; runs refuse without MPS rather than fall back (diagnostic_fit.py:355-363) |
| numpy | scorer, tests | yes | 2.4.6 | none |
| `/usr/bin/pmset` | AC gate | yes | Darwin 25.5.0 | none; the gate refuses if absent |
| `/usr/bin/caffeinate` | keep awake on AC | yes | Darwin 25.5.0 | run without it; risk of idle sleep |
| git | admission, ancestry checks | yes | 2.54.0 | none |
| `scripts/agent-commit`, `.githooks` | commits | yes | in repo; `core.hooksPath=.githooks` | none |
| AC power at launch time | all compute | yes now (`Now drawing from 'AC Power'`, 100 percent, charged, Saturday 2026-10-31) | owner window: weekends only | defer to the next weekend |
| Apple M5 Pro, 24 GB | timing and runs | stated in PROJECT.md Constraints | not probed | none (Mac only, SCOPE-48) |

**Missing dependencies with no fallback:** none. **With fallback:** `caffeinate` (optional).

## Validation Architecture

(`workflow.nyquist_validation` is `true` in `.planning/config.json`.)

### Test Framework
| Property | Value |
|----------|-------|
| Framework | Python standard-library `unittest`, pinn-train environment |
| Config file | none (same convention as Phase 65) |
| Quick run command | `<home>/miniforge3/envs/pinn-train/bin/python -B -m unittest discover -s tests/phase66 -t .` |
| Full suite command | `<home>/miniforge3/envs/pinn-train/bin/python -B -m unittest discover -s tests/phase65 -t .` then the quick run (Phase 65: 204 tests, about 33 s; it includes one MPS parity test) |

### Phase Requirements to Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| EXP-01 / SC-1 | Variant registered through `register_variant` into a copy; sealed `REGISTRY` unchanged; duplicates refused | unit | `... -m unittest tests.phase66.test_catalog` | no, Wave 0 |
| EXP-01 / SC-1 | Page variant JSON and parameter count equal the production-class computation; page and timing page agree on the design block; band numbers equal 0.95 and 1.05 times the E_const constants | static | `... -m unittest tests.phase66.test_pages` | no, Wave 0 |
| EXP-01 / SC-1 | Registrations admit; all Phase 65 refusals apply; unknown registry refuses; cap at 3600 refuses | unit (fixture repos) | `... -m unittest tests.phase66.test_admission` | no, Wave 0 |
| EXP-01 / SC-1 | AC gate fail-closed; launch order | unit (fakes) | `... -m unittest tests.phase66.test_power` | no, Wave 0 |
| EXP-01 / SC-2 | Record carries registry, rows `input` and `h1`, scores, both comparison rows; verify checks the registry | unit (synthetic corpus) | `... -m unittest tests.phase66.test_records` | no, Wave 0 |
| EXP-01 / SC-2, SC-3 | `classify_exp01` and `confirm` at every boundary | unit | `... -m unittest tests.phase66.test_reading_rule` | no, Wave 0 |
| Phase 65 preserved | Four unedited pins and the 11 evidence hashes unchanged; `diagnostic_fit.py` matches at the introducing commit | unit (git) | `... -m unittest tests.phase66.test_historical` | no, Wave 0 |
| Phase 65 preserved | The 204 Phase 65 tests still pass | regression | full suite command above | yes |
| EXP-01 / SC-1 | Page, then registration, then record ancestry holds for the timing run and each experiment | git verification (after evidence exists) | evidence-order snippet in Code Examples | executor-run |
| EXP-01 / SC-2 | Each record verifies against its registration | CLI | `... -m pinn.verification.diagnostic_fit verify-result --registration R --result record.json` (expect `VERIFY-RESULT-OK`, exit 0) for the timing run and all three runs | executor-run |
| EXP-01 / SC-2 | Step-0 `first_layer_frequency.max` lies in [21.6, 22.7364]; `E` classification and confirmation printed from the three records | scripted check | a short `python -B` snippet over the records using `classify_exp01` | executor-run |
| EXP-01 / SC-3 | `66-REVIEW.md` contains the branch, a plain-language reading, and any SCOPE-49 proposal with the owner's answer, and cites record digests | structure check, plus manual | grep for the required headings; the owner's answer is manual-only (a human decision) | executor-run, manual |

### Sampling Rate
- **Per task commit:** the closest `tests.phase66` module (seconds).
- **Per wave merge:** all of `tests/phase66` plus all of `tests/phase65`.
- **Phase gate:** both suites green, `check-registration` and `verify-result` for every Phase 66 registration and record, and the evidence-order check, before `/gsd-verify-work`.

### Wave 0 Gaps
- [ ] `tests/phase66/__init__.py`, `test_catalog.py`, `test_admission.py`, `test_records.py`, `test_reading_rule.py`, `test_power.py`, `test_pages.py`, `test_historical.py`
- [ ] `pinn/verification/diagnostic_phase66.py`, `pinn/verification/diagnostic_power.py` (created test-first)
- [ ] No framework install; no change to `tests/phase65`.

## Security Domain

`security_enforcement` is absent from the config, so it is treated as enabled.

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | no | single-user local tool |
| V3 Session Management | no | none |
| V4 Access Control | yes (data access) | Stage-0 TRAIN-only guarded reader, refusals before any open, process attestation (unchanged) |
| V5 Input Validation | yes | strict registration validation: whitelist lookup of `variant_registry`, type checks, byte-agreeing variant block, name regex |
| V6 Cryptography | yes (integrity only) | SHA-256 digest pins and exact-byte checks via the existing helpers; no new crypto |
| V10 Malicious Code / V14 Configuration | yes | no new dependencies; fixed-argv `subprocess` for `pmset` and `caffeinate`, never `shell=True` |

### Known Threat Patterns for this stack

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Registration or page edited after commit | Tampering | committed-clean plus exact digest admission (guard:397-410) |
| A variant smuggled in by a crafted registry name | Tampering | closed `REGISTRIES` table; byte-agreement with the entry; unknown name refuses |
| Command injection through paths | Elevation | fixed argv; paths passed as list items; repo-relative validation (`_one_entry`) |
| Record points verification at an arbitrary file (WR-04) | Information disclosure | deferred hardening (Pitfall 9); records are harness-written at registered paths |
| Running a graded or evaluator path on a diagnostic artifact | Tampering | existing intrinsic marker and entry-point refusals (Phase 65), top-level marker written by `fit_diagnostic` (WR-01 is a graded-use precondition only) |
| Spoofed power state | Spoofing | not a security boundary; the receipt makes the check auditable |
| Home-directory path in committed JSON | Information disclosure | repo-relative paths in the receipt; harness redaction guard for records |

## Sources

### Primary (HIGH confidence)
- Repository files read this session: `pinn/network.py`, `pinn/architecture_spec.py`, `pinn/constants.py`, `pinn/verification/diagnostic_fit.py`, `diagnostic_variants.py`, `diagnostic_guard.py`, `diagnostic_data.py`, `diagnostic_similarity.py`, `pinn/verification/artifacts/feasibility_scorecard_v1.json`, `scripts/phase60_run_control.py`, `.planning/phases/60-single-system-learnability/evidence/launch_phase60_arm.py`, `tests/phase65/*` (patterns), `.planning/phases/65-probe-on-the-record-fit-harness/{65-CONTEXT,65-CLOSEOUT,65-FINDINGS,65-SMOKE-PREDICTION,65-PROBE-RESULT,65-VALIDATION}.md` and `evidence/fit/smoke-registration.json`, `.planning/phases/59-.../evidence/census/{panels.json,census.csv}`, `.planning/phases/60-single-system-learnability/60-FINDINGS.md`, `.planning/phases/64-feasibility-verdict/64-VERDICT.md` and `evidence/numbers.json`, `.planning/{REQUIREMENTS,STATE,PROJECT,ROADMAP,config}`.
- Local runs this session (no training, no Stage-0 data, no MPS): instantiation of the production class on CPU; the Kepler harmonic estimate; the closed-form readout probes; `pmset -g batt`; `check-registration` and `verify-result` on the Phase 65 smoke; 24 registry and admission tests (Appendix A).
- Local manual pages: `man caffeinate`, `man pmset`.

### Secondary (MEDIUM confidence)
- [Gentle Introduction to SIREN](https://3d.bk.tudelft.nl/nail/siren) and [SirenPose, arXiv 2512.20531](https://arxiv.org/pdf/2512.20531) for the default `omega_0 = 30` and the `U[-1/n, 1/n]` first-layer init (search summary; the repository's `network.py` is authoritative).

### Tertiary (LOW confidence)
- A claim that SIREN audio fitting uses `omega_0 = 3000` could not be confirmed by search and is not used.

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH, every component exists and was exercised.
- Architecture (harness extension, gate, sequencing): HIGH on mechanics, MEDIUM on the Phase 65 smoke disposition (a judgment under delegation).
- Variant numbers (`first_omega_0`, depth, width): MEDIUM, synthetic proxy.
- Pitfalls: HIGH for the digest and cap mechanics, MEDIUM for timing behaviour.

**Research date:** 2026-10-31
**Valid until:** 2026-11-30, or until any of the five Phase 65 pinned modules or the frozen scorer changes.

## Appendix A: Re-derivation scripts (no training, no Stage-0 data, no MPS)

Run from the repository root with `<home>/miniforge3/envs/pinn-train/bin/python -B`; they import only the production network through the harness and the committed census numbers. The session ran fuller versions from the session scratchpad; these are the load-bearing parts.

```python
# A.1 parameter counts and first-layer frequency (cycles per window) at initialization
import math, sys, torch
sys.path.insert(0, ".")
from pinn.verification.diagnostic_variants import DiagnosticVariant, build_variant, LOCKED_12
def mk(depth, width, w0): return DiagnosticVariant(name="x", time_features="raw_tau_ic13", depth=depth,
        width=width, learning_rate=1e-4, window_length=10.0, first_omega_0=float(w0))
cpu = torch.device("cpu")
n = lambda v: sum(p.numel() for p in build_variant(v, seed=42, dtype=torch.float64, device=cpu).parameters())
print(n(LOCKED_12), n(mk(1, 384, 1000)), n(mk(2, 256, 30)))        # 795657 157065 137737
m = build_variant(mk(1, 384, 1000), seed=42, dtype=torch.float64, device=cpu)
f = m.input_layer.weight[:, 0].detach().abs() * 1000.0 / math.pi
print(float(f.median()), float(f.max()), 1000.0 / (14 * math.pi))   # max <= 22.736
```

```python
# A.2 Kepler-proxy harmonic need (inputs: census N_in and rough eccentricity from sep extrema)
import math, numpy as np
def kepler_E(M, e):
    E = M + e * np.sin(M)
    for _ in range(60): E = E - (E - e * np.sin(E) - M) / (1.0 - e * np.cos(E))
    return E
def need(e, tol, n=1 << 14):
    M = np.linspace(0, 2 * np.pi, n, endpoint=False); E = kepler_E(M, e)
    comps = [np.cos(E) - e, math.sqrt(1 - e * e) * np.sin(E)]
    for nc in range(1, 200):
        err = max(np.max(np.abs(np.fft.irfft(np.where(np.arange(n // 2 + 1) <= nc, np.fft.rfft(c), 0), n=n) - c)) for c in comps)
        if err / (1 + e) <= tol: return nc
print(need(0.768, 0.1), need(0.854, 0.1))                             # 4 6
```

```python
# A.3 closed-form readout on INITIAL hidden features (the head is linear): max error / (1+e)
import math, sys, numpy as np, torch
sys.path.insert(0, ".")
from pinn.verification.diagnostic_variants import DiagnosticVariant, build_variant
DT, CPU = torch.float64, torch.device("cpu")
def target(tau, N, e):
    M = 2 * np.pi * N * (tau + 1) / 2
    E = M + e * np.sin(M)
    for _ in range(80): E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    return np.stack([np.cos(E) - e, math.sqrt(1 - e * e) * np.sin(E)], 1)
def readout_error(depth, width, w0, N, e, seed=42, ic_seed=7):
    tau = np.linspace(-1, 1, 1001)
    ic = torch.tanh(torch.randn(13, dtype=DT, generator=torch.Generator().manual_seed(ic_seed)))
    X = torch.cat([torch.as_tensor(tau, dtype=DT).reshape(-1, 1), ic.reshape(1, 13).expand(1001, 13)], 1)
    v = DiagnosticVariant(name="p", time_features="raw_tau_ic13", depth=depth, width=width,
                          learning_rate=1e-4, window_length=10.0, first_omega_0=float(w0))
    model = build_variant(v, seed=seed, dtype=DT, device=CPU)
    with torch.no_grad():
        a = model.input_layer(X)
        for layer in list(model.hidden_layers)[:depth]: a = layer(a)
    A = torch.cat([a, torch.ones(1001, 1, dtype=DT)], 1); Y = torch.as_tensor(target(tau, N, e), dtype=DT)
    sol = torch.linalg.lstsq(A, Y, driver="gelsd").solution
    return (A @ sol - Y).abs().max().item() / (1 + e)
print(readout_error(1, 384, 1000, 10.471994, 0.768), readout_error(1, 384, 1000, 18.612048, 0.854))   # ~0.005 ~0.045
```
