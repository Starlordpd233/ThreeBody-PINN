---
status: active
purpose: verification-report
created: 2026-10-04
milestone: untracked
phase: cross-cutting
review_target: pinn_instruction/markdown_conversion/framework-specs/trainex-r4/
baseline_commit: 735e2ae8d5ec30b9915ec9172ac06965fbaa8afb
package_commit: d3a6e61bbb39a986bd7df440de817d74e0dae153
retirement_trigger: the trainex-r4 round is consumed — its reports are verified (Rule 19), consolidated, and the owner has ruled on the decision sheet
---

# trainex-r4 Package Double-Check Analysis & Pre-Handoff Findings

**Document Purpose:** Independent verification of the `trainex-r4` External Research Workflow (ERW) research package prior to external agent dispatch. This report documents both the verified ground truth and specific discrepancies discovered during an in-depth, secondary audit of the authored artifacts.

**Audience:** Project owner and peer reviewing agents evaluating the integrity and accuracy of the `trainex-r4` handoff package.

---

## 1. Executive Summary

The `trainex-r4` package located at `pinn_instruction/markdown_conversion/framework-specs/trainex-r4/` was evaluated against repository baseline `735e2ae8d5ec30b9915ec9172ac06965fbaa8afb`.

- **Mechanical Bars:** All 8 mechanical audit bars (Bars A, A2, B, C, D, E, F, G) established in `docs/work/reviews/cross_cutting/trainex-r4/2026-10-04-trainex-r4-package-audit.md` pass under independent re-execution.
- **Bundle Fidelity:** All 11 excerpts in `specs/framework-specs-bundle.md` and all 9 verbatim parts in `research_package/v2.3-closure-evidence-bundle.md` are byte-identical to `git show 735e2ae8:<path>`. The derived telemetry digest script (SHA-256 `12dd87f6...`) executes cleanly and reproduces the embedded tables byte-for-byte.
- **Substantive Accuracy:** Claims `F-01` through `F-06`, `F-08` through `F-12`, and `F-14` through `F-18` are strictly verified against underlying run logs, checkpoints, configurations, and rulings.
- **Discrepancies Identified:** Four distinct issues were identified in `research_package/RESEARCH-CONTEXT-MASTER.md`:
  1. **Finding 1 (Numerical Typo in F-07):** Tabulated `loss_data` range lower bound stated as `0.0164` instead of `0.0160` (step 931).
  2. **Finding 2 (Internal Contradiction in F-13 vs F-02):** `F-13` describes Generation 6's monitor front as "still 2 when the process died", whereas `F-02` and the checkpoint replay establish the instantaneous front had fallen back to 1 (only the high-water mark was 2).
  3. **Finding 3 (Step 951/952 Logging Nuance in F-07):** Trip loss values match the halted step recorded as `step 952` in `train.log.jsonl` rather than completed `step 951`. Tabulated Part G terminates at step 951, producing an apparent mismatch without explanatory context.
  4. **Finding 4 (Manifest Path Omission):** Table §2 lists `framework-specs-bundle.md` without the `specs/` directory prefix.

---

## 2. Verification Matrix

