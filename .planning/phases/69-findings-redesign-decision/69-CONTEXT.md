# Phase 69: Findings & Redesign Decision - Context

**Gathered:** 2026-11-08
**Status:** Ready for research and planning
**Decision authority:** The owner's accepted evidence-first recommendation
in `69-SPEC.md`, plus PROJECT.md's standing technical delegation.

<domain>
## Phase boundary

Synthesize v2.5's evidence about the v2.4 failure, reconcile the failed
recipe with the successful locked-network controls, and bring the owner
supported choices for v2.6 and trainex-r5. The synthesis may honestly leave
a causal mechanism open. Phase 69 preparation authorizes no new experiment
and selects no final redesign.

</domain>

<spec_lock>
## Requirements locked by SPEC.md

Three requirements are locked: VERD-01, VERD-02 and VER-23. Downstream
agents must read `.planning/phases/69-findings-redesign-decision/69-SPEC.md`
before research or planning. It defines the requirements, constraints,
acceptance criteria, edge coverage and scientific/authority prohibitions.

**In scope:**

- The one-page findings, with linked supporting evidence and exact sources.
- Read-only reconciliation of existing v2.4 and v2.5 records and the code
  revisions those records identify, including successful locked controls.
- Measured v2.5 compute accounting and the SCOPE-49 disposition history.
- Evidence-backed options, a conditional diagnostic recommendation and
  the owner's closing decision record, including explicit open choices.
- Final requirement-to-phase traceability and the v2.6 handoff.

**Out of scope:**

- New training, retries, continuation of frozen arms, or another general
  sweep. A focused follow-up requires its own prospective proposal,
  authorization, budget and pre-registration before execution.
- Architectural redesign, rebuilding, physics-pipeline repairs, framework
  amendments or moving locked values. These belong to authorized v2.6 work.
- Reopening Phase 68's C-7 ruling or deciding its deferred pass bars by
  inference. C-2 and C-4 through C-6 remain open until owner instruction.
- Assembling or conducting trainex-r5. This phase records whether and why
  the owner commissions it; any package is subsequent work.
- A graded run, new validation/test access or spending the preserved
  held-out evaluation. SCOPE-45 remains in force.

</spec_lock>

<decisions>
## Implementation decisions

### Evidence and claim strength

- **D-01: Carry forward the decision delegation.** The owner chooses
  scope, resources, acceptable outcomes and the reserved closing decisions.
  Agents perform the scientific analysis and technical implementation
  choices. The owner's instruction to proceed accepts the evidence-first
  sequence, not a particular redesign or a new run. Do not conduct another
  scientific interview for questions the sources and delegation answer.
- **D-02: Separate the hypotheses and their measured scope.** Report the
  three original suspects, splitting the pipeline into training settings
  and physics terms, plus the original probe lead. DIAG-09 retained the
  adjacent-time association; its causal explanation remains open. The
  EXP-03 rate-improvement hypothesis being refuted is not a withdrawal of
  that original association. The successful smaller network refutes
  parameter shortage for the tested supervised one-orbit task, not for
  full Stage 0 or unseen initial conditions. The yardstick identifies a
  measurement defect; it does not establish which neural-network pass bar
  is achievable, nor explain the data-only mean-position failure.
- **D-03: Preserve the time and authority of each result.** Read the
  committed predictions, reviews and owner rulings, not just phase
  verification summaries. Historical Phase 65/67 pages correctly describe
  GAP-59-08 as open at their time; the current synthesis must also cite the
  later Phase 68 ruling closing it. Preserve the historical bytes instead
  of rewriting those pages. Quote registered labels faithfully, including
  the EXP-03 confirmed-worsening contrast and all unsettled/ambiguous
  contrasts. A positive control is not an isolated-factor experiment.

### Failed-versus-successful recipe reconciliation

- **D-04: Begin with the matched records already available.** Compare the
  v2.4 r1-1632 and r1-851 records with the corresponding locked-architecture
  EXP-03 lr1e-4 controls, preserving the repeat seed as additional evidence.
  Identify the same system/seed where available; do not silently equate
  4658 with 851 or treat a second seed as a second physical system. The
  comparison is retrospective and descriptive. Retain the original full
  prediction/review context for the controls, not just their endpoint E.
