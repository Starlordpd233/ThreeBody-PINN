# Phase 43: Verification, Stage-0 Pilot & Acceptance - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-07-20
**Phase:** 43-verification-stage-0-pilot-acceptance
**Areas discussed:** Chain/pipeline shape, Pilot+verdict driving, verify ladder, smoke test, evaluate gate, summary enrichment, Stage-0 pilot, verdict/handoff

**Mode:** `--all` with owner delegation of technical/scientific/mathematical decisions
(owner instruction 2026-07-20). SPEC.md locked 6 requirements (ambiguity 0.16); the
multi-round Socratic interview was skipped because the gate was already met and technical
decisions were delegated. High-level "how should this phase work / what pipeline" choices
were surfaced to the owner via AskUserQuestion; all implementation gray areas were decided
by the agent and recorded in CONTEXT.md (CTX-70..83).

---

## Chain / pipeline shape (owner-answered)

| Option | Description | Selected |
|--------|-------------|----------|
| Minimal, grow by append | Launch A→B (spec+discuss / plan); append execute/verify positions as planning reveals them | ✓ |
| Fixed 4-stage pipeline | Launch A→B→C→D up front | |
| No chain yet | Spec+discuss only, decide the chain later | |

**Owner's choice:** Minimal, grow by append.
**Notes:** Watchdog chain `phase-43-work` launched with position A = spec+discuss (this
session), position B = plan-phase. Downstream positions appended after planning.

## Pilot + verdict driving (owner-answered)

| Option | Description | Selected |
|--------|-------------|----------|
| Agent runs, pauses for you | Agent builds tooling + runs smoke/pilot autonomously, pausing for owner sign-off at each ratification point + the final verdict | ✓ |
| You drive pilot + verdict | Agent builds + smoke-tests; owner launches pilot runs and renders the verdict | |
| Settle during discuss | Defer | |

**Owner's choice:** Agent runs, pauses for you.
**Notes:** Encoded as the CTX-82 owner-ratification pause protocol — four pause points
(B-5 before run #1, D4-a ceiling post-smoke, R-1/R-2 post-pilot, ACC-06 verdict).

## verify pre-flight ladder (ACC-01) — agent-decided

| Option | Description | Selected |
|--------|-------------|----------|
| New `python -m pinn.verify` orchestrator wrapping existing probes | Device-sanity rung + the 4 existing probe mains as library calls; gate in `pinn.train` preflight | ✓ |
| Fold the ladder into `pinn.train` | Run probes inline at launch; no separate command | |

**Notes:** CTX-70/71. Mirrors the `python -m pinn.train` convention; > 30-min gate enforced
in the train launch preflight against the smoke forecast + a verify-green marker.

## smoke test (ACC-02) — agent-decided

| Option | Description | Selected |
|--------|-------------|----------|
| Config preset over the ordinary `pinn.train` path | ≈32 traj / ~300 steps / checkpoint_every=100; exercises the real mechanical surface + resume; forecast reuses `s_per_step` EMA | ✓ |
| Dedicated standalone smoke harness | Bespoke loop separate from the real trainer | |

**Notes:** CTX-72/73. Reuses the real signals/status/summary/resume path; honest partial
s/step (never a fabricated forecast) on early divergence.

## evaluate gate (ACC-03) — agent-decided

| Option | Description | Selected |
|--------|-------------|----------|
| New `python -m pinn.evaluate`, gate from `ctl_instruction.md` | Authoritative direction (REJECT if ε_H > 1e-5; PASS if SCS > -5); reuse invariants machinery | ✓ |
| Copy the design-doc §6.3 render | Rejected — its ε_H example is backwards | |

**Notes:** CTX-74/75/76/77. Precise ε_H/SCS formulas flagged as a research item (not
invented); plots matplotlib-optional; boundary unit test locks the direction.

## summary.md enrichment (ACC-04) — agent-decided

| Option | Description | Selected |
|--------|-------------|----------|
| Extend `pinn/training/summary.py` in place | Preserve stub-then-finalize + render-don't-recompute + must-NOT #1; add val summary / test preview / comparison hint / honesty rules | ✓ |
| New separate summary module | Rejected — would duplicate the OPS-05 writer | |

**Notes:** CTX-78.

## Stage-0 pilot + calibration (ACC-05) — agent-decided

| Option | Description | Selected |
|--------|-------------|----------|
| 2–3 seeded runs on the real admitted Stage-0 data | Copy the gitignored payload into the worktree; record seed-band + derived R-1/R-2 + D4-a candidates for owner ratification | ✓ |
| Synthetic-only pilot | Rejected — variance calibration needs the real data | |

**Notes:** CTX-79/80. Diverged seed included (variance signal); < 2 completed seeds →
low-confidence flag.

## verdict + handoff (ACC-06) — agent-decided

| Option | Description | Selected |
|--------|-------------|----------|
| Markdown verdict artifact + FUT-01/FUT-04 handoff update, owner-rendered | go|adjust|rethink + cited evidence; never unqualified "go" on a FAILing gate | ✓ |
| Verdict inferred automatically from the gate | Rejected — the verdict is owner-owned | |

**Notes:** CTX-81. Reflects GAP-38-01's disposition in the handoff.

## Claude's Discretion

All technical/implementation gray areas above were decided by the agent under owner
delegation (2026-07-20). Flexibility retained on module internals, the verify-marker
path + freshness window, plot contents, and the calibration-note/verdict-artifact format.

## Deferred Ideas

- PLAT-01..07 + the trainex-r2 tuning round — deferred pending the ACC-06 verdict.
- D-06 static-epsilon sensitivity check — reviewed, not folded (validation concern, not ACC scope).
- trainex-r1 research handoff — out of scope.
