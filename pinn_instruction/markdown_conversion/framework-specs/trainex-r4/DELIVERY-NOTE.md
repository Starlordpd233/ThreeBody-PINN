---
title: Trainex R4 Delivery Note (single sub-package)
package_for: trainex-r4 (single sub-package)
role: user-facing handoff and routing instructions — NOT part of any upload to external agents
status: active
created: 2026-10-04
access_mode: open-book
source_baseline: 735e2ae8d5ec30b9915ec9172ac06965fbaa8afb
---

# Trainex R4 Delivery Note

**This file stays in the repository. Do NOT send it to external research agents.**

## Status: ruled; the next milestone is next (2026-10-07)

Codex (2026-10-04) and Claude (2026-10-06) returned reports.

- **Part 1** of the Rule-19 verification checked every premise-challenge
  finding in both reports and refuted none. The round was then re-framed
  (ruling below).
- **Part 2** checked the diagnoses, the facts behind each option, the gaps, and
  the registers. One numeric claim was refuted, and its error strengthens its
  own conclusion. Thirteen were narrowed. The literature is routed to a
  primary-source reading.
- **The consolidation** (`trainex-r4-resolution-doc.md`, commit `53b7c008`)
  joins both reports under rulings R-2 and R-3.
  - **The sheet.** Twelve decisions (`JD-0` to `JD-11`) and five owner
    questions, with the owner's-pick column empty. Conformance (`JD-0`)
    carries the owner's Option A default.
  - **The disputes.** The reports disagree on whether the guard may halt the
    next run, whether that run exercises L-BFGS, its seed design, and
    whether a balancing remedy is named before measurement.
  - **The literature.** The primary-source reading confirms every
    source-method fact the reports state, narrows one citation, and could
    not read four items.
- **The ruling** (`trainex-r4-ruling.md`, commit `c4bea18a`) was made on
  2026-10-07 by the in-repo agent under the owner's delegation.
  - **The next run** is the corrected control: the ratified recipe executed as
    specified, Adam-only for 1,000 steps on seeds 42, 41 and 43. The guard and
    the plateau handoff only record what they would have done, and telemetry is
    complete. It is not graded.
  - **The order.** Read-only checkpoint measurements come first, then
    conformance and its gates, then the run. The readout branches are fixed
    before the run.

The next milestone is next. It follows the ruling's "Order of work".

The owner routed the next milestone to this round at checkpoint ⑤ on
2026-10-03 (`.planning/phases/58-verdict-traceability-close/58-VERDICT.md`,
"Routing of the next milestone").

On 2026-10-04 the owner made two decisions about the round:

- **Hosting:** assemble it as a standalone round now, with a self-audit, not
  as the first phase of a new GSD milestone. The next milestone opens later to
  consume the results.
- **Output shape:** **diagnosis first, then options**. This combines a
  diagnostic contract (mechanisms, discriminating experiments) with the ERW
  Rule 7 build-design contract (options menus, marked defaults, door types,
  decision sheet).

Package root: `pinn_instruction/markdown_conversion/framework-specs/trainex-r4/`.

## Re-framing ruling (2026-10-07)

**Provenance.**

- **Who rules.** On 2026-10-07 the owner delegated this decision to the in-repo
  agent, Claude Code (`claude-opus-5-5`).
- **What it rests on.** Part 1 of the Rule-19 verification, which re-derived
  every premise-challenge finding in both reports and refuted none
  (`docs/work/reviews/cross_cutting/trainex-r4/2026-10-07-trainex-r4-rule19-claim-verification.md`,
  commits `b4b975e9` and `d97328d4`).
- **No second check.** A second, independent check of that layer was briefed
  but not run. The facts this ruling rests on are proved mechanically, by the
  code and by a replay of the run's random-number stream that matches every
  retained checkpoint.
- **What it decides.** How the round's returned answers may be used. The ERW
  runbook's "Handoff" step 6 requires this whenever a verified claim
  contradicts a package premise.
- **What it does not do.** It selects no option, changes no recipe value,
  authorizes no run or evaluation, and reverses no owner ruling.

**R-1. The round is re-framed, not re-commissioned.**

