# Phase 67: Design & Settings Ladders - Pattern Map

**Mapped:** 2026-11-01. **Files classified:** 13 proposed implementation/test files. **Analogs:** 13/13 have structural matches; two new scientific algorithms have no exact implementation.

Scope follows `67-CONTEXT.md:133-157` and `67-RESEARCH.md:213-245`. Names below are proposed where files do not exist. Reuse current tracked code, not stale codebase maps. This map performs no corpus access, timing or training.

## File Classification

| New/modified file | Role | Data flow | Closest tracked analog | Match |
|---|---|---|---|---|
| `pinn/verification/diagnostic_phase67.py` | service | batch, file-I/O | `pinn/verification/diagnostic_phase66.py` | role-match |
| `pinn/verification/diagnostic_time_features.py` | model | transform | `pinn/network.py` | role-match |
| `pinn/verification/diagnostic_variants.py` | config | transform | same file | exact extension |
| `pinn/verification/diagnostic_fit.py` | service | batch, file-I/O | same file | exact extension |
| `pinn/verification/diagnostic_similarity.py` | utility | transform | same file | exact extension |
| `tests/phase67/__init__.py` | config | transform | `tests/phase66/__init__.py` | exact |
| `tests/phase67/_fixtures.py` | utility | file-I/O | `tests/phase66/test_tracer.py` | role-match |
| `tests/phase67/test_catalog.py` | test | transform | `tests/phase66/test_catalog.py` | exact |
| `tests/phase67/test_budget.py` | test | transform | `tests/phase66/test_budget.py` | exact |
| `tests/phase67/test_time_features.py` | test | transform | `tests/phase66/test_catalog.py` | role-match |
| `tests/phase67/test_windows.py` | test | transform | `tests/phase65/test_fit_short.py` | role-match |
| `tests/phase67/test_records.py` | test | file-I/O | `tests/phase66/test_records.py` | role-match |
| `tests/phase67/test_isolation.py` | test | file-I/O | `tests/phase65/test_isolation.py` | exact |

Predictions, registrations and eventual exclusive evidence belong under this phase directory. Their concrete filenames follow the planner's experiment decomposition. `diagnostic_data.py`, `stage0_census.py`, `two_kepler.py`, the scorer, production network and historical Phase 65/66 files are reuse references, not proposed edit targets.

## Pattern Assignments

### `pinn/verification/diagnostic_phase67.py`

Copy the lightweight import direction and fresh immutable catalog from `diagnostic_phase66.py:37-41,82-100`. Keep the catalog independent of fit/data/power imports, as checked by `tests/phase66/test_catalog.py:100-120`.

```python
from pinn.verification.diagnostic_variants import (
    REGISTRY,
    DiagnosticVariant,
    register_variant,
)
```

Use the cost-only pure function structure in `diagnostic_phase66.py:386-511`. Its current projection is at lines 439-445:

```python
    def projected_wall(steps):
        return (
            fixed_wall
            + warmup_seconds
            + (steps - warmup_steps) * seconds_per_step * (1.0 + margin)
            + len(exp01_cadence(steps)) * logging_per_entry
        )
```

Replace EXP-01 cadence/constants with Phase 67's registered policy. Include scoring/comparison/write overhead and select a common update count that fits every arm and repeat. Keep scientific scores out of budget selection. Reuse reader separation at `diagnostic_phase66.py:589-604,760-777,823-839`, but validate shapes before dereferencing, finite numbers excluding booleans, exact registered identity/settings/window, all expected layers, digests and same-window baselines. Do not copy its two-orbit `E_CONST_PREDICTED` lookup or fixed `["input", "h1"]` rows at lines 640-658.

Keep the signed-lap helper here initially. Copy `stage0_census.py:135-138`:

```python
    cross = np.cross(stacked[:-1], stacked[1:])
    triple = cross @ np.asarray(normal, dtype=np.float64).reshape(3)
    dots = np.sum(stacked[:-1] * stacked[1:], axis=1)
    return np.arctan2(triple, dots)
```

Reuse its initial normal and ordered inner-pair separation at lines 112-128,160-181. Extend signed steps to cumulative turns and first EXISTING gold-sample crossing, with preceding/current bracket evidence, nonfinite/unreached/step-guard refusals. Do not copy the census `_window` tolerance at lines 149-157. Apply `diagnostic_data.physical_window` instead, whose exact inclusive mask is at `diagnostic_data.py:446-459`; preserve global tau at lines 550-556. Reuse fit `_comparison_rows` at `diagnostic_fit.py:699-775`, including explicit formula nonapplicability.

### `pinn/verification/diagnostic_time_features.py`

`pinn/network.py:160-196` constructs the current layer types and exposes `input_layer`/`hidden_layers` for hooks. Its internal forward core at lines 205-208 is:

```python
        x = self.input_layer(tau_ic13)
        for layer in self.hidden_layers:
            x = layer(x)
        return self.output_layer(x)
```

Keep the public raw `forward(tau_ic13, masses)` signature and COM projection at lines 210-228. Transform only inside the diagnostic model, with differentiable tensor operations and persistent frequency buffers. Follow `67-RESEARCH.md:201-207,229-231` for the new Fourier algorithm; no existing feature encoder supplies it. Reuse current fan-in initialization at `network.py:74-92`, including its changed bound for 16/18 internal inputs. Preserve raw input and IC13, ordered masses, dtype/device, seeded construction and observable layers. Do not change `ArchitectureSpec` or the frozen scorer.

### `pinn/verification/diagnostic_variants.py`

