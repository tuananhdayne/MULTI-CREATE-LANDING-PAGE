from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    """
    Request payload to trigger multi-agent generation of a landing page.
    """
    prompt: str = Field(..., description="Description or requirements for the landing page")
    theme: str = Field(default="auto", description="Preferred theme: 'auto', 'dark', or 'light'")
    model: Optional[str] = Field(default=None, description="Optional override for Gemini model")


class TweakElementRequest(BaseModel):
    """
    Request payload for targeted element editing (Click-to-Inspect).
    """
    element_id: Optional[str] = Field(default=None, description="HTML ID or selector of the target element")
    tag: str = Field(..., description="HTML tag name (e.g. 'button', 'section', 'h1')")
    classes: str = Field(default="", description="Current Tailwind CSS classes")
    current_html: str = Field(..., description="The outer HTML of the element being edited")
    instruction: str = Field(..., description="User's natural language tweak instructions")
    full_code: Optional[str] = Field(default=None, description="Current full HTML code of the page")


class ProjectResponse(BaseModel):
    """
    Response schema representing the current project state and version control.
    """
    id: str = Field(..., description="Project session ID")
    code: str = Field(..., description="Complete single-file HTML5 code")
    version: int = Field(default=1, description="Current version number")
    can_undo: bool = Field(default=False, description="True if an older version exists")
    can_redo: bool = Field(default=False, description="True if a newer version exists in redo stack")


class AgentProgressEvent(BaseModel):
    """
    Schema for Server-Sent Events (SSE) streaming updates to the frontend.
    """
    agent: str = Field(..., description="Name of the agent (e.g. 'strategist', 'copywriter', 'coder')")
    status: str = Field(..., description="'started' | 'thinking' | 'completed' | 'error'")
    message: str = Field(..., description="Human-readable progress description")
    data: Optional[Dict[str, Any]] = Field(default=None, description="Optional auxiliary payload or code snippet")
