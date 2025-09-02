# PowerShell version of backup_db.sh for Windows users
# Usage: .\ops\scripts\backup_db.ps1

param(
    [string]$RetentionDays = "14",
    [string]$EncCmd = "",
    [string]$ComposeFile = "docker-compose.prod.yml",
    [string]$PgService = "postgres",
    [string]$PgHost = "postgres",
    [string]$PgPort = "5432",
    [string]$PgUser = "zimmer",
    [string]$PgDatabase = "zimmer",
    [string]$PgPassword = "zimmer"
)

# Set error action preference
$ErrorActionPreference = "Stop"

# Configuration
$BackupDir = "ops/backup/archives"

# Create backup directory if it doesn't exist
if (!(Test-Path $BackupDir)) {
    New-Item -ItemType Directory -Path $BackupDir -Force | Out-Null
}

# Generate timestamp
$Stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$Out = "$BackupDir/zimmer-$Stamp.dump"
$Sha = "$Out.sha256"

Write-Host ">>> Creating logical backup (pg_dump -Fc)"

# Set environment variable for password
$env:PGPASSWORD = $PgPassword

# Create backup using Docker Compose
try {
    docker compose -f $ComposeFile exec -T $PgService pg_dump -Fc -h $PgHost -p $PgPort -U $PgUser $PgDatabase | Out-File -FilePath $Out -Encoding ASCII
} catch {
    Write-Error "Failed to create backup: $_"
    exit 1
}

# Handle encryption if specified
if ($EncCmd) {
    Write-Host ">>> Encrypting backup"
    try {
        Invoke-Expression "$EncCmd < `"$Out`" > `"$Out.enc`""
        Get-FileHash -Path "$Out.enc" -Algorithm SHA256 | Select-Object -ExpandProperty Hash | Out-File -FilePath $Sha -Encoding ASCII
        Remove-Item $Out -Force
    } catch {
        Write-Error "Failed to encrypt backup: $_"
        exit 1
    }
} else {
    Write-Host ">>> Writing checksum"
    try {
        Get-FileHash -Path $Out -Algorithm SHA256 | Select-Object -ExpandProperty Hash | Out-File -FilePath $Sha -Encoding ASCII
    } catch {
        Write-Error "Failed to create checksum: $_"
        exit 1
    }
}

# Retention cleanup
Write-Host ">>> Retention: deleting backups older than $RetentionDays days"
try {
    $CutoffDate = (Get-Date).AddDays(-[int]$RetentionDays)
    Get-ChildItem -Path $BackupDir -Filter "zimmer-*.dump" | Where-Object { $_.LastWriteTime -lt $CutoffDate } | Remove-Item -Force
    Get-ChildItem -Path $BackupDir -Filter "*.sha256" | Where-Object { $_.LastWriteTime -lt $CutoffDate } | Remove-Item -Force
} catch {
    Write-Warning "Failed to clean up old backups: $_"
}

Write-Host "✅ Backup complete: $Out"
Get-ChildItem -Path $BackupDir | Format-Table Name, Length, LastWriteTime
