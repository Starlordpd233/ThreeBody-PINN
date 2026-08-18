---
phase: 50-valid-stage-0-re-run
plan: 08
subsystem: owner-authorization
tags: [pinn, owner-checkpoint, d-19, d-20, preregistration, causal-front]

requires:
  - phase: 50-valid-stage-0-re-run
    provides: Plan 50-06 conformance repairs and bounded diagnosis; Plan 50-07 normal evidence tooling
provides:
  - "Owner-ready non-predictive decision brief for D-19/D-20 later-generation preregistration"
  - "Committed phase50-owner-preregistration-decision/v1 JSON block recording selected_option=stop-incomplete"
affects: [v2.3-milestone-routing]

actuals:
  tokens: 4500
  tasks: 2
  commits: 1

tech-stack:
  added: []
  patterns:
    - "Conformance readiness is recorded separately from causal-front dynamics"
    - "Owner preregistration authority is reserved in a committed-blob JSON block and is not inferred"

key-files:
  created:
    - .planning/phases/50-valid-stage-0-re-run/50-08-SUMMARY.md
  modified: []

key-decisions:
  - "Owner selected stop-incomplete 2026-08-17: Phase 50 closes with RUN-01/RUN-02 unsatisfied"
  - "GAP-50-03 remains read-only historical context"
  - "Routes to v2.3 recipe adjudication per REQUIREMENTS.md Future Requirements (trainex-r2 as candidate verdict source, SCOPE-29/31)"

patterns-established:
  - "Removing observation defects does not predict causal-front advance"
  - "A conformance audit closing the open dynamics question is grounding for a stop/continue decision without itself selecting the option"

requirements-completed: []

coverage:
  - id: D1
    description: "Owner-ready brief distinguishes grounded conformance repairs from ungrounded causal dynamics and records exact ancestor commits plus artifact hashes"
    requirement: RUN-01
    verification:
      - kind: unit
        ref: "tests.phase46.test_gate_composition + tests.phase46.test_validation_wiring + tests.phase50.test_causal_telemetry + tests.phase50.test_evidence_builder + tests.phase50.test_band_record + tests.phase50.test_candidate_finalization + tests.phase50.test_evidence_verifier"
        status: pass
      - kind: other
        ref: "verify_phase50_evidence.py terminal --manifest terminal-manifest.json"
        status: pass
      - kind: other
        ref: "! grep '\"band_generation\": 4' evidence/run-ledger.md"
        status: pass
    human_judgment: false
  - id: D2
    description: "Owner records a bounded preregistration decision in the reserved JSON block"
    requirement: RUN-02
    verification:
      - kind: other
        ref: "commit blob SHA-256 matches Decision-Summary-SHA256 trailer"
        status: pass
    human_judgment: true
    rationale: "gate=blocking-human; Task 2 records the verbatim owner response. Owner selected stop-incomplete 2026-08-17."

duration: 6min (Task 1) + owner-checkpoint wait + <5min (Task 2)
completed: 2026-08-17
status: closed-incomplete
---

# Phase 50 Plan 08: Owner Preregistration Decision Brief

**Owner-ready D-19/D-20 brief after grounded conformance work: seed 41's invariant-B HALT was conforming, current sources ground no causal-front remedy, and no later-generation or launch authority exists until the owner selects one option.**

## Performance

- **Duration:** 6 min (Task 1 only)
- **Started:** 2026-08-15T13:36:00Z
- **Completed:** 2026-08-15T13:42:26Z
- **Tasks:** 1 of 2 (checkpoint reached; Task 2 not started)
- **Files modified:** 1 (this uncommitted brief)

## Owner decision requested

Per D-19 and D-20, the executor may not invent a causal-front remedy and may not convert a retry into a prediction. The owner — not this brief — decides whether an unchanged-recipe later generation may even be preregistered.

This checkpoint authorizes no process launch and does not reopen GAP-50-03.

### Options

