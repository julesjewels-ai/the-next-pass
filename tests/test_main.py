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
    main,
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
def mock_translate_skills(mocker: MockerFixture) -> Mock:
    """Mock the translate_skills service."""
    return mocker.patch("main.translate_skills")

@pytest.mark.parametrize("mock_return_value, expected_substrings", [
    (
        {"Communication": "Cross-functional communication"},
        ["--- Resume Translation for Football Captain ---", "Athletic Context: \"Communication\"", "Resume Bullet:    \"Cross-functional communication\""]
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
    expected_substrings: list[str]
) -> None:
    """Test handle_translate with various return values."""
    args = argparse.Namespace(sport="Football", role="Captain")
    mock_translate_skills.return_value = mock_return_value

    handle_translate(args)

    captured = capsys.readouterr()
    for expected in expected_substrings:
        assert expected in captured.out, f"Missing expected output: {expected}"

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
        ["--- Career Matches (Grit: 8, Teamwork: 9) ---", "- Software Engineer", "Structure is gone. But your discipline remains."]
    ),
    (
        [],
        ["--- Career Matches (Grit: 8, Teamwork: 9) ---", "Structure is gone. But your discipline remains."]
    )
])
def test_handle_match(
    mock_match_careers: Mock,
    capsys: CaptureFixture,
    mock_return_value: list[Job],
    expected_substrings: list[str]
) -> None:
    """Test handle_match with various return values."""
    args = argparse.Namespace(grit=8, teamwork=9)
    mock_match_careers.return_value = mock_return_value

    handle_match(args)

    captured = capsys.readouterr()
    for expected in expected_substrings:
        assert expected in captured.out, f"Missing expected output: {expected}"

    mock_match_careers.assert_called_once_with(8, 9)


@pytest.mark.parametrize("argv, expect_exit, expected_output, expected_handler", [
    (["main.py"], False, "usage:", None),
    (["main.py", "invalid"], True, "invalid choice", None),
    (["main.py", "translate", "--sport", "Football"], False, None, "handle_translate"),
    (["main.py", "match"], False, None, "handle_match"),
    (["main.py", "employers", "--sport", "Swimming"], False, None, "handle_employers"),
    (["main.py", "opportunities", "--sport", "Golf"], False, None, "handle_opportunities"),
    (["main.py", "demand"], False, None, "handle_demand"),
])
def test_main(
    mocker: MockerFixture,
    capsys: CaptureFixture,
    argv: list[str],
    expect_exit: bool,
    expected_output: str | None,
    expected_handler: str | None
) -> None:
    """Test the main argparse dispatch logic."""
    mocker.patch.object(sys, "argv", argv)

    # Mock handlers to prevent actual logic execution and verify routing
    mock_handlers = {
        "handle_translate": mocker.patch("main.handle_translate"),
        "handle_match": mocker.patch("main.handle_match"),
        "handle_employers": mocker.patch("main.handle_employers"),
        "handle_opportunities": mocker.patch("main.handle_opportunities"),
        "handle_demand": mocker.patch("main.handle_demand"),
    }

    if expect_exit:
        with pytest.raises(SystemExit):
            main()
    else:
        main()

    if expected_output:
        captured = capsys.readouterr()
        # argparse can print to stdout or stderr depending on the version/command
        assert expected_output in captured.out or expected_output in captured.err, f"Missing expected output: {expected_output}"

    if expected_handler:
        mock_handlers[expected_handler].assert_called_once()
        # Ensure others were not called
        for name, mock in mock_handlers.items():
            if name != expected_handler:
                mock.assert_not_called()


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
