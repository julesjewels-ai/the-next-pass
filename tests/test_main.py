"""
Tests for the main CLI application logic.
"""
import argparse
from unittest.mock import Mock

import pytest
from pytest import CaptureFixture
from pytest_mock import MockerFixture
import sys
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
def mock_translate_skills(mocker: MockerFixture) -> Mock:
    """Mock the translate_skills service."""
    return mocker.patch("main.translate_skills")

@pytest.mark.parametrize("mock_return_value, expected_substrings", [
    (
        {"Captain": "Leader"},
        ["--- Resume Translation for Football Captain ---", "Athletic Context: \"Captain\"", "Resume Bullet:    \"Leader\""]
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
    """Test handle_translate with various match scenarios."""
    # Arrange
    args = argparse.Namespace(sport="Football", role="Captain")
    mock_translate_skills.return_value = mock_return_value

    # Act
    handle_translate(args)

    # Assert
    captured = capsys.readouterr()
    for substring in expected_substrings:
        assert substring in captured.out, f"Expected '{substring}' to be in stdout: {captured.out}"

    # Verify the service was called with correct profile
    mock_translate_skills.assert_called_once()
    call_arg = mock_translate_skills.call_args[0][0]
    assert isinstance(call_arg, AthleteProfile), f"Expected AthleteProfile, got {type(call_arg)}"
    assert call_arg.sport == "Football", f"Expected sport 'Football', got {call_arg.sport}"
    assert call_arg.role == "Captain", f"Expected role 'Captain', got {call_arg.role}"


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
    ),
])
def test_handle_match(
    mock_match_careers: Mock,
    capsys: CaptureFixture,
    mock_return_value: list[Job],
    expected_substrings: list[str]
) -> None:
    """Test handle_match with various match scenarios."""
    # Arrange
    args = argparse.Namespace(grit=8, teamwork=9)
    mock_match_careers.return_value = mock_return_value

    # Act
    handle_match(args)

    # Assert
    captured = capsys.readouterr()
    for substring in expected_substrings:
        assert substring in captured.out, f"Expected '{substring}' to be in stdout: {captured.out}"

    # Verify the service was called with correct arguments
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
        assert substring in captured.out, f"Expected '{substring}' to be in stdout: {captured.out}"

    # Verify the service was called with correct profile
    mock_match_employers.assert_called_once()
    call_arg = mock_match_employers.call_args[0][0]
    assert isinstance(call_arg, AthleteProfile), f"Expected AthleteProfile, got {type(call_arg)}"
    assert call_arg.sport == "Football", f"Expected sport 'Football', got {call_arg.sport}"
    assert call_arg.role == "Captain", f"Expected role 'Captain', got {call_arg.role}"


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
        assert substring in captured.out, f"Expected '{substring}' to be in stdout: {captured.out}"

    # Verify the service was called with correct arguments
    mock_match_opportunities.assert_called_once()
    # Call args: (profile, grit, teamwork)
    call_args = mock_match_opportunities.call_args[0]
    profile_arg = call_args[0]
    grit_arg = call_args[1]
    teamwork_arg = call_args[2]

    assert isinstance(profile_arg, AthleteProfile), f"Expected AthleteProfile, got {type(profile_arg)}"
    assert profile_arg.sport == "Football", f"Expected sport 'Football', got {profile_arg.sport}"
    assert profile_arg.role == "Captain", f"Expected role 'Captain', got {profile_arg.role}"
    assert grit_arg == 8, f"Expected grit 8, got {grit_arg}"
    assert teamwork_arg == 9, f"Expected teamwork 9, got {teamwork_arg}"

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

    assert "--- Skill Demand Analytics ---" in captured.out, f"Expected analytic header in: {captured.out}"
    assert "- Leadership: Required by 5 role(s)" in captured.out, f"Expected leadership count in: {captured.out}"
    assert "- Teamwork: Required by 3 role(s)" in captured.out, f"Expected teamwork count in: {captured.out}"
    assert "Train for what the market demands." in captured.out, f"Expected closing statement in: {captured.out}"
    mock_get_skill_demand_report.assert_called_once()

def test_handle_demand_empty_data(mock_get_skill_demand_report: Mock, capsys: CaptureFixture) -> None:
    """Test handle_demand when report returns empty."""
    mock_get_skill_demand_report.return_value = {}
    args = argparse.Namespace()

    handle_demand(args)
    captured = capsys.readouterr()

    assert "No job data available to calculate demand." in captured.out, f"Expected empty data message in: {captured.out}"
    mock_get_skill_demand_report.assert_called_once()


@pytest.mark.parametrize("argv, mocked_handler_name, expected_exception", [
    (["main.py", "translate", "--sport", "Basketball", "--role", "Starter"], "main.handle_translate", None),
    (["main.py", "match", "--grit", "5", "--teamwork", "6"], "main.handle_match", None),
    (["main.py", "employers", "--sport", "Basketball", "--role", "Starter"], "main.handle_employers", None),
    (["main.py", "opportunities", "--sport", "Basketball", "--role", "Starter", "--grit", "7", "--teamwork", "8"], "main.handle_opportunities", None),
    (["main.py", "demand"], "main.handle_demand", None),
    (["main.py", "invalid_command"], "argparse.ArgumentParser.print_help", SystemExit),
    (["main.py"], "argparse.ArgumentParser.print_help", None),
])
def test_main_dispatch(
    mocker: MockerFixture,
    argv: list[str],
    mocked_handler_name: str,
    expected_exception: type[Exception] | None
) -> None:
    """Test main command dispatch logic."""
    mocker.patch.object(sys, 'argv', argv)

    mock_handler = mocker.patch(mocked_handler_name)

    if expected_exception:
        with pytest.raises(expected_exception):
            main()
    else:
        main()
        mock_handler.assert_called_once()
