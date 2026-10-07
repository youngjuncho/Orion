"""Shared execution context contract for one Orion runtime cycle."""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Mapping

from data.contracts import MarketDataSet

from .config_loader import OrionConfig
from .execution import ExecutionMetadata
from .state import OrionStateSnapshot

DEFAULT_FRAMEWORKS = ("Aurora", "Moon", "Orbit", "Supernova", "Phoenix")


@dataclass(frozen=True)
class RuntimeContext:
    """Read-only shared context for a single Orion execution."""

    configuration: OrionConfig
    execution: ExecutionMetadata
    market_data: MarketDataSet | None = None
    registered_frameworks: tuple[str, ...] = DEFAULT_FRAMEWORKS
    services: Mapping[str, object] = field(default_factory=dict)
    framework_results: Mapping[str, object] = field(default_factory=dict)
    system_state: OrionStateSnapshot | None = None
    dashboard_data: Mapping[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.registered_frameworks:
            raise ValueError("at least one framework must be registered")
        if any(not framework.strip() for framework in self.registered_frameworks):
            raise ValueError("registered framework names must not be empty")
        if len(self.registered_frameworks) != len(set(self.registered_frameworks)):
            raise ValueError("registered framework names must be unique")

        object.__setattr__(self, "services", MappingProxyType(dict(self.services)))
        object.__setattr__(self, "framework_results", MappingProxyType(dict(self.framework_results)))
        object.__setattr__(self, "dashboard_data", MappingProxyType(dict(self.dashboard_data)))
