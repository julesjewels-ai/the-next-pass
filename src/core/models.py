"""
Domain models for The 98% Platform.
"""
from typing import List
from pydantic import BaseModel, Field


class AthleteProfile(BaseModel):
    """Represents a student-athlete's basic background."""
    sport: str = Field(..., min_length=1, description="The sport played by the athlete")
    role: str = Field(..., min_length=1, description="The role or position within the team")


class Skill(BaseModel):
    """Represents a translated skill."""
    name: str = Field(..., description="The corporate skill name")
    description: str = Field(..., description="The resume-ready description")


class Job(BaseModel):
    """Represents a job opportunity."""
    title: str = Field(..., description="The job title")
    employer: str = Field("General", description="The hiring company")
    min_grit: int = Field(0, description="Minimum grit score required")
    min_teamwork: int = Field(0, description="Minimum teamwork score required")
    required_skills: List[str] = Field(default_factory=list, description="Skills required for the job")


class Employer(BaseModel):
    """Represents a hiring partner."""
    name: str = Field(..., description="The company name")
    industry: str = Field(..., description="The industry sector")
    required_skills: List[str] = Field(..., description="List of required skills")
