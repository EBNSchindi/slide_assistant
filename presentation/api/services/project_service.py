import os
import json
import shutil
import sys
from typing import List, Dict, Optional
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_logger

logger = get_logger(__name__)


class ProjectService:
    """Handle project management and discovery"""

    def __init__(self, projects_base_path: str):
        self.projects_base_path = projects_base_path
        logger.debug(f"ProjectService initialized with base path: {projects_base_path}")

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

        logger.debug(f"Found {len(projects)} valid projects")
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

    def create_project(self, project_name: str, initial_style: str = "github") -> str:
        """Create a new project structure

        Args:
            project_name: Name for new project
            initial_style: Initial style theme (default: "github")

        Returns:
            Project path
        """
        project_path = os.path.join(self.projects_base_path, project_name)

        # Validate project name
        if not project_name.replace('-', '').replace('_', '').isalnum():
            raise ValueError(
                "Project name can only contain letters, numbers, hyphens, and underscores"
            )

        # Check if project already exists
        if os.path.exists(project_path):
            raise ValueError(f"Project '{project_name}' already exists")

        # Create directory structure
        os.makedirs(os.path.join(project_path, "markdown", "input"), exist_ok=True)
        os.makedirs(os.path.join(project_path, "markdown", "optimized"), exist_ok=True)
        os.makedirs(os.path.join(project_path, "html"), exist_ok=True)
        os.makedirs(os.path.join(project_path, "styles", initial_style), exist_ok=True)

        # Create default PROJECT_SCOPE.md
        scope_path = os.path.join(project_path, "PROJECT_SCOPE.md")
        with open(scope_path, 'w', encoding='utf-8') as f:
            f.write(self._get_default_scope_template())

        # Update projects.json
        self._update_projects_json('add', project_name=project_name, initial_style=initial_style)

        logger.info(f"Created new project: {project_name} with style: {initial_style}")
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
        shutil.copytree(source_path, target_path)
        logger.info(f"Duplicated style '{source_style}' to '{target_style}' in project {project_name}")
        return target_path

    def delete_project(self, project_name: str, force: bool = False) -> bool:
        """Delete a project directory and update projects.json

        Args:
            project_name: Name of project to delete
            force: If True, delete even if directory is not empty

        Returns:
            True if successful

        Raises:
            ValueError: If project doesn't exist or directory not empty (without force)
        """
        project_path = self.get_project_path(project_name)

        # Check if directory is empty (unless force=True)
        if not force:
            # Check if there are any files besides expected structure
            has_content = False
            for root, dirs, files in os.walk(project_path):
                # Skip checking in certain directories
                rel_path = os.path.relpath(root, project_path)
                if any(skip in rel_path for skip in ['.git', '__pycache__', 'venv']):
                    continue
                # Check for meaningful files
                meaningful_files = [f for f in files if not f.startswith('.')]
                if meaningful_files:
                    # Allow PROJECT_SCOPE.md and a few config files
                    content_files = [f for f in meaningful_files if f not in ['PROJECT_SCOPE.md', '.gitkeep']]
                    if content_files:
                        has_content = True
                        break

            if has_content:
                raise ValueError(
                    f"Project '{project_name}' is not empty. Use force=True to delete anyway."
                )

        # Delete directory
        shutil.rmtree(project_path)

        # Update projects.json
        self._update_projects_json('remove', project_name=project_name)

        logger.info(f"Deleted project: {project_name}")
        return True

    def rename_project(self, old_name: str, new_name: str) -> str:
        """Rename a project (directory and projects.json entry)

        Args:
            old_name: Current project name
            new_name: New project name

        Returns:
            New project path

        Raises:
            ValueError: If old project doesn't exist or new name already exists
        """
        # Validate old project exists
        old_path = self.get_project_path(old_name)

        # Validate new name is available
        new_path = os.path.join(self.projects_base_path, new_name)
        if os.path.exists(new_path):
            raise ValueError(f"Project '{new_name}' already exists")

        # Validate new name format (alphanumeric, hyphens, underscores only)
        if not new_name.replace('-', '').replace('_', '').isalnum():
            raise ValueError(
                "Project name can only contain letters, numbers, hyphens, and underscores"
            )

        # Rename directory
        os.rename(old_path, new_path)

        # Update projects.json
        self._update_projects_json('rename', old_name=old_name, new_name=new_name)

        logger.info(f"Renamed project from '{old_name}' to '{new_name}'")
        return new_path

    def get_project_scope(self, project_name: str) -> str:
        """Get project scope/context markdown file content

        Args:
            project_name: Name of project

        Returns:
            Content of PROJECT_SCOPE.md or empty string if doesn't exist
        """
        project_path = self.get_project_path(project_name)
        scope_path = os.path.join(project_path, "PROJECT_SCOPE.md")

        if not os.path.exists(scope_path):
            return ""

        try:
            with open(scope_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error reading scope file for {project_name}: {e}")
            return ""

    def update_project_scope(self, project_name: str, scope_content: str) -> str:
        """Update or create project scope file

        Args:
            project_name: Name of project
            scope_content: Markdown content for scope

        Returns:
            Path to scope file
        """
        project_path = self.get_project_path(project_name)
        scope_path = os.path.join(project_path, "PROJECT_SCOPE.md")

        try:
            with open(scope_path, 'w', encoding='utf-8') as f:
                f.write(scope_content)
            logger.info(f"Updated project scope for: {project_name}")
            return scope_path
        except Exception as e:
            logger.error(f"Failed to write scope file for {project_name}: {e}")
            raise ValueError(f"Failed to write scope file: {e}")

    def _get_default_scope_template(self) -> str:
        """Get default PROJECT_SCOPE.md template"""
        return """# Project Scope

## Overview
Brief description of this presentation project.

## Target Audience
Who is this presentation for? (e.g., investors, clients, internal team)

## Key Objectives
- What are the main goals of this presentation?
- What action should the audience take?

## Key Messages
1. Primary message to convey
2. Supporting points
3. Call to action

## Tone & Style Guidelines
- Professional / Casual / Technical / Creative
- Formal / Informal
- Conservative / Bold

## Content Constraints
- Length: Number of slides expected
- Time: Presentation duration
- Required sections or topics
- Topics to avoid

## Design Preferences
- Visual style preferences
- Color schemes
- Component types preferred (stats, bullet lists, quotes, etc.)

## Brand Guidelines
- Company/product name
- Key terminology to use/avoid
- Brand voice characteristics

## Additional Context
Any other information that will help generate better content for this project.
"""

    def _update_projects_json(self, action: str, **kwargs):
        """Helper to update projects.json file

        Actions: 'add', 'remove', 'rename'
        """
        projects_json_path = os.path.join(
            os.path.dirname(self.projects_base_path),
            'projects.json'
        )

        # Check if projects.json exists
        if not os.path.exists(projects_json_path):
            # If it doesn't exist, create basic structure
            data = {
                "defaultStyle": "github",
                "projects": []
            }
        else:
            try:
                with open(projects_json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except Exception as e:
                logger.error(f"Error reading projects.json: {e}")
                return

        # Perform action
        if action == 'remove':
            project_name = kwargs.get('project_name')
            data['projects'] = [
                p for p in data['projects']
                if p.get('name') != project_name
            ]

        elif action == 'rename':
            old_name = kwargs.get('old_name')
            new_name = kwargs.get('new_name')
            for project in data['projects']:
                if project.get('name') == old_name:
                    project['name'] = new_name
                    project['displayName'] = new_name.replace('-', ' ').title()
                    project['path'] = f"projects/{new_name}"
                    break

        elif action == 'add':
            project_name = kwargs.get('project_name')
            initial_style = kwargs.get('initial_style', 'github')

            # Check if project already exists in JSON
            existing = any(p.get('name') == project_name for p in data['projects'])
            if not existing:
                new_project = {
                    "name": project_name,
                    "displayName": project_name.replace('-', ' ').title(),
                    "path": f"projects/{project_name}",
                    "htmlPath": "html",
                    "markdownPath": "markdown",
                    "styles": [
                        {
                            "name": initial_style,
                            "displayName": initial_style.title(),
                            "cssPath": f"styles/{initial_style}/style.css",
                            "default": True
                        }
                    ]
                }
                data['projects'].append(new_project)

        # Write back to file
        try:
            with open(projects_json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.debug(f"Updated projects.json: action={action}")
        except Exception as e:
            logger.error(f"Error writing projects.json: {e}")