| ID | Name | Effect if later selected |
|---|---|---|
| `authorize-preregistration` | Authorize unchanged-recipe preregistration | Permits Plan 50-09 to prepare an immutable later-generation experiment definition under SCOPE-29. Causal-front success remains uncertain. Does **not** authorize smoke or graded launch. |
| `supply-grounded-remedy` | Supply a grounded causal remedy | Stops this plan set before preregistration. The remedy must be researched and replanned; it is not inserted during execution. |
| `stop-incomplete` | Stop with Phase 50 incomplete | Avoids further compute without a grounded expectation of causal-front success. RUN-01 and RUN-02 remain unsatisfied. |

**Resume signal:** Select exactly one of `authorize-preregistration`, `supply-grounded-remedy`, or `stop-incomplete`, and include the explicit scope acknowledgment.

**No option is selected here.**

## Readiness independently confirmed

HEAD at this brief: `565607f9a4799fa21055beb3278e964ce1ddf0b3` (`docs(50-07): complete normal evidence tooling plan`) on `milestone/v2.2`.

Named Task 1 suite and source files are byte-identical to that HEAD (working-tree diff 0 bytes). The orchestrator already ran the Task 1 automated suites at this same HEAD (92 tests OK; `TERMINAL-EVIDENCE-OK`). This executor therefore cites that run rather than re-executing it, and independently confirmed ledger, generation-4 absence, GAP-50-03 identity, and artifact SHA-256 values.

### Exact passing test commands

```bash
<home>/miniforge3/bin/conda run -n pinn-train python -m unittest \
  tests.phase46.test_gate_composition \
  tests.phase46.test_validation_wiring \
  tests.phase50.test_causal_telemetry \
  tests.phase50.test_evidence_builder \
  tests.phase50.test_band_record \
  tests.phase50.test_candidate_finalization \
  tests.phase50.test_evidence_verifier -v
```

Result cited: **92 tests OK** at HEAD `565607f9`.

```bash
<home>/miniforge3/bin/conda run -n pinn-train python \
  .planning/phases/50-valid-stage-0-re-run/evidence/verify_phase50_evidence.py terminal \
  --repo-root <home>/Desktop/3_body_problem/.worktrees/trainex \
  --manifest .planning/phases/50-valid-stage-0-re-run/evidence/terminal-manifest.json
```

Result cited: **TERMINAL-EVIDENCE-OK**.

Independent this-dispatch checks:

```bash
! grep -q '"band_generation": 4' \
  .planning/phases/50-valid-stage-0-re-run/evidence/run-ledger.md
```

Result: **pass**. Ledger `band_generations` are `[1, 2, 3]`, all `status=terminal`. Record generations are `{1, 2, 3}`. `final_band_generation` is `null`. No `identity-baseline-generation-4.json`, `band-record.md`, `candidate-receipt.json`, `runs/stage0-rerun-seed42`, or `runs/stage0-rerun-seed43` exists.

## Full committed Plan 50-06 and Plan 50-07 commit IDs

All of the following are ancestors of HEAD `565607f9a4799fa21055beb3278e964ce1ddf0b3`.

### Plan 50-06 (six commits)

| Commit | Subject |
|---|---|
| `7a587f9ff4f38d3b0df19c21805c9fcf39c2325c` | `test(50-06): add failing mps validation conversion regression` |
| `169b7abea283131dfbec956843eed6093103e319` | `feat(50-06): convert mps predictions to cpu before float64` |
| `9b0311d74fbb301e4c8afa9e44985bd24d4cf994` | `test(50-06): add failing causal telemetry ownership regression` |
| `1c4836cb62d470e39af8ebaa82bd02a6f303db69` | `feat(50-06): snapshot training causal stats before validation` |
| `f9679f86d75882feed79224f18480e59652f23f6` | `fix(50-06): record bounded causal-front diagnosis` |
| `f339179e40ae0a4b80f999d321dcb7e1cf3b0699` | `docs(50-06): record plan progress in state and roadmap` |

