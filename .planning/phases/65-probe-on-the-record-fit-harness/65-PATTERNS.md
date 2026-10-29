# Phase 65: Probe on the Record & Fit Harness - Pattern Map

**Mapped:** 2026-10-28, America/Chicago
**Files classified:** 14 proposed source paths. **Analogs:** 10/14, comprising 3 exact and 7 role matches.
**Scope:** `65-CONTEXT.md` and `65-RESEARCH.md`. Test names come from research; new implementation names below are proposed layout, not locked decisions. Existing source references remain unchanged unless listed as modified.

## File Classification

All new implementation modules are under `pinn/verification/`; original-source paths are relative to this phase directory.

| New/modified file | Role | Data flow | Closest tracked analog | Quality |
|---|---|---|---|---|
| `diagnostic_variants.py` | model/config | transform | `pinn/verification/diagnostic_architecture.py` | role-match |
| `diagnostic_data.py` | service | file-I/O | `pinn/verification/learnability_data.py` | exact |
| `diagnostic_similarity.py` | utility | transform | No complete analog; layer access in `pinn/network.py` | none |
| `diagnostic_probe.py` | service | batch | `.planning/phases/64-feasibility-verdict/evidence/build_phase64_evidence.py` | role-match |
| `diagnostic_fit.py` | service | batch/file-I/O | `pinn/verification/learnability_run.py` | exact |
| `diagnostic_guard.py` | middleware | file-I/O | No early content-based diagnostic guard | none |
| `pinn/train.py`, modified | controller | request-response | Existing `main` admission ordering | role-match |
| `pinn/evaluate.py`, modified | controller | request-response | Existing `evaluate_run` ownership check | role-match |
| `tests/phase65/test_probe.py` | test | batch/transform | `tests/phase60/test_refusals.py` | role-match |
| `tests/phase65/test_contracts.py` | test | transform | `tests/phase60/test_refusals.py` | role-match |
| `tests/phase65/test_isolation.py` | test | file-I/O | `tests/phase60/test_data_seam.py` | role-match |
| `tests/phase65/test_fit_short.py` | test | batch/file-I/O | `tests/phase60/test_run_short.py` | exact |
| `evidence/original/probe_time_signal.py` | utility/provenance | file-I/O | Preserve supplied source bytes and context hash | none |
| `evidence/original/probe_all_arms.py` | utility/provenance | file-I/O | Preserve supplied source bytes and context hash | none |

Registration pages, extracted stdout, reproduction results and fit records are additional evidence artifacts. Planner names these outputs and freezes their fields before execution; do not treat missing historical deep-layer cells as predictions.

## Pattern Assignments

### 1. Variant registry and network builder

For `diagnostic_variants.py`, copy the isolated constructor in `pinn/verification/diagnostic_architecture.py:51-57`:
```python
fields = dataclasses.asdict(ArchitectureSpec(seed=seed))
fields["first_omega_0"] = omega
generator = torch.Generator(device=device)
generator.manual_seed(int(seed))
return SQRSkipResNetSIREN(
    SimpleNamespace(**fields), dtype=dtype, device=device, generator=generator
)
```
Imports are absolute `from pinn.architecture_spec import ArchitectureSpec` and `from pinn.network import SQRSkipResNetSIREN`, lines 24-25. Adapt the copied fields only inside the new diagnostic module. The constructor in `pinn/network.py:160-196` already consumes input dimension, depth and width; its forward at 226-228 preserves COM projection. Keep `ArchitectureSpec` locked. Copy immutable named-spec validation from `pinn/verification/learnability_arms.py:132-169`; record time features, learning rate and window independently of the sealed arm catalog.

### 2. Training-only Stage-0 reader and frozen statistics

