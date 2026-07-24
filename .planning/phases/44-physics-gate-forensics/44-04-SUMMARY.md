---
phase: 44-physics-gate-forensics
plan: 04
wave: 2
requirements: [DIAG-01, DIAG-02, DIAG-03]
status: complete
---

# 44-04 Summary — Evidence manifest (DIAG-01..03 input pinning)

## Objective
Pin every input file read by the three analysis scripts by SHA-256 + git HEAD,
cross-checked against each diag output's embedded provenance, so every number in
`44-DIAGNOSIS.md` is re-derivable from a pinned tree (D-02).

## What was built
- `evidence/build_manifest.py` — reads the three diag provenance blocks,
  recomputes each input's SHA-256 from the live tree, halts without writing on
  any mismatch (tamper evidence). Plain stdlib; cwd-independent.
- `evidence/manifest.json` — the single pinning record (2,835 B).
- `evidence/README.md` — reproduction boundary, self-check assertions,
  determinism, and the new-convention note.

## Key results
- **15 inputs pinned**, all cross-checks `all_match: true` (1 metrics.json +
  4 train.log.jsonl + 4 validation.jsonl + 4 splits.json + 43-CALIBRATION.md +
  38-VERIFICATION.md).
- `git_head = 8631576…` (the Wave-1 tip the diag outputs were produced against),
  `git_head_available: true` — bounded `git rev-parse HEAD`, mirroring
  `pinn/verify.py`.
- No timestamp field → the manifest is a deterministic function of the tree at a
  given commit.
- `splits.json` hashes recorded (smoke == seed42; seed41, seed43 diverge),
  consistent with DIAG-03 and the seed-42 evaluation receipt.

## Verification
- Byte-identical on consecutive re-runs at this commit.
- Fail-closed: a hash disagreement between a diag script's recorded input and the
  current tree halts the manifest write.

## Deviations
None. One path-resolution bug in `build_manifest.py` was caught by its own
fail-closed guard during development (diag outputs are under `evidence/`, not
`evidence/evidence/`); fixed and re-verified before commit.
