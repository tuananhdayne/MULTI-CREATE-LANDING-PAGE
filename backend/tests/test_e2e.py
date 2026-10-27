import pytest
import json
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.services.project_service import get_project_service

client = TestClient(app)


def test_full_e2e_landing_page_pipeline_and_undo_redo():
    service = get_project_service()
    project_id = "e2e-project-lifecycle"

    # Step 1: Health check
    health_res = client.get("/api/health")
    assert health_res.status_code == 200
    assert health_res.json()["status"] == "ok"

    # Step 2: Simulate initial page creation via ProjectService
    html_content = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>E2E Landing Page</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-900 text-white">
    <header class="p-4"><nav>Logo</nav></header>
    <main>
        <section id="hero" class="p-8 text-center">
            <h1 id="hero-title" class="text-4xl font-bold">Quản Lý Chi Tiêu</h1>
            <button id="hero-cta" class="bg-blue-600 text-white px-4 py-2">Bắt đầu</button>
        </section>
    </main>
    <footer>Bản quyền 2026</footer>
</body>
</html>"""

    # Save v1
    p1 = service.save_version(project_id, html_content)
    assert p1.version == 1
    assert p1.can_undo is False

    # Step 3: Tweak element via API (Click-to-Inspect)
    with patch("app.main.tweak_element_node") as mock_tweak:
        tweaked_html = html_content.replace(
            '<button id="hero-cta" class="bg-blue-600 text-white px-4 py-2">Bắt đầu</button>',
            '<button id="hero-cta" class="bg-gradient-to-r from-orange-500 to-amber-500 text-white px-6 py-3 rounded-full">Bắt đầu ngay</button>'
        )
        mock_tweak.return_value = tweaked_html

        tweak_payload = {
            "element_id": "hero-cta",
            "tag": "button",
            "classes": "bg-blue-600 text-white px-4 py-2",
            "current_html": '<button id="hero-cta" class="bg-blue-600 text-white px-4 py-2">Bắt đầu</button>',
            "instruction": "Đổi thành gradient cam và bo tròn full"
        }

        tweak_res = client.post(f"/api/tweak-element?project_id={project_id}", json=tweak_payload)
        assert tweak_res.status_code == 200
        p2 = tweak_res.json()
        assert p2["version"] == 2
        assert p2["can_undo"] is True
        assert "from-orange-500" in p2["code"]

    # Step 4: Verify Undo
    undo_res = client.post(f"/api/undo?project_id={project_id}")
    assert undo_res.status_code == 200
    p_undone = undo_res.json()
    assert p_undone["version"] == 1
    assert "bg-blue-600" in p_undone["code"]
    assert p_undone["can_redo"] is True

    # Step 5: Verify Redo
    redo_res = client.post(f"/api/redo?project_id={project_id}")
    assert redo_res.status_code == 200
    p_redone = redo_res.json()
    assert p_redone["version"] == 2
    assert "from-orange-500" in p_redone["code"]
