---
phase: 30-research-package-assembly
plan: 03
subsystem: erw-research-package
tags: [erw, specwork, doc-03, pkg-05, pkg-08, snapshots, byte-fidelity, provenance, consolidation]
requires:
  - "30-02 D-09 APPROVED record (document list + three inclusion calls)"
  - "30-01 30-SNAPSHOT-HASHES.txt seed + recovery-tag record"
  - "v1.5-verified dataset facts (24-VERIFIED-FACTS.md), simulation_data/Documentation"
provides:
  - "research_package/specs/ — six byte-for-byte intact source snapshots + consolidated-context.md"
  - "research_package/verified-facts-reference.md — standalone v1.5-verified-facts reference (sole owner, F11)"
  - "30-SNAPSHOT-HASHES.txt — complete per-file content sha256 + source-commit provenance + package-wide source_baseline pin"
affects:
  - "30-04 (authors companions; references verified-facts-reference.md + claims register)"
  - "30-05 (originally writes source_baseline = 522cea71 into master frontmatter; audit refresh later supersedes current package baseline to 3781d1a after the CTL path-only citation repair; DELIVERY-NOTE.md at round root, D-03)"
tech-stack:
  added: []
  patterns: ["byte-for-byte cp snapshotting", "content sha256 + source-commit dual provenance", "assembly-time HEAD pin (F7)"]
key-files:
  created:
    - "pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_package/specs/03-curriculum-and-training-loop.md"
    - "pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_package/specs/ctl_instruction.md"
    - "pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_package/specs/pinn_architecture.md"
    - "pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_package/specs/sampling_method.md"
    - "pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_package/specs/review_of_framework.md"
    - "pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_package/specs/stage_strat_revision.md"
    - "pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_package/specs/consolidated-context.md"
    - "pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_package/verified-facts-reference.md"
  modified:
    - ".planning/phases/30-research-package-assembly/30-SNAPSHOT-HASHES.txt"
decisions:
  - "verified-facts-reference.md created STANDALONE per D-09 inclusion call (b) APPROVED-STANDALONE; 30-03 is sole owner (F11)"
  - "source_baseline originally pinned to assembly-time HEAD 522cea71 (F7), NOT the recovery-tag commit e841c958; audit refresh later supersedes current package baseline to 3781d1a after the CTL path-only citation repair"
  - "DELIVERY-NOTE.md placement (round root, D-03) is 30-05's concern; not created here"
metrics:
  duration: "~1 task-session"
  tasks: 3
  files-created: 8
  files-modified: 1
  completed: 2026-06-18
---

# Phase 30 Plan 03: Research-Package Specs Snapshots Summary

Byte-for-byte commit-pinned assembly of the approved doc-03 ERW package `specs/`: six intact
source snapshots, one consolidated context file, and a standalone verified-facts reference, with
complete dual-provenance (content sha256 + source commit) and a package-wide `source_baseline`
pin to the assembly-time `milestone/v1.6` HEAD.

## What Was Built

- **Task 1 — six intact snapshots.** Created `research_package/specs/` and copied the six
  D-09-approved sources byte-for-byte (`cp`, never retyped/reformatted/excerpted):
  `03-curriculum-and-training-loop.md` (issue-03), `ctl_instruction.md`, `pinn_architecture.md`,
  `sampling_method.md`, `review_of_framework.md`, `stage_strat_revision.md`. Framework specs were
  NEVER consolidated (D-04). `cmp -s snapshot==source` exits 0 for all six pairs; `git diff
  --quiet` exits 0 for all six sources (the three specs + two reports + issue-03), proving the
  SPEC zero-edits AC for the whole source set (F9), not just the reports.
- **Task 2 — consolidated context + standalone verified-facts reference.** Built
  `specs/consolidated-context.md` holding ONLY the D-09-approved MINIMAL fragments (per-variant
  `dt_out` distributions; per-variant median snapshot counts; stage-assignment counts; the
  184-gap + ~2,565 gold count; the EVID-10 `D`-rejection anchor) with internal per-fragment
  source labels (D-10), minimal per D-22. Per D-09 inclusion call (b) APPROVED-STANDALONE, also
  built `research_package/verified-facts-reference.md` as the standalone v1.5-verified-facts
  reference (sole owner, F11). Every figure in both files carries a CLM-NN row in
  `30-CLAIMS-INVENTORY.md` (15 distinct CLM IDs referenced; all registered).
