import React, { useState } from "react";
import { 
  Compass, 
  PenTool, 
  Palette, 
  Code2, 
  CheckCircle2, 
  Clock, 
  AlertTriangle,
  Loader2,
  X,
  Copy,
  Check,
  MessagesSquare,
  ChevronRight
} from "lucide-react";
import type { AgentEvent } from "../services/api";

interface AgentTimelineProps {
  events: AgentEvent[];
  isGenerating: boolean;
}

const AGENTS_CONFIG = [
  { key: "strategist", name: "Strategist", role: "Chiến lược CRO", icon: Compass, color: "text-blue-400 bg-blue-500/10 border-blue-500/20" },
  { key: "copywriter", name: "Copywriter", role: "Soạn nội dung", icon: PenTool, color: "text-purple-400 bg-purple-500/10 border-purple-500/20" },
  { key: "designer", name: "UI Designer", role: "Design System", icon: Palette, color: "text-pink-400 bg-pink-500/10 border-pink-500/20" },
  { key: "coder", name: "Frontend Coder", role: "Lập trình HTML5", icon: Code2, color: "text-amber-400 bg-amber-500/10 border-amber-500/20" },
  { key: "qa", name: "Visual QA", role: "Kiểm thử CDP", icon: CheckCircle2, color: "text-emerald-400 bg-emerald-500/10 border-emerald-500/20" },
];

