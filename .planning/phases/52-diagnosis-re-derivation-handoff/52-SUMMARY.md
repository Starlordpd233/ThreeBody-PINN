---
phase: 52-diagnosis-re-derivation-handoff
plan: adapted-closeout
subsystem: milestone-handoff
tags: [pinn, diagnosis, ver-19, ver-20, milestone-close, v2.3-routing]

requires:
  - phase: 50-valid-stage-0-re-run
    provides: Owner decision (stop-incomplete) and the 2026-08-17 residual-frame conformance audit
provides:
  - "Re-derived Phase 44 diagnosis discharging GAP-44-02"
  - "VER-19 requirement traceability closeout for v2.2 (24/24, adapted)"
  - "VER-20 spec-amendment routing list (5 items) handed off to v2.3"
affects: [v2.3-milestone-proposal]

key-decisions:
  - "Phase 51 (RUN-03/EVAL-01) is not attempted, not failed — the sole authorized held-out evaluation is preserved for v2.3, per owner instruction 2026-08-17"
  - "DIAG-05 is discharged via the 'design failure' branch of Phase 51's own anticipated fork, without Phase 51 having executed, because the evidence (architecture-only characterization) is independent of any training run's outcome"
  - "VER-20 routing list grows from 4 to 5 items; item (e) is the substantive one"

completed: 2026-08-17
status: closed-incomplete-adapted
---

# Phase 52: Diagnosis Re-Derivation & Handoff (adapted)

**This phase was never planned through the standard discuss/plan/execute
workflow** — Phase 50 halting incomplete (owner decision, `50-08-SUMMARY.md`,
2026-08-17) meant Phase 51 never started and Phase 52's roadmap dependency
("Depends on: Phase 51 (the conformant run and its evaluation)") could not be
satisfied literally. Per owner instruction the same day, Phase 52's three
requirements are discharged now in adapted form, without Phase 51 having run,
because DIAG-05's own success criterion anticipates a design-failure branch
that does not require a completed held-out evaluation, and VER-19/VER-20 are
bookkeeping that do not depend on one either.

## Phase 51 disposition (recorded here, since Phase 51 has no directory)

**RUN-03 and EVAL-01: not attempted.** Not failed, not waived as tech debt —
deliberately not spent. Phase 51's own success criteria require "a run that
passed every precondition" before the evaluator is invoked; Phase 50 closed
with RUN-01/RUN-02 unsatisfied, so no such run exists. Spending the single
SCOPE-28 held-out evaluation on a run already known (from the retained
502-step log) to have received physics supervision at a single collocation
point would repeat the v2.0 mistake the "exactly one look" design existed to
prevent. **The evaluation is preserved, unspent, for v2.3**, to be used once a
genuinely conformant *and completed* run exists under a recalibrated recipe.

## DIAG-05 — Complete

See `52-DIAG-05-REDERIVATION.md`. Summary: the v2.0 physics-gate failure is
explained by a design-level mismatch between the locked SIREN initialization
scale and the locked causal-weight calibration, established independent of
any particular run's outcome (architecture-only characterization, 6
seed/IC cases, zero training steps). This is stronger evidence than a failed
held-out grade would have been, and it discharges GAP-44-02's re-derivation
obligation.

## VER-19 — Complete

Requirement traceability re-verified at v2.2 close, adapted for the halted
outcome:

| Requirement | Phase | Status at close |
|---|---|---|
| CONF-01, CONF-08, INST-01 | 46 | Complete |
| CONF-09, CONF-02, CONF-03 | 47 | Complete |
| CONF-04..07, INST-02, TEST-01, TEST-02 | 48 | Complete |
| GATE-01..03, INST-03 | 49 | Complete |
| RUN-01, RUN-02 | 50 | **Closed incomplete** (owner `stop-incomplete`, 2026-08-17) |
| RUN-03, EVAL-01 | 51 | **Not attempted** (evaluation preserved for v2.3) |
| DIAG-05, VER-19, VER-20 | 52 | Complete (this document) |

24/24 requirements map to exactly one phase; no orphans, no duplicates. Three
requirements (RUN-01, RUN-02) close unsatisfied and two (RUN-03, EVAL-01)
close not-attempted — this is the milestone's actual outcome, not a gap in
coverage. Per the CONF-09 lesson recorded at roadmap-amendment time (
`REQUIREMENTS.md` line 141): "a passing coverage count is evidence of no
*orphans*, never of no *gaps*." VER-19 here certifies mapping completeness,
not requirement satisfaction — satisfaction is recorded per-requirement above
and in the v2.2 archive.

## VER-20 — Complete

See `52-VER-20-ROUTING-HANDOFF.md`. Five items handed off, none resolved (no
spec file edited): (a) misleading "default" wording on §4.1's `λ_phys^max`
line, (b) locked-vs-default table convention, (c) explicit `L_data` reduction,
(d) aggregate gate statistic, (e) causal-weight/SIREN-scale calibration (new,
the substantive item, routed to v2.3).

## Files Created

- `.planning/phases/52-diagnosis-re-derivation-handoff/52-DIAG-05-REDERIVATION.md`
- `.planning/phases/52-diagnosis-re-derivation-handoff/52-VER-20-ROUTING-HANDOFF.md`
- `.planning/phases/52-diagnosis-re-derivation-handoff/52-SUMMARY.md` (this file)

No recipe, config, framework-spec, ledger, or experiment artifact was edited.

---
*Phase: 52-diagnosis-re-derivation-handoff*
*Completed: 2026-08-17 (adapted — Phase 51 did not execute)*
