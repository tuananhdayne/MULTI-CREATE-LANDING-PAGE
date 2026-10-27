from typing import Dict, Any
from langchain_core.messages import SystemMessage, HumanMessage
from app.models.state import AgentState
from app.agents.base import get_gemini_llm

COPYWRITER_SYSTEM_PROMPT = """Bạn là Chuyên gia viết nội dung bán hàng chuyển đổi cao (Elite Conversion Copywriter).
Dựa trên Dàn ý chiến lược và Yêu cầu của người dùng, hãy viết toàn bộ VĂN BẢN (COPY) hoàn chỉnh cho từng phần của Landing Page:

1. Tiêu đề (Headlines): Hấp dẫn, khơi gợi tò mò, đánh thẳng vào nỗi đau và lợi ích cốt lõi.
2. Tiêu đề phụ (Subheadlines): Ngắn gọn, giải thích rõ sản phẩm làm được gì và vì sao nên chọn.
3. Kêu gọi hành động (CTAs): Sử dụng động từ mạnh mẽ, hướng tới hành động ngay (e.g. "Bắt đầu miễn phí trong 30 giây", "Nhận tư vấn ngay", "Trải nghiệm không rủi ro").
4. Mô tả tính năng / Lợi ích: Viết theo cấu trúc Tính năng -> Lợi ích thực tế mang lại cho khách hàng.
5. Lời chứng thực (Testimonials): 3 đánh giá tự nhiên, có số liệu cụ thể (e.g. "Tiết kiệm 4 giờ mỗi ngày", "Tăng 35% doanh thu").
6. FAQ: 4 câu hỏi trả lời ngắn gọn, tạo niềm tin tuyệt đối.

Nội dung phải tự nhiên, chuyên nghiệp, hấp dẫn bằng Tiếng Việt chuẩn (hoặc ngôn ngữ được yêu cầu)."""


def copywriter_node(state: AgentState) -> Dict[str, Any]:
    """
    Copywriter agent node in LangGraph.
    Generates high-converting marketing copy for each section.
    """
    prompt = state.get("prompt", "")
    outline = state.get("outline", "")

    llm = get_gemini_llm()
    messages = [
        SystemMessage(content=COPYWRITER_SYSTEM_PROMPT),
        HumanMessage(content=f"Yêu cầu ban đầu: {prompt}\n\nDàn ý chiến lược đã duyệt:\n{outline}")
    ]

    response = llm.invoke(messages)
    copy_text = response.content if hasattr(response, "content") else str(response)

    current_messages = list(state.get("messages", []))
    current_messages.append({
        "agent": "copywriter",
        "status": "completed",
        "message": "Đã soạn thảo toàn bộ nội dung chuyển đổi (Headlines, CTAs, Benefits, FAQs).",
        "summary": copy_text[:300] + "..." if len(copy_text) > 300 else copy_text
    })

    return {
        "copy": copy_text,
        "messages": current_messages
    }
