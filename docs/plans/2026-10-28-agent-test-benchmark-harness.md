# Agent Test & Benchmark Evaluation Harness Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Xây dựng hệ thống Agent Test & Benchmark Evaluation Harness hoàn chỉnh cho 8 Agent trong hệ thống Landing Page Builder: hỗ trợ chạy cô lập từng Agent (sandboxed execution), chấm điểm chất lượng tự động theo Rubrics (0–100 điểm), benchmark trên tập dữ liệu chuẩn đa ngành, và cung cấp CLI + Pytest Runner xuất báo cáo trực quan.

**Architecture:**
- `app.harness.models`: Định nghĩa các Pydantic schemas (`TestCase`, `EvaluationResult`, `BenchmarkSuiteResult`, `RubricScoreBreakdown`).
- `app.harness.rubrics`: Engine chấm điểm chuyên biệt cho 8 Agent (BA Analyst, Proposal, Strategist, Copywriter, Designer, Coder, Visual QA, Element Editor).
- `app.harness.fixtures`: Bộ dữ liệu benchmark chuẩn gồm 5 kịch bản (B2B SaaS, E-Commerce, Education, Creative Agency, Edge Cases).
- `app.harness.runner`: Core harness engine điều phối sandboxed execution (mock hoặc live LLM), tính toán điểm số và xuất báo cáo Markdown / JSON.
- `app.harness.cli` & `scripts/run_agent_benchmark.py`: Công cụ dòng lệnh chạy linh hoạt theo agent, theo test case, hoặc toàn bộ test suite.

