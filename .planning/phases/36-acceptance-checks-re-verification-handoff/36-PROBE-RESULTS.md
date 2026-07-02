# Phase 36: Probe Results

Fresh execution date: 2026-07-02T00:11:08Z

Interpreter: `python3 3.14.5`

Environment evidence:

- `.planning/phases/36-acceptance-checks-re-verification-handoff/evidence/python_environment.stdout.txt`
- SHA-256: `4373dc77149071d1f8b0c4a57ff9a06c5e1f3649cff98e8c40fa60cdb586a23f`

All 26 Phase 36 disposable acceptance probes executed. Each probe's raw stdout is captured in a committed evidence file; this document summarizes that captured output rather than replacing it.

## OVERALL VERDICT: BLOCKED

**Status:** BLOCKED — 15/26 required probes failed (58% failure rate)

**Route-back targets:**
- CURR failures (4 probes) → Phase 33 (adaptive stage assignment, stage transitions, L_norm metadata, s_min gate)
- LOOP failures (3 probes) → Phase 34 (replay/lookahead batching, gradient clipping mechanism, ALM μ_p clamp)
- LOSS failures (4 probes) → Phase 35 (loss scaling, componentwise AD, energy-weight schedule, Huber-δ)
- EVID-15 failures (3 probes) → Phase 32 (D=6.694 conflict transcription, D-05/D06 epsilon strategy)
- PROTECTED-PATH-GUARD (1 probe) → Phase 36 (probe self-matching bug)

**Blocking condition:** Per Plan 36-02 Prohibition 2, any required FAIL or missing-evidence must be recorded as BLOCKED with a route-back target, not an advisory note. Phase 36 cannot proceed to completion until these failures are resolved.

---

## CURR Family

### AC-CURR-01

- **Status:** FAIL
- **Command:** `bash .planning/phases/36-acceptance-checks-re-verification-handoff/probes/ac-curr-01.sh`
- **Raw stdout evidence:** `.planning/phases/36-acceptance-checks-re-verification-handoff/evidence/AC-CURR-01.stdout.txt`
- **SHA-256:** `bbe7f0e50840a3205d6b6493431c75bcb2e7affec510a98a1eb310aee808332e`
- **Observed metric:** Check [3] failed (Table 4 rejection)
- **Pass criterion:** Methodology tokens present + Table 4 rejected + population safeguard owner-pending
- **Route-back:** Phase 33 (stage assignment transcription)

### AC-CURR-02-LMAX

- **Status:** PASS
- **Command:** `python3 .planning/phases/36-acceptance-checks-re-verification-handoff/probes/ac-curr-02-lmax.py`
- **Raw stdout evidence:** `.planning/phases/36-acceptance-checks-re-verification-handoff/evidence/AC-CURR-02-LMAX.stdout.txt`
- **SHA-256:** `3bb6cd011c9dfad09b7d6e67838e0a5f550697c043d89e9d6e1fe653d5f68ab5`
- **Observed metric:** D ≈ 4.6416 formula-sanity check passed
- **Pass criterion:** Raw-mass D characteristic scale verified; rejected value absent

### AC-CURR-02-M7

- **Status:** PASS
- **Command:** `bash .planning/phases/36-acceptance-checks-re-verification-handoff/probes/ac-curr-02-m7.sh`
- **Raw stdout evidence:** `.planning/phases/36-acceptance-checks-re-verification-handoff/evidence/AC-CURR-02-M7.stdout.txt`
- **SHA-256:** `9a92ddd58cd08060c4157461b338f16a284464cc6a72729598cde4bd7c23d637`
- **Observed metric:** τ_L outside IC₁₃ assertion passed
- **Pass criterion:** `tau_L` is staging/eval metadata, outside IC₁₃ by design

### AC-CURR-03

- **Status:** FAIL
- **Command:** `bash .planning/phases/36-acceptance-checks-re-verification-handoff/probes/ac-curr-03.sh`
- **Raw stdout evidence:** `.planning/phases/36-acceptance-checks-re-verification-handoff/evidence/AC-CURR-03.stdout.txt`
- **SHA-256:** `ede71a197174113eca8e78edf4b20c6e71ea44eb5afa434e29d848813d402729`
- **Observed metric:** Check [1] failed (ADVANCE/RECOVER/HALT-REVIEW state machine tokens)
- **Pass criterion:** ADVANCE / RECOVER / HALT-REVIEW state machine anchored in `## Stage Transition Criteria`
- **Route-back:** Phase 33 (stage transition criteria transcription)

