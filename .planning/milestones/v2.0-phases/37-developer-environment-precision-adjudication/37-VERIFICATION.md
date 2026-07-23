---
phase: 37-developer-environment-precision-adjudication
verified: 2026-07-13T04:30:00Z
status: passed
score: 4/4 must-haves verified
behavior_unverified: 0
overrides_applied: 0
---

# Phase 37: Developer Environment & Precision Adjudication — Verification Report

**Phase Goal:** A fresh M5 Pro Mac goes from no-Python to a verified `pinn-train` environment in one command, and the D1-p precision decision has its evidence — the `pinn_architecture.md` §10.3 componentwise-AD dual-arm probe — recorded for owner adjudication as the first build act. Every later phase runs on this substrate and under the precision switch this phase establishes.

**Verified:** 2026-07-13
**Status:** passed
**Re-verification:** No — initial verification
**Method:** Goal-backward. Each ROADMAP success criterion (ENV-01..ENV-04) was checked against the delivered artifacts at four levels (exists → substantive → wired → data flows). SUMMARY.md claims were not accepted as evidence.

## Goal Achievement

### Observable Truths (ROADMAP Success Criteria)

| # | Truth (Success Criterion) | Status | Evidence |
|---|---|---|---|
| 1 | ENV-01 — one-command setup on a fresh Mac produces a verified `pinn-train` env (Miniforge3 arm64, Python 3.11, PyTorch 2.12 + MPS, numpy/h5py/pyyaml/tensorboard), idempotently, with `torch.backends.mps.is_available()` True | ✓ VERIFIED | `setup.sh` (root, 97 lines); Miniforge3 arm64 auto-install at `scripts/lib/conda_bootstrap.sh:31-36` (pinned release + committed SHA-256, Darwin/arm64 gate before any network access); idempotency branch at `setup.sh:55-68`; MPS assertion at `scripts/verify_environment.py:181,241`. Live re-execution (UAT 2026-07-13) took the validation-only path and emitted fingerprint `evidence/environment/20260713T035710Z` with `verification.status = pass`, all 6 checks true, `torch.mps.is_available = True`, `python = 3.11.15`, `torch = 2.12.1` |
| 2 | ENV-02 — setup writes an environment fingerprint (`sw_vers`, `python -V`, framework version/build, lockfile hash) and a reproducible `environment.yml` + pinned lockfile pair | ✓ VERIFIED | `environment.yml` (32 lines, direct-intent declaration) + `requirements-lock.txt` (22 lines, exact osx-arm64 replay set) both committed; fingerprint fields present in `evidence/environment/20260713T035710Z/fingerprint.json`: `platform.sw_vers.{product_name,product_version,build_version}` = macOS 26.5.1 (25F80), `python` = 3.11.15, `torch.{version,git_version,is_debug,mps.*}`, `lock.sha256` = `36e718cc…`. Emitted by `scripts/verify_environment.py:103-131,176-177`; wired into `setup.sh:78-89` (setup fails if the verifier does not emit the fingerprint paths). Append-only: 5 distinct timestamped fingerprints on disk, none overwritten |
| 3 | ENV-03 — the §10.3 componentwise-AD probe runs both arms (fp32/`mps` with `PYTORCH_ENABLE_MPS_FALLBACK` **unset**, and fp64/`cpu`), times both AD patterns, and writes a recorded result the owner reads to adjudicate D1-p; **the agent records evidence and does not choose** | ✓ VERIFIED | Both halves hold. **(a) Evidence recorded, verdict-free:** `evidence/precision/20260712T150406Z/{raw.json,summary.md}` contains both arms (`fp32-mps`, `fp64-cpu`, both `status: ok`, `actual_device` matching `requested_device`) and both AD patterns (`full_jacobian`, `scalar_u_jvp`) with median timings. MPS-fallback hygiene is enforced structurally, not assumed: `scripts/run_precision_probe.py:117-127` pops the key from the child env and `:202-208` fails the arm with `fallback_leakage` if the worker reports it set — recorded `pre_import_fallback: None` on both arms. The summary carries **no** score, winner, or recommendation; it ends `Owner decision required; no D1-p verdict is recorded by this report.` (`run_precision_probe.py:52` makes this string a constant). **(b) Owner ruling recorded and propagated:** GAP-37-01 is `RESOLVED-WITH-INSTRUCTION` (2026-07-12) with the verbatim owner quote and an explicit branch-naming confirmation of **fp32-MPS**; propagated to `.planning/milestones/v2.0-GAPS.md:9` and `.planning/STATE.md:178`. CTX-14 holds — no code encodes a default (see truth 4) |
| 4 | ENV-04 — precision is a single config switch (`precision: float32\|float64`, `device: mps\|cpu`) such that the fp32-MPS and fp64-CPU branches run the same code path, the fp64-CPU arm being the in-framework escape | ✓ VERIFIED | `pinn/runtime.py:65` `resolve_runtime(precision, device)` — both args mandatory, **no default values**; exactly two profile pairs (`pinn/runtime.py:44-57`), returning a frozen `RuntimeSpec`; cross-pairs and omissions raise `ValueError` before tensor construction. Exported at `pinn/__init__.py:18`. **Same-code-path proof:** the AD worker calls the one resolver at `pinn/verification/componentwise_ad.py:188,330`, and both arms dispatch through the same `_PATTERN_IMPLEMENTATIONS` table (`:160-162`) and the same `run_probe_arm` (`:302`) — the arms differ only in the two resolved values, and both produced `passed=True` on both patterns. The fp64-CPU escape hatch is reachable through that same resolver. Covered by `tests/phase37/test_runtime.py` (both valid pairs, both cross-pairs, None/partial/unknown inputs, and a no-global-dtype-mutation assertion at `:137`) |

