"""
Unit tests for job enrichment.
"""
from src.core.services import match_careers
from src.core.data import HIGH_SCORE_THRESHOLD


def test_match_careers_returns_rich_data():
    """Test that jobs returned by match_careers have employer and skills populated."""
    # Using high scores to get all jobs
    jobs = match_careers(grit_score=HIGH_SCORE_THRESHOLD + 1, teamwork_score=HIGH_SCORE_THRESHOLD + 1)

    assert len(jobs) > 0, "Should return some jobs"

    for job in jobs:
        # Check employer is populated (not just default "General" if we updated it)
        # Note: Some base jobs might still be General if we didn't update them,
        # but in my plan I updated all of them to have specific employers.
        assert job.employer in ["TechCorp", "ConsultingGroup", "LogisticsInc"], \
            f"Job {job.title} has unexpected employer: {job.employer}"

        # Check required_skills is populated
        assert len(job.required_skills) > 0, \
            f"Job {job.title} should have required skills"

def test_match_careers_grit_filtering():
    """Test that grit filtering still works with new implementation."""
    # Low grit, Low teamwork -> Only base jobs
    jobs = match_careers(grit_score=0, teamwork_score=0)
    for job in jobs:
        assert job.min_grit == 0
        assert job.min_teamwork == 0

    # High grit, Low teamwork
    jobs_grit = match_careers(grit_score=HIGH_SCORE_THRESHOLD + 1, teamwork_score=0)
    # Should include grit jobs
    grit_job_titles = [j.title for j in jobs_grit if j.min_grit > 0]
    assert "Operations Manager (High Intensity)" in grit_job_titles
