"""
Claude Guard & Eval Framework (`claude-guard-eval`)
An Open-Source Automated Evaluation, Security Guardrail & MCP Testing Suite for Anthropic Claude Agents.
"""

from .evaluator import ClaudeEvaluator, EvalResult
from .mcp_scanner import MCPScanner, MCPScanResult
from .benchmarks import BenchmarkSuite, load_benchmark
from .reporter import ReportGenerator

__version__ = "0.1.0"
__all__ = [
    "ClaudeEvaluator",
    "EvalResult",
    "MCPScanner",
    "MCPScanResult",
    "BenchmarkSuite",
    "load_benchmark",
    "ReportGenerator",
]
