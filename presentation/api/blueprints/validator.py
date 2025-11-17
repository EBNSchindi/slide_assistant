"""
Blueprint validation logic.

Validates blueprints before rendering to ensure:
- Schema version compatibility
- Component positions match layout type
- Image paths exist (optional)
- All required fields are present
"""

from typing import Dict, Any, Optional
from pathlib import Path
from pydantic import ValidationError
import logging

from .models import (
    SlideBlueprint,
    CompleteBlueprint,
    LayoutType,
    ComponentType,
    ComponentPosition,
    validate_layout_positions,
)

logger = logging.getLogger(__name__)


class BlueprintValidationError(Exception):
    """Raised when blueprint validation fails"""
    pass


class BlueprintValidator:
    """Validates blueprints before rendering"""

    SUPPORTED_SCHEMA_VERSIONS = ["1.0", "1.1"]

    def __init__(self, validate_image_paths: bool = True):
        """
        Initialize validator.

        Args:
            validate_image_paths: Whether to check if image paths exist (default: True)
        """
        self.validate_image_paths = validate_image_paths

    def validate(self, blueprint_dict: Dict[str, Any]) -> SlideBlueprint:
        """
        Validate blueprint structure.

        Args:
            blueprint_dict: Blueprint as dictionary

        Returns:
            Validated SlideBlueprint instance

        Raises:
            BlueprintValidationError: If blueprint is invalid
        """
        # Try to parse as SlideBlueprint
        try:
            blueprint = SlideBlueprint(**blueprint_dict)
        except ValidationError as e:
            raise BlueprintValidationError(f"Invalid blueprint schema: {e}")

        # Additional validation
        self._validate_schema_version(blueprint)
        self._validate_component_positions(blueprint)

        if self.validate_image_paths:
            self._validate_image_paths(blueprint)

        return blueprint

    def validate_complete(self, blueprint_dict: Dict[str, Any]) -> CompleteBlueprint:
        """
        Validate complete blueprint (from Agent 3).

        Args:
            blueprint_dict: Complete blueprint as dictionary

        Returns:
            Validated CompleteBlueprint instance

        Raises:
            BlueprintValidationError: If blueprint is invalid or incomplete
        """
        # Try to parse as CompleteBlueprint
        try:
            blueprint = CompleteBlueprint(**blueprint_dict)
        except ValidationError as e:
            raise BlueprintValidationError(f"Invalid complete blueprint: {e}")

        # Additional validation
        self._validate_schema_version(blueprint)
        self._validate_component_positions(blueprint)
        self._validate_completeness(blueprint)

        if self.validate_image_paths:
            self._validate_image_paths(blueprint)

        return blueprint

    def _validate_schema_version(self, blueprint: SlideBlueprint):
        """Check schema version compatibility"""
        if blueprint.schema_version not in self.SUPPORTED_SCHEMA_VERSIONS:
            raise BlueprintValidationError(
                f"Unsupported schema version: {blueprint.schema_version}. "
                f"Supported versions: {self.SUPPORTED_SCHEMA_VERSIONS}"
            )

    def _validate_component_positions(self, blueprint: SlideBlueprint):
        """Ensure positions are compatible with layout"""
        try:
            validate_layout_positions(blueprint.layout_type, blueprint.components)
        except ValueError as e:
            raise BlueprintValidationError(str(e))

    def _validate_image_paths(self, blueprint: SlideBlueprint):
        """Check that image paths exist (optional, can be disabled)"""
        for component in blueprint.components:
            if component.type == ComponentType.IMAGE_FRAME:
                self._check_image_component(component)

    def _check_image_component(self, component):
        """Check image paths in image frame component"""
        content = component.content

        # Handle different content types
        if isinstance(content, dict):
            # Single image variant
            if "image_path" in content and content["image_path"]:
                image_path = Path(content["image_path"])
                if not image_path.exists():
                    logger.warning(f"Image not found: {image_path}")

            # Gallery variant
            if "images" in content and content["images"]:
                for img in content["images"]:
                    if isinstance(img, dict) and "image_path" in img:
                        image_path = Path(img["image_path"])
                        if not image_path.exists():
                            logger.warning(f"Image not found: {image_path}")

    def _validate_completeness(self, blueprint: CompleteBlueprint):
        """Validate that complete blueprint has all required fields filled"""
        # Check slide title
        if not blueprint.slide_title or blueprint.slide_title.strip() == "":
            raise BlueprintValidationError("Complete blueprint must have a slide_title")

        # Check all components have content
        for i, component in enumerate(blueprint.components):
            if not component.content:
                raise BlueprintValidationError(
                    f"Component {i} ({component.component_id}) is missing content"
                )

            # Type-specific validation
            self._validate_component_content(component, i)

        # Check metadata
        if not blueprint.metadata:
            raise BlueprintValidationError("Complete blueprint must have metadata")

    def _validate_component_content(self, component, index: int):
        """Validate component-specific content requirements"""
        content = component.content

        if component.type == ComponentType.STAT_GRID:
            if isinstance(content, dict):
                if "items" not in content or not content["items"]:
                    raise BlueprintValidationError(
                        f"Stat grid component {index} missing items"
                    )
                if len(content["items"]) < 2 or len(content["items"]) > 4:
                    raise BlueprintValidationError(
                        f"Stat grid component {index} must have 2-4 items, got {len(content['items'])}"
                    )

        elif component.type == ComponentType.BULLET_LIST:
            if isinstance(content, dict):
                if "items" not in content or not content["items"]:
                    raise BlueprintValidationError(
                        f"Bullet list component {index} missing items"
                    )
                if len(content["items"]) < 2 or len(content["items"]) > 6:
                    raise BlueprintValidationError(
                        f"Bullet list component {index} must have 2-6 items, got {len(content['items'])}"
                    )

        elif component.type == ComponentType.IMAGE_FRAME:
            if isinstance(content, dict):
                frame_variant = content.get("frame_variant", "single")

                if frame_variant == "single":
                    if not content.get("image_path"):
                        raise BlueprintValidationError(
                            f"Image frame component {index} (single) missing image_path"
                        )
                    if not content.get("alt_text"):
                        raise BlueprintValidationError(
                            f"Image frame component {index} (single) missing alt_text (required for accessibility)"
                        )

                elif frame_variant in ["gallery_2", "gallery_3"]:
                    if not content.get("images"):
                        raise BlueprintValidationError(
                            f"Image frame component {index} ({frame_variant}) missing images list"
                        )

                    expected_count = 2 if frame_variant == "gallery_2" else 3
                    actual_count = len(content["images"])
                    if actual_count != expected_count:
                        raise BlueprintValidationError(
                            f"Image frame component {index} ({frame_variant}) "
                            f"requires {expected_count} images, got {actual_count}"
                        )

        elif component.type == ComponentType.QUOTE:
            if isinstance(content, dict):
                if not content.get("quote_text"):
                    raise BlueprintValidationError(
                        f"Quote component {index} missing quote_text"
                    )

        elif component.type == ComponentType.TEXT_BLOCK:
            if isinstance(content, dict):
                if not content.get("paragraphs"):
                    raise BlueprintValidationError(
                        f"Text block component {index} missing paragraphs"
                    )


def quick_validate(blueprint_dict: Dict[str, Any]) -> bool:
    """
    Quick validation without exceptions.

    Args:
        blueprint_dict: Blueprint as dictionary

    Returns:
        True if valid, False otherwise
    """
    validator = BlueprintValidator(validate_image_paths=False)
    try:
        validator.validate(blueprint_dict)
        return True
    except BlueprintValidationError:
        return False
