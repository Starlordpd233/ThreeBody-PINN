---
title: doc-03 Research Context Master
package_for: doc-03 (curriculum + training loop)
role: single uploaded entry point — source-treatment preamble + per-file manifest + reading order (PKG-05/06/07 orientation)
status: active
created: 2026-06-18
source_baseline: 3781d1a68a9364717d399e536b7fc9ad56e19645
self_contained: true
form: multi-companion (the master references companions by bare filename; it never folds them)
---

# doc-03 Research Context Master

This file is the single research-context entry point for the doc-03 ("Curriculum and
Training Loop") external-research package. It orients a repo-blind external researcher:
it states how to treat each input (which files are authoritative and which are not), it
indexes every file shipped in this package by bare filename with its role and treatment,
and it gives the reading order. It does **not** restate the questions, the constraints,
the figures, or the dataset facts — those live in their own companion files, referenced
here by bare filename. **This is a multi-companion package: the master points at the
companions; it does not fold them.**

The package is **self-contained**. Every file named below is shipped in this package
(either in this directory or in its `specs/` subdirectory). The external researcher is
assumed to have **no repository access** and works only from the attached files. The
authored entry points — this master and `RESEARCH-AGENT-PROMPT.md` — name no repository
path; the grounding companions (`claims-register.md`, `verified-facts-reference.md`,
`consolidated-context.md`) retain repo-relative provenance *labels* by design
(non-navigable, for v1.5 traceability — see those files' headers). No uploaded file points
a repo-blind agent at a path that would dangle without repository access; repository
routing lives only in the never-uploaded delivery note.

## Reading order

Read the package in this order:

1. **This master** — orientation: the source-treatment preamble (how to weigh each input)
   and the per-file manifest (what every file is). Read it first.
2. **`RESEARCH-AGENT-PROMPT.md`** — the paste-ready prompt. Its header lists exactly which
   files to attach; below the rule is the verbatim task prompt. A package without its
   prompt is incomplete — they ship together.
3. **`scope-12-hard-constraints.md`** — the fixed, already-decided v1.4 + v1.5 outcomes.
   These are boundary conditions, not open questions. Read them before the questions so
   you know what may not be re-opened.
4. **`framed-research-questions.md`** — the task list. Every contested or unverified
   in-scope finding is posed as an explicit, neutral question (by issue-03's own section
   order). This is what the research must answer.
5. **`claims-register.md`** — the figure-grounding table. Every inline `CLM-NN` reference
   in the questions resolves to a row here, marked `claimed-unverified` or `verified`.
   Treat any `claimed-unverified` figure as a claim, not a fact.
6. **`verified-facts-reference.md`** — the v1.5-verified dataset anchors that the
   curriculum / training-loop contracts depend on (safe to rely on as fact).
7. **`resolution-doc-skeleton.md`** — a **non-binding** per-finding coverage skeleton. It
   carries the downstream finding → adjudication-phase mapping. No schema is mandated.
8. **`specs/` snapshots** — the byte-for-byte source documents (the issue doc, the two
   spec-edit targets, the FROZEN sampling spec, the two baseline-critique reports, and the
   minimal consolidated dataset context), read as the questions direct you to them.

---

## Source-Treatment Preamble

Read these conventions before using any file in this package. They govern how every input
is weighed; the verbatim hard constraints themselves are in `scope-12-hard-constraints.md`.

- **The issue doc is non-authoritative.** `03-curriculum-and-training-loop.md` (in
  `specs/`) is the adjudication subject, not a source of truth. Both its findings **and**
  its "Recommended Resolutions" may contain errors and must NOT be treated as settled. The
  worked example is the `D` conflict: the issue doc derives `D = 6.694`, which **conflicts
  with** the locked raw-mass `D ≈ 4.6416` (rejected by v1.5 Phase 25 EVID-10; see
  `scope-12-hard-constraints.md` item 6 and `claims-register.md` CLM-01/CLM-19). The research
  adjudicates such conflicts; it does not assume the issue doc is correct.

- **The framework specs are the source of truth.** `ctl_instruction.md` and
  `pinn_architecture.md` (in `specs/`) carry the locked v1.4 + v1.5 conventions and are
  the only spec-edit targets for downstream adjudication.

- **The live implementation-code "Canonical" citations are OVERRIDDEN.** The issue doc
  cites two live implementation files — `data-processing-pipeline-full.py` and
  `basic_architecture.py` — as "Canonical". Those citations carry **no authority** for
  this adjudication (the SCOPE-10 override; see `scope-12-hard-constraints.md` §2). The
  live implementation code is **not** a grounding source and is excluded from this package
  entirely; where the issue doc cites it, the framework specs are authoritative instead.

- **Locked hard constraints vs. revisable baseline.** Two categories of spec content
  travel here and must NOT be conflated. The SCOPE-12 outcomes in
  `scope-12-hard-constraints.md` (items 1–7) are **locked** — fixed, not re-openable. The
  **current doc-03 positions** in `ctl_instruction.md` / `pinn_architecture.md` on the
  training-loop contracts (curriculum staging, batch construction, stage transitions, loss
  scaling, the `τ_L` / `L_max` formulas, gradient clipping) are the **revisable baseline**
  — the genuinely-open spec-edit targets the resolution may change. Reconcile the baseline
  *under* the locked constraints, never against them.

- **Figures are claims until verified.** Every dataset / empirical figure stated anywhere
  in this package carries a stable `CLM-NN` ID in `claims-register.md` with status
  `claimed-unverified` or `verified`. No figure is fact unless its row is `verified`.
  **Unlike v1.5, v1.6 has no in-milestone phase that verifies these claims** — see the
  boundary statement in `claims-register.md`. `claimed-unverified` figures are unverified
  inputs; do not rely on them as fact.

- **Annotations live here, not in the snapshots.** The `specs/*.md` files are byte-for-byte
  intact copies. All role / FROZEN / non-authoritative / baseline-critique annotations live
  in this manifest's Treatment column, never inside the copied files.

---

## Per-File Manifest

This table records, for every file in this package, its role, the source commit it was
snapshotted from (where applicable), and how it should be treated. **Every file is
referenced by bare filename.** The "Source commit" column is a provenance label for
re-derivation by an agent that *does* have the repository; the external researcher does
not need it. Files marked "generated" are package artifacts authored during assembly and
have no single source commit. `specs/` snapshots are pinned package-wide to
`source_baseline` (frontmatter); the per-file commit is each source's last-touching commit.

### Authored upload companions (in this directory)

| Package file | Role | Source commit | Treatment |
|--------------|------|---------------|-----------|
| `RESEARCH-CONTEXT-MASTER.md` | This file — single uploaded entry point: source-treatment preamble + manifest + reading order | generated | Generated package artifact; orientation only (no folded content) |
| `RESEARCH-AGENT-PROMPT.md` | Paste-ready prompt + attach-list header; ships with the master | generated | Generated package artifact; the task prompt for the external agent |
| `scope-12-hard-constraints.md` | The locked v1.4 + v1.5 outcomes (SCOPE-12), verbatim — hard constraints, not questions | generated | Authored companion; fixed boundary conditions, not re-openable |
| `framed-research-questions.md` | The neutral framed questions (issue-03 section order) — the research task list | generated | Authored companion; questions only, no verdicts |
| `resolution-doc-skeleton.md` | NON-BINDING per-finding coverage skeleton + finding→phase map | generated | Authored companion; suggestion only, no schema mandated |

### Grounding-class companions (in this directory)

| Package file | Role | Source commit | Treatment |
|--------------|------|---------------|-----------|
| `claims-register.md` | Claimed-vs-verified figure register; resolves every inline `CLM-NN`; states the no-in-milestone-verification boundary | generated | Grounding companion; `verified` rows retain v1.5 provenance citations by design |
| `verified-facts-reference.md` | Standalone v1.5-verified dataset anchors the curriculum / training-loop contracts depend on | generated | Grounding companion; safe-as-fact v1.5 subset; retains internal source labels |

### `specs/` snapshots (in the `specs/` subdirectory)

| Package file | Role | Source commit | Treatment |
|--------------|------|---------------|-----------|
| `specs/03-curriculum-and-training-loop.md` | Adjudication subject — NON-authoritative; carries the `D = 6.694` claim and the overridden "Canonical" citations | `d43afcd69af027e0689f42ac61e130f8497939f8` | Byte-for-byte intact snapshot |
| `specs/ctl_instruction.md` | Spec-edit target; carries curriculum staging, `τ_L`/`L_max`, s_min gate, loss scaling, PHYS-01 `D ≈ 4.6416` | `3781d1a68a9364717d399e536b7fc9ad56e19645` | Byte-for-byte intact snapshot |
| `specs/pinn_architecture.md` | Spec-edit target; carries gradient-clipping / training-strategy contracts | `ea2af12348b6fd95521e0e4c251c92a0160030cf` | Byte-for-byte intact snapshot |
| `specs/sampling_method.md` | FROZEN (SCOPE-08); historical record of dataset generation; not a revision target | `916d3f84ad7282c1f8ace45901441f7d3ac054ca` | Byte-for-byte intact snapshot |
| `specs/review_of_framework.md` | Baseline design intent; ships WITH a baseline-critique mandate; the broadest doc-03-relevant report | `6ab19ea3f8f9248578296472f75b659a8e5b19a4` | Byte-for-byte intact snapshot |
| `specs/stage_strat_revision.md` | Baseline design intent; ships WITH a baseline-critique mandate; the stage-assignment deep-dive | `2f952cf0154b40e054287902716f16f8d50db576` | Byte-for-byte intact snapshot |
| `specs/consolidated-context.md` | Minimal consolidated dataset context (v1.5 facts + minimal excerpts); retains internal source labels | generated | Snapshot-class grounding companion; not a framework spec (never consolidated those) |

**Package-wide pin.** All `specs/` snapshots were taken against project state
`source_baseline` (frontmatter); each row's "Source commit" records that source file's own
last-touching commit. The framework specs (`ctl_instruction.md`, `pinn_architecture.md`,
`sampling_method.md`) are copied byte-for-byte intact and were **never** consolidated,
excerpted, or summarized.

### Baseline-critique mandate (the two reports)

`review_of_framework.md` and `stage_strat_revision.md` ship as **baseline design intent**,
not as hard constraints. They are research reports — useful, detailed, and the deepest
written articulation of several doc-03 positions, but non-authoritative. The research is
**mandated to critique them**: where a report proposes a methodology or value, treat it as
a baseline to evaluate (via an explicit option-vs-baseline comparison), not as settled law.
Their recommended package role is confirmed in the phase's reports characterization.

### Self-Contained Guarantee

Every file named in this manifest is shipped inside this package — in this directory or in
its `specs/` subdirectory. No entry above is a navigable link out of the package, and no
uploaded file points a repo-blind agent at a repository path that would dangle without
repository access. Repository routing exists in exactly one file — the never-uploaded
delivery note — which is **not** part of this manifest and is **not** uploaded to the
external research.
