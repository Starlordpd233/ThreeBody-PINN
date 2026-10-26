# Phase 64: Feasibility Verdict - Research

**Researched:** 2026-10-25
**Domain:** an evidence-backed verdict and charter written from frozen v2.4 records; a read-only CPU re-derivation of committed network weights; owner-checkpoint mechanics; requirement-traceability close
**Confidence:** HIGH for the in-repo evidence map, the frozen-code behaviour and the cheap check commands (each re-run this session). MEDIUM for the two published comparison points (read from arXiv excerpts, not whole papers). LOW, proposal-level, for every numeric charter bar and the budget (the owner decides).

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

#### Verdict wording
- **D-01: Side by side.**
  - The headline states the frozen rule's output exactly as pre-registered: RETHINK-REPRESENTATION, for "G2 fired and the sweep rescued nothing".
  - Directly beside it, a plain box states what the evidence shows. Source: `60-VERIFICATION.md`, "Independent observation for Phase 64".
    - Every trained network learned only each body's average position, so it is a time-constant predictor.
    - Its accuracy curves stayed flat.
    - The sweep varied only `first_omega_0`.
    - So the records cannot yet tell a design limit from a limit of the fixed training recipe.
  - Nothing pre-registered changes and the label is not amended. Amending it after seeing the result would need a formal amendment with the owner's sign-off (SCOPE-42, SCOPE-43). The owner chose "Side by side".
- **D-02: Explain the qualifier field plainly.** This item comes from the agent reading the code. It is not an owner choice.
  - `stop-handoff.json` records `representation_limit_qualifier: false`. `decision_verdict` returns `false` on the G2 path without evaluating the qualifier, and it refuses a Rung 1 comparison input on that path (`pinn/verification/feasibility_scorecard.py:735-752`).
  - The amendment's text applies the qualifier "whatever the branch" (`docs/work/designs/cross_cutting/v2.4-milestone-proposal/2026-10-11-v2.4-feasibility-amendments.md:187-189`).
  - The two do not conflict in substance. On this branch the label already names the representation as the limit. On the committed numbers the qualifier's condition also holds: Rung 1 is Tier 0 on all three systems, and its E is lower than the formula's only on 4658.
  - The verdict reports the field exactly as recorded. It adds one plain sentence: here `false` means "not evaluated on this branch", not "the condition failed". The verdict does not recompute or change the field.
- **D-03: Candidate fixes for the next milestone, unranked.** The owner chose "Design and recipe".
  - The pre-registered design changes: time-windowed networks, a different output frame, new input features or architecture, a shorter window (REQUIREMENTS "On RETHINK-REPRESENTATION" routing).
  - The untested recipe suspects beside them: learning rate, optimizer, schedule, depth.
  - trainex-r5 ranks them, not this phase.
- **D-04: One figure.** It shows system 1632's real orbit beside the network's prediction.
  - It is drawn read-only from the committed weights and takes seconds on the CPU.
  - It is saved next to the verdict, with its source paths and SHA-256 hashes.
  - The owner chose "Yes, one figure".

#### Cost estimates
- **D-05: Measured + for-scale.** The owner chose "Measured + for-scale". The cost section gives:
  - the hours spent per rung, from `stop-handoff.json`: 22.378 h of arm wall time in Phase 60, plus each arm's wall hours and timed seconds per step (about 0.011–0.0136 s);
  - the measured cost of one single-orbit experiment on this Mac (about 2.6–3 h for most arms; the exact per-arm values are in `stop-handoff.json`);
  - a costed first step for v2.5;
  - a clearly labelled for-scale figure for the finish, from published step counts (amendments doc `:227-230`: generation 7 at 12.3 s per step × about 200,000 Adam steps ≈ a month of nonstop computing).

  Every assumption is stated. "Hours to the next level" is not projected from the flat curves.
- **D-06: This Mac only.** All computation runs on the owner's Mac (Apple M5 Pro, 24 GB). This is a standing owner rule (`.planning/PROJECT.md` Constraints; trainex-r1 design, 2026-06-10). The owner restated it twice in this discussion.
  - The verdict, the charter and the next-milestone proposal contain no GPU figures, prices, speed-up assumptions, tripwires or GPU-dependent routes.
  - The amendments doc's rented-GPU clause (`:222-225`) is superseded. ROADMAP criterion 3, FEAS-06 and the FEAS-10 budget item were corrected in `bb323a52`.
  - No claim that the Mac can or can't handle a workload is made without measured evidence. Where a projection is unknown, the verdict says so and names what would measure it.
  - The charter records the owner's words under its budget item. Latest statement, verbatim: "For now, the only device on which we will do the computation will be on this MacBook, so ignore any proposal or route where it requires a rented GPU, either that is a cloud GPU or some other thing. That will not be something that we should consider at this point, so right now treat every single computation that will be needed done on this Mac."
  - Earlier statement, verbatim: "We will not have access to a rented GPU unless that is absolutely necessary and it is proven to make a difference. I will not invest into buying or renting a separate GPU for speeding up the work. The training process should be done on this Mac. does that make sense? tell me if this mac cannot handle the computation. I doubt that's the case. but that statement also requires lots of proofing and actual evidence to support. so I would be careful making any statements toward that"

#### Charter draft (FEAS-10)
- **D-07: Purpose.** The owner's answer, verbatim (2026-10-25): "1 and 2. we're not aiming for a perfect research result. I think this project could be more for like a PoC because not many people have done training PINN for 3 body porblems in the past. does that make sense? also, i'm just a freshman in college, and all i have this macbook. so reasonably we wouldn't achieve somethign great here. but it's just good to see some positive results coming out."
  - "1 and 2" are the first two options offered: Learning and Research paper.
  - Read together, this is a learning project whose research output is a proof of concept, a modest positive result rather than a polished paper.
  - The charter records the answer verbatim. The definition of done and the pass bars are drafted from it.
- **D-08: Pre-filled draft.**
  - Every charter item gets a few options and a recommended answer, already filled in, so the owner can approve the page as it stands or change single lines at checkpoint ①.
  - Items the owner leaves open are recorded as open.
  - This was the agent's default, stated to the owner on 2026-10-25 with no objection. The owner asked why so many questions were needed, so checkpoint ① should take as little of the owner's effort as possible.
- **D-09: Pass bars.** This was the agent's default, stated with no objection.
  - Stage 0 gets a concrete proposed bar, with a position criterion and an energy criterion (never energy alone), fixed before any held-out exam.
  - The bar aims at a reachable positive result for a proof of concept. It is set against the comparison points: the two-Kepler formula, the nearest-neighbour copy, Breen et al. (arXiv:1910.07291) and the 2026 PINN study (arXiv:2607.23501).
  - Stages 1–6 are listed and marked open.
  - On `10⁻⁵`, the draft recommends replacing it, by formal amendment, with a bar based on evidence. That follows the owner's recorded lean (amendments doc `:235`). Moving a locked value is outside the delegation, so the owner decides.
- **D-10: GAP-59-08 at the checkpoint.** This was the agent's default, stated with no objection.
  - Its options A, B and C (`59-GAPS.md`; A is recommended) sit beside the pass bars, because the energy criterion depends on how energy is measured.
  - Today's finite-difference check gives even the exact Brutus orbits 5–38% error.
  - Any proposed energy bar is written as conditional on the owner's answer.
- **D-11: Budget.** The budget is how many months of computing on this Mac. The draft offers options and a recommendation. It states the measured per-experiment cost from D-05 so the owner can size it.
- **D-12: Stop rule.** FEAS-10's draft text is the recommended default: "a milestone that neither climbs a ladder level nor beats the best fixed-scorecard result means stop or change approach, with no third attempt at the same idea."
- **D-13: Routed items the charter records.**
  - `ctl_instruction.md`'s evaluation section (`:2057`, `:2081`, `:2111`) describes results that do not exist. Its rewrite is routed to the milestone that sets the bars.
  - `PROJECT.md`'s "What This Is" and Core Value still describe the LLM project. A rewrite matching the charter is drafted and applied only on the owner's approval at checkpoint ①.

#### Next milestone
- **D-14: v2.5, committed only to its name and first phase.**
  - The first phase is the trainex-r5 research round: open-book (Route B), diagnosis first, on why every trained network predicts a time-constant position.
  - `/gsd-new-milestone` plans the later phases.
  - Work continues in `.worktrees/trainex`.
  - This was recommended on 2026-10-24 and the owner proceeded on that basis. It was restated as the default on 2026-10-25 with no objection.

### Claude's Discretion
- The verdict and charter documents: structure and file names. The v2.0 precedent keeps them in the phase directory: `.planning/milestones/v2.0-phases/43-verification-stage-0-pilot-acceptance/43-VERDICT.md`.
- The figure: its styling, and how its script loads the weights. Reuse the Phase 60 verifier's real-data loading path.
- The layout of the readiness-ladder evidence table.
- Plain-language wording throughout. The owner is a first-year student, so lead with what happened and define each term once.

### Deferred Ideas (OUT OF SCOPE)

#### Reviewed Todos (not folded)
- `.planning/todos/pending/d-06-static-epsilon-sensitivity-check.md` is about stage labels and validation gates, which Phase 64 doesn't set. The owner declined it for Phase 60 for the same reason. Its "D-06" is an earlier phase's decision number, not this file's D-06.

#### After Phase 64
- `/gsd-complete-milestone` for v2.4.
- Merging v2.4 into master, only with the owner's explicit OK.
- The GitHub backup, handled by a separate agent.

#### Optional Phase 60 follow-ups (user-invoked, not Phase 64 work)
- `/gsd-code-review 60`, `/gsd-secure-phase 60`, `/gsd-validate-phase 60`.
- `60-VALIDATION.md` is still `status: draft`.
- The `plan_head_before` in `60-13-SUMMARY.md` is malformed.

Out of scope (CONTEXT `<domain>`): new training or tuning runs; the held-out exam; any change to the frozen scorer, the frozen decision rule or a pre-registered output; the trainex-r5 research itself (v2.5); resolving GAP-59-08 (the owner decides it at checkpoint ①); merging v2.4 into master; the GitHub backup.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| FEAS-06 | The feasibility verdict, plain language first: tier per rung and where along the window each broke; the control's readout branch; the best `ε_H` against the locked bar; the result under the pre-registered rule; the next milestone; the readiness level with evidence per level; each rung beside the comparison points, accuracy curves, survey and probes; the cost on this Mac only. Presented at checkpoint ① with the charter; the owner's decision recorded verbatim. | "Evidence Map" gives the committed file and key behind every clause. "Findings that correct the brief" fixes what `trace` can and cannot show. "Comparison points" is the first primary-source read of both papers in this repo. "Cost inputs" holds every measured primitive. "Code Examples" 1-2 re-derive the numbers and the label. |
| FEAS-10 | The one-page project charter: purpose, definition of done, current level, pass bar per stage (position and energy criteria, fixed before any held-out exam; `10⁻⁵` retained or replaced by formal amendment), budget in months on this Mac, a stop rule; records that `ctl_instruction.md:2057/:2081/:2111` describe results that do not exist; on approval rewrites `PROJECT.md` "What This Is" and Core Value. | "Charter inputs": anchors, option menus, GAP-59-08, the prior checkpoint patterns (60-17, 58-VERDICT, 43-VERDICT) and the verbatim-quote mechanics. |
| VER-22 | Every v2.4 requirement maps to exactly one phase, re-verified at close against the final count. | "VER-22 mechanics": the VER-21 precedent, a prototype that counts 24 defined, 24 in the table, 24 in the ROADMAP lines, no duplicates, no orphans, and the open question on the 12 requirements whose phases were skipped. |
</phase_requirements>

## Summary

Phase 64 is a document-and-verification phase. Its one input is `.planning/phases/60-single-system-learnability/evidence/g2/stop-handoff.json` (SHA-256 `7ed8223c066e62bd55e527dc703565367a0f9764a253e086a3bc0b4e719d02d5`), plus the records it points at. The frozen rule's output on those inputs is `RETHINK-REPRESENTATION`. I re-ran the frozen `decision_verdict` on the committed inputs this session and it returns exactly the handoff's dictionary. Nothing about the phase needs training. Everything it needs to compute is a CPU float64 re-score of committed weights: all seven arms and both states took 5 seconds, read only train-split files (test-split opens 0, validation opens 0), and reproduced the Phase 60 verifier's "time-constant predictor" observation to the digit. That observation was computed in an uncommitted scratch script, so the verdict cannot quote it until a committed script re-derives it. That script, a small independent verifier, is the main new engineering in this phase.

