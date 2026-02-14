import argparse
from typing import List, Dict
import pytest
from pytest_mock import MockerFixture
from src.core.models import Employer, Job
from main import handle_employers, handle_translate, handle_match

@pytest.fixture
def mock_employer_args() -> argparse.Namespace:
    return argparse.Namespace(sport="Football", role="Captain")

@pytest.mark.parametrize("matches, expected_output_snippets", [
    (
        [],
        ["Employer Matches for Football Captain", "No direct matches found", "Keep training"]
    ),
    (
        [Employer(name="Tech Corp", industry="Tech", required_skills=["Coding"])],
        ["Employer Matches for Football Captain", "Tech Corp (Tech)", "Required Skills: Coding"]
    ),
    (
        [
            Employer(name="Tech Corp", industry="Tech", required_skills=["Coding"]),
            Employer(name="Biz Inc", industry="Business", required_skills=["Selling"])
        ],
        ["Tech Corp (Tech)", "Biz Inc (Business)", "Required Skills: Coding", "Required Skills: Selling"]
    )
])
def test_handle_employers(
    mock_employer_args: argparse.Namespace,
    matches: List[Employer],
    expected_output_snippets: List[str],
    mocker: MockerFixture,
    capsys: pytest.CaptureFixture[str]
) -> None:
    """Test handle_employers with various match scenarios."""
    # Arrange
    mocker.patch("main.match_employers", return_value=matches)

    # Act
    handle_employers(mock_employer_args)

    # Assert
    captured = capsys.readouterr()
    for snippet in expected_output_snippets:
        assert snippet in captured.out

@pytest.mark.parametrize("skills, expected_snippets", [
    ({}, ["Resume Translation for Tennis Player"]),
    ({"Run": "Execute"}, ["Athletic Context: \"Run\"", "Resume Bullet:    \"Execute\""])
])
def test_handle_translate(
    mocker: MockerFixture,
    capsys: pytest.CaptureFixture[str],
    skills: Dict[str, str],
    expected_snippets: List[str]
) -> None:
    """Test handle_translate with various skill sets."""
    args = argparse.Namespace(sport="Tennis", role="Player")
    mocker.patch("main.translate_skills", return_value=skills)

    handle_translate(args)

    captured = capsys.readouterr()
    for s in expected_snippets:
        assert s in captured.out

@pytest.mark.parametrize("jobs, expected_snippets", [
    ([], ["Career Matches (Grit: 8, Teamwork: 9)", "Structure is gone"]),
    ([Job(title="CEO")], ["- CEO"])
])
def test_handle_match(
    mocker: MockerFixture,
    capsys: pytest.CaptureFixture[str],
    jobs: List[Job],
    expected_snippets: List[str]
) -> None:
    """Test handle_match with various job lists."""
    args = argparse.Namespace(grit=8, teamwork=9)
    mocker.patch("main.match_careers", return_value=jobs)

    handle_match(args)

    captured = capsys.readouterr()
    for s in expected_snippets:
        assert s in captured.out
