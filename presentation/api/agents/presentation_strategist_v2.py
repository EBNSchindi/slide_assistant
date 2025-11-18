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
   Best for: ContentBlock type MARKDOWN_TABLE (pipe-separated markdown tables)
   Constraints: Max 5 rows × 5 columns
   **CRITICAL**: When ContentBlock has type "markdown_table", ALWAYS use "table" component type
   Do NOT convert markdown tables to stat-grid or other types

8. feature-grid
   Purpose: Display multiple features/products with icons and descriptions
   Best for: Multiple related features, product offerings, USPs with titles
   Constraints: 3-6 features per grid, each with title + description
   **WHEN TO USE**: User lists multiple features/benefits/USPs with consistent structure
   Example input: "✨ Feature 1: Description\n🎯 Feature 2: Description"

9. image-grid
   Purpose: Display multiple images in a grid layout
   Best for: Multiple related images that belong together (gallery, comparison)
   Constraints: 2-4 images in grid
   **WHEN TO USE**: User mentions multiple images for same context

10. process-horizontal
    Purpose: Show sequential workflow/timeline horizontally
    Best for: Linear workflows, timelines, step-by-step processes displayed left-to-right
    Constraints: 4-6 steps max, each with title + description
    **WHEN TO USE**: When process/timeline should flow horizontally instead of vertically

11. comparison-cards
    Purpose: Side-by-side comparison of options (Before/After, Competitor, Problem/Solution)
    Best for: Contrasting scenarios, highlighting changes, competitive analysis
    Constraints: 2-3 cards max, each with label, icon, 3-5 bullet points, and style (success/danger/warning)
    **WHEN TO USE**: User compares two things, shows before/after, or contrasts alternatives

12. timeline
    Purpose: Chronological display of events, milestones, or roadmap
    Best for: Company history, project timeline, future roadmap, milestone tracking
    Constraints: 4-8 items max, each with date, title, description, status (completed/current/upcoming)
    **WHEN TO USE**: User mentions dates, phases, quarters, milestones, or chronological progression

13. logo-grid
    Purpose: Display partner, client, or investor logos for social proof
    Best for: Customer logos, partner companies, press mentions, investor names
    Constraints: 6-12 logos recommended, grayscale by default for visual consistency
    **WHEN TO USE**: User mentions clients, partners, customers, investors, or "supported by"

14. team-grid
    Purpose: Showcase team members with photos, names, roles, and credentials
    Best for: Team introduction, founder profiles, advisory board, key people
    Constraints: 4-8 members max per slide, includes name, role, credentials, optional LinkedIn
    **WHEN TO USE**: User mentions team, founders, advisors, experts, or key personnel

15. metric-trend
    Purpose: Display KPI metrics with trend indicators and percentage changes
    Best for: Performance metrics, growth indicators, comparative KPIs over time
    Constraints: 2-4 metrics max, each with value, label, trend (up/down/neutral), change%, period
    **WHEN TO USE**: User mentions growth, trends, YoY/MoM changes, or performance tracking

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
      "type": "stat-grid|bullet-list|quote|text|image-frame|process|table|feature-grid|image-grid|process-horizontal|comparison-cards|timeline|logo-grid|team-grid|metric-trend",
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

**🔴 MARKDOWN_TABLE (CRITICAL RULE):**
→ If ANY ContentBlock has type "markdown_table":
→ ALWAYS use "table" component type
→ NEVER convert to stat-grid or other types
→ Single table layout or multiple tables in two_row/three_component

**🟠 FEATURES (IMPORTANT RULE):**
→ If ANY ContentBlock has type "feature" OR "features":
→ ALWAYS use "feature-grid" component type
→ Combine all feature blocks into single feature-grid (3-6 features)
→ Do NOT split into multiple bullet-list or text components
→ Example: 6 features with icons → single feature-grid, NOT 3 × bullet-list

STATISTICS (2-6 metrics):
→ Use stat-grid in single component layout
→ Do NOT use for markdown tables (use "table" component instead)

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

✓ Max 3 components per slide (design constraint)
  → HOWEVER: feature-grid with 6 features = 1 component (not 3)
  → HOWEVER: image-grid with 4 images = 1 component (not 4)
  → Think in components, not in content items
  → Prefer aggregating related content into one rich component over splitting

✓ Each component should focus on one idea/dimension
  → Exception: feature-grid groups multiple related features (that's its purpose)

✓ Position components for visual flow (top: headline, middle: main, bottom: supporting)
✓ Assign correct content_block_indices
✓ If image exists, prefer image-frame or image-grid component
✓ Match language of input (design_notes in same language)
✓ Set realistic layout_type

EXAMPLE:
  ❌ BAD: 6 features → text + bullet-list + bullet-list (3 components, fragmented)
  ✅ GOOD: 6 features → feature-grid (1 component, cohesive)

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

        # Build context for the LLM (enhanced with JSON schema if available)
        design_context = ""
        if design_system:
            # Check if we have component schemas from design-guide.json
            components_schema = design_system.get('components_schema', [])
            layouts = design_system.get('layouts', [])

            if components_schema:
                # Enhanced context with JSON schema details
                design_context = f"""═══════════════════════════════════════════════════════════
📦 DESIGN SYSTEM (from design-guide.json)
═══════════════════════════════════════════════════════════

Available Components ({len(components_schema)} types):
"""
                for comp in components_schema:
                    comp_id = comp.get('id', 'unknown')
                    comp_name = comp.get('name', '')
                    comp_desc = comp.get('description', '')
                    slots = comp.get('slots', {})
                    design_context += f"\n• {comp_id} ({comp_name})"
                    design_context += f"\n  Description: {comp_desc}"
                    design_context += f"\n  Slots: {list(slots.keys())}"

                if layouts:
                    design_context += f"\n\nAvailable Layouts ({len(layouts)} patterns):\n"
                    for layout in layouts:
                        layout_id = layout.get('id', 'unknown')
                        layout_desc = layout.get('description', '')
                        design_context += f"• {layout_id}: {layout_desc}\n"

                design_context += f"\nMax Components per Slide: {design_system.get('max_components', 3)}\n"
            else:
                # Fallback to simple component list (Markdown-based)
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
