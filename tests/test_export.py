"""
Unit tests for export functionality.
"""

from src.core.app import AthleteProfile
from src.core.export import MarkdownResumeGenerator, validate_filename


def test_markdown_generation():
    """Test that markdown is generated correctly."""
    profile = AthleteProfile(sport="Soccer", role="Captain")
    skills = {"Leadership": "Led team..."}

    generator = MarkdownResumeGenerator()
    output = generator.generate(profile, skills)

    assert "# Resume Translation: Soccer Captain" in output
    assert "### Leadership" in output
    assert "- Led team..." in output


def test_validate_filename_valid():
    """Test valid filenames."""
    assert validate_filename("resume.md") is True
    assert validate_filename("my_resume.md") is True
    assert validate_filename("resume-final.txt") is True


def test_validate_filename_invalid():
    """Test invalid filenames (traversal)."""
    assert validate_filename("../resume.md") is False
    assert validate_filename("/etc/passwd") is False
    assert validate_filename("..\\resume.md") is False
    assert validate_filename("resume/../hack") is False
