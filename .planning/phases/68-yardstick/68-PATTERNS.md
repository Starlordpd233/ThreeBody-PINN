# Phase 68 yardstick pattern map

**Mapped** 2026-11-08. The analogs use tracked source from the trainex
worktree. File names on the left are execution targets.

## File classification

| File | Role | Data flow | Closest tracked analog | Match |
|---|---|---|---|---|
| `pinn/verification/yardstick_audit.py` | Read-only measurement CLI | Fixed panel to evidence | `pinn/verification/baselines.py` and `diagnostic_data.py` in the same directory | Role and reader |
| `tests/phase68/__init__.py` | Test package | None | `tests/phase67/__init__.py` | Package |
| `tests/phase68/test_yardstick_audit.py` | Wiring and refusal tests | Temporary corpus and numeric arrays | `tests/phase65/test_isolation.py`, `tests/phase59/test_scorer_known_errors.py`, `tests/phase43/test_gate_boundary.py` | Reader and numerical assertions |
| `.planning/phases/68-yardstick/evidence/yardstick-audit.json` | Reproducible evidence | Deterministic results and provenance | `.planning/phases/59-read-only-baseline-scorecard/evidence/baselines/baselines.json`, `pinn/verification/evidence_io.py` | Evidence |
| `.planning/phases/68-yardstick/68-AUDIT.md` | Audit reading | Inventory and complete known-answer tables | `.planning/phases/64-feasibility-verdict/64-VERDICT.md` | Evidence before interpretation |
| `.planning/phases/68-yardstick/68-CHECKPOINT-2.md` | Decision packet | Committed measurements to options | `.planning/phases/64-feasibility-verdict/64-CHARTER.md` | Options and reply rule |
| `.planning/phases/68-yardstick/68-CHECKPOINT-2-RULING.md` | Owner replies and v2.6 routing | Verbatim reply to disposition | `.planning/phases/67-design-settings-ladders/67-EXP03-RULING.md` | Evidence-bound ruling |
| `.planning/phases/59-read-only-baseline-scorecard/59-GAPS.md` | Existing gap register | Ruling to the GAP-59-08 block | Same file and `docs/git-guidelines.md` | Scoped update |

## Pattern assignments

- Use the manifest and attestation construction in
  `diagnostic_data.open_diagnostic_context`. Skip its normalizer and use
  `production_reference.load_reference` directly. `baselines._open_context`
  shows the lighter evidence path, with the stricter
  `Stage0TrainingReader` selected here. Use `physical_window` for the native
  mask and the single mean expression in `diagnostic_fit._comparison_rows`
  for the constant. The latter also scores a Kepler formula, which belongs
  in the packet as frozen evidence.
- Use the fixture manifest and refusal assertions in
  `tests/phase65/test_isolation.py`. The `TinyCorpus` builder in
  `tests/phase39/_fixtures.py` supplies valid file syntax. The fixture's
  default base and gold schedules have different sample counts but are not
  nested. For the end-to-end test, write the allowed pair on nested native
  grids using the existing `write_brutus` helper in the temporary tree.
  Install the global attestation only in a fresh process.
- Use `ScoreResult.to_json_dict` and `validation_gate.json_safe_float` for
  nonfinite conventions. Use the provenance/hash helpers in
  `evidence_io.py`. Build on the Phase 59 baseline evidence pattern, with a
  single result object whose rows preserve key, prediction and velocity
  route. Compare the replay on stable content while retaining the capture
  timestamp and code commit.
- Use Phase 64's readable comparison table and charter layout. Cite the
  full source values, then identify the practical consequence of each
  option. Phase 67's ruling pattern binds the verbatim reply to the evidence
  and preserves the original result. Use the existing GAP-59-08 block's
  status and resolution fields after an explicit reply.

## Shared patterns

Use the existing local Python environment. Check facts in committed
artifacts, run the scoped tests, and commit explicit owned paths through
`scripts/agent-commit`. Keep the audit capture and owner ruling separate.
Audit code has no production consumer. Scope, thresholds, splits, caller
implementations and historical evidence remain governed by the phase spec.
