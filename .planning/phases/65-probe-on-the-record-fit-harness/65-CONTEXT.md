# Phase 65: Probe on the Record & Fit Harness - Context

**Gathered:** 2026-10-28
**Status:** Ready for planning
**Decision source:** The owner explicitly delegated technical and scientific
judgments in this discussion. The agent resolved the areas below from the
milestone contracts and two independent source/code audits. No technical
questionnaire was put to the owner. The standing instruction for future
milestones is in `.planning/PROJECT.md`, Context.

<domain>
## Phase boundary

Deliver DIAG-09 and INST-08. Put the 2026-10-27 exploratory probe on the
record, reproduce its measurements read-only on the seven committed Phase 60
arms, and provide a tested diagnostic harness that fits and scores one named
network variant on one Stage-0 training orbit. Complete one short, scored run
on system 1632 and measure its cost for later experiments.

The experiments belong to Phases 66-67, the yardstick decisions to Phase 68,
and the findings/redesign decision to Phase 69. SCOPE-45..49 remain binding.
This discussion authorizes context capture, not an experiment launch.

</domain>

<decisions>
## Implementation decisions

### Decision ownership

- **D-01:** Agents handle the intellectual work, including technical research,
  scientific interpretation, implementation tradeoffs and verification within
  scope. Record the evidence and rationale. Ask the owner only for scope and
  user-only choices, with a recommendation in plain language. The explicit
  milestone checkpoints, locks and applicable gap protocols remain in force.

### Probe provenance and reproduction

- **D-02:** Treat DIAG-09 as a reproduction of already-seen exploratory
  results. Commit the original figures, measurement definitions, selected
  states, reproduction tolerances and reading rule before the first rerun.
  Preserve that chronology; this is not an independent prospective discovery
  of the lead. Do not widen tolerances after seeing results.
- **D-03:** Recover the original printed figures rather than constructing
  per-arm predictions from PROJECT.md's summary ranges. The all-arm script
  printed h1, h2 and a min/max range over deeper hidden layers. New individual
  deep-layer readings are new measurements, not historical predictions.
  Missing source output is a provenance limitation, not a failed reproduction.
- **D-04:** Preserve the original probe's CPU float64, seed-42 initialization
  as its own reconstruction. Phase 60 trained on MPS float32; a matching seed
  alone does not establish identical initial weights across these runtimes.
  Label the two accurately. Test INST-08's production forward parity separately
  using the same weights and runtime. Do not describe the old reconstruction
  as the historical training initialization without evidence.
- **D-05:** Reproduce the original centred neighbour-cosine definition and
  use the same measurement implementation in the fit logger. Record layer
  identities and time coordinates. Adjacent gold samples are physically 0.01
  apart; that is not a claim that normalized tau differs by 0.01. The original
  output-rate ratio uses network autograd derivatives and finite differences
  of the gold positions in the same tau coordinate. Label that comparator
  explicitly. Preserve the first-layer frequency and output-variation measures.
- **D-06:** Enumerate the seven arms from committed records and check each
  weight file against its committed SHA-256 before loading. Follow each arm's
  architecture/frequency and the original probe's state selection. The all-arm
  script uses `better_state`; the single-arm script also inspects Adam and
  polish. Keep those comparisons distinct. The probe takes no optimizer step
  and attests to its dataset access.
- **D-07:** Low mean neighbour cosine is a measured association. It does not
  itself establish information loss, a capacity limit or the cause of failure.
  Report every registered figure as reproduced or not. If the lead fails the
  registered reproduction rule, withdraw it and propose the roadmap change
  through SCOPE-49. Do not repair the lead by changing the rule.

### Diagnostic fit harness and isolation

- **D-08:** Build on INST-05's data, model, loss, scoring and record helpers
  while preserving its sealed historical protocol. INST-08 has named diagnostic
  variants recording depth, width, time features, learning rate and window
  length. Its locked 12-layer variant must match the production forward pass
  at the same seed and weights. Production architecture locks remain intact.
  Detailed Phase 66-67 variant choices belong to their prediction pages.
- **D-09:** Restrict data access to Stage-0 training records. The existing
  split allowlist admits both training and validation, so reusing it alone is
  insufficient. Test refusal before opening disallowed data. Directly test
  that production graded-run and evaluator entry points reject INST-08
  artifacts, including after relocation. A `diagnostic` label alone is not
  proof of isolation. Keep the preserved evaluation unspent.

### Scoring and measured budgets

- **D-10:** Call the frozen FEAS-01 scorer and scorecard directly. Preserve
  their hashes and semantics. Report physical scores and tier beside the
  constant predictor and two-Kepler comparison on the same orbit and window.
  Keep training loss as context. Known energy-metric limitations stay explicit;
  their adjudication belongs to Phase 68. The logger must reproduce DIAG-09 on
  one committed arm before its training trace is trusted.
- **D-11:** The short system-1632 run establishes mechanical operation and a
  measured seconds-per-step, not learnability or a confirmed cause. Record the
  variant, device/dtype, step count, logging cadence, wall time and timing basis.
  Use measured cost to set later budgets. Any run over an hour must have working
  governed pause/resume and power controls; the existing Phase 60 wrappers
  hardcode old paths and need compatibility verification before reuse.

### Agent discretion for research and planning

- Recover the historical figure source and define exact reproduction
  tolerances from its precision and the computation, before any rerun.
