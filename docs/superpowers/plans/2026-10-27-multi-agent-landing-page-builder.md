# Multi-Agent Landing Page Builder Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Xây dựng ứng dụng Full-stack (Python FastAPI + LangGraph + React/Vite) điều phối 5 Agent chuyên sâu sử dụng Google Gemini (cấu hình trong `.env`) để tự động tạo ra Landing Page HTML5/Tailwind hoàn chỉnh, xem trước Live Preview theo thời gian thực và hỗ trợ chỉnh sửa trực quan từng phần tử với Chrome DevTools / Click-to-Inspect.

**Architecture:** 
- **Backend (FastAPI + LangGraph)**: Quản lý StateGraph gồm 5 Agent (Strategist, Copywriter, Designer, Coder, Visual QA), kết nối mô hình Google Gemini qua API Key trong `.env`, stream tiến độ qua SSE, hỗ trợ Playwright CDP kiểm tra DOM/console và API sửa đổi theo vị trí phần tử (targeted element tweak).
- **Frontend (React + Vite + Tailwind CSS)**: Giao diện trực quan Dark/Light, hiển thị timeline từng bước của Agent, nhúng iframe Live Preview với 3 chế độ (Desktop/Tablet/Mobile), hỗ trợ chế độ Click-to-Inspect để chọn phần tử và yêu cầu AI sửa trực tiếp, hỗ trợ Undo/Redo lịch sử phiên bản và tải về `index.html` 1-click.

**Tech Stack:** 
- Backend: Python 3.10+, FastAPI, Uvicorn, LangGraph, LangChain-Google-GenAI, Pydantic, Playwright (Chrome CDP), python-dotenv
- Frontend: React 18+, TypeScript, Vite, Tailwind CSS, Lucide React, Axios / EventSource

**Spec:** Đã thống nhất qua phiên `/grill-me` (Kiến trúc Multi-Agent LangGraph + Google Gemini API trong `.env` + Single-file HTML5/Tailwind output + Dual Chrome DevTools Click-to-Inspect + Version History).

## Global Constraints
- `GEMINI_API_KEY` tuyệt đối không được hardcode hoặc để lộ qua API client; bắt buộc đọc từ `.env`. File `.env` phải nằm trong `.gitignore`.
- Cung cấp file `.env.example` với giá trị mẫu, biến `GEMINI_MODEL=gemini-2.5-flash` (hoặc `gemini-1.5-pro` / `gemini-3.7-flash`).
- Mã Landing Page xuất xưởng phải là single-file HTML5 độc lập, nạp Tailwind CSS CDN, Google Fonts, Lucide Icons và responsive hoàn chỉnh.
- Quản lý phiên bản hỗ trợ Undo/Redo mượt mà trên bộ nhớ session/local.

## Review Focus
1. **Bảo mật API Key**: Kiểm tra chắc chắn không có endpoint nào trả về `GEMINI_API_KEY` ra frontend và `.env` không bị git track.
2. **Khả năng phục hồi của Agent Coder**: Đảm bảo mã HTML được trích xuất sạch sẽ từ markdown code block (` ```html ... ``` `), không bị cắt xén hay dính text thừa.
3. **Cơ chế Click-to-Inspect**: PostMessage giữa iframe và React app phải chính xác, gửi đúng selector/path và innerHTML của phần tử được click.
4. **Vòng lặp Critic/Fix**: QA Agent tự động kiểm tra cú pháp thẻ đóng và console errors; nếu có lỗi phải kích hoạt Coder sửa lại trước khi hoàn tất (tối đa 2 vòng lặp).
5. **Responsive & Mobile Viewport**: Iframe preview phải co dãn chuẩn xác kích thước (Desktop: 100%, Tablet: 768px, Mobile: 375px).

---

