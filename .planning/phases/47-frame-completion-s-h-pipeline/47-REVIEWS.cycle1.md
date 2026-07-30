---
phase: 47
reviewers: [codex, codex1, claude-max, claude-alt]
rerun_reviewers: [codex, codex1, claude-max, claude-alt]
reviewed_at: 2026-07-30T07:39:26Z
generated_by: xreview
xreview_run_dir: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260730T073326Z-55205
---

# Cross-AI Plan Review — Phase 47

## codex Review

_codex failed: returned empty output, failed, or timed out._

Diagnostics:
- reviewer=codex
- exit_code=143
- elapsed_seconds=360
- timeout_seconds=360
- watchdog=triggered
- timeout_after_seconds=360
- command=codex exec --ephemeral --dangerously-bypass-hook-trust --model gpt-5.5 -c model_reasoning_effort=\"xhigh\" --skip-git-repo-check - 
- stdout_bytes=0
- stderr_bytes=298277

Artifacts:
- stdout: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260730T073326Z-55205/xreview-codex-47.md
- stderr: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260730T073326Z-55205/xreview-codex-47.err
- metadata: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260730T073326Z-55205/xreview-codex-47.meta

Stderr excerpt:
```
ase40/test_grad_clip.py:23:MODULE = "pinn.training.grad_clip"
tests/phase40/test_grad_clip.py:391:    unittest.main()

hook: PostToolUse
hook: PostToolUse
hook: PostToolUse
hook: PostToolUse
hook: PostToolUse
hook: PostToolUse
exec
/bin/zsh -lc 'rg -n "def _synthetic_split_sources|SimpleNamespace|stage_label|k0|uabs0|records_at_or_below|snapshot_positions" pinn/train.py tests/phase41/test_train_entrypoint.py' in <home>/Desktop/3_body_problem/.worktrees/trainex
 succeeded in 0ms:
pinn/train.py:208:def _synthetic_split_sources(
pinn/train.py:218:    from types import SimpleNamespace
pinn/train.py:237:        def records_at_or_below(self, k):
pinn/train.py:244:            return SimpleNamespace(
pinn/train.py:247:                stage_label=StageLabel.STAGE_0,
pinn/train.py:261:        def snapshot_positions(self, key):
pinn/train.py:279:        def stage_label(self, key):

hook: PostToolUse
hook: PostToolUse
hook: PostToolUse
hook: PostToolUse Completed
hook: PostToolUse Completed
hook: PostToolUse Completed
hook: PostToolUse Completed
hook: PostToolUse Completed
hook: PostToolUse Completed
hook: PostToolUse Completed
hook: PostToolUse Completed
hook: PostToolUse Completed

```

---

## codex1 Review

_codex1 failed: returned empty output, failed, or timed out._

Diagnostics:
- reviewer=codex1
- exit_code=143
- elapsed_seconds=360
- timeout_seconds=360
- watchdog=triggered
- timeout_after_seconds=360
- command=env CODEX_HOME=<home>/.codex1 codex exec --ephemeral --dangerously-bypass-hook-trust --model gpt-5.6-sol -c model_reasoning_effort=\"xhigh\" --skip-git-repo-check - 
- stdout_bytes=0
- stderr_bytes=252422

Artifacts:
- stdout: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260730T073326Z-55205/xreview-codex1-47.md
- stderr: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260730T073326Z-55205/xreview-codex1-47.err
- metadata: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260730T073326Z-55205/xreview-codex1-47.meta

