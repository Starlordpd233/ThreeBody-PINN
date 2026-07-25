---
plan: "45-03"
phase: 45-trainex-r2-erw-package-assembly
status: complete
completed: 2026-07-24
wave: 3
requirement: PKG-10
---

# 45-03 Summary — research-agent prompt and delivery-note draft

## What was built

The two routing artifacts that complete the assembled package: the paste-ready
`RESEARCH-AGENT-PROMPT.md` (PKG-10 — carries the D-04 neutral contract to the
external agent) and the user-only `DELIVERY-NOTE.md` draft (PKG-11/D-10 —
contents, upload list, provenance, return format, standing, and the two D-13
owner questions framed but NOT answered).

## Upload list (the 4 attachments)

Both the prompt header and the delivery-note "What to send" section name exactly
these four files (routing match confirmed):

1. `RESEARCH-CONTEXT-MASTER.md` (attachment 1 — entry point)
2. `44-DIAGNOSIS.md` (attachment 2 — verbatim diagnosis snapshot)
3. `framework-specs-bundle.md` (attachment 3 — locked spec excerpts)
4. `run-evidence-bundle.md` (attachment 4 — run evidence)

4 of the at-most-5 hard cap (ERW Rule 15); the prompt is pasted as text and
never uploaded.

## D-13 owner questions — both PENDING (D-13 NON-DISCRETIONARY)

Both carried-forward todos are framed as neutral A/B/C questions in
`DELIVERY-NOTE.md` §"Owner decisions to record at assembly", each with an
explicit **"Owner's pick: PENDING"** field and **no** recommended marker,
ranking, or default:

- **Question 1 — `trainex-r1-research-handoff`** (r1b relationship): (A)
  independent / no linkage; (B) reference specific r1b findings in the package
  per owner direction; (C) r1b completes first as a soft precondition.
- **Question 2 — `d-06-static-epsilon-sensitivity-check`** (inclusion): (A)
  include as a 6th question (owner override of the locked five-question set,
  D-05); (B) do not include (scoped to the future data-pipeline build); (C)
  mention as related-but-out-of-scope context.

Neither is pre-answered anywhere in the package. They surface at the Plan 45-04
checkpoint.

## source_baseline (matches 45-01 / 45-02)

`source_baseline = 9b1f0e7a4735df1c54867530cfd1f13b390e1514` — consistent across
all authored uploads. Complementary diagnosis evidence pin
`8631576dc5d8f76d1d0b301895ec5014161941cc` recorded in the delivery-note
provenance section with a concrete pre-delivery freshness procedure.

## Self-Check: PASSED

- Task 1 gate (prompt): one header/body separator (3 `^---$` incl. frontmatter);
  all 4 attachment filenames present; `not recommend` and `attached files only`
  present; **negative grep for `suggest defaults` passes** (build-design
  directive absent — D-04); zero banned repo-path markers.
- Task 2 gate (delivery note): both todo IDs present; 2 `PENDING`; `source_baseline`
  + diagnosis pin; `candidate verdict source`; both routing filenames; 6 A/B/C
  option markers (≥2).
- `git status --short` shows only the two new files (no spec/seed/diagnosis
  edits).

## Notes for Plan 45-04

- The checkpoint presents exactly the delivery-note D-13 section; recorded
  answers land back in that same section (and may motivate a package adjustment
  — e.g. Q1=B or Q2=A/C — applied before the final audit).
- The package-wide audit (≤5 uploads, zero repo paths in authored uploads,
  byte-identical diagnosis, consistent source_baseline, neutrality, claims-sync)
  runs last, after any owner-instructed adjustment.
