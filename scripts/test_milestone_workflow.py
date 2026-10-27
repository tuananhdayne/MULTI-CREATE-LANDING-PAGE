import sys
import json
import time
import requests

API_BASE = "http://localhost:8000/api/project"

def test_full_milestone_workflow():
    print("=" * 60)
    print("🚀 BẮT ĐẦU KIỂM THỬ TOÀN TRÌNH: HUMAN-IN-THE-LOOP MILESTONE WORKFLOW")
    print("=" * 60)

    # 1. Start Brief
    prompt = "Landing page SaaS Nền tảng AI tự động hóa tuyển dụng & sàng lọc CV thông minh (TalentAI)"
    print(f"\n[CHẶNG 1] Khởi tạo Brief với yêu cầu: '{prompt}'...")
    res = requests.post(f"{API_BASE}/start-brief", json={"prompt": prompt, "auto_pilot": False}, timeout=60)
    assert res.status_code == 200, f"Lỗi start-brief: {res.text}"
    brief_data = res.json()
    session_id = brief_data["session_id"]
    questions = brief_data["questions"]
    print(f"✅ Khởi tạo thành công Session ID: {session_id}")
    print(f"📋 Agent BA đã tạo ra {len(questions)} câu hỏi khảo sát:")
    for idx, q in enumerate(questions, 1):
        print(f"   {idx}. {q['question']}")
        print(f"      Gợi ý: {', '.join(q['quick_options'][:3])}")

    assert len(questions) >= 2, "Cần có ít nhất 2 câu hỏi Brief"

    # 2. Submit Brief answers
    print("\n[CHẶNG 1] Đối tác hoàn tất trả lời câu hỏi Brief...")
    answers = {
        questions[0]["id"]: questions[0]["quick_options"][0] if questions[0]["quick_options"] else "Doanh nghiệp & Startup",
        questions[1]["id"]: "Hiện đại, Công nghệ cao (Dark Mode xanh neon & tím)",
        questions[2]["id"]: "Đặt lịch Demo 1-1 với chuyên gia AI"
    }
    sub_res = requests.post(f"{API_BASE}/submit-brief", json={"session_id": session_id, "answers": answers}, timeout=30)
    assert sub_res.status_code == 200, f"Lỗi submit-brief: {sub_res.text}"
    print("✅ Đã chốt yêu cầu Briefing thành công!")

    # 3. Generate Proposal
    print("\n[CHẶNG 2] Đội ngũ Agent Strategist & Designer lập Bản Đề Xuất Proposal...")
    t0 = time.time()
    prop_res = requests.post(f"{API_BASE}/generate-proposal", json={"session_id": session_id}, timeout=90)
    assert prop_res.status_code == 200, f"Lỗi generate-proposal: {prop_res.text}"
    session_obj = prop_res.json()
    proposal = session_obj["proposal"]
    print(f"✅ Đã tạo Proposal thành công sau {time.time() - t0:.1f}s!")
    print(f"   - Value Proposition: {proposal['value_proposition']}")
    print(f"   - Target Audience: {proposal['target_audience']}")
    print(f"   - Tone of Voice: {proposal['tone_of_voice']}")
    print(f"   - Palette Màu: {proposal['color_palette']}")
    print(f"   - Sections Roadmap ({len(proposal['sections_outline'])} khối):")
    for s in proposal['sections_outline']:
        print(f"     * [{s['id']}] {s['name']}: {s.get('purpose', '')}")

    assert len(proposal['sections_outline']) >= 4, "Proposal cần ít nhất 4 section"

    # 4. Approve Proposal
    print("\n[CHẶNG 2] Đối tác ký duyệt Đề Xuất (Proposal Sign-off)...")
    app_res = requests.post(f"{API_BASE}/approve-proposal", json={"session_id": session_id}, timeout=30)
    assert app_res.status_code == 200, f"Lỗi approve-proposal: {app_res.text}"
    print("✅ Proposal đã được phê duyệt! Trạng thái chuyển sang BUILDING.")

    # 5. Build Code via SSE
    print("\n[CHẶNG 3] Coder & Visual QA bắt tay vào lập trình mã nguồn Landing Page...")
    t_build = time.time()
    build_res = requests.post(
        f"{API_BASE}/build-code",
        json={"session_id": session_id},
        stream=True,
        timeout=300
    )
    assert build_res.status_code == 200, f"Lỗi build-code: {build_res.text}"

    final_session = None
    for line in build_res.iter_lines(decode_unicode=True):
        if not line:
            continue
        if line.startswith(": keep-alive"):
            print(f"   ⏳ [Keep-Alive Heartbeat] Coder đang suy nghĩ & viết mã nguồn... ({time.time() - t_build:.1f}s)")
            continue
        if line.startswith("data: "):
            try:
                payload = json.loads(line[6:])
                msg_type = payload.get("type")
                if msg_type == "step_start":
                    print(f"   ▶ [{payload.get('step', 'AGENT')}] {payload.get('message')}")
                elif msg_type == "complete":
                    final_session = payload.get("session")
                    print("   🎉 Hoàn tất lập trình và thẩm định chất lượng QA!")
            except Exception as e:
                pass

    assert final_session is not None, "Không nhận được event complete từ SSE stream"
    html_code = final_session.get("build", {}).get("html_code", "")
    assert len(html_code) > 1000, f"HTML code quá ngắn ({len(html_code)} bytes)"
    print(f"✅ Mã nguồn HTML5 hoàn chỉnh đã được sinh: {len(html_code):,} bytes")

    # Save to preview file
    out_path = "scripts/milestone_generated_page.html"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html_code)
    print(f"💾 Đã lưu trang web nghiệm thu tại: {out_path}")

    # 6. Test UAT Feedback Loop
    print("\n[CHẶNG 3] Nghiệm thu UAT: Đối tác gửi góp ý tinh chỉnh...")
    uat_res = requests.post(
        f"{API_BASE}/uat-feedback",
        json={"session_id": session_id, "feedback": "Thêm hiệu ứng hover sáng rực cho nút CTA chính"},
        stream=True,
        timeout=180
    )
    assert uat_res.status_code == 200
    print("✅ Vòng lặp phản hồi nghiệm thu UAT hoạt động trơn tru!")

    print("\n" + "=" * 60)
    print("🏆 TOÀN BỘ 3 CHẶNG CỘNG TÁC CHUẨN PHÒNG BAN IT ĐÃ VƯỢT QUA KIỂM THỬ THÀNH CÔNG!")
    print("=" * 60)

if __name__ == "__main__":
    test_full_milestone_workflow()
