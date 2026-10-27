import pytest
from app.schemas.session import ProjectSession, SessionStatus
from app.services.session_service import SessionService

def test_session_lifecycle():
    service = SessionService()
    session = service.create_session(prompt="SaaS for dental clinics")
    assert session.status == SessionStatus.BRIEFING
    assert session.initial_prompt == "SaaS for dental clinics"
    assert session.session_id is not None
    
    # Update brief
    updated = service.update_brief(session.session_id, answers={"target": "Dentists", "tone": "Modern"})
    assert updated.status == SessionStatus.BRIEF_READY
    assert updated.brief.answers["target"] == "Dentists"
    
    # Set proposal
    proposal_data = {
        "target_audience": "Dentists",
        "value_proposition": "Automate patient scheduling",
        "sections_outline": [{"id": "hero", "name": "Hero Section"}],
        "color_palette": {"primary": "#3B82F6", "secondary": "#1E293B"},
        "typography": {"heading": "Outfit", "body": "Inter"},
        "tone_of_voice": "Professional & Trustworthy"
    }
    with_proposal = service.set_proposal(session.session_id, proposal_data)
    assert with_proposal.status == SessionStatus.PROPOSAL_REVIEW
    assert with_proposal.proposal.value_proposition == "Automate patient scheduling"
    
    # Approve proposal -> building
    approved = service.approve_proposal(session.session_id)
    assert approved.status == SessionStatus.BUILDING
    
    # Set code
    with_code = service.set_code(session.session_id, html_code="<html><body>Dentist</body></html>", qa_report={"score": 100})
    assert with_code.status == SessionStatus.UAT_REVIEW
    assert "Dentist" in with_code.build.html_code
    
    # Add UAT feedback
    with_uat = service.add_uat_feedback(session.session_id, feedback="Make button bigger")
    assert len(with_uat.uat_history) == 1
    assert with_uat.uat_history[0].feedback == "Make button bigger"
