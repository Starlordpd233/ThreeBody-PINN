---
status: active
purpose: design
created: 2026-06-19
milestone: untracked
phase: cross-cutting
retirement_trigger: The Issue 03 final consolidation bundles are built and verified, the final resolution doc lands, and a byte-exact reference audit passes
---

# Issue 03 Consolidation Packaging — Core Spec

**This document supersedes the earlier design skeleton at this same path.** It is the
authoritative specification for the Issue 03 (curriculum and training loop) *final*
consolidation round. A later builder agent executes it to produce the upload bundles and
builder script; the user then hands the bundles plus a pasted prompt to one external
final-adjudication agent.

It was produced by reviewing the skeleton against the user's review prompt:

> *"Use an appropriate skill to review and examine your own design to identify any flaws,
> errors, issues, and gaps. The file size limit should not exceed 3–5 MB for best results.
> Also, how can we ensure that the bundle files can be accurately and mechanically bundled
> into the correct file, with proper format, syntax, and organized in a way that can best
> help the agent that later reads these files, since these files are going to be HUGE
> containing all the research reports, results, tables, formulas, and literally everything
> in the individual research reports?"*

Every claim about a file's existence, size, hash, or content below was verified by direct
observation on **2026-06-19** (read-only) against the **specwork worktree**
(`.worktrees/specwork`, branch `milestone/v1.6`). The builder re-derives all sizes and
hashes at build time; **the generated `BUNDLE-MANIFEST.md` is the authoritative record**,
not the numbers transcribed here (they are for grounding and review).

> **Status note (2026-06-19).** The user's rulings resolved the original five open
> decisions (see §5.0). Ground-truthing against specwork then surfaced three further
> items — D-6 (an Issue 02 file in the results folder → **excluded**), D-7 (canonical
> sources two commits behind phase30 → **fast-forwarded**, `milestone/v1.6 @ 05df2619`),
> and D-8 (phase30 worktree retirement → **still pending**, §5.1). With D-6/D-7 ruled, the
> two bundles were **built and byte-exact-verified** on 2026-06-19; full provenance lives
> in the generated, never-uploaded `BUNDLE-MANIFEST.md` (nonce `f26fed61251ff665`).

---

## 1. Purpose and scope

**Goal.** Let *one* external final-adjudication agent review the canonical Issue 03
research package together with all first-version resolution reports, in a single pass,
without exceeding the external UI's 6-attachment cap and without losing provenance or
byte fidelity.

**In scope:** the packaging mechanism — which files are bundled, how they are bundled
byte-exactly, how the bundle is organized for a large-file reader, the builder script
contract, the final-agent prompt contract, and the verification gates.

**Explicitly NOT in scope:** adjudicating Issue 03 itself. This spec never decides
curriculum/training-loop science. Where the attached materials are silent or ambiguous,
the *final agent* surfaces a gap; the *builder* never invents content. (Project STOP
protocol applies to the eventual adjudication, not to this packaging design — but the same
surface-don't-invent posture governs *which inputs* feed the adjudicator, which is why
D-6/D-7 are surfaced rather than decided by the agent.)

## 2. Recommendation (TL;DR)