- **The false premise.** The package premise that generation 7 executed the
  ratified recipe is false:
  - its physics term ran on one trajectory per step;
  - its invariant-B monitor scored one trajectory;
  - L-BFGS could not run in its configuration;
  - generations 6 and 7 are one experiment.
- **Why the answers are still usable.** Both reports found this themselves and
  built their diagnoses on the corrected premise. Their answers are read
  through the re-framed question: *what did the executed run show, and what
  must change, starting with conformance, before a run can test the ratified
  recipe?*
- **No new round now.** No corrected package goes out. A new research round,
  if any, waits for evidence from a conformant run.

**R-2. How each kind of answer may be used.**

- **Structural findings are usable as findings.** These are properties of the
  configuration, code, specs, or guard that hold whichever trajectories the
  loss evaluates. Examples:
  - L-BFGS is unreachable when `max_epochs == n_adam`;
  - the cosine schedule and the guard window interact;
  - an `R_ref`-relative front cannot certify absolute accuracy;
  - the guard is a high-water record statistic;
  - the conformance verifier tested the sampler, not the loss;
  - the IC gradient dominates under residual-wide normalization. This is a
    design concern, to be re-measured once the run conforms.
- **Empirical rates and magnitudes from generations 6 and 7 describe the
  single-anchor run.** These include front pace, residual reductions, budget
  estimates, oscillation statistics, and the natural experiment. They may
  motivate hypotheses and experiments. They may not set or justify any recipe
  value.
- **Answers about the ratified recipe's own behavior are void as answers.**
  These are the Q4 step budget, and Q5's oscillation as a property of the
  recipe. They are carried forward as open questions.

**R-3. Conformance leads the decision sheet.**

- **The governing default.** The owner's 2026-09-07 Option A instruction
  stands: physics contributions come from every selected slot
  (`.planning/phases/57-corrected-re-run-the-preserved-evaluation/57-GAPS.md:214-218`).
  The consolidation presents conformance as decision D0 with that instruction
  as its default. Ratifying the one-trajectory behavior instead is possible
  only as the owner's explicit reversal of Option A.
- **Consequences, not choices.**
  - Any fix to selected-slot semantics triggers re-measuring `R_ref` and
    re-running GATE-04 (`pinn_architecture.md:454`).
  - A graded run before conformance is restored would again not test the
    recipe.
  - The next conformance gate must test what the loss evaluates, not what the
    sampler emits.
- **The IC term's batch behavior is its own decision.** It also runs on one
  trajectory, but Phase 57 kept that on purpose (`57-02-PLAN.md:87`), and the
  spec's `L_IC` states no batch rule. It goes to the decision sheet as its own
  item, because it carries the dominant gradient.

**R-4. The v2.3 record is annotated, not rewritten.**

- **The verdict stands.** The owner's v2.3 verdict `rethink` is unchanged.
- **Its rationale is not supported.** The recorded rationale is that "the
  corrected recipe's causal front failed to keep advancing"
  (`.planning/phases/58-verdict-traceability-close/58-VERDICT.md:19-20`). The
  corrected recipe's physics term did not run, so generation 7's stall is
  evidence about the executed run, not about the recipe.
