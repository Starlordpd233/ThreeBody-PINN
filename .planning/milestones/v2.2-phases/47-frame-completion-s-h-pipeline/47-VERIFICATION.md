---
phase: 47-frame-completion-s-h-pipeline
verified: 2026-07-31T08:11:30Z
evidence_gathered: 2026-07-31T08:06:52Z
status: passed
score: 5/5 must-haves verified
behavior_unverified: 0
must_haves_source: ROADMAP.md Success Criteria (Option B — override PLAN-level must_haves)
prohibitions_checked: 16
prohibitions_violated: 0
decision_coverage:
  honored: 0
  total: 14
  parse_status: could-not-parse
  blocking: false
deferred:

  - item: "First authoritative real-corpus S_H, eps_H and N_train values"
    to_phase: 50
    evidence: "Phase 50 covers RUN-01/RUN-02 — the first authorized Stage-0 setup/run. Owner ruling 2026-07-30 Option B, recorded at .planning/STATE.md:356."
---

# Phase 47: Frame Completion & S_H Pipeline — Verification Report

**Phase Goal:** The training path runs in the frame the specs lock, and the loss's energy scale is a real dataset statistic computed in that frame — not a per-anchor stand-in built on an incoherent one.
**Verified:** 2026-07-31T08:06:52Z
**Status:** human_needed → canonicalized to `passed` (see Verification Metadata)

## Goal Achievement

### Observable Truths

Must-haves are the five ROADMAP Success Criteria, which are the contract and override the
29 PLAN-level truths (10 + 11 + 8). Each was verified by independent re-derivation against
the live tree, not by reading the SUMMARY claims.

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | Resident position/velocity series are the locked canonical contract (`pre.r_gauge`/`pre.v_gauge`), physics residual zero on a true trajectory, `dr'/du = v_gauge` exactly, `IC₁₃` and position targets share one gauge (CONF-09) | ✓ VERIFIED | Grid-refinement convergence study on a curved trajectory: residual falls at exactly the O(h²) rate (4.03→4.02→4.01→4.00 over N=128→2048), i.e. entirely finite-difference truncation — the identity holds exactly. Counterfactual: the superseded CONF-08 source holds a **constant 9.000** under the same refinement (= `T−1`, `T=10`), a real non-vanishing incoherence. `V == D/T` exactly; `D = 4.641588833612778`. `r_gauge[0]`/`v_gauge[0]` elementwise-equal `r0_gauge`/`v0_gauge`; `build_raw_ic13` bit-identical from either. Wiring: `adapter.py:861,884-885,890,894`. |
| 2 | `RATIFIED_VALIDATION_FRAME` re-ratified to the scaled triple in the same change, and any test encoding the superseded pairing corrected in that same change (CONF-09) | ✓ VERIFIED | Runtime read: `("r_prime", "u_t_over_T", "ordered_raw")`; `conf01_evidence_ref` resolves to the Phase 47 D-07 record naming GAP-46-07. `git show --name-only 2c84d161` = exactly 4 paths (evidence, adapter.py, validation_gate.py, tests/phase46/test_pairing_repair.py). `git diff 2c84d161^ 2c84d161 -- pinn/data/preprocessing.py` = 0 lines. |
| 3 | A preprocessing stage computes `S_H = median_train(K0 + Uabs0)` over the admitted set **in the completed frame** and persists it in training metadata (CONF-02) | ✓ VERIFIED | Independent median oracle: odd→2.0, even→2.5 (central average), single→itself; `n_train` correct; permutation-invariant. Artifact carries the exact 7-key set; `s_h` round-trips bit-exact float64; `eps_h == factor·s_h` exact; frame block carries the re-ratified triple. Write path: 4 `atomic_write_text` refs, 0 raw writes (`atomic_io.py:41`, independently covered by `tests/phase41/test_atomic_io.py`). Capture is float64 at admission, before the fp32 cast (`adapter.py:861-864`). |
| 4 | `S_H` validation fails closed per §3.4: non-finite or `≤ 0` is a validation failure (CONF-02) | ✓ VERIFIED | `validate_s_h` refuses NaN, +inf, −inf, −1.0 and exactly 0.0 (ValueError); accepts 1.5. `write_training_metadata` refuses all five **and leaves 0 files on disk** in every case — refusal provably precedes the artifact. Empty train pool refuses before numpy can reach a NaN-median path. Adversarial tamper matrix: 12/12 mutations refused (eps_h decoupled, s_h→0/NaN/negative, n_train→0, n_train→bool, extra key, missing key, schema bump, eps_train drift, factor drift, frame→superseded triple), plus a mismatched live factor. Good artifact byte-unchanged (SHA-256) after the campaign. |
| 5 | `ε_H = 1e-4 · S_H` is wired into the loss assembly and the §3.4-prohibited `+1e-12` additive fallback floor is removed (CONF-03) | ✓ VERIFIED | Swept 8 (factor, s_h) combinations × 300 anchors each, every anchor with a **distinct** `h0`: exactly ONE `eps_h` per combination, equal to `factor·s_h` exactly — provably independent of `h0`. `s_h` is `KEYWORD_ONLY`, no default (omitted→TypeError, positional→TypeError, NaN/±inf/0/negative→ValueError). AST sweep: 15/15 `RunController(` sites carry explicit `s_h=`, 0 missing. `1e-12` in `controllers.py` = 0; diff shows `abs(h0)*factor + 1e-12` → `factor*self._s_h` with the WR-02 comment deleted. D-20 holds: `denom = h0_t.abs() + eps_h_t`, numerically h0-dependent (1.343→0.584→0.508 for h0 = 1/10/100 at fixed eps_h); `loss_catalog.py` byte-unchanged across 47-03. |

