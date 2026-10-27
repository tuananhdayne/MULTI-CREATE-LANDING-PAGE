from typing import Literal
from langgraph.graph import StateGraph, START, END
from app.models.state import AgentState
from app.agents.strategist import strategist_node
from app.agents.copywriter import copywriter_node
from app.agents.designer import designer_node
from app.agents.coder import coder_node
from app.agents.visual_qa import qa_node


def should_continue_qa(state: AgentState) -> Literal["coder", "__end__"]:
    """
    Evaluates whether the generated code passed QA or requires another iteration of fixing.
    Limits to at most 2 iterations to avoid infinite loops.
    """
    qa_passed = state.get("qa_passed", False)
    iteration = state.get("iteration", 0)

    if qa_passed:
        return END

    if iteration >= 2:
        # Reached max retry limit, finish with the best available code
        return END

    return "coder"


def create_landing_page_graph():
    """
    Constructs and compiles the 5-agent LangGraph workflow with a Critic-Fix loop.
    Flow:
    START -> Strategist -> Copywriter -> Designer -> Coder -> QA -> (Passed? END : Coder)
    """
    workflow = StateGraph(AgentState)

    # 1. Register all agent nodes
    workflow.add_node("strategist", strategist_node)
    workflow.add_node("copywriter", copywriter_node)
    workflow.add_node("designer", designer_node)
    workflow.add_node("coder", coder_node)
    workflow.add_node("qa", qa_node)

    # 2. Add sequential flow edges
    workflow.add_edge(START, "strategist")
    workflow.add_edge("strategist", "copywriter")
    workflow.add_edge("copywriter", "designer")
    workflow.add_edge("designer", "coder")
    workflow.add_edge("coder", "qa")

    # 3. Add conditional critic-fix loop edge
    workflow.add_conditional_edges(
        "qa",
        should_continue_qa,
        {
            "coder": "coder",
            END: END
        }
    )

    return workflow.compile()