For `diagnostic_data.py`, preserve all-key validation before loading from `pinn/verification/learnability_data.py:234-242`:
```python
for _name, key in assigned:
    if not isinstance(key, RecordKey):
        raise TypeError(f"an arm record must be a RecordKey; got {key!r}")
    context.allowlist.require(key)
```
Strengthen that admission to require both `split == "train"` and `manifest_stage(key) == 0`, before any reader/path operation. These are separate checks. `pinn/verification/split_allowlist.py:188-213` supplies `require` and `manifest_stage`; its current allowed population includes validation, lines 175-177.
The reader's order at `split_allowlist.py:273-275` is `split = self._require(key)`, then `path = self._brutus_path(key)`, then parsing. Apply the stronger guard to ancillary reads, `read`, `exists`, scoring and baseline inputs.
Do not call `open_real_context` at `learnability_data.py:123-166`: it recovers statistics through additional record reads. Hydrate `NormalizationStats` from the tracked `.planning/phases/59-read-only-baseline-scorecard/evidence/audit/reader_acceptance.json:56-92`, then verify `production_reference.stats_digest`, lines 310-323, against `EXPECTED_STATS_SHA256` at `learnability_data.py:69`. Never refit on a permitted subset.
Copy `resident_record` residency/normalization at `pinn/verification/production_reference.py:136-178` and the tensor assembly at `learnability_data.py:262-276`; retain raw masses and distinguish physical time from tau. Window handling is at lines 183-205.

### 3. Shared similarity logger and read-only seven-arm probe

For `diagnostic_probe.py`, copy hash-before-load ordering from `build_phase64_evidence.py:387-391` at the tracked Phase 64 path above:
```python
disk = sha256_file(weights_path)
if disk != recorded.get("sha256"):
    fail(f"weights SHA-256 {disk} != recorded {recorded.get('sha256')} for {arm_id} {state}")
weights = torch.load(weights_path, map_location="cpu", weights_only=True)
```
Its lines 398-407 reconstruct each recorded frequency before loading weights. Copy that ordering, not its legacy data-context acquisition. Select all-arm states from committed `better_state`; single-arm Adam/polish comparisons remain separate. CPU float64 seed-42 reconstruction is distinct from historical MPS float32 initialization.
For `diagnostic_similarity.py`, instrument the existing boundaries in `pinn/network.py:205-208`:
```python
x = self.input_layer(tau_ic13)
for layer in self.hidden_layers:
    x = layer(x)
return self.output_layer(x)
```
Use temporary layer hooks around the actual forward, with cleanup on exceptions. Do not replace the production mathematics. No tracked source currently implements the historical centered-neighbor reduction: derive its exact centering axis, reduction, output variation, tau derivative comparator and frequency measure from the preserved originals. Probe and fit must call one implementation. Original formatters and signed-zero behavior define registered acceptance; never widen cells after measurements.

### 4. Short fit, frozen scoring and diagnostic records

For `diagnostic_fit.py`, reuse `pinn/verification/learnability_losses.py:479-491` directly:
```python
pred = model(data_points.tau_ic13, data_points.masses)
return data_huber_loss(
    pred.reshape(-1, 3, 3),
    data_points.targets.reshape(-1, 3, 3),
    dtype=dtype,
    device=device,
)
```
Copy finite-update checks from `pinn/verification/learnability_run.py:447-499`; use a new diagnostic policy, not `run_arm` or its sealed catalog/budgets. Synchronized timing is at 636-650, using an injected monotonic clock and `wall / steps`. Separate optimizer timing from logging/scoring overhead and record its basis.
Call `score_network` exactly as `learnability_run.py:1081-1093`; the frozen implementation in `pinn/verification/feasibility_scorer.py:438-480` supplies autograd velocities and scoring. Use the frozen `score_trajectory` for comparator score rows, and report physical scores/tier beside loss. Recompute both comparisons on the same orbit/window: `pinn/verification/two_kepler.py:90-127` provides `two_kepler_prediction(r0, v0, masses, inner_pair, dt)`; Phase 64's `constant_predictor_error`, lines 433-446, uses each body's window mean with `position_errors`.
Reuse `save_weights` at `learnability_run.py:349-359` for CPU state and both file/tensor hashes. Its record provenance at 1954-1963 records scorer/scorecard hashes, access attestation and statistics digest.
For record creation, reuse `pinn/verification/learnability_arms.py:443-450`:
```python
destination = Path(path)
evidence_io.reject_evidence_root(destination, data_root=data_root)
raw = evidence_io.canonical_json_bytes(payload)
evidence_io.guard_redaction(raw, data_root=data_root)
destination.parent.mkdir(parents=True, exist_ok=True)
flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
```
The same function fsyncs file/directory and refuses overwrite, lines 450-465. A new record schema must carry variant, runtime, seed, window, steps, cadence, timings, diagnostic identity and access counts. Preserve the old record schema.

