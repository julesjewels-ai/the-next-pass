# Implementation Plan - The 98% Platform

## Phase 1: MVP Enhancements (Current)
- [x] **Feature: Markdown Resume Export**
    - Create `ResumeGenerator` interface.
    - Implement `MarkdownResumeGenerator`.
    - Update CLI to add `--output` flag.
    - **Security:** Input validation for filenames (prevent directory traversal).
- [ ] **Feature: Expanded Skill Database**
    - Add at least 5 common sports and 3 roles per sport.

## Phase 2: User Experience
- [ ] **Feature: Interactive CLI Wizard**
    - Use `input()` to guide users who don't know the args.

## Phase 3: Architecture
- [ ] **Refactor: External Configuration**
    - Move hardcoded skills/jobs to a config file.
