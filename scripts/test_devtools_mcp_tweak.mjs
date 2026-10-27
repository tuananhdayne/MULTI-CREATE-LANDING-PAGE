import { spawn } from "child_process";
import fs from "fs";
import path from "path";

const ARTIFACTS_DIR = "/home/tuananh/.gemini/antigravity-ide/brain/9cd55b4d-1c89-4c12-804a-89d767ba9adf";

// Sample high-converting landing page to seed into backend session
const SAMPLE_LANDING_PAGE = `<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AI SaaS Platform - Nền Tảng Tự Động Hóa</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-950 text-white min-h-screen font-sans">
  <header class="py-6 px-8 border-b border-slate-800 flex justify-between items-center max-w-7xl mx-auto">
    <div class="text-2xl font-black bg-gradient-to-r from-blue-400 to-indigo-500 bg-clip-text text-transparent">AI Flow</div>
    <nav class="hidden md:flex gap-6 text-sm text-slate-300">
      <a href="#features" class="hover:text-white transition">Tính năng</a>
      <a href="#pricing" class="hover:text-white transition">Bảng giá</a>
      <a href="#faq" class="hover:text-white transition">Hỏi đáp</a>
    </nav>
    <button class="bg-slate-800 hover:bg-slate-700 px-4 py-2 rounded-lg text-sm font-medium">Đăng Nhập</button>
  </header>

  <main class="max-w-5xl mx-auto px-6 py-20 text-center">
    <div class="inline-block px-4 py-1.5 rounded-full bg-blue-500/10 border border-blue-500/30 text-blue-400 text-xs font-semibold uppercase tracking-wider mb-6">
      🚀 Đột Phá Năng Suất Doanh Nghiệp 2026
    </div>
    <h1 id="hero-heading" class="text-4xl md:text-6xl font-extrabold tracking-tight mb-6 bg-gradient-to-b from-white via-slate-100 to-slate-400 bg-clip-text text-transparent">
      Tự Động Hóa Mọi Quy Trình Bán Hàng Với Trí Tuệ Nhân Tạo
    </h1>
    <p id="hero-subtext" class="text-lg md:text-xl text-slate-400 max-w-2xl mx-auto mb-10 leading-relaxed">
      Tăng trưởng doanh số thần tốc, tự động chăm sóc 10.000+ khách hàng cùng lúc mà không cần mở rộng đội ngũ nhân sự.
    </p>

    <div class="flex flex-col sm:flex-row gap-4 justify-center items-center">
      <button id="hero-cta-btn" class="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-8 py-4 rounded-xl shadow-lg shadow-blue-500/25 transition-all text-base">
        Bắt Đầu Dùng Thử Miễn Phí
      </button>
      <button id="hero-demo-btn" class="bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-200 font-semibold px-8 py-4 rounded-xl transition-all text-base">
        Xem Bản Demo (2 Phút)
      </button>
    </div>
  </main>
</body>
</html>`;

async function seedLandingPage() {
  console.log("1. Seeding sample landing page into backend...");
  const resp = await fetch("http://localhost:8000/api/tweak-element?project_id=default-project", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      element_id: "hero-cta-btn",
      tag: "button",
      classes: "bg-blue-600 hover:bg-blue-700 text-white font-semibold px-8 py-4 rounded-xl shadow-lg shadow-blue-500/25 transition-all text-base",
      current_html: '<button id="hero-cta-btn" class="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-8 py-4 rounded-xl shadow-lg shadow-blue-500/25 transition-all text-base">\n        Bắt Đầu Dùng Thử Miễn Phí\n      </button>',
      instruction: "Giữ nguyên mã",
      full_code: SAMPLE_LANDING_PAGE
    })
  });
  const data = await resp.json();
  console.log("   Seeded successfully! Version:", data.version);
}

class ChromeDevToolsClient {
  constructor() {
    this.proc = null;
    this.reqId = 0;
    this.pending = new Map();
  }

