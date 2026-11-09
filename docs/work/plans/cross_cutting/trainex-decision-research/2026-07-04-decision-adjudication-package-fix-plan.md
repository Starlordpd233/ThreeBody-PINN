---
status: active
purpose: implementation-plan
created: 2026-07-04
milestone: untracked
phase: cross-cutting
retirement_trigger: All findings below are resolved and the trainex-r1 decision-adjudication package is sent to the external agent, OR this plan is superseded by a revised fix plan.
---

# Fix Plan — trainex-r1 `decision-adjudication` ERW research package

## 0. What this is

A consolidated, evidence-backed list of everything that must be **fixed, re-grounded, or
optionally tightened** in the research package at
`pinn_instruction/markdown_conversion/framework-specs/trainex-r1/decision-adjudication/`
before it is uploaded to 2–3 external research agents. The bar is **100 % flawless**: the
external agent receives only the 9 uploaded files and cannot disambiguate against the repo,
so any stale fact, broken reference, or contradictory instruction becomes a wrong input that
produces a wrong adjudication.

**How the findings were produced.** A 6-dimension adversarial audit workflow (ERW compliance,
provenance/freshness, grounding accuracy, scope consistency, numerical/data, external
completeness) with per-finding re-verification; a 4-claim `deep-research` run (3-vote
adversarial verification per claim) for the load-bearing tooling assertions; and direct
manual recovery of the one audit dimension whose agent died mid-response (provenance) plus
the one verifier that hit a rate limit.

**Package channel:** build-design (recommendation the owner ratifies; **not** a specwork
verdict source). ERW rules 1, 5, 6, 7, 9 apply (see
`docs/runbooks/external-research/2026-06-11-external-research-workflow.md`).

## 1. Where edits go and how to apply them

- The package lives in the **trainex worktree** (`.worktrees/trainex/`, branch `track/trainex`),
  not on `master`. All edits to the sheet (attachment) and the three authored uploads
  (master / prompt / consolidation) are made there. `master` stays untouched (it is the
  cross-cutting governance/planning home; only this plan lives here, next to the design at
  `docs/work/designs/cross_cutting/trainex-decision-research/`).
- The uploaded (authored) files are `research_package/RESEARCH-CONTEXT-MASTER.md`,
  `research_package/RESEARCH-AGENT-PROMPT.md`, `consolidation/CONSOLIDATION-PROMPT.md`, and
  the 8 files under `attachments/`. `DELIVERY-NOTE.md` is user-only (never uploaded).
- Commit each logical fix atomically via `scripts/agent-commit` with `GIT_AGENT_ID` and
  `GIT_AGENT_OWNED_PATHS` set to the package subtree. Stage explicit paths only.
- **One finding is STOP-grade** (F1, the B-8 carve-out). It must be resolved by the owner
  before the package is sent; do not edit it past the options in §F1 without instruction.

## 2. Verified CLEAN (recorded so the coverage is explicit — no action)

| Check | Result |
|---|---|
| Snapshot provenance — sha256(8) of every attachment vs delivery-note prefixes | **All 8 match** (ctl `a9d64200`, pinn `e629b2fc`, chatgpt `fe71a1ec`, sheet `15a65a60`, r1b1 `544fb717`, r1b2 `b943dc50`, postspec `f57c63d5`, design `8395564c`). |
| `attachments/ctl_instruction.md` vs `master@4bbd5443` and vs master HEAD | **Byte-identical** (0 diff lines both). Snapshot is the current, post-v1.6 authoritative spec — no stale-spec risk. |
| `attachments/pinn_architecture.md` vs `master@4bbd5443` and vs master HEAD | **Byte-identical** (0 diff lines both). |
| Locked values present in attached specs | Present (input 14D `[τ, IC₁₃]`; raw masses; `ε_train = 1e-5`; SCS gate; SIREN 12×256, ω 30/1). |
| Tooling claim — `torch.mps.current_allocated_memory()` (sheet F5) | **ACCURATE** — correct API, documented, distinct from `driver_allocated_memory()`. |
| Tooling claim — "MPS has no user streams to tune" (sheet F5) | **ACCURATE** — no user-configurable MPS streams. |
| Tooling claim — "MLX cannot honestly satisfy fp64-on-GPU" (sheet F10/U-8) | **Conclusion ACCURATE** (see F12 for a wording tightening). |

## 3. Findings

Severity legend — **STOP** = owner decision required before send (semantic/spec-accuracy);
**HIGH** = factual error that biases the external agent's output; **MED** = real ERW-rule
deviation or contradiction; **LOW** = cheap correctness/consistency fix; **OPT** = optional
precision improvement.