Verifier reserved single ancestor (unfilled in JSON below): last Plan 50-06 commit `f339179e40ae0a4b80f999d321dcb7e1cf3b0699`.

### Plan 50-07 (seven commits)

| Commit | Subject |
|---|---|
| `ad16e0a9e6d345b58f3399cca34f64aaecdb3288` | `test(50-07): add failing tests for extract and identity` |
| `470c0a137ba98bba5f6e5786e1b384564adbb800` | `feat(50-07): implement extract identity and manifest checks` |
| `64ba3acbb8a90b59659f8f40467261323216c6b8` | `test(50-07): add failing tests for attempt and band` |
| `60622a681ecc19e95611c7f9ff83d1a75be9a6df` | `feat(50-07): implement attempt verifier and descriptive band` |
| `1b044350376553ead683a8e3df9c8124bf04a176` | `test(50-07): add failing tests for candidate and finalize` |
| `8786f17b7f17fddfadb06f29eda070ca6652bfe2` | `feat(50-07): implement candidate finalize and all` |
| `565607f9a4799fa21055beb3278e964ce1ddf0b3` | `docs(50-07): complete normal evidence tooling plan` |

Verifier reserved single ancestor (unfilled in JSON below): last Plan 50-07 commit `565607f9a4799fa21055beb3278e964ce1ddf0b3`.

## Validation-conversion disposition

**Repaired.** This is a proven D-19 conformance defect, not a causal-dynamics finding.

Production `compute_validation_gate` used a one-step MPS-to-CPU/`float64` cast that torch 2.12.1 rejects. The locked metric adapter already requires detach → CPU → then `float64`. Plan 50-06 repaired only the prediction conversion. Metric, frame, population, thresholds, cadence, and fail-closed exception semantics are unchanged.

This repair explains the seed-41 `gate_status=failed:TypeError` rows. It did not cause the invariant-B HALT: the guard runs before validation.

## Telemetry-overwrite disposition

**`telemetry_overwrite_proven: true`.** Validation compose overwrote `_last_widened_details` between StepGuards and `_log_step` on both the Adam (`phase=2a`) and L-BFGS (`phase=2b`) validation-step boundaries.

Plan 50-06 took an immutable training snapshot of `w_n_stats` and residuals immediately after the training compose and passed those explicit values to `_log_step`. Guard ordering and the causal formula are unchanged. This is D-24 provenance, not a causal-dynamics remedy, and cannot have caused the seed-41 HALT.

## `grounded_causal_front_repair`

**`grounded_causal_front_repair: none-in-current-sources`.**

**`later_generation_likelihood_claim: prohibited`.**

**`causal_front_behavioral_remedy: none`.**

The invariant-B HALT, the locked prefix-exponential formula, the locked `N=500` window, and `front_idx=0` on the retained seed-41 log are internally consistent. Current sources identify no wrong literal, no guard defect, and no authorized recipe change. Plan 50-06 recorded that classification and did not infer, implement, or automatically repair causal dynamics from `front_idx=0`.

## Retained seed-41 invariant-B facts

Cited from the already-committed generation-3 terminal record. These numbers justify no recipe edit (D-19 / SCOPE-29 / D-20).

- `evidence/attempts/stage0-rerun-seed41-attempt-02/failure/trip.json`: `guard=invariant_b`, `disposition=HALT`, `step=501`, `threshold=500.0`, `threshold_provisional=false`, `metric=steps_since_front_advance`, `value=501.0`, reason `"causal front high-water mark did not advance within N=500 steps"`.
- `50-05-SUMMARY.md` / `50-VERIFICATION.md`: `front_idx=0` on all 502 logged steps; seeds 42 and 43 were not launched; `final_band_generation` is null.
- `configs/stage0-rerun-seed41.yaml`: `front_advance_window_n: 500`, `max_epochs: 1000`, `n_adam: 1000`, `validation_every: 100`, `lambda_e_max: 0.0`, `replay_count` unset (DATA-05 default 240). Neither 50-06 nor 50-07 edited this file.
- Five validation events exist with `gate_status=failed:TypeError` and no sidecar. That is the validation-conversion class above. It did not cause the HALT.

