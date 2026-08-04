---
status: complete
phase: 48-loss-math-conformance
source:
  - 48-01-SUMMARY.md
  - 48-02-SUMMARY.md
  - 48-03-SUMMARY.md
  - 48-04-SUMMARY.md
started: 2026-08-03T04:54:57Z
updated: 2026-08-04T01:12:34Z
verify_pre_gates:
  - capId: ai-integration
    check: api-coverage.verify-pre
    block: false
    message: "api-coverage: no external-API integration detected; coverage matrix not required"
---

## Current Test

[testing complete]

## Tests

### 1. Conformance deliverables — independently re-verified
expected: |
  13/13 coverage entries auto-covered (48-01 D1-D3, 48-02 D1-D3, 48-03 D1-D3,
  48-04 D1-D4), each with a passing named test ref and human_judgment: false.

  Independent re-verification performed this session (46 checks, all passing),
  written from the spec text rather than from the phase's own test helpers:
  - CONF-04: Rbar == (1/3) sum_i ||f_i||^2 against a per-body hand oracle; the
    value is exactly 3x the former /9 component mean.
  - CONF-07: L_data == sum(Huber)/(9*N_t) against a two-branch float64 oracle at
    N_t in {1, 2, 5, 11}.
  - CONF-05: invariant A holds strictly (0 < w_n <= 1) on CPU float32/float64
    and on the real locked MPS float32 backend (torch 2.12.1); w_1 == 1.0
    exactly; the clip is a bit-exact no-op above the floor; the causal weight
    is genuinely stopgrad (grad == w_n / N_t).
  - CONF-06: lambda_e_max is exact 0.0 from the dataclass default, from both
    shipped YAML files through the real loader, and through ScheduledWeights at
    every schedule state (warmup, saturation, freeze, rewarm).
  - INST-02: telemetry writes no parameter .grad; each raw norm matches an
    independent autograd oracle; applied == lambda * raw exactly; zero lambda_e
    yields exact 0.0 applied with a nonzero raw; graphless terms record 0.0;
    missing terms record null and force incomplete; a released graph returns
    None rather than a fabricated number.
  - TEST-01: both divergence-defending tests corrected (phase38 causal
    underflow now asserts strict positivity; phase41 keyed-YAML now expects 0.0).
  - TEST-02: the Rbar seam test intercepts the real controller-to-catalog
    argument; the phase47 eps_H exact-value boundary test is retained and green.

  Full cross-phase regression aggregate (the figure the phase's own verification
  report could not capture): 729 passed, 3 skipped, 279 subtests passed in 418s
  over tests/phase38 phase40 phase41 phase42 phase46 phase47 phase48. The 3
  skips are pre-existing environment-conditional phase42 residual-panel tests.

  Scope: no framework-spec, evaluator, trainex-r2, or recipe file in the phase
  diff; git diff --check clean; all 19 declared commits present in history.
  GAP-45-01 was resolved by a real owner ruling on 2026-07-31 with both
  reduction magnitudes presented (0.1539..0.1630 vs 1.3852..1.4673, exactly 9x).
result: pass

### 2. step_completed now depends on telemetry completeness
expected: |
  _log_step emits `step_completed = step_completed AND grad_stats_complete`
  (pinn/training/controllers.py:944). A step where the optimizer advanced
  normally but any of the ten gradient norms is missing or non-finite is
  recorded in canonical JSONL as `step_completed: false`.

  This was ratified in advance (48-CONTEXT.md D-20:166-171, 48-04-PLAN.md:112),
  so it is not an invented behavior. An independent grep confirms the summary's
  enumeration: `step_completed` appears only in the controller (producer) and
  step_log.py (registry) — zero production consumers today, so it is currently
  inert.

  Confirm you accept that the canonical completion field is a telemetry-health
  field rather than an optimizer-advancement field, and that Phase 49's gate
  must not read it as optimizer progress.
