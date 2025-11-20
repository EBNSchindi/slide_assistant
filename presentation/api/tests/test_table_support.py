"""
Test Table Support - Verify table template with badges works correctly
"""

from renderers.component_renderer import HTMLComponentRenderer, Theme

# Test data matching Folie 04 structure
test_slide = {
    "slide_id": "slide-2000",
    "slide_title": "Test: Tabellen-Support mit Badges",
    "theme": "github",
    "components": [
        {
            "type": "table",
            "title": "Roboter-Modell Vergleich",
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
            }
        }
    ],
}

def test_table_support():
    """Test the table template with badges and CSS classes"""
    print("=" * 70)
    print("TESTING TABLE SUPPORT WITH BADGES")
    print("=" * 70)

    renderer = HTMLComponentRenderer(theme=Theme(name="github"))
    html = renderer.render_slide(test_slide)

    print("\n📝 Generated HTML (Table with Badges):\n")
    print(html)
    print("\n" + "=" * 70)
    print("VALIDATION CHECKS")
    print("=" * 70)

    checks = [
        ('<table class="comparison-table">', "✓ Table: CSS class 'comparison-table'"),
        ('<h2>Roboter-Modell Vergleich</h2>', "✓ Table: title heading"),
        ('<th>Roboter-Modell</th>', "✓ Table: header cell 1"),
        ('<th>Autonomiegrad</th>', "✓ Table: header cell 2"),
        ('<th>Einsatzbereich</th>', "✓ Table: header cell 3"),
        ('<th>Verfügbarkeit</th>', "✓ Table: header cell 4"),
        ('<td>RoboClean Alpha</td>', "✓ Table: data cell (row 1, col 1)"),
        ('<td>Teilautonom</td>', "✓ Table: data cell (row 1, col 2)"),
        ('<td>Gebäudereinigung</td>', "✓ Table: data cell (row 1, col 3)"),
        ('<span class="badge badge-success">Verfügbar</span>', "✓ Badge: success type (Verfügbar)"),
        ('<span class="badge badge-warning">2026</span>', "✓ Badge: warning type (2026)"),
        ('<tbody>', "✓ Table: tbody structure"),
        ('<thead>', "✓ Table: thead structure"),
        ('style="', "✗ NO inline styles"),
    ]

    results = {"passed": 0, "failed": 0}

    for check_str, message in checks:
        is_positive_check = message.startswith("✓")
        found = check_str in html

        if is_positive_check:
            if found:
                print(f"✅ {message}")
                results["passed"] += 1
            else:
                print(f"❌ MISSING: {message}")
                results["failed"] += 1
        else:
            if not found:
                print(f"✅ {message}")
                results["passed"] += 1
            else:
                print(f"❌ FOUND: {message}")
                results["failed"] += 1

    print("\n" + "=" * 70)
    print(f"RESULTS: {results['passed']} passed, {results['failed']} failed")
    print("=" * 70)

    if results["failed"] == 0:
        print("\n🎉 TABLE SUPPORT WITH BADGES WORKING PERFECTLY!")
        print("\nNext step: Test with v2 API to generate real table from user input.")
    else:
        print(f"\n⚠️  {results['failed']} checks failed.")

    return results["failed"] == 0


if __name__ == "__main__":
    success = test_table_support()
    exit(0 if success else 1)
