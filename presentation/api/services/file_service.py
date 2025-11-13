import os
import re
from pathlib import Path
from typing import Dict, Tuple
from datetime import datetime


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

    def save_markdown_slide(self, slide_name: str, content: str) -> str:
        """Save markdown slide to optimized folder"""
        # Sanitize slide name
        slide_name = self._sanitize_filename(slide_name)

        filepath = os.path.join(self.markdown_optimized_path, f"{slide_name}.md")

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            return filepath
        except Exception as e:
            raise Exception(f"Error saving markdown: {e}")

    def save_html_slide(self, slide_name: str, content: str) -> str:
        """Save HTML slide to html folder"""
        # Sanitize slide name
        slide_name = self._sanitize_filename(slide_name)

        filepath = os.path.join(self.html_path, f"{slide_name}.html")

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            return filepath
        except Exception as e:
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
                print(f"Error saving slide {slide.get('name')}: {e}")

        return results

    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename to be filesystem safe"""
        # Remove invalid characters
        filename = re.sub(r"[<>:\"/\\|?*]", "", filename)
        # Replace spaces with hyphens
        filename = filename.replace(" ", "-")
        # Convert to lowercase
        filename = filename.lower()
        # Remove leading/trailing hyphens
        filename = filename.strip("-")

        return filename

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
            print(f"Error reading markdown: {e}")

        try:
            if os.path.exists(html_path):
                with open(html_path, "r", encoding="utf-8") as f:
                    html_content = f.read()
        except Exception as e:
            print(f"Error reading HTML: {e}")

        return markdown_content, html_content

    def backup_slide(self, slide_name: str) -> None:
        """Create a backup of existing slide files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = os.path.join(self.project_path, "backups", timestamp)
        os.makedirs(backup_dir, exist_ok=True)

        # Backup markdown
        md_path = os.path.join(self.markdown_optimized_path, f"{slide_name}.md")
        if os.path.exists(md_path):
            backup_md = os.path.join(backup_dir, f"{slide_name}.md")
            with open(md_path, "r", encoding="utf-8") as src:
                with open(backup_md, "w", encoding="utf-8") as dst:
                    dst.write(src.read())

        # Backup HTML
        html_path = os.path.join(self.html_path, f"{slide_name}.html")
        if os.path.exists(html_path):
            backup_html = os.path.join(backup_dir, f"{slide_name}.html")
            with open(html_path, "r", encoding="utf-8") as src:
                with open(backup_html, "w", encoding="utf-8") as dst:
                    dst.write(src.read())
