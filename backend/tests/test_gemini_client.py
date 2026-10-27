import pytest
from app.models.state import AgentState
from app.models.api_schemas import GenerateRequest, TweakElementRequest, ProjectResponse
from app.agents.base import clean_markdown_code, get_gemini_llm


def test_clean_markdown_code_with_html_blocks():
    raw_markdown = """Here is the landing page code:
```html
<!DOCTYPE html>
<html lang="en">
<head><title>Test Page</title></head>
<body><h1>Hello World</h1></body>
</html>
```
Hope you like it!"""
    cleaned = clean_markdown_code(raw_markdown)
    assert cleaned.startswith("<!DOCTYPE html>")
    assert cleaned.endswith("</html>")
    assert "Here is the landing page code:" not in cleaned
    assert "Hope you like it!" not in cleaned


def test_clean_markdown_code_without_blocks():
    raw_html = "<!DOCTYPE html><html><body><h1>Direct HTML</h1></body></html>"
    cleaned = clean_markdown_code(raw_html)
    assert cleaned == raw_html


def test_generate_request_validation():
    req = GenerateRequest(prompt="Tạo landing page cho app tài chính cá nhân")
    assert req.prompt == "Tạo landing page cho app tài chính cá nhân"
    assert req.theme == "auto"


def test_tweak_element_request_validation():
    tweak = TweakElementRequest(
        element_id="hero-cta-btn",
        tag="button",
        classes="bg-blue-600 text-white px-6 py-3 rounded-lg",
        current_html="<button class='bg-blue-600'>Get Started</button>",
        instruction="Đổi thành nút gradient cam neon và thêm hiệu ứng hover scale"
    )
    assert tweak.tag == "button"
    assert "gradient cam neon" in tweak.instruction


def test_gemini_llm_instantiation_without_leak(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "AIzaSyDummySecretKeyTest123")
    monkeypatch.setenv("GEMINI_MODEL", "gemini-2.5-flash")

    llm = get_gemini_llm()
    assert llm is not None
    # String representation must not expose raw key
    assert "AIzaSyDummySecretKeyTest123" not in repr(llm)