---

### F1 — STOP — B-8 carve-out is grounded in a §6.3 contradiction that does not exist in the attached spec

- **Where.** Sheet `trainex-r1a-options-and-decisions.md` §8 line 294, §10 decision row line 367,
  §11 line 427, §13 register U-3 line 453; carved out in master §3 lines 65–67,
  `RESEARCH-AGENT-PROMPT.md` lines 37–38, `CONSOLIDATION-PROMPT.md` line 40,
  `DELIVERY-NOTE.md` lines 81–84.
- **What the package says.** B-8 asserts a live, unresolved internal contradiction in "the
  locked gate's transcription": *"§6.3 prints `ε_H: 8.2e-6 (required: > 1e-5) → FAIL` — i.e.,
  larger passes — while the same section's plain-English says 'Smaller is better. < 10⁻⁵ is
  excellent.'"* It tells the reader the verification layer "cannot be implemented until the
  owner states the intended direction."
- **Why it is flawed (re-verified directly).** Neither attached spec contains a "§6.3", the
  string `8.2e-6`, or the quoted example output. The actual acceptance gate lives in
  `attachments/ctl_instruction.md` lines 550–555 and is **unambiguous**:
  `eps_H = max_t |(H(t)-H(0))/H(0)|`, `SCS = log10(eps_H)`, **`REJECT if SCS > -5`
  (equivalently `eps_H > 1e-5`)** → i.e. **smaller passes**; `eps_H = 0 → SCS = -inf →
  Excellent`; band `Excellent ≤ -10`. So the "plain-English / smaller-is-better" reading the
  sheet calls contradictory **matches** the current spec; the "larger passes" reading does not
  survive. An external agent sent hunting for the §6.3 contradiction will not find it and may
  conclude the locked gate is unreliable — undercutting the package's own "specs are hard
  constraints" framing.
- **Owner decision (pick one; do not silently choose).** This touches a locked metric, so the
  direction is owner-resolved per project governance:
  - **(A) Drop B-8** — the attached post-v1.6 spec defines the gate consistently (smaller
    passes). Remove the B-8 row from sheet §8/§10/§13-U-3 and remove B-8 from every carve-out
    list (master §3, prompt, consolidation, delivery note).
  - **(B) Re-ground B-8** — replace the §6.3 quote with the actual citations
    (`ctl_instruction.md` 550–555) and reframe the row as *"previously flagged, now consistent
    in the post-v1.6 spec (reject if `eps_H > 1e-5`); confirm and close"* rather than an open
    contradiction.
  - **(C) Keep an open question** — only if the owner judges a real ambiguity remains; then
    re-state it accurately against the actual spec text (not the non-existent §6.3 quote).
  - Recommended: **(A)** or **(B)**.

---

### F2 — HIGH — Wrong trajectory count for the dt_out = 0.01 (gold) sets; upper memory bracket understates fp64 pressure by ~30 %

- **Where.** Sheet `trainex-r1a-options-and-decisions.md` §D3.1, line 143.
- **What it says.** *"if the 8×/17×-denser Sets 2a/2b run long horizons, S̄ = 10,000 for those
  **5,314** trajectories alone ≈ **9.4 GB** fp64 — pressure."*
- **Why it is wrong.** "8×/17×-denser" unambiguously means the two dt_out = 0.01 **gold** sets
  (0.08→0.01 = 8×; 0.17→0.01 = 17×). Those are `brutus_hierarchical_gold_standard` (4,857) +
  `brutus_standard_quasi_random_gold_standard` (2,565) = **7,422**, not 5,314. The sheet's 5,314
  is `2,749 + 2,565` = the *standard base* (dt_out = 0.17, the **least** dense set) + standard
  gold — the standard base does not belong to the denser group. Re-derived:
  `5,314 × 10,000 × 176 B = 9.35 GB` (the sheet's figure, on the **wrong** input);
  `7,422 × 10,000 × 176 B = 13.06 GB` (correct). The fp32 implication also flips:
  `7,422 × 10,000 × 88 B ≈ 6.5 GB` for the gold sets **alone**, which sits at the sheet's own
  D3-A "switch to streaming" threshold (~6–8 GB, line 151) before any cumulative-stage replay.
- **Evidence.** `simulation_data/Documentation/README.md` lines 151, 153, 515–518.
- **Fix.** Replace "those 5,314 trajectories" with "those **7,422** trajectories (4,857
  hierarchical_gold + 2,565 standard_gold — the two dt_out = 0.01 sets)" and "≈ 9.4 GB fp64"
  with "≈ **13.1 GB** fp64 / ~6.5 GB fp32 — genuine pressure on the 24 GB budget". Re-check
  the surrounding "pressure" framing: the corrected figure **strengthens** it.
