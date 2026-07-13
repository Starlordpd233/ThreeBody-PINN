---
phase: 37-developer-environment-precision-adjudication
plan: "05"
subsystem: infra
tags: [d1-p, owner-checkpoint, deferred, evidence, blocking]

requires:
  - phase: 37-04
    provides: "run_precision_probe.py orchestrator + append-only evidence contract"
  - phase: 37-02
    provides: "committed environment pair + canonical fingerprint (the substrate the probe runs against)"
provides:
  - "One validated on-device dual-arm D1-p evidence record (raw.json + summary.md), retained append-only"
  - "Wave-4 environment re-verification fingerprints binding the precision run to the committed lock"
  - "An explicit, owner-recorded D1-p DEFERRED status (Phase 38 blocked until the owner records a branch)"
affects:
  - "Phase 38 (NET) is blocked at D1-p until the owner records fp32-MPS or fp64-CPU"
  - "ACC-01 pre-flight rung 2 (§10.3 AD probe) is satisfied by this retained evidence"

tech-stack: []
patterns: []

key-files:
  created:
    - "evidence/precision/20260712T150406Z/{raw.json,summary.md} — the one authorized on-device dual-arm record"
    - "evidence/environment/20260712T145701Z/, ...20260712T150344Z/ — Wave-4 validation-only re-verification fingerprints"
  modified:
    - "pinn/verification/componentwise_ad.py — worker fix surfaced by the empirical MPS run (constants wrapped as same-dtype tensors)"

key-decisions:
  - "D1-p is DEFERRED. The owner retracted an initial fp32-MPS selection ('i picked the wrong option. let's defer that and we'll decide on this later') and explicitly deferred. Phase 38 remains blocked. The ratified resolution (RATIFICATION.md 2026-07-05, lines 36-40) carves D1-p out as owner-adjudicated; the resolution does not pick a branch, so the agent did not transcribe one."
  - "The empirical Wave-4 run surfaced one real worker defect (scalar_u_jvp on MPS crashed on float × dual-tensor); fixed by wrapping constants as same-dtype tensors. The analytical values are unchanged. The CPU-only Wave 0 contract had not exercised the MPS dual-number path."

requirements-completed: []   # ENV-03 requires the owner's verdict; the evidence is recorded but D1-p is deferred, so the requirement is "surfaced, not chosen" — satisfied as far as the agent may go, but Phase 38 stays blocked.

coverage:
  - id: D1
    description: "One authorized on-device dual-arm D1-p evidence run, validated, owner-readable, with both arms and both AD patterns preserved"
    requirement: "ENV-03"
    verification:
      - kind: integration
        ref: "evidence/precision/20260712T150406Z/raw.json — both arms status=ok, actual devices match requested, no fallback leakage; all four (arm,pattern) cells pass §10.3 criterion (<1e-6); fingerprint SHA-256 bound; validate --run-dir OK; summary byte-identical to independent render"
        status: pass
    human_judgment: true
    rationale: "The owner's D1-p verdict is required to close ENV-03. The agent recorded the evidence and the owner's explicit deferral; it did not choose or apply a branch."

duration: ~30min
completed: 2026-07-12
status: deferred   # plan-level: task 37-05-01 complete; the checkpoint task recorded an explicit deferral per plan (<done>: "The owner's explicit branch or deferral is recorded verbatim")
---

# Phase 37 Plan 05: On-Device Dual-Arm Evidence + Owner D1-p Checkpoint Summary

**The one authorized M5 Pro dual-arm run is retained and validated; the owner explicitly DEFERRED D1-p (retracting an initial fp32-MPS pick); Phase 38 remains blocked**

## Performance

- **Duration:** ~30 min active
- **Tasks:** 37-05-01 (software gate + empirical run + validate) complete; the blocking owner-decision checkpoint recorded an explicit deferral
- **Files committed:** worker fix + 4 retained evidence runs + 2 Wave-4 fingerprints (commit `a65e78c`)

## Accomplishments

- **Full software gate green before the empirical run:** `bash -n` on all shell scripts; full `tests/phase37` discovery (55 tests, 0 failures); `verify_environment.py --check-only` PASS; `git diff --check` clean.
- **Wave-4 environment re-verification:** two more `./setup.sh` validation-only passes (fingerprints `20260712T145701Z`, `20260712T150344Z`), both with all 6 verification checks PASS and lock SHA `36e718cc...0293e3` bound — re-derivable from committed inputs.
- **One authorized dual-arm run** (`run_precision_probe.py run --fingerprint-json $PATH`, with `PYTORCH_ENABLE_MPS_FALLBACK` unset for the MPS child) against the Wave-4 fingerprint. Output retained at `evidence/precision/20260712T150406Z/`. Both arms `status=ok`; actual devices match requested; no fallback leakage; no exceptions.
  - **fp32-mps:** full_jacobian agg=0.00e+00 median≈607µs; scalar_u_jvp agg=0.00e+00 median≈806µs
  - **fp64-cpu:** full_jacobian agg=0.00e+00 median≈103µs; scalar_u_jvp agg=0.00e+00 median≈113µs
  - All four (arm, pattern) cells pass the §10.3 criterion `< 1e-6`.
