---
phase: 67-design-settings-ladders
verified: 2026-11-08T12:50:04Z
status: passed
score: 4/4 roadmap success criteria verified (plus 16 plan-level must-have truths sampled, all passing)
behavior_unverified: 0
overrides_applied: 0
prohibitions_judgment_tier: 3 # all 3 resolved with direct evidence; see prohibitions checklist below
re_verification:
  previous_status: none
  previous_score: n/a
  gaps_closed: []
  gaps_remaining: []
  regressions: []
gaps: []
deferred:
  - truth: "GAP-59-08: the frozen position-error E limitation — how energy error is measured is not adjudicated in this phase"
    addressed_in: "Phase 68 (Yardstick)"
    evidence: "ROADMAP.md Phase 68: 'the owner decides how energy error is measured (GAP-59-08)'; every review.json carries a gap_59_08 field; 67-FINDINGS.md 'GAP-59-08 energy caveat'; 59-GAPS.md records GAP-59-08 OPEN and owner-routed"
behavior_unverified_items: []
coincidental_reliance_items: []
requirements:
  EXP-02:
    status: satisfied
    evidence: "Depth ladder run and recorded: 15/15 science rows (d2/d4/d6/d8/d12 x 3 cases) at common N=152900, each record carrying 5 similarity events with per-layer adjacent_cosine_mean for exactly the arm's layers (d2=3, d4=5, d6=7, d8=9, d12=13 including input) and 3 score checkpoints with E and tier; verdict unsettled-continue committed in evidence/exp02/review.json (confirmed empty, all four contrasts unsettled)"
  EXP-03:
    status: satisfied
    evidence: "Learning-rate ladder run and recorded: 15/15 rows (lr1e-3/lr3e-4/lr1e-4/lr3e-5/lr1e-5 x 3 cases) at common N=155100, identical similarity trace steps [0, 38775, 77550, 116325, 155100] through training in every row; the only confirming contrast (lr1e-3 confirmed-worsening) qualifies on all three cases with settled endpoints; refuted-lead owner ruling digest-bound in 67-EXP03-RULING.md"
  EXP-04:
    status: satisfied
    evidence: "Time-input ladder run and recorded: 18/18 rows on both backbones — exp01-raw/f1/f12 (depth 1, width 384, first omega 1000 = the Phase 66 network) and locked-raw/f1/f12 (depth 12, width 256, omega 30) — each with E/tier at 3 checkpoints and 5 per-layer similarity events (2 layers on the exp01 backbone, 13 on locked); verdict unsettled-continue in evidence/exp04/review.json"
  EXP-05:
    status: satisfied
    evidence: "Window ladder run and recorded: 12/12 rows (lap1/lap2/lap5/lap10 x 3 cases) at locked depth 12 with exact signed first-crossing windows (lap1 last_time 0.95 on 1632 verified in registration window_metadata) and per-window recomputed same-window baselines; verdict unsettled-continue in evidence/exp05/review.json"
---

# Phase 67: Design & Settings Ladders — Verification Report

**Phase Goal:** The project knows which part of the locked setup turns the network's view of time to noise: its depth, its training settings, its time input or the window length. (ROADMAP.md, Phase 67)
**Verified:** 2026-11-08T12:50:04Z
**Status:** passed (4/4 roadmap success criteria verified; registered verdicts EXP-02 unsettled-continue, EXP-03 refuted at confirmation grade with owner ruling, EXP-04/EXP-05 unsettled-continue — diagnostic knowledge, which is the goal, does not require a confirmed lead)
**Re-verification:** No — initial verification
**Verifier stance:** goal-backward, adversarial. Every claim below was re-derived from committed bytes in this worktree (branch milestone/v2.5, HEAD 82720003); SUMMARY.md claims were treated as hypotheses, not evidence.

## Goal Achievement

The goal is diagnostic knowledge about which part of the locked setup degrades the network's view of time. That knowledge exists in committed, digest-verified form: four registered designs with predictions and reading rules, 60 complete science-row records (plus 60 timing rows and 4 metadata captures), four machine reviews applying a pre-registered reading rule, four result pages embedding their reviews byte-exactly, one digest-bound owner ruling, an aggregate findings page whose every number was re-checked, and a re-derivable evidence index. The verdicts (three unsettled, one refuted-at-confirmation-grade) are the intended outputs of the registered rules, not failures of the phase.

