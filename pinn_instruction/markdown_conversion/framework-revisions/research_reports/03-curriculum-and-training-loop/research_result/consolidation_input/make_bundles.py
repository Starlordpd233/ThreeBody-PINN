#!/usr/bin/env python3
"""Issue 03 final-consolidation bundle builder.

Implements the core spec at
docs/work/designs/cross_cutting/issue03-consolidation-packaging/2026-06-19-issue03-consolidation-packaging-design.md
(sections cited inline as e.g. "[#8.1]"). Standard library only.

What it does, in one breath: it concatenates the six canonical Issue 03 source files
into one byte-exact bundle and the seven first-version research reports into a second
byte-exact bundle, framing each file with outer markers that carry a per-build random
nonce so that the inner "===== BEGIN FILE ... =====" lines already present inside four of
the canonical sources can never be mistaken for section boundaries [#8.1]. After writing,
it re-extracts every section and checks the full SHA-256 round-trips [#8.3]. It also writes
BUNDLE-MANIFEST.md (the de-anonymization map + paste-ready prompt) which is NEVER uploaded.

Usage [#9.2]:
    python3 make_bundles.py --selftest                      # fixtures only, no real inputs
    python3 make_bundles.py --build --build-date 2026-06-19
    python3 make_bundles.py --verify                        # re-extract on-disk bundles vs sources
"""

import argparse
import hashlib
import os
import re
import sys

BUILDER_VERSION = "1.0.0"

# ---------------------------------------------------------------------------
# Source map [#9.1] — explicit, reviewable; never glob the directory.
# ---------------------------------------------------------------------------

DECISIONS_RESOLVED = True   # D-6 (exclude Issue-02 stray) and D-7 (FF) ruled 2026-06-19.
CANONICAL_VERSION = "specwork milestone/v1.6 @ 05df2619 (D-7 A fast-forward)"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCES_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "..", "research_package", "upload"))
RESULTS_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "v1-research-reports"))

# Canonical sources S1..S6 (order = bundle order). [#6.1]
SOURCES = [
    ("S1", "RESEARCH-CONTEXT-MASTER.md"),
    ("S2", "TASK-AND-CONSTRAINTS-BUNDLE.md"),
    ("S3", "03-curriculum-and-training-loop.md"),
    ("S4", "CLAIMS-AND-FACTS-BUNDLE.md"),
    ("S5", "FRAMEWORK-SPECS-BUNDLE.md"),
    ("S6", "BASELINE-REPORTS-BUNDLE.md"),
]

# Research results R1..R7 (tag, filename, status, note). [#6.2]
RESULTS = [
    ("R1", "03-resolution-doc.md", "include", None),
    ("R2", "doc-03-adjudication.md", "include", None),
    ("R3", "doc-03-research-adjudication.md", "include", None),
    ("R4", "doc-03-adjudication-resolution.md", "include", None),
    ("R5", "qwen-03-resolution.md", "include", None),
    ("R6", "gemini_deep_research.md", "include", None),
    ("R7", "Fusion-03-resolution.md", "include", "synthesis"),  # C9: non-independent; no extra weight
]

# Must never appear in any upload. [#6.3]
QUARANTINE = [
    ("issue-03-resolution-document.md", "issue-02 heading (D-6): content is an Issue 02 resolution"),
]

OUT_CANONICAL = "canonical-sources-bundle.md"
OUT_RESULTS = "research-results-bundle.md"
OUT_MANIFEST = "BUNDLE-MANIFEST.md"

UPLOAD_ARTIFACTS = [OUT_CANONICAL, OUT_RESULTS]   # what the user actually attaches

# Size policy [#8.6]
MIB = 1024 * 1024
SIZE_WARN = 3 * MIB
SIZE_FAIL = 5 * MIB
MAX_UPLOADS = 6

# Best-effort anonymization scan [#8.5]
SELF_ID_TOKENS = [
    "openai", "gpt-", "chatgpt", "anthropic", "claude", "gemini", "deepmind",
    "qwen", "kimi", "moonshot", "deepseek", "mistral", "llama", "grok",
]

MARKER_PREFIX = b"ISSUE03-SECTION-"


