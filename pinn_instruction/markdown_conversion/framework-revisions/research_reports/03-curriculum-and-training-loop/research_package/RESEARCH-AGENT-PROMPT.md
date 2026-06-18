---
title: doc-03 Research Agent Prompt
package_for: doc-03 (curriculum + training loop)
role: paste-ready prompt + six-file attach-list header; prompt is pasted separately
status: active
created: 2026-06-18
---

# doc-03 Research Agent Prompt

This file is pasted into the external AI agent separately; it is not counted as an
uploaded file. The header below tells you which six files to attach from the package's
`upload/` directory. Below the horizontal rule is the verbatim, paste-ready prompt.

## Attach these files (by bare filename)

Attach **all six** of the following files to the external research agent. They are the
complete upload package:

- `RESEARCH-CONTEXT-MASTER.md` — read first; uploaded entry point and manifest
- `TASK-AND-CONSTRAINTS-BUNDLE.md` — hard constraints, framed questions, and the
  non-binding resolution skeleton
- `CLAIMS-AND-FACTS-BUNDLE.md` — claimed-vs-verified figure register, v1.5 verified
  anchors, and minimal consolidated dataset context
- `03-curriculum-and-training-loop.md` — issue doc snapshot; non-authoritative
  adjudication subject
- `FRAMEWORK-SPECS-BUNDLE.md` — framework spec snapshots, bundled byte-identically for
  transport
- `BASELINE-REPORTS-BUNDLE.md` — baseline design-intent reports, bundled byte-identically
  for transport

---

You are a research agent adjudicating the open questions for the "Curriculum and Training
Loop" (doc-03) revision of a physics-informed neural-network (CTL-PINN) framework. **You
work from the attached files only.** You have no repository access; every input you need is
attached. Do not assume, invent, or fetch any file, path, or figure that is not in the
attached set.

Read `RESEARCH-CONTEXT-MASTER.md` first. Then read
`TASK-AND-CONSTRAINTS-BUNDLE.md`; inside it, read `scope-12-hard-constraints.md` before
`framed-research-questions.md`. Use `CLAIMS-AND-FACTS-BUNDLE.md` to ground every figure,
and use the issue doc, framework-spec bundle, and baseline-report bundle as the questions
direct you.

Honor these treatment rules:

- **The issue doc (`03-curriculum-and-training-loop.md`) and its "Recommended Resolutions"
  are non-authoritative and may contain errors.** Adjudicate its findings; do not transcribe
  its proposals as decisions. The worked example is the `D` conflict: the issue doc's
  `D = 6.694` conflicts with the locked raw-mass `D ≈ 4.6416` — the locked value stands (see
  `scope-12-hard-constraints.md` item 6 and `claims-register.md` CLM-01/CLM-19 inside the
  attached bundles).
- **The framework specs (`ctl_instruction.md`, `pinn_architecture.md`) are the source of
  truth.** Where the issue doc cites live implementation code as "Canonical", that citation
  is overridden — the specs are authoritative instead (`scope-12-hard-constraints.md` §2).
- **The hard constraints in `scope-12-hard-constraints.md` (items 1–7) are fixed.** Do not
  re-open or contradict them. Reconcile your answers *under* them. The current doc-03
  positions in the specs (curriculum staging, batch construction, stage transitions, loss
  scaling, the `τ_L`/`L_max` formulas, gradient clipping) are the **revisable baseline** —
  those you may propose changes to.
- **Figures are claims unless `verified`.** Reference each figure by its `CLM-NN` ID from
  `claims-register.md`. No in-milestone phase verifies the `claimed-unverified` figures —
  treat them as unverified inputs, not facts.

Answer each question in `framed-research-questions.md` inside
`TASK-AND-CONSTRAINTS-BUNDLE.md`. For each: state your finding, cite which attached files
(and which sections) you relied on, and identify conflicts and uncertainty explicitly.
Where the attached materials are **silent or ambiguous**, say so and **log the gap in the
claims register rather than inventing an answer** — record what is missing and what would
resolve it. "Insufficient evidence" is an acceptable, honest finding. Do not force a
resolution where the sources do not support one.

The `resolution-doc-skeleton.md` section inside `TASK-AND-CONSTRAINTS-BUNDLE.md` is offered
only to ease coverage-checking and is non-binding — you may structure your resolution
however you prefer; the cited resolution docs are format precedents, not a required schema.
