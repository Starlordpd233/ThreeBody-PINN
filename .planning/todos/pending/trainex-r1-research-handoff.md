---
title: Review and hand off the trainex-r1 research sub-packages (r1a + r1b)
date: 2026-06-11
priority: high
---

# Todo: Trainex R1 Research Handoff (two parallel sub-packages)

The trainex-r1 foundational round was assembled 2026-06-11 and split into two parallel
sub-packages under `pinn_instruction/markdown_conversion/framework-specs/trainex-r1/`
(`specs/` snapshots pinned to commit `c17e23ed`; design-doc snapshot includes its
2026-06-11 standing note):

- **`research_package_a/`** — decisions & structure: D1 framework, D2 tracking, D3
  compute + ingestion memory strategy, D4 checkpoint policy + auto-guards + diagnostic
  bundle, D5 loop-skeleton capabilities (optimizer family, collocation, loss-weighting
  machinery), D6 determinism policy, D7 stage-boundary mechanics, + baseline critique
  mandate. Output: options menus, door classifications, decision sheet, first-run recipe.
- **`research_package_b/`** — runbook & ops knowledge: K4 feasibility envelope + K5
  trainer-correctness verification ladder (the two priorities), K1 health watchlist, K2
  unattended-Mac ops, K3 runbook patterns. Output: cited findings, parameterized
  estimates, decision-relevant observations.

The shared `DELIVERY-NOTE.md` at the round root is user-facing routing only — never
uploaded. Each sub-package has its own RESEARCH-AGENT-PROMPT.md.

**Status update (2026-06-19):** R1a research returned from **ChatGPT Pro** and landed at
`trainex-r1/research_results/r1a/chatgpt-pro-resolution.md` (committed on the `track/trainex`
worktree branch; build-design channel — an options menu, not a verdict). R1b has not yet
returned. Action 3 below is therefore partially complete (r1a only); consolidation (action 4),
the D1–D7 decision sheet (action 5), and join-point checks are deferred until R1b lands.

**User actions remaining:**

1. Review both RESEARCH-CONTEXT-MASTER.md files — especially r1a's decision areas +
   output contract and r1b's K4 feasibility question.
2. Hand off both in parallel: per each sub-package's RESEARCH-AGENT-PROMPT.md, attach
   its master + the three snapshots from the shared `trainex-r1/specs/` directory, and
   paste its prompt (same multi-AI pattern as issue-02; ERW runbook:
   `docs/runbooks/external-research/2026-06-11-external-research-workflow.md`).
3. Land results under `trainex-r1/research_results/r1a/` and `.../r1b/` as
   `<agent>-resolution.md`.
4. Consolidate into `r1a-resolution-doc.md` + `r1b-resolution-doc.md` (or one joined
   doc). Check the join points listed in DELIVERY-NOTE.md (K4 duration → first-run
   recipe and D4 cadence; decision-relevant observations → decision menus).
5. Fill in the r1a decision sheet — your D1–D7 picks and keep/change calls on baseline
   deviations are the actual decisions, recorded as project Key Decisions.
6. The resolutions + picks unblock: runbook v0 draft (from K findings), trainex-r2
   (numeric tuning inside the D5 skeleton), and one trigger input for
   `.planning/seeds/ctl-pinn-build-milestone.md`.

**Note:** the packages, the design-doc standing note, and the trainex planning artifacts
were committed 2026-06-11 (late evening). Phase 25 planning changes from concurrent
sessions remain uncommitted and are owned by those sessions.
