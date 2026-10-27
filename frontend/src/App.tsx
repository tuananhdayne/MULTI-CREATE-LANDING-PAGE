import React, { useState, useEffect } from "react";
import { Header } from "./components/Header";
import { PromptInput } from "./components/PromptInput";
import { AgentTimeline } from "./components/AgentTimeline";
import { LivePreview } from "./components/LivePreview";
import { InspectModal } from "./components/InspectModal";
import { CodeModal } from "./components/CodeModal";
import { api } from "./services/api";
import type { ProjectData, AgentEvent, HealthStatus } from "./services/api";

export function App() {
  const [projectId] = useState<string>("landing-session-1");
  const [project, setProject] = useState<ProjectData | null>(null);
  const [events, setEvents] = useState<AgentEvent[]>([]);
  const [isGenerating, setIsGenerating] = useState<boolean>(false);
  const [viewport, setViewport] = useState<"desktop" | "tablet" | "mobile">("desktop");
  const [inspectMode, setInspectMode] = useState<boolean>(false);
  const [selectedElement, setSelectedElement] = useState<any | null>(null);
  const [isTweaking, setIsTweaking] = useState<boolean>(false);
  const [isCodeModalOpen, setIsCodeModalOpen] = useState<boolean>(false);
  const [health, setHealth] = useState<HealthStatus | null>(null);
  const [errorToast, setErrorToast] = useState<string | null>(null);

  // Load backend health and initial project on mount
  useEffect(() => {
    api.getHealth()
      .then((h) => setHealth(h))
      .catch((err) => console.warn("Backend not available yet:", err.message));

    api.getProject(projectId)
      .then((p) => {
        if (p && p.code) setProject(p);
      })
      .catch((err) => console.warn("No active project loaded:", err.message));
  }, [projectId]);

  // Handle multi-agent generation via SSE
  const handleGenerate = async (prompt: string, theme: string) => {
    setIsGenerating(true);
    setEvents([]);
    setErrorToast(null);

    await api.streamGenerate(
      prompt,
      theme,
      projectId,
      (event) => {
        setEvents((prev) => [...prev, event]);
      },
      (completedProject) => {
        setProject(completedProject);
        setIsGenerating(false);
      },
      (errorMsg) => {
        setErrorToast(errorMsg);
        setIsGenerating(false);
      }
    );
  };

  // Handle Undo
  const handleUndo = async () => {
    if (!project?.can_undo) return;
    try {
      const updated = await api.undo(projectId);
      setProject(updated);
    } catch (err: any) {
      setErrorToast("Không thể hoàn tác: " + err.message);
    }
  };

  // Handle Redo
  const handleRedo = async () => {
    if (!project?.can_redo) return;
    try {
      const updated = await api.redo(projectId);
      setProject(updated);
    } catch (err: any) {
      setErrorToast("Không thể làm lại: " + err.message);
    }
  };

  // Handle targeted element modification (Click-to-Inspect)
  const handleTweakElement = async (instruction: string) => {
    if (!selectedElement || !project) return;
    setIsTweaking(true);
    try {
      const updated = await api.tweakElement(projectId, {
        element_id: selectedElement.element_id,
        tag: selectedElement.tag,
        classes: selectedElement.classes,
        current_html: selectedElement.current_html,
        instruction,
        full_code: project.code,
      });
      setProject(updated);
      setSelectedElement(null);
      setInspectMode(false);
    } catch (err: any) {
      setErrorToast("Lỗi khi chỉnh sửa phần tử: " + err.message);
    } finally {
      setIsTweaking(false);
    }
  };

  // Download index.html
  const handleDownload = () => {
    if (!project?.code) return;
    const blob = new Blob([project.code], { type: "text/html;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "landing-page.html";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="flex flex-col h-screen w-screen bg-slate-950 text-slate-100 overflow-hidden font-sans">
      {/* Top Header */}
      <Header
        viewport={viewport}
        setViewport={setViewport}
        inspectMode={inspectMode}
        setInspectMode={setInspectMode}
        canUndo={Boolean(project?.can_undo)}
        canRedo={Boolean(project?.can_redo)}
        version={project?.version || 0}
        onUndo={handleUndo}
        onRedo={handleRedo}
        onOpenCode={() => setIsCodeModalOpen(true)}
        onDownload={handleDownload}
        modelName={health?.model || "ag/gemini-3.7-flash"}
        hasCode={Boolean(project?.code)}
      />

      {/* Main Workspace Layout */}
      <div className="flex-1 flex flex-col md:flex-row overflow-hidden relative">
        {/* Left Control Panel: Prompt & Timeline */}
        <aside className="w-full md:w-[420px] lg:w-[460px] p-4 flex flex-col gap-4 overflow-y-auto border-r border-slate-800/80 bg-slate-900/30 shrink-0">
          <PromptInput onGenerate={handleGenerate} isGenerating={isGenerating} />
          <AgentTimeline events={events} isGenerating={isGenerating} />
        </aside>

        {/* Right Preview Panel: Live Iframe with Responsive Frame */}
        <main className="flex-1 h-full overflow-hidden flex flex-col bg-slate-950">
          <LivePreview
            code={project?.code || ""}
            viewport={viewport}
            inspectMode={inspectMode}
            onSelectElement={(el) => setSelectedElement(el)}
            isGenerating={isGenerating}
          />
        </main>
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
        code={project?.code || ""}
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