## File Structure Map
- `.gitignore`: Loại trừ `.env`, `node_modules`, `venv`, `__pycache__`
- `.env.example`: File mẫu cấu hình biến môi trường
- `backend/`:
  - `requirements.txt`: Khai báo các thư viện Python
  - `app/config.py`: Đọc cấu hình môi trường an toàn từ `.env`
  - `app/models/state.py`: Định nghĩa State của LangGraph
  - `app/models/api_schemas.py`: Schema request/response cho FastAPI
  - `app/agents/base.py`: Kết nối Gemini API, xử lý prompt & streaming
  - `app/agents/strategist.py`: Agent lập dàn ý & chiến lược chuyển đổi
  - `app/agents/copywriter.py`: Agent viết nội dung & tiêu đề
  - `app/agents/designer.py`: Agent thiết kế hệ màu & typography
  - `app/agents/coder.py`: Agent lập trình HTML5/Tailwind
  - `app/agents/element_editor.py`: Agent tinh chỉnh phần tử theo DevTools context
  - `app/agents/visual_qa.py`: Agent kiểm tra DOM/Console bằng Playwright CDP
  - `app/graph/workflow.py`: Xây dựng LangGraph StateGraph kết nối các agent
  - `app/services/project_service.py`: Quản lý lịch sử phiên bản (Undo/Redo)
  - `app/main.py`: Entrypoint FastAPI, CORS, SSE streaming endpoint
- `frontend/`:
  - `package.json`, `vite.config.ts`, `tailwind.config.js`: Cấu hình React + Vite
  - `src/App.tsx`: Layout chính tích hợp Header, Prompt bar, Timeline, Live Preview
  - `src/components/Header.tsx`: Thanh điều hướng, chọn viewport, Undo/Redo, Export
  - `src/components/PromptInput.tsx`: Khung nhập prompt + Templates gợi ý
  - `src/components/AgentTimeline.tsx`: Hiển thị tiến độ và suy nghĩ từng agent thời gian thực
  - `src/components/LivePreview.tsx`: Iframe preview + chế độ Click-to-Inspect
  - `src/components/InspectModal.tsx`: Hộp thoại sửa nhanh phần tử được chọn
  - `src/components/CodeModal.tsx`: Hộp thoại xem/copy source code HTML
  - `src/services/api.ts`: Kết nối REST & SSE với Backend

---

## Implementation Tasks

### Task 1: Thiết lập cấu trúc dự án & Bảo mật môi trường (.gitignore, .env.example, Backend Scaffolding)
**Files:**
- Create: `.gitignore`
- Create: `.env.example`
- Create: `backend/requirements.txt`
- Create: `backend/app/config.py`
- Test: `backend/tests/test_config.py`

**Interfaces:**
- Produces: `Settings` class trong `backend/app/config.py` với các thuộc tính `gemini_api_key: str`, `gemini_model: str = "gemini-2.5-flash"`, `host: str = "0.0.0.0"`, `port: int = 8000`.

- [x] **Step 1: Tạo .gitignore và .env.example đảm bảo bảo mật 100% key**
- [x] **Step 2: Viết test cho Config trong `backend/tests/test_config.py`**
- [x] **Step 3: Tạo `backend/requirements.txt` và triển khai `backend/app/config.py`**
- [x] **Step 4: Chạy test xác minh Config nạp đúng biến và giấu an toàn key**
- [x] **Step 5: Commit `git commit -m "chore: setup project structure and secure env config"`**

---

### Task 2: Định nghĩa State, Schemas và Base Gemini Client
**Files:**
- Create: `backend/app/models/state.py`
- Create: `backend/app/models/api_schemas.py`
- Create: `backend/app/agents/base.py`
- Test: `backend/tests/test_gemini_client.py`

**Interfaces:**
- Produces: `AgentState` TypedDict trong `state.py` (chứa `prompt`, `outline`, `copy`, `design`, `code`, `errors`, `messages`, `iteration`).
- Produces: `get_gemini_model(model_name: Optional[str])` trả về instance ChatGoogleGenerativeAI hoặc Gemini Client an toàn.

- [x] **Step 1: Viết test khởi tạo Gemini Client và kiểm tra không leak key**
- [x] **Step 2: Tạo `AgentState` và Pydantic API Schemas (`GenerateRequest`, `TweakElementRequest`, `ProjectResponse`)**
- [x] **Step 3: Cài đặt `base.py` với xử lý retry và trích xuất code markdown sạch**
- [x] **Step 4: Chạy test xác minh base client**
- [x] **Step 5: Commit `git commit -m "feat(backend): add state schemas and base gemini client"`**

---