| Target / Item | Status | Verification Detail / Command |
|---|---|---|
| **Bar A (Lexical Ban)** | **PASS** | No banned terms (`recommend`, `suggest`, `prefer`, etc.) in §0–§8 of `RESEARCH-CONTEXT-MASTER.md`. |
| **Bar A2 (Rule 7 Output Contract)** | **PASS** | 6 matching lines (minimum 4) in §9. |
| **Bar B (Questions Q1–Q5 Verbatim)** | **PASS** | Normalized byte match with §6 of `58-diag-06-verdict-packet.md`. |
| **Bar C (Read-Only Boundary)** | **PASS** | `git diff --stat 735e2ae8 d3a6e61b` touches only package directory. |
| **Bar D (Pin Consistency)** | **PASS** | `source_baseline: 735e2ae8...` identical across all 5 markdown documents. |
| **Bar E (Bundle Excerpts Fidelity)** | **PASS** | 20 of 20 verbatim blocks byte-identical to `git show 735e2ae8:<path>`. |
| **Bar E (Part G Digest Reproduction)** | **PASS** | Script SHA-256 matches; execution matches digest output byte-for-byte. |
| **Bar F (Citation Resolution)** | **PASS** | All 20 `path:line` citations resolve to valid source lines at baseline. |
| **Bar G (Attachment Cap)** | **PASS** | Exactly 3 attachments specified (under ERW Rule 15 cap of 5). |
| **F-01 (Trip State & Metric)** | **PASS** | Invariant B tripped at step 951; `steps_since_front_advance = 501.0 > 500.0`. |
| **F-02 (Frozen Replay Arithmetic)** | **PASS** | Front distances, sums, next weights at all tabulated checkpoints verified. |
| **F-03 (Per-bin Reductions)** | **PASS** | Bins 0–5 reductions: 3.5×, 2.7×, 3.2×, 2.2×, 2.1×, 1.5×; sum = 3.88. |
| **F-04 (Learning Rate Schedule)** | **PASS** | Cosine decay values at steps 1, 450, 900, 950, 951 match log values. |
| **F-05 (Optimizer Phase)** | **PASS** | All 952 records are phase `2a`; L-BFGS never ran. |
| **F-06 (Warmup & Lambdas)** | **PASS** | Physics warmup to 1.0 at step 101 (graded) and step 31 (smoke). |
| **F-07 (Loss Term Ranges & Trip)** | **FAIL (Minor)** | `loss_data` range lower bound typo (Finding 1) & step 952 trip alignment (Finding 3). |
| **F-08 (Gradient Norm Ratios)** | **PASS** | 19 diagnostic steps; `applied_ic / applied_phys` ranges from 2.78e+04 to 2.62e+06. |
| **F-09 (Training-Batch Front Histogram)** | **PASS** | `{0: 342, 1: 381, 2: 194, 3: 35}`, 492 changes, first 3 at step 677. |
| **F-10 (Front Definition Locality)** | **PASS** | Spec does not define `front_idx` or `w_n > 0.5`; code and rulings define them. |
| **F-11 (Init Front 0 & Late Bin Prefix)** | **PASS** | Structurally verified against causal prefix formulation. |
| **F-12 (Recipe Ratification & R_ref)** | **PASS** | Governed `R_ref = 1.9749775821244170e+10` verified against JSON artifact. |
| **F-13 (Gen 6 & Gen 7 Seed 42 Comparison)** | **FAIL (Ambiguity)** | Front 2 high-water mark vs instantaneous front contradiction (Finding 2). |
| **F-14 (Smoke Run State)** | **PASS** | Smoke reached front 1 at step 93; training-batch front never exceeded 1. |
| **F-15 (Epoch Budget Provisional Status)** | **PASS** | Verified against `ctl_instruction.md:1994-1997`. |
| **F-16 (First Omega 0 Fixed at 30)** | **PASS** | Verified against `pinn_architecture.md:181, :188`. |
| **F-17 (Single Graded Launch)** | **PASS** | Seed 42 only; seeds 41/43 not launched. |
| **F-18 (Held-out Evaluation Preservation)** | **PASS** | Verified unspent (`no-candidate.json`). |

---

## 3. Detailed Findings and Discrepancies

### Finding 1: Numerical Range Error in Claim `F-07` (`loss_data` lower bound)

- **Target File:** `pinn_instruction/markdown_conversion/framework-specs/trainex-r4/research_package/RESEARCH-CONTEXT-MASTER.md`
- **Location:** Line 329, table row `F-07`
- **Current Text:**
  ```text
  `loss_data` from 0.0164 to 0.0721.
  ```
