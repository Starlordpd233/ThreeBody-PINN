---
phase: 46
slug: frame-resolution-gate-aligned-validation
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# status stays draft until /gsd-validate-phase §6; wave_0_complete flips when 46-01 executes
status: draft
nyquist_compliant: true
wave_0_complete: false
created: 2026-07-25
revised: 2026-07-25  # plan revision 1 (post-checker): nyquist sign-off + measured environment
---

# Phase 46 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
> Seeded by `/gsd-plan-phase 46` from `46-RESEARCH.md` § Validation Architecture.
> The per-task map below is completed once `*-PLAN.md` task IDs exist.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | `unittest` (stdlib), organized per-phase under `tests/phaseNN/`, run via `pytest` |
| **Config file** | none — no `pytest.ini` / `pyproject.toml` / `setup.cfg` at repo root; implicit discovery per `docs/TESTING.md:36` |
| **Quick run command** | `pytest tests/phase46/ -x` |
| **Full suite command** | `pytest tests/` |
| **Estimated runtime** | quick ~seconds (dataset-free synthetic fixtures); full suite covers `tests/phase37`–`phase43` and must stay green |

**Environment precondition (MEASURED at plan revision 1, 2026-07-25):** the resolved
interpreter `"$(dirname "$(git rev-parse --git-common-dir)")/.venv/bin/python"`
(→ `<home>/Desktop/3_body_problem/.venv/bin/python`) imports torch 2.12.0,
numpy 2.2.0, pytest 9.1.1. Lockfile-drift observation retained: `requirements-lock.txt:19`
pins torch 2.12.1 while 2.12.0 is installed — 46-01 Task 1 records this drift in its
SUMMARY as an observation; a lockfile change is out of Phase 46 scope. The
`python -m unittest discover` fallback is unnecessary (pytest present) but remains valid.

**Corpus location:** the real corpus lives in the MAIN checkout
(`<home>/Desktop/3_body_problem/simulation_data/Data`), not in this worktree.
`pinn.data.adapter.default_data_root()` resolves it via `git rev-parse --git-common-dir`
(`adapter.py:593-605`), so execution from `.worktrees/trainex` is correct by design —
do not "fix" a path here.

---

## Sampling Rate

- **After every task commit:** `pytest tests/phase46/ -x`
- **After every plan wave:** `pytest tests/` (full suite; nothing in Phase 46 may
  break `tests/phase37`–`phase43` — the phase composes existing verified components,
  it does not reopen them per D-13/D-26)
- **Before `/gsd-verify-work`:** full suite green
- **One-time, NOT a standing suite dependency (D-24):** the single real-corpus CONF-01
  evidence run. Its artifact is committed; it is not re-run per test invocation.
- **Max feedback latency:** < 60s for the quick command

---

## Per-Task Verification Map

