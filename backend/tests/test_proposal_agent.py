import pytest
from app.agents.proposal_agent import ProposalAgent
from app.schemas.session import DesignProposal

@pytest.mark.asyncio
async def test_proposal_agent_generates_design_spec():
    agent = ProposalAgent()
    proposal = await agent.generate_proposal(
        prompt="SaaS CRM cho môi giới bất động sản",
        brief_answers={
            "target_audience": "Môi giới cá nhân & sàn giao dịch",
            "brand_style": "Sang trọng, hiện đại, tối giản",
            "conversion_goal": "Đăng ký dùng thử 14 ngày"
        }
    )
    assert isinstance(proposal, DesignProposal)
    assert len(proposal.sections_outline) >= 4
    assert "primary" in proposal.color_palette
    assert proposal.tone_of_voice != ""
    assert proposal.target_audience != ""
