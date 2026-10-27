# Design Specification: Visual QA Chrome DevTools MCP Integration

**Date:** 2026-10-28  
**Author:** Antigravity & User  
**Status:** In Review  
**Target File:** `docs/specs/2026-10-28-visual-qa-chrome-devtools-mcp-design.md`

---

## 1. Intent and the Why

### Context
Hiện tại, `Visual QA Agent` (`backend/app/agents/visual_qa.py`) chỉ kiểm tra mã nguồn HTML tĩnh bằng Regular Expression (kiểm tra thẻ `DOCTYPE`, CDN Tailwind, thẻ đóng). Agent chưa thực sự biết liệu trang web có hiển thị đúng trên trình duyệt thực hay không, có nổ lỗi JavaScript runtime trong Console hay không, và có bị vỡ layout khi co kéo màn hình hay không.

### The Problem
Mô hình QA tĩnh này có thể bỏ sót các lỗi nghiêm trọng trong môi trường runtime:
- Lỗi cú pháp hoặc hàm JavaScript bị gọi sai trong console (ví dụ: `Uncaught TypeError: lucide is not defined`, hàm accordion bị crash).
- Phần tử bị tràn chiều ngang (overflow) trên màn hình di động (Mobile 375px).
- Ảnh hoặc tài nguyên CDN bị lỗi kết nối hoặc chặn hiển thị.

### The Goal
Trang bị cho `Visual QA Agent` khả năng tương tác trực tiếp với **Chrome DevTools MCP Server** (`chrome-devtools-mcp`) theo chuẩn giao thức Model Context Protocol (JSON-RPC stdio). Visual QA sẽ thực sự mở trang trong Chrome ngầm (Headless Chrome), thanh tra console errors, kiểm tra kích thước responsive, và đưa ra biên bản thẩm định chất lượng có căn cứ kỹ thuật chính xác.

---

## 2. Goals, Non-Goals, and Anti-Goals

### Goals
1. **MCP Client Service (`backend/app/services/devtools_mcp_client.py`):** Xây dựng module Python quản lý vòng đời tiến trình `npx -y chrome-devtools-mcp --headless` qua chuẩn JSON-RPC stdio (initialize, list_tools, call_tool).
2. **Runtime Console Inspection:** Sử dụng công cụ `navigate_page` và `list_console_messages` để phát hiện mọi lỗi JavaScript runtime, cảnh báo và lỗi cú pháp.
3. **Responsive Layout Check:** Sử dụng `resize_page` và `evaluate_script` để kiểm tra độ tràn viền (`document.documentElement.scrollWidth > window.innerWidth`) trên các viewport: Desktop (1440px), Tablet (768px), Mobile (375px).
4. **Graceful Fallback:** Nếu Chrome hoặc MCP Server gặp sự cố hoặc timeout, hệ thống tự động fallback về kiểm tra cú pháp tĩnh (Static Validation), không làm gián đoạn luồng sinh trang của đối tác.

### Non-Goals
- Không chạy các bài test tải (load testing) hay giả lập hàng nghìn người dùng đồng thời.
- Không can thiệp sâu vào bộ nhớ heap snapshot hay CPU profiling trong pha QA tiêu chuẩn.

### Anti-Goals
- Không để tiến trình Chrome hoặc Node.js bị treo ngầm (zombie processes) sau khi kết thúc phiên QA.
- Không để lỗi mạng từ phía trình duyệt làm crash server FastAPI.

---

## 3. Constraints & Technical Boundaries
- **Runtime Environment:** Linux, Google Chrome (`/usr/bin/google-chrome`), Node.js v20.
- **MCP Server CLI:** `npx -y chrome-devtools-mcp --headless`.
- **Protocol:** JSON-RPC 2.0 over standard I/O (stdin/stdout).
- **Timeout Policy:** Tổng thời gian kiểm tra DevTools không vượt quá 10 giây/lần.

---

## 4. Approaches Considered

