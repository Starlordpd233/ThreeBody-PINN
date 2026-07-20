"""Phase 42 / Plan 09 — redaction (must-NOT #2 / CTX-79).

The one-pager records run-directory-relative identity only — no absolute
``/Users/…`` paths, no hostnames, no secrets. The ratified environment
fingerprint (``sw_vers``, ``python -V``, torch version/build) lives in the
``summary.json`` run header ONLY, never in ``summary.md``.

Test: drive a dataset-free synthetic run to completion, then negative-grep
every operator-visible artifact for the forbidden shapes. Full suite green
is the gate.
"""

from __future__ import annotations

import json
import os
import re
import socket
import subprocess
import tempfile
import unittest
from pathlib import Path
from typing import Iterable, List, Tuple

from tests.phase42._fixtures import launch_train, write_train_config

# Regexes for the forbidden shapes (must-NOT #2).
_FORBIDDEN_PATTERNS: List[Tuple[str, re.Pattern[str]]] = [
    ("absolute home path (/Users/)", re.compile(r"/Users/")),
    ("hostname", re.compile(re.escape(socket.gethostname()))),
    # Secret shapes: AWS-style access keys, generic long hex tokens.
    ("AWS access-key shape", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("bearer-token shape", re.compile(r"bearer\s+[A-Za-z0-9\-_\.]{20,}", re.IGNORECASE)),
]


def _unique_name(test_name: str) -> str:
    return f"red-{test_name}-{os.getpid()}"


def _artifact_paths(run_dir: Path) -> Iterable[Path]:
    """Operator-visible text artifacts to scan for forbidden shapes."""
    candidates = [
        run_dir / "status.json",
        run_dir / "summary.json",
        run_dir / "summary.md",
        run_dir / "logs" / "train.log.jsonl",
        run_dir / "logs" / "train.log",
        run_dir / "config.yaml",
        run_dir / "curriculum.jsonl",
    ]
    # TensorBoard events (binary, but we scan for the forbidden ASCII shapes).
    tb_dir = run_dir / "tb"
    if tb_dir.is_dir():
        candidates.extend(sorted(tb_dir.glob("*")))
    for p in candidates:
        if p.is_file():
            yield p


def _scan(path: Path) -> List[str]:
    """Return lines containing a forbidden pattern, tagged with the match name."""
    hits: List[str] = []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return hits
    for label, pat in _FORBIDDEN_PATTERNS:
        for i, line in enumerate(text.splitlines(), 1):
            if pat.search(line):
                hits.append(f"{path}:{i}: [{label}] {line.rstrip()[:200]}")
    return hits


class RedactionTests(unittest.TestCase):
    """must-NOT #2: no /Users/, hostname, or secret shapes in any artifact."""

    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="phase42-redaction-"))
        self.runs_root = self.tmp / "runs"
        self.runs_root.mkdir()

    def tearDown(self) -> None:
        import shutil

        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_no_forbidden_shapes_in_artifacts(self) -> None:
        name = _unique_name("redact")
        cfg = self.tmp / f"{name}.yaml"
        write_train_config(
            cfg,
            run={"run_name": name, "log_every": 1},
            stage={"max_epochs": 2, "n_adam": 2},
        )
        proc = launch_train(cfg, self.runs_root)
        out, err = proc.communicate(timeout=120)
        self.assertEqual(
            proc.returncode,
            0,
            msg=f"synthetic run failed\nstdout={out}\nstderr={err}",
        )
        run_dir = self.runs_root / name
        all_hits: List[str] = []
        for artifact in _artifact_paths(run_dir):
            all_hits.extend(_scan(artifact))
        self.assertEqual(
            all_hits,
            [],
            msg=(
                "forbidden shapes found in artifacts (must-NOT #2 / CTX-79):\n"
                + "\n".join(all_hits)
            ),
        )

    def test_summary_md_has_no_env_fingerprint(self) -> None:
        """summary.md must NOT contain the env fingerprint (summary.json only)."""
        name = _unique_name("md-nofp")
        cfg = self.tmp / f"{name}.yaml"
        write_train_config(
            cfg,
            run={"run_name": name, "log_every": 1},
            stage={"max_epochs": 2, "n_adam": 2},
        )
        proc = launch_train(cfg, self.runs_root)
        proc.communicate(timeout=120)
        run_dir = self.runs_root / name
        md = (run_dir / "summary.md").read_text(encoding="utf-8")
        # The env_fingerprint keys live in summary.json only (B-6/D-12).
        self.assertNotIn("sw_vers", md)
        self.assertNotIn("torch_version", md)
        self.assertNotIn("torch_build", md)
        # summary.json carries the fingerprint (positive control).
        summary = json.loads((run_dir / "summary.json").read_text(encoding="utf-8"))
        self.assertIn("env_fingerprint", summary["header"])


if __name__ == "__main__":
    unittest.main()
