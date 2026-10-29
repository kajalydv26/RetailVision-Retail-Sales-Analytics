import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load sales data
df = pd.read_csv("sales_data.csv")

# Remove duplicate records
df = df.drop_duplicates(subset="Order_ID")

# Convert dates into datetime format
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Convert numeric columns into numbers
df["Quantity"] = pd.to_numeric(
    df["Quantity"], errors="coerce"
)

df["Unit_Price"] = pd.to_numeric(
    df["Unit_Price"], errors="coerce"
)

# Remove invalid or missing records
df = df.dropna(
    subset=[
        "Date", "Quantity", "Unit_Price",
        "Product", "Category", "Region"
    ]
)

# Remove invalid quantities and prices
df = df[
    (df["Quantity"] > 0) &
    (df["Unit_Price"] >= 0)
]

# Calculate revenue after cleaning
df["Revenue"] = df["Quantity"] * df["Unit_Price"]

# Calculate total revenue
total_revenue = np.sum(df["Revenue"])

# Calculate total orders
total_orders = len(df)

# Calculate total quantity sold
total_quantity = np.sum(df["Quantity"])

print(df[["Order_ID", "Quantity", "Unit_Price", "Revenue"]])
print("Number of records:", len(df))  

# Calculate monthly sales
df["Month"] = df["Date"].dt.to_period("M").astype(str)

monthly_sales = df.groupby("Month")["Revenue"].sum()

# Create line chart
plt.figure(figsize=(8, 5))

plt.plot(
    monthly_sales.index,
    monthly_sales.values,
    marker="o"
)

plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Revenue (Rs.)")

plt.xticks(rotation=45)
plt.tight_layout()

plt.show()

# Display summary
print("SALES SUMMARY")
print("Total Revenue: Rs.", total_revenue)
print("Total Orders:", total_orders)
print("Total Quantity Sold:", total_quantity)

# Calculate sales by category

category_sales = df.groupby("Category")["Revenue"].sum()

# Create bar chart

plt.figure(figsize=(8, 5))

plt.bar(category_sales.index, category_sales.values)

plt.title("Sales by Product Category")
plt.xlabel("Product Category")
plt.ylabel("Revenue (Rs.)")

plt.tight_layout()
plt.show()

# Calculate sales by region

region_sales = df.groupby("Region")["Revenue"].sum()

# Create bar chart

plt.figure(figsize=(8, 5))

plt.bar(region_sales.index, region_sales.values)

plt.title("Sales by Region")
plt.xlabel("Region")
plt.ylabel("Revenue (Rs.)")

plt.tight_layout()
plt.show()

# Calculate sales by category

category_sales = df.groupby("Category")["Revenue"].sum()

# Create pie chart

plt.figure(figsize=(7, 7))

plt.pie(
category_sales.values,
labels=category_sales.index,
autopct="%1.1f%%",
startangle=90
)

plt.title("Sales Distribution by Category")
plt.tight_layout()
plt.show()

# Calculate monthly sales

monthly_sales = df.groupby("Month")["Revenue"].sum()

# Create area chart

plt.figure(figsize=(8, 5))

plt.fill_between(
monthly_sales.index,
monthly_sales.values,
alpha=0.5
)

plt.plot(
monthly_sales.index,
monthly_sales.values,
marker="o"
)

plt.title("Monthly Sales Area Chart")
plt.xlabel("Month")
plt.ylabel("Revenue (Rs.)")

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
