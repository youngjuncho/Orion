import pytest

from orion.services import ServiceRegistry


def test_service_registry_preserves_registration_order_and_lookup() -> None:
    registry = ServiceRegistry()
    configuration = object()
    logging = object()

    registry.register("Configuration", configuration)
    registry.register("Logging", logging)

    assert registry.names == ("Configuration", "Logging")
    assert registry.get("Configuration") is configuration


def test_service_registry_rejects_duplicate_names() -> None:
    registry = ServiceRegistry()
    registry.register("Configuration", object())

    with pytest.raises(ValueError, match="already registered"):
        registry.register("Configuration", object())


def test_service_registry_rejects_unknown_lookup() -> None:
    with pytest.raises(KeyError, match="not registered"):
        ServiceRegistry().get("Configuration")
