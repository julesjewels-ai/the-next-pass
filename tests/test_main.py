"""
Tests for the main CLI application logic.
"""
import argparse
from typing import List
import sys
from typing import Any
from unittest.mock import Mock

import pytest
from pytest import CaptureFixture
from pytest_mock import MockerFixture
from src.core.models import Employer, AthleteProfile, Job
from main import (
    handle_employers,
    handle_opportunities,
    handle_demand,
    handle_translate,
    handle_match,
    main as main_func
)

@pytest.fixture
def mock_translate_skills(mocker: MockerFixture) -> Mock:
    """Mock the translate_skills service."""
    return mocker.patch("main.translate_skills")

@pytest.mark.parametrize("mock_return_value, expected_substrings", [
    (
        {"Called audible": "Adapted to changing circumstances"},
        ["Athletic Context: \"Called audible\"", "Resume Bullet:    \"Adapted to changing circumstances\""]
    ),
    (
        {},
        ["--- Resume Translation for Football Captain ---"]
    )
])
def test_handle_translate(
    mock_translate_skills: Mock,
    capsys: CaptureFixture,
    mock_return_value: dict[str, str],
    expected_substrings: List[str]
) -> None:
    """Test handle_translate with various translation scenarios."""
    args = argparse.Namespace(sport="Football", role="Captain")
    mock_translate_skills.return_value = mock_return_value

    handle_translate(args)

    captured = capsys.readouterr()
    for substring in expected_substrings:
        assert substring in captured.out

    mock_translate_skills.assert_called_once()
    call_arg = mock_translate_skills.call_args[0][0]
    assert isinstance(call_arg, AthleteProfile)
    assert call_arg.sport == "Football"
    assert call_arg.role == "Captain"


@pytest.fixture
def mock_match_careers(mocker: MockerFixture) -> Mock:
    """Mock the match_careers service."""
    return mocker.patch("main.match_careers")

@pytest.mark.parametrize("mock_return_value, expected_substrings", [
    (
        [Job(title="Software Engineer", employer="TechCorp", required_skills=["Coding"])],
        ["- Software Engineer", "Structure is gone. But your discipline remains."]
    ),
    (
        [],
        ["Structure is gone. But your discipline remains."]
    )
])
def test_handle_match(
    mock_match_careers: Mock,
    capsys: CaptureFixture,
    mock_return_value: List[Job],
    expected_substrings: List[str]
) -> None:
    """Test handle_match with career match scenarios."""
    args = argparse.Namespace(grit=8, teamwork=9)
    mock_match_careers.return_value = mock_return_value

    handle_match(args)

    captured = capsys.readouterr()
    for substring in expected_substrings:
        assert substring in captured.out

    mock_match_careers.assert_called_once_with(8, 9)


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
    mock_return_value: List[Employer],
    expected_substrings: List[str]
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
    mock_return_value: List[Job],
    expected_substrings: List[str]
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
def mock_handlers(mocker: MockerFixture) -> dict[str, Mock]:
    """Mock all handlers to test dispatch logic."""
    return {
        "translate": mocker.patch("main.handle_translate"),
        "match": mocker.patch("main.handle_match"),
        "employers": mocker.patch("main.handle_employers"),
        "opportunities": mocker.patch("main.handle_opportunities"),
        "demand": mocker.patch("main.handle_demand")
    }

@pytest.mark.parametrize("argv, expected_handler, expected_args", [
    (["main.py", "translate", "--sport", "Football"], "translate", {"sport": "Football", "role": "Player"}),
    (["main.py", "match"], "match", {"grit": 8, "teamwork": 9}),
    (["main.py", "employers", "--sport", "Basketball", "--role", "Guard"], "employers", {"sport": "Basketball", "role": "Guard"}),
    (["main.py", "opportunities", "--sport", "Swimming", "--grit", "10"], "opportunities", {"sport": "Swimming", "role": "Player", "grit": 10, "teamwork": 9}),
    (["main.py", "demand"], "demand", {}),
])
def test_main_dispatch_valid_commands(
    mocker: MockerFixture,
    mock_handlers: dict[str, Mock],
    argv: List[str],
    expected_handler: str,
    expected_args: dict[str, Any]
) -> None:
    """Test main dispatching logic for valid commands."""
    mocker.patch.object(sys, "argv", argv)

    main_func()

    handler = mock_handlers[expected_handler]
    handler.assert_called_once()

    # Verify the arguments passed to the handler
    args_obj = handler.call_args[0][0]
    for key, value in expected_args.items():
        assert getattr(args_obj, key) == value

def test_main_dispatch_no_args(mocker: MockerFixture, capsys: CaptureFixture) -> None:
    """Test main dispatching logic when no arguments are provided."""
    mocker.patch.object(sys, "argv", ["main.py"])

    # Depending on argparse configuration, it might raise SystemExit or print help directly
    # The codebase memory states "When executing main() with no arguments, it calls parser.print_help() but does not raise SystemExit."
    main_func()

    captured = capsys.readouterr()
    assert "usage:" in captured.out
    assert "Available commands" in captured.out

def test_main_dispatch_invalid_command(mocker: MockerFixture, capsys: CaptureFixture) -> None:
    """Test main dispatching logic for invalid commands."""
    mocker.patch.object(sys, "argv", ["main.py", "invalid_command"])

    with pytest.raises(SystemExit):
        main_func()

    captured = capsys.readouterr()
    assert "invalid choice: 'invalid_command'" in captured.err
