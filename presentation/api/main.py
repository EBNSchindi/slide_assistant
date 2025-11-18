"""
FastAPI Server for Slides Helper AI Content Generation
"""
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
import sys
import re
from PIL import Image
import io
from datetime import datetime

# Add parent directory to path for relative imports
sys.path.insert(0, os.path.dirname(__file__))

from config import (
    OPENAI_API_KEY,
    PROJECTS_BASE_PATH,
    HOST,
    PORT,
    DEFAULT_MODEL,
    TEST_MODE,
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
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
project_service = ProjectService(PROJECTS_BASE_PATH)


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "Slides Helper AI API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "api_docs": "/docs",
            "projects": "/api/projects",
            "generate": "/api/generate",
            "regenerate": "/api/regenerate",
        },
        "message": "API is running. Visit /docs for interactive API documentation."
    }


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
async def create_project(project_name: str, initial_style: str = "github"):
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
async def rename_project(project_name: str, new_name: str):
    """Rename a project"""
    try:
        if not new_name or not new_name.replace("-", "").replace("_", "").isalnum():
            raise ValueError("Invalid new project name")

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
async def update_project_scope(project_name: str, scope_content: str):
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
            project_name=request.project_name,
            slide_title=request.slide_title,
            preferences=request.preferences,
            image_references=request.image_references,
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


# Image upload endpoints
@app.post("/api/projects/{project_name}/upload-image")
async def upload_image(project_name: str, file: UploadFile = File(...)):
    """Upload an image to a project"""
    try:
        # Validate project exists
        project_path = project_service.get_project_path(project_name)

        # Validate file type
        allowed_types = ["image/png", "image/jpeg", "image/jpg", "image/gif", "image/svg+xml"]
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Allowed: PNG, JPG, GIF, SVG. Got: {file.content_type}"
            )

        # Read file content
        content = await file.read()

        # Validate file size (5MB max)
        max_size = 5 * 1024 * 1024  # 5MB
        if len(content) > max_size:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Max size: 5MB. File size: {len(content) / 1024 / 1024:.2f}MB"
            )

        # Validate image with Pillow (except SVG)
        image_info = {}
        if file.content_type != "image/svg+xml":
            try:
                img = Image.open(io.BytesIO(content))
                image_info = {
                    "width": img.width,
                    "height": img.height,
                    "format": img.format,
                }
                img.close()
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Invalid image file: {str(e)}")

        # Sanitize filename
        original_filename = file.filename
        safe_filename = re.sub(r"[<>:\"/\\|?*]", "", original_filename)
        safe_filename = safe_filename.replace(" ", "-").lower()

        # Add timestamp prefix for uniqueness
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        final_filename = f"{timestamp}_{safe_filename}"

        # Create images/uploads directory if it doesn't exist
        images_dir = os.path.join(project_path, "images", "uploads")
        os.makedirs(images_dir, exist_ok=True)

        # Save file
        file_path = os.path.join(images_dir, final_filename)
        with open(file_path, "wb") as f:
            f.write(content)

        # Return relative path for use in HTML
        relative_path = f"images/uploads/{final_filename}"

        return {
            "success": True,
            "filename": final_filename,
            "original_filename": original_filename,
            "relative_path": relative_path,
            "file_size": len(content),
            "content_type": file.content_type,
            "image_info": image_info,
            "message": "Image uploaded successfully"
        }

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/projects/{project_name}/images")
async def list_project_images(project_name: str):
    """List all images for a project"""
    try:
        project_path = project_service.get_project_path(project_name)
        images_dir = os.path.join(project_path, "images", "uploads")

        if not os.path.exists(images_dir):
            return {
                "success": True,
                "project_name": project_name,
                "images": [],
                "count": 0
            }

        # List all image files
        images = []
        for filename in os.listdir(images_dir):
            file_path = os.path.join(images_dir, filename)
            if os.path.isfile(file_path):
                stat = os.stat(file_path)
                images.append({
                    "filename": filename,
                    "relative_path": f"images/uploads/{filename}",
                    "size": stat.st_size,
                    "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                })

        # Sort by creation time (newest first)
        images.sort(key=lambda x: x["created"], reverse=True)

        return {
            "success": True,
            "project_name": project_name,
            "images": images,
            "count": len(images)
        }

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/projects/{project_name}/images/{filename}")
async def delete_project_image(project_name: str, filename: str):
    """Delete an image from a project"""
    try:
        project_path = project_service.get_project_path(project_name)

        # Sanitize filename to prevent path traversal
        safe_filename = os.path.basename(filename)
        file_path = os.path.join(project_path, "images", "uploads", safe_filename)

        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail=f"Image not found: {filename}")

        # Delete file
        os.remove(file_path)

        return {
            "success": True,
            "message": f"Image '{filename}' deleted successfully"
        }

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except HTTPException:
        raise
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
