# Phase 65: Probe on the Record & Fit Harness - Research

**Researched:** 2026-10-28 (America/Chicago) | **Domain:** diagnostic reproduction and single-orbit instrumentation | **Confidence:** HIGH for locked scope and recovered stdout; inherited code details require source confirmation.

<user_constraints>
## User Constraints (from CONTEXT.md)
The following decision text is copied verbatim, with paragraph wrapping compacted. [VERIFIED: .planning/phases/65-probe-on-the-record-fit-harness/65-CONTEXT.md:31-114,203-216]
### Locked Decisions
- **D-01:** Agents handle the intellectual work, including technical research, scientific interpretation, implementation tradeoffs and verification within scope. Record the evidence and rationale. Ask the owner only for scope and user-only choices, with a recommendation in plain language. The explicit milestone checkpoints, locks and applicable gap protocols remain in force.
- **D-02:** Treat DIAG-09 as a reproduction of already-seen exploratory results. Commit the original figures, measurement definitions, selected states, reproduction tolerances and reading rule before the first rerun. Preserve that chronology; this is not an independent prospective discovery of the lead. Do not widen tolerances after seeing results.
- **D-03:** Recover the original printed figures rather than constructing per-arm predictions from PROJECT.md's summary ranges. The all-arm script printed h1, h2 and a min/max range over deeper hidden layers. New individual deep-layer readings are new measurements, not historical predictions. Missing source output is a provenance limitation, not a failed reproduction.
- **D-04:** Preserve the original probe's CPU float64, seed-42 initialization as its own reconstruction. Phase 60 trained on MPS float32; a matching seed alone does not establish identical initial weights across these runtimes. Label the two accurately. Test INST-08's production forward parity separately using the same weights and runtime. Do not describe the old reconstruction as the historical training initialization without evidence.
- **D-05:** Reproduce the original centred neighbour-cosine definition and use the same measurement implementation in the fit logger. Record layer identities and time coordinates. Adjacent gold samples are physically 0.01 apart; that is not a claim that normalized tau differs by 0.01. The original output-rate ratio uses network autograd derivatives and finite differences of the gold positions in the same tau coordinate. Label that comparator explicitly. Preserve the first-layer frequency and output-variation measures.
- **D-06:** Enumerate the seven arms from committed records and check each weight file against its committed SHA-256 before loading. Follow each arm's architecture/frequency and the original probe's state selection. The all-arm script uses `better_state`; the single-arm script also inspects Adam and polish. Keep those comparisons distinct. The probe takes no optimizer step and attests to its dataset access.
- **D-07:** Low mean neighbour cosine is a measured association. It does not itself establish information loss, a capacity limit or the cause of failure. Report every registered figure as reproduced or not. If the lead fails the registered reproduction rule, withdraw it and propose the roadmap change through SCOPE-49. Do not repair the lead by changing the rule.
- **D-08:** Build on INST-05's data, model, loss, scoring and record helpers while preserving its sealed historical protocol. INST-08 has named diagnostic variants recording depth, width, time features, learning rate and window length. Its locked 12-layer variant must match the production forward pass at the same seed and weights. Production architecture locks remain intact. Detailed Phase 66-67 variant choices belong to their prediction pages.
- **D-09:** Restrict data access to Stage-0 training records. The existing split allowlist admits both training and validation, so reusing it alone is insufficient. Test refusal before opening disallowed data. Directly test that production graded-run and evaluator entry points reject INST-08 artifacts, including after relocation. A `diagnostic` label alone is not proof of isolation. Keep the preserved evaluation unspent.
- **D-10:** Call the frozen FEAS-01 scorer and scorecard directly. Preserve their hashes and semantics. Report physical scores and tier beside the constant predictor and two-Kepler comparison on the same orbit and window. Keep training loss as context. Known energy-metric limitations stay explicit; their adjudication belongs to Phase 68. The logger must reproduce DIAG-09 on one committed arm before its training trace is trusted.
- **D-11:** The short system-1632 run establishes mechanical operation and a measured seconds-per-step, not learnability or a confirmed cause. Record the variant, device/dtype, step count, logging cadence, wall time and timing basis. Use measured cost to set later budgets. Any run over an hour must have working governed pause/resume and power controls; the existing Phase 60 wrappers hardcode old paths and need compatibility verification before reuse.
### Agent Discretion for Research and Planning
- Recover the historical figure source and define exact reproduction tolerances from its precision and the computation, before any rerun.
- Choose the module layout and registry/record details, the smoke run's optimizer settings and length, and the fixed similarity cadence. Justify those choices from existing tooling and timing, rather than asking the owner to pick technical constants. Freeze run settings before the run.
- Choose the smallest implementation that proves INST-08(a-e), including any necessary refusal or run-control integration. Protect frozen evidence and avoid importing Phase 60's multi-hour budgets into a minute-scale harness.
### Deferred Ideas (OUT OF SCOPE)
- The small-network control and ladders, Phases 66-67.
- Metric amendments and pass-bar choices, Phase 68; GAP-59-08 remains open.
- Redesign direction and commissioning trainex-r5, Phase 69.
- Framework-spec amendments, physics-term repairs and the rebuild, v2.6.
### Reviewed todos, not folded
- `.planning/todos/pending/d-06-static-epsilon-sensitivity-check.md`: concerns stage labels and validation gates, outside this training-only, data-only phase.
- `.planning/todos/pending/trainex-r1-research-handoff.md`: stale handoff housekeeping, already identified in Phase 60. No scope expansion or todo edit.
</user_constraints>

