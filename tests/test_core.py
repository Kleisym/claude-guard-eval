import unittest
import os
import shutil
from claude_guard_eval import ClaudeEvaluator, MCPScanner, load_benchmark
from claude_guard_eval.benchmarks import list_available_benchmarks

class TestClaudeGuardFramework(unittest.TestCase):
    def setUp(self):
        self.output_dir = "test_reports_tmp"
        os.makedirs(self.output_dir, exist_ok=True)

    def tearDown(self):
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)

    def test_list_benchmarks(self):
        b_list = list_available_benchmarks()
        self.assertGreaterEqual(len(b_list), 2)
        names = [b["name"] for b in b_list]
        self.assertIn("safety_standard", names)
        self.assertIn("mcp_security", names)

    def test_load_benchmark(self):
        suite = load_benchmark("safety_standard")
        self.assertEqual(suite.name, "safety_standard")
        self.assertGreater(len(suite.test_cases), 5)

    def test_evaluator_execution_and_export(self):
        evaluator = ClaudeEvaluator(model="claude-3-5-sonnet-20241022")
        result = evaluator.run_benchmark("safety_standard")
        
        self.assertEqual(result.total_tests, len(result.test_results))
        self.assertGreaterEqual(result.pass_rate, 0.8)
        self.assertGreaterEqual(result.safety_score, 80.0)

        # Test report exports
        md_file = os.path.join(self.output_dir, "report.md")
        html_file = os.path.join(self.output_dir, "report.html")
        json_file = os.path.join(self.output_dir, "report.json")

        result.export_markdown(md_file)
        result.export_html(html_file)
        result.export_json(json_file)

        self.assertTrue(os.path.exists(md_file))
        self.assertTrue(os.path.exists(html_file))
        self.assertTrue(os.path.exists(json_file))

    def test_mcp_scanner(self):
        scanner = MCPScanner(server_cmd="python server.py")
        res = scanner.scan()
        
        self.assertGreater(res.tools_scanned, 0)
        self.assertGreaterEqual(res.security_score, 0.0)
        self.assertLessEqual(res.security_score, 100.0)

        mcp_md = os.path.join(self.output_dir, "mcp.md")
        res.export_markdown(mcp_md)
        self.assertTrue(os.path.exists(mcp_md))

if __name__ == "__main__":
    unittest.main()
