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

## Status: ASSEMBLED, awaiting handoff (2026-10-04)

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
`research_results/<agent>-resolution.md`.

## Rule-20 live-tree pin — stamp one block per engagement

ERW Rule 20 pins the tree each agent actually saw. In trainex-r3 two agents
saw different things (one read the tree, one worked from attachments only), so
this note uses one block per returned report. Copy the block below for each
engagement and fill it at the time access is granted. If an agent works
without repository access, write **not applicable** for worktree, branch, and
commit, and never invent a pin for it.

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
| Rule-20 live-tree pin | at each engagement (template above) |
| `research_results/<agent>-resolution.md` | at delivery |
| Rule-19 per-claim in-repo verification report under `docs/work/reviews/cross_cutting/trainex-r4/` | after delivery, **before** any claim informs a decision |
| Consolidated `trainex-r4-resolution-doc.md` (Rule 12) | after verification |
| Owner ruling on the decision sheet, plus any authorized experiments | owner, after consolidation; picks recorded as project Key Decisions (Rule 13) and carried into the next milestone |

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