With `eta_c = 1`, `front_idx = 0` means `w_1` is the last (and first) weight above 0.5, equivalently that the first-bin mean squared residual was not below `ln(2)` at the evaluated step. That is an algebraic consequence of the implemented formula, not a diagnosis of why the residual stayed there. A HALT at step 501 after `front_idx` stayed 0 is the defined GATE-03 / D-20 gate, not a crash.

## Consulted artifact SHA-256 values

Working-tree bytes match the HEAD blobs.

| Path | SHA-256 |
|---|---|
| `.planning/phases/50-valid-stage-0-re-run/50-06-SUMMARY.md` | `205b23d280967c7407924239fcac45db4d3bf1b531aee26ce6b5838a8532e6d0` |
| `.planning/phases/50-valid-stage-0-re-run/50-07-SUMMARY.md` | `3e651ff34e31df4c68fb2cd885f00fe6936eb37c7a36649ce9680c4851bec14f` |
| `.planning/phases/50-valid-stage-0-re-run/50-RESEARCH.md` | `f1dbf75a6ad75608f7899b83d5d57b426789c380aff269456a16c23cfccec972` |
| `.planning/phases/50-valid-stage-0-re-run/50-VERIFICATION.md` | `3b77cdf945836cfe6f1e68eb5db4dc1c7a81c08dbda03d8cca603fa2912e065c` |
| `.planning/phases/50-valid-stage-0-re-run/50-GAPS.md` | `13422b26653ba93ae4ba1cbc700d67b8a75c93e42844216683a12b7929a15da3` |

`50-GAPS.md` last committed at `cb4df9c9df1c93beca13c3caf98271b2f9cc2f57`. Working tree matches HEAD. GAP-50-03 remains `RESOLVED-WITH-INSTRUCTION` Option A (2026-08-15): accept the generation-3 HALT record; no band; seeds 42/43 stay unlaunched; `N=500` unchanged; no later generation until separately authorized. **GAP-50-03 is read-only history.** This brief does not edit, reopen, reinterpret, or resolve it.

## Plain statements required by Task 1

- Removing observation defects does not predict causal-front advance.
- Successful conformance repairs (validation conversion; telemetry ownership) do not establish that the locked causal recipe will advance within `N=500`.
- No new generation authority exists.
- No smoke, graded-seed, or other launch authority exists.
- Completing this brief is not Phase-50 goal completion. RUN-01 and RUN-02 remain unsatisfied. ROADMAP success criteria 2 and 3 remain false.
- GAP-50-03 is read-only history.

## Reserved owner-decision JSON (Task 2)

The following `phase50-owner-preregistration-decision/v1` block is reserved for Task 2. Fields that only the owner or the post-answer recorder may fill are empty placeholders. **`selected_option` is not guessed.**

