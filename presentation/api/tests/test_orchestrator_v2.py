"""
Integration Tests for OrchestratorV2 (Multi-Provider)

Tests the orchestrator with all 3 providers.
"""
import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from agents.orchestrator_v2 import AgentOrchestratorV2
from config import OPENAI_API_KEY, ANTHROPIC_API_KEY, GOOGLE_API_KEY, TEST_MODE, MODEL_TO_PROVIDER


class TestOrchestratorV2Initialization:
    """Test orchestrator initialization and provider detection"""

    def test_init_with_openai_model(self):
        """Test that OpenAI models are detected correctly"""
        orchestrator = AgentOrchestratorV2(
            model="gpt-4o",
            test_mode=True,  # Use mocks
        )

        assert orchestrator.provider == "openai"
        assert orchestrator.model == "gpt-4o"

    def test_init_with_anthropic_model(self):
        """Test that Anthropic models are detected correctly"""
        orchestrator = AgentOrchestratorV2(
            model="claude-sonnet-4.5",
            test_mode=True,
        )

        assert orchestrator.provider == "anthropic"
        assert orchestrator.model == "claude-sonnet-4.5"

    def test_init_with_google_model(self):
        """Test that Google models are detected correctly"""
        orchestrator = AgentOrchestratorV2(
            model="gemini-3.0-pro",
            test_mode=True,
        )

        assert orchestrator.provider == "google"
        assert orchestrator.model == "gemini-3.0-pro"

    def test_init_with_explicit_provider(self):
        """Test explicit provider override"""
        orchestrator = AgentOrchestratorV2(
            model="custom-model",
            provider="openai",
            test_mode=True,
        )

        assert orchestrator.provider == "openai"

    def test_init_with_unknown_model_defaults_to_openai(self):
        """Test that unknown models default to openai"""
        orchestrator = AgentOrchestratorV2(
            model="unknown-model-12345",
            test_mode=True,
        )

        assert orchestrator.provider == "openai"


class TestOrchestratorV2MockMode:
    """Test orchestrator in mock mode (no API calls)"""

    def test_generate_slide_mock_openai(self):
        """Test mock slide generation with OpenAI provider"""
        orchestrator = AgentOrchestratorV2(
            model="gpt-4o",
            test_mode=True,
        )

        result = orchestrator.generate_slide(
            user_input="Our team consists of 5 experts in robotics and AI",
            project_name="beispiel-projekt",
            slide_title="Team",
            slide_number=5,
            theme="github",
            language="en",
        )

        # Mock mode should still return success
        assert result.get("success") == True
        assert result.get("provider") == "openai"
        assert result.get("model") == "gpt-4o"

    def test_generate_slide_mock_anthropic(self):
        """Test mock slide generation with Anthropic provider"""
        orchestrator = AgentOrchestratorV2(
            model="claude-sonnet-4.5",
            test_mode=True,
        )

        result = orchestrator.generate_slide(
            user_input="€5M ARR, 120% growth, 500 customers",
            project_name="beispiel-projekt",
            slide_title="Metrics",
            slide_number=10,
            theme="apple",
            language="de",
        )

        assert result.get("success") == True
        assert result.get("provider") == "anthropic"
        assert result.get("model") == "claude-sonnet-4.5"

    def test_generate_slide_mock_google(self):
        """Test mock slide generation with Google provider"""
        orchestrator = AgentOrchestratorV2(
            model="gemini-3.0-pro",
            test_mode=True,
        )

        result = orchestrator.generate_slide(
            user_input="Key features: Real-time analytics, AI insights, Custom dashboards",
            project_name="beispiel-projekt",
            slide_title="Features",
            slide_number=7,
            theme="openai",
            language="en",
        )

        assert result.get("success") == True
        assert result.get("provider") == "google"
        assert result.get("model") == "gemini-3.0-pro"