Use a **single final consolidation agent** with **two byte-exact derived bundles** plus a
**pasted prompt** (the user's confirmed rulings):

| Attachment | File | Uploaded? |
|---|---|---|
| 1 | `canonical-sources-bundle.md` | Yes |
| 2 | `research-results-bundle.md` | Yes |
| — | the final-agent prompt | **Pasted** from §10 — produced as **no separate file** |

That is exactly **2 attachments** — comfortably within the cap of 6. The user's original
A/B → C split is retained only as a **fallback** (§11) for when the single agent cannot
handle the input or produces low-quality output; even then, A/B produce *ledgers*, never
`FINAL-A`/`FINAL-B` documents that could become accidental authorities.

Bundling (not splitting) is preferred because the binding constraint is *attachment
count*, not size — and bundling preserves every original byte-for-byte instead of
compressing evidence into lossy summaries.

## 3. Review of the skeleton — findings

The skeleton was directionally correct (single-agent primary, originals bundled,
quarantine list, anti-majority-vote prompt). Applying the review prompt surfaced the
following, ordered by severity. Resolutions are specified in the later sections cited.

| # | Severity | Finding | Resolution |
|---|---|---|---|
| **C1** | **CRITICAL** | The skeleton says "adapt the Issue 02 `make_bundles.py`" and lists "delimiter collision" only as an *abort* condition. But **four of the six canonical sources are themselves bundles** (`TASK-AND-CONSTRAINTS-BUNDLE.md`, `CLAIMS-AND-FACTS-BUNDLE.md`, `FRAMEWORK-SPECS-BUNDLE.md`, `BASELINE-REPORTS-BUNDLE.md`) and contain lines beginning `===== ` and `===== BEGIN FILE … =====`. Issue 02's `check_no_delimiter_collision()` calls `sys.exit()` on any line starting with `===== `. **Reusing that scheme would abort and could never build the canonical bundle.** The skeleton's own recommended tool is self-defeating. | §8.1 — collision-proof **per-build nonce delimiter** + absence verification. |
| **C2** | **RESOLVED** | Kimi report `R6` was missing at design time. **User ruling: Kimi is removed from the v1 set** — it is not part of this round. No "missing include" hazard remains. | §5.0 — Kimi dropped; results set is the 7 reports in §6.2. |
| **C3** | **RESOLVED** | The two Gemini files were near-duplicates. **User ruling: they are now consolidated into one `gemini_deep_research.md`.** No supersede/family logic is needed. | §5.0 — single Gemini report (`R6`). |
| **C4** | **HIGH (coordination)** | Output location + source-of-truth branch were undefined, and the canonical sources turned out to be **two commits behind** the phase30 branch. | §5 D-7 + §7 — build in **specwork**; output to a new `research_result/consolidation_input/`; reconcile the canonical-source version first. |
| **C5** | **MED (units/expectation)** | User said "3–5 MB"; skeleton wrote "MiB" without defining it, and implied the files are "HUGE". **Reality: each finished bundle ≈ 0.28–0.39 MB; combined < 0.7 MB — an order of magnitude under the ceiling.** | §8.6 — define units (MiB), record measured sizes, keep the gate as a *safety* backstop. |
| **C6** | **MED (readability)** | Because the canonical bundle is a bundle-of-bundles, it will contain **inner** `===== BEGIN FILE … =====` markers. The reader must be told these are ordinary verbatim content and that **only outer markers carry the nonce**, else it mis-navigates. | §8.5 + §9 header — explicit nested-bundle notice + generated heading index. |
| **C7** | **RESOLVED** | **User ruling: anonymize** the reports. The Issue 02 model is kept (R-tags, manifest-only map, self-ID vendor-token scan, "do NOT upload the manifest"). | §5.0 + §6.2 + §9.4. |
| **C8** | **LOW (correctness)** | At least one input **lacks a trailing newline** (`qwen-03-resolution.md`, `Fusion-03-resolution.md`). Byte-exactness must survive this. | §8.2 — preserve the Issue 02 framing mechanism (verified round-trips no-trailing-newline); §9.3 mandates a no-trailing-newline self-test. |
| **C9** | **CONFIRMED OK** | `Fusion-03-resolution.md` is a **synthesis/adjudication, not a raw first-round vote** — its first line reads *"I now have a thorough panel analysis. Below is my adjudication…"*. It is included (the user wants all v1 reports) but the prompt must neutralize any double-counting **without naming which tag it is** (that would de-anonymize). | §10 — generic "synthesis gets no extra weight" clause. |

## 4. What the final agent receives — workflow shape

1. User builds the two bundles with `make_bundles.py` (§9), which self-verifies byte-exact
   round-trip and writes `BUNDLE-MANIFEST.md` (kept project-side, **never uploaded**).
2. User **attaches the two bundles** and **pastes the prompt** (§10) — no prompt file is
   produced; the attach-list lives in §10's user-facing header and in the manifest.
3. The agent works *only* from the two attached files, produces an independent claim
   ledger from the canonical bundle **before** reading the results bundle, then returns the
   output schema in §10.
4. The returned doc lands as the Issue 03 `…-resolution-doc.md`; the manifest de-references
   the R-tags for provenance afterward.

## 5. Open decisions

### 5.0 Resolved this round (user rulings, 2026-06-19)

| Was | Decision | Ruling |
|---|---|---|
| D-1 | Kimi `R6` missing | **Removed** — Kimi is not part of the v1 set; no longer bundled. |
| D-2 | Gemini pair | **Consolidated** into one `gemini_deep_research.md`; single Gemini report. |
| D-3 | Anonymize? | **Yes** — keep the Issue 02 anonymization model. |
| D-4 | Build location | **specwork worktree**; outputs near the v1 results folder (§7). |
| D-5 | Prompt delivery | **Paste** the prompt; produce **no** standalone prompt file. |

### 5.1 Build-blockers — **resolved 2026-06-19** (D-8 pending)

D-6 and D-7 were the build gates (guard in `make_bundles.py` §9.1) and are now ruled; the
bundles were built and verified. D-8 is a git-hygiene decision that did not block the build
but must be ruled before the phase30 worktree is touched.

#### D-6 — An Issue 02 file is sitting in the v1 results folder  ·  **RESOLVED: exclude (A)**
`research_result/v1-research-reports/issue-03-resolution-document.md` (57,260 B,
`6930368854f0`) has the first heading **"Resolution Document — Issue 02: Data Pipeline and
Validation"** and an inventory of Issue 02 spec files. Despite the `issue-03` filename, its
**content is Issue 02**. The user's "all v1 reports live in that folder" statement is
blanket; this one file contradicts it.
- **A (recommended):** **Exclude** it (quarantine, reason recorded). Feeding an Issue 02
  resolution to the Issue 03 adjudicator would corrupt the verdict. The §8.4 Issue-02-heading
  guard enforces the exclusion mechanically.
- **B:** Include it anyway (only if the user knows it carries Issue 03 content the heading
  mislabels — not what the bytes show).
- *Never:* silently include or silently exclude — the user's blanket statement is surfaced.

#### D-7 — Canonical sources are two commits behind the phase30 branch  ·  **RESOLVED: fast-forward (A) → `milestone/v1.6 @ 05df2619`**
specwork (`milestone/v1.6` @ `f03137c7`) holds the canonical `upload/` set at
`FRAMEWORK-SPECS-BUNDLE.md` = 179,853 B / `e9636b4c828b` and
`RESEARCH-CONTEXT-MASTER.md` = 4,171 B / `9ba80f493fb5`. The phase30 branch
(`codex/phase30-package-audit-fixes` @ `05df2619`) is **two commits ahead** —
`3781d1a6 docs(30): correct phase 25 evidence paths in ctl spec` and
`05df2619 docs(30): refresh issue-03 research package baseline` — and carries the
**later-committed** versions (`73c1fd9d693a` / `ea501d1ceebe`). `f03137c7` is a direct
ancestor of `05df2619`, so the two are reconcilable by fast-forward.
- **A (recommended):** **Fast-forward `milestone/v1.6` to `05df2619`** (clean FF; adds the
  phase-25 spec fix + the package refresh), then build the canonical bundle from specwork's
  now-current sources. This honors "work in specwork," uses the latest committed sources,
  and fully contains the phase30 branch.
- **B:** Build from specwork's **current** `milestone/v1.6` sources as-is (two commits
  stale); reconcile phase30 separately. Risks adjudicating against slightly outdated
  framework-spec text.
