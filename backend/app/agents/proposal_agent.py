import json
import re
from typing import Optional, Any
from langchain_core.messages import SystemMessage, HumanMessage
from app.agents.base import get_gemini_llm
from app.schemas.session import DesignProposal
from app.services.design_intelligence import get_recommended_design_system

PROPOSAL_SYSTEM_PROMPT = """Bạn là Giám đốc Nghệ thuật & Trưởng phòng Chiến lược CRO (Creative Director & CRO Lead) tại Agency phát triển Landing Page, kết hợp tiêu chuẩn thiết kế từ UI UX Pro Max và Frontend Design Skill.
Nhiệm vụ của bạn: Từ thông tin Briefing đã được đối tác xác nhận, hãy thiết lập một Bản Đề Xuất Kế Hoạch & Thiết Kế (Design & Architecture Proposal) độc bản, tinh tế để trình cho đối tác phê duyệt trước khi lập trình.

QUY TẮC THIẾT KẾ (UI UX PRO MAX & FRONTEND DESIGN):
1. Phối màu theo quy tắc 60-30-10:
   - `background`: Màu canvas nền chính (60% không gian).
   - `surface`: Màu nền thẻ card/khối nổi bật.
   - `secondary`: Màu cấu trúc phụ (đường viền, badge thứ cấp).
   - `primary`: Màu chuyển đổi chính (Primary CTA) tương phản cao WCAG AA.
   - `accent`: Điểm nhấn thị giác bổ trợ.
   Tất cả 5 màu bắt buộc phải là mã HEX hợp lệ (#RRGGBB).
2. Typography:
   - Sử dụng các cặp font Google Fonts chất lượng cao (ví dụ: Outfit + Inter, Space Grotesk + Plus Jakarta Sans, hoặc Syne + DM Sans).
3. Kiến trúc sections:
   - Tối thiểu 5-6 sections có cấu trúc logic (Hero, Social Proof, Features, Pricing/Offer, FAQ, Final CTA).
4. Định dạng trả về:
   - Trả về ĐÚNG JSON Object (không văn bản dẫn xuất thừa):
{
  "target_audience": "Mô tả chi tiết chân dung khách hàng",
  "value_proposition": "Tuyên ngôn giá trị cốt lõi giải quyết nỗi đau của khách",
  "sections_outline": [
    {"id": "hero", "name": "Hero Section", "purpose": "Thu hút sự chú ý kèm CTA nổi bật"},
    {"id": "social_proof", "name": "Social Proof & Trust Badges", "purpose": "Xây dựng uy tín"},
    {"id": "features", "name": "Core Features / Bento Showcase", "purpose": "Trình diễn tính năng vượt trội"},
    {"id": "pricing", "name": "Pricing / Comparison Table", "purpose": "Minh bạch chi phí và kích thích chuyển đổi"},
    {"id": "faq", "name": "FAQ Section", "purpose": "Giải tỏa mọi rào cản cuối cùng"},
    {"id": "final_cta", "name": "Final CTA Banner", "purpose": "Chốt chuyển đổi mạnh mẽ"}
  ],
  "color_palette": {
    "primary": "#2563EB",
    "secondary": "#1E293B",
    "accent": "#10B981",
    "background": "#0F172A",
    "surface": "#1E293B"
  },
  "typography": {
    "heading": "Outfit, sans-serif",
    "body": "Inter, sans-serif"
  },
  "tone_of_voice": "Chuyên nghiệp, tin cậy, truyền cảm hứng và hướng tới hành động",
  "revision_notes": "Tóm tắt các điểm đã điều chỉnh nếu có feedback"
}
"""

class ProposalAgent:
    def __init__(self, model_name: Optional[str] = "ag/gemini-3.8-flash"):
        self.llm = get_gemini_llm(model_name=model_name, temperature=0.4)

    async def generate_proposal(
        self,
        prompt: str,
        brief_answers: dict[str, str],
        feedback: Optional[str] = None
    ) -> DesignProposal:
        # Get tailored UI UX Pro Max baseline
        brand_style = brief_answers.get('brand_style', '')
        ds_rec = get_recommended_design_system(prompt, brand_style)
        rec_palette = ds_rec["color_palette"]
        rec_typo = ds_rec["typography"]

        context = (
            f"Dự án: {prompt}\n"
            f"Brief đối tác đã chốt:\n"
            f"- Đối tượng khách hàng: {brief_answers.get('target_audience', 'Khách hàng quan tâm')}\n"
            f"- Phong cách thương hiệu: {brand_style or 'Hiện đại, chuyên nghiệp'}\n"
            f"- Mục tiêu chuyển đổi: {brief_answers.get('conversion_goal', 'Đăng ký nhận tư vấn')}\n"
            f"\nGỢI Ý THIẾT KẾ (UI UX PRO MAX BASELINE):\n"
            f"- Palette 60-30-10: Primary={rec_palette['primary']}, Background={rec_palette['background']}, Surface={rec_palette['surface']}\n"
            f"- Typography: Heading={rec_typo['heading']}, Body={rec_typo['body']}\n"
        )
        if feedback:
            context += f"\nÝ KIẾN ĐỐI TÁC YÊU CẦU ĐIỀU CHỈNH:\n\"{feedback}\"\nHãy tích hợp các yêu cầu này vào bản đề xuất mới."

        messages = [
            SystemMessage(content=PROPOSAL_SYSTEM_PROMPT),
            HumanMessage(content=f"{context}\n\nHãy tạo bản đề xuất Design & Architecture dạng JSON.")
        ]

        try:
            response = await self.llm.ainvoke(messages)
            content = response.content if hasattr(response, "content") else str(response)

            json_match = re.search(r"\{\s*\"target_audience\"[\s\S]*\}\s*", content)
            raw_json = json_match.group(0) if json_match else content.strip()
            data = json.loads(raw_json)
            return DesignProposal(**data)
        except Exception as e:
            # Fallback proposal backed by UI UX Pro Max intelligence
            return DesignProposal(
                target_audience=brief_answers.get("target_audience", "Doanh nghiệp & Khách hàng tiềm năng"),
                value_proposition=f"Giải pháp chuyển đổi đột phá cho {prompt}",
                sections_outline=[
                    {"id": "hero", "name": "Hero Section", "purpose": "Thu hút chuyển đổi ban đầu"},
                    {"id": "social_proof", "name": "Chứng nhận & Đối tác", "purpose": "Gia tăng niềm tin"},
                    {"id": "features", "name": "Tính năng nổi bật (Bento Showcase)", "purpose": "Mô tả giá trị sản phẩm"},
                    {"id": "pricing", "name": "Bảng giá minh bạch", "purpose": "Tối ưu tỷ lệ chuyển đổi"},
                    {"id": "faq", "name": "Câu hỏi thường gặp", "purpose": "Giải tỏa thắc mắc"},
                    {"id": "final_cta", "name": "Kêu gọi hành động", "purpose": "Thúc đẩy đăng ký ngay"}
                ],
                color_palette=rec_palette,
                typography={
                    "heading": rec_typo["heading"],
                    "body": rec_typo["body"]
                },
                tone_of_voice=brief_answers.get("brand_style", "Hiện đại, chuyên nghiệp, truyền cảm hứng"),
                revision_notes=feedback
            )
