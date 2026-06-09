---
phase: 20.5
slug: sampling-coordinate-allocation
status: passed
nyquist_compliant: true
wave_0_complete: true
created: 2026-06-09
---

# Phase 20.5 - Validation Strategy

## Test Infrastructure

| Property | Value |
|---|---|
| Framework | disposable Python probe plus shell/doc checks |
| Python | `.venv/bin/python` |
| Quick run command | `.venv/bin/python .planning/milestones/v1.4-phases/20.5-sampling-coordinate-allocation/probes/verify_sobol_allocation.py` |
| Full suite command | AC-SAMP-01 three-surface probe plus gap, handoff, and no-`pinn/`-diff guards |
| Estimated runtime | under 5 seconds |

## Sampling Rate

- After sampling-spec edits: run the SPEC surface.
- After probe or data-generation reference changes: run all three surfaces.
- Before closeout: require the complete AC-SAMP-01 probe to exit 0.

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---|---|---|---|---|---|---|---|
| 20.5-01-* | PART1 | 0 | SAMP-01, SAMP-02, VER-05 | governance/doc-structure | Check requirements, roadmap mapping, SCOPE-05, and resolved gap records | yes | green |
| 20.5-02-* | PART2 | 1 | SAMP-01, SAMP-02, VER-05 | three-surface probe | `.venv/bin/python .planning/milestones/v1.4-phases/20.5-sampling-coordinate-allocation/probes/verify_sobol_allocation.py` | yes | green |
| 20.5-03-* | PART3 | 2 | SAMP-01, SAMP-02, VER-05 | closure/full-suite | Re-run AC-SAMP-01 and check the alignment handoff, scoped provenance caveat, and no open gaps | yes | green |

## Wave 0 Requirements

- [x] `verify_sobol_allocation.py` exists.
- [x] `simulation_data/Scripts/ic_generation/` is available under the SCOPE-05 carveout.
- [x] `20-5-DATA-ALIGNMENT.md` records AC-SAMP-01 and the scoped provenance claim.
- [x] No additional test framework is required.

## Manual-Only Verifications

None. The probe exercises the spec text, entrypoint AST/configuration, and sampler behavior directly. Historical dataset provenance remains explicitly outside the scoped claim.

## Validation Sign-Off

- [x] All task groups have automated verification.
- [x] Sampling continuity is preserved.
- [x] Wave 0 dependencies exist.
- [x] No watch-mode flags.
- [x] Feedback latency < 5s.
- [x] `nyquist_compliant: true` set in frontmatter.

**Approval:** approved 2026-06-09 after AC-SAMP-01 passed on the current tree.

## Validation Audit 2026-06-09

| Metric | Count |
|---|---|
| Gaps found | 1 missing `VALIDATION.md` |
| Resolved | 1 |
| Escalated | 0 |
