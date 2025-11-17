"""
Basic tests for the renderer.

Tests that blueprints can be loaded and rendered to HTML.
"""

import pytest
import json
from pathlib import Path

from presentation.api.renderer import SlideRenderer, RendererError
from presentation.api.blueprints.validator import BlueprintValidator, BlueprintValidationError


# Path to fixtures
FIXTURES_DIR = Path(__file__).parent / "fixtures" / "blueprints"


def load_blueprint(filename: str) -> dict:
    """Load a blueprint fixture from JSON file"""
    filepath = FIXTURES_DIR / filename
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def test_load_team_slide_blueprint():
    """Test that team slide blueprint can be loaded"""
    blueprint = load_blueprint("example_team_slide.json")

    assert blueprint["slide_id"] == "slide-03-team"
    assert blueprint["slide_title"] == "Unser Team"
    assert blueprint["layout_type"] == "two_column"
    assert len(blueprint["components"]) == 2


def test_load_problem_slide_blueprint():
    """Test that problem slide blueprint can be loaded"""
    blueprint = load_blueprint("example_problem_slide.json")

    assert blueprint["slide_id"] == "slide-01-problem"
    assert blueprint["slide_title"] == "Das Problem"
    assert blueprint["layout_type"] == "single_column"
    assert len(blueprint["components"]) == 1


def test_validate_team_slide():
    """Test that team slide blueprint validates correctly"""
    blueprint = load_blueprint("example_team_slide.json")
    validator = BlueprintValidator(validate_image_paths=False)

    # Should not raise exception
    validated = validator.validate(blueprint)

    assert validated.slide_id == "slide-03-team"
    assert validated.layout_type.value == "two_column"
    assert len(validated.components) == 2


def test_validate_problem_slide():
    """Test that problem slide blueprint validates correctly"""
    blueprint = load_blueprint("example_problem_slide.json")
    validator = BlueprintValidator(validate_image_paths=False)

    # Should not raise exception
    validated = validator.validate(blueprint)

    assert validated.slide_id == "slide-01-problem"
    assert validated.layout_type.value == "single_column"
    assert len(validated.components) == 1


def test_render_team_slide():
    """Test rendering team slide to HTML"""
    blueprint = load_blueprint("example_team_slide.json")
    renderer = SlideRenderer()

    html, markdown, metadata = renderer.render(blueprint, theme="github", validate=False)

    # Check HTML was generated
    assert html is not None
    assert len(html) > 0

    # Check basic HTML structure
    assert "<!DOCTYPE html>" in html
    assert "slide-03-team" in html
    assert "Unser Team" in html

    # Check components rendered
    assert "stat-grid" in html
    assert "image-frame" in html

    # Check metadata
    assert metadata["component_count"] == 2
    assert metadata["layout_type"] == "two_column"
    assert metadata["theme"] == "github"


def test_render_problem_slide():
    """Test rendering problem slide to HTML"""
    blueprint = load_blueprint("example_problem_slide.json")
    renderer = SlideRenderer()

    html, markdown, metadata = renderer.render(blueprint, theme="github", validate=False)

    # Check HTML was generated
    assert html is not None
    assert len(html) > 0

    # Check basic HTML structure
    assert "<!DOCTYPE html>" in html
    assert "slide-01-problem" in html
    assert "Das Problem" in html

    # Check bullet list rendered
    assert "bullet-list" in html
    assert "Manuelle Prozesse" in html

    # Check metadata
    assert metadata["component_count"] == 1
    assert metadata["layout_type"] == "single_column"


def test_invalid_layout_positions():
    """Test that invalid layout/position combinations are caught"""
    blueprint = load_blueprint("example_team_slide.json")

    # Modify to have invalid positions for two_column layout
    blueprint["components"][0]["position"] = "top"
    blueprint["components"][1]["position"] = "bottom"

    validator = BlueprintValidator(validate_image_paths=False)

    with pytest.raises(BlueprintValidationError) as excinfo:
        validator.validate(blueprint)

    assert "two_column layout requires 'left' and 'right' positions" in str(excinfo.value)


def test_missing_template():
    """Test that missing templates raise appropriate errors"""
    blueprint = load_blueprint("example_team_slide.json")

    # Change component type to something that doesn't have a template
    blueprint["components"][0]["type"] = "nonexistent_component"

    renderer = SlideRenderer()

    with pytest.raises(RendererError) as excinfo:
        renderer.render(blueprint, validate=False)

    assert "Component template not found" in str(excinfo.value)


if __name__ == "__main__":
    # Run tests manually
    print("Testing blueprint loading...")
    test_load_team_slide_blueprint()
    test_load_problem_slide_blueprint()
    print("✓ Blueprint loading works\n")

    print("Testing blueprint validation...")
    test_validate_team_slide()
    test_validate_problem_slide()
    print("✓ Blueprint validation works\n")

    print("Testing rendering...")
    test_render_team_slide()
    test_render_problem_slide()
    print("✓ Rendering works\n")

    print("All basic tests passed! ✅")
