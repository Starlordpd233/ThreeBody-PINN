---
phase: 34
slug: training-loop-batch-construction-contracts
verified: 2026-06-25T07:30:00Z
status: passed
score: 9/9 requirements verified; 5/5 LOOP ledger rows VERIFIED; GAP-34-01 resolved (Plan 34-06)
gaps_remaining: []
behavior_unverified: 0
overrides_applied: 0
roadmap_truths:
  - "LOOP-01 replay/lookahead batch construction transcribed as provisional (B_replay=240, B_lookahead=16, has_stage guard, SI-PINN-003 canonical home in ctl); source-silent edge cases recorded as GAP-34-01, not invented"
  - "LOOP-02 two-independent-point-set contract transcribed (data-fidelity snapshots vs collocation points, single forward pass allowed, 8192/4096 provisional/example budgets)"
  - "LOOP-03 mixed time sampling reconciled: data-fidelity 50/50 retained, collocation 50/50 deferred (not mandated)"
  - "LOOP-04 merged gradient clipping single-homed: mechanism `clip_value = C_stage * median(...)` canonical in pinn §4.4, schedule `7-10 / 5 / 3` canonical in ctl, 8.5 absent both, bidirectional AC-LOOP-04 anchors resolve"
  - "LOOP-05 ALM parameter-update / mu_p clamp transcribed as deferred/optional; dense-residual ALM rejected from default loss"
  - "LOOP-06 dt_out-aware collocation scaling realized-as-deferred (candidate direction only, no probe-able formula); inverse form not adopted"
  - "LOOP-07 IPR/PSC training-side roles carried provisionally with VAL-03/VAL-04 forward-references"
  - "LOOP-08 SASD training-side collocation-weighting role carried provisionally with VAL-02 forward-reference"
  - "SI-PINN-003 reconciled: pinn §3.1 author-comment inconsistency removed, ctl_instruction.md canonical, RESOLVED log in pinn"
artifacts:
  - path: "pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md"
    provides: "Transcribed LOOP-01/02/03/06/07/08 contracts and LOOP-04 C-schedule (single canonical home)"
  - path: "pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md"
    provides: "Transcribed LOOP-04 mechanism (single canonical home), LOOP-05 optional/deferred ALM, SI-PINN-003 reconciliation"
  - path: ".planning/phases/34-training-loop-batch-construction-contracts/evidence/b-07-replay-lookahead-batching.md"
    provides: "LOOP-01 grounding packet (B-07 accept-resolution)"
  - path: ".planning/phases/34-training-loop-batch-construction-contracts/evidence/b-08-data-vs-collocation-points.md"
    provides: "LOOP-02/03 grounding packet (B-08 accept-resolution)"
  - path: ".planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence/m14-gradient-clipping.md"
    provides: "LOOP-04 grounding packet (M14 accept-resolution; Phase 32 packet, Phase 34 consumes)"
  - path: ".planning/phases/34-training-loop-batch-construction-contracts/evidence/alm-mu-p-clamp.md"
    provides: "LOOP-05 grounding packet (ALM defer-with-blocker)"
  - path: ".planning/phases/34-training-loop-batch-construction-contracts/evidence/m16-dt-out-collocation-scaling.md"
    provides: "LOOP-06 grounding packet (M16 defer-with-blocker)"
key_links:
  - from: "34-VERIFICATION.md"
    to: "32-ISSUE-LEDGER.md"
    via: "five LOOP rows closed VERIFIED after this verification records PASS"
  - from: "34-VERIFICATION.md"
    to: "34-GAPS.md / v1.6-GAPS.md"
    via: "GAP-34-01 STOP-completeness + closure-gating record"
  - from: "pinn_architecture.md §4.4"
    to: "ctl_instruction.md C-schedule"
    via: "bidirectional AC-LOOP-04 anchors; mechanism one home in pinn, schedule one home in ctl"
