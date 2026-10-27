from typing import Dict, Any
from app.harness.models import TestCase
from app.schemas.session import BriefQuestion, DesignProposal

BENCHMARK_CASES: Dict[str, TestCase] = {
    "b2b_saas": TestCase(
        id="b2b_saas",
        industry="B2B SaaS / Enterprise AI",
        prompt="TalentAI - Nền tảng AI tự động sàng lọc và phỏng vấn ứng viên công nghệ hàng đầu.",
        brief_answers={
            "target_audience": "Tech Recruiter, Giám đốc Nhân sự & CTO tại các công ty công nghệ vừa và lớn",
            "brand_style": "Hiện đại, Công nghệ cao (Tech-forward), Tối giản sang trọng và Đáng tin cậy",
            "conversion_goal": "Đăng ký dùng thử 14 ngày & Đặt lịch Demo trực tiếp 1-on-1"
        },
        proposal={
            "target_audience": "Tech Recruiter & HR Leaders tại các công ty công nghệ",
            "value_proposition": "Cắt giảm 70% thời gian tuyển dụng với AI sàng lọc CV và phỏng vấn tự động",
            "sections_outline": [
                {"id": "hero", "name": "Hero Section", "purpose": "Thu hút và kêu gọi đăng ký demo"},
                {"id": "social_proof", "name": "Trust Bar", "purpose": "Logo 500+ doanh nghiệp tin dùng"},
                {"id": "features", "name": "Core Features", "purpose": "AI matching & Auto video screening"},
                {"id": "pricing", "name": "Transparent Pricing", "purpose": "Bảng giá minh bạch 3 gói"},
                {"id": "faq", "name": "FAQ", "purpose": "Giải đáp về bảo mật dữ liệu & tích hợp ATS"},
                {"id": "cta", "name": "Final CTA", "purpose": "Chốt chuyển đổi dùng thử miễn phí"}
            ],
            "color_palette": {
                "primary": "#3B82F6",
                "secondary": "#1E293B",
                "accent": "#10B981",
                "background": "#0F172A",
                "surface": "#1E293B"
            },
            "typography": {
                "heading": "Outfit, sans-serif",
                "body": "Inter, sans-serif"
            },
            "tone_of_voice": "Chuyên nghiệp, tin cậy, đột phá công nghệ"
        },
        target_element={
            "tag": "button",
            "element_id": "hero-cta-btn",
            "current_html": '<button id="hero-cta-btn" class="bg-blue-600 text-white font-medium px-6 py-3 rounded-lg shadow-md hover:bg-blue-700">Dùng Thử Miễn Phí</button>'
        },
        tweak_instruction="Đổi nút sang gradient cam bo tròn đầy đủ, thêm hiệu ứng bóng đổ và đổi chữ thành Đặt Lịch Demo Ngay"
    ),
    "ecommerce_fashion": TestCase(
        id="ecommerce_fashion",
        industry="E-Commerce / Streetwear Fashion",
        prompt="StreetVibe - Thương hiệu thời trang dạo phố phong cách Cyberpunk trẻ trung, năng động.",
        brief_answers={
            "target_audience": "Giới trẻ Gen Z (18-28 tuổi) đam mê phong cách đường phố độc bản",
            "brand_style": "Nổi loạn, Cyberpunk neon, Đậm chất tương lai (Futuristic)",
            "conversion_goal": "Săn bộ sưu tập giới hạn (Drop) & Nhận mã giảm 20%"
        }
    ),
    "online_education": TestCase(
        id="online_education",
        industry="EdTech / Professional Bootcamps",
        prompt="ProDev Bootcamp - Khóa học lập trình Full-Stack Web thực chiến từ con số 0 trong 12 tuần.",
        brief_answers={
            "target_audience": "Sinh viên CNTT và người đi làm muốn chuyển ngành sang lập trình viên",
            "brand_style": "Thực chiến, Truyền cảm hứng, Uy tín và Cam kết đầu ra",
            "conversion_goal": "Đăng ký nhận lộ trình học tập chi tiết & Học bổng 30%"
        }
    ),
    "creative_agency": TestCase(
        id="creative_agency",
        industry="Creative Agency / Digital Marketing",
        prompt="NovaStudio - Agency thiết kế nhận diện thương hiệu và giải pháp tiếp thị kỹ thuật số cao cấp.",
        brief_answers={
            "target_audience": "Nhà sáng lập Startup & Doanh nghiệp SME muốn nâng tầm thương hiệu",
            "brand_style": "Nghệ thuật, Sang trọng, Sáng tạo và Đột phá thị giác",
            "conversion_goal": "Gửi yêu cầu báo giá dự án (Request a Proposal)"
        }
    ),
    "edge_cases": TestCase(
        id="edge_cases",
        industry="Edge Cases / Minimal & Malformed Inputs",
        prompt="Quán cà phê góc phố",
        brief_answers={
            "target_audience": "Khách vãng lai",
            "brand_style": "Mộc mạc",
            "conversion_goal": "Đến quán"
        }
    )
}

