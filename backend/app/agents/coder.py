from typing import Dict, Any
from langchain_core.messages import SystemMessage, HumanMessage
from app.models.state import AgentState
from app.agents.base import get_gemini_llm, clean_markdown_code

CODER_SYSTEM_PROMPT = """Bạn là Staff Frontend Engineer & Tailwind CSS Expert.
Nhiệm vụ của bạn là hiện thực hóa TOÀN BỘ Landing Page thành MỘT FILE HTML5 DUY NHẤT (Single-file HTML5) hoàn chỉnh, đẹp xuất sắc, không cắt xén, không dùng placeholder sơ sài.

Yêu cầu kỹ thuật bắt buộc:
1. Cấu trúc chuẩn HTML5:
   - `<!DOCTYPE html>`
   - `<html lang="vi" class="scroll-smooth">`
   - `<head>` đầy đủ thẻ meta viewport, charset utf-8, title hấp dẫn.
   - Nạp Google Fonts (Plus Jakarta Sans hoặc Inter).
   - Nạp Tailwind CSS CDN: `<script src="https://cdn.tailwindcss.com"></script>`
   - Nạp Lucide Icons CDN: `<script src="https://unpkg.com/lucide@latest"></script>`
2. Nội dung và Thẩm mỹ:
   - Sử dụng chính xác văn bản từ bản COPYWRITER.
   - Áp dụng đầy đủ bảng màu, gradient, glassmorphism, và typography từ bản DESIGN SYSTEM.
   - Responsive 100% trên cả Mobile (sm:), Tablet (md:), và Desktop (lg:, xl:).
   - Thêm micro-interactions (hover, transitions mượt mà).
3. DOM & IDs cho DevTools:
   - Mỗi section chính phải có ID rõ ràng: `id="hero"`, `id="features"`, `id="how-it-works"`, `id="testimonials"`, `id="pricing"`, `id="faq"`, `id="cta"`.
   - Các nút bấm quan trọng cần có ID hoặc class định danh (ví dụ `id="hero-cta-btn"`).
4. Khởi tạo Icon:
   - Trước thẻ đóng `</body>`, phải có đoạn script khởi tạo icons:
     `<script>lucide.createIcons();</script>`

QUAN TRỌNG: Chỉ xuất ra duy nhất mã HTML5 hoàn chỉnh bên trong code block ```html ... ```. Không viết lời chào hoặc giải thích ngoài code block."""


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

--- DESIGN SYSTEM & TAILWIND STYLING ---
{design_spec}
"""
    if qa_feedback:
        user_instructions += f"""
--- PHẢN HỒI KIỂM THỬ TỪ QA (CẦN SỬA ĐỔI NGAY) ---
{qa_feedback}
Vui lòng khắc phục triệt để các vấn đề trên trong phiên bản này!
"""

    llm = get_gemini_llm(temperature=0.4)
    messages = [
        SystemMessage(content=CODER_SYSTEM_PROMPT),
        HumanMessage(content=user_instructions)
    ]

    response = llm.invoke(messages)
    raw_content = response.content if hasattr(response, "content") else str(response)
    clean_code = clean_markdown_code(raw_content)

    current_messages = list(state.get("messages", []))
    msg_status = "Lập trình viên đã tạo xong mã nguồn HTML5 hoàn chỉnh." if iteration == 0 else f"Lập trình viên đã sửa đổi mã nguồn theo phản hồi QA (vòng {iteration})."
    current_messages.append({
        "agent": "coder",
        "status": "completed",
        "message": msg_status,
        "code_length": len(clean_code)
    })

    return {
        "code": clean_code,
        "messages": current_messages
    }
