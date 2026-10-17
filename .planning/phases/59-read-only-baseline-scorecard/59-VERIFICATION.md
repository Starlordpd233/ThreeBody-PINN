---
phase: 59-read-only-baseline-scorecard
verified: 2026-10-17T16:38:24Z
status: passed
score: 6/6 success criteria met
verifier: executing agent (claude-code/claude-opus-5-5); not an independent gsd-verifier pass
head: 505cba7410bfaf3fbc14e7f5053aaa8f9b25a358
behavior_unverified: 0
overrides_applied: 0
human_verification: []
---

# Phase 59: Read-Only Baseline & Scorecard — Verification Report

**Phase goal:** Before anything trains, the project knows five things: exactly
what it will measure; what a no-learning formula and a copy of the nearest
training system already score; how hard the Stage-0 target is; how hard every
later stage is; and whether generation 7's checkpoints contradict the plan.

**Verified:** 2026-10-17 at HEAD `505cba74`
**Status:** passed. All six success criteria are met, and Gate G1's outcome is
"proceed".

## In plain language

Phase 59 set out to measure before training anything, and it did. The rules
for judging a network were written down and locked first. Two cheap yardsticks
were then scored, and neither reaches the pass line on the validation panel.
The difficulty of Stage 0 and of every later stage was measured from the
training data alone. Generation 7's saved checkpoints were examined, and they
do not contradict the plan. An independent checker re-derived every recorded
result from the raw data and got the same bytes. No network was trained, and
no test-split file was opened.

## Method note

The agent that executed 59-10 wrote this report, so it is not an independent
verification. SUMMARY claims were treated as allegations and checked against
the committed evidence and the verifier. Evidence was reused only where its
inputs are unchanged:

- **Fresh at `505cba74`:** `scorecard-frozen`, `audit`, `diag07 --require all`,
  `guardrails`, `manifest --area all` (all with `--require-committed` where the
  command takes it), the hash-only `census`, `survey` and `baselines` checks,
  and the phase-file and findings-contract steps of `final`. All exit 0; log
  retained outside the repository.
- **Reused from `087e4179`:** the byte-for-byte re-derivations inside
  `verify_phase59_evidence.py final` (exit 0, `PHASE59-EVIDENCE-OK`, 644 s),
  the full `tests/phase59` suite (319 OK, 185.0 s) and the adjacent regression
  (177 OK, 1.9 s). Since `087e4179` only `59-VALIDATION.md`, `59-10-SUMMARY.md`,
  `STATE.md`, `ROADMAP.md` and `REQUIREMENTS.md` changed. The verifier reads
  `59-VALIDATION.md` only for its test-module list, and that list is identical
  before and after the sign-off. No code, data or evidence byte changed.

A separate gsd-verifier pass can be requested if independent confirmation is
wanted.

## Success criteria

| # | Criterion | Verdict | Evidence |
|---|---|---|---|
| SC1 | Scorecard and scorer committed before any rung, with metrics, tiers 0–3, budget and decision rules (incl. the counting rule), polish budget, G2 sweep grid and reading cadence; the known-error tests pass | **MET** | `evidence/scorecard-freeze.json` (frozen at `0aac08d8`, commit `4ea3b1bc`) pins `feasibility_scorecard_v1.json` `f4b17688…9444b`, the module `12fcb230…dfe5` and `59-SCORECARD.md` `7142dfc6…653e`. `scorecard-frozen` → `SCORECARD-FROZEN-OK` at HEAD. `tests/phase59/test_scorer_known_errors.py` covers the reference against itself (`SelfTests`), a known displacement (`OffsetTests`), known velocity scaling (`VelocityScalingTests`) and an inner-pair-only error (`InnerPairPhaseTests`). They are part of the 319-test suite, which passes. No rung ran in this phase. |
| SC2 | Difficulty census over the 1,812 Stage-0 training systems, re-derivable, with the phase-accuracy figure; three panels committed with their selection rule | **MET** | `af13a180` (census and frozen-rule panels). `final` re-derived the census byte for byte (59.2 s). `census --skip-rederive --require-committed` → `CENSUS-OK` at HEAD. Phase accuracy: 1 part in 1,169 at 10%. Panels: singles 1632/851/4658, the 16-system family, and the 227-system validation panel. |
| SC3 | Two-Kepler formula scored on every panel system, nearest-neighbour copy on the validation panel, before any rung | **MET** | `c5c6cd18`. The formula reaches Tier ≥ 1 on 1 of 1,812 training systems and 0 of 227 validation systems. The copy reaches Tier 1 on 0 of 227 (median E 2.14). Re-derived byte for byte in `final` (66.0 s); `BASELINES-OK` at HEAD. The two FEAS-09 probes are recorded as "not applicable: no hierarchical split". |
| SC4 | Whole-dataset survey with predictability envelope and stage difficulty ordering, re-derivable; two hard-stage probes selected by their pre-declared rule | **MET** | `04e17dac`. 12,023 records. Difficulty ordering by tau_L, closest approach, acc_max, error growth and N_in. Picks: `standard/base/2279` (4b) and `standard/base/3418` (6). Re-derived byte for byte in `final` (504.4 s); `SURVEY-OK` at HEAD. |
| SC5 | JX-1 (executed half), JX-2, JX-3, JX-4, JX-5 (split) and JX-10 each have a command, checkpoint provenance (`best.pt`, `global_step` 900; GAP-59-01) and a reading; Gate G1's outcome recorded | **MET** | `41dee29a` (JX-10, JX-1, G1) and `ce1e6104` (JX-5, JX-2, JX-4, JX-3). `diag07 --require all --require-committed` → `DIAG07-OK` at HEAD. Readings: JX-10 supports (54/54); JX-1 physics share 7.187e-07, below the 1e-2 threshold, so **G1 does not fire: proceed**; JX-2 noise not excluded; JX-3 mixed; JX-4 relative descent without useful accuracy; JX-5 initialization dominated by the physics term (RMS 2.899e+05 against 44.10). |
| SC6 | No training step ran and no test-split file was opened; the tooling asserts it | **MET** | `guardrails` → `GUARDRAILS-OK` at HEAD. `tests.phase59.test_static_guards` (no optimizer, no checkpoint write, no `pinn.train`/`pinn.evaluate` import, `weights_only=True` loads) passes. The split allowlist refuses test IDs before any path is built, and every area's `files_opened.json` records 0 test-split opens and 0 blocked attempts. |

