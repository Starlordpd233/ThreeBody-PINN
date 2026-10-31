# Phase 66: Small-Network Control - Context

**Gathered:** 2026-10-31
**Status:** Ready for planning
**Decision source:** The standing owner delegation in `.planning/PROJECT.md`,
Context (2026-10-28). The agent resolved the technical and scientific areas
below from the milestone contracts, the Phase 59-65 records and the production
network source. One owner-authority question was asked: how much Mac time the
phase may use. The answer is recorded verbatim in D-08.

<domain>
## Phase boundary

Deliver EXP-01. Phase 66 trains one smaller, shallower network on orbit 1632
with the INST-08 harness. It scores the result with the frozen FEAS-01
scorecard and repeats it on a second panel system and with a second seed. The
result is then reviewed against the pre-registered branches at owner
checkpoint ①.

The ladders (EXP-02..05) belong to Phase 67, which stays provisional until
this phase's review. The yardstick belongs to Phase 68 and the findings to
Phase 69. SCOPE-45..49 are binding. This discussion fixes the design
principles. The exact settings, budget and reading-rule numbers are fixed on
the committed prediction page before the first run (SCOPE-47).

</domain>

<decisions>
## Implementation decisions

### Decision ownership

- **D-01:** Phase 65 D-01 carries forward. Agents make the technical and
  scientific calls, recording evidence and rationale. The owner is asked only
  for scope, resource and other reserved choices. Owner checkpoint ① is the
  designed review after this experiment. It is not a technical questionnaire.

### What the experiment is for

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

### The network

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

### Repeats and reading

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

### Scoring, records and isolation

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

### Review and plan change

- **D-12:** At checkpoint ①, record the branch taken, a plain-language reading
  and any SCOPE-49 proposal (for example, an inserted Phase 66.1 or re-aimed
  Phase 67 experiments), with the owner's answer. A proposal blocks only the
  work that depends on it.

### Agent discretion for research and planning

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

</decisions>

<canonical_refs>
## Canonical references

Downstream agents must read these before planning or implementing.

### Phase and governance

- `.planning/ROADMAP.md`: Phase 66, its gate and the v2.5 diagnosis discipline.
- `.planning/REQUIREMENTS.md`: EXP-01, the prediction-page contents,
  SCOPE-45..49, the owner checkpoints and "How the first results can reshape
  the plan".
- `.planning/PROJECT.md`: Current Milestone v2.5, the standing delegation in
  Context, and Constraints (Mac only).
- `docs/git-guidelines.md`: agent-owned paths and atomic commits through
  `scripts/agent-commit`.

### Phase 65 harness and its limits

- `.planning/phases/65-probe-on-the-record-fit-harness/65-CONTEXT.md`
- `.planning/phases/65-probe-on-the-record-fit-harness/65-FINDINGS.md`:
  Sections 3-4, the smoke, its measured rate and the basis of that rate.
- `.planning/phases/65-probe-on-the-record-fit-harness/65-CLOSEOUT.md`: the
  reuse conditions and preserved hashes.
- `.planning/phases/65-probe-on-the-record-fit-harness/65-SMOKE-PREDICTION.md`:
  the format precedent for a prediction page and registration.
- `pinn/verification/diagnostic_fit.py`, `diagnostic_variants.py`,
  `diagnostic_similarity.py`, `diagnostic_guard.py` and `diagnostic_data.py`.
- `tests/phase65/`: the contract, isolation and parity suites that must keep
  passing.

### Prior results and frozen scoring

- `.planning/phases/60-single-system-learnability/60-FINDINGS.md`: the Rung 1
  results and the G2 sweep on 1632, including `first_omega_0` at 60-480, step
  counts and rates.
- `.planning/phases/64-feasibility-verdict/64-VERDICT.md`: the
  constant-predictor E values.
- `.planning/phases/59-read-only-baseline-scorecard/evidence/census/panels.json`
  and `census.json`: inner-lap counts (1632: 10.47, 851: 18.61).
- `.planning/phases/59-read-only-baseline-scorecard/59-GAPS.md`: GAP-59-08.
- `pinn/verification/artifacts/feasibility_scorecard_v1.json`,
  `pinn/verification/feasibility_scorer.py`,
  `pinn/verification/two_kepler.py`.

### Network and run control

- `pinn/network.py`: `_SIRENLayer` initialization, the source of the D-05
  frequency calculation.
- `pinn/architecture_spec.py`: the locks that variants must not relax.
- `scripts/phase60_run_control.py`, `scripts/phase60-pause.sh`,
  `scripts/phase60-resume.sh`, `scripts/phase60-power-guard.sh`: needed only
  if a run at or above one hour is registered. Their compatibility is
  unverified (Phase 65 D-11).

</canonical_refs>

<code_context>
## Existing code insights

- `diagnostic_variants.py` already carries `depth`, `width`, `learning_rate`,
  `window_length` and `first_omega_0` per variant. It builds the production
  class with only the topology and frequency fields replaced. Its sealed
  `REGISTRY` holds only `locked-12`, and `register_variant` returns a new
  registry without altering it.
- `validate_smoke_settings` in `diagnostic_fit.py` requires a byte-agreeing
  registry entry and a whole-run cap strictly below 3,600 s, before any data
  access. Admitting a Phase 66 variant means extending that path, not
  bypassing it.
- Only `raw_tau_ic13` is a supported time-feature declaration. That is
  consistent with D-03.
- The smoke record's timing basis separates measured optimizer steps from
  logging, scoring and setup. Budgets should use the same basis, plus the
  end-to-end per-step figure for wall-clock planning.

</code_context>

<specifics>
## Specific facts carried into planning

- On 1632, the locked network gave E 1.1574 after 794,350 Adam steps plus
  polish (2.57 h). At `first_omega_0 = 480` it gave E 1.1575.
- On 1632, the constant predictor scores 1.1538 and the two-Kepler formula
  0.9168. On 851 the constant predictor scores 1.2337.
- Phase 65's locked-12 rate is 0.014265 s per measured step, with 0.136 s per
  completed step end to end. It does not transfer to other variants.

</specifics>

<deferred>
## Deferred ideas

- The locked-frequency shallow network, the depth ladder, the learning-rate
  ladder, time-input designs and window lengths: Phase 67.
- Energy-metric adjudication and pass bars: Phase 68. GAP-59-08 stays open.
- Repairing the governed pause/resume and power-guard tooling: only if a run
  at or above one hour is registered.

### Reviewed todos, not folded

- `.planning/todos/pending/d-06-static-epsilon-sensitivity-check.md`: concerns
  stage labels and validation gates, outside this training-only, data-only
  phase. Same disposition as Phase 65.
- `.planning/todos/pending/trainex-r1-research-handoff.md`: stale handoff
  housekeeping. Same disposition as Phase 65.

</deferred>

---

*Phase: 66-small-network-control*
*Context gathered: 2026-10-31*
