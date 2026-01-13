# Ockham's Journal

## 2025-02-24 - Magic Strings and Implicit Mappings
**Observation:** In `src/core/app.py`, `translate_skills` relies on magic string keys ("5am Workouts", "Film Study") to map to `SKILL_DB`. The relationship between the "Corporate Skill" (e.g., "Time Management") and the "Athletic Context" (e.g., "5am Workouts") is hardcoded in the function logic.
**Action:** Extract these mappings into a constant structure `UNIVERSAL_SKILLS` to separate data from logic. This reduces cognitive load when reading the function and makes it easier to add new universal skills.
