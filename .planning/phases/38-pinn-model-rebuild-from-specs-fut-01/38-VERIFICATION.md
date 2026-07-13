---
phase: 38-pinn-model-rebuild-from-specs-fut-01
verified: 2026-07-13
status: passed
score: 12/12
gaps_remaining: []
must_haves:
  - NET-01..05 goal-backward verification
  - rung 2 fp64-CPU gradcheck evidence
  - rung 3 residual-on-ground-truth on a real admitted Brutus trajectory
  - rung 4 single-trajectory overfit on a real admitted Brutus trajectory
  - prohibitions (spec byte-identity, no sim_data writes, no precision default, no v1.3 derivation)
artifacts:
  - evidence/gradcheck/20260713T121039Z/
  - evidence/residual/20260713T133400Z/
  - evidence/overfit/20260713T133619Z/
  - tests/phase38/ (128 tests, OK)
---

# Phase 38: Verification Report

**Goal (38-SPEC.md):** `pinn/` carries a spec-faithful model — SQR-SkipResNet-SIREN with the hard
mass-weighted COM projection head, PHYS-02 autograd physics residuals, and the locked five-term loss
catalog — rebuilt from `ctl_instruction.md` / `pinn_architecture.md` (not the v1.3-era code), and proven
correct by the gradcheck, residual-on-ground-truth, and single-trajectory-overfit rungs before it feeds
any training run.

**Verdict: PASS — goal delivered.** The rebuilt `pinn/` package meets NET-01..05. All three proof rungs
produce recorded PASS evidence, and **rungs 3 and 4 now pass on a REAL admitted Brutus trajectory**
(the phase-close gate `GAP-38-01`, previously `DEFERRED` for want of the dataset payload, is closed this
verification via decision B). The automated suite is green (128 tests OK); all four MUST-NOT prohibitions
hold. No open gaps remain.

---

## Goal-backward acceptance-criteria matrix (12/12)

| # | Acceptance criterion (38-SPEC.md) | Evidence | Status |
|---|-----------------------------------|----------|--------|
| 1 | Structure test: exact topology 14→256; 12 hidden 256×256; 256→9; SIREN `first_omega_0=30.0`/`hidden_omega_0=1.0`; LayerNorm `elementwise_affine=False` on odd layers + skips | `tests/phase38/test_network_structure.py` (128-test suite) | ✅ |
| 2 | Forward pass succeeds under both `resolve_runtime` branches (fp32-MPS and fp64-CPU) through the same code path | `tests/phase38/test_network_structure.py`, `test_architecture_spec.py` (fp64-CPU certified here; fp32-MPS path exercised by the Phase-37 substrate + structure tests) | ✅ |
| 3 | Same config + seed ⇒ identical params; no FS / global-state writes (edge R1) | `tests/phase38/test_network_structure.py` (determinism + side-effect assertions) | ✅ |
| 4 | Projected outputs satisfy `Σ mᵢ·rᵢ′ = 0` within dtype tol; idempotent; no loss/metric consumes unprojected output (edge R2) | `tests/phase38/test_com_projection.py` | ✅ |
| 5 | `torch.autograd.gradcheck` passes on the physics-residual computation under fp64-CPU | **Rung 2** — `evidence/gradcheck/20260713T121039Z/` (eps=1e-6, atol=1e-5, rtol=1e-3, PyTorch 2.12.1, PASS) | ✅ |
| 6 | Residual-on-ground-truth probe runs on a Brutus trajectory and exits PASS; threshold + measured values recorded | **Rung 3 (REAL trajectory)** — `evidence/residual/20260713T133400Z/` | ✅ |
| 7 | All five loss terms finite on a synthetic batch; δ values, causal weighting, `D ≈ 4.6416` conversions confirmed | `tests/phase38/test_loss_catalog.py` | ✅ |
| 8 | Single-trajectory overfit probe reduces data loss ≥ 10³×; achieved floor recorded | **Rung 4 (REAL trajectory)** — `evidence/overfit/20260713T133619Z/` (ratio 1097.6) | ✅ |
| 9 | MUST NOT: `ctl_instruction.md` / `pinn_architecture.md` byte-identical before and after every Phase 38 commit | `tests/phase38/test_prohibitions.py` — endpoint sha256 + history-aware `git log --name-only <base>..HEAD` empty | ✅ |
| 10 | MUST NOT: no `pinn/` module hard-codes precision/device or encodes a precision default | `tests/phase38/test_prohibitions.py` — AST scan over glob-discovered `pinn/**/*.py` | ✅ |
| 11 | MUST NOT: no implementation derived from the v1.3-era `pinn/` files | `tests/phase38/test_prohibitions.py` — no-import check + spec-faithfulness review | ✅ |
| 12 | MUST NOT: no Phase 38 code or probe writes under `simulation_data/` | `tests/phase38/test_prohibitions.py` — write-spy over loader + probes; `git status --short simulation_data/` clean | ✅ |