- **D-05: Verify comparability before interpreting the difference.** Trace
  the recorded revisions and compare the actual architecture, initialization,
  input/target preparation, body order, gauge, normalization, window/grid,
  sample selection, loss/reduction, optimizer policy, clipping, polish,
  precision/device, update budget and scored-state selection. Distinguish
  a checked equivalence, a checked difference and a source-unresolved
  comparison. Current code can help locate the recorded implementation,
  but cannot substitute for it when a revision changed. Existing field
  names, evidence readers and source hashes are preferred over a new
  general reporting framework.
- **D-06: Preserve the decisive known facts without selecting a cause.**
  The locked 12-layer, width-256, first-frequency-30 controls at constant
  Adam 1e-4 reached settled Tier 1 position fits on 1632/42, 851/42 and
  1632/41. The old runs used a cosine starting at 1e-3, clipping and
  polish; the new controls did not use clipping or polish. These facts
  make a training-recipe explanation worth examining and prevent a claim
  that only a smaller architecture can fit. They do not isolate the
  historical cause, prove energy accuracy or establish generalization.
  Compare final and intermediate recorded states where relevant without
  inventing unrecorded scores or selecting a new winner after results.
- **D-07: Make further compute conditional on its decision value.** First
  state what the existing comparison resolves. For each remaining question,
  explain whether different answers would change the recommendation, such
  as repairing a training recipe versus replacing the architecture. Only
  then recommend a focused prospective comparison if warranted. Describe
  the confounds it must control and the scope/resource decision needed.
  Do not specify unresearched numeric defaults, continue a frozen arm,
  silently insert a phase, or launch anything from this context. Any
  experiment design, budget and reading rule require the applicable
  prospective workflow and owner authorization.

### Findings, cost and requirement accounting

- **D-08: Keep the main findings readable and the detail auditable.**
  Lead with the plain-language answer and its uncertainty. Use a compact
  suspect/status/evidence presentation, with the registered predictions
  and detailed recipe comparison linked nearby. Keep the main findings
  to the roadmap's one-page intent; use supporting tables for detail
  rather than filling the main page with raw records. No new word-count
  rule is imposed. Every empirical claim must identify its committed
  source revision or digest. Separate observations, interpretations and
  proposed actions in the prose.
- **D-09: Account for measured work without implying unknown totals.**
  Derive v2.5 costs from unique existing run/attempt records and their
  documented timing bases. Include recorded diagnostic training, timing
  and other measured activities; include any recorded failed or partial
  attempt rather than counting successful rows alone. Preserve a missing
  duration as unknown. Do not add optimizer time to a wall that already
  includes it, count the same control through several contrasts, mix
  incompatible wall definitions silently, or add v2.4 costs to v2.5.
  State the coverage of the total instead of calling it all Mac usage.
  The Phase 67 science subtotal is about 28 hours on its documented mixed
  record/launch-wall basis; it is not the entire milestone's cost.
- **D-10: Recheck mapping separately from completion.** Derive final
  requirement IDs and mappings from the live active milestone sources at
  closing time. Check set equality, duplicates, one phase per ID and
  referenced-phase existence. Keep the current count of 13 as orientation,
  not a constant that can conceal a later approved change. A mapped but
  open requirement is not necessarily satisfied. Report each actual
  SCOPE-49 proposal and owner disposition. In particular, EXP-03's
  authorization to continue did not amend the roadmap or registration.

### Closing checkpoint and v2.6 handoff

- **D-11: Present the completed evidence before the reserved choices.**
  Give the owner a recommendation with practical consequences and honest
  alternatives. Ask for the v2.6 direction and the trainex-r5 decision
  and question. Record the reply verbatim against the packet actually
  presented, with choices explicitly open if left open. The accepted
  preparation recommendation does not answer that checkpoint. The default
  order-A research purpose is redesign; do not switch to diagnosis merely
  because one ladder hypothesis was refuted. A diagnostic proposal that
  needs a SCOPE-49 or resource ruling has its own reserved decision.
