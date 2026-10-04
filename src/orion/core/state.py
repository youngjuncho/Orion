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
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string")

        if (
            not isinstance(self.system_status, str)
            or self.system_status not in SYSTEM_STATUSES
        ):
            raise ValueError(f"unsupported system status: {self.system_status}")

        for name, values in (
            ("framework_states", self.framework_states),
            ("portfolio_state", self.portfolio_state),
        ):
            if not isinstance(values, Mapping):
                raise ValueError(f"{name} must be a mapping")
            snapshot = dict(values)
            if any(
                not isinstance(key, str)
                or not key.strip()
                or not isinstance(value, str)
                or not value.strip()
                for key, value in snapshot.items()
            ):
                raise ValueError(f"{name} must contain non-empty string keys and values")
            object.__setattr__(self, name, MappingProxyType(snapshot))