- Choose the module layout and registry/record details, the smoke run's
  optimizer settings and length, and the fixed similarity cadence. Justify
  those choices from existing tooling and timing, rather than asking the owner
  to pick technical constants. Freeze run settings before the run.
- Choose the smallest implementation that proves INST-08(a-e), including any
  necessary refusal or run-control integration. Protect frozen evidence and
  avoid importing Phase 60's multi-hour budgets into a minute-scale harness.

</decisions>

<canonical_refs>
## Canonical references

Read the relevant contracts before research, planning or implementation.

### Phase and governance

- `.planning/ROADMAP.md`, Phase 65 and diagnosis discipline.
- `.planning/REQUIREMENTS.md`, DIAG-09, INST-08, SCOPE-45..49, owner checkpoints
  and the registered result branches.
- `.planning/PROJECT.md`, Current Milestone, standing delegation in Context,
  Constraints, and the build-milestone grounding decisions.
- `AGENTS.md`, applicable gap and Git protocols.
- `docs/git-guidelines.md`, agent-owned paths and atomic commits.

### Prior evidence and frozen scoring

- `.planning/phases/60-single-system-learnability/60-CONTEXT.md`.
- `.planning/phases/60-single-system-learnability/60-FINDINGS.md`.
- `.planning/phases/60-single-system-learnability/60-VERIFICATION.md`.
- `.planning/phases/60-single-system-learnability/evidence/arms/`, the seven
  committed arm records and their selected weight files.
- `.planning/phases/64-feasibility-verdict/64-VERDICT.md`.
- `.planning/phases/64-feasibility-verdict/evidence/build_phase64_evidence.py`,
  hash-before-load precedent and constant-predictor measurements.
- `.planning/phases/59-read-only-baseline-scorecard/59-GAPS.md`, GAP-59-08.
- `.planning/phases/59-read-only-baseline-scorecard/evidence/census/`.
- `.planning/phases/59-read-only-baseline-scorecard/evidence/baselines/`.
- `pinn/verification/artifacts/feasibility_scorecard_v1.json`.
- `pinn/verification/feasibility_scorecard.py`.
- `pinn/verification/feasibility_scorer.py`.

### Production contract and diagnostic integration

- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md`.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md`.
- `pinn/architecture_spec.py` and `pinn/network.py`.
- `pinn/verification/diagnostic_architecture.py`.
- `pinn/verification/learnability_data.py`, `pinn/verification/learnability_losses.py`
  and `pinn/verification/learnability_run.py`.
- `pinn/verification/split_allowlist.py`.
- `pinn/training/checkpoint.py`, `pinn/training/resume.py` and `pinn/evaluate.py`.
- `scripts/phase60_run_control.py`, `scripts/phase60-pause.sh`,
  `scripts/phase60-resume.sh` and `scripts/phase60-power-guard.sh`.
- `tests/phase60/test_data_seam.py`, `tests/phase60/test_refusals.py`,
  `tests/phase60/test_run_short.py` and `tests/phase60/test_scorer_mps.py`.

</canonical_refs>

<code_context>
## Existing code insights

- The production network exposes its input and hidden layers. Instrument those
  boundaries without reimplementing its forward mathematics or COM head.
- INST-05 already supplies real IC13, retained-normalizer recovery, gold-record
  loading, frozen scoring and diagnostic records. Its old catalog, seed and
  budgets are not INST-08's run policy.
- Phase 64 hashes weights before loading. The older Phase 60 rescorer performs
  that check after loading, so copy the former ordering.
- Current rebuilt `pinn/` code is permitted build evidence under PROJECT.md's
  build-milestone decision. June 2026 codebase maps describe older code; use the
  current requirements and source for integration facts.
- Existing diagnostic refusal checks depend on checkpoint structure and run
  ownership. Verify the new record at the actual entry points.

</code_context>

<specifics>
## Preserved exploratory sources

Both scripts were located and read without execution on 2026-10-28 in:

`/private/tmp/claude-501/-Users-<user>-Desktop-3-body-problem--worktrees-trainex/bac24a94-a63c-43a3-acbd-dfc3a0bbe1ba/scratchpad/v25-probe-origin/`

- `probe_time_signal.py`, SHA-256
  `16db5c8cccf76417f4d18a84811d62b99eea4746d11d6f2322cef349065c9a4f`.
- `probe_all_arms.py`, SHA-256
  `a4dea7d08b750b8cef9fa28c3d354f646922b7eb4463b3b39a2ede18ac9d04c8`.

These temporary paths are a handoff, not durable evidence. Implementation must
preserve the source and recover its original numerical output before the
registered rerun. This discussion did not recover that output or run the probe.

</specifics>

<deferred>
## Deferred ideas

- The small-network control and ladders, Phases 66-67.
- Metric amendments and pass-bar choices, Phase 68; GAP-59-08 remains open.
- Redesign direction and commissioning trainex-r5, Phase 69.
- Framework-spec amendments, physics-term repairs and the rebuild, v2.6.

### Reviewed todos, not folded

- `.planning/todos/pending/d-06-static-epsilon-sensitivity-check.md`: concerns
  stage labels and validation gates, outside this training-only, data-only phase.
- `.planning/todos/pending/trainex-r1-research-handoff.md`: stale handoff
  housekeeping, already identified in Phase 60. No scope expansion or todo edit.

</deferred>
