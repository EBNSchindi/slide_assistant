"""
Integration Tests for Anthropic Claude Agents

Tests all 3 Anthropic agents with mock and real API calls.
"""
import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from agents.content_analyzer_anthropic import ContentAnalyzerAgentAnthropic
from agents.presentation_strategist_anthropic import PresentationStrategistAgentAnthropic
from agents.content_generator_anthropic import ContentGeneratorAgentAnthropic
from config import ANTHROPIC_API_KEY, TEST_MODE


# Skip tests if no API key available
pytestmark = pytest.mark.skipif(
    not ANTHROPIC_API_KEY and not TEST_MODE,
    reason="ANTHROPIC_API_KEY not set and not in TEST_MODE"
)


class TestContentAnalyzerAnthropic:
    """Test Anthropic Content Analyzer Agent"""

    @pytest.fixture
    def analyzer(self):
        """Create analyzer instance"""
        return ContentAnalyzerAgentAnthropic(
            api_key=ANTHROPIC_API_KEY or "test-key",
            model="claude-sonnet-4.5-20250514",
        )

    def test_analyzer_initialization(self, analyzer):
        """Test that analyzer initializes correctly"""
        assert analyzer.model_name == "claude-sonnet-4.5-20250514"
        assert analyzer.client is not None

    @pytest.mark.skipif(TEST_MODE, reason="Requires real API key")
    def test_analyze_team_slide_german(self, analyzer):
        """Test analyzing German team slide content"""
        user_input = """Unser 5-köpfiges Team
- Gründer: 20 Jahre Erfahrung Robotik
- CTO: PhD KI, vorher Google
- Drei weitere Robotik-Experten
Standorte: Berlin & München"""

        result = analyzer.analyze(user_input)

        # Validate structure
        assert "slide_intent" in result
        assert "content_blocks" in result

        slide_intent = result["slide_intent"]
        assert slide_intent["language"] == "de"
        assert slide_intent["intent_type"] in ["team", "other"]
        assert "density" in slide_intent

        content_blocks = result["content_blocks"]
        assert len(content_blocks) > 0
        assert any(block["type"] in ["statistic", "bullets", "statement"] for block in content_blocks)

    @pytest.mark.skipif(TEST_MODE, reason="Requires real API key")
    def test_analyze_statistics_english(self, analyzer):
        """Test analyzing English statistics content"""
        user_input = """Our Growth Metrics
- €5M ARR
- 120% YoY Growth
- 500+ Customers
- 95% Retention Rate"""

        result = analyzer.analyze(user_input)

        slide_intent = result["slide_intent"]
        assert slide_intent["language"] == "en"
        assert slide_intent["intent_type"] in ["kpi", "metrics", "other"]

        content_blocks = result["content_blocks"]
        # Should detect statistics
        stat_blocks = [b for b in content_blocks if b["type"] in ["statistic", "statistics"]]
        assert len(stat_blocks) > 0

    @pytest.mark.skipif(TEST_MODE, reason="Requires real API key")
    def test_analyze_markdown_table(self, analyzer):
        """Test that markdown tables are detected correctly"""
        user_input = """Pricing Comparison

| Plan | Price | Features |
|------|-------|----------|
| Basic | $10/mo | 5 users |
| Pro | $50/mo | 50 users |
| Enterprise | Custom | Unlimited |"""

        result = analyzer.analyze(user_input)

        content_blocks = result["content_blocks"]
        # Should have a markdown_table type block
        table_blocks = [b for b in content_blocks if b["type"] == "markdown_table"]
        assert len(table_blocks) > 0
        assert "| Plan |" in table_blocks[0]["content"]


class TestPresentationStrategistAnthropic:
    """Test Anthropic Presentation Strategist Agent"""

    @pytest.fixture
    def strategist(self):
        """Create strategist instance"""
        return PresentationStrategistAgentAnthropic(
            api_key=ANTHROPIC_API_KEY or "test-key",
            model="claude-sonnet-4.5-20250514",
        )

    def test_strategist_initialization(self, strategist):
        """Test that strategist initializes correctly"""
        assert strategist.model_name == "claude-sonnet-4.5-20250514"
        assert strategist.client is not None

    @pytest.mark.skipif(TEST_MODE, reason="Requires real API key")
    def test_plan_stat_grid_layout(self, strategist):
        """Test planning layout for statistics"""
        slide_intent = {
            "intent_type": "kpi",
            "primary_message": "Show our growth metrics",
            "language": "en",
            "density": "medium",
        }

        content_blocks = [
            {"type": "statistics", "content": "€5M ARR, 120% Growth, 500 Customers", "priority": "must_have"},
        ]

        design_system = {
            "max_components": 3,
            "available_components": ["stat-grid", "bullet-list", "text", "quote"],
        }

        blueprint = strategist.plan(
            slide_intent=slide_intent,
            content_blocks=content_blocks,
            design_system=design_system,
        )

        # Validate blueprint structure
        assert "components" in blueprint
        assert len(blueprint["components"]) > 0

        # Should recommend stat-grid for statistics
        component_types = [c["type"] for c in blueprint["components"]]
        assert "stat-grid" in component_types

    @pytest.mark.skipif(TEST_MODE, reason="Requires real API key")
    def test_replan_with_feedback(self, strategist):
        """Test replanning based on feedback"""
        original_blueprint = {
            "slide_title": "Team",
            "layout_type": "single",
            "components": [
                {
                    "component_id": "comp-1",
                    "type": "bullet-list",
                    "position": "center",
                    "content_block_indices": [0, 1, 2],
                }
            ],
        }

        feedback = {
            "needs_replanning": True,
            "issue": "Too much content for single bullet-list",
            "suggested_changes": {"split_into_two_components": True},
        }

        adjusted_blueprint = strategist.replan(
            original_blueprint=original_blueprint,
            feedback=feedback,
        )

        # Should return a blueprint (structure may vary based on LLM decision)
        assert "components" in adjusted_blueprint
        assert isinstance(adjusted_blueprint["components"], list)


