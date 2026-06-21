---
phase: 32
slug: evidence-framework-issue-ledger-conflict-adjudication
status: active
nyquist_compliant: true
wave_0_complete: true
created: 2026-06-21
---

# Phase 32 - Validation Strategy

> Per-phase validation contract for evidence-framework planning and execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | shell + Python structural checks |
| **Config file** | none |
| **Quick run command** | `python3 - <<'PY' ... PY` structural probes recorded in `32-VERIFICATION.md` |
| **Full suite command** | artifact existence, verdict/lifecycle enum, ledger row parsing, owner mapping, resolution-doc freshness, forbidden-path status, dirty-doc/gap baseline, and packet source-discipline checks |
| **Estimated runtime** | ~10 seconds |

---

## Sampling Rate

- **After every task commit:** Run the task-local artifact existence and forbidden-path status check.
- **After every plan wave:** Run the full structural check set below.
- **Before `$gsd-verify-work`:** `32-VERIFICATION.md` must record all structural checks as passing, or record explicit deferred blockers.
- **Max feedback latency:** 10 seconds.

---

## Structural Check Set

### Required Artifact Existence

```bash
test -f .planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence/README.md
test -f .planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence/_TEMPLATE.md
test -f .planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-BASELINE-CAPTURED
test -f .planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md
test -f .planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-VERIFICATION.md
```

### Headline Packet Coverage

```bash
for f in d-04-causal-training-mode d-05-s-min-frame d-06-epsilon-strategy m14-gradient-clipping d-6-694-conflict; do
  test -f ".planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence/$f.md"
done
```

### Verdict and Lifecycle Tokens

```bash
python3 - <<'PY'
from pathlib import Path
root = Path(".planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication")
txt = (root / "evidence/README.md").read_text()
required = [
    "accept-resolution",
    "accept-issue-doc",
    "accept-third-position",
    "reject-both-as-unsupported",
    "defer-with-blocker",
    "PENDING",
    "IN_PROGRESS",
    "FIX_APPLIED",
    "VERIFIED",
    "DEFERRED",
]
missing = [token for token in required if token not in txt]
assert not missing, missing
PY
```

### Ledger Status Column Parser

This parser inspects the ledger Status column and Owner Phase column directly.

```bash
python3 - <<'PY'
from pathlib import Path
p = Path(".planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md")
txt = p.read_text()
required = [
    "D-04",
    "D-05",
    "D-06",
    "B-07",
    "B-08",
    "M6",
    "M7",
    "M14",
    "M15",
    "M16",
    "D5",
    "NS-12",
    "NS-13",
    "NS-18",
    "adaptive stage assignment",
    "D = 6.694",
    "L_max / tau_L",
    "ALM mu_p clamp",
]
missing = [item for item in required if item not in txt]
assert not missing, missing

lines = [line for line in txt.splitlines() if line.startswith("|")]
header = next(line for line in lines if "Finding ID" in line and "Status" in line)
cols = [col.strip() for col in header.strip("|").split("|")]
idx = {col: i for i, col in enumerate(cols)}
rows = [line for line in lines if line != header and not set(line.replace("|", "").strip()) <= {"-", " "}]
found = {}
terminal_fix_applied = []
owner_expected = {
    "B-07": "Phase 34",
    "B-08": "Phase 34",
    "M6": "Phase 33",
    "M7": "Phase 33",
    "M15": "Phase 35",
    "M16": "Phase 34",
    "D5": "Phase 33",
    "NS-12": "Phase 35",
    "NS-13": "Phase 35",
    "NS-18": "Phase 35",
    "adaptive stage assignment": "Phase 33",
    "L_max / tau_L": "Phase 33",
    "ALM mu_p clamp": "Phase 34",
}
owner_bad = []
for line in rows:
    cells = [cell.strip() for cell in line.strip("|").split("|")]
    if len(cells) < len(cols):
        continue
    fid = cells[idx["Finding ID"]]
    found[fid] = cells
    if cells[idx["Status"]] == "FIX_APPLIED":
        terminal_fix_applied.append(fid)
    if fid in owner_expected and cells[idx["Owner Phase"]] != owner_expected[fid]:
        owner_bad.append((fid, cells[idx["Owner Phase"]]))
missing_rows = [item for item in required if item not in found]
assert not missing_rows, missing_rows
assert not terminal_fix_applied, terminal_fix_applied
assert not owner_bad, owner_bad
PY
```

