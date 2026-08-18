---
phase: 46-frame-resolution-gate-aligned-validation
plan: "06"
subsystem: verification
tags: [conf-01, frame-probe, evidence, d-08, d-09, verdict, owner-checkpoint, stop-protocol]

requires:
  - phase: 46-frame-resolution-gate-aligned-validation
    provides: 46-04 evidence writer + manifest-parametric CLI (the sole entry point this plan invokes once)
  - phase: 46-frame-resolution-gate-aligned-validation
    provides: 46-01 confirmed interpreter resolution and dual-frame fixture tolerance derivation
provides:
  - "The one sanctioned real-corpus CONF-01 evidence run, committed (evidence/target-frame/20260727T070221Z/raw.json + summary.md)"
  - "46-VERDICT.md — the measured verdict (VERDICT_AMBIGUOUS) and D-09 branch routing"
  - "A complete STOP-protocol owner-decision surface for the orchestrator (this plan writes no gap register itself)"
affects: [46-07 (BLOCKED pending owner resolution), 47-frame-repair (BLOCKED pending owner resolution), 50-51-stage0-rerun-and-eval (downstream of GAP-46-01's consequence note)]

tech-stack:
  added: []
  patterns:
    - "Evidence-first verdict authoring: 46-VERDICT.md cites only committed raw.json/summary.md bytes, never re-derives or asserts from code inspection"
    - "D-08/D-09 branch routing driven strictly by the machine verdict constant, never by executor judgment about which branch 'should' apply"

key-files:
  created:
    - .planning/phases/46-frame-resolution-gate-aligned-validation/evidence/target-frame/20260727T070221Z/raw.json
    - .planning/phases/46-frame-resolution-gate-aligned-validation/evidence/target-frame/20260727T070221Z/summary.md
    - .planning/phases/46-frame-resolution-gate-aligned-validation/46-VERDICT.md
  modified: []

key-decisions:
  - "GAP-46-02 HARD GATE evaluated first: Status RESOLVED-WITH-INSTRUCTION, Option A (conservative intersection of seed41/42/43 manifests) — the plan proceeded using exactly that basis, quoted verbatim as provenance"
  - "Machine verdict VERDICT_AMBIGUOUS (decide_verdict rule 6, the fail-closed catch-all) routes to D-09 — not the clean D-08 VERDICT_TARGETS_ARE_SCALED continuation; no data-path repair was made under any branch"
  - "GAP-46-01's consequence note records that the measured verdict selects neither of that gap's two evaluator-pairing readings cleanly, though the identity classification (identity_raw=true for 100% of trajectories) leans structurally toward the raw-target reading — recorded as information for Phase 50/51, not a resolution"

patterns-established: []

requirements-completed: [CONF-01]

coverage:
  - id: D1
    description: "GAP-46-02 HARD GATE evaluated before any preflight/probe step; population basis pinned to the exact owner-ratified resolution"
    requirement: CONF-01
    verification:
      - kind: other
        ref: "manifest SHA-256 digests (c25568a1.../5846ae5b.../a8618b0c...) matched GAP-46-02's content-pinned values exactly"
        status: pass
    human_judgment: false
  - id: D2
    description: "Single real-corpus CONF-01 evidence run executed exactly once and committed (D-24)"
    requirement: CONF-01
    verification:
      - kind: other
        ref: "commit f106889b90b84dcc4889427a8e0272dc76f6e59b; raw.json sha256 3fa8251b464600fd2e99f5745bdfb1c315fb0073051de009d2b60a13a7dfcf08; schema/verdict/host-path checks all pass"
        status: pass
    human_judgment: false
  - id: D3
    description: "46-VERDICT.md authored from committed evidence only, D-08/D-09 branch routed exactly per the machine verdict"
    requirement: CONF-01
    verification:
      - kind: other
        ref: "commit 6638204d...; Task 3 verify block (verdict constant + D-0(8|9) + raw.json + tolerance + GAP-46-01 all present) passed"
        status: pass
    human_judgment: true
    rationale: "D-09 routes an owner scope decision that only the project owner can resolve or defer; this deliverable's completeness is machine-verifiable but its resolution is explicitly not this executor's or this plan's to make"

duration: ~25min (estimated; exact session start not independently timestamped — see Performance note)
completed: 2026-07-27
status: complete
---

# Phase 46 Plan 06: CONF-01 Real-Corpus Evidence Run and Verdict Summary

**The one sanctioned real-corpus CONF-01 probe ran once over the GAP-46-02-ratified 1651-trajectory intersection population and returned `VERDICT_AMBIGUOUS` — routing the D-09 owner-checkpoint branch, not the clean D-08 continuation, because 100% of eligible trajectories carry a body-permutation confound that leaves only 66.6% of corrected-raw residuals within numerical tolerance**

## Performance

- **Duration:** ~25 min (estimated — file-reading and analysis phases were not independently timestamped at session start; the two verified bookends are the real-corpus probe run itself, 06:59:13Z–07:02:21Z UTC (~188s), and the two task commits, 07:07:08Z and 07:08:32Z UTC)
- **Completed:** 2026-07-27T07:08:32Z
- **Tasks:** 3 (Task 1 preflight produced no committable artifact — an empty directory is untracked by git; Tasks 2 and 3 each produced one commit)
- **Files modified:** 3 created (2 evidence artifacts + 1 verdict document), 0 modified

## Accomplishments

- **Task 1 HARD GATE evaluated first**, before any other step: `46-GAPS.md` § GAP-46-02 Status = `RESOLVED-WITH-INSTRUCTION`, Resolution note = **Option A** (conservative intersection across the three retained pilot manifests, seed41/seed42/seed43, content-pinned by SHA-256). The plan proceeded using exactly that basis. Interpreter reconfirmed identical to the 46-01 SUMMARY (`torch 2.12.0`, `numpy 2.2.0`). Corpus root reachable via `default_data_root()`'s `git_common_dir_default` resolution; all four README-documented Brutus folders present (`brutus_hierarchical`, `brutus_hierarchical_gold_standard`, `brutus_standard_quasi_random`, `brutus_standard_quasi_random_gold_standard`). All four manifest SHA-256 digests recomputed and matched GAP-46-02's pinned values exactly; the three pilot manifests differ pairwise (confirmed) and the smoke manifest is byte-identical to seed-42 (confirmed, correctly omitted from the probe's `--manifest` set). Blacklist path resolved from `runs/stage0-pilot-seed42/config.yaml`'s `data.blacklist_path` (`../Documentation/problematic_ics_blacklist.json`, resolved against the resolved data root) to `simulation_data/Documentation/problematic_ics_blacklist.json` (repo-relative rendering; SHA-256 `238efd12...`). No probe run occurred in Task 1; the evidence-tree parent directory was created empty.
- **Task 2: the single real-corpus evidence run**, executed exactly once from the worktree root under the confirmed interpreter with all three GAP-46-02 manifests and the resolved blacklist path. Exit 0 (evidence measured and durably written). New run directory `evidence/target-frame/20260727T070221Z/` contains `raw.json` (5.7 MB) and `summary.md` (196 KB), both committed. Verified: `schema_version = "phase46-target-frame/v1"`; `verdict = "VERDICT_AMBIGUOUS"`; manifest hash list matches Task 1's digests exactly; population counts internally consistent (`eligible_count = 1651`, matching GAP-46-02's arithmetic exactly); no `/Users/` byte sequence anywhere in either committed file. `git status --short -- pinn/` showed no change from this task.
- **Task 3: `46-VERDICT.md` authored and the D-09 branch routed.** The machine verdict is `VERDICT_AMBIGUOUS` (not `VERDICT_TARGETS_ARE_SCALED`), so **D-09 applies**: the measured outcome and branch determination were recorded, the verdict document was committed, and all frame-dependent work (Plan 46-07, Phase 47) is declared BLOCKED. No `46-GAPS.md` entry and no `.planning/milestones/v2.2-GAPS.md` entry were written by this executor — those are orchestrator-owned per the plan's explicit prohibition. The full STOP-protocol block is provided below and will also appear verbatim in this plan's completion message under the heading `## CONF-01 BRANCH: OWNER SCOPE DECISION REQUIRED`.

## The measured verdict, in detail

- **Eligible population:** 1651 trajectories, matching GAP-46-02's Option A arithmetic exactly (2,265 Stage-0 physical identities → 2,039 non-test per individual seed → 1,651 all-three intersection).
- **Symmetric hypothesis table (D-03):** both control arms (positive: fully preprocessed ordered/gauged/scaled; provenance: parsed raw with matching raw metadata) are fully self-consistent, 1651/1651 — confirming the measurement apparatus is sound. Neither hypothesis arm is unanimous: `raw_hypothesis` (uncorrected) is 0/1651 consistent (fully separated, matching the ~99x theoretical prediction); `scaled_hypothesis` is 47/1651 consistent (97.2% separated).
- **Confound register (D-04), covering all 1651 eligible trajectories with no exception:**
  - **Body-permutation confound: 1651/1651 (100%).** Every resident position array is paired with a mass vector in a different body order (`(2,0,1)` for 1547 trajectories, `(0,2,1)` for 104) — zero trajectories show the identity permutation.
  - **COM/gauge divergence: 1651/1651 (100%).** Every trajectory's `first_diverging_step` is `com_recenter_boost`.
  - **Identity classification:** `identity_raw = true` for 1651/1651; `identity_scaled = false` for 1651/1651 — structurally "raw-shaped," but the **corrected**-for-permutation raw residual clears the numerical tolerance for only 1100/1651 (66.6%), short of the unanimity `decide_verdict` rule 4 requires for a clean `VERDICT_TARGETS_ARE_RAW`. This specific gap (100% confound prevalence vs. 66.6% corrected-residual pass rate) is exactly why the verdict falls through to the rule-6 fail-closed catch-all rather than resolving cleanly to raw, scaled, or non-frame-divergence.
- **A previously unmeasured population fact:** all 1651 eligible identities are `variant=hierarchical, fidelity=base` — no `standard` or `gold_standard` identity survives the three-manifold Stage-0 intersection. Recorded as a measured fact in `46-VERDICT.md`, without asserting whether it is an intended curriculum property or a labeling artifact (undecidable from this evidence alone).
- **Tolerance (D-06, GAP-46-03):** the ratified two-term measured tolerance (finite-difference floor + fp32 round-trip increment), reported separately from the explicit no-physics-threshold statement. No safety multiplier, percentile, imported threshold, or theory-predicted separation entered the tolerance or the verdict logic.

## Task Commits

1. **Task 1: Preflight** — no commit (empty directory creation only; git does not track empty directories; `git status --short` confirmed nothing to stage)
2. **Task 2: The single real-corpus evidence run, committed** — `f106889b90b84dcc4889427a8e0272dc76f6e59b` (evidence)
3. **Task 3: Author 46-VERDICT.md and route the D-08/D-09 branch** — `6638204d...` (evidence)

Both commits made via `scripts/agent-commit` with `GIT_AGENT_ID="Claude Code (Sonnet 5)"` and `GIT_AGENT_OWNED_PATHS=".planning/phases/46-frame-resolution-gate-aligned-validation/"`, staging only the explicit owned files under this plan's evidence tree — no other in-progress worktree changes (`.planning/config.json`, `.agents/`, `.planning/tmp/`, `docs/work/...`, `phase-40-plan-04-grok.md`) were touched, staged, or committed.

## Files Created/Modified

- `.planning/phases/46-frame-resolution-gate-aligned-validation/evidence/target-frame/20260727T070221Z/raw.json` — the D-05 machine-readable evidence artifact (schema `phase46-target-frame/v1`); 1651 per-trajectory rows, four arm coordinate conventions, confound register, tolerance derivation, population/exclusion accounting.
- `.planning/phases/46-frame-resolution-gate-aligned-validation/evidence/target-frame/20260727T070221Z/summary.md` — the Markdown rendering: leads with verdict + population size, symmetric hypothesis table with controls beside, tolerance stated separately from the no-physics-threshold sentence, full confound register, provenance block.
- `.planning/phases/46-frame-resolution-gate-aligned-validation/46-VERDICT.md` — the phase artifact: headline, evidence citation, symmetric hypothesis table, population/exclusion accounting, confound register, tolerance statement, D-09 branch section, GAP-46-01 consequence note. Self-sufficient: every claim re-derivable from the committed evidence run alone.

## Decisions Made

- GAP-46-02's HARD GATE was evaluated strictly as state (a) (RESOLVED-WITH-INSTRUCTION with Option A named): the plan used exactly the three named manifests, no more, no fewer, and quoted the resolution note verbatim as provenance in both this SUMMARY and `46-VERDICT.md`.
- The D-09 branch was routed strictly because the machine verdict constant is `VERDICT_AMBIGUOUS`, not `VERDICT_TARGETS_ARE_SCALED` — no executor judgment substituted for the machine verdict; the confound-driven near-miss on a clean raw verdict (66.6% vs. the 100% rule 4 requires) is reported as measured context, not treated as license to round up to a clean raw verdict.
- No repair, correction, or "for clarity" rewrite was made to any file under `pinn/` under any branch, per the plan's absolute prohibition.

## Deviations from Plan

None — plan executed exactly as written. No Rule 1/2/3 auto-fixes were needed; the probe ran cleanly on the first invocation (after one operator-side timeout of the interactive shell wrapper at the default 2-minute Bash-tool ceiling, resolved by re-running the same unmodified invocation in the background with a longer wait — not a plan deviation, an execution-environment accommodation for the plan's own documented "expect minutes-scale runtime" guidance).

## Issues Encountered

- The Bash tool's default 2-minute command timeout is shorter than the probe's actual ~188s runtime plus process-startup overhead; the first foreground invocation was killed (`exit 143`, SIGTERM) before completion. Re-ran the identical, unmodified invocation via `nohup` in the background and polled to completion; no retry with altered flags, no partial-corpus workaround. This is an execution-tooling accommodation, not a change to the plan-specified command.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

**BLOCKED.** Per D-09, Plan 46-07 (INST-01 production wiring) and Phase 47 (the target-frame repair phase) remain blocked pending owner resolution or deferral of the CONF-01 ambiguity recorded in `46-VERDICT.md`. The frame-independent INST-01 deliverables already landed in Waves 1-3 (46-01, 46-02, 46-03, 46-05: fixtures, probe core, gate-composition module, isolation/artifact test suites) are complete and unaffected by this branch — they do not themselves require a resolved frame. The full STOP-protocol owner-decision surface is provided in this plan's completion message under `## CONF-01 BRANCH: OWNER SCOPE DECISION REQUIRED`; per governance, this executor does not write `46-GAPS.md` or `.planning/milestones/v2.2-GAPS.md` — those writes belong to the orchestrator.

## Self-Check: PASSED

- `.planning/phases/46-frame-resolution-gate-aligned-validation/evidence/target-frame/20260727T070221Z/raw.json` — FOUND
- `.planning/phases/46-frame-resolution-gate-aligned-validation/evidence/target-frame/20260727T070221Z/summary.md` — FOUND
- `.planning/phases/46-frame-resolution-gate-aligned-validation/46-VERDICT.md` — FOUND
- Commit `f106889b90b84dcc4889427a8e0272dc76f6e59b` — FOUND (`git log --oneline` confirms)
- Commit `6638204d` — FOUND (`git log --oneline` confirms)
- `git status --short -- pinn/` — clean (no modification from this plan)
- `git status --short -- .planning/phases/46-frame-resolution-gate-aligned-validation/46-GAPS.md .planning/milestones/v2.2-GAPS.md` — clean (no gap-register file touched by this executor)

---
*Phase: 46-frame-resolution-gate-aligned-validation*
*Completed: 2026-07-27*
