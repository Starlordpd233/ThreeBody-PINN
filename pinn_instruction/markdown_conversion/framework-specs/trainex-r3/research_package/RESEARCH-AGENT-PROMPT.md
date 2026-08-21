---
title: Trainex R3 Research Agent Prompt — Causal-Weight / SIREN-Scale Recalibration
package_for: trainex-r3 (single sub-package)
role: paste-ready prompt for the external research agent; the header above the rule is user-facing routing and is NOT pasted
status: active
created: 2026-08-21
access_mode: open-book
source_baseline: 6a4f9b9902ab62e1d1f57bba0e521f38120c416d
---

# Trainex R3 — Research Agent Prompt

## FOR THE USER — attach these three files, then paste everything below the rule

Attach individually (no folders). All three live under
`pinn_instruction/markdown_conversion/framework-specs/trainex-r3/`:

1. `research_package/RESEARCH-CONTEXT-MASTER.md`
2. `specs/framework-specs-bundle.md`
3. `research_package/v2.2-closure-evidence-bundle.md`

Three attachments, against ERW Rule 15's cap of five.

**This round is open-book (Route B).** Before pasting, grant the agent read-only
access to the repository, and record in `DELIVERY-NOTE.md` which worktree, which
branch, and which commit the tree was at during the engagement (ERW Rule 20).
Without that pin the agent's `file:line` citations rot silently as the tree moves.

**Fan out.** Paste to more than one external agent. Save each result as
`research_results/<agent>-resolution.md` under the round root.

**Do not skip the verification pass.** Every repository-derived claim the report
returns is a checkable assertion, not an established fact, until it is
independently re-derived in-repo and the verification is recorded (ERW Rule 19).
That report lands under
`docs/work/reviews/milestone_v2.3/54-recalibration-decision-grounding/`.

---

You are a research agent working on a physics-informed neural network (PINN)
project that trains a curriculum-staged network to predict three-body
gravitational trajectories. I need a rigorous, cited research report that
informs one engineering decision. You are not making the decision — a human
owner ratifies it — but I need your analysis, your options, and your marked
defaults so that the owner has something concrete to rule on.

## Read this first

Start with `RESEARCH-CONTEXT-MASTER.md`. It is the entry point and it governs
everything else: its §3 tells you how to treat each class of source, its §4
states the confirmed mechanism and the coupled decision surfaces, its §5 carries
the questions (including §5.7, which constrains the *form* of an adequate
answer), its §6 separates established facts from analysis you should challenge,
its §7 states what the assembled evidence cannot answer, and its §9 is your
output contract. Read §5.7 carefully; it is where most of the difficulty lives.

The two bundles are verbatim, unedited pins of the locked specification
excerpts and the closure evidence. They are reproduced at a named commit and
every excerpt can be re-derived from it.

## The problem, in one paragraph

A SIREN network (sinusoidal activations, `first_omega_0 = 30`, 12 layers, with a
power-enhanced skip-residual stack) is trained against a physics residual that
is a **second-derivative** operator. A causal weighting scheme paces training
along the trajectory: `w_1 = 1`, `w_n = exp(-eta_c * sum_{m<n} stopgrad(Rbar_m))`
with `eta_c = 1`, applied to an **unnormalized** residual `Rbar`. At
initialization the network's second derivative is `O(10^5)` in its own units,
so `Rbar` is `~10^10` — about 8.5 decades past the point where the exponential
underflows float32. Every causal weight but the first pins to the numerical
floor, the weight vector carries no differential information, the causal front
never advances, and a conformant training run halted on that condition. Both
halves of the specification are internally coherent; they were never calibrated
against each other. The master's §4 gives the numbers and their sources.

## Access mode: open-book

You have read-only access to the repository. Use it. The attachments frame the
questions and fix the baseline; they are not the boundary of your evidence.

**Published literature is a required evidence source for this round, not an
optional one.** The causal-weighting formula is not original to this project,
and the project's own specification cites no source for it (master `F-13`).
Identify the published method it derives from, cite it properly, and state that
method's own calibration procedure in the source's own terms.

**Resolve repository anchors by content, not by line number.** Four files named
`pinn_architecture.md` exist in the tree with different line numbering, and only
one is the live locked specification — master §3 names it and tabulates the
others. The live file was also edited recently, so line anchors quoted inside
older planning documents are stale by construction.

## Your duties

**Challenge the premises. This is a duty, not a permission.** Test this
package's own stated premises against the repository. Report every contradiction
as a **first-class finding, up front, ahead of your per-question answers** — not
as a per-question footnote. An agent that finds a false premise and buries it
has failed the round. This instruction exists because it has already happened
on this project: a previous round was commissioned closed-book, was granted
repository access anyway, and discovered that the executed run diverged from the
locked specification in five respects — one of which made the entire question
set's premise false. A closed-book agent cannot tell you your question is wrong.

**Derive independently before you compare.** Where the package transcribes an
analysis — every `H-` row in master §6 — work the result out yourself first,
then state where you agree and where you disagree, with reasons. Do not treat a
transcribed analysis as a starting point to refine.

**Record gaps rather than inventing.** Where the attachments, the repository,
and the literature are silent or ambiguous, say so in your gaps section. A
well-stated gap is a valued output on this project, not a failure.

## Hard bars — read-only, in the imperative

- Edit no file.
- Start no training run.
- Invoke no evaluation. The project holds exactly one unspent held-out
  evaluation and it is governed by owner policy; it is not yours to spend.
- Run no command with side effects. Make no commit.
- Edit no framework specification.
- Select no remedy. Propose, rank, and mark a default — but the ratification is
  the owner's.
- Propose discriminating experiments as owner-gated options. Never perform them.

## What to produce

One research report. Structure it as: (1) a premise-challenge findings section,
up front; (2) per-question sections answering master §5.1 through §5.6, each
satisfying every requirement in §5.7; (3) a decision sheet; (4) a gaps section;
(5) a claims-and-uncertainty register.

For each decision, give:

- an **options menu** of two to four options, with their mechanical-surface
  trade-offs and their cross-decision interactions;
- a **suggested default, clearly marked**, on each menu;
- a **one-way versus two-way door classification** on every suggested default
  and every deviation from it — state whether committing to it is cheaply
  reversible or not, and why;
- a **composed first-run recipe** that assembles your suggested defaults into
  one coherent configuration, presented as a cross-menu coherence check: if the
  menus disagree with each other, this is where it shows;
- a **"what the runbook inherits"** section — what a person implementing this
  would need to carry forward;
- a fill-in **decision sheet** with columns: decision | options | suggested
  default | door type | owner's pick.

Every repository claim carries a `file:line` citation. Every literature claim
carries author, title, venue, and year. Label each claim by its evidence base:
package-derived, repository-verified, literature, or your own analysis.

**Suggest defaults; never decide.** The distinction matters here more than
usual: the values at stake sit inside owner-ratified contracts, and changing one
is a formal amendment with its own provenance requirements. Your job is to make
the ruling well-informed and concrete, not to pre-empt it.

## One thing worth knowing about scope

The routing document that commissioned this work authorizes four remedy
families, not three: changing the exponent coefficient or the exponent's form;
introducing an explicit normalization of the residual against a reference scale;
changing the network's initialization scale; **or redesigning the curriculum
mechanism so that it does not require the two to agree at initialization**. The
fourth is in scope. Master §4.3 quotes the authorization verbatim. Treat the
mechanism itself as available for redesign if the evidence takes you there —
and if it does not, say why.
