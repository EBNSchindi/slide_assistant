"""
Integration Tests for Google Gemini Agents

Tests all 3 Google agents with mock and real API calls.
"""
import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from agents.content_analyzer_google import ContentAnalyzerAgentGoogle
from agents.presentation_strategist_google import PresentationStrategistAgentGoogle
from agents.content_generator_google import ContentGeneratorAgentGoogle
from config import GOOGLE_API_KEY, TEST_MODE


# Skip tests if no API key available
pytestmark = pytest.mark.skipif(
    not GOOGLE_API_KEY and not TEST_MODE,
    reason="GOOGLE_API_KEY not set and not in TEST_MODE"
)


class TestContentAnalyzerGoogle:
    """Test Google Gemini Content Analyzer Agent"""

    @pytest.fixture
    def analyzer(self):
        """Create analyzer instance"""
        return ContentAnalyzerAgentGoogle(
            api_key=GOOGLE_API_KEY or "test-key",
            model="gemini-3.0-pro",
        )

    def test_analyzer_initialization(self, analyzer):
        """Test that analyzer initializes correctly"""
        assert analyzer.model_name == "gemini-3.0-pro"
        assert analyzer.model is not None

    @pytest.mark.skipif(TEST_MODE, reason="Requires real API key")
    def test_analyze_kpi_slide_german(self, analyzer):
        """Test analyzing German KPI slide content"""
        user_input = """Unsere Q4 Kennzahlen
- €12,5 Mio ARR
- 180% Wachstum YoY
- 800+ aktive Kunden
- 98% Kundenzufriedenheit"""

        result = analyzer.analyze(user_input)

        # Validate structure
        assert "slide_intent" in result
        assert "content_blocks" in result

        slide_intent = result["slide_intent"]
        assert slide_intent["language"] == "de"
        assert slide_intent["intent_type"] in ["kpi", "metrics", "other"]
        assert "density" in slide_intent

        content_blocks = result["content_blocks"]
        assert len(content_blocks) > 0
        # Should detect statistics
        assert any(block["type"] in ["statistic", "statistics"] for block in content_blocks)

    @pytest.mark.skipif(TEST_MODE, reason="Requires real API key")
    def test_analyze_problem_statement_english(self, analyzer):
        """Test analyzing English problem statement"""
        user_input = """The Challenge
Traditional data analysis is slow and manual. Teams spend 60% of their time on data preparation instead of insights. This leads to delayed decisions and missed opportunities."""

        result = analyzer.analyze(user_input)

        slide_intent = result["slide_intent"]
        assert slide_intent["language"] == "en"
        assert slide_intent["intent_type"] in ["problem", "other"]

        content_blocks = result["content_blocks"]
        # Should have statement or text type
        assert any(block["type"] in ["statement", "text", "bullets"] for block in content_blocks)

    @pytest.mark.skipif(TEST_MODE, reason="Requires real API key")
    def test_analyze_quote(self, analyzer):
        """Test that quotes are detected correctly"""
        user_input = """"This product transformed our workflow. We save 20 hours per week."
- Sarah Johnson, CEO at DataCorp"""

        result = analyzer.analyze(user_input)

        content_blocks = result["content_blocks"]
        # Should have a quote type block
        quote_blocks = [b for b in content_blocks if b["type"] == "quote"]
        assert len(quote_blocks) > 0


