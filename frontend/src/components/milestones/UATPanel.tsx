import React, { useState } from 'react';
import type { BuildArtifact, UATFeedbackItem } from '../../types/project';
import { 
  CheckCircle, 
  ShieldCheck, 
  Send, 
  Download, 
  History, 
  MousePointerClick, 
  Sparkles,
  ChevronDown,
  ChevronUp
} from 'lucide-react';

interface UATPanelProps {
  build?: BuildArtifact;
  uatHistory: UATFeedbackItem[];
  loading: boolean;
  onSendFeedback: (feedback: string) => void;
  onDownload: () => void;
  onAcceptFinal: () => void;
  inspectMode: boolean;
  setInspectMode: (val: boolean) => void;
}

export const UATPanel: React.FC<UATPanelProps> = ({
  build,
  uatHistory,
  loading,
  onSendFeedback,
  onDownload,
  onAcceptFinal,
  inspectMode,
  setInspectMode,
}) => {
  const [feedbackInput, setFeedbackInput] = useState<string>('');
  const [isCollapsed, setIsCollapsed] = useState<boolean>(false);

  const handleSend = (e: React.FormEvent) => {
    e.preventDefault();
    if (!feedbackInput.trim()) return;
    onSendFeedback(feedbackInput.trim());
    setFeedbackInput('');
  };

  return (
    <div className="border-t border-slate-800 bg-slate-900/95 backdrop-blur-xl shadow-2xl z-20 transition-all">
      {/* Bar Header */}
      <div className="px-4 py-3 flex items-center justify-between border-b border-slate-800/80">
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse" />
            <h3 className="text-xs font-bold uppercase tracking-wider text-white flex items-center gap-1.5">
              <span>Chặng 3: Bảng Nghiệm Thu & Tinh Chỉnh (UAT Board)</span>
            </h3>
          </div>

          <div className="hidden sm:flex items-center gap-1.5 bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 px-2.5 py-0.5 rounded-full text-[11px] font-medium">
            <ShieldCheck className="w-3.5 h-3.5" />
            <span>Visual QA Validated</span>
          </div>
        </div>

        <div className="flex items-center gap-2">
          {/* Click to inspect toggle helper */}
          <button
            type="button"
            onClick={() => setInspectMode(!inspectMode)}
            className={`flex items-center gap-1 px-3 py-1.5 rounded-lg text-xs font-medium border transition-all ${
              inspectMode
                ? 'bg-amber-500/20 border-amber-500/40 text-amber-300'
                : 'bg-slate-800/60 border-slate-700 text-slate-300 hover:text-white'
            }`}
          >
            <MousePointerClick className="w-3.5 h-3.5 text-amber-400" />
            <span className="hidden md:inline">{inspectMode ? 'Đang chọn phần tử...' : 'Sửa theo phần tử'}</span>
          </button>

          {/* Accept / Download */}
          <button
            type="button"
            onClick={onAcceptFinal}
            className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg text-xs font-semibold bg-gradient-to-r from-emerald-600 to-teal-500 hover:from-emerald-500 hover:to-teal-400 text-white shadow-md shadow-emerald-600/20 active:scale-95 transition-all"
          >
            <CheckCircle className="w-3.5 h-3.5" />
            <span>Ký Duyệt Nghiệm Thu</span>
          </button>

          <button
            type="button"
            onClick={() => setIsCollapsed(!isCollapsed)}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800"
          >
            {isCollapsed ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
          </button>
        </div>
      </div>

      {/* Expandable Feedback Area */}
      {!isCollapsed && (
        <div className="p-4 grid grid-cols-1 lg:grid-cols-3 gap-4">
          {/* Left: Input feedback */}
          <div className="lg:col-span-2 space-y-2">
            <form onSubmit={handleSend} className="flex gap-2">
              <input
                type="text"
                value={feedbackInput}
                onChange={(e) => setFeedbackInput(e.target.value)}
                placeholder="Góp ý sửa đổi toàn trang (Ví dụ: Cho tiêu đề to hơn, thêm hiệu ứng bóng đổ cho nút CTA)..."
                className="flex-1 bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500"
              />
              <button
                type="submit"
                disabled={loading || !feedbackInput.trim()}
                className="px-5 py-2.5 rounded-xl text-xs font-semibold text-white bg-indigo-600 hover:bg-indigo-500 active:scale-95 disabled:opacity-50 transition-all flex items-center gap-1.5 shrink-0"
              >
                <Send className="w-3.5 h-3.5" />
                <span>{loading ? 'Đang tinh chỉnh...' : 'Áp Dụng'}</span>
              </button>
            </form>
            <p className="text-[11px] text-slate-500 flex items-center gap-1">
              <Sparkles className="w-3 h-3 text-amber-400 inline" />
              <span>Mẹo: Bạn cũng có thể click trực tiếp vào nút hoặc khối trên trang để sửa nhanh một phần tử.</span>
            </p>
          </div>

          {/* Right: History log */}
          <div className="bg-slate-950/60 rounded-xl border border-slate-800/80 p-3 max-h-24 overflow-y-auto">
            <div className="flex items-center gap-1.5 text-[11px] font-semibold text-slate-400 mb-1.5">
              <History className="w-3 h-3 text-slate-500" />
              <span>Lịch sử nghiệm thu ({uatHistory.length} lượt tinh chỉnh)</span>
            </div>
            {uatHistory.length === 0 ? (
              <p className="text-[10px] text-slate-600 italic">Chưa có lượt góp ý nào. Trang web đang ở bản dựng ban đầu.</p>
            ) : (
              <div className="space-y-1">
                {uatHistory.map((item, idx) => (
                  <div key={idx} className="text-[11px] text-slate-300 flex items-start gap-1.5 truncate">
                    <span className="text-emerald-400 font-mono">#{idx + 1}</span>
                    <span className="truncate">{item.feedback}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
