#!/usr/bin/env python3
"""
Project Manager API
Provides REST API endpoints for managing presentation projects
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import shutil
from pathlib import Path
import re

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
PROJECTS_JSON = 'projects.json'
PROJECTS_DIR = 'projects'

# Default styles that each new project gets
DEFAULT_STYLES = [
    {
        "name": "github",
        "displayName": "GitHub Design",
        "cssPath": "styles/github/style.css",
        "default": True
    },
    {
        "name": "modern",
        "displayName": "Modern",
        "cssPath": "styles/modern/style.css",
        "default": False
    },
    {
        "name": "minimal",
        "displayName": "Minimal",
        "cssPath": "styles/minimal/style.css",
        "default": False
    }
]

# Default CSS content for new styles
DEFAULT_STYLE_CSS = """/* Project-specific styles */
.presentation-slide {
    background: white;
    color: #24292e;
}
"""


def sanitize_project_name(name):
    """Convert display name to filesystem-safe project name"""
    # Convert to lowercase and replace spaces with hyphens
    name = name.lower().strip()
    # Remove special characters, keep only alphanumeric, hyphens, and underscores
    name = re.sub(r'[^a-z0-9\-_]', '-', name)
    # Remove multiple consecutive hyphens
    name = re.sub(r'-+', '-', name)
    # Remove leading/trailing hyphens
    name = name.strip('-')
    return name


def load_projects_config():
    """Load projects.json configuration"""
    try:
        with open(PROJECTS_JSON, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"defaultStyle": "github", "projects": []}


def save_projects_config(config):
    """Save projects.json configuration"""
    with open(PROJECTS_JSON, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def create_project_structure(project_path, project_name):
    """Create the directory structure for a new project"""
    base_path = Path(project_path)

    # Create main directories
    (base_path / 'html').mkdir(parents=True, exist_ok=True)
    (base_path / 'markdown' / 'input').mkdir(parents=True, exist_ok=True)
    (base_path / 'markdown' / 'optimized').mkdir(parents=True, exist_ok=True)

    # Create style directories with default CSS
    for style in DEFAULT_STYLES:
        style_path = base_path / 'styles' / style['name']
        style_path.mkdir(parents=True, exist_ok=True)

        # Create default style.css
        css_file = style_path / 'style.css'
        if not css_file.exists():
            css_file.write_text(DEFAULT_STYLE_CSS, encoding='utf-8')

    # Create a README in markdown/input
    readme_path = base_path / 'markdown' / 'input' / 'README.md'
    readme_path.write_text(
        f"# {project_name}\n\n"
        "Place your markdown source files here.\n\n"
        "## Structure\n"
        "- Use H1 (`#`) for slide boundaries\n"
        "- Use H2 (`##`) for component boundaries\n",
        encoding='utf-8'
    )


@app.route('/api/projects', methods=['GET'])
def get_projects():
    """Get all projects"""
    config = load_projects_config()
    return jsonify(config)


@app.route('/api/projects', methods=['POST'])
def create_project():
    """Create a new project"""
    data = request.json
    display_name = data.get('displayName', '').strip()

    if not display_name:
        return jsonify({"error": "Project name is required"}), 400

    # Generate project name from display name
    project_name = sanitize_project_name(display_name)

    if not project_name:
        return jsonify({"error": "Invalid project name"}), 400

    # Load current config
    config = load_projects_config()

    # Check if project already exists
    for project in config['projects']:
        if project['name'] == project_name:
            return jsonify({"error": f"Project '{project_name}' already exists"}), 409

    # Create project directory structure
    project_path = f"{PROJECTS_DIR}/{project_name}"

    if os.path.exists(project_path):
        return jsonify({"error": f"Project directory '{project_path}' already exists"}), 409

    try:
        create_project_structure(project_path, display_name)

        # Add project to config
        new_project = {
            "name": project_name,
            "displayName": display_name,
            "path": project_path,
            "htmlPath": "html",
            "markdownPath": "markdown",
            "styles": DEFAULT_STYLES.copy()
        }

        config['projects'].append(new_project)
        save_projects_config(config)

        return jsonify({
            "message": "Project created successfully",
            "project": new_project
        }), 201

    except Exception as e:
        # Clean up on error
        if os.path.exists(project_path):
            shutil.rmtree(project_path)
        return jsonify({"error": f"Failed to create project: {str(e)}"}), 500


@app.route('/api/projects/<project_name>', methods=['PUT'])
def rename_project(project_name):
    """Rename an existing project"""
    data = request.json
    new_display_name = data.get('displayName', '').strip()

    if not new_display_name:
        return jsonify({"error": "New project name is required"}), 400

    # Generate new project name from display name
    new_project_name = sanitize_project_name(new_display_name)

    if not new_project_name:
        return jsonify({"error": "Invalid project name"}), 400

    # Load current config
    config = load_projects_config()

    # Find the project to rename
    project_index = None
    old_project = None

    for i, project in enumerate(config['projects']):
        if project['name'] == project_name:
            project_index = i
            old_project = project
            break

    if project_index is None:
        return jsonify({"error": f"Project '{project_name}' not found"}), 404

    # Check if new name conflicts with existing project
    if new_project_name != project_name:
        for project in config['projects']:
            if project['name'] == new_project_name:
                return jsonify({"error": f"Project '{new_project_name}' already exists"}), 409

    try:
        old_path = old_project['path']
        new_path = f"{PROJECTS_DIR}/{new_project_name}"

        # Rename directory if name changed
        if new_project_name != project_name and os.path.exists(old_path):
            os.rename(old_path, new_path)

        # Update config
        config['projects'][project_index] = {
            "name": new_project_name,
            "displayName": new_display_name,
            "path": new_path,
            "htmlPath": old_project['htmlPath'],
            "markdownPath": old_project['markdownPath'],
            "styles": old_project['styles']
        }

        save_projects_config(config)

        return jsonify({
            "message": "Project renamed successfully",
            "project": config['projects'][project_index]
        }), 200

    except Exception as e:
        return jsonify({"error": f"Failed to rename project: {str(e)}"}), 500


@app.route('/api/projects/<project_name>', methods=['DELETE'])
def delete_project(project_name):
    """Delete a project"""
    # Load current config
    config = load_projects_config()

    # Find the project to delete
    project_index = None
    project_to_delete = None

    for i, project in enumerate(config['projects']):
        if project['name'] == project_name:
            project_index = i
            project_to_delete = project
            break

    if project_index is None:
        return jsonify({"error": f"Project '{project_name}' not found"}), 404

    try:
        # Delete project directory
        project_path = project_to_delete['path']
        if os.path.exists(project_path):
            shutil.rmtree(project_path)

        # Remove from config
        config['projects'].pop(project_index)
        save_projects_config(config)

        return jsonify({
            "message": "Project deleted successfully",
            "projectName": project_name
        }), 200

    except Exception as e:
        return jsonify({"error": f"Failed to delete project: {str(e)}"}), 500


if __name__ == '__main__':
    # Change to presentation directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    print("Project Manager API starting...")
    print(f"Working directory: {os.getcwd()}")
    print(f"Projects config: {PROJECTS_JSON}")
    print(f"Projects directory: {PROJECTS_DIR}")
    print("\nAPI Endpoints:")
    print("  GET    /api/projects         - List all projects")
    print("  POST   /api/projects         - Create new project")
    print("  PUT    /api/projects/<name>  - Rename project")
    print("  DELETE /api/projects/<name>  - Delete project")
    print("\nStarting server on http://localhost:5000")

    app.run(debug=True, port=5000, host='0.0.0.0')
