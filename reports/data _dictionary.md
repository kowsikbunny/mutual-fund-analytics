# Data Dictionary

## dim_fund
- amfi_code : Fund Code
- scheme_name : Mutual Fund Name
- fund_house : Fund House Name
- category : Fund Category
- plan : Plan Type

## fact_nav
- amfi_code : Fund Code
- date : NAV Date
- nav : Net Asset Value

## fact_transactions
- investor_id : Investor ID
- transaction_date : Transaction Date
- transaction_type : SIP/Lumpsum/Redemption
- amount_inr : Transaction Amount
- state : Investor State
- city : Investor City
- kyc_status : KYC Status

## fact_performance
- return_1yr_pct : 1 Year Return
- return_3yr_pct : 3 Year Return
- return_5yr_pct : 5 Year Return
- expense_ratio_pct : Expense Ratio
- aum_crore : Assets Under Management