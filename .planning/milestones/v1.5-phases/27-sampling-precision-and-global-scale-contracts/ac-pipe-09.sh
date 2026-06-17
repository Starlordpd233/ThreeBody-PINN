#!/usr/bin/env bash
# AC-PIPE-09: PIPE-09 compute_globals global-scale contract acceptance check

CTL="pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md"
ARCH="pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md"
ERR=0

echo "=== AC-PIPE-09 ==="
echo ""

# Positive: canonical D
grep -qE 'D = \(G T\^2\)\^\{1/3\}|D = \(G·T\^2\)\^\(1/3\)|\(G·T\^2\)\^\(1/3\)|\(G T\^2\)\^\{1/3\}' "$CTL" && echo "[1] PASS: raw-mass D expression" || { echo "[1] FAIL: raw-mass D"; ERR=1; }
grep -qE '4\.6416' "$CTL" && echo "[2] PASS: D=4.6416" || { echo "[2] FAIL: D=4.6416"; ERR=1; }
grep -qE 'Normative .*compute_globals.*contract' "$CTL" && echo "[3] PASS: normative contract heading" || { echo "[3] FAIL: heading"; ERR=1; }
grep -qE 'r_\{\\mathrm\{safe\}\}|r_safe' "$CTL" && grep -qE 'epsilon_\{\\mathrm\{inv\}\}|varepsilon_\{\\mathrm\{inv\}\}|eps.*=.*1e-10' "$CTL" && echo "[4] PASS: Plummer r_safe/eps_inv" || { echo "[4] FAIL: Plummer"; ERR=1; }
grep -qE 'admitted set|admitted-set' "$CTL" && grep -qE 'Step-1A|Step 1A' "$CTL" && grep -qE 'DATA-05|DATA-05-quarantine' "$CTL" && echo "[5] PASS: admitted-set scope" || { echo "[5] FAIL: admitted-set"; ERR=1; }
grep -qF 'compute-globals-D' "$CTL" && echo "[6] PASS: packet citation" || { echo "[6] FAIL: citation"; ERR=1; }

# Negative: 6.694 only in rejection context
NL=$(grep -nE '6\.694' "$CTL" 2>/dev/null)
if [ -n "$NL" ] && [ -z "$(echo "$NL" | grep -vE 'reject|prohibit|alternative|anti-pattern|future-only|mass-fraction')" ]; then
    echo "[7] PASS: 6.694 only in rejection"
else
    echo "[7] FAIL: 6.694 outside rejection"; ERR=1
fi

# Negative: mass-fraction D form (G M_... T^2)^{1/3} only in rejection context
MFD=$(grep -nE 'D = \(G .*M.*T\^2\)\^\{1/3\}|D = \(G M.*T\^2\)\^\(1/3\)|D = \(G M_\{.*M.*T\^2' "$CTL" 2>/dev/null)
if [ -n "$MFD" ] && [ -z "$(echo "$MFD" | grep -vE 'reject|alternative|prohibit|mass-fraction')" ]; then
    echo "[8] PASS: mass-fraction D form only in rejection"
elif [ -z "$MFD" ]; then
    echo "[8] PASS: mass-fraction D form absent (rejection complete)"
else
    echo "[8] FAIL: mass-fraction D outside rejection"; echo "$MFD"; ERR=1
fi

# Positive: prohibition naming
grep -qE 'No configuration parameter|configuration parameter.*select|configuration parameter.*mass-fraction' "$CTL" && echo "[8b] PASS: 'No configuration parameter' prohibition" || { echo "[8b] FAIL: prohibition"; ERR=1; }

# Negative: E_scale floor NOT 1e-10
BAD=$(grep -nE 'E_\{\\mathrm\{scale\}\}.*10\^\{-10\}|E_\{\\mathrm\{scale\}\}.*1e-10|E_\{mathrm\{scale\}\}.*1e-10' "$CTL" 2>/dev/null)
[ -z "$BAD" ] && echo "[9] PASS: E_scale floor not 1e-10" || { echo "[9] FAIL: E_scale=1e-10"; ERR=1; }

# Positive: E_scale floor = 1e-8
grep -qE 'E_\{\\mathrm\{scale\}\} = \\lvert \\mathrm\{median\}.*10\^\{-8\}|E_\{\\mathrm\{scale\}\} = \\lvert \\mathrm\{median\}.*1e-8' "$CTL" && echo "[10] PASS: E_scale=1e-8" || { echo "[10] FAIL: E_scale=1e-8"; ERR=1; }

# Positive: Plummer eps_inv preserved
grep -qE 'epsilon_\{\\mathrm\{inv\}\} = 10\^\{-10\}|varepsilon_\{\\mathrm\{inv\}\} = 10\^\{-10\}|eps.*=.*1e-10' "$CTL" && echo "[11] PASS: Plummer eps_inv=1e-10 preserved" || { echo "[11] FAIL: Plummer"; ERR=1; }

# Positive: additive-epsilon prohibition
grep -qE 'additive.*epsilon|additive.*eps|anti-pattern' "$CTL" && echo "[12] PASS: additive-eps prohibition" || { echo "[12] FAIL: prohibition"; ERR=1; }

# Arch consistency (read-only)
if [ -f "$ARCH" ] && grep -qE 'E_scale = \|median_traj\(E\)\| \+ 10\^-8' "$ARCH"; then
    echo "[13] PASS: arch §5.2 E_scale already +1e-8"
else
    echo "[13] WARN: arch §5.2 inconclusive"
fi

# SCS untouched
if ! grep -A 20 'Normative .*compute_globals.*contract' "$CTL" | grep -qE 'SCS threshold|1e-6.*SCS|SCS.*1e-6'; then
    echo "[14] PASS: SCS untouched"
else
    echo "[14] FAIL: SCS touched"; ERR=1
fi

echo ""
[ "$ERR" -eq 0 ] && echo "=== AC-PIPE-09: ALL CHECKS PASSED ===" || echo "=== AC-PIPE-09: SOME CHECKS FAILED ==="
exit $ERR