- *Either way* the byte-exact canonical bundle pins to whichever version is chosen and
  records it in the manifest.

#### D-8 — phase30 worktree disposition (does not block the build)  ·  **PENDING**
The user wants the `phase30-package-audit-fixes` worktree gone. It is a **real registered
worktree** on a 29-commit branch (the entire Phase 30 research-package assembly), two
commits ahead of `milestone/v1.6`. Removing the worktree directory does not delete commits
(the branch ref persists), but deleting the branch would. Under D-7 **A**, once
`milestone/v1.6` contains `05df2619` the branch is fully merged and the worktree is safely
redundant.
- **Recommended:** after D-7 A, retire the worktree **with a recovery tag**
  (`archive/phase30-pre-retire` on `05df2619`) and explicit destructive-op approval, then
  `git worktree remove`. Branch deletion only after the user confirms nothing else needs it.
- *Never:* remove the worktree or delete the branch without explicit approval + recovery
  checkpoint (project destructive-git governance).

## 6. Authoritative input inventory

All paths are repo-relative within the **specwork worktree**
(`.worktrees/specwork/`), under
`pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/`.

### 6.1 Canonical source inputs (`S1–S6`)

Source dir: `research_package/upload/`. **Hashes below are the post-fast-forward
`milestone/v1.6 @ 05df2619` values (D-7 A) — the version the bundles were built from; the
builder re-derives them at build time and the manifest records the full SHA-256s.**

