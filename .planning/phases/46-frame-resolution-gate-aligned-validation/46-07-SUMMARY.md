---
phase: 46-frame-resolution-gate-aligned-validation
plan: "07"
subsystem: training
tags: [inst-01, conf-01, validation-gate, frame-ratification, eval01-precondition]

requires:
  - phase: 46-frame-resolution-gate-aligned-validation
    provides: 46-03 validation_gate core (FrameConvention, publishers, validator)
  - phase: 46-frame-resolution-gate-aligned-validation
    provides: 46-09 post-repair CONF-01 measurement and D-09 branch routing
  - phase: 46-frame-resolution-gate-aligned-validation
    provides: GAP-46-06 owner ratification of the operational validation frame
provides:
  - "RATIFIED_VALIDATION_FRAME traceable to the GAP-46-06 owner ruling"
  - "Full-pool conservation observation at every existing validation event"
  - "EVAL-01 precondition (iii) as an inspectable, fail-closed summary field"
affects: [INST-01 complete, ROADMAP Phase 46 criterion 3 satisfied]

key-files:
  created:
    - tests/phase46/test_validation_wiring.py
  modified:
    - pinn/training/validation_gate.py
    - pinn/train.py
    - pinn/training/summary.py
    - tests/phase43/test_summary_enrichment.py

key-decisions:
  - "Task 1 resolved to state (b): D-09 routed, GAP-46-06 RESOLVED-WITH-INSTRUCTION"
  - "Frame values quoted from the resolution note, never inferred from measurement (D-12)"
  - "Sidecar published before the pointer record is appended (D-17)"
  - "Gate failure converts to a failed: status record, never a training signal (D-15/D-20)"
  - "Sidecar validator imported function-locally so summary.py stays stdlib-only at module level"

requirements-completed: [INST-01]
completed: 2026-07-28
status: complete
---

# Phase 46 Plan 07: Frame Ratification and Gate-Aligned Validation Wiring

**Task 1's hard gate resolved to state (b), not state (c): the D-09 branch is
routed AND GAP-46-06 is `RESOLVED-WITH-INSTRUCTION`. INST-01 is complete — every
validation event now computes, durably persists, and inline-records a full-pool
conservation observation, and EVAL-01 precondition (iii) is an inspectable
summary field.**

## Ratification source cited for `RATIFIED_VALIDATION_FRAME`

The in-code comment block at `pinn/training/validation_gate.py:509-527` cites:

> GAP-46-06, Status RESOLVED-WITH-INSTRUCTION, owner ruling 2026-07-28, option B
> — "ratify an operational raw/native validation frame by instruction". Full
> record: `.planning/phases/46-frame-resolution-gate-aligned-validation/46-GAPS.md`,
> section "## GAP-46-06".

The constant quotes the resolution note's named triple rather than inferring one
from any measurement (D-12):

| field | constant | value |
|---|---|---|
| `position_frame` | `POSITION_FRAME_RAW` | `r_raw` |
| `time_coord` | `TIME_COORD_RAW` | `t_native` |
| `mass_convention` | `MASS_CONVENTION_ORDERED_RAW` | `ordered_raw` |

`conf01_evidence_ref` =
`.planning/phases/46-frame-resolution-gate-aligned-validation/evidence/target-frame/20260728T014532Z/raw.json`

**The machine verdict was not overwritten.** Plan 46-09's
`VERDICT_NON_FRAME_DIVERGENCE` (rule 5, D-09) stands unchanged in
`46-VERDICT-POSTREPAIR.md`. This wiring is the consequence of the owner's D-09
branch exercise on recorded evidence, not of a clean CONF-01 machine verdict,
and the comment block says so in-code.

## Final `validation.jsonl` record key list

Observed on a real run (not asserted from the plan text) — `runs/<run>/validation.jsonl`:

```
final_val_loss, gate_eps_h, gate_n_nonfinite, gate_n_trajectories,
gate_schema_version, gate_scs, gate_sidecar, gate_status, gate_verdict,
step, trend
```

Three legacy keys plus the eight `gate_*` keys, merged into the SAME event
stream — no parallel summary source.

## Summary projection key list

`summary.json.validation` (12 keys) and the `## Validation summary` section of
`summary.md`:

```
final_val_loss, trend, step,
gate_schema_version, gate_eps_h, gate_scs, gate_verdict, gate_status,
gate_n_trajectories, gate_n_nonfinite, gate_sidecar,
eval01_precondition_iii
```

Markdown render order is metrics-first: `gate_eps_h`, `gate_scs`,
`gate_verdict`, `gate_status`, `gate_n_trajectories`, `gate_n_nonfinite`,
`gate_sidecar`, `gate_schema_version`, then `eval01_precondition_iii`.

## End-to-end observation (ROADMAP Phase 46 criterion 3)

A real short run was executed and its artifacts inspected directly rather than
inferred from unit tests:

- 2 validation events → 2 sidecars (`validation_gate/step-00000001.json`,
  `step-00000002.json`)
