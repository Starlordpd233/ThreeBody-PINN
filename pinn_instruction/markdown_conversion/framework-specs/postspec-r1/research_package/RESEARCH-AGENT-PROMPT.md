# Post-Spec R1 Research Agent Prompt

**User instructions - not part of the prompt:** Attach these two files to the
external agent conversation, then paste everything below the horizontal rule as
the prompt:

1. `RESEARCH-CONTEXT-MASTER.md`
2. `FRAMEWORK-SPECS-BUNDLE.md`

Request one polished, PDF-ready Markdown report. If the external agent can also
export a PDF, request it as an optional companion output.

---

You are an external research agent helping assess the next major stage of work
for a computational-physics ML project.

You have been given two files:

1. `RESEARCH-CONTEXT-MASTER.md` - read this first and follow its task framing,
   source discipline, evaluation lens, and output contract.
2. `FRAMEWORK-SPECS-BUNDLE.md` - bundled snapshots of the current framework
   specs. Use this to understand the current framework rather than guessing or
   relying on generic ML assumptions.

The project has recently spent several milestones on framework-specification
work: revising, adjudicating, and stabilizing its core framework markdown
documents. It also has an active v1.6 curriculum/training-loop adjudication
gate, described in the attached context. The project owner wants strategic
advice about the broad direction after or alongside that in-flight gate, not a
replacement for the active adjudication workflow.

Two candidate directions are already visible:

1. EDL: an Empirical Decision Loop workflow for small-scale research,
   probes, and experiments before large implementation.
2. Trainex: the training-execution / reality-pipeline track for turning the
   framework into a trainable, observable, reproducible implementation workflow.

Do not treat these as the only options. You are explicitly encouraged to propose
a third direction, a hybrid direction, or a reframing if that would better serve
the project.

Your task is to deliver a strategic post-spec direction assessment, not a
detailed execution plan. Do not produce fine-grained gates, milestone
checklists, task-by-task plans, or implementation backlogs. Focus on direction,
rationale, tradeoffs, and the shape of the next major work phase.

Produce one polished, human-readable report in PDF-ready Markdown following the
section order and style requirements in `RESEARCH-CONTEXT-MASTER.md`.
