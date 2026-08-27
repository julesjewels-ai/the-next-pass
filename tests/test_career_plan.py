"""
Unit tests for the Career Plan feature.
"""
import pytest
import argparse
from src.core.models import AthleteProfile
from src.core.services import generate_career_plan
from main import handle_plan

@pytest.fixture
def mock_print(mocker):
    return mocker.patch('builtins.print')

@pytest.mark.parametrize("sport,role,grit,teamwork,expected_skill,expected_job", [
    ("Basketball", "Captain", 10, 10, "Team Collaboration", "Customer Success Manager"),
    ("Football", "Captain Walk-on", 10, 10, "Operational Command", "Operations Manager (High Intensity)"),
])
def test_generate_career_plan(sport, role, grit, teamwork, expected_skill, expected_job):
    profile = AthleteProfile(sport=sport, role=role)
    plan = generate_career_plan(profile, grit, teamwork)

    assert plan.profile.sport == sport
    assert plan.profile.role == role
    assert expected_skill in plan.translated_skills

    job_titles = [job.title for job in plan.matching_opportunities]
    assert expected_job in job_titles

@pytest.mark.parametrize("sport,role,grit,teamwork", [
    ("Basketball", "Captain", 10, 10),
])
def test_handle_plan_cli(sport, role, grit, teamwork, mock_print):
    args = argparse.Namespace(sport=sport, role=role, grit=grit, teamwork=teamwork)
    handle_plan(args)

    # Verify that print was called with expected plan sections
    mock_print.assert_any_call(f"\n--- Career Plan for {sport} {role} ---")
    mock_print.assert_any_call("\n# Translated Skills")
    mock_print.assert_any_call("\n# Matching Employers")
    mock_print.assert_any_call("\n# Matching Opportunities")
    mock_print.assert_any_call("\nThe playbook is set. Time to execute.")
