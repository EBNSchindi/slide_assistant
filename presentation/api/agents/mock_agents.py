"""
Mock Agents for testing without OpenAI API
"""
import json
import random


class MockContentAnalyzerAgent:
    """Mock Content Analyzer for testing"""

    def __init__(self, api_key: str = None, model: str = "mock"):
        self.model = model

    def analyze(self, user_input: str, slide_title: str = None, project_scope: str = "") -> dict:
        """Mock analysis of user input

        Args:
            user_input: The content to analyze
            slide_title: Optional slide title
            project_scope: Project scope/context (optional)
        """
        # Determine content type based on keywords
        content_type = "mixed"
        if any(word in user_input.lower() for word in ["€", "%", "million", "mio"]):
            content_type = "statistics"
        elif any(word in user_input.lower() for word in ["list", "bullet", "point"]):
            content_type = "list"
        elif any(word in user_input.lower() for word in ["quote", "say", "said"]):
            content_type = "quote"
        elif any(word in user_input.lower() for word in ["problem", "challenge"]):
            content_type = "narrative"

        return {
            "content_type": content_type,
            "key_messages": ["Message 1", "Message 2", "Message 3"],
            "raw_content": user_input,
            "has_statistics": "€" in user_input or "%" in user_input,
            "has_lists": "-" in user_input or "•" in user_input,
            "has_quotes": '"' in user_input,
            "formatting_preferences": ["clean", "modern"],
            "project_context_available": bool(project_scope),
        }


class MockPresentationStrategistAgent:
    """Mock Presentation Strategist for testing"""

    def __init__(self, api_key: str = None, model: str = "mock"):
        self.model = model

    def recommend(
        self, analysis: dict, style_guide: dict, preferences: dict = None, project_scope: str = ""
    ) -> dict:
        """Mock strategy recommendation

        Args:
            analysis: Content analysis from ContentAnalyzerAgent
            style_guide: Project style guide
            preferences: Optional user preferences
            project_scope: Project scope/context (optional)
        """
        available_components = style_guide.get("available_components", [])
        component_count = min(
            len([c for c in available_components if c in ["stat-grid", "bullet-list"]]) or 2,
            3,
        )

        return {
            "recommended_components": [
                {
                    "type": "bullet-list",
                    "content_indices": [0, 1, 2],
                    "layout_position": "middle",
                },
            ],
            "component_count": component_count,
            "layout_strategy": "Center-aligned with clear hierarchy",
            "styling_suggestions": [
                f"Use primary color {style_guide.get('primary_color')}",
                "Apply 16px spacing",
            ],
            "reasoning": "Simple, clean layout that respects design system",
            "scope_aware": bool(project_scope),
        }