The brief carries four premises that the files do not support, and the planner must not inherit them (see "Findings that correct the brief"). The `trace` lists in the arm records are convergence curves against training step, not error along the window. "Where along the window each rung broke" comes from the recorded valid-horizon fractions (0.0 and 0.0) and from a re-derivation: the worst body's error was already 80–101% of the system size at the first scored moment (the inner pair's error 89–100% of its separation), and at none of the 1,001 scored times, in any of the 14 scored states, was the error at or below the Tier-1 limit of 0.1. The headline `E` values (1.1574 and so on) are MPS float32 numbers from the records; the CPU float64 re-derivation differs in the third or fourth digit, so every quoted number must say which it is. No plotting library exists in the `pinn-train` environment (no matplotlib, scipy or pandas), so the figure should be a stdlib SVG, which I prototyped, rendered and checked for byte-determinism. And the repo holds no primary-source reading of the two comparison papers: Phase 59's research says "cited by the amendment; not re-fetched". I read both on arXiv. One amendment figure is off (the 2026 study's energy range is about 0.02–3%, not 0.08–3%), and neither paper trained one network over many initial conditions.

**Primary recommendation:** write `64-VERDICT.md` and `64-CHARTER.md` from committed records, gate them with a small independent verifier (`evidence/verify_phase64_verdict.py`) that re-derives every quoted number, scans for rented or cloud GPU wording, and proves no frozen file changed; draw the one figure as a stdlib SVG from a CPU float64 load of the committed polish weights; present the pre-filled charter at one blocking `checkpoint:decision`, recording the owner's words verbatim in an `owner-quote` fence and asking again if ambiguous; apply the `PROJECT.md` rewrite only on approval; run the VER-22 check last, against 24.

## Findings that correct or extend the brief

1. **`trace` is not along-window data.** `record.json` `trace` has 22 entries (43 for `r1-4658`) of `{E, elapsed_seconds, eps_h, step, tier}` at training steps 0, 39717, 79434 and on. It is the convergence curve (`record.json:492-653` in `r1-1632`). Along-window information lives only in `result.h` (`record.json:251-260`: `[[0.01, 0.0], [0.1, 0.0]]`) and in a re-derivation from the weights. [VERIFIED: `.planning/phases/60-single-system-learnability/evidence/arms/r1-1632/record.json:247-263`, quoted `"h": [[0.01, 0.0], [0.1, 0.0]]`; `pinn/verification/feasibility_scorer.py:223-239`, quoted "First scoring time where ``max(e_sys, e_in) > delta``, divided by ``T``."]
2. **D-02's line numbers.** The G2 branch is `feasibility_scorecard.py:734-752` (`if g2_fired:` is line 734; the nested `if sweep_rescued:` is 735). The behaviour D-02 describes is exact: [VERIFIED: `pinn/verification/feasibility_scorecard.py:734-752`] `raise OwnerRouted("owner checkpoint 4")` on a rescue; `raise ValueError("later-rung inputs must be None when G2 fired: " ...)` if any later-rung input is given; and the return is `{"verdict": gate["on_no_rescue"], "representation_limit_qualifier": False, "reasons": ["G2 fired and the sweep rescued nothing"]}`. Off the G2 path the qualifier is `sum(rung1) < qualifier_min` (`:771-775`), and `qualifier_min` is `2` [VERIFIED: `pinn/verification/artifacts/feasibility_scorecard_v1.json:69`, quoted `"rung1_representation_qualifier_min_count": 2`]. Evaluated off the refused path on the committed records, Rung 1's `E` is below the formula's on 1 of 3 systems (4658 only), and `counts()` is true on 0 of 3, so the condition would hold either way. [VERIFIED: re-derived read-only this session.]
3. **Official numbers are MPS float32.** Every `E`, `ε_H` and tier in the arm records' `result` and `score_gold` blocks comes from the MPS float32 run. The CPU float64 cross-check is stored separately in `states.<state>.cross_check` and differs in the third or fourth digit (for `r1-1632` polish: MPS 1.157387, CPU 1.159997). Label every quoted number "official (MPS float32)" or "re-derived (CPU float64)".
4. **The repo never read the two papers.** `59-RESEARCH.md:984`: "Breen et al., arXiv:1910.07291, and arXiv:2607.23501 (cited by the amendment; not re-fetched)". The Phase 59 "survey" is the dataset survey (FEAS-08), not a literature survey. See "Comparison points". The amendment's "0.08–3%" for the 2026 study should read "about 0.02–3%".
5. **No plotting library.** `pinn-train` has numpy 2.4.6, torch 2.12.1, Pillow 12.3.0, h5py and PyYAML; matplotlib, scipy, pandas and plotly are absent, and no other Python on the Mac has matplotlib. Installing needs the owner's permission and is not needed.
6. **`default_data_root()` depends on the working directory.** It runs `git rev-parse --git-common-dir` in the cwd (`pinn/data/adapter.py:603-606`). Run from outside the repository, my first figure attempt failed with exit 128. Run every data-dependent mode from the repository root (or set `GSD_DATA_ROOT`).
7. **"Flat" needs numbers.** In all seven arms `E` falls from 35.6–76.7 at step 0 to 1.3–1.6 at the first reading (about 5% of the budget), then creeps to 1.14–1.24, a range of 0.27–0.59 after the first reading. "Plateau" with those numbers is accurate; an unqualified "flat" is not.
8. **"Best `ε_H`" has three readings.** The official best is 123.617 (`g2s-1632-w240`). The lowest on any scored state is 30.295 (`r1-1632` Adam). The lowest on any trace reading is 0.9999 (`r1-4658`, step 1,863,178). All are about 10⁵ times the `10⁻⁵` bar or more (0.9999 is 99,992 times it). Quote the official 123.62 and footnote the most favourable reading so the number cannot look chosen.
9. **The proposal's own gloss overreaches.** The original proposal says RETHINK-REPRESENTATION "Meaning: the network cannot represent a single Stage-0 trajectory over the window even when shown the answer, so no change to the training recipe can fix it" (`2026-10-09-v2.4-roadmap-proposal.md:148-150`). The sweep varied one setting on one system, so the evidence does not carry the second half. D-01's side-by-side box exists for this; do not repeat the gloss as established.
10. **The rented-GPU clause survives in a consumed design doc** (`2026-10-11-v2.4-feasibility-amendments.md:222-226`, "on this Mac and on a rented GPU ... including the GPU speed-up"). The registries were corrected in `bb323a52`; the doc was not. An executor who reads only the amendments doc will reintroduce it. See the mechanical guard in "Validation Architecture".
11. **Phase 59's 604 s `final` is not needed.** Its producer modules and evidence have no diff since `4df5d4a8` (checked this session over 10 modules and two directories), so its `PHASE59-EVIDENCE-OK` still stands. Cheap modes exist (see "Environment Availability" and "Validation Architecture").

## Project Constraints (from CLAUDE.md)

Directives that bind this phase (repo `CLAUDE.md`, global `CLAUDE.md`, `.claude/rules/`):

- **STOP protocol.** v1.4-style governance applies to similar adjudication milestones. Do not invent content where sources are silent. A semantic or process-artifact decision must be surfaced, never made silently. Gaps are recorded by the parent agent in `.planning/phases/64-feasibility-verdict/64-GAPS.md` and `.planning/milestones/v2.4-GAPS.md` (subagents return findings only). Candidates from this research are listed in "Open Questions".
- **Git.** Surface `git status --short --branch` at start and before committing; existing changes are user-owned. Commit only through `scripts/agent-commit` with `GIT_AGENT_ID` and `GIT_AGENT_OWNED_PATHS`; stage explicit paths (never `git add .`, `-A`, `-u`); no `--no-verify`. Subject: `<type>(<scope>): <lowercase imperative>`, at most 80 characters, no trailing period, no ticks, quotes or semicolons. Types: `spec`, `evidence`, `verify`, `plan`, `docs`, `feat`, `fix`, `refactor`, `test`, `chore`. Scope: `64` or `64-NN`. A body is required for `spec`, `evidence`, `verify` and `plan` commits and for multi-file or `.planning/` commits. A trailer `Agent-Assisted-By:` or `Co-Authored-By:` is required. Never push from `master`, `main` or `milestone/*`. Do not stage the two files already dirty in this worktree: `.planning/config.json` and `docs/work/designs/milestone_v2.2/50-valid-stage-0-re-run/2026-08-16-stage0-causal-front-halt-brief.md`.
- **Worktree.** v2.4 work lives in `.worktrees/trainex` on `milestone/v2.4`.
- **Docs.** Anything new under `docs/work/` needs the frontmatter block and a date-prefixed name, in a purpose folder, never a legacy path. Phase 64's deliverables belong in `.planning/phases/64-feasibility-verdict/` (D discretion, v2.0 precedent), so no docs file is needed.
- **Evidence integrity.** When a commit asserts a verifiable invariant, record the supporting hashes or counts in committed state, not in `/tmp`.
- **Global.** Minimum complete change; no new dependency without asking (so no matplotlib); show evidence of checks run; retain full output of any command expected to exceed 60 s outside the repo and do not rerun it unchanged.
- **Tooling directive.** `CLAUDE.md` says to use the Sequential Thinking MCP for any task with more than one step. It was not available in this research session's toolset; the planner and executor should use it where present.
- **Memory-derived project lessons** (user memory, applied here): plan `<automated>` gates run under zsh and do not word-split unquoted variables; smoke every new verifier mode read-only on real artifacts first and test with real object shapes; `scripts/agent-commit` appends its own `-m` after your arguments, so no `--` pathspec; the `gsd-tools` state and roadmap mutating verbs corrupt files here, so edit STATE and ROADMAP by hand and diff; the generic post-merge wave gate passes vacuously here, so run the phase's own commands; do not auto-advance STATE or close the milestone.
- **`/gsd-plan-phase` gate notes for this repo** (user memory, 2026-07 to 08): `check gap-analysis-plan-post` is milestone-scoped and non-blocking, so check the phase's own IDs (FEAS-06, FEAS-10, VER-22) against each plan's `requirements:` field instead; the decision-coverage gate may mis-parse, so cover D-01 to D-14 by hand against the coverage map below; the UI plan-gate keyword trips on "UI hint: no" lines, and this phase's ROADMAP section has none (checked), so it should not fire.

## Architectural Responsibility Map

This phase has no web tiers. The tiers below are the layers a number or a decision passes through.

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| A number quoted in the verdict | Evidence store (committed JSON records, SHA-256 cited) | Verifier (independent re-derivation) | No number is typed by hand; it traces to a file and key and is re-derived |
| The pre-registered label | Frozen code (`decision_verdict`) via the sealed handoff | Verifier recompute | The label is never edited or re-computed by hand |
| Time-constant-predictor evidence and the figure | Derivation layer (CPU float64 re-score of committed weights, train split only) | Evidence store (provenance JSON) | Not in any committed record; a committed script must re-derive it |
| Plain-language narrative | Document layer (`64-VERDICT.md`, `64-CHARTER.md`) | Verifier structure checks | Written from the evidence map; gated by contract checks |
| Continue, change course or stop; charter choices | Human decision layer (checkpoint ①) | Record layer (`owner-quote` fence) | Only the owner decides; the agent records verbatim and never infers |
| Requirement, roadmap and project registries | Planning-registry layer (hand edits, diffed) | Verifier (`traceability`) | The `gsd-tools` mutating verbs are unreliable here |
| Frozen and sealed inputs | Git plus the sealed protocol hashes | Verifier (`frozen`) | Any edit to a pinned path is drift |

## Evidence Map (success criterion to committed source)

Paths are relative to the repository root. `P60` = `.planning/phases/60-single-system-learnability/evidence`; `P59` = `.planning/phases/59-read-only-baseline-scorecard/evidence`.

