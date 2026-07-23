# Phase 38: PINN Model Rebuild from Specs (FUT-01) - Pattern Map

**Mapped:** 2026-07-12
**Files analyzed:** 10 new source files + 1 test package + 1 evidence tree (no RESEARCH.md; file list from 38-CONTEXT.md CTX-15..32 and 38-SPEC.md NET-01..05)
**Analogs found:** 9 / 10 (fixture loader has no in-repo analog — spec-derived, provenance pattern only)

> **Governance constraint (38-SPEC.md Prohibitions, CTX-17):** The v1.3-era files
> `pinn/basic_architecture.py`, `pinn/data-processing-pipeline-full.py`, and
> `pinn/data-handling/` are reference-only and **BANNED as pattern/analog sources**.
> No excerpt in this document is drawn from them. Every analog below is Phase 37
> substrate (`pinn/runtime.py`, `pinn/verification/componentwise_ad.py`,
> `scripts/run_precision_probe.py`, `tests/phase37/`, the Phase 37 evidence tree).
> Model/loss/residual *content* is spec-derived from `pinn_architecture.md` /
> `ctl_instruction.md`; the analogs supply only *structure* (dataclass shape, CLI
> shape, evidence discipline, test organization), never physics.

## File Classification

Exact filenames are planner discretion (CTX-15/16); the role/flow/analog assignment is fixed.

| New file (indicative name) | Role | Data Flow | Closest Analog | Match Quality |
|----------------------------|------|-----------|----------------|---------------|
| `pinn/architecture_spec.py` (frozen config dataclass, NET-01) | config | transform | `pinn/runtime.py` (`RuntimeSpec`) | exact (frozen validated dataclass) |
| `pinn/constants.py` (locked science constants, CTX-15/30) | config | (static data) | `pinn/runtime.py` module-level constants (`_ALLOWED_PROFILES`, `AGGREGATE_CRITERION` in `componentwise_ad.py`) | role-match |
| `pinn/network.py` (SQR-SkipResNet-SIREN, NET-01) | model | transform (forward pass) | no exact model analog; construction/dtype-device seam from `pinn/runtime.py` + `compute_derivative` explicit-dtype pattern | partial (structure only; content spec-derived) |
| `pinn/com_projection.py` (mass-weighted COM head, NET-02) | model | transform (pure function) | `componentwise_ad.py` pure-function + explicit dtype/device pattern (`synthetic_trajectory`) | role-match (pure transform) |
| `pinn/physics_residual.py` (PHYS-02 autograd, NET-03) | service | transform (autograd) | `componentwise_ad.py` (`_full_jacobian`/`_scalar_u_jvp`, `torch.func`, explicit leaf on resolved dtype/device) | exact (AD kernel discipline) |
| `pinn/loss_catalog.py` (five-term catalog + composer, NET-04) | service | transform (reduce) | `componentwise_ad.py` result-dict pattern (`compute_derivative` return); `RuntimeSpec` for the frozen weights container | role-match |
| `pinn/verification/fixture_loader.py` (probe-local Brutus loader, CTX-25) | utility | file-I/O (read-only) | **none in repo** (data files absent from worktree); provenance/hash pattern from `run_precision_probe.py` `_sha256_file` | no-analog (structure only) |
| `pinn/verification/gradcheck_probe.py` (rung 2, NET-03) | test/probe | request-response (CLI→exit) | `componentwise_ad.py` `main()` argparse + `run_precision_probe.py` evidence write | exact |
| `pinn/verification/residual_probe.py` (rung 3, NET-03) | test/probe | request-response (CLI→exit) | `componentwise_ad.py` `main()` + `run_precision_probe.py` `write_evidence_run` | exact |
| `pinn/verification/overfit_probe.py` (rung 4, NET-05) | test/probe | request-response (CLI→exit) | `componentwise_ad.py` `main()` + `run_precision_probe.py` evidence + threshold/measured recording | exact |
| `tests/phase38/*` (per-module tests, CTX-31) | test | request-response | `tests/phase37/test_runtime.py`, `tests/phase37/test_componentwise_ad.py` | exact |

