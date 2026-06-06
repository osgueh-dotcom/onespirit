# Sprint 7.1 — Instruments Readiness Stabilization Patch

## Objective
Sprint 7.1 provides a stabilization patch to ensure that the project readiness calculations, dashboard analytics summaries, and empty-state representations are safe from mathematical errors (division by zero, `NaN`, `Infinity` rendering) and that security reminders are decoupled from operational readiness penalties.

---

## Bugs Fixed & Improvements

### 1. Dashboard Division by Zero & Empty Filters
- **Problem**: When dashboard filters matched zero active projects (e.g. searching for a future year or an inactive program manager), calculations dividing by `total_projects` could crash or result in mathematical errors.
- **Fix**: Verified all ratios and averages in `backend/app/modules/dashboard/service.py` to ensure they are fully guarded. The instrument summary calculation:
  ```python
  average_instrument_completion_rate = (
      (total_instrument_completion_rate_sum / total_projects * 100.0) 
      if total_projects > 0 else 0.0
  )
  ```
  safely handles the `total_projects == 0` boundary state. All other division operations (e.g., deal rate, cancel rate, average budget) use similar safeguards.
- **Verification**: Added `test_analytics_calculations` assertion verifying that filtering dashboard analytics to a non-existent year (e.g., `year=2099`) returns a safe `200 OK` response with `0.0` values.

### 2. Decoupled PNL Security Note from Readiness Score
- **Problem**: The system-wide warning note *"PNL access warning: PNL document is sensitive and should be restricted to Management/Finance/Admin in production."* was appended to all projects containing a PNL instrument. This warning lowered the project's operational readiness score by `20%` even though it is a security notice, not an operational failure.
- **Fix**: Adjusted `calculate_project_readiness(project)` in `backend/app/modules/projects/service.py` to filter out warnings containing `"PNL access warning"` when computing the `status_consistency_score`:
  ```python
  warnings = check_project_validation_warnings(project)
  operational_warnings = [w for w in warnings if "PNL access warning" not in w]
  status_consistency_score = max(0.0, 1.0 - 0.2 * len(operational_warnings))
  ```
- **Verification**: Decoupled warnings still display in the UI list for administrative reference but do not reduce the readiness score. A test `test_sprint_7_1_readiness_safeguards` asserts that the project score remains `0.2` instead of dropping to `0.16` in the presence of this warning.

### 3. Frontend Empty-State and NaN Safeguards
- **Problem**: In Vue components, displaying `NaN` or crashing when checking properties of uninitialized or empty lists was a potential risk.
- **Fixes**:
  - **`ProjectInstrumentsPanel.vue`**: Safeguarded all computed metrics (`totalRequired`, `doneCount`, `needRevisionCount`, `overdueCount`) with `props.instruments || []` fallback check.
  - **`ProjectDetail.vue`**: Added safeguards (`!isNaN` and `!== null`) to metric formatting filters for `project.project_readiness_score` and `project.instrument_completion_rate`, falling back to `0%` if data is missing or loading.

---

## Verification Checklist

### Automated Tests
- Run all backend test cases (including instrument workflows and dashboard analytics):
  ```bash
  docker exec onespirit_backend pytest
  ```
  *Result: 13 passed, 0 failed.*

### Manual Verification Status
- [x] Dashboard with empty filters loaded without crashes.
- [x] PNL security note remains visible in the project validation list.
- [x] PNL security note does not decrease the project's readiness score.
- [x] Project Detail renders `0%` metrics instead of `NaN` when loading or empty.
- [x] All instruments marked "Not Required" or soft-deleted are calculated correctly.
- [x] Frontend compiled successfully with `npm run build`.

---

## Known Limitations
- Deleting default instruments is soft-deleted. The database maintains references for auditing, but the API filter safely ignores deleted rows.

---

## Next Sprint Recommendation
Implement Sprint 8: Role-based document access controls for all modules to graduate the PNL sensitivity foundation into a complete system-wide file access authorization layer.
