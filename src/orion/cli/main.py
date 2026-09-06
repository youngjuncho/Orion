"""Orion command-line entry point."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import Callable

from orion.dashboard import render_dashboard
from orion.frameworks.aurora.main import run_report as run_aurora_report
from orion.frameworks.moon.main import run_report as run_moon_report
from orion.frameworks.phoenix.main import run_report as run_phoenix_report
from orion.frameworks.supernova.main import run_report as run_supernova_report


Handler = Callable[[argparse.Namespace], int]


@dataclass(frozen=True)
class CommandSpec:
    name: str
    help: str
    handler: Handler


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="orion")
    subparsers = parser.add_subparsers(dest="command", required=True)

    _add_simple_command(subparsers, "version", "Print Orion version.", _handle_version)
    _add_simple_command(subparsers, "health", "Run a health check.", _handle_health)
    _add_simple_command(subparsers, "config", "Show configuration status.", _handle_config)
    _add_simple_command(subparsers, "dashboard", "Open the Orion dashboard.", _handle_dashboard)

    data = subparsers.add_parser("data", help="Data operations.")
    data_sub = data.add_subparsers(dest="data_command", required=True)
    _add_simple_command(data_sub, "update", "Update all data.", _handle_data_update)
    _add_simple_command(data_sub, "status", "Check data status.", _handle_data_status)

    for framework in ("moon", "aurora", "supernova", "phoenix"):
        framework_parser = subparsers.add_parser(framework, help=f"{framework.title()} commands.")
        framework_sub = framework_parser.add_subparsers(dest=f"{framework}_command", required=True)
        _add_simple_command(framework_sub, "report", f"Show {framework} report.", _make_framework_report_handler(framework))

        if framework == "moon":
            _add_simple_command(framework_sub, "run", "Run Moon.", _make_framework_handler(framework, "run"))
            _add_simple_command(
                framework_sub,
                "allocation",
                "Show Moon allocation.",
                _make_framework_handler(framework, "allocation"),
            )
        elif framework == "aurora":
            _add_simple_command(framework_sub, "regime", "Show Aurora regime.", _make_framework_handler(framework, "regime"))
            _add_simple_command(
                framework_sub,
                "indicators",
                "Show Aurora indicators.",
                _make_framework_handler(framework, "indicators"),
            )
        elif framework == "supernova":
            _add_simple_command(framework_sub, "leaders", "Show Supernova leaders.", _make_framework_handler(framework, "leaders"))
            _add_simple_command(
                framework_sub,
                "watchlist",
                "Show Supernova watchlist.",
                _make_framework_handler(framework, "watchlist"),
            )
        elif framework == "phoenix":
            _add_simple_command(framework_sub, "leaders", "Show Phoenix leaders.", _make_framework_handler(framework, "leaders"))
            _add_simple_command(
                framework_sub,
                "categories",
                "Show Phoenix categories.",
                _make_framework_handler(framework, "categories"),
            )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    handler = getattr(args, "handler", None)
    if handler is None:
        parser.error("missing handler")
    return handler(args)


def _add_simple_command(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    name: str,
    help_text: str,
    handler: Handler,
) -> None:
    parser = subparsers.add_parser(name, help=help_text)
    parser.set_defaults(handler=handler)


def _handle_version(_: argparse.Namespace) -> int:
    print("Orion v1")
    return 0


def _handle_health(_: argparse.Namespace) -> int:
    print("Orion health: not yet implemented")
    return 0


def _handle_config(_: argparse.Namespace) -> int:
    print("Orion config: loaded")
    return 0


def _handle_dashboard(_: argparse.Namespace) -> int:
    return render_dashboard()


def _handle_data_update(_: argparse.Namespace) -> int:
    print("Orion data update: not yet implemented")
    return 0


def _handle_data_status(_: argparse.Namespace) -> int:
    print("Orion data status: not yet implemented")
    return 0


def _make_framework_handler(framework: str, action: str) -> Handler:
    def _handler(_: argparse.Namespace) -> int:
        print(f"{framework} {action}: not yet implemented")
        return 0

    return _handler


def _make_framework_report_handler(framework: str) -> Handler:
    handlers: dict[str, Callable[[], int]] = {
        "moon": run_moon_report,
        "aurora": run_aurora_report,
        "supernova": run_supernova_report,
        "phoenix": run_phoenix_report,
    }

    def _handler(_: argparse.Namespace) -> int:
        return handlers[framework]()

    return _handler
