# Phase 60 Single-System Learnability Run Protocol

**Audience:** the project owner, a non-specialist.
**This document is:** the plain-language twin of evidence/run-protocol.json.
**This document is not:** a result. No arm has launched.

## In plain language

Before any real experiment launches, this protocol pre-registers and seals the exact rules, hyper-parameters, budgets, and fingerprints that govern Phase 60. Every experiment must cite this protocol's SHA-256 fingerprint:

`93486d240f129bb5947cddb56d2eb18936ac0cbad7ac0bceeb0af0372b850383`

If any code, threshold, or input data changes after this seal, the harness refuses to start.

### What the experiments do

Phase 60 measures whether a Physics-Informed Neural Network (PINN) can learn chaotic 3-body trajectories when given single systems rather than a broad population:

1. **Rung 1 (Data-only ceiling):** Three representative systems from the Stage-0 training panel (1632, 851, 4658) train on supervised position data alone (gold trajectories). This establishes whether the architecture has enough capacity to fit the motion when shown the answer directly.
2. **Gate G2 (Learnability gate):** If at least 2 of the 3 Rung-1 systems fail to reach Tier 1 accuracy (`E <= 0.1`), Gate G2 fires. This means standard capacity at the default frequency (`first_omega_0 = 30`) is insufficient. A frequency sweep on the easiest failing system tests `first_omega_0 in [60, 120, 240, 480]`. If any setting reaches Tier 1, it is confirmed on the second failing system. If confirmation fails or no setting reaches Tier 1, the phase stops for the owner or routes to `RETHINK-REPRESENTATION`.
3. **Rung 2 (Physics ladder):**
   - **Rung 2a:** Physics loss with initial-condition (IC) supervision, training on base trajectories with physics residuals enforcing Newton's laws.
   - **Rung 2b:** Full physics loss without IC supervision.
4. **Probes:** Diagnostic runs on standard-variant systems (2279 at Stage 4b, 3418 at Stage 6) testing harder dynamical regimes.

### Execution rules

- **Hardware & Precision:** Every real arm runs on this Mac's GPU via Apple Silicon Metal Performance Shaders (MPS) in `float32`. Seed 42 is fixed across all arms. A parallel double-precision CPU `float64` cross-check re-scores both saved states; any disagreement in tier or formula counts triggers an immediate owner stop.
- **Budget & Polish:** Each arm receives an Adam step budget scaled from an isolated pre-arm timing run to equal 3.0 wall-clock hours (at least 50 timing steps for physics arms, 500 for data-only). A "still-improving" test allows at most one budget doubling (factor 2.0). Following Adam, every arm undergoes a full-batch L-BFGS polish capped at 5 outer iterations without progress or 25% of Adam wall time (at most ~45 minutes).
- **First Result Invariant:** The first completed run is the permanent record. No silent restarts, retries, or extra seeds are permitted.
- **Owner Checkpoints:** The owner is stopped and consulted if:
  - Gate G2 is rescued to Tier 1 (Owner Checkpoint ④ to approve the setting);
  - A G2 confirmation fails below Tier 1 (unsettled by pre-answer, so the owner decides at the time);
  - A budget extension ends with an undeterminable rate;
  - The CPU cross-check disagrees with the MPS score;
  - An assigned data file is blocked or unreadable.

---

## What you decided before the protocol was sealed

Prior to sealing this protocol, the owner made two binding decisions at Task 3:

### 1. GAP-60-03: Gradient clipping in data-only arms

- **Decision:** Kept (the delegated default).
- **Owner's exact response:**
  > "Keep clipping in data-only arms (delegated default: Adam limits unusually large gradient steps using GradClipper at Stage 0 multiplier 8.5)"
- **Effect:** Every Adam step in every data-only arm uses the trainer's median-based `GradClipper` at Stage 0 multiplier 8.5 (median floor `1e-6`). This ensures data-only and physics arms use identical optimizer stabilization safeguards, preventing a data-only failure from being an artifact of different clipping rules.

### 2. GAP-60-09: Failed G2 confirmation interpretation

- **Decision:** No pre-answer (ask if it happens).
- **Owner's exact response:**
  > "No pre-answer: ask me if it happens (stop the phase and prompt for decision if a failed confirmation occurs)"
- **Effect:** If Gate G2 fires, a frequency setting reaches Tier 1 on the sweep system, but falls below Tier 1 during the single confirmation run on the second failing system, the harness will not assume "no rescue" nor "rescue". Instead, it writes the sweep curve and confirmation records, halts with an owner-routed stop, and presents the actual results to the owner for an explicit decision.

These answers are sealed into `evidence/run-protocol.json` (`clip.clip_data_only_arms: true`, `g2.failed_confirmation_pre_answer: null`) and will not be altered by any subsequent plan.

---

## Pinned values

