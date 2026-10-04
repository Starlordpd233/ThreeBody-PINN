---
status: active
purpose: verification-report
created: 2026-10-04
milestone: untracked
phase: cross-cutting
retirement_trigger: the trainex-r4 round is consumed — its reports are verified (Rule 19), consolidated, and the owner has ruled on the decision sheet
---

# trainex-r4 package audit (pre-handoff)

**What this is.** This is the self-audit of the trainex-r4 External Research
Workflow package before it is handed to external agents. The package was
assembled 2026-10-04 as a standalone round (owner decision), routed by the
v2.3 `rethink` verdict (`.planning/phases/58-verdict-traceability-close/58-VERDICT.md`).

**What was audited.** The package root
`pinn_instruction/markdown_conversion/framework-specs/trainex-r4/` (five
authored or assembled files plus `research_results/.gitkeep`), against the
baseline commit `735e2ae8d5ec30b9915ec9172ac06965fbaa8afb`.

**Verdict.** All checks pass. The package is ready for handoff. Four facts
surfaced during assembly are worth the owner's attention before handoff; they
are listed under "Findings" and recorded in the package as evidence, not
resolved.

## Results

| Check | Result | Evidence |
|---|---|---|
| Bar A: scoped lexical ban on the master's own voice (§0–§8) | **PASS**: no line in the `NEUTRALITY-BAN` region matches the ten banned terms | audit script below |
| Bar A2: the ERW Rule-7 vocabulary is present in the output contract (§9) | **PASS**: 6 matching lines (at least 4 required) | audit script below |
| Bar B: the five questions are the verdict packet's §6 verbatim | **PASS**: 5 of 5 identical after line-break normalization | audit script below |
| Bar C: read-only boundary | **PASS**: the package commit touches only the round root and this report; no framework spec, `pinn/`, `configs/`, `runs/`, or `tests/` path changes | `git diff --cached --stat` at commit time |
| Bar D: pin consistency | **PASS**: `source_baseline` is `735e2ae8…` in the master, prompt, delivery note, and both bundles | audit script below |
| Bar E: bundle fidelity | **PASS**: <ul><li>20 verbatim blocks (11 in `specs/framework-specs-bundle.md`, 9 in `research_package/v2.3-closure-evidence-bundle.md`) are byte-identical to `git show 735e2ae8:<path>`, or its `sed -n` range for heading-bounded excerpts;</li><li>the derived digest's embedded script hashes to `12dd87f6b805200c1d009b3ee3079f90c02c36c0e027b09dee4ba6c2cd6fb09d`;</li><li>a fresh run of that script reproduces the embedded output byte-for-byte.</li></ul> | independent parser over the BEGIN/END markers, separate from the scripts that built the bundles |
| Bar F: citation resolution | **PASS**: all 20 `path:line` citations in the master resolve at the baseline. Each cited line was read and carries the attributed content | list below |
| Bar G: attachment cap | **PASS**: 3 attachments (cap 5), all present | audit script below |

**Bar F, resolved citations** (first line of each range, at `735e2ae8`):

| Citation | First line |
|---|---|
| `pinn/training/config.py:574` | `n_adam: Optional[int] = None  # T_max = N_Adam,k` |
| `pinn/training/controllers.py:483-507` | `def _build_gradient_stats(` |
| `pinn/training/controllers.py:1058`, `:1241`, `:1974` | `[n for n, w in enumerate(w_n_list) if w > 0.5], …` (monitor, training batch, microbatched path) |
| `pinn/training/controllers.py:1993-2009` | `gradient_stats: dict[str, Any] = {` |
| `pinn/training/controllers.py:2040-2042` | `handoff_trigger = "budget-exhausted"` |
| `pinn/training/controllers.py:2169` | `fires = plateau.update(float(loss_terms.phys.detach()))` |
| `pinn/training/controllers.py:2201` | `handoff_trigger = "plateau"` |
| `pinn/training/controllers.py:2658-2660` | `scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(` |
| `ctl_instruction.md:1803` | `- Set initial learning rate: $\text{LR}_k = 10^{-3} \times (0.7)^k$.` |
| `ctl_instruction.md:1805` | `- Initialize a cosine annealing scheduler to decay the learning rate` |
| `ctl_instruction.md:1894` | `Hand off to L-BFGS when the physics loss plateaus:` |
| `ctl_instruction.md:1994-1997` | the `MAX_EPOCHS` … **claimed-unverified** … provisional sentence |
| `pinn_architecture.md:181` | `` `first_omega_0` is fixed at `30` and is not scheduled during training. `` |
| `pinn_architecture.md:188` | the Phase 56 `first_omega_0` NOT AMENDED contract |
| `pinn_architecture.md:452`, `:454`, `:456` | the three Phase 56 §3.2 contract blocks |
| `pinn_architecture.md:699-701` | the `I_warm` / `λ_phys` warmup and `λ_phys^max = 1` **[LOCKED]** |