### Task 3: Phát triển 5 Agent chuyên sâu (Strategist, Copywriter, Designer, Coder, Visual QA)
**Files:**
- Create: `backend/app/agents/strategist.py`
- Create: `backend/app/agents/copywriter.py`
- Create: `backend/app/agents/designer.py`
- Create: `backend/app/agents/coder.py`
- Create: `backend/app/agents/visual_qa.py`
- Create: `backend/app/agents/element_editor.py`
- Test: `backend/tests/test_agents.py`

**Interfaces:**
- Consumes: `AgentState` từ `state.py`, Gemini wrapper từ `base.py`
- Produces: Các hàm node: `strategist_node`, `copywriter_node`, `designer_node`, `coder_node`, `qa_node`, `tweak_element_node`.

- [ ] **Step 1: Viết test cho logic của từng agent node**
- [ ] **Step 2: Cài đặt `strategist.py` và `copywriter.py` (prompts tối ưu tỷ lệ chuyển đổi)**
- [ ] **Step 3: Cài đặt `designer.py` và `coder.py` (single-file HTML5 + Tailwind CDN, Google Fonts, Lucide)**
- [ ] **Step 4: Cài đặt `visual_qa.py` (kiểm tra cú pháp HTML, layout, tags) và `element_editor.py` (tinh chỉnh phần tử mục tiêu)**
- [ ] **Step 5: Chạy unit tests xác minh output chuẩn của các node**
- [ ] **Step 6: Commit `git commit -m "feat(backend): implement 5 specialized agents and element editor"`**

---

### Task 4: Xây dựng LangGraph Workflow & Streaming Pipeline
**Files:**
- Create: `backend/app/graph/workflow.py`
- Create: `backend/app/services/project_service.py`
- Test: `backend/tests/test_graph.py`

**Interfaces:**
- Consumes: Các agent node từ Task 3.
- Produces: `compiled_graph` chạy StateGraph với router vòng lặp Critic: `coder -> qa -> (cần sửa ? coder : END)`.
- Produces: `ProjectService` quản lý stack undo/redo các phiên bản HTML.

- [ ] **Step 1: Viết test cho workflow loop và cơ chế undo/redo**
- [ ] **Step 2: Xây dựng LangGraph StateGraph kết nối các agent với điều kiện lặp tối đa 2 lần nếu QA báo lỗi**
- [ ] **Step 3: Cài đặt `project_service.py` lưu trữ phiên bản trang web**
- [ ] **Step 4: Chạy test xác minh luồng graph hoàn chỉnh**
- [ ] **Step 5: Commit `git commit -m "feat(backend): build langgraph stategraph workflow and version service"`**

---

### Task 5: Xây dựng FastAPI Server & SSE Streaming Endpoints
**Files:**
- Create: `backend/app/main.py`
- Test: `backend/tests/test_api.py`

**Interfaces:**
- Produces:
  - `POST /api/generate` (Server-Sent Events stream: emit trạng thái từng agent và code HTML hoàn thành)
  - `POST /api/tweak-element` (sửa đổi phần tử được chọn)
  - `POST /api/undo` & `POST /api/redo` (hoàn tác / làm lại phiên bản)
  - `GET /api/project` (lấy code và trạng thái hiện tại)
  - `GET /api/health`

- [ ] **Step 1: Viết integration test cho API endpoints**
- [ ] **Step 2: Triển khai FastAPI app với CORS middleware và SSE stream handler**
- [ ] **Step 3: Triển khai endpoint `/api/tweak-element` và endpoint quản lý phiên bản**
- [ ] **Step 4: Chạy test toàn bộ API backend**
- [ ] **Step 5: Commit `git commit -m "feat(backend): implement fastapi server with sse streaming and rest endpoints"`**

---

### Task 6: Khởi tạo Frontend React + Vite + Tailwind CSS & API Service
**Files:**
- Create: `frontend/package.json`
- Create: `frontend/vite.config.ts`
- Create: `frontend/tailwind.config.js`
- Create: `frontend/src/index.css`
- Create: `frontend/src/services/api.ts`

**Interfaces:**
- Produces: Single-page React application kết nối với backend qua Axios và EventSource listener.