### Forbidden-Path Status Guard

```bash
python3 - <<'PY'
from pathlib import Path
import hashlib
import subprocess

root = Path(".planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication")
sentinel = (root / "32-BASELINE-CAPTURED").read_text().splitlines()
def get(prefix: str) -> str:
    return [line.split(": ", 1)[1] for line in sentinel if line.startswith(prefix)][-1]

protected = [
    "pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md",
    "pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md",
    "pinn_instruction/markdown_conversion/framework-specs/sampling_method.md",
    "pinn_instruction/markdown_conversion/framework-revisions/data_quality_assessment.md",
    "pinn_instruction/markdown_conversion/framework-revisions/review-of-framework/review_of_framework.md",
    "pinn_instruction/markdown_conversion/framework-revisions/stage-strat-revision/stage_strat_revision.md",
    "pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md",
    ".planning/STATE.md",
    "pinn/",
]
tracked = (
    subprocess.check_output(["git", "diff", "--name-only", "--"] + protected, text=True).splitlines()
    + subprocess.check_output(["git", "diff", "--cached", "--name-only", "--"] + protected, text=True).splitlines()
)
assert not tracked, tracked

untracked_pinn = subprocess.check_output(
    ["git", "ls-files", "--others", "--exclude-standard", "--", "pinn/"], text=True
)
assert hashlib.sha256(untracked_pinn.encode()).hexdigest() == get("Untracked pinn baseline sha256: "), untracked_pinn
PY
```

### Baseline Sentinel Guard

Record this baseline as the first Phase 32 execution write in both `32-BASELINE-CAPTURED` and `32-VERIFICATION.md`, then compare it at closeout. The closeout check fails if dirty-doc state, gap-file baselines, resolution-doc identity, or untracked `pinn/` state changes without an explicit recorded STOP/blocker reason.

```bash
python3 - <<'PY'
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import subprocess

phase = Path(".planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication")
doc = "docs/work/plans/cross_cutting/gsd-cross-ai-review-resilience/2026-06-20-gsd-review-dispatch-resilience-plan.md"
resolution = Path("pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md")
gap_files = [
    ("32-GAPS", phase / "32-GAPS.md"),
    ("v1.6-GAPS", Path(".planning/milestones/v1.6-GAPS.md")),
]

def gap_baseline(path: Path) -> str:
    if not path.exists():
        return "MISSING"
    data = path.read_bytes()
    return f"EXISTS lines={len(path.read_text().splitlines())} sha256={hashlib.sha256(data).hexdigest()}"

untracked_pinn = subprocess.check_output(["git", "ls-files", "--others", "--exclude-standard", "--", "pinn/"], text=True)
resolution_bytes = resolution.read_bytes()
lines = [
    f"Baseline captured at UTC: {datetime.now(timezone.utc).isoformat()}",
    f"Dirty docs baseline status: {subprocess.check_output(['git','status','--short','--',doc], text=True).strip()}",
    f"Dirty docs baseline patch-sha256: {hashlib.sha256(subprocess.check_output(['git','diff','--',doc])).hexdigest()}",
    f"32-GAPS baseline: {gap_baseline(gap_files[0][1])}",
    f"v1.6-GAPS baseline: {gap_baseline(gap_files[1][1])}",
    f"Untracked pinn baseline sha256: {hashlib.sha256(untracked_pinn.encode()).hexdigest()}",
    f"Untracked pinn baseline entries: {len([line for line in untracked_pinn.splitlines() if line])}",
    f"Resolution doc baseline lines: {len(resolution.read_text().splitlines())}",
    f"Resolution doc baseline bytes: {len(resolution_bytes)}",
    f"Resolution doc baseline sha256: {hashlib.sha256(resolution_bytes).hexdigest()}",
]
print("\n".join(lines))
PY
```

### Resolution-Doc Freshness and Citation Freshness

This check enforces resolution-doc freshness and headline packet citation freshness.

