import os
from pathlib import Path
from typing import Dict, Tuple
from datetime import datetime
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import sanitize_filename, get_logger

logger = get_logger(__name__)


class FileService:
    """Handle file operations for markdown and HTML generation"""

    def __init__(self, project_path: str):
        self.project_path = project_path
        self.markdown_optimized_path = os.path.join(
            project_path, "markdown", "optimized"
        )
        self.html_path = os.path.join(project_path, "html")

        # Create directories if they don't exist
        os.makedirs(self.markdown_optimized_path, exist_ok=True)
        os.makedirs(self.html_path, exist_ok=True)

        logger.debug(f"FileService initialized for project: {project_path}")

    def save_markdown_slide(self, slide_name: str, content: str) -> str:
        """Save markdown slide to optimized folder"""
        # Sanitize slide name
        slide_name = sanitize_filename(slide_name)

        filepath = os.path.join(self.markdown_optimized_path, f"{slide_name}.md")

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            logger.info(f"Saved markdown slide: {slide_name}.md")
            return filepath
        except Exception as e:
            logger.error(f"Error saving markdown slide {slide_name}: {e}")
            raise Exception(f"Error saving markdown: {e}")

    def save_html_slide(self, slide_name: str, content: str) -> str:
        """Save HTML slide to html folder"""
        # Sanitize slide name
        slide_name = sanitize_filename(slide_name)

        filepath = os.path.join(self.html_path, f"{slide_name}.html")

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            logger.info(f"Saved HTML slide: {slide_name}.html")
            return filepath
        except Exception as e:
            logger.error(f"Error saving HTML slide {slide_name}: {e}")
            raise Exception(f"Error saving HTML: {e}")

    def save_slides(self, slides: list) -> Dict[str, list]:
        """Save multiple slides at once"""
        results = {"markdown": [], "html": []}

        for slide in slides:
            try:
                md_path = self.save_markdown_slide(slide["name"], slide["markdown"])
                html_path = self.save_html_slide(slide["name"], slide["html"])

                results["markdown"].append(md_path)
                results["html"].append(html_path)
            except Exception as e:
                logger.error(f"Error saving slide {slide.get('name')}: {e}")

        logger.info(f"Batch saved {len(results['markdown'])} slides")
        return results


    def list_slides(self) -> Dict[str, list]:
        """List all existing slides in markdown and html folders"""
        markdown_slides = []
        html_slides = []

        # List markdown files
        if os.path.exists(self.markdown_optimized_path):
            markdown_slides = [
                f.replace(".md", "")
                for f in os.listdir(self.markdown_optimized_path)
                if f.endswith(".md")
            ]

        # List HTML files
        if os.path.exists(self.html_path):
            html_slides = [
                f.replace(".html", "")
                for f in os.listdir(self.html_path)
                if f.endswith(".html")
            ]

        return {"markdown": sorted(markdown_slides), "html": sorted(html_slides)}

    def get_slide_content(self, slide_name: str) -> Tuple[str, str]:
        """Get both markdown and HTML content for a slide"""
        md_path = os.path.join(self.markdown_optimized_path, f"{slide_name}.md")
        html_path = os.path.join(self.html_path, f"{slide_name}.html")

        markdown_content = ""
        html_content = ""

        try:
            if os.path.exists(md_path):
                with open(md_path, "r", encoding="utf-8") as f:
                    markdown_content = f.read()
        except Exception as e:
            logger.error(f"Error reading markdown for {slide_name}: {e}")

        try:
            if os.path.exists(html_path):
                with open(html_path, "r", encoding="utf-8") as f:
                    html_content = f.read()
        except Exception as e:
            logger.error(f"Error reading HTML for {slide_name}: {e}")

        return markdown_content, html_content

    def backup_slide(self, slide_name: str) -> None:
        """Create a backup of existing slide files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = os.path.join(self.project_path, "backups", timestamp)
        os.makedirs(backup_dir, exist_ok=True)

        backed_up_files = []

        # Backup markdown
        md_path = os.path.join(self.markdown_optimized_path, f"{slide_name}.md")
        if os.path.exists(md_path):
            backup_md = os.path.join(backup_dir, f"{slide_name}.md")
            with open(md_path, "r", encoding="utf-8") as src:
                with open(backup_md, "w", encoding="utf-8") as dst:
                    dst.write(src.read())
            backed_up_files.append("markdown")

        # Backup HTML
        html_path = os.path.join(self.html_path, f"{slide_name}.html")
        if os.path.exists(html_path):
            backup_html = os.path.join(backup_dir, f"{slide_name}.html")
            with open(html_path, "r", encoding="utf-8") as src:
                with open(backup_html, "w", encoding="utf-8") as dst:
                    dst.write(src.read())
            backed_up_files.append("html")

        if backed_up_files:
            logger.info(f"Backed up {slide_name} ({', '.join(backed_up_files)}) to {backup_dir}")
