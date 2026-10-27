import pytest
from app.schemas.session import BriefQuestion, DesignProposal
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


def test_evaluate_ba_analyst_valid():
    questions = [
        BriefQuestion(id="target_audience", question="Ai là khách hàng mục tiêu?", quick_options=["B2B", "B2C", "Agency", "Devs"]),
        BriefQuestion(id="brand_style", question="Phong cách thương hiệu?", quick_options=["Minimal", "Cyberpunk", "Corporate"]),
        BriefQuestion(id="conversion_goal", question="Mục tiêu chuyển đổi?", quick_options=["Đăng ký", "Mua ngay", "Gọi điện"])
    ]
    res = evaluate_ba_analyst(questions, test_case_id="saas_test")
    assert res.score == 100.0
    assert res.status == HarnessStatus.PASS
    assert len(res.issues) == 0


def test_evaluate_ba_analyst_incomplete():
    questions = [
        BriefQuestion(id="unknown", question="Câu hỏi không rõ?", quick_options=[])
    ]
    res = evaluate_ba_analyst(questions, test_case_id="saas_test")
    assert res.score < 80.0
    assert res.status == HarnessStatus.FAIL
    assert len(res.issues) > 0


def test_evaluate_proposal_valid():
    proposal = DesignProposal(
        target_audience="Doanh nghiệp IT",
        value_proposition="Tuyển dụng nhanh hơn 5x với AI",
        sections_outline=[
            {"id": "hero", "name": "Hero", "purpose": "Hook"},
            {"id": "social_proof", "name": "Social Proof", "purpose": "Trust"},
            {"id": "features", "name": "Features", "purpose": "Showcase"},
            {"id": "pricing", "name": "Pricing", "purpose": "Tiers"},
            {"id": "faq", "name": "FAQ", "purpose": "Answers"},
            {"id": "cta", "name": "Final CTA", "purpose": "Convert"}
        ],
        color_palette={
            "primary": "#3B82F6",
            "secondary": "#1E293B",
            "accent": "#10B981",
            "background": "#0F172A",
            "surface": "#1E293B"
        },
        typography={"heading": "Outfit", "body": "Inter"},
        tone_of_voice="Chuyên nghiệp"
    )
    res = evaluate_proposal(proposal, test_case_id="saas_test")
    assert res.score == 100.0
    assert res.status == HarnessStatus.PASS


def test_evaluate_proposal_invalid_colors():
    proposal = DesignProposal(
        target_audience="Khách hàng",
        value_proposition="Giá trị cốt lõi",
        sections_outline=[{"id": "hero", "name": "Hero", "purpose": "Hook"}],
        color_palette={
            "primary": "invalid_color",
            "secondary": "#1E293B",
            "accent": "#10B981",
            "background": "rgb(0,0,0)",
            "surface": "#1E293B"
        },
        typography={"heading": "Outfit", "body": "Inter"},
        tone_of_voice="Thân thiện"
    )
    res = evaluate_proposal(proposal, test_case_id="saas_test")
    assert res.score < 80.0
    assert any("HEX" in issue for issue in res.issues)


def test_evaluate_coder_valid_html():
    valid_html = """<!DOCTYPE html>
<html lang="vi" class="scroll-smooth">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TalentAI</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
</head>
<body class="bg-slate-900 text-white">
    <section id="hero" class="py-20 px-4 md:px-8">
        <h1 class="text-4xl md:text-6xl font-bold">TalentAI</h1>
        <button id="hero-cta-btn" class="bg-blue-600 sm:px-6 px-4 py-3 rounded-lg">Bắt đầu ngay</button>
    </section>
    <section id="features" class="py-16">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6"></div>
    </section>
    <section id="cta" class="py-12 text-center"></section>
    <script>lucide.createIcons();</script>
</body>
</html>"""
    res = evaluate_coder(valid_html, test_case_id="saas_test")
    assert res.score >= 90.0
    assert res.status == HarnessStatus.PASS


def test_evaluate_coder_missing_tailwind_and_doctype():
    broken_html = "<div><h1>Hello</h1></div>"
    res = evaluate_coder(broken_html, test_case_id="saas_test")
    assert res.score < 80.0
    assert res.status == HarnessStatus.FAIL
    assert any("Tailwind" in issue for issue in res.issues)


def test_evaluate_element_editor_valid():
    orig_element = {
        "tag": "button",
        "element_id": "cta-btn",
        "current_html": '<button id="cta-btn" class="bg-blue-600 text-white">Click</button>'
    }
    new_html = '<button id="cta-btn" class="bg-gradient-to-r from-orange-500 to-amber-500 text-white rounded-full">Đăng ký ngay</button>'
    res = evaluate_element_editor(new_html, orig_element, instruction="Đổi sang gradient cam bo tròn", test_case_id="tweak_test")
    assert res.score >= 90.0
    assert res.status == HarnessStatus.PASS


def test_evaluate_element_editor_leak_full_page():
    orig_element = {"tag": "button", "element_id": "cta-btn", "current_html": '<button id="cta-btn">Click</button>'}
    full_page = '<html><head></head><body><button id="cta-btn">Click</button></body></html>'
    res = evaluate_element_editor(full_page, orig_element, instruction="Đổi màu", test_case_id="tweak_test")
    assert res.score < 80.0
    assert res.status == HarnessStatus.FAIL
