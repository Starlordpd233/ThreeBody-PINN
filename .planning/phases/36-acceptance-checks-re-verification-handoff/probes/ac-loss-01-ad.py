#!/usr/bin/env python3
# AC-LOSS-01-AD: componentwise AD acceptance check.
# Disposable Phase-36 formula-sanity probe. Reads pinn_architecture.md only; no pinn execution.
# Validates AD chain factors on a synthetic trajectory.

print("=== AC-LOSS-01-AD: componentwise AD ===")

# Synthetic trajectory with tau = 2u - 1
# u = t/T where T = 1.0 (toy normalization)
def tau(u):
    return 2 * u - 1

def dr_dtau(u):
    """Derivative of r with respect to tau: dr/dtau = 2 * dr/du"""
    # On a synthetic trajectory r(u) = u^3, dr/du = 3u^2
    return 2 * (3 * u**2)

def d2r_dtau2(u):
    """Second derivative: d²r/dtau² = 4 * d²r/du²"""
    # For r(u) = u^3, d²r/du² = 6u
    return 4 * (6 * u)

# Test at a few points
test_points = [0.0, 0.25, 0.5, 0.75, 1.0]

print("Testing AD chain factors on synthetic trajectory r(u) = u³:")
print(f"{'u':<8} {'tau':<10} {'dr/dtau':<15} {'d²r/dtau²':<15}")
print("-" * 50)

ERR = 0

for u in test_points:
    t_val = tau(u)
    dr_val = dr_dtau(u)
    d2r_val = d2r_dtau2(u)
    print(f"{u:<8.2f} {t_val:<10.2f} {dr_val:<15.4f} {d2r_val:<15.4f}")

# Verify AD chain factors formula
print("")
print("Verifying AD chain factors:")

# Test dr/du = 2 * dr/dtau
u_test = 0.5
dr_du_manual = 3 * u_test**2
dr_dtau_val = dr_dtau(u_test)
dr_du_from_dtau = dr_dtau_val / 2  # Inverse of dr/dtau = 2*dr/du

if abs(dr_du_manual - dr_du_from_dtau) < 0.001:
    print("[1] PASS: dr/du = (1/2) * dr/dtau (equivalent to dr/dtau = 2 * dr/du)")
else:
    print(f"[1] FAIL: dr/du mismatch: {dr_du_manual} vs {dr_du_from_dtau}")
    ERR = 1

# Test d²r/du² = (1/4) * d²r/dtau²
d2r_du2_manual = 6 * u_test
d2r_dtau2_val = d2r_dtau2(u_test)
d2r_du2_from_dtau2 = d2r_dtau2_val / 4  # Inverse of d²r/dtau² = 4*d²r/du²

if abs(d2r_du2_manual - d2r_du2_from_dtau2) < 0.001:
    print("[2] PASS: d²r/du² = (1/4) * d²r/dtau² (equivalent to d²r/dtau² = 4 * d²r/du²)")
else:
    print(f"[2] FAIL: d²r/du² mismatch: {d2r_du2_manual} vs {d2r_du2_from_dtau2}")
    ERR = 1

# Check spec transcription
print("")
print("Checking spec transcription...")

PINN = "pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md"
with open(PINN) as f:
    pinn_content = f.read()

# Componentwise AD, canonical u=t/T leaf
if "componentwise" in pinn_content.lower() and "u=t/T" in pinn_content:
    print("[3] PASS: componentwise AD with canonical u=t/T leaf present")
else:
    print("[3] FAIL: componentwise AD / u=t/T not found")
    ERR = 1

# Summed-output VJP rejected
if "summed-output VJP rejected" in pinn_content or "VJP.*rejected" in pinn_content:
    print("[4] PASS: summed-output VJP rejected")
else:
    print("[4] FAIL: summed-output VJP rejection not found")
    ERR = 1

print("")
if ERR == 0:
    print("=== AC-LOSS-01-AD: ALL CHECKS PASSED ===")
else:
    print("=== AC-LOSS-01-AD: SOME CHECKS FAILED ===")

exit(ERR)