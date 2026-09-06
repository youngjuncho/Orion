"""In-memory framework registry for one Orion runtime."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class FrameworkRegistry:
    """Register each framework instance once per runtime execution."""

    _frameworks: dict[str, object] = field(default_factory=dict, init=False, repr=False)

    @property
    def names(self) -> tuple[str, ...]:
        """Return registered framework names in registration order."""

        return tuple(self._frameworks)

    def register(self, name: str, framework: object) -> None:
        """Register a framework instance under a non-empty unique name."""

        if not name.strip():
            raise ValueError("framework name must not be empty")
        if name in self._frameworks:
            raise ValueError(f"framework already registered: {name}")
        self._frameworks[name] = framework

    def get(self, name: str) -> object:
        """Return a registered framework instance."""

        try:
            return self._frameworks[name]
        except KeyError as exc:
            raise KeyError(f"framework is not registered: {name}") from exc
