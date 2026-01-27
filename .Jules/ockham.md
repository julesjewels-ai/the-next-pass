# Ockham's Journal

## 2024-05-21 - Initial Audit
**Observation:** `src/core/app.py` contains hardcoded strings and magic numbers within methods (`match_careers`, `translate_skills`).
**Action:** Extract constants for job titles and skill mappings to improve readability and testability.

## 2024-05-22 - Magic String Removal
**Observation:** `UNIVERSAL_SKILLS` in `src/core/app.py` used raw strings for "Time Management" and "Strategic Analysis".
**Action:** Extracted `SKILL_TIME_MANAGEMENT` and `SKILL_STRATEGIC_ANALYSIS` constants to centralize domain terminology.

## 2024-05-24 - CLI Control Flow Simplification
**Observation:** `main.py` used nested `if/elif` statements for command routing, increasing cognitive load and hindering extensibility.
**Action:** Refactored into `command_handlers` dictionary with isolated functions `handle_translate` and `handle_match` (Table-Driven Method).

## 2024-05-25 - Kingdom of Nouns Removal
**Observation:** `CareerPlatform` in `src/core/app.py` was a stateless class acting only as a namespace for functions, adding unnecessary boilerplate and instantiation.
**Action:** Refactored methods into top-level functions `translate_skills` and `match_careers`, removing the class entirely.
