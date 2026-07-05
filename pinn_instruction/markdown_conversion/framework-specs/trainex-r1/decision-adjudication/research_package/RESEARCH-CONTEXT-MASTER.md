---
title: "Trainex r1a — Decision-Adjudication Research Brief (Context Master)"
created: 2026-07-04
source_baseline: 4bbd5443 (master; v1.6 merged, tag v1.6)
channel: build-design (recommendation only; the project owner ratifies)
---

# Trainex r1a — Decision-Adjudication Research Brief

## 0. What you are doing (read this first)

You are an external research agent producing a **decisive engineering-decision
resolution** for the *training-execution build* of a curriculum-trained, physics-informed
neural network (a "CTL-PINN") that predicts three-body gravitational trajectories. The
system will be built and operated by a **non-expert on a single Apple-Silicon laptop**
(M-series, ~24 GB unified memory, **no cloud, no distributed training**).

A prior research round already enumerated the decisions, laid out the options, and marked
a *suggested default* for each. **Your job is not to re-invent the option space. Your job
is to adjudicate it:** for each in-scope decision, recommend the choice — endorsing or
overriding the prior suggested default — with clear reasoning, so the owner can adopt your
resolution as the default and ratify it.

Be **decisive** (recommend one option per decision) but **honest** (state your confidence
and the biggest uncertainty). You are a recommender; the owner makes the final call. Where
the attached materials are silent or ambiguous, **record the gap — never invent** a fact,
number, or capability.

You work **only from the attached files.** If something references a file that is not
attached, treat it as unavailable and note it if it matters.

## 1. The attached files (your only sources)

| Filename | What it is | How to treat it |
|---|---|---|
| `trainex-r1a-options-and-decisions.md` | **The decision sheet you are adjudicating** — the 7 core decisions (D1–D7) and baseline-review items (B-1..B-12), each with option menus, a *suggested default*, and a one-way/two-way "door" label | Prior round's recommendation, to **endorse or override** — not settled |
| `chatgpt-pro-resolution.md` | The **full-depth source report** behind that sheet (deeper per-option rationale) | Same standing; use for depth |
| `ctl_instruction.md` | Authoritative **science spec** — curriculum staging + training-loop contracts | **Hard constraint.** Current; may postdate the decision sheet — flag conflicts |
| `pinn_architecture.md` | Authoritative **science spec** — network, autodiff contract, output head, and the §10 numerical acceptance probes | **Hard constraint** |
| `2026-06-10-training-execution-design.md` | The **pipeline baseline** the sheet critiques (subsystem decomposition; "PH-1..PH-10" placeholders) | **Baseline design intent** — challengeable starting point, not authority (it says so itself) |
| `postspec-r1-direction-assessment.md` | **Strategy context** — recommends the first build be a thin *"Stage-0 viability slice"*, not the full platform | Use to tag decisions needed-now vs deferrable (§4). *Note:* it was written against a prior round's bundle that also included `sampling_method.md` and a `FRAMEWORK-SPECS-BUNDLE.md` (neither attached — `sampling_method.md` is the frozen data-generation spec, out of scope for build decisions); treat any references to those as background only. |
| `trainex-r1b-findings.md`, `trainex-r1b-findings-2.md` | **Operations knowledge** — training-feasibility envelope, a trainer-correctness verification ladder, a PINN health watchlist, unattended-run practice | Background for the rows whose thresholds are marked "⚖" in the sheet. Those ⚖ values are **filled at Stage 2 (consolidation)**, not Stage 1: in Stage 1 leave them as placeholders and record in your claims register any ⚖ threshold these files do not actually give a number for. |

## 2. Standing and authority (do not overstep)

- This is a **build-design** round — engineering choices about how to build and run the
  trainer. It is **NOT** a science/spec adjudication and does **NOT** edit or ground the
  science specs.
- Your resolution is a **recommendation the owner ratifies.** Recommend decisively; do not
  claim final authority.
- **Suggest a default; never assert final authority.** You suggest a decisive default for the
  owner to ratify — you do not decide with final authority. On rows that are really an **owner
  preference** (e.g., risk tolerance) or an **empirical** matter (needs a probe/measurement),
  flag the row for the owner rather than deciding it.
- **Do not re-adjudicate the science.** The attached specs are locked; treat them as fixed
  constraints, not open questions.

## 3. Scope — what to decide, what to leave alone

