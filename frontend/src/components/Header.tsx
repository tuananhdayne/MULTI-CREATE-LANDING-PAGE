import React from "react";
import { 
  Monitor, 
  Tablet, 
  Smartphone, 
  Undo2, 
  Redo2, 
  Download, 
  Code2, 
  MousePointerClick,
  Sparkles,
  Zap
} from "lucide-react";

interface HeaderProps {
  viewport: "desktop" | "tablet" | "mobile";
  setViewport: (v: "desktop" | "tablet" | "mobile") => void;
  inspectMode: boolean;
  setInspectMode: (val: boolean) => void;
  canUndo: boolean;
  canRedo: boolean;
  version: number;
  onUndo: () => void;
  onRedo: () => void;
  onOpenCode: () => void;
  onDownload: () => void;
  modelName: string;
  hasCode: boolean;
}

export const Header: React.FC<HeaderProps> = ({
  viewport,
  setViewport,
  inspectMode,
  setInspectMode,
  canUndo,
  canRedo,
  version,
  onUndo,
  onRedo,
  onOpenCode,
  onDownload,
  modelName,
  hasCode,
}) => {
  return (
    <header className="h-16 border-b border-slate-800 bg-slate-900/80 backdrop-blur-md px-4 flex items-center justify-between z-30 sticky top-0">
      {/* Brand logo & model badge */}
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 via-indigo-500 to-emerald-400 flex items-center justify-center shadow-lg shadow-indigo-500/20">
          <Sparkles className="w-5 h-5 text-white" />
        </div>
        <div>
          <div className="flex items-center gap-2">
            <h1 className="font-bold text-base tracking-tight text-white flex items-center gap-1.5">
              LandingCraft <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">Multi-Agent</span>
            </h1>
          </div>
          <p className="text-xs text-slate-400 flex items-center gap-1">
            <Zap className="w-3 h-3 text-amber-400 inline" />
            <span className="truncate max-w-[160px] font-mono text-[11px] text-slate-300" title={modelName}>
              {modelName || "ag/gemini-3.7-flash"}
            </span>
            {version > 0 && (
              <span className="text-[10px] px-1.5 py-0.2 rounded bg-slate-800 text-slate-300 border border-slate-700">
                v{version}
              </span>
            )}
          </p>
        </div>
      </div>

      {/* Middle: Viewport switchers & DevTools inspect mode */}
      <div className="flex items-center gap-2">
        {/* Viewport switchers */}
        <div className="bg-slate-950/60 p-1 rounded-xl border border-slate-800 flex items-center gap-1">
          <button
            onClick={() => setViewport("desktop")}
            className={`p-2 rounded-lg text-xs font-medium transition-all flex items-center gap-1.5 ${
              viewport === "desktop"
                ? "bg-indigo-600 text-white shadow-md shadow-indigo-600/30"
                : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/60"
            }`}
            title="Desktop View (100%)"
          >
            <Monitor className="w-4 h-4" />
            <span className="hidden md:inline">Desktop</span>
          </button>
          <button
            onClick={() => setViewport("tablet")}
            className={`p-2 rounded-lg text-xs font-medium transition-all flex items-center gap-1.5 ${
              viewport === "tablet"
                ? "bg-indigo-600 text-white shadow-md shadow-indigo-600/30"
                : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/60"
            }`}
            title="Tablet View (768px)"
          >
            <Tablet className="w-4 h-4" />
            <span className="hidden md:inline">Tablet</span>
          </button>
          <button
            onClick={() => setViewport("mobile")}
            className={`p-2 rounded-lg text-xs font-medium transition-all flex items-center gap-1.5 ${
              viewport === "mobile"
                ? "bg-indigo-600 text-white shadow-md shadow-indigo-600/30"
                : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/60"
            }`}
            title="Mobile View (375px)"
          >
            <Smartphone className="w-4 h-4" />
            <span className="hidden md:inline">Mobile</span>
          </button>
        </div>

        {/* Chrome DevTools Click-to-Inspect Toggle */}
        <button
          onClick={() => setInspectMode(!inspectMode)}
          disabled={!hasCode}
          className={`flex items-center gap-1.5 px-3 py-2 rounded-xl text-xs font-medium transition-all border ${
            inspectMode
              ? "bg-amber-500/10 border-amber-500/40 text-amber-400 shadow-lg shadow-amber-500/10 animate-pulse"
              : "bg-slate-800/50 border-slate-700 text-slate-300 hover:bg-slate-800 hover:text-white"
          } ${!hasCode ? "opacity-50 cursor-not-allowed" : "cursor-pointer"}`}
          title="Bật/Tắt chế độ Click-to-Inspect để chọn và sửa phần tử trực quan"
        >
          <MousePointerClick className="w-4 h-4" />
          <span className="hidden sm:inline">{inspectMode ? "Đang Inspect..." : "Click-to-Inspect"}</span>
        </button>
      </div>

      {/* Right: Undo / Redo & Actions */}
      <div className="flex items-center gap-2">
        <div className="flex items-center gap-1 bg-slate-950/60 p-1 rounded-xl border border-slate-800">
          <button
            onClick={onUndo}
            disabled={!canUndo}
            className={`p-2 rounded-lg transition-all ${
              canUndo
                ? "text-slate-200 hover:bg-slate-800 hover:text-white"
                : "text-slate-600 cursor-not-allowed"
            }`}
            title="Hoàn tác (Undo)"
          >
            <Undo2 className="w-4 h-4" />
          </button>
          <button
            onClick={onRedo}
            disabled={!canRedo}
            className={`p-2 rounded-lg transition-all ${
              canRedo
                ? "text-slate-200 hover:bg-slate-800 hover:text-white"
                : "text-slate-600 cursor-not-allowed"
            }`}
            title="Làm lại (Redo)"
          >
            <Redo2 className="w-4 h-4" />
          </button>
        </div>

        {/* View Code */}
        <button
          onClick={onOpenCode}
          disabled={!hasCode}
          className={`p-2.5 rounded-xl border border-slate-800 bg-slate-950/60 transition-all ${
            hasCode
              ? "text-slate-300 hover:text-white hover:bg-slate-800"
              : "text-slate-600 cursor-not-allowed"
          }`}
          title="Xem / Sao chép mã nguồn HTML"
        >
          <Code2 className="w-4 h-4" />
        </button>

        {/* Export HTML */}
        <button
          onClick={onDownload}
          disabled={!hasCode}
          className={`flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-semibold shadow-lg transition-all ${
            hasCode
              ? "bg-gradient-to-r from-emerald-600 to-teal-500 hover:from-emerald-500 hover:to-teal-400 text-white shadow-emerald-600/20 active:scale-95"
              : "bg-slate-800 text-slate-500 cursor-not-allowed"
          }`}
          title="Tải về file index.html độc lập"
        >
          <Download className="w-4 h-4" />
          <span className="hidden sm:inline">Tải HTML</span>
        </button>
      </div>
    </header>
  );
};
