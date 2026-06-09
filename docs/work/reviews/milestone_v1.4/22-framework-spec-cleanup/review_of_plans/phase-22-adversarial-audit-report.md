---
phase: 22
review_type: adversarial-plan-audit
status: consumed
superseded_by: docs/work/reviews/milestone_v1.4/22-framework-spec-cleanup/review_of_plans/2026-06-09-phase22-review-closeout-matrix.md
date: 2026-06-08
closed_out: 2026-06-09
closeout_verdict: ALL-MATERIAL-FINDINGS-RESOLVED
---

# Adversarial Audit Report: Phase 22 Planning Artifacts

**Audit Date:** 2026-06-08
**Auditor:** Multi-Dimensional Adversarial Review Panel (Logical Integrity + Execution Clarity + Operational Resilience)
**Scope:** Phase 22 planning artifacts (`.planning/milestones/v1.4-phases/22-framework-spec-cleanup/22-0[1-5]-PLAN.md`, plus `22-RESEARCH.md`, `22-CONTEXT.md`, `22-VALIDATION.md`)
**Execution Risk Score:** 8 / 10
**Confidence:** HIGH

---

## 1. Executive Summary

This audit assesses the Phase 22 framework-spec cleanup planning artifacts for readiness before autonomous execution. The five interdependent plans (22-01 through 22-05) describe a detector build, two parallel repair waves (WS-A), a comment census/preservation audit (WS-B), and phase closure.

**Overall Verdict: NOT READY FOR AUTONOMOUS EXECUTION**

Of 10 top-priority findings, **6 are CRITICAL severity** and **4 are HIGH severity**. All 10 findings carry the `must_fix_before_execution` flag. The phase cannot execute safely in its current state without material risk of spec corruption, phase deadlock, false verification failures, and irreversible edit damage.

**Key Concern Count:**

| Dimension | CRITICAL | HIGH | MEDIUM | LOW |
|-----------|----------|------|--------|-----|
| Logical Integrity | 2 | 5 | 4 | 3 |
| Execution Clarity | 3 | 3 | 7 | 3 |
| Operational Resilience | 5 | 6 | 3 | 2 |
| **Total** | **10** | **14** | **14** | **8** |

---

## 2. Audit Scope & Methodology

**Scope:**
- All five plan files: `22-01-PLAN.md` through `22-05-PLAN.md`
- Supporting research: `22-RESEARCH.md`, `22-CONTEXT.md`, `22-VALIDATION.md`
- Live corpus verification: `ctl_instruction.md`, `pinn_architecture.md`, `sampling_method.md`
- Git state: tags, branches, `.gitignore`

**Methodology:**
1. Cross-reference verification targets against live corpus (grep counts, tag existence)
2. Trace dependencies between plans for circularity, false parallelism, and unnecessary serialization
3. Inspect every "verify" step for mechanical realizability vs. semantic hand-waving
4. Check detector contract stability (output format, CLI modes, regression behavior)
5. Audit preservation gates for contradiction with permitted edits
6. Assess rollback, recovery, and state-tracking mechanisms

---

## 3. Top Priority Findings

### Finding 1 — CRITICAL: Missing Pre-Phase Baseline Snapshot
**Plans affected:** 22-01, 22-04, 22-05
**Location:** `22-01-PLAN.md:83`; `22-04-PLAN.md:58`; `22-05-PLAN.md:67-73`

The `v1.4-pre-phase-22` tag does not exist (`git tag -l 'v1.4*'` shows only through `v1.4-pre-phase-21`), yet 22-04 and 22-05 depend on it for the pre-WS-A census snapshot and G3 content-preservation audit. 22-04 mandates a hard STOP if the tag is missing, blocking the phase indefinitely. No fallback mechanism (e.g., `git log --before=<date> -1 -- <files>`) is specified.

**Why it matters:** Without a baseline snapshot, the G3 content-preservation audit has no "before" state to compare against. The phase literally cannot verify its own success criterion.

**Must fix before execution:** YES

---

### Finding 2 — CRITICAL: Incorrect Author-Comment Census Count
**Plans affected:** 22-01, 22-02, 22-03, 22-04, 22-05
**Location:** `22-01-PLAN.md:83`; `22-RESEARCH.md:317`; `22-CONTEXT.md:30`