| Criterion | What the verdict states | Committed source (file : key or lines) | Re-derivation or check |
|---|---|---|---|
| 1. Tier per rung | Rung 1 is Tier 0 on 1632, 851 and 4658. The four sweep arms (system 1632) are Tier 0, labelled "below Tier 1". Rung 2, the probes, Rung 3 and the control did not run. | `P60/arms/<arm>/record.json` `result.tier` (r1-1632 `:247-263`); `P60/g2/g2-outcome.json` `tiers` `[0, 0, 0]`, `g2_fired` `true`; `P60/g2/sweep-curve.json` four rows `label` "below Tier 1"; `P60/g2/skip-records.json:12-21` FEAS-04 and FEAS-09 `skipped: true`, `reason: "no rescue"`; `P60/g2/stop-handoff.json:80` "skipped at G2, not failed" | `verifier inputs`: recompute `g2_fires` and tiers from the records; assert exactly seven arm directories and no `r2*`, `p*`, `c-*`, `continue/` or `rescue.json` (the absences 60-VERIFICATION checked) |
| 1. Where along the window each broke | Valid horizon is 0.0 at 1% and at 10% on every arm: the first scored moment (t = 0) was already outside both limits. At no scored time was any state within 10%. | `result.h` in each record (`[[0.01, 0.0], [0.1, 0.0]]`). Re-derived only: `e_sys(0)` 0.805–1.009, `e_in(0)` 0.894–0.998, best moment (min over t of `max(e_sys, e_in)`) 0.817–0.935, scored times within 0.1: 0 of 1001 in all 14 states | `verifier derive` (CPU float64; Code Example 1) |
| 1. Control's readout branch | The control did not run (Phase 63 skipped at G2); there is no branch. | `stop-handoff.json:80`; ROADMAP `:144-151`, `:406`. `decision_verdict` raises if `control_branch` is not `None` on the G2 path (`feasibility_scorecard.py:737-747`) | state it plainly; do not write "n/a" without the reason |
| 1. Best `ε_H` against the locked bar | 123.617 (official, `g2s-1632-w240`) against `10⁻⁵`: about 1.24 × 10⁷ times the bar. No arm reached Tier 1, so none is near Tier 3. | `P60/g2/sweep-curve.json` row `g2s-1632-w240` `eps_h` `123.61725046233964`; `pinn/verification/artifacts/feasibility_scorecard_v1.json:616-620` `"E_max": 0.01`, `"eps_h_max": 1e-05`, `"tier": 3`; `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:1087` "the gate fails if ANY held-out trajectory's `eps_H` exceeds `1e-5`" | footnote the most favourable reading (Finding 8); say plainly that `ε_H` is not a measure of correctness for a near-constant predictor (see Pitfall 5) |
| 1. Result under the rule | `RETHINK-REPRESENTATION`, reason "G2 fired and the sweep rescued nothing", `representation_limit_qualifier: false` | `P60/g2/stop-handoff.json:84-90`; `feasibility_scorecard_v1.json:390` `"on_no_rescue": "RETHINK-REPRESENTATION"` | `verifier inputs`: call `decision_verdict(g2_fired=True, sweep_rescued=False, ... None ...)` and require equality with the handoff (verified equal this session, Code Example 2) |
| 2. Readiness ladder | Level 1 is the highest level with every level below it reached (rule: amendments `:198-203`). Levels 2 to 9 are not tested or not reached. | Ladder table: amendments `:205-216`. Level 3 text: `stop-handoff.json:77` `"level3": "not tested (skipped at G2)"`. See "Ladder evidence" below | cite, do not recompute |
| 2. Comparison points | Formula `E`: 0.9168, 0.4312, 1.9697. Formula reaches Tier 1 on 1 of 1812 training and 0 of 227 validation systems; median `E` 0.989 and 0.940. Nearest-neighbour copy median `E` 2.135, Tier 1 on 0 of 227. Published: see "Comparison points". | `record.json` `formula.E_formula` (r1-1632 `:158-161`); `P59/baselines/baselines.json` keys `formula_tier_counts`, `median_E` (`formula_train` 0.9890032980038623, `formula_validation` 0.940265743143744, `copy_validation` 2.135396659314407), `nn_copy_reaches_tier1_on_validation` "0 of 227" | `verifier numbers` |
| 2. Accuracy curves | Rung 1 and sweep arms only: `E` from 35.6–76.7 at step 0 to 1.3–1.6 at the first reading, then 1.14–1.24 at the end. No Rung 3 or control curves exist. | `record.json` `trace` and `budget.readings` | `verifier numbers` (first reading, last, range after first) |
| 2. Survey | Stage-0 median error growth `e^(T/τ_L)` 1.22; Stage 4b 28.53; Stage 6 351.6; Stage 3 empty; stage mapping beyond 0 and 1 is owner-pending; findings are reported, not gating | `P59/survey/survey.json` per-stage; `59-FINDINGS.md:104-166` | `verifier numbers` for the quoted cells |
| 2. Hard-stage probes | Skipped: reason "no rescue". The pre-declared picks (`standard/base/2279`, Stage 4b; `standard/base/3418`, Stage 6) were never trained or scored. | `P60/g2/skip-records.json:17-20`; `P59/survey/picks.json`; `60-FINDINGS.md:85-87` | state plainly that nothing is known about the hard stages |
| 3. Machine hours | 22.378 h of arm wall time in all: Rung 1 11.108 h (3 arms), sweep 11.270 h (4 arms). Per-arm values below. | `P60/g2/stop-handoff.json:83` `total_wall_hours` `22.37828873402778`, `arms[*].wall_hours`, `seconds_per_step`; records `wall.*`, `timing.*`, `budget.*` | `verifier numbers` (sum equals the handoff total) |
| 3. Cost to the next level and the finish | Measured primitives plus a labelled for-scale figure; no projection from the flat curves; no GPU content. See "Cost inputs". | stop-handoff; `runs/stage0-v23g7-seed42/status.json:21` `"s_per_step_ema": 12.31781584770918`; amendments `:228-231` (for scale only) | `verifier numbers`; `verifier rules` (D-06 guard) |
| 4. Next milestone | v2.5, first phase the trainex-r5 research round, open-book (Route B), diagnosis first | CONTEXT D-14; REQUIREMENTS `:370-372` ("On RETHINK-REPRESENTATION"); ERW runbook `docs/runbooks/external-research/2026-06-11-external-research-workflow.md:53-60` (Route B) | string checks in `verifier rules` |
| 5. Charter | Purpose (verbatim), definition of done, level, bars, `10⁻⁵`, GAP-59-08, budget, stop rule, routed items; owner decision and choices verbatim; open items recorded as open | CONTEXT D-07 to D-13; REQUIREMENTS `:196-211`; `59-GAPS.md:281-333`; `ctl_instruction.md:2057`, `:2081`, `:2111` | `verifier charter` and `verifier ruling` |
| 6. Traceability | 24 requirements, each in exactly one of Phases 59 to 64 | REQUIREMENTS `:5`, `:394-424`; ROADMAP per-phase `**Requirements**:` lines | `verifier traceability` (prototype counts 24, 24, 24) |

### What is absent, and where the absence is recorded

| Absent | Committed record of the absence | Do not do |
|---|---|---|
| Rung 2 (FEAS-04) and probes (FEAS-09) | `P60/g2/skip-records.json:12-21`; `arms/` holds exactly seven directories | do not report a Rung 2 comparison; do not write "failed" |
| Confirmation run, checkpoint ④ | `P60/g2/sweep-curve.json` `confirmation_arm: null`, `confirmed_first_omega_0: null`; `stop-handoff.json:79` `"owner_answer": null`; no `60-CHECKPOINT-4-RULING.md` | do not fill `owner_answer` or `verdict_note`; the handoff is sealed |
| Phases 61 to 63 (CONF-10/11, INST-06/07, SPEC-07 to 10, GATE-05, FEAS-05, RUN-06, DIAG-08) | `stop-handoff.json:80`; ROADMAP `:135-151`, `:404-406` | do not say "failed"; Level 2 and Level 4 are "not tested" |
| R_ref re-measure, GATE-04 re-run | `P60/run-protocol.json` decision D-07 (continue path only) | none |

### Ladder evidence (levels 0 to 9)

| Level | Capability | Verdict reading | Evidence to cite |
|---|---|---|---|
| 0 | Data and specs exist | Reached | `runs/stage0-v23g7-seed42/training_metadata.json` `n_train` 1812; `validation.jsonl` `gate_n_trajectories` 227; `P59/census/census.json`, `P59/survey/survey.json`; the two locked specs |
| 1 | The training code runs | Reached, not to spec | Generation 7 ran 951 steps (`runs/stage0-v23g7-seed42/status.json:25-26` `"state": "failed"`, `"step": 951`). v2.0 pilot: seeds 41, 42, 43 each finished 300 of 300 finite steps (`43-VERDICT.md:43`). Phase 60: seven real arms ran 0.8 to 2.0 million Adam steps each through the trainer's own loss functions (`record.json` `run_kind: "real"`). "Not to spec": REQUIREMENTS `:24-29` (five divergences in the v2.0 pilot; generation 7 evaluated physics on one trajectory per step) |
| 2 | The code provably matches the spec (CONF-10/11 and a mechanical code-against-spec check) | Not tested: Phase 61 skipped at G2, and the generation-7 defect is a known unmet item | ROADMAP `:135-142`; REQUIREMENTS `:28-29` |
| 3 | Learns one system (Rung 2b counts on at least 2 of 3) | Not tested (skipped at G2). Say that Rung 1, the easier exam, ended at Tier 0 on 3 of 3, without saying Level 3 failed | `stop-handoff.json:77`; `skip-records.json:22` |
| 4 | Learns a small family (Rung 3 on at least 12 of 16) | Not tested (Phase 62 skipped) | `stop-handoff.json:80` |
| 5 to 9 | All Stage 0 and unseen systems; the one-shot Stage-0 exam; Stages 1 to 2; 3 to 5; 6 | Not reached; the held-out evaluation stays unspent (SCOPE-40) | amendments `:212-216`; REQUIREMENTS `:320` |

### Per-arm table (official, MPS float32; the verdict's core table)

| Arm | System | Official state | Tier | E | ε_H | Formula E | Adam steps | Timed s/step | Wall h |
|---|---|---|---|---|---|---|---|---|---|
| r1-1632 | 1632 | polish | 0 | 1.1574 | 705.69 | 0.9168 | 794,350 | 0.013596 | 2.573 |
| r1-851 | 851 | adam | 0 | 1.2375 | 165.50 | 0.4312 | 980,523 | 0.011015 | 2.842 |
| r1-4658 | 4658 | adam | 0 | 1.1432 | 13,127.5 | 1.9697 | 980,623, doubled once to 1,961,246 | 0.011013 | 5.693 |
| g2s-1632-w060 | 1632 | adam | 0 | 1.1569 | 4,052.3 | 0.9168 | 908,063 | 0.011893 | 2.730 |
| g2s-1632-w120 | 1632 | adam | 0 | 1.1561 | 1,342.9 | 0.9168 | 955,466 | 0.011303 | 2.903 |
| g2s-1632-w240 | 1632 | adam | 0 | 1.1539 | 123.62 | 0.9168 | 994,807 | 0.010856 | 3.046 |
| g2s-1632-w480 | 1632 | adam | 0 | 1.1575 | 4,170.1 | 0.9168 | 842,770 | 0.012815 | 2.591 |

[VERIFIED: re-derived read-only from the seven `record.json` files this session; the handoff holds `wall_hours` and `seconds_per_step` for each (`stop-handoff.json:1-67`).] The counts are false on all seven (`formula.counts`). `first_omega_0` is 30 for the first three arms and 60, 120, 240, 480 for the sweep. Every `h` is `[[0.01, 0.0], [0.1, 0.0]]`.

### The time-constant evidence (new, re-derived on the CPU in float64)

| System | Constant "each body's time-mean position" predictor, frozen scorer error | Official trained `E` | Trained net's time variation ÷ orbit's (14 states) | RMS error ÷ RMS orbit deviation |
|---|---|---|---|---|
| 1632 and its four sweep arms | 1.1538 | 1.1574 (r1-1632) | 0.0030 to 0.0034 | 0.9999 to 1.0001 |
| 851 | 1.2337 | 1.2375 | 0.0031 to 0.0032 | 1.00004 to 1.0001 |
| 4658 | 1.1396 | 1.1432 | 0.0031 to 0.0032 | 0.99996 to 0.99999 |

[VERIFIED: scratch prototype, 5.0 s for all seven arms and both states, CPU float64, `attestation.test_split_opened` 0, validation opens 0. The constant predictor's `E` equals the Phase 60 verifier's figures 1.1538, 1.2337 and 1.1396, and the trained net is about 0.004 worse.] A ratio of 1.0000 means the network's error equals the error of predicting the average, which also implies its constant is within about 0.6% of the orbit's RMS spread of each body's true mean. Define each ratio in the verdict (time variation: RMS deviation of the output about its own time mean, over the same for the real orbit, over all three bodies and three coordinates).

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Python (`pinn-train` env) | 3.11.15 | all scripts | The interpreter recorded in every arm record (`versions.python`); `<home>/miniforge3/envs/pinn-train/bin/python` |
| numpy | 2.4.6 | error series, hashing of rounded arrays | recorded `versions.numpy` |
| torch (CPU) | 2.12.1 | `torch.load(..., weights_only=True)`, float64 forward and autograd velocities | recorded `versions.torch`; MPS is not needed |
| Python stdlib | 3.11 | `json`, `hashlib`, `re`, `argparse`, `subprocess` (git), `importlib.util`, `unittest`, `pathlib` | repo precedent for every verifier |
| Repo modules, imported read-only | pinned | `pinn.verification.feasibility_scorecard` (`load_scorecard`, `decision_verdict`, `g2_fires`, `counts`), `feasibility_scorer` (`network_trajectory`, `position_errors`, `tier_defining_error`, `valid_horizon`), `learnability_arms` (`arm_spec`, `EVIDENCE_REL`, `SEED`), `learnability_data` (`open_real_context`, `load_arm_data`), `learnability_run._float32_rounded`, `pinn.network` (`ArchitectureSpec`, `build_network`), `diagnostic_architecture.build_network_with_first_omega` | These are the pinned objects that produced the records; no re-implementation |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| Pillow | 12.3.0 (FreeType present) | optional PNG twin of the figure | only if an SVG is not acceptable; not needed |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| stdlib SVG writer | matplotlib | Not installed anywhere on this Mac. Installing needs the owner's permission (`CLAUDE.md`: ask before adding dependencies) and adds a one-off dependency for one figure |
| stdlib SVG | Pillow PNG | Raster, version-dependent bytes; usable if the owner cannot open SVG |
| Importing the Phase 60 verifier's helpers | local copies of `sha256_file`, `load_json`, `fail` | Phases 59 and 60 each re-implemented them; either is acceptable; keep the Phase 64 verifier independent of the producer |

