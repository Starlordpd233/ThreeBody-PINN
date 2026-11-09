---
phase: 68
phase_name: "Yardstick"
project: "Three-Body Physics-Informed LLM"
generated: "2026-11-08"
counts:
  decisions: 6
  lessons: 5
  patterns: 5
  surprises: 4
missing_artifacts:
  - "68-UAT.md"
---

# Phase 68 Learnings: Yardstick

Phase 68 audited every judging metric and validation gate against Brutus ground truth and the window-mean constant baseline across the fixed Stage-0 training panel (`1632`, `851`, `4658`) on both the native gold ($dt = 0.01$) and coarse base ($dt = 0.08$) grids, without training any model or opening validation or test data. The committed known-answer audit empirically confirmed `GAP-59-08` (Brutus achieves Tier 3 with explicit velocities under FEAS-01 but fails the $10^{-5}$ centered finite-difference validation gate on every system, while the static constant predictor passes the energy gate with $\text{eps}_H = 0$). At owner checkpoint ②, the owner ruled `C-7: A` (autograd velocities in the validation gate and evaluator), closing `GAP-59-08` with instruction, left companion rows C-2, C-4, C-5 and C-6 open for separate discussion in v2.6, and routed all specification and code amendments (`ROUT-68-01..05`) to milestone v2.6. Extracted from `68-01-PLAN.md`, `68-01-SUMMARY.md`, `68-02-PLAN.md`, `68-02-SUMMARY.md`, `68-AUDIT.md`, `68-CHECKPOINT-2.md`, `68-CHECKPOINT-2-RULING.md`, `68-CONTEXT.md`, `68-VERIFICATION.md`, and `STATE.md`. No UAT file exists for this phase.

## Decisions

### Owner C-7 ruling selects Option A (autograd velocities), closing GAP-59-08
At owner checkpoint ②, the owner ruled verbatim `C-7: A. Leave C-2, C-4, C-5 and C-6 open for separate discussion.`, selecting automatic differentiation ($\mathbf{v}_{\text{autograd}} = \partial \mathbf{r}_{\text{pred}} / \partial t$) for velocity computation in the validation gate and held-out evaluator and resolving `GAP-59-08` in `59-GAPS.md` as `RESOLVED-WITH-INSTRUCTION`.

**Rationale:** centered finite differences on discrete position outputs introduce an $O(\Delta t^2)$ truncation floor that causes even exact Brutus ground truth to fail the $10^{-5}$ gate ($109\times$ to $2,380\times$ above threshold on the gold grid), whereas autograd evaluates the true instantaneous derivative implied by the continuous network trajectory and aligns with the FEAS-01 explicit-velocity convention.
**Source:** 68-CHECKPOINT-2-RULING.md, 68-02-SUMMARY.md, 68-VERIFICATION.md

### Leave companion charter rows C-2, C-4, C-5 and C-6 open for v2.6
Per the owner's explicit checkpoint ② instruction, Definition of Done (C-2), Stage-0 position pass bar (C-4), Stage-0 energy pass bar (C-5), and replacement of the locked $10^{-5}$ held-out bar (C-6) are recorded as `OPEN (deferred)` for separate discussion in milestone v2.6.

**Rationale:** under charter governance, unapproved rows or rows explicitly deferred by the owner supply no implied consent; recording them as open preserves the existing locked contracts in Phase 68 while establishing the C-7 autograd prerequisite that C-5 depends on.
**Source:** 68-CHECKPOINT-2-RULING.md, 68-02-PLAN.md, 68-02-SUMMARY.md

### Route all specification and gate amendments to milestone v2.6
Rather than editing `pinn_architecture.md`, `ctl_instruction.md`, `validation_gate.py`, or `evaluate.py` during Phase 68, the ruling establishes a five-entry routing table (`ROUT-68-01..05`) handing the §10.6 autograd clarification, validation/evaluator autograd support, companion pass-bar discussion, and C-11 evaluation-section rewrite to milestone v2.6.