**Score:** 5/5 truths verified (0 present, behavior-unverified)

### Required Artifacts

| Artifact | Expected | Status | Details |
|---|---|---|---|
| `pinn/data/adapter.py` | Residency from `pre.r_gauge`/`pre.v_gauge`; float64 `k0`/`uabs0` capture | ✓ EXISTS + SUBSTANTIVE + WIRED | :861,884-885,890,894 |
| `pinn/training/validation_gate.py` | `RATIFIED_VALIDATION_FRAME` = scaled triple | ✓ EXISTS + SUBSTANTIVE + WIRED | :791; verified at runtime |
| `pinn/training/run_metadata.py` | `compute_s_h`, `validate_s_h`, `write_training_metadata`, `load_training_metadata` | ✓ EXISTS + SUBSTANTIVE + WIRED | All four exported; loader signature keyword-only |
| `pinn/loss_catalog.py` | `_matched_plummer_components` seam | ✓ EXISTS + SUBSTANTIVE + WIRED | Delegation preserves `_matched_plummer_hamiltonian` |
| `pinn/data/types.py`, `pinn/data/splits.py` | `AdmittedRecord.k0/uabs0`, `StageIndex.k0/uabs0` | ✓ EXISTS + SUBSTANTIVE + WIRED | `_source_value` delegation |
| `pinn/training/controllers.py` | Required keyword-only `s_h`; `eps_h` assembly | ✓ EXISTS + SUBSTANTIVE + WIRED | :311,326-328,490 |
| `pinn/train.py` | `s_h` bound on BOTH setup branches | ✓ EXISTS + SUBSTANTIVE + WIRED | `compute_s_h` at :872; `_assert_s_h_matches_artifact` returns validated `s_h` |
| `tests/phase47/` (3 modules) | CONF-09/02/03 suites | ✓ EXISTS + SUBSTANTIVE | 21 tests, 112 assertions, 0 skipped |
| `evidence/frame-re-ratification/…` | D-07 supersession record | ✓ EXISTS | Resolves from `conf01_evidence_ref` |
| `evidence/target-frame/…` | One-shot D-22 re-probe + D-23 comparison | ✓ EXISTS | Exactly 1 directory (probe run once) |
| `run_dir/training_metadata.json` | Production setup artifact | ✓ SCHEMA + BEHAVIOUR PROVEN | Deliberately no real-corpus instance — deferred to Phase 50 |

