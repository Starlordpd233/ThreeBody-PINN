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
- **Status** — `RESOLVED-WITH-INSTRUCTION`
- **Resolution note** — Closed 2026-07-13 via **decision B** (owner instruction 2026-07-13: close on real evidence). The plan-sanctioned recommended default — variant `standard_quasi_random_gold_standard`, id `0000` (admission encoded by gold-standard folder) — was copied read-only from the master-root checkout into the worktree at the loader folder-mapping paths (`simulation_data/Data/brutus_output/brutus_standard_quasi_random_gold_standard/brutus_standard_0000.txt`, sha256 `1e48ae0d…`; paired IC `ic_final/ic_standard_quasi_random/ic_standard_0000.txt`, sha256 `36923ca8…`). Both paths are gitignored (`.gitignore:315/316`) — no tracked noise; the copy is the operator data-provision step decision B authorizes, not a probe write. Rung 3 (residual) PASS: Gate A max rel err 1.495e-15 < 1e-5, Gate B median 0.00647 < 0.1, 1002 snapshots, final_t 10.01 (`evidence/residual/20260713T133400Z/`). Rung 4 (overfit) PASS: L0 0.2192 → Lf 1.997e-4, ratio 1097.6 ≥ 1e3 in 176 steps, lr 1e-4 (`evidence/overfit/20260713T133619Z/`). Recorded in `38-VERIFICATION.md`. Phase no longer closes on synthetic-only evidence.