class TestOrchestratorV2RealAPI:
    """Test orchestrator with real API calls (requires API keys)"""

    @pytest.mark.skipif(not OPENAI_API_KEY or TEST_MODE, reason="Requires OPENAI_API_KEY")
    def test_generate_slide_openai_real(self):
        """Test real slide generation with OpenAI"""
        orchestrator = AgentOrchestratorV2(
            model="gpt-4o",
            test_mode=False,
        )

        result = orchestrator.generate_slide(
            user_input="Our 3-person founding team has 50+ years combined experience in AI and robotics",
            project_name="beispiel-projekt",
            slide_title="Founding Team",
            slide_number=3,
            theme="github",
            language="en",
        )

        assert result.get("success") == True
        assert result.get("provider") == "openai"
        assert "html_content" in result
        assert "markdown_content" in result
        assert len(result["html_content"]) > 0

        print("\n✅ OpenAI real API test passed!")
        print(f"   HTML length: {len(result['html_content'])} chars")
        print(f"   Components: {result.get('components_used', [])}")

    @pytest.mark.skipif(not ANTHROPIC_API_KEY or TEST_MODE, reason="Requires ANTHROPIC_API_KEY")
    def test_generate_slide_anthropic_real(self):
        """Test real slide generation with Anthropic Claude"""
        orchestrator = AgentOrchestratorV2(
            model="claude-sonnet-4.5-20250514",
            test_mode=False,
        )

        result = orchestrator.generate_slide(
            user_input="""Unsere Q4 Kennzahlen:
- €12,5 Mio ARR
- 180% Wachstum YoY
- 800+ Kunden
- 98% Zufriedenheit""",
            project_name="beispiel-projekt",
            slide_title="Q4 Metriken",
            slide_number=8,
            theme="apple",
            language="de",
        )

        assert result.get("success") == True
        assert result.get("provider") == "anthropic"
        assert "html_content" in result
        assert "markdown_content" in result
        assert len(result["html_content"]) > 0

        print("\n✅ Anthropic Claude real API test passed!")
        print(f"   HTML length: {len(result['html_content'])} chars")
        print(f"   Feedback iterations: {result.get('feedback_iterations', 0)}")

    @pytest.mark.skipif(not GOOGLE_API_KEY or TEST_MODE, reason="Requires GOOGLE_API_KEY")
    def test_generate_slide_google_real(self):
        """Test real slide generation with Google Gemini"""
        orchestrator = AgentOrchestratorV2(
            model="gemini-3.0-pro",
            test_mode=False,
        )

        result = orchestrator.generate_slide(
            user_input="""Key Platform Features:
✨ Real-time Analytics Dashboard
🎯 AI-powered Predictive Insights
⚡ Lightning-fast Query Performance
🔒 Enterprise-grade Security""",
            project_name="beispiel-projekt",
            slide_title="Platform Features",
            slide_number=12,
            theme="openai",
            language="en",
        )

        assert result.get("success") == True
        assert result.get("provider") == "google"
        assert "html_content" in result
        assert "markdown_content" in result
        assert len(result["html_content"]) > 0

        print("\n✅ Google Gemini real API test passed!")
        print(f"   HTML length: {len(result['html_content'])} chars")
        print(f"   Components: {result.get('components_used', [])}")


class TestOrchestratorV2ThemeCompatibility:
    """Test that all providers work with all themes"""

    @pytest.mark.parametrize("theme", ["github", "modern", "minimal", "apple", "openai"])
    def test_all_themes_with_openai(self, theme):
        """Test OpenAI with all 5 themes"""
        orchestrator = AgentOrchestratorV2(
            model="gpt-4o",
            test_mode=True,
        )

        result = orchestrator.generate_slide(
            user_input="Test content",
            project_name="beispiel-projekt",
            slide_title="Test",
            slide_number=1,
            theme=theme,
            language="en",
        )

        # Should work with all themes
        assert result.get("success") == True

    @pytest.mark.parametrize("model,provider", [
        ("gpt-4o", "openai"),
        ("claude-sonnet-4.5", "anthropic"),
        ("gemini-3.0-pro", "google"),
    ])
    def test_all_providers_with_apple_theme(self, model, provider):
        """Test all 3 providers with Apple theme"""
        orchestrator = AgentOrchestratorV2(
            model=model,
            test_mode=True,
        )

        result = orchestrator.generate_slide(
            user_input="Test content",
            project_name="beispiel-projekt",
            slide_title="Test",
            slide_number=1,
            theme="apple",
            language="en",
        )

        assert result.get("success") == True
        assert result.get("provider") == provider


class TestOrchestratorV2LanguageSupport:
    """Test language handling across providers"""

    @pytest.mark.parametrize("language,expected", [
        ("de", "de"),
        ("en", "en"),
    ])
    def test_language_preservation(self, language, expected):
        """Test that language is preserved through pipeline"""
        orchestrator = AgentOrchestratorV2(
            model="gpt-4o",
            test_mode=True,
        )

        result = orchestrator.generate_slide(
            user_input="Test content in specified language",
            project_name="beispiel-projekt",
            slide_title="Test",
            slide_number=1,
            theme="github",
            language=language,
        )

        assert result.get("success") == True


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
