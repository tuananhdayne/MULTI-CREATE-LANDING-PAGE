import React, { useState } from "react";
import { Sparkles, ArrowRight, Loader2, Palette } from "lucide-react";

interface PromptInputProps {
  onGenerate: (prompt: string, theme: string) => void;
  isGenerating: boolean;
}

const TEMPLATES = [
  {
    title: "🚀 SaaS AI Assistant",
    prompt: "Tạo landing page cho phần mềm SaaS AI Meeting Assistant tự động ghi chép và tóm tắt cuộc họp, phong cách Dark Mode cao cấp, glassmorphism, bảng giá 3 gói và nút dùng thử 14 ngày.",
    theme: "dark"
  },
  {
    title: "🎓 Khóa Học Fullstack",
    prompt: "Landing page bán khóa học Lập trình Web Fullstack hiện đại từ số 0, đếm ngược ưu đãi giảm 40%, lộ trình 4 module, cam kết hoàn tiền và các review học viên xuất sắc.",
    theme: "light"
  },
  {
    title: "💼 B2B Growth Agency",
    prompt: "Landing page dịch vụ Digital Marketing & Growth Hacking B2B, biểu đồ tăng trưởng doanh thu 300%, logo 20+ đối tác lớn, form đặt lịch tư vấn chiến lược miễn phí.",
    theme: "dark"
  },
  {
    title: "💳 Ứng Dụng Fintech",
    prompt: "Landing page cho ứng dụng quản lý tài chính thông minh và đầu tư vi mô, giao diện bảo mật chuẩn ngân hàng, thẻ bài học chi tiêu, nút tải app trên App Store & Google Play.",
    theme: "auto"
  }
];

export const PromptInput: React.FC<PromptInputProps> = ({ onGenerate, isGenerating }) => {
  const [prompt, setPrompt] = useState("");
  const [theme, setTheme] = useState("auto");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!prompt.trim() || isGenerating) return;
    onGenerate(prompt.trim(), theme);
  };

  const applyTemplate = (templatePrompt: string, templateTheme: string) => {
    setPrompt(templatePrompt);
    setTheme(templateTheme);
  };

  return (
    <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-4 shadow-xl backdrop-blur-md">
      <form onSubmit={handleSubmit} className="space-y-3">
        <div className="relative">
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            disabled={isGenerating}
            placeholder="Mô tả Landing Page bạn muốn tạo (ví dụ: Landing page cho phần mềm SaaS AI, ứng dụng tài chính, khóa học online...)"
            rows={3}
            className="w-full bg-slate-950/80 border border-slate-700/80 rounded-xl px-4 py-3 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 transition-all resize-none"
          />
        </div>

        <div className="flex flex-wrap items-center justify-between gap-3">
          {/* Theme selector */}
          <div className="flex items-center gap-2">
            <span className="text-xs text-slate-400 flex items-center gap-1">
              <Palette className="w-3.5 h-3.5 text-indigo-400" />
              Theme:
            </span>
            <div className="flex items-center gap-1 bg-slate-950/60 p-1 rounded-lg border border-slate-800 text-xs">
              {(["auto", "dark", "light"] as const).map((t) => (
                <button
                  key={t}
                  type="button"
                  onClick={() => setTheme(t)}
                  className={`px-2.5 py-1 rounded capitalize transition-all ${
                    theme === t
                      ? "bg-indigo-600 text-white font-medium shadow-sm"
                      : "text-slate-400 hover:text-slate-200"
                  }`}
                >
                  {t}
                </button>
              ))}
            </div>
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            disabled={!prompt.trim() || isGenerating}
            className={`flex items-center gap-2 px-5 py-2.5 rounded-xl text-xs font-semibold shadow-lg transition-all ${
              prompt.trim() && !isGenerating
                ? "bg-gradient-to-r from-indigo-600 via-indigo-500 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white shadow-indigo-500/25 active:scale-95 cursor-pointer"
                : "bg-slate-800 text-slate-500 cursor-not-allowed"
            }`}
          >
            {isGenerating ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                <span>Đội ngũ Agent đang tạo...</span>
              </>
            ) : (
              <>
                <Sparkles className="w-4 h-4" />
                <span>Tạo Landing Page</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </>
            )}
          </button>
        </div>
      </form>

      {/* Suggested Templates */}
      <div className="mt-3 pt-3 border-t border-slate-800/60 flex flex-wrap items-center gap-2">
        <span className="text-[11px] text-slate-500 font-medium">Gợi ý mẫu:</span>
        {TEMPLATES.map((tpl, i) => (
          <button
            key={i}
            type="button"
            onClick={() => applyTemplate(tpl.prompt, tpl.theme)}
            disabled={isGenerating}
            className="text-[11px] px-2.5 py-1 rounded-lg bg-slate-800/40 hover:bg-slate-800 hover:text-indigo-300 text-slate-300 border border-slate-700/50 transition-all"
          >
            {tpl.title}
          </button>
        ))}
      </div>
    </div>
  );
};
