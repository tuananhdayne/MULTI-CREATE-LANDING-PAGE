import pytest
from app.harness.fixtures import BENCHMARK_CASES, MOCK_AGENT_OUTPUTS
from app.harness.models import HarnessStatus
from app.harness.rubrics import (
    evaluate_ba_analyst,
    evaluate_proposal,
    evaluate_strategist,
    evaluate_copywriter,
    evaluate_designer,
    evaluate_coder,
    evaluate_visual_qa,
    evaluate_element_editor,
)


def test_benchmark_cases_structure():
    expected_keys = {"b2b_saas", "ecommerce_fashion", "online_education", "creative_agency", "edge_cases"}
    assert expected_keys.issubset(set(BENCHMARK_CASES.keys()))

    for cid, case in BENCHMARK_CASES.items():
        assert case.id == cid
        assert case.industry != ""
        assert case.prompt != ""
        assert isinstance(case.brief_answers, dict)


def test_mock_outputs_coverage():
    expected_agents = {
        "ba_analyst", "proposal", "strategist", "copywriter",
        "designer", "coder", "visual_qa", "element_editor"
    }
    assert expected_agents.issubset(set(MOCK_AGENT_OUTPUTS.keys()))


def test_mock_outputs_pass_rubrics():
    # 1. BA Analyst
    ba_res = evaluate_ba_analyst(MOCK_AGENT_OUTPUTS["ba_analyst"])
    assert ba_res.status == HarnessStatus.PASS
    assert ba_res.score >= 90.0

    # 2. Proposal
    prop_res = evaluate_proposal(MOCK_AGENT_OUTPUTS["proposal"])
    assert prop_res.status == HarnessStatus.PASS
    assert prop_res.score >= 90.0

    # 3. Strategist
    strat_res = evaluate_strategist(MOCK_AGENT_OUTPUTS["strategist"])
    assert strat_res.status == HarnessStatus.PASS
    assert strat_res.score >= 85.0

    # 4. Copywriter
    copy_res = evaluate_copywriter(MOCK_AGENT_OUTPUTS["copywriter"])
    assert copy_res.status == HarnessStatus.PASS
    assert copy_res.score >= 85.0

    # 5. Designer
    des_res = evaluate_designer(MOCK_AGENT_OUTPUTS["designer"])
    assert des_res.status == HarnessStatus.PASS
    assert des_res.score >= 85.0

    # 6. Coder
    coder_res = evaluate_coder(MOCK_AGENT_OUTPUTS["coder"])
    assert coder_res.status == HarnessStatus.PASS
    assert coder_res.score >= 90.0

    # 7. Visual QA
    qa_res = evaluate_visual_qa(MOCK_AGENT_OUTPUTS["visual_qa"])
    assert qa_res.status == HarnessStatus.PASS
    assert qa_res.score >= 90.0

    # 8. Element Editor
    orig_el = {
        "tag": "button",
        "element_id": "hero-cta-btn",
        "current_html": '<button id="hero-cta-btn" class="bg-blue-600 text-white">Bắt đầu</button>'
    }
    editor_res = evaluate_element_editor(
        MOCK_AGENT_OUTPUTS["element_editor"],
        target_element=orig_el,
        instruction="Đổi sang gradient cam bo tròn"
    )
    assert editor_res.status == HarnessStatus.PASS
    assert editor_res.score >= 90.0
