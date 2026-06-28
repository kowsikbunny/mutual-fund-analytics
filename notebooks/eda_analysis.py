import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the cleaned data
fund_master = pd.read_csv("data/processed/fund_master_clean.csv")
nav_history = pd.read_csv("data/processed/nav_history_clean.csv")
transactions = pd.read_csv("data/processed/transactions_clean.csv")
scheme = pd.read_csv("data/processed/scheme_clean.csv")

# Display the first few rows of each DataFrame
print(fund_master.head())
print(nav_history.head())
print(transactions.head())
print(scheme.head())

print(fund_master.info())
print(nav_history.info())
print(transactions.info())
print(scheme.info())

print(fund_master.describe())
print(nav_history.describe())
print(transactions.describe())
print(scheme.describe())

print("Fund Master Missing Values")
print(fund_master.isnull().sum())
print("NAV History Missing Values")
print(nav_history.isnull().sum())
print("Transactions Missing Values")
print(transactions.isnull().sum())
print("Scheme Missing Values")
print(scheme.isnull().sum())

print("Fund Master Columns")
print(fund_master.columns.tolist())

print("NAV History Columns")
print(nav_history.columns.tolist())

print("Transactions Columns")
print(transactions.columns.tolist())

print("Scheme Columns")
print(scheme.columns.tolist())




# CHART -1 NAV TREND ANALUSIS
nav_history['date'] = pd.to_datetime(nav_history['date'])
avg_nav = nav_history.groupby('date')['nav'].mean()
plt.figure(figsize=(12, 6))
plt.plot(avg_nav.index, avg_nav.values, linewidth=2)
plt.title("Average NAV Trend (2022-2025)")
plt.xlabel("Date")
plt.ylabel("Average NAV")
plt.grid(True)
plt.tight_layout()
plt.show()


