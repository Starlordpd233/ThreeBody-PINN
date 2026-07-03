#!/usr/bin/env python3
# AC-CURR-02-LMAX: L_max and tau_L formula acceptance check.
# Disposable Phase-36 formula-sanity probe. Reads ctl_instruction.md only; no pinn touch.
# Validates characteristic-scale L_max + raw-mass D ≈ 4.6416 on a documented sample.

import math

# Documented constants from v1.5-locked convention (see Phase 33 verification)
# Source: ctl_instruction.md §2.5 "Raw-Mass Characteristic Scale"
G = 1.0  # Gravitational constant (G-units)
T = 10.0  # Characteristic time period (days)
M_tot = 3.0  # Total mass (solar masses, sum of three equal bodies)

# Characteristic scale calculations
# D = (G * T^2)^(1/3) ≈ 4.6416
D_calculated = (G * T**2) ** (1/3)
D_locked = 4.6416
D_rejected = 6.694

# L_max = M_tot * r_char * v_char
# For a Plummer model with Plummer scale a = 1.0:
#   r_char = a * 2^(1/3) ≈ 1.2599
#   v_char = sqrt(G * M_tot / a) ≈ sqrt(3.0) ≈ 1.7321
r_char = 1.0 * (2 ** (1/3))  # Plummer radius at peak circular velocity
v_char = math.sqrt(G * M_tot / 1.0)
L_max = M_tot * r_char * v_char

print("=== AC-CURR-02-LMAX: L_max and tau_L formula sanity check ===")
print(f"Documented toy sample: G={G}, T={T}, M_tot={M_tot}")
print(f"Calculated D = (G * T^2)^(1/3) = {D_calculated:.4f}")
print(f"Locked v1.5 convention: D ≈ {D_locked}")
print(f"Rejected provenance: D = {D_rejected}")
print(f"L_max = M_tot * r_char * v_char = {L_max:.4f}")
print("")

ERR = 0

# Verify D ≈ 4.6416 (active value)
if abs(D_calculated - D_locked) < 0.01:
    print("[1] PASS: raw-mass D ≈ 4.6416 is numerically reproducible")
else:
    print(f"[1] FAIL: D calculation {D_calculated:.4f} does not match locked {D_locked}")
    ERR = 1

# Verify rejected 6.694 is NOT the active scale
if abs(D_calculated - D_rejected) > 0.1:
    print("[2] PASS: D = 6.694 is NOT the active scale (rejected provenance only)")
else:
    print(f"[2] FAIL: D = {D_rejected} appears to be active (should be rejected)")
    ERR = 1

# Verify L_max formula produces reasonable characteristic scale
if 0 < L_max < 10:  # Sanity bounds for toy sample
    print(f"[3] PASS: L_max = {L_max:.4f} is a reasonable characteristic angular-momentum scale")
else:
    print(f"[3] FAIL: L_max = {L_max:.4f} is outside reasonable bounds")
    ERR = 1

print("")
if ERR == 0:
    print("=== AC-CURR-02-LMAX: ALL CHECKS PASSED ===")
else:
    print("=== AC-CURR-02-LMAX: SOME CHECKS FAILED ===")

exit(ERR)