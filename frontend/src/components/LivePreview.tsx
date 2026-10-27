import React, { useEffect, useRef } from "react";
import { Sparkles, Eye } from "lucide-react";

interface SelectedElementData {
  element_id?: string;
  tag: string;
  classes: string;
  current_html: string;
}

interface LivePreviewProps {
  code: string;
  viewport: "desktop" | "tablet" | "mobile";
  inspectMode: boolean;
  onSelectElement: (element: SelectedElementData) => void;
  isGenerating: boolean;
}

export const LivePreview: React.FC<LivePreviewProps> = ({
  code,
  viewport,
  inspectMode,
  onSelectElement,
  isGenerating,
}) => {
  const iframeRef = useRef<HTMLIFrameElement>(null);

  // Viewport width styling
  const getViewportContainerStyle = () => {
    switch (viewport) {
      case "mobile":
        return "w-[375px] h-[720px] rounded-[36px] border-8 border-slate-800 shadow-2xl overflow-hidden my-auto";
      case "tablet":
        return "w-[768px] h-[920px] rounded-2xl border-4 border-slate-800 shadow-2xl overflow-hidden my-auto";
      case "desktop":
      default:
        return "w-full h-full rounded-none border-0";
    }
  };

  // Inject code and DevTools inspector script into iframe
  useEffect(() => {
    const iframe = iframeRef.current;
    if (!iframe) return;

    if (!code) {
      const doc = iframe.contentDocument || iframe.contentWindow?.document;
      if (doc) {
        doc.open();
        doc.write(`
          <!DOCTYPE html>
          <html>
          <head>
            <script src="https://cdn.tailwindcss.com"></script>
          </head>
          <body class="bg-slate-950 text-slate-400 flex flex-col items-center justify-center min-h-screen font-sans p-6 text-center">
            <div class="w-16 h-16 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center mb-4 text-indigo-400">
              <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12h20"/><path d="M20 12v8H4v-8"/><path d="m4 4 16 0"/><path d="M4 4v4h16V4"/></svg>
            </div>
            <h2 class="text-xl font-bold text-white mb-2">Chưa có Landing Page nào được tạo</h2>
            <p class="text-sm text-slate-500 max-w-md">Nhập mô tả sản phẩm của bạn ở thanh phía trên hoặc chọn một mẫu gợi ý để các Agent bắt đầu lập trình.</p>
          </body>
          </html>
        `);
        doc.close();
      }
      return;
    }

    // Build inspector helper script
    const inspectorScript = `
      <script>
        (function() {
          let activeOverlay = null;
          let isInspectActive = ${inspectMode};

          window.addEventListener('message', function(e) {
            if (e.data && e.data.type === 'SET_INSPECT_MODE') {
              isInspectActive = e.data.value;
              if (!isInspectActive && activeOverlay) {
                activeOverlay.remove();
                activeOverlay = null;
              }
            }
          });

          function createOverlay() {
            const el = document.createElement('div');
            el.id = '__devtools_inspect_overlay';
            el.style.position = 'absolute';
            el.style.pointerEvents = 'none';
            el.style.zIndex = '999999';
            el.style.border = '2px dashed #6366f1';
            el.style.backgroundColor = 'rgba(99, 102, 241, 0.15)';
            el.style.borderRadius = '4px';
            el.style.transition = 'all 0.1s ease';
            el.style.display = 'none';

            const badge = document.createElement('div');
            badge.id = '__devtools_inspect_badge';
            badge.style.position = 'absolute';
            badge.style.top = '-24px';
            badge.style.left = '0';
            badge.style.backgroundColor = '#4f46e5';
            badge.style.color = '#ffffff';
            badge.style.fontSize = '11px';
            badge.style.fontFamily = 'monospace';
            badge.style.padding = '2px 6px';
            badge.style.borderRadius = '4px';
            badge.style.whiteSpace = 'nowrap';
            el.appendChild(badge);

            document.body.appendChild(el);
            return el;
          }

          document.addEventListener('mouseover', function(e) {
            if (!isInspectActive) return;
            const target = e.target;
            if (!target || target.id === '__devtools_inspect_overlay' || target.id === '__devtools_inspect_badge') return;

            if (!activeOverlay) activeOverlay = createOverlay();

            const rect = target.getBoundingClientRect();
            const scrollLeft = window.pageXOffset || document.documentElement.scrollLeft;
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

            activeOverlay.style.width = rect.width + 'px';
            activeOverlay.style.height = rect.height + 'px';
            activeOverlay.style.top = (rect.top + scrollTop) + 'px';
            activeOverlay.style.left = (rect.left + scrollLeft) + 'px';
            activeOverlay.style.display = 'block';

            const badge = activeOverlay.querySelector('#__devtools_inspect_badge');
            if (badge) {
              const tag = target.tagName.toLowerCase();
              const id = target.id ? '#' + target.id : '';
              badge.textContent = tag + id;
            }
          }, true);

          document.addEventListener('click', function(e) {
            if (!isInspectActive) return;
            const target = e.target;
            if (!target || target.id === '__devtools_inspect_overlay') return;

            e.preventDefault();
            e.stopPropagation();

            window.parent.postMessage({
              type: 'ELEMENT_SELECTED',
              data: {
                element_id: target.id || '',
                tag: target.tagName.toLowerCase(),
                classes: target.className || '',
                current_html: target.outerHTML
              }
            }, '*');
          }, true);
        })();
      </script>
    `;

    const doc = iframe.contentDocument || iframe.contentWindow?.document;
    if (doc) {
      doc.open();
      // Inject inspector script right before </body>
      const htmlWithInspector = code.includes("</body>")
        ? code.replace("</body>", `${inspectorScript}</body>`)
        : code + inspectorScript;
      doc.write(htmlWithInspector);
      doc.close();
    }
  }, [code, inspectMode]);

  // Listen for message from iframe inspector
  useEffect(() => {
    const handleMessage = (e: MessageEvent) => {
      if (e.data && e.data.type === "ELEMENT_SELECTED") {
        onSelectElement(e.data.data);
      }
    };
    window.addEventListener("message", handleMessage);
    return () => window.removeEventListener("message", handleMessage);
  }, [onSelectElement]);

  // Broadcast inspectMode changes to iframe
  useEffect(() => {
    const iframe = iframeRef.current;
    if (iframe && iframe.contentWindow) {
      iframe.contentWindow.postMessage(
        { type: "SET_INSPECT_MODE", value: inspectMode },
        "*"
      );
    }
  }, [inspectMode]);

  return (
    <div className="relative w-full h-full flex items-center justify-center overflow-auto p-4 bg-slate-950/80">
      {/* Inspect Mode Banner Alert */}
      {inspectMode && (
        <div className="absolute top-4 left-1/2 -translate-x-1/2 z-40 bg-indigo-600/90 text-white text-xs font-semibold px-4 py-2 rounded-full shadow-xl shadow-indigo-600/30 backdrop-blur-md flex items-center gap-2 border border-indigo-400/30 animate-bounce">
          <Eye className="w-4 h-4" />
          <span>Click-to-Inspect đang bật: Hãy nhấp vào bất kỳ phần tử nào để sửa</span>
        </div>
      )}

      {/* Frame Container */}
      <div className={`relative transition-all duration-300 bg-white ${getViewportContainerStyle()}`}>
        <iframe
          ref={iframeRef}
          title="Landing Page Live Preview"
          className="w-full h-full border-0"
          sandbox="allow-scripts allow-same-origin allow-modals allow-forms"
        />

        {/* Generating Overlay Indicator */}
        {isGenerating && (
          <div className="absolute inset-0 bg-slate-950/40 backdrop-blur-[2px] z-20 flex items-center justify-center">
            <div className="bg-slate-900/90 border border-slate-700 p-4 rounded-2xl shadow-2xl flex items-center gap-3 text-white">
              <Sparkles className="w-5 h-5 text-indigo-400 animate-spin" />
              <div className="text-xs font-medium">Đội ngũ Agent đang hoàn thiện trang web...</div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
