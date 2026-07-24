---
title: Trainex R2 Delivery Note (single sub-package)
package_for: trainex-r2 (single sub-package)
role: user-facing handoff and routing instructions — NOT part of any upload to external agents
status: active
created: 2026-07-24
---

# Trainex R2 Delivery Note

**This file stays in the repository. Do NOT send it to external research agents.**
It carries repository paths and routing context that mean nothing outside the
codebase. The authored uploads — `RESEARCH-CONTEXT-MASTER.md`,
`framework-specs-bundle.md`, `run-evidence-bundle.md` — contain **no** repo
paths and refer to companion files by bare filename only. `44-DIAGNOSIS.md` is a
**verbatim pin** of a project document and intentionally retains its internal
cross-references; the master instructs agents to treat any unattached reference
as unavailable rather than guessing (D-08, D-11).

## The package

trainex-r2 is delivered as a **single sub-package** (D-01): five research
questions is under the ~6–7-item split threshold (ERW Rule 10), the questions
share one coherent output contract and one centerpiece (`44-DIAGNOSIS.md`), so
one package keeps them mutually consistent.

The five question areas: (Q1) training budget/steps; (Q2) warmup + learning-rate
schedule; (Q3) loss weighting/balancing — including the normalization/data-scale
sub-facet; (Q4) Stage-0 curriculum pacing; (Q5) evaluation policy.

**Purpose:** this package hands the training-recipe questions raised by the v2.0
Stage-0 pilot's physics-gate failure to external research agents, so their
returned resolution doc can serve as a **candidate verdict source** for the
*next* milestone's owner-adjudicated remedy selection. It does not select (or
even recommend) a remedy (SCOPE-26).

Package root: `pinn_instruction/markdown_conversion/framework-specs/trainex-r2/`

## What to send to each external research agent

Open `research_package/RESEARCH-AGENT-PROMPT.md`. Attach exactly these **four
individual files** (upload files individually — no folders):

1. `pinn_instruction/markdown_conversion/framework-specs/trainex-r2/research_package/RESEARCH-CONTEXT-MASTER.md`
2. `pinn_instruction/markdown_conversion/framework-specs/trainex-r2/research_package/44-DIAGNOSIS.md`
3. `pinn_instruction/markdown_conversion/framework-specs/trainex-r2/specs/framework-specs-bundle.md`
4. `pinn_instruction/markdown_conversion/framework-specs/trainex-r2/research_package/run-evidence-bundle.md`

Then paste the prompt body (everything below the horizontal rule in
`RESEARCH-AGENT-PROMPT.md`) into the conversation.

**Cap arithmetic (ERW Rule 15):** these are **4 uploads of the at-most-5 hard
cap** — one slot of headroom. A fifth attachment requires explicit owner
override, and any additional source material must be **bundled into the existing
bundles** (`framework-specs-bundle.md` / `run-evidence-bundle.md`), never added
as new attachments (D-02 + Rule 4). The prompt file itself is **pasted as text,
never uploaded** — it does not count against the cap.

## Provenance

- **Package baseline (`source_baseline`):**
  `9b1f0e7a4735df1c54867530cfd1f13b390e1514` — the repository commit at package
  assembly (recorded in the frontmatter of every authored upload and in the
  `45-01-SUMMARY.md`).
- **Complementary diagnosis evidence pin:** the snapshotted diagnosis carries
  its own deeper evidence pin in its §8 — its 15 analysis inputs are pinned by
  SHA-256 at commit `8631576dc5d8f76d1d0b301895ec5014161941cc`
  (`cross_check.all_match: true`). The two pins are complementary (package
  baseline vs diagnosis evidence tree).

**Pre-delivery freshness procedure (run before actual handoff; ERW Rule 5,
RESEARCH Pitfall 8):** verify no snapshotted source drifted after
`source_baseline`. For each source path —
`.planning/phases/44-physics-gate-forensics/44-DIAGNOSIS.md` and its `evidence/`,
`.planning/milestones/v2.0-phases/43-verification-stage-0-pilot-acceptance/43-CALIBRATION.md`
and `43-VERDICT.md`, `runs/stage0-pilot-seed42/evaluation/*`, and
`pinn_instruction/markdown_conversion/framework-specs/{ctl_instruction,pinn_architecture}.md`
— run `git diff 9b1f0e7a4735df1c54867530cfd1f13b390e1514 -- <path>`. If any path
drifted, refresh the affected snapshot/bundle and re-pin `source_baseline`. If
any package file was touched after the Plan 45-04 audit, re-run the audit greps
before sending.

