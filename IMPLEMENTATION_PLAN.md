# Implementation Plan - The 98% Platform

## Roadmap
1.  **Core Architecture Refactoring (Completed)**
    -   [x] Decouple data from logic in `src/core/app.py`.
    -   [x] Introduce Pydantic DTOs for type safety.
    -   [x] Extract hardcoded data into a data layer.

2.  **Skill Translation Engine Expansion (Current)**
    -   [x] Support more sports and roles.
    -   [x] Implement advanced mapping logic (e.g. multi-factor mapping).

3.  **Employer Matching Enhancements**
    -   [ ] Add "Employer" entity.
    -   [ ] Implement matching based on specific requirements.

## Current Gap Analysis
-   **Type Safety**: Runtime validation enabled via Pydantic.
-   **Testing**: Coverage for new sports and roles added.