- **Analysis:**
  Examining the tabulated steps (`KEY_STEPS = [1, 50, 93, 100, 101, 200, 300, 353, 400, 450, 451, 500, 513, 600, 700, 800, 900, 931, 941, 950, 951]`) in Part G for `stage0-v23g7-seed42`:
  - Step 1: `0.072055...` (formatted `0.0721`)
  - Step 900: `0.016489...` (formatted `0.0165`)
  - Step 931: `0.0159758...` (formatted `0.016`)
  - Step 941: `0.016480...` (formatted `0.0165`)
  - Step 950: `0.016565...` (formatted `0.0166`)
  - Step 951: `0.016412...` (formatted `0.0164`)
  The value `0.0164` is the `loss_data` value at **step 951**. However, the minimum across the tabulated steps occurs at **step 931**, where `loss_data = 0.0159758` (`0.0160`). Across all 952 steps in `train.log.jsonl`, the absolute minimum is `0.0158389` at step 906.
- **Severity:** Low (factual range typo).
- **Remediation:** Update range to: `` `loss_data` from 0.0160 (step 931) to 0.0721 (step 1) ``.

---

### Finding 2: Contradiction Between `F-13` and `F-02` Regarding Generation 6 Front Status

- **Target File:** `pinn_instruction/markdown_conversion/framework-specs/trainex-r4/research_package/RESEARCH-CONTEXT-MASTER.md`
- **Location:** Line 335, table row `F-13`
- **Current Text:**
  ```text
  Generation 6's monitor reached front 2 at step 353 and was still 2 when the process died at step 513
  ```
- **Conflict with `F-02`:**
  Line 324 (`F-02`) states:
  ```text
  Gen 6 steps 490 / 500 / 510: front 1 (back from 2), bins 0–1 = 0.954 / 0.805 / 0.789.
  ```
- **Analysis:**
  - In `runs/stage0-v23g6-seed42/checkpoints/`:
    - `step-000490.pt`: `front_idx = 1`, `stored_invariant_b.front_high_water = 2`
    - `step-000500.pt`: `front_idx = 1`, `stored_invariant_b.front_high_water = 2`
    - `step-000510.pt`: `front_idx = 1`, `stored_invariant_b.front_high_water = 2`
  - In `.planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/blocked-state-g6.json`:
    ```json
    "invariant_b_state": {
      "front_high_water": 2,
      "last_advance_step": 353
    }
    ```
  `F-13` transcribed the wording directly from `57-05-SUMMARY.md` line 152 (*"had reached front 2 at step 353 and was still at 2 when it died at step 513"*), where the author intended `front_high_water`. Stating that the monitor "was still 2" directly contradicts the frozen-monitor replay in `F-02` showing the instantaneous front fell back to 1.
- **Severity:** Medium (internal analytical inconsistency that external review agents will flag as a premise contradiction).
- **Remediation:** Update `F-13` to explicitly specify: `` Generation 6's monitor high-water mark reached 2 at step 353 and remained 2 when the process died at step 513, while its instantaneous front had dropped back to 1 ``.

---

### Finding 3: Telemetry Disconnect Between `trip.json` and Tabulated Step 951 in `F-07`

- **Target File:** `pinn_instruction/markdown_conversion/framework-specs/trainex-r4/research_package/RESEARCH-CONTEXT-MASTER.md`
- **Location:** Line 329, table row `F-07`
- **Current Text:**
  ```text
  At the trip: `ic 1905.42`, `phys 0.0794`, `data 0.0163`
  ```
- **Analysis:**
  An external research agent comparing `F-07` against the Part G table for step 951 will observe:
  - Part G table step 951: `loss_ic = 2.83e+03` (`2828.94`), `loss_phys = 0.0733`, `loss_data = 0.0164`.
  - `F-07` trip text: `ic 1905.42`, `phys 0.0794`, `data 0.0163`.
  
  **Root Cause in Trainer Implementation:**
  In `pinn/training/controllers.py`:
  - Completed optimizer step 951 logged with `"step": 951`.
  - On the subsequent iteration (`_global_step = 951`, which represents the calculation for step 952), the guard hook evaluates loss terms and triggers:
    ```python
    guard_outcome = self._guard_hook(self, loss_terms, grad_norm, self._global_step, k, "2a")
    ```
  - The guard generates `trip.json` with `"step": 951` and records the current evaluated `loss_terms` (`ic: 1905.42`, `phys: 0.07937`, `data: 0.01632`).
  - Next, `controllers.py` line 2119 logs the diverged/halted step with:
    ```python
    self._log_step(step=self._global_step + 1, loss_terms=loss_terms, lr=None, step_completed=False, ...)
    ```
    This emits record `"step": 952` in `train.log.jsonl`.
  - Because Part G's `KEY_STEPS` concludes at step 951, the values for the halted step (row 952) are absent from the table.
