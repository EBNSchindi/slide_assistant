"""
Content Generator Agent (Google Gemini) - Generates final formatted text for slide components

Agent 3 of 3 in the new pipeline (Google Gemini version):
- Input: SlideBlueprint (layout plan) + ContentBlocks
- Output: FormattedSlide (fully formatted text) OR ValidationResult (feedback for replan)
- Job: Write the actual text for each component, with validation and feedback loop support
- Provider: Google Generative AI (Gemini)
"""

import google.generativeai as genai
from typing import List, Dict, Any, Union, Optional
import json
import sys
import os

# Handle imports robustly
try:
    from schemas.blueprint import FormattedSlide, FormattedComponentData, ValidationResult, ValidationWarning
except ImportError:
    from ..schemas.blueprint import FormattedSlide, FormattedComponentData, ValidationResult, ValidationWarning


class ContentGeneratorAgentGoogle:
    """Generates final formatted text for slide components with feedback loop support (Google Gemini)"""

    def __init__(
        self,
        api_key: str,
        model: str = "gemini-2.0-flash",
        reasoning_effort: str = "medium",
        verbosity: str = "medium",
        use_structured_outputs: bool = False,
    ):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)
        self.model_name = model
        self.reasoning_effort = reasoning_effort
        self.verbosity = verbosity
        self.use_structured_outputs = use_structured_outputs

        self.system_prompt = """
═══════════════════════════════════════════════════════════
🎯 AGENT 3: CONTENT GENERATOR
═══════════════════════════════════════════════════════════

YOUR JOB: Write the actual final text for each component.

INPUT:
- SlideBlueprint (from Agent 2): Component layout plan
- ContentBlocks (from Agent 1): Raw content to work with

OUTPUT:
- FormattedSlide: Fully formatted text for each component
- OR ValidationResult: Feedback if content doesn't fit (for retry loop)

DO NOT: Generate HTML, styling, or layout. Just beautiful, concise text.

═══════════════════════════════════════════════════════════
✍️ YOUR JOB FOR EACH COMPONENT
═══════════════════════════════════════════════════════════

stat-grid:
- Write clear labels for each statistic
- Keep values concise (number + unit)
- Example: label="Revenue Growth", value="45%"

bullet-list:
- Write 3-5 compelling bullet points
- Each bullet: 8-12 words max
- Active voice, specific (not "we do good work" → "30% faster than competitors")

quote:
- Preserve the quote exactly
- Include author/attribution
- Keep it punchy (max 2 sentences)

text:
- Professional paragraphs (3-4 sentences max each)
- Clear, direct language
- Support the slide's main message

image-frame:
- Write compelling title (3-5 words)
- Brief caption (1 sentence max)
- Alt text for accessibility (descriptive, factual)

process:
- 4-6 sequential steps
- Each step: clear action (verb + noun)
- Include timeframe if relevant

table:
- Use for: Product comparisons, feature matrices, pricing, specs, roadmaps
- Include table_headers (array of column names)
- Include table_rows (2D array: [[row1_col1, row1_col2], [row2_col1, row2_col2]])

- **🔴 CRITICAL - ContentBlock type "markdown_table":**
  * Agent 1 (ContentAnalyzer) detects markdown tables and marks them as type: "markdown_table"
  * When you see content_block type = "markdown_table", the content field contains the FULL raw markdown
  * ALWAYS output component type: "table" (not stat-grid, not bullets)

- MARKDOWN TABLE PARSING (CRITICAL):
  * If input contains markdown table (with pipes |), PARSE it:
    - Extract headers from first row: | Header 1 | Header 2 |
    - Skip separator row: |---|---|
    - Extract data rows: | Cell 1 | Cell 2 |
  * Trim whitespace from all cells
  * Do NOT convert markdown table to prose/bullets
  * Preserve markdown structure in table_rows array
- Add table_class for styling:
  * "comparison-table" for product/feature comparisons
  * "pricing-table" for pricing structures
  * "roadmap-table" for timeline/roadmap data
  * "financial-table" for financial/projection data
- Add badges using SEMANTIC SENTIMENT ANALYSIS (not keyword matching):
  * Analyze cell content MEANING, not exact text
  * badge-success: Positive status (available, ready, completed, active, in stock, approved, verfügbar)
  * badge-warning: Neutral/pending status (future dates, TBD, planned, in progress, 2026, Q1 2025)
  * badge-danger: Negative status (unavailable, discontinued, failed, blocked, rejected, entwicklung)
- Use cell_badges format: {"column_index": [{"row_index": 0, "badge_type": "success"}]}
- Keep cells concise (2-5 words max per cell)
- Headers: clear, short column names (1-3 words)
- Max 6 columns, max 8 rows (for readability)
- For financial/data tables: identify summary/total rows → add to emphasis_rows
  * Triggers: Total, Subtotal, Sum, Deckungsbeitrag, Net, Gross, Gesamt, Summe
  * Effect: Rows get background: #f6f8fa; font-weight: 600;

feature-grid (NEW - Folie 6 pattern):
- Use for: Service features, product capabilities, team skills (4-9 items with icons)
- Include features array: [{"icon": "🤖", "title": "...", "description": "..."}]
- Icons: Use emojis (🤖 🎓 🔧 💡 ⚡ 🌍 📊 🔒)
- Each feature: title (3-5 words) + description (1-2 sentences)

image-grid (NEW - Folie 8.2 pattern):
- Use for: Multiple related images with optional status badges
- Include images array: [{"path": "...", "caption": "...", "badge": {"type": "success", "text": "..."}}]
- Include grid_layout: "2x2" or "3x2" (number of columns)
- Each image: path OR placeholder, title, caption, optional badge

process-horizontal (NEW - Folie 5.2 pattern):
- Use for: Timeline, process flows with sequential steps
- Include steps array: [{"title": "...", "description": "...", "timeframe": "..."}]
- Include show_arrows: true (display arrows between steps)
- Each step: clear action title + brief description + optional timeframe (e.g., "2026-2028")

multi-line-labels (semantic trigger):
- Use in stat-grid when statistics have CONTEXTUAL INFORMATION:
  * Source attribution: "18,000 units<br>(Bank of America, 2025)"
  * Product category: "Unitree H1<br>(High-End, Industrial)"
  * Timeframe: "500,000 shortage<br>(by 2030)"
- Add source_attributions metadata when sources are included

phased-structures (semantic pattern):
- Detect when content describes temporal phases or stages
- Structure as nested bullets with phase titles: "Phase 1: Title (2026-2028)"
- Useful for roadmaps, rollout plans, growth stages

═══════════════════════════════════════════════════════════
📊 READABILITY RULES
═══════════════════════════════════════════════════════════

✓ Avg word length: < 15 chars per word
✓ Sentence length: < 20 words
✓ Bullet points: < 12 words each
✓ Use numbers and concrete details (not vague)
✓ Active voice > Passive voice
✓ Parallel structure for lists
✓ Match input language throughout

═══════════════════════════════════════════════════════════
🔄 VALIDATION & FEEDBACK LOOP
═══════════════════════════════════════════════════════════

After generating FormattedSlide, VALIDATE:

1. Does each component fit its type?
   - stat-grid: 2-6 stats? ✓
   - bullet-list: 3-5 bullets? ✓
   - text: < 150 words? ✓
   - quote: < 100 words? ✓

2. Total word count reasonable?
   - Low density: < 100 words total
   - Medium density: 100-200 words
   - High density: 200-300 words (max before warning)

3. Is any component overloaded?
   - Too many words?
   - Too many bullets?
   - Text too complex?

IF VALIDATION FAILS:
- Return ValidationResult with warnings
- Suggest changes (e.g., "Remove 2 bullets", "Split into two components")
- System will replan (Agent 2) and retry

IF VALIDATION PASSES:
- Return FormattedSlide
- Ready for HTML rendering

═══════════════════════════════════════════════════════════
📋 OUTPUT FORMAT (JSON) - SUCCESS CASE
═══════════════════════════════════════════════════════════

{
  "slide_title": "Slide Title",
  "slide_subtitle": "Optional subtitle",
  "components": [
    {
      "component_id": "comp-1",
      "type": "stat-grid|bullet-list|quote|text|image-frame|process|table|feature-grid|image-grid|process-horizontal",
      "title": "Component Title",
      "subtitle": "Optional",

      // For stat-grid:
      "statistics": [
        {"label": "Revenue Growth", "value": "45%"},
        {"label": "New Markets", "value": "8"}
      ],

      // For bullet-list:
      "bullets": [
        "First bullet point",
        "Second bullet point"
      ],

      // For quote:
      "quote_text": "Actual quote",
      "quote_author": "Author Name",

      // For text:
      "paragraphs": ["Paragraph 1", "Paragraph 2"],

      // For image-frame:
      "image_path": "path/to/image.png",
      "image_caption": "Image caption",
      "image_alt_text": "Descriptive alt text",

      // For table:
      "table_headers": ["Column 1", "Column 2", "Status"],
      "table_rows": [
        ["Product A", "Feature X", "Verfügbar"],
        ["Product B", "Feature Y", "2026"]
      ],
      "table_class": "comparison-table",
      "cell_badges": {
        "2": [
          {"row_index": 0, "badge_type": "success"},
          {"row_index": 1, "badge_type": "warning"}
        ]
      },

      // For feature-grid:
      "features": [
        {"icon": "🤖", "title": "Hardware Integration", "description": "Seamless integration with existing robotics platforms"},
        {"icon": "⚡", "title": "Fast Deployment", "description": "Get up and running in hours, not weeks"}
      ],

      // For image-grid:
      "images": [
        {"path": "path/to/image1.png", "title": "Product A", "caption": "High-end model", "badge": {"type": "success", "text": "Available"}},
        {"path": "path/to/image2.png", "title": "Product B", "caption": "Coming soon", "badge": {"type": "warning", "text": "2026"}}
      ],
      "grid_layout": "2x2",

      // For process-horizontal:
      "steps": [
        {"title": "Planning", "description": "Define requirements and timeline", "timeframe": "2026"},
        {"title": "Development", "description": "Build and test the solution", "timeframe": "2026-2027"},
        {"title": "Launch", "description": "Roll out to market", "timeframe": "2027"}
      ],
      "show_arrows": true,

      // Semantic metadata (all component types):
      "semantic_context": "product_comparison|status_update|feature_showcase|timeline",
      "emphasis_rows": [2],
      "source_attributions": ["Bank of America, 2025"],
      "phase_structure": {"phases": [{"title": "Phase 1", "timeframe": "2026-2028"}]},

      // Metadata:
      "word_count": 45,
      "formatting_notes": "Applied active voice"
    }
  ],
  "language": "de|en",
  "total_word_count": 180,
  "readability_score": "easy|medium|complex",
  "accessibility_notes": ["Alt text provided for images"]
}

═══════════════════════════════════════════════════════════
📋 OUTPUT FORMAT (JSON) - VALIDATION FAILURE CASE
═══════════════════════════════════════════════════════════

{
  "is_valid": false,
  "warnings": [
    {
      "component_id": "comp-2",
      "issue": "Bullet list has 8 bullets (max 6)",
      "suggestion": "Remove least important 2 bullets"
    }
  ],
  "suggested_changes": {
    "comp-2": {
      "action": "reduce_bullets",
      "target_count": 5
    }
  },
  "retry_count": 1,
  "max_retries": 2
}

═══════════════════════════════════════════════════════════
💡 EXAMPLES
═══════════════════════════════════════════════════════════

EXAMPLE 1: Team Slide (SUCCESS)
INPUT BLOCKS:
- title: "Unser Team"
- statistic: "5 Experten"
- statement: "20 Jahre Robotik-Erfahrung"
- bullets: "Berlin\\nMünchen"

BLUEPRINT:
- comp-1 (stat-grid): statistic
- comp-2 (bullet-list): locations
- comp-3 (text): expertise statement

OUTPUT (FormattedSlide):
{
  "slide_title": "Unser Team",
  "components": [
    {
      "component_id": "comp-1",
      "type": "stat-grid",
      "title": "Team Größe",
      "statistics": [
        {"label": "Experten", "value": "5"}
      ],
      "word_count": 2
    },
    {
      "component_id": "comp-2",
      "type": "bullet-list",
      "title": "Standorte",
      "bullets": ["Berlin", "München"],
      "word_count": 2
    },
    {
      "component_id": "comp-3",
      "type": "text",
      "title": "Expertise",
      "paragraphs": ["20+ Jahre Erfahrung in Robotik und KI"],
      "word_count": 8
    }
  ],
  "total_word_count": 12,
  "readability_score": "easy"
}

EXAMPLE 2: Product Comparison Table (SUCCESS)
INPUT BLOCKS:
- title: "Unsere Roboter-Modelle"
- statement: "Verschiedene Autonomiegrade für unterschiedliche Einsatzbereiche"
- bullets: "RoboClean Alpha - Teilautonom - Gebäudereinigung\nRoboClean Beta - Vollautonom - Industriehallen\nRoboClean Gamma - Teilautonom - Außenbereiche"

BLUEPRINT:
- comp-1 (table): Product comparison with availability status

OUTPUT (FormattedSlide):
{
  "slide_title": "Unsere Roboter-Modelle",
  "components": [
    {
      "component_id": "comp-1",
      "type": "table",
      "title": "Produktübersicht",
      "table_headers": ["Roboter-Modell", "Autonomiegrad", "Einsatzbereich", "Verfügbarkeit"],
      "table_rows": [
        ["RoboClean Alpha", "Teilautonom", "Gebäudereinigung", "Verfügbar"],
        ["RoboClean Beta", "Vollautonom", "Industriehallen", "Verfügbar"],
        ["RoboClean Gamma", "Teilautonom", "Außenbereiche", "2026"]
      ],
      "table_class": "comparison-table",
      "cell_badges": {
        "3": [
          {"row_index": 0, "badge_type": "success"},
          {"row_index": 1, "badge_type": "success"},
          {"row_index": 2, "badge_type": "warning"}
        ]
      },
      "word_count": 24
    }
  ],
  "total_word_count": 24,
  "readability_score": "easy"
}

═══════════════════════════════════════════════════════════
✅ QUALITY RULES
═══════════════════════════════════════════════════════════

✓ Match input language for ALL text
✓ Keep it concise - each component focused
✓ Use strong verbs (not "is", "has" → "grows", "powers")
✓ Validate before returning
✓ Provide helpful feedback if validation fails
✓ Preserve user intent and tone
✓ Alt text: descriptive, not "image of X" but "X doing Y in Z"

═══════════════════════════════════════════════════════════
"""

    def _validate_component_slots(
        self,
        component: Dict[str, Any],
        components_schema: List[Dict[str, Any]],
    ) -> List[str]:
        """
        Validate a component against design-guide.json schema

        Returns:
            List of warning messages (empty if valid)
        """
        warnings = []
        component_type = component.get("type", "unknown")

        # Find schema for this component type
        schema = None
        for comp_schema in components_schema:
            if comp_schema.get("id") == component_type:
                schema = comp_schema
                break

        if not schema:
            # Component type not in schema, skip validation
            return warnings

        # Get required slots
        slots = schema.get("slots", {})
        component_id = component.get("component_id", "unknown")

        for slot_name, slot_def in slots.items():
            slot_required = slot_def.get("required", False)
            slot_type = slot_def.get("type", "string")

            # Check if slot exists in component
            if slot_required and slot_name not in component:
                warnings.append(
                    f"Component '{component_id}' (type: {component_type}) is missing required slot '{slot_name}'"
                )
            elif slot_name in component:
                # Validate slot type
                actual_value = component[slot_name]
                if slot_type == "array" and not isinstance(actual_value, list):
                    warnings.append(
                        f"Component '{component_id}' slot '{slot_name}' should be array, got {type(actual_value).__name__}"
                    )
                elif slot_type == "string" and not isinstance(actual_value, str):
                    warnings.append(
                        f"Component '{component_id}' slot '{slot_name}' should be string, got {type(actual_value).__name__}"
                    )

        return warnings

    def generate(
        self,
        slide_title: str,
        slide_blueprint: Dict[str, Any],
        content_blocks: List[Dict[str, Any]],
        language: str = "de",
        design_system: Optional[Dict[str, Any]] = None,
    ) -> Union[Dict[str, Any], ValidationResult]:
        """
        Generate formatted slide content with validation (Google Gemini)

        Args:
            slide_title: Title of the slide
            slide_blueprint: Component layout plan from Agent 2
            content_blocks: Raw content from Agent 1
            language: Output language (de/en)
            design_system: Design system with components_schema for validation

        Returns:
            FormattedSlide dict (if valid) or ValidationResult dict (if needs feedback)
        """

        # Map content blocks for reference
        blocks_by_index = {i: block for i, block in enumerate(content_blocks)}

        user_message = f"""Generate formatted text for this slide:

SLIDE TITLE: {slide_title}

BLUEPRINT:
{json.dumps(slide_blueprint, indent=2)}

CONTENT BLOCKS:
{json.dumps(content_blocks, indent=2)}

OUTPUT LANGUAGE: {language}

Please generate FormattedSlide JSON with all text content filled in and validated.
If any component is overloaded, return ValidationResult instead.

IMPORTANT: Return ONLY valid JSON, no markdown code blocks or extra text."""

        try:
            # Combine system prompt and user message for Gemini
            full_prompt = f"{self.system_prompt}\n\n{user_message}"

            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=4096,
                ),
            )

            # Extract JSON from response
            content = response.text

            # Remove markdown code blocks if present
            if content.startswith("```json"):
                content = content.replace("```json", "").replace("```", "").strip()
            elif content.startswith("```"):
                content = content.replace("```", "").strip()

            result = json.loads(content)

            # Check if this is a validation result or a formatted slide
            if "is_valid" in result and result["is_valid"] is False:
                # Validation failed, return feedback for retry
                return {
                    "is_valid": False,
                    "warnings": result.get("warnings", []),
                    "suggested_changes": result.get("suggested_changes"),
                    "retry_count": result.get("retry_count", 0),
                    "max_retries": result.get("max_retries", 2),
                }
            else:
                # Success! Return formatted slide
                formatted_slide = {
                    "slide_title": result.get("slide_title", slide_title),
                    "slide_subtitle": result.get("slide_subtitle"),
                    "components": result.get("components", []),
                    "language": language,
                    "total_word_count": result.get("total_word_count", 0),
                    "readability_score": result.get("readability_score", "medium"),
                    "accessibility_notes": result.get("accessibility_notes", []),
                }

                # Validate component slots against design-guide.json schema (if available)
                validation_warnings = []
                if design_system and "components_schema" in design_system:
                    components_schema = design_system["components_schema"]
                    for component in formatted_slide["components"]:
                        slot_warnings = self._validate_component_slots(
                            component, components_schema
                        )
                        validation_warnings.extend(slot_warnings)

                # Add validation warnings to response (if any)
                if validation_warnings:
                    formatted_slide["validation_warnings"] = validation_warnings
                    # Log warnings to console for developer visibility
                    print("⚠️ Component slot validation warnings:")
                    for warning in validation_warnings:
                        print(f"   - {warning}")

                return formatted_slide

        except Exception as e:
            raise Exception(f"ContentGeneratorAgentGoogle error: {str(e)}")
