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

- **Status:** RESOLVED-WITH-INSTRUCTION

- **Resolution note:** Owner instruction 2026-07-23 (interactive session,
  AskUserQuestion): **Option A — the worst-case max is the spec-intended gate
  statistic.** The held-out physics gate fails if ANY trajectory's `eps_H`
  exceeds `1e-5`, and the headline is
  `max(per_trajectory.eps_h) = 237.2086056078468` — confirming the evaluator's
  rendering, consistent with the per-trajectory reject rule applied set-wide,
  43-VERDICT's citation, and the preserved aggregate `SCS = log10(max)`.
  Applied: `44-DIAGNOSIS.md` (GAP-44-01 section, §2 gate table, §7) updated to
  designate max as THE gate number with this grounding; mean (5.6222) and
  median (2.2327) remain quoted as distribution facts, not gate numbers;
  `v2.1-GAPS.md` row updated. Codifying the aggregate-statistic wording into
  `ctl_instruction.md` is NOT done here (SCOPE-24 — Phase 44 edits no spec);
  it remains available to a later spec-editing milestone if the owner wants
  the gate definition to state it explicitly.

## GAP-44-02 — Is an erratum sufficient for the DIAG-04 rankings, or must Phase 44 be reopened?

- **Decision point:** The trainex-r2 research result, and the independent
  verification that followed it, established that the executed Stage-0 pilot
  diverged from the locked framework specs in at least five verified respects.
  `44-DIAGNOSIS.md`'s DIAG-04 candidate-cause rankings were assembled on the
  assumption that the run implemented the spec. Does the qualification land as a
  standalone erratum (`44-ERRATUM.md`, written 2026-07-24, diagnosis left
  byte-identical), or must Phase 44 be reopened and its diagnosis re-derived
  against the corrected understanding?

- **Where in artifact:**
  `.planning/phases/44-physics-gate-forensics/44-DIAGNOSIS.md` §7 (DIAG-04
  ranking table) and its supporting §§3-6;
  `.planning/phases/44-physics-gate-forensics/44-ERRATUM.md` (the proposed
  qualification);
  `docs/work/reviews/cross_cutting/stage0-conformance-audit/2026-07-24-stage0-training-path-conformance-audit.md`
  (findings C-01…C-08);
  `docs/work/reviews/milestone_v2.1/45-trainex-r2-erw-package-assembly/2026-07-24-trainex-r2-report-factw-verification.md`
  (per-claim verification).

- **Task context:** Post-delivery verification of the returned trainex-r2 report
  (Route B / open-book, per the amended ERW runbook Rule 19). Six repository-derived
  claims were verified; all six confirmed, two stronger than the report asserted.
  A bounded conformance audit of the executed Stage-0 path then established the
  full inventory. The question of what happens to Phase 44's already-delivered
  interpretive layer surfaced immediately and is not answerable from any source.

- **Classification:** cross-phase reframing — the answer determines whether a
  closed phase reopens, and it changes what the next milestone inherits as its
  starting diagnosis.

- **Source silence:**
  - `.planning/ROADMAP.md:57-85` (Phase 44 success criteria) states what the
    diagnosis must contain and that it must abstain from remedy selection. It is
    silent on what happens if the diagnosis's premise is later falsified.
  - `.planning/REQUIREMENTS.md` DIAG-01..04 define the deliverables, not a
    revision protocol for them.
  - `docs/README.md` defines a supersession protocol for `docs/` review reports
    (`status: superseded`, never delete-and-recreate). `44-DIAGNOSIS.md` is a
    `.planning/` phase artifact, not a `docs/` file, and no equivalent protocol
    is stated for phase artifacts.
  - CLAUDE.md's STOP protocol governs gaps found *during* a phase; it does not
    address retroactive qualification of a completed phase's output.
  - `45-AUDIT.md` Checks 4-5 assert the diagnosis is byte-identical to the
    package snapshot and that no source changed since `source_baseline` — a
    constraint on any in-place edit, but not an instruction about which route to
    take.