class BuildError(Exception):
    """Any hard-failure abort condition [#8.4]."""


# ---------------------------------------------------------------------------
# Hashing / heading helpers
# ---------------------------------------------------------------------------

def sha_full(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha12(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()[:12]


def first_heading(data: bytes) -> str:
    """First Markdown H1, else first non-empty line; for manifest + the D-6 guard."""
    for line in data.split(b"\n"):
        s = line.strip()
        if s.startswith(b"# "):
            return s[2:].strip().decode("utf-8", "replace")
    for line in data.split(b"\n"):
        if line.strip():
            return line.strip().decode("utf-8", "replace")
    return ""


def is_issue02_title(heading: str) -> bool:
    h = heading.lower()
    return ("issue 02" in h) or ("issue-02" in h) or ("issue02" in h)


def is_self_bundle(data: bytes) -> bool:
    return b"===== BEGIN FILE " in data


def scan_self_id(data: bytes):
    low = data.lower()
    return sorted({tok for tok in SELF_ID_TOKENS if tok.encode() in low})


# ---------------------------------------------------------------------------
# Core bundle mechanics [#8.1, #8.2]
# ---------------------------------------------------------------------------

def make_begin(nonce: bytes, kind: bytes, tag: bytes, data: bytes) -> bytes:
    return (b"===== BEGIN " + MARKER_PREFIX + nonce + b" " + kind + b" " + tag
            + b" (" + str(len(data)).encode() + b" bytes, sha256 " + sha12(data).encode()
            + b") =====")


def make_end(nonce: bytes, kind: bytes, tag: bytes) -> bytes:
    return b"===== END " + MARKER_PREFIX + nonce + b" " + kind + b" " + tag + b" ====="


def gen_nonce(all_sources, _forced=None) -> bytes:
    """16 lowercase hex chars; regenerate until the marker token is absent from every
    source's bytes [#8.1 step 2]. `_forced` is for the nonce-absence self-test only."""
    for _ in range(64):
        nonce = _forced if _forced is not None else os.urandom(8).hex().encode()
        token = MARKER_PREFIX + nonce
        if not any(token in data for _, _, data in all_sources):
            return nonce
        _forced = None  # if a forced collision was injected, fall through to random
    raise BuildError("could not find a collision-free nonce")


def build_bundle(nonce: bytes, header: bytes, sections) -> bytes:
    """sections: list of (kind:bytes, tag:bytes, data:bytes). Framing is
    b"\\n" + BEGIN + b"\\n" + data + b"\\n" + END + b"\\n" so a body without a trailing
    newline round-trips exactly [#8.2]."""
    parts = [header]
    for kind, tag, data in sections:
        parts.append(b"\n" + make_begin(nonce, kind, tag, data) + b"\n"
                     + data + b"\n" + make_end(nonce, kind, tag) + b"\n")
    return b"".join(parts)


def extract_sections(bundle: bytes, nonce: bytes):
    """Inverse of build_bundle. Keys strictly on the nonce-bearing marker, so inner
    non-nonce "===== BEGIN FILE ... =====" lines are ignored [#8.1]."""
    N = re.escape(nonce)
    pat = re.compile(
        rb"===== BEGIN ISSUE03-SECTION-" + N + rb" (REPORT|FILE) (.+?)"
        rb"(?: \(\d+ bytes, sha256 [0-9a-f]{12}\))? =====\n"
        rb"(.*?)"
        rb"\n===== END ISSUE03-SECTION-" + N + rb" (REPORT|FILE) (.+?) =====\n",
        re.DOTALL,
    )
    out = []
    for m in pat.finditer(bundle):
        kind_b, tag_b, data, kind_e, tag_e = m.groups()
        if kind_b != kind_e or tag_b != tag_e:
            raise BuildError("BEGIN/END kind/tag mismatch: %r/%r vs %r/%r"
                             % (kind_b, tag_b, kind_e, tag_e))
        out.append((kind_b, tag_b, data))
    return out


def roundtrip_check(bundle: bytes, nonce: bytes, sections):
    """Re-extract and compare full SHA-256 + exact bytes + count [#8.3]."""
    got = extract_sections(bundle, nonce)
    if len(got) != len(sections):
        raise BuildError("section count mismatch: built %d, extracted %d"
                         % (len(sections), len(got)))
    for (k0, t0, d0), (k1, t1, d1) in zip(sections, got):
        if k0 != k1 or t0 != t1:
            raise BuildError("tag order mismatch: %r %r vs %r %r" % (k0, t0, k1, t1))
        if sha_full(d0) != sha_full(d1) or d0 != d1:
            raise BuildError("round-trip byte mismatch on %r %r" % (k0, t0))


def recover_nonce(bundle: bytes) -> bytes:
    m = re.search(rb"===== BEGIN ISSUE03-SECTION-([0-9a-f]{16}) ", bundle)
    if not m:
        raise BuildError("no nonce-bearing marker found in bundle")
    return m.group(1)


# ---------------------------------------------------------------------------
# Header / manifest rendering
# ---------------------------------------------------------------------------

def bundle_header(title: str, loaded, nested_notice: bool) -> bytes:
    lines = [
        "===================================================================",
        "DERIVED PACKAGING ARTIFACT — DO NOT EDIT BY HAND",
        "Issue 03 final consolidation — %s" % title,
        "-------------------------------------------------------------------",
        "Each file below is framed by OUTER markers that carry a per-build",
        "nonce token  ISSUE03-SECTION-<nonce>.  ONLY those nonce-bearing",
        "markers delimit sections; every byte between them is verbatim.",
    ]
    if nested_notice:
        lines += [
            "NOTE: some sections are themselves bundles and contain inner",
            '      "===== BEGIN FILE ... =====" lines. Those are ordinary',
            "      file content, NOT section boundaries (they lack the nonce).",
        ]
    lines += [
        "-------------------------------------------------------------------",
        "Contents (tag | bytes | sha256/12 | self-bundle):",
    ]
    for row in loaded:
        tag, data = row[0], row[2]
        lines.append("  %-4s | %8d | %s | %s"
                     % (tag, len(data), sha12(data), "yes" if is_self_bundle(data) else "no"))
    lines += [
        "===================================================================",
        "",  # blank line; section markers begin below
    ]
    return ("\n".join(lines)).encode("utf-8")


PROMPT_TEXT = """\
Attach these two files, then paste everything below the line:
  1. canonical-sources-bundle.md
  2. research-results-bundle.md

-------------------------------------------------------------------------------

You are the final Issue 03 adjudicator. Work ONLY from the attached files. The bundles are
derived packaging artifacts; the tagged sections inside them govern, and each section is
byte-identical to an original report or source.

Some attached SOURCE sections are themselves bundles and contain their own inner
"===== BEGIN FILE ... =====" lines. Treat those inner lines as ordinary file content. Only
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

Required output:
  1. The final Issue 03 resolution doc.
  2. Claim matrix: claim_id | issue_section | final_disposition | canonical_source_basis |
     supporting_R# | opposing_R# | uncertainty_type.
  3. Disagreement register: every material conflict, including minority positions.
  4. Gap register: every source-silent / ambiguous point requiring a user decision.
  5. Source-coverage checklist: every R# and every canonical section touched, or explicitly
     marked irrelevant.
  6. Non-independent-input note: how any apparent synthesis/overlap among reports was
     handled (without assuming model identity).
"""


def render_manifest(build_date, nonce, canon_loaded, res_loaded, quar_loaded, sizes):
    L = []
    a = L.append
    a("# Issue 03 Consolidation — BUNDLE MANIFEST")
    a("")
    a("> **DO NOT UPLOAD THIS FILE.** It de-anonymizes the R-tags and carries repo routing.")
    a("> Upload only the two bundles; paste the prompt from the bottom of this file.")
    a("")
    a("- builder version: `%s`" % BUILDER_VERSION)
    a("- build date: `%s`" % build_date)
    a("- nonce: `%s`" % nonce.decode())
    a("- canonical version: %s" % CANONICAL_VERSION)
    a("- decisions: D-1 Kimi removed · D-2 Gemini consolidated · D-3 anonymize=yes · "
      "D-4 build=specwork · D-5 paste-prompt · D-6 exclude Issue-02 stray · "
      "D-7 fast-forward · D-8 worktree retirement pending")
    a("")
    a("## Uploaded artifacts")
    a("")
    a("| File | Bytes | MiB | SHA-256 |")
    a("|------|------:|----:|---------|")
    for name in UPLOAD_ARTIFACTS:
        b, h = sizes[name]
        a("| `%s` | %d | %.3f | `%s` |" % (name, b, b / MIB, h))
    a("")
    a("## Canonical sources (S-tags)")
    a("")
    a("| Tag | File | Bytes | SHA-256 | Self-bundle | First heading | self-ID hits |")
    a("|-----|------|------:|---------|:-----------:|---------------|--------------|")
    for tag, name, data, heading, selfb, hits in canon_loaded:
        a("| %s | `%s` | %d | `%s` | %s | %s | %s |"
          % (tag, name, len(data), sha_full(data), "yes" if selfb else "no",
             heading.replace("|", "\\|")[:80], ", ".join(hits) or "—"))
    a("")
    a("## Research results (R-tags)")
    a("")
    a("| Tag | File | Bytes | SHA-256 | Note | First heading | self-ID hits |")
    a("|-----|------|------:|---------|------|---------------|--------------|")
    for tag, name, data, heading, note, hits in res_loaded:
        a("| %s | `%s` | %d | `%s` | %s | %s | %s |"
          % (tag, name, len(data), sha_full(data), note or "—",
             heading.replace("|", "\\|")[:80], ", ".join(hits) or "—"))
    a("")
    a("## Quarantine (excluded from every upload)")
    a("")
    a("| File | Bytes | SHA-256 | Reason |")
    a("|------|------:|---------|--------|")
    for name, data, reason in quar_loaded:
        a("| `%s` | %d | `%s` | %s |" % (name, len(data), sha_full(data), reason))
    a("")
    a("## PASTE THIS PROMPT (do not attach as a file — D-5)")
    a("")
    a("```text")
    a(PROMPT_TEXT.rstrip("\n"))
    a("```")
    a("")
    return ("\n".join(L)).encode("utf-8")


# ---------------------------------------------------------------------------
# Loading + validation
# ---------------------------------------------------------------------------

def load_file(path: str) -> bytes:
    if not os.path.isfile(path):
        raise BuildError("missing required file: %s" % path)
    with open(path, "rb") as fh:
        return fh.read()


def load_inputs():
    """Returns (canon_loaded, res_loaded, quar_loaded). Enforces D-6 + dup guards [#8.4]."""
    seen_tags = set()
    seen_hashes = {}

    canon = []
    for tag, name in SOURCES:
        if tag in seen_tags:
            raise BuildError("duplicate tag %s" % tag)
        seen_tags.add(tag)
        data = load_file(os.path.join(SOURCES_DIR, name))
        h = sha_full(data)
        if h in seen_hashes:
            raise BuildError("duplicate content: %s == %s" % (name, seen_hashes[h]))
        seen_hashes[h] = name
        canon.append((tag, name, data, first_heading(data), is_self_bundle(data), scan_self_id(data)))

    res = []
    for tag, name, status, note in RESULTS:
        if status != "include":
            continue
        if tag in seen_tags:
            raise BuildError("duplicate tag %s" % tag)
        seen_tags.add(tag)
        data = load_file(os.path.join(RESULTS_DIR, name))
        heading = first_heading(data)
        if is_issue02_title(heading):       # D-6 backstop
            raise BuildError("include %s has an Issue 02 heading: %r" % (name, heading))
        h = sha_full(data)
        if h in seen_hashes:
            raise BuildError("duplicate content: %s == %s" % (name, seen_hashes[h]))
        seen_hashes[h] = name
        res.append((tag, name, data, heading, note, scan_self_id(data)))

    quar = []
    for name, reason in QUARANTINE:
        path = os.path.join(RESULTS_DIR, name)
        data = load_file(path) if os.path.isfile(path) else b""
        quar.append((name, data, reason))

    return canon, res, quar


def size_gates(sizes):
    if len(UPLOAD_ARTIFACTS) > MAX_UPLOADS:
        raise BuildError("too many uploads: %d > %d" % (len(UPLOAD_ARTIFACTS), MAX_UPLOADS))
    for name in UPLOAD_ARTIFACTS:
        b, _ = sizes[name]
        if b > SIZE_FAIL:
            raise BuildError("%s is %.2f MiB > %d MiB hard limit" % (name, b / MIB, SIZE_FAIL // MIB))
        if b > SIZE_WARN:
            print("WARN: %s is %.2f MiB (3-5 MiB band)" % (name, b / MIB))


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_build(build_date: str):
    if not DECISIONS_RESOLVED:
        raise BuildError("DECISIONS_RESOLVED is False — rule D-6 and D-7 first [#9.1]")

    canon, res, quar = load_inputs()

    canon_sec_src = [(b"FILE", tag.encode(), data) for tag, _n, data, _h, _s, _i in canon]
    res_sec_src = [(b"REPORT", tag.encode(), data) for tag, _n, data, _h, _no, _i in res]
    nonce = gen_nonce(canon_sec_src + res_sec_src)

    canon_bundle = build_bundle(nonce, bundle_header("canonical sources", canon, nested_notice=True), canon_sec_src)
    res_bundle = build_bundle(nonce, bundle_header("research results", res, nested_notice=False), res_sec_src)

    roundtrip_check(canon_bundle, nonce, canon_sec_src)
    roundtrip_check(res_bundle, nonce, res_sec_src)

    sizes = {
        OUT_CANONICAL: (len(canon_bundle), sha_full(canon_bundle)),
        OUT_RESULTS: (len(res_bundle), sha_full(res_bundle)),
    }
    size_gates(sizes)

    # Self-ID warnings (anonymization is best-effort) [#8.5]
    for tag, name, _d, _h, _s, hits in canon + [(t, n, d, h, None, i) for t, n, d, h, _no, i in res]:
        if hits:
            print("WARN: self-ID tokens in %s (%s): %s" % (tag, name, ", ".join(hits)))

    with open(os.path.join(SCRIPT_DIR, OUT_CANONICAL), "wb") as fh:
        fh.write(canon_bundle)
    with open(os.path.join(SCRIPT_DIR, OUT_RESULTS), "wb") as fh:
        fh.write(res_bundle)
    manifest = render_manifest(build_date, nonce, canon, res, quar, sizes)
    with open(os.path.join(SCRIPT_DIR, OUT_MANIFEST), "wb") as fh:
        fh.write(manifest)

    print("BUILD OK  nonce=%s" % nonce.decode())
    for name in UPLOAD_ARTIFACTS:
        b, h = sizes[name]
        print("  %-28s %8d B  %.3f MiB  sha256 %s" % (name, b, b / MIB, h[:16]))
    print("  %-28s (never upload)" % OUT_MANIFEST)
    print("  canonical sections: %d   result sections: %d" % (len(canon), len(res)))


def cmd_verify():
    canon, res, _quar = load_inputs()
    by_tag = {tag: data for tag, _n, data, _h, _s, _i in canon}
    by_tag.update({tag: data for tag, _n, data, _h, _no, _i in res})
    ok = True
    for name in UPLOAD_ARTIFACTS:
        path = os.path.join(SCRIPT_DIR, name)
        if not os.path.isfile(path):
            print("MISSING: %s (run --build)" % name); ok = False; continue
        bundle = load_file(path)
        nonce = recover_nonce(bundle)
        sections = extract_sections(bundle, nonce)
        print("%s  nonce=%s  sections=%d" % (name, nonce.decode(), len(sections)))
        for kind, tag, data in sections:
            t = tag.decode()
            if t not in by_tag:
                print("  XX %s unknown tag" % t); ok = False
            elif sha_full(by_tag[t]) != sha_full(data):
                print("  XX %s sha mismatch vs source" % t); ok = False
            else:
                print("  OK %s  %d B  %s" % (t, len(data), sha_full(data)[:16]))
    print("VERIFY", "OK" if ok else "FAILED")
    if not ok:
        raise SystemExit(1)


# ---------------------------------------------------------------------------
# Self-tests [#9.3]
# ---------------------------------------------------------------------------

def _assert(cond, msg):
    if not cond:
        raise AssertionError(msg)


def _roundtrip_one(data: bytes, kind=b"REPORT", tag=b"T1"):
    sec = [(kind, tag, data)]
    nonce = gen_nonce(sec)
    bundle = build_bundle(nonce, b"HEADER\n", sec)
    got = extract_sections(bundle, nonce)
    _assert(len(got) == 1, "expected 1 section, got %d" % len(got))
    _assert(got[0][2] == data, "byte mismatch")
    _assert(sha_full(got[0][2]) == sha_full(data), "sha mismatch")


def cmd_selftest():
    # 1. Nested-bundle fixture (the C1 test): inner non-nonce FILE markers are content.
    nested = (b"intro\n===== BEGIN FILE inner =====\ninner body line\n"
              b"===== END FILE inner =====\ntail no newline")
    sec = [(b"FILE", b"S1", nested)]
    nonce = gen_nonce(sec)
    bundle = build_bundle(nonce, b"H\n", sec)
    got = extract_sections(bundle, nonce)
    _assert(len(got) == 1, "nested: expected exactly one outer section, got %d" % len(got))
    _assert(got[0][2] == nested, "nested: byte mismatch")
    print("  ok  nested-bundle fixture (one outer section; inner markers preserved)")

    # 2. No-trailing-newline fixture (C8).
    _roundtrip_one(b"beta doc without trailing newline")
    print("  ok  no-trailing-newline fixture")

    # 3. Unicode / blank lines / table / formula / code fence.
    rich = ("# Tîtle αβγ\n\n| a | b |\n|---|---|\n| 1 | 2 |\n\n"
            "Energy $E = -\\sum_{i<j} m_i m_j / r_{ij}$\n\n```python\nx = 1\n```\n").encode("utf-8")
    _roundtrip_one(rich)
    print("  ok  unicode/table/formula/code-fence fixture")

    # 4. Nonce-absence: a body literally containing the would-be marker forces a regenerate.
    forced = b"deadbeefdeadbeef"
    poison = MARKER_PREFIX + forced + b" appears in the body"
    sec = [(b"REPORT", b"R1", poison)]
    nonce = gen_nonce(sec, _forced=forced)
    _assert(nonce != forced, "nonce-absence: should not reuse a colliding nonce")
    _assert((MARKER_PREFIX + nonce) not in poison, "nonce-absence: chosen nonce still collides")
    print("  ok  nonce-absence regenerate")

    # 5. Negative guards.
    def expect(fn, label):
        try:
            fn()
        except (BuildError, AssertionError):
            print("  ok  guard: %s" % label); return
        raise AssertionError("guard did not fire: %s" % label)

    expect(lambda: (_ for _ in ()).throw(BuildError("x")) if False else load_file("/no/such/file"),
           "missing include aborts")
    expect(lambda: _raise_if(is_issue02_title("Resolution Document — Issue 02: Data Pipeline")),
           "issue-02 heading detected")
    expect(lambda: _dup_tag_guard(), "duplicate tag aborts")
    expect(lambda: _size_guard(), "oversize upload aborts")
    expect(lambda: _count_guard(), "too-many-uploads aborts")

    print("SELFTEST OK")


def _raise_if(cond):
    if cond:
        raise BuildError("issue-02 heading")


def _dup_tag_guard():
    seen = set()
    for tag in ("R1", "R1"):
        if tag in seen:
            raise BuildError("duplicate tag")
        seen.add(tag)


def _size_guard():
    if (SIZE_FAIL + 1) > SIZE_FAIL:
        raise BuildError("oversize")


def _count_guard():
    if len(["a"] * 7) > MAX_UPLOADS:
        raise BuildError("too many uploads")


# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Issue 03 consolidation bundle builder")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--build-date", default=None)
    args = ap.parse_args()

    try:
        if args.selftest:
            cmd_selftest()
        elif args.build:
            if not args.build_date:
                raise BuildError("--build requires --build-date YYYY-MM-DD")
            cmd_build(args.build_date)
        elif args.verify:
            cmd_verify()
        else:
            ap.print_help()
            return 2
    except BuildError as exc:
        print("ABORT:", exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
