"""Phase 60 (D-11): owner ruling loaders for checkpoint ④ and GAP-60-09.

The owner's answers enter the ladder from committed files and from nothing else. A
ruling file is Markdown with exactly two fenced blocks that matter:

* one block whose info string is exactly ``phase60-ruling``: the machine block. It holds
  ``key: value`` lines from a closed set of keys. For checkpoint 4 the keys are
  ``ruling: checkpoint-4``, ``answer: continue`` or ``answer: go-to-verdict``, and, for
  ``continue`` only, ``approved_first_omega_0`` as a plain positive decimal such as
  ``120`` or ``37.5``. For GAP-60-09 the keys are ``ruling: gap-60-09`` and
  ``reading: no_rescue`` or ``reading: rescue``.
* one block whose info string is exactly ``owner-quote``: the owner's words, kept as
  opaque text. The loader finds its fences so that nothing inside it can be mistaken for
  a block, and then ignores it. It is never parsed, evaluated, executed, formatted into a
  path or a command, or returned.

Everything else in the file (front matter, headings, prose) is ignored. A fence is a line
of three or more backticks or tildes, indented by at most three spaces; a block closes at
the first fence of the same character that is at least as long as the one that opened
it, so a quote fenced longer than anything inside it cannot be cut short by its content.
A block that never closes, a missing or repeated block, an unknown or repeated key, or a
value that is not a plain positive decimal is a ``RulingError``.

A loaded ruling must be tracked and clean in git (an uncommitted file is refused), and
carries the SHA-256 of the file's bytes, which every continue-path record cites. The
loaders read only the two fixed paths below, or a path a test supplies.
"""

from __future__ import annotations

import hashlib
import math
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

from pinn.verification.learnability_arms import PHASE_REL

__all__ = [
    "KIND_CHECKPOINT4",
    "KIND_GAP6009",
    "RULING4_REL",
    "RULING_GAP6009_REL",
    "Checkpoint4Ruling",
    "Gap6009Ruling",
    "RulingError",
    "RulingMissing",
    "RulingUncommitted",
    "load_checkpoint4_ruling",
    "load_gap6009_ruling",
    "parse_machine_block",
    "ruling_grid_facts",
    "tracked_and_clean",
]

_REPO_ROOT = Path(__file__).resolve().parents[2]

RULING4_REL = PHASE_REL / "60-CHECKPOINT-4-RULING.md"
RULING_GAP6009_REL = PHASE_REL / "60-GAP-60-09-RULING.md"
KIND_CHECKPOINT4 = "checkpoint-4"
KIND_GAP6009 = "gap-60-09"

_MACHINE_INFO = "phase60-ruling"
_QUOTE_INFO = "owner-quote"
_ANSWERS = ("continue", "go-to-verdict")
_READINGS = ("no_rescue", "rescue")
_KEYS = {
    KIND_CHECKPOINT4: frozenset({"ruling", "answer", "approved_first_omega_0"}),
    KIND_GAP6009: frozenset({"ruling", "reading"}),
}
# Markdown line endings only: str.splitlines would also split on U+2028 and others.
_LINE_BREAK = re.compile(r"\r\n|\n|\r")
_FENCE_OPEN = re.compile(r"^ {0,3}(?P<fence>`{3,}|~{3,})[ \t]*(?P<info>.*?)[ \t]*$")
_FENCE_CLOSE = re.compile(r"^ {0,3}(?P<fence>`{3,}|~{3,})[ \t]*$")
_KEY_VALUE = re.compile(r"^(?P<key>[A-Za-z0-9_]+):[ \t]+(?P<value>\S(?:.*\S)?)[ \t]*$")
_PLAIN_DECIMAL = re.compile(r"[0-9]+(?:\.[0-9]+)?")


class RulingError(ValueError):
    """The ruling file is absent, uncommitted or not in the strict format. Nothing is taken from it."""


class RulingMissing(RulingError):
    """There is no ruling file yet: the owner has not answered, or the answer is not written."""


