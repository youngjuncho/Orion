from pathlib import Path
import tempfile

import pytest

from orion.core.config_loader import (
    ConfigFileNotFoundError,
    ConfigValidationError,
    MoonConfig,
    OrionConfig,
    load_config,
    load_yaml_file,
    validate_required_files,
)


def test_load_yaml_file_returns_mapping() -> None:
    tmp_path = _temp_dir()
    config_file = tmp_path / "system.yaml"
    config_file.write_text("system:\n  version: '1.0'\n", encoding="utf-8")

    assert load_yaml_file(config_file) == {"system": {"version": "1.0"}}


def test_validate_required_files_raises_for_missing_file() -> None:
    tmp_path = _temp_dir()
    _write_valid_config(tmp_path)
    (tmp_path / "phoenix.yaml").unlink()

    with pytest.raises(ConfigFileNotFoundError, match="phoenix.yaml"):
        validate_required_files(tmp_path)


def test_load_config_returns_typed_configuration() -> None:
    tmp_path = _temp_dir()
    _write_valid_config(tmp_path)

    config = load_config(tmp_path)

    assert isinstance(config, OrionConfig)
    assert isinstance(config.moon, MoonConfig)
    assert config.system.timezone == "Asia/Seoul"
    assert config.moon.strategies == ("ADM", "BAA", "BDA", "HAA", "VAA")
    assert config.moon.active_strategies == ()
    assert config.aurora.scoring_range.min == 0
    assert config.supernova.candidate_universe.source == (
        "Supernova_Candidate_Universe.md"
    )
    assert config.phoenix.categories["oracle"].leader == "LINK"


def test_load_config_raises_for_missing_required_field() -> None:
    tmp_path = _temp_dir()
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


def test_load_config_raises_for_invalid_enum() -> None:
    tmp_path = _temp_dir()
    _write_valid_config(tmp_path)
    (tmp_path / "moon.yaml").write_text(
        """
moon:
  enabled: true
  rebalance_frequency: weekly
  strategies:
    - ADM
  active_strategies: []
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


def test_load_config_rejects_unregistered_active_strategy() -> None:
    tmp_path = _temp_dir()
    _write_valid_config(tmp_path)
    (tmp_path / "moon.yaml").write_text(
        """
moon:
  enabled: true
  rebalance_frequency: monthly
  strategies:
    - ADM
  active_strategies:
    - BAA
  strategy_weighting: equal
  execution_mode: consensus
  signal_assets:
    enabled: true
  execution_mapping:
    enabled: true
""".lstrip(),
        encoding="utf-8",
    )

    with pytest.raises(ConfigValidationError, match="unregistered"):
        load_config(tmp_path)


@pytest.mark.parametrize("field", ["strategies", "active_strategies"])
def test_load_config_rejects_duplicate_moon_strategy_names(field: str) -> None:
    tmp_path = _temp_dir()
    _write_valid_config(tmp_path)
    moon_file = tmp_path / "moon.yaml"
    content = moon_file.read_text(encoding="utf-8")
    if field == "strategies":
        content = content.replace("    - BAA\n", "    - BAA\n    - ADM\n", 1)
    else:
        content = content.replace(
            "  active_strategies: []", "  active_strategies: [ADM, ADM]"
        )
    moon_file.write_text(content, encoding="utf-8")

    with pytest.raises(ConfigValidationError, match=f"moon\\.{field}.*duplicate"):
        load_config(tmp_path)


def test_load_config_rejects_blank_moon_strategy_name() -> None:
    tmp_path = _temp_dir()
    _write_valid_config(tmp_path)
    moon_file = tmp_path / "moon.yaml"
    content = moon_file.read_text(encoding="utf-8").replace(
        "  active_strategies: []", "  active_strategies: ['   ']"
    )
    moon_file.write_text(content, encoding="utf-8")

    with pytest.raises(
        ConfigValidationError, match="moon.active_strategies.*non-empty"
    ):
        load_config(tmp_path)


def test_load_config_requires_documented_top_level_key() -> None:
    tmp_path = _temp_dir()
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
  active_strategies: []
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


def _temp_dir() -> Path:
    base = Path.cwd() / "test_tmp"
    base.mkdir(parents=True, exist_ok=True)
    return Path(tempfile.mkdtemp(prefix="config-", dir=base))