---

## The three proof rungs

### Rung 2 — fp64-CPU gradcheck (PHYS-02 AD contract)

`evidence/gradcheck/20260713T121039Z/`. `gradcheck_result: true` under `float64`/`cpu`,
tolerances `eps=1e-6 / atol=1e-5 / rtol=1e-3` (PyTorch 2.12.1). Certifies the componentwise
second-derivative PHYS-02 path (`dr′/du = 2·dr′/dτ`, `d²r′/du² = 4·d²r′/dτ²`, `eps_soft = 1e-5`).

### Rung 3 — residual on ground truth (REAL admitted trajectory)

`evidence/residual/20260713T133400Z/`. Variant `standard_quasi_random_gold_standard`, id `0000`
(1002 snapshots, final time 10.01 ≥ 9.5 completeness gate; equal masses [1,1,1]; GT mass-weighted COM
offset 1.49e-12).

- **Gate A (force–energy consistency):** max relative error **1.4952905418063441e-15** < `1e-5` → **PASS**
  (near machine precision — the loaded trajectory's frame is physically consistent with the
  softened-Newtonian residual model: `r_safe = sqrt(‖d‖² + eps_soft²)`, raw masses, G absorbed into D).
- **Gate B (u-leaf Newtonian ODE residual):** median relative error **0.006471392964707071** < `0.1` → **PASS**
  (per-snapshot max 82.6 from finite-difference noise at small denominators; the median is the gated
  statistic). Excluded snapshots: 0 (min-separation guard never tripped).
- Overall: **PASS**.

### Rung 4 — single-trajectory overfit (REAL admitted trajectory)

`evidence/overfit/20260713T133619Z/`. Same trajectory.

- Initial data loss `L0 = 0.21921204799884003` → floor `Lf = 0.0001997174686303869`.
- **Ratio `L0/Lf = 1097.6107873895164` ≥ `1e3` → PASS**, reached in **176 steps** (Adam `lr=1e-4`,
  early-broke from the `--max-steps 5000` cap).
- Model conditioned on `tau_ic13(u_n) = [2u_n−1, zeros(13)]` (Phase-38 smoke placeholder; physically-normalized
  IC13 deferred to Phase 39); no COM-offset warning fired (offset ≪ `1e-3` threshold).
- The input-available diagnostic loss-catalog terms (data, IC, causal-physics, angular-momentum) evaluated
  finite at initial + final steps; soft-energy recorded "not evaluated — requires Phase 39/40 metadata".

---

## Real-trajectory phase-close evidence — `GAP-38-01` close-out (decision B)

`GAP-38-01` deferred rungs 3/4 on a real admitted Brutus trajectory because no payload existed in the
`.worktrees/trainex` checkout (the bulky `simulation_data/Data/{brutus_output,ic_final}/` trees are
gitignored and were not present in the worktree). The operator chose **decision B** (provide/copy one
admitted trajectory and re-run the evidence now) over `DEFERRED` (A) or `WAIVE` (C).

**Admitted trajectory provided.** The plan-sanctioned recommended default
(`38-03-PLAN.md <default_trajectory>`) — variant `standard_quasi_random_gold_standard`, nominal id `0000`,
admission encoded by gold-standard folder membership — was copied read-only from the master-root checkout
(worktrees do not receive gitignored payloads) into the worktree at the loader's folder-mapping paths:

- `simulation_data/Data/brutus_output/brutus_standard_quasi_random_gold_standard/brutus_standard_0000.txt`
  — sha256 `1e48ae0dad9b58b310228ca76cfb2ee8f767a76b4076997213358666bcb53aff`
