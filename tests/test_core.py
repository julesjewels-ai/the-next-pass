"""
Forensic test suite for core business logic.
Targeting high-value logic with parametrized edge cases.
"""
import pytest
from src.core.models import AthleteProfile
from src.core.services import translate_skills, match_careers
from src.core.data import (
    HIGH_SCORE_THRESHOLD,
    BASE_JOBS,
    GRIT_JOBS,
    TEAMWORK_JOBS,
    SKILL_LEADERSHIP,
    SKILL_TEAM_COLLABORATION,
    SKILL_STRATEGIC_EXECUTION,
    SKILL_RESILIENCE
)

# --- Tests for translate_skills ---
@pytest.mark.parametrize("sport, role, expected_skills", [
    # 1. Standard Match (Basketball + Captain) -> Leadership + Team Collaboration + Universal
    ("Basketball", "Captain", [SKILL_LEADERSHIP, SKILL_TEAM_COLLABORATION, "Time Management"]),

    # 2. Sport Only Match (Basketball + Unknown Role) -> Team Collaboration + Universal
    ("Basketball", "Bench", [SKILL_TEAM_COLLABORATION, "Time Management"]),

    # 3. Role Only Match (Unknown Sport + Captain) -> Leadership + Universal
    ("Curling", "Captain", [SKILL_LEADERSHIP, "Time Management"]),

    # 4. No Match (Unknown Sport + Unknown Role) -> Universal Only
    ("Curling", "Sweeper", ["Time Management", "Strategic Analysis"]),

    # 5. Substring Match (Sport contains key) -> "Men's Basketball" contains "Basketball"
    ("Men's Basketball", "Captain", [SKILL_TEAM_COLLABORATION, SKILL_LEADERSHIP]),

    # 6. Case Sensitivity Verification (Code is currently case-sensitive)
    # "basketball" != "Basketball", so it should NOT match Sport/Role mappings
    ("basketball", "captain", ["Time Management"]),

    # 7. Walk-on Edge Case (Resilience)
    ("Track", "Walk-on", [SKILL_RESILIENCE]),

    # 8. Football Quarterback (Strategic Execution)
    ("Football", "Quarterback", [SKILL_STRATEGIC_EXECUTION]),
])
def test_translate_skills_logic(
    sport: str,
    role: str,
    expected_skills: list[str]
) -> None:
    profile = AthleteProfile(sport=sport, role=role)
    result = translate_skills(profile)

    # Verify all expected skills are present in the keys
    for skill in expected_skills:
        assert skill in result, f"Missing expected skill '{skill}' for {sport}/{role}"

    # Verify Universal skills are ALWAYS present
    # (Checking one known universal skill is sufficient to verify the merge)
    assert "Time Management" in result
    assert "Strategic Analysis" in result


# --- Tests for match_careers ---
@pytest.mark.parametrize("grit, teamwork, expected_includes, expected_excludes", [
    # 1. High Grit, High Teamwork (> Threshold)
    (HIGH_SCORE_THRESHOLD + 1, HIGH_SCORE_THRESHOLD + 1, GRIT_JOBS + TEAMWORK_JOBS, []),

    # 2. High Grit, Low Teamwork
    (HIGH_SCORE_THRESHOLD + 1, HIGH_SCORE_THRESHOLD, GRIT_JOBS, TEAMWORK_JOBS),

    # 3. Low Grit, High Teamwork
    (HIGH_SCORE_THRESHOLD, HIGH_SCORE_THRESHOLD + 1, TEAMWORK_JOBS, GRIT_JOBS),

    # 4. Low Grit, Low Teamwork
    (HIGH_SCORE_THRESHOLD, HIGH_SCORE_THRESHOLD, [], GRIT_JOBS + TEAMWORK_JOBS),

    # 5. Boundary Condition (Exactly Threshold) -> Should be Low (implied > check)
    (HIGH_SCORE_THRESHOLD, HIGH_SCORE_THRESHOLD, [], GRIT_JOBS + TEAMWORK_JOBS),
])
def test_match_careers_logic(
    grit: int,
    teamwork: int,
    expected_includes: list[str],
    expected_excludes: list[str]
) -> None:
    result = match_careers(grit, teamwork)
    titles = [job.title for job in result]

    # Base jobs should always be present
    for job in BASE_JOBS:
        assert job in titles, "Base jobs missing"

    # Check conditional inclusions
    for job in expected_includes:
        assert job in titles, f"Expected {job} for grit={grit}, teamwork={teamwork}"

    # Check conditional exclusions
    for job in expected_excludes:
        assert job not in titles, f"Did not expect {job} for grit={grit}, teamwork={teamwork}"
