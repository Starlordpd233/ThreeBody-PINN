# Evidence Packet: L_max / tau_L - L_max, tau_L, and Staging-Metadata Contract (CURR-02)

## Header

| Field | Value |
|---|---|
| ID | `L_max / tau_L` |
| Title | `L_max`, `tau_L`, raw-mass D, and Rosenstein-baseline revisable estimator (CURR-02) |
| Phase 33 Decisions Covered | `D-33-04` (`L_max` characteristic scale), `D-33-05` (raw-mass `D ~= 4.6416` preserved), `D-33-07` (Rosenstein revisable baseline) — see `33-CONTEXT.md` decisions section |
| Severity | MAJOR |
| Current Status | IN_PROGRESS |
| Current Verdict | accept-resolution |
| Phase | Phase 33 |
| Owner Phase | Phase 33 |
| Consumer Phase | Phase 36 |
| Acceptance Check ID | AC-CURR-02-LMAX |
| Spec Sections Touched | `ctl_instruction.md` Step 3 item 2 (`L_max` / `L_norm`); `ctl_instruction.md` Step 3 item 5 (`tau_L` Rosenstein estimator); `ctl_instruction.md` §2.5 Global scaling (raw-mass `D ~= 4.6416`); `ctl_instruction.md` Step 4 (`tau_L`/`L_norm` metadata exclusion from IC13) |
| Code Paths Touched | Not code-applicable |

## Source Positions

Neither source is authoritative.

| Source | Required Line-Range Citation | Standing | Position Summary |
|---|---|---|---|
| `pinn_instruction/issues/03-curriculum-and-training-loop.md` | `pinn_instruction/issues/03-curriculum-and-training-loop.md:229-305` (`tau_L` and `L_max` formula resolution, including the shadow-trajectory `compute_tau_L` pseudocode at 261-300); `pinn_instruction/issues/03-curriculum-and-training-loop.md:251` (`np.clip(L/(L_max+eps), 0, 1)`); `pinn_instruction/issues/03-curriculum-and-training-loop.md:265, 305` (`D = np.cbrt(G*M_tot_ref*T_scale**2) = 6.694` and P4-1 re-run directive); `pinn_instruction/issues/03-curriculum-and-training-loop.md:303` (PCA+Rosenstein shortcut "faster approximation"); `pinn_instruction/issues/03-curriculum-and-training-loop.md:262` (`epsilon_pert = 1e-8`, `epsilon_soft = 1e-10`) | Non-authoritative issue source | Proposes `L_max = M_total * r_char * v_char` with `v_char = sqrt(2|E|/M_total)` (matching the current spec formula), but re-frames it as a maximum; locks a shadow-trajectory `tau_L` estimator with `epsilon_pert=1e-8` / `epsilon_soft=1e-10` and an active `D = 6.694` mass-fraction scale (the P4-1 re-run directive); recommends an unspecified "PCA+Rosenstein" shortcut for batch processing; uses `np.clip(L/(L_max+eps), 0, 1)` as a storage/gate value. |
| `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md` | `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md:88-91` (§1.17 `L_max` and `tau_L` formulas — `modified` / `surface_to_user`); `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md:173-179` (claim rows `LMAX-01` accepted, `LMAX-02` modified (characteristic, not maximum), `TAUL-01` `surface_to_user`, `TAUL-02` rejected, `TAUL-03` defer, `TAUL-04` accepted, `TAUL-05` rejected); `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md:207-209` (DGR-18 L_max interpretation, DGR-19 tau_L estimator, DGR-20 tau_L units) | candidate verdict source, not authority | §1.17 retains `L_max = M_tot * r_char * sqrt(2|E|/M_tot)` as the current **characteristic angular-momentum scale**, not as a proven global maximum (LMAX-02). The canonical `tau_L` estimator remains unresolved; the owner must select the method and time-unit convention before locking `tau_L` stage thresholds (TAUL-01 `surface_to_user`, TAUL-03 defer). The current Rosenstein-style trajectory estimator is retained as the revisable baseline. The issue shadow code is NOT normatively adopted because its force denominator is not matched-Plummer; the unspecified "PCA+Rosenstein" shortcut is NOT adopted (TAUL-02, TAUL-05 rejected). `epsilon_pert = 1e-8` and `epsilon_soft = 1e-10` are shadow-method parameters only, distinct from training softening `epsilon_train = 1e-5`. |
| `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md` | `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md:62` (§1.17 line range 88-91); `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md:97` (finding -> §1.17 mapping) | Navigation / line-map aid | §1.17 anchored to lines 88-91 in committed `49fb7958`; section anchor stable across re-pagination. |

