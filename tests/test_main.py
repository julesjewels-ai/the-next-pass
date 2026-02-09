import sys
import argparse
import pytest
from src.core.models import AthleteProfile, Job
import main

# Type hints for fixtures
from typing import Dict, List, Any, Optional
from pytest import CaptureFixture, MonkeyPatch
from pytest_mock import MockerFixture

@pytest.mark.parametrize("sport, role, expected_skills", [
    ("Football", "Quarterback", {"Leadership": "Team Management"}),
    ("Basketball", "Point Guard", {"Agility": "Adaptive Thinking"}),
    ("Swimming", "Captain", {"Discipline": "Self-Motivation"}),
    ("UnknownSport", "UnknownRole", {}),
])
def test_handle_translate(
    mocker: MockerFixture,
    capsys: CaptureFixture,
    sport: str,
    role: str,
    expected_skills: Dict[str, str]
) -> None:
    mock_translate = mocker.patch("main.translate_skills", return_value=expected_skills)
    args = argparse.Namespace(sport=sport, role=role)

    main.handle_translate(args)

    mock_translate.assert_called_once()
    call_args = mock_translate.call_args[0][0]
    assert isinstance(call_args, AthleteProfile)
    assert call_args.sport == sport
    assert call_args.role == role

    captured = capsys.readouterr()
    assert f"Resume Translation for {sport} {role}" in captured.out
    for raw, corpo in expected_skills.items():
        assert f"Athletic Context: \"{raw}\"" in captured.out
        assert f"Resume Bullet:    \"{corpo}\"" in captured.out


@pytest.mark.parametrize("grit, teamwork, expected_jobs", [
    (8, 9, [Job(title="Project Manager")]),
    (5, 5, [Job(title="Sales Rep")]),
    (10, 10, [Job(title="CEO"), Job(title="Founder")]),
    (0, 0, []),
])
def test_handle_match(
    mocker: MockerFixture,
    capsys: CaptureFixture,
    grit: int,
    teamwork: int,
    expected_jobs: List[Job]
) -> None:
    mock_match = mocker.patch("main.match_careers", return_value=expected_jobs)
    args = argparse.Namespace(grit=grit, teamwork=teamwork)

    main.handle_match(args)

    mock_match.assert_called_once_with(grit, teamwork)

    captured = capsys.readouterr()
    assert f"Career Matches (Grit: {grit}, Teamwork: {teamwork})" in captured.out
    for job in expected_jobs:
        assert f"- {job.title}" in captured.out
    assert "Structure is gone. But your discipline remains." in captured.out


@pytest.mark.parametrize("cli_args, expected_action, check_args", [
    (["prog", "translate", "--sport", "Football"], "call_translate", {"sport": "Football"}),
    (["prog", "match", "--grit", "8"], "call_match", {"grit": 8}),
    (["prog"], "print_help", None),
])
def test_main_dispatch(
    mocker: MockerFixture,
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture,
    cli_args: List[str],
    expected_action: str,
    check_args: Optional[Dict[str, Any]]
) -> None:
    monkeypatch.setattr(sys, "argv", cli_args)
    mock_translate = mocker.patch("main.handle_translate")
    mock_match = mocker.patch("main.handle_match")

    main.main()

    if expected_action == "call_translate":
        mock_translate.assert_called_once()
        if check_args:
            args = mock_translate.call_args[0][0]
            assert args.sport == check_args["sport"]
    elif expected_action == "call_match":
        mock_match.assert_called_once()
        if check_args:
            args = mock_match.call_args[0][0]
            assert args.grit == check_args["grit"]
    elif expected_action == "print_help":
        mock_translate.assert_not_called()
        mock_match.assert_not_called()
        captured = capsys.readouterr()
        # argparse prints to stdout or stderr
        assert "usage:" in captured.out or "usage:" in captured.err or "Available commands" in captured.out or "Available commands" in captured.err


def test_main_invalid_command(monkeypatch: MonkeyPatch, capsys: CaptureFixture) -> None:
    monkeypatch.setattr(sys, "argv", ["prog", "invalid"])
    with pytest.raises(SystemExit):
        main.main()
    captured = capsys.readouterr()
    assert "usage:" in captured.err or "usage:" in captured.out
