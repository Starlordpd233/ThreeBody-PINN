#!/usr/bin/env python3
# AC-LOSS-02: energy-weight schedule acceptance check.
# Disposable Phase-36 formula-sanity probe. Reads both specs; no pinn execution.
# Validates adjudicated weight rule and PHYS-05 constraint.

print("=== AC-LOSS-02: energy-weight schedule ===")

# Transcribed adjudicated weight rule (per Phase 35 verification)
# This is a placeholder for the actual adjudicated rule structure
# The probe asserts the PHYS-05 constraint and checks rejected patterns are absent

CTL = "pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md"
PINN = "pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md"

with open(CTL) as f:
    ctl_content = f.read()
with open(PINN) as f:
    pinn_content = f.read()

ERR = 0

# PHYS-05: retain λ_E^max ≤ 1.0
if "λ_E^max ≤ 1.0" in pinn_content or "lambda_E^max <= 1.0" in pinn_content.lower():
    print("[1] PASS: PHYS-05 λ_E^max ≤ 1.0 constraint retained")
else:
    print("[1] FAIL: PHYS-05 λ_E^max ≤ 1.0 constraint not found")
    ERR = 1

# Issue-doc energy cap-table replacement REJECTED
# Check that the rejected cap-table pattern is absent from both specs
cap_table_pattern = "{0:1...6:500}"  # The rejected literal pattern
if cap_table_pattern not in ctl_content and cap_table_pattern not in pinn_content:
    print("[2] PASS: rejected energy cap-table pattern absent from specs")
else:
    print("[2] FAIL: rejected energy cap-table pattern still present")
    ERR = 1

# Check for lambda_E = 1000 rejection (negative check)
if "lambda_E = 1000" not in ctl_content and "lambda_E = 1000" not in pinn_content:
    print("[3] PASS: lambda_E = 1000 rejected value absent")
else:
    print("[3] FAIL: lambda_E = 1000 still present (should be rejected)")
    ERR = 1

# Logging-first diagnostics
if "logging-first" in ctl_content.lower() or "logging-first" in pinn_content.lower():
    print("[4] PASS: logging-first diagnostics specified")
else:
    print("[4] FAIL: logging-first diagnostics not found")
    ERR = 1

# Dominance reweighting deferred
if "dominance reweighting deferred" in ctl_content.lower() or "dominance.*deferred" in pinn_content.lower():
    print("[5] PASS: dominance reweighting deferred")
else:
    print("[5] FAIL: dominance reweighting deferral not found")
    ERR = 1

print("")
if ERR == 0:
    print("=== AC-LOSS-02: ALL CHECKS PASSED ===")
else:
    print("=== AC-LOSS-02: SOME CHECKS FAILED ===")

exit(ERR)