**Score:** 4/4 truths verified (0 present, behavior-unverified)

### Required Artifacts

| Artifact | Expected | Status | Details |
|---|---|---|---|
| `setup.sh` | one-command entry | ✓ VERIFIED | 97 lines; gates inputs before any mutation, bootstraps conda, creates-or-validates, verifies in-env |
| `scripts/lib/conda_bootstrap.sh` | Miniforge3 arm64 bootstrap | ✓ VERIFIED | 188 lines; pinned installer + committed SHA-256; never silently replaces an existing conda |
| `environment.yml` | direct-dependency intent | ✓ VERIFIED | 32 lines; python 3.11, torch 2.12.*, numpy/h5py/PyYAML/tensorboard |
| `requirements-lock.txt` | exact replay set | ✓ VERIFIED | 22 lines; hashed into every fingerprint (`lock.sha256`) |
| `scripts/verify_environment.py` | fingerprint + 6-check contract | ✓ VERIFIED | 430 lines; `--check-only` no-write path confirmed (UAT) |
| `scripts/refresh-environment-lock.sh` | lock maintenance (separate from setup) | ✓ VERIFIED | 253 lines; `bash -n` clean; setup never invokes it |
| `scripts/run_precision_probe.py` | dual-arm orchestrator | ✓ VERIFIED | 542 lines; both arms always run; failures become structured arm records, never silent |
| `pinn/runtime.py` | ENV-04 precision seam | ✓ VERIFIED | 95 lines; no defaults, two pairs, frozen spec |
| `pinn/verification/componentwise_ad.py` | §10.3 shared AD worker | ✓ VERIFIED | 398 lines; two AD patterns over one shared trajectory |
| `tests/phase37/` | phase test suite | ✓ VERIFIED | 5 modules; 55 tests, 0 failures / 0 errors / 0 skips under `pinn-train` (UAT re-execution) |
| `evidence/environment/*/` | append-only fingerprints | ✓ VERIFIED | 5 runs; latest all-pass |
| `evidence/precision/20260712T150406Z/` | D1-p evidence | ✓ VERIFIED | `raw.json` + verdict-free `summary.md`; `validate` subcommand re-run OK (UAT) |

### Key Link Verification

| From | To | Via | Status |
|---|---|---|---|
| `setup.sh` | `scripts/lib/conda_bootstrap.sh` | `source` :27, `conda_bootstrap_resolve` :46 | ✓ WIRED |
| `setup.sh` | `scripts/verify_environment.py` | `conda run -n pinn-train python "$VERIFY_PY"` :78; dies if no fingerprint emitted :87-89 | ✓ WIRED |
| `scripts/run_precision_probe.py` | `pinn/verification/componentwise_ad.py` | subprocess child with sanitized env :117-127, :141-150 | ✓ WIRED |
| `pinn/verification/componentwise_ad.py` | `pinn/runtime.py` | `from pinn.runtime import resolve_runtime` :55; called :188, :330 | ✓ WIRED |
| Both probe arms | one shared AD implementation | `_PATTERN_IMPLEMENTATIONS` :160-162 → `run_probe_arm` :302 | ✓ WIRED (this is the ENV-04 "same code path" claim, and it is structurally true) |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|---|---|---|---|
| Phase test suite | `python -m unittest discover tests/phase37` (in `pinn-train`) | 55 tests, 0 failures, 0 errors, 0 skips | ✓ PASS |
| Shell syntax | `bash -n setup.sh scripts/refresh-environment-lock.sh scripts/lib/conda_bootstrap.sh` | clean | ✓ PASS |
| Env contract, no-write path | `scripts/verify_environment.py --check-only` | PASS, wrote nothing | ✓ PASS |
| Evidence integrity | `scripts/run_precision_probe.py validate --run-dir evidence/precision/20260712T150406Z` | OK | ✓ PASS |
| Idempotent rerun | `./setup.sh` (live) | validation-only path; `environment.yml` + `requirements-lock.txt` byte-identical before/after; one new append-only fingerprint, 6/6 checks pass, MPS available | ✓ PASS |
| Fingerprint reproducibility | independent `render_summary(raw.json)`; SHA-256 recompute | byte-identical / hash matched | ✓ PASS |
| No encoded precision default | inspect `resolve_runtime` signature; search configs | no default args; no config encodes precision/device (CTX-14) | ✓ PASS |

