---
title: Issue-02 Research Package — Delivery Note
package_for: issue-02
created: 2026-06-10
---

# Issue-02 Research Package — Delivery Note

This note hands off the issue-02 ("Data Pipeline and Validation") research package for
external multi-AI research. On the commit that delivers this package, the milestone enters
the external resolution-doc gate: the user's multi-AI research begins, and Phase 24 (empirical
dataset verification) starts in parallel.

## How To Use This Package

The package is self-contained — every file an external researcher needs is a sibling in this
directory. Read it in this order:

1. **`RESEARCH-CONTEXT-MASTER.md`** — the research-context master and single entry point
   (consolidated 2026-06-11 from the package's former `README.md`,
   `framed-research-questions.md`, `claims-table.md`, `consolidated-context.md`, and
   `ERRATUM-2026-06-10.md`). Its sections, in reading order:
   - **Package Orientation And Manifest** — file roles, provenance, and source-treatment
     conventions. Read it first so you know which files are authoritative (the framework
     specs) and which are not (the issue doc, the DQA report).
   - **Framed Research Questions** — the task list. Every contested or unverified in-scope
     finding is posed as an explicit, neutral question. This is what the research must answer.
   - **CLM Claims Register** — the factual baseline. Every dataset figure carries a stable CLM
     ID and a `claimed-unverified` / `verified` status. Treat figures as claims, not facts,
     unless the CLM row is marked `verified`.
   - **Consolidated Dataset Context** — scattered dataset facts gathered into one place, each
     fragment labeled with its source path.
   - **Correction Provenance And Verification Boundaries** — the package's correction history
     and what remains unverified.
2. **`specs/*.md`** — the source-of-truth conventions. `ctl_instruction.md` and
   `pinn_architecture.md` carry the locked v1.4 contracts the research must respect as hard
   constraints; `sampling_method.md` and `data_quality_assessment.md` are context (FROZEN and
   non-authoritative respectively — see the master's manifest).

The issue doc and its "Recommended Resolutions" are non-authoritative and may contain errors;
do not treat them as settled. The `pinn/` "Canonical" citation in the issue doc is overridden
(SCOPE-10) — the framework specs are the source of truth.

## Where The Resolution Doc Lands

The resolution doc produced by the external research must land under exactly:

`pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/`

Phases 25–29 read it from that path. A resolution doc placed anywhere else will not be picked
up by the adjudication phases.

## Resolution-Doc Format

v1.4's `ctl_pinn_resolution.md` (under `research_reports/01-architecture-and-physics-foundations/`)
is offered as a **format precedent only** — a suggestion, not a required schema. The resolution
doc is the user's product; there is **no required schema** and no prescribed structure. The
format precedent is there to inspire, not to constrain.

## Phase 24 Runs In Parallel

Phase 24 (empirical dataset verification) starts immediately and runs **in parallel** with this
external-research gate window. It gates on nothing external. Phase 24 verifies every CLM row in
the master's **CLM Claims Register** section against the on-disk dataset and forwards a
**DATA-07 correction addendum**, keyed by CLM ID, for any package-stated claim that
verification contradicts. The addendum is a standalone sibling file; it supersedes the
master's **Correction Provenance And Verification Boundaries** section for any claim it
covers. If nothing is
contradicted, the addendum is nil. The addendum is forwarded to the in-flight external research
so the researchers can correct any figure the package got wrong.

## The Phase 25–29 Gate

Phases 25–29 (evidence framework, ingestion/selection, sampling/precision/global-scale,
validation-metrics, and acceptance/handoff — all adjudication and spec-edit work) gate on
**both** of the following:

1. The resolution doc landing at
   `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/`, AND
2. Phase 24 completion.

Neither condition alone unblocks the adjudication phases. Until both are met, no verdict is
adjudicated and no framework spec (`ctl_instruction.md` / `pinn_architecture.md`) is edited.
