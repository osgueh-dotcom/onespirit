# Sprint 0 Technical Modernization Report

This document reports on the completed tasks and modernization baseline established for the **One Spirit** Workflow system by GVSys. 

---

## 1. What Was Changed

### Backend Component
- **Dependency Upgrades**: Modernized all python packages in [requirements.txt](../backend/requirements.txt) to stable modern releases:
  - `fastapi` $\ge$ `0.111.0` (from `0.100.0`)
  - `uvicorn[standard]` $\ge$ `0.30.1` (from `0.22.0`)
  - `sqlalchemy` $\ge$ `2.0.31` (from `2.0.0`)
  - `psycopg2-binary` $\ge$ `2.9.9` (from `2.9.6`)
  - `alembic` $\ge$ `1.13.2` (from `1.11.0`)
  - `pydantic-settings` $\ge$ `2.3.4` (from `2.0.0`)
  - `python-multipart` $\ge$ `0.0.9` (from `0.0.6`)
  - `pytest` $\ge$ `8.2.2` (from `7.3.0`)
  - `httpx` $\ge$ `0.27.0` (from `0.24.0`)
  - `email-validator` $\ge$ `2.2.0` (from `2.0.0`)
  - `openpyxl` $\ge$ `3.1.5` (from `3.1.0`)
  - `bcrypt` $\ge$ `4.1.3` (from `4.0.1`)
- **Health Check Endpoint**: Added a new `/health` GET endpoint in [main.py](../backend/app/main.py) which returns the current service status and identifier:
  ```json
  {
    "status": "ok",
    "service": "onespirit-backend"
  }
  ```

### Frontend Component
- **Package Updates**: Modernized [package.json](../frontend/package.json) dependencies to stable newer versions:
  - `vue` $\ge$ `^3.4.27`
  - `vite` $\ge$ `^5.2.11` (upgraded from Vite 4 to Vite 5)
  - `pinia` $\ge$ `^2.1.7`
  - `vue-router` $\ge$ `^4.3.2`
  - `axios` $\ge$ `^1.7.2`
  - `@heroicons/vue` $\ge$ `^2.1.3`
  - `@vitejs/plugin-vue` $\ge$ `^5.0.4`
  - `postcss` $\ge$ `^8.4.38`
  - `autoprefixer` $\ge$ `^10.4.19`

### Docker & Infrastructure Component
- **Database Port Conflict Mitigation**: Mapped PostgreSQL host-exposed port from `5432` to the configurable `DB_PORT_HOST` (defaulting to `5433` in `.env`) in [docker-compose.yml](../docker-compose.yml). This ensures the stack can run on developer environments with existing PostgreSQL instances running on the host port `5432`. Internally within the Docker network, service-to-service communication continues to use port `5432`.
- **Health check Configuration**: Added a Docker container health check to the `backend` service utilizing Python's built-in `urllib.request` against the `/health` endpoint (eliminating external curl dependency).
- **Service Dependency Order**: Configured the `frontend` container to only launch after the `backend` container is fully healthy (`condition: service_healthy`).
- **Environment config**: Added the new `DB_PORT_HOST=5433` environment config variables in `.env` and [.env.example](../.env.example).

---

## 2. What Was Intentionally Not Changed
- **Business Workflows**: The core database logic, Pydantic data schemas, controllers, and router bindings were left completely untouched to preserve workflow behavior.
- **Tailwind Version**: Retained Tailwind CSS v3 (`^3.4.3`) to prevent breaking the existing CSS layout and post-processing plugins.
- **Database Driver**: Kept the stable `psycopg2-binary` driver for postgresql connections rather than migrating to the newer `psycopg` (v3) to prevent query/type mapping issues.
- **Language Stack**: Kept Javascript (ES6+) for the frontend instead of introducing TypeScript in this sprint to avoid build pipeline changes.

---

## 3. Commands to Run and Test the Project

### Running the System
To start the multi-container stack, run the operations launcher script:
```powershell
.\run.cmd
```
Alternatively, execute docker compose manually:
```powershell
docker compose up -d --build
```

### Running Backend Tests
Execute the unit test suite inside the backend container context:
```powershell
docker compose exec backend pytest
```

### Building the Frontend Assets
Verify compilation of production-ready static assets:
```powershell
docker compose exec frontend npm run build
```

---

## 4. Verification Results & Known Issues

### Test Summary
- **Backend Tests**: 6 passed, 0 failed in ~20 seconds.
- **Frontend Build**: Assets successfully compiled using Vite 5.4 in 3.59 seconds.
- **Manual Verification Checks**:
  - `GET /health` -> `200 OK` (returns status: "ok")
  - `GET /docs` -> `200 OK` (docs interactive page serves correctly)
  - `GET /` -> `200 OK` (returns online status message)
  - Frontend landing page (`http://localhost:5173`) -> `200 OK`

### Known Issues & Warnings
- **Pydantic V2 Deprecation Warning**: During test execution, Pydantic outputs warnings regarding the use of legacy class-based `class Config` overrides inside schemas (such as `from_attributes = True`). In a future refactor, these should be updated to use `model_config = ConfigDict(from_attributes=True)` as recommended by Pydantic v2.
- **FastAPI Deprecation Warning**: The `@app.on_event("startup")` syntax produces a deprecation warning recommending migration to the FastAPI lifespan context manager framework.

---

## 5. Next Recommended Sprint
### **Sprint 1 — One Spirit Domain Refactor**
Now that the technical infrastructure, container synchronization, and testing baseline are modern and stable, the following tasks are recommended for Sprint 1:
1. Address the Pydantic v2 `ConfigDict` deprecation warnings across all schemas.
2. Refactor the backend startup handler from `@app.on_event` to a lifespan context manager.
3. Migrate the business domain logic (PO, PM, external sales, dashboard analytics, and Excel import parsing mapping) according to the new GVSys domain structures.
