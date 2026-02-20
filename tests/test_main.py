"""
Tests for the main CLI application logic.
"""
import argparse
from unittest.mock import Mock

import pytest
from pytest import CaptureFixture
from pytest_mock import MockerFixture
from src.core.models import Employer, AthleteProfile, Job
from main import handle_employers, handle_translate, handle_match

@pytest.fixture
def mock_match_careers(mocker: MockerFixture) -> Mock:
    """Mock the match_careers service."""
    return mocker.patch("main.match_careers")

@pytest.fixture
def mock_translate_skills(mocker: MockerFixture) -> Mock:
    """Mock the translate_skills service."""
    return mocker.patch("main.translate_skills")

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


@pytest.mark.parametrize("mock_return_value, expected_substrings", [
    (
        [Job(title="Software Engineer", min_grit=5, min_teamwork=5)],
        ["Software Engineer", "Structure is gone"]
    ),
    (
        [],
        ["Structure is gone"]
    ),
    (
        [
            Job(title="CEO", min_grit=10, min_teamwork=10),
            Job(title="Founder", min_grit=10, min_teamwork=10)
        ],
        ["CEO", "Founder"]
    )
])
def test_handle_match(
    mock_match_careers: Mock,
    capsys: CaptureFixture,
    mock_return_value: list[Job],
    expected_substrings: list[str]
) -> None:
    """Test handle_match with various job matches."""
    # Arrange
    args = argparse.Namespace(grit=8, teamwork=9)
    mock_match_careers.return_value = mock_return_value

    # Act
    handle_match(args)

    # Assert
    captured = capsys.readouterr()
    for substring in expected_substrings:
        assert substring in captured.out

    # Verify call
    mock_match_careers.assert_called_once_with(8, 9)


@pytest.mark.parametrize("mock_return_value, expected_substrings", [
    (
        {"Agility": "Quick reactions"},
        ["Athletic Context: \"Agility\"", "Resume Bullet:    \"Quick reactions\""]
    ),
    (
        {},
        ["Resume Translation for Football Captain"]
    ),
    (
        {"Teamwork": "Collaboration", "Leadership": "Management"},
        ["Teamwork", "Collaboration", "Leadership", "Management"]
    )
])
def test_handle_translate(
    mock_translate_skills: Mock,
    capsys: CaptureFixture,
    mock_return_value: dict[str, str],
    expected_substrings: list[str]
) -> None:
    """Test handle_translate with various skill mappings."""
    # Arrange
    args = argparse.Namespace(sport="Football", role="Captain")
    mock_translate_skills.return_value = mock_return_value

    # Act
    handle_translate(args)

    # Assert
    captured = capsys.readouterr()
    for substring in expected_substrings:
        assert substring in captured.out

    # Verify the service was called with correct profile
    mock_translate_skills.assert_called_once()
    call_arg = mock_translate_skills.call_args[0][0]
    assert isinstance(call_arg, AthleteProfile)
    assert call_arg.sport == "Football"
    assert call_arg.role == "Captain"
