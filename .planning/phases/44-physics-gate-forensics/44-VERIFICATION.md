---
phase: 44-physics-gate-forensics
verified: 2026-07-24T06:28:31Z
status: passed
score: 5/5 must-haves verified
behavior_unverified: 0
overrides_applied: 0
---

# Phase 44: Physics-Gate Forensics Verification Report

**Phase Goal:** The failure is characterized, not guessed at: the held-out ε_H distribution, the training-time loss composition, and the seed band are each quantified from retained artifacts, and a hypothesis-ranked diagnosis report gives the owner (and the trainex-r2 researchers) an evidence map of candidate causes — with the remedy deliberately left open.
**Verified:** 2026-07-24T06:28:31Z
**Status:** passed
**Re-verification:** No — initial verification

## Goal Achievement

This is a read-only forensics phase: no application under test, no conventional
test suite. "Verification" reduces to two independent invariants, both confirmed
by the verifier's own process (not by trusting SUMMARY/UAT claims):

1. **Every number quoted in `44-DIAGNOSIS.md` mechanically regenerates from
   pinned inputs.** Re-ran all four scripts with the pinned interpreter
   (`~/miniforge3/envs/pinn-train/bin/python3`, Python 3.11.15); the three diag
   JSONs came back **byte-identical** (SHA-256 unchanged), and the DIAGNOSIS
   headline figures were cross-checked field-by-field against the JSON.
2. **Each script self-checks and fails closed.** Confirmed by reading all four
   scripts: fail-closed guards precede every write, and no evaluator/training
   entry point is invoked (only preserved artifacts are read).

### Observable Truths (ROADMAP Success Criteria)

| # | Truth (Success Criterion) | Status | Evidence |
|---|---------------------------|--------|----------|
| 1 | DIAG-01: per-trajectory ε_H over all 1,500 held-out trajectories, from preserved artifacts only (no evaluator, SCOPE-22); states uniform vs tail-driven with numbers | ✓ VERIFIED | `diag01/eps_h_distribution.py` reads **only** `runs/stage0-pilot-seed42/evaluation/metrics.json` (preserved, dated Jul 22, pre-phase); no evaluator/subprocess call. Re-run JSON byte-identical (SHA-256 `036e8c40…`). `n=1500`, `min=0.9741251227996501 > 1e-5` → **uniform failure**, `n_exceeding=1500/1500`, `frac=1.0`; heavy right tail `max/median=106.24`, `p99/median=24.66`; neither `variant` nor `fidelity` separates (both `separates_population=False`). |
| 2 | DIAG-02: per-step per-term decomposition across `stage0-smoke` + 3 pilot seeds; dominant term + warmup-spike (~3.7e9) attribution; PHYS-05 scheduled weights | ✓ VERIFIED | `diag02/loss_decomposition.json` (re-run byte-identical, SHA-256 `3e644b44…`): `loss_phys` dominant in every warmup spike — smoke 194/4.61e9, seed41 123/6.08e9, **seed42 100/3.735e9 (~3.7e9)**, seed43 169/3.83e9, shares 0.99998–0.99999, `grad_norm` 5.6e13–7.1e13. PHYS-05: `lambda_phys` first ≥1.0 at **step 31** (all runs); `lambda_l ≡ 0.0` at all 300 steps (asserted). `loss_phys` dominates both raw AND λ-weighted cumulative (no flip); 300/300 finite, 0 non-finite; smoke kept as separate fourth trace. |
| 3 | DIAG-03: three-seed characterization (budget-limited vs recipe instability) with cited per-seed evidence; Phase 38 overfit rung as machinery-integrity control | ✓ VERIFIED | `diag03/seed_band.json` (re-run byte-identical, SHA-256 `3c93be40…`): first-vs-last trends seed41 2.27e9→4.64e8 (improving), seed42 8.38e8→7.85e7 (improving), seed43 8.97e8→1.85e9 (worsening) = **1/3 worsened**; explicitly **DISAGREE** with 43-CAL "2/3", attributed to direction definition (last-window step200→300 gives seed41+seed43 = 2/3), adjudicating neither. `relative_span=3.8224247683129153` reproduces 43-CAL exactly (`matches_within_1e-9_rel=true`). Held-out split divergence: smoke==seed42 (identical SHA-256), seed41/seed43 diverge. Phase 38 rung cited verbatim (`ratio=1097.6107…`, PASS, 176 steps), flagged `CITATION-NOT-COMPUTATION`, never re-run (SCOPE-23). |
| 4 | DIAG-04: `44-DIAGNOSIS.md` ranks ≥4 causes each with supporting AND contradicting evidence; abstains from remedy; routes source-silent call to a gap register | ✓ VERIFIED | `44-DIAGNOSIS.md` §5 pre-registers an evidence-support rubric BEFORE §6's ranked table; §6 ranks **5** candidate causes (population-scale generalization Strong; loss-imbalance / optimization-warmup / normalization-scale Moderate declared tie, alphabetical; insufficient-budget Weak). Candidates 2–5 each carry supporting AND contradicting citations; candidate 1 uses the rubric-sanctioned "no contradicting evidence identified" (a Strong cause has none by definition — honest, not a gap). Remedy abstinence stated up front and in §7 (4× SCOPE-26). Source-silent gate-statistic call routed to **GAP-44-01** (§GAP section), resolved by owner instruction (option A), not decided by the agent. |
| 5 | Every reported number re-derivable: scripts + pinned inputs retained in the phase evidence directory | ✓ VERIFIED | `evidence/` holds all four scripts + JSON outputs + `manifest.json` + `README.md`. Re-run: diag01/02/03 JSONs byte-identical to committed; `build_manifest.py` reports "15 inputs pinned; all_match=True". `manifest.json` differs **only** in `git_head` (`8631576…`→ current `4788efb4…`) because HEAD advanced two commits after 44-04 — `git diff` confirms that single-line delta; all 15 input SHA-256 hashes match. Working tree restored after re-run (evidence/, runs/, pinn/, pinn_instruction/ all clean). |

