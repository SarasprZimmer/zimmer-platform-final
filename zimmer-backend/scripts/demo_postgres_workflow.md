# PostgreSQL Migration Testing Workflow

This document demonstrates the complete PostgreSQL migration testing workflow.

## Prerequisites

1. **Docker Desktop** must be running
2. **PostgreSQL dependencies** installed (`psycopg2-binary`)

## Complete Workflow

### Step 0: Start PostgreSQL Container
```bash
docker compose -f docker-compose.postgres.yml up -d db
```

**Expected Output:**
```
[+] Running 1/1
 ✔ Container zimmer_pg_test  Started
```

### Step 1: Set PostgreSQL Database URL
```bash
export DATABASE_URL=postgresql+psycopg2://zimmer:zimmer@localhost:5432/zimmer
```

### Step 2: Test PostgreSQL Setup
```bash
python scripts/test_postgres_setup.py
```

**Expected Output:**
```
🔍 Testing PostgreSQL setup...
✅ Docker is available
✅ PostgreSQL container is running
✅ PostgreSQL connection successful: PostgreSQL 15.x
🎉 PostgreSQL setup is working correctly!
```

### Step 3: Start from Scratch and Migrate Up
```bash
# Downgrade to base (fresh start)
alembic -c alembic.ini downgrade base

# Upgrade to head (apply all migrations)
alembic -c alembic.ini upgrade head
```

**Expected Output:**
```
INFO  [alembic.runtime.migration] Context impl PostgreSQLImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> a9b90e0973ef, Initial migration
```

### Step 4: Validate Constraints
```bash
python scripts/validate_constraints.py
```

**Expected Output:**
```
✅ Passed [insert valid user]
✅ Expected fail [unique email duplicate (should fail)]: IntegrityError
✅ Expected fail [missing password_hash (should fail)]: IntegrityError
✅ Passed [insert automation]
✅ Passed [insert user_automation valid]
✅ Expected fail [duplicate telegram_bot_token (should fail)]: IntegrityError
✅ Expected fail [FK violation user_id (should fail)]: IntegrityError
✅ Passed [insert payment valid]
✅ Expected fail [payment FK violation user_id (should fail)]: IntegrityError
🎉 Constraint validation passed.
```

### Step 5: Run Complete Roundtrip Test
```bash
# Linux/macOS
./scripts/roundtrip_postgres.sh

# Windows PowerShell
powershell -ExecutionPolicy Bypass -File scripts/roundtrip_postgres.ps1
```

**Expected Output:**
```
>>> Starting Postgres (if not running)
>>> Waiting for DB health...
>>> Alembic downgrade to base
>>> Alembic upgrade to head
>>> Alembic downgrade to base
>>> Alembic upgrade to head
>>> Roundtrip on Postgres complete.
```

### Step 6: Clean Up
```bash
docker compose -f docker-compose.postgres.yml down
```

## Key Differences from SQLite

1. **Database Type**: PostgreSQL vs SQLite
2. **Transaction Support**: Full ACID compliance
3. **Constraint Enforcement**: Stricter foreign key constraints
4. **Performance**: Better for concurrent access
5. **Production-like**: Matches production database environment

## Troubleshooting

### Docker Issues
- Ensure Docker Desktop is running
- Check Docker service: `docker info`
- Verify Docker Compose: `docker compose version`

### Connection Issues
- Verify PostgreSQL container is running: `docker ps`
- Check container logs: `docker logs zimmer_pg_test`
- Test connection: `python scripts/test_postgres_setup.py`

### Migration Issues
- Check current migration: `alembic current`
- View migration history: `alembic history`
- Reset if needed: `alembic downgrade base && alembic upgrade head`