## Pattern Assignments

### `pinn/architecture_spec.py` — frozen config dataclass (config, transform)

**Analog:** `pinn/runtime.py` (`RuntimeSpec`). CTX-18 explicitly names the `RuntimeSpec`
pattern: a frozen typed dataclass, validated at construction, spec-locked values as
validated defaults.

**Frozen-dataclass shape** (`pinn/runtime.py:23-38`):
```python
@dataclass(frozen=True)
class RuntimeSpec:
    """An immutable resolved precision + device specification."""
    precision: str
    requested_device: str
    dtype: torch.dtype
    torch_device: torch.device
```
Apply to the architecture block: fields for input/output dims, hidden depth/width,
`first_omega_0`/`hidden_omega_0`, LayerNorm placement + `elementwise_affine`, skip
configuration, seed (CTX-18). Spec-locked defaults come from `pinn/constants.py`.

**Fail-closed validation-at-construction discipline** (`pinn/runtime.py:84-95`): the
resolver raises `ValueError` before any tensor is built, naming the permitted values so
the caller can recover. The architecture dataclass validates its fields at construction
the same way (raise on out-of-contract topology, not silent coercion).

**CTX-20 constraint (critical):** precision/device are NOT fields of this dataclass. They
flow only through `resolve_runtime`; the model constructor accepts resolved `dtype`/`device`
explicitly (see network pattern). No precision default anywhere (CTX-14 persists).

---

### `pinn/constants.py` — locked science constants (config, static data)

**Analog:** module-level named-constant discipline in `componentwise_ad.py:113-118`
(`AGGREGATE_CRITERION = 1e-6`, pattern IDs) and `pinn/runtime.py:44-62` (the
`_ALLOWED_PROFILES` table + `_ALLOWED_PAIR_DESCRIPTION`).

**Pattern:** each constant is a named module-level value with a docstring/comment citing
its spec section (CTX-15 requires per-constant spec citation). Locked values to carry:
raw-mass `D ≈ 4.6416`, `eps_soft = 1e-5`, SIREN `first_omega_0=30.0` / `hidden_omega_0=1.0`,
Huber `δ_r = 1` / `δ = 1.0`, `t_τ ∈ [-1,1]`, `r′ = r/D`. Cite `pinn_architecture.md` §2.3/§2.4/§3/§4.1/§5.3.1 and `ctl_instruction.md` loss contract inline. Tested against spec formulas (CTX-30).

---

### `pinn/network.py` — SQR-SkipResNet-SIREN backbone (model, transform)

**Analog:** no in-repo model exists (the only prior model is the BANNED v1.3
`basic_architecture.py`). Structure/wiring discipline is borrowed; all topology content is
spec-derived from `pinn_architecture.md` §2.3/§2.4 (14→256 input, 12×256 hidden, 256→9
output, SIREN ω, LayerNorm `elementwise_affine=False` on odd layers, skip connections).

**Explicit-dtype/device construction seam** (from `componentwise_ad.py:196-199`, the
one legal way to build tensors on the resolved runtime):
```python
spec = _resolve_runtime(precision, device)  # raises on unsupported pair
predicted = impl(u_val, spec.dtype, spec.torch_device)
```
The model constructor takes the resolved `dtype`/`device` (or a `RuntimeSpec`) explicitly
and builds every parameter on them — no `.to()` afterthought, no default-dtype mutation,
no availability probe (mirrors `pinn/runtime.py:73-79` prohibitions). Deterministic seeded
init + no filesystem/global-state writes satisfies SPEC AC #3.

**NET-02 wiring (CTX-21):** `forward()` returns projected positions as the ONLY public
output; the raw 9-dim tensor is reachable solely via an explicitly named internal/test hook.
Make "no loss/metric consumes unprojected output" a structural property, not a convention.

---

### `pinn/com_projection.py` — mass-weighted COM head (model, pure transform)

