import json
import uuid
import asyncio
from typing import Optional, AsyncGenerator
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from app.config import get_settings
from app.models.api_schemas import (
    GenerateRequest,
    TweakElementRequest,
    ProjectResponse,
    AgentProgressEvent,
)
from app.models.state import AgentState
from app.agents.strategist import strategist_node
from app.agents.copywriter import copywriter_node
from app.agents.designer import designer_node
from app.agents.coder import coder_node
from app.agents.visual_qa import qa_node
from app.agents.element_editor import tweak_element_node
from app.graph.workflow import should_continue_qa
from app.services.project_service import get_project_service

app = FastAPI(
    title="Multi-Agent Landing Page Builder API",
    description="Backend API coordinating 5 AI Agents to generate and live-edit high-converting landing pages.",
    version="1.0.0"
)

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health_check():
    """
    Health check endpoint.
    Safely reports system readiness and active model without exposing API keys.
    """
    settings = get_settings()
    has_key = bool(settings.gemini_api_key and settings.gemini_api_key != "your_gemini_api_key_here")
    return {
        "status": "ok",
        "model": settings.gemini_model,
        "has_api_key": has_key,
        "masked_key": settings.masked_api_key
    }


@app.get("/api/project", response_model=ProjectResponse)
def get_project(project_id: str = Query(default="default-project")):
    """
    Retrieves the current project state, code, and undo/redo capabilities.
    """
    service = get_project_service()
    project = service.get_project(project_id)
    if not project:
        # Return initial empty project session
        return ProjectResponse(
            id=project_id,
            code="",
            version=0,
            can_undo=False,
            can_redo=False
        )
    return project


@app.post("/api/undo", response_model=ProjectResponse)
def undo_project(project_id: str = Query(default="default-project")):
    """
    Reverts to the previous landing page version.
    """
    service = get_project_service()
    project = service.undo(project_id)
    if not project:
        raise HTTPException(status_code=400, detail="Không thể hoàn tác phiên bản này.")
    return project


@app.post("/api/redo", response_model=ProjectResponse)
def redo_project(project_id: str = Query(default="default-project")):
    """
    Redoes an undone landing page version.
    """
    service = get_project_service()
    project = service.redo(project_id)
    if not project:
        raise HTTPException(status_code=400, detail="Không thể làm lại phiên bản này.")
    return project


@app.post("/api/tweak-element", response_model=ProjectResponse)
def tweak_element(
    request: TweakElementRequest,
    project_id: str = Query(default="default-project")
):
    """
    Performs targeted element modification using Chrome DevTools context.
    """
    service = get_project_service()
    current_project = service.get_project(project_id)

    full_code = request.full_code or (current_project.code if current_project else "")
    if not full_code:
        raise HTTPException(status_code=400, detail="Chưa có mã nguồn trang web để chỉnh sửa.")

    target_element_data = {
        "element_id": request.element_id,
        "tag": request.tag,
        "classes": request.classes,
        "current_html": request.current_html
    }

    updated_code = tweak_element_node(
        full_code=full_code,
        target_element=target_element_data,
        instruction=request.instruction
    )

    return service.save_version(project_id, updated_code)


