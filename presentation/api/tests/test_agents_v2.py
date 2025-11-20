"""
Unit tests for v2 agents and renderer

Run with: pytest presentation/api/test_agents_v2.py -v
"""

import sys
import os

# Add api directory to Python path
api_dir = os.path.dirname(__file__)
sys.path.insert(0, api_dir)

import pytest

# Try relative imports first (when running from api directory), then absolute (when running from parent)
try:
    from agents.mock_agents_v2 import (
        MockContentAnalyzerAgentV2,
        MockPresentationStrategistAgentV2,
        MockContentGeneratorAgentV2,
    )
    from renderers.component_renderer import HTMLComponentRenderer, Theme
    from schemas.blueprint import (
        ContentBlock,
        SlideIntent,
        ComponentBlueprint,
        SlideBlueprint,
        FormattedSlide,
    )
except ImportError:
    # Fallback to absolute imports
    from api.agents.mock_agents_v2 import (
        MockContentAnalyzerAgentV2,
        MockPresentationStrategistAgentV2,
        MockContentGeneratorAgentV2,
    )
    from api.renderers.component_renderer import HTMLComponentRenderer, Theme
    from api.schemas.blueprint import (
        ContentBlock,
        SlideIntent,
        ComponentBlueprint,
        SlideBlueprint,
        FormattedSlide,
    )


class TestContentAnalyzerV2:
    """Test ContentAnalyzer v2 with mock implementation"""

    def test_mock_analyzer_returns_correct_structure(self):
        """Mock analyzer should return slide_intent + content_blocks"""
        analyzer = MockContentAnalyzerAgentV2()
        result = analyzer.analyze("Test input")

        assert "slide_intent" in result
        assert "content_blocks" in result
        assert isinstance(result["slide_intent"], dict)
        assert isinstance(result["content_blocks"], list)

    def test_slide_intent_has_required_fields(self):
        """SlideIntent should have all required fields"""
        analyzer = MockContentAnalyzerAgentV2()
        result = analyzer.analyze("Test")

        intent = result["slide_intent"]
        assert "intent_type" in intent
        assert "primary_message" in intent
        assert "language" in intent
        assert "density" in intent

    def test_content_blocks_have_required_fields(self):
        """ContentBlocks should have type, content, priority"""
        analyzer = MockContentAnalyzerAgentV2()
        result = analyzer.analyze("Test")

        for block in result["content_blocks"]:
            assert "type" in block
            assert "content" in block
            assert "priority" in block

    def test_content_block_types_valid(self):
        """ContentBlock types should be valid"""
        analyzer = MockContentAnalyzerAgentV2()
        result = analyzer.analyze("Test")

        valid_types = [
            "title",
            "statistic",
            "statistics",
            "statement",
            "bullet",
            "bullets",
            "quote",
            "image_ref",
        ]

        for block in result["content_blocks"]:
            assert block["type"] in valid_types


class TestPresentationStrategistV2:
    """Test PresentationStrategist v2 with mock implementation"""

    def test_mock_strategist_returns_blueprint(self):
        """Mock strategist should return SlideBlueprint structure"""
        strategist = MockPresentationStrategistAgentV2()

        slide_intent = {
            "intent_type": "team",
            "primary_message": "Our team",
            "language": "de",
            "density": "medium",
        }
        content_blocks = [
            {"type": "title", "content": "Team", "priority": "must_have"},
        ]

        blueprint = strategist.plan(
            slide_intent=slide_intent,
            content_blocks=content_blocks,
        )

        assert "slide_title" in blueprint
        assert "layout_type" in blueprint
        assert "components" in blueprint
        assert isinstance(blueprint["components"], list)

    def test_components_have_required_fields(self):
        """Blueprint components should have required fields"""
        strategist = MockPresentationStrategistAgentV2()

        slide_intent = {"intent_type": "team", "primary_message": "Test", "language": "de", "density": "medium"}
        content_blocks = [{"type": "title", "content": "Test", "priority": "must_have"}]

        blueprint = strategist.plan(
            slide_intent=slide_intent,
            content_blocks=content_blocks,
        )

        for comp in blueprint["components"]:
            assert "component_id" in comp
            assert "type" in comp
            assert "position" in comp
            assert "content_block_indices" in comp

    def test_component_types_valid(self):
        """Component types should be from available list"""
        strategist = MockPresentationStrategistAgentV2()

        slide_intent = {"intent_type": "team", "primary_message": "Test", "language": "de", "density": "medium"}
        content_blocks = [{"type": "title", "content": "Test", "priority": "must_have"}]

        blueprint = strategist.plan(
            slide_intent=slide_intent,
            content_blocks=content_blocks,
        )

        valid_types = ["stat-grid", "bullet-list", "quote", "text", "image-frame", "process", "table"]

        for comp in blueprint["components"]:
            assert comp["type"] in valid_types

    def test_replan_reduces_components(self):
        """Replan should be able to adjust blueprint"""
        strategist = MockPresentationStrategistAgentV2()

        original = {
            "components": [
                {"component_id": "1", "type": "stat-grid", "position": "top"},
                {"component_id": "2", "type": "bullet-list", "position": "middle"},
                {"component_id": "3", "type": "text", "position": "bottom"},
            ]
        }

        feedback = {"issue": "Too many components"}

        adjusted = strategist.replan(original, feedback)

        assert "components" in adjusted
        assert len(adjusted["components"]) <= len(original["components"])