## Findings surfaced during assembly

These are facts, recorded in the master's claims register for the external
agents to test. None is resolved here, and none changes the five questions.

1. **Generations 6 and 7 are not independent runs.**
   - **What was found:** they share seed 42 and the configuration apart from
     `run.run_name`. Their logged values are identical through step 8, differ
     only in the seventh or eighth significant figure from step 9, agree to
     three figures through step 200, and differ visibly by step 300.
   - **What it bears on:** the verdict packet's §4 calls them "two independent
     runs".
   - **Where it is recorded:** master `F-13`, with the packet's reading listed
     as challengeable (`H-02`). The packet itself is not edited; it is
     reproduced verbatim as evidence.
2. **The locked specs do not define the causal front.**
   - **What was found:** `front_idx`, its `0.5` threshold, and invariant B's
     500-step window come from code and owner rulings, not from
     `pinn_architecture.md` or `ctl_instruction.md`.
   - **Where it is recorded:** master `F-10`.
3. **The IC loss term dominates the logged loss and gradient.**
   - **What was found:**
     - The IC term ranged from 84 to about `8 × 10⁴` across the tabulated
       steps, against a normalized physics term of 0.07–0.19.
     - On the 19 steps with complete gradient statistics, the applied IC
       gradient norm exceeded the applied physics gradient norm by
       `2.8 × 10⁴` to `2.6 × 10⁶`.
   - **What it bears on:** the recalibration ruling's own reasoning
     (point 2) expected the normalization to address a physics/data
     conditioning mismatch.
   - **Where it is recorded:** master `F-07`, `F-08`, and `H-01`.
4. **The schedule length is tied to the configured Adam budget.**
   - **What was found:** the spec says to decay the learning rate "over the
     phase" and to hand off to L-BFGS at a physics-loss plateau. The code sets
     the cosine length, and the physics warmup length, from
     `n_adam = 1000`.
   - **What it bears on:** the spec itself calls the per-stage epoch budget
     provisional.
   - **Where it is recorded:** master `F-04`, `F-05`, `F-06`, `F-15`.

## Scope attestation

- **What was written:** only files under the round root, plus this report.
- **What was not edited:** the reproduced source documents (verdict,
  rulings, verdict packet, run records, configs, logs).
- **What was not done:** no training run, no evaluation, and no
  framework-spec edit.
- **Telemetry digest:** the one derived component. It read the Git-tracked
  logs only and wrote nothing.

The verdict packet
(`docs/work/designs/milestone_v2.3/58-verdict-traceability-close/2026-10-03-phase-58-diag-06-verdict-packet.md`)
stays `status: active`. trainex-r4 reproduces and cites it as evidence until
the round is consumed.

## Audit script (exact text)

Run from the repository root as `python3 r4_audit.py 735e2ae8d5ec30b9915ec9172ac06965fbaa8afb`.
SHA-256 `d840a9685c714fb0e4ecd93b384a1bf4d238a49ab7398ce7e6534f3e53edb78a`.
Bars C and E are checked separately, as described in the results table.

