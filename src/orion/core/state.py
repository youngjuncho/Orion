"""Immutable Orion state snapshot contract."""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Mapping

SYSTEM_STATUSES = frozenset({"Initializing", "Running", "Completed", "Warning", "Error"})


@dataclass(frozen=True)
class OrionStateSnapshot:
    """A complete operational snapshot described by the State Model."""

    timestamp: str
    execution_id: str
    orion_version: str
    framework_states: Mapping[str, str] = field(default_factory=dict)
    portfolio_state: Mapping[str, str] = field(default_factory=dict)
    system_status: str = "Initializing"

    def __post_init__(self) -> None:
        for name, value in (
            ("timestamp", self.timestamp),
            ("execution_id", self.execution_id),
            ("orion_version", self.orion_version),
        ):
            if not value.strip():
                raise ValueError(f"{name} must not be empty")

        if self.system_status not in SYSTEM_STATUSES:
            raise ValueError(f"unsupported system status: {self.system_status}")

        object.__setattr__(self, "framework_states", MappingProxyType(dict(self.framework_states)))
        object.__setattr__(self, "portfolio_state", MappingProxyType(dict(self.portfolio_state)))
