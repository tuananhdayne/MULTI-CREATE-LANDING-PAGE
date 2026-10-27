import pytest
from app.services.devtools_mcp_client import DevToolsMCPClient

@pytest.mark.asyncio
async def test_mcp_client_lifecycle_and_tools():
    client = DevToolsMCPClient()
    try:
        await client.start()
        assert client.is_running is True
        
        # Call list tools
        tools = await client.list_tools()
        assert isinstance(tools, list)
        tool_names = [t.get("name") for t in tools if isinstance(t, dict)]
        assert "navigate_page" in tool_names or "list_pages" in tool_names
    finally:
        await client.close()
        assert client.is_running is False
