import argparse
import sys
from typing import List, Dict
import pytest
from pytest_mock import MockerFixture
from src.core.models import Job, Employer
from main import handle_translate, handle_match, handle_employers, main


@pytest.mark.parametrize("matches, expected_output", [
    (
        [Employer(name="Alpha", industry="Tech", required_skills=["Code"])],
        ["Alpha (Tech)", "Required Skills: Code"]
    ),
    (
        [],
        ["No direct matches found. Keep training."]
    )
])
def test_handle_employers(
    matches: List[Employer],
    expected_output: List[str],
    mocker: MockerFixture,
    capsys: pytest.CaptureFixture
) -> None:
    """Test handle_employers prints correct output based on matches."""
    # Arrange
    args = argparse.Namespace(sport="Football", role="Captain")
    mock_match = mocker.patch("main.match_employers", return_value=matches)

    # Act
    handle_employers(args)

    # Assert
    captured = capsys.readouterr()
    mock_match.assert_called_once()
    for text in expected_output:
        assert text in captured.out


@pytest.mark.parametrize("translation_result, expected_bullets", [
    (
        {"Field Vision": "Strategic Analysis"},
        ['Athletic Context: "Field Vision"', 'Resume Bullet:    "Strategic Analysis"']
    )
])
def test_handle_translate(
    translation_result: Dict[str, str],
    expected_bullets: List[str],
    mocker: MockerFixture,
    capsys: pytest.CaptureFixture
) -> None:
    """Test handle_translate prints correct skill translations."""
    # Arrange
    args = argparse.Namespace(sport="Basketball", role="Guard")
    mock_translate = mocker.patch("main.translate_skills", return_value=translation_result)

    # Act
    handle_translate(args)

    # Assert
    captured = capsys.readouterr()
    mock_translate.assert_called_once()
    for bullet in expected_bullets:
        assert bullet in captured.out


@pytest.mark.parametrize("career_matches, expected_titles", [
    (
        [Job(title="Sales Rep"), Job(title="Consultant")],
        ["- Sales Rep", "- Consultant"]
    ),
    (
        [],
        ["Structure is gone. But your discipline remains."]
    )
])
def test_handle_match(
    career_matches: List[Job],
    expected_titles: List[str],
    mocker: MockerFixture,
    capsys: pytest.CaptureFixture
) -> None:
    """Test handle_match prints career suggestions."""
    # Arrange
    args = argparse.Namespace(grit=8, teamwork=9)
    mock_match_careers = mocker.patch("main.match_careers", return_value=career_matches)

    # Act
    handle_match(args)

    # Assert
    captured = capsys.readouterr()
    mock_match_careers.assert_called_once_with(8, 9)
    for title in expected_titles:
        assert title in captured.out


@pytest.mark.parametrize("cli_args, mocked_handler_name", [
    (["main.py", "translate", "--sport", "Football", "--role", "Captain"], "main.handle_translate"),
    (["main.py", "match", "--grit", "5", "--teamwork", "5"], "main.handle_match"),
    (["main.py", "employers", "--sport", "Tennis"], "main.handle_employers"),
])
def test_main_dispatch(
    cli_args: List[str],
    mocked_handler_name: str,
    mocker: MockerFixture
) -> None:
    """Test that main dispatches to the correct handler based on arguments."""
    # Arrange
    mocker.patch.object(sys, 'argv', cli_args)
    mock_handler = mocker.patch(mocked_handler_name)

    # Act
    main()

    # Assert
    mock_handler.assert_called_once()


def test_main_no_args_prints_help(mocker: MockerFixture, capsys: pytest.CaptureFixture) -> None:
    """Test that main prints help when no arguments are provided."""
    # Arrange
    mocker.patch.object(sys, 'argv', ["main.py"])

    # Act
    main()

    # Assert
    captured = capsys.readouterr()
    assert "usage:" in captured.out or "usage:" in captured.err
