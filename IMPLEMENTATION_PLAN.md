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
    -   [ ] **Unified Matching Service**: Create `match_opportunities` to filter jobs by skills & traits.
    -   [ ] **CLI Integration**: Expose `opportunities` command.

## Current Gap Analysis
-   **Unified Matching**: While `match_careers` uses rich data now, it only filters by soft skills (Grit/Teamwork). A new service `match_opportunities` is needed to filter by `required_skills` as well.
-   **CLI**: Need a command to expose the unified matching.