**Artifacts:** 11/11 verified

### Key Link Verification

| From | To | Via | Status | Details |
|---|---|---|---|---|
| adapter residency | every anchor target (`h0`, `l0`, `true_r0`, `true_v0`) | `StageIndex` pass-through | ✓ WIRED | Swap propagates with no signature change |
| `RATIFIED_VALIDATION_FRAME` | `_validate_frame` coherence check | frame block | ✓ WIRED | Pair admitted by `COHERENT_FRAME_PAIRS`; superseded triple now rejected |
| `pre.r_gauge[0] == pre.r0_gauge` | `build_raw_ic13` inputs | identity | ✓ WIRED | Elementwise equality confirmed at runtime |
| admission float64 capture | `AdmittedRecord.k0/uabs0` → `StageIndex` → `compute_s_h` | accessor chain | ✓ WIRED | float64 boundary crossed once, at admission |
| `_matched_plummer_components` | adapter capture + loss | single seam | ✓ WIRED | One implementation feeds both |
| `write_training_metadata` | `atomic_write_text` | `atomic_io.py:41` | ✓ WIRED | 4 refs, 0 raw writes |
| validated `s_h` | `RunController(s_h=)` → `_AnchorContext.eps_h` → `soft_energy_loss` denominator | explicit parameter chain | ✓ WIRED | Never a module global; never frozen config |
| `stage.energy_floor_factor` | `eps_h` assembly site | config read | ✓ WIRED | Named home of `1e-4`; not duplicated |
| `soft_energy_loss` | `ε_H` single legal use site | byte-unchanged | ✓ WIRED | `git diff` empty across 47-03 |

**Wiring:** 9/9 connections verified

## Requirements Coverage

| Requirement | Status | Blocking Issue |
|---|---|---|
| CONF-09: Complete the residency transform; re-ratify the frame in the same change | ✓ SATISFIED | — |
| CONF-02: Build the `S_H` pipeline, persisted in training metadata, fail-closed | ✓ SATISFIED | — |
| CONF-03: Wire `ε_H = 1e-4 · S_H`; remove the `+1e-12` additive fallback floor | ✓ SATISFIED | — |

**Coverage:** 3/3 requirements satisfied

## Prohibition Enforcement (16 items, all judgment-tier)

No plan projected `check_kind`/`check_target` scalars, so none is test-tier; each was
instead discharged by a deterministic mechanical check recorded below.

| # | Plan | Prohibition (abbreviated) | Result |
|---|---|---|---|
| 1 | 47-01 | Re-probe run at most once | ✓ exactly 1 evidence directory |
| 2 | 47-01 | Time handling not moved; `u = t/T` stays at the sampling boundary | ✓ residents keep `parsed_brutus.times`; `batches.py` diff = 0 lines |
| 3 | 47-01 | `r_com_ordered`/`v_com_ordered` NOT deleted | ✓ still on `PreprocessedTrajectory` |
| 4 | 47-01 | `IC₁₃`/`E` construction not edited | ✓ `compute_invariants(...r0_gauge, v0_gauge)` intact |
| 5 | 47-01 | No parallel Phase 47 resident-pairing oracle | ✓ phase-46 file corrected in place |
| 6 | 47-01 | No framework-spec edit; no training run; no held-out eval | ✓ `pinn_instruction/` diff = 0 lines |
| 7 | 47-01 | `target_frame_probe.py` unmodified | ✓ diff = 0 lines |
| 8 | 47-02 | No fallback floor/max/clamp/default substituting for `S_H`/`ε_H` | ✓ 0 occurrences in `run_metadata.py` |
| 9 | 47-02 | `compute_invariants` not a source; no `gate_metrics`/`EPS_INV` import | ✓ 0 refs in the four CONF-02 production files |
| 10 | 47-02 | `S_H` never written into config | ✓ `config.py`/`config_yaml.py` diff = 0 lines |
| 11 | 47-02 | Median never reduced inside `_materialize` | ✓ 0 `median` refs in that scope |
| 12 | 47-02 | `trainex-r2/` not consulted (SCOPE-31) | ✓ 0 refs |
| 13 | 47-03 | No additive floor survives or reappears under any name, anywhere | ✓ `controllers.py` = 0; **no `1e-12` line added anywhere in `pinn/` during the phase** (diff grep empty). The 24 repo-wide occurrences are COM/momentum tolerances, `clamp_min` guards, `rtol` comparisons and legacy v1.3 reference code — none an energy floor |
| 14 | 47-03 | `S_H` never read from config | ✓ 0 `config.stage.s_h` refs |
| 15 | 47-03 | `soft_energy_loss`/`_matched_plummer_hamiltonian` bodies not edited | ✓ `loss_catalog.py` diff = 0 lines across 47-03 |
| 16 | 47-03 | No spec edit; §3.4:542 comment is VER-20 routing material only | ✓ `pinn_instruction/` diff = 0 lines |

