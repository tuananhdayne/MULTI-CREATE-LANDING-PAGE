const API_BASE_URL = "http://localhost:8000";

export interface ProjectData {
  id: string;
  code: string;
  version: number;
  can_undo: boolean;
  can_redo: boolean;
}

export interface AgentEvent {
  agent: string;
  status: "started" | "thinking" | "completed" | "warning" | "error";
  message: string;
  summary?: string;
  passed?: boolean;
  errors?: string[];
}

export interface TweakPayload {
  element_id?: string;
  tag: string;
  classes: string;
  current_html: string;
  instruction: string;
  full_code?: string;
}

export interface HealthStatus {
  status: string;
  model: string;
  has_api_key: boolean;
  masked_key: string;
}

export const api = {
  async getHealth(): Promise<HealthStatus> {
    const res = await fetch(`${API_BASE_URL}/api/health`);
    if (!res.ok) throw new Error("Backend server is not responding");
    return res.json();
  },

  async getProject(projectId: string): Promise<ProjectData> {
    const res = await fetch(`${API_BASE_URL}/api/project?project_id=${encodeURIComponent(projectId)}`);
    if (!res.ok) throw new Error("Failed to load project");
    return res.json();
  },

  async undo(projectId: string): Promise<ProjectData> {
    const res = await fetch(`${API_BASE_URL}/api/undo?project_id=${encodeURIComponent(projectId)}`, {
      method: "POST"
    });
    if (!res.ok) throw new Error("Undo failed");
    return res.json();
  },

  async redo(projectId: string): Promise<ProjectData> {
    const res = await fetch(`${API_BASE_URL}/api/redo?project_id=${encodeURIComponent(projectId)}`, {
      method: "POST"
    });
    if (!res.ok) throw new Error("Redo failed");
    return res.json();
  },

  async tweakElement(projectId: string, payload: TweakPayload): Promise<ProjectData> {
    const res = await fetch(`${API_BASE_URL}/api/tweak-element?project_id=${encodeURIComponent(projectId)}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw new Error("Failed to tweak element");
    return res.json();
  },

  async streamGenerate(
    prompt: string,
    theme: string,
    projectId: string,
    onProgress: (event: AgentEvent) => void,
    onDone: (project: ProjectData) => void,
    onError: (errorMsg: string) => void
  ): Promise<void> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/generate?project_id=${encodeURIComponent(projectId)}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt, theme })
      });

      if (!response.ok || !response.body) {
        throw new Error(`Generation request failed: ${response.statusText}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n\n");
        buffer = lines.pop() || "";

        for (const block of lines) {
          if (!block.trim()) continue;

          let eventType = "message";
          let dataStr = "";

          const blockLines = block.split("\n");
          for (const line of blockLines) {
            if (line.startsWith("event: ")) {
              eventType = line.slice(7).trim();
            } else if (line.startsWith("data: ")) {
              dataStr = line.slice(6).trim();
            }
          }

          if (dataStr) {
            try {
              const parsed = JSON.parse(dataStr);
              if (eventType === "agent_progress") {
                onProgress(parsed);
              } else if (eventType === "done") {
                onDone(parsed.project);
              } else if (eventType === "error") {
                onError(parsed.message || "An error occurred");
              }
            } catch (e) {
              console.error("Failed to parse SSE event payload:", dataStr, e);
            }
          }
        }
      }
    } catch (err: any) {
      onError(err.message || "Failed to communicate with agent pipeline");
    }
  }
};
