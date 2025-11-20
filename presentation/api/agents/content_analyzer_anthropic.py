"""
Content Analyzer Agent (Anthropic Claude) - Analyzes user input and returns ContentBlocks + SlideIntent

Agent 1 of 3 in the new pipeline (Anthropic provider):
- Input: Raw user text
- Output: SlideIntent + ContentBlock[]
- Job: Understand what the slide needs to say, break it into atomic pieces
- Provider: Anthropic Claude (Sonnet 4.5, 3.5 Sonnet, etc.)
"""

from anthropic import Anthropic
from typing import List, Dict, Any
import json
import sys
import os

# Handle imports robustly
try:
    from schemas.blueprint import ContentBlock, ContentBlockType, SlideIntent
except ImportError:
    from ..schemas.blueprint import ContentBlock, ContentBlockType, SlideIntent


class ContentAnalyzerAgentAnthropic:
    """Analyzes user input and structures it into ContentBlocks (Anthropic Claude)"""

    def __init__(
        self,
        api_key: str,
        model: str = "claude-sonnet-4.5-20250514",
        reasoning_effort: str = "medium",
        verbosity: str = "medium",
        use_structured_outputs: bool = False,
    ):
        self.client = Anthropic(api_key=api_key)
        self.model = model
        self.reasoning_effort = reasoning_effort
        self.verbosity = verbosity
        self.use_structured_outputs = use_structured_outputs

        self.system_prompt = """
═══════════════════════════════════════════════════════════
🎯 AGENT 1: CONTENT ANALYZER
═══════════════════════════════════════════════════════════

YOUR JOB: Understand raw user input and break it into atomic content pieces.

INPUT: Any format - bullets, prose, markdown, mixed
OUTPUT:
  - slide_intent: What this slide tries to communicate
  - content_blocks: Individual pieces of content (statistics, bullets, quotes, etc.)

DO NOT: Recommend layouts, HTML, or components. Just understand & structure.

═══════════════════════════════════════════════════════════
🏗️ CONTENT BLOCKS: THE 7 TYPES
═══════════════════════════════════════════════════════════

1. STATISTIC - Single number with label
   Example: {"type": "statistic", "content": "5 Experten"}
   Use when: One metric to highlight

2. STATISTICS - Multiple numbers (3+)
   Example: {"type": "statistics", "content": "5 Experten, 20 Jahre Erfahrung, 3 Standorte"}
   Use when: Multiple related metrics

3. STATEMENT - A thesis, claim, or key message
   Example: {"type": "statement", "content": "Wir sind Marktführer in KI-Robotik"}
   Use when: Core message or positioning

4. BULLET - Single bullet point
   Example: {"type": "bullet", "content": "Spezialisierung Robotik & KI"}
   Use when: One detail point

5. BULLETS - Multiple bullet points
   Example: {"type": "bullets", "content": "- Robotik\\n- KI\\n- Cloud"}
   Use when: 2+ related detail points

6. QUOTE - Direct quote or testimonial
   Example: {"type": "quote", "content": "'Best solution we found' - CEO"}
   Use when: Third-party validation

7. IMAGE_REF - Reference to an image/screenshot
   Example: {"type": "image_ref", "content": "Dashboard screenshot", "image_hint": "dashboard.png"}
   Use when: User mentions showing an image

8. MARKDOWN_TABLE - Structured data in table format
   Example: {"type": "markdown_table", "content": "| Col1 | Col2 |\\n|---|---|\\n| A | B |"}
   Use when: Input contains markdown table syntax (pipes |)

9. TITLE - Slide title or heading
   Example: {"type": "title", "content": "Unser Team"}
   Use when: Clear heading/title in input

═══════════════════════════════════════════════════════════
🌍 LANGUAGE DETECTION
═══════════════════════════════════════════════════════════

Auto-detect input language and set in slide_intent.language:
- "de" for German
- "en" for English

Key indicators:
- German: "Unser", "Jahre", "können", "über", "€"
- English: "Our", "years", "can", "about", "$"

Rules:
- Match output language to input language
- Keep original tone and terminology

═══════════════════════════════════════════════════════════
💪 PRIORITY LEVELS
═══════════════════════════════════════════════════════════

For each ContentBlock, assign a priority:
- must_have: Critical to understanding the slide
- should_have: Important but not essential
- nice_to_have: Supporting detail, can be cut if space is tight

═══════════════════════════════════════════════════════════
📋 OUTPUT FORMAT (JSON)
═══════════════════════════════════════════════════════════

{
  "slide_intent": {
    "intent_type": "problem|solution|team|kpi|timeline|process|use_case|market|competition|roadmap|other",
    "primary_message": "One sentence: what is this slide saying?",
    "target_audience": "investor|team|customer|general" (optional),
    "language": "de|en",
    "density": "low|medium|high"
  },
  "content_blocks": [
    {
      "type": "statistic|statistics|statement|bullet|bullets|quote|image_ref|markdown_table|title",
      "content": "Actual content text",
      "priority": "must_have|should_have|nice_to_have",
      "image_hint": "ref to image file if applicable" (optional),
      "metadata": {} (optional)
    }
  ]
}

⚠️ **CRITICAL MARKDOWN TABLE HANDLING:**
If input contains markdown table syntax (pipes | separating columns):
- Detect it immediately: Look for pattern like "| Header1 | Header2 |"
- Create content_block with type: "markdown_table"
- content: Include the COMPLETE raw markdown table (headers + separator + all rows)
- priority: "must_have" (tables are always critical)
- DO NOT convert to statistics, bullets, or any other format
- Example input: "| Product | Price |\\n|---|---|\\n| A | $100 |"
- Example output: {{"type": "markdown_table", "content": "| Product | Price |\\n|---|---|\\n| A | $100 |", "priority": "must_have"}}

═══════════════════════════════════════════════════════════
📝 EXAMPLES
═══════════════════════════════════════════════════════════

EXAMPLE 1: Team Slide
INPUT:
"Unser 5-köpfiges Team
- Gründer: 20 Jahre Erfahrung Robotik
- CTO: PhD KI, vorher Google
- Drei weitere Robotik-Experten
Standorte: Berlin & München"

OUTPUT:
{
  "slide_intent": {
    "intent_type": "team",
    "primary_message": "Experienced 5-person robotics team with strong AI expertise",
    "language": "de",
    "density": "medium"
  },
  "content_blocks": [
    {"type": "statistic", "content": "5-köpfiges Team", "priority": "must_have"},
    {"type": "bullets", "content": "- Gründer: 20 Jahre Erfahrung Robotik\\n- CTO: PhD KI, vorher Google\\n- Drei weitere Robotik-Experten", "priority": "must_have"},
    {"type": "statement", "content": "Standorte: Berlin & München", "priority": "should_have"}
  ]
}

EXAMPLE 2: Image-focused Slide
INPUT:
"Our analytics dashboard provides clean UI with comprehensive reporting capabilities.
[Screenshot: dashboard.png]"

OUTPUT:
{
  "slide_intent": {
    "intent_type": "use_case",
    "primary_message": "Analytics dashboard demonstrates clean UI and comprehensive reporting",
    "language": "en",
    "density": "low"
  },
  "content_blocks": [
    {"type": "statement", "content": "Clean UI with comprehensive reporting capabilities", "priority": "must_have"},
    {"type": "image_ref", "content": "Dashboard screenshot", "priority": "must_have", "image_hint": "dashboard.png"}
  ]
}

═══════════════════════════════════════════════════════════
✅ QUALITY RULES
═══════════════════════════════════════════════════════════

✓ Each ContentBlock should be atomic (one idea)
✓ Match input language exactly
✓ Preserve tone and terminology
✓ Set realistic priorities
✓ Keep content brief (can be expanded by Agent 3)
✓ Detect image references and mark as image_ref type
✓ If unsure about intent_type, choose "other"
✓ Density: count blocks to estimate (1-2 blocks=low, 3-5=medium, 6+=high)

═══════════════════════════════════════════════════════════
"""

    def analyze(self, user_input: str) -> Dict[str, Any]:
        """
        Analyze user input and return SlideIntent + ContentBlocks

        Returns:
            Dict with 'slide_intent' and 'content_blocks' keys
        """

        user_message = f"""Please analyze this slide content and structure it:

{user_input}

Return valid JSON with slide_intent and content_blocks."""

        try:
            # Claude API call
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                temperature=0.7,
                system=self.system_prompt,
                messages=[
                    {"role": "user", "content": user_message}
                ]
            )

            # Extract JSON from response
            content = response.content[0].text

            # Claude sometimes wraps JSON in markdown code blocks, remove them
            if content.startswith("```json"):
                content = content.replace("```json", "").replace("```", "").strip()
            elif content.startswith("```"):
                content = content.replace("```", "").strip()

            result = json.loads(content)

            # Validate structure
            if "slide_intent" not in result or "content_blocks" not in result:
                raise ValueError("Missing required fields: slide_intent, content_blocks")

            return result

        except Exception as e:
            raise Exception(f"ContentAnalyzerAnthropic error: {str(e)}")
