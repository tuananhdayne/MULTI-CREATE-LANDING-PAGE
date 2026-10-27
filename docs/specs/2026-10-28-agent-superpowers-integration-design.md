# Technical Design Spec: Agent Superpowers Integration
## UI UX Pro Max, Frontend Design Skill, Chrome DevTools MCP & Playwright

**Date:** 2026-10-28  
**Author:** Antigravity Team  
**Status:** Approved  
**Scope:** Designer Agent, Coder Agent, Visual QA Agent, Element Editor Agent, Test Harness

---

## 1. Objectives & Agent Allocation Map

Theo chỉ đạo kiến trúc từ đối tác, hệ thống nâng cấp 4 nguồn năng lực chuyên sâu (Superpowers) vào các Agent tương ứng:

| Superpower / Skill | Target Agents | Nhiệm vụ & Giá trị đem lại |
| :--- | :--- | :--- |
| **UI UX Pro Max** | **Designer Agent** (`designer.py`, `proposal_agent.py`) | Thiết lập Design System đẳng cấp: Bảng màu theo quy tắc 60-30-10, 79+ UI Styles (Bento Grid, Dark Cyberpunk, Soft Glassmorphism, Editorial), Cặp font Google Fonts cao cấp, Đảm bảo tương phản WCAG AA. |
| **Frontend Design Skill** | **Designer Agent** + **Coder Agent** (`coder.py`) | Triệt tiêu "AI-slop" (chống template rập khuôn): Không dùng gradient tím mòn mắt, bố cục bất đối xứng táo bạo, phân cấp thị giác rõ ràng, animation có chủ đích (orchestrated motion). |
| **Chrome DevTools MCP** | **Visual QA Agent** + **Element Editor Agent** (`element_editor.py`) | Trực tiếp audit Console logs, đo đạc DOM, kiểm tra tràn viền 375px, và tinh chỉnh phần tử chính xác theo computed styles. |
| **Playwright** | **Visual QA Agent** (`visual_qa.py`) | Kiểm thử chức năng tương tác (Click nút CTA, cuộn trang mượt, mở FAQ) và kiểm tra hiển thị responsive trên cả 3 viewport (Desktop 1280px, Tablet 768px, Mobile 375px). |

---

## 2. Core Enhancements Per Agent

### 2.1 Designer Agent & Proposal Agent (UI UX Pro Max + Frontend Design)
- **Knowledge Base `ui_ux_pro_max_kb.py`**:
  - **Styles Library**:
    - `modern_saas`: Crisp borders, subtle glassmorphism, high-contrast dark/light accents.
    - `bento_grid`: Modular cards, asymmetrical spans, deliberate information density.
    - `dark_cyberpunk`: Deep slate/black, neon primary accents, energetic gradients.
    - `minimal_editorial`: Elegant typography, generous whitespace, understated luxury.
  - **Curated Google Fonts Pairings**:
    - Tech/Modern: `Outfit` (Heading) + `Inter` (Body)
    - High-Tech / Dev: `Space Grotesk` + `Plus Jakarta Sans`
    - Editorial / Luxury: `Syne` + `DM Sans`
    - Warm / Human: `Plus Jakarta Sans` + `Inter`
  - **Color Harmony (60-30-10)**:
    - 60% Dominant (Background & Canvas)
    - 30% Structural (Cards, Borders, Secondary text)
    - 10% Accent / Conversion (Primary CTA, High-impact badges)
- **Anti-"AI Slop" Directives (Anthropic Frontend Design)**:
  - Cấm tô màu đơn lẻ cho một từ duy nhất trong tiêu đề theo kiểu cliché.
  - Cấm lạm dụng nhãn viết hoa toàn bộ (ALL-CAPS) vô nghĩa trên từng card.
  - Cấm dùng số thứ tự 01, 02, 03 nếu nội dung không phải quy trình tuần tự.
  - Cấm hiệu ứng fade-in slide-up rời rạc trên từng khối gây chóng mặt.

### 2.2 Coder Agent (Frontend Design Execution)
- Cài đặt single-file HTML5 với Tailwind CSS theo triết lý "Production-grade Craft":
  - Tích hợp các tokens và styles từ Designer Agent.
  - Bố cục responsive đa tầng (Mobile-first, Tablet `md:`, Desktop `lg:` & `xl:`).
  - Tự động nạp đúng cặp Google Fonts đã chọn từ CDN.
  - Script khởi tạo Lucide icons an toàn trước `</body>`.
  - Giữ lại các ID định danh ngữ cảnh (`id="hero"`, `id="features"`, `id="cta"`, v.v.).

### 2.3 Visual QA Agent (Chrome DevTools MCP + Playwright Engine)
- **Multi-Viewport Audit via Playwright / Chrome Inspector**:
  - Viewport 1: **Desktop (1280 x 800)**: Kiểm tra layout full-width, navigation bar, grid 3-4 cột.
  - Viewport 2: **Tablet (768 x 1024)**: Kiểm tra co giãn grid 2 cột, không đè chữ.
  - Viewport 3: **Mobile (375 x 812)**: Kiểm tra hamburger menu hoặc compact header, padding cân đối, phát hiện tràn viền ngang (`scrollWidth > clientWidth`).
- **Interactive Smoke Test via Playwright**:
  - Tìm tất cả nút CTA (`button`, `a[href]`) và xác minh không gây crash hoặc unhandled exceptions.
  - Kiểm tra script `lucide.createIcons()` thực sự đã render các thẻ SVG.
- **Chrome DevTools MCP Telemetry**:
  - Bắt lỗi JavaScript runtime console.
  - Đo lường DOM metrics.

### 2.4 Element Editor Agent (Chrome DevTools MCP Context Aware)
- Tiếp nhận selector và computed styles từ Chrome DevTools Inspector.
- Áp dụng các nguyên tắc UI UX Pro Max khi tinh chỉnh:
  - Tự động bù trừ tương phản text và background.
  - Tối ưu kích thước cảm ứng trên mobile (`min-h-[44px]`).
  - Giữ nguyên ID và không làm biến dạng cấu trúc phân cấp xung quanh.

---

## 3. Implementation Workflow

1. Tạo thư viện thiết kế `backend/app/services/design_intelligence.py` tổng hợp quy tắc UI UX Pro Max & Frontend Design.
2. Nâng cấp `backend/app/agents/designer.py` & `backend/app/agents/proposal_agent.py` tích hợp `design_intelligence`.
3. Nâng cấp `backend/app/agents/coder.py` áp dụng triết lý Frontend Design (anti-AI slop).
4. Nâng cấp `backend/app/services/chrome_inspector.py` & `backend/app/agents/visual_qa.py` tích hợp Playwright multi-viewport testing song hành cùng DevTools MCP.
5. Cập nhật `rubrics.py` và chạy bộ Test Harness để xác minh toàn bộ agent đạt điểm xuất sắc (>= 90/100).
