---
title: Trainex R2 Research Agent Prompt — paste-ready, never uploaded
role: user-facing attach-list header above the rule; the paste-ready neutral-contract prompt body below it
status: active
created: 2026-07-24
self_contained: true
---

> [USER INSTRUCTIONS — this bracketed header is NOT part of the prompt. It is
> routing for the person performing the handoff.]
>
> Attach exactly these **four individual files** (no folders) to the
> conversation:
>
> 1. `RESEARCH-CONTEXT-MASTER.md`
> 2. `44-DIAGNOSIS.md`
> 3. `framework-specs-bundle.md`
> 4. `run-evidence-bundle.md`
>
> Then paste everything below the horizontal rule as the prompt. This prompt
> file itself is **pasted as text and is never uploaded** — it does not count
> against the attachment cap (4 uploads of the at-most-5 hard cap).

---

# [PROMPT BODY — paste from here down]

You are performing **adjudication-grade research** over the attached materials
for a physics-informed neural-network (PINN) training-recipe investigation.
You are one of several external research agents whose reports the project owner
will later consolidate. Write your report to stand on its own.

## Read the master first

Read `RESEARCH-CONTEXT-MASTER.md` first and treat it as your **single entry
point**. Its manifest, its source tiering, its five research questions, its
claims register, and its output contract govern your work. The other three
attachments are the evidence and the locked spec it directs you to.

## What you are doing

Answer the **five research questions** defined in `RESEARCH-CONTEXT-MASTER.md`
(Q1 training budget/steps; Q2 warmup + learning-rate schedule; Q3 loss
weighting/balancing, which includes the normalization/data-scale sub-facet;
Q4 Stage-0 curriculum pacing; Q5 evaluation policy). The questions are posed
**neutrally** — they recommend no answer, and neither does this prompt.

## How to answer (your contract)

- **Cite your evidence.** Support each answer with reasoning and evidence cited
  to the attached files by **bare filename and section** — for example
  "44-DIAGNOSIS.md §3", "framework-specs-bundle.md Excerpt 5", or a claims-register
  row like "F-07". List which `F-` (established fact) and `H-` (hypothesis) rows
  each answer relied on.
- **Frame trade-offs.** Where plausible positions exist, lay out the trade-offs
  between them. Do **not** assume a house preference.
- **Do not recommend a remedy.** The project owner adjudicates the remedy in a
  separately governed step from the consolidated research. Your answers inform
  that decision; they do not make it. Pose, do not steer.
- **Treat the rankings as challengeable.** Every `[HYP]`-tagged passage and
  every `H-` register row is **agent analysis — not established fact**. The
  DIAG-04 candidate-cause rankings are one prior analysis to test against the
  evidence, not settled findings to defend. Do not treat "population-scale
  generalization shortfall" or any other candidate as established.
- **Discriminating tests are proposals only.** Any discriminating test mentioned
  in the materials is a proposed research direction requiring separate
  project-owner authorization. You are not asked to run, commission, or promise
  any experiment, training run, or evaluation.
- **Record gaps — never invent.** Where the attached materials are silent or
  ambiguous, record it explicitly in a dedicated gaps section. A gap is a
  legitimate, valued output. Do not fill silence with assumed values, schedules,
  thresholds, or directions.

## You are working from the attached files only

You have **no codebase access**. Any file referenced inside an attachment but
not itself one of the four attached files is **unavailable** to you — do not
guess at its content. If an unattached reference matters to an answer, name it
and record the gap. (The verbatim diagnosis snapshot retains internal
cross-references that point at files you do not have; treat those pointers as
unavailable, per `RESEARCH-CONTEXT-MASTER.md` §1.)

## Report structure

Produce one report with **per-question sections (Q1–Q5)** and a final
**gaps section**. In each answer, state the evidence you relied on, frame the
trade-offs, and flag any place you relied on an `H-` row as if it were
established (you should not, but say so if you did). The project will
consolidate your report with others into one resolution document.
