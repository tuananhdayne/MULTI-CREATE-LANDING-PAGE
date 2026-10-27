import React, { useState } from 'react';
import type { BriefQuestion } from '../../types/project';
import { HelpCircle, CheckCircle2, Sparkles, Zap, ArrowRight, MessageSquareText } from 'lucide-react';

interface BriefSurveyCardProps {
  prompt: string;
  questions: BriefQuestion[];
  loading: boolean;
  onSubmit: (answers: Record<string, string>) => void;
  onAutoPilot: () => void;
}

export const BriefSurveyCard: React.FC<BriefSurveyCardProps> = ({
  prompt,
  questions,
  loading,
  onSubmit,
  onAutoPilot,
}) => {
  const [answers, setAnswers] = useState<Record<string, string>>(() => {
    const initial: Record<string, string> = {};
    questions.forEach((q) => {
      // Pick first suggestion as friendly default if available
      if (q.quick_options && q.quick_options.length > 0) {
        initial[q.id] = q.quick_options[0];
      }
    });
    return initial;
  });

  const handleSelectOption = (questionId: string, option: string) => {
    setAnswers((prev) => ({ ...prev, [questionId]: option }));
  };

  const handleCustomInput = (questionId: string, val: string) => {
    setAnswers((prev) => ({ ...prev, [questionId]: val }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(answers);
  };

  return (
    <div className="max-w-4xl mx-auto my-8 px-4 animate-fade-in">
      {/* Brief Header */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 mb-6 shadow-2xl backdrop-blur-xl">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-800">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-2xl bg-indigo-500/10 border border-indigo-500/30 flex items-center justify-center text-indigo-400">
              <MessageSquareText className="w-6 h-6" />
            </div>
            <div>
              <span className="text-xs uppercase tracking-wider font-semibold text-indigo-400 bg-indigo-500/10 px-2.5 py-0.5 rounded-full border border-indigo-500/20">
                Chặng 1: Khảo sát & Chốt Brief (BA Analyst)
              </span>
              <h2 className="text-xl font-bold text-white mt-1">Làm Rõ Mục Tiêu & Yêu Cầu Thương Hiệu</h2>
            </div>
          </div>
          <button
            type="button"
            onClick={onAutoPilot}
            disabled={loading}
            className="flex items-center gap-2 px-4 py-2.5 rounded-xl text-xs font-semibold bg-amber-500/10 hover:bg-amber-500/20 text-amber-300 border border-amber-500/30 transition-all shadow-lg shadow-amber-500/10 self-start md:self-auto"
            title="Bỏ qua phỏng vấn và tự động sinh trang ngay lập tức"
          >
            <Zap className="w-4 h-4 text-amber-400" />
            <span>Tạo nhanh (Auto-pilot 1-Click)</span>
          </button>
        </div>

        <div className="mt-4 bg-slate-950/60 rounded-xl p-3.5 border border-slate-800/80 flex items-start gap-2.5 text-xs text-slate-300">
          <Sparkles className="w-4 h-4 text-indigo-400 shrink-0 mt-0.5" />
          <div>
            <span className="font-semibold text-slate-200">Đề bài dự án: </span>
            <span className="text-slate-400 italic">"{prompt}"</span>
          </div>
        </div>
      </div>

      {/* Survey Questions Form */}
      <form onSubmit={handleSubmit} className="space-y-6">
        {questions.map((q, idx) => {
          const currentAnswer = answers[q.id] || '';
          return (
            <div
              key={q.id}
              className="bg-slate-900/80 border border-slate-800/90 rounded-2xl p-6 shadow-xl backdrop-blur-md transition-all hover:border-slate-700"
            >
              <div className="flex items-center gap-2 mb-3">
                <span className="w-6 h-6 rounded-full bg-indigo-600/30 text-indigo-300 text-xs font-bold flex items-center justify-center border border-indigo-500/30">
                  {idx + 1}
                </span>
                <label className="text-sm font-semibold text-white flex items-center gap-2">
                  {q.question}
                  {q.required && <span className="text-rose-400 text-xs">*</span>}
                </label>
              </div>

              {/* Quick option pills */}
              {q.quick_options && q.quick_options.length > 0 && (
                <div className="flex flex-wrap gap-2 mb-4">
                  {q.quick_options.map((opt) => {
                    const isSelected = currentAnswer === opt;
                    return (
                      <button
                        key={opt}
                        type="button"
                        onClick={() => handleSelectOption(q.id, opt)}
                        className={`text-xs px-3.5 py-2 rounded-xl border transition-all text-left flex items-center gap-2 ${
                          isSelected
                            ? 'bg-indigo-600/20 border-indigo-500 text-indigo-200 shadow-md shadow-indigo-600/10 font-medium'
                            : 'bg-slate-950/40 border-slate-800 text-slate-400 hover:text-slate-200 hover:border-slate-700'
                        }`}
                      >
                        <CheckCircle2
                          className={`w-3.5 h-3.5 shrink-0 ${isSelected ? 'text-indigo-400' : 'text-slate-600'}`}
                        />
                        <span>{opt}</span>
                      </button>
                    );
                  })}
                </div>
              )}

              {/* Custom input or refinement */}
              <div className="relative">
                <input
                  type="text"
                  value={currentAnswer}
                  onChange={(e) => handleCustomInput(q.id, e.target.value)}
                  placeholder="Hoặc tự gõ câu trả lời theo ý bạn..."
                  className="w-full bg-slate-950/80 border border-slate-800 rounded-xl px-4 py-2.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all"
                />
              </div>
            </div>
          );
        })}

        {/* Submit Actions */}
        <div className="flex items-center justify-end gap-3 pt-2">
          <button
            type="submit"
            disabled={loading}
            className="flex items-center gap-2 px-6 py-3 rounded-xl text-sm font-semibold text-white bg-gradient-to-r from-indigo-600 via-indigo-500 to-emerald-500 hover:from-indigo-500 hover:to-emerald-400 shadow-lg shadow-indigo-500/25 active:scale-95 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span>{loading ? 'Đang phân tích...' : 'Chốt Yêu Cầu & Chuyển Sang Duyệt Concept'}</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </form>
    </div>
  );
};
