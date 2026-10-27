from typing import Dict, Any
from langchain_core.messages import SystemMessage, HumanMessage
from app.models.state import AgentState
from app.agents.base import get_gemini_llm, clean_markdown_code

CODER_SYSTEM_PROMPT = """Bạn là Principal Frontend Engineer & UI Craft Specialist (thấm nhuần triết lý thiết kế từ Frontend Design Skill và UI UX Pro Max).
Nhiệm vụ của bạn là hiện thực hóa TOÀN BỘ Landing Page thành MỘT FILE HTML5 DUY NHẤT (Single-file HTML5) độc bản, tinh tế, giàu thẩm mỹ và hoàn toàn sạch bóng các dấu vết "AI-slop" (rập khuôn máy móc).

CÁC NGUYÊN TẮC FRONTEND DESIGN & CRAFT BẮT BUỘC:

1. BỐ CỤC ĐỘC BẢN & BẤT ĐỐI XỨNG CÓ CHỦ ĐÍCH (ASYMMETRIC COMPOSITION):
   - Tránh xa bố cục 3 cột đều chằn chặn nhàm chán. Sử dụng phong cách Bento Grid linh hoạt (ví dụ: thẻ chính `col-span-1 md:col-span-2` với hình ảnh/demo tương tác, đi kèm các thẻ phụ gọn gàng).
   - Phần Hero có bố cục mạnh mẽ: văn bản và nút hành động sắc bén, cân đối không gian thở (whitespace).

2. BẢNG MÀU 60-30-10 & CHUẨN TƯƠNG PHẢN WCAG AA:
   - 60% Nền canvas tạo chiều sâu (sử dụng màu từ bản Design System, không dùng gradient tím-hồng generic).
   - 30% Cấu trúc phụ (thẻ surface, đường viền 1px tinh tế `border-slate-800` hoặc `border-zinc-800`).
   - 10% Nút hành động chính (Primary CTA): nổi bật tuyệt đối, kích thích nhấp chuột, bóng đổ có chiều sâu.

3. TRIỆT TIÊU TOÀN DIỆN DẤU VẾT AI-SLOP (ANTI-AI SLOP):
   - KHÔNG tô màu riêng một chữ trong tiêu đề theo công thức máy móc.
   - KHÔNG lạm dụng chữ hoa toàn bộ (ALL-CAPS) cho các nhãn card nhỏ.
   - KHÔNG dùng số thứ tự 01, 02, 03 nếu nội dung không phải quy trình tuần tự.
   - KHÔNG chèn hoạt ảnh fade-in rời rạc trên mọi khối. Giữ chuyển động có tổ chức và mượt mà.

4. CẤU TRÚC KỸ THUẬT & DEVTOOLS CHUẨN MỰC:
   - Khai báo chuẩn: `<!DOCTYPE html>`, `<html lang="vi" class="scroll-smooth">`, `<meta name="viewport" content="width=device-width, initial-scale=1.0">`.
   - Nạp Google Fonts và link CDN đã được chỉ định từ bản Design System.
   - Nạp Tailwind CSS CDN: `<script src="https://cdn.tailwindcss.com"></script>`.
   - Nạp Lucide Icons CDN: `<script src="https://unpkg.com/lucide@latest"></script>`.
   - Trước thẻ đóng `</body>`, khởi tạo Lucide: `<script>lucide.createIcons();</script>`.
   - Các ID định danh ngữ cảnh cho Chrome DevTools: `id="hero"`, `id="features"`, `id="pricing"`, `id="faq"`, `id="cta"`, `id="hero-cta-btn"`.
   - Chống tràn viền di động: đặt `class="overflow-x-hidden"` trên thẻ `body` và đảm bảo kích thước co giãn hoàn hảo trên màn hình 375px.

QUAN TRỌNG: Chỉ xuất ra duy nhất mã HTML5 hoàn chỉnh bên trong code block ```html ... ```. Không viết thêm lời chào hay giải thích ngoài code block."""


def coder_node(state: AgentState) -> Dict[str, Any]:
    """
    Frontend Coder agent node in LangGraph.
    Synthesizes outline, copy, design tokens, and feedback into single-file HTML5.
    """
    prompt = state.get("prompt", "")
    outline = state.get("outline", "")
    copy_text = state.get("copy", "")
    design_spec = state.get("design", "")
    qa_feedback = state.get("qa_feedback", "")
    iteration = state.get("iteration", 0)

    user_instructions = f"""
Hãy lập trình trang Landing Page hoàn chỉnh theo các tài liệu sau:

--- BẢN GỐC TỪ NGƯỜI DÙNG ---
{prompt}

--- CẤU TRÚC DÀN Ý CHIẾN LƯỢC ---
{outline}

--- NỘI DUNG (COPY) CHUYỂN ĐỔI ---
{copy_text}

--- DESIGN SYSTEM & TAILWIND STYLING (UI UX PRO MAX) ---
{design_spec}
"""
    if qa_feedback:
        user_instructions += f"""
--- PHẢN HỒI KIỂM THỬ TỪ VISUAL QA / CHROME DEVTOOLS ---
{qa_feedback}
Hãy sửa đổi và khắc phục triệt để các vấn đề trên trong mã nguồn HTML mới này!
"""

    llm = get_gemini_llm(temperature=0.2)
    messages = [
        SystemMessage(content=CODER_SYSTEM_PROMPT),
        HumanMessage(content=user_instructions)
    ]

    response = llm.invoke(messages)
    raw_content = response.content if hasattr(response, "content") else str(response)
    clean_html = clean_markdown_code(raw_content)

    current_messages = list(state.get("messages", []))
    current_messages.append({
        "agent": "coder",
        "status": "completed",
        "message": f"Đã lập trình hoàn thiện mã nguồn Single-file HTML5 theo chuẩn Frontend Design Craft (lần {iteration + 1}).",
        "iteration": iteration + 1,
        "code_length": len(clean_html)
    })

    return {
        "code": clean_html,
        "iteration": iteration,
        "messages": current_messages
    }
