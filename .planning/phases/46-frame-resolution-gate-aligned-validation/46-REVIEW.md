---
phase: 46-frame-resolution-gate-aligned-validation
reviewed: 2026-07-29T13:05:37Z
depth: standard
files_reviewed: 13
files_reviewed_list:
  - pinn/data/adapter.py
  - pinn/data/preprocessing.py
  - pinn/train.py
  - pinn/training/summary.py
  - pinn/training/validation_gate.py
  - pinn/verification/target_frame_probe.py
  - tests/phase39/test_prohibitions.py
  - tests/phase43/test_summary_enrichment.py
  - tests/phase46/test_artifacts.py
  - tests/phase46/test_frame_probe_evidence.py
  - tests/phase46/test_isolation.py
  - tests/phase46/test_pairing_repair.py
  - tests/phase46/test_validation_wiring.py
findings:
  critical: 5
  warning: 1
  info: 0
  total: 6
status: issues_found
---

# Phase 46: Code Review Report

**Reviewed:** 2026-07-29T13:05:37Z
**Depth:** standard
**Files Reviewed:** 13
**Status:** issues_found

## Summary

The implementation has five ship-blocking correctness/integrity defects. The
CONF-08 resident targets do not share the model input gauge, the post-repair
probe cannot classify the frame it now observes, EVAL-01 eligibility can be
unlocked by an unrelated or malformed sidecar, and a later failed validation
event can leave a stale eligible record presented as current. The focused test
suite passes because these adversarial cases are absent; one test explicitly
pins the unsafe non-finite early return.

## Narrative Findings (AI reviewer)

### Critical Issues

#### CR-01 [BLOCKER]: Resident targets and IC13 encode different coordinate frames

**Files:** `pinn/data/adapter.py:861-872`, `pinn/data/preprocessing.py:68-74`

**Issue:** The adapter materializes `pre.r_com_ordered` and
`pre.v_com_ordered`, which deliberately omit the rotation gauge and `D/V`
scaling, while `raw_ic13` is still assembled from `pre.r0_gauge` and
`pre.v0_gauge`, which are rotated and scaled. The network therefore receives a
gauge-fixed initial condition but is trained against an unrotated/unscaled
trajectory. The discarded rotation is not present in the 14D input, so
rotation-related raw targets do not define a single-valued mapping from IC13.
The same mismatch also pairs the training physics path with a frame that the
gate module itself does not recognize as coherent. Training on this residency
can optimize contradictory targets and invalid physics residuals.

**Fix:** Complete the canonical residency transform before any training run:
materialize `pre.r_gauge` / `pre.v_gauge` with the matching normalized-time
contract, keep ordered raw masses, and re-ratify
`RATIFIED_VALIDATION_FRAME`. If raw/native outputs are intentionally retained,
the model contract must instead carry the per-trajectory inverse rotation and
scale and apply them explicitly at the output boundary; do not mix the two
frames implicitly.

#### CR-02 [BLOCKER]: The post-repair probe has no identity class for the repaired resident frame

**File:** `pinn/verification/target_frame_probe.py:632-695`

**Issue:** Identity is tested only against parsed file-order raw arrays or the
fully rotated/scaled gauge arrays. CONF-08 residency is the intermediate
`r_com_ordered` / `v_com_ordered` frame, so every repaired record is forced into
`identity_neither`. The attribution loop then reports the first intermediate
that differs rather than the intermediate the resident matches, and the raw
arm is always inverse-permuted even though repaired positions and masses are
already ordered. Rule 5 at lines 887-894 consequently emits
`VERDICT_NON_FRAME_DIVERGENCE` for the authorized repaired surface. The
instrument cannot produce a truthful machine verdict after the repair it was
used to assess.

**Fix:** Add an explicit ordered-COM/raw identity state comparing residents to
`r_bar_perm` and its velocity equivalent. Determine the latest matching
pipeline state (or first next transform), not the first mismatch. Apply the
inverse mass permutation only when the detected resident body order is file
order. Update verdict rules and fixtures so the repaired intermediate has a
reachable, semantically correct route.

#### CR-03 [BLOCKER]: EVAL-01 eligibility trusts arbitrary sidecar paths and never binds the record to the artifact

**Files:** `pinn/training/summary.py:223-233`,
`pinn/training/validation_gate.py:470-502`

