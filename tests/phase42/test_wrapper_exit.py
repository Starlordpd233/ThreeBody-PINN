"""Phase 42 / Plan 07 — wrapper exit propagation (must-NOT #3)."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WRAPPER = ROOT / "scripts" / "train-unattended.sh"


class WrapperExitTests(unittest.TestCase):
    """must-NOT #3: guard trip surfaces a non-zero exit code, not a silent success."""

    @unittest.skipUnless(shutil.which("caffeinate"), "requires macOS caffeinate")
    def test_guard_trip_returns_nonzero_exit(self):
        args = ["--config", str(ROOT / "does-not-exist.yaml")]
        env = os.environ.copy()
        env["PATH"] = os.pathsep.join(
            (str(Path(sys.executable).parent), env.get("PATH", ""))
        )
        direct = subprocess.run(
            [sys.executable, "-m", "pinn.train", *args],
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        wrapped = subprocess.run(
            [str(WRAPPER), *args],
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertNotEqual(direct.returncode, 0, msg=direct.stderr)
        self.assertEqual(wrapped.returncode, direct.returncode, msg=wrapped.stderr)


if __name__ == "__main__":
    unittest.main()
