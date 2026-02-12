import argparse
import sys
from typing import Dict, List, Any
from unittest.mock import MagicMock

import pytest
from pytest import CaptureFixture
from pytest_mock import MockerFixture

# Import the module under test
import main
from src.core.models import AthleteProfile, Job, Employer

# Type aliases for better readability
MockType = MagicMock


@pytest.fixture
def mock_services(mocker: MockerFixture) -> Dict[str, MockType]:
    """Mock the service functions used in main.py."""
    # We need to mock the functions where they are imported in main.py
    return {
        "translate_skills": mocker.patch("main.translate_skills"),
        "match_careers": mocker.patch("main.match_careers"),
        "match_employers": mocker.patch("main.match_employers"),
    }


@pytest.mark.parametrize(
    "sport, role, expected_skills",
    [
        (
            "Football",
            "Captain",
            {"Field Vision": "Strategic Analysis", "Huddle Call": "Team Leadership"},
        ),
        (
            "Swimming",
            "Swimmer",
            {"Lap Count": "Data Entry", "Breath Control": "Stress Management"},
        ),
    ],
)
def test_handle_translate(
    mock_services: Dict[str, MockType],
    capsys: CaptureFixture,
    sport: str,
    role: str,
    expected_skills: Dict[str, str],
) -> None:
    """Test the handle_translate function with various inputs."""
    args = argparse.Namespace(sport=sport, role=role)
    mock_services["translate_skills"].return_value = expected_skills

    main.handle_translate(args)

    mock_services["translate_skills"].assert_called_once()
    call_args = mock_services["translate_skills"].call_args[0][0]
    assert isinstance(call_args, AthleteProfile)
    assert call_args.sport == sport
    assert call_args.role == role

    captured = capsys.readouterr()
    assert f"Resume Translation for {sport} {role}" in captured.out
    for raw, corpo in expected_skills.items():
        assert f'Athletic Context: "{raw}"' in captured.out
        assert f'Resume Bullet:    "{corpo}"' in captured.out


@pytest.mark.parametrize(
    "grit, teamwork, expected_jobs",
    [
        (
            8,
            9,
            [
                Job(title="Sales Director"),
                Job(title="Ops Manager"),
            ],
        ),
        (
            2,
            3,
            [Job(title="Freelance Coder")],
        ),
    ],
)
def test_handle_match(
    mock_services: Dict[str, MockType],
    capsys: CaptureFixture,
    grit: int,
    teamwork: int,
    expected_jobs: List[Job],
) -> None:
    """Test the handle_match function with various inputs."""
    args = argparse.Namespace(grit=grit, teamwork=teamwork)
    mock_services["match_careers"].return_value = expected_jobs

    main.handle_match(args)

    mock_services["match_careers"].assert_called_once_with(grit, teamwork)

    captured = capsys.readouterr()
    assert f"Career Matches (Grit: {grit}, Teamwork: {teamwork})" in captured.out
    for job in expected_jobs:
        assert f"- {job.title}" in captured.out
    assert "Structure is gone. But your discipline remains." in captured.out


@pytest.mark.parametrize(
    "sport, role, expected_employers",
    [
        (
            "Tennis",
            "Player",
            [
                Employer(
                    name="Tech Corp",
                    industry="Technology",
                    required_skills=["Resilience"],
                )
            ],
        ),
        ("Curling", "Sweeper", []),
    ],
)
def test_handle_employers(
    mock_services: Dict[str, MockType],
    capsys: CaptureFixture,
    sport: str,
    role: str,
    expected_employers: List[Employer],
) -> None:
    """Test the handle_employers function with various inputs."""
    args = argparse.Namespace(sport=sport, role=role)
    mock_services["match_employers"].return_value = expected_employers

    main.handle_employers(args)

    mock_services["match_employers"].assert_called_once()
    call_args = mock_services["match_employers"].call_args[0][0]
    assert isinstance(call_args, AthleteProfile)
    assert call_args.sport == sport
    assert call_args.role == role

    captured = capsys.readouterr()
    assert f"Employer Matches for {sport} {role}" in captured.out

    if not expected_employers:
        assert "No direct matches found. Keep training." in captured.out
    else:
        for employer in expected_employers:
            assert f"- {employer.name} ({employer.industry})" in captured.out
            assert f"Required Skills: {', '.join(employer.required_skills)}" in captured.out


@pytest.mark.parametrize(
    "cli_args, expected_handler, expected_exit",
    [
        (
            ["main.py", "translate", "--sport", "Football", "--role", "Captain"],
            "handle_translate",
            None,
        ),
        (
            ["main.py", "match", "--grit", "5", "--teamwork", "5"],
            "handle_match",
            None,
        ),
        (
            ["main.py", "employers", "--sport", "Football"],
            "handle_employers",
            None,
        ),
        # Default args check
        (
            ["main.py", "translate", "--sport", "Football"],
            "handle_translate",
            None,
        ),
        # Missing required arg (should exit)
        (
            ["main.py", "translate"],
            None,
            SystemExit,
        ),
        # Invalid command (should exit)
        (
            ["main.py", "invalid"],
            None,
            SystemExit,
        ),
        # No args (should print help, but argparse behavior on no args depends.
        # Here it just falls through to print_help if 'command' is None or not found)
        # Wait, if no subparser is selected, 'command' attribute might be None.
        (
            ["main.py"],
            None,
            None,  # Our main() calls print_help() but doesn't exit explicitly
        ),
    ],
)
def test_main_integration(
    mocker: MockerFixture,
    capsys: CaptureFixture,
    cli_args: List[str],
    expected_handler: str | None,
    expected_exit: Any,
) -> None:
    """Test the main entry point with various CLI arguments."""
    # Mock sys.argv
    mocker.patch.object(sys, "argv", cli_args)

    # Mock the handlers
    handlers = {
        "handle_translate": mocker.patch("main.handle_translate"),
        "handle_match": mocker.patch("main.handle_match"),
        "handle_employers": mocker.patch("main.handle_employers"),
    }

    # Mock sys.exit to prevent test from exiting
    # But for SystemExit we want to catch it or let pytest handle it if we expect it.
    # If we expect SystemExit, we should use pytest.raises

    if expected_exit:
        with pytest.raises(expected_exit):
            main.main()
    else:
        main.main()

    if expected_handler:
        handlers[expected_handler].assert_called_once()
        # Verify other handlers were not called
        for name, mock_handler in handlers.items():
            if name != expected_handler:
                mock_handler.assert_not_called()
    else:
        # If no handler expected (e.g. invalid command or no args),
        # verify no handlers were called
        for mock_handler in handlers.values():
            mock_handler.assert_not_called()

        if not expected_exit:
            # If we didn't exit, we probably printed help
            captured = capsys.readouterr()
            assert "usage:" in captured.out or "usage:" in captured.err