- **Severity:** Low to Medium (source of confusion for third-party automated agents).
- **Remediation:** Clarify in `F-07` that the trip values reflect the uncompleted halt step logged at index 952.

---

### Finding 4: Minor Path Omission in Master Manifest Table

- **Target File:** `pinn_instruction/markdown_conversion/framework-specs/trainex-r4/research_package/RESEARCH-CONTEXT-MASTER.md`
- **Location:** Line 96, §2 Manifest table
- **Current Text:**
  ```text
  | 2 | `framework-specs-bundle.md` | Eleven verbatim excerpts... |
  ```
- **Analysis:**
  Attachment 2 is located at `specs/framework-specs-bundle.md`. Both `DELIVERY-NOTE.md` (line 43) and `RESEARCH-AGENT-PROMPT.md` (line 19) cite the full relative path `specs/framework-specs-bundle.md`. Listing `framework-specs-bundle.md` without the directory prefix is inconsistent.
- **Severity:** Minor (path precision).
- **Remediation:** Change to `specs/framework-specs-bundle.md`.

---

## 4. Verification Evidence & Replication Commands

Any peer agent can independently reproduce these findings using the following shell and Python commands:

```bash
# 1. Verify loss_data minimum in Part G tabulated steps:
python3 -c "
import json
rows = [json.loads(l) for l in open('runs/stage0-v23g7-seed42/logs/train.log.jsonl') if l.strip()]
key_steps = [1, 50, 93, 100, 101, 200, 300, 353, 400, 450, 451, 500, 513, 600, 700, 800, 900, 931, 941, 950, 951]
tab = [r for r in rows if r['step'] in key_steps]
min_data = min(tab, key=lambda r: r['loss_data'])
print(f'Tabulated min loss_data: {min_data[\"loss_data\"]} at step {min_data[\"step\"]}')
"

# 2. Verify Gen 6 instantaneous monitor front vs high-water mark:
python3 -c "
import torch
for s in [490, 500, 510]:
    ckpt = torch.load(f'runs/stage0-v23g6-seed42/checkpoints/step-000{s}.pt', map_location='cpu', weights_only=True)
    inv = ckpt.get('invariant_b_state')
    print(f'Gen 6 step {s}: invariant_b_state={inv}')
"

# 3. Verify step 951 vs 952 logging and trip alignment:
python3 -c "
import json
rows = [json.loads(l) for l in open('runs/stage0-v23g7-seed42/logs/train.log.jsonl') if l.strip()]
trip = json.load(open('runs/stage0-v23g7-seed42/failure/trip.json'))
r951 = [r for r in rows if r['step'] == 951][0]
r952 = [r for r in rows if r['step'] == 952][0]
print(f'trip.json loss_ic={trip[\"loss_terms\"][\"ic\"]}')
print(f'log step 951 loss_ic={r951[\"loss_ic\"]}, step_completed={r951.get(\"step_completed\", True)}')
print(f'log step 952 loss_ic={r952[\"loss_ic\"]}, step_completed={r952.get(\"step_completed\", True)}')
"
```

---

## 5. Recommended Unified Patch

Below is the proposed unified diff for `research_package/RESEARCH-CONTEXT-MASTER.md` to resolve all four findings:

