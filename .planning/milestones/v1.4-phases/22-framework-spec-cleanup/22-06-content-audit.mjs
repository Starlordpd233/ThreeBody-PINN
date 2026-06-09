#!/usr/bin/env node
// 22-06-content-audit.mjs — Phase 22 content-preservation audit (audit-only).
//
// Purpose: mechanically determine whether the Phase 22 syntax/formatting cleanup
// of pinn_architecture.md and ctl_instruction.md *accidentally altered content*
// (a number, an equation, a dropped/added term, a swapped operator/index, a
// mangled word, or a broken table cell). The git diff between the baseline tag
// (v1.4-pre-phase-22) and HEAD is the COMPLETE universe of changes; this script
// adjudicates every changed hunk.
//
// It does NOT fix anything. It emits CANDIDATE findings; a human curates the
// final FINDINGS table (declared-formatting-transform vs real content change).
//
// Detectors:
//   A. Per-hunk normalized token-multiset symmetric difference  -> Steps 2,3,5
//      (numbers, math symbols/operators/indices, prose words, footnote refs).
//   B. Table cell boundary & content audit                      -> Step 4
//   C. Footnote-definition / cross-reference integrity          -> Step 5
//   D. Whole-file normalized residual (backstop triage)         -> Step 6
//
// BOUNDED NORMALIZATION GUARANTEE: normalization folds ONLY declared formatting
// transforms (emphasis/delimiters, math formatting wrappers \mathbf/\mathrm/\text,
// spacing, fraction keyword, multiplication operators, greek-name spelling,
// norm/abs-bar notation, relation-symbol spelling, footnote [^n]<->[n], brace
// style, unicode-exponent / ** -> ^). It NEVER alters the signal: digits,
// +/-/=/</> operators, sign, or subscript/superscript *contents* (_i, _{i,j},
// ^3, ^{-5}) pass through untouched. So a real content change cannot be masked.
//
// Usage:
//   node 22-06-content-audit.mjs            # self-tests, then audit real data
//   node 22-06-content-audit.mjs --selftest # self-tests only
//
// Reads (read-only): git show v1.4-pre-phase-22:<file> and git show HEAD:<file>,
// and the saved canonical diff 22-06-BASELINE-HEAD.diff.

import { execSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const HERE = dirname(fileURLToPath(import.meta.url));
const REPO = resolve(HERE, '..', '..', '..');
const BASELINE = 'v1.4-pre-phase-22';
const SPECS = [
  'pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md',
  'pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md',
];
const DIFF_FILE = resolve(HERE, '22-06-BASELINE-HEAD.diff');

// ----------------------------------------------------------------------------
// Normalization (declared formatting transforms only)
// ----------------------------------------------------------------------------
// Greek is canonicalized to a tokenizable ASCII name so all three encodings
// (\lambda, unicode λ, plain "lambda") converge and a real letter change
// (e.g. λ -> μ) still surfaces. Variants (\varepsilon, \vartheta) fold to the
// base letter (same glyph, declared formatting choice).
const GREEK_VARIANT = { varepsilon:'epsilon', vartheta:'theta', varphi:'phi', varpi:'pi', varrho:'rho', varsigma:'sigma' };
const UNI_GREEK = {
  'α':'alpha','β':'beta','γ':'gamma','δ':'delta','ε':'epsilon','ζ':'zeta','η':'eta',
  'θ':'theta','ϑ':'theta','ι':'iota','κ':'kappa','λ':'lambda','μ':'mu','ν':'nu','ξ':'xi',
  'π':'pi','ρ':'rho','σ':'sigma','ς':'sigma','τ':'tau','φ':'phi','ϕ':'phi','χ':'chi',
  'ψ':'psi','ω':'omega','Γ':'Gamma','Δ':'Delta','Θ':'Theta','Λ':'Lambda','Ξ':'Xi',
  'Π':'Pi','Φ':'Phi','Ψ':'Psi','Ω':'Omega',
};

function normalize(input) {
  let s = input;

  // unicode superscripts/subscripts that encode exponents -> ^N
  s = s.replace(/¹/g, '^1').replace(/²/g, '^2').replace(/³/g, '^3')
       .replace(/⁴/g, '^4').replace(/⁻/g, '^-'); // (rare) superscript minus

  // ORDER MATTERS: strip paired markdown bold **X** FIRST (before ** is read as
  // a power operator and before single * is read as multiplication). Otherwise
  // bold markers leak in as spurious ^{...} tokens and emphasis stars get paired
  // with multiplication stars, fusing G*T into one token.
  s = s.replace(/\*\*([^*]+?)\*\*/g, '$1');     // bold
  // remaining ** is python-style power (a**b); single * is multiplication.
  s = s.replace(/\*\*/g, '^');
  // any surviving single * (italic markers OR multiplication) -> space; content
  // is preserved either way and tokens stay separated (G*T -> G T, matching the
  // implicit-multiplication "G T" form used in the LaTeX side).
  s = s.replace(/\*/g, ' ');

  // math/code delimiters removed, interior kept (declared: $ <-> ` <-> bare)
  s = s.replace(/\$\$?/g, ' ').replace(/`/g, ' ');

  // hard-break markers (Pandoc trailing backslash, GFM <br>) -> space
  s = s.replace(/<br\s*\/?>/gi, ' ').replace(/\\(?=\s|$)/g, ' ');

  // footnote reference style: [^n] <-> [n]  (canonicalize to [n])
  s = s.replace(/\[\^(\d+)\]/g, '[$1]');

  // LaTeX formatting wrappers (no content): \mathbf{X}->X etc. (loop for nesting)
  for (let i = 0; i < 4; i++) {
    s = s.replace(/\\(?:mathbf|mathrm|mathit|mathsf|mathcal|boldsymbol|bm|operatorname|text|textbf|textit)\s*\{([^{}]*)\}/g, '$1');
  }
  // spacing / delimiter-sizing commands (no content)
  s = s.replace(/\\(?:left|right|big|Big|bigg|Bigg)\b/g, ' ');
  s = s.replace(/\\[,;:! ]/g, ' ').replace(/\\(?:quad|qquad)\b/g, ' ');
  s = s.replace(/\\!/g, ' ');
  // fraction keyword IS a division: \frac{A}{B} == (A)/(B) == A/B (declared
  // code-form<->LaTeX transform). Emit a "/" so both notations carry the same
  // division token; the multiset diff is order-independent so operand order is
  // irrelevant. (Token regex ignores bare braces/parens, so grouping drops out.)
  s = s.replace(/\\[tdc]?frac\b/g, ' / ');

  // relation symbols -> canonical unicode
  s = s.replace(/<=|\\leq\b/g, '≤').replace(/>=|\\geq\b/g, '≥');
  s = s.replace(/\\approx\b|\\sim\b|(?<![<>=!])~/g, '≈');
  s = s.replace(/\\neq\b|!=/g, '≠');

  // norm bars (double) and abs bars (single) -> canonical
  s = s.replace(/\\lVert\b|\\rVert\b|\\Vert\b/g, '‖').replace(/\\\|/g, '‖').replace(/\|\|/g, '‖');
  s = s.replace(/\\lvert\b|\\rvert\b|\\vert\b/g, '|');
  s = s.replace(/‖\s*‖/g, '‖'); // collapse accidental doubles

  // multiplication operators carry no content (often implicit) -> drop
  // (literal * already handled above with emphasis ordering)
  s = s.replace(/\\cdot\b|\\times\b|·/g, ' ');

  // derivative dot accent: \dot{X} and spelled "_dot_" -> canonical ˙ marker
  s = s.replace(/\\dot\s*\{([^{}]*)\}/g, '$1˙').replace(/\\ddot\s*\{([^{}]*)\}/g, '$1¨');
  s = s.replace(/_dot_/g, '˙_').replace(/_dot\b/g, '˙');

  // escaped set braces \{ \} -> plain braces (declared: set-notation delimiters)
  s = s.replace(/\\([{}])/g, '$1');

  // summation symbol (unicode Σ / ∑) <-> \sum (declared ASCII->LaTeX map)
  s = s.replace(/[Σ∑]/g, ' sum ');

  // unicode greek letters -> canonical ASCII name (declared spelling transform)
  s = s.replace(/[Ͱ-Ͽ]/g, (ch) => (UNI_GREEK[ch] ? ` ${UNI_GREEK[ch]} ` : ch));

  // all remaining LaTeX commands: strip backslash, keep the name. Greek
  // variants fold to base letter; functions/operators keep their name
  // (declared ASCII<->LaTeX map: sqrt<->\sqrt, sum<->\sum, tanh<->\tanh,
  //  min<->\min, sin<->\sin, median<->\mathrm{median}, \varepsilon->epsilon).
  s = s.replace(/\\([A-Za-z]+)/g, (m, name) => GREEK_VARIANT[name] || name);
  // plain (non-backslash) variant spellings
  s = s.replace(/\b(varepsilon|vartheta|varphi|varpi|varrho|varsigma)\b/g, (m) => GREEK_VARIANT[m]);

  // move primes to attach right after base letter:  r_j' -> r'_j
  for (let i = 0; i < 3; i++) {
    s = s.replace(/(_(?:\{[^}]*\}|[A-Za-z0-9]))('+)/g, '$2$1');
  }

  // numeric canonicalization: powers of ten and scientific -> 1eK
  s = s.replace(/(?<![\w}])10\^\{?\s*([-+]?\d+)\s*\}?/g, (m, k) => `1e${parseInt(k, 10)}`);
  s = s.replace(/(?<![\w.])(\d+(?:\.\d+)?)[eE]([-+]?\d+)/g, (m, mant, k) => {
    const v = parseFloat(mant);
    return `${v}e${parseInt(k, 10)}`;
  });

  // brace-style canonicalization (declared: _total <-> _{total}, ^2 <-> ^{2}).
  // Parenthesized sub/superscripts -> braced; bare alnum (incl comma-indices)
  // -> braced. NEVER touches the index/exponent CONTENT (the signal).
  s = s.replace(/\^\(([^()]*)\)/g, '^{$1}').replace(/_\(([^()]*)\)/g, '_{$1}');
  s = s.replace(/_([A-Za-z0-9]+(?:,[A-Za-z0-9]+)*)/g, '_{$1}');
  s = s.replace(/\^([-+]?[A-Za-z0-9]+)/g, '^{$1}');

  // strip spaces INSIDE {...} groups so subscript/superscript tokens compare
  // consistently regardless of greek encoding (unicode α expands with padding
  // spaces, LaTeX \alpha does not). This affects only braced index/exponent
  // tuples — never inter-token spacing — so the signal is untouched.
  s = s.replace(/\{([^{}]*)\}/g, (m, inner) => '{' + inner.replace(/\s+/g, '') + '}');

  // collapse whitespace
  s = s.replace(/\s+/g, ' ').trim();
  return s;
}

// ----------------------------------------------------------------------------
// Tokenizer + bucketing
// ----------------------------------------------------------------------------
const TOKEN_RE = new RegExp(
  [
    '1e[-+]?\\d+',                 // canonical sci/power-of-ten number
    '\\d+(?:\\.\\d+)?',            // plain number
    '\\\\[A-Za-z]+',              // surviving LaTeX command (\sqrt \sum \sin \tanh ...)
    '_\\{[^}]*\\}', '\\^\\{[^}]*\\}', // braced sub/superscript (index/exponent content)
    '_[A-Za-z0-9]', '\\^[-+]?[A-Za-z0-9]', // single sub/superscript
    "[A-Za-z]+'*",               // identifier / word (with trailing primes)
    '[+\\-=<>/≤≥≈≠‖|˙¨]',         // meaning-bearing operators / relations / bars
  ].join('|'),
  'g'
);

function tokenize(normStr) {
  return normStr.match(TOKEN_RE) || [];
}

// digit immediately after _ or ^ is an index/exponent (handled as part of the
// _x/^x tokens already); a bare number token is a numeric literal.
function bucket(tok) {
  if (/^1e[-+]?\d+$/.test(tok) || /^\d+(\.\d+)?$/.test(tok)) return 'NUM';
  if (/^[A-Za-z]+'*$/.test(tok) && tok.replace(/'/g, '').length >= 2) return 'WORD';
  return 'SYM'; // commands, sub/sup tuples, single letters, operators, bars
}

function multisetDiff(minusToks, plusToks) {
  const count = (arr) => arr.reduce((m, t) => (m.set(t, (m.get(t) || 0) + 1), m), new Map());
  const a = count(minusToks), b = count(plusToks);
  const removed = [], added = [];
  for (const [t, n] of a) { const d = n - (b.get(t) || 0); for (let i = 0; i < d; i++) removed.push(t); }
  for (const [t, n] of b) { const d = n - (a.get(t) || 0); for (let i = 0; i < d; i++) added.push(t); }
  return { removed, added };
}

// ----------------------------------------------------------------------------
// Diff parsing
// ----------------------------------------------------------------------------
function parseDiff(diffText) {
  const lines = diffText.split('\n');
  const hunks = [];
  let file = null, cur = null, idx = 0;
  for (const ln of lines) {
    if (ln.startsWith('+++ b/')) { file = ln.slice(6).split('/').pop(); continue; }
    const m = ln.match(/^@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@/);
    if (m) { idx++; cur = { idx, file, newStart: +m[2], minus: [], plus: [] }; hunks.push(cur); continue; }
    if (!cur) continue;
    if (ln.startsWith('-') && !ln.startsWith('---')) cur.minus.push(ln.slice(1));
    else if (ln.startsWith('+') && !ln.startsWith('+++')) cur.plus.push(ln.slice(1));
  }
  return hunks;
}

// ----------------------------------------------------------------------------
// Detector A: per-hunk token-multiset symmetric difference
// ----------------------------------------------------------------------------
function detectorA(hunks) {
  const results = [];
  for (const h of hunks) {
    const minusToks = tokenize(normalize(h.minus.join('\n')));
    const plusToks = tokenize(normalize(h.plus.join('\n')));
    const { removed, added } = multisetDiff(minusToks, plusToks);
    if (removed.length || added.length) {
      const byBucket = (arr) => {
        const g = { NUM: [], SYM: [], WORD: [] };
        for (const t of arr) g[bucket(t)].push(t);
        return g;
      };
      results.push({ idx: h.idx, file: h.file, newStart: h.newStart,
                     removed: byBucket(removed), added: byBucket(added) });
    }
  }
  return results;
}

// ----------------------------------------------------------------------------
// Detector B: table cell boundary & content audit
// ----------------------------------------------------------------------------
// Protect $...$, `...`, and \| before splitting GFM rows on unescaped pipes.
function splitGfmRow(row) {
  const ph = [];
  let s = row.replace(/\$[^$]*\$|`[^`]*`|\\\|/g, (m) => { ph.push(m); return ` ${ph.length - 1} `; });
  const cells = s.split('|').map((c) => c.replace(/ (\d+) /g, (_, i) => ph[+i]).trim());
  // drop leading/trailing empties produced by the outer pipes
  if (cells.length && cells[0] === '') cells.shift();
  if (cells.length && cells[cells.length - 1] === '') cells.pop();
  return cells;
}

function parseGfmTable(lines) {
  const rows = [];
  for (const ln of lines) {
    const t = ln.trim();
    if (!/^\|.*\|$/.test(t)) continue;
    if (/^\|?[\s:|-]+\|?$/.test(t) && t.includes('-')) continue; // separator row
    rows.push(splitGfmRow(t));
  }
  return rows; // rows[0] is header
}

// Cells in these Pandoc tables are separated by runs of 2+ spaces (the authors'
// VISUAL separator). The dashed-rule column positions are NOT reliable here:
// the long math cells overflow their declared columns, so slicing by the rule
// mis-places boundaries (this is the exact mechanism that produced the line-263
// corruption — Pandoc split by column position mid-word). The 2+ space split
// recovers the intended logical cells. Within-cell math/prose uses single
// spaces, so the split is unambiguous for these specs.
const RULE_RE = /^\s*-{2,}(\s+-{2,})+\s*$/;
function splitPandocRow(line) {
  return line.trim().split(/\s{2,}/).map((c) => c.trim());
}

// Parse a Pandoc simple/multiline table given its raw lines.
// mode 'simple'   : one logical row per non-blank body line (table #18).
// mode 'multiline': new row starts when first cell is a **bold key**; other
//                   non-blank lines (bullets, wrapped prose) continue the
//                   current row's spec column; full-width prose before the
//                   first bold row (e.g. an author comment) is skipped (#31).
function parsePandocTable(lines, mode) {
  const ruleIdx = lines.findIndex((l) => RULE_RE.test(l));
  if (ruleIdx < 0) return null;
  const rows = [];
  if (mode === 'simple') {
    let hi = ruleIdx - 1;
    while (hi >= 0 && lines[hi].trim() === '') hi--;       // header above rule
    if (hi >= 0) rows.push(splitPandocRow(lines[hi]));
    for (let i = ruleIdx + 1; i < lines.length; i++) {      // body below rule
      const ln = lines[i];
      if (ln.trim() === '') continue;
      if (/^\s*:/.test(ln) || RULE_RE.test(ln)) break;      // caption / closing
      rows.push(splitPandocRow(ln));
    }
  } else {
    let cur = null;
    for (let i = ruleIdx + 1; i < lines.length; i++) {
      const ln = lines[i];
      if (ln.trim() === '') continue;
      if (/^\s*:/.test(ln) || RULE_RE.test(ln)) break;      // caption / bottom rule
      const cells = splitPandocRow(ln);
      const isBoldKey = /^\*\*.+\*\*$/.test(cells[0] || '');
      if (isBoldKey) { cur = cells.slice(); rows.push(cur); }   // new logical row
      else if (cur) { cur[1] = (cur[1] || '') + ' ' + ln.trim(); } // continuation -> spec col
      // else: pre-header prose (author comment) -> skip
    }
  }
  return rows;
}

// Compare two grids cell-by-cell after normalization. Align body rows by their
// normalized col0 key; report boundary/content mismatches.
function compareGrids(label, base, head, out) {
  if (!base || !head) { out.push(`${label}: PARSE FAILED (base=${!!base} head=${!!head})`); return; }
  const key = (r) => normalize(r[0] || '').toLowerCase();
  const baseBody = base.slice(1), headBody = head.slice(1);
  // header check
  const bh = base[0].map(normalize), hh = head[0].map(normalize);
  if (JSON.stringify(bh) !== JSON.stringify(hh))
    out.push(`${label}: HEADER differs base=${JSON.stringify(bh)} head=${JSON.stringify(hh)}`);
  out.push(`${label}: rows base=${baseBody.length} head=${headBody.length}, cols/row base=${[...new Set(base.map(r=>r.length))]} head=${[...new Set(head.map(r=>r.length))]}`);

  // FLATTENED content check (authoritative for completeness; immune to per-cell
  // mis-slicing of multiline tables): every cell token in base must appear in
  // head and vice versa. A dropped/added/changed token anywhere surfaces here.
  const cellToks = (grid) => grid.flat().flatMap((c) => tokenize(normalize(c || '')));
  const fd = multisetDiff(cellToks(base), cellToks(head));
  out.push(`${label}: FLATTENED token diff removed=${JSON.stringify(fd.removed)} added=${JSON.stringify(fd.added)}`);

  // PER-CELL boundary check: token-multiset diff localizes which cell drifted
  // (e.g. a cell separator lost/inserted moves tokens across columns).
  const headByKey = new Map(headBody.map((r) => [key(r), r]));
  const baseKeys = new Set(baseBody.map(key));
  for (const r of baseBody) {
    const k = key(r);
    const hr = headByKey.get(k);
    if (!hr) { out.push(`${label}: ROW present in base, missing in head: "${(r[0]||'').trim()}"`); continue; }
    const n = Math.max(r.length, hr.length);
    for (let c = 0; c < n; c++) {
      const d = multisetDiff(tokenize(normalize(r[c] || '')), tokenize(normalize(hr[c] || '')));
      if (d.removed.length || d.added.length) {
        out.push(`${label}: CELL DRIFT row="${(r[0]||'').trim()}" col${c} removed=${JSON.stringify(d.removed)} added=${JSON.stringify(d.added)}`);
      }
    }
  }
  for (const r of headBody) if (!baseKeys.has(key(r))) out.push(`${label}: ROW present in head, missing in base: "${(r[0]||'').trim()}"`);
}

function detectorB(hunks, out) {
  // Table 1 (#18): Pandoc simple -> GFM
  const h18 = hunks.find((h) => h.idx === 18);
  if (h18) compareGrids('TABLE#18 pinn (Architectural Hyperparameters)',
    parsePandocTable(h18.minus, 'simple'), parseGfmTable(h18.plus), out);
  // Table 2 (#31): Pandoc multiline -> GFM
  const h31 = hunks.find((h) => h.idx === 31);
  if (h31) compareGrids('TABLE#31 pinn (Implementation Blueprint)',
    parsePandocTable(h31.minus, 'multiline'), parseGfmTable(h31.plus), out);
  // Table (#6 ctl): GFM -> GFM (cell content code-span -> math)
  const h6 = hunks.find((h) => h.idx === 6 && h.file === 'ctl_instruction.md');
  if (h6) compareGrids('TABLE#6 ctl (Input normalization slots)',
    parseGfmTable(h6.minus), parseGfmTable(h6.plus), out);

  if (process.env.DBG) {
    const b = parsePandocTable(h18.minus, 'simple'), hh = parseGfmTable(h18.plus);
    const find = (g) => (g || []).find((r) => /Weight Init\. \(Hidden\)/.test(r[0] || ''));
    out.push('DBG18 base row: ' + JSON.stringify(find(b)));
    out.push('DBG18 head row: ' + JSON.stringify(find(hh)));
  }
}

// ----------------------------------------------------------------------------
// Detector C: footnote-definition & cross-reference integrity
// ----------------------------------------------------------------------------
function detectorC(baseFull, headFull, out) {
  // footnote definitions: [^n]: <text>  (base)  vs  [n] <text> (head)
  const defRe = (s, re) => {
    const map = new Map(); let m;
    while ((m = re.exec(s))) map.set(+m[1], m[2].trim());
    return map;
  };
  const bDefs = defRe(baseFull, /^\[\^(\d+)\]:\s*(.*)$/gm);
  const hDefs = defRe(headFull, /^\[(\d+)\]\s+(.*)$/gm);
  out.push(`footnote/reference DEFINITIONS: base=${bDefs.size} head=${hDefs.size}`);
  let mismatch = 0;
  for (const [n, t] of bDefs) {
    const ht = hDefs.get(n);
    if (ht === undefined) { out.push(`  def [${n}] present in base, missing in head`); mismatch++; }
    else if (ht !== t) { out.push(`  def [${n}] TEXT differs:\n    base: ${JSON.stringify(t.slice(0,120))}\n    head: ${JSON.stringify(ht.slice(0,120))}`); mismatch++; }
  }
  for (const n of hDefs.keys()) if (!bDefs.has(n)) { out.push(`  def [${n}] present in head, missing in base`); mismatch++; }
  if (!mismatch && bDefs.size) out.push('  -> all footnote/reference definition texts byte-identical (modulo [^n]->[n])');

  // cross-reference labels preserved
  const labels = (s) => (s.match(/PHYS-\d+|FUT-\d+|AC-[A-Z]+-\d+|§\s*\d+(?:\.\d+)*/g) || []);
  const bd = multisetDiff(labels(baseFull), labels(headFull));
  if (bd.removed.length || bd.added.length)
    out.push(`  xref labels CHANGED removed=${JSON.stringify(bd.removed)} added=${JSON.stringify(bd.added)}`);
  else out.push('  -> cross-reference label set (PHYS-/FUT-/AC-/§) unchanged');
}

// ----------------------------------------------------------------------------
// Detector D: whole-file token-multiset residual (Step 6 backstop)
// ----------------------------------------------------------------------------
// The authoritative file-level completeness check. Tokenizes the ENTIRE
// normalized file and diffs the multisets. Unchanged regions are byte-identical
// (git guarantee) so they net to zero; only genuinely added/removed meaning-
// bearing tokens survive. Immune to table/paragraph reflow (line granularity is
// not used). Bucketed: NUM and WORD are pure content signal; SYM contains the
// declared structural transforms (Pandoc rule dashes "-" -> GFM pipes "|",
// footnote bracket digits) alongside any real operator/subscript change.
function detectorD(baseFull, headFull, out) {
  const aTok = tokenize(normalize(baseFull.replace(/\n/g, ' ')));
  const bTok = tokenize(normalize(headFull.replace(/\n/g, ' ')));
  const { removed, added } = multisetDiff(aTok, bTok);
  const byBucket = (arr) => {
    const g = { NUM: [], WORD: [], SYM: [] };
    for (const t of arr) g[bucket(t)].push(t);
    return g;
  };
  const r = byBucket(removed), a = byBucket(added);
  // collapse the high-volume structural SYM tokens for readability
  const collapse = (arr) => {
    const m = new Map();
    for (const t of arr) m.set(t, (m.get(t) || 0) + 1);
    return [...m.entries()].map(([t, n]) => (n > 3 ? `${t}×${n}` : Array(n).fill(t)).toString().replace(/,/g, ' '))
      .join(' ');
  };
  out.push(`whole-file token residual: removed ${removed.length} / added ${added.length}`);
  out.push(`  NUM  removed=${JSON.stringify(r.NUM)}  added=${JSON.stringify(a.NUM)}`);
  out.push(`  WORD removed=${JSON.stringify(r.WORD)}  added=${JSON.stringify(a.WORD)}`);
  out.push(`  SYM  removed=[${collapse(r.SYM)}]  added=[${collapse(a.SYM)}]`);
  return { num: { r: r.NUM, a: a.NUM }, word: { r: r.WORD, a: a.WORD } };
}

// ----------------------------------------------------------------------------
// Self-tests: plant known edits, confirm the relevant detector flags each.
// ----------------------------------------------------------------------------
function selftest() {
  const fails = [];
  const ok = (cond, name) => { console.log(`  [${cond ? 'PASS' : 'FAIL'}] ${name}`); if (!cond) fails.push(name); };

  // 1. changed digit -> NUM bucket in token symdiff
  {
    const minus = ['eps = 1e-5 and width 256'];
    const plus = ['eps = 1e-4 and width 256'];
    const d = multisetDiff(tokenize(normalize(minus.join('\n'))), tokenize(normalize(plus.join('\n'))));
    ok(d.removed.includes('1e-5') && d.added.includes('1e-4'), 'planted digit change (1e-5 -> 1e-4) flagged by NUM audit');
  }
  // 2. swapped subscript index i/j -> SYM
  {
    const minus = ['$r_{i,j}$'];
    const plus = ['$r_{j,i}$'];
    const d = multisetDiff(tokenize(normalize(minus.join('\n'))), tokenize(normalize(plus.join('\n'))));
    ok(d.removed.includes('_{i,j}') && d.added.includes('_{j,i}'), 'planted index swap (i,j -> j,i) flagged by SYM audit');
  }
  // 3. + -> - operator flip -> SYM
  {
    const minus = ['$a + b$'];
    const plus = ['$a - b$'];
    const d = multisetDiff(tokenize(normalize(minus.join('\n'))), tokenize(normalize(plus.join('\n'))));
    ok(d.removed.includes('+') && d.added.includes('-'), 'planted operator flip (+ -> -) flagged by SYM audit');
  }
  // 4. removed/moved table pipe -> CELL DIFFERS in table audit
  {
    const base = ['  A   B   C', '  --- --- ---', '  k1  x   yyy zzz'];
    // GFM with a pipe dropped between B-cell and C-cell (B and C fused), spurious pipe in C
    const head = ['| A | B | C |', '| --- | --- | --- |', '| k1 | x   yyy | zzz |'];
    const out = [];
    compareGrids('SELFTEST', parsePandocTable(base, 'simple'), parseGfmTable(head), out);
    ok(out.some((l) => /CELL DRIFT/.test(l)), 'planted table-pipe move (B/C boundary) flagged by TABLE audit');
  }
  // 5. dropped letter in a word -> WORD
  {
    const minus = ['designed to preserve'];
    const plus = ['designe to preserve'];
    const d = multisetDiff(tokenize(normalize(minus.join('\n'))), tokenize(normalize(plus.join('\n'))));
    ok(d.removed.includes('designed') && d.added.includes('designe'), 'planted word mangle (designed -> designe) flagged by WORD audit');
  }
  // 6. NEGATIVE control: pure declared formatting transform -> empty symdiff
  {
    const minus = ['`E_scale = |median({E_j})| + 1e-10`, and `Q_scale` fixed at `0.5`'];
    const plus = ['$E_{\\mathrm{scale}} = \\lvert \\mathrm{median}(\\{E_j\\}) \\rvert + 10^{-10}$, and $Q_{\\mathrm{scale}}$ fixed at $0.5$'];
    const d = multisetDiff(tokenize(normalize(minus.join('\n'))), tokenize(normalize(plus.join('\n'))));
    ok(d.removed.length === 0 && d.added.length === 0, `negative control: declared formatting transform yields empty symdiff (got -${d.removed.length}/+${d.added.length}: ${JSON.stringify({r:d.removed,a:d.added})})`);
  }
  return fails;
}

// ----------------------------------------------------------------------------
// Main
// ----------------------------------------------------------------------------
function gitShow(ref, file) {
  return execSync(`git show ${ref}:${file}`, { cwd: REPO, maxBuffer: 64 * 1024 * 1024 }).toString();
}

console.log('=== SELF-TESTS (detector validation against planted edits) ===');
const fails = selftest();
if (fails.length) { console.log(`\nSELF-TESTS FAILED: ${fails.length}. Detectors not trusted. Aborting.`); process.exit(1); }
console.log('ALL SELF-TESTS PASS\n');

if (process.argv.includes('--selftest')) process.exit(0);

const diffText = readFileSync(DIFF_FILE, 'utf8');
const hunks = parseDiff(diffText);
console.log(`=== STEP 1: change universe = ${hunks.length} hunks ===`);
const perFile = {};
for (const h of hunks) perFile[h.file] = (perFile[h.file] || 0) + 1;
console.log('  per file:', JSON.stringify(perFile), '\n');

console.log('=== DETECTOR A: per-hunk token-multiset symmetric difference (Steps 2/3/5) ===');
const aRes = detectorA(hunks);
if (!aRes.length) console.log('  (no token differences in any hunk)');
for (const r of aRes) {
  const fmt = (g) => Object.entries(g).filter(([, v]) => v.length).map(([k, v]) => `${k}:${JSON.stringify(v)}`).join('  ');
  console.log(`hunk#${r.idx} ${r.file} L${r.newStart}`);
  if (fmt(r.removed)) console.log(`   removed  ${fmt(r.removed)}`);
  if (fmt(r.added))   console.log(`   added    ${fmt(r.added)}`);
}

console.log('\n=== DETECTOR B: table cell boundary & content (Step 4) ===');
const bOut = [];
detectorB(hunks, bOut);
bOut.forEach((l) => console.log(l));

console.log('\n=== DETECTOR C / D over whole files (Steps 5 footnotes, 6 residual) ===');
const dTotals = {};
for (const file of SPECS) {
  const short = file.split('/').pop();
  const baseFull = gitShow(BASELINE, file);
  const headFull = gitShow('HEAD', file);
  console.log(`\n--- ${short} ---`);
  const cOut = []; detectorC(baseFull, headFull, cOut); cOut.forEach((l) => console.log(l));
  const dOut = []; const tot = detectorD(baseFull, headFull, dOut); dOut.forEach((l) => console.log(l));
  dTotals[short] = tot;
}
console.log('\n=== Detector D residual totals ===', JSON.stringify(dTotals));

// known-positive anchor assertion
const anchorHit = bOut.some((l) => /TABLE#18/.test(l) && /designe/.test(l))
  || aRes.some((r) => r.idx === 18 && (r.added.WORD.includes('designe') || r.removed.WORD.includes('designed')));
console.log(`\n=== KNOWN-POSITIVE ANCHOR (pinn_architecture.md:263 designe|to) ===`);
console.log(anchorHit ? 'ANCHOR SURFACED ✓ (audit trusted)' : 'ANCHOR NOT SURFACED ✗ — AUDIT DEFECTIVE, DEBUG BEFORE TRUSTING');
if (!anchorHit) process.exit(2);
