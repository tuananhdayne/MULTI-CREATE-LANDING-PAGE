# Human-in-the-Loop Milestone Workflow Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transform the linear multi-agent generator into a collaborative 3-phase Human-in-the-Loop IT Department workflow (Briefing -> Proposal Review -> Build & Interactive UAT).

**Architecture:** A session-backed milestone state machine in FastAPI coordinating specialized agents (`BAAnalyst`, `ProposalAgent`, `Coder`, `VisualQA`), consumed by a React 18 + Vite frontend with Stepper navigation, interactive Survey/Proposal cards, and a Live Preview UAT board.

**Tech Stack:** Python 3.10+, FastAPI, LangGraph / LangChain OpenAI adapter, Pydantic v2, pytest, React 18, TypeScript, Tailwind CSS, Lucide React, 9router LLM gateway (`ag/gemini-3.8-flash-high` & `ag/gemini-3.8-flash`).

**Spec:** [docs/superpowers/specs/2026-10-27-human-in-the-loop-milestone-workflow-design.md](file:///home/tuananh/GEN_LANDING/docs/superpowers/specs/2026-10-27-human-in-the-loop-milestone-workflow-design.md)

## Global Constraints

- **Python & Pydantic:** Strict type hints and Pydantic v2 models for all request/response schemas.
- **Frontend Types:** Clean TypeScript interfaces with no implicit `any`.
- **Zero Secret Leakage:** Never print, log, or commit `.env` or `GEMINI_API_KEY`.
- **Model Gateway:** Access models through local 9router at `http://localhost:20128/v1` with `streaming=True` and keep-alive heartbeats for long operations.
- **Evidence Before Assertion:** Every task must be verified with automated test output or actual execution evidence before being marked complete.

## Review Focus

1. **Session Resume / Page Refresh:** When a user refreshes the page mid-phase, the system must restore session state from `session_id` without resetting to Phase 1.
2. **Empty or Partial Brief Answers:** If the user skips some questions or inputs minimal text, the system must use sensible industry defaults without crashing.
3. **Proposal Revision Cycle:** When a user rejects a proposal with feedback, the updated proposal must incorporate the user's specific instructions (e.g. changing color palette or adding a comparison table).
4. **SSE Heartbeat during Build:** Code generation takes 30-90s; the backend SSE stream must emit `: keep-alive\n\n` to prevent client read timeouts.
5. **Auto-Pilot Express Lane:** When the user clicks "Bỏ qua & Tạo nhanh", the system must bypass Phases 1 & 2 cleanly, initializing sensible defaults and jumping directly to Phase 3 generation.

---

### Task 1: Session State & Data Schemas

**Files:**
- Create: `backend/app/schemas/session.py`
- Create: `backend/app/services/session_service.py`
- Test: `backend/tests/test_session_service.py`

**Interfaces:**
- Consumes: Nothing
- Produces: `ProjectSession`, `BriefQuestion`, `BriefSubmission`, `DesignProposal`, `UATFeedback`, `SessionService`

- [ ] **Step 1: Write the failing test**

```python
# backend/tests/test_session_service.py
import pytest
from app.schemas.session import ProjectSession, SessionStatus
from app.services.session_service import SessionService

def test_session_lifecycle():
    service = SessionService()
    session = service.create_session(prompt="SaaS for dental clinics")
    assert session.status == SessionStatus.BRIEFING
    assert session.initial_prompt == "SaaS for dental clinics"
    
    # Update brief
    updated = service.update_brief(session.session_id, answers={"target": "Dentists", "tone": "Modern"})
    assert updated.status == SessionStatus.BRIEF_READY
    assert updated.brief.answers["target"] == "Dentists"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest backend/tests/test_session_service.py -v`  
Expected: FAIL with `ModuleNotFoundError: No module named 'app.schemas.session'`

- [ ] **Step 3: Implement schemas & service**

In `backend/app/schemas/session.py`:
- Define `SessionStatus` enum: `BRIEFING`, `BRIEF_READY`, `PROPOSING`, `PROPOSAL_REVIEW`, `BUILDING`, `UAT_REVIEW`, `COMPLETED`.
- Define `BriefQuestion`: `id: str`, `question: str`, `quick_options: list[str]`, `required: bool = True`.
- Define `DesignProposal`: `target_audience: str`, `value_proposition: str`, `sections_outline: list[dict]`, `color_palette: dict[str, str]`, `typography: dict[str, str]`, `tone_of_voice: str`.
- Define `ProjectSession` encompassing state, timestamps, brief, proposal, code, and uat log.

In `backend/app/services/session_service.py`:
- In-memory dictionary `dict[str, ProjectSession]` with thread-safe access.
- Methods: `create_session`, `get_session`, `update_brief`, `set_proposal`, `set_code`, `add_uat_feedback`.

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest backend/tests/test_session_service.py -v`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add backend/app/schemas/session.py backend/app/services/session_service.py backend/tests/test_session_service.py
git commit -m "feat: add session schemas and state manager service"
```

---

### Task 2: BA Requirement Analyst Agent

**Files:**
- Create: `backend/app/agents/ba_analyst.py`
- Test: `backend/tests/test_ba_agent.py`

**Interfaces:**
- Consumes: `initial_prompt: str`
- Produces: `generate_interview_questions(prompt: str) -> list[BriefQuestion]`

- [ ] **Step 1: Write the failing test**

```python
# backend/tests/test_ba_agent.py
import pytest
from app.agents.ba_analyst import BAAnalystAgent

@pytest.mark.asyncio
async def test_ba_generates_three_targeted_questions():
    agent = BAAnalystAgent()
    questions = await agent.generate_questions("Landing page cho nền tảng quản lý tiệm trà sữa")
    assert len(questions) >= 2
    assert all(len(q.quick_options) >= 2 for q in questions)
    assert any("khách hàng" in q.question.lower() or "đối tượng" in q.question.lower() or "target" in q.question.lower() for q in questions)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest backend/tests/test_ba_agent.py -v`  
Expected: FAIL with `ModuleNotFoundError: No module named 'app.agents.ba_analyst'`

- [ ] **Step 3: Implement `BAAnalystAgent`**

In `backend/app/agents/ba_analyst.py`:
- Use `ag/gemini-3.8-flash` via 9router (`ChatOpenAI` at `settings.openai_api_base`).
- Structured system prompt instructing the BA to formulate 3 critical questions (Target Audience, Brand Style & Mood, Primary Conversion Goal) with 3-4 clickable quick suggestions per question.
- Robust JSON parser fallback if LLM response includes markdown fences.

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest backend/tests/test_ba_agent.py -v`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add backend/app/agents/ba_analyst.py backend/tests/test_ba_agent.py
git commit -m "feat: add BA requirement analyst agent"
```

---

### Task 3: Design Proposal Generator Agent

**Files:**
- Create: `backend/app/agents/proposal_agent.py`
- Test: `backend/tests/test_proposal_agent.py`

**Interfaces:**
- Consumes: `initial_prompt: str`, `brief_answers: dict[str, str]`, `feedback: Optional[str]`
- Produces: `generate_proposal(...) -> DesignProposal`

- [ ] **Step 1: Write the failing test**

```python
# backend/tests/test_proposal_agent.py
import pytest
from app.agents.proposal_agent import ProposalAgent

@pytest.mark.asyncio
async def test_proposal_agent_generates_design_spec():
    agent = ProposalAgent()
    proposal = await agent.generate_proposal(
        prompt="SaaS CRM cho môi giới bất động sản",
        brief_answers={"target": "Môi giới cá nhân & sàn giao dịch", "style": "Sang trọng, hiện đại, tối giản"}
    )
    assert len(proposal.sections_outline) >= 4
    assert "primary" in proposal.color_palette
    assert proposal.tone_of_voice != ""
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest backend/tests/test_proposal_agent.py -v`  
Expected: FAIL with `ModuleNotFoundError: No module named 'app.agents.proposal_agent'`

- [ ] **Step 3: Implement `ProposalAgent`**

In `backend/app/agents/proposal_agent.py`:
- Synthesize Strategist CRO framework and Designer visual styling into a cohesive structured proposal.
- If `feedback` is passed (e.g. "Đổi sang màu tối neon và bổ sung bảng so sánh giá"), adjust color tokens and section outline accordingly.

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest backend/tests/test_proposal_agent.py -v`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add backend/app/agents/proposal_agent.py backend/tests/test_proposal_agent.py
git commit -m "feat: add proposal agent for concept and outline generation"
```

---

### Task 4: Milestone REST & SSE Endpoints

**Files:**
- Create: `backend/app/routers/project.py`
- Modify: `backend/app/main.py`
- Test: `backend/tests/test_project_api.py`

**Interfaces:**
- Consumes: `SessionService`, `BAAnalystAgent`, `ProposalAgent`, `coder_node`, `visual_qa_node`
- Produces:
  - `POST /api/project/start-brief`
  - `POST /api/project/submit-brief`
  - `POST /api/project/generate-proposal`
  - `POST /api/project/approve-proposal`
  - `POST /api/project/build-code` (SSE with keep-alive)
  - `POST /api/project/uat-feedback` (SSE with keep-alive)
  - `GET /api/project/session/{session_id}`

- [ ] **Step 1: Write the failing test**

```python
# backend/tests/test_project_api.py
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_api_start_brief_and_get_session():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.post("/api/project/start-brief", json={"prompt": "Ứng dụng đặt món ăn healthy"})
        assert res.status_code == 200
        data = res.json()
        assert "session_id" in data
        assert len(data["questions"]) >= 2
        
        # Check get session
        s_res = await client.get(f"/api/project/session/{data['session_id']}")
        assert s_res.status_code == 200
        assert s_res.json()["status"] == "BRIEFING"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest backend/tests/test_project_api.py -v`  
Expected: FAIL with 404 Not Found on `/api/project/start-brief`

- [ ] **Step 3: Implement endpoints in `backend/app/routers/project.py`**

- Wire router into `backend/app/main.py`.
- Handle SSE heartbeats (`: keep-alive\n\n`) on `build-code` and `uat-feedback` to prevent network timeouts.
- Implement Auto-pilot mode bypass when requested.

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest backend/tests/test_project_api.py -v`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add backend/app/routers/project.py backend/app/main.py backend/tests/test_project_api.py
git commit -m "feat: add milestone workflow REST and SSE endpoints"
```

---

### Task 5: Frontend TypeScript Types & Session Hook

**Files:**
- Create: `frontend/src/types/project.ts`
- Create: `frontend/src/hooks/useProjectSession.ts`
- Test: Build validation via `npm run build`

**Interfaces:**
- Consumes: Backend API `/api/project/*`
- Produces: `useProjectSession()` hook exposing `session`, `activePhase`, `loading`, `error`, `actions`

- [ ] **Step 1: Create types and hook**

In `frontend/src/types/project.ts`:
- Define `BriefQuestion`, `DesignProposal`, `ProjectSession`, `PhaseStep`.

In `frontend/src/hooks/useProjectSession.ts`:
- State for `session`, `activePhase` (1, 2, or 3), `autoPilotMode`.
- Methods: `startBrief(prompt)`, `submitBrief(answers)`, `generateProposal(feedback?)`, `approveProposal()`, `buildCode()`, `submitUATFeedback(feedback)`.
- Persist `session_id` in `localStorage` so reload maintains state.

- [ ] **Step 2: Run build to verify type safety**

Run: `cd frontend && npm run build`  
Expected: PASS with 0 TypeScript errors.

- [ ] **Step 3: Commit**

```bash
git add frontend/src/types/project.ts frontend/src/hooks/useProjectSession.ts
git commit -m "feat: add frontend project session state and types"
```

---

### Task 6: Frontend Phase 1 Component: Brief Questionnaire

**Files:**
- Create: `frontend/src/components/milestones/BriefSurveyCard.tsx`
- Modify: `frontend/src/components/Header.tsx` (Add Stepper indicator & Auto-pilot toggle)
- Test: Build validation and visual render check

**Interfaces:**
- Consumes: `questions: BriefQuestion[]`, `onSubmit: (answers) => void`, `onAutoPilot: () => void`
- Produces: Interactive survey cards with quick suggestion chips and submit action.

- [ ] **Step 1: Implement `BriefSurveyCard.tsx`**

- Render cards for each question with Lucide icons (Users, Palette, Target).
- Clickable suggestion chips that auto-populate text inputs.
- Secondary action: "⚡ Bỏ qua & Tạo nhanh (Auto-pilot 1-Click)" button.
- Primary CTA: "Chốt Yêu Cầu & Chuyển Sang Duyệt Concept ->"

- [ ] **Step 2: Add Stepper Indicator in Header**

- Show 3 stages: `1. Khảo sát Brief` -> `2. Duyệt Concept` -> `3. Nghiệm thu & Live Preview`.
- Highlight current active phase with glow and badge.

- [ ] **Step 3: Run build to verify**

Run: `cd frontend && npm run build`  
Expected: PASS

- [ ] **Step 4: Commit**

```bash
git add frontend/src/components/milestones/BriefSurveyCard.tsx frontend/src/components/Header.tsx
git commit -m "feat: implement Phase 1 Brief survey questionnaire and header stepper"
```

---

### Task 7: Frontend Phase 2 Component: Proposal Review Card

**Files:**
- Create: `frontend/src/components/milestones/ProposalReviewCard.tsx`
- Test: Build validation and visual render check

**Interfaces:**
- Consumes: `proposal: DesignProposal`, `onApprove: () => void`, `onRevise: (feedback: string) => void`
- Produces: Visual proposal card showing color chips, section roadmap, and approval controls.

- [ ] **Step 1: Implement `ProposalReviewCard.tsx`**

- Color palette display: Primary, Secondary, Accent, Background chips with hex values.
- Typography & Tone badges (e.g. "Chuyên nghiệp", "Inter + Outfit").
- Section Roadmap: Timeline list of planned sections (Hero, Value Prop, Features, Social Proof, CTA).
- Action buttons:
  - `[Phê duyệt & Bắt Đầu Lập Trình]` (Green gradient glow)
  - `[Yêu cầu chỉnh sửa concept]` (Opens concise feedback modal/textarea)

- [ ] **Step 2: Run build to verify**

Run: `cd frontend && npm run build`  
Expected: PASS

- [ ] **Step 3: Commit**

```bash
git add frontend/src/components/milestones/ProposalReviewCard.tsx
git commit -m "feat: implement Phase 2 Proposal review card with visual styling tokens"
```

---

### Task 8: Frontend Phase 3 Component: Live Preview & UAT Board

**Files:**
- Create: `frontend/src/components/milestones/UATPanel.tsx`
- Modify: `frontend/src/App.tsx` (Wire 3 phases seamlessly)
- Test: Build validation and integration check

**Interfaces:**
- Consumes: `session.build`, `onSendFeedback: (text: string) => void`, `onAcceptFinal: () => void`
- Produces: Collapsible UAT feedback board alongside `LivePreview` and DevTools Click-to-Inspect.

- [ ] **Step 1: Implement `UATPanel.tsx`**

- QA Checklist summary (Valid semantic HTML, Responsive tags, Clean CSS).
- Feedback submission bar: "Góp ý chỉnh sửa trang web..." with submit button.
- "Ký duyệt nghiệm thu & Xuất bản" button allowing instant HTML download.

- [ ] **Step 2: Connect all 3 phases in `App.tsx`**

- If `activePhase === 1`: show `BriefSurveyCard`.
- If `activePhase === 2`: show `ProposalReviewCard`.
- If `activePhase === 3`: show `LivePreview` + `UATPanel`.

- [ ] **Step 3: Run build to verify**

Run: `cd frontend && npm run build`  
Expected: PASS

- [ ] **Step 4: Commit**

```bash
git add frontend/src/components/milestones/UATPanel.tsx frontend/src/App.tsx
git commit -m "feat: integrate Phase 3 UAT board and complete milestone app state"
```

---

### Task 9: End-to-End Verification & Evidence

**Files:**
- Create: `scripts/test_milestone_workflow.py`
- Test: End-to-end multi-phase query run

**Interfaces:**
- Consumes: Running backend on port 8000 and frontend on port 5173
- Produces: Full log trace of Phase 1 (Brief) -> Phase 2 (Proposal) -> Phase 3 (Build) and screenshot evidence.

- [ ] **Step 1: Write and run verification script**

Run: `python3 scripts/test_milestone_workflow.py`  
Verify:
1. `start-brief` returns 3 relevant questions with options.
2. `submit-brief` records answers.
3. `generate-proposal` returns valid color palette and section list.
4. `approve-proposal` & `build-code` streams HTML to completion.
5. Capture screenshot of rendered page.

- [ ] **Step 2: Check Git status and verify zero secrets**

Run: `git status && git log -n 5`  
Verify: Clean working tree, no untracked `.env` files.

- [ ] **Step 3: Commit and push**

```bash
git add scripts/test_milestone_workflow.py
git commit -m "test: add end-to-end verification script for milestone workflow"
git push origin main
```
