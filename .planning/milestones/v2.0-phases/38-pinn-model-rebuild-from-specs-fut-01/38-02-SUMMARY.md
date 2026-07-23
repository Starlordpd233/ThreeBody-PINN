---
phase: 38-pinn-model-rebuild-from-specs-fut-01
plan: "02"
subsystem: pinn
tags: [network, siren, sqr-skipresnet, com-projection, net-01, net-02, projected-only-forward, determinism]

requires:
  - phase: 38-pinn-model-rebuild-from-specs-fut-01
    provides: "plan 01 — pinn/constants.py + frozen ArchitectureSpec substrate"
  - phase: 37-developer-environment-precision-adjudication
    provides: "pinn-train env + RuntimeSpec/resolve_runtime seam + deferred-import test pattern"
provides:
  - "pinn/network.py — SQRSkipResNetSIREN backbone + build_network(spec, *, dtype, device) factory, projected-only public forward(tau_ic13, masses)"
  - "pinn/com_projection.py — pure idempotent mass-weighted project_com(positions, masses, *, dtype, device)"
  - "pinn/__init__.py — re-exports ArchitectureSpec, build_network, SQRSkipResNetSIREN"
  - "tests/phase38/test_network_structure.py, tests/phase38/test_com_projection.py — structure + projection suites"
affects:
  - "38-03 (residual) consumes the projected output of forward (NET-02 boundary)"
  - "38-04 (probes) consume build_network + forward(tau_ic13, masses) under both precision branches"
  - "38-05 (loss catalog) consumes projected positions only (unprojected output is not public)"
  - "38-06 (AST + overfit smoke) consumes the model; the placeholder-IC13 contract is fixed here"

tech-stack:
  added: []
  patterns:
    - "Raw nn.Parameter tensors built directly on (dtype, device) and filled via Tensor.uniform_(generator=<local>) — avoids nn.Linear.reset_parameters touching the global RNG"
    - "Local seeded torch.Generator(device=device) threaded through every layer; global RNG + default dtype pristine"
    - "SIREN forward wraps omega_0 as torch.as_tensor(..., dtype, device) — no Python-float x tensor on MPS"
    - "Projected-only public forward; raw 9-dim tensor exposed solely via private _forward_unprojected hook"

key-files:
  created:
    - "pinn/network.py"
    - "pinn/com_projection.py"
    - "tests/phase38/test_network_structure.py"
    - "tests/phase38/test_com_projection.py"
  modified:
    - "pinn/__init__.py"

key-decisions:
  - "SIREN principled init is UNIFORM via Tensor.uniform_(generator=<local>) on raw nn.Parameter tensors built directly on (dtype, device). First layer bound = 1/n_in (n_in=14); hidden bound = sqrt(6/n_in)/hidden_omega_0 (n_in=256, omega_0=1). Verified uniform: first-layer pooled var 0.001700 vs uniform b^2/3 0.001701; hidden pooled var 0.007814 vs 0.007812; max-abs reaches the bound in both. The init-statistics test's three checks (within-bound, var within +/-20% of b^2/3, max-abs >= 0.9b) jointly reject any Kaiming/Xavier NORMAL substitute."
  - "Bias init bound = the SAME bound as its layer's weights (first: 1/n_in; hidden: sqrt(6/n_in)/omega_0). The spec (pinn_architecture.md §2.2) fixes only weight bounds; bias bound is silent, so this is the conventional internally-consistent SIREN choice (mechanical, not a physics adjudication)."
  - "Output linear head (256->9, no activation) init: weight and bias U[-1/sqrt(n_in), 1/sqrt(n_in)] seeded by the LOCAL generator. Spec (§2.4 Table 1) fixes the output as linear but is silent on its init; PyTorch's default Linear fan-in bound was chosen and made deterministic via the local generator. Mechanical readout-init choice, not a physics adjudication."
  - "Avoided nn.Linear entirely so construction never advances the global RNG (nn.Linear.reset_parameters uses the global generator). Parameters are torch.empty(..., dtype, device) (uninitialized, no RNG) filled by uniform_(generator=<local>). torch.get_default_dtype() and the global CPU RNG are provably unchanged after build (asserted by no-side-effects tests)."
  - "omega_0 wrapped as torch.as_tensor(self.omega_0, dtype=x.dtype, device=x.device) inside _SIRENLayer.forward so the path never does Python-float x tensor on MPS (componentwise_ad MPS discipline)."
  - "Masses interface pinned (cycle-1 HIGH #2): forward(tau_ic13, masses) takes raw ordered masses EXPLICITLY (unrecoverable from the tanh-normalized IC13 mass slots; never assumed equal). tau_ic13 (14-dim) is supplied WHOLESALE — forward never synthesizes or re-normalizes the IC13 slice and imposes no IC13 normalization contract (cycle-3 HIGH #1). The 38-06 overfit smoke conditions on a fixed placeholder IC13."
  - "NET-02 boundary is structural (cycle-1 HIGH #1 / cycle-3): the public forward returns project_com(raw, masses) as the ONLY public output; the raw 9-dim tensor is reachable solely through the explicitly private _forward_unprojected hook. test_forward_return_equals_project_com_of_unprojected_hook asserts forward == project_com(raw, masses)."