- **Independent validation:** `validate --run-dir` OK; `render_summary(raw)` byte-identical to the on-disk `summary.md`; the fixed owner-decision statement is present; no verdict language.
- **Worker defect surfaced and fixed:** the empirical fp32-MPS run of `scalar_u_jvp` crashed with `TypeError: unsupported operand type(s) for *: 'float' and 'Tensor'`. Root cause: inside `torch.func.jvp`, the dual-number tangent representation on MPS does not support Python-float × dual-tensor in either operand ordering (CPU float64 accepts both). The CPU-only Wave 0 contract had not exercised the MPS dual-number path, so this defect was not catchable earlier. Fix: `synthetic_trajectory` and `analytical_first_derivative` wrap constants as same-dtype/device tensors. Analytical values unchanged. Committed in `a65e78c`.

## Files Created/Modified

- `pinn/verification/componentwise_ad.py` — worker fix (constants as tensors; both patterns now work on both backends)
- `evidence/environment/20260712T145701Z/` — Wave-4 validation-only fingerprint
- `evidence/environment/20260712T150344Z/` — Wave-4 validation-only fingerprint (bound to the precision run)
- `evidence/precision/20260712T150406Z/{raw.json,summary.md}` — the one authorized dual-arm record

## Decisions Made

- **D1-p = DEFERRED.** The owner initially selected fp32-MPS, then retracted: *"i picked the wrong option. let's defer that and we'll decide on this later."* Recorded verbatim per the plan's `<resume-signal>` contract. Phase 38 remains blocked until the owner records `fp32-MPS` or `fp64-CPU`. The agent did NOT choose, recommend, or apply a branch; no production precision default was introduced.
- **Worker fix recorded as an auto-fix** (not a deviation from the D1-p contract): the fix is a correctness repair that the empirical gate is designed to surface. It changes no owner-carved decision.

## Owner D1-p Checkpoint (verbatim record)

- **Evidence presented:** `evidence/precision/20260712T150406Z/{raw.json,summary.md}` — both arms, both patterns, symmetric facts, no verdict.
- **Question asked:** "Which D1-p branch do you record — fp32-MPS or fp64-CPU — given the attached correctness, failure, and timing evidence?"
- **Owner response (verbatim):** *"i picked the wrong option. let's defer that and we'll decide on this later. record this gap firstr"*
- **Resolution:** D1-p DEFERRED. Phase 38 blocked. Evidence retained for the owner's later adjudication; no re-run required when the owner records a branch (the substrate + probe are reproducible from committed inputs).

## Deviations from Plan

None. The plan explicitly authorizes deferral as a valid resume-signal: *"If the owner defers, record only that explicit deferral and leave Phase 38 blocked."* This summary records the verbatim deferral; the agent applied no precision default and began no Phase 38 work.

## Issues Encountered

- The empirical MPS run surfaced the `scalar_u_jvp` dual-number multiplication defect (fixed; see Accomplishments). This is the empirical gate functioning as designed — the CPU-only Wave 0 contract could not have caught it.

## Next Phase Readiness

- **Phase 38 (NET) is BLOCKED at D1-p.** When the owner records `fp32-MPS` or `fp64-CPU`, the single config default may change without changing the implementation path (CTX-14). No re-run of the probe is required: the retained evidence is reusable.
- ENV-01, ENV-02, ENV-04 are GREEN; ENV-03 is satisfied as far as the agent may go (evidence recorded, owner decision surfaced and deferred). Phase 37's verification surface is otherwise complete.

## Addendum — D1-p recorded (2026-07-12, later session)

- The owner resolved GAP-37-01 with **fp32-MPS** (Option A), retiring the same-day deferral recorded above. The verbatim ruling plus an explicit branch-naming confirmation (owner selected "fp32-MPS" from {fp32-MPS, fp64-CPU, keep deferred}) are recorded in `37-GAPS.md` (RESOLVED-WITH-INSTRUCTION), including the R-6 dual-arm tolerance ratification (fp64-CPU reference arm; fp32-MPS within ~1e-4).
- Production default: `precision=float32, device=mps`; the fp64-CPU arm stays the in-framework escape hatch (ENV-04). **Phase 38 (NET) is UNBLOCKED**; ENV-03 is closable. No probe re-run was needed; no code changed (CTX-14 — `pinn/runtime.py` encodes no default; the Phase 40/41 training config consumes the recorded value).
- The owner additionally ruled that training remains single-machine on the M5 Pro; a Lenovo/multi-machine split is a later cost-benefit question outside v2.0.

---
*Phase: 37-developer-environment-precision-adjudication*
*Plan 37-05 status: complete (owner-recorded D1-p ruling: fp32-MPS; Phase 38 unblocked — see Addendum)*
*Completed: 2026-07-12*