## Project Constraints (from AGENTS.md)
- Use Sequentialthinking for multi-step work; inspect context and state the approach and success checks before substantive edits. Keep changes minimal and preserve concurrent work. [CITED: user-provided AGENTS.md, Tooling and Editing workflow]
- Ground decisions in authorized evidence; follow applicable STOP/gap protocols and owner checkpoints. Technical delegation does not authorize scope changes. [CITED: user-provided AGENTS.md, Critical Governance; VERIFIED: .planning/REQUIREMENTS.md:180-194]
- Orient in the owning worktree, surface Git state, declare disjoint ownership, and serialize commits through `scripts/agent-commit` with `GIT_AGENT_ID` and `GIT_AGENT_OWNED_PATHS`; stage explicit paths, review staged/unstaged changes and run `git diff --check`. Preserve unrelated work. [CITED: user-provided AGENTS.md, Git Commit Protocol]
- Use the required commit format/body/trailer and one atomic end-of-task commit for planning/spec changes; do not push protected branches or bypass hooks. This research child is explicitly instructed not to commit. [CITED: user-provided AGENTS.md, Commit cadence and Git Commit Protocol; parent assignment]
- Obtain exact approval and recovery protection for destructive Git operations; ask before production dependencies, deployment changes, production data or unusually costly validation. Read `docs/README.md` before creating/moving/deleting docs files. [CITED: user-provided AGENTS.md, Repo hygiene and Docs lifecycle]

<phase_requirements>
## Phase Requirements
| ID | Required behavior | Research support |
|---|---|---|
| DIAG-09 | “The 2026-10-27 probe, on the record.” | Exact stdout below; precommitted rounding cells; hash-before-load; no training or test-split access. [VERIFIED: .planning/REQUIREMENTS.md:78-88] |
| INST-08 | “A minute-scale diagnostic fit harness.” | Shared instrumentation, production parity, frozen scoring, pre-open refusal, relocated-artifact rejection and one bounded scored run. [VERIFIED: .planning/REQUIREMENTS.md:92-102] |
| SCOPE-45..49 | Stage-0 training only; no spec/lock edits; committed predictions; this Mac only; owner decides pivots. | Keep later experiments and yardstick changes outside this phase. [VERIFIED: .planning/REQUIREMENTS.md:180-184] |
</phase_requirements>

## Summary
Use a separate diagnostic implementation that reuses the production forward mathematics and frozen scoring, shares one probe/logger measurement function, and enforces Stage-0 TRAIN access before every data open. Success is DIAG-09 reproduction plus INST-08(a-e), without spending evaluation. [VERIFIED: .planning/phases/65-probe-on-the-record-fit-harness/65-CONTEXT.md:55-102; .planning/REQUIREMENTS.md:78-102]
The original numerical output has now been recovered from the two specifically authorized transcript tool results. Commit durable copies of the scripts, extracted numerical output, exact acceptance intervals and reading rule before rerunning; individual deep-layer values absent from the all-arm output remain new measurements. [VERIFIED: <home>/.claude-alt/projects/-Users-<user>-Desktop-3-body-problem--worktrees-trainex/acb49c49-444a-46ea-a66b-792086b740d2.jsonl:332-332,353-353; .planning/phases/65-probe-on-the-record-fit-harness/65-CONTEXT.md:39-48]
**Primary recommendation:** implement refusal and synthetic parity/scorer tests first, register the reproduction, reproduce one arm through the shared logger, then permit the separately registered short system-1632 smoke. [VERIFIED: .planning/phases/65-probe-on-the-record-fit-harness/65-CONTEXT.md:82-111]