Extend explicit declarations at lines 52-56 and validation at lines 86-118. Keep boolean exclusion, finite positive values and exact JSON fields at lines 120-132. Preserve `register_variant` copy-on-registration at lines 176-195. The existing local-seed construction at lines 213-223 is:

```python
    resolved = resolve_variant(variant)
    fields = dataclasses.asdict(ArchitectureSpec(seed=int(seed)))
    fields["hidden_depth"] = int(resolved.depth)
    fields["hidden_width"] = int(resolved.width)
    fields["first_omega_0"] = float(resolved.first_omega_0)
    fields["hidden_omega_0"] = float(resolved.hidden_omega_0)
    generator = torch.Generator(device=device)
    generator.manual_seed(int(seed))
```

Dispatch feature variants to the diagnostic model while retaining bitwise raw locked construction. Pin frequency/feature identity in new registration metadata rather than changing historical declarations.

### `pinn/verification/diagnostic_fit.py`

Extend `_named_registry` at lines 317-330 with Phase 67 dispatch while keeping the current default and Phase 66 table intact. Reuse `log_similarity` at lines 244-262; add Phase 67 checkpoint scores through the same frozen `score_network` call at lines 957-968. Keep checkpoint overhead inside the deadline and outside optimizer-step timing. Admission/settings precede construction at lines 821-856; existing evidence refuses replacement at lines 865-870. Committed registration checks are at lines 608-648. New dependency digests belong in new registrations.

### `pinn/verification/diagnostic_similarity.py`

Reuse hook capture and `finally` cleanup at lines 199-215. The centred adjacent-time measurement at lines 218-222 is:

```python
    for order, name, activation in sorted(captured, key=lambda item: item[0]):
        centered = activation - activation.mean(dim=0, keepdim=True)
        adjacent = F.cosine_similarity(centered[:-1], centered[1:], dim=1).mean()
        rows.append(LayerRow(name=name, order=order,
                             adjacent_cosine_mean=_finite_float(adjacent, f"{name} cosine")))
```

Preserve all layer rows and actual physical/raw tau coordinates. Column-zero bandwidth at lines 224-227 applies to raw input only. Encoded variants need explicit nonapplicability plus registered feature-frequency metadata. Apply the affected-use tau-monotonicity condition from `65-CLOSEOUT.md:77`; preserve historical raw record shapes.

### Synthetic tests and fixtures

Use standard-library `unittest`, explicit CPU float64 tensors, temporary fixture repositories and injected clocks/power/readers. `tests/phase66/test_tracer.py:72-92` patches both fit and data modules; lines 81-88 show the pattern:

```python
    for module in (fit_module, diagnostic_data):
        stack.enter_context(mock.patch.object(
            module, "open_diagnostic_context", create=True,
            return_value=context,
        ))
        stack.enter_context(mock.patch.object(
            module, "load_diagnostic_data", create=True, return_value=data,
        ))
```

- `_fixtures.py`: adapt that seam, `phase66_fixture_registration` at tracer lines 65-69, and `_loaded` at `tests/phase65/test_fit_short.py:80-94`. Avoid running MPS or real corpus operations in unit tests.
- `test_catalog.py`: copy sealed-catalog/duplicate tests from `tests/phase66/test_catalog.py:38-64` and parameter-count/production-lock tests at lines 76-91. `__init__.py` follows the one-line Phase 66 package marker.
- `test_budget.py`: use synthetic `_timing_record` from `tests/phase66/test_budget.py:29-61`; vary costs across arms/repeats and prove score independence, common updates, cap/quantum/overhead accounting and malformed-input refusal.
- `test_time_features.py`: extend catalog construction assertions with raw14/16/18 dimensions, persistent buffers, analytic first/second derivatives, frozen-scorer differentiation, COM and hook cleanup. These new numerical assertions need purpose-built synthetic inputs.
- `test_windows.py`: adapt independent baseline recomputation from `tests/phase65/test_fit_short.py:258-300`; add signed reversals, crossing brackets, exact inclusion, unreached laps and unchanged tau.
- `test_records.py`: adapt temporary fixture lifecycle from `tests/phase66/test_records.py:38-73`; replace EXP-01 assumptions with all registered shapes and hostile/malformed evidence cases.
- `test_isolation.py`: copy pre-open tripwires and reader/exists refusal assertions from `tests/phase65/test_isolation.py:249-261,467-490`; retain production-entry diagnostic-marker rejection and historical-byte checks.

## Shared Patterns

Reuse committed-registration and TRAIN-only pre-open admission, exclusive evidence publication, AC/weekend launch gating and the frozen scorer. Authentication is inapplicable to this local diagnostic path. `65-CLOSEOUT.md:68-91` and `66-REVIEW.md:48-111` identify affected-use hardening; apply it to new paths without rewriting historical evidence. Keep physics/spec adjudication, production redesign and energy-bar changes outside this phase.

## No Analog Found

No exact implementation exists for internal Fourier time encoding, cumulative signed first-crossing prefixes, or Phase 67's cross-arm budget/reader rules. Use the structural analogs above and the prospective algorithms in `67-RESEARCH.md:199-219`; do not copy EXP-01 scientific constants.

## Metadata

Search scope: current `pinn/verification/`, `pinn/network.py`, `tests/phase65/` and `tests/phase66/`. Fourteen source/test analog or extension files inspected. Every named existing code/test path was verified with `git ls-files -- <path>`. Extraction date: 2026-11-01. Artifact-only validation: check listed tracked paths, fence balance, line count and `git diff --check`; no tests or experiments executed by this mapper.
