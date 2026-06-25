-- 1. View Fund Master
SELECT * FROM dim_fund LIMIT 10;

-- 2. View NAV History
SELECT * FROM fact_nav LIMIT 10;

-- 3. View Transactions
SELECT * FROM fact_transactions LIMIT 10;

-- 4. View Scheme Performance
SELECT * FROM fact_performance LIMIT 10;

-- 5. Top 5 Funds by AUM
SELECT scheme_name, aum_crore
FROM fact_performance
ORDER BY aum_crore DESC
LIMIT 5;

-- 6. Average NAV
SELECT AVG(nav) AS avg_nav
FROM fact_nav;

-- 7. Total Transactions
SELECT COUNT(*) AS total_transactions
FROM fact_transactions;

-- 8. Total SIP Transactions
SELECT COUNT(*) AS sip_count
FROM fact_transactions
WHERE transaction_type = 'SIP';

-- 9. Average Expense Ratio
SELECT AVG(expense_ratio_pct) AS avg_expense_ratio
FROM fact_performance;

-- 10. Highest 1-Year Return
SELECT scheme_name, return_1yr_pct
FROM fact_performance
ORDER BY return_1yr_pct DESC
LIMIT 5;