result: pass
initial_result: issue
gap_id: G-48-2
reported: "what do you recommend? is this better? / proceed as your recommended option"
severity: minor
resolution: |
  Owner ratified the recommended option 2026-08-03: KEEP the AND logic, RENAME
  the emitted field. The registry already declared this field as
  "EMISSION-COMPLETENESS METADATA ... the step record was fully assembled"
  (step_log.py), so the logic was definitionally correct; the NAME was the
  liability. Field was marked `provisional: True / owner-ratify before run #1`,
  so this is the scheduled ratification.

  Applied in this session:
  - emitted JSONL field `step_completed` -> `record_complete`
    (pinn/training/controllers.py:949, pinn/training/step_log.py registry key)
  - `_log_step`'s `step_completed` PARAMETER and its 8 guard/failure call sites
    are unchanged — that argument carries the call-site optimizer fact, which is
    a different question and is correctly named.
  - registry provenance rewritten to state explicitly that the field is NOT an
    optimizer-advancement flag and to route the two underlying questions.
  - test assertions updated in tests/phase42/test_step_log_jsonl.py and
    tests/phase48/test_gradient_observability.py (emitted-field reads only).
  Validation: tests/phase42 + tests/phase48 -> 70 passed, 3 skipped
  (pre-existing env-conditional), 4 subtests passed. Full cross-phase sweep
  after the rename -> 729 passed, 3 skipped, 279 subtests passed: byte-identical
  to the pre-rename baseline, so the rename is regression-neutral.

  Known consequence (accepted, no code impact): historical run records carry
  `step_completed` (e.g. v2.1 Phase-44 forensics evidence
  diag02/loss_decomposition.json); Phase 50 onward emits `record_complete`.
  No code or runbook reads either name. The step log has no schema-version
  constant to signal the change, unlike training_metadata.json's v2 bump.
result_after_fix: pass

### 3. Always-on instrumentation cost, no configuration knob
expected: |
  Under locked D-16, every Adam optimizer step and every L-BFGS closure
  evaluation performs five additional autograd.grad backward traversals to
  produce the per-term norms. There is intentionally no config knob to disable
  it (48-04-SUMMARY.md Phase-50 handoff).

  This is a real wall-clock multiplier on the backward pass, and L-BFGS
  evaluates its closure several times per optimizer step, so the multiplier
  compounds there. Phase 50's Stage-0 rerun budget must be planned against the
  instrumented cost, not the pre-Phase-48 cost.

  Confirm you accept always-on instrumentation for the Phase-50 rerun.
result: pass
note: |
  Accepted 2026-08-03. Carry-forward obligation for Phase 50 planning: budget
  the Stage-0 rerun against the INSTRUMENTED backward cost. The L-BFGS
  multiplier is 5 x (closure evaluations per optimizer step), not 5.

### 4. Schema-v2 metadata bump refuses pre-Phase-48 resume
expected: |
  TRAINING_METADATA_SCHEMA_VERSION is now 2 with five required causal-clip
  fields. Any run whose training_metadata.json predates Phase 48 is refused on
  resume with an explicit "regenerate run metadata via fresh setup" message.

  This is intended fail-closed behavior — a pre-Phase-48 run is non-conformant
  by definition, which is the whole premise of v2.2 — but it does mean no
  in-flight run started before this phase can be resumed; it must be restarted
  from fresh setup.

  Confirm no in-flight run needs to survive this bump.
result: pass
note: |
  Accepted 2026-08-03. Verified concretely during UAT: `find . -name
  training_metadata.json` returns zero artifacts, so no in-flight run is
  stranded. The refusal path is defensive-only until Phase 50 writes the first
  schema-v2 artifact.

## Causal clip bound — recorded numerics (CONF-05 recording obligation)

Measured this session on both dtypes and both backends. Re-derivable via
`pinn.loss_catalog.resolve_causal_clip_facts(dtype, device)`.

| precision | device | causal_clip_exponent_floor | causal_clip_min_weight |
|---|---|---|---|
| float32 | cpu | -87.33654022216797 | 1.175499675756452e-38 |
| float32 | mps (torch 2.12.1) | -87.33654022216797 | 1.1754998158862984e-38 |
| float64 | cpu | -708.3964185322641 | 2.2250738585072626e-308 |

