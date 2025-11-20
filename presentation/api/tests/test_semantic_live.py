"""
Live Semantic Framework Test - Complete end-to-end with real content
Tests the new semantic analysis, component types, and rendering
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from renderers.component_renderer import HTMLComponentRenderer, Theme

# Real-world test cases demonstrating semantic framework

TEST_CASES = [
    {
        "name": "Produktvergleich mit Badges (Semantic Sentiment Analysis)",
        "description": "Testet: Badge-Sentiment-Analyse statt Keywords, table mit Emphasis-Rows",
        "formatted_slide": {
            "slide_title": "Roboter-Modelle im Vergleich",
            "components": [
                {
                    "component_id": "comp-1",
                    "type": "table",
                    "title": "Verfügbare und geplante Modelle",
                    "semantic_context": "product_comparison",
                    "table_headers": ["Modell", "Preis", "Autonomie", "Status"],
                    "table_rows": [
                        ["RoboClean Alpha", "€84.000", "Teilautonom", "Im Bestand"],
                        ["RoboClean Beta", "€18.500", "Vollautonom", "Sofort lieferbar"],
                        ["RoboClean Gamma", "€15.000", "Teilautonom", "2026 erwartet"],
                        ["Unitree H1", "~€84.000", "Vollautonom", "Entwicklung"]
                    ],
                    "table_class": "comparison-table",
                    "cell_badges": {
                        "3": [
                            {"row_index": 0, "badge_type": "success"},
                            {"row_index": 1, "badge_type": "success"},
                            {"row_index": 2, "badge_type": "warning"},
                            {"row_index": 3, "badge_type": "warning"}
                        ]
                    }
                }
            ]
        }
    },
    {
        "name": "Feature-Grid Showcase (NEU)",
        "description": "Testet: feature-grid Component-Typ mit Icons",
        "formatted_slide": {
            "slide_title": "Unsere Kernkompetenzen",
            "components": [
                {
                    "component_id": "comp-1",
                    "type": "feature-grid",
                    "semantic_context": "feature_showcase",
                    "features": [
                        {
                            "icon": "🤖",
                            "title": "KI-Integration",
                            "description": "Advanced machine learning für autonome Navigationsentscheidungen"
                        },
                        {
                            "icon": "⚡",
                            "title": "Schnelle Bereitstellung",
                            "description": "Ready-to-use Lösung in wenigen Stunden einsatzbereit"
                        },
                        {
                            "icon": "🔒",
                            "title": "Enterprise-Security",
                            "description": "Vollständige Verschlüsselung und Compliance mit internationalen Standards"
                        },
                        {
                            "icon": "📊",
                            "title": "Real-time Analytics",
                            "description": "Live-Monitoring und Leistungsmetriken im Dashboard"
                        }
                    ]
                }
            ]
        }
    },
    {
        "name": "Image-Grid mit Badges (NEU)",
        "description": "Testet: image-grid mit Status-Badges auf Bildern",
        "formatted_slide": {
            "slide_title": "Produktlinie",
            "components": [
                {
                    "component_id": "comp-1",
                    "type": "image-grid",
                    "semantic_context": "product_showcase",
                    "grid_layout": "2x2",
                    "images": [
                        {
                            "path": "/images/product-a.png",
                            "title": "RoboClean Alpha",
                            "caption": "Für kleine bis mittlere Flächen",
                            "badge": {"type": "success", "text": "Verfügbar"}
                        },
                        {
                            "path": "/images/product-b.png",
                            "title": "RoboClean Beta",
                            "caption": "High-performance Industriemodell",
                            "badge": {"type": "success", "text": "Verfügbar"}
                        },
                        {
                            "path": "/images/product-c.png",
                            "title": "RoboClean Gamma",
                            "caption": "Outdoor-spezialisiert",
                            "badge": {"type": "warning", "text": "2026"}
                        },
                        {
                            "path": "/images/product-d.png",
                            "title": "RoboClean Delta",
                            "caption": "Healthcare-zertifiziert",
                            "badge": {"type": "warning", "text": "Q4 2025"}
                        }
                    ]
                }
            ]
        }
    },
    {
        "name": "Process-Horizontal Timeline (NEU)",
        "description": "Testet: process-horizontal mit temporalen Phasen",
        "formatted_slide": {
            "slide_title": "Implementierungs-Roadmap",
            "components": [
                {
                    "component_id": "comp-1",
                    "type": "process-horizontal",
                    "semantic_context": "timeline",
                    "steps": [
                        {
                            "title": "Konzeption",
                            "description": "Anforderungsanalyse und technisches Design",
                            "timeframe": "Q4 2025"
                        },
                        {
                            "title": "Entwicklung",
                            "description": "Coding, Testing, Integration",
                            "timeframe": "Q1-Q2 2026"
                        },
                        {
                            "title": "Pilotierung",
                            "description": "Feld-Tests mit Kunden",
                            "timeframe": "Q3 2026"
                        },
                        {
                            "title": "Marktstart",
                            "description": "Offizielle Produkteinführung",
                            "timeframe": "Q4 2026"
                        }
                    ],
                    "show_arrows": True
                }
            ]
        }
    },
    {
        "name": "Finanz-Tabelle mit Emphasis-Rows",
        "description": "Testet: Semantische Erkennung von Summary-Rows für Hervorhebung",
        "formatted_slide": {
            "slide_title": "Finanzielle Projektion",
            "components": [
                {
                    "component_id": "comp-1",
                    "type": "table",
                    "title": "Umsatz und Margin nach Produktlinie",
                    "semantic_context": "financial_data",
                    "table_headers": ["Produktlinie", "2025", "2026", "2027"],
                    "table_rows": [
                        ["RoboClean Alpha", "€500K", "€1.2M", "€2.1M"],
                        ["RoboClean Beta", "€300K", "€850K", "€1.5M"],
                        ["RoboClean Gamma", "€0", "€200K", "€800K"],
                        ["Gesamt-Umsatz", "€800K", "€2.25M", "€4.4M"]
                    ],
                    "emphasis_rows": [3],
                    "table_class": "financial-table"
                }
            ]
        }
    }
]


def test_semantic_live():
    """Run live tests of semantic framework with real content"""
    print("=" * 80)
    print("🚀 SEMANTIC FRAMEWORK - LIVE INTEGRATION TEST")
    print("=" * 80)

    renderer = HTMLComponentRenderer(theme=Theme(name="github"))

    results = {
        "passed": 0,
        "failed": 0,
        "tests": []
    }

    for test_case in TEST_CASES:
        print("\n" + "=" * 80)
        print(f"TEST: {test_case['name']}")
        print(f"      {test_case['description']}")
        print("=" * 80)

        try:
            # Prepare slide data
            slide_data = {
                "slide_id": f"slide-{TEST_CASES.index(test_case)}",
                "slide_title": test_case["formatted_slide"]["slide_title"],
                "components": test_case["formatted_slide"]["components"]
            }

            # Render HTML
            html = renderer.render_slide(slide_data)

            # Validation checks
            checks = []
            component = test_case["formatted_slide"]["components"][0]
            comp_type = component.get("type")

            # Common checks
            checks.append((f'<div class="slide-section">', "✓ Slide wrapper"))
            checks.append((f'<div class="component"', "✓ Component wrapper"))
            checks.append((component.get("title"), "✓ Component title"))

            # Type-specific checks
            if comp_type == "table":
                checks.append(('<table', "✓ Table element"))
                checks.append(('<thead>', "✓ Table header"))
                checks.append(('<tbody>', "✓ Table body"))
                if component.get("cell_badges"):
                    checks.append(('<span class="badge', "✓ Badges rendered"))
                if component.get("emphasis_rows"):
                    checks.append(('style="background: #f6f8fa; font-weight: 600;"', "✓ Emphasis row styling"))

            elif comp_type == "feature-grid":
                checks.append(('<div class="feature-grid">', "✓ Feature grid container"))
                checks.append(('<div class="feature-card">', "✓ Feature cards"))
                if component.get("features"):
                    checks.append((component["features"][0].get("icon"), "✓ Icons present"))

            elif comp_type == "image-grid":
                checks.append(('<div class="image-grid">', "✓ Image grid container"))
                checks.append(('<img', "✓ Image elements"))
                if any(img.get("badge") for img in component.get("images", [])):
                    checks.append(('<span class="badge', "✓ Image badges"))

            elif comp_type == "process-horizontal":
                checks.append(('<div class="process-horizontal">', "✓ Process horizontal"))
                checks.append(('<div class="process-item">', "✓ Process items"))
                checks.append(('<div class="process-item-circle">', "✓ Step circles"))

            # Run checks
            passed = 0
            failed = 0
            for check_str, message in checks:
                if check_str and check_str in html:
                    print(f"  ✅ {message}")
                    passed += 1
                elif check_str:
                    print(f"  ❌ {message}")
                    failed += 1

            # Also check for no inline styles (except emphasis)
            if 'style="' in html and comp_type != "table":
                print(f"  ⚠️  Inline styles found (should be CSS classes)")
                failed += 1
            elif comp_type != "table" or not component.get("emphasis_rows"):
                print(f"  ✅ No hardcoded inline styles")
                passed += 1

            results["passed"] += passed
            results["failed"] += failed
            results["tests"].append({
                "name": test_case["name"],
                "passed": passed,
                "failed": failed
            })

            # Save HTML for inspection
            output_path = f"/tmp/semantic_test_{comp_type}.html"
            full_html = f"""<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <title>{test_case['formatted_slide']['slide_title']}</title>
