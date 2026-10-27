import React, { useState } from 'react';
import type { DesignProposal } from '../../types/project';
import { 
  Palette, 
  Type, 
  Layers, 
  CheckCircle2, 
  Edit3, 
  ArrowRight, 
  FileText, 
  Sparkles,
  RefreshCw,
  Send
} from 'lucide-react';

interface ProposalReviewCardProps {
  proposal: DesignProposal;
  loading: boolean;
  onApprove: () => void;
  onRevise: (feedback: string) => void;
}

export const ProposalReviewCard: React.FC<ProposalReviewCardProps> = ({
  proposal,
  loading,
  onApprove,
  onRevise,
}) => {
  const [isRevising, setIsRevising] = useState<boolean>(false);
  const [feedbackText, setFeedbackText] = useState<string>('');

  const handleSendRevision = (e: React.FormEvent) => {
    e.preventDefault();
    if (!feedbackText.trim()) return;
    onRevise(feedbackText.trim());
    setFeedbackText('');
    setIsRevising(false);
  };

  return (
    <div className="max-w-4xl mx-auto my-8 px-4 animate-fade-in">
      {/* Proposal Card Header */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 mb-6 shadow-2xl backdrop-blur-xl">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-800">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
              <FileText className="w-6 h-6" />
            </div>
            <div>
              <span className="text-xs uppercase tracking-wider font-semibold text-emerald-400 bg-emerald-500/10 px-2.5 py-0.5 rounded-full border border-emerald-500/20">
                Chặng 2: Duyệt Kế Hoạch & Thiết Kế (Proposal Sign-off)
              </span>
              <h2 className="text-xl font-bold text-white mt-1">Đề Xuất Cấu Trúc & Ngôn Ngữ Thiết Kế</h2>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => setIsRevising(!isRevising)}
              disabled={loading}
              className="flex items-center gap-2 px-4 py-2.5 rounded-xl text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition-all"
            >
              <Edit3 className="w-3.5 h-3.5 text-amber-400" />
              <span>Yêu cầu chỉnh sửa</span>
            </button>
            <button
              onClick={onApprove}
              disabled={loading}
              className="flex items-center gap-2 px-5 py-2.5 rounded-xl text-xs font-semibold text-white bg-gradient-to-r from-emerald-600 to-teal-500 hover:from-emerald-500 hover:to-teal-400 shadow-lg shadow-emerald-500/25 active:scale-95 transition-all disabled:opacity-50"
            >
              <CheckCircle2 className="w-4 h-4" />
              <span>Phê Duyệt & Lập Trình</span>
            </button>
          </div>
        </div>

        {/* Value Prop Banner */}
        <div className="mt-4 bg-slate-950/60 rounded-xl p-4 border border-slate-800/80">
          <p className="text-xs text-slate-400 font-medium uppercase tracking-wider mb-1">Tuyên ngôn giá trị cốt lõi (Value Proposition):</p>
          <p className="text-sm font-semibold text-white">{proposal.value_proposition}</p>
          <div className="mt-2 flex items-center gap-2 text-xs text-slate-400">
            <span className="font-medium text-indigo-400">Khách hàng mục tiêu:</span>
            <span>{proposal.target_audience}</span>
          </div>
        </div>

        {proposal.revision_notes && (
          <div className="mt-3 bg-amber-500/10 border border-amber-500/20 rounded-xl p-3 text-xs text-amber-300 flex items-start gap-2">
            <Sparkles className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
            <div>
              <span className="font-semibold">Đã cập nhật theo góp ý: </span>
              <span>"{proposal.revision_notes}"</span>
            </div>
          </div>
        )}
      </div>

      {/* Revision Input Modal / Drawer if active */}
      {isRevising && (
        <form onSubmit={handleSendRevision} className="bg-slate-900 border border-amber-500/40 rounded-2xl p-5 mb-6 shadow-2xl backdrop-blur-xl animate-fade-in">
          <label className="text-xs font-semibold text-amber-300 block mb-2">
            Nhập phản hồi bạn muốn đội ngũ điều chỉnh (ví dụ: đổi sang tông màu tối neon, bổ sung khối so sánh giá, làm nổi bật cam kết hoàn tiền):
          </label>
          <div className="flex gap-2">
            <textarea
              value={feedbackText}
              onChange={(e) => setFeedbackText(e.target.value)}
              rows={2}
              placeholder="Gõ chi tiết yêu cầu thay đổi..."
              className="flex-1 bg-slate-950 border border-slate-700 rounded-xl p-3 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-amber-400"
            />
            <button
              type="submit"
              disabled={loading || !feedbackText.trim()}
              className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-amber-500 to-orange-500 text-white font-semibold text-xs flex items-center gap-1.5 self-end disabled:opacity-50"
            >
              <Send className="w-3.5 h-3.5" />
              <span>Gửi</span>
            </button>
          </div>
        </form>
      )}

      {/* Design System Tokens Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        {/* Color Palette */}
        <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 backdrop-blur-md shadow-xl">
          <div className="flex items-center gap-2 mb-4 text-slate-200">
            <Palette className="w-4 h-4 text-indigo-400" />
            <h3 className="text-sm font-semibold">Bảng Màu Chủ Đạo (Color Palette)</h3>
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
            {Object.entries(proposal.color_palette || {}).map(([role, hex]) => (
              <div key={role} className="bg-slate-950/70 border border-slate-800 rounded-xl p-2.5 flex items-center gap-2.5">
                <span
                  className="w-7 h-7 rounded-lg border border-white/20 shrink-0 shadow-inner"
                  style={{ backgroundColor: hex || '#3B82F6' }}
                />
                <div className="overflow-hidden">
                  <p className="text-[11px] font-semibold text-white capitalize truncate">{role}</p>
                  <p className="text-[10px] text-slate-400 font-mono">{hex}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Typography & Tone */}
        <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 backdrop-blur-md shadow-xl flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-2 mb-4 text-slate-200">
              <Type className="w-4 h-4 text-teal-400" />
              <h3 className="text-sm font-semibold">Typography & Tone Giọng</h3>
            </div>
            <div className="space-y-3">
              <div className="bg-slate-950/70 border border-slate-800 rounded-xl p-3">
                <span className="text-[10px] text-slate-400 uppercase tracking-wider block font-semibold mb-1">Kiểu Chữ (Fonts):</span>
                <p className="text-xs text-white">
                  <span className="text-slate-400">Tiêu đề: </span>{proposal.typography?.heading || 'Outfit'} | <span className="text-slate-400">Nội dung: </span>{proposal.typography?.body || 'Inter'}
                </p>
              </div>
              <div className="bg-slate-950/70 border border-slate-800 rounded-xl p-3">
                <span className="text-[10px] text-slate-400 uppercase tracking-wider block font-semibold mb-1">Tone of Voice:</span>
                <p className="text-xs text-emerald-300 font-medium">{proposal.tone_of_voice}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Sections Roadmap Outline */}
      <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6 backdrop-blur-md shadow-xl">
        <div className="flex items-center gap-2 mb-4 text-slate-200">
          <Layers className="w-4 h-4 text-amber-400" />
          <h3 className="text-sm font-semibold">Cấu Trúc Các Khối Nội Dung (Sections Roadmap)</h3>
          <span className="text-xs text-slate-500">({proposal.sections_outline?.length || 0} khối)</span>
        </div>

        <div className="space-y-3">
          {proposal.sections_outline?.map((sec, idx) => (
            <div
              key={sec.id || idx}
              className="bg-slate-950/60 border border-slate-800/90 rounded-xl p-3.5 flex items-start gap-3 transition-all hover:border-slate-700"
            >
              <span className="w-6 h-6 rounded-lg bg-indigo-600/20 text-indigo-300 text-xs font-bold flex items-center justify-center shrink-0 border border-indigo-500/20">
                {idx + 1}
              </span>
              <div className="flex-1">
                <h4 className="text-xs font-bold text-white flex items-center gap-2">
                  <span>{sec.name}</span>
                  <span className="text-[10px] font-mono text-slate-500 font-normal">#{sec.id}</span>
                </h4>
                {sec.purpose && (
                  <p className="text-xs text-slate-400 mt-0.5">{sec.purpose}</p>
                )}
              </div>
            </div>
          ))}
        </div>

        {/* Footer Actions */}
        <div className="flex items-center justify-end gap-3 mt-6 pt-4 border-t border-slate-800">
          <button
            onClick={() => setIsRevising(true)}
            disabled={loading}
            className="px-4 py-2.5 rounded-xl text-xs font-semibold text-slate-300 hover:text-white hover:bg-slate-800 transition-all"
          >
            Sửa lại một vài chỗ
          </button>
          <button
            onClick={onApprove}
            disabled={loading}
            className="flex items-center gap-2 px-6 py-3 rounded-xl text-xs font-semibold text-white bg-gradient-to-r from-emerald-600 via-teal-600 to-emerald-500 hover:from-emerald-500 hover:to-teal-400 shadow-lg shadow-emerald-500/25 active:scale-95 transition-all"
          >
            <span>{loading ? 'Đang chuyển giao...' : 'Phê Duyệt & Bắt Đầu Lập Trình'}</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
};
