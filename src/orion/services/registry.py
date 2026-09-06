"""In-memory service registry for one Orion runtime."""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Mapping


@dataclass
class ServiceRegistry:
    """Register shared service instances under unique names."""

    _services: dict[str, object] = field(default_factory=dict, init=False, repr=False)

    @property
    def names(self) -> tuple[str, ...]:
        """Return registered service names in registration order."""

        return tuple(self._services)

    @property
    def snapshot(self) -> Mapping[str, object]:
        """Return a read-only view of the current registry contents."""

        return MappingProxyType(dict(self._services))

    def register(self, name: str, service: object) -> None:
        """Register a service instance under a non-empty unique name."""

        if not name.strip():
            raise ValueError("service name must not be empty")
        if name in self._services:
            raise ValueError(f"service already registered: {name}")
        self._services[name] = service

    def get(self, name: str) -> object:
        """Return a registered service instance."""

        try:
            return self._services[name]
        except KeyError as exc:
            raise KeyError(f"service is not registered: {name}") from exc