```python
import re, subprocess, sys
from pathlib import Path
BASE = sys.argv[1]
R = Path("pinn_instruction/markdown_conversion/framework-specs/trainex-r4")
M = (R / "research_package/RESEARCH-CONTEXT-MASTER.md").read_text()
def sh(c): return subprocess.run(c, shell=True, capture_output=True, text=True).stdout
# Bar A
region = M[M.index("<!-- NEUTRALITY-BAN-BEGIN -->"):M.index("<!-- NEUTRALITY-BAN-END -->")]
ban = re.compile(r"recommend|suggest|prefer|best|most likely|primary candidate|default to|should use|ranked|leading option", re.I)
hits = [l for l in region.splitlines() if ban.search(l)]
print("BAR-A", "PASS" if not hits else f"FAIL {hits}")
# Bar A2
s9 = M[M.index("## 9. Output contract"):M.index("## 10.")]
n = sum(1 for l in s9.splitlines() if re.search(r"suggested default|one-way|two-way|decision sheet", l, re.I))
print("BAR-A2", "PASS" if n >= 4 else "FAIL", n)
# Bar B: questions verbatim vs packet §6
pk = sh(f"git show {BASE}:docs/work/designs/milestone_v2.3/58-verdict-traceability-close/2026-10-03-phase-58-diag-06-verdict-packet.md")
sec6 = pk[pk.index("## 6. Open questions"):pk.index("## 7. Evidence index")]
bullets = [" ".join(b.split()) for b in re.findall(r"^- (.*?)(?=^- |^\n|\Z)", sec6, re.S | re.M)]
quoted = [" ".join(q.split()) for q in re.findall(r'^\*"(.*?)"\*$', M, re.S | re.M)]
print("BAR-B", "PASS" if quoted == bullets[:5] and len(quoted) == 5 else "FAIL", len(quoted), len(bullets))
for q, b in zip(quoted, bullets):
    if q != b: print("  MISMATCH:", q, "|", b)
# Bar D: pin consistency
files = [R/"research_package/RESEARCH-CONTEXT-MASTER.md", R/"research_package/RESEARCH-AGENT-PROMPT.md", R/"DELIVERY-NOTE.md", R/"specs/framework-specs-bundle.md", R/"research_package/v2.3-closure-evidence-bundle.md"]
pins = {str(f.name): set(re.findall(r"source_baseline: ([0-9a-f]{40})", f.read_text())) for f in files}
ok = all(p == {BASE} for p in pins.values())
print("BAR-D", "PASS" if ok else "FAIL", pins)
# Bar F: citation resolution. Within each line, a backticked `path:N[-M]` sets the
# current file; a following backticked `:N[-M]` cites that same file. Bare spec names
# resolve to the live spec directory.
SPEC_DIR = "pinn_instruction/markdown_conversion/framework-specs/"
cites = set()
for line in M.splitlines():
    cur = None
    for tok in re.findall(r"`([^`]+)`", line):
        m = re.fullmatch(r"([\w./-]+\.(?:py|md|yaml|json)):(\d+)(?:-(\d+))?", tok)
        if m:
            path = m.group(1)
            if "/" not in path:
                path = SPEC_DIR + path
            cur = path
            cites.add((cur, int(m.group(2)), int(m.group(3) or m.group(2))))
            continue
        m = re.fullmatch(r":(\d+)(?:-(\d+))?", tok)
        if m and cur:
            cites.add((cur, int(m.group(1)), int(m.group(2) or m.group(1))))
bad = []
for path, a, b in sorted(cites):
    n = int(sh(f"git show {BASE}:{path} | wc -l").strip() or 0)
    if n < b: bad.append((path, a, b, n))
print("BAR-F", "PASS" if not bad else f"FAIL {bad}", f"{len(cites)} path:line citations resolved")
for path, a, b in sorted(cites):
    print(f"  {path}:{a}-{b} ::", sh(f"git show {BASE}:{path} | sed -n '{a}p'").strip()[:110])
# Bar G: attachment cap
P = (R / "research_package/RESEARCH-AGENT-PROMPT.md").read_text()
hdr = P[:P.index("\n---\n", P.index("## FOR THE USER"))]
att = re.findall(r"^\d+\. `([^`]+)`", hdr, re.M)
print("BAR-G", "PASS" if 0 < len(att) <= 5 and all((R / a).exists() for a in att) else "FAIL", att)
```
