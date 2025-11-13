from pydantic import BaseModel
from typing import Optional, List, Dict


class AgentStep(BaseModel):
    """Single step in agent processing"""
    agent_name: str
    status: str  # "processing", "completed", "error"
    output: Optional[str] = None
    error: Optional[str] = None


class GeneratedSlide(BaseModel):
    """Generated slide with markdown and HTML"""
    slide_name: str
    slide_title: str
    markdown_path: str
    html_path: str
    components: List[str] = []
    html_content: Optional[str] = None
    markdown_content: Optional[str] = None


class GenerateContentResponse(BaseModel):
    """Response from content generation"""
    success: bool
    project_name: str
    agent_steps: List[AgentStep]
    generated_slides: List[GeneratedSlide]
    message: str
    total_components: int = 0


class ProjectStyle(BaseModel):
    """Project style guide information"""
    primary_color: str
    secondary_colors: List[str] = []
    font_family: str
    spacing_scale: List[int] = []
    available_components: List[str] = []
    design_guide: Optional[str] = None


class ProjectStyleResponse(BaseModel):
    """Response with project style info"""
    project_name: str
    style: ProjectStyle
