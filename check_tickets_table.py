import sqlite3

# Check tickets table
conn = sqlite3.connect('zimmer_dashboard.db')
cursor = conn.cursor()

print("Tickets table schema:")
cursor.execute('PRAGMA table_info(tickets)')
for row in cursor.fetchall():
    print(row)

print("\nTickets count:")
cursor.execute('SELECT COUNT(*) FROM tickets')
print(f"Total tickets: {cursor.fetchone()[0]}")

print("\nSample tickets:")
cursor.execute('SELECT * FROM tickets LIMIT 3')
for row in cursor.fetchall():
    print(row)

conn.close()