| Domain | Parameter / Rule | Pinned Value | Source Citation |
|---|---|---|---|
| **RNG Seed** | Random seed | `42` | SPEC Requirement 4 |
| **Runtime** | Primary device & dtype | `mps` / `float32` | SPEC Requirement 4 |
| **Cross-check** | Secondary device & dtype | `cpu` / `float64` on both Adam & polish states | GAP-60-07, SPEC Requirement 3 |
| **Schedule** | Base LR & decay | `lr_base = 0.001`, `lr_decay = 0.7` | D-01 |
| **Schedule** | Data-only schedule | Stage-0 cosine annealing (`k = 0`) over budget `B` | D-04 |
| **Schedule** | Warmup steps | `min(2000, floor(0.1 * B))` | D-03 |
| **Schedule** | Probe Rung-2b LR | Stage-specific rate (`k = 4` for 2279, `k = 6` for 3418) | D-05 |
| **Budget** | Single-system cap | 3.0 wall-clock hours (`floor(3.0 h / (wall / steps))`) | D-02 |
| **Budget** | Extension factor | `2.0` (at most 1 extension if still improving) | Frozen scorecard §fairness |
| **Clipping** | Gradient clipper table | Stage 0: `8.5`, Stage 4: `3.0`, Stage 6: `3.0`, floor `1e-6` | GAP-60-03 |
| **Timing Run** | Pre-arm steps | 500 steps (data-only), 50 steps (physics); all timed | GAP-60-04 |
| **Cadence** | Scoring frequency | Step 0, every `floor(0.05 * B)` steps, and final budget step | D-06 |
| **Cadence** | Monitor logging | Causal weights & front logged at readings; never halts | D-06 |
| **Polish** | L-BFGS settings | Full-batch, history 10, strong Wolfe, max 50 iters/call | GAP-60-05 |
| **Polish** | Termination | 5 outer calls without improvement or 25% Adam wall time | GAP-60-05 |
| **Polish** | Physics freeze | Collocation rows, causal weights, loss weights frozen | 57-RULING.md:112-124 |
| **Divergence** | Non-finite loss/grad | End Adam at last good state, score & polish; no restart | GAP-60-06 |
| **Weights** | File format & storage | `adam.weights` & `polish.weights` in plain git | D-10, GAP-60-08 |
| **G2 Sweep** | Swept parameter & grid | `first_omega_0 in [60.0, 120.0, 240.0, 480.0]` | FEAS-03, D-08 |
| **G2 Trigger** | Firing threshold | At least 2 of 3 Rung-1 arms below Tier 1 | FEAS-03, SPEC Requirement 6 |
| **Skip Reasons** | Allowed skip strings | `"no rescue"` or `"checkpoint ④ answered go to the verdict"` | 60-SPEC skip reasons |
| **R_ref** | Reference scale | Stage-0 reference in force (`r_ref_stage0.json` or re-measured) | D-07, D-08, GAP-60-10 |
| **Approval** | Approved setting rule | Any finite positive frequency approved by owner at Checkpoint ④ | D-11, GAP-60-11 |
| **Energy Scale** | Probe S_H & eps_H | Persisted gen-7 values (`22.3217...`, `0.002232...`) | GAP-60-12 |
| **Normalizer** | IC13 statistics | Recovered gen-7 statistics digest (`77526e53...79f6`) | GAP-60-13 |

### Registered Owner Stops

The harness raises an `OwnerRouted` exception and pauses execution for owner intervention upon:
1. `missing_formula_on_counted_system`: Counted panel system lacks two-Kepler formula (SPEC Requirement 7).
2. `rescue`: Confirmed G2 sweep setting reaches Tier 1 (Owner Checkpoint ④, SPEC Requirement 6).
3. `undeterminable_improvement_rate`: Extended arm improvement rate cannot be evaluated (SPEC Requirement 8).
4. `cross_check_disagreement`: CPU float64 cross-check disagrees with MPS score in tier or counts boolean (GAP-60-07).
5. `failed_confirmation_without_pre_answer`: G2 confirmation falls below Tier 1 and protocol has no pre-answer (GAP-60-09).
6. `arm_cannot_resume_or_non_governed_exit`: Checkpoint cannot be restored or arm exits abnormally (SPEC Requirement 8).
7. `blocked_record`: Assigned dataset record is missing, empty, unreadable, or refused (SPEC Requirement 8).
8. `gate04_block_on_continue`: GATE-04 re-measure at approved frequency fails (D-07).
9. `protocol_drift_after_real_record`: Pinned file differs from protocol after real record exists (SCOPE-42).

---

## Fingerprints

- **Run Protocol JSON SHA-256:** `93486d240f129bb5947cddb56d2eb18936ac0cbad7ac0bceeb0af0372b850383`
- **Feasibility Scorecard SHA-256:** `f4b17688c05de68b7aa0f62e452baad751989b0ce2ce36828359a53f9e09444b`
- **Feasibility Scorer Successor SHA-256:** `00edf81d59396fe189d476dd3e69473c4291b71bc6af6171da758f68b61f2bc7`
- **Preflight Records SHA-256:** `7f4fffe8702da3da8307582310221ccc0d4b1abab1156dd48b2c6103c89892cd`
- **Scope Amendment Commit:** `dc3edac0e9ae737b42be276dd9b67e12b8ab8926`
