# Production Readiness Checklist

OneSpirit Workflow is demo-ready, but production is not yet declared. Use this checklist before any production candidate deployment.

---

## 1. Environment

- [ ] `ENV=production` is set.
- [ ] `DEBUG=false` or equivalent debug behavior is disabled.
- [ ] `JWT_SECRET` is strong, unique, and not the development default.
- [ ] `DB_PASSWORD` is strong, unique, and not committed.
- [ ] `BACKEND_CORS_ORIGINS` lists only approved production/demo origins.
- [ ] HTTPS is mandatory for public access.
- [ ] Default demo/admin passwords are changed.
- [ ] `SEED_DEMO_USER=false` and `SEED_PLACEHOLDER_USERS=false`.
- [ ] `.env` is not committed.
- [ ] Production startup fails when required secrets are absent or still default.

---

## 2. Database

- [ ] PostgreSQL is used for production candidate data.
- [ ] Database volume is persistent.
- [ ] Database port is not public.
- [ ] Backup schedule is defined.
- [ ] Restore has been tested at least once.
- [ ] Alembic migration strategy is defined.
- [ ] Migration rollback plan is documented.
- [ ] `AUTO_CREATE_TABLES` is disabled after migration-first startup is ready.

---

## 3. Security

- [ ] No secrets in repository or frontend env files.
- [ ] No database public port.
- [ ] `/docs` and OpenAPI access are disabled or restricted for production if required.
- [ ] Password policy is strong.
- [ ] Role permission audit is complete.
- [ ] Logs do not print secrets or passwords.
- [ ] Temporary backend tunnel is not used as production access.
- [ ] Login rate limiting and account lockout strategy are defined.
- [ ] PNL/import/project ownership backend permissions are reviewed.

---

## 4. Deployment

- [ ] Production domain selected.
- [ ] SSL certificate configured.
- [ ] Reverse proxy configured if used.
- [ ] Docker Compose production override prepared.
- [ ] Development bind mounts and Uvicorn `--reload` are removed.
- [ ] PostgreSQL host port publishing is removed unless explicitly required.
- [ ] Restart policy configured.
- [ ] Healthcheck configured and monitored.
- [ ] Release commit hash recorded.

---

## 5. Monitoring

- [ ] Backend logs are collected.
- [ ] Frontend availability is monitored.
- [ ] Uptime monitoring configured.
- [ ] Disk usage monitoring configured.
- [ ] Backup job monitoring configured.
- [ ] Error reporting process defined.
- [ ] Restore drill result and backup age are monitored.

---

## 6. Demo vs Production

- [ ] GitHub Pages demo is understood as demo-only.
- [ ] Backend tunnel is understood as demo-only.
- [ ] Local PC is not treated as production server.
- [ ] Demo credentials are rotated after public demos.
- [ ] Production candidate uses separate data and secrets.

---

## Current Sprint 14 Blockers

- Current Compose/Dockerfiles remain development/demo configuration.
- Role PO/PM/Admin and project ownership gates are not formalized.
- Backup automation and restore drill are not complete.
- `/docs`, monitoring, rate limiting, and production reverse proxy are not finalized.
- Production deployment must not proceed until these blockers are closed.