- **Load-bearing.** This number feeds the entire D3 in-memory-vs-streaming menu; an external
  agent cannot catch the 30 % understatement.

---

### F3 — HIGH — Positional mismatch between the N_traj list and the dt_out list (root cause of F2)

- **Where.** Same sentence, sheet line 143.
- **What it says.** *"N_traj = 15,028 (4,857 + 4,857 + 2,749 + 2,565) and per-set output
  cadences (dt_out 0.08 / 0.17 / 0.01 / 0.01)."*
- **Why it is wrong.** The two lists are in different orders. The trajectory-count list is in
  README folder order (hierarchical, hierarchical_gold, standard, standard_gold); the dt_out
  list reads as (hierarchical, standard, hierarchical_gold, standard_gold). Read positionally —
  the only reading available to an external agent — it pairs hierarchical_gold(4,857)↔0.17
  [wrong; actual 0.01] and standard(2,749)↔0.01 [wrong; actual 0.17]. This mis-mapping is the
  root cause of F2.
- **Evidence.** `simulation_data/Documentation/README.md` §"Brutus Parameters by Variant"
  lines 515–518; correct README-folder-order cadence sequence is (0.08, 0.01, 0.17, 0.01).
- **Fix.** Pair each count with its dt_out inline so no positional inference is needed, e.g.:
  *"N_traj = 15,028 = 4,857 @ dt_out=0.08 (hierarchical) + 4,857 @ dt_out=0.01
  (hierarchical_gold) + 2,749 @ dt_out=0.17 (standard) + 2,565 @ dt_out=0.01 (standard_gold)."*
  This also prevents the F2 grouping error from recurring.

---

### F4 — MED — MASTER frontmatter missing the `source_baseline` commit pin (ERW Rule 5)

- **Where.** `research_package/RESEARCH-CONTEXT-MASTER.md` frontmatter (lines 1–5).
- **Problem.** Rule 5 requires the snapshot commit pin to be recorded **in the master
  frontmatter** (`source_baseline`). The pin (`4bbd5443`) exists only in `DELIVERY-NOTE.md`
  line 7, which is the user-only file that is never uploaded.
- **Fix.** Add `source_baseline: 4bbd5443 (master; v1.6 merged, tag v1.6)` to the MASTER
  frontmatter (keep the delivery-note copy too).

---

### F5 — MED — ⚖ threshold ownership is contradictory and unfulfillable (merges grounding + scope findings)

- **Where.** Master §1 line 41 (r1b "How to use it" cell); contradicted by sheet §3 line 165,
  §4.2 line 189, §7 line 267, §11 line 399, §12 line 441; consolidation prompt assumes Stage-2
  fill.
- **Problem (two facets).** (a) **When:** master §1 tells the **Stage-1** agent to "use [r1b]
  to **close** the rows whose thresholds are marked ⚖", but the sheet states those values
  "take their values from R1b **at consolidation**" (Stage 2). (b) **Whether:** neither r1b
  file actually contains the numeric threshold values the ⚖ placeholders stand for
  (loss-explosion multiple + consecutive-log window, line 194; disk-floor GB, line 195;
  memory-watermark multiple, line 197). So the Stage-1 agent is directed to "close" rows from
  a source that has no numbers, on a schedule the sheet assigns to a different stage.
- **Fix.** Pick one stage to own the ⚖ fill and reconcile both docs. Recommended (defer to
  Stage 2, since r1b has no values): change master §1 line 41 to — *"Source the consolidator
  uses at Stage 2 to inform the ⚖ thresholds; in Stage 1 leave them as placeholders and record
  in the claims register any threshold r1b does not answer."* Add an explicit threshold-fill
  step to `CONSOLIDATION-PROMPT.md`, and align the sheet's "at consolidation" wording.

---

### F6 — LOW — `CONSOLIDATION-PROMPT.md` contains an `attachments/` directory reference (Rule 1)

- **Where.** `consolidation/CONSOLIDATION-PROMPT.md` line 4.
- **Problem.** *"attach … the same 8 originals from `attachments/`"* — a directory reference
  lost on upload. Rule 1 allows only bare filenames in authored uploads (the verbatim-snapshot
  exception covers the attachments' *internal* cross-refs, not the prompt's routing prose).
