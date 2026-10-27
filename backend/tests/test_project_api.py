import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_api_start_brief_and_get_session():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Start brief
        res = await client.post("/api/project/start-brief", json={"prompt": "Ứng dụng đặt món ăn healthy"})
        assert res.status_code == 200
        data = res.json()
        assert "session_id" in data
        assert "questions" in data
        assert len(data["questions"]) >= 2
        
        session_id = data["session_id"]
        
        # 2. Get session
        s_res = await client.get(f"/api/project/session/{session_id}")
        assert s_res.status_code == 200
        assert s_res.json()["status"] == "BRIEFING"
        
        # 3. Submit brief
        sub_res = await client.post("/api/project/submit-brief", json={
            "session_id": session_id,
            "answers": {
                "target_audience": "Dân văn phòng",
                "brand_style": "Tươi sáng, xanh lá healthy",
                "conversion_goal": "Tải app nhận voucher 50k"
            }
        })
        assert sub_res.status_code == 200
        assert sub_res.json()["status"] == "BRIEF_READY"
        
        # 4. Approve proposal
        # We manually inject a proposal in service or call generate
        app_res = await client.post("/api/project/approve-proposal", json={"session_id": session_id})
        assert app_res.status_code == 200
        assert app_res.json()["status"] == "BUILDING"