**Analog:** `componentwise_ad.py` pure-function-with-explicit-dtype pattern
(`synthetic_trajectory`, lines 62-76) — constants wrapped as same-dtype/device tensors, no
Python-float × tensor on MPS:
```python
two_pi = _torch.as_tensor(2 * _math.pi, dtype=u.dtype, device=u.device)
```
Apply: the projection subtracts `Σ mᵢ·rᵢ / Σ mᵢ` using mass tensors on the input's
dtype/device. It is a pure, idempotent function (SPEC AC #4: `Σ mᵢ·rᵢ′ = 0`, double-projection
is a fixed point). No module-level dtype assumption.

---

### `pinn/physics_residual.py` — PHYS-02 autograd residuals (service, autograd transform)

**Analog:** `componentwise_ad.py` — the repo's canonical autograd kernel. This is the
strongest structural match in the phase.

**Autograd-on-explicit-leaf pattern** (`componentwise_ad.py:128-157`):
```python
def _full_jacobian(u_scalar, dtype, device):
    def f(leaf):
        return synthetic_trajectory(leaf)
    u_leaf = _torch.tensor(float(u_scalar), dtype=dtype, device=device,
                           requires_grad=True)
    jac = _torch.func.jacrev(f)(u_leaf)
    return jac
```
Apply to PHYS-02: the leaf is `u` (autograd leaf, `τ = 2u−1`); componentwise second
derivatives w.r.t. `u`, with the spec chain-rule factors `d²r′/du² = 4·d²r′/dτ²`,
`dr′/du = 2·dr′/dτ` and PHYS-03 softening `eps_soft = 1e-5` (from `pinn/constants.py`).
Consumes the projected output of NET-02.

**Non-finite refusal** (`componentwise_ad.py:193-206`): raise on non-finite components
("refusing to produce evidence") rather than emitting a passing record. The residual
module inherits this fail-loud discipline (relevant to SPEC edge R3, softening-active points).

**gradcheck contract:** `torch.autograd.gradcheck` runs under the fp64-CPU arm by contract
(SPEC AC, CTX-22); the residual code path is dtype/device-agnostic so the same code passes
gradcheck (fp64-CPU) and runs in production (fp32-MPS).

---

### `pinn/loss_catalog.py` — five-term catalog + composer (service, reduce)

**Analog:** `componentwise_ad.py` `compute_derivative` result-dict pattern (lines 215-229)
for the per-term + total result container; `RuntimeSpec` (frozen dataclass) for the
**supplied** five-field frozen weights container (CTX-28: named fields, not positional).

**Result-container pattern** (`componentwise_ad.py:215-229`): return a dict/dataclass
carrying each named quantity plus the aggregate. Apply to the composer (CTX-29): return
per-term scalars alongside the weighted total so Phase 42 OPS-03 logging (5 terms + total +
λ vector) consumes it without refactor.

**Five terms (CTX-28, spec-derived):** data Huber (`δ_r = 1`), IC squared-error anchors,
causally-weighted physics residual (D-04 Option A), soft-energy Huber (`δ = 1.0`),
componentwise angular-momentum Huber (`δ = 1.0`). All δ/`D`/`t_τ` values from
`pinn/constants.py`, tested against spec formulas (CTX-30). Composer takes a supplied λ
vector (frozen named container); the PHYS-05 scheduler that produces it is Phase 40.

---

### `pinn/verification/fixture_loader.py` — probe-local Brutus loader (utility, read-only file-I/O)

**Analog:** NONE in repo. The v1.3 data-handling parsers are BANNED (CTX-17); the on-disk
`simulation_data/` trajectory payloads are absent from this worktree (excluded bulk data),
so there is no code or data analog to copy. Build spec-derived, minimal.

**Provenance/hash pattern to reuse** (`scripts/run_precision_probe.py:109-113`):
```python
def _sha256_file(path):
    h = hashlib.sha256()
    ...
```
CTX-26 requires each probe to record provenance in evidence: variant, ID, resolved path,
file hash. Reuse `_sha256_file`-style hashing for the file hash.

