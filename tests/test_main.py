"""
Tests for the main CLI application logic.
"""
import argparse
from typing import List, Dict, Any
from unittest.mock import Mock

import pytest
from pytest import CaptureFixture
from pytest_mock import MockerFixture
from src.core.models import Employer, AthleteProfile, Job
from main import handle_employers, handle_opportunities, handle_translate, handle_match, main

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
        {"Touchdown": "Successful Project Completion", "Interception": "Risk Mitigation"},
        ["Athletic Context: \"Touchdown\"", "Resume Bullet:    \"Successful Project Completion\"", "Athletic Context: \"Interception\"", "Resume Bullet:    \"Risk Mitigation\""]
    ),
    (
        {},
        []
    ),
])
def test_handle_translate(
    mock_translate_skills: Mock,
    capsys: CaptureFixture,
    mock_return_value: dict,
    expected_substrings: List[str]
) -> None:
    """Test handle_translate with various translation scenarios."""
    # Arrange
    args = argparse.Namespace(sport="Football", role="Captain")
    mock_translate_skills.return_value = mock_return_value

    # Act
    handle_translate(args)

    # Assert
    captured = capsys.readouterr()
    for substring in expected_substrings:
        assert substring in captured.out

    # Verify
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
        [Job(title="Software Engineer"), Job(title="Data Scientist")],
        ["- Software Engineer", "- Data Scientist", "Structure is gone. But your discipline remains."]
    ),
    (
        [],
        ["Structure is gone. But your discipline remains."]
    ),
])
def test_handle_match(
    mock_match_careers: Mock,
    capsys: CaptureFixture,
    mock_return_value: List[Job],
    expected_substrings: List[str]
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
        assert substring in captured.out

    # Verify
    mock_match_careers.assert_called_once_with(8, 9)


@pytest.mark.parametrize("argv, handler_name, expected_args", [
    (
        ["translate", "--sport", "Football", "--role", "Captain"],
        "handle_translate",
        {"sport": "Football", "role": "Captain"}
    ),
    (
        ["match", "--grit", "8", "--teamwork", "9"],
        "handle_match",
        {"grit": 8, "teamwork": 9}
    ),
    (
        ["employers", "--sport", "Football", "--role", "Captain"],
        "handle_employers",
        {"sport": "Football", "role": "Captain"}
    ),
    (
        ["opportunities", "--sport", "Football", "--role", "Captain", "--grit", "8", "--teamwork", "9"],
        "handle_opportunities",
        {"sport": "Football", "role": "Captain", "grit": 8, "teamwork": 9}
    ),
])
def test_main_dispatch(
    mocker: MockerFixture,
    argv: List[str],
    handler_name: str,
    expected_args: Dict[str, Any]
) -> None:
    """Test main dispatch logic."""
    # Arrange
    mock_handler = mocker.patch(f"main.{handler_name}")
    mocker.patch("sys.argv", ["main.py"] + argv)

    # Act
    main()

    # Assert
    mock_handler.assert_called_once()
    call_args = mock_handler.call_args[0][0]
    assert isinstance(call_args, argparse.Namespace)
    for key, value in expected_args.items():
        assert getattr(call_args, key) == value

def test_main_no_args(mocker: MockerFixture, capsys: CaptureFixture) -> None:
    """Test main with no arguments prints help."""
    mocker.patch("sys.argv", ["main.py"])

    # Act
    main()

    # Assert
    captured = capsys.readouterr()
    assert "usage:" in captured.out or "usage:" in captured.err

def test_main_version(mocker: MockerFixture, capsys: CaptureFixture) -> None:
    """Test main with --version prints version."""
    mocker.patch("sys.argv", ["main.py", "--version"])

    # Act
    with pytest.raises(SystemExit):
        main()

    # Assert
    captured = capsys.readouterr()
    assert "0.1.0-mvp" in captured.out
