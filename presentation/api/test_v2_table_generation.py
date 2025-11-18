"""
Test v2 API Table Generation - Full 3-agent pipeline test with table output
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from agents.orchestrator import AgentOrchestrator
from renderers.component_renderer import HTMLComponentRenderer, Theme
import json

# Test with robot model data (like Folie 04)
test_input = """
Unsere Roboter-Modelle

Wir bieten verschiedene Roboter-Modelle für unterschiedliche Einsatzbereiche:

RoboClean Alpha - Teilautonom - Gebäudereinigung - Verfügbar
RoboClean Beta - Vollautonom - Industriehallen - Verfügbar
RoboClean Gamma - Teilautonom - Außenbereiche - 2026
RoboClean Delta - Vollautonom - Krankenhäuser - Ende 2025

Preis: 50.000 - 150.000 €
"""

def test_v2_table_generation():
    """Test the complete v2 pipeline with table generation"""
    print("=" * 70)
    print("V2 API TABLE GENERATION TEST")
    print("=" * 70)

    # Initialize orchestrator
    orchestrator = AgentOrchestrator(
        model="gpt-4o",
        reasoning_effort="medium",
        verbosity="medium",
        use_structured_outputs=False
    )

    print("\n📝 INPUT:")
    print(test_input)
    print("\n" + "=" * 70)

    # Check if we're in TEST_MODE
    from config import TEST_MODE
    if TEST_MODE:
        print("⚠️  Running in TEST_MODE (using mock agents)")
        print("Note: Mock agents don't support table generation yet.")
        print("Set OPENAI_API_KEY in .env to test with real agents.\n")
        return False

    try:
        print("🤖 Running 3-agent pipeline...")
        print("   Agent 1: Content Analyzer")
        print("   Agent 2: Presentation Strategist")
        print("   Agent 3: Content Generator")
        print()

        # Run the full pipeline
        result = orchestrator.generate_slide(
            user_input=test_input,
            slide_title="Roboter-Modelle Übersicht",
            project_name="beispiel-projekt",
            language="de"
        )

        print("=" * 70)
        print("AGENT OUTPUTS")
        print("=" * 70)

        print("\n📊 Agent 1 - Content Blocks:")
        if "content_blocks" in result:
            for i, block in enumerate(result["content_blocks"], 1):
                print(f"  {i}. {block.get('type')}: {block.get('content')[:50]}...")

        print("\n🎨 Agent 2 - Blueprint:")
        if "blueprint" in result:
            blueprint = result["blueprint"]
            print(f"  Layout: {blueprint.get('layout_type')}")
            print(f"  Components: {len(blueprint.get('components', []))}")
            for comp in blueprint.get("components", []):
                print(f"    - {comp.get('type')} (position: {comp.get('position')})")

        print("\n✍️  Agent 3 - Formatted Slide:")
        if "formatted_slide" in result:
            formatted = result["formatted_slide"]
            print(f"  Title: {formatted.get('slide_title')}")
            print(f"  Components: {len(formatted.get('components', []))}")

            for i, comp in enumerate(formatted.get("components", []), 1):
                comp_type = comp.get("type")
                print(f"\n  Component {i} ({comp_type}):")

                if comp_type == "table":
                    print(f"    Table class: {comp.get('table_class')}")
                    print(f"    Headers: {comp.get('table_headers')}")
                    print(f"    Rows: {len(comp.get('table_rows', []))} rows")
                    print(f"    Badges: {comp.get('cell_badges')}")
                elif comp_type == "stat-grid":
                    print(f"    Stats: {len(comp.get('statistics', []))} items")
                elif comp_type == "bullet-list":
                    print(f"    Bullets: {len(comp.get('bullets', []))} items")

        print("\n" + "=" * 70)
        print("HTML RENDERING")
        print("=" * 70)

        # Render to HTML
        if "formatted_slide" in result:
            renderer = HTMLComponentRenderer(theme=Theme(name="github"))

            # Prepare slide data for rendering
            slide_data = {
                "slide_id": "slide-test",
                "slide_title": result["formatted_slide"]["slide_title"],
                "components": result["formatted_slide"]["components"]
            }

            html = renderer.render_slide(slide_data)

            print("\n📄 Generated HTML:\n")
            print(html)

            # Validation checks
            print("\n" + "=" * 70)
            print("VALIDATION CHECKS")
            print("=" * 70)

            checks = [
                ('<table', "✓ Table element present"),
                ('<span class="badge', "✓ Badges present"),
                ('class="comparison-table"', "✓ CSS class 'comparison-table'"),
                ('badge-success', "✓ Success badge"),
                ('badge-warning', "✓ Warning badge"),
                ('<thead>', "✓ Table header"),
                ('<tbody>', "✓ Table body"),
            ]

            passed = 0
            failed = 0

            for check_str, message in checks:
                if check_str in html:
                    print(f"✅ {message}")
                    passed += 1
                else:
                    print(f"❌ MISSING: {message}")
                    failed += 1

            print("\n" + "=" * 70)
            print(f"RESULTS: {passed} passed, {failed} failed")
            print("=" * 70)

            if failed == 0:
                print("\n🎉 V2 API TABLE GENERATION WORKING PERFECTLY!")
                print("\nThe complete pipeline successfully:")
                print("  ✓ Analyzed content (Agent 1)")
                print("  ✓ Planned layout with table component (Agent 2)")
                print("  ✓ Generated formatted table with badges (Agent 3)")
                print("  ✓ Rendered correct HTML with comparison-table class")
            else:
                print(f"\n⚠️  {failed} checks failed.")

            # Save HTML output for inspection
            output_path = "/tmp/test_v2_table_output.html"
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>V2 Table Test</title>
    <link rel="stylesheet" href="../projects/beispiel-projekt/styles/github/style.css">
</head>
<body>
{html}
</body>
</html>""")
            print(f"\n💾 Full HTML saved to: {output_path}")

            return failed == 0
        else:
            print("❌ No formatted_slide in result")
            return False

    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_v2_table_generation()
    exit(0 if success else 1)
