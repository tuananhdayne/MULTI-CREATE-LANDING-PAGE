# Design Specification: Human-in-the-Loop Milestone Workflow (IT Department Model)

**Date:** 2026-10-27  
**Author:** Antigravity & User  
**Status:** In Review  
**Target File:** `docs/superpowers/specs/2026-10-27-human-in-the-loop-milestone-workflow-design.md`

---

## 1. Intent and the Why

### Context
Hệ thống hiện tại vận hành theo cơ chế tự động hóa tuyến tính (linear automated pipeline): khi người dùng nhập một câu prompt, 5 agent (`Strategist -> Copywriter -> Designer -> Coder -> Visual QA`) tự động chạy một mạch từ đầu đến cuối mà không có bất kỳ điểm dừng hoặc tương tác nào với người dùng.

### The Problem
Mô hình "black-box" này không phản ánh đúng cách làm việc thực tế của một phòng ban IT hoặc agency chuyên nghiệp. Khách hàng/đối tác (Product Owner / Client) bị cô lập hoàn toàn:
- Không được làm rõ yêu cầu nghiệp vụ (briefing), dẫn đến việc agent tự đưa ra giả định chủ quan.
- Không được duyệt concept và định hướng giao diện/tone giọng trước khi đội ngũ lập trình bắt tay vào viết code.
- Không có quy trình nghiệm thu bàn giao (UAT) với vòng lặp phản hồi có cấu trúc.

### The Goal
Chuyển đổi hệ thống từ cơ chế "máy sinh code một chiều" sang mô hình **"Phòng ban IT cộng tác thông minh (Human-in-the-Loop Milestone Workflow)"**, thiết lập 3 trạm kiểm soát (checkpoints) chặt chẽ giữa đội ngũ Agent và Đối tác.

---

## 2. Goals, Non-Goals, and Anti-Goals

### Goals
1. **Chặng 1 - Khảo sát & Chốt Brief (BA/PO Agent):** Khi nhận ý tưởng ban đầu, agent BA đóng vai trò Business Analyst phỏng vấn đối tác bằng 2–4 câu hỏi trọng tâm (khách hàng mục tiêu, phong cách thương hiệu, hành vi chuyển đổi chính), cho phép đối tác xác nhận hoặc tùy chỉnh trước khi sinh kế hoạch.
2. **Chặng 2 - Trình bày & Duyệt Concept (Strategist & Designer):** Đội ngũ lập một "Bản Đề Xuất Kế Hoạch & Thiết Kế" trực quan (Outline cấu trúc khối, Tone giọng, Bảng màu Tailwind, Font chữ mẫu) và tạm dừng để đối tác phê duyệt hoặc gửi yêu cầu tinh chỉnh trước khi code.
3. **Chặng 3 - Lập trình & Nghiệm thu UAT (Coder, QA & Partner):** Sinh trang hiển thị trên Live Preview, hỗ trợ vòng lặp phản hồi nghiệm thu (UAT feedback loop) để đối tác nhận xét hoặc chỉnh sửa trước khi xuất mã nguồn cuối cùng.
4. **Bảo tồn khả năng Click-to-Inspect:** Tích hợp mượt mà với tính năng chỉnh sửa từng phần tử qua Chrome DevTools MCP đã có.

### Non-Goals
- Không xây dựng một hệ thống chatroom hỗn tạp dạng group chat Slack tự do thiếu cấu trúc.
- Không hỗ trợ phân quyền nhiều người dùng doanh nghiệp phức tạp (RBAC) trong phạm vi hiện tại (tập trung vào 1 đối tác / session).

### Anti-Goals
- Không duy trì trạng thái "black-box waterfall" tự chạy không thể tạm dừng.
- Không làm gián đoạn hoặc mất trạng thái dự án khi người dùng tải lại trang web hoặc tạm dừng suy nghĩ.

---

## 3. Constraints & Technical Boundaries
- **Backend:** FastAPI, Python 3.10+, LangGraph, Pydantic v2 schemas.
- **Frontend:** React 18, Vite, Tailwind CSS, Lucide icons.
- **LLM Gateway:** 9router gateway (`http://localhost:20128/v1`) sử dụng model `ag/gemini-3.8-flash-high`.
- **Security:** Tuyệt đối không để lộ API keys, không commit file `.env`.
- **State Persistence:** Sử dụng `ProjectService` quản lý session trong bộ nhớ kèm checkpoint để lưu trữ toàn bộ trạng thái qua từng chặng (brief, proposal, code, uat history).

---

## 4. Approaches Considered