**Constraints:** parses exactly one Brutus trajectory (+ its IC/masses) into tensors on an
explicitly passed dtype/device (CTX-25). No Step-1A gate, no splits, no batching, no
`data_version_hash`. Trajectory supplied at invocation (path or variant+ID), never
hardcoded, no absolute paths (CTX-26). `simulation_data/` strictly read-only (CTX-27).
The planner picks + documents a default known-good admitted trajectory.

---

### `pinn/verification/{gradcheck,residual,overfit}_probe.py` — rungs 2–4 (test/probe, request-response)

**Analog:** `componentwise_ad.py` `main()` CLI + `scripts/run_precision_probe.py` evidence
writer. All three rungs share this grammar (the phase requires visible symmetry with the
Phase 37 probe — CTX-22/23/24).

**argparse CLI with required explicit precision/device** (`componentwise_ad.py:371-382`):
```python
parser.add_argument("--precision", required=True, choices=("float32", "float64"))
parser.add_argument("--device", required=True, choices=("mps", "cpu"))
```
CTX-22: no module encodes a precision default; the gradcheck rung documents+enforces its
fp64-CPU contract but still selects the arm explicitly.

**PASS/FAIL via exit code with numeric criterion printed** (`componentwise_ad.py:383-394`
for the JSON-on-stdout + `_sys.exit` discipline; the `passed` field at line 228). CTX-24:
exit PASS/FAIL through exit codes with the numeric criterion printed. Rung 3 records
residual threshold + measured residuals; rung 4 records initial loss / achieved floor /
reduction ratio (≥ 10³× for PASS, SPEC AC).

**MPS-fallback discipline** (`componentwise_ad.py:30-41`): capture
`PYTORCH_ENABLE_MPS_FALLBACK` BEFORE importing torch; any invocation certifying MPS
behavior runs with the key unset (CTX-24, SCOPE-20). Record the pre-import fallback fact in
evidence.

