from typing import Dict, Any
from langchain_core.messages import SystemMessage, HumanMessage
from app.models.state import AgentState
from app.agents.base import get_gemini_llm
from app.services.design_intelligence import get_recommended_design_system

DESIGNER_SYSTEM_PROMPT = """Bạn là Principal UI/UX Designer & Design System Lead (sở hữu tri thức kết hợp từ UI UX Pro Max và Frontend Design Skill).
Nhiệm vụ của bạn là kiến tạo một HỆ THỐNG THIẾT KẾ ĐỘC BẢN, GIÀU TÍNH NGHỆ THUẬT VÀ TỐI ƯU CHUYỂN ĐỔI CHO LANDING PAGE.

QUY TẮC CỐT LÕI (UI UX PRO MAX & FRONTEND DESIGN):

1. TỶ LỆ PHỐI MÀU 60-30-10 & CHUẨN TƯƠNG PHẢN WCAG AA:
   - 60% Màu chủ đạo Canvas/Nền: Nền chính tạo không gian thở (ví dụ Deep Slate #0F172A hoặc Editorial Cream #FAFAF9).
   - 30% Cấu trúc phụ: Thẻ (Card surface), Đường viền (Borders 1px), Typography nội dung.
   - 10% Điểm nhấn chuyển đổi (Accent/Primary CTA): Màu sắc tương phản cao, nổi bật hoàn toàn để thu hút ánh nhìn vào nút hành động chính.
   - Đảm bảo tỷ lệ tương phản văn bản tối thiểu 4.5:1 so với nền (WCAG AA).

2. TYPOGRAPHY ĐẲNG CẤP & CÓ CHỦ ĐÍCH:
   - Chọn cặp Google Fonts phù hợp với ngành nghề (ví dụ: Outfit + Inter cho SaaS, Space Grotesk + Plus Jakarta Sans cho Dev/Bento, Syne + DM Sans cho Editorial).
   - Thiết lập phân cấp kích thước rõ ràng, không lạm dụng chữ hoa toàn bộ (ALL-CAPS) cho các nhãn nhỏ.

3. TRIỆT TIÊU DẤU HIỆU AI RẬP KHUÔN (ANTI-AI SLOP):
   - Tuyệt đối KHÔNG sử dụng gradient tím-hồng generic mòn mắt.
   - KHÔNG tô màu riêng một chữ đơn lẻ trong tiêu đề theo thói quen máy móc.
   - KHÔNG gắn nhãn số 01, 02, 03 nếu nội dung không phải quy trình tuần tự.
   - Bố cục bất đối xứng có chủ đích (ví dụ phong cách Bento Grid hoặc Asymmetric Columns) thay vì chỉ xếp các thẻ 3 cột nhàm chán.
   - Animation có tổ chức (orchestrated motion): chỉ một hiệu ứng chuyển động ấn tượng khi vào trang, tránh hoạt ảnh rung lắc/fade-in rải rác trên mọi phần tử.

4. BẢN ĐẶC TẢ CHI TIẾT CẦN XUẤT RA:
   - Phong cách giao diện (UI Style: Bento Grid / Modern SaaS / Dark Cyberpunk / Minimal Editorial).
   - Bảng mã màu cụ thể (HEX codes kèm class Tailwind tương ứng).
   - Cặp font Google Fonts và link nhúng CDN.
   - Các class Tailwind cụ thể cho từng thành phần: Header, Hero, Bento/Feature Cards, Buttons, Footer."""


def designer_node(state: AgentState) -> Dict[str, Any]:
    """
    UI/UX Designer agent node in LangGraph.
    Infused with UI UX Pro Max intelligence and Frontend Design principles.
    """
    prompt = state.get("prompt", "")
    theme = state.get("theme", "auto")
    outline = state.get("outline", "")

    # Retrieve expert design system recommendations based on the prompt
    recommended_ds = get_recommended_design_system(prompt)
    style_info = recommended_ds["style"]
    palette = recommended_ds["color_palette"]
    typo = recommended_ds["typography"]

    llm = get_gemini_llm()
    messages = [
        SystemMessage(content=DESIGNER_SYSTEM_PROMPT),
        HumanMessage(content=f"""YÊU CẦU DỰ ÁN: {prompt}
THEME YÊU CẦU: {theme}

GỢI Ý TỪ THƯ VIỆN UI UX PRO MAX:
- Phong cách khuyên dùng: {style_info['name']} ({style_info['keywords']})
- Bố cục đề xuất: {recommended_ds['layout_pattern']}
- Bảng màu 60-30-10:
  + Primary CTA (10%): {palette['primary']}
  + Secondary Surface (30%): {palette['secondary']}
  + Accent Highlight: {palette['accent']}
  + Canvas Background (60%): {palette['background']}
  + Card Surface: {palette['surface']}
- Cặp Typography đề xuất: {typo['heading']} + {typo['body']}
  Google Fonts URL: {typo['google_fonts_url']}

CẤU TRÚC DÀN Ý:
{outline}

Hãy xuất ra bản đặc tả Design System hoàn chỉnh, sắc nét và tuân thủ các quy tắc trên.""")
    ]

    response = llm.invoke(messages)
    design_spec = response.content if hasattr(response, "content") else str(response)

    current_messages = list(state.get("messages", []))
    current_messages.append({
        "agent": "designer",
        "status": "completed",
        "message": f"Đã thiết lập Design System đẳng cấp ({style_info['name']}) theo chuẩn UI UX Pro Max & Frontend Design.",
        "summary": design_spec[:300] + "..." if len(design_spec) > 300 else design_spec
    })

    return {
        "design": design_spec,
        "messages": current_messages
    }
