import pytest
from app.agents.coder import CODER_SYSTEM_PROMPT, coder_node
from app.models.state import AgentState
from app.harness.rubrics import evaluate_coder


def test_coder_prompt_contains_frontend_design_principles():
    prompt_lower = CODER_SYSTEM_PROMPT.lower()
    assert "anti-ai slop" in prompt_lower or "ai-slop" in prompt_lower or "rập khuôn" in prompt_lower
    assert "60-30-10" in CODER_SYSTEM_PROMPT or "tỷ lệ phối màu" in prompt_lower
    assert "devtools" in prompt_lower or "id=" in prompt_lower
    assert "bento" in prompt_lower or "bất đối xứng" in prompt_lower or "asymmetric" in prompt_lower


def test_coder_node_execution():
    state: AgentState = {
        "prompt": "TalentAI - Nền tảng tuyển dụng bằng trí tuệ nhân tạo",
        "outline": "Hero với nút CTA đăng ký, Bento features 3 thẻ, Pricing 3 gói, FAQ",
        "copy": "Tiêu đề: Tuyển Dụng Nhanh Hơn 5 Lần Với AI. Nút CTA: Bắt Đầu Ngay.",
        "design": "Phong cách Bento Grid. Bảng màu: Nền #0F172A, Card #1E293B, Primary #2563EB, Accent #10B981. Font: Outfit + Inter.",
        "iteration": 0,
        "messages": []
    }

    res = coder_node(state)
    assert "code" in res
    html = res["code"]

    # Verify HTML passes the Coder Rubric
    rubric_eval = evaluate_coder(html, test_case_id="coder_superpower_test")
    assert rubric_eval.score >= 85.0
    assert rubric_eval.passed is True
