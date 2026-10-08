from orion.cli.main import main
import importlib

cli_module = importlib.import_module("orion.cli.main")


def test_framework_report_commands_use_runtime_boundary(monkeypatch, capsys):
    called = []

    def fake_run(framework):
        called.append(framework)
        print("runtime report")
        return 0

    monkeypatch.setattr(cli_module, "run_framework_report", fake_run)
    assert main(["aurora", "report"]) == 0
    assert called == ["aurora"]
    assert "runtime report" in capsys.readouterr().out