**Non-overwriting timestamped evidence** (`run_precision_probe.py:390-416`):
```python
run_id = _dt.datetime.now(_dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
run_dir = evidence_root / run_id
run_dir.mkdir(parents=True, exist_ok=False)   # exclusive; never overwrite
raw_json = json.dumps(raw, sort_keys=True, indent=2) + "\n"
```
Write JSON + owner-readable Markdown summary together (CTX-23). Target layout:
`.planning/phases/38-pinn-model-rebuild-from-specs-fut-01/evidence/<rung>/<UTC>/` with
`raw.json` + `summary.md` (mirrors Phase 37's `evidence/precision/<UTC>/{raw.json,summary.md}`).

---

### `tests/phase38/*` — per-module tests (test, request-response)

**Analog:** `tests/phase37/test_runtime.py` and `tests/phase37/test_componentwise_ad.py`.
Mirror exactly (CTX-31): pytest/unittest, per-module test files, no new framework.

**Deferred-import skip guard** (`test_runtime.py:14-42`): import the production module
inside test methods; `SkipTest` if not yet implemented, so module compilation is the only
pre-implementation green condition.

**Frozen-dataclass assertion** (`test_runtime.py:66-73`):
```python
with self.assertRaises((AttributeError, TypeError)):
    spec.dtype = "x"
```
Reuse for the architecture-spec dataclass immutability test.

**Source-inspection prohibition test** (`test_runtime.py:139-183`): AST-parse the module,
strip docstrings/comments, assert executable code does NOT contain `torch.set_default_dtype`
/ `is_available` / `retry`. Reuse this exact technique for CTX-32's mechanical checks:
(a) no `pinn/` module hard-codes precision/device, and (b) no import of the v1.3 files.

**Test files to create (CTX-31):** structure/topology test (asserts 14→256, 12×256, 256→9,
`first_omega_0=30.0`, `hidden_omega_0=1.0`, LayerNorm `elementwise_affine=False` on odd
layers vs `pinn_architecture.md` §2.3/§2.4); deterministic-seeded-instantiation +
no-side-effects test; projection tests (zero-COM, idempotence, no-unprojected-consumption);
residual/gradcheck tests; per-term loss tests (δ values, causal weighting, dimensionless
conversions); probe-contract tests.

## Shared Patterns

### Explicit precision/device seam (applies to ALL new source files)
**Source:** `pinn/runtime.py:65-95` (`resolve_runtime`). Consume, never re-implement or
default around (CTX-20, ENV-04). Every module accepts resolved `dtype`/`device` explicitly;
no module calls `torch.set_default_dtype`, probes availability, or encodes a precision default.

### Frozen validated dataclass (architecture spec, loss-weights container)
**Source:** `pinn/runtime.py:23-38` + fail-closed validation `pinn/runtime.py:84-95`.
**Apply to:** `architecture_spec.py`, the five-field loss-weights container in `loss_catalog.py`.

### Autograd on an explicit leaf via `torch.func`
**Source:** `componentwise_ad.py:128-157`. **Apply to:** `physics_residual.py`, gradcheck rung.
Same-dtype/device tensor constants (`_torch.as_tensor(..., dtype=u.dtype, device=u.device)`),
never Python-float × tensor on MPS (`componentwise_ad.py:73-76`).

### Probe CLI + non-overwriting timestamped evidence
**Source:** `componentwise_ad.py:371-394` (argparse, required `--precision`/`--device`,
JSON-on-stdout, `_sys.exit`) + `run_precision_probe.py:109-113,390-416` (`_sha256_file`,
UTC `run_id`, `mkdir(exist_ok=False)`, `json.dumps(..., sort_keys=True, indent=2)`, JSON+MD pair).
**Apply to:** all three rung probes; evidence under
`38-.../evidence/<rung>/<UTC>/{raw.json,summary.md}`.

### MPS-fallback capture discipline
**Source:** `componentwise_ad.py:30-41`. **Apply to:** every probe that certifies MPS
behavior — capture `PYTORCH_ENABLE_MPS_FALLBACK` before torch import; run with it unset;
record the fact (SCOPE-20, CTX-24).

### AST source-inspection prohibition check
**Source:** `test_runtime.py:139-183`. **Apply to:** CTX-32 mechanical checks (no hardcoded
precision/device; no import of the banned v1.3 files) and the framework-spec byte-identity
check.

## No Analog Found

| File | Role | Data Flow | Reason |
|------|------|-----------|--------|
| `pinn/verification/fixture_loader.py` | utility | read-only file-I/O | Only prior Brutus parser is the BANNED v1.3 `pinn/data-handling/` (CTX-17); on-disk trajectory payloads are absent from this worktree. Build spec-derived + minimal; reuse only the `_sha256_file` provenance pattern from `run_precision_probe.py`. Planner must document the default example trajectory + Brutus file format from `simulation_data/Documentation/README.md`. |
| `pinn/network.py` | model | transform | No spec-faithful model exists; v1.3 `basic_architecture.py` is BANNED. Topology is spec-derived (`pinn_architecture.md` §2.3/§2.4); only the explicit-dtype construction seam is borrowed. |

## Metadata

**Analog search scope:** `pinn/`, `pinn/verification/`, `tests/phase37/`, `scripts/`,
`.planning/phases/37-*/evidence/`, `simulation_data/` (data absent).
**Files scanned:** `pinn/runtime.py` (95 lines, full), `pinn/verification/componentwise_ad.py`
(398 lines, full), `tests/phase37/test_runtime.py` (188 lines, full),
`tests/phase37/test_componentwise_ad.py` (head), `scripts/run_precision_probe.py` (grep-targeted),
Phase 37 evidence tree + `summary.md` (head).
**Banned from analog set (governance):** `pinn/basic_architecture.py`,
`pinn/data-processing-pipeline-full.py`, `pinn/data-handling/` — not read, not excerpted.
**Pattern extraction date:** 2026-07-12
