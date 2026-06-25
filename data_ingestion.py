import pandas as pd

# Load datasets
fund_master = pd.read_csv("data/raw/01_fund_master.csv")
nav_history = pd.read_csv("data/raw/02_nav_history.csv")
aum = pd.read_csv("data/raw/03_aum_by_fund_house.csv")
sip = pd.read_csv("data/raw/04_monthly_sip_inflows.csv")
category = pd.read_csv("data/raw/05_category_inflows.csv")
industry = pd.read_csv("data/raw/06_industry_folio_count.csv")
scheme = pd.read_csv("data/raw/07_scheme_performance.csv")
transactions = pd.read_csv("data/raw/08_investor_transactions.csv")
portfolio = pd.read_csv("data/raw/09_portfolio_holdings.csv")
benchmark = pd.read_csv("data/raw/10_benchmark_indices.csv")

print("All datasets loaded successfully!")

print("Fund Master:", fund_master.shape)
print("NAV History:", nav_history.shape)
print("AUM:", aum.shape)
print("SIP:", sip.shape)
print("Category:", category.shape)
print("Industry:", industry.shape)
print("Scheme:", scheme.shape)
print("Transactions:", transactions.shape)
print("Portfolio:", portfolio.shape)
print("Benchmark:", benchmark.shape)
print(nav_history.head())
nav_history["date"]=pd.to_datetime(nav_history["date"])
nav_history = nav_history.sort_values(by=["amfi_code", "date"])
nav_history = nav_history.drop_duplicates()
nav_history = nav_history[nav_history["nav"] > 0]
nav_history["nav"] = nav_history .groupby("amfi_code")["nav"].ffill()
print("Valid NAV records:", nav_history.shape)
print(nav_history.info())

print(transactions.head())
transactions["transaction_date"]=pd.to_datetime(transactions["transaction_date"])
print(transactions["transaction_type"].unique())
print(transactions["kyc_status"].unique())
#print(transactions.info())


print(scheme.head())
scheme["return_1yr_pct"] = pd.to_numeric(scheme["return_1yr_pct"], errors="coerce")
scheme["return_3yr_pct"] = pd.to_numeric(scheme["return_3yr_pct"], errors="coerce")
scheme["return_5yr_pct"] = pd.to_numeric(scheme["return_5yr_pct"], errors="coerce")
print(scheme.info())


print(scheme ["expense_ratio_pct"].describe())
print(scheme[scheme["expense_ratio_pct"]>2.5])

fund_master.to_csv("data/processed/fund_master_clean.csv",index=False)
nav_history.to_csv("data/processed/nav_history_clean.csv",index=False)
transactions.to_csv("data/processed/transactions_clean.csv",index=False)
scheme.to_csv("data/processed/scheme_clean.csv",index=False)

print("All cleaned files saved successfully!")