```diff
diff --git a/pinn_instruction/markdown_conversion/framework-specs/trainex-r4/research_package/RESEARCH-CONTEXT-MASTER.md b/pinn_instruction/markdown_conversion/framework-specs/trainex-r4/research_package/RESEARCH-CONTEXT-MASTER.md
index 6dc2a76..9bb2312 100644
--- a/pinn_instruction/markdown_conversion/framework-specs/trainex-r4/research_package/RESEARCH-CONTEXT-MASTER.md
+++ b/pinn_instruction/markdown_conversion/framework-specs/trainex-r4/research_package/RESEARCH-CONTEXT-MASTER.md
@@ -93,7 +93,7 @@ This packet frames questions. It marks no default, orders no option, and picks
 | # | Attachment | Treatment |
 |---|---|---|
 | 1 | `RESEARCH-CONTEXT-MASTER.md` — this file | The entry point. §3 fixes how to treat each source, §5 carries the questions, §9 the output contract. |
-| 2 | `framework-specs-bundle.md` | Eleven verbatim excerpts of the locked framework specs at the baseline commit: SIREN initialization and the `first_omega_0` record, the skip/power stack, the hyperparameter table, §3.2 with its three Phase 56 contract blocks, the IC loss, the warmup and clip guard, the optimizer split and clipping, Stage 0, the total-loss assembly, the Adam and L-BFGS phases, and the stage transition criteria. **Hard constraint** as a statement of what the contract currently says. |
+| 2 | `specs/framework-specs-bundle.md` | Eleven verbatim excerpts of the locked framework specs at the baseline commit: SIREN initialization and the `first_omega_0` record, the skip/power stack, the hyperparameter table, §3.2 with its three Phase 56 contract blocks, the IC loss, the warmup and clip guard, the optimizer split and clipping, Stage 0, the total-loss assembly, the Adam and L-BFGS phases, and the stage transition criteria. **Hard constraint** as a statement of what the contract currently says. |
 | 3 | `v2.3-closure-evidence-bundle.md` | Verbatim: the owner verdict (A), the verdict packet with its frozen-monitor replay (B), the recalibration ruling (C), the checkpoint ③/④ ruling (D), the Phase 56 front-index findings (E), and the terminal, trip, and config records (F1–F4). Plus one **derived** digest of the Git-tracked training logs (G), with its exact script and output. |
 
 Files at the round root that are **not** uploaded: `DELIVERY-NOTE.md`
@@ -329,7 +329,7 @@ Run artifacts are cited by repository path; Part letters refer to `v2.3-closure-
 | F-06 | `I_warm = min(2000, 0.1 · N_Adam,k)` and `λ_phys^max(k) = 1` **[LOCKED]**. Logged `lambda_phys` is 0.0 at step 1 and first reaches 1.0 at step 101 (graded) and step 31 (smoke, `n_adam: 300`). `lambda_data` and `lambda_ic` are 1.0 and `lambda_e` and `lambda_l` are 0.0 on every logged step. On every record, `total` equals the λ-weighted sum of the five loss terms | `pinn_architecture.md:699-701`; Part G | established |