async def sse_agent_pipeline_generator(
    prompt: str,
    theme: str,
    project_id: str
) -> AsyncGenerator[str, None]:
    """
    Executes the multi-agent graph sequentially and streams real-time progress events via SSE.
    """
    service = get_project_service()

    state: AgentState = {
        "prompt": prompt,
        "theme": theme,
        "messages": [],
        "iteration": 0
    }

    def format_sse(event_type: str, data: dict) -> str:
        return f"event: {event_type}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"

    try:
        # Step 1: Strategist Agent
        yield format_sse("agent_progress", {
            "agent": "strategist",
            "status": "started",
            "message": "Chiến lược gia (Strategist) đang phân tích yêu cầu và lên dàn ý chuyển đổi..."
        })
        strategist_res = await asyncio.to_thread(strategist_node, state)
        state.update(strategist_res)
        yield format_sse("agent_progress", {
            "agent": "strategist",
            "status": "completed",
            "message": "Đã hoàn thành cấu trúc dàn ý chiến lược.",
            "summary": state.get("outline", "")[:350]
        })

        # Step 2: Copywriter Agent
        yield format_sse("agent_progress", {
            "agent": "copywriter",
            "status": "started",
            "message": "Copywriter đang soạn thảo tiêu đề, lời kêu gọi (CTAs) và nội dung bán hàng..."
        })
        copywriter_res = await asyncio.to_thread(copywriter_node, state)
        state.update(copywriter_res)
        yield format_sse("agent_progress", {
            "agent": "copywriter",
            "status": "completed",
            "message": "Đã hoàn thành nội dung chuyển đổi cho từng mục.",
            "summary": state.get("copy", "")[:350]
        })

        # Step 3: UI Designer Agent
        yield format_sse("agent_progress", {
            "agent": "designer",
            "status": "started",
            "message": "UI/UX Designer đang thiết lập hệ màu Tailwind, Typography và hiệu ứng thị giác..."
        })
        designer_res = await asyncio.to_thread(designer_node, state)
        state.update(designer_res)
        yield format_sse("agent_progress", {
            "agent": "designer",
            "status": "completed",
            "message": "Đã hoàn thành Design System và hiệu ứng giao diện.",
            "summary": state.get("design", "")[:350]
        })

        # Step 4: Coder & QA Loop
        qa_passed = False
        iteration = 0
        while not qa_passed and iteration < 2:
            iteration += 1
            state["iteration"] = iteration

            # Coder
            coder_msg = "Frontend Coder đang viết mã HTML5 + Tailwind CSS hoàn chỉnh..." if iteration == 1 else f"Frontend Coder đang sửa đổi mã nguồn theo phản hồi QA (vòng {iteration})..."
            yield format_sse("agent_progress", {
                "agent": "coder",
                "status": "started",
                "message": coder_msg
            })
            coder_res = await asyncio.to_thread(coder_node, state)
            state.update(coder_res)
            yield format_sse("agent_progress", {
                "agent": "coder",
                "status": "completed",
                "message": "Đã lập trình xong mã nguồn trang web."
            })

            # Visual QA
            yield format_sse("agent_progress", {
                "agent": "qa",
                "status": "started",
                "message": "Visual QA đang kiểm tra tính toàn vẹn cú pháp HTML và Tailwind CDN..."
            })
            qa_res = await asyncio.to_thread(qa_node, state)
            state.update(qa_res)
            qa_passed = qa_res.get("qa_passed", False)

            yield format_sse("agent_progress", {
                "agent": "qa",
                "status": "completed" if qa_passed else "warning",
                "message": qa_res.get("qa_feedback", ""),
                "passed": qa_passed
            })

        # Finalize and Save Version
        final_code = state.get("code", "")
        project = service.save_version(project_id, final_code)

        yield format_sse("done", {
            "status": "success",
            "message": "Landing Page đã được tạo thành công!",
            "project": project.model_dump()
        })

    except Exception as exc:
        yield format_sse("error", {
            "status": "error",
            "message": f"Đã xảy ra lỗi trong quá trình điều phối Agent: {str(exc)}"
        })


@app.post("/api/generate")
async def generate_landing_page(
    request: GenerateRequest,
    project_id: Optional[str] = Query(default=None)
):
    """
    SSE Streaming endpoint triggering the 5-agent pipeline.
    Streams incremental status and outputs the final HTML5 landing page.
    """
    active_project_id = project_id or str(uuid.uuid4())
    return StreamingResponse(
        sse_agent_pipeline_generator(
            prompt=request.prompt,
            theme=request.theme,
            project_id=active_project_id
        ),
        media_type="text/event-stream"
    )
