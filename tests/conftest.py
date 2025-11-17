"""
Pytest configuration and shared fixtures for slide_assistant tests
"""
import os
import sys
import pytest
import tempfile
import shutil
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture(scope="session")
def project_root():
    """Return the project root directory"""
    return PROJECT_ROOT


@pytest.fixture(scope="session")
def test_data_dir(project_root):
    """Return the test data directory"""
    return project_root / "tests" / "data"


@pytest.fixture
def temp_project_dir(tmp_path):
    """Create a temporary project directory for testing"""
    project_dir = tmp_path / "test_project"
    project_dir.mkdir()

    # Create standard project structure
    (project_dir / "markdown" / "input").mkdir(parents=True)
    (project_dir / "markdown" / "optimized").mkdir(parents=True)
    (project_dir / "html").mkdir(parents=True)
    (project_dir / "styles" / "github").mkdir(parents=True)
    (project_dir / "images" / "uploads").mkdir(parents=True)

    # Create PROJECT_SCOPE.md
    scope_file = project_dir / "PROJECT_SCOPE.md"
    scope_file.write_text("# Test Project Scope\n\nThis is a test project.")

    yield project_dir

    # Cleanup is automatic with tmp_path


@pytest.fixture
def mock_api_key():
    """Provide a mock API key for testing"""
    return "sk-test-mock-api-key-12345"


@pytest.fixture
def test_mode():
    """Enable TEST_MODE for tests that don't need real API calls"""
    original_value = os.environ.get("TEST_MODE")
    os.environ["TEST_MODE"] = "true"
    yield True

    # Restore original value
    if original_value is None:
        os.environ.pop("TEST_MODE", None)
    else:
        os.environ["TEST_MODE"] = original_value


@pytest.fixture
def sample_markdown_content():
    """Provide sample markdown content for testing"""
    return """# Test Slide

## Component 1: Statistics
- Revenue: €12.3M
- Growth: 45%
- Markets: 8 new regions

## Component 2: Bullet List
- Key point 1
- Key point 2
- Key point 3
"""


@pytest.fixture
def sample_html_content():
    """Provide sample HTML content for testing"""
    return """<!DOCTYPE html>
<html>
<head>
    <title>Test Slide</title>
</head>
<body>
    <div class="stat-grid">
        <div class="stat-card">
            <div class="stat-number">€12.3M</div>
            <div class="stat-label">Revenue</div>
        </div>
    </div>
</body>
</html>
"""


@pytest.fixture
def sample_style_guide():
    """Provide a sample style guide for testing"""
    return {
        "primary_color": "#238636",
        "secondary_colors": ["#0969da", "#bf8700"],
        "font_family": "sans-serif",
        "available_components": ["stat-grid", "bullet-list", "quote", "text", "image"],
        "spacing_scale": ["16px", "24px", "32px", "48px"],
        "border_radius": "6px",
        "badge_colors": {
            "success": "#238636",
            "warning": "#bf8700",
            "danger": "#d1242f"
        }
    }


@pytest.fixture
def sample_analysis():
    """Provide a sample content analysis for testing"""
    return {
        "content_type": "statistics",
        "key_messages": [
            "45% revenue growth demonstrates strong traction",
            "Expansion into 8 new markets shows scalability",
            "250 new enterprise clients validate product-market fit"
        ],
        "has_statistics": True,
        "has_lists": False,
        "has_quotes": False,
        "has_images": False,
        "confidence_score": 0.95,
        "warnings": [],
        "content_density": "high"
    }


@pytest.fixture
def sample_strategy():
    """Provide a sample presentation strategy for testing"""
    return {
        "recommended_components": [
            {
                "type": "stat-grid",
                "content_indices": [0, 1, 2],
                "layout_position": "top"
            }
        ],
        "component_count": 1,
        "layout_strategy": "single_hero_component",
        "styling_suggestions": [
            "Use large stat-numbers for immediate visual impact",
            "Apply primary color to numbers for emphasis"
        ],
        "reasoning": "Multiple growth metrics form cohesive narrative",
        "cognitive_load_score": "low",
        "accessibility_notes": []
    }


@pytest.fixture(scope="session")
def skip_if_no_api_key():
    """Skip test if OPENAI_API_KEY is not set"""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key or api_key == "mock":
        pytest.skip("OPENAI_API_KEY not set - skipping test requiring real API")


@pytest.fixture
def cleanup_test_files():
    """Cleanup test files after test execution"""
    files_to_cleanup = []

    def register_file(filepath):
        files_to_cleanup.append(filepath)

    yield register_file

    # Cleanup after test
    for filepath in files_to_cleanup:
        if os.path.exists(filepath):
            if os.path.isfile(filepath):
                os.remove(filepath)
            elif os.path.isdir(filepath):
                shutil.rmtree(filepath)
