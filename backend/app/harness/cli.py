import sys
import argparse
from pathlib import Path
from app.harness.runner import AgentHarness, ALL_AGENTS
from app.harness.fixtures import BENCHMARK_CASES
from app.harness.models import HarnessStatus


def main():
    parser = argparse.ArgumentParser(description="Multi-Agent Landing Page Builder - Test & Benchmark Harness")
    parser.add_argument("--agent", choices=ALL_AGENTS + ["all"], default="all", help="Target agent to evaluate")
    parser.add_argument("--case", choices=list(BENCHMARK_CASES.keys()) + ["all"], default="all", help="Benchmark case to run")
    parser.add_argument("--live", action="store_true", help="Execute live LLM & browser audits (instead of mock replay)")
    parser.add_argument("--report", type=str, default="", help="Path to write Markdown benchmark report")
    parser.add_argument("--json", type=str, default="", help="Path to write JSON benchmark results")

    args = parser.parse_args()

    agent_names = None if args.agent == "all" else [args.agent]
    case_keys = None if args.case == "all" else [args.case]

    print("\n" + "=" * 70)
    print("🚀 MULTI-AGENT TEST & BENCHMARK EVALUATION HARNESS")
    print(f"Mode: {'LIVE LLM & BROWSER' if args.live else 'MOCK REPLAY (CI/CD)'}")
    print(f"Agents: {args.agent} | Cases: {args.case}")
    print("=" * 70 + "\n")

    harness = AgentHarness()
    suite_res = harness.run_suite(agent_names=agent_names, cases=case_keys, live=args.live)

    # Print Terminal Table
    print(f"{'AGENT':<16} | {'CASE':<18} | {'SCORE':<7} | {'STATUS':<7} | {'TIME'}")
    print("-" * 70)
    for r in suite_res.results:
        status_colored = f"\033[92m{r.status.value}\033[0m" if r.status == HarnessStatus.PASS else f"\033[91m{r.status.value}\033[0m"
        print(f"{r.agent_name:<16} | {r.test_case_id:<18} | {r.score:<7.1f} | {status_colored:<16} | {r.latency_sec}s")
        if r.issues:
            print(f"   ↳ Issues: {'; '.join(r.issues)}")

    print("-" * 70)
    print(f"📊 Evaluated: {suite_res.total_cases} | Passed: {suite_res.passed_cases} | Failed: {suite_res.failed_cases}")
    print(f"🎯 Average Score: {suite_res.average_score} / 100 | Total Time: {suite_res.total_time_sec}s\n")

    # Generate Markdown Report
    if args.report:
        report_path = Path(args.report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        md_content = harness.generate_markdown_report(suite_res)
        report_path.write_text(md_content, encoding="utf-8")
        print(f"📝 Markdown benchmark report saved to: {report_path.resolve()}")

    if args.json:
        json_path = Path(args.json)
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(suite_res.model_dump_json(indent=2), encoding="utf-8")
        print(f"💾 JSON benchmark data saved to: {json_path.resolve()}")

    sys.exit(0 if suite_res.failed_cases == 0 else 1)


if __name__ == "__main__":
    main()
