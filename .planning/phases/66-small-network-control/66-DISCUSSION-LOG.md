# Phase 66: Small-Network Control - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-10-31
**Phase:** 66-small-network-control
**Areas discussed:** Mac compute commitment (owner-authority question only)

Under the standing delegation (`.planning/PROJECT.md`, Context, 2026-10-28),
technical and scientific areas were resolved by the agent and recorded in
`66-CONTEXT.md` D-02..D-12. They were not put to the owner as a questionnaire.

---

## Mac compute commitment

| Option | Description | Selected |
|--------|-------------|----------|
| Under 1 hour per run (Recommended) | Each run capped just under an hour, about 3 hours in total. No pause/resume tooling repair. A run still improving at its cap goes to the owner at the review rather than being extended automatically. | |
| About 15 minutes per run | About 1 hour in total. Cheaper, but risks an ambiguous "under-trained" reading. | |
| Several hours per run | Like v2.4's 2.5-3 hours per run, roughly 8-10 hours in total. Needs pause/resume and power-guard tooling to be proven first. | |

**User's choice (free text, verbatim):** "as long as you need. this mac will be
plugged into power for the weekend only. not weekdays. i have classes weekdays"

**Notes:** The agent recorded this as no fixed time cap, with an AC-power
window. Training runs only while the Mac is plugged in (weekends), and each
launch confirms AC power. Runs under one hour are preferred. A longer or
extended run may be pre-registered if timing evidence calls for it, after
SCOPE-48's pause/resume and power-guard compatibility is proven (D-08).

---

## Claude's Discretion

These were decided by the agent under the standing delegation (`66-CONTEXT.md`):

- The positive-control design: D-02, with "from time alone" read in D-03.
- The production layer types at 2 or fewer hidden layers (D-04).
- The bandwidth-matched `first_omega_0` (D-05). The production first layer
  starts about 15 times too slow for orbit 1632's inner laps, and a shallow
  network at the locked frequency is EXP-02's rung, so it was rejected here.
- Locked learning rate, window and seed (D-06).
- Both repeats pre-registered and always run (D-07).
- The numeric reading band (D-09).
- Scoring and isolation (D-10, D-11).

Alternatives considered and not taken:

- A time-only (1-input) network. It changes the input design, which is EXP-04's
  factor.
- A shallow network at the locked frequency. That is EXP-02's 2-layer rung, and
  it is confounded by bandwidth.
- Running the repeats only after a Tier-1 result. That is a post-result choice.

## Deferred Ideas

- The shallow network at the locked frequency and the remaining ladders: Phase 67.
- Energy-metric adjudication: Phase 68.
- Repairing the pause/resume and power-guard tooling: only if a run at or above
  one hour is registered.
- Two matched todos (D-06 static epsilon check, trainex-r1 handoff) were
  reviewed and not folded, with the same disposition as in Phase 65.
