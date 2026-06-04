# Sprint 2.6 — Local Stabilization Patch Report

This patch stabilizes local configurations, seeds needed test data, and ensures exact data mapping alignments for One Spirit imports.

## Key Changes Included

1. **Docker Environment Variables**:
   - Environment flags `ENV` and `AUTO_CREATE_TABLES` are now explicitly propagated to the backend service block in `docker-compose.yml`.
   
2. **Vite Dynamic Proxy Targets**:
   - `vite.config.js` is updated to load `VITE_PROXY_TARGET` from process environments (which is set to `http://backend:8000` under Docker Compose) and defaults to `http://localhost:8000` for local host development.
   
3. **Expanded Payment Mapping**:
   - `map_payment_status` now translates variations of outstanding strings (`out standing`, `out-standing`, `outstanding payment`, `out standing payment`) to `Outstanding`.
   
4. **Seed User Initials**:
   - User seeding logic triggers database insertion of 14 placeholder internal staff users corresponding to initials used in the Excel worksheet (`JIP`, `OME`, etc.).

---

## Migration Architecture Notice

> [!IMPORTANT]
> **Alembic Database Schema Migration Dependencies**:
> - Alembic migrations currently assume an existing baseline structure or the use of `Base.metadata.create_all` for local development.
> - A full database baseline migration snapshot revision MUST be generated and tested prior to staging or production deployment.
> - For now, local development environments remain fully supported by running with `AUTO_CREATE_TABLES=true`.

---

## Excel Import QA Recalibration
Run execution dry-runs verify exact data counts on `Project Workflow OS 2025.xlsx`:

- **Total processed records**: 263 (1 skipped empty row)
- **Quotation Cancel count**: 141
- **Signed & Deal count**: 122
- **Paid count**: 103
- **Outstanding count**: 12 (correctly mapped from outstanding variations)
- **Invoice Sent count**: 1
- **Warnings count**: Reduced from 961 warnings to 153 warnings (unmapped PO/PM warnings are completely eliminated!).
