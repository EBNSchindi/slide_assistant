"""
Content Analyzer Agent (v2) - Analyzes user input and returns ContentBlocks + SlideIntent

Agent 1 of 3 in the new pipeline:
- Input: Raw user text
- Output: SlideIntent + ContentBlock[]
- Job: Understand what the slide needs to say, break it into atomic pieces
"""

from openai import OpenAI
from typing import List, Dict, Any
import json
import sys
import os

# Handle imports robustly
try:
    from schemas.blueprint import ContentBlock, ContentBlockType, SlideIntent
except ImportError:
    from ..schemas.blueprint import ContentBlock, ContentBlockType, SlideIntent


class ContentAnalyzerAgentV2:
    """Analyzes user input and structures it into ContentBlocks"""

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

7. IMAGE_REF - Reference to an image
   Example: {"type": "image_ref", "content": "Team photo showing 5 experts"}
   Use when: User mentions images, screenshots, photos

8. TITLE - Slide title
   Example: {"type": "title", "content": "Unser Team"}
   Use when: There's a clear heading

═══════════════════════════════════════════════════════════
📊 SLIDE INTENT TYPES
═══════════════════════════════════════════════════════════

When analyzing, identify the slide's main goal:
- problem: Defining a market problem
- solution: Presenting a solution/approach
- team: Introducing team members
- kpi: Showing key metrics
- timeline: Showing phases/timeline
- process: Showing a workflow
- use_case: Demonstrating product usage
- market: Market opportunity/size
- competition: Competitive landscape
- roadmap: Future plans
- other: Something else

═══════════════════════════════════════════════════════════
🎯 LANGUAGE HANDLING
═══════════════════════════════════════════════════════════

CRITICAL: Match input language!
- German input → analyze in German, content in German
- English input → analyze in English, content in English
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
      "type": "statistic|statistics|statement|bullet|bullets|quote|image_ref|title",
      "content": "Actual content text",
      "priority": "must_have|should_have|nice_to_have",
      "image_hint": "ref to image file if applicable" (optional),
      "metadata": {} (optional)
    }
  ]
}

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
    "primary_message": "Five-person expert team with deep robotics and AI background",
    "language": "de",
    "density": "medium"
  },
  "content_blocks": [
    {"type": "title", "content": "Unser Team", "priority": "must_have"},
    {"type": "statistic", "content": "5 Experten", "priority": "must_have"},
    {"type": "statement", "content": "20 Jahre Erfahrung Robotik", "priority": "should_have"},
    {"type": "statement", "content": "PhD KI, ehemals Google", "priority": "should_have"},
    {"type": "statement", "content": "3 zusätzliche Robotik-Experten", "priority": "should_have"},
    {"type": "bullets", "content": "Berlin\\nMünchen", "priority": "nice_to_have", "metadata": {"type": "locations"}}
  ]
}

EXAMPLE 2: KPI Slide
INPUT:
"45% revenue growth to €12.3M
8 new markets entered
250 enterprise customers signed"

OUTPUT:
{
  "slide_intent": {
    "intent_type": "kpi",
    "primary_message": "Strong growth across revenue, markets, and customer base",
    "language": "en",
    "density": "high"
  },
  "content_blocks": [
    {"type": "statistic", "content": "45% revenue growth to €12.3M", "priority": "must_have"},
    {"type": "statistic", "content": "8 new markets", "priority": "must_have"},
    {"type": "statistic", "content": "250 enterprise customers", "priority": "must_have"}
  ]
}

EXAMPLE 3: With Image
INPUT:
"Dashboard screenshot showing our analytics platform
Clean UI with comprehensive reporting
Here's dashboard.png"

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
            api_params = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_message},
                ],
                "temperature": 0.7,
                "response_format": {"type": "json_object"},
            }

            # Add GPT-5 controls if applicable
            if "gpt-5" in self.model.lower():
                api_params["extra_body"] = {
                    "reasoning_effort": self.reasoning_effort,
                    "verbosity": self.verbosity,
                }

            response = self.client.chat.completions.create(**api_params)
            result = json.loads(response.choices[0].message.content)

            # Validate structure
            if "slide_intent" not in result or "content_blocks" not in result:
                raise ValueError("Missing required fields: slide_intent, content_blocks")

            return result

        except Exception as e:
            raise Exception(f"ContentAnalyzerV2 error: {str(e)}")
