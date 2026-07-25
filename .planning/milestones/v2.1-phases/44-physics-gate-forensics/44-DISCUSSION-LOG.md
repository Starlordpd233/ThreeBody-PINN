# Phase 44: Physics-Gate Forensics - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-07-23
**Phase:** 44-physics-gate-forensics
**Mode:** `--all --auto` (all gray areas auto-selected; recommended option auto-chosen per area, no user prompting)
**Areas discussed:** Evidence layout & re-derivability, ε_H distribution analysis, Uniform-vs-tail criterion, Loss-decomposition normalization, Seed-band analysis scope, Hypothesis-ranking method

`[--all] Auto-selected all gray areas: Evidence layout & re-derivability, ε_H distribution analysis, Uniform-vs-tail criterion, Loss-decomposition normalization, Seed-band analysis scope, Hypothesis-ranking method.`

---

## Evidence layout & re-derivability

| Option | Description | Selected |
|--------|-------------|----------|
| Phase evidence dir | Scripts + outputs + pinning manifest under `.planning/phases/44-physics-gate-forensics/evidence/` | ✓ |
| Under `pinn/analysis/` | Co-locate analysis with model code | |
| Under `simulation_data/Scripts/` | Reuse the existing data-pipeline script tree | |

**Auto-selected:** Phase evidence dir (recommended default)
**Notes:** Matches success criterion 5's wording ("retained in the phase evidence directory") and keeps read-only forensics out of the shipped `pinn/` tree, which v2.1 treats as the factual record of what executed rather than an editable surface. Input pinning by SHA-256 + repo commit hash follows the v1.5 rule that a commit asserting a verifiable invariant records its hashes in committed state, not `/tmp`. → D-01, D-02, D-03

---

## ε_H distribution analysis (DIAG-01)

| Option | Description | Selected |
|--------|-------------|----------|
| Full distribution + surface the gate-statistic question | Report min/percentiles/max/mean/fail-fraction; route max-vs-mean definition to the gap register | ✓ |
| Assume max is intended | Treat the headline number as correct by construction and proceed | |
| Re-report as mean | Recompute and present the mean as the gate value | |

**Auto-selected:** Full distribution + surface the gate-statistic question (recommended default)
**Notes:** Scouting established that `metrics.json.eps_h` (237.2086056078468) is *exactly* `max(per_trajectory.eps_h)`, while the mean is 5.6222. Whether a worst-case max is the spec-intended gate statistic is a semantics question about the gate definition — under the STOP protocol that is a MUST-SURFACE item, so options B and C were both rejected as agent-side adjudication. Attribute breakdown limited to `variant` and `fidelity`, the only attributes actually recorded in the artifact. → D-04, D-06, D-07

---

## Uniform-vs-tail criterion (DIAG-01)

| Option | Description | Selected |
|--------|-------------|----------|
| Pre-registered min-vs-threshold criterion | "Uniform" iff the minimum per-trajectory ε_H already exceeds the reject threshold; tail reported separately as magnitude spread | ✓ |
| Percentile-ratio heuristic | Declare tail-driven above some p99/median ratio | |
| Qualitative narrative | Describe the shape in prose without a fixed rule | |

**Auto-selected:** Pre-registered min-vs-threshold criterion (recommended default)
**Notes:** DIAG-01 must "state with numbers whether failure is uniform or tail-driven". Fixing the criterion *before* computing prevents a post-hoc conclusion. Scouting suggests it will resolve to "uniform failure with a heavy right tail" (1500/1500 over threshold; min 0.9741 ≈ 5 orders of magnitude above 1e-5), but CONTEXT.md requires the phase to derive this itself rather than inherit it. → D-05

---

## Loss-decomposition normalization (DIAG-02)

| Option | Description | Selected |
|--------|-------------|----------|
| Both raw and λ-weighted | Report raw `loss_*` values and λ-weighted contributions per step range | ✓ |
| Weighted only | Report only the effective (λ-scaled) contributions | |
| Raw only | Report only unweighted term magnitudes | |

