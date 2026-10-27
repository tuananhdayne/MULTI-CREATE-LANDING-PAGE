from datetime import datetime, timezone
from typing import Optional, Any
from app.schemas.session import (
    ProjectSession,
    SessionStatus,
    BriefQuestion,
    DesignProposal,
    BuildArtifact,
    UATFeedback,
)

class SessionService:
    def __init__(self):
        self._sessions: dict[str, ProjectSession] = {}

    def create_session(self, prompt: str) -> ProjectSession:
        session = ProjectSession(initial_prompt=prompt, status=SessionStatus.BRIEFING)
        self._sessions[session.session_id] = session
        return session

    def get_session(self, session_id: str) -> Optional[ProjectSession]:
        return self._sessions.get(session_id)

    def set_brief_questions(self, session_id: str, questions: list[BriefQuestion]) -> ProjectSession:
        session = self._require_session(session_id)
        session.brief.questions = questions
        session.status = SessionStatus.BRIEFING
        session.updated_at = datetime.now(timezone.utc).isoformat()
        return session

    def update_brief(self, session_id: str, answers: dict[str, str], confirmed_summary: Optional[str] = None) -> ProjectSession:
        session = self._require_session(session_id)
        session.brief.answers.update(answers)
        if confirmed_summary:
            session.brief.confirmed_summary = confirmed_summary
        session.status = SessionStatus.BRIEF_READY
        session.updated_at = datetime.now(timezone.utc).isoformat()
        return session

    def set_proposal(self, session_id: str, proposal_data: dict[str, Any]) -> ProjectSession:
        session = self._require_session(session_id)
        session.proposal = DesignProposal(**proposal_data)
        session.status = SessionStatus.PROPOSAL_REVIEW
        session.updated_at = datetime.now(timezone.utc).isoformat()
        return session

    def approve_proposal(self, session_id: str) -> ProjectSession:
        session = self._require_session(session_id)
        session.status = SessionStatus.BUILDING
        session.updated_at = datetime.now(timezone.utc).isoformat()
        return session

    def set_code(self, session_id: str, html_code: str, qa_report: Optional[dict[str, Any]] = None) -> ProjectSession:
        session = self._require_session(session_id)
        session.build = BuildArtifact(html_code=html_code, qa_report=qa_report or {})
        session.status = SessionStatus.UAT_REVIEW
        session.updated_at = datetime.now(timezone.utc).isoformat()
        return session

    def add_uat_feedback(self, session_id: str, feedback: str, target_element_id: Optional[str] = None) -> ProjectSession:
        session = self._require_session(session_id)
        item = UATFeedback(feedback=feedback, target_element_id=target_element_id)
        session.uat_history.append(item)
        session.updated_at = datetime.now(timezone.utc).isoformat()
        return session

    def _require_session(self, session_id: str) -> ProjectSession:
        session = self._sessions.get(session_id)
        if not session:
            raise KeyError(f"Session {session_id} not found")
        return session

# Global singleton service
session_service = SessionService()
