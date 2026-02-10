"""
Domain models for The 98% Platform.
"""
from typing import List
from pydantic import BaseModel, Field


class AthleteProfile(BaseModel):
    """Represents a student-athlete's basic background."""
    sport: str = Field(..., description="The sport played by the athlete")
    role: str = Field(..., description="The role or position within the team")
    grit: int = Field(default=5, ge=1, le=10, description="Grit score (1-10)")
    teamwork: int = Field(default=5, ge=1, le=10, description="Teamwork score (1-10)")
    gpa: float = Field(default=3.0, ge=0.0, le=4.0, description="Grade Point Average (0.0-4.0)")


class Skill(BaseModel):
    """Represents a translated skill."""
    name: str = Field(..., description="The corporate skill name")
    description: str = Field(..., description="The resume-ready description")


class Job(BaseModel):
    """Represents a job opportunity."""
    title: str = Field(..., description="The job title")


class Employer(BaseModel):
    """Represents a hiring partner."""
    name: str = Field(..., description="The company name")
    industry: str = Field(..., description="The industry sector")
    required_skills: List[str] = Field(..., description="List of required skills")
