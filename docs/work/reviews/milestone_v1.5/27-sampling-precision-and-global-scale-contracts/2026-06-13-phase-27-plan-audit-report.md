---
status: active
purpose: review-findings
created: 2026-06-13
milestone: v1.5
phase: 27-sampling-precision-and-global-scale-contracts
retirement_trigger: after Phase 27 plan remediation is complete and each finding is closed with evidence (or explicitly waived by the user)
---

# Phase 27 Plan-Set Audit Report

> **Status of this document:** This is the authoritative audit of the Phase 27
> implementation plan-set. It supersedes an earlier same-day preliminary draft of
> this report (uncommitted, authored ~21:48). The earlier draft's seven findings
> are retained here, verified against the live files, and extended with new
> findings surfaced by independent adversarial review. Where verification
> refuted or narrowed a prior claim, that is stated explicitly (see
> "Changes versus the 21:48 draft").

## Scope

Reviewed the Phase 27 execution plan-set scheduled for autonomous execution, plus
the shared support artifacts and the live target files:

- `.planning/phases/27-sampling-precision-and-global-scale-contracts/27-01-PLAN.md` (PIPE-04 / M12 + G5, wave 1)
- `.planning/phases/27-sampling-precision-and-global-scale-contracts/27-02-PLAN.md` (PIPE-07 precision, wave 2)
- `.planning/phases/27-sampling-precision-and-global-scale-contracts/27-03-PLAN.md` (PIPE-08 stage-query, wave 3)
- `.planning/phases/27-sampling-precision-and-global-scale-contracts/27-04-PLAN.md` (PIPE-09 compute_globals, wave 4)
- Shared: `27-VALIDATION.md`, `27-GAPS.md`, `27-SPEC.md`, `27-CONTEXT.md`, `27-RESEARCH.md`
- Evidence packets: `m11-m12-severity.md`, `compute-globals-D.md`, `data05-precision.md`, `evidence/README.md`
- Ledger: `24-ISSUE-LEDGER.md`
- Live targets: `ctl_instruction.md`, `pinn_architecture.md` (read-only verification)

## Method

`compound-engineering:ce-doc-review` (report/headless mode) with three reviewer
personas — `ce-coherence-reviewer` (logical integrity), `ce-feasibility-reviewer`
(operational resilience), and `ce-adversarial-document-reviewer` (execution
clarity / false-green-and-false-red construction) — dispatched in parallel, each
directed to verify every claim against the actual files. A fourth persona
(`ce-scope-guardian-reviewer`) was dispatched but returned no usable output; the
governance/scope axis is covered by the parent's manual analysis (see Coverage).
All persona findings were then re-verified by direct file reads before being
accepted into this report; severity was calibrated against the verified evidence
rather than taken at the persona's assertion.

## Executive Verdict

**Do not hand this plan-set to an autonomous executor unchanged.**

The plan-set is internally disciplined — correct ledger row numbers, correct
verdict-locking, correct same-commit intent, and a sound no-invention posture.
But its **verification architecture cannot reliably detect the failure modes its
own threat register names**, and several required execution steps have no
home in any plan's owned paths. The decisive problems are narrow operational
hazards, not design flaws:

- Two acceptance checks can produce a **false green** that lets a contract
  "land" on a grep that fired on the wrong paragraph (AC-PIPE-04) or a
  **false red** that blocks on text the phase must not touch (AC-PIPE-08).
- Files that *must* mutate during execution (`27-VALIDATION.md` status +
  frontmatter, the `27-0N-SUMMARY.md` artifacts) are owned by **no** plan.
- The `autonomous: true` flag and the mandatory STOP branches are mutually
  contradictory: under autonomous execution there is no defined consumer for a
  surfaced gap.

Three findings are P0 (will fire on the files as they exist today); the
remainder are P1/P2 hazards that compound them.

## Verification highlights (empirical facts confirmed against the live files)

These anchor the findings below and were checked by direct `grep`/`Read`:

1. The AC-PIPE-04 discriminator token `min(n_pts_cap, n_snapshots` **already
   exists** at `ctl_instruction.md:498`, and that line contains the *full* locked
   M12 rule. The intended operative target — the Mini-Batch block at
   `ctl_instruction.md:1417-1430` — still carries the old "50% uniform / 50%
   weighted by acceleration norm" prose (`:1421-1423`).
2. The Mini-Batch block at `ctl:1417-1430` is itself a **training-policy**
   section: `reserve ρ_lookahead (e.g., 5%)` (`:1419`), `| Replay set | B_≤k | 240 |`
   (`:1427`), `| Look-ahead set | B_{k+1} | 16 |` (`:1428`).
3. `ctl_instruction.md:771` (§2.5) reads `E_scale = |median({E_j})| + 10^{-10}`
   (the outlier), while `pinn_architecture.md:761` (§5.2) and
   `ctl_instruction.md:1224` (normalization table) are already `+10^{-8}`. So
   the 27-04 `E_scale` canonicalization is a real 2-of-3 consistency fix and the
   arch §5.2 edit is genuinely **no-change**.
4. There are **~10 legitimate** `1e-10` / `10^{-10}` occurrences in
   `ctl_instruction.md` (Plummer `ε_inv` at 475/858/868/876/1085/1154; default
   args at 899/924; COM/dimensional gates at 963/968) that the AC-PIPE-09
   negative control must **not** flag.
