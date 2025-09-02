# Database Migrations with Alembic

This document explains how to use Alembic for database migrations in the Zimmer backend.

## Setup

The migration system is already configured with:
- `alembic.ini` - Configuration file
- `migrations/env.py` - Environment configuration
- `migrations/script.py.mako` - Migration template

## Commands

### Initialize Migrations (First Time)
```bash
# Check if models import correctly
python scripts/check_models_import.py

# Initialize migrations
python scripts/init_migrations.py
```

### Testing Migrations
```bash
# Make scripts executable (Linux/macOS)
chmod +x scripts/roundtrip_sqlite.sh

# Test migration roundtrip (downgrade/upgrade cycle)
./scripts/roundtrip_sqlite.sh

# Validate database constraints
python scripts/validate_constraints.py
```

**Windows PowerShell:**
```powershell
# Test migration roundtrip (downgrade/upgrade cycle)
powershell -ExecutionPolicy Bypass -File scripts/roundtrip_sqlite.ps1

# Validate database constraints
python scripts/validate_constraints.py
```

### Daily Usage

#### Create a New Migration
```bash
# After making model changes
alembic revision --autogenerate -m "Description of changes"
```

#### Apply Migrations
```bash
# Apply all pending migrations
alembic upgrade head

# Apply specific migration
alembic upgrade <revision_id>

# Apply one migration forward
alembic upgrade +1
```

#### Rollback Migrations
```bash
# Rollback one migration
alembic downgrade -1

# Rollback to specific revision
alembic downgrade <revision_id>

# Rollback all migrations
alembic downgrade base
```

#### Check Status
```bash
# Check current migration status
alembic current

# Check migration history
alembic history

# Check what migrations are pending
alembic show <revision_id>
```

## Development Workflow

1. **Make model changes** in `models/` directory
2. **Generate migration**: `alembic revision --autogenerate -m "Description"`
3. **Review migration** in `migrations/versions/`
4. **Apply migration**: `alembic upgrade head`
5. **Test your changes**

## Production Deployment

1. **Backup database** before applying migrations
2. **Review migrations** that will be applied
3. **Apply migrations**: `alembic upgrade head`
4. **Verify application** works correctly

## Testing

### Migration Roundtrip Testing
Test that migrations can be applied and rolled back safely:

#### SQLite Testing
```bash
# Linux/macOS
./scripts/roundtrip_sqlite.sh

# Windows PowerShell
powershell -ExecutionPolicy Bypass -File scripts/roundtrip_sqlite.ps1
```

#### PostgreSQL Testing
```bash
# Linux/macOS
chmod +x scripts/roundtrip_postgres.sh
./scripts/roundtrip_postgres.sh

# Windows PowerShell
powershell -ExecutionPolicy Bypass -File scripts/roundtrip_postgres.ps1
```

**Note:** PostgreSQL testing requires Docker Desktop to be running. If Docker is not available, you can use SQLite testing instead.

### PostgreSQL Database Testing
Test migrations against a real PostgreSQL database:

1. **Start PostgreSQL container:**
   ```bash
   docker compose -f docker-compose.postgres.yml up -d db
   ```

2. **Set PostgreSQL database URL:**
   ```bash
   export DATABASE_URL=postgresql+psycopg2://zimmer:zimmer@localhost:5432/zimmer
   ```

3. **Run migration tests:**
   ```bash
   # Test roundtrip
   ./scripts/roundtrip_postgres.sh
   
   # Test constraints
   python scripts/validate_constraints.py
   ```

4. **Clean up:**
   ```bash
   docker compose -f docker-compose.postgres.yml down
   ```

**Test PostgreSQL setup:**
```bash
python scripts/test_postgres_setup.py
```

### Constraint Validation
Verify that database constraints are working correctly:

```bash
python scripts/validate_constraints.py
```

This script tests:
- UNIQUE constraints (email, telegram_bot_token)
- NOT NULL constraints (password_hash, tokens_remaining)
- Foreign key constraints (user_id, automation_id)
- Primary key constraints

## Troubleshooting

### Common Issues

#### Models Not Detected
```bash
# Check if models import correctly
python scripts/check_models_import.py
```

#### Migration Conflicts
```bash
# Check migration history
alembic history --verbose

# If needed, create a new migration to resolve conflicts
alembic revision --autogenerate -m "Resolve conflicts"
```

#### Database Connection Issues
- Verify `DATABASE_URL` in `.env` file
- Check database server is running
- Ensure database user has proper permissions

#### Docker Issues (PostgreSQL Testing)
- Ensure Docker Desktop is running
- Check Docker service status: `docker info`
- Verify Docker Compose is available: `docker compose version`
- If Docker is not available, use SQLite testing instead

### Reset Development Database

If you need to start fresh in development:

```bash
# Remove existing database
rm dev.db

# Remove all migration files (except env.py and script.py.mako)
rm migrations/versions/*.py

# Reinitialize migrations
python scripts/init_migrations.py
```

## Migration Best Practices

1. **Always review** auto-generated migrations before applying
2. **Use descriptive names** for migrations
3. **Test migrations** on development data before production
4. **Backup database** before applying migrations in production
5. **Keep migrations small** and focused on specific changes
6. **Document complex migrations** with comments

## Drift Guard

Run this locally to ensure your models match the current DB schema:

```bash
# Use SQLite or Postgres by setting DATABASE_URL
export DATABASE_URL=sqlite:///./dev.db
python scripts/check_migration_drift.py
```

## File Structure

```
zimmer-backend/
├── alembic.ini              # Alembic configuration
├── migrations/
│   ├── env.py              # Environment configuration
│   ├── script.py.mako      # Migration template
│   └── versions/           # Migration files
│       ├── 001_initial.py
│       ├── 002_add_user_fields.py
│       └── ...
├── models/                 # SQLAlchemy models
├── scripts/
│   ├── check_models_import.py
│   ├── init_migrations.py
│   ├── roundtrip_sqlite.sh
│   ├── roundtrip_sqlite.ps1
│   ├── roundtrip_postgres.sh
│   ├── roundtrip_postgres.ps1
│   ├── test_postgres_setup.py
│   └── validate_constraints.py
├── docker-compose.postgres.yml
└── MIGRATIONS_README.md    # This file
```
