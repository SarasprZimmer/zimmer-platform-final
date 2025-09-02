# Zimmer Backup & Restore System Guide

## 🎯 Overview

This backup system provides production-safe database backup and restore capabilities for the Zimmer platform using PostgreSQL's `pg_dump` and `pg_restore` tools.

## 📁 File Structure

```
ops/
├── backup/
│   ├── README.md                 # Quick reference
│   ├── archives/                 # Backup storage location
│   │   ├── zimmer-20250828_143022.dump
│   │   └── zimmer-20250828_143022.dump.sha256
│   └── BACKUP_SYSTEM_GUIDE.md    # This comprehensive guide
├── scripts/
│   ├── backup_db.sh              # Create backups
│   ├── restore_db.sh             # Restore backups
│   ├── test_restore.sh           # End-to-end restore testing
│   ├── latest_backup.sh          # Find latest backup
│   └── backup_status.sh          # Monitor backup health
├── restore-compose.yml           # Isolated restore environment
└── .github/workflows/
    └── backup-restore-test.yml   # CI restore testing
```

## 🚀 Quick Start

### 1. Create Your First Backup

```bash
# From repository root
bash ops/scripts/backup_db.sh
```

**Expected Output:**
```
>>> Creating logical backup (pg_dump -Fc)
>>> Writing checksum
>>> Retention: deleting backups older than 14 days
✅ Backup complete: ops/backup/archives/zimmer-20250828_143022.dump
```

### 2. Test Restore End-to-End

```bash
# Test that your backup can be restored (uses port 5433, safe)
bash ops/scripts/test_restore.sh
```

**Expected Output:**
```
>>> Using latest backup: ops/backup/archives/zimmer-20250828_143022.dump
>>> Verifying checksum
>>> Ensure restore Postgres is running on 5433
>>> Restoring dump (pg_restore --clean --no-owner --no-privileges)
>>> Running alembic upgrade head against restored DB
>>> Running constraint validation
🎉 Restore test passed: backup can be restored and schema is consistent.
```

### 3. Monitor Backup Health

```bash
bash ops/scripts/backup_status.sh
```

## 🔧 Configuration

### Environment Variables

The backup system uses these environment variables (with defaults):

```bash
# Database connection
PGHOST=postgres
PGPORT=5432
PGUSER=zimmer
PGDATABASE=zimmer
PGPASSWORD=zimmer

# Docker Compose
COMPOSE_FILE=docker-compose.prod.yml
PG_SERVICE=postgres

# Retention
RETENTION_DAYS=14

# Optional encryption
ENC_CMD=""  # e.g., "age -r <pubkey>"
DEC_CMD=""  # e.g., "age -d -i key.txt"
```

### Production Setup

1. **Create `.env` file** in repository root:
```bash
POSTGRES_USER=zimmer
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=zimmer
```

2. **Ensure production stack is running**:
```bash
docker compose -f docker-compose.prod.yml up -d
```

## 📅 Scheduling

### Cron Job Setup

Add to your server's crontab (`crontab -e`):

```bash
# Daily backup at 2 AM
0 2 * * * cd /path/to/zimmer-full-structure && bash ops/scripts/backup_db.sh >> /var/log/zimmer-backup.log 2>&1

# Weekly restore test on Sunday at 3 AM
0 3 * * 0 cd /path/to/zimmer-full-structure && bash ops/scripts/test_restore.sh >> /var/log/zimmer-restore-test.log 2>&1
```

### CI/CD Integration

The system includes a GitHub Actions workflow (`.github/workflows/backup-restore-test.yml`) that can be triggered manually to test restore functionality.

## 🔒 Security Features

### Checksum Verification
- Every backup includes a SHA256 checksum
- Restore process verifies checksum before proceeding
- Prevents corruption during transfer/storage

### Encryption Support
- Optional encryption using `age` or `gpg`
- Set `ENC_CMD` and `DEC_CMD` environment variables
- Encrypted backups are automatically handled

### Isolated Restore Environment
- Restore testing uses separate PostgreSQL on port 5433
- Never touches production database
- Fresh container for each test

## 🛠️ Advanced Usage

### Manual Restore

```bash
# Restore specific backup file
bash ops/scripts/restore_db.sh ops/backup/archives/zimmer-20250828_143022.dump
```

### Encrypted Backups

```bash
# Create encrypted backup
ENC_CMD="age -r age1..." bash ops/scripts/backup_db.sh

# Restore encrypted backup
DEC_CMD="age -d -i key.txt" bash ops/scripts/restore_db.sh backup.enc
```

### Custom Retention

```bash
# Keep backups for 30 days
RETENTION_DAYS=30 bash ops/scripts/backup_db.sh
```

### Backup to Remote Storage

```bash
# After backup, sync to remote storage
bash ops/scripts/backup_db.sh
rsync -av ops/backup/archives/ user@backup-server:/backups/zimmer/
```

