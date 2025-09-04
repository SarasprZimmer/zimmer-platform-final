# Email Verification Migration
Run:
```bash
alembic revision --autogenerate -m "email verification"
alembic upgrade head
```

## Discounts
Run:
```bash
alembic revision --autogenerate -m "discount codes and redemptions"
alembic upgrade head
```

**Run migrations & tests**
```bash
cd zimmer-backend
$env:DATABASE_URL="sqlite:///./_discounts.db"        # PowerShell; bash: export DATABASE_URL=...
alembic revision --autogenerate -m "discount codes and redemptions"
alembic upgrade head
pytest -q tests/test_discounts.py
```