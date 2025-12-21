#!/usr/bin/env python3
"""
Compare original vs revised prescreening thresholds
"""

import json
import numpy as np

# Load the failed results
json_file = "<home>/Desktop/cursor/3_Body_Problem/run_results_2025-06-16T21-27-29.065044.json"
with open(json_file, 'r') as f:
    data = json.load(f)

# Extract parameters
results = data['detailed_results']
virial_ratios = [r['virial_ratio'] for r in results]
angular_momenta = [r['angular_momentum'] for r in results]

print("="*60)
print("THRESHOLD COMPARISON")
print("="*60)

# Original thresholds
print("\nORIGINAL THRESHOLDS:")
print("  Virial ratio: 0.7 < Q < 1.5")
print("  Angular momentum: L > 0.1")

orig_virial_pass = sum(1 for v in virial_ratios if 0.7 <= v <= 1.5)
orig_angular_pass = sum(1 for l in angular_momenta if l > 0.1)
orig_both_pass = sum(1 for i in range(len(virial_ratios)) 
                     if 0.7 <= virial_ratios[i] <= 1.5 and angular_momenta[i] > 0.1)

print(f"\nWith original thresholds:")
print(f"  Virial pass: {orig_virial_pass}/{len(virial_ratios)} ({orig_virial_pass/len(virial_ratios)*100:.1f}%)")
print(f"  Angular pass: {orig_angular_pass}/{len(angular_momenta)} ({orig_angular_pass/len(angular_momenta)*100:.1f}%)")
print(f"  Both pass: {orig_both_pass}/{len(results)} ({orig_both_pass/len(results)*100:.1f}%)")

print("\n" + "-"*60)

# Revised thresholds
print("\nREVISED THRESHOLDS (Fixed):")
print("  Virial ratio: 0.001 < Q < 2.0")
print("  Angular momentum: L > 0.0")

rev_virial_pass = sum(1 for v in virial_ratios if 0.001 <= v <= 2.0)
rev_angular_pass = sum(1 for l in angular_momenta if l > 0.0)
rev_both_pass = sum(1 for i in range(len(virial_ratios)) 
                    if 0.001 <= virial_ratios[i] <= 2.0 and angular_momenta[i] > 0.0)

print(f"\nWith revised thresholds:")
print(f"  Virial pass: {rev_virial_pass}/{len(virial_ratios)} ({rev_virial_pass/len(virial_ratios)*100:.1f}%)")
print(f"  Angular pass: {rev_angular_pass}/{len(angular_momenta)} ({rev_angular_pass/len(angular_momenta)*100:.1f}%)")
print(f"  Both pass: {rev_both_pass}/{len(results)} ({rev_both_pass/len(results)*100:.1f}%)")

print("\n" + "-"*60)

# Adaptive thresholds (percentile-based)
virial_5th = np.percentile(virial_ratios, 5)
virial_99th = np.percentile(virial_ratios, 99)

print("\nADAPTIVE THRESHOLDS (5th-99th percentile):")
print(f"  Virial ratio: {virial_5th:.4f} < Q < {virial_99th:.4f}")
print("  Angular momentum: L > 0.0")

adapt_virial_pass = sum(1 for v in virial_ratios if virial_5th <= v <= virial_99th)
adapt_both_pass = sum(1 for i in range(len(virial_ratios)) 
                      if virial_5th <= virial_ratios[i] <= virial_99th)

print(f"\nWith adaptive thresholds:")
print(f"  Virial pass: {adapt_virial_pass}/{len(virial_ratios)} ({adapt_virial_pass/len(virial_ratios)*100:.1f}%)")
print(f"  Angular pass: {rev_angular_pass}/{len(angular_momenta)} ({rev_angular_pass/len(angular_momenta)*100:.1f}%)")
print(f"  Both pass: {adapt_both_pass}/{len(results)} ({adapt_both_pass/len(results)*100:.1f}%)")

print("\n" + "="*60)
print("RECOMMENDATION")
print("="*60)
print("\nThe revised script includes:")
print("1. Fixed relaxed thresholds suitable for cold systems")
print("2. Optional adaptive thresholds based on data distribution")
print("3. Ability to process without angular momentum filtering")
print("\nThis should allow ~95% of your ICs to pass static checks,")
print("then the dynamic integration will filter out truly unstable ones.")
