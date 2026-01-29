# Implementation Plan - The 98% Platform

## Gap Analysis
Comparing the `README.md` stated features against the current codebase (`src/core/app.py`, `main.py`).

| Feature Category | Feature | Status | Notes |
|------------------|---------|--------|-------|
| **Athlete** | Free platform access | ✅ Implemented | Basic CLI access |
| **Athlete** | AI-driven skill assessment | ❌ Missing | Currently static dictionary mapping |
| **Athlete** | Skill translation | ⚠️ Partial | Hardcoded, limited database |
| **Athlete** | Personalized career plans | ❌ Missing | Basic list of jobs only |
| **Athlete** | Financial guidance | ❌ Missing | No logic implemented |
| **Employer** | Access to elite talent pool | ❌ Missing | No employer interface |
| **Employer** | Candidate discovery | ❌ Missing | No search functionality |
| **Employer** | Dashboard | ❌ Missing | No dashboard |
| **Athletic Dept**| White-label platform | ❌ Missing | No multi-tenant/branding support |
| **Core** | Performance data analysis | ❌ Missing | No analytics engine |

## Prioritized Task List

### Phase 1: Core Athlete Features (MVP Expansion)
1. **Implement Financial Guidance**
   - **Goal**: Add value to the "Free" tier.
   - **Scope**: New CLI command `guide` that takes financial inputs and returns a basic plan.
   - **Architecture**: New `src/core/financial.py` module with `FinancialProfile` DTO and service logic.
   - **Status**: Ready to Start.

2. **Enhance Skill Translation (AI/Scalable)**
   - **Goal**: Move away from hardcoded dictionaries.
   - **Scope**: Load skills from a JSON/YAML database or integrate a simple NLP model (or mock it).
   - **Architecture**: Repository pattern for SkillDB.
   - **Status**: Pending.

### Phase 2: Employer Features
3. **Employer Dashboard CLI**
   - **Goal**: Allow employers to view "matches".
   - **Scope**: Mock database of athletes, command to query them.
   - **Status**: Pending.

## Architecture & Security (SCP)
- **Input Validation**: All CLI inputs must be typed and validated.
- **Complexity**: Keep functions < 30 lines.
- **Dependency Injection**: Use DTOs for data transfer.
