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
    -   [x] **Unified Matching Service**: Create `match_opportunities` to filter jobs by skills & traits.
    -   [x] **CLI Integration**: Expose `opportunities` command.

5.  **Analytics and Reporting (Phase 3)**
    -   [x] **Skill Demand Analytics**: Build a service to aggregate the frequency of required skills across all jobs to help athletes understand market demand. (Completed)

6.  **Financial Guidance (Phase 4)**
    -   [ ] **Compensation Estimator**: Build a service to format compensation strings with base salary and signing bonus using thousands separators.

## Current Gap Analysis
-   Phase 3 is complete. Moving on to Phase 4: Financial Guidance. The current highest priority task is to implement the "Compensation Estimator".