Populated by `/gsd-plan-phase 46` (7 plans, 5 waves). `PY` below is the confirmed
interpreter `"$(dirname "$(git rev-parse --git-common-dir)")/.venv/bin/python"`.

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 46-01-T1 | 46-01 | 1 | CONF-01, INST-01 | T-46-01-02/03 | Stub exposes insertion order; no withheld-split constructor | unit | inline `"$PY" -c` import/contract check (plan verify) | ❌ Wave 0 | ⬜ pending |
| 46-01-T2 | 46-01 | 1 | CONF-01 | T-46-01-01 | Dual-frame fixture force-consistent + frame-separable | unit | `"$PY" -m pytest tests/phase46/test_fixtures_selfcheck.py -x -q` | ❌ Wave 0 | ⬜ pending |
| 46-02-T1 | 46-02 | 2 | CONF-01 | T-46-02-01/03 | Symmetric arms; numerics-only tolerance; boundary pinned | unit (tdd) | `"$PY" -m pytest tests/phase46/test_frame_probe.py -x -q` | ❌ | ⬜ pending |
| 46-02-T2 | 46-02 | 2 | CONF-01 | T-46-02-02/04 | Fail-closed 4-way verdict; sorted traversal; confound attribution | unit (tdd) | `"$PY" -m pytest tests/phase46/test_frame_probe.py -x -q` | ❌ | ⬜ pending |
| 46-03-T1 | 46-03 | 2 | INST-01 | T-46-03-04 | Coherent-pair enforcement; explicit u; full pool; prior-mode restore | unit (tdd) | `"$PY" -m pytest tests/phase46/test_gate_composition.py -x -q` | ❌ | ⬜ pending |
| 46-03-T2 | 46-03 | 2 | INST-01 | T-46-03-01/02/03 | Atomic sidecar; sentinel non-finite; pointer-after-durable | unit (tdd) | `"$PY" -m pytest tests/phase46/test_gate_composition.py -x -q` | ❌ | ⬜ pending |
| 46-04-T1 | 46-04 | 3 | CONF-01 | T-46-04-04/05 | Manifest-key eligibility; no withheld-split StageIndex; drift fails closed | unit (tdd) | `"$PY" -m pytest tests/phase46/test_frame_probe_evidence.py -x -q` | ❌ | ⬜ pending |
| 46-04-T2 | 46-04 | 3 | CONF-01 | T-46-04-01/02/03 | Deterministic D-05 evidence; redaction; containment | unit (tdd) | `"$PY" -m pytest tests/phase46/test_frame_probe_evidence.py -x -q` | ❌ | ⬜ pending |
| 46-05-T1 | 46-05 | 3 | INST-01 | T-46-05-01 | AST + subprocess evaluator isolation; mode restore; non-interference | unit | `"$PY" -m pytest tests/phase46/test_isolation.py -x -q` | ❌ | ⬜ pending |
| 46-05-T2 | 46-05 | 3 | INST-01 | T-46-05-02/03/04 | Schema fail-closed; sentinel retention; pointer discipline | unit | `"$PY" -m pytest tests/phase46/test_artifacts.py -x -q` | ❌ | ⬜ pending |
| 46-06-T1 | 46-06 | 4 | CONF-01 | T-46-06-04 | Manifest hashes + population-decision provenance recorded pre-run | integration preflight | plan verify (root reachability + 3 distinct manifest digests + blacklist key) | n/a | ⬜ pending |
| 46-06-T2 | 46-06 | 4 | CONF-01 | T-46-06-01/03 | One real-corpus evidence run; schema/verdict/no-host-path checks | integration / evidence (one-time, D-24) | plan verify (raw.json parse + verdict constant + host-path scan) | n/a | ⬜ pending |
| 46-06-T3 | 46-06 | 4 | CONF-01 | T-46-06-01/02 | Evidence-grounded verdict doc; exact D-08/D-09 routing | evidence + manual branch check | plan verify (46-VERDICT.md section greps) + Manual-Only rows below | n/a | ⬜ pending |
| 46-07-T1 | 46-07 | 5 | INST-01 | T-46-07-01 | Frame constant only from recorded ratification; else BLOCKED | source assertion | plan verify (import + coherence check of RATIFIED_VALIDATION_FRAME) | n/a | ⬜ pending |
| 46-07-T2 | 46-07 | 5 | INST-01 | T-46-07-02/04 | Sidecar-before-pointer at existing cadence; failure fails closed | unit (tdd) | `"$PY" -m pytest tests/phase46/test_validation_wiring.py -x -q` | ❌ | ⬜ pending |
| 46-07-T3 | 46-07 | 5 | INST-01 | T-46-07-03/05 | EVAL-01 (iii) render fail-closed; sentinel passthrough | unit (tdd) | `"$PY" -m pytest tests/phase46/test_validation_wiring.py -x -q && "$PY" -m pytest tests/ -q` | ❌ | ⬜ pending |

> **Revision 1 note (2026-07-25, checker B2):** the per-plan `<verify>` blocks now wrap each
> OWN-suite pytest invocation in a skip-intolerant guard (`-rs` plus a zero-"skipped" check),
> so a suite whose tests all hit the `_require` SkipTest path can no longer exit green. The
> commands above are the underlying pytest invocations; phase-WIDE sweeps stay skip-tolerant
> mid-wave (sibling plans may not have landed) and become skip-intolerant at 46-07-T3 (wave 5,
> all owners landed).

