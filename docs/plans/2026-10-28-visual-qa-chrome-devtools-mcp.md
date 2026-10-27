# Visual QA Chrome DevTools MCP Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade Visual QA Agent to autonomously inspect landing pages using the official Chrome DevTools MCP Server (`chrome-devtools-mcp`) via JSON-RPC stdio to detect runtime JavaScript console errors and mobile layout overflow.

**Architecture:** A lightweight asynchronous Python JSON-RPC client (`DevToolsMCPClient`) managing the `npx -y chrome-devtools-mcp --headless` subprocess, orchestrated by `ChromeInspector` and integrated into `visual_qa_node`, surfacing live DevTools audit signals on the UAT Acceptance Board.

**Tech Stack:** Python 3.10+, asyncio, JSON-RPC 2.0, Node.js v20, `chrome-devtools-mcp`, Google Chrome (`/usr/bin/google-chrome`), FastAPI, React 18.

**Spec:** [docs/specs/2026-10-28-visual-qa-chrome-devtools-mcp-design.md](file:///home/tuananh/GEN_LANDING/docs/specs/2026-10-28-visual-qa-chrome-devtools-mcp-design.md)

## Global Constraints

- **Process Hygiene:** Every spawned MCP subprocess must be cleanly terminated in `finally` blocks; zero orphan/zombie processes.
- **Fail-Safe / Fallback:** If Chrome or Node is unavailable or times out (>15s), gracefully fallback to static regex validation without crashing the generation pipeline.
- **Security:** Zero secret leakage; never pass credentials or API keys through browser command-line flags.
- **Evidence Before Assertion:** Every task must be verified with automated test output before being marked complete.

## Review Focus

1. **Subprocess Deadlock:** Large stdout/stderr output from `npx` must not deadlock the stdio pipe (use `asyncio.StreamReader` / non-blocking line reading).
2. **Temporary File Isolation:** Store temporary HTML inspection files in `.temp/` within the workspace and clean them up after inspection.
3. **Detection of Deliberate Console Errors:** Prove that an HTML file containing `<script>console.error("Test error")</script>` is flagged as a failure by Visual QA.
4. **Mobile Overflow Detection:** Prove that an element with fixed `w-[800px]` triggers mobile overflow warning on 375px viewport.
5. **Fast Response Time:** Keep total DevTools inspection under 6 seconds on local machine.

---

### Task 1: DevTools MCP Stdio Client Module

**Files:**
- Create: `backend/app/services/devtools_mcp_client.py`
- Test: `backend/tests/test_devtools_mcp_client.py`

**Interfaces:**
- Consumes: Nothing
- Produces: `DevToolsMCPClient`:
  - `async def start()`
  - `async def call_tool(name: str, arguments: dict) -> dict`
  - `async def close()`

- [ ] **Step 1: Write the failing test**

```python
# backend/tests/test_devtools_mcp_client.py
import pytest
from app.services.devtools_mcp_client import DevToolsMCPClient

@pytest.mark.asyncio
async def test_mcp_client_lifecycle_and_tools():
    client = DevToolsMCPClient()
    try:
        await client.start()
        assert client.is_running is True
        
        # Call a basic tool or list tools
        tools = await client.list_tools()
        assert any(t["name"] == "navigate_page" for t in tools)
        assert any(t["name"] == "list_console_messages" for t in tools)
    finally:
        await client.close()
        assert client.is_running is False
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=backend pytest backend/tests/test_devtools_mcp_client.py -v`  
Expected: FAIL with `ModuleNotFoundError: No module named 'app.services.devtools_mcp_client'`

- [ ] **Step 3: Implement `DevToolsMCPClient`**

In `backend/app/services/devtools_mcp_client.py`:
- Use `asyncio.create_subprocess_exec` to spawn `npx --yes chrome-devtools-mcp --headless`.
- Send standard JSON-RPC 2.0 messages via `proc.stdin.write(json.dumps(msg).encode() + b"\n")`.
- Read responses via `proc.stdout.readline()`.
- Implement `start()`, `list_tools()`, `call_tool(name, arguments)`, and `close()`.

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=backend pytest backend/tests/test_devtools_mcp_client.py -v`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add backend/app/services/devtools_mcp_client.py backend/tests/test_devtools_mcp_client.py
git commit -m "feat: implement DevTools MCP stdio client for chrome-devtools-mcp"
```

---

### Task 2: Chrome Inspector Service

**Files:**
- Create: `backend/app/services/chrome_inspector.py`
- Test: `backend/tests/test_chrome_inspector.py`

**Interfaces:**
- Consumes: `DevToolsMCPClient`
- Produces: `ChromeInspector`:
  - `async def inspect_html(html_code: str) -> dict`
  - Returns `{ "passed": bool, "console_errors": list, "has_overflow": bool, "overflow_elements": list }`

- [ ] **Step 1: Write the failing test**

```python
# backend/tests/test_chrome_inspector.py
import pytest
from app.services.chrome_inspector import ChromeInspector

@pytest.mark.asyncio
async def test_inspector_detects_clean_html():
    inspector = ChromeInspector()
    clean_html = """<!DOCTYPE html><html><head><title>Clean</title></head><body><h1>Hello World</h1></body></html>"""
    report = await inspector.inspect_html(clean_html)
    assert report["passed"] is True
    assert len(report["console_errors"]) == 0
    assert report["has_overflow"] is False

@pytest.mark.asyncio
async def test_inspector_catches_runtime_error():
    inspector = ChromeInspector()
    broken_html = """<!DOCTYPE html><html><head></head><body><script>console.error("CRITICAL_JS_ERROR");</script></body></html>"""
    report = await inspector.inspect_html(broken_html)
    assert report["passed"] is False
    assert any("CRITICAL_JS_ERROR" in str(err) for err in report["console_errors"])
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=backend pytest backend/tests/test_chrome_inspector.py -v`  
Expected: FAIL with `ModuleNotFoundError: No module named 'app.services.chrome_inspector'`

- [ ] **Step 3: Implement `ChromeInspector`**

In `backend/app/services/chrome_inspector.py`:
- Writes HTML to a temporary file in `.temp/` within workspace.
- Starts `DevToolsMCPClient`, calls `navigate_page` with file URL.
- Calls `list_console_messages` and filters `level == "error"`.
- Calls `resize_page` with width=375, height=812, then calls `evaluate_script` checking `scrollWidth > clientWidth`.
- Returns structured audit dictionary.

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=backend pytest backend/tests/test_chrome_inspector.py -v`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add backend/app/services/chrome_inspector.py backend/tests/test_chrome_inspector.py
git commit -m "feat: add ChromeInspector service detecting runtime console errors and overflow"
```

---

### Task 3: Upgrade Visual QA Agent with DevTools Inspector

**Files:**
- Modify: `backend/app/agents/visual_qa.py`
- Test: `backend/tests/test_visual_qa_devtools.py`

**Interfaces:**
- Consumes: `ChromeInspector`
- Produces: `visual_qa_node(state)` enhanced with Chrome DevTools runtime audit report.

- [ ] **Step 1: Write the failing test**

```python
# backend/tests/test_visual_qa_devtools.py
import pytest
from app.agents.visual_qa import visual_qa_node

def test_visual_qa_node_with_devtools_audit():
    valid_html = """<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-900 text-white">
    <header class="p-4"><h1>Valid Page</h1></header>
    <main><p>Content</p></main>
</body>
</html>"""
    state = {"code": valid_html, "iteration": 0, "messages": []}
    result = visual_qa_node(state)
    assert result["qa_passed"] is True
    assert "devtools_audit" in result
    assert result["devtools_audit"]["console_errors_count"] == 0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=backend pytest backend/tests/test_visual_qa_devtools.py -v`  
Expected: FAIL with `KeyError: 'devtools_audit'`

- [ ] **Step 3: Implement DevTools audit integration in `visual_qa_node`**

- In `backend/app/agents/visual_qa.py`:
  - Run static syntax check first.
  - If syntax passes, invoke `ChromeInspector().inspect_html(code)` synchronously via helper or `asyncio.run`.
  - Attach `devtools_audit` payload to returned dictionary:
    `{"console_errors_count": int, "has_mobile_overflow": bool, "runtime_tested": True}`.
  - If console errors or mobile overflow detected, mark `qa_passed = False` and populate specific repair instructions.

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=backend pytest backend/tests/test_visual_qa_devtools.py -v`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add backend/app/agents/visual_qa.py backend/tests/test_visual_qa_devtools.py
git commit -m "feat: upgrade Visual QA agent with Chrome DevTools runtime verification"
```

---

### Task 4: Frontend UAT Board Chrome DevTools Badges

**Files:**
- Modify: `frontend/src/components/milestones/UATPanel.tsx`
- Modify: `frontend/src/types/project.ts`
- Test: Build validation via `npm run build`

**Interfaces:**
- Consumes: `session.build.qa_report.devtools_audit`
- Produces: Live DevTools status badges (Console: 0 errors, Responsive: Passed) in UAT Acceptance Board.

- [ ] **Step 1: Update TypeScript types and `UATPanel.tsx`**

- In `frontend/src/types/project.ts`: Add `DevToolsAudit` interface to `BuildArtifact.qa_report`.
- In `frontend/src/components/milestones/UATPanel.tsx`:
  - Display green badge: `Chrome DevTools MCP: 0 Errors` or red badge with error count.
  - Display responsive status: `Mobile 375px: No Overflow` or warning badge if overflow detected.

- [ ] **Step 2: Run build to verify type safety**

Run: `cd frontend && npm run build`  
Expected: PASS with 0 errors.

- [ ] **Step 3: Commit**

```bash
git add frontend/src/types/project.ts frontend/src/components/milestones/UATPanel.tsx
git commit -m "feat: display Chrome DevTools runtime audit metrics on UAT Acceptance panel"
```

---

### Task 5: End-to-End Verification & Evidence

**Files:**
- Create: `scripts/test_visual_qa_devtools_e2e.py`
- Test: End-to-end audit run on broken vs clean page

**Interfaces:**
- Consumes: Full Visual QA agent with Chrome DevTools MCP
- Produces: Test execution logs and verified runtime detection evidence.

- [ ] **Step 1: Write and run verification script**

Run: `python3 scripts/test_visual_qa_devtools_e2e.py`  
Verify:
1. Chrome DevTools MCP spawns and loads page cleanly.
2. Deliberate JS error is caught and reported by Visual QA.
3. Clean landing page passes all checks with 0 errors.

- [ ] **Step 2: Check Git status and push to GitHub**

```bash
git status
git add scripts/test_visual_qa_devtools_e2e.py
git commit -m "test: add end-to-end verification for Visual QA Chrome DevTools MCP"
git push origin main
```