The float32 CPU/MPS min weights differ by one ulp from the same exponent floor
— the documented backend-kernel difference that 48-03 preserved deliberately.
Formula `exp(clamp_min(x_n, causal_clip_exponent_floor))`, provenance
`log_smallest_normal:directed_up`. Both floors verified >= mathematical
log(finfo(dtype).tiny).

### 5. Two residual robustness notes (advisory)
expected: |
  Neither is a conformance failure; both are places where a future change could
  silently break a currently-correct guarantee.

  (a) CONF-05 asks that the chosen bound be recorded "in the plan and the run
  record". The plan records the derivation *rule* (upward-directed representable
  log(finfo.tiny)); the numeric floors are in the per-run metadata artifact and
  in this session's evidence (float32 -87.33654022216797 -> min weight
  1.175499675756452e-38 on CPU and 1.1754998158862984e-38 on MPS, one ulp apart
  as documented; float64 -708.3964185322641 -> 2.2250738585072626e-308). A rule
  is arguably stronger than a literal, but the plan text does not state the
  number.

  (b) In the L-BFGS closure the "raw" data-gradient norm is read from the
  accumulated parameter .grad after accumulate_chunked_data_term, which applied
  weights.lambda_data. That is correct today only because LossWeights hard-
  rejects lambda_data != 1.0 (pinn/loss_catalog.py:155). If that constraint ever
  loosens, grad_norm_raw_data silently becomes weighted and grad_norm_applied_data
  double-weighted, with no test catching it.

  Confirm these are acknowledged as-is, or say if you want either tightened.
result: pass
note: |
  Closed 2026-08-04 under delegated judgment. Both recommendations stand:

  (a) Satisfied without editing the ratified plan. The measured floor/min-weight
  table above is now part of the phase record and is re-derivable via
  `resolve_causal_clip_facts(dtype, device)`. Rewriting 48-03-PLAN.md would
  falsify a historical decision document to satisfy a bookkeeping clause.

  (b) NO guard added, deliberately. `lambda_data == 1.0` is not a fragile
  accident: it is a spec-level lock (pinn_architecture.md 3.1, "data term
  unweighted") enforced by a RAISING validator at LossWeights construction
  (pinn/loss_catalog.py:155). Reaching the failure mode requires a framework-
  spec amendment, which v2.2 forbids outright (SCOPE-30). A second guard here
  would be speculative defensive handling against a state the type system
  already refuses to construct. Recorded as a Phase-49/50 handoff note instead.

## Summary

total: 5
passed: 5
issues: 1
issues_resolved_in_session: 1
issues_open: 0
pending: 0
skipped: 0

## Gaps

- gap_id: G-48-2
  truth: "The canonical JSONL completion field states what it means and cannot be misread as optimizer advancement."
  status: resolved
  reason: "Field named `step_completed` carried AND-ed telemetry-completeness semantics; name and meaning disagreed."
  severity: minor
  test: 2
  resolved_by: in-session fix (owner-ratified rename), not a gap-closure plan
  resolved_at: 2026-08-04
  artifacts:
    - pinn/training/controllers.py
    - pinn/training/step_log.py
    - tests/phase42/test_step_log_jsonl.py
    - tests/phase48/test_gradient_observability.py
  missing: []

**Gap-closure routing note.** The workflow's `diagnose_issues` ->
`plan_gap_closure` -> `verify_gap_plans` path was deliberately NOT run for
G-48-2. That path exists to diagnose and plan a fix for an OPEN issue; this one
was diagnosed, owner-ratified, fixed, and regression-verified inside the UAT
session itself (729 passed / 3 skipped / 279 subtests, byte-identical to the
pre-fix baseline). Spawning a planner to author a fix plan for an already-closed
gap would produce a plan with nothing to execute. No `gap_ids` plan exists for
G-48-2 by design, so `reconcile_gaps` on any future resume will correctly find
it already `status: resolved` rather than re-diagnosing it.