### Approach 1: Mô hình Chặng Độc lập có Kiểm soát (Milestone-Driven Workflow) — *ĐƯỢC CHỌN LÀM MẶC ĐỊNH*
- **Mô tả:** Chia giao diện và API thành 3 chặng tuần tự:
  1. *Chặng 1 (Briefing):* Card phỏng vấn BA tương tác (hoặc nút "Bỏ qua & Tạo nhanh" - Express Auto-pilot).
  2. *Chặng 2 (Proposal):* Thẻ đề xuất Kế hoạch & Thiết kế kèm nút `[Phê duyệt]` hoặc `[Yêu cầu chỉnh sửa]`.
  3. *Chặng 3 (Build & UAT):* Live Preview kèm bảng kiểm tra nghiệm thu UAT và hộp thoại gửi phản hồi lặp.
- **Quyết định thiết kế:** Quy trình 3 chặng cộng tác chuẩn IT là **chế độ mặc định** của hệ thống. Đồng thời cung cấp tùy chọn "Tạo nhanh (Auto-pilot 1-Click)" ở thanh điều hướng để người dùng có thể kích hoạt chế độ sinh tự động tức thì khi cần.
- **Ưu điểm:** Giao diện trực quan, chuyên nghiệp, kiểm soát trạng thái chắc chắn, phân định trách nhiệm rõ ràng theo chuẩn Agile/Scrum.
- **Đánh đổi:** Cần thiết kế các thẻ tương tác cho từng chặng trên Frontend.

### Approach 2: Mô hình Phòng họp Chatbox Nhóm (Interactive Team Chat) — *LOẠI BỎ*
- **Mô tả:** Mô phỏng một nhóm chat Slack/Teams nơi các agent và đối tác nhắn tin qua lại tự do.
- **Lý do loại bỏ:** Dễ gây rối mắt khi các tài liệu thiết kế và code HTML dài làm trôi thông tin quan trọng; thiếu tính kỷ luật so với các văn bản ký duyệt (sign-off) chính thức.

---

## 5. Detailed Architecture & Workflow

### 5.1. Session State Schema (`ProjectSession`)
Mỗi phiên làm việc được gắn một `session_id` với các trạng thái tương ứng:
- `status`: `"BRIEFING"` | `"BRIEF_READY"` | `"PROPOSING"` | `"PROPOSAL_REVIEW"` | `"BUILDING"` | `"UAT_REVIEW"` | `"COMPLETED"`
- `initial_prompt`: Ý tưởng ban đầu của đối tác.
- `brief`:
  - `questions`: Danh sách câu hỏi BA đã tạo (kèm gợi ý trắc nghiệm/nhanh).
  - `answers`: Câu trả lời của đối tác.
  - `confirmed_brief`: Tóm tắt yêu cầu cốt lõi đã chốt.
- `proposal`:
  - `target_audience`: Chân dung khách hàng mục tiêu.
  - `value_proposition`: Tuyên ngôn giá trị cốt lõi.
  - `sections_outline`: Danh sách các section dự kiến (Hero, Features, Social Proof, Pricing, FAQ, CTA).
  - `design_system`: Palette màu (Primary, Secondary, Accent, Background), Typography, Phong cách (Glassmorphism, Minimalist, Corporate, v.v.).
  - `tone_of_voice`: Giọng văn.
- `build`:
  - `html_code`: Mã nguồn HTML5 + Tailwind CSS hoàn chỉnh.
  - `qa_report`: Báo cáo thẩm định chất lượng từ Visual QA.
- `uat_history`: Danh sách các lượt góp ý của đối tác và kết quả tinh chỉnh tương ứng.

---

### 5.2. Chặng 1: Khảo sát & Chốt Brief (BA/PO Agent)
1. **Khởi tạo:** Đối tác nhập ý tưởng ngắn (ví dụ: *"Landing page cho app học tiếng Anh AI cho trẻ em"*).
2. **BA Agent xử lý:** Agent `BAAnalyst` phân tích ý tưởng, nhận diện các điểm còn mơ hồ và tạo ra 3 câu hỏi trắc nghiệm/gợi ý nhanh:
   - *Câu 1:* Tệp người dùng cụ thể là ai? (Ví dụ: Phụ huynh có con 4-8 tuổi hay học sinh tự học?)
   - *Câu 2:* Phong cách cảm xúc mong muốn? (Ví dụ: Tươi vui nhiều màu sắc hay Hiện đại tối giản cao cấp?)
   - *Câu 3:* Mục tiêu chuyển đổi chính trên trang? (Ví dụ: Tải app miễn phí, Đăng ký dùng thử 7 ngày, hay Đặt lịch tư vấn?)
