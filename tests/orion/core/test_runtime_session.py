from pathlib import Path

import pytest

from orion.core import ExecutionMetadata, RuntimeSession, load_config


def make_session() -> RuntimeSession:
    config = load_config(Path(__file__).resolve().parents[3] / "config")
    execution = ExecutionMetadata("execution-001", "2026-08-01T09:00:00+09:00", "1.0")
    return RuntimeSession(config, execution)


def test_runtime_session_follows_documented_lifecycle() -> None:
    session = make_session()

    assert session.status == "Initializing"
    session.start()
    assert session.status == "Running"
    session.complete()
    assert session.status == "Completed"


def test_runtime_session_can_fail_before_completion() -> None:
    session = make_session()
    session.start()
    session.fail()

    assert session.status == "Error"


def test_runtime_session_rejects_invalid_transition() -> None:
    session = make_session()
    session.start()
    session.complete()

    with pytest.raises(RuntimeError, match="cannot move"):
        session.start()
