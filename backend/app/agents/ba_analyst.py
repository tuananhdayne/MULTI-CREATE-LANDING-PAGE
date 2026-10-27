import json
import re
from typing import Optional
from langchain_core.messages import SystemMessage, HumanMessage
from app.agents.base import get_gemini_llm
from app.schemas.session import BriefQuestion

BA_SYSTEM_PROMPT = """Bạn là một Chuyên viên Phân tích Nghiệp vụ (Business Analyst - BA) cấp cao tại một Agency IT phát triển Landing Page chuyển đổi cao.
Nhiệm vụ của bạn: Khi khách hàng/đối tác đưa ra một ý tưởng ban đầu, hãy đặt ra 3 câu hỏi cốt lõi để làm rõ yêu cầu nghiệp vụ (Brief) trước khi đội ngũ thiết kế và lập trình bắt tay vào làm.

3 câu hỏi bắt buộc phải nhắm vào 3 khía cạnh sau:
1. `target_audience`: Đối tượng khách hàng mục tiêu cụ thể là ai?
2. `brand_style`: Phong cách thị giác & cảm xúc thương hiệu mong muốn? (ví dụ: Sang trọng tối giản, Trẻ trung năng động, Công nghệ hiện đại, v.v.)
3. `conversion_goal`: Mục tiêu hành động chuyển đổi chính (Primary CTA) trên trang là gì? (ví dụ: Đăng ký dùng thử, Đặt lịch tư vấn, Tải app, v.v.)

QUY ĐỊNH BẮT BUỘC:
- Trả về ĐÚNG định dạng JSON Array chứa 3 object, không bọc văn bản dẫn nhập thừa thãi.
- Mỗi object có cấu trúc:
  {
    "id": "target_audience" | "brand_style" | "conversion_goal",
    "question": "Câu hỏi bằng tiếng Việt rõ ràng, chuyên nghiệp",
    "quick_options": ["Gợi ý nhanh 1", "Gợi ý nhanh 2", "Gợi ý nhanh 3", "Gợi ý nhanh 4"],
    "required": true
  }
- Các `quick_options` phải được cá nhân hóa sát với đề bài cụ thể mà người dùng vừa đưa ra để họ có thể bấm chọn ngay trong 1 click.
"""

class BAAnalystAgent:
    def __init__(self, model_name: Optional[str] = "ag/gemini-3.8-flash"):
        self.llm = get_gemini_llm(model_name=model_name, temperature=0.3)

    async def generate_questions(self, initial_prompt: str) -> list[BriefQuestion]:
        messages = [
            SystemMessage(content=BA_SYSTEM_PROMPT),
            HumanMessage(content=f"Ý tưởng Landing Page của đối tác:\n\"{initial_prompt}\"\n\nHãy tạo 3 câu hỏi Brief tương ứng dạng JSON.")
        ]
        
        try:
            response = await self.llm.ainvoke(messages)
            content = response.content if hasattr(response, "content") else str(response)
            
            # Clean JSON extraction
            json_match = re.search(r"\[\s*\{[\s\S]*\}\s*\]", content)
            raw_json = json_match.group(0) if json_match else content.strip()
            data = json.loads(raw_json)
            
            questions = [BriefQuestion(**item) for item in data]
            if len(questions) >= 2:
                return questions
        except Exception as e:
            # Fallback to sensible tailored questions if LLM fails
            pass

        return [
            BriefQuestion(
                id="target_audience",
                question=f"Đối tượng khách hàng mục tiêu chính cho dự án '{initial_prompt}' là ai?",
                quick_options=["Cá nhân & Giới trẻ", "Doanh nghiệp & Chủ cơ sở kinh doanh", "Gia đình có trẻ nhỏ", "Chuyên gia & Dân văn phòng"],
                required=True
            ),
            BriefQuestion(
                id="brand_style",
                question="Phong cách thị giác và bảng màu bạn mong muốn cho thương hiệu?",
                quick_options=["Hiện đại & Công nghệ (Dark Mode / Neon)", "Sang trọng & Tối giản (Navy / Gold / Trắng)", "Tươi sáng, Thân thiện & Năng động", "Chuyên nghiệp & Đáng tin cậy (Corporate Blue)"],
                required=True
            ),
            BriefQuestion(
                id="conversion_goal",
                question="Hành động chuyển đổi quan trọng nhất bạn muốn khách truy cập thực hiện?",
                quick_options=["Đăng ký trải nghiệm miễn phí", "Liên hệ tư vấn / Đặt lịch hẹn", "Mua ngay / Đặt hàng trực tiếp", "Tải tài liệu / Ứng dụng"],
                required=True
            ),
        ]
