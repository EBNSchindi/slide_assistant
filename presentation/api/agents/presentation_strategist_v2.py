"""
Presentation Strategist Agent (v2) - Plans component layout and structure

Agent 2 of 3 in the new pipeline:
- Input: ContentBlocks + SlideIntent + Design System + Image metadata
- Output: SlideBlueprint (which components, in what order, where images go)
- Job: Decide WHAT components, not HOW to render them
"""

from openai import OpenAI
from typing import List, Dict, Any, Optional
import json
import sys
import os

# Handle imports robustly
try:
    from schemas.blueprint import SlideBlueprint, ComponentBlueprint, ImageSlot
except ImportError:
    from ..schemas.blueprint import SlideBlueprint, ComponentBlueprint, ImageSlot


class PresentationStrategistAgentV2:
    """Recommends optimal component layout and structure"""

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o",
        reasoning_effort: str = "high",
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
🎯 AGENT 2: PRESENTATION STRATEGIST
═══════════════════════════════════════════════════════════

YOUR JOB: Decide WHAT components to use and HOW to arrange them.

INPUT:
- ContentBlocks (from Agent 1): Individual content pieces
- SlideIntent: What this slide is trying to say
- Design System: Available component types
- Image metadata: Which images are available

OUTPUT:
- SlideBlueprint: Component layout plan (no HTML, no text generation)

DO NOT: Generate text, HTML, or styling details. Just plan structure.

═══════════════════════════════════════════════════════════
🧩 COMPONENT TYPES YOU CAN USE
═══════════════════════════════════════════════════════════

1. stat-grid
   Purpose: Display multiple statistics/metrics in a grid
   Best for: ContentBlock types STATISTIC, STATISTICS
   Constraints: Max 6 stats in a grid

2. bullet-list
   Purpose: Display bullet points or short items
   Best for: ContentBlock types BULLET, BULLETS
   Constraints: Max 5-6 bullets per component

3. quote
   Purpose: Highlight a quote or testimonial
   Best for: ContentBlock type QUOTE
   Constraints: One quote per component

4. text
   Purpose: Display paragraphs or longer statements
   Best for: ContentBlock type STATEMENT
   Constraints: Readable text length (max 150 words)

5. image-frame
   Purpose: Display an image with caption
   Best for: ContentBlock type IMAGE_REF
   Constraints: One image per component (ideally), with alt text

6. process
   Purpose: Show sequential steps or timeline
   Best for: BULLETS formatted as steps
   Constraints: 4-6 steps max

7. table
   Purpose: Comparison or structured data
   Best for: Complex structured data
   Constraints: Max 5 rows × 5 columns

═══════════════════════════════════════════════════════════
📐 LAYOUT PATTERNS
═══════════════════════════════════════════════════════════

single:
- One large component (full width)
- Use for: Hero stats, full-width image, single quote

two_column:
- Left: text/list, Right: image
- Or: left: stat-grid, right: bullets
- Best for: Mixed content with visual support

two_row:
- Top: heading + stat-grid
- Bottom: bullets or text
- Best for: Metrics + explanation

three_component:
- Three smaller components stacked/arranged
- Best for: Multiple dimensions (e.g., stats + list + image)

═══════════════════════════════════════════════════════════
🖼️ IMAGE HANDLING
═══════════════════════════════════════════════════════════

If user provided images:
1. Identify which ContentBlock references the image
2. Create an ImageSlot pointing to the image
3. Assign it to appropriate component (usually image-frame)
4. Decide position: left, right, top, bottom, center

If no images: ImageSlot is null for all components

═══════════════════════════════════════════════════════════
📋 OUTPUT FORMAT (JSON)
═══════════════════════════════════════════════════════════

{
  "slide_title": "Slide heading",
  "layout_type": "single|two_column|two_row|three_component|custom",
  "components": [
    {
      "component_id": "comp-1",
      "type": "stat-grid|bullet-list|quote|text|image-frame|process|table",
      "position": "top|middle|bottom",
      "content_block_indices": [0, 1],  // Which ContentBlocks go here
      "image_slot": {
        "slot_id": "main_visual",
        "image_filename": "team.png",
        "position": "right",
        "description": "Team photo"
      } or null,
      "layout_hints": {"columns": 2}  // Optional hints
    }
  ],
  "design_notes": "Optional designer notes",
  "image_count": 1
}

