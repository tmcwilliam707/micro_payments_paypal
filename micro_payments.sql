WITH transaction_segments AS (
    SELECT 
        transaction_id,
        user_id,
        transaction_amount,
        CASE 
            WHEN transaction_amount <= 5 THEN 'Micropayment'
            WHEN transaction_amount <= 20 THEN 'Small'
            ELSE 'Large'
        END AS amount_segment,
        status,
        fee_amount,
        merchant_category,
        experiment_variant
    FROM transactions
)
SELECT 
    amount_segment,
    experiment_variant,
    COUNT(*) AS transaction_count,
    AVG(transaction_amount) AS avg_amount,
    COUNT(CASE WHEN status = 'failed' THEN 1 END) AS failed_count,
    AVG(fee_amount) AS avg_fee,
    COUNT(DISTINCT user_id) AS unique_users,
    merchant_category
FROM transaction_segments
GROUP BY amount_segment, experiment_variant, merchant_category
ORDER BY amount_segment, experiment_variant, transaction_count DESC;