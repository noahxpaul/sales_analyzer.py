# This is a sales analyzer that pulls from sales_data.csv. It calculates total revenue (quantity * price for each row, summed), revenue per product, total quantity sold per product, and the day with the highest total revenue. It will then output the results to a text file called sales_report.txt. It will write a summary csv called product_summary.csv with columns: product, total_quantity, total_revenue.



# Read sales data

import csv


sales_data = []

with open("sales_data.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        # Convert quantity and price to floats
        row["Quantity"] = float(row["Quantity"])
        row["Price"] = float(row["Price"])
        sales_data.append(row)

print(f"Loaded {len(sales_data)} sales records.")

# Calculate total revenue
total_revenue = sum(row["Quantity"] * row["Price"] for row in sales_data)
print(f"Total revenue: ${total_revenue:.2f}")

# Calculate revenue per product
product_revenue = {}
for row in sales_data:
    product = row["Product"]
    if product not in product_revenue:
        product_revenue[product] = 0
    product_revenue[product] += row["Quantity"] * row["Price"]

# Calculate total quantity sold per product
product_quantity = {}
for row in sales_data:
    product = row["Product"]
    if product not in product_quantity:
        product_quantity[product] = 0
    product_quantity[product] += row["Quantity"]

# Find the day with the highest total revenue
daily_revenue = {}
for row in sales_data:
    date = row["Date"]
    if date not in daily_revenue:
        daily_revenue[date] = 0
    daily_revenue[date] += row["Quantity"] * row["Price"]

highest_day = max(daily_revenue, key=daily_revenue.get)
print(f"Day with highest revenue: {highest_day} (${daily_revenue[highest_day]:.2f})")


# Write results to a text file
with open("sales_report.txt", "w") as file:
    file.write("SALES REPORT\n")
    file.write("=" * 40 + "\n\n")
    file.write(f"Total revenue: ${total_revenue:.2f}\n")
    file.write(f"Day with highest revenue: {highest_day} (${daily_revenue[highest_day]:.2f})\n\n")

    file.write("REVENUE BY PRODUCT:\n")
    for product, revenue in product_revenue.items():
        file.write(f" {product}: ${revenue:.2f}\n")

    file.write("\nQUANTITY SOLD BY PRODUCT:\n")
    for product, quantity in product_quantity.items():
        file.write(f" {product}: {quantity}\n")

print("\nReport written to sales_report.txt")

# Write summary to a CSV file
with open("product_summary.csv", "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["product", "total_quantity", "total_revenue"])
    writer.writeheader()

    for product in product_revenue:
        writer.writerow({
            "product": product,
            "total_quantity": product_quantity[product],
            "total_revenue": product_revenue[product]
        })

print("Summary written to product_summary.csv")