- **D-12: Carry forward unresolved obligations without implementing them.**
  Hand off the Phase 68 autograd amendment routes and C-11 evaluation-text
  rewrite, C-2/C-4/C-5/C-6 still open, and the named physics-pipeline
  defects. Keep the unreachable production L-BFGS stage distinct from
  Phase 60's executed diagnostic polish. The energy-only constant-predictor
  pass remains relevant even after changing the velocity source. Stage 1+
  and PLAT-01 through PLAT-07 remain blocked. Any remaining causal or
  comparability uncertainty travels with the recommendation.

### Agent discretion for research and planning

Choose the smallest evidence inventory, source comparison and reporting
checks that can establish the specification's claims. Reuse existing
parsers and verifiers where they apply; establish any historical-reader
limitations before reuse. Do not turn a documentation phase into a
general experiment framework or add tests that merely assert the presence
of prose. Research should resolve the recorded recipe comparison and the
value of a focused follow-up, not select an unsupported architecture or
rerun a broad ladder. A source-silent semantic or scope decision outside
the delegation follows the STOP protocol. No such new decision is settled
by this context.

</decisions>

<canonical_refs>
## Canonical references

Downstream agents must read the relevant sources before planning. Paths
below are repository-relative. There is no new external candidate verdict
source for this phase; the owner decisions and committed experiments are
the grounding. A claim requiring external support must identify its source
and cannot be substituted for the local measured result.

### Scope, requirements and authority

- `.planning/phases/69-findings-redesign-decision/69-SPEC.md` - locked requirements and acceptance checks; read first.
- `.planning/ROADMAP.md` - diagnosis discipline and Phase 69 checkpoint.
- `.planning/REQUIREMENTS.md` - VERD-01, VERD-02, VER-23, SCOPE-45 through SCOPE-49 and named future defects.
- `.planning/PROJECT.md` - Current Milestone, order A, standing technical delegation and Mac constraint.
- `.planning/phases/64-feasibility-verdict/64-VERDICT.md` - v2.4 terminal reading and candidate directions.
- `.planning/phases/64-feasibility-verdict/64-CHARTER.md` - charter rows and explicitly open choices.

### Evidence and historical recipe

- `.planning/phases/65-probe-on-the-record-fit-harness/65-PROBE-PREDICTION.md` - original reproduction prediction.
- `.planning/phases/65-probe-on-the-record-fit-harness/65-FINDINGS.md` - reproduced association and its limits.
- `.planning/phases/65-probe-on-the-record-fit-harness/65-CLOSEOUT.md` - affected-use conditions and historical-reader limitations.
- `.planning/phases/66-small-network-control/66-PREDICTION.md` - multi-setting positive control and reading rule.
- `.planning/phases/66-small-network-control/66-RESULT.md` - replicated small-network fit and cited records.
- `.planning/phases/66-small-network-control/66-CHECKPOINT-1-RULING.md` - existing owner continue decision.
- `.planning/phases/60-single-system-learnability/evidence/arms/r1-1632/record.json` - historical same-system/seed recipe and states.
- `.planning/phases/60-single-system-learnability/evidence/arms/r1-851/record.json` - second-system historical recipe and states.
- `.planning/phases/67-design-settings-ladders/67-FINDINGS.md` - predictions, results, limitations and source index.
- `.planning/phases/67-design-settings-ladders/67-CLOSEOUT.md` - evidence coverage and accepted-use limits.
- `.planning/phases/67-design-settings-ladders/67-EVIDENCE-INDEX.json` - the committed phase audit index.
- `.planning/phases/67-design-settings-ladders/evidence/exp03/review.json` - exact locked-control E/tier, settle statuses and contrast readings.
- `.planning/phases/67-design-settings-ladders/67-EXP03-RULING.md` - scoped, digest-bound continue instruction.
- `.planning/phases/67-design-settings-ladders/evidence/exp03/science/main-1632-s42/lr1e-4/record.json` - successful matched locked-control settings, scores and timing.
- `.planning/phases/67-design-settings-ladders/evidence/exp03/science/repeat-851-s42/lr1e-4/record.json` - successful second-system control.
- `.planning/phases/67-design-settings-ladders/evidence/exp03/science/repeat-1632-s41/lr1e-4/record.json` - successful second-seed control.

