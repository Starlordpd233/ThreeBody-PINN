---
phase: 34-training-loop-batch-construction-contracts
plan: 06
subsystem: specwork
tags: [LOOP-01, batch-construction, GAP-34-01, edge-case-policy, closure-gate, ctl_instruction, specwork]

requires:
  - phase: 34-03
    provides: "ctl_instruction.md Mini-Batch Construction canonical LOOP-01 contract with the owner-pending GAP-34-01 callout"
  - phase: 34-05
    provides: "34-VERIFICATION.md passed-with-closure-gate verdict gating Phase-34 completion on GAP-34-01"

provides:
  - "Owner-ratified Option A batch edge-case policy transcribed into the ctl_instruction.md LOOP-01 contract (provisional)"
  - "GAP-34-01 referenced as RESOLVED-WITH-INSTRUCTION in the ctl contract (no longer OPEN/owner-pending)"
  - "34-VERIFICATION.md closure gate CLEARED (status passed; gaps_remaining [])"

affects:
  - phase: 35-loss-scaling-causal-mode
  - phase: 36-final-verification
  - milestone-v1-6-closure

tech-stack:
  added: []
  patterns:
    - "Owner-instruction-grounded transcription: a resolved STOP gap (RESOLVED-WITH-INSTRUCTION) is transcribed verbatim-in-intent, with no Option B/C drift"
    - "Closure-gate clearance addendum: prior verification body preserved; frontmatter + a dated §8 addendum record the gate clearance"

key-files:
  created:
    - ".planning/phases/34-training-loop-batch-construction-contracts/34-06-PLAN.md"
    - ".planning/phases/34-training-loop-batch-construction-contracts/34-06-SUMMARY.md"
  modified:
    - "pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md"
    - ".planning/phases/34-training-loop-batch-construction-contracts/34-VERIFICATION.md"

key-decisions:
  - "Transcribed Option A exactly (final-stage replay-only; undersized look-ahead padded with replacement at fixed 240+16; replay without replacement across the epoch); Option B (reservoir / shrink-batch) and C declined"
  - "Tagged the edge policy provisional (B-07 modified), inheriting the LOOP-01 status rather than promoting it to locked/verified"
  - "Cleared the closure gate by updating 34-VERIFICATION.md frontmatter + a §8 addendum; preserved the original 2026-06-25T07:30 verification body; left STATE.md/ROADMAP.md advancement to the user (D-34-18)"

requirements-completed:
  - LOOP-01

duration: 6min
completed: 2026-06-26
status: complete
---

# Phase 34 Plan 06: GAP-34-01 Option A Transcription + Closure-Gate Clearance Summary

**Transcribed the owner-ratified Option A batch edge-case policy into the `ctl_instruction.md` Mini-Batch Construction LOOP-01 contract (provisional) and cleared the Phase-34 closure gate recorded in `34-VERIFICATION.md`, with the LOOP-04 cross-file and locked-convention guards re-verified intact.**

## Performance

- **Duration:** ~6 min
- **Tasks:** 2
- **Files modified:** 2 spec/verification files + 1 plan + 1 summary

## Accomplishments

- Replaced the `ctl_instruction.md` Mini-Batch Construction `> **Batch edge cases — owner-pending (GAP-34-01).**` callout with the ratified **Option A** contract callout, tagged `provisional` (B-07 `modified`):
  - **(1) Final stage** (`has_stage(k+1)` false) → trains on the **replay set only** (`B_lookahead = 0`).
  - **(2) Undersized look-ahead pool** (<16 eligible) → **padded by sampling with replacement** from the available pool, batch size fixed at `B_replay + B_lookahead = 240 + 16`.
  - **(3) Replay** → **sampled without replacement** across the epoch (standard once-per-epoch coverage).
- Referenced GAP-34-01 as `RESOLVED-WITH-INSTRUCTION` (2026-06-25, Option A via UAT) in the contract; the OPEN/owner-pending framing ("the source gives no policy") is gone.
- Left the LOOP-01 core contract (`B_replay = 240`, `B_lookahead = 16`, `has_stage(k+1)`, `n_pts_cap = 32`), the windowed-causal-mode note, and all other LOOP contracts unchanged.
- Re-ran the LOOP-04 (a)-(e) cross-file consistency suite and the locked-convention regression guard after the ctl batch — all PASS.
- Cleared the `34-VERIFICATION.md` §8 closure gate: frontmatter `status: passed-with-closure-gate → passed`, `gaps_remaining: [GAP-34-01] → []`, plus a dated §8 closure-gate-cleared addendum; preserved the original 2026-06-25T07:30 verification body.

## Task Commits

Executed inline during `/gsd-verify-work 34` follow-through (not via the `gsd-executor` atomic-commit path). **Commits are deferred to the user** — this worktree is on the protected `milestone/v1.6` branch, and STATE.md/ROADMAP.md advancement is user-owned (D-34-18). Files are staged in the working tree for the user to commit.

