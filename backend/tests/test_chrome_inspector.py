import pytest
from app.services.chrome_inspector import ChromeInspector

@pytest.mark.asyncio
async def test_inspector_detects_clean_html():
    inspector = ChromeInspector()
    clean_html = """<!DOCTYPE html>
<html>
<head><title>Clean Page</title></head>
<body style="margin:0; padding:20px;">
    <h1>Hello World</h1>
    <p>Everything is normal</p>
</body>
</html>"""
    report = await inspector.inspect_html(clean_html)
    assert report["passed"] is True
    assert len(report["console_errors"]) == 0
    assert report["has_overflow"] is False

@pytest.mark.asyncio
async def test_inspector_catches_runtime_error():
    inspector = ChromeInspector()
    broken_html = """<!DOCTYPE html>
<html>
<head><title>Broken Page</title></head>
<body>
    <h1>Broken Page</h1>
    <script>
        console.error("CRITICAL_JS_ERROR: Something broke");
    </script>
</body>
</html>"""
    report = await inspector.inspect_html(broken_html)
    assert report["passed"] is False
    assert any("CRITICAL_JS_ERROR" in str(err) for err in report["console_errors"])
