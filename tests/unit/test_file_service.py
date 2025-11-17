"""
Unit tests for FileService
"""
import pytest
import os
from pathlib import Path
from presentation.api.services.file_service import FileService


@pytest.mark.unit
class TestFileService:
    """Test FileService class"""

    def test_init_creates_directories(self, temp_project_dir):
        """Test that FileService creates necessary directories"""
        service = FileService(str(temp_project_dir))

        assert service.project_path == str(temp_project_dir)
        assert os.path.exists(service.markdown_optimized_path)
        assert os.path.exists(service.html_path)

    def test_save_markdown_slide(self, temp_project_dir, sample_markdown_content):
        """Test saving markdown slide"""
        service = FileService(str(temp_project_dir))

        filepath = service.save_markdown_slide("test-slide", sample_markdown_content)

        assert os.path.exists(filepath)
        assert filepath.endswith("test-slide.md")

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        assert content == sample_markdown_content

    def test_save_html_slide(self, temp_project_dir, sample_html_content):
        """Test saving HTML slide"""
        service = FileService(str(temp_project_dir))

        filepath = service.save_html_slide("test-slide", sample_html_content)

        assert os.path.exists(filepath)
        assert filepath.endswith("test-slide.html")

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        assert content == sample_html_content

    def test_sanitize_filename(self, temp_project_dir):
        """Test filename sanitization"""
        service = FileService(str(temp_project_dir))

        # Test various problematic filenames
        assert service._sanitize_filename("Test Slide") == "test-slide"
        assert service._sanitize_filename("Test/Slide") == "testslide"
        assert service._sanitize_filename("Test:Slide") == "testslide"
        assert service._sanitize_filename("Test*Slide?") == "testslide"
        assert service._sanitize_filename("  Test Slide  ") == "test-slide"

    def test_save_slides_multiple(self, temp_project_dir, sample_markdown_content, sample_html_content):
        """Test saving multiple slides at once"""
        service = FileService(str(temp_project_dir))

        slides = [
            {
                "name": "slide-1",
                "markdown": sample_markdown_content,
                "html": sample_html_content
            },
            {
                "name": "slide-2",
                "markdown": sample_markdown_content,
                "html": sample_html_content
            }
        ]

        results = service.save_slides(slides)

        assert len(results["markdown"]) == 2
        assert len(results["html"]) == 2
        assert all(os.path.exists(p) for p in results["markdown"])
        assert all(os.path.exists(p) for p in results["html"])

    def test_list_slides(self, temp_project_dir, sample_markdown_content, sample_html_content):
        """Test listing slides"""
        service = FileService(str(temp_project_dir))

        # Save some test slides
        service.save_markdown_slide("slide-1", sample_markdown_content)
        service.save_markdown_slide("slide-2", sample_markdown_content)
        service.save_html_slide("slide-1", sample_html_content)

        slides = service.list_slides()

        assert "slide-1" in slides["markdown"]
        assert "slide-2" in slides["markdown"]
        assert "slide-1" in slides["html"]
        assert len(slides["markdown"]) == 2
        assert len(slides["html"]) == 1

    def test_get_slide_content(self, temp_project_dir, sample_markdown_content, sample_html_content):
        """Test getting slide content"""
        service = FileService(str(temp_project_dir))

        # Save slide
        service.save_markdown_slide("test-slide", sample_markdown_content)
        service.save_html_slide("test-slide", sample_html_content)

        # Get content
        md_content, html_content = service.get_slide_content("test-slide")

        assert md_content == sample_markdown_content
        assert html_content == sample_html_content

    def test_get_slide_content_missing(self, temp_project_dir):
        """Test getting content for non-existent slide"""
        service = FileService(str(temp_project_dir))

        md_content, html_content = service.get_slide_content("non-existent")

        assert md_content == ""
        assert html_content == ""

    def test_backup_slide(self, temp_project_dir, sample_markdown_content, sample_html_content):
        """Test creating backup of slide"""
        service = FileService(str(temp_project_dir))

        # Create original slide
        service.save_markdown_slide("test-slide", sample_markdown_content)
        service.save_html_slide("test-slide", sample_html_content)

        # Create backup
        service.backup_slide("test-slide")

        # Check backup directory was created
        backup_dir = os.path.join(temp_project_dir, "backups")
        assert os.path.exists(backup_dir)

        # Check backup files exist
        backups = os.listdir(backup_dir)
        assert len(backups) >= 1  # At least one timestamp folder

    def test_save_slide_variants(self, temp_project_dir):
        """Test saving slide variants"""
        service = FileService(str(temp_project_dir))

        variants = [
            {
                "profile": "corporate",
                "html_content": "<html>Corporate variant</html>",
                "markdown_content": "# Corporate variant",
                "components_used": ["stat-grid"]
            },
            {
                "profile": "creative",
                "html_content": "<html>Creative variant</html>",
                "markdown_content": "# Creative variant",
                "components_used": ["quote"]
            },
            {
                "profile": "minimal",
                "html_content": "<html>Minimal variant</html>",
                "markdown_content": "# Minimal variant",
                "components_used": ["text"]
            }
        ]

        result = service.save_slide_variants("test-slide", variants)

        assert len(result["markdown_paths"]) == 3
        assert len(result["html_paths"]) == 3
        assert os.path.exists(result["metadata_path"])

        # Check files exist
        assert all(os.path.exists(p) for p in result["markdown_paths"])
        assert all(os.path.exists(p) for p in result["html_paths"])

    def test_get_slide_variants(self, temp_project_dir):
        """Test getting slide variants"""
        service = FileService(str(temp_project_dir))

        # First save variants
        variants = [
            {
                "profile": "corporate",
                "html_content": "<html>Corporate</html>",
                "markdown_content": "# Corporate",
                "components_used": ["stat-grid"]
            }
        ]
        service.save_slide_variants("test-slide", variants)

        # Now get variants
        result = service.get_slide_variants("test-slide")

        assert result["found"] is True
        assert "metadata" in result
        assert len(result["metadata"]["variants"]) == 1

    def test_get_slide_variants_not_found(self, temp_project_dir):
        """Test getting variants for non-existent slide"""
        service = FileService(str(temp_project_dir))

        result = service.get_slide_variants("non-existent")

        assert result["found"] is False
        assert result["variants"] == []
