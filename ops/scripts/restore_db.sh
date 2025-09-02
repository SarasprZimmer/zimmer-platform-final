#!/usr/bin/env bash
set -euo pipefail

# Usage: ops/scripts/restore_db.sh <dump_file_or_encrypted>
# Restores into the postgres-restore service (port 5433) using DB zimmer_restore.

DUMP="${1:-}"
if [ -z "$DUMP" ]; then
  echo "Usage: $0 <dump_file>" >&2
  exit 1
fi

# If encrypted, decrypt first (set DEC_CMD to e.g., "age -d -i key.txt")
DEC_CMD="${DEC_CMD:-}"

if [ ! -f "$DUMP" ]; then
  echo "File not found: $DUMP" >&2
  exit 1
fi

# Verify checksum if available
if [ -f "$DUMP.sha256" ]; then
  echo ">>> Verifying checksum"
  sha256sum -c "$DUMP.sha256"
else
  # If using encrypted dumps, expect .enc and paired .sha256
  [ -f "$DUMP.enc.sha256" ] && sha256sum -c "$DUMP.enc.sha256" || true
fi

TMPFILE="$DUMP"
if [ -n "$DEC_CMD" ] && [[ "$DUMP" == *.enc ]]; then
  echo ">>> Decrypting backup"
  TMPFILE="$(mktemp)"
  sh -c "$DEC_CMD < \"$DUMP\" > \"$TMPFILE\""
fi

echo ">>> Ensure restore Postgres is running on 5433"
docker compose -f ops/restore-compose.yml up -d postgres-restore

# Wait for health
echo ">>> Waiting for postgres-restore health…"
for i in {1..30}; do
  status="$(docker inspect --format='{{json .State.Health.Status}}' zimmer_postgres_restore 2>/dev/null || echo null)"
  echo "  status: $status"
  if echo "$status" | grep -q healthy; then break; fi
  sleep 1
done

export PGPASSWORD="zimmer"
PGHOST="localhost"
PGPORT="5433"
PGUSER="zimmer"
PGDATABASE="zimmer_restore"

echo ">>> Dropping and recreating schema (public)"
docker run --rm --network host -e PGPASSWORD="$PGPASSWORD" postgres:15 \
  psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -c "DROP SCHEMA IF EXISTS public CASCADE; CREATE SCHEMA public;"

echo ">>> Restoring dump (pg_restore --clean --no-owner --no-privileges)"
docker run --rm --network host -e PGPASSWORD="$PGPASSWORD" -v "$(pwd):/work" -w /work postgres:15 \
  pg_restore -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" --clean --no-owner --no-privileges "$TMPFILE"

echo "✅ Restore complete into db=zimmer_restore on port 5433"
