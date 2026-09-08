# Phase 57 Deferred Items

- 2026-09-08 — The Phase-50 adjacent `CandidateFinalizationTests`,
  `ExtractManifestTests`, and `BandRecordTests` cannot run in this checkout
  because their fixture launcher expects the archived path
  `.planning/phases/50-valid-stage-0-re-run/evidence/build_phase50_evidence.py`.
  The preserved Phase-50 implementation is under
  `.planning/milestones/v2.2-phases/50-valid-stage-0-re-run/evidence/`; copying
  or re-baselining it would alter historical evidence and is outside Plan
  57-04. This is a pre-existing path/layout issue, not a Phase-57 regression.
