# Claude Guard & Eval Framework (`claude-guard-eval`)

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Anthropic Claude](https://img.shields.io/badge/Powered%20By-Anthropic%20Claude-orange.svg)](https://anthropic.com)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io)

> **An Open-Source Automated Evaluation, Security Guardrail & MCP Testing Suite for Anthropic Claude Agents.**

`claude-guard-eval` is a developer toolkit designed to evaluate, red-team, and continuously audit AI agents powered by Claude. It provides standardized benchmarks for tool-use accuracy, prompt injection resilience, hallucination detection, and Model Context Protocol (MCP) schema & security verification.

---

## 🌟 Key Features

- 🛡️ **MCP Security & Schema Scanner**: Automatically test Model Context Protocol (MCP) server endpoints for tool injection vulnerability, schema leaks, and execution safety.
- 🎯 **Tool-Use & Function Calling Evals**: Quantify how reliably Claude models invoke tool calls under complex multi-step user scenarios.
- ⚡ **Prompt Injection Resilience Benchmarks**: Test agent immunity against direct and indirect prompt injection attempts.
- 📊 **Automated Report Generation**: Output clean HTML, Markdown, and JSON evaluation reports with granular safety scores.
- 🚀 **CI/CD Integration Ready**: Integrate easily with GitHub Actions to run evals on every pull request.

---

## 📦 Installation

```bash
pip install claude-guard-eval
```

Or install from source:

```bash
git clone https://github.com/YOUR_USERNAME/claude-guard-eval.git
cd claude-guard-eval
pip install -e .
```

---

## 🚀 Quickstart

### 1. Set up your Anthropic API Key

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

### 2. Run a Built-in Safety & Tool Eval Benchmark

```bash
claude-guard run --benchmark safety_standard --model claude-3-5-sonnet-20241022
```

### 3. Audit an MCP (Model Context Protocol) Server

```bash
claude-guard mcp-scan --server-cmd "python my_mcp_server.py"
```

---

## 🛠️ Python Usage

```python
from claude_guard_eval import ClaudeEvaluator, MCPScanner

# Initialize evaluator with target model
evaluator = ClaudeEvaluator(model="claude-3-5-sonnet-20241022")

# Run safety injection benchmark suite
results = evaluator.run_benchmark("prompt_injection_v1")

print(f"Pass Rate: {results.pass_rate * 100:.1f}%")
print(f"Safety Score: {results.safety_score}/100")

# Generate Markdown audit report
results.export_markdown("report.md")
```

---

## 📁 Project Structure

```
claude-guard-eval/
├── claude_guard_eval/
│   ├── __init__.py
│   ├── cli.py          # Command line interface
│   ├── evaluator.py    # Core evaluation engine
│   ├── mcp_scanner.py  # Model Context Protocol security & schema validator
│   ├── benchmarks.py   # Built-in eval datasets (safety, tools, reasoning)
│   └── reporter.py     # HTML / MD report generator
├── tests/
│   └── test_core.py    # Unit tests
├── pyproject.toml
└── README.md
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