### Yardstick, preserved contracts and handoff

- `.planning/phases/68-yardstick/68-AUDIT.md` - measurement routes and the constant-predictor limitation.
- `.planning/phases/68-yardstick/evidence/yardstick-audit.json` - exact audit values, source hashes and access attestation.
- `.planning/phases/68-yardstick/68-CHECKPOINT-2-RULING.md` - C-7 A, explicitly open companion rows and v2.6 routing.
- `.planning/phases/59-read-only-baseline-scorecard/59-GAPS.md` - original GAP-59-08 resolution record.
- `pinn/verification/artifacts/feasibility_scorecard_v1.json` - frozen metrics and tiers; no re-freeze.
- `pinn/verification/feasibility_scorer.py` - frozen score definitions, not a new classifier.

</canonical_refs>

<code_context>
## Existing code insights

### Reusable assets

- `pinn/verification/evidence_io.py` provides existing committed-evidence,
  provenance and frozen-scorecard checks. Apply its established patterns.
- `pinn/verification/diagnostic_phase67.py` and
  `pinn/verification/diagnostic_phase67_execution.py` expose the existing
  read-only phase audit and review checks. They establish mechanical
  evidence integrity, not scientific causality.
- `pinn/verification/diagnostic_phase66.py` provides the positive-control
  record and review interpretation. Its historical reuse conditions matter.
- `pinn/verification/yardstick_audit.py` replays the known-answer evidence.
- `pinn/verification/learnability_run.py`,
  `pinn/verification/learnability_protocol.py`,
  `pinn/verification/learnability_losses.py`,
  `pinn/verification/diagnostic_fit.py` and
  `pinn/verification/diagnostic_variants.py` locate the recipe/model/loss
  implementations to compare at the revisions identified by the records.
- `.planning/phases/64-feasibility-verdict/evidence/verify_phase64_verdict.py`
  and `tests/phase64/test_verifier_phase64.py` show the earlier closing
  evidence/traceability checks. Their archived v2.4 inputs must not be
  mistaken for the active milestone's final requirement inventory.

### Established patterns

Use committed predictions before run evidence, exact run identities and
digests, separate mechanical acceptance from scientific interpretation,
and verbatim owner rulings bound to a presented result. The recent phase
findings and ruling files are closer reporting examples than the June
codebase maps. Prefer a small phase-specific synthesis over new shared
infrastructure. Keep the main page concise and supporting evidence linked.

### Integration points

Phase 69 consumes the existing Phase 65 through 68 records and v2.4
comparison sources. Its outputs inform the owner checkpoint, final
requirement status review and subsequent v2.6 planning. No change to
production training, evaluation or the frozen experiment readers is
required merely to prepare the specification and context.

</code_context>

<specifics>
## Specific ideas from the discussion

The owner asked whether more diagnostics would teach anything new. The
accepted recommendation separates readiness to synthesize from confidence
in a redesign: close the completed yardstick work, use the existing
failed/successful recipe comparison first, and propose narrowly focused
work only when it could change the next decision. It does not claim that
all future diagnostics would be redundant or that a redesign is already
scientifically compelled.

</specifics>

<deferred>
## Deferred ideas

- New diagnostic launches, if recommended, need a separately authorized
  prospective design, reading rule and measured budget. No broad campaign
  is added by this discussion.
- Architecture changes, physics-pipeline repairs, the autograd production
  amendments and the evaluation-text rewrite belong to authorized v2.6 work.
- trainex-r5 assembly/research follows an explicit commission and question.
- Deferred charter choices and the preserved evaluation remain owner matters.

### Reviewed todos, outside scope

- `.planning/todos/pending/d-06-static-epsilon-sensitivity-check.md` is an
  admission/stage-label sensitivity study. It is not the approved existing
  recipe reconciliation and would add empirical work.
- `.planning/todos/pending/trainex-r1-research-handoff.md` concerns an older
  external package. Keyword overlap does not make it the Phase 69
  trainex-r5 commissioning decision. Its status is not adjudicated here.

</deferred>

---

*Phase: 69-findings-redesign-decision*
*Context gathered: 2026-11-08*