## Architectural Responsibility Map
| Capability | Primary tier | Secondary tier | Rationale |
|---|---|---|---|
| Access policy and normalizer recovery | Local diagnostic data boundary | Recorded evidence | Guard both target and ancillary reads before loading. [VERIFIED: .planning/phases/65-probe-on-the-record-fit-harness/65-CONTEXT.md:82-87] |
| Variant construction, fit and similarity | Local Python diagnostic tooling | Production model | Reuse forward mathematics; preserve the locked architecture. [VERIFIED: .planning/phases/65-probe-on-the-record-fit-harness/65-CONTEXT.md:76-80,170-174] |
| Physical scoring | Frozen FEAS-01 scorer | Diagnostic record | Call the scorer directly beside matched comparison predictors. [VERIFIED: .planning/phases/65-probe-on-the-record-fit-harness/65-CONTEXT.md:91-96] |
| Production refusal | Graded training/evaluator entry points | Diagnostic artifact marker | Reject artifacts even after relocation, before evaluation ownership is claimed. [VERIFIED: .planning/phases/65-probe-on-the-record-fit-harness/65-CONTEXT.md:82-87; ASSUMED: inherited entry-point ordering finding, A2] |

## Historical Probe: Exact Printed All-Arm Figures
All cells below quote stdout verbatim, including precision and signed zero. “d/dt x truth” is the historical heading; register its actual network-AD/gold-FD comparison in tau. Source: all-arm tool result `toolu_01NHGWRv6pEQCJmqeAXxqonK`, 2026-10-27T14:14:01.814Z. [VERIFIED: <home>/.claude-alt/projects/-Users-<user>-Desktop-3-body-problem--worktrees-trainex/acb49c49-444a-46ea-a66b-792086b740d2.jsonl:353-353; .planning/phases/65-probe-on-the-record-fit-harness/65-CONTEXT.md:55-61]
| arm | state | 1st-layer cyc | adj h1 | adj h2 | adj h3..h12 range | out move | d/dt x truth |
|---|---|---|---|---|---|---|---|
| g2s-1632-w060 | init | 0.78 | 1.000 | 1.000 | 0.751 to 1.000 | 2.7741 | 195 |
| g2s-1632-w060 | adam | 7.75 | 0.938 | 0.017 | -0.004 to 0.003 | 0.0034 | 1.9e+08 |
| g2s-1632-w120 | init | 1.56 | 1.000 | 1.000 | 0.413 to 0.999 | 2.8467 | 388 |
| g2s-1632-w120 | adam | 16.80 | 0.772 | -0.004 | -0.003 to 0.004 | 0.0032 | 4.65e+08 |
| g2s-1632-w240 | init | 3.13 | 0.999 | 0.999 | 0.104 to 0.996 | 2.8247 | 810 |
| g2s-1632-w240 | adam | 33.53 | 0.479 | -0.000 | -0.005 to 0.004 | 0.0030 | 9.74e+08 |
| g2s-1632-w480 | init | 6.25 | 0.997 | 0.995 | 0.020 to 0.987 | 2.8461 | 1.61e+03 |
| g2s-1632-w480 | adam | 66.38 | 0.256 | -0.002 | -0.005 to 0.003 | 0.0030 | 9.67e+08 |
| r1-1632 | init | 0.39 | 1.000 | 1.000 | 0.925 to 1.000 | 2.8730 | 101 |
| r1-1632 | polish | 4.25 | 0.985 | 0.351 | -0.004 to 0.018 | 0.0034 | 4.97e+07 |
| r1-4658 | init | 0.39 | 1.000 | 1.000 | 0.921 to 1.000 | 7.0396 | 51.9 |
| r1-4658 | adam | 5.29 | 0.929 | -0.000 | -0.004 to 0.001 | 0.0030 | 2.19e+09 |
| r1-851 | init | 0.39 | 1.000 | 1.000 | 0.932 to 1.000 | 2.3525 | 77.4 |
| r1-851 | adam | 3.98 | 0.981 | 0.201 | -0.004 to 0.004 | 0.0031 | 1.59e+08 |