### AC-CURR-04

- **Status:** FAIL
- **Command:** `bash .planning/phases/36-acceptance-checks-re-verification-handoff/probes/ac-curr-04.sh`
- **Raw stdout evidence:** `.planning/phases/36-acceptance-checks-re-verification-handoff/evidence/AC-CURR-04.stdout.txt`
- **SHA-256:** `dc84018e83d761b57052c5399ff0fb145eba4c8b0f622cee56a59efb148dc10d`
- **Observed metric:** Check [1] failed (raw un-clipped L_norm metadata token)
- **Pass criterion:** Raw un-clipped `L_norm` metadata + mandatory nonfinite/near-degenerate `L_max` guard; "No global clamp is authorized"; `np.clip` gate NOT locked
- **Route-back:** Phase 33 (Stage 0-6 inventory transcription)

### AC-CURR-05

- **Status:** FAIL
- **Command:** `bash .planning/phases/36-acceptance-checks-re-verification-handoff/probes/ac-curr-05.sh`
- **Raw stdout evidence:** `.planning/phases/36-acceptance-checks-re-verification-handoff/evidence/AC-CURR-05.stdout.txt`
- **SHA-256:** `d4bc4fb827a473e4bab544cd6f7c82529e152c113f8e31d7dd149b98958557b8`
- **Observed metric:** Check [2] failed (matched-Plummer loss-side, epsilon dual context)
- **Pass criterion:** Unsoftened geometric `s_min` gate; dual-context epsilon; rejected clip constant absent
- **Route-back:** Phase 33 (s_min gate + epsilon strategy transcription)

---

## LOOP Family

### AC-LOOP-01

- **Status:** FAIL
- **Command:** `bash .planning/phases/36-acceptance-checks-re-verification-handoff/probes/ac-loop-01.sh`
- **Raw stdout evidence:** `.planning/phases/36-acceptance-checks-re-verification-handoff/evidence/AC-LOOP-01.stdout.txt`
- **SHA-256:** `8d62147b96e8b2a65bb8cf0e75b0122ed651590a62d9790ec7e630c925c758c2`
- **Observed metric:** Check [2] failed (B_replay=240, B_lookahead=16)
- **Pass criterion:** `B_replay=240`, `B_lookahead=16`, `has_stage(k+1)` guard; edge-case policy transcribed
- **Route-back:** Phase 34 (replay/lookahead batching transcription)

### AC-LOOP-02

- **Status:** PASS
- **Command:** `bash .planning/phases/36-acceptance-checks-re-verification-handoff/probes/ac-loop-02.sh`
- **Raw stdout evidence:** `.planning/phases/36-acceptance-checks-re-verification-handoff/evidence/AC-LOOP-02.stdout.txt`
- **SHA-256:** `e47dcb82b5218877df87519b032786c4d0f42432ee2577f758e823f53ffc4090`
- **Observed metric:** Two independent point sets + 8192/4096 provisional tokens present
- **Pass criterion:** Two independent point sets (data-fidelity vs collocation, 8192/4096 provisional); data-fidelity 50/50 retained, collocation 50/50 deferred

### AC-LOOP-04

- **Status:** FAIL
- **Command:** `python3 .planning/phases/36-acceptance-checks-re-verification-handoff/probes/ac-loop-04.py`
- **Raw stdout evidence:** `.planning/phases/36-acceptance-checks-re-verification-handoff/evidence/AC-LOOP-04.stdout.txt`
- **SHA-256:** `6b8e9e8a7fb19c1d6cd7f582fc79af65731b64d55910537520f98c0fbdc9cfdc`
- **Observed metric:** Check [2] failed (C-schedule 7-10 / 5 / 3, rejected clip constant)
- **Pass criterion:** Mechanism `clip_value = C_stage·median(grad_norm_history)`; C-schedule `7-10 / 5 / 3`; rejected clip constant absent
- **Route-back:** Phase 34 (gradient clipping mechanism transcription)

### AC-LOOP-05

