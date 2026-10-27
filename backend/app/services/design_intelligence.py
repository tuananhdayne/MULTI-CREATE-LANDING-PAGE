from typing import Dict, Any, List, Optional

STYLE_PRESETS: Dict[str, Dict[str, Any]] = {
    "modern_saas": {
        "id": "modern_saas",
        "name": "Modern High-Performance SaaS",
        "keywords": "Clean lines, subtle borders, high clarity, corporate trust, crisp contrast",
        "best_for": "B2B SaaS, AI platforms, FinTech, Developer tools, Enterprise software",
        "color_palette": {
            "primary": "#2563EB",      # Electric Blue
            "secondary": "#1E293B",    # Slate Dark
            "accent": "#10B981",       # Emerald Green
            "background": "#0F172A",   # Deep Slate Canvas
            "surface": "#1E293B"       # Elevated Card Surface
        },
        "typography": {
            "heading": "Outfit, sans-serif",
            "body": "Inter, sans-serif",
            "google_fonts_url": "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Outfit:wght@600;700;800&display=swap"
        },
        "layout_pattern": "Hero with prominent single-direction CTA, 3-column benefit grid, sticky glassmorphism header",
        "ui_rules": "Borders 1px slate-800, subtle hover glow, clear typographic scale, generous vertical rhythm."
    },
    "bento_grid": {
        "id": "bento_grid",
        "name": "Asymmetrical Bento Grid",
        "keywords": "Modular bento boxes, asymmetrical spans, deliberate information density, modern Apple-style craft",
        "best_for": "Product launches, hardware, modern software with diverse feature sets, tech startups",
        "color_palette": {
            "primary": "#6366F1",      # Indigo Accent
            "secondary": "#18181B",    # Zinc Surface
            "accent": "#EC4899",       # Vivid Pink
            "background": "#09090B",   # Pitch Black
            "surface": "#18181B"       # Dark Zinc
        },
        "typography": {
            "heading": "Space Grotesk, sans-serif",
            "body": "Plus Jakarta Sans, sans-serif",
            "google_fonts_url": "https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600&family=Space+Grotesk:wght@600;700&display=swap"
        },
        "layout_pattern": "Bento layout with 1 large spotlight card (col-span-2) paired with 2-3 compact stat cards",
        "ui_rules": "Rounded 2xl cards, border border-zinc-800/80, internal padding p-6 to p-8, backdrop-blur."
    },
    "dark_cyberpunk": {
        "id": "dark_cyberpunk",
        "name": "Dark Cyberpunk / Neo-Futuristic",
        "keywords": "Vibrant neon glows, deep midnight blacks, energetic borders, high-contrast cyber accents",
        "best_for": "Streetwear, Gaming, Web3, Crypto, Nightlife, Youth culture brands",
        "color_palette": {
            "primary": "#06B6D4",      # Cyber Cyan
            "secondary": "#0F172A",    # Dark Midnight
            "accent": "#F43F5E",       # Neon Rose
            "background": "#030712",   # Void Black
            "surface": "#111827"       # Night Gray
        },
        "typography": {
            "heading": "Space Grotesk, sans-serif",
            "body": "Inter, sans-serif",
            "google_fonts_url": "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@600;700;800&display=swap"
        },
        "layout_pattern": "Angled accents, glowing button outlines, stark dark mode contrast with saturated focal points",
        "ui_rules": "Shadows shadow-cyan-500/20, high-contrast cyan/rose accents, bold dark canvas."
    },
    "minimal_editorial": {
        "id": "minimal_editorial",
        "name": "Minimalist Editorial & Luxury",
        "keywords": "Generous whitespace, refined serif/sans contrast, understated elegance, high-craft typography",
        "best_for": "Design agencies, luxury architecture, fashion lookbooks, boutique consulting, premium retreats",
        "color_palette": {
            "primary": "#0F172A",      # Deep Ink
            "secondary": "#475569",    # Charcoal
            "accent": "#D97706",       # Amber Gold
            "background": "#FAFAF9",   # Warm Editorial Paper
            "surface": "#FFFFFF"       # Crisp White
        },
        "typography": {
            "heading": "Syne, sans-serif",
            "body": "DM Sans, sans-serif",
            "google_fonts_url": "https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Syne:wght@600;700;800&display=swap"
        },
        "layout_pattern": "Generous whitespace (py-24), asymmetrical text-to-whitespace ratio, hairline 1px dividers",
        "ui_rules": "Subtle border-stone-200, no loud drop shadows, emphasis on typographic scale and negative space."
    },
    "warm_creator": {
        "id": "warm_creator",
        "name": "Warm Creator & Community",
        "keywords": "Warm friendly tones, organic rounded corners, human-centric trust, conversational flow",
        "best_for": "Online courses, community memberships, creators, coaching, wellness, non-profit",
        "color_palette": {
            "primary": "#EA580C",      # Warm Sunset Orange
            "secondary": "#292524",    # Warm Stone
            "accent": "#16A34A",       # Forest Growth Green
            "background": "#FFFBEB",   # Warm Cream White
            "surface": "#FFFFFF"       # Crisp White Card
        },
        "typography": {
            "heading": "Plus Jakarta Sans, sans-serif",
            "body": "Inter, sans-serif",
            "google_fonts_url": "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap"
        },
        "layout_pattern": "Friendly avatar clusters, prominent testimonial cards, rounded-2xl buttons with warm glow",
        "ui_rules": "Soft shadows shadow-orange-500/10, friendly approachable badges, warm welcoming layout."
    },
    "neo_brutalism": {
        "id": "neo_brutalism",
        "name": "Bold Neo-Brutalism",
        "keywords": "High contrast black borders, hard drop shadows, bold pop colors, retro punch, high energy",
        "best_for": "Gen-Z tools, viral marketing, disruptive consumer apps, hackathons, bold startups",
        "color_palette": {
            "primary": "#FFE600",      # Electric Yellow
            "secondary": "#000000",    # Pure Black
            "accent": "#FF5C00",       # Vibrant Tangerine
            "background": "#FFFDF0",   # Off-white Paper
            "surface": "#FFFFFF"       # White
        },
        "typography": {
            "heading": "Space Grotesk, sans-serif",
            "body": "Inter, sans-serif",
            "google_fonts_url": "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@700;800&display=swap"
        },
        "layout_pattern": "Stark 2px/3px black borders, offset solid shadows (shadow-[4px_4px_0px_#000]), bold badge stickers",
        "ui_rules": "border-2 border-black, shadow-[4px_4px_0px_#000], hover:translate-x-0.5 hover:translate-y-0.5."
    }
}