- `simulation_data/Data/ic_final/ic_standard_quasi_random/ic_standard_0000.txt`
  — sha256 `36923ca8109179c61e45f29a151053a8d7041c04bece88dfb966dd329ebd932a`

Both paths are gitignored (`.gitignore:315` `ic_final/`, `:316` `brutus_output/`), so the copy introduces no
tracked noise; the loader resolves the pair via `resolve_trajectory_path(variant, id)` and binds both sha256
digests into probe provenance. The probes themselves only read `simulation_data/`; the operator copy is the
data-provision step decision B authorizes, not a probe write.

**Result:** both real-trajectory rungs PASS (see above). `GAP-38-01` is resolved
`RESOLVED-WITH-INSTRUCTION` in `38-GAPS.md`. The phase no longer closes on synthetic-only evidence.

---

## Prohibitions (MUST-NOT) — `tests/phase38/test_prohibitions.py` (6/6 OK)

1. **Spec byte-identity** — endpoint sha256 of both framework specs equals the pre-phase committed baseline
   (`git show <phase-base>:<spec> | shasum -a 256`), AND history-aware `git log --name-only <base>..HEAD`
   over both specs is empty. No Phase 38 commit touched either spec. ✅
2. **No `simulation_data/` writes** — write-spy over the write-capable I/O entry points across the loader +
   both probes (the weak mtime/snapshot fallback was dropped this phase); no target resolves under
   `simulation_data/`. `git status --short simulation_data/` is clean. ✅
3. **No precision default** — AST scan over the glob-discovered `pinn/**/*.py` module set (minus the
   documented v1.3 + Phase-37 excludes) finds no global default-dtype mutator, no MPS-availability probe,
   no encoded precision default. ✅
4. **No v1.3-era derivation** — no discovered module imports `basic_architecture`, the data-processing
   pipeline, or `data-handling/`. ✅

---

## Automated suite

```
conda run -n pinn-train python -m unittest discover -s tests/phase38 -p 'test_*.py'
-> Ran 128 tests in 20.741s
-> OK
```

The deliberate "FAIL" lines printed during the run are expected: the prohibition and fail-loud tests drive
the probes against degenerate synthetic fixtures (`--max-steps 1`, mutated gate-A fixtures, NaN-injected
inputs) to assert the FAIL path is loud and bounded. The suite verdict is OK with zero failures/errors.

---

## Out of scope / downstream handoff

Per 38-SPEC.md boundaries, the following remain **out of scope** for Phase 38 and are not verified here:
the in-memory admitted-set adapter / Step-1A admission gate / `data_version_hash` / split manifest / batch
constructor (**Phase 39**, DATA-01..06); the training loop, Adam→L-BFGS, the PHYS-05 scheduled-weight
*module*, collocation sampler, stage-exit machine (**Phase 40**, TRAIN-01..07); config/checkpoint/resume
(**Phase 41**); operator runbook + the packaged `verify` ladder + Stage-0 pilot (**Phase 42/43**).

The probe-local fixture loader is intentionally minimal (no Step-1A gate, no splits, no batching) — it is
**not** the Phase 39 adapter. The overfit probe's IC13 slot is a fixed `zeros(13)` placeholder;
physically-normalized IC13 (tanh with dataset-wide statistics) is Phase-39 territory.

---

## Closure verdict

**Phase 38 goal ACHIEVED.** The rebuilt `pinn/` package is spec-faithful (NET-01..05), proven by three
recorded rungs — gradcheck (fp64-CPU), residual-on-ground-truth, and single-trajectory overfit — with
rungs 3 and 4 now evidenced on a **real admitted Brutus trajectory** (the `GAP-38-01` phase-close gate,
closed this verification). All 12 acceptance criteria pass; all four MUST-NOT prohibitions hold; the
128-test automated suite is green; `simulation_data/` is untouched by Phase 38 code. **No open gaps.**
The spec-faithful model is ready to feed downstream training work (Phase 39 data adapter, Phase 40
training loop).

*Verification performed 2026-07-13 on branch `milestone/v2.0` in `.worktrees/trainex`, conda env `pinn-train`
(PyTorch 2.12.1), by the trainex verification pass under the Fable five-gate discipline.*