prohibitions:
  - statement: "MUST NOT close any ledger row to VERIFIED before 34-VERIFICATION.md records passing checks"
    status: resolved
    verification: "ledger closure in Task 2 occurred only after Task 1 verification PASS recorded"
  - statement: "MUST NOT overwrite a concurrently edited ledger"
    status: resolved
    verification: "pre-write SHA-256 matched ledger_post_34_01_sha256"
  - statement: "MUST NOT mint a new status enum, verdict value, or AC-ID scheme"
    status: resolved
    verification: "ledger uses only PENDING/IN_PROGRESS/FIX_APPLIED/VERIFIED/DEFERRED and reserved AC-LOOP-01/02/04/05/06 IDs"
  - statement: "MUST NOT touch Phase-33/35-owned rows, D-04, or non-LOOP rows; MUST NOT re-litigate any verdict"
    status: resolved
    verification: "D-04, M15, NS-12/13/18, and Phase-33 rows unchanged; verdicts preserved"
  - statement: "MUST NOT declare Phase 34 complete over OPEN GAP-34-01"
    status: enforced
    verification: "closure-gating record in STOP Gap Completeness + Overall Verdict"
  - statement: "MUST NOT edit framework specs, frozen/read-only reports, live pinn/ code, or .planning/STATE.md"
    status: resolved
    verification: "git diff shows only 34-VERIFICATION.md, 32-ISSUE-LEDGER.md, and 34-05-SUMMARY.md; forbidden paths empty"
---

# Phase 34: Training-Loop & Batch-Construction Contracts — Goal-Backward Verification

**Phase Goal (ROADMAP.md):** `ctl_instruction.md` / `pinn_architecture.md` carry the training-loop and batch-construction contracts as normative spec contracts — replay/lookahead batch construction, two independent point sets, mixed time sampling, merged gradient clipping, the ALM update with `μ_p` clamp, `dt_out`-aware collocation scaling, and the training-side use of the v1.5-provisional metrics — each reconciled with the Phase 32 verdicts and the locked v1.4/v1.5 conventions.

**Verified:** 2026-06-25T07:30:00Z
**Status:** passed-with-closure-gate
**Verifier:** Claude (gsd-executor-34-05, deterministic structural/source-token review)

**Scope:** v1.6 specwork-only under the CRITICAL-GOVERNANCE STOP protocol. Only `ctl_instruction.md` and `pinn_architecture.md` may be edited among framework specs (SCOPE-13).

---

## Goal Achievement

### Observable Truths (ROADMAP Phase 34 Success Criteria → LOOP-01..08 + SI-PINN-003)