**Rationale:** `SCOPE-46` forbids specification edits and production metric changes inside v2.5; routing ledger entries bind the owner's authority now while deferring edits to the redesign milestone.
**Source:** 68-CHECKPOINT-2-RULING.md, 68-02-SUMMARY.md

### Audit both explicit-velocity FEAS-01 and finite-difference gate calculations on the same fixed TRAIN panel
`pinn/verification/yardstick_audit.py` evaluates 12 prediction/grid groups (3 systems $\times$ 2 grids $\times$ 2 predictors) and 8 panel aggregates strictly through `Stage0TrainingReader`, `load_reference`, `score_trajectory`, `compute_trajectory_gate_metrics`, and `aggregate_gate_verdict`, with pre-path Stage-0/TRAIN admission and process-level split-open attestation.

**Rationale:** exercising the exact frozen scorer and shared production gate functions on identical in-memory Stage-0 training trajectories proves the discrepancy is intrinsic to the velocity estimator without touching validation/test splits or invoking the held-out evaluator receipt path.
**Source:** 68-01-PLAN.md, 68-01-SUMMARY.md, 68-AUDIT.md, 68-CONTEXT.md (D-01, D-02, D-03)

### Measure float32 input-rounding sensitivity separately from native float64 finite differences
Each audited prediction/grid group computes both the native float64 finite-difference gate reading (`gate_fd_native`) and a same-sample reading with positions, times, and masses cast to float32 before gate-time conversion (`gate_fd_float32_input`).

**Rationale:** production training and validation paths cross float32 residency boundaries; isolating float32 input rounding proves whether precision casts or finite-difference stencil truncation drive the observed energy drift.
**Source:** 68-01-PLAN.md, 68-01-SUMMARY.md, 68-AUDIT.md

### Preserve strict physical_window (t <= 10.0) base sample count difference as keyed evidence
On the coarse base grid ($dt = 0.08$), `physical_window(times, t_max=10.0)` retains 125 snapshots ($t \in [0.0, 9.92]$) because the 126th snapshot sits at $t = 10.000000000000007$, whereas the Phase 59 census retained 126 snapshots using $t \le 10.0 + 10^{-9}$; the audit records this difference explicitly rather than widening the window tolerance.

**Rationale:** `yardstick_audit.py` must mirror the exact diagnostic loader contract (`physical_window`) while keeping any grid-count delta against historical census artifacts visible and re-derivable.
**Source:** 68-01-SUMMARY.md, 68-AUDIT.md

---

## Lessons

### Centered finite differences create an O(dt^2) floor that rejects Brutus ground truth even at native gold cadence
Second-order centered finite differences approximate velocity with truncation error $\frac{1}{6}\mathbf{r}^{(3)}(t)\Delta t^2 + O(\Delta t^4)$, which feeds into kinetic energy as $\Delta T \approx \sum_i m_i \mathbf{v}_i \cdot \mathbf{r}_i^{(3)} \Delta t^2 / 6$. Even at native gold resolution ($\Delta t = 0.01$, $\Delta t^2 = 10^{-4}$), close encounters in chaotic three-body orbits produce jerk magnitudes that push $\text{eps}_H$ to $1.09 \times 10^{-3}$ (`1632`), $3.44 \times 10^{-3}$ (`851`), and $2.38 \times 10^{-2}$ (`4658`).

**Context:** auditing the C-7 Option B (dense-grid finite-difference) alternative in 68-01 and 68-02.
**Source:** 68-AUDIT.md (§1, §6.1), 68-CHECKPOINT-2.md (§1.1, §1.3)

### Energy conservation alone passes a static constant predictor that fails position accuracy completely
A window-mean constant predictor sets $\mathbf{r}(t) = \bar{\mathbf{r}}$ and $\mathbf{v}(t) = \mathbf{0}$, yielding zero kinetic energy and constant potential energy $U(\bar{\mathbf{r}})$. Its Hamiltonian drift is identically $\Delta H = 0.0$ ($\text{eps}_H = 0.0$, $\text{SCS} = -\infty$), earning a `PASS` verdict from the production energy gate despite catastrophic position error ($E \approx 1.14\text{--}1.24$, Tier 0, valid horizons $0.0$).