**Installation:** none. This phase adds no package. Versions are those pinned in the environment and recorded in every arm record, not looked up on PyPI (the Bash sandbox has no network).

## Package Legitimacy Audit

No external package is installed by this phase.

| Package | Registry | Age | Downloads | Source Repo | Verdict | Disposition |
|---------|----------|-----|-----------|-------------|---------|-------------|
| Pillow 12.3.0 | PyPI | already installed in `pinn-train` | n/a | n/a | not run (no install) | Optional use only; discovered by `pip list` in the environment, not recommended for installation |
| matplotlib | PyPI | not installed | n/a | n/a | not run | NOT recommended. Absent by design; installing needs the owner's approval and is unnecessary |

**Packages removed due to [SLOP] verdict:** none. **Packages flagged [SUS]:** none. If a later plan decides to install anything, it must gate that behind a `checkpoint:human-verify` task and the legitimacy check.

## Architecture Patterns

### System Architecture Diagram

```
 committed evidence (sealed, read-only)                      external, untracked
 +-----------------------------------+                       +--------------------------+
 | P60/g2/stop-handoff.json (single  |                       | simulation_data/Data     |
 |   input) -> g2-outcome, sweep,    |                       | (train split only, via   |
 |   skip-records                    |                       |  the Phase 59 allowlist) |
 | P60/arms/*/record.json + weights  |                       +------------+-------------+
 | P59 baselines, survey, census     |                                    |
 | amendments doc, REQUIREMENTS,     |                                    v
 |   ROADMAP, PROJECT, run status    |         +------------------------------------------+
 +----------------+------------------+         | derive (CPU float64, torch.load weights_ |
                  |                            | only): E, e(0), best moment, counts<=0.1, |
                  |                            | constant-predictor E, time-variation,     |
                  |                            | RMS ratios; series for the figure         |
                  |                            +--------------------+---------------------+
                  v                                                 v
 +-------------------------------+            +-----------------------------------------+
 | numbers.json: every quoted    |<-----------| figure-1632.svg + provenance.json       |
 | number, source key, derivation|            | (SHA-256 of inputs and of the SVG)       |
 +---------------+---------------+            +--------------------+--------------------+
                 |                                                  |
                 v                                                  v
 +--------------------------------------------------------------------------------+
 | 64-VERDICT.md  (plain language first; label + side-by-side box; tables; figure)|
 | 64-CHARTER.md  (one page, pre-filled; options; owner column; appendices)       |
 +----------------------------------+---------------------------------------------+
                                    |
              verify_phase64_verdict.py: inputs | numbers | derive | figure | rules |
                          frozen | charter | traceability   (all green before the checkpoint)
                                    |
                                    v
                  OWNER CHECKPOINT ①  (blocking; continue / change course / stop;
                  approve or edit each charter line; GAP-59-08; the 10^-5 bar)
                                    |
                      owner's words verbatim  ->  64-CHECKPOINT-1-RULING.md
                                    |
          apply only what is approved: PROJECT.md rewrite, requirement dispositions,
          REQUIREMENTS/ROADMAP/STATE hand edits  ->  verifier ruling | traceability | final
```

### Recommended Project Structure

```
.planning/phases/64-feasibility-verdict/
├── 64-CONTEXT.md, 64-RESEARCH.md, 64-VALIDATION.md, 64-NN-PLAN.md   (GSD)
├── 64-VERDICT.md                  # FEAS-06
├── 64-CHARTER.md                  # FEAS-10, one page plus appendices
├── 64-CHECKPOINT-1-RULING.md      # written only after the owner answers
└── evidence/
    ├── build_phase64_evidence.py  # producer: numbers.json, the figure, provenance
    ├── verify_phase64_verdict.py  # independent verifier (modes below)
    ├── numbers.json
    ├── figure-1632.svg
    └── figure-1632.provenance.json
tests/phase64/{__init__.py, test_verifier_phase64.py}
```

File names are discretionary (CONTEXT). Keep the producer and the verifier separate and re-derive in the verifier from raw records, so it does not grade its own homework (the Phase 60 verifier is "independent of the runner").

### Suggested plan decomposition (the planner may merge or split; assumption A8)

| Plan | Wave | Autonomous | Content | Needs data root |
|------|------|-----------|---------|-----------------|
| 64-01 | 1 | yes | Verifier skeleton and the committed-JSON modes (`inputs`, `numbers`, `rules`, `frozen`, `traceability`), `tests/phase64/`, each mode smoke-run on the real files first | no |
| 64-02 | 2 (same verifier file, so after 64-01) | yes | `derive` and `figure` modes, the builder, `numbers.json`, the SVG and its provenance; run the builder twice in separate processes and require one SHA-256; render the SVG and look at it | yes |
| 64-03 | 3 | yes | `64-VERDICT.md` from `numbers.json` and the figure; `numbers`, `rules`, `inputs` green | no |
| 64-04 | 3 (different file from 64-03) | yes | `64-CHARTER.md`: the pre-filled page, the appendices (options, GAP-59-08, the draft `PROJECT.md` text, the routed lines); `charter` green | no |
| 64-05 | 4 | no | Pre-checkpoint gate (every mode green, drafts committed), then the blocking `checkpoint:decision`, then `64-CHECKPOINT-1-RULING.md` written from the owner's words; `ruling` green | no |
| 64-06 | 5 | yes | Apply only what the owner approved (the `PROJECT.md` rewrite, any requirement dispositions); tick FEAS-06, FEAS-10, VER-22; hand-edit ROADMAP and STATE and diff; `traceability` last; `final`; SUMMARY. Leave `/gsd-complete-milestone` and the merge to the owner | no |

If the owner does not answer at once, only 64-05 holds; 64-01 to 64-04 complete on their own. While checkpoint ① is unanswered the phase does not close (the 60-17 rule).

### Pattern 1: Number manifest with an independent re-derivation
**What:** every number the documents quote has an ID, a value, a source file and key, and a derivation. The producer writes `numbers.json`; the verifier recomputes each from raw committed files and requires the rendered token to appear in the verdict.
**When to use:** all headline numbers, the per-arm table, the cost table, the comparison-point cells.
**Example:** Code Examples 1 to 3.

### Pattern 2: Sealed-input gate
**What:** prove no frozen path changed since the phase base `1ebb1d9b`, and that the Phase 60 and Phase 59 evidence still verify, using the cheap modes only.
**Example:** Code Example 4, plus `verify_phase60_evidence.py final` (1.3 s) and Phase 59 `scorecard-frozen`, `guardrails`, `manifest --area <a> --require-committed`.

### Pattern 3: Owner checkpoint with a verbatim record (the repo's own form)
**What:** plan 60-17 is the template. `autonomous: false`; a `checkpoint:decision gate="blocking-human"` task with `<decision>`, `<context>`, `<options>` and `<resume-signal>`; the owner's message is stored byte for byte in a fence whose info string is `owner-quote` (a fence longer than any backtick or tilde run inside the message); "If the message does not unambiguously choose one option ... ask again; never infer an answer"; the ruling file has front matter (phase, milestone, created, status, authority), an "Authority and boundary" section, and is committed with a body quoting the owner. [VERIFIED: `.planning/phases/60-single-system-learnability/60-17-PLAN.md` Task 2 and Task 3; `pinn/verification/learnability_ruling.py:1-30` docstring.]
**Precedent for the verdict file:** `58-VERDICT.md` and `43-VERDICT.md` (front matter `schema_version`, `status: owner-signed`, `owner_decision`, `owner_decision_date`; sections "Decision boundary", "Evidence matrix", "Requirement dispositions", "Routing of the next milestone", "Owner sign-off"). Phase 64 needs no machine-read block unless a verifier parses it; a `phase64-ruling` block would be a new schema, so do not add one without a reader.

### Pattern 4: Real-path smoke before any test
**What:** run each new verifier mode read-only on the real committed files before writing its tests. Test with the real types: the real frozen `DataContext` dataclass (not a context manager), NumPy `ArmData` arrays (not tensors), real JSON records. Phase 60's verifier crashed on first real use twice because tests mocked the wrong shapes. The derivation path in Code Example 1 has already been smoke-run (3 s for one arm, 5 s for seven).
**Add a mutant check:** reintroduce the bug and confirm the test fails.

### Pattern 5: One lazy-import verifier
**What:** keep `torch` and `pinn` imports inside `derive` and `figure`, so `inputs`, `numbers`, `rules`, `frozen`, `charter` and `traceability` run in about 0.1 s with no data root. Phase 60's verifier imports torch at the top (about 1 s). Call `open_real_context` once per process (it installs a process-wide open attestation).

### Anti-Patterns to Avoid
- **Hand-copying numbers into prose.** Phase 60's own scratch observation is the cautionary case: it lives only in an uncommitted scratchpad. Derive, then quote.
- **Recomputing the label by hand or amending it.** Re-run the frozen function and compare; never edit a pre-registered output.
- **Filling the sealed handoff's `owner_answer` or `verdict_note`.** They are `null` by design; the handoff is a hashed input.
- **Ranking the candidate fixes** (D-03). List design and recipe candidates unranked.
- **Quoting CPU numbers as official or the reverse.**
- **Any GPU price, speed-up, tripwire or rental route** (D-06), including in negative form beyond the owner's fenced quotes.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Position error, valid horizon, tier | your own error formulas | `position_errors`, `tier_defining_error`, `valid_horizon`, `tier_of` from the frozen scorer | The records were scored by these; a re-implementation can disagree in the last digit and would not be the pre-registered measure |
| The pre-registered label | a hand-written rule | `decision_verdict` with `g2_fired` from `g2_fires` | Verified equal to the handoff this session |
| Loading committed weights and the real reference orbit | a new reader | `open_real_context`, `load_arm_data`, `torch.load(weights_only=True)`, `build_network` or `build_network_with_first_omega` (the `rescore` path) | The allowlist keeps test-split files unopened and counts every open |
| File hashing, tracked-and-clean checks | ad hoc | `hashlib.sha256` on bytes; `git ls-files --error-unmatch`, `git diff --quiet`, `git status --porcelain -- <path>` | The Phase 59 and 60 verifiers use exactly these |
| A line chart | a plotting library install | a 60-line stdlib SVG writer (Code Example 5) | matplotlib is absent; one figure does not justify a dependency |
| The owner's decision text | a paraphrase | the `owner-quote` fence | A paraphrase of a governing decision is the T-60-04 and T-60-20 threat |
| Registry counts | `gsd-tools` mutating verbs | the `traceability` mode (Code Example 3) plus hand edits | The verbs corrupt STATE and ROADMAP here |

**Key insight:** every discrete value in this phase already exists in a sealed file with a hash. The work is to cite and re-derive, never to restate from memory.

## Cost inputs (D-05, D-06)

All of these are Mac-only and measured. Nothing here is a projection from the flat curves.

| Quantity | Value | Source |
|---|---|---|
| Machine: Apple M5 Pro, 24 GiB, 15 logical CPUs (5 performance, 10 efficiency), macOS 26.5.1, torch MPS available | verified this session with `sysctl` and torch | `PROJECT.md:368` (Hardware); records `versions.macos` `26.5.1`. The trainex-r1 design says "16 cores" (`docs/work/designs/cross_cutting/training-execution/2026-06-10-training-execution-design.md:59`); use the PROJECT.md and `sysctl` figure, 15 |
| Arm wall time, six arms | 2.573 to 3.046 h each | `stop-handoff.json` `arms[*].wall_hours` |
| Arm wall time, the arm that earned its one doubling | 5.693 h (`r1-4658`) | same |
| Total Phase 60 arm time | 22.378 h: Rung 1 11.108 h, sweep 11.270 h | `stop-handoff.json:83` |
| Calendar | Rung 1: 2026-10-21 21:29 to 2026-10-22 08:35 CDT; sweep: 2026-10-22 12:01 to 23:18 CDT; each in one launch with no pause or stop | `STATE.md` "Decisions from 60-14" and "60-15"; records `launch.invocations` 1, `launch.stops` `[]` |
| Timed seconds per step, data-only single orbit | 0.010856 to 0.013596 | `stop-handoff.json` `arms[*].seconds_per_step` |
| Sustained seconds per step (Adam seconds over steps) | 0.01042 to 0.01164 | records `wall.adam_seconds` over `budget` steps (re-derived) |
| Total Adam steps in the seven arms | 7,437,225 | records, with `r1-4658` at 1,961,246 (re-derived) |
| Timing runs themselves | 5.4 to 6.8 s each, 41.2 s in all, outside the arm totals | records `timing.wall_seconds` |
| Polish | 4.4 to 5.4 s per arm | records `wall.polish_seconds` |
| This phase's own compute | CPU float64 re-score of all seven arms, both states, 5.0 s | prototype, this session |
| Generation 7 (non-conformant physics step) | 12.3178 s per step (EMA at step 951), `"state": "failed"` | `runs/stage0-v23g7-seed42/status.json:21-26` |
| Harness physics step on the CPU (oracle test) | about 29 s for a production-shape step | `STATE.md` "Decisions from 60-05" |
| No harness physics arm was ever timed on the corrected path | no Rung 2, probe or control ran | `skip-records.json` |

