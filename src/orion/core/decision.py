"""Decision and state-transition contracts for the Orion Runtime."""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Mapping


@dataclass(frozen=True)
class DecisionCandidate:
    """A proposed decision that is not yet authoritative."""

    candidate_id: str
    framework_name: str
    decision_type: str
    entity_type: str
    entity_id: str
    payload: Mapping[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _strings(
            candidate_id=self.candidate_id,
            framework_name=self.framework_name,
            decision_type=self.decision_type,
            entity_type=self.entity_type,
            entity_id=self.entity_id,
        )
        object.__setattr__(self, "payload", _mapping(self.payload, "payload"))


@dataclass(frozen=True)
class AcceptedDecision:
    """An accepted candidate produced by an explicit Runtime policy."""

    decision_id: str
    candidate: DecisionCandidate
    accepted_by: str
    conditions: Mapping[str, object] | None = None

    def __post_init__(self) -> None:
        _strings(accepted_by=self.accepted_by, decision_id=self.decision_id)
        if not isinstance(self.candidate, DecisionCandidate):
            raise ValueError("candidate must be DecisionCandidate")
        if self.conditions is not None:
            object.__setattr__(self, "conditions", _mapping(self.conditions, "conditions"))


def auto_approve(candidate: DecisionCandidate) -> AcceptedDecision:
    """Accept one candidate under Orion's default Runtime governance policy.

    Auto-approval is a governance acceptance policy, not investment methodology
    or broker execution. The accepted decision remains an explicit
    ``AcceptedDecision`` in the canonical lifecycle.
    """
    if not isinstance(candidate, DecisionCandidate):
        raise TypeError("candidate must be DecisionCandidate")
    return AcceptedDecision(
        decision_id=f"accepted:{candidate.candidate_id}",
        candidate=candidate,
        accepted_by="orion-runtime:auto-approval",
    )


@dataclass(frozen=True)
class StateTransition:
    """An explicit proposed state change derived from an AcceptedDecision."""

    transition_id: str
    decision_id: str
    entity_type: str
    entity_id: str
    previous_state: str | None
    new_state: str
    state_payload: Mapping[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _strings(
            transition_id=self.transition_id,
            decision_id=self.decision_id,
            entity_type=self.entity_type,
            entity_id=self.entity_id,
            new_state=self.new_state,
        )
        if self.previous_state is not None and not self.previous_state.strip():
            raise ValueError("previous_state must be non-empty when provided")
        object.__setattr__(self, "state_payload", _mapping(self.state_payload, "state_payload"))


def _strings(**values: str) -> None:
    for name, value in values.items():
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{name} must be a non-empty string")


def _mapping(value: Mapping[str, object], name: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{name} must be a mapping")
    copied = dict(value)
    if any(not isinstance(key, str) or not key.strip() for key in copied):
        raise ValueError(f"{name} keys must be non-empty strings")
    return MappingProxyType(copied)
