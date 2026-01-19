# Ockham's Journal

## 2024-05-21 - Initial Audit
**Observation:** `src/core/app.py` contains hardcoded strings and magic numbers within methods (`match_careers`, `translate_skills`).
**Action:** Extract constants for job titles and skill mappings to improve readability and testability.

## 2024-05-22 - Magic String Removal
**Observation:** `UNIVERSAL_SKILLS` in `src/core/app.py` used raw strings for "Time Management" and "Strategic Analysis".
**Action:** Extracted `SKILL_TIME_MANAGEMENT` and `SKILL_STRATEGIC_ANALYSIS` constants to centralize domain terminology.

## 2024-05-24 - CLI Dispatch Refactor
**Observation:** `main.py` contained a growing `if/elif/else` block for command handling, mixing argument parsing with presentation logic.
**Action:** Refactored to use a table-driven `command_handlers` dictionary and extracted `handle_translate` and `handle_match` functions to isolate responsibilities.