- **Status:** FAIL
- **Command:** `bash .planning/phases/36-acceptance-checks-re-verification-handoff/probes/ac-loop-05.sh`
- **Raw stdout evidence:** `.planning/phases/36-acceptance-checks-re-verification-handoff/evidence/AC-LOOP-05.stdout.txt`
- **SHA-256:** `6df61693ac2642712499091784aa88e28ac660e1b392db41a6789374dc1d68f7`
- **Observed metric:** Check [2] failed (ALM deferred/optional, dense-residual ALM rejected)
- **Pass criterion:** ALM deferred/optional; dense-residual ALM rejected from default loss; `[1e-4,100]` clamp conditional only
- **Route-back:** Phase 34 (ALM μ_p clamp transcription)

### AC-LOOP-06

- **Status:** PASS
- **Command:** `bash .planning/phases/36-acceptance-checks-re-verification-handoff/probes/ac-loop-06.sh`
- **Raw stdout evidence:** `.planning/phases/36-acceptance-checks-re-verification-handoff/evidence/AC-LOOP-06.stdout.txt`
- **SHA-256:** `165713fbce6b877410b88569f62109cb86d00006de78d6b40c21ded781c3aa86`
- **Observed metric:** Negative check passed (no probe-able collocation-scaling formula)
- **Pass criterion:** Realized-as-deferred; no probe-able `n_col=` formula; inverse form NOT adopted

### LOOP-07

- **Status:** PASS
- **Command:** `bash .planning/phases/36-acceptance-checks-re-verification-handoff/probes/ac-loop-07.sh`
- **Raw stdout evidence:** `.planning/phases/36-acceptance-checks-re-verification-handoff/evidence/LOOP-07.stdout.txt`
- **SHA-256:** `2947028c50fbecfb882a9ff81006325f7d60b75d95c943ead135f1131e90e081`
- **Observed metric:** Provisional tokens IPR/PSC/provisional/VAL-03/VAL-04 present
- **Pass criterion:** Provisional carry-forward; `IPR`/`PSC`/`provisional`/`VAL-03`/`VAL-04` tokens present
- **Evidence anchor:** 34-VERIFICATION.md truth 6 (no dedicated ledger row)

### LOOP-08

- **Status:** PASS
- **Command:** `bash .planning/phases/36-acceptance-checks-re-verification-handoff/probes/ac-loop-08.sh`
- **Raw stdout evidence:** `.planning/phases/36-acceptance-checks-re-verification-handoff/evidence/LOOP-08.stdout.txt`
- **SHA-256:** `3ab4eaa66ac4ab3dda9b7dbb2d1f835d9bb51c11a6d5fa449becce18b4c85b11`
- **Observed metric:** Provisional tokens SASD/provisional/VAL-02 present
- **Pass criterion:** Provisional carry-forward; `SASD`/`provisional`/`VAL-02` tokens present
- **Evidence anchor:** 34-VERIFICATION.md truth 7 (no dedicated ledger row)

---

## LOSS Family

### AC-LOSS-01

- **Status:** FAIL
- **Command:** `bash .planning/phases/36-acceptance-checks-re-verification-handoff/probes/ac-loss-01.sh`
- **Raw stdout evidence:** `.planning/phases/36-acceptance-checks-re-verification-handoff/evidence/AC-LOSS-01.stdout.txt`
- **SHA-256:** `c3cd84a1e6fb3e61d3785064c009c1c66dfe1b22874049c160303282dd30726d`
- **Observed metric:** Check [2] failed (dimensionless L_data/L_physics/L_energy, no linear-momentum)
- **Pass criterion:** Dimensionless `L_data`/`L_physics`/`L_energy`; no linear-momentum term
- **Route-back:** Phase 35 (loss scaling transcription)

### AC-LOSS-01-AD

- **Status:** FAIL
- **Command:** `python3 .planning/phases/36-acceptance-checks-re-verification-handoff/probes/ac-loss-01-ad.py`
- **Raw stdout evidence:** `.planning/phases/36-acceptance-checks-re-verification-handoff/evidence/AC-LOSS-01-AD.stdout.txt`
- **SHA-256:** `f3fca34e321dc70dc8295a5a9b049738741f6355264862e4d642f30347867407`
- **Observed metric:** Check [1] failed (summed-output VJP rejected)
- **Pass criterion:** Componentwise AD, canonical `u=t/T` leaf; summed-output VJP rejected
- **Route-back:** Phase 35 (componentwise AD transcription)

### AC-LOSS-02

