from types import SimpleNamespace

from orion.core import FrameworkResult, Score, make_report_adapter
from orion.core.runtime import RuntimeContext


def test_report_adapter_maps_framework_report_to_canonical_result():
    adapter = make_report_adapter("Aurora", lambda: SimpleNamespace(score=None))
    result = adapter(None)  # type: ignore[arg-type]
    assert isinstance(result, FrameworkResult)
    assert result.framework_name == "Aurora"
    assert result.execution_status == "Completed"


def test_report_adapter_maps_phoenix_score_without_changing_domain_model():
    adapter = make_report_adapter("Phoenix", lambda: SimpleNamespace(phoenix_score=Score(7)))
    result = adapter(None)  # type: ignore[arg-type]
    assert result.score.value == 7


def test_satellite_report_adapters_preserve_framework_boundary():
    from orion.frameworks.supernova import SupernovaEngine
    from orion.frameworks.phoenix import PhoenixEngine

    supernova = make_report_adapter("Supernova", SupernovaEngine().build_report)(None)  # type: ignore[arg-type]
    phoenix = make_report_adapter("Phoenix", PhoenixEngine().build_report)(None)  # type: ignore[arg-type]

    assert supernova.framework_name == "Supernova"
    assert supernova.execution_status == "Completed"
    assert phoenix.framework_name == "Phoenix"
    assert phoenix.execution_status == "Completed"
    assert phoenix.score.value == 0


def test_satellite_report_adapters_do_not_create_portfolio_decisions():
    from orion.frameworks.supernova import SupernovaEngine
    from orion.frameworks.phoenix import PhoenixEngine

    supernova = make_report_adapter("Supernova", SupernovaEngine().build_report)(None)  # type: ignore[arg-type]
    phoenix = make_report_adapter("Phoenix", PhoenixEngine().build_report)(None)  # type: ignore[arg-type]

    assert supernova.decision_candidates == ()
    assert phoenix.decision_candidates == ()
