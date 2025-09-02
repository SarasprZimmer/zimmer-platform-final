#!/usr/bin/env bash
set -euo pipefail

export DATABASE_URL=${DATABASE_URL:-postgresql+psycopg2://zimmer:zimmer@localhost:5432/zimmer}

echo ">>> Starting Postgres (if not running)"
docker compose -f docker-compose.postgres.yml up -d db

echo ">>> Waiting for DB health..."
for i in {1..30}; do
  if docker inspect --format='{{json .State.Health.Status}}' zimmer_pg_test 2>/dev/null | grep -q healthy; then
    break
  fi
  sleep 1
done

echo ">>> Alembic downgrade to base"
alembic -c alembic.ini downgrade base

echo ">>> Alembic upgrade to head"
alembic -c alembic.ini upgrade head

echo ">>> Alembic downgrade to base"
alembic -c alembic.ini downgrade base

echo ">>> Alembic upgrade to head"
alembic -c alembic.ini upgrade head

echo ">>> Roundtrip on Postgres complete."