| Tag | File | Bytes | SHA-256(12) | Self-bundle? | Treatment |
|-----|------|------:|-------------|:---:|-----------|
| `S1` | `RESEARCH-CONTEXT-MASTER.md` | 4,171 | `ea501d1ceebe` | no | Orientation, source hierarchy, manifest of companions |
| `S2` | `TASK-AND-CONSTRAINTS-BUNDLE.md` | 44,339 | `b7187d00b724` | **yes** | Task, hard constraints, output expectations |
| `S3` | `03-curriculum-and-training-loop.md` | 49,635 | `94c3c03b1323` | no | The Issue 03 source doc (decisions, findings) |
| `S4` | `CLAIMS-AND-FACTS-BUNDLE.md` | 22,353 | `11807cabb98a` | **yes** | Claims register + verified facts |
| `S5` | `FRAMEWORK-SPECS-BUNDLE.md` | 179,949 | `73c1fd9d693a` | **yes** | Framework-spec snapshots (governing technical source) |
| `S6` | `BASELINE-REPORTS-BUNDLE.md` | 99,296 | `f28f5a4746f1` | **yes** | Baseline-report snapshots |

Canonical raw total ≈ **390.4 KiB** (D-7 A). The four "self-bundle" files carry inner
`===== BEGIN FILE … =====` markers — the C1 hazard; handled by §8.1.

These are **source-context** materials, not prior model votes. Where they are silent or
ambiguous, the final agent records a gap rather than inferring.

### 6.2 Research result inputs (`R`-tags)

Source dir: `research_result/v1-research-reports/` (in the specwork worktree; currently
**untracked** working-tree files). The builder reads only the files in the explicit source
map below — **never by globbing the directory** — so no stray file can leak in.

| Tag | File | Bytes | SHA-256(12) | Status / treatment |
|-----|------|------:|-------------|--------------------|
| `R1` | `03-resolution-doc.md` | 57,819 | `d696b601f0eb` | Independent first-version report |
| `R2` | `doc-03-adjudication.md` | 47,478 | `c1a12efe49da` | Independent first-version report |
| `R3` | `doc-03-research-adjudication.md` | 55,221 | `7a877b20bf2d` | Independent first-version report |
| `R4` | `doc-03-adjudication-resolution.md` | 42,645 | `10ee26b34975` | Independent first-version report |
| `R5` | `qwen-03-resolution.md` | 11,132 | `ba2cbe8174e4` | Independent first-version report (no trailing newline) |
| `R6` | `gemini_deep_research.md` | 48,267 | `34e45c41d97d` | Independent first-version report (consolidated Gemini, per D-2) |
| `R7` | `Fusion-03-resolution.md` | 26,170 | `bfecf583dffb` | **Synthesis-style input, not an independent vote** (no trailing newline) |

Results raw total ≈ **282.0 KiB** (7 reports). `R`-tag → file binding is fixed in the
manifest; the uploaded bundle uses the tags only. Agreement among reports is **not**
evidence; only source-grounded claims become final.

`issue-03-resolution-document.md` is **excluded pending D-6** (see §6.3).

### 6.3 Quarantine list (must not appear in any upload)

| File | Bytes | Reason |
|------|------:|--------|
| `issue-03-resolution-document.md` | 57,260 | First heading is *"Resolution Document — Issue 02: Data Pipeline and Validation"* — **wrong issue**. Excluded per **D-6 A** (pending confirmation). |

Because the builder reads only the explicit source map (§9.1), any other unlisted file in
the folder is excluded by construction. Quarantined paths + reasons are recorded in the
manifest, never uploaded.

## 7. Output artifacts

Written to a new `research_result/consolidation_input/` (sibling of `v1-research-reports/`,
per the user's "near the v1 folder" instruction — a deliberate deviation from Issue 02,
which placed `consolidation_input/` at the issue root).