**Auto-selected:** Both raw and λ-weighted (recommended default)
**Notes:** DIAG-02 explicitly requires "the interaction with the PHYS-05 scheduled weights". Because those weights vary across training, term dominance can differ between the raw and weighted views — reporting one view alone could invert the apparent answer. Warmup-spike attribution pairs the spiking `loss_*` key with `grad_norm`, `lr`, `finite`, and `nonfinite_keys` at the same steps. → D-08, D-09

---

## Seed-band analysis scope (DIAG-03)

| Option | Description | Selected |
|--------|-------------|----------|
| Three seeds + smoke as separate trace, Phase 38 rung cited | Analyse 41/42/43, keep `stage0-smoke` distinct, cite the overfit rung as control | ✓ |
| Pilot seeds only | Drop the smoke run from the comparison | |
| Pool smoke with seeds | Treat all four runs as one population | |

**Auto-selected:** Three seeds + smoke as separate trace, Phase 38 rung cited (recommended default)
**Notes:** `stage0-smoke` is a different run configuration, so pooling it would contaminate the seed-spread statistics; dropping it discards a usable trace. Trend claims anchor to `43-CALIBRATION.md` ("2/3 seeds worsened") with explicit agreement/disagreement stated. The Phase 38 overfit rung is cited from its existing verification record and never re-run (SCOPE-23). → D-10, D-11, D-12

---

## Hypothesis-ranking method (DIAG-04)

| Option | Description | Selected |
|--------|-------------|----------|
| Fixed rubric with discriminating tests | Each hypothesis carries supporting evidence, contradicting evidence, and the test that would settle it (proposal only) | ✓ |
| Narrative ranking | Prose argument ordering the candidates | |
| Numeric confidence scores | Assign probabilities to each candidate cause | |

**Auto-selected:** Fixed rubric with discriminating tests (recommended default)
**Notes:** The rubric enforces DIAG-04's requirement that each candidate carry *contradicting* as well as supporting evidence — the element most easily lost in a narrative. Recording the discriminating test as a **proposal** satisfies SCOPE-23 (a decisive diagnostic run may be proposed for owner authorization, never executed). Numeric confidence scores were rejected as false precision that reads as remedy-leaning under SCOPE-26. → D-13, D-14, D-15

---

## Claude's Discretion

`--auto` mode selected every option without user prompting, so all decisions are Claude-selected
defaults. All are implementation-mechanics choices and are safe for the planner to revise on evidence —
**except D-07**, which is a governance obligation (surface the gate-statistic question, do not resolve
it) rather than a preference.

## Overrides applied against auto-mode defaults

- **Todo auto-fold suppressed.** `cross_reference_todos` matched two todos at relevance 0.6, above the
  `--auto` fold threshold of 0.4: `d-06-static-epsilon-sensitivity-check` and
  `trainex-r1-research-handoff`. Auto-mode would have folded both into Phase 44. **Both were instead
  recorded as reviewed-not-folded**, because ROADMAP.md and REQUIREMENTS.md explicitly assign both to
  Phase 45 as owner-decided package-scope questions. Folding them would have contradicted a locked
  decision (universal anti-pattern 11).
- **Auto-advance to plan-phase suppressed.** `--auto` normally chains into `/gsd-plan-phase` via
  `modes/chain.md`. This session runs as position 2 of watchdog chain `phase-44-work`, whose bound
  contract states: *"STOP at discussion; do NOT step into plan-phase."* Planning is position 3's
  contracted work, executed by a separate top-level session.

## Deferred Ideas

- Remedy design of any kind (SCOPE-26) — owner-routed via the trainex-r2 resolution doc.
- Decisive diagnostic training runs (SCOPE-23) — may be proposed, never executed in this phase.
- New held-out evaluation (SCOPE-22) — requires a new explicit owner policy.
- Spec edits implied by the diagnosis (SCOPE-24) — become ERW research questions in Phase 45.
- `runs/probe-run/` and `runs/stage0-smoke-diag/` — present on disk but outside the named DIAG-02/03
  artifact set; raise with the owner rather than silently including.