### Approach 1: Tích hợp trực tiếp Playwright CDP trong Python — *LOẠI BỎ*
- **Mô tả:** Sử dụng thư viện `playwright` của Python để gắn listener CDP trực tiếp.
- **Lý do loại bỏ:** Người dùng đã quyết định chọn **Hướng 2** để bám sát và phát huy tối đa chuẩn giao tiếp Model Context Protocol (MCP) chính thức từ Google Chrome Team.

### Approach 2: Kết nối qua tiến trình MCP Server (`chrome-devtools-mcp` stdio client) — *ĐƯỢC CHỌN*
- **Mô tả:** Backend Python tạo tiến trình con `npx -y chrome-devtools-mcp --headless`, khởi tạo phiên làm việc MCP, gọi tuần tự các tool `navigate_page`, `list_console_messages`, `evaluate_script`, và đóng phiên an toàn.
- **Ưu điểm:** Đúng chuẩn kiến trúc MCP, độc lập với runtime Python, dễ mở rộng thêm các tool MCP khác trong tương lai.
- **Đánh đổi:** Cần xử lý cẩn thận I/O luồng stdio bất đồng bộ và kiểm soát tắt tiến trình an toàn.

---

## 5. Detailed Architecture & Design Decisions

### 5.1. DevTools MCP Client (`DevToolsMCPClient`)
- **Khởi tạo tiến trình:**
  ```python
  proc = await asyncio.create_subprocess_exec(
      "npx", "--yes", "chrome-devtools-mcp", "--headless",
      stdin=asyncio.subprocess.PIPE,
      stdout=asyncio.subprocess.PIPE,
      stderr=asyncio.subprocess.PIPE
  )
  ```
- **Chuẩn hóa thông điệp JSON-RPC:**
  - `initialize`: gửi phiên bản protocol và capabilities.
  - `tools/call`: gọi `navigate_page` truyền đường dẫn file HTML cục bộ (`file:///tmp/qa_temp_xxx.html`).
  - `tools/call`: gọi `list_console_messages` lọc các message có `level == "error"`.
  - `tools/call`: gọi `evaluate_script` thực thi đoạn script kiểm tra overflow trên Mobile:
    ```javascript
    () => {
      const hasOverflow = document.documentElement.scrollWidth > window.innerWidth;
      const brokenElements = [];
      document.querySelectorAll('*').forEach(el => {
        if (el.scrollWidth > window.innerWidth) brokenElements.push(el.tagName + (el.id ? '#' + el.id : ''));
      });
      return { hasOverflow, brokenElements: brokenElements.slice(0, 5) };
    }
    ```
- **Dọn dẹp tài nguyên:** Luôn gọi `proc.terminate()` trong khối `finally` để triệt tiêu tiến trình Chrome ngầm.

### 5.2. Tích hợp vào `Visual QA Agent` (`visual_qa_node`)
Quy trình thẩm định của `Visual QA` nâng cấp thành 2 tầng:
1. **Tầng 1 (Cú pháp tĩnh):** Chạy `validate_html_structure(code)` kiểm tra nhanh tính toàn vẹn thẻ.
2. **Tầng 2 (DevTools MCP Runtime Inspector):**
   - Lưu tạm file HTML vào thư mục an toàn trong workspace.
   - Kích hoạt `DevToolsMCPClient.inspect(html_path)`.
   - Thu thập danh sách lỗi:
     - `console_errors`: danh sách các lỗi JS nếu có.
     - `mobile_overflow`: cảnh báo nếu phần tử bị tràn viền trên màn hình 375px.
     - `render_passed`: True nếu không có lỗi console nghiêm trọng.
3. **Phản hồi báo cáo QA:** Trả về đối tượng `qa_report` giàu thông tin, đính kèm vào UAT Acceptance board tại Frontend.

---

## 6. What's Left to the Builder
- Viết module giao tiếp JSON-RPC stdio nhỏ gọn, không cần phụ thuộc thư viện bên ngoài cồng kềnh.
- Xử lý timeout an toàn nếu `npx` tải lần đầu tốn thời gian.
- Bổ sung unit test mô phỏng phản hồi MCP và kiểm thử thực tế trên một file HTML có chứa lỗi cố ý để chứng minh bắt được lỗi.
