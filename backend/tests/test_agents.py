import pytest
from unittest.mock import MagicMock, patch
from app.models.state import AgentState
from app.agents.strategist import strategist_node
from app.agents.copywriter import copywriter_node
from app.agents.designer import designer_node
from app.agents.coder import coder_node
from app.agents.visual_qa import qa_node, validate_html_structure
from app.agents.element_editor import tweak_element_node


def test_validate_html_structure_valid():
    html = """<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <script src="https://cdn.tailwindcss.com"></script>
        <title>Landing Page</title>
    </head>
    <body class="bg-slate-900 text-white">
        <header>Navbar</header>
        <main><section>Hero Section</section></main>
        <footer>Footer</footer>
    </body>
    </html>"""
    is_valid, errors = validate_html_structure(html)
    assert is_valid is True
    assert len(errors) == 0


def test_validate_html_structure_missing_tailwind():
    html = """<!DOCTYPE html>
    <html>
    <head><title>No Tailwind</title></head>
    <body><h1>Hello</h1></body>
    </html>"""
    is_valid, errors = validate_html_structure(html)
    assert is_valid is False
    assert any("Tailwind" in err for err in errors)


def test_qa_node_passes_for_valid_code():
    state: AgentState = {
        "code": """<!DOCTYPE html>
        <html><head><script src="https://cdn.tailwindcss.com"></script></head>
        <body><h1>Success</h1></body></html>""",
        "iteration": 0,
        "messages": []
    }
    result = qa_node(state)
    assert result["qa_passed"] is True
    assert result["iteration"] == 1


def test_qa_node_fails_for_invalid_code():
    state: AgentState = {
        "code": "Broken HTML without closing tags",
        "iteration": 0,
        "messages": []
    }
    result = qa_node(state)
    assert result["qa_passed"] is False
    assert result["iteration"] == 1
    assert "qa_feedback" in result


@patch("app.agents.strategist.get_gemini_llm")
def test_strategist_node(mock_get_llm):
    mock_llm = MagicMock()
    mock_llm.invoke.return_value = MagicMock(content="1. Hero Section\n2. Features Section\n3. CTA")
    mock_get_llm.return_value = mock_llm

    state: AgentState = {
        "prompt": "Landing page cho ứng dụng quản lý chi tiêu",
        "theme": "dark",
        "messages": []
    }
    result = strategist_node(state)
    assert "outline" in result
    assert "Hero Section" in result["outline"]
    assert len(result["messages"]) > 0


@patch("app.agents.copywriter.get_gemini_llm")
def test_copywriter_node(mock_get_llm):
    mock_llm = MagicMock()
    mock_llm.invoke.return_value = MagicMock(content="# Headline: Quản lý tài chính thông minh\nCTA: Bắt đầu ngay")
    mock_get_llm.return_value = mock_llm

    state: AgentState = {
        "prompt": "Landing page cho ứng dụng quản lý chi tiêu",
        "outline": "1. Hero Section",
        "messages": []
    }
    result = copywriter_node(state)
    assert "copy" in result
    assert "Quản lý tài chính" in result["copy"]


@patch("app.agents.element_editor.get_gemini_llm")
def test_tweak_element_node(mock_get_llm):
    original_html = """<!DOCTYPE html><html><head><script src="https://cdn.tailwindcss.com"></script></head><body>
    <button id="cta-btn" class="bg-blue-600 text-white">Click Me</button>
    </body></html>"""

    mock_llm = MagicMock()
    # The LLM outputs the updated button
    mock_llm.invoke.return_value = MagicMock(
        content='<button id="cta-btn" class="bg-gradient-to-r from-orange-500 to-amber-500 text-white shadow-lg">Khám phá ngay</button>'
    )
    mock_get_llm.return_value = mock_llm

    target_element = {
        "element_id": "cta-btn",
        "tag": "button",
        "classes": "bg-blue-600 text-white",
        "current_html": '<button id="cta-btn" class="bg-blue-600 text-white">Click Me</button>'
    }

    updated_code = tweak_element_node(
        full_code=original_html,
        target_element=target_element,
        instruction="Đổi nút thành gradient cam và đổi chữ thành Khám phá ngay"
    )

    assert "bg-gradient-to-r from-orange-500" in updated_code
    assert "Khám phá ngay" in updated_code
    assert "<!DOCTYPE html>" in updated_code
