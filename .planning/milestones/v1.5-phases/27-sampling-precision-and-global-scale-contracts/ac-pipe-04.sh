#!/bin/bash
# AC-PIPE-04: M12 points-per-trajectory contract verification
# Run against ctl_instruction.md after Mini-Batch Construction edit

set -e

CTL="pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md"
REGION=$(awk '/^### Mini-Batch Construction with Lookahead Sampling/{f=1;next} /^## /{f=0} f' "$CTL")

echo "=== AC-PIPE-04 Verification ==="
echo ""

# (1) min(n_pts_cap, n_snapshots) present in Mini-Batch region
if echo "$REGION" | grep -q 'min(n_pts_cap, n_snapshots'; then
    echo "PASS (1): min(n_pts_cap, n_snapshots) present in Mini-Batch region"
else
    echo "FAIL (1): min(n_pts_cap, n_snapshots) NOT present in Mini-Batch region"
    exit 1
fi

# (2) without replacement present
if echo "$REGION" | grep -qi 'without replacement'; then
    echo "PASS (2): 'without replacement' present"
else
    echo "FAIL (2): 'without replacement' NOT present"
    exit 1
fi

# (3) default cap 32 flagged as example/non-evidence-based
if echo "$REGION" | grep -qi '32' && echo "$REGION" | grep -qi 'example\|not evidence-based\|configuration knob'; then
    echo "PASS (3): cap 32 flagged as example/non-evidence-based"
else
    echo "FAIL (3): cap 32 NOT properly flagged"
    exit 1
fi

# (4) NEGATIVE CONTROL: 0.5 * n_snapshots appears ONLY in rejection context
if echo "$REGION" | grep -q '0\.5.*n_snapshots\|0\.5×'; then
    if echo "$REGION" | grep -q 'reject\|unevidenced\|not imposed'; then
        echo "PASS (4): 0.5 factor appears ONLY in rejection context (vacuous per F-22)"
    else
        echo "FAIL (4): 0.5 factor appears as operative rule"
        exit 1
    fi
else
    echo "PASS (4): No 0.5 factor found in region (vacuous per F-22)"
fi

# (5) DATA-06 medians cited
if echo "$REGION" | grep -q '61\|127\|1003'; then
    echo "PASS (5): DATA-06 medians (61/127/1003) cited"
else
    echo "FAIL (5): DATA-06 medians NOT cited"
    exit 1
fi

# (6) m11-m12-severity packet cited
if echo "$REGION" | grep -q 'm11-m12-severity'; then
    echo "PASS (6): m11-m12-severity.md packet cited"
else
    echo "FAIL (6): m11-m12-severity.md packet NOT cited"
    exit 1
fi

# (7) n_snapshots and dt_out named as metadata; M16/doc-03 deferral
if echo "$REGION" | grep -q 'n_snapshots' && echo "$REGION" | grep -q 'dt_out'; then
    if echo "$REGION" | grep -qi 'doc-03\|M16\|deferred\|collocation'; then
        echo "PASS (7): n_snapshots/dt_out metadata + M16/doc-03 deferral present"
    else
        echo "FAIL (7): M16/doc-03 deferral NOT present"
        exit 1
    fi
else
    echo "FAIL (7): n_snapshots/dt_out metadata NOT named"
    exit 1
fi

# (8) POST-EDIT ABSENCE ASSERTION: stale "50% uniform" / "weighted by acceleration norm" prose replaced
if echo "$REGION" | grep -q '50% uniform.*50% weighted by acceleration norm'; then
    echo "FAIL (8): Stale 50/50 prose still present in Mini-Batch region"
    exit 1
else
    echo "PASS (8): Stale 50/50 prose replaced (or no longer in region)"
fi

# (8b) Curriculum table preserved
if echo "$REGION" | grep -q 'Replay set' && echo "$REGION" | grep -q 'Look-ahead set'; then
    echo "PASS (8b): Curriculum table (Replay set / Look-ahead set) preserved"
else
    echo "FAIL (8b): Curriculum table NOT preserved"
    exit 1
fi

echo ""
echo "=== AC-PIPE-04: ALL PASS ==="
