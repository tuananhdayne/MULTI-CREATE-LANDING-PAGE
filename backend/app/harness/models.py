from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class HarnessStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    WARN = "WARN"


class EvaluationMetric(BaseModel):
    name: str = Field(..., description="Name of the evaluated metric")
    score: float = Field(..., description="Score awarded for this metric")
    max_score: float = Field(..., description="Maximum possible score for this metric")
    passed: bool = Field(..., description="Whether this criterion passed")
    description: Optional[str] = Field(default=None, description="Details or failure reason")


class EvaluationResult(BaseModel):
    agent_name: str = Field(..., description="Name of the agent under evaluation")
    test_case_id: str = Field(..., description="Identifier of the benchmark test case")
    status: HarnessStatus = Field(default=HarnessStatus.PASS, description="Pass/Fail status")
    score: float = Field(..., description="Overall score out of 100")
    metrics: List[EvaluationMetric] = Field(default_factory=list, description="Breakdown of scored criteria")
    issues: List[str] = Field(default_factory=list, description="List of detected defects or warnings")
    latency_sec: float = Field(default=0.0, description="Execution duration in seconds")
    output_summary: str = Field(default="", description="Human-readable preview of agent output")
    raw_output: Optional[Any] = Field(default=None, description="Raw returned artifact for inspection")

    @property
    def passed(self) -> bool:
        return self.status != HarnessStatus.FAIL and self.score >= 80.0


class TestCase(BaseModel):
    __test__ = False
    id: str = Field(..., description="Unique case key (e.g. b2b_saas)")
    industry: str = Field(..., description="Business domain or category")
    prompt: str = Field(..., description="Raw user prompt or campaign idea")
    brief_answers: Dict[str, str] = Field(default_factory=dict, description="Answers to clarifying questions")
    proposal: Optional[Dict[str, Any]] = Field(default=None, description="Approved proposal if testing phase 3")
    target_element: Optional[Dict[str, Any]] = Field(default=None, description="DOM element for Element Editor")
    tweak_instruction: Optional[str] = Field(default=None, description="Element modification instruction")
    initial_code: Optional[str] = Field(default=None, description="HTML code for QA or editor tests")


class BenchmarkSuiteResult(BaseModel):
    total_cases: int = Field(..., description="Total evaluated test cases")
    passed_cases: int = Field(..., description="Number of passed evaluations")
    failed_cases: int = Field(..., description="Number of failed evaluations")
    average_score: float = Field(..., description="Mean score across all evaluations (0-100)")
    total_time_sec: float = Field(..., description="Cumulative duration of the suite")
    results: List[EvaluationResult] = Field(default_factory=list, description="Detailed evaluation results")