- **Task 3 — snapshot-hash provenance + source_baseline pin.** Extended `30-SNAPSHOT-HASHES.txt`
  (F8 schema `basename | canonical source path | file sha256 | source commit | notes`): the four
  new snapshot lines (issue-03 + three specs) record BOTH a content sha256 (byte-fidelity) AND
  the source's last-touching commit (provenance); the two report lines (seeded in 30-01) are the
  packaged snapshots for those sources. Added the package-wide `source_baseline` pin =
  `522cea7182bf3d0e3206d8faa75150e705b174f0` (assembly-time `git rev-parse HEAD`, F7), with a
  byte-identity note that the recovery tag `v1.6-pre-phase-30` = `e841c958` trails HEAD by the
  30-01/30-02 `.planning/` commits and that all six sources are byte-identical across both refs.

> Audit refresh 2026-06-18: the current package baseline is
> `3781d1a68a9364717d399e536b7fc9ad56e19645`; `ctl_instruction.md` was refreshed
> after a path-only correction to stale Phase 25 evidence citations. See
> `30-SNAPSHOT-HASHES.txt` and `30-VERIFICATION.md` for current hash and
> re-validation records.

## Verification Evidence

- VC-02: `cmp -s` snapshot==source exits 0 for all six pairs (ctl_instruction, pinn_architecture,
  sampling_method, review_of_framework, stage_strat_revision, 03-curriculum-and-training-loop).
- Re-derived content sha256 of the six PACKAGED snapshots equals the recorded values (the two
  report packaged-copy hashes equal the seeded source hashes — byte-identity confirmed).
- VC-03 + F9: `git diff --quiet` exits 0 for all six sources (no source modified).
- F7: recorded `source_baseline` (`522cea71…`) equals `git rev-parse HEAD` at assembly time.
- All 15 CLM IDs referenced in the two authored files are registered in `30-CLAIMS-INVENTORY.md`
  (no unregistered figure).

## Decisions Made

- **verified-facts-reference.md is STANDALONE** (D-09 inclusion call (b) APPROVED-STANDALONE). It
  is reused by the claims register + the SCOPE-12 preamble; folding it would force those two
  companions to re-cite a buried fragment. 30-03 is its sole owner (F11). The consolidated-context
  file reproduces the verified anchors compactly and points to this standalone file for full
  statements.
- **source_baseline = assembly-time HEAD (`522cea71`), NOT the recovery-tag commit** (F7). 30-01/
  30-02 committed `.planning/` artifacts after the `v1.6-pre-phase-30` tag (`e841c958`), so HEAD
  is ahead. The six sources are byte-identical across both refs (those commits never touched the
  sources), so either ref reproduces the snapshots; the assembly-time HEAD is the value 30-05
  writes into the master frontmatter.
- **DELIVERY-NOTE.md round-root placement (D-03)** is recorded by the plan as 30-05's task; this
  plan creates no master/prompt/delivery-note and nests only the uploaded payload under
  `research_package/`. (Mechanical/structural choice already grounded in D-03; noted per the plan
  objective.)

## Deviations from Plan

None — plan executed exactly as written. No deviation rules (1–4) triggered; no auto-fixes
needed. No STOP-protocol gap encountered: every decision (the MINIMAL excerpt set, the STANDALONE
verified-facts form, the ALM-clamp inclusion) was pre-grounded in the 30-02 D-09 APPROVED record;
all transcribed figures trace to a CLM row or a verbatim source.

## Known Stubs

None. All eight created files are complete; `consolidated-context.md` (95 lines) and
`verified-facts-reference.md` (91 lines) carry substantive grounded content, not placeholders.

## Self-Check: PASSED

- All eight created files exist on disk; `30-SNAPSHOT-HASHES.txt` modified.
- Snapshot byte-fidelity re-derived (sha256 match) and `cmp -s` exit-0 for all six pairs.
- Commit verification recorded in the commit footer of this plan's atomic commit.
