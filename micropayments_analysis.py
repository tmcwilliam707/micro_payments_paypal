import sqlite3
import pandas as pd

conn = sqlite3.connect('paypal_micropayments_fixed.db')
query = """
    SELECT 
        transaction_id,
        user_id,
        transaction_amount,
        CASE 
            WHEN transaction_amount <= 5 THEN 'Micropayment'
            WHEN transaction_amount <= 20 THEN 'Small'
            ELSE 'Large'
        END AS amount_segment,
        transaction_date,
        payment_method,
        merchant_category,
        status,
        fee_amount,
        timestamp,
        experiment_variant
    FROM transactions;
"""
df = pd.read_sql_query(query, conn)
df.to_csv('micropayment_fixed_analysis.csv', index=False)
conn.close()
print(f"Exported {len(df)} rows to 'micropayment_fixed_analysis.csv'.")