# Backup & Restore Plan

## 1. Backup Scope

- PostgreSQL database.
- Upload volume/folder.
- Environment examples, tanpa secret asli.
- Docker/deployment configuration.
- Alembic migrations.
- Release commit hash.

## 2. Manual Backup

Create the destination first:

```bash
mkdir -p backups
```

Database backup from the generic `db` service:

```bash
docker compose exec -T db sh -c 'pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB"' > backups/onespirit_YYYYMMDD_HHMMSS.sql
```

Upload volume backup through the backend service:

```bash
docker compose exec -T backend tar -czf - -C /app uploads > backups/uploads_YYYYMMDD_HHMMSS.tar.gz
```

Record the release:

```bash
git rev-parse HEAD > backups/release_YYYYMMDD_HHMMSS.txt
```

Do not put a real password directly in command history.

## 3. Restore

Restore into a clean/test database, not directly over the only production copy:

```bash
docker compose exec -T db sh -c 'psql -U "$POSTGRES_USER" "$POSTGRES_DB"' < backups/onespirit_YYYYMMDD_HHMMSS.sql
```

Restore uploads:

```bash
docker compose exec -T backend tar -xzf - -C /app < backups/uploads_YYYYMMDD_HHMMSS.tar.gz
```

For Windows PowerShell, run the commands through Git Bash/WSL or use `docker compose cp` to copy `/app/uploads` before compressing it. Binary archives must not be passed through text conversion cmdlets.

## 4. Schedule

- Before every client demo.
- Before every migration.
- Daily for production candidate data.
- Weekly archive with defined retention.
- Before deployment and rollback rehearsal.

## 5. Restore Test

A backup is not valid until restore succeeds.

1. Start a clean database/volume.
2. Restore SQL and uploads.
3. Start backend and frontend.
4. Verify login, Dashboard, Projects, Documents, Finance, PM Control, and PO Control.
5. Verify representative CL, ROS, CK, and PNL records.
6. Record backup filename, restore date, operator, result, and commit hash.

## 6. Limitations

- No scheduled backup job.
- No off-site or encrypted backup storage.
- No automatic retention cleanup.
- No completed restore drill is recorded yet.