# CHART -2 AUM GROWTH BAR CHARTS
plt.figure(figsize=(12, 6))
aum_data =(
    scheme.groupby("fund_house")["aum_crore"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)
colors = ["red" if "SBI" in x else "steelblue" for x in aum_data.index]
plt.bar(aum_data.index, aum_data.values, color=colors)
plt.title("Top 10 Fund Houses by AUM(2022-2025)")
plt.xlabel("Fund House")
plt.ylabel("AUM (Crore)")
plt.xticks(rotation=45)

# highlight sbi
for i, value in enumerate(aum_data.values):
    if "SBI" in aum_data.index[i]:
        plt.text(i, value + 1000, "12.5lcr", ha='center',  color='red', fontweight='bold')
plt.tight_layout()
plt.show()




# CHART 3 - SIP INFLOW TIME SERIES
transactions["transaction_date"] = pd.to_datetime(transactions["transaction_date"])
sip_data = transactions[transactions["transaction_type"] == "SIP"].copy()
sip_data["month"] = sip_data["transaction_date"].dt.to_period("M").astype(str)
monthly_sip = sip_data.groupby("month")["amount_inr"].sum().reset_index()
plt.figure(figsize=(12, 6))
plt.plot(monthly_sip["month"], monthly_sip["amount_inr"], marker='o', color='blue',linewidth=2)
max_row = monthly_sip.loc[monthly_sip["amount_inr"].idxmax()]
plt.annotate("31,002cr(All-time High)", 
             xy=(max_row["month"], max_row["amount_inr"]), 
             xytext=(5, 15), 
             textcoords="offset points", arrowprops=dict(arrowstyle="->", color='red'),
             color='red', 
             fontsize=10 
            ) 
             
plt.title("Monthly SIP Inflow Trend ( jan2022-dec2025)")
plt.xlabel("Month")
plt.ylabel("SIP Inflow (INR)")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()


# ==========================
# CHART 4 - CATEGORY INFLOW HEATMAP
# ==========================

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Convert transaction date
transactions["transaction_date"] = pd.to_datetime(transactions["transaction_date"])

# Extract month
transactions["Month"] = transactions["transaction_date"].dt.strftime("%b-%Y")

# Merge transactions with fund categories
heatmap_data = transactions.merge(
    fund_master[["amfi_code", "category"]],
    on="amfi_code",
    how="left"
)

# Aggregate net SIP inflow
pivot_table = heatmap_data.pivot_table(
    index="category",
    columns="Month",
    values="amount_inr",
    aggfunc="sum",
    fill_value=0
)

# Arrange months chronologically
month_order = sorted(
    pivot_table.columns,
    key=lambda x: pd.to_datetime(x, format="%b-%Y")
)
pivot_table = pivot_table[month_order]

# Plot Heatmap
plt.figure(figsize=(14,6))

sns.heatmap(
    pivot_table,
    cmap="YlGnBu",
    annot=False,
    fmt=".0f",
    linewidths=0.5
)

plt.title("Category Inflow Heatmap")
plt.xlabel("Months")
plt.ylabel("Fund Categories")

plt.tight_layout()
plt.show()



# chat 5- INVESTOR AGE GROUP DISTRUBTION
plt.figure(figsize=(8,8))
age_data = transactions["age_group"].value_counts()
plt.pie(
    age_data,
    labels=age_data.index,
    autopct="%1.1f%%",
    startangle=90
)
plt.title("Investor Age Group Distrubution")
plt.tight_layout()
plt.show()



# ===========================
# CHART 6 - GEOGRAPHIC DISTRIBUTION
# ===========================

# 6A - Horizontal Bar Chart (SIP Amount by State)

state_data = (
    transactions.groupby("state")["amount_inr"]
    .sum()
    .sort_values(ascending=True)
)

plt.figure(figsize=(10,6))
plt.barh(
    state_data.index,
    state_data.values,
    color="steelblue",
    edgecolor="black"
)
plt.title("Geographic Distribution - SIP Amount by State")
plt.xlabel("Total SIP Amount (INR)")
plt.ylabel("State")
plt.tight_layout()
plt.show()


# 6B - T30 vs B30 City Tier Pie Chart

city_data = transactions["city_tier"].value_counts()

plt.figure(figsize=(7,7))
plt.pie(
    city_data,
    labels=city_data.index,
    autopct="%1.1f%%",
    startangle=90,
    wedgeprops={"edgecolor":"black"}
)
plt.title("T30 vs B30 City Tier Distribution")
plt.tight_layout()
plt.show()


# CHART 7 - FOLIO COUNT GROWTH
# Skipped because the dataset does not contain folio_count data.
# The project requirement mentions folio count from 13.26 Cr to 26.12 Cr,
# but this dataset does not have the required column.



# ===========================
# CHART 8 - NAV RETURN CORRELATION MATRIX
# ===========================

import seaborn as sns
import matplotlib.pyplot as plt

# Convert date column to datetime
nav_history["date"] = pd.to_datetime(nav_history["date"])

# Select first 10 funds
top_funds = nav_history["amfi_code"].unique()[:10]

# Filter data for selected funds
nav_data = nav_history[
    nav_history["amfi_code"].isin(top_funds)
]

# Create pivot table
pivot_df = nav_data.pivot(
    index="date",
    columns="amfi_code",
    values="nav"
)

# Calculate daily returns
daily_returns = pivot_df.pct_change().dropna()

# Correlation matrix
corr_matrix = daily_returns.corr()

# Plot Heatmap
plt.figure(figsize=(10,8))

sns.heatmap(
    corr_matrix,
    annot=True,
    cmap="coolwarm",
    linewidths=0.5,
    fmt=".2f"
)

plt.title("NAV Return Correlation Matrix")
plt.xlabel("AMFI Code")
plt.ylabel("AMFI Code")

plt.tight_layout()
plt.show()

# ==========================
# CHART 9 - SECTOR ALLOCATION DONUT CHART
# ==========================

import pandas as pd
import matplotlib.pyplot as plt

# Load portfolio holdings
portfolio = pd.read_csv("data/raw/09_portfolio_holdings.csv")

print(portfolio.columns.to_list())

# Aggregate sector weights
sector_data = portfolio.groupby("sector")["weight_pct"].sum()

# Plot Donut Chart
plt.figure(figsize=(8,8))

plt.pie(
    sector_data,
    labels=sector_data.index,
    autopct="%1.1f%%",
    startangle=90,
    wedgeprops=dict(width=0.4)
)

plt.title("Sector Allocation Across Equity Funds")

plt.tight_layout()
plt.show()