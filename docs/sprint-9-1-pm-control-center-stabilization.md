# Sprint 9.1 — PM Control Center Stabilization Patch

## Objective
This stabilization patch fixes a series of minor stability, usability, and correctness issues identified in the PM Control Center (Operational Dashboard) prior to the launch of Sprint 10 features.

## Changes & Fixes

### 1. Vue Import Correction
- **File**: [PmControlCenter.vue](file:///e:/GVsys%20Project/One%20Spirit/frontend/src/views/PmControlCenter.vue)
- **Fix**: Added missing `computed` utility import from the `'vue'` module, resolving runtime errors during compilation and rendering.

### 2. Readiness Score Scale Correction
- **File**: [PmControlCenter.vue](file:///e:/GVsys%20Project/One%20Spirit/frontend/src/views/PmControlCenter.vue)
- **Fix**: Adjusted `getReadinessScoreBadgeStyles(score)` to evaluate thresholds on a raw `0–100` percentage scale (`>= 80` for green/emerald, `>= 50` for yellow, `< 50` for red) rather than comparing against decimal values (`0.8` / `0.5`). 
- Passed raw readiness score values directly to the badge styling helper rather than dividing them by 100.

### 3. Priority Action Title Fallback
- **File**: [operational_service.py](file:///e:/GVsys%20Project/One%20Spirit/backend/app/modules/dashboard/operational_service.py)
- **Fix**: Replaced the direct reference to `p.title` on the recommended priority action builder with a safe chain of fallbacks: `p.title or p.program_name or p.project_code or "Untitled Project"`. This prevents pydantic model schema validation exceptions if a project has a null title.

### 4. Database-first PM Initial Code
- **File**: [operational_service.py](file:///e:/GVsys%20Project/One%20Spirit/backend/app/modules/dashboard/operational_service.py)
- **Fix**: Updated PM workload aggregation to check for and prioritize `pm.initial_code` fetched directly from the database user record, fallback to email prefix parsing ONLY if the database value is null.

### 5. Advanced Frontend Filters
- **File**: [PmControlCenter.vue](file:///e:/GVsys%20Project/One%20Spirit/frontend/src/views/PmControlCenter.vue)
- **Improvement**: Added advanced filter options inside the dashboard filters bar:
  - **Readiness Min (%)**
  - **Readiness Max (%)**
  - **Status Instrumen** (select dropdown with options: Not Started, In Progress, Need Revision, Done, Not Required)
- These values bind to `readiness_min`, `readiness_max`, and `instrument_status` query parameters sent to the backend `/pm-control-center` API.

### 6. Empty State & NaN Safety Checks
- **File**: [PmControlCenter.vue](file:///e:/GVsys%20Project/One%20Spirit/frontend/src/views/PmControlCenter.vue)
- **Fix**: Applied null/undefined guards (`val || 0`) inside template `Math.round()` calculations, ensuring the dashboard never shows `NaN` values when data load is in progress or when metrics are missing.

---

## Verification & Testing

### Backend Unit Tests
Run backend tests to verify endpoints and business calculations remain functional:
```bash
docker exec onespirit_backend pytest
```

### Production Build Test
Verify that the frontend builds and compiles cleanly without compile-time warnings:
```bash
docker exec onespirit_frontend npm run build
```

### Manual Verification
1. Access `/pm-control-center`.
2. Inspect the **Beban Kerja PM** tab: verify PM initials match their database `initial_code` (e.g. `POT`, `PMT`) and the average readiness badge color scale displays correctly based on percentage values.
3. Test filters: Set readiness thresholds and verify projects filter dynamically.
4. Try filtering by instrument status and check dashboard updates.
5. Verify priority actions display safe fallbacks when project titles are empty.
