---
title: doc-03 Research Context Master
package_for: doc-03 (curriculum + training loop)
role: uploaded entry point for the six-file transport package
status: active
created: 2026-06-18
updated: 2026-06-18
source_baseline: 522cea7182bf3d0e3206d8faa75150e705b174f0
self_contained: true
form: six-file upload package; prompt is pasted separately
---

# doc-03 Research Context Master

This is the entry point for the doc-03 ("Curriculum and Training Loop")
external-research package. The package has exactly six uploaded files. The
prompt is pasted separately and is not an attachment.

The package is self-contained. Work only from the six attached files. Do not
assume, invent, fetch, or request any file that is not attached. Some uploaded
files are mechanical bundles: content between BEGIN/END delimiters is
byte-identical to the named source part and was round-trip verified before
handoff. Treat bundled sections exactly as if the corresponding bare filename
had been attached separately.

## Reading Order

1. `RESEARCH-CONTEXT-MASTER.md` - this file.
2. `TASK-AND-CONSTRAINTS-BUNDLE.md` - hard constraints, framed questions, and
   the non-binding resolution skeleton.
3. `CLAIMS-AND-FACTS-BUNDLE.md` - claimed-vs-verified figure register,
   v1.5-verified dataset anchors, and minimal consolidated dataset context.
4. `03-curriculum-and-training-loop.md` - the issue doc, the adjudication
   subject.
5. `FRAMEWORK-SPECS-BUNDLE.md` - the framework spec snapshots.
6. `BASELINE-REPORTS-BUNDLE.md` - the baseline design-intent reports.

## Source-Treatment Preamble

- The issue doc is non-authoritative. Its findings and "Recommended
  Resolutions" may contain errors. Adjudicate them; do not treat them as
  settled.
- `ctl_instruction.md` and `pinn_architecture.md`, inside
  `FRAMEWORK-SPECS-BUNDLE.md`, are the framework spec-edit targets and the
  source of truth for downstream adjudication.
- The issue doc's implementation-code "Canonical" citations are overridden.
  The framework specs govern where those citations conflict with the package
  constraints.
- The hard constraints in `scope-12-hard-constraints.md`, inside
  `TASK-AND-CONSTRAINTS-BUNDLE.md`, are locked v1.4 + v1.5 outcomes. Do not
  re-open them.
- Current doc-03 positions in the framework specs on curriculum staging, batch
  construction, stage transitions, loss scaling, tau_L / L_max formulas, and
  gradient clipping are the revisable baseline. Reconcile any proposed changes
  under the locked constraints.
- Figures are claims until verified. Use `claims-register.md`, inside
  `CLAIMS-AND-FACTS-BUNDLE.md`, for every CLM-NN status. A
  `claimed-unverified` row is an input claim, not a fact.
- Annotations live in this master and in bundle wrapper tables, not inside the
  byte-identical bundled sections.

## Uploaded File Manifest

| Uploaded file | Contents | Treatment |
|---------------|----------|-----------|
| `RESEARCH-CONTEXT-MASTER.md` | This entry point | Orientation and source treatment only |
| `TASK-AND-CONSTRAINTS-BUNDLE.md` | `scope-12-hard-constraints.md`; `framed-research-questions.md`; `resolution-doc-skeleton.md` | Generated/source-authored package parts, bundled byte-identically for transport |
| `CLAIMS-AND-FACTS-BUNDLE.md` | `claims-register.md`; `verified-facts-reference.md`; `consolidated-context.md` | Grounding-class package parts; verified rows retain their provenance labels by design |
| `03-curriculum-and-training-loop.md` | Issue doc snapshot | Non-authoritative adjudication subject |
| `FRAMEWORK-SPECS-BUNDLE.md` | `ctl_instruction.md`; `pinn_architecture.md`; `sampling_method.md` | Byte-identical framework-spec snapshots; bundled for transport, not summarized |
| `BASELINE-REPORTS-BUNDLE.md` | `review_of_framework.md`; `stage_strat_revision.md` | Byte-identical baseline design-intent reports; critique mandate applies |

## Bundle Reading Rule

When a bundle contains multiple BEGIN/END sections, read the wrapper table first,
then read each enclosed section as its named file. The wrapper exists only to
reduce the upload count. It does not merge findings, change source standing, or
resolve conflicts between enclosed files.
