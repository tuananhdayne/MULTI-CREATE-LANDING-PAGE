# Agent Superpowers Integration Implementation Plan
## UI UX Pro Max, Frontend Design Skill, Chrome DevTools MCP & Playwright

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Tích hợp 4 nguồn năng lực thiết kế & kiểm thử chuẩn quốc tế vào hệ thống Multi-Agent Landing Page Builder:
1. **UI UX Pro Max**: Cung cấp tri thức thiết kế chuyên sâu (60-30-10 palette, curated font pairings, UI style patterns, WCAG AA).
2. **Frontend Design Skill**: Triệt tiêu "AI-slop", định hình thẩm mỹ độc bản, kiến trúc bố cục giàu tính nghệ thuật cho Designer & Coder.
3. **Chrome DevTools MCP**: Kiểm tra runtime console errors, đo đạc DOM, chống tràn viền di động 375px cho QA & Element Editor.
4. **Playwright**: Kiểm thử chức năng tương tác (CTA clicks, icons render) và kiểm tra responsive 3 viewport (Desktop, Tablet, Mobile) cho Visual QA.

**Spec:** [`docs/specs/2026-10-28-agent-superpowers-integration-design.md`](file:///home/tuananh/GEN_LANDING/docs/specs/2026-10-28-agent-superpowers-integration-design.md)

---

## Tasks

### Task 1: Xây dựng Module Tri Thức Thiết Kế `design_intelligence.py`
**Files:**
- Create: `backend/app/services/design_intelligence.py`
- Test: `backend/tests/test_design_intelligence.py`

**Interfaces:**
- Produces:
  - `STYLE_PRESETS`: Từ điển 6 phong cách thiết kế chuẩn (Modern SaaS, Bento Grid, Dark Cyberpunk, Minimalist Editorial, Warm Creator, Neo-Brutalism).
  - `FONT_PAIRINGS`: Danh mục cặp font Google Fonts chất lượng cao kèm link CDN.
  - `COLOR_HARMONIES`: Hệ thống phối màu 60-30-10 với mã HEX chuẩn.
  - `ANTI_AI_SLOP_GUIDELINES`: Danh sách quy tắc triệt tiêu giao diện AI rập khuôn.
  - `get_recommended_design_system(prompt: str, industry: Optional[str]) -> dict`.

- [ ] **Step 1: Viết test cho `design_intelligence.py` trong `backend/tests/test_design_intelligence.py`**
- [ ] **Step 2: Triển khai `backend/app/services/design_intelligence.py`**
- [ ] **Step 3: Chạy test xác nhận module trả về đầy đủ presets, fonts và guidelines**
- [ ] **Step 4: Commit `git commit -m "feat(design): implement design intelligence module with ui-ux-pro-max and frontend-design knowledge"`**

---

### Task 2: Nâng cấp `Designer Agent` và `Proposal Agent` với UI UX Pro Max & Frontend Design
**Files:**
- Modify: `backend/app/agents/designer.py`
- Modify: `backend/app/agents/proposal_agent.py`
- Test: `backend/tests/test_designer_superpowers.py`

**Interfaces:**
- Consumes: `design_intelligence.py`.
- Produces:
  - `designer_node`: Sản sinh bản đặc tả Design System có phong cách cụ thể, typography pairings, bảng màu 60-30-10, và chỉ dẫn layout không rập khuôn.
  - `ProposalAgent.generate_proposal`: Tích hợp style presets và font pairings vào proposal cho khách hàng phê duyệt.

- [ ] **Step 1: Viết test cho `designer_node` và `ProposalAgent` với tri thức mới**
- [ ] **Step 2: Nâng cấp prompt & logic của `designer.py` và `proposal_agent.py`**
- [ ] **Step 3: Chạy test xác minh đầu ra tuân thủ quy tắc 60-30-10 và font pairings chuẩn**
- [ ] **Step 4: Commit `git commit -m "feat(agents): empower Designer and Proposal agents with UI UX Pro Max and Frontend Design skills"`**

---

### Task 3: Nâng cấp `Coder Agent` với Frontend Design Skill (Anti-AI Slop & Craft Quality)
**Files:**
- Modify: `backend/app/agents/coder.py`
- Test: `backend/tests/test_coder_superpowers.py`

**Interfaces:**
- Produces:
  - `coder_node`: Áp dụng quy tắc Frontend Design để lập trình HTML5: layout độc bản (asymmetry / deliberate spacing), nạp đúng Google Fonts từ CDN, nạp Lucide, phân bổ màu 60-30-10, không dùng gradient tím nhàm chán hoặc ALL-CAPS vô tội vạ.

- [ ] **Step 1: Viết test kiểm tra mã HTML xuất xưởng có font CDN hợp lệ và không dính AI-slop**
- [ ] **Step 2: Cập nhật prompt & system guidelines của `coder.py`**
- [ ] **Step 3: Chạy test xác nhận mã nguồn đạt chuẩn craft chất lượng cao**
- [ ] **Step 4: Commit `git commit -m "feat(coder): inject Frontend Design principles into Coder Agent"`**

---

### Task 4: Nâng cấp `Visual QA Agent` với Playwright Multi-Viewport & Chrome DevTools MCP
**Files:**
- Modify: `backend/app/services/chrome_inspector.py`
- Modify: `backend/app/agents/visual_qa.py`
- Test: `backend/tests/test_visual_qa_playwright.py`

**Interfaces:**
- Produces:
  - `ChromeInspector.inspect_responsive_playwright`: Kiểm tra responsive trên cả 3 khung nhìn (Desktop 1280px, Tablet 768px, Mobile 375px), click thử nút CTA, kiểm tra rendering của SVG icons.
  - `qa_node`: Tổng hợp kết quả từ cả Playwright multi-viewport và Chrome DevTools MCP console/overflow audit.

- [ ] **Step 1: Viết test cho responsive & functional audit trong `backend/tests/test_visual_qa_playwright.py`**
- [ ] **Step 2: Nâng cấp `chrome_inspector.py` và `visual_qa.py`**
- [ ] **Step 3: Chạy test xác nhận phát hiện chính xác lỗi trên từng khung nhìn**
- [ ] **Step 4: Commit `git commit -m "feat(qa): integrate Playwright multi-viewport and functional testing into Visual QA"`**

---

### Task 5: Nâng cấp `Element Editor Agent` & Chạy Benchmark Toàn Diện
**Files:**
- Modify: `backend/app/agents/element_editor.py`
- Modify: `backend/app/harness/rubrics.py`
- Execute: `scripts/run_agent_benchmark.py`

- [ ] **Step 1: Cập nhật `element_editor.py` áp dụng UI UX Pro Max styling cho các phần tử chỉnh sửa**
- [ ] **Step 2: Cập nhật `rubrics.py` bổ sung tiêu chí đánh giá font pairings và anti-AI slop**
- [ ] **Step 3: Chạy toàn bộ test suite backend (`pytest`) đạt 100% pass**
- [ ] **Step 4: Chạy Benchmark Suite trên cả 5 ngành nghề và cập nhật báo cáo vào `docs/benchmarks/benchmark_latest.md`**
- [ ] **Step 5: Khởi động lại Uvicorn & Vite server, xác minh hoạt động mượt mà trên trình duyệt**
- [ ] **Step 6: Commit `git commit -m "feat(system): complete integration of UI UX Pro Max, Frontend Design, Chrome DevTools MCP, and Playwright across all agents"`**
