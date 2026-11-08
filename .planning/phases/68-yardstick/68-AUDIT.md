# Phase 68: Yardstick Known-Answer Audit Report

**Audience:** The project owner and scientific reviewers.  
**Purpose:** Comprehensive known-answer audit of Brutus's recorded ground truth and the constant baseline predictor across Stage-0 training panel systems (1632, 851, 4658), auditing explicit-velocity FEAS-01 metrics against finite-difference energy at native gold ($dt=0.01$) and coarse base ($dt=0.08$) cadences, plus same-sample float32 input precision sensitivity.  
**Evidence Artifact:** `.planning/phases/68-yardstick/evidence/yardstick-audit.json`  
**Evidence SHA-256:** `4b82c21918ba578c9f889cc21f1a93494d12aaa60940b2dac5ef073318922fe4`  
**Replay Command:** `<home>/miniforge3/envs/pinn-train/bin/python -B -m pinn.verification.yardstick_audit --check .planning/phases/68-yardstick/evidence/yardstick-audit.json` -> `YARDSTICK-AUDIT-OK`  

---

## 1. Executive Summary

This audit establishes the empirical ground-truth baseline ("the yardstick") by evaluating numerical integrator outputs (Brutus) and constant baseline predictors on the Stage-0 training panel against both the frozen FEAS-01 feasibility scorecard and the production validation gate.

### Key Findings

