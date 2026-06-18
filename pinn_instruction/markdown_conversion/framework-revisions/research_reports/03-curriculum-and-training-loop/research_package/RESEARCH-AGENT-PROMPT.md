---
title: doc-03 Research Agent Prompt
package_for: doc-03 (curriculum + training loop)
role: paste-ready prompt + attach-list header; ships with RESEARCH-CONTEXT-MASTER.md
status: active
created: 2026-06-18
---

# doc-03 Research Agent Prompt

This file ships with `RESEARCH-CONTEXT-MASTER.md`; a package without its prompt is
incomplete. The header below tells you which files to attach to the external AI agent.
Below the horizontal rule is the verbatim, paste-ready prompt.

## Attach these files (by bare filename)

Attach **all** of the following to the external research agent. Every file is in this
package; attach them as a set:

**Entry point and authored companions**

- `RESEARCH-CONTEXT-MASTER.md` — read first (orientation: source-treatment preamble +
  manifest + reading order)
- `scope-12-hard-constraints.md` — the locked v1.4 + v1.5 outcomes (hard constraints)
- `framed-research-questions.md` — the questions to answer
- `resolution-doc-skeleton.md` — the non-binding coverage skeleton (suggestion only)

**Grounding companions**

- `claims-register.md` — the claimed-vs-verified figure register (resolves every `CLM-NN`)
- `verified-facts-reference.md` — the v1.5-verified dataset anchors

**`specs/` snapshots**

- `03-curriculum-and-training-loop.md` — the issue doc (non-authoritative adjudication
  subject)
- `ctl_instruction.md` — spec-edit target (source of truth)
- `pinn_architecture.md` — spec-edit target (source of truth)
- `sampling_method.md` — FROZEN; historical record (context only)
- `review_of_framework.md` — baseline design intent (critique mandate)
- `stage_strat_revision.md` — baseline design intent (critique mandate)
- `consolidated-context.md` — minimal consolidated dataset context

---

You are a research agent adjudicating the open questions for the "Curriculum and Training
Loop" (doc-03) revision of a physics-informed neural-network (CTL-PINN) framework. **You
work from the attached files only.** You have no repository access; every input you need is
attached. Do not assume, invent, or fetch any file, path, or figure that is not in the
attached set.

Read the attached files in this order: read `RESEARCH-CONTEXT-MASTER.md` first (it tells
you how to treat each input), then `scope-12-hard-constraints.md`, then
`framed-research-questions.md`. Use `claims-register.md` and `verified-facts-reference.md`
to ground every figure, and the `specs/` snapshots as the questions direct you.

Honor these treatment rules:

- **The issue doc (`03-curriculum-and-training-loop.md`) and its "Recommended Resolutions"
  are non-authoritative and may contain errors.** Adjudicate its findings; do not transcribe
  its proposals as decisions. The worked example is the `D` conflict: the issue doc's
  `D = 6.694` conflicts with the locked raw-mass `D ≈ 4.6416` — the locked value stands (see
  `scope-12-hard-constraints.md` item 6 and `claims-register.md` CLM-01/CLM-19).
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

Answer each question in `framed-research-questions.md`. For each: state your finding, cite
which attached files (and which sections) you relied on, and identify conflicts and
uncertainty explicitly. Where the attached materials are **silent or ambiguous**, say so
and **log the gap in the claims register rather than inventing an answer** — record what is
missing and what would resolve it. "Insufficient evidence" is an acceptable, honest finding.
Do not force a resolution where the sources do not support one.

The `resolution-doc-skeleton.md` is offered only to ease coverage-checking and is
non-binding — you may structure your resolution however you prefer; the cited resolution
docs are format precedents, not a required schema.
