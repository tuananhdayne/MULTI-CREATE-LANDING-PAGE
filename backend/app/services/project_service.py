from typing import Dict, List, Optional
import time
from app.models.api_schemas import ProjectResponse


class ProjectSession:
    """
    Maintains the code history and undo/redo stacks for a single user project session.
    """
    def __init__(self, project_id: str):
        self.project_id: str = project_id
        self.history: List[str] = []      # Past versions
        self.redo_stack: List[str] = []   # Undone versions for redo
        self.current_code: str = ""       # Currently active HTML code
        self.version: int = 0

    @property
    def can_undo(self) -> bool:
        return len(self.history) > 0

    @property
    def can_redo(self) -> bool:
        return len(self.redo_stack) > 0

    def to_response(self) -> ProjectResponse:
        return ProjectResponse(
            id=self.project_id,
            code=self.current_code,
            version=self.version,
            can_undo=self.can_undo,
            can_redo=self.can_redo
        )


class ProjectService:
    """
    In-memory state and version management service for projects.
    """
    def __init__(self):
        self._sessions: Dict[str, ProjectSession] = {}

    def get_or_create_session(self, project_id: str) -> ProjectSession:
        if project_id not in self._sessions:
            self._sessions[project_id] = ProjectSession(project_id)
        return self._sessions[project_id]

    def save_version(self, project_id: str, code: str) -> ProjectResponse:
        session = self.get_or_create_session(project_id)
        if session.current_code and session.current_code != code:
            session.history.append(session.current_code)
            # Clear redo stack when a new edit branch is introduced
            session.redo_stack.clear()

        session.current_code = code
        session.version += 1
        return session.to_response()

    def undo(self, project_id: str) -> Optional[ProjectResponse]:
        session = self.get_or_create_session(project_id)
        if not session.can_undo:
            return session.to_response() if session.current_code else None

        # Push current code to redo stack
        session.redo_stack.append(session.current_code)
        # Pop previous version from history
        session.current_code = session.history.pop()
        session.version = max(1, session.version - 1)
        return session.to_response()

    def redo(self, project_id: str) -> Optional[ProjectResponse]:
        session = self.get_or_create_session(project_id)
        if not session.can_redo:
            return session.to_response() if session.current_code else None

        # Push current code to history
        session.history.append(session.current_code)
        # Pop from redo stack
        session.current_code = session.redo_stack.pop()
        session.version += 1
        return session.to_response()

    def get_project(self, project_id: str) -> Optional[ProjectResponse]:
        if project_id in self._sessions:
            return self._sessions[project_id].to_response()
        return None


# Global singleton instance
_project_service = ProjectService()


def get_project_service() -> ProjectService:
    return _project_service
