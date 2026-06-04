"""
Unit tests for domain models.
"""
import pytest
from pydantic import ValidationError
from src.core.models import Employer, Job


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


def test_job_creation_defaults():
    """Test creating a Job with only required fields (title)."""
    job = Job(title="Software Engineer")
    assert job.title == "Software Engineer"
    assert job.employer == "General"
    assert job.min_grit == 0
    assert job.min_teamwork == 0
    assert job.required_skills == []
    assert job.base_salary == 0
    assert job.signing_bonus == 0


def test_job_creation_full():
    """Test creating a Job with all fields."""
    job = Job(
        title="Product Manager",
        employer="TechCorp",
        min_grit=8,
        min_teamwork=7,
        required_skills=["Leadership", "Strategic Analysis"],
        base_salary=100000,
        signing_bonus=15000
    )
    assert job.title == "Product Manager"
    assert job.employer == "TechCorp"
    assert job.min_grit == 8
    assert job.min_teamwork == 7
    assert job.required_skills == ["Leadership", "Strategic Analysis"]
    assert job.base_salary == 100000
    assert job.signing_bonus == 15000


def test_job_creation_negative_salary():
    """Test that negative salary or bonus raises a ValidationError."""
    with pytest.raises(ValidationError):
        Job(title="Underpaid Worker", base_salary=-10)

    with pytest.raises(ValidationError):
        Job(title="Owe Money", signing_bonus=-500)
