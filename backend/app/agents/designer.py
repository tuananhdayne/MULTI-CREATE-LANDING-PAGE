from typing import Dict, Any
from langchain_core.messages import SystemMessage, HumanMessage
from app.models.state import AgentState
from app.agents.base import get_gemini_llm

DESIGNER_SYSTEM_PROMPT = """Bạn là Lead UI/UX Designer & Design System Architect hàng đầu.
Nhiệm vụ của bạn là định hình HỆ THỐNG THIẾT KẾ THỊ GIÁC (Visual Design System & Design Tokens) cho Landing Page bằng Tailwind CSS hiện đại:

1. Bảng màu (Color Palette):
   - Background & Surface: Dark mode cao cấp (slate-950, slate-900, slate-800/50 kèm glassmorphism) hoặc Light mode thanh lịch, sạch sẽ.
   - Primary & Accent Colors: Màu chủ đạo nổi bật (e.g. Indigo, Violet, Emerald, hoặc Amber), kết hợp gradient hiện đại (e.g. `bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500`).
   - Text Hierarchy: Tiêu đề rõ ràng, tương phản cao (`text-slate-100`, `text-slate-400`).

2. Typography & Fonts:
   - Google Font cao cấp (Inter, Outfit, hoặc Plus Jakarta Sans).
   - Quy tắc kích thước: `text-5xl lg:text-7xl font-extrabold tracking-tight` cho Hero.

3. Hiệu ứng thị giác & Micro-interactions:
   - Glassmorphism: `backdrop-blur-md bg-white/5 border border-white/10`.
   - Hover Effects: `hover:scale-105 hover:shadow-indigo-500/25 transition-all duration-300`.
   - Nút CTA phát sáng (Glow / Shadow): `shadow-lg shadow-indigo-500/30`.

4. Iconography:
   - Sử dụng Lucide Icons (nạp qua CDN).

Hãy xuất ra bản thiết kế chi tiết bao gồm các Tailwind classes cụ thể cho từng thành phần (Navbar, Hero, Cards, Buttons, Footer)."""


def designer_node(state: AgentState) -> Dict[str, Any]:
    """
    UI/UX Designer agent node in LangGraph.
    Defines the visual theme, colors, typography, and styling rules.
    """
    prompt = state.get("prompt", "")
    theme = state.get("theme", "auto")
    outline = state.get("outline", "")

    llm = get_gemini_llm()
    messages = [
        SystemMessage(content=DESIGNER_SYSTEM_PROMPT),
        HumanMessage(content=f"Yêu cầu: {prompt}\nTheme: {theme}\nCấu trúc:\n{outline}")
    ]

    response = llm.invoke(messages)
    design_spec = response.content if hasattr(response, "content") else str(response)

    current_messages = list(state.get("messages", []))
    current_messages.append({
        "agent": "designer",
        "status": "completed",
        "message": "Đã thiết lập Design System, bảng màu Tailwind, hiệu ứng Glassmorphism và Typography.",
        "summary": design_spec[:300] + "..." if len(design_spec) > 300 else design_spec
    })

    return {
        "design": design_spec,
        "messages": current_messages
    }
