# Phase 43 Gap Register

## GAP-43-01 — ACC-01 device-sanity rung conflicts with the Phase 38 availability-probe prohibition

- **Decision point:** Phase 43's required device-sanity rung directly calls
  `torch.backends.mps.is_available()` in `pinn/verify.py`, while the retained
  Phase 38 regression gate glob-discovers later `pinn/**/*.py` modules and
  rejects executable `is_available` calls outside its exclusion list. The
  repository-wide acceptance suite is red, so Phase 43 cannot close until the
  owner chooses whether the implementation or the older prohibition boundary
  changes.
- **Where in artifact:** `pinn/verify.py:151-166` (`_rung_device_sanity`);
  `tests/phase38/test_prohibitions.py:99-121,289-300`
  (`_discover_phase38_modules` and the availability-probe assertion);
  `43-12-PLAN.md:113-127` (repository-green gate and explicit STOP rule).
- **Task context:** Post-wave integration verification after Plans 43-09 through
  43-12 completed. The independent command
  `~/miniforge3/envs/pinn-train/bin/python -m unittest discover -s tests -v`
  exited 1; a fail-fast rerun stopped at
  `phase38.test_prohibitions.ProhibitionTests.test_no_precision_default_in_discovered_modules`
  with `module='pinn/verify.py'`. This invalidates Plan 43-12's recorded
  repository-green premise; ACC-02 and ACC-04 were returned to Pending while
  this gap is open.
- **Classification:** cross-phase reframing — resolving it chooses whether the
  Phase 38 future-module prohibition retains global scope or the Phase 43
  operator preflight changes how it proves device availability.
- **Source silence:**
  - `.planning/phases/38-pinn-model-rebuild-from-specs-fut-01/38-06-PLAN.md:217,221,227-230`
    requires glob-discovery of later `pinn/**/*.py` and forbids availability
    probes outside the documented Phase 37 exclusions. It does not anticipate
    a later operator verification entrypoint whose purpose is device sanity.
  - `tests/phase38/test_prohibitions.py:99-121,289-300` implements that global
    future-module scan and explicitly excludes `pinn/runtime.py`, but not
    `pinn/verify.py`; it gives no exception rule for operator preflights.
  - `.planning/phases/43-verification-stage-0-pilot-acceptance/43-SPEC.md:49-54`,
    `43-CONTEXT.md:50-55`, and `43-01-PLAN.md:72` require the first rung to prove
    MPS availability plus the resolved dtype/device. They do not specify
    whether that proof must call `is_available()` or may rely on actual tensor
    materialization.
  - `pinn/runtime.py:1-15,65-78` explicitly says `resolve_runtime` does not
    inspect availability or infer/fallback a device, so silently moving the
    probe into `resolve_runtime` would violate the Phase 37 seam rather than
    resolve the conflict.
  - `.planning/phases/43-verification-stage-0-pilot-acceptance/43-12-PLAN.md:118-127`
    requires the full suite to be green before ACC-02/ACC-04 completion and
    requires STOP on a residual out-of-scope product/contract failure. It does
    not authorize a repair shape.
- **Mathematical / engineering grounding:** Backend availability and successful
  device materialization are related but distinct observations. The PyTorch
  availability predicate reports whether the MPS backend is currently
  available; constructing a tensor on the resolved MPS device is a stronger
  end-to-end proof that the requested dtype/device can actually execute. Phase
  38's invariant centralizes precision/device policy and prevents arbitrary
  production modules from making availability-based fallback decisions. Phase
  43's rung is not selecting or falling back—it is a fail-closed operator
  preflight—but the global token-based test cannot express that distinction.
  Option A keeps the old invariant unchanged by using materialization as the
  availability proof. Option B formally exempts the operator preflight and
  preserves its explicit backend diagnostic, but narrows a previously global
  safety net. Option C restricts the old scan to Phase 38-owned modules, which
  removes the immediate conflict but also stops it from detecting future policy
  drift anywhere else. Moving the call into `resolve_runtime` is not a valid
  option because the locked Phase 37 contract explicitly forbids availability
  inspection there.
- **Agent was tempted to:** Choose Option A: remove the explicit
  `mps.is_available()` predicate and let the existing resolved-device tensor
  construction be the availability proof, while catching its exception to keep
  the rung's failure reason explicit. This is the smallest implementation-side
  repair and preserves both fail-closed behavior and the Phase 38 global check,
  but Plan 43-12 explicitly requires the agent to surface an out-of-scope
  contract failure rather than select a repair silently.
- **What the user needs to decide:**
  - **A. Materialization proof (recommended):** remove the explicit
    `torch.backends.mps.is_available()` call from `pinn.verify`; resolve the
    explicit profile and prove availability by constructing the device/dtype
    probe tensor. Update Phase 43 tests to exercise successful and failing
    materialization. Phase 38's global prohibition stays unchanged.
  - **B. Targeted operator-preflight exception:** add `pinn/verify.py` to the
    Phase 38 exclusion list (or encode an equally narrow AST exception) because
    an operator verification entrypoint legitimately owns an availability
    diagnostic. The explicit availability message stays, but the global
    prohibition is narrowed.
  - **C. Phase-38-owned scope only:** change the Phase 38 test to scan only its
    known Phase 38 implementation modules. This resolves the collision but
    abandons the deliberate later-module drift detection established by Plan
    38-06 and is not recommended.
- **Confidence of impact:** HIGH — the failure is deterministic and blocks the
  1,036-test repository gate, ACC-02/ACC-04 completion, Phase 43 verification,
  and milestone closeout.
- **Status:** RESOLVED-WITH-INSTRUCTION (2026-07-22)
- **Resolution note:** Owner selected **Option A (materialization proof)** at
  the surfaced checkpoint (2026-07-22). Implemented in `pinn/verify.py`: the
  explicit availability predicate was deleted and replaced by the constructive
  seam `_mps_materialization_error()`, which proves the MPS runtime by building
  a probe tensor on it (a raise becomes a curated rung FAIL; a wrong-device
  landing becomes a silent-fallback FAIL). The D1-p-resolved dtype/device probe
  and its landing checks are unchanged, and CTX-70's unconditional-MPS
  semantics are preserved on every arm. `tests/phase43/test_verify_ladder.py`
  patches the seam instead of the predicate and adds three hermetic tests
  exercising successful and failing materialization. Phase 38's prohibition
  scan is untouched. Evidence: prohibition discovery 58/58 OK;
  `tests.phase43.test_verify_ladder` 52/52 OK; independent
  `python -m unittest discover -s tests` → 1,039 tests, exit 0 (1,036 prior +
  3 new materialization tests). ACC-02/ACC-04 restored to Complete in
  `.planning/REQUIREMENTS.md`.