## Scope notes (the standing boundaries, in plain terms)

- **No held-out evaluation** is performed or requested — the evaluator budget is
  exhausted (two failed attempts plus one completed FAIL, audited in
  `43-VERDICT.md`); any future evaluation requires a new, explicitly changed
  owner policy and a separately governed evidence boundary (SCOPE-22; Q5 asks
  *about* that governance, it does not trigger it).
- **No training runs** and **no executed discriminating tests** — they appear in
  the package as proposed, owner-authorization-gated research directions only
  (SCOPE-23).
- **No framework-spec edits** — `ctl_instruction.md` and `pinn_architecture.md`
  are read-only excerpt sources; the package carries verbatim excerpts, never
  edits (SCOPE-24).
- **No Stage-1 / PLAT-01..07 work** (SCOPE-25).
- **No remedy is selected** by anyone but the owner — the questions stay neutral;
  the external report is research input, never a verdict (SCOPE-26, D-14).

## Result delivery conventions

1. Each agent's result lands at
   `pinn_instruction/markdown_conversion/framework-specs/trainex-r2/research_results/<agent>-resolution.md`
   (e.g. `chatgpt-pro-resolution.md`, `gemini-deep-research-resolution.md`).
2. Consolidation (reusing the issue-02 consolidation workflow / bundle tooling
   if desired) produces
   `pinn_instruction/markdown_conversion/framework-specs/trainex-r2/trainex-r2-resolution-doc.md`
   at the package root — **that file intentionally does not exist yet** and is
   not created by this phase.
3. **Expected return format:** individual per-agent reports consolidated into
   **one** resolution document (v1.4/v1.5/v1.6 precedent, PKG-11). Check the
   master's output contract (§7) for the per-question + gaps structure each
   report should follow so consolidation is clean.

## Standing of the eventual resolution doc

The eventual `trainex-r2-resolution-doc.md` is a **candidate verdict source**
for the **next** milestone's owner-adjudicated remedy selection (SCOPE-26). It
is **never authoritative**: the full verification protocol applies before any of
it is transcribed into framework specs. Delivery of this package **closes the
v2.1 milestone** and opens the external research gate; the returning resolution
doc gates the *next* milestone, not this one.

## Owner decisions to record at assembly (D-13)

Two carried-forward todos are **owner-decided** and must be surfaced at the
Plan 45-04 checkpoint — the agent does **not** pre-select either. Both are
presented below as neutral A/B/C questions with **no** recommended marker,
ranking, or default (D-13 NON-DISCRETIONARY; RESEARCH Pitfall 6). Nothing in
this file concludes either question.

### Question 1 — `trainex-r1-research-handoff` (the r1b relationship)

The trainex-r1 round's R1b sub-package (runbook/ops knowledge: K1 health
watchlist, K2 unattended-Mac ops, K4 feasibility envelope, K5 verification
ladder, K3 runbook patterns) has not yet returned; R1a has. The owner decides
how (if at all) the r1b findings relate to the trainex-r2 package.

- **(A)** r1b's K-series findings are **independent** of the trainex-r2
  training-recipe questions — no linkage; deliver trainex-r2 as-is.
- **(B)** specific r1b findings (e.g. K1 divergence-after-transition health
  signals) are relevant context for Q2/Q4 and should be **referenced in the
  package** per owner direction (the owner names which findings and how).
- **(C)** the r1b handoff **completes first**, as a soft precondition on
  trainex-r2 delivery.

**Owner's pick: PENDING (recorded at the Plan 45-04 checkpoint).**

### Question 2 — `d-06-static-epsilon-sensitivity-check` (inclusion)

This is the one open follow-up from the v1.6/Phase-32 D-06 (epsilon strategy)
adjudication — a verification that the locked dual-epsilon choice
(`epsilon_train = 1e-5` in the training loss; `epsilon_inv = 1e-10` for offline
ground-truth invariants) is safe on the real data. It is a spec-side /
verification item, not a training-recipe question. The owner decides whether it
enters trainex-r2.

- **(A)** **include as a 6th research question** — this requires an explicit
  owner override of the locked five-question set (D-05).
- **(B)** **do not include** — it is scoped to the future data-pipeline build;
  keep it a later-triggered verification item (its own todo).
- **(C)** **mention in the package as related-but-out-of-scope context**, not
  posed as a question.

**Owner's pick: PENDING (recorded at the Plan 45-04 checkpoint).**
