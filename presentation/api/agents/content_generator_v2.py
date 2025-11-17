"""
Content Generator Agent (v2) - Generates final formatted text for slide components

Agent 3 of 3 in the new pipeline:
- Input: SlideBlueprint (layout plan) + ContentBlocks
- Output: FormattedSlide (fully formatted text) OR ValidationResult (feedback for replan)
- Job: Write the actual text for each component, with validation and feedback loop support
"""

from openai import OpenAI
from typing import List, Dict, Any, Union, Optional
import json
import sys
import os

# Handle imports robustly
try:
    from schemas.blueprint import FormattedSlide, FormattedComponentData, ValidationResult, ValidationWarning
except ImportError:
    from ..schemas.blueprint import FormattedSlide, FormattedComponentData, ValidationResult, ValidationWarning


class ContentGeneratorAgentV2:
    """Generates final formatted text for slide components with feedback loop support"""

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o",
        reasoning_effort: str = "medium",
        verbosity: str = "medium",
        use_structured_outputs: bool = False,
    ):
        self.client = OpenAI(api_key=api_key)
        self.model = model
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
      "type": "stat-grid|bullet-list|quote|text|image-frame|process|table",
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

    def generate(
        self,
        slide_title: str,
        slide_blueprint: Dict[str, Any],
        content_blocks: List[Dict[str, Any]],
        language: str = "de",
    ) -> Union[Dict[str, Any], ValidationResult]:
        """
        Generate formatted slide content with validation

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
If any component is overloaded, return ValidationResult instead."""

        try:
            api_params = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_message},
                ],
                "temperature": 0.7,
                "response_format": {"type": "json_object"},
            }

            if "gpt-5" in self.model.lower():
                api_params["extra_body"] = {
                    "reasoning_effort": self.reasoning_effort,
                    "verbosity": self.verbosity,
                }

            response = self.client.chat.completions.create(**api_params)
            result = json.loads(response.choices[0].message.content)

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
                return {
                    "slide_title": result.get("slide_title", slide_title),
                    "slide_subtitle": result.get("slide_subtitle"),
                    "components": result.get("components", []),
                    "language": language,
                    "total_word_count": result.get("total_word_count", 0),
                    "readability_score": result.get("readability_score", "medium"),
                    "accessibility_notes": result.get("accessibility_notes", []),
                }

        except Exception as e:
            raise Exception(f"ContentGeneratorV2 error: {str(e)}")
