import pytest
from app.harness.runner import AgentHarness
from app.harness.fixtures import BENCHMARK_CASES
from app.harness.models import HarnessStatus, BenchmarkSuiteResult


def test_harness_run_single_agent_mock():
    harness = AgentHarness()
    case = BENCHMARK_CASES["b2b_saas"]
    res = harness.run_agent("coder", case, live=False)
    assert res.agent_name == "coder"
    assert res.test_case_id == "b2b_saas"
    assert res.status == HarnessStatus.PASS
    assert res.score >= 85.0
    assert res.latency_sec >= 0.0


def test_harness_run_suite_mock():
    harness = AgentHarness()
    suite_res = harness.run_suite(cases=["b2b_saas", "ecommerce_fashion"], live=False)
    assert isinstance(suite_res, BenchmarkSuiteResult)
    assert suite_res.total_cases > 0
    assert suite_res.passed_cases == suite_res.total_cases
    assert suite_res.failed_cases == 0
    assert suite_res.average_score >= 85.0


def test_harness_generate_markdown_report():
    harness = AgentHarness()
    suite_res = harness.run_suite(cases=["b2b_saas"], live=False)
    md_report = harness.generate_markdown_report(suite_res)
    assert "# Multi-Agent Benchmark Evaluation Report" in md_report
    assert "coder" in md_report.lower()
    assert "Average Score" in md_report or "Điểm Trung Bình" in md_report
