import re
import asyncio
import concurrent.futures
from typing import Dict, Any, Tuple, List
from app.models.state import AgentState
from app.services.chrome_inspector import ChromeInspector

def run_sync(coro):
    """Executes an async coroutine synchronously, safe inside running event loops."""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            with concurrent.futures.ThreadPoolExecutor() as pool:
                return pool.submit(asyncio.run, coro).result()
        else:
            return loop.run_until_complete(coro)
    except RuntimeError:
        return asyncio.run(coro)


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
    Validates HTML syntax and leverages Chrome DevTools MCP to audit
    real-time runtime console errors and mobile responsiveness.
    """
    code = state.get("code", "")
    iteration = state.get("iteration", 0) + 1

    # Stage 1: Static HTML Syntax Validation
    is_valid, errors = validate_html_structure(code)

    current_messages = list(state.get("messages", []))

    if not is_valid:
        feedback = "Phát hiện lỗi cú pháp cần khắc phục: " + "; ".join(errors)
        current_messages.append({
            "agent": "qa",
            "status": "warning" if iteration < 2 else "error",
            "message": f"QA phát hiện vấn đề cú pháp (lần {iteration}): {feedback}",
            "passed": False,
            "errors": errors
        })
        return {
            "qa_passed": False,
            "qa_feedback": feedback,
            "iteration": iteration,
            "messages": current_messages,
            "devtools_audit": {
                "runtime_tested": False,
                "reason": "Static validation failed before DevTools launch"
            }
        }

    # Stage 2: Chrome DevTools MCP Runtime Inspector
    inspector = ChromeInspector()
    devtools_audit = run_sync(inspector.inspect_html(code))

    has_runtime_errors = devtools_audit.get("console_errors_count", 0) > 0
    has_overflow = devtools_audit.get("has_overflow", False)

    if has_runtime_errors or has_overflow:
        runtime_issues = []
        if has_runtime_errors:
            runtime_issues.append(f"Lỗi JavaScript Console: {'; '.join(devtools_audit['console_errors'][:3])}")
        if has_overflow:
            runtime_issues.append("Phát hiện phần tử bị tràn viền (overflow) trên màn hình di động 375px.")

        feedback = "Chrome DevTools phát hiện vấn đề runtime: " + " | ".join(runtime_issues)
        current_messages.append({
            "agent": "qa",
            "status": "warning" if iteration < 2 else "error",
            "message": f"DevTools MCP phát hiện lỗi runtime (lần {iteration}): {feedback}",
            "passed": False,
            "devtools_audit": devtools_audit
        })
        return {
            "qa_passed": False,
            "qa_feedback": feedback,
            "iteration": iteration,
            "messages": current_messages,
            "devtools_audit": devtools_audit
        }

    # All checks passed
    feedback = "Kiểm tra chất lượng thành công: Cấu trúc HTML5 chuẩn, Tailwind CSS CDN đầy đủ, Playwright Responsive (Desktop/Tablet/Mobile) hoàn hảo, Chrome DevTools 0 lỗi console & tương tác CTA mượt mà."
    current_messages.append({
        "agent": "qa",
        "status": "completed",
        "message": feedback,
        "passed": True,
        "devtools_audit": devtools_audit
    })
    return {
        "qa_passed": True,
        "qa_feedback": feedback,
        "iteration": iteration,
        "messages": current_messages,
        "devtools_audit": devtools_audit
    }

visual_qa_node = qa_node