**Prohibitions:** 16/16 upheld, 0 violated.

## Anti-Patterns Found

Scanned the eight phase-47-modified production files.

| Category | Count |
|---|---|
| 🛑 TBD/FIXME/XXX without issue reference | 0 |
| 🛑 Placeholder content | 0 |
| ⚠️ TODO/HACK | 0 |

**Anti-patterns:** 0 found (0 blockers, 0 warnings)

## Test Quality Audit

| Test File | Linked Req | Tests | Assertions | Skipped | Circular | Assertion Level | Verdict |
|---|---|---|---|---|---|---|---|
| `test_conf09_frame_completion.py` | CONF-09 | 4 | 26 | 0 | No | Value + behavioural | ✓ Sound |
| `test_conf02_s_h_pipeline.py` | CONF-02 | 7 | 72 | 0 | No | Value + behavioural | ✓ Sound |
| `test_conf03_eps_h_wiring.py` | CONF-03 | 6 | 14 | 0 | No | Value + behavioural | ✓ Sound |

**Disabled tests on requirements:** 0
**Circular patterns detected:** 0 — the two `write_text` sites in `test_conf02_s_h_pipeline.py` (:416, :456) write *mutated and truncated* payloads to prove the loader refuses them. They are adversarial tamper fixtures, the inverse of circular expected-value generation.
**Insufficient assertions:** 0
**Expected-value provenance:** VALID — CONF-09 compares against an analytic first-principles identity; CONF-02 against `numpy.median` as an independent oracle; derived bounds are formulas over dtype contracts, never fitted to observation (SCOPE-29/D-26).

## Behavioral Verification

| Check | Result | Detail |
|---|---|---|
| `tests/phase47/` | ✓ 21 passed | 1.07s |
| `tests/phase46/ tests/phase47/` (phase gate) | ✓ 172 passed, 68 subtests, **0 skipped** | exit 0 |
| Full suite (phase41/42/43/46/47) | 12 failed, 586 passed, 3 skipped, 94 subtests | 359.86s — all 12 in `tests/phase43/`, all pre-existing |
| Regression causation | ✓ ZERO regressions | Detached worktree at the branch point (`c0d4d9dd`) with an identical environment yields **12 failed / 186 passed / 0 skipped — byte-identical to HEAD** |

The 12 `tests/phase43/` failures are environmental, not code: `git log --diff-filter=D`
names `89348b7c chore(planning): archive v2.0 milestone files` (2026-07-23) as the commit
that deleted the evidence tree they read, and `git merge-base --is-ancestor` confirms it
predates the first Phase 47 commit (2026-07-30) by six days. Control: the two `phase43`
modules that DO exercise Phase 47 symbols pass fully (13 and 29 tests). Tracked as
D-47-01 in `deferred-items.md`.

## Decision Coverage

⚠️ Non-blocking warning: the handler could not parse the `47-CONTEXT.md` `<decisions>`
block — 14 decisions detected, 0 parsed. The bullets use a `- **D-NN [JUDGEMENT]** …`
form the parser does not accept (it expects `- **D-NN** …`). This is a **format** issue in
the CONTEXT file, not evidence that decisions were abandoned: D-01 … D-27 are each cited
by name in the plan SUMMARYs and, where mechanical, were independently confirmed above
(D-01, D-03, D-05, D-06, D-07, D-09..D-21). No status impact.

