# 🚀 LandingCraft: Multi-Agent Landing Page Builder

Hệ thống Full-stack phối hợp **8 AI Agent chuyên sâu** theo mô hình **Human-in-the-Loop 3 Giai đoạn (Milestone Workflow)**, ứng dụng Google Gemini (qua 9router Local Gateway), tích hợp **UI UX Pro Max**, **Frontend Design Skill**, **Chrome DevTools MCP** và **Playwright** để kiến tạo các trang Landing Page HTML5 + Tailwind CSS độc bản, tối ưu chuyển đổi, xem trước thời gian thực và hỗ trợ chỉnh sửa trực quan từng phần tử với **Click-to-Inspect**.

📖 **Tài liệu Kiến trúc & Triển khai toàn diện:** [docs/PROJECT_ARCHITECTURE.md](docs/PROJECT_ARCHITECTURE.md)

---

## 🌟 Tính Năng Nổi Bật

1. **Quy trình Hợp tác Agency 3 Giai đoạn (Human-in-the-Loop)**:
   - 📋 **Giai đoạn 1 (Briefing)**: Khảo sát nghiệp vụ với `BA Analyst Agent` qua 3 câu hỏi cốt lõi có sẵn gợi ý 1-click.
   - 🎨 **Giai đoạn 2 (Proposal)**: Ký duyệt bản Đề xuất Kiến trúc & Thiết kế do `Proposal Agent` thiết lập trước khi lập trình.
   - 💻 **Giai đoạn 3 (Build & UAT)**: Hệ sinh thái 5 Agent (Strategist, Copywriter, Designer, Coder, QA) tự động lập trình và nghiệm thu tương tác.
2. **Đội ngũ 8 AI Agents chuyên trách**:
   - `BA Analyst`, `Proposal Agent`, `Product Strategist`, `Conversion Copywriter`, `UI/UX Designer`, `Frontend Coder`, `Visual QA` và `Targeted Element Editor`.
3. **Trải nghiệm Chrome DevTools Click-to-Inspect**:
   - Nhấp trực tiếp vào bất kỳ phần tử nào trên giao diện (nút bấm, tiêu đề, thẻ card) để ra lệnh cho AI sửa chính xác phần đó.
4. **Quản lý phiên bản & Xem trước đa màn hình**:
   - Hỗ trợ **Hoàn tác (Undo)** và **Làm lại (Redo)** mượt mà trên bộ nhớ session.
   - Chuyển đổi khung nhìn linh hoạt: **Desktop (1280px)**, **Tablet (768px)**, **Mobile (375px)**.
   - Xuất bản và tải về tệp `index.html` chạy ngay chỉ với 1 cú click.
5. **Hỗ trợ 9router Local Gateway**:
   - Tích hợp cổng kết nối `http://localhost:20128/v1` của 9router với các model như `ag/gemini-3.8-flash-high` hoặc Google Gemini API trực tiếp.
   - Tuyệt đối bảo mật API Key, không lưu vết hay để lộ key ra ngoài.

---

## 🛠️ Hướng Dẫn Cài Đặt & Khởi Chạy

### 1. Cấu hình biến môi trường
Sao chép tệp mẫu `.env.example` thành `.env`:
```bash
cp .env.example .env
```
Mở `.env` và điền key của bạn:
```env
# Gemini API Key hoặc 9router Token
GEMINI_API_KEY=your_key_here

# 9router Gateway (để trống nếu dùng thẳng Google API)
LLM_BASE_URL=http://localhost:20128/v1

# Model Gemini mong muốn
GEMINI_MODEL=ag/gemini-3.7-flash-high

HOST=0.0.0.0
PORT=8000
```

---

### 2. Khởi chạy Backend Server (FastAPI)
```bash
cd backend
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
* API Documentation (Swagger UI): `http://localhost:8000/docs`
* Health Check: `http://localhost:8000/api/health`

---

### 3. Khởi chạy Frontend (React + Vite)
Mở một terminal mới:
```bash
cd frontend
npm run dev
```
Truy cập giao diện Web tại: **`http://localhost:5173`**

---

## 🧪 Chạy Kiểm Thử (Testing)

### Kiểm thử Backend (pytest):
```bash
PYTHONPATH=backend pytest backend/tests/ -v
```
*(Hiện có 22 test cases pass 100% bao gồm cả E2E lifecycle)*

### Kiểm tra build Frontend:
```bash
cd frontend && npm run build
```

---

## ⚡ Năng Lực Chuyên Sâu Tích Hợp (Agent Superpowers)

Hệ thống được nâng cấp toàn diện với 4 nguồn năng lực thiết kế & kiểm thử chuẩn quốc tế:

1. **🎨 UI UX Pro Max (`Designer Agent`)**:
   - Tự động thiết lập Design System chuẩn mực theo quy tắc phối màu **60-30-10** (60% canvas nền, 30% cấu trúc thẻ, 10% điểm nhấn CTA chuyển đổi).
   - Thư viện 6 phong cách thị giác cao cấp: *Modern SaaS, Bento Grid, Dark Cyberpunk, Minimalist Editorial, Warm Creator, Neo-Brutalism*.
   - Tuyển tập cặp font Google Fonts chất lượng cao (*Outfit + Inter, Space Grotesk + Plus Jakarta Sans, Syne + DM Sans*).
   - Bảo đảm tiêu chuẩn tương phản khả dụng **WCAG AA** (tối thiểu 4.5:1).

2. **✨ Frontend Design Skill (`Designer Agent + Coder Agent`)**:
   - Triệt tiêu toàn diện các đặc điểm **"AI-slop" (rập khuôn máy móc)**: loại bỏ gradient tím-hồng generic, không tô màu lẻ loi một chữ trong tiêu đề, không lạm dụng nhãn ALL-CAPS vô tội vạ.
   - Bố cục bất đối xứng có chủ đích (*Asymmetric Bento layout*) thay vì xếp card 3 cột nhàm chán.
   - Chuyển động có tổ chức (*orchestrated motion*), tạo điểm nhấn xuất hiện mượt mà.

3. **🛠️ Chrome DevTools MCP (`Visual QA + Element Editor Agent`)**:
   - Giao tiếp trực tiếp với Headless Chrome qua giao thức MCP (`chrome-devtools-mcp`).
   - Audit sâu runtime JavaScript: phát hiện và phân loại chính xác các lỗi `console.error`.
   - Kiểm tra co dãn giao diện di động 375px và đo đạc thuộc tính DOM thực tế.

4. **🎭 Playwright (`Visual QA Agent`)**:
   - Tự động kiểm thử responsive trên cả **3 khung nhìn thực tế**: Desktop (1280x800), Tablet (768x1024), và Mobile (375x812).
   - Kiểm thử tương tác (Interactive smoke test): Click thử các nút CTA chính và kiểm tra rendering của SVG icons.

---

## 📊 Agent Test & Benchmark Evaluation Harness

Dự án cung cấp bộ công cụ kiểm thử và đo lường chất lượng Agent độc lập:

### Chạy Benchmark Suite toàn diện (40 bài test trên 5 ngành nghề):
```bash
python3 scripts/run_agent_benchmark.py
```
*(Chế độ Mock Replay chạy siêu tốc trong < 1 giây, xuất báo cáo Markdown tại `docs/benchmarks/benchmark_latest.md`)*

### Chạy Sandbox trực tiếp với Live LLM / Browser:
```bash
# Test riêng Visual QA với Playwright & DevTools MCP trên case B2B SaaS
python3 scripts/run_agent_benchmark.py --agent visual_qa --case b2b_saas --live

# Test riêng Element Editor chỉnh sửa phần tử DOM theo lệnh DevTools
python3 scripts/run_agent_benchmark.py --agent element_editor --case b2b_saas --live
```

---

## 📁 Cấu Trúc Mã Nguồn

```
GEN_LANDING/
├── .env.example                # Tệp mẫu cấu hình môi trường
├── .gitignore                  # Loại trừ .env và các dữ liệu nhạy cảm
├── AGENTS.md                   # Workspace rules cho Antigravity IDE
├── README.md                   # Hướng dẫn dự án
├── backend/
│   ├── app/
│   │   ├── config.py           # Quản lý cấu hình an toàn
│   │   ├── main.py             # FastAPI entrypoint & SSE streaming
│   │   ├── agents/             # 8 Agent chuyên sâu (BA, Proposal, Coder, QA, v.v.)
│   │   ├── graph/              # LangGraph StateGraph & Critic Loop
│   │   ├── harness/            # Agent Test & Benchmark Evaluation Harness
│   │   │   ├── models.py       # Pydantic schemas cho Test & Benchmark
│   │   │   ├── rubrics.py      # Thang điểm 0-100 cho 8 agent
│   │   │   ├── fixtures.py     # Benchmark dataset 5 ngành nghề
│   │   │   ├── runner.py       # Sandboxed Agent Runner
│   │   │   └── cli.py          # CLI runner
│   │   ├── services/           # Design Intelligence, Chrome Inspector, Session Service
│   │   └── schemas/            # Pydantic API & Session Schemas
│   └── tests/                  # Bộ 60+ test cases tự động
├── frontend/                   # React 18 + Vite + Tailwind CSS + Lucide
├── scripts/
│   ├── run_agent_benchmark.py  # Script chạy Benchmark Harness
│   └── test_milestone_workflow.py # Script kiểm thử E2E 3-stage milestone
└── docs/
    ├── specs/                  # Tài liệu thiết kế kỹ thuật (Design Specs)
    ├── plans/                  # Kế hoạch triển khai (Implementation Plans)
    ├── progress/               # Nhật ký tiến độ chi tiết (Ledgers)
    └── benchmarks/             # Báo cáo Benchmark định lượng
```