class RulingUncommitted(RulingError):
    """The ruling file exists but is not tracked and clean in git."""

    def __init__(self, relative):
        super().__init__(f"uncommitted {relative}")
        self.relative = relative


@dataclass(frozen=True)
class Checkpoint4Ruling:
    """The owner's checkpoint 4 answer. ``approved_first_omega_0`` is set only for ``continue``."""

    answer: str
    approved_first_omega_0: float | None
    sha256: str
    path: str


@dataclass(frozen=True)
class Gap6009Ruling:
    """The owner's reading of a G2 confirmation that ended below Tier 1."""

    reading: str
    sha256: str
    path: str


# ---------------------------------------------------------------------------
# The strict block format.
# ---------------------------------------------------------------------------

def _fenced_blocks(text):
    """``[(info string, content lines)]`` for every fenced block of ``text``, Markdown-style."""
    lines = _LINE_BREAK.split(text)
    blocks = []
    index = 0
    while index < len(lines):
        opening = _FENCE_OPEN.match(lines[index])
        if opening is None or (opening["fence"][0] == "`" and "`" in opening["info"]):
            index += 1
            continue
        fence, info = opening["fence"], opening["info"]
        content = []
        index += 1
        while True:
            if index >= len(lines):
                raise RulingError("a fenced block is never closed")
            closing = _FENCE_CLOSE.match(lines[index])
            if (
                closing is not None
                and closing["fence"][0] == fence[0]
                and len(closing["fence"]) >= len(fence)
            ):
                break
            content.append(lines[index])
            index += 1
        blocks.append((info, content))
        index += 1
    return blocks


def _plain_positive(raw):
    if _PLAIN_DECIMAL.fullmatch(raw) is None:
        raise RulingError("approved_first_omega_0 must be a plain decimal such as 120 or 37.5")
    value = float(raw)
    if not math.isfinite(value) or value <= 0.0:
        raise RulingError("approved_first_omega_0 must be finite and positive")
    return value


def parse_machine_block(text, *, kind):
    """The validated fields of the one ``phase60-ruling`` block in ``text``.

    ``kind`` is ``checkpoint-4`` (returns ``answer`` and ``approved_first_omega_0``, the
    latter ``None`` unless the answer is ``continue``) or ``gap-60-09`` (returns
    ``reading``). The ``owner-quote`` block is located but never read.
    """
    if kind not in _KEYS:
        raise ValueError(f"kind must be one of {sorted(_KEYS)}; got {kind!r}")
    blocks = _fenced_blocks(text)
    machine = [content for info, content in blocks if info == _MACHINE_INFO]
    quote_count = sum(1 for info, _content in blocks if info == _QUOTE_INFO)
    if len(machine) != 1:
        raise RulingError(f"exactly one {_MACHINE_INFO} block is required; found {len(machine)}")
    if quote_count != 1:
        raise RulingError(f"exactly one {_QUOTE_INFO} block is required; found {quote_count}")
    pairs = {}
    for number, raw in enumerate(machine[0], start=1):
        if not raw.strip():
            continue
        match = _KEY_VALUE.match(raw)
        if match is None:
            raise RulingError(f"line {number} of the machine block is not 'key: value'")
        key, value = match["key"], match["value"]
        if key not in _KEYS[kind]:
            raise RulingError(f"the machine block holds an unknown key {key!r}")
        if key in pairs:
            raise RulingError(f"the machine block repeats the key {key!r}")
        pairs[key] = value
    if pairs.get("ruling") != kind:
        raise RulingError(f"the machine block must say 'ruling: {kind}'")
    if kind == KIND_GAP6009:
        reading = pairs.get("reading")
        if reading not in _READINGS:
            raise RulingError(f"reading must be one of {_READINGS}")
        return {"reading": reading}
    answer = pairs.get("answer")
    if answer not in _ANSWERS:
        raise RulingError(f"answer must be one of {_ANSWERS}")
    if answer == "continue":
        if "approved_first_omega_0" not in pairs:
            raise RulingError("a continue answer must name approved_first_omega_0")
        return {
            "answer": answer,
            "approved_first_omega_0": _plain_positive(pairs["approved_first_omega_0"]),
        }
    if "approved_first_omega_0" in pairs:
        raise RulingError("a go-to-verdict answer must not name approved_first_omega_0")
    return {"answer": answer, "approved_first_omega_0": None}


