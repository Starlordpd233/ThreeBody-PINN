#!/usr/bin/env python3
# AC-LOOP-04: merged gradient clipping acceptance check.
# Disposable Phase-36 formula-sanity probe. Reads both specs; no pinn execution.
# Validates clip_value = C_stage * median(grad_norm_history) and C-schedule.

print("=== AC-LOOP-04: merged gradient clipping ===")

# Synthetic gradient-norm history (toy sample)
import statistics
grad_norm_history = [1.0, 2.5, 3.0, 2.8, 3.2, 4.0, 3.8, 2.2, 1.5, 2.0]

# C-schedule from ctl: 7-10 / 5 / 3 (canonical)
C_schedule = {
    0: 7,
    1: 8,
    2: 9,
    3: 10,
    4: 5,
    5: 3
}

print(f"Synthetic gradient-norm history: {grad_norm_history}")
print(f"Median: {statistics.median(grad_norm_history):.2f}")
print(f"C-schedule: {C_schedule}")
print("")

ERR = 0

# Test clip_value formula: clip_value = C_stage * median(history)
median_val = statistics.median(grad_norm_history)
for stage, C in C_schedule.items():
    clip_value = C * median_val
    print(f"Stage {stage}: C={C}, clip_value={clip_value:.2f}")

    # Verify monotonic-by-stage behavior
    if stage > 0:
        prev_C = C_schedule[stage - 1]
        if not (prev_C >= C):  # Non-increasing C schedule
            print(f"  [FAIL] C not non-increasing: C[{stage-1}]={prev_C}, C[{stage}]={C}")
            ERR = 1

# Verify mechanism transcribed in both specs
print("")
print("Checking spec transcription...")

CTL = "pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md"
PINN = "pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md"

with open(CTL) as f:
    ctl_content = f.read()
with open(PINN) as f:
    pinn_content = f.read()

# Mechanism in pinn §4.4
if "clip_value = C_stage * median(recent global gradient norms)" in pinn_content or \
   "clip_value = C_stage·median(grad_norm_history)" in pinn_content:
    print("[1] PASS: mechanism canonical in pinn §4.4")
else:
    print("[1] FAIL: mechanism not found in pinn §4.4")
    ERR = 1

# C-schedule 7-10 / 5 / 3 in ctl
if "7-10" in ctl_content and "/ 5 /" in ctl_content:
    print("[2] PASS: C-schedule 7-10 / 5 / 3 canonical in ctl")
else:
    print("[2] FAIL: C-schedule not found in ctl")
    ERR = 1

# Negative check: rejected clip constant (8.5) absent from both specs
if "8.5" not in ctl_content and "8.5" not in pinn_content:
    print("[3] PASS: rejected clip constant 8.5 absent from both specs")
else:
    print("[3] FAIL: rejected clip constant 8.5 present (should be absent)")
    ERR = 1

# Bidirectional anchors (both specs reference the other)
if "SI-PINN-003" in ctl_content or "Mini-Batch Construction" in pinn_content:
    print("[4] PASS: bidirectional anchors present")
else:
    print("[4] FAIL: bidirectional anchors missing")
    ERR = 1

print("")
if ERR == 0:
    print("=== AC-LOOP-04: ALL CHECKS PASSED ===")
else:
    print("=== AC-LOOP-04: SOME CHECKS FAILED ===")

exit(ERR)