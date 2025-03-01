import pandas as pd
from scipy.stats import chi2_contingency

# Use your provided data directly
control_total = 10108.0
control_failed = 3531.0
variant_total = 9902.0
variant_failed = 2827.0

control_completed = control_total - control_failed
variant_completed = variant_total - variant_failed

# Contingency table
contingency = [
    [control_completed, control_failed],
    [variant_completed, variant_failed]
]

# Chi-squared test
chi2, p_value, dof, expected = chi2_contingency(contingency)
print(f"Chi-squared: {chi2:.3f}, P-value: {p_value:.3f}")

# Completion rates and lift
control_completion_rate = control_completed / control_total
variant_completion_rate = variant_completed / variant_total
lift = ((variant_completion_rate - control_completion_rate) / control_completion_rate) * 100
print(f"Control Completion Rate: {control_completion_rate:.2%}, Variant Completion Rate: {variant_completion_rate:.2%}, Lift: {lift:.2f}%")
print(f"Absolute Improvement in Completion Rate: {(variant_completion_rate - control_completion_rate)*100:.2f}%")

# Save for Tableau
results = pd.DataFrame({
    'Variant': ['Control', 'Variant'],
    'Total Transactions': [control_total, variant_total],
    'Failed Transactions': [control_failed, variant_failed],
    'Completion Rate': [control_completion_rate, variant_completion_rate]
})
results.to_csv('micropayment_fixed_stats.csv', index=False)
print("Results saved to 'micropayment_fixed_stats.csv'.")