**Context:** evaluating the constant baseline across all 6 base/gold trajectory pairs in `yardstick_audit.py`.
**Source:** 68-01-SUMMARY.md, 68-AUDIT.md (§1, §6.2), 68-CHECKPOINT-2.md (§1.1)

### Float32 input rounding has negligible effect on finite-difference energy drift
Casting positions, times, and masses to float32 before running the finite-difference gate shifts the gold Brutus panel aggregate $\text{eps}_H$ from $0.023797$ to $0.023795$ ($< 0.012\%$ relative change) and base Brutus from $0.378998$ to $0.379000$.

**Context:** testing whether float32 residency casts contributed to the production validation gate failures.
**Source:** 68-01-SUMMARY.md, 68-AUDIT.md (§1, §4.2, §5)

### Strict t <= 10.0 drops the 126th base snapshot due to +7.1e-15 float roundoff
In the on-disk base records, $125 \times 0.08$ accumulates floating-point representation error to $t = 10.000000000000007$ ($+7.1 \times 10^{-15}$ above $10.0$). A strict `t <= 10.0` mask retains 125 samples ($t_{\text{last}} = 9.92$), whereas the gold grid's 1001st sample lands at $t = 9.999999999999831 \le 10.0$ and is retained.

**Context:** comparing retained sample counts in `yardstick_audit.py` against Phase 59 `census.csv` counts (`1001` gold / `126` base).
**Source:** 68-01-SUMMARY.md, 68-AUDIT.md (§1.4)

### Passing paths first to module_hashes is required for provenance pinning
During Task 68-01-02 implementation, `evidence_io.module_hashes` required the sequence of module paths as its first argument before keyword/root arguments, requiring a targeted fix commit (`e95f0b84`) before final capture.

**Context:** wiring producer module SHA-256 hashes into `yardstick_audit.py`.
**Source:** 68-01-SUMMARY.md

---

## Patterns

### Known-answer yardstick audit pairing exact ground truth against a trivial baseline
Evaluate every judging metric and gate simultaneously on (1) the exact numerical integrator ground truth (`brutus`) and (2) a trivial baseline (`window_mean_constant`) across the same fixed panel and grids, tabulating where the exact answer fails or the trivial answer passes.

**When to use:** qualifying any scientific evaluation metric or acceptance gate before using it to judge model training or spend a held-out exam.
**Source:** 68-01-PLAN.md, 68-AUDIT.md

### Little-endian float64 array digests for bitwise input preservation
Hash every scored time, position, velocity, and mass NumPy array as canonical little-endian `float64` bytes (`<f8`) alongside its shape tuple (`array_digest`), embedding the digests in the evidence JSON.

**When to use:** proving that two scoring or replay passes consumed bitwise-identical numerical arrays across processes or platforms.
**Source:** 68-01-PLAN.md, 68-01-SUMMARY.md

### Read-only replay verification (--check) tolerant only of invocation metadata
`python -B -m pinn.verification.yardstick_audit --check <path>` re-runs the full calculation in a fresh process, verifies that the capture commit is an ancestor of `HEAD` and producer hashes match, and requires canonical JSON equality on all scientific payloads while allowing only invocation metadata (timestamps, elapsed wall time, command argv, dirty flag, RSS, current `HEAD`) to vary.

**When to use:** deterministic CLI evidence artifacts that must be re-verifiable in CI or phase verification without overwriting committed evidence.
**Source:** 68-01-PLAN.md, 68-01-SUMMARY.md, 68-VERIFICATION.md

### Two-stage checkpoint packet separating prerequisite measurement rulings from dependent pass bars
Structure the owner decision packet (`68-CHECKPOINT-2.md`) so the prerequisite measurement choice (C-7) is presented first with committed audit evidence, and dependent pass-bar items (C-2, C-4, C-5, C-6) explicitly state their dependency on C-7 and can be decided or left open independently.

