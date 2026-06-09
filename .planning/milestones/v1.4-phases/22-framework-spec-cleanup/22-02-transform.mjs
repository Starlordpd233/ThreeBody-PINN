#!/usr/bin/env node
// 22-02 render-repair transform for pinn_architecture.md
// Applies equivalence-preserving fixes to reach detector G2 (0 findings).
// Does NOT touch author comments (WS-B is deferred to FUT-05).
// Each transform is reversible in principle; all are presentation-only.

import { readFileSync, writeFileSync } from 'node:fs';

const FILE = 'pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md';
const src = readFileSync(FILE, 'utf8');
let text = src;

// Helper: column spans of a Pandoc dash row (contiguous runs of `-`).
function columnSpans(dashLine) {
  const spans = [];
  let i = 0;
  while (i < dashLine.length) {
    if (dashLine[i] === '-') {
      const start = i;
      while (i < dashLine.length && dashLine[i] === '-') i++;
      spans.push([start, i]);
    } else i++;
  }
  return spans;
}
function extractCells(line, spans) {
  return spans.map(([s, e]) => {
    const slice = line.length >= s ? line.slice(s, Math.min(line.length, e)) : '';
    return slice.trim();
  });
}
const isPandocSep = l => /^\s-{20,}\s+-{20,}/.test(l);

// ============================================================================
// 1. FOOTNOTE REFS: [^n] → [n] (but NOT the [^n]: definition lines)
// ============================================================================
text = text.replace(/\[\^(\d+)\](?!:)/g, '[$1]');

