"""
Tests for the data layer of The 98% Platform.
"""
from src.core.models import Job
from src.core.data import JOBS_DB, BASE_JOBS, GRIT_JOBS, TEAMWORK_JOBS

def test_jobs_db_exists():
    """Verify that JOBS_DB is defined and is a list."""
    assert isinstance(JOBS_DB, list)
    assert len(JOBS_DB) > 0

def test_jobs_db_content():
    """Verify that JOBS_DB contains valid Job objects."""
    for job in JOBS_DB:
        assert isinstance(job, Job)
        assert job.title
        assert job.employer
        assert isinstance(job.required_skills, list)
        assert job.min_grit >= 0
        assert job.min_teamwork >= 0

def test_jobs_db_covers_existing_lists():
    """Verify that JOBS_DB covers titles in legacy lists (for now)."""
    db_titles = {job.title for job in JOBS_DB}
    all_legacy_titles = set(BASE_JOBS + GRIT_JOBS + TEAMWORK_JOBS)

    # Check coverage or at least ensure critical ones are present
    for title in all_legacy_titles:
        assert title in db_titles, f"Missing job title in DB: {title}"
