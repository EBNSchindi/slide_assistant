"""
Demo script to test the renderer without pytest.

Loads example blueprints and renders them to HTML.
"""

import json
from pathlib import Path

from presentation.api.renderer import SlideRenderer
from presentation.api.blueprints.validator import BlueprintValidator


def load_blueprint(filename: str) -> dict:
    """Load a blueprint fixture from JSON file"""
    fixtures_dir = Path(__file__).parent / "tests" / "fixtures" / "blueprints"
    filepath = fixtures_dir / filename
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    print("=" * 60)
    print("BLUEPRINT RENDERER DEMO")
    print("=" * 60)
    print()

    # Initialize renderer
    renderer = SlideRenderer()
    validator = BlueprintValidator(validate_image_paths=False)

    # Test 1: Team Slide
    print("1. Loading team slide blueprint...")
    team_blueprint = load_blueprint("example_team_slide.json")
    print(f"   ✓ Loaded: {team_blueprint['slide_id']}")
    print(f"   Title: {team_blueprint['slide_title']}")
    print(f"   Layout: {team_blueprint['layout_type']}")
    print(f"   Components: {len(team_blueprint['components'])}")
    print()

    print("2. Validating team slide...")
    try:
        validated = validator.validate(team_blueprint)
        print(f"   ✓ Validation passed")
        print(f"   Schema version: {validated.schema_version}")
        print(f"   Language: {validated.language}")
    except Exception as e:
        print(f"   ✗ Validation failed: {e}")
        return
    print()

    print("3. Rendering team slide to HTML...")
    try:
        html, markdown, metadata = renderer.render(team_blueprint, theme="github", validate=False)
        print(f"   ✓ Rendered successfully")
        print(f"   HTML length: {len(html)} characters")
        print(f"   Component count: {metadata['component_count']}")
        print(f"   Theme: {metadata['theme']}")

        # Save to file
        output_dir = Path(__file__).parent / "output"
        output_dir.mkdir(exist_ok=True)
        output_file = output_dir / "team_slide_demo.html"

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"   ✓ Saved to: {output_file}")

    except Exception as e:
        print(f"   ✗ Rendering failed: {e}")
        import traceback
        traceback.print_exc()
        return
    print()

    # Test 2: Problem Slide
    print("4. Loading problem slide blueprint...")
    problem_blueprint = load_blueprint("example_problem_slide.json")
    print(f"   ✓ Loaded: {problem_blueprint['slide_id']}")
    print(f"   Title: {problem_blueprint['slide_title']}")
    print()

    print("5. Rendering problem slide to HTML...")
    try:
        html, markdown, metadata = renderer.render(problem_blueprint, theme="github", validate=False)
        print(f"   ✓ Rendered successfully")
        print(f"   HTML length: {len(html)} characters")

        output_file = output_dir / "problem_slide_demo.html"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"   ✓ Saved to: {output_file}")

    except Exception as e:
        print(f"   ✗ Rendering failed: {e}")
        import traceback
        traceback.print_exc()
        return
    print()

    # Show HTML preview
    print("6. HTML Preview (first 500 chars of team slide):")
    print("-" * 60)
    print(html[:500])
    print("...")
    print("-" * 60)
    print()

    print("=" * 60)
    print("✅ ALL TESTS PASSED!")
    print("=" * 60)
    print()
    print("Output files:")
    print(f"  - {output_dir / 'team_slide_demo.html'}")
    print(f"  - {output_dir / 'problem_slide_demo.html'}")
    print()
    print("Open these files in a browser to see the rendered slides.")
    print()


if __name__ == "__main__":
    main()