## 🔍 Monitoring & Troubleshooting

### Backup Status Check

```bash
bash ops/scripts/backup_status.sh
```

**Sample Output:**
```
📊 Zimmer Backup Status Report
==============================

📈 Backup Statistics:
  Total backups: 5
  Checksum files: 5

📅 Recent Backups:
    2025-08-28 14:30:22 - 45M - zimmer-20250828_143022.dump
    2025-08-27 14:30:15 - 44M - zimmer-20250827_143015.dump

🔍 Integrity Check:
  All backups have checksums ✓

⏰ Backup Age Analysis:
  ✅ Latest backup is 2 hours old

💾 Disk Usage:
  Backup directory size: 220M

🎯 Recommendations:
  • Backup system is healthy ✓
  • Consider testing restore: bash ops/scripts/test_restore.sh
```

### Common Issues

#### 1. "No backups found"
- Check if `ops/backup/archives/` directory exists
- Verify production stack is running
- Check database connection settings

#### 2. "pg_dump: connection to server failed"
- Ensure PostgreSQL container is healthy
- Verify `PGHOST`, `PGPORT`, `PGUSER`, `PGPASSWORD` settings
- Check if database exists

#### 3. "Restore test failed"
- Check if port 5433 is available
- Verify backup file integrity
- Check Alembic migration status

#### 4. "Permission denied"
- Ensure scripts are executable: `chmod +x ops/scripts/*.sh`
- Check Docker permissions
- Verify file ownership

## 📊 Backup Formats

### pg_dump Custom Format (-Fc)
- **Compressed**: Significantly smaller than plain SQL
- **Selective restore**: Can restore specific tables/schemas
- **Parallel restore**: Faster restoration with `--jobs`
- **Metadata preservation**: Includes indexes, constraints, etc.

### File Naming Convention
```
zimmer-YYYYMMDD_HHMMSS.dump
zimmer-YYYYMMDD_HHMMSS.dump.sha256
```

## 🔄 Restore Process

### Safety Features
1. **Checksum verification** before restore
2. **Isolated environment** (port 5433)
3. **Schema cleanup** (drops and recreates public schema)
4. **No ownership transfer** (--no-owner flag)
5. **Migration re-application** after restore
6. **Constraint validation** to ensure integrity

### Restore Steps
1. Verify backup file exists and has checksum
2. Start isolated PostgreSQL container
3. Wait for database health check
4. Drop and recreate public schema
5. Restore data using pg_restore
6. Run Alembic migrations
7. Validate database constraints

## 🎯 Best Practices

### Backup Strategy
- **Frequency**: Daily backups for production
- **Retention**: 14 days minimum, 30 days recommended
- **Testing**: Weekly restore tests
- **Off-site**: Store backups in multiple locations
- **Monitoring**: Regular status checks

### Security
- **Encryption**: Use encryption for sensitive data
- **Access control**: Limit backup file access
- **Network security**: Secure backup transfer
- **Audit logging**: Log backup operations

### Performance
- **Timing**: Run backups during low-traffic periods
- **Compression**: Use pg_dump custom format
- **Parallel restore**: Use --jobs for large databases
- **Monitoring**: Track backup size and duration

## 🚨 Disaster Recovery

### Recovery Scenarios

#### 1. Complete Database Loss
```bash
# 1. Stop production services
docker compose -f docker-compose.prod.yml down

# 2. Restore latest backup
bash ops/scripts/restore_db.sh $(ops/scripts/latest_backup.sh)

# 3. Update production database
# (Copy from restore environment to production)

# 4. Restart services
docker compose -f docker-compose.prod.yml up -d
```

#### 2. Partial Data Loss
```bash
# Restore specific tables from backup
pg_restore -h localhost -p 5432 -U zimmer -d zimmer \
  --table=users --table=payments \
  ops/backup/archives/zimmer-20250828_143022.dump
```

#### 3. Schema Corruption
```bash
# 1. Test restore to verify backup integrity
bash ops/scripts/test_restore.sh

# 2. If successful, restore to production
bash ops/scripts/restore_db.sh $(ops/scripts/latest_backup.sh)
```

## 📞 Support

### Logs
- Backup logs: `/var/log/zimmer-backup.log`
- Restore test logs: `/var/log/zimmer-restore-test.log`
- Docker logs: `docker logs zimmer_postgres_restore`

### Health Checks
- Database health: `docker compose -f docker-compose.prod.yml ps`
- Backup status: `bash ops/scripts/backup_status.sh`
- Restore environment: `docker compose -f ops/restore-compose.yml ps`

### Emergency Contacts
- Database administrator
- DevOps team
- System administrator

---

**Last Updated**: August 28, 2025  
**Version**: 1.0.0  
**Maintainer**: Zimmer DevOps Team
