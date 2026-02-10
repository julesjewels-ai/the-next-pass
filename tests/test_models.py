"""
Unit tests for domain models.
"""
import pytest
from pydantic import ValidationError
from src.core.models import Employer, AthleteProfile


def test_athlete_profile_defaults():
    """Test that AthleteProfile has sensible defaults."""
    profile = AthleteProfile(sport="Swimming", role="Athlete")
    assert profile.grit == 5
    assert profile.teamwork == 5
    assert profile.gpa == 3.0


def test_athlete_profile_custom_values():
    """Test that AthleteProfile accepts custom values."""
    profile = AthleteProfile(
        sport="Swimming",
        role="Athlete",
        grit=8,
        teamwork=9,
        gpa=3.8
    )
    assert profile.grit == 8
    assert profile.teamwork == 9
    assert profile.gpa == 3.8


def test_athlete_profile_validation_grit():
    """Test that grit must be between 1 and 10."""
    with pytest.raises(ValidationError):
        AthleteProfile(sport="S", role="R", grit=11)
    with pytest.raises(ValidationError):
        AthleteProfile(sport="S", role="R", grit=0)


def test_athlete_profile_validation_teamwork():
    """Test that teamwork must be between 1 and 10."""
    with pytest.raises(ValidationError):
        AthleteProfile(sport="S", role="R", teamwork=11)
    with pytest.raises(ValidationError):
        AthleteProfile(sport="S", role="R", teamwork=0)


def test_athlete_profile_validation_gpa():
    """Test that GPA must be between 0.0 and 4.0."""
    with pytest.raises(ValidationError):
        AthleteProfile(sport="S", role="R", gpa=4.1)
    with pytest.raises(ValidationError):
        AthleteProfile(sport="S", role="R", gpa=-0.1)


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
