import pytest
from app.models.state import AgentState
from app.agents.designer import designer_node
from app.agents.proposal_agent import ProposalAgent
from app.schemas.session import DesignProposal


def test_designer_node_injects_superpowers():
    state: AgentState = {
        "prompt": "TalentAI - Nền tảng AI tuyển dụng nhân sự tự động cho công ty công nghệ",
        "outline": "Dàn ý gồm Hero, Tính năng, Bảng giá, FAQ, CTA",
        "copy": "Nội dung tuyển dụng nhanh hơn 5x",
        "theme": "auto",
        "messages": []
    }

    result = designer_node(state)
    assert "design" in result
    design_text = result["design"]

    # Verify UI UX Pro Max & Frontend Design elements
    assert "60-30-10" in design_text or "TỶ LỆ PHỐI MÀU" in design_text or "BẢNG MÀU" in design_text
    assert any(k in design_text.lower() for k in ["outfit", "inter", "space grotesk", "plus jakarta", "syne"])
    assert any(k in design_text.lower() for k in ["ai-slop", "rập khuôn", "gradient", "chuyển động"])
    assert len(result["messages"]) > 0


@pytest.mark.asyncio
async def test_proposal_agent_generates_enhanced_proposal():
    agent = ProposalAgent()
    # Mocking or calling generate_proposal with fallback safety
    proposal = await agent.generate_proposal(
        prompt="StreetVibe - Thời trang dạo phố cyberpunk",
        brief_answers={
            "target_audience": "Gen Z đam mê streetwear",
            "brand_style": "Dark Cyberpunk neon",
            "conversion_goal": "Săn drop giảm giá 20%"
        }
    )
    assert isinstance(proposal, DesignProposal)
    assert len(proposal.color_palette) == 5
    for color in proposal.color_palette.values():
        assert color.startswith("#")
    assert proposal.typography.get("heading") != ""
    assert proposal.typography.get("body") != ""
