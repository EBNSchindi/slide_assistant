import os
import json
from typing import List, Dict, Optional
from pathlib import Path


class ProjectService:
    """Handle project management and discovery"""

    def __init__(self, projects_base_path: str):
        self.projects_base_path = projects_base_path

    def list_projects(self) -> List[str]:
        """List all available projects"""
        projects = []

        if not os.path.exists(self.projects_base_path):
            return projects

        for item in os.listdir(self.projects_base_path):
            project_path = os.path.join(self.projects_base_path, item)
            if os.path.isdir(project_path):
                # Check if it has required structure
                if self._is_valid_project(project_path):
                    projects.append(item)

        return sorted(projects)

    def _is_valid_project(self, project_path: str) -> bool:
        """Check if a directory is a valid project"""
        # A valid project should have markdown folder structure
        markdown_path = os.path.join(project_path, "markdown")
        return os.path.exists(markdown_path)

    def get_project_path(self, project_name: str) -> str:
        """Get full path for a project"""
        project_path = os.path.join(self.projects_base_path, project_name)

        if not os.path.exists(project_path):
            raise ValueError(f"Project '{project_name}' not found")

        return project_path

    def create_project(self, project_name: str) -> str:
        """Create a new project structure"""
        project_path = os.path.join(self.projects_base_path, project_name)

        # Create directory structure
        os.makedirs(os.path.join(project_path, "markdown", "input"), exist_ok=True)
        os.makedirs(os.path.join(project_path, "markdown", "optimized"), exist_ok=True)
        os.makedirs(os.path.join(project_path, "html"), exist_ok=True)
        os.makedirs(os.path.join(project_path, "styles", "github"), exist_ok=True)

        return project_path

    def get_project_info(self, project_name: str) -> Dict:
        """Get information about a project"""
        project_path = self.get_project_path(project_name)

        # Get markdown files
        markdown_optimized = os.path.join(project_path, "markdown", "optimized")
        markdown_files = []
        if os.path.exists(markdown_optimized):
            markdown_files = [
                f.replace(".md", "")
                for f in os.listdir(markdown_optimized)
                if f.endswith(".md")
            ]

        # Get HTML files
        html_dir = os.path.join(project_path, "html")
        html_files = []
        if os.path.exists(html_dir):
            html_files = [
                f.replace(".html", "")
                for f in os.listdir(html_dir)
                if f.endswith(".html")
            ]

        # Get styles
        styles_dir = os.path.join(project_path, "styles")
        styles = []
        if os.path.exists(styles_dir):
            styles = [
                d
                for d in os.listdir(styles_dir)
                if os.path.isdir(os.path.join(styles_dir, d))
            ]

        return {
            "name": project_name,
            "path": project_path,
            "markdown_slides": sorted(markdown_files),
            "html_slides": sorted(html_files),
            "available_styles": sorted(styles),
        }

    def duplicate_style(self, project_name: str, source_style: str, target_style: str) -> str:
        """Duplicate a style theme"""
        project_path = self.get_project_path(project_name)
        source_path = os.path.join(project_path, "styles", source_style)
        target_path = os.path.join(project_path, "styles", target_style)

        if not os.path.exists(source_path):
            raise ValueError(f"Source style '{source_style}' not found")

        if os.path.exists(target_path):
            raise ValueError(f"Target style '{target_style}' already exists")

        # Copy style directory
        import shutil

        shutil.copytree(source_path, target_path)
        return target_path
