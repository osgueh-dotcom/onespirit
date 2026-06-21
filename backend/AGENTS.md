# Backend Agent Rules

- Follow the FastAPI module pattern: `router.py`, `service.py`, `schemas.py`,
  `models.py`.
- Keep routers thin. Put reusable queries and workflow rules in services.
- Use typed Pydantic schemas and SQLAlchemy 2-compatible patterns.
- Keep authentication and permission enforcement server-side.
- Use Alembic for durable schema changes. Do not rely on `create_all()` as a
  production migration strategy.
- Roll back failed transactions and return safe user-facing errors.
- Add or update pytest coverage for workflow, authorization, validation, and
  response-contract changes.
- Validate from `backend/` with `python -m pytest app/tests -q` and
  `python -m pip check`.