| Artifact | Uploaded? | Purpose |
|----------|:---:|---------|
| `canonical-sources-bundle.md` | **Yes** | Byte-exact bundle of `S1–S6` |
| `research-results-bundle.md` | **Yes** | Byte-exact bundle of the confirmed `R`-tags |
| `BUNDLE-MANIFEST.md` | **No — never** | Tag→path map, full SHA-256s, sizes, self-ID scan, quarantine list, decisions D-1…D-8 as resolved, build date, nonce, chosen canonical version (D-7), **and the paste-ready prompt + attach-list copy** |
| `make_bundles.py` | No | Reproducible builder + self-test (§9) |

No `final-consolidation-prompt.md` is produced (D-5). The authoritative prompt is §10 of
this design doc; the builder copies it verbatim into the manifest's "PASTE THIS" block so
the user has it beside the bundles without an extra (or uploadable) file.

## 8. Mechanical bundle format

Adapts the Issue 02 byte-exact framing, with one essential change (§8.1) to survive the
bundle-of-bundles inputs.

### 8.1 Collision-proof delimiter (the C1 fix)

The Issue 02 delimiter (`===== BEGIN FILE … =====`) collides with content that already
contains that token. Replace it with a **per-build nonce-namespaced** delimiter:

1. Generate `NONCE` = 16 lowercase hex chars (8 bytes from `os.urandom`).
2. Form the marker token `ISSUE03-SECTION-<NONCE>`. **Verify** this token does not appear
   in any source file's bytes; if it does (astronomically unlikely), regenerate `NONCE`.
3. Frame each section exactly as:

   ```text
   ===== BEGIN ISSUE03-SECTION-<NONCE> REPORT R1 (57819 bytes, sha256 d696b601f0eb) =====
   <verbatim source bytes>
   ===== END ISSUE03-SECTION-<NONCE> REPORT R1 =====
   ```

   Canonical source sections use `FILE` and the `S`-tag in place of `REPORT R1`:

   ```text
   ===== BEGIN ISSUE03-SECTION-<NONCE> FILE S5 (179853 bytes, sha256 e9636b4c828b) =====
   <verbatim source bytes>
   ===== END ISSUE03-SECTION-<NONCE> FILE S5 =====
   ```

Because extraction keys on the literal `ISSUE03-SECTION-<NONCE>`, the **inner**
`===== BEGIN FILE … =====` lines that live inside `S2/S4/S5/S6` can never match — they
lack the nonce. The inner bytes are copied verbatim and untouched.

Extraction regex (Python `bytes`, `re.DOTALL`), with `N` = the nonce and `K` ∈ {`REPORT`,`FILE`}:

```python
pat = re.compile(
    rb"===== BEGIN ISSUE03-SECTION-" + N + rb" " + K + rb" (.+?)"
    rb"(?: \(\d+ bytes, sha256 [0-9a-f]{12}\))? =====\n"
    rb"(.*?)"
    rb"\n===== END ISSUE03-SECTION-" + N + rb" " + K + rb" (.+?) =====\n",
)
```

### 8.2 Byte-exact framing (preserve the Issue 02 mechanism)

Build each section as `b"\n" + BEGIN + b"\n" + data + b"\n" + END + b"\n"`. The capture
group is non-greedy up to the `\n` immediately before `END`, so a body that does **not**
end in a newline round-trips exactly (the framing `\n` is structural, not part of the
content). This is the C8 guarantee; §9.3 requires a self-test fixture proving it.

### 8.3 Verification

After writing each bundle, re-extract every section and compare **full** SHA-256 against
the in-memory originals. Abort on any mismatch. `--verify` re-runs this against the
on-disk bundles and the manifest at any later time.

### 8.4 Abort conditions (hard failure)

- Missing manifest / source-map.
- Any declared **include** file missing.
- Duplicate tag.
- Duplicate **full** SHA-256 across two included files.
- `BEGIN` vs `END` tag/kind mismatch.
- Nonce-absence verification fails and cannot be resolved by regeneration.
- Round-trip SHA-256 mismatch on any section.
- Any uploaded artifact **> 5 MiB**.
- More than **6** files marked for upload.
- Any unresolved build-blocker (D-6, D-7) in the source map.
- An `R`-slot whose first heading matches an **Issue 02** title (the
  `issue-03-resolution-document.md` guard / D-6 enforcement) — refuse rather than mislabel.

