# Phase 46: Frame Resolution & Gate-Aligned Validation - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution
> agents. Decisions are captured in `46-CONTEXT.md`; this log preserves the
> alternatives considered.

**Date:** 2026-07-25

**Phase:** 46-frame-resolution-gate-aligned-validation

**Mode:** `--all` with owner-delegated automatic selection — all discussion
areas covered, the recommended default selected for each without prompting.
The user's bare `auto` instruction applies to discussion choices only; it does
not auto-chain planning or execution. Single discussion pass.

**Areas discussed:** Stored-target frame probe, frame-defect branch handling,
validation metric cadence and isolation, metric persistence and failure
semantics, regression coverage.

---

## Stored-target Frame Probe

| Decision point | Selected default | Alternatives considered |
|---|---|---|
| Data surface | Probe the exact `StageIndex.snapshot_positions` surface consumed by `sample_data_points`; raw corpus and canonical preprocessing are controls. | Raw corpus files only; code inspection only. |
| Population | Every eligible Stage-0 identity in frozen train and validation views, deterministic key order; exclude test. | Deterministic sample only; all splits including test. |
| Hypothesis comparison | Symmetric raw/scaled residual arms over identical resident targets and times, using locked `D`/`T` and coherent `u=t/T`; report both distributions. | Test only the expected scaled arm; infer the result from storage code. |
| Positive/provenance controls | Canonical full preprocessing is the positive control; parsed raw positions with matching raw metadata are the provenance control. | No controls; compare two unlabeled aggregate means. |
| Other transform seams | Make mass order, COM/boost, rotation gauge, and scale explicit so a non-scale data-path mismatch cannot masquerade as frame noise. | Collapse every mismatch into a raw-vs-scaled label; repair unexpected seams inline. |
| Verdict rule | Require finite, reproducible, theory-consistent separation and control agreement; derive only representation tolerances, not a new physics threshold. | Reuse the Phase 38 one-fixture threshold as a new lock; choose whichever arm has the lower mean. |
| Evidence scope | Versioned population-level JSON plus Markdown rendering with repository/data/split provenance, stable identities, arm definitions, exclusions, and distributions. | Console-only result; one scalar without per-trajectory evidence. |

**Selection source:** The owner delegated all choices to the agent's judgement.

**Notes:** Code inspection identified the resident-target seam as suspicious,
but that observation is deliberately not treated as the verdict. The empirical
probe must settle CONF-01.

---

## Frame-defect Branch Handling

| Decision point | Selected default | Alternatives considered |
|---|---|---|
| Delivery order | Resolve CONF-01 before implementing frame-dependent INST-01 behavior. | Implement both in parallel; add metrics first and revisit their frame later. |
| Conformant result | Record clean evidence, leave the data path unchanged, then implement validation metrics in the confirmed frame. | Rewrite the target path anyway; omit evidence because inspection looked clean. |
| Confirmed wrong frame | Stop frame-dependent work, record the sixth data-path divergence in `46-GAPS.md` and the v2.2 index, and surface the required owner scope decision. | Silently repair the adapter in Phase 46; defer the finding while continuing dependent work. |
| Ambiguous/non-finite result | Preserve measurements and fail closed into the governed semantic-gap path. | Pick the numerically smaller arm; expand into a training experiment. |
| Unexpected non-scale data-path defect | Route through the same owner checkpoint because it changes the validity and scope of the target path. | Treat it as incidental; absorb it without a scope ruling. |

**Selection source:** The owner delegated defaults, but the wrong-frame owner
checkpoint itself is roadmap-mandated and cannot be auto-decided.

**Notes:** Phase 47 is frame-dependent because `H' = D H`; a forced or
inspection-only verdict would contaminate the rest of v2.2.

---

## Validation Metric Cadence and Isolation

| Decision point | Selected default | Alternatives considered |
|---|---|---|
| Cadence | Run conservation observation at every existing validation event; introduce no new cadence option. | Terminal-only metrics; independently configurable cadence. |
| Evaluated records | Complete sorted validation population eligible at the current stage via `records_at_or_below(stage)`. | Reuse the random validation-loss batch; undocumented fixed panel. |
| Forward pass | Detached full-trajectory `model.eval()` / `torch.no_grad()` pass with prior model mode restored. | Grad-enabled diagnostic; leave the model in eval mode after the observation. |
| Coordinate/time pair | Use the coherent pair established by CONF-01; under the locked contract this is `r'` with `u=t/T`, so finite differences produce `dr'/du`. | Mix scaled position with native time; leave the convention implicit. |
| Metric implementation | Compose `pinn.verification.gate_metrics`; do not duplicate finite difference, Hamiltonian, aggregation, SCS, or verdict formulas. | Duplicate formulas in the trainer; call the held-out evaluator. |
| Per-trajectory output | Record every trajectory's `epsilon_H` and diagnostic SCS with canonical identity. | Aggregate-only record; discard per-trajectory identity. |
| Aggregate headline | Worst-trajectory maximum, with aggregate SCS derived from it; distributions are descriptive only. | Mean headline; median headline; competing headline statistics. |
| Training influence | Observation only: no loss, stage, optimizer, replay, checkpoint, early-stop, or recipe effect. | Rank checkpoints by `epsilon_H`; stop or tune when the metric worsens. |
| Held-out protection | Validation helper receives validation only, never constructs/reads test and never imports/calls `pinn.evaluate`. | Generic helper permitted to consume any split; preview test when validation is inconclusive. |
| Existing metric contract | Integrate verified functions without reopening component math; surface a real caller/spec conflict as a gap. | Opportunistically change the held-out evaluator or redefine metric units. |

