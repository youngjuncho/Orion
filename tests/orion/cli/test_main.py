import pytest
from importlib import import_module

cli_main = import_module("orion.cli.main")
from orion.cli.main import main


@pytest.mark.parametrize(
    ("argv", "expected"),
    [
        (["version"], "Orion v1"),
        (["health"], "Orion health: not yet implemented"),
        (["config"], "Orion config: loaded"),
        (["data", "update"], "Orion data update: not yet implemented"),
        (["aurora", "indicators"], "aurora indicators: not yet implemented"),
        (["supernova", "watchlist"], "supernova watchlist: not yet implemented"),
        (["phoenix", "categories"], "phoenix categories: not yet implemented"),
    ],
)
def test_cli_commands_dispatch(argv, expected, capsys) -> None:
    exit_code = main(argv)
    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out.strip() == expected


def test_cli_requires_command() -> None:
    with pytest.raises(SystemExit):
        main([])


def test_config_command_reports_invalid_configuration(monkeypatch, capsys) -> None:
    def raise_config_error():
        raise cli_main.ConfigError("invalid test configuration")

    monkeypatch.setattr(cli_main, "load_config", raise_config_error)

    exit_code = main(["config"])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert captured.out.strip() == (
        "Orion config: invalid (invalid test configuration)"
    )


@pytest.mark.parametrize(
    ("argv", "expected_lines"),
    [
        (
            ["moon", "report"],
            (
                "Current Asset: Unknown",
                "Momentum State: Unknown",
                "Risk State: Unknown",
                "Next Rebalance Date: Unknown",
            ),
        ),
        (
            ["aurora", "report"],
            (
                "Aurora Score: 0",
                "Current Regime: Unknown",
                "Regime Direction: Stable",
                "Risk State: Unknown",
                "Transition Risk: Unknown",
            ),
        ),
        (
            ["supernova", "report"],
            (
                "Approved Companies: 5",
                "Theme Health: Unknown",
                "Leadership Status: Unknown",
                "Replacement Risk: Unknown",
            ),
        ),
        (
            ["phoenix", "report"],
            (
                "Phoenix Score: 0",
                "Categories: 5",
                "Current Leaders: 5",
                "Replacement Risk: Unknown",
            ),
        ),
    ],
)
def test_framework_report_commands_dispatch_to_entry_points(argv, expected_lines, capsys) -> None:
    exit_code = main(argv)
    captured = capsys.readouterr()

    assert exit_code == 0
    assert tuple(captured.out.strip().splitlines()) == expected_lines
