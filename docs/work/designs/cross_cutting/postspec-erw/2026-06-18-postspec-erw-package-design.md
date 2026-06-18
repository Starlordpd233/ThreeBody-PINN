---
status: active
purpose: design
created: 2026-06-18
milestone: untracked
phase: cross-cutting
retirement_trigger: postspec-r1 ERW package has been sent, results have landed, and the package design has been absorbed or superseded
---

# Post-Spec ERW Package Design

## Purpose

Create a ready-to-send External Research Workflow package that asks an external
research agent to assess the next broad stage of work after the recent
framework-specification milestones.

The package should help the project owner decide the direction of travel after
spec-heavy work. It should not ask the research agent for a detailed execution
plan, task-by-task roadmap, milestone checklist, or implementation backlog.

## Package Standing

This is a build-design / strategy advisory ERW package. The returned report is
not a candidate verdict source for framework-spec adjudication, and it does not
make binding project decisions.

The research agent may recommend a direction, but the project owner makes the
final decision.

## Package Location

Round root:

```text
pinn_instruction/markdown_conversion/framework-specs/postspec-r1/
```

Package files:

```text
postspec-r1/
  DELIVERY-NOTE.md
  research_package/
    RESEARCH-AGENT-PROMPT.md
    RESEARCH-CONTEXT-MASTER.md
    FRAMEWORK-SPECS-BUNDLE.md
```

The external agent receives two attachments:

1. `RESEARCH-CONTEXT-MASTER.md`
2. `FRAMEWORK-SPECS-BUNDLE.md`

`RESEARCH-AGENT-PROMPT.md` is pasted into the external agent conversation.
`DELIVERY-NOTE.md` is user-only and is not uploaded.

## Context Strategy

The package intentionally consolidates context to reduce upload friction.

`RESEARCH-CONTEXT-MASTER.md` carries:

- current project-state summary;
- owner intent;
- ERW channel standing;
- EDL and Trainex context;
- strategic evaluation lens;
- report failure modes to avoid;
- output contract and style expectations.

`FRAMEWORK-SPECS-BUNDLE.md` carries the three framework specs in one attachment:

- `ctl_instruction.md`
- `pinn_architecture.md`
- `sampling_method.md`

The specs are included because they are the best available representation of
the current framework. The context master should orient the agent; it should not
try to paraphrase the framework in enough detail to replace the specs.

## Output Design

The research result should be polished, human-readable, and friendly to read.
The requested source format is PDF-ready Markdown, with an optional PDF export
if the external agent supports it.

Markdown is preferred as the durable source because it preserves headings,
citations, and later consolidation/editing. PDF is welcome as a presentation
format, but not as the only output.

Required report shape:

```text
Title
Executive Summary
Current-State Diagnosis
Strategic Evaluation Lens Applied
Candidate Direction Assessment
Recommended Direction of Travel
Why This Direction Is Better Than The Alternatives
What Not To Work On Yet
Key Risks and Unknowns
Closing Recommendation
References / Source Notes
```

The report should be clear, organized, and readable. It should not produce
fine-grained gates, checklists, or a task-by-task plan.

## Strategic Evaluation Lens

The prompt should evaluate next-stage directions by how well they:

1. Reduce the largest risk before full-scale implementation.
2. Create useful evidence without requiring the whole system to be built first.
3. Preserve momentum after a long spec-heavy period.
4. Avoid premature engineering detail.
5. Avoid false certainty where sources or evidence are unsettled.
6. Fit a single-machine, non-expert-operator project reality.
7. Clarify what broad class of work should come next.

This replaces a reactive "information that would change this recommendation"
section. The package should improve the answer up front by telling the research
agent what a good strategic answer optimizes for.

## Candidate Directions

The package names two visible candidate directions:

- EDL-first: use the Empirical Decision Loop to run small research/probe cycles
  before full implementation.
- Trainex-first: prioritize the training-execution / reality-pipeline track.

The package must not force a binary choice. The agent is explicitly encouraged
to propose a hybrid direction, a third path, or a reframing.

## Success Criteria

The package is ready when:

- the two uploaded files exist and are self-contained;
- the paste-ready prompt names exactly those two attachments;
- the framework specs are present in the bundle;
- the context master describes project state, EDL, Trainex, owner intent,
  evaluation lens, and output contract;
- the delivery note gives user-only routing and handoff instructions;
- validation confirms there are no accidental repo paths in uploaded authored
  context outside the verbatim framework-spec snapshot material.