class TestPresentationStrategistGoogle:
    """Test Google Gemini Presentation Strategist Agent"""

    @pytest.fixture
    def strategist(self):
        """Create strategist instance"""
        return PresentationStrategistAgentGoogle(
            api_key=GOOGLE_API_KEY or "test-key",
            model="gemini-3.0-pro",
        )

    def test_strategist_initialization(self, strategist):
        """Test that strategist initializes correctly"""
        assert strategist.model_name == "gemini-3.0-pro"
        assert strategist.model is not None

    @pytest.mark.skipif(TEST_MODE, reason="Requires real API key")
    def test_plan_mixed_content_layout(self, strategist):
        """Test planning layout for mixed content"""
        slide_intent = {
            "intent_type": "solution",
            "primary_message": "Our platform solves the data problem",
            "language": "en",
            "density": "medium",
        }

        content_blocks = [
            {"type": "statement", "content": "Our AI-powered platform automates data analysis", "priority": "must_have"},
            {"type": "bullets", "content": "- Real-time insights\n- Automated reports\n- Custom dashboards", "priority": "must_have"},
            {"type": "statistic", "content": "10x faster than manual analysis", "priority": "should_have"},
        ]

        design_system = {
            "max_components": 3,
            "available_components": ["stat-grid", "bullet-list", "text", "quote", "feature-grid"],
        }

        blueprint = strategist.plan(
            slide_intent=slide_intent,
            content_blocks=content_blocks,
            design_system=design_system,
        )

        # Validate blueprint structure
        assert "components" in blueprint
        assert len(blueprint["components"]) > 0
        assert len(blueprint["components"]) <= 3  # Respects max_components

        # Should have appropriate component types
        component_types = [c["type"] for c in blueprint["components"]]
        assert any(t in component_types for t in ["text", "bullet-list", "stat-grid"])

    @pytest.mark.skipif(TEST_MODE, reason="Requires real API key")
    def test_plan_table_layout(self, strategist):
        """Test planning layout for markdown table"""
        slide_intent = {
            "intent_type": "comparison",
            "primary_message": "Pricing tiers comparison",
            "language": "en",
            "density": "low",
        }

        content_blocks = [
            {
                "type": "markdown_table",
                "content": "| Plan | Price | Users |\n|------|-------|-------|\n| Basic | $10 | 5 |\n| Pro | $50 | 50 |",
                "priority": "must_have",
            }
        ]

        design_system = {
            "max_components": 3,
            "available_components": ["stat-grid", "bullet-list", "text", "table"],
        }

        blueprint = strategist.plan(
            slide_intent=slide_intent,
            content_blocks=content_blocks,
            design_system=design_system,
        )

        # Should recommend table component for markdown_table
        component_types = [c["type"] for c in blueprint["components"]]
        assert "table" in component_types


class TestContentGeneratorGoogle:
    """Test Google Gemini Content Generator Agent"""

    @pytest.fixture
    def generator(self):
        """Create generator instance"""
        return ContentGeneratorAgentGoogle(
            api_key=GOOGLE_API_KEY or "test-key",
            model="gemini-2.0-flash",  # Fast model for generation
        )

    def test_generator_initialization(self, generator):
        """Test that generator initializes correctly"""
        assert generator.model_name == "gemini-2.0-flash"
        assert generator.model is not None

    @pytest.mark.skipif(TEST_MODE, reason="Requires real API key")
    def test_generate_feature_grid(self, generator):
        """Test generating feature-grid component"""
        slide_blueprint = {
            "slide_title": "Key Features",
            "layout_type": "single",
            "components": [
                {
                    "component_id": "comp-1",
                    "type": "feature-grid",
                    "position": "center",
                    "content_block_indices": [0],
                }
            ],
        }

        content_blocks = [
            {
                "type": "features",
                "content": "✨ Real-time Analytics\n🎯 AI-powered Insights\n⚡ Lightning Fast\n🔒 Enterprise Security",
                "priority": "must_have",
            }
        ]

        slide_intent = {
            "intent_type": "solution",
            "language": "en",
            "density": "medium",
        }

        result = generator.generate(
            slide_blueprint=slide_blueprint,
            content_blocks=content_blocks,
            slide_intent=slide_intent,
            slide_title="Key Features",
            language="en",
        )

        # Validate FormattedSlide structure
        assert "slide_title" in result
        assert "components" in result
        assert len(result["components"]) > 0

        # Check feature-grid component
        feature_comp = result["components"][0]
        assert feature_comp["type"] == "feature-grid"
        assert "slots" in feature_comp
        assert "features" in feature_comp["slots"]
        assert len(feature_comp["slots"]["features"]) > 0

        # Validate feature structure
        first_feature = feature_comp["slots"]["features"][0]
        assert "title" in first_feature
        assert "description" in first_feature

    @pytest.mark.skipif(TEST_MODE, reason="Requires real API key")
    def test_generate_quote_component(self, generator):
        """Test generating quote component"""
        slide_blueprint = {
            "slide_title": "Customer Testimonial",
            "layout_type": "single",
            "components": [
                {
                    "component_id": "comp-1",
                    "type": "quote",
                    "position": "center",
                    "content_block_indices": [0],
                }
            ],
        }

        content_blocks = [
            {
                "type": "quote",
                "content": '"Best analytics tool we\'ve ever used. Saves us hours every week." - John Doe, CTO',
                "priority": "must_have",
            }
        ]

        slide_intent = {
            "intent_type": "use_case",
            "language": "en",
            "density": "low",
        }

        result = generator.generate(
            slide_blueprint=slide_blueprint,
            content_blocks=content_blocks,
            slide_intent=slide_intent,
            slide_title="Customer Testimonial",
            language="en",
        )

        # Validate quote component
        quote_comp = result["components"][0]
        assert quote_comp["type"] == "quote"
        assert "slots" in quote_comp
        assert "quote" in quote_comp["slots"]
        assert len(quote_comp["slots"]["quote"]) > 0

    @pytest.mark.skipif(TEST_MODE, reason="Requires real API key")
    def test_generate_german_content(self, generator):
        """Test generating German language content"""
        slide_blueprint = {
            "slide_title": "Unser Ansatz",
            "layout_type": "single",
            "components": [
                {
                    "component_id": "comp-1",
                    "type": "bullet-list",
                    "position": "center",
                    "content_block_indices": [0],
                }
            ],
        }

        content_blocks = [
            {
                "type": "bullets",
                "content": "- KI-gestützte Datenanalyse\n- Automatisierte Berichte\n- Echtzeit-Dashboards",
                "priority": "must_have",
            }
        ]

        slide_intent = {
            "intent_type": "solution",
            "language": "de",
            "density": "medium",
        }

        result = generator.generate(
            slide_blueprint=slide_blueprint,
            content_blocks=content_blocks,
            slide_intent=slide_intent,
            slide_title="Unser Ansatz",
            language="de",
        )

        # Validate language preservation
        assert result.get("language") == "de"
        bullet_comp = result["components"][0]
        assert "slots" in bullet_comp
        assert "items" in bullet_comp["slots"]


