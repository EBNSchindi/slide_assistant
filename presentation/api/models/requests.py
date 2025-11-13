from pydantic import BaseModel
from typing import Optional


class GenerateContentRequest(BaseModel):
    """Request model for content generation"""
    project_name: str
    user_input: str
    slide_title: Optional[str] = None
    preferences: Optional[dict] = None
    regenerate_feedback: Optional[str] = None


class RegenerateSlideRequest(BaseModel):
    """Request model for slide regeneration"""
    project_name: str
    slide_name: str
    feedback: str


class ProjectStyleRequest(BaseModel):
    """Request model for getting project style guide"""
    project_name: str