| # | Truth (ROADMAP SC / LOOP ID) | Status | Evidence |
|---|---|---|---|
| 1 | LOOP-01 replay/lookahead batch construction is defined (`B_replay=240`, `B_lookahead=16`, `has_stage(k+1)` guard) per B-07; causal-mode kept as compatibility-only (D-04 deferred to Phase 35); edge cases (final stage / undersized lookahead / replacement) recorded as owner-pending GAP-34-01 | ✓ VERIFIED | `ctl_instruction.md:1787-1799` Phase 34 contract callout; `B_replay=240`, `B_lookahead=16`, `has_stage(k+1)` present; tagged `provisional`; `evidence/b-07-replay-lookahead-batching.md` linked. No causal mode locked. |
| 2 | LOOP-02 two-independent-point-set contract defined (data-fidelity snapshots vs collocation points, single forward pass allowed, `8192/4096` provisional/example budgets); LOOP-03 mixed sampling reconciled (data-fidelity 50/50 retained, collocation 50/50 deferred, not mandated) | ✓ VERIFIED | `ctl_instruction.md:1801-1818` LOOP-02/03 callouts; `data-fidelity` / `collocation` / `provisional` / `deferred` tokens present; `evidence/b-08-data-vs-collocation-points.md` linked. ROADMAP "applied to both sets" wording superseded by adjudicated B-08 deferral. |
| 3 | LOOP-04 merged gradient clipping defined — `clip_value = C_stage · median(...)` mechanism canonical in `pinn_architecture.md` §4.4, C-schedule `7-10 / 5 / 3` canonical in `ctl_instruction.md`; `8.5` absent both; bidirectional `AC-LOOP-04` anchors resolve | ✓ VERIFIED | `pinn_architecture.md:714-728` mechanism callout + formula; `ctl_instruction.md:1825-1849` C-schedule callout + table; `8.5` absent both files; `AC-LOOP-04` in both. `evidence/m14-gradient-clipping.md` linked. |
| 4 | LOOP-05 ALM parameter-update contract defined at deferred status — dense-residual ALM rejected from default loss, `μ_p` clamp `[1e-4,100]` carried as optional/conditional only | ✓ VERIFIED | `pinn_architecture.md:674` Phase 34 contract callout; `ALM`, `optional`, `deferred` tokens present; forbidden strings "dense-residual ALM in the default loss" / "ALM is enabled by default" absent. `evidence/alm-mu-p-clamp.md` linked. |
| 5 | LOOP-06 `dt_out`-aware collocation scaling realized-as-deferred — candidate direction only, no probe-able formula, inverse form explicitly not adopted | ✓ VERIFIED | `ctl_instruction.md:1819-1823` Phase 34 contract callout; `realized-as-deferred` / `deferred` tokens present; no `n_col = ...` formula assignment. `evidence/m16-dt-out-collocation-scaling.md` linked. |
| 6 | LOOP-07 IPR/PSC training-side roles carried provisionally with VAL-03/VAL-04 forward-references | ✓ VERIFIED | `ctl_instruction.md:770` Phase 34 contract callout; `IPR`, `PSC`, `provisional`, `VAL-03`, `VAL-04` tokens present. |
| 7 | LOOP-08 SASD training-side collocation-weighting role carried provisionally with VAL-02 forward-reference | ✓ VERIFIED | `ctl_instruction.md:684` Phase 34 contract callout; `SASD`, `provisional`, `VAL-02` tokens present. |
| 8 | SI-PINN-003 batch-construction inconsistency reconciled — `ctl_instruction.md` canonical, `pinn_architecture.md` references it, author-comment inconsistency removed, RESOLVED log present | ✓ VERIFIED | `pinn_architecture.md:351` points to ctl canonical; `:1042-1045` RESOLVED log; "is not consistent with the CTL instruction plan" absent from pinn. |

**Score:** 9/9 truths verified (0 present-behavior-unverified).

### ROADMAP Staleness Note

The ROADMAP Phase 34 Success Criteria carry preview wording that predates the SPEC correction (commit `0ffa3d8`):
- SC 2: "applied to **both** point sets" — superseded by the adjudicated B-08 deferral; LOOP-03 records data-fidelity 50/50 retained and collocation 50/50 **deferred**.
- SC 3: "stages 0-1: **8.5**" — superseded by the M14 `accept-resolution` verdict; `8.5` is NOT canonized, only the `7-10 / 5 / 3` schedule is preserved.
- SC 4: "`n_col ∝ dt_base/dt_out` verbatim direction" — superseded by the M16 `defer` verdict; the direction is recorded only as a **deferred candidate**, not a transcribed/probe-able contract.

The adjudicated verdicts in `34-SPEC.md`, `03-final-resolution.md`, and the Phase-32 ledger govern where they diverge. ROADMAP reconciliation is deferred to Phase 36 (Phase 34 SCOPE-13 does not include editing `.planning/ROADMAP.md`).

---

## Requirements Coverage (LOOP-01..08 + SI-PINN-003)

Cross-reference against `.planning/REQUIREMENTS.md` LOOP-01..08 + SI-PINN-003 and the Phase 34 PLAN `requirements` fields:

