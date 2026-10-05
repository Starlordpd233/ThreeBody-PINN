---
title: Trainex R4 Research Agent Prompt — Stage-0 Causal-Front Stall After the v2.3 Recalibration
package_for: trainex-r4 (single sub-package)
role: paste-ready prompt for the external research agent; the header above the rule is user-facing routing and is NOT pasted
status: active
created: 2026-10-04
access_mode: open-book
source_baseline: 735e2ae8d5ec30b9915ec9172ac06965fbaa8afb
---

# Trainex R4 — Research Agent Prompt

## FOR THE USER — attach these three files, then paste everything below the rule

Attach each file individually, not as a folder. All three live under
`pinn_instruction/markdown_conversion/framework-specs/trainex-r4/`:

1. `research_package/RESEARCH-CONTEXT-MASTER.md`
2. `specs/framework-specs-bundle.md`
3. `research_package/v2.3-closure-evidence-bundle.md`

That is three attachments, under ERW Rule 15's cap of five.

**This round is open-book (Route B).** Before pasting, give the agent
read-only access to the repository. Then record in `DELIVERY-NOTE.md` which
worktree, which branch, and which commit the tree was at during the
engagement (ERW Rule 20). Without that pin, the agent's `file:line` citations
rot silently as the tree moves. If an agent ends up working without
repository access, record that too. Do not stamp a live-tree pin for an agent
that never saw the tree.

**Fan out.** Paste to more than one external agent. Save each result as
`research_results/<agent>-resolution.md` under the round root.

**Do not skip the verification pass.** Every repository-derived claim in a
returned report is a checkable assertion, not an established fact, until it
is independently re-derived in-repo and the verification is recorded (ERW
Rule 19). That report lands under `docs/work/reviews/cross_cutting/trainex-r4/`.

---

You are a research agent on a project that trains a physics-informed neural
network (PINN) to predict three-body gravitational trajectories, under a
staged curriculum. I need a rigorous, cited research report on why a training
run stalled, followed by concrete options for what to do next.

You are not making the decision. A human owner rules on it. I need your
diagnosis first, then your options and marked defaults, so the owner has
something concrete to rule on.

## Read this first

Start with `RESEARCH-CONTEXT-MASTER.md`. It is the entry point and it governs
everything else:

- **§3:** how to treat each class of source.
- **§4:** the recipe that ran and what the run did.
- **§5:** the five questions, plus §5.6, which constrains the *form* of an
  adequate answer.
- **§6:** separates established facts from prior analysis you should
  challenge.
- **§7:** what the assembled evidence cannot answer.
- **§9:** your output contract.

Read §5.6 carefully; most of the difficulty lives there.

The two bundles reproduce the locked specification excerpts and the v2.3
closure records verbatim, pinned to a named commit. The evidence bundle's
Part G is the one derived component: a telemetry digest of the training logs,
reproduced with its exact script so it can be re-run.

## The problem, in one paragraph

A SIREN network (sinusoidal activations, `first_omega_0 = 30`, 12 layers, a
power-enhanced skip stack) is trained against a second-derivative physics
residual. Causal weights pace the training along the trajectory:
`w_n = exp(-η_c · Σ_{m<n} stopgrad(R̃_m))`, over 16 time bins. A previous
round fixed a failure in which these weights underflowed at initialization.
The fix normalizes each bin residual by a frozen reference
`R_ref ≈ 1.97 × 10¹⁰` measured at initialization, and it was proven healthy
at initialization before any run was spent.

Under that recipe, the "causal front" (the last bin whose weight exceeds 0.5)
moved from bin 0 to bin 2 by step 450. It then made no further progress, and
a guard requiring a new front high-water mark within 500 steps halted the run
at step 951.

In the same window, the cosine learning rate fell about 100×. Throughout the
run, the initial-condition loss term was at least 236 times the rest of the
loss. On the steps where gradients were measured per term, its gradient norm
was 2.78 × 10⁴ to 2.62 × 10⁶ times the physics term's. The front measured on
the resampled training batches moved between 0 and 3, while the frozen
monitor stayed at or below 2.

