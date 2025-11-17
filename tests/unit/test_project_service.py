"""
Unit tests for ProjectService
"""
import pytest
import os
import json
from pathlib import Path
from presentation.api.services.project_service import ProjectService


@pytest.mark.unit
class TestProjectService:
    """Test ProjectService class"""

    def test_list_projects(self, tmp_path):
        """Test listing projects"""
        # Create test project structure
        project1 = tmp_path / "project1"
        project1.mkdir()
        (project1 / "markdown").mkdir()

        project2 = tmp_path / "project2"
        project2.mkdir()
        (project2 / "markdown").mkdir()

        # Create non-project directory
        non_project = tmp_path / "not-a-project"
        non_project.mkdir()

        service = ProjectService(str(tmp_path))
        projects = service.list_projects()

        assert "project1" in projects
        assert "project2" in projects
        assert "not-a-project" not in projects
        assert len(projects) == 2

    def test_is_valid_project(self, tmp_path):
        """Test project validation"""
        service = ProjectService(str(tmp_path))

        # Valid project
        valid_project = tmp_path / "valid"
        valid_project.mkdir()
        (valid_project / "markdown").mkdir()
        assert service._is_valid_project(str(valid_project)) is True

        # Invalid project (no markdown folder)
        invalid_project = tmp_path / "invalid"
        invalid_project.mkdir()
        assert service._is_valid_project(str(invalid_project)) is False

    def test_get_project_path(self, tmp_path):
        """Test getting project path"""
        project_dir = tmp_path / "test-project"
        project_dir.mkdir()
        (project_dir / "markdown").mkdir()

        service = ProjectService(str(tmp_path))
        path = service.get_project_path("test-project")

        assert path == str(project_dir)

    def test_get_project_path_not_found(self, tmp_path):
        """Test getting path for non-existent project"""
        service = ProjectService(str(tmp_path))

        with pytest.raises(ValueError, match="not found"):
            service.get_project_path("non-existent")

    def test_create_project(self, tmp_path):
        """Test creating a new project"""
        service = ProjectService(str(tmp_path))

        project_path = service.create_project("new-project", "github")

        # Check directory structure
        assert os.path.exists(project_path)
        assert os.path.exists(os.path.join(project_path, "markdown", "input"))
        assert os.path.exists(os.path.join(project_path, "markdown", "optimized"))
        assert os.path.exists(os.path.join(project_path, "html"))
        assert os.path.exists(os.path.join(project_path, "styles", "github"))

        # Check PROJECT_SCOPE.md exists
        scope_path = os.path.join(project_path, "PROJECT_SCOPE.md")
        assert os.path.exists(scope_path)

    def test_create_project_invalid_name(self, tmp_path):
        """Test creating project with invalid name"""
        service = ProjectService(str(tmp_path))

        with pytest.raises(ValueError, match="can only contain"):
            service.create_project("invalid/name")

        with pytest.raises(ValueError, match="can only contain"):
            service.create_project("invalid name!")

    def test_create_project_already_exists(self, tmp_path):
        """Test creating project that already exists"""
        service = ProjectService(str(tmp_path))

        # Create first time
        service.create_project("test-project")

        # Try to create again
        with pytest.raises(ValueError, match="already exists"):
            service.create_project("test-project")

    def test_get_project_info(self, tmp_path, sample_markdown_content):
        """Test getting project information"""
        service = ProjectService(str(tmp_path))

        # Create project
        project_path = service.create_project("test-project")

        # Add some test files
        md_file = Path(project_path) / "markdown" / "optimized" / "slide-1.md"
        md_file.write_text(sample_markdown_content)

        html_file = Path(project_path) / "html" / "slide-1.html"
        html_file.write_text("<html>Test</html>")

        # Get info
        info = service.get_project_info("test-project")

        assert info["name"] == "test-project"
        assert info["path"] == project_path
        assert "slide-1" in info["markdown_slides"]
        assert "slide-1" in info["html_slides"]
        assert "github" in info["available_styles"]

    def test_delete_project_empty(self, tmp_path):
        """Test deleting empty project"""
        service = ProjectService(str(tmp_path))

        # Create project
        project_path = service.create_project("test-project")

        # Delete it
        result = service.delete_project("test-project", force=False)

        assert result is True
        assert not os.path.exists(project_path)

    def test_delete_project_with_content_no_force(self, tmp_path):
        """Test deleting project with content without force flag"""
        service = ProjectService(str(tmp_path))

        # Create project with content
        project_path = service.create_project("test-project")
        test_file = Path(project_path) / "markdown" / "optimized" / "test.md"
        test_file.write_text("Content")

        # Try to delete without force
        with pytest.raises(ValueError, match="not empty"):
            service.delete_project("test-project", force=False)

    def test_delete_project_with_force(self, tmp_path):
        """Test deleting project with content using force flag"""
        service = ProjectService(str(tmp_path))

        # Create project with content
        project_path = service.create_project("test-project")
        test_file = Path(project_path) / "markdown" / "optimized" / "test.md"
        test_file.write_text("Content")

        # Delete with force
        result = service.delete_project("test-project", force=True)

        assert result is True
        assert not os.path.exists(project_path)

    def test_rename_project(self, tmp_path):
        """Test renaming a project"""
        service = ProjectService(str(tmp_path))

        # Create project
        old_path = service.create_project("old-name")

        # Rename it
        new_path = service.rename_project("old-name", "new-name")

        assert not os.path.exists(old_path)
        assert os.path.exists(new_path)
        assert new_path.endswith("new-name")

    def test_rename_project_invalid_new_name(self, tmp_path):
        """Test renaming with invalid new name"""
        service = ProjectService(str(tmp_path))

        service.create_project("test-project")

        with pytest.raises(ValueError, match="can only contain"):
            service.rename_project("test-project", "invalid/name")

    def test_rename_project_already_exists(self, tmp_path):
        """Test renaming to existing project name"""
        service = ProjectService(str(tmp_path))

        service.create_project("project-1")
        service.create_project("project-2")

        with pytest.raises(ValueError, match="already exists"):
            service.rename_project("project-1", "project-2")

    def test_get_project_scope(self, tmp_path):
        """Test getting project scope"""
        service = ProjectService(str(tmp_path))

        project_path = service.create_project("test-project")
        scope = service.get_project_scope("test-project")

        # Should return default scope template
        assert "Project Scope" in scope
        assert len(scope) > 0

    def test_update_project_scope(self, tmp_path):
        """Test updating project scope"""
        service = ProjectService(str(tmp_path))

        service.create_project("test-project")

        new_scope = "# Custom Scope\n\nThis is custom content."
        scope_path = service.update_project_scope("test-project", new_scope)

        # Read back and verify
        scope = service.get_project_scope("test-project")
        assert scope == new_scope

    def test_duplicate_style(self, tmp_path):
        """Test duplicating a style theme"""
        service = ProjectService(str(tmp_path))

        # Create project
        project_path = service.create_project("test-project", "github")

        # Create a test file in source style
        source_style_path = Path(project_path) / "styles" / "github"
        test_file = source_style_path / "style.css"
        test_file.write_text("body { color: green; }")

        # Duplicate style
        target_path = service.duplicate_style("test-project", "github", "custom")

        # Verify duplication
        assert os.path.exists(target_path)
        custom_file = Path(target_path) / "style.css"
        assert custom_file.exists()
        assert custom_file.read_text() == "body { color: green; }"

    def test_duplicate_style_not_found(self, tmp_path):
        """Test duplicating non-existent style"""
        service = ProjectService(str(tmp_path))

        service.create_project("test-project")

        with pytest.raises(ValueError, match="not found"):
            service.duplicate_style("test-project", "non-existent", "custom")

    def test_duplicate_style_already_exists(self, tmp_path):
        """Test duplicating to existing style name"""
        service = ProjectService(str(tmp_path))

        project_path = service.create_project("test-project", "github")

        # Create target style manually
        (Path(project_path) / "styles" / "modern").mkdir()

        with pytest.raises(ValueError, match="already exists"):
            service.duplicate_style("test-project", "github", "modern")