patterns-established:
  - "Phase 38 model core: config-supplied ArchitectureSpec -> deterministic, precision-agnostic backbone with a projected-only forward; raw output reachable only via a private hook."
  - "Deferred-import per-symbol SkipTest guard (Phase 37 pattern) extended to cross-module structural tests (test_com_projection.py imports build_network per-symbol so partial impl SKIPs rather than ERRORs)."

requirements-completed: [NET-01, NET-02]

coverage:
  - id: N1
    description: "SQR-SkipResNet-SIREN backbone matches §2.4 Table 1 exactly (14->256 input, 12 hidden 256x256, 256->9 linear; SIREN first_omega_0=30 / hidden_omega_0=1; LayerNorm elementwise_affine=False eps=1e-5 on odd layers only; odd-layer update x = SIREN(x_prev) + (LayerNorm(x_prev))^2; even-layer plain SIREN; power p=2)"
    requirement: "NET-01"
    verification:
      - kind: unit
        ref: "tests/phase38/test_network_structure.py#TopologyTests (10 cases) — green under pinn-train"
        status: pass
    human_judgment: false
  - id: N2
    description: "SIREN principled init is UNIFORM (not normal) and tested: first/hidden-layer pooled weights within bound, var within +/-20% of b^2/3, max-abs >= 0.9b — a Kaiming/Xavier normal substitute cannot pass"
    requirement: "NET-01"
    verification:
      - kind: unit
        ref: "tests/phase38/test_network_structure.py#SirenInitStatisticsTests (6 cases) — green; empirical var matches uniform b^2/3 to 4 sig figs"
        status: pass
    human_judgment: false
  - id: N3
    description: "Deterministic + side-effect-free construction (local seeded generator; same spec+seed -> identical state_dict; default dtype + global RNG + filesystem unchanged)"
    requirement: "NET-01 AC #3 / edge R1"
    verification:
      - kind: unit
        ref: "tests/phase38/test_network_structure.py#DeterminismAndSideEffectsTests (5 cases) — green"
        status: pass
    human_judgment: false
  - id: N4
    description: "Both-precision forward through the SAME code path: forward(tau_ic13, masses) returns shape (..., 9) under fp64-CPU and fp32-MPS"
    requirement: "NET-01 AC #2"
    verification:
      - kind: unit
        ref: "tests/phase38/test_network_structure.py#ForwardPrecisionTests (3 cases) — green (MPS arm runs on this host)"
        status: pass
    human_judgment: false
  - id: C1
    description: "Hard mass-weighted COM projection: zero-COM (abs(COM) < 1e-10 fp64 / < 1e-4 fp32), idempotent, equal-vs-UNEQUAL-mass behavior, batched + per-sample masses, both precisions"
    requirement: "NET-02"
    verification:
      - kind: unit
        ref: "tests/phase38/test_com_projection.py#ProjectComCoreTests (9 cases) — green"
        status: pass
    human_judgment: false
  - id: C2
    description: "Projected-only public output: forward == project_com(raw, masses); raw reachable only via private _forward_unprojected; unequal-mass forward proves mass-weighting reaches the projection inside forward"
    requirement: "NET-02 / CTX-21"
    verification:
      - kind: unit
        ref: "tests/phase38/test_com_projection.py#ForwardProjectionContractTests (3 cases) — green"
        status: pass
    human_judgment: false

