import os
import sys
from pathlib import Path

# Add backend to sys.path
backend_path = Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from app.agents.visual_qa import visual_qa_node

def test_visual_qa_devtools_e2e():
    print("=" * 65)
    print("🧪 BẮT ĐẦU KIỂM THỬ TOÀN TRÌNH: VISUAL QA CHROME DEVTOOLS MCP")
    print("=" * 65)

    # 1. Test Clean Landing Page
    print("\n[TEST 1] Kiểm tra trang Landing Page sạch không có lỗi...")
    clean_html = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Landing Page Chuẩn</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-900 text-white min-h-screen">
    <header class="p-6 border-b border-slate-800">
        <h1 class="text-2xl font-bold text-indigo-400">Trang Web Mẫu</h1>
    </header>
    <main class="max-w-4xl mx-auto p-8">
        <p class="text-slate-300">Nội dung trang web hiển thị hoàn hảo không có lỗi runtime.</p>
    </main>
</body>
</html>"""
    state_clean = {"code": clean_html, "iteration": 0, "messages": []}
    res_clean = visual_qa_node(state_clean)

    assert res_clean["qa_passed"] is True, f"Trang sạch nhưng bị đánh trượt: {res_clean['qa_feedback']}"
    audit_clean = res_clean["devtools_audit"]
    assert audit_clean["runtime_tested"] is True, "DevTools MCP chưa chạy trên trang"
    assert audit_clean["console_errors_count"] == 0, f"Phát hiện lỗi không mong muốn: {audit_clean['console_errors']}"
    assert audit_clean["has_overflow"] is False, "Báo tràn viền sai"
    print("✅ TEST 1 PASSED: Trang sạch vượt qua kiểm định Chrome DevTools (0 lỗi console, không tràn viền)!")

    # 2. Test Page With Deliberate Runtime Console Error
    print("\n[TEST 2] Thử thách DevTools: Cố ý tiêm mã JavaScript nổ lỗi Runtime...")
    broken_js_html = clean_html.replace(
        "</body>",
        """<script>
            // Cố ý gây lỗi runtime JavaScript
            console.error("Uncaught ReferenceError: nonExistentAnalyticsTracker is not defined");
        </script></body>"""
    )
    state_broken = {"code": broken_js_html, "iteration": 0, "messages": []}
    res_broken = visual_qa_node(state_broken)

    assert res_broken["qa_passed"] is False, "DevTools bỏ sót lỗi console runtime!"
    audit_broken = res_broken["devtools_audit"]
    assert audit_broken["console_errors_count"] > 0, "Không đếm được lỗi console"
    print(f"✅ TEST 2 PASSED: Visual QA đã phát hiện chính xác lỗi JavaScript qua Chrome DevTools MCP:")
    for err in audit_broken["console_errors"]:
        print(f"   🚨 [Bắt được lỗi]: {err}")

    # 3. Test Mobile Layout Overflow (375px)
    print("\n[TEST 3] Thử thách Responsive: Cố ý tạo phần tử tràn màn hình 1200px...")
    overflow_html = clean_html.replace(
        "</body>",
        """<div style="width: 1200px; height: 40px; background: red;">Phần tử cố định gây tràn màn hình điện thoại</div></body>"""
    )
    state_overflow = {"code": overflow_html, "iteration": 0, "messages": []}
    res_overflow = visual_qa_node(state_overflow)

    assert res_overflow["qa_passed"] is False, "DevTools bỏ sót lỗi tràn viền điện thoại!"
    audit_overflow = res_overflow["devtools_audit"]
    assert audit_overflow["has_overflow"] is True, "Không phát hiện được overflow"
    print("✅ TEST 3 PASSED: Visual QA và Chrome DevTools MCP đã bắt được lỗi tràn viền trên màn hình Mobile 375px!")

    print("\n" + "=" * 65)
    print("🏆 TẤT CẢ CÁC BÀI TEST CHROME DEVTOOLS MCP CHO VISUAL QA ĐỀU THÀNH CÔNG RỰC RỠ!")
    print("=" * 65)

if __name__ == "__main__":
    test_visual_qa_devtools_e2e()
