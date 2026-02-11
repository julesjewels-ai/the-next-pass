import argparse
import sys
import pytest
from pytest import CaptureFixture, MonkeyPatch
from unittest.mock import MagicMock
from src.core.models import Job, Employer
import main
from typing import List, Dict, Any

# Fixtures for mocked services
@pytest.fixture
def mock_translate_skills(mocker: Any) -> MagicMock:
    return mocker.patch("main.translate_skills")

@pytest.fixture
def mock_match_careers(mocker: Any) -> MagicMock:
    return mocker.patch("main.match_careers")

@pytest.fixture
def mock_match_employers(mocker: Any) -> MagicMock:
    return mocker.patch("main.match_employers")

# --- handle_translate tests ---

@pytest.mark.parametrize("sport, role, translated_skills", [
    ("Football", "Captain", {"Leadership": "Led team", "Strategy": "Game plans"}),
    ("Swimming", "Swimmer", {"Discipline": "Early mornings"}),
])
def test_handle_translate(
    capsys: CaptureFixture,
    mock_translate_skills: MagicMock,
    sport: str,
    role: str,
    translated_skills: Dict[str, str]
) -> None:
    # Arrange
    args = argparse.Namespace(sport=sport, role=role)
    mock_translate_skills.return_value = translated_skills

    # Act
    main.handle_translate(args)

    # Assert
    mock_translate_skills.assert_called_once()
    args_passed = mock_translate_skills.call_args[0][0]
    assert args_passed.sport == sport
    assert args_passed.role == role

    captured = capsys.readouterr()
    assert f"Resume Translation for {sport} {role}" in captured.out
    for key, value in translated_skills.items():
        assert f"Athletic Context: \"{key}\"" in captured.out
        assert f"Resume Bullet:    \"{value}\"" in captured.out

# --- handle_match tests ---

@pytest.mark.parametrize("grit, teamwork, expected_jobs", [
    (8, 9, [Job(title="Manager"), Job(title="Lead")]),
    (5, 5, [Job(title="Associate")]),
])
def test_handle_match(
    capsys: CaptureFixture,
    mock_match_careers: MagicMock,
    grit: int,
    teamwork: int,
    expected_jobs: List[Job]
) -> None:
    # Arrange
    args = argparse.Namespace(grit=grit, teamwork=teamwork)
    mock_match_careers.return_value = expected_jobs

    # Act
    main.handle_match(args)

    # Assert
    mock_match_careers.assert_called_once_with(grit, teamwork)

    captured = capsys.readouterr()
    assert f"Career Matches (Grit: {grit}, Teamwork: {teamwork})" in captured.out
    for job in expected_jobs:
        assert f"- {job.title}" in captured.out
    assert "Structure is gone. But your discipline remains." in captured.out

# --- handle_employers tests ---

@pytest.mark.parametrize("sport, role, matches, expected_output_snippets", [
    (
        "Football", "Captain",
        [
            Employer(name="TechCorp", industry="Technology", required_skills=["Coding"]),
            Employer(name="BizInc", industry="Business", required_skills=["Sales"])
        ],
        [
            "Employer Matches for Football Captain",
            "- TechCorp (Technology)",
            "Required Skills: Coding",
            "- BizInc (Business)",
            "Network is net worth."
        ]
    ),
    (
        "Golf", "Player",
        [],
        [
            "No direct matches found. Keep training."
        ]
    )
])
def test_handle_employers(
    capsys: CaptureFixture,
    mock_match_employers: MagicMock,
    sport: str,
    role: str,
    matches: List[Employer],
    expected_output_snippets: List[str]
) -> None:
    # Arrange
    args = argparse.Namespace(sport=sport, role=role)
    mock_match_employers.return_value = matches

    # Act
    main.handle_employers(args)

    # Assert
    mock_match_employers.assert_called_once()
    args_passed = mock_match_employers.call_args[0][0]
    assert args_passed.sport == sport
    assert args_passed.role == role

    captured = capsys.readouterr()
    for snippet in expected_output_snippets:
        assert snippet in captured.out

# --- main (dispatch) tests ---

@pytest.mark.parametrize("cli_args, expected_handler_mock", [
    (["translate", "--sport", "Football", "--role", "Captain"], "mock_translate_skills"),
    (["match", "--grit", "8", "--teamwork", "9"], "mock_match_careers"),
    (["employers", "--sport", "Football"], "mock_match_employers"),
])
def test_main_dispatch(
    monkeypatch: MonkeyPatch,
    request: pytest.FixtureRequest,
    cli_args: List[str],
    expected_handler_mock: str
) -> None:
    # Arrange
    mock_handler = request.getfixturevalue(expected_handler_mock)

    # Mocking sys.argv. The first arg is the script name.
    monkeypatch.setattr(sys, "argv", ["main.py"] + cli_args)

    # Act
    main.main()

    # Assert
    mock_handler.assert_called_once()

def test_main_no_command(monkeypatch: MonkeyPatch, capsys: CaptureFixture) -> None:
    # Arrange
    monkeypatch.setattr(sys, "argv", ["main.py"])

    # Act
    main.main()

    # Assert
    captured = capsys.readouterr()
    assert "usage:" in captured.out

def test_main_invalid_command(monkeypatch: MonkeyPatch, capsys: CaptureFixture) -> None:
    # Arrange
    monkeypatch.setattr(sys, "argv", ["main.py", "invalid_command"])

    # Act
    with pytest.raises(SystemExit):
        main.main()

    # Assert
    captured = capsys.readouterr()
    assert "invalid choice: 'invalid_command'" in captured.err