| Requirement | REQUIREMENTS.md description (abridged) | Plan coverage | Spec status | Ledger status |
|---|---|---|---|---|
| LOOP-01 | Replay/lookahead batch construction (B_replay/B_lookahead/has_stage) | 34-01, 34-03, 34-05 | ✓ SATISFIED | B-07 row VERIFIED (AC-LOOP-01) |
| LOOP-02 | Two-independent-point-set contract | 34-01, 34-03, 34-05 | ✓ SATISFIED | B-08 row VERIFIED (AC-LOOP-02) |
| LOOP-03 | Mixed time sampling (data 50/50 retained, collocation 50/50 deferred) | 34-01, 34-03, 34-05 | ✓ SATISFIED | covered by B-08 row (AC-LOOP-02) |
| LOOP-04 | Merged gradient clipping (single canonical home) | 34-01, 34-02, 34-05 | ✓ SATISFIED | M14 row VERIFIED (AC-LOOP-04) |
| LOOP-05 | ALM parameter update / μ_p clamp (deferred) | 34-01, 34-04, 34-05 | ✓ SATISFIED | ALM μ_p clamp row VERIFIED (AC-LOOP-05) |
| LOOP-06 | dt_out-aware collocation scaling (realized-as-deferred) | 34-01, 34-03, 34-05 | ✓ SATISFIED | M16 row VERIFIED (AC-LOOP-06) |
| LOOP-07 | Training-side IPR/PSC roles (provisional) | 34-01, 34-03, 34-05 | ✓ SATISFIED | no dedicated ledger row (provisional carry-forward) |
| LOOP-08 | SASD training-side collocation-weighting (provisional) | 34-01, 34-03, 34-05 | ✓ SATISFIED | no dedicated ledger row (provisional carry-forward) |
| SI-PINN-003 | Reconcile pinn/ctl batch-construction inconsistency | 34-01, 34-02, 34-03, 34-05 | ✓ SATISFIED | reconciled, RESOLVED log in pinn |

**Orphaned requirements:** None. All nine IDs declared in REQUIREMENTS.md for Phase 34 appear in at least one Phase 34 PLAN `requirements` field.

---

## 1. Planning Artifact Coverage — PASS

Commands run:

```bash
test -f .planning/phases/34-training-loop-batch-construction-contracts/34-SPEC.md
test -f .planning/phases/34-training-loop-batch-construction-contracts/34-CONTEXT.md
test -f .planning/phases/34-training-loop-batch-construction-contracts/34-RESEARCH.md
python3 - <<'PY'
from pathlib import Path
root = Path(".planning/phases/34-training-loop-batch-construction-contracts")
plans = sorted(root.glob("34-*-PLAN.md"))
assert plans
required = ["LOOP-01","LOOP-02","LOOP-03","LOOP-04","LOOP-05","LOOP-06","LOOP-07","LOOP-08","SI-PINN-003"]
missing = [req for req in required if req not in "\n".join(p.read_text() for p in plans)]
assert not missing, missing
PY
```

Result: all three artifacts FOUND; all nine requirement IDs appear across the `34-*-PLAN.md` set.

---

## 2. Framework-Spec Contract Tokens — PASS

Command run (matches `34-VALIDATION.md`):

```python
from pathlib import Path
ctl = Path("pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md").read_text()
pinn = Path("pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md").read_text()
checks = {
    "LOOP-01 replay/lookahead (ctl)": (ctl, ["B_replay", "B_lookahead", "has_stage", "provisional"]),
    "LOOP-02 two point sets (ctl)":   (ctl, ["collocation", "data-fidelity", "provisional"]),
    "LOOP-03 mixed sampling (ctl)":   (ctl, ["50/50", "deferred"]),
    "LOOP-04 mechanism (pinn §4.4)":  (pinn, ["C_stage", "median", "AC-LOOP-04"]),
    "LOOP-05 ALM optional (pinn)":    (pinn, ["ALM", "optional", "deferred"]),
    "LOOP-06 M16 deferred (ctl)":     (ctl, ["realized-as-deferred", "deferred"]),
    "LOOP-07 IPR/PSC (ctl)":          (ctl, ["IPR", "PSC", "provisional", "VAL-0"]),
    "LOOP-08 SASD (ctl)":             (ctl, ["SASD", "provisional", "VAL-02"]),
    "SI-PINN-003 reconciled (pinn)":  (pinn, ["RESOLVED", "ctl_instruction"]),
}
```

