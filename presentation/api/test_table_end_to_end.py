"""
End-to-End Table Test - Simulates Agent 3 output with table data and renders HTML
"""

import sys
import os
api_dir = os.path.dirname(__file__)
sys.path.insert(0, api_dir)

from renderers.component_renderer import HTMLComponentRenderer, Theme

# Simulate what Agent 3 (ContentGeneratorAgentV2) would output for a table
# This mimics the exact output structure from the agent with table_headers, table_rows, etc.
formatted_slide_with_table = {
    "slide_title": "Roboter-Modelle Vergleich",
    "slide_subtitle": None,
    "components": [
        {
            "component_id": "comp-1",
            "type": "table",
            "title": "Verfügbare Modelle",
            "subtitle": None,
            "table_headers": ["Roboter-Modell", "Autonomiegrad", "Einsatzbereich", "Verfügbarkeit"],
            "table_rows": [
                ["RoboClean Alpha", "Teilautonom", "Gebäudereinigung", "Verfügbar"],
                ["RoboClean Beta", "Vollautonom", "Industriehallen", "Verfügbar"],
                ["RoboClean Gamma", "Teilautonom", "Außenbereiche", "2026"],
                ["RoboClean Delta", "Vollautonom", "Krankenhäuser", "Ende 2025"]
            ],
            "table_class": "comparison-table",
            "cell_badges": {
                "3": [
                    {"row_index": 0, "badge_type": "success"},
                    {"row_index": 1, "badge_type": "success"},
                    {"row_index": 2, "badge_type": "warning"},
                    {"row_index": 3, "badge_type": "warning"}
                ]
            },
            "word_count": 32
        }
    ],
    "language": "de",
    "total_word_count": 32,
    "readability_score": "easy"
}

def test_table_end_to_end():
    """Test complete table rendering from formatted data to HTML"""
    print("=" * 70)
    print("END-TO-END TABLE TEST (Agent 3 Output → HTML Renderer)")
    print("=" * 70)

    print("\n📊 Simulated Agent 3 Output (FormattedSlide):")
    print(f"  Title: {formatted_slide_with_table['slide_title']}")
    print(f"  Components: {len(formatted_slide_with_table['components'])}")

    comp = formatted_slide_with_table['components'][0]
    print(f"\n  Component 1 (table):")
    print(f"    Table class: {comp['table_class']}")
    print(f"    Headers: {comp['table_headers']}")
    print(f"    Rows: {len(comp['table_rows'])} rows")
    print(f"    Badges in column 3: {len(comp['cell_badges']['3'])} badges")

    print("\n" + "=" * 70)
    print("HTML RENDERING")
    print("=" * 70)

    # Render with HTMLComponentRenderer
    renderer = HTMLComponentRenderer(theme=Theme(name="github"))

    slide_data = {
        "slide_id": "slide-999",
        "slide_title": formatted_slide_with_table["slide_title"],
        "components": formatted_slide_with_table["components"]
    }

    html = renderer.render_slide(slide_data)

    print("\n📄 Generated HTML:\n")
    print(html)

    # Validation
    print("\n" + "=" * 70)
    print("VALIDATION CHECKS")
    print("=" * 70)

    checks = [
        ('<table class="comparison-table">', "✓ Table with CSS class 'comparison-table'"),
        ('<h2>Verfügbare Modelle</h2>', "✓ Component title"),
        ('<th>Roboter-Modell</th>', "✓ Header: Roboter-Modell"),
        ('<th>Verfügbarkeit</th>', "✓ Header: Verfügbarkeit"),
        ('<td>RoboClean Alpha</td>', "✓ Cell: RoboClean Alpha"),
        ('<td>RoboClean Delta</td>', "✓ Cell: RoboClean Delta"),
        ('<span class="badge badge-success">Verfügbar</span>', "✓ Badge success: Verfügbar"),
        ('<span class="badge badge-warning">2026</span>', "✓ Badge warning: 2026"),
        ('<span class="badge badge-warning">Ende 2025</span>', "✓ Badge warning: Ende 2025"),
        ('<thead>', "✓ Table thead"),
        ('<tbody>', "✓ Table tbody"),
        ('style="', "✗ NO inline styles"),
    ]

    passed = 0
    failed = 0

    for check_str, message in checks:
        is_positive = message.startswith("✓")
        found = check_str in html

        if is_positive:
            if found:
                print(f"✅ {message}")
                passed += 1
            else:
                print(f"❌ MISSING: {message}")
                print(f"   Looking for: {check_str[:60]}...")
                failed += 1
        else:
            if not found:
                print(f"✅ {message}")
                passed += 1
            else:
                print(f"❌ FOUND: {message}")
                failed += 1

    print("\n" + "=" * 70)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 70)

    if failed == 0:
        print("\n🎉 END-TO-END TABLE RENDERING WORKING PERFECTLY!")
        print("\nThe pipeline successfully:")
        print("  ✓ Received formatted table data from Agent 3")
        print("  ✓ Extracted table_headers, table_rows, table_class, cell_badges")
        print("  ✓ Rendered table with comparison-table CSS class")
        print("  ✓ Applied badges (success + warning types)")
        print("  ✓ Matched Folie 04 reference structure")
        print("\n✅ Ready for production use with ContentGeneratorAgentV2!")
    else:
        print(f"\n⚠️  {failed} checks failed.")

    # Save HTML for visual inspection
    output_path = "/tmp/test_table_end_to_end.html"
    full_html = f"""<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Table End-to-End Test</title>
    <link rel="stylesheet" href="{os.path.abspath('../projects/beispiel-projekt/styles/github/style.css')}">
</head>
<body>
{html}
</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_html)

    print(f"\n💾 Full HTML saved to: {output_path}")
    print("   Open in browser to see visual result!")

    return failed == 0


if __name__ == "__main__":
    success = test_table_end_to_end()
    exit(0 if success else 1)