═══════════════════════════════════════════════════════════
💡 DECISION RULES
═══════════════════════════════════════════════════════════

STATISTICS (2-6 metrics):
→ Use stat-grid in single component layout

MANY BULLETS (5+):
→ Use bullet-list, max 5-6 per component

STATEMENT + BULLETS:
→ Two components: text (top) + bullet-list (bottom)

IMAGE + TEXT:
→ Two_column layout: image on right/left, text on other side

MIXED CONTENT (stats + bullets + image):
→ Three_component: arrange by visual flow (top-to-bottom)

═══════════════════════════════════════════════════════════
✅ QUALITY RULES
═══════════════════════════════════════════════════════════

✓ Max 3 components per slide (constraint from design system)
✓ Each component should focus on one idea
✓ Position components for visual flow (top: headline, middle: main, bottom: supporting)
✓ Assign correct content_block_indices
✓ If image exists, use image-frame component
✓ Match language of input (design_notes in same language)
✓ Set realistic layout_type

═══════════════════════════════════════════════════════════
"""

    def plan(
        self,
        slide_intent: Dict[str, Any],
        content_blocks: List[Dict[str, Any]],
        design_system: Optional[Dict[str, Any]] = None,
        image_metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Plan slide layout and component structure

        Args:
            slide_intent: From Agent 1 - what this slide is trying to say
            content_blocks: From Agent 1 - individual content pieces
            design_system: Available components, constraints
            image_metadata: Available images info

        Returns:
            SlideBlueprint as dict
        """

        # Build context for the LLM
        design_context = ""
        if design_system:
            design_context = f"""Available Components: {design_system.get('available_components', ['stat-grid', 'bullet-list', 'quote', 'text', 'image-frame'])}
Max Components per Slide: {design_system.get('max_components', 3)}
Spacing: {design_system.get('spacing', 'standard')}
"""

        image_context = ""
        if image_metadata:
            images_list = image_metadata.get("images", [])
            if images_list:
                image_context = f"""Available Images:
{json.dumps(images_list, indent=2)}
"""

        content_blocks_str = json.dumps(content_blocks, indent=2)

        user_message = f"""Plan the slide layout based on this content:

SLIDE INTENT:
{json.dumps(slide_intent, indent=2)}

CONTENT BLOCKS:
{content_blocks_str}

{design_context}

{image_context}

Output a SlideBlueprint as JSON with components and layout."""

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

            # Add GPT-5 controls
            if "gpt-5" in self.model.lower():
                api_params["extra_body"] = {
                    "reasoning_effort": self.reasoning_effort,
                    "verbosity": self.verbosity,
                }

            response = self.client.chat.completions.create(**api_params)
            blueprint = json.loads(response.choices[0].message.content)

            # Validate minimum structure
            if "components" not in blueprint:
                raise ValueError("Missing components in blueprint")

            return blueprint

        except Exception as e:
            raise Exception(f"PresentationStrategistV2 error: {str(e)}")

    def replan(
        self,
        original_blueprint: Dict[str, Any],
        feedback: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Adjust blueprint based on feedback from Agent 3

        Used in feedback loop when Agent 3 says content won't fit.

        Args:
            original_blueprint: The original SlideBlueprint
            feedback: Feedback from Agent 3 (which component is problematic)

        Returns:
            Adjusted SlideBlueprint
        """

        user_message = f"""Adjust this slide blueprint based on feedback:

ORIGINAL BLUEPRINT:
{json.dumps(original_blueprint, indent=2)}

FEEDBACK:
{json.dumps(feedback, indent=2)}

Please adjust the components or layout to address the feedback. Return updated blueprint as JSON."""

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
                    "reasoning_effort": "high",
                    "verbosity": self.verbosity,
                }

            response = self.client.chat.completions.create(**api_params)
            adjusted_blueprint = json.loads(response.choices[0].message.content)

            return adjusted_blueprint

        except Exception as e:
            raise Exception(f"PresentationStrategistV2 replan error: {str(e)}")
