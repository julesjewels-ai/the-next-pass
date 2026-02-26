"""
Tests for verifying employer constraints in job matching.
"""
import pytest
from src.core.models import AthleteProfile
from src.core.services import match_opportunities
from src.core.data import HIGH_SCORE_THRESHOLD

@pytest.fixture
def high_scores():
    return HIGH_SCORE_THRESHOLD + 1

def test_job_match_fails_if_employer_skills_missing(high_scores):
    """
    Test that a job match is rejected if the athlete lacks the employer's
    baseline required skills, even if they have the job-specific skills.

    Scenario:
    - Employer: TechCorp (Requires: Leadership, Strategic Analysis)
    - Job: Sales Development Representative (Requires: Strategic Analysis)
    - Athlete: Swimmer / Player (Has: Strategic Analysis [Universal], but NO Leadership)

    Expected Result:
    - The athlete matches the Job requirements.
    - The athlete fails the Employer requirements.
    - The job should NOT be returned.
    """
    profile = AthleteProfile(sport="Swimming", role="Player")
    # Swimmers get Universal skills:
    # - Time Management (via 5am Workouts)
    # - Strategic Analysis (via Film Study)
    # They do NOT get Leadership (which comes from Captain role).

    matches = match_opportunities(profile, grit_score=high_scores, teamwork_score=high_scores)
    titles = [job.title for job in matches]

    # Before fix: This assertion will FAIL because the job IS currently returned.
    # After fix: This assertion will PASS.
    assert "Sales Development Representative" not in titles, \
        "Should not match if employer baseline skills (Leadership) are missing"

def test_job_match_succeeds_if_employer_skills_met(high_scores):
    """
    Test that a job match works when both job and employer skills are met.

    Scenario:
    - Employer: StartUp (Requires: Time Management)
    - Job: Junior Associate (Requires: [])
    - Athlete: Swimmer / Player (Has: Time Management, Strategic Analysis)

    Expected Result:
    - Athlete has Time Management.
    - Match should succeed.
    """
    profile = AthleteProfile(sport="Swimming", role="Player")

    matches = match_opportunities(profile, grit_score=high_scores, teamwork_score=high_scores)
    titles = [job.title for job in matches]

    assert "Junior Associate" in titles