3. **Đối tác tương tác:** Đối tác chọn gợi ý hoặc gõ nhanh câu trả lời -> Nhấn nút **"Chốt Yêu Cầu Brief"**.

---

### 5.3. Chặng 2: Trình bày & Duyệt Concept (Strategist & Designer)
1. **Agent phối hợp:**
   - `Strategist`: Xây dựng cấu trúc các section chuyển đổi tối ưu (CRO Outline).
   - `Designer`: Tạo bảng màu phong thủy/thương hiệu, font chữ, phong cách thị giác.
2. **Hiển thị Thẻ Đề Xuất (Proposal Card):**
   - Bản xem trước bảng màu mẫu (Color chips).
   - Danh sách khối nội dung kèm mục đích từng khối.
   - Giọng văn thương hiệu.
3. **Hành động của Đối tác:**
   - **Nút [Phê Duyệt & Bắt Đầu Lập Trình]:** Chuyển sang Chặng 3.
   - **Nút [Yêu Cầu Thay Đổi]:** Nhập ghi chú (Ví dụ: *"Đổi màu chủ đạo sang xanh navy thanh lịch hơn, thêm khối bảng giá so sánh 3 gói"*) -> Agent Designer & Strategist cập nhật lại đề xuất trong vòng vài giây.

---

### 5.4. Chặng 3: Lập trình & Nghiệm thu UAT (Coder, QA & Đối tác)
1. **Coder & Visual QA:** Lập trình mã nguồn duy nhất HTML5 + Tailwind CSS theo đúng Proposal đã duyệt, QA kiểm tra hợp lệ.
2. **Hiển thị Live Preview:** Trang web được dựng lập tức trong khung xem trước với công cụ chuyển Viewport (Desktop / Tablet / Mobile).
3. **Bảng Nghiệm Thu UAT (Acceptance Board):**
   - Hộp thoại gửi phản hồi tinh chỉnh tổng thể (Ví dụ: *"Nút CTA trên cùng cho to hơn một chút, sửa lại tiêu đề Hero cho giật gân hơn"*).
   - Tích hợp công cụ Click-to-Inspect DevTools để nhấp trực tiếp vào phần tử trên màn hình và sửa ngay lập tức.
   - **Nút [Ký Duyệt Nghiệm Thu - Xuất Bản]:** Đóng phiên, cho phép tải file `index.html` hoặc sao chép mã nguồn sạch.

---

## 6. API Specifications (FastAPI)

1. `POST /api/project/start-brief`:
   - Input: `{ prompt: string }`
   - Output: `{ session_id: string, questions: [...] }`
2. `POST /api/project/submit-brief`:
   - Input: `{ session_id: string, answers: Record<string, string> }`
   - Output: `{ session_id: string, confirmed_brief: object }`
3. `POST /api/project/generate-proposal`:
   - Input: `{ session_id: string, feedback?: string }`
   - Output: `SSE Stream` hoặc JSON chứa `proposal` (sections, colors, tone).
4. `POST /api/project/approve-proposal`:
   - Input: `{ session_id: string }`
   - Output: `{ session_id: string, status: "BUILDING" }`
5. `POST /api/project/build-code`:
   - Input: `{ session_id: string }`
   - Output: `SSE Stream` trả về tiến độ Coder -> Visual QA -> Mã nguồn HTML.
6. `POST /api/project/uat-feedback`:
   - Input: `{ session_id: string, feedback: string, target_element_id?: string }`
   - Output: `SSE Stream` trả về mã nguồn sau khi tinh chỉnh.

---

## 7. Frontend UI Components Architecture

- `WorkspaceLayout`: Thanh điều hướng tiến độ (Stepper: `1. Khảo sát Brief` -> `2. Duyệt Concept` -> `3. Nghiệm thu & Live Preview`).
- `BriefSurveyCard`: Form hiển thị câu hỏi từ BA với các pill chọn nhanh và ô nhập tùy ý.
- `ProposalReviewCard`: Thẻ trình bày bảng màu, font chữ, danh sách khối trang web kèm 2 nút phê duyệt / góp ý.
- `LivePreview` & `UATFeedbackPanel`: Khung hiển thị trang web trực tiếp, tích hợp chế độ soi phần tử (Click-to-Inspect) và khung gửi phản hồi nghiệm thu.

---

## 8. What's Left to the Builder
- Triển khai cụ thể các prompt cho `BAAnalyst` và `ProposalGenerator`.
- Tối ưu hóa thời gian sinh proposal bằng cách stream trực tiếp các trường dữ liệu.
- Thiết kế giao diện thẻ (Proposal Card) đồng bộ với bảng màu Dark Mode hiện đại của hệ thống.