### 8.5 Warn conditions (proceed, but print + record)

- Any uploaded artifact between **3 MiB and 5 MiB**.
- Self-ID vendor tokens found inside a report body (anonymization is best-effort).

### 8.6 Size policy (units + reality)

Use **MiB** (1 MiB = 1,048,576 bytes); "3–5 MB" maps to **target < 3 MiB, warn 3–5 MiB,
hard-fail > 5 MiB**, applied per uploaded artifact. Measured reality (2026-06-19): canonical
bundle ≈ 0.39 MB, results bundle ≈ 0.28 MB, **combined < 0.7 MB** — about an order of
magnitude under the ceiling. The gate is therefore a *safety backstop* against future
additions (converted PDFs, extra reports), not a constraint that binds today.

## 9. Builder contract — `make_bundles.py`

Small, standard-library-only Python (no third-party deps), modeled on the Issue 02 builder.

### 9.1 Source map and decision guard

At the top of the script, an explicit, reviewable mapping (in git) — **not** filename
globbing — declares the evidence set and pins the open decisions:

```python
DECISIONS_RESOLVED = True           # D-6 and D-7 ruled 2026-06-19
CANONICAL_VERSION  = "specwork"     # or "phase30-ff" per D-7
SOURCES_DIR = "research_package/upload"               # S1..S6, repo-relative (specwork)
RESULTS_DIR = "research_result/v1-research-reports"   # R-tags, repo-relative (specwork)
RESULTS = [                                           # explicit; no globbing
    ("R1", "03-resolution-doc.md",            "include", None),
    ("R2", "doc-03-adjudication.md",          "include", None),
    ("R3", "doc-03-research-adjudication.md", "include", None),
    ("R4", "doc-03-adjudication-resolution.md","include", None),
    ("R5", "qwen-03-resolution.md",           "include", None),
    ("R6", "gemini_deep_research.md",         "include", None),
    ("R7", "Fusion-03-resolution.md",         "include", "synthesis"),  # C9; no extra weight
]
QUARANTINE = [ ("issue-03-resolution-document.md", "issue-02 heading (D-6)") ]
```

The build entry point asserts `DECISIONS_RESOLVED`, that every `include` path exists, and
that no `include` file's first heading matches an Issue 02 title, before doing any work.

### 9.2 CLI

```sh
python3 make_bundles.py --selftest                 # fixtures only; no real inputs
python3 make_bundles.py --build --build-date 2026-06-19
python3 make_bundles.py --verify                   # re-extract on-disk bundles vs manifest
```

### 9.3 Required self-tests (must pass before `--build` is trusted)

- **Nested-bundle fixture (the C1 test):** a fixture whose body literally contains
  `===== BEGIN FILE inner =====`, inner content, `===== END FILE inner =====`. Prove it
  round-trips byte-exact and that extraction returns exactly one outer section.
- **No-trailing-newline fixture (C8):** a body with no final `\n` round-trips exactly.
- **Unicode / blank-line / table / `$…$` formula / code-fence fixture:** round-trips exactly.
- **Nonce-absence:** a fixture containing the chosen marker token forces a regenerate.
- **Negative guards:** duplicate tag; duplicate hash; missing include; Issue-02-heading
  slot; size-gate breach; upload-count breach — each must abort.

### 9.4 Manifest fields

Build date + builder version + **nonce** + **chosen canonical version (D-7)**; and per file:
source path, upload tag, role/treatment, bytes, **full** SHA-256, first heading/title,
include/quarantine status (+ reason), synthesis flag, self-ID token hits. Plus the resolved
values of D-1…D-8 and the **paste-ready prompt + attach-list**. The manifest header repeats
the Issue 02 warning: **do NOT upload — it de-anonymizes the tags.**

## 10. Final-agent prompt contract

The prompt is authored here (this section is its single source of truth) and **pasted** by
the user (D-5). A user-facing header lists exactly which files to attach; below a horizontal
rule, the verbatim prompt. Required clauses:

**User-facing header (not pasted as part of the prompt)**

```text
Attach these two files, then paste everything below the line:
  1. canonical-sources-bundle.md
  2. research-results-bundle.md
```

