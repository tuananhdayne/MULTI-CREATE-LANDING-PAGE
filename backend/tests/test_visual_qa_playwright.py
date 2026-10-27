import pytest
from app.services.chrome_inspector import ChromeInspector
from app.agents.visual_qa import visual_qa_node
from app.models.state import AgentState


@pytest.mark.asyncio
async def test_playwright_multi_viewport_valid_html():
    inspector = ChromeInspector()
    clean_html = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Clean Page</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
</head>
<body class="bg-slate-900 text-white overflow-x-hidden">
    <header class="p-4 flex justify-between">
        <i data-lucide="zap" class="w-6 h-6"></i>
        <button id="hero-cta-btn" class="bg-blue-600 px-4 py-2 rounded">Click Me</button>
    </header>
    <main class="max-w-4xl mx-auto p-4">
        <h1 class="text-3xl font-bold">Responsive Layout</h1>
    </main>
    <script>lucide.createIcons();</script>
</body>
</html>"""

    res = await inspector.inspect_with_playwright(clean_html)
    assert res["playwright_tested"] is True
    assert res["viewports"]["desktop"]["has_overflow"] is False
    assert res["viewports"]["tablet"]["has_overflow"] is False
    assert res["viewports"]["mobile"]["has_overflow"] is False
    assert res["cta_clickable"] is True
    assert res["passed"] is True


@pytest.mark.asyncio
async def test_playwright_detects_mobile_overflow():
    inspector = ChromeInspector()
    overflow_html = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Overflow Page</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-900 text-white">
    <div style="width: 1200px; height: 100px; background: red;">Forced wide element</div>
</body>
</html>"""

    res = await inspector.inspect_with_playwright(overflow_html)
    assert res["playwright_tested"] is True
    assert res["viewports"]["mobile"]["has_overflow"] is True
    assert res["passed"] is False


def test_visual_qa_node_with_playwright_and_devtools():
    state: AgentState = {
        "prompt": "Test Landing Page",
        "code": """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Superpowers Test</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
</head>
<body class="bg-slate-900 text-white overflow-x-hidden">
    <section id="hero" class="p-8 text-center">
        <h1 class="text-4xl">Title</h1>
        <button id="hero-cta-btn" class="bg-blue-600 px-4 py-2 mt-4 rounded">CTA</button>
    </section>
    <script>lucide.createIcons();</script>
</body>
</html>""",
        "iteration": 0,
        "messages": []
    }

    result = visual_qa_node(state)
    assert result["qa_passed"] is True
    assert "devtools_audit" in result
    audit = result["devtools_audit"]
    assert "playwright_audit" in audit or "runtime_tested" in audit
