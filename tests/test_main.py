"""
Tests for the main CLI application logic.
"""
import argparse
from unittest.mock import Mock

import pytest
from pytest import CaptureFixture
from pytest_mock import MockerFixture

from main import handle_demand, handle_employers, handle_opportunities, handle_plan
from src.core.models import AthleteProfile, CareerPlan, Employer, Job


@pytest.fixture
def mock_match_employers(mocker: MockerFixture) -> Mock:
    """Mock the match_employers service."""
    return mocker.patch("main.match_employers")

@pytest.mark.parametrize("mock_return_value, expected_substrings", [
    (
        [Employer(name="TechCorp", industry="Tech", required_skills=["Coding"])],
        ["TechCorp", "(Tech)", "Required Skills: Coding"]
    ),
    (
        [],
        ["No direct matches found", "Keep training"]
    ),
    (
        [
            Employer(name="TechCorp", industry="Tech", required_skills=["Coding"]),
            Employer(name="BizCorp", industry="Business", required_skills=["Strategy"])
        ],
        ["TechCorp", "BizCorp", "Coding", "Strategy"]
    )
])
def test_handle_employers(
    mock_match_employers: Mock,
    capsys: CaptureFixture,
    mock_return_value: list[Employer],
    expected_substrings: list[str]
) -> None:
    """Test handle_employers with various match scenarios."""
    # Arrange
    args = argparse.Namespace(sport="Football", role="Captain")
    mock_match_employers.return_value = mock_return_value

    # Act
    handle_employers(args)

    # Assert
    captured = capsys.readouterr()
    for substring in expected_substrings:
        assert substring in captured.out

    # Verify the service was called with correct profile
    mock_match_employers.assert_called_once()
    call_arg = mock_match_employers.call_args[0][0]
    assert isinstance(call_arg, AthleteProfile)
    assert call_arg.sport == "Football"
    assert call_arg.role == "Captain"


@pytest.fixture
def mock_match_opportunities(mocker: MockerFixture) -> Mock:
    """Mock the match_opportunities service."""
    return mocker.patch("main.match_opportunities")

@pytest.mark.parametrize("mock_return_value, expected_substrings", [
    (
        [Job(title="Software Engineer", employer="TechCorp", required_skills=["Coding"])],
        ["Software Engineer", "(TechCorp)"]
    ),
    (
        [],
        ["No direct matches found", "Expand your skillset"]
    ),
])
def test_handle_opportunities(
    mock_match_opportunities: Mock,
    capsys: CaptureFixture,
    mock_return_value: list[Job],
    expected_substrings: list[str]
) -> None:
    """Test handle_opportunities with various match scenarios."""
    # Arrange
    args = argparse.Namespace(sport="Football", role="Captain", grit=8, teamwork=9)
    mock_match_opportunities.return_value = mock_return_value

    # Act
    handle_opportunities(args)

    # Assert
    captured = capsys.readouterr()
    for substring in expected_substrings:
        assert substring in captured.out

    # Verify the service was called with correct arguments
    mock_match_opportunities.assert_called_once()
    # Call args: (profile, grit, teamwork)
    call_args = mock_match_opportunities.call_args[0]
    profile_arg = call_args[0]
    grit_arg = call_args[1]
    teamwork_arg = call_args[2]

    assert isinstance(profile_arg, AthleteProfile)
    assert profile_arg.sport == "Football"
    assert profile_arg.role == "Captain"
    assert grit_arg == 8
    assert teamwork_arg == 9

@pytest.fixture
def mock_get_skill_demand_report(mocker: MockerFixture) -> Mock:
    """Mock the get_skill_demand_report service."""
    return mocker.patch("main.get_skill_demand_report")

def test_handle_demand_with_data(mock_get_skill_demand_report: Mock, capsys: CaptureFixture) -> None:
    """Test handle_demand when report returns data."""
    mock_get_skill_demand_report.return_value = {"Leadership": 5, "Teamwork": 3}
    args = argparse.Namespace()

    handle_demand(args)
    captured = capsys.readouterr()

    assert "--- Skill Demand Analytics ---" in captured.out
    assert "- Leadership: Required by 5 role(s)" in captured.out
    assert "- Teamwork: Required by 3 role(s)" in captured.out
    assert "Train for what the market demands." in captured.out
    mock_get_skill_demand_report.assert_called_once()

def test_handle_demand_empty_data(mock_get_skill_demand_report: Mock, capsys: CaptureFixture) -> None:
    """Test handle_demand when report returns empty."""
    mock_get_skill_demand_report.return_value = {}
    args = argparse.Namespace()

    handle_demand(args)
    captured = capsys.readouterr()

    assert "No job data available to calculate demand." in captured.out
    mock_get_skill_demand_report.assert_called_once()

@pytest.fixture
def mock_generate_career_plan(mocker: MockerFixture) -> Mock:
    """Mock the generate_career_plan service."""
    return mocker.patch("main.generate_career_plan")

def test_handle_plan_found_ready(mock_generate_career_plan: Mock, capsys: CaptureFixture) -> None:
    """Test handle_plan when target job is found and athlete is ready."""
    mock_plan = CareerPlan(
        target_job_title="Project Coordinator",
        current_skills=["Team Collaboration"],
        missing_skills=[],
        is_ready=True
    )
    mock_generate_career_plan.return_value = mock_plan
    args = argparse.Namespace(sport="Basketball", role="Player", target_job="Project Coordinator")

    handle_plan(args)
    captured = capsys.readouterr()

    assert "Career Plan for Basketball Player targeting 'Project Coordinator'" in captured.out
    assert "Status: READY." in captured.out
    mock_generate_career_plan.assert_called_once()

def test_handle_plan_found_gap(mock_generate_career_plan: Mock, capsys: CaptureFixture) -> None:
    """Test handle_plan when target job is found but athlete has skill gaps."""
    mock_plan = CareerPlan(
        target_job_title="Sales Development Representative",
        current_skills=["Team Collaboration"],
        missing_skills=["Strategic Analysis"],
        is_ready=False
    )
    mock_generate_career_plan.return_value = mock_plan
    args = argparse.Namespace(sport="Basketball", role="Player", target_job="Sales Development Representative")

    handle_plan(args)
    captured = capsys.readouterr()

    assert "Career Plan for Basketball Player targeting 'Sales Development Representative'" in captured.out
    assert "Status: GAP DETECTED." in captured.out
    assert "- Strategic Analysis" in captured.out
    mock_generate_career_plan.assert_called_once()

def test_handle_plan_not_found(mock_generate_career_plan: Mock, capsys: CaptureFixture) -> None:
    """Test handle_plan when target job is not found."""
    mock_generate_career_plan.return_value = None
    args = argparse.Namespace(sport="Basketball", role="Player", target_job="Astronaut")

    handle_plan(args)
    captured = capsys.readouterr()

    assert "Target job 'Astronaut' not found in our database." in captured.out
    mock_generate_career_plan.assert_called_once()
