# Secret Rotation Plan

This plan defines which secrets must be managed and when they should be rotated for OneSpirit Workflow.

---

## 1. Secrets to Manage

- `JWT_SECRET`
- `DB_PASSWORD`
- Admin user password
- Demo user password
- GitHub Actions secret `VITE_API_BASE_URL`
- Any future API token or integration credential

---

## 2. When to Rotate

- After a public demo.
- If a tunnel URL or demo password was shared too broadly.
- Before production candidate deployment.
- After a team member or vendor leaves the project.
- After suspected credential exposure.
- On a planned quarterly production maintenance cycle.

---

## 3. Rotation Procedure

### JWT Secret

1. Generate a new strong random secret.
2. Update backend environment configuration.
3. Restart backend.
4. Existing JWT sessions become invalid and users must login again.
5. Verify login and protected routes.

### Database Password

1. Create a database backup.
2. Change PostgreSQL user password.
3. Update backend environment configuration.
4. Restart backend.
5. Verify healthcheck, login, dashboard, and write flows.

### Admin/Demo Password

1. Update user password through admin workflow or database maintenance script.
2. Update secure password manager, not repository docs.
3. Verify login.
4. Revoke or change demo password after public demos.

### GitHub Actions `VITE_API_BASE_URL`

1. Update repository secret in GitHub Actions.
2. Re-run frontend Pages deployment workflow.
3. Verify GitHub Pages frontend can reach backend tunnel.

---

## 4. Important Notes

- `VITE_API_BASE_URL` is not a sensitive secret because frontend build values are visible in the browser bundle. It still needs rotation whenever the demo tunnel URL changes.
- `JWT_SECRET` and `DB_PASSWORD` must never be placed in frontend env files.
- `.env` must remain untracked.
- Do not paste production secrets into screenshots, public issue trackers, or client demo materials.
- Record only rotation date, owner, environment, and verification result. Never record the secret value.

---

## 5. Sprint 15+ Recommendations

- Adopt a password manager or cloud secret manager.
- Add a release checklist item for secret rotation.
- Document emergency token invalidation procedure.
- Separate demo, staging, and production credentials.
