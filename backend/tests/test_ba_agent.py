import pytest
from app.agents.ba_analyst import BAAnalystAgent
from app.schemas.session import BriefQuestion

@pytest.mark.asyncio
async def test_ba_generates_three_targeted_questions():
    agent = BAAnalystAgent()
    questions = await agent.generate_questions("Landing page cho nền tảng quản lý tiệm trà sữa")
    assert isinstance(questions, list)
    assert len(questions) >= 2
    for q in questions:
        assert isinstance(q, BriefQuestion)
        assert len(q.id) > 0
        assert len(q.question) > 0
        assert len(q.quick_options) >= 2
