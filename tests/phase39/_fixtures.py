"""Deterministic tiny on-disk corpus builder for the Phase 39 test contract.

Everything here is synthesized under a caller-supplied ``TemporaryDirectory``
root: NO helper ever writes beneath the repository ``simulation_data/`` tree
(project governance — the corpus is strictly read-only). The builder models the
README-confirmed file/folder schemas
(``simulation_data/Documentation/README.md`` — File Schemas, File Naming
Conventions, Mandatory Parsing Rules) faithfully enough that the Wave-1+ adapter
can be exercised without the real 6.3 GB dataset.

Modeled invariants (see ``_fixtures`` acceptance criteria in 39-01-PLAN):

* Exactly TWO IC folders (``ic_hierarchical``, ``ic_standard_quasi_random``) for
  FOUR ``brutus_output`` folders — the README 4->2 variant mapping (HIGH-3,
  README:90-155). NO ``_for_gold_standard`` IC folders are created: gold runs
  read the base IC folders (README:155).
* At least one gold Brutus record whose ``(variant, id)`` pairs to a BASE IC
  record — the exact real-corpus shape where a naive 1:1-folder-pairing
  assumption would mass-quarantine ~91% of gold snapshots (HIGH-3 / cycle-2).
* Defensive asymmetric pairing fixtures: a Brutus file with no matching IC file
  and an IC file with no matching Brutus file (cross-AI review N4). The README
  documents the pairing schema, not the real-corpus frequency of either
  anomaly, so neither is asserted to be the most likely observed anomaly
  (cycle-4 claude LOW-2).
* Sparse IDs (real ID ranges carry gaps), paired base/gold hierarchical records
  sharing one IC (hence identical invariants, differing only by fidelity),
  optional/misleading ``Result:`` footers, valid and invalid blacklist JSON,
  optional ``data_version_hash`` metadata, and non-finite/malformed snapshot
  variants.

The builder is fully deterministic: no timestamps, no RNG, no process-specific
tokens enter file CONTENT, so two builds with the same parameters produce
byte-identical relative files (see ``relative_manifest``).
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory

# ---------------------------------------------------------------------------
# Canonical folder / naming constants (README File Naming Conventions).
# ---------------------------------------------------------------------------

IC_SUBDIR = "ic_final"
BRUTUS_SUBDIR = "brutus_output"

# EXACTLY two IC folders (README:90-155). No ``_for_gold_standard`` IC folder.
IC_FOLDERS = ("ic_hierarchical", "ic_standard_quasi_random")

# FOUR Brutus folders, base + gold per variant.
BRUTUS_FOLDERS = (
    "brutus_hierarchical",
    "brutus_hierarchical_gold_standard",
    "brutus_standard_quasi_random",
    "brutus_standard_quasi_random_gold_standard",
)

# Filename prefixes are the BASE prefixes in every folder; gold status lives in
# the folder name only (README:207-222).
_IC_PREFIX = {"hierarchical": "ic_hierarchical", "standard": "ic_standard"}
_BRUTUS_PREFIX = {"hierarchical": "brutus_hierarchical", "standard": "brutus_standard"}

# Deterministic distinct masses (hierarchical vary; standard are exactly 1.0).
HIER_MASSES = (1.3490330328149076, 0.3068019185652623, 1.3441650486198304)
STD_MASSES = (1.0, 1.0, 1.0)

# A fixed synthetic version hash so match/mismatch/absent paths are testable.
KNOWN_DATA_VERSION_HASH = "a" * 64


def _body_line(mass, index, t):
    """One body line ``m x y z vx vy vz`` with deterministic distinct values.

    ``repr`` guarantees an exact float round-trip, matching the Phase 38
    fixture writer (``tests/phase38/test_fixture_loader.py``).
    """
    x = 1.0 + index + 0.1 * t
    y = -0.5 * (index + 1) + 0.2 * t
    z = 0.05 * (index + 1) - 0.01 * t
    vx = 0.3 * (index + 1)
    vy = -0.2 * (index + 1)
    vz = 0.01 * (index + 1)
    return f"{mass!r} {x!r} {y!r} {z!r} {vx!r} {vy!r} {vz!r}"


def complete_times(n=12):
    """Times whose FINAL value is >= 9.5 (passes the completeness gate)."""
    return [round(i * (10.0 / (n - 1)), 6) for i in range(n)]


def truncated_times(n=6):
    """Times whose FINAL value is < 9.5 (fails the completeness gate)."""
    return [round(i * (4.0 / (n - 1)), 6) for i in range(n)]


# Three observed footer schemas + None (README:283-300). A footer claiming a
# complete run must NEVER rescue a truncated file (metadata only).
FOOTER_FULL = (
    "Result: filename= /x/ic_0000.txt N= 3 t_begin= 0 t_end= 10 dt= 0.08 "
    "eta= 0.263027 tol= 1e-15 Lw= 130 t_cpu= 11.2667 E_initial= -1.23733 "
    "E_final= -1.23733 dE/E= 1.49235e-14"
)
FOOTER_PARTIAL = (
    "Result: filename= /x/ic_0000.txt N= 3 t_begin= 0.0 t_end= 10.0 dt= 0.08 "
    "tol= 1e-15 Lw= 130 t_cpu= 8.5887 E_initial= -3.11082 E_final= -3.11082 "
    "dE/E= 1.97004e-14"
)
FOOTER_MINIMAL = (
    "Result: filename= C:\\x\\ic_0000.txt N= 3 t_begin= 0.0 t_end= 10.01 "
    "dt= 0.01 Lw= 130 t_cpu= 431.969 E_initial= -2.10843 E_final= -2.10843 "
    "dE/E= 1.44300e-12"
)


def _brutus_text(times, masses, footer=None, body_override=None):
    """Render a Brutus trajectory. ``body_override(t, i, m)`` may inject a
    malformed / non-finite line for a specific snapshot/body."""
    lines = []
    for t in times:
        lines.append(f"{t!r} 3 {0.5 * t!r}")
        for i, m in enumerate(masses):
            if body_override is not None:
                line = body_override(t, i, m)
                if line is None:
                    continue  # drop the row entirely (malformed block)
                lines.append(line)
            else:
                lines.append(_body_line(m, i, t))
        lines.append("")
    if footer is not None:
        lines.append(footer)
    return "\n".join(lines) + "\n"


def write_ic(path, masses):
    Path(path).write_text(
        "\n".join(_body_line(m, i, 0.0) for i, m in enumerate(masses)) + "\n"
    )
    return Path(path)


def write_brutus(path, times, masses, footer=None, body_override=None):
    Path(path).write_text(_brutus_text(times, masses, footer, body_override))
    return Path(path)


def _nonfinite_interior(t, i, m):
    """Inject a single non-finite value in an INTERIOR snapshot (t == 4.0),
    leaving >= 2 finite monotone blocks around it (GAP-39-05 salvage bait)."""
    if abs(t - 4.0) < 1e-9 and i == 1:
        return f"{m!r} inf 0.0 0.0 0.0 0.0 0.0"
    return _body_line(m, i, t)


def _nonfinite_pervasive(t, i, m):
    """Inject non-finite values in ALL but the first snapshot, so fewer than two
    finite blocks remain after dropping (GAP-39-05 dual-reason case)."""
    if t > 0.0 and i == 0:
        return f"{m!r} nan 0.0 0.0 0.0 0.0 0.0"
    return _body_line(m, i, t)


def _malformed_missing_row(t, i, m):
    """Drop the 3rd body row of one snapshot (t == 2.0): a partial body block
    that must NOT be salvaged as a sample (GAP-39-05)."""
    if abs(t - 2.0) < 1e-9 and i == 2:
        return None
    return _body_line(m, i, t)


class TinyCorpus:
    """A deterministic, read-only tiny corpus tree under a ``TemporaryDirectory``.

    Use as a context manager::

        with TinyCorpus() as corpus:
            adapter = AdmittedSetAdapter(root=corpus.data_root, ...)

    Layout (all ``id`` values are sparse — real ID ranges carry gaps):

    * hierarchical base IC ids .......... {0, 3, 7, 42, 100}
    * brutus_hierarchical (base) ids .... {0, 3, 7, 42, 55, 200, 201, 202, 900}
    * brutus_hierarchical_gold ids ...... {0, 3, 7}   (each has a BASE IC -> HIGH-3)
    * standard base IC ids .............. {0, 5, 9}
    * brutus_standard_quasi_random ...... {0, 5, 9}
    * brutus_standard_..._gold ids ...... {0, 5}      (id 9 has no gold -> anomaly)

    Asymmetric pairing:
      * IC-without-Brutus ..... ("hierarchical", 100)
      * Brutus-without-IC ..... ("hierarchical", 55)
    HIGH-3 gold-with-base-IC .. ("hierarchical", 0) (and 3, 7)
    """

    def __init__(self):
        self._tmp = TemporaryDirectory(prefix="phase39-tinycorpus-")
        base = Path(self._tmp.name)
        self.data_root = base / "Data"
        self.run_dir = base / "run"
        self.created_paths: list[Path] = []
        self._build()

    # -- context manager -----------------------------------------------------
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self._tmp.cleanup()
        return False

    # -- path helpers --------------------------------------------------------
    def _ic_path(self, variant, id_):
        folder = "ic_hierarchical" if variant == "hierarchical" else "ic_standard_quasi_random"
        return self.data_root / IC_SUBDIR / folder / f"{_IC_PREFIX[variant]}_{id_:04d}.txt"

    def _brutus_path(self, folder, variant, id_):
        return self.data_root / BRUTUS_SUBDIR / folder / f"{_BRUTUS_PREFIX[variant]}_{id_:04d}.txt"

    def _record(self, path):
        self.created_paths.append(Path(path))
        return path

    def _masses(self, variant):
        return HIER_MASSES if variant == "hierarchical" else STD_MASSES

    # -- construction --------------------------------------------------------
    def _build(self):
        for folder in IC_FOLDERS:
            (self.data_root / IC_SUBDIR / folder).mkdir(parents=True, exist_ok=True)
        for folder in BRUTUS_FOLDERS:
            (self.data_root / BRUTUS_SUBDIR / folder).mkdir(parents=True, exist_ok=True)
        self.run_dir.mkdir(parents=True, exist_ok=True)

        self._build_hierarchical()
        self._build_standard()
        self._build_blacklists()
        self._build_version_metadata()

    def _build_hierarchical(self):
        m = HIER_MASSES
        footers = {0: FOOTER_FULL, 3: FOOTER_PARTIAL, 7: FOOTER_MINIMAL, 42: None}

        # Base IC for the clean ids plus the IC-without-Brutus id (100).
        for id_ in (0, 3, 7, 42, 100):
            self._record(write_ic(self._ic_path("hierarchical", id_), m))

        # Base Brutus for the clean ids (0,3,7,42). id 55 has NO IC.
        for id_ in (0, 3, 7, 42):
            self._record(write_brutus(
                self._brutus_path("brutus_hierarchical", "hierarchical", id_),
                complete_times(), m, footer=footers[id_]))
        # Brutus-without-IC: ("hierarchical", 55).
        self._record(write_brutus(
            self._brutus_path("brutus_hierarchical", "hierarchical", 55),
            complete_times(), m, footer=FOOTER_FULL))

        # Gold Brutus for ids {0,3,7} — each pairs to a BASE IC (HIGH-3). Higher
        # cadence footer (dt_out=0.01) but structurally identical parse.
        for id_ in (0, 3, 7):
            self._record(write_brutus(
                self._brutus_path("brutus_hierarchical_gold_standard", "hierarchical", id_),
                complete_times(24), m, footer=FOOTER_MINIMAL))

        # Anomaly Brutus variants (each also has a base IC so the anomaly is
        # isolated to the Brutus structural / conservation gate).
        for id_ in (200, 201, 202, 900):
            self._record(write_ic(self._ic_path("hierarchical", id_), m))

        self.nonfinite_interior_path = self._record(write_brutus(
            self._brutus_path("brutus_hierarchical", "hierarchical", 200),
            complete_times(), m, body_override=_nonfinite_interior))
        self.nonfinite_pervasive_path = self._record(write_brutus(
            self._brutus_path("brutus_hierarchical", "hierarchical", 201),
            complete_times(), m, body_override=_nonfinite_pervasive))
        self.malformed_path = self._record(write_brutus(
            self._brutus_path("brutus_hierarchical", "hierarchical", 202),
            complete_times(), m, body_override=_malformed_missing_row))
        # Truncated file with a MISLEADING footer claiming a complete run.
        self.truncated_misleading_footer_path = self._record(write_brutus(
            self._brutus_path("brutus_hierarchical", "hierarchical", 900),
            truncated_times(), m, footer=FOOTER_FULL))

    def _build_standard(self):
        m = STD_MASSES
        for id_ in (0, 5, 9):
            self._record(write_ic(self._ic_path("standard", id_), m))
            self._record(write_brutus(
                self._brutus_path("brutus_standard_quasi_random", "standard", id_),
                complete_times(), m, footer=None))
        # Gold for {0,5} only — id 9 has no gold counterpart (the documented
        # "184 IDs not in gold" anomaly, README dataset-reference).
        for id_ in (0, 5):
            self._record(write_brutus(
                self._brutus_path("brutus_standard_quasi_random_gold_standard", "standard", id_),
                complete_times(24), m, footer=FOOTER_MINIMAL))

    def _build_blacklists(self):
        # Valid blacklist: top-level ``hierarchical`` and ``standard`` integer
        # lists (fail-closed schema, ctl_instruction.md:609-635). Blacklist ids
        # that EXIST in the corpus so the filter is observable.
        self.blacklist_path = self._record(self.data_root / "problematic_ics_blacklist.json")
        self.blacklist_path.write_text(
            json.dumps({"hierarchical": [3], "standard": [5]}, sort_keys=True, indent=2) + "\n"
        )
        self.blacklisted_hierarchical = (3,)
        self.blacklisted_standard = (5,)

        # Invalid schema (wrong types) — must be a HARD init failure, never an
        # empty-blacklist substitution.
        self.invalid_blacklist_path = self._record(self.data_root / "blacklist_invalid.json")
        self.invalid_blacklist_path.write_text(
            json.dumps({"hierarchical": "not-a-list", "standard": [5]}) + "\n"
        )

    def _build_version_metadata(self):
        self.version_metadata_path = self._record(self.data_root / "data_version.json")
        self.version_metadata_path.write_text(
            json.dumps({"data_version_hash": KNOWN_DATA_VERSION_HASH}, sort_keys=True, indent=2) + "\n"
        )
        # A path that deliberately does not exist — the absent-field deferral.
        self.absent_version_metadata_path = self.data_root / "data_version_absent.json"

    # -- accessors used by the deferred contract tests -----------------------
    gold_with_base_ic = ("hierarchical", 0)
    brutus_without_ic = ("hierarchical", 55)
    ic_without_brutus = ("hierarchical", 100)
    known_data_version_hash = KNOWN_DATA_VERSION_HASH

    def relative_manifest(self):
        """Map every created corpus file to its sha256, keyed by path RELATIVE to
        the temporary base. Absolute temp names differ per build; relative paths
        and bytes are byte-identical for equal parameters (determinism check)."""
        base = Path(self._tmp.name)
        manifest = {}
        for path in sorted(self.created_paths):
            p = Path(path)
            if p.is_file():
                rel = p.relative_to(base).as_posix()
                manifest[rel] = hashlib.sha256(p.read_bytes()).hexdigest()
        return manifest


def simulation_data_root(repo_root):
    """Resolved repository ``simulation_data/`` root (the read-only boundary)."""
    return (Path(repo_root) / "simulation_data").resolve()


def path_is_outside(path, forbidden_root):
    """True iff ``path`` does NOT resolve beneath ``forbidden_root``."""
    try:
        Path(path).resolve().relative_to(Path(forbidden_root))
    except ValueError:
        return True
    return False