class TestContentGeneratorAnthropic:
    """Test Anthropic Content Generator Agent"""

    @pytest.fixture
    def generator(self):
        """Create generator instance"""
        return ContentGeneratorAgentAnthropic(
            api_key=ANTHROPIC_API_KEY or "test-key",
            model="claude-sonnet-4.5-20250514",
        )

    def test_generator_initialization(self, generator):
        """Test that generator initializes correctly"""
        assert generator.model_name == "claude-sonnet-4.5-20250514"
        assert generator.client is not None

    @pytest.mark.skipif(TEST_MODE, reason="Requires real API key")
    def test_generate_stat_grid(self, generator):
        """Test generating stat-grid component"""
        slide_blueprint = {
            "slide_title": "Growth Metrics",
            "layout_type": "single",
            "components": [
                {
                    "component_id": "comp-1",
                    "type": "stat-grid",
                    "position": "center",
                    "content_block_indices": [0],
                }
            ],
        }

        content_blocks = [
            {
                "type": "statistics",
                "content": "€5M ARR, 120% Growth, 500 Customers",
                "priority": "must_have",
            }
        ]

        slide_intent = {
            "intent_type": "kpi",
            "language": "en",
            "density": "medium",
        }

        result = generator.generate(
            slide_blueprint=slide_blueprint,
            content_blocks=content_blocks,
            slide_intent=slide_intent,
            slide_title="Growth Metrics",
            language="en",
        )

        # Validate FormattedSlide structure
        assert "slide_title" in result
        assert "components" in result
        assert len(result["components"]) > 0

        # Check stat-grid component
        stat_comp = result["components"][0]
        assert stat_comp["type"] == "stat-grid"
        assert "slots" in stat_comp
        assert "stats" in stat_comp["slots"]
        assert len(stat_comp["slots"]["stats"]) > 0

        # Validate stat structure
        first_stat = stat_comp["slots"]["stats"][0]
        assert "value" in first_stat
        assert "label" in first_stat

    @pytest.mark.skipif(TEST_MODE, reason="Requires real API key")
    def test_generate_bullet_list(self, generator):
        """Test generating bullet-list component"""
        slide_blueprint = {
            "slide_title": "Key Features",
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
                "content": "- Real-time Analytics\n- AI-powered Insights\n- Custom Dashboards",
                "priority": "must_have",
            }
        ]

        slide_intent = {
            "intent_type": "solution",
            "language": "en",
            "density": "low",
        }

        result = generator.generate(
            slide_blueprint=slide_blueprint,
            content_blocks=content_blocks,
            slide_intent=slide_intent,
            slide_title="Key Features",
            language="en",
        )

        # Validate bullet-list component
        bullet_comp = result["components"][0]
        assert bullet_comp["type"] == "bullet-list"
        assert "slots" in bullet_comp
        assert "items" in bullet_comp["slots"]
        assert len(bullet_comp["slots"]["items"]) >= 3


class TestAnthropicEndToEnd:
    """End-to-end tests with all 3 Anthropic agents"""

    @pytest.mark.skipif(TEST_MODE, reason="Requires real API key")
    def test_full_pipeline_german_team_slide(self):
        """Test full 3-agent pipeline with German team slide"""
        user_input = """Unser 5-köpfiges Team
- Gründer: 20 Jahre Erfahrung Robotik
- CTO: PhD KI, vorher Google
- Drei weitere Robotik-Experten
Standorte: Berlin & München"""

        # Agent 1: Analyze
        analyzer = ContentAnalyzerAgentAnthropic(
            api_key=ANTHROPIC_API_KEY,
            model="claude-sonnet-4.5-20250514",
        )
        analysis = analyzer.analyze(user_input)

        assert "slide_intent" in analysis
        assert "content_blocks" in analysis
        assert analysis["slide_intent"]["language"] == "de"

        # Agent 2: Plan
        strategist = PresentationStrategistAgentAnthropic(
            api_key=ANTHROPIC_API_KEY,
            model="claude-sonnet-4.5-20250514",
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
        generator = ContentGeneratorAgentAnthropic(
            api_key=ANTHROPIC_API_KEY,
            model="claude-sonnet-4.5-20250514",
        )

        formatted_slide = generator.generate(
            slide_blueprint=blueprint,
            content_blocks=analysis["content_blocks"],
            slide_intent=analysis["slide_intent"],
            slide_title="Unser Team",
            language="de",
        )

        # Validate final output
        assert "slide_title" in formatted_slide
        assert "components" in formatted_slide
        assert len(formatted_slide["components"]) > 0

        # Check language preservation
        assert formatted_slide.get("language") == "de"

        print("\n✅ Full Anthropic pipeline test passed!")
        print(f"   Slide: {formatted_slide['slide_title']}")
        print(f"   Components: {len(formatted_slide['components'])}")
        print(f"   Types: {[c['type'] for c in formatted_slide['components']]}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
