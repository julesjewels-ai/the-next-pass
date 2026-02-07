"""
Unit tests for domain models.
"""
import pytest
from pydantic import ValidationError
from src.core.models import Employer


def test_employer_creation_valid():
    """Test creating a valid Employer instance."""
    employer = Employer(
        name="TechCorp",
        industry="Technology",
        required_skills=["Leadership", "Communication"]
    )
    assert employer.name == "TechCorp"
    assert employer.industry == "Technology"
    assert employer.required_skills == ["Leadership", "Communication"]


def test_employer_creation_missing_field():
    """Test that missing required fields raises ValidationError."""
    with pytest.raises(ValidationError):
        Employer(
            name="IncompleteCorp",
            # Missing industry
            required_skills=["Leadership"]
        )


def test_employer_creation_invalid_type():
    """Test that invalid types raise ValidationError."""
    with pytest.raises(ValidationError):
        Employer(
            name="BadTypeCorp",
            industry="Technology",
            required_skills="Not a list"  # Should be a list
        )
