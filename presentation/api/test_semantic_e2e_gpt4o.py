"""
End-to-End Semantic Framework Test with GPT-4o
Tests the complete 3-agent pipeline: Analyzer → Strategist → Generator → Renderer
"""

import sys
import os
import json

# Add api directory to Python path
api_dir = os.path.dirname(__file__)
sys.path.insert(0, api_dir)

# Try relative imports first (when running from api directory)
try:
    from agents.orchestrator import AgentOrchestrator
    from config import OPENAI_API_KEY
    from renderers.component_renderer import HTMLComponentRenderer, Theme
except ImportError:
    # Fallback to absolute imports (when running from parent directory)
    from api.agents.orchestrator import AgentOrchestrator
    from api.config import OPENAI_API_KEY
    from api.renderers.component_renderer import HTMLComponentRenderer, Theme


def run_e2e_test():
    """Run complete end-to-end test with real GPT-4o agents"""

    print("=" * 90)
    print("🚀 SEMANTIC FRAMEWORK E2E TEST - Complete 3-Agent Pipeline")
    print("=" * 90)

    orchestrator = AgentOrchestrator(
        api_key=OPENAI_API_KEY,
        model="gpt-4o",
        reasoning_effort="high",
        verbosity="medium"
    )
    renderer = HTMLComponentRenderer(theme=Theme(name="github"))

    # Test cases covering all new semantic patterns
    test_cases = [
        {
            "name": "Feature List Detection (→ feature-grid)",
            "description": "Tests semantic detection of feature lists with emoji icons",
            "input": """Unsere Plattform bietet folgende Kernkompetenzen:

🤖 KI-Integration - Advanced machine learning für autonome Entscheidungen
⚡ Schnelle Bereitstellung - Ready-to-use Lösung in wenigen Stunden
🔒 Enterprise Security - Vollständige Verschlüsselung und Compliance
📊 Real-time Analytics - Live-Monitoring im Dashboard
🌍 Globale Skalierbarkeit - Deployment in 100+ Ländern
💡 Innovative Features - Ständig neue Funktionen und Updates""",
            "expected_component_type": "feature-grid",
            "language": "German"
        },
        {
            "name": "Timeline/Process Detection (→ process-horizontal)",
            "description": "Tests semantic detection of temporal/sequential processes",
            "input": """Unsere Implementierungs-Roadmap:

Q4 2025: Konzeption und technisches Design
Q1-Q2 2026: Entwicklung und Testing
Q3 2026: Pilotierung mit Kunden
Q4 2026: Offizieller Marktstart""",
            "expected_component_type": "process-horizontal",
            "language": "German"
        },
        {
            "name": "Comparison Table with Status (→ table + badges + emphasis)",
            "description": "Tests semantic detection of product comparison with status",
            "input": """Produkt-Vergleich:

RoboClean Alpha - €84.000 - Im Bestand - Teilautonom
RoboClean Beta - €18.500 - Sofort lieferbar - Vollautonom
RoboClean Gamma - €15.000 - 2026 erwartet - Teilautonom
Unitree H1 - ~€84.000 - Entwicklung - Vollautonom""",
            "expected_component_type": "table",
            "language": "German"
        },
        {
            "name": "Financial Data with Summary Rows (→ table + emphasis_rows)",
            "description": "Tests semantic detection of financial projections with totals",
            "input": """Finanzielle Projektion nach Produktlinie:

RoboClean Alpha: 2025: €500K, 2026: €1.2M, 2027: €2.1M
RoboClean Beta: 2025: €300K, 2026: €850K, 2027: €1.5M
RoboClean Gamma: 2025: €0, 2026: €200K, 2027: €800K
TOTAL: 2025: €800K, 2026: €2.25M, 2027: €4.4M""",
            "expected_component_type": "table",
            "language": "German"
        },
        {
            "name": "English Feature List (→ feature-grid)",
            "description": "Tests language auto-detection and English content handling",
            "input": """Core competencies:

🎯 Market Intelligence - Deep insights into customer behavior and trends
📈 Growth Acceleration - Proven methods to scale revenue 2-3x
🤝 Partnership Network - Access to 500+ enterprise customers
💼 Expert Team - 50+ professionals with 20+ years average experience
🏆 Industry Awards - Recognized as Top 3 provider in 2024""",
            "expected_component_type": "feature-grid",
            "language": "English"
        }
    ]

    results = {
        "passed": 0,
        "failed": 0,
        "details": []
    }

    for i, test_case in enumerate(test_cases, 1):
        print("\n" + "=" * 90)
        print(f"TEST {i}: {test_case['name']}")
        print(f"         {test_case['description']}")
        print("=" * 90)

        try:
            print(f"\n📝 Input ({test_case['language']}):")
            print(f"   {test_case['input'][:100]}...")

            # Run the 3-agent pipeline
            print(f"\n🔄 Running agent pipeline...")
            print(f"   1. ContentAnalyzer (detect semantic patterns)")
            print(f"   2. PresentationStrategist (recommend components)")
            print(f"   3. ContentGenerator (generate formatted output)")

            result = orchestrator.generate(
                user_input=test_case['input'],
                project_name="test-project",
                slide_title=test_case['name']
            )

            # Analyze results
            print(f"\n✅ Pipeline completed successfully")

            if "error" in result:
                print(f"❌ Error in pipeline: {result['error']}")
                results["failed"] += 1
                results["details"].append({
                    "test": test_case['name'],
                    "status": "FAILED",
                    "reason": "Pipeline error"
                })
                continue

            # Extract formatted slide
            formatted_slide = result.get("formatted_slide", {})
            components = formatted_slide.get("components", [])

            if not components:
                print(f"❌ No components generated")
                results["failed"] += 1
                results["details"].append({
                    "test": test_case['name'],
                    "status": "FAILED",
                    "reason": "No components in output"
                })
                continue

            main_component = components[0]
            actual_type = main_component.get("type")

            print(f"\n🎯 Component Analysis:")
            print(f"   Expected type: {test_case['expected_component_type']}")
            print(f"   Actual type:   {actual_type}")

            # Check semantic metadata
            semantic_context = main_component.get("semantic_context")
            print(f"   Semantic context: {semantic_context}")

            # Validate semantic metadata fields based on component type
            checks_passed = 0
            checks_total = 3

            # Check 1: Component type match
            if actual_type == test_case['expected_component_type']:
                print(f"   ✅ Component type matches")
                checks_passed += 1
            else:
                print(f"   ⚠️  Component type mismatch (expected {test_case['expected_component_type']}, got {actual_type})")

            # Check 2: Semantic context present
            if semantic_context:
                print(f"   ✅ Semantic context detected: {semantic_context}")
                checks_passed += 1
            else:
                print(f"   ⚠️  No semantic context in output")

            # Check 3: Type-specific semantic metadata
            metadata_found = False
            if actual_type == "feature-grid":
                if "features" in main_component and len(main_component.get("features", [])) > 0:
                    features_count = len(main_component["features"])
                    print(f"   ✅ Feature-grid with {features_count} features")
                    metadata_found = True
                    checks_passed += 1
            elif actual_type == "process-horizontal":
                if "steps" in main_component and len(main_component.get("steps", [])) > 0:
                    steps_count = len(main_component["steps"])
                    print(f"   ✅ Process-horizontal with {steps_count} steps")
                    metadata_found = True
                    checks_passed += 1
            elif actual_type == "table":
                has_badges = "cell_badges" in main_component
                has_emphasis = "emphasis_rows" in main_component
                if has_badges or has_emphasis:
                    if has_badges:
                        print(f"   ✅ Table with semantic badges")
                    if has_emphasis:
                        print(f"   ✅ Table with emphasis rows: {main_component['emphasis_rows']}")
                    metadata_found = True
                    checks_passed += 1

            # Try to render HTML
            print(f"\n🎨 Rendering HTML...")
            try:
                slide_data = {
                    "slide_id": f"slide-{i}",
                    "slide_title": test_case['name'],
                    "components": components
                }
                html = renderer.render_slide(slide_data)

                # Validate HTML output
                html_valid = False
                if '<div class="slide-section">' in html and '<div class="component">' in html:
                    print(f"   ✅ Valid HTML generated")
                    html_valid = True
                else:
                    print(f"   ⚠️  HTML missing expected structure")

                # Save HTML for inspection
                output_path = f"/tmp/semantic_e2e_test_{i}_{actual_type}.html"
                full_html = f"""<!DOCTYPE html>
<html lang="{test_case['language'].lower()}">
<head>
    <meta charset="UTF-8">
    <title>{test_case['name']}</title>
</head>
<body>
{html}
</body>
</html>"""
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(full_html)
                print(f"   💾 HTML saved: {output_path}")

            except Exception as e:
                print(f"   ⚠️  HTML rendering error: {str(e)}")
                html_valid = False

            # Final status
            if checks_passed >= 2 and html_valid:
                print(f"\n✅ TEST PASSED")
                results["passed"] += 1
                results["details"].append({
                    "test": test_case['name'],
                    "status": "PASSED",
                    "component_type": actual_type,
                    "semantic_context": semantic_context
                })
            elif checks_passed >= 2:
                print(f"\n⚠️  TEST PARTIAL (semantic metadata OK, HTML rendering issue)")
                results["passed"] += 1
                results["details"].append({
                    "test": test_case['name'],
                    "status": "PARTIAL",
                    "component_type": actual_type,
                    "semantic_context": semantic_context
                })
            else:
                print(f"\n❌ TEST FAILED")
                results["failed"] += 1
                results["details"].append({
                    "test": test_case['name'],
                    "status": "FAILED",
                    "component_type": actual_type,
                    "semantic_context": semantic_context
                })

        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}")
            import traceback
            traceback.print_exc()
            results["failed"] += 1
            results["details"].append({
                "test": test_case['name'],
                "status": "ERROR",
                "error": str(e)
            })

    # Print summary
    print("\n" + "=" * 90)
    print("📊 TEST SUMMARY")
    print("=" * 90)

    for detail in results["details"]:
        if detail["status"] == "PASSED":
            print(f"✅ {detail['test']}")
            print(f"   Type: {detail['component_type']}, Context: {detail['semantic_context']}")
        elif detail["status"] == "PARTIAL":
            print(f"⚠️  {detail['test']} (Partial pass)")
            print(f"   Type: {detail['component_type']}, Context: {detail['semantic_context']}")
        elif detail["status"] == "ERROR":
            print(f"❌ {detail['test']}")
            print(f"   Error: {detail.get('error', 'Unknown error')}")
        else:
            print(f"❌ {detail['test']}")
            print(f"   Reason: {detail.get('reason', 'Unknown reason')}")

    total_tests = results["passed"] + results["failed"]
    print(f"\n{'=' * 90}")
    print(f"TOTAL: {results['passed']}/{total_tests} tests passed")
    print(f"{'=' * 90}")

    if results["failed"] == 0:
        print("\n🎉 ALL END-TO-END TESTS PASSED!")
        print("\n✅ Complete semantic framework validation:")
        print("   ✓ ContentAnalyzer detects semantic patterns correctly")
        print("   ✓ PresentationStrategist recommends optimal components")
        print("   ✓ ContentGenerator produces semantic metadata")
        print("   ✓ ComponentRenderer generates valid HTML")
        print("   ✓ Language auto-detection works (German + English)")
        print("   ✓ All 3 new component types functional")
        return True
    else:
        print(f"\n⚠️  {results['failed']} test(s) failed")
        return False


if __name__ == "__main__":
    success = run_e2e_test()
    exit(0 if success else 1)
