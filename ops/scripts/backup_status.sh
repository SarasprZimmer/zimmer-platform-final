#!/usr/bin/env bash
set -euo pipefail

# Backup status monitoring script
# Shows recent backups, sizes, and health status

BACKUP_DIR="ops/backup/archives"

echo "📊 Zimmer Backup Status Report"
echo "=============================="
echo ""

if [ ! -d "$BACKUP_DIR" ]; then
  echo "❌ Backup directory not found: $BACKUP_DIR"
  exit 1
fi

# Count backups
BACKUP_COUNT=$(find "$BACKUP_DIR" -name "zimmer-*.dump" | wc -l)
SHA_COUNT=$(find "$BACKUP_DIR" -name "*.sha256" | wc -l)

echo "📈 Backup Statistics:"
echo "  Total backups: $BACKUP_COUNT"
echo "  Checksum files: $SHA_COUNT"
echo ""

# Show recent backups
echo "📅 Recent Backups:"
if [ "$BACKUP_COUNT" -eq 0 ]; then
  echo "  No backups found"
else
  echo "  $(find "$BACKUP_DIR" -name "zimmer-*.dump" -printf "%T@ %p\n" | sort -nr | head -5 | while read timestamp file; do
    date=$(date -d "@${timestamp%.*}" '+%Y-%m-%d %H:%M:%S')
    size=$(du -h "$file" | cut -f1)
    echo "    $date - $size - $(basename "$file")"
  done)"
fi
echo ""

# Check for missing checksums
echo "🔍 Integrity Check:"
MISSING_CHECKSUMS=0
for dump in "$BACKUP_DIR"/zimmer-*.dump; do
  if [ -f "$dump" ]; then
    if [ -f "$dump.sha256" ]; then
      echo "  ✅ $(basename "$dump") - checksum present"
    else
      echo "  ❌ $(basename "$dump") - missing checksum"
      MISSING_CHECKSUMS=$((MISSING_CHECKSUMS + 1))
    fi
  fi
done

if [ "$MISSING_CHECKSUMS" -eq 0 ]; then
  echo "  All backups have checksums ✓"
else
  echo "  $MISSING_CHECKSUMS backups missing checksums"
fi
echo ""

# Check backup age
echo "⏰ Backup Age Analysis:"
LATEST_BACKUP=$(find "$BACKUP_DIR" -name "zimmer-*.dump" -printf "%T@ %p\n" | sort -nr | head -1 | cut -d' ' -f2)
if [ -n "$LATEST_BACKUP" ]; then
  LATEST_AGE=$(( ($(date +%s) - $(stat -c %Y "$LATEST_BACKUP")) / 3600 ))
  if [ "$LATEST_AGE" -lt 24 ]; then
    echo "  ✅ Latest backup is $LATEST_AGE hours old"
  elif [ "$LATEST_AGE" -lt 48 ]; then
    echo "  ⚠️  Latest backup is $LATEST_AGE hours old (consider running backup)"
  else
    echo "  ❌ Latest backup is $LATEST_AGE hours old (backup needed)"
  fi
else
  echo "  ❌ No backups found"
fi
echo ""

# Disk usage
echo "💾 Disk Usage:"
BACKUP_SIZE=$(du -sh "$BACKUP_DIR" | cut -f1)
echo "  Backup directory size: $BACKUP_SIZE"
echo ""

echo "🎯 Recommendations:"
if [ "$BACKUP_COUNT" -eq 0 ]; then
  echo "  • Run initial backup: bash ops/scripts/backup_db.sh"
elif [ "$MISSING_CHECKSUMS" -gt 0 ]; then
  echo "  • Regenerate missing checksums"
elif [ "$LATEST_AGE" -gt 48 ]; then
  echo "  • Run backup: bash ops/scripts/backup_db.sh"
else
  echo "  • Backup system is healthy ✓"
  echo "  • Consider testing restore: bash ops/scripts/test_restore.sh"
fi
