"""In-memory state snapshot store for one Orion runtime."""

from __future__ import annotations

from dataclasses import dataclass, field

from .state import OrionStateSnapshot


@dataclass
class StateStore:
    """Keep immutable state snapshots in publication order."""

    _snapshots: list[OrionStateSnapshot] = field(default_factory=list, init=False, repr=False)

    @property
    def snapshots(self) -> tuple[OrionStateSnapshot, ...]:
        """Return all published snapshots without exposing mutable storage."""

        return tuple(self._snapshots)

    @property
    def current(self) -> OrionStateSnapshot | None:
        """Return the latest snapshot, if one has been published."""

        return self._snapshots[-1] if self._snapshots else None

    def publish(self, snapshot: OrionStateSnapshot) -> None:
        """Publish one complete snapshot without replacing prior history."""
        self.validate(snapshot)
        self._snapshots.append(snapshot)

    def validate(self, snapshot: OrionStateSnapshot) -> None:
        """Check whether a snapshot can be published without changing the store."""
        if not isinstance(snapshot, OrionStateSnapshot):
            raise TypeError("snapshot must be an OrionStateSnapshot")
        if any(existing.execution_id == snapshot.execution_id for existing in self._snapshots):
            raise ValueError(f"execution_id already exists: {snapshot.execution_id}")

    def _rollback_to(self, snapshot_count: int) -> None:
        del self._snapshots[snapshot_count:]
