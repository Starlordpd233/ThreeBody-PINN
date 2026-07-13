# Phase 38 Gap Register

## GAP-38-01 — Real-trajectory rung 3/4 phase-close evidence

- **Decision point** — Whether Phase 38 may close without operator-committed residual + overfit evidence on a real admitted Brutus trajectory.
- **Where in artifact** — `38-06-PLAN.md` must_haves / planner assumptions (phase-close real-dataset gate); `38-06-SUMMARY.md`.
- **Task context** — Plan 38-06 completion in worktree without Brutus payload under `simulation_data/Data/`.
- **Classification** — operational coordination.
- **Source silence** — Worktree has no complete Brutus outputs; plan authorizes DEFERRED entry when payload unavailable (codex M #8).
- **Mathematical / engineering grounding** — Synthetic fixtures prove wiring of model+AD+loss; they do not prove residual/overfit behavior on real integrator trajectories with real tol/Lw/dt_out provenance. Phase-close truth requires one real admitted trajectory or an explicit deferral.
- **Agent was tempted to** — Silently mark phase closed on synthetic-only evidence.
- **What the user needs to decide** —
  - **A (DEFERRED, current):** Keep phase blocked/deferred on real-trajectory evidence until payload is available; operator then runs residual + overfit probes and commits evidence under `evidence/{residual,overfit}/`.
  - **B:** Provide/copy a real admitted trajectory into the dataset path and re-run operator evidence now.
  - **C:** Explicitly waive the real-trajectory gate for v2.0 Phase 38 (would need owner instruction).
- **Confidence of impact** — HIGH — affects phase-close readiness, not the automated NET-05 bar.
- **Status** — `DEFERRED`
- **Resolution note** — Payload unavailable in `.worktrees/trainex` at 2026-07-13 plan-06 completion. Automated suite green on synthetic fixtures. Operator-owned real rung 3/4 evidence remains a phase-close gate.
