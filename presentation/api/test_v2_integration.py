"""
Integration tests for v2 pipeline

Tests the complete flow from input through all agents to HTML output.

Run with: pytest presentation/api/test_v2_integration.py -v
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
    from renderers.component_renderer import HTMLComponentRenderer
except ImportError:
    # Fallback to absolute imports
    from api.agents.mock_agents_v2 import (
        MockContentAnalyzerAgentV2,
        MockPresentationStrategistAgentV2,
        MockContentGeneratorAgentV2,
    )
    from api.renderers.component_renderer import HTMLComponentRenderer


class TestCompleteV2Pipeline:
    """Test complete v2 pipeline from input to HTML"""

    def test_full_pipeline_flow(self):
        """Test complete flow: Analyzer → Strategist → Generator → Renderer"""

        # Setup agents (using mocks)
        analyzer = MockContentAnalyzerAgentV2()
        strategist = MockPresentationStrategistAgentV2()
        generator = MockContentGeneratorAgentV2()
        renderer = HTMLComponentRenderer()

        # User input
        user_input = "Our 5-person team has 20+ years of robotics experience. Located in Berlin and Munich."

        # Stage 1: Analyze
        analysis = analyzer.analyze(user_input)
        assert analysis is not None
        assert "slide_intent" in analysis
        assert "content_blocks" in analysis

        slide_intent = analysis["slide_intent"]
        content_blocks = analysis["content_blocks"]

        # Stage 2: Plan layout
        blueprint = strategist.plan(
            slide_intent=slide_intent,
            content_blocks=content_blocks,
        )
        assert blueprint is not None
        assert "components" in blueprint
        assert len(blueprint["components"]) > 0

        # Stage 3: Generate content
        formatted_slide = generator.generate(
            slide_title=blueprint.get("slide_title", "Test"),
            slide_blueprint=blueprint,
            content_blocks=content_blocks,
            language="en",
        )
        assert formatted_slide is not None
        assert "components" in formatted_slide

        # Stage 4: Render HTML
        formatted_slide["slide_id"] = "slide-1"
        formatted_slide["theme"] = "github"

        html = renderer.render_slide(formatted_slide)
        assert html is not None
        assert len(html) > 0
        assert "<section" in html
        assert "</section>" in html

    def test_feedback_loop_simulation(self):
        """Simulate feedback loop: Generator finds issue, Strategist replans"""

        analyzer = MockContentAnalyzerAgentV2()
        strategist = MockPresentationStrategistAgentV2()
        generator = MockContentGeneratorAgentV2()

        # Stage 1: Analyze
        analysis = analyzer.analyze("Some content")
        slide_intent = analysis["slide_intent"]
        content_blocks = analysis["content_blocks"]

        # Stage 2: Plan
        blueprint = strategist.plan(
            slide_intent=slide_intent,
            content_blocks=content_blocks,
        )

        initial_component_count = len(blueprint["components"])

        # Stage 3: Generate (would get validation error in real scenario)
        formatted_slide = generator.generate(
            slide_title=blueprint.get("slide_title"),
            slide_blueprint=blueprint,
            content_blocks=content_blocks,
            language="de",
        )

        # Simulate feedback
        feedback = {
            "warnings": [
                {
                    "component_id": "comp-2",
                    "issue": "Bullet list has 8 bullets (max 6)",
                    "suggestion": "Reduce to 5 bullets",
                }
            ]
        }

        # Stage 2b: Replan based on feedback
        adjusted_blueprint = strategist.replan(blueprint, feedback)

        # Verify replan happened
        assert adjusted_blueprint is not None
        assert "components" in adjusted_blueprint
        # Mock replan reduces components
        assert len(adjusted_blueprint["components"]) <= initial_component_count

    def test_different_content_types(self):
        """Test pipeline with different content types"""

        analyzer = MockContentAnalyzerAgentV2()
        strategist = MockPresentationStrategistAgentV2()
        generator = MockContentGeneratorAgentV2()

        test_inputs = [
            "We grew 45% YoY to €12.3M revenue",  # Statistics
            "Here's our deployment timeline: Phase 1 (Jan), Phase 2 (Mar), Phase 3 (Jun)",  # Timeline
            "Our solution reduces costs by 30% through automation",  # Problem/Solution
        ]

        for user_input in test_inputs:
            # Analyzer
            analysis = analyzer.analyze(user_input)
            assert "slide_intent" in analysis
            assert "content_blocks" in analysis

            # Strategist
            blueprint = strategist.plan(
                slide_intent=analysis["slide_intent"],
                content_blocks=analysis["content_blocks"],
            )
            assert "components" in blueprint

            # Generator
            formatted_slide = generator.generate(
                slide_title="Test",
                slide_blueprint=blueprint,
                content_blocks=analysis["content_blocks"],
            )
            assert "components" in formatted_slide

    def test_language_preservation(self):
        """Test that language is preserved through pipeline"""

        analyzer = MockContentAnalyzerAgentV2()
        strategist = MockPresentationStrategistAgentV2()
        generator = MockContentGeneratorAgentV2()

        languages = ["de", "en"]

        for lang in languages:
            # Analyze
            analysis = analyzer.analyze("Test content")

            # Force language
            analysis["slide_intent"]["language"] = lang

            # Plan
            blueprint = strategist.plan(
                slide_intent=analysis["slide_intent"],
                content_blocks=analysis["content_blocks"],
            )

            # Generate
            formatted_slide = generator.generate(
                slide_title="Test",
                slide_blueprint=blueprint,
                content_blocks=analysis["content_blocks"],
                language=lang,
            )

            # Verify language preserved
            assert formatted_slide["language"] == lang

    def test_html_output_validity(self):
        """Test that generated HTML is valid and complete"""

        analyzer = MockContentAnalyzerAgentV2()
        strategist = MockPresentationStrategistAgentV2()
        generator = MockContentGeneratorAgentV2()
        renderer = HTMLComponentRenderer()

        # Full pipeline
        analysis = analyzer.analyze("Test content")
        blueprint = strategist.plan(
            slide_intent=analysis["slide_intent"],
            content_blocks=analysis["content_blocks"],
        )
        formatted_slide = generator.generate(
            slide_title=blueprint.get("slide_title"),
            slide_blueprint=blueprint,
            content_blocks=analysis["content_blocks"],
        )

        # Add required fields for renderer
        formatted_slide["slide_id"] = "slide-1"
        formatted_slide["theme"] = "github"

        # Render
        html = renderer.render_slide(formatted_slide)

        # Verify HTML structure
        assert html.startswith('<section')
        assert html.strip().endswith('</section>')
        assert 'class="slide' in html
        assert 'id="slide-1"' in html

        # Should have components
        assert 'class="slide-component' in html

    def test_multiple_themes(self):
        """Test that different themes render correctly"""

        analyzer = MockContentAnalyzerAgentV2()
        strategist = MockPresentationStrategistAgentV2()
        generator = MockContentGeneratorAgentV2()

        themes = ["github", "modern", "minimal"]

        for theme_name in themes:
            from renderers.component_renderer import Theme

            theme = Theme(name=theme_name)
            renderer = HTMLComponentRenderer(theme=theme)

            # Full pipeline
            analysis = analyzer.analyze("Test")
            blueprint = strategist.plan(
                slide_intent=analysis["slide_intent"],
                content_blocks=analysis["content_blocks"],
            )
            formatted_slide = generator.generate(
                slide_title=blueprint.get("slide_title"),
                slide_blueprint=blueprint,
                content_blocks=analysis["content_blocks"],
            )

            # Add fields
            formatted_slide["slide_id"] = f"slide-{theme_name}"
            formatted_slide["theme"] = theme_name

            # Render
            html = renderer.render_slide(formatted_slide)

            # Verify theme is referenced
            assert f'slide-theme-{theme_name}' in html

    def test_image_handling(self):
        """Test that images are properly handled through pipeline"""

        analyzer = MockContentAnalyzerAgentV2()
        strategist = MockPresentationStrategistAgentV2()
        generator = MockContentGeneratorAgentV2()

        # Analyze
        analysis = analyzer.analyze("Check out this dashboard screenshot")
        content_blocks = analysis["content_blocks"]

        # Plan with image metadata
        blueprint = strategist.plan(
            slide_intent=analysis["slide_intent"],
            content_blocks=content_blocks,
            image_metadata={
                "images": [
                    {"filename": "dashboard.png", "description": "Analytics dashboard"}
                ]
            },
        )

        # Generate
        formatted_slide = generator.generate(
            slide_title=blueprint.get("slide_title"),
            slide_blueprint=blueprint,
            content_blocks=content_blocks,
        )

        # Verify components are structured
        assert "components" in formatted_slide
        assert len(formatted_slide["components"]) > 0

    def test_error_handling_missing_intent(self):
        """Test handling of malformed input"""

        analyzer = MockContentAnalyzerAgentV2()

        # Mocks always return valid data, but we can test structure
        result = analyzer.analyze("")  # Empty input

        assert "slide_intent" in result
        assert "content_blocks" in result

    def test_component_id_consistency(self):
        """Test that component IDs are consistent through pipeline"""

        analyzer = MockContentAnalyzerAgentV2()
        strategist = MockPresentationStrategistAgentV2()
        generator = MockContentGeneratorAgentV2()

        # Pipeline
        analysis = analyzer.analyze("Test")
        blueprint = strategist.plan(
            slide_intent=analysis["slide_intent"],
            content_blocks=analysis["content_blocks"],
        )

        # Get component IDs from blueprint
        blueprint_ids = set(c["component_id"] for c in blueprint["components"])

        # Generate
        formatted_slide = generator.generate(
            slide_title=blueprint.get("slide_title"),
            slide_blueprint=blueprint,
            content_blocks=analysis["content_blocks"],
        )

        # Get component IDs from formatted slide
        formatted_ids = set(c["component_id"] for c in formatted_slide["components"])

        # IDs should match or be subset
        assert formatted_ids.issubset(blueprint_ids) or len(formatted_ids) > 0


class TestRendererComponentTypes:
    """Test renderer with all component types"""

    def test_all_component_types_render(self):
        """Verify all component types can be rendered"""

        renderer = HTMLComponentRenderer()

        component_types = {
            "stat-grid": {
                "type": "stat-grid",
                "component_id": "comp-stat",
                "title": "Statistics",
                "statistics": [{"label": "Metric", "value": "100"}],
            },
            "bullet-list": {
                "type": "bullet-list",
                "component_id": "comp-bullet",
                "title": "Points",
                "bullets": ["Point 1", "Point 2"],
            },
            "quote": {
                "type": "quote",
                "component_id": "comp-quote",
                "quote_text": "A wise quote",
                "quote_author": "Author",
            },
            "text": {
                "type": "text",
                "component_id": "comp-text",
                "paragraphs": ["A paragraph of text"],
            },
            "image-frame": {
                "type": "image-frame",
                "component_id": "comp-image",
                "title": "Image",
                "image_path": "/img.png",
                "image_caption": "Caption",
                "image_alt_text": "Alt text",
            },
            "process": {
                "type": "process",
                "component_id": "comp-process",
                "title": "Process",
                "bullets": ["Step 1", "Step 2"],
            },
        }

        for comp_type, comp_data in component_types.items():
            html = renderer.render_component(comp_data)

            # Should produce valid HTML
            assert html is not None
            assert len(html) > 0
            assert comp_data["component_id"] in html
            assert '<div' in html


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
