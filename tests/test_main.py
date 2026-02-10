"""
Tests for the CLI entry point (main.py).
"""
import pytest
import argparse
import sys
from src.core.models import AthleteProfile, Job, Employer
from main import handle_translate, handle_match, handle_employers, main

# Fixtures for mocked data and services

@pytest.fixture
def mock_services(mocker):
    """Mocks the service layer functions imported in main.py."""
    return {
        "translate_skills": mocker.patch("main.translate_skills"),
        "match_careers": mocker.patch("main.match_careers"),
        "match_employers": mocker.patch("main.match_employers"),
    }


# Tests for handle_translate

def test_handle_translate(mock_services, capsys):
    """Test the translate command handler."""
    # Arrange
    args = argparse.Namespace(sport="Football", role="Captain")
    mock_services["translate_skills"].return_value = {
        "Leadership": "Led team to victory",
        "Discipline": "Showed up on time"
    }

    # Act
    handle_translate(args)

    # Assert
    captured = capsys.readouterr()
    assert "--- Resume Translation for Football Captain ---" in captured.out
    assert "Athletic Context: \"Leadership\"" in captured.out
    assert "Resume Bullet:    \"Led team to victory\"" in captured.out

    mock_services["translate_skills"].assert_called_once()
    call_args = mock_services["translate_skills"].call_args[0][0]
    assert isinstance(call_args, AthleteProfile)
    assert call_args.sport == "Football"
    assert call_args.role == "Captain"


# Tests for handle_match

def test_handle_match(mock_services, capsys):
    """Test the match command handler."""
    # Arrange
    args = argparse.Namespace(grit=8, teamwork=9)
    mock_services["match_careers"].return_value = [
        Job(title="Project Manager"),
        Job(title="Sales Lead")
    ]

    # Act
    handle_match(args)

    # Assert
    captured = capsys.readouterr()
    assert "--- Career Matches (Grit: 8, Teamwork: 9) ---" in captured.out
    assert "- Project Manager" in captured.out
    assert "- Sales Lead" in captured.out
    assert "Structure is gone. But your discipline remains." in captured.out

    mock_services["match_careers"].assert_called_once_with(8, 9)


# Tests for handle_employers

def test_handle_employers_with_matches(mock_services, capsys):
    """Test the employers command handler with matches found."""
    # Arrange
    args = argparse.Namespace(sport="Tennis", role="Player")
    mock_services["match_employers"].return_value = [
        Employer(name="TechCorp", industry="Technology", required_skills=["Coding"]),
        Employer(name="BizInc", industry="Business", required_skills=["Excel"])
    ]

    # Act
    handle_employers(args)

    # Assert
    captured = capsys.readouterr()
    assert "--- Employer Matches for Tennis Player ---" in captured.out
    assert "- TechCorp (Technology)" in captured.out
    assert "  Required Skills: Coding" in captured.out
    assert "- BizInc (Business)" in captured.out

    mock_services["match_employers"].assert_called_once()
    call_args = mock_services["match_employers"].call_args[0][0]
    assert isinstance(call_args, AthleteProfile)
    assert call_args.sport == "Tennis"
    assert call_args.role == "Player"


def test_handle_employers_no_matches(mock_services, capsys):
    """Test the employers command handler when no matches are found."""
    # Arrange
    args = argparse.Namespace(sport="Chess", role="Grandmaster")
    mock_services["match_employers"].return_value = []

    # Act
    handle_employers(args)

    # Assert
    captured = capsys.readouterr()
    assert "--- Employer Matches for Chess Grandmaster ---" in captured.out
    assert "No direct matches found. Keep training." in captured.out
    assert "Network is net worth." in captured.out


# Tests for main function (Integration / Routing)

@pytest.mark.parametrize("command_args, expected_handler", [
    (["translate", "--sport", "Rugby", "--role", "Prop"], "handle_translate"),
    (["match", "--grit", "5", "--teamwork", "5"], "handle_match"),
    (["employers", "--sport", "Swimming", "--role", "Diver"], "handle_employers"),
])
def test_main_routing(mocker, command_args, expected_handler):
    """Test that main routes to the correct handler based on arguments."""
    # Arrange
    # We patch sys.argv. Note: sys.argv[0] is usually the script name.
    mocker.patch.object(sys, 'argv', ["main.py"] + command_args)

    # Mock the handlers to verify they are called.
    # We must patch them where they are USED (in main.py), or where they are defined.
    # In main.py, they are defined in the module scope.
    # So we patch 'main.handle_translate', etc.
    mock_handlers = {
        "handle_translate": mocker.patch("main.handle_translate"),
        "handle_match": mocker.patch("main.handle_match"),
        "handle_employers": mocker.patch("main.handle_employers"),
    }

    # Act
    main()

    # Assert
    mock_handlers[expected_handler].assert_called_once()

    # Verify other handlers were NOT called
    for name, mock in mock_handlers.items():
        if name != expected_handler:
            mock.assert_not_called()


def test_main_help_no_command(mocker, capsys):
    """Test that main prints help when no arguments are provided."""
    # Arrange
    mocker.patch.object(sys, 'argv', ["main.py"])

    # Act
    main()

    # Assert
    captured = capsys.readouterr()
    assert "usage:" in captured.out
    assert "Available commands" in captured.out

def test_main_version(mocker, capsys):
    """Test the version flag."""
    mocker.patch.object(sys, 'argv', ["main.py", "--version"])

    with pytest.raises(SystemExit):
        main()

    captured = capsys.readouterr()
    # Argparse usually prints version to stdout or stderr
    assert "0.1.0-mvp" in captured.out or "0.1.0-mvp" in captured.err