- **Fix.** Replace with the bare-file list (or "the same 8 originals listed in the master's
  manifest table").

### F7 — LOW — Prompt inverts Rule 7's "suggest defaults; never decide" into "be decisive; recommend one"

- **Where.** Master lines 23, 48, 55; `RESEARCH-AGENT-PROMPT.md` line 41;
  `CONSOLIDATION-PROMPT.md` line 44.
- **Problem.** Rule 7's literal requirement "Prompt must say: *suggest defaults; never
  decide*" is absent; the package says the opposite ("Be decisive", "recommend one option",
  "Decide (recommend one option each)").
- **Fix.** Add one explicit Rule-7 sentence to master §2 and the prompt — e.g. *"You suggest
  a decisive default for the owner to ratify; you never assert final authority. On
  owner-preference or empirical rows, flag the row rather than deciding it."* — alongside the
  existing "be decisive" framing.

### F8 — LOW — Output contract omits "what the runbook inherits" (Rule 7)

- **Where.** Master §5 "Output contract", lines 84–105.
- **Problem.** Rule 7's build-design contract enumerates: options menus; door classification;
  decision sheet; composed first-run recipe; **"what the runbook inherits"**; claims register.
  The master's contract omits "what the runbook inherits" (grep returns zero hits).
- **Fix.** Add one once-per-report bullet: *"What the runbook inherits — the subset of your
  recommended picks that lands in the non-expert operator's first runbook (the needed-now set,
  stated as concrete defaults/instructions), kept distinct from the deferrable set."*

### F9 — LOW — Master says "B-1..B-11"; sheet §8 actually contains B-1..B-12

- **Where.** Master line 35 (attached-files manifest, "What it is" for the sheet).
- **Problem.** The sheet's §8 contains **12** baseline items (B-1 … B-12, with B-12
  "Split-policy tension between the documents" at line 302); the master's range omits B-12.
- **Fix.** Correct master line 35 to "baseline-review items (B-1..B-12)" (or note the
  carve-outs inline).

### F10 — LOW — B-7 and B-12 are silently dropped from adjudication scope (only D1-p and B-8 are explained)

- **Where.** Master §3 lines 53–67; `RESEARCH-AGENT-PROMPT.md` lines 36–38;
  `CONSOLIDATION-PROMPT.md` lines 18–20, 40.
- **Problem.** The sheet's §8 enumerates B-1 … B-12, but the Decide list names B-1..B-6,
  B-9..B-11 and explains only D1-p and B-8 as carved out. **B-7** (sheet §8 line 292:
  *"Cosmetic: the error table's 'CUDA out of memory' row should read MPS wording … Fold into
  the next doc revision"*) and **B-12** (split-policy tension routed to v1.5) fall in neither
  bucket — a transparency gap, not a scope error.
- **Fix.** Add explicit one-line carve-outs to master §3 (mirrored in the prompt and
  consolidation): *"B-7 (cosmetic doc edit per sheet §8 — CUDA→MPS error-row wording; no
  adjudication needed) and B-12 (split-policy tension routed to v1.5/PH-5; register U-4) are
  intentionally not adjudicated here."*

### F11 — LOW — postspec references files that are not in the 9 uploads

- **Where.** `attachments/postspec-r1-direction-assessment.md` lines 16–20, 81–82, 141,
  408–413.
- **Problem.** The postspec states it was "written from `RESEARCH-CONTEXT-MASTER.md` and the
  three specs bundled in `FRAMEWORK-SPECS-BUNDLE.md`", attributes claims to
  `sampling_method.md`, and invokes its own round's master (which defined the "seven evaluation
  criteria"). Only two of the three specs are uploaded; `sampling_method.md` and the bundle are
  not. An external agent will read claims attributed to an absent file.
- **Fix.** Add a note to master §1 (postspec row): *"This assessment was written against a
  prior round's bundle that also included `sampling_method.md` (not attached — the frozen
  data-generation pipeline spec, out of scope for build decisions); treat any
  `sampling_method.md` / `FRAMEWORK-SPECS-BUNDLE.md` references as background only."*

---

### F12 — OPT — MLX fp64 framing is softer than reality (deep-research)

