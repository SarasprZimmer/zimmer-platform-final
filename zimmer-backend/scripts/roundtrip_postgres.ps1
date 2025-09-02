#!/usr/bin/env pwsh
# PowerShell version of roundtrip_postgres.sh

$env:DATABASE_URL = if ($env:DATABASE_URL) { $env:DATABASE_URL } else { "postgresql+psycopg2://zimmer:zimmer@localhost:5432/zimmer" }

Write-Host ">>> Starting Postgres (if not running)"
docker compose -f docker-compose.postgres.yml up -d db

Write-Host ">>> Waiting for DB health..."
for ($i = 1; $i -le 30; $i++) {
    try {
        $health = docker inspect --format='{{json .State.Health.Status}}' zimmer_pg_test 2>$null
        if ($health -match "healthy") {
            break
        }
    } catch {
        # Container might not exist yet
    }
    Start-Sleep -Seconds 1
}

Write-Host ">>> Alembic downgrade to base"
alembic -c alembic.ini downgrade base

Write-Host ">>> Alembic upgrade to head"
alembic -c alembic.ini upgrade head

Write-Host ">>> Alembic downgrade to base"
alembic -c alembic.ini downgrade base

Write-Host ">>> Alembic upgrade to head"
alembic -c alembic.ini upgrade head

Write-Host ">>> Roundtrip on Postgres complete."
