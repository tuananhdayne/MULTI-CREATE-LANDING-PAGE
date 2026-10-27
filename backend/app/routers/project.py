import asyncio
import json
from typing import Optional, Dict, Any
from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from app.services.session_service import session_service
from app.schemas.session import SessionStatus, ProjectSession
from app.agents.ba_analyst import BAAnalystAgent
from app.agents.proposal_agent import ProposalAgent
from app.agents.coder import coder_node
from app.agents.visual_qa import visual_qa_node
from app.agents.element_editor import tweak_element_node

router = APIRouter(prefix="/api/project", tags=["Project Milestones"])

ba_agent = BAAnalystAgent()
proposal_agent = ProposalAgent()

class StartBriefRequest(BaseModel):
    prompt: str = Field(..., min_length=3)
    auto_pilot: bool = False

class SubmitBriefRequest(BaseModel):
    session_id: str
    answers: Dict[str, str]

class GenerateProposalRequest(BaseModel):
    session_id: str
    feedback: Optional[str] = None

class ApproveProposalRequest(BaseModel):
    session_id: str

class BuildCodeRequest(BaseModel):
    session_id: str

class UATFeedbackRequest(BaseModel):
    session_id: str
    feedback: str
    target_element_id: Optional[str] = None

@router.post("/start-brief")
async def start_brief(req: StartBriefRequest):
    session = session_service.create_session(prompt=req.prompt)
    if req.auto_pilot:
        # Auto-pilot mode: bypass interview
        default_proposal = await proposal_agent.generate_proposal(
            prompt=req.prompt,
            brief_answers={
                "target_audience": "Khách hàng đại chúng & doanh nghiệp",
                "brand_style": "Hiện đại, cao cấp",
                "conversion_goal": "Đăng ký dùng thử ngay"
            }
        )
        session_service.set_proposal(session.session_id, default_proposal.model_dump())
        session_service.approve_proposal(session.session_id)
        return {
            "session_id": session.session_id,
            "status": SessionStatus.BUILDING,
            "auto_pilot": True,
            "questions": []
        }

    questions = await ba_agent.generate_questions(req.prompt)
    session_service.set_brief_questions(session.session_id, questions)
    return {
        "session_id": session.session_id,
        "status": SessionStatus.BRIEFING,
        "auto_pilot": False,
        "questions": [q.model_dump() for q in questions]
    }

@router.get("/session/{session_id}")
async def get_session(session_id: str):
    session = session_service.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.post("/submit-brief")