## Human Verification Required

This is an infrastructure/foundation phase (data pipeline, internal contracts, loss
assembly) with no user-facing elements, so no artificial manual steps are invented. Two
items nonetheless route to the human checkpoint:

### 1. Judgment-tier prohibition acknowledgement

**Test:** Confirm the 16 prohibitions above were discharged acceptably.
**Expected:** All 16 upheld with the mechanical evidence recorded in this report.
**Why human:** No plan projected `check_kind`/`check_target` scalars, so none is test-tier;
the workflow routes judgment-tier prohibitions to the end-of-phase checkpoint rather than
letting a verifier self-grade them green.
**Discharged by:** `47-UAT.md` — 7/7 passed, 0 issues, owner-delegated agent verification.

### 2. Real-corpus values (deferred, not a gap)

**Test:** Produce the first authoritative real-corpus `S_H`, `ε_H`, `N_train`.
**Expected:** Emitted by Phase 50's first authorized Stage-0 setup/run.
**Why human:** Owner ruling 2026-07-30 Option B forbids launching training in Phase 47.
Confirmed absent: no `training_metadata.json` exists anywhere in the tree, and `runs/`
holds only pre-existing Phase-43-era directories dated 2026-07-19..22.

## Deferred Items

| Item | Deferred To | Evidence |
|---|---|---|
| First authoritative real-corpus `S_H`, `ε_H`, `N_train` | Phase 50 | Phase 50 covers RUN-01/RUN-02, the first authorized Stage-0 setup/run. Owner ruling 2026-07-30 Option B, recorded at `.planning/STATE.md:356`. |
| 12 pre-existing `tests/phase43/` failures (D-47-01) | v2.2 test-hygiene pass | Proven pre-existing above; routing recorded in `deferred-items.md`. |

## Gaps Summary

**No gaps found.** Phase goal achieved. All five success criteria verified by independent
re-derivation, all three requirements satisfied, all 16 prohibitions upheld, zero
anti-patterns, zero regressions.

## Verification Metadata

**Verification approach:** Goal-backward from ROADMAP.md Success Criteria (Option B)
**Must-haves source:** ROADMAP.md Success Criteria (override PLAN frontmatter; the 29
PLAN-level truths were cross-referenced)
**Automated checks:** 5 truths + 11 artifacts + 9 key links + 3 requirements + 16
prohibitions + 3 test-quality audits + 4 behavioral checks = **51 passed, 0 failed**
**Human checks required:** 2 (both discharged — see above)
**Status derivation:** `human_needed` per `determine_status` step 3 (judgment-tier
prohibitions route to the end-of-phase human checkpoint in an interactive run).
Subsequently canonicalized to `passed` under the `verify-work` completion rule — execution
verification was waiting only on human UAT, and `47-UAT.md` recorded 7/7 passed with zero
issues.

**Re-affirmation note.** All evidence in this report was gathered at
`2026-07-31T08:06:52Z` (`evidence_gathered`). The `verified:` timestamp was
subsequently refreshed to `08:11:30Z` because the phase-close documentation pass
edited three SUMMARY/deferred-items files after the original stamp, which the
staleness gate correctly flagged. The refresh is **not** a re-grading: `find`
over `pinn/` and `tests/` confirms **zero `.py` files** changed since evidence
was gathered, and `git status` confirms no uncommitted code exists. The
post-verification edits were exclusively prose corrections that make the
SUMMARYs *agree* with this report — a superseded-notice on 47-01's stale
owner-ruling section, a construction-site count correction on 47-03, and the
historical pre-existence proof appended to `deferred-items.md`. The phase gate
was re-run after those edits: `tests/phase46/ tests/phase47/` → 172 passed, 68
subtests, 0 skipped.

---
*Evidence gathered: 2026-07-31T08:06:52Z · Re-affirmed: 2026-07-31T08:11:30Z*
*Verifier: Claude (orchestrator, inline — owner delegated verification 2026-07-31)*
