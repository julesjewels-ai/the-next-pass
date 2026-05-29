"""
Tests for the main CLI application logic.
"""
import argparse
import sys
from unittest.mock import Mock

import pytest
from pytest import CaptureFixture
from pytest_mock import MockerFixture
from src.core.models import Employer, AthleteProfile, Job
from typing import Any
from main import (
    handle_employers,
    handle_opportunities,
    handle_demand,
    handle_translate,
    handle_match,
    main
)

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
        [Job(title="Software Engineer", employer="TechCorp", required_skills=["Coding"], base_salary=100000, signing_bonus=10000)],
        ["Software Engineer", "(TechCorp)", "$100,000 base + $10,000 sign-on"]
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
def mock_translate_skills(mocker: MockerFixture) -> Mock:
    return mocker.patch("main.translate_skills")

def test_handle_translate(mock_translate_skills: Mock, capsys: CaptureFixture) -> None:
    mock_translate_skills.return_value = {"Athletic Context": "Corporate Term"}
    args = argparse.Namespace(sport="Football", role="Captain")

    handle_translate(args)
    captured = capsys.readouterr()

    assert "Resume Translation for Football Captain" in captured.out
    assert "Athletic Context:" in captured.out
    assert "Resume Bullet:    \"Corporate Term\"" in captured.out


@pytest.fixture
def mock_match_careers(mocker: MockerFixture) -> Mock:
    return mocker.patch("main.match_careers")

def test_handle_match(mock_match_careers: Mock, capsys: CaptureFixture) -> None:
    mock_match_careers.return_value = [Job(title="Test Job", employer="Test", required_skills=[])]
    args = argparse.Namespace(grit=8, teamwork=9)

    handle_match(args)
    captured = capsys.readouterr()

    assert "Career Matches (Grit: 8, Teamwork: 9)" in captured.out
    assert "- Test Job" in captured.out


@pytest.mark.parametrize("argv, expected_handler, called_with", [
    (["main.py", "translate", "--sport", "Basketball"], "main.handle_translate", {"sport": "Basketball", "role": "Player"}),
    (["main.py", "match", "--grit", "5"], "main.handle_match", {"grit": 5, "teamwork": 9}),
    (["main.py", "employers", "--sport", "Football"], "main.handle_employers", {"sport": "Football", "role": "Player"}),
    (["main.py", "opportunities", "--sport", "Basketball", "--grit", "8"], "main.handle_opportunities", {"sport": "Basketball", "role": "Player", "grit": 8, "teamwork": 9}),
    (["main.py", "demand"], "main.handle_demand", {}),
])
def test_main_dispatch(mocker: MockerFixture, argv: list[str], expected_handler: str, called_with: dict[str, Any]) -> None:
    mocker.patch.object(sys, 'argv', argv)
    mock_handler = mocker.patch(expected_handler)

    main()

    mock_handler.assert_called_once()
    args = mock_handler.call_args[0][0]
    for k, v in called_with.items():
        assert getattr(args, k) == v


def test_main_no_args_prints_help(mocker: MockerFixture, capsys: CaptureFixture) -> None:
    mocker.patch.object(sys, 'argv', ["main.py"])

    main()
    captured = capsys.readouterr()

    assert "usage:" in captured.out
    assert "Available commands" in captured.out

def test_main_invalid_command(mocker: MockerFixture, capsys: CaptureFixture) -> None:
    mocker.patch.object(sys, 'argv', ["main.py", "invalid_command"])
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert "invalid choice: 'invalid_command'" in captured.err