class TestGoogleEndToEnd:
    """End-to-end tests with all 3 Google Gemini agents"""

    @pytest.mark.skipif(TEST_MODE, reason="Requires real API key")
    def test_full_pipeline_english_metrics_slide(self):
        """Test full 3-agent pipeline with English metrics slide"""
        user_input = """Our Q4 Performance
- $10M ARR (up 200% YoY)
- 1,000+ enterprise customers
- 99.9% uptime
- #1 rated support team"""

        # Agent 1: Analyze
        analyzer = ContentAnalyzerAgentGoogle(
            api_key=GOOGLE_API_KEY,
            model="gemini-3.0-pro",
        )
        analysis = analyzer.analyze(user_input)

        assert "slide_intent" in analysis
        assert "content_blocks" in analysis
        assert analysis["slide_intent"]["language"] == "en"

        # Agent 2: Plan
        strategist = PresentationStrategistAgentGoogle(
            api_key=GOOGLE_API_KEY,
            model="gemini-3.0-pro",
        )

        design_system = {
            "max_components": 3,
            "available_components": ["stat-grid", "bullet-list", "text", "quote"],
        }

        blueprint = strategist.plan(
            slide_intent=analysis["slide_intent"],
            content_blocks=analysis["content_blocks"],
            design_system=design_system,
        )

        assert "components" in blueprint
        assert len(blueprint["components"]) > 0

        # Agent 3: Generate
        generator = ContentGeneratorAgentGoogle(
            api_key=GOOGLE_API_KEY,
            model="gemini-2.0-flash",  # Fast model
        )

        formatted_slide = generator.generate(
            slide_blueprint=blueprint,
            content_blocks=analysis["content_blocks"],
            slide_intent=analysis["slide_intent"],
            slide_title="Q4 Performance",
            language="en",
        )

        # Validate final output
        assert "slide_title" in formatted_slide
        assert "components" in formatted_slide
        assert len(formatted_slide["components"]) > 0

        # Check language preservation
        assert formatted_slide.get("language") == "en"

        # Should have stat-grid for metrics
        component_types = [c["type"] for c in formatted_slide["components"]]
        assert "stat-grid" in component_types

        print("\n✅ Full Google Gemini pipeline test passed!")
        print(f"   Slide: {formatted_slide['slide_title']}")
        print(f"   Components: {len(formatted_slide['components'])}")
        print(f"   Types: {component_types}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
