# Implementation Plan - The 98% Platform

## Roadmap
1.  **Core Architecture Refactoring (Completed)**
    -   [x] Decouple data from logic in `src/core/app.py`.
    -   [x] Introduce Pydantic DTOs for type safety.
    -   [x] Extract hardcoded data into a data layer.

2.  **Skill Translation Engine Expansion (Completed)**
    -   [x] Support more sports and roles.
    -   [x] Implement advanced mapping logic (e.g. multi-factor mapping).

3.  **Employer Matching Enhancements**
    -   [x] Add "Employer" entity.
    -   [x] Implement matching based on specific requirements.

4.  **Profile Enrichment & Logic Unification**
    -   [x] Add `grit`, `teamwork`, and `gpa` fields to `AthleteProfile`.
    -   [x] Refactor `match_careers` to accept `AthleteProfile`.
    -   [x] Update `main.py` CLI to populate the full profile and pass it to services.

## Current Gap Analysis
-   **Model Completeness**: `AthleteProfile` lacks key attributes (grit, teamwork, GPA) needed for career matching.
-   **Service Consistency**: `translate_skills` operates on `AthleteProfile`, while `match_careers` operates on raw integers.
-   **Type Safety**: Runtime validation enabled via Pydantic.
