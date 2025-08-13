import os
import subprocess
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from models.backup import BackupLog, BackupStatus
import logging
from sqlalchemy import func

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BackupService:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.backup_dir = Path("backups")
        self.backup_dir.mkdir(exist_ok=True)
        
        # Database configuration
        self.db_path = "zimmer_dashboard.db"
        self.db_type = self._detect_db_type()
    
    def _detect_db_type(self) -> str:
        """Detect if we're using SQLite or PostgreSQL"""
        if os.path.exists(self.db_path):
            return "sqlite"
        else:
            # Check for PostgreSQL connection string in environment
            if os.getenv("DATABASE_URL", "").startswith("postgresql"):
                return "postgresql"
            return "sqlite"  # Default to SQLite
    
    def run_backup(self) -> Tuple[bool, str, Optional[str]]:
        """
        Run database backup
        Returns: (success, message, file_path)
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            if self.db_type == "sqlite":
                return self._backup_sqlite(timestamp)
            elif self.db_type == "postgresql":
                return self._backup_postgresql(timestamp)
            else:
                return False, "Unknown database type", None
                
        except Exception as e:
            logger.error(f"Backup failed: {e}")
            return False, f"Backup failed: {str(e)}", None
    
    def _backup_sqlite(self, timestamp: str) -> Tuple[bool, str, Optional[str]]:
        """Backup SQLite database"""
        try:
            backup_file = self.backup_dir / f"zimmer_backup_{timestamp}.sql"
            
            # Create SQLite dump
            conn = sqlite3.connect(self.db_path)
            with open(backup_file, 'w', encoding='utf-8') as f:
                for line in conn.iterdump():
                    f.write(f'{line}\n')
            conn.close()
            
            # Get file size
            file_size = backup_file.stat().st_size
            
            # Create backup log entry
            backup_log = BackupLog(
                file_name=backup_file.name,
                file_size=file_size,
                status=BackupStatus.success,
                storage_location="local"
            )
            self.db_session.add(backup_log)
            self.db_session.commit()
            
            logger.info(f"SQLite backup successful: {backup_file.name} ({file_size} bytes)")
            return True, f"Backup successful: {backup_file.name}", str(backup_file)
            
        except Exception as e:
            logger.error(f"SQLite backup failed: {e}")
            
            # Log failed backup
            backup_log = BackupLog(
                file_name=f"failed_backup_{timestamp}",
                file_size=0,
                status=BackupStatus.failed,
                storage_location="local"
            )
            self.db_session.add(backup_log)
            self.db_session.commit()
            
            return False, f"SQLite backup failed: {str(e)}", None
    
    def _backup_postgresql(self, timestamp: str) -> Tuple[bool, str, Optional[str]]:
        """Backup PostgreSQL database"""
        try:
            backup_file = self.backup_dir / f"zimmer_backup_{timestamp}.sql"
            
            # Get database connection details from environment
            database_url = os.getenv("DATABASE_URL")
            if not database_url:
                return False, "DATABASE_URL not configured", None
            
            # Extract connection details
            # Format: postgresql://user:password@host:port/database
            import urllib.parse
            parsed = urllib.parse.urlparse(database_url)
            
            # Run pg_dump
            cmd = [
                "pg_dump",
                f"--host={parsed.hostname}",
                f"--port={parsed.port or 5432}",
                f"--username={parsed.username}",
                f"--dbname={parsed.path[1:]}",  # Remove leading slash
                f"--file={backup_file}"
            ]
            
            # Set password environment variable
            env = os.environ.copy()
            if parsed.password:
                env["PGPASSWORD"] = parsed.password
            
            # Execute pg_dump
            result = subprocess.run(cmd, env=env, capture_output=True, text=True)
            
            if result.returncode != 0:
                raise Exception(f"pg_dump failed: {result.stderr}")
            
            # Get file size
            file_size = backup_file.stat().st_size
            
            # Create backup log entry
            backup_log = BackupLog(
                file_name=backup_file.name,
                file_size=file_size,
                status=BackupStatus.success,
                storage_location="local"
            )
            self.db_session.add(backup_log)
            self.db_session.commit()
            
            logger.info(f"PostgreSQL backup successful: {backup_file.name} ({file_size} bytes)")
            return True, f"Backup successful: {backup_file.name}", str(backup_file)
            
        except Exception as e:
            logger.error(f"PostgreSQL backup failed: {e}")
            
            # Log failed backup
            backup_log = BackupLog(
                file_name=f"failed_backup_{timestamp}",
                file_size=0,
                status=BackupStatus.failed,
                storage_location="local"
            )
            self.db_session.add(backup_log)
            self.db_session.commit()
            
            return False, f"PostgreSQL backup failed: {str(e)}", None
    
    def upload_to_remote(self, file_path: str) -> bool:
        """
        Upload backup to remote storage (S3, etc.)
        This is a stub function for future implementation
        """
        try:
            # TODO: Implement S3 upload (ArvanCloud, MinIO, etc.)
            logger.info(f"Remote upload stub called for: {file_path}")
            return True
        except Exception as e:
            logger.error(f"Remote upload failed: {e}")
            return False
    
    def cleanup_old_backups(self, retention_days: int = 7) -> Tuple[int, List[str]]:
        """
        Clean up old backup files and database records
        Returns: (deleted_count, cleaned_files)
        """
        try:
            cutoff_date = datetime.now() - timedelta(days=retention_days)
            deleted_count = 0
            cleaned_files = []
            
            # Get old backup records
            old_backups = self.db_session.query(BackupLog).filter(
                BackupLog.created_at < cutoff_date
            ).all()
            
            for backup in old_backups:
                # Delete backup file if it exists
                backup_file = self.backup_dir / backup.file_name
                if backup_file.exists():
                    try:
                        backup_file.unlink()
                        cleaned_files.append(backup.file_name)
                        logger.info(f"Deleted backup file: {backup.file_name}")
                    except Exception as e:
                        logger.error(f"Failed to delete backup file {backup.file_name}: {e}")
                
                # Delete database record
                self.db_session.delete(backup)
                deleted_count += 1
            
            self.db_session.commit()
            logger.info(f"Cleanup completed: {deleted_count} backups removed")
            
            return deleted_count, cleaned_files
            
        except Exception as e:
            logger.error(f"Cleanup failed: {e}")
            self.db_session.rollback()
            return 0, []
    
    def verify_backup(self, backup_id: int) -> bool:
        """Mark a backup as verified"""
        try:
            backup = self.db_session.query(BackupLog).filter(BackupLog.id == backup_id).first()
            if not backup:
                return False
            
            backup.verified = True
            self.db_session.commit()
            
            logger.info(f"Backup {backup_id} marked as verified")
            return True
            
        except Exception as e:
            logger.error(f"Failed to verify backup {backup_id}: {e}")
            self.db_session.rollback()
            return False
    
    def get_backup_stats(self) -> dict:
        """Get backup statistics"""
        try:
            total_backups = self.db_session.query(BackupLog).count()
            successful_backups = self.db_session.query(BackupLog).filter(
                BackupLog.status == BackupStatus.success
            ).count()
            failed_backups = self.db_session.query(BackupLog).filter(
                BackupLog.status == BackupStatus.failed
            ).count()
            verified_backups = self.db_session.query(BackupLog).filter(
                BackupLog.verified == True
            ).count()
            
            # Get last successful backup
            last_successful = self.db_session.query(BackupLog).filter(
                BackupLog.status == BackupStatus.success
            ).order_by(BackupLog.backup_date.desc()).first()
            
            # Calculate total size
            total_size = self.db_session.query(BackupLog).filter(
                BackupLog.status == BackupStatus.success
            ).with_entities(func.sum(BackupLog.file_size)).scalar() or 0
            
            return {
                "total_backups": total_backups,
                "successful_backups": successful_backups,
                "failed_backups": failed_backups,
                "verified_backups": verified_backups,
                "last_successful_backup": last_successful.backup_date if last_successful else None,
                "total_size_bytes": total_size
            }
            
        except Exception as e:
            logger.error(f"Failed to get backup stats: {e}")
            return {
                "total_backups": 0,
                "successful_backups": 0,
                "failed_backups": 0,
                "verified_backups": 0,
                "last_successful_backup": None,
                "total_size_bytes": 0
            } 