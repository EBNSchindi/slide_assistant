"""Text processing utilities"""
import re
from typing import Optional


def sanitize_filename(filename: str, max_length: Optional[int] = 255) -> str:
    """Sanitize filename to be filesystem safe

    Args:
        filename: The filename to sanitize
        max_length: Maximum length of the filename (default: 255)

    Returns:
        Sanitized filename safe for filesystem use

    Examples:
        >>> sanitize_filename("My File!@#.txt")
        'my-file.txt'
        >>> sanitize_filename("  spaces  ")
        'spaces'
    """
    # Remove invalid filesystem characters and special characters
    # Keep only alphanumeric, dots, hyphens, underscores, and spaces
    filename = re.sub(r'[<>:"/\\|?*!@#$%^&()+=\[\]{};\',]', '', filename)
    # Replace spaces with hyphens
    filename = filename.replace(' ', '-')
    # Convert to lowercase
    filename = filename.lower()
    # Remove consecutive hyphens
    filename = re.sub(r'-+', '-', filename)
    # Remove leading/trailing hyphens and dots
    filename = filename.strip('-.')
    # Limit length if specified
    if max_length and len(filename) > max_length:
        filename = filename[:max_length].rstrip('-.')

    return filename


def sanitize_slide_name(name: str) -> str:
    """Sanitize slide name for use in filenames

    This is an alias for sanitize_filename with default settings
    optimized for slide names.

    Args:
        name: The slide name to sanitize

    Returns:
        Sanitized slide name

    Examples:
        >>> sanitize_slide_name("Slide 1: Introduction")
        'slide-1-introduction'
    """
    return sanitize_filename(name, max_length=100)