duration: ~12min
completed: 2026-07-13
status: complete
---

# Phase 38 Plan 02: SQR-SkipResNet-SIREN Network + COM Projection Head Summary

**Wave-2 model core landed: a spec-faithful SQR-SkipResNet-SIREN backbone instantiated from an ArchitectureSpec, with a hard mass-weighted COM projection head wired so projected positions are the model's only public output.**

## Performance

- **Duration:** ~12 min
- **Tasks:** 3 (38-02-01 RED tests; 38-02-02 com_projection; 38-02-03 network + __init__)
- **Files:** 4 created + 1 modified + this SUMMARY

## Accomplishments

- **`pinn/network.py`:** `SQRSkipResNetSIREN(nn.Module)` + factory `build_network(spec, *, dtype, device)`. Topology from `ArchitectureSpec`: input SIREN 14->256 (omega_0=30, U[-1/14, 1/14]); 12 hidden 256->256 (omega_0=1, U[-sqrt(6/256), +sqrt(6/256)]), odd-numbered (1,3,...,11) are `_OddSkipBlock` doing `siren(x_prev) + LayerNorm(x_prev)**2` with `LayerNorm(256, elementwise_affine=False, eps=1e-5)`, even-numbered (2,4,...,12) are plain `_SIRENLayer`; output `_LinearHead` 256->9 linear. `_SIRENLayer` builds raw `nn.Parameter` weight/bias on (dtype, device) filled by `uniform_(generator=<local>)` — no global RNG touch. `forward(tau_ic13, masses)` applies `project_com` and returns ONLY the projected positions; the raw 9-dim tensor is exposed solely via private `_forward_unprojected`.
- **`pinn/com_projection.py`:** pure `project_com(positions, masses, *, dtype, device)` — reshapes 9->(3,3), computes `com = sum(m_i r_i)/sum(m_i)` with mass tensors on (dtype, device), subtracts from every body, flattens. Idempotent by construction. Supports single (9,), batched (N,9), shared (3,) and per-sample (N,3) masses. No Python-float x tensor.
- **`pinn/__init__.py`:** re-exports `ArchitectureSpec`, `build_network`, `SQRSkipResNetSIREN` (plus the Phase 37 `RuntimeSpec`/`resolve_runtime`); docstring updated to note Phase 38 adds the model modules.
- **Tests:** 38 cases green under `pinn-train` (26 network-structure + 12 com-projection). Per-symbol deferred-import SkipTest guards mean both suites SKIP cleanly before the modules exist; the project_com-only tests turn green at 38-02-02, the network-dependent structural tests at 38-02-03.

## Verification

```bash
source <home>/miniforge3/etc/profile.d/conda.sh
conda run -n pinn-train python -m unittest tests.phase38.test_network_structure tests.phase38.test_com_projection -v
# Ran 38 tests — OK (0 errors, 0 failures, 0 skipped after both modules land)
conda run -n pinn-train python -c "import pinn.network, pinn.com_projection; import torch; print('default dtype unchanged:', torch.get_default_dtype())"
# default dtype unchanged: torch.float32
```