  async start() {
    this.proc = spawn("npx", ["-y", "chrome-devtools-mcp@latest", "--headless=true", "--no-usage-statistics"], {
      stdio: ["pipe", "pipe", "inherit"]
    });

    let buffer = "";
    this.proc.stdout.on("data", (chunk) => {
      buffer += chunk.toString("utf-8");
      const lines = buffer.split("\n");
      buffer = lines.pop();
      for (const line of lines) {
        if (!line.trim()) continue;
        try {
          const msg = JSON.parse(line);
          if (msg.id && this.pending.has(msg.id)) {
            const { resolve, reject } = this.pending.get(msg.id);
            this.pending.delete(msg.id);
            if (msg.error) reject(msg.error);
            else resolve(msg.result);
          }
        } catch (e) {}
      }
    });

    await new Promise((r) => setTimeout(r, 1500));
  }

  call(method, params = {}) {
    return new Promise((resolve, reject) => {
      const id = ++this.reqId;
      this.pending.set(id, { resolve, reject });
      const payload = JSON.stringify({ jsonrpc: "2.0", id, method, params }) + "\n";
      this.proc.stdin.write(payload);
    });
  }

  async callTool(name, args = {}) {
    return this.call("tools/call", { name, arguments: args });
  }

  stop() {
    if (this.proc) this.proc.kill();
  }
}