- **Mathematical / engineering grounding:** The distinction at stake is between
  measurement and inference. Phase 44's measurements — the per-trajectory ε_H
  distribution, the five-term loss decomposition, the three-seed band — are
  derived from retained artifacts and are unaffected by the conformance findings;
  they describe what the run did, and the run did what it did. What the findings
  invalidate is the *inference step* that mapped those measurements onto ranked
  causes, because that mapping assumed the observed behavior was produced by the
  specified recipe. Concretely: the top-ranked cause (population-scale
  generalization shortfall) was supported by a uniform 1500/1500 failure plus a
  single-trajectory overfit control. A uniform failure discriminates between
  "population-scale capacity limit" and "recipe-level mechanism applying
  identically to every trajectory" only if the recipe is known correct — and
  C-01/C-02 establish a mechanism of exactly the second kind (physics supervision
  reaching 1 of 16 collocation points on every step of every run). The evidence
  therefore under-determines the ranking it was used to justify. Reopening would
  re-derive the inference against the corrected premise; an erratum records that
  the inference is under-determined and defers re-derivation to the next
  milestone, where the divergences will be fixed and the pilot re-run — which is
  the only thing that can actually discriminate the hypotheses. The engineering
  trade-off is whether the project's record should carry a corrected ranking now
  (costly, and still not decidable without a valid run) or an honest statement
  that the ranking is under-determined pending one.

- **Agent was tempted to:** write the erratum and treat the matter as closed,
  on the reasoning that Phase 44's success criteria were met, its measurements
  stand, and re-ranking hypotheses without a valid training run would substitute
  one under-determined inference for another. That reasoning is the case for
  Option A below, but choosing between A/B/C decides whether a closed phase
  reopens and what the next milestone inherits — a cross-phase reframing the
  agent does not decide.

- **What the user needs to decide:**
  - **(A)** Erratum is sufficient. `44-ERRATUM.md` stands alongside the
    byte-identical diagnosis; Phase 44 stays closed; re-derivation happens in the
    next milestone after the divergences are fixed and the pilot re-run.
  - **(B)** Reopen Phase 44. Re-derive DIAG-04 against the conformance findings,
    re-verify, and re-close the phase. Note this breaks the delivered package's
    byte-identity pin unless the revision is written to a new file.
  - **(C)** Erratum now, mandatory re-derivation later. Phase 44 stays closed but
    the next milestone carries an explicit requirement to re-derive the diagnosis
    from a conformant run, rather than leaving it to judgement.

- **Confidence of impact:** MEDIUM — the measurements are unaffected either way,
  so no number changes; the impact is on what the next milestone treats as its
  inherited diagnosis and on whether the project record shows a corrected or an
  explicitly-under-determined ranking.

- **Status:** RESOLVED-WITH-INSTRUCTION

- **Resolution note:** Owner instruction 2026-07-24 (interactive session,
  AskUserQuestion): **Option C — erratum now, re-derivation mandatory later.**
  1. **Phase 44 stays closed.** `44-ERRATUM.md` stands alongside the
     byte-identical `44-DIAGNOSIS.md`; the diagnosis is not edited, preserving the
     delivered trainex-r2 package's snapshot pin (`45-AUDIT.md` Checks 4-5).
  2. **The DIAG-04 rankings are recorded as under-determined, not corrected.**
     Re-ranking hypotheses without a conformant training run would substitute one
     under-determined inference for another; the only thing that discriminates the
     candidate causes is a valid Stage-0 run, which does not yet exist.
  3. **The next milestone carries an explicit requirement** to re-derive the
     diagnosis from a conformant run — a mapped requirement with an acceptance
     check, not a judgement call or a best-effort intention. This is the operative
     difference from a plain erratum, and it is the condition on which Phase 44 is
     permitted to stay closed.
  4. Phase 44's measurements, its GAP-44-01 headline
     (`max = 237.2086056078468`), the uniform 1500/1500 failure, and its remedy
     abstinence all stand unchanged.

  *All five v2.1 gaps are now terminal (four RESOLVED-WITH-INSTRUCTION, one
  DEFERRED). The milestone-close blocker is cleared.*
