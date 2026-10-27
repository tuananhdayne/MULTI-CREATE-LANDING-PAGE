import pytest
from app.models.state import AgentState
from app.graph.workflow import should_continue_qa, create_landing_page_graph
from app.services.project_service import ProjectService


def test_should_continue_qa_logic():
    # Case 1: QA Passed -> Go to END
    state_passed: AgentState = {"qa_passed": True, "iteration": 1}
    assert should_continue_qa(state_passed) == "__end__"

    # Case 2: QA Failed, iteration 1 -> Loop back to coder
    state_failed_retry: AgentState = {"qa_passed": False, "iteration": 1}
    assert should_continue_qa(state_failed_retry) == "coder"

    # Case 3: QA Failed, max iterations reached (>=2) -> Stop at END
    state_max_retry: AgentState = {"qa_passed": False, "iteration": 2}
    assert should_continue_qa(state_max_retry) == "__end__"


def test_create_landing_page_graph_structure():
    graph = create_landing_page_graph()
    assert graph is not None
    # Graph should contain all 5 nodes
    nodes = graph.nodes
    assert "strategist" in nodes
    assert "copywriter" in nodes
    assert "designer" in nodes
    assert "coder" in nodes
    assert "qa" in nodes


def test_project_service_undo_redo():
    service = ProjectService()
    project_id = "test-session-1"

    # Initial version v1
    v1_code = "<html>v1</html>"
    p1 = service.save_version(project_id, v1_code)
    assert p1.version == 1
    assert p1.can_undo is False
    assert p1.can_redo is False

    # Second version v2
    v2_code = "<html>v2</html>"
    p2 = service.save_version(project_id, v2_code)
    assert p2.version == 2
    assert p2.can_undo is True
    assert p2.can_redo is False

    # Third version v3
    v3_code = "<html>v3</html>"
    p3 = service.save_version(project_id, v3_code)
    assert p3.version == 3
    assert p3.can_undo is True

    # Undo to v2
    undone = service.undo(project_id)
    assert undone is not None
    assert undone.code == v2_code
    assert undone.version == 2
    assert undone.can_undo is True
    assert undone.can_redo is True

    # Redo back to v3
    redone = service.redo(project_id)
    assert redone is not None
    assert redone.code == v3_code
    assert redone.version == 3
    assert redone.can_undo is True
    assert redone.can_redo is False
