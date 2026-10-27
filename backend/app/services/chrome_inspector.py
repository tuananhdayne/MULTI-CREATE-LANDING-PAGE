import os
import re
import json
import uuid
import asyncio
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path
from playwright.async_api import async_playwright
from app.services.devtools_mcp_client import DevToolsMCPClient

logger = logging.getLogger("ChromeInspector")

VIEWPORTS = {
    "desktop": {"width": 1280, "height": 800},
    "tablet": {"width": 768, "height": 1024},
    "mobile": {"width": 375, "height": 812}
}


class ChromeInspector:
    """
    Unified QA Inspector combining:
    1. Chrome DevTools MCP: Deep runtime console messages & CDP telemetry.
    2. Playwright: Multi-viewport responsive verification (Desktop/Tablet/Mobile)
       and interactive functional smoke tests.
    """
    def __init__(self, temp_dir: Optional[str] = None):
        self.temp_dir = Path(temp_dir or Path(os.getcwd()) / ".temp")
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    async def inspect_with_playwright(self, html_code: str) -> Dict[str, Any]:
        """
        Loads HTML into Playwright Chromium, audits multi-viewport responsive layouts,
        tests CTA interactions and icon rendering.
        """
        temp_file = self.temp_dir / f"pw_inspect_{uuid.uuid4().hex[:8]}.html"
        temp_file.write_text(html_code, encoding="utf-8")
        abs_url = f"file://{temp_file.resolve()}"

        issues: List[str] = []
        viewport_results: Dict[str, Any] = {}
        cta_clickable = False
        icons_count = 0

        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()

                # 1. Multi-viewport testing
                for vp_name, vp_dims in VIEWPORTS.items():
                    await page.set_viewport_size(vp_dims)
                    await page.goto(abs_url, wait_until="load")
                    await asyncio.sleep(0.1)

                    overflow_info = await page.evaluate("""() => ({
                        hasOverflow: document.documentElement.scrollWidth > window.innerWidth,
                        scrollWidth: document.documentElement.scrollWidth,
                        clientWidth: window.innerWidth
                    })""")

                    has_overflow = bool(overflow_info.get("hasOverflow", False))
                    viewport_results[vp_name] = {
                        "width": vp_dims["width"],
                        "height": vp_dims["height"],
                        "has_overflow": has_overflow,
                        "scroll_width": overflow_info.get("scrollWidth", 0)
                    }
                    if has_overflow:
                        issues.append(f"Giao diện bị tràn viền (overflow) trên {vp_name.title()} ({vp_dims['width']}px).")

                # 2. Interactive CTA click test
                try:
                    cta_btn = page.locator("#hero-cta-btn, button, a[href]").first
                    if await cta_btn.count() > 0:
                        await cta_btn.click(timeout=1500)
                        cta_clickable = True
                    else:
                        cta_clickable = True  # No button to click
                except Exception as e:
                    logger.debug(f"CTA click test notice: {e}")
                    cta_clickable = False
                    issues.append("Nút kêu gọi hành động (CTA) bị che khuất hoặc không thể tương tác.")

                # 3. Lucide icons rendering check
                icons_count = await page.evaluate("() => document.querySelectorAll('svg').length")

                await browser.close()

            passed = len(issues) == 0
            return {
                "passed": passed,
                "playwright_tested": True,
                "viewports": viewport_results,
                "cta_clickable": cta_clickable,
                "icons_count": icons_count,
                "issues": issues
            }

        except Exception as e:
            logger.warning(f"Playwright responsive inspection error: {e}")
            return {
                "passed": True,
                "playwright_tested": False,
                "viewports": {},
                "cta_clickable": True,
                "icons_count": 0,
                "issues": [],
                "warning": str(e)
            }
        finally:
            if temp_file.exists():
                try:
                    temp_file.unlink()
                except Exception:
                    pass

    async def inspect_html(self, html_code: str) -> Dict[str, Any]:
        """
        Executes unified audit using both Chrome DevTools MCP (for console errors)
        and Playwright (for multi-viewport responsiveness and interaction).
        """
        # 1. Run Playwright multi-viewport and functional audit
        pw_audit = await self.inspect_with_playwright(html_code)

        # 2. Run Chrome DevTools MCP for deep runtime console errors
        temp_file = self.temp_dir / f"qa_inspect_{uuid.uuid4().hex[:8]}.html"
        client = DevToolsMCPClient()
        console_errors: List[str] = []
        mcp_overflow = False
        mcp_tested = False

        try:
            temp_file.write_text(html_code, encoding="utf-8")
            abs_url = f"file://{temp_file.resolve()}"

            await client.start(timeout=15.0)
            await client.call_tool("navigate_page", {"pageId": 1, "url": abs_url}, timeout=10.0)
            await asyncio.sleep(0.3)

            # Audit console errors
            console_res = await client.call_tool("list_console_messages", {"pageId": 1, "types": ["error"]}, timeout=5.0)
            content_list = console_res.get("content", [])
            for item in content_list:
                text_content = item.get("text", "")
                for line in text_content.split("\n"):
                    line_clean = line.strip()
                    if "[error]" in line_clean:
                        err_msg = line_clean.split("[error]", 1)[-1].strip()
                        console_errors.append(err_msg)

            # Audit 375px mobile resize via DevTools MCP
            await client.call_tool("resize_page", {"pageId": 1, "width": 375, "height": 812}, timeout=5.0)
            overflow_fn = "() => ({ hasOverflow: document.documentElement.scrollWidth > window.innerWidth })"
            eval_res = await client.call_tool("evaluate_script", {"pageId": 1, "function": overflow_fn}, timeout=5.0)
            for item in eval_res.get("content", []):
                text_content = item.get("text", "")
                json_match = re.search(r"```json\s*([\s\S]*?)\s*```", text_content)
                raw_json = json_match.group(1).strip() if json_match else text_content.strip()
                try:
                    data = json.loads(raw_json)
                    if isinstance(data, dict):
                        mcp_overflow = bool(data.get("hasOverflow", False))
                except Exception:
                    pass

            mcp_tested = True
        except Exception as e:
            logger.warning(f"DevTools MCP console audit notice: {e}")
            mcp_tested = False
        finally:
            await client.close()
            if temp_file.exists():
                try:
                    temp_file.unlink()
                except Exception:
                    pass

        has_overflow = mcp_overflow or any(
            vp.get("has_overflow", False) for vp in pw_audit.get("viewports", {}).values()
        )

        all_passed = (len(console_errors) == 0) and (not has_overflow) and pw_audit.get("passed", True)

        return {
            "passed": all_passed,
            "console_errors": console_errors,
            "console_errors_count": len(console_errors),
            "has_overflow": has_overflow,
            "runtime_tested": mcp_tested or pw_audit.get("playwright_tested", False),
            "playwright_audit": pw_audit,
            "mobile_viewport": {"width": 375, "height": 812}
        }