- **Status:** FAIL
- **Command:** `python3 .planning/phases/36-acceptance-checks-re-verification-handoff/probes/ac-loss-02.py`
- **Raw stdout evidence:** `.planning/phases/36-acceptance-checks-re-verification-handoff/evidence/AC-LOSS-02.stdout.txt`
- **SHA-256:** `1ccbf0108cb21abfc8aa523a196a74be207d0e3c9f607a9df5938b7ef5091db2`
- **Observed metric:** Check [2] failed (PHYS-05 λ_E^max ≤ 1.0, rejected cap-table)
- **Pass criterion:** Adjudicated M15: retain PHYS-05 `λ_E^max ≤ 1.0`; issue-doc cap-table replacement REJECTED; rejected saturated weight absent
- **Route-back:** Phase 35 (energy-weight schedule transcription)

### AC-LOSS-03

- **Status:** FAIL
- **Command:** `bash .planning/phases/36-acceptance-checks-re-verification-handoff/probes/ac-loss-03.sh`
- **Raw stdout evidence:** `.planning/phases/36-acceptance-checks-re-verification-handoff/evidence/AC-LOSS-03.stdout.txt`
- **SHA-256:** `63d406d32b742427ff7ad20ed43c517d3481c46cd293a48f91784efa70d0ccad`
- **Observed metric:** Check [1] failed (delta_E=1.0 baseline)
- **Pass criterion:** `delta_E=1.0` baseline retained; empirical/median-scaled calibration deferred; no per-stage δ table locked
- **Route-back:** Phase 35 (Huber-δ transcription)

### AC-LOSS-04

- **Status:** PASS
- **Command:** `bash .planning/phases/36-acceptance-checks-re-verification-handoff/probes/ac-loss-04.sh`
- **Raw stdout evidence:** `.planning/phases/36-acceptance-checks-re-verification-handoff/evidence/AC-LOSS-04.stdout.txt`
- **SHA-256:** `f314d36a940f190a715e4ba330bddda459ef837cf534d718c0ab6e66ddc768a8`
- **Observed metric:** D-04 Option A tokens present; dense-residual pseudo-ALM rejected; scalar ALM deferred
- **Pass criterion:** D-04 Option A: per-time causal weighting; dense-residual pseudo-ALM rejected; scalar ALM deferred P2

---

## EVID-15 Headlines

### AC-EVID-15-D-CONFLICT

- **Status:** FAIL
- **Command:** `bash .planning/phases/36-acceptance-checks-re-verification-handoff/probes/ac-evid-15-d-conflict.sh`
- **Raw stdout evidence:** `.planning/phases/36-acceptance-checks-re-verification-handoff/evidence/AC-EVID-15-D-CONFLICT.stdout.txt`
- **SHA-256:** `2f6998517ee38090c64be860b33edfaf97771292f5d4463b77b8d9ed4c1f15f1`
- **Observed metric:** Check [1] failed (D = 6.694 present in ctl_instruction.md)
- **Pass criterion:** `D ≈ 4.6416` active; rejected raw-mass D value described only, not transcribed
- **Route-back:** Phase 32 (D-6.694 conflict transcription)

### AC-EVID-15-D05

- **Status:** FAIL
- **Command:** `bash .planning/phases/36-acceptance-checks-re-verification-handoff/probes/ac-evid-15-d05.sh`
- **Raw stdout evidence:** `.planning/phases/36-acceptance-checks-re-verification-handoff/evidence/AC-EVID-15-D05.stdout.txt`
- **SHA-256:** `d46d062819a0bbc0e0d20bcf1b85e454301e2d192c35e85cc7a1b61bbbc7d75a`
- **Observed metric:** Check [1] failed (D-05 owner Option A transcription)
- **Pass criterion:** Owner Option A (geometric gate + matched-Plummer loss-side)
- **Route-back:** Phase 32 (D-05 owner transcription)

### AC-EVID-15-D06

- **Status:** FAIL
- **Command:** `bash .planning/phases/36-acceptance-checks-re-verification-handoff/pro-evid-15-d06.sh`
- **Raw stdout evidence:** `.planning/phases/36-acceptance-checks-re-verification-handoff/evidence/AC-EVID-15-D06.stdout.txt`
- **SHA-256:** `e0ca3d889dbc7d7b6453d9a8f2ab1515c6e237ed18a2337c76e5369d982bcce5`
- **Observed metric:** Check [1] failed (D-06 dual-context epsilon transcription)
- **Pass criterion:** Owner dual-context (`epsilon_inv=1e-10` / `epsilon_train=1e-5`)
- **Route-back:** Phase 32 (D-06 dual-context transcription)