- each sidecar carries **240 per-trajectory rows**, every row an
  `{record_key, eps_h, scs}` triple — criterion 3 ("records per-trajectory
  epsilon_H/SCS per run") holds
- the sidecar's `frame` block records the ratified triple and the
  `conf01_evidence_ref` verbatim
- `gate_status = "ok"` with `gate_verdict = "FAIL"` — the D-20 distinction
  between instrumentation success and metric failure is preserved end to end
  (the network is untrained, so FAIL is the honest result)
- `summary.json.validation.eval01_precondition_iii = true` for that run

## Measured `pytest tests/phase42/ -q` wall-clock (Task 2 acceptance criterion 7)

| | wall-clock | result |
|---|---:|---|
| BEFORE (commit `fe3d45de`, throwaway detached worktree) | **337.88s** | 35 passed, 3 skipped |
| AFTER (this plan's wiring) | **318.71s** | 35 passed, 3 skipped |

**Measured delta: −19.17s** — negative, i.e. the gate's cost is inside
run-to-run variance. The suite total is dominated by three signal tests with
fixed multi-second sleeps, so a per-test comparison was taken as well:

| test | BEFORE | AFTER |
|---|---:|---:|
| `test_sigint_twice_outside_debounce_escalates` | 105.02s | 92.09s |
| `test_sigint_mid_lbfgs_closure_stops_between_evals` | 102.05s | 102.26s |
| `test_sigint_twice_inside_debounce_coalesces` | 100.48s | 99.42s |

No test grew materially. The gate genuinely fires in these runs — the
dataset-free `_StubSource` (`pinn/train.py:215-281`) implements the full
`records_at_or_below`/`get`/`snapshot_times` surface, so each event computes
over 240 records × 32 snapshots — but the runs contain few validation events, so
the added cost stays under the sleep-dominated noise floor.

**FINDING for the orchestrator (thin margin, PRE-EXISTING).** The three
`tests/phase42/test_signals.py` subprocess tests run at 92–105s against the
**120s** per-subprocess timeout (`tests/phase42/test_runs_contract.py:110`).
Worst observed margin is ~15s at the BEFORE baseline and ~18s AFTER. Plan 46-07
did not consume this margin, but it is thin enough that an unrelated slowdown on
a loaded machine could surface as a flaky timeout. D-10 forbids escaping via a
new cadence/chunking knob, so this is reported rather than mitigated here.

## Validation

| check | result |
|---|---|
| `pytest tests/phase46/test_validation_wiring.py -q -rs` | **12 passed, 0 skipped** |
| `pytest tests/phase46/ -q -rs` | **114 passed, 27 subtests, 0 skipped** |
| `pytest tests/phase42/ -q` | **35 passed, 3 skipped** (pre-existing skips) |
| `pytest tests/ -q` | **1272 passed, 14 failed, 3 skipped, 311 subtests** |
| `grep -c '^def _run_validation_gate_pass' pinn/train.py` | 1 |
| `grep -c '^RATIFIED_VALIDATION_FRAME' pinn/training/validation_gate.py` | 1 |
| `grep -cE '^(import\|from) +(torch\|pinn\.training\.validation_gate\|pinn\.verification)' pinn/training/summary.py` | 0 |
| Task 1 frame-coherence import check | passed (`r_raw t_native`) |
| `git diff --check` | clean |

**The full suite is NOT green, and this plan did not make it so.** All 14
failures are pre-existing and environmental, in five modules that this plan does
not touch:

| module | count | cause |
|---|---:|---|
| `tests/phase43/test_verdict_grounding.py` | 7 | `FileNotFoundError` on `.planning/phases/43-verification-stage-0-pilot-acceptance/43-VERDICT.md` |
| `tests/phase43/test_verify_gate.py` | 2 | "no valid persisted Stage-0 timing calibration" — a preflight refusal raised *before* construction |
| `tests/phase43/test_pilot_calibration.py` | 2 | missing pilot evidence artifacts |
| `tests/phase43/test_smoke.py` | 1 | missing evidence README findings |
| `tests/watchdog/test_global_packaging.py` | 2 | `wd-arm` drift between the repo copy and the deployed canonical bin |

Evidence that none are attributable to 46-07:

1. `.planning/phases/` contains ONLY `46-frame-resolution-gate-aligned-validation`
   — the phase-43 artifacts these tests read were archived at v2.0 milestone
   close, so the files genuinely do not exist.
2. Gitignored `runs/` (6 entries) is present in this working tree but absent in
   a fresh worktree; its presence is what flips these tests from *skip* to
   *fail*. The same modules run clean in a fresh detached worktree.
3. An explicit A/B was run in a throwaway worktree at `fe3d45de` over all six
   affected modules, first at baseline and then with this plan's five changed
   files copied in. Both failure sets were identical.
4. `tests/phase43/test_summary_enrichment.py` — the ONE pre-existing test this
   plan modifies — passes.

`pytest tests/phase41/`, `tests/phase42/`, `tests/phase43/test_summary_enrichment.py`,
and `tests/phase46/` — the suites this plan's verify commands name as gates —
are all green.

## Follow-up carried forward

`RATIFIED_VALIDATION_FRAME` goes stale if Phase 47/48 moves residency to the
locked canonical scaled contract (`r'` with `u = t/T`). GAP-46-06's resolution
note records this as an accepted, owner-acknowledged consequence; the in-code
comment block makes re-ratification a traceable edit rather than a silent one.

---

*Phase: 46-frame-resolution-gate-aligned-validation*
*Plan: 46-07*
*Completed: 2026-07-28*
