import React from "react";
import { 
  Compass, 
  PenTool, 
  Palette, 
  Code2, 
  CheckCircle2, 
  Clock, 
  AlertTriangle,
  Loader2
} from "lucide-react";
import { AgentEvent } from "../services/api";

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
  // Find current agent status from events list
  const getAgentStatus = (agentKey: string) => {
    const matching = events.filter((e) => e.agent === agentKey);
    if (!matching.length) return { status: "idle", message: "Chờ thực hiện..." };
    const latest = matching[matching.length - 1];
    return {
      status: latest.status,
      message: latest.message,
      summary: latest.summary,
      passed: latest.passed
    };
  };

  const latestEvent = events.length ? events[events.length - 1] : null;

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
        {latestEvent && (
          <span className="text-[11px] text-slate-400 font-mono">
            {latestEvent.message}
          </span>
        )}
      </div>

      {/* Grid of 5 Agents */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-2.5">
        {AGENTS_CONFIG.map((agent) => {
          const { status, message, summary } = getAgentStatus(agent.key);
          const Icon = agent.icon;

          const isCompleted = status === "completed";
          const isStarted = status === "started" || status === "thinking";
          const isWarning = status === "warning" || status === "error";

          return (
            <div
              key={agent.key}
              className={`p-3 rounded-xl border transition-all duration-300 relative overflow-hidden ${
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
                <div className="font-semibold text-xs text-white">{agent.name}</div>
                <div className="text-[11px] text-slate-400 truncate">{agent.role}</div>
              </div>

              {summary && (
                <div className="mt-2 text-[10px] text-slate-400 line-clamp-2 bg-slate-900/50 p-1.5 rounded border border-slate-800">
                  {summary}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};
