import React, { useState } from "react";
import { X, Sparkles, Loader2, MousePointerClick, Sliders } from "lucide-react";

interface SelectedElementData {
  element_id?: string;
  tag: string;
  classes: string;
  current_html: string;
}

interface InspectModalProps {
  isOpen: boolean;
  onClose: () => void;
  element: SelectedElementData | null;
  onSubmitTweak: (instruction: string) => Promise<void>;
  isTweaking: boolean;
}

const QUICK_TWEAKS = [
  "Đổi màu thành gradient cam - hổ phách nổi bật",
  "Tăng bo góc tròn (rounded-full) và thêm bóng đổ shadow-xl",
  "Thêm hiệu ứng hover phóng to (hover:scale-105) và chuyển động mượt mà",
  "Đổi font chữ đậm hơn và tăng cỡ chữ lên text-xl",
  "Đổi nội dung text thành 'Khám Phá Ngay Hôm Nay'"
];

export const InspectModal: React.FC<InspectModalProps> = ({
  isOpen,
  onClose,
  element,
  onSubmitTweak,
  isTweaking,
}) => {
  const [instruction, setInstruction] = useState("");

  if (!isOpen || !element) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!instruction.trim() || isTweaking) return;
    await onSubmitTweak(instruction.trim());
    setInstruction("");
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-lg shadow-2xl overflow-hidden flex flex-col">
        {/* Header */}
        <div className="px-5 py-4 border-b border-slate-800 flex items-center justify-between bg-slate-950/50">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400">
              <MousePointerClick className="w-4 h-4" />
            </div>
            <div>
              <h3 className="text-sm font-bold text-white flex items-center gap-2">
                <span>Tinh chỉnh phần tử</span>
                <span className="font-mono text-xs px-2 py-0.5 rounded bg-indigo-600/20 text-indigo-300 border border-indigo-500/30">
                  &lt;{element.tag}{element.element_id ? ` id="${element.element_id}"` : ""}&gt;
                </span>
              </h3>
              <p className="text-[11px] text-slate-400">Ra lệnh cho AI sửa đổi đúng phần tử này mà không ảnh hưởng phần khác</p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-all"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Body Form */}
        <form onSubmit={handleSubmit} className="p-5 space-y-4">
          {/* Current Element Preview */}
          <div className="bg-slate-950/80 p-3 rounded-xl border border-slate-800 text-[11px] font-mono text-slate-300 max-h-24 overflow-auto">
            <span className="text-slate-500 block mb-1">Mã HTML hiện tại:</span>
            <pre className="whitespace-pre-wrap break-all">{element.current_html.slice(0, 300)}{element.current_html.length > 300 ? "..." : ""}</pre>
          </div>

          {/* Quick suggestions */}
          <div>
            <span className="text-[11px] text-slate-400 font-medium flex items-center gap-1 mb-2">
              <Sliders className="w-3 h-3 text-indigo-400" />
              Gợi ý nhanh:
            </span>
            <div className="flex flex-wrap gap-1.5">
              {QUICK_TWEAKS.map((tweak, i) => (
                <button
                  key={i}
                  type="button"
                  onClick={() => setInstruction(tweak)}
                  className="text-[11px] text-left px-2.5 py-1 rounded-lg bg-slate-800/60 hover:bg-indigo-600/20 hover:text-indigo-300 text-slate-300 border border-slate-700/60 transition-all"
                >
                  {tweak}
                </button>
              ))}
            </div>
          </div>

          {/* Prompt instruction textarea */}
          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1.5">
              Yêu cầu chỉnh sửa cụ thể:
            </label>
            <textarea
              value={instruction}
              onChange={(e) => setInstruction(e.target.value)}
              placeholder="Ví dụ: Đổi màu nút sang gradient tím - hồng, thêm icon ngôi sao, đổi chữ thành Đăng Ký Miễn Phí..."
              rows={3}
              className="w-full bg-slate-950 border border-slate-700/80 rounded-xl px-3.5 py-2.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 transition-all resize-none"
            />
          </div>

          {/* Actions */}
          <div className="flex items-center justify-end gap-2 pt-2 border-t border-slate-800">
            <button
              type="button"
              onClick={onClose}
              disabled={isTweaking}
              className="px-4 py-2 rounded-xl text-xs font-medium text-slate-400 hover:text-white hover:bg-slate-800 transition-all"
            >
              Hủy
            </button>

            <button
              type="submit"
              disabled={!instruction.trim() || isTweaking}
              className={`flex items-center gap-2 px-5 py-2 rounded-xl text-xs font-semibold shadow-lg transition-all ${
                instruction.trim() && !isTweaking
                  ? "bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white shadow-indigo-500/20 active:scale-95 cursor-pointer"
                  : "bg-slate-800 text-slate-500 cursor-not-allowed"
              }`}
            >
              {isTweaking ? (
                <>
                  <Loader2 className="w-3.5 h-3.5 animate-spin" />
                  <span>Đang sửa...</span>
                </>
              ) : (
                <>
                  <Sparkles className="w-3.5 h-3.5" />
                  <span>Áp dụng chỉnh sửa</span>
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
