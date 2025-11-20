"""
Test Template System - Verify Jinja2 templates work correctly
"""

from renderers.component_renderer import HTMLComponentRenderer, Theme

# Test data (same as before, but now rendered via templates)
test_slide = {
    "slide_id": "slide-1000",
    "slide_title": "Test: Template System",
    "theme": "github",
    "components": [
        {
            "type": "stat-grid",
            "title": "Template-Based Statistics",
            "statistics": [
                {"value": "100%", "label": "Template Coverage"},
                {"value": "0", "label": "Inline Styles"},
                {"value": "7", "label": "Jinja2 Templates"},
            ],
        },
        {
            "type": "bullet-list",
            "title": "Benefits of Template System",
            "bullets": [
                "100% consistent HTML structure",
                "Easy to maintain and extend",
                "No inline styles - pure CSS classes",
                "Type-safe rendering with Jinja2",
            ],
        },
    ],
}

def test_template_system():
    """Test the new template-based renderer"""
    print("=" * 70)
    print("TESTING JINJA2 TEMPLATE SYSTEM")
    print("=" * 70)

    renderer = HTMLComponentRenderer(theme=Theme(name="github"))
    html = renderer.render_slide(test_slide)

    print("\n📝 Generated HTML (via Jinja2 Templates):\n")
    print(html)
    print("\n" + "=" * 70)
    print("VALIDATION CHECKS")
    print("=" * 70)

    checks = [
        ('<div class="slide-section">', "✓ Template: slide-section wrapper"),
        ('<div class="component" id="slide-1000-comp-1"', "✓ Template: component wrapper with ID"),
        ('<div class="component-label">Komponente 1000.1</div>', "✓ Template: component label"),
        ('<div class="stat-grid">', "✓ Template: stat-grid container"),
        ('<div class="stat-card">', "✓ Template: stat-card"),
        ('<span class="stat-number">', "✓ Template: stat-number (span)"),
        ('<span class="stat-label">', "✓ Template: stat-label (span)"),
        ('<h2>Template-Based Statistics</h2>', "✓ Template: h2 heading"),
        ('<ul class="bullet-list">', "✓ Template: bullet-list"),
        ('style="', "✗ NO inline styles"),
        ('<div class="slide-component"', "✗ OLD class names"),
        ('<h3 class="component-title">', "✗ OLD heading level"),
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
        print("\n🎉 TEMPLATE SYSTEM WORKING PERFECTLY!")
        print("\nNext step: Test with v2 API to generate real slides.")
    else:
        print(f"\n⚠️  {results['failed']} checks failed.")

    return results["failed"] == 0


if __name__ == "__main__":
    success = test_template_system()
    exit(0 if success else 1)
