import pytest

from orion.core import FrameworkRegistry


def test_framework_registry_preserves_registration_order_and_lookup() -> None:
    registry = FrameworkRegistry()
    moon = object()
    aurora = object()

    registry.register("Moon", moon)
    registry.register("Aurora", aurora)

    assert registry.names == ("Moon", "Aurora")
    assert registry.get("Moon") is moon


def test_framework_registry_rejects_duplicate_names() -> None:
    registry = FrameworkRegistry()
    registry.register("Moon", object())

    with pytest.raises(ValueError, match="already registered"):
        registry.register("Moon", object())


def test_framework_registry_rejects_unknown_framework_lookup() -> None:
    with pytest.raises(KeyError, match="not registered"):
        FrameworkRegistry().get("Moon")
