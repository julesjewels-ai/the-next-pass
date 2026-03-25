"""
Tests for the main CLI application logic.
"""
import argparse
import sys
from typing import List
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
def mock_translate_skills(mocker: MockerFixture) -> Mock:
    """Mock the translate_skills service."""
    return mocker.patch("main.translate_skills")

@pytest.mark.parametrize("mock_return_value, expected_substrings", [
    (
        {"Played through injury": "Demonstrated resilience under pressure"},
        ["Played through injury", "Demonstrated resilience under pressure"]
    ),
    (
        {},
        ["--- Resume Translation"]
    )
])
def test_handle_translate(
    mock_translate_skills: Mock,
    capsys: CaptureFixture,
    mock_return_value: dict[str, str],
    expected_substrings: list[str]
) -> None:
    """Test handle_translate with various translations."""
    args = argparse.Namespace(sport="Basketball", role="Starter")
    mock_translate_skills.return_value = mock_return_value

    handle_translate(args)

    captured = capsys.readouterr()
    for substring in expected_substrings:
        assert substring in captured.out, f"Missing expected output: {substring}"

    mock_translate_skills.assert_called_once()
    call_arg = mock_translate_skills.call_args[0][0]
    assert isinstance(call_arg, AthleteProfile)
    assert call_arg.sport == "Basketball"
    assert call_arg.role == "Starter"


@pytest.fixture
def mock_match_careers(mocker: MockerFixture) -> Mock:
    """Mock the match_careers service."""
    return mocker.patch("main.match_careers")

@pytest.mark.parametrize("mock_return_value, expected_substrings", [
    (
        [Job(title="Sales Rep", employer="Acme", required_skills=["Sales"])],
        ["--- Career Matches", "Sales Rep"]
    ),
    (
        [],
        ["--- Career Matches", "Structure is gone. But your discipline remains."]
    )
])
def test_handle_match(
    mock_match_careers: Mock,
    capsys: CaptureFixture,
    mock_return_value: list[Job],
    expected_substrings: list[str]
) -> None:
    """Test handle_match with various matches."""
    args = argparse.Namespace(grit=7, teamwork=8)
    mock_match_careers.return_value = mock_return_value

    handle_match(args)

    captured = capsys.readouterr()
    for substring in expected_substrings:
        assert substring in captured.out, f"Missing expected output: {substring}"

    mock_match_careers.assert_called_once_with(7, 8)

@pytest.mark.parametrize("test_argv, expected_call, expected_exit", [
    (
        ["main.py", "translate", "--sport", "Football", "--role", "Captain"],
        "handle_translate",
        None
    ),
    (
        ["main.py", "match", "--grit", "8", "--teamwork", "9"],
        "handle_match",
        None
    ),
    (
        ["main.py", "employers", "--sport", "Swimming"],
        "handle_employers",
        None
    ),
    (
        ["main.py", "opportunities", "--sport", "Baseball"],
        "handle_opportunities",
        None
    ),
    (
        ["main.py", "demand"],
        "handle_demand",
        None
    ),
    (
        ["main.py"],
        None,
        None
    ),
    (
        ["main.py", "invalid_command"],
        None,
        SystemExit
    )
])
def test_main_dispatch(
    mocker: MockerFixture,
    capsys: CaptureFixture,
    test_argv: list[str],
    expected_call: str | None,
    expected_exit: type[Exception] | None
) -> None:
    """Test the main dispatch logic based on CLI arguments."""
    mocker.patch.object(sys, "argv", test_argv)

    # Mock all handlers to prevent actual execution
    handlers = {
        "handle_translate": mocker.patch("main.handle_translate"),
        "handle_match": mocker.patch("main.handle_match"),
        "handle_employers": mocker.patch("main.handle_employers"),
        "handle_opportunities": mocker.patch("main.handle_opportunities"),
        "handle_demand": mocker.patch("main.handle_demand")
    }

    if expected_exit:
        with pytest.raises(expected_exit):
            main()
    else:
        main()
        if expected_call:
            handlers[expected_call].assert_called_once()

            # Ensure other handlers weren't called
            for name, mock_handler in handlers.items():
                if name != expected_call:
                    mock_handler.assert_not_called()
        else:
            # Empty args triggers parser.print_help() without SystemExit
            captured = capsys.readouterr()
            assert "usage:" in captured.out or "usage:" in captured.err
