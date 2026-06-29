---
phase: 35
slug: loss-energy-weight-contracts
verified: 2026-06-29T03:32:42Z
status: pre-ledger-passed
score: "LOSS-01..04 structural checks passed; GAP-32-01 dual-register check passed; ledger closure pending"
gaps_remaining: []
behavior_unverified: 0
overrides_applied: 0
roadmap_truths:
  - "LOSS-01 boundary and precision represented: epsilon_train = 1e-5, tau/u chain factors 2 and 4, componentwise AD, dimensionless coordinates, raw-mass convention, and derivative-scaling distinction"
  - "LOSS-02 boundary and precision represented: PHYS-05 energy weights remain <= 1 and dominance control remains deferred until weighted-loss and gradient evidence exists"
  - "LOSS-03 boundary and precision represented: delta_E = 1.0 remains the baseline and smaller/stage-indexed calibration is deferred until named measurements exist"
  - "LOSS-04 boundary and precision represented: D-04 owner-ratified Option A is transcribed, eta_c = 1 remains, dense-residual ALM is rejected, and window mechanics / numeric causal-clip bounds are absent"
artifacts:
  - path: ".planning/phases/35-loss-energy-weight-contracts/35-VERIFICATION.md"
    provides: "Durable verification record for AC-LOSS-01..04, GAP-32-01, prohibitions, protected paths, and ledger closure"
  - path: ".planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md"
    provides: "Phase 35-owned lifecycle rows; closure appended after this verification precheck"
  - path: "pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md"
    provides: "Phase 35 component-math callouts and single canonical energy-Huber loss body"
  - path: "pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md"
    provides: "Phase 35 total-loss assembly and causal-mode methodology callouts"
prohibitions:
  - statement: "MUST NOT transcribe stale roadmap or issue-doc proposals as final Phase 35 verdicts when the resolution doc marks them modified, rejected, or deferred."
    status: resolved
    verification: "Source-precedence negative checks passed across both framework specs."
  - statement: "MUST NOT fabricate deferred numeric values: no causal-exponent clip bound, no stage-indexed delta table, no automatic dominance controller, and no rejected energy cap schedule."
    status: resolved
    verification: "Cross-spec negative checks passed for all named constructs."
  - statement: "MUST NOT reintroduce dense-residual pseudo-ALM or describe the superseded global+dense label as the current/default verdict."
    status: resolved
    verification: "Dense-residual ALM is rejected from the default loss; optional scalar-conservation ALM remains deferred P2 only."
  - statement: "MUST NOT duplicate normative loss math in both framework specs or create a second canonical home conflict."
    status: resolved
    verification: "D-35-05 sentinel PASS: energy-Huber loss body `L_{E} =` appears only in `pinn_architecture.md`."
---

# Phase 35: Loss & Energy-Weight Contracts - Goal-Backward Verification

Phase 35 structural verification passed before ledger closure. This file records
the command evidence for `AC-LOSS-01`, `AC-LOSS-01-AD`, `AC-LOSS-02`,
`AC-LOSS-03`, `AC-LOSS-04`, the active `GAP-32-01` dual-register read, the
source-precedence negative checks, protected-path checks, and the D-35-05
single-home sentinel.

## Goal Achievement

| # | Truth (ROADMAP / LOSS ID) | Status | Evidence |
|---|---|---|---|
| 1 | LOSS-01 loss scaling and units are represented: dimensionless `u=t/T`, `tau = 2u - 1`, scaled positions, raw-mass force metadata, matched `epsilon_train = 1e-5`, no linear-momentum loss, and componentwise AD with tau/u chain-factor boundary. | VERIFIED | `pinn_architecture.md:310`, `pinn_architecture.md:890`, `ctl_instruction.md:1737`; `AC-LOSS-01` / `AC-LOSS-01-AD` callout-structure PASS. |
| 2 | LOSS-02 energy-loss weights retain PHYS-05 weights <= 1 and reject the stale issue-doc cap-table / high-weight premise; automatic dominance control remains evidence-deferred. | VERIFIED | `pinn_architecture.md:667`, `ctl_instruction.md:1739`; source-precedence negative checks PASS. |
| 3 | LOSS-03 energy Huber delta keeps `delta_E = 1.0` as the current baseline and defers smaller/stage-indexed calibration until normalized `|Delta H|` quantiles, branch occupancy, validation drift, and weighted gradients are measured. | VERIFIED | `pinn_architecture.md:523-537`, `ctl_instruction.md:1741`; D-35-05 `L_{E} =` sentinel PASS. |
| 4 | LOSS-04 causal-training mode consumes owner-ratified D-04 Option A: per-time causal weighting remains baseline, `eta_c = 1`, dense-residual pseudo-ALM rejected, scalar ALM deferred, and windowed-causal mechanics / numeric causal-clip bound not commissioned. | VERIFIED | `pinn_architecture.md:424`, `ctl_instruction.md:1749`, `ctl_instruction.md:1803`; GAP-32-01 dual-register PASS. |

