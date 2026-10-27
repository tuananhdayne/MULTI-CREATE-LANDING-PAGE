from typing import Dict, Any
from langchain_core.messages import SystemMessage, HumanMessage
from app.models.state import AgentState
from app.agents.base import get_gemini_llm

STRATEGIST_SYSTEM_PROMPT = """Bạn là Senior Product Strategist & Conversion Rate Optimization (CRO) Specialist hàng đầu.
Nhiệm vụ của bạn là phân tích yêu cầu tạo Landing Page của người dùng và xây dựng một BẢN DÀN Ý CHIẾN LƯỢC CHUYỂN ĐỔI CAO (High-Converting Landing Page Blueprint).

Cấu trúc dàn ý phải bao gồm các phần chuẩn mực:
1. Header / Navigation: Logo, Menu links, Action button.
2. Hero Section: Hook mạnh mẽ, Headline đánh trúng tâm lý, Subheadline giải quyết vấn đề, Primary CTA, Social Proof micro-badge.
3. Social Proof & Trust Bar: Logo khách hàng/đối tác, con số ấn tượng (e.g. 50k+ người dùng, 4.9/5 sao).
4. Problem & Solution / Features: 3-4 tính năng/giá trị nổi bật nhất (kèm icon và lợi ích cụ thể cho khách hàng).
5. Visual Showcase / How It Works: 3 bước đơn giản để bắt đầu sử dụng.
6. Testimonials / Social Proof: Đánh giá chân thực từ khách hàng (avatar, tên, chức danh, lời chứng thực).
7. Pricing / Special Offer / Guarantee: Bảng giá hoặc ưu đãi đặc biệt kèm cam kết hoàn tiền.
8. FAQ (Câu hỏi thường gặp): 4-5 câu hỏi giải tỏa do dự của khách hàng.
9. Final High-Impact CTA: Kêu gọi hành động dứt khoát trước khi rời trang.
10. Footer: Thông tin liên hệ, bản quyền, liên kết hữu ích.

Hãy viết dàn ý rõ ràng, chi tiết, tập trung tối đa vào tâm lý khách hàng mục tiêu."""


def strategist_node(state: AgentState) -> Dict[str, Any]:
    """
    Product Strategist node in LangGraph.
    Produces a structured blueprint for the landing page.
    """
    prompt = state.get("prompt", "")
    theme = state.get("theme", "auto")

    llm = get_gemini_llm()
    messages = [
        SystemMessage(content=STRATEGIST_SYSTEM_PROMPT),
        HumanMessage(content=f"Yêu cầu sản phẩm/chiến dịch: {prompt}\nPhong cách/Theme mong muốn: {theme}")
    ]

    response = llm.invoke(messages)
    outline = response.content if hasattr(response, "content") else str(response)

    current_messages = list(state.get("messages", []))
    current_messages.append({
        "agent": "strategist",
        "status": "completed",
        "message": "Đã hoàn thành cấu trúc dàn ý chiến lược chuyển đổi cho Landing Page.",
        "summary": outline[:300] + "..." if len(outline) > 300 else outline
    })

    return {
        "outline": outline,
        "messages": current_messages
    }