Result: `CONTRACT-TOKENS: PASS`. Every discriminating token is present; these phrases were introduced by Phase 34 and would fail against pre-Phase-34 boilerplate.

---

## 3. LOOP-04 Cross-File Consistency Suite (a)-(e) — PASS

Command run (whitespace-tolerant, word-boundary anchored):

```python
import re
from pathlib import Path
ctl = Path("pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md").read_text()
pinn = Path("pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md").read_text()
assert not re.search(r'\b8\.5\b', ctl) and not re.search(r'\b8\.5\b', pinn)
assert 'AC-LOOP-04' in ctl and 'AC-LOOP-04' in pinn
assert len(re.findall(r'clip_value\s*=\s*C_stage', pinn)) >= 1
assert not re.search(r'clip_value\s*=\s*C_stage', ctl)
assert len(re.findall(r'7\s*[\-–—]\s*10', ctl)) == 1
assert re.search(r'\|\s*5\s*\|', ctl)
assert re.search(r'\|\s*3\s*\|', ctl)
```

Result: `LOOP-04-SUITE: PASS`.
- (a) `clip_value = C_stage·median(...)` mechanism canonical in `pinn_architecture.md` §4.4; zero occurrences in `ctl_instruction.md`.
- (b) `8.5` absent from both files; `7-10 / 5 / 3` C-schedule present in ctl.
- (c) Bidirectional `AC-LOOP-04` anchors resolve in both files.
- (d) No duplication: mechanism one home in pinn, schedule one home in ctl; `5` and `3` survive only as right-aligned C-schedule table cells.
- (e) Status-tag parity: structure locked (`C_stage` schedule locked in ctl, mechanism locked in pinn); deferred constants (exact early-stage `C`, bootstrap, lower floor, history-reset) are FUT-routed in both halves, not tagged locked.

**Win-condition judgment:** the merged contract is recoverable as one coherent rule from the two cross-referenced halves with zero duplicated normative text.

---

## 4. Negative / Owner-Pending Checks — PASS

Command run:

```python
from pathlib import Path
ctl = Path("pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md").read_text()
pinn = Path("pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md").read_text()
assert not re.search(r'\b8\.5\b', ctl) and not re.search(r'\b8\.5\b', pinn)
assert not re.search(r'n_col\s*=\s*(?:dt_|n_|C_|\d|[a-z]+\s*/\s*)', ctl)
for forbidden in ["dense-residual ALM in the default loss", "ALM is enabled by default"]:
    assert forbidden not in pinn
assert "is not consistent with the CTL instruction plan" not in pinn
```

Result: `NEGATIVE-CHECKS: PASS`.
- `8.5` absent both files.
- No probe-able `n_col = ...` formula assignment in ctl (LOOP-06 deferred).
- Forbidden ALM default-loss strings absent from pinn.
- SI-PINN-003 author-comment inconsistency string gone from pinn.

---

## 5. Locked-Convention / locked-convention Regression Guard (SCOPE-12) — PASS

Command run:

```python
import subprocess, re
from pathlib import Path
ctl = Path("pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md").read_text()
pinn = Path("pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md").read_text()
head_ctl = subprocess.check_output(
    ["git", "show", "HEAD:pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md"]
).decode()
assert ctl.count("6.694") <= head_ctl.count("6.694")
assert "6.694" not in pinn
assert "4.6416" in ctl
current_pipe = set(re.findall(r'PIPE-\d+', ctl))
head_pipe = set(re.findall(r'PIPE-\d+', head_ctl))
current_val = set(re.findall(r'VAL-\d+', ctl))
head_val = set(re.findall(r'VAL-\d+', head_ctl))
assert head_pipe <= current_pipe
assert head_val <= current_val
```