Stderr excerpt:
```
nk_size", 1024, "RESEARCH Open Question 2 accumulate-in-closure chunk"),
    ("opt.validation_every", 10, "CTX-49 validation_every provisional"),
    ("opt.adam_lr_base", 1e-3, "ctl_instruction.md consolidated schedule LR 1e-3·0.7^k"),
    ("opt.adam_lr_decay", 0.7, "ctl_instruction.md consolidated schedule LR 1e-3·0.7^k"),
    # ⚖ Phase-41 owner-carved seams (D4-a / R-1) — provisional, not ratified.
    (
        "run.checkpoint.wall_clock_ceiling_s",
        _PROVISIONAL_WALL_CLOCK_CEILING_S,
        "⚖ PROVISIONAL (D4-a): owner-ratify-before-run-#1 wall-clock checkpoint "
        "ceiling in seconds; mechanism ships, value is owner-carved",
    ),
    (
        "run.guards.loss_explosion_ceiling",
        _PROVISIONAL_LOSS_EXPLOSION_CEILING,
        "⚖ R-1: OWNER-RATIFIED via delegation 2026-07-21 at value 1e11 "
        "(calibrated from the 43-06 diagnostic peak ~4e9, MPS/fp32, ~25x "
        "headroom); explicitly revisable at the ACC-05 Stage-0 pilot. Still "
        "surfaced here (provisional=True) as part of the shared R-1 "

hook: PostToolUse
hook: PostToolUse
hook: PostToolUse
hook: PostToolUse Completed
hook: PostToolUse Completed
hook: PostToolUse Completed

```

---

## claude-max Review

I have verified the plans against the live code and grounding docs. All listed files were readable; I additionally confirmed key code seams, the referenced `47-VALIDATION.md`, the probe manifests, and the current frame constant. Here is the review.

---

# Cross-AI Plan Review — Phase 47 (Frame Completion & S_H Pipeline)

## 1. Summary

Three strictly-sequential plans discharge CONF-09 → CONF-02 → CONF-03. 47-01 swaps residency to the rotation-gauged/`D`-`V`-scaled `pre.r_gauge`/`pre.v_gauge`, re-ratifies `RATIFIED_VALIDATION_FRAME` to the scaled triple, and corrects the one phase-46 pairing test — all in one atomic commit — plus a CONF-09 invariant suite and a one-shot record-only re-probe. 47-02 builds the `S_H = median_train(K0+Uabs0)` pipeline (float64 admission capture via a loss-catalog component seam, train-split median at setup, fail-closed `training_metadata.json`). 47-03 wires `ε_H = 1e-4·S_H` through a required keyword-only `RunController(s_h=…)` channel and deletes the prohibited `+1e-12` floor.

The plans map cleanly onto ROADMAP SC-1…SC-5 and are exceptionally well-grounded. I verified the core seams against live code: adapter residency at `:865/866/871/875`, single `AdmittedRecord(` site, `kinetic`/`potential` as separate locals in `_matched_plummer_hamiltonian`, the `:482` floor (`1e-12` count = 2, both in the deleted block), `records_at`/`records_at_or_below`/`_source_value`/`from_split`, and the current frame = `(RAW, RAW, ORDERED_RAW)` — all as the plans describe.

## 2. Strengths

- **Load-bearing ordering is correct and physically justified.** `S_H` is frame-dependent (`H'=D·H`); enforcing frame → statistic → wiring via `wave`/`depends_on` prevents computing `S_H` twice. Intra-plan task order is also clean (swap → invariants → re-probe).
- **Atomicity of the frame swap.** Forcing residency + `RATIFIED_VALIDATION_FRAME` + pairing-test into one commit (47-01 crit 7) is the right call — it eliminates any tree where `COHERENT_FRAME_PAIRS` silently lies. I confirmed `(POSITION_FRAME_SCALED, TIME_COORD_NORMALIZED)` is already an admitted pair, so re-ratification won't throw.
- **Scope discipline is grep-enforced, not aspirational.** Dual-epsilon separation (`EPS_SOFT` vs `EPS_INV`), no-fallback-floor, `preprocessing.py`/`loss_catalog.py` byte-unchanged, single-oracle correction — each is a concrete acceptance gate. This directly targets the milestone's "single easiest mis-scale."
- **Strong data-integrity posture:** fail-closed at setup before step 1, atomic writes, re-validate-on-load, one-shot re-probe cap + mandatory "NOT a frame verdict" framing. Verification is dataset-free/train-free.
- **Drift-resistant.** Line numbers were re-verified live and the plans instruct symbol-greps before editing; I confirmed the flagged stale `:526-528` citation and the corrected `:788` anchor.

