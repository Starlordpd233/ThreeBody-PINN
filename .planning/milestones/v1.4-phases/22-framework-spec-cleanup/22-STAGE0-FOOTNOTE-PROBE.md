---
phase: 22
slug: framework-spec-cleanup
artifact: stage-0-footnote-probe
status: CONFIRMED
created: 2026-06-09
confirmed: 2026-06-09
confirmer: user (Cursor Markdown Preview observation)
decides: detector D4 footnote policy + 22-02 footnote-repair scope (37 refs / 17 defs in pinn_architecture.md)
---

# Stage-0 footnote probe — does the Cursor target render `[^n]`?

This is the blocking Wave-0 probe for Assumption **A2** (22-RESEARCH.md): whether the Cursor /
VS Code Markdown Preview renders Pandoc-style footnotes `[^n]`. The answer decides whether the
**37 footnote references / 17 definitions** in `pinn_architecture.md` are survivor **defects**
(repair in 22-02) or correctly-rendered content (leave as-is), and it sets the detector's runtime
**D4 footnote policy**.

> Governance: per the v1.4 STOP protocol, the deciding value below is **not invented**. The
> detector records only what its own engine does; the real Cursor/VS Code render is filled in by
> the human at the Task-3 checkpoint.

## Machine-readable policy (read by `detect.mjs --footnote-policy auto`)

```
FOOTNOTE_POLICY: unsupported
```

While this value is `UNCONFIRMED`, `detect.mjs --footnote-policy auto` exits **3** ("Stage-0
footnote probe required") for any target containing `[^n]`. The human replaces it with exactly
`supported` or `unsupported` after the Cursor render is observed.

## Detector-engine result (derived, factual)

Rendered with the detector's exact engine — `markdown-it@14.2.0` + `@vscode/markdown-it-katex@1.1.2`
+ `katex@0.16.47`, the same packages the detector uses — the minimal sample below produces:

```html
<p>A claim needing a source.[^1]</p>
<p>[^1]: The cited reference.</p>
```

i.e. the literal token `[^1]` **survives in the visible text** for both the reference and the
definition. The detector engine does **not** load a footnote plugin, so on the detector engine
alone, footnotes are **unsupported** (they would be D4 survivors).

**Why this is not the final answer:** Cursor / VS Code's Markdown Preview may enable a footnote
plugin (e.g. `markdown-it-footnote`) that the bare detector stack does not. The deciding target is
the human's actual Cursor preview, recorded below. If Cursor renders `[^n]` as real footnotes, the
detector's `unsupported` engine result is a known, accepted divergence and the policy is
`supported`; if Cursor also leaves `[^n]` literal, the policy is `unsupported` and the 37 refs are
repair targets.

## Minimal `[^n]` probe sample (open THIS file in the Cursor / VS Code Markdown Preview)

A claim that needs a citation.[^probe1] And a second claim.[^probe2]

[^probe1]: First probe footnote definition.
[^probe2]: Second probe footnote definition.

When previewed in Cursor / VS Code, observe whether:
- the references render as small superscript links (e.g. ¹ ²) that jump to a footnotes section, **and**
- the definitions render as a footnotes list (not literal `[^probe1]: …` text).

If both render as footnotes → **supported**. If either survives as literal `[^...]` markup →
**unsupported**.

## Human confirmation (fill at the Task-3 checkpoint — leave blank until observed)

- **Observed in Cursor/VS Code preview:** unsupported
- **Observed behavior (one line):** `[^probe1]` and `[^probe2]` render as literal text in prose; definitions render as inline text, not as a footnotes list
- **Editor + version:** Cursor (version unspecified by user)
- **Date / confirmer:** 2026-06-09 / user screenshot

## Decision this controls

- **supported** → detector D4 suppresses the `[^n]` class (`--footnote-policy supported`); the 37
  refs / 17 defs are **not** defects; `--all` can reach zero with footnotes intact; 22-02 does no
  footnote repair.
- **unsupported** → detector D4 flags `[^n]` refs/defs as DEFINITE survivors; 22-02 converts them to
  a render-safe form preserving every citation, byte-for-byte where possible.
- **UNCONFIRMED (current)** → footnote classification is blocked; `auto` exits 3; non-footnote WS-A
  work may proceed, but no final `--all` closure that depends on footnote policy.
