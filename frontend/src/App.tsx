import React, { useState, useEffect } from "react";
import { Header } from "./components/Header";
import { PromptInput } from "./components/PromptInput";
import { AgentTimeline } from "./components/AgentTimeline";
import { LivePreview } from "./components/LivePreview";
import { InspectModal } from "./components/InspectModal";
import { CodeModal } from "./components/CodeModal";
import { BriefSurveyCard } from "./components/milestones/BriefSurveyCard";
import { ProposalReviewCard } from "./components/milestones/ProposalReviewCard";
import { UATPanel } from "./components/milestones/UATPanel";
import { useProjectSession } from "./hooks/useProjectSession";
import { api } from "./services/api";
import type { HealthStatus } from "./services/api";
import { Sparkles, Layers, ArrowLeft } from "lucide-react";

export function App() {
  const {
    session,
    activePhase,
    setActivePhase,
    loading: sessionLoading,
    statusMessage,
    error: sessionError,
    startBrief,
    submitBrief,
    reviseProposal,
    approveProposalAndBuild,
    submitUATFeedback,
    resetProject,
  } = useProjectSession();

  const [viewport, setViewport] = useState<"desktop" | "tablet" | "mobile">("desktop");
  const [inspectMode, setInspectMode] = useState<boolean>(false);
  const [selectedElement, setSelectedElement] = useState<any | null>(null);
  const [isTweaking, setIsTweaking] = useState<boolean>(false);
  const [isCodeModalOpen, setIsCodeModalOpen] = useState<boolean>(false);
  const [health, setHealth] = useState<HealthStatus | null>(null);
  const [errorToast, setErrorToast] = useState<string | null>(null);

  // Check health on mount
  useEffect(() => {
    api.getHealth()
      .then((h) => setHealth(h))
      .catch((err) => console.warn("Backend not available yet:", err.message));
  }, []);

  useEffect(() => {
    if (sessionError) {
      setErrorToast(sessionError);
    }
  }, [sessionError]);

  // Initial prompt submit -> Starts Phase 1 (Briefing)
  const handleInitialPrompt = async (prompt: string, _theme: string) => {
    await startBrief(prompt, false);
  };

  // Auto-pilot express lane
  const handleAutoPilot = async () => {
    if (session) {
      await startBrief(session.initial_prompt, true);
    }
  };

  // Targeted element edit in Phase 3
  const handleTweakElement = async (instruction: string) => {
    if (!selectedElement) return;
    setIsTweaking(true);
    try {
      await submitUATFeedback(instruction, selectedElement.element_id);
      setSelectedElement(null);
      setInspectMode(false);
    } catch (err: any) {
      setErrorToast("Lỗi khi chỉnh sửa phần tử: " + err.message);
    } finally {
      setIsTweaking(false);
    }
  };

  // Download final HTML
  const handleDownload = () => {
    const code = session?.build?.html_code;
    if (!code) return;
    const blob = new Blob([code], { type: "text/html;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "landing-page.html";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const currentHtml = session?.build?.html_code || "";

  return (
    <div className="flex flex-col h-screen w-screen bg-slate-950 text-slate-100 overflow-hidden font-sans">
      {/* Top Header with 3-Phase Stepper */}
      <Header
        viewport={viewport}
        setViewport={setViewport}
        inspectMode={inspectMode}
        setInspectMode={setInspectMode}
        canUndo={false}
        canRedo={false}
        version={session?.uat_history.length || 1}
        onUndo={() => {}}
        onRedo={() => {}}
        onOpenCode={() => setIsCodeModalOpen(true)}
        onDownload={handleDownload}
        modelName={health?.model || "ag/gemini-3.8-flash"}
        hasCode={Boolean(currentHtml)}
        activePhase={activePhase}
        setActivePhase={setActivePhase}
      />

      {/* Main Container */}
      <div className="flex-1 flex flex-col overflow-hidden relative">
        {/* Loading overlay banner when agents are working */}
        {sessionLoading && (
          <div className="bg-indigo-600/90 text-white text-xs px-4 py-2.5 flex items-center justify-center gap-2.5 backdrop-blur-md shadow-lg z-40 animate-pulse">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
            <span className="font-semibold">{statusMessage || "Đội ngũ IT Agent đang xử lý..."}</span>
          </div>
        )}

        {/* State 0: Initial Screen (No session yet) */}
        {!session && (
          <div className="flex-1 flex flex-col items-center justify-center p-6 max-w-2xl mx-auto w-full text-center">
            <div className="w-16 h-16 rounded-3xl bg-gradient-to-tr from-indigo-600 via-indigo-500 to-emerald-400 flex items-center justify-center shadow-2xl shadow-indigo-500/30 mb-6">
              <Sparkles className="w-8 h-8 text-white" />
            </div>
            <h2 className="text-3xl font-extrabold text-white tracking-tight mb-2">
              Phòng Ban IT AI Phát Triển Landing Page
            </h2>
            <p className="text-sm text-slate-400 max-w-md mb-8">
              Cộng tác thông minh qua 3 chặng: Khảo sát Brief chuẩn BA, Duyệt đề xuất thiết kế & Wireframe, rồi mới chuyển giao lập trình nghiệm thu UAT.
            </p>
            <div className="w-full text-left">
              <PromptInput onGenerate={handleInitialPrompt} isGenerating={sessionLoading} />
            </div>
          </div>
        )}

        {/* State 1: Phase 1 - Brief Questionnaire */}
        {session && activePhase === 1 && (
          <div className="flex-1 overflow-y-auto p-4">
            <div className="max-w-4xl mx-auto flex items-center justify-between mb-4">
              <button
                onClick={resetProject}
                className="text-xs text-slate-400 hover:text-white flex items-center gap-1.5 transition-colors"
              >
                <ArrowLeft className="w-3.5 h-3.5" />
                <span>Bắt đầu dự án mới</span>
              </button>
            </div>
            <BriefSurveyCard
              prompt={session.initial_prompt}
              questions={session.brief.questions || []}
              loading={sessionLoading}
              onSubmit={submitBrief}
              onAutoPilot={handleAutoPilot}
            />
          </div>
        )}

        {/* State 2: Phase 2 - Proposal Review Card */}
        {session && activePhase === 2 && session.proposal && (
          <div className="flex-1 overflow-y-auto p-4">
            <div className="max-w-4xl mx-auto flex items-center justify-between mb-4">
              <button
                onClick={() => setActivePhase(1)}
                className="text-xs text-slate-400 hover:text-white flex items-center gap-1.5 transition-colors"
              >
                <ArrowLeft className="w-3.5 h-3.5" />
                <span>Xem lại câu trả lời Brief</span>
              </button>
            </div>
            <ProposalReviewCard
              proposal={session.proposal}
              loading={sessionLoading}
              onApprove={approveProposalAndBuild}
              onRevise={reviseProposal}
            />
          </div>
        )}

        {/* State 3: Phase 3 - Live Preview & UAT Acceptance */}
        {session && activePhase === 3 && (
          <div className="flex-1 flex flex-col h-full overflow-hidden bg-slate-950">
            <div className="flex-1 overflow-hidden">
              <LivePreview
                code={currentHtml}
                viewport={viewport}
                inspectMode={inspectMode}
                onSelectElement={(el) => setSelectedElement(el)}
                isGenerating={sessionLoading}
              />
            </div>
            <UATPanel
              build={session.build}
              uatHistory={session.uat_history || []}
              loading={sessionLoading}
              onSendFeedback={(fb) => submitUATFeedback(fb)}
              onDownload={handleDownload}
              onAcceptFinal={handleDownload}
              inspectMode={inspectMode}
              setInspectMode={setInspectMode}
            />
          </div>
        )}
      </div>

      {/* Targeted Element Edit Modal */}
      <InspectModal
        isOpen={Boolean(selectedElement)}
        onClose={() => setSelectedElement(null)}
        element={selectedElement}
        onSubmitTweak={handleTweakElement}
        isTweaking={isTweaking}
      />

      {/* Code Viewer / Export Modal */}
      <CodeModal
        isOpen={isCodeModalOpen}
        onClose={() => setIsCodeModalOpen(false)}
        code={currentHtml}
      />

      {/* Error Toast Notification */}
      {errorToast && (
        <div className="fixed bottom-6 right-6 z-50 bg-red-500/90 text-white text-xs px-4 py-3 rounded-xl shadow-2xl backdrop-blur-md border border-red-400/30 flex items-center gap-3 animate-in slide-in-from-bottom duration-300">
          <span>{errorToast}</span>
          <button
            onClick={() => setErrorToast(null)}
            className="text-white/80 hover:text-white font-bold ml-2"
          >
            ✕
          </button>
        </div>
      )}
    </div>
  );
}

export default App;
