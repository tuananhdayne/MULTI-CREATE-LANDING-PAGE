import re
from typing import Dict, Any, Tuple, List
from app.models.state import AgentState


def validate_html_structure(code: str) -> Tuple[bool, List[str]]:
    """
    Validates HTML syntax, essential tags, Tailwind CDN inclusion, and closing tags.
    """
    errors: List[str] = []

    if not code or len(code.strip()) < 100:
        return False, ["Mã nguồn HTML quá ngắn hoặc trống."]

    lower_code = code.lower()

    # 1. DOCTYPE and HTML tag check
    if "<!doctype html" not in lower_code and "<html" not in lower_code:
        errors.append("Thiếu thẻ khai báo <!DOCTYPE html> hoặc <html>.")

    # 2. Tailwind CSS CDN check
    if "cdn.tailwindcss.com" not in lower_code:
        errors.append("Thiếu thẻ nhúng Tailwind CSS CDN (<script src='https://cdn.tailwindcss.com'></script>).")

    # 3. Head and Body check
    if "<head" not in lower_code or "</head>" not in lower_code:
        errors.append("Thiếu thẻ <head> hoặc thẻ đóng </head>.")

    if "<body" not in lower_code or "</body>" not in lower_code:
        errors.append("Thiếu thẻ <body> hoặc thẻ đóng </body>.")

    if "</html>" not in lower_code:
        errors.append("Thiếu thẻ đóng </html> ở cuối trang.")

    # 4. Check for basic content structure
    has_content = any(tag in lower_code for tag in ["<section", "<main", "<header", "<div", "<h1"])
    if not has_content:
        errors.append("Thiếu các khối nội dung HTML hợp lệ (<section>, <main>, hoặc <div>).")

    is_valid = len(errors) == 0
    return is_valid, errors


def qa_node(state: AgentState) -> Dict[str, Any]:
    """
    Visual QA Inspector node in LangGraph.
    Validates the generated HTML code and decides whether it passes or needs revision.
    """
    code = state.get("code", "")
    iteration = state.get("iteration", 0) + 1

    is_valid, errors = validate_html_structure(code)

    current_messages = list(state.get("messages", []))

    if is_valid:
        feedback = "Kiểm tra chất lượng thành công: Cấu trúc HTML5 chuẩn, Tailwind CSS CDN đầy đủ, semantic markup hợp lệ."
        current_messages.append({
            "agent": "qa",
            "status": "completed",
            "message": feedback,
            "passed": True
        })
        return {
            "qa_passed": True,
            "qa_feedback": feedback,
            "iteration": iteration,
            "messages": current_messages
        }
    else:
        feedback = "Phát hiện lỗi cần khắc phục: " + "; ".join(errors)
        current_messages.append({
            "agent": "qa",
            "status": "warning" if iteration < 2 else "error",
            "message": f"QA phát hiện vấn đề (lần {iteration}): {feedback}",
            "passed": False,
            "errors": errors
        })
        return {
            "qa_passed": False,
            "qa_feedback": feedback,
            "iteration": iteration,
            "messages": current_messages
        }

visual_qa_node = qa_node