## Requirements Coverage

| Requirement | Acceptance ID | Result | Evidence |
|---|---|---|---|
| LOSS-01 | AC-LOSS-01 | PASS | Loss-scaling callouts found in both specs; component math is canonical in `pinn_architecture.md`, assembly in `ctl_instruction.md`. |
| LOSS-01 | AC-LOSS-01-AD | PASS | `pinn_architecture.md:890` records componentwise AD, canonical `u=t/T`, tau factors 2/4 only on the tau-leaf path, and forbids summed-output VJP. |
| LOSS-02 | AC-LOSS-02 | PASS | PHYS-05 retained with `lambda_E^max <= 1`; cap-table / `lambda_E = 1000` checks absent as normative/default text. |
| LOSS-03 | AC-LOSS-03 | PASS | `delta_E = 1.0` baseline present; per-stage Huber-delta table absent as normative/default text. |
| LOSS-04 | AC-LOSS-04 | PASS | D-04 Option A transcribed; no owner-pending D-04 text remains; windowed-causal mechanics absent as commissioned/default text. |

## 1. Planning Artifact Coverage - PASS

Command run:

```bash
rg -n "AC-LOSS|LOSS-|M15|NS-12|NS-13|NS-18|D-04" \
  .planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md \
  pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md \
  pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md
```

Result: `QUICK-RG: PASS lines=30`.

## 2. Framework-Spec Contract Tokens - PASS

Command run:

```python
from pathlib import Path
text = (
    Path("pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md").read_text()
    + "\n"
    + Path("pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md").read_text()
)
req = ["AC-LOSS-01", "AC-LOSS-02", "AC-LOSS-03", "AC-LOSS-04",
       "NS-18", "M15", "NS-13", "D-04"]
missing = [r for r in req if r not in text]
assert not missing, missing
```

Result: `CONTRACT-TOKENS: PASS`.

## 3. Source-Precedence Negative Checks - PASS

The cross-spec negative suite checked both framework specs for stale/default
loss constructs while allowing explicit rejected or deferred provenance lines.

Covered prohibitions:

| Prohibition | Result |
|---|---|
| Stale `lambda_E = 1000` premise | PASS |
| Stale cap table `{0: 1, 1: 5, 2: 20, 3: 50, 4: 100, 5: 200, 6: 500}` | PASS |
| Per-stage / fabricated Huber-delta table | PASS |
| Numeric causal-exponent clip bound | PASS |
| Automatic dominance reweighting/control law as default | PASS |
| Option C / windowed-causal mechanics as commissioned/default | PASS |
| Default dense-residual ALM or global+dense Option B as current/default | PASS |
| Owner-pending D-04 / causal-mode Phase 35 wording | PASS |

Command result: `NEGATIVE-CHECKS: PASS`.

## 4. Content-Preservation / Anti-Truncation Guards - PASS

Command results:

```text
PINN-TRUNCATION-GUARD-ADJUSTED: PASS lines=1064
CTL-TRUNCATION-GUARD: PASS lines=2142
```

The `pinn_architecture.md` guard uses the current committed section heading
`The Multi-Component Loss Function (Physics-Constrained)`, introduced by Phase
35 Plan 35-02 commit `8c61eb16`. The original 35-04 plan command expected the
older heading `The Multi-Component, Physics-Constrained Loss Function`; that
string is stale against current HEAD. The adjusted guard checks the same section,
plus `Loss Balancing via Warmup Schedule (PHYS-05)` and `Output Layer and
Kinematic Consistency`, with a line-count floor of 1040.

## 5. D-35-05 Single-Home Sentinel - PASS

Command run:

```python
from pathlib import Path
sent = "L_{E} ="
pinn = Path("pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md").read_text()
ctl = Path("pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md").read_text()
homes = [name for name, src in [("pinn_architecture.md", pinn), ("ctl_instruction.md", ctl)] if sent in src]
assert homes == ["pinn_architecture.md"], homes
```

Result: `D-35-05-SENTINEL: PASS homes=['pinn_architecture.md']`.

`GAP-35-01` is already `RESOLVED-WITH-INSTRUCTION` with owner-ratified Option A:
the deterministic no-duplication verifier stays on the energy-Huber `L_{E} =`
single-home sentinel, and the pre-existing causal-weight occurrence in
`ctl_instruction.md` is not edited by Phase 35.