### Observable Truths (roadmap success criteria)

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | Each experiment has its prediction page committed before its first run | ✓ VERIFIED | Git chronology + run receipts, per experiment (table below). Design with registered hypothesis/prediction/reading rule committed before the first real metadata/timing attempt; science prediction page committed before the first science run. |
| 2 | Depth ladder records E, tier and per-layer neighbour similarity at 2/4/6/8/12 layers; learning-rate ladder records the same, with the similarity trace through training, at each rate | ✓ VERIFIED | 15/15 exp02 rows validated: layer counts exactly 3/5/7/9/13 (input + h1..hN) with non-null adjacent_cosine_mean at 5 events; E and tier at 3 score checkpoints per row (d12 main final E=0.03483/tier 1). 15/15 exp03 rows: 13 layers, similarity trace at steps [0, 38775, 77550, 116325, 155100] of N=155100 in every row. |
| 3 | Time-input and window experiments each record E, tier and similarity for every variant, on the locked depth and, for time input, on the Phase 66 network | ✓ VERIFIED | 18/18 exp04 rows across six variants; design declarations confirm exp01 backbone = depth 1 / width 384 / first omega 1000 (the Phase 66 network) vs locked backbone = depth 12 / width 256 / omega 30. 12/12 exp05 rows at locked depth 12 (13-layer similarity events) with per-window recomputed baselines. |
| 4 | Every confirming result is repeated on a second panel system and a second seed, and every result is reviewed against the plan under SCOPE-49 | ✓ VERIFIED | The only confirming contrast (exp03 lr1e-3 confirmed-worsening) qualifies in all three registered cases — main-1632-s42, repeat-851-s42 (second panel system), repeat-1632-s41 (second seed) — with all six endpoints settled (review.json). All four experiments have committed reviews (schema phase67-review/v1) recording scope49_disposition; the exp03 refuted lead went proposal-pending → owner ruling, digest-bound (see below). |

**Score:** 4/4 truths verified (0 present, behavior-unverified)

### SC-1 chronology evidence (commit hashes and run receipts)

| Exp | Design + timing-prediction commit (local) | First metadata/timing gate check (UTC) | Science prediction page commit (local) | First science gate check (UTC) |
|-----|-------------------------------------------|----------------------------------------|----------------------------------------|-------------------------------|
| exp02 | 75424795, Nov 2 22:50 | Nov 4 02:04 | 652d1a9d, Nov 3 20:35 | Nov 4 02:45 |
| exp03 | 952f4dcb, Nov 4 03:07 | Nov 4 09:09 | 1977d85d, Nov 4 03:18 | Nov 4 21:40 |
| exp04 | ffd80b7b, Nov 6 17:45 | Nov 7 00:01 | 4c8b7b25, Nov 7 12:00 | Nov 7 18:13 |
| exp05 | 072abd88, Nov 7 18:50 | Nov 8 01:46 | 79587171, Nov 7 19:56 | Nov 8 02:09 |

Every design (containing the registered hypothesis, prediction, reading rule, variants, cases and controls — verified in `evidence/exp0N/design.json`) precedes the first real attempt; every science prediction page precedes the first science run. This matches the plans' registered chronology (e.g. 67-08 task 67-08-03: "Commit budget.json, both budget/prediction pages, science-matrix.json and ALL science registrations before science").

### Full 60-row record validation (SC-2/SC-3 substance)

Every one of the 60 science rows (`evidence/exp0{2,3,4,5}/science/{main-1632-s42,repeat-851-s42,repeat-1632-s41}/{arms}`) was mechanically validated by this verification:

- attempt.json `status: published`; record.json `status: complete`, `counted: false`, `artifact_kind: diagnostic`
- access attestation: exactly 1 TRAIN open, 0 validation opens, 0 test-split opens (TRAIN-only boundary intact in every row)
- 5 similarity events at 5 distinct steps, consistent per-event layer count, non-null `adjacent_cosine_mean` on every layer
- 3 score checkpoints each carrying non-null E and tier
- power-gate.json with `power_source: AC Power` in every row

Result: 60/60 rows pass with zero problems. Layer counts per arm match depths exactly: exp02 d2/d4/d6/d8/d12 → 3/5/7/9/13 layers; exp03 all arms → 13; exp04 exp01-* → 2, locked-* → 13; exp05 all arms → 13.

