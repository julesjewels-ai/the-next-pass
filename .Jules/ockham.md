# Ockham's Journal

## 2024-05-21 - Initial Audit
**Observation:** `src/core/app.py` contains hardcoded strings and magic numbers within methods (`match_careers`, `translate_skills`).
**Action:** Extract constants for job titles and skill mappings to improve readability and testability.