**For scale only (label it so).** 200,000 Adam steps at 12.3178 s is 2,463,563 s: 684.3 h, 28.5 days of nonstop computing; at 300,000 steps, 42.8 days. The 2026 study reports 2 to 3 × 10⁵ Adam epochs plus 1.5 × 10⁴ L-BFGS epochs for one forward orbit, with 3 to 5 layer, 64 to 128 neuron networks in float64 and 64 collocation points [CITED: arxiv.org/pdf/2607.23501v1, Section 3.1 and Table 1]. Ours is 12 layers of 256 (795,657 parameters) with 4,096 collocation rows per step, and our target is a family of orbits, so the multiplication is an order-of-magnitude illustration and not a forecast. The 1,000-step control would be 3.42 h per seed at the generation-7 rate (about 10.3 h for three seeds), unmeasured on corrected code.

**Derived consequences the verdict may state, each labelled "unmeasured on the harness":** the frozen budget rule caps a single-system arm at 3 hours (`budget_rule.cap_hours_single_system` 3.0 in the scorecard), so at 12.3 s per step a physics arm would get about 877 Adam steps in the cap, against 0.8 to 2.0 million for a data-only arm (a ratio of about 900 to 1,100 in step time). What would measure it: the harness's own 50-step physics timing run (`timing.physics_steps` 50 in `run-protocol.json`). That is a future action; Phase 64 trains nothing, so it must only name it.

**Not measured, so say so:** Phase 59's read-only compute (census, survey, baselines, checkpoint experiments) was not itemised as machine hours; Phase 60's launcher clock times are not process accounting. Do not estimate them. The skipped ladder's budget under the pre-registered caps (SCOPE-44: sweep about 15 h, probes about 12 h; Rung 3 capped at 8 h; control 1,000 steps per seed) is available as a reference for what was budgeted but never run, and is Mac-only; plan 60-17 estimated about 41 h for the continue path (Rung 1 on 4658 about 3.75 h, Rung 2 about 22.5 h, four probe arms about 15 h).

