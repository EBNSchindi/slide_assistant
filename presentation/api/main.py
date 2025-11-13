"""
FastAPI Server for Slides Helper AI Content Generation
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
import sys

# Add parent directory to path for relative imports
sys.path.insert(0, os.path.dirname(__file__))

from config import (
    OPENAI_API_KEY,
    PROJECTS_BASE_PATH,
    HOST,
    PORT,
    DEFAULT_MODEL,
    TEST_MODE,
    ALLOWED_ORIGINS,
)
from models import (
    GenerateContentRequest,
    RegenerateSlideRequest,
    GenerateContentResponse,
    ProjectStyleResponse,
    ProjectStyle,
    AgentStep,
)
from agents import AgentOrchestrator
from services import ProjectService, StyleParser, FileService

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Slides Helper AI API",
    description="AI-powered content generation for presentation slides",
    version="1.0.0",
)

# Add CORS middleware
# Parse ALLOWED_ORIGINS (comma-separated string to list)
origins_list = [origin.strip() for origin in ALLOWED_ORIGINS.split(",") if origin.strip()]

# If "*" is in the list, allow all origins (NOT recommended for production)
if "*" in origins_list:
    origins_list = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins_list,
    allow_credentials=True if "*" not in origins_list else False,  # Don't use credentials with *
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Initialize services
project_service = ProjectService(PROJECTS_BASE_PATH)


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "api_key_configured": bool(OPENAI_API_KEY),
    }


# List projects endpoint
@app.get("/api/projects")
async def list_projects():
    """List all available projects"""
    try:
        projects = project_service.list_projects()
        return {
            "success": True,
            "projects": projects,
            "total": len(projects),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Get project info endpoint
@app.get("/api/projects/{project_name}")
async def get_project_info(project_name: str):
    """Get information about a specific project"""
    try:
        info = project_service.get_project_info(project_name)
        return {
            "success": True,
            "project": info,
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Get project style guide endpoint
@app.get("/api/projects/{project_name}/style")
async def get_project_style(project_name: str):
    """Get style guide for a project"""
    try:
        project_path = project_service.get_project_path(project_name)
        style_parser = StyleParser(project_path)
        style_info = style_parser.parse_project_style()

        project_style = ProjectStyle(
            primary_color=style_info.get("primary_color", "#238636"),
            secondary_colors=style_info.get("secondary_colors", []),
            font_family=style_info.get(
                "font_family",
                "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
            ),
            spacing_scale=style_info.get("spacing_scale", [4, 8, 16, 24, 32, 48]),
            available_components=style_info.get(
                "available_components",
                ["stat-grid", "bullet-list", "quote", "paragraph"],
            ),
            design_guide=style_info.get("design_guide", ""),
        )

        return ProjectStyleResponse(
            project_name=project_name,
            style=project_style,
        )

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Create project endpoint
@app.post("/api/projects")
async def create_project(
    project_name: str = Query(..., min_length=1, max_length=100, pattern=r'^[a-zA-Z0-9_-]+$'),
    initial_style: str = Query(default="github", max_length=50, pattern=r'^[a-zA-Z0-9_-]+$')
):
    """Create a new project"""
    try:
        project_path = project_service.create_project(project_name, initial_style)
        info = project_service.get_project_info(project_name)

        return {
            "success": True,
            "message": f"Project '{project_name}' created",
            "project": info,
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Delete project endpoint
@app.delete("/api/projects/{project_name}")
async def delete_project(project_name: str, force: bool = False):
    """Delete a project"""
    try:
        success = project_service.delete_project(project_name, force)
        return {
            "success": True,
            "message": f"Project '{project_name}' deleted successfully",
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Rename project endpoint
@app.put("/api/projects/{project_name}/rename")
async def rename_project(
    project_name: str,
    new_name: str = Query(..., min_length=1, max_length=100, pattern=r'^[a-zA-Z0-9_-]+$')
):
    """Rename a project"""
    try:
        new_path = project_service.rename_project(project_name, new_name)
        info = project_service.get_project_info(new_name)

        return {
            "success": True,
            "message": f"Project renamed from '{project_name}' to '{new_name}'",
            "project": info,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Get project scope endpoint
@app.get("/api/projects/{project_name}/scope")
async def get_project_scope(project_name: str):
    """Get project scope/context"""
    try:
        scope = project_service.get_project_scope(project_name)
        return {
            "success": True,
            "project_name": project_name,
            "scope": scope,
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Update project scope endpoint
@app.put("/api/projects/{project_name}/scope")
async def update_project_scope(
    project_name: str,
    scope_content: str = Query(..., max_length=100000)  # 100KB limit for scope
):
    """Update project scope/context"""
    try:
        scope_path = project_service.update_project_scope(project_name, scope_content)
        return {
            "success": True,
            "message": "Project scope updated",
            "scope_path": scope_path,
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Main content generation endpoint
@app.post("/api/generate")
async def generate_content(request: GenerateContentRequest):
    """Generate content using AI agents"""

    # Validate API key (skip if test mode)
    if not TEST_MODE and not OPENAI_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="OPENAI_API_KEY not configured. Set it in .env or enable TEST_MODE",
        )

    try:
        # Validate project exists
        project_path = project_service.get_project_path(request.project_name)

        # Initialize orchestrator
        orchestrator = AgentOrchestrator(OPENAI_API_KEY, DEFAULT_MODEL)

        # Process content through agent chain
        result = orchestrator.process(
            user_input=request.user_input,
            project_path=project_path,
            slide_title=request.slide_title,
            preferences=request.preferences,
        )

        if result["success"]:
            return GenerateContentResponse(
                success=True,
                project_name=request.project_name,
                agent_steps=result["agent_steps"],
                generated_slides=result["generated_slides"],
                message=result["message"],
                total_components=result["total_components"],
            )
        else:
            raise HTTPException(
                status_code=400,
                detail=result.get("message", "Content generation failed"),
            )

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Regenerate slide endpoint
@app.post("/api/regenerate")
async def regenerate_slide(request: RegenerateSlideRequest):
    """Regenerate a slide with feedback"""

    if not TEST_MODE and not OPENAI_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="OPENAI_API_KEY not configured. Set it in .env or enable TEST_MODE",
        )

    try:
        project_path = project_service.get_project_path(request.project_name)
        file_service = FileService(project_path)

        # Create backup of existing slide
        file_service.backup_slide(request.slide_name)

        # Get existing markdown
        markdown_content, html_content = file_service.get_slide_content(
            request.slide_name
        )

        # Use feedback to regenerate
        preferences = {"feedback": request.feedback}

        orchestrator = AgentOrchestrator(OPENAI_API_KEY, DEFAULT_MODEL)
        result = orchestrator.process(
            user_input=markdown_content,
            project_path=project_path,
            slide_title=request.slide_name,
            preferences=preferences,
        )

        if result["success"]:
            return GenerateContentResponse(
                success=True,
                project_name=request.project_name,
                agent_steps=result["agent_steps"],
                generated_slides=result["generated_slides"],
                message=result["message"],
                total_components=result["total_components"],
            )
        else:
            raise HTTPException(
                status_code=400,
                detail=result.get("message", "Regeneration failed"),
            )

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/projects/{project_name}/slides")
async def get_project_slides(project_name: str):
    """Get all slides for a project"""
    try:
        project_path = project_service.get_project_path(project_name)
        file_service = FileService(project_path)

        slides = file_service.list_slides()

        return {
            "success": True,
            "project_name": project_name,
            "markdown_slides": slides["markdown"],
            "html_slides": slides["html"],
        }

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Startup event
@app.on_event("startup")
async def startup_event():
    """Run on startup"""
    print("=" * 50)
    print("Slides Helper AI API Starting...")
    print(f"Base Path: {PROJECTS_BASE_PATH}")
    print(f"API Key Configured: {bool(OPENAI_API_KEY)}")
    print(f"Test Mode: {TEST_MODE}")
    print(f"Default Model: {DEFAULT_MODEL}")
    print("=" * 50)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=HOST,
        port=PORT,
    )
