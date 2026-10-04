"""Aurora framework models."""

from __future__ import annotations

from dataclasses import dataclass

from orion.core import Score


@dataclass(frozen=True)
class AuroraIndicator:
    """A single Aurora indicator."""

    name: str
    category: str
    value: float | int | str | None
    score: Score
    state: str

    def __post_init__(self) -> None:
        for name, value in (("name", self.name), ("category", self.category), ("state", self.state)):
            if not value.strip():
                raise ValueError(f"{name} must not be empty")
@dataclass(frozen=True)
class AuroraRegime:
    """Aurora regime output."""

    regime: str
    score: Score
    direction: str
    confidence: Score

    def __post_init__(self) -> None:
        for name, value in (("regime", self.regime), ("direction", self.direction)):
            if not value.strip():
                raise ValueError(f"{name} must not be empty")


@dataclass(frozen=True)
class AuroraReport:
    """Normalized Aurora report payload."""

    score: Score
    current_regime: str
    regime_direction: str
    risk_state: str
    transition_risk: str
    indicators: tuple[AuroraIndicator, ...] = ()

    def __post_init__(self) -> None:
        for name, value in (
            ("current_regime", self.current_regime),
            ("regime_direction", self.regime_direction),
            ("risk_state", self.risk_state),
            ("transition_risk", self.transition_risk),
        ):
            if not value.strip():
                raise ValueError(f"{name} must not be empty")

        indicators = tuple(self.indicators)
        if any(not isinstance(item, AuroraIndicator) for item in indicators):
            raise ValueError("indicators must contain AuroraIndicator values")
        object.__setattr__(self, "indicators", indicators)
