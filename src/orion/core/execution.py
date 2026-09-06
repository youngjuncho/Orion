"""Execution metadata contract for one Orion runtime cycle."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ExecutionMetadata:
    """Immutable execution information described by the Runtime model."""

    execution_id: str
    start_time: str
    orion_version: str
    end_time: str | None = None
    duration_seconds: float | None = None

    def __post_init__(self) -> None:
        for name, value in (
            ("execution_id", self.execution_id),
            ("start_time", self.start_time),
            ("orion_version", self.orion_version),
        ):
            if not value.strip():
                raise ValueError(f"{name} must not be empty")

        if self.end_time is not None and not self.end_time.strip():
            raise ValueError("end_time must not be empty when provided")
        if self.duration_seconds is not None and self.duration_seconds < 0:
            raise ValueError("duration_seconds must be non-negative")
