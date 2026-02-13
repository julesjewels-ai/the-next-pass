import pytest
import argparse
from typing import List, Dict, Any
from pytest_mock import MockerFixture
from main import main, handle_translate, handle_match, handle_employers
from src.core.models import AthleteProfile, Job, Employer

@pytest.mark.parametrize("command_args, expected_handler, expected_attrs", [
    (
        ["main.py", "translate", "--sport", "Football", "--role", "Captain"],
        "translate",
        {"sport": "Football", "role": "Captain"}
    ),
    (
        ["main.py", "match", "--grit", "8", "--teamwork", "9"],
        "match",
        {"grit": 8, "teamwork": 9}
    ),
    (
        ["main.py", "employers", "--sport", "Swimming", "--role", "Starter"],
        "employers",
        {"sport": "Swimming", "role": "Starter"}
    ),
])
def test_main_dispatch_success(
    command_args: List[str],
    expected_handler: str,
    expected_attrs: Dict[str, Any],
    mocker: MockerFixture
) -> None:
    """Verify that main() dispatches to the correct handler with parsed arguments."""
    # Mock handlers
    mock_translate = mocker.patch("main.handle_translate")
    mock_match = mocker.patch("main.handle_match")
    mock_employers = mocker.patch("main.handle_employers")

    # Mock sys.argv
    mocker.patch("sys.argv", command_args)

    main()

    if expected_handler == "translate":
        mock_translate.assert_called_once()
        args = mock_translate.call_args[0][0]
        for attr, val in expected_attrs.items():
            assert getattr(args, attr) == val
        mock_match.assert_not_called()
        mock_employers.assert_not_called()

    elif expected_handler == "match":
        mock_match.assert_called_once()
        args = mock_match.call_args[0][0]
        for attr, val in expected_attrs.items():
            assert getattr(args, attr) == val
        mock_translate.assert_not_called()
        mock_employers.assert_not_called()

    elif expected_handler == "employers":
        mock_employers.assert_called_once()
        args = mock_employers.call_args[0][0]
        for attr, val in expected_attrs.items():
            assert getattr(args, attr) == val
        mock_translate.assert_not_called()
        mock_match.assert_not_called()


def test_main_version(mocker: MockerFixture, capsys: pytest.CaptureFixture) -> None:
    """Verify --version flag outputs the version string."""
    mocker.patch("sys.argv", ["main.py", "--version"])

    with pytest.raises(SystemExit) as excinfo:
        main()

    assert excinfo.value.code == 0
    captured = capsys.readouterr()
    assert "0.1.0-mvp" in captured.out


def test_main_no_command(mocker: MockerFixture, capsys: pytest.CaptureFixture) -> None:
    """Verify that calling main without arguments prints help."""
    mocker.patch("sys.argv", ["main.py"])

    # Mock handlers to ensure none are called
    mock_translate = mocker.patch("main.handle_translate")
    mock_match = mocker.patch("main.handle_match")
    mock_employers = mocker.patch("main.handle_employers")

    main()

    captured = capsys.readouterr()
    assert "usage:" in captured.out or "usage:" in captured.err

    mock_translate.assert_not_called()
    mock_match.assert_not_called()
    mock_employers.assert_not_called()


def test_main_invalid_command(mocker: MockerFixture, capsys: pytest.CaptureFixture) -> None:
    """Verify that an invalid command triggers usage error."""
    mocker.patch("sys.argv", ["main.py", "invalid_command"])

    with pytest.raises(SystemExit) as excinfo:
        main()

    assert excinfo.value.code != 0
    captured = capsys.readouterr()
    assert "usage:" in captured.err or "error:" in captured.err

def test_handle_translate(mocker: MockerFixture, capsys: pytest.CaptureFixture) -> None:
    """Verify handle_translate calls service and prints correct output."""
    # Mock the service
    mock_translate_skills = mocker.patch("main.translate_skills")
    mock_translate_skills.return_value = {
        "Leadership": "Strategic Direction",
        "Teamwork": "Collaborative Synergy"
    }

    # Mock arguments
    args = argparse.Namespace(sport="Football", role="Captain")

    # Call the handler
    handle_translate(args)

    # Verify service call
    mock_translate_skills.assert_called_once()
    call_args = mock_translate_skills.call_args[0][0]
    assert isinstance(call_args, AthleteProfile)
    assert call_args.sport == "Football"
    assert call_args.role == "Captain"

    # Verify output
    captured = capsys.readouterr()
    assert "--- Resume Translation for Football Captain ---" in captured.out
    assert 'Athletic Context: "Leadership"' in captured.out
    assert 'Resume Bullet:    "Strategic Direction"' in captured.out
    assert 'Athletic Context: "Teamwork"' in captured.out
    assert 'Resume Bullet:    "Collaborative Synergy"' in captured.out

def test_handle_match(mocker: MockerFixture, capsys: pytest.CaptureFixture) -> None:
    """Verify handle_match calls service and prints correct output."""
    # Mock the service
    mock_match_careers = mocker.patch("main.match_careers")
    mock_match_careers.return_value = [
        Job(title="Project Manager"),
        Job(title="Sales Representative")
    ]

    # Mock arguments
    args = argparse.Namespace(grit=8, teamwork=9)

    # Call the handler
    handle_match(args)

    # Verify service call
    mock_match_careers.assert_called_once_with(8, 9)

    # Verify output
    captured = capsys.readouterr()
    assert "--- Career Matches (Grit: 8, Teamwork: 9) ---" in captured.out
    assert "- Project Manager" in captured.out
    assert "- Sales Representative" in captured.out
    assert "Structure is gone. But your discipline remains." in captured.out

@pytest.mark.parametrize("mock_matches, expected_output", [
    (
        [Employer(name="Tech Corp", industry="Technology", required_skills=["Coding"])],
        ["--- Employer Matches for Football Captain ---", "- Tech Corp (Technology)", "Required Skills: Coding", "Network is net worth."]
    ),
    (
        [],
        ["--- Employer Matches for Football Captain ---", "No direct matches found. Keep training.", "Network is net worth."]
    )
])
def test_handle_employers(
    mock_matches: List[Employer],
    expected_output: List[str],
    mocker: MockerFixture,
    capsys: pytest.CaptureFixture
) -> None:
    """Verify handle_employers output for both match and no-match scenarios."""
    # Mock the service
    mock_match_employers = mocker.patch("main.match_employers")
    mock_match_employers.return_value = mock_matches

    # Mock arguments
    args = argparse.Namespace(sport="Football", role="Captain")

    # Call the handler
    handle_employers(args)

    # Verify service call
    mock_match_employers.assert_called_once()
    call_args = mock_match_employers.call_args[0][0]
    assert isinstance(call_args, AthleteProfile)
    assert call_args.sport == "Football"
    assert call_args.role == "Captain"

    # Verify output
    captured = capsys.readouterr()
    for line in expected_output:
        assert line in captured.out
