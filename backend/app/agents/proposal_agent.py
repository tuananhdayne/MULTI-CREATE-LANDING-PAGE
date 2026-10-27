import json
import re
from typing import Optional, Any
from langchain_core.messages import SystemMessage, HumanMessage
from app.agents.base import get_gemini_llm
from app.schemas.session import DesignProposal

PROPOSAL_SYSTEM_PROMPT = """Bạn là Giám đốc Nghệ thuật & Trưởng phòng Chiến lược CRO (Creative Director & CRO Lead) tại Agency phát triển Landing Page.
Nhiệm vụ của bạn: Từ thông tin Briefing đã được đối tác xác nhận, hãy thiết lập một Bản Đề Xuất Kế Hoạch & Thiết Kế (Design & Architecture Proposal) hoàn chỉnh để trình cho đối tác phê duyệt trước khi lập trình.

QUY ĐỊNH BẮT BUỘC:
- Trả về ĐÚNG định dạng JSON Object (không markdown thừa):
{
  "target_audience": "Mô tả chi tiết chân dung khách hàng",
  "value_proposition": "Tuyên ngôn giá trị cốt lõi giải quyết nỗi đau của khách",
  "sections_outline": [
    {"id": "hero", "name": "Hero Section", "purpose": "Thu hút sự chú ý ngay trong 3 giây đầu kèm CTA nổi bật"},
    {"id": "social_proof", "name": "Social Proof / Trust Badges", "purpose": "Xây dựng uy tín và sự tin cậy"},
    {"id": "features", "name": "Core Features / Benefits", "purpose": "Chứng minh giải pháp và tính năng vượt trội"},
    {"id": "pricing", "name": "Pricing / Comparison Table", "purpose": "Minh bạch chi phí và kích thích chuyển đổi"},
    {"id": "faq", "name": "FAQ Section", "purpose": "Giải tỏa mọi rào cản và thắc mắc cuối cùng"},
    {"id": "final_cta", "name": "Final CTA Banner", "purpose": "Chốt chuyển đổi mạnh mẽ"}
  ],
  "color_palette": {
    "primary": "#3B82F6",
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
- Phối màu `color_palette` phải hài hòa, chuẩn tương phản WCAG AA, phù hợp với ngành nghề và phong cách đối tác yêu cầu.
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
        context = (
            f"Dự án: {prompt}\n"
            f"Brief đối tác đã chốt:\n"
            f"- Đối tượng khách hàng: {brief_answers.get('target_audience', 'Khách hàng quan tâm')}\n"
            f"- Phong cách thương hiệu: {brief_answers.get('brand_style', 'Hiện đại, chuyên nghiệp')}\n"
            f"- Mục tiêu chuyển đổi: {brief_answers.get('conversion_goal', 'Đăng ký nhận tư vấn')}\n"
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
            # Fallback proposal
            return DesignProposal(
                target_audience=brief_answers.get("target_audience", "Doanh nghiệp & Khách hàng tiềm năng"),
                value_proposition=f"Giải pháp đột phá cho {prompt}",
                sections_outline=[
                    {"id": "hero", "name": "Hero Section", "purpose": "Thu hút chuyển đổi ban đầu"},
                    {"id": "social_proof", "name": "Chứng nhận & Đối tác", "purpose": "Gia tăng niềm tin"},
                    {"id": "features", "name": "Tính năng nổi bật", "purpose": "Mô tả giá trị sản phẩm"},
                    {"id": "pricing", "name": "Bảng giá minh bạch", "purpose": "Tối ưu tỷ lệ chuyển đổi"},
                    {"id": "faq", "name": "Câu hỏi thường gặp", "purpose": "Giải đáp thắc mắc"},
                    {"id": "final_cta", "name": "Kêu gọi hành động", "purpose": "Thúc đẩy đăng ký ngay"}
                ],
                color_palette={
                    "primary": "#3B82F6",
                    "secondary": "#1E293B",
                    "accent": "#F59E0B",
                    "background": "#0F172A",
                    "surface": "#1E293B"
                },
                typography={
                    "heading": "Outfit, sans-serif",
                    "body": "Inter, sans-serif"
                },
                tone_of_voice=brief_answers.get("brand_style", "Hiện đại, chuyên nghiệp, truyền cảm hứng"),
                revision_notes=feedback
            )