## 3. Concerns

**HIGH** — none that are architectural. The design is sound; the items below are execution/coverage risks.

**MEDIUM — `problematic_ics_blacklist.json` is absent from the worktree.** The seed41/42/43 `splits.json` manifests exist, but `find` locates no blacklist anywhere. 47-01 Task 3 invokes the probe with `--blacklist-path problematic_ics_blacklist.json` and instructs "if the blacklist is missing … STOP and surface." As written, Task 3 will halt and block phase closure. This fails safe (no silent corruption), but it is a concrete blocker that should be pre-staged or path-corrected before execution.

**MEDIUM — the D-08 tolerance is the single most fragile element.** `test_gate_metric_near_invariance` must use a first-principles softening-floor tolerance and is explicitly forbidden from tuning it to observed output; Task 3 then records the measured max-difference against that same constant. If the a-priori bound is miscalibrated (too tight), the test fails and the executor has no sanctioned escape except declaring a real defect. This rigor is intentional, but it concentrates risk on one hand-derived number. Mitigation is available (derive a conservative *upper* bound on the floor-binding term rather than an estimate), but the plans should state that the bound must be an upper bound, not a fit.

**MEDIUM — the resume recompute-and-compare path is asserted but untested.** 47-02 Task 2(b) and the 47-03 idempotency `must_have` describe recomputing `S_H` on resume and refusing on mismatch with the persisted artifact. No test node exercises this `train.py` orchestration; `test_metadata_roundtrip_revalidates` covers only load-side validation. Add a node that writes an artifact, mutates the live source, and asserts the resume path refuses (rather than overwrites).

**LOW — "COM/momentum test passes byte-unmodified" depends on scale-relative tolerance.** After the fixture is rescaled, `test_resident_trajectory_preserves_com_and_zero_momentum_gauge` (`:223`) runs on scaled arrays. The gauge invariants (COM=0, Σmᵢv=0) are scale-invariant, so physics supports the claim — but if that test hardcodes an absolute `atol`, it could break, creating a tension with the "byte-unmodified" requirement vs. the "fix any third failure" catch-all. Worth confirming the test's tolerance is relative before relying on the byte-unmodified guarantee.

**LOW — stale line anchors in grounding docs.** ROADMAP SC-2 and CONTEXT D-05 still cite `validation_gate.py:526-528`; the live symbol is `:788-796`. Execution is robust (symbol-grep), but the success-criterion text carries a wrong anchor — a traceability nit.

**LOW — `grep | wc -l` sweep gate (47-03 crit 4) is brittle.** It assumes every textual `RunController(` is a real construction. True today (13 = 12 tests + `train.py`), but any future comment/string occurrence would make the gate unsatisfiable without touching unrelated code.

**LOW — `compute_s_h` on a source without accessors.** The "still refuses fail-closed" claim would surface as `AttributeError`, not a `ValueError` naming the predicate — not truly fail-closed-with-reason. Minor.

## 4. Suggestions

