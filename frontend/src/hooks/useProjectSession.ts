import { useState, useEffect, useCallback } from 'react';
import type { ProjectSession, PhaseStep, SessionStatus } from '../types/project';

const API_BASE = 'http://localhost:8000';

export function useProjectSession() {
  const [session, setSession] = useState<ProjectSession | null>(null);
  const [activePhase, setActivePhase] = useState<PhaseStep>(1);
  const [loading, setLoading] = useState<boolean>(false);
  const [statusMessage, setStatusMessage] = useState<string>('');
  const [error, setError] = useState<string | null>(null);

  // Restore session from localStorage on mount
  useEffect(() => {
    const savedSessionId = localStorage.getItem('lp_session_id');
    if (savedSessionId) {
      fetch(`${API_BASE}/api/project/session/${savedSessionId}`)
        .then(res => {
          if (res.ok) return res.json();
          throw new Error('Không tìm thấy phiên làm việc cũ');
        })
        .then((data: ProjectSession) => {
          setSession(data);
          determinePhase(data.status);
        })
        .catch(() => {
          localStorage.removeItem('lp_session_id');
        });
    }
  }, []);

  const determinePhase = (status: SessionStatus) => {
    if (status === 'BRIEFING' || status === 'BRIEF_READY') {
      setActivePhase(1);
    } else if (status === 'PROPOSING' || status === 'PROPOSAL_REVIEW') {
      setActivePhase(2);
    } else {
      setActivePhase(3);
    }
  };

  const startBrief = async (prompt: string, autoPilot: boolean = false) => {
    setLoading(true);
    setError(null);
    setStatusMessage(autoPilot ? 'Đang kích hoạt chế độ Auto-pilot...' : 'Agent BA đang phân tích yêu cầu brief...');
    try {
      const res = await fetch(`${API_BASE}/api/project/start-brief`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt, auto_pilot: autoPilot }),
      });
      if (!res.ok) throw new Error('Không thể khởi tạo Briefing');
      const data = await res.json();

      // Fetch fresh session
      const sRes = await fetch(`${API_BASE}/api/project/session/${data.session_id}`);
      const freshSession: ProjectSession = await sRes.json();
      setSession(freshSession);
      localStorage.setItem('lp_session_id', freshSession.session_id);

      if (autoPilot) {
        setActivePhase(3);
        await buildCodeInternal(freshSession.session_id);
      } else {
        setActivePhase(1);
      }
    } catch (err: any) {
      setError(err.message || 'Lỗi khi bắt đầu khảo sát Brief');
    } finally {
      setLoading(false);
      setStatusMessage('');
    }
  };

  const submitBrief = async (answers: Record<string, string>) => {
    if (!session) return;
    setLoading(true);
    setError(null);
    setStatusMessage('Đang chốt brief và tạo bản đề xuất thiết kế (Proposal)...');
    try {
      const res = await fetch(`${API_BASE}/api/project/submit-brief`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: session.session_id, answers }),
      });
      if (!res.ok) throw new Error('Lỗi khi lưu câu trả lời Brief');

      // Immediately generate proposal
      const propRes = await fetch(`${API_BASE}/api/project/generate-proposal`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: session.session_id }),
      });
      if (!propRes.ok) throw new Error('Lỗi khi sinh bản đề xuất Proposal');
      const updatedSession: ProjectSession = await propRes.json();
      setSession(updatedSession);
      setActivePhase(2);
    } catch (err: any) {
      setError(err.message || 'Lỗi khi chốt brief');
    } finally {
      setLoading(false);
      setStatusMessage('');
    }
  };

  const reviseProposal = async (feedback: string) => {
    if (!session) return;
    setLoading(true);
    setError(null);
    setStatusMessage('Đội ngũ đang cập nhật Proposal theo góp ý của bạn...');
    try {
      const res = await fetch(`${API_BASE}/api/project/generate-proposal`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: session.session_id, feedback }),
      });
      if (!res.ok) throw new Error('Không thể cập nhật Proposal');
      const updatedSession: ProjectSession = await res.json();
      setSession(updatedSession);
    } catch (err: any) {
      setError(err.message || 'Lỗi khi cập nhật đề xuất');
    } finally {
      setLoading(false);
      setStatusMessage('');
    }
  };

  const approveProposalAndBuild = async () => {
    if (!session) return;
    setLoading(true);
    setError(null);
    setStatusMessage('Đã duyệt Proposal! Bắt đầu chuyển giao cho Coder lập trình...');
    try {
      await fetch(`${API_BASE}/api/project/approve-proposal`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: session.session_id }),
      });
      setActivePhase(3);
      await buildCodeInternal(session.session_id);
    } catch (err: any) {
      setError(err.message || 'Lỗi khi duyệt Proposal');
      setLoading(false);
    }
  };

  const buildCodeInternal = async (sessionId: string) => {
    setLoading(true);
    setStatusMessage('Coder đang lập trình mã nguồn HTML5 & Tailwind CSS...');
    try {
      const response = await fetch(`${API_BASE}/api/project/build-code`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: sessionId }),
      });

      if (!response.body) throw new Error('Không thể nhận luồng SSE');
      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        const text = decoder.decode(value);
        const lines = text.split('\n');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6));
              if (data.type === 'step_start') {
                setStatusMessage(data.message || 'Đang xử lý...');
              } else if (data.type === 'complete' && data.session) {
                setSession(data.session);
              }
            } catch {
              // Ignore partial JSON
            }
          }
        }
      }
    } catch (err: any) {
      setError(err.message || 'Lỗi trong quá trình lập trình mã nguồn');
    } finally {
      setLoading(false);
      setStatusMessage('');
    }
  };

  const submitUATFeedback = async (feedback: string, targetElementId?: string) => {
    if (!session) return;
    setLoading(true);
    setError(null);
    setStatusMessage('Đang áp dụng góp ý UAT vào giao diện...');
    try {
      const response = await fetch(`${API_BASE}/api/project/uat-feedback`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: session.session_id,
          feedback,
          target_element_id: targetElementId,
        }),
      });

      if (!response.body) throw new Error('Không thể nhận luồng SSE');
      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        const text = decoder.decode(value);
        const lines = text.split('\n');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6));
              if (data.type === 'step_start') {
                setStatusMessage(data.message || 'Đang xử lý...');
              } else if (data.type === 'complete' && data.session) {
                setSession(data.session);
              }
            } catch {
              // Ignore partial JSON
            }
          }
        }
      }
    } catch (err: any) {
      setError(err.message || 'Lỗi khi gửi góp ý UAT');
    } finally {
      setLoading(false);
      setStatusMessage('');
    }
  };

  const resetProject = () => {
    localStorage.removeItem('lp_session_id');
    setSession(null);
    setActivePhase(1);
    setStatusMessage('');
    setError(null);
  };

  return {
    session,
    activePhase,
    setActivePhase,
    loading,
    statusMessage,
    error,
    startBrief,
    submitBrief,
    reviseProposal,
    approveProposalAndBuild,
    submitUATFeedback,
    resetProject,
  };
}
