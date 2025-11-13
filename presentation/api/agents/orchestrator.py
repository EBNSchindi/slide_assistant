"""
Agent Orchestrator - Coordinates the multi-agent chain
"""
import sys
import os

# Import services - use absolute imports when running from main
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import TEST_MODE

if TEST_MODE:
    from .mock_agents import (
        MockContentAnalyzerAgent as ContentAnalyzerAgent,
        MockPresentationStrategistAgent as PresentationStrategistAgent,
        MockContentGeneratorAgent as ContentGeneratorAgent,
    )
else:
    from .content_analyzer import ContentAnalyzerAgent
    from .presentation_strategist import PresentationStrategistAgent
    from .content_generator import ContentGeneratorAgent

from services import StyleParser, FileService, ProjectService


class AgentOrchestrator:
    """Orchestrates the multi-agent content generation pipeline"""

    def __init__(self, api_key: str = None, model: str = "gpt-4o", test_mode: bool = False):
        self.api_key = api_key
        self.model = model
        self.test_mode = test_mode or TEST_MODE

        # Initialize agents
        self.content_analyzer = ContentAnalyzerAgent(api_key, model)
        self.presentation_strategist = PresentationStrategistAgent(api_key, model)
        self.content_generator = ContentGeneratorAgent(api_key, model)

    def process(
        self,
        user_input: str,
        project_path: str,
        slide_title: str = None,
        preferences: dict = None,
    ) -> dict:
        """Process user input through the full agent chain"""

        steps = []
        slides = []

        try:
            # Step 1: Content Analysis
            step1 = {
                "agent_name": "Content Analyzer",
                "status": "processing",
                "output": None,
                "error": None,
            }
            steps.append(step1)

            analysis = self.content_analyzer.analyze(user_input, slide_title)
            step1["status"] = "completed"
            step1["output"] = f"Identified content type: {analysis.get('content_type')}"

            # Step 2: Load Style Guide
            style_parser = StyleParser(project_path)
            style_guide = style_parser.parse_project_style()

            # Step 3: Presentation Strategy
            step2 = {
                "agent_name": "Presentation Strategist",
                "status": "processing",
                "output": None,
                "error": None,
            }
            steps.append(step2)

            strategy = self.presentation_strategist.recommend(
                analysis, style_guide, preferences
            )
            step2["status"] = "completed"
            step2[
                "output"
            ] = f"Recommended {strategy.get('component_count', 1)} components"

            # Step 4: Content Generation
            step3 = {
                "agent_name": "Content Generator",
                "status": "processing",
                "output": None,
                "error": None,
            }
            steps.append(step3)

            generated = self.content_generator.generate(
                analysis, strategy, style_guide, slide_title or "Folie"
            )
            step3["status"] = "completed"
            step3["output"] = f"Generated {generated.get('component_count', 1)} components"

            # Step 5: Save Files
            file_service = FileService(project_path)

            slide_name = self._sanitize_slide_name(
                slide_title or f"folie-{len(file_service.list_slides()['markdown']) + 1}"
            )

            markdown_path = file_service.save_markdown_slide(
                slide_name, generated.get("markdown", "")
            )
            html_path = file_service.save_html_slide(
                slide_name, generated.get("html", "")
            )

            slide_result = {
                "slide_name": slide_name,
                "slide_title": slide_title or slide_name,
                "markdown_path": markdown_path,
                "html_path": html_path,
                "components": generated.get("components_used", []),
                "html_content": generated.get("html", ""),
                "markdown_content": generated.get("markdown", ""),
            }
            slides.append(slide_result)

            return {
                "success": True,
                "agent_steps": steps,
                "generated_slides": slides,
                "message": "Content successfully generated",
                "total_components": sum(
                    len(s.get("components", [])) for s in slides
                ),
            }

        except Exception as e:
            # Mark the current step as failed
            if steps:
                steps[-1]["status"] = "error"
                steps[-1]["error"] = str(e)

            return {
                "success": False,
                "agent_steps": steps,
                "generated_slides": slides,
                "message": f"Generation failed: {str(e)}",
                "error": str(e),
            }

    def _sanitize_slide_name(self, name: str) -> str:
        """Sanitize slide name"""
        import re

        # Remove invalid characters
        name = re.sub(r"[<>:\"/\\|?*]", "", name)
        # Replace spaces with hyphens
        name = name.replace(" ", "-")
        # Convert to lowercase
        name = name.lower()
        # Remove leading/trailing hyphens
        name = name.strip("-")

        return name