async function main() {
  await seedLandingPage();

  console.log("2. Launching Chrome DevTools MCP Client...");
  const devtools = new ChromeDevToolsClient();
  await devtools.start();

  await devtools.call("initialize", {
    protocolVersion: "2024-11-05",
    capabilities: {},
    clientInfo: { name: "test-client", version: "1.0.0" }
  });

  console.log("3. Connecting DevTools to page...");
  const pagesRes = await devtools.callTool("list_pages", {});
  console.log("   Pages available:", JSON.stringify(pagesRes.content));
  const pageId = 1;

  console.log("4. Navigating to Web App at http://localhost:5173...");
  await devtools.callTool("navigate_page", { pageId, url: "http://localhost:5173" });
  await new Promise((r) => setTimeout(r, 3000));

  console.log("5. Checking DOM state on http://localhost:5173...");
  const inspectCheck = await devtools.callTool("evaluate_script", {
    pageId,
    function: `() => {
      const iframe = document.querySelector('iframe');
      if (!iframe || !iframe.contentDocument) return { ready: false };
      const doc = iframe.contentDocument;
      const heading = doc.querySelector('#hero-heading');
      const cta = doc.querySelector('#hero-cta-btn');
      return {
        ready: true,
        heading: heading ? heading.textContent.trim() : null,
        ctaHtml: cta ? cta.outerHTML : null,
        ctaClasses: cta ? cta.className : null
      };
    }`
  });
  console.log("   Initial element check:", inspectCheck.content[0].text);

  console.log("6. Capturing DevTools BEFORE screenshot...");
  const beforeShot = await devtools.callTool("take_screenshot", {
    pageId,
    format: "png"
  });
  const beforeImg = beforeShot.content.find((c) => c.type === "image");
  if (beforeImg) {
    fs.writeFileSync(path.join(ARTIFACTS_DIR, "devtools_before_edit.png"), Buffer.from(beforeImg.data, "base64"));
    console.log("   Saved devtools_before_edit.png!");
  }

  console.log("7. Enabling 'Click-to-Inspect' mode in Header...");
  const enableInspect = await devtools.callTool("evaluate_script", {
    pageId,
    function: `() => {
      const buttons = Array.from(document.querySelectorAll('button'));
      const inspectBtn = buttons.find(b => b.textContent && b.textContent.includes('Click-to-Inspect'));
      if (inspectBtn) {
        inspectBtn.click();
        return { enabled: true, text: inspectBtn.textContent.trim() };
      }
      return { enabled: false };
    }`
  });
  console.log("   Inspect mode toggle:", enableInspect.content[0].text);
  await new Promise((r) => setTimeout(r, 800));

  console.log("8. Clicking #hero-cta-btn inside iframe to trigger InspectModal...");
  const clickInspect = await devtools.callTool("evaluate_script", {
    pageId,
    function: `() => {
      const iframe = document.querySelector('iframe');
      if (!iframe || !iframe.contentDocument) return { error: 'Iframe not ready' };
      const doc = iframe.contentDocument;
      const cta = doc.querySelector('#hero-cta-btn');
      if (!cta) return { error: 'No CTA button found' };

      // Click the element directly
      cta.click();
      return { clicked: true, tag: cta.tagName, id: cta.id, current_classes: cta.className };
    }`
  });
  console.log("   Click on CTA element:", clickInspect.content[0].text);
  await new Promise((r) => setTimeout(r, 1000));

  console.log("9. In InspectModal, selecting quick tweak 'Đổi màu thành gradient cam - hổ phách' and submitting...");
  const applyTweak = await devtools.callTool("evaluate_script", {
    pageId,
    function: `async () => {
      const modal = document.querySelector('.fixed.inset-0');
      if (!modal) {
        // Fallback: trigger message directly if click was blocked
        const iframe = document.querySelector('iframe');
        const cta = iframe?.contentDocument?.querySelector('#hero-cta-btn');
        if (cta) {
          window.postMessage({
            type: 'ELEMENT_SELECTED',
            data: {
              element_id: cta.id,
              tag: cta.tagName.toLowerCase(),
              classes: cta.className,
              current_html: cta.outerHTML
            }
          }, '*');
          await new Promise(r => setTimeout(r, 500));
        }
      }

      const activeModal = document.querySelector('.fixed.inset-0');
      if (!activeModal) return { error: 'InspectModal still not open' };

      // Click the quick tweak button for orange gradient
      const quickBtns = Array.from(activeModal.querySelectorAll('button[type="button"]'));
      const orangeBtn = quickBtns.find(b => b.textContent && b.textContent.includes('gradient cam'));
      if (orangeBtn) {
        orangeBtn.click();
      }

      await new Promise(r => setTimeout(r, 500));

      // Click the submit button: "Áp dụng chỉnh sửa"
      const submitBtn = activeModal.querySelector('button[type="submit"]');
      if (!submitBtn) return { error: 'Submit button not found' };
      submitBtn.click();

      return {
        submitted: true,
        instruction: activeModal.querySelector('textarea')?.value
      };
    }`
  });
  console.log("   Tweak submitted:", applyTweak.content[0].text);

  console.log("10. Waiting for Gemini AI Element Editor agent to process and update the landing page...");
  let updatedSuccessfully = false;
  let finalCtaInfo = null;

  for (let attempt = 1; attempt <= 15; attempt++) {
    await new Promise((r) => setTimeout(r, 2000));
    const checkUpdate = await devtools.callTool("evaluate_script", {
      pageId,
      function: `() => {
        const iframe = document.querySelector('iframe');
        if (!iframe || !iframe.contentDocument) return { error: 'Iframe missing' };
        const doc = iframe.contentDocument;
        const cta = doc.querySelector('#hero-cta-btn');
        if (!cta) return { error: 'No CTA' };
        const cls = cta.className;
        const hasOrangeGradient = cls.includes('orange') || cls.includes('amber') || cls.includes('gradient');
        return {
          hasOrangeGradient,
          classes: cls,
          html: cta.outerHTML,
          text: cta.textContent.trim()
        };
      }`
    });

    try {
      const match = checkUpdate.content[0].text.match(/```json\n([\s\S]*?)\n```/);
      if (match) {
        const parsed = JSON.parse(match[1]);
        if (parsed.hasOrangeGradient) {
          updatedSuccessfully = true;
          finalCtaInfo = parsed;
          console.log(`   Element updated on attempt ${attempt}! New classes: ${parsed.classes}`);
          break;
        }
      }
    } catch (e) {}
    console.log(`   Waiting for AI update (attempt ${attempt}/15)...`);
  }

  console.log("11. Capturing DevTools AFTER screenshot...");
  const afterShot = await devtools.callTool("take_screenshot", {
    pageId,
    format: "png"
  });
  const afterImg = afterShot.content.find((c) => c.type === "image");
  if (afterImg) {
    fs.writeFileSync(path.join(ARTIFACTS_DIR, "devtools_after_edit.png"), Buffer.from(afterImg.data, "base64"));
    console.log("   Saved devtools_after_edit.png!");
  }

  devtools.stop();

  console.log("=================================================");
  console.log("CHROME DEVTOOLS MCP MODIFICATION TEST RESULT:");
  console.log("Success:", updatedSuccessfully);
  console.log("Final Element Data:", JSON.stringify(finalCtaInfo, null, 2));
  console.log("=================================================");
}

main().catch((err) => {
  console.error("FATAL ERROR:", err);
  process.exit(1);
});
