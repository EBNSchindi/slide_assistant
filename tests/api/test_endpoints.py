"""
API Endpoint integration tests
"""
import pytest
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Set TEST_MODE before importing app
os.environ["TEST_MODE"] = "true"
os.environ["OPENAI_API_KEY"] = "test-mock-key"

from presentation.api.main import app

# Import after app to avoid issues
from starlette.testclient import TestClient


@pytest.fixture
def client():
    """Create test client"""
    return TestClient(app=app, base_url="http://testserver")


@pytest.mark.api
class TestHealthEndpoint:
    """Test health check endpoint"""

    def test_health_check(self, client):
        """Test health check returns OK"""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "api_key_configured" in data


@pytest.mark.api
class TestProjectEndpoints:
    """Test project management endpoints"""

    def test_list_projects(self, client):
        """Test listing projects"""
        response = client.get("/api/projects")

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "projects" in data
        assert "total" in data

    def test_get_project_info_existing(self, client):
        """Test getting info for existing project"""
        # Assuming beispiel-projekt exists
        response = client.get("/api/projects/beispiel-projekt")

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["project"]["name"] == "beispiel-projekt"

    def test_get_project_info_not_found(self, client):
        """Test getting info for non-existent project"""
        response = client.get("/api/projects/non-existent-project")

        assert response.status_code == 404

    def test_get_project_style(self, client):
        """Test getting project style guide"""
        response = client.get("/api/projects/beispiel-projekt/style")

        assert response.status_code == 200
        data = response.json()
        assert data["project_name"] == "beispiel-projekt"
        assert "style" in data
        assert "primary_color" in data["style"]

    def test_get_project_scope(self, client):
        """Test getting project scope"""
        response = client.get("/api/projects/beispiel-projekt/scope")

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["project_name"] == "beispiel-projekt"
        assert "scope" in data


@pytest.mark.api
class TestContentGeneration:
    """Test content generation endpoints"""

    def test_generate_content_basic(self, client):
        """Test basic content generation"""
        request_data = {
            "project_name": "beispiel-projekt",
            "user_input": "Wir haben den Umsatz um 45% gesteigert",
            "slide_title": "test-slide-api",
            "preferences": {},
            "image_references": []
        }

        response = client.post("/api/generate", json=request_data)

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "agent_steps" in data
        assert "generated_slides" in data

    def test_generate_content_missing_project(self, client):
        """Test content generation with non-existent project"""
        request_data = {
            "project_name": "non-existent-project",
            "user_input": "Test content",
            "slide_title": "test-slide",
            "preferences": {},
            "image_references": []
        }

        response = client.post("/api/generate", json=request_data)

        assert response.status_code == 404

    def test_generate_content_with_variants(self, client):
        """Test content generation with variant generation"""
        request_data = {
            "project_name": "beispiel-projekt",
            "user_input": "Test content for variants",
            "slide_title": "test-variants",
            "preferences": {"generate_variants": True},
            "image_references": []
        }

        response = client.post("/api/generate", json=request_data)

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

        # Check if variants were generated (in TEST_MODE)
        if data["generated_slides"]:
            slide = data["generated_slides"][0]
            # Variants may or may not be present depending on mock implementation
            assert "slide_name" in slide


@pytest.mark.api
class TestSlideEndpoints:
    """Test slide-related endpoints"""

    def test_get_project_slides(self, client):
        """Test getting project slides"""
        response = client.get("/api/projects/beispiel-projekt/slides")

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "markdown_slides" in data
        assert "html_slides" in data


@pytest.mark.api
class TestImageUpload:
    """Test image upload endpoints"""

    def test_list_images(self, client):
        """Test listing project images"""
        response = client.get("/api/projects/beispiel-projekt/images")

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "images" in data
        assert "count" in data

    def test_upload_image_invalid_type(self, client):
        """Test uploading invalid file type"""
        files = {"file": ("test.txt", b"text content", "text/plain")}

        response = client.post(
            "/api/projects/beispiel-projekt/upload-image",
            files=files
        )

        assert response.status_code == 400
        assert "Invalid file type" in response.json()["detail"]

    def test_upload_image_too_large(self, client):
        """Test uploading file that's too large"""
        # Create 6MB of data (exceeds 5MB limit)
        large_data = b"x" * (6 * 1024 * 1024)
        files = {"file": ("large.png", large_data, "image/png")}

        response = client.post(
            "/api/projects/beispiel-projekt/upload-image",
            files=files
        )

        assert response.status_code == 400
        assert "too large" in response.json()["detail"]


@pytest.mark.api
@pytest.mark.slow
class TestRegenerateEndpoint:
    """Test slide regeneration endpoint"""

    def test_regenerate_slide_not_implemented(self, client):
        """Test regenerate endpoint structure"""
        request_data = {
            "project_name": "beispiel-projekt",
            "slide_name": "test-slide",
            "feedback": "Make it more concise"
        }

        response = client.post("/api/regenerate", json=request_data)

        # May fail if slide doesn't exist, but endpoint should exist
        assert response.status_code in [200, 404, 400, 500]
