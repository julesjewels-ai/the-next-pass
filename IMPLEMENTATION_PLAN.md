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

4.  **Intelligent Job Matching (Completed)**
    -   [x] **Enhance Job Model**: Add metadata (employer, skills, traits) to `Job` entity.
    -   [x] **Unified Matching Service**: Create `match_opportunities` to filter jobs by skills & traits.
    -   [x] **CLI Integration**: Expose `opportunities` command.

5.  **Deep Integration (Phase 3)**
    -   [ ] **Enforce Employer Baseline Requirements**: Ensure job matches also satisfy the parent employer's baseline skill requirements.

## Current Gap Analysis
-   **Employer Constraints**: Currently, `match_opportunities` checks job-specific skills but ignores the employer's baseline requirements. For example, TechCorp requires "Leadership" for *all* roles, but a "Sales Development Representative" job there only lists "Strategic Analysis". A candidate with "Strategic Analysis" but no "Leadership" is currently matched, which is incorrect.
