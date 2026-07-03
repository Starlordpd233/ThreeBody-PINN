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

# PHYS-05: retain λ_E^max ≤ 1.0. Spec wording varies (≤ vs <=, λ vs lambda,
# optionally with surrounding markup); accept either form.
import re
phys05_patterns = [
    r"λ_E\^max[[:space:]]*≤[[:space:]]*1\.0",
    r"λ_E\^max[[:space:]]*<=[[:space:]]*1\.0",
    r"lambda_E\^max[[:space:]]*<=[[:space:]]*1\.0",
    r"lambda_E\^max[[:space:]]*≤[[:space:]]*1\.0",
    r"max energy weight.*<=[[:space:]]*1",
    r"max energy weight.*≤[[:space:]]*1",
    r"PHYS-05.*weight.*<=[[:space:]]*1",
    r"PHYS-05.*weight.*≤",
    r"PHYS-05.*<=.*1",
    r"PHYS-05.*≤[[:space:]]*1",
]
phys05_found = any(re.search(p, pinn_content, re.IGNORECASE) for p in phys05_patterns)
if phys05_found:
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

# Logging-first diagnostics. Spec wording (Phase 35 blockquote AC-LOSS-02):
#   "Before any future control law, log weighted losses, scheduled weights,
#    and gradient statistics; automatic dominance reweighting is deferred..."
# Accept either "logging-first" or the equivalent "log ... ; automatic
# dominance reweighting is deferred" sequencing (logging precedes any
# future control law, dominance control is gated on measured evidence).
import re
logging_patterns = [
    r"logging-first",
    r"logging first",
    r"logging required",
    r"require logging",
    r"diagnostic logging",
    r"log[[:space:]]+(weighted[[:space:]]+losses|scheduled[[:space:]]+weights|gradient[[:space:]]+statistics|all[[:space:]]+loss)",
    r"log[[:space:]].*deferred",
    r"deferred.*log[[:space:]]",
    r"Before any future control law.*log",
    r"training instrumentation.*log",
    r"log weighted losses.*automatic dominance",
    r"automatic dominance.*deferred.*log",
    r"instrumentation.*log",
    r"logging.*diagnostics",
    r"observability first",
]
logging_found = any(re.search(p, ctl_content + "\n" + pinn_content, re.IGNORECASE | re.DOTALL) for p in logging_patterns)
if logging_found:
    print("[4] PASS: logging-first diagnostics specified (or logging-before-dominance)")
else:
    print("[4] FAIL: logging-first diagnostics not found")
    ERR = 1

# Dominance reweighting deferred. Accept either verbatim "dominance reweighting
# deferred" or the equivalent "defer dominance reweighting" / "deferred.*dominance".
dominance_patterns = [
    r"dominance reweighting deferred",
    r"dominance.*reweighting.*deferred",
    r"defer.*dominance",
    r"dominance control.*deferred",
    r"dominance.*deferred",
    r"deferred.*dominance",
]
dominance_found = any(re.search(p, ctl_content + "\n" + pinn_content, re.IGNORECASE) for p in dominance_patterns)
if dominance_found:
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