- **Where.** Sheet line 93 / register U-8 ("MLX under (ii): cannot satisfy it on GPU … on CPU
  its fp64 op coverage is partial and unverified").
- **Finding.** MLX 0.31.2 raises a **hard GPU exception** on float64
  (*"Arrays with type `float64` only work with CPU operations. Using `float64` arrays on the
  GPU will result in an exception"* — `ml-explore.github.io/mlx/…/data_types.html`, MLX 0.31.2
  docs). The sheet's *conclusion* (MLX cannot satisfy fp64-on-GPU) is correct; only the
  "partial and unverified" wording understates it.
- **Fix (optional, strengthens the sheet's own verdict).** State it as a hard GPU block, not
  partial coverage.

### F13 — OPT — Name the MPS `jacfwd`+concat hazard in the AD-pressure discussion (deep-research)

- **Where.** Sheet line 144 (AD-graph pressure point) and line 86 (the §10-probe "first build
  act" that anticipates MPS failure).
- **Finding.** As of PyTorch 2.7.0, `torch.func.jacfwd` on MPS raises a hard `RuntimeError`
  (`as_strided_tensorimpl does not work with MPS`) for any traced function containing
  `torch.cat` / `torch.stack` / `torch.vstack` — reproduced on Apple M4 Max
  (pytorch/pytorch#152701). `torch.func.jacrev` is unaffected and has better-documented op
  coverage; `jacfwd(jacrev(...))` is the documented good-default Hessian route. The bug is
  closed (fixed in 2.7.1+ / 2.8+). A SIREN backbone with skip connections is exactly the
  concat-bearing case.
- **Fix (optional).** In the sheet's AD-pressure paragraph, note: (a) prefer a
  `jacrev`-based second-order path on MPS; (b) pin PyTorch ≥ the fix; (c) the §10 probes are
  the instrument that catches this early — which the sheet already says generically.

## 4. Dismissed / verified-not-flaws (for transparency — no action)

- **r1b "K1–K5" / "the master file" references** (flagged by the review agent, verifier hit a
  429 — checked manually). **Not a flaw:** K1–K5 are defined inline in the r1b files
  (`## K4 — Training Feasibility Envelope`, `## K5 — Verification Ladder`, …), the files
  declare `self_contained: true`, and "the master file" refers to r1b's own prior-round master.
  At most a cosmetic note that r1b's `RESEARCH-CONTEXT-MASTER.md` means its *own* prior master,
  not this package's — optionally clarify in master §1.
- **`<agent>-decide-resolution.md` Stage-1 naming** deviates from Rule 12's
  `<agent>-resolution.md`, but the deviation is justified in the delivery note (disambiguation
  from the r1a `chatgpt-pro-resolution.md` attachment). Optional: move Stage-1 results to a
  `research_results/r1a-decide/` subfolder so the files themselves keep Rule 12's form.
- **chatgpt-pro `[P-MASTER]` citations** — verifier found the "recurrent" claim overstated
  (`[P-MASTER]` appears only twice); not a defect.
- **Master has no top-level dataset section** — verifier: appropriate layering; the dataset
  picture lives in the sheet's D3 section, which is in-scope. Not a defect.

## 5. Verification to run after applying the fixes

1. `shasum -a 256` the re-saved attachments → confirm prefixes still match the delivery note
   (F4's frontmatter edit and any sheet edits must not change attachment sha256 unexpectedly;
   the spec snapshots must remain byte-identical to master — do not edit them).
2. `grep -rnE 'attachments/|specs/|\.planning/|docs/work|framework-specs/' research_package/
   consolidation/` → confirm zero repo paths in the three authored uploads (F6).
3. Confirm the in-scope list is **identical** across master §3, the prompt, and the
   consolidation prompt, and that B-7/B-12 carve-outs and the B-8 resolution are reflected in
   all three (F1, F10).
4. Confirm the ⚖ fill-in is owned by exactly one stage across master §1, the sheet, and the
   consolidation prompt (F5).
5. Re-confirm the dataset arithmetic in sheet §D3.1 against `simulation_data/Documentation/README.md`
   after F2/F3 (7,422 gold-set trajectories; 13.1 GB fp64 / ~6.5 GB fp32 at S̄ = 10,000).
6. Re-run the package against its design blueprint
   (`docs/work/designs/cross_cutting/trainex-decision-research/2026-07-04-trainex-r1a-decision-research-package-design.md`)
   for conformance.

## 6. Sequencing recommendation

1. **Owner resolves F1 (B-8)** — blocking; everything else can proceed in parallel.
2. Apply F2 + F3 together (same sentence; F3 is the root cause of F2).
3. Apply F4, F5, F9, F10 (master / prompt / consolidation scope-and-pin edits) as one atomic
   "scope-and-grounding" commit.
4. Apply F6, F7, F8, F11 (ERW-rule compliance edits) as one atomic "ERW-compliance" commit.
5. Optionally apply F12, F13 (deep-research precision) as one "tooling-precision" commit.
6. Run §5 verification; only then hand off via `DELIVERY-NOTE.md`.