```bash
python3 - <<'PY'
from pathlib import Path
import hashlib

root = Path(".planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication")
doc = Path("pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md")
sentinel = (root / "32-BASELINE-CAPTURED").read_text().splitlines()
def get(prefix: str) -> str:
    return [line.split(": ", 1)[1] for line in sentinel if line.startswith(prefix)][-1]

data = doc.read_bytes()
assert int(get("Resolution doc baseline lines: ")) == len(doc.read_text().splitlines())
assert int(get("Resolution doc baseline bytes: ")) == len(data)
assert get("Resolution doc baseline sha256: ") == hashlib.sha256(data).hexdigest()

lines = doc.read_text().splitlines()
packets = root / "evidence"
expected = {
    "d-04-causal-training-mode.md": (24, 27, "### 1.1"),
    "d-05-s-min-frame.md": (28, 31, "### 1.2"),
    "d-06-epsilon-strategy.md": (32, 35, "### 1.3"),
    "m14-gradient-clipping.md": (52, 55, "### 1.8"),
    "d-6-694-conflict.md": (84, 87, "### 1.16"),
}
bad = []
for name, (start, end, heading) in expected.items():
    packet = (packets / name).read_text()
    snippet = "\n".join(lines[start - 1 : end])
    if heading not in snippet or f"section {heading.split()[1]}" not in packet:
        bad.append(name)
assert not bad, bad
PY
```

### Packet-Scoped Live-Code Discipline

```bash
python3 - <<'PY'
from pathlib import Path
import re

root = Path(".planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence")
pattern = re.compile(r"pinn/(basic_architecture|data-processing-pipeline-full)\.py")
bad = []
for path in root.glob("*.md"):
    lines = path.read_text().splitlines()
    for index, line in enumerate(lines):
        if pattern.search(line):
            window = "\n".join(lines[max(0, index - 3) : min(len(lines), index + 4)])
            if "NOT grounding" not in window and "FUT" not in window:
                bad.append(f"{path}:{index + 1}")
assert not bad, bad
PY
```

### Owner Decision Packet Parser

```bash
python3 - <<'PY'
from pathlib import Path
import re

root = Path(".planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication")
bad = []
for path in [
    root / "evidence/d-04-causal-training-mode.md",
    root / "evidence/d-05-s-min-frame.md",
    root / "evidence/d-06-epsilon-strategy.md",
]:
    text = path.read_text()
    verdict = re.search(r"^Verdict:\s*(.+)$", text, re.M)
    instruction = re.search(r"^Explicit user instruction:\s*(.+)$", text, re.M)
    value = verdict.group(1).strip() if verdict else ""
    cited = bool(instruction and instruction.group(1).strip().lower() not in {"", "none", "n/a", "todo", "missing"})
    if value != "defer-with-blocker" and not cited:
        bad.append((path.name, value, instruction.group(1).strip() if instruction else None))
assert not bad, bad
```

---

## Per-Plan Verification Map

| Plan | Wave | Requirement | Test Type | Automated Command | Status |
|------|------|-------------|-----------|-------------------|--------|
| 32-01 | 1 | EVID-11, EVID-12 | artifact schema | baseline sentinel; required artifact existence; verdict and lifecycle token checks | pending |
| 32-02 | 2 | EVID-13, EVID-14, EVID-15 | packet coverage | resolution-doc freshness; D-conflict and M14 packet source checks | pending |
| 32-03 | 3 | EVID-11, EVID-12, EVID-15 | STOP-safe packet coverage | resolution-doc freshness; D-04/D-05/D-06 parser checks plus gap-register checks if any source-silent semantic decision is opened | pending |
| 32-04 | 4 | EVID-11..15 | full structural verification | all structural checks; forbidden-path guard; baseline comparisons; citation sanity; `32-VERIFICATION.md` updated | pending |

---

## Wave 0 Requirements

Existing infrastructure covers all phase requirements:

- `rg` is available for source and artifact checks.
- `python3` is available for deterministic Markdown/token probes.
- Git hooks are configured through `.githooks`.
- Commits must use `scripts/agent-commit` with explicit owned paths.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| D-04/D-05/D-06 owner decisions | EVID-15 | Semantic owner-routed decisions cannot be selected by structural tests. | Confirm packets either cite explicit user instruction or record `defer-with-blocker` / STOP gaps. |
| First-principles contradiction against v1.5 `D ~= 4.6416` | EVID-15 | A genuine contradiction requires physics reasoning and user instruction before overturning SCOPE-12. | Read `d-6-694-conflict.md`; verify it preserves v1.5 EVID-10 unless a fully surfaced gap is resolved. |

---

## Validation Sign-Off

- [x] All plans have automated structural verification hooks.
- [x] Sampling continuity: every plan has at least one automated check.
- [x] Wave 0 has no missing test framework dependency.
- [x] No watch-mode flags.
- [x] Feedback latency < 10s.
- [x] `nyquist_compliant: true` set in frontmatter.

**Approval:** approved 2026-06-21 for planning.
