#!/usr/bin/env bash
set -euo pipefail

# === Config ===
BACKUP_DIR="ops/backup/archives"
RETENTION_DAYS="${RETENTION_DAYS:-14}" # simple retention (delete files older than N days)

# Encryption (optional): set ENC_CMD to something like: "age -r <pubkey>"
ENC_CMD="${ENC_CMD:-}"

# Compose file and service names (assumes docker-compose.prod.yml)
COMPOSE_FILE="docker-compose.prod.yml"
PG_SERVICE="${PG_SERVICE:-postgres}"
PGHOST="${PGHOST:-postgres}"
PGPORT="${PGPORT:-5432}"
PGUSER="${POSTGRES_USER:-zimmer}"
PGDATABASE="${POSTGRES_DB:-zimmer}"
PGPASSWORD="${POSTGRES_PASSWORD:-zimmer}"

mkdir -p "$BACKUP_DIR"

STAMP="$(date +%Y%m%d_%H%M%S)"
OUT="$BACKUP_DIR/zimmer-$STAMP.dump"
SHA="$OUT.sha256"

echo ">>> Creating logical backup (pg_dump -Fc)"
export PGPASSWORD="$PGPASSWORD"
docker compose -f "$COMPOSE_FILE" exec -T "$PG_SERVICE" \
  pg_dump -Fc -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" "$PGDATABASE" > "$OUT"

if [ -n "$ENC_CMD" ]; then
  echo ">>> Encrypting backup"
  sh -c "$ENC_CMD < \"$OUT\" > \"$OUT.enc\""
  sha256sum "$OUT.enc" > "$SHA"
  rm -f "$OUT"
else
  echo ">>> Writing checksum"
  sha256sum "$OUT" > "$SHA"
fi

echo ">>> Retention: deleting backups older than $RETENTION_DAYS days"
find "$BACKUP_DIR" -type f -name "zimmer-*.dump" -mtime +$RETENTION_DAYS -print -delete || true
find "$BACKUP_DIR" -type f -name "*.sha256" -mtime +$RETENTION_DAYS -print -delete || true

echo "✅ Backup complete: $OUT"
ls -lh "$BACKUP_DIR" | tail -n +1
