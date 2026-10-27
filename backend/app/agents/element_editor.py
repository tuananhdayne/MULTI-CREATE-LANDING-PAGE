import re
from typing import Dict, Any, Optional
from langchain_core.messages import SystemMessage, HumanMessage
from app.agents.base import get_gemini_llm

ELEMENT_EDITOR_PROMPT = """Bạn là Chuyên gia tinh chỉnh UI và Tailwind CSS với Chrome DevTools (Targeted Element Editor, tích hợp tri thức từ UI UX Pro Max & Frontend Design).
Người dùng đã sử dụng công cụ Inspect Element để chọn một phần tử cụ thể trên giao diện và yêu cầu chỉnh sửa nó.

Nhiệm vụ của bạn là:
1. Xem xét mã HTML hiện tại của phần tử được chọn và yêu cầu chỉnh sửa của người dùng.
2. Viết lại ĐÚNG phần tử đó với các thuộc tính HTML, class Tailwind CSS, hoặc nội dung text mới theo yêu cầu:
   - Áp dụng các quy tắc thẩm mỹ từ UI UX Pro Max (độ tương phản màu chữ WCAG AA, bo góc hài hòa, hiệu ứng đổ bóng mượt mà `shadow-lg shadow-orange-500/20`, kích thước cảm ứng tối thiểu `min-h-[44px]`).
   - Thêm hiệu ứng transition mượt mà (`transition-all duration-300`).
3. Giữ nguyên ID (nếu có) hoặc các thuộc tính quan trọng để không làm đứt gãy layout xung quanh.
4. QUAN TRỌNG NHẤT: CHỈ xuất ra duy nhất mã HTML của phần tử được sửa đổi (ví dụ: `<button ...>...</button>`), KHÔNG xuất ra cả trang web và KHÔNG viết thêm giải thích bên ngoài.

Ví dụ:
Input:
Tag: button
ID: hero-cta-btn
Current HTML: <button id="hero-cta-btn" class="bg-blue-600 text-white px-4 py-2">Click</button>
Instruction: Đổi thành nút gradient cam, bo tròn đầy đủ, đổi chữ thành Đăng Ký Ngay

Output:
<button id="hero-cta-btn" class="bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-white font-semibold px-6 py-3 rounded-full shadow-lg shadow-orange-500/25 transition-all duration-300">Đăng Ký Ngay</button>
"""


def generate_element_tweak(
    target_element: Dict[str, Any],
    instruction: str
) -> str:
    """
    Invokes LLM to generate the modified HTML snippet for a specific DOM element.
    """
    current_html = target_element.get("current_html", "").strip()
    tag = target_element.get("tag", "")
    element_id = target_element.get("element_id", "")
    classes = target_element.get("classes", "")

    if not current_html:
        return ""

    llm = get_gemini_llm(temperature=0.3)
    user_prompt = f"""
THÔNG TIN PHẦN TỬ ĐƯỢC CHỌN TRÊN DEVTOOLS:
- Thẻ (Tag): {tag}
- ID: {element_id or 'Không có'}
- Classes hiện tại: {classes}
- Mã HTML hiện tại của phần tử:
{current_html}

YÊU CẦU CHỈNH SỬA TỪ NGƯỜI DÙNG:
{instruction}

Hãy trả về mã HTML mới của duy nhất phần tử này (không bao bọc trang web):
"""
    messages = [
        SystemMessage(content=ELEMENT_EDITOR_PROMPT),
        HumanMessage(content=user_prompt)
    ]

    response = llm.invoke(messages)
    new_element_html = response.content if hasattr(response, "content") else str(response)
    new_element_html = new_element_html.strip()

    # Clean markdown backticks if any
    if new_element_html.startswith("```"):
        lines = new_element_html.split("\n")
        if len(lines) >= 2:
            new_element_html = "\n".join(lines[1:-1]).strip()

    return new_element_html


def tweak_element_node(
    full_code: str,
    target_element: Dict[str, Any],
    instruction: str
) -> str:
    """
    Modifies a specific DOM element within the landing page based on Chrome DevTools inspector feedback.
    """
    current_html = target_element.get("current_html", "").strip()
    tag = target_element.get("tag", "")
    element_id = target_element.get("element_id", "")

    if not current_html or not full_code:
        return full_code

    new_element_html = generate_element_tweak(target_element, instruction)
    if not new_element_html:
        return full_code

    # Replace the current_html in full_code
    if current_html in full_code:
        return full_code.replace(current_html, new_element_html, 1)

    # Fallback: if exact substring match fails due to whitespace differences, try relaxed match by element_id
    if element_id:
        pattern = rf'(<{tag}[^>]*id=["\']?{re.escape(element_id)}["\']?[^>]*>[\s\S]*?</{tag}>|<{tag}[^>]*id=["\']?{re.escape(element_id)}["\']?[^>]*/>)'
        if re.search(pattern, full_code, re.IGNORECASE):
            return re.sub(pattern, lambda _: new_element_html, full_code, count=1, flags=re.IGNORECASE)

    return full_code
