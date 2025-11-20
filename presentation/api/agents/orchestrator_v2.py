"""
Agent Orchestrator V2 - Multi-Provider Support (OpenAI, Anthropic, Google)

Coordinates the multi-agent chain with dynamic provider selection.
"""
import sys
import os

# Import services - use absolute imports when running from main
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import TEST_MODE, MODEL_TO_PROVIDER, OPENAI_API_KEY, ANTHROPIC_API_KEY, GOOGLE_API_KEY

# Import V2 agents based on provider
from .content_analyzer_v2 import ContentAnalyzerAgentV2
from .presentation_strategist_v2 import PresentationStrategistAgentV2
from .content_generator_v2 import ContentGeneratorAgentV2

# Import provider-specific agents
try:
    from .content_analyzer_anthropic import ContentAnalyzerAgentAnthropic
    from .presentation_strategist_anthropic import PresentationStrategistAgentAnthropic
    from .content_generator_anthropic import ContentGeneratorAgentAnthropic
except ImportError:
    print("⚠️ Anthropic agents not available")
    ContentAnalyzerAgentAnthropic = None
    PresentationStrategistAgentAnthropic = None
    ContentGeneratorAgentAnthropic = None

try:
    from .content_analyzer_google import ContentAnalyzerAgentGoogle
    from .presentation_strategist_google import PresentationStrategistAgentGoogle
    from .content_generator_google import ContentGeneratorAgentGoogle
except ImportError:
    print("⚠️ Google agents not available")
    ContentAnalyzerAgentGoogle = None
    PresentationStrategistAgentGoogle = None
    ContentGeneratorAgentGoogle = None

# Import mock agents for testing
if TEST_MODE:
    from .mock_agents_v2 import (
        MockContentAnalyzerAgentV2 as MockContentAnalyzer,
        MockPresentationStrategistAgentV2 as MockStrategist,
        MockContentGeneratorAgentV2 as MockGenerator,
    )

from services import StyleParser, FileService
from renderers.component_renderer import HTMLComponentRenderer


