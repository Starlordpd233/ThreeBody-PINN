#!/usr/bin/env node
// Phase 22 framework-spec render detector.
//
// Mirrors the Cursor / VS Code Markdown Preview math engine
// (markdown-it + @vscode/markdown-it-katex + katex) and reports rendering defects.
//
// Layers (design §5.1):
//   D1 KaTeX throwOnError ........ DEFINITE  (hard math parse errors)         [global]
//   D2 KaTeX strict .............. REVIEW    (suspicious math)                [global, math]
//   D3 LaTeX lint ................ REVIEW    (bare multi-char sub/sup)        [global, code/fence excluded]
//   D4 render survivor scan ...... DEFINITE  (control markup in visible text) [global, code/math excluded]
//   D5 backtick-math scan ........ REVIEW    (ASCII math in code spans)       [oracle-guided]
//   D6 prose-math scan ........... REVIEW    (ASCII math in prose)            [oracle-guided]
// plus a plugin double-wrap SANITY GATE (inline + block) and an author-comment CENSUS pass.
//
// Recall = detector (survivor/structural/lint) ∪ author comments as oracle (prose/backtick math)
//          ∪ human render review (design §5.2). D5/D6 are oracle-guided: they only emit inside
//          author-flagged regions, which keeps the clean negative control (sampling_method.md,
//          0 author markers) at zero findings despite its many `snake_case = value` code spans.
//
// Reporting is by section/anchor + matched snippet (Pattern 3 — no hardcoded line numbers; the
// line number shown is derived from live bytes at run time). Exit codes:
//   0 clean (or selftest/regression pass) · 1 findings (DEFINITE or REVIEW) ·
//   2 sanity-gate failure · 3 missing prerequisite (Stage-0 footnote probe) · other = tool failure.

import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
import MarkdownIt from 'markdown-it';
import katex from 'katex';
import * as katexPluginNS from '@vscode/markdown-it-katex';

const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(SCRIPT_DIR, '..', '..');
const SPEC_DIR = path.join(REPO_ROOT, 'pinn_instruction', 'markdown_conversion', 'framework-specs');
const SPECS = ['ctl_instruction.md', 'pinn_architecture.md', 'sampling_method.md']
  .map((f) => path.join(SPEC_DIR, f));
const SAMPLING_SPEC = path.join(SPEC_DIR, 'sampling_method.md');
const FIXTURES = path.join(SCRIPT_DIR, 'fixtures', 'regression.md');
const PROBE_FILE = path.join(
  REPO_ROOT, '.planning', 'phases', '22-framework-spec-cleanup', '22-STAGE0-FOOTNOTE-PROBE.md',
);

const ORACLE_WINDOW = 20; // lines around an author marker that D5/D6 may scan

// ---------------------------------------------------------------------------
// Plugin resolution + engine (Pitfall 1: @vscode/markdown-it-katex double-wrap)
// ---------------------------------------------------------------------------
function resolvePlugin(ns) {
  for (const c of [ns, ns && ns.default, ns && ns.default && ns.default.default]) {
    if (typeof c === 'function') return c;
  }
  return null;
}

function buildMd(plugin = resolvePlugin(katexPluginNS)) {
  if (typeof plugin !== 'function') throw new Error('katex plugin export is not callable');
  const md = new MarkdownIt({ html: true, linkify: false, typographer: false });
  md.use(plugin, { throwOnError: false, strict: false });
  return md;
}

function looksRendered(html) {
  return /class="katex/i.test(html) || /<annotation/i.test(html) || /<math/i.test(html);
}

// Sanity gate: assert the loaded plugin actually consumes inline AND block math.
// Validates plugin BEHAVIOR (renders real math), not literal source text — so a fixture that
// merely *mentions* `.default.default` wrapper forms does not trip the gate. A pluginOverride is
// accepted only to prove Pitfall-1 protection (forcing a non-callable/absent plugin => exit 2).
function sanityGate(pluginOverride) {
  let md;
  try {
    md = pluginOverride !== undefined ? buildMd(pluginOverride) : buildMd();
  } catch (e) {
    abort(2, `sanity gate: plugin failed to load (${e.message})`);
  }
  const inline = md.render('$x^2$');
  const block = md.render('$$\\int_0^1 x\\,dx$$');
  if (!looksRendered(inline)) abort(2, 'sanity gate: inline math $x^2$ was not rendered by KaTeX');
  if (!looksRendered(block)) abort(2, 'sanity gate: block math $$...$$ was not rendered by KaTeX');
  return md;
}

function abort(code, msg) {
  process.stderr.write(`detect.mjs ABORT (exit ${code}): ${msg}\n`);
  process.exit(code);
}

