from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, Any


class GenerateContentRequest(BaseModel):
    """Request model for content generation"""

    project_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        pattern=r'^[a-zA-Z0-9_-]+$',
        description="Project name (alphanumeric, hyphens, underscores only)"
    )
    user_input: str = Field(
        ...,
        min_length=1,
        max_length=50000,
        description="User input for content generation (max 50KB)"
    )
    slide_title: Optional[str] = Field(
        None,
        max_length=200,
        description="Optional slide title"
    )
    preferences: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional preferences for content generation"
    )
    regenerate_feedback: Optional[str] = Field(
        None,
        max_length=10000,
        description="Optional feedback for regeneration"
    )

    @field_validator('preferences')
    @classmethod
    def validate_preferences_size(cls, v: Optional[Dict]) -> Optional[Dict]:
        """Validate preferences dict size to prevent DoS"""
        if v is not None:
            # Convert to string to check size
            import json
            try:
                serialized = json.dumps(v)
                if len(serialized) > 10000:  # 10KB limit
                    raise ValueError('Preferences object too large (max 10KB)')
            except (TypeError, ValueError) as e:
                if 'too large' in str(e):
                    raise
                raise ValueError(f'Invalid preferences format: {e}')
        return v


class RegenerateSlideRequest(BaseModel):
    """Request model for slide regeneration"""

    project_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        pattern=r'^[a-zA-Z0-9_-]+$',
        description="Project name (alphanumeric, hyphens, underscores only)"
    )
    slide_name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Name of the slide to regenerate"
    )
    feedback: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="Feedback for regeneration (max 10KB)"
    )


class ProjectStyleRequest(BaseModel):
    """Request model for getting project style guide"""

    project_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        pattern=r'^[a-zA-Z0-9_-]+$',
        description="Project name (alphanumeric, hyphens, underscores only)"
    )
