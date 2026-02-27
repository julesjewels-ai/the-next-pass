# Implementation Plan - The 98% Platform

## Roadmap
1.  **Core Architecture Refactoring (Completed)**
    -   [x] Decouple data from logic in `src/core/app.py`.
    -   [x] Introduce Pydantic DTOs for type safety.
    -   [x] Extract hardcoded data into a data layer.

2.  **Skill Translation Engine Expansion (Completed)**
    -   [x] Support more sports and roles.
    -   [x] Implement advanced mapping logic (e.g. multi-factor mapping).

3.  **Employer Matching Enhancements (Completed)**
    -   [x] Add "Employer" entity.
    -   [x] Implement matching based on specific requirements.

4.  **Intelligent Job Matching (Phase 2)**
    -   [x] **Enhance Job Model**: Add metadata (employer, skills, traits) to `Job` entity.
    -   [ ] **Unified Matching Service**: Enhance `match_opportunities` to filter jobs by both job-specific skills and the employer's required skills.
    -   [x] **CLI Integration**: Expose `opportunities` command.

## Current Gap Analysis
-   **Matching Logic**: `match_opportunities` currently only checks for the skills explicitly listed on the `Job` object. It needs to also enforce that the candidate possesses all the `required_skills` of the `Employer` associated with the job.
-   **Data Access**: We need an `EMPLOYERS_INDEX` in the data layer to quickly look up `Employer` objects by name during the matching process.