Plans assert 26 author-marker lines (13 ctl + 13 pinn), but live corpus shows 22 marker lines (13 ctl + 9 pinn + 0 sampling). The detector is calibrated to the wrong target. If the detector expects 26 and finds 22, the census diff reports 4 missing comments — a false preservation failure blocking 22-04 and 22-05.

**Why it matters:** Every verification gate that depends on "26" as a hard target is unsatisfiable. The preservation predicate fails by construction.

**Must fix before execution:** YES

---

### Finding 3 — CRITICAL: Detector CLI Output Format Is Underspecified
**Plans affected:** 22-01, 22-02, 22-03, 22-04, 22-05
**Location:** `22-01-PLAN.md` Task 2; all downstream verify blocks

Downstream plans grep for magic strings (`fenced div|multiline table|: Table|separator row`, `survivor|$$|begin{aligned}|\command`) without a stable output contract. If the implementer changes formatting (e.g., `DEFINITE` -> `ERROR`, different column order), every verify step breaks silently. A green verify step is indistinguishable from "no findings" vs. "grep pattern no longer matches."

**Why it matters:** The entire verification pipeline rests on an informal string-matching contract. A single formatting change in the detector silently invalidates all downstream verification.

**Must fix before execution:** YES

---

### Finding 4 — CRITICAL: G3 Content-Preservation Audit Is Unmechanized and Contradicts D-05
**Plans affected:** 22-02, 22-03, 22-04, 22-05
**Location:** `22-02-PLAN.md:96-99`; `22-03-PLAN.md:88-93`; `22-05-PLAN.md:78`

G3 claims "every changed line differs only in delimiters/structure/whitespace/representation" but provides no mechanized verification. "Differs only in delimiters" is a semantic judgment, not a mechanical check. Worse, the preservation check contradicts permitted D-05 wrapper repairs: a permitted wrapper repair changes comment bytes, so a text-hash compare flags it as semantic change and STOPs, even though D-05 explicitly allows it.

**Why it matters:** An autonomous agent cannot execute a semantic judgment without inventing criteria (violating CLAUDE.md governance) or stopping constantly (blocking progress). The contradiction with D-05 means the audit is guaranteed to fail on permitted repairs.

**Must fix before execution:** YES

---

### Finding 5 — CRITICAL: Parallelism Claims Are False — Shared Mutable State
**Plans affected:** 22-02, 22-03
**Location:** `22-02-PLAN.md:61-84`; `22-03-PLAN.md:59-78`

Plans claim "zero overlap" parallel execution, but both edit files sharing cross-references, the same detector tool, the same `VER-05` ledger (`16-ISSUE-LEDGER.md`), and the same git branch. There is no merge strategy, ledger-locking mechanism, or coordination protocol. Race conditions on git commits, ledger appends, and detector state are inevitable.

**Why it matters:** Two autonomous agents running these plans concurrently will corrupt shared state. The "parallel" claim is a fiction that invites race conditions.

**Must fix before execution:** YES

---

### Finding 6 — CRITICAL: 22-03 Blocked by Unnecessary Footnote Probe Dependency
**Plans affected:** 22-01, 22-03
**Location:** `22-01-PLAN.md` Task 3; `22-03-PLAN.md` dependency declaration

Plan 22-03 depends on 22-01 completion, but 22-01 Task 3 blocks on a human footnote probe. `ctl_instruction.md` has zero footnotes (confirmed in `22-RESEARCH.md`). If the human never responds, 22-03 is unnecessarily blocked, violating the parallel wave design.

**Why it matters:** Serializes parallel waves on an irrelevant dependency. The phase's schedule is artificially extended by a probe that has no applicability to the file being repaired.

**Must fix before execution:** YES

---

### Finding 7 — HIGH: No Rollback or Recovery Mechanism
**Plans affected:** 22-02, 22-03
**Location:** `22-02-PLAN.md` Task 2; `22-03-PLAN.md` Task 2

Repair plans edit framework spec files but never mention git commits per construct or file-revert instructions. If a math conversion introduces a new D1 parse error, the plan says "revert any region to IN_PROGRESS in the ledger" but does not say how to revert the actual file edit. Without git-based rollback, the agent must manually reconstruct original text — error-prone and potentially compounding defects.