```json
{
  "schema": "phase50-owner-preregistration-decision/v1",
  "owner_response_verbatim": "stop phase 50 incomplete, route to v2.3 now",
  "selected_option": "stop-incomplete",
  "scope_acknowledgements": {
    "not_causal_success_forecast": true,
    "not_smoke_or_graded_launch_authority": true,
    "preserves_unchanged_recipe_n500_seed_order_no_held_out": true,
    "does_not_reopen_gap_50_03": true
  },
  "plan_50_06_commit": "f339179e40ae0a4b80f999d321dcb7e1cf3b0699",
  "plan_50_07_commit": "565607f9a4799fa21055beb3278e964ce1ddf0b3",
  "referenced_artifacts": [
    {"path": ".planning/phases/50-valid-stage-0-re-run/50-06-SUMMARY.md", "sha256": "205b23d280967c7407924239fcac45db4d3bf1b531aee26ce6b5838a8532e6d0"},
    {"path": ".planning/phases/50-valid-stage-0-re-run/50-07-SUMMARY.md", "sha256": "3e651ff34e31df4c68fb2cd885f00fe6936eb37c7a36649ce9680c4851bec14f"},
    {"path": ".planning/phases/50-valid-stage-0-re-run/50-RESEARCH.md", "sha256": "f1dbf75a6ad75608f7899b83d5d57b426789c380aff269456a16c23cfccec972"},
    {"path": ".planning/phases/50-valid-stage-0-re-run/50-VERIFICATION.md", "sha256": "3b77cdf945836cfe6f1e68eb5db4dc1c7a81c08dbda03d8cca603fa2912e065c"},
    {"path": ".planning/phases/50-valid-stage-0-re-run/50-GAPS.md", "sha256": "13422b26653ba93ae4ba1cbc700d67b8a75c93e42844216683a12b7929a15da3"},
    {"path": "docs/work/reviews/milestone_v2.2/50-valid-stage-0-re-run/2026-08-17-residual-frame-conformance-audit.md", "sha256": "3a0cd8ec2a230bdc26833719019ff673b7b0e47217ec7006a087c0e325cc40b1"}
  ]
}
```

**Owner decision recorded 2026-08-17.** The owner selected `stop-incomplete`. Verbatim response: "stop phase 50 incomplete, route to v2.3 now". No new generation, preregistration, smoke, or graded-seed launch authority exists. RUN-01 and RUN-02 remain unsatisfied. GAP-50-03 is unchanged, byte-for-byte historical context (Option A, 2026-08-15).

**Grounding added since Task 1.** Between Task 1 (2026-08-15) and this decision (2026-08-17), a bounded residual-frame conformance audit (`docs/work/reviews/milestone_v2.2/50-valid-stage-0-re-run/2026-08-17-residual-frame-conformance-audit.md`) closed the question this checkpoint was waiting on. It (a) refuted the only named code-defect hypothesis (a missing `u↔t` chain factor) on four independent grounds — dimensional closure of `D³=G·T²`, term-for-term spec conformance, training-residency frame consistency, and the committed Phase-38 dual-gate probe evidence; (b) established, by a read-only characterization of the locked architecture alone (no data, no optimizer, no training step), that `R̄≈10¹⁰` is set at initialization by the SIREN's second derivative and is seed- and IC-independent across six cases tried; and (c) concluded no dynamics remedy is available inside v2.2: `η_c`, the causal formula, and the residual normalization are framework-spec parameters, and SCOPE-30 forbids editing framework specs in this milestone. This directly informs the option selected here: `authorize-preregistration` would spend compute preparing a later generation of a recipe now shown to be in a deterministic, architecture-level saturated regime at step 0, independent of seed; `supply-grounded-remedy` has no legal path inside Phase 50. `stop-incomplete` is the only option consistent with the audit's own finding, and routes the milestone to v2.3 recipe adjudication per `.planning/REQUIREMENTS.md`'s existing "Future Requirements" entry (trainex-r2 resolution doc as premise-qualified candidate verdict source, SCOPE-29/31).

This selection and its grounding do not reopen GAP-50-03, do not reinterpret the invariant-B HALT, and do not constitute a later-generation-likelihood forecast (`later_generation_likelihood_claim: prohibited` stands): the audit's finding is a property of the locked architecture at initialization, not a prediction about what a further-trained run would do.

Task 2 records the owner's response verbatim, the exact selected option, explicit scope acknowledgements, both source commit IDs, and the path/SHA-256 references from this brief, per the plan's `phase50-owner-preregistration-decision/v1` schema. Only `authorize-preregistration` may continue to Plan 50-09; that option was not selected. This is a committed blob, not a working-tree draft — see Task Commits below.

## Accomplishments