## Current Spec Evidence

- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1071-1085` defines the current `L_max` formula: `L_max = M_tot * r_char * v_char` with `r_char = (1/3) * sum pairwise ||r'_i - r'_j||` and `v_char = sqrt(2|E|/M_tot)`; the surrounding prose calls `L_max` the "characteristic circular-orbit scale at energy `E`" (line 1084) — this is the characteristic-scale language Phase 33 will preserve. The arithmetic in the issue-doc `L_max` formula (lines 239-251) matches this current spec; the disagreement is the *interpretation* (maximum vs characteristic scale).
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1087-1097` gives the `compute_L_norm(m, r_prime, v_prime, E, eps=1e-10)` pseudocode that returns `L / (L_max + eps)` with no clamp; the `eps=1e-10` here is the offline-invariant degeneracy guard, NOT a training-side softening.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1155-1192` defines the current `tau_L` Rosenstein-style estimator (uniform cadence -> delay-embedding -> nearest neighbors -> divergence curve -> linear regression -> `tau_L = 1/lambda_max`). This is the revisable baseline Phase 33 will retain.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:897-913` defines global scaling with raw-mass `D = (G*T**2)^(1/3) ~= 4.6416` (G=1, T=10). The issue-doc `D = 6.694` mass-fraction scale is rejected by current spec §2.5 (lines 915-929) and by the Phase 32 `D = 6.694` packet.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1419` confirms `tau_L`, `L_norm`, and other invariant-heavy descriptors are metadata only, not network IC slots under the Phase 17 input contract.

No framework spec is edited by this packet (Plan 33-01 only authors evidence; Plan 33-02 will transcribe).

## Locked Convention / Dataset Evidence

- `.planning/REQUIREMENTS.md` `CURR-02` is the requirement for this packet. The roadmap / `CURR-02` shadow-trajectory + PCA+Rosenstein shortcut + `eps_pert`/`eps_soft` phrasing is **superseded** by `GAP-33-02`.
- `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence/d-6-694-conflict.md:60-67,93-99` locks `D ~= 4.6416` as the active raw-mass scale and rejects `D = 6.694` as a pipeline instruction; Phase 33 consumes that verdict directly.
- `.planning/REQUIREMENTS.md` SCOPE-12 makes the v1.5-locked raw-mass `D ~= 4.6416` convention a hard constraint for `tau_L` / `L_max` transcription.
- `GAP-33-02` (`33-GAPS.md:63-134`, `RESOLVED-WITH-INSTRUCTION` 2026-06-22) is the owner-routed resolution that carries the grounded disposition for this packet: keep Rosenstein-baseline / defer final estimator.

## FUT Hand-off Note

- FUT path / note: The final `tau_L` estimator (Rosenstein vs shadow/Benettin vs other), time-unit convention, fit windows, perturbation size, uncertainty handling, and final stage thresholds are owner-pending FUT/trainex decisions. Any shadow-trajectory implementation referenced in `pinn/data-processing-pipeline-full.py` is NOT grounding; it is FUT-01/FUT-04 hand-off context only.
- Not FUT-applicable: This packet does not derive its verdict from any live code reference.

## First-Principles or Engineering Check

`L_max = M_tot * r_char * v_char = M_tot * r_char * sqrt(2|E|/M_tot)` is a dimensional angular-momentum scale: `[M] * [L] * [L/T] = [M L^2 / T]`, which is the dimension of angular momentum. For a circular orbit at binding energy `E`, this is the angular momentum that orbit would carry at the characteristic radius `r_char`. It is not a proven global maximum over the full three-body state space (which includes high-eccentricity or hierarchical configurations where `L` can transiently exceed this scale); it is a characteristic normalization, which is why `L_norm = L / L_max` can legitimately overshoot 1 (the M6 packet handles that case).

For `tau_L`, Rosenstein-style finite-time divergence estimation and shadow/Benettin integration estimate related but operationally different quantities. Rosenstein estimates `lambda_max` from nearest-neighbor divergence in a delay-embedded reconstruction of a single observed trajectory; shadow/Benettin integration propagates an explicit perturbed orbit alongside the reference and measures their exponential separation. Time-axis normalization (raw `t` vs scaled `u = t/T`), fitting window, perturbation magnitude, potential softening, and uncertainty handling all change the numeric `lambda_max` and therefore `tau_L = 1/lambda_max`. Because Phase 33 stage thresholds use `tau_L` (e.g. Stage 4a `tau_L > 5`, Stage 4b `2 < tau_L <= 5`), locking a method also locks the scale of Stage 4/5/chaotic gates. Without an explicit owner selection of method + time-unit + fit-window + uncertainty + threshold calibration, no final threshold can be transcribed as locked.

The issue-doc shadow `compute_tau_L` uses a non-matched-Plummer force denominator (`||dr||^3 + epsilon_soft`), which is inconsistent with the v1.5-locked matched-Plummer training softening (PHYS-03). This is why the resolution doc rejects the issue shadow code as normative and why `epsilon_pert` / `epsilon_soft` are shadow-method parameters only, distinct from training `epsilon_train = 1e-5`.

## Verdict

Verdict: accept-resolution

Explicit user instruction: `GAP-33-02` (`33-GAPS.md:117-134`, `RESOLVED-WITH-INSTRUCTION` 2026-06-22, owner AskUserQuestion ratification of keep-Rosenstein-baseline / defer-estimator).

Reasoning:

- The resolution doc §1.17 retains `L_max = M_tot * r_char * sqrt(2|E|/M_tot)` as the characteristic angular-momentum scale (not a proven maximum), retains the Rosenstein-style estimator as the revisable baseline, and rejects the issue shadow code and the unspecified PCA+Rosenstein shortcut. This is the grounded position.
- The owner-routed `GAP-33-02` resolution carries the estimator / time-unit / threshold deferral forward: method, time-unit convention, fit parameters, uncertainty handling, and final stage thresholds are owner-pending.
- The Phase 32 `D = 6.694` packet locks `D ~= 4.6416` as the active raw-mass scale and rejects `D = 6.694`; Phase 33 consumes that verdict directly.
- The roadmap / `CURR-02` shadow-trajectory + `eps_pert = 1e-8` / `eps_soft = 1e-10` + fast PCA+Rosenstein phrasing is explicitly NOT normatively adopted and must not be transcribed as locked.

## Root-Cause Ambiguity

The root ambiguity has three layers: (1) the issue doc frames `L_max` as a maximum while the current spec and resolution doc frame it as a characteristic scale; (2) the issue doc locks a shadow-trajectory estimator while the current spec uses Rosenstein; (3) the issue doc's `D = 6.694` mass-fraction scale conflicts with the v1.5-locked raw-mass `D ~= 4.6416`. Phase 33 resolves all three by transcribing the characteristic-scale `L_max` formula, retaining Rosenstein as the revisable baseline, and consuming the Phase 32 `D ~= 4.6416` lock.

## Locked Convention or Owner Route

**Locked by this packet (transcribed in Plan 33-02; decisions D-33-04, D-33-05, D-33-07):**

- Per D-33-04: `L_max = M_tot * r_char * sqrt(2 * |E| / M_tot)` as the **characteristic** angular-momentum scale (LMAX-01 accepted; LMAX-02 characteristic-scale, not a proven global maximum).
- Per D-33-05: raw-mass `D ~= 4.6416` as the active global scale; `D = 6.694` rejected as a mass-fraction pipeline instruction (Phase 32 `D = 6.694` packet; SCOPE-12).
- Per D-33-07: the Rosenstein-style trajectory estimator retained as the **revisable baseline**.

**Owner route (deferred, GAP-33-02):** The final `tau_L` estimator (Rosenstein vs shadow/Benettin vs other), time-unit convention, fit window, perturbation size, uncertainty handling, and final stage thresholds are owner-pending before any threshold lock. The issue-doc shadow-trajectory method, its `epsilon_pert = 1e-8` / `epsilon_soft = 1e-10` parameters (shadow-method parameters only, distinct from training `epsilon_train = 1e-5`), and the unspecified PCA+Rosenstein shortcut are NOT normatively adopted (TAUL-02, TAUL-05 rejected).

## Which Source Was Correct / Wrong

- Resolution doc (§1.17): correct on the characteristic-scale `L_max` interpretation, correct to retain Rosenstein as the revisable baseline, correct to reject the issue shadow code as normative, and correct to reject the unspecified PCA+Rosenstein shortcut, after independent grounding.
- Issue doc: partly correct on the `L_max` formula (matches current spec); wrong to frame `L_max` as a proven maximum; wrong to lock the shadow-trajectory method with a non-matched-Plummer denominator; wrong to lock `D = 6.694` (rejected by Phase 32); wrong to recommend an unspecified PCA+Rosenstein shortcut.
- Current spec / Phase 32 `D = 6.694` packet / SCOPE-12: correct and governing.
- The roadmap / `CURR-02` shadow + PCA/Rosenstein phrasing is superseded by `GAP-33-02` and must not be transcribed as locked.

## Before / After or Intentional Non-Change Note

**Before:** `ctl_instruction.md` Step 3 item 2 defines `L_max = M_tot * r_char * v_char` with the surrounding prose calling it the "characteristic circular-orbit scale at energy E" (line 1084). Step 3 item 5 (lines 1155-1192) defines the Rosenstein-style `tau_L` estimator. §2.5 (lines 897-929) locks `D ~= 4.6416`.

**After (Plan 33-02, not Plan 33-01):** `ctl_instruction.md` will explicitly state "characteristic angular-momentum scale, not a proven global maximum"; retain Rosenstein as the revisable baseline; record that the `tau_L` estimator, time-unit convention, fit parameters, uncertainty handling, and final stage thresholds are owner-pending; explicitly NOT adopt the issue shadow method, its `epsilon_pert`/`epsilon_soft` parameters, or the unspecified PCA+Rosenstein shortcut; keep `D ~= 4.6416` active and reject `D = 6.694` only as provenance.

Plan 33-01 makes no spec edit. This packet routes the evidence and AC-CURR-02-LMAX identity.

## Named Acceptance Check

AC-CURR-02-LMAX

Planned pass criterion (Plan 33-04 / Phase 36): `ctl_instruction.md` Step 3 item 2 / item 5 / §2.5 text states (a) `L_max = M_tot * r_char * sqrt(2|E|/M_tot)` as the characteristic scale, not a proven global maximum; (b) raw-mass `D ~= 4.6416` active and `D = 6.694` rejected; (c) Rosenstein-style revisable baseline retained; (d) `tau_L` estimator / time-unit / fit window / uncertainty / final thresholds owner-pending; (e) no shadow-trajectory method, no `epsilon_pert`/`epsilon_soft` shadow parameters, and no PCA+Rosenstein shortcut adopted as normative.

Owning phase: Phase 33 (Plan 33-02 transcribes; Plan 33-04 verifies).

## STOP / Gap Handling

No STOP gap opened — disposition grounded in `GAP-33-02` `RESOLVED-WITH-INSTRUCTION` 2026-06-22 (owner-routed keep-Rosenstein-baseline / defer-estimator; AskUserQuestion ratification), matching resolution doc §1.17 (TAUL-01 `surface_to_user`, TAUL-03 defer, TAUL-02 / TAUL-05 rejected, LMAX-01 accepted, LMAX-02 modified). The characteristic-scale `L_max` formula, the raw-mass `D ~= 4.6416`, and the Rosenstein baseline are all grounded; the `tau_L` estimator / units / threshold selection is the explicitly owner-pending remainder and is not a source-silent semantic gap.

## Status Transition Log

```text
2026-06-23 0113f86 PENDING -> IN_PROGRESS (Phase 33 P01 Task 2 by claude-code-gsd-executor-33-01; packet authored, ledger link applied in Task 3)
```