# ---------------------------------------------------------------------------
# The committed file.
# ---------------------------------------------------------------------------

def tracked_and_clean(repo_root, relative):
    """True when ``relative`` is tracked in git and has no change, staged or not."""

    def git(*args):
        return subprocess.run(
            ["git", *args], cwd=str(repo_root), capture_output=True, text=True, check=False
        )

    if git("ls-files", "--error-unmatch", "--", relative).returncode != 0:
        return False
    status = git("status", "--porcelain", "--", relative)
    return status.returncode == 0 and status.stdout.strip() == ""


def _read_ruling(default_rel, repo_root, path, require_committed):
    """``(text, SHA-256 of the file's bytes, repo-relative path)`` of a ruling file."""
    root = (_REPO_ROOT if repo_root is None else Path(repo_root)).resolve()
    target = default_rel if path is None else Path(path)
    candidate = target if target.is_absolute() else root / target
    if candidate.is_symlink():
        raise RulingError(f"{candidate.name} is a symbolic link; a ruling must be a regular file")
    if not candidate.exists():
        raise RulingMissing(f"there is no ruling file {candidate.name}")
    resolved = candidate.resolve()
    try:
        relative = resolved.relative_to(root).as_posix()
    except ValueError as exc:
        raise RulingError("the ruling file lies outside the repository") from exc
    if not resolved.is_file():
        raise RulingError(f"{relative} is not a regular file")
    if require_committed and not tracked_and_clean(root, relative):
        raise RulingUncommitted(relative)
    raw = resolved.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise RulingError(f"{relative} is not UTF-8 text") from exc
    return text, hashlib.sha256(raw).hexdigest(), relative


def load_checkpoint4_ruling(*, repo_root=None, path=None, require_committed=True):
    """The owner's checkpoint 4 ruling (D-11), read from the committed ruling file.

    ``path`` is for tests; by default the fixed ``60-CHECKPOINT-4-RULING.md`` is read.
    Raises ``RulingMissing`` when there is no file, ``RulingUncommitted`` when it is not
    tracked and clean (unless ``require_committed`` is False), and ``RulingError`` for any
    departure from the strict format.
    """
    text, digest, relative = _read_ruling(RULING4_REL, repo_root, path, require_committed)
    fields = parse_machine_block(text, kind=KIND_CHECKPOINT4)
    return Checkpoint4Ruling(
        answer=fields["answer"],
        approved_first_omega_0=fields["approved_first_omega_0"],
        sha256=digest,
        path=relative,
    )


def load_gap6009_ruling(*, repo_root=None, path=None, require_committed=True):
    """The owner's GAP-60-09 reading, read from its committed ruling file (see above)."""
    text, digest, relative = _read_ruling(RULING_GAP6009_REL, repo_root, path, require_committed)
    fields = parse_machine_block(text, kind=KIND_GAP6009)
    return Gap6009Ruling(reading=fields["reading"], sha256=digest, path=relative)


def ruling_grid_facts(ruling, *, scorecard, confirmed_first_omega_0):
    """Whether the approved setting is on the sweep grid and equals the confirmed one (GAP-60-11).

    Any finite positive setting the owner names is accepted; these two facts are recorded
    beside it. ``confirmed_first_omega_0`` is ``None`` when the sweep confirmed nothing.
    """
    value = getattr(ruling, "approved_first_omega_0", None)
    if getattr(ruling, "answer", None) != "continue" or value is None:
        raise RulingError("only a continue ruling names a setting")
    grid = tuple(float(item) for item in scorecard.section("gate_g2")["grid"])
    confirmed = confirmed_first_omega_0
    return {
        "on_grid": float(value) in grid,
        "equals_confirmed": confirmed is not None and float(value) == float(confirmed),
    }