class TestContentGeneratorV2:
    """Test ContentGenerator v2 with mock implementation"""

    def test_mock_generator_returns_formatted_slide(self):
        """Mock generator should return FormattedSlide structure"""
        generator = MockContentGeneratorAgentV2()

        blueprint = {
            "slide_title": "Test",
            "components": [
                {"component_id": "comp-1", "type": "stat-grid"},
            ],
        }

        result = generator.generate(
            slide_title="Test",
            slide_blueprint=blueprint,
            content_blocks=[],
            language="de",
        )

        assert "slide_title" in result
        assert "components" in result
        assert "language" in result
        assert result["language"] == "de"

    def test_formatted_components_have_correct_fields(self):
        """FormattedComponentData should have correct fields per type"""
        generator = MockContentGeneratorAgentV2()

        blueprint = {"slide_title": "Test", "components": []}

        result = generator.generate(
            slide_title="Test",
            slide_blueprint=blueprint,
            content_blocks=[],
            language="de",
        )

        for comp in result["components"]:
            assert "component_id" in comp
            assert "type" in comp
            assert "word_count" in comp

    def test_stat_grid_has_statistics(self):
        """stat-grid component should have statistics field"""
        generator = MockContentGeneratorAgentV2()

        blueprint = {"slide_title": "Test", "components": []}

        result = generator.generate(
            slide_title="Test",
            slide_blueprint=blueprint,
            content_blocks=[],
            language="de",
        )

        stat_comps = [c for c in result["components"] if c["type"] == "stat-grid"]
        for comp in stat_comps:
            assert "statistics" in comp
            assert isinstance(comp["statistics"], list)

    def test_bullet_list_has_bullets(self):
        """bullet-list component should have bullets field"""
        generator = MockContentGeneratorAgentV2()

        blueprint = {"slide_title": "Test", "components": []}

        result = generator.generate(
            slide_title="Test",
            slide_blueprint=blueprint,
            content_blocks=[],
            language="de",
        )

        bullet_comps = [c for c in result["components"] if c["type"] == "bullet-list"]
        for comp in bullet_comps:
            assert "bullets" in comp
            assert isinstance(comp["bullets"], list)


