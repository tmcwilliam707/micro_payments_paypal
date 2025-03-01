import sqlite3

# Connect to database
conn = sqlite3.connect('paypal_micropayments_fixed.db')
cursor = conn.cursor()

# Check row count
cursor.execute("SELECT COUNT(*) FROM transactions")
print(f"Total transactions: {cursor.fetchone()[0]}")

# Preview first 5 rows
cursor.execute("SELECT * FROM transactions LIMIT 5")
for row in cursor.fetchall():
    print(row)

conn.close()