- [ ] **Step 1: Khởi tạo dự án Vite React TypeScript trong thư mục `frontend/`**
- [ ] **Step 2: Cấu hình Tailwind CSS, Google Fonts và Lucide Icons**
- [ ] **Step 3: Viết `src/services/api.ts` kết nối REST API và lắng nghe SSE events**
- [ ] **Step 4: Kiểm tra build frontend thành công**
- [ ] **Step 5: Commit `git commit -m "feat(frontend): scaffold vite react app and api integration"`**

---

### Task 7: Xây dựng các UI Components (Timeline, Prompt Bar, Header)
**Files:**
- Create: `frontend/src/components/Header.tsx`
- Create: `frontend/src/components/PromptInput.tsx`
- Create: `frontend/src/components/AgentTimeline.tsx`
- Create: `frontend/src/components/CodeModal.tsx`

**Interfaces:**
- Produces:
  - `Header`: Quản lý Viewport (Desktop/Tablet/Mobile), nút Undo/Redo, Export HTML, View Source Code.
  - `PromptInput`: Ô nhập yêu cầu có đính kèm danh sách thẻ template (SaaS, Khóa học, Agency, E-commerce, Event...).
  - `AgentTimeline`: Thanh tiến độ hiển thị trực quan 5 Agent (đang suy nghĩ, hoàn thành, chi tiết nội dung).

- [ ] **Step 1: Cài đặt `Header.tsx` với đầy đủ nút thao tác nhanh**
- [ ] **Step 2: Cài đặt `PromptInput.tsx` với giao diện hiện đại và các prompt mẫu**
- [ ] **Step 3: Cài đặt `AgentTimeline.tsx` với animation mượt mà khi agent đang làm việc**
- [ ] **Step 4: Cài đặt `CodeModal.tsx` để xem và copy code 1-click**
- [ ] **Step 5: Commit `git commit -m "feat(frontend): implement header, prompt bar, and agent timeline components"`**

---

### Task 8: Xây dựng Live Preview Iframe & Trải nghiệm Chrome DevTools Click-to-Inspect
**Files:**
- Create: `frontend/src/components/LivePreview.tsx`
- Create: `frontend/src/components/InspectModal.tsx`
- Modify: `frontend/src/App.tsx`

**Interfaces:**
- Produces:
  - `LivePreview`: Render HTML an toàn trong iframe, tự động chèn script lắng nghe sự kiện click/hover khi bật chế độ "Inspect", gửi thông tin phần tử (tag, class, text, outerHTML) ra ngoài qua `postMessage`.
  - `InspectModal`: Bật popup cho phép người dùng nhập yêu cầu chỉnh sửa riêng cho phần tử đó, gửi về `/api/tweak-element` và cập nhật iframe ngay lập tức.

- [ ] **Step 1: Cài đặt `LivePreview.tsx` với responsive frame (Desktop 100%, Tablet 768px, Mobile 375px)**
- [ ] **Step 2: Cài đặt script inject DevTools Inspector vào iframe (highlight box + selector pill)**
- [ ] **Step 3: Cài đặt `InspectModal.tsx` nhận diện phần tử được click và gửi lệnh tinh chỉnh**
- [ ] **Step 4: Lắp ráp toàn bộ vào `App.tsx` với state đồng bộ mượt mà**
- [ ] **Step 5: Commit `git commit -m "feat(frontend): implement live preview with click-to-inspect devtools feature"`**

---

### Task 9: Kiểm thử tích hợp toàn diện (End-to-End Test & Verification)
**Files:**
- Test: `backend/tests/test_e2e.py`
- Modify: `README.md` (hướng dẫn chạy 1 lệnh cả Frontend + Backend)

- [ ] **Step 1: Chạy toàn bộ test suite backend (`pytest`)**
- [ ] **Step 2: Chạy build frontend (`npm run build`)**
- [ ] **Step 3: Kiểm tra luồng tạo trang thực tế từ một prompt mẫu**
- [ ] **Step 4: Kiểm tra tính năng Click-to-Inspect và Undo/Redo**
- [ ] **Step 5: Kiểm tra tính năng Export HTML và mở thử file ngoài trình duyệt độc lập**
- [ ] **Step 6: Tạo `README.md` chi tiết và commit hoàn thiện `git commit -m "docs: add setup guide and complete e2e verification"`**