(Spot-checks 1–7 were independently re-executed during UAT on 2026-07-13 and are cited rather than re-run.)

### Requirements Coverage

| Requirement | Status | Evidence |
|---|---|---|
| ENV-01 | ✓ SATISFIED | Truth 1 |
| ENV-02 | ✓ SATISFIED | Truth 2 |
| ENV-03 | ✓ SATISFIED | Truth 3 (both halves: agent recorded without choosing; owner ruling recorded) |
| ENV-04 | ✓ SATISFIED | Truth 4 |

No orphaned requirements: REQUIREMENTS.md maps exactly ENV-01..ENV-04 to Phase 37, and all four are claimed and delivered.

### Anti-Patterns Found

| File | Pattern | Severity | Impact |
|---|---|---|---|
| — | none | — | Debt-marker scan (`TBD`/`FIXME`/`XXX`/`TODO`/`HACK`/placeholder/"not yet implemented") over all 10 production files returned only `mktemp` templates in `scripts/refresh-environment-lock.sh` (`phase37-seed-XXXXXX` etc.), which are literal filename templates, not debt markers. No stubs, no empty implementations, no hardcoded-empty returns. |

## Honest Observations (not gaps)

Recorded for accuracy; none of these block the goal or reduce a criterion below TRUE.

1. **"Activated" in ENV-01 is satisfied in substance, not literally.** `setup.sh` cannot activate the *caller's* shell — no child process can. It instead verifies the environment *from inside* it (`conda run -n pinn-train`, `setup.sh:78`) and prints the exact activation line (`setup.sh:96-97`). This was a deliberate, documented contract (`setup.sh:14-17`, CTX-05: "never claims to activate the caller"; the setup also never mutates shell startup files). The criterion's testable core — fresh Mac → verified env in one command, idempotent, MPS available — is fully met.

2. **`torch.build` records as `"unknown"`.** `scripts/verify_environment.py:176` reads `getattr(torch.version, "build", None) or "unknown"`; PyTorch's `torch.version` exposes no `build` attribute, so the field is always `"unknown"`. Build identity is nonetheless captured — `torch.git_version` (`7269437d…`), `torch.is_debug`, and the macOS `build_version` (25F80) are all recorded. ENV-02's "framework version/build" is met by those fields; the literal `build` key is cosmetically empty.

3. **The probe's `0.00e+00` aggregate error certifies AD wiring, not precision loss.** Each arm's error is measured against *its own* dtype's analytical vector, so a zero on both arms says the AD pattern is correctly wired — it does not say fp32 and fp64 agree. The actual cross-arm fp32-vs-fp64 delta, computed during UAT, is **2.02e-07**, inside the R-6 ~1e-4 tolerance. The recorded evidence is honest about scope; the phase does not overclaim.

4. **fp64-CPU measured ~6× faster than fp32-MPS on this fixture.** Per GAP-37-01's own grounding, the §10.3 fixture (scalar-leaf, single trajectory) is unrepresentative of the Stage-0 workload; Phase 43 measures that. This is noted, not adjudicated — the owner's fp32-MPS ruling stands as recorded, and this verification does not re-adjudicate D1-p or recommend a precision branch.

## Gaps Summary

None. All four ROADMAP success criteria are TRUE of the delivered artifacts, verified at the code, wiring, and evidence levels. The one gap this phase raised — GAP-37-01 (D1-p, owner-carved) — is `RESOLVED-WITH-INSTRUCTION` with a verbatim owner ruling (fp32-MPS), propagated to the milestone gap index and STATE.md, with no precision default encoded in code (CTX-14 verified directly against `pinn/runtime.py:65`).

The ENV-03 governance constraint — the hardest thing to get right in this phase, and the one most likely to be silently violated — held: the agent produced the evidence and did **not** choose. The verdict-free assertion is not merely a summary claim; it is enforced by a constant in the orchestrator (`run_precision_probe.py:52`) and confirmed by reading the recorded `summary.md`, which contains no score, winner, or recommendation.

**Phase goal: ACHIEVED.** The substrate (verified `pinn-train` env, one command, idempotent, fingerprinted) and the precision switch (`resolve_runtime`, two profiles, one shared code path, fp64-CPU escape hatch) both exist and function. Phase 38 has what it depends on.

---

_Verified: 2026-07-13T04:30:00Z_
_Verifier: Claude (gsd-verifier), goal-backward against ROADMAP Phase 37 Success Criteria 1–4_
