# ============================================================
# NOVAMART RETAIL ANALYTICS
# analysis.py (Part 1A)
# Author: Praneeth Koduru
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ============================================================
# LOAD DATA
# ============================================================

print("=" * 60)
print("NOVAMART RETAIL ANALYTICS")
print("=" * 60)

customers = pd.read_csv("customers.csv")
transactions = pd.read_csv("transactions.csv")

print("\nData Loaded Successfully\n")

print("Customers Shape :", customers.shape)
print("Transactions Shape :", transactions.shape)

# ============================================================
# PREVIEW
# ============================================================

print("\nCustomers")
print(customers.head())

print("\nTransactions")
print(transactions.head())

# ============================================================
# DATA TYPES
# ============================================================

print("\nCustomer Data Types")
print(customers.dtypes)

print("\nTransaction Data Types")
print(transactions.dtypes)

# ============================================================
# CONVERT DATES
# ============================================================

customers["Join_Date"] = pd.to_datetime(customers["Join_Date"])
transactions["Date"] = pd.to_datetime(transactions["Date"])

# ============================================================
# REMOVE DUPLICATES
# ============================================================

customers = customers.drop_duplicates()
transactions = transactions.drop_duplicates()

# ============================================================
# HANDLE MISSING VALUES
# ============================================================

customers.fillna(
    {
        "Membership": "Bronze",
        "City": "Unknown"
    },
    inplace=True
)

transactions.fillna(
    {
        "Discount_%": 0
    },
    inplace=True
)

# ============================================================
# FEATURE ENGINEERING
# ============================================================

transactions["Year"] = transactions["Date"].dt.year
transactions["Month"] = transactions["Date"].dt.month
transactions["Month_Name"] = transactions["Date"].dt.strftime("%b")
transactions["Quarter"] = transactions["Date"].dt.quarter
transactions["Weekday"] = transactions["Date"].dt.day_name()

customers["Customer_Age"] = (
    pd.Timestamp.today().year -
    customers["Join_Date"].dt.year
)

# ============================================================
# CHECK DATA QUALITY
# ============================================================

print("\nMissing Values\n")

print(customers.isnull().sum())

print()

print(transactions.isnull().sum())

# ============================================================
# KPI CALCULATIONS
# ============================================================

total_revenue = transactions["Amount"].sum()

total_orders = len(transactions)

unique_customers = transactions["Customer_ID"].nunique()

average_order_value = (
    total_revenue /
    total_orders
)

average_customer_value = (
    total_revenue /
    unique_customers
)

total_quantity = transactions["Quantity"].sum()

average_discount = transactions["Discount_%"].mean()

# ============================================================
# PRINT KPIs
# ============================================================

print("\n" + "=" * 60)

print("KEY PERFORMANCE INDICATORS")

print("=" * 60)

print(f"Revenue                : ${total_revenue:,.2f}")

print(f"Orders                 : {total_orders:,}")

print(f"Customers              : {unique_customers:,}")

print(f"Items Sold             : {total_quantity:,}")

print(f"Average Order Value    : ${average_order_value:,.2f}")

print(f"Customer Value         : ${average_customer_value:,.2f}")

print(f"Average Discount       : {average_discount:.2f}%")

# ============================================================
# MEMBERSHIP DISTRIBUTION
# ============================================================

membership_summary = (
    customers["Membership"]
    .value_counts()
    .reset_index()
)

membership_summary.columns = [
    "Membership",
    "Customers"
]

print("\nMembership Distribution\n")

print(membership_summary)

# ============================================================
# CITY DISTRIBUTION
# ============================================================

city_summary = (
    customers
    .groupby("City")
    .size()
    .sort_values(ascending=False)
)

print("\nTop Cities\n")

print(city_summary)

# ============================================================
# CATEGORY SUMMARY
# ============================================================

category_summary = (
    transactions
    .groupby("Category")
    .agg(
        Revenue=("Amount","sum"),
        Orders=("Order_ID","count"),
        Quantity=("Quantity","sum")
    )
    .sort_values(
        by="Revenue",
        ascending=False
    )
)

print("\nCategory Summary\n")

print(category_summary)

# ============================================================
# PAYMENT METHOD
# ============================================================

payment_summary = (
    transactions["Payment_Method"]
    .value_counts()
)

print("\nPayment Methods\n")

print(payment_summary)

# ============================================================
# MONTHLY REVENUE
# ============================================================

monthly_revenue = (
    transactions
    .groupby(["Year","Month"])["Amount"]
    .sum()
    .reset_index()
)

print("\nMonthly Revenue\n")

print(monthly_revenue.head())

# ============================================================
# EXPORT CLEAN DATA
# ============================================================

Path("output").mkdir(exist_ok=True)

customers.to_csv(
    "output/customers_clean.csv",
    index=False
)

transactions.to_csv(
    "output/transactions_clean.csv",
    index=False
)

category_summary.to_csv(
    "output/category_summary.csv"
)

monthly_revenue.to_csv(
    "output/monthly_revenue.csv",
    index=False
)

print("\nCleaned files saved successfully.")

# ============================================================
# SIMPLE KPI CHART
# ============================================================

plt.figure(figsize=(10,5))

plt.bar(
    ["Revenue","Orders","Customers"],
    [
        total_revenue,
        total_orders,
        unique_customers
    ]
)

plt.title("Business KPIs")

plt.tight_layout()

plt.savefig(
    "output/business_kpis.png",
    dpi=300
)

plt.close()

print("\nBusiness KPI chart saved.")

print("\nPart 1A Completed Successfully.")