export const AgentTimeline: React.FC<AgentTimelineProps> = ({ events, isGenerating }) => {
  const [selectedAgentKey, setSelectedAgentKey] = useState<string | null>(null);
  const [showFullLogs, setShowFullLogs] = useState<boolean>(false);
  const [copied, setCopied] = useState<boolean>(false);

  // Find agent status and output
  const getAgentData = (agentKey: string) => {
    const matching = events.filter((e) => e.agent === agentKey);
    if (!matching.length) {
      return { 
        status: "idle", 
        message: "Chờ đến lượt...", 
        summary: null, 
        full_content: null 
      };
    }
    const latest = matching[matching.length - 1];
    return {
      status: latest.status,
      message: latest.message,
      summary: latest.summary,
      full_content: latest.full_content || latest.summary || latest.message,
      passed: latest.passed
    };
  };

  const latestEvent = events.length ? events[events.length - 1] : null;

  // Selected agent for modal
  const selectedConfig = AGENTS_CONFIG.find((a) => a.key === selectedAgentKey);
  const selectedData = selectedAgentKey ? getAgentData(selectedAgentKey) : null;

  const handleCopy = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-4 shadow-xl backdrop-blur-md">
      <div className="flex items-center justify-between mb-3">
        <h2 className="text-xs font-semibold uppercase tracking-wider text-slate-400 flex items-center gap-2">
          <span>Tiến độ đội ngũ 5 Agents</span>
          {isGenerating && (
            <span className="flex h-2 w-2 relative">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
            </span>
          )}
        </h2>

        {/* View all dialogues button */}
        {events.length > 0 && (
          <button
            onClick={() => setShowFullLogs(true)}
            className="text-[11px] font-medium text-indigo-400 hover:text-indigo-300 flex items-center gap-1 px-2 py-0.5 rounded-lg bg-indigo-500/10 hover:bg-indigo-500/20 border border-indigo-500/20 transition-all"
          >
            <MessagesSquare className="w-3.5 h-3.5" />
            <span>Xem nhật ký</span>
          </button>
        )}
      </div>

      {latestEvent && (
        <div className="mb-3 text-[11px] text-slate-300 bg-slate-950/60 px-3 py-1.5 rounded-xl border border-slate-800/80 flex items-center justify-between">
          <span className="truncate mr-2 font-mono">{latestEvent.message}</span>
          <span className="text-[10px] text-indigo-400 whitespace-nowrap">Bấm vào từng Agent để xem ➔</span>
        </div>
      )}

      {/* Grid of 5 Agents */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-2.5">
        {AGENTS_CONFIG.map((agent) => {
          const { status, summary, full_content } = getAgentData(agent.key);
          const Icon = agent.icon;

          const isCompleted = status === "completed";
          const isStarted = status === "started" || status === "thinking";
          const isWarning = status === "warning" || status === "error";
          const hasContent = Boolean(full_content || summary);

          return (
            <div
              key={agent.key}
              onClick={() => hasContent && setSelectedAgentKey(agent.key)}
              className={`p-3 rounded-xl border transition-all duration-300 relative overflow-hidden ${
                hasContent ? "cursor-pointer hover:border-indigo-400/80 hover:shadow-lg hover:shadow-indigo-500/10 active:scale-[0.98]" : ""
              } ${
                isStarted
                  ? "bg-slate-900 border-indigo-500/60 shadow-lg shadow-indigo-500/10 ring-1 ring-indigo-500/30"
                  : isCompleted
                  ? "bg-slate-950/60 border-slate-800/80"
                  : "bg-slate-950/30 border-slate-900 opacity-60"
              }`}
            >
              {isStarted && (
                <div className="absolute top-0 left-0 right-0 h-0.5 bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 animate-pulse" />
              )}

              <div className="flex items-center justify-between mb-1.5">
                <div className={`w-7 h-7 rounded-lg flex items-center justify-center border ${agent.color}`}>
                  <Icon className="w-3.5 h-3.5" />
                </div>
                <div>
                  {isStarted && <Loader2 className="w-3.5 h-3.5 text-indigo-400 animate-spin" />}
                  {isCompleted && <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />}
                  {isWarning && <AlertTriangle className="w-3.5 h-3.5 text-amber-400" />}
                  {!isStarted && !isCompleted && !isWarning && <Clock className="w-3.5 h-3.5 text-slate-600" />}
                </div>
              </div>

              <div className="space-y-0.5">
                <div className="font-semibold text-xs text-white flex items-center justify-between">
                  <span>{agent.name}</span>
                  {hasContent && <ChevronRight className="w-3 h-3 text-slate-500" />}
                </div>
                <div className="text-[11px] text-slate-400 truncate">{agent.role}</div>
              </div>

              {summary && (
                <div className="mt-2 text-[10px] text-slate-300 line-clamp-2 bg-slate-900/60 p-1.5 rounded border border-slate-800/80">
                  {summary}
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* MODAL 1: Single Agent Deliverables Detail */}
      {selectedConfig && selectedData && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-in fade-in duration-200">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-2xl max-h-[80vh] flex flex-col shadow-2xl overflow-hidden">
            <div className="px-5 py-4 border-b border-slate-800 flex items-center justify-between bg-slate-950/60">
              <div className="flex items-center gap-2.5">
                <div className={`w-8 h-8 rounded-lg flex items-center justify-center border ${selectedConfig.color}`}>
                  <selectedConfig.icon className="w-4 h-4" />
                </div>
                <div>
                  <h3 className="text-sm font-bold text-white flex items-center gap-2">
                    <span>{selectedConfig.name}</span>
                    <span className="text-xs font-normal text-slate-400">({selectedConfig.role})</span>
                  </h3>
                  <p className="text-[11px] text-emerald-400 flex items-center gap-1 font-mono">
                    <CheckCircle2 className="w-3 h-3" /> {selectedData.message}
                  </p>
                </div>
              </div>

              <div className="flex items-center gap-2">
                {selectedData.full_content && (
                  <button
                    onClick={() => handleCopy(selectedData.full_content!)}
                    className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition-all"
                  >
                    {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                    <span>{copied ? "Đã chép" : "Sao chép"}</span>
                  </button>
                )}
                <button
                  onClick={() => setSelectedAgentKey(null)}
                  className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-all"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>
            </div>

            <div className="flex-1 overflow-y-auto p-5 text-xs text-slate-200 leading-relaxed font-sans space-y-3 bg-slate-950/40">
              <div className="text-[11px] text-slate-400 font-semibold uppercase tracking-wider mb-1">
                Nội dung bàn giao / Trao đổi chi tiết:
              </div>
              <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800 font-mono text-[11px] whitespace-pre-wrap leading-relaxed text-slate-200">
                {selectedData.full_content || "Chưa có nội dung"}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* MODAL 2: Full Unified Conversation Log of all Agents */}
      {showFullLogs && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-in fade-in duration-200">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-3xl max-h-[85vh] flex flex-col shadow-2xl overflow-hidden">
            <div className="px-6 py-4 border-b border-slate-800 flex items-center justify-between bg-slate-950/60">
              <div className="flex items-center gap-2">
                <MessagesSquare className="w-5 h-5 text-indigo-400" />
                <h3 className="text-sm font-bold text-white">Toàn bộ Nhật ký Trao đổi của 5 Agents</h3>
              </div>
              <button
                onClick={() => setShowFullLogs(false)}
                className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-all"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="flex-1 overflow-y-auto p-6 space-y-4 bg-slate-950/40">
              {events.map((evt, idx) => {
                const conf = AGENTS_CONFIG.find((a) => a.key === evt.agent);
                const Icon = conf?.icon || Compass;
                return (
                  <div key={idx} className="p-4 rounded-xl bg-slate-900/80 border border-slate-800/80 space-y-2">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <div className={`w-6 h-6 rounded-md flex items-center justify-center border ${conf?.color || "text-slate-400"}`}>
                          <Icon className="w-3.5 h-3.5" />
                        </div>
                        <span className="font-bold text-xs text-white capitalize">{conf?.name || evt.agent}</span>
                        <span className="text-[11px] text-slate-400">({conf?.role})</span>
                      </div>
                      <span className={`text-[10px] px-2 py-0.5 rounded-full font-medium ${
                        evt.status === "completed" ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20" :
                        evt.status === "started" ? "bg-indigo-500/10 text-indigo-400 border border-indigo-500/20" :
                        "bg-amber-500/10 text-amber-400 border border-amber-500/20"
                      }`}>
                        {evt.status}
                      </span>
                    </div>

                    <p className="text-xs text-slate-300 font-medium">{evt.message}</p>

                    {(evt.full_content || evt.summary) && (
                      <div className="bg-slate-950 p-3 rounded-lg border border-slate-800 text-[11px] font-mono text-slate-300 whitespace-pre-wrap max-h-48 overflow-y-auto">
                        {evt.full_content || evt.summary}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
