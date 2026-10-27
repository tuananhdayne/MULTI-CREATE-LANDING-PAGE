import pytest
import json
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.services.project_service import get_project_service

client = TestClient(app)


def test_health_check_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "model" in data
    # Security check: Never return the API key
    assert "api_key" not in data
    assert "gemini_api_key" not in data


def test_project_get_and_undo_redo():
    service = get_project_service()
    project_id = "api-test-session"
    service.save_version(project_id, "<html><body>v1</body></html>")
    service.save_version(project_id, "<html><body>v2</body></html>")

    # 1. GET /api/project
    get_res = client.get(f"/api/project?project_id={project_id}")
    assert get_res.status_code == 200
    data = get_res.json()
    assert data["id"] == project_id
    assert data["version"] == 2
    assert "v2" in data["code"]
    assert data["can_undo"] is True

    # 2. POST /api/undo
    undo_res = client.post(f"/api/undo?project_id={project_id}")
    assert undo_res.status_code == 200
    undo_data = undo_res.json()
    assert undo_data["version"] == 1
    assert "v1" in undo_data["code"]
    assert undo_data["can_redo"] is True

    # 3. POST /api/redo
    redo_res = client.post(f"/api/redo?project_id={project_id}")
    assert redo_res.status_code == 200
    redo_data = redo_res.json()
    assert redo_data["version"] == 2
    assert "v2" in redo_data["code"]


@patch("app.main.tweak_element_node")
def test_tweak_element_endpoint(mock_tweak):
    service = get_project_service()
    project_id = "tweak-test-session"
    initial_html = "<!DOCTYPE html><html><body><button id='btn'>Old</button></body></html>"
    service.save_version(project_id, initial_html)

    mock_tweak.return_value = "<!DOCTYPE html><html><body><button id='btn' class='new'>New</button></body></html>"

    payload = {
        "element_id": "btn",
        "tag": "button",
        "classes": "old",
        "current_html": "<button id='btn'>Old</button>",
        "instruction": "Đổi thành class new và chữ New"
    }

    response = client.post(f"/api/tweak-element?project_id={project_id}", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "new" in data["code"]
    assert data["version"] == 2
