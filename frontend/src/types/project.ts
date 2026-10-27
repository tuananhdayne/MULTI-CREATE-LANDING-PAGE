export type SessionStatus = 
  | "BRIEFING"
  | "BRIEF_READY"
  | "PROPOSING"
  | "PROPOSAL_REVIEW"
  | "BUILDING"
  | "UAT_REVIEW"
  | "COMPLETED";

export interface BriefQuestion {
  id: string;
  question: string;
  quick_options: string[];
  required: boolean;
}

export interface BriefData {
  questions: BriefQuestion[];
  answers: Record<string, string>;
  confirmed_summary?: string;
}

export interface SectionOutline {
  id: string;
  name: string;
  purpose?: string;
}

export interface DesignProposal {
  target_audience: string;
  value_proposition: string;
  sections_outline: SectionOutline[];
  color_palette: {
    primary?: string;
    secondary?: string;
    accent?: string;
    background?: string;
    surface?: string;
    [key: string]: string | undefined;
  };
  typography: {
    heading?: string;
    body?: string;
    [key: string]: string | undefined;
  };
  tone_of_voice: string;
  revision_notes?: string;
}

export interface DevToolsAudit {
  passed?: boolean;
  console_errors?: string[];
  console_errors_count?: number;
  has_overflow?: boolean;
  runtime_tested?: boolean;
  warning?: string;
}

export interface BuildArtifact {
  html_code: string;
  qa_report: {
    qa_passed?: boolean;
    qa_feedback?: string;
    devtools_audit?: DevToolsAudit;
    [key: string]: any;
  };
  created_at: string;
}

export interface UATFeedbackItem {
  feedback: string;
  target_element_id?: string;
  applied: boolean;
  timestamp: string;
}

export interface ProjectSession {
  session_id: string;
  status: SessionStatus;
  initial_prompt: string;
  brief: BriefData;
  proposal?: DesignProposal;
  build?: BuildArtifact;
  uat_history: UATFeedbackItem[];
  created_at: string;
  updated_at: string;
}

export type PhaseStep = 1 | 2 | 3;
