"""Moon ETF allocation framework."""
from .adm import ADM_RISK_ASSETS, ADMSignalInput, ADMStrategy, calculate_adjusted_price_return
from .consensus import ConsensusAllocator
from .engine import MoonEngine
from .execution import DOCUMENTED_EXECUTION_MAPPING, ExecutionMapper
from .main import run_report
from .models import ConsensusAllocation, MoonReport, Strategy, StrategyResult

__all__ = [
    "ADM_RISK_ASSETS", "ADMSignalInput", "ADMStrategy", "calculate_adjusted_price_return",
    "ConsensusAllocator", "ConsensusAllocation", "DOCUMENTED_EXECUTION_MAPPING", "ExecutionMapper",
    "MoonEngine", "MoonReport", "Strategy", "StrategyResult", "run_report",
]
