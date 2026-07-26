from src.cli.main import main


def test_dashboard_command_renders_summary(capsys) -> None:
    exit_code = main(["dashboard"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Orion Dashboard" in captured.out
    assert "Aurora:" in captured.out
    assert "Phoenix:" in captured.out
