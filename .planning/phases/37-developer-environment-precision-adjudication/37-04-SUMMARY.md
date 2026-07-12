---
phase: 37-developer-environment-precision-adjudication
plan: "04"
subsystem: infra
tags: [subprocess, orchestrator, evidence, provenance, verdict-free, d1-p]

requires:
  - phase: 37-03
    provides: "pinn.verification.componentwise_ad worker (dual-pattern, JSON child worker, fallback-capture-before-import)"
provides:
  - "scripts/run_precision_probe.py — stdlib-only dual-arm orchestrator + evidence writer + renderer + validator"
  - "Append-only, atomic, hash-bound precision-evidence contract (raw.json + summary.md under exclusive UTC run dirs)"
  - "Verdict-free rendering with the fixed owner-decision statement"
affects:
  - "37-05 (Wave 4) invokes run_precision_probe.py run once against the committed fingerprint, then stops at the owner D1-p checkpoint"

tech-stack:
  added: []
  patterns:
    - "Stdlib-only parent: never imports torch or the worker in-process; spawns fixed-argv subprocesses"
    - "Copied + sanitized child env: PYTORCH_ENABLE_MPS_FALLBACK removed for the MPS arm before spawn"
    - "Structured failure retention: timeout/signal/nonzero/malformed-JSON/profile-mismatch/fallback-leakage/device-mismatch/worker-exception all become complete arm records"
    - "Exclusive UTC run dirs + sibling-temp atomic writes; run_id restricted to [A-Za-z0-9_-]+"
    - "Raw-first, renderer-second; summary byte-identical to an independent render_summary(raw)"

key-files:
  created:
    - "scripts/run_precision_probe.py — RuntimeProfile, run_child, build_evidence, render_summary, write_evidence_run, validate_run, main (run/validate CLI)"
  modified: []

key-decisions:
  - "Profile consistency is checked via the worker's top-level precision+requested_device fields (not the 'profile' string label), so the orchestrator's short ids ('fp64-cpu') and the worker's full ids ('float64-cpu') agree"
  - "write_evidence_run restricts run_id to [A-Za-z0-9_-]+ (no dots, slashes, hidden-dir prefixes) so evidence directories are predictable and grep-friendly"
  - "The renderer emits symmetric arm facts plus exactly 'Owner decision required; no D1-p verdict is recorded by this report.' — no score, winner, recommendation, or production default"

patterns-established:
  - "The empirical command is one fixed invocation that runs both arms; no profile/tolerance/workload selector exists"
  - "Failed evidence is retained rather than hidden or converted into another profile's result"

requirements-completed: [ENV-03]

coverage:
  - id: D1
    description: "Stdlib-only dual-arm orchestrator launches exactly fp32-MPS and fp64-CPU through the same worker module with fixed 10/30/100 argv; MPS fallback removed from the copied child env before spawn"
    requirement: "ENV-03"
    verification:
      - kind: unit
        ref: "tests/phase37/test_precision_orchestrator.py#PrecisionOrchestratorTests (15 cases) — green under pinn-train"
        status: pass
      - kind: integration
        ref: "source inspection: argv targets pinn.verification.componentwise_ad; no shell=True; no --profile/--arm selector; PYTORCH_ENABLE_MPS_FALLBACK removed (not replaced) for the MPS arm"
        status: pass
    human_judgment: false
  - id: D2
    description: "Append-only, atomic, hash-bound precision evidence; summary byte-identical to independent render_summary(raw); validator independently checks profile/device/fallback, component/aggregate facts, timing counts/stats, fingerprint hash, and raw-to-summary agreement"
    requirement: "ENV-03"
    verification:
      - kind: unit
        ref: "tests/phase37/test_precision_orchestrator.py#test_write_evidence_run_is_exclusive_and_atomic + test_render_summary_is_byte_identical_to_independent_invocation + test_render_summary_does_not_choose_or_recommend"
        status: pass
      - kind: integration
        ref: "CPU failure smoke: injected MPS failure + real fp64-CPU worker via subprocess -> one raw+summary pair; validate correctly flags the incomplete MPS arm; summary byte-identical to independent render; verdict-free"
        status: pass
    human_judgment: false

duration: ~25min
completed: 2026-07-12
status: complete
---

# Phase 37 Plan 04: Dual-Arm Orchestrator + Evidence Contract Summary

**One stdlib-only command that runs both D1-p profiles through isolated, sanitized subprocesses and writes append-only, provenance-bound, verdict-free evidence — no real MPS run yet (that is Plan 37-05)**

## Performance

- **Duration:** ~25 min
- **Tasks:** 2 (37-04-01 child launch + isolation; 37-04-02 evidence + renderer + validator)
- **Files created:** 1 (scripts/run_precision_probe.py)

## Accomplishments