**Score:** 5/5 truths verified (0 present, behavior-unverified)

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `evidence/diag01/eps_h_distribution.py` → `.json` | DIAG-01 ε_H distribution | ✓ VERIFIED | Read-only over preserved `metrics.json`; fail-closed (len==1500, exact max==top-level equality, key-set check); re-run byte-identical |
| `evidence/diag02/loss_decomposition.py` → `.json` | DIAG-02 five-term decomposition | ✓ VERIFIED | Read-only over 4 `train.log.jsonl`; fail-closed (26 required keys, step set {1..300}, `lambda_l==0` asserted); re-run byte-identical |
| `evidence/diag03/seed_band.py` → `.json` | DIAG-03 seed band | ✓ VERIFIED | Read-only over validation.jsonl/splits.json + 43-CAL + 38-VERIFICATION; fail-closed (median≠0 before division); re-run byte-identical |
| `evidence/build_manifest.py` → `manifest.json` | SHA-256 + git-head pinning | ✓ VERIFIED | Cross-checks all 15 provenance inputs against live tree; fails closed on any mismatch; only `subprocess` use is bounded `git rev-parse HEAD` |
| `44-DIAGNOSIS.md` | ≥4 ranked causes, remedy-abstinent | ✓ VERIFIED | 5 ranked causes, pre-registered rubric, [FACT]/[HYP] separation (23 FACT / 7 HYP), remedy abstinence, GAP routing |
| `44-GAPS.md` + `v2.1-GAPS.md` | STOP-protocol gap register | ✓ VERIFIED | GAP-44-01 full 11-field schema, RESOLVED-WITH-INSTRUCTION (owner option A); phase register, milestone index, and DIAGNOSIS agree |

### Scope-Boundary Compliance (SCOPE-22..26)