**Issue:** `_eval01_precondition_iii` joins the JSONL-provided string directly
to the run directory without resolving or checking containment. A record can
point through `../` to a valid sidecar from another run and is marked eligible.
It also never checks that the record's step, schema version, metrics, verdict,
counts, or pointer agree with the sidecar. `compact_validation_fields` has the
same identity gap: it validates bytes from disk but returns metric values from
the independent in-memory observation. Reproduction confirmed that a record
at step 999 pointing to `../donor/validation_gate/step-00000007.json` returns
`eval01_precondition_iii=True`.

**Fix:** Resolve the candidate beneath the run directory and require both
containment and the exact step-derived name, then compare every compact field
with the validated payload:

```python
run_dir = Path(path).parent.resolve()
step = require_nonnegative_integral(record["step"])
expected_rel = sidecar_relative_path(step)
if record["gate_sidecar"] != expected_rel:
    return False
sidecar = (run_dir / expected_rel).resolve()
sidecar.relative_to(run_dir)
payload = validate_sidecar_payload(json.loads(sidecar.read_text()))
if payload["global_step"] != step or payload["sidecar_path"] != expected_rel:
    return False
```

Also derive compact JSONL values from the validated payload (or compare them
exactly to the observation) so two different observations cannot be joined
into one apparently valid receipt.

#### CR-04 [BLOCKER]: The fail-closed sidecar validator accepts semantically invalid gate records

**File:** `pinn/training/validation_gate.py:419-467`

**Issue:** `validate_sidecar_payload` checks only top-level presence, row count
and order, metric JSON legality, and the verdict token. It accepts an empty
`frame`, `split="test"`, `gate_status="failed"`, a negative or non-integral
step/stage, duplicate record keys, arbitrary thresholds, an incorrect
`n_nonfinite`, and aggregates/verdicts inconsistent with the rows. Because the
summary treats this validator as the EVAL-01 eligibility boundary, malformed
or tampered evidence becomes a schema-valid durable validation record.
Reproduction confirmed a payload with `frame={}`, `split="test"`,
`gate_status="failed"`, and `global_step=-99` passes unchanged.

**Fix:** Validate all nested types and invariants: exact frame keys and a
coherent accepted tuple; `split == "validation"` and `gate_status == "ok"`;
non-negative integral step/stage/counts; exact relative path; unique, strictly
ordered record keys; canonical thresholds; `n_nonfinite` derived from rows;
and aggregate/SCS/verdict values recomputed with `gate_metrics`. Reject unknown
keys or explicitly version an extension policy.

#### CR-05 [BLOCKER]: Later validation failures are hidden behind a stale eligible record

**Files:** `pinn/train.py:84-110`, `pinn/train.py:848-874`,
`pinn/training/summary.py:200-206`, `pinn/training/summary.py:238-260`,
`tests/phase46/test_validation_wiring.py:185-195`

**Issue:** The gate pass runs before `_append_validation_record`, but a
non-finite validation loss makes that function return without appending
anything, including the contemporaneous gate failure or sidecar pointer. The
summary then selects the previous JSONL record and may report its
`eval01_precondition_iii=True` as current. The JSONL reader similarly skips a
malformed/truncated later line and silently selects an older record. A
two-event reproduction (valid step 7, non-finite failed step 8) leaves one
record whose reported last step is 7. The test at lines 185-195 codifies this
unsafe behavior instead of asserting fail-closed eligibility.

**Fix:** Persist every validation event. Encode a non-finite validation loss as
a JSON-safe sentinel (the summary already maps such strings to `null`), use an
`"unavailable"` trend, and retain the contemporaneous gate fields. Treat a
malformed trailing JSONL record as an incomplete latest event that forces
eligibility false; do not skip past it to an older success. Update the test to
require the failed/latest record and false eligibility.

### Warnings

#### WR-01 [WARNING]: Fractional and string steps are silently coerced into artifact-name collisions

**File:** `pinn/training/validation_gate.py:327-344`

**Issue:** `sidecar_relative_path` claims to require a non-negative integer but
uses `int(global_step)`. Values such as `1.9` and `"1"` are accepted, and `1.9`
maps to `step-00000001.json`. This can overwrite or alias evidence for a
different event when the helper is called outside the currently integer-only
training seam.

**Fix:** Require `numbers.Integral` (while continuing to reject `bool`) and
convert only after the type/range check:

```python
if isinstance(global_step, bool) or not isinstance(global_step, numbers.Integral):
    raise ValueError("global_step must be a non-negative integer")
n = int(global_step)
if n < 0:
    raise ValueError("global_step must be non-negative")
```

---

_Reviewed: 2026-07-29T13:05:37Z_
_Reviewer: the agent (gsd-code-reviewer)_
_Depth: standard_