1. Before executing 47-01 Task 3, locate or regenerate `problematic_ics_blacklist.json` (or correct the invocation's path/cwd assumption) so the one-shot re-probe does not stall the phase; if it is intentionally generated, document where.
2. Specify in 47-01/47-02 that the D-08 tolerance must be a derived **upper bound** on the softening-floor asymmetry, and record the derivation inline — closing the "what if the bound is too tight" trap.
3. Add a resume-path test (write → perturb source → assert refusal) to 47-02 or 47-03 so the idempotency `must_have` has a green node behind it.
4. Confirm `test_resident_trajectory_preserves_com_and_zero_momentum_gauge` uses a relative/scale-derived tolerance; if not, note it explicitly as an expected in-place edit rather than "byte-unmodified."
5. Fix the `:526-528` → `:788-796` anchor in ROADMAP SC-2 / CONTEXT D-05 during this phase (or note it for VER-20 routing) to keep grounding traceable.

## 5. Overall Risk: **MEDIUM**

The architecture, ordering, and scope discipline are excellent, and the code seams verify as described — there is no design-level risk. The rating is driven by three controllable execution/coverage items: the confirmed-absent probe blacklist (will block Task 3), the hand-derived D-08 tolerance concentrating numeric risk, and the untested resume recompute-compare path. All are fixable before execution; resolving suggestions 1–3 would bring this to LOW.

---

## claude-alt Review

I have read all three plans plus CONTEXT and VALIDATION, and cross-checked the roadmap/requirements citations they depend on. Here is the review.

---

# Phase 47 Plan Review — Frame Completion & S_H Pipeline

## 1. Summary

Phase 47 discharges three conformance defects in strict wave order: **47-01 (CONF-09)** completes residency to the rotation-gauged, `D`/`V`-scaled frame and re-ratifies `RATIFIED_VALIDATION_FRAME` in the same atomic commit; **47-02 (CONF-02)** builds the `S_H = median_train(K0 + Uabs0)` float64 pipeline with a fail-closed `training_metadata.json` artifact; **47-03 (CONF-03)** wires `ε_H = 1e-4·S_H` through a required `RunController` constructor channel and deletes the spec-prohibited additive floor. The plans are exceptionally well-grounded — every decision carries a `[GROUNDED]`/`[JUDGEMENT]` provenance tag traceable to CONTEXT D-01…D-27, and the dependency ordering (frame → statistic → wiring) is physically justified (`S_H` is frame-dependent via `H'=D·H`). All ten VALIDATION node IDs map cleanly to task `<verify>` blocks. I found no correctness defect that blocks execution; concerns are about acceptance-check brittleness and one external dependency.

## 2. Strengths

- **Grounding discipline is the strongest feature.** Semantic decisions are separated from mechanical ones; the swap is correctly framed as "three lines; the proof is the work" (IC₁₃ invariance, velocity identity, gate-metric near-invariance).
- **Atomicity of the CONF-09 change** (residency + frame constant + pairing-test correction in one commit, criterion 7) correctly prevents a tree where `COHERENT_FRAME_PAIRS` lies.
- **Fail-closed data-integrity design** is thorough: strict-positive predicate (exact `0.0` rejected), empty/single-element population cases, atomic write, re-validate-on-load, resume recompute-and-compare, refusal-precedes-artifact. Genuinely good edge coverage.
- **Dual-epsilon defense** (`EPS_SOFT=1e-5` vs `EPS_INV=1e-10`) is enforced by a negative grep gate, not just prose — this is the milestone's easiest silent mis-scale and the plan treats it accordingly.
- **Line-number staleness is pre-empted:** 47-01 flags the stale `validation_gate.py:526-528` citation carried in CONTEXT/REQUIREMENTS and instructs grep-by-symbol.

## 3. Concerns

**MEDIUM — Brittle exact-string grep acceptance criteria.** Several gates assert `grep -c` on exact-formatted source lines: 47-02 criterion 4 (`compute_invariants(pre.masses_ordered, pre.r0_gauge, pre.v0_gauge)` == 1), 47-03 criterion 3 (`energy_floor_factor) \* self._s_h` == 1). These pass only under one exact whitespace/line-break rendering. A correct implementation formatted differently (e.g. Black wrapping a multi-line call) fails the gate. Since the executor authors to match, this mostly causes churn, but it couples "verified" to formatting rather than behavior.

**MEDIUM — Task 3 (47-01) external-manifest dependency can stall phase closure.** The one-shot D-22 re-probe requires `runs/stage0-pilot-seed4*/splits.json` and `problematic_ics_blacklist.json` on disk; the plan correctly says STOP-and-surface if absent. That is the right safety behavior, but it means an evidence-only task can block a plan whose *code* is already complete. Worth confirming those artifacts exist in the `trainex` worktree before execution, so closure doesn't halt on missing corpus paths.

**LOW — `train.py` line drift between waves.** 47-02 inserts the `compute_s_h`/persist block before `RunController(...)`, shifting it below the `:964` that 47-03's `read_first` cites as the construction site. 47-03 does say the call is "all-keyword" and to thread `s_h=s_h`, and greps by symbol, so this is self-correcting — but the cited line will be stale by the time 47-03 runs.

**LOW — Sweep-completeness gate (47-03 criterion 4)** compares `grep -rn "RunController(" pinn/ tests/ | wc -l` against sites carrying `s_h=`. This counts any textual `RunController(` occurrence (comments, docstrings, future call sites) and assumes exactly the 12 enumerated sites plus `train.py`. A stray reference or an untracked construction site elsewhere in `pinn/`/`tests/` would silently break the equality. The per-file cross-check mitigates this.

**LOW — CONTEXT still cites superseded line numbers** (D-05 `526-528`, D-19 `:482`/`:480-481`). The plans handle it, but downstream readers of CONTEXT alone could be misled.

## 4. Suggestions

- Soften the exact-line greps to intent-level checks: use `grep -n 'self\._s_h'` plus a targeted pytest assertion on the computed `eps_h`, rather than pinning whitespace; likewise assert `k0`/`uabs0` derive from the seam via a test rather than an exact-argument grep on `compute_invariants(...)`.
- Add an explicit pre-flight in 47-01 Task 3 (or the phase preamble) that checks the probe manifests/blacklist exist and surfaces early, so the stall — if any — happens before Tasks 1–2 rather than at closure.
- In 47-03 criterion 4, exclude comments/strings from the `RunController(` count or assert the exact expected site count (13) to avoid a false pass/fail from stray text.
- Consider a one-line note in 47-03 that `train.py:964` is pre-47-02 numbering (grep the `RunController(` symbol), to remove the only cross-wave stale anchor.

## 5. Overall Risk

**LOW.** The plans are rigorous, well-sequenced, and correctly scoped (no framework-spec edits, no training runs, no tuning; test-file edits in 47-03 are a necessary consequence of the required constructor parameter, not scope creep). Data-integrity and destructive-operation risk is negligible — fail-closed throughout, atomic writes, one-shot capped probe with STOP-on-missing-input. The residual risks are acceptance-check brittleness (self-imposed, executor-correctable) and one external-artifact dependency that is already guarded by a STOP clause. No correctness or ordering defect was found that would prevent the plan set from achieving the five ROADMAP success criteria.

---

## Consensus Summary
_Synthesize shared concerns across reviewers above (2+ agreement = highest priority)._

## xreview Diagnostics

### codex
- reviewer=codex
- exit_code=143
- elapsed_seconds=360
- timeout_seconds=360
- watchdog=triggered
- timeout_after_seconds=360
- command=codex exec --ephemeral --dangerously-bypass-hook-trust --model gpt-5.5 -c model_reasoning_effort=\"xhigh\" --skip-git-repo-check - 
- stdout_bytes=0
- stderr_bytes=298277

### codex1
- reviewer=codex1
- exit_code=143
- elapsed_seconds=360
- timeout_seconds=360
- watchdog=triggered
- timeout_after_seconds=360
- command=env CODEX_HOME=<home>/.codex1 codex exec --ephemeral --dangerously-bypass-hook-trust --model gpt-5.6-sol -c model_reasoning_effort=\"xhigh\" --skip-git-repo-check - 
- stdout_bytes=0
- stderr_bytes=252422

### claude-max
- reviewer=claude-max
- exit_code=0
- elapsed_seconds=342
- timeout_seconds=360
- watchdog=not_triggered
- command=ccp claude-max --model claude-opus-4-8 -p - 
- stdout_bytes=7500
- stderr_bytes=0

### claude-alt
- reviewer=claude-alt
- exit_code=0
- elapsed_seconds=135
- timeout_seconds=360
- watchdog=not_triggered
- command=ccp alt --model claude-opus-4-8 -p - 
- stdout_bytes=5978
- stderr_bytes=0
