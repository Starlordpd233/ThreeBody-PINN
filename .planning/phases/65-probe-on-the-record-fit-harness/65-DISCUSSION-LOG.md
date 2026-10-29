# Phase 65: Probe on the Record & Fit Harness - Discussion log

> Audit trail only. Research, planning and execution use `65-CONTEXT.md`.

**Date:** 2026-10-28
**Areas resolved:** decision ownership; probe provenance and reproduction;
diagnostic fit harness and isolation; scoring and measured budgets.

## User instruction and workflow adaptation

The owner requested `$gsd-discuss-phase 65` and explicitly delegated technical
and scientific decisions to the agent. The owner said:

> "i can't really answer any technical and scientific quesitons, but I can
> answer scope questions or questions that require generic decision that only
> the user should make the call."

The owner asked for this preference to apply to discussions in future GSD
milestones. It is recorded as a standing instruction in PROJECT.md's Context
section, with a Key Decision pointer.

The agent therefore replaced the technical questionnaire with evidence review
and two read-only GSD agent audits. No interactive options were presented and no
user answers were inferred. The choices below are agent judgments under that
delegation, not verbatim owner selections. Planning and execution were not
started.

## Alternatives considered by the agent

| Area | Selected approach | Alternative and reason not selected |
|------|-------------------|-------------------------------------|
| Decision ownership | Agents resolve technical questions; owner retains scope and reserved choices. | Technical interviewing would contradict the owner's instruction. Blanket waiver of locks or owner checkpoints was not requested. |
| Historical predictions | Recover actual printed output and register its expectations before rerunning. | Deriving a full per-layer prediction table from summary ranges would invent historical figures. |
| Initialization | Preserve the original CPU float64 reconstruction and distinguish production initialization. | Calling seed-42 CPU and MPS initial states identical is unsupported because construction uses the selected dtype/device. |
| Interpretation | Reproduce the observations, with causal confirmation left to the experiments. | Treating mean cosine alone as proof of lost information or the failure's cause would overstate the measurement. |
| Harness | Reuse production mathematics and INST-05 helpers while preserving the old sealed protocol. | Copying the old runner wholesale would inherit obsolete catalog, seed and budget restrictions. |
| Data and artifact boundaries | Enforce training-only access and test rejection at production entry points. | The old allowlist also admits validation, and a diagnostic label alone does not prove rejection. |
| Numeric details | Research/planning justifies tolerances, cadence and smoke settings, then fixes them before running. | Arbitrary discussion-stage constants lack evidence; result-dependent adjustment would undermine the reproduction. |
| Scoring and cost | Reuse frozen scoring and measure a short system-1632 run. | A new scorer or a full experiment here would exceed the phase-discussion boundary. |

## Evidence and limitations

- The milestone contracts already delegate technical rulings and reserve plan
  pivots, yardstick choices and the close decision to the owner.
- Both preserved exploratory scripts were inspected without execution. Their
  paths and hashes are in CONTEXT.md. Original stdout was not recovered in this
  discussion; it remains a prerequisite for registering the rerun.
- The original all-arm output summarizes deeper layers as a range. Additional
  per-layer readings must be identified as new measurements.
- Source review found the CPU float64 versus MPS float32 initialization
  distinction, the train/validation allowlist limitation, and old run-control
  path assumptions. These are planning inputs, not newly observed run results.
- No experiment, training step, scored smoke run or held-out evaluation was
  performed. No test-split dataset file was opened.

## Agent discretion and deferred work

CONTEXT.md assigns exact tolerances, module/record details, logger cadence,
smoke settings and necessary integration work to research/planning. It carries
the registered failure branch forward without changing the roadmap.

The experiments, yardstick, redesign choice and v2.6 implementation remain in
their assigned phases. Both keyword-matched todos were reviewed and left
outside Phase 65. No owner-only choice was needed to complete this context.
