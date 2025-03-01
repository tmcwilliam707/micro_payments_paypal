import sqlite3
import random
from datetime import datetime, timedelta

# Connect and recreate database
conn = sqlite3.connect('paypal_micropayments_fixed.db')
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS transactions")
cursor.execute('''
    CREATE TABLE transactions (
        transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        transaction_amount REAL,
        transaction_date TEXT,
        payment_method TEXT,
        merchant_category TEXT,
        status TEXT,
        fee_amount REAL,
        timestamp TEXT,
        experiment_variant INTEGER
    )
''')

# Parameters
num_transactions = 50000
start_date = datetime(2025, 1, 1)
user_ids = range(1, 10001)
categories = ['Gaming', 'Content', 'Retail', 'Food', 'Services']
methods = ['PayPal Wallet', 'Credit Card', 'Debit Card']

# Generate data with explicit failure rates
data = []
for i in range(num_transactions):
    user_id = random.choice(user_ids)
    amount = random.choices(
        [random.uniform(0.5, 5), random.uniform(5, 20), random.uniform(20, 100)],
        weights=[0.4, 0.4, 0.2], k=1
    )[0]
    date = start_date + timedelta(days=random.randint(0, 59), hours=random.randint(0, 23))
    payment_method = random.choice(methods)
    merchant_category = random.choice(categories)
    variant = random.randint(0, 1)
    fee = 0.10 if (amount <= 5 and variant == 1) else (amount * 0.029 + 0.30)
    # Failure rates
    if amount <= 5:
        if variant == 0:
            status = random.choices(['completed', 'failed'], weights=[0.65, 0.35])[0]  # 35% failure
        else:
            status = random.choices(['completed', 'failed'], weights=[0.71, 0.29])[0]  # 29% failure
    else:
        status = random.choices(['completed', 'failed'], weights=[0.80, 0.20])[0]  # 20% failure

    data.append((user_id, amount, date.strftime('%Y-%m-%d'), payment_method, merchant_category,
                 status, fee, date.strftime('%Y-%m-%d %H:%M:%S'), variant))

# Insert and verify
cursor.executemany('INSERT INTO transactions VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?)', data)
conn.commit()

cursor.execute("SELECT COUNT(*) as total, SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failed "
               "FROM transactions")
total, failed = cursor.fetchone()
print(f"Total Transactions: {total}, Total Failures: {failed}, Overall Failure Rate: {failed/total:.2%}")

cursor.execute("SELECT experiment_variant, COUNT(*) as total, SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failed "
               "FROM transactions WHERE transaction_amount <= 5 GROUP BY experiment_variant")
print("Micropayment Failure Rates:")
for row in cursor.fetchall():
    print(f"Variant {row[0]}: {row[2]/row[1]:.2%} failure ({row[2]}/{row[1]})")

conn.close()