**When to use:** owner checkpoints where one technical/methodology choice changes the meaning or numerical scale of downstream target bars.
**Source:** 68-02-PLAN.md, 68-CHECKPOINT-2.md, 68-CHECKPOINT-2-RULING.md

### Explicit v2.6 routing table (ROUT-68-01..05) instead of in-phase contract edits
When a milestone's scope rules forbid editing specs or production code, record approved changes in a structured routing ledger (`Route ID`, `Target Document / File`, `Action Required`, `Source Authority`) inside the ratified ruling file.

**When to use:** adjudication or diagnosis phases operating under spec/code freeze constraints (`SCOPE-46`).
**Source:** 68-CHECKPOINT-2-RULING.md (§4), 68-02-SUMMARY.md

---

## Surprises

### Brutus fails the 10^-5 finite-difference gate by up to 2,380x on gold and 37,900x on base
Even when evaluated on the $8\times$ denser native gold grid ($dt = 0.01$), Brutus's exact trajectory fails the $10^{-5}$ finite-difference energy gate on every single panel system: $109\times$ above threshold on `1632` ($\text{eps}_H = 0.001090$), $344\times$ on `851` ($0.003442$), and $2,380\times$ on `4658` ($0.023797$). To reach $10^{-5}$ via finite differences during close encounters would require $dt \sim 10^{-5}$ (millions of points per trajectory).

**Impact:** ruled out C-7 Option B (dense-grid finite differences) as impractical on Mac hardware and made Option A (autograd velocities) the clear recommendation.
**Source:** 68-AUDIT.md (§1, §6.1), 68-CHECKPOINT-2.md (§1.2, §1.3)

### The window-mean constant predictor achieves SCS = -Infinity and a PASS verdict on the production gate
Because `gate_metrics.py` evaluates relative drift $|\Delta H| / |H_0|$ where $H_0 = U(\bar{\mathbf{r}}) \ne 0$ is finite and $\Delta H \equiv 0$, the static mean predictor achieves $\text{eps}_H = 0.0$ and $\text{SCS} = -\infty$, passing the production validation gate on both base and gold grids without moving a single body.

**Impact:** demonstrated that energy conservation must always be paired with a position accuracy criterion (C-4 + C-5) even after switching to autograd velocities.
**Source:** 68-AUDIT.md (§4.2, §6.2), 68-CHECKPOINT-2.md (§1.1)

### Close-encounter jerk r^(3) reaches 10^2 to 10^3 and dominates dt = 0.01 velocity truncation
Across the three panel systems, native gold FD $\text{eps}_H$ scales monotonically with orbital complexity and close-encounter tightness (`1632` at 10 inner laps $\rightarrow 1.09 \times 10^{-3}$; `851` at 18 inner laps $\rightarrow 3.44 \times 10^{-3}$; `4658` at 39 inner laps $\rightarrow 2.38 \times 10^{-2}$), governed by interior close-encounter jerk spikes rather than endpoint stencil boundary effects (`Peak Loc = interior` on all six Brutus rows).

**Impact:** confirmed that trimming trajectory endpoints cannot rescue finite-difference energy evaluation on chaotic three-body orbits.
**Source:** 68-AUDIT.md (§4.2, §6.1)

### The entire 12-group, 8-aggregate audit runs and replays in ~0.59 seconds
Despite loading six hierarchical base/gold trajectories, verifying manifest and scorecard digests, running 12 FEAS-01 explicit-velocity scorings, and computing 24 native/float32 finite-difference Hamiltonian series, the full fixed-panel capture and `--check` replay complete in ~0.59 seconds wall time.

**Impact:** allows `yardstick_audit.py --check` to run as an instant deterministic gate in unit and closeout verification suites.
**Source:** 68-AUDIT.md (§2), 68-VERIFICATION.md (§3)

