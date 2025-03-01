import sqlite3

conn = sqlite3.connect('paypal_micropayments_fixed.db')
cursor = conn.cursor()
cursor.execute("SELECT experiment_variant, COUNT(*) as total, SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failed "
               "FROM transactions WHERE transaction_amount <= 5 GROUP BY experiment_variant")
print("Micropayment Failure Rates:")
for row in cursor.fetchall():
    print(f"Variant {row[0]}: {row[2]/row[1]:.2%} failure ({row[2]}/{row[1]})")
conn.close()