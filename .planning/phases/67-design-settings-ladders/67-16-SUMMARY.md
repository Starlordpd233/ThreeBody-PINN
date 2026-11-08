---
phase: 67-design-settings-ladders
plan: "16"
subsystem: verification-diagnostics
tags: [pinn, exp02, exp03, exp04, exp05, phase-audit, evidence-index, closeout, validation]

requires:
  - phase: 67-design-settings-ladders (67-15)
    provides: the complete EXP-05 evidence chain with its committed review (3b19801c) and check-review gate PHASE67-AUDIT-OK-eligible phase state, all four experiments reviewed and on the record at f887f5e1
provides:
  - The re-derivable evidence index .planning/phases/67-design-settings-ladders/67-EVIDENCE-INDEX.json — the read-only audit-phase --json object's exact data with status PHASE67-AUDIT-OK (problems empty; harness freeze verified for all four experiments; exp02/exp04/exp05 scope none, exp03 proposal-ruled under its digest-bound ruling), persisted at 0a6de0c5 and re-verified by the plan's equality check (PHASE67-INDEX-OK)
  - The bounded four-experiment findings page 67-FINDINGS.md — every quantitative claim cited by committed path and sha256, with each experiment's registered prediction, complete observed branch, all matched main/repeat effects, uncertainty and SCOPE-49 disposition, and the shared limits (EXP-01 multi-setting positive-control confound, depth parameter confound, EXP-04 fan-in/dimension change, exact EXP-05 window coverage, GAP-59-08 energy caveat, association-only cosine, finite-budget reading, no-new-IC limit)
  - The verified phase boundary 67-CLOSEOUT.md and the observed validation state in 67-VALIDATION.md — all five planned contract commands green (phase67 260 OK / phase65 204 OK / phase66 101 OK, zero skipped required cases; protocol PROTOCOL-OK; final audit PHASE67-AUDIT-OK), the 17 spec-less probe candidates reconciled against the committed SPEC-less pass record by actual test identifiers, and the Phase 68/69 handoff without making either phase's decisions
affects: [phase 67 independent verification (orchestrator-owned), Phase 68 energy adjudication, Phase 69 final cause findings and redesign]

# Actuals (#2632) — pairs with the plan's `estimate` (10000 est / 20000 raw tokens, 2 tasks).
# Scale caveat: the realized diff is hand-authored planning text only; no
# harness code, evidence bytes or review JSON changed in this plan (the index
# is the audit's own output persisted mechanically).
actuals:
  tokens: 10648      # chars/4 over the realized text diff 0a6de0c5~1..18291f77 (42,591 bytes)
  tasks: 2           # 67-16-01 and 67-16-02 both executed; no conditional task existed
  commits: 3         # two verify(67-16) task commits + this docs close-out

tech-stack:
  added: []
  patterns:
    - "Closeout by re-derivation, not recomputation: the evidence index is the existing read-only audit's exact JSON persisted after its OK status, and every scientific claim in the findings is machine-copied from a committed review/result/budget/summary and pinned by sha256."
    - "Validation closure with observed-only updates: the validation contract's completion/Nyquist fields were set and the sign-off checked only after the five planned commands ran green, with real discovered counts, durations and zero-skip evidence recorded."

key-files:
  created:
    - .planning/phases/67-design-settings-ladders/67-EVIDENCE-INDEX.json
    - .planning/phases/67-design-settings-ladders/67-FINDINGS.md
    - .planning/phases/67-design-settings-ladders/67-CLOSEOUT.md
  modified:
    - .planning/phases/67-design-settings-ladders/67-VALIDATION.md (observed results, sign-off, SPEC-less reconciliation; completion fields set after all contracts passed)

key-decisions:
  - "The evidence index stayed the audit's exact object with nothing added — no source symbols, thresholds or owner decisions — so the read-only audit remains the single authority and the plan's byte-equality check re-derives it (PHASE67-INDEX-OK)."
  - "The plan's '17 spec-less probe candidates' count is not itemized as a named list in any committed planning artifact, so the reconciliation ran against the committed SPEC-less pass record (67-05/67-06 prohibition_probe_resolution) citing actual test identifiers and results, and states that basis plainly rather than reconstructing a list."

## Result Reading (transcribed from the committed reviews; digests in 67-FINDINGS.md)

