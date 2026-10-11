"""Keep the experimental registry persistence layer out of production frameworks."""
from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FRAMEWORK_SOURCE_ROOTS = (ROOT / "src" / "orion", ROOT / "src" / "runtime")
FORBIDDEN_MODULES = {
    "data.registry_high_water_store",
    "data.registry_acceptance_service",
    "data.registry_acceptance_consumer",
    "src.data.registry_high_water_store",
    "src.data.registry_acceptance_service",
    "src.data.registry_acceptance_consumer",
}


def _imported_modules(tree: ast.AST):
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                yield alias.name
        elif isinstance(node, ast.ImportFrom) and node.module:
            yield node.module


def test_registry_persistence_remains_isolated_from_framework_source():
    violations = []
    for source_root in FRAMEWORK_SOURCE_ROOTS:
        if not source_root.exists():
            continue
        for path in sorted(source_root.rglob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            forbidden = sorted(set(_imported_modules(tree)) & FORBIDDEN_MODULES)
            if forbidden:
                violations.append((path.relative_to(ROOT).as_posix(), forbidden))

    assert not violations, (
        "Registry persistence is still an unapproved experiment and must not be "
        f"wired into Runtime/framework code: {violations}"
    )


def test_importing_general_data_package_does_not_load_experimental_persistence():
    import subprocess
    import sys

    script = (
        "import sys; "
        f"sys.path.insert(0, {str(ROOT / 'src')!r}); "
        "import data; "
        "blocked = {'data.registry_high_water_store', "
        "'data.registry_acceptance_service', "
        "'data.registry_acceptance_consumer'}; "
        "loaded = sorted(blocked.intersection(sys.modules)); "
        "assert not loaded, f'experimental persistence loaded: {loaded}'"
    )
    result = subprocess.run(
        [sys.executable, "-c", script],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