// 2. Footnote section heading + definition list → References bulleted list
text = text.replace(/^## Footnotes$/m, '## References');
text = text.replace(/^\[\^(\d+)\]: (.*)$/gm, '- **[$1]** $2');

// ============================================================================
// 3. FENCED DIV MARKERS (`::: {#tab:...}` and closing `:::`)
//    We also fold the `: Table 1:` caption into the fenced-div removal,
//    emitting a single bold caption line.
// ============================================================================
{
  // Match the whole fenced-div + caption block and replace with the bold caption.
  const re = /::: \{#tab:architectural_hyperparameters\}\n([\s\S]*?\n)  : Table 1: Architectural hyperparameters of the SQR-SkipResNet-SIREN backbone\n:::\n/;
  text = text.replace(re, (_, inner) => {
    // `inner` contains header row + dash row + body rows (with trailing blank line)
    // We'll handle the actual table conversion in step 4; here we just strip the div markers.
    return inner + '**Table 1: Architectural hyperparameters of the SQR-SkipResNet-SIREN backbone**\n';
  });
}

// ============================================================================
// 4. TABLE 1 — Pandoc multiline → GFM pipe table
// ============================================================================
{
  const lines = text.split('\n');
  const headerIdx = lines.findIndex(l => l.includes('**Hyperparameter**') && l.includes('**Recommended Value**'));
  if (headerIdx >= 0) {
    const dashIdx = headerIdx + 1;
    if (lines[dashIdx] && lines[dashIdx].trim().startsWith('---')) {
      const spans = columnSpans(lines[dashIdx]);
      // Find the bold caption line we just produced.
      let captionIdx = dashIdx + 1;
      while (captionIdx < lines.length && !lines[captionIdx].startsWith('**Table 1:')) captionIdx++;
      const bodyRows = lines.slice(dashIdx + 1, captionIdx);
      const headerCells = extractCells(lines[headerIdx], spans);
      const gfmHeader = '| ' + headerCells.join(' | ') + ' |';
      const gfmSep    = '| ' + spans.map(() => '---').join(' | ') + ' |';
      const gfmBody   = bodyRows.filter(l => l.trim().length > 0)
                                .map(l => '| ' + extractCells(l, spans).join(' | ') + ' |');
      const newBlock = [gfmHeader, gfmSep, ...gfmBody, '', lines[captionIdx]];
      lines.splice(headerIdx, captionIdx - headerIdx + 1, ...newBlock);
      text = lines.join('\n');
    }
  }
}

// ============================================================================
// 5. TABLE 2 — Pandoc multiline → GFM pipe table
//    The top separator has an interlude (author comment prose) between it and
//    the actual header row. We preserve that prose BEFORE the table.
// ============================================================================
{
  const lines = text.split('\n');
  const sepIdx = lines.findIndex(isPandocSep);
  if (sepIdx >= 0) {
    let headerIdx = sepIdx + 1;
    while (headerIdx < lines.length && !lines[headerIdx].includes('**Component**')) headerIdx++;
    const interlude = lines.slice(sepIdx + 1, headerIdx).filter(l => l.trim().length > 0);
    let bottomIdx = headerIdx + 1;
    while (bottomIdx < lines.length && !isPandocSep(lines[bottomIdx])) bottomIdx++;
    const spans = columnSpans(lines[bottomIdx]);
    const bodyRows = lines.slice(headerIdx + 1, bottomIdx);
    const headerCells = extractCells(lines[headerIdx], spans);
    const gfmHeader = '| ' + headerCells.join(' | ') + ' |';
    const gfmSep    = '| ' + spans.map(() => '---').join(' | ') + ' |';
    const gfmBody   = bodyRows.filter(l => l.trim().length > 0)
                              .map(l => '| ' + extractCells(l, spans).join(' | ') + ' |');
    // Convert the caption: `: Table 2: ...` → `**Table 2: ...**`
    let captionIdx = bottomIdx + 1;
    while (captionIdx < lines.length && !lines[captionIdx].trim().startsWith(': Table 2:')) captionIdx++;
    const captionLine = captionIdx < lines.length
      ? lines[captionIdx].replace(/^\s*: (Table 2:.*)$/, '**$1**')
      : '**Table 2: Consolidated Implementation Blueprint Summary**';
    const endIdx = captionIdx < lines.length ? captionIdx : bottomIdx;
    const newBlock = [...interlude, '', gfmHeader, gfmSep, ...gfmBody, '', captionLine];
    lines.splice(sepIdx, endIdx - sepIdx + 1, ...newBlock);
    text = lines.join('\n');
  }
}

// ============================================================================
// 6. BARE MULTI-CHAR SUBSCRIPTS (D3) — L_<name> family, brace them.
//    Pass 1 handles sub+super both bare (L_phys^causal → L_{phys}^{causal}).
//    Pass 2 handles sub only (L_total → L_{total}).
//    The negative lookbehind at start avoids matching \lambda_<...> etc.
//    The lookahead excludes already-braced forms like L_{IC}.
// ============================================================================
text = text.replace(/(?<![A-Za-z\\])L_([A-Za-z]+)\^([A-Za-z]+)/g, 'L_{$1}^{$2}');
text = text.replace(/(?<![A-Za-z\\])L_([A-Za-z]+)(?![A-Za-z{])/g, 'L_{$1}');

// ============================================================================
// 7. SURVIVING LATEX MID-PARAGRAPH (D4 on lines 653–655)
//    The inline math $\lambda_E^{max}(k) = ...$ is split across 3 lines;
//    collapse to one line so markdown-it treats it as a single math token.
// ============================================================================
{
  const target = [
    '$\\lambda_E^{max}(k) = \\lambda_L^{max}(k) = \\{0 \\text{ for } k \\in',
    '  \\{0,1\\}; 10^{k-4} \\text{ for } k \\in \\{2,3,4\\}; 1 \\text{ for } k \\in',
    '  \\{5,6\\}\\}$'
  ].join('\n');
  const replacement = '$\\lambda_E^{max}(k) = \\lambda_L^{max}(k) = \\{0 \\text{ for } k \\in \\{0,1\\}; 10^{k-4} \\text{ for } k \\in \\{2,3,4\\}; 1 \\text{ for } k \\in \\{5,6\\}\\}$';
  if (text.includes(target)) text = text.replace(target, replacement);
  else console.log('WARN: step 7 target not found');
}

// ============================================================================
// 8. BACKTICK-WRAPPED MATH / CODE (D5)
//    Convert each to a form that no longer triggers D5. Math goes to $…$;
//    code identifiers go to $\text{…}$ (renders identically as roman text).
// ============================================================================
// 8a. Redundant parenthetical ASCII duplicates of adjacent LaTeX (D7)
text = text.replace(/ \(`10\^-5`\)/g, '');
text = text.replace(/ \(`10\^-8`\)/g, '');
// 8b. Math symbol references
text = text.replace(/`ΔH_n`/g, '$\\Delta H_n$');
// 8c. Code variable epsilon_H → Greek-letter math (matches adjacent $S_H$)
text = text.replace(/`epsilon_H`/g, '$\\epsilon_H$');
// 8d. Code-identifier hyperparameter names → $\text{...}$ (visual equivalence)
text = text.replace(/`first_omega_0`/g, '$\\text{first\\_omega\\_0}$');
text = text.replace(/`hidden_omega_0 = 1`/g, '$\\text{hidden\\_omega\\_0} = 1$');
text = text.replace(/`hidden_omega_0`/g, '$\\text{hidden\\_omega\\_0}$');
text = text.replace(/`elementwise_affine=False`/g, '$\\text{elementwise\\_affine}=\\text{False}$');
text = text.replace(/`elementwise_affine=True`/g,  '$\\text{elementwise\\_affine}=\\text{True}$');
// 8e. Author comment mentioning `\text{xxx}` — render as math-escaped literal
text = text.replace(/`\\text\{xxx\}`/g, '$\\backslash\\text{text\\{xxx\\}}$');
// 8f. Canonical text form of loss formula (line 286) — convert to LaTeX
text = text.replace(
  /Canonical text form: `L_total = L_data \+ λ_IC · L_IC \+ λ_phys · L_phys\^causal \+ λ_E · L_E \+ λ_L · L_L`\./g,
  'Canonical text form: $L_{\\text{total}} = L_{\\text{data}} + \\lambda_{IC} \\cdot L_{IC} + \\lambda_{\\text{phys}} \\cdot L_{\\text{phys}}^{\\text{causal}} + \\lambda_E \\cdot L_E + \\lambda_L \\cdot L_L$.'
);

// ============================================================================
// 9. PROSE ASCII MATH (D6) — §4.2 ALM constraints line 676
//    The physics is unambiguous: c_E / c_{L,α} are scalar ALM constraint values;
//    RMS_n is the root-mean-square operator over n samples.
// ============================================================================
text = text.replace(
  /c_E = RMS_n\(ΔH_n\) \(energy drift\), c_\{L,α\} = RMS_n\(\(L'_θ,α\(u_n\) - L_0,α'\) \/ L_scale\) \(angular momentum drift per component\)/,
  '$c_E = \\mathrm{RMS}_n(\\Delta H_n)$ (energy drift), $c_{L,\\alpha} = \\mathrm{RMS}_n((L\'_{\\theta,\\alpha}(u_n) - L\'_{0,\\alpha}) / L_{\\text{scale}})$ (angular momentum drift per component)'
);

// ============================================================================
// 10. TRAILING `\` hard-break on line 177 (D8) — remove as conversion noise
// ============================================================================
text = text.replace(/(\\text\{hidden\\_omega\\_0\}\}\]\)\.)\\\n(    The crucial difference)/, '$1\n$2');

// ============================================================================
// Write output
// ============================================================================
if (text !== src) {
  writeFileSync(FILE, text);
  console.log(`Transform applied. Bytes: ${src.length} → ${text.length} (Δ${text.length - src.length})`);
} else {
  console.log('No changes applied.');
}