### SC-4 evidence chain integrity

- All 14 key cited artifacts' SHA-256 digests recomputed by this verification and matching `67-FINDINGS.md` citations exactly: 4 review.json files, 4 result pages, 67-EXP03-RULING.md, 4 budget.json files, harness-freeze.json (14/14 match).
- Result pages embed their reviews byte-exactly (spot-verified: exp02 review's relative_E_effect 2.4911142745966544 and arm E 0.12158120320360874 both present in 67-EXP02-RESULT.md, which carries per-row tables with row-commit columns).
- exp03 ruling digest-binding verified: `evidence/exp03/review.json` and `67-EXP03-RESULT.md` were introduced together at bfd85916 (2026-11-05 03:02) and have no later commits; the ruling commit eab52f7d (2026-11-05 20:42) added only 67-EXP03-RULING.md — `changed_by_ruling: false` holds for both reviewed artifacts. Ruling content matches the registered verdict: owner verbatim "proceed with option 1", option `authorize-recorded-proposal`, authorizing only EXP-04's dependent launch, no plan/scope/pass-bar/registration change.
- exp05 exact-window coverage spot-verified: lap1 registration on 1632 carries `window_metadata.last_time = 0.95` with per-window recomputed same-window baselines (two-Kepler E 0.16544, window-constant E 1.14540), matching the closeout's claim.

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `evidence/exp0{2..5}/design.json` | Registered design: hypothesis, prediction, reading rule, variants, cases, controls, no-continuation | ✓ VERIFIED | All keys present (verified in exp02: hypothesis, prediction_table, reading_rule, variants, cases, controls, no_continuation, schedule, budget_rule, scope_branches); each digest-cited in FINDINGS |
| `67-EXP0{2..5}-PREDICTION.md` + `-TIMING-PREDICTION.md` + `-BUDGET.md` | Prediction pages per experiment | ✓ VERIFIED | All 12 files exist; 592/…-line science pages committed at the budget-freeze commits per the registered chronology |
| `evidence/exp0N/…/science/*/*/{registration,record,attempt,power-gate}.json + diagnostic.weights` | 60 complete science rows x 5 artifacts | ✓ VERIFIED | 60/60 rows validated; closeout's "exactly five committed artifacts per row" confirmed by the validation pass |
| `evidence/exp0{2..5}/review.json` | phase67-review/v1 reviews with confirmation + scope49 disposition | ✓ VERIFIED | All four present; verdicts match registered verdicts; exp03 `confirmed: [{arm: lr1e-3, confirmation: confirmed-worsening}]` |
| `67-EXP0{2..5}-RESULT.md` | Result pages embedding reviews byte-exactly with per-row tables | ✓ VERIFIED | Embedding verified; per-row tables with E/tier/endpoint/row-commit columns present |
| `67-EXP03-RULING.md` | Owner ruling, digest-bound | ✓ VERIFIED | Digests match; introducing-commit and changed_by_ruling claims verified via git |
| `67-FINDINGS.md`, `67-CLOSEOUT.md`, `67-EVIDENCE-INDEX.json` | Aggregate, closeout, re-derivable index | ✓ VERIFIED | FINDINGS numbers spot-checked against review.json (exp02 d2 effects; exp03 endpoint E values); index equals audit output (PHASE67-AUDIT-OK re-derived below) |
| `evidence/harness-freeze.json` | 41 frozen paths at commit 84754309 | ✓ VERIFIED | Digest matches FINDINGS citation; audit reports freeze_verified true for all four experiments |

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|----|--------|---------|
| Row registration | Run record | registration-bound reader (`check-row`), registration pinned in record | ✓ WIRED | Every record carries its registration; audit re-derives registration-to-attempt relations (problems empty) |
| Record scores | Review contrasts | `write_review` reads records under the pre-registered rule | ✓ WIRED | Review JSON carries per-case observed_fit/relative_E_effect/endpoint_status matching record score_checkpoints (spot-verified d2 main) |
| Review | Result page | Byte-exact embedding | ✓ WIRED | Verified for exp02; closeout claims byte-exact for all four and review-consistency was part of the committed audit |
| exp03 review | Owner ruling | SHA-256 binding in 67-EXP03-RULING.md | ✓ WIRED | review_sha256/result_page_sha256 recomputed and match; artifacts unchanged since introduction |
| All experiments | Phase audit | `audit-phase` → 67-EVIDENCE-INDEX.json equality | ✓ WIRED | PHASE67-AUDIT-OK re-run by this verification (exit 0); index status PHASE67-AUDIT-OK, problems empty |

### Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
|----------|--------------|--------|--------------------|--------|
| review.json contrasts | E, tier, endpoints | record.json score_checkpoints (frozen scorer output in committed records) | Yes — 60 committed records | ✓ FLOWING |
| RESULT pages | per-row tables | committed records + row commits | Yes | ✓ FLOWING |
| 67-FINDINGS.md numbers | all quantitative claims | committed reviews/budgets/summaries (digest-cited) | Yes — 14/14 digests recomputed | ✓ FLOWING |
| 67-EVIDENCE-INDEX.json | experiment states | live audit of committed evidence | Yes — re-run in this verification | ✓ FLOWING |

No static fallbacks or hardcoded scientific values found in the evidence chain; check-row provably hides scientific values during runs (confirmed by the phase's committed code review, 67-REVIEW.md).

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
| Phase audit gate | `python -B -m pinn.verification.diagnostic_phase67 audit-phase` | PHASE67-AUDIT-OK, exit 0 (re-run by verifier, <1 s) | ✓ PASS |
| Protocol load | `load_protocol(); print('PROTOCOL-OK')` | PROTOCOL-OK | ✓ PASS |
| Test-suite discovery | discover `tests/phase67` | 260 tests (matches committed claim exactly); skip-scan: zero skip markers | ✓ PASS |
| Reading-rule boundary test (single named) | `unittest tests.phase67.test_reading_rule.ImprovementTests.test_exact_five_percent_is_settled_and_the_next_instant_is_not` | OK (0.41 s) | ✓ PASS |
| Reading-rule module | `unittest tests.phase67.test_reading_rule` | 21 tests OK (0.435 s) | ✓ PASS |

(An initial named-test invocation failed only because this verifier guessed the wrong test class; the correct class passes. Recorded for honesty.)

### Probe Execution

| Probe | Command | Result | Status |
|-------|---------|--------|--------|
| (none declared) | — | No `scripts/*/tests/probe-*.sh` exists for this phase; plan mentions of "probe" refer to the planning-time prohibition-probe reconciliation, not executable probes. The phase's own executable gates (audit-phase, protocol load) were re-run above. | N/A |

### Requirements Coverage

| Requirement | Source Plans | Description | Status | Evidence |
|-------------|--------------|-------------|--------|----------|
| EXP-02 | 67-01, 02, 04–09, 16 | Depth ladder, E/tier/per-layer similarity at each depth | ✓ SATISFIED | See truths 2; frontmatter mapping above |
| EXP-03 | 67-01, 04–07, 10, 11, 16 | Learning-rate ladder with similarity trace through training | ✓ SATISFIED | See truths 2 and 4 |
| EXP-04 | 67-01, 02, 04–07, 12, 13, 16 | Time-input design on locked depth and EXP-01 network | ✓ SATISFIED | See truth 3 |
| EXP-05 | 67-01, 03–07, 14–16 | Window ladder 1/2/5/10 laps | ✓ SATISFIED | See truth 3 |

Orphan check: REQUIREMENTS.md maps exactly EXP-02..05 to Phase 67; all four are claimed by plans. No orphaned requirements. (The REQUIREMENTS.md traceability rows and ROADMAP.md checkbox still read Pending/unchecked — that is the orchestrator's post-verification bookkeeping, same convention as Phases 65/66.)

### Test Quality Audit

| Test Area | Linked Req | Active | Skipped | Circular | Assertion Level | Verdict |
|-----------|-----------|--------|---------|----------|-----------------|---------|
| tests/phase67 (13 modules, 260 tests) | EXP-02..05 + cross-cutting | 260 | 0 | 0 | Value-level (e.g. "exact five percent is settled and the next instant is not"; "exact twenty percent effect confirms improvement") | VALID |

Disabled tests on requirements: 0. Circular patterns: 0. The per-module decomposition in 67-VALIDATION.md sums exactly to 260. The committed state-A validation audit found 0 gaps/escalations.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| (none in phase-modified files) | — | TBD/FIXME/XXX/TODO/HACK/PLACEHOLDER scan of pinn/verification/diagnostic_phase67*.py, diagnostic_fit.py, diagnostic_time_features.py, diagnostic_variants.py, diagnostic_similarity.py, diagnostic_power.py, tests/phase67/ | — | Zero matches |
| 67-REVIEW.md (phase's own code review) | WR-01..WR-05 | Defense-in-depth enforcement gaps (dead census admission check; launch-vs-row predicate not re-verified; freeze not re-verified at launch; ruling scope list not per-dependent; supervisor race can downgrade a published claim) | Warning (recorded by the phase, not a verification gap) | All are tampering-path-only; committed evidence shows no instance of any being hit; each refusal still happens at the reader before scientific values are exposed |

### Prohibitions Checklist (judgment tier — 3 items, all resolved with direct evidence)

| Prohibition | Verdict | Evidence |
|-------------|---------|----------|
| MUST NOT present low adjacent-time hidden-state cosine as proof of information loss or a causal mechanism (67-05) | Resolved — no violation | The only "causal"/"information loss" occurrences in 67-FINDINGS.md (lines 64, 330, 339–343) and in all four result pages are the explicit disclaimer note "adjacent-time hidden-state similarity is associated evidence only; no cosine threshold and no causal claim" (embedded in every review), plus FINDINGS 339–343 which explicitly states the experiments do not establish causal attribution. No cosine threshold appears in any review. |
| MUST NOT present a budget-limited or unsettled fit as proof of representational impossibility (67-05) | Resolved — no violation | Only occurrences are the disclaimers "not representational impossibility" (FINDINGS 324, CLOSEOUT 153); zero matches in all four result pages. Reviews record unsettled endpoints as unsettled; the no-continuation policy extends nothing. |
| MUST NOT present a successful short prefix as full-window success or an orbit-specific training fit as evidence of generalization to new initial conditions (67-06) | Resolved — no violation | FINDINGS 332–334 ("No new-IC generalization…"), FINDINGS EXP-05 section ("never full-window successes"), EXP02 result page line 374 ("No new-IC generalization claim"); zero generalization/full-window-success claims elsewhere. |

These are LLM-judged narrative checks resolved against committed text; they are recorded here with their evidence rather than silently absorbed (per the ADR-550 D4 flagging requirement). If the owner wants an explicit human sign-off on these three narrative obligations, it can be added to the phase-tail checkpoint without reopening any evidence.

### Decision Coverage

All 13 trackable 67-CONTEXT.md decisions are honored by shipped artifacts (`check.decision-coverage-verify`: total 13, honored 13, not_honored empty, non-blocking gate).

### Human Verification Required

None. This is a diagnostic-evidence phase with no user-facing elements; the real runs were owner-supervised live in the owner's AC windows (power-gate receipts on every row); the one owner decision the rules reserved (exp03 refuted lead) was made by the owner and is recorded verbatim and digest-bound; every roadmap truth is verified from committed bytes; no truth is left behavior-unverified. The 67-REVIEW.md warnings WR-01..WR-05 are recorded defense-in-depth findings for future harness work, not owner decisions.

### Gaps Summary

No gaps. All four roadmap success criteria are verified against concrete committed artifacts: prediction-before-run chronology holds for every experiment and every run stage; the ladders' E/tier/per-layer-similarity records are complete and mechanically validated across all 60 science rows; the time-input experiment covers both backbones including the Phase 66 network and the window experiment covers all four lap prefixes with exact signed first-crossing windows; the single confirming result is replicated on the second panel system and second seed with settled endpoints, and every result carries a committed SCOPE-49 review with the one reserved decision resolved by a digest-bound owner ruling. GAP-59-08 (energy measurement) is not a phase failure: it is explicitly deferred to Phase 68 by the roadmap and recorded as owner-routed in every review, the findings page and the closeout.

The registered verdicts themselves (EXP-02/04/05 unsettled-continue; EXP-03 refuted at confirmation grade with "proceed with option 1" / authorize-recorded-proposal) are committed and were not re-litigated; under the pre-registered reading rules these verdicts are the phase's intended diagnostic outputs, and the goal — knowing which part of the locked setup turns the network's view of time to noise, with depth, training settings, time input and window length each now carrying committed evidence — is achieved.

---

_Verified: 2026-11-08T12:50:04Z_
_Verifier: Claude (gsd-verifier)_
