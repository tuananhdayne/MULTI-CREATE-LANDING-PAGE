from enum import Enum
from datetime import datetime, timezone
from typing import Optional, Any
from pydantic import BaseModel, Field
import uuid

class SessionStatus(str, Enum):
    BRIEFING = "BRIEFING"
    BRIEF_READY = "BRIEF_READY"
    PROPOSING = "PROPOSING"
    PROPOSAL_REVIEW = "PROPOSAL_REVIEW"
    BUILDING = "BUILDING"
    UAT_REVIEW = "UAT_REVIEW"
    COMPLETED = "COMPLETED"

class BriefQuestion(BaseModel):
    id: str = Field(..., description="Unique question ID, e.g. target_audience")
    question: str = Field(..., description="The question text")
    quick_options: list[str] = Field(default_factory=list, description="Preset clickable quick suggestions")
    required: bool = True

class BriefData(BaseModel):
    questions: list[BriefQuestion] = Field(default_factory=list)
    answers: dict[str, str] = Field(default_factory=dict)
    confirmed_summary: Optional[str] = None

class SectionSpec(BaseModel):
    id: str
    name: str
    purpose: Optional[str] = None

class DesignProposal(BaseModel):
    target_audience: str
    value_proposition: str
    sections_outline: list[dict[str, Any]] = Field(default_factory=list)
    color_palette: dict[str, str] = Field(default_factory=dict)
    typography: dict[str, str] = Field(default_factory=dict)
    tone_of_voice: str
    revision_notes: Optional[str] = None

class BuildArtifact(BaseModel):
    html_code: str
    qa_report: dict[str, Any] = Field(default_factory=dict)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class UATFeedback(BaseModel):
    feedback: str
    target_element_id: Optional[str] = None
    applied: bool = False
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class ProjectSession(BaseModel):
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    status: SessionStatus = SessionStatus.BRIEFING
    initial_prompt: str
    brief: BriefData = Field(default_factory=BriefData)
    proposal: Optional[DesignProposal] = None
    build: Optional[BuildArtifact] = None
    uat_history: list[UATFeedback] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