| Boundary | Requirement | Status | Evidence |
|----------|-------------|--------|----------|
| SCOPE-22 | No evaluator invocation | ✓ | Scripts read preserved `metrics.json`/logs only; no evaluator entry point called; grep for `evaluate/train/torch/os.system` finds only a citation string and the bounded git rev-parse |
| SCOPE-23 | No training / no executed diagnostic run | ✓ | Phase 38 rung cited `CITATION-NOT-COMPUTATION`, never re-run; discriminating tests marked "proposed only" |
| SCOPE-24 | No framework-spec edit | ✓ | Working tree under `pinn_instruction/` clean after re-run; GAP-44-01 resolution explicitly defers spec codification |
| SCOPE-26 | No remedy selected | ✓ | Remedy abstinence stated in header + §7; ranking is [HYP], selection owner-routed to trainex-r2 |

### Re-derivability Evidence (verifier-run)

| Output | Committed SHA-256 | Re-run SHA-256 | Verdict |
|--------|-------------------|----------------|---------|
| `diag01/eps_h_distribution.json` | `036e8c40…` | `036e8c40…` | ✓ byte-identical |
| `diag02/loss_decomposition.json` | `3e644b44…` | `3e644b44…` | ✓ byte-identical |
| `diag03/seed_band.json` | `3c93be40…` | `3c93be40…` | ✓ byte-identical |
| `manifest.json` | `d25f5b15…` | `84661e71…` | ⚠ expected — sole delta is `git_head` provenance stamp (HEAD advanced 2 commits); all 15 input hashes match, `all_match=True`. Not a re-derivability defect; substantive numbers do not depend on `git_head`. Working tree restored. |

### Anti-Patterns Found

None. No debt markers (`TODO`/`FIXME`/`XXX`/`HACK`) introduced in the four analysis
scripts or the diagnosis. No stub/hollow outputs: every JSON field is computed from
a pinned input and cross-checked. The scripts fail closed (write nothing on any
self-check failure) rather than emitting placeholder data.

### Requirements Coverage

| Requirement | Description | Status | Evidence |
|-------------|-------------|--------|----------|
| DIAG-01 | Per-trajectory ε_H distribution, preserved artifacts only | ✓ SATISFIED | Truth 1 |
| DIAG-02 | Five-term loss decomposition + spike attribution + PHYS-05 | ✓ SATISFIED | Truth 2 |
| DIAG-03 | Three-seed characterization + Phase 38 control | ✓ SATISFIED | Truth 3 |
| DIAG-04 | Ranked remedy-abstinent diagnosis + gap routing | ✓ SATISFIED | Truth 4 |

### Human Verification Required

None. All success criteria are mechanically verifiable and were confirmed by the
verifier directly (re-run byte-identity, field-by-field number tracing, script
read-only/fail-closed inspection, scope-boundary tree cleanliness). Consistent with
the established practice for trainex/specwork acceptance phases, the verifier ran the
semantic/contract checks rather than deferring them. There are no runtime state
transitions or cancellation/cleanup invariants in a static forensics deliverable, so
no present-but-behavior-unverified items arise.

### Gaps Summary

No gaps. GAP-44-01 (the source-silent max-vs-aggregate gate-statistic question) is a
correctly-handled STOP-protocol item — surfaced by the phase, RESOLVED-WITH-INSTRUCTION
by the owner (option A: worst-case max is the gate statistic, 2026-07-23), and reflected
consistently across `44-GAPS.md`, `v2.1-GAPS.md`, and `44-DIAGNOSIS.md`. It is not an open
blocker. The choice is verdict-neutral (1500/1500 trajectories fail the per-trajectory rule
individually, so FAIL holds under any aggregate).

The phase goal is achieved: the held-out ε_H distribution, the training-time loss
composition, and the seed band are each quantified from retained artifacts; the
hypothesis-ranked `44-DIAGNOSIS.md` gives an evidence map of five candidate causes with
the remedy deliberately left open; and every reported number is mechanically re-derivable.

---

_Verified: 2026-07-24T06:28:31Z_
_Verifier: Claude (gsd-verifier)_
