"""
Test script to verify Component Renderer fixes

Tests that the renderer now outputs HTML matching the reference structure.
"""

from renderers.component_renderer import HTMLComponentRenderer, Theme

# Create test data
test_slide = {
    "slide_id": "slide-999",
    "slide_title": "Test: Renderer Fix Verification",
    "theme": "github",
    "components": [
        {
            "type": "stat-grid",
            "title": "Marktstatistiken",
            "statistics": [
                {"value": "18.000", "label": "Einheiten 2025"},
                {"value": ">1 Mrd.", "label": "Roboter bis 2050"},
                {"value": "$5 Billionen", "label": "Marktvolumen 2050"},
            ],
        },
        {
            "type": "bullet-list",
            "title": "Schlüssel-Deployments",
            "bullets": [
                "GXO × Agility: Logistikbetrieb seit 2024",
                "BMW × Figure: Produktionseinsatz 2024",
                "Neura Robotics: Serienstart 2025",
            ],
        },
        {
            "type": "text",
            "title": "Marktanalyse",
            "paragraphs": [
                "Marktreife Modelle werden bis 2025 erwartet, welche den Robotikmarkt revolutionieren können.",
                "Die Zukunftsprognosen deuten auf ein enormes Wachstum hin, mit über einer Milliarde Robotern bis 2050.",
            ],
        },
    ],
}

def test_renderer():
    """Test the renderer with fixed structure"""
    print("=" * 70)
    print("TESTING COMPONENT RENDERER FIXES")
    print("=" * 70)

    renderer = HTMLComponentRenderer(theme=Theme(name="github"))
    html = renderer.render_slide(test_slide)

    print("\n📝 Generated HTML:\n")
    print(html)
    print("\n" + "=" * 70)
    print("VALIDATION CHECKS")
    print("=" * 70)

    checks = [
        ('<div class="slide-section">', "✓ Correct wrapper: div.slide-section"),
        ('<section class="slide"', "✗ Wrong wrapper: section.slide"),
        ('<div class="component" id="slide-999-comp-1"', "✓ Correct component class: .component"),
        ('<div class="slide-component"', "✗ Wrong component class: .slide-component"),
        ('<div class="component-label">Komponente 999.1</div>', "✓ Component label present"),
        ('id="slide-999-comp-1"', "✓ Correct ID format: slide-X-comp-Y"),
        ('id="comp-1"', "✗ Wrong ID format: comp-X"),
        ('<div class="stat-card">', "✓ Correct stat class: .stat-card"),
        ('<div class="stat-item">', "✗ Wrong stat class: .stat-item"),
        ('<span class="stat-number">', "✓ Correct stat tag: <span>"),
        ('<div class="stat-value"', "✗ Wrong stat tag: <div>"),
        ('<h2>', "✓ Correct heading: <h2>"),
        ('<h3 class="component-title">', "✗ Wrong heading: <h3>"),
        ('style="', "✗ Inline styles found"),
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
        print("\n🎉 ALL CHECKS PASSED! Renderer is fixed correctly.")
    else:
        print(f"\n⚠️  {results['failed']} checks failed. Review the HTML above.")

    return results["failed"] == 0


if __name__ == "__main__":
    success = test_renderer()
    exit(0 if success else 1)
