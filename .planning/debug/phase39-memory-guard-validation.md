---
status: investigating
trigger: "Diagnose root cause only for Phase 39 UAT gap: DATA-01 residency and memory safety inputs fail closed. Expected: adapter rejects invalid memory settings and non-CPU residency. Reproductions: TinyCorpus with capacity_bytes=1 and memory_watermark=float('nan') constructs with 14,044 resident bytes; TinyCorpus with device='meta' constructs non-CPU records and reports 1,504 bytes with only a warning. Read 39-UAT.md, 39-03-PLAN.md, 39-SPEC.md, pinn/data/adapter.py, pinn/data/stage_scan.py, and tests/phase39/test_adapter.py/test_stage_scan.py. Confirm/refute severity and exact root cause, distinguish production-default safety from caller-controlled bypass, and identify minimal fix direction/tests. Root-cause-only; write only this debug file."
created: 2026-07-15T13:50:32Z
updated: 2026-07-15T13:58:00Z
---

## Current Focus

hypothesis: Confirmed — missing constructor validation is the common cause; CLI numeric parsing is not validation, and meta-accounting undercount is a downstream symptom of permitting a forbidden device.
test: Confirm argparse accepts non-finite/range-invalid values and demonstrate invalid interim_s0 changes classification; then run the unchanged adapter/stage-scan suites to show the coverage gap rather than a broad regression.
expecting: CLI will parse NaN/Inf/negative settings and forward them; a known Stage-0 record will become UNASSIGNED under NaN interim_s0; existing suites will still pass.
next_action: Run focused CLI/classifier controls and the existing test_adapter plus test_stage_scan suites without modifying tests.

## Symptoms

expected: Adapter construction rejects invalid memory settings and non-CPU residency, satisfying DATA-01 fail-closed behavior.
actual: TinyCorpus with capacity_bytes=1 and memory_watermark=float('nan') constructs with 14,044 resident bytes; TinyCorpus with device='meta' constructs non-CPU records and reports 1,504 bytes with only a warning.
errors: No exception is raised; the non-CPU case emits only a warning.
reproduction: Construct TinyCorpus once with capacity_bytes=1 and memory_watermark=float('nan'), and once with device='meta'; inspect construction outcome, record devices, and resident_bytes.
started: Observed during Phase 39 UAT; prior behavior is not specified.

## Eliminated

## Evidence

- timestamp: 2026-07-15T13:50:32Z
  checked: Required repository baseline and worktree state.
  found: HEAD is e9e2996acf5ffe4c82dbbbefbc8672538833515c on milestone/v2.0; unrelated dirty paths pre-existed.
  implication: Investigation is running against the mandated baseline and must preserve unrelated shared-worktree changes.

- timestamp: 2026-07-15T13:52:00Z
  checked: 39-UAT.md, 39-03-PLAN.md, and 39-SPEC.md.
  found: DATA-01 requires admitted tensors to be owned CPU fp32, memory to be measured against explicit capacity, and construction to fail when the measured fraction exceeds the configurable watermark; UAT classifies successful NaN/capacity and meta-device construction as major.
  implication: Input validation is part of enforcing a hard safety invariant. Valid production evidence at the 24 GiB/0.7 defaults cannot prove safety for public explicit or CLI-controlled inputs.

- timestamp: 2026-07-15T13:55:00Z
  checked: Complete pinn/data/adapter.py and pinn/data/stage_scan.py implementations.
  found: AdmittedSetAdapter validates precision only. It coerces capacity with int(), watermark with float(), leaves interim_s0 unvalidated, stores device verbatim, and materializes every tensor with device=self._device. The memory gate runs after materialization as fraction > self._watermark. stage_scan argparse converts types but accepts NaN/Inf/range-invalid values and forwards capacity, watermark, and interim_s0 directly.
  implication: NaN makes the greater-than hard gate false by IEEE comparison rules; non-CPU residency violates DATA-01 before accounting; invalid CLI memory inputs reach the adapter unchanged.

- timestamp: 2026-07-15T13:55:00Z
  checked: Resident accounting behavior for non-CPU meta tensors in adapter.py.
  found: Storage identity is keyed by (data_ptr, nbytes); meta storages have no resident allocation and report data_ptr 0, so equal-size distinct storages can collapse. The independent ballpark mismatch path only warns and construction continues.
  implication: The 1,504-byte meta line is not trustworthy resident CPU-byte evidence; it is a secondary consequence of allowing a forbidden device, not a separate valid accounting mode.

- timestamp: 2026-07-15T13:55:00Z
  checked: Complete tests/phase39/test_adapter.py and tests/phase39/test_stage_scan.py.
  found: Adapter tests assert valid CPU fp32 residency, valid default/large-capacity memory lines, and a mocked CLI forwarding test with valid numbers. They contain no rejection matrix for zero/negative/non-finite capacity, non-finite/out-of-range watermark, invalid interim_s0, or non-CPU device; CLI tests never pass NaN.
  implication: Existing green coverage proves only the safe-value path and cannot detect caller-controlled bypasses.

- timestamp: 2026-07-15T13:58:00Z
  checked: Repository-wide AdmittedSetAdapter call sites, relevant project rules, and pinn/data/stages.py.
  found: The only production constructor call is stage_scan.main. It fixes no device argument (therefore uses the safe CPU default) but forwards argparse-converted capacity, watermark, and interim_s0. classify_stage_label performs comparisons against interim_s0 without validating it; stage_scan validates that value only later while building a report, after adapter scan/materialization.
  implication: Production defaults are safe, direct callers control device, and production CLI callers control the numeric safety settings. The adapter must own validation because it is the shared invariant boundary and is usable independently of stage_scan.

- timestamp: 2026-07-15T13:58:00Z
  checked: Focused TinyCorpus experiment matrix on the mandated baseline.
  found: Default constructed 14,044 CPU bytes at fraction 0.000001. capacity=1 with watermark=0.7 raised RuntimeError; the same capacity with NaN constructed at fraction 14,044. Negative capacity constructed with fraction -14,044; infinite watermark constructed at fraction 14,044. device=meta constructed meta tensors, reported 1,504 bytes against a 12,768-byte ballpark, and emitted only resident_tensor_bytes_misfit.
  implication: The UAT failures are repeatable and causally isolated. The ordinary comparison works for a valid watermark; invalid values defeat it. Meta undercount follows from entering an unsupported residency mode.

## Eliminated

- hypothesis: The memory gate arithmetic is generally reversed or broken for valid settings.
  evidence: With capacity_bytes=1 and valid watermark=0.7, the same 14,044-byte TinyCorpus raises the intended RuntimeError.
  timestamp: 2026-07-15T13:58:00Z

- hypothesis: An upstream production caller sanitizes explicit memory settings before adapter construction.
  evidence: stage_scan argparse performs only int/float conversion and main forwards the values directly; no other production AdmittedSetAdapter call site exists.
  timestamp: 2026-07-15T13:58:00Z

- hypothesis: The default production configuration itself violates the observed memory/CPU invariant.
  evidence: The unchanged default uses device=cpu, capacity=24 GiB, watermark=0.7 and constructs the TinyCorpus at fraction 0.000001 without warning; retained UAT evidence reports the real corpus at fraction 0.024292.
  timestamp: 2026-07-15T13:58:00Z

## Resolution

root_cause:
fix:
verification:
files_changed: []