**Why it matters:** A single bad conversion corrupts a framework spec file. Without rollback, the corruption persists across sessions and may be compounded by subsequent "fixes."

**Must fix before execution:** YES

---

### Finding 8 — HIGH: D3 LaTeX Lint Regex Is Both Over- and Under-Inclusive
**Plans affected:** 22-01, 22-02, 22-03
**Location:** `22-01-PLAN.md:120-128`; `22-02-PLAN.md:96`; `22-03-PLAN.md:88`

The D3 regex `(?<!\\)[_^](?!\\{)[A-Za-z]{2,}` false-positives on Markdown emphasis like `_italic_` and misses single-letter subscripts like `x_i`. No false-positive suppression mechanism exists. A single false positive in a heavily-math file could block the entire phase.

**Why it matters:** The agent must either incorrectly "fix" valid notation (violating D-02) or leave the finding unaddressed (blocking G2). There is no escape hatch.

**Must fix before execution:** YES

---

### Finding 9 — HIGH: Sanity Gate Tests Only Inline Math, Not Block Math
**Plans affected:** 22-01
**Location:** `22-01-PLAN.md:127-128`; `22-RESEARCH.md:417-424`

The sanity gate renders only `$x^2$` (inline math) but does not verify block math (`$$...$$`), which is the primary defect class in `ctl_instruction.md`. A plugin with block-math parsing disabled would pass the gate while failing to catch the dominant defect class, giving false confidence.

**Why it matters:** The detector's primary purpose is to catch block math defects. If the sanity gate doesn't test block math, a broken detector installation gives a false positive "all clear."

**Must fix before execution:** YES

---

### Finding 10 — HIGH: Pandoc-to-GFM Table Conversion Is Lossy Without Per-Construct Checkpoints
**Plans affected:** 22-02
**Location:** `22-02-PLAN.md` Task 1

Pandoc-to-GFM table conversion claims "preserve every cell byte-for-byte" but GFM cannot represent rowspan/colspan/multi-line cells. Multi-line cell joining is ambiguous (spaces vs. `<br>`). Verification runs only after all 7 constructs are converted, making bisection expensive if the second table introduces a new D4 survivor. Without per-construct git commits, recovery is manual and error-prone.

**Why it matters:** Structural information loss in tables is irreversible. Without per-construct checkpoints, a bad conversion corrupts the table and the agent cannot easily determine which construct caused the regression.

**Must fix before execution:** YES

---

## 4. Cross-Cutting Themes

### Theme 1: The Detector Is the Linchpin, but It Is Underspecified
**Affected plans:** 22-01, 22-02, 22-03, 22-04, 22-05 (6 findings)

The detector is treated as a solved problem in 22-01, yet every downstream wave's verification depends on capabilities never specified: no output schema, no machine-readable mode, no version checks, no false-positive suppression, no snippet render/comparison utility, and an incomplete sanity gate. The detector spec needs to be a first-class contract before any repair plan can safely rely on it.

### Theme 2: Verification Gates Are Semantic, Not Mechanical
**Affected plans:** 22-02, 22-03, 22-04, 22-05 (5 findings)

Every "verify" step requires a human judgment call ("genuinely math", "differs ONLY in delimiters", "conversion noise", "evidence-bound"). An autonomous agent cannot execute these without either inventing criteria (violating CLAUDE.md governance) or stopping constantly (blocking progress). The plans conflate "human oracle" with "automated gate" and provide no mechanized equivalence check.

### Theme 3: Baseline and State Management Are Afterthoughts
**Affected plans:** 22-01, 22-02, 22-03, 22-04, 22-05 (5 findings)

The plans assume a clean starting state, stable baselines, and forward-only progress. There is no mechanism to create a pre-edit snapshot, track wave status across sessions, recover from bad edits, or verify that negative controls have not been contaminated by prior phases. The missing pre-phase tag and lack of rollback are symptoms of this systemic neglect.

### Theme 4: Parallelism Claims Are False — Shared Mutable State Everywhere
**Affected plans:** 22-02, 22-03 (2 findings)

Plans 22-02 and 22-03 advertise parallel execution for efficiency but share the git branch, ledger file, detector tool, and regression fixtures without any coordination protocol. The dependency graph also fails to respect file-specific needs: 22-03 is blocked on a footnote probe it does not need because `ctl_instruction.md` has zero footnotes.

