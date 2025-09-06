import sqlite3

# Check tickets table data
conn = sqlite3.connect('zimmer-backend/zimmer_dashboard.db')
cursor = conn.cursor()

print("Tickets table schema:")
cursor.execute('PRAGMA table_info(tickets)')
for row in cursor.fetchall():
    print(f"  {row[1]} ({row[2]}) - {'NOT NULL' if row[3] else 'NULL'}")

print("\nTickets count:")
cursor.execute('SELECT COUNT(*) FROM tickets')
count = cursor.fetchone()[0]
print(f"Total tickets: {count}")

if count > 0:
    print("\nSample tickets:")
    cursor.execute('SELECT * FROM tickets LIMIT 3')
    for row in cursor.fetchall():
        print(f"  {row}")
else:
    print("No tickets found in database")

conn.close()