class TestHTMLComponentRenderer:
    """Test HTML Component Renderer"""

    def test_renderer_initialization(self):
        """Renderer should initialize with default theme"""
        renderer = HTMLComponentRenderer()
        assert renderer.theme is not None
        assert renderer.theme.name == "github"

    def test_renderer_with_custom_theme(self):
        """Renderer should accept custom theme"""
        theme = Theme(name="modern", primary_color="#ff00ff")
        renderer = HTMLComponentRenderer(theme=theme)

        assert renderer.theme.name == "modern"
        assert renderer.theme.primary_color == "#ff00ff"

    def test_render_stat_grid_component(self):
        """Should render stat-grid component to HTML"""
        renderer = HTMLComponentRenderer()

        component = {
            "component_id": "comp-1",
            "type": "stat-grid",
            "title": "Metrics",
            "statistics": [
                {"label": "Revenue", "value": "€10M"},
                {"label": "Growth", "value": "+45%"},
            ],
        }

        html = renderer.render_component(component)

        assert "comp-1" in html
        assert "stat-grid" in html
        assert "Metrics" in html
        assert "Revenue" in html
        assert "€10M" in html
        assert "html" not in html.lower() or "<div" in html  # Check it's HTML

    def test_render_bullet_list_component(self):
        """Should render bullet-list component to HTML"""
        renderer = HTMLComponentRenderer()

        component = {
            "component_id": "comp-2",
            "type": "bullet-list",
            "title": "Features",
            "bullets": ["Feature 1", "Feature 2", "Feature 3"],
        }

        html = renderer.render_component(component)

        assert "comp-2" in html
        assert "bullet-list" in html
        assert "Feature 1" in html
        assert "<ul" in html or "<li" in html  # Should have list markup

    def test_render_quote_component(self):
        """Should render quote component to HTML"""
        renderer = HTMLComponentRenderer()

        component = {
            "component_id": "comp-3",
            "type": "quote",
            "quote_text": "This is a great quote",
            "quote_author": "Someone Famous",
        }

        html = renderer.render_component(component)

        assert "comp-3" in html
        assert "quote" in html
        assert "This is a great quote" in html
        assert "Someone Famous" in html
        assert "<blockquote" in html or "quote" in html.lower()

    def test_render_text_component(self):
        """Should render text component to HTML"""
        renderer = HTMLComponentRenderer()

        component = {
            "component_id": "comp-4",
            "type": "text",
            "title": "Description",
            "paragraphs": ["This is paragraph one.", "This is paragraph two."],
        }

        html = renderer.render_component(component)

        assert "comp-4" in html
        assert "Description" in html
        assert "This is paragraph one" in html
        assert "<p" in html

    def test_render_image_frame_component(self):
        """Should render image-frame component to HTML"""
        renderer = HTMLComponentRenderer()

        component = {
            "component_id": "comp-5",
            "type": "image-frame",
            "title": "Team Photo",
            "image_path": "/images/team.png",
            "image_caption": "Our awesome team",
            "image_alt_text": "Team members gathered",
        }

        html = renderer.render_component(component)

        assert "comp-5" in html
        assert "image-frame" in html
        assert "Team Photo" in html
        assert "/images/team.png" in html
        assert "Our awesome team" in html
        assert "<img" in html

    def test_render_process_component(self):
        """Should render process component with steps"""
        renderer = HTMLComponentRenderer()

        component = {
            "component_id": "comp-6",
            "type": "process",
            "title": "Process",
            "bullets": ["Step 1", "Step 2", "Step 3"],
        }

        html = renderer.render_component(component)

        assert "comp-6" in html
        assert "process" in html
        assert "Step 1" in html
        assert "Step 2" in html

    def test_render_complete_slide(self):
        """Should render complete slide with multiple components"""
        renderer = HTMLComponentRenderer()

        formatted_slide = {
            "slide_id": "slide-1",
            "slide_title": "Our Team",
            "slide_subtitle": "Meet the experts",
            "theme": "github",
            "components": [
                {
                    "component_id": "comp-1",
                    "type": "stat-grid",
                    "title": "Size",
                    "statistics": [{"label": "Members", "value": "5"}],
                },
                {
                    "component_id": "comp-2",
                    "type": "bullet-list",
                    "title": "Locations",
                    "bullets": ["Berlin", "Munich"],
                },
            ],
        }

        html = renderer.render_slide(formatted_slide)

        assert "Our Team" in html
        assert "Meet the experts" in html
        assert "comp-1" in html
        assert "comp-2" in html
        assert "<section" in html

    def test_render_styled_slide_includes_css(self):
        """render_styled_slide should include CSS"""
        from renderers.component_renderer import render_styled_slide

        formatted_slide = {
            "slide_id": "slide-1",
            "slide_title": "Test",
            "theme": "github",
            "components": [],
        }

        html = render_styled_slide(formatted_slide)

        assert "<style>" in html or "<style " in html
        assert "<!DOCTYPE html>" in html
        assert "</html>" in html

    def test_component_html_escaping(self):
        """Should escape HTML special characters in content"""
        renderer = HTMLComponentRenderer()

        component = {
            "component_id": "comp-1",
            "type": "text",
            "paragraphs": ["This has <script> and & special chars"],
        }

        html = renderer.render_component(component)

        # Should be escaped
        assert "<script>" not in html
        assert "&amp;" in html or "amp;" in html


class TestFeedbackLoop:
    """Test feedback loop mechanism"""

    def test_validation_result_structure(self):
        """ValidationResult should have proper structure"""
        generator = MockContentGeneratorAgentV2()

        # Generator always returns valid in mock, but we can test structure
        result = generator.generate(
            slide_title="Test",
            slide_blueprint={"components": []},
            content_blocks=[],
            language="de",
        )

        # Should not have is_valid: false (mock always succeeds)
        assert "is_valid" not in result or result.get("is_valid", True)

    def test_replan_on_feedback(self):
        """Strategist should replan when feedback provided"""
        strategist = MockPresentationStrategistAgentV2()

        original_blueprint = {
            "components": [
                {"component_id": "1", "type": "stat-grid"},
                {"component_id": "2", "type": "bullet-list"},
                {"component_id": "3", "type": "text"},
            ]
        }

        feedback = {
            "warnings": [{"component_id": "2", "issue": "Too many bullets"}],
        }

        adjusted = strategist.replan(original_blueprint, feedback)

        # Should have modified blueprint
        assert "components" in adjusted
        assert adjusted["components"] is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
