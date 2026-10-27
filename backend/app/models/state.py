from typing import TypedDict, List, Dict, Any, Optional


class AgentState(TypedDict, total=False):
    """
    State shared across all nodes in the LangGraph Multi-Agent system.
    """
    prompt: str
    theme: str
    outline: str
    copy: str
    design: str
    code: str
    qa_feedback: str
    qa_passed: bool
    iteration: int
    messages: List[Dict[str, Any]]
    target_element: Optional[Dict[str, Any]]