- **The annotation.** It lives in `.planning/milestones/v2.3-GAPS.md` ("Post-close
  finding") and in `.planning/STATE.md`. The archived phase files stay as they
  are.

**R-5. Claude's training- and validation-data reads (its gap G-11) are
permitted.**

- The read-only bar protects the unspent held-out evaluation and forbids side
  effects.
- Reading training- and validation-split files spends nothing, and no
  test-split file was opened.
- Future prompts should state this boundary explicitly.

**R-6. Fan-out is closed.** The package goes to no further agents. The two
returned reports are the round's evidence.

**R-7. Next steps.**

1. Part 2 of the Rule-19 verification: the diagnoses, the facts each option
   rests on, the gaps, and the claims registers.
2. Consolidation into `trainex-r4-resolution-doc.md`, under R-2 and R-3.
3. The owner's ruling on the decision sheet.
4. The next milestone.

The verification also found a residual error in the delivered evidence bundle.
Part G's lead-in says the replay scored "four checkpoints"; the correct count
is five generation-7 plus three generation-6. It is recorded in the
verification report and left as delivered (D-15).

## Corrections before handoff (2026-10-04)

An independent double-check of the assembled package
(`docs/work/reviews/cross_cutting/trainex-r4/2026-10-04-trainex-r4-package-double-check-findings.md`)
found four issues in the master. The in-repo assessment found further
statements of the same kind. No agent had received the package (owner
confirmation, 2026-10-04), so the attachments were corrected in place rather
than through an erratum.

**What changed:**

- **Master F-07:** the tabulated `loss_data` lower bound is 0.016 (step 931).
  The trip record's loss values belong to the halted iteration logged as record
  952, not to completed step 951. Full-run ranges were added.
- **Master F-13:** generation 6's high-water mark was 2 at its last
  checkpoint (step 510), and the replay found its instantaneous front at 1. The
  description of how the two seed-42 runs diverge is corrected; the earlier
  "seventh or eighth significant figure from step 9" was wrong.
- **Master F-01, F-05, F-09, and §4.2:** clarified the step-951/952 semantics.
  The physics-term range now matches the digest (its tabulated maximum is
  0.192, not 0.19), and the IC dominance is stated as measured (at least 236
  times).
- **Master §1.1 and §4.2:** the verdict packet's "not a near miss" and "flat"
  readings are restated as the measured sums, consistent with listing those
  readings as challengeable (`H-02`).
- **Master §7 Q5:** the replay scored five generation-7 checkpoints, not four.
  The monitor's state lives in the checkpoints and the terminal record, and
  the TensorBoard file holds per-step training-batch traces.
- **Master §2:** added where each attachment sits in the repository.
- **Prompt:** "several orders of magnitude" is replaced by the measured factors.
- **Evidence bundle Part G:** the digest now also checks the trip record
  against the log, gives full-run ranges, and compares the two seed-42 runs.
  Its reading notes explain record 952, when `lr` is logged, and the replay's
  checkpoint count.

**What did not change:** the `source_baseline` and the 20 verbatim blocks.
The re-audit is recorded in the audit report's addendum. Hand off the
corrected version: stamp the Rule-20 pin with the commit at engagement, which
is after the correction commit.

## Handoff — what to attach, what to paste

Open `research_package/RESEARCH-AGENT-PROMPT.md`. Everything above its
horizontal rule is routing for you; everything below it is the prompt to paste.

**Attach these three files individually** (ERW Rule 15 caps a sub-package at five):

| # | Attachment | What it is |
|---|---|---|
| 1 | `research_package/RESEARCH-CONTEXT-MASTER.md` | The agent's entry point: source tiering, the recipe and the run, the five questions with their answer requirements, the claims register, the gaps, the output contract. |
| 2 | `specs/framework-specs-bundle.md` | Eleven verbatim locked-spec excerpts at the baseline commit, byte-verified. |
| 3 | `research_package/v2.3-closure-evidence-bundle.md` | The v2.3 closure record, verbatim (owner verdict, verdict packet with its replay, recalibration ruling, checkpoint ③/④ ruling, Phase 56 front-index findings, terminal, trip, and config records), plus a derived telemetry digest (Part G) with its exact script. |

Not uploaded: this delivery note, the prompt (pasted, not attached), and
`research_results/` (filled at delivery).

**Fan out across several external agents.** Save each report as
`research_results/<agent>-resolution.md`. *Closed on 2026-10-07 by ruling R-6:
the Codex and Claude reports are the round's returns.*

## Rule-20 live-tree pin — stamp one block per engagement

ERW Rule 20 pins the tree each agent actually saw. In trainex-r3 two agents
saw different things (one read the tree, one worked from attachments only), so
this note uses one block per returned report. Copy the block below for each
engagement and fill it at the time access is granted. If an agent works
without repository access, write **not applicable** for worktree, branch, and
commit, and never invent a pin for it.

### Codex engagement (2026-10-04)

| Field | Value |
|---|---|
| Report file | `research_results/codex-resolution.md` |
| Worktree | `<home>/Desktop/3_body_problem/.worktrees/trainex` |
| Branch | `milestone/v2.3` |
| Commit at engagement | `LIVE-TREE-PIN=b09c4c8cfd22429e0d14482c355719f862a54e6f` |
| How access was granted | The owner directed Codex to follow `research_package/RESEARCH-AGENT-PROMPT.md` and explicitly granted codebase access in this chat. |
| Date of engagement | 2026-10-04, America/Chicago |

The report was returned in chat after a read-only investigation. The owner then
explicitly requested saving it in the result folder. That delivery write does
not authorize experiments, recipe changes, or evaluation. Independent Rule-19
verification, consolidation, and the owner's ruling remain pending. Additional
agent engagements and returns may be recorded separately.

### Claude engagement (2026-10-06)

| Field | Value |
|---|---|
| Report file | `research_results/claude-resolution.md` |
| Worktree | `<home>/Desktop/3_body_problem/.worktrees/trainex` |
| Branch | `milestone/v2.3` |
| Commit at engagement | `LIVE-TREE-PIN=9bebe667b520e25e0bea5b84eeb0a4fc7168a9e5` |
| How access was granted | The owner directed Claude Code (`claude-opus-5-5`) to follow `research_package/RESEARCH-AGENT-PROMPT.md` and granted codebase access in this chat. The owner later authorized read-only sub-agents (Opus tier). |
| Date of engagement | 2026-10-06, America/Chicago |

The report was returned in chat after a read-only investigation, in which no
repository file was edited, no training was run, no evaluation was invoked, and
no commit was made. The owner then explicitly requested saving the report in the
result folder and recording this pin. That delivery write does not authorize
experiments, recipe changes, or evaluation.

The report's §0 records four disclosures:

- **Data files read.** It read training- and validation-split trajectory files:
  row counts, and the Stage-0 training positions, velocities and masses for
  physical scales. It opened no test-split file. Whether this counts as permitted
  read-only analysis is the report's gap G-11.
- **One forward-pass measurement.** A read-only sub-agent re-scored the frozen
  monitor from checkpoint contents only (CPU float32). This is the same class of
  measurement as the package's Part B replay.
- **Independence.** It did not read `research_results/codex-resolution.md`.
- **Uncommitted working files.** Its analysis scripts and sub-agent working files
  stayed in the session scratchpad and are not part of the delivery commit. The
  report records their SHA-256 digests.

Independent Rule-19 verification, consolidation, and the owner's ruling remain
pending.

### Engagement template

| Field | Value |
|---|---|
| Report file | `research_results/<agent>-resolution.md` |
| Worktree | _(fill at engagement)_ |
| Branch | _(fill at engagement)_ |
| Commit at engagement | _(fill with the full output of `git rev-parse HEAD` at the moment access is granted, written as `LIVE-TREE-PIN=<40 hex>`)_ |
| How access was granted | _(fill at engagement)_ |
| Date of engagement | _(fill at engagement)_ |

The `source_baseline` pin (below) covers the attachments. It does **not**
cover the live tree; that is what these blocks are for.

## Consolidation join points (ERW Rule 11)

When merging several agents' reports:

- **Premise-challenge findings merge first,** before any diagnosis is read. A
  contradicted premise invalidates the answers built on it.
- **The diagnoses join per question (Q1–Q5).** Two agents who name the same
  mechanism but disagree on its evidence have a resolvable disagreement. Two
  who name different mechanisms for the same observation have a diagnostic
  dispute. Route that dispute to the discriminating experiments, not to a vote.
- **The discriminating experiments are pooled.** Merge duplicates, and keep
  each one's stated cost and whether it needs a training run. The owner
  decides which, if any, to authorize. A read-only experiment on retained
  logs and checkpoints can run before any new training run.
- **The options join on the decision.** Each option carries the diagnostic
  outcome it presupposes, so options whose presuppositions conflict with the
  merged diagnosis are flagged, not silently dropped.
- **The source-method identification should converge,** and should be
  compared with trainex-r3's JOIN-2 identification. A disagreement here is
  resolved first, because several answers depend on what the source method
  says about scheduling.
- **The composed next-run recipes are the coherence check.** Compare them
  directly. A recipe that no agent's own menus compose into is a signal that
  the menus interact in a way the per-question answers missed.

## Access mode — open-book (ERW Rules 16, 20)

`access_mode: open-book`. The ERW runbook's default applies: every question
here references a run, a config, a code path, or a log, so the round runs
Route B. Under Route B, ERW Rules 1–2 invert: repository paths in the master
are expected, and the "attached files only" instruction must not appear.

## Obligations — what is done and what remains

| Obligation | State |
|---|---|
| `research_package/RESEARCH-CONTEXT-MASTER.md` | **done** |
| `research_package/RESEARCH-AGENT-PROMPT.md` (Rule 17 premise challenge, Rule 18 read-only bars, the diagnosis-then-options contract) | **done** |
| `specs/framework-specs-bundle.md` (Rule 15 single-file bundle) | **done**: 11 excerpts, byte-verified |
| `research_package/v2.3-closure-evidence-bundle.md` | **done**: 9 verbatim parts plus one derived digest, byte-verified |
| Package self-audit | **done**: `docs/work/reviews/cross_cutting/trainex-r4/2026-10-04-trainex-r4-package-audit.md`; re-audited after the pre-handoff corrections (its addendum) |
| Rule-20 live-tree pin | Codex and Claude engagements recorded above; fan-out closed 2026-10-07 (R-6) |
| `research_results/<agent>-resolution.md` | Codex result received as `research_results/codex-resolution.md` (2026-10-04); Claude result received as `research_results/claude-resolution.md` (2026-10-06); no further returns (R-6) |
| Rule-19 per-claim in-repo verification report under `docs/work/reviews/cross_cutting/trainex-r4/` | **done** 2026-10-07 (`2026-10-07-trainex-r4-rule19-claim-verification.md`). Part 1, the premise findings: 122 rows, none refuted (`b4b975e9`, `d97328d4`). Part 2, the diagnoses, option facts, gaps, and registers: 137 rows, 1 refuted, 13 narrowed, literature routed (`654d6ffe`) |
| Re-framing ruling (ERW runbook "Handoff" step 6) | **done** 2026-10-07, owner-delegated; see "Re-framing ruling" above |
| Consolidated `trainex-r4-resolution-doc.md` (Rule 12) | **done** 2026-10-07 (`53b7c008`), under rulings R-2 and R-3. Twelve decisions and five owner questions, picks empty. Its JOIN-2 holds the primary-source reading: every source-method fact the reports state confirmed, one citation narrowed, four items not read |
| Owner ruling on the decision sheet, plus any authorized experiments | **done** 2026-10-07, owner-delegated (`trainex-r4-ruling.md`, `c4bea18a`). Recorded as a project Key Decision (Rule 13). It authorizes the read-only experiments and, once its gates pass, the control run |
| The next milestone | **next**: read-only measurements, conformance, gates, the control run, the readout (`trainex-r4-ruling.md`, "Order of work") |

## Provenance

`source_baseline`: `735e2ae8d5ec30b9915ec9172ac06965fbaa8afb`. It is the
repository commit at assembly and the ERW Rule-5 pin for both bundles and the
master's citations. It is byte-identical to the value in the master, the
prompt, and both bundles.

## Standing boundaries, in plain terms

These carry forward from the v2.3 close (`58-VERDICT.md`):

- **No tuning without a new owner decision.** No recipe value (`η_c`, the
  `R_ref` normalization, `ω₀`, `N_t`, and the rest) is changed against these
  results without an explicit owner ruling (SCOPE-37's carry-forward).
- **One held-out evaluation, preserved unspent.** Only owner policy spends it.
- **Stage-0 only.** Stage-1+ and PLAT-01..07 stay blocked until a `go`
  verdict.
- **No run before a ruling.** No training run is authorized until this round
  returns and the owner rules.
- **Read-only agents.** External agents edit nothing, run no training, and
  invoke no evaluation.

## Standing of the eventual resolution doc

This is a build-design round. The consolidated resolution doc offers findings,
experiment proposals, and options menus, not verdicts. The owner fills the
decision sheet, and those picks are the decisions. The report is not a
grounding source for framework-spec adjudication. Any spec change it leads to
is a formal amendment requiring explicit owner re-ratification.