Which of these, if any, explains the stall is unknown. That is what you are
asked to work out, before anyone changes the recipe.

## Access mode: open-book

You have read-only access to the repository. Use it. The attachments frame the
questions and fix the baseline; they are not the boundary of your evidence.
The full training logs (`runs/stage0-v23g7-*/logs/`, `runs/stage0-v23g6-*/logs/`),
checkpoints, and the trainer code are all available to read.

**Published literature is a required evidence source.** The causal-weighting
scheme is not original to this project, and the project's specification
cites no source for it. Identify the published method, cite it properly, and
state what it says, in its own terms, about the following:

- setting or scheduling its causal parameter;
- how training progress moves the weights;
- how the optimizer schedule interacts with them.

**Resolve repository anchors by content, not by line number.** Several copies
of each framework specification exist with different line numbering, and only
the live ones are authoritative. Master §3 lists them.

## Your duties

**Challenge the premises. This is a duty, not a permission.** Test this
package's own stated premises against the repository, including every
"established" row in master §6. Report every contradiction as a
**first-class finding, up front, ahead of your diagnosis**, not as a footnote.
An agent that finds a false premise and buries it has failed the round. On
this project a previous round discovered exactly that: the executed run did
not match the specification, which made the whole question set's premise
false.

**Diagnose before you prescribe.** For each question, do three things before
proposing any option:

- name the mechanisms the evidence admits;
- say what each predicts for the recorded quantities;
- say which existing evidence discriminates between them.

Where nothing existing discriminates, propose an experiment that would. Say
what it measures, what each outcome would mean, roughly what it costs, and
whether it needs a new training run or can be done read-only on the retained
logs and checkpoints.

**Derive independently before you compare.** Every `H-` row in master §6 is
transcribed analysis. Work the result out yourself first, then state where you
agree and disagree, with reasons.

**Record gaps rather than inventing.** Where the attachments, the repository,
and the literature are silent or ambiguous, say so in your gaps section. A
well-stated gap is a valued output on this project, not a failure.

## Hard bars — read-only, in the imperative

- Edit no file.
- Start no training run.
- Invoke no evaluation. The project holds exactly one unspent held-out
  evaluation, governed by owner policy; it is not yours to spend.
- Run no command with side effects. Make no commit.
- Edit no framework specification.
- Select no remedy. Propose options and mark defaults, but the ruling is the
  owner's.
- Propose experiments as owner-gated options. Never perform them. Read-only
  analysis of the retained logs and checkpoints is permitted.

## What to produce

One research report in five parts, in this order:

1. premise-challenge findings;
2. a diagnosis for each of master §5.1 through §5.5, satisfying §5.6;
3. options;
4. gaps;
5. a claims-and-uncertainty register.

For each decision the diagnosis exposes, give:

- an **options menu** of two to four options, with their mechanical-surface
  trade-offs and their cross-decision interactions;
- for each option, **which diagnostic outcome it presupposes**;
- a **suggested default, clearly marked**, on each menu, or an explicit
  branch on an experiment's outcome where the right option depends on it;
- a **one-way versus two-way door classification** on every suggested default
  and every deviation from it: state whether committing to it is cheaply
  reversible or not, and why.

Across all decisions, add:

- a **composed next-run recipe** that assembles your suggested defaults into
  one coherent configuration, as a cross-menu coherence check;
- a **"what the runbook inherits"** section;
- a fill-in **decision sheet** with columns: decision | options | suggested
  default | door type | presupposed diagnosis | owner's pick.

Every repository claim carries a `file:line` citation. Every literature claim
carries author, title, venue, and year. Label each claim by its evidence base:
package-derived, repository-verified, literature, or your own analysis.

**Suggest defaults; never decide.** The values at stake sit inside
owner-ratified contracts, and changing one is a formal amendment with its own
provenance requirements. Your job is to make the ruling well-informed and
concrete, not to pre-empt it.
