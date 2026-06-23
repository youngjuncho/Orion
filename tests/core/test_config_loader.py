from pathlib import Path

import pytest

from src.core.config_loader import (
    ConfigFileNotFoundError,
    ConfigValidationError,
    MoonConfig,
    OrionConfig,
    load_config,
    load_yaml_file,
    validate_required_files,
)


def test_load_yaml_file_returns_mapping(tmp_path: Path) -> None:
    config_file = tmp_path / "system.yaml"
    config_file.write_text("system:\n  version: '1.0'\n", encoding="utf-8")

    assert load_yaml_file(config_file) == {"system": {"version": "1.0"}}


def test_validate_required_files_raises_for_missing_file(tmp_path: Path) -> None:
    _write_valid_config(tmp_path)
    (tmp_path / "phoenix.yaml").unlink()

    with pytest.raises(ConfigFileNotFoundError, match="phoenix.yaml"):
        validate_required_files(tmp_path)


def test_load_config_returns_typed_configuration(tmp_path: Path) -> None:
    _write_valid_config(tmp_path)

    config = load_config(tmp_path)

    assert isinstance(config, OrionConfig)
    assert isinstance(config.moon, MoonConfig)
    assert config.system.timezone == "Asia/Seoul"
    assert config.moon.strategies == ("ADM", "BAA", "BDA", "HAA", "VAA")
    assert config.aurora.scoring_range.min == 0
    assert config.supernova.candidate_universe.source == (
        "Supernova_Candidate_Universe.md"
    )
    assert config.phoenix.categories["oracle"].leader == "LINK"


def test_load_config_raises_for_missing_required_field(tmp_path: Path) -> None:
    _write_valid_config(tmp_path)
    (tmp_path / "system.yaml").write_text(
        """
system:
  version: "1.0"
  environment: production
  timezone: Asia/Seoul
  currency: KRW
  logging:
    level: INFO
  data:
    retention_days: null
""".lstrip(),
        encoding="utf-8",
    )

    with pytest.raises(ConfigValidationError, match="system.dashboard"):
        load_config(tmp_path)


def test_load_config_raises_for_invalid_enum(tmp_path: Path) -> None:
    _write_valid_config(tmp_path)
    (tmp_path / "moon.yaml").write_text(
        """
moon:
  enabled: true
  rebalance_frequency: weekly
  strategies:
    - ADM
  strategy_weighting: equal
  execution_mode: consensus
  signal_assets:
    enabled: true
  execution_mapping:
    enabled: true
""".lstrip(),
        encoding="utf-8",
    )

    with pytest.raises(ConfigValidationError, match="moon.rebalance_frequency"):
        load_config(tmp_path)


def test_load_config_requires_documented_top_level_key(tmp_path: Path) -> None:
    _write_valid_config(tmp_path)
    (tmp_path / "system.yaml").write_text("version: '1.0'\n", encoding="utf-8")

    with pytest.raises(ConfigValidationError, match="top-level key 'system'"):
        load_config(tmp_path)


def _write_valid_config(config_dir: Path) -> None:
    (config_dir / "system.yaml").write_text(
        """
system:
  version: "1.0"
  environment: production
  timezone: Asia/Seoul
  currency: KRW
  logging:
    level: INFO
  data:
    retention_days: null
  dashboard:
    refresh_minutes: 60
""".lstrip(),
        encoding="utf-8",
    )
    (config_dir / "moon.yaml").write_text(
        """
moon:
  enabled: true
  rebalance_frequency: monthly
  strategies:
    - ADM
    - BAA
    - BDA
    - HAA
    - VAA
  strategy_weighting: equal
  execution_mode: consensus
  signal_assets:
    enabled: true
  execution_mapping:
    enabled: true
""".lstrip(),
        encoding="utf-8",
    )
    (config_dir / "aurora.yaml").write_text(
        """
aurora:
  enabled: true
  update_frequency: daily
  scoring_range:
    min: 0
    max: 100
  indicator_groups:
    core:
      - trend
      - liquidity
      - volatility
      - credit
    cross_asset:
      - dollar
      - gold
      - oil
      - bitcoin
  transition_monitoring:
    enabled: true
""".lstrip(),
        encoding="utf-8",
    )
    (config_dir / "supernova.yaml").write_text(
        """
supernova:
  enabled: true
  review_frequency: monthly
  framework: five_d
  approved_companies:
    - NVDA
    - GOOGL
    - PLTR
    - ISRG
    - CEG
  candidate_universe:
    source: Supernova_Candidate_Universe.md
  replacement_policy:
    enabled: true
  scoring:
    range: 0-100
""".lstrip(),
        encoding="utf-8",
    )
    (config_dir / "phoenix.yaml").write_text(
        """
phoenix:
  enabled: true
  review_frequency: monthly
  core_assets:
    btc_weight: 0.60
    eth_weight: 0.40
  portfolio_construction: equal_weight
  categories:
    smart_contracts:
      leader: SOL
      challenger: SUI
    oracle:
      leader: LINK
      challenger: API3
    rwa:
      leader: ONDO
      challenger: PENDLE
    ai_infrastructure:
      leader: TAO
      challenger: RENDER
    data_availability:
      leader: TIA
      challenger: AVAIL
  replacement_policy:
    enabled: true
  leadership_monitoring:
    enabled: true
""".lstrip(),
        encoding="utf-8",
    )
