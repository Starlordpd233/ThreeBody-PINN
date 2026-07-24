# Phase 44 Gap Register — Physics-Gate Forensics

Phase-local STOP-protocol gap register for Phase 44 (milestone v2.1). Each entry
is a source-silent physics-adjudication or gate-semantics decision that this
phase **surfaced** rather than decided, per the CLAUDE.md STOP protocol and the
ROADMAP "STOP-protocol spirit" clause. The milestone-wide index is
`.planning/milestones/v2.1-GAPS.md` (created on the first gap, standing trigger).

This register is written by the Phase 44 orchestrator (parent session), not by a
subagent — per governance, the parent owns gap-register writes.

## GAP-44-01 — Which statistic is the held-out physics-gate `eps_H` headline (worst-case max vs aggregate)?

- **Decision point:** Which statistic constitutes the held-out physics-gate
  `eps_H` headline number — the per-trajectory **maximum** (worst-case =
  237.2086056078468, what `metrics.json` reports as top-level `eps_h`), an
  aggregate over the 1,500 trajectories (mean = 5.622187097745829, median =
  2.232675867436938), or a fraction-failing measure (here 1500/1500 = 100%)?
  The locked spec defines per-trajectory `eps_H` and the per-trajectory reject
  rule but does not explicitly define the aggregate held-out headline statistic;
  the evaluator rendered `max`. Whether worst-case-max is the spec-intended gate
  statistic is a source-silent semantics question (D-07).

- **Where in artifact:** `runs/stage0-pilot-seed42/evaluation/metrics.json`
  (top-level `eps_h = 237.2086056078468`, exactly `max(per_trajectory.eps_h)`);
  `.planning/phases/44-physics-gate-forensics/evidence/diag01/eps_h_distribution.json`
  (`d07_observation`, `overall`, `verdict`);
  `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:567-579`
  (gate definition);
  `.planning/milestones/v2.0-phases/43-verification-stage-0-pilot-acceptance/43-VERDICT.md:27-49`;
  `44-CONTEXT.md` decision D-07.

- **Task context:** DIAG-01 (plan 44-01) computed the per-trajectory `eps_h`
  distribution from the preserved `metrics.json` and confirmed
  `max(per_trajectory.eps_h) == top-level eps_h` by EXACT float equality
  (237.2086056078468 == 237.2086056078468), with mean 5.6222 and median 2.2327.
  The gate-statistic question surfaced during distribution characterization;
  per D-07 it is MUST-SURFACE — the phase checks the locked spec and the Phase 43
  evaluator record, and records a gap if they are silent or ambiguous, without
  deciding the intended statistic and without quietly re-reporting the mean as
  "the" gate number.

- **Classification:** semantic — gate-statistic semantics; the source defines the
  per-trajectory quantity and rule precisely but is silent on the aggregate
  held-out headline statistic.

- **Source silence:**
  - `ctl_instruction.md:567-572` defines per-trajectory
    `eps_H = max_t |(H(t) - H(0)) / H(0)|` and the per-trajectory reject rule
    `eps_H > 1e-5` (equivalently `SCS > -5`). It does NOT define the aggregate
    held-out statistic over the 1,500 test trajectories (max vs mean vs median
    vs fraction-failing).
  - `ctl_instruction.md:578-579` distinguishes the validation-gate `eps_H` from
    the training-loss `eps_H = 1e-4*S_H`, but still speaks per-trajectory; it
    does not specify the aggregate.
  - `43-VERDICT.md:27-49` reports `eps_H = 237.2086…` and verdict FAIL, grounded
    in the receipt; it does not adjudicate whether the headline must be the
    worst-case max or an aggregate.
  - `43-VERIFICATION.md` ACC-03 cites the preserved receipt
    `eps_h = 237.2086…` (the max) as the gate number; it does not define the
    aggregate-statistic semantics.
  - `metrics.json` reports top-level `eps_h = max(per_trajectory.eps_h)`; this
    is the evaluator's rendering, not a spec statement of intent. (`pinn/`
    live code is NOT a grounding source for spec intent per the standing
    2026-05-19 directive; it is the factual record of what executed.)

- **Mathematical / engineering grounding:** Per-trajectory `eps_H` is the max
  over time of the relative Hamiltonian drift — a worst-case-over-time measure
  for one trajectory. Aggregating 1,500 per-trajectory values into a single gate
  number can be done several defensible ways: (a) worst-case over trajectories
  (`max = 237.21`) — the strongest "any failure fails the gate" reading, implied
  by applying the per-trajectory reject rule to the whole held-out set; (b)
  central-tendency magnitude (mean 5.62 / median 2.23); (c) fraction exceeding
  the threshold (100%). Because DIAG-01 shows the minimum per-trajectory `eps_h`
  (0.9741251227996501) already exceeds `1e-5` by roughly five orders of
  magnitude, **all 1,500 trajectories individually fail the per-trajectory
  reject rule**, so the population verdict is FAIL under any aggregate — the
  choice does NOT change pass/fail. It changes only the reported HEADLINE
  magnitude and the downstream framing (notably for the trainex-r2 researchers,
  who will see "`eps_H = 237.21`"). Reporting the mean (5.62) as "the" gate
  number would materially understate the worst-case violation and is exactly
  what D-07 forbids doing silently.

- **Agent was tempted to:** Treat the evaluator's `max` rendering as
  authoritative (it is what the locked receipt reports and what 43-VERDICT
  cites) and state in `44-DIAGNOSIS.md` that "the gate statistic is the
  worst-case max." That is an *inference* from the per-trajectory reject rule
  plus the evaluator's observed behavior — not an explicit spec statement — and
  D-07 requires surfacing the question, not inferring the answer.

- **What the user needs to decide:**
  - **A. Worst-case max is the spec-intended gate statistic** (confirm the
    evaluator's choice): the held-out gate fails if ANY trajectory's `eps_H`
    exceeds `1e-5`; the headline is the max. `44-DIAGNOSIS.md` then reports `max`
    as THE gate number with that grounding.
  - **B. An aggregate is intended** (mean / median / fraction): specify which;
    `44-DIAGNOSIS.md` reports that aggregate as the headline (still FAIL).
  - **C. Defer to the trainex-r2 resolution doc / Phase 45** (recommended
    default-until-resolved): leave the statistic semantics as an open research
    question; `44-DIAGNOSIS.md` reports BOTH max and mean as facts without
    designating either as THE gate number (the behavior D-07/D-15 already
    require).

- **Confidence of impact:** MEDIUM — the FAIL verdict is unaffected (100% of
  trajectories fail the per-trajectory rule individually), but the choice
  affects the reported headline magnitude and the trainex-r2 research framing;
  silently reporting the mean would mislead downstream research.

- **Status:** OPEN

- **Resolution note:** *(empty — awaiting owner instruction; until resolved,
  `44-DIAGNOSIS.md` follows option C and quotes both max and mean as facts
  without designating either as the gate statistic, per D-15.)*