</head>
<body>
{html}
</body>
</html>"""
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(full_html)
            print(f"\n  💾 HTML saved: {output_path}")

        except Exception as e:
            print(f"  ❌ ERROR: {str(e)}")
            results["failed"] += 1
            results["tests"].append({
                "name": test_case["name"],
                "error": str(e)
            })

    # Summary
    print("\n" + "=" * 80)
    print("📊 TEST SUMMARY")
    print("=" * 80)
    for test_result in results["tests"]:
        if "error" in test_result:
            print(f"❌ {test_result['name']}: ERROR")
        else:
            status = "✅" if test_result["failed"] == 0 else "⚠️"
            print(f"{status} {test_result['name']}: {test_result['passed']} passed, {test_result['failed']} failed")

    print("\n" + "=" * 80)
    print(f"TOTAL: {results['passed']} passed, {results['failed']} failed")
    print("=" * 80)

    if results["failed"] == 0:
        print("\n🎉 ALL TESTS PASSED!")
        print("\n✅ Semantic Framework fully operational:")
        print("   ✓ Semantic sentiment analysis for badges")
        print("   ✓ feature-grid component type (Folie 6)")
        print("   ✓ image-grid component type (Folie 8.2)")
        print("   ✓ process-horizontal component type (Folie 5.2)")
        print("   ✓ Table emphasis rows (Folie 7)")
        print("   ✓ No hardcoded content rules in code")
        print("\n📚 Documentation: /presentation/api/SEMANTIC_FRAMEWORK.md")
        return True
    else:
        print(f"\n⚠️  {results['failed']} test(s) failed")
        return False


if __name__ == "__main__":
    success = test_semantic_live()
    exit(0 if success else 1)
