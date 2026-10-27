import time
import json
import requests
import sys

BACKEND_URL = "http://localhost:8000"
PROJECT_ID = "landing-session-1"

PROMPT = "Xây dựng Landing Page SaaS cho Nền tảng AI Chatbot CSKH tự động đa kênh 24/7 chuyên biệt cho chuỗi nhà hàng F&B và cửa hàng bán lẻ"
THEME = "modern"

def run_query():
    print("=" * 70, flush=True)
    print("🚀 BẮT ĐẦU CHẠY MULTI-AGENT LANDING PAGE GENERATION", flush=True)
    print(f"📌 Prompt: {PROMPT}", flush=True)
    print(f"🎨 Theme:  {THEME}", flush=True)
    print(f"🌐 Target:  {BACKEND_URL}/api/generate?project_id={PROJECT_ID}", flush=True)
    print("=" * 70, flush=True)

    start_time = time.time()
    url = f"{BACKEND_URL}/api/generate?project_id={PROJECT_ID}"
    payload = {"prompt": PROMPT, "theme": THEME}

    final_code = ""
    agent_logs = []

    try:
        response = requests.post(url, json=payload, stream=True, timeout=(15, 300))
        response.raise_for_status()

        for line in response.iter_lines(decode_unicode=True):
            if not line:
                continue
            if line.startswith(":"):
                # SSE Heartbeat comment
                print(".", end="", flush=True)
                continue
            if line.startswith("data:"):
                raw_data = line[5:].strip()
                try:
                    data = json.loads(raw_data)
                except Exception:
                    continue

                status = data.get("status")
                agent = data.get("agent")
                message = data.get("message", "")
                summary = data.get("summary", "")
                elapsed = round(time.time() - start_time, 1)

                if status == "started":
                    print(f"\n⏱️  [{elapsed:>5}s] 🤖 Agent [{agent.upper()}] BẮT ĐẦU: {message}", flush=True)
                elif status in ("completed", "warning"):
                    icon = "✅" if status == "completed" else "⚠️"
                    print(f"\n⏱️  [{elapsed:>5}s] {icon} Agent [{agent.upper()}] HOÀN THÀNH!", flush=True)
                    if summary:
                        print(f"           📝 Tóm tắt: {summary[:160]}...", flush=True)
                    agent_logs.append({
                        "agent": agent,
                        "time": elapsed,
                        "summary": summary,
                        "full": data.get("full_content", "")
                    })
                elif status == "success":
                    print(f"\n\n🎉 [{elapsed:>5}s] TOÀN BỘ MULTI-AGENT PIPELINE ĐÃ HOÀN THÀNH XUẤT SẮC!", flush=True)
                    project_info = data.get("project", {})
                    final_code = project_info.get("code", "")
                    print(f"   - Project ID: {project_info.get('id')}", flush=True)
                    print(f"   - Phiên bản (Version): {project_info.get('version')}", flush=True)
                    print(f"   - Độ dài mã HTML sinh ra: {len(final_code):,} ký tự", flush=True)
                elif status == "error":
                    print(f"\n\n❌ [{elapsed:>5}s] LỖI: {message}", flush=True)

    except Exception as exc:
        print(f"\n❌ Lỗi kết nối HTTP: {exc}", flush=True)
        sys.exit(1)

    total_time = round(time.time() - start_time, 1)
    print("\n" + "=" * 70, flush=True)
    print(f"🏁 TỔNG THỜI GIAN THỰC THI: {total_time} giây", flush=True)
    print("=" * 70, flush=True)

    if final_code:
        with open("scripts/last_generated_page.html", "w", encoding="utf-8") as f:
            f.write(final_code)
        print("💾 Đã lưu mã nguồn trang web vào file: scripts/last_generated_page.html", flush=True)
    else:
        print("⚠️ Không nhận được mã nguồn HTML cuối cùng.", flush=True)
        sys.exit(1)

if __name__ == "__main__":
    run_query()
