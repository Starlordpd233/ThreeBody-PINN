---
phase: 38-pinn-model-rebuild-from-specs-fut-01
plan: "01"
subsystem: pinn
tags: [constants, architecture-spec, net-01, frozen-dataclass, siren, pipe-09]

requires:
  - phase: 37-developer-environment-precision-adjudication
    provides: "pinn-train env + RuntimeSpec frozen/fail-closed pattern + tests/phase37 deferred-import style"
provides:
  - "pinn/constants.py — locked science constants with per-constant framework-spec citations"
  - "pinn/architecture_spec.py — frozen validated ArchitectureSpec (14→256×12→9, SIREN ω from constants)"
  - "tests/phase38/ — foundation unit suites for constants + architecture-spec"
affects:
  - "38-02 (network + COM head) consumes ArchitectureSpec + SIREN/topology constants"
  - "38-03 (residual) and 38-04 (probes) consume D/T/eps_soft from constants"
  - "38-05 (loss catalog) consumes Huber deltas, causal weights, eps_L"

tech-stack:
  added: []
  patterns:
    - "Spec-cited module-level pure-Python floats (no torch, no precision/device)"
    - "RuntimeSpec-style frozen dataclass with fail-closed __post_init__ validation"
    - "SIREN ω defaults sourced from pinn.constants, not fresh literals"

key-files:
  created:
    - "pinn/constants.py"
    - "pinn/architecture_spec.py"
    - "tests/phase38/__init__.py"
    - "tests/phase38/test_constants.py"
    - "tests/phase38/test_architecture_spec.py"
  modified: []

key-decisions:
  - "D_CHARACTERISTIC_LENGTH = 100.0**(1/3) (exact PIPE-09 identity under G=1, T=10) rather than a hard-coded 4.6416 literal; tests assert closeness to 4.6416 within 1e-3 and mutual consistency with T."
  - "T_CHARACTERISTIC_TIME = 10.0 grounded at pinn_architecture.md Table 2 (T = t_max) with dataset horizon t_end = 10; cross-checked by locked D."
  - "ArchitectureSpec validates locked topology (input_dim=14, output_dim=9, depth=12, width=256, power_p=2, elementwise_affine=False, omega from constants) and raises ValueError naming the field; skip_cadence default is the string 'alternating'; seed default is 0."
  - "No precision/device fields on ArchitectureSpec (CTX-20); pinn/__init__.py left unchanged (still only RuntimeSpec/resolve_runtime re-exports)."

patterns-established:
  - "Phase 38 foundation: constants module is the single cited home for science locks; ArchitectureSpec is the config surface network construction will consume"
  - "tests/phase38 mirrors phase37 deferred-import SkipTest guards + frozen-immutability assertions"

requirements-completed: [NET-01]

coverage:
  - id: D1
    description: "Locked science constants module with per-constant framework-spec citations (D≈4.6416, T=10, eps_soft, SIREN ω, Huber deltas, causal weights)"
    requirement: "NET-01"
    verification:
      - kind: unit
        ref: "tests/phase38/test_constants.py#ConstantsTests (11 cases) — green under pinn-train"
        status: pass
    human_judgment: false
  - id: D2
    description: "Frozen validated ArchitectureSpec default topology 14→256×12→9; fail-closed; no precision/device field; SIREN ω from constants"
    requirement: "NET-01"
    verification:
      - kind: unit
        ref: "tests/phase38/test_architecture_spec.py#ArchitectureSpecTests (10 cases) — green under pinn-train"
        status: pass
    human_judgment: false

duration: ~25min
completed: 2026-07-13
status: complete
---

# Phase 38 Plan 01: Foundation Constants + ArchitectureSpec Summary

**Wave-1 substrate landed: one cited constants home and a frozen fail-closed ArchitectureSpec for every later Phase 38 module**

## Performance

- **Duration:** ~25 min
- **Tasks:** 3 (38-01-01 tests; 38-01-02 constants; 38-01-03 architecture-spec)
- **Files created:** 5 production/test files + this SUMMARY

## Accomplishments

- **`pinn/constants.py`:** dtype-agnostic pure-Python floats for locked science values with inline citations to `ctl_instruction.md` §2.5/PIPE-09 and `pinn_architecture.md` Table 2 / §2.2/§2.4/§3.1/§3.2/§3.4/§3.5/§5.3.1. Exports include `D_CHARACTERISTIC_LENGTH` (cbrt(100) ≈ 4.6416), `T_CHARACTERISTIC_TIME` (10.0), `EPS_SOFT` (1e-5), SIREN ω (30.0/1.0), three Huber deltas (1.0), `EPS_L` (1e-8), `CAUSAL_ETA_C`/`CAUSAL_W1` (1.0). No torch import; no precision/device default; mass-fraction D≈6.694 is not selectable.
- **`pinn/architecture_spec.py`:** `@dataclass(frozen=True) ArchitectureSpec` with locked defaults 14/9/12/256, SIREN ω from `pinn.constants`, LayerNorm `elementwise_affine=False` + `eps=1e-5`, `power_p=2`, `skip_cadence="alternating"`, `seed=0`. `__post_init__` raises `ValueError` naming the field on out-of-contract topology. No precision/device attribute (CTX-20).
- **`tests/phase38/`:** stdlib unittest package with deferred-import skip guards (Phase 37 pattern). 21 cases green under `pinn-train` (11 constants + 10 architecture-spec).

## Verification

```bash
source <home>/miniforge3/etc/profile.d/conda.sh
conda run -n pinn-train python -m unittest tests.phase38.test_constants tests.phase38.test_architecture_spec -v
# Ran 21 tests — OK (run twice; both exit 0)
```

- Framework specs `ctl_instruction.md` / `pinn_architecture.md` byte-identical (sha256 unchanged).
- Import probe: locked numerics + frozen raise + out-of-contract `input_dim` naming + no precision/device attrs.
- Watchdog producer announce: tooling present, but this Grok Build harness has no Claude ancestor process / `CLAUDE_CODE_SESSION_ID`; `wd-announce` exited 0 with "liveness unavailable (no Claude ancestor process); no record written" — evidence under implementer scratch `wd-producer.log`. Wave-1 code criteria still gate completion.

## Self-Check: Requirements Coverage

| Requirement | Status | Evidence |
|-------------|--------|----------|
| NET-01 (config-supplied architecture + locked constants substrate) | Met (Wave-1 portion) | constants + ArchitectureSpec + green suites |
| Waves 2–5 (network/residual/probes/loss/AST) | Deferred | Explicitly out of Wave-1 scope |

## Deviations from Plan

- None for production scope. Process note: `wd-announce`/`wd-publish-done` cannot write a full liveness handle in this non-Claude harness; captured honestly rather than simulated.
- `conda` is not on the default PATH in this shell; runs use miniforge (`<home>/miniforge3`) + `conda run -n pinn-train`.

## Next Phase Readiness

- Wave 2 (38-02) can instantiate the network from `ArchitectureSpec()` and import SIREN/topology constants without inventing literals.
- Do not treat Phase 38 as complete; only plan 01 / Wave 1 is closed.
