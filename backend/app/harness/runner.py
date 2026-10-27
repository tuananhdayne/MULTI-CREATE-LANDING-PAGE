import time
import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

from app.harness.models import (
    TestCase,
    EvaluationResult,
    BenchmarkSuiteResult,
    HarnessStatus
)
from app.harness.fixtures import BENCHMARK_CASES, MOCK_AGENT_OUTPUTS
from app.harness.rubrics import (
    evaluate_ba_analyst,
    evaluate_proposal,
    evaluate_strategist,
    evaluate_copywriter,
    evaluate_designer,
    evaluate_coder,
    evaluate_visual_qa,
    evaluate_element_editor
)

logger = logging.getLogger("AgentHarness")

ALL_AGENTS = [
    "ba_analyst", "proposal", "strategist", "copywriter",
    "designer", "coder", "visual_qa", "element_editor"
]


class AgentHarness:
    """
    Test and Benchmark Evaluation Harness runner for 8 Landing Page Builder agents.
    Supports deterministic mock execution (for CI/CD testing) and live LLM sandboxing.
    """
    def __init__(self, benchmark_cases: Optional[Dict[str, TestCase]] = None):
        self.cases = benchmark_cases or BENCHMARK_CASES

    def run_agent(self, agent_name: str, case: TestCase, live: bool = False) -> EvaluationResult:
        """Executes a single agent in an isolated sandbox and evaluates it against rubrics."""
        start_time = time.time()

        if not live:
            raw_output = MOCK_AGENT_OUTPUTS.get(agent_name)
            latency = round(time.time() - start_time, 3)
            return self._evaluate_output(agent_name, raw_output, case, latency)

        # Live execution sandbox
        try:
            raw_output = self._execute_live_agent(agent_name, case)
            latency = round(time.time() - start_time, 2)
            return self._evaluate_output(agent_name, raw_output, case, latency)
        except Exception as e:
            logger.error(f"Error executing agent {agent_name} live: {e}", exc_info=True)
            latency = round(time.time() - start_time, 2)
            return EvaluationResult(
                agent_name=agent_name,
                test_case_id=case.id,
                status=HarnessStatus.FAIL,
                score=0.0,
                metrics=[],
                issues=[f"Execution exception: {str(e)}"],
                latency_sec=latency,
                output_summary=f"Crashed with: {str(e)}"
            )

    def _execute_live_agent(self, agent_name: str, case: TestCase) -> Any:
        """Invokes the specific agent with live LLM / Playwright in an isolated state."""
        if agent_name == "ba_analyst":
            from app.agents.ba_analyst import BAAnalystAgent
            agent = BAAnalystAgent()
            return asyncio.run(agent.generate_questions(case.prompt))

        elif agent_name == "proposal":
            from app.agents.proposal_agent import ProposalAgent
            agent = ProposalAgent()
            return asyncio.run(agent.generate_proposal(case.prompt, case.brief_answers))

        elif agent_name == "strategist":
            from app.agents.strategist import strategist_node
            state = {"prompt": case.prompt, "theme": "auto", "messages": []}
            res = strategist_node(state)
            return res.get("outline", "")

        elif agent_name == "copywriter":
            from app.agents.copywriter import copywriter_node
            outline = MOCK_AGENT_OUTPUTS["strategist"]
            state = {"prompt": case.prompt, "outline": outline, "messages": []}
            res = copywriter_node(state)
            return res.get("copy", "")

        elif agent_name == "designer":
            from app.agents.designer import designer_node
            outline = MOCK_AGENT_OUTPUTS["strategist"]
            state = {"prompt": case.prompt, "theme": "auto", "outline": outline, "messages": []}
            res = designer_node(state)
            return res.get("design", "")

        elif agent_name == "coder":
            from app.agents.coder import coder_node
            state = {
                "prompt": case.prompt,
                "outline": MOCK_AGENT_OUTPUTS["strategist"],
                "copy": MOCK_AGENT_OUTPUTS["copywriter"],
                "design": MOCK_AGENT_OUTPUTS["designer"],
                "iteration": 0,
                "messages": []
            }
            res = coder_node(state)
            return res.get("code", "")

        elif agent_name == "visual_qa":
            from app.agents.visual_qa import visual_qa_node
            code = case.initial_code or MOCK_AGENT_OUTPUTS["coder"]
            state = {"code": code, "iteration": 0, "messages": []}
            return visual_qa_node(state)

        elif agent_name == "element_editor":
            from app.agents.element_editor import generate_element_tweak
            target_el = case.target_element or {
                "tag": "button",
                "element_id": "hero-cta-btn",
                "current_html": '<button id="hero-cta-btn" class="bg-blue-600 font-medium px-6 py-3 rounded-lg">Dùng Thử</button>'
            }
            instruction = case.tweak_instruction or "Đổi sang gradient cam bo tròn"
            return generate_element_tweak(target_el, instruction)

        raise ValueError(f"Unknown agent: {agent_name}")

    def _evaluate_output(self, agent_name: str, output: Any, case: TestCase, latency: float) -> EvaluationResult:
        """Dispatches agent output to the appropriate rubric evaluator."""
        cid = case.id
        if agent_name == "ba_analyst":
            return evaluate_ba_analyst(output, test_case_id=cid, latency_sec=latency)
        elif agent_name == "proposal":
            return evaluate_proposal(output, test_case_id=cid, latency_sec=latency)
        elif agent_name == "strategist":
            return evaluate_strategist(output, test_case_id=cid, latency_sec=latency)
        elif agent_name == "copywriter":
            return evaluate_copywriter(output, test_case_id=cid, latency_sec=latency)
        elif agent_name == "designer":
            return evaluate_designer(output, test_case_id=cid, latency_sec=latency)
        elif agent_name == "coder":
            return evaluate_coder(output, test_case_id=cid, latency_sec=latency)
        elif agent_name == "visual_qa":
            return evaluate_visual_qa(output, test_case_id=cid, latency_sec=latency)
        elif agent_name == "element_editor":
            target_el = case.target_element or {
                "tag": "button",
                "element_id": "hero-cta-btn",
                "current_html": '<button id="hero-cta-btn">Click</button>'
            }
            inst = case.tweak_instruction or "Đổi sang màu cam"
            return evaluate_element_editor(output, target_el, inst, test_case_id=cid, latency_sec=latency)

        raise ValueError(f"Unsupported agent name: {agent_name}")

    def run_suite(
        self,
        agent_names: Optional[List[str]] = None,
        cases: Optional[List[str]] = None,
        live: bool = False
    ) -> BenchmarkSuiteResult:
        """Executes selected agents across selected test cases."""
        selected_agents = agent_names or ALL_AGENTS
        selected_cases = [self.cases[k] for k in (cases or list(self.cases.keys())) if k in self.cases]

        results: List[EvaluationResult] = []
        suite_start = time.time()

        for case in selected_cases:
            for agent in selected_agents:
                logger.info(f"Harness running agent={agent} case={case.id} (live={live})")
                res = self.run_agent(agent, case, live=live)
                results.append(res)

        total_time = round(time.time() - suite_start, 2)
        total_evals = len(results)
        passed_evals = sum(1 for r in results if r.passed)
        failed_evals = total_evals - passed_evals
        avg_score = round(sum(r.score for r in results) / total_evals, 1) if total_evals > 0 else 0.0

        return BenchmarkSuiteResult(
            total_cases=total_evals,
            passed_cases=passed_evals,
            failed_cases=failed_evals,
            average_score=avg_score,
            total_time_sec=total_time,
            results=results
        )

    def generate_markdown_report(self, suite_res: BenchmarkSuiteResult) -> str:
        """Generates an executive Markdown benchmark report with summary tables."""
        now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        pass_rate = round((suite_res.passed_cases / suite_res.total_cases) * 100, 1) if suite_res.total_cases > 0 else 0.0

        md = f"""# Multi-Agent Benchmark Evaluation Report
**Generated At:** {now_str}  
**Overall Status:** {"✅ PASS" if suite_res.failed_cases == 0 else "⚠️ WARNING / FAILED"}  
**Average Score:** **{suite_res.average_score} / 100**  
**Pass Rate:** **{pass_rate}%** ({suite_res.passed_cases}/{suite_res.total_cases} passed)  
**Total Duration:** {suite_res.total_time_sec}s  

---

## 1. Executive Summary

| Metric | Value |
| :--- | :--- |
| **Total Test Evaluations** | {suite_res.total_cases} |
| **Passed Evaluations (>=80 pts)** | {suite_res.passed_cases} |
| **Failed Evaluations (<80 pts)** | {suite_res.failed_cases} |
| **Mean Benchmark Score** | **{suite_res.average_score} / 100** |
| **Cumulative Execution Time** | {suite_res.total_time_sec}s |

---

## 2. Detailed Agent Scorecard

| Agent Name | Test Case | Score | Status | Latency | Summary / Issues |
| :--- | :--- | :---: | :---: | :---: | :--- |
"""
        for r in suite_res.results:
            status_icon = "🟢 PASS" if r.status == HarnessStatus.PASS else "🔴 FAIL"
            summary = r.output_summary.replace("|", "/")
            issues_str = f" (Issues: {'; '.join(r.issues)})" if r.issues else ""
            md += f"| `{r.agent_name}` | `{r.test_case_id}` | **{r.score:.1f}** | {status_icon} | {r.latency_sec}s | {summary}{issues_str} |\n"

        md += "\n---\n*Report generated automatically by Antigravity Agent Test & Benchmark Evaluation Harness.*\n"
        return md
