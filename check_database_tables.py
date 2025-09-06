import sqlite3

# Check what tables exist
conn = sqlite3.connect('zimmer-backend/zimmer_dashboard.db')
cursor = conn.cursor()

print("Tables in database:")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
for row in cursor.fetchall():
    print(f"  - {row[0]}")

print("\nChecking for tickets table specifically:")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tickets'")
result = cursor.fetchone()
if result:
    print(f"  ✅ Tickets table exists: {result[0]}")
else:
    print("  ❌ Tickets table does NOT exist")

conn.close()