## Files Created/Modified

- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` — Mini-Batch Construction LOOP-01 contract now carries the Option A edge-case policy (provisional) in place of the owner-pending GAP-34-01 callout.
- `.planning/phases/34-training-loop-batch-construction-contracts/34-VERIFICATION.md` — closure gate CLEARED (frontmatter `passed` / `gaps_remaining []`; §8 addendum).
- `.planning/phases/34-training-loop-batch-construction-contracts/34-06-PLAN.md` — this plan.
- `.planning/phases/34-training-loop-batch-construction-contracts/34-06-SUMMARY.md` — this summary.

## Decisions Made

- Transcribed **Option A exactly** as ratified; no Option B/C mechanics (no `reservoir` sampler, no batch-size reduction, no backfill-from-replay) were introduced.
- Kept the edge policy `provisional` (B-07 `modified`), inheriting the LOOP-01 status; it is not promoted to a locked/verified optimum.
- Cleared the closure gate in the phase verification record only; **did not** advance `.planning/STATE.md` or `.planning/ROADMAP.md` (user-owned per D-34-18).

## Deviations from Plan

None substantive — plan executed as written. Execution crossed the 2026-06-25 → 2026-06-26 date boundary: the GAP-34-01 *resolution* is correctly dated 2026-06-25 (owner ratification), while this plan's *execution/closure-gate clearance* is dated 2026-06-26.

## Issues Encountered

None.

## Verification Results

| Check | Result |
|---|---|
| Task 1 — Option A tokens present (`batch edge-case policy`, `Option A`, `replay set only`, `with replacement`, `without replacement`, `provisional`, `GAP-34-01`, `RESOLVED-WITH-INSTRUCTION`) | PASS |
| Task 1 — OPEN/owner-pending framing removed (`the source gives no policy`, `owner-pending (GAP-34-01)` absent) | PASS |
| Task 1 — LOOP-01 core intact (`B_replay = 240`, `B_lookahead = 16`, `has_stage(k+1)`, `n_pts_cap = 32`) | PASS |
| Task 1 — no Option B/C mechanics in the callout (`reservoir` / batch-shrink absent) | PASS |
| Task 2 — LOOP-04 (a) mechanism canonical in pinn §4.4 only (`clip_value = C_stage` in pinn, 0 in ctl) | PASS |
| Task 2 — LOOP-04 (b) `8.5` absent both; `7-10 / 5 / 3` single-home in ctl | PASS |
| Task 2 — LOOP-04 (c) bidirectional `AC-LOOP-04` anchors resolve (ctl 7×, pinn 2×) | PASS |
| Task 2 — LOOP-04 (d)/(e) no duplication; status tags agree | PASS |
| Task 2 — locked-convention guard (`4.6416` canonical ctl; ctl `6.694` 4 ≤ HEAD 4; `6.694` absent pinn) | PASS |
| Task 2 — `34-VERIFICATION.md` closure gate cleared (`status: passed`, `gaps_remaining: []`, addendum) | PASS |
| Task 2 — forbidden-path scope guard (only ctl + 34-VERIFICATION + this summary changed; STATE.md/ROADMAP.md/pinn/ untouched) | PASS |

## Known Stubs

None. The edge policy is a complete, owner-ratified deterministic contract carried at `provisional` status (pending the FUT admitted-set tuning that governs all LOOP-01 provisional defaults); it is not a silent stub.

## Threat Flags

None. Spec-edit-only; no new security-relevant surface. The scope guard confirms only `ctl_instruction.md` and the phase verification record changed; `pinn_architecture.md`, frozen/read-only specs, live `pinn/`, `.planning/STATE.md`, and `.planning/ROADMAP.md` are untouched.

## Next Phase Readiness

- LOOP-01 is now complete end-to-end (core contract + deterministic edge policy); the Phase-34 closure gate is cleared.
- **Remaining for Phase-34 completion:** the user advances Phase 34 → complete in STATE.md / ROADMAP.md (D-34-18) and commits the Phase-34 UAT + GAP-34-01 resolution + this plan/summary.
- Phase 35 (loss-scaling / causal mode) and Phase 36 (final verification) can consume the completed LOOP-01 contract.

## Self-Check: PASSED

- [x] `ctl_instruction.md` carries the Option A edge-case policy (provisional); OPEN framing removed.
- [x] LOOP-01 core + LOOP-04 cross-file invariants intact (re-verified).
- [x] `34-VERIFICATION.md` closure gate cleared (status passed; gaps_remaining []).
- [x] `34-06-SUMMARY.md` created.
- [x] No edits to `.planning/STATE.md`, `.planning/ROADMAP.md`, `pinn_architecture.md`, frozen/read-only specs, or `pinn/`.

---
*Phase: 34-training-loop-batch-construction-contracts*
*Plan: 06*
*Completed: 2026-06-26*