**Spec:** [`docs/specs/2026-10-28-agent-test-benchmark-harness-design.md`](file:///home/tuananh/GEN_LANDING/docs/specs/2026-10-28-agent-test-benchmark-harness-design.md)

---

## Global Constraints
- Tuân thủ quy định bảo mật: không in hoặc lộ API key trong logs/reports.
- Đầy đủ Type Hints Pydantic và Python 3.10+.
- Hỗ trợ cả 2 chế độ: Mock Deterministic (cho CI/CD siêu tốc) và Live LLM (đo lường chất lượng thực tế).

---

## Tasks

### Task 1: Định nghĩa Pydantic Schemas cho Test Harness (`models.py`)
**Files:**
- Create: `backend/app/harness/__init__.py`
- Create: `backend/app/harness/models.py`
- Test: `backend/tests/test_harness_models.py`

**Interfaces:**
- Produces: `EvaluationMetric`, `EvaluationResult`, `TestCase`, `BenchmarkSuiteResult`.

- [ ] **Step 1: Viết test cho Pydantic models trong `backend/tests/test_harness_models.py`**
- [ ] **Step 2: Triển khai `backend/app/harness/models.py`**
- [ ] **Step 3: Chạy pytest xác nhận schemas hợp lệ**
- [ ] **Step 4: Commit `git commit -m "feat(harness): define pydantic schemas for agent test harness"`**

---

### Task 2: Phát triển Rubrics Evaluation Engine cho 8 Agent (`rubrics.py`)
**Files:**
- Create: `backend/app/harness/rubrics.py`
- Test: `backend/tests/test_harness_rubrics.py`

**Interfaces:**
- Produces: `AgentRubricEvaluator` với các phương thức evaluate chuyên biệt:
  - `evaluate_ba_analyst(questions: list[BriefQuestion]) -> EvaluationResult`
  - `evaluate_proposal(proposal: DesignProposal) -> EvaluationResult`
  - `evaluate_strategist(outline: str) -> EvaluationResult`
  - `evaluate_copywriter(copy: str) -> EvaluationResult`
  - `evaluate_designer(design: str) -> EvaluationResult`
  - `evaluate_coder(code: str) -> EvaluationResult`
  - `evaluate_visual_qa(qa_result: dict) -> EvaluationResult`
  - `evaluate_element_editor(output_html: str, target_element: dict, instruction: str) -> EvaluationResult`

- [ ] **Step 1: Viết unit tests kiểm tra từng hàm evaluate với cả sample đạt chuẩn (>=80 pts) và sample lỗi (<80 pts)**
- [ ] **Step 2: Triển khai toàn bộ rubric evaluation functions trong `backend/app/harness/rubrics.py`**
- [ ] **Step 3: Chạy test xác nhận rubrics chấm điểm chính xác và trả về chi tiết tiêu chí**
- [ ] **Step 4: Commit `git commit -m "feat(harness): implement rubric evaluation engine for 8 agents"`**

---

### Task 3: Xây dựng Benchmark Datasets & Fixtures (`fixtures.py`)
**Files:**
- Create: `backend/app/harness/fixtures.py`
- Test: `backend/tests/test_harness_fixtures.py`

**Interfaces:**
- Produces:
  - `BENCHMARK_CASES: dict[str, TestCase]` chứa 5 test case chuẩn (`b2b_saas`, `ecommerce_fashion`, `online_education`, `creative_agency`, `edge_cases`).
  - `MOCK_AGENT_OUTPUTS: dict[str, Any]` phục vụ cho chế độ mock execution không tốn chi phí token.

- [ ] **Step 1: Viết test kiểm tra tính toàn vẹn của dataset và fixtures trong `test_harness_fixtures.py`**
- [ ] **Step 2: Cài đặt `backend/app/harness/fixtures.py` với đầy đủ dữ liệu 5 lĩnh vực**
- [ ] **Step 3: Chạy test xác nhận fixtures nạp đúng và tương thích với schemas**
- [ ] **Step 4: Commit `git commit -m "feat(harness): create multi-industry benchmark dataset and mock fixtures"`**

---

### Task 4: Triển khai Sandboxed Execution Runner & Reporter (`runner.py`)
**Files:**
- Create: `backend/app/harness/runner.py`
- Test: `backend/tests/test_agent_harness.py`

**Interfaces:**
- Produces: `AgentHarness` class với:
  - `run_agent(agent_name: str, test_case: TestCase, live: bool = False) -> EvaluationResult`
  - `run_suite(agent_names: Optional[list[str]] = None, cases: Optional[list[str]] = None, live: bool = False) -> BenchmarkSuiteResult`
  - `generate_markdown_report(suite_result: BenchmarkSuiteResult) -> str`

- [ ] **Step 1: Viết test kiểm tra `AgentHarness` trong cả 2 chế độ Mock và Live sandbox**
- [ ] **Step 2: Triển khai `backend/app/harness/runner.py` điều phối thực thi và tính toán điểm số**
- [ ] **Step 3: Chạy integration test xác nhận runner hoạt động trơn tru cho tất cả 8 Agent**
- [ ] **Step 4: Commit `git commit -m "feat(harness): implement sandboxed agent runner and markdown reporter"`**

---

### Task 5: Xây dựng CLI Tool, Executable Script & Báo cáo Benchmark Thực Tế
**Files:**
- Create: `backend/app/harness/cli.py`
- Create: `scripts/run_agent_benchmark.py`
- Create: `docs/benchmarks/benchmark_latest.md` (kết quả chạy thực tế)

- [ ] **Step 1: Cài đặt CLI argument parser trong `backend/app/harness/cli.py`**
- [ ] **Step 2: Tạo script `scripts/run_agent_benchmark.py` với terminal formatting sinh động**
- [ ] **Step 3: Chạy kiểm thử CLI với `--mock` và xác minh mã thoát 0**
- [ ] **Step 4: Chạy kiểm thử benchmark live trên case `b2b_saas` và lưu báo cáo vào `docs/benchmarks/`**
- [ ] **Step 5: Cập nhật README.md hướng dẫn sử dụng Harness**
- [ ] **Step 6: Commit `git commit -m "feat(harness): add cli runner, benchmark script and initial benchmark report"`**