### Requirement-level map (binding; from `46-RESEARCH.md`)

| Req ID | Behavior | Test Type | Automated Command | File Exists |
|--------|----------|-----------|-------------------|-------------|
| CONF-01 | Symmetric raw/scaled-hypothesis probe identifies the correct arm on synthetic fixtures; canonical preprocessing is the positive control; stable key ordering; train/validation inclusion and **test exclusion**; mismatched body-order/metadata controls; ambiguous/non-finite fails closed (D-21) | unit | `pytest tests/phase46/test_frame_probe.py -x` | ❌ Wave 0 |
| CONF-01 | Real-corpus evidence run producing the committed machine-readable evidence + Markdown rendering (D-05) | integration / evidence (one-time, D-24) | dedicated CLI invocation over the real corpus — **not** part of `pytest tests/` | ❌ Wave 0 |
| INST-01 | Per-trajectory `eps_H`/SCS composed via `gate_metrics`; strict threshold direction; worst-case aggregation; aggregate SCS derived from that single value; sorted `RecordKey` identity; coherent position/time pair; reuse **not** reimplementation of gate functions (D-22) | unit + small multi-trajectory integration | `pytest tests/phase46/test_gate_composition.py -x` | ❌ Wave 0 |
| INST-01 | Held-out isolation: validation-only construction, never imports/calls `pinn.evaluate`, model-mode restoration even on error, loss/optimizer/scheduler/stage-exit/replay/checkpoint/early-stop provably untouched (D-16/D-23) | unit | `pytest tests/phase46/test_isolation.py -x` | ❌ Wave 0 |
| INST-01 | Atomic sidecar publication, schema validation, JSON-safe non-finite encoding, compact `validation.jsonl` linkage, terminal-summary projection, fail-closed empty/missing/corrupt cases — all dataset-free (D-17/D-18/D-20/D-24) | unit | `pytest tests/phase46/test_artifacts.py -x` | ❌ Wave 0 |

---

## Wave 0 Requirements

- [ ] `tests/phase46/__init__.py` — `_SKIP_PHRASE` convention, mirroring `tests/phase43/__init__.py:26`
- [ ] `tests/phase46/_fixtures.py` — extend `tests/phase40/_fixtures.py::_StubSource` (duck-typed `StageIndex`) for gate-composition and isolation tests; **plus** a separate synthetic raw-vs-scaled trajectory-pair fixture for the frame-probe tests (D-21: same trajectory encoded once raw, once locked processed/scaled, same `D`/`T`)
- [ ] Environment confirmation — `pytest` and `torch` present where execution happens (no install command prescribed; research could not verify the real dev environment)

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| CONF-01 verdict adjudication (raw `r` vs `r' = r/D`) | CONF-01 | The verdict is an owner-facing conclusion drawn from committed population evidence, not an assertable constant. Automating a pass/fail here would be the invented threshold D-06 forbids. | Read the committed evidence artifact + Markdown rendering; confirm both hypothesis arms are reported symmetrically, the positive and provenance controls agree as expected, the confound discriminators (permutation / COM-boost / rotation-gauge / metadata-pairing) are each reported, and the numerical tolerance is stated separately from any physics threshold. |
| CONF-01 branch routing on a defect or ambiguous result | CONF-01 | D-09 requires the owner scope decision to be surfaced, not decided by a test. | If the verdict is "wrong frame" or "ambiguous": confirm `46-GAPS.md` + `.planning/milestones/v2.2-GAPS.md` carry the full record and that dependent work halted rather than being absorbed. |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies (16/16 task rows carry an automated command)
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references (46-01 lands `__init__`, `_fixtures`, selfcheck before every consumer)
- [x] No watch-mode flags
- [x] Feedback latency < 60s (dataset-free synthetic suites; the one real-corpus run is 46-06's committed one-time evidence, not a standing suite)
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** planner sign-off 2026-07-25 (revision 1, after gsd-plan-checker audit: 16/16 per-task map rows populated and Nyquist-compliant). The `status: validated` flip remains with `/gsd-validate-phase` §6.