### Theme 5: The Census/Preservation Handoff Is Built on Unverified Assumptions
**Affected plans:** 22-04, 22-05 (3 findings)

The WS-B handoff (22-04) and closure (22-05) depend on a census count that was never verified against live corpus, a preservation check that contradicts permitted D-05 wrapper repairs, and a reconciliation algorithm that does not exist. The entire "author comment preservation" guarantee rests on assumptions that collapse under inspection.

---

## 5. Per-Dimension Deep Dive

### 5.1 Logical Integrity

| # | Severity | Plans | Location | Finding |
|---|----------|-------|----------|---------|
| 1 | CRITICAL | 22-01, 22-04, 22-05 | `22-01-PLAN.md:83`; `22-04-PLAN.md:58`; `22-05-PLAN.md:67-73` | Missing `v1.4-pre-phase-22` tag blocks pre-WS-A census and G3 audit. No fallback. |
| 2 | CRITICAL | All five | `22-01-PLAN.md:83`; `22-RESEARCH.md:317`; `22-CONTEXT.md:30` | Author-comment census count is 22 (live), not 26 (asserted). Detector calibrated to wrong target. |
| 3 | HIGH | 22-01, 22-02, 22-03 | `22-01-PLAN.md:127-128`; `22-02-PLAN.md:69-72`; `22-03-PLAN.md:66-68` | D4 survivor scan does not distinguish Pandoc multiline table separator rows from GFM pipe table separator rows. |
| 4 | HIGH | 22-02, 22-03, 22-05 | `22-02-PLAN.md:96-99`; `22-03-PLAN.md:88-93`; `22-05-PLAN.md:78` | G3 content-preservation audit has no mechanized verification method. |
| 5 | HIGH | 22-01, 22-02, 22-03 | `22-01-PLAN.md:120-121`; `22-RESEARCH.md:417-424` | Sanity gate tests only inline math; block math (primary defect class) is untested. |
| 6 | HIGH | 22-02, 22-03, 22-04, 22-05 | `22-02-PLAN.md:69-72`; `22-03-PLAN.md:66-68`; `22-04-PLAN.md:66-76`; `22-05-PLAN.md:67-78` | SI-PINN-002 meta-doc treated inconsistently: negative control for defects but positive control for census. |
| 7 | HIGH | 22-02, 22-03 | `22-02-PLAN.md:61-84`; `22-03-PLAN.md:59-78` | "Zero overlap" parallel claim is false — shared ledger, branch, detector, fixtures. |
| 8 | MEDIUM | 22-01, 22-02, 22-03 | `22-01-PLAN.md:120-128`; `22-02-PLAN.md:96`; `22-03-PLAN.md:88` | D3 regex `(?<!\\)[_^](?!\\{)[A-Za-z]{2,}` false-positives on `_italic_`, misses `x_i`. |
| 9 | MEDIUM | All five | `22-01-PLAN.md:76-84`; `22-VALIDATION.md:22-25` | Detector CLI modes (`--all`, `--census`, `--regression`, `--selftest`) are plan inventions, not grounded in design doc. |
| 10 | MEDIUM | 22-02, 22-03 | `22-02-PLAN.md:69-72`; `22-03-PLAN.md:66-68` | Pandoc-to-GFM "byte-for-byte" claim is unsatisfiable when rowspan/colspan/multi-line cells exist. |
| 11 | MEDIUM | 22-01 | `22-01-PLAN.md:82`; `22-RESEARCH.md:197-203` | `tools/spec-render-check/` directory path assumes no existing `tools/` conflict; unverified. |
| 12 | LOW | 22-01 | `22-01-PLAN.md:83` | Claim that `node_modules/` is git-ignored by "repo-root .gitignore line 238" is unverified (pattern form unknown). |
| 13 | LOW | 22-02, 22-03, 22-04, 22-05 | `22-02-PLAN.md:139-145`; `22-03-PLAN.md:132-138`; `22-04-PLAN.md:133-138`; `22-05-PLAN.md:144-150` | ROADMAP SC-to-plan mapping is ambiguous; SC 3 appears in multiple plans. |
| 14 | LOW | All five | Across all plans | All plans append to `16-ISSUE-LEDGER.md` but none verify the file exists at the expected path. |

### 5.2 Execution Clarity

