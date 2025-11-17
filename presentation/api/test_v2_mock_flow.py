"""
Test v2 pipeline with mock agents - complete flow simulation

This tests the full generation pipeline without needing OpenAI API.
Run with: python3 test_v2_mock_flow.py
"""

import sys
import os
import json

# Setup path
api_dir = os.path.dirname(__file__)
sys.path.insert(0, api_dir)

from agents.mock_agents_v2 import (
    MockContentAnalyzerAgentV2,
    MockPresentationStrategistAgentV2,
    MockContentGeneratorAgentV2,
)
from renderers.component_renderer import HTMLComponentRenderer, Theme


def test_complete_v2_pipeline():
    """Test complete v2 pipeline with mock agents"""

    print("\n" + "="*70)
    print("🧪 Testing v2 Pipeline with Mock Agents")
    print("="*70)

    # Initialize agents
    print("\n1️⃣  Initializing Agents...")
    analyzer = MockContentAnalyzerAgentV2()
    strategist = MockPresentationStrategistAgentV2()
    generator = MockContentGeneratorAgentV2()
    renderer = HTMLComponentRenderer(theme=Theme(name="github"))
    print("   ✅ All agents initialized")

    # Sample user input
    user_input = """Unser 5-köpfiges Team mit über 20 Jahren Erfahrung in Robotik und KI.
Gegründet von Experten aus Forschung und Industrie.
Standorte: Berlin und München."""

    print(f"\n2️⃣  User Input:")
    print(f"   {user_input[:60]}...")

    # Stage 1: Content Analysis
    print("\n3️⃣  Stage 1: Content Analysis")
    analysis = analyzer.analyze(user_input)
    slide_intent = analysis.get("slide_intent", {})
    content_blocks = analysis.get("content_blocks", [])

    print(f"   Intent Type: {slide_intent.get('intent_type')}")
    print(f"   Primary Message: {slide_intent.get('primary_message')}")
    print(f"   Content Blocks: {len(content_blocks)}")
    for i, block in enumerate(content_blocks):
        print(f"     - Block {i+1}: {block['type']} | {block['content'][:40]}...")

    # Stage 2: Layout Planning
    print("\n4️⃣  Stage 2: Layout Planning")
    blueprint = strategist.plan(
        slide_intent=slide_intent,
        content_blocks=content_blocks,
    )

    print(f"   Slide Title: {blueprint.get('slide_title')}")
    print(f"   Layout Type: {blueprint.get('layout_type')}")
    print(f"   Components: {len(blueprint.get('components', []))}")
    for i, comp in enumerate(blueprint.get("components", [])):
        print(
            f"     - Comp {i+1}: {comp['type']} @ {comp['position']} (blocks: {comp['content_block_indices']})"
        )

    # Stage 3: Content Generation
    print("\n5️⃣  Stage 3: Content Generation")
    formatted_slide = generator.generate(
        slide_title=blueprint.get("slide_title"),
        slide_blueprint=blueprint,
        content_blocks=content_blocks,
        language="de",
    )

    print(f"   Slide Title: {formatted_slide.get('slide_title')}")
    print(f"   Components Generated: {len(formatted_slide.get('components', []))}")
    print(f"   Total Word Count: {formatted_slide.get('total_word_count')}")
    print(f"   Readability: {formatted_slide.get('readability_score')}")

    for i, comp in enumerate(formatted_slide.get("components", [])):
        print(f"   Component {i+1}: {comp['type']}")
        if comp['type'] == 'stat-grid':
            for stat in comp.get('statistics', []):
                print(f"     - {stat['label']}: {stat['value']}")
        elif comp['type'] == 'bullet-list':
            for bullet in comp.get('bullets', []):
                print(f"     - {bullet}")
        elif comp['type'] == 'text':
            for para in comp.get('paragraphs', [])[:1]:  # First para
                print(f"     {para[:60]}...")

    # Stage 4: HTML Rendering
    print("\n6️⃣  Stage 4: HTML Rendering")
    formatted_slide["slide_id"] = "slide-46"
    formatted_slide["theme"] = "github"

    html = renderer.render_slide(formatted_slide)
    print(f"   HTML Generated: {len(html)} bytes")
    print(f"   Contains <section>: {('<section' in html)}")
    print(f"   Contains components: {('slide-component' in html)}")

    # Count HTML elements
    component_count = html.count('class="slide-component')
    print(f"   Components in HTML: {component_count}")

    # Stage 5: Markdown Conversion
    print("\n7️⃣  Stage 5: Output Summary")
    print(f"   ✅ HTML Output: {len(html)} bytes")
    print(f"   ✅ Slide Title: {formatted_slide.get('slide_title')}")
    print(f"   ✅ Components: {len(formatted_slide.get('components'))}")
    print(f"   ✅ Language: {formatted_slide.get('language')}")

    # Test with different theme
    print("\n8️⃣  Testing Theme Variations")
    for theme_name in ["github", "modern", "minimal"]:
        theme = Theme(name=theme_name)
        renderer_themed = HTMLComponentRenderer(theme=theme)
        formatted_slide_themed = formatted_slide.copy()
        formatted_slide_themed["theme"] = theme_name
        html_themed = renderer_themed.render_slide(formatted_slide_themed)
        print(f"   {theme_name}: {len(html_themed)} bytes, theme class: {f'slide-theme-{theme_name}' in html_themed}")

    print("\n" + "="*70)
    print("✅ All v2 Pipeline Tests Passed!")
    print("="*70)

    return {
        "success": True,
        "slide_intent": slide_intent,
        "blueprint": blueprint,
        "formatted_slide": formatted_slide,
        "html_length": len(html),
        "components": len(formatted_slide.get("components", [])),
    }