**Selection source:** The owner delegated all implementation-mechanics choices.
Split isolation, no tuning, and the single-look budget are hard v2.2
constraints rather than discretionary defaults.

---

## Metric Persistence and Failure Semantics

| Decision point | Selected default | Alternatives considered |
|---|---|---|
| Per-event persistence | Atomically publish one versioned per-trajectory sidecar, then append compact aggregate fields and a run-relative pointer to `validation.jsonl`. | Inline every trajectory in JSONL; persist aggregate numbers only. |
| Artifact identity | Record schema/run identity, step, stage, validation split, CONF-01 evidence reference, coordinate/time convention, and sorted `RecordKey` rows. | Anonymous scalar metrics; held-out receipt schema copied verbatim. |
| Metric fields | Per-trajectory `epsilon_H`/SCS, non-finite count, locked thresholds, worst-case aggregate, aggregate SCS, and diagnostic PASS/FAIL. | Drop non-finite rows; omit thresholds or coordinate convention. |
| Headline and diagnostics | Worst-case maximum is authoritative; means/quantiles/fractions may be labeled diagnostics only. | Mean or median replaces the gate headline. |
| Terminal projection | Project the latest durable aggregate, sidecar pointer, validation step, and model-state association into the terminal summary. | Rely on console output; check only that `validation.jsonl` exists. |
| EVAL-01 eligibility | No durable schema-valid validation metric means the run is ineligible for held-out evaluation. | Treat loss-only validation as sufficient. |
| Instrumentation failure | Empty pool, compute/schema error, or persistence failure fails the instrumentation path closed. | Warn and continue without metrics. |
| Numeric metric failure | Persist a genuinely computed non-finite/high `epsilon_H` honestly as FAIL, without changing the recipe or training controls. | Drop failing trajectories; use the result to tune automatically. |
| Publication ordering | Sidecar must be durable before JSONL advertises its pointer. | Append pointer first and repair missing sidecars later. |

**Selection source:** The owner delegated all defaults. Fail-closed eligibility
and observation-only behavior follow EVAL-01 and SCOPE-29.

---

## Regression Coverage

| Decision point | Selected default | Alternatives considered |
|---|---|---|
| Frame probe unit cases | Synthetic raw and processed/scaled encodings with locked `D`/`T`, plus canonical positive control. | Real-corpus-only test; snapshot the current code-inspection conclusion. |
| Population boundaries | Test deterministic ordering, train/validation inclusion, test exclusion, and canonical identity retention. | Rely on review; allow random sampling. |
| Confound/failure cases | Test mismatched body-order/metadata controls, ambiguous arms, and non-finite fail-closed behavior. | Treat confounds as noise; force a verdict. |
| Gate composition | Extend Phase 43 boundary/non-finite fixtures and add a small multi-trajectory validation integration seam. | Build a second metric implementation; test a happy-path scalar only. |
| Aggregate correctness | Assert per-trajectory values, maximum aggregation, SCS derivation, exact strict boundary, and sorted identity. | Assert only that output exists. |
| Isolation | Assert validation-only source, no test/evaluator path, model-state restoration, and no training-control changes. | Document prohibitions without executable tests. |
| Artifact durability | Dataset-free tests for atomic publication, schema, JSON-safe non-finites, JSONL linkage, summary projection, and missing/corrupt cases. | Require full corpus in the standing test suite; skip artifact tests. |
| Real-corpus role | One committed, re-derivable CONF-01 evidence run during Phase 46 execution. | Use the corpus as a non-deterministic unit-test dependency; omit real evidence. |

**Selection source:** The owner delegated all choices to the agent's judgement.

---

## Codex's Discretion

The owner explicitly delegated every discussion-area selection. The planner
retains discretion over focused helper names, evidence/sidecar filenames,
sidecar directory layout, deterministic batching/chunking, and descriptive
distribution fields. It has no discretion to alter the CONF-01 branch,
introduce a verdict threshold, use the test split/evaluator, tune from observed
metrics, edit framework specs, or consult trainex-r2 as grounding.

## Deferred Ideas

- Any target/data-path repair discovered by CONF-01 — owner checkpoint first.
- `S_H` and loss-math conformance — Phases 47–48.
- General conformance enforcement — Phase 49 / charter workstream.
- Stage-0 rerun and the single held-out evaluation — Phases 50–51.
- Recipe tuning / trainex-r2 remedy adjudication — v2.3.
- D-06 static-epsilon sensitivity check — remains an unlinked pending todo and
  is not folded into v2.2.
