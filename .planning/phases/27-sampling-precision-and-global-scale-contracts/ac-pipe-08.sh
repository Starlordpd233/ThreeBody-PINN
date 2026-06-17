#!/usr/bin/env bash
# AC-PIPE-08: Acceptance check for PIPE-08 stage-query contract
# Verifies: dt_out + n_snapshots metadata, sample_replay/sample_lookahead signatures,
#           param_provenance preserved, doc-03/M16 forward-reference present,
#           NO training-loop/collocation-density policy in the NEW stage-query sub-section.

CTL="pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md"

ERR=0

echo "=== AC-PIPE-08: PIPE-08 stage-query contract ==="
echo ""

# --- Positive assertions ---

echo "[1] Checking sample_replay(n, max_stage) signature..."
if grep -qE 'sample_replay\(n, max_stage\)' "$CTL"; then
    echo "    PASS: sample_replay(n, max_stage) found"
else
    echo "    FAIL: sample_replay(n, max_stage) NOT found"
    ERR=1
fi

echo "[2] Checking sample_lookahead(n, stage) signature..."
if grep -qE 'sample_lookahead\(n, stage\)' "$CTL"; then
    echo "    PASS: sample_lookahead(n, stage) found"
else
    echo "    FAIL: sample_lookahead(n, stage) NOT found"
    ERR=1
fi

echo "[3] Checking dt_out in metadata schema..."
if grep -qE 'dt_out' "$CTL"; then
    echo "    PASS: dt_out found in spec"
else
    echo "    FAIL: dt_out NOT found"
    ERR=1
fi

echo "[4] Checking n_snapshots in metadata schema..."
if grep -qE 'n_snapshots' "$CTL"; then
    echo "    PASS: n_snapshots found in spec"
else
    echo "    FAIL: n_snapshots NOT found"
    ERR=1
fi

echo "[5] Checking param_provenance preserved (PIPE-06 regression)..."
if grep -qF 'param_provenance' "$CTL"; then
    echo "    PASS: param_provenance still present"
else
    echo "    FAIL: param_provenance NOT found (PIPE-06 regression!)"
    ERR=1
fi

echo "[6] Checking doc-03 / M16 forward-reference..."
if grep -qiE 'doc-03|M16' "$CTL"; then
    echo "    PASS: doc-03 or M16 forward-reference found"
else
    echo "    FAIL: doc-03/M16 forward-reference NOT found"
    ERR=1
fi

# --- Negative control: scoped to the NEW stage-query sub-section ONLY ---
# Extract the stage-query sub-section (from its heading to the next ### or ## heading)
# and grep within it for forbidden policy text.

echo ""
echo "[7] Negative control: no training-loop/collocation-density policy in NEW stage-query sub-section..."

# Find the stage-query section heading line number
SQ_LINE=$(grep -nE '^#{2,4} .*[Ss]tage[- ][Qq]uery|^#{2,4} .*[Dd]ata[- ][Ss]ide.*[Qq]uery' "$CTL" | head -1 | cut -d: -f1)

if [ -n "$SQ_LINE" ]; then
    # Extract from that line to the next ### or ## heading
    awk -v start="$SQ_LINE" '
        NR >= start {
            if (NR > start && /^#{2,3} /) exit
            print
        }
    ' "$CTL" > /tmp/ac_pipe08_stagequery_section.txt

    # Filter out blockquote lines (the scope-boundary deferral note) — only check non-blockquote content
    grep -v '^>' /tmp/ac_pipe08_stagequery_section.txt > /tmp/ac_pipe08_filtered.txt

    if grep -qiE 'replay.fraction|collocation.density|ρ_lookahead|lookahead.*fraction|training[- ]loop.*policy' /tmp/ac_pipe08_filtered.txt; then
        echo "    FAIL: forbidden policy text found in stage-query sub-section (outside blockquote deferral note)"
        grep -niE 'replay.fraction|collocation.density|ρ_lookahead|lookahead.*fraction|training[- ]loop.*policy' /tmp/ac_pipe08_filtered.txt | head -5
        ERR=1
    else
        echo "    PASS: no forbidden policy text in stage-query sub-section (deferral note correctly blockquoted)"
    fi
else
    echo "    SKIP: stage-query sub-section heading not found (will be checked after edit)"
fi

echo ""
if [ "$ERR" -eq 0 ]; then
    echo "=== AC-PIPE-08: ALL CHECKS PASSED ==="
else
    echo "=== AC-PIPE-08: SOME CHECKS FAILED ==="
fi

exit $ERR