## 6. GAP-32-01 Dual-Register Read - PASS

Command run:

```python
from pathlib import Path
import re
g = Path(".planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-GAPS.md").read_text()
m = re.search(r"##\s*GAP-32-01.*?(?=\n##\s|\Z)", g, re.S)
assert m
assert "RESOLVED-WITH-INSTRUCTION" in m.group(0)
assert "Option A" in m.group(0)
v = Path(".planning/milestones/v1.6-GAPS.md").read_text()
rows = [ln for ln in v.splitlines() if "GAP-32-01" in ln]
assert rows and any("RESOLVED-WITH-INSTRUCTION" in ln and "Option A" in ln for ln in rows)
```

Result: `GAP-32-01-DUAL-REGISTER: PASS`.

Read evidence:

- `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-GAPS.md:50-51` records `GAP-32-01` as `RESOLVED-WITH-INSTRUCTION` and Option A.
- `.planning/milestones/v1.6-GAPS.md:22` records the same owner-ratified Option A and routes Phase 35 `LOSS-04` transcription.

## 7. Callout-Structure Check - PASS

Command run:

```python
from pathlib import Path
import re
specs = [
    Path("pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md").read_text(),
    Path("pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md").read_text(),
]
verdict = re.compile(r"locked|modified|rejected|defer|owner-ratified|RESOLVED-WITH-INSTRUCTION", re.I)
def well_formed(ac):
    return any(
        line.lstrip().startswith(">")
        and ac in line
        and "Phase 35 contract" in line
        and "grounded" in line
        and re.search(r"LOSS-0[1-4]", line)
        and verdict.search(line)
        for text in specs
        for line in text.splitlines()
    )
missing = [ac for ac in ["AC-LOSS-01", "AC-LOSS-02", "AC-LOSS-03", "AC-LOSS-04"] if not well_formed(ac)]
assert not missing, missing
```

Result: `B4-CALLOUT-STRUCTURE: PASS`.

## 8. Protected-Path Status Guard - PASS

Command run:

```python
import subprocess
paths = [
    "pinn_instruction/markdown_conversion/framework-specs/sampling_method.md",
    "pinn_instruction/markdown_conversion/framework-revisions/data_quality_assessment.md",
    "pinn_instruction/markdown_conversion/framework-revisions/review-of-framework/review_of_framework.md",
    "pinn_instruction/markdown_conversion/framework-revisions/stage-strat-revision/stage_strat_revision.md",
    "pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md",
    "pinn",
]
out = subprocess.check_output(["git", "diff", "HEAD", "--name-only", "--"] + paths, text=True)
assert out.strip() == "", out
```

Result: `PROTECTED-PATH-GUARD: PASS`.

## 9. No Package Install Expectation - PASS

No package-manager install commands were run for Phase 35 Plan 35-04. The plan
used only existing local tools: `rg`, `python3`, `git`, and `scripts/agent-commit`
for later commits.

## 10. STOP Gap Completeness - PASS

No new STOP gap was opened by Plan 35-04. Existing gap state read during this
verification:

| Gap | Register | Status | Result |
|---|---|---|---|
| GAP-32-01 | `32-GAPS.md` | RESOLVED-WITH-INSTRUCTION / Option A | PASS |
| GAP-32-01 | `v1.6-GAPS.md` | RESOLVED-WITH-INSTRUCTION / Option A | PASS |
| GAP-35-01 | `35-GAPS.md` and `v1.6-GAPS.md` | RESOLVED-WITH-INSTRUCTION / Option A accept-as-is | PASS |

Because all Phase 35 decisions were already grounded or resolved with explicit
instruction, this plan does not create or modify gap registers.

## 11. Phase-32 Ledger Closure - PENDING

This Task 1 precheck does not mark any ledger row `VERIFIED`. Task 2 may close
only the Phase 35-owned rows after this file records PASS:

| Finding row | Current status before Task 2 | Target after Task 2 |
|---|---|---|
| D-04 | IN_PROGRESS | VERIFIED |
| M15 | IN_PROGRESS | VERIFIED |
| NS-12 | IN_PROGRESS | VERIFIED |
| NS-13 | IN_PROGRESS | VERIFIED |
| NS-18 | IN_PROGRESS | VERIFIED |

## Overall Verdict

Phase 35 structural verification is ready for ledger closure. The only
execution deviation so far is the stale `pinn_architecture.md` anti-truncation
anchor in the plan command; the adjusted guard checks the current committed
heading from Plan 35-02 and preserves the same truncation intent.