class MockContentGeneratorAgent:
    """Mock Content Generator for testing"""

    def __init__(self, api_key: str = None, model: str = "mock"):
        self.model = model

    def generate(
        self,
        analysis: dict,
        strategy: dict,
        style_guide: dict,
        slide_title: str = "Folie",
        project_scope: str = "",
        image_references: list = None,
        project_name: str = "beispiel-projekt",
        generate_variants: bool = False,
        variant_profiles: list = None,
    ) -> dict:
        """Mock content generation

        Args:
            analysis: Content analysis
            strategy: Strategy recommendations
            style_guide: Style guide information
            slide_title: Title for the slide
            project_scope: Project scope/context (optional)
            image_references: List of image filenames to include (optional)
            project_name: Name of the project for dynamic paths
            generate_variants: Whether to generate 3 design variants
            variant_profiles: List of variant profile dicts (optional)
        """
        # DEBUG: Log image references and variant generation
        print("\n" + "="*50)
        print("=== DEBUG MOCK AGENT GENERATOR ===")
        print(f"generate_variants: {generate_variants}")
        print(f"variant_profiles: {variant_profiles}")
        print(f"image_references: {image_references}")
        if image_references:
            print(f"✅ Image count: {len(image_references)}")
        print("="*50 + "\n")

        # If variants requested, generate all 3
        if generate_variants and variant_profiles:
            variants = []

            for profile in variant_profiles:
                profile_name = profile.get("name", "default")
                primary_color = profile.get("primary_color", "#238636")

                # Generate profile-specific markdown
                markdown = f"""# {slide_title} ({profile_name.title()})

## Komponente 1: Inhalt

- Punkt 1
- Punkt 2
- Punkt 3

## Komponente 2: Details

- Detail A
- Detail B
"""

                # Generate profile-specific HTML
                html_parts = [f"""<div class="slide-section">
  <div class="component" id="slide-1-comp-1" style="border: 2px solid {primary_color}; padding: 20px; margin-bottom: 20px;">
    <div class="component-label">{profile_name.title()} - Komponente 1</div>
    <h2 style="color: {primary_color};">{slide_title}</h2>
    <ul class="bullet-list">
      <li>Punkt 1</li>
      <li>Punkt 2</li>
      <li>Punkt 3</li>
    </ul>
  </div>
  <div class="component" id="slide-1-comp-2" style="border: 2px solid {primary_color}; padding: 20px;">
    <div class="component-label">{profile_name.title()} - Komponente 2</div>
    <h2 style="color: {primary_color};">Details</h2>
    <ul class="bullet-list">
      <li>Detail A</li>
      <li>Detail B</li>
    </ul>
  </div>"""]

                # Add images if provided
                if image_references:
                    for i, img_filename in enumerate(image_references):
                        html_parts.append(f"""
  <div class="component image-component" id="slide-1-img-{i+1}" style="border: 2px solid {primary_color}; padding: 10px;">
    <div class="component-label">{profile_name.title()} - Image {i+1}</div>
    <img src="projects/{project_name}/images/uploads/{img_filename}" alt="Slide image {i+1}" class="slide-image" />
  </div>""")

                html_parts.append("\n</div>")
                html = "".join(html_parts)

                components_used = ["bullet-list", "text"]
                if image_references:
                    components_used.append("image")

                variants.append({
                    "profile": profile_name,
                    "html_content": html,
                    "markdown_content": markdown,
                    "components_used": components_used,
                })

            return {
                "variants": variants,
                "component_count": 2 + (len(image_references) if image_references else 0),
                "used_project_scope": bool(project_scope),
                "images_included": len(image_references) if image_references else 0,
            }

        # Original single-variant generation
        markdown = f"""# {slide_title}

## Komponente 1: Inhalt

- Punkt 1
- Punkt 2
- Punkt 3

## Komponente 2: Details

- Detail A
- Detail B
"""

        # Generate simple HTML
        html_parts = [f"""<div class="slide-section">
  <div class="component" id="slide-1-comp-1">
    <div class="component-label">Komponente 1</div>
    <h2>{slide_title}</h2>
    <ul class="bullet-list">
      <li>Punkt 1</li>
      <li>Punkt 2</li>
      <li>Punkt 3</li>
    </ul>
  </div>
  <div class="component" id="slide-1-comp-2">
    <div class="component-label">Komponente 2</div>
    <h2>Details</h2>
    <ul class="bullet-list">
      <li>Detail A</li>
      <li>Detail B</li>
    </ul>
  </div>"""]

        # Add images if provided
        if image_references:
            for i, img_filename in enumerate(image_references):
                html_parts.append(f"""
  <div class="component image-component" id="slide-1-img-{i+1}">
    <div class="component-label">Image {i+1}</div>
    <img src="projects/{project_name}/images/uploads/{img_filename}" alt="Slide image {i+1}" class="slide-image" />
  </div>""")

        html_parts.append("\n</div>")
        html = "".join(html_parts)

        components_used = ["bullet-list", "text"]
        if image_references:
            components_used.append("image")

        return {
            "markdown": markdown,
            "html": html,
            "component_count": 2 + (len(image_references) if image_references else 0),
            "components_used": components_used,
            "used_project_scope": bool(project_scope),
            "images_included": len(image_references) if image_references else 0,
        }
