---
title: Issue-02 Research Package — Manifest & Index
package_for: issue-02
created: 2026-06-10
source_commit: 96f9150a02919d492a86ef9f63e10e5942d2d8e3
self_contained: true
---

# Issue-02 Research Package — Manifest & Index

This file is the index for the issue-02 ("Data Pipeline and Validation") external-research
package. It records, for every file in this package, its role annotation, its canonical
source path inside the project repository, the source commit hash it was snapshotted from,
and how it should be treated. Read this manifest first, then the delivery note
(`DELIVERY-NOTE.md`), then the framed research questions (`framed-research-questions.md`).

The package is **self-contained**: every file referenced here is a sibling file inside this
package directory. Source paths in the manifest are provenance labels (where the file came
from in the project repository), not navigation links — the external researcher is assumed to
have no repository access and works only from the snapshot copies shipped here.

## Source-Treatment Preamble

Read these conventions before using any file in this package:

- **The issue doc is non-authoritative.** `specs/02-data-pipeline-and-validation.md` is the
  adjudication subject, not a source of truth. Both its findings **and** its "Recommended
  Resolutions" may contain errors and must NOT be treated as settled. The worked example of
  this is the known seed conflict: the issue doc's ratio-based SCS thresholds (`> 1e-6` /
  `< 1e-8`) conflict with the locked post-v1.3 gate (`epsilon_H > 1e-5` / `SCS > -5`). The
  external research adjudicates such conflicts; it does not assume the issue doc is correct.
- **The framework specs are the source of truth.** `specs/ctl_instruction.md` and
  `specs/pinn_architecture.md` carry the locked v1.4 conventions (14D input contract, Jacobi
  IC13, mass-weighted COM projection head, PHYS-03 softening, PHYS-01 D convention, post-v1.3
  SCS gate). They are the only spec-edit targets for downstream adjudication.
- **The `pinn/` "Canonical" citation is OVERRIDDEN.** The issue doc cites
  `pinn/data-processing-pipeline-full.py` as "Canonical". That citation is **overridden** by
  the 2026-05-19 directive (SCOPE-10): live `pinn/` code is NOT a grounding source and is
  excluded from this package entirely. The framework specs are authoritative instead.
- **Figures are claims until verified.** Every dataset figure in this package is tracked in
  `claims-table.md` by a stable CLM ID with status `claimed-unverified` or `verified`. No
  figure is presented as fact unless its CLM row is marked `verified`. Phase 24 verifies every
  row regardless of status.
- **Annotations live here, not in the snapshots.** The `specs/*.md` files are byte-for-byte
  intact copies. All role / FROZEN / non-authoritative annotations live in this manifest's
  Role annotation column, never inside the copied files (D-03).

## Per-File Manifest

| Package file | Role annotation | Canonical source path | Source commit hash | Treatment |
|--------------|-----------------|-----------------------|--------------------|-----------|
| `specs/02-data-pipeline-and-validation.md` | NON-authoritative; adjudication subject | `pinn_instruction/issues/02-data-pipeline-and-validation.md` | `d43afcd69af027e0689f42ac61e130f8497939f8` | Byte-for-byte intact snapshot |
| `specs/ctl_instruction.md` | Spec-edit target; D-03 byte-for-byte; carries 14D input contract, Jacobi IC13, PHYS-01 D convention | `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` | `192c7c3c55ca0730c34ce708abf24c613234dd2e` | Byte-for-byte intact snapshot |
| `specs/pinn_architecture.md` | Spec-edit target; D-03 byte-for-byte; carries COM projection head, PHYS-03 softening, loss contracts | `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` | `192c7c3c55ca0730c34ce708abf24c613234dd2e` | Byte-for-byte intact snapshot |
| `specs/sampling_method.md` | FROZEN (SCOPE-08); historical record of dataset generation; not a revision target | `pinn_instruction/markdown_conversion/framework-specs/sampling_method.md` | `916d3f84ad7282c1f8ace45901441f7d3ac054ca` | Byte-for-byte intact snapshot |
| `specs/data_quality_assessment.md` | Research report, NOT an authoritative spec (SCOPE-09); non-authoritative; sole written home of the post-v1.3 SCS gate + metric definitions | `pinn_instruction/markdown_conversion/framework-revisions/data_quality_assessment.md` | `d3fcff99268b4493629eb2f0fe580f43c51ec019` | Byte-for-byte intact snapshot |
| `consolidated-context.md` | Scattered dataset fragments, each labeled with its source path (D-05) | generated in Phase 23 | package commit | Generated package artifact |
| `claims-table.md` | Claims register (PKG-03); every dataset figure with a stable CLM ID + status | generated in Phase 23 | package commit | Generated package artifact |
| `framed-research-questions.md` | Neutral framed research questions (PKG-02); the external-research task list | generated in Phase 23 | package commit | Generated package artifact |
| `DELIVERY-NOTE.md` | Handoff / gate-open delivery note (D-16) | generated in Phase 23 | package commit | Generated package artifact |
| `README.md` | This manifest / index (PKG-01) | generated in Phase 23 | package commit | Generated package artifact |

**Package-wide pin:** all snapshots were taken against project state `96f9150a02919d492a86ef9f63e10e5942d2d8e3`; per-file hashes above record each source file's own last-touched commit.

## Self-Contained Guarantee

Every file named in this manifest is a sibling inside this package directory
(`research_package/` and its `specs/` subdirectory). No entry above is a navigable link out of
the package, and no in-package file points a repo-blind agent at a project path that would
dangle without repository access. The canonical source paths in the manifest are recorded
solely for provenance and re-derivation by an agent that *does* have the repository; the
external researcher does not need them to use the package.