Result: `LOCKED-CONVENTION: PASS`.
- `D ~= 4.6416` present in ctl; `6.694` absent from pinn.
- No NEW active-convention `6.694` in ctl vs HEAD (rejected-provenance occurrences preserved per SCOPE-12/EVID-10).
- PIPE/VAL references unregressed: no reference present at HEAD was removed by Phase 34. (PIPE-01/02/05/10 and VAL-01 were not present at baseline; they are not treated as regressions.)
- Core locked conventions intact: 14D `[τ, IC₁₃]`, Jacobi mass-weighted COM projection head, `eps_soft = 1e-5` / `epsilon_train = 1e-5`, post-v1.3 SCS gate.

---

## 6. Forbidden-Path Status Guard (SCOPE-08/09/13 + no-live-code) — PASS

Command run:

```bash
git diff --name-only -- \
  pinn_instruction/markdown_conversion/framework-specs/sampling_method.md \
  pinn_instruction/markdown_conversion/framework-revisions/data_quality_assessment.md \
  pinn_instruction/markdown_conversion/framework-revisions/review-of-framework/review_of_framework.md \
  pinn_instruction/markdown_conversion/framework-revisions/stage-strat-revision/stage_strat_revision.md \
  pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md \
  pinn/

git ls-files --others --exclude-standard -- \
  pinn_instruction/markdown_conversion/framework-specs/sampling_method.md \
  pinn_instruction/markdown_conversion/framework-revisions/data_quality_assessment.md \
  pinn_instruction/markdown_conversion/framework-revisions/review-of-framework/review_of_framework.md \
  pinn_instruction/markdown_conversion/framework-revisions/stage-strat-revision/stage_strat_revision.md \
  pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md \
  pinn/
```

Result: both tracked-diff and untracked outputs EMPTY. Only `ctl_instruction.md` and `pinn_architecture.md` changed among framework files.

---

## 7. Dirty-Doc / STATE.md Preservation — PASS WITH DOCUMENTED DIVERGENCE

Command run:

```python
import subprocess, re, hashlib
from pathlib import Path
base = Path(".planning/phases/34-training-loop-batch-construction-contracts/34-BASELINE-CAPTURED").read_text()
paths = re.findall(r'dirty_doc_path=(.+)', base)
want = re.search(r'dirty_docs_sha256=([0-9a-f]+)', base).group(1)
got = hashlib.sha256(subprocess.check_output(["git", "diff", "--"] + sorted(paths))).hexdigest()
```

Result: `DIRTY-DOC: PASS-DOCUMENTED-DIVERGENCE`.
- Baseline `dirty_docs_sha256 = 0db058e4...` (captured when `.planning/STATE.md` was dirty).
- Current combined diff SHA-256 is `e3b0c442...` (empty diff).
- The captured dirty-doc set contains only `.planning/STATE.md`, which is now clean (no diff). This is the expected outcome of Wave 1-3 tracking writes delegating STATE.md updates, not a protected-path violation.
- Independent per-path confirmation: `.planning/STATE.md` is byte-identical to its committed state; no user-owned protected doc outside the captured set was modified.

This follows the same documented-divergence pattern as `33-VERIFICATION.md` §8.

---

## 8. STOP Gap Completeness — PASS (GAP-34-01 OPEN, closure-gated)

Command run:

```python
from pathlib import Path
phase_gap = Path(".planning/phases/34-training-loop-batch-construction-contracts/34-GAPS.md")
milestone_gap = Path(".planning/milestones/v1.6-GAPS.md")
required = [
    "Decision point","Where in artifact","Task context","Classification",
    "Source silence","Mathematical / engineering grounding","Agent was tempted to",
    "What the user needs to decide","Confidence of impact","Status",
]
txt = phase_gap.read_text()
missing = [t for t in required if t not in txt]
assert not missing, missing
assert "GAP-34-01" in milestone_gap.read_text()
```