- **EXP-02 (depth):** unsettled-continue; `confirmed` empty. The depth
  hypothesis is not supported at confirmation grade — d2 worsens on all
  three registered cases with qualifying effects but unsettled endpoints
  block confirmation, and the main-case d12 control is itself unsettled;
  d8 improves on all three without qualifying on main. Parameter counts
  137,737..795,657 stay recorded as the D-03 size confound.
- **EXP-03 (rate):** the registered rate-sensitivity hypothesis is refuted
  at confirmation grade — lr1e-3 confirmed-worsening (worsening in all
  three cases, relative E effects 15.4..39.2, matching tier change, all six
  endpoints settled) and nothing confirmed-improving; lr3e-5 ambiguous,
  the other arms unsettled. The committed proposal-pending review was
  resolved by the owner ruling of 2026-11-05 (verbatim "proceed with
  option 1" -> authorize-recorded-proposal), authorizing only EXP-04's
  dependent launch under its existing registration; the audit reads exp03
  proposal-ruled.
- **EXP-04 (time input):** unsettled-continue on all four contrasts;
  `confirmed` empty; encoded arms worsen in ten of twelve registered cells
  (the only improvement cells are the seed-41 repeat on the two locked
  arms, one below the 20% line), with the fan-in 1/16 (f1) and 1/18 (f12)
  input-design change preserved as a recorded confound.
- **EXP-05 (window):** unsettled-continue on all three contrasts;
  `confirmed` empty. The improvement direction is present on all nine
  case-contrast cells with every relative E effect qualifying (0.14..0.88)
  and the tier improving only on the seed-41 repeat, but the main case is
  unsettled end to end (all six endpoints still improving past the 5% line
  at budget end) and the repeat-system lap10 control is unsettled, so only
  the seed-41 repeat is fully settled; no short-window success or
  full-window failure is declared.
- **Phase-level:** no pass-bar ruling, no redesign decision, no framework
  or locked-value change, and no unresolved reserved proposal; the four
  SCOPE-49 dispositions are factual (none / proposal-ruled / none / none).

## Task Commits

1. **67-16-01** - 0a6de0c5: `verify(67-16): commit the phase evidence index and findings` — the persisted PHASE67-AUDIT-OK index (row presence re-derived: 15/15/18/12 timing and science rows; 124 attempt records all published, no failed or partial attempt) and the four-experiment findings with path+sha256 citations and measured costs (19,750.2 / 32,185 / 19,695 / 29,246 s science walls against 25,466.9 / 39,055.1 / 25,880.3 / 30,305.5 s projections).
2. **67-16-02** - 18291f77: `verify(67-16): commit the phase boundary closeout and observed validation` — the five green contract commands with real counts/durations, the validation sign-off and SPEC-less reconciliation, and the closeout recording acceptance coverage, exact evidence counts, harness freeze (41 paths at source commit 84754309), budget fairness, chronology, the immutable scientific boundary and the Phase 68/69 handoff (100,876.2 measured science wall seconds, about 28.0 machine hours).
3. **Plan close-out** - this commit: the plan summary.

## Verification

- `python -B -m pinn.verification.diagnostic_phase67 audit-phase` -> PHASE67-AUDIT-OK (exit 0), run before persisting the index and again after the closure artifacts.
- The plan's index equality check -> PHASE67-INDEX-OK.
- `python -B -m unittest discover -s tests/phase67 -t .` -> 260 tests, OK, 159.9 s, zero skipped.
- `python -B -m unittest discover -s tests/phase65 -t .` -> 204 tests, OK, 31.1 s.
- `python -B -m unittest discover -s tests/phase66 -t .` -> 101 tests, OK, 15.1 s.
- Protocol load -> PROTOCOL-OK.

## Deviations from Plan

None — the plan executed as written. One grounding note, recorded in the
closeout and summary rather than silently handled: the plan's "17 spec-less
probe candidates" count appears only in the plan text; the reconciliation
therefore reconciles against the committed SPEC-less pass record and actual
test identifiers instead of a reconstructed list, introducing no new
threshold, adjudication choice or probe execution.

## Handoff

Phase 67's four experiments are complete and on the record. The
independent verifier/orchestrator owns final phase acceptance and the
roadmap/state bookkeeping (this plan deliberately did not touch
STATE.md or ROADMAP.md). Phase 68 receives the unchanged energy/yardstick
issue; Phase 69 receives the evidence-backed finite-budget findings and
actual machine hours. Neither phase's decisions were made here.