## Requirements coverage

Every plan's `requirements` field is accounted for:

| Requirement | Plans | REQUIREMENTS.md |
|---|---|---|
| FEAS-01 | 59-01, 59-02, 59-04, 59-10 | Complete |
| FEAS-02 | 59-03, 59-04, 59-05, 59-10 | Complete |
| FEAS-07 | 59-03, 59-04, 59-08, 59-10 | Complete |
| FEAS-08 | 59-03, 59-04, 59-06, 59-10 | Complete |
| DIAG-07 | 59-03, 59-04, 59-07, 59-09, 59-10 | Complete |

## Supporting checks

| Check | Result |
|---|---|
| `verify_phase59_evidence.py final` (detached, at `087e4179`) | exit 0, `PHASE59-EVIDENCE-OK`, 644 s |
| `unittest discover -s tests/phase59 -p 'test_*.py' -v` (at `087e4179`) | 319 tests OK, 185.0 s |
| Adjacent regression (`tests.phase39.test_prohibitions`, `test_splits`, `test_adapter`, `tests.phase46.test_isolation`, two `tests.phase38` prohibition tests) | 177 tests OK, 1.9 s |
| Fast verifier subcommands at `505cba74` | all exit 0 (see Method note) |
| GAP-59-08 section vs `phase_start_head` `f3d2f420` | unchanged, Status OPEN |
| (59-10)-scoped commits touch only the plan's own files | OWN-COMMITS-OK (3 commits) |
| `59-VALIDATION.md` | 15/15 rows ✅ green, `nyquist_compliant: true`, `wave_0_complete: true` |

## Carried forward

- **GAP-59-08 (OPEN, owner-routed).** The production energy check measures
  ε_H with finite-difference velocities, so even the exact Brutus answer scores
  4.7e-2 to 3.8e-1. Phase 59 reported it and did not fix it, as planned. It
  blocks any spend of the held-out evaluation and the FEAS-10 pass-bar choice.
  It does not block Phase 60.
- **GAP-59-13 (resolved, option A).** The scorer's network scoring crashes on
  MPS. The scorer was left byte-unchanged because Plan-07 evidence pins its
  hash. Phase 60 must fix it before scoring a network on MPS.

## Known issues

- The `59-VALIDATION.md` sign-off item "Feedback latency < 10s" is not met
  and stays unticked: `test_evidence_verifier` takes 69.7 s and `test_diag07`
  13.6 s. This affects how fast feedback is during development, not what the
  phase established.
- The audit step prints the owner-accepted GAP-59-10 deviation line
  (`ic13_max_abs` 1.19e-07 against the frozen 1e-07), as expected.
- `ROADMAP.md` said "9/10 plans executed" in the Phase 59 detail section after
  59-10 closed. The closeout commit corrects it.
- The backup tag `backup/59-10-closeout` from the approved soft reset still
  exists. The owner may delete it.