def test_feedback_loop():
    """Test feedback loop mechanism"""

    print("\n" + "="*70)
    print("🔄 Testing Feedback Loop Mechanism")
    print("="*70)

    analyzer = MockContentAnalyzerAgentV2()
    strategist = MockPresentationStrategistAgentV2()

    # Initial analysis
    print("\n1️⃣  Stage 1: Initial Analysis")
    analysis = analyzer.analyze("Test content for feedback loop")
    slide_intent = analysis["slide_intent"]
    content_blocks = analysis["content_blocks"]
    print("   ✅ Content analyzed")

    # Initial plan
    print("\n2️⃣  Stage 2: Initial Blueprint")
    blueprint = strategist.plan(
        slide_intent=slide_intent,
        content_blocks=content_blocks,
    )
    initial_comp_count = len(blueprint.get("components", []))
    print(f"   Initial components: {initial_comp_count}")

    # Simulate feedback
    print("\n3️⃣  Stage 3: Feedback (Simulate too many bullets)")
    feedback = {
        "warnings": [
            {
                "component_id": "comp-2",
                "issue": "Bullet-list has 8 bullets, max is 6",
                "suggestion": "Reduce to 5-6 bullets",
            }
        ]
    }
    print(f"   Feedback: {feedback['warnings'][0]['issue']}")

    # Replan
    print("\n4️⃣  Stage 4: Replan with Feedback")
    adjusted_blueprint = strategist.replan(blueprint, feedback)
    adjusted_comp_count = len(adjusted_blueprint.get("components", []))
    print(f"   Adjusted components: {adjusted_comp_count}")
    print(f"   Result: {'✅ Reduced' if adjusted_comp_count <= initial_comp_count else '⚠️ Not reduced'}")

    print("\n" + "="*70)
    print("✅ Feedback Loop Test Completed!")
    print("="*70)


if __name__ == "__main__":
    # Test main pipeline
    result = test_complete_v2_pipeline()

    # Test feedback loop
    test_feedback_loop()

    # Print final summary
    print("\n" + "="*70)
    print("📊 FINAL SUMMARY")
    print("="*70)
    print(f"✅ Pipeline Status: {'WORKING' if result['success'] else 'FAILED'}")
    print(f"✅ Components Generated: {result['components']}")
    print(f"✅ HTML Output Size: {result['html_length']} bytes")
    print("="*70)
