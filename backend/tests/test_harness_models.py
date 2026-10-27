import pytest
from app.harness.models import (
    EvaluationMetric,
    EvaluationResult,
    TestCase,
    BenchmarkSuiteResult,
    HarnessStatus
)

def test_evaluation_metric_creation():
    metric = EvaluationMetric(
        name="html5_compliance",
        score=30,
        max_score=30,
        passed=True,
        description="Contains valid DOCTYPE, html, head, body tags"
    )
    assert metric.name == "html5_compliance"
    assert metric.score == 30
    assert metric.passed is True


def test_evaluation_result_scoring():
    metric1 = EvaluationMetric(name="m1", score=50, max_score=50, passed=True)
    metric2 = EvaluationMetric(name="m2", score=35, max_score=50, passed=False, description="Minor issue")

    result = EvaluationResult(
        agent_name="coder",
        test_case_id="b2b_saas",
        status=HarnessStatus.PASS,
        score=85.0,
        metrics=[metric1, metric2],
        issues=["Minor issue in m2"],
        latency_sec=2.1,
        output_summary="Generated single-file HTML5"
    )
    assert result.agent_name == "coder"
    assert result.score == 85.0
    assert result.status == HarnessStatus.PASS
    assert len(result.issues) == 1
    assert result.passed is True


def test_test_case_schema():
    case = TestCase(
        id="b2b_saas",
        industry="B2B SaaS",
        prompt="TalentAI - AI Recruitment Platform",
        brief_answers={
            "target_audience": "Tech Recruiter & HR Leaders",
            "brand_style": "Modern Tech",
            "conversion_goal": "Book a Demo"
        }
    )
    assert case.id == "b2b_saas"
    assert case.industry == "B2B SaaS"
    assert "target_audience" in case.brief_answers


def test_benchmark_suite_result():
    res1 = EvaluationResult(
        agent_name="ba_analyst",
        test_case_id="b2b_saas",
        status=HarnessStatus.PASS,
        score=90.0,
        metrics=[]
    )
    res2 = EvaluationResult(
        agent_name="coder",
        test_case_id="b2b_saas",
        status=HarnessStatus.PASS,
        score=85.0,
        metrics=[]
    )
    suite = BenchmarkSuiteResult(
        total_cases=2,
        passed_cases=2,
        failed_cases=0,
        average_score=87.5,
        total_time_sec=4.2,
        results=[res1, res2]
    )
    assert suite.total_cases == 2
    assert suite.passed_cases == 2
    assert suite.average_score == 87.5
