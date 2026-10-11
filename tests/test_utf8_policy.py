"""Repository-wide UTF-8 text-file policy."""
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_repository_text_files_are_utf8_without_bom():
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "check_utf8.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
