"""Configuration loading and validation for Orion OS."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover - exercised only in incomplete environments
    raise ImportError("PyYAML is required to load Orion configuration files.") from exc


REQUIRED_CONFIG_FILES = {
    "system": "system.yaml",
    "moon": "moon.yaml",
    "aurora": "aurora.yaml",
    "supernova": "supernova.yaml",
    "phoenix": "phoenix.yaml",
}


class ConfigError(Exception):
    """Base exception for Orion configuration errors."""


class ConfigFileNotFoundError(ConfigError):
    """Raised when one or more required configuration files are missing."""


class ConfigValidationError(ConfigError):
    """Raised when configuration content does not match Orion documentation."""


@dataclass(frozen=True)
class LoggingConfig:
    level: str


@dataclass(frozen=True)
class SystemDataConfig:
    retention_days: int | None


@dataclass(frozen=True)
class DashboardConfig:
    refresh_minutes: int


@dataclass(frozen=True)
class SystemConfig:
    version: str
    environment: str
    timezone: str
    currency: str
    logging: LoggingConfig
    data: SystemDataConfig
    dashboard: DashboardConfig


@dataclass(frozen=True)
class FeatureFlagConfig:
    enabled: bool


@dataclass(frozen=True)
class MoonConfig:
    enabled: bool
    rebalance_frequency: str
    strategies: tuple[str, ...]
    strategy_weighting: str
    execution_mode: str
    signal_assets: FeatureFlagConfig
    execution_mapping: FeatureFlagConfig


@dataclass(frozen=True)
class ScoreRangeConfig:
    min: int
    max: int


@dataclass(frozen=True)
class IndicatorGroupsConfig:
    core: tuple[str, ...]
    cross_asset: tuple[str, ...]


@dataclass(frozen=True)
class AuroraConfig:
    enabled: bool
    update_frequency: str
    scoring_range: ScoreRangeConfig
    indicator_groups: IndicatorGroupsConfig
    transition_monitoring: FeatureFlagConfig


@dataclass(frozen=True)
class CandidateUniverseConfig:
    source: str


@dataclass(frozen=True)
class SupernovaScoringConfig:
    range: str


@dataclass(frozen=True)
class SupernovaConfig:
    enabled: bool
    review_frequency: str
    framework: str
    approved_companies: tuple[str, ...]
    candidate_universe: CandidateUniverseConfig
    replacement_policy: FeatureFlagConfig
    scoring: SupernovaScoringConfig


@dataclass(frozen=True)
class CoreAssetsConfig:
    btc_weight: float
    eth_weight: float


@dataclass(frozen=True)
class CategoryLeadershipConfig:
    leader: str
    challenger: str


@dataclass(frozen=True)
class PhoenixConfig:
    enabled: bool
    review_frequency: str
    core_assets: CoreAssetsConfig
    portfolio_construction: str
    categories: dict[str, CategoryLeadershipConfig]
    replacement_policy: FeatureFlagConfig
    leadership_monitoring: FeatureFlagConfig


@dataclass(frozen=True)
class OrionConfig:
    system: SystemConfig
    moon: MoonConfig
    aurora: AuroraConfig
    supernova: SupernovaConfig
    phoenix: PhoenixConfig


def load_yaml_file(path: str | Path) -> dict[str, Any]:
    """Load a YAML file and require a top-level mapping."""

    config_path = Path(path)
    try:
        with config_path.open("r", encoding="utf-8") as handle:
            loaded = yaml.safe_load(handle)
    except yaml.YAMLError as exc:
        raise ConfigValidationError(f"{config_path} is not valid YAML: {exc}") from exc

    if not isinstance(loaded, dict):
        raise ConfigValidationError(f"{config_path} must contain a YAML mapping.")

    return loaded


def validate_required_files(config_dir: str | Path) -> None:
    """Validate that all required Orion configuration files exist."""

    root = Path(config_dir)
    missing = [
        filename
        for filename in REQUIRED_CONFIG_FILES.values()
        if not (root / filename).is_file()
    ]
    if missing:
        raise ConfigFileNotFoundError(
            f"Missing required configuration file(s): {', '.join(missing)}"
        )


def load_config(config_dir: str | Path = "config") -> OrionConfig:
    """Load all required Orion configuration files as typed objects."""

    root = Path(config_dir)
    validate_required_files(root)

    payloads = {
        name: _section(load_yaml_file(root / filename), name, root / filename)
        for name, filename in REQUIRED_CONFIG_FILES.items()
    }

    return OrionConfig(
        system=_parse_system(payloads["system"]),
        moon=_parse_moon(payloads["moon"]),
        aurora=_parse_aurora(payloads["aurora"]),
        supernova=_parse_supernova(payloads["supernova"]),
        phoenix=_parse_phoenix(payloads["phoenix"]),
    )


def _section(payload: dict[str, Any], name: str, path: Path) -> dict[str, Any]:
    if name not in payload:
        raise ConfigValidationError(f"{path} must contain top-level key '{name}'.")
    section = payload[name]
    if not isinstance(section, dict):
        raise ConfigValidationError(f"{path}:{name} must be a mapping.")
    return section


def _parse_system(payload: dict[str, Any]) -> SystemConfig:
    return SystemConfig(
        version=_required_str(payload, "version", "system.version"),
        environment=_enum(
            _required_str(payload, "environment", "system.environment"),
            {"production"},
            "system.environment",
        ),
        timezone=_required_str(payload, "timezone", "system.timezone"),
        currency=_required_str(payload, "currency", "system.currency"),
        logging=LoggingConfig(
            level=_enum(
                _required_str(_required_mapping(payload, "logging", "system.logging"), "level", "system.logging.level"),
                {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"},
                "system.logging.level",
            )
        ),
        data=SystemDataConfig(
            retention_days=_optional_int(
                _required_mapping(payload, "data", "system.data"),
                "retention_days",
                "system.data.retention_days",
            )
        ),
        dashboard=DashboardConfig(
            refresh_minutes=_required_int(
                _required_mapping(payload, "dashboard", "system.dashboard"),
                "refresh_minutes",
                "system.dashboard.refresh_minutes",
            )
        ),
    )


def _parse_moon(payload: dict[str, Any]) -> MoonConfig:
    return MoonConfig(
        enabled=_required_bool(payload, "enabled", "moon.enabled"),
        rebalance_frequency=_enum(
            _required_str(payload, "rebalance_frequency", "moon.rebalance_frequency"),
            {"monthly"},
            "moon.rebalance_frequency",
        ),
        strategies=_tuple_of_str(payload, "strategies", "moon.strategies"),
        strategy_weighting=_enum(
            _required_str(payload, "strategy_weighting", "moon.strategy_weighting"),
            {"equal"},
            "moon.strategy_weighting",
        ),
        execution_mode=_enum(
            _required_str(payload, "execution_mode", "moon.execution_mode"),
            {"consensus"},
            "moon.execution_mode",
        ),
        signal_assets=_feature_flag(
            payload, "signal_assets", "moon.signal_assets"
        ),
        execution_mapping=_feature_flag(
            payload, "execution_mapping", "moon.execution_mapping"
        ),
    )


def _parse_aurora(payload: dict[str, Any]) -> AuroraConfig:
    groups = _required_mapping(payload, "indicator_groups", "aurora.indicator_groups")
    scoring_range = _required_mapping(payload, "scoring_range", "aurora.scoring_range")
    return AuroraConfig(
        enabled=_required_bool(payload, "enabled", "aurora.enabled"),
        update_frequency=_enum(
            _required_str(payload, "update_frequency", "aurora.update_frequency"),
            {"daily"},
            "aurora.update_frequency",
        ),
        scoring_range=ScoreRangeConfig(
            min=_required_int(scoring_range, "min", "aurora.scoring_range.min"),
            max=_required_int(scoring_range, "max", "aurora.scoring_range.max"),
        ),
        indicator_groups=IndicatorGroupsConfig(
            core=_tuple_of_str(groups, "core", "aurora.indicator_groups.core"),
            cross_asset=_tuple_of_str(
                groups, "cross_asset", "aurora.indicator_groups.cross_asset"
            ),
        ),
        transition_monitoring=_feature_flag(
            payload, "transition_monitoring", "aurora.transition_monitoring"
        ),
    )


def _parse_supernova(payload: dict[str, Any]) -> SupernovaConfig:
    candidate_universe = _required_mapping(
        payload, "candidate_universe", "supernova.candidate_universe"
    )
    scoring = _required_mapping(payload, "scoring", "supernova.scoring")
    return SupernovaConfig(
        enabled=_required_bool(payload, "enabled", "supernova.enabled"),
        review_frequency=_enum(
            _required_str(payload, "review_frequency", "supernova.review_frequency"),
            {"monthly"},
            "supernova.review_frequency",
        ),
        framework=_enum(
            _required_str(payload, "framework", "supernova.framework"),
            {"five_d"},
            "supernova.framework",
        ),
        approved_companies=_tuple_of_str(
            payload, "approved_companies", "supernova.approved_companies"
        ),
        candidate_universe=CandidateUniverseConfig(
            source=_required_str(
                candidate_universe,
                "source",
                "supernova.candidate_universe.source",
            )
        ),
        replacement_policy=_feature_flag(
            payload, "replacement_policy", "supernova.replacement_policy"
        ),
        scoring=SupernovaScoringConfig(
            range=_required_str(scoring, "range", "supernova.scoring.range")
        ),
    )


def _parse_phoenix(payload: dict[str, Any]) -> PhoenixConfig:
    core_assets = _required_mapping(payload, "core_assets", "phoenix.core_assets")
    categories_payload = _required_mapping(payload, "categories", "phoenix.categories")
    categories = {}
    for name, category_payload in categories_payload.items():
        category = _ensure_mapping(category_payload, f"phoenix.categories.{name}")
        categories[name] = CategoryLeadershipConfig(
            leader=_required_str(
                category, "leader", f"phoenix.categories.{name}.leader"
            ),
            challenger=_required_str(
                category, "challenger", f"phoenix.categories.{name}.challenger"
            ),
        )

    return PhoenixConfig(
        enabled=_required_bool(payload, "enabled", "phoenix.enabled"),
        review_frequency=_enum(
            _required_str(payload, "review_frequency", "phoenix.review_frequency"),
            {"monthly"},
            "phoenix.review_frequency",
        ),
        core_assets=CoreAssetsConfig(
            btc_weight=_required_number(
                core_assets, "btc_weight", "phoenix.core_assets.btc_weight"
            ),
            eth_weight=_required_number(
                core_assets, "eth_weight", "phoenix.core_assets.eth_weight"
            ),
        ),
        portfolio_construction=_enum(
            _required_str(
                payload,
                "portfolio_construction",
                "phoenix.portfolio_construction",
            ),
            {"equal_weight"},
            "phoenix.portfolio_construction",
        ),
        categories=categories,
        replacement_policy=_feature_flag(
            payload, "replacement_policy", "phoenix.replacement_policy"
        ),
        leadership_monitoring=_feature_flag(
            payload, "leadership_monitoring", "phoenix.leadership_monitoring"
        ),
    )


def _feature_flag(payload: dict[str, Any], key: str, path: str) -> FeatureFlagConfig:
    mapping = _required_mapping(payload, key, path)
    return FeatureFlagConfig(enabled=_required_bool(mapping, "enabled", f"{path}.enabled"))


def _required_mapping(payload: dict[str, Any], key: str, path: str) -> dict[str, Any]:
    value = _required(payload, key, path)
    return _ensure_mapping(value, path)


def _ensure_mapping(value: Any, path: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ConfigValidationError(f"{path} must be a mapping.")
    return value


def _required(payload: dict[str, Any], key: str, path: str) -> Any:
    if key not in payload:
        raise ConfigValidationError(f"Missing required configuration field: {path}")
    return payload[key]


def _required_str(payload: dict[str, Any], key: str, path: str) -> str:
    value = _required(payload, key, path)
    if not isinstance(value, str):
        raise ConfigValidationError(f"{path} must be a string.")
    return value


def _required_bool(payload: dict[str, Any], key: str, path: str) -> bool:
    value = _required(payload, key, path)
    if not isinstance(value, bool):
        raise ConfigValidationError(f"{path} must be a boolean.")
    return value


def _required_int(payload: dict[str, Any], key: str, path: str) -> int:
    value = _required(payload, key, path)
    if not isinstance(value, int) or isinstance(value, bool):
        raise ConfigValidationError(f"{path} must be an integer.")
    return value


def _optional_int(payload: dict[str, Any], key: str, path: str) -> int | None:
    value = _required(payload, key, path)
    if value is None:
        return None
    if not isinstance(value, int) or isinstance(value, bool):
        raise ConfigValidationError(f"{path} must be an integer or null.")
    return value


def _required_number(payload: dict[str, Any], key: str, path: str) -> float:
    value = _required(payload, key, path)
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ConfigValidationError(f"{path} must be a number.")
    return float(value)


def _tuple_of_str(payload: dict[str, Any], key: str, path: str) -> tuple[str, ...]:
    value = _required(payload, key, path)
    if not isinstance(value, list):
        raise ConfigValidationError(f"{path} must be a list.")
    if not all(isinstance(item, str) for item in value):
        raise ConfigValidationError(f"{path} must contain only strings.")
    return tuple(value)


def _enum(value: str, allowed: set[str], path: str) -> str:
    if value not in allowed:
        allowed_values = ", ".join(sorted(allowed))
        raise ConfigValidationError(
            f"{path} must be one of: {allowed_values}. Received: {value}"
        )
    return value
