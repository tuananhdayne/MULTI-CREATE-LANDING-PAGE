import re
from typing import List, Dict, Any, Optional
from app.schemas.session import BriefQuestion, DesignProposal
from app.harness.models import EvaluationMetric, EvaluationResult, HarnessStatus

HEX_COLOR_REGEX = re.compile(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")


def evaluate_ba_analyst(output: Any, test_case_id: str = "default", latency_sec: float = 0.0) -> EvaluationResult:
    """Rubric for BA Analyst Agent (100 pts)."""
    metrics: List[EvaluationMetric] = []
    issues: List[str] = []

    questions = output if isinstance(output, list) else []

    # 1. Schema & Structure (30 pts)
    has_valid_items = len(questions) >= 2 and all(
        hasattr(q, "id") and hasattr(q, "question") and hasattr(q, "quick_options")
        for q in questions
    )
    if has_valid_items:
        metrics.append(EvaluationMetric(name="json_schema", score=30.0, max_score=30.0, passed=True))
    else:
        metrics.append(EvaluationMetric(name="json_schema", score=10.0, max_score=30.0, passed=False, description="BriefQuestion list incomplete or invalid"))
        issues.append("Danh sách câu hỏi không đúng định dạng BriefQuestion hoặc quá ít (< 2 câu).")

    # 2. Core Coverage (40 pts)
    question_ids = {q.id for q in questions if hasattr(q, "id")}
    covered_core = {"target_audience", "brand_style", "conversion_goal"}.intersection(question_ids)
    coverage_score = (len(covered_core) / 3.0) * 40.0
    passed_cov = len(covered_core) >= 2
    metrics.append(EvaluationMetric(
        name="core_coverage",
        score=coverage_score,
        max_score=40.0,
        passed=passed_cov,
        description=f"Covered {len(covered_core)}/3 core domains ({', '.join(covered_core)})"
    ))
    if not passed_cov:
        issues.append(f"Thiếu các câu hỏi cốt lõi (chỉ có {', '.join(covered_core)}).")

    # 3. Quick Options Quality (30 pts)
    options_qualities = [len(q.quick_options) >= 3 for q in questions if hasattr(q, "quick_options")]
    if options_qualities and all(options_qualities):
        metrics.append(EvaluationMetric(name="options_quality", score=30.0, max_score=30.0, passed=True))
    elif any(options_qualities):
        metrics.append(EvaluationMetric(name="options_quality", score=15.0, max_score=30.0, passed=False, description="Some questions lack quick options (>=3)"))
        issues.append("Một số câu hỏi có ít hơn 3 lựa chọn quick_options gợi ý.")
    else:
        metrics.append(EvaluationMetric(name="options_quality", score=0.0, max_score=30.0, passed=False, description="No valid quick options found"))
        issues.append("Không có các lựa chọn gợi ý nhanh (quick_options).")

    total_score = sum(m.score for m in metrics)
    status = HarnessStatus.PASS if total_score >= 80.0 else HarnessStatus.FAIL

    return EvaluationResult(
        agent_name="ba_analyst",
        test_case_id=test_case_id,
        status=status,
        score=total_score,
        metrics=metrics,
        issues=issues,
        latency_sec=latency_sec,
        output_summary=f"Generated {len(questions)} brief questions",
        raw_output=output
    )


def evaluate_proposal(output: Any, test_case_id: str = "default", latency_sec: float = 0.0) -> EvaluationResult:
    """Rubric for Proposal Agent (100 pts)."""
    metrics: List[EvaluationMetric] = []
    issues: List[str] = []

    proposal = output if isinstance(output, DesignProposal) else None
    if not proposal:
        if isinstance(output, dict):
            try:
                proposal = DesignProposal(**output)
            except Exception:
                pass

    if not proposal:
        return EvaluationResult(
            agent_name="proposal",
            test_case_id=test_case_id,
            status=HarnessStatus.FAIL,
            score=0.0,
            metrics=[EvaluationMetric(name="schema_validity", score=0.0, max_score=100.0, passed=False, description="Invalid DesignProposal")],
            issues=["Đầu ra không thể chuyển đổi thành DesignProposal schema."],
            latency_sec=latency_sec
        )

    # 1. Schema & Completeness (30 pts)
    has_target = bool(proposal.target_audience and len(proposal.target_audience) > 5)
    has_value = bool(proposal.value_proposition and len(proposal.value_proposition) > 5)
    if has_target and has_value:
        metrics.append(EvaluationMetric(name="schema_completeness", score=30.0, max_score=30.0, passed=True))
    else:
        metrics.append(EvaluationMetric(name="schema_completeness", score=10.0, max_score=30.0, passed=False, description="Missing target_audience or value_prop"))
        issues.append("Chưa có đầy đủ mô tả đối tượng mục tiêu hoặc tuyên ngôn giá trị.")

    # 2. Color Palette Validity (25 pts)
    palette = proposal.color_palette or {}
    expected_colors = {"primary", "secondary", "accent", "background", "surface"}
    present_colors = expected_colors.intersection(palette.keys())
    valid_hex = [bool(HEX_COLOR_REGEX.match(str(palette.get(k, "")))) for k in present_colors]
    if len(present_colors) == 5 and all(valid_hex):
        metrics.append(EvaluationMetric(name="color_palette_hex", score=25.0, max_score=25.0, passed=True))
    else:
        invalid_keys = [k for k in present_colors if not HEX_COLOR_REGEX.match(str(palette.get(k, "")))]
        missing_keys = expected_colors - present_colors
        metrics.append(EvaluationMetric(name="color_palette_hex", score=10.0, max_score=25.0, passed=False, description=f"Invalid HEX: {invalid_keys}, missing: {missing_keys}"))
        issues.append(f"Màu sắc không hợp lệ chuẩn HEX hoặc thiếu trường ({', '.join(missing_keys or invalid_keys)}).")

    # 3. Section Architecture (25 pts)
    sections = proposal.sections_outline or []
    section_ids = [s.get("id", "").lower() if isinstance(s, dict) else "" for s in sections]
    has_hero = any("hero" in sid for sid in section_ids)
    has_cta = any(key in sid for sid in section_ids for key in ["cta", "action", "pricing"])
    if len(sections) >= 5 and has_hero and has_cta:
        metrics.append(EvaluationMetric(name="section_outline", score=25.0, max_score=25.0, passed=True))
    else:
        metrics.append(EvaluationMetric(name="section_outline", score=10.0, max_score=25.0, passed=False, description=f"Sections count={len(sections)}, hero={has_hero}, cta={has_cta}"))
        issues.append(f"Dàn ý sections quá ngắn (< 5) hoặc thiếu hero/cta.")

    # 4. Typography & Tone (20 pts)
    typo = proposal.typography or {}
    has_fonts = bool(typo.get("heading") and typo.get("body"))
    has_tone = bool(proposal.tone_of_voice and len(proposal.tone_of_voice) > 3)
    if has_fonts and has_tone:
        metrics.append(EvaluationMetric(name="typography_and_tone", score=20.0, max_score=20.0, passed=True))
    else:
        metrics.append(EvaluationMetric(name="typography_and_tone", score=10.0, max_score=20.0, passed=False, description="Missing typography fonts or tone"))
        issues.append("Chưa chỉ định rõ font chữ tiêu đề/nội dung hoặc tone of voice.")

    total_score = sum(m.score for m in metrics)
    status = HarnessStatus.PASS if total_score >= 80.0 else HarnessStatus.FAIL

    return EvaluationResult(
        agent_name="proposal",
        test_case_id=test_case_id,
        status=status,
        score=total_score,
        metrics=metrics,
        issues=issues,
        latency_sec=latency_sec,
        output_summary=f"Proposal for: {proposal.target_audience[:40]}...",
        raw_output=output
    )


def evaluate_strategist(output: Any, test_case_id: str = "default", latency_sec: float = 0.0) -> EvaluationResult:
    """Rubric for Strategist Agent (100 pts)."""
    text = str(output or "").strip()
    metrics: List[EvaluationMetric] = []
    issues: List[str] = []

    # 1. Section Coverage (50 pts)
    lower = text.lower()
    core_keys = {
        "hero": any(k in lower for k in ["hero", "headline", "hook"]),
        "features": any(k in lower for k in ["feature", "tính năng", "giải pháp", "solution"]),
        "social_proof": any(k in lower for k in ["social proof", "tin cậy", "trust", "chứng thực", "testimonial"]),
        "cta": any(k in lower for k in ["cta", "hành động", "call to action", "đăng ký"]),
        "faq": any(k in lower for k in ["faq", "hỏi đáp", "thường gặp"])
    }
    hit_count = sum(1 for v in core_keys.values() if v)
    cov_score = (hit_count / len(core_keys)) * 50.0
    metrics.append(EvaluationMetric(
        name="section_coverage",
        score=cov_score,
        max_score=50.0,
        passed=hit_count >= 4,
        description=f"Matched {hit_count}/5 core CRO sections"
    ))
    if hit_count < 4:
        missing = [k for k, v in core_keys.items() if not v]
        issues.append(f"Dàn ý thiếu các phần chiến lược quan trọng: {', '.join(missing)}.")

    # 2. Clarity & Depth (30 pts)
    has_length = len(text) >= 300
    has_structure = bool(re.search(r"(\d+\.|\-|\*|\#\#)", text))
    if has_length and has_structure:
        metrics.append(EvaluationMetric(name="clarity_and_depth", score=30.0, max_score=30.0, passed=True))
    else:
        metrics.append(EvaluationMetric(name="clarity_and_depth", score=15.0, max_score=30.0, passed=False, description="Length < 300 chars or lacks structured headings"))
        issues.append("Bản phân tích dàn ý quá ngắn hoặc thiếu cấu trúc phân mục rõ ràng.")

    # 3. Target Alignment (20 pts)
    has_target = any(k in lower for k in ["khách hàng", "đối tượng", "mục tiêu", "chuyển đổi", "tâm lý"])
    if has_target:
        metrics.append(EvaluationMetric(name="target_alignment", score=20.0, max_score=20.0, passed=True))
    else:
        metrics.append(EvaluationMetric(name="target_alignment", score=5.0, max_score=20.0, passed=False, description="No target audience or conversion focus"))
        issues.append("Chưa tập trung vào đối tượng khách hàng mục tiêu.")

    total_score = sum(m.score for m in metrics)
    status = HarnessStatus.PASS if total_score >= 80.0 else HarnessStatus.FAIL

    return EvaluationResult(
        agent_name="strategist",
        test_case_id=test_case_id,
        status=status,
        score=total_score,
        metrics=metrics,
        issues=issues,
        latency_sec=latency_sec,
        output_summary=f"Strategist Blueprint ({len(text)} chars)",
        raw_output=output
    )


def evaluate_copywriter(output: Any, test_case_id: str = "default", latency_sec: float = 0.0) -> EvaluationResult:
    """Rubric for Copywriter Agent (100 pts)."""
    text = str(output or "").strip()
    metrics: List[EvaluationMetric] = []
    issues: List[str] = []
    lower = text.lower()

    # 1. Headline & Hook (25 pts)
    has_headline = any(k in lower for k in ["tiêu đề", "headline", "slogan", "hook", "h1"]) and len(text) >= 200
    if has_headline:
        metrics.append(EvaluationMetric(name="headline_and_hook", score=25.0, max_score=25.0, passed=True))
    else:
        metrics.append(EvaluationMetric(name="headline_and_hook", score=10.0, max_score=25.0, passed=False, description="Lacks clear hero headline/hook"))
        issues.append("Nội dung thiếu tiêu đề chính nổi bật (Hero headline).")

    # 2. Call To Action (25 pts)
    has_cta = any(k in lower for k in ["cta", "nút", "đăng ký", "bắt đầu", "trải nghiệm", "liên hệ"])
    if has_cta:
        metrics.append(EvaluationMetric(name="call_to_action", score=25.0, max_score=25.0, passed=True))
    else:
        metrics.append(EvaluationMetric(name="call_to_action", score=0.0, max_score=25.0, passed=False, description="No conversion CTA text found"))
        issues.append("Thiếu lời kêu gọi hành động (Call To Action) rõ ràng.")

    # 3. Social Proof & Values (30 pts)
    has_proof = any(k in lower for k in ["khách hàng", "tin dùng", "đánh giá", "cam kết", "lợi ích", "vượt trội", "sao", "%", "triệu"])
    if has_proof:
        metrics.append(EvaluationMetric(name="social_proof_and_values", score=30.0, max_score=30.0, passed=True))
    else:
        metrics.append(EvaluationMetric(name="social_proof_and_values", score=10.0, max_score=30.0, passed=False, description="Lacks testimonials or proof"))
        issues.append("Thiếu yếu tố tạo dựng lòng tin (social proof/con số ấn tượng).")

    # 4. FAQ Completeness (20 pts)
    has_faq = any(k in lower for k in ["faq", "câu hỏi", "thắc mắc", "hỏi đáp"])
    if has_faq:
        metrics.append(EvaluationMetric(name="faq_completeness", score=20.0, max_score=20.0, passed=True))
    else:
        metrics.append(EvaluationMetric(name="faq_completeness", score=5.0, max_score=20.0, passed=False, description="FAQ section missing"))
        issues.append("Chưa có phần giải đáp thắc mắc thường gặp (FAQ).")

    total_score = sum(m.score for m in metrics)
    status = HarnessStatus.PASS if total_score >= 80.0 else HarnessStatus.FAIL

    return EvaluationResult(
        agent_name="copywriter",
        test_case_id=test_case_id,
        status=status,
        score=total_score,
        metrics=metrics,
        issues=issues,
        latency_sec=latency_sec,
        output_summary=f"Copywriter Text ({len(text)} chars)",
        raw_output=output
    )


def evaluate_designer(output: Any, test_case_id: str = "default", latency_sec: float = 0.0) -> EvaluationResult:
    """Rubric for Designer Agent (100 pts)."""
    text = str(output or "").strip()
    metrics: List[EvaluationMetric] = []
    issues: List[str] = []
    lower = text.lower()

    # 1. Color Tokens (30 pts)
    has_colors = bool(re.search(r"#[0-9a-fA-F]{3,6}", text)) or any(k in lower for k in ["palette", "bảng màu", "màu sắc", "primary", "secondary"])
    if has_colors:
        metrics.append(EvaluationMetric(name="color_tokens", score=30.0, max_score=30.0, passed=True))
    else:
        metrics.append(EvaluationMetric(name="color_tokens", score=10.0, max_score=30.0, passed=False, description="No HEX colors or color tokens found"))
        issues.append("Thiếu mã màu hoặc chỉ dẫn bảng màu cụ thể.")

    # 2. Typography Guidance (25 pts)
    has_font = any(k in lower for k in ["font", "typography", "inter", "outfit", "sans", "tiêu đề", "cỡ chữ"])
    if has_font:
        metrics.append(EvaluationMetric(name="typography_guidance", score=25.0, max_score=25.0, passed=True))
    else:
        metrics.append(EvaluationMetric(name="typography_guidance", score=10.0, max_score=25.0, passed=False, description="No font guidance found"))
        issues.append("Thiếu hướng dẫn typography và phân cấp cỡ chữ.")

    # 3. Layout & Spacing Specs (25 pts)
    has_layout = any(k in lower for k in ["grid", "flex", "container", "padding", "margin", "khoảng cách", "px-", "py-", "gap-"])
    if has_layout:
        metrics.append(EvaluationMetric(name="layout_and_spacing", score=25.0, max_score=25.0, passed=True))
    else:
        metrics.append(EvaluationMetric(name="layout_and_spacing", score=10.0, max_score=25.0, passed=False, description="No layout/spacing guidance"))
        issues.append("Thiếu hướng dẫn về bố cục (Grid/Flex) và khoảng cách (Spacing).")

    # 4. Visual Effects (20 pts)
    has_effects = any(k in lower for k in ["gradient", "shadow", "rounded", "glass", "hiệu ứng", "hover", "transition"])
    if has_effects:
        metrics.append(EvaluationMetric(name="visual_effects", score=20.0, max_score=20.0, passed=True))
    else:
        metrics.append(EvaluationMetric(name="visual_effects", score=5.0, max_score=20.0, passed=False, description="No visual effects/interactions specified"))
        issues.append("Thiếu chỉ dẫn hiệu ứng thị giác (Gradient, Shadow, Bo góc).")

    total_score = sum(m.score for m in metrics)
    status = HarnessStatus.PASS if total_score >= 80.0 else HarnessStatus.FAIL

    return EvaluationResult(
        agent_name="designer",
        test_case_id=test_case_id,
        status=status,
        score=total_score,
        metrics=metrics,
        issues=issues,
        latency_sec=latency_sec,
        output_summary=f"Design System Spec ({len(text)} chars)",
        raw_output=output
    )


def evaluate_coder(output: Any, test_case_id: str = "default", latency_sec: float = 0.0) -> EvaluationResult:
    """Rubric for Coder Agent (100 pts)."""
    code = str(output or "").strip()
    metrics: List[EvaluationMetric] = []
    issues: List[str] = []
    lower = code.lower()

    # 1. HTML5 Compliance (30 pts)
    has_doctype = "<!doctype html" in lower
    has_html = "<html" in lower and "</html>" in lower
    has_head = "<head" in lower and "</head>" in lower
    has_body = "<body" in lower and "</body>" in lower
    has_viewport = 'meta name="viewport"' in lower or "meta name='viewport'" in lower
    if has_doctype and has_html and has_head and has_body and has_viewport:
        metrics.append(EvaluationMetric(name="html5_compliance", score=30.0, max_score=30.0, passed=True))
    else:
        missing = []
        if not has_doctype: missing.append("<!DOCTYPE html>")
        if not has_html: missing.append("<html>/</html>")
        if not has_head: missing.append("<head>")
        if not has_body: missing.append("<body>")
        if not has_viewport: missing.append("viewport meta")
        metrics.append(EvaluationMetric(name="html5_compliance", score=10.0, max_score=30.0, passed=False, description=f"Missing: {', '.join(missing)}"))
        issues.append(f"Cấu trúc HTML5 chưa hoàn chỉnh (thiếu {', '.join(missing)}).")

    # 2. CDN Dependencies (25 pts)
    has_tailwind = "cdn.tailwindcss.com" in lower
    has_lucide = "unpkg.com/lucide" in lower or "lucide" in lower
    if has_tailwind and has_lucide:
        metrics.append(EvaluationMetric(name="cdn_dependencies", score=25.0, max_score=25.0, passed=True))
    elif has_tailwind:
        metrics.append(EvaluationMetric(name="cdn_dependencies", score=15.0, max_score=25.0, passed=False, description="Missing Lucide icons CDN"))
        issues.append("Thiếu thẻ nhúng Lucide Icons CDN.")
    else:
        metrics.append(EvaluationMetric(name="cdn_dependencies", score=0.0, max_score=25.0, passed=False, description="Missing Tailwind CSS CDN"))
        issues.append("Thiếu thẻ nhúng Tailwind CSS CDN (<script src='https://cdn.tailwindcss.com'></script>).")

    # 3. Semantic DevTools IDs (20 pts)
    common_ids = ["hero", "features", "cta", "pricing", "faq", "footer"]
    matched_ids = [cid for cid in common_ids if f'id="{cid}"' in lower or f"id='{cid}'" in lower]
    if len(matched_ids) >= 3:
        metrics.append(EvaluationMetric(name="semantic_ids", score=20.0, max_score=20.0, passed=True, description=f"Found IDs: {matched_ids}"))
    else:
        metrics.append(EvaluationMetric(name="semantic_ids", score=10.0, max_score=20.0, passed=False, description=f"Found only {len(matched_ids)} IDs: {matched_ids}"))
        issues.append("Thiếu các ID phân định ngữ cảnh cho DevTools (cần tối thiểu id='hero', id='features', id='cta'...).")

    # 4. Lucide Init & Responsiveness (15 pts)
    has_lucide_init = "lucide.createicons()" in lower or "createicons" in lower
    has_responsive = any(p in code for p in ["sm:", "md:", "lg:", "xl:"])
    if has_lucide_init and has_responsive:
        metrics.append(EvaluationMetric(name="lucide_and_responsive", score=15.0, max_score=15.0, passed=True))
    else:
        metrics.append(EvaluationMetric(name="lucide_and_responsive", score=5.0, max_score=15.0, passed=False, description="Missing lucide.createIcons() or responsive prefixes"))
        issues.append("Thiếu script khởi tạo lucide.createIcons() hoặc các class responsive sm:/md:/lg:.")

    # 5. Clean Code (10 pts)
    has_markdown_leak = "```html" in code or "```" in code
    if not has_markdown_leak:
        metrics.append(EvaluationMetric(name="clean_code", score=10.0, max_score=10.0, passed=True))
    else:
        metrics.append(EvaluationMetric(name="clean_code", score=0.0, max_score=10.0, passed=False, description="Markdown code block fences detected"))
        issues.append("Mã nguồn bị dính markdown code blocks (```html ... ```).")

    total_score = sum(m.score for m in metrics)
    status = HarnessStatus.PASS if total_score >= 80.0 else HarnessStatus.FAIL

    return EvaluationResult(
        agent_name="coder",
        test_case_id=test_case_id,
        status=status,
        score=total_score,
        metrics=metrics,
        issues=issues,
        latency_sec=latency_sec,
        output_summary=f"Single-file HTML5 ({len(code)} bytes)",
        raw_output=output
    )


def evaluate_visual_qa(output: Any, test_case_id: str = "default", latency_sec: float = 0.0) -> EvaluationResult:
    """Rubric for Visual QA Agent (100 pts)."""
    metrics: List[EvaluationMetric] = []
    issues: List[str] = []

    qa_res = output if isinstance(output, dict) else {}
    passed = qa_res.get("qa_passed", False)
    audit = qa_res.get("devtools_audit", {})

    # 1. Syntax Audit (40 pts)
    has_messages = bool(qa_res.get("messages"))
    has_feedback = bool(qa_res.get("qa_feedback"))
    if has_messages and has_feedback:
        metrics.append(EvaluationMetric(name="syntax_audit", score=40.0, max_score=40.0, passed=True))
    else:
        metrics.append(EvaluationMetric(name="syntax_audit", score=15.0, max_score=40.0, passed=False, description="Missing QA feedback or messages"))
        issues.append("Báo cáo QA thiếu thông điệp phản hồi hoặc cấu trúc messages.")

    # 2. Chrome DevTools Telemetry (40 pts)
    has_devtools_fields = "console_errors_count" in audit or "runtime_tested" in audit
    if has_devtools_fields:
        metrics.append(EvaluationMetric(name="devtools_telemetry", score=40.0, max_score=40.0, passed=True))
    else:
        metrics.append(EvaluationMetric(name="devtools_telemetry", score=10.0, max_score=40.0, passed=False, description="No Chrome DevTools MCP telemetry"))
        issues.append("Thiếu dữ liệu kiểm tra runtime từ Chrome DevTools MCP.")

    # 3. Verdict Consistency (20 pts)
    console_errors = audit.get("console_errors_count", 0)
    has_overflow = audit.get("has_overflow", False)
    expected_pass = (console_errors == 0 and not has_overflow and not bool(qa_res.get("errors")))
    verdict_consistent = (passed == expected_pass)
    if verdict_consistent:
        metrics.append(EvaluationMetric(name="verdict_consistency", score=20.0, max_score=20.0, passed=True))
    else:
        metrics.append(EvaluationMetric(name="verdict_consistency", score=0.0, max_score=20.0, passed=False, description=f"Verdict {passed} contradicts runtime metrics"))
        issues.append(f"Kết luận qa_passed={passed} mâu thuẫn với kết quả console={console_errors}, overflow={has_overflow}.")

    total_score = sum(m.score for m in metrics)
    status = HarnessStatus.PASS if total_score >= 80.0 else HarnessStatus.FAIL

    return EvaluationResult(
        agent_name="visual_qa",
        test_case_id=test_case_id,
        status=status,
        score=total_score,
        metrics=metrics,
        issues=issues,
        latency_sec=latency_sec,
        output_summary=f"Visual QA verdict: {'PASS' if passed else 'FAIL'}",
        raw_output=output
    )


def evaluate_element_editor(
    output: Any,
    target_element: Dict[str, Any],
    instruction: str,
    test_case_id: str = "default",
    latency_sec: float = 0.0
) -> EvaluationResult:
    """Rubric for Element Editor Agent (100 pts)."""
    metrics: List[EvaluationMetric] = []
    issues: List[str] = []

    code = str(output or "").strip()
    lower = code.lower()

    # 1. Targeted Output (40 pts) - Must NOT leak the full HTML document
    is_full_doc = any(k in lower for k in ["<!doctype", "<html", "<head", "<body"])
    tag = target_element.get("tag", "").lower()
    has_tag = (f"<{tag}" in lower) if tag else True

    if not is_full_doc and has_tag:
        metrics.append(EvaluationMetric(name="targeted_output", score=40.0, max_score=40.0, passed=True))
    elif is_full_doc:
        metrics.append(EvaluationMetric(name="targeted_output", score=0.0, max_score=40.0, passed=False, description="Leaked entire HTML document instead of element"))
        issues.append("Agent xuất toàn bộ mã nguồn trang web thay vì chỉ phần tử mục tiêu.")
    else:
        metrics.append(EvaluationMetric(name="targeted_output", score=15.0, max_score=40.0, passed=False, description=f"Missing target tag <{tag}>"))
        issues.append(f"Không tìm thấy thẻ mục tiêu <{tag}> trong kết quả.")

    # 2. Instruction Adherence (30 pts)
    # Check if keyword changes from instruction or expected new traits appear
    keywords = [w.lower() for w in re.findall(r"\b\w{3,}\b", instruction) if w.lower() not in ["thành", "sang", "đổi", "thêm", "chữ", "nút"]]
    matched_inst = any(k in lower for k in keywords) if keywords else True
    if matched_inst or len(code) != len(target_element.get("current_html", "")):
        metrics.append(EvaluationMetric(name="instruction_adherence", score=30.0, max_score=30.0, passed=True))
    else:
        metrics.append(EvaluationMetric(name="instruction_adherence", score=10.0, max_score=30.0, passed=False, description="Did not reflect user instruction"))
        issues.append("Chưa phản ánh đúng yêu cầu chỉnh sửa của người dùng.")

    # 3. Structure Integrity (30 pts)
    element_id = target_element.get("element_id")
    has_id = (f'id="{element_id}"' in code or f"id='{element_id}'" in code) if element_id else True
    has_valid_brackets = code.startswith("<") and code.endswith(">")
    if has_id and has_valid_brackets:
        metrics.append(EvaluationMetric(name="structure_integrity", score=30.0, max_score=30.0, passed=True))
    else:
        metrics.append(EvaluationMetric(name="structure_integrity", score=15.0, max_score=30.0, passed=False, description="Broken HTML syntax or lost element ID"))
        issues.append("Mất ID phần tử hoặc thẻ HTML bị lỗi cú pháp đóng/mở.")

    total_score = sum(m.score for m in metrics)
    status = HarnessStatus.PASS if total_score >= 80.0 else HarnessStatus.FAIL

    return EvaluationResult(
        agent_name="element_editor",
        test_case_id=test_case_id,
        status=status,
        score=total_score,
        metrics=metrics,
        issues=issues,
        latency_sec=latency_sec,
        output_summary=f"Edited element: {code[:60]}...",
        raw_output=output
    )
