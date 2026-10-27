import pytest
from app.services.design_intelligence import (
    STYLE_PRESETS,
    FONT_PAIRINGS,
    ANTI_AI_SLOP_GUIDELINES,
    get_recommended_design_system,
)


def test_style_presets_integrity():
    expected_styles = {"modern_saas", "bento_grid", "dark_cyberpunk", "minimal_editorial", "warm_creator", "neo_brutalism"}
    assert expected_styles.issubset(set(STYLE_PRESETS.keys()))

    for key, style in STYLE_PRESETS.items():
        assert "name" in style
        assert "color_palette" in style
        palette = style["color_palette"]
        for c in ["primary", "secondary", "accent", "background", "surface"]:
            assert c in palette
            assert palette[c].startswith("#")
        assert "typography" in style
        assert "heading" in style["typography"]
        assert "body" in style["typography"]


def test_font_pairings_integrity():
    assert len(FONT_PAIRINGS) >= 4
    for key, pairing in FONT_PAIRINGS.items():
        assert "heading" in pairing
        assert "body" in pairing
        assert "google_fonts_url" in pairing


def test_anti_ai_slop_guidelines():
    assert len(ANTI_AI_SLOP_GUIDELINES) >= 5
    guideline_text = " ".join(ANTI_AI_SLOP_GUIDELINES)
    assert "gradient" in guideline_text.lower()
    assert "caps" in guideline_text.lower() or "chữ hoa" in guideline_text.lower()


def test_get_recommended_design_system_b2b():
    ds = get_recommended_design_system("TalentAI - Nền tảng tuyển dụng bằng trí tuệ nhân tạo")
    assert "style" in ds
    assert "color_palette" in ds
    assert "typography" in ds
    assert "anti_ai_slop_rules" in ds
    assert ds["typography"]["heading"] != ""


def test_get_recommended_design_system_cyberpunk():
    ds = get_recommended_design_system("StreetVibe - Thời trang dạo phố cyberpunk cho giới trẻ")
    assert ds["style"]["id"] in ["dark_cyberpunk", "neo_brutalism", "bento_grid"]