async def submit_brief(req: SubmitBriefRequest):
    session = session_service.get_session(req.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    updated = session_service.update_brief(req.session_id, req.answers)
    return updated

@router.post("/generate-proposal")
async def generate_proposal(req: GenerateProposalRequest):
    session = session_service.get_session(req.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    proposal = await proposal_agent.generate_proposal(
        prompt=session.initial_prompt,
        brief_answers=session.brief.answers,
        feedback=req.feedback
    )
    updated = session_service.set_proposal(req.session_id, proposal.model_dump())
    return updated

@router.post("/approve-proposal")
async def approve_proposal(req: ApproveProposalRequest):
    session = session_service.get_session(req.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    updated = session_service.approve_proposal(req.session_id)
    return updated

@router.post("/build-code")
async def build_code(req: BuildCodeRequest):
    session = session_service.get_session(req.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    async def event_generator():
        proposal = session.proposal
        if not proposal:
            yield f"data: {json.dumps({'type': 'error', 'message': 'Không tìm thấy proposal đã duyệt'}, ensure_ascii=False)}\n\n"
            return

        async def run_node_with_heartbeat(func, current_state):
            task = asyncio.create_task(asyncio.to_thread(func, current_state))
            while not task.done():
                try:
                    res = await asyncio.wait_for(asyncio.shield(task), timeout=8.0)
                    yield ("result", res)
                    return
                except asyncio.TimeoutError:
                    yield ("heartbeat", ": keep-alive\n\n")

        # Step 1: Coder
        yield f"data: {json.dumps({'type': 'step_start', 'step': 'coder', 'message': 'Coder đang tiến hành lập trình Landing Page theo Proposal...'}, ensure_ascii=False)}\n\n"

        coder_state = {
            "prompt": session.initial_prompt,
            "outline": json.dumps(proposal.sections_outline, ensure_ascii=False, indent=2),
            "copy": f"Tiêu đề chính: {proposal.value_proposition}\nĐối tượng mục tiêu: {proposal.target_audience}\nTone giọng: {proposal.tone_of_voice}",
            "design": json.dumps({
                "palette": proposal.color_palette,
                "typography": proposal.typography,
                "tone": proposal.tone_of_voice
            }, ensure_ascii=False, indent=2),
            "qa_feedback": "",
            "iteration": 0,
            "messages": []
        }

        coder_res = {}
        async for kind, val in run_node_with_heartbeat(coder_node, coder_state):
            if kind == "heartbeat":
                yield val
            else:
                coder_res = val

        html_code = coder_res.get("code", "")

        # Step 2: Visual QA
        yield f"data: {json.dumps({'type': 'step_start', 'step': 'visual_qa', 'message': 'Visual QA đang kiểm định tính hợp lệ của mã nguồn HTML5...'}, ensure_ascii=False)}\n\n"

        qa_state = {**coder_state, "code": html_code}
        qa_res = {}
        async for kind, val in run_node_with_heartbeat(visual_qa_node, qa_state):
            if kind == "heartbeat":
                yield val
            else:
                qa_res = val

        # Save to session
        updated_session = session_service.set_code(req.session_id, html_code=html_code, qa_report=qa_res)

        yield f"data: {json.dumps({'type': 'complete', 'session': updated_session.model_dump()}, ensure_ascii=False)}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@router.post("/uat-feedback")
async def uat_feedback(req: UATFeedbackRequest):
    session = session_service.get_session(req.session_id)
    if not session or not session.build:
        raise HTTPException(status_code=404, detail="Session or build not found")

    session_service.add_uat_feedback(req.session_id, req.feedback, req.target_element_id)

    async def event_generator():
        yield f"data: {json.dumps({'type': 'step_start', 'message': 'Đang áp dụng góp ý UAT vào mã nguồn...'}, ensure_ascii=False)}\n\n"

        current_html = session.build.html_code
        if req.target_element_id:
            # Targeted element edit
            task = asyncio.create_task(
                asyncio.to_thread(
                    tweak_element_node,
                    full_code=current_html,
                    target_element={"element_id": req.target_element_id, "current_html": f"id='{req.target_element_id}'"},
                    instruction=req.feedback
                )
            )
            while not task.done():
                try:
                    new_html = await asyncio.wait_for(asyncio.shield(task), timeout=5.0)
                    break
                except asyncio.TimeoutError:
                    yield ": keep-alive\n\n"
        else:
            # Full page refinement via coder
            state = {
                "prompt": session.initial_prompt,
                "outline": "",
                "copy": "",
                "design": "",
                "qa_feedback": f"Góp ý sửa đổi UAT từ đối tác: {req.feedback}",
                "iteration": 1,
                "messages": []
            }
            task = asyncio.create_task(asyncio.to_thread(coder_node, state))
            while not task.done():
                try:
                    refine_res = await asyncio.wait_for(asyncio.shield(task), timeout=8.0)
                    new_html = refine_res.get("code", current_html)
                    break
                except asyncio.TimeoutError:
                    yield ": keep-alive\n\n"

        updated_session = session_service.set_code(req.session_id, html_code=new_html, qa_report={"uat_refined": True})
        yield f"data: {json.dumps({'type': 'complete', 'session': updated_session.model_dump()}, ensure_ascii=False)}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