1. **The Brutus Known-Answer Floor Confirms GAP-59-08:**
   - Under the frozen **FEAS-01 scorecard** (using Brutus's recorded explicit velocities $\mathbf{v}_{\text{recorded}}$), Brutus achieves **Tier 3** on all systems ($E = 0.0$ exact, $\text{eps}_H \le 2.17 \times 10^{-11}$ on gold and $\le 1.88 \times 10^{-14}$ on base).
   - Under the **production validation gate** (which computes velocity via centered finite differences on positions, $\mathbf{v}_{\text{FD}}$), the exact same Brutus trajectory **FAILS** the $\text{eps}_H \le 10^{-5}$ ($\text{SCS} \le -5.0$) gate across all systems:
     - On the native **gold grid** ($dt = 0.01$): $\text{eps}_H \approx 0.00109$ (1632), $0.00344$ (851), $0.02380$ (4658); panel aggregate $\text{eps}_H = 0.023797$ ($\text{SCS} = -1.623$), **FAIL**.
     - On the coarse **base grid** ($dt = 0.08$): $\text{eps}_H \approx 0.0471$ (1632), $0.2046$ (851), $0.3790$ (4658); panel aggregate $\text{eps}_H = 0.378998$ ($\text{SCS} = -0.421$), **FAIL**.
   - **Conclusion:** Brutus itself cannot pass the production validation gate at $dt = 0.01$ or $dt = 0.08$. Centered finite-difference truncation error $O(\Delta t^2)$ creates an empirical error floor that is $2$ to $3$ orders of magnitude above the $10^{-5}$ gate threshold even at native gold cadence.

2. **The Constant Predictor Paradox:**
   - The trivial window-mean constant predictor predicts fixed static positions with zero velocity.
   - It fails position accuracy completely ($E \approx 1.14 - 1.24 > 0.1$, Tier 0, valid horizons $h(0.01) = h(0.1) = 0.0$).
   - However, because its velocity is identically zero, its kinetic energy is zero and its potential energy is constant. Thus $\Delta H \equiv 0.0$, $\text{eps}_H = 0.0$, $\text{SCS} = -\infty$, and the constant predictor achieves a **`PASS`** on the production validation gate!
   - This proves that energy conservation alone without position accuracy is insufficient to judge model quality.

3. **Input Precision Rounding Sensitivity:**
   - Rounding positions, times, and masses to float32 before computing the finite-difference gate produces negligible shift in $\text{eps}_H$: on gold Brutus, $\text{eps}_H$ shifts from $0.023797$ to $0.023795$ (a relative change of $< 0.012\%$).
   - Input precision is not the root cause of the gate failure; discretization truncation error of finite differences is the sole dominant factor.

4. **Grid Boundaries & Sample Count Verification:**
   - Gold grid: 1001 snapshots retained in $[0.0, 10.0]$ ($t_{\text{last}} = 9.999999999999831 \le 10.0$), matching Phase 59 census exactly.
   - Base grid: 125 snapshots retained in $[0.0, 10.0]$ ($t \in [0.0, 9.92]$). The 126th snapshot at $t = 10.000000000000007$ is excluded by strict `physical_window` comparison ($t \le 10.0$), whereas Phase 59 census included it via $t \le 10.0 + 10^{-9}$. This boundary difference is preserved as keyed evidence.
   - Cadences match expected $0.01$ and $0.08$ to within float epsilon ($< 10^{-14}$ relative error, 0 warnings).

5. **Access and Process Attestation:**
   - Exactly 6 files opened (3 base, 3 gold in Stage 0 TRAIN split).
   - 0 validation or test records opened. 0 blocked attempts. 0 refusals.
   - The CLI executes read-only analysis without invoking model training, optimizers, evaluators, or test receipts.

---

## 2. Provenance and Integrity

| Property | Value |
|---|---|
| Schema Version | `phase68-yardstick-audit/v1` |
| Capture Commit (`git_head`) | `3d60908a7b94e66909651cb21c4fbe0d1cec3404` |
| Scorecard SHA-256 | `f4b17688c05de68b7aa0f62e452baad751989b0ce2ce36828359a53f9e09444b` |
| Scorecard Freeze Commit | `4ea3b1bc95e2dc3794fec4fb2047b9d32b5e889f` |
| Split Manifest SHA-256 | `5846ae5b55104e55a85d644875c3da187200c3d521f52a9298876d656c6d8903` |
| Panels JSON SHA-256 | `56ad5185148fca7e72b21f4fc1dbaaaf8eea7aa9ecdf498653af98ad88d6aa92` |
| Python Environment | Python 3.11.15, NumPy 2.4.6, PyTorch 2.12.1 |
| Execution Time | ~0.59 seconds wall time |
| Coverage Complete | `True` (12 rows, 8 aggregates, 6 opens, 0 problems) |

### Producer Module Hashes

```
pinn/verification/yardstick_audit.py     : 01f5dff320f7725dc8254c5c7d0d1952a26c8ec0cf25e0a6d09fe91a5da79ee4
pinn/verification/evidence_io.py        : f5ec843f54d6fc22a94fb21ba99cc6d7083063ca52ae82b615cc52f68bc7fcf0
pinn/verification/feasibility_scorecard.py: 1dbba65538e146746cfdf9a8b1a8d184ebc992796e67cf77be329cbf9bfb6736
pinn/verification/feasibility_scorer.py  : e2aa251508db8c5d15c7e3f8fe439ae577319e64e569e2c6080b0b8df04e389e
pinn/verification/gate_metrics.py       : fa40ea674a2432c69ea4a362534a7493d8b598b9daea254ff01ea76395ec6db8
pinn/training/validation_gate.py        : ba5470559eb4da53ec2d5e9b0b467ec67a3f443831cbb281ebcf719caae9e29a
pinn/verification/split_allowlist.py    : 16d56d113ae8b9658ecda834c382ce6a87796d11d1ec9cba150df265bcff1dc8
pinn/verification/diagnostic_data.py    : bb42637956d784a0d91d9047d848698bf0bf699298516ee76d33010b9f074d28
pinn/verification/production_reference.py: b2785669b352e0a2948c084f3abde39e94628ee3e0856aa76d4948a74ecff5f8
pinn/verification/stage0_census.py      : f173dd70ae0a30aa01cb4dce61a68cebc9d75fbf806161c9ec8d0e515d42ec0a
```

---

## 3. Direct Caller Map

The audit is strictly bounded, read-only, and reuses verified production components:

```
yardstick_audit.py::run_fixed_panel_audit
  │
  ├── require_frozen_scorecard() -> checks scorecard freeze commit in git history
  ├── SplitAllowlist.from_manifest() -> verifies generation7_splits.json SHA-256
  ├── panels.json check -> verifies singles tuple (1632, 851, 4658)
  │
  ├── For each system (1632, 851, 4658):
  │     ├── require_stage0_training(allowlist, base_key)
  │     ├── require_stage0_training(allowlist, gold_key)
  │     │
  │     └── audit_pair(reader, base_key, gold_key):
  │           ├── load_reference(reader, base_key) [production COM boost, scaling, canon perm]
  │           ├── load_reference(reader, gold_key)
  │           ├── check physical identity (D, T, ordered masses, inner_pair, perm)
  │           ├── physical_window(times, t_max=10.0) -> slices exact window [0, 10]
  │           ├── gold_base_agreement(sliced_base, sliced_gold) <= 1e-6
  │           │
  │           ├── For grid in (base, gold):
  │           │     ├── For pred in ("brutus", "window_mean_constant"):
  │           │     │     ├── score_trajectory(pred_pos, pred_vel, ref_pos, masses, ...) [FEAS-01]
  │           │     │     ├── compute_fd_metrics(pred_pos, times, masses) [Gate FD Native float64]
  │           │     │     └── compute_fd_metrics_float32_input(...) [Gate FD float32 input]
  │
  └── aggregate_gate_verdict(per_sys_eps) for 8 aggregates
```

**Caller Isolation Verification:**
- Both the FEAS-01 scorer and the FD gate share `matched_plummer_hamiltonian_series` and `trajectory_eps_h` in `gate_metrics.py`.
- No model network (`SQRSkipResNetSIREN`), optimizer (`Adam`, `L-BFGS`), trainer (`train.py`), or production evaluator (`evaluate.py`) is imported or executed.
- No test-split or validation-split file is accessed.

---

## 4. Full Known-Answer Tables (12 Prediction / Grid Groups)

### 4.1 FEAS-01 Feasibility Metrics

*Note:* Primary tier is determined by the **gold** grid. Base grid scores are provided for comparison only.

| System | Grid | Prediction | Tier | $E$ | $e_{\text{sys\_max}}$ | $e_{\text{in\_max}}$ | $h(0.01)$ | $h(0.1)$ | Explicit $\text{eps}_H$ | Vel Source |
|---|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1632 | base | brutus | 3 | 0.0000 | 0.0000 | 0.0000 | 1.0000 | 1.0000 | $1.1441 \times 10^{-14}$ | brutus |
| 1632 | base | constant | 0 | 1.1516 | 1.1064 | 1.1516 | 0.0000 | 0.0000 | 0.0000 | analytic |
| **1632** | **gold** | **brutus** | **3** | **0.0000** | **0.0000** | **0.0000** | **1.0000** | **1.0000** | $\mathbf{3.4353 \times 10^{-12}}$ | **brutus** |
| 1632 | gold | constant | 0 | 1.1538 | 1.1079 | 1.1538 | 0.0000 | 0.0000 | 0.0000 | analytic |
| 851 | base | brutus | 3 | 0.0000 | 0.0000 | 0.0000 | 1.0000 | 1.0000 | $1.8769 \times 10^{-14}$ | brutus |
| 851 | base | constant | 0 | 1.2381 | 1.0585 | 1.2381 | 0.0000 | 0.0000 | 0.0000 | analytic |
| **851** | **gold** | **brutus** | **3** | **0.0000** | **0.0000** | **0.0000** | **1.0000** | **1.0000** | $\mathbf{2.1701 \times 10^{-11}}$ | **brutus** |
| 851 | gold | constant | 0 | 1.2337 | 1.0606 | 1.2337 | 0.0000 | 0.0000 | 0.0000 | analytic |
| 4658 | base | brutus | 3 | 0.0000 | 0.0000 | 0.0000 | 1.0000 | 1.0000 | $1.6216 \times 10^{-14}$ | brutus |
| 4658 | base | constant | 0 | 1.1460 | 1.0076 | 1.1460 | 0.0000 | 0.0000 | 0.0000 | analytic |
| **4658** | **gold** | **brutus** | **3** | **0.0000** | **0.0000** | **0.0000** | **1.0000** | **1.0000** | $\mathbf{9.1504 \times 10^{-12}}$ | **brutus** |
| 4658 | gold | constant | 0 | 1.1396 | 1.0075 | 1.1396 | 0.0000 | 0.0000 | 0.0000 | analytic |

### 4.2 Production Finite-Difference Gate Metrics & Diagnostic Quantities

*Gate Pass Line:* $\text{eps}_H \le 1.0 \times 10^{-5}$ ($\text{SCS} \le -5.0$).

| System | Grid | Prediction | Native FD $\text{eps}_H$ | Native FD SCS | Verdict | Float32 FD $\text{eps}_H$ | Float32 FD SCS | F32 Verdict | $H(0)$ | $\Delta H_{\text{abs\_max}}$ | Peak Loc |
|---|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1632 | base | brutus | 0.047079 | -1.3272 | **FAIL** | 0.047079 | -1.3272 | **FAIL** | -5.0641 | 0.2384 | interior |
| 1632 | base | constant | 0.000000 | -Infinity | **PASS** | 0.000000 | -Infinity | **PASS** | -54.7824 | 0.0000 | endpoint |
| **1632** | **gold** | **brutus** | **0.001090** | **-2.9628** | **FAIL** | **0.001135** | **-2.9450** | **FAIL** | -4.9761 | 0.0054 | interior |
| 1632 | gold | constant | 0.000000 | -Infinity | **PASS** | 0.000000 | -Infinity | **PASS** | -54.7835 | 0.0000 | endpoint |
| 851 | base | brutus | 0.204586 | -0.6891 | **FAIL** | 0.204585 | -0.6891 | **FAIL** | -5.7635 | 1.1791 | interior |
| 851 | base | constant | 0.000000 | -Infinity | **PASS** | 0.000000 | -Infinity | **PASS** | -77.2224 | 0.0000 | endpoint |
| **851** | **gold** | **brutus** | **0.003442** | **-2.4632** | **FAIL** | **0.003449** | **-2.4623** | **FAIL** | -5.5157 | 0.0190 | interior |
| 851 | gold | constant | 0.000000 | -Infinity | **PASS** | 0.000000 | -Infinity | **PASS** | -78.7962 | 0.0000 | endpoint |
| 4658 | base | brutus | 0.378998 | -0.4214 | **FAIL** | 0.379000 | -0.4214 | **FAIL** | -12.9078 | 4.8920 | interior |
| 4658 | base | constant | 0.000000 | -Infinity | **PASS** | 0.000000 | -Infinity | **PASS** | -291.1613 | 0.0000 | endpoint |
| **4658** | **gold** | **brutus** | **0.023797** | **-1.6235** | **FAIL** | **0.023795** | **-1.6235** | **FAIL** | -11.7580 | 0.2798 | interior |
| 4658 | gold | constant | 0.000000 | -Infinity | **PASS** | 0.000000 | -Infinity | **PASS** | -294.3364 | 0.0000 | endpoint |

---

## 5. Panel Aggregate Table (8 Aggregates)

Panel verdict aggregates across the 3 systems by taking $\text{eps}_H = \max(\text{eps}_{H, 1632}, \text{eps}_{H, 851}, \text{eps}_{H, 4658})$.

| Grid | Prediction | Precision | Panel $\text{eps}_H$ | Panel SCS | Panel Verdict | Per-System $\text{eps}_H$ `[1632, 851, 4658]` |
|---|---|---|:---:|:---:|:---:|:---|
| base | brutus | native_float64 | 0.378998 | -0.4214 | **FAIL** | `[0.047079, 0.204586, 0.378998]` |
| base | brutus | float32_input | 0.379000 | -0.4214 | **FAIL** | `[0.047079, 0.204585, 0.379000]` |
| base | constant | native_float64 | 0.000000 | -Infinity | **PASS** | `[0.0, 0.0, 0.0]` |
| base | constant | float32_input | 0.000000 | -Infinity | **PASS** | `[0.0, 0.0, 0.0]` |
| **gold** | **brutus** | **native_float64** | **0.023797** | **-1.6235** | **FAIL** | `[0.001090, 0.003442, 0.023797]` |
| **gold** | **brutus** | **float32_input** | **0.023795** | **-1.6235** | **FAIL** | `[0.001135, 0.003449, 0.023795]` |
| gold | constant | native_float64 | 0.000000 | -Infinity | **PASS** | `[0.0, 0.0, 0.0]` |
| gold | constant | float32_input | 0.000000 | -Infinity | **PASS** | `[0.0, 0.0, 0.0]` |

---

## 6. Detailed Analysis of Findings

### 6.1 The Discrepancy Between Explicit Velocity and Finite-Difference Velocity

In the FEAS-01 evaluation, Brutus trajectories use the recorded explicit velocities output directly by the high-precision Bulirsch-Stoer integration engine:
$$\text{eps}_H(\text{explicit}) = \max_t \left| \frac{H(\mathbf{r}(t), \mathbf{v}_{\text{recorded}}(t)) - H_0}{H_0} \right| \sim 10^{-11} \text{ to } 10^{-14}$$
This achieves near machine-precision Hamiltonian conservation, placing all three systems in **Tier 3**.

In contrast, the production validation gate operates on positions alone and constructs velocities using 2nd-order centered finite differences:
$$\mathbf{v}_{\text{FD}}(t_n) = \frac{\mathbf{r}(t_{n+1}) - \mathbf{r}(t_{n-1})}{2 \Delta t} = \mathbf{v}(t_n) + \frac{1}{6} \mathbf{r}^{(3)}(t_n) \Delta t^2 + O(\Delta t^4)$$
The kinetic energy evaluated with $\mathbf{v}_{\text{FD}}$ incurs an $O(\Delta t^2)$ discretization error proportional to acceleration curvature:
$$T_{\text{FD}} - T_{\text{true}} \approx \sum_i m_i \mathbf{v}_i \cdot \mathbf{r}_i^{(3)} \frac{\Delta t^2}{6}$$
At $\Delta t = 0.01$, $\Delta t^2 = 10^{-4}$. For highly dynamic chaotic 3-body orbits with tight close encounters, body jerk $\mathbf{r}^{(3)}$ can reach magnitudes of $10^2 - 10^3$, pushing $\Delta T / |H_0|$ directly into the $10^{-3} - 10^{-2}$ range.

As a direct mathematical consequence:
- System 1632 (10 inner laps): $\text{eps}_H(\text{FD}) = 1.09 \times 10^{-3}$ ($109\times$ above the $10^{-5}$ line).
- System 851 (18 inner laps): $\text{eps}_H(\text{FD}) = 3.44 \times 10^{-3}$ ($344\times$ above the $10^{-5}$ line).
- System 4658 (39 inner laps, closest encounter): $\text{eps}_H(\text{FD}) = 2.38 \times 10^{-2}$ ($2380\times$ above the $10^{-5}$ line).

Even at native gold resolution, **Brutus cannot pass the $10^{-5}$ finite-difference gate**. This provides the definitive empirical proof required by `GAP-59-08` and establishes that any neural network trained to match Brutus positions would also fail this validation gate unless it deviates from the true positions.

### 6.2 The Constant Baseline Anomaly

The constant predictor sets $\mathbf{r}(t) = \bar{\mathbf{r}}$ and $\mathbf{v}(t) = \mathbf{0}$.
- Because positions are static, finite-difference velocity is identically zero: $\mathbf{v}_{\text{FD}} \equiv \mathbf{0}$.
- The Hamiltonian series is $H(t) = U(\bar{\mathbf{r}}) = \text{const}$.
- The peak absolute change $\Delta H_{\text{abs\_max}} = 0.0$, giving $\text{eps}_H = 0.0$ and $\text{SCS} = -\infty$.
- The constant predictor passes the production gate with verdict `PASS`, despite having position error $E > 1.14$ (Tier 0).
- This finding demonstrates that the production gate $\text{eps}_H \le 10^{-5}$ evaluates **internal consistency of energy conservation**, not **trajectory accuracy**.

---

## 7. Data Access and Process Isolation

The execution complied strictly with the v2.5 data isolation requirements:

```
{
  "schema": "phase59-files-opened/v1",
  "tool": "yardstick_audit",
  "data_root_source": "git_common_dir_default",
  "opened": {
    "train": 6,
    "validation": 0,
    "other_under_root": 0
  },
  "blocked_attempts": 0,
  "refused_before_open": 0,
  "test_split_opened": 0
}
```

- Admitted records opened: exactly 6 (`hierarchical/base/1632`, `hierarchical/gold/1632`, `hierarchical/base/851`, `hierarchical/gold/851`, `hierarchical/base/4658`, `hierarchical/gold/4658`).
- Preserved evaluation remains completely unspent (0 validation opens, 0 test opens).
- Verification replay confirms deterministic reproduction with exit code 0 and `YARDSTICK-AUDIT-OK`.