**A costed first step for v2.5** should be assembled from these primitives and not invented: the trainex-r5 round itself is research (the ERW runbook's Route B), with near-zero compute; any short diagnostic arm it commissions costs the per-step rate times its steps (for example, a data-only arm at 10⁵ steps is about 0.3 h at 0.011 s per step). Give it as an example of how to read the table, not a plan.

## Comparison points (first primary-source read in this repo)

[CITED: arxiv.org/abs/1910.07291v1, arxiv.org/pdf/1910.07291v1, read via excerpts, MEDIUM]

- **Breen, Foley, Boekholt, Portegies Zwart, "Newton vs the machine: solving the chaotic three-body problem using deep neural networks" (arXiv:1910.07291, submitted 16 Oct 2019; MNRAS 2020, doi 10.1093/mnras/staa713).**
  - A supervised deep network trained on solutions from Brutus, an arbitrary-precision N-body integrator (the same integrator family this project's data comes from). No physics term. Not a PINN.
  - The training set is restricted to "three equal mass particles with zero initial velocity, located in a plane".
  - Trajectories matched with MAE at most 0.1. Relative energy error "of order 10⁻²", spiking to 10¹ at close encounters; a projection layer onto a nearby energy surface brings it to order 10⁻⁵. A second network produced the velocities. About 10⁵ times (sometimes 10⁸) faster than Brutus; the abstract says "up to 100 million times".
- **Kollias and Matzakos, "Physics-Informed Neural Networks for Discovering Periodic Orbits in the Gravitational Three-Body Problem" (arXiv:2607.23501, submitted 26 Jul 2026, cs.LG, 39 pages)** [CITED: arxiv.org/abs/2607.23501v1, arxiv.org/pdf/2607.23501v1, MEDIUM].
  - PINNs that recover periodic orbits from sparse noisy observations without initial conditions, including families absent from the training data (23 to 25% of runs in two 100-seed ensembles).
  - Forward problems (Euler, Lagrange, figure-eight): 3 to 5 layer, 64 to 128 neuron networks, float64, Adam (η = 10⁻⁴, 2 to 3 × 10⁵ epochs) then L-BFGS (1.5 × 10⁴ epochs). Energy conserved "to within ∼ 0.02–3% over one orbital period": Euler 7.74 × 10⁻⁴, Lagrange 3.23 × 10⁻², figure-eight 1.64 × 10⁻⁴ (Table 12).
  - These are separate networks per orbit or run. I saw no experiment in the excerpts in which one network is conditioned on a family of initial conditions.
- **Not required by FEAS-06, found by this research:** Pereira et al., "Advancing Solutions for the Three-Body Problem Through Physics-Informed Neural Networks" (arXiv:2503.04585, submitted 6 Mar 2025, cs.LG, IAC-24). A PINN approach to the three-body problem; its abstract says PINNs "surpass current state-of-the-art machine learning methods with comparable prediction quality"; a search summary describes its data as the same restricted case (three unit masses, zero initial velocity) [CITED: arxiv.org/abs/2503.04585 for the abstract; the restricted-case scope is [ASSUMED] from a search summary and not read in full].

**How to scope the proof-of-concept claim accurately.** Neither source did what this project attempts: one network, 14 inputs (time plus 13 initial-condition values), a 12 × 256 network, a physics-informed curriculum loss, and seven stages of increasing chaos. Breen et al. is supervised, on a very restricted family (the amendment counts 2 free parameters against 13 here [CITED: amendments `:239`; not checked in the paper]); the 2026 study is per orbit. Their metrics are not this scorecard's (MAE and energy drift, against the worst error over the whole window as a fraction of system size), so any numeric comparison is indicative only. That PINN three-body papers exist (two found here) means the owner's belief that few have done it is plausible but unverified; the project made no literature survey. Recommend one sentence: "no novelty claim is made". The 2026 study's energy range should be quoted as about 0.02 to 3%, correcting the amendment.

## Charter inputs (FEAS-10, D-07 to D-13)

**Design the page for the owner's effort.** The owner asked "why are you even asking all this?" and said the Mac-only rule was settled "a LONG TIME AGO" (`64-DISCUSSION-LOG.md`). So the page must not re-ask the purpose, the compute location or the v2.5 default (D-07, D-06, D-14). Use a pre-filled table with item IDs (C-1 and so on), a recommended answer in each row, short options, and an empty "Owner" column, so the owner can reply "approve all except C-4: ...". Keep the decision page to about 60 lines between two markers (`<!-- page:begin -->` and `<!-- page:end -->`) and put options, evidence and the draft `PROJECT.md` text in appendices. Define each term once; reuse the plain wording of `60-FINDINGS.md` "In plain language".

**Anchors for the Stage-0 bar** (all measured or cited):

| Anchor | Value | Source |
|---|---|---|
| Two-Kepler formula, no learning | median `E` 0.989 (train), 0.940 (validation); Tier 1 on 1 of 1812 and 0 of 227 | `P59/baselines/baselines.json` |
| Nearest-neighbour copy | median `E` 2.135 on validation; Tier 1 on 0 of 227 | same |
| Constant "average position" predictor | `E` 1.14 to 1.23 on the three panel systems | this phase's `derive` |
| Trained network under the recipe | `E` 1.14 to 1.24, no arm at Tier 1 | records |
| Scorecard tiers | Tier 1: `E` at most 0.1, no energy test; Tier 2: `E` at most 0.01 and `ε_H` at most 10⁻³; Tier 3: `E` at most 0.01 and `ε_H` at most 10⁻⁵ | `feasibility_scorecard_v1.json:613-634` |
| Frozen decision-rule proportions | Rung 2b on at least 2 of 3; Rung 3 on at least 12 of 16 (75%) | `feasibility_scorecard_v1.json:54-72` |
| Published energy levels | Breen about 10⁻² typical (10⁻⁵ after projection); 2026 study about 0.02 to 3% | the two papers |
| How hard Stage 0 is | median 18.61 inner laps; to keep the end-of-window miss under 10% the lap timing must be right to about 1 part in 1,169 | `59-FINDINGS.md:38-47` |
| The spec's own stated aim | "relative energy error staying below 0.1% over very long times" (`ctl_instruction.md:2057-2058`), which is `10⁻³`, but the text is aspirational and is not evidence | read this session |

**Proposed Stage-0 bar (a proposal for the owner, not a decision; tag it so on the page).** Position: the scorecard's counting rule extended to the copy (Tier 1, that is `E` at most 0.1, and strictly below both the formula's and the copy's `E`) on at least 75% of Stage-0 validation-panel systems, mirroring the frozen 12-of-16 proportion. A softer alternative the owner may prefer for a proof of concept: a valid-horizon fraction `h` at 10% of at least 0.5 (the scorecard already reports `h`). Energy: `ε_H` at most `10⁻²` computed from autograd velocities (the level of the raw published networks), conditional on GAP-59-08 option A; Tier 2 (`10⁻³`) as the stretch; Tier 3 (`10⁻⁵`) kept as the long-run aspiration and not the Stage-0 pass bar. Every number is [ASSUMED] until the owner approves it. Stages 1 to 6 are listed as open, with two cautions the survey records: Stage 3 is empty in the survey, and the official stage mapping beyond Stages 0 and 1 is owner-pending (`59-FINDINGS.md:106`, `:119`, `:127`).

**GAP-59-08, as the owner will see it** [VERIFIED: `.planning/phases/59-read-only-baseline-scorecard/59-GAPS.md:281-333`]. The validation gate and held-out evaluator compute `ε_H` from finite-difference velocities on the coarse output grid; on that grid the exact Brutus answer already scores 4.7e-2, 2.1e-1 and 3.8e-1 on systems 1632, 851 and 4658 (5 to 38%), against about 1e-14 with true velocities, so "no model, not even a perfect one, can pass the `1e-5` bar on this data". Options, verbatim in substance: **A** the evaluator and validation gate use the network's autograd velocities, by a formal clarifying amendment to §10.6 (the recommendation; it matches the v2.4 scorecard); **B** keep finite differences on a dense grid (likely still above `1e-5` for the fastest binaries, so probably unpassable); **C** keep the gate as is, knowing it cannot pass. It blocks any spend of the held-out evaluation and the FEAS-10 pass-bar choice, and nothing else in v2.4. Phase 64 records the answer and routes the amendment; it does not edit `pinn_architecture.md` (SCOPE-43).

**The `10⁻⁵` bar.** Recommendation per D-09: replace it by formal amendment with an evidence-based bar, following the owner's recorded lean (amendments `:235`). The `10⁻⁵` text lives at `pinn_architecture.md:1087`. A formal amendment is not performed in Phase 64 (REQUIREMENTS "Out of Scope": "The owner decides in the charter at the verdict (FEAS-10), by formal amendment. v2.4 only measures the distance to it."); route it with the `ctl_instruction.md` rewrite to the milestone that sets the bars.

**Routed items (D-13), verbatim anchors.** `ctl_instruction.md:2057` "In our results, the final model shows minimal energy drift (e.g.,"; `:2081` "much sooner than it should. In testing our model, we found that it can"; `:2111` "our case, after the final active learning fine-tuning, the model passes". [VERIFIED: read this session.] No such results exist; the text is aspirational and is not evidence that the approach works (amendments `:276-282`). Record, route, do not edit (SCOPE-43). `PROJECT.md` still opens "# Three-Body Physics-Informed LLM" with "What This Is" (`:3-5`) and Core Value (`:7-9`) describing an LLM project. FEAS-10 names only those two sections; the title line, the Model constraint ("Qwen 3.5 2B 4-bit", `:369`) and Context bullets stay LLM-flavoured after the rewrite. Offer that as one extra pre-filled line for the owner rather than editing unasked.

**Budget (D-11).** The unit is months of computing on this Mac. Give measured anchors (Cost inputs), not a projection. Useful facts: the Mac leaves the charger for classes from about 09:00 daily, so usable computing is mostly overnight (user memory); two overnight-length sessions of 11.1 h and 11.3 h ran with no pause. Option shape: per-milestone budgets re-set by the owner at each verdict. For example A, about one month for diagnosis plus one Stage-0 attempt (recommended, a proposal); B, three months; C, six months. Say that at 12.3 s per step a 200,000-step orbit-equivalent is about 28.5 days nonstop, so B or C is needed for any physics-heavy Stage-0 production attempt. Label all of this as options and a proposal. No GPU wording anywhere outside the fenced owner quotes.

**Stop rule (D-12).** Draft text: "a milestone that neither climbs a ladder level nor beats the best fixed-scorecard result means stop or change approach, with no third attempt at the same idea." State the baseline: the project is at Level 1, and the best fixed-scorecard result is the official `E` 1.1432 (4658) and `ε_H` 123.62, which a constant predictor nearly matches. The rule's "beats" needs an operational definition, or a milestone could "beat" the baseline by 0.01 with no real progress. Offer options (reaching Tier 1 on any panel system; or lowering `E` below the constant predictor's by a stated margin) with a recommended default, and leave the margin to the owner (Open Question 2).

**Recommended continue-or-not line.** D-14 records the agent's recommendation of 2026-10-24 that the owner proceeded on. The verdict can offer three options with consequences, recommending "change course": v2.5 begins with the diagnosis round and no new long training run until it says why every network is time-constant. Label it a recommendation; the owner decides.

## VER-22 mechanics

**Precedent (VER-21, v2.3).** [VERIFIED: `.planning/phases/58-verdict-traceability-close/58-SUMMARY.md:43-64`] "The check compared every `- [ ] **ID**` definition in `REQUIREMENTS.md` with each Phase 53–58 `**Requirements**:` line in `ROADMAP.md` and with the traceability table: 15 defined, 15 mapped, no duplicates, no orphans, and the table agreed with the roadmap." And the lesson: "a passing coverage count shows there are no *orphans*, not that there are no *gaps*. VER-21 certifies mapping completeness, not requirement satisfaction."

**Current counts** [VERIFIED: prototype this session over `REQUIREMENTS.md` and `ROADMAP.md`]: 24 definitions in "## v2.4 Requirements" (9 ticked); 24 rows in the Traceability table; 24 unique IDs across the six per-phase `**Requirements**:` lines (Phase 59: 5; 60: 4; 61: 8; 62: 2; 63: 2; 64: 3); no duplicates; the table equals the roadmap; the REQUIREMENTS header says "Total: 24 requirements (10 FEAS + 2 DIAG + 3 INST + 2 CONF + 4 SPEC + 1 GATE + 1 RUN + 1 VER)" and the Coverage block says "24 total, Mapped 24, Unmapped 0". The count also appears in `ROADMAP.md:29`, `:67`, `:413-414` and `PROJECT.md:340` ("24 requirements"); check them all. Two of those lines also carry the creation-time history ("20/20 mapped at roadmap creation", `ROADMAP.md:67` and `:413`); the check must assert the current 24 and not flag that history.

**Do it last, after every registry edit,** against the final text (REQUIREMENTS statuses, the ticks for FEAS-06, FEAS-10 and VER-22 once the owner's decision is recorded, the ROADMAP Phase 64 line and Progress row). The `traceability` mode should also print the per-phase counts and the status vocabulary found (Pending 15, Complete 7, "Complete (recorded as skipped: no rescue)" 2 today).

**The 12 requirements of the skipped phases** (CONF-10, CONF-11, INST-06, INST-07, SPEC-07 to SPEC-10 under Phase 61; GATE-05, FEAS-05 under Phase 62; RUN-06, DIAG-08 under Phase 63) remain "Pending". The v2.3 close recorded owner-decided dispositions ("Closed incomplete", "Not attempted") beside VER-21; the v2.4 sources are silent on how to label these 12 at close. Do not decide it in the plan; see Open Question 1.

## Decision coverage map (D-01 to D-14)

For the plan-checker's decision-coverage pass (the automated gate may mis-parse this repo's CONTEXT format).

| Decision | Where it lands | Mechanical check |
|---|---|---|
| D-01 | `64-VERDICT.md`: the headline states `RETHINK-REPRESENTATION` and "G2 fired and the sweep rescued nothing"; beside it a plain box with four statements (the networks are time-constant predictors, with the re-derived numbers; the accuracy curves levelled off, with numbers; the sweep varied only `first_omega_0`; design versus recipe is still open). The label is not amended | `rules`: exact label string and box present; the proposal's gloss "no change to the training recipe can fix it" absent |
| D-02 | one plain sentence that `representation_limit_qualifier: false` means "not evaluated on this branch", not "the condition failed"; the field reported as recorded | `rules`: field name and sentence present; `inputs`: field equals the handoff |
| D-03 | an unranked bullet list: the four pre-registered design changes and the four recipe suspects | `rules`: all eight named; a bullet list, not a numbered one |
| D-04 | the figure and its provenance beside the verdict | `figure` |
| D-05 | cost tables: measured per rung and per arm, one for-scale line labelled as such, every assumption listed, no projection from the curves | `numbers`, `rules` |
| D-06 | no GPU, cloud, price, speed-up or tripwire wording; the owner's two statements verbatim in `owner-quote` fences under the charter's budget item | `rules`, `charter` (byte-equal to CONTEXT) |
| D-07 | the purpose recorded verbatim; definition of done and bars drafted from it | `charter` |
| D-08 | a pre-filled table with item IDs, a recommended answer, short options and an Owner column; open items recorded as open | `charter` |
| D-09 | a Stage-0 proposed bar (position and energy, fixed before any held-out exam), Stages 1 to 6 listed as open, the `10⁻⁵` recommendation | `charter` |
| D-10 | GAP-59-08 options A, B, C beside the bars; every energy bar written as conditional on the answer | `charter` |
| D-11 | budget options and a recommendation, with the measured per-experiment cost | `charter`, `numbers` |
| D-12 | the stop-rule text verbatim, with its baseline stated | `charter` |
| D-13 | the three `ctl_instruction.md` lines recorded and routed (not edited); the `PROJECT.md` rewrite drafted and applied only on approval | `charter`, `ruling` |
| D-14 | v2.5, first phase the trainex-r5 round (open-book Route B, diagnosis first); nothing else committed | `rules` |

## Common Pitfalls

### Pitfall 1: Treating `trace` as along-window evidence
**What goes wrong:** the verdict says "the curves show where it broke". **Why:** the brief says the `trace` lists carry it. **Avoid:** use `result.h` and the re-derivation (Finding 1). **Warning sign:** a sentence that cites `trace` for position along the window.

### Pitfall 2: Mixing MPS and CPU numbers
**What goes wrong:** `1.1574` and `1.1600` appear for the same state. **Avoid:** quote official numbers from the records; use CPU numbers only for the new claims; label each; the verifier checks CPU `E` equals `cross_check.E` to 1e-12 and does not compare it to the official `E`.

### Pitfall 3: Repeating the proposal's "no change to the training recipe can fix it"
**What goes wrong:** the verdict overclaims what a one-setting, one-system sweep tested. **Avoid:** D-01's side-by-side box; state that the sweep varied only `first_omega_0` (60, 120, 240, 480 beside the locked 30) on system 1632.

### Pitfall 4: "Flat" accuracy curves
**What goes wrong:** the curves are not flat; `E` fell 25- to 50-fold in the first 5% of training (35.6 to 76.7 down to 1.3 to 1.6) and 12 to 29% more from the first reading to the end. **Avoid:** say "levelled off at 1.14 to 1.24, about 11 to 12 times the Tier-1 limit", with the numbers.

### Pitfall 5: Reading `ε_H` as accuracy
**What goes wrong:** a near-constant predictor has near-zero velocity, so its energy can look anything. The recorded `ε_H` spans 1.0 to 13,127 across arms whose positions are all equally wrong. **Avoid:** the charter's "never energy alone" rule, and one plain sentence in the verdict.

### Pitfall 6: Comparing the nearest-neighbour copy to Rung 1
**What goes wrong:** the copy was scored on the 227 validation systems; Rung 1 was trained and scored on three training systems. **Avoid:** show the copy's validation-panel median only, labelled, and say the populations differ.

### Pitfall 7: GPU or cloud wording
**What goes wrong:** the superseded amendment text slips in. **Avoid:** the `rules` guard (Code Example 6): no rented, cloud, price, speed-up or tripwire wording outside fenced owner quotes. "This Mac's GPU (MPS)" is legitimate and passes (it appears in `60-FINDINGS.md`).

### Pitfall 8: Running from the wrong directory
**What goes wrong:** `open_real_context` fails with `git rev-parse --git-common-dir` exit 128. **Avoid:** `os.chdir(REPO_ROOT)` at the start of data-dependent modes, and run from the repository root.

### Pitfall 9: Absolute paths in committed evidence
**What goes wrong:** `<home>/...` lands in the provenance JSON. **Avoid:** repo-relative paths only; record `data_root_source` (`"git_common_dir_default"`), never the root (Phase 59 README: "Do not paste a host path into a committed evidence file"). The `rules` mode scans new committed files for `/Users/`.

### Pitfall 10: Editing a pinned or sealed path
**What goes wrong:** one edit to any of 33 pinned files makes `PROTOCOL-FAIL`. **Avoid:** Phase 64 adds files only under `.planning/phases/64-feasibility-verdict/`, `tests/phase64/` and the registries; the `frozen` mode and the Phase 60 verifier prove it.

### Pitfall 11: A figure that fits the plot but not the legend
**What goes wrong:** my first prototype put the legend below the canvas; only rendering it showed that. **Avoid:** render and look (Code Example 5 note); the predicted tracks are tiny, so label them or add a magnified inset.

### Pitfall 12: Non-deterministic figure bytes
**What goes wrong:** the verifier cannot compare regenerated bytes. **Avoid:** `torch.set_num_threads(1)`, round pixel coordinates to 0.1, fixed element order; run the producer twice in separate processes and require the same SHA-256 (the prototype did).

### Pitfall 13: The zsh gate that cannot fail
**What goes wrong:** an unquoted multi-path variable in an `<automated>` block does not split under zsh, so a pathspec gate passes vacuously. **Avoid:** write the path list to a temp file, expand `$(cat "$T")`, assert the argument count, and run a negative control (Code Example 4 does).

### Pitfall 14: Inferring the owner's answer
**What goes wrong:** an ambiguous reply is read as approval. **Avoid:** if the message does not unambiguously settle an item, ask again for that item only. Items the owner does not address are recorded as open, not approved.

### Pitfall 15: Running the 13-minute suite for nothing
**What goes wrong:** `tests/phase60` discovery takes about 13 minutes (992 tests, 787.906 s at `2ca6a821`; the plan and `60-VALIDATION.md` say "under about 60 s", which is stale). **Avoid:** Phase 64 changes no `pinn/` code, so run the cheap set in "Validation Architecture"; if any `pinn/` file changes, say why and run it once, retaining the full log outside the repo.

### Pitfall 16: Stale registry counts
**What goes wrong:** VER-22 passes against a count that a later edit changed. **Avoid:** run it last; check every place the count appears (REQUIREMENTS `:5` and `:421-424`, ROADMAP `:29`, `:67` and `:413-414`, PROJECT `:340`).

## Code Examples

All verified read-only on 2026-10-25 from the repository root unless stated. `PY=<home>/miniforge3/envs/pinn-train/bin/python`.

### 1. CPU float64 re-derivation of the committed weights (3 s for one arm, 5 s for seven)
```python
# Mirrors verify_phase60_evidence.py:701-806 (cmd_rescore). Run from the repo root.
import json, sys
from collections import OrderedDict
from pathlib import Path
import numpy as np, torch

REPO_ROOT = Path.cwd()                       # default_data_root() shells out to git in the cwd
sys.path.insert(0, str(REPO_ROOT))
from pinn.network import ArchitectureSpec, build_network
from pinn.verification.diagnostic_architecture import build_network_with_first_omega
from pinn.verification.feasibility_scorecard import load_scorecard
from pinn.verification.feasibility_scorer import (
    network_trajectory, position_errors, tier_defining_error, valid_horizon)
from pinn.verification.learnability_arms import EVIDENCE_REL, SEED, arm_spec
from pinn.verification.learnability_data import load_arm_data, open_real_context
from pinn.verification.learnability_run import _float32_rounded

torch.set_num_threads(1)
card = load_scorecard()
ctx = open_real_context(repo_root=REPO_ROOT)   # ONCE per process; a plain frozen DataContext
arm = "r1-1632"
rec = json.loads((REPO_ROOT / EVIDENCE_REL / "arms" / arm / "record.json").read_text())
ad = load_arm_data(arm_spec(arm), ctx, scorecard=card, dtype=torch.float32, device="cpu")
state = rec["better_state"]                    # the arm's official state ("polish" for r1-1632)
w = torch.load(REPO_ROOT / EVIDENCE_REL / "arms" / arm / f"{state}.weights",
               map_location="cpu", weights_only=True)
om = float(rec["first_omega_0"])               # 30.0 for the locked arms; 60..480 for sweep arms
model = (build_network(ArchitectureSpec(seed=SEED), dtype=torch.float64, device="cpu")
         if abs(om - 30.0) < 1e-9 else
         build_network_with_first_omega(om, seed=SEED, dtype=torch.float64, device="cpu"))
model.load_state_dict(OrderedDict((k, v.detach().to("cpu").to(torch.float64)) for k, v in w.items()))
pos, vel = network_trajectory(model, _float32_rounded(ad.ic13), _float32_rounded(ad.masses),
                              ad.score.times, dtype=torch.float64, device=torch.device("cpu"))
ref = np.asarray(ad.score.positions)           # (1001, 3, 3), the gold grid, same frame
e_sys, e_in, _ = position_errors(pos, ref, ad.score.inner_pair)
err = np.maximum(e_sys, e_in)                  # err.max() equals states[state].cross_check.E
const = np.broadcast_to(ref.mean(axis=0, keepdims=True), ref.shape)   # each body's time-mean
cs, ci, _ = position_errors(const, ref, ad.score.inner_pair)
E_const = tier_defining_error(cs, ci)          # 1.153841 on system 1632
dev = lambda a: np.sqrt(((a - a.mean(axis=0)) ** 2).sum(axis=(1, 2)).mean())
ratio_timevar = dev(pos) / dev(ref)            # 0.0034 (adam) and 0.003345 (polish) on 1632
print(ctx.attestation.summary())               # test_split_opened 0; validation 0
```
Measured on `r1-1632`: `E` CPU 1.157053 (Adam) and 1.159997 (polish), both equal to `cross_check.E`; `e_sys(0)` 0.8066 and `e_in(0)` 0.9961 (polish); `min_t err` 0.8662; scored times within 0.1: 0 of 1001.

### 2. Confirm the pre-registered verdict from committed inputs
```python
from pinn.verification.feasibility_scorecard import load_scorecard, decision_verdict, g2_fires
card = load_scorecard()
H = json.load(open(P60 + "/g2/stop-handoff.json")); G = json.load(open(P60 + "/g2/g2-outcome.json"))
S = json.load(open(P60 + "/g2/sweep-curve.json"))
v = decision_verdict(g2_fired=g2_fires(G["tiers"], scorecard=card),
                     sweep_rescued=(S["outcome"] != "no_rescue"),
                     rung2b_counts=None, rung3_counts=None, control_branch=None,
                     rung1_beats_formula=None, scorecard=card)
assert v == H["verdict"]   # {'verdict': 'RETHINK-REPRESENTATION', 'representation_limit_qualifier': False,
                           #  'reasons': ['G2 fired and the sweep rescued nothing']}   -> verified True
```

### 3. VER-22 counts
```python
import re, collections
req = open(".planning/REQUIREMENTS.md", encoding="utf8").read()
sec = req[req.index("## v2.4 Requirements"):req.index("## Scope Boundaries")]
defs = [i for _, i in re.findall(r"^- \[( |x)\] \*\*([A-Z]+-\d+)\*\*", sec, flags=re.M)]
rows = re.findall(r"^\| ([A-Z]+-\d+) \| Phase (\d+) \| (.*?) \|$", req[req.index("## Traceability"):], flags=re.M)
rm = open(".planning/ROADMAP.md", encoding="utf8").read()
road = collections.defaultdict(list)
for s in re.split(r"^### Phase ", rm, flags=re.M)[1:]:
    m = re.match(r"(\d+):", s)
    r = re.search(r"^\*\*Requirements\*\*: (.*)$", s, flags=re.M)
    if m and r and 59 <= int(m.group(1)) <= 64:
        for i in re.findall(r"[A-Z]+-\d+", r.group(1)): road[i].append(int(m.group(1)))
table = collections.defaultdict(list)
for i, p, _ in rows: table[i].append(int(p))
assert len(defs) == len(set(defs)) == len(table) == len(road) == 24
assert dict(table) == dict(road) and all(len(v) == 1 for v in road.values())
```

### 4. Frozen-path gate that cannot pass vacuously (zsh-safe)
```bash
T=$(mktemp); printf '%s\n' <the 41 paths: 33 pinned + 8 sealed> > "$T"   # list built from run-protocol.json module_sha256 keys
COUNT=$(wc -l < "$T" | tr -d ' '); N=0; for p in $(cat "$T"); do N=$((N+1)); done
[ "$N" -eq "$COUNT" ] || exit 1                       # self-test: the list really split into $COUNT arguments
for p in $(cat "$T"); do [ -e "$p" ] || { echo MISSING "$p"; exit 1; }; done
test -z "$(git diff --name-only 1ebb1d9b HEAD -- $(cat "$T"))" || exit 1   # expect empty
# negative control: the same command over a path known to change must be non-empty
test -n "$(git diff --name-only HEAD~40 HEAD -- $(cat "$T") .planning/STATE.md)"
```
The 33 pinned paths are the keys of `module_sha256` at `P60/run-protocol.json:829-862`; the eight sealed are `run-protocol.json`, `60-RUN-PROTOCOL.md`, `P60/g2/{g2-outcome,sweep-curve,skip-records,stop-handoff}.json`, `P59/scorecard-freeze.json` and `59-SCORECARD.md`. Tested here: 41 paths, self-test passes, none missing, empty diff at `HEAD`, negative control non-empty.

### 5. A stdlib SVG polyline (no plotting library)
```python
def poly(xs, ys, color, width=2.0, dash=None):
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="{width}" '
            f'stroke-linejoin="round" stroke-linecap="round"{d}/>')
```
Prototype result: two panels (top-down real orbit with the network's near-stationary prediction; error against time with the 0.1 limit line), 105 KB, 3 s end to end, byte-identical SHA-256 across two separate process runs, rendered with macOS Quick Look (`qlmanage -t -s 1000 -o <dir> copy.svg`, using a copy with smaller `width` and `height` attributes because the thumbnail otherwise crops) and read as a PNG. Palette: the reference palette's slots 1 to 3 (blue `#2a78d6`, orange `#eb6834`, aqua `#1baf7a`), validated light mode with `node scripts/validate_palette.js ... --pairs all`: all checks PASS; one WARN (aqua contrast 2.74 : 1 below 3 : 1), which is relieved by visible legend labels plus the verdict's per-arm table as the table view. Text uses ink tokens, never the series colour; gridlines are solid hairlines. Pixel-space rounding to 0.1 and `torch.set_num_threads(1)` gave stable bytes.

### 6. The rented-GPU guard
```python
import re
FORBID = re.compile(r"\b(rent(?:ed|ing|al|s)?|cloud|A100|H100|RTX|4090|Colab|AWS|Azure|GCP|RunPod|Lambda Labs|vast\.ai)\b|\$\s?\d", re.I)
GPU_WITH = re.compile(r"\b(buy|bought|purchase|price|pricing|speed-?up|tripwire|hourly|per hour)\b", re.I)
# strip fenced blocks whose info string is owner-quote first, then flag a line when FORBID matches,
# or when it contains the word GPU together with GPU_WITH.
```
Tested: 0 hits on `60-FINDINGS.md` (its "this Mac's GPU (MPS ...)" passes); it flags `64-CONTEXT.md` and the amendments doc where they discuss the rule, as intended. The verdict and charter must therefore avoid the words entirely outside fenced owner quotes, including the roadmap's literal "no rented or cloud GPU route is costed or proposed" sentence; say "All computation runs on this Mac (standing owner rule, `PROJECT.md` Constraints, reaffirmed 2026-10-25)" instead, or allow one named sentence in the verifier.

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Gates on loss and energy of non-conformant runs (v2.0 held-out `ε_H` 237.2; generation 7 validation `ε_H` 15.65 then 50.63 while its loss fell) | A fixed physical-unit scorecard (`E`, valid horizon, `ε_H`, tiers) with known-error tests, frozen before any rung | 2026-10-11 to 17 (Phase 59) | The verdict quotes `E` and tiers, not loss |
| `ε_H` from finite-difference velocities (a 5 to 38% floor on Brutus's own answer) | Autograd velocities in the scorecard (GAP-59-02); the evaluator is unchanged (GAP-59-08 open) | 2026-10-11 | The charter's energy criterion is conditional |
| Verdict gloss "no change to the training recipe can fix it" | Label plus a plain side-by-side evidence box | 2026-10-25 (D-01) | Wording discipline in the verdict |
| Cost estimate "on this Mac and on a rented GPU" | Mac only (D-06) | 2026-10-25 (`bb323a52`) | Cost section, charter budget |

**Deprecated or outdated:**
- The amendments doc's "0.08–3%" for the 2026 study: the paper says about 0.02 to 3% (Table 12 and text).
- The amendments doc's rented-GPU clause (`:222-226`): superseded by D-06.
- `60-VALIDATION.md` and the plan text "under about 60 s" for `tests/phase60`: it takes about 13 minutes.

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | Breen et al. is a "2-parameter family" against 13 here | Comparison points | Overstates how restricted it is; the paper text confirms only "equal mass, zero initial velocity, planar". Quote the paper's own words |
| A2 | arXiv:2503.04585 uses the same restricted case (three unit masses, zero initial velocity) | Comparison points | Mis-scopes a paper the verdict may mention; read its full text first, or omit |
| A3 | The proposed Stage-0 bar (Tier 1 plus counts against formula and copy on at least 75% of validation systems; `ε_H` at most `10⁻²` on autograd velocities; `h` at 10% of at least 0.5 as the softer position alternative) | Charter inputs | These are proposals; the owner may want a different bar. Label them "proposed" on the page |
| A4 | A per-milestone budget of about one month (options 1, 3, 6 months) | Charter inputs | Sizing is the owner's call |
| A5 | Figure bytes stay identical across machines and library versions | Pitfall 12 | Only two runs on this Mac were compared; the verifier should compare rounded series, or record the versions |
| A6 | Levels 0 and 1 "reached" rest on earlier milestones' records; I re-read `43-VERDICT.md`, generation 7's `status.json` and REQUIREMENTS `:24-29`, not the v2.1 audit itself | Ladder evidence | The "not to spec" detail is second-hand; cite REQUIREMENTS, not the audit |
| A7 | The Mac-only rule forbids even a negative sentence about rented GPUs outside the owner's fenced quotes | Pitfall 7 | If the owner would accept one neutral sentence, relax the guard to allow it; the conservative reading is safer |
| A8 | File names, the `tests/phase64` package and the six-plan decomposition | Structure, Open Questions | Discretionary; any equivalent works |
| A9 | The owner answers checkpoint ① in free text in chat | Pattern 3 | If the answer arrives by another route, record it the same way |

## Open Questions (RESOLVED)

1. **How should the 12 requirements of the skipped phases be labelled at close?** (Source-silent; a candidate STOP item for the orchestrator to judge.)
   - What we know: CONF-10, CONF-11, INST-06, INST-07, SPEC-07 to SPEC-10, GATE-05, FEAS-05, RUN-06 and DIAG-08 read "Pending"; their phases read "Skipped at G2 (no rescue), not failed". VER-22 only tests the mapping. The v2.3 close recorded owner-decided dispositions beside VER-21.
   - What's unclear: whether "Pending" stands, or each gets a disposition, and whether it is carried forward to v2.5.
   - Recommendation: do not decide in the plan; fold one pre-filled line into checkpoint ① (proposed label "Skipped at G2 (no rescue), not failed; carried forward"), and apply it only if the owner approves.
   - → **Routed, not resolved by a plan:** GAP-64-01 in `64-GAPS.md` (OPEN, owner-routed). Checkpoint ① shows it as one pre-filled line (charter row C-14, option A as the default, `64-05-PLAN.md`), and `64-07-PLAN.md` applies only the label the owner chooses.
2. **What does "beats the best fixed-scorecard result" mean in the stop rule?** The baseline is a constant predictor, so a margin is needed. Offer options with a recommended default and leave the margin to the owner.
   - → **Resolved by D-12:** charter row C-10 (`64-05-PLAN.md`) proposes a default margin (A: at least one panel system reaches Tier 1, `E` at most 0.1), beside B (`E` below the constant predictor's by a margin the owner names) and C (any lower `E`); the owner decides at checkpoint ①.
3. **Should the rewrite go beyond "What This Is" and Core Value?** The title line and the Model constraint stay LLM-flavoured. One extra pre-filled line at the checkpoint.
   - → **Resolved by D-13:** one pre-filled charter line, C-13 (`64-05-PLAN.md`), offers rewriting the title line and the Model constraint too (A, with a draft) or leaving them (B); `64-07-PLAN.md` applies it only on the owner's approval.
4. **Mention the 2025 PINN paper?** It supports the "no novelty claim" sentence. Optional; read the full text before characterizing its data.
   - → **Decided:** optional, and only by what its abstract states, with no characterization of its data (`64-04-PLAN.md` `<interfaces>`, sources per section), so the full text need not be read; its data scope stays [ASSUMED] (A2), and it is not one of FEAS-06's comparison points.
5. **Numeric Stage-0 bar and budget.** These are proposals. If the owner would rather name the numbers, the page needs only an empty "Owner" cell.
   - → **Resolved by D-08 and D-09 (the bar) and D-11 (the budget):** C-4, C-5 and C-9 are pre-filled proposals on the charter page (`64-05-PLAN.md`), each with other options and an empty Owner cell; the owner approves them or names other numbers at checkpoint ①.
6. **The Key Decisions row in `PROJECT.md`.** v2.3 and earlier closes added one. `/gsd-complete-milestone` (out of scope) handles Evolution; add the row only if the plan takes it on explicitly.
   - → **Not taken on:** no Phase 64 plan adds the row (`64-07-PLAN.md` changes only the `PROJECT.md` parts the owner approves); it is left to `/gsd-complete-milestone`, which `64-CONTEXT.md` lists under "After Phase 64", out of scope here.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| `pinn-train` Python | every script | yes | 3.11.15 | none |
| numpy, torch (CPU), h5py, PyYAML | derive, figure | yes | 2.4.6, 2.12.1, 3.16.0, 6.0.3 | none |
| Pillow (FreeType) | optional PNG | yes | 12.3.0 | stdlib SVG |
| matplotlib, scipy, pandas, plotly | none | no | n/a | stdlib SVG (decided) |
| External data root `simulation_data/Data` (6.3 GB, untracked) | `derive`, `figure` | yes, on this Mac | n/a | none; without it only the committed-JSON modes run |
| git with worktrees | `frozen`, `traceability`, clean checks | yes | n/a | none |
| `node` and `gsd-tools.cjs` | GSD seams | yes | 1.13.0 | none |
| macOS Quick Look (`qlmanage`) | render the SVG to look at it | yes | n/a | open the SVG in a browser |
| MPS | not required (CPU only) | yes | torch 2.12.1 | none |
| Network from the Bash sandbox | not required at execution | no (curl timed out) | n/a | the literature facts are already captured here |
| `unittest` (pytest is not installed) | tests | yes | stdlib | none |

**Missing dependencies with no fallback:** none for a document phase. **Missing with fallback:** a plotting library (use the stdlib SVG). If the repo is reopened on another machine, `derive` and `figure` need the dataset copied there; `inputs`, `numbers`, `rules`, `frozen`, `charter` and `traceability` do not.

## Validation Architecture

`workflow.nyquist_validation` is `true` in `.planning/config.json`, so this section applies.

### Test Framework
| Property | Value |
|----------|-------|
| Framework | Python stdlib `unittest` under `pinn-train` 3.11.15 (`pytest` is not installed) |
| Config file | none; new package `tests/phase64/` (Wave 0) |
| Quick run command | `<home>/miniforge3/envs/pinn-train/bin/python -B -m unittest tests.phase64.test_verifier_phase64 -v` (target at most 30 s) |
| Full suite command | the quick command, plus the cheap regression set below |
| Existing verifier modules to reuse | `.planning/phases/60-single-system-learnability/evidence/verify_phase60_evidence.py` and `.planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py` |

### Phase Requirements to Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| FEAS-06 | The handoff is intact and the label re-derives; exactly seven arm directories; nothing that should be absent exists | contract | `$PY -B <E>/verify_phase64_verdict.py inputs` (prints `INPUTS-OK`) | Wave 0 |
| FEAS-06 | Every quoted number equals its re-derived value; the verdict contains the rendered tokens | contract | `$PY -B <E>/verify_phase64_verdict.py numbers` (`NUMBERS-OK`) | Wave 0 |
| FEAS-06 | Time-constant evidence and the along-window facts re-derive from the committed weights; zero test and validation opens | integration, real data | `cd <repo root> && $PY -B <E>/verify_phase64_verdict.py derive` (`DERIVE-OK`, about 5 s) | Wave 0 |
| FEAS-06 | The figure's SHA-256 matches its provenance; regenerated series match; no host path inside | integration, real data | `... figure` (`FIGURE-OK`) | Wave 0 |
| FEAS-06 | No GPU, cloud or price wording outside owner quotes; no `/Users/` in committed evidence; the verdict opens with `## In plain language`; the label string, D-02 sentence, D-03 candidates (unranked) and D-14 naming are present | contract | `... rules` (`RULES-OK`) | Wave 0 |
| FEAS-06 | No frozen or sealed path changed since `1ebb1d9b`; Phase 60 and 59 cheap checks pass | regression | `... frozen` (`FROZEN-OK`); `$PY -B <P60>/verify_phase60_evidence.py final` (1.3 s, `PHASE60-EVIDENCE-OK`); `$PY -B <P59>/verify_phase59_evidence.py scorecard-frozen` and `guardrails` (2 s each) | partly exists |
| FEAS-10 | The charter has the required items, owner quotes byte-equal to CONTEXT D-06 and D-07, Stages 1 to 6 marked open, `10⁻⁵`, GAP-59-08 A/B/C, stop-rule text, routed lines, the page region within the line limit | contract | `... charter` (`CHARTER-OK`) | Wave 0 |
| FEAS-06, FEAS-10 | The owner's decision record has exactly one non-empty `owner-quote` block, is tracked and clean, and approved edits (PROJECT.md rewrite) are applied only if the record approves | contract plus manual | `... ruling` (`RULING-OK`) | Wave 0 |
| FEAS-06, FEAS-10 | The owner's decision itself (continue, change course, stop; each charter choice) | manual-only | the blocking `checkpoint:decision`; only the owner can supply it | n/a |
| VER-22 | 24 defined, 24 in the table, 24 in the roadmap lines, no duplicates or orphans, and the stated count (24) agrees in every place it appears (REQUIREMENTS header and Coverage block, ROADMAP, PROJECT) | contract | `... traceability` (`TRACEABILITY-OK`) | Wave 0 |
| all | Every mode green, the final line last | aggregate | `... final` (`PHASE64-VERDICT-OK`) | Wave 0 |

`<E>` = `.planning/phases/64-feasibility-verdict/evidence`; `<P60>` and `<P59>` as in the Evidence Map. Print each success token on its own line and the aggregate token last, so a plan clause such as `tail -n 1 ... | grep -qx 'PHASE64-VERDICT-OK'` holds (Phase 60 lost a clause to an `END=` line printed after `EXIT=0`).

**Unit tests** (`tests/phase64/test_verifier_phase64.py`), each with a negative control: flip one number in a temporary copy of the verdict and `numbers` must fail; insert "rented GPU" outside a fence and `rules` must fail but pass inside an `owner-quote` fence; touch a frozen file in a temporary git repository and `frozen` must fail; delete a table row or duplicate a roadmap ID and `traceability` must fail; truncate an owner quote and `charter` must fail. Use real object shapes (the frozen `DataContext`, NumPy `ArmData`, real JSON records). One real-data integration test may skip with a clear reason if the data root is absent; the pure functions must not skip.

### Sampling Rate
- **Per task commit:** the quick unit command, plus the one verifier mode the task built, run on the real files.
- **Per wave merge:** the quick command; optionally `tests.phase60.test_verifier_phase60` (32 tests, 7.4 s, checked) to confirm the borrowed verifier still imports; `verify_phase60_evidence.py final`; Phase 59 `scorecard-frozen`, `guardrails`, and `manifest --area <area> --require-committed` for the five areas (about 2 s each); the `frozen` mode. Do not rely on the generic post-merge gate: it finds no Makefile or pyproject here and passes on `true`.
- **Phase gate (before `/gsd-verify-work`):** `final` plus the owner's recorded decision.
- **Substituted for the expensive commands, with reasons:** Phase 59 `final` (about 604 s) is not rerun because `git diff --quiet 4df5d4a8 HEAD` over its 10 producer modules and two directories is empty (checked); `tests/phase60` discovery (about 13 minutes) is not rerun because no `pinn/` file changes. If either reason stops holding, run the command once, detached, with full output kept outside the repo, and record the elapsed time.

### Wave 0 Gaps
- [ ] `tests/phase64/__init__.py` and `tests/phase64/test_verifier_phase64.py`
- [ ] `evidence/verify_phase64_verdict.py` (modes above) and `evidence/build_phase64_evidence.py`
- [ ] A real-file smoke of each mode before its tests are written (Pattern 4)
- [ ] The frozen-path list file for the `frozen` mode (41 paths) and its arg-count self-test

*(Framework install: none.)*

## Security Domain

`security_enforcement` is absent in `.planning/config.json`, so it is enabled.

### Applicable ASVS Categories
| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication, V3 Session Management | no | no network surface |
| V4 Access Control | yes (repo rule) | the Phase 59 allowlist keeps test-split files unopened; assert `test_split_opened` 0 and validation opens 0 |
| V5 Input Validation | yes | parse JSON and Markdown defensively; the owner's text lives only inside an `owner-quote` fence and is never parsed, executed or formatted into a path or command |
| V6 Cryptography | partial | SHA-256 from `hashlib` only; no custom crypto |
| V8 Data Protection | yes | repo-relative paths only; no absolute paths, host names or email addresses in committed evidence; the owner's email is not written anywhere |
| V10 Malicious Code | yes | `torch.load(..., weights_only=True)`; no `eval` or `exec`; no `shell=True` |

### Known Threat Patterns
| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Editing sealed evidence or a pinned module | Tampering | `frozen` mode, the Phase 60 verifier's `protocol` and `g2` checks, the sealed handoff hash |
| Free text from the owner becoming a governing file | Tampering | opaque `owner-quote` fence, a re-ask on ambiguity, a commit body that quotes the message (T-60-04) |
| A decision recorded without the owner's words | Repudiation | the verbatim record and its commit (T-60-20) |
| Local paths or host names leaking into evidence | Information disclosure | repo-relative paths, `data_root_source` label only, a `/Users/` scan |
| A held-out or test-split file opened by a re-derivation | Elevation of privilege | the real context's allowlist and attestation; fail closed on any nonzero counter |
| A pickle in a weights file | Tampering or code execution | `weights_only=True` on every `torch.load` |

## Sources

### Primary (HIGH confidence)
- Repository files read this session, with line ranges cited inline: `.planning/phases/64-feasibility-verdict/64-CONTEXT.md`, `.planning/REQUIREMENTS.md`, `.planning/ROADMAP.md`, `.planning/STATE.md`, `.planning/PROJECT.md`; `.planning/phases/60-single-system-learnability/{evidence/g2/*.json, evidence/arms/*/record.json, evidence/run-protocol.json, evidence/verify_phase60_evidence.py, 60-FINDINGS.md, 60-VERIFICATION.md, 60-17-PLAN.md}`; `.planning/phases/59-read-only-baseline-scorecard/{59-FINDINGS.md, 59-GAPS.md, 59-RESEARCH.md, evidence/scorecard-freeze.json, evidence/baselines/baselines.json, evidence/verify_phase59_evidence.py}`; `.planning/phases/58-verdict-traceability-close/{58-SUMMARY.md, 58-VERDICT.md}`; `.planning/milestones/v2.0-phases/43-verification-stage-0-pilot-acceptance/43-VERDICT.md`; `docs/work/designs/cross_cutting/v2.4-milestone-proposal/{2026-10-09-v2.4-roadmap-proposal.md, 2026-10-11-v2.4-feasibility-amendments.md}`; `pinn/verification/{feasibility_scorecard.py, feasibility_scorer.py, learnability_data.py, learnability_ruling.py, artifacts/feasibility_scorecard_v1.json}`; `pinn/data/adapter.py:594-606`; `pinn_instruction/markdown_conversion/framework-specs/{ctl_instruction.md, pinn_architecture.md}`; `runs/stage0-v23g7-seed42/{status.json, training_metadata.json, validation.jsonl}`; `docs/runbooks/external-research/2026-06-11-external-research-workflow.md`.
- arXiv primary pages and PDF excerpts, fetched through the Tavily extract tool: `arxiv.org/abs/1910.07291v1`, `arxiv.org/pdf/1910.07291v1`, `arxiv.org/abs/2607.23501v1`, `arxiv.org/pdf/2607.23501v1`, `arxiv.org/abs/2503.04585`. (The classify-confidence seam rates the Tavily provider LOW alone and MEDIUM when cross-checked; I cross-checked abs page against PDF text, so MEDIUM. Both digests are cached through `research-store`.)
- Scratch programs run read-only on the real committed files this session (in the session scratchpad, not committed): CPU float64 re-derivation, VER-22 count, verdict recompute, frozen-path gate, SVG prototype, GPU-wording guard.

### Secondary (MEDIUM confidence)
- The dataviz skill's palette validator (`validate_palette.js`), used for the three-slot light-mode palette.
- A web search summary that characterized arXiv:2503.04585's data scope (flagged [ASSUMED], A2).

### Tertiary (LOW confidence)
- None used for a recommendation.

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH, the stack is the pinned environment and records; one deliberate non-choice (no plotting library).
- Architecture: HIGH, every pattern is an existing repo pattern and the derivation path ran on real files.
- Pitfalls: HIGH, each was observed here or in the repo's own history (Phase 60's two first-use crashes; the vacuous zsh gate; the legend I drew off-canvas).
- Comparison points: MEDIUM, excerpts of two papers.
- Charter bars and budget: LOW by nature; they are proposals for the owner.

**Research date:** 2026-10-25
**Valid until:** the frozen evidence changes. Re-check with the `frozen` gate and `verify_phase60_evidence.py final`; otherwise the findings hold for the life of the phase.