MOCK_AGENT_OUTPUTS: Dict[str, Any] = {
    "ba_analyst": [
        BriefQuestion(
            id="target_audience",
            question="Đối tượng khách hàng mục tiêu chính cho dự án của bạn là ai?",
            quick_options=["Doanh nghiệp IT & Startup", "Doanh nghiệp vừa và nhỏ (SME)", "Cá nhân & Freelancer", "Chuyên viên tuyển dụng"],
            required=True
        ),
        BriefQuestion(
            id="brand_style",
            question="Phong cách nhận diện và cảm xúc thương hiệu bạn muốn truyền tải?",
            quick_options=["Công nghệ hiện đại (Tech-forward)", "Tối giản sang trọng (Minimal Luxury)", "Trẻ trung năng động", "Tin cậy truyền thống"],
            required=True
        ),
        BriefQuestion(
            id="conversion_goal",
            question="Mục tiêu hành động chuyển đổi chính (Primary CTA) của Landing Page là gì?",
            quick_options=["Đăng ký dùng thử miễn phí 14 ngày", "Đặt lịch tư vấn trực tiếp 1-on-1", "Tải tài liệu / Báo cáo", "Liên hệ nhận báo giá"],
            required=True
        )
    ],
    "proposal": DesignProposal(
        target_audience="Tech Recruiter & HR Leaders tại các công ty công nghệ",
        value_proposition="Cắt giảm 70% thời gian tuyển dụng với AI sàng lọc CV và phỏng vấn kỹ năng tự động",
        sections_outline=[
            {"id": "hero", "name": "Hero Section", "purpose": "Thu hút sự chú ý ngay lập tức kèm CTA nổi bật"},
            {"id": "social_proof", "name": "Social Proof & Trust Badges", "purpose": "500+ doanh nghiệp công nghệ tin dùng"},
            {"id": "features", "name": "Core Features & AI Matching", "purpose": "Trình diễn tính năng sàng lọc CV tự động"},
            {"id": "pricing", "name": "Pricing Tiers", "purpose": "Minh bạch chi phí với 3 gói linh hoạt"},
            {"id": "faq", "name": "FAQ Section", "purpose": "Giải tỏa các lo ngại về bảo mật dữ liệu"},
            {"id": "cta", "name": "Final CTA Banner", "purpose": "Kêu gọi dùng thử 14 ngày không rủi ro"}
        ],
        color_palette={
            "primary": "#3B82F6",
            "secondary": "#1E293B",
            "accent": "#10B981",
            "background": "#0F172A",
            "surface": "#1E293B"
        },
        typography={
            "heading": "Outfit, sans-serif",
            "body": "Inter, sans-serif"
        },
        tone_of_voice="Chuyên nghiệp, tin cậy, đột phá công nghệ và hướng tới hành động",
        revision_notes="Bản đề xuất chuẩn tối ưu chuyển đổi"
    ),
    "strategist": """# BẢN DÀN Ý CHIẾN LƯỢC CHUYỂN ĐỔI CAO (TALENTAI)

## 1. Header & Navigation
- Logo: TalentAI biểu tượng tia sét công nghệ.
- Menu: Tính năng, Giải pháp, Bảng giá, Khách hàng, Đăng nhập.
- CTA Header: Dùng Thử Miễn Phí.

## 2. Hero Section (Móc câu chuyển đổi)
- Hook mạnh mẽ: "Tuyển dụng nhân tài công nghệ nhanh gấp 5 lần với AI."
- Subheadline: "Tự động hóa toàn bộ quy trình từ lọc CV, phỏng vấn kỹ năng sơ bộ đến gửi bài test lập trình."
- Primary CTA: "Bắt Đầu Dùng Thử 14 Ngày" (Nổi bật, cam kết không cần thẻ tín dụng).
- Social Proof micro-badge: "Được tin dùng bởi 10,000+ HR Manager và CTO."

## 3. Social Proof & Trust Bar
- Logo các công ty công nghệ hàng đầu tin tưởng.
- Số liệu ấn tượng: 99.4% độ chính xác matching, 72 giờ để hoàn tất quy trình phỏng vấn.

## 4. Problem & Solution / Features
- Tính năng 1: Smart CV Parser đọc hiểu 50+ định dạng hồ sơ kỹ thuật.
- Tính năng 2: AI Voice/Video Screening phỏng vấn phản xạ ứng viên.
- Tính năng 3: Auto Coding Assessment chấm điểm tự động.

## 5. Visual Showcase & How It Works
- Bước 1: Đăng tải mô tả công việc (JD).
- Bước 2: AI quét và phỏng vấn ứng viên theo tiêu chuẩn.
- Bước 3: Nhận danh sách Top 5 ứng viên xuất sắc nhất.

## 6. Testimonials & Khách Hàng
- Lời chứng thực chân thật từ Head of Talent tại VNG và FPT Software.

## 7. Pricing & Special Offer
- Gói Starter, Pro, Enterprise kèm cam kết hoàn tiền 30 ngày nếu không hài lòng.

## 8. FAQ (Câu Hỏi Thường Gặp)
- Dữ liệu ứng viên có được bảo mật không?
- Có tích hợp được với hệ thống ATS sẵn có không?

## 9. Final High-Impact CTA
- Banner chốt hạ chuyển đổi: Sẵn sàng nâng cấp phòng tuyển dụng của bạn?

## 10. Footer
- Bản quyền, chính sách bảo mật, liên kết mạng xã hội.""",
    "copywriter": """# NỘI DUNG CHUYỂN ĐỔI (TALENTAI)

**Hero Headline**: Tuyển Dụng Nhân Tài Công Nghệ Nhanh Hơn 5 Lần Với Trợ Lý AI
**Hero Subheadline**: Loại bỏ 90% công việc thủ công, tự động sàng lọc hàng ngàn hồ sơ và phỏng vấn kỹ năng chuẩn xác.
**Hero CTA Button**: Bắt Đầu Dùng Thử Miễn Phí (Không cần thẻ tín dụng)

**Social Proof**: Hơn 500+ doanh nghiệp công nghệ hàng đầu tăng 300% hiệu suất tuyển dụng.
**Value Proposition**: Tiết kiệm 40 giờ làm việc mỗi tuần cho đội ngũ HR và tìm đúng lập trình viên xuất sắc.

**FAQ Section**:
- Q: Dữ liệu hồ sơ ứng viên có được bảo mật chuẩn GDPR không?
  A: Tuyệt đối an toàn với mã hóa đầu cuối 256-bit và tuân thủ chuẩn bảo mật ISO 27001.
- Q: Nền tảng có hỗ trợ phỏng vấn các ngôn ngữ lập trình nào?
  A: Hỗ trợ hơn 30+ ngôn ngữ phổ biến gồm Python, Java, Golang, React, v.v.
- Q: Tôi có thể hủy dịch vụ bất kỳ lúc nào không?
  A: Bạn có thể nâng cấp hoặc hủy gói bất cứ lúc nào với 1 cú click.""",
    "designer": """# DESIGN SYSTEM SPECIFICATION (TALENTAI)

- **Color Palette**:
  - Primary: `#3B82F6` (Electric Blue - tạo cảm giác công nghệ đột phá)
  - Secondary: `#1E293B` (Slate Dark - nền tảng vững chắc, tin cậy)
  - Accent: `#10B981` (Emerald Green - điểm nhấn chuyển đổi thành công)
  - Background: `#0F172A` (Deep Slate - sang trọng, hiện đại)
  - Surface: `#1E293B` (Card elevated surface)

- **Typography**:
  - Font Heading: `Outfit, sans-serif` (Trẻ trung, hình học hiện đại)
  - Font Body: `Inter, sans-serif` (Dễ đọc tối ưu trên mọi màn hình)

- **Layout & Spacing**:
  - Container: `max-w-7xl mx-auto px-4 sm:px-6 lg:px-8`
  - Section Spacing: `py-16 md:py-24`
  - Grid: `grid grid-cols-1 md:grid-cols-3 gap-8`

- **Visual Effects**:
  - Card Shadow: `shadow-xl shadow-blue-500/10`
  - Glassmorphism: `backdrop-blur-md bg-slate-800/60 border border-slate-700/50`
  - Gradient Accent: `bg-gradient-to-r from-blue-500 to-indigo-600`""",
    "coder": """<!DOCTYPE html>
<html lang="vi" class="scroll-smooth">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TalentAI - Nền tảng tuyển dụng công nghệ tự động</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
</head>
<body class="bg-slate-950 text-slate-100 font-sans antialiased">
    <header class="sticky top-0 z-50 backdrop-blur-md bg-slate-900/80 border-b border-slate-800">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
            <div class="flex items-center gap-2">
                <i data-lucide="zap" class="w-6 h-6 text-blue-500"></i>
                <span class="text-xl font-bold tracking-tight text-white">TalentAI</span>
            </div>
            <button class="bg-blue-600 hover:bg-blue-500 text-white text-sm font-semibold px-4 py-2 rounded-lg transition-colors">
                Dùng Thử Miễn Phí
            </button>
        </div>
    </header>

    <main>
        <section id="hero" class="py-20 md:py-32 px-4 text-center max-w-4xl mx-auto">
            <h1 class="text-4xl sm:text-5xl md:text-6xl font-extrabold tracking-tight text-white mb-6">
                Tuyển Dụng Nhân Tài Nhanh Hơn <span class="text-blue-500">5 Lần</span> Với AI
            </h1>
            <p class="text-lg text-slate-300 mb-8 max-w-2xl mx-auto">
                Tự động hóa sàng lọc hồ sơ, phỏng vấn kỹ năng kỹ thuật chuẩn xác và tìm đúng lập trình viên xuất sắc.
            </p>
            <div class="flex flex-col sm:flex-row justify-center gap-4">
                <button id="hero-cta-btn" class="bg-blue-600 hover:bg-blue-500 text-white font-semibold px-8 py-3.5 rounded-xl shadow-lg shadow-blue-500/25 transition-all">
                    Bắt Đầu Dùng Thử 14 Ngày
                </button>
            </div>
        </section>

        <section id="features" class="py-16 bg-slate-900/50">
            <div class="max-w-7xl mx-auto px-4 grid grid-cols-1 md:grid-cols-3 gap-8">
                <div class="p-6 rounded-2xl bg-slate-800/50 border border-slate-700/50">
                    <i data-lucide="scan" class="w-8 h-8 text-blue-400 mb-4"></i>
                    <h3 class="text-xl font-semibold mb-2">Smart CV Parsing</h3>
                    <p class="text-slate-400">Trích xuất kỹ năng và đối chiếu kinh nghiệm với độ chính xác 99%.</p>
                </div>
                <div class="p-6 rounded-2xl bg-slate-800/50 border border-slate-700/50">
                    <i data-lucide="bot" class="w-8 h-8 text-emerald-400 mb-4"></i>
                    <h3 class="text-xl font-semibold mb-2">AI Interviewer</h3>
                    <p class="text-slate-400">Phỏng vấn tự động 24/7 đánh giá phản xạ và tư duy thuật toán.</p>
                </div>
                <div class="p-6 rounded-2xl bg-slate-800/50 border border-slate-700/50">
                    <i data-lucide="award" class="w-8 h-8 text-amber-400 mb-4"></i>
                    <h3 class="text-xl font-semibold mb-2">Auto Scoring</h3>
                    <p class="text-slate-400">Chấm điểm khách quan không định kiến, báo cáo chi tiết cho CTO.</p>
                </div>
            </div>
        </section>

        <section id="cta" class="py-20 text-center">
            <div class="max-w-3xl mx-auto px-4">
                <h2 class="text-3xl font-bold mb-4">Sẵn sàng cách mạng hóa tuyển dụng?</h2>
                <button class="bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-bold px-8 py-4 rounded-xl shadow-xl hover:opacity-95 transition-opacity">
                    Trải Nghiệm Miễn Phí Ngay
                </button>
            </div>
        </section>
    </main>

    <footer class="py-8 text-center text-slate-500 text-sm border-t border-slate-800">
        <p>© 2026 TalentAI. Bản quyền thuộc về Antigravity Landing Page Builder.</p>
    </footer>

    <script>
        lucide.createIcons();
    </script>
</body>
</html>""",
    "visual_qa": {
        "qa_passed": True,
        "qa_feedback": "Kiểm tra chất lượng thành công: Cấu trúc HTML5 chuẩn, Tailwind CSS CDN đầy đủ, Chrome DevTools 0 lỗi console & giao diện di động hoàn hảo.",
        "iteration": 1,
        "messages": [
            {
                "agent": "qa",
                "status": "completed",
                "message": "Quality checks passed",
                "passed": True
            }
        ],
        "devtools_audit": {
            "runtime_tested": True,
            "console_errors_count": 0,
            "console_errors": [],
            "has_overflow": False,
            "mobile_viewport": {"width": 375, "height": 812}
        }
    },
    "element_editor": '<button id="hero-cta-btn" class="bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-white font-bold px-8 py-4 rounded-full shadow-lg shadow-orange-500/25 transition-all duration-300">Đặt Lịch Demo Ngay</button>'
}
