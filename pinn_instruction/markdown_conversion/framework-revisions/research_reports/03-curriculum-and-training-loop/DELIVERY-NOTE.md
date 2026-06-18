---
title: doc-03 Research Package — Delivery Note
package_for: doc-03 (curriculum + training loop)
status: active
purpose: other
created: 2026-06-18
milestone: v1.6
phase: research-package-assembly
audience: user-only — NEVER uploaded to the external research
retirement_trigger: the doc-03 resolution doc has landed and Phase 31 readiness has passed
---

# doc-03 Research Package — Delivery Note

This note hands off the doc-03 ("Curriculum and Training Loop") research package for
external multi-AI research (the ERW workflow). It is **user-only** and is **never
uploaded** to the external research — it is the one file in this round that names
repository paths (the routing lives here so the uploaded package stays repo-blind). On the
commit that delivers this package, the milestone enters the external resolution-doc gate:
the user's multi-AI research begins.

## How To Use This Package

The uploaded package lives in the `research_package/` subdirectory of this round. It is
self-contained — every file an external researcher needs is shipped inside it, and the
researcher works only from the attached files (no repository access). Read it in this
order:

1. **`research_package/RESEARCH-CONTEXT-MASTER.md`** — the single uploaded entry point.
   Orientation only: the source-treatment preamble (how to weigh each input) and the
   per-file manifest (what every file is). This is a **multi-companion** package — the
   master references its companions by bare filename and does not fold them.
2. **`research_package/RESEARCH-AGENT-PROMPT.md`** — the paste-ready prompt. Its header
   lists exactly which files to attach (by bare filename); below the rule is the verbatim
   prompt. The prompt ships with the master — a package without its prompt is incomplete.
3. **`research_package/scope-12-hard-constraints.md`** — the locked v1.4 + v1.5 outcomes
   (hard constraints, not open questions).
4. **`research_package/framed-research-questions.md`** — the questions to answer.
5. **`research_package/claims-register.md`** and
   **`research_package/verified-facts-reference.md`** — the figure-grounding companions.
6. **`research_package/resolution-doc-skeleton.md`** — the non-binding coverage skeleton.
7. **`research_package/specs/*.md`** — the byte-for-byte source snapshots (the issue doc,
   the two spec-edit targets, the FROZEN sampling spec, the two baseline-critique reports,
   and the minimal consolidated dataset context).

To run the handoff: attach the full set listed in the prompt's header to the external AI
agent(s), paste the prompt, and collect each agent's resolution into the user's
multi-AI synthesis. The issue doc and its "Recommended Resolutions" are non-authoritative;
the framework specs are the source of truth; the live implementation-code "Canonical"
citations are overridden (SCOPE-10).

## Where The Resolution Doc Lands

The resolution doc produced by the external research must land under exactly:

`pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/`

Phase 31 (resolution-doc readiness verification) and the downstream adjudication phases
read it from that path. A resolution doc placed anywhere else will not be picked up.

## Resolution-Doc Format

There is **no required schema** and no prescribed structure. The resolution doc is the
user's product. Two prior resolution docs are offered as **format precedents only** — a
suggestion, not a template:

- v1.4's `ctl_pinn_resolution.md` (under
  `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/`)
- v1.5's `02-resolution-doc.md` (under
  `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/`)

The non-binding `resolution-doc-skeleton.md` shipped in the package mirrors the framed
questions for coverage-checking only; it mandates nothing.

## No In-Milestone Verification (the key v1.6 ≠ v1.5 difference)

**v1.6 has no parallel empirical-verification phase — there is no Phase-24 analog.** In
v1.5 a dedicated phase (Phase 24) re-verified every claimed figure in the package while the
external-research gate was open. v1.6 has nothing equivalent: doc-03's dataset facts were
settled in v1.5, and the remaining empirical work is deferred to FUT (FUT-01 / FUT-02 /
FUT-04). Consequently, **no phase in this milestone verifies any `claimed-unverified`
figure in the package.** Those figures are unverified inputs — they are not treated as
fact, and any figure that would gate a verdict is flagged in the claims register for a
future FUT empirical check. The package carries this boundary honestly; do not expect an
in-milestone phase to confirm a package figure.

## The Gate

Phases 32–36 (evidence ledger + conflict adjudication, the CURR / LOOP / LOSS contract
phases, and the VER acceptance/handoff phase) gate on **both** of the following:

1. The consolidated resolution doc landing at
   `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/`, AND
2. **Phase 31 (resolution-doc readiness verification) passing.**

Stated plainly: **Phases 32–36 gate on the consolidated doc landing AND Phase 31 passing.**
Neither condition alone unblocks the adjudication phases. Until both are met, no verdict is
adjudicated and no framework spec (`ctl_instruction.md` / `pinn_architecture.md`) is edited.
