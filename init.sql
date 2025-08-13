-- Zimmer Dashboard Database Initialization
-- This script runs when the PostgreSQL container starts for the first time

-- Create extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create additional indexes for better performance
-- (These will be created automatically by SQLAlchemy, but you can add custom ones here)

-- Set timezone
SET timezone = 'UTC';

-- Create a backup user (optional)
-- CREATE USER zimmer_backup WITH PASSWORD 'backup_password';
-- GRANT CONNECT ON DATABASE zimmer_dashboard TO zimmer_backup;
-- GRANT USAGE ON SCHEMA public TO zimmer_backup;
-- GRANT SELECT ON ALL TABLES IN SCHEMA public TO zimmer_backup; 