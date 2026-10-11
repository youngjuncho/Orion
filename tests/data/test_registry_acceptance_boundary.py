"""Static architectural guards for the isolated Step 50 trust boundary."""
from __future__ import annotations

import ast
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"


def _python_sources():
    return sorted(SRC.rglob("*.py"))


def _calls_named(path: Path, method_name: str):
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
            continue
        if node.func.attr == method_name:
            yield node


def test_production_accept_snapshot_calls_are_confined_to_guarded_facade():
    calls = {
        path.relative_to(ROOT).as_posix(): list(_calls_named(path, "accept_snapshot"))
        for path in _python_sources()
    }
    calls = {path: nodes for path, nodes in calls.items() if nodes}
    assert set(calls) == {"src/data/registry_acceptance_service.py"}, (
        "Direct acceptance storage calls bypass the guarded validation facade: "
        f"{sorted(calls)}"
    )


def test_production_code_does_not_advance_hwm_directly():
    violations = []
    for path in _python_sources():
        if path.name == "registry_high_water_store.py":
            continue  # The storage primitive defines the method here.
        nodes = list(_calls_named(path, "advance"))
        if nodes:
            violations.append(path.relative_to(ROOT).as_posix())
    assert not violations, f"Direct HWM advance bypasses acceptance journaling: {violations}"


def test_moon_strategy_activation_remains_empty():
    config = yaml.safe_load((ROOT / "config" / "moon.yaml").read_text(encoding="utf-8"))
    assert config["moon"]["active_strategies"] == []
