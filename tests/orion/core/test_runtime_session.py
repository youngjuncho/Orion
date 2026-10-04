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
    service = object()
    session.services.register("Configuration", service)
    assert session.services.get("Configuration") is service
    session.start()
    assert session.status == "Running"
    session.complete()
    assert session.status == "Completed"


def test_runtime_session_can_fail_before_completion() -> None:
    session = make_session()
    session.start()
    session.fail()

    assert session.status == "Error"


def test_runtime_sessions_own_independent_in_memory_stores_and_registries() -> None:
    first = make_session()
    second = make_session()
    marker = object()
    first.registry.register("Moon", marker)
    first.services.register("Marker", marker)

    assert second.registry.names == ()
    assert second.services.names == ()
    assert first.events is not second.events
    assert first.states is not second.states


def test_runtime_session_rejects_invalid_transition() -> None:
    session = make_session()
    session.start()
    session.complete()

    with pytest.raises(RuntimeError, match="cannot move"):
        session.start()


def test_runtime_session_builds_read_only_context_from_registered_components() -> None:
    session = make_session()
    framework = object()
    service = object()
    session.registry.register("Moon", framework)
    session.services.register("Configuration", service)

    context = session.build_context(
        framework_results={"Moon": "result"},
        dashboard_data={"status": "ready"},
    )

    assert context.registered_frameworks == ("Moon",)
    assert context.services["Configuration"] is service
    assert context.framework_results["Moon"] == "result"
    assert context.dashboard_data["status"] == "ready"


def test_runtime_session_requires_registered_framework_for_context() -> None:
    with pytest.raises(ValueError, match="at least one framework"):
        make_session().build_context()