| # | Severity | Plans | Location | Ambiguity | Derailment Risk |
|---|----------|-------|----------|-----------|-----------------|
| 1 | CRITICAL | 22-01, 22-02, 22-03 | 22-01 Task 2; 22-02 Task 1; 22-03 Task 1 | D4 survivor scan: does it emit source locations or only rendered-output findings? | Agent cannot perform repairs without source-to-rendered mapping algorithm. |
| 2 | CRITICAL | 22-01 | 22-01 Task 2, D3 | "Bake in exclusions": are listed exclusions examples the regex already excludes, or additional hardcoded rules? | `H_\\epsilon` is already excluded by `[A-Za-z]{2+}` (backslash not a letter); listing it causes confusion. |
| 3 | CRITICAL | 22-02, 22-03 | 22-02 Task 2; 22-03 Task 2 | "convert to `$...$` only when genuinely math" — what are the decision criteria? | AI converts too much (breaking code identifiers) or too little (leaving math unrendered). |
| 4 | HIGH | 22-01 | 22-01 Task 2, D4 | Distinguish `: Table N:` captions from Pandoc definition-list `:   ` bodies — exact algorithm? | Detector may false-positive on `sampling_method.md` negative control. |
| 5 | HIGH | 22-04 | 22-04 Task 1 | Pre-WS-A census: which git ref to use if tag is missing? | Agent blocked trying to find valid pre-WS-A ref; may use already-edited files as "before" state. |
| 6 | HIGH | 22-02, 22-03 | 22-02 Task 2; 22-03 Task 2 | Trailing-`\` hard-breaks: what constitutes "conversion noise"? | AI removes intentional breaks or leaves noise in place. |
| 7 | HIGH | 22-01, 22-02, 22-03, 22-04 | 22-01 Task 2; 22-02/22-03/22-04 Task 1 | "Target by section/anchor, not line number" — does detector emit section names? | Agent may resort to forbidden hardcoded line numbers. |
| 8 | HIGH | 22-01, 22-02, 22-03 | 22-01 Task 2; 22-02 Task 2; 22-03 Task 2 | "Escape literal `$` as `\$`" — which `$` characters are literal? | Naive approach breaks inline math using single-dollar delimiters. |
| 9 | MEDIUM | 22-02 | 22-02 Task 1 | Multi-line Pandoc cell → GFM: concatenate with spaces, `<br>`, or keep first line? | Visual layout may change; "renders identically" is unverified. |
| 10 | MEDIUM | 22-02 | 22-02 Task 1 | `{#tab:...}` cross-reference preservation: what constitutes a "live reference"? | Agent may miss text references or false-positive on unrelated mentions. |
| 11 | MEDIUM | 22-03 | 22-03 Task 1 | Block math inside list items: exact blank-line/indentation requirements? | `markdown-it` may still not recognize block math, or list structure breaks. |
| 12 | MEDIUM | 22-02, 22-03 | 22-02 Task 2; 22-03 Task 2 | "Wrap in `$...$` with correct braces, grounded by author's canonical text forms" — how to find canonical form? | AI may choose form that contradicts existing usage elsewhere in document. |
| 13 | MEDIUM | 22-03 | 22-03 Task 2 | "Redundant fallback removal — PER-INSTANCE ON CONFIRMATION" — what is the duplicate-detection algorithm? | Agent may remove non-redundant content or leave all fallbacks in place. |
| 14 | MEDIUM | 22-01, 22-04 | 22-01 Task 2; 22-04 Task 1 | `**[...]**` bold notes treated as author comments "when they carry/derive-from an author marker" — what is the criterion? | Agent must read external design doc §6.1; criterion is still vague. |
| 15 | MEDIUM | All five | `22-RESEARCH.md` Live Defect Map | "13 author-marker lines (5+8+3)" — 5+8+3=16, not 13. Confusion between lines vs. phrases. | Census target is unclear; agent may over-search or under-count. |
| 16 | MEDIUM | 22-05 | 22-05 Task 1 | G3 audit "differs ONLY in delimiters/structure/whitespace/representation" — what is the audit method? | Subjective judgment may pass changes that alter meaning. |
| 17 | MEDIUM | 22-05 | 22-05 Task 1 | "Re-run on previously-clean specs the batches could have regressed" — which specs, based on what rule? | Agent may under-check (missing regressions) or over-check (wasting time). |
| 18 | LOW | 22-01 | 22-01 Task 3 | Footnote probe requires human to open Cursor — how does observation get back to agent? | Probe may hang indefinitely if human is unavailable. |
| 19 | LOW | 22-01 | 22-01 Task 1 AC | `node -e "require(...)"` acceptance criterion requires package to be installed, but checkpoint says human approves BEFORE install. | Sequencing contradiction; AI following checkpoint literally fails acceptance criterion. |

### 5.3 Operational Resilience

| # | Severity | Plans | Location | Fragile Step | Failure Mode | Downstream Impact |
|---|----------|-------|----------|--------------|--------------|-------------------|
| 1 | CRITICAL | All five | 22-01 Task 2; all verify blocks | Detector CLI output format unspecified; downstream grep for magic strings | Format change breaks all grep-based verify steps silently | All WS-A repair verification, census diffing, closure gating become unreliable |
| 2 | CRITICAL | 22-04 | 22-04 Task 1 | Pre-WS-A census requires discovering Phase-22 start tag/commit; if missing, hard STOP | If 22-02/22-03 agents did not record explicit start tag, 22-04 cannot proceed | Entire WS-B workstream blocked; phase cannot close |
| 3 | CRITICAL | 22-04 | 22-04 Task 1; D-05 in 22-CONTEXT.md | Preservation check uses text-hash compare, but D-05 permits wrapper repairs that change bytes | Permitted D-05 wrapper repair triggers false preservation failure | Any wrapper repair blocks handoff and phase closure |
| 4 | CRITICAL | 22-05 | 22-05 Task 2 | G4 manual Cursor render review is blocking human checkpoint with no timeout/fallback | Human unavailable → phase hangs indefinitely | v1.4 milestone cannot close |
| 5 | CRITICAL | 22-02, 22-03 | 22-02 Task 2; 22-03 (implicit via 22-01 dep) | 22-03 has no footnotes but depends on 22-01 which blocks on footnote probe | ctl_instruction.md repairs delayed on irrelevant dependency | Parallel wave execution serialized unnecessarily |
| 6 | HIGH | 22-02 | 22-02 Task 1 verify | Verification runs once after all 7 constructs; no per-construct checkpoint | Second table conversion introduces new D4 survivor — agent cannot tell which construct caused it | Expensive manual bisection; agent may guess wrong and compound errors |
| 7 | HIGH | 22-02, 22-03 | 22-02 Task 2; 22-03 Task 2 | Math equivalence verification requires `--compare-render` mode, but 22-01 never specifies it | Agent must write ad-hoc KaTeX code or skip equivalence verification | Math conversions proceed without verified equivalence; meaning may change |
| 8 | HIGH | 22-02, 22-03 | 22-02 Task 2; 22-03 Task 2 | No git commit per construct; only ledger status revert mentioned | Bad conversion cannot be rolled back; agent must manually reconstruct original text | Single bad conversion corrupts spec file irreversibly |
| 9 | HIGH | 22-01, 22-02, 22-03, 22-05 | 22-01 Task 2; `22-RESEARCH.md` Pitfall 2 | No false-positive suppression mechanism for detector | New false positive pattern discovered → agent must "fix" valid notation or leave finding unaddressed | Single false positive could block entire phase or corrupt spec |
| 10 | HIGH | 22-01 | `22-RESEARCH.md` Standard Stack; 22-01 Task 1 | Node.js >= 24 assumed but never runtime-checked | Agent/CI on Node 18/20 may produce different rendering output | Detector output diverges from Cursor; CI non-reproducible |
| 11 | HIGH | 22-01, 22-05 | 22-01 Task 3; 22-05 Task 1 | `sampling_method.md` assumed stable 0-findings negative control, but Phase 20.5 may edit it | If 20.5 adds Pandoc constructs, negative control assumption invalid | False regression alarms; agent may fix 20.5 issues under 22 scope |
| 12 | HIGH | 22-04 | 22-04 Task 2 | Handoff count must match PRE/POST/live "exactly" — no rule for which source is authoritative when they disagree | Lost comment could go undetected, or phantom discrepancy blocks handoff indefinitely | FUT-05 handoff based on inconsistent data |
| 13 | MEDIUM | 22-01 | 22-01 Task 3 | Regression fixtures built using census output from Task 2, but census correctness only verified in Task 3 | If Task 2 census has bug (e.g., case sensitivity), fixtures are incomplete; Task 3 --selftest passes against incomplete fixtures | Detector might miss real author comments during WS-A |
| 14 | MEDIUM | 22-03 | 22-03 Task 2 | "Mechanically evidence-bound as presentation-only" is subjective | Two agents may disagree on whether fallback is evidence-bound | Inconsistent execution; content loss or incomplete cleanup |
| 15 | MEDIUM | All five | Across all plans | No single state file tracks wave/task status | Next agent must reconstruct state from 5 plan files + git log | Session handoffs slow and error-prone; work may be repeated or skipped |
| 16 | LOW | 22-01 | 22-01 Task 1, threat model T-22-01 | Supply-chain verification uses `npm view` (metadata only), not tarball integrity | Compromised registry returns correct metadata but malicious tarball | Malicious code in detector dependencies could exfiltrate spec content |
| 17 | LOW | 22-VALIDATION | `22-VALIDATION.md` frontmatter | Placeholder task IDs (`22-00-*`, `22-0?-*`) and `nyquist_compliant: false` | Verification map cannot be used for traceability | Verification steps skipped or misapplied |

---

## 6. Pre-Execution Requirements

The following must be completed before any Phase 22 plan executes:

1. **Create the `v1.4-pre-phase-22` tag** at current HEAD before any WS-A edits begin. Document the commit hash in `22-CONTEXT.md`. Add a fallback heuristic (e.g., `git log --before=<date> -1 -- <files>`) to 22-04 for base-commit discovery.

2. **Re-count all author markers** in the live corpus (`ctl_instruction.md`, `pinn_architecture.md`, `sampling_method.md`) and update ALL artifacts (`22-RESEARCH.md`, `22-CONTEXT.md`, `22-GAPS.md`, all five plans) with the verified count. The detector must derive the count at execution time; no hardcoded figure may be used as a verification target.

3. **Specify the detector output format as a stable contract**: add a `--json` mode to `detect.mjs` with a documented schema (fields: `finding_type`, `severity`, `file`, `section`, `line`, `message`, `snippet`). Downstream plans must verify format stability before relying on grep patterns.

4. **Mechanize the G3 content-preservation audit**: define the algorithm as (a) alphanumeric token-sequence comparison (before/after tokens must match except math delimiter tokens and whitespace), and (b) render equivalence (detector renders both versions; visible text must match except rendering improvements). Document this explicitly in 22-05.

5. **Add required detector features before any repair plan executes**: `--compare-render` mode for snippet equivalence, `--suppress <pattern>` or `exclusions.json` for false-positive suppression, runtime Node version check (>=24), and a D4 survivor scan that distinguishes Pandoc multiline separators from GFM pipe-table separators.

6. **Fix the parallelism model**: either sequence 22-02 before 22-03 (removing the "parallel" claim), or define an explicit coordination protocol (one agent owns ledger appends, commits are batched and merged, detector is read-only during repair). Remove the footnote probe dependency from 22-03; `ctl_instruction.md` has no footnotes.

7. **Mandate git commit after each construct conversion** in 22-02 and 22-03. Add explicit rollback instructions: "If a new finding appears after conversion, run `git checkout -- <file>` to revert, then re-attempt." Record the base commit hash in each plan's SUMMARY for recovery reference.

8. **Refine the D3 regex** to exclude Markdown emphasis contexts (require underscore between word characters, not whitespace-word), and add an `exclusions.json` file for confirmed false positives. Document the single-letter subscript decision explicitly.

9. **Extend the sanity gate** to test BOTH inline math (`$x^2$`) AND block math (`$$\begin{aligned}x\\y\end{aligned}$$`), asserting KaTeX output for both.

10. **For each ambiguous conversion decision, provide a concrete decision tree or STOP-surface rule**: backtick-to-math (use context + D5 signatures + exclusion of paths/file extensions), trailing-backslash removal (define "conversion noise" as appearing in converted math or author-flagged lines), brace style (lookup existing LaTeX form in doc; if multiple conflicting forms, STOP), redundant fallback removal (character-for-character identical within 2 lines, or author-flagged only).

11. **Verify `sampling_method.md` is still a 0-findings negative control** after any Phase 20.5 edits. If it has changed, re-establish the baseline or update the negative control assumption with explicit documentation.

12. **Create a `22-STATE.md` file** to track active wave, completed tasks, blocked items, and last verified checkpoint. Update it atomically with each task completion. Agents must read it before starting work.

---

## 7. Recommendations for Plan Optimization

### Immediate (Block Execution)

1. **Restructure 22-01 into three sub-tasks**: (a) detector scaffold + install, (b) D1-D6 implementation, (c) regression + census fixtures. Sub-task (c) must verify census count against live corpus before building fixtures.

2. **Make the detector a first-class artifact** with its own `README.md` specifying: CLI modes, output formats (human and `--json`), version requirements, false-positive suppression mechanism, and regression fixture maintenance protocol.

3. **Replace all semantic verification gates with mechanical ones**: "Differs only in delimiters" becomes "alphanumeric token sequence identical except delimiter tokens." "Genuinely math" becomes a decision tree with STOP-surface rules, not open-ended judgment.

4. **Add a pre-flight checklist** to 22-01 (or a new `22-00-PREFLIGHT.md`) that verifies: tag exists, ledger file exists, `tools/` directory is clear, Node >= 24, sampling_method.md is still 0-findings.

### Near-Term (Before First Repair Wave)

5. **Convert 22-02 and 22-03 from "parallel" to "staged"**: run 22-02 first (pinn_architecture.md), then 22-03 (ctl_instruction.md). This eliminates shared-state races without requiring a complex coordination protocol. If parallelism is truly required, implement file-based locking on the ledger.

6. **Add per-construct git commits and verify steps** to 22-02 and 22-03. After each table/div/caption conversion: commit, run detector, assert specific construct class is gone. This makes bisection trivial.

7. **Define the G3 audit as a script**, not a manual diff inspection. The script should: extract before/after token sequences, compare (excluding `$`/`$$`/whitespace), render both versions, compare visible text. If the script cannot be written in time, G3 must be a human checkpoint, not an autonomous gate.

### Process Improvements

8. **Require that every plan with `autonomous: true` have only mechanical acceptance criteria**. Any criterion requiring domain judgment ("genuinely math", "evidence-bound", "conversion noise") must be either mechanized or moved to a `checkpoint:human` task.

9. **Maintain a live gap register** (`22-GAPS.md`) with the required fields from the STOP protocol: decision point, artifact location, classification, source silence, mathematical grounding, agent temptation, concrete options, impact confidence, status. Update it atomically with each gap discovery and resolution.

10. **After fixing all critical findings, re-run this audit** before execution begins. The re-audit should focus on whether the pre-execution requirements were satisfied correctly, not just that they were attempted.

---

## 8. Auditor Notes & Limitations

**What was verified live:**
- Git tag existence: `v1.4-pre-phase-22` does not exist (confirmed via `git tag -l 'v1.4*'`).
- Author marker counts: `ctl_instruction.md` = 13, `pinn_architecture.md` = 9, `sampling_method.md` = 0 (confirmed via grep).
- `ctl_instruction.md` footnote presence: zero footnotes (confirmed via grep for `[^` pattern).
- Git branch: `milestone/v1.4` (not master).

**What was not verified:**
- The actual content of `pinn_architecture.md` tables (rowspan/colspan/multi-line cells were not individually inspected; the finding is based on the general unsatisfiability of the "byte-for-byte" claim given GFM's limitations).
- The exact `.gitignore` pattern form for `node_modules/` (line number claim was not verified).
- Whether Phase 20.5 edited `sampling_method.md` (this requires cross-referencing commit history outside the provided context).
- Whether `tools/` directory already exists at repo root.

**Assumptions made during audit:**
- The synthesized findings accurately represent the raw data.
- The "live corpus" refers to the current working-tree versions of the three framework spec files.
- Phase 22 has not yet begun execution (no WS-A edits have been made).

**Confidence in audit:** HIGH. The critical findings (missing tag, wrong census count, unspecified detector contract, false parallelism, unmechanized G3) are all independently verifiable from the provided artifacts and live corpus. The execution risk score of 8 reflects that the plans are well-structured in intent but contain material gaps in contract specification, verification mechanics, and operational resilience that make autonomous execution unsafe.