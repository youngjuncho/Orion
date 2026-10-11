"""Validate UTF-8 (without BOM) for repository text files.

Binary assets such as PDF, images, archives, and compiled files are excluded.
Run from any directory: python scripts/check_utf8.py
"""
from __future__ import annotations

from pathlib import Path

TEXT_SUFFIXES = {
    ".py", ".md", ".json", ".yaml", ".yml", ".toml", ".ini", ".cfg",
    ".txt", ".sh", ".ps1", ".bat", ".sql", ".html", ".css", ".js",
    ".ts", ".tsx", ".jsx", ".xml", ".csv", ".rst",
}
SPECIAL_NAMES = {".gitignore", ".gitattributes", ".editorconfig"}
EXCLUDED_DIRS = {".git", ".venv", "venv", "env", "__pycache__", ".pytest_cache"}

def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors: list[str] = []
    checked = 0
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if any(part in EXCLUDED_DIRS for part in relative.parts):
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in SPECIAL_NAMES:
            continue
        try:
            data = path.read_bytes()
            data.decode("utf-8", errors="strict")
            if data.startswith(b"\xef\xbb\xbf"):
                errors.append(f"{relative}: UTF-8 BOM is not allowed")
            checked += 1
        except UnicodeDecodeError as exc:
            errors.append(f"{relative}: not valid UTF-8 ({exc})")
    if errors:
        print("UTF-8 policy check failed:")
        print("\n".join(f"- {item}" for item in errors))
        return 1
    print(f"UTF-8 policy check passed ({checked} text files; UTF-8 without BOM).")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
