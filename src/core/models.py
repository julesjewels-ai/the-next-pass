"""
Domain models for The 98% Platform.
"""
from pydantic import BaseModel, Field


class AthleteProfile(BaseModel):
    """Represents a student-athlete's basic background."""
    sport: str = Field(..., description="The sport played by the athlete")
    role: str = Field(..., description="The role or position within the team")
    gpa: float = Field(0.0, ge=0.0, le=4.0, description="Grade Point Average (0.0 - 4.0)")


class Skill(BaseModel):
    """Represents a translated skill."""
    name: str = Field(..., description="The corporate skill name")
    description: str = Field(..., description="The resume-ready description")


class Job(BaseModel):
    """Represents a job opportunity."""
    title: str = Field(..., description="The job title")