class AgentOrchestratorV2:
    """Orchestrates the V2 multi-agent content generation pipeline with multi-provider support"""

    def __init__(
        self,
        api_key: str = None,
        model: str = "gpt-4o",
        test_mode: bool = False,
        reasoning_effort: str = None,
        verbosity: str = None,
        use_structured_outputs: bool = False,
        provider: str = None,
    ):
        """
        Initialize orchestrator with provider detection

        Args:
            api_key: API key (can be None, will be auto-selected based on provider)
            model: Model name (e.g., gpt-4o, claude-sonnet-4.5, gemini-3.0-pro)
            test_mode: Use mock agents for testing
            reasoning_effort: Reasoning effort level (minimal, low, medium, high)
            verbosity: Output verbosity (minimal, low, medium, high)
            use_structured_outputs: Enable Pydantic structured outputs
            provider: Override provider detection (openai|anthropic|google)
        """
        self.model = model
        self.test_mode = test_mode or TEST_MODE
        self.reasoning_effort = reasoning_effort or "medium"
        self.verbosity = verbosity or "medium"
        self.use_structured_outputs = use_structured_outputs

        # Auto-detect provider from model name
        if provider is None:
            provider = MODEL_TO_PROVIDER.get(model, "openai")
        self.provider = provider

        # Auto-select API key based on provider
        if api_key is None:
            if provider == "openai":
                api_key = OPENAI_API_KEY
            elif provider == "anthropic":
                api_key = ANTHROPIC_API_KEY
            elif provider == "google":
                api_key = GOOGLE_API_KEY
            else:
                raise ValueError(f"Unknown provider: {provider}")

        if not api_key and not self.test_mode:
            raise ValueError(f"API key required for provider: {provider}")

        self.api_key = api_key

        # Initialize agents based on provider
        if self.test_mode:
            print(f"🧪 TEST MODE: Using mock agents")
            self.content_analyzer = MockContentAnalyzer()
            self.presentation_strategist = MockStrategist()
            self.content_generator = MockGenerator()
        else:
            self._initialize_agents()

    def _initialize_agents(self):
        """Initialize agents based on provider"""
        print(f"🤖 Initializing {self.provider} agents with model: {self.model}")

        if self.provider == "openai":
            self.content_analyzer = ContentAnalyzerAgentV2(
                api_key=self.api_key,
                model=self.model,
                reasoning_effort=self.reasoning_effort,
                verbosity=self.verbosity,
                use_structured_outputs=self.use_structured_outputs,
            )
            self.presentation_strategist = PresentationStrategistAgentV2(
                api_key=self.api_key,
                model=self.model,
                reasoning_effort="high",  # Strategy needs high reasoning
                verbosity=self.verbosity,
                use_structured_outputs=self.use_structured_outputs,
            )
            self.content_generator = ContentGeneratorAgentV2(
                api_key=self.api_key,
                model=self.model,
                reasoning_effort=self.reasoning_effort,
                verbosity=self.verbosity,
                use_structured_outputs=self.use_structured_outputs,
            )

        elif self.provider == "anthropic":
            if not ContentAnalyzerAgentAnthropic:
                raise ImportError("Anthropic agents not available")
            self.content_analyzer = ContentAnalyzerAgentAnthropic(
                api_key=self.api_key,
                model=self.model,
                reasoning_effort=self.reasoning_effort,
                verbosity=self.verbosity,
                use_structured_outputs=self.use_structured_outputs,
            )
            self.presentation_strategist = PresentationStrategistAgentAnthropic(
                api_key=self.api_key,
                model=self.model,
                reasoning_effort="high",
                verbosity=self.verbosity,
                use_structured_outputs=self.use_structured_outputs,
            )
            self.content_generator = ContentGeneratorAgentAnthropic(
                api_key=self.api_key,
                model=self.model,
                reasoning_effort=self.reasoning_effort,
                verbosity=self.verbosity,
                use_structured_outputs=self.use_structured_outputs,
            )

        elif self.provider == "google":
            if not ContentAnalyzerAgentGoogle:
                raise ImportError("Google agents not available")
            self.content_analyzer = ContentAnalyzerAgentGoogle(
                api_key=self.api_key,
                model=self.model,
                reasoning_effort=self.reasoning_effort,
                verbosity=self.verbosity,
                use_structured_outputs=self.use_structured_outputs,
            )
            self.presentation_strategist = PresentationStrategistAgentGoogle(
                api_key=self.api_key,
                model=self.model,
                reasoning_effort="high",
                verbosity=self.verbosity,
                use_structured_outputs=self.use_structured_outputs,
            )
            self.content_generator = ContentGeneratorAgentGoogle(
                api_key=self.api_key,
                model=self.model,
                reasoning_effort=self.reasoning_effort,
                verbosity=self.verbosity,
                use_structured_outputs=self.use_structured_outputs,
            )

        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    def generate_slide(
        self,
        user_input: str,
        project_name: str,
        slide_title: str,
        slide_number: int,
        theme: str = "github",
        language: str = "de",
        image_references: list = None,
    ) -> dict:
        """
        Generate a slide using V2 deterministic pipeline

        Args:
            user_input: User's raw content input
            project_name: Project name (for paths)
            slide_title: Title of the slide
            slide_number: Slide number
            theme: Theme name (github, modern, minimal, apple, openai)
            language: Output language (de, en)
            image_references: List of image filenames

        Returns:
            dict with success, html_content, markdown_content, etc.
        """
        try:
            print(f"\n{'='*60}")
            print(f"🎬 AGENT ORCHESTRATOR V2 - {self.provider.upper()}")
            print(f"   Model: {self.model}")
            print(f"   Theme: {theme}")
            print(f"   Language: {language}")
            print(f"{'='*60}\n")

            # Step 1: Content Analysis
            print("📊 STEP 1: Content Analysis...")
            analysis_result = self.content_analyzer.analyze(user_input)
            slide_intent = analysis_result.get("slide_intent", {})
            content_blocks = analysis_result.get("content_blocks", [])
            print(f"   ✓ Intent: {slide_intent.get('intent_type')}")
            print(f"   ✓ Blocks: {len(content_blocks)}")
            print(f"   ✓ Language: {slide_intent.get('language', 'unknown')}")

            # Step 2: Load Design System
            print("\n🎨 STEP 2: Loading Design System...")
            project_path = os.path.join(
                os.path.dirname(__file__), "..", "..", "projects", project_name
            )
            style_parser = StyleParser(project_path, theme_name=theme)
            design_guide = style_parser.load_design_guide()
            print(f"   ✓ Theme: {design_guide.get('theme', theme)}")

            # Step 3: Presentation Strategy
            print("\n🧩 STEP 3: Planning Layout...")
            image_metadata = {"images": image_references or []}
            blueprint = self.presentation_strategist.plan(
                slide_intent=slide_intent,
                content_blocks=content_blocks,
                design_system=design_guide,
                image_metadata=image_metadata,
            )
            print(f"   ✓ Layout: {blueprint.get('layout_type')}")
            print(f"   ✓ Components: {len(blueprint.get('components', []))}")

            # Step 4: Content Generation (with feedback loop)
            print("\n✍️ STEP 4: Generating Content...")
            max_feedback_iterations = 2
            feedback_count = 0

            while feedback_count < max_feedback_iterations:
                formatted_slide = self.content_generator.generate(
                    slide_blueprint=blueprint,
                    content_blocks=content_blocks,
                    slide_intent=slide_intent,
                    slide_title=slide_title,
                    language=language,
                )

                # Check for validation issues
                validation_feedback = formatted_slide.get("validation_feedback")
                if validation_feedback and validation_feedback.get("needs_replanning"):
                    print(f"\n⚠️ Validation issue detected, replanning... (iteration {feedback_count + 1})")
                    blueprint = self.presentation_strategist.replan(
                        original_blueprint=blueprint,
                        feedback=validation_feedback,
                    )
                    feedback_count += 1
                else:
                    break

            print(f"   ✓ Content generated (feedback loops: {feedback_count})")

            # Step 5: Render HTML
            print("\n🎨 STEP 5: Rendering HTML...")
            renderer = HTMLComponentRenderer(theme_name=theme, project_name=project_name)
            html_content = renderer.render_slide(formatted_slide)
            print(f"   ✓ HTML rendered ({len(html_content)} chars)")

            # Step 6: Generate Markdown
            print("\n📝 STEP 6: Generating Markdown...")
            markdown_content = self._generate_markdown(formatted_slide, slide_title)
            print(f"   ✓ Markdown generated ({len(markdown_content)} chars)")

            # Step 7: Save files
            print("\n💾 STEP 7: Saving files...")
            file_service = FileService(project_path)
            slide_name = self._sanitize_slide_name(slide_title)

            markdown_path = file_service.save_markdown_slide(slide_name, markdown_content)
            html_path = file_service.save_html_slide(slide_name, html_content)

            print(f"   ✓ Markdown: {markdown_path}")
            print(f"   ✓ HTML: {html_path}")

            print(f"\n{'='*60}")
            print("✅ SLIDE GENERATION COMPLETE")
            print(f"{'='*60}\n")

            return {
                "success": True,
                "provider": self.provider,
                "model": self.model,
                "slide_title": slide_title,
                "html_content": html_content,
                "markdown_content": markdown_content,
                "markdown_path": markdown_path,
                "html_path": html_path,
                "components_used": [
                    comp.get("type") for comp in formatted_slide.get("components", [])
                ],
                "feedback_iterations": feedback_count,
            }

        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}")
            import traceback
            traceback.print_exc()

            return {
                "success": False,
                "error": str(e),
                "provider": self.provider,
                "model": self.model,
            }

    def _generate_markdown(self, formatted_slide: dict, slide_title: str) -> str:
        """Generate markdown representation of the slide"""
        lines = [f"# {slide_title}\n"]

        for component in formatted_slide.get("components", []):
            comp_type = component.get("type")
            slots = component.get("slots", {})

            if comp_type == "stat-grid":
                stats = slots.get("stats", [])
                for stat in stats:
                    lines.append(f"**{stat.get('value')}** - {stat.get('label')}")
                lines.append("")

            elif comp_type == "bullet-list":
                items = slots.get("items", [])
                for item in items:
                    lines.append(f"- {item}")
                lines.append("")

            elif comp_type == "text":
                lines.append(slots.get("content", ""))
                lines.append("")

            elif comp_type == "quote":
                quote_text = slots.get("quote", "")
                author = slots.get("author", "")
                lines.append(f"> {quote_text}")
                if author:
                    lines.append(f"> — {author}")
                lines.append("")

            elif comp_type == "table":
                table_markdown = slots.get("table_markdown", "")
                lines.append(table_markdown)
                lines.append("")

            elif comp_type == "image-frame":
                src = slots.get("src", "")
                alt = slots.get("alt", "")
                lines.append(f"![{alt}]({src})")
                caption = slots.get("caption")
                if caption:
                    lines.append(f"*{caption}*")
                lines.append("")

        return "\n".join(lines)

    def _sanitize_slide_name(self, name: str) -> str:
        """Sanitize slide name for filesystem"""
        import re
        name = re.sub(r"[<>:\"/\\|?*]", "", name)
        name = name.replace(" ", "-")
        name = name.lower()
        name = name.strip("-")
        return name