### 5. Early production refusal and Phase 65 tests

For `diagnostic_guard.py` plus the two entry-point modifications, copy fail-closed error propagation but add content-based diagnostic rejection before side effects. `pinn/train.py:775-819` performs CLI/config checks before creating the run directory at 861. `pinn/evaluate.py:386-418` checks ownership/config and claims evaluation, then opens the test adapter at 422 before loading weights at 441. Place the diagnostic refusal before manifest/test construction and the claim, preserving existing canonical-frame checks. Ownership or a basename alone cannot reject relocated artifacts.
Use standard-library `unittest`, `ExitStack`, temporary directories and `unittest.mock`, as imported in `tests/phase60/test_refusals.py:13-38`. Its early-refusal spy pattern at 215-230 is:
```python
with mock.patch.object(
    learnability_run, "build_arm_network", side_effect=AssertionError("network built")
) as build, mock.patch.object(
    learnability_run, "load_arm_data", side_effect=AssertionError("data read")
) as read:
```
Adapt spy targets to the new modules. `tests/phase60/test_data_seam.py:60-88` patches all open APIs and asserts zero opens. Add validation, Stage-1, unknown and withheld-key cases; assert no opener/reader call. Process-global access attestation tests use subprocesses, lines 139-247.
The evaluator test at `test_refusals.py:177-184` asserts no evaluation attempt/output; its relocation test at 186-201 covers only the checkpoint store. Extend relocation tests to actual `evaluate_run` and graded `train.main`, beside plausible production provenance, with spies proving no test data or evaluation claim.
For `test_fit_short.py`, copy temporary fixture setup and canonical record assertions from `tests/phase60/test_run_short.py:90-149`. `tests/phase60/_fixtures.py:45-90` supplies a synthetic gold corpus and identity stats; never use the real corpus for unit tests. `test_contracts.py` must prove same-runtime/same-weights production parity and frozen hashes; `test_probe.py` must cover formatter boundaries, selected states, hash-before-load and shared logger agreement.

## Shared Patterns

- Frozen-source boundary: `pinn/verification/learnability_protocol.py:145-179` pins 33 modules, including all historical model/data/loss/scoring helpers above. Reuse them without edits. `pinn/train.py`, `pinn/evaluate.py`, checkpoint and resume are outside that list; modify only entry points needed for demonstrated refusals.
- Evidence safety: `pinn/verification/evidence_io.py:114-193` canonicalizes nonfinite values, rejects dataset output roots and redacts private paths. Prefer exclusive final records over overwriting historical results.
- Access evidence: `evidence_io.files_opened_record`, lines 230-235, wraps the process attestation. Install attestation in the guarded context and retain train/validation/test counts. Existing zero test counts do not prove zero Stage-1 reads.
- No authentication layer applies to these offline tools. Integrity guards, typed refusal errors and admission-before-I/O are the shared controls.
- Keep reproduction registration before rerun and smoke registration before fit. The short 1632 run measures mechanics/cost only. Do not launch later experiments or reuse hour-scale wrappers without compatibility verification.

## No Analog Found

`diagnostic_similarity.py` needs the preserved original measurement definitions; `diagnostic_guard.py` needs a new early artifact-content check. The two `evidence/original/*.py` files are byte-preserved provenance, not patterns to redesign. These four destinations have no complete tracked analog; other assignments explain their partial integration references.

## Metadata

**Search scope:** named current `pinn/` anchors, Phase 64 producer, Phase 59 reader-acceptance evidence and Phase 60 tests. Five bounded pattern groups; no stale maps or runtime mirrors.
**Tracked-source gate:** all analog paths above returned from `git ls-files -- <path>` in this worktree. No probe, fit, tests, benchmark or dataset file was opened/executed during mapping.