Result: `STOP-GAP-COMPLETENESS: PASS`.
- `GAP-34-01` carries all required STOP fields.
- Status is `OPEN`.
- Indexed in `.planning/milestones/v1.6-GAPS.md` Phase 34 section.

### Phase-34 Closure Gating

Because `GAP-34-01` is an **OPEN owner-pending STOP gap**, Phase-34 closure is **GATED** on the user resolving it (`RESOLVED-WITH-INSTRUCTION`) or explicitly deferring it (`DEFERRED`) per the AGENTS.md STOP protocol ("a phase may not close with an unresolved gap unless the user explicitly resolves or defers it"). The source-silent batch edge cases (final-stage `has_stage(k+1)`=false, undersized next-stage lookahead pool <16, replacement policy) are NOT filled with an invented default. Phase 34 must not be declared fully complete until this gap is resolved or deferred.

### Phase-34 Closure-Gate Update (2026-06-26, Plan 34-06)

**Gate CLEARED.** `GAP-34-01` was resolved `RESOLVED-WITH-INSTRUCTION` on 2026-06-25 — the owner ratified **Option A** via AskUserQuestion during the Phase 34 UAT (`/gsd-verify-work 34`): final stage trains replay-only; an undersized look-ahead pool (<16) is padded by sampling **with** replacement (batch size fixed at `B_replay + B_lookahead = 240 + 16`); replay is sampled **without** replacement across the epoch. The ratified policy was transcribed into the `ctl_instruction.md` Mini-Batch Construction LOOP-01 contract (provisional tag) by **Plan 34-06**, replacing the prior `owner-pending (GAP-34-01)` callout. The LOOP-04 (a)-(e) cross-file suite and the locked-convention regression guard re-passed after the ctl batch (see `34-06-SUMMARY.md`). The frontmatter `status` is updated `passed-with-closure-gate → passed` and `gaps_remaining → []`. The original 2026-06-25T07:30 verification body above is preserved as the historical record. STATE.md / ROADMAP.md advancement remains with the user (D-34-18).

---

## 9. Phase-32 Ledger Closure — PASS

Pre-write freshness check (concurrency guard):

```python
import hashlib
from pathlib import Path
lp = Path(".planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md")
base = Path(".planning/phases/34-training-loop-batch-construction-contracts/34-BASELINE-CAPTURED").read_text()
want = [l.split("=")[1] for l in base.splitlines() if "ledger_post_34_01_sha256=" in l][0]
got = hashlib.sha256(lp.read_bytes()).hexdigest()
assert got == want, f"ledger drift: got {got}, want {want}"
```

Result: `LEDGER-FRESHNESS: PASS` — current ledger SHA-256 equals `ledger_post_34_01_sha256` (`0b24619a...`).

After verification, the five LOOP-related rows are closed `VERIFIED` with preserved verdicts:

| Finding row | AC ID | Consuming plan | Transition | Preserved verdict |
|---|---|---|---|---|
| B-07 | AC-LOOP-01 | 34-03 (ctl LOOP-01) | `IN_PROGRESS → FIX_APPLIED → VERIFIED` | `accept-resolution` |
| B-08 | AC-LOOP-02 | 34-03 (ctl LOOP-02/03) | `IN_PROGRESS → FIX_APPLIED → VERIFIED` | `accept-resolution` |
| M16 | AC-LOOP-06 | 34-03 (ctl LOOP-06 deferral body) | `IN_PROGRESS → FIX_APPLIED → VERIFIED` | `defer-with-blocker` |
| ALM μ_p clamp | AC-LOOP-05 | 34-04 (pinn §4.2 ALM body) | `IN_PROGRESS → FIX_APPLIED → VERIFIED` | `defer-with-blocker` |
| M14 | AC-LOOP-04 | 34-02 (pinn §4.4 mechanism + ctl C-schedule) | `PENDING → FIX_APPLIED → VERIFIED` | `accept-resolution` (existing Phase-32) |

