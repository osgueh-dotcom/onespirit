# Repository Map

## Stack

- Backend: FastAPI, SQLAlchemy, Pydantic, Alembic, PostgreSQL, pytest.
- Frontend: Vue 3, Pinia, Vue Router, Axios, Tailwind, Vite, Vitest.
- Local test database: SQLite.
- Integrated local runtime: Docker Compose.

## Key Paths

- `backend/app/main.py`: app lifecycle, middleware, router registration.
- `backend/app/core/`: configuration, database, security, dependencies.
- `backend/app/modules/`: domain modules using router/service/schema/model files.
- `backend/alembic/versions/`: durable schema migrations.
- `backend/app/tests/`: backend regression tests.
- `frontend/src/router/index.js`: route and UI access metadata.
- `frontend/src/utils/access.js`: shared frontend access helpers.
- `frontend/src/views/`: workflow screens.
- `frontend/src/components/`: shared and domain UI.
- `frontend/src/store/`: Pinia stores and API-facing state.
- `docs/`: focused operational, security, deployment, and historical documents.

## Current Hotspots

Large views require careful scoped edits:

- `frontend/src/views/ProjectDetail.vue`
- `frontend/src/views/Projects.vue`
- `frontend/src/views/PmControlCenter.vue`
- `frontend/src/views/SourceVendorPerformance.vue`
- `frontend/src/views/PoControlCenter.vue`
- `frontend/src/views/Finance.vue`

Extract only cohesive behavior. Do not refactor a large view merely because it
is large.