---

## Source-Issue (SI) Rows

### SI-CTL-001

- **Status:** PASS
- **Command:** `bash .planning/phases/36-acceptance-checks-re-verification-handoff/probes/ac-si-ctl-001.sh`
- **Raw stdout evidence:** `.planning/phases/36-acceptance-checks-re-verification-handoff/evidence/SI-CTL-001.stdout.txt`
- **SHA-256:** `1ea041540984a19b9d28828a3eb3053d23e017179830484863a55ff99c6d3cbe`
- **Observed metric:** SI-CTL-001 block present with resolved-by text
- **Pass criterion:** Input-vector dimensionality inconsistency — resolved by v1.4 finding B-03 / Phase 17

### SI-PINN-002

- **Status:** PASS
- **Command:** `bash .planning/phases/36-acceptance-checks-re-verification-handoff/probes/ac-si-pinn-002.sh`
- **Raw stdout evidence:** `.planning/phases/36-acceptance-checks-re-verification-handoff/evidence/SI-PINN-002.stdout.txt`
- **SHA-256:** `34228f9eb014ef9d1b986900182af1be4d428d024cb94fa44ca4037fefcf1e18`
- **Observed metric:** SI-PINN-002 block present with author notes + batch-construction resolution
- **Pass criterion:** Author comments documented; batch-construction resolved under SI-PINN-003

### SI-PINN-003

- **Status:** PASS
- **Command:** `bash .planning/phases/36-acceptance-checks-re-verification-handoff/probes/ac-si-pinn-003.sh`
- **Raw stdout evidence:** `.planning/phases/36-acceptance-checks-re-verification-handoff/evidence/SI-PINN-003.stdout.txt`
- **SHA-256:** `c368a4544d3d4f9bcae173efc1e85f9db07179e59f01155d300fce48d334a17e`
- **Observed metric:** SI-PINN-003 resolution token + canonical spec pointer present
- **Pass criterion:** Batch-construction inconsistency RESOLVED by Phase 34; `ctl_instruction.md` canonical

### SI-DQA-003

- **Status:** PASS
- **Command:** `bash .planning/phases/36-acceptance-checks-re-verification-handoff/probes/ac-si-dqa-003.sh`
- **Raw stdout evidence:** `.planning/phases/36-acceptance-checks-re-verification-handoff/evidence/SI-DQA-003.stdout.txt`
- **SHA-256:** `ac9f66ff4c16d14a5a9c818fbc883cefc5fa245f978f1c40fe45ac9651ce5d98`
- **Observed metric:** Inline conservation/SCS gate citation + data-quality lineage present
- **Pass criterion:** Inline citation on conservation/SCS gate; data-quality lineage preserved

---

## Protected-Path Guard

### PROTECTED-PATH-GUARD

- **Status:** FAIL
- **Command:** `bash .planning/phases/36-acceptance-checks-re-verification-handoff/probes/ac-protected-path-guard.sh`
- **Raw stdout evidence:** `.planning/phases/36-acceptance-checks-re-verification-handoff/evidence/PROTECTED-PATH-GUARD.stdout.txt`
- **SHA-256:** `7279a63d4b6c1e3e01403d2d16dc225b1d5cce879ccb6215c569d906d267f34d`
- **Observed metric:** Check [1] failed (8 pinn/ references found in probes/)
- **Pass criterion:** No probes/ script references pinn/ code; git diff over pinn/ + frozen/read-only specs empty
- **Root cause:** Probe self-matching bug — `ac-evid-15-d-conflict.sh` has `$PINN` variable referencing `pinn_architecture.md`, which is not an import but a string variable for grep target
- **Route-back:** Phase 36 (fix guard regex to exclude false-positive matches)

---

## Manifest Snapshot

**Commit:** `68126c3` (probe suite commit)

**Manifest:** `36-ACCEPTANCE-MANIFEST.md` (26 rows: CURR 1-6, LOOP 1-8, LOSS 1-4, EVID-15 headlines 3, SI rows 4, PROTECTED-PATH-GUARD)

All probe results are tied to this manifest snapshot to ensure stale/mixed evidence is detectable.