**Controlling instruction**

```text
You are the final Issue 03 adjudicator. Work ONLY from the attached files. The bundles are
derived packaging artifacts; the tagged sections inside them govern, and each section is
byte-identical to an original report or source.

Some attached SOURCE sections are themselves bundles and contain their own inner
"===== BEGIN FILE … =====" lines. Treat those inner lines as ordinary file content. Only
the outer markers that carry the token ISSUE03-SECTION-<nonce> delimit sections.

Do NOT vote, average, or merge by majority. Report agreement is NOT evidence; the identity
of the model behind a report is irrelevant and is not provided. Some reports may overlap
heavily, and one report may be a synthesis or merge of the others — give NO report extra
weight for restating others. Every final claim must cite the canonical source section(s) it
rests on and the report section(s) it came from.

First, produce an INDEPENDENT claim ledger from the canonical-sources bundle BEFORE reading
the research-results bundle. Then map every report claim onto that ledger.

Classify each claim: accepted | rejected | modified | surface_to_user | defer.
If the attached sources are silent or ambiguous, do NOT infer — mark surface_to_user or
defer and record it as a gap. If a report cites material that is not attached, treat it as
unavailable. Preserve every dissent and minority position.
```

**Required output schema**

1. The final Issue 03 resolution doc.
2. **Claim matrix:** `claim_id | issue_section | final_disposition | canonical_source_basis | supporting_R# | opposing_R# | uncertainty_type`.
3. **Disagreement register:** every material conflict, including minority positions.
4. **Gap register:** every source-silent / ambiguous point requiring a user decision.
5. **Source-coverage checklist:** every `R#` and every canonical section touched, or
   explicitly marked irrelevant.
6. **Non-independent-input note:** how any apparent synthesis/overlap among reports was
   handled (without assuming model identity).

## 11. Fallback workflow (only if the single agent struggles)

Do **not** ask A/B to write `FINAL-A`/`FINAL-B`. Instead:

- **Agent A:** source-led claim ledger from the canonical + results bundles.
- **Agent B:** disagreement-led conflict ledger from the same inputs.
- **Agent C (final):** must produce its **own** independent source-led ledger **before**
  reading A and B. A/B outputs are navigation pointers only, never evidence. If C lacks the
  original bundle text for a claim, it marks the claim unresolved rather than trusting an
  A/B summary.

A/B agreement is not evidence. The split is by analytical role, never by an arbitrary "half
the documents" cut.

## 12. Acceptance criteria

- The external final agent needs **exactly 2 attachments** on the primary path (2 bundles;
  prompt pasted).
- Every included original is **extractable byte-for-byte** from its bundle (round-trip
  SHA-256 verified at build and re-checkable via `--verify`).
- Every uploaded artifact is **< 3 MiB** in this build; the builder hard-fails any future
  artifact **> 5 MiB**.
- The manifest proves which local file produced each tag, records the chosen canonical
  version (D-7), and records D-1…D-8 as resolved.
- The Issue 02 stray file is excluded with a recorded reason (D-6) and appears in no upload.
- The prompt forbids majority voting and requires source-grounded dispositions, an
  independent canonical-first ledger, and source-silence-as-gap, without revealing model
  identity or which report is a synthesis.

## 13. Governance and provenance

- **ERW alignment** (`docs/runbooks/external-research/2026-06-11-external-research-workflow.md`):
  uploads carry **zero repo paths**; companion files are referred to by the tags/roles in
  the bundle header; the agent is told it works from attached files only; the manifest (the
  only place provenance and repo routing live) is **never uploaded**; source-silence-is-a-gap
  culture is extended to the external agent via the prompt.
- **Byte-exact provenance:** originals govern; bundles are derived artifacts; the
  `--verify` round-trip is the re-derivable proof.
- **Surface-don't-invent:** this spec packages evidence; it does not adjudicate Issue 03.
  The semantic calls are the final agent's, surfaced as gaps. The packaging-layer choices
  that determine *which* inputs reach the adjudicator (D-6 stray file, D-7 source version)
  are the user's, surfaced here — never decided by the builder.
- **Destructive-git governance:** the phase30 worktree/branch (D-8) is retired only with
  explicit approval and a recovery tag; never removed unilaterally.