-| F-07 | Generation-7 graded logged loss terms at the tabulated steps: `loss_ic` from 84.3 (step 900) to `8.2e+04` (step 200), changing by more than 10× between neighbouring tabulated steps (e.g. 84.3 at 900, 1.54e+03 at 931, 1.91e+04 at 941, 110 at 950). `loss_phys` (after `R_ref` normalization) from 0.0733 to 0.192. `loss_data` from 0.0164 to 0.0721. At the trip: `ic 1905.42`, `phys 0.0794`, `data 0.0163` | Part G; `runs/stage0-v23g7-seed42/failure/trip.json` (Part F2) | established |
+| F-07 | Generation-7 graded logged loss terms at the tabulated steps: `loss_ic` from 84.3 (step 900) to `8.2e+04` (step 200), changing by more than 10× between neighbouring tabulated steps (e.g. 84.3 at 900, 1.54e+03 at 931, 1.91e+04 at 941, 110 at 950). `loss_phys` (after `R_ref` normalization) from 0.0733 to 0.192. `loss_data` from 0.0160 (step 931) to 0.0721 (step 1). At the trip (the halted step logged as step 952): `ic 1905.42`, `phys 0.0794`, `data 0.0163` | Part G; `runs/stage0-v23g7-seed42/failure/trip.json` (Part F2) | established |
 | F-08 | On the 19 generation-7 graded steps with complete gradient statistics (every 50 steps), `applied_ic / applied_phys` ranges from `2.78e+04` (step 900) to `2.62e+06` (step 50); `applied_data` ranges from 1.45 to 5.78. `raw` is the global parameter-gradient L2 norm of the unweighted term; `applied = λ × raw` | Part G; `pinn/training/controllers.py:483-507` (canonical builder), `:1993-2009` (the microbatched Adam path these steps used, provenance `microbatch_pass2_diagnostic`) | established |
 | F-09 | Generation-7 graded training-batch `front_idx` histogram `{0: 342, 1: 381, 2: 194, 3: 35}`, 492 step-to-step changes, first value 3 at step 677. The frozen monitor's high-water mark never exceeded 2. By ruling, a resampled training-batch front is diagnostic only and cannot satisfy invariant B | Part G; `terminal-state.json` (Part F1); `54-RULING.md` "Front-monitoring boundary" (Part C); `57-RULING.md` §2 (Part D) | established |
 | F-10 | `front_idx` is the largest `n` with `w_n > 0.5`, computed in code for the frozen monitor and for training batches. Neither locked spec defines `front_idx`, its threshold, or invariant B's window: `pinn_architecture.md` mentions the front only inside the Phase 56 contract block at `:452` (GATE-04's front condition; training-batch front diagnostic only), and `ctl_instruction.md` has no occurrence. `N = 500` and the frozen training-only monitor are an owner ruling | `pinn/training/controllers.py:1058` (monitor), `:1241`, `:1974` (training batch); `pinn_architecture.md:452`; `57-RULING.md` §2 (Part D) | established |
 | F-11 | Under the ratified formula, front 0 at initialization is the expected healthy result, and a residual reduction confined to late bins cannot move the front at any magnitude | `56-OPEN-ITEMS.md` Section 2 (Part E) | established |
 | F-12 | The ratified recipe `A1 + B2 (residual-wide) + C1 + D3 + E1`: `η_c = 1` on `R̃_b = R̄_b / R_ref`; one frozen `R_ref` = median of 96 initialization bin means from the six-case GATE-04 probe, also applied to the training physics loss; `first_omega_0 = 30`; 4096 rows per batch in 16 equal bins (256 per bin) with one batch-global 16-term prefix; clip unchanged. Governed `R_ref = 1.9749775821244170e+10` (logged `r_ref` `19749775821.24417`). GATE-04 passed on the amended recipe | `54-RULING.md` disposition table (Part C); `pinn_architecture.md:452`, `:454`, `:456`; `pinn/verification/artifacts/r_ref_stage0.json`; Part G | established |
-| F-13 | Generation-6 and generation-7 seed 42 share the seed and the configuration apart from `run.run_name`, and ran at commits `ef4764f9…` and `629b1a6c…`. Logged values are identical through step 8, differ from step 9 in the seventh or eighth significant figure, agree to three significant figures at every tabulated step through 200, and differ visibly by step 300. Generation 6's monitor reached front 2 at step 353 and was still 2 when the process died at step 513 | Part G and its reading notes; `.planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/blocked-state-g6.json`; `.planning/phases/57-corrected-re-run-the-preserved-evaluation/57-05-SUMMARY.md` "Descriptive record" | established |
+| F-13 | Generation-6 and generation-7 seed 42 share the seed and the configuration apart from `run.run_name`, and ran at commits `ef4764f9…` and `629b1a6c…`. Logged values are identical through step 8, differ from step 9 in the seventh or eighth significant figure, agree to three significant figures at every tabulated step through 200, and differ visibly by step 300. Generation 6's monitor high-water mark reached 2 at step 353 and remained 2 when the process died at step 513, while its instantaneous front had dropped back to 1 | Part G and its reading notes; `.planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/blocked-state-g6.json`; `.planning/phases/57-corrected-re-run-the-preserved-evaluation/57-05-SUMMARY.md` "Descriptive record" | established |
 | F-14 | The generation-7 smoke (`n_adam: 300`) finished. Its monitor reached front 1 at step 93, the same as generation 6's smoke. Its training-batch front never exceeded 1 | `57-05-SUMMARY.md` "Descriptive record"; `configs/stage0-v23g7-smoke.yaml` (Part F4); Part G | established |
```
