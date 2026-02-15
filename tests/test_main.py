import argparse
import pytest
from pytest_mock import MockerFixture
from src.core.models import Employer
from main import handle_employers

@pytest.mark.parametrize("sport, role, mock_matches, expected_output_parts", [
    (
        "Football",
        "Captain",
        [
            Employer(
                name="TechCorp",
                industry="Software",
                required_skills=["Leadership", "Strategy"]
            )
        ],
        [
            "--- Employer Matches for Football Captain ---",
            "- TechCorp (Software)",
            "Required Skills: Leadership, Strategy",
            "Network is net worth."
        ]
    ),
    (
        "Swimming",
        "Swimmer",
        [],
        [
            "--- Employer Matches for Swimming Swimmer ---",
            "No direct matches found. Keep training.",
            "Network is net worth."
        ]
    ),
    (
        "",
        "",
        [
            Employer(
                name="LogisticsInc",
                industry="Supply Chain",
                required_skills=["Planning"]
            )
        ],
        [
            "--- Employer Matches for   ---",
            "- LogisticsInc (Supply Chain)",
            "Required Skills: Planning",
            "Network is net worth."
        ]
    ),
    (
        "General",
        "Athlete",
        [
            Employer(
                name="ConsultingGroup",
                industry="Consulting",
                required_skills=["Analysis"]
            ),
            Employer(
                name="BankCo",
                industry="Finance",
                required_skills=["Risk"]
            )
        ],
        [
            "--- Employer Matches for General Athlete ---",
            "- ConsultingGroup (Consulting)",
            "Required Skills: Analysis",
            "- BankCo (Finance)",
            "Required Skills: Risk",
            "Network is net worth."
        ]
    )
])
def test_handle_employers(
    sport: str,
    role: str,
    mock_matches: list[Employer],
    expected_output_parts: list[str],
    mocker: MockerFixture,
    capsys: pytest.CaptureFixture[str]
) -> None:
    # Arrange
    args = argparse.Namespace(sport=sport, role=role)
    mock_match_employers = mocker.patch("main.match_employers", return_value=mock_matches)

    # Act
    handle_employers(args)

    # Assert
    captured = capsys.readouterr()
    output_lines = [line.strip() for line in captured.out.splitlines() if line.strip()]

    # Verify mock was called
    mock_match_employers.assert_called_once()
    called_profile = mock_match_employers.call_args[0][0]
    assert called_profile.sport == sport
    assert called_profile.role == role

    # Verify output contains all expected parts
    # We check if each expected part is present as a substring in at least one line of the output
    for part in expected_output_parts:
        assert any(part in line for line in output_lines), \
            f"Expected part '{part}' not found in output: {output_lines}"