- Regression: `tests.phase37.test_runtime tests.phase38.test_constants tests.phase38.test_architecture_spec` still green (33 tests) — the `pinn/__init__.py` re-export change is import-safe for prior waves.
- Framework specs `ctl_instruction.md` / `pinn_architecture.md` byte-identical to HEAD (`git diff --stat` empty) — untouched, no spec edits.
- SIREN init is provably UNIFORM: first-layer pooled var 0.001700 vs uniform `b^2/3` 0.001701; hidden-layer pooled var 0.007814 vs 0.007812; max-abs reaches the bound in both (0.07142/0.07143 and 0.15309/0.15309). No Kaiming/Xavier normal substitute could match.
- `hidden_layers` layout: alternating `_OddSkipBlock`, `_SIRENLayer` (x6 each) = 12 total.
- `torch.get_default_dtype()` unchanged (float32) and global CPU RNG unchanged after build (asserted by `test_build_does_not_mutate_global_default_dtype` / `test_build_does_not_mutate_global_rng`).

## Self-Check: Requirements Coverage

| Requirement | Status | Evidence |
|-------------|--------|----------|
| NET-01 (spec-faithful backbone from ArchitectureSpec, both-precision, deterministic) | Met | topology + init + determinism + both-precision suites green |
| NET-02 (hard COM projection; projected-only public output) | Met | project_com suite + forward-projection structural tests green |

## Deviations from Plan

None for production scope. Process notes:

- **Commit-interface adaptation (process, not a plan deviation):** the orchestrator's suggested `scripts/agent-commit --type feat --scope 38-02` form is incompatible with this repo's `scripts/agent-commit` (which forwards all args to `git commit`; git commit rejects `--type/--scope`). Adapted to the actual interface: `bash scripts/agent-commit -m "feat(38-02): ..." -m "<body>"`. The commit-msg validator accepts scope `38-02` (`^\d{2}-\d{2}$`), the body is required (multi-file + `.planning/`), and the agent trailer is auto-appended.
- **Single atomic commit (process, not a plan deviation):** per the orchestrator's concurrent-agent commit discipline (one lock acquisition in a shared worktree), RED tests + GREEN implementation landed in one `feat(38-02)` commit rather than separate `test(...)` / `feat(...)` commits. The TDD ordering was honored at the code-authoring level (tests authored and verified to SKIP first, then com_projection, then network).
- **Spec-silent mechanical choices (documented as key-decisions, not STOP gaps):** bias init bound (= its layer's weight bound) and output-linear-head init bound (PyTorch default fan-in, seeded) are not specified by `pinn_architecture.md`. Both are well-established SIREN/Linear conventions within planner discretion (CTX-15/16), not physics adjudications — documented above rather than surfaced as STOP-protocol gaps. No spec defect was found; the locked spec was explicit on every semantic choice (topology, init weight bounds, skip update, COM head).

## Next Phase Readiness

- Wave 3 (38-03 residual) can consume `model.forward(tau_ic13, masses)` and differentiate the PROJECTED output; the raw 9-dim tensor is deliberately not public.
- Wave 4 (38-04 probes) can `build_network(ArchitectureSpec(), dtype=..., device=...)` under both `resolve_runtime` branches and run forward through the same code path.
- Wave 5 (38-05 loss catalog) consumes projected positions only — the NET-02 boundary is structural, so no loss/metric can accidentally consume the unprojected output.
- Wave 6 (38-06 overfit smoke) conditions on a fixed placeholder IC13 (the model imposes no IC13 normalization contract); the AST no-v1.3-import and no-precision-default checks will pass (the source-inspection tests already encode them).

## Self-Check: PASSED

- All six created/modified files verified present on disk (`pinn/network.py`, `pinn/com_projection.py`, `pinn/__init__.py`, `tests/phase38/test_network_structure.py`, `tests/phase38/test_com_projection.py`, this SUMMARY).
- No executable-code imports of v1.3-era modules (`basic_architecture`, `data-processing-pipeline-full`, `data-handling`) — the AST source-inspection test strips docstrings/comments and passed; the only textual mentions are in module docstrings documenting the CTX-17 ban.
- No executable-code `torch.set_default_dtype` / `is_available` / retry in either module — the AST source-inspection test passed; textual mentions are docstring prose stating the impl does NOT use them.
- Both suites green on a fresh re-run: `Ran 38 tests in 1.806s — OK`.
- The single atomic commit hash for this plan is recorded in the completion report returned to the orchestrator (per the concurrent-agent one-commit discipline).
