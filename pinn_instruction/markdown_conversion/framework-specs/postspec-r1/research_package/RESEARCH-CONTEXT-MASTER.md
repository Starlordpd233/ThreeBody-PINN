---
title: Post-Spec R1 Research Context Master
source_baseline: 6a720fe0
created: 2026-06-18
channel: build-design / strategy advisory
standing: recommendations and findings only; not a project decision and not a candidate verdict source
attachments:
  - RESEARCH-CONTEXT-MASTER.md
  - FRAMEWORK-SPECS-BUNDLE.md
---

# Post-Spec R1 Research Context Master

You are advising on the next broad stage of work for a computational-physics ML
project. The project is a curriculum-trained physics-informed neural network
for the gravitational three-body problem.

The project owner has recently spent several milestones on framework-spec work:
editing, adjudicating, and stabilizing the core framework markdown documents.
The owner is now deciding what broad type of work should come next.

This is a strategic direction assessment. It is not a request for a detailed
implementation plan.

## Companion File Manifest

You have two attached files:

1. `RESEARCH-CONTEXT-MASTER.md` - this orientation and output contract.
2. `FRAMEWORK-SPECS-BUNDLE.md` - bundled snapshots of the framework specs:
   `ctl_instruction.md`, `pinn_architecture.md`, and `sampling_method.md`.

You do not have repository access. Work only from the attached files plus your
own external research where useful. Refer to companion files by bare filename.

## Project State

The project has completed multiple spec-heavy milestones. Recent work has
focused on architecture and physics foundations, data-pipeline and validation
contracts, and framework-spec correction.

The current framework source of truth is the markdown framework specs bundled
in `FRAMEWORK-SPECS-BUNDLE.md`.

The project has not yet performed the main production implementation/training
buildout from those specs. Existing older live code is not treated as the source
of truth for the current framework. Future implementation work is expected to
rebuild from the current specs and from later user decisions.

The project is currently near the transition between spec-heavy design work and
the next major stage. The owner wants help deciding what kind of stage that
should be.

## Owner Intent

The owner is not asking for a detailed execution plan yet. They are asking for a
strategic compass: what broad kind of work should come next, why that direction
is better than the alternatives, and what should probably wait.

The owner specifically wants the assessment to leave room for independent
thinking. EDL and Trainex are known candidate directions, but they are not the
only acceptable answers.

The owner does not want the report to get stuck in procedural detail. Avoid
fine-grained gates, milestone checklists, task-by-task plans, or implementation
backlogs.

## ERW Standing

This is an External Research Workflow package in the build-design / strategy
advisory channel.

Your report may recommend a direction, but it does not decide for the project.
The project owner makes final decisions.

Your report is not a candidate verdict source for framework-spec adjudication.
Do not present your recommendations as binding spec truth.

## Candidate Direction: EDL

EDL means Empirical Decision Loop. It is a support workflow for source-silent or
ambiguous decisions where empirical behavior may matter.

EDL is used to package research context, decide whether small probes are useful,
and potentially run small-scale experiments before a framework contract or
implementation path is locked.

EDL does not decide outcomes by itself. It produces evidence or research support
for later user-approved decisions.

An EDL-first next stage would emphasize small experiments, probes, and research
loops before a larger buildout.

## Candidate Direction: Trainex

Trainex means the training-execution / reality-pipeline track. It concerns how
the framework becomes a runnable, observable, reproducible training system for
the project owner.

The Trainex baseline is focused on practical training execution: environment,
data ingestion, training loop, monitoring, checkpoint/resume, verification
surface, and user runbook.

Trainex already exists as a framed project track and has a foundational research
round prepared elsewhere. No returned Trainex research result is included in
this package.

A Trainex-first next stage would emphasize turning the framework into a
trainable operational system.

## Strategic Evaluation Lens

Assess next-stage directions by how well they:

1. Reduce the largest risk before full-scale implementation.
2. Create useful evidence without requiring the whole system to be built first.
3. Preserve momentum after a long spec-heavy period.
4. Avoid premature engineering detail.
5. Avoid false certainty where sources or evidence are unsettled.
6. Fit a single-machine, non-expert-operator project reality.
7. Clarify what broad class of work should come next.

Use this lens to improve your recommendation up front. Do not defer the useful
thinking into a large "what information would change this recommendation"
section.

## Report Failure Modes To Avoid

Do not produce:

- a detailed task-by-task implementation plan;
- a milestone gate/checklist system;
- a generic ML project roadmap detached from the attached framework;
- a simple endorsement of EDL or Trainex without considering alternatives;
- a re-adjudication of the framework specs;
- a long list of possible work with no prioritized direction;
- a recommendation that depends on facts not present in the attached materials
  without clearly marking that dependency.

## Your Task

Deliver a strategic post-spec direction assessment.

Assess at least these possible directions:

1. EDL-first.
2. Trainex-first.
3. A hybrid EDL plus Trainex path.
4. Any third path or reframing you believe is more valuable.

You are encouraged to challenge the framing if the attached materials suggest a
better way to think about the next stage.

## Required Output

Produce one polished, human-readable report in PDF-ready Markdown. If your
environment can also export a PDF, a PDF companion is welcome, but Markdown is
the durable required source.

Use this section order:

1. Title.
2. Executive Summary.
3. Current-State Diagnosis.
4. Strategic Evaluation Lens Applied.
5. Candidate Direction Assessment.
6. Recommended Direction of Travel.
7. Why This Direction Is Better Than The Alternatives.
8. What Not To Work On Yet.
9. Key Risks and Unknowns.
10. Closing Recommendation.
11. References / Source Notes.

Style requirements:

- Write in clear, friendly, organized prose.
- Use headings, short paragraphs, and tables only where they improve readability.
- Be opinionated enough to be useful.
- Mark uncertainty plainly.
- Do not invent missing project facts.
- Do not turn the answer into a detailed execution plan.

## Source Discipline

Where the attached materials are silent or ambiguous, say so. Do not fill the
gap with a confident-sounding assumption.

If you use outside sources, cite them clearly and date-sensitive claims should
be verified from current primary sources.

If your recommendation depends on an assumption, state the assumption in the
relevant section rather than placing all uncertainty in a separate appendix.