**Decide (recommend one option each):** D1, D2, D3, D4-a/b/c/d, D5-a/b/c, D6,
D7-a/b/c/d, and baseline items B-1, B-2, B-3, B-4, B-5, B-6, B-9, B-10, B-11. The attached
decision sheet defines each and gives you the full menus.

**Do NOT decide — context only:**

- **D1-p (numerical precision, fp32 vs fp64).** A separate science/precision question in
  another channel. Do not pick it. Instead ensure your recommendations **hold under both
  branches** (fp32-on-GPU and fp64-on-CPU); where a decision's shape depends on the branch,
  give the recommendation for each.
- **B-8 (the ε_H acceptance-gate direction).** Settled by the spec — `ctl_instruction.md`
  (lines 550–555) defines it unambiguously: REJECT if `eps_H > 1e-5` (smaller passes),
  `eps_H = 0 → Excellent`. The baseline design doc's §6.3 renders an inverted-looking gate
  example (r1b flags it as C-12); that is a display typo in a non-authoritative doc, not a
  contradiction in the locked metric. Treat the gate as a fixed constraint (do not
  re-adjudicate its direction); if a recommendation depends on it, note the dependency.

**Not adjudicated here (handled elsewhere — transparency note):** the decision sheet's §8 also
lists **B-7** (cosmetic: its error-table "CUDA out of memory" row should read MPS wording — a
doc edit, no adjudication needed) and **B-12** (a split-policy tension routed to v1.5/PH-5;
register U-4). Neither is in your Decide list; both are intentionally out of scope for this
round. Your Decide set therefore covers B-1..B-6 and B-9..B-11.

## 4. The lens: recommend for a thin first step, not the whole platform

Per the attached strategy assessment, the intended first build is a **minimal Stage-0
viability slice** — the thinnest end-to-end path that can train the first curriculum stage
and reveal whether the model does anything physically sensible on the available data. So
for **every** decision, tag your recommendation:

- **Needed now** — required to stand up the Stage-0 slice, or a one-way (expensive-to-
  reverse) choice that must be right from the start; **or**
- **Deferrable** — safely postponed until the slice proves the approach (a two-way choice
  addable later).

Prefer the simplest recommendation that lets the thin slice run, while protecting the
one-way doors.

## 5. Output contract (what to return)

One polished, human-readable Markdown report. For **each in-scope decision**:

1. **Recommendation** — the single option you recommend.
2. **Endorse or override** — whether you agree with the prior suggested default, and *why*.
3. **Confidence** — High / Medium / Low, plus the single biggest uncertainty behind it.
4. **Consistency** — how this pick fits the others (e.g., the framework choice constrains
   the tracking, data-loading, and loop options). The full set must be coherent.
5. **Timing** — Needed-now or Deferrable (§4).
6. **Nature** — flag if the choice is really an **owner preference** (e.g., risk tolerance)
   or an **empirical** matter (needs a measurement/probe) rather than research-settled.

Then, once for the report:

- **Composed first-run recipe** — a short end-to-end description of the resulting first
  run, as a coherence check that your picks work together.
- **What the runbook inherits** — the subset of your recommended picks that lands in the
  non-expert operator's first runbook (the needed-now set, stated as concrete
  defaults/instructions), kept distinct from the deferrable set.
- **Claims-and-uncertainty register** — every place the attached materials were
  silent/ambiguous, every project-side number you needed but did not have (do **not**
  invent them), and every assumption you made.
- **Standing restatement** — one line confirming this is a recommendation for the owner to
  ratify, not a science-spec verdict, and that D1-p and B-8 were left to the owner.

## 6. Hard constraints (never recommend against these)

- **Single machine:** one Apple-Silicon laptop (M-series, ~24 GB unified memory). **No
  cloud, no distributed training.**
- **Non-expert operator:** comfortable with a terminal and a runbook; not a Python
  developer. Favor simplicity, well-typed failures, and searchable/well-supported tools.
- **Science specs are authoritative:** `ctl_instruction.md` and `pinn_architecture.md` fix
  the network, losses, curriculum, optimizer regime, and acceptance probes. Build decisions
  serve them; they do not change them.
- **Current specs may postdate the decision sheet:** if the attached specs contradict any
  option in the sheet, flag it as a spec-drift finding rather than silently following the
  older text.

## 7. Source discipline

Work only from attached files. Do not import outside numbers for this project's data
sizes, run durations, or hardware behavior — where you need such a number, name it in the
claims register as a project-side unknown. Cite the attached filename when a recommendation
leans on it. If the decision sheet references something not attached, treat it as
unavailable and note it.