5. Stage-query signatures `sample_replay` / `sample_lookahead` are **absent**
   pre-edit (27-03's discriminator is valid). No operative `0.5 × n_snapshots`
   factor exists anywhere in `ctl_instruction.md` (the AC-PIPE-04 `0.5` negative
   control is currently vacuous).
6. The cited verbatim anchors are **wider than their target**: the locked
   blockquote paragraph is a single line at `m11-m12-severity.md:107` (cited as
   `:105-113`) and `compute-globals-D.md:106` (cited as `:104-108`); the cited
   ranges also include lead-ins, sibling rulings, and "Phase 25 makes zero edits"
   process notes.
7. `compute-globals-D.md:108` *explicitly* delegates `E_scale = 1e-8` to Phase 27
   ("a Phase 27 edit decision (2-of-3 editable-spec choice) … recorded here so
   Phase 27 PIPE-09 can transcribe it without re-deriving"). The **admitted-set
   scope** at `compute-globals-D.md:106` is, by contrast, "a documented minor
   judgment **flagged for spec-author sign-off**."
8. `data05-precision.md:90-93` plus git history show the pointer packet's
   authoring-SHA backfill is already complete (commit `656de848`), so 27-02's
   instruction to "backfill the `<commit-pending>` SHA" is stale; the
   substantive Phase 27 commit SHA still requires the two-phase pattern.

## Findings

### P0 — fix before any execution

#### F-01 [P0] AC-PIPE-04's discriminator is pre-satisfied by `ctl:498`; the "fails pre-edit" acceptance is unachievable and the M12 edit can be skipped while the AC is green

**Dimension:** logical integrity, operational resilience (false-green + false-red)

The Plan 27-01 AC-PIPE-04 positive assertion is `grep -E 'min\(n_pts_cap, n_snapshots'`
(`27-01-PLAN.md:100,114,120,159`; `27-VALIDATION.md:50`). That token already
matches `ctl_instruction.md:498` — a Phase-26 forward-reference that states the
**full** locked M12 rule. The verify block (`27-01-PLAN.md:114`) and acceptance
(`:120`) require the check to **FAIL** on the un-edited spec to prove it
discriminates; it passes immediately. The intended operative edit target is the
Mini-Batch block at `:1417-1423`, which still holds the stale "50% uniform / 50%
weighted" prose.

**Failure modes.** *False-green:* the executor marks AC-PIPE-04 discriminating
and passing, treats that as proof the M12 contract landed, and **skips the actual
Mini-Batch transcription** — M12 → VERIFIED on a grep that fired on the wrong
line, while the Mini-Batch block keeps the superseded prose. *False-red:* the
executor hits the self-contradiction "must fail pre-edit but passes pre-edit" and
halts Task 1 on a plan-internal AC-design bug rather than a source-silent gap.

**Fix.** Scope AC-PIPE-04's positive assertion to the Mini-Batch Construction
block specifically (section-anchored, e.g. match the token **and** require it to
land at line ≥ the Mini-Batch heading, not at 498); drop or restate the "fails
pre-edit" claim as "fails when scoped to the Mini-Batch region"; add a positive
post-edit assertion that the Mini-Batch block no longer contains the stale
"50% uniform / 50% weighted" prose.

#### F-02 [P0] AC-PIPE-08's "no replay-fraction/collocation POLICY" negative control false-reds on the existing Mini-Batch policy block, and forces a collision with Plan 27-01

**Dimension:** logical integrity, execution clarity (false-red + scope corruption)

Plan 27-03's negative control forbids "replay-fraction / collocation-density
POLICY text" (`27-03-PLAN.md:115-117`), and Task 2 directs the new sub-section to
be "co-located near Mini-Batch ~1417 or §2.6" (`27-03-PLAN.md:141-142`). But the
existing Mini-Batch block at `ctl:1417-1430` **is** training-loop policy text:
`reserve ρ_lookahead (e.g., 5%)`, a `Replay set | B_≤k | 240` and
`Look-ahead set | B_{k+1} | 16` table. A file-wide negative-control grep over
`replay`/`collocation`/`ρ_lookahead`/`B_≤k` hits these pre-existing lines and
fails — criminalizing text that predates Phase 27.

This compounds with F-01: Plan 27-01 and Plan 27-03 **both target the Mini-Batch
region** — 27-01 to transcribe the M12 data-loss contract, 27-03 to co-locate the
stage-query interface — and 27-03's negative control forbids the very section
27-01 must edit. An executor that "fixes" the false-red by deleting the
`Replay set`/`Look-ahead set` table silently rewrites a curriculum-training
section outside Phase 27's scope.

**Deeper placement tension (flagged for the user).** 27-01 transcribes a
**data-side** contract (points per trajectory = the data-loss sample) into a
**training-loop policy** block. That co-location is the root cause of both F-01
(the data-side token and policy text share a region the AC cannot distinguish)
and F-02 (the negative control cannot be file-wide). The plans should decide,
on the record, whether the M12 contract gets its own data-side sub-section
(parallel to 27-03's stage-query) or explicitly replaces only the
"50% uniform / 50% weighted" sentence while preserving the surrounding
replay/lookahead policy — and the ACs must enforce that exact boundary.

**Fix.** Scope AC-PIPE-08's negative control to the **new stage-query
sub-section only** (between its heading and the next `###`); add an explicit
precondition that the existing Mini-Batch policy block is out of scope for the
control; reconsider "co-locate near Mini-Batch" in favor of a §2.6 placement.

#### F-03 [P0] Files that must mutate during execution are owned by no plan (`27-VALIDATION.md`, `27-0N-SUMMARY.md`)

**Dimension:** operational resilience, execution clarity

Every plan's `files_modified` block is restricted to the nominal
spec/ledger/packet files (e.g. 27-01 lists four files, 27-03 three, 27-04 four).
But execution **requires** mutating files that appear in none of them:

- `27-VALIDATION.md` — its per-task `Status` column rows (`:50-55`) must flip
  `pending → green`, and its frontmatter `wave_0_complete` / `nyquist_compliant`
  (`:5-6`) must flip to `true` per its own Validation Sign-Off block (`:85-90`).
  An executor honoring owned-paths discipline literally cannot commit these
  flips, so the phase exits with `nyquist_compliant: false` despite all four
  contracts landed, and `/gsd-verify-work` rejects it.
- `27-0N-SUMMARY.md` — each plan's `<output>` (`27-01:284`, `27-02:254`,
  `27-03:249`, `27-04:251`) creates one, and every Task 3/4 records results "in
  the SUMMARY." None is in any `files_modified`; each lands in an ambiguous
  commit or is lost on the next clean.

**Fix.** Before execution, choose a durable convention: add
`27-VALIDATION.md` to the final wave's `files_modified` with a dedicated task
that flips the status rows and frontmatter after all ACs pass, and add each
`27-0N-SUMMARY.md` to its plan's `files_modified` (or define a single trailing
`docs(27): record plan summaries` commit owned by the orchestrator).

### P1 — likely to bite, with concrete triggers

#### F-04 [P1] Verbatim-transcription anchors are imprecise and have no pre-transcription verification step

**Dimension:** execution clarity (false-green / silent spec corruption)

The plans cite ranges (`m11-m12-severity.md:105-113`, `compute-globals-D.md:104-108`,
`data05-precision.md:65-79`) and say "transcribe VERBATIM from the named anchor."
Verification confirms the locked blockquote is a single line (`:107`, `:106`,
`:67`); the cited ranges also include the lead-in header, the sibling M11/global
ruling, and a "Phase 25 makes zero framework-spec edits" process note. No plan
step verifies that the cited anchor actually contains the expected content
before transcribing. *Mitigation:* the plans also name the paragraph by its
opening words ("the paragraph beginning 'Per-trajectory data-loss point count.'"),
which reduces — but does not eliminate — the risk that an autonomous executor
transcribes the lead-in or a sibling ruling into the spec as if it were locked
convention. The risk is real because the packets themselves mutate during the
phase (27-01 appends to `m11-m12-severity.md`'s transition log, etc.).

**Fix.** Add a mandatory pre-transcription sub-step to each Task 2: anchor by
**content marker** (`grep -n 'Per-trajectory data-loss point count'`), assert
the matched line's opening tokens match expectation, and STOP-and-re-anchor if it
has drifted. Narrow the cited ranges to the single target line.

#### F-05 [P1] PIPE-09 "admitted-set scope" is flagged-for-sign-off but transcribed autonomously (E_scale leg is grounded — refined)

**Dimension:** logical integrity, governance resilience

`compute-globals-D.md:106` records the `compute_globals` admitted-set scope
(post-Step-1A, post-blacklist, post-DATA-05-quarantine) as "a documented minor
judgment **flagged for spec-author sign-off**." Plan 27-04 transcribes it as an
autonomous target (`27-04-PLAN.md:18,149-150`) without citing a sign-off. If a
prior user/source authorization exists, the plan must cite it; if not, this is a
source-silent semantic decision and the STOP protocol blocks the dependent
PIPE-09 edit.

**Refinement versus the 21:48 draft.** The earlier draft (F-02 there) bundled
this with `E_scale +1e-8`. That leg is **refuted**: `compute-globals-D.md:108`
explicitly delegates `E_scale = 1e-8` to Phase 27 as a "2-of-3 editable-spec
choice," and the live files confirm the majority (`arch:761` and `ctl:1224`
already `+1e-8`; only `ctl:771` was the outlier). The E_scale canonicalization
is well-grounded and not sign-off-pending. Only the **admitted-set scope** leg
remains open.

**Fix.** Add a pre-Task-2 checkpoint in 27-04 that cites the concrete sign-off
source for the admitted-set scope. If none exists, log a Phase 27 STOP gap and
halt only the PIPE-09-dependent work until the user resolves it.

#### F-06 [P1] `autonomous: true` collides with mandatory STOP branches — no defined consumer for a surfaced gap

**Dimension:** operational resilience (false-red + false-green)

All four plans declare `autonomous: true` and also instruct "STOP and surface a
NEW candidate gap to the orchestrator" (27-02 `:114-115`; 27-03 `:48,110,123,127`).
Under autonomous execution there is no defined orchestrator or human-in-the-loop
channel (the CLAUDE.md STOP protocol step 5 assumes one). `27-GAPS.md` carries
no definition of the escalation path, recipient, or block-vs-proceed semantics.
Consequently a STOP either (a) deadlocks waiting for an orchestrator that does
not exist, (b) is treated as resolved and the executor proceeds (the STOP
protocol is vitiated), or (c) is paper-trailed into a SUMMARY while work
continues — equivalent to (b).

**Fix.** Define in `27-CONTEXT.md` what "surface to the orchestrator" means
under `autonomous: true` (a `HALT_UNTIL_INSTRUCTION` marker the user sees on
resume? a park-the-plan-and-move-to-the-next-independent-plan protocol?).
Alternatively, downgrade to `autonomous: false`, since the plans contain genuine
STOP branches that require adjudication.

#### F-07 [P1] The 27-03 A1 STOP branch is not a hard halt; the edit task it gates has no STOP path

**Dimension:** logical integrity (false-green)

Plan 27-03's Task 1 acceptance allows "OR a NEW candidate gap was surfaced … and
the sub-section work is halted" as a *success* state (`27-03-PLAN.md:122-127`),
and the `<done>` line treats "a new gap is surfaced" as task completion. Task 2
— the actual edit, where the invention risk lives — has **no** STOP branch
(`27-03-PLAN.md:139-157`); its only instruction is "Do NOT invent … (A1)" with no
halt path. An executor can therefore surface a gap in Task 1, mark it done, and
proceed into Task 2 where, lacking a halt path, it invents the ungrounded detail
to finish — exactly what A1 was meant to prevent.

**Fix.** Make the A1 guard a hard precondition for Task 2 entry ("IF Task 1
surfaced a gap, STOP — do not proceed"); add a STOP branch to Task 2 mirroring
Task 1's; rewrite the Task 1 `<done>` to separate "grounded → proceed" from
"gap surfaced → HALT plan."

#### F-08 [P1] Commit-SHA-backfill paradox + one stale instruction; the two-phase pattern is unstated

**Dimension:** operational resilience

A commit cannot contain its own SHA, yet each Task 3 instructs the executor to
write the substantive commit's short SHA into the transition log **in the same
commit** as the spec edit (citing the Phase 25/26 house pattern, which is in
fact a *separate provenance commit* — `m11-m12-severity.md:182`). Separately,
Plan 27-02's instruction to "backfill the `<commit-pending>` SHA" is **stale**:
that backfill is already complete (`data05-precision.md:90-93`; commit
`656de848`). The substantive Phase 27 commit SHA still requires the two-phase
pattern (substantive commit carries a placeholder; an immediately-following
provenance commit backfills the real SHA), which no plan spells out.

**Fix.** Add an explicit two-phase commit/provenance pattern to each plan:
substantive commit writes a `<pending-27-0N-sha>` placeholder; a follow-up
provenance commit (explicit owned paths) backfills the short SHA. Delete 27-02's
stale "backfill `<commit-pending>`" instruction.

#### F-09 [P1] STOP-recovery after partial ledger mutation is unspecified

**Dimension:** operational resilience

Each plan's Task 1 advances a ledger row `PENDING → IN_PROGRESS` *before* the
spec edit lands (the EVID-06 packet-before-edit gate). If a STOP/gap fires
mid-wave — after a row has advanced but before VERIFIED — the plan does not say
whether to revert the row (a destructive op), leave it at IN_PROGRESS (blocks the
phase-exit gate, which forbids any in-scope row at IN_PROGRESS/FIX_APPLIED), or
checkpoint. An autonomous executor faces an unscripted, possibly destructive
decision.

**Fix.** Add a one-paragraph "STOP-recovery contract" to `27-CONTEXT.md` (or each
plan's threat model): on a mid-task STOP after a row has advanced past PENDING,
record the halt in `27-GAPS.md` and leave the row at its current status — do not
revert (avoids destructive ops); the gap's resolution note carries the resume
path.

#### F-10 [P1] "Corroborating" dataset probes race a live gold-dataset regeneration

**Dimension:** operational resilience

Plans 27-01 (`:107-110`) and 27-02 (`:151`) instruct re-running
`data06_snapshots.py` and `data05_mass_drift.py` to reconfirm the cited medians
(61 / 127 / 1003 and 0/4857). A concurrent **standard-gold missing-184 Brutus
rerun is actively running** (untracked
`simulation_data/Scripts/brutus_runners/rerun_standard_gold_missing_184.py`;
live `brutus` processes visible). The cited gold median (1003) is drawn from the
very dataset being regenerated, so a probe run mid-rerun may return transient
in-flight counts that do not match the recorded facts. The plans call the probes
"corroborating, not blocking," which is correct *for a static dataset* but does
not tell the executor what to do when the probe disagrees with a moving target.

**Fix.** Add a Wave-0 / Task-1 precondition: before any dataset probe, check for
in-flight Brutus reruns; if present, record the probe as deferred (grep-only
fallback) rather than racing it. The medians are CLM-10-verified facts in
`24-VERIFIED-FACTS.md` and need not be re-derived from a moving dataset.

#### F-11 [P1] AC-PIPE-09's `1e-10` negative control is a multi-collision trap; the scoping is prose, not a runnable command

**Dimension:** logical integrity, operational resilience (false-green PHYS-03 corruption + false-red)

AC-PIPE-09's negative control requires `grep '1e-10'` to return "NOTHING for the
`E_scale` floor" while exempting the Plummer `ε_inv = 1e-10`
(`27-04-PLAN.md:111-113`). Verification shows ~10 legitimate `1e-10`/`10^{-10}`
sites in `ctl_instruction.md`. The exemption ("scope the negative grep to the
`E_scale` line") is prose, not an enforced command. *False-green:* an executor
authoring a file-wide `grep '1e-10'` sees the Plummer hits post-edit and "fixes"
`ε_inv` to `1e-8`, **corrupting PHYS-03** — the plan's own threat register
(T-27-EPSCONFUSE at `27-04-PLAN.md:230`) names this exact failure. *False-red:* a
cautious executor flags the unspecified scoping mechanism as a process-schema
gap (D-06) and halts.

**Fix.** Specify the exact runnable negative-control command scoped to the
`E_scale` line (e.g. `grep -nE 'E_(scale|\\mathrm{scale}).*10\^\{-?10\}'`),
and add a positive-control assertion that the Plummer `ε_inv = 10^{-10}` sites
are unchanged (count ≥ pre-edit baseline).

#### F-12 [P1] Regression ACs (AC-PIPE-01/06) are presence-greps, not byte-exact invariants

**Dimension:** operational resilience (false-green)

The AC-PIPE-01 regression (`27-01-PLAN.md:224-234`) greps for the *presence* of
`## Step 1A — Trajectory Admission Gate`, `final_timestep >= 9.5`, `SCS > -5`.
Presence cannot detect a subtle value change (`>= 9.5` → `> 9.5`, or
`SCS > -5` → `SCS >= -5`) — exactly the drift risk when 27-01 edits text
adjacent to this region (the plan itself flags the line-498 region as a shared
edit surface). An executor that finds the grep empty may silently "re-canonicalize"
the AC to the new text, blessing the corruption. (Same weakness applies to the
AC-PIPE-06 footer/`param_provenance` regression.)

**Fix.** Replace presence-greps with byte-exact invariants on the shared
regression surfaces: capture the byte range (or a fixture of the locked tokens)
pre-edit and `diff`/hash post-edit; make the AC fail on any line-number drift,
not just token absence.

#### F-13 [P1] The final phase gate checks ledger status, not a full AC re-run

**Dimension:** operational resilience

`27-VALIDATION.md` requires the full suite (AC-PIPE-04/07/08/09 + regression
AC-PIPE-01/06) green and `nyquist_compliant: true` before `/gsd-verify-work`
(`:32,41,90`). Plan 27-04, the final wave, confirms ledger states in the SUMMARY
but has **no task** that reruns all ACs after the last edit or updates the
`27-VALIDATION.md` sign-off (`27-04-PLAN.md:193-195`). Phase 27 can exit green on
ledger status while an earlier AC is stale against the final spec state.

**Fix.** Add a final 27-04 exit task that reruns all four Phase 27 ACs plus
AC-PIPE-01 and AC-PIPE-06, records outputs, updates the validation status rows
and frontmatter, and only then confirms phase exit (this also closes F-03's
VALIDATION-ownership gap).

### P2 — consistency and coordination (apply before execution)

#### F-14 [P2] Wave numbering drifts between plan frontmatter and the validation map

Plan frontmatter serializes waves 1/2/3/4 (`27-0N-PLAN.md:5`). The
`27-VALIDATION.md` Per-Task Verification Map lists PIPE-08 as wave 2 and PIPE-09
as wave 3 (`:52-53`), and `27-RESEARCH.md:179` floats batching
`{PIPE-07, possibly +PIPE-08}`. An executor reading VALIDATION as the wave
source-of-truth would launch PIPE-08 alongside PIPE-07 and skip the
`depends_on` chain 27-03 declares. **Fix:** pick one scheme and propagate; the
`depends_on` chains imply strictly serial 1/2/3/4, so update VALIDATION's
`:52-53`.

#### F-15 [P2] 27-04 lists `pinn_architecture.md` in `files_modified` while every body instruction says no-change

`27-04-PLAN.md:8-9` lists arch in `files_modified`, but the artifacts (`:86-87`),
Task 2 action (`:154`), and acceptance (`:166`) all say confirm-only/no-change —
confirmed by `pinn_architecture.md:761` already reading `+10^-8`. This collides
with the same-commit/owned-paths policy (an owned path with an empty diff is
ambiguous to stage). **Fix:** remove `pinn_architecture.md` from 27-04's
`files_modified`/owned paths; record the §5.2 consistency check in the SUMMARY as
a read-side verification.

#### F-16 [P2] Phase-exit "all rows VERIFIED" is incompatible with the footer row staying PENDING-by-design

The phase-exit gate (`27-04-PLAN.md:204`) requires "all Phase 27 in-scope rows …
at VERIFIED," but the `footer` row's Status field is never advanced — 27-02 only
"closes the footer row's PIPE-07 facet" (`27-02-PLAN.md:184-187`). The ledger
lifecycle keys on row Status, not facets. A literal executor either blocks exit
(footer Status ≠ VERIFIED) or silently passes. **Fix:** explicitly carve the
footer row out of the "all rows VERIFIED" assertion, or advance its Status to a
terminal state in 27-02.

#### F-17 [P2] The G5 per-finding ledger note is written by 27-01 then re-edited by 27-03 with no preserve-prior instruction

27-01 moves the G5 row and its per-finding note (`24-ISSUE-LEDGER.md:329-337`) to
VERIFIED (`27-01-PLAN.md:186-188`); 27-03 then appends a PIPE-08 metadata note to
the same note region (`27-03-PLAN.md:180-183`). This is sequenced (27-03 depends
on 27-01) but 27-03 never tells the executor the note was just authored and must
be preserved (append-only). **Fix:** add an explicit append-only preserve
instruction to 27-03 Task 3; gate behind F-14 so the two cannot run concurrently.

#### F-18 [P2] 27-04's `depends_on` is broader than the section coupling; it over-serializes

27-04 declares `depends_on: ["27-01","27-02","27-03"]` but RESEARCH calls PIPE-09
"the most isolated … safely last" (`27-RESEARCH.md:177`) and 27-04's tasks
reference no deliverable from 27-02 or 27-03. A STOP in 27-02/27-03 would block
the isolated 27-04 unnecessarily. **Fix:** change `depends_on` to `[]` (rely on
wave ordering) or document the actual coupling (likely only
`24-ISSUE-LEDGER.md` write-coordination).

#### F-19 [P2] Fixed line-number `read_first` anchors will rot across waves

`read_first` blocks cite fixed ranges in `ctl_instruction.md` (e.g. `:1410-1430`,
`:800-825`, `:744-774`). Wave 1 inserts ~12-40 new lines into ctl, so later
waves' anchors shift by the insertion delta. (Already observed: the 27-04 `E_scale`
"~line 773" anchor is actually `:771`.) **Fix:** replace fixed line numbers with
section/content anchors and note that earlier-wave edits shift later anchors.

#### F-20 [P2] AC-PIPE-10 (D-03 HDF5) is conditionally required by 27-03 but absent from the validation full-suite

27-03 Task 3 conditionally re-confirms AC-PIPE-10 if the stage-query text is
relocated near Step-1 item 6 (`27-03-PLAN.md:188-189,203`), exercising the
"Codex discretion on placement" granted at `:142`. But the full-suite command in
`27-VALIDATION.md:32` omits AC-PIPE-10. The phase could pass `/gsd-verify-work`
while skipping a regression the plan made mandatory. **Fix:** add the
conditional AC-PIPE-10 to the full-suite command, or drop the conditional from
27-03.

### P3 / FYI

#### F-21 [P3] Owned-paths is advisory, not hook-enforced

`scripts/agent-commit` only checks `GIT_AGENT_OWNED_PATHS` is non-empty, and
`.githooks` → `validate_staged_paths.py` enforces only blocked patterns and blob
size — it does **not** cross-check staged paths against owned paths. The
"exactly N files" wording is self-policed. Operationally this is benign
(concurrent waves re-using `ctl_instruction.md` won't be blocked), but an
executor that over-stages will not be caught. **Fix:** note in `27-CONTEXT.md`
that owned paths are advisory and the executor must self-audit
`git diff --cached --name-only`.

#### F-22 [P3] The AC-PIPE-04 `0.5×` negative control is currently vacuous

No operative `0.5 × n_snapshots` factor exists in `ctl_instruction.md` pre- or
(post-) edit, so the negative control passes trivially and proves nothing about
the edit. Harmless, but worth noting so an executor does not read a passing
negative control as meaningful coverage.

## Residual risks

- The acceptance-check strategy is grep-heavy. `27-VALIDATION.md:75-78` concedes
  that **transcription fidelity** (edited prose matches the locked verdict's
  *meaning*, not just tokens) is Manual-Only — yet in an autonomous-execution
  plan there is no human reviewer in the loop at the point that fidelity matters.
  At minimum, each `<output>` SUMMARY should flag transcription fidelity as a
  required human-review item before `/gsd-verify-work`.
- The working tree already carries unrelated user-owned changes (`.gitignore`,
  untracked Brutus rerun scripts) and a live dataset regeneration (F-10).
  Execution agents must re-run `git status --short --branch` and stage only
  explicit owned paths.
- The `ce-scope-guardian-reviewer` persona did not return usable output; the
  governance/scope axis was covered by the parent's manual analysis instead. A
  dedicated scope pass would add confidence on owned-path coverage and
  no-invention boundaries.

## Recommended remediation order

1. **F-01, F-02** (P0): re-scope AC-PIPE-04 to the Mini-Batch block; re-scope
   AC-PIPE-08's negative control to the new sub-section and decide the
   data-side-vs-training-policy placement. These block correct execution.
2. **F-03** (P0): assign ownership of `27-VALIDATION.md` and `27-0N-SUMMARY.md`
   before execution.
3. **F-05** (P1): cite or surface the PIPE-09 admitted-set-scope sign-off.
4. **F-06, F-07, F-09** (P1): define the autonomous-STOP contract, harden the
   A1 halt, and add STOP-recovery semantics.
5. **F-08, F-13** (P1): state the two-phase SHA-backfill pattern; add the final
   full-suite validation/sign-off task.
6. **F-10, F-11, F-12** (P1): gate dataset probes against the live rerun; make
   the AC-PIPE-09 negative control a runnable scoped command; convert regression
   ACs to byte-exact invariants.
7. **F-04** (P1): add pre-transcription anchor verification.
8. **F-14–F-20** (P2): apply the cross-artifact consistency fixes.
9. **F-21, F-22** (P3/FYI): document and note.

## Changes versus the 21:48 draft

- **New P0s:** F-02 (AC-PIPE-08 negative-control collision + placement tension)
  and F-03 (un-owned `27-VALIDATION.md` / `27-0N-SUMMARY.md`).
- **Sharpened:** the prior F-01 (AC-PIPE-04) is reframed as a P0 with the
  "unachievable fails-pre-edit acceptance" + "skip-the-edit false-green" framing,
  verified at `ctl:498`.
- **Refuted/narrowed:** the prior F-02 E_scale leg is **refuted** —
  `compute-globals-D.md:108` explicitly delegates `E_scale = 1e-8` to Phase 27
  and the live files confirm the 2-of-3 majority. Only the admitted-set-scope leg
  survives (now F-05).
- **New P1s:** F-04 (anchor verification), F-06 (autonomous-vs-STOP), F-07 (A1
  halt), F-09 (STOP-recovery), F-10 (probe/rerun race), F-11 (`1e-10`
  multi-collision), F-12 (presence-grep regressions).
- **Retained and verified:** prior F-03 → F-08; prior F-04 → F-13; prior F-05 →
  absorbed into F-02/F-07; prior F-06 → F-08; prior F-07 → F-14/F-15/F-16/F-17.

## Coverage

Review personas completed: `ce-coherence-reviewer`, `ce-feasibility-reviewer`,
`ce-adversarial-document-reviewer`. The `ce-scope-guardian-reviewer` persona was
dispatched but returned no usable output; its axis (owned-path coverage,
no-invention boundaries, phase-exit rigor) is covered by the parent's manual
analysis (F-03, F-05, F-13, F-15, F-16, F-21).

All findings were re-verified against the live files before inclusion; severity
was calibrated to the verified evidence. **No Phase 27 plan or support artifact
was modified by this audit** — only this report was written.

---

## Remediation Status (applied 2026-06-14)

A second pass re-verified every finding's factual claims against the live files
(the spec anchors, the evidence packets, the four plans, VALIDATION, GAPS,
CONTEXT, RESEARCH, and the ledger) and confirmed **all 22 findings are
factually valid**. The recommended fixes were then applied to the Phase 27
planning artifacts. Disposition per finding:

### Applied (grounded mechanical / operational fixes)

| Finding | Disposition | Grounding | Artifact(s) |
|---|---|---|---|
| F-01 | Applied | `ctl:497-498` carries the full M12 rule (token pre-satisfied); the operative Mini-Batch block (`ctl:1417-1431`) lacks it and holds the stale prose. Scoped AC-PIPE-04 assertions (1)+(8) to the Mini-Batch region via an `awk` extractor + added a post-edit stale-prose-absent assertion. | 27-01 Task 1/verify/acceptance, Task 2 verify |
| F-02 | Applied | The Mini-Batch block IS pre-existing curriculum policy (`Replay set`/`B_≤k`/240, `Look-ahead set`/`B_{k+1}`/16, `ρ_lookahead`). Scoped AC-PIPE-08 negative control to the new sub-section only; added the out-of-scope precondition; §2.6 preferred placement (avoids 27-01 region collision). | 27-03 Task 1, Task 2 |
| F-03 | Applied | No plan owned VALIDATION/SUMMARY. Added each `27-0N-SUMMARY.md` to its plan's owned paths; added `27-VALIDATION.md` to 27-04 (Task 4) for the status/frontmatter flips. | all 4 plans frontmatter; 27-04 Task 4 |
| F-04 | Applied | Cited ranges are wider than the single locked line. Added a content-marker grep + assert + STOP-if-drift pre-transcription step; re-locate targets by heading. | 27-01/02/04 Task 2; 27-03 via D-18 |
| F-06 | Applied (grounded default; confirmed) | `autonomous: true` does not vitiate STOP (CLAUDE.md "no exception"; step 5 "halted work stays halted"). Added CONTEXT D-15: a STOP parks the plan + records the gap + phase-exit blocks while a gap is OPEN; independent waves proceed. User follow-up on 2026-06-14 requested fixing the Phase 27 issues, with no override to this default. | 27-CONTEXT D-15 |
| F-07 | Applied | Task 1 allowed "gap surfaced" as completion; Task 2 had no STOP path. Made A1 a hard precondition for Task 2, added a Task 2 STOP branch, split Task 1 `<done>` into proceed vs. park. | 27-03 Task 1/acceptance/done, Task 2 |
| F-08 | Applied | A commit cannot contain its own SHA; the Phase 25/26 house pattern (`m11-m12-severity.md:182`, `e05b4b1a`) is a separate provenance commit. Stated the two-phase `<pending-27-0N-sha>` pattern in all 4 plans; fixed 27-02's stale "backfill `<commit-pending>`" (authoring SHA already done at `09e37f8`/commit `656de848`). | all 4 plans Task 3; 27-02 artifacts |
| F-09 | Applied | Reverting a ledger row mid-STOP is a destructive op. Added CONTEXT D-16: leave the row at current status, record the halt, do not revert; the gap resolution carries the resume path. | 27-CONTEXT D-16 |
| F-10 | Applied | A live standard-gold Brutus rerun is active (the gold median 1003 is drawn from the mutating dataset). Added a Wave-0/Task-1 precondition to check for in-flight reruns and DEFER the probe (grep-only + CLM-10 facts) if present. | 27-01 Task 1, 27-02 Task 2 |
| F-11 | Applied | 9 legitimate `1e-10`/`10^{-10}` sites exist (Plummer `eps`/`ε_inv`). Replaced the prose-scoped control with an exact runnable `E_scale`-scoped grep + a Plummer positive-control (count drops by exactly 1; surviving sites byte-identical). | 27-04 Task 1/acceptance |
| F-12 | Applied | Presence-greps miss subtle value flips. Converted the B-06 (27-01) and D7 (27-02/03) regression checks to byte-exact invariants: pre-edit region fixture + `shasum` + post-edit `diff`. | 27-01 Task 4, 27-02 Task 3, 27-03 Task 3 |
| F-13 | Applied | No full-suite re-run + VALIDATION flip task existed. Added 27-04 Task 4: rerun the full AC suite against the final spec, flip VALIDATION frontmatter/status, confirm the phase-exit gate. | 27-04 Task 4 |
| F-14 | Applied | VALIDATION listed PIPE-08 as wave 2, PIPE-09 as wave 3 (plans say 3/4). Corrected to 3/4 to match the serial `depends_on`/wave chain. | 27-VALIDATION Per-Task Map |
| F-15 | Applied | `arch:760` already `+10^-8`; every 27-04 instruction says no-change. Removed `pinn_architecture.md` from 27-04 owned paths; §5.2 check is read-side (SUMMARY). | 27-04 frontmatter + objective |
| F-16 | Applied (grounded default; confirmed) | Footer row (`:40`) spans PIPE-06 (done via D7) + PIPE-07 (27-02); D-07 implies touched rows reach VERIFIED (precedent: cross-phase D=6.694 row). 27-02 now advances footer Status → VERIFIED; 27-04 Task 4 gate requires it. User follow-up on 2026-06-14 requested fixing the Phase 27 issues, with no override to this default. | 27-02 Task 3; 27-04 Task 4 |
| F-17 | Applied | 27-01 authors the G5 note; 27-03 appends to it. Added an explicit append-only preserve instruction to 27-03 Task 3. | 27-03 Task 3 |
| F-18 | Applied | RESEARCH:177 calls PIPE-09 "most isolated." Changed 27-04 `depends_on` to `[]` (rely on wave ordering for ctl write-serialization); documented that the exit-gate task (Task 4) waits for prior rows — so 27-04 can proceed under D-15 even if 27-02/03 park. | 27-04 frontmatter + objective |
| F-19 | Applied | Wave 1 inserts ~12-40 lines, shifting later anchors (the 27-04 "~line 773" is `:771`). Added CONTEXT D-18 (re-locate by heading/content marker, not line number) + per-plan re-locate notes. | 27-CONTEXT D-18; all 4 plans |
| F-20 | Applied | AC-PIPE-10 is conditionally mandatory (27-03 relocation) but absent from the full suite. Added the conditional AC-PIPE-10 to the VALIDATION full-suite command. | 27-VALIDATION; 27-04 Task 4 |
| F-21 | Applied | `agent-commit` only checks owned-paths non-empty; `.githooks` doesn't cross-check. Added CONTEXT D-17 (advisory; executor self-audits `git diff --cached --name-only`). | 27-CONTEXT D-17 |
| F-22 | Applied | No operative `0.5 × n_snapshots` factor exists (the negative control is vacuous). Noted it in 27-01 Task 1 so a passing negative control is not misread as coverage; the real signal is F-01's scoped (1)+(8). | 27-01 Task 1 |

### Surfaced and resolved (genuine STOP gap)

| Finding | Disposition | Detail |
|---|---|---|
| F-05 | **Resolved as GAP-27-02 Option A** | The candidate source `compute-globals-D.md:106` records the `compute_globals` admitted-set scope as "flagged for spec-author sign-off." The gap was correctly surfaced in `27-GAPS.md` + `v1.5-GAPS.md` (semantic; impact MEDIUM). User follow-up on 2026-06-14 requested fixing the Phase 27 issues after Option A was recommended, so GAP-27-02 is now `RESOLVED-WITH-INSTRUCTION`: sign off the admitted-set scope and transcribe it cleanly as normative ctl §2.5 text, with the sign-off caveat retained only in the gap/evidence provenance. |

### Files changed by remediation

- `.planning/phases/27-.../27-01-PLAN.md` (F-01, F-03, F-04, F-08, F-10, F-12, F-19, F-22)
- `.planning/phases/27-.../27-02-PLAN.md` (F-03, F-04, F-08, F-10, F-12, F-16, F-19)
- `.planning/phases/27-.../27-03-PLAN.md` (F-02, F-03, F-04/D-18, F-07, F-08, F-12, F-17, F-19)
- `.planning/phases/27-.../27-04-PLAN.md` (F-03, F-04, F-05 resolved sign-off, F-08, F-11, F-13 Task 4, F-15, F-16, F-18, F-19)
- `.planning/phases/27-.../27-CONTEXT.md` (D-15 F-06, D-16 F-09, D-17 F-21, D-18 F-19)
- `.planning/phases/27-.../27-VALIDATION.md` (F-14 wave numbers, F-20 full suite)
- `.planning/phases/27-.../27-GAPS.md` (GAP-27-02 / F-05)
- `.planning/milestones/v1.5-GAPS.md` (GAP-27-02 mirror / F-05)
- `docs/work/reviews/.../2026-06-13-phase-27-plan-audit-report.md` (this appendix)

### User-confirmed grounded defaults

- **F-06** (CONTEXT D-15 autonomous-STOP operationalization) and **F-16** (footer row → VERIFIED
  via D-07) were resolved with grounded defaults rather than surfaced as gaps, because each
  follows directly from an existing governance rule (STOP protocol step 5; ledger lifecycle
  D-07). User follow-up on 2026-06-14 requested fixing the Phase 27 issues with no override, so
  these defaults stand.

### Blocking item before Phase 27 execution can close

- **No GAP-27-02 blocker remains.** Phase 27 execution can close once the plan-set executes,
  all in-scope ledger rows reach their terminal states, the full AC suite passes, and no new
  in-scope gap is OPEN.
