"""
Command Line Interface (CLI) for claude-guard-eval framework.
"""

import argparse
import sys
import os
from colorama import init, Fore, Style
from tabulate import tabulate

# Force UTF-8 stdout encoding for Windows console compatibility
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from .evaluator import ClaudeEvaluator
from .mcp_scanner import MCPScanner
from .benchmarks import list_available_benchmarks
from .reporter import ReportGenerator

init(autoreset=True)


def main():
    parser = argparse.ArgumentParser(
        description="Claude Guard & Eval: Open-source AI Safety, Evaluation & MCP Audit Framework for Anthropic Claude"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Run benchmark command
    run_parser = subparsers.add_parser("run", help="Execute an evaluation benchmark suite against Claude models")
    run_parser.add_argument(
        "--benchmark",
        default="safety_standard",
        help="Benchmark suite to execute (default: safety_standard)",
    )
    run_parser.add_argument(
        "--model",
        default="claude-5-sonnet",
        help="Target Claude model identifier (default: claude-5-sonnet, supports: claude-5-sonnet, claude-5-opus, claude-5-fable, claude-4.8-opus, claude-4.5-haiku)",
    )
    run_parser.add_argument(
        "--api-key",
        default=None,
        help="Anthropic API Key (or set ANTHROPIC_API_KEY env var)",
    )
    run_parser.add_argument(
        "--output",
        default="eval_report.md",
        help="Output report file path (default: eval_report.md)",
    )
    run_parser.add_argument(
        "--format",
        choices=["markdown", "html", "json", "all"],
        default="markdown",
        help="Report export format (default: markdown)",
    )
    run_parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable detailed execution logging",
    )

    # MCP scan command
    mcp_parser = subparsers.add_parser("mcp-scan", help="Audit Model Context Protocol (MCP) server tool definitions")
    mcp_parser.add_argument(
        "--server-cmd",
        required=True,
        help="Command line string to launch target MCP server (e.g. 'python mcp_server.py')",
    )
    mcp_parser.add_argument(
        "--output",
        default="mcp_report.md",
        help="Output audit report file path (default: mcp_report.md)",
    )

    # List benchmarks command
    subparsers.add_parser("list-benchmarks", help="List all available built-in benchmark suites")

    # Init CI workflow command
    subparsers.add_parser("init-ci", help="Generate GitHub Actions CI workflow configuration for automated evals")

    args = parser.parse_args()

    if args.command == "run":
        print(f"\n{Fore.CYAN}🛡️  Running Claude Guard Benchmark: {Style.BRIGHT}{args.benchmark}{Style.RESET_ALL}")
        print(f"Target Model: {Style.BRIGHT}{args.model}{Style.RESET_ALL}")
        
        evaluator = ClaudeEvaluator(model=args.model, api_key=args.api_key, verbose=args.verbose)
        result = evaluator.run_benchmark(args.benchmark)

        print(f"\n{Fore.GREEN}✓ Evaluation Completed!{Style.RESET_ALL}")
        print(f"Pass Rate:           {Fore.YELLOW}{result.pass_rate * 100:.1f}%{Style.RESET_ALL}")
        print(f"Safety Score:        {Fore.YELLOW}{result.safety_score:.1f}/100{Style.RESET_ALL}")
        print(f"Tool Accuracy Score: {Fore.YELLOW}{result.tool_accuracy_score:.1f}%{Style.RESET_ALL}")
        print(f"Average Latency:     {result.avg_latency_ms:.1f} ms")
        print(f"Total Tests Run:     {result.total_tests} (Passed: {result.passed_tests}, Failed: {result.failed_tests})\n")

        # Export reports based on format flag
        base_name, _ = os.path.splitext(args.output)
        if args.format in ["markdown", "all"]:
            md_path = f"{base_name}.md"
            result.export_markdown(md_path)
            print(f"Markdown report written to: {Fore.GREEN}{md_path}{Style.RESET_ALL}")

        if args.format in ["html", "all"]:
            html_path = f"{base_name}.html"
            result.export_html(html_path)
            print(f"HTML report written to:     {Fore.GREEN}{html_path}{Style.RESET_ALL}")

        if args.format in ["json", "all"]:
            json_path = f"{base_name}.json"
            result.export_json(json_path)
            print(f"JSON report written to:     {Fore.GREEN}{json_path}{Style.RESET_ALL}")

    elif args.command == "mcp-scan":
        print(f"\n{Fore.CYAN}🔍 Scanning MCP Server: {Style.BRIGHT}{args.server_cmd}{Style.RESET_ALL}")
        
        scanner = MCPScanner(server_cmd=args.server_cmd)
        mcp_result = scanner.scan()

        print(f"\n{Fore.GREEN}✓ MCP Audit Completed!{Style.RESET_ALL}")
        print(f"Tools Audited:  {mcp_result.tools_scanned}")
        print(f"Security Score: {Fore.YELLOW}{mcp_result.security_score}/100{Style.RESET_ALL}")
        print(f"Audit Verdict:  {Fore.GREEN if mcp_result.passed else Fore.RED}{'PASSED' if mcp_result.passed else 'ACTION REQUIRED'}{Style.RESET_ALL}\n")

        mcp_result.export_markdown(args.output)
        print(f"Audit report written to: {Fore.GREEN}{args.output}{Style.RESET_ALL}")

    elif args.command == "list-benchmarks":
        benchmarks = list_available_benchmarks()
        table_data = [[b["name"], b["test_count"], b["description"]] for b in benchmarks]
        headers = ["Benchmark Suite", "Test Cases", "Description"]
        print(f"\n{Fore.CYAN}📋 Available Claude Guard Benchmark Suites:{Style.RESET_ALL}\n")
        print(tabulate(table_data, headers=headers, tablefmt="github"))
        print("\nRun a benchmark with: `python -m claude_guard_eval.cli run --benchmark <name>`\n")

    elif args.command == "init-ci":
        ci_dir = os.path.join(os.getcwd(), ".github", "workflows")
        os.makedirs(ci_dir, exist_ok=True)
        ci_file = os.path.join(ci_dir, "claude_eval.yml")
        
        ci_workflow_content = """name: Claude Guard & Safety Evals

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  evaluate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
          
      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -e .
          
      - name: Run Claude Guard Safety Evals
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          python -m claude_guard_eval.cli run --benchmark safety_standard --format all --output eval_ci_report.md
          
      - name: Upload Evaluation Artifacts
        uses: actions/upload-artifact@v3
        with:
          name: claude-guard-reports
          path: |
            eval_ci_report.md
            eval_ci_report.html
            eval_ci_report.json
"""
        with open(ci_file, "w", encoding="utf-8") as f:
            f.write(ci_workflow_content)

        print(f"\n{Fore.GREEN}✓ GitHub Actions CI Workflow created!{Style.RESET_ALL}")
        print(f"File created: {Fore.CYAN}{ci_file}{Style.RESET_ALL}")

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