FONT_PAIRINGS: Dict[str, Dict[str, str]] = {
    "outfit_inter": {
        "heading": "Outfit, sans-serif",
        "body": "Inter, sans-serif",
        "google_fonts_url": "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Outfit:wght@600;700;800&display=swap",
        "vibe": "Tech-forward, crisp, highly legible across desktop and mobile"
    },
    "space_jakarta": {
        "heading": "Space Grotesk, sans-serif",
        "body": "Plus Jakarta Sans, sans-serif",
        "google_fonts_url": "https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600&family=Space+Grotesk:wght@600;700&display=swap",
        "vibe": "Modern developer, energetic geometry, distinctive character"
    },
    "syne_dm_sans": {
        "heading": "Syne, sans-serif",
        "body": "DM Sans, sans-serif",
        "google_fonts_url": "https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Syne:wght@600;700;800&display=swap",
        "vibe": "Editorial, artistic, premium boutique studio feel"
    },
    "cormorant_montserrat": {
        "heading": "Cormorant Garamond, serif",
        "body": "Montserrat, sans-serif",
        "google_fonts_url": "https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600;700&family=Montserrat:wght@400;500;600&display=swap",
        "vibe": "Luxury elegance, timeless beauty, upscale wellness"
    }
}

ANTI_AI_SLOP_GUIDELINES: List[str] = [
    "KHÔNG dùng gradient tím-hồng generic (dấu hiệu nhận biết AI-slop). Hãy chọn bảng màu gắn liền với cá tính thực tế của sản phẩm.",
    "KHÔNG tô màu hoặc in nghiêng chỉ một chữ đơn lẻ trong tiêu đề (ví dụ 'Nhanh Hơn <span class=gradient>5 Lần</span>') theo công thức rập khuôn.",
    "KHÔNG lạm dụng nhãn chữ hoa toàn bộ (ALL-CAPS) trên đầu mọi thẻ nội dung không cần thiết.",
    "KHÔNG đánh số thứ tự 01, 02, 03 nếu nội dung không phải là quy trình các bước theo trình tự thời gian.",
    "KHÔNG áp dụng hiệu ứng chuyển động hoặc hover rải rác trên mọi khối; chỉ giữ một hiệu ứng xuất hiện có chủ đích (orchestrated motion).",
    "Tuân thủ quy tắc tỷ lệ màu 60-30-10: 60% nền và không gian thở, 30% cấu trúc thẻ/đường viền, 10% điểm nhấn chuyển đổi (CTA chính).",
    "Đảm bảo chuẩn tương phản WCAG AA giữa màu chữ và màu nền (tối thiểu 4.5:1 đối với body text)."
]


def get_recommended_design_system(prompt: str, industry: Optional[str] = None) -> Dict[str, Any]:
    """
    Analyzes user requirements and recommends a tailored design system
    combining UI UX Pro Max intelligence and Frontend Design anti-default principles.
    """
    text = f"{prompt} {industry or ''}".lower()

    if any(k in text for k in ["cyberpunk", "thời trang dạo phố", "streetwear", "gaming", "game", "neon"]):
        style_key = "dark_cyberpunk"
    elif any(k in text for k in ["bento", "apple", "hardware", "thiết bị"]):
        style_key = "bento_grid"
    elif any(k in text for k in ["agency", "studio", "luxury", "kiến trúc", "nghệ thuật", "thời trang cao cấp"]):
        style_key = "minimal_editorial"
    elif any(k in text for k in ["khóa học", "giáo dục", "bootcamp", "cộng đồng", "coach", "học tập"]):
        style_key = "warm_creator"
    elif any(k in text for k in ["brutalism", "gen z", "viral", "hackathon", "pop"]):
        style_key = "neo_brutalism"
    else:
        # Default to Modern High-Performance SaaS
        style_key = "modern_saas"

    preset = STYLE_PRESETS[style_key]

    return {
        "style": preset,
        "color_palette": preset["color_palette"],
        "typography": preset["typography"],
        "layout_pattern": preset["layout_pattern"],
        "ui_rules": preset["ui_rules"],
        "anti_ai_slop_rules": ANTI_AI_SLOP_GUIDELINES
    }
