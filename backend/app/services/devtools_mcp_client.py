import asyncio
import json
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger("DevToolsMCPClient")

class DevToolsMCPClient:
    """
    Lightweight asynchronous JSON-RPC stdio client communicating with the
    official chrome-devtools-mcp server (Google Chrome Team).
    """
    def __init__(self, command: str = "npx", args: Optional[List[str]] = None):
        self.command = command
        self.args = args or ["--yes", "chrome-devtools-mcp", "--headless"]
        self.proc: Optional[asyncio.subprocess.Process] = None
        self._request_id = 0
        self._lock = asyncio.Lock()
        self.is_running = False

    async def start(self, timeout: float = 15.0):
        """Spawns the MCP server subprocess and performs the initialize handshake."""
        async with self._lock:
            if self.is_running and self.proc:
                return

            self.proc = await asyncio.create_subprocess_exec(
                self.command,
                *self.args,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            self.is_running = True

            # Handshake: initialize
            init_payload = {
                "jsonrpc": "2.0",
                "id": self._next_id(),
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {
                        "name": "LandingCraft-VisualQA",
                        "version": "1.0.0"
                    }
                }
            }
            await self._send(init_payload)
            init_res = await self._read_response(init_payload["id"], timeout=timeout)

            # Handshake: initialized notification
            notif = {
                "jsonrpc": "2.0",
                "method": "notifications/initialized"
            }
            await self._send(notif)
            logger.info("DevTools MCP Client initialized successfully")

    async def list_tools(self, timeout: float = 10.0) -> List[Dict[str, Any]]:
        """Queries tools/list from the MCP server."""
        req_id = self._next_id()
        payload = {
            "jsonrpc": "2.0",
            "id": req_id,
            "method": "tools/list",
            "params": {}
        }
        await self._send(payload)
        res = await self._read_response(req_id, timeout=timeout)
        result = res.get("result", {})
        return result.get("tools", [])

    async def call_tool(self, name: str, arguments: Dict[str, Any], timeout: float = 20.0) -> Dict[str, Any]:
        """Calls a tool via tools/call and returns the tool output."""
        req_id = self._next_id()
        payload = {
            "jsonrpc": "2.0",
            "id": req_id,
            "method": "tools/call",
            "params": {
                "name": name,
                "arguments": arguments
            }
        }
        await self._send(payload)
        res = await self._read_response(req_id, timeout=timeout)
        return res.get("result", {})

    async def close(self):
        """Cleanly terminates the MCP subprocess."""
        async with self._lock:
            if not self.proc:
                self.is_running = False
                return
            try:
                if self.proc.stdin:
                    self.proc.stdin.close()
                self.proc.terminate()
                await asyncio.wait_for(self.proc.wait(), timeout=3.0)
            except Exception:
                try:
                    self.proc.kill()
                except Exception:
                    pass
            finally:
                self.proc = None
                self.is_running = False

    def _next_id(self) -> int:
        self._request_id += 1
        return self._request_id

    async def _send(self, data: Dict[str, Any]):
        if not self.proc or not self.proc.stdin:
            raise RuntimeError("MCP process not running")
        encoded = json.dumps(data, ensure_ascii=False).encode("utf-8") + b"\n"
        self.proc.stdin.write(encoded)
        await self.proc.stdin.drain()

    async def _read_response(self, expected_id: int, timeout: float = 15.0) -> Dict[str, Any]:
        if not self.proc or not self.proc.stdout:
            raise RuntimeError("MCP process not running")

        loop = asyncio.get_running_loop()
        deadline = loop.time() + timeout

        while True:
            remaining = deadline - loop.time()
            if remaining <= 0:
                raise asyncio.TimeoutError(f"Timeout waiting for MCP response id={expected_id}")

            line_bytes = await asyncio.wait_for(self.proc.stdout.readline(), timeout=remaining)
            if not line_bytes:
                # Subprocess EOF
                stderr_output = ""
                if self.proc.stderr:
                    try:
                        err_bytes = await asyncio.wait_for(self.proc.stderr.read(1024), timeout=1.0)
                        stderr_output = err_bytes.decode(errors="ignore")
                    except Exception:
                        pass
                raise RuntimeError(f"MCP server closed stdout prematurely. Stderr: {stderr_output}")

            line_str = line_bytes.decode("utf-8", errors="ignore").strip()
            if not line_str:
                continue

            try:
                parsed = json.loads(line_str)
                if isinstance(parsed, dict) and parsed.get("id") == expected_id:
                    if "error" in parsed:
                        raise RuntimeError(f"MCP error response: {parsed['error']}")
                    return parsed
            except json.JSONDecodeError:
                # Ignore non-JSON log lines output by node/chrome
                continue