- Independently confirmed readiness: suites pass at HEAD `565607f9`, terminal evidence is OK, ledger has no generation beyond 3 and no final generation.
- Wrote this owner-ready brief with exact test commands, all Plan 50-06/50-07 commit IDs, both dispositions, `grounded_causal_front_repair: none-in-current-sources`, retained seed-41 facts, and artifact SHA-256 values.
- Reserved an empty decision JSON block. Created no generation-4 artifact, invocation, preregistration, or launch.

## Task Commits

1. **Task 1: Prove the decision boundary from conformance results to an owner-ready brief** — folded into the Task 2 commit below (Task 1 alone was never committed per dispatch; the plan forbids committing `50-08-SUMMARY.md` until Task 2 records the owner answer).
2. **Task 2: Decide whether an unchanged-recipe later generation may be preregistered** — committed via `scripts/agent-commit`; see commit SHA and `Decision-Summary-SHA256` trailer recorded at close of this file.

## Files Created/Modified

- `.planning/phases/50-valid-stage-0-re-run/50-08-SUMMARY.md` — owner-ready brief plus the committed `stop-incomplete` decision (this file)

No recipe, config, ledger, gap register, preregistration, or experiment artifact was edited.

## Decisions Made

- **Owner selected `stop-incomplete`** (2026-08-17; verbatim: "stop phase 50 incomplete, route to v2.3 now"). Phase 50 stops with RUN-01/RUN-02 unsatisfied. No preregistration, smoke, or graded-seed launch authority is created. GAP-50-03 is unchanged.

## Deviations from Plan

None - plan Task 1 executed exactly as written.

**Total deviations:** 0
**Impact on plan:** None.

## Issues Encountered

None. The generation-3 invariant-B HALT and the now-repaired observation defects remain historical facts. GAP-50-03 Option A is untouched.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

**Plan 50-09 is not authorized.** The committed `selected_option` is `stop-incomplete`, not `authorize-preregistration`; per the plan's own gate, only `authorize-preregistration` may continue to Plan 50-09.

**Phase 50 is closed incomplete.** RUN-01/RUN-02 remain unsatisfied. `final_band_generation` remains null. Routing: v2.3 recipe adjudication (see `.planning/REQUIREMENTS.md` "Future Requirements"; trainex-r2 resolution doc is the premise-qualified candidate verdict source, SCOPE-29/31). Downstream milestone-level disposition (Phase 51 EVAL-01 handling, Phase 52 adapted handoff, v2.2 archival) is recorded separately per owner instruction 2026-08-17.

## Self-Check: PASSED (Task 1 and Task 2)

- Readiness suites and terminal verifier: cited passing orchestrator run at HEAD `565607f9` (Task 1); independently re-confirmed 2026-08-17 that no `pinn/` or `tests/` file changed between `565607f9` and current HEAD (`git diff --stat` empty), so the cited pass remains valid evidence — not re-run, per unchanged-inputs reuse.
- Ledger re-checked 2026-08-17: no `"band_generation": 4` entry.
- Brief distinguishes grounded conformance defects from ungrounded causal dynamics.
- No generation-4 artifact, invocation, or final generation exists.
- GAP-50-03 remains unchanged and is treated as read-only.
- `grounded_causal_front_repair` is present in this file.
- Decision JSON `selected_option` is `stop-incomplete`, owner-selected, not inferred.
- **`verify_phase50_evidence.py identity --state authorization` is not run for this branch.** Its `cmd_identity` hard-codes `expected_option="authorize-preregistration"` (script line ~1080) — it validates only the branch that continues to Plan 50-09. For `stop-incomplete` this check is structurally inapplicable, not skipped for convenience; completion is instead verified by the SHA-256/commit-trailer match on the committed blob, per the plan's generic Task 2 acceptance criterion.

---
*Phase: 50-valid-stage-0-re-run*
*Task 1 completed: 2026-08-15*
*Task 2 completed: 2026-08-17*
*Status: CLOSED — incomplete (RUN-01/RUN-02 unsatisfied; routed to v2.3)*
