"""
Export functionality for The 98% Platform.

Handles the generation of resume artifacts.
"""

from typing import Dict, Protocol
import re
from src.core.app import AthleteProfile


class ResumeGenerator(Protocol):
    """Protocol for resume generation strategies."""

    def generate(self, profile: AthleteProfile, skills: Dict[str, str]) -> str:
        """Generates the resume content."""
        ...


class MarkdownResumeGenerator:
    """Generates a resume in Markdown format."""

    def generate(self, profile: AthleteProfile, skills: Dict[str, str]) -> str:
        """
        Generates the resume content in Markdown.

        Args:
            profile: The athlete's profile.
            skills: The dictionary of translated skills.

        Returns:
            A string containing the Markdown content.
        """
        lines = [
            f"# Resume Translation: {profile.sport} {profile.role}",
            "",
            "## Professional Summary",
            f"Former {profile.sport} {profile.role} with a proven track record of...",
            "",
            "## Skills & Experience",
            ""
        ]

        for skill_name, description in skills.items():
            lines.append(f"### {skill_name}")
            lines.append(f"- {description}")
            lines.append("")

        return "\n".join(lines)


def validate_filename(filename: str) -> bool:
    """
    Validates the output filename to prevent directory traversal.

    Args:
        filename: The desired output filename.

    Returns:
        True if valid, False otherwise.
    """
    # Prevent directory traversal
    if ".." in filename or filename.startswith("/") or filename.startswith("\\"):
        return False

    # Allow alphanumeric, underscore, dash, and dots
    if not re.match(r"^[\w\-. ]+$", filename):
        return False

    return True