// ---------------------------------------------------------------------------
// Source model: fence mask, block-math regions, headings, inline segmentation
// ---------------------------------------------------------------------------
function slug(s) {
  return s.toLowerCase().replace(/[`*_$\\{}]/g, '').replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '') || '(section)';
}

// Returns { lines, kind[], headings:[{line,slug,text}] }
// kind[i] ∈ 'fence' | 'mathblock' | 'normal'
function modelOf(src) {
  const lines = src.split('\n');
  const kind = new Array(lines.length).fill('normal');
  const headings = [];
  let fence = null; // {char,len}
  let i = 0;
  while (i < lines.length) {
    const line = lines[i];
    const fenceOpen = line.match(/^\s*(`{3,}|~{3,})/);
    if (fence) {
      kind[i] = 'fence';
      if (fenceOpen && fenceOpen[1][0] === fence.char && fenceOpen[1].length >= fence.len
          && /^\s*(`{3,}|~{3,})\s*$/.test(line)) {
        fence = null;
      }
      i += 1;
      continue;
    }
    if (fenceOpen) {
      fence = { char: fenceOpen[1][0], len: fenceOpen[1].length };
      kind[i] = 'fence';
      i += 1;
      continue;
    }
    // Block math: a line whose first non-space content starts with `$$` (own-line opener).
    const trimmed = line.replace(/^\s+/, '');
    if (trimmed.startsWith('$$')) {
      const dollarPairs = (line.match(/\$\$/g) || []).length;
      kind[i] = 'mathblock';
      if (dollarPairs >= 2) { i += 1; continue; } // single-line $$ ... $$
      // multi-line: consume until a line containing a closing $$
      i += 1;
      while (i < lines.length) {
        kind[i] = 'mathblock';
        if (lines[i].includes('$$')) { i += 1; break; }
        i += 1;
      }
      continue;
    }
    const h = line.match(/^(#{1,6})\s+(.*\S)\s*$/);
    if (h) headings.push({ line: i, slug: slug(h[2]), text: h[2].trim() });
    i += 1;
  }
  return { lines, kind, headings };
}

function anchorOf(model, lineIdx) {
  let best = null;
  for (const h of model.headings) {
    if (h.line <= lineIdx) best = h;
    else break;
  }
  return best ? best.slug : '(preamble)';
}

// Segment a single 'normal' line into code / math / prose runs.
// Returns [{kind:'code'|'math'|'prose', text, col}]
function segmentLine(line) {
  const segs = [];
  let i = 0;
  const n = line.length;
  let prose = '';
  let proseCol = 0;
  const flushProse = () => {
    if (prose) segs.push({ kind: 'prose', text: prose, col: proseCol });
    prose = '';
  };
  while (i < n) {
    const ch = line[i];
    if (ch === '\\') { // escaped char — keep both in prose, skip next
      if (!prose) proseCol = i;
      prose += line.slice(i, i + 2);
      i += 2;
      continue;
    }
    if (ch === '`') {
      let run = 1;
      while (line[i + run] === '`') run += 1;
      const close = line.indexOf('`'.repeat(run), i + run);
      if (close !== -1
          && line[close + run] !== '`') {
        flushProse();
        segs.push({ kind: 'code', text: line.slice(i + run, close), col: i });
        i = close + run;
        continue;
      }
      if (!prose) proseCol = i;
      prose += ch; i += 1; continue;
    }
    if (ch === '$') {
      if (line[i + 1] === '$') { // `$$` — never valid inline math; leave in prose (D4 survivor)
        if (!prose) proseCol = i;
        prose += '$$'; i += 2; continue;
      }
      // inline math $...$ : find next unescaped single $
      let j = i + 1;
      let found = -1;
      while (j < n) {
        if (line[j] === '\\') { j += 2; continue; }
        if (line[j] === '$') { found = j; break; }
        j += 1;
      }
      if (found !== -1 && found > i + 1) {
        flushProse();
        segs.push({ kind: 'math', text: line.slice(i + 1, found), col: i });
        i = found + 1;
        continue;
      }
      if (!prose) proseCol = i;
      prose += ch; i += 1; continue;
    }
    if (!prose) proseCol = i;
    prose += ch; i += 1;
  }
  flushProse();
  return segs;
}

// ---------------------------------------------------------------------------
// Author markers (census basis + oracle seeds), all forms, fence-excluded for prose
// ---------------------------------------------------------------------------
const PROSE_MARKERS = [
  { form: 'Author Comment', re: /Author Comment/i },
  { form: 'Author note', re: /Author note/i },
  { form: 'Historical author note', re: /Historical author note/i },
];
const AUTHCOMMENT_RE = /\\authcomment/;

// Detect whether a line is inside the SI-PINN-002-style meta-doc (documents preserved comments,
// not an author flagging broken render). Census enumerates it; oracle (D5/D6) does NOT seed there.
function metaDocLineSet(model) {
  const set = new Set();
  const { lines, headings } = model;
  for (let i = 0; i < lines.length; i += 1) {
    if (/SI-PINN-00\d/i.test(lines[i])
        || /preserved in the converted body/i.test(lines[i])
        || /These notes are metadata/i.test(lines[i])) {
      // mark the whole heading-section containing this line
      let start = 0; let end = lines.length;
      for (const h of headings) {
        if (h.line <= i) start = h.line;
        if (h.line > i) { end = h.line; break; }
      }
      for (let k = start; k < end; k += 1) set.add(k);
    }
  }
  return set;
}

function findMarkers(model) {
  const { lines, kind } = model;
  const markers = [];
  for (let i = 0; i < lines.length; i += 1) {
    const line = lines[i];
    if (kind[i] === 'fence') {
      // \authcomment literal still matters inside fenced code? meta-doc uses inline code, not fence.
      continue;
    }
    // prose markers: must be outside inline code too
    const segs = kind[i] === 'normal' ? segmentLine(line) : [{ kind: 'prose', text: line, col: 0 }];
    const proseText = segs.filter((s) => s.kind !== 'code').map((s) => s.text).join('');
    // One marker per line (GAP-22-02: census basis is author-marker LINES, ~26 union). A line
    // carrying several forms (e.g. the meta-doc's descriptive "author comments" + `\authcomment`)
    // is a single marker line; record all matched forms but count the line once.
    const forms = [];
    for (const m of PROSE_MARKERS) if (m.re.test(proseText)) forms.push(m.form);
    if (AUTHCOMMENT_RE.test(line)) forms.push('\\authcomment');
    if (forms.length) markers.push({ line: i, form: forms.join(' + '), forms });
  }
  return markers;
}

// union of [marker±window] line indices, excluding meta-doc sections, for D5/D6 oracle scope
function oracleLineSet(model, markers, metaSet) {
  const set = new Set();
  for (const mk of markers) {
    if (metaSet.has(mk.line)) continue;
    const lo = Math.max(0, mk.line - ORACLE_WINDOW);
    const hi = Math.min(model.lines.length - 1, mk.line + ORACLE_WINDOW);
    for (let k = lo; k <= hi; k += 1) if (model.kind[k] === 'normal') set.add(k);
  }
  return set;
}

// ---------------------------------------------------------------------------
// Math extraction for D1 / D2
// ---------------------------------------------------------------------------
function extractMath(model) {
  const { lines, kind } = model;
  const exprs = []; // {content, line, display}
  let i = 0;
  while (i < lines.length) {
    if (kind[i] === 'mathblock') {
      const start = i;
      const buf = [];
      while (i < lines.length && kind[i] === 'mathblock') { buf.push(lines[i]); i += 1; }
      const content = buf.join('\n').replace(/\$\$/g, '');
      if (content.trim()) exprs.push({ content, line: start, display: true });
      continue;
    }
    if (kind[i] === 'normal') {
      for (const s of segmentLine(lines[i])) {
        if (s.kind === 'math' && s.text.trim()) {
          exprs.push({ content: s.text, line: i, display: false });
        }
      }
    }
    i += 1;
  }
  return exprs;
}

// ---------------------------------------------------------------------------
// Layers
// ---------------------------------------------------------------------------
function snippetAt(model, line, col = 0, len = 90) {
  const raw = (model.lines[line] || '').trim();
  return raw.length > len ? `${raw.slice(0, len)}…` : raw;
}

function mkFinding(layer, tier, model, file, line, message, col = 0) {
  return {
    layer, tier, file: path.basename(file), anchor: anchorOf(model, line),
    line: line + 1, snippet: snippetAt(model, line, col), message,
  };
}

// D1 / D2 — KaTeX throwOnError (DEFINITE) and strict warnings (REVIEW)
function layerKatex(model, file, findings) {
  for (const e of extractMath(model)) {
    try {
      katex.renderToString(e.content, { throwOnError: true, displayMode: e.display });
    } catch (err) {
      findings.push(mkFinding('D1', 'DEFINITE', model, file, e.line,
        `KaTeX parse error: ${String(err.message).split('\n')[0]}`));
      continue; // a hard error already reported; strict pass would be redundant
    }
    const warns = [];
    try {
      katex.renderToString(e.content, {
        throwOnError: false,
        displayMode: e.display,
        strict: (code, msg) => { warns.push(`${code}: ${msg}`); return 'ignore'; },
      });
    } catch { /* non-strict render shouldn't throw */ }
    if (warns.length) {
      findings.push(mkFinding('D2', 'REVIEW', model, file, e.line,
        `KaTeX strict warning: ${warns[0]}`));
    }
  }
}

// D3 — LaTeX lint: bare multi-char sub/sup outside code/fence.
// Baked-in exclusions: escaped \_ \^ , braced t_{max}, digit-led m_1, H_\epsilon.
// Identifier-shape tokens (snake_case, base length>2) are SUPPRESSED (surfaced, not findings)
// per the plan's no-silent-drop rule. Math-symbol shape (base length<=2, e.g. L_total) = REVIEW.
const D3_RE = /(?<![\\A-Za-z0-9])([A-Za-z][A-Za-z0-9]*)((?:[_^][A-Za-z0-9]+)+)/g;
function layerLint(model, file, findings, suppressed) {
  for (let i = 0; i < model.lines.length; i += 1) {
    if (model.kind[i] === 'fence') continue;
    const segs = model.kind[i] === 'mathblock'
      ? [{ kind: 'math', text: model.lines[i], col: 0 }]
      : segmentLine(model.lines[i]);
    for (const s of segs) {
      if (s.kind === 'code') continue; // code spans excluded (Pitfall 2)
      let m;
      D3_RE.lastIndex = 0;
      while ((m = D3_RE.exec(s.text)) !== null) {
        const base = m[1];
        const chain = m[2];
        // require at least one multi-letter sub/sup component (letters-only, no brace/digit-lead)
        if (!/[_^][A-Za-z]{2,}/.test(chain)) continue;
        // braced label exclusion: text immediately after match is '{' handled by regex class;
        // digit-led component like _1 won't match [A-Za-z]{2,}; H_\epsilon: '\' breaks the token.
        const token = base + chain;
        if (base.length <= 2) {
          findings.push(mkFinding('D3', 'REVIEW', model, file, i,
            `bare multi-char sub/superscript outside math: ${token}`));
        } else {
          suppressed.push(mkFinding('D3', 'SUPPRESSED', model, file, i,
            `identifier-shape sub/sup excluded (surfaced for review): ${token}`));
        }
      }
    }
  }
}

// D4 — render survivor scan: control markup that must never appear in visible text.
// Implemented as a code/math/block-math-excluded prose scan (complete-by-construction:
// enumerates "markup that must never appear literally", not a fixed defect list).
function layerSurvivor(model, file, findings, footnotePolicy) {
  for (let i = 0; i < model.lines.length; i += 1) {
    const line = model.lines[i];
    if (model.kind[i] === 'fence' || model.kind[i] === 'mathblock') continue;
    // structural Pandoc constructs (markdown-it passes them through as literal text)
    if (/^:::/.test(line.trimStart())) {
      findings.push(mkFinding('D4', 'DEFINITE', model, file, i, 'Pandoc fenced div `:::` survives'));
    }
    if (/^\s*:\s*Table\b/i.test(line)) {
      findings.push(mkFinding('D4', 'DEFINITE', model, file, i, 'Pandoc caption `: Table …` survives'));
    }
    if (/^\s*-{3,}\s+-{3,}/.test(line)) {
      findings.push(mkFinding('D4', 'DEFINITE', model, file, i, 'Pandoc multiline-table separator row survives'));
    }
    // prose-segment control markup
    for (const s of segmentLine(line)) {
      if (s.kind !== 'prose') continue;
      if (s.text.includes('$$')) {
        findings.push(mkFinding('D4', 'DEFINITE', model, file, i, 'literal `$$` survives in text (block math not on its own line)'));
      }
      const cmd = s.text.match(/\\[a-zA-Z]{2,}/);
      if (cmd) {
        findings.push(mkFinding('D4', 'DEFINITE', model, file, i, `surviving LaTeX command \`${cmd[0]}\` outside math`));
      }
      const attr = s.text.match(/\{[.#][A-Za-z][\w:-]*\}/);
      if (attr) {
        findings.push(mkFinding('D4', 'DEFINITE', model, file, i, `Pandoc attribute \`${attr[0]}\` survives`));
      }
      const fn = s.text.match(/\[\^\d+\]/);
      if (fn || /^\s*\[\^\d+\]:/.test(line)) {
        const tok = fn ? fn[0] : line.trim().split(':')[0];
        if (footnotePolicy === 'unsupported') {
          findings.push(mkFinding('D4', 'DEFINITE', model, file, i, `footnote token \`${tok}\` survives (policy: unsupported)`));
        }
        // 'supported' → suppress (Cursor renders footnotes); 'auto' resolved before scan
      }
    }
  }
}

const ASCII_MATH = /[A-Za-z0-9]_[A-Za-z0-9]|[A-Za-z0-9]\^|=|\\[a-zA-Z]+|\b(?:sqrt|sum|RMS|frac)\b|\|\||[0-9](?:\.[0-9]+)?e[-+]?[0-9]/;

// D5 — backtick-math (oracle-guided): code spans inside author-flagged regions only.
function layerBacktick(model, file, findings, oracleSet) {
  for (let i = 0; i < model.lines.length; i += 1) {
    if (!oracleSet.has(i) || model.kind[i] !== 'normal') continue;
    for (const s of segmentLine(model.lines[i])) {
      if (s.kind === 'code' && ASCII_MATH.test(s.text)) {
        findings.push(mkFinding('D5', 'REVIEW', model, file, i,
          `backtick-wrapped ASCII math near author flag: \`${s.text}\``));
      }
    }
  }
}

// D6 — prose-math (oracle-guided): prose inside author-flagged regions only.
function layerProse(model, file, findings, oracleSet) {
  for (let i = 0; i < model.lines.length; i += 1) {
    if (!oracleSet.has(i) || model.kind[i] !== 'normal') continue;
    for (const s of segmentLine(model.lines[i])) {
      if (s.kind !== 'prose') continue;
      const m = s.text.match(/[A-Za-z]_[A-Za-z0-9]|[A-Za-z]\^[A-Za-z0-9]|=\s*[A-Za-z\\]|\bRMS\b|\\[a-zA-Z]+/);
      if (m && ASCII_MATH.test(s.text)) {
        findings.push(mkFinding('D6', 'REVIEW', model, file, i,
          `prose ASCII math near author flag: …${s.text.trim().slice(0, 70)}…`));
      }
    }
  }
}

// ---------------------------------------------------------------------------
// Footnote policy resolution
// ---------------------------------------------------------------------------
function readProbePolicy() {
  if (!fs.existsSync(PROBE_FILE)) return 'UNCONFIRMED';
  const txt = fs.readFileSync(PROBE_FILE, 'utf8');
  const m = txt.match(/FOOTNOTE_POLICY:\s*(supported|unsupported|UNCONFIRMED)/i);
  return m ? m[1].toLowerCase() : 'UNCONFIRMED';
}

function resolveFootnotePolicy(requested, modelsWithFootnotes) {
  if (requested === 'supported' || requested === 'unsupported') return requested;
  // auto
  const policy = readProbePolicy();
  if (policy === 'supported' || policy === 'unsupported') return policy;
  if (modelsWithFootnotes) {
    abort(3, 'Stage-0 footnote probe required: 22-STAGE0-FOOTNOTE-PROBE.md has no confirmed '
      + 'FOOTNOTE_POLICY and a target file contains `[^n]`. Run the Stage-0 probe first.');
  }
  return 'unsupported'; // no footnotes present anyway
}

// ---------------------------------------------------------------------------
// Adjudication allowlist (opt-in, per-plan)
// ---------------------------------------------------------------------------
// Loads a JSON allowlist of REVIEW findings that have been human-adjudicated and cleared.
// Each entry: {file, line, token, verdict, rationale}.
// When a REVIEW finding matches (file basename + line + token substring in message), it is
// reported as ADJUDICATED (cleared) rather than REVIEW. Exit code: 0 when 0 DEFINITE + all
// REVIEWs are either adjudicated or absent. Does NOT change D1-D7 core logic.
function loadAdjudications(adjudicationsPath) {
  if (!adjudicationsPath) return null;
  if (!fs.existsSync(adjudicationsPath)) {
    abort(9, `adjudications file not found: ${adjudicationsPath}`);
  }
  try {
    const raw = JSON.parse(fs.readFileSync(adjudicationsPath, 'utf8'));
    if (!Array.isArray(raw)) {
      abort(9, `adjudications file must contain a JSON array: ${adjudicationsPath}`);
    }
    return raw.map((entry, idx) => {
      if (!entry.file || !entry.line || !entry.token) {
        abort(9, `adjudications[${idx}] missing required field (file, line, token): ${JSON.stringify(entry)}`);
      }
      return {
        file: path.basename(entry.file), // normalize to basename for matching
        line: Number(entry.line),
        token: String(entry.token),
        verdict: entry.verdict || 'adjudicated',
        rationale: entry.rationale || '',
      };
    });
  } catch (e) {
    abort(9, `adjudications file parse error: ${e.message}`);
  }
  return null; // unreachable
}

function findAdjudication(allowlist, finding) {
  if (!allowlist) return null;
  for (const entry of allowlist) {
    if (entry.file === finding.file
        && entry.line === finding.line
        && finding.message.includes(entry.token)) {
      return entry;
    }
  }
  return null;
}

// ---------------------------------------------------------------------------
// Per-file run
// ---------------------------------------------------------------------------
function fileHasFootnotes(model) {
  return model.lines.some((l, i) => model.kind[i] !== 'fence' && /\[\^\d+\]/.test(l));
}

function runFile(file, src, footnotePolicy) {
  const model = modelOf(src);
  const markers = findMarkers(model);
  const metaSet = metaDocLineSet(model);
  const oracleSet = oracleLineSet(model, markers, metaSet);
  const findings = [];
  const suppressed = [];
  layerKatex(model, file, findings);
  layerLint(model, file, findings, suppressed);
  layerSurvivor(model, file, findings, footnotePolicy);
  layerBacktick(model, file, findings, oracleSet);
  layerProse(model, file, findings, oracleSet);
  return { model, file, findings, suppressed, markers };
}

// ---------------------------------------------------------------------------
// Census
// ---------------------------------------------------------------------------
function captureVerbatim(model, line) {
  // join the marker line + contiguous continuation (same blockquote depth / indented), until blank/heading
  const { lines } = model;
  const out = [lines[line].trim()];
  for (let k = line + 1; k < lines.length; k += 1) {
    const l = lines[k];
    if (!l.trim()) break;
    if (/^#{1,6}\s/.test(l)) break;
    if (/^\s*>/.test(lines[line]) && /^\s*>/.test(l)) { out.push(l.trim()); continue; }
    if (/^\s{2,}\S/.test(l) && !/^\s*>/.test(lines[line])) { out.push(l.trim()); continue; }
    break;
  }
  return out.join(' ').replace(/\s+/g, ' ').trim();
}

function runCensus(files) {
  const records = [];
  const perFile = {};
  for (const file of files) {
    const src = fs.readFileSync(file, 'utf8');
    const model = modelOf(src);
    const markers = findMarkers(model);
    const base = path.basename(file);
    perFile[base] = 0;
    // ordinal per section/anchor for stable ids
    const ordinal = {};
    for (const mk of markers) {
      const anchor = anchorOf(model, mk.line);
      ordinal[anchor] = (ordinal[anchor] || 0) + 1;
      const verbatim = captureVerbatim(model, mk.line);
      const textHash = crypto.createHash('sha256').update(verbatim).digest('hex');
      const stableId = `${base.replace(/\.md$/, '')}::${anchor}::${ordinal[anchor]}`;
      records.push({
        form: mk.form, file: base, anchor, line: mk.line + 1,
        snippet: snippetAt(model, mk.line, 0, 80), verbatim, textHash, stableId,
      });
      perFile[base] += 1;
    }
  }
  return { records, perFile, union: records.length };
}

function printCensus(census) {
  const out = [];
  out.push('# Author-comment census (re-derived from live bytes)');
  out.push('');
  for (const r of census.records) {
    out.push(`- [${r.form}] ${r.file} §${r.anchor} (line ${r.line})`);
    out.push(`    snippet: ${r.snippet}`);
    out.push(`    verbatim: ${r.verbatim}`);
    out.push(`    text_hash: ${r.textHash}`);
    out.push(`COMMENT_HASH ${r.stableId} ${r.textHash}`);
  }
  out.push('');
  for (const [f, n] of Object.entries(census.perFile)) out.push(`count ${f}: ${n}`);
  out.push(`count union: ${census.union}`);
  process.stdout.write(`${out.join('\n')}\n`);
}

// ---------------------------------------------------------------------------
// Report
// ---------------------------------------------------------------------------
function printReport(results, adjudications) {
  let definite = 0; let review = 0; let suppressed = 0; let adjudicated = 0;
  const adjudicatedItems = [];
  for (const r of results) {
    const all = [...r.findings].sort((a, b) => a.line - b.line);
    process.stdout.write(`\n=== ${path.basename(r.file)} ===\n`);
    if (!all.length && !r.suppressed.length) { process.stdout.write('  (clean — 0 findings)\n'); continue; }
    for (const f of all) {
      const adj = findAdjudication(adjudications, f);
      if (adj) {
        process.stdout.write(`  [ADJUDICATED/${f.layer}] §${f.anchor} (line ${f.line}): ${f.message}\n`);
        process.stdout.write(`      | ${f.snippet}\n`);
        process.stdout.write(`      | verdict: ${adj.verdict} — ${adj.rationale}\n`);
        adjudicated += 1;
        adjudicatedItems.push({ file: f.file, line: f.line, layer: f.layer, ...adj });
      } else {
        process.stdout.write(`  [${f.tier}/${f.layer}] §${f.anchor} (line ${f.line}): ${f.message}\n`);
        process.stdout.write(`      | ${f.snippet}\n`);
        if (f.tier === 'DEFINITE') definite += 1; else review += 1;
      }
    }
    for (const s of r.suppressed) {
      process.stdout.write(`  [SUPPRESSED/${s.layer}] §${s.anchor} (line ${s.line}): ${s.message}\n`);
      suppressed += 1;
    }
  }
  if (adjudicatedItems.length) {
    process.stdout.write(`\n-- adjudicated (cleared): ${adjudicatedItems.length} --\n`);
    for (const a of adjudicatedItems) {
      process.stdout.write(`  ${a.file}:${a.line} [${a.layer}] ${a.token} → ${a.verdict}\n`);
    }
  }
  process.stdout.write(`\n-- totals: ${definite} DEFINITE, ${review} REVIEW, ${adjudicated} ADJUDICATED, ${suppressed} SUPPRESSED (surfaced for review) --\n`);
  return { definite, review, suppressed, adjudicated };
}

// ---------------------------------------------------------------------------
// Regression / selftest over labeled fixtures
// ---------------------------------------------------------------------------
// Fixture regions are delimited by HTML comment markers (derived from live fixture bytes — no
// hardcoded line numbers): <!-- REGION id=<id> expect=flag|clean -->
function parseRegions(src) {
  const lines = src.split('\n');
  const regions = [];
  let cur = null;
  for (let i = 0; i < lines.length; i += 1) {
    const m = lines[i].match(/<!--\s*REGION\s+id=(\S+)\s+expect=(flag|clean)\s*-->/);
    if (m) {
      if (cur) { cur.end = i - 1; regions.push(cur); }
      cur = { id: m[1], expect: m[2], start: i + 1, end: lines.length - 1 };
    }
  }
  if (cur) regions.push(cur);
  return regions;
}

function runRegression() {
  const src = fs.readFileSync(FIXTURES, 'utf8');
  const regions = parseRegions(src);
  // fixtures exercise the unsupported footnote branch deterministically
  const res = runFile(FIXTURES, src, 'unsupported');
  const findingLines = res.findings.map((f) => f.line - 1); // 0-based
  const problems = [];
  for (const reg of regions) {
    const hits = findingLines.filter((ln) => ln >= reg.start && ln <= reg.end).length;
    if (reg.expect === 'flag' && hits === 0) {
      problems.push(`region '${reg.id}' expected ≥1 finding but got 0`);
    }
    if (reg.expect === 'clean' && hits > 0) {
      const detail = res.findings.filter((f) => (f.line - 1) >= reg.start && (f.line - 1) <= reg.end)
        .map((f) => `${f.layer}:${f.message}`).join('; ');
      problems.push(`region '${reg.id}' expected 0 findings but got ${hits} (${detail})`);
    }
  }
  return { regions, problems, res };
}

function runSelftest() {
  sanityGate();
  process.stdout.write('sanity gate: PASS (inline + block math rendered by KaTeX)\n');
  const reg = runRegression();
  process.stdout.write(`\nregression fixtures: ${reg.regions.length} labeled regions\n`);
  for (const r of reg.regions) process.stdout.write(`  region '${r.id}' expect=${r.expect}\n`);
  // negative control 2: the real sampling_method.md must be 0 findings
  const sSrc = fs.readFileSync(SAMPLING_SPEC, 'utf8');
  const sRes = runFile(SAMPLING_SPEC, sSrc, 'unsupported');
  const samplingProblems = sRes.findings.length
    ? [`sampling_method.md expected 0 findings but got ${sRes.findings.length}: `
       + sRes.findings.map((f) => `${f.layer}@L${f.line}:${f.message}`).join(' | ')]
    : [];
  const problems = [...reg.problems, ...samplingProblems];
  process.stdout.write(`\nnegative control sampling_method.md: ${sRes.findings.length} findings`
    + ` (${sRes.suppressed.length} suppressed)\n`);
  if (problems.length) {
    process.stdout.write('\nSELFTEST FAIL (G1):\n');
    for (const p of problems) process.stdout.write(`  - ${p}\n`);
    process.exit(1);
  }
  process.stdout.write('\nSELFTEST PASS (G1): regression reproduced, negative controls clean.\n');
  process.exit(0);
}

// ---------------------------------------------------------------------------
// CLI
// ---------------------------------------------------------------------------
function usage() {
  process.stdout.write(`spec-render-check — Phase 22 render detector (run from repo root)

Usage:
  node tools/spec-render-check/detect.mjs <file> [file ...]   quick single-file run
  node tools/spec-render-check/detect.mjs --all               all 3 framework specs
  node tools/spec-render-check/detect.mjs --census [--root D] [file ...]
  node tools/spec-render-check/detect.mjs --regression        reproduce author-flag fixtures + controls
  node tools/spec-render-check/detect.mjs --selftest          sanity gate + regression + controls (G1)
  node tools/spec-render-check/detect.mjs --footnote-policy auto|supported|unsupported   (default auto)
  node tools/spec-render-check/detect.mjs --adjudications <path>   load REVIEW adjudication allowlist

Exit: 0 clean · 1 findings · 2 sanity-gate failure · 3 missing prerequisite (footnote probe).
With --adjudications: exit 0 when 0 DEFINITE + every REVIEW is adjudicated or absent.
`);
}

function main() {
  const argv = process.argv.slice(2);
  if (argv.includes('--help') || argv.includes('-h')) { usage(); process.exit(0); }

  let footnotePolicy = 'auto';
  const fpIdx = argv.indexOf('--footnote-policy');
  if (fpIdx !== -1) footnotePolicy = (argv[fpIdx + 1] || 'auto').toLowerCase();

  let adjudicationsPath = null;
  const adjIdx = argv.indexOf('--adjudications');
  if (adjIdx !== -1) adjudicationsPath = argv[adjIdx + 1] || null;

  // Pitfall-1 proof: force a non-callable plugin; the sanity gate must abort with exit 2
  // (never run a layer on an unloaded engine). Exits 2 on success of the proof.
  if (argv.includes('--prove-sanity-gate')) {
    sanityGate({}); // non-callable -> buildMd throws -> abort(2)
    abort(9, 'sanity-gate proof FAILED: a non-callable plugin did not trigger exit 2');
  }

  if (argv.includes('--selftest')) { runSelftest(); return; }

  if (argv.includes('--regression')) {
    sanityGate();
    const reg = runRegression();
    const sSrc = fs.readFileSync(SAMPLING_SPEC, 'utf8');
    const sRes = runFile(SAMPLING_SPEC, sSrc, 'unsupported');
    const problems = [...reg.problems];
    if (sRes.findings.length) problems.push(`sampling_method.md not clean: ${sRes.findings.length} findings`);
    if (problems.length) {
      for (const p of problems) process.stdout.write(`FAIL: ${p}\n`);
      process.exit(1);
    }
    process.stdout.write('REGRESSION PASS: author-flag fixtures reproduced, negative controls clean.\n');
    process.exit(0);
    return;
  }

  if (argv.includes('--census')) {
    let files = [];
    const rootIdx = argv.indexOf('--root');
    const positionals = argv.filter((a, i) => !a.startsWith('--')
      && !(rootIdx !== -1 && i === rootIdx + 1)
      && !(fpIdx !== -1 && i === fpIdx + 1)
      && !(adjIdx !== -1 && i === adjIdx + 1));
    if (rootIdx !== -1) {
      const root = argv[rootIdx + 1];
      files = fs.readdirSync(root).filter((f) => f.endsWith('.md')).map((f) => path.join(root, f));
    } else if (positionals.length) {
      files = positionals.map((f) => path.resolve(f));
    } else {
      files = SPECS;
    }
    printCensus(runCensus(files));
    process.exit(0);
    return;
  }

  // detector run: --all or explicit files
  let files;
  if (argv.includes('--all')) {
    files = SPECS;
  } else {
    const positionals = argv.filter((a, i) => !a.startsWith('--')
      && !(fpIdx !== -1 && i === fpIdx + 1)
      && !(adjIdx !== -1 && i === adjIdx + 1));
    if (!positionals.length) { usage(); process.exit(0); }
    files = positionals.map((f) => path.resolve(f));
  }

  sanityGate();

  // resolve footnote policy once (auto needs to know if any target has footnotes)
  const sources = files.map((f) => ({ file: f, src: fs.readFileSync(f, 'utf8') }));
  const anyFootnotes = sources.some(({ src }) => fileHasFootnotes(modelOf(src)));
  const policy = resolveFootnotePolicy(footnotePolicy, anyFootnotes);

  const adjudications = loadAdjudications(adjudicationsPath);
  const results = sources.map(({ file, src }) => runFile(file, src, policy));
  const totals = printReport(results, adjudications);
  process.exit(totals.definite + totals.review > 0 ? 1 : 0);
}

main();