The separate single-arm result `toolu_01PUFNWxrDDsVrU8DTCH4tX3` (2026-10-27T14:12:02.670Z) prints Adam h3 `0.0186`, polish h3 `0.0177`; Adam output `0.0035` and `5.19e+07`, polish output `0.0034` and `4.97e+07`. Do not merge Adam's h3 with the selected polish range's `0.018`. [VERIFIED: <home>/.claude-alt/projects/-Users-<user>-Desktop-3-body-problem--worktrees-trainex/acb49c49-444a-46ea-a66b-792086b740d2.jsonl:332-332]
**Tolerance recommendation:** pre-register exact rendered-field equality using the original all-arm formatters: frequency `.2f`, cosine/range `.3f`, output movement `.4f`, derivative ratio `.3g`. Also retain unrounded new measurements and deltas. The `.3g` formatter omits trailing zeros, so `1.9e+08` represents three-significant-digit rounding; counting its visible digits would widen acceptance incorrectly. This formatter rule defines the original rounding cells, including signed zero and tie behavior. Before any rerun, derive and record every exact boundary from the preserved formatter, and test both sides of boundaries plus zero/ties; do not widen after results. Single-arm fields must retain their own original formatters. [CITED: parent's completed original-script audit and formatter correction; VERIFIED: .planning/phases/65-probe-on-the-record-fit-harness/65-CONTEXT.md:39-43,106-111; ASSUMED: exact formatter details pending preserved-source confirmation, A5]
**Preserve original script identities:** `probe_time_signal.py` SHA-256 `16db5c8cccf76417f4d18a84811d62b99eea4746d11d6f2322cef349065c9a4f`; `probe_all_arms.py` SHA-256 `a4dea7d08b750b8cef9fa28c3d354f646922b7eb4463b3b39a2ede18ac9d04c8`. The temporary handoff directory is recorded in context; copy and verify its contents rather than trusting continued existence. [CITED: .planning/phases/65-probe-on-the-record-fit-harness/65-CONTEXT.md:188-199]

## Standard Stack
Reuse the installed Python/PyTorch stack and existing diagnostic/scoring helpers; install no new packages. The completed research handoff reports Python `3.11.15`, torch `2.12.1` and runtime `<home>/miniforge3/envs/pinn-train/bin/python`; this child did not independently probe them. [ASSUMED: inherited environment observation, A4]
Use the production network as the source of forward mathematics; keep CPU float64 seed-42 probe reconstruction distinct from MPS float32 historical training and same-weights forward-parity testing. [VERIFIED: .planning/phases/65-probe-on-the-record-fit-harness/65-CONTEXT.md:49-54,170-174]
## Package Legitimacy Audit
No external package installation is recommended; a registry/legitimacy audit is therefore not required for this handoff. [CITED: bounded parent assignment; recommendation above]

## Architecture Patterns
**Data flow:** registered prediction + verified weights → Stage-0 TRAIN pre-open guard → recorded normalizer + gold record → production-compatible variant → shared probe/logger → frozen scorer + matched baselines → diagnostic record → production-entry refusal. This is the proposed integration order. [VERIFIED: .planning/phases/65-probe-on-the-record-fit-harness/65-CONTEXT.md:62-102; ASSUMED: inherited normalizer integration, A3]
Keep new modules under the context-designated `pinn/verification/` boundary. Reuse `SQRSkipResNetSIREN` with a verification-only variant specification, `data_only_loss`, `score_network`/`score_trajectory`, and `two_kepler_prediction`; confirm these inherited symbol names in source before implementation. [CITED: .planning/REQUIREMENTS.md:92-102; ASSUMED: inherited symbol audit, A1]
The completed audit reports `PINNED_MODULES` contains 33 modules in `pinn/verification/learnability_protocol.py:145-179`, including network/spec/data/loss/scorer/scorecard/protocol. Preserve every original digest with an automated check and do not modify pinned files. It reports `pinn/evaluate.py`, `pinn/train.py`, `pinn/training/checkpoint.py`, `pinn/training/resume.py` are outside that set: confine any necessary early refusal there after confirming membership. [ASSUMED: inherited pinned-file audit, A1]
Guard all ancillary reads, not only the orbit loader. The inherited audit found `open_real_context()` reconstructs 256 monitor keys (240 Stage 0 + 16 Stage 1), unsuitable here; instead reconstruct recorded `slot_means`, `slot_stds`, `e_scale`, `stats_sha256` from `.planning/phases/59-read-only-baseline-scorecard/evidence/audit/reader_acceptance.json:56-92`, verify `stats_digest == EXPECTED_STATS_SHA256`, and fail closed. Never refit statistics on a permitted subset. Confirm this source before implementing the adapter. [ASSUMED: inherited normalizer audit and parent's corrected artifact path, A3]
Reject diagnostic records before the evaluator claims preserved evaluation. Test actual `evaluate_run` and graded training entry points with artifacts relocated beside `config.yaml`/`splits.json`; basename or original-location checks are insufficient. [VERIFIED: .planning/phases/65-probe-on-the-record-fit-harness/65-CONTEXT.md:82-87,180-181; ASSUMED: inherited evaluator ordering and entry names, A2]

## Don't Hand-Roll
Reuse production forward mathematics, the frozen scorer/scorecard, INST-05 data-only loss and matched comparison predictors; make one shared centred-cosine implementation serve probe and logger. Do not clone the frozen protocol or recompute a new normalization population. [VERIFIED: .planning/phases/65-probe-on-the-record-fit-harness/65-CONTEXT.md:55-61,76-96,170-174; ASSUMED: inherited normalizer finding, A3]

## Common Pitfalls
- Summary ranges are not the per-arm historical figures: preserve the table, state selection, individual single-arm evidence and original rounding separately. Low cosine alone does not prove causality. [VERIFIED: .planning/phases/65-probe-on-the-record-fit-harness/65-CONTEXT.md:39-72]
- Training-plus-validation allowlisting is insufficient; enforce Stage-0 TRAIN before any open, including retained-stat recovery, with open-spy refusal tests. [VERIFIED: .planning/phases/65-probe-on-the-record-fit-harness/65-CONTEXT.md:82-87; ASSUMED: inherited normalizer finding, A3]
- A diagnostic marker alone cannot prove production isolation; verify actual relocated entry-point refusal and unchanged frozen digests. [VERIFIED: .planning/phases/65-probe-on-the-record-fit-harness/65-CONTEXT.md:82-96; ASSUMED: inherited pinned-module audit, A1]
- A bounded smoke demonstrates mechanics and measured cost only. Do not transfer locked-baseline rates to future depth ladders or launch Phases 66-69 work. [VERIFIED: .planning/phases/65-probe-on-the-record-fit-harness/65-CONTEXT.md:20-22,97-114,206-209]

## Code Examples
Measurement skeleton to verify against preserved original scripts before coding: `mean(cosine(centered_hidden[:-1], centered_hidden[1:]))`; output variation is the centered norm ratio; output-rate ratio compares network AD `d/dtau` with gold finite differences in that same coordinate; first-layer frequency is `abs(weight_time) * omega / pi` cycles per full normalized window. Preserve the original reductions and centering axis rather than guessing them from this shorthand. [VERIFIED: .planning/phases/65-probe-on-the-record-fit-harness/65-CONTEXT.md:55-61; ASSUMED: inherited exact formula audit, A5]

## State of the Art
For this phase, replace unregistered summary-based repetition with a committed historical-output record and immutable reading rule; replace label-only isolation with tested pre-open and production-entry refusals. This is a phase-specific recommendation, not a claim about external framework releases. [VERIFIED: .planning/phases/65-probe-on-the-record-fit-harness/65-CONTEXT.md:39-48,82-87]

## Environment Availability
The inherited audit reports the local Python runtime above is available. Reconfirm at implementation; no cloud route or new dependency is planned. Smoke seconds-per-step and later experiment rates remain **unknown** until the registered short run measures them. Runs over one hour require proven pause/resume/power compatibility; the old wrappers' hardcoded paths require checking before reuse. [ASSUMED: inherited availability observation, A4; VERIFIED: .planning/phases/65-probe-on-the-record-fit-harness/65-CONTEXT.md:97-114; .planning/REQUIREMENTS.md:183-183]

## Validation Architecture
**Framework:** proposed standard-library `unittest`, small synthetic fixtures; add no test framework. Existing Phase 60 data-seam/refusal/short-run/scorer tests are reuse references recorded in context, not checks executed by this child. [CITED: .planning/phases/65-probe-on-the-record-fit-harness/65-CONTEXT.md:160-163]
**Proposed new test directory:** `tests/phase65/`; all modules below are **not yet created**. Commands are planned acceptance checks, not reported passes. [CITED: parent assignment; implementation recommendation]
| Requirement | Proposed coverage | Planned command |
|---|---|---|
| DIAG-09 | Original precision/endpoints, state selection, hash-before-load, shared measurement reductions | `<home>/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase65.test_probe -v` |
| INST-08(a,b) | Same-runtime/same-weights forward parity; direct frozen scorer; preserved 33 digests | `<home>/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase65.test_contracts -v` |
| INST-08(d) | Pre-open Stage-0 TRAIN refusal and relocated graded/evaluator refusal without evaluation claim | `<home>/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase65.test_isolation -v` |
| INST-08(e) | Tiny synthetic fit, cadence, record and matched-window baseline plumbing | `<home>/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase65.test_fit_short -v` |
**Full synthetic suite:** `<home>/miniforge3/envs/pinn-train/bin/python -m unittest discover -s tests/phase65 -p 'test_*.py' -v`. Run targeted tests per task and the full suite at phase integration; test duration is unmeasured. [CITED: proposed validation design; ASSUMED: runtime path, A4]
**Separate real acceptance gates:** only after their committed prediction pages, perform the seven-arm read-only reproduction and the short scored system-1632 smoke. First reproduce one committed arm with the shared logger for INST-08(c). Before smoke, freeze variant, optimizer, step count and similarity cadence; then record wall time, timing basis and measured rate. These are future execution tasks; none ran during this handoff. [VERIFIED: .planning/phases/65-probe-on-the-record-fit-harness/65-CONTEXT.md:39-43,91-114; .planning/REQUIREMENTS.md:85-102]
**Wave 0 gaps:** create the four proposed modules plus fixtures/open spies; confirm inherited symbol/pinned/normalizer facts and runtime; preserve original numerical output and scripts; commit exact rounding endpoints and both execution registrations before their respective runs. [CITED: proposed task decomposition; .planning/phases/65-probe-on-the-record-fit-harness/65-CONTEXT.md:39-43,62-67,82-114]

## Security Domain
Focus on local artifact integrity and authorized data access: check hashes before deserialization, guard Stage-0 TRAIN reads before opening, fail closed on normalizer mismatch, and reject diagnostic production use. No authentication/session/cryptography feature is introduced. ASVS input-validation/access-control concepts are relevant; numbered ASVS-version mappings were not looked up in this bounded handoff and are not asserted. [VERIFIED: .planning/phases/65-probe-on-the-record-fit-harness/65-CONTEXT.md:62-67,82-96; ASSUMED: normalizer details, A3]

## Assumptions Log
The following are inherited completed-research findings, not independently source-opened in this child; verify them in the listed implementation sources before relying on discrete symbols or membership. Routine technical verification is delegated; no new owner choice is requested. [VERIFIED: .planning/phases/65-probe-on-the-record-fit-harness/65-CONTEXT.md:31-35]
| ID | Inherited claim to confirm | Risk if wrong |
|---|---|---|
| A1 | Exact reusable symbols and 33 pinned modules/nonmembers in `learnability_protocol.py:145-179`. | Frozen historical protocol could change or an import fail. |
| A2 | Evaluator ownership-claim ordering; actual entry names and relocated config layout. | Preserved evaluation could be consumed before refusal. |
| A3 | Monitor population and recorded-normalizer fields, digest contract and source location. | Ancillary Stage-1/validation reads or changed normalization. |
| A4 | Installed Python/torch versions and absolute runtime path. | Planned commands may not run; actual smoke cost stays unknown. |
| A5 | Exact centering/reductions, variation ratio, frequency formula and original field formatters in original scripts. | The logger could measure a different quantity or accept an incorrectly widened rounding cell. |

## Open Questions
No unresolved owner technical choice is identified within this bounded handoff. Exact smoke settings and all interval endpoints must be frozen during planning/registration; measured timing awaits the smoke. A failed reproduction or result outside registered branches follows SCOPE-49 rather than a revised reading rule. [VERIFIED: .planning/phases/65-probe-on-the-record-fit-harness/65-CONTEXT.md:68-72,97-114; .planning/REQUIREMENTS.md:182-184,198-204]

## Sources and Metadata
Primary sources opened for this handoff: `65-CONTEXT.md` and `.planning/REQUIREMENTS.md`, plus only numerical tool results at transcript lines 332 and 353. Integration/environment details explicitly marked A1-A5 come from the parent's completed-research handoff and were not reinvestigated. No external documentation lookup, package install, dataset open, test, probe, training or benchmark was performed. [CITED: bounded parent assignment; this handoff's tool record]
**Confidence:** scope/provenance HIGH; inherited integration details pending source confirmation; performance unknown. Research is valid for the current frozen records and phase constraints; recheck integration facts if source or protocol digests change. [CITED: source distinctions above; .planning/phases/65-probe-on-the-record-fit-harness/65-CONTEXT.md:76-102]
