# Zimmer DB Backup & Restore

## What this does
- `backup_db.sh` → creates a compressed, versioned `pg_dump` (custom format) and a SHA256 checksum.
- `restore_db.sh` → restores a dump into a target Postgres, with integrity checks and safety guards.
- `test_restore.sh` → spins a *fresh* Postgres on port 5433, restores the latest dump, and runs health checks (migrations + constraints).

## Where files go
All backups are stored under `ops/backup/archives/`:
- `zimmer-YYYYMMDD_HHMMSS.dump`
- `zimmer-YYYYMMDD_HHMMSS.dump.sha256`

## Quick start
```bash
# Create backup from running prod/staging stack (uses docker-compose.prod.yml Postgres)
bash ops/scripts/backup_db.sh

# Test restore end-to-end (uses a temp Postgres on 5433)
bash ops/scripts/test_restore.sh
```

## Scheduling
Run backup_db.sh via host cron or CI on a schedule (e.g., hourly or nightly).

Keep at least 7 daily + 4 weekly backups (see retention policy at the top of the script).

## Security
Backups may contain sensitive data; store off-server too.

For extra safety, wrap backups with age/gpg for encryption (optional hook provided).