No new status enum or AC-ID scheme was minted. D-04, the Phase-33-owned rows, and the Phase-35-owned rows (M15/NS-12/NS-13/NS-18) remain unchanged.

---

## 10. Behavioral Spot-Checks

Specwork-only phase: no runnable code, no tests to run, no probes. Spot-checks SKIP with reason "specwork-only; no runnable entry points this phase." All verification is source-token, structural, and grounding-trace evidence (the appropriate verification modality for spec-transcription phases under the STOP protocol).

No EDA, Stage-0 pilot, training run, package install, schema push, or UI check was executed.

---

## 11. Anti-Patterns / Stubs

Scan of the modified framework specs found no load-bearing stubs (no hardcoded empty values flowing to rendering, no placeholder text, no TODO/FIXME in the transcribed contract bodies). The `n_col ∝ dt_base/dt_out` candidate direction in LOOP-06 and the edge-case policy in GAP-34-01 are intentionally deferred with explicit deferral tags/citations, not silent stubs.

---

## 12. Prohibition Compliance

All Plan 34-05 `prohibitions` entries are satisfied (see frontmatter and sections above):
- Ledger closure followed verification (T-34-18 mitigated).
- Pre-write ledger freshness check passed (T-34-19 mitigated).
- No new enum/verdict/AC-ID scheme minted (T-34-23 mitigated).
- Non-LOOP rows untouched, no verdict re-litigated.
- Phase 34 not declared complete over OPEN GAP-34-01 (T-34-22 mitigated).
- No framework spec, frozen/read-only report, live `pinn/` code, or `.planning/STATE.md` modified by this plan (T-34-20, T-34-21 mitigated).

---

## Overall Verdict (goal-backward)

**Status: passed-with-closure-gate.** Phase 34 achieved its ROADMAP goal for all nine requirements: `ctl_instruction.md` and `pinn_architecture.md` carry the training-loop and batch-construction contracts at their adjudicated verdicts and statuses, reconciled with the Phase 32 issue ledger and the locked v1.4/v1.5 conventions. The LOOP-04 cross-file split has exactly one canonical home per half with bidirectional `AC-LOOP-04` anchors. The five LOOP-related Phase-32 ledger rows are closed `VERIFIED` with preserved verdicts. The forbidden-path invariant holds, and `.planning/STATE.md` is preserved (its dirty→clean transition is a documented Wave 1-3 tracking-write divergence, not a protected-path violation).

**Closure gate:** Phase 34 is NOT declared fully complete because `GAP-34-01` (LOOP-01 source-silent batch edge cases) remains OPEN. Completion is gated on the user resolving or deferring that gap per AGENTS.md.

---

_Verified: 2026-06-25T07:30:00Z_
_Verifier: Claude (gsd-executor-34-05)_


## Re-verification — v1.6 closure (2026-07-02)

Re-confirmed verdict: **passed** (status unchanged).
Basis: goal-backward re-check re-ran the VERIFICATION.md deterministic suites (Sections 2–5: contract tokens, LOOP-04 cross-file single-home suite, negative/owner-pending checks, locked-convention regression guard) against the current `ctl_instruction.md` and `pinn_architecture.md` — all PASS; confirmed all five evidence packets exist in `evidence/`, GAP-34-01 is `RESOLVED-WITH-INSTRUCTION`, the LOOP-04 `8.5`-absent / `7-10 / 5 / 3` single-home and `AC-LOOP-04` bidirectional anchors hold, and `4.6416`/`6.694`-absent (pinn) locked conventions are intact. The only framework-spec commits since the 2026-06-25 verification are Phase 35 downstream work; no Phase-34 contract regressed.
Timestamp refresh: this re-verification refreshes VERIFICATION.md mtime relative to SUMMARY.md, resolving the stale-verification false-positive flagged by init.manager.
