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
   - **Corrected later:** the description of how the two runs differ is wrong.
     See the addendum below.
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

## Addendum — re-audit after the pre-handoff corrections (2026-10-04)

**Trigger.** An independent double-check of the package
(`docs/work/reviews/cross_cutting/trainex-r4/2026-10-04-trainex-r4-package-double-check-findings.md`,
committed unchanged in `58fcb079`) reported four findings in the master. Each
finding was re-derived in-repo before anything changed. The owner confirmed
that no agent had received the package, so the attachments were corrected in
place, in `c4887da2`. The sections above are left as the record of the first
audit, except for the pointer added to Findings item 1.

### The review's four findings, assessed

| Finding | Assessment | Action in `c4887da2` |
|---|---|---|
| 1. F-07 `loss_data` lower bound | **Confirmed.** The tabulated minimum is 0.016 at step 931 (unrounded 0.0159758), not 0.0164. | Corrected, written as the digest prints it ("0.016"). |
| 2. F-13 "still 2" for generation 6 | **Confirmed in substance; the proposed wording overstates.** <ul><li>The step 490, 500, and 510 checkpoints (`latest.pt` = 510) record `front_high_water: 2`, `last_advance_step: 353`.</li><li>The verdict packet's replay found the instantaneous front at 1 at those three checkpoints. No checkpoint stores an instantaneous front.</li><li>The process died at step 513 and no record holds the front at 513, so the proposed "had dropped back to 1" at death is not supported.</li></ul> | Restated: high-water 2 at the last checkpoint (510); the replay's instantaneous front was 1 at 490, 500, and 510. |
| 3. Trip values versus step 951 | **Confirmed against the code.** <ul><li>`trip.json` records `step: 951`, the count of completed Adam updates (`pinn/training/controllers.py:2105-2106`).</li><li>The 952nd iteration's forward and backward pass tripped the guard before any update, and it is logged as record 952 with `lr` and `epoch` null (`:2118-2121`).</li><li>Its five loss terms and `grad_norm` equal `trip.json` exactly.</li><li>The review's replication command 3 reads a `step_completed` field the log does not contain, so it would print `True` for both records.</li></ul> | F-01, F-05, F-07, and F-09 clarified. Part G now checks the equality and tabulates record 952. |
| 4. §2 lists `framework-specs-bundle.md` without `specs/` | **Not adopted as proposed.** §2 names all three attachments by their upload names, as trainex-r3's master did. Prefixing only the second would make it inconsistent with the other two. | Added one sentence giving each attachment's repository location. |

### Further corrections found during the assessment

None of these was in the review.

1. **The seed-42 divergence.** This report's Findings item 1, master F-13, and
   the Part G notes all said the two runs differ "in the seventh or eighth
   significant figure from step 9". In fact:
   - every compared field is bit-identical through step 8;
   - at step 9, `w_min` differs in the fifth digit and `loss_phys` in the
     seventh;
   - `loss_ic`, `total`, and `grad_norm` stay bit-identical through step 269;
   - every step from 270 onward differs;
   - the first difference visible at three significant figures is at step
     275.

   Part G's new comparison section prints all of this.
2. **The physics-term range.** Master §4.2 said the physics term "stayed
   between 0.073 and 0.19". The tabulated maximum is 0.192 (step 300), and
   the full-run range is 0.0723 to 0.257.
3. **"Several orders of magnitude."** The prompt used this phrase for the IC
   term's dominance. The smallest ratio of the IC term to the rest of the
   loss is 236.6 (step 947), so the text now says "at least 236 times". The
   digest prints this ratio to four figures, because at three figures it reads
   237 and would have made "at least 237" false.
4. **Tier inconsistency.** Master §1.1 and §4.2 stated the verdict packet's
   "not a near miss" and "flat" readings in the packet's own voice, while §6
   lists them as challengeable (`H-02`). They are now restated as the measured
   sums.
5. **The replay's checkpoint count.** Master §7 Q5 and the Part G notes said
   the replay scored four generation-7 checkpoints; it scored five (steps 0,
   900, 931, 941, 951). §7 also said the run logs record the monitor's
   high-water mark, but they do not; the checkpoints and the terminal record
   do. The Git-tracked TensorBoard file holds per-step training-batch traces:
   its `causal/front_idx` equals the log's batch front at all 952 points, and
   it has no monitor tags.
6. **Learning-rate timing.** The Part G notes now say that `lr` is logged
   after the scheduler steps, so it is the rate for the next update
   (`pinn/training/controllers.py:2162-2185`).

### Re-audit results (after `c4887da2`, baseline `735e2ae8`)

| Check | Result |
|---|---|
| Bar A | **PASS**: no banned term in the master's §0–§8 |
| Bar A2 | **PASS**: 6 lines |
| Bar B | **PASS**: 5 of 5 questions verbatim |
| Bar C | **PASS**: `c4887da2` touches only the round root |
| Bar D | **PASS**: `source_baseline` `735e2ae8…` in all five files |
| Bar E | **PASS**: <ul><li>20 verbatim blocks are byte-identical to `git show 735e2ae8:<path>`, with fenced blocks compared exactly;</li><li>the regenerated digest script hashes to `d28c7d9281dfcc6c8d7ab25538e4e17d8007d5f54cd9c60819dd55223f803065`;</li><li>a fresh run reproduces the embedded output byte-for-byte.</li></ul> |
| Bar F | **PASS**: 21 `path:line` citations resolve at the baseline, adding `pinn/training/controllers.py:2105-2130` |
| Bar G | **PASS**: 3 attachments |

The audit script is unchanged (SHA-256
`d840a9685c714fb0e4ecd93b384a1bf4d238a49ab7398ce7e6534f3e53edb78a`).
None of the reproduced sources changed between `735e2ae8` and `c4887da2`.
