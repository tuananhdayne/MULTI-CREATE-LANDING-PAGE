import pytest
from app.agents.visual_qa import visual_qa_node

def test_visual_qa_node_with_devtools_audit():
    valid_html = """<!DOCTYPE html>
<html>
<head>
    <title>Valid QA</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-900 text-white">
    <header class="p-4"><h1>Valid Page</h1></header>
    <main><p>Content goes here</p></main>
</body>
</html>"""
    state = {"code": valid_html, "iteration": 0, "messages": []}
    result = visual_qa_node(state)
    assert result["qa_passed"] is True
    assert "devtools_audit" in result
    assert result["devtools_audit"]["console_errors_count"] == 0
    assert result["devtools_audit"]["runtime_tested"] is True

def test_visual_qa_node_catches_runtime_js_error():
    broken_html = """<!DOCTYPE html>
<html>
<head>
    <title>Broken QA</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-900 text-white">
    <header class="p-4"><h1>Broken Page</h1></header>
    <main><p>Content</p></main>
    <script>
        console.error("Uncaught TypeError: window.nonExistentFn is not a function");
    </script>
</body>
</html>"""
    state = {"code": broken_html, "iteration": 0, "messages": []}
    result = visual_qa_node(state)
    assert result["qa_passed"] is False
    assert "devtools_audit" in result
    assert result["devtools_audit"]["console_errors_count"] > 0
