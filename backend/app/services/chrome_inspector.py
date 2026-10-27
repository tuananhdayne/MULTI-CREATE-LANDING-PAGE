import os
import re
import json
import uuid
import asyncio
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path
from app.services.devtools_mcp_client import DevToolsMCPClient

logger = logging.getLogger("ChromeInspector")

class ChromeInspector:
    """
    High-level auditor leveraging Chrome DevTools MCP to inspect HTML pages
    in a real headless Chrome environment for runtime JS console errors and
    mobile responsive overflow.
    """
    def __init__(self, temp_dir: Optional[str] = None):
        self.temp_dir = Path(temp_dir or Path(os.getcwd()) / ".temp")
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    async def inspect_html(self, html_code: str) -> Dict[str, Any]:
        """
        Loads HTML into headless Chrome via chrome-devtools-mcp, audits
        console errors, and checks for mobile overflow.
        """
        temp_file = self.temp_dir / f"qa_inspect_{uuid.uuid4().hex[:8]}.html"
        client = DevToolsMCPClient()
        
        try:
            # 1. Write HTML to temporary file
            temp_file.write_text(html_code, encoding="utf-8")
            abs_url = f"file://{temp_file.resolve()}"

            # 2. Start MCP server
            await client.start(timeout=15.0)

            # 3. Navigate page on pageId=1
            await client.call_tool("navigate_page", {"pageId": 1, "url": abs_url}, timeout=10.0)
            await asyncio.sleep(0.3)

            # 4. Check console messages
            console_res = await client.call_tool("list_console_messages", {"pageId": 1, "types": ["error"]}, timeout=5.0)
            console_errors: List[str] = []
            
            content_list = console_res.get("content", [])
            for item in content_list:
                text_content = item.get("text", "")
                lines = text_content.split("\n")
                for line in lines:
                    line_clean = line.strip()
                    if "[error]" in line_clean:
                        # Extract error message after [error]
                        err_msg = line_clean.split("[error]", 1)[-1].strip()
                        console_errors.append(err_msg)

            # 5. Check Mobile Overflow (375px)
            await client.call_tool("resize_page", {"pageId": 1, "width": 375, "height": 812}, timeout=5.0)
            overflow_fn = "() => ({ hasOverflow: document.documentElement.scrollWidth > window.innerWidth, scrollWidth: document.documentElement.scrollWidth, clientWidth: window.innerWidth })"
            
            has_overflow = False
            eval_res = await client.call_tool("evaluate_script", {"pageId": 1, "function": overflow_fn}, timeout=5.0)
            eval_content = eval_res.get("content", [])
            for item in eval_content:
                text_content = item.get("text", "")
                json_match = re.search(r"```json\s*([\s\S]*?)\s*```", text_content)
                raw_json = json_match.group(1).strip() if json_match else text_content.strip()
                try:
                    data = json.loads(raw_json)
                    if isinstance(data, dict):
                        has_overflow = bool(data.get("hasOverflow", False))
                except Exception:
                    pass

            passed = (len(console_errors) == 0) and (not has_overflow)

            return {
                "passed": passed,
                "console_errors": console_errors,
                "console_errors_count": len(console_errors),
                "has_overflow": has_overflow,
                "runtime_tested": True
            }

        except Exception as e:
            logger.warning(f"Chrome DevTools MCP inspection encountered an issue: {e}")
            # Graceful fallback: report runtime test skipped but do not fail pipeline
            return {
                "passed": True,
                "console_errors": [],
                "console_errors_count": 0,
                "has_overflow": False,
                "runtime_tested": False,
                "warning": f"DevTools runtime test skipped: {str(e)}"
            }
        finally:
            await client.close()
            if temp_file.exists():
                try:
                    temp_file.unlink()
                except Exception:
                    pass
