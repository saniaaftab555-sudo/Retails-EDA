"""
Exploratory Data Analysis (EDA) on Retail Sales Data
=====================================================
Covers: Data Loading & Cleaning, Descriptive Statistics,
        Time Series Analysis, Customer & Product Analysis,
        Visualizations, and Recommendations.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from pathlib import Path

# ── Output folder ────────────────────────────────────────────────────────────
OUT = Path("eda_outputs")
OUT.mkdir(exist_ok=True)

sns.set_theme(style="whitegrid", palette="Set2")
plt.rcParams.update({"figure.dpi": 130, "figure.figsize": (10, 5)})


# ═══════════════════════════════════════════════════════════════════════════════
# 1. DATA LOADING & CLEANING
# ═══════════════════════════════════════════════════════════════════════════════
print("=" * 60)
print("1. DATA LOADING & CLEANING")
print("=" * 60)

df = pd.read_csv("retail_sales_dataset.csv")

print(f"\nShape : {df.shape}")
print(f"\nColumn dtypes:\n{df.dtypes}")
print(f"\nFirst 5 rows:\n{df.head()}")

# Parse date
df["Date"] = pd.to_datetime(df["Date"])
df["Year"]  = df["Date"].dt.year
df["Month"] = df["Date"].dt.month
df["Month_Name"] = df["Date"].dt.strftime("%b")
df["Quarter"] = df["Date"].dt.quarter

# Missing values
print(f"\nMissing values:\n{df.isnull().sum()}")
df.dropna(inplace=True)

# Duplicates
n_dup = df.duplicated().sum()
print(f"\nDuplicate rows: {n_dup}")
df.drop_duplicates(inplace=True)

print(f"\nClean shape: {df.shape}")


# ═══════════════════════════════════════════════════════════════════════════════
# 2. DESCRIPTIVE STATISTICS
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("2. DESCRIPTIVE STATISTICS")
print("=" * 60)

numeric_cols = ["Age", "Quantity", "Price per Unit", "Total Amount"]

desc = df[numeric_cols].describe().T
desc["median"] = df[numeric_cols].median()
desc["mode"]   = df[numeric_cols].mode().iloc[0]
print(f"\n{desc.round(2)}")

print(f"\nTotal Revenue : ${df['Total Amount'].sum():,.2f}")
print(f"Avg Order Value: ${df['Total Amount'].mean():,.2f}")
print(f"Median Order   : ${df['Total Amount'].median():,.2f}")


# ═══════════════════════════════════════════════════════════════════════════════
# 3. TIME SERIES ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("3. TIME SERIES ANALYSIS")
print("=" * 60)

monthly = (
    df.groupby(df["Date"].dt.to_period("M"))["Total Amount"]
    .sum()
    .reset_index()
)
monthly["Date"] = monthly["Date"].dt.to_timestamp()

# Rolling 3-month average
monthly["Rolling_3M"] = monthly["Total Amount"].rolling(3, min_periods=1).mean()

fig, ax = plt.subplots()
ax.plot(monthly["Date"], monthly["Total Amount"], marker="o", label="Monthly Revenue", linewidth=2)
ax.plot(monthly["Date"], monthly["Rolling_3M"], linestyle="--", color="tomato", label="3-Month Rolling Avg")
ax.set_title("Monthly Sales Revenue with 3-Month Rolling Average")
ax.set_xlabel("Month")
ax.set_ylabel("Revenue ($)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(OUT / "01_monthly_revenue.png")
plt.close()
print("Saved: 01_monthly_revenue.png")

# Quarterly breakdown
quarterly = df.groupby(["Year", "Quarter"])["Total Amount"].sum().reset_index()
quarterly["Period"] = quarterly["Year"].astype(str) + " Q" + quarterly["Quarter"].astype(str)
fig, ax = plt.subplots()
sns.barplot(data=quarterly, x="Period", y="Total Amount", ax=ax)
ax.set_title("Quarterly Revenue")
ax.set_ylabel("Revenue ($)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(OUT / "02_quarterly_revenue.png")
plt.close()
print("Saved: 02_quarterly_revenue.png")


# ═══════════════════════════════════════════════════════════════════════════════
# 4. CUSTOMER & PRODUCT ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("4. CUSTOMER & PRODUCT ANALYSIS")
print("=" * 60)

# -- 4a. Gender split
gender_rev = df.groupby("Gender")["Total Amount"].sum()
print(f"\nRevenue by Gender:\n{gender_rev}")

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
gender_rev.plot.pie(ax=axes[0], autopct="%1.1f%%", startangle=90)
axes[0].set_title("Revenue Share by Gender")
axes[0].set_ylabel("")

# -- 4b. Age distribution
axes[1].hist(df["Age"], bins=20, color=sns.color_palette("Set2")[1], edgecolor="white")
axes[1].set_title("Customer Age Distribution")
axes[1].set_xlabel("Age")
axes[1].set_ylabel("Count")
plt.tight_layout()
plt.savefig(OUT / "03_gender_age.png")
plt.close()
print("Saved: 03_gender_age.png")

# Age groups
df["Age Group"] = pd.cut(df["Age"], bins=[17, 25, 35, 45, 55, 65],
                          labels=["18-25", "26-35", "36-45", "46-55", "56-65"])
age_rev = df.groupby("Age Group", observed=True)["Total Amount"].sum().reset_index()
fig, ax = plt.subplots()
sns.barplot(data=age_rev, x="Age Group", y="Total Amount", ax=ax)
ax.set_title("Revenue by Age Group")
ax.set_ylabel("Revenue ($)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
plt.tight_layout()
plt.savefig(OUT / "04_revenue_by_age_group.png")
plt.close()
print("Saved: 04_revenue_by_age_group.png")

# -- 4c. Product Category
cat_stats = df.groupby("Product Category").agg(
    Revenue=("Total Amount", "sum"),
    Orders=("Transaction ID", "count"),
    Avg_Order=("Total Amount", "mean")
).sort_values("Revenue", ascending=False)
print(f"\nProduct Category Stats:\n{cat_stats.round(2)}")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
cat_stats["Revenue"].sort_values().plot.barh(ax=axes[0], color=sns.color_palette("Set2"))
axes[0].set_title("Revenue by Product Category")
axes[0].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))

cat_stats["Orders"].sort_values().plot.barh(ax=axes[1], color=sns.color_palette("Set2"))
axes[1].set_title("Order Count by Product Category")
plt.tight_layout()
plt.savefig(OUT / "05_product_category.png")
plt.close()
print("Saved: 05_product_category.png")

# -- 4d. Gender × Category heatmap
pivot_gc = df.pivot_table(index="Product Category", columns="Gender",
                           values="Total Amount", aggfunc="sum")
fig, ax = plt.subplots(figsize=(8, 4))
sns.heatmap(pivot_gc, annot=True, fmt=",.0f", cmap="YlOrRd", ax=ax)
ax.set_title("Revenue Heatmap: Category × Gender")
plt.tight_layout()
plt.savefig(OUT / "06_heatmap_category_gender.png")
plt.close()
print("Saved: 06_heatmap_category_gender.png")

# -- 4e. Monthly category trend
cat_monthly = (
    df.groupby([df["Date"].dt.to_period("M"), "Product Category"])["Total Amount"]
    .sum()
    .reset_index()
)
cat_monthly["Date"] = cat_monthly["Date"].dt.to_timestamp()
fig, ax = plt.subplots(figsize=(12, 5))
for cat, grp in cat_monthly.groupby("Product Category"):
    ax.plot(grp["Date"], grp["Total Amount"], marker="o", label=cat)
ax.set_title("Monthly Revenue by Product Category")
ax.set_ylabel("Revenue ($)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(OUT / "07_category_monthly_trend.png")
plt.close()
print("Saved: 07_category_monthly_trend.png")

# -- 4f. Quantity vs. Price scatter
fig, ax = plt.subplots()
for cat, grp in df.groupby("Product Category"):
    ax.scatter(grp["Price per Unit"], grp["Quantity"], label=cat, alpha=0.5, s=30)
ax.set_title("Price per Unit vs. Quantity Sold")
ax.set_xlabel("Price per Unit ($)")
ax.set_ylabel("Quantity")
ax.legend()
plt.tight_layout()
plt.savefig(OUT / "08_price_vs_quantity.png")
plt.close()
print("Saved: 08_price_vs_quantity.png")

# -- 4g. Correlation heatmap
fig, ax = plt.subplots(figsize=(6, 4))
sns.heatmap(df[numeric_cols].corr(), annot=True, cmap="coolwarm", ax=ax, vmin=-1, vmax=1)
ax.set_title("Correlation Matrix")
plt.tight_layout()
plt.savefig(OUT / "09_correlation_matrix.png")
plt.close()
print("Saved: 09_correlation_matrix.png")


# ═══════════════════════════════════════════════════════════════════════════════
# 5. TOP-N SUMMARIES
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("5. TOP CUSTOMERS BY REVENUE")
print("=" * 60)

top_customers = (
    df.groupby("Customer ID")["Total Amount"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)
print(top_customers)

fig, ax = plt.subplots()
sns.barplot(data=top_customers, x="Total Amount", y="Customer ID", ax=ax)
ax.set_title("Top 10 Customers by Revenue")
ax.set_xlabel("Total Revenue ($)")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
plt.tight_layout()
plt.savefig(OUT / "10_top_customers.png")
plt.close()
print("Saved: 10_top_customers.png")


# ═══════════════════════════════════════════════════════════════════════════════
# 6. RECOMMENDATIONS
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("6. RECOMMENDATIONS")
print("=" * 60)

top_cat = cat_stats["Revenue"].idxmax()
top_age = age_rev.sort_values("Total Amount", ascending=False)["Age Group"].iloc[0]
peak_month = monthly.sort_values("Total Amount", ascending=False)["Date"].iloc[0].strftime("%B %Y")

print(f"""
Based on the EDA:

1. Focus marketing on '{top_cat}' — it drives the highest revenue.
2. The '{top_age}' age group is the most valuable segment; tailor promotions for them.
3. Sales peaked in {peak_month}; plan inventory & campaigns around this period.
4. Gender revenue is roughly split — consider balanced product assortments.
5. High-price items show lower quantity; bundling or installment offers may help.
6. Loyalty programs for top customers can improve retention and LTV.
""")

print(f"\nAll charts saved to '{OUT}/' folder.")
