"""
Unit tests for the financial guidance functionality.
"""
from src.core.models import Job
from src.core.services import get_compensation_estimate

def test_get_compensation_estimate_with_both() -> None:
    job = Job(title="Test", employer="TestEmp", base_salary=90000, signing_bonus=10000)
    assert get_compensation_estimate(job) == "$90000 base + $10000 sign-on"

def test_get_compensation_estimate_with_base_only() -> None:
    job = Job(title="Test", employer="TestEmp", base_salary=80000, signing_bonus=0)
    assert get_compensation_estimate(job) == "$80000 base"

def test_get_compensation_estimate_with_none() -> None:
    job = Job(title="Test", employer="TestEmp", base_salary=0, signing_bonus=0)
    assert get_compensation_estimate(job) == "Compensation not specified"