- **Stdlib-only parent (`scripts/run_precision_probe.py`):** the parent imports neither Torch nor the worker in-process. Source-inspection test confirms no top-level `import torch` and no in-process worker import. It invokes `pinn.verification.componentwise_ad` twice via fixed argv (one fp32-MPS, one fp64-CPU) with `shell=False`, copied/sanitized env, captured text stdout/stderr, and a bounded 900-second timeout.
- **Fallback sanitation (CTX-08):** `_clean_child_env` removes `PYTORCH_ENABLE_MPS_FALLBACK` from the copied environment for the MPS arm (never replaces it with another value). The worker records the pre-import fallback fact; a leaked fallback is structured failed evidence.
- **Structured failure retention (CTX-10):** every failure mode — timeout, signal, nonzero exit, malformed/multiple JSON, schema/profile mismatch, fallback leakage, actual-device mismatch, worker exception — becomes a complete structured arm record. The parent never launches a retry/fallback/third child, synthesizes CPU success, or chooses a D1-p profile.
- **Append-only atomic evidence (CTX-07):** `write_evidence_run` creates an exclusive UTC run directory (rejecting collisions, separators, traversal, hidden-dir prefixes, and symlinked roots). Each file is sibling-temp + `os.replace` with fsync. The `run_id` is restricted to `[A-Za-z0-9_-]+`.
- **Hash-bound provenance:** `build_evidence` loads and SHA-256-hashes the referenced fingerprint JSON path; the raw record carries `fingerprint.path`, `schema_version`, and `sha256` so every precision run is bound to an exact environment fingerprint.
- **Verdict-free rendering (CTX-11/14):** `render_summary` reports symmetric arm facts (status, requested/resolved/actual device, pre-import fallback, torch build, both pattern records' aggregate error + criterion + median) plus the fixed statement `Owner decision required; no D1-p verdict is recorded by this report.` Source-inspection + behavioral tests confirm no `winner`, `recommend`, `faster`, `preferred`, `default to`, or score language.
- **Independent validator:** `validate_run` checks schema version, both arm IDs, per-arm precision/device consistency, both patterns per arm, raw-sample count (30), the six summary statistics, finite aggregate error, fingerprint-hash presence, and summary byte-identity to `render_summary(raw)`.

## Files Created/Modified

- `scripts/run_precision_probe.py` — orchestrator + evidence contract (RuntimeProfile, run_child, build_evidence, render_summary, write_evidence_run, validate_run, main with run/validate subcommands)

## Decisions Made

- **Profile-match check uses precision+requested_device, not the `profile` string.** The worker emits `profile: "float64-cpu"` with separate `precision: "float64"` and `requested_device: "cpu"` fields; the orchestrator compares the latter two so the short-form ids (`fp64-cpu`) and full-form ids (`float64-cpu`) agree. Caught and fixed during the CPU failure smoke (the real CPU worker initially tripped `profile_mismatch`).
- **run_id regex `[A-Za-z0-9_-]+`** (no dots, slashes, hidden-dir prefixes). The test demanded `.hidden` be rejected; the regex is the predictable rule.
- **Injected failure arms in tests.** `build_evidence` accepts either a real `"__spawn__"` sentinel or a dict arm record. Tests inject timeout/signal/malformed/device-mismatch/fallback-leakage records directly to exercise the failure paths deterministically without needing real broken children.

## Deviations from Plan

### Auto-fixed Issues

**1. CPU failure smoke initially returned `profile_mismatch`**
- **Found during:** Task 37-04-02 (CPU failure smoke with the real fp64-CPU worker)
- **Issue:** the orchestrator compared `record.get("profile")` (worker emits `"float64-cpu"`) against `RuntimeProfile.profile_id` (`"fp64-cpu"`). Two naming conventions, no agreement.
- **Fix:** compare `record.get("precision")` and `record.get("requested_device")` instead — those are the canonical fields both sides agree on.
- **Files modified:** scripts/run_precision_probe.py
- **Verification:** CPU smoke now `cpu arm status: ok actual_device: cpu`; 26 orchestrator+componentwise tests green.
- **Committed in:** this task's commit.

**2. `write_evidence_run` initially allowed `.hidden` run IDs**
- **Found during:** Task 37-04-02 (test_write_evidence_run_rejects_path_traversal)
- **Issue:** my separator/traversal check allowed `.hidden` because it has no `/` or `..`. The test's intent was "only safe, predictable run IDs".
- **Fix:** restricted run_id to `[A-Za-z0-9_-]+` (no dots).
- **Files modified:** scripts/run_precision_probe.py
- **Verification:** 15 orchestrator tests green.
- **Committed in:** this task's commit.

---

**Total deviations:** 2 auto-fixed (both in the new orchestrator; no scope creep)
**Impact on plan:** both necessary for correctness. No owner-carved decision touched.

## Issues Encountered

None beyond the two auto-fixes above.

## Next Phase Readiness

- The empirical command is ready: `run_precision_probe.py run --fingerprint-json <path>` will run both fixed arms through the shared worker with MPS fallback disabled, write one exclusive raw+summary record, and print the canonical `PRECISION_RUN_DIR`/`RAW_JSON`/`SUMMARY_MARKDOWN` paths.
- Wave 4 (37-05) runs this command exactly once against the committed fingerprint, validates the result, and stops at the blocking owner D1-p checkpoint.

---
*Phase: 37-developer-environment-precision-adjudication*
*Completed: 